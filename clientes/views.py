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
from .models import Produto
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


class PersonList(ListView):
    model = Person

    '''
    Vai mandar a requisição para o home3 sem a necessidade do return
    template_name = 'home3.html'
    '''

    '''
    Se não especificar o template de retorno o Djando entenderá que 
    é person_list.html
    '''

'''
Igual a anterior acima, também é possível injetar o contexto
'''
class PersonDetail(DetailView):
    model = Person

    '''É possível injetar contexto'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class PersonCreate(CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')

class PersonUpdate(UpdateView):
    model = Person

    # Caso não fosse específicado o template que executaria
    # seria o person_form.html
    template_name_suffix = '_update_form'
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')


class PersonDelete(DeleteView):

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
