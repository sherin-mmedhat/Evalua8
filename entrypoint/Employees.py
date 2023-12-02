from fastapi import FastAPI, HTTPException, APIRouter
from service.employee_service import EmployeeService
from model.employee import Employee
from typing import Dict

router = APIRouter()

service = EmployeeService()


@router.get("/api/employee/{employee_id}")
def get_details(employee_id: int):
  
    employee = service.get_details(employee_id)   
    if employee:
        wrapped_employee = {'employee': employee}
        return wrapped_employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

    
@router.get("/api/employees/hierarchy")
def get_hierarchy():
  
    employee_hierarchy = service.get_hierarchy()   
    if employee_hierarchy:
        
        return employee_hierarchy
    else:
        raise HTTPException(status_code=404, detail="no employee hierarchy found")

@router.get("/api/evaluators/{evaluator_id}/employees-being-evaluated")
def get_employees_to_evaluate(evaluator_id: int):
      
    employee_to_evaluate = service.get_employees_to_evaluate(evaluator_id)
    if employee_to_evaluate:
        
        return employee_to_evaluate[0]
    else:
        raise HTTPException(status_code=404, detail="no employees to evaluate")

@router.get("/api/employees/{employee_id}/evaluators/{evaluator_id}/feedbacks")
def get_feedbacks(evaluator_id: int, employee_id: int):
    return service.get_employees_by_evaluator_feedbacks(employee_id,evaluator_id)

