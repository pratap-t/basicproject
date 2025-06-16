from django.urls import path
from . import views

app_name = 'genre'

urlpatterns = [
    path('', views.ListGenre.as_view(), name="all"),
    path('new/', views.CreateGenre.as_view(), name="create"),
    path('<slug:slug>/', views.SingleGenre.as_view(), name="single"),
    path('associate/<slug:slug>/', views.JoinGenre.as_view(), name="join"),
    path('disassociate/<slug:slug>/', views.LeaveGenre.as_view(), name="leave"),
]