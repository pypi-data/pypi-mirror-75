# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['setuplog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'setuplog',
    'version': '0.2.2',
    'description': '',
    'long_description': '![CircleCI](https://img.shields.io/circleci/build/gh/schireson/setuplog/master) [![codecov](https://codecov.io/gh/schireson/setuplog/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/setuplog) [![Documentation Status](https://readthedocs.org/projects/setuplog/badge/?version=latest)](https://setuplog.readthedocs.io/en/latest/?badge=latest)\n\n## The pitch\n\nLogging setup is one of those annoying things that one finds themselves relearning\nevery time a new project is started.\n\n`setuplog` attempts to centralize, and simplify the set of decisions one needs to make\nwhen bootstrapping a project.\n\n```python\n# app.py\nfrom setuplog import setup_logging\n\nsetup_logging(\n    log_level=\'INFO\',\n    namespace=\'project_name\',\n\n    # opt into {}-style formatting!\n    style=\'format\',\n)\n\n# elsewhere\nfrom setuplog import log\n\nlog.info(\'Info!\')\n```\n\n## Installing\n\n```bash\npip install "setuplog"\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schireson/setuplog',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
