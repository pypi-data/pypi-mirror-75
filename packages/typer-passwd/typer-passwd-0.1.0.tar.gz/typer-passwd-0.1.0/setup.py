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
    'version': '0.1.0',
    'description': 'Simple CLI app that generates random passwords.',
    'long_description': "# `typer-passwd`\n> Quick typer cli app that'll give colored random passwords!\n\n[![NPM Version][npm-image]][npm-url]\n[![Build Status][travis-image]][travis-url]\n[![Downloads Stats][npm-downloads]][npm-url]\n\nAre you sick and tired of coming up with a password for every website you go to or being forced to reset your password every 30, 90 days??? Well you came to the right place! Just [pip install](https://realpython.com/what-is-pip/#installing-packages-with-pip), or better yet(!), [pipx](https://pipxproject.github.io/pipx/examples/#pipx-install-examples) `typer-passwd` and you'll never have to worry about coming up with certain length passwords that need a number, special character, blood, urine sample...\n![](header.png)\n\n## Installation\n\nOS X & Linux:\n\n```sh\nnpm install my-crazy-module --save\n```\n\nWindows:\n\n```sh\nedit autoexec.bat\n```\n\n## Usage example\n\nA few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.\n\n_For more examples and usage, please refer to the [Wiki][wiki]._\n\n## Development setup\n\nDescribe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.\n\n```sh\nmake install\nnpm test\n```\n\n## Release History\n\n* 0.2.1\n    * CHANGE: Update docs (module code remains unchanged)\n* 0.2.0\n    * CHANGE: Remove `setDefaultXYZ()`\n    * ADD: Add `init()`\n* 0.1.1\n    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)\n* 0.1.0\n    * The first proper release\n    * CHANGE: Rename `foo()` to `bar()`\n* 0.0.1\n    * Work in progress\n\n## Meta\n\nYour Name \xe2\x80\x93 [@YourTwitter](https://twitter.com/dbader_org) \xe2\x80\x93 YourEmail@example.com\n\nDistributed under the XYZ license. See ``LICENSE`` for more information.\n\n[https://github.com/yourname/github-link](https://github.com/dbader/)\n\n## Contributing\n\n1. Fork it (<https://github.com/yourname/yourproject/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am 'Add some fooBar'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n\n<!-- Markdown link & img dfn's -->\n[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square\n[npm-url]: https://npmjs.org/package/datadog-metrics\n[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square\n[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square\n[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics\n[wiki]: https://github.com/yourname/yourproject/wiki\n",
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
