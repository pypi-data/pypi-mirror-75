# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stormlock', 'stormlock.backends']

package_data = \
{'': ['*']}

extras_require = \
{'dynamodb': ['boto3>=1.13.1,<2.0.0'],
 'etcd': ['etcd3>=0.12.0,<0.13.0'],
 'postgresql': ['psycopg2>=2.8.5,<3.0.0'],
 'redis': ['redis>=3.4.1,<4.0.0']}

entry_points = \
{'console_scripts': ['stormlock = stormlock.cli:run'],
 'stormlock.backends': ['dynamodb = stormlock.backends.dynamodb:DynamoDB '
                        '[dynamodb]',
                        'etcd = stormlock.backends.etcd:Etcd [etcd]',
                        'postgresql = stormlock.backends.postgresql:Postgresql '
                        '[postgresql]',
                        'redis = stormlock.backends.redis:Redis [redis]']}

setup_kwargs = {
    'name': 'stormlock',
    'version': '0.1.1',
    'description': 'Simple distributed lock with support for multiple backends',
    'long_description': '==============\nStormlock\n==============\n\n|status| |version|\n\n.. |status| image:: https://github.com/tmccombs/stormlock/workflows/Main/badge.svg\n    :alt: Build Status\n    :target: https://github.com/tmccombs/stormlock/actions\n.. |version| image:: https://img.shields.io/pypi/v/stormlock\n    :alt: Version\n\n.. note:: Stormlock is a work in progress and not ready for production use.\n  Also documentation is mostly missing at this point.\n\nStormlock is a simple centralized locking system primarily intended for human operators (although it may also be useful in some\nsimple scripting scenarios).\n\nThe basic idea is that you acquire a lock by running a command, which gives you a "lease id". That lease id can then be used to\nrelease the lock, or extend its duration. All locks are given a duration after which they are automatically released. The lock is\nstored in  a backend, which is generally some kind of database.\n\nThe intended use case is where you have some kind of operation which happens somewhat infrequently across a distributed system,\nand you want to ensure multiple operators don\'t perform the operation at the same time. For example, this could be used to make sure\nto prevent simultaneous attempts to apply infrastructure-as-code changes, database patches, etc. to the same system by different\noperators.\n\nThis is **not** intended as a general purpose lock. It is designed with the assumption that locks can be held for a long time without\nproblems (hours or even days), and that the TTL for the lock doesn\'t need granularity better than a second. Furthermore, the availability\nof the lock is a function of the availability of the backend it uses.\n\nBackends\n--------\n\nThe currently supported backends are:\n\n* Etcd\n    - Renewing a lock always uses the same TTL as the original acquisition\n* Redis\n* DynamoDB\n* PostgreSQL\n\nIt\'s also possible to implement your own backend by implementing the ``stormlock.Backend`` interface and registering the class in the\n``stormlock.backends`` entry point in python.\n',
    'author': 'Thayne McCombs',
    'author_email': 'astrothayne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tmccombs/stormlock',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
