# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paroxython',
 'paroxython.cli',
 'paroxython.docs_developer_manual',
 'paroxython.docs_user_manual']

package_data = \
{'': ['*'], 'paroxython': ['resources/*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'regex>=2020.7.14,<2021.0.0',
 'typed-ast>=1.4.1,<2.0.0',
 'typing-extensions>=3.7.4.2,<4.0.0.0']

entry_points = \
{'console_scripts': ['paroxython = paroxython.cli.cli:main']}

setup_kwargs = {
    'name': 'paroxython',
    'version': '0.4.2',
    'description': 'Search Python code for algorithmic features',
    'long_description': '[![Build Status](https://travis-ci.com/laowantong/paroxython.svg?branch=master)](https://travis-ci.com/laowantong/paroxython)\n[![codecov](https://img.shields.io/codecov/c/github/laowantong/paroxython/master)](https://codecov.io/gh/laowantong/paroxython)\n[![Checked with mypy](https://img.shields.io/badge/typing-mypy-brightgreen)](http://mypy-lang.org/)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/73432ed4c5294326ba6279bbbb0fe2e6)](https://www.codacy.com/manual/laowantong/paroxython)\n[![Updates](https://pyup.io/repos/github/laowantong/paroxython/shield.svg)](https://pyup.io/repos/github/laowantong/paroxython/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/paroxython)\n[![GitHub Release](https://img.shields.io/github/release/laowantong/paroxython.svg?style=flat)]()\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/laowantong/paroxython)\n![paroxython SLOC](https://img.shields.io/badge/main%20program-~1600%20SLOC-blue)\n![tests SLOC](https://img.shields.io/badge/tests-~2600%20SLOC-blue)\n![helpers SLOC](https://img.shields.io/badge/helpers-~800%20SLOC-blue)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/laowantong/paroxython.svg?style=flat)]()\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n![](docs/resources/logo.png)\n\nParoxython is a set of command-line tools which finds and tags algorithmic features (such as assignments, nested loops, tail-recursive functions, etc.) in a collection of small Python programs, typically gathered for educational purposes (_e.g._, examples, patterns, exercise corrections).\n\nEach tag consists in a free-form label associated with its spanning lines. These labels are then mapped onto a knowledge taxonomy designed by the teacher with basic order constraints in mind (_e.g._, the fact that the introduction of the concept of early exit must come after that of loop, which itself requires that of control flow, is expressed with the following taxon: `flow/loop/exit/early`).\n\nSource codes, labels and taxa are stored in a database, which can finally be filtered through a pipeline of inclusion, exclusion, impartment and hiding commands on programs or taxa.\n\n# Installation and test-drive\n\n```\npip install paroxython\n```\n\nThe following command should print a help message and exit:\n\n```\nparoxython --help\n```\n\nUnder Jupyter notebook, you should first load the magic command:\n\n```python\n%load_ext paroxython\n```\n\nRun it on a cell of Python code (line numbers added for clarity):\n\n```python\n1   %%paroxython\n2   def fibonacci(n):\n3       result = []\n4       (a, b) = (0, 1)\n5       while a < n:\n6           result.append(a)\n7           (a, b) = (b, a + b)\n8       return result\n```\n\n| Taxon | Lines |\n|:--|:--|\n| `call/method/append` | 6 |\n| `flow/loop/exit/late` | 5-7 |\n| `flow/loop/while` | 5-7 |\n| `metadata/program` | 2-8 |\n| `metadata/sloc/8` | 2-8 |\n| `operator/arithmetic/addition` | 7 |\n| `subroutine/argument/arg` | 2 |\n| `subroutine/function` | 2-8 |\n| `test/inequality` | 5 |\n| `type/number/integer/literal` | 4 |\n| `type/number/integer/literal/zero` | 4 |\n| `type/sequence/list` | 6 |\n| `type/sequence/list/literal/empty` | 3 |\n| `type/sequence/tuple/literal` | 4, 4, 7, 7 |\n| `variable/assignment/parallel` | 4 |\n| `variable/assignment/parallel/slide` | 7 |\n| `variable/assignment/single` | 3 |\n\n# Documentation\n\nComing soon.\n',
    'author': 'Aristide Grange',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laowantong/paroxython/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
