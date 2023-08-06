# -*- encoding: utf-8 -*-
import sys

from github import GithubException

from suite_py.commands.ask_review import AskReview
from suite_py.lib import logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.youtrack_handler import YoutrackHandler


class OpenPR:
    def __init__(self, project, config, tokens):
        self._project = project
        self._config = config
        self._tokens = tokens
        self._youtrack = YoutrackHandler(config, tokens)
        self._git = GitHandler(project, config)
        self._branch_name = self._git.current_branch_name()
        self._github = GithubHandler(tokens)

    def run(self):
        if not self._git.remote_branch_exists(self._branch_name):
            logger.warning(f"Non ho trovato il branch {self._branch_name} su GitHub")
            if prompt_utils.ask_confirm("Vuoi commitare tutti i file e pusharlo?"):
                self._git.add()
                self._git.commit("Initial commit")
                self._git.push(self._branch_name)
            else:
                logger.error("Per favore esegui un 'git push' manualmente")
                sys.exit(-1)

        pulls = self._github.get_pr_from_branch(self._project, self._branch_name)
        if pulls.totalCount:
            pr = pulls[0]
            logger.info(
                f"Esiste una pull request su GitHub per il branch {self._branch_name}"
            )

            if prompt_utils.ask_confirm(
                "Vuoi modificare la description della pull request?"
            ):
                _edit_pr(pr)
            sys.exit(0)

        youtrack_id = self._get_youtrack_id()

        self._create_pr(youtrack_id)

    def _get_youtrack_id(self):
        youtrack_id = self._youtrack.get_card_from_name(self._branch_name)
        if youtrack_id:
            return youtrack_id

        logger.warning(
            "Non sono riuscito a trovare una issue YouTrack nel nome del branch o la issue indicata non esiste"
        )
        if prompt_utils.ask_confirm("Vuoi collegare la pull request con una issue?"):
            return self._ask_for_card_id()
        return None

    def _ask_for_card_id(self):
        card_id = prompt_utils.ask_questions_input(
            "Inserisci ID della card (ex: PRIMA-1234): "
        )
        if self._youtrack.validate_issue(card_id):
            return card_id
        logger.error("ID non esistente su YouTrack")
        return self._ask_for_card_id()

    def _create_pr(self, youtrack_id):
        if youtrack_id:
            logger.info(
                f"Creo una pull request sul progetto {self._project} per il branch {self._branch_name} collegato con la card {youtrack_id}"
            )
            link = self._youtrack.get_link(youtrack_id)
            title = (
                f"[{youtrack_id}]: {self._youtrack.get_issue(youtrack_id)['summary']}"
            )
        else:
            logger.warning(
                f"Creo una pull request sul progetto {self._project} per il branch {self._branch_name} SENZA collegamenti a YouTrack"
            )
            link = ""
            title = _ask_for_title()

        base_branch = _ask_for_base_branch()
        pr_body = _ask_for_description()

        body = f"{link} \n\n {pr_body}"

        is_draft = prompt_utils.ask_confirm(
            "Vuoi aprire la pull request come draft?", default=False
        )

        try:
            pr = self._github.create_pr(
                self._project, self._branch_name, title, body, base_branch, is_draft
            )
            logger.info(f"Pull request numero {pr.number} creata! {pr.html_url}")
        except GithubException as e:
            logger.error("Errore durante la richiesta a GitHub: ")
            logger.error(e.data["errors"][0])
            sys.exit(-1)

        if youtrack_id:
            self._youtrack.comment(youtrack_id, f"PR {self._project} -> {pr.html_url}")
            logger.info(f"Inserito link della pull request nella card {youtrack_id}")

        if prompt_utils.ask_confirm("Vuoi inserire i reviewers?"):
            AskReview(self._project, self._config, self._tokens).run()


def _edit_pr(pr):
    pr_body = _ask_for_description(pr.body)
    pr.edit(body=pr_body)
    logger.info("Pull request modificata")


def _ask_for_base_branch():
    branch = prompt_utils.ask_questions_input(
        "Inserisci il base branch della pull request: ", "master"
    )
    return branch


def _ask_for_description(pr_body=""):
    input(
        "Inserisci la description della pull request. Premendo invio si aprira l'editor di default"
    )
    description = prompt_utils.ask_questions_editor(
        "Inserisci la description della PR: ", pr_body
    )
    if description == "":
        logger.warning("La descrizione della pull request non può essere vuota")
        return _ask_for_description(pr_body)
    return description


def _ask_for_title():
    title = prompt_utils.ask_questions_input("Inserisci il titolo della pull request: ")
    if title == "":
        logger.warning("Il titolo della pull request non può essere vuoto")
        return _ask_for_title()
    return title
