"""
This module contains functions to initialize python packages and projects
"""

import os
import click
from croco_cli.globals import GITHUB_USER_EMAIL, GITHUB_USER_LOGIN, GITHUB_USER_NAME
from croco_cli.utils import snake_case


@click.group()
def init():
    """Initialize python packages and projects"""


def _add_poetry(
        snaked_name: str,
        project_name: str,
        description: str
) -> None:
    """
    Adds a pyproject.toml file
    :param snaked_name: The name of the project in snake_case
    :param project_name: Name of the package
    :param description: The description of the project
    :return: None
    """
    toml = 'pyproject.toml'
    with open(toml, 'w') as toml_file:
        toml_file.write(f"""[tool.poetry]
name = '{snaked_name}'
version = '0.1.0'
description = '{description}'
authors = ['{GITHUB_USER_NAME} <{GITHUB_USER_EMAIL}>']
license = 'MIT'
readme = 'README.md'
repository = 'https://github.com/{GITHUB_USER_LOGIN}/{project_name}'
homepage = 'https://github.com/{GITHUB_USER_LOGIN}/{project_name}'
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS'
]
packages = [{{ include = '{snaked_name}' }}]

[tool.poetry.dependencies]
python = '^3.11'

[build-system]
requires = ['poetry-core']
build-backend = 'poetry.core.masonry.api'
""")
        while not os.path.exists(toml):
            pass


def _add_packages(open_source: bool) -> None:
    """
    Adds initial packages to pyproject.toml
    :param open_source: Whether project should be open-source
    :return: None
    """
    os.system('poetry add -D pytest')

    if open_source:
        os.system('poetry add -D build')
        os.system('poetry add -D twine')


def _initialize_folders(
        snaked_name: str,
        project_name: str,
        description: str
) -> None:
    """
    Initializes the project folders
    :param snaked_name: The name of the project in snake_case
    :param project_name: Name of the package
    :param description: The description of the project
    :return: None
    """
    os.mkdir(snaked_name)
    os.chdir(snaked_name)

    package_files = ['utils.py', 'types.py', 'exceptions.py']
    for filename in package_files:
        open(filename, 'w').close()

    with open('globals.py', 'w') as globals_file:
        globals_file.write("""import os

PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
""")

    with open('__init__.py', 'w') as init_file:
        init_file.write(f"""\"\"\"
{project_name}
~~~~~~~~~~~~~~
{description}

:copyright: (c) 2023 by {GITHUB_USER_NAME}
:license: MIT, see LICENSE for more details.
\"\"\"
""")

    os.chdir('../')
    os.mkdir('tests')
    os.chdir('tests')
    open('__init__.py', 'w').close()
    os.chdir('../')

    with open('conftest.py', 'w') as conftest_file:
        conftest_file.write('import pytest')

    with open('LICENSE', 'w') as license_file:
        license_file.write(f"""MIT License

Copyright (c) 2023 {GITHUB_USER_NAME}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")


def _add_readme(
        project_name: str,
        description: str,
        open_source: bool
) -> None:
    """
    :param project_name: Name of the package
    :param description: The description of the project
    :param open_source: Whether project should be open-source
    :return: None
    """
    with open('README.md', 'w') as readme_file:
        content = (f"""# {project_name}

[![Croco Logo](https://i.ibb.co/G5Pjt6M/logo.png)](https://t.me/crocofactory)

{description}

- **[Telegram channel](https://t.me/crocofactory)**
- **[Bug reports](https://github.com/{GITHUB_USER_LOGIN}/{project_name}/issues)**

Package's source code is made available under the [MIT License](LICENSE)

# Installing {project_name}""")

        if open_source:
            content += (f"""
To install `{project_name}` from PyPi, you can use that:

```shell
pip install {project_name}
```
""")
            content += (f"""
To install `{project_name}` from GitHub, use that:

```shell
pip install git+https://github.com/{GITHUB_USER_LOGIN}/{project_name}.git
```""")
        else:
            content += (f"""
To install `{project_name}` you need to get GitHub API token. After you need to replace this token instead of `<TOKEN>`:

```shell
pip install git+https://<TOKEN>@github.com/{GITHUB_USER_LOGIN}/{project_name}.git
```""")
        readme_file.write(content)


@init.command()
def _package() -> None:
    """Initialize the package directory"""
    repo_name = os.path.basename(os.getcwd())
    snaked_name = snake_case(repo_name)

    description = click.prompt('Enter the package description')

    click.echo('The package will be configured as open-source package')
    open_source = click.confirm('Agree?')

    _add_poetry(snaked_name, repo_name, description)
    _add_packages(open_source)
    _initialize_folders(snaked_name, repo_name, description)
    _add_readme(repo_name, description, open_source)