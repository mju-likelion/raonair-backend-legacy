from django.shortcuts import render

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def searchPage(request) :
    return render(request, 'searchPage.html')

def theaterDetail(request) :
    return render(request, 'theater_detail.html')