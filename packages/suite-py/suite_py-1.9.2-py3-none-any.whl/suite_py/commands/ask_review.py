# -*- coding: utf-8 -*-
import readline
import functools
import sys

from suite_py.lib import logger
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.captainhook_handler import CaptainHook


class AskReview:
    def __init__(self, project, config, tokens):
        self._project = project
        self._config = config
        self._youtrack = YoutrackHandler(config, tokens)
        self._captainhook = CaptainHook(config)
        self._git = GitHandler(project, config)
        self._github = GithubHandler(tokens)

    def run(self):
        users = self._maybe_get_users_list()
        pr = self._get_pr()
        youtrack_reviewers = _ask_reviewer(users)
        github_reviewers = _find_github_nicks(youtrack_reviewers, users)
        pr.create_review_request(github_reviewers)
        logger.info("Aggiungo reviewers su GitHub")
        self._maybe_adjust_youtrack_card(pr.title, youtrack_reviewers)

    def _maybe_get_users_list(self):
        try:
            users = self._captainhook.get_users_list().json()
            self._config.put_cache("users", users)
            return users
        except Exception:
            logger.warning(
                "Non riesco ad ottenere la lista degli utenti da captainhook. Utilizzo la versione in cache."
            )
            return self._config.get_cache("users")

    def _get_pr(self):
        branch_name = self._git.current_branch_name()
        pull = self._github.get_pr_from_branch(self._project, branch_name)

        if pull.totalCount:
            pr = pull[0]
            logger.info(
                f"Ho trovato la pull request numero {pr.number} per il branch {branch_name} sul repo {self._project}"
            )
        else:
            logger.error(
                f"Nessuna pull request aperta trovata per il branch {branch_name}"
            )
            sys.exit(-1)

        return pr

    def _maybe_adjust_youtrack_card(self, title, youtrack_reviewers):
        youtrack_id = self._youtrack.get_card_from_name(title)

        if youtrack_id:
            logger.info(
                f"Sposto la card {youtrack_id} in review su youtrack e aggiungo i tag degli utenti"
            )
            self._youtrack.update_state(youtrack_id, "Review")
            for rev in youtrack_reviewers:
                try:
                    self._youtrack.add_tag(youtrack_id, f"review:{rev}")
                except BaseException as e:
                    logger.warning(
                        f"Non sono riuscito ad aggiungere i tag di review: {e}"
                    )
                    sys.exit(-1)
        else:
            logger.warning(
                "Reviewers inseriti SOLO su GitHub. Nessuna card collegata o card nel nome del branch inesistente su YouTrack."
            )


def _ask_reviewer(users):
    u_completer = functools.partial(_completer, users)
    readline.set_completer(u_completer)
    readline.parse_and_bind("tab: complete")

    youtrack_reviewers = []

    youtrack_reviewers = list(
        input(
            "Scegli i reviewers (nome.cognome - separati da spazio - premere TAB per autocomplete) > "
        ).split()
    )

    if not youtrack_reviewers:
        logger.warning("Devi inserire almeno un reviewer")
        return _ask_reviewer(users)

    return youtrack_reviewers


def _completer(users, text, state):
    options = [x["youtrack"] for x in users if text.lower() in x["youtrack"].lower()]
    try:
        return options[state]
    except IndexError:
        return None


def _find_github_nicks(youtrack_reviewers, users):
    github_reviewers = []
    for rev in youtrack_reviewers:
        for user in users:
            if user["youtrack"] == rev:
                github_reviewers.append(user["github"])

    return github_reviewers
