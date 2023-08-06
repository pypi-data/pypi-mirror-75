import os, os.path
import json
from neo4j import GraphDatabase

import autoneo.exporter as exporter, autoneo.query_builder as query_builder

def build(config_file, data_directory, query_directory, csv_directory):
    """
    Builds a graph database in Neo4j according to the config file provided. If needed,
    the tool will attempt to export node/edge data from the proper data dump using the corresponding
    query into a CSV format and then load the data from CSV into Neo4j.

    Data directory - path to the directory containing data dumps (the config file must specify what kind of database)
    Query directory - path to directory containing queries for extracting data from data dumps
    CSV directory - path to directory containing CSVs (CSV files produced by the build will be stored here as well)
    """
    with open(config_file) as cf:
        config = json.load(open(config_file))

        nodes = config["nodes"]
        edges = config["edges"]

        graph_bolt_url = input("Neo4j BOLT URL: ") # e.g., bolt://localhost:7687"
        user_name = input("Neo4j username: ") # e.g., neo4j
        password = input("Neo4j password: ") # e.g., admin
        credentials = [graph_bolt_url, user_name, password]

        for node in nodes:
            load_db(node, data_directory, query_directory, csv_directory, credentials, isNode=True)

        for edge in edges:
            load_db(edge, data_directory, query_directory, csv_directory, credentials, isNode=False)



def export_db_csv(db_type, db_path, query_file_path, csv_file_path):
    if db_type == "sqllite3":
        return exporter.handle_sqlite3(db_path, query_file_path, csv_file_path)
    elif db_type == "annotation":
        return exporter.handle_annotations(db_path, csv_file_path)
    else:
        return None



def load_db(config_entity, data_directory, query_directory, csv_directory, credentials, isNode):
    print("Processing " + config_entity["entityType"])

    db_type = config_entity["dataSource"]["dbType"]
    csv_file_path = os.path.join(csv_directory, config_entity["dataSource"]["csvFile"])

    if db_type != "csv":
        print("Exporting CSV for " + config_entity["entityType"])

        db_file_path = os.path.join(data_directory, config_entity["dataSource"]["dbFile"])
        query_file_path = os.path.join(query_directory, config_entity["dataSource"]["queryFile"])

        export_db_csv(db_type, db_file_path, query_file_path, csv_file_path)

    build_run_queries(config_entity, csv_file_path, credentials, isNode)



def build_run_queries(config_entity, csv_file_path, credentials, isNode):
    queries = []

    if isNode:
        queries = query_builder.create_nodes(config_entity, csv_file_path)
    else:
        queries = query_builder.create_edges(config_entity, csv_file_path)

    for query in queries:
        run_query(query, credentials)
        

def run_query(query_string, credentials):
    driver = GraphDatabase.driver(credentials[0], auth=(credentials[1], credentials[2]))

    with driver.session() as session:
        session.run(query_string)