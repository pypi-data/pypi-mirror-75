def create_nodes(entity, csv_file_path):
    queries = []

    query = "USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///" + csv_file_path + "\" AS row "
    node_properties = entity["properties"]
    prop_string = " {"

    for idx, prop in enumerate(node_properties):
        prop_string += prop + ": row." + prop
        if idx < len(node_properties) - 1:
            prop_string += ", "
        else:
            prop_string += "}"

    query += "CREATE (:" + entity["entityType"] + prop_string + ");"
    queries.append(query)
    
    for index in entity["indices"]:
        query = "CREATE INDEX ON :" + entity["entityType"] + "(" + index+ ");"
        queries.append(query)

    
    return queries


def create_edges(entity, csv_file_path):
    queries = []

    query = "USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///" + csv_file_path + "\" AS row "
    query += "MATCH (from:" + entity["fromNodeType"] + " {" + entity["fromNodeKey"] + ": row." + entity["fromNodeKey"] +  "}) "
    query += "MATCH (to:" + entity["toNodeType"] + " {" + entity["toNodeKey"] + ": row." + entity["toNodeKey"] + "}) "

    query += "MERGE (from)-[e:" + entity["entityType"] + "]->(to) "

    query += "ON CREATE SET"

    for prop in entity["properties"]:
        if is_numeric(entity, prop):
            query += " e." + prop + " = toFloat(row." + prop + ")"
        else:
            query += " e." + prop + " = row." + prop
        
    query += ";"

    queries.append(query)
    return queries


def is_numeric(entity, prop):
    return prop in entity["numeric"]