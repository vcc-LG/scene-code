from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('games/', views.game_list, name='games-index'),
    path('games/<int:pk_game>/', views.game_detail, name='games-detail'),
    path('games/<int:pk_game>/moves/', views.move_list, name='moves-index'),
    path('games/<int:pk_game>/moves/<int:pk_move>/',
         views.move_detail, name='moves-detail'),
]
