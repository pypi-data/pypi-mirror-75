# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbk', 'tbk.soap']

package_data = \
{'': ['*']}

install_requires = \
['xmlsec>=0.6.1', 'zeep>=3.0.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['typing>=3.6']}

setup_kwargs = {
    'name': 'pancho-tbk',
    'version': '0.3.0',
    'description': 'Unofficial TBK Web Services Python SDK',
    'long_description': "======================================\nUnofficial TBK Web Services Python SDK\n======================================\n\n.. image:: https://circleci.com/gh/cornershop/python-tbk/tree/master.svg?style=svg\n    :target: https://circleci.com/gh/cornershop/python-tbk/tree/master\n\n.. image:: https://badge.fury.io/py/python-tbk.svg\n    :target: https://pypi.org/project/python-tbk/\n\nRequirements\n============\n\n* python: ~2.7, ^3.6\n* libxml2 >= 2.9.1\n* libxmlsec1 >= 1.2.14\n\n----------\n\n🇬🇧\n\nInstallation\n============\n\nJust run::\n\n    $ pip install python-tbk\n\n\nUsage\n=====\n\nAs simple as call (snakecased) webpay api methods::\n\n    >>> from tbk.services import WebpayService\n    >>> from tbk.commerce import Commerce\n    >>> from tbk import INTEGRACION\n    >>> commerce = Commerce(commerce_code, key_data, cert_data, tbk_cert_data, INTEGRACION)\n    >>> webpay = WebpayService(commerce)\n    >>> transaction = webpay.init_transaction(amount, buy_order, return_url, final_url)\n    >>> print(transaction['token'])\n    e87df74f7af4dcfdc1d17521b07413ff9a004a7b423dc47ad09f6a8166a73842\n\n\nConventions\n===========\n\nThis library use a snake cased naming convention for webservices and params for a more pythonic implementation. Every camelcased name in the webpay API was transformed to snakecase::\n\n    initTransaction(amount, buyOrder, returnURL, finalURL, sessionId)\n\nbecame::\n\n    init_transaction(amount, buy_order, return_url, final_url, session_id)\n\n\nOneclick Mall Service\n=====================\n\nA list of :code:`tbk.services.StoreInput` input is expected as :code:`wsOneClickMulticodeStorePaymentInput` for :code:`stores_input` parameter on :code:`authorize` method.\n\nDocumentation\n=============\n\nYou can refer to http://www.transbankdevelopers.cl/?m=api for official API documentation. This library documentation is on the way.\n\n\nLoggers\n=======\n\nThere are two levels of loggers::\n\n    tbk.services\n    tbk.soap\n\nSpecific service logger are defined by class name::\n\n    tbk.services.WebpayService\n\n\nBugs?\n=====\n\nIssues are welcome at https://github.com/cornershop/python-tbk/issues\n\n\n🇪🇸\n\nInstalación\n===========\n\nEjecuta::\n\n    $ pip install python-tbk\n\n\nUso\n===\n\nTan simple como llamar los métodos del API de Webpay (pero snakecased)::\n\n    >>> from tbk.services import WebpayService\n    >>> from tbk.commerce import Commerce\n    >>> from tbk import INTEGRACION\n    >>> commerce = Commerce(commerce_code, key_data, cert_data, tbk_cert_data, INTEGRACION)\n    >>> webpay = WebpayService(commerce)\n    >>> transaction = webpay.init_transaction(amount, buy_order, return_url, final_url)\n    >>> print(transaction['token'])\n    e87df74f7af4dcfdc1d17521b07413ff9a004a7b423dc47ad09f6a8166a73842\n\n\nConvenciones\n============\n\nLa librería usa una convención de nombres snakecased para ser más pythonica. Cada nombre camelcased en el API de Webpay se transformó a snakecased::\n\n    initTransaction(amount, buyOrder, returnURL, finalURL, sessionId)\n\nse traduce en::\n\n    init_transaction(amount, buy_order, return_url, final_url, session_id)\n\n\nServicio Oneclick Mall\n======================\n\nEl método :code:`authorize` espera una lista de :code:`tbk.services.StoreInput` en el parámetro :code:`stores_input` que se corresponde con la definición de :code:`wsOneClickMulticodeStorePaymentInput`.\n\n\nDocumentación\n=============\n\nLa documentación oficial se encuentra disponible en http://www.transbankdevelopers.cl/?m=api. La documentación de esta librería está en desarrollo.\n\n\nLoggers\n=======\n\nSe encuentran definidos dos niveles de logger::\n\n    tbk.services\n    tbk.soap\n\nEl logger específico de un servicio está definido por su nombre de clase::\n\n    tbk.services.WebpayService\n\n\n\n----------\n\n\nTesting cards / Tarjetas de prueba\n==================================\n\nCredit / Crédito\n\n+----------------+------------------+------------------+\n| Marca          | VISA             | MASTERCARD       |\n+================+==================+==================+\n| No de Tarjeta  | 4051885600446623 | 5186059559590568 |\n+----------------+------------------+------------------+\n| Año Expiración | Cualquiera       | Cualquiera       |\n+----------------+------------------+------------------+\n| CVV            | 123              | 123              |\n+----------------+------------------+------------------+\n| Resultado      | APROBADO         | RECHAZADO        |\n+----------------+------------------+------------------+\n\nDebit / Débito\n\n+----------+------------------+------------------+\n|          | APRUEBA          | RECHAZA          |\n+==========+==================+==================+\n| TARJETA  | 4051885600446620 | 5186059559590560 |\n+----------+------------------+------------------+\n| RUT      | 11.111.111-1     | 11.111.111-1     |\n+----------+------------------+------------------+\n| PASSWORD | 123              | 123              |\n+----------+------------------+------------------+\n",
    'author': 'Cornershop',
    'author_email': 'tech@cornershopapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cornershop/python-tbk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
