import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import models
from datetime import datetime
import re

import base64
import os


def home(request):
    return JsonResponse({'request': 'home.html'})

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
        next = request.get_full_path().split(
            '&start=')[0] + '&start=' + str(start+10)
    else:
        start = 0
        next = request.get_full_path() + '&start=11'

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


def search_play(request):
    keyword = request.GET.get('query', '')
    loc = request.GET.get('location', '')

    filter_keyword = models.Play.objects.filter(
        title__icontains=keyword)  # 검색어에 포함되는 play를 받아옴
    plays = filter_keyword.filter(theater__location__icontains=loc)

    # 검색결과가 0개일 때 return
    if len(plays) == 0:
        return JsonResponse({
            'error': {
                'query': keyword,
                'error_meessage': '검색 결과가 없습니다',
            }
        })

    # 공연 진행 상태
    ongoing_list = []
    tobe_list = []
    closed_list = []

    tody = datetime.strftime(datetime.now(), '%Y-%m-%d')

    for i in plays:
        start_date = datetime.strftime(i.start_date, '%Y-%m-%d')
        end_date = datetime.strftime(
            i.end_date, '%Y-%m-%d') if (i.end_date) else None
        stars = models.Star.objects.filter(play=i.id)
        likes = models.Like.objects.filter(play=i.id).count()  # 찜 데이터 아직 없음

        # 평균 별점 구하기
        star_sum = 0
        for j in stars:
            star_sum += j.star
        star_avg = star_sum / len(stars) / 2

        new_play = ({
            'id': i.id,
            'title': i.title,
            'poster': i.poster,
            'start_date': start_date,
            'end_date': end_date,
            'star_avg': star_avg,
            'likes': likes,
            'location': i.theater.location,
        })

        # 날짜 비교
        if tody >= start_date and (end_date == None or tody <= end_date):
            ongoing_list.append(new_play)
        elif tody < start_date:
            tobe_list.append(new_play)
        elif tody > end_date:
            closed_list.append(new_play)
        else:
            print('날짜설정에러')

    return JsonResponse({
        'data': {
            'query': keyword,
            'searched_results': {
                'ongoing_plays': ongoing_list[0:4],
                'tobe_plays': tobe_list[0:4],
                'closed_plays': closed_list[0:4],
            }
        }
    })


def play_options(request):
    play_location = [
        {'key': 'seoul', 'value': '서울'}, {'key': 'gyeonggi', 'value': '경기'},
        {'key': 'gangwon', 'value': '강원'}, {'key': 'gyeongbuk', 'value': '경북'},
        {'key': 'gyeongnam', 'value': '경남'}, {'key': 'gwangju', 'value': '광주'},
        {'key': 'daegu', 'value': '대구'}, {'key': 'daejeon', 'value': '대전'},
        {'key': 'busan', 'value': '부산'}, {'key': 'sejong', 'value': '세종'},
        {'key': 'ulsan', 'value': '울산'}, {'key': 'incheon', 'value': '인천'},
        {'key': 'jeonnam', 'value': '전남'}, {'key': 'jeonbuk', 'value': '전북'},
        {'key': 'jeju', 'value': '제주'}, {'key': 'chungnam.', 'value': '충남'},
        {'key': 'chungbuk', 'value': '충북'},
    ]

    return JsonResponse({
        'data': {
            'play_options': play_location
        }
    })


def search_troupe(request):
    query = request.GET.get('query', '')
    type = request.GET.get('type', '')

    filter_query = models.Troupe.objects.filter(name__icontains=query)
    troupes = filter_query.filter(type__icontains=type)

    if len(troupes) == 0:
        return JsonResponse({
            'error': {
                'query': query,
                'type': type,
                'error_message': '검색 결과가 없습니다'
            }
        })
    troupe_all = []  # 타입 선택 안했을 때
    troupe_normal = []  # 일반 극단
    troupe_student = []  # 학생 극단
    for i in troupes:
        new_troupe = ({
            'id': i.id,
            'name': i.name,
            'type': i.type,
            'logo': i.logo,
        })

        # type을 선택 안하면 타입 구분 없이 출력
        if type == '':
            troupe_all.append(new_troupe)
        else:
            if i.type == 'normal':
                troupe_normal.append(new_troupe)
            elif i.type == 'student':
                troupe_student.append(new_troupe)

    return JsonResponse({
        'data': {
            'query': query,
            'type': type,
            'searched_results': {
                'troupe_all': troupe_all[0:12],
                'troupe_normal': troupe_normal[0:6],
                'troupe_student': troupe_student[0:6],
            }
        }
    })

# 검색 결과 페이지, 더보기 클릭 (GET /api/search/<str:type>)


