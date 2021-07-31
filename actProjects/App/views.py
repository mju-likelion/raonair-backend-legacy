from django.http import JsonResponse
from django.shortcuts import render

import base64
import os

# Create your views here.


# 홈페이지 공연 추천
def home(request):
    return JsonResponse({
        "data": {
            "play": {
                "name": string,  # 연극이름
                "poster": string,  # 포스터 링크
                "like_count": number,  # 찜수
                "star_avg": number,  # 평균 별점
                "star_count": number,  # 별점수
                "price": number,  # 가격
                "time": number,  # 공연시간
                "start_date": date,  # 공연시작일
                "end_date": date,  # 공연시작일
                "external_links": [
                    {
                        "key": enum(yes24, interpark, playDB, cultureGov),
                        "link": string,
                    },
                ],
                "actor": [
                    {
                        "name": string,  # 배우 이름
                        "photo": string,  # 사진 링크
                        "position": string,  # 배역
                    },
                ],
            }
        }
    }
    )


# 검색결과 페이지
def serch(request):
    return JsonResponse({"request": 'searchPage.html'})


# 검색결과 페이지, 더보기 클릭
def serch_detail(request):
    return JsonResponse({"request": "detailpage.html"})


# 극단 개별 페이지
def troupe(request):
    return JsonResponse({"request": "listpage.html"})


# 연극 개별 페이지
def play(request):
    return JsonResponse({'request': 'theater_detail.html'})


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
