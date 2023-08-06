[![Build Status](https://travis-ci.com/laowantong/paroxython.svg?branch=master)](https://travis-ci.com/laowantong/paroxython)
[![codecov](https://img.shields.io/codecov/c/github/laowantong/paroxython/master)](https://codecov.io/gh/laowantong/paroxython)
[![Checked with mypy](https://img.shields.io/badge/typing-mypy-brightgreen)](http://mypy-lang.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/73432ed4c5294326ba6279bbbb0fe2e6)](https://www.codacy.com/manual/laowantong/paroxython)
[![Updates](https://pyup.io/repos/github/laowantong/paroxython/shield.svg)](https://pyup.io/repos/github/laowantong/paroxython/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/paroxython)
[![GitHub Release](https://img.shields.io/github/release/laowantong/paroxython.svg?style=flat)]()
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/laowantong/paroxython)
![paroxython SLOC](https://img.shields.io/badge/main%20program-~1600%20SLOC-blue)
![tests SLOC](https://img.shields.io/badge/tests-~2700%20SLOC-blue)
![helpers SLOC](https://img.shields.io/badge/helpers-~800%20SLOC-blue)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/laowantong/paroxython.svg?style=flat)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![](docs/resources/logo.png)

# Presentation

Paroxython is a set of command-line tools which finds, tags and filters algorithmic features (such as assignments, nested loops, tail-recursive functions, etc.) in a collection of small Python programs, typically gathered for educational purposes (_e.g._, examples, patterns, exercise corrections).

## Intended audience

- You are a teacher, in charge of an introductory course in Python programming in an educational institution. Over the years, you have accumulated many—far too many—programs and code snippets that may be of interest to your students.
- You are a seasoned developer, and would like to share your knowledge by helping a loved one learn how to code. A cursory search for pedagogical material quickly yields an overwhelming amount of websites and repositories stuffed with Python programs of various levels (_e.g._,
[1](https://github.com/TheAlgorithms/Python),
[2](http://rosettacode.org/wiki/Category:Python),
[3](https://www.programming-idioms.org/about#about-block-language-coverage),
[4](https://github.com/codebasics/py),
[5](https://github.com/keon/algorithms),
[6](https://github.com/OmkarPathak/Python-Programs)
and a lot more from [Awesome Python in Education](https://github.com/quobit/awesome-python-in-education)).

## For which uses?

### Simple questions

### Complex questions

- Should I introduce the concept of subroutine before those of conditional and loop?
- Among the loops, which should come first: the most general (`while`), or the most useful in practice (`for`)?
- What are the concepts to be introduced prior to that of assignment?

Paroxython won't answer these questions for you, but it will give you some quantitative arguments 

These are issues on which I have personally changed my mind over the course of my teaching career.

You know some online resources offering tens, if not hundreds

https://github.com/OmkarPathak/Python-Programs


Paroxython won't answer these questions for you, but it will give you some quantitative arguments 

Or simply, You know Python and would like to help a loved one learn programming.


Over the years, you have accumulated dozens of programs and code snippets which you may use .
- 


Some are suitable for beginners, others require more advanced knowledge.

Paroxython is for people who teach Python programming.




programs

	|
	| paroxython collect
	V

labelled programs     teacher's taxonomy

    |   /
	| /
    V



Each tag consists in a free-form label associated with its spanning lines. These labels are then mapped onto a knowledge taxonomy designed by the teacher with basic order constraints in mind (_e.g._, the fact that the introduction of the concept of early exit must come after that of loop, which itself requires that of control flow, is expressed with the following taxon: `flow/loop/exit/early`).

Source codes, labels and taxa are stored in a database, which can finally be filtered through a pipeline of inclusion, exclusion, impartment and hiding commands on programs or taxa.

# Installation and test-drive

```
pip install paroxython
```

The following command should print a help message and exit:

```
paroxython --help
```

Under Jupyter notebook, you should first load the magic command:

```python
%load_ext paroxython
```

Run it on a cell of Python code (line numbers added for clarity):

```python
1   %%paroxython
2   def fibonacci(n):
3       result = []
4       (a, b) = (0, 1)
5       while a < n:
6           result.append(a)
7           (a, b) = (b, a + b)
8       return result
```

| Taxon | Lines |
|:--|:--|
| `call/method/append` | 6 |
| `flow/loop/exit/late` | 5-7 |
| `flow/loop/while` | 5-7 |
| `metadata/program` | 2-8 |
| `metadata/sloc/8` | 2-8 |
| `operator/arithmetic/addition` | 7 |
| `subroutine/argument/arg` | 2 |
| `subroutine/function` | 2-8 |
| `test/inequality` | 5 |
| `type/number/integer/literal` | 4 |
| `type/number/integer/literal/zero` | 4 |
| `type/sequence/list` | 6 |
| `type/sequence/list/literal/empty` | 3 |
| `type/sequence/tuple/literal` | 4, 4, 7, 7 |
| `variable/assignment/parallel` | 4 |
| `variable/assignment/parallel/slide` | 7 |
| `variable/assignment/single` | 3 |

# Examples

## Documentation

- [User manual and tutorials](docs/docs_user_manual/index.html) (under construction)
- [Developer manual](docs/docs_developer_manual/index.html) (under construction)
- [Module reference](docs/index.html#header-submodules)
