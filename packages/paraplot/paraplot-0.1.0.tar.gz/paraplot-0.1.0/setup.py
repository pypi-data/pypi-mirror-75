# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paraplot']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.17.0,<8.0.0',
 'flask>=1.1.2,<2.0.0',
 'json_minify>=0.3.0,<0.4.0',
 'matplotlib>=3.3.0,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'paraplot',
    'version': '0.1.0',
    'description': 'Parameter retrieval and plotting',
    'long_description': '# paraplot\n\n[![Build Status](https://travis-ci.com/cruisen/paraplot.svg?branch=master)](https://travis-ci.com/cruisen/paraplot)\n[![Coverage](https://coveralls.io/repos/github/cruisen/paraplot/badge.svg?branch=master)](https://coveralls.io/github/cruisen/paraplot?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/paraplot.svg)](https://pypi.org/project/paraplot/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nParameter retrieval and plotting\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install paraplot\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom paraplot.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[MIT](https://github.com/cruisen/paraplot/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [69435b231f7f398474073ac6dd14868dd3edf2c1](https://github.com/wemake-services/wemake-python-package/tree/69435b231f7f398474073ac6dd14868dd3edf2c1). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/69435b231f7f398474073ac6dd14868dd3edf2c1...master) since then.\n',
    'author': 'Nikolai von Krusenstiern',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cruisen/paraplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
