from django.contrib import admin


from .models import (
    Venda, ItemPedido
)

from .actions.nfe.nfe import nfe_emitida, nfe_nao_emitida

#class ItemPedidoInline(admin.StackedInline):
#    model = ItemPedido
#    extra = 1

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


# Register your models here.
class VendaAdmin(admin.ModelAdmin):
    search_fields = ('id', 'pessoa__first_name', 'pessoa__last_name', 'pessoa__doc__num_doc')
    list_display = ['numero', 'nfe_emitida', 'total', 'desconto', 'impostos', 'pessoa', ]

    list_filter = ['pessoa__doc']

    def total(self, obj):
        return obj.valor

    total.short_description = 'Total'

    # Abre a janela para selecionar um contato
    #raw_id_fields = ('pessoa',)

    # AutoComplete
    autocomplete_fields = ('pessoa',)

    readonly_fields = ('valor',)
    actions = [nfe_emitida, nfe_nao_emitida]

    # Filter que passa de uma caixa para outra
    #filter_horizontal = ['produtos']

    inlines = [ItemPedidoInline]


class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'qtde']


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)