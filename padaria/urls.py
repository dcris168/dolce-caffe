from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cadastroCliente, login_user, fazer_pedido, index, meus_pedidos, detalhes_pedido

urlpatterns = [
    path('', index, name='index'),
    path('cadastro/', cadastroCliente, name='cadastro'),
    path('login/', login_user, name='login'),
    path('fazer/pedido/', fazer_pedido, name='fazer_pedido'),
    path('meuspedidos/<int:user_id>', meus_pedidos, name='meus_pedidos'),
    path('pedido/<str:pedido_codigo>', detalhes_pedido, name='detalhes_pedido'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]