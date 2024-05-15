from django.urls import path
from .views import HomeView,event_search, EventView,EventDetailView,EventCreateView,register_for_event,EventUpdateView,EventDeleteView,UserRegisteredEventsView,cancel_registration,PasswordsChangeView,password_success
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("event_list/",EventView.as_view(),name="event_list"),
    path("event/<int:pk>",EventDetailView.as_view(), name="eventdetail"),
    path('event/create/', EventCreateView.as_view(), name='create-event'),
    path('event/register/<int:event_id>/', register_for_event, name='register-for-event'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
    path('registered-events/', UserRegisteredEventsView.as_view(), name='user-registered-events'),
    path('event/cancel-registration/<int:event_id>/', cancel_registration, name='cancel-registration'),
    path("<int:pk>/password/",PasswordsChangeView.as_view(), name="change-password"),
    path('password_success/', password_success, name="password_success"),
    path('event_search/', event_search, name='event_search'),  
]
