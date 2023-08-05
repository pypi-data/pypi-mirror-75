# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solid_backend',
 'solid_backend.contact',
 'solid_backend.contact.migrations',
 'solid_backend.contact.tests',
 'solid_backend.contact.tests.conftest_files',
 'solid_backend.content',
 'solid_backend.content.migrations',
 'solid_backend.glossary',
 'solid_backend.glossary.migrations',
 'solid_backend.glossary.tests',
 'solid_backend.glossary.tests.conftest_files',
 'solid_backend.message',
 'solid_backend.message.migrations',
 'solid_backend.message.tests',
 'solid_backend.message.tests.conftest_files',
 'solid_backend.photograph',
 'solid_backend.photograph.migrations',
 'solid_backend.photograph.tests',
 'solid_backend.photograph.tests.conftest_files',
 'solid_backend.quiz',
 'solid_backend.quiz.migrations',
 'solid_backend.quiz.tests',
 'solid_backend.quiz.tests.conftest_files',
 'solid_backend.slideshow',
 'solid_backend.slideshow.migrations',
 'solid_backend.slideshow.tests',
 'solid_backend.slideshow.tests.conftest_files',
 'solid_backend.utility']

package_data = \
{'': ['*']}

install_requires = \
['django-cleanup==4.0.0',
 'django-mptt==0.11.0',
 'django-stdimage>=5.1.1,<6.0.0',
 'django>=3.0.7,<4.0.0',
 'djangorestframework==3.11.0',
 'mutagen>=1.44.0,<2.0.0',
 'pillow==7.1.2',
 'psycopg2-binary>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'solid-backend',
    'version': '0.1.6',
    'description': 'Clean Django App for E-Learning apllication with ',
    'long_description': '# S.O.L.I.D-Backend\n\n## What is S.O.L.I.D?\n\n\n## Documentation\n\nComing soon...\n\n## Coverage\n\nComing soon...\n\n## Try it out and local development\n\nFor a How-To guide see the README in the sample_project directory.\n\n',
    'author': 'Christian Grossm\xc3\xbcller',
    'author_email': 'chgad.games@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zentrumnawi/solid-backend',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
