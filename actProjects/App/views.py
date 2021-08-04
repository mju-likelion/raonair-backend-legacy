from django.http import JsonResponse
from django.shortcuts import render
from . import models
from datetime import datetime

import base64
import os

def home(request) :
    return JsonResponse({"request":'home.html'})

def search(request) :
    # 검색어 쿼리, 두 번째 요소에는 기본값을 넣어야한다 (임시로 POST를 넣음)
    keyword = request.POST.get('q', "")
    plays = models.Play.objects.filter(title__icontains=keyword) # play 모든 결과 불러옴

    ongoing_list = []
    tobe_list = []
    closed_list = []

    tody = datetime.strftime(datetime.now(), '%Y-%m-%d')

    for i in plays:
        # 날짜 비교
        start_date = datetime.strftime(i.start_date, '%Y-%m-%d')
        end_date = datetime.strftime(i.end_date, '%Y-%m-%d') if (i.end_date) else None

        new_play = ({
            "title": i.title,
            "poster": i.poster,
            "start_date": start_date,
            "end_date": end_date,

            "keyword": keyword, # 쿼리 확인용
        })

        if(tody >= start_date and (end_date == None or tody <= end_date)):
            ongoing_list.append(new_play)
        elif(tody < start_date):
            tobe_list.append(new_play)
        elif(tody > end_date):
            closed_list.append(new_play)
        else:
            print("에러")

    return JsonResponse({
        "data": {
            # "query": str,
            "searched_results": {
                "ongoing_plays": ongoing_list[0:4],
                "tobe_plays": tobe_list[0:4],
                "closed_plays": closed_list[0:4],
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