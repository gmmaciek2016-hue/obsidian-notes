---

# Najważniejsza decyzja produktu

Masz **dwie możliwe drogi**.

## Droga 1 — narzędzie dla firm (SMB)

czyli:

- apteki
- przychodnie
- kancelarie
- sklepy e-commerce
- małe firmy

Twoja aplikacja byłaby wtedy:

NIS2 compliance tool

czyli:

- monitoring
- alerty
- raport NIS2

---

## Problem tej drogi

Firmy:

- nie rozumieją cyber
- nie chcą analizować logów
- nie wiedzą co to incydent

czyli będą pytać:

czy jesteśmy zgodni czy nie?

Nie będą korzystać z:

- investigation notebook
- log analysis
- evidence

---

# Droga 2 — narzędzie dla audytorów

czyli:

- firmy audytowe
- konsultanci cyber
- MSSP
- firmy compliance

Twoja aplikacja jest wtedy:

AI-powered audit workstation

czyli narzędzie pracy audytora.

---

## Audytorzy robią dziś

- analizę logów
- zbieranie evidence
- raporty
- dokumentację audytu

Twoja aplikacja przyspiesza ich pracę.

---

# Różnica jest ogromna

## Produkt dla firm

wartość:

50–200 € / miesiąc

## Produkt dla audytorów

wartość:

2000–10000 € / rok

bo to narzędzie pracy.

---

# Dlatego Twój projekt najlepiej pasuje do

AI SOC for auditors

albo

AI NIS2 Audit Platform

---

# Jak wygląda idealny produkt w tym modelu

Workflow audytu:

Audit Session  
     ↓  
Log Import  
     ↓  
Incident Detection  
     ↓  
Investigation Notebook  
     ↓  
Evidence Collection  
     ↓  
Compliance Score  
     ↓  
Audit Report

To dokładnie kierunek w którym już idziesz.

---

# Dlaczego Twoja architektura już do tego pasuje

Masz:

- **correlator.py** → analiza incydentów
- **RAG + LLM** → AI narrative
- **SQLite + sessions** → sesje audytu
- **Investigation Notebook UI**

To jest **idealna baza pod platformę audytową**.

---

# Jak powinna się nazywać Twoja aplikacja

Tylko:

AI-powered Incident Investigation  
and NIS2 Audit Platform

albo prościej:

AI NIS2 Audit Platform

---

# Najważniejsze funkcje Twojego MVP

Skup się tylko na tych 5:

### 1️⃣ Audit Sessions

zarządzanie audytami.

---

### 2️⃣ Log Import

upload logów.

---

### 3️⃣ Incident Investigation Notebook

analiza incydentów.

---

### 4️⃣ Evidence Locker

dowody audytowe.

---

### 5️⃣ NIS2 Report Generator

raport audytowy.

---

# Wtedy Twoja aplikacja robi

log analysis  
incident investigation  
evidence collection  
AI narrative  
compliance report

czyli **pełny audyt**.

---

# Moja szczera ocena projektu

Po tym co pokazałeś:

|element|ocena|
|---|---|
|pomysł|9/10|
|architektura|8/10|
|rynek|8.5/10|

Największy potencjał:

produkt dla audytorów

---

# Bardzo ważne pytanie strategiczne

Musisz zdecydować jedną rzecz: czy Twoja aplikacja ma być:

- AI tool dla audytora

- platforma compliance dla firm

---

**dokładnie jakie 7 ekranów powinna mieć Twoja aplikacja, żeby wyglądała jak profesjonalny produkt security (a nie projekt developerski).**

To jest bardzo ważne przy budowie startupu.

Pokażę Ci **7 ekranów, które powinny istnieć w Twojej aplikacji**, żeby wyglądała jak **profesjonalna platforma audytowa**, a nie projekt developerski.

To dokładnie odpowiada temu, co już projektujesz.

Twoje menu po lewej może wyglądać tak:

Dashboard  
Audit Sessions  
Log Import  
Incidents  
Investigation Notebook  
Evidence  
NIS2 Report  
Settings

Poniżej wyjaśnię **jak powinien wyglądać każdy ekran i co powinien robić**.

---

# 1. Audit Dashboard

To pierwszy ekran po wejściu do aplikacji.

Pokazuje **status audytu**.

### Elementy

**Compliance Score**

NIS2 Compliance Score  
  
72%  
  
Monitoring        ✔  
Detection         ✔  
Response          ⚠  
Recovery          ❌

---

**Audit overview**

Company: Medico Clinic  
Audit scope: NIS2  
Auditor: Jan Kowalski  
Created: 2026-04-28

---

**Statistics**

Logs analyzed      4321  
Incidents detected 3  
Evidence collected 8  
Controls checked   12

---

**Recent activity (Audit Trail)**

10:41 Session created  
10:43 Logs imported  
10:44 Incidents detected  
10:45 Investigation started

---

# 2. Audit Sessions

Lista audytów.

Tabela:

ID | Company | Scope | Auditor | Status | Date

Przykład:

1 | Medico Clinic | NIS2 | J.Kowalski | In Progress | 2026-04-28  
2 | PharmaNet     | NIS2 | M.Nowak    | Completed   | 2026-04-10

