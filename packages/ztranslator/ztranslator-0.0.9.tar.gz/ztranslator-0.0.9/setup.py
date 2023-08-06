# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['translator']

package_data = \
{'': ['*']}

install_requires = \
['notify-send>=0.0.13,<0.0.14', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['ztranslator = translator.__main__:main']}

setup_kwargs = {
    'name': 'ztranslator',
    'version': '0.0.9',
    'description': 'Powerful command line translator.',
    'long_description': '# ztranslator\n\nSimples tradutor de linha de comando, com mymemory.translated.net por trás. Você pode configurar uma combinação de teclas de atalho para que execute o ztranslator. Para isso basta passar --notify como parametro, que o ztranslator se encarrega de pegar a última entrada na área de transferência e exibir o texto traduzido em um simpático balãozinho no seu desktop.\n\n![](header.gif)\n\n## Instalação:\n\n```sh\n$ pip install ztranslator\n```\n\n## Exemplos de uso:\n\n#### Na linha de comando:\n\n```sh\n$ ztranslator --help\n```\n\n```sh\n$ python -m translator --help\n```\n\n#### No seu código python:\n\n```python\nIn [1]: from translator import Translator\n\nIn [2]: t = Translator(to_lang=\'pt-br\')\n\nIn [3]: t.translate("Type copyright, credits or license for more information")\nOut[3]: \'Digite copyright, créditos ou licença para mais informações\'\n```\n\n## Configuração para Desenvolvimento\n\n```sh\n$ git clone https://github.com/andreztz/ztranslator.git\n$ cd ztranslator\n$ virtualenv venv\n$ source venv/bin/activate\n$ pip install -e .\n```\n\n## Histórico de lançamento\n\n-   0.0.7 - O primeiro lançamento adequado.\n    -   Trabalho em andamento\n\nAndré Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com\n\n[https://github.com/andreztz/ztranslator](https://github.com/andreztz/)\n\n## Contribua\n\n1. Fork it (<https://github.com/andreztz/ztranslator/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n',
    'author': 'André P. Santos',
    'author_email': 'andreztz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
