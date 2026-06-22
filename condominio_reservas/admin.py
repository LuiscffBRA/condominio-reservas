from django.contrib import admin
from .models import Usuario, Morador, Administrador, Sindico, AreaComum, Reserva

admin.site.register(Usuario)
admin.site.register(Morador)
admin.site.register(Administrador)
admin.site.register(Sindico)
admin.site.register(AreaComum)
admin.site.register(Reserva)