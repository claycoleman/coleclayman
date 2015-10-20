from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from portfolio.models import Category, Project
from portfolio.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def home(request):
    context = {}
    projects = Project.objects.all()
    for project in projects:
        project.create_slug()
        print project
    context['projects'] = projects
    categories = Category.objects.all()
    for category in categories:
        category.create_slug()
    context['categories'] = categories
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        print "hello"
        if form.is_valid():
            print 'yikes'
            send_mail("coleclayman portfolios: %s" % form.cleaned_data['name'], form.cleaned_data['message'] + "\n" + form.cleaned_data['phone'], form.cleaned_data['email'], [settings.EMAIL_HOST_USER], fail_silently=False)
            return render(request, 'thanks.html')
    else:
        form = ContactForm()
        context['form'] = form


    return render_to_response('home.html', context, context_instance=RequestContext(request))


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['projects'] = Project.objects.all()[:4]

        return context