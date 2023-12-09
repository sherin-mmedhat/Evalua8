from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage

from data_access.profiling.repository import evaluation_repository
# from model.feedback_metadata import FeedbackMetadata
from service.employee_service import EmployeeService
from service.kpi_service import KpiService
from service.openAI_service import OpenAIService

# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain
kpi_service = KpiService()
employee_service = EmployeeService()
openAi_service = OpenAIService()


class FeedbackValidationService:
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def validate_feedbacks(self, employee_id, evaluator_id):

        kpi_feedbacks_dic = employee_service.get_employees_by_evaluator_feedbacks_grouped_by_kpis(employee_id, evaluator_id)
        evaluator_object = employee_service.get_details(evaluator_id)
        employee_object = employee_service.get_details(employee_id)
        for kpi_feedbacks in kpi_feedbacks_dic:
            self.validate_feedbacks_per_kpi(evaluator_object,employee_object,kpi_feedbacks)
        return "job finished validating "

    def validate_feedbacks_per_kpi(self,evaluator,employee,kpi_feedbacks):
        kpi = kpi_feedbacks["kpi"]
        feedbacks = [feedback["text"] for feedback in kpi_feedbacks["feedbacks"]]
        kpi_questions = kpi_service.find_by_employee_job_title_filtered_questions_by_evaluator_title(
            employee.title_code, evaluator.title_code,kpi)  ##todo must get mentor and mentor by relation
        questions_list = [kpi["Question"] for kpi in kpi_questions]

        validated_response = self.are_feedbacks_sufficient(feedbacks, kpi, questions_list)

        for validated_object in validated_response:
            evaluation_repository.update_evaluation_validation(employee.id, evaluator.id, validated_object["question"],
                                                               validated_object["is_sufficient"], [kpi])

    def are_feedbacks_sufficient(self, feedbacks, kpis, questions):

        llm_model = "gpt-3.5-turbo"

        system_message = SystemMessage(content=(
            """
            You are now assigned to analyze employee feedback for this system. Your role is to assess the feedback entries based on the following criteria:

            * **Clarity:** Evaluate if the feedback is clear, concise, and easy to understand.
            * **Specificity:** Assess whether the feedback includes specific examples and details.
            * **Informativeness:** Determine if the feedback provides enough information to answer competencies about the employee's competency.
            * **Alignment with competency:** Evaluate whether the feedback addresses the relevant aspects of the employee's competency, as defined in the provided KPIs.

            You must consider both positive and negative feedback. Your task is to provide:

            * A list of employee feedback entries.
            * A list of relevant KPI categories.
            * A list of competencies to be answered about the employee's competency.

            Ensure that your input covers a diverse range of feedback types to allow the system to provide a comprehensive analysis. Thank you for your assistance!

            **Remember, your evaluation should be based on the provided KPIs and the diverse range of feedback provided.**
            """)
        )

        response_schemas = [
            ResponseSchema(
                name="response",
                description="""array contains competency,is_sufficient and Suggestions in the following format: [
            {{ "question": string // Each competency from the given competencies.', "is_sufficient": boolean // Boolean indicating whether any feedback is sufficient to completely and clearly answer the competency without needing additional information.',  ,"suggestions": [string] // Suggestions with a follow up question to enhance feedback for better clarity and specificity, and dont repeat the question in the inputs, else if part is covered mentioned what aspect is missing from the feedback.' }}
        ]
        """,
            )
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions().replace(
            '"response": string', '"response": array of objects'
        )
        human_message_prompt_template = HumanMessagePromptTemplate.from_template(
            """
            **Feedback:**
            {feedback_list}

            **KPIs:**
            {kpi_list}

            **Competencies:**
            {question_list}

            **format_instructions**
            {format_instructions}
            """
        )

        feedbacks_str = '\n'.join(feedbacks)
        kpis_str = '\n'.join(kpis)
        questions_str = '\n'.join(questions)

        chat_prompt_template = ChatPromptTemplate.from_messages([system_message, human_message_prompt_template])
        formatted_user_input = chat_prompt_template.format_messages(
            feedback_list=feedbacks_str, kpi_list=kpis_str, question_list=questions_str, format_instructions=format_instructions
        )
        print(formatted_user_input)
        chat = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=self._open_Api_key)
        response = chat(formatted_user_input)
        print(response.content)
        if response and response.content:
            output_dict = output_parser.parse(response.content)
            print(output_dict)
            print(output_dict.get('response'))
            return output_dict.get('response')
        else:
            return None
