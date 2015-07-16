from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime

def home(request):
    template = 'index.html'
    return render(request, template)

def search(request):
    if request.method == 'POST':
        today = datetime.date.today().isoformat()
        going = request.POST.get("Dday")
        coming = request.POST.get("Aday")
        destination = request.POST.get("selected")
        if coming < going:
            messages.error(request,"Can't come back if you're not there first! Check the dates!")
            return HttpResponseRedirect('/')
        elif today > going:
            messages.error(request,"This isn't a time machine! Check the dates!")
            return HttpResponseRedirect('/')
        message = going + coming + destination
        return render(request, "search.html")
    else:
        return redirect('/')
