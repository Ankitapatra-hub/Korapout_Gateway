from django.test import TestCase

# Create your tests here.
from planner.models import Service
from django.contrib.auth.models import User

user = User.objects.create_user('test', 'test@test.com', 'test123')
Service.objects.create(
    name="Royal Enfield Bike Rental",
    service_type="bike",
    description="Best bikes for Koraput hills!",
    price=800,
    location="Koraput",
    available=True,
    owner=user
)