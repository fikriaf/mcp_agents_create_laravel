from PyPDF2 import PdfReader
import os

docs_path = "frontend/docs"

pdf_files = [
    ("cover.pdf", "Cover"),
    ("Project Planning_Agent Auto Generate Laravel Project.pdf", "Latar Belakang & Masalah Proyek"),
    ("Kelompok 7_project_charter_scope.pdf", "Stakeholder, Scope Statement & Project Charter"),
    ("Kelompok 7_wbs.pdf", "Work Breakdown Structure (WBS)"),
    ("Kelompok 7_network_diagram.pdf", "Network Diagram"),
    ("Kelompok 7_scrum_gantt_chart.pdf", "Gantt Chart"),
    ("Kelompok 7_EVM_GenLaravel.pdf", "Anggaran & Earned Value Management (EVM)"),
    ("Kelompok 7_GenLaravel_Procurement Analysis.pdf", "Risiko & Procurement Analysis"),
    ("Kelompok 7_GenLaravel_Draft Dokumen Kontrak Pengadaan.pdf", "Draft Dokumen Kontrak Pengadaan"),
    ("GenLaravel_Project_Monitoring_Report.pdf", "Hasil Monitoring & Kontrol"),
]

current_page = 1
print("=" * 60)
print(f"{'Dokumen':<45} {'Hal':<5} {'Jumlah'}")
print("=" * 60)

for filename, title in pdf_files:
    full_path = os.path.join(docs_path, filename)
    if os.path.exists(full_path):
        reader = PdfReader(full_path)
        num_pages = len(reader.pages)
        print(f"{title:<45} {current_page:<5} {num_pages} hal")
        current_page += num_pages
    else:
        print(f"{title:<45} NOT FOUND")

print("=" * 60)
print(f"Total halaman: {current_page - 1}")
