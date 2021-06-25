from django.shortcuts import render

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def searchPage(request) :
    return render(request, 'searchPage.html')


def search_play_with_options(request) :
    return render(request, 'search-play-with-options.html')