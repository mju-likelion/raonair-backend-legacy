from django.http import JsonResponse
from django.shortcuts import render
from . import models


import base64
import os

# Create your views here.
def search_troupe_detail(request):
    query = request.GET.get('query', '')
    type = request.GET.get('type', '')

    filter_query = models.Troupe.objects.filter(name__icontains=query)
    troupes = filter_query.filter(type__icontains=type)

    search_list = []

    if len(troupes) == 0:
        return JsonResponse({
            'error': {
                'query': query,
                'type': type,
                'error_message': '검색결과가 없습니다'
            }
        })

    if request.GET.get('start', ''):
        start = int(request.GET.get('start', ''))
        next = request.get_full_path().split('&start=')[0] + '&start=' + str(start+10)
    else:
        start = 0
        next = request.get_full_path() + "&start=11"

    for i in troupes:
        new_troupe = ({
            'id': i.id,
            'name': i.name,
            'type': i.type,
            'logo': i.logo,
        })
        search_list.append(new_troupe)

    return JsonResponse({
        'links': {
            'next': next,
        },
        'data': {
            'query': query,
            'type': type,
            'search_results': search_list[start:start+10]
        }
    })

def home(request) :
    return JsonResponse({"request":'home.html'})

def search_play(request):
    return JsonResponse({"request":'search_play.html'})

def search_troupe(request):
    return JsonResponse({"request":'search_troupe.html'})

def search_detail(request):
    return JsonResponse({"request":'search_detail.html'})

def troupe(request):
    return JsonResponse({"request":'troupe.html'})

def play(request):
    return JsonResponse({"request":'play.html'})

def signin(request):
    return JsonResponse({"request":'signin.html'})

def signup(request):
    return JsonResponse({"request":'signup.html'})

def password(request):
    return JsonResponse({"request":'password.html'})

def playlike(request):
    return JsonResponse({'request': 'playlike.html'})


def troupelike(request):
    return JsonResponse({'request': 'troupelike.html'})


def star(request):
    return JsonResponse({'request': 'star.html'})

def comment(request):
    return JsonResponse({'request': 'comment.html'})

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