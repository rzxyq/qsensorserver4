from django.contrib import admin
from .models import Data, Trial



#python manage.py createsuperuser

#python manage.py shell


class DataInline(admin.TabularInline):
    model = Data

class TrialAdmin(admin.ModelAdmin):
    inlines = [
        DataInline,
    ]


# Register your models here.
admin.site.register(Trial, TrialAdmin)
admin.site.register(Data)
