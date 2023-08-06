from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

import core.models
from django.contrib.auth.models import UserManager, PermissionsMixin, Permission, Group
from compositefk.fields import CompositeForeignKey
from django.utils.translation import gettext_lazy as _

class Profile(AbstractBaseUser, core.models.Log, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    USERNAME_FIELD = 'username'
    is_staff = models.BooleanField(null=True, default=False)

    objects = BaseUserManager()

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    origem_codigo = models.CharField(null=True, max_length=200)
    origem_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    origem = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_origem', to_fields={
        "codigo": "origem_codigo",
        "tipo": "origem_tipo"
    })

    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="%(app_label)s_%(class)s_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_user_set",
        related_query_name="user",
    )

    class Meta(core.models.Log.Meta):
        abstract = True


class Grupo(core.models.Log):
    nivel = models.IntegerField(null=True)
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    grupo_pai = models.ForeignKey('usr.Grupo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_grupo_pai')

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'usr_grupo'


class GrupoUser(core.models.Log):
    grupo = models.ForeignKey('usr.Grupo', on_delete=models.DO_NOTHING, null=True)

    usr_id = models.IntegerField(null=True)
    usr_codigo = models.CharField(null=True, max_length=200)
    usr_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    usr = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_usr', to_fields={
        "codigo": "usr_codigo",
        "tipo": "usr_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'usr_grupouser'

