from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View

# TODO: Refatorar para usar threads assim que possível
def home(request):


    '''
    # Debug modo HARD
    import pdb
    pdb.set_trace()

    Executar o servidor pelo terminal
    l - visualizar códgo
    n - para seguir para o próxima linha
    c - continue
    '''

    return render(request, 'home.html')

# FIXME: Corrigir bug
def my_logout(request):
    logout(request)
    return redirect('home')

class MyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home3.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('retornando do post')

class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['minha_variavel'] = 'Olá, seja bem vindo ao curso'
        return contexto