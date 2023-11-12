import neo4j_connection

from neo4j import GraphDatabase

def get_employee_details(employee_id):
    
    query =  """
       MATCH (e:Employee)-[:MEMBER_OF]->(s:Squad)-[OWNS]->(p:Project)
       WHERE ID(e) = 3
       RETURN e.name AS employee_name, COLLECT(Distinct s.name) AS squads , COLLECT(DISTINCT p.name) AS projects
        """
    
    result = neo4j_connection.execute_cypher_query(query, {'employee_id': employee_id})
    data = result.single()
    print(result)
    return data
    # if data:
    #     return {
    #         'employee_name': data['name'],
    #         'squads': data['squads'],
    #         'projects': data['projects'],
    #     }
    # else:
    #     return None
