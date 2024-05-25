from rest_framework import serializers
from .models import Appointment, ConsultingRoom, Owner, Patient, Service, Treatment,Payment
from django.contrib.auth import authenticate
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model= Patient
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields = '__all__'
        
class TreatmentSerializer(serializers.ModelSerializer):
    payment_info = serializers.SerializerMethodField()
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    class Meta:
        model=Treatment
        fields = [
            'id', 'id_patient', 'services', 'date', 'note', 'dental_aucense', 'conserved_teeth', 
            'absence_teeth', 'teeth_to_replace', 'prosthesis_type', 'prosthesis_description', 
            'observations', 'updated_price', 'prosthesis_procedure','payment_info'
        ]
    
    def get_payment_info(self, obj):
        payments = Payment.objects.filter(id_treatment=obj.id)
        payments_serializer =  PaymentSerializer(payments, many= True)
        total = sum(float(payment.contribution) for payment in payments)
        payment_status ={}
        payment_status['name_services']=[service.name for service in obj.services.all()]
        payment_status['total_amount_service'] = sum(service.price for service in obj.services.all())
        payment_status['total_paid'] = total
        payment_status['total_debt'] = sum(service.price for service in obj.services.all()) - total
        payment_status['payments_list'] = payments_serializer.data
        return payment_status
    
    def create(self, validated_data):
        services = validated_data.pop('services')
        treatment = Treatment.objects.create(**validated_data)
        treatment.services.set(services)
        return treatment
        
    
class PaymentSerializer(serializers.ModelSerializer):
    # treatment_service_name = serializers.SerializerMethodField()
    class Meta:
        model =  Payment
        fields = '__all__'
    # def get_treatment_service_name(self, obj):
    #     treatment = Treatment.objects.select_related('servicea').get(id=obj.id_treatment.id)
    #     service_name = treatment.services.name if treatment.services else None
    #     return service_name


class AppointmetSerializer(serializers.ModelSerializer):
    # id_patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    patient_info = PatientSerializer(source='id_patient',read_only=True)
    class Meta:
        model= Appointment
        fields = '__all__'

class ConsultingRoomSerailizer(serializers.ModelSerializer):
    count_appointments = serializers.SerializerMethodField()
    class Meta:
        model = ConsultingRoom
        fields = '__all__'

    def get_count_appointments(self, obj):
        return Appointment.objects.filter(id_consultingRoom=obj.id).count()

class OwnerSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
