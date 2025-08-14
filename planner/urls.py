from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # default route for api/
    path('services/', views.services, name='services'),
    path('book/', views.book_vehicle, name='book_vehicle'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/verify-otp/', views.verify_otp, name='verify_otp'),
]
