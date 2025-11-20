# Praktikum: Gantt Chart SCRUM - Proyek GenLaravel

## Deskripsi Proyek

**GenLaravel** adalah AI-powered Laravel code generator yang menggunakan multi-agent system untuk menghasilkan aplikasi Laravel lengkap dari prompt natural language. Proyek ini menggunakan metodologi SCRUM untuk pengembangan sistematis.

## Output yang Harus Dikumpulkan

- Product Backlog
- Sprint Backlog (3 Sprint)
- Gantt Chart lengkap 4 minggu
- Assignment role Scrum (PO, SM, Dev, QA)
- Screenshot tampilan Gantt Chart Notion

## Timeline Proyek

Proyek berjalan selama **4 minggu**:

- **Sprint 1**: 18–24 November 2024 (Foundation & Core Agents)
- **Sprint 2**: 25 Nov – 8 Desember 2024 (Multi-Page & Enhancement)
- **Sprint 3**: 9–15 Desember 2024 (Testing, Optimization, Deploy)

## Struktur Scrum dan Tanggung Jawab

### SCRUM Roles

- **Product Owner (PO)**: Requirements, Backlog prioritization, Sprint review
- **Scrum Master (SM)**: Sprint planning, Daily standup, Remove blockers
- **AI/ML Engineer**: LLM integration, Agent orchestration, Prompt engineering
- **Backend Developer**: FastAPI server, WebSocket, Agent pipeline
- **Frontend Developer**: Web UI, Real-time updates, User experience
- **QA Tester**: Agent validation, Integration testing, Bug fixing

---

## 1. Struktur Proyek Secara Umum

Proyek GenLaravel berjalan selama 4 minggu, dibagi menjadi 3 Sprint berdasarkan SCRUM.

### ✔ SCRUM Roles

- **Product Owner (PO)** → Vision, feature prioritization, acceptance criteria
- **Scrum Master (SM)** → Sprint management, team coordination, impediment removal
- **Dev Team**:
  - AI/ML Engineer (Agent development)
  - Backend Developer (API & orchestration)
  - Frontend Developer (UI/UX)
  - QA Tester (Validation & testing)

### ✔ Output Besar (Deliverables)

- **Sprint 1** → Core agent system + Single-page generation
- **Sprint 2** → Multi-page support + Web interface
- **Sprint 3** → Optimization + Testing + Documentation

---

## 2. Timeline 4 Minggu (High-Level)

| Minggu      | Sprint   | Kegiatan Utama                                    |
|-------------|----------|---------------------------------------------------|
| 18–24 Nov   | Sprint 1 | Foundation + Core Agents + Single-page            |
| 25–1 Des    | Sprint 2 | Multi-page system + Web UI                        |
| 2–8 Des     | Sprint 2 | Enhancement + Auto-fix utilities                  |
| 9–15 Des    | Sprint 3 | Testing + Optimization + Documentation + Deploy   |

---

## 3. Fase Proyek (Waterfall yang Dipetakan ke SCRUM)

### FASE 1 – FOUNDATION & SETUP (Sprint 1)

- Setup project structure
- Configure LLM clients (Cerebras + Mistral)
- Design agent architecture
- Create base orchestrator (main.py)
- Setup environment & dependencies

**Output**: Project foundation + LLM integration  
**Durasi**: 18–19 Nov  
**Dependency**: –  
**Role**: Backend Dev, AI/ML Engineer

---

### FASE 2 – CORE AGENTS DEVELOPMENT (Sprint 1)

- Agent 1: Prompt Expander
- Agent 2: Draft Agent (HTML preview)
- Agent 3: Prompt Planner
- Agent 4: Page Architect
- Agent 5: Layout Generator

**Output**: 5 core agents functional  
**Durasi**: 20–22 Nov  
**Dependency**: Foundation selesai  
**Role**: AI/ML Engineer, Backend Dev

---

### FASE 3 – BLADE GENERATION AGENTS (Sprint 1)

- Agent 6: UI Generator (Blade views)
- Agent 7: Route Agent
- Agent 8: Component Agent
- Agent 9: Validator Agent
- Agent 10: Project Mover

**Output**: Complete agent pipeline  
**Durasi**: 23–24 Nov  
**Dependency**: Core agents selesai  
**Role**: AI/ML Engineer, Backend Dev

---

### FASE 4 – WEB INTERFACE DEVELOPMENT (Sprint 2)

- Design frontend UI/UX
- Build FastAPI backend server
- Implement WebSocket for real-time updates
- Create single-page interface
- Daily limit tracker (5 gen/day)

