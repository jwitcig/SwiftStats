from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView

from .forms import CreateUserForm, LoginForm

class CreateUserView(FormView):
    form_class = CreateUserForm
    template_name = "new_user.html"
    success_url = reverse_lazy('login:login')

    def form_valid(self, form):

        User.objects.create_user(**form.cleaned_data).save()

        return super(CreateUserView, self).form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = reverse_lazy('stats:request-processing')

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)

        if user is not None:
            return HttpResponseRedirect(reverse('stats:request-processing'))

            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            return HttpResponseRedirect(reverse('login:login'))

        return super(LoginView, self).form_valid(form)
