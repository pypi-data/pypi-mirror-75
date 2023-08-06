# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkpp']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['mkpp = mkpp.main:main']}

setup_kwargs = {
    'name': 'mkpp',
    'version': '0.1.7',
    'description': 'A simple tool for creating Python packages. For lazies.',
    'long_description': '# mkpp\nA simple tool for creating Python packages. For lazies.\n![preview](https://imgur.com/kwoKr6A.jpg)\n\n## Installation\nmkpp can be easily installed via pip:\n`pip install mkpp`\n\n## Usage\n`mkpp [--help] [--version] [--ignore-pep8] [--executable] packages [packages ...] [--add [FILE [FILE ...]]]`\n\n## Examples\n* `mkpp --executable my_package1 ~/Projects/Python/my_package2 some-dir/my_package3 --add config`\n* `mkpp app`\n* `mkpp --executable program1`\n* `mkpp app --add config utils`\n',
    'author': 'jieggii',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jieggii/mkpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
