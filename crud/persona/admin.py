from django.contrib import admin
from .models import Persona

# Register your models here.
#admin.site.register(Persona)
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad', 'oficina')
    search_fields = ('nombre', 'apellido', 'oficina__nombre')
