from django.http import HttpResponse
from django.shortcuts import render 
from django.shortcuts import redirect
from django.views import View

from .models import Venda, ItemPedido

from .forms import ItemPedidoForm, ItemPedidoModelForm

# Create your views here.
class DashboardView(View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Acesso Negado. Sem permissão para acessar o dashboard')

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        dados = {}

        media = Venda.objects.media()
        media_desc = Venda.objects.media_desconto()
        min = Venda.objects.min()
        max = Venda.objects.max()
        n_pedidos = Venda.objects.n_pedidos()
        nf_emitidas = Venda.objects.notas_emitidas()

        dados['media'] = media
        dados['media_desc'] = media_desc
        dados['min'] = min
        dados['max'] = max
        dados['n_pedidos'] = n_pedidos
        dados['nf_emitidas'] = nf_emitidas

        return render(request, 'vendas/dashboard.html', dados)

class NovoPedido(View):

    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        
        dados = {}
        dados['form_item'] = ItemPedidoForm()
        dados['numero'] = request.POST['numero']
        dados['desconto'] = float(request.POST['desconto'].replace(',', '.'))
        dados['venda_id'] = request.POST['venda_id']

        if dados['venda_id']:
            venda = Venda.objects.get(id=dados['venda_id'])
            venda.desconto = dados['desconto']
            venda.numero = dados['numero']
            venda.save()
        
        else:
            venda = Venda.objects.create(
                numero = dados['numero'], 
                desconto = dados['desconto']
            )

        itens = venda.itempedido_set.all()
        dados['venda'] = venda
        dados['itens'] = itens

        return render(request, 'vendas/novo-pedido.html', dados)

class NovoItemPedido(View):
    def get(self, request, pk):
        pass
    
    def post(self, request, venda):
        dados = {}

        item = ItemPedido.objects.filter(produto_id=request.POST['produto_id'], venda_id=venda) # Retorna um  QuerySet

        if item:
            
            dados = {}
            dados['mensagem'] = 'Item já incluído no pedido, por favor atualize o item'
            item = item[0]

        else:         
            item = ItemPedido.objects.create(
                produto_id = request.POST['produto_id'],
                qtde = request.POST['quantidade'],
                desconto = request.POST['desconto'],
                venda_id = venda)

        dados['item'] = item
        dados['form_item'] = ItemPedidoForm()
        dados['numero'] = item.venda.numero
        dados['desconto'] = item.venda.desconto
        
        dados['venda'] = item.venda
        dados['itens'] = item.venda.itempedido_set.all()

        return render(request, 'vendas/novo-pedido.html', dados)
        
class ListaVendas(View):
    def get(self, request):
        vendas = Venda.objects.all()
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas})

class EditaPedido(View):
    def get(self, request, venda):
        dados = {}
        venda = Venda.objects.get(id=venda)
        dados['form_item'] = ItemPedidoForm()
        dados['numero'] = venda.numero
        dados['desconto'] = float(venda.desconto)
        dados['venda'] = venda
        dados['itens'] = venda.itempedido_set.all()

        return render(
            request, 'vendas/novo-pedido.html', dados
        )

class ExcluiPedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(
            request, 'vendas/exclui-pedido-confirm.html', {'venda': venda}
        )
    
    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')

class ExcluiItemPedido(View):
    def get(self, request, item):
        item = ItemPedido.objects.get(id=item)
        return render(
            request, 'vendas/exclui-itempedido-confirm.html', {'item': item}
        )
    
    def post(self, request, item):
        item = ItemPedido.objects.get(id=item)
        venda_id = item.venda_id
        item.delete()
        return redirect('edita-pedido', venda=venda_id)

class EditaItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemPedido.objects.get(id=item)
        form = ItemPedidoModelForm(instance=item_pedido)

        dados = {}
        dados['form'] = form
        dados['item'] = item_pedido

        return render(
            request, 'vendas/edita-itempedido.html', dados
        )
    
    def post(self, request, item):
        item = ItemPedido.objects.get(id=item)
        item.qtde = request.POST['qtde']
        item.desconto = request.POST['desconto']
        item.save()
        
        venda_id = item.venda_id

        return redirect('edita-pedido', venda=venda_id)