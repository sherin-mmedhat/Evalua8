from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from manager import report_plotting_manager, dummy_data

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

    employee_data, kpis = dummy_data.generate_dummy_employee_data(1)  # Set the employee ID for the dummy data
    plot_images, buffers = report_plotting_manager.generate_plots(employee_data, kpis)
    content.extend(plot_images)

    # Add the content to the PDF document
    document.build(content)

    # Close all buffers
    for buffer in buffers:
        buffer.close()

    # Move the buffer's cursor to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer
