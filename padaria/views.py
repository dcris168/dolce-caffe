from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView, View, FormView
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import *
import uuid
from django.contrib.auth.decorators import login_required

def index(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'index.html', context)

def cadastroCliente(request): 
    if request.method == "POST":
        form = CustomUsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro Realizado com Sucesso')
            return redirect('login')
        else:
            messages.error(request, 'Tivemos algum problema')
    else:
        form = CustomUsuarioCreateForm()
    context = {
        'form': form
    }
    return render(request, 'cadastro_cliente.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Usuário ou Senha errados')
            return redirect('login')
    return render(request, 'login.html')

@login_required
def fazer_pedido(request):
    produtos = Produto.objects.all()
    if request.method == "POST":
        prods = []
        total = 0
        user = request.POST.get('user', False)
        user = CustomUsuario.objects.get(id=user)
        pagamento = request.POST.get('pagamento', False)
        codigo = uuid.uuid1()
        codigo = str(codigo).split('-')[0]
        for p in produtos:
            qnt = int(request.POST.get(p.sabor, False))
            if qnt > 0:
                prods.append([p.id, p.precoUnitario, qnt])
                total += (p.precoUnitario * qnt)
        lista = []
        pedido = Pedido.objects.create(codigo=codigo, pagamento=pagamento, statusPedido='separando', valorPedido=total, user=user)
        for p in prods:
            produto = Produto.objects.get(id=p[0])
            lista.append(produto)
            ItensPedido.objects.create(codigo=codigo, valorProduto=produto.precoUnitario, quantidadeProduto=p[-1], valorPedido=total, produto=produto, pedido=pedido)
        pedido.produtos.add(produto)
        messages.success(request, 'Pedido realizado com sucesso')
    
    context = {
        'produtos': produtos
    }
    return render(request, 'fazer_pedido.html', context)

@login_required
def meus_pedidos(request, user_id): 

    user = CustomUsuario.objects.get(id=user_id)

    pedidos = Pedido.objects.filter(user=user).order_by('-dataCriacao').values()

    context = {
        'user': user,
        'pedidos': pedidos
    }
    return render(request, 'meus_pedidos.html', context)

@login_required
def detalhes_pedido(request, pedido_codigo):

    pedido = Pedido.objects.get(codigo=pedido_codigo)
    codigo = pedido_codigo
    produtos = ItensPedido.objects.filter(pedido=pedido.id)

    context = {
        'pedido': pedido,
        'codigo': codigo,
        'produtos': produtos
    }
    return render(request, 'detalhes_pedido.html', context)