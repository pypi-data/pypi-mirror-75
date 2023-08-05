# CHIME/FRB API

|  **`Release`**  |   **`Style`**   |   **`Documentation`**   |
|-----------------|-----------------|-------------------------|
| [![PyPI version](https://img.shields.io/pypi/v/epigraph.svg)](https://pypi.org/project/epigraph/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)|[![Documentation: sphinx](https://img.shields.io/badge/documentation-docs-brightgreen)](https://chimefrb.github.io/epigraph/build/html/index.html)|

--------

# epigraph
Automated GraphQL API

### Installation
```
pip install epigraph
```

### Running the API
```python
In [1]: from epigraph import graphql_api

In [2]: API = graphql_api.GraphQLAPI(url="https://swapi.graph.cool/")

In [3]: API.query('Planet').args({'name': "Alderaan"}).fetch(['climate'])
Out[3]: {"data": {"Planet": {"climate": ["temperate"]}}}

```
