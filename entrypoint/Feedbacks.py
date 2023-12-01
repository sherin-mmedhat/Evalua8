from fastapi import FastAPI, HTTPException, APIRouter
from service.feedback_service import FeedbackService
from service.feedback_validation_service import FeedbackValidationService
from model.feedback_request import FeedbackRequest

router = APIRouter()

service = FeedbackService()

validationService = FeedbackValidationService()

@router.post("/api/employee/{employee_id}/feedback")
def submit_feedback(employee_id: int, feedback_request: FeedbackRequest):
    service.submit_feedback(evaluator_id=feedback_request.evaluator_id, employee_id=employee_id, feedback=feedback_request.feedback)
    return {"message": "Feedback submitted successfully"}

@router.post("/api/validation/feedbacks/evaluator/{evaluator_id}/employee/{employee_id}")
def submit_feedback(employee_id: int, evaluator_id: int, ):
     return validationService.validate_feedbacks(employee_id,evaluator_id)
