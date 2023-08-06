from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models


# Create your models here.
class Modulo(core.models.Log):
    nome = models.SlugField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    modulo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_modulo'


class Versao(core.models.Log):
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    dat_atualizacao = models.DateField(null=True)
    codigo = models.CharField(max_length=100, null=True)
    commit = models.CharField(max_length=50, null=True)
    descricao = models.TextField(null=True)

    responsavel_id = models.IntegerField(null=True)
    responsavel_codigo = models.CharField(null=True, max_length=200)
    responsavel_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    responsavel = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_responsavel', to_fields={
        "codigo": "responsavel_codigo",
        "tipo": "responsavel_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_versao'


class VersaoItem(core.models.Log):
    versao = models.ForeignKey('sistema.Versao', null=True, on_delete=models.DO_NOTHING)
    ordem = models.IntegerField(null=True)
    descricao = models.TextField(null=True)

    responsavel_id = models.IntegerField(null=True)
    responsavel_codigo = models.CharField(null=True, max_length=200)
    responsavel_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    responsavel = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_responsavel', to_fields={
        "codigo": "responsavel_codigo",
        "tipo": "responsavel_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_versaoitem'


class PontoFuncao(core.models.Log):
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    acao = models.CharField(max_length=100, primary_key=True)
    codigo = models.IntegerField(null=True)

    versao = models.CharField(max_length=10, null=True)
    descricao = models.CharField(max_length=500, null=True)

    lugares = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_pontofuncao'


class Perfil(core.models.Log):
    nivel = models.IntegerField(null=True)
    is_login = models.BooleanField(null=True)
    is_staff = models.BooleanField(default=False)
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    pontofuncao = models.ManyToManyField('sistema.PontoFuncao', through='sistema.PerfilPontoFuncao', through_fields=('perfil', 'pontofuncao'))

    grupo = models.ManyToManyField('usr.Grupo', through='sistema.PerfilGrupo', through_fields=('perfil', 'grupo'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_grupo'


class PerfilPontoFuncao(core.models.Log):
    pontofuncao = models.ForeignKey('sistema.PontoFuncao', on_delete=models.DO_NOTHING, null=True)
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_grupopontofuncao'


class PerfilLogin(core.models.Log):
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING)
    view_inicial = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfillogin'


class PerfilGrupo(core.models.Log):
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING, null=True)
    grupo = models.ForeignKey('usr.Grupo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfilgrupo'
