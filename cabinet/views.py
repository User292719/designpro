from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect

from .forms import *

class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())


class RegisterView(TemplateView):
    form_class = UserForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            user =form.save(commit=False)

            user.first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)

            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/")


        return render(request, self.template_name, locals())



class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")