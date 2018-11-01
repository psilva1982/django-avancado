from django.contrib import admin
from .models import Person, Documento, Venda, Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'preco']

class PersonAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'age', 'doc']

admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
admin.site.register(Venda)
admin.site.register(Produto, ProdutoAdmin)
