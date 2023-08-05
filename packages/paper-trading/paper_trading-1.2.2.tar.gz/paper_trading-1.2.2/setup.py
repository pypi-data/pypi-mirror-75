# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paper_trading',
 'paper_trading.api',
 'paper_trading.app',
 'paper_trading.event',
 'paper_trading.tasks',
 'paper_trading.trade',
 'paper_trading.utility']

package_data = \
{'': ['*'],
 'paper_trading.app': ['static/css/*',
                       'static/font/*',
                       'static/highcharts/*',
                       'static/images/*',
                       'static/js/*',
                       'static/js/charts/easypiechart/*',
                       'static/js/charts/sparkline/*',
                       'static/js/combodate/*',
                       'static/js/data/*',
                       'static/js/datatables/*',
                       'static/js/datepicker/*',
                       'static/js/file-input/*',
                       'static/js/fuelux/*',
                       'static/js/fullcalendar/*',
                       'static/js/ie/*',
                       'static/js/lightbox/*',
                       'static/js/parsley/*',
                       'static/js/slider/*',
                       'templates/*']}

install_requires = \
['APScheduler>=3.6.3,<4.0.0',
 'Flask-Bootstrap>=3.3.7.1,<4.0.0.0',
 'Flask-Login>=0.4.1,<0.5.0',
 'Flask-Mail>=0.9.1,<0.10.0',
 'Flask-Moment>=0.8.0,<0.9.0',
 'Flask-Script>=2.0.6,<3.0.0',
 'Flask-SocketIO>=3.3.2,<4.0.0',
 'Flask>=1.0.2,<2.0.0',
 'flask-blueprint>=1.2.9,<2.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'mpl_finance>=0.10.1,<0.11.0',
 'numpy>=1.16.3,<2.0.0',
 'pandas>=0.24.2,<0.25.0',
 'pymongo>=3.8.0,<4.0.0',
 'pytdx>=1.68,<2.0',
 'requests>=2.21.0,<3.0.0',
 'ta-lib>=0.4.18,<0.5.0',
 'tushare>=1.2.40,<2.0.0']

entry_points = \
{'console_scripts': ['trading = paper_trading.run:main']}

setup_kwargs = {
    'name': 'paper-trading',
    'version': '1.2.2',
    'description': 'creat your own paper trading server',
    'long_description': None,
    'author': 'Michael',
    'author_email': 'cao6237699@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pTraderTeam/paper_trading',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
