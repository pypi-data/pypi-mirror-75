from __future__ import annotations

from compositefk.fields import CompositeForeignKey
from django.db import models
from django.utils import timezone
import time

from core.util.core import Inteliger
from django.apps import apps


class InteligerQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(status=True)

    def desabilitar(self, request_=None):
        usuario = request_.user.id if request_ is not None else None
        qs = self.update(status=False, usr_delete=usuario, dat_delete=timezone.now())
        return qs


class InteligerManager(models.Manager):
    def get_queryset(self):
        ini = time.time()
        qs = InteligerQuerySet(self.model)
        fim = time.time()
        tempo = Inteliger().tempo_pesquisa
        if 0 < tempo < fim - ini:
            Query = apps.get_model('log', 'Query')
            Query(
                time=fim - ini,
                query=str(qs.query)
            ).save()

        return qs

    def ativos(self):
        return self.get_queryset().ativos()

    def desabilitar(self, request_=None):
        return self.get_queryset().desabilitar(request_=request_)


class DatLog(models.Model):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True)
    dat_delete = models.DateTimeField(null=True)

    class Meta:
        managed = False
        abstract = True


class UsrLog(models.Model):
    usr_insercao = models.IntegerField(null=True)
    usr_edicao = models.IntegerField(null=True)
    usr_delete = models.IntegerField(null=True)
    # trocar por inteiro
    origem_insercao_codigo = models.CharField(null=True, max_length=200)
    origem_insercao_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    origem_insercao = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_origem_insercao', to_fields={
        "codigo": "origem_insercao_codigo",
        "tipo": "origem_insercao_tipo"
    })

    origem_edicao_codigo = models.CharField(null=True, max_length=200)
    origem_edicao_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    origem_edicao = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_origem_edicao', to_fields={
        "codigo": "origem_edicao_codigo",
        "tipo": "origem_edicao_tipo"
    })

    origem_delete_codigo = models.CharField(null=True, max_length=200)
    origem_delete_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    origem_delete = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_origem_delete', to_fields={
        "codigo": "origem_delete_codigo",
        "tipo": "origem_delete_tipo"
    })

    class Meta:
        managed = False
        abstract = True


class Log(DatLog, UsrLog):
    normal_objects = models.Manager()
    objects = InteligerManager()

    status = models.BooleanField(null=True, default=True)

    class Meta:
        managed = True
        abstract = True

    def save(self, request_=None, *args, **kwargs):
        if request_ is not None:
            if self.pk is None:
                self.usr_insercao = request_.user.id if request_ is not None else None
                self.dat_insercao = timezone.now()
                self.origem_insercao_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.id is not None else None
                self.status = True
            else:
                self.usr_edicao = request_.user.id if request_ is not None else None
                self.dat_edicao = timezone.now()
                self.origem_codigo_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.id is not None else None
        super(Log, self).save(*args, **kwargs)

    def desabilitar(self, request_=None, *args, **kwargs):
        self.status = False
        self.usr_delete_id = request_.user.id if request_ is not None else None
        self.dat_delete = timezone.now()
        self.origem_delete_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.id is not None else None
        super(Log, self).save(*args, **kwargs)


class EmpresaLog(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.DO_NOTHING, null=True)

    class Meta(Log.Meta):
        abstract = True


class ContatoLog(models.Model):
    celular_numero = models.CharField(max_length=50, null=True)
    celular_ddd = models.CharField(max_length=3, null=True)
    celular_completo = models.CharField(max_length=50, null=True)
    celular_completo_form = models.CharField(max_length=50, null=True)

    telefone_numero = models.CharField(max_length=50, null=True)
    telefone_ddd = models.CharField(max_length=3, null=True)
    telefone_completo = models.CharField(max_length=50, null=True)
    telefone_completo_form = models.CharField(max_length=50, null=True)

    email = models.EmailField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = True


