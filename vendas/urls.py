from django.urls import path
#from .views import persons_list

from .views import DashboardView

urlpatterns = [

    #path('list/', persons_list, name="person_list"),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
