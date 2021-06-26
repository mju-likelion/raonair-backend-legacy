from django.contrib import admin
from django.urls import path

import App.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', App.views.home, name="home"),
    path('searchPage', App.views.searchPage, name="searchPage"),
]


urlpatterns = [
    path('/detail', admin.site.urls),
    path('', App.views.home, name="detailpage"),
    path('detailpage', App.views.detailpage, name="detailpage"),
]