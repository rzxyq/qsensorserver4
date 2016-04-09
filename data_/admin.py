from django.contrib import admin
from .models import Data, Trial

# Register your models here.
admin.site.register(Trial)
admin.site.register(Data)

#python manage.py createsuperuser

#python manage.py shell