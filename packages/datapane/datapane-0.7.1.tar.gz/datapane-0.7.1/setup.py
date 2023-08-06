# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.scripts',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.scaffold',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.report_def': ['samples/*']}

install_requires = \
['PyYAML>=5.3.0,<6.0.0',
 'altair>=4.0.0,<5.0.0',
 'bokeh>=2.0.0,<3.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.0.0,<8.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'dacite>=1.2.0,<2.0.0',
 'flit-core>=2.3.0,<2.4.0',
 'folium>=0.11.0,<0.12.0',
 'furl>=2.1.0,<3.0.0',
 'importlib_resources>=3.0.0,<4.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'lxml>=4.5.2,<5.0.0',
 'matplotlib>=3.1.0,<4.0.0',
 'munch>=2.5.0,<3.0.0',
 'nbconvert>=5.6.1,<6.0.0',
 'numpy>=1.18.0,<2.0.0',
 'packaging>=20.3,<21.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pyarrow>=0.17.0,<0.18.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.20.0,<3.0.0',
 'ruamel.yaml>=0.16.5,<0.17.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toolz>=0.10.0,<0.11.0',
 'validators>=0.16.0,<0.17.0']

extras_require = \
{':python_version >= "3.6.1" and python_version < "3.7.0"': ['dataclasses==0.7']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.7.1',
    'description': 'Datapane client library and CLI tool',
    'long_description': '### Datapane Python Client\n\n![Test [DP CLI]](https://github.com/datapane/datapane-hosted/workflows/Test%20%5BDP%20CLI%5D/badge.svg)\n\n- See https://github.com/datapane/datapane/\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
