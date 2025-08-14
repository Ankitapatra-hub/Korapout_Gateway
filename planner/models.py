from django.db import models
from django.conf import settings  # Gives access to AUTH_USER_MODEL

class Service(models.Model):
    SERVICE_TYPES = [
        ('bike', 'Bike Rental'),
        ('car', 'Car Rental'),
        ('camping', 'Camping Equipment'),
        ('hotel', 'Hotel/Stay'),
        ('guide', 'Local Guide'),
    ]
    
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # updated

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # updated
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        default='pending', 
        choices=[
            ('pending', 'Pending'), 
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ]
    )
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.service.name}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars for {self.booking.service.name}"
