#! -*- encoding: utf-8 -*-
import os
import sys

import click
from autoupgrade import Package

from suite_py.__version__ import __version__
from suite_py.commands.ask_review import AskReview
from suite_py.commands.check import Check
from suite_py.commands.create_branch import CreateBranch
from suite_py.commands.create_qa import CreateQA
from suite_py.commands.delete_qa import DeleteQA
from suite_py.commands.deploy import Deploy
from suite_py.commands.generator import Generator
from suite_py.commands.ip import IP
from suite_py.commands.merge_pr import MergePR
from suite_py.commands.open_pr import OpenPR
from suite_py.commands.project_lock import ProjectLock
from suite_py.commands.rollback import Rollback
from suite_py.commands.status import Status
from suite_py.lib.config import Config
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler import prompt_utils
from suite_py.lib.tokens import Tokens


@click.group()
@click.option(
    "--project",
    type=click.Path(exists=True),
    default=os.getcwd(),
    help="Path del progetto su cui eseguire il comando (default directory corrente)",
)
@click.option(
    "--timeout",
    type=click.INT,
    help="Timeout in secondi per le operazioni di CaptainHook",
)
@click.pass_context
def main(ctx, project, timeout):
    Package("suite_py").upgrade()
    print(f"v{__version__}")

    config = Config()

    if not git.is_repo(project):
        print(f"la directory {project} non è un repository git")
        sys.exit(-1)

    if not os.path.basename(project) in os.listdir(config.user["projects_home"]):
        print(f"la directory {project} non è in {config.user['projects_home']}")
        sys.exit(-1)

    if not config.user.get("skip_confirmation", False) and not prompt_utils.ask_confirm(
        f"Vuoi continuare sul progetto {os.path.basename(project)}?"
    ):
        sys.exit()

    ctx.ensure_object(dict)
    ctx.obj["project"] = os.path.basename(project)
    if timeout:
        config.user["captainhook_timeout"] = timeout
    ctx.obj["config"] = config
    ctx.obj["tokens"] = Tokens()
    os.chdir(os.path.join(config.user["projects_home"], ctx.obj["project"]))


@main.command(
    "create-branch", help="Crea branch locale e imposta la card di YouTrack in progress"
)
@click.option("--card", type=click.STRING, help="Numero card youtrack (ex. PRIMA-123)")
@click.pass_obj
def cli_create_branch(obj, card):
    CreateBranch(obj["project"], card, obj["config"], obj["tokens"]).run()


@main.command("lock", help="Lock di un progetto su staging o prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_obj
def cli_lock_project(obj, environment):
    ProjectLock(obj["project"], environment, "lock", obj["config"]).run()


@main.command("unlock", help="Unlock di un progetto su staging o prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_obj
def cli_unlock_project(obj, environment):
    ProjectLock(obj["project"], environment, "unlock", obj["config"]).run()


@main.command("open-pr", help="Apre una PR su GitHub")
@click.pass_obj
def cli_open_pr(obj):
    OpenPR(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("ask-review", help="Chiede la review di una PR")
@click.pass_obj
def cli_ask_review(obj):
    AskReview(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("create-qa", help="Crea un QA (integrazione con qainit)")
@click.pass_obj
def cli_create_qa(obj):
    CreateQA(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("delete-qa", help="Cancella un QA (integrazione con qainit)")
@click.pass_obj
def cli_delete_qa(obj):
    DeleteQA(obj["project"], obj["config"], obj["tokens"]).run()


@main.command(
    "merge-pr", help="Merge del branch selezionato con master se tutti i check sono ok"
)
@click.pass_obj
def cli_merge_pr(obj):
    MergePR(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("deploy", help="Deploy in produzione del branch master")
@click.pass_obj
def cli_deploy(obj):
    Deploy(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("rollback", help="Rollback in produzione")
@click.pass_obj
def cli_rollback(obj):
    Rollback(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("status", help="Stato attuale di un progetto")
@click.pass_obj
def cli_status(obj):
    Status(obj["project"], obj["config"]).run()


@main.command("check", help="Verifica autorizzazioni ai servizi di terze parti")
@click.pass_obj
def cli_check(obj):
    Check(obj["config"], obj["tokens"]).run()


@main.command("ip", help="Ottieni gli indirizzi IP degli hosts dove il task è running")
@click.argument("environment", type=click.Choice(("staging", "production")))
@click.pass_obj
def cli_ip(obj, environment):
    IP(obj["project"], environment).run()


@main.command("generator", help="Genera diversi file partendo da dei templates")
@click.pass_obj
def cli_generator(obj):
    Generator(obj["config"], obj["tokens"]).run()
