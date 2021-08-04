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
    stars = models.Star.objects.filter(play=id)  # 데이터들의 리스트
    # star_count = models.Star.objects.count(play=id)  # 정수 별점 갯수
    staffs = models.Staff.objects.filter(play=id)
    likes = models.Like.objects.filter(play=id).count()

    # 별점 갯수
    stars_count = 0
    for i in range(len(stars)):
        stars_count += stars[i].star

    # 별점 평균 리스트
    # sum = 0
    # for i in range(stars_count):
    #     if plays.id == id:
    #         sum += stars_count148+]

    # avg = sum/len(stars)

    # 관련정보더보기 링크 리스트
    links = []
    # for i in range(4):
    # if plays.yes24_external_link is not None: // null은 출력안하려면 ?
    links.append({"name": 'yes24', "link": plays.yes24_external_link})
    links.append({"name": 'interpark', "link": plays.interpark_external_link})
    links.append({"name": 'playDB', "link": plays.playdb_external_link})
    links.append({"name": 'cultureGov', "link": plays.culturegov_external_link})

    # 배우 및 극단 프로필 리스트
    staffss = []
    for i in range(len(staffs)):
        staffss.append({"name": staffs[i].person.name, "position": staffs[i].role, "photo": staffs[i].person.photo})

    return JsonResponse({
        "data": {
            "play": {
                "name": plays.title,  # 연극이름
                "poster": plays.poster,  # 포스터 링크
                # "like_count": likes,  # 찜수
                # "star_avg": avg,  # 평균 별점
                "star_cnt": stars_count,  # 별점수
                "time": plays.running_time,  # 공연시간
                "start_date": plays.start_date,  # 공연시작일
                "end_date": plays.end_date,  # 공연시작일
                "external_links": links,  # 관련정보더보기 링크
                "actor": staffss  # 배우 및 극단 프로필
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
