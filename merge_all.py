from PyPDF2 import PdfMerger
import os

docs_path = "frontend/docs"

# Urutan lengkap sesuai daftar isi
pdf_files = [
    "cover.pdf",                                                 # 1. Cover
    "daftar_isi.pdf",                                            # 2. Daftar Isi
    "Project Planning_Agent Auto Generate Laravel Project.pdf",  # 3. Latar belakang
    "Kelompok 7_project_charter_scope.pdf",                      # 4. Stakeholder, Scope, Charter
    "Kelompok 7_wbs.pdf",                                        # 5. WBS
    "Kelompok 7_network_diagram.pdf",                            # 6. Network Diagram
    "Kelompok 7_scrum_gantt_chart.pdf",                          # 7. Gantt Chart
    "Kelompok 7_EVM_GenLaravel.pdf",                             # 8. Anggaran & EVM
    "Kelompok 7_GenLaravel_Procurement Analysis.pdf",            # 9. Risiko & Procurement
    "Kelompok 7_GenLaravel_Draft Dokumen Kontrak Pengadaan.pdf", # 10. Kontrak Pengadaan
    "GenLaravel_Project_Monitoring_Report.pdf",                  # 11. Monitoring & Kontrol
    "kesimpulan.pdf",                                            # 12. Kesimpulan
    "lampiran.pdf",                                              # 13. Lampiran
]

merger = PdfMerger()

for pdf in pdf_files:
    full_path = os.path.join(docs_path, pdf)
    if os.path.exists(full_path):
        print(f"✅ Adding: {pdf}")
        merger.append(full_path)
    else:
        print(f"❌ Not found: {pdf}")

output_path = os.path.join(docs_path, "GenLaravel_Laporan_UAS_Lengkap.pdf")
merger.write(output_path)
merger.close()

print(f"\n🎉 Merged PDF saved to: {output_path}")

# Count total pages
from PyPDF2 import PdfReader
reader = PdfReader(output_path)
print(f"📄 Total pages: {len(reader.pages)}")
