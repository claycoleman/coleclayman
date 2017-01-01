from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import *


def blog_home(request):
    context = {}

    # TODO is 5 enough?
    context['posts'] = Post.objects.published_visible_posts()[:5]

    if request.GET.get('serr') == '1':
        context['bad_post'] = True

    return render(request, 'blog_home.html', context)


def post_detail(request, slug):
    context = {}

    try:
        if slug == "intro":
            post = Post.objects.get(slug=slug)
        else:
            post = Post.objects.published_visible_posts().get(slug=slug)
    except Post.DoesNotExist, e:
        return HttpResponseRedirect('/jerusalem/?serr=1')

    # post.update_statistics(request.session._get_or_create_session_key())

    context['post'] = post

    return render(request, 'post_detail.html', context)