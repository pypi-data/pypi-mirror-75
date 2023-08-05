from epigraph import graphql_api

API = graphql_api.GraphQLAPI(url="https://swapi.graph.cool/")


def test_schema():
    response = API.schema.queries
    assert "Planet" in response
    response = API.schema.mutations
    assert "createPlanet" in response
    response = API.schema.subscriptions
    assert "Planet" in response
    response = API.schema.fetch("Planet")
    assert "name" in response[0]
    assert "climate" in response[1]
    response = API.schema.explore("FilmcharactersPerson")
    assert "birthYear" in response
    assert "eyeColor" in response
    assert "homeworld" in response


def test_query():
    args = {"name": "Alderaan"}
    payload = ["climate"]
    response = API.query("Planet").args(args).fetch(payload)
    assert response == {"data": {"Planet": {"climate": ["temperate"]}}}


def test_mutations():
    args = {"name": "Earth"}
    payload = ["name"]
    response = API.mutate("createPlanet").args(args).fetch(payload)
    assert response["data"] is not None
    if response["data"]:
        assert "createPlanet" in response["data"]
