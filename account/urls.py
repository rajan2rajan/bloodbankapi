from account.views import *
from django.urls import path

urlpatterns = [
    # register user 
    path('register/',UserRegistrationView.as_view(),name = 'register'),
    # login user  
    path('login/',LoginView.as_view(),name = 'login'),
    # logout user
    path('logout/',LogoutView.as_view(),name = 'logout'),
    # afte login visit profile 
    path('profile/',UserProfileView.as_view(),name = 'profile'),
    # change password without email
    path('passwordchange/',ChangePasswordView.as_view(),name = 'passwordchange'),
    # sending mail 
    path('sendemail/',EmailPasswordView.as_view(),name = 'sendemail'),
    # change password with email 
    path('change/<uid>/<token>/',ResetView.as_view(),name = 'change'),
    # this is to do submit donor who donare blood 
    path('editdonor/',EditDonerView.as_view(),name = 'editdonor'),
    path('editdonor/<pk>',EditDonerView.as_view(),name = 'editdonor'),
    # this is for reciver form Post 
    path('requestform/',RequestorFormView.as_view(),name = 'requestform'),
    # all the requestor who request the blood 
    path('requestor/',RequestorView.as_view(),name = 'requestor'),
    # this is for those who are emergency 
    path('emergency/',VerifyReciverEmergencyView.as_view(),name = 'emergency'),
    # this is for those who are not in emergency
    path('nonemergency/',VerifyReciverView.as_view(),name = 'nonemergency'),
    




]
