# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssl_certinfo']

package_data = \
{'': ['*']}

install_requires = \
['pyopenssl', 'pyyaml', 'tqdm']

entry_points = \
{'console_scripts': ['ssl_certinfo = ssl_certinfo.cli:main']}

setup_kwargs = {
    'name': 'ssl-certinfo',
    'version': '0.3.5',
    'description': 'SSL CertInfo collects information about SSL certificates from a set of hosts.',
    'long_description': '============\nSSL CertInfo\n============\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - build\n      - |travis|\n    * - quality\n      - |codacy| |codeclimate| |sonar-qg| |sonar-rel|\n    * - coverage\n      - |coveralls| |codecov| |codeclimate-cov|\n    * - dependencies\n      - |pyup| |pyup-p3| |requires|\n\n\n.. |travis| image:: https://api.travis-ci.com/stdtom/ssl_certinfo.svg\n   :target: https://travis-ci.com/stdtom/ssl_certinfo\n   :alt: Travis Build Status\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/589c03a215ec4ddbb0085b523a857e55\n   :target: https://www.codacy.com/manual/stdtom/ssl_certinfo\n   :alt: Codacy Grade\n\n.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/1ed86e874b3c68672c5c/maintainability\n   :target: https://codeclimate.com/github/stdtom/ssl_certinfo/maintainability\n   :alt: Code Climate Maintainability\n\n.. |sonar-qg| image:: https://sonarcloud.io/api/project_badges/measure?project=stdtom_ssl_certinfo&metric=alert_status\n   :target: https://sonarcloud.io/dashboard?id=stdtom_ssl_certinfo\n   :alt: Sonar Quality Gate Status\n\n.. |sonar-rel| image:: https://sonarcloud.io/api/project_badges/measure?project=stdtom_ssl_certinfo&metric=reliability_rating\n   :target: https://sonarcloud.io/dashboard?id=stdtom_ssl_certinfo\n   :alt: Sonar Reliability Rating\n\n.. |coveralls| image:: https://coveralls.io/repos/github/stdtom/ssl_certinfo/badge.svg?branch=master\n   :target: https://coveralls.io/github/stdtom/ssl_certinfo?branch=master\n   :alt: Coveralls Test Coverage\n\n.. |codecov| image:: https://codecov.io/gh/stdtom/ssl_certinfo/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/stdtom/ssl_certinfo\n   :alt: CodeCov\n\n.. |codeclimate-cov| image:: https://api.codeclimate.com/v1/badges/1ed86e874b3c68672c5c/test_coverage\n   :target: https://codeclimate.com/github/stdtom/ssl_certinfo/test_coverage\n   :alt: Code Climate Test Coverage\n\n.. |pyup| image:: https://pyup.io/repos/github/stdtom/ssl_certinfo/shield.svg\n   :target: https://pyup.io/repos/github/stdtom/ssl_certinfo/\n   :alt: Updates\n\n.. |pyup-p3| image:: https://pyup.io/repos/github/stdtom/ssl_certinfo/python-3-shield.svg\n   :target: https://pyup.io/repos/github/stdtom/ssl_certinfo/\n   :alt: Python 3\n\n.. |requires| image:: https://requires.io/github/stdtom/ssl_certinfo/requirements.svg?branch=master\n   :target: https://requires.io/github/stdtom/ssl_certinfo/requirements/?branch=master\n   :alt: Requirements Status\n\n.. end-badges\n\n\n\n\nSSL CertInfo collects information about SSL certificates from a set of hosts.\n\n\n* Free software: Apache Software License 2.0\n* Documentation: https://ssl-certinfo.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `stdtom/cookiecutter-pypackage-pipenv`_ project template, based on `audreyr/cookiecutter-pypackage`_.\n\n.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter\n.. _`stdtom/cookiecutter-pypackage-pipenv`: https://github.com/stdtom/cookiecutter-pypackage-pipenv\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'StdTom',
    'author_email': 'stdtom@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stdtom/ssl_certinfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
