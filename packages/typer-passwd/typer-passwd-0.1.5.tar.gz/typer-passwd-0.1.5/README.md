<p align="center">
  <!--<img width="460" height="300" src="typpic.png">-->
  <img src="typpic.png">
</p>

# typer-passwd
> Quick typer cli app that'll give colored random passwords!

[![PyPI version](https://badge.fury.io/py/typer-passwd.svg)](https://badge.fury.io/py/typer-passwd) ![GitHub All Releases](https://img.shields.io/github/downloads/mrcartoonster/typer-passwd/total)

Are you sick and tired of coming up with a password for every website you go to or being forced to reset your password every 30, 90 days??? Well you came to the right place! Just [pip install](https://realpython.com/what-is-pip/#installing-packages-with-pip), or better yet(!), [pipx](https://pipxproject.github.io/pipx/examples/#pipx-install-examples) `typer-passwd` and you'll never have to worry about coming up with certain length passwords that need a number, special character, blood, urine sample...

## Installation

OS X & Linux:

pipx install:

```bash
$ pipx install typer-passwd
```

pip install:

```bash
$ pip install --user typer-passwd
```

pipenv install:

```bash
$ pipenv install typer-passwd
```


## Usage example

The cli app is set to output 8 to 64 characters as this time. To output color randomly generated password:

```bash
$ typer-passwd coloring
```

If you're wanting to output a password more than 8 characters in length just add the number you want.

```bash
$ typer-passwd coloring 55
```

If you want to view the password without color output then use the `no-color` argument:

```bash
$ typer-passwd no-coloring
```

As with `color` to generate a longer password, just add the number for the length of the password.

```bash
$ typer-passwd no-coloring 55
```


## Release History


## Meta

Catch me on Twitter @ [@mrcartoonster](https://twitter.com/mrcartoonster)
Or email me @ mrcartoonster@gmail.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/mrcartoonster/](https://github.com/mrcartoonster/typer-passwd)
