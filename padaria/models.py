from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager #AbstractBaseUser - bem básico
from stdimage.models import StdImageField
from django.utils.safestring import mark_safe
import uuid

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    name = filename.split('.')[0]
    codigo = uuid.uuid1()
    codigo = str(codigo).split('-')[0]
    filename = f'{name}-{codigo}.{ext}'
    return filename

class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)

class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    rua = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=14)
    celular = models.CharField(max_length=14) 
    dataNascimento = models.DateField()
    is_staff = models.BooleanField('Membro da equipe', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf', 'estado', 'cidade', 'rua', 'numero', 'cep', 'celular','dataNascimento']

    def __str__(self):
        return self.email

    objects = UsuarioManager()

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    sabor = models.CharField(max_length=100, blank=True, null=True)
    tamanho = models.CharField(max_length=7, blank=True, null=True)
    descricao = models.TextField()
    precoUnitario = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})

    def image_tag(self): # new
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.imagem))

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    PAGAMENTO_CHOICES = (
        ('dinheiro', 'Dinheiro'),
        ('cartao-credito', 'Crédito'),
        ('cartao-debito', 'Débito')
    )
    STATUS_CHOICES = (
        ('preparando', 'Preparando'),
        ('concluido', 'Concluído'),
        ('entrega', 'Em Trânsito'),
    )
    codigo = models.CharField('Código', max_length=20)
    pagamento = models.CharField('Pagamento', max_length=20, choices=PAGAMENTO_CHOICES, default=PAGAMENTO_CHOICES[0][0])
    statusPedido = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    valorPedido = models.DecimalField('Valor Total', max_digits=6, decimal_places=2)
    dataCriacao = models.DateTimeField('Criação', auto_now_add=True)
    dataAtualizacao = models.DateTimeField('Atualização', auto_now=True)
    produtos = models.ManyToManyField(Produto, through='ItensPedido')
    user = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class ItensPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    codigo = models.CharField('Código', max_length=20)
    valorPedido = models.DecimalField('Valor Total', max_digits=6, decimal_places=2)
    valorProduto = models.DecimalField('Valor Produto', max_digits=6, decimal_places=2)
    dataCriacao = models.DateTimeField('Criação', auto_now_add=True)
    dataAtualizacao = models.DateTimeField('Atualização', auto_now=True)
    quantidadeProduto = models.IntegerField('Quantidade Produto')

    class Meta:
        verbose_name = 'Items Pedido'
        verbose_name_plural = 'Items Pedido'

    def __str__(self):
        return "{}_{}".format(self.pedido.__str__(), self.produto.__str__())