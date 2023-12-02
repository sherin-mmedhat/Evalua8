from ..neo4j_connection import Neo4jConnector


def get_evaluation(employee_id, evaluator_id):
    connector = Neo4jConnector()
    connector.connect()
    query = """
       MATCH (e:Evaluation {employee_id: $employee_id, evaluator_id: $evaluator_id })
       RETURN COLLECT(properties(e)) AS evaluations;
        """
    evaluation_data = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id})
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None

#can be score or isSufficient
def update_evaluation_score(employee_id, evaluator_id, question, is_sufficient):
    connector = Neo4jConnector()
    connector.connect()
    query = """
          MATCH (e:Evaluation {employee_id:$employee_id , evaluator_id: $evaluator_id , question: $question})
          SET e.is_sufficient = toString($is_sufficient)
          return e;
           """
    evaluation_data = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id,
                                                'question': question, 'is_sufficient': is_sufficient })
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None