**Output**: Web interface functional  
**Durasi**: 25–28 Nov  
**Dependency**: Agent pipeline selesai  
**Role**: Frontend Dev, Backend Dev

---

### FASE 5 – MULTI-PAGE SYSTEM (Sprint 2)

- Enhanced Draft Agent V2
- Enhanced Planner V2
- Enhanced Route Agent V2
- Multi-page orchestrator
- Tabbed preview system

**Output**: Multi-page generation support  
**Durasi**: 29 Nov – 2 Des  
**Dependency**: Web interface selesai  
**Role**: AI/ML Engineer, Backend Dev

---

### FASE 6 – UTILITIES & AUTO-FIX (Sprint 2)

- Clean project utility
- Fix nested UI utility
- Fix draft styling utility
- Auto-fix multi-page utility
- Validation utilities

**Output**: Complete utility suite  
**Durasi**: 3–5 Des  
**Dependency**: Multi-page selesai  
**Role**: Backend Dev, QA Tester

---

### FASE 7 – INTEGRATION & ENHANCEMENT (Sprint 2)

- Laravel project integration
- Browser auto-launch
- History management
- Component validation
- Route synchronization

**Output**: Seamless Laravel integration  
**Durasi**: 6–8 Des  
**Dependency**: Utilities selesai  
**Role**: Backend Dev, QA Tester

---

### FASE 8 – TESTING & VALIDATION (Sprint 3)

- Unit testing agents
- Integration testing pipeline
- End-to-end testing
- Bug fixing
- Performance optimization

**Output**: Stable tested system  
**Durasi**: 9–11 Des  
**Dependency**: Integration selesai  
**Role**: QA Tester, All Team

---

### FASE 9 – DOCUMENTATION (Sprint 3)

- README.md (main)
- README_MULTI_PAGE.md
- Architecture diagrams (PlantUML)
- Code documentation
- User guide

**Output**: Complete documentation  
**Durasi**: 12–13 Des  
**Dependency**: Testing selesai  
**Role**: PO, All Team

---

### FASE 10 – DEPLOYMENT & DEMO (Sprint 3)

- Final testing
- Demo preparation
- Repository cleanup
- Screenshots & demo assets
- Project presentation

**Output**: Production-ready system  
**Durasi**: 14–15 Des  
**Dependency**: Documentation selesai  
**Role**: All Team

---

## 4. Gambaran Dependencies

```
Foundation → Core Agents → Blade Agents → Web Interface
                ↓              ↓              ↓
           Agent Pipeline → Multi-Page → Utilities → Integration
                                            ↓
                                    Testing → Documentation → Deploy
```

### Inti dependency:

- Tidak bisa develop agents tanpa foundation
- Tidak bisa buat web interface tanpa agent pipeline
- Tidak bisa multi-page tanpa web interface
- Tidak bisa utilities tanpa multi-page system
- Tidak bisa integration tanpa utilities
- Tidak bisa testing tanpa integration
- Tidak bisa documentation tanpa testing
- Tidak bisa deploy tanpa documentation

---

## 5. GAMBARAN GANTT CHART AKHIR (Sederhana & Jelas)

Gambaran yang nanti muncul di Notion:

### Sprint 1 (18—24 Nov) - Foundation & Core Agents
```
|== Foundation Setup ==|
|========== Core Agents (1-5) ==========|
|========== Blade Agents (6-10) ==========|
```

### Sprint 2 (25 Nov—8 Des) - Enhancement & Features
```
|======== Web Interface ========|
|========== Multi-Page System ==========|
|====== Utilities & Auto-Fix ======|
|======== Laravel Integration ========|
```

### Sprint 3 (9—15 Des) - Testing & Deploy
```
|======== Testing & Validation ========|
|==== Bug Fix ====|
|==== Documentation ====|
|=== Deploy & Demo ===|
```

**Catatan**:
- Warna berbeda → Role berbeda
- Bar yang berhubungan → Dependencies
- Panjang bar → Durasi task

---

## 6. GAMBARAN TOTAL: WBS + SCRUM + TIMELINE + DEPENDENCY

### Big Picture Workflow

1. **Sprint 1 (Foundation & Core)**
   - Backend Dev + AI/ML: Setup project, LLM integration
   - AI/ML Engineer: Develop 10 agents (sequential pipeline)
   - Backend Dev: Orchestrator & file management

