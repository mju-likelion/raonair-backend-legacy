from django.contrib import admin
from django.urls import path

import App.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home', App.views.home, name='home'),  # 홈페이지
    path('api/search/play', App.views.search_play,
         name='search_play'),  # 검색결과페이지
    path('api/search/play/<str:type>', App.views.search_detail,
         name='search_detail'),  # 검색결과페이지, 더보기 클릭
    path('api/troupe/<int:id>', App.views.troupe, name='troupe'),  # 극단개별페이지
    path('api/play/<int:id>', App.views.play, name='play'),  # 연극개별페이지
    path('api/auth/signin', App.views.signin),  # 로그인
    path('api/auth/signup', App.views.signup, name='signup'),  # 회원가입
    path('api/auth/find-password', App.views.password, name='password'),  # 비밀번호찾기
    path('api/plays/:id/star', App.views.star, name='star'),  # 별점
    path('api/plays/:id/liked', App.views.playlike, name='playlike'),  # 연극찜하기
    path('api/troupes/:id/like', App.views.troupelike, name='troupelike'),  # 극단찜하기
    path('api/plays/:id/comment', App.views.comment, name='comment'),  # 커멘트달기
]
