from decouple import config
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

class ReportingService:
    def __init__(self):
        self._open_Api_key = "KEY"

    def generate_report(self, feedback_data):
        responses = []
        llm_model = "gpt-3.5-turbo"

        response_schemas = [
            ResponseSchema(
                name="response",
                description="""array contains strengths, weakness and personal enhancements in the following format: 
                [
                  {{ "strengths": [string], "weakness": [string], "suggestions": [string] }}
                ]
        """,
            )
        ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions().replace(
            '"response": string', '"response": array of objects'
        )
        template_string = """Analyze the employee feedback. Don't use exact wording of feedback in output itself
              What are his strengths based on the feedback {feedback_data} ? Give more than 1 strength 
              What are his weaknesses based on the feedback {feedback_data} ? Give more than 1 Weakness 
              What should he work on based on the feedback {feedback_data} ?
           Input:
            - Feedback: A list of evaluator feedback {feedback_data}.
           Outputs:
            - Strengths: A list of Strengths.
            - Weakness: A list of questions.
            - Suggestions: A list of questions.

            Format the response output as of JSON array, having the following keys:
            {format_instructions}
            """

        prompt_template = ChatPromptTemplate.from_template(template_string)

        messages = prompt_template.format_messages(feedback_data=feedback_data, format_instructions=format_instructions)

        chat = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=self._open_Api_key)
        response = chat(messages)

        if response and response.content:
            output_dict = output_parser.parse(response.content)
            print(output_dict)
            print(output_dict.get('response'))
            return output_dict.get('response')
        else:
            return response

# Sample feedback data
feedback_data = [
    "John Always replies in time and is the first to volunteer any help",
    "John tends to procrastinate on tasks and misses deadlines.",
    "John should prioritize time management and meet deadlines consistently."
]

# Create an instance of ReportingService
reporting_service = ReportingService()

# Call generate_report method with the sample feedback data
report_result = reporting_service.generate_report(feedback_data)

# Print the result or perform assertions based on your expectations
print(report_result)

#prompt= PromptTemplate(input_variables=["subtitle", "feedbacks"],
                        # template=" What are his {subtitle} based on the {feedbacks}? Give me at least 2 points",)
# print(prompt.format(subtitle="strengths", feedbacks="John Always replies in time and is the first to volunteer any help"))