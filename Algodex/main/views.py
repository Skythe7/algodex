from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import forms
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.http import JsonResponse

# Algorithms library

def home(request):
    if request.GET.get("category"):
        category = request.GET.get("category")
        algorithms = models.Algorithm.objects.filter(category=category)
    else:
        algorithms = models.Algorithm.objects.all()

    return render(request, 'home.html', {
        'algorithms': algorithms,
    })


def algorithm_page(request, id):
    algorithm = models.Algorithm.objects.get(id=id)

    return render(request, 'page.html', {
        'algorithm': algorithm,
    })


def practice_page(request, id):
    return render(request, 'practice.html', {
        "algorithm": models.Algorithm.objects.get(id=id),
    })


# Authentication systems

def logout_page(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect!")
            return redirect('/login')
    
    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        if password != confirm_password:
            messages.error(request, "Password and confirm password must be the same!")
            return redirect('/register')
        elif User.objects.filter(username=username):
            messages.error(request, "Username exist! Please create different one")
            return redirect('/register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
    
    return render(request, 'register.html')


# Algorithm pages

@login_required(login_url='/login')
def create_page(request):
    if request.method == "POST":
        form = forms.PostAlgorithm(request.POST)

        if form.is_valid():
            algorithm = form.save(commit=False)
            algorithm.creator = request.user
            algorithm.save()
        else:
            messages.error(request, "Please input all the field!")

        return redirect("/")
    else:
        form = forms.PostAlgorithm()
    return render(request, 'create.html', {
        "form": form,
    })


@login_required(login_url='/login')
def voting(request, status, id):
    algorithm = models.Algorithm.objects.get(id=id)

    if algorithm.creator == request.user:
        messages.error(request, "You are the creator of this post, you cannot vote!")
        return redirect(f'/page/{id}')
    elif algorithm.voters.filter(id=request.user.id).exists():
        messages.error(request, "You already vote on this algorithm!")
        return redirect(f'/page/{id}')

    match status:
        case "yes":
            algorithm.yes_count += 1
            algorithm.voters.add(request.user)
            algorithm.save()
        case "no":
            algorithm.no_count += 1
            algorithm.voters.add(request.user)
            algorithm.save()
        case _:
            messages.error(request, "Something went wrong! Please try again later")
        
    return redirect(f'/page/{id}')


@login_required(login_url='/login')
def save_solve(request):
    if request.method == "POST":
        data = json.loads(request.body)

        models.Solve.objects.create(user=request.user, time=data["time"])

        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST required"}, status=405)


def profile_page(request, id):
    user = User.objects.get(id=id)
    solves = models.Solve.objects.filter(user=user)

    return render(request, 'profile.html', {
        "user": user,
        "solves": solves,
    })