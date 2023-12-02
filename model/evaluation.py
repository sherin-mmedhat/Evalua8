from pydantic import BaseModel
from typing import List, Dict, Optional
    
class Evaluation(BaseModel):
    id: int
    question:  str
    kpi:str = None
    is_sufficient: str
    suggestions: List[str] = None
    score: int = None
    evaluator_id: int
    employee_id: int
    
    @classmethod
    def from_json(cls, json_data: Dict) -> 'Evaluation':
        if json_data:
            print(json_data)
            evaluation_data = json_data.get('evaluation', {})
            return cls(
                id=evaluation_data.get('id'),
                question=evaluation_data.get('question'),
                is_sufficient=evaluation_data.get('is_sufficient'),
                kpi=evaluation_data.get('kpi'),
                score=evaluation_data.get('score'),
                evaluation_id=evaluation_data.get('evaluation_id'),
                employee_id=evaluation_data.get('employee_id'),
            )
        else:
            {}
class EvaluationList(BaseModel):
    evaluations: List[Evaluation]