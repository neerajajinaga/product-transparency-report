from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = FastAPI()

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static index.html
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_index():
    return FileResponse("index.html")

# Data model for product input
class ProductData(BaseModel):
    product_name: str
    category: str
    ingredients: str
    benefits: str
    manufacturing_date: str
    expiry_date: str
    certifications: str

# Endpoint for previewing the report
@app.post("/preview-report")
def preview_report(data: ProductData):
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

# Endpoint to generate PDF
@app.post("/generate-report")
def generate_pdf(data: ProductData):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y = 750

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Product Transparency Report")
    pdf.setFont("Helvetica", 12)
    y -= 40

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
