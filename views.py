from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
from .extractor import currency, temp_get_data, get_data ### DELETE TEMP ###

def home(request):
    template = 'index.html'
    return render(request, template)

def search(request):
    if request.method == 'POST':
        today = datetime.date.today().isoformat()
        going = request.POST.get("Dday")
        coming = request.POST.get("Aday")
        destination = request.POST.get("selected")
        money = currency(destination)
        if coming < going:
            messages.error(request,"Can't come back if you're not there first! Check the dates!")
            return HttpResponseRedirect('/')
        elif today > going:
            messages.error(request,"This isn't a time machine! Check the dates!")
            return HttpResponseRedirect('/')
        #message = temp_get_data() ### DELETE TEMP ###
        message = get_data(going, coming, destination)
        if message == "Ran out of quota!":
            messages.error(request,"Sorry, daily search quota of 50 has been reached, try again tomorrow!")
            return HttpResponseRedirect('/')
        else:
            return render(request, 'search.html', { 'data': message, 'destination': destination, 'currency': money })
    else:
        return redirect('/')

def custom404(request):
    return render(request, '404.html')
