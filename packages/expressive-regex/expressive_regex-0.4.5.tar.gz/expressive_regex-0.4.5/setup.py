# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expressive_regex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'expressive-regex',
    'version': '0.4.5',
    'description': '',
    'long_description': '# Expressive Regex\n\n<img alt="PyPI - License" src="https://img.shields.io/github/license/fsadannn/expressive_regex"> <img alt="PyPI - License" src="https://travis-ci.org/fsadannn/expressive_regex.svg"> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fsadannn/expressive_regex.svg">\n\nThis project was made with inspiration from [Super Expressive for JavaScript](https://github.com/francisrstokes/super-expressive).\n\nExpressive Regex allow you to build regular expressions in almost natural language and without external dependency.\n\n[Documentation](https://fsadannn.github.io/expressive_regex/)\n\n**Example**\nto match a telephone number that can be in the format 555-555-555, 555 555 555 or 555555555.\n\n```Python\nExpressiveRegex()\\\n    .exactly(2).group\\\n        .oneOrMore.digit\\\n        .optional.setOfLiterals\\\n            .char(\'-\')\\\n            .whitespaceChar\\\n        .end()\\\n    .end()\\\n    .oneOrMore.digit\\\n.toRegexString()\n```\n\n```Python\n"(?:\\d+[\\-\\s]?){2}\\d+"\n```',
    'author': 'fsadannn',
    'author_email': 'fsadannn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
