from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

from data_access.profiling.repository import employee_repository
from data_access.profiling.repository import evaluation_repository
# from model.feedback_metadata import FeedbackMetadata
from model.evaluation import EvaluationList


# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain


class FeedbackValidationService:
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def validate_feedbacks(self, employee_id, evaluator_id):

        feedbacks = employee_repository.get_employee_feedbacks(employee_id, evaluator_id)
        print(feedbacks)
        evaluations_data = evaluation_repository.get_evaluation(employee_id, evaluator_id)

        evaluationList = EvaluationList(**evaluations_data)
        questions_list = [evaluation.question for evaluation in evaluationList.evaluations]

        validated_response = self.are_feedbacks_sufficient(feedbacks, ["Productivity,Teamwork"], questions_list)
        print(validated_response)
        validated_list = json.loads(validated_response)
        # for validated_object in validated_list:
        #     evaluation_repository.update_evaluation_score(employee_id,evaluator_id,validated_object["question"],"is_sufficient", validated_object["is_sufficient"])
        # return validated_list
        return validated_list

    def are_feedbacks_sufficient(self, feedbacks, kpis, questions):

        template = f"""You are an expert in performance evaluation. Your task is to analyze evaluator feedback for employees to ensure its clarity, specificity, and informativeness, addressing the KPIs and questions provided. Evaluate each question and ensur the feedback contains sufficient information to answer.
Inputs:
- Feedback: A list of evaluator feedback [{', '.join(feedbacks)}].
- KPI Categories: A list of KPI categories {[', '.join(kpis)]}.
- Questions: A list of questions {[', '.join(questions)]}.

Format the output as a JSON list with the following keys:
- "question": Each question from the given questions.
- "is_sufficient": Boolean indicating whether any feedback is sufficient to answer the question.
- "suggestions": Suggestions with a follow up question to enhance feedback for better clarity and specificity, and dont repeat the question in the inputs, else if part is covered mentioned what aspect is missing from the feedback.

The response list will depend on the number of questions.
"""

        prompt_template = ChatPromptTemplate.from_template(template)
        messages = prompt_template.format_messages(feedbacks=feedbacks, kpis=kpis, questions=questions)
        chat = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo", openai_api_key=self._open_Api_key)
        response = chat(messages)
        print(response.content)
        # prompt = PromptTemplate(template = template)
        # #prompt_formated= prompt.format(feedbacks=feedbacks, kpis= kpis, questions= questions)
        # # chain1 = LLMChain(llm=llm,prompt=prompt_formated)
        # # chain1.run(feedbacks,kpis,questions)
        # print(f"LLM Output: {llm(prompt)}")
        # response = self.get_completion(prompt)
        # print(response)
        # if response and response.choices[0]:
        #    return response.choices[0].message.content
        # else: 
        #   return None
        if response and response.content:
            return response.content
        else:
            return None
