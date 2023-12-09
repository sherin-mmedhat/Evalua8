from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from service.reporting_service import ReportingService

router = APIRouter()

service = ReportingService()

@router.get("/api/employee/{employee_id}/report",tags=["reports"])
def get_report(employee_id: int):

    pdf_buffer = service.generate_report(employee_id)

    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment;filename=employee_feedback.pdf"})
