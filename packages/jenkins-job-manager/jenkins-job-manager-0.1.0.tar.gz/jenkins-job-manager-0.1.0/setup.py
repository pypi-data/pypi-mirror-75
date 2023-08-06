# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jenkins_job_manager']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jenkins-job-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremy Lavergne',
    'author_email': 'github@lavergne.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
