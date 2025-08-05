from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = FastAPI()

# CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductData(BaseModel):
    product_name: str
    category: str
    ingredients: str
    benefits: str
    manufacturing_date: str
    expiry_date: str
    certifications: str

@app.post("/preview-report")
def preview_report(data: ProductData):
    # Returns formatted HTML preview
    preview_text = f"""
    <strong>Product Name:</strong> {data.product_name}<br/>
    <strong>Category:</strong> {data.category}<br/>
    <strong>Ingredients:</strong> {data.ingredients}<br/>
    <strong>Benefits:</strong> {data.benefits}<br/>
    <strong>Manufacturing Date:</strong> {data.manufacturing_date}<br/>
    <strong>Expiry Date:</strong> {data.expiry_date}<br/>
    <strong>Certifications:</strong> {data.certifications}<br/>
    """
    return {"report_html": preview_text}

@app.post("/generate-report")
def generate_pdf(data: ProductData):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y = 750

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Product Transparency Report")
    y -= 40
    pdf.setFont("Helvetica", 12)

    fields = [
        ("Product Name", data.product_name),
        ("Category", data.category),
        ("Ingredients", data.ingredients),
        ("Benefits", data.benefits),
        ("Manufacturing Date", data.manufacturing_date),
        ("Expiry Date", data.expiry_date),
        ("Certifications", data.certifications),
    ]

    for label, value in fields:
        pdf.drawString(50, y, f"{label}: {value}")
        y -= 30

    pdf.save()
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/pdf")
