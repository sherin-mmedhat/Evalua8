from typing import Dict, List
from pymongo import MongoClient

#To use this you need to start mangodb
#So connect with following command "mongod --dbpath data/db"
#If using for first time run "Python3 data_access/kpi/KPI_db_migration.py" to create db 
class KpiService:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient()
        self.db = self.client['KPI']
        self.kpi_collection = self.db['kpi_collection']

    def get_all_kpi():
        projection = {'_id': 0}
        kpi_data_list = list(self.kpi_collection.find({}, projection))
        return kpi_data_list

    def get_questions_for_kpi(self, KPI: str):
        query = {'KPI': KPI}
        distinct_questions = self.kpi_collection.find(query).distinct('Question')
        projected_questions = list(self.kpi_collection.find(query, {'Question': 1, '_id': 0}))
        return distinct_questions

    def get_kpi_by_job_title(self, Job_title: str):
        projection = {'_id': 0}
        kpi_with_job_title = self.kpi_collection.find({"Job_title": Job_title}, projection)
        kpi_data_list = list(kpi_with_job_title)
        return kpi_data_list

    def get_kpi_for_job_title_and_evaluator(self, job_title: str, evaluator_job_title: str):
        valid_evaluators = ["Engineering_manager", "Team_lead", "Project_manager", "Quality_control", "Mentored_by", "CL"]
    
        if evaluator_job_title not in valid_evaluators:
            return "Invalid evaluator '{evaluator_job_title}'. Valid evaluators are: {', '.join(valid_evaluators)}"

        projection = {'Question': 1, 'KPI': 1, '_id': 0}
        query = {evaluator_job_title: "Yes", "Job_title": job_title}
        kpi_data_list = list(self.kpi_collection.find(query, projection))
        return kpi_data_list
   
# Example usage
KPI_service = KpiService()
Questions = KPI_service.get_questions_for_kpi("Dependability")
print("Questions", Questions)