from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def create_toc():
    output_path = "frontend/docs/daftar_isi.pdf"
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    black = HexColor("#000000")
    
    # Border
    margin = 50
    c.setStrokeColor(black)
    c.setLineWidth(2)
    c.rect(margin, margin, width - 2*margin, height - 2*margin)
    
    # Inner border
    c.setLineWidth(0.5)
    c.rect(margin + 5, margin + 5, width - 2*margin - 10, height - 2*margin - 10)
    
    # Title centered
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 120, "DAFTAR ISI")
    
    # Table of contents
    toc_items = [
        ("1.", "Cover", "1"),
        ("2.", "Daftar Isi", "2"),
        ("3.", "Latar Belakang & Masalah Proyek", "3"),
        ("4.", "Stakeholder, Scope Statement & Project Charter", "8"),
        ("5.", "Work Breakdown Structure (WBS)", "19"),
        ("6.", "Network Diagram", "28"),
        ("7.", "Gantt Chart", "37"),
        ("8.", "Anggaran & Earned Value Management (EVM)", "67"),
        ("9.", "Risiko & Procurement Analysis", "84"),
        ("10.", "Draft Dokumen Kontrak Pengadaan", "91"),
        ("11.", "Hasil Monitoring & Kontrol", "102"),
        ("12.", "Kesimpulan", "113"),
        ("13.", "Lampiran", "114"),
    ]
    
    y_start = height - 200
    line_height = 35
    
    c.setFont("Helvetica", 12)
    
    for i, (no, title, page) in enumerate(toc_items):
        y = y_start - (i * line_height)
        
        # Number
        c.drawString(margin + 40, y, no)
        
        # Title
        c.drawString(margin + 70, y, title)
        
        # Dots
        title_width = c.stringWidth(title, "Helvetica", 12)
        dots_start = margin + 75 + title_width
        dots_end = width - margin - 70
        
        dot_spacing = 5
        x = dots_start
        while x < dots_end:
            c.drawString(x, y, ".")
            x += dot_spacing
        
        # Page number (right aligned)
        c.drawRightString(width - margin - 40, y, page)
    
    c.save()
    print(f"✅ Daftar Isi created: {output_path}")

if __name__ == "__main__":
    create_toc()
