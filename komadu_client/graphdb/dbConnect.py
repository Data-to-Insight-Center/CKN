from neo4j import GraphDatabase
from komadu_client.graphdb.queries import CREATE_USER, READ_USER


class Database(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def run_fobs_init_graph_query(self, query):
        """
        Creates the initial graph for the fobs information
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.run_init_fobs_graph, query)

    def add_input_to_graph(self, query):
        """
        Adds an input to the graph
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.add_input_graph, query)

    def run_cypher_query(self, query):
        """
        Runs a given query
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.add_input_graph, query)

    def add_property_to_node(self, query):
        """
        Adds an input to the graph
        :param query:
        :return:
        """
        with self._driver.session() as session:
            session.write_transaction(self.add_property_to_graph, query)

    def add_user(self, name):
        with self._driver.session() as session:
            session.write_transaction(self.create_user_node, name)
            return session.read_transaction(self.match_user_node, name)

    def retrieve_data(self, query):
        with self._driver.session() as session:
            return session.read_transaction(self.get_data, query).data()

    # Units of work
    @staticmethod
    def create_user_node(tx, name):
        return tx.run(CREATE_USER, name=name).single().value()

    @staticmethod
    def match_user_node(tx, name):
        result = tx.run(READ_USER, name=name)
        return result.single()[0]

    @staticmethod
    def get_data(tx, query):
        result = tx.run(query)
        return result

    @staticmethod
    def run_init_fobs_graph(tx, query):
        return tx.run(query).single()

    @staticmethod
    def add_input_graph(tx, query):
        return tx.run(query).single()

    @staticmethod
    def add_property_to_graph(tx, query):
        return tx.run(query).single()


