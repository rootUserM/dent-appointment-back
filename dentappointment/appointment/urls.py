from rest_framework import routers
from .views import AppointmentViewSet, ConsultingRoomViewSet, LoginView, PatientView,SericeView, TreatmentView, PaymentView
from django.urls import path,include

routers = routers.DefaultRouter()

routers.register(r'appointment',  AppointmentViewSet,basename='appointment' )
routers.register(r'consultingroom',ConsultingRoomViewSet,basename='consultingroom') 
routers.register(r'patients',PatientView,basename='patients') 
routers.register(r'services',SericeView,basename='services')
routers.register(r'treatments',TreatmentView,basename='treatments')
routers.register(r'payments',PaymentView,basename='payments')


