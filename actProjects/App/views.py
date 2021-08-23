import jwt
import os
import base64
from datetime import datetime
from django.views.decorators.http import require_http_methods
import re
import json
from . import models
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models.fields import EmailField
import bcrypt
# from test01.settings import SECRET_KEY


secret = "raonair"


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


def search_troupe_detail(request):
    query = request.GET.get('query', '')
    type = request.GET.get('type', '')
    limit = request.GET.get('limit', '')
    limit = int(limit)

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
            '&start=')[0] + '&start=' + str(start+limit)
    else:
        start = 0
        next = request.get_full_path() + '&start=' + str(limit)

    for i in troupes:
        new_troupe = ({
            'id': i.id,
            'name': i.name,
            'type': i.type,
            'logo': i.logo,
        })
        search_list.append(new_troupe)
    print(len(search_list[start:start+limit]))

    # 더 로딩할 데이터가 없는 경우
    if (len(search_list[start:start + limit]) < limit):
        return JsonResponse({
            'links': {
                'next': ''
            },
            'data': {
                'query': query,
                'type': type,
                'search_results': search_list[start:start+limit]
            },
        })
    if search_list[start] == search_list[-1]:
        return JsonResponse({
            'links': {
                'next': ''
            },
            'data': {
                'query': query,
                'type': type,
                'search_results': search_list[start:start + limit]
            },
        })

    return JsonResponse({
        'links': {
            'next': next,
        },
        'data': {
            'query': query,
            'type': type,
            'search_results': search_list[start:start+limit]
        }
    })


# 로그인
def signin(request):
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

    today = datetime.strftime(datetime.now(), '%Y-%m-%d')

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
        star_count = stars.count() if (stars.count()) else 1
        star_avg = star_sum / star_count / 2

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
        if today >= start_date and (end_date == None or today <= end_date):
            ongoing_list.append(new_play)
        elif today < start_date:
            tobe_list.append(new_play)
        elif today > end_date:
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
    limit = request.GET.get('limit', '')
    limit = int(limit)

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
            + str(start + limit)
    else:
        start = 0
        next = request.get_full_path() + '&start=' + str(limit)

    for i in plays:
        stars = models.Star.objects.filter(play=i.id)
        likes = models.Like.objects.filter(play=i.id).count()

        # 평균 별점 구하기
        star_sum = 0
        for j in stars:
            star_sum += j.star
        star_count = stars.count() if (stars.count()) else 1
        star_avg = star_sum / star_count / 2

        new_play = ({
            'id': i.id,
            'title': i.title,
            'poster': i.poster,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'star_avg': star_avg,
            'likes': likes,
            'location': i.theater.location,
        })
        search_list.append(new_play)

    # 더 로딩할 데이터가 없는 경우
    if len(search_list[start:start+limit]) < limit:
        return JsonResponse({
            'links': {
                'next': ''
            },
            'data': {
                'query': keyword,
                'type': type,
                'search_results': search_list[start:start+limit],
            },
        })

    # 더 로딩할 데이터가 있는 경우
    return JsonResponse({
        'links': {
            'next': next
        },
        'data': {
            'query': keyword,
            'type': type,
            'search_results': search_list[start:start+limit],
        },
    })

# 직책 필드는 극단이 아닌 연극에 종속적이라 극단에서 구현하기 어려움에 있음
# ex) 극단에서는 감독이지만 A 공연에서는 배우일 경우


@csrf_exempt
def troupe(request, id):
    troupe = models.Troupe.objects.get(id=id)
    troupe_like = models.TroupeLike.objects.filter(troupe=id).count()
    '''
    # JWT Token 활용 user의 정보를 가져온다.
    encoded_jwt = request.headers.get('Authorization', None)
    token = encoded_jwt.split('Bearer ')[1]
    payload = jwt.decode(token, 'raonair', algorithms=['HS256'])
    user_id = models.User.objects.get(id=payload['id'])
    '''
    if request.user.is_authenticated:  # 사용자가 로그인 했을 때만 body에서 값을 읽음
        body = json.loads(request.body)
        if not models.User.objects.filter(id=body['user']):
            return JsonResponse({
                'message': '로그인된 사용자가 아닙니다',
            }, status=401)
        user_id = models.User.objects.get(id=body['user'])
        troupe_like_check = models.TroupeLike.objects.filter(
            troupe=id, user=user_id).exists()  # user 추후 수정 필요(더미데이터)
    else:
        troupe_like_check = False

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
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    for i in plays:
        start_date = datetime.strftime(i.start_date, '%Y-%m-%d')
        end_date = datetime.strftime(
            i.end_date, '%Y-%m-%d') if (i.end_date) else None

        new_play = {
            'id': i.id,
            'title': i.title,
            'poster': i.poster,
            'start_date': start_date,
            'end_date': end_date,
        }

        if today >= start_date and (end_date == None or today <= end_date):
            ongoing_play.append(new_play)
        elif today < start_date:
            tobe_play.append(new_play)
        elif today > end_date:
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
            'context': {
                'like_check': troupe_like_check
            },
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
            },
        },
    })


def troupe_options(request):
    troupe_type = {'noraml': '일반', 'student': '학생'}

    return JsonResponse({
        'data': {
            'troupe_option': troupe_type
        }
    })


def play(request):
    return JsonResponse({'request': 'play.html'})


