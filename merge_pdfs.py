from PyPDF2 import PdfMerger
import os

# Urutan PDF sesuai instruksi:
# 1. Latar belakang & masalah proyek
# 2. Stakeholder & Scope Statement  
# 3. Project Charter
# 4. WBS & Network Diagram
# 5. Gantt Chart
# 6. Anggaran & EVM
# 7. Risiko & Procurement
# 8. Hasil monitoring & kontrol
# 9. Kesimpulan (belum ada PDF, skip dulu)

docs_path = "frontend/docs"

pdf_files = [
    "cover.pdf",                                                 # 0. Cover
    "Project Planning_Agent Auto Generate Laravel Project.pdf",  # 1. Latar belakang
    "Kelompok 7_project_charter_scope.pdf",                      # 2-3. Stakeholder, Scope, Charter
    "Kelompok 7_wbs.pdf",                                        # 4. WBS
    "Kelompok 7_network_diagram.pdf",                            # 4. Network Diagram
    "Kelompok 7_scrum_gantt_chart.pdf",                          # 5. Gantt Chart
    "Kelompok 7_EVM_GenLaravel.pdf",                             # 6. Anggaran & EVM
    "Kelompok 7_GenLaravel_Procurement Analysis.pdf",            # 7. Risiko & Procurement
    "Kelompok 7_GenLaravel_Draft Dokumen Kontrak Pengadaan.pdf", # 7. Kontrak Pengadaan
    "GenLaravel_Project_Monitoring_Report.pdf",                  # 8. Monitoring & Kontrol
]

merger = PdfMerger()

for pdf in pdf_files:
    full_path = os.path.join(docs_path, pdf)
    if os.path.exists(full_path):
        print(f"✅ Adding: {pdf}")
        merger.append(full_path)
    else:
        print(f"❌ Not found: {pdf}")

output_path = os.path.join(docs_path, "GenLaravel_Complete_Project_Documentation.pdf")
merger.write(output_path)
merger.close()

print(f"\n🎉 Merged PDF saved to: {output_path}")
