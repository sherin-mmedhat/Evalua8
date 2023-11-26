from ..neo4j_vector_index_connector import Neo4jVectorIndexConnector

def submit_feedback(evaluator_id: int, feedback: str, kpis: [str]):
    vector_store_connector = Neo4jVectorIndexConnector()
    feedback_id = vector_store_connector.add_feedback(
        feedback=feedback,
        evaluator_id=evaluator_id,
        kpis=kpis,
    )
    return feedback_id
