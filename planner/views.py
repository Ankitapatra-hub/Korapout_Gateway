from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Service, Booking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

@login_required
def book_vehicle(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.otp = str(random.randint(100000, 999999))
            booking.save()
            return render(request, 'planner/thank_you.html', {'booking': booking})
    else:
        form = BookingForm()
    return render(request, 'planner/book_vehicle.html', {'form': form})

@csrf_exempt
def services(request):
    if request.method == 'GET':
        service_type = request.GET.get('type', '')
        services = Service.objects.filter(available=True)
        if service_type:
            services = services.filter(service_type=service_type)
        data = [{
            'id': s.id,
            'name': s.name,
            'type': s.service_type,
            'description': s.description,
            'price': float(s.price),
            'location': s.location
        } for s in services]
        return JsonResponse(data, safe=False)

@login_required
@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            service = Service.objects.get(id=service_id)
            booking = Booking.objects.create(
                user=request.user,
                service=service,
                start_date=start_date,
                end_date=end_date,
                otp=str(random.randint(100000, 999999))
            )
            return JsonResponse({
                'success': True,
                'booking_id': booking.id,
                'otp': booking.otp
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@login_required
def verify_otp(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        otp = request.POST.get('otp')
        
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            if booking.otp == otp:
                booking.otp_verified = True
                booking.status = 'completed'
                booking.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
