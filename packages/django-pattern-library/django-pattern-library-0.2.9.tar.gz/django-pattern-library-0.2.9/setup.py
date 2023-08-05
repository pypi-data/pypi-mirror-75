# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pattern_library']

package_data = \
{'': ['*'], 'pattern_library': ['templates/pattern_library/*']}

install_requires = \
['Django>=1.11,<3.1', 'Markdown>=3.1,<4.0', 'PyYAML>=5.1,<6.0']

setup_kwargs = {
    'name': 'django-pattern-library',
    'version': '0.2.9',
    'description': 'A module for Django that allows to build pattern libraries for your projects.',
    'long_description': "# Django pattern library\n\n[![PyPI](https://img.shields.io/pypi/v/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![PyPI downloads](https://img.shields.io/pypi/dm/django-pattern-library.svg)](https://pypi.org/project/django-pattern-library/) [![Travis](https://travis-ci.com/torchbox/django-pattern-library.svg?branch=master)](https://travis-ci.com/torchbox/django-pattern-library) [![Total alerts](https://img.shields.io/lgtm/alerts/g/torchbox/django-pattern-library.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/torchbox/django-pattern-library/alerts/)\n\nA module for Django that helps you to build pattern libraries and follow the\n[Atomic design](http://bradfrost.com/blog/post/atomic-web-design/) methodology.\n\n![Screenshot of the pattern library UI, with navigation, pattern rendering, and configuration](.github/pattern-library-screenshot.png)\n\n## Objective\n\nAt the moment, the main focus is to allow developers and designers\nuse exactly the same Django templates in a design pattern library\nand in production code.\n\nThere are a lot of alternative solutions for building\npattern libraries already. Have a look at [Pattern Lab](http://patternlab.io/) and\n[Astrum](http://astrum.nodividestudio.com/), for example.\nBut at [Torchbox](https://torchbox.com/) we mainly use Python and Django and\nwe find it hard to maintain layout on big projects in several places:\nin a project's pattern library and in actual production code. This is our\nattempt to solve this issue and reduce the amount of copy-pasted code.\n\n## Documentation\n\nDocumentation is located [here](./docs).\n\n## How to install\n\n1. Add `pattern_library` into your `INSTALLED_APPS`:\n\n   ```python\n   INSTALLED_APPS = [\n       # ...\n\n       'pattern_library',\n\n       # ...\n   ]\n   ```\n\n2. Add `pattern_library.loader_tags` into the `TEMPLATES` setting. For example:\n\n   ```python\n   TEMPLATES = [\n       {\n           'BACKEND': 'django.template.backends.django.DjangoTemplates',\n           'DIRS': [],\n           'APP_DIRS': True,\n           'OPTIONS': {\n               'context_processors': [\n                   'django.template.context_processors.debug',\n                   'django.template.context_processors.request',\n                   'django.contrib.auth.context_processors.auth',\n                   'django.contrib.messages.context_processors.messages',\n               ],\n               'builtins': ['pattern_library.loader_tags'],\n           },\n       },\n   ]\n   ```\n\n   Note that this module only supports the Django template backend out of the box.\n\n3. Set the `PATTERN_LIBRARY_TEMPLATE_DIR` setting to point to a template directory with your patterns:\n\n   ```python\n   PATTERN_LIBRARY_TEMPLATE_DIR = os.path.join(BASE_DIR, 'project_styleguide', 'templates')\n   ```\n\n   Note that `PATTERN_LIBRARY_TEMPLATE_DIR` must be available for\n   [template loaders](https://docs.djangoproject.com/en/1.11/ref/templates/api/#loader-types).\n\n4. Include `pattern_library.urls` into your `urlpatterns`. Here's an example `urls.py`:\n\n   ```python\n   from django.apps import apps\n   from django.conf.urls import url, include\n   ```\n\n\n    urlpatterns = [\n        # ... Your URLs\n    ]\n\n    if apps.is_installed('pattern_library'):\n        urlpatterns += [\n            url(r'^pattern-library/', include('pattern_library.urls')),\n        ]\n    ```\n\n## Contributing\n\nSee anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](CONTRIBUTING.md).\n\nIf you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.\n\n## Credits\n\nView the full list of [contributors](https://github.com/torchbox/django-pattern-library/graphs/contributors). [BSD](LICENSE) licensed.\n",
    'author': 'Mikalai Radchuk',
    'author_email': 'mikalai.radchuk@torchbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/torchbox/django-pattern-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
