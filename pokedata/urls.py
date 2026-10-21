from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemon-table/', views.pokemon_table, name='pokemon_table'),
    path('team-builder/', views.team_builder, name='team_builder'),
    path('moves/', views.moves, name='moves'),
] 