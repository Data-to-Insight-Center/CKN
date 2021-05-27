INIT_Q = "MERGE (sg:SweepGroup{{id:'{0}'}})<-[:Created]-(user1:User{{id:'{1}'}})<-[:Collaborator]-(n0:Campaign{{id:'{2}'}})-[:Contains]->(sg)-[:ConsistsOf]->(n3:Sweep{{id:'{3}'}})-[:instanced]->(n4:Instance{{id:'{4}'}})-[:runs]->(n7:WorkflowNode{{id:'{5}'}})-[:Used]->(:Input{{id:'{6}'}})" \
        "MERGE (r1:Results{{id:'{7}'}})-[:generatedBy]->(n7)" \
        "MERGE (r2:Results{{id:'{8}'}})-[:generatedBy]->(wf:WorkflowNode{{id:'{9}'}})<-[:runs]-(n4)" \
        "MERGE (n3)-[:Used]->(plan:Plan{{id:'{10}'}})" \
        "MERGE (n34:User{{id:'{11}'}})<-[:Collaborator]-(n0)-[:Contains]->(sg2:SweepGroup{{id:'{12}'}})<-[:Created]-(n34)"

SWEEP_ONLY = "MATCH (sg:SweepGroup{{id:'{0}'}}) CREATE (sg)-[:ConsistsOf]->(:Sweep{{id:'{1}'}})-[:Used]->(:Plan{{id:'{2}'}})"

SWEEP_TREE = "MERGE (:SweepGroup)-[:ConsistsOf]->(n3:Sweep)-[:instanced]->(n4:Instance)-[:runs]->(n7:WorkflowNode)-[:Used]->(:Input)" \
        "MERGE (:Results)-[:generatedBy]->(n7)" \
        "MERGE (:Results)-[:generatedBy]->(:WorkflowNode)<-[:runs]-(n4)" \
        "MERGE (n3)-[:Used]->(:Plan)"

INSTANCE_QUERY = "MATCH (sw:Sweep{{id:'{0}'}})" \
        "CREATE (sw)-[:instanced]->(n4:Instance{{id:'{1}'}})-[:runs]->(n7:WorkflowNode{{id:'{2}'}})-[:Used]->(:Input{{id:'{3}'}})" \
        "CREATE (:Results{{id:'{4}'}})-[:generatedBy]->(n7)" \
        "CREATE (:Results{{id:'{5}'}})-[:generatedBy]->(:WorkflowNode{{id:'{6}'}})<-[:runs]-(n4)"


INSTANCE_UPDATE_QUERY = "MATCH (inst:Instance{{id:'{0}' }}) SET inst.machine='{1}', inst.node_layout='{2}'"\
                        ", inst.modules='{3}'"

INPUT_UPDATE_QUERY = "MATCH (input:Input{{id:'{0}' }}) SET "\
                     "input.L={1}, input.Du={2},"\
                     "input.Dv={3}, input.F={4},"\
                     "input.k={5}, input.dt={6},"\
                     "input.plotgap={7}, input.steps={8},"\
                     "input.noise={9}"

CONSTRAINTS = "CREATE CONSTRAINT ON (user:User) ASSERT user.id IS UNIQUE; "\
        "CREATE CONSTRAINT ON (cod:Codesign) ASSERT cod.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (camp:Campaign) ASSERT camp.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (sg:SweepGroup) ASSERT sg.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (sw:Sweep) ASSERT sw.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (inst:Instance) ASSERT inst.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (rs:Results) ASSERT rs.id IS UNIQUE;" \
        "CREATE CONSTRAINT ON (wf:WorkflowNode) ASSERT wf.id IS UNIQUE;"

