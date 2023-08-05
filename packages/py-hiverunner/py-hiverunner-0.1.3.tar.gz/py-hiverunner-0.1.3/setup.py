# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_hiverunner', 'py_hiverunner.core']

package_data = \
{'': ['*']}

install_requires = \
['JPype1>=0.7.5,<0.8.0',
 'py4j>=0.10.9,<0.11.0',
 'python-dotenv>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'py-hiverunner',
    'version': '0.1.3',
    'description': 'Python API for unittest Hive applications',
    'long_description': '# py-hiverunner\n[![Build Status](https://travis-ci.com/la9ran9e/py-hiverunner.svg?branch=master)](https://travis-ci.com/la9ran9e/py-hiverunner)\n[![Code Coverage Status](https://codecov.io/gh/la9ran9e/py-hiverunner/branch/master/graph/badge.svg)](https://codecov.io/gh/la9ran9e/py-hiverunner)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-hiverunner)](https://pypi.org/project/py-hiverunner/)\n[![Docker Build Status](https://img.shields.io/docker/cloud/build/la9ran9e/py-hiverunner)](https://hub.docker.com/r/la9ran9e/py-hiverunner)\n\nLibrary provides python API for [Klarna\'s HiveRunner](https://github.com/klarna/HiveRunner).\n\n## Install\n\nInstall `py-hiverunner` package with [pip](https://pypi.org/project/py-hiverunner/):\n\n```bash\n$ python -m pip install py-hiverunner\n```\n\n## Usage\nBefore using `py-hiverunner` you need start JVM with facade service based on original Klarna\'s `HiveRunner` - \n[java-hiverunner](./java-hiverunner).\nThis repo provides [docker container for Py4J Java Gateway for HiveRunner](https://hub.docker.com/r/la9ran9e/py-hiverunner).\n\nYou can pull this:\n```bash\n$ docker pull la9ran9e/py-hiverunner\n```\nand then run the container:\n```bash\n$ docker run -ti -p 25333:25333 -p 25334:25334 la9ran9e/py-hiverunner\n```\nAfter that you will have working server with Java HiveRunner.\n\nTry this:\n\n```python\nfrom py_hiverunner import hiverunner\nfrom pprint import pprint\n\n\nwith hiverunner() as hive:\n    hive.execute_query("create schema meh")\n    hive.execute_query("create table meh.nonsub(a int, b string, c array<string>)")\n    hive.execute_query("insert into meh.nonsub select 1, \'la9ran9e\', array(\'1\', \'a\', \'b\', \'6\')")\n    hive.execute_query("insert into meh.nonsub select 2, \'la9ran9e\', array(\'1\', \'b\', \'b\', \'6\')")\n    hive.execute_query("insert into meh.nonsub select 3, \'la9ran9e\', array(\'1\', \'c\', \'b\', \'6\')")\n    hive.execute_query("insert into meh.nonsub select 4, \'\', array(\'1\', \'d\', \'b\', \'6\')")\n\n    hive.execute_query("create table meh.sub(a int, b string, c boolean)")\n    hive.execute_query("insert into meh.sub select 1, \'la9ran9e\', true")\n\n    print("RESULT:")\n    pprint(hive.execute_query("""\n        select\n            *\n        from\n            meh.sub as sub\n        inner join\n            meh.nonsub as nonsub\n        on\n            sub.b = nonsub.b\n    """))\n```',
    'author': 'la9ran9e',
    'author_email': 'tvauritimur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/la9ran9e/py-hiverunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
