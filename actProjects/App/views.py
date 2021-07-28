from django.http import JsonResponse
import base64
import os

# Create your views here.
def home(request) :
    return JsonResponse({"request":'home.html'})

def searchPage(request) :
    return render(request, 'searchPage.html')

def detailpage(request) :
    return render(request, 'detailpage.html')

def listpage(request) :
    return render(request, 'listpage.html')

def search_play_with_options(request) :
    #이미지 파일들의 이름을 읽어 온다.
    images_name = os.listdir(os.path.join(os.getcwd(), 'App/static/img'))
    posters_name = []
    for img in images_name:
        if is_poster(img):
            posters_name.append(img)
    return render(request, 'search-play-with-options.html', {'images_name': posters_name})

def theaterDetail(request) :
    return render(request, 'theater_detail.html')

def is_poster(image_name) :
    return True if (('home' in image_name) or ('theme' in image_name) or ('month' in image_name)) else False