from django.shortcuts import render

def home(request):
   return render(request, 'index.html')

def pricing(request):
   return render(request, 'pricing.html')