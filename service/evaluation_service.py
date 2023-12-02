from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate

from data_access.profiling.repository import evaluation_repository
from data_access.profiling.repository import employee_repository
from model.evaluation import EvaluationList
class EvaluationService:

    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def get_evaluation(self, evaluator_id: int, employee_id: int):
        return evaluation_repository.get_evaluation(employee_id=employee_id, evaluator_id=evaluator_id)

    def score_evaluations(self, employee_id, evaluator_id):

        feedbacks = employee_repository.get_employee_feedbacks_by_evaluator(employee_id, evaluator_id)
        print(feedbacks)
        evaluations_data = evaluation_repository.get_evaluation(employee_id, evaluator_id)

        evaluationList = EvaluationList(**evaluations_data)
        questions_list = [evaluation.question for evaluation in evaluationList.evaluations]

        score_response = self.give_rates_for_questions(feedbacks, questions_list)

        print(score_response)
        for score_object in score_response:
            print(score_object["question"])
            print(score_object["score"])
            evaluation_repository.update_evaluation_score(employee_id, evaluator_id, score_object["question"],
                                                          score_object["score"])

        return self.get_evaluation(evaluator_id, employee_id)

    def give_rates_for_questions(self, feedbacks, questions):

        llm_model = "gpt-3.5-turbo"

        response_schemas = [
            ResponseSchema(
                name="response",
                description="""array contains question,score  in the following format: [
            {{ "question": string // Each question from the given questions.', "score": int // number representing the score given for each question according to feedback .',  }}
        ]
        """,
            )
        ]

        feedbacks_str = ', '.join(feedbacks)
        questions_str = ', '.join(questions)

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions().replace(
            '"response": string', '"response": array of objects'
        )
        template_string = """Given the following feedback about an employee, please rate their performance on a scale of 1 to 10 (1 being the lowest and 10 being the highest) for each of the specified questions:
            Inputs:
            - Feedback: A list of employee feedbacks {feedbacks_str}.
            - Questions: A list of questions {questions_str}.
            provide a numerical rating (1-10) for each question based on the feedback given. If a question cannot be adequately answered from the feedback, you may assign a neutral score
            Format the response output as of JSON array, having the following keys:
            {format_instructions}
            The response list will depend on the number of questions.
            """

        prompt_template = ChatPromptTemplate.from_template(template_string)

        messages = prompt_template.format_messages(feedbacks_str=feedbacks_str,
                                                   questions_str=questions_str,
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