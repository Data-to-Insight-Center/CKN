from komadu_client.graphdb.dbConnect import Database
from komadu_client.synthetic_gen.queries import *
from komadu_client.synthetic_gen.constants import *
from komadu_client.synthetic_gen.util import append, get_graphdb
import numpy as np
import itertools
import time

graphdb = get_graphdb()

user_1 = "igor"
user_2 = "kmehta"
campaign = "grayscott"

sg1 = append(campaign, "sg1")
sg2 = append(campaign, "sg2")

sweep1 = append(sg1, "sw1")
plan1 = append(sweep1, "plan")
instance_sw1 = append(sweep1, "instance1")

wfn_io = append(instance_sw1, "gs")
input_io = append(wfn_io, "input")
results_io = append(wfn_io, "results")

wfn_flush = append(instance_sw1, "pdf")
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
    return sweep_id


def get_input_query(input_id, inputs):
    """
    Given the input array for grayscott, provides the neo4j query.
    :param inputs: order: L, Du, Dv, F, k, dt, plotgap, steps, noise
    :return:
    """
    return INPUT_UPDATE_QUERY.format(input_id, inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5]
                                     , inputs[6], inputs[7], inputs[8])


def instance_query(sweep_id, instance_name, inputs, workflowNode1="gray-scott", workflowNode2="pdf-analysis"):
    instance_id = append(sweep_id, instance_name)
    wf1 = append(instance_id, workflowNode1)
    wf2 = append(instance_id, workflowNode2)
    input_id = append(wf1, "input")
    result1 = append(wf1, "result")
    result2 = append(wf2, "result")

    instance_q = INSTANCE_QUERY.format(sweep_id, instance_id, wf1, input_id, result1, result2, wf2)
    input_update_q = get_input_query(input_id, inputs)

    print(instance_q)
    print(input_update_q)

    graphdb.run_cypher_query(instance_q)
    graphdb.run_cypher_query(input_update_q)


def gray_scott_generator(sweep_group_id):
    """
    Generates the knowledge graph queries for the gray-scott query.
    @param sweep_group_id:
    @return:
    """
    # Uses Igor's dataset
    L = [256]
    noise = [0.00005]
    dt = [1]
    plotgap = [25]
    steps = [500]
    Du = [0.1, 0.2, 0.3]
    Dv = [0.05, 0.1, 0.15]
    F = [0.01, 0.02, 0.03]
    k = [0.048, 0.04, 0.06]

    # Creating all possible combinations of the above input sweep
    result = []
    iterables = [L, Du, Dv, F, k, dt, plotgap, steps, noise]
    for t in itertools.product(*iterables):
        result.append(np.array(t))

    in_params = np.array(result)

    # adding all these as individual sweeps
    for i in range(in_params.shape[0]):
        sweep_name = "sweep_" + str(i)

        # adding sweep
        sweep_id = sweep_only_query(sweep_group_id, sweep_name)
        # adding instance
        instance_query(sweep_id, 'instance-01', in_params[i])
        # waiting for the transactions finish each iteration
        time.sleep(1)

def main():
    # run_init_query()
    gray_scott_generator('grayscott-sg1')
    # sweep_only_query('OSU_IO_Summit_BigRed3-sg1', 'sweep23')
    # sweep_only_query('grayscott-sg1', 'sweep12')
    # inputs = [48, 0.2, 0.1, 0.02, 0.048, 1.0, 25, 500, 0.01]
    # instance_query('grayscott-sg1-sweep12', 'instance007', inputs)


if __name__ == "__main__":
    main()
