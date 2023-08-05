import copy


class BaseType(object):
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name


class Types(object):
    def __init__(self, kind, name, ofType):
        self.kind = kind
        self.name = name
        self.ofType = None
        if ofType:
            self.ofType = BaseType(ofType["kind"], ofType["name"])


class Field(object):
    def __init__(self, name, field_type, args):
        self.name = name
        self.type = Types(field_type["kind"], field_type["name"], field_type["ofType"])
        self.args = []
        for a in args:
            self.args.append(Args(a["name"], a["defaultValue"], a["type"]))


class Args(object):
    def __init__(self, name, default_value, arg_type):
        self.name = name
        self.default_value = default_value
        self.type = Types(arg_type["kind"], arg_type["name"], arg_type["ofType"])


class RootTypes(object):
    def __init__(self, kind, name, ofType, fields):
        self.kind = kind
        self.name = name
        self.ofType = None
        if ofType:
            self.ofType = BaseType(ofType["kind"], ofType["name"])
        self.fields = []
        if fields:
            for f in fields:
                self.fields.append(Field(f["name"], f["type"], f["args"]))


class Schema(object):
    """
    Parses the schema of the graphql endpoint.
    returns all queries, mutations and subscriptions allowed by the graphql endpoint.
    Allows you to fetch any type and see it's underlying fields.

    Parameters
    ==========
    schema_json: parsed json data
        schema from the graphwl endpoint.
    """

    def __init__(self, schema_json):
        self.default_types = [
            "String",
            "Int",
            "Float",
            "Boolean",
            "DateTime",
            "ID",
            "Enum",
            "__Schema",
            "__Type",
            "__TypeKind",
            "__Field",
            "__InputValue",
            "__EnumValue",
            "__Directive",
            "__DirectiveLocation",
        ]
        self.type_map = {
            "INPUT_OBJECT": [dict],
            "OBJECT": [dict],
            "SCALAR": [int, float, bool, str],
        }
        self.__parse_schema(schema_json)

    def __parse_schema(self, schema):
        """
        Parses the schema and extracts query, mutation and subscription types.
        Parameters
        ==========
        schema: json
            loaded json schema from the graphql endpoint.
        """
        self.query_type = schema["data"]["__schema"]["queryType"]
        self.query_interfaces = self.query_type["interfaces"]
        self.mutation_type = schema["data"]["__schema"]["mutationType"]
        self.subscription_type = schema["data"]["__schema"]["subscriptionType"]
        self.all_types = schema["data"]["__schema"]["types"]
        queries = []
        mutations = []
        subscriptions = []
        for s in self.all_types:
            if self.query_type and s["name"] == self.query_type["name"]:
                queries.append(
                    RootTypes(s["kind"], s["name"], s["ofType"], s["fields"])
                )
            if self.mutation_type and s["name"] == self.mutation_type["name"]:
                mutations.append(
                    RootTypes(s["kind"], s["name"], s["ofType"], s["fields"])
                )
            if self.subscription_type and s["name"] == self.subscription_type["name"]:
                subscriptions.append(
                    RootTypes(s["kind"], s["name"], s["ofType"], s["fields"])
                )
        self.queries = []
        for r in queries:
            for f in r.fields:
                self.queries.append(f.name)
        self.mutations = []
        for r in mutations:
            for f in r.fields:
                self.mutations.append(f.name)
        self.subscriptions = []
        for r in subscriptions:
            for f in r.fields:
                self.subscriptions.append(f.name)

    def fetch(self, fetch_type):
        """
        Fetches the arguments and return types for a query, mutation, subscription type.

        Parameters
        ==========
        fetch_type: str
        
        Returns
        =======
            tuple of (arguments, fields).
        """
        assert (
            fetch_type in self.queries + self.mutations + self.subscriptions
        ), "Wrong input type. Choices are: \nQueries: {}\nMutations: {}\n Subscriptions:{}\n".format(
            self.queries, self.mutations, self.subscriptions
        )
        if fetch_type in self.queries:
            base_type = self.query_type["name"]
            return self.__fetch(base_type, fetch_type)
        if fetch_type in self.mutations:
            base_type = self.mutation_type["name"]
            return self.__fetch(base_type, fetch_type)
        if fetch_type in self.subscriptions:
            base_type = self.subscription_type["name"]
            return self.__fetch(base_type, fetch_type)

    def explore(self, fetch_type):
        """
        Explores the fields of any typedef.

        Parameters
        ==========
        fetch_type: str
            typedef you want to explore.
        
        Returns
        =======
        dict of fields for the typedef.
        """
        if fetch_type in self.queries + self.mutations + self.subscriptions:
            return self.fetch(fetch_type)

        return self.__explore_struct(fetch_type)

    def __explore_struct(self, base_type):
        """
        Helper method to explore the typedef.

        Parameters
        ==========
        base_type: str
            typedef you want to explore.
        
        Returns
        =======
        dict of fields for the typedef.
        """
        return_type = {}
        for t in self.all_types:
            if t["name"] == base_type:
                if t["fields"]:
                    for f in t["fields"]:
                        name_to_check = f["type"]["name"]
                        check = f["type"]
                        islist = False
                        if check["kind"] in ["LIST"]:
                            islist = True
                        while name_to_check is None:
                            if check["kind"] in ["LIST"]:
                                islist = True
                            name_to_check = check["ofType"]["name"]
                            check = check["ofType"]
                        if islist:
                            name_to_check = [name_to_check]
                        return_type[f["name"]] = name_to_check
                if t["inputFields"]:
                    for f in t["inputFields"]:
                        name_to_check = f["type"]["name"]
                        check = f["type"]
                        islist = False
                        if check["kind"] in ["LIST"]:
                            islist = True
                        while name_to_check is None:
                            if check["kind"] in ["LIST"]:
                                islist = True
                            name_to_check = check["ofType"]["name"]
                            check = check["ofType"]
                        if islist:
                            name_to_check = [name_to_check]
                        return_type[f["name"]] = name_to_check
                if t["enumValues"]:
                    # struct[c] = 'Enum'
                    enums = []
                    for f in t["enumValues"]:
                        enums.append(f["name"])
                    return_type = enums
        return return_type

    def __fetch(self, base_type, fetch_type):
        """
        Fetches the arguments and fields of requested query/mutation/schema.
        
        Parameters
        ==========
        base_type: str
            name of the base query/mutation/schema.
        fetch_type: str
            query/mutation/scubscription that needs to be fetch.

        Returns
        =======
        args: dict
            Arguments that the fetch type needs
            eg.
            query{
              Planet(args){
                climate
              }
            }
        return_type: dict
            Return types that the fetch type needs.
            eg.
            query{
              Planet(name: "Earth"){
                return_type
              }
            }

        """
        return_type = None
        args = None
        for t in self.all_types:
            if t["name"] == base_type:
                for f in t["fields"]:
                    if fetch_type == f["name"]:
                        if f["type"]["kind"] in ["LIST", "NON_NULL"]:
                            return_type = [
                                self.__fetch_return_type(f["type"]["ofType"])
                            ]
                        else:
                            return_type = self.__fetch_return_type(
                                {"kind": f["type"]["kind"], "name": f["type"]["name"]}
                            )
                        args = self.__fetch_args(f["args"])

        return args, return_type

    def __fetch_args(self, args):
        """
        Helper method to fetch the args of a query/mutation/subscription type.
        
        Parameters
        ==========
        args: dict

        Returns
        =======
        args: dict
            nicely formated
            {name: type}
        """
        if args == []:
            return
        outer_struct = {}
        for a in args:
            if a["type"]["name"] in self.default_types:
                outer_struct[a["name"]] = a["type"]["name"]
                continue
            struct = {}
            name_to_check = a["type"]["name"]
            check = a["type"]
            while name_to_check is None:
                name_to_check = check["ofType"]["name"]
                check = check["ofType"]
            to_check = [check["name"]]
            return_type = check["name"]
            check = to_check
            checked = []
            while len(check):
                for c in to_check:
                    checked.append(c)
                    if c in self.default_types:
                        struct[return_type] = c
                        check.remove(c)
                        check = list(set(check))
                        continue
                    for t in self.all_types:
                        if t["name"] == c:
                            dstruct = {}
                            if t["fields"]:
                                for f in t["fields"]:
                                    further, value = self.__explore_further(f)
                                    if further:
                                        if isinstance(value, list):
                                            if value[0] not in checked:
                                                check.append(value[0])
                                        else:
                                            if value not in checked:
                                                check.append(value)
                                        dstruct[f["name"]] = value
                                    else:
                                        dstruct[f["name"]] = value
                                    struct[c] = dstruct
                            if t["inputFields"]:
                                for f in t["inputFields"]:
                                    further, value = self.__explore_further(f)
                                    if further:
                                        if isinstance(value, list):
                                            if value[0] not in checked:
                                                check.append(value[0])
                                        else:
                                            if value not in checked:
                                                check.append(value)
                                        dstruct[f["name"]] = value
                                    else:
                                        dstruct[f["name"]] = value
                                    struct[c] = dstruct
                            if t["enumValues"]:
                                # struct[c] = 'Enum'
                                struct[c] = []
                                for f in t["enumValues"]:
                                    struct[c].append(f["name"])
                    if c in check:
                        check.remove(c)
                    check = list(set(check))
                to_check = check
            reduced_struct = copy.deepcopy(struct)
            while len(reduced_struct) > 0:
                to_check = list(reduced_struct.keys())
                for c in to_check:
                    if isinstance(struct[c], dict):
                        for k in struct[c].keys():
                            if isinstance(struct[c][k], list):
                                if struct[c][k][0] in struct:
                                    struct[c][k][0] = struct[struct[c][k][0]]
                                    # break
                            else:
                                if struct[c][k] in struct:
                                    struct[c][k] = struct[struct[c][k]]
                                    # break
                    del reduced_struct[c]
            outer_struct[a["name"]] = struct[return_type]
        return outer_struct

    def __fetch_return_type(self, return_type):
        """
        Helper method to fetch the fields of a query/mutation/subscription type.
        
        Parameters
        ==========
        return_type: dict

        Returns
        =======
        return_type: dict
            nicely formated
            {name: type}
        """
        if return_type["name"] in self.default_types:
            return return_type["name"]
        struct = {}
        name_to_check = return_type["name"]
        check = return_type
        while name_to_check is None:
            name_to_check = check["ofType"]["name"]
            check = check["ofType"]
        to_check = [check["name"]]
        return_type = check["name"]
        check = to_check
        checked = []
        while len(check):
            for c in to_check:
                checked.append(c)
                if c in self.default_types:
                    struct[return_type] = c
                    check.remove(c)
                    check = list(set(check))
                    continue
                for t in self.all_types:
                    if t["name"] == c:
                        dstruct = {}
                        if t["fields"]:
                            for f in t["fields"]:
                                further, value = self.__explore_further(f)
                                if further:
                                    if isinstance(value, list):
                                        if value[0] not in checked:
                                            check.append(value[0])
                                    else:
                                        if value not in checked:
                                            check.append(value)
                                    dstruct[f["name"]] = value
                                else:
                                    dstruct[f["name"]] = value
                                struct[c] = dstruct
                        if t["enumValues"]:
                            struct[c] = "Enum"
                if c in check:
                    check.remove(c)
                check = list(set(check))
            to_check = check
        reduced_struct = copy.deepcopy(struct)
        while len(reduced_struct) > 0:
            to_check = list(reduced_struct.keys())
            for c in to_check:
                if isinstance(struct[c], dict):
                    for k in struct[c].keys():
                        if isinstance(struct[c][k], list):
                            if struct[c][k][0] in struct:
                                struct[c][k][0] = struct[struct[c][k][0]]
                        else:
                            if struct[c][k] in struct:
                                struct[c][k] = struct[struct[c][k]]
                del reduced_struct[c]
        return struct[return_type]

    def __explore_further(self, field):
        """
        Helper method to determine if the field needs to be explored further
        in case it is a nested field with internal data structures.

        Parameters
        ==========
        field: dict
            check if this field needs to be explored

        Return
        ======
        bool, name : whether the field needs to be explored further and the name of the field.
        """
        name_to_check = field["type"]["name"]
        check = field["type"]
        return_type = None
        if check["kind"] == "LIST":
            return_type = "LIST"
        elif check["kind"] == "ENUM":
            return_type = "ENUM"
        while name_to_check is None:
            name_to_check = check["ofType"]["name"]
            if check["kind"] == "LIST":
                return_type = "LIST"
            elif check["kind"] == "ENUM":
                return_type = "ENUM"
            check = check["ofType"]
        if return_type == "LIST":
            if check["name"] not in self.default_types:
                return True, [check["name"]]
            else:
                return False, [check["name"]]
        elif return_type == "ENUM":
            return False, "Enum"
        elif field["type"]["kind"] in ["INPUT_OBJECT", "OBJECT"]:
            return True, check["name"]
        else:
            return False, check["name"]
