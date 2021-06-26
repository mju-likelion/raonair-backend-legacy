from django.shortcuts import render
import base64
import os

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def searchPage(request) :
    return render(request, 'searchPage.html')


def search_play_with_options(request) :
    #이미 파일들의 이름을 읽어 온다.
    images_name = os.listdir(os.path.join(os.getcwd(), 'App/static/img'))
    return render(request, 'search-play-with-options.html', {'images_name': images_name})