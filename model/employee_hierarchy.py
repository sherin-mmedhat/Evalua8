from pydantic import BaseModel
from typing import List, Dict, Optional
from model.employee import Employee

class EmployeeHierarchy(BaseModel):
    team: str
    employees_by_level:dict
    
    @classmethod       
    def from_json_list(cls, json_data):
        team_list = [
        EmployeeHierarchy(
            team=team_data.get("team"),
            employees_by_level={
                employees_level_data["level"]: [
                    Employee(**employee) for employee in employees_level_data["employees"]
                ] for employees_level_data in team_data.get("employees", [])
            }
        )
         for team_data in json_data
        ]
        return cls(EmployeeHierarchy=team_list)