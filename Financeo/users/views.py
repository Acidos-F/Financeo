from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "dashboard.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken"})

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already registered"})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("/dashboard/")

    return render(request, "signup.html")

from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "signup.html")