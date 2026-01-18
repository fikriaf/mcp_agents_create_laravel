from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os

def create_cover():
    output_path = "frontend/docs/cover.pdf"
    logo_path = "demo/logo_GenLaravel.png"
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Colors
    black = HexColor("#000000")
    gray = HexColor("#6b7280")
    
    # Logo
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width/2 - 75, height - 220, width=150, height=150, preserveAspectRatio=True, mask='auto')
    
    # Title
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 280, "GenLaravel")
    
    c.setFillColor(gray)
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 305, "AI-Powered Laravel Project Generator")
    
    # UAS Title
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 380, "LAPORAN TUGAS UAS")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 410, "Mata Kuliah Project Management")
    
    # Team info
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height - 480, "Disusun Oleh:")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 505, "Kelompok 7")
    
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, height - 535, "Fikri Armia Fahmi (2023071018)")
    c.drawCentredString(width/2, height - 555, "Nadia (2024071004)")
    
    # University
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 640, "UNIVERSITAS PEMBANGUNAN JAYA")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 665, "Program Studi Informatika")
    c.drawCentredString(width/2, height - 690, "2025")
    
    c.save()
    print(f"✅ Cover created: {output_path}")

if __name__ == "__main__":
    create_cover()
