from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import FileResponse
import os
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt



def generatePdf(request):
     return render(request,'template.html')

@csrf_exempt 
def makepdf(request):
    from PlotGeneratorV9 import makepdf
   
    if request.method == 'POST': 
        from .forms import MakepdfForm
        form = MakepdfForm(request.POST)
        if form.is_valid():
            csvfile = form.data['csvfile']
            title = form.data['title']
            makepdf(title,csvfile)
        
    return HttpResponse({'message':title+" Finish!"}, status=200)
