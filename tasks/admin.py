from django.contrib import admin
from .models import Tarea
# Register your models here.

class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ("creado", )


admin.site.register(Tarea, TareaAdmin)