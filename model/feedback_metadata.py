from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
    
class FeedbackMetadata(BaseModel):
    evaluator_id: int
    kpis: List[str]
    date: datetime = datetime.now()
    
    @classmethod
    def from_json(cls, json_data: Dict) -> 'FeedbackMetadata':
        if json_data:
            return cls(
                evaluator_id=json_data.get('evaluator_id'),
                kpis=json_data.get('kpis', []),
                date=json_data.get('date'),
            )
        else:
            return cls()
