from django.contrib import admin

from .models import (
    Person,
    Documento,

)


class PersonAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Dados Gerais', {
          'fields': (('first_name', 'last_name'),
              ('age', 'doc'))
        }),

        ('Complemento', {
            'classes': ('collapse',),
            'fields': ('bio', 'salary', 'photo')
        })
    )

    #fields = (('doc', 'first_name'), 'last_name', ('age', 'salary'), 'bio', 'photo')

    # Exibe apenas os campos específicados
    # fields = ('first_name', 'second_name')

    # Exclui os campos
    # exclude = ('bio')

    # Campos exibidos na tabela
    list_display = ['nome_completo', 'age', 'doc', 'tem_foto']
    list_filter = ['age', 'salary']

    def tem_foto(self, obj):
        if obj.photo:
            return True
        else:
            return False

    tem_foto.short_description = 'Foto'
    search_fields = ('first_name', 'last_name','doc__num_doc',)



admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
