# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_unicorn',
 'django_unicorn.management.commands',
 'django_unicorn.templatetags']

package_data = \
{'': ['*'],
 'django_unicorn': ['static/js/.babelrc',
                    'static/js/.babelrc',
                    'static/js/.babelrc',
                    'static/js/.babelrc',
                    'static/js/.babelrc',
                    'static/js/debounce.js',
                    'static/js/debounce.js',
                    'static/js/debounce.js',
                    'static/js/debounce.js',
                    'static/js/debounce.js',
                    'static/js/morphdom/2.6.1/morphdom-livewire.js',
                    'static/js/morphdom/2.6.1/morphdom-livewire.js',
                    'static/js/morphdom/2.6.1/morphdom-livewire.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.min.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.min.js',
                    'static/js/morphdom/2.6.1/morphdom-umd.min.js',
                    'static/js/unicorn.js',
                    'static/js/unicorn.js',
                    'static/js/unicorn.js',
                    'static/js/unicorn.js',
                    'static/js/unicorn.js',
                    'static/js/unicorn.min.js',
                    'static/js/unicorn.min.js',
                    'static/js/unicorn.min.js',
                    'static/js/unicorn.min.js',
                    'static/js/unicorn.min.js',
                    'static/js/utils.js',
                    'static/js/utils.js',
                    'static/js/utils.js',
                    'static/js/utils.js',
                    'static/js/utils.js',
                    'templates/unicorn/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'django>=3.0.0', 'orjson>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'django-unicorn',
    'version': '0.2.3',
    'description': 'A magical fullstack framework for Django.',
    'long_description': '# django-unicorn\nThe magical fullstack framework for Django. ✨\n\n`django-unicorn` provides a way to use backend Django code and regular Django templates to create interactive experiences without investing in a separate frontend framework.\n\n# Why?\nBuilding server-side sites in Django with the ORM and template engine is so pleasant, but once you need more interactivity on the frontend, there is a lot more ambiguity. Should you build out an entire API in Django REST framework? Should you use React or Vue.js (or some) other frontend framework?\n\nIt seems like there should be an easier way to create interactive experiences.\n\n# A note on beta software\n`django-unicorn` is beta software and the API will likely change on the way to 1.0. All efforts will be made to include an easy upgrade path. 1.0.0 will signify that the API won\'t change until the next major release.\n\n# Site\nhttps://www.django-unicorn.com\n\n# Demo\nhttps://github.com/adamghill/django-unicorn/blob/master/demo.mp4\n\n# Install\n1. `git clone git@github.com:adamghill/django-unicorn.git`\n1. `pip install -e ../django-unicorn`\n1. Add `django_unicorn` and `unicorn` to `INSTALL_APPS` in your Django settings file\n1. Add `path("unicorn/", include("django_unicorn.urls")),` into your project\'s `urlpatterns` in `urls.py`\n1. Add `{% load unicorn %}` to the top of your base template file\n1. Add `{% unicorn_styles %}` and `{% unicorn_scripts %}` into your base HTML file\n\n# How to create a component\n1. `python manage.py startunicorn hello-world`\n1. Add `{% unicorn \'hello-world\' %}` into the template you want to load the new `hello-world` component\n1. Take a look at `hello_world` class and `hello-world.html` template\n\n# Current functionality\n- `unicorn_styles`, `unicorn_scripts`, `unicorn` template tags\n- Base `component` class\n- Handles text input, checkbox, select options, select multiple options\n\n# Developing\n1. `git clone git@github.com:adamghill/django-unicorn.git`\n1. `poetry install`\n1. `poetry run example/manage.py migrate`\n1. `poetry run example/manage.py runserver 0:8000`\n1. Go to `localhost:8000` in your browser\n1. To install in another project `pip install -e ../django-unicorn`\n\n# Minify Javascript\n1. `npm install`\n1. `npm run-script build`\n\n# Bump version\n1. `npm run-script build`\n1. `poetry version major|minor|patch`\n1. Commit/push version bump\n1. `poetry publish --build -r pypi -u __token__`\n',
    'author': 'Adam Hill',
    'author_email': 'unicorn@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.django-unicorn.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