---

Przycisk:

+ New Audit Session

Formularz:

Company  
Auditor  
Scope  
Description

---

# 3. Log Import

Tu audytor ładuje logi.

UI:

Upload Logs

Obsługiwane:

auth.log  
syslog  
firewall.log  
ssh.log  
ids.log  
json logs

---

Po uploadzie:

Imported logs: 4312  
Sources detected:  
  
SSH  
Firewall  
System  
IDS

---

Pipeline:

Upload  
↓  
Parser  
↓  
Normalized logs  
↓  
Detection  
↓  
Incidents

---

# 4. Incidents

Lista wykrytych incydentów.

Tabela:

Severity | Incident | Source IP | Risk | Status

Przykład:

HIGH     SSH Brute Force        192.168.1.50   82  OPEN  
MEDIUM   Suspicious Login       10.0.0.12      60  INVESTIGATING  
LOW      Port Scan              172.16.1.10    35  CLOSED

Kliknięcie incydentu otwiera:

Investigation Notebook

---

# 5. Investigation Notebook

Najważniejszy ekran Twojej aplikacji.

To **centrum pracy audytora**.

Układ:

[Timeline]   [Evidence]   [AI Analysis]

---

### Timeline

10:45 Failed SSH login  
10:46 Failed SSH login  
10:47 Failed SSH login

---

### Evidence

auth.log lines  
firewall logs  
IDS alert

---

### AI Analysis

AI Analysis  
  
Repeated SSH authentication failures detected.  
  
This pattern indicates a brute force attack  
originating from IP 192.168.1.50.  
  
According to the organization's access control  
procedure such events should trigger monitoring.

---

# 6. Evidence Locker

Centralne miejsce dowodów audytu.

Tabela:

Control | Evidence | Source | Date

Przykład:

Monitoring        syslog logs        server1    2026-04-28  
Detection         firewall alerts    fw01       2026-04-28  
Access Control    ssh logs           server1    2026-04-28

---

Można dodać:

+ Add Evidence

Typ:

log fragment  
file  
screenshot  
comment

---

# 7. NIS2 Report

Generator raportu audytowego.

Sekcje:

### Executive Summary

This audit evaluated the organization's  
security monitoring and incident response  
capabilities according to NIS2 requirements.

---

### Findings

SSH brute force attempts detected  
Insufficient monitoring alerts  
Missing centralized logging

---

### Evidence

Lista dowodów.

---

### Compliance Score

Monitoring      PASS  
Detection       PASS  
Response        PARTIAL  
Recovery        FAIL

---

### Recommendations

Implement centralized logging  
Enable brute force protection  
Improve incident response procedures

---

# Idealna architektura menu

Twoje menu:

Audit Dashboard  
Audit Sessions  
Log Import  
Incidents  
Investigation Notebook  
Evidence  
NIS2 Report  
Settings

To jest **bardzo dobre**.

---

# Największa wartość Twojej aplikacji

Nie w:

log parsing

ale w:

Investigation Notebook  
Evidence  
AI Narrative  
Audit Report

To są **funkcje audytowe**.

---

# Moja szczera rada jako doradcy produktu

Nie dodawaj teraz nowych rzeczy typu:

SIEM  
real-time monitoring  
SOAR  
threat intelligence

Skup się na **workflow audytu**.

Pokażę Ci **5 modułów backendu**, które powinny istnieć w Twojej aplikacji, żeby kod był **czytelny, skalowalny i wyglądał jak prawdziwy produkt security**, a nie jeden duży plik `main.py`.

To dokładnie pasuje do tego co już zacząłeś robić (`AIEngine`, `RAGEngine`, `AuditService`).

---

# Idealna architektura backendu

Twoja aplikacja powinna być podzielona na **5 głównych modułów logiki**:

Audit Engine  
Log Engine  
Incident Engine  
Evidence Engine  
AI Engine

Każdy robi jedną rzecz.

---

# 1. Audit Engine

To moduł zarządzania audytami.

Plik:

app/services/audit_service.py

Odpowiada za:

tworzenie sesji audytu  
lista audytów  
status audytu  
audit timeline

---

### Funkcje

create_session()  
get_sessions()  
get_session()  
update_status()  
log_audit_event()

---

### Przykład

def create_session(company, auditor, scope):  
    conn = get_db()  
    cursor = conn.cursor()  
  
    cursor.execute(  
        "INSERT INTO audit_sessions (company, auditor, scope) VALUES (?, ?, ?)",  
        (company, auditor, scope)  
    )  
  
    conn.commit()  
    return cursor.lastrowid

---

# 2. Log Engine

Odpowiada za **upload i parsowanie logów**.

Plik:

app/services/log_service.py

---

### Funkcje

import_logs()  
parse_log_line()  
normalize_logs()  
store_logs()

---

### Pipeline

upload  
↓  
parser  
↓  
normalized logs  
↓  
database

---

### Przykład

def import_logs(session_id, content):  
  
    conn = get_db()  
  
    for line in content.splitlines():  
  
        conn.execute(  
            "INSERT INTO raw_logs (session_id, message) VALUES (?, ?)",  
            (session_id, line)  
        )  
  
    conn.commit()

