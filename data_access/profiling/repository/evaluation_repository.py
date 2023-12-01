from ..neo4j_connection import Neo4jConnector


def get_evaluation(employee_id, evaluator_id):
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (e:Evaluation {employee_id: $employeeId, evaluator_id: $evaluatorId })
       RETURN COLLECT(properties(e)) AS evaluations;
        """
    evaluation_data = connector.find_by(query, {'employeeId': employee_id, 'evaluatorId': evaluator_id})
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None

#can be score or isSufficient
def update_evaluation_score(employee_id, evaluator_id, question, property, value):
    connector = Neo4jConnector()
    connector.connect()
    query = """
          MATCH (e:Evaluation {employeeId: '$employee_id', evaluator_id:'$evaluator_id' , question: '$question'})
          SET  e[$property] = $value'
           """
    evaluation_data = connector.find_by(query, {'employeeId': employee_id, 'evaluatorId': evaluator_id,
                                                'question': question, 'property': property, 'value': value })
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None

