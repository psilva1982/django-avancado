from django import forms

from .models import ItemPedido

class ItemPedidoForm(forms.Form):
    produto_id = forms.IntegerField(label='ID do Produto')
    quantidade = forms.IntegerField(label='Quantidade')
    desconto = forms.DecimalField(label='Desconto', max_digits=7, decimal_places=2)

# Outra maneira de implementar Django Form
class ItemPedidoModelForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['qtde', 'desconto']


