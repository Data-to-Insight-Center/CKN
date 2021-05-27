from komadu_client.graphdb.dbConnect import Database


def append(first, last):
    return first + "-" + last


def get_graphdb():
    graph_db_uri = "bolt://127.0.0.1:7687"
    graph_db_username = "neo4j"
    graph_db_password = "rootroot"
    return Database(graph_db_uri, graph_db_username, graph_db_password)