@csrf_exempt
@require_http_methods(["POST"])
def signin(request):

    request_body = json.loads(request.body)

    # 400_BAD_REQUEST // 아이디 형식이 틀린 경우
    if not re.match(r'^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$', request_body['email']):
        return JsonResponse({
            "error": {
                "message": "올바른 이메일 형식이 아닙니다."
            }
        }, status=400)

    # 403 // 아이디가 디비에 존재하지 않는 경우
    if not models.User.objects.filter(email=request_body['email']):
        return JsonResponse({
            "error": "존재하지않는 아이디입니다."
        }, status=403)

    signinuser = models.User.objects.get(email=request_body['email'])

    password = request_body['password']  # 로그인 시 입력받은 패스워드
    db_password = signinuser.password  # 디비에 저장되어있는 패스워드

    # 401 // 아이디는 맞는데, 비밀번호 오류
    if not bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
        return JsonResponse({
            "error": "비밀번호가 틀렸습니다."
        }, status=401)

    # 200 // 로그인 완료
    login = HttpResponse(json.dumps({
        "message": {
            "nickname": signinuser.nickname,
            "id": signinuser.id}  # 바디에 저장한 id
    }))

    # 쿠키
    encoded = jwt.encode({'email': signinuser.email}, secret, algorithm='HS256')
    login.set_cookie(
        '_h_udin',
        encoded,
        max_age=60*60*24*7,  # 7일동안
        httponly=True,  # http요청일때만
        path='/',
        domain=None,
        secure=False,
        samesite=None  # CSRF 보호 방법 제공
    )
    return login


# 로그아웃시
# @login_decorator
# def logout(request):
#     logout = JsonResponse({
#         "message": "로그아웃 되었습니다."})
#     logout.set_cookie('encoded', '')

#     return logout


# 로그인 쿠키
# def login_decorator(func):

#     def wrapper(self, request, *args, **kwargs):  # self > 받아온 함수를 다시 넘긴다 access token이 헤더에 들어있음> json.load가 아님(헤더에 있는 값만 할 것임) > 키 벨류로 돼있는 양식 >

#         if "Authorization" not in request.headers:  # 1)번
#             return JsonResponse({"error_code": "INVALID_LOGIN"}, status=401)

#         encoded = request.headers["Authorization"]

#         try:
#             data = jwt.decode(encoded, secret, algorithm='HS256')
#             # 2번)decode를 하게 될 경우 프론트엔드에 전달했던 페이로드값만 나옴(즉 로그인뷰에 바디)

#             user = models.User.objects.get(id=data["id"])  # 3번
#             request.user = user  # 4번
#         except jwt.DecodeError:  # 2-1번 error
#             return JsonResponse({
#                 "error_code": "INVALID_TOKEN"
#             }, status=401)  # 401에러 : 권한이 없을때 발생
#         except Accounts.DoesNotExist:  # 1-1번 error
#             return JsonResponse({
#                 "error_code": "UNKNOWN_USER"
#             }, status=401)  # 401에러 : 권한이 없을때 발생

#         return func(self, request, *args, **kwargs)  # 5번

#     return wrapper


def password(request):
    return JsonResponse({'request': 'find-password.html'})


@csrf_exempt
@require_http_methods(['POST'])
def playlike(request, id):
    input = json.loads(request.body)
    play = models.Play.objects.get(id=id)
    user = models.User.objects.get(id=input['user'])
    check_play_like = models.Like.objects.filter(
        play=play.id, user=user.id)  # 찜 여부 판단

    if check_play_like.exists():
        check_play_like.delete()
        return JsonResponse({
            'data': {
                'play': play.title,
                'email': user.email,
                'nickname': user.nickname,
            },
            'message': 'deleted play like'
        }, status=200)
    else:
        new_play_like = models.Like.objects.create(play=play, user=user)
        return JsonResponse({
            'data': {
                'id': new_play_like.id,
                'play': new_play_like.play.title,
                'email': new_play_like.user.email,
                'nickname': new_play_like.user.nickname,
            },
            'message': 'add play like'
        }, status=200)


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

@ csrf_exempt
@ require_http_methods(['POST'])
def star(request, id):
    # id 는 play의 id이다.
    user_body = json.loads(request.body)

    # 존재하지 않는 ID인 경우
    if not models.User.objects.get(id=user_body['user']):
        return JsonResponse({
            'message': '로그인된 사용자가 아닙니다',
        }, status=401)
    user = models.User.objects.get(id=user_body['user'])
    selected_play = models.Play.objects.get(id=id)

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
    body = json.loads(request.body)

    if not models.User.objects.filter(id=body['user']):
        return JsonResponse({
            'message': '로그인된 사용자가 아닙니다',
        }, status=401)

    comment_user = models.User.objects.get(id=body['user'])
    comment_play = models.Play.objects.get(id=id)

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


# 회원가입
@ csrf_exempt
@ require_http_methods(["POST"])
def signup(request):
    input = json.loads(request.body)

    # 403_BAD_REQUEST

    # 아이디(이메일) 형식 오류

    if not re.match(r'^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$', input['email']):
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

    if re.match(r"^[가-힣]{2, 4}$", input['name']):
        return JsonResponse({
            "error": "올바른 이름 형식이 아닙니다."
        }, status=400)

    # 409_CONFLICT

    if models.User.objects.filter(email=input['email']):
        return JsonResponse({
            "data": "이미 존재하는 아이디입니다."
        }, status=409)

    # 200_OK
    password = input['password']
    # bytes(password, 'utf-8')
    # password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    decode_password = hashed_password.decode('utf-8')

    userdata = models.User.objects.create(
        email=input['email'], password=decode_password, nickname=input['nickname'], name=input['name'])

    return JsonResponse({
        "data": {
            "id": userdata.id,  # 사용자의 id
            "email": userdata.email,  # 사용자의 email
            "nickname": userdata.nickname,  # 사용자의 nickname
            "name": userdata.name,  # 사용자의 이름
        },
        "message": "회원가입이 완료되었습니다."
    }, status=200)
