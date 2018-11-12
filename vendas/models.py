from django.db import models
from django.db.models import Sum, F, FloatField, Max
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from clientes.models import Person
from produtos.models import Produto

from .managers import VendaManager

# Create your models here.
class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    nfe_emitida = models.BooleanField(default=False)

    objects = VendaManager()

    class Meta:
        permissions = (
            ('setar_nfe', 'Usuário pode alterar o parametro da NF-e'),
            ('ver_dashboard', 'Pode visualizar o dashboard'),
            ('permissao3', 'Permissão 3'),
        )

    def get_total(self):
        tot = self.itempedido_set.all().aggregate(
            tot_ped=Sum((F('qtde') * F('produto__preco')) - F('desconto'), output_field=FloatField())
        )['tot_ped'] or 0

        tot = tot - float(self.desconto) - float(self.impostos)
        self.valor = tot
        Venda.objects.filter(id=self.id).update(valor=tot)


    def __str__(self):
        return self.numero

class ItemPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.FloatField(default=0.0, null=False, blank=False)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.produto.descricao


# Signal para itens da venda
@receiver(post_save, sender=ItemPedido)
def update_total_itens_venda(sender, instance, **kwargs):
    instance.venda.get_total()

# Signal para o cabeçalho da venda
@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance, **kwargs):
    instance.get_total()

