import math
from codar.cheetah import Campaign
from codar.cheetah import parameters as p
from codar.savanna.machines import SummitNode
from codar.cheetah.parameters import SymLink
import node_layouts as node_layouts
import sweeps as sweeps
import copy


class GrayScott(Campaign):
    name = "osu-jitter"

    codes = [ ("create", dict(exe="create.sh")),
              ("flush", dict(exe="flush.sh")),
              ("osu0", dict(exe="osu_bw")),
              ("osu1", dict(exe="osu_bw")),
              ("osu2", dict(exe="osu_bw")),
              ("osu3", dict(exe="osu_bw")),
              ("osu4", dict(exe="osu_bw")),
              ("osu5", dict(exe="osu_bw")),
              ("term", dict(exe="term.sh")), ]

    supported_machines = ['local', 'theta', 'summit']
    kill_on_partial_failure = True
    run_dir_setup_script = None
    run_post_process_script = "bin/cleanup.sh"
    umask = '027'
    scheduler_options = {'theta': {'project':'CSC249ADCD01', 'queue': 'default'},
                         'summit': {'project':'csc299'}}
    app_config_scripts = {'local': 'env-setup.sh', 'theta': 'env_setup.sh', 'summit':'env-setup.sh'}

    per_run_timeout = 300
    num_repetitions = 2

    sw_list = []
    for nstreams in range(1,11):
        sw1 = sweeps.sweep1(nstreams,1)
        sw_list.append(sw1)
    sw1 = sweeps.sweep1(2,0)
    sw_list.append(sw1)

    
    sg1 = p.SweepGroup ("interference-test-1-thru-10-streams-separate-out-files-2",
                        walltime=per_run_timeout * (num_repetitions+1) * len(sw_list),
                        per_run_timeout=per_run_timeout,
                        parameter_groups=sw_list,
                        launch_mode='default',
                        tau_profiling=False,
                        tau_tracing=False,
                        #nodes=16,
                        # component_inputs = {'simulation': ['settings-files.json', 'settings-staging.json'], },
                        run_repetitions=num_repetitions, )
    
    # Activate the SweepGroup
    sweeps = {'summit':[sg1]}

