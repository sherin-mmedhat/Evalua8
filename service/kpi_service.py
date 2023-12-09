from data_access.kpi.repository import Kpi_repository


class KpiService:

    def get_all_job_title_codes(self):
        list(Kpi_repository.get_all_collection_names())
    def get_questions_by_job_title_and_kpi(self, job_title_code: str, kpi: str):
        return list(Kpi_repository.get_question_by_title_code_and_kpi(job_title_code, kpi))

    def find_by_job_title(self, title_code: str):
        return list(Kpi_repository.get_kpis_by_title_code(title_code))

    def find_by_employee_job_title_filtered_questions_by_evaluator_title(self, employee_job_title_code: str,
                                                                         evaluator_job_title_code: str,
                                                                         kpi:str,
                                                                         is_mentor=False, is_mentored_by=False
                                                                         ):
        titles_exists_to_filter = list(Kpi_repository.get_all_filtered_titles_columns(
            employee_job_title_code))  ## EM, TL, PM ,QC,

        filter_questions_by = self.filter_question_by_evaluator_title(evaluator_job_title_code, is_mentor,
                                                                      is_mentored_by, titles_exists_to_filter)

        query = {"$or": [{key: "Yes","KPI": kpi} for key in filter_questions_by]}
        print(query)
        return list(Kpi_repository.get_kpis_by_title_code(employee_job_title_code, query))

    def filter_question_by_evaluator_title(self, evaluator_job_title_code, is_mentor, is_mentored_by,
                                           titles_exists_to_filter):
        filter_questions_by = []  ## can be extracted to a method
        if evaluator_job_title_code not in titles_exists_to_filter:
            if is_mentor:
                filter_questions_by.append("ME")
            if is_mentored_by:
                filter_questions_by.append("ME_BY")

            filter_questions_by.append("CL")
        else:
            filter_questions_by.append(evaluator_job_title_code)
        return filter_questions_by
