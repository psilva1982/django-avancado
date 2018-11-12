from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Venda

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