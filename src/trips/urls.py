from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.WelcomeView.as_view(), name='index'),
    path('welcome', views.WelcomeView.as_view(), name='welcome'),
    path('destination', views.DestinationView.as_view(), name='destination'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('saved_trips/', views.saved_trips, name='saved_trips'),
    path('view_trip/', views.view_trip, name='view_trip'),
    path('profile/', views.profile, name='profile'),
    path('compare/', views.compare, name='compare'),
    path('new_account/', views.new_account, name='new_account'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('view_flight/', views.ViewFlightView.as_view(), name='view_flight'),
]