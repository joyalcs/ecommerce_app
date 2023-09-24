from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Signupform, LoginForm
# Create your views here.

class SignupView(CreateView):
    form_class = Signupform
    success_url = reverse_lazy('signin')
    template_name = 'user/signup.html'

class LoginView(View):
    def get(self, request):
        form = LoginForm(request.POST)
        return render(request, 'user/signin.html', {'form':form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Successfull completed log")
                return redirect('core:home')
            else:
                messages.error(request, "There are some problems with login credentials")
        return render(request, 'user/signin.html', {'form':form})
@login_required
def logoutview(request):
    logout(request)
    messages.success(request, 'Sucessfully logout')
    return redirect('user:signin')


