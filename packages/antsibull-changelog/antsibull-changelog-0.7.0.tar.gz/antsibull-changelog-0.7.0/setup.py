# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antsibull_changelog', 'tests', 'tests.functional', 'tests.units']

package_data = \
{'': ['*'], 'tests.functional': ['bad/*', 'good/*']}

install_requires = \
['PyYAML', 'docutils', 'packaging', 'rstcheck>=3,<4', 'semantic_version']

entry_points = \
{'console_scripts': ['antsibull-changelog = antsibull_changelog.cli:main']}

setup_kwargs = {
    'name': 'antsibull-changelog',
    'version': '0.7.0',
    'description': 'Changelog tool for Ansible-base and Ansible collections',
    'long_description': "# antsibull-changelog -- Ansible Changelog Tool\n\nA changelog generator used by Ansible and Ansible collections.\n\n- Using the\n  [`antsibull-changelog` CLI tool](https://github.com/ansible-community/antsibull-changelog/tree/main/docs/changelogs.rst).\n- Documentation on the [`changelogs/config.yaml` configuration file for `antsibull-changelog`](https://github.com/ansible-community/antsibull-changelog/tree/main/docs/changelog-configuration.rst).\n- Documentation on the\n  [`changelog.yaml` format](https://github.com/ansible-community/antsibull-changelog/tree/main/docs/changelog.yaml-format.md).\n\n## Installation\n\nIt can be installed with pip:\n\n    pip install antsibull-changelog\n\nFor more information, see the\n[documentation](https://github.com/ansible-community/antsibull-changelog/tree/main/docs/changelogs.rst).\n\n## Using directly from git clone\n\nScripts are created by poetry at build time.  So if you want to run from\na checkout, you'll have to run them under poetry:\n\n    python3 -m pip install poetry\n    poetry install  # Installs dependencies into a virtualenv\n    poetry run antsibull-changelog --help\n\nIf you want to create a new release:\n\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\nNote: When installing a package published by poetry, it is best to use pip >= 19.0.\nInstalling with pip-18.1 and below could create scripts which use pkg_resources\nwhich can slow down startup time (in some environments by quite a large amount).\n\nIf you prefer to work with `pip install -e`, you can use [dephell](https://pypi.org/project/dephell/)\nto create a `setup.py` file from `pyproject.toml`:\n\n    dephell deps convert --from-path pyproject.toml --from-format poetry --to-path setup.py --to-format setuppy\n\nThen you can install antsibull-changelog with `pip install -e .`.\n\n\n## License\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later. See\n[LICENSE](https://github.com/ansible-community/antsibull-changelog/tree/main/LICENSE)\nfor a copy of the license.\n",
    'author': 'Felix Fontein',
    'author_email': 'felix@fontein.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ansible-community/antsibull-changelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
