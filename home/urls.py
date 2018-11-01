from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    home,
    my_logout,
    HomePageView,
    MyView,
)

urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),

    # Não há necessidade de declarar uma view - Serve apenas para servir conteúdo html
    path('home2/', TemplateView.as_view(template_name='home2.html')),

    # Se quiser ler / injetar contexto é necessário criar sua própria view
    path('home3/', HomePageView.as_view(template_name='home3.html')),

    path('home3/', HomePageView.as_view(template_name='home3.html')),

    path('view/', MyView.as_view()),
]