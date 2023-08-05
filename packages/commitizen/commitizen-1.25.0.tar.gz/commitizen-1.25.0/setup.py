# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commitizen',
 'commitizen.commands',
 'commitizen.config',
 'commitizen.cz',
 'commitizen.cz.conventional_commits',
 'commitizen.cz.customize',
 'commitizen.cz.jira']

package_data = \
{'': ['*'], 'commitizen': ['templates/*']}

install_requires = \
['colorama>=0.4.1,<0.5.0',
 'decli>=0.5.0,<0.6.0',
 'jinja2>=2.10.3,<3.0.0',
 'packaging>=19,<21',
 'questionary>=1.4.0,<2.0.0',
 'termcolor>=1.1,<2.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['cz = commitizen.cli:main',
                     'git-cz = commitizen.cli:main']}

setup_kwargs = {
    'name': 'commitizen',
    'version': '1.25.0',
    'description': 'Python commitizen client tool',
    'long_description': '[![Github Actions](https://github.com/commitizen-tools/commitizen/workflows/Python%20package/badge.svg?style=flat-square)](https://github.com/commitizen-tools/commitizen/actions)\n[![Conventional\nCommits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)\n[![PyPI Package latest\nrelease](https://img.shields.io/pypi/v/commitizen.svg?style=flat-square)](https://pypi.org/project/commitizen/)\n[![Supported\nversions](https://img.shields.io/pypi/pyversions/commitizen.svg?style=flat-square)](https://pypi.org/project/commitizen/)\n[![Codecov](https://img.shields.io/codecov/c/github/commitizen-tools/commitizen.svg?style=flat-square)](https://codecov.io/gh/commitizen-tools/commitizen)\n\n![Using commitizen cli](images/demo.gif)\n\n---\n\n**Documentation**: https://commitizen-tools.github.io/\n\n---\n\n## About\n\nCommitizen is a tool designed for teams.\n\nIts main purpose is to define a standard way of committing rules\nand communicating it (using the cli provided by commitizen).\n\nThe reasoning behind it is that it is easier to read, and enforces writing\ndescriptive commits.\n\nBesides that, having a convention on your commits makes it possible to\nparse them and use them for something else, like generating automatically\nthe version or a changelog.\n\n### Commitizen features\n\n- Command-line utility to create commits with your rules. Defaults: [Conventional commits][conventional_commits]\n- Display information about your commit rules (commands: schema, example, info)\n- Bump version automatically using [semantic versioning][semver] based on the commits. [Read More](./bump.md)\n- Generate a changelog using [Keep a changelog][keepchangelog]\n\n## Requirements\n\nPython 3.6+\n\n[Git][gitscm] `1.8.5.2`+\n\n## Installation\n\nGlobal installation\n\n```bash\nsudo pip3 install -U Commitizen\n```\n\n### Python project\n\nYou can add it to your local project using one of these:\n\n```bash\npip install -U commitizen\n```\n\n```bash\npoetry add commitizen --dev\n```\n\n## Usage\n\n### Committing\n\nRun in your terminal\n\n```bash\ncz commit\n```\n\nor the shortcut\n\n```bash\ncz c\n```\n\n### Integrating with Pre-commit\nCommitizen can lint your commit message for you with `cz check`.\nYou can integrate this in your [pre-commit](https://pre-commit.com/) config with:\n\n```yaml\n---\nrepos:\n  - repo: https://github.com/commitizen-tools/commitizen\n    rev: master\n    hooks:\n      - id: commitizen\n        stages: [commit-msg]\n```\n\nAfter the configuration is added, you\'ll need to run\n\n```sh\npre-commit install --hook-type commit-msg\n```\n\nRead more about the `check` command [here](https://commitizen-tools.github.io/commitizen/check/).\n\n### Help\n\n```bash\n$ cz --help\nusage: cz [-h] [--debug] [-n NAME] [--version]\n          {init,commit,c,ls,example,info,schema,bump,changelog,ch,check,version}\n          ...\n\nCommitizen is a cli tool to generate conventional commits.\nFor more information about the topic go to https://conventionalcommits.org/\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --debug               use debug mode\n  -n NAME, --name NAME  use the given commitizen (default:\n                        cz_conventional_commits)\n  --version             get the version of the installed commitizen\n\ncommands:\n  {init,commit,c,ls,example,info,schema,bump,changelog,ch,check,version}\n    init                init commitizen configuration\n    commit (c)          create new commit\n    ls                  show available commitizens\n    example             show commit example\n    info                show information about the cz\n    schema              show commit schema\n    bump                bump semantic version based on the git log\n    changelog (ch)      generate changelog (note that it will overwrite\n                        existing file)\n    check               validates that a commit message matches the commitizen\n                        schema\n    version             get the version of the installed commitizen or the\n                        current project (default: installed commitizen)\n```\n\n## Third-Party Commitizen Templates\n\nSee [Third-Party Commitizen Templates](third-party-commitizen.md).\n\n## FAQ\n\n### Why are `revert` and `chore` valid types in the check pattern of cz conventional_commits but not types we can select?\n\n`revert` and `chore` are added to the "pattern" in `cz check` in order to prevent backward errors, but officially they are not part of conventional commits, we are using the latest [types from Angular](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#type) (they used to but were removed).\nHowever, you can create a customized `cz` with those extra types. (See [Customization](https://commitizen-tools.github.io/commitizen/customization/)\n\nSee more discussion in issue [#142](https://github.com/commitizen-tools/commitizen/issues/142) and [#36](https://github.com/commitizen-tools/commitizen/issues/36)\n\n### How to handle revert commits?\n\n```sh\ngit revert --no-commit <SHA>\ngit commit -m "revert: foo bar"\n```\n\n## Contributing\n\nSee [Contributing](contributing.md)\n\n[conventional_commits]: https://www.conventionalcommits.org\n[semver]: https://semver.org/\n[keepchangelog]: https://keepachangelog.com/\n[gitscm]: https://git-scm.com/downloads\n',
    'author': 'Santiago Fraire',
    'author_email': 'santiwilly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/commitizen-tools/commitizen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
