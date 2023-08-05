from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models
# Create your models here.


class Filial(core.models.Log, core.models.EmpresaLog, core.models.EnderecoComplementoLog):
    cd_filial = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nome_completo = models.CharField(max_length=200, null=True)
    cnpj = models.CharField(max_length=50, null=True)
    telefone = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)

    servicos = models.ManyToManyField('filial.Servico', through='FilialServico', through_fields=('cd_filial', 'servico'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial'


class Servico(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='FILIAL.SERVICO')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='filial_servico_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_servico'


class FilialServico(core.models.Log):
    servico = models.ForeignKey('filial.Servico', on_delete=models.DO_NOTHING, null=True)
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_filialservico'


class FilialHoraFuncionamento(core.models.Log):
    is_padrao = models.BooleanField(null=True, default=True)
    dat_ini_validade = models.DateField(null=True)
    dat_fim_validade = models.DateTimeField(null=True)

    cd_hr_util_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_util_inicio")
    cd_hr_util_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_util_fim")
    cd_hr_sab_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_sab_inicio")
    cd_hr_sab_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_sab_fim")
    cd_hr_dom_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_dom_inicio")
    cd_hr_dom_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_dom_fim")
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_horafuncionamento'
