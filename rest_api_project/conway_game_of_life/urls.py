from django.urls import path, include
from conway_game_of_life import views

urlpatterns = [
    path('', views.GridList),
    path('<int:pk>', views.GridDetail),
    path('<int:pk>/', views.GridAfter),
]