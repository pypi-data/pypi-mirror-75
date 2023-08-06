from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models


class Cliente(core.models.Log, core.models.PessoaLog):
    cpf = models.BigIntegerField(primary_key=True)
    imagem = models.FileField(upload_to='fotos/clientes', default='fotos/sem-foto.png', null=True)

    origem_codigo = models.CharField(null=True, max_length=200)
    origem_tipo = models.CharField(null=True, max_length=200, default='CLIENTE.ORIGEM')
    origem = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='cliente_cliente_origem', to_fields={
        "codigo": "origem_codigo",
        "tipo": "origem_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente'


class Endereco(core.models.Log, core.models.EnderecoComplementoLog):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    codigo = models.IntegerField(default=1, null=True)
    is_principal = models.BooleanField(default=True, null=True)

    apelido = models.CharField(max_length=200, null=True)

    origem_codigo = models.CharField(null=True, max_length=200)
    origem_tipo = models.CharField(null=True, max_length=200, default='CLIENTE.ORIGEM')
    origem = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='cliente_endereco_origem', to_fields={
        "codigo": "origem_codigo",
        "tipo": "origem_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        unique_together = ('cliente', 'codigo')
        db_table = 'cliente_endereco'


class Cartao(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    cliente_token = models.CharField(max_length=200, null=True)
    cartao_token = models.CharField(max_length=200, null=True)
    cartao_id = models.CharField(max_length=50, null=True)

    primeiros_6 = models.CharField(max_length=6, null=True)
    ultimos_4 = models.CharField(max_length=4, null=True)

    nm_impresso = models.CharField(max_length=200, null=True)
    cpf_titular_numero = models.CharField(max_length=200, null=True)

    dat_val = models.CharField(max_length=5, null=True)
    mes_val = models.IntegerField(null=True)
    ano_val = models.IntegerField(null=True)

    bandeira = models.ForeignKey('cliente.CartaoBandeira', on_delete=models.DO_NOTHING, null=True)
    is_principal = models.BooleanField(null=True, default=False)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='CLIENTE.CARTAO')
    tipo = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='cliente_cartao', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    adquirente_codigo = models.CharField(null=True, max_length=200)
    adquirente_tipo = models.CharField(null=True, max_length=200, default='CLIENTE.CARTAO.ADQUIRENTE')
    adquirente = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='cliente_cartao_adquirente', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_cartao'


class CartaoBandeira(core.models.Log):
    nome = models.CharField(max_length=50, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    imagem = models.FileField(upload_to="bandeiras", default='bandeiras/sem-imagem.jpg', null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_cartaobandeira'


class CartaoBandeiraParcela(core.models.Log):
    bandeira = models.ForeignKey('cliente.CartaoBandeira', on_delete=models.DO_NOTHING, null=True)
    quantidade = models.IntegerField(default=1, null=True)
    is_juros = models.BooleanField(default=False, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_cartaobandeiraparcela'


class Termo(core.models.Log):
    nome = models.CharField(max_length=200, primary_key=True)
    nome_descritivo = models.CharField(max_length=200, null=True)
    nome_html = models.CharField(max_length=200, null=True)
    versao = models.CharField(max_length=50, null=True)
    termo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    descricao = models.TextField(null=True)
    ordem = models.IntegerField(null=True)

    cliente = models.ManyToManyField('cliente.Cliente', through='cliente.ClienteTermo', through_fields=('termo', 'cliente'))

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='CLIENTE.TERMO')
    tipo = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='cliente_termo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_termo'


class ClienteTermo(core.models.Log):
    termo = models.ForeignKey('cliente.Termo', on_delete=models.DO_NOTHING, null=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_clientetermo'


class Receita(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_receita'


class Avaliacao(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_avaliacao'


class Favorito(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_favorito'


class Cupom(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_cupom'