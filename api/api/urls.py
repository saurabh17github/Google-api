from django.urls import path
from api.views import GoogleCalendarInitView, GoogleCalendarRedirectView, CalendarHomeView

urlpatterns = [
    path('google/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar-init'),
    path('google/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='calendar-redirect'),
    path('calendar/home/', CalendarHomeView.as_view(), name='calendar-home'),
]
