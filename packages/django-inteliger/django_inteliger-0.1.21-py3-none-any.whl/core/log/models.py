from django.db import models
import core.models


class Log(core.models.Log):
    status_code = models.IntegerField(null=True)
    reason_phrase = models.CharField(max_length=500, null=True)
    metodo = models.CharField(max_length=30, null=True)
    ip = models.GenericIPAddressField(null=True)
    path = models.CharField(max_length=500, null=True)
    session_key = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True)

    info_user = models.TextField(null=True)
    info_user_navegador_familia = models.CharField(max_length=200, null=True)
    info_user_navegador_versao = models.CharField(max_length=50, null=True)
    info_user_aparelho_familia = models.CharField(max_length=200, null=True)
    info_user_aparelho_modelo = models.CharField(max_length=200, null=True)
    info_user_os_familia = models.CharField(max_length=200, null=True)
    info_user_os_versao = models.CharField(max_length=50, null=True)

    info_user_is_bot = models.BooleanField(null=True)
    info_user_is_email_client = models.BooleanField(null=True)
    info_user_is_mobile = models.BooleanField(null=True)
    info_user_is_pc = models.BooleanField(null=True)
    info_user_is_tablet = models.BooleanField(null=True)
    info_user_is_touch_capable = models.BooleanField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class Query(core.models.Log):
    time = models.FloatField(null=True)
    query = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class Erro(core.models.Log):
    erro = models.ForeignKey('core.Erro', on_delete=models.DO_NOTHING, null=True)
    tipo = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class ClienteLog(Log):
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_log"'


class ClienteQuery(Query):
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_query"'


class ClienteErro(Erro):
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_erro"'


class IndicadorLog(Log):
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_log"'


class IndicadorQuery(Query):
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_query"'


class IndicadorErro(Erro):
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_erro"'


class FornecedorLog(Log):
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_log"'


class FornecedorQuery(Query):
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_query"'


class FornecedorErro(Erro):
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_erro"'


class Venda_maisLog(Log):
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_log"'


class Venda_maisQuery(Query):
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_query"'


class Venda_maisErro(Erro):
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_erro"'


class ProcessosLog(Log):
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"processos_log"'


class ProcessosQuery(Query):
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"processos_query"'


class ProcessosErro(Erro):
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"processos_erro"'
