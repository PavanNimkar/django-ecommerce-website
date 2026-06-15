from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.shortcuts import redirect


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.error(request, "Account not found")
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.error(request, "Account is not verified")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        print(user_obj)
        if user_obj:
            login(request, user_obj)
            return redirect("/")

        messages.error(request, "Invalid credentails!")
        return HttpResponseRedirect(request.path_info)
    return render(request, "accounts/login.html")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.warning(request, "Email already taken!")
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            password=password,
        )

        messages.success(request, "Email has been sent on your mail")
        return HttpResponseRedirect(request.path_info)
    return render(request, "accounts/register.html")


def activate_account(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect("/")
    except Exception as e:
        print(e)
        return HttpResponse("Invalid email token")
