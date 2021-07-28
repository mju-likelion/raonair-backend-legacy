from django.http import JsonResponse
from django.shortcuts import render

import base64
import os

# Create your views here.
def home(request) :
    return JsonResponse({"request":'home.html'})

def searchPage(request) :
    return JsonResponse({"request":'searchPage.html'})

def detailpage(request) :
    return JsonResponse({"request":"detailpage.html"})

def listpage(request) :
    return  JsonResponse({"request": "listpage.html"})

def search_play_with_options(request) :
    return JsonResponse({
        "data": {
            "page": "searchPlayWithOptions"
        }
    })

def theaterDetail(request) :
    return JsonResponse({'request': 'theater_detail.html'})

def is_poster(image_name) :
    return True if (('home' in image_name) or ('theme' in image_name) or ('month' in image_name)) else False