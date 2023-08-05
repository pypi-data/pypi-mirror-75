# epigraph
Automated GraphQL API

###Installation
```
pip install epigraph
```

###Running the API
```python
In [1]: from epigraph import graphql_api

In [2]: API = graphql_api.GraphQLAPI(url="https://swapi.graph.cool/")

In [3]: API.query('Planet', args={'name': "Earth"}).fetch(['climate'])
Out[3]: {'data': {'Planet': None}}

```
