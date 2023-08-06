# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastx_barber', 'fastx_barber.scripts']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.77,<2.0',
 'joblib>=0.16.0,<0.17.0',
 'numpy>=1.19.1,<2.0.0',
 'regex>=2020.7.14,<2021.0.0',
 'tqdm>=4.48.1,<5.0.0']

entry_points = \
{'console_scripts': ['fbarber = fastx_barber.scripts.barber:main']}

setup_kwargs = {
    'name': 'fastx-barber',
    'version': '0.0.1',
    'description': 'FASTX trimming tools',
    'long_description': "# fastx-barber\n\nA Python3.6+ package to trim and extract flags from FASTA  and FASTQ files.\n\n## Features\n\n* Supports both FASTA and FASTQ files.\n* Select your reads based on a pattern (regular expression).\n* Trim your reads based on a pattern (regular expression).\n* Extract parts (flags) of reads based on a pattern and store them in the read headers.\n    - Extract the corresponding portions of the quality string too (only for fastq files).\n* All patterns use the `regex` Python package to support [*fuzzy* matching](https://pypi.org/project/regex/#approximate-fuzzy-matching-hg-issue-12-hg-issue-41-hg-issue-109).\n    - Using fuzzy matching might affect the barber's speed).\n* Export reads that do not match the provided pattern.\n* Parallelized processing by splitting the fastx file in chunks.\n* Filter reads based on quality score of extracted flags.\n    - Supports Sanger QSCORE definition (not old Solexa/Illumina one), and allows to specify different PHRED offsets.\n\n## Requirements\n\n`fastx-barber` has been tested with Python 3.6, 3.7, and 3.8. We recommend installing it using `pipx` (see [below](https://github.com/ggirelli/fastx-barber#install)) to avoid dependency conflicts with other packages. The packages it depends on are listed in our [dependency graph](https://github.com/ggirelli/fastx-barber/network/dependencies). We use [`poetry`](https://github.com/python-poetry/poetry) to handle our dependencies.\n\n## Install\n\nWe recommend installing `fastx-barber` using [`pipx`](https://github.com/pipxproject/pipx). Check how to install `pipx` [here](https://github.com/pipxproject/pipx#install-pipx) if you don't have it yet!\n\nOnce you have `pipx` ready on your system, install the latest stable release of `fastx-barber` by running: `pipx install fastx-barber`. If you see the stars (✨ 🌟 ✨), then the installation went well!\n\n## Usage\n\nRun:\n\n* `fbarber` to access the barber's services.\n* `fbarber trim` to trim your reads.\n* `fbarber match` to select reads based on a pattern (regular expression).\n* `fbarber extract` to extract parts of a read and store them in the read name, and then trim it.\n\nAdd `-h` to see the full help page of a command!\n\n## Contributing\n\nWe welcome any contributions to `fastx-barber`. In short, we use [`black`](https://github.com/psf/black) to standardize code format. Any code change also needs to pass `mypy` checks. For more details, please refer to our [contribution guidelines](https://github.com/ggirelli/fastx-barber/blob/master/CONTRIBUTING.md) if this is your first time contributing! Also, check out our [code of conduct](https://github.com/ggirelli/fastx-barber/blob/master/CODE_OF_CONDUCT.md).\n\n## License\n\n`MIT License - Copyright (c) 2020 Gabriele Girelli`\n",
    'author': 'Gabriele Girelli',
    'author_email': 'gigi.ga90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggirelli/fastx-barber',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
