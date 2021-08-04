from django.http import JsonResponse
from django.shortcuts import render
from . import models

import base64
import os

def home(request) :
    return JsonResponse({"request":'home.html'})

# self의 정확한 용도?
def search(request) :
    keyword = request.POST.get('q', "") # 검색어 쿼리
    # plays = models.Play.objects.get(title=keyword)

    # plays = models.Play.objects.get(title__icontains=keyword)
    plays = models.Play.objects.all() # play 모든 결과 불러옴
    play_list = []
    for i in range(len(plays)):
        play_list.append({
            "title": plays[i].title,
            "start_date": plays[i].start_date,
            "end_date": plays[i].end_date,
            "poster": plays[i].poster,
        })

    return JsonResponse({
        "data": {
            # "query": str,
            "searched_results": {
                "ongoing_plays": play_list[0:len(play_list)],
                # "tobe_plays": play_tobe[4],
                # "closed_plays": play_closed[4],
            }
        }
    })

def search_detail(request) :
    return JsonResponse({"request":"detailpage.html"})

def troupe(request) :
    return JsonResponse({"request": "listpage.html"})

def play(request) :
    return JsonResponse({"request":"play.html"})

def signin(request) :
    return  JsonResponse({"request": "signin.html"})

def signup(request) :
    return  JsonResponse({"request": "signup.html"})

def password(request) :
    return  JsonResponse({"request": "find-password.html"})

def playlike(request) :
    return  JsonResponse({"request": "playlike.html"})

def troupelike(request) :
    return  JsonResponse({"request": "troupelike.html"})

def star(request) :
    return  JsonResponse({"request": "star.html"})

def comment(request) :
    return  JsonResponse({"request": "comment.html"})