from django.shortcuts import render, redirect, render_to_response
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

        # Trabalhando com cookies
        response = render_to_response('home3.html')

        # Setando um cookie
        response.set_cookie('cor', 'azul', max_age=1000)    # max_age - cookie expira em 1000 segundos

        # Lendo um cookie
        meu_cookie = request.COOKIES.get('cor')
        print('>>>> ' +meu_cookie)

        return response


    def post(self, request, *args, **kwargs):
        return HttpResponse('retornando do post')

class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['minha_variavel'] = 'Olá, seja bem vindo ao curso'
        return contexto