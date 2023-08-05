# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_passwd']

package_data = \
{'': ['*'], 'typer_passwd': ['.vscode/*']}

install_requires = \
['colorful>=0.5.4,<0.6.0',
 'pyperclip>=1.8.0,<2.0.0',
 'typer[all]>=0.3.0,<0.4.0',
 'wasabi>=0.7.1,<0.8.0',
 'yakutils>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['typer-passwd = typer_passwd.main:app']}

setup_kwargs = {
    'name': 'typer-passwd',
    'version': '0.1.3',
    'description': 'Simple CLI app that generates random passwords.',
    'long_description': "# typer-passwd\n> Quick typer cli app that'll give colored random passwords!\n\n[![PyPI version](https://badge.fury.io/py/typer-passwd.svg)](https://badge.fury.io/py/typer-passwd)\n\nAre you sick and tired of coming up with a password for every website you go to or being forced to reset your password every 30, 90 days??? Well you came to the right place! Just [pip install](https://realpython.com/what-is-pip/#installing-packages-with-pip), or better yet(!), [pipx](https://pipxproject.github.io/pipx/examples/#pipx-install-examples) `typer-passwd` and you'll never have to worry about coming up with certain length passwords that need a number, special character, blood, urine sample...\n![](header.png)\n\n## Installation\n\nOS X & Linux:\n\npipx install:\n\n```bash\n$ pipx install typer-passwd\n```\n\npip install:\n\n```bash\n$ pip install --user typer-passwd\n```\n\n\n## Usage example\n\nThe cli app is set to output 8 to 64 characters as this time. To output color randomly generated password:\n\n```bash\n$ typer-passwd coloring\n```\n\nIf you're wanting to output a password more than 8 characters in length just add the number you want.\n\n```bash\n$ typer-passwd coloring 55\n```\n\nIf you want to view the password without color output then use the `no-color` argument:\n\n```bash\n$ typer-passwd no-coloring\n```\n\nAs with `color` to generate a longer password, just add the number for the length of the password.\n\n```bash\n$ typer-passwd no-coloring 55\n```\n\n\n## Release History\n\n\n## Meta\n\nCatch me on Twitter @ [@mrcartoonster](https://twitter.com/mrcartoonster) \nOr email me @ mrcartoonster@gmail.com\n\nDistributed under the XYZ license. See ``LICENSE`` for more information.\n\n[https://github.com/mrcartoonster/](https://github.com/mrcartoonster/typer-passwd)\n",
    'author': 'Mrnobody',
    'author_email': 'mrcartoonster@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