2. **Sprint 2 (Enhancement & Features)**
   - Frontend Dev: Web UI, real-time updates, WebSocket
   - Backend Dev: FastAPI server, daily limit tracker
   - AI/ML Engineer: Multi-page system, enhanced agents
   - Backend Dev: Utilities & auto-fix tools

3. **Sprint 3 (Quality & Delivery)**
   - QA Tester: Comprehensive testing, bug fixing
   - All Team: Performance optimization
   - PO + All Team: Documentation & user guide
   - All Team: Demo preparation & deployment

### Architecture Flow

![Architecture Flow Diagram](architecture_flow_diagram.puml)

---

## 7. Kesimpulan

Inilah gambaran lengkap yang kalian butuhkan:

✔ Mahasiswa tahu **apa** yang dikerjakan  
✔ Mahasiswa tahu **kapan** dikerjakan (tanggal & durasi)  
✔ Mahasiswa tahu **siapa** yang mengerjakan (SCRUM role)  
✔ Mahasiswa tahu **urutan logis** antar task (dependencies)  
✔ Mahasiswa tahu **bagaimana** mengimplementasikan semuanya ke Gantt Chart

---

## Product Backlog - GenLaravel

| ID | User Story | Priority | Sprint | Assignee | Status |
|----|-----------|----------|--------|----------|--------|
| 1  | Sebagai developer, saya ingin setup project foundation dengan LLM integration | High | 1 | Backend Dev, AI/ML | Done |
| 2  | Sebagai developer, saya ingin agent yang bisa expand prompt user | High | 1 | AI/ML Engineer | Done |
| 3  | Sebagai user, saya ingin preview HTML draft sebelum generate Laravel | High | 1 | AI/ML Engineer | Done |
| 4  | Sebagai developer, saya ingin agent yang bisa plan component structure | High | 1 | AI/ML Engineer | Done |
| 5  | Sebagai developer, saya ingin agent yang bisa design page layout | High | 1 | AI/ML Engineer | Done |
| 6  | Sebagai developer, saya ingin agent yang bisa generate Blade views | High | 1 | AI/ML Engineer | Done |
| 7  | Sebagai developer, saya ingin agent yang bisa generate Laravel routes | High | 1 | AI/ML Engineer | Done |
| 8  | Sebagai developer, saya ingin agent yang bisa extract components | High | 1 | AI/ML Engineer | Done |
| 9  | Sebagai developer, saya ingin agent yang bisa validate generated code | High | 1 | AI/ML Engineer | Done |
| 10 | Sebagai developer, saya ingin agent yang bisa move files ke Laravel project | High | 1 | AI/ML Engineer | Done |
| 11 | Sebagai user, saya ingin web interface untuk generate UI | High | 2 | Frontend Dev | Done |
| 12 | Sebagai user, saya ingin real-time progress updates | Medium | 2 | Backend Dev | Done |
| 13 | Sebagai user, saya ingin daily limit tracker (5 gen/day) | Medium | 2 | Backend Dev | Done |
| 14 | Sebagai user, saya ingin generate multiple pages sekaligus | High | 2 | AI/ML Engineer | Done |
| 15 | Sebagai user, saya ingin preview semua pages dengan tabs | Medium | 2 | AI/ML Engineer | Done |
| 16 | Sebagai developer, saya ingin utility untuk clean project | Medium | 2 | Backend Dev | Done |
| 17 | Sebagai developer, saya ingin auto-fix untuk nested UI issues | Medium | 2 | Backend Dev | Done |
| 18 | Sebagai developer, saya ingin auto-fix untuk route conversion | Medium | 2 | Backend Dev | Done |
| 19 | Sebagai developer, saya ingin comprehensive testing suite | High | 3 | QA Tester | In Progress |
| 20 | Sebagai user, saya ingin dokumentasi lengkap cara penggunaan | High | 3 | PO, All Team | In Progress |

## Sprint Backlog

### Sprint 1 (18-24 Nov) - Foundation & Core Agents

