from openai import OpenAI
import os
import json

from decouple import config
# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain


class FeedbackValidationService: 
    def __init__(self):
        self._open_pi_key = config('OPEN_AI_KEY')

    def get_completion(self,prompt, model="gpt-3.5-turbo"):
        client = OpenAI(api_key=self._open_pi_key)
        
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response
        
    def are_feedbacks_sufficient(self,feedbacks, kpis, questions):
    
        prompt = f"""Analyze the employee feedback for clarity, specificity, and informativeness. Ensure examples of skills are given and the performance assessment questions are addressed thoroughly, it may be adressed in a negative or positive way which will be considered sufficient in both cases.Feedback:{', '.join(feedbacks)}
KPI Categories:{', '.join(kpis)}
Question:{{"questions": {json.dumps(questions)}}}
Confirm feedback alignment with employee's KPIs for objective evaluation. Offer improvement suggestions for feedback lacking clarity or specificity
Response Format: JSON object with analysis, sufficiency status, and suggestions for each question if and only if the sufficiency status is false, referenced by question ID. Example:
[{{"question_id": 123, "is_sufficient": "true/false", "suggestions": "brief analysis"}}]"""


        # prompt = PromptTemplate(template = template)
        # #prompt_formated= prompt.format(feedbacks=feedbacks, kpis= kpis, questions= questions)
        # # chain1 = LLMChain(llm=llm,prompt=prompt_formated)
        # # chain1.run(feedbacks,kpis,questions)
        # print(f"LLM Output: {llm(prompt)}")
        response = self.get_completion(prompt)
        print(response)
        if response and response.choices[0]:
           return response.choices[0].message.content
        else: 
          return None
        
    