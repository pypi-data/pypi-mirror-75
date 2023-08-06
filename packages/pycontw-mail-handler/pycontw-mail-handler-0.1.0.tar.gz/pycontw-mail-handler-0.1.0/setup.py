# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mail_handler']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0']

entry_points = \
{'console_scripts': ['render_mail = mail_handler.render_mail:main',
                     'send_mail = mail_handler.send_mail:main']}

setup_kwargs = {
    'name': 'pycontw-mail-handler',
    'version': '0.1.0',
    'description': 'Mail toolkit for PyCon Taiwan',
    'long_description': None,
    'author': 'Lee-W',
    'author_email': 'weilee.rx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
