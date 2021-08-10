from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from . import models
from datetime import datetime
from django.views.decorators.http import require_http_methods

import base64
import os


def home(request):
    return JsonResponse({'request': 'home.html'})


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


def troupe(request, id):
    troupe = models.Troupe.objects.get(id=id)
    troupe_like = models.TroupeLike.objects.filter(troupe=id).count()
    team = models.Team.objects.filter(troupe=id)
    team_list = []  # 극단 구성원
    plays = models.Play.objects.filter(troupe=id)  # 극단에서 공연한 연극
    ongoing_play = []
    tobe_play = []
    closed_play = []

    # 구성원 구하기
    for i in team:
        team_list.append({
            'name': i.person.name,
            'photo': i.person.photo,
            # "role": i.person.role,
        })

    # 연극 구하기
    tody = datetime.strftime(datetime.now(), '%Y-%m-%d')
    for i in plays:
        start_date = datetime.strftime(i.start_date, '%Y-%m-%d')
        end_date = datetime.strftime(
            i.end_date, '%Y-%m-%d') if (i.end_date) else None

        new_play = [{
            'id': i.id,
            'title': i.title,
            'poster': i.poster,
            'start_date': start_date,
            'end_date': end_date,
        }]

        if tody >= start_date and (end_date == None or tody <= end_date):
            ongoing_play.append(new_play)
        elif tody < start_date:
            tobe_play.append(new_play)
        elif tody > end_date:
            closed_play.append(new_play)
        else:
            print('날짜에러')

    # 페이징 테스트
    # for i in range(20):
    #     closed_play.append({
    #         'id': i,
    #         'title': str(i) + "번째 테스트 공연",
    #         'poster': str(i) + "번째 테스트 포스터",
    #         'start_date': "2021-01-01",
    #         'end_date': "2021-01-01",
    #     })

    # 페이징
    if request.GET.get('start', ''):
        start = int(request.GET.get('start', ''))
        next = request.get_full_path().split(
            '&start=')[0] + '&start=' + str(start+10)
    else:
        start = 0
        next = request.get_full_path() + '&start=11'

    return JsonResponse({
        'data': {
            # 유저의 찜하기 액션
            # "context": {
            #     "like_check": boolean
            # },
            'links': {
                'next': next,
            },
            'troupe': {
                'id': troupe.id,
                'name': troupe.name,
                'type': troupe.type,
                'logo': troupe.logo,
            },
            'troupe_like': troupe_like,
            'team': team_list,
            'play': {
                'ongoing_play': ongoing_play,
                'tobe_play': tobe_play,
                'closed_play': closed_play[start:start+10],
                # 'closed_play': closed_play,
            },
        },
    })


def play(request):
    return JsonResponse({'request': 'play.html'})


def signin(request):
    return JsonResponse({'request': 'signin.html'})


def signup(request):
    return JsonResponse({'request': 'signup.html'})


def password(request):
    return JsonResponse({'request': 'find-password.html'})


def playlike(request):
    return JsonResponse({'request': 'playlike.html'})


# @login_required #  로그인 되어야만 클릭 가능
@csrf_exempt  # csrf verification 에러 조치
@require_http_methods(['POST'])  # 포스트 방식 확인
def troupelike(request, id):
    input = json.loads(request.body)  # body 데이터 받아옴
    troupe = models.Troupe.objects.get(id=id)
    user = models.User.objects.get(id=input['user'])  # 로그인 구현 후 바꿔줘야함

    # 찜 여부 판단, 로그인 구현 후 수정 필요
    check_troupe = models.TroupeLike.objects.filter(
        troupe=id, user=input['user'])

    if check_troupe.exists():
        troupe_like = check_troupe.delete()  # check_troupe에 해당하는 튜플 삭제
        return JsonResponse({
            'data': {
                'troupe': troupe.name,
                'email': user.email,
                'nickname': user.nickname,
                'context': {
                    'like_checked': check_troupe.exists()
                }
            },
            'message': 'deleted like'
        }, status=200)
    else:
        troupe_like = models.TroupeLike.objects.create(
            troupe=troupe,
            user=user
        )
        return JsonResponse({
            'data': {
                'id': troupe_like.id,
                'troupe': troupe_like.troupe.name,
                'email': troupe_like.user.email,
                'nickname': troupe_like.user.nickname,
                'context': {
                    'like_checked': check_troupe.exists()
                }
            },
            'message': 'success'
        }, status=200)


def star(request):
    return JsonResponse({'request': 'star.html'})


def comment(request):
    return JsonResponse({'request': 'comment.html'})
