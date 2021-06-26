from django.shortcuts import render
import base64
import os

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def searchPage(request) :
    return render(request, 'searchPage.html')


def search_play_with_options(request) :
    # with open(os.path.join(os.getcwd(), 'App/static/img/*'), 'rb') as img_file:
    #     img_data = base64.b64encode(img_file.read()).decode('utf-8')
    # print(img_data)
    # print(os.path.join(os.getcwd(), 'App/static/img'))
    images_name = os.listdir(os.path.join(os.getcwd(), 'App/static/img'))
    print(images_name)
    # print(os.listdir(os.path.join(os.getcwd(), 'App/static/img')))
    return render(request, 'search-play-with-options.html', {'images_name': images_name})