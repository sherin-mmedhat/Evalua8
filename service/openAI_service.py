from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from service.constants import llm_model


class OpenAIService:
    def __init__(self):
        self._open_Api_key = config('OPEN_API_KEY')

    def call_openAI(self, system_message: str,human_message_prompt_template: str, variables_dic):
        chat_prompt_template = ChatPromptTemplate.from_messages([system_message, human_message_prompt_template])
        formatted_user_input = chat_prompt_template.invoke(
            variables_dic
        )
        print(formatted_user_input)
        chat = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=self._open_Api_key)
        response = chat(formatted_user_input)

        return response
