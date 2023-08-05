from __future__ import annotations

from typing import Optional

from django.apps import apps
try:
    from base.settings import DATABASES
except:
    DATABASES = {}


class InteligerMeta(type):
    _instance: Optional[Inteliger] = None

    def __call__(self) -> Inteliger:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Inteliger(metaclass=InteligerMeta):
    def __init__(self):
        self.__tempo_pesquisa = 0
        self.atualizar_tempo_query()

    def salvar_log(self, request=None, response=None):
        try:
            if request.META.get('REMOTE_ADDR') != '127.0.0.1':
                db = DATABASES['default']['USER'].capitalize()
                log = apps.get_model('log', db + 'Log')
                log(
                    status_code=response.status_code,
                    reason_phrase=response.reason_phrase,
                    metodo=request.method,
                    ip=request.META.get('REMOTE_ADDR'),
                    path=request.path,
                    session_key=request.session.session_key,
                    body=str(request.body) if not request.POST.get('password') else '',
                    info_user=str(request.user_agent),
                    info_user_navegador_familia=request.user_agent.browser.family,
                    info_user_navegador_versao=request.user_agent.browser.version_string,
                    info_user_aparelho_familia=request.user_agent.device.family,
                    info_user_aparelho_modelo=request.user_agent.device.model,
                    info_user_os_familia=request.user_agent.os.family,
                    info_user_os_versao=request.user_agent.os.version_string,
                    info_user_is_bot=request.user_agent.is_bot,
                    info_user_is_email_client=request.user_agent.is_email_client,
                    info_user_is_mobile=request.user_agent.is_mobile,
                    info_user_is_pc=request.user_agent.is_pc,
                    info_user_is_tablet=request.user_agent.is_tablet,
                    info_user_is_touch_capable=request.user_agent.is_touch_capable,
                ).save(request_=request)
        except:
            pass

    def atualizar_tempo_query(self):
        tipo = apps.get_model('core', 'Tipo')
        tempo = tipo.normal_objects.values('nome').filter(tipo='SISTEMA.TEMPO_QUERY', status=True).order_by('-dat_insercao').first()
        try:
            self.tempo_pesquisa = int(tempo['nome']) if tempo is not None else 0
        except:
            pass

    @property
    def tempo_pesquisa(self):
        return self.__tempo_pesquisa

    @tempo_pesquisa.setter
    def tempo_pesquisa(self, value):
        self.__tempo_pesquisa = value

    @tempo_pesquisa.deleter
    def tempo_pesquisa(self):
        del self.__tempo_pesquisa