def search_detail(request, type):
    keyword = request.GET.get('query', '')
    loc = request.GET.get('location', '')

    filter_keyword = models.Play.objects.filter(
        title__icontains=keyword)  # 검색어에 포함되는 play를 받아옴
    plays = filter_keyword.filter(theater__location__icontains=loc)

    search_list = []  # 검색 결과들

    # 검색 결과가 0 일 때
    if len(plays) == 0:
        return JsonResponse({
            'error': {
                'query': keyword,
                'type': type,
                'error_message': '검색 결과가 없습니다',
            }
        })

    # start 데이터가 있는 경우와 없는 경우

    if request.GET.get('start', ''):
        start = int(request.GET.get('start', ''))
        next = request.get_full_path().split('&start=')[0] \
            + '&start=' \
            + str(start + 10)
    else:
        start = 0
        next = request.get_full_path() + '&start=11'

    for i in plays:
        stars = models.Star.objects.filter(play=i.id)
        likes = models.Like.objects.filter(play=i.id).count()

        # 평균 별점 구하기
        star_sum = 0
        for each_star in stars:
            star_sum += each_star.star
        star_avg = star_sum / len(stars) / 2

        new_play = ({
            'title': i.title,
            'poster': i.poster,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'star_avg': star_avg,
            'likes': likes,
            'location': i.theater.location,
        })
        search_list.append(new_play)

    # 검색결과가 0이 아닐 때
    return JsonResponse({
        'links': {
            'next': next
        },
        'data': {
            'query': keyword,
            'type': type,
            'search_results': search_list[start:start+10],
        },
    })


def troupe_options(request):
    troupe_type = {'noraml': '일반', 'student': '학생'}

    return JsonResponse({
        'data': {
            'troupe_option': troupe_type
        }
    })


def troupe(request):
    return JsonResponse({'request': 'listpage.html'})


def play(request):
    return JsonResponse({'request': 'play.html'})


@csrf_exempt
@require_http_methods(["POST"])
def signin(request):

    requsestbody = json.loads(request.body)

    # 400_BAD_REQUEST
    # if re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'", input['email']) == False:
    #     return JsonResponse({
    #         "error": {
    #             "message": "아이디가 이메일 형식이 아닙니다."
    #         }
    #     }, status=400)

    # 200_OK // 입력받은 아이디(사용자)가 DB에 있는 경우

    if models.User.objects.filter(email=requsestbody['email']):

        # 아이디는 맞는데 비밀번호가 틀린 경우 :
        if models.User.objects.filter(password=requsestbody['password']):
            return JsonResponse({
                "error": "비밀번호가 틀렸습니다."
            }, status=400)

        # 200_OK // 로그인 완료
        # 사용자 닉네임 ****************
        else:
            signinuser = models.User.objects.filter(email=requsestbody['email'])
            return JsonResponse({
                "message": {
                    signinuser.nickname,
                    "님 안녕하세요!"
                }
            }, status=200)

     # 401_Unauthorized // # 입력받은 아이디(사용자)가 DB에 없는 경우 -> 회원가입 ??
    else:
        return JsonResponse({
            "error": "존재하지않는 아이디입니다."
        }, status=401)


def signup(request):
    return JsonResponse({'request': 'signup.html'})


def password(request):
    return JsonResponse({'request': 'find-password.html'})


def playlike(request):
    return JsonResponse({'request': 'playlike.html'})


def troupelike(request):
    return JsonResponse({'request': 'troupelike.html'})


@csrf_exempt
@require_http_methods(['POST'])
def star(request, id):
    # 존재하지 않는 ID인 경우
    if not models.User.objects.filter(id=id):
        return JsonResponse({
            'message': '로그인된 사용자가 아닙니다',
        }, status=401)

    user = models.User.objects.get(id=id)
    user_body = json.loads(request.body)
    selected_play = models.Play.objects.get(id=user_body['play'])

    # 별점평가 여부 판단
    check_star = models.Star.objects.filter(user=user, play=selected_play)
    if check_star.exists():
        checked_star = models.Star.objects.get(user=user, play=selected_play)
        return JsonResponse({
            'data': {
                'context': {
                    'star_checked': checked_star.star
                }
            },
            'message': 'star already checked'
        }, status=200)
    else:
        if user_body['star'] < 1:
            return JsonResponse({
                'message': '최소 별점보다 별점이 낮습니다',
            }, status=400)
        else:
            new_star = models.Star.objects.create(
                user=user,
                star=user_body['star'],
                play=selected_play
            )
            return JsonResponse({
                'data': {
                    'user': new_star.user.id,
                    'star': new_star.star,
                    'play': new_star.play.id
                }
            }, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def comment(request, id):
    # 존재하지 않는 ID인 경우
    if not models.User.objects.filter(id=id):
        return JsonResponse({
            'message': '로그인된 사용자가 아닙니다',
        }, status=401)

    body = json.loads(request.body)
    comment_user = models.User.objects.get(id=id)
    comment_play = models.Play.objects.get(id=body['play'])

    # 커멘트 작성 여부 판단
    check_comment = models.Comment.objects.filter(
        user=comment_user, play=comment_play)
    if check_comment.exists():
        checked_comment = models.Comment.objects.get(
            user=comment_user, play=comment_play)
        return JsonResponse({
            'data': {
                'context': {
                    'commented': checked_comment.comment
                }
            },
            'message': 'already commented'
        }, status=200)
    else:
        if len(body['comment']) > 200:
            return JsonResponse({
                'message': '글자 수는 200자를 넘을 수 없습니다',
            }, status=400)
        else:
            new_comment = models.Comment.objects.create(
                user=comment_user,
                comment=body['comment'],
                play=comment_play
            )
            return JsonResponse({
                'data': {
                    'user': new_comment.user.id,
                    'comment': new_comment.comment,
                    'play': new_comment.play.id
                }
            }, status=200)
