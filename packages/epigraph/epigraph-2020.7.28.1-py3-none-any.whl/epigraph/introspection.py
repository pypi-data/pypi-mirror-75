SCHEMA_QUERY_STR = """{
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
