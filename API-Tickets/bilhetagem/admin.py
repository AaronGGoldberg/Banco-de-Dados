from django.contrib import admin

from .models import (
    Municipio,
    EmpresaTransporte,
    Usuario,
    TipoTicket,
    Ticket,
    Transporte,
    Validador,
    Validacao
)

admin.site.register(Municipio)
admin.site.register(EmpresaTransporte)
admin.site.register(Usuario)
admin.site.register(TipoTicket)
admin.site.register(Ticket)
admin.site.register(Transporte)
admin.site.register(Validador)
admin.site.register(Validacao)