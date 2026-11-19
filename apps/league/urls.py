from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns =[
    path('salir/', LogoutView.as_view(next_page='home'), name='league_logout'),
    path('', views.home, name='home'),
    path('equipos/', views.TeamList.as_view(), name='team_list'),
    path('equipos/nuevo/', views.TeamCreate.as_view(), name='team_create'),
    path('equipos/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),
    path('equipos/<int:pk>/editar/', views.TeamUpdate.as_view(), name='team_update'),
    path('equipos/<int:pk>/eliminar/', views.TeamDelete.as_view(), name='team_delete'),
    path('jugadores/', views.PlayerList.as_view(), name='player_list'),
    path('jugadores/nuevo/', views.PlayerCreate.as_view(), name='player_create'),
    path('jugadores/<int:pk>/', views.PlayerDetail.as_view(), name='player_detail'),
    path('jugadores/<int:pk>/editar/', views.PlayerUpdate.as_view(), name='player_update'),
    path('jugadores/<int:pk>/eliminar/', views.PlayerDelete.as_view(), name='player_delete'),
]
