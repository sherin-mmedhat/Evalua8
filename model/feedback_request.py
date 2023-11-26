from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    evaluator_id: int
    feedback: str
