from ..config import DATABASE_NAME
from ..mongodb_connection import MongodbConnection


def get_all_collection_names():  ## get all collections names (SSE, SSE1, .....) each title had a collection
    connection = MongodbConnection(DATABASE_NAME)
    return connection.get_collections()


def get_all_filtered_titles_columns(title_code: str):  ## get all colomns from a collection with the titles to filter the questions with
    connection = MongodbConnection(DATABASE_NAME)
    projection = {'Question': 0, 'KPI': 0, '_id': 0, 'id': 0, 'Weight': 0, 'Job_title_code': 0}
    document = connection.find_document(title_code, None, projection)
    print(document)
    print(title_code)
    if document:
       return document.keys()
    else:
        return []

def get_kpis_by_title_code(title_code: str, filter_by=None):
    connection = MongodbConnection(DATABASE_NAME)
    return connection.find_documents(title_code, filter_by,{'_id':0})


def get_question_by_title_code_and_kpi(title_code: str, kpi: str):
    connection = MongodbConnection(DATABASE_NAME)
    query = {'KPI': kpi}
    return connection.find_documents(title_code, query,{'_id':0})
