# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mupix']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'click>=7.0,<8.0',
 'lxml>=4.3,<5.0',
 'matplotlib>=3.1,<4.0',
 'music21>=5.7,<6.0',
 'scipy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['mupix = mupix:commands.cli']}

setup_kwargs = {
    'name': 'mupix',
    'version': '0.3.0',
    'description': 'MusicXML Evaluation Tool',
    'long_description': '# Mupix - musicfile comparison for humans\n\n![Travis (.com)](https://img.shields.io/travis/com/deepio/mupix)\n![GitHub last commit](https://img.shields.io/github/last-commit/deepio/mupix)\n![GitHub tag (latest by date)](https://img.shields.io/github/tag-date/deepio/mupix)\n![GitHub repo size](https://img.shields.io/github/repo-size/deepio/mupix)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mupix)\n![License](https://img.shields.io/github/license/deepio/mupix)\n\n### Installation\nBuild the latest version using poetry\n- `poetry install`\n\nBuild the latest version using pip\n- `pip install .`\n\nInstall it from PyPi\n- `pip install mupix`\n\n\n### Usage\nFor up-to-date usage information\n  - Checkout the [ReadTheDocs](https://mupix.readthedocs.io/en/latest/commands/)!\n  - For the offline version run `mupix` or `mupix --help`\n\n### Features\n- Outputs valid `JSON` data\n- Open and read (output to screen as JSON) symbolic music files\n- Align musical markings from two or more symbolic files using sequence alignment algorithms\n- Output the deferences between two files as full `error descriptions` or as `counted types`.\n  - **Error Description**\n\n  ```json\n  {\n    "ErrorDescription": {\n      "part2_0.0_C major": "part2_0.0_G major",\n      "part2_0.0_<music21.note.Note C>": "part2_0.0_<music21.note.Note G>",\n      "part2_1.0_<music21.note.Note D>": "part2_1.0_<music21.note.Note A>",\n      "part2_2.0_<music21.note.Note E>": "part2_2.0_<music21.note.Note B>",\n      "part2_3.0_<music21.note.Note F>": "part2_3.0_<music21.note.Note C>",\n      "part2_0.0_<music21.note.Note G>": "part2_0.0_<music21.note.Note D>",\n      "part2_1.0_<music21.note.Note A>": "part2_1.0_<music21.note.Note E>",\n      "part2_2.0_<music21.note.Note B>": "part2_2.0_<music21.note.Note F#>",\n      "part2_3.0_<music21.note.Note C>": "part2_3.0_<music21.note.Note G>"\n    }\n  }\n  ```\n\n  - **Counted error types**\n\n  ```python\n  # Syntax highlighting as python because of the need for comments.\n  {\n    "Notes": [\n      {\n        "right": 8,\n        "wrong": 8,\n        "name": "NoteNameResult"\n      }, # example was truncated\n      {\n        "right": 111,\n        "wrong": 17,\n        "name": "NoteTotalResult"\n      }\n    ]\n  }\n  ```\n',
    'author': 'Deepio',
    'author_email': 'global2alex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
