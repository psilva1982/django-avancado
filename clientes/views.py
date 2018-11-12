from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Person
from produtos.models import Produto
from vendas.models import Venda

from .forms import PersonForm


@login_required
def persons_list(request):

    nome = request.GET.get('nome' or None)
    sobrenome = request.GET.get('sobrenome' or None)

    dados = {}
    dados['footer_message'] = 'Desenvolvido com Django'

    if nome or sobrenome:
        # nome ou sobrenome
        persons = Person.objects.filter(first_name__icontains=nome) | Person.objects.filter(last_name__icontains=sobrenome)
        dados['persons'] = persons

    else:
        dados['persons'] = Person.objects.all()


    return render(request, 'person.html', dados)


@login_required
def persons_new(request):

    # Verificando se o usuário possui permissão para adicionar novo cliente
    if not request.user.has_perm('clientes.add_person'):
        return HttpResponse('não autorizado')
    elif not request.user.is_superuser:
        return HttpResponse('Não é superusuário')

    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):

    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})

#Mixin deve ser o primeiro a esquerda
class PersonList(LoginRequiredMixin, ListView):
    model = Person

    '''
    Vai mandar a requisição para o home3 sem a necessidade do return
    template_name = 'home3.html'
    '''

    '''
    Se não especificar o template de retorno o Djando entenderá que 
    é person_list.html
    '''

    # Trabalhando com Sessões

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Setando uma variável na sessão
        primeiro_acesso = self.request.session.get('primeiro_acesso', False)    # Se não existir passa False

        if not primeiro_acesso:
            context['mensagem'] = 'Seja bem vindo ao seu primeiro acesso hoje'
            self.request.session['primeiro_acesso'] = True

        else:
            context['mensagem'] = 'Seja bem vindo ao sistema'

        return context

'''
Igual a anterior acima, também é possível injetar o contexto
'''
class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person

    '''É possível injetar contexto'''
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

    # Método herdado subscrito para utilizar o select_related
    def get_object(self, queryset=None):
         pk = self.kwargs.get(self.pk_url_kwarg)
         return Person.objects.select_related('doc').get(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['vendas'] = Venda.objects.filter(
            pessoa=self.object.id
        )
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')

class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person

    # Caso não fosse específicado o template que executaria
    # seria o person_form.html
    template_name_suffix = '_update_form'
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('clientes.deletar_cliente',)

    model = Person

    # É possível a tomada de decisão em get_success_url
    def get_success_url(self):
        return reverse_lazy('person_list_cbv')

# Exemplo utilizando BulkCreate - Caso a lista a ser inserida seja
# grande demais - ex. panilha do excel
class ProdutoBulk(View):
    def get(self, request):
        produtos = ['Banana', 'Maça', 'Limão', 'Pera', 'Melancia', 'Laranja']
        list_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            list_produtos.append(p)

        Produto.objects.bulk_create(list_produtos)

        return HttpResponse('Funcionou')
