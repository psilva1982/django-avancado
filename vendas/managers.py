from django.db import models

from django.db.models import Sum, F, FloatField, Max, Min, Avg, Count


class VendaManager(models.Manager):

    def media(self):
        return self.all().aggregate(Avg('valor'))['valor__avg']

    def media_desconto(self):
        return self.all().aggregate(Avg('desconto'))['desconto__avg']

    def min(self):
        return self.all().aggregate(Min('valor'))['valor__min']

    def max(self):
        return self.all().aggregate(Max('valor'))['valor__max']

    def n_pedidos(self):
        return self.all().aggregate(Count('id'))['id__count']

    def notas_emitidas(self):
        return self.filter(nfe_emitida=True).aggregate(Count('id'))['id__count']
