import os

import click

from .command.ci import Travis
from .command.managers import Pip, config_pyup
from .command.vcs import create_dir, git_init

APP_NAME = "pycutter"

manager_choices = {
    "pip": Pip,
}

ci_choices = {
    "travis": Travis(),
}


@click.command()
@click.option("-d", "--directory", default=os.getcwd(), help="Project directory")
@click.option(
    "-m",
    "--manager-package",
    default="pip",
    type=click.Choice(("pip",)),
    show_default=True,
    help="manager package to install dependences",
)
@click.option(
    "-c",
    "--ci",
    default="travis",
    type=click.Choice(("travis",)),
    show_default=True,
    help="Contiuous integration service",
)
@click.option(
    "-p",
    "--pyup",
    is_flag=True,
    help="Pyup keep your Python dependencies secure, up-to-date & compliant",
)
def main(directory, manager_package, ci, pyup):
    """
    Cookiecutter CLI to start projects Python
    """
    click.echo("Start project")
    create_dir(directory)

    manager = manager_choices[manager_package](directory)
    manager.create()

    git_init(directory)

    ci_choices[ci].config(directory)

    if pyup:
        config_pyup(directory)


if __name__ == "__main__":
    main()
