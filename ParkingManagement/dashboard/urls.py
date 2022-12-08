from django.urls import path
from . import views

urlpatterns = [
    path('home',views.HomePage.as_view(),name='homepage'),
    path('initialize_data',views.InitializeParkingData.as_view(),name='initialize_data'),
    path('book_parking_space',views.BookParkingSpace.as_view(),name='book_parking_space'),
    path('release_parking_space',views.ReleaseParkingSpace.as_view(),name='release_parking_space'),
    path('reports',views.Reports.as_view(),name='reports'),
]