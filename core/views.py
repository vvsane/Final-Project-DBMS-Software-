from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Event, Attendance, Fee
from core.forms import EventForm, AttendanceForm, FeeForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EventSerializer, FeeSerializer, AttendanceSerializer

# -------------------------------
# AUTHENTICATION VIEWS
# -------------------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# -------------------------------
# DASHBOARD VIEW
# -------------------------------

@login_required(login_url='login')
def dashboard(request):
    context = {
        'username': request.user.username,
        'events': Event.objects.all(),
        'attendances': Attendance.objects.count(),
        'fees': Fee.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)

# -------------------------------
# ATTENDANCE VIEWS
# -------------------------------

@login_required(login_url='login')
def attendance(request):
    if request.user.is_staff:
        # Admin sees all records grouped by event
        records = Attendance.objects.select_related('user', 'event').order_by('event__date')
        grouped_records = defaultdict(list)
        for record in records:
            grouped_records[record.event].append(record)
        context = {
            'grouped_records': grouped_records.items(),
            'is_admin': True
        }
    else:
        # Regular user sees only their own attendance
        records = Attendance.objects.filter(user=request.user).select_related('event').order_by('event__date')
        context = {
            'records': records,
            'is_admin': False
        }

    return render(request, 'core/attendance.html', context)

@login_required
def attendance_mark(request):
    if not request.user.is_staff:
        return redirect('attendance')

    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('attendance')

    return render(request, 'core/form_template.html', {
        'form': form,
        'title': 'Mark Attendance',
        'cancel_url': 'attendance'
    })

@login_required(login_url='login')
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)

    form = AttendanceForm(request.POST or None, instance=attendance)
    if form.is_valid():
        form.save()
        return redirect('attendance')
    
    return render(request, 'core/form_template.html', {
        'form': form,
        'title': 'Edit Attendance',
        'cancel_url': 'attendance'
    })

@login_required(login_url='login')
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance')
    return render(request, 'core/attendance_confirm_delete.html', {'attendance': attendance})

# -------------------------------
# EVENTS VIEWS
# -------------------------------
@login_required(login_url='login')
def events(request):
    events = Event.objects.all()
    return render(request, 'core/events.html', {
        'events': events,
        'is_admin': request.user.is_staff
    })

@login_required
def event_create(request):
    if not request.user.is_staff:
        return redirect('events')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Handle image uploads
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm()

    return render(request, 'core/form_template.html', {
        'form': form,
        'title': 'Add Event',
        'cancel_url': 'events'
    })

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm(instance=event)

    return render(request, 'core/form_template.html', {
        'form': form,
        'title': 'Edit Event',
        'cancel_url': 'events'
    })

@login_required(login_url='login')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events')
    return render(request, 'core/event_confirm_delete.html', {'event': event})

# -------------------------------
# FEES VIEWS
# -------------------------------

@login_required(login_url='login')
def fees(request):
    if request.user.is_staff:
        fees = Fee.objects.select_related('user')
    else:
        fees = Fee.objects.filter(user=request.user)

    return render(request, 'core/fees.html', {
        'fees': fees,
        'is_admin': request.user.is_staff
    })

@login_required(login_url='login')
def fee_create(request):
    if not request.user.is_staff:
        return redirect('fees')
    form = FeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fees')
    return render(request, 'core/fee_form.html', {'form': form})

@login_required(login_url='login')
def fee_update(request, pk):
    if not request.user.is_staff:
        return redirect('fees')  
    fee = get_object_or_404(Fee, pk=pk)
    form = FeeForm(request.POST or None, instance=fee)
    if form.is_valid():
        form.save()
        return redirect('fees')
    return render(request, 'core/fee_form.html', {'form': form})

@login_required(login_url='login')
def fee_delete(request, pk):
    if not request.user.is_staff:
        return redirect('fees')  # Only admins can delete
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        return redirect('fees')
    return render(request, 'core/fee_confirm_delete.html', {'fee': fee})

# -------------------------------
# API VIEWS
# -------------------------------

@api_view(['GET'])
def event_list_api(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fee_list_api(request):
    fees = Fee.objects.all()
    serializer = FeeSerializer(fees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def attendance_list_api(request):
    attendance = Attendance.objects.all()
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data)
