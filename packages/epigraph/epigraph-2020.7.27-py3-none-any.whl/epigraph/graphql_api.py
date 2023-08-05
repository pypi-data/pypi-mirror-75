"""
A python client to parse the schema from any graphql endpoint.
It allows you to do the following:

- access the schema of any graphql endpoint
  - allowed queries/mutations/subscriptions using
      API.schema.queries, API.schema.mutations, API.schema.subscriptions
  - allowed fields and args for queries/mutations/subscriptions
      API.schema.fetch(<query/mutation/subscription name>)
  - explore fields of type defs
      API.schema.explore(<typedef>)

- query the graphql endpoint with format
    API.query(<query type>, args=<args>).fetch(<list of fields>)

- murate the graphql endpoint with format
    API.mutate(<mutation type>, args=<args>).fetch(<list of fields>)
"""

from graphqlclient import GraphQLClient
import json
from epigraph import schema
from epigraph import utilities

class GraphQLAPI(object):
    """
    Class to parse the schema from any graphql endpoint.
    It allows you to do the following:
    - access the schema of any graphql endpoint
      - allowed queries/mutations/subscriptions
      - allowed fields and args for queries/mutations/subscriptions
      - explore fields of type defs
    - query the graphql endpoint with format
        API.query(<query type>, args=<args>).fetch(<list of fields>)
    - murate the graphql endpoint with format
        API.mutate(<mutation type>, args=<args>).fetch(<list of fields>)

    Parameters
    ==========
    url : str
        url of the graphql endpoint.
    """
    def __init__(self, url):
        self.client = GraphQLClient(url)
        schema_quert_str = """{
          __schema {
            queryType {
              name
              interfaces {
                name
              }
            }
            mutationType{
              name
              interfaces{
                name
              }
            }
            subscriptionType{
              name
              interfaces{
                name
              }
            }
            types {
              name
              kind
              ofType {
                kind
                name
              }
              enumValues {
                name
              }
              fields {
                name
                type{
                  name
                  kind
                  ofType{
                    name
                    kind
                    ofType{
                      name
                      kind
                      ofType{
                        name
                        kind
                      }
                    }
                  }
                }
                args {
                  name
                  defaultValue
                  type {
                    name
                    kind
                    ofType {
                      name
                      kind
                      ofType{
                        name
                        kind
                        ofType{
                          name
                          kind
                        }
                      }
                    }
                  }
                }
              }
              inputFields {
                name
                defaultValue
                type {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType{
                      name
                      kind
                      ofType{
                        name
                        kind
                      }
                    }
                  }
                }
              }
            }
          }
        }"""
        schema_json = json.loads(self.client.execute(schema_quert_str))
        self.schema = schema.Schema(schema_json)

    def query(self, query_type, args={}):
        """
        Method to allow the user to query the graphql endpoint.
        This method needs to be appended with `.fetch()` method. 
        Parameters
        ==========

        query_type: str
            the name of the query you want to make.
        args: dict
            the input args if the query requires them.
        """
        #query_type = inputs.get('query_type')
        assert query_type in self.schema.queries, "Wrong query_type. Choices are: {}".format(self.schema.queries)
        self.query_mutation = query_type
        #args = inputs.get('args')
        if args:
            assert isinstance(args, dict), "Wrong data structure for args: Must be a dictionary"
        if args == {}:
            assert len(list(self.schema.fetch(self.query_mutation)[0].keys())) == 0, "Missing arguments. Choices are: {}".format(list(self.schema.fetch(self.query_mutation)[0].keys()))
        for a in args:
            assert a in self.schema.fetch(self.query_mutation)[0].keys(), "Wrong input argument key '{}'. Choices are: {}".format(a, list(self.schema.fetch(self.query_mutation)[0].keys()))
        self.query_str = "{"
        self.query_str += query_type
        #self.query_str += self.query_mutation
        if len(args)> 0:
            arg_str = utilities.dict_to_arg_str(args)
            arg_str = arg_str.replace("{", '')
            arg_str = arg_str.replace(",{", '')
            arg_str = arg_str.replace("[", '{')
            arg_str = arg_str.replace("]", '')
            self.query_str += arg_str
        self.query_str += "}"
        return self

    def mutate(self, mutation_type, args={}):
        """
        Method to allow the user to do a mutattion at the graphql endpoint.
        This method needs to be appended with `.fetch()` method. 
        Parameters
        ==========

        mutation_type: str
            the name of the mutation you want to make.
        args: dict
            the input args if the mutation requires them.
        """
        assert mutation_type in self.schema.mutations, "Wrong mutation_type. Choices are: {}".format(self.schema.mutations)
        self.query_mutation = mutation_type
        if args:
            assert isinstance(args, dict), "Wrong data structure for args: Must be a dictionary"
        self.query_str = "mutation{"
        self.query_str += mutation_type
        if len(args)> 0:
            query_str = utilities.dict_to_arg_str(args)
            self.query_str += query_str
        self.query_str += "}"
        return self

    def fetch(self, return_struct=None):
        """
        Method to allow the user to complete the query/mutation and execute it at the graphql endpoint.
        This method needs to be called after `.query() or .mutate()` method.
        eg. API.query().fetch() or API.mutate().fetch().

        Parameters
        ==========
        return_struct: list
            list of all the fields you would like to request from the graphql endpoint.
            If `None`, the code tries to figure it out from the schema and returns all fields.
        
        Returns
        =======
        data: dict
            Returned data structure of a query/mutation.
        """
        if self.query_str.endswith('}'):
            self.query_str = self.query_str[:-1]
        if not return_struct:
            return_str = str(self.schema.fetch(self.query_mutation)[1])
            return_str = return_str.replace('[', '')
            return_str = return_str.replace(']', '')
            return_str = return_str.replace(': ', '')
            return_str = return_str.replace(':', '')
            for d in self.schema.default_types:
                return_str = return_str.replace("'{}'".format(d), "")
            return_str = return_str.replace("'", "")
        else:    
            return_str = utilities.dict_to_query_str(return_struct)
            return_str = return_str.replace(":", '')
            return_str = return_str.replace("{", '')
            return_str = return_str.replace(",{", '')
            return_str = return_str.replace("[", '{')
            return_str = return_str.replace("]", '')
            while return_str.count('{') != return_str.count('}'):
                if return_str.count('{') > return_str.count('}'):
                    return_str += '}'
                else:
                    return_str.insert(0, '{')

        self.query_str += return_str
        self.query_str += '}'
        data = json.loads(self.client.execute(self.query_str))
        return data
