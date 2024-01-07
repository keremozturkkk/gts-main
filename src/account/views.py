from django.http import *
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from django.urls import reverse

from .forms import RegistrationForm

from .decorators import unauthenticated_user

# Create your views here.

@unauthenticated_user
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('panel:home')
        else:
            messages.info(request, "Username or password is wrong.")
    
    return render(request, 'account/pages/login.html', {})

def logout_view(request):
    logout(request)
    return redirect('account:login')

@unauthenticated_user
def signup_view(request):
    
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, "Account named " + username + " has been created successfully.")
            return redirect('account:login')

    context = {'form': form}

    return render(request, 'account/pages/signup.html', context)
