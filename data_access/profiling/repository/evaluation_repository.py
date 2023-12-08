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
def update_evaluation_validation(employee_id, evaluator_id, question, is_sufficient,kpis):
    connector = Neo4jConnector()
    connector.connect()
    query = """
          MERGE (e:Evaluation {employee_id:$employee_id , evaluator_id: $evaluator_id , question: $question})
          SET e.is_sufficient = toString($is_sufficient),
              e.employee_id = $employee_id ,
              e.evaluator_id =$evaluator_id,
              e.question = $question,
              e.score= 0,
              e.kpi=$kpis
          return e;
           """
    evaluation_data = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id,
                                                'question': question, 'is_sufficient': is_sufficient , 'kpis':  kpis})
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None

def update_evaluation_score(employee_id, evaluator_id, question, score):
    connector = Neo4jConnector()
    connector.connect()
    query = """
          MATCH (e:Evaluation {employee_id:$employee_id , evaluator_id: $evaluator_id , question: $question})
          SET e.score = $score
          return e;
           """
    evaluation_data = connector.find_by(query, {'employee_id': employee_id, 'evaluator_id': evaluator_id,
                                                'question': question, 'score': score })
    connector.close()
    if evaluation_data:
        return evaluation_data
    else:
        return None