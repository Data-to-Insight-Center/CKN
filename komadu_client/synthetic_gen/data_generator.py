from komadu_client.graphdb.dbConnect import Database
from komadu_client.synthetic_gen.queries import *
from komadu_client.synthetic_gen.constants import *
from komadu_client.synthetic_gen.util import append

graph_db_uri = "bolt://127.0.0.1:7687"
graph_db_username = "neo4j"
graph_db_password = "rootroot"
graphdb = Database(graph_db_uri, graph_db_username, graph_db_password)

user_1 = "swithana"
user_2 = "kmehta"
campaign = "OSU_IO_Summit_BigRed3"

sg1 = append(campaign, "sg1")
sg2 = append(campaign, "sg2")

sweep1 = append(sg1, "sw1")
plan1 = append(sweep1, "plan")
instance_sw1 = append(sweep1, "instance1")

wfn_io = append(instance_sw1, "IO")
input_io = append(wfn_io, "input")
results_io = append(wfn_io, "results")

wfn_flush = append(instance_sw1, "flush")
input_flush = append(wfn_flush, "input")
results_flush = append(wfn_flush, "results")


def run_init_query():
    """
    Initializes the graph structure with one instance.
    """
    init_query = INIT_Q.format(sg1, user_1, campaign, sweep1, instance_sw1, wfn_io,
                               input_io, results_io, results_flush, wfn_flush, plan1, user_2, sg2)
    print(init_query)
    graphdb.run_cypher_query(init_query)


def sweep_only_query(sg_id, sweep_name):
    sweep_id = append(sg_id, sweep_name)
    plan_id = append(sweep_id, 'plan')
    sw_query = SWEEP_ONLY.format(sg_id, sweep_id, plan_id)
    print(sw_query)
    graphdb.run_cypher_query(sw_query)


def instance_query(sweep_id, instance_name):
    instance_id = append(sweep_id, instance_name)
    wf1 = append(instance_id, "OSU_bw")
    wf2 = append(instance_id, "flush")
    input = append(wf1, "input")
    result1 = append(wf1, "result")
    result2 = append(wf2, "result")

    instance_q = INSTANCE_QUERY.format(sweep_id, instance_id, wf1, input, result1, result2, wf2)
    print(instance_q)
    graphdb.run_cypher_query(instance_q)


def main():
    # run_init_query()
    # sweep_only_query('OSU_IO_Summit_BigRed3-sg1', 'sweep23')
    instance_query('OSU_IO_Summit_BigRed3-sg1-sweep23', 'instance008')


if __name__ == "__main__":
    main()
