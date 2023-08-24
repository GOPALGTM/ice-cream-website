from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import logout,authenticate, login as auth_login
from myapp.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from .utils.email import send_verification_email,  send_password_reset_email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
# Create your views here.

def index(reequest):
    if reequest.user.is_anonymous:
       return redirect("login")
    return render(reequest,'index.html')

def about(reequest):
    return render(reequest,'about.html')

def services(reequest):
    return render(reequest,'services.html')
    
def contact(reequest):
    if reequest.method == "POST":
      name=reequest.POST.get('name')
      email=reequest.POST.get('email')
      phone=reequest.POST.get('phone')
      desc=reequest.POST.get('desc')
      contact=Contact(name=name, email=email,phone=phone,desc=desc, date=datetime.today())
      contact.save()
      messages.success(reequest, 'your  message has been sent...')
    return render(reequest,'contact.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("index")  # Assuming you have defined the 'index' URL pattern in your Django project's urls.py
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")  # Optional: You can add a logout message
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        # Check if passwords match
        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect("signup")

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different username.")
            return redirect("signup")

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            if user:
                # Send verification email
                send_verification_email(email)
                return redirect("login")
            else:
                messages.error(request, "User account not created")
        except:
            messages.error(request, "An error occurred while creating the user account.")
    return render(request, 'signup.html')

def send_reset_password_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'message': 'User with this email does not exist.'})
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
        reset_url = f'http://{current_site.domain}{reset_url}'
        send_password_reset_email(email, reset_url)

        return render(request, 'forgot_password.html', {'message': 'An email has been sent to reset your password.'})

    return render(request, 'forgot_password.html')



def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
        # You might want to add some validation checks for the new password here.

        # Update the user's password securely using set_password
            user.set_password(new_password)
            user.save()

        # Redirect the user to the login page or any other page after resetting the password
            return redirect('login')
        else:
            # If it's not a POST request, render the reset_password.html page
            return render(request, 'reset_password.html', {'user': user})
    else:
        # Handle the case where the token is invalid or the user does not exist
        return redirect('login')