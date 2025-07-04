from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name="logout"),
]
