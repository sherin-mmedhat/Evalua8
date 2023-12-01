from data_access.profiling.repository import evaluation_repository


class EvaluationService:

    def get_evaluation(self, evaluator_id: int, employee_id: int):
        return evaluation_repository.get_evaluation(employee_id=employee_id, evaluator_id=evaluator_id)
