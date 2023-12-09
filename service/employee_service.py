from typing import List, Optional
from data_access.profiling.repository import employee_repository
from model.employee import Employee
from model.employee_hierarchy import EmployeeHierarchy

class EmployeeService: 
    
    def get_details(self, employee_id: int) -> Optional[Employee]:
         employee_json = employee_repository.get_employee_details(employee_id)
         print(employee_json) 
         employee = Employee.from_json(employee_json)
         return employee
    
    def get_hierarchy(self):
         employees_hierarchy_json = employee_repository.get_employees_hierarchy()
         print(employees_hierarchy_json) 
         # employees_hierarchy = EmployeeHierarchy.from_json_list(employees_hierarchy_json)
         return employees_hierarchy_json
    
    def get_employees_to_evaluate(self, evaluator_id: int):
         employees_to_evaluate_json = employee_repository.get_employees_to_evaluate(evaluator_id)
         print(employees_to_evaluate_json) 
         return employees_to_evaluate_json

    def get_employees_by_evaluator_feedbacks(self,employee_id: int , evaluator_id: int):
         employees_feedbacks = employee_repository.get_employee_feedbacks_by_evaluator(employee_id, evaluator_id)
         print(employees_feedbacks)
         return employees_feedbacks

##todo to be used in reports
    def filters_employees_by_evaluator_feedbacks(self,employee_id: int , evaluator_id: int):
         employees_feedbacks=employee_repository.filter_employee_feedbacks(employee_id,evaluator_id, "What are his strengths based on the feedback?")
         print(employees_feedbacks)
         return employees_feedbacks

    def get_employees_by_evaluator_feedbacks_grouped_by_kpis(self,employee_id: int , evaluator_id: int):
         employees_feedbacks = employee_repository.get_employee_feedbacks_by_evaluator_grouped_by_kpis(employee_id, evaluator_id)
         print(employees_feedbacks)
         return employees_feedbacks
