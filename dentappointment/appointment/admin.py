from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Owner,ConsultingRoom, Appointment,Patient, Treatment, Service, Payment
admin.site.register(Owner)
admin.site.register(ConsultingRoom)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Treatment)
admin.site.register(Service)
admin.site.register(Payment)



# Register your models here.
