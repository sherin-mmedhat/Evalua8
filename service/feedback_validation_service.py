from itertools import chain

from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import json
from data_access.profiling.repository import employee_repository
from data_access.profiling.repository import evaluation_repository
# from model.feedback_metadata import FeedbackMetadata
from model.evaluation import EvaluationList

from langchain.output_parsers import ResponseSchema, StructuredOutputParser, PydanticOutputParser


# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain


class FeedbackValidationService:
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def validate_feedbacks(self, employee_id, evaluator_id):

        feedbacks = employee_repository.get_employee_feedbacks_by_evaluator(employee_id, evaluator_id)
        print(feedbacks)
        evaluations_data = evaluation_repository.get_evaluation(employee_id, evaluator_id)

        evaluationList = EvaluationList(**evaluations_data)
        questions_list = [evaluation.question for evaluation in evaluationList.evaluations]

        validated_response = self.are_feedbacks_sufficient(feedbacks, ["Productivity,Teamwork"], questions_list)

        print(validated_response)
        for validated_object in validated_response:
             print(validated_object["question"])
             print(validated_object["is_sufficient"])
             evaluation_repository.update_evaluation_validation(employee_id,evaluator_id,validated_object["question"] , validated_object["is_sufficient"])
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
        template_string = """Analyze the employee feedback for clarity, specificity, and informativeness, addressing the questions given. Analyze each question against each feedback and check if the feedback covers the answer to the questions given, even in a negative context
            Inputs:
            - Feedback: A list of evaluator feedback {feedbacks_str}.
            - KPI Categories: A list of KPI categories {kpis_str}.
            - Questions: A list of questions {questions_str}.
    
            Format the response output as of JSON array, having the following keys:
            {format_instructions}
            The response list will depend on the number of questions.
            """

        prompt_template = ChatPromptTemplate.from_template(template_string)

        messages = prompt_template.format_messages(feedbacks_str=feedbacks_str, kpis_str=kpis_str, questions_str=questions_str,
                                                  format_instructions=format_instructions)

        chat = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=self._open_Api_key)
        response = chat(messages)

        if response and response.content:
            output_dict = output_parser.parse(response.content)
            print(output_dict)
            print(output_dict.get('response'))
            return output_dict.get('response')
        else:
         return None
