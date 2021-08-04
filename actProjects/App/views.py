from django.http import JsonResponse
from django.shortcuts import render
from . import models
import base64
import os

# Create your views here.
def home(request) :
    return JsonResponse({"request":'home.html'})

# 검색 결과 페이지, 더보기 클릭 (GET /api/search/:type)
def detailpage(request) :
    plays = models.Play.objects.get()
    #links
    #start
    #limit
    start_date = models.Play.objects.get()

    # 검색 결과가 0개 일 때
    if(len(plays) == 0):
        return JsonResponse({
            "error": {
                #"query": string, #입력 받은 검색어
                #"type": enum()
            }
        })

    # 더보기를 눌러서 더 많은 공연을 조회했을 때
    return JsonResponse({
        "links": {
            # next 가 null이 아니라면
            #"next": string ,
        },
        "data": {
            #"query": string,
            #"type": enum("ongoing", "tobe", "closed"),
            #"search_results": play_simple[10],
        },
    })

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