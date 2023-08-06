from django.db import models
import core.models


# Create your models here.
class Fornecedor(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'fornecedor'


class Fabricante(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'fabricante'
