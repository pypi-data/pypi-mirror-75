# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['apirouter']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'django>=3.0.8,<4.0.0',
 'mkdocs-material[docs]>=5.5.0,<6.0.0',
 'mkdocs[docs]>=1.1.2,<2.0.0',
 'mkdocstrings[docs]>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'django-apirouter',
    'version': '0.2.1',
    'description': 'Django API router',
    'long_description': '# Django APIRouter (in progress)\n\nDjango API router component.\n\n*Inspired by [FastAPI](https://fastapi.tiangolo.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).*\n\n![tests](https://github.com/antonrh/django-apirouter/workflows/tests/badge.svg)\n[![codecov](https://codecov.io/gh/antonrh/django-apirouter/branch/master/graph/badge.svg)](https://codecov.io/gh/antonrh/django-apirouter)\n[![Documentation Status](https://readthedocs.org/projects/django-apirouter/badge/?version=latest)](https://django-apirouter.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![version](https://img.shields.io/pypi/v/django-apirouter.svg)](https://pypi.org/project/django-apirouter/)\n[![license](https://img.shields.io/pypi/l/django-apirouter)](https://github.com/antonrh/django-apirouter/blob/master/LICENSE)\n\n---\n\nDocumentation: https://django-apirouter.readthedocs.io/\n\n---\n\n## Installing\n\nInstall using `pip`:\n\n```bash\npip install django-apirouter\n```\n\n## Quick Example\n\n*project/urls.py*\n\n```python\nfrom apirouter import APIRouter, Response, Request\n\nrouter = APIRouter()\n\n\n@router.route("/")\ndef index(request: Request):\n    return Response("Hello, Django APIRouter!")\n\n\nurlpatterns = router.urls\n```\n\n## TODO:\n\n* Documentation\n* OpenAPI support (Swagger, ReDoc)\n* Pydantic support\n* Async views support (with Django 3.1)\n* etc.\n',
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antonrh/django-apirouter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
