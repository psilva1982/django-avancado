from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Venda, ItemPedido

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
        dados['numero'] = request.POST['numero']
        dados['desconto'] = float(request.POST['desconto'])
        dados['venda'] = request.POST['venda_id']

        if dados['venda']:
            venda = Venda.objects.get(id=dados['venda'])
        
        else:
            venda = Venda.objects.create(
                numero = dados['numero'], 
                desconto = dados['desconto']
            )

        itens = venda.itempedido_set.all()
        dados['venda_obj'] = venda
        dados['itens'] = itens

        return render(request, 'vendas/novo-pedido.html', dados)
    