| Task | Description | Assignee | Estimate | Status |
|------|-------------|----------|----------|--------|
| Setup Project | Initialize project structure, dependencies | Backend Dev | 0.5 hari | Done |
| LLM Integration | Configure Cerebras + Mistral clients | Backend Dev, AI/ML | 0.5 hari | Done |
| Agent Architecture | Design multi-agent system architecture | AI/ML Engineer | 1 hari | Done |
| Agent 1: Prompt Expander | Develop prompt expansion agent | AI/ML Engineer | 0.5 hari | Done |
| Agent 2: Draft Agent | Develop HTML draft preview agent | AI/ML Engineer | 0.5 hari | Done |
| Agent 3: Prompt Planner | Develop component planning agent | AI/ML Engineer | 0.5 hari | Done |
| Agent 4: Page Architect | Develop layout design agent | AI/ML Engineer | 0.5 hari | Done |
| Agent 5: Layout Generator | Develop app.blade.php generator | AI/ML Engineer | 0.5 hari | Done |
| Agent 6: UI Generator | Develop Blade view generator | AI/ML Engineer | 0.5 hari | Done |
| Agent 7: Route Agent | Develop route generator | AI/ML Engineer | 0.5 hari | Done |
| Agent 8: Component Agent | Develop component extractor | AI/ML Engineer | 0.5 hari | Done |
| Agent 9: Validator | Develop code validator | AI/ML Engineer | 0.5 hari | Done |
| Agent 10: Project Mover | Develop Laravel integration agent | AI/ML Engineer | 0.5 hari | Done |
| Main Orchestrator | Build main.py orchestrator | Backend Dev | 1 hari | Done |

### Sprint 2 (25 Nov - 8 Des) - Enhancement & Features

| Task | Description | Assignee | Estimate | Status |
|------|-------------|----------|----------|--------|
| Frontend UI Design | Design web interface mockup | Frontend Dev | 1 hari | Done |
| FastAPI Backend | Build backend server | Backend Dev | 1 hari | Done |
| WebSocket Integration | Implement real-time updates | Backend Dev | 1 hari | Done |
| Single-Page Interface | Build single-page generation UI | Frontend Dev | 1 hari | Done |
| Daily Limit Tracker | Implement 5 gen/day limit | Backend Dev | 0.5 hari | Done |
| Draft Agent V2 | Enhance for multi-page support | AI/ML Engineer | 1 hari | Done |
| Planner V2 | Enhance for multi-page detection | AI/ML Engineer | 1 hari | Done |
| Route Agent V2 | Enhance for multiple routes | AI/ML Engineer | 1 hari | Done |
| Multi-Page Orchestrator | Build main_multi_page.py | Backend Dev | 1 hari | Done |
| Tabbed Preview | Implement tab navigation for drafts | Frontend Dev | 0.5 hari | Done |
| Clean Utility | Build clean_project.py | Backend Dev | 0.5 hari | Done |
| Fix Nested UI | Build fix_nested_ui.py | Backend Dev | 0.5 hari | Done |
| Fix Draft Styling | Build fix_draft_styling.py | Backend Dev | 0.5 hari | Done |
| Auto-Fix Multi-Page | Build auto_fix_multi_page.py | Backend Dev | 0.5 hari | Done |
| Validation Utilities | Build validate_components.py | Backend Dev | 0.5 hari | Done |
| Laravel Integration | Seamless file moving & route sync | Backend Dev | 1 hari | Done |
| Browser Auto-Launch | Auto-open preview & localhost | Backend Dev | 0.5 hari | Done |

### Sprint 3 (9-15 Des) - Testing & Deploy

| Task | Description | Assignee | Estimate | Status |
|------|-------------|----------|----------|--------|
| Unit Testing | Test individual agents | QA Tester | 1 hari | In Progress |
| Integration Testing | Test agent pipeline | QA Tester | 1 hari | In Progress |
| E2E Testing | Test complete workflow | QA Tester | 1 hari | Todo |
| Bug Fixing | Fix identified issues | All Team | 1 hari | In Progress |
| Performance Optimization | Optimize LLM calls & speed | Backend Dev | 0.5 hari | Todo |
| README.md | Write main documentation | PO | 0.5 hari | Done |
| README_MULTI_PAGE.md | Write multi-page guide | PO | 0.5 hari | Done |
| Architecture Diagrams | Create PlantUML diagrams | Backend Dev | 0.5 hari | Done |
| Code Documentation | Add inline documentation | All Team | 0.5 hari | In Progress |
| User Guide | Write usage tutorial | PO | 0.5 hari | Todo |
| Demo Preparation | Prepare screenshots & demo | All Team | 0.5 hari | Todo |
| Repository Cleanup | Clean & organize files | Backend Dev | 0.5 hari | Todo |
| Final Testing | Complete system test | QA Tester | 0.5 hari | Todo |
| Deployment | Deploy & publish | All Team | 0.5 hari | Todo |

---

**Catatan**: Silakan masukkan gambar/screenshot Gantt Chart dari Notion pada bagian yang ditandai dengan `![...]`
