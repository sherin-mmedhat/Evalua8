from data_access.feedback.repository import feedback_repository
from data_access.profiling.repository import employee_repository

class FeedbackService:

    def submit_feedback(self, evaluator_id: int, employee_id: int, feedback: str):
       feedback_id = feedback_repository.submit_feedback(evaluator_id=evaluator_id, feedback=feedback, kpis=["Problem Solving", "Hard Worker"])
       employee_repository.create_feedback_relation(employee_id=employee_id, feedback_id=feedback_id)
       return True
