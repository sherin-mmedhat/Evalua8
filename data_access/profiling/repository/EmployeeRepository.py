from neo4j_connection import Neo4jConnector

from decouple import config
from neo4j import GraphDatabase

def get_employee_details(employee_id):

    connector = Neo4jConnector()
    connector.connect()
    query =  """
       MATCH (e:Employee {id: $employeeId})
       OPTIONAL MATCH (e)-[:MEMBER_OF]->(s:Squad)-[:OWNS]->(p:Project)
       RETURN e AS employee, COLLECT(DISTINCT p.name) AS projects, COLLECT(DISTINCT s.name) AS squads
        """
    employee_data = connector.find_by(query,{'employeeId':employee_id})
    
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None

def get_employees_hirerachy():

    connector = Neo4jConnector()
    connector.connect()
    query =  """
        MATCH (e:Employee)-[:BELONGS_TO]->(t:Team)
        WITH e, t, e.level AS employeeLevel
        ORDER BY employeeLevel desc
        WITH t.name AS team,e.level AS level, COLLECT({ id: e.id, name: e.name, level: e.level , job_title: e.job_title }) AS employees
        RETURN team, COLLECT({level: level, employees: employees}) AS employees
        ORDER BY team 
        """
    employee_data = connector.find_all(query)
    
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None

def get_employees_to_evaluate(evaluatorId):
    connector = Neo4jConnector()
    connector.connect()
    query =  """
        MATCH (employee:Employee {id: $evaluatorId})
        OPTIONAL MATCH (employee)-[:MENTOR]->(mentee:Employee)
        OPTIONAL MATCH (employee)-[r1:MEMBER_OF]->(s:Squad)<-[r2:MEMBER_OF]-(colleague:Employee)
        WITH employee, 
        COLLECT(DISTINCT mentee {.*}) AS mentees,
        COLLECT(DISTINCT colleague {.*}) AS colleagues
        OPTIONAL MATCH (mentor:Employee)-[:MENTOR]->(employee)
        RETURN employee.id AS employeeId, employee.name AS employeeName, mentees,colleagues,
        COLLECT(DISTINCT mentor {.*}) AS mentors
        """
    employee_data = connector.find_all(query,{'evaluatorId':evaluatorId})
    
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None



    