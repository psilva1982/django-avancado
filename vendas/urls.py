from django.urls import path
#from .views import persons_list

from .views import DashboardView, NovoPedido

urlpatterns = [

    #path('list/', persons_list, name="person_list"),
    path('novo-pedido/', NovoPedido.as_view(), name='novo-pedido'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