class PessoaLog(ContatoLog):
    nm_completo = models.CharField(max_length=200, null=True)
    nm_primeiro = models.CharField(max_length=200, null=True)
    nm_ultimo = models.CharField(max_length=200, null=True)

    cpf = models.BigIntegerField(null=True)
    cpf_form = models.CharField(max_length=20, unique=True)

    rg = models.CharField(max_length=15, null=True)

    dat_nasc = models.DateField(null=True)

    nm_mae = models.CharField(max_length=200, null=True)
    nm_pai = models.CharField(max_length=200, null=True)

    sexo_codigo = models.CharField(null=True, max_length=200)
    sexo_tipo = models.CharField(null=True, max_length=200, default='PESSOA.SEXO')
    sexo = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_sexo', to_fields={
        "codigo": "sexo_codigo",
        "tipo": "sexo_tipo"
    })

    educacao_codigo = models.CharField(null=True, max_length=200)
    educacao_tipo = models.CharField(null=True, max_length=200, default='PESSOA.EDUCACAO')
    educacao = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_educacao', to_fields={
        "codigo": "educacao_codigo",
        "tipo": "educacao_tipo"
    })

    ocupacao_codigo = models.CharField(null=True, max_length=200)
    ocupacao_tipo = models.CharField(null=True, max_length=200, default='PESSOA.OCUPACAO')
    ocupacao = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_ocupacao', to_fields={
        "codigo": "ocupacao_codigo",
        "tipo": "ocupacao_tipo"
    })

    estado_civil_codigo = models.CharField(null=True, max_length=200)
    estado_civil_tipo = models.CharField(null=True, max_length=200, default='PESSOA.ESTADO_CIVIL')
    estado_civil = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_estado_civil', to_fields={
        "codigo": "estado_civil_codigo",
        "tipo": "estado_civil_tipo"
    })

    class Meta(Log.Meta):
        abstract = True


class EnderecoLog(models.Model):
    cep = models.CharField(max_length=10, null=True)
    cep_form = models.CharField(max_length=15, null=True)
    municipio = models.ForeignKey('core.Municipio', on_delete=models.DO_NOTHING, null=True)
    bairro_cep = models.CharField(max_length=100, null=True)
    endereco_cep = models.CharField(max_length=100, null=True)
    endereco_comp_cep = models.CharField(max_length=200, null=True)
    latitude_cep = models.CharField(max_length=200, null=True)
    longitude_cep = models.CharField(max_length=200, null=True)
    tipo_cep = models.CharField(max_length=200, null=True)


    class Meta(Log.Meta):
        abstract = True


class EnderecoComplementoLog(models.Model):
    cep = models.ForeignKey('core.Cep', null=True, on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=30, null=True)
    complemento = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100, null=True)
    endereco = models.CharField(max_length=100, null=True)

    ponto_referencia = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=200, null=True)
    longitude = models.CharField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = True


class Tipo(Log):
    codigo = models.IntegerField(null=True)
    tipo = models.CharField(max_length=200, null=True)
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'tipo'
        unique_together = ('codigo', 'tipo')


class Empresa(Log):
    nome = models.CharField(max_length=100, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'empresa'


class Erro(Log):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'erro'


class Data(Log):
    anomesdia = models.IntegerField(primary_key=True)
    anomes = models.IntegerField(null=True)
    ano = models.IntegerField(null=True)

    dat_dia = models.DateTimeField(null=True)

    nr_mes = models.IntegerField(null=True)
    ds_mes = models.CharField(max_length=50, null=True)
    ds_mes_abreviado = models.CharField(max_length=3, null=True)

    nr_dia = models.IntegerField(null=True)
    ds_dia_semana = models.CharField(max_length=50, null=True)

    nr_semana_ano = models.IntegerField(null=True)
    ds_semana_ano = models.CharField(max_length=50, null=True)

    nr_semana_mes = models.IntegerField(null=True)
    ds_semana_mes = models.CharField(max_length=50, null=True)

    nr_bimestre_ano = models.IntegerField(null=True)
    ds_bimestre_ano = models.CharField(max_length=50, null=True)

    nr_trimestre_ano = models.IntegerField(null=True)
    ds_trimestre_ano = models.CharField(max_length=50, null=True)

    nr_quadrimestre_ano = models.IntegerField(null=True)
    ds_quadrimestre_ano = models.CharField(max_length=50, null=True)

    nr_semestre_ano = models.IntegerField(null=True)
    ds_semestre_ano = models.CharField(max_length=50, null=True)

    nr_primeiro_dia_anomes = models.IntegerField(null=True)

    is_ultimo_dia_mes = models.BooleanField(null=True)
    ds_feriado_nacional = models.CharField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'data'


class Hora(Log):
    descricao = models.CharField(max_length=200, null=True)
    hora = models.IntegerField(null=True)
    minuto = models.IntegerField(null=True)
    hora_minuto = models.TimeField(null=True)
    cd_hora_minuto = models.IntegerField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'hora'


class UF(Log):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nm_abrev = models.CharField(max_length=2, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'uf'


class Municipio(Log):
    uf = models.ForeignKey('core.UF', on_delete=models.DO_NOTHING, null=True)
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'municipio'


class Cep(Log, EnderecoLog):
    cep = models.CharField(max_length=10, primary_key=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'cep'