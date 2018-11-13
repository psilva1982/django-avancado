from django.urls import path

from .views import (
    DashboardView, 
    NovoPedido, 
    NovoItemPedido,
    ListaVendas,
    EditaPedido,
    ExcluiPedido,
    ExcluiItemPedido, 
    EditaItemPedido
)

urlpatterns = [

    path('', ListaVendas.as_view(), name='lista-vendas'),
    path('novo-pedido/', NovoPedido.as_view(), name='novo-pedido'),
    path('edita-pedido/<int:venda>/', EditaPedido.as_view(), name='edita-pedido'),
    path('exclui-pedido/<int:venda>/', ExcluiPedido.as_view(), name='exclui-pedido'),
    path('novo-item-pedido/<int:venda>/', NovoItemPedido.as_view(), name='novo-item-pedido'),
    path('edita-item-pedido/<int:item>/', EditaItemPedido.as_view(), name='edita-item-pedido'),
    path('exclui-item-pedido/<int:item>/', ExcluiItemPedido.as_view(), name='exclui-item-pedido'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
