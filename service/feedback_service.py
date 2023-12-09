from data_access.feedback.repository import feedback_repository
from data_access.profiling.repository import employee_repository
from service.employee_service import EmployeeService
from service.kpi_service import KpiService
from service.categorizing_service_T5 import CategorizingUsingTransformersService

kpi_service = KpiService()
employee_service = EmployeeService()
categorizing_service = CategorizingUsingTransformersService()


class FeedbackService:

    def submit_feedback(self, evaluator_id: int, employee_id: int, feedback: str):
        employee_details= employee_service.get_details(employee_id)

        kpi_data_list = kpi_service.find_by_job_title(employee_details.title_code)

        kpis = list(set([kpi["KPI"] for kpi in kpi_data_list]))
        
        category_label = categorizing_service.categorize_text(kpis, [feedback])
        print("Feedback category:", category_label)
        
        feedback_id = feedback_repository.submit_feedback(evaluator_id=evaluator_id, feedback=feedback,
                                                          kpis=kpis)
        employee_repository.create_feedback_relation(employee_id=employee_id, feedback_id=feedback_id)
        return True
