# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['run_all_the_tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'run-all-the-tests',
    'version': '0.1.16',
    'description': "Make sure both 'python -m pytest' and 'pytest' run your tests.",
    'long_description': "Run a series of test invocation making sure each test case works with both 'pytest' and\n 'python -m pytest' over all working directories between the project root and the directory\n  containing the test script.\n\n```\n├─ src\n│\n│<-- # run selected __main__'s from this working directory\n│\n│  └─ __init__.py\n│  └─ foo.py\n│  ├─ bar\n│  │   └─ __init__.py\n│  │   └─ bar.py\n│  │\n│  │<-- # run selected __main__'s from this working directory\n│  │\n│  └─ run_foo_main.py\n│  └─ run_bar_main.py\n│\n│<-- # run selected test cases from this working directory\n│\n├─ tests\n│  │\n│  │<-- # run selected test cases from this working directory\n│  │\n│  └─ test_foo.py\n│  └─ bar\n│        │<-- # run selected bar test cases from this working directory\n│        │\n│        └─ test_bar.py\n└─ setup.py\n```\n\nYour `run_all_my_tests.py`:\n```\nfrom run_all_the_tests import TestCasePath, TestCase, Group, TestType\n\nif __name__ == '__main__': \n    project_path: PurePath = Path(__file__).absolute().parent.parent\n\n\n    def gen_test_case_path(test_case: str) -> TestCasePath:\n        return TestCasePath(project_path, PurePath(test_case))\n\n\n    all_test_cases: Tuple[TestCase, ...] = (\n        TestCase.gen_test_case(gen_test_case_path('tests/test_foo.py')),\n        TestCase.gen_test_case(gen_test_case_path('tests/bar/test_bar.py')),\n    )\n\n    run_all_tests(all_test_cases)\n```\n\nEach set of tests are run in parallel within `Group.ONE`. Designate\ntests to run within non-conflicting groups of parallel runs by assigning\nall test cases that can run without conflict to the same `Group`.\n\n```\n    all_test_cases: Tuple[TestCase, ...] = (\n        TestCase.gen_test_case(gen_test_case_path('tests/test_foo.py')),\n        TestCase.gen_test_case(gen_test_case_path('tests/bar/test_bar.py'), Group.TWO),\n    )\n```\n\n`TestCase.gen_test_case()` also supports the following agrs:\n```\n    pytest_filter: str = None\n    :param pytest_filter: pytest -k string\n \n    test_types: Tuple[TestType, ...] = TestType.all_test_types()\n    :param test_types: for exceptional situations, limit a TestCase to run for limited set of TestType's\n```\n",
    'author': 'Greg Kedge',
    'author_email': 'gregwork@kedges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkedge/run-all-the-tests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
