from codar.cheetah import Campaign
from codar.cheetah import parameters as p
from codar.savanna.machines import SummitNode
from datetime import timedelta
import math

class GrayScott(Campaign):
    name = "Gray-Scott"
    codes = [("gray-scott", dict(exe="gray-scott"))]
    app_config_scripts = {'summit': 'env_summit.sh'}
    supported_machines = ['local', 'theta', 'summit']
    scheduler_options = {
        "theta": {
            "queue": "debug-flat-quad",
            "project": "CSC249ADCD01",
        },
        "summit": {
            "project": "csc299",
        }
    }
    kill_on_partial_failure = True

    umask = '027'

    nprocs = 6

    shared_node = SummitNode()
    for i in range(nprocs):
        shared_node.cpu[i] = "gray-scott:{}".format(i)
        shared_node.gpu[i] = ["gray-scott:{}".format(i)]
    shared_node_layout = [shared_node]
    
    L = [256]
    noise = [1.e-5]

    Du = [0.1, 0.2, 0.3]
    Dv = [0.05, 0.1, 0.15]
    F = [0.01, 0.02, 0.03]
    k = [0.048, 0.04, 0.06]

    sweep_parameters = \
    [
        p.ParamCmdLineArg("gray-scott", "settings", 1, ["settings.json"]),
        p.ParamConfig("gray-scott", "L", "settings.json", "L",
                      L),
        p.ParamConfig("gray-scott", "noise", "settings.json", "noise",
                      noise),
        p.ParamConfig("gray-scott", "Du", "settings.json", "Du",
                      Du),
        p.ParamConfig("gray-scott", "Dv", "settings.json", "Dv",
                      Dv),
        p.ParamConfig("gray-scott", "F", "settings.json", "F",
                      F),
        p.ParamConfig("gray-scott", "k", "settings.json", "k",
                      k),
        p.ParamRunner('gray-scott', 'nprocs', [nprocs] ),
    ]

    sweep = p.Sweep(parameters = sweep_parameters, node_layout={'summit':shared_node_layout})
    nodes = len(noise)*len(Du)*len(Dv)*len(F)*len(k)

    sweeps = \
    [
        p.SweepGroup(
            name = "gs",
            walltime = timedelta(minutes=60),
            nodes = nodes,
            component_subdirs = True,
            component_inputs = {
                'gray-scott': ['settings.json','adios2.xml'],
            },
            parameter_groups = [sweep]
        )
    ]


