from komadu_client.graphdb.dbConnect import Database
from komadu_client.config_graph.queries import *
from datetime import datetime
import os


class ConfigGraph:

    def __init__(self):
        graph_db_uri = "neo4j://localhost:7687"
        graph_db_username = "neo4j"
        graph_db_password = "rootroot"

        self.graphdb = Database(graph_db_uri, graph_db_username, graph_db_password)

    def get_init_sweep(self):
        user = 'igor'
        camp_id = 'cs_pipeline'
        camp_name = 'Compression Pipeline'
        sg_name = sg_id = user + '-' + camp_id + '-sg01'

        return sg_id, INIT_SWEEP.format(user, camp_id, camp_name, sg_id, sg_name
                                        ) + " " + SINGLE_FOBS_RELATIONSHIP

    def get_config_graph(self, sg_id, counter):
        sweep_name = sweep_id = sg_id + '-' + str(counter)

        instance_id = sweep_id + '-instance-01'
        sim_id = instance_id + '-simulation'
        pdf_id = instance_id + '-pdf'
        adios_id = instance_id + '-adios'
        input_id = instance_id + '-input'

        sw_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        return instance_id, CONFIG_GRAPH.format(instance_id, sim_id, pdf_id, adios_id, input_id, sg_id, sweep_id, sweep_name, sw_time)

    def get_input_query(self, input_id, inputs):
        """
        Given the input array for grayscott, provides the neo4j query.
        :param inputs: order: L, Du, Dv, F, k, dt, plotgap, steps, noise
        :return:
        """
        return INPUT_UPDATE_QUERY.format(input_id, inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5]
                                  , inputs[6], inputs[7], inputs[8])

    def run(self):
        sg_id, init_query = self.get_init_sweep()
        instance_id, config_graph = self.get_config_graph(sg_id, 0)


        # initializing the campaign graph
        self.graphdb.run_cypher_query(init_query)

        # adding the config graph
        self.graphdb.run_cypher_query(config_graph)

        # adding input params
        input_query = self.get_input_query(instance_id + '-input', [48, 0.2, 0.1, 0.02, 0.048, 1.0, 25, 500, 0.01])
        self.graphdb.run_cypher_query(input_query)


if __name__ == "__main__":
    print("Hello World!")
    config_graph = ConfigGraph()
    config_graph.run()
