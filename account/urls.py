from account.views import *
from django.urls import path,include
from account import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# this urls is for admin to do crud operation 
router.register('homeadmin',views.PostAdminView,basename="postadmin")



urlpatterns = [
    path('',include(router.urls)),
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
    # this urls is for normal user to see the post done by admin 
    path('home/<pk>/',UserSeeView.as_view(),name="home"),
    # this urls is when normal user click on post for detail 
    path('home/',UserSeeView.as_view(),name="home"),

    path('aprove/<pk>/',Aprove.as_view(),name="aprove"),
  






    # yedi pagination ko lagi xuti chiyako xa vana mtra use garne  ntra mathi last ra second last ma pagination, search ra list ko lagi bani sakako xa  
    
    # this is for pagination in emergency 
    path('paginationemergency/',PaginationEmergencyView.as_view(),name = 'paginationemergency'),
    # this is for pagination in non emergency 
    path('paginationnonemergency/',PaginationNonEmergencyView.as_view(),name = 'paginationnonemergency'),



  


# this urls is to show all the list of item contain in the database in the form of table 
  path('list',Listdata.as_view() , name='listview')
]
