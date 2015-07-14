from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    template = 'index.html'
    return render(request, template)

def search(request):
    if request.method == 'POST':
        going = request.POST.get("Dday")
        coming = request.POST.get("Aday")
        destination = request.POST.get("selected")
        message = going + coming + destination
        return HttpResponse(message)
    else:
        return redirect('/')
