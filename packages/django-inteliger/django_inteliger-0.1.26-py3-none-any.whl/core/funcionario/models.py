from django.db import models
import core.models
import core.usr.models
# Create your models here.


class FuncionarioLogin(core.usr.models.Profile):
    funcionario = models.OneToOneField('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'funcionario_login'


class Funcionario(core.models.Log, core.models.PessoaLog):
    matricula = models.CharField(max_length=200, primary_key=True)
    cargo = models.ForeignKey('funcionario.Cargo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'funcionario'


class Cargo(core.models.Log):
    nome = models.CharField(max_length=200, primary_key=True)
    cargo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    nm_descritivo = models.CharField(max_length=500, null=True)
    funcao = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cargo'
