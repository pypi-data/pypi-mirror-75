# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decode',
 'decode.core',
 'decode.core.array',
 'decode.core.cube',
 'decode.io',
 'decode.logging',
 'decode.models',
 'decode.plot',
 'decode.utils',
 'decode.utils.misc',
 'decode.utils.ndarray']

package_data = \
{'': ['*'], 'decode': ['data/*']}

install_requires = \
['astropy>=4.0,<5.0',
 'matplotlib>=3.2,<4.0',
 'netcdf4>=1.5,<2.0',
 'numpy>=1.18,<2.0',
 'pyyaml>=5.3,<6.0',
 'scikit-learn>=0.22,<0.23',
 'scipy>=1.4,<2.0',
 'tqdm>=4.41,<5.0',
 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'decode',
    'version': '0.5.9',
    'description': 'DESHIMA code for data analysis',
    'long_description': '# De:code\n\n[![PyPI](https://img.shields.io/pypi/v/decode.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/decode/)\n[![Python](https://img.shields.io/pypi/pyversions/decode.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/decode/)\n[![Test](https://img.shields.io/github/workflow/status/deshima-dev/decode/Test?logo=github&label=Test&style=flat-square)](https://github.com/deshima-dev/decode/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3384216-blue?style=flat-square)](https://doi.org/10.5281/zenodo.3384216)\n\n:zap: DESHIMA code for data analysis\n\n## Requirements\n\n- **Python:** 3.6, 3.7, or 3.8 (tested by the author)\n- **Dependencies:** See [pyproject.toml](https://github.com/deshima-dev/decode/pyproject.toml)\n\n## Installation\n\n```shell\n$ pip install decode\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deshima-dev/decode/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
