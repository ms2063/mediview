from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('main/main/')
    else :
        return redirect('main/main/')
