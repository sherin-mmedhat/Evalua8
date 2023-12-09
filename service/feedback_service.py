from data_access.feedback.repository import feedback_repository
from data_access.profiling.repository import employee_repository
from service.employee_service import EmployeeService
from service.kpi_service import KpiService

kpi_service = KpiService()
employee_service = EmployeeService()


class FeedbackService:

    def submit_feedback(self, evaluator_id: int, employee_id: int, feedback: str):
        employee_details= employee_service.get_details(employee_id)

        kpi_data_list = kpi_service.find_by_job_title(employee_details.title_code)
        ##todo take kpis list and  feedback as inputs call categorise method , that will be used in kpis variable in submit_feedback
        feedback_id = feedback_repository.submit_feedback(evaluator_id=evaluator_id, feedback=feedback,
                                                          kpis=kpis)
        employee_repository.create_feedback_relation(employee_id=employee_id, feedback_id=feedback_id)
        return True
