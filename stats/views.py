import os

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView

from .git_checkout import checkout_repo
from .forms import RequestProcessingForm
from .parser import process_repo

class HomeView(View):

    def get(self, request, *args, **kwargs):
        return None

class ViewResultsView(TemplateView):
    template_name = "view_processing.html"
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super(ViewResultsView, self).get_context_data(**kwargs)
        context['results'] = self.request.session['quantities']
        return context

class RequestProccessingView(FormView):
    form_class = RequestProcessingForm
    template_name = "request_processing.html"
    success_url = reverse_lazy('stats:view-results')

    def form_valid(self, form):
        repo_data = form.cleaned_data
        self.request.session['repo_data'] = repo_data

        repo_directory = checkout_repo(repo_data['repo_url'], repo_data['username'], repo_data['repo_name'])
        self.request.session['quantities'] = process_repo(repo_directory)

        return super(RequestProccessingView, self).form_valid(form)
