# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat', 'mdformat._renderer']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py>=0.4.7,<0.5.0']

entry_points = \
{'console_scripts': ['mdformat = mdformat.__main__:run']}

setup_kwargs = {
    'name': 'mdformat',
    'version': '0.1.0',
    'description': 'CommonMark compliant Markdown formatter',
    'long_description': '[![Build Status](https://travis-ci.com/hukkinj1/mdformat.svg?branch=master)](<https://travis-ci.com/hukkinj1/mdformat>)\n[![codecov.io](https://codecov.io/gh/hukkinj1/mdformat/branch/master/graph/badge.svg)](<https://codecov.io/gh/hukkinj1/mdformat>)\n[![PyPI version](https://badge.fury.io/py/mdformat.svg)](<https://badge.fury.io/py/mdformat>)\n\n# mdformat\n\n> CommonMark compliant Markdown formatter\n\nMdformat is an opinionated Markdown formatter that can be used to enforce a consistent style in Markdown files.\nMdformat is a Unix-style command-line tool as well as a Python library.\n\nThe features/opinions of the formatter include:\n\n- Strip trailing and leading whitespace\n- Always use ATX style headings\n- Consistent indentation for contents of block quotes and list items\n- Reformat reference links as inline links\n- Reformat indented code blocks as fenced code blocks\n- Separate blocks with a single empty line\n  (an exception being tight lists where the separator is a single newline character)\n- End the file in a single newline character\n- Use `1.` as the ordered list marker if possible, also for noninitial list items\n\nMdformat by default will not change word wrapping.\nThe rationale for this is to support techniques like\n[One Sentence Per Line](<https://asciidoctor.org/docs/asciidoc-recommended-practices/#one-sentence-per-line>)\nand\n[Semantic Line Breaks](<https://sembr.org/>).\n\n**NOTE:**\nThe formatting style produced by mdformat may change in each version.\nIt is recommended to pin mdformat dependency version.\n\n## Installing\n\n~~~bash\npip install mdformat\n~~~\n\n## Command line usage\n\n### Format files\n\nFormat files `README.md` and `CHANGELOG.md` in place\n\n~~~bash\nmdformat README.md CHANGELOG.md\n~~~\n\nFormat `.md` files in current working directory recursively\n\n~~~bash\nmdformat .\n~~~\n\nRead Markdown from standard input until `EOF`.\nWrite formatted Markdown to standard output.\n\n~~~bash\nmdformat -\n~~~\n\n### Check formatting\n\n~~~bash\nmdformat --check README.md CHANGELOG.md\n~~~\n\nThis will not apply any changes to the files.\nIf a file is not properly formatted, the exit code will be non-zero.\n\n## Python API usage\n\n### Format text\n\n~~~python\nimport mdformat\n\nunformatted = "\\n\\n# A header\\n\\n"\nformatted = mdformat.text(unformatted)\nassert formatted == "# A header\\n"\n~~~\n\n### Format a file\n\nFormat file `README.md` in place:\n\n~~~python\nimport mdformat\n\n# Input filepath as a string...\nmdformat.file("README.md")\n\n# ...or a pathlib.Path object\nimport pathlib\nfilepath = pathlib.Path("README.md")\nmdformat.file(filepath)\n~~~\n\n## Usage as a pre-commit hook\n\n`mdformat` can be used as a [pre-commit](<https://github.com/pre-commit/pre-commit>) hook.\nAdd the following to your project\'s `.pre-commit-config.yaml` to enable this:\n\n~~~yaml\n- repo: https://github.com/hukkinj1/mdformat\n  rev: 0.1.0  # Use the ref you want to point at\n  hooks:\n  - id: mdformat\n~~~\n',
    'author': 'hukkinj1',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
