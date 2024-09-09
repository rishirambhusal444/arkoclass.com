# authentic/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def auth(request):
    form = CustomUserCreationForm()
    
    return render(request, 'reg_login.html', {'register_form': form, 'show_register': True})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'reg_login.html', {'login_form': form, 'show_login': True})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user immediately after registration
            return redirect('home')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'Invalid registration form submission.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'reg_login.html', {'register_form': form, 'show_register': True})

def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('home')  # Replace 'home' with your desired redirect URL
