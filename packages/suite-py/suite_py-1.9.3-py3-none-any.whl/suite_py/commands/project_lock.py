# -*- coding: utf-8 -*-
import sys
import requests

from suite_py.lib import logger
from suite_py.lib.handler.captainhook_handler import CaptainHook


class ProjectLock:
    def __init__(self, project, env, action, config):
        self._project = project
        self._env = _parse_env(env)
        self._action = action
        self._captainhook = CaptainHook(config)

    def run(self):
        if self._action == "lock":
            try:
                req = self._captainhook.lock_project(self._project, self._env)
                _handle_request(req)
                logger.info(
                    f"Bloccato deploy su {self._env} del progetto {self._project}"
                )
            except requests.exceptions.Timeout:
                logger.warning(
                    "Richiesta a Captainhook in timeout. Prova con suite-py --timeout=60 lock-project lock"
                )
                sys.exit(1)
        elif self._action == "unlock":
            try:
                req = self._captainhook.unlock_project(self._project, self._env)
                _handle_request(req)
                logger.info(
                    f"Abilitato deploy su {self._env} del progetto {self._project}"
                )
            except requests.exceptions.Timeout:
                logger.warning(
                    "Richiesta a Captainhook in timeout. Prova con suite-py --timeout=60 lock-project unlock"
                )
                sys.exit(1)
        else:
            logger.warning("Non ho capito che cosa devo fare")
            sys.exit(-1)


def _handle_request(request):
    if request.status_code != 200:
        logger.error(
            "Qualcosa è andato storto durante la richiesta. Richiedi supporto ai devops su slack."
        )
        sys.exit(-1)

    return True


def _parse_env(env):
    # implementare uno switch era troppo noioso
    if env == "deploy":
        return "production"
    if env == "merge":
        return "staging"
    return env
