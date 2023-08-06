# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['threader3000']
entry_points = \
{'console_scripts': ['threader3000 = threader3000:main']}

setup_kwargs = {
    'name': 'threader3000',
    'version': '1.0.7',
    'description': 'Threader3000 - Multi-threaded Port Scanner',
    'long_description': '<h5>Multi-threaded Python Port Scanner for use on Linux or Windows</h5>\n<br>\n-----------------------------------------------------------------------\n<br>\nThreader3000 is a script written in Python3 that allows multi-threaded \nport scanning. The program is interactive and simply requires you to run \nit to begin. Once started, you will be asked to input an IP address or a \nFQDN as Threader3000 does resolve hostnames. A full port scan should take \nthree minutes or less depending on your internet connection.\n<br>\nCheck me out on Twitter @joehelle, Twitch at https://twitch.tv/themayor11/, \non Github at https://github.com/dievus, or visit my cybersec Discord at \nhttps://discord.gg/DW4Q4pp.\n',
    'author': 'The Mayor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dievus/threader3000',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
