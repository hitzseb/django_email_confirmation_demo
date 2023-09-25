import secrets
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from .forms import RegisterForm

# Home

def home_view(request):
    return render(request, 'home.html')

# Dashboard

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

# Register

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.confirmation_token = secrets.token_urlsafe(32)
            user.username = user.email
            user.save()
            subject = 'Confirma tu cuenta'
            message = f'Por favor, sigue este enlace para confirmar tu cuenta: http://127.0.0.1:8000/confirm/{user.confirmation_token}'
            from_email = 'hitzseb.test@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout
 
def logout_view(request):
    logout(request)
    return redirect('home')

# Email confirmation

def confirm_email(request, token):
    User = get_user_model()
    try:
        user = User.objects.get(confirmation_token=token)
    except User.DoesNotExist:
        return HttpResponse('Token inválido')
    user.is_active = True
    user.save()
    return HttpResponse('Tu cuenta ha sido activada')