# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render
from . import models
from datetime import datetime

import base64
import os


def home(request):
    return JsonResponse({'request': 'home.html'})


def search_play(request):
    return JsonResponse({'request': 'search_play.html'})


def search_troupe(request):
    return JsonResponse({'request': 'search_troupe.html'})


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
