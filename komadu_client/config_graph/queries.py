INIT_SWEEP = "MERGE (user:User{{name:'{0}' }}) " \
                "MERGE (camp:Campaign{{id:'{1}', name: '{2}' }}) " \
                "MERGE (sg:SweepGroup{{id:'{3}', name: '{4}'}}) " \
                # "MERGE (sw:Sweep{{id:'{5}', name: '{6}', created_at: localdatetime('{7}') }})"

SINGLE_FOBS_RELATIONSHIP = "MERGE (user)-[:Created]->(camp) " \
                "MERGE (camp)-[:Consists]->(sg) " \
                # "MERGE (sg)-[:Contains]->(sw) "

CONFIG_GRAPH = "MERGE (inst:RunInstance{{id:'{0}' }}) " \
                "MERGE (sim:GS_Simulation{{id:'{1}', name: '{1}'}}) " \
                "MERGE (pdf:GS_PDF{{id:'{2}', name: '{2}'}}) "\
                "MERGE (adios:ADIOS2{{id:'{3}', name: '{3}'}}) "\
                "MERGE (input:INPUT{{id:'{4}'}}) "\
                "MERGE (sg:SweepGroup{{id:'{5}' }})"\
                "MERGE (sw:Sweep{{id:'{6}'}})"\
                ""\
                "MERGE (sg)-[:Contains]->(sw)"\
                "MERGE (sw)-[:instance]->(inst) "\
                "MERGE (inst)-[:used]->(input) "\
                "MERGE (inst)-[:used]->(adios) "\
                "MERGE (inst)-[:workflow]->(sim) "\
                "MERGE (sim)-[:feeds]->(pdf) "


INSTANCE_UPDATE_QUERY = "Merge (inst:RunInstance{{id:'{0}' }}) SET inst.machine='{1}', inst.node_layout='{2}'"\
                        ", inst.modules='{3}'"

INPUT_UPDATE_QUERY = "Merge (input:INPUT{{id:'{0}' }}) SET "\
                     "input.L={1}, input.Du={2},"\
                     "input.Dv={3}, input.F={4},"\
                     "input.k={5}, input.dt={6},"\
                     "input.plotgap={7}, input.steps={8},"\
                     "input.noise={9}"
