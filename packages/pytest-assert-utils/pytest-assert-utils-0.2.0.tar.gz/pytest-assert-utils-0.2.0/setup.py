# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_assert_utils', 'pytest_assert_utils.util']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['assert_utils = pytest_assert_utils']}

setup_kwargs = {
    'name': 'pytest-assert-utils',
    'version': '0.2.0',
    'description': 'Useful assertion utilities for use with pytest',
    'long_description': '# pytest-assert-utils\n\nHandy assertion utilities for use with pytest\n\n\n# Installation\n\n```bash\npip install pytest-assert-utils\n```\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/usePF/pytest-assert-utils',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
