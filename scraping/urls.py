#Endpoints da API por estado
from django.urls import path
from . import views

urlpatterns = [
    path('ceara/', views.CearaView.as_view(), name='ceara'),
    path('pa/', views.PaView.as_view(), name='pa'),
    path('pe/', views.PeView.as_view(), name='pe'),
]