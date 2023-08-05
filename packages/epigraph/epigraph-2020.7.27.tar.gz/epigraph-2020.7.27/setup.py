# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epigraph']

package_data = \
{'': ['*']}

install_requires = \
['graphqlclient>=0.2,<0.3']

setup_kwargs = {
    'name': 'epigraph',
    'version': '2020.7.27',
    'description': 'Python API for graphql',
    'long_description': '# epigraph\nAutomated GraphQL API\n\n###Installation\n```\npip install epigraph\n```\n\n###Running the API\n```python\nIn [1]: from epigraph import graphql_api\n\nIn [2]: API = graphql_api.GraphQLAPI(url="https://swapi.graph.cool/")\n\nIn [3]: API.query(\'Planet\', args={\'name\': "Earth"}).fetch([\'climate\'])\nOut[3]: {\'data\': {\'Planet\': None}}\n\n```\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/epigraph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
