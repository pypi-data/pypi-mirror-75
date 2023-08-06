# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_locker']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.2,<6.0.0']

setup_kwargs = {
    'name': 'pytest-locker',
    'version': '0.2.2',
    'description': ' Used to lock object during testing. Essentially changing assertions from being hard coded to asserting that nothing changed ',
    'long_description': '.. image:: https://github.com/luttik/pytest-locker/workflows/CI/badge.svg\n    :alt: actions batch\n    :target: https://github.com/Luttik/pytest-locker/actions?query=workflow%3ACI+branch%3Amaster\n.. image:: https://badge.fury.io/py/pytest-locker.svg\n    :alt: pypi\n    :target: https://pypi.org/project/pytest-locker/\n\n.. image:: https://codecov.io/gh/Luttik/pytest-locker/branch/master/graph/badge.svg\n    :alt: codecov\n    :target: https://codecov.io/gh/luttik/pytest-locker\n\nPyTest-Locker\n-------------\nThe test-locker can be used to "lock" data from during a test.\nThis means that rather than having to manually specify the expected output\nyou lock the data when it corresponds to expected bahaviour.\n\nWhy use Locker\n==============\n- Time efficient: No need to hard code expected responses. (Especially usefull for data heavy unittests)\n- Easy to verify changes: \n\n  - Seperates logic of the test and expected values in the test further\n  - Lock files, and changes to them, are easy to interpret. \n    Therefore, evaluting them in pull-requests a great method of quality controll. \n\nInstall\n=======\nrun ``pip install pytest-locker``\n\nUse\n===\n- Step 1: Add ``from pytest_locker import locker`` to your\n  `conftest.py <https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re>`_ file\n- Step 2: To access the locker by adding it to the method parameters i.e. ``def test_example(locker)``\n- Step 3: Use ``locker.lock(your_string, optional_name)`` to lock the data.\n- Additionally: Don\'t forget to commit the ``.pytest_locker/`` directory for ci/cd testing\n\nAnd you\'re all set!\n\nTip\n===\nWhen using locks to test your file it is even more important than usual that the\n`pytest rootdir <https://docs.pytest.org/en/latest/customize.html>`_ is fixed.\nClick the `link <https://docs.pytest.org/en/latest/customize.html>`_ for all the options\n(one is adding a ``pytest.ini`` to the root folder).\n\nThe Locker test Flows\n=====================\nThere are two modes based on for locking.\n\n- When user input is allowed, i.e. when running pytest with ``--capture  no`` or ``-s``\n\n  When user input is allowed and the given data does not correspond to the data in the lock\n  the *user is prompted* if the new data should be stored or if the tests should fail.\n\n- When user input is captured which is default behavior for pytest\n\n  If user input is not allowed the tests will *automatically fail* if the expected lock file does not exist\n  or if the data does not correspond to the data in the lock file.\n\nThe Locker class\n================\nYou can also use ``pytest_locker.Locker`` (i.e. the class of which the ``locker`` fixture returns an instance).\ndirectly to create fixtures that locks a (non-string) object without needing to turn the object into a string it.\n\nExamples\n========\nFor example of use look at the tests in `<https://github.com/Luttik/repr_utils>`_.\n',
    'author': 'Luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luttik/pytest-locker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
