# -*- coding: utf-8 -*-
import re
import sys

from suite_py.lib import logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.youtrack_handler import YoutrackHandler


class CreateBranch:
    def __init__(self, project, card, config, tokens):
        self._project = project
        self._card = card
        self._config = config
        self._youtrack = YoutrackHandler(config, tokens)
        self._git = GitHandler(project, config)

    def run(self):
        if self._git.is_dirty():
            logger.error("Hai modifiche non committate, non posso continuare")
            sys.exit(-1)

        try:
            if self._card:
                issue = self._youtrack.get_issue(self._card)
            else:
                issue = self._youtrack.get_issue(self._ask_card())
        except Exception:
            logger.error(
                "Si e' verificato un problema recuperando la issue da youtrack. Controlla che il numero della issue e' corretto"
            )
            sys.exit(-1)

        self._checkout_branch(issue)

        self._youtrack.assign_to(issue["id"], "me")

        self._youtrack.update_state(issue["id"], self._config.youtrack["picked_state"])

    def _ask_card(self):
        return prompt_utils.ask_questions_input(
            "Inserisci il numero della issue youtrack:",
            self._config.user["default_slug"],
        )

    def _checkout_branch(self, issue):
        branch_name = prompt_utils.ask_questions_input(
            "Inserisci nome del branch: ",
            re.sub(
                r'([\s\\.,~\^:\(\)\[\]\<\>"\'?]|[^\x00-\x7F]|[0-9])+',
                "-",
                issue["summary"],
            ).lower(),
        )

        default_parent_branch_name = self._git.current_branch_name()

        parent_branch_name = prompt_utils.ask_questions_input(
            "Inserisci branch iniziale: ", default_parent_branch_name
        )

        branch_type = issue["Type"].lower().replace(" ", "-")

        branch_name = f"{issue['id']}/{branch_type}/{branch_name}"

        self._git.checkout(parent_branch_name)

        self._git.checkout(branch_name)
