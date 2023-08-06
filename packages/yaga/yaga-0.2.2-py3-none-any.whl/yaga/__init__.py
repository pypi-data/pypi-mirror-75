__version__ = "0.2.2"

from pathlib import Path

import click
from click import ClickException


@click.group()
def cli():
    pass


@cli.command()
def targets():
    rules = []

    workspace = _resolve_workspace()

    build_files = workspace.glob("**/BUILD")
    for build_file in build_files:
        if build_file.exists():
            path = "/".join(build_file.relative_to(workspace).parts[:-1])

            def genrule(name):  # noqa
                rules.append(f"//{path}:{name}")

            exec(build_file.read_text())

    for rule in rules:
        click.echo(rule)


def _resolve_workspace():
    cwd = Path.cwd()
    for path in [cwd, *cwd.parents]:
        if (path / "WORKSPACE").is_file():
            return path
    raise ClickException("Could not find directory containing WORKSPACE file")
