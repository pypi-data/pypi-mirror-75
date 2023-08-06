from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models


# Create your models here.
class Produto(core.models.Log):
    cd_produto = models.IntegerField(primary_key=True)
    cd_externo = models.IntegerField(null=True)

    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    marca = models.ForeignKey('produto.Marca', on_delete=models.DO_NOTHING, related_name='marca', null=True)
    tipo_produto = models.ForeignKey('produto.Tipo', on_delete=models.DO_NOTHING, null=True)
    fabricante = models.ForeignKey('fornecedor.Fabricante', on_delete=models.DO_NOTHING, null=True)

    imagem = models.FileField(upload_to="produtos", default='produtos/caixa-nissei.jpg', null=True)

    produto_pai = models.ForeignKey('self', models.DO_NOTHING, null=True)

    is_ecommerce = models.BooleanField(default=True, null=True)
    nm_url_ecommerce = models.SlugField(max_length=200, null=True)
    nm_ecommerce = models.CharField(max_length=200, null=True)
    descricao_ecommerce = models.TextField(null=True)
    altura_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    largura_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    profundidade_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    peso_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    qtd_min_venda_ecommerce = models.IntegerField(null=True, default=1)
    qtd_max_venda_ecommerce = models.IntegerField(null=True)

    is_retencao_receita = models.BooleanField(default=False, null=True)
    is_venda_controlada = models.BooleanField(default=False, null=True)
    is_pbm = models.BooleanField(default=False, null=True)

    categoria_principal = models.ForeignKey('produto.Categoria', on_delete=models.DO_NOTHING, null=True, related_name='categoria_principal')

    grupo = models.ManyToManyField('produto.Grupo', through='produto.ProdutoGrupo', through_fields=('produto', 'grupo'))
    categoria = models.ManyToManyField('produto.Categoria', through='produto.ProdutoCategoria', through_fields=('produto', 'categoria'))
    kit = models.ManyToManyField('produto.Kit', through='produto.ProdutoKit', through_fields=('produto', 'kit'))
    bula = models.ManyToManyField('produto.Bula', through='produto.ProdutoBula', through_fields=('produto', 'bula'))
    tipo_receita = models.ManyToManyField('produto.TipoReceita', through='produto.ProdutoTipoReceita', through_fields=('produto', 'tipo_receita'))
    principio_ativo = models.ManyToManyField('produto.PrincipioAtivo', through='produto.ProdutoPrincipioAtivo', through_fields=('produto', 'principio_ativo'))
    especialidade = models.ManyToManyField('produto.Especialidade', through='produto.ProdutoEspecialidade', through_fields=('produto', 'especialidade'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto'


class Tipo(core.models.Log):
    nome = models.CharField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tipo'


class Marca(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)
    nm_ecommerce = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_marca'


class ProdutoImagem(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    imagem = models.FileField(upload_to="produtos", default='produtos/caixa-nissei.jpg', null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_imagem'


class Grupo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_grupo'


class ProdutoGrupo(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    grupo = models.ForeignKey('produto.Grupo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtogrupo'


class Categoria(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    categoria_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_categoria'


class ProdutoCategoria(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    categoria = models.ForeignKey('produto.Categoria', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtocategoria'


class Kit(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_kit'


class ProdutoKit(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    kit = models.ForeignKey('produto.Kit', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtokit'


class Bula(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_bula'


class ProdutoBula(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    bula = models.ForeignKey('produto.Bula', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtobula'


class TipoReceita(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tiporeceita'


class ProdutoTipoReceita(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    tipo_receita = models.ForeignKey('produto.TipoReceita', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtotiporeceita'


class PrincipioAtivo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_principioativo'


class ProdutoPrincipioAtivo(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    principio_ativo = models.ForeignKey('produto.PrincipioAtivo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoprincipioativo'


class Especialidade(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_especialidade'


class ProdutoEspecialidade(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    especialidade = models.ForeignKey('produto.Especialidade', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoespecialidade'


class ProdutoEan(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    ean = models.CharField(max_length=50, primary_key=True)
    is_principal = models.BooleanField(default=True, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_ean'


class PrecoLista(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    dat_ini = models.DateField(null=True)
    dat_fim = models.DateField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'preco_lista'


class ProdutoPreco(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    precolista = models.ForeignKey('produto.PrecoLista', on_delete=models.DO_NOTHING, null=True)
    desconto = models.ManyToManyField('produto.Desconto', through='produto.DescontoProdutoPreco', through_fields=('produtopreco', 'desconto'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_preco'


class TipoDesconto(core.models.Log):
    nome = models.CharField(max_length=100, primary_key=True)
    descricao = models.CharField(max_length=200, null=True)
    tipo = models.CharField(max_length=10, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tipodesconto'


class Desconto(core.models.Log):
    tipo = models.ForeignKey('produto.TipoDesconto', on_delete=models.DO_NOTHING, null=True)
    qtd_ini_desc = models.IntegerField(null=True)
    qtd_fim_desc = models.IntegerField(null=True)
    valor_desc = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    per_desc = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dat_ini = models.DateField(null=True)
    dat_fim = models.DateField(null=True)

    prioridade = models.IntegerField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_desconto'


class DescontoProdutoPreco(core.models.Log):
    desconto = models.ForeignKey('produto.Desconto', on_delete=models.DO_NOTHING, null=True)
    produtopreco = models.ForeignKey('produto.ProdutoPreco', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_descontoprodutopreco'


class Estoque(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    quantidade = models.IntegerField(null=True)
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_estoque'