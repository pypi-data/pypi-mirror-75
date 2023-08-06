from django.urls import re_path, include
from core.views import InteligerView

urlpatterns = [
    re_path(r'cliente/', include(('core.cliente.urls', 'core.cliente'), namespace='cliente')),
    re_path(r'filial/', include(('core.filial.urls', 'core.filial'), namespace='filial')),
    re_path(r'fornecedor/', include(('core.fornecedor.urls', 'core.fornecedor'), namespace='fornecedor')),
    re_path(r'funcionario/', include(('core.funcionario.urls', 'core.funcionario'), namespace='funcionario')),
    re_path(r'log/', include(('core.log.urls', 'core.log'), namespace='log')),
    re_path(r'produto/', include(('core.produto.urls', 'core.produto'), namespace='produto')),
    re_path(r'sistema/', include(('core.sistema.urls', 'core.sistema'), namespace='sistema')),
    re_path(r'usr/', include(('core.usr.urls', 'core.usr'), namespace='usr')),

    re_path(r'atualizar$', InteligerView.as_view(), name='sistema_atualizar'),
]
