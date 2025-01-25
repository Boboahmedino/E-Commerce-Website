from email import message
from genericpath import exists
from django import conf, views
from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib import auth
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import re
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        confirm_password = request.POST['confirm_password']


        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                print('Username has been used')
                messages.warning(request, 'Username has been used!')
                return redirect('register')
            
            elif User.objects.filter(email = email).exists():
                print('Email has been used')
                messages.warning(request, 'Email has been used!')
                return redirect('register')
            
            elif User.objects.filter(first_name = first_name).exists():
                print('Phone Number has been used')
                messages.warning(request, 'Phone Number has been used!')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, first_name = first_name, password=password)
                user.set_password(password)
                user.is_active = True
                user.save()
                print('User account created')
                messages.success(request, f'{user} your account has been created, please sign in')
                return redirect('login')
            
        elif len(password) < 6:
            print('password too short')
            messages.error(request, 'Password too short, It should be 6 or more characters')
            return redirect('register')
        
        else:
            print("Password doesn't match")
            messages.error(request, "Password doesn't match")
            return redirect('register')
        
    else:
        return render(request, 'authentication/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '') # Safely get email
        password = request.POST.get('password', '')  # Safely get password

        if email:  # Ensure email is not empty
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                # Authenticate using email (after fetching user from email)
                user = auth.authenticate(username=user.username, password=password)

                if user is not None:
                    auth.login(request, user)
                    print(f'Welcome! {user} you are now logged in')
                    messages.success(request, f'Welcome! {user} you are now logged in')
                    return redirect('shop')

                else:
                    print('Your email or password is incorrect, please try again')
                    messages.error(request, 'Your email or password is incorrect, please try again')
                    return redirect('login')
            else:
                print('No account found with that email')
                messages.error(request, "You don't have an account, please register to continue")
                return redirect('login')
        else:
            print('Email field is empty')
            messages.error(request, 'Please enter your email')
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    print("You have been logged out")
    messages.success(request, "You have been logged out")
    return redirect('login')



# Admin User functions
def admin_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        

        if user.is_superuser is not None:
            auth.login(request, user)
            print(f'Welcome! {user} you are now logged in')
            messages.success(request, f'Welcome! {user} you are now logged in')
            return redirect('dashboard')

               
        else:
            print('Your email or password is incorrect, Please fill all fields correctly')
            messages.error(request, 'Your email or password is incorrect, fill all fields correctly')
            return redirect('admin_user')
        
    else:
        return render(request, 'authentication/admin_user.html')




def admin_logout(request):
    auth.logout(request)
    print("You have been logged out")
    messages.success(request, "You have been logged out")
    return redirect('admin_user')


