"""
URL configuration for webgame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tictactoe import views

from django.urls import path
from django.shortcuts import render

def test_audio(request):
    return render(request, 'tictactoe/play_game_test.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new/', views.new_game, name='new_game'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),
    path('results/', views.results, name='results'),
    path('clear/', views.clear_all, name='clear_all'),
    path('play2/<int:game_id>/', views.play_game2, name='play_game2'),
    path('new_with/<int:game_id>/', views.new_game_with_players, name='new_game_with_players'),

]
