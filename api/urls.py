from django.urls import path
from . import views

urlpatterns = [
    path('create_game/', views.create_game, name='create_game'),
    path('get_score/', views.get_score, name='get_score'),
    path('register_round/', views.register_round, name='register_round'),
]