from rest_framework import viewsets
from . import serializers as ZERS
from .models import Appointment, ConsultingRoom, Owner, Patient, Service, Treatment, Payment
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from datetime import datetime
import io
import segno
from django.core.files.base import ContentFile
from PIL import Image
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = ZERS.AppointmetSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def appointmentsConsultingRoom(self, request, pk=None):
        appointments = Appointment.objects.prefetch_related('id_patient').filter(id_consultingRoom=pk)
        respon = self.serializer_class(appointments, many= True)
        return Response(respon.data)
    
    @action(detail=True, methods=['get'],url_path='patient', url_name='patient')
    def appointmentsPatients(self, request, pk=None):
        appointments = Appointment.objects.filter(id_patient=pk)
        respon = self.serializer_class(appointments, many= True)
        return Response(respon.data)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
# class CreateAppointmentView(CreateAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = ZERS.AppointmetSerializer

#     @action(detail=True, methods=['post'],url_path='createappointment', url_name='createappointment',permission_classes=[AllowAny])
#     def createAppointmentPublic(self, request, *args, **kwargs):
#         print(request.data['patient']) 
#         # patient =  Patient.objects.create(request.patient)
#         # print(patient)
#         # instance_ap = super().create(request, *args, **kwargs)
        
#         return Response("jejeje")
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)


class ConsultingRoomViewSet(viewsets.ModelViewSet):
    queryset = ConsultingRoom.objects.all()
    serializer_class = ZERS.ConsultingRoomSerailizer

    def list(self, request, *args, **kwargs):
        owner = Owner.objects.get(email=request.user)
        owner_serializer = ZERS.OwnerSerailizer(owner)
        consulting_rooms =  ConsultingRoom.objects.filter(id_owner=owner_serializer.data['id'])
        serializer = self.serializer_class(consulting_rooms, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        instance_cr = super().create(request, *args, **kwargs)
        url = os.getenv("SITE_URL")+'/appointment/gen/'+str(instance_cr.data['id'])
        qrcode = segno.make(url)
        out = io.BytesIO()
        qrcode.save(out, kind='png', light=None, scale=5)

        room_created =  ConsultingRoom.objects.get(id=instance_cr.data['id'])
        qr_name = 'consulting_room_'+str(instance_cr.data['id'])+'.png'
        room_created.qr_code.save(qr_name, ContentFile(out.getvalue()), save=False)
        room_created.save()
        return Response(instance_cr.data, status=instance_cr.status_code)

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = ZERS.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
            },status=status.HTTP_202_ACCEPTED)

       
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = ZERS.PatientSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def patientesPerConsultingRoom(self, request,pk=None):
        patients =  Patient.objects.filter(id_consultingRoom=pk)
        result = self.serializer_class(patients, many=True)
        return Response(result.data)
    
class SericeView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class =  ZERS.ServiceSerializer

    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def servicesPerConsultingRoom(self, request,pk=None):
        services =  Service.objects.filter(id_consultingRoom=pk)
        result = self.serializer_class(services, many=True)
        return Response(result.data)
    
class TreatmentView(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class =  ZERS.TreatmentSerializer

    def create(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=request.data['id_patient'])
        service =  Service.objects.get(id=request.data['id_service'])
        treatment_created = Treatment.objects.create(
            id_patient=patient,
            id_service=service,
            note=request.data['note'],
            date=request.data['date'],
        )
        consultingroom =  ConsultingRoom.objects.get(id=request.data['id_consultingRoom'])
        Payment.objects.create(id_consultingRoom=consultingroom,contribution=request.data['payment'],id_treatment=treatment_created)
        treatment_serializer = self.serializer_class(treatment_created)
        return Response(treatment_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'],url_path='patient', url_name='patient')
    def treatmentsPatients(self, request, pk=None):
        treatments = Treatment.objects.filter(id_patient=pk)
        respon = self.serializer_class(treatments, many= True)
        return Response(respon.data)

class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class =  ZERS.PaymentSerializer

    def create(self, request, *args, **kwargs):
        instance_cr = super().create(request, *args, **kwargs)
        query = Payment.objects.filter(id_treatment=request.data['id_treatment'])
        serializer = self.serializer_class(query,many=True)
        return Response(serializer.data, status=instance_cr.status_code)
    
    @action(detail=True, methods=['get'],url_path='consultingroom', url_name='consultingroom')
    def treatmentsPatients(self, request, pk=None):
        payments = Payment.objects.filter(id_consultingRoom=pk)
        respon = self.serializer_class(payments, many= True)
        return Response(respon.data)
    
    

