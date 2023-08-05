# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wkcuber',
 'wkcuber.api',
 'wkcuber.api.Properties',
 'wkcuber.api.TiffData',
 'wkcuber.vendor']

package_data = \
{'': ['*']}

install_requires = \
['cluster_tools==1.49',
 'natsort>=6.2.0,<7.0.0',
 'nibabel>=2.5.1,<3.0.0',
 'numpy>=1.17.4,<2.0.0',
 'pillow>=6.2.1,<7.0.0',
 'psutil>=5.6.7,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'scipy>=1.4.0,<2.0.0',
 'wkw==0.1.2']

setup_kwargs = {
    'name': 'wkcuber',
    'version': '0.2.62',
    'description': 'A cubing tool for webKnossos',
    'long_description': None,
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
