from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models


class Cliente(core.models.Log, core.models.PessoaLog):
    cpf = models.BigIntegerField(primary_key=True)

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
    ist_principal = models.BooleanField(default=True, null=True)

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


class Termo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    versao = models.CharField(max_length=50, null=True)
    termo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    descricao = models.TextField(null=True)
    cliente = models.ManyToManyField('cliente.Cliente', through='cliente.ClienteTermo', through_fields=('termo', 'cliente'))

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


class Cartao(core.models.Log):
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cliente_cartao'


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