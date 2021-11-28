from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('driver-standings', views.api_driverStandings, name='api-driverStandings'),
    path('constructor-standings', views.api_constructorStandings, name='api-constructorStandings' ),
    path('teams/<str:team>', views.api_teamInfo, name='api-teamInfo')
]