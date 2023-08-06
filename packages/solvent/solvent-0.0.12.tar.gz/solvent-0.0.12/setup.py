# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solvent']

package_data = \
{'': ['*'],
 'solvent': ['sites/action.iowagunowners.org/action/re-open-iowa-for-business/*',
             'sites/action.iowagunowners.org/sign-up/*',
             'sites/nolabels.salsalabs.org/071020trumphandlingcovid--19/index.html/*',
             'sites/oneclickpolitics.global.ssl.fastly.net/messages/edit/*',
             'sites/reopennc.com/@/*',
             'sites/secure.donaldjtrump.com/official-2020-strategy-survey/*',
             'sites/steube.house.gov/@/*',
             'sites/steube.house.gov/contact/newsletter/*',
             'sites/steube.house.gov/contact/newsletter/newsletter-subscribe-thank-you/*',
             'sites/www.donaldjtrump.com/landing/the-official-2020-strategy-survey/*',
             'sites/www.facebook.com/login.php/*']}

install_requires = \
['pomace==0.2b8']

entry_points = \
{'console_scripts': ['solvent = solvent:main']}

setup_kwargs = {
    'name': 'solvent',
    'version': '0.0.12',
    'description': 'Kills off fake grass.',
    'long_description': None,
    'author': 'Solvent',
    'author_email': 'solvent@example.com',
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
