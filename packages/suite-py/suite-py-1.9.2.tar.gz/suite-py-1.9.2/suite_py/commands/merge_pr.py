# -*- coding: utf-8 -*-
import sys

from halo import Halo

from suite_py.lib import logger
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler.drone_handler import DroneHandler
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.qainit import qainit_shutdown
from suite_py.lib.symbol import CHECKMARK, CROSSMARK


class MergePR:
    def __init__(self, project, config, tokens):
        self._project = project
        self._config = config
        self._youtrack = YoutrackHandler(config, tokens)
        self._captainhook = CaptainHook(config)
        self._git = GitHandler(project, config)
        self._github = GithubHandler(tokens)
        self._drone = DroneHandler(config, tokens, repo=project)

    def run(self):
        self._stop_if_master_locked()

        pr = self._select_pr()

        print(f"\nHai selezionato: \n{self._check_pr_status(pr)}")
        if not prompt_utils.ask_confirm("Vuoi continuare il merge?", default=False):
            sys.exit()

        branch_name = pr.head.ref
        youtrack_id = self._youtrack.get_card_from_name(branch_name)

        _check_migrations_merge(pr)

        logger.info("Eseguo il merge...")

        merge_status = pr.merge(
            commit_title=f"{pr.title} (#{pr.number})",
            commit_message="",
            merge_method="squash",
        )

        if not merge_status.merged:
            logger.error("Si è verificato un errore durante il merge.")
            sys.exit(-1)

        drone_build_number = self._drone.get_pr_build_number(merge_status.sha)
        drone_build_url = self._drone.get_build_url(drone_build_number)

        if drone_build_url:
            logger.info(
                f"Pull request mergiata su master! Puoi seguire lo stato della build su {drone_build_url}"
            )
        else:
            logger.info("Pull request mergiata su master!")

        self._git.fetch()
        if self._git.remote_branch_exists(branch_name):
            self._git.delete_remote_branch(branch_name)

        if prompt_utils.ask_confirm(
            "Vuoi bloccare staging? (Necessario se bisogna testare su staging)",
            default=False,
        ):
            if self._drone.prestart_success(drone_build_number):
                self._captainhook.lock_project(self._project, "staging")
            else:
                logger.error(
                    "Problemi con la build su drone, non riesco a bloccare staging"
                )
                sys.exit(-1)

        if youtrack_id:
            logger.info("Aggiorno lo stato della card su youtrack...")
            self._youtrack.update_state(
                youtrack_id, self._config.youtrack["merged_state"]
            )
            logger.info("Card aggiornata")

            logger.info("Spengo il qa, se esiste")
            qainit_shutdown(youtrack_id, self._config)
        else:
            logger.warning(
                "Non sono riuscito a trovare una issue YouTrack nel nome del branch o la issue indicata non esiste."
            )
            logger.warning(
                "Nessuna card aggiornata su YouTrack e nessun QA spento in automatico"
            )

        logger.info("Tutto fatto!")
        sys.exit()

    def _select_pr(self):
        if self._github.user_is_admin(self._project):
            logger.warning(
                "Sei admin del repository, puoi fare il merge skippando i check (CI, review, ecc...)\nDa grandi poteri derivano grandi responsabilita'"
            )

        with Halo(text="Loading pull requests...", spinner="dots", color="magenta"):
            choices = [
                {"name": pr.title, "value": pr}
                for pr in self._github.get_list_pr(self._project)
            ]
        if choices:
            choices.sort(key=lambda x: x["name"])
            return prompt_utils.ask_choices("Seleziona PR: ", choices)

        logger.error(
            f"Non esistono pull request pronte per il merge o potresti non avere i permessi, per favore controlla su https://github.com/primait/{self._project}/pulls"
        )
        sys.exit(-1)

    def _stop_if_master_locked(self):
        request = self._captainhook.status(self._project, "staging")

        if request.status_code != 200:
            logger.error("Impossibile determinare lo stato del lock su master.")
            sys.exit(-1)

        request_object = request.json()
        if request_object["locked"]:
            logger.error(
                f"Il progetto è lockato su staging da {request_object['by']}. Impossibile continuare."
            )
            sys.exit(-1)

    def _check_pr_status(self, pr):
        build_status = CHECKMARK
        reviews = CHECKMARK
        print(pr.mergeable_state)
        if pr.mergeable_state == "dirty":
            logger.error(
                "La pull request selezionata non è mergeable. Controlla se ci sono conflitti."
            )
            sys.exit(-1)
        if pr.mergeable_state == "blocked":
            build_status = self._pr_build_status(pr)
            reviews = _pr_reviews(pr)

        return f"#{pr.number} {pr.title}\n     build: {build_status} - reviews: {reviews}\n"

    def _pr_build_status(self, pr):
        if self._github.get_build_status(self._project, pr.head.sha).state == "success":
            return CHECKMARK
        return CROSSMARK


def _check_migrations_merge(pr):
    files_changed = [x.filename for x in pr.get_files()]
    if git.migrations_found(files_changed):
        logger.warning("ATTENZIONE: migrations rilevate nel codice")
        if not prompt_utils.ask_confirm("Sicuro di voler continuare?"):
            sys.exit()


def _pr_reviews(pr):
    reviews = [r for r in pr.get_reviews() if r.state == "APPROVED"]
    if reviews:
        return CHECKMARK
    return CROSSMARK
