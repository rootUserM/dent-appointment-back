from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin
import uuid
# Create your models here.

class CreateRegisBase(models.Model): 
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.BigAutoField(primary_key=True)
    date_created =  models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(auto_now_add=True)

class Owner(AbstractUser,PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    username = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class ConsultingRoom(CreateRegisBase):
    name = models.CharField(max_length=100,null=False,default='')
    id_owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    webpage =  models.URLField()
    email =  models.EmailField(null=True)
    phone_number = models.CharField(max_length=10,null=True)
    qr_code = models.ImageField(upload_to='consultingroom-qrcodes/', null=True)
    def __str__(self):
        return self.name

class Patient(CreateRegisBase):
    Name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Second_last_name = models.CharField(max_length=100,blank=True)
    Eage = models.CharField(max_length=100,blank=True)
    Gender = models.CharField(max_length=100)
    Email = models.EmailField(blank=True)
    PhoneNumber =  models.CharField(max_length=100,unique=True)
    id_consultingRoom = models.ForeignKey(ConsultingRoom, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.Name 
    
class Service(CreateRegisBase):
    id_consultingRoom = models.ForeignKey(ConsultingRoom, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    active= models.BooleanField(default=False)
    def __str__(self):
        return self.name 


class Treatment(CreateRegisBase):
    id_patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    id_service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    date= models.DateField(null=True,db_comment="Fecha en la que el tratamiento normal fue entregado/realizado")
    note =  models.CharField(null=True,max_length=100)
    dental_aucense = models.CharField(null=True,max_length=100,)
    conserved_teeth = models.CharField(null=True,max_length=100)
    absence_teeth = models.CharField(null=True,max_length=100)
    teeth_to_replace = models.CharField(null=True,max_length=100)
    prosthesis_type = models.CharField(null=True,max_length=100)
    prosthesis_description = models.CharField(null=True,max_length=100)
    observations = models.CharField(null=True,max_length=100)
    updated_price = models.FloatField(null=True)
    prosthesis_procedure = models.JSONField(null=True,db_comment="Configuracion en caso de que el tratamineto sea protesis")

class Payment(CreateRegisBase):
    id_consultingRoom = models.ForeignKey(ConsultingRoom, null=True, on_delete=models.CASCADE)
    id_treatment = models.ForeignKey(Treatment, null=True, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=50)

class Appointment(CreateRegisBase):
    appointmentDate = models.DateField()
    appointmentHour = models.TimeField(default=timezone.now)
    id_consultingRoom = models.ForeignKey(ConsultingRoom, null=True, on_delete=models.CASCADE)
    appointmentMotive =  models.CharField(max_length=100)
    firstTimePatient =  models.BooleanField()
    status = models.CharField(max_length=100,default='Programada')
    id_patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    id_service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.id_consultingRoom





