# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anansi_market_data_handler']

package_data = \
{'': ['*'], 'anansi_market_data_handler': ['klines/binance_btcusdt_1m.csv']}

install_requires = \
['pandas>=1.0.5,<2.0.0',
 'pendulum>=2.1.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'requests_mock>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'anansi-market-data-handler',
    'version': '0.2.0',
    'description': 'An API to obtain and manipulate market data, which aims to be independent from both market and  broker.',
    'long_description': '# Anansi Market Data Handler\n\nPacote python cujo objetivo é servir como abstração para aquisição,\narmazenamento, leitura e apresentação de dados de mercado, procurando\nser agnóstico quanto à fonte dados[^1].\n\nA ***API*** deste pacote fornece uma interface para os objetos de dados\ncujos *métodos* procuram refletir a necessidade de quem lida,\nusualmente, com dados deste tipo - os **traders** - abstraindo, por\nexemplo, a complexidade matemática da implementação dos indicadores de\nmercado, como médias móveis, bandas de bollinger e afins sobre um\nconjunto de *candlesticks*, por exemplo.\n\n[^1]: Corretoras, *exchanges*, *brokers* são nomenclaturas comuns para\nessas fontes.\n',
    'author': 'Marcus Vintem',
    'author_email': 'marcus@vintem.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcusmello/tradingbots',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
