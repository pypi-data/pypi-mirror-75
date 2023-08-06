# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jse']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['jse = jse.entry:main']}

setup_kwargs = {
    'name': 'jse',
    'version': '0.1.1',
    'description': 'Quickly edit json files from the command line',
    'long_description': '# jse - JSON Editor [![Build Status](https://travis-ci.org/bjubes/jse.svg?branch=master)](https://travis-ci.org/bjubes/jse) [![Coverage Status](https://coveralls.io/repos/github/bjubes/jse/badge.svg?branch=master)](https://coveralls.io/github/bjubes/jse?branch=master)\n\n\nquickly edit json files from the command line\n\njse is pragmatic and terse. It lets you edit json fast, without needing to care about quotes, types, exact indexes, or any of the stuff that makes json a pain.\n## Usage\n```\n$ jse FILE COMMAND QUERY VALUE\n```\n#### TLDR Version\nedit an existing key: `e` or `edit`\n```\n$ jse config.json edit app.version 0.3.3\n```\nadd a new element: `a` or `add`\n```\n$ jse todo.json add list.shopping {task:eggs,done:false}\n```\ndelete a value: `d` or `delete`\n```\n$ jse problems.json delete problems[99]\n```\nfull [examples with json files](#examples) below\n\n## Installing\n\n```\npip3 install jse\n```\n\n### Running from Source\nRequirements:\n- Python 3.7+\n- [Click](https://pypi.org/project/click/)\n\nSteps:\n1. clone the repository\n2. install click `pip3 install click`\n3. make the run script executable `chmod +x run.py`\n4. place jse on the path `ln -s /path/to/run.py ~/.local/bin/jse`\n\nusing pipenv is recommended if you plan to contribute\n\n## Examples\nAssume we have this json file\n```json\n# example.json\n{\n    "users": [\n        {"name": "alice", "age": 21, "admin": false},\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": false}\n    ]\n}\n```\n\nWe want to delete the user alice using jse. All we need to do is specify `d` or `delete` mode and the path to her `user` object\n```\n$ jse example.json d users[0]\n```\nWe can use both index or dot notation.\n```shell\n$ jse example.json d users.0   #users.first or users.^ also work\n```\n```json\n# example.json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": false}\n    ]\n}\n```\nNow lets make charlie an admin. To edit an existing field we use the edit command with `e` or `edit`. Edit takes a key to change and its new value.\n```\n$ jse example.json e users.1.admin true\n```\n```json\n# example.json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ]\n}\n```\njse is smart enough to infer datatypes from the command line. it can also accept complex nested objects and arrays in a terse, quote-free format. Lets add a new nested field to the file with `add` or `a`\n```\n$ jse example.json a highscore [{score:32.5,user:bob,metadata:{ip:192.168.1.102,client:firefox}}]\n```\n```json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ],\n    "highscore": [\n        {\n            "score": 32.5,\n            "user": "bob",\n            "metadata": {\n                "ip": "192.168.1.102",\n                "client": "firefox"\n            }\n        }\n    ]\n}\n```\njse also understands lists, so we can add new elements to one without needing an explicit index. It will infer we are trying to append from `add` instead of changing the list itself to an object (`edit`)\n```\n$ jse example.json a highscore {score:52,user:charlie}\n```\n```json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ],\n    "highscore": [\n        {\n            "score": "32.5",\n            "user": "bob",\n            "metadata": {\n                "ip": "192.168.1.102",\n                "client": "firefox"\n            }\n        },\n        {\n            "score": 52.0,\n            "user": "charlie"\n        }\n    ]\n}\n```\nfirst and last (or `^` and `$`) can also be used as a list index for any operation\n\n```\n$ jse example.json a users.first {name:jon,age:22,admin:false}\n```\n```json\n{\n    "users": [\n        {"name": "jon", "age": 22, "admin":false},\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ],\n    "highscore": [\n        {\n            "score": "32.5",\n            "user": "bob",\n            "metadata": {\n                "ip": "192.168.1.102",\n                "client": "firefox"\n            }\n        },\n        {\n            "score": 52.0,\n            "user": "charlie"\n        }\n    ]\n}\n```\n\njse\'s error messages are informative, because no one wants a generic KeyError\n```\n$ jse example.json a users.0.name "not bob"\n\'name\' already has a value. Use the edit command to modify it\n```\n```\n$ jse example.json d users[2]\nThere is no element with index 2. The largest index is 1\n```\n\nYou can also delete mulitple keys by passing them seperately\n```\n$ jse example.json d users.0.age users.1.age users.2.age\n```\n```json\n{\n    "users": [\n        {\n            "name": "jon",\n            "admin": false,\n        },\n        {\n            "name": "bob",\n            "admin": true,\n        },\n        {\n            "name": "charlie",\n            "admin": true\n        }\n    ]\n    ...\n}\n```\nIf you want to select every element, use the  `*` or `all` operator\n```shell\n$ jse example.json d users.*.age # or users.all.age\n```\n',
    'author': 'Brian Jubelirer',
    'author_email': 'brian2386@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bjubes/jse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
