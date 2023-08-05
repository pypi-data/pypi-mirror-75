# -*- coding: utf-8 -*-
import secrets
import string
from typing import Optional, Sequence

import typer
from wasabi import color as c

app = typer.Typer()

__version__ = "0.1.0"


def version_callback(value: bool) -> None:
    """Returns version of typer-passwd."""
    ver_num = c(__version__, fg="green", bold=True)
    if value:
        typer.echo(f"typer-passwd version: {ver_num}")
        raise typer.Exit()


def colorizer(random_str: Sequence[str]):
    """Returns colored output of strings.

    Where letters are white, numbers are red, and special characters are
    blue.
    """
    color_str = []
    for _ in random_str:
        if _.isalpha():
            color_str.append(c(_, fg="white"))
        elif _.isnumeric():
            color_str.append(c(_, fg="red"))
        else:
            # This is Blue1. A deep blue.
            color_str.append(c(_, fg=21))
    return "".join(color_str)


def rstring(num: int, no: bool = False):
    """Helper function to create a color-coded random string.

    As well as non color-coded random string if given the option --no-
    color/-nc.
    """

    if no:
        return "".join([secrets.choice(string.printable[:94]) for _ in range(num)],)
    else:
        return colorizer([secrets.choice(string.printable[:94]) for _ in range(num)],)


def callback_color(value: int = 8):
    """Typer callback function to generate random string."""
    if value < 8 or value > 64:
        raise typer.BadParameter(
            "Password length must be between eight(8) to sixty-four(64)!",
        )
    else:
        return rstring(value)


def callback_no_color(value: int):
    """Typer callback function that will generate random non color-code
    password."""
    if value < 8 or value > 64:

        raise typer.BadParameter(
            "Password length must be between eight(8) to sixty-four(64)!",
        )
    else:
        return rstring(value, True)


@app.command()
def main(
    color: int = typer.Argument(
        ...,
        callback=callback_color,
        help="Takes integer for the length of random color-coded password.",
    ),
    no_color: int = typer.Option(
        8,
        "--no-color",
        "-nc",
        callback=callback_no_color,
        help="Take integer for the length of random non-color-coded password.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Returns current version of typer-passwd.",
        is_eager=True,
    ),
):
    """Outputs random password with the length given or eight(8) characters
    long by default."""
    typer.echo(color)
