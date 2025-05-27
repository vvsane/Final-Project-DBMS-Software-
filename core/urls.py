from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('attendance/', views.attendance, name='attendance'),
    path('events/', views.events, name='events'),
    path('fees/', views.fees, name='fees'),

    # Event CRUD
    path('events/create/', views.event_create, name='event_create'),
    path('events/update/<int:pk>/', views.event_update, name='event_update'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),

    # Attendance CRUD
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('attendance/edit/<int:pk>/', views.attendance_edit, name='attendance_edit'),
    path('attendance/delete/<int:pk>/', views.attendance_delete, name='attendance_delete'),

    # Fees
    path('fees/create/', views.fee_create, name='fee_create'),
    path('fees/update/<int:pk>/', views.fee_update, name='fee_update'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),

    # API
    path('api/events/', views.event_list_api, name='api-events'),
    path('api/fees/', views.fee_list_api, name='api-fees'),
    path('api/attendance/', views.attendance_list_api, name='api-attendance'),
]

