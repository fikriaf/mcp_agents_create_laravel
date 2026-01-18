from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

def create_kesimpulan():
    output_path = "frontend/docs/kesimpulan.pdf"
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    black = HexColor("#000000")
    margin = 70
    
    # Title centered
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 70, "Kesimpulan")
    
    # Content
    c.setFont("Helvetica", 11)
    
    text = """Proyek GenLaravel berhasil diselesaikan dengan pencapaian 100% dari 16 task yang 
direncanakan, mencakup pengembangan 10 AI agent untuk auto-generate aplikasi Laravel, 
implementasi WebSocket streaming, dan deployment ke Railway (backend) serta Vercel 
(frontend). Sistem fallback LLM (Cerebras → Mistral AI) terbukti efektif dengan 77.8% 
issue terselesaikan, meskipun masih terdapat 2 issue rate limit yang bersifat eksternal. 
Vendor Mistral AI menunjukkan performa terbaik dengan 100% uptime dan 0% error rate 
sebagai fallback provider, sementara sistem monitoring otomatis berhasil mencatat 
seluruh aktivitas proyek secara real-time."""
    
    y = height - 110
    for line in text.split('\n'):
        c.drawString(margin, y, line.strip())
        y -= 18
    
    c.save()
    print(f"✅ Kesimpulan created: {output_path}")

def create_lampiran():
    output_path = "frontend/docs/lampiran.pdf"
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    black = HexColor("#000000")
    blue = HexColor("#1e40af")
    margin = 70
    max_width = width - 2 * margin
    
    # Title centered
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 70, "Lampiran")
    
    y = height - 120
    
    # Link Notion
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Link Notion:")
    y -= 20
    c.setFont("Helvetica", 9)
    c.setFillColor(blue)
    notion_url = "https://horse-aunt-9cf.notion.site/GenLaravel-MCP-Agents-"
    c.drawString(margin, y, notion_url)
    y -= 15
    notion_url2 = "Laravel-UI-Generator-link-demo-9e1d4a01fad7408da16ce4f3c0c298ae"
    c.drawString(margin, y, notion_url2)
    
    y -= 40
    
    # Link YouTube
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Link Presentasi YouTube:")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Part 1 (Pembukaan + Penjelasan):")
    y -= 15
    c.setFont("Helvetica", 9)
    c.setFillColor(blue)
    c.drawString(margin, y, "https://youtu.be/SLTOWBXYCzc?si=-jbBqZQUm1Nf9sRR")
    y -= 20
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Part 2 (Penjelasan + Demo):")
    y -= 15
    c.setFont("Helvetica", 9)
    c.setFillColor(blue)
    c.drawString(margin, y, "https://youtu.be/3ZV_AVcg82E?si=ECpMfBvGY0QatKwQ")
    
    y -= 40
    
    # Link Demo Website
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Link Demo Website:")
    y -= 20
    c.setFont("Helvetica", 9)
    c.setFillColor(blue)
    c.drawString(margin, y, "https://mcp-agents-create-laravel.vercel.app/")
    
    y -= 40
    
    # Link PPT
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Link PPT:")
    y -= 20
    c.setFont("Helvetica", 9)
    c.setFillColor(blue)
    ppt_url = "https://www.canva.com/design/DAG7KSmsGC4/"
    c.drawString(margin, y, ppt_url)
    y -= 15
    ppt_url2 = "7K6z1h-vDdIVrryOGTpu3A/edit"
    c.drawString(margin, y, ppt_url2)
    
    c.save()
    print(f"✅ Lampiran created: {output_path}")

if __name__ == "__main__":
    create_kesimpulan()
    create_lampiran()
