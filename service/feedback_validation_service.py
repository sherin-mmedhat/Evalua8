from openai import OpenAI
import os
import json

from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain


class FeedbackValidationService: 
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')
        


    def get_completion(self,prompt, model="gpt-3.5-turbo"):
        client = OpenAI(api_key=self._open_Api_key)
        
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        return response
        
    def are_feedbacks_sufficient(self,feedbacks, kpis, questions):
    
        template = f"""Analyze the employee feedback for clarity, specificity, and informativeness that should address the KPIs and the questions given. Analyze each question against each feedback and check if the feedback covers the answer to the questions given, both in a positive and negative context.

Format the output as JSON with the following keys:
- question: each question from the given questions
- is_sufficient: if the positive or negative aspects of the feedback are sufficient to answer the question; answer True if yes, False
- suggestions: Offer improvement suggestions for each question that the feedback lacks clarity or specificity. Explicitly mention that examples have already been provided and ask for more specific details or instances.

Feedback: [{', '.join(feedbacks)}]
KPI Categories: {[', '.join(kpis)]}
Questions: {[', '.join(questions)]}

 if feedback was negative and contain a specifc reason so consider sufficient
example : 
feedback: employee x deosnt work quite well in team because he is rude to other employees , should ne considered as sufficient"""

        prompt_template = ChatPromptTemplate.from_template(template)
        messages = prompt_template.format_messages(feedbacks=feedbacks,kpis =kpis, questions= questions)
        chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo",openai_api_key=self._open_Api_key)
        response = chat(messages)
        print(response.content)
        # prompt = PromptTemplate(template = template)
        # #prompt_formated= prompt.format(feedbacks=feedbacks, kpis= kpis, questions= questions)
        # # chain1 = LLMChain(llm=llm,prompt=prompt_formated)
        # # chain1.run(feedbacks,kpis,questions)
        # print(f"LLM Output: {llm(prompt)}")
        # response = self.get_completion(prompt)
        #print(response)
        # if response and response.choices[0]:
        #    return response.choices[0].message.content
        # else: 
        #   return None
        if response and response.content:
            return response.content
        else: 
           return None 
    