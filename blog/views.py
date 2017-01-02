import shutil
import gzip
import os

from zipfile import ZipFile
import itertools
import requests

from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .models import *
from .forms import *


def blog_home(request):
    context = {}

    # TODO is 5 enough?
    context['posts'] = Post.objects.published_visible_posts(include_intro=True)[:5]

    if request.GET.get('serr') == '1':
        context['bad_post'] = True

    return render(request, 'blog_home.html', context)


def all_posts(request):
    context = {}

    # TODO is 5 enough?
    posts = Post.objects.published_visible_posts(include_intro=True)
    dates = [ (post, post.posted.strftime('%Y-%m')) for post in posts ]

    post_dict = {}
    for key, group in itertools.groupby(dates, key=lambda x: x[1][:11]):
        post_dict[key] = list(group)

    print post_dict
    context['posts'] = post_dict

    return render(request, 'all_posts.html', context)


def upload_images(request):
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return HttpResponseRedirect('/')

    context = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            count = upload_images_from_zip(file=request.FILES['file'] )
            if count:
                context['success'] = count
            else:
                context['failure'] = 'form valid but had upload process had errors.'

    return render(request, 'upload_images.html', context)


def post_detail(request, slug):
    context = {}
    context['GOOGLE_CAPTCHA_CLIENT'] = settings.GOOGLE_CAPTCHA_CLIENT
    
    if request.GET.get('cmts', False):
        context['go_to_comments'] = True

    try:
        if slug == "intro":
            post = Post.objects.get(slug=slug)
        else:
            post = Post.objects.published_visible_posts().get(slug=slug)
    except Post.DoesNotExist, e:
        return HttpResponseRedirect('/jerusalem/?serr=1')

    # post.update_statistics(request.session._get_or_create_session_key())
    if request.POST:
        print "in post"
        form = CommentForm(request.POST)
        google_verify = request.POST.get('g-recaptcha-response', False)
        # print 'google_verify', google_verify
        
        if not google_verify:
            print 'bad_google'
            context['bad_google'] = True

        elif form.is_valid():
            print 'valid form'
            body = form.cleaned_data.get('body', '').strip()
            author = form.cleaned_data.get('author', '').strip()
            post_data = {
                'secret': settings.GOOGLE_CAPTCHA_SECRET,
                'response': google_verify,
            }
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=post_data).json()

            print 'resp', resp

            if resp.get('success', False) and author and body:
                print 'everything worked great! should create'
                new_comment = Comment.objects.create(
                    post=post,
                    author=author,
                    body=body,
                    parent_comment=None
                )

                return HttpResponseRedirect('/jerusalem/p/%s/?cmts=dc' % post.slug)
            # 
        else:
            print form.errors



    context['post'] = post

    return render(request, 'post_detail.html', context)


def upload_images_from_zip(file):
    if not file:
        print "Fail! You need to pass in a zip file object."
        return 0

    date_str = datetime.datetime.now().strftime("%y.%m.%d-%H.%M.%S")
    dir_name = "%s/%s" % (settings.MEDIA_ROOT, date_str)
    delete_dir_name = "%s" % dir_name

    # ZipFile takes either a file path or a file-like object
    with ZipFile(file) as myzip:
        myzip.extractall(path=dir_name)

    zip_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]

    # if there's nothing in the unzipped folder
    if len(zip_files) is 0:
        # check if there is a folder with the same name as the zip folder
        zip_file_name, extension = os.path.splitext(file.name)
        if zip_file_name in [f for f in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, f))]:
            dir_name = "%s/%s" % (dir_name, zip_file_name)
            zip_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))]
    count = 0
    for unzipped in zip_files:
        file_name, extension = os.path.splitext(unzipped)
        if not extension in ['.jpg', '.png', '.jpeg']:
            continue
    
        new_post_image = PostImage.objects.create(title=file_name)
        new_post_image.image_file.save(
            unzipped, 
            File( open( os.path.join(dir_name, unzipped), 'rb' ) ) 
        )
        new_post_image.save()
        count += 1

    shutil.rmtree(delete_dir_name)

    print "done"
    return count

