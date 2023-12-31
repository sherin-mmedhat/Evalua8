from ..neo4j_connection import Neo4jConnector


def get_employee_details(employee_id):
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (e:Employee {id: $employeeId})
       OPTIONAL MATCH (e)-[:MEMBER_OF]->(s:Squad)-[:OWNS]->(p:Project)
       RETURN e AS employee, COLLECT(DISTINCT p.name) AS projects, COLLECT(DISTINCT s.name) AS squads
        """
    employee_data = connector.find_by(query, {'employeeId': employee_id})
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None

def get_employees_hierarchy():
    connector = Neo4jConnector()
    connector.connect()
    query = """
        MATCH (e:Employee)-[:BELONGS_TO]->(t:Team)
        WITH e, t, e.level AS employeeLevel
        ORDER BY employeeLevel desc
        WITH t.name AS team,e.level AS level, COLLECT({ id: e.id, name: e.name, level: e.level , job_title: e.job_title , title_code: e.title_code  }) AS employees
        RETURN team, COLLECT({level: level, employees: employees}) AS employees
        ORDER BY team 
        """
    employee_data = connector.find_all(query)
    print("sheryyyy")
    print(employee_data)
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None

def get_employees_to_evaluate(evaluator_id):
    connector = Neo4jConnector()
    connector.connect()
    query = """
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
    employee_data = connector.find_all(query, {'evaluatorId': evaluator_id})
    connector.close()
    if employee_data:
        return employee_data
    else:
        return None


def get_employee_feedbacks(employee_id):
    print(employee_id)
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (e:Employee {id: $employee_id})<-[:HAVE]->(f:Feedback)
       RETURN COLLECT(f.text) AS feedbacks;
        """
    feedbacks = connector.find_by(query, {'employee_id': employee_id})
    connector.close()
    if feedbacks:
        return feedbacks
    else:
        return None

def get_employee_feedbacks_by_evaluator(employee_id,evaluator_id):
    print(employee_id)
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (e:Employee {id: $employee_id})<-[:HAVE]->(f:Feedback {evaluator_id: $evaluator_id})
       RETURN COLLECT({ text: f.text, kpis: f.kpis }) AS feedbacks;
        """
    feedbacks = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id})
    connector.close()
    if feedbacks:
        return feedbacks
    else:
        return []
##todo filterss embedding part is missing
def filter_employee_feedbacks(employee_id, evaluator_id, filters):
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (f:Feedback {evaluator_id: $evaluator_id})<-[:HAVE](e:Employee{ id : $employee_id}]
       RETURN COLLECT(f.feedback) AS feedbacks;
        """
    feedbacks = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id})
    connector.close()
    if feedbacks:
        return feedbacks
    else:
        return None

def create_feedback_relation(employee_id, feedback_id):
    connector = Neo4jConnector()
    connector.connect()
    query = """
    MATCH (e:Employee {id: $employee_id}),(f:Feedback{id : $feedback_id})
    CREATE (e)-[:HAVE]->(f)
    RETURN f
    """
    employee_feedback_data = connector.find_by(query, {'employee_id': employee_id, 'feedback_id': feedback_id})
    connector.close()
    if employee_feedback_data:
        return employee_feedback_data
    else:
        return None
