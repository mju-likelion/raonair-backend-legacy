from django.shortcuts import render

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def searchPage(request) :
    return render(request, 'searchPage.html')

def detailpage(request) :
    return render(request, 'detailpage.html')

       
    