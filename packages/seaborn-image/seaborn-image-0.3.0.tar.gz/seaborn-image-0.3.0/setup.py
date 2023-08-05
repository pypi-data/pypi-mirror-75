# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seaborn_image']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib-scalebar>=0.6.2,<0.7.0',
 'matplotlib>=3.2.2,<4.0.0',
 'palettable>=3.3.0,<4.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scipy>=1.5.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'seaborn-image',
    'version': '0.3.0',
    'description': 'seaborn-image: image data visualization and processing like seaborrn using matplotlib, scipy and scikit-image',
    'long_description': '# seaborn-image: image data visualization\n\n[![Tests](https://github.com/SarthakJariwala/seaborn-image/workflows/Tests/badge.svg)](https://github.com/SarthakJariwala/seaborn-image/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/SarthakJariwala/seaborn-image/branch/master/graph/badge.svg)](https://codecov.io/gh/SarthakJariwala/seaborn-image)\n[![PyPI](https://img.shields.io/pypi/v/seaborn-image.svg)](https://pypi.org/project/seaborn-image/)\n[![Documentation Status](https://readthedocs.org/projects/seaborn-image/badge/?version=latest)](https://seaborn-image.readthedocs.io/en/latest/?badge=latest)\n\n<div class="row">\n\n  <a>\n  <img src="./examples/image_0.png" height="180" width="200">\n  </a>\n\n  <a>\n  <img src="./examples/image_1.png" height="180" width="200">\n  </a>\n\n  <a>\n  <img src="./examples/image_3.png" height="165" width="400">\n  </a>\n\n</div>\n\n<div class="row">\n  \n  <a>\n  <img src="./examples/image_5.png" height="250" width="375">\n  </a>\n\n</div>\n\n<div class="row">\n\n  <a>\n  <img src="./examples/image_4.png" height="600" width="600">\n  </a>\n\n</div>\n\nSeaborn-like image data visualization using matplotlib, scikit-image and scipy.\n\n## Description\n\nSeaborn-image is a seaborn like python **image** visualization and processing library\nbased on matplotlib, scipy and scikit-image.\n\nThe aim of seaborn-image is to provide a high-level API to **process and plot attractive images quickly and effectively**.\n\n\n## Installation\n\n```bash\npip install seaborn-image\n```\n\n## Usage\n### Simple usage\n\n```python\n\nimport seaborn_image as isns\n\n"""Plot image"""\nisns.imgplot(data)\n\n"""Plot image with scalebar"""\nisns.imgplot(data, dx=0.01, units="um")\n\n"""Add colorbar label"""\nisns.imgplot(data, dx=0.01, units="um", cbar_label="Height (nm)")\n```\n<a>\n<img src="./examples/image_0.png" height="275" width="300">\n</a>\n\n### Plot image with a histogram\n\n```python\nimport seaborn_image as isns\n\nisns.imghist(data, dx=150, units="nm", cbar_label="Height (nm)", cmap="ice")\n```\n\n<a>\n<img src="./examples/image_5.png" height="300" width="450">\n</a>\n\n### Set context like seaborn\n\n```python\n\nimport seaborn_image as isns\n\nisns.set_context("notebook") # Other options include paper, talk, presentation, poster\n```\n\n### Apply image filters (from scipy and skimage) and plot\n\n```python\n\nimport seaborn_image as isns\n\nisns.filterplot(data, filter="gaussian", sigma=5, cbar_label="Height (nm)")\n```\n\n<a>\n<img src="./examples/image_3.png" height="260" width="600">\n</a>\n\n## Documentation\n\nCheck out the docs [here](https://seaborn-image.readthedocs.io/)\n',
    'author': 'Sarthak Jariwala',
    'author_email': 'jariwala@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SarthakJariwala/seaborn-image',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
