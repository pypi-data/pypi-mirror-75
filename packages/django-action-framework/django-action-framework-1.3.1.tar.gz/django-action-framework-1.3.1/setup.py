# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daf',
 'daf.migrations',
 'daf.tests',
 'daf.tests.actions',
 'daf.tests.migrations']

package_data = \
{'': ['*'],
 'daf': ['templates/daf/admin/*'],
 'daf.tests': ['templates/tests/*']}

install_requires = \
['django-args>=1.3.0,<2.0.0',
 'django>=2',
 'djangorestframework>=3.0.0,<4.0.0',
 'python-args>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'django-action-framework',
    'version': '1.3.1',
    'description': 'Easily create actions and various interfaces around them.',
    'long_description': "django-action-framework\n#######################\n\n``django-action-framework`` (``daf``) provides the ability to generate\na number of diverse interfaces from a single action definition. What is\nan action? It's a function. By writing a function and providing a few\nhints about the characteristics of your function, you can:\n\n1. Generate a form view from the function with proper form validation.\n2. Generate an update view on a model object that is passed to the function.\n3. Generate a bulk update view on multiple objects. These objects can\n   be parametrized over a function expecting one object, meaning your detail\n   and bulk views share the same code when desired.\n4. Generate wizard views to collect function arguments over multiple steps,\n   even if the steps are conditional.\n5. Natively integrate these views into the Django admin as model, detail,\n   or bulk actions.\n6. Generate Django Rest Framework actions on your viewsets.\n\n``daf`` removes the boilerplate and cognitive overhead of maintaining validation\nlogic, view logic, and update logic spread across Django views, models, admin\ninterfaces, API endpoints, and other locations in a Django project. ``daf``\nallows the engineer to focus on writing one clear and easily-testable piece of\nbusiness logic while treating complex UI and APIs as an extension of the\nfunction rather than a piece of intertwined code.\n\nFor examples and a full tutorial of how to use ``django-action-framework``,\ncheck out the `docs <https://django-action-framework.readthedocs.io/>`__.\n\nDocumentation\n=============\n\n`View the django-action-framework docs here\n<https://django-action-framework.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall django-action-framework with::\n\n    pip3 install django-action-framework\n\nAfter this, add ``daf`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-action-framework for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n- @romansul (Roman Sul)\n- @chang-brian (Brian Chang)\n",
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/django-action-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
