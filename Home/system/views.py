from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import RegisterForm 
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # or 'password2', both should be the same
            user = authenticate(username=username, password=password)
            login(request, user)

            # Redirect to the login page
            return redirect('login')  # Replace 'login' with the actual URL name for your login page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page or home page
            return redirect('home')  # Replace 'home' with your actual URL name for home page
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
