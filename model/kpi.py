from pydantic import BaseModel
from typing import List, Dict, Optional
    
class Kpi(BaseModel):
    id: int
    KPI: str
    Question: str
    Weight: str
    Job_title: str
    Engineering_manager: str
    Team_lead: str
    Project_manager: str
    Quality_control: str
    Mentored_by: str
    CL: str
    
    @classmethod
    def from_json(cls, json_data: Dict) -> 'Kpi':
        if json_data:
            return cls(
                id=json_data.get('id'),
                KPI=json_data.get('KPI'),
                Question=json_data.get('Question'),
                Weight=json_data.get('Weight'),
                Job_title=json_data.get('Job_title'),
                Engineering_manager=json_data.get('Engineering_manager'),
                Team_lead=json_data.get('Team_lead'),
                Project_manager=json_data.get('Project_manager'),
                Quality_control=json_data.get('Quality_control'),
                Mentored_by=json_data.get('Mentored_by'),
                CL=json_data.get('CL'),
            )
        else:
            return cls()
