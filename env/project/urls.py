from django.contrib import admin
from django.db import router
from django.urls import path,include
# from rest_framework import router
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reservations',views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    #first
    path('django/jsonresponse/',views.no_rest_no_model),
    #second
    path('django/jsonresponsemodel/',views.no_reset_from_model),
    #3.1
    path('django/third/',views.FBV_List),
    #3.2
    path('django/third2/<int:pk>',views.FPV_pk),
    #class 4.1
    path('django/cbv/',views.CBV_LIST.as_view()),
    #4.2
    path('django/cbv/<int:pk>',views.CBV_pk.as_view()),
    #5.1
    path('django/mixins/',views.mixins_list.as_view()),
    #5.2
    path('django/mixins/<int:pk>',views.mixins_pk.as_view()),
    #6.1
    path('django/generics/',views.generics_list.as_view()),
    #6.2
    path('django/generics/<int:pk>',views.generics_pk.as_view()),
    #7
    path('django/viewsets/',include(router.urls)),
    #8 find
    path('fbv/find',views.find_movie),  
    #9 create new
    path('fbv/create',views.create_reservation),
    #10 list user url
    path('api-auth',include('rest_framework.urls')),
    
    #11 Token authentication
    path('api-token-auth',obtain_auth_token)
]
