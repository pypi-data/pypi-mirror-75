# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jenkins_job_manager']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'jenkins-job-builder>=3.5.0,<4.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'python-jenkins>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['jjm = jenkins_job_manager.cli:jjm']}

setup_kwargs = {
    'name': 'jenkins-job-manager',
    'version': '0.2.3',
    'description': '',
    'long_description': None,
    'author': 'Jeremy Lavergne',
    'author_email': 'github@lavergne.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
