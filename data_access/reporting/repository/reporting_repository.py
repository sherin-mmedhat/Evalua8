from manager import report_pdf_manager

def generate_pdf(data):
    pdf_buffer = report_pdf_manager.generate_pdf(data)
    return pdf_buffer
