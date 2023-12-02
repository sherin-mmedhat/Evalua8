from model.employee import Employee
import openai
import json
from decouple import config

from data_access.profiling.repository import employee_repository
from service.employee_service import EmployeeService


class ReportingService: 

    def __init__(self):
        openai.api_key= config('OPEN_API_KEY')

    def generate_report(self, employee_id):


          employee_json = employee_repository.get_employee_details(employee_id)
          employee = Employee.from_json(employee_json)
          feedbacks = employee_repository.get_employee_feedbacks(employee_id)
          employee_name =employee.name
          feedback= [feedback_object for feedback_object in feedbacks['feedbacks']]
          responses = []
          prompts = [
              f"For {employee_name}. What are his strengths based on the feedback? {feedback}. Give me 2 points ",
              f"For {employee_name}. What are his weaknesses based on the feedback? {feedback}. Give me 2 points ",
              f"For {employee_name}. What should he work on based on the feedback? {feedback}"
          ]
          for prompt in prompts:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": prompt},
                        ]
                # max_tokens=50
            )
            responses.append(response.choices[0].message.content.strip("."))

          # Create a JSON structure
          report_json = {
              "employee_name": employee_name,
              "strengths": responses[0],
              "weaknesses": responses[1],
              "areas_for_improvement": responses[2]
          }
          return report_json

# Example usage
employee_name = "John Doe"
feedback_data = [
    "John ALways replies in time and the first to volunteer any help",
    "John tends to procrastinate on tasks and misses deadlines.",
    "John should prioritize time management and meet deadlines consistently."
]
# reporting_service = ReportingService()

# report_json = reporting_service.generate_report(2)

# Print the JSON report
# print(json.dumps(report_json, indent=2))