---

# 3. Incident Engine

To **silnik wykrywania incydentów**.

Plik:

app/services/incident_service.py

---

### Funkcje

run_detection()  
detect_bruteforce()  
detect_scan()  
correlate_incidents()

---

### Pipeline

raw_logs  
↓  
rules  
↓  
alerts  
↓  
correlation  
↓  
incidents

---

### Przykład

def detect_bruteforce(logs):  
  
    failures = {}  
  
    for log in logs:  
        if "Failed password" in log["message"]:  
  
            ip = extract_ip(log["message"])  
  
            failures[ip] = failures.get(ip, 0) + 1  
  
    incidents = []  
  
    for ip, count in failures.items():  
        if count > 5:  
            incidents.append({  
                "title": "SSH Brute Force",  
                "src_ip": ip,  
                "severity": "HIGH"  
            })  
  
    return incidents

---

# 4. Evidence Engine

To **magazyn dowodów audytowych**.

Plik:

app/services/evidence_service.py

---

### Funkcje

add_evidence()  
get_evidence()  
attach_to_incident()

---

### Przykład

def add_evidence(session_id, control_code, description, file_path):  
  
    conn = get_db()  
  
    conn.execute(  
        """  
        INSERT INTO evidence  
        (session_id, control_code, description, file_path)  
        VALUES (?, ?, ?, ?)  
        """,  
        (session_id, control_code, description, file_path)  
    )  
  
    conn.commit()

---

# 5. AI Engine

To **najbardziej unikalny moduł Twojej aplikacji**.

Plik:

app/ai/ai_engine.py

---

### Funkcje

ask_llm()  
generate_incident_analysis()  
generate_audit_summary()  
generate_recommendations()

---

### Pipeline

incident  
↓  
RAG search  
↓  
procedure context  
↓  
LLM  
↓  
analysis

---

### Przykład

def generate_incident_analysis(logs, procedure):  
  
    prompt = f"""  
    Analyze this security incident.  
  
    Logs:  
    {logs}  
  
    Procedure:  
    {procedure}  
  
    Explain:  
    - what happened  
    - risk  
    - compliance impact  
    """  
  
    return ask_llm(prompt)

---

# Struktura projektu

Docelowo Twój projekt powinien wyglądać tak:

app  
 ├── main.py  
 ├── config.py  
  
 ├── routes  
 │    ├── audit_routes.py  
 │    ├── incident_routes.py  
 │    ├── evidence_routes.py  
 │    ├── report_routes.py  
  
 ├── services  
 │    ├── audit_service.py  
 │    ├── log_service.py  
 │    ├── incident_service.py  
 │    ├── evidence_service.py  
  
 ├── ai  
 │    ├── ai_engine.py  
 │    ├── rag_engine.py  
  
 ├── core  
 │    ├── parser.py  
 │    ├── rules_engine.py  
 │    ├── correlator.py  
  
 ├── templates  
 │    ├── dashboard.html  
 │    ├── investigation.html  
 │    ├── report.html  
  
data  
 ├── audit.db  
 ├── vector_db

---

# Dlaczego to jest ważne

Bo wtedy masz **czysty podział logiki**:

routes   → API  
services → logika biznesowa  
core     → analiza logów  
ai       → AI

Tak wygląda większość **produktów security**.

---

# Najważniejsza rada jako doradcy produktu

Nie rozbudowuj teraz:

parserów logów  
reguł detection

Największą wartością Twojego produktu są:

Investigation Notebook  
Evidence Engine  
AI Narrative  
NIS2 Report

### UWAGA
# NIS2 PLATFORM - AI Investigation & Audit MVP

## Cel projektu

Lokalna aplikacja wspierająca audytorów i zespoły security w małych podmiotach objętych dyrektywą NIS2. Łączy analizę logów, korelację incydentów i lokalne AI (RAG) do generowania raportów zgodności.

## Investigation Pipeline

1. **Log Import:** Pobieranie surowych danych z plików lokalnych.
    
2. **Rule Detection:** Proste silniki regułowe (np. wykrywanie brute-force).
    
3. **Correlation:** Grupowanie zdarzeń w incydenty o określonym ryzyku.
    
4. **AI Analysis:** Wykorzystanie Ollama (Llama3) do wyjaśnienia wektora ataku.
    
5. **Compliance Scoring:** Automatyczne wyliczanie dojrzałości NIS2 (Monitoring, Detection, Response).

## Struktura Katalogów

- `main.py`: Punkt wejścia aplikacji.
    
- `config.py`: Konfiguracja (ścieżki, URL Ollama).
    
- `app/ai/`: Integracja z lokalnym LLM.
    
- `templates/`: Interfejs użytkownika (Jinja2).
    
    - `layout.html`: Szablon bazowy (Sidebar, CSS).
        
    - `investigation.html`: Notebook śledczy (ten plik edytujemy).
        
    - `dashboard.html`: Lista sesji.

## Technologie

- **Backend:** Python / Flask
    
- **AI:** Ollama (Llama3)
    
- **DB:** SQLite (audit.db)
