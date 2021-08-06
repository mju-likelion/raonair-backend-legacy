from django.http import JsonResponse
from django.shortcuts import render
from . import models
from datetime import datetime

import base64
import os


def home(request):
    return JsonResponse({'request': 'home.html'})


def search_play(request):
    return JsonResponse({'request': 'home.html'})


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


def search_detail(request):
    return JsonResponse({'request': 'detailpage.html'})


def troupe(request):
    return JsonResponse({'request': 'listpage.html'})


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


def troupelike(request):
    return JsonResponse({'request': 'troupelike.html'})


def star(request):
    return JsonResponse({'request': 'star.html'})


def comment(request):
    return JsonResponse({'request': 'comment.html'})
