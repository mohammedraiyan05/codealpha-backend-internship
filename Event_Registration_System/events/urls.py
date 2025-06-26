from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list),
    path('events/<int:event_id>/', views.event_detail),
    path('register/', views.register_event),
    path('registrations/', views.view_registrations),
    path('cancel/<int:reg_id>/', views.cancel_registration),
]
