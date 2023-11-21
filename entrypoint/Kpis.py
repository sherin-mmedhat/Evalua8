from fastapi import FastAPI, HTTPException, APIRouter
from typing import Dict
from pymongo import MongoClient

router = APIRouter()

# Connect to MongoDB
client = MongoClient('evalu8-mongodb', 27017)
db = client['KPI']
kpi_collection = db['kpi_collection']

@router.get("/api/kpi/all")
def get_all_kpi():
    projection = {'_id': 0}
    kpi_data_list = list(kpi_collection.find({}, projection))
    return kpi_data_list

@router.get("/api/kpi/{KPI}")
def get_questions_for_kpi(KPI: str):
    query = {'KPI': KPI}
    distinct_questions = kpi_collection.find(query).distinct('Question')
    projected_questions = list(kpi_collection.find(query, {'Question': 1, '_id': 0}))
    
    if projected_questions:
        return distinct_questions
    else:
        raise HTTPException(status_code=404, detail=f"No questions found for: {KPI}")

@router.get("/api/kpi/{Job_title}")
def get_kpi_by_job_title(Job_title: str):
    projection = {'_id': 0}
    kpi_with_job_title = kpi_collection.find({"Job_title": Job_title}, projection)
    kpi_data_list = list(kpi_with_job_title)
    if kpi_data_list:
        return kpi_data_list
    else:
        raise HTTPException(status_code=404, detail=f"No employees found with job title:{Job_title}")

@router.get("/api/kpi/{job_title}/{evaluator_job_title}")
def get_kpi_for_job_title_and_evaluator(job_title: str, evaluator_job_title: str):
    valid_evaluators = ["Engineering_manager", "Team_lead", "Project_manager", "Quality_control", "Mentored_by", "CL"]
   
    if evaluator_job_title not in valid_evaluators:
        raise HTTPException(status_code=400, detail=f"Invalid evaluator '{evaluator_job_title}'. Valid evaluators are: {', '.join(valid_evaluators)}")

    projection = {'Question': 1, 'KPI': 1, '_id': 0}
    query = {evaluator_job_title: "Yes", "Job_title": job_title}
    kpi_data_list = list(kpi_collection.find(query, projection))
   
    if kpi_data_list:
        return kpi_data_list
    else:
        raise HTTPException(status_code=404, detail=f"No KPI found for '{job_title}' and '{evaluator_job_title}'")