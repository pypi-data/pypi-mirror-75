import os

import click
import git

from .gitignore import GITIGNORE


def create_dir(directory):
    if not os.path.isdir(directory):
        click.echo(f"Creating directory: {directory}")
        os.makedirs(directory)


def git_init(directory):
    git_dir = os.path.join(directory, ".git")
    if not os.path.isdir(git_dir):
        click.echo("Inicializing Git")
        g = git.cmd.Git(directory)
        g.init()
        gitignore(directory)


def gitignore(directory):
    file_gitignore = os.path.join(directory, ".gitignore")
    if not os.path.isfile(file_gitignore):
        click.echo("Creating file .gitignore")
        with open(file_gitignore, "w") as f:
            f.write(GITIGNORE)
