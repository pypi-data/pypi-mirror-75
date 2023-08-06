# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['worktimething']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'worktimething',
    'version': '0.1.7',
    'description': 'A simple cli tool to record time spent on tasks.',
    'long_description': "WorkTimeThing\n=============\n\nSimple task time tracker::\n\n    alias wtt='python3 -m worktimething'\n    wtt b 141\n    wtt b 142\n    wtt e 142\n    wtt b 143\n    wtt  # shows a summary\n    141 :   4h 49m\n    142 :   2h 55m\n    143 : * 1h 20m\n    --------------------\n    TOTAL :   9h 5m\n    wtt a 141 5h3m  # Add time manually\n    wtt s 141 2h30m  # Subtract time manually\n\n\nThen get summaries in Jira work log format so that you don't have to worry about those any longer.\n",
    'author': 'arjoonn sharma',
    'author_email': 'arjoonn.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theSage21/worktime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
