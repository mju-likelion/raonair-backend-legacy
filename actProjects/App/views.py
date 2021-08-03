from django.http import JsonResponse
from django.shortcuts import render
from . import models

import base64
import os

# Create your views here.


# 홈페이지 공연 추천
def home(request):
    return JsonResponse({"request": 'searchPage.html'})


# 검색결과 페이지
def search(request):
    return JsonResponse({"request": 'searchPage.html'})


# 검색결과 페이지, 더보기 클릭
def search_detail(request):
    return JsonResponse({"request": "detailpage.html"})


# 극단 개별 페이지
def troupe(request):
    return JsonResponse({"request": "listpage.html"})


# 연극 개별 페이지
def play(request, id):
    print(id)
    plays = models.Play.objects.get(id=id)
    # stars = models.Star.objects.get(play=id)  # 데이터들의 리스트
    # star_count = models.Star.objects.count(play=id)  # 정수 별점 갯수
    staffs = models.Staff.objects.filter(play=id)
    likes = models.Like.objects.filter(play=id).count()
    print(plays.title)

    '''
    t=0

    for i in range (star_count):
        if play == id :
            sum+=stars
            t+=1

    avg = sum/t;

    '''

    return JsonResponse({
        "data": {
            "play": {
                "name": plays.title,  # 연극이름
                "poster": plays.poster,  # 포스터 링크
                "like_count": likes,  # 찜수
                # "star_avg": avg,  # 평균 별점
                # "star_count": star_count,  # 별점수
                "time": plays.running_time,  # 공연시간
                "start_date": plays.start_date,  # 공연시작일
                "end_date": plays.end_date,  # 공연시작일
                # "external_links": [
                #     {
                #         "key": "enum(yes24, interpark, playDB, cultureGov)",
                #         "link": "string",
                #     },
                # ],
                # "actor": [
                #     {
                #         "name": staffs.person,  # 배우 이름
                #         # "photo": person.photo,  # 사진 링크
                #         "position": staffs.role,  # 배역
                #     },
                # ],
            }
        }
    })


# 로그인
def signin(request):
    return JsonResponse({"request": "listpage.html"})


# 회원가입
def signup(request):
    return JsonResponse({"request": "listpage.html"})


# 비밀번호 찾기
def password(request):
    return JsonResponse({"request": "listpage.html"})


# 연극 찜하기
def playlike(request):
    return JsonResponse({"request": "listpage.html"})


# 극단 찜하기
def troupelike(request):
    return JsonResponse({"request": "listpage.html"})


# 별점평가
def star(request):
    return JsonResponse({"request": "listpage.html"})


# 커멘트 달기
def comment(request):
    return JsonResponse({"request": "listpage.html"})


'''
#c언어
#include <stdio.h>
int main()
{
    int avg=0, sum=0, t=0;
    for(int i=0; i< ; i++)
    {
        if(play_id == 1)
        {
            sum+=play_id;
            t+=1;
        }
    }
    avg = sum/t;
    return avg;
}

#파이썬
t=0

for i in range :
    if play_id == 1 :
        sum+=play_id
        t+=1

avg = sum/t;


'''
