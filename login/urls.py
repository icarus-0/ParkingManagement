from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.SignUp.as_view(),name='signup'),
    path('signin',views.SignIn.as_view(),name='signin'),
    path('logout',views.logout,name='logout'),
]