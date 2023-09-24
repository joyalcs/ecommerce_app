from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='signin'),
    path('logout/', views.logoutview, name='logout')
]

