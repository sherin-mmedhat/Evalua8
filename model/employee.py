from pydantic import BaseModel
from typing import List, Dict, Optional
    
class Employee(BaseModel):
    id: int
    name: str
    level: str
    department: str
    job_title: str
    title_code: str
    projects: List[str] = None
    squads: List[str] = None
    
    @classmethod
    def from_json(cls, json_data: Dict) -> 'Employee':
        if json_data:
            print(json_data)
            employee_data = json_data.get('employee', {})
            return cls(
                id=employee_data.get('id'),
                name=employee_data.get('name'),
                level=employee_data.get('level'),
                department=employee_data.get('department'),
                job_title=employee_data.get('job_title'),
                title_code=employee_data.get('title_code'),
                projects=json_data.get('projects',[]),
                squads=json_data.get('squads',[]),
            )
        else:
            {}        