import pytest
from io import StringIO
import sys
import os, os.path

from autoneo import builder

curr_path = os.path.dirname(os.path.abspath(__file__))

data_dir_path = os.path.join(curr_path, "data")
query_dir_path = os.path.join(curr_path, "query")
csv_dir_path = os.path.join(curr_path, "csv")


def test_build():
    """
    Tests loading data into a graph when the config file indicates:
     - the data from Person & Work tables must be extracted from the database and loaded into Neo4j as Nodes
     - the data correlating People and what they do is in a CSV and must be loaded as an Edge
    """
    with StringIO('bolt://localhost:7687\nneo4j\nadmin') as f:
        stdin = sys.stdin
        sys.stdin = f
        builder.build(
            os.path.join(curr_path, "config.json"), 
            data_dir_path, query_dir_path, csv_dir_path)
        sys.stdin = stdin
