from django.contrib import admin
from django.urls import path

import App.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', App.views.home, name="home"),
    path('searchPage/', App.views.searchPage, name="searchPage"),
    path('detail/', admin.site.urls),
    path('detailpage/', App.views.detailpage, name="detailpage"),
    path('troupelist/', admin.site.urls),
    path('listpage/', App.views.listpage, name="listpage"),
]

