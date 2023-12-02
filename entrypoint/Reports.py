from fastapi import APIRouter
from fastapi.responses import StreamingResponse
# from service.reporting_service import ReportingService
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

router = APIRouter()

# service = ReportingService()

def generate_plots(employee_data):
    buffers = []
    for attribute in ['Productivity', 'Teamwork']:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(employee_data['Date'], employee_data[attribute], marker='o', linestyle='-')
        ax.set_title(attribute)
        ax.set_xlabel('Date')
        ax.set_ylabel('Score')
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffers.append(buffer)

    plot_images = [Image(buffer) for buffer in buffers]
    return plot_images, buffers

def generate_dummy_employee_data(employee_id):
    # Generate dummy data for an employee
    dates = [datetime(2023, 1, 1) + timedelta(days=i*180) for i in range(3)]
    productivity = np.random.uniform(1, 10, size=3)
    teamwork = np.random.uniform(1, 10, size=3)

    data = {
        'Employee_ID': [employee_id] * 3,
        'Date': dates,
        'Productivity': productivity,
        'Teamwork': teamwork
    }

    employee_data = pd.DataFrame(data)
    employee_data['Date'] = employee_data['Date'].dt.strftime('%Y-%m-%d')
    return employee_data

def generate_pdf(data):
    pdf_buffer = BytesIO()

    # Create a PDF document
    document = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Create styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    body_style = styles['BodyText']

    # Create a list to hold the content of the PDF
    content = []

    # Add data to the PDF content
    content.append(Paragraph(f"<u>{data['employee_name']}</u>", title_style))
    
    # Strengths section
    content.append(Spacer(1, 12))
    content.append(Paragraph("Strengths", heading_style))
    strengths_items = [ListItem(Paragraph(point, body_style), bulletAlign='left') for point in data['strengths'].split('\n')]
    strengths_list = ListFlowable(strengths_items, bulletType='bullet', start='', leftIndent=20, bulletFontName='Helvetica', bulletFontSize=10)
    content.append(strengths_list)

    # Weaknesses section
    content.append(Spacer(1, 12))
    content.append(Paragraph("Weaknesses", heading_style))
    weaknesses_items = [ListItem(Paragraph(point, body_style), bulletAlign='left') for point in data['weaknesses'].split('\n')]
    weaknesses_list = ListFlowable(weaknesses_items, bulletType='bullet', start='', leftIndent=20, bulletFontName='Helvetica', bulletFontSize=10)
    content.append(weaknesses_list)

    # Areas for Improvement section
    content.append(Spacer(1, 12))
    content.append(Paragraph("Areas for Improvement", heading_style))
    areas_for_improvement_items = [ListItem(Paragraph(point, body_style), bulletAlign='left') for point in data['areas_for_improvement'].split('\n')]
    areas_for_improvement_list = ListFlowable(areas_for_improvement_items, bulletType='bullet', start='', leftIndent=20, bulletFontName='Helvetica', bulletFontSize=10)
    content.append(areas_for_improvement_list)

    # Add space before the matplotlib plot
    content.append(Spacer(1, 12))

    employee_data = generate_dummy_employee_data(1)  # Set the employee ID for the dummy data
    plot_images, buffers = generate_plots(employee_data)
    content.extend(plot_images)

    # Add the content to the PDF document
    document.build(content)

    # Close all buffers
    for buffer in buffers:
        buffer.close()

    # Move the buffer's cursor to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer

@router.get("/api/employee/{employee_id}/report")
def get_report(employee_id: int):

    json_data = """
        {
        "employee_name": "John Doe",
        "strengths": "1. John's strength is his ability to reply in a timely manner. This indicates that he is attentive and responsible, ensuring that he addresses any requests or inquiries promptly.\\n\\n2. Another strength of John is his willingness to volunteer and offer help. This demonstrates his proactive nature and willingness to assist others, showcasing a strong sense of teamwork and collaboration.\\n\\nRecommendation:\\n- John should prioritize time management to address his tendency to procrastinate and miss deadlines. By effectively managing his time and breaking tasks into smaller, manageable portions, John can improve his productivity and ensure timely completion of assignments.\\n- Additionally, John should make it a habit to consistently meet deadlines. This can be achieved by setting realistic deadlines, utilizing task management techniques such as prioritizing tasks, creating schedules, and setting reminders to stay on track. Meeting deadlines consistently will help improve John's overall performance and reliability",
        "weaknesses": "1. Weakness: Procrastination and missed deadlines.\\n- John's tendency to procrastinate on tasks and miss deadlines is a significant weakness that needs to be addressed. This behavior can negatively impact his productivity and overall performance.\\n\\n2. Improvement Required: Prioritizing time management and meeting deadlines consistently.\\n- To overcome this weakness, John should focus on improving his time management skills. This includes developing effective strategies to prioritize tasks, setting realistic deadlines, as well as utilizing time management tools or techniques that can help him stay organized and on track. Meeting deadlines consistently will not only enhance his productivity but also positively impact his reputation and reliability within the team",
        "areas_for_improvement": "He should work on improving his ability to manage his time effectively and ensure that he completes tasks within the given time frames. By overcoming procrastination and consistently meeting deadlines, John will be seen as reliable and dependable in his work. This will contribute to his overall professional growth and success"
        }
    """

    data = json.loads(json_data)

    # Generate the PDF
    pdf_buffer = generate_pdf(data)

    # Return the PDF as a downloadable file
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment;filename=employee_feedback.pdf"})
