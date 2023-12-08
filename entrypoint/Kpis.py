from fastapi import FastAPI, HTTPException, APIRouter

from service.kpi_service import KpiService

router = APIRouter()

kpi_service = KpiService()


# @router.get("/api/kpi/all")
# def get_all_kpi():
#     projection = {'_id': 0}
#     kpi_data_list = list(kpi_collection.find({}, projection))
#     return kpi_data_list

# @router.get("/api/kpi/{KPI}")
# def get_questions_for_kpi(KPI: str):
#     query = {'KPI': KPI}
#     distinct_questions = kpi_collection.find(query).distinct('Question')
#     projected_questions = list(kpi_collection.find(query, {'Question': 1, '_id': 0}))
#
#     if projected_questions:
#         return distinct_questions
#     else:
#         raise HTTPException(status_code=404, detail=f"No questions found for: {KPI}")

@router.get("/api/kpi/{Job_title}", tags=["KPI"])
def get_kpi_by_job_title(Job_title: str):

    kpi_data_list= kpi_service.find_by_job_title(Job_title)
    if kpi_data_list:
        return kpi_data_list
    else:
        raise HTTPException(status_code=404, detail=f"No employees found with job title:{Job_title}")

@router.get("/api/kpi/{employee_job_title}/{evaluator_job_title}",tags=["KPI"])
def get_kpi_for_job_title_and_evaluator(employee_job_title: str, evaluator_job_title: str):

    #  todo add validation step to call profile an make sure there is a connection between evlauator
    #   and employee before proceeding [working in same squad or mentor , mentored by ]
    # raise HTTPException(status_code=400, detail=f"Invalid evaluator '{evaluator_job_title}'. Valid evaluators are: {', '.join(valid_evaluators)}")

    #  update is_mentor flags
    #   update  is_mentored_by = false # todo should call profile to know if evluator is mentored by employee
    kpi_data_list = kpi_service.find_by_employee_job_title_filtered_questions_by_evaluator_title(employee_job_title,
                                                                                                 evaluator_job_title)  # default will be colegue(CL)
    if kpi_data_list:
        return kpi_data_list
    else:
        raise HTTPException(status_code=404, detail=f"No KPI found for '{employee_job_title}' and '{evaluator_job_title}'")