from itertools import chain

from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate

from data_access.profiling.repository import evaluation_repository
# from model.feedback_metadata import FeedbackMetadata
from service.employee_service import EmployeeService
from service.kpi_service import KpiService

# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain
kpi_service = KpiService()
employee_service = EmployeeService()


class FeedbackValidationService:
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def validate_feedbacks(self, employee_id, evaluator_id):

        feedbacks_object = employee_service.get_employees_by_evaluator_feedbacks(employee_id, evaluator_id)
        evaluator_object = employee_service.get_details(evaluator_id)
        employee_object = employee_service.get_details(employee_id)

        kpis = list(chain.from_iterable(feedback['kpis'] for feedback in feedbacks_object['feedbacks']))
        feedbacks = [feedback["text"] for feedback in feedbacks_object["feedbacks"]]

        kpi_object = kpi_service.find_by_employee_job_title_filtered_questions_by_evaluator_title(
            employee_object.title_code, evaluator_object.title_code) ##todo must get mentor and mentor by relation

        questions_list = [kpi["Question"] for kpi in kpi_object]
        ##todo  we cant filter here but we can map reduce if feedbacks size is max
        validated_response = self.are_feedbacks_sufficient(feedbacks, kpis, questions_list)

        for validated_object in validated_response:
            evaluation_repository.update_evaluation_validation(employee_id, evaluator_id, validated_object["question"],
                                                               validated_object["is_sufficient"], kpis)
        return validated_response

    def are_feedbacks_sufficient(self, feedbacks, kpis, questions):

        llm_model = "gpt-3.5-turbo"

        # x communicated well when there was an issue and was very constructive to resolve the issue, addresed many suggested answer and reached the optimal one
        # x is not communicating well, when y asked him to check his emails he answered rudly and he doesnt have time , while this email is urgently need reply and he is very late replying for almost 1 week, he is not helpful person to his team and always get away when asked to help others,v in his team asked him to push the code he ignored his request causing v to not able to finish as his task depends on x changes
        response_schemas = [
            ResponseSchema(
                name="response",
                description="""array contains question,is_sufficient and Suggestions in the following format: [
            {{ "question": string // Each question from the given questions.', "is_sufficient": boolean // Boolean indicating whether any feedback is sufficient to answer the question.',  ,"suggestions": [string] // Suggestions with a follow up question to enhance feedback for better clarity and specificity, and dont repeat the question in the inputs, else if part is covered mentioned what aspect is missing from the feedback.' }}
        ]
        """,
            )
        ]

        feedbacks_str = ', '.join(feedbacks)
        kpis_str = ', '.join(kpis)
        questions_str = ', '.join(questions)

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions().replace(
            '"response": string', '"response": array of objects'
        )
        template_string = """Analyze the employee feedback for clarity, specificity, and informativeness, check each questions given for all feedback list and make sure that the feedbacks are sufficient and contains enough data to answer each questions given else return is_sufficient false and prove by adding some suggestions and followup questions
            Inputs:
            - Feedback: A list of evaluator feedback {feedbacks_str}.
            - KPI Categories: A list of KPI categories {kpis_str}.
            - Questions: A list of questions {questions_str}.
    
            Format the response output as of JSON array, having the following keys:
            {format_instructions}
            The response list will depend on the number of questions.
            """

        prompt_template = ChatPromptTemplate.from_template(template_string)

        messages = prompt_template.format_messages(feedbacks_str=feedbacks_str, kpis_str=kpis_str,
                                                   questions_str=questions_str,
                                                   format_instructions=format_instructions)

        chat = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=self._open_Api_key)
        response = chat(messages)
        print(response.content)
        if response and response.content:
            output_dict = output_parser.parse(response.content)
            print(output_dict)
            print(output_dict.get('response'))
            return output_dict.get('response')
        else:
            return None
