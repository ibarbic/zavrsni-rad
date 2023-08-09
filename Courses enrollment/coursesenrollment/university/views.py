from django.shortcuts import render

def home(request):
    return render(request, 'home', {'title': 'Home'})
# Create your views here.
