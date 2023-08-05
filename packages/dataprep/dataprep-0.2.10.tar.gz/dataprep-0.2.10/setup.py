# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataprep',
 'dataprep.assets',
 'dataprep.data_connector',
 'dataprep.eda',
 'dataprep.eda.basic',
 'dataprep.eda.correlation',
 'dataprep.eda.create_report',
 'dataprep.eda.missing',
 'dataprep.eda.outlier',
 'dataprep.tests',
 'dataprep.tests.data_connector',
 'dataprep.tests.eda']

package_data = \
{'': ['*'], 'dataprep.eda.create_report': ['templates/*']}

install_requires = \
['bokeh>=2.0,<2.1',
 'dask[complete]>=2.13,<2.14',
 'holoviews>=1.13,<1.14',
 'jinja2>=2.11,<2.12',
 'jsonpath-ng>=1.5.1,<2.0.0',
 'jsonschema>=3.2,<3.3',
 'lxml>=4.5,<4.6',
 'nltk>=3.5,<4.0',
 'numpy>=1.18,<1.19',
 'pandas>=1.0,<1.1',
 'pillow>=7.1.2,<8.0.0',
 'requests>=2.23,<2.24',
 'scipy>=1.4,<1.5',
 'tornado==5.0.2',
 'tqdm>=4.47.0,<5.0.0',
 'wordcloud>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'dataprep',
    'version': '0.2.10',
    'description': 'Dataprep: Data Preparation in Python',
    'long_description': '<div align="center"><img width="100%" src="https://github.com/sfu-db/dataprep/raw/develop/assets/logo.png"/></div>\n\n-----------------\n\n[![License]](LICENSE) [![Doc Badge]](https://sfu-db.github.io/dataprep/) [![Version]](https://pypi.org/project/dataprep/) [![Python Version]](https://pypi.org/project/dataprep/)  [![Downloads]](https://pepy.tech/project/dataprep) [![Codecov]](https://codecov.io/gh/sfu-db/dataprep) ![Build Status]  [![Chat]](https://discord.gg/xwbkFNk) \n\nDataprep lets you prepare your data using a single library with a few lines of code.\n\nCurrently, you can use `dataprep` to:\n* Collect data from common data sources (through `dataprep.data_connector`)\n* Do your exploratory data analysis (through `dataprep.eda`)\n* ...more modules are coming\n\n\n[Documentation] | [Mail List & Forum] \n\n## Installation\n\n```bash\npip install dataprep\n```\n\n## Examples & Usages\n\nThe following examples can give you an impression of what dataprep can do:\n\n* [Documentation: Data Connector](https://sfu-db.github.io/dataprep/data_connector.html)\n* [Documentation: EDA](https://sfu-db.github.io/dataprep/eda/introduction.html)\n* [EDA Case Study: Titanic](https://sfu-db.github.io/dataprep/case_study/titanic.html)\n* [EDA Case Study: House Price](https://sfu-db.github.io/dataprep/case_study/house_price.html)\n\n### EDA\n\nThere are common tasks during the exploratory data analysis stage, \nlike a quick look at the columnar distribution, or understanding the correlations\nbetween columns. \n\nThe EDA module categorizes these EDA tasks into functions helping you finish EDA\ntasks with a single function call.\n\n* Want to understand the distributions for each DataFrame column? Use `plot`.\n\n<a href="https://sfu-db.github.io/dataprep/eda/introduction.html#analyzing-basic-characteristics-via-plot"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot(df).gif"/></a>\n\n* Want to understand the correlation between columns? Use `plot_correlation`.\n\n<a href="https://sfu-db.github.io/dataprep/eda/introduction.html#analyzing-correlation-via-plot-correlation"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot_correlation(df).gif"/></a>\n\n* Or, if you want to understand the impact of the missing values for each column, use `plot_missing`.\n\n<a href="https://sfu-db.github.io/dataprep/eda/plot_missing.html#plotting-the-position-of-missing-values-via-plot-missing-df"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot_missing(df).gif"/></a>\n\nYou can drill down to get more information by given `plot`, `plot_correlation` and `plot_missing` a column name.: E.g. for `plot_missing`\n\n<a href="https://sfu-db.github.io/dataprep/eda/plot_missing.html#the-impact-on-basic-characteristics-of-missing-values-in-column-x-via-plot-missing-df-x"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot_missing(df, x).gif"/></a>\n\n&nbsp;&nbsp;&nbsp;&nbsp;for numerical column using`plot`:\n\n<a href="https://sfu-db.github.io/dataprep/eda/plot.html#zooming-into-a-column-via-plot-df-x"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot(df,x)_num.gif"/></a>\n\n&nbsp;&nbsp;&nbsp;&nbsp;for categorical column using`plot`:\n\n<a href="https://sfu-db.github.io/dataprep/eda/plot.html#zooming-into-a-column-via-plot-df-x"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/plot(df,x)_cat.gif"/></a>\n\nDon\'t forget to checkout the [examples] folder for detailed demonstration!\n\n### Data Connector\n\nYou can download Yelp business search result into a pandas DataFrame, \nusing two lines of code, without taking deep looking into the Yelp documentation!\nMoreover, Data Connector will automatically do the pagination for you so that \nyou can specify the desire count of the returned results without even considering the count-per-request restriction from the API.\n\n<a href="https://sfu-db.github.io/dataprep/data_connector.html#getting-web-data-with-connector-query"><img src="https://github.com/sfu-db/dataprep/raw/develop/assets/data_connector.png"/></a>\n\n_The code requests 120 records even though Yelp restricts you can only fetch 50 per request._\n\n## Contribute\n\nThere are many ways to contribute to Dataprep.\n\n* Submit bugs and help us verify fixes as they are checked in.\n* Review the source code changes.\n* Engage with other Dataprep users and developers on StackOverflow.\n* Help each other in the [Dataprep Community Discord](https://discord.gg/xwbkFNk) and [Mail list & Forum].\n* [![Twitter]](https://twitter.com/sfu_db)\n* Contribute bug fixes.\n* Providing use cases and writing down your user experience.\n\nPlease take a look at our [wiki] for development documentations!\n\n\n[Build Status]: https://img.shields.io/circleci/build/github/sfu-db/dataprep/master?style=flat-square&token=f68e38757f5c98771f46d1c7e700f285a0b9784d\n[Documentation]: https://sfu-db.github.io/dataprep/\n[Mail list & Forum]: https://groups.google.com/forum/#!forum/dataprep\n[wiki]: https://github.com/sfu-db/dataprep/wiki\n[examples]: https://github.com/sfu-db/dataprep/tree/master/examples\n[Chat]: https://img.shields.io/discord/702765817154109472?style=flat-square\n[License]: https://img.shields.io/pypi/l/dataprep?style=flat-square\n[Downloads]: https://pepy.tech/badge/dataprep\n[Python Version]: https://img.shields.io/pypi/pyversions/dataprep?style=flat-square\n[Version]: https://img.shields.io/pypi/v/dataprep?style=flat-square\n[Codecov]: https://img.shields.io/codecov/c/github/sfu-db/dataprep?style=flat-square\n[Twitter]: https://img.shields.io/twitter/follow/sfu_db?style=social\n[Doc Badge]: https://img.shields.io/badge/dynamic/json?color=blue&label=docs&prefix=v&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdataprep%2Fjson&style=flat-square\n',
    'author': 'SFU Database System Lab',
    'author_email': 'dsl.cs.sfu@gmail.com',
    'maintainer': 'Weiyuan Wu',
    'maintainer_email': 'youngw@sfu.com',
    'url': 'https://github.com/sfu-db/dataprep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
