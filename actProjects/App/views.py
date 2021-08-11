from django.db.models.fields import EmailField
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from . import models
import json
import re
from django.views.decorators.http import require_http_methods

# from email_validator import validate_email, EmailNotValidError

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
    play = models.Play.objects.get(id=id)
    star = models.Star.objects.filter(play=id)  # 데이터들의 리스트
    staff = models.Staff.objects.filter(play=id)
    like = models.Like.objects.filter(play=id).count()
    comment = models.Comment.objects.filter(play=id)

    # 별점 갯수
    star_count = 0
    for i in range(len(star)):
        star_count += star[i].star

    # 별점 평균 리스트
    avg = star_count/len(star)/2

    # 찜 갯수
    # like_cnt = 0
    # for i in range(len(like)):
    #     like_cnt += like[i].like #찜 갯수 컬럼 없음

    # 공연장소
    theater = []
    theater.append({"name": play.theater.name, "location": play.theater.location, "address": play.theater.address})

    # 리뷰
    review = []
    for i in range(len(comment)):
        review.append({"nickname": comment[i].user.nickname, "comment": comment[i].comment})
    # "date": comment.date}) # date 컬럼 없음

    # 관련정보더보기 링크 리스트
    link = []
    if play.yes24_external_link is not None:
        link.append({"name": 'yes24', "link": play.yes24_external_link})
    if play.interpark_external_link is not None:
        link.append({"name": 'interpark', "link": play.interpark_external_link})
    if play.playdb_external_link is not None:
        link.append({"name": 'playDB', "link": play.playdb_external_link})
    if play.culturegov_external_link is not None:
        link.append({"name": 'cultureGov', "link": play.culturegov_external_link})

    # 배우 및 극단 프로필 리스트
    staffs = []
    for i in range(len(staff)):
        staffs.append({"name": staff[i].person.name, "position": staff[i].role, "photo": staff[i].person.photo})

    return JsonResponse({
        "data": {
            "play": {
                "name": play.title,  # 연극이름
                "poster": play.poster,  # 포스터 링크
                # "like_cnt": like_cnt,  # 찜수
                "star_avg": avg,  # 평균 별점
                "star_cnt": star_count,  # 별점수
                # "time": play.running_time,  # 공연시간
                "start_date": play.start_date,  # 공연시작일
                "end_date": play.end_date,  # 공연시작일
                "external_links": link,  # 관련정보더보기 링크
                "staff": staffs,  # 배우 및 극단 프로필
                "review": review,  # 리뷰 및 커멘트
                "theater": theater  # 공연장소
                # "context": {
                # "like_check": boolean,
                # "rating": number | | null,
                # }
            }
        }
    })


# 로그인
def signin(request):
    return JsonResponse({"request": "listpage.html"})


# 회원가입
@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    input = json.loads(request.body)

    # 403_BAD_REQUEST

    # 아이디(이메일) 형식 오류

    if re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'", input['email']) == False:
        return JsonResponse({
            "error": "올바른 이메일 형식이 아닙니다."
        }, status=400)

    # 비밀번호 형식 오류

    if len(input['password']) < 6:
        return JsonResponse({
            "error": "올바른 비밀번호 형식이 아닙니다. 비밀번호는 6글자 이상입니다."
        }, status=400)

    # 사용자 닉네임 형식 오류

    if len(input['nickname']) > 10:
        return JsonResponse({
            "error": "올바른 닉네임 형식이 아닙니다. 닉네임은 10글자 이하 입니다."
        }, status=400)

    # 사용자 이름 형식 오류

    if re.match(r"^ [가-힣]{2, 4}$", input['name']):
        return JsonResponse({
            "error": "올바른 이름 형식이 아닙니다."
        }, status=400)

    # 409_CONFLICT

    if models.User.objects.filter(email=input['email']):
        return JsonResponse({
            "data": "이미 존재하는 아이디입니다."
        }, status=409)

     # 200_OK
    userdata = models.User.objects.create(email=input['email'], nickname=input['nickname'], name=input['name'])
    return JsonResponse({
        "data": {
            "id": userdata.id,  # 사용자의 id
            "email": userdata.email,  # 사용자의 email
            "nickname": userdata.nickname,  # 사용자의 nickname
            "name": userdata.name,  # 사용자의 이름
        },
        "message": "회원가입이 완료되었습니다."
    }, status=200)


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
