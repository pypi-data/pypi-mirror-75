import logging
import sys

import click
import coloredlogs
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

from . import __version__


@with_plugins(iter_entry_points("nomnomdata.cli_plugins"))
@click.group()
@click.version_option(version=__version__, prog_name="nomnomdata-cli")
@click.option(
    "-l",
    "--loglevel",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
@click.pass_context
def cli(ctx, loglevel=None):
    """NomNomData Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["LOG_LEVEL"] = loglevel
    coloredlogs.install(
        level=logging.getLevelName(loglevel),
        stream=sys.stdout,
        fmt="%(msecs)d:%(levelname)s:%(name)s:%(message)s",
    )


@cli.command()
def test():
    import pytest
