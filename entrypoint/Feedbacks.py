from fastapi import FastAPI, HTTPException, APIRouter
from service.feedback_service import FeedbackService
from service.feedback_validation_service import FeedbackValidationService
from service.evaluation_service import EvaluationService
from model.feedback_request import FeedbackRequest

router = APIRouter()

service = FeedbackService()
validationService = FeedbackValidationService()
evaluationService = EvaluationService()

@router.post("/api/employee/{employee_id}/feedback")
def submit_feedback(employee_id: int, feedback_request: FeedbackRequest):
    service.submit_feedback(evaluator_id=feedback_request.evaluator_id, employee_id=employee_id, feedback=feedback_request.feedback)
    return {"message": "Feedback submitted successfully"}

@router.post("/api/validation/feedbacks/evaluators/{evaluator_id}/employees/{employee_id}")
def validate_submitted_feedback(employee_id: int, evaluator_id: int, ):
     return validationService.validate_feedbacks(employee_id,evaluator_id)

@router.get("/api/evaluators/{evaluator_id}/employees/{employee_id}/evaluations")
def get_evaluation(evaluator_id: int, employee_id: int):
    return evaluationService.get_evaluation(evaluator_id, employee_id)