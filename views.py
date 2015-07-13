#!/usr/bin/env python2.7
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import extractor

def home(request):
    template = 'index.html'
    return render(request, template)

def search(request):
    if request.method == 'POST':
        going = request.POST.get("Dday")
        coming = request.POST.get("Aday")
        destination = request.POST.get("selected")
        message = going + coming + destination
        return HttpResponse(extractor.foo())
    else:
        return redirect('/')