
# 08 PoC Narrative Playbook — Szablon Opisu Podatności i Dowodu Słuszności (PoC)

Ta notatka steruje strukturą tworzenia szczegółowych wpisów technicznych dotyczących pojedynczych podatności (Technical Finding / PoC Write-up). Służy do precyzyjnego opisania jak, gdzie i dlaczego dana luka występuje oraz jak ją powtórzyć.

---

## 🎯 Schemat Opisu Podatności (Technical Finding Flow)

1. NAGŁÓWEK I KLASYFIKACJA (Title, Asset, Severity, CWE)
   ↓
2. OPIS TECHNICZNY I PRZYCZYNA ŹRÓDŁOWA (Technical Description & Root Cause)
   ↓
3. DOWÓD SŁUSZNOŚCI / KROKI REPRODUKCJI (Step-by-Step PoC Narrative)
   ↓
4. DOWODY DZIAŁANIA / ARTEFAKTY (Evidence & Impact Proof)
   ↓
5. REKOMENDACJA TECHNICZNA (Detailed Technical Remediation)

---

## 🌲 Zasady Formowania Wpisu Technicznego

### Krok 1: Nagłówek i Identyfikacja
Każdy opis podatności musi zaczynać się od jednoznacznej identyfikacji:
* **Tytuł Findings:** Zwięzła nazwa wskazująca typ podatności i lokalizację (np. *SQL Injection w punkcie końcowym `/api/v1/search`*).
* **Klasyfikacja:** Poziom dotkliwości (Critical / High / Medium / Low / Info), wynik CVSS v3/v4 oraz identyfikator CWE (np. *CWE-89: SQL Injection*).
* **Dotknięty zasób:** Dokładny adres URL, parametr, usługa lub plik.

### Krok 2: Opis Techniczny (Technical Description & Root Cause)
Opisz zwięźle mechanizm powstania luki:
* Dlaczego system jest podatny (np. *brak sanityzacji danych wejściowych w filtrze wyszukiwania, przekazywanie zmiennych bezpośrednio do zapytania SQL*).
* Jaki warunek techniczny musi zostać spełniony, aby eksploatacja była możliwa.

### Krok 3: Szczegółowe Kroki Reprodukcji (Step-by-Step PoC)
Podaj ciąg kroków potrzebny do odtworzenia podatności przez zespół bezpieczeństwa lub deweloperów:
1. Stan początkowy (np. *Wymagane konto zwykłego użytkownika*).
2. Przygotowane żądanie HTTP lub komenda (używaj generycznych, bezpiecznych przykładów z adresami `127.0.0.1` / `example.com`).
3. Oczekiwana i faktyczna odpowiedź systemu.

### Krok 4: Dowód Wpływu (Impact & Evidence)
Wskazanie, co dokładnie atakujący osiąga po udanej eksploatacji (np. *odczyt bazy danych, wykonanie komendy, podniesienie uprawnień*).

### Krok 5: Remediacja Techniczna (Technical Remediation)
Podaj konkretne instrukcje naprawcze dla programistów / administratorów:
* Przykłady bezpiecznego kodu (np. *użycie Prepared Statements zamiast konkatenacji stringów*).
* Zmiany w konfiguracji (np. *wyłączenie niepotrzebnych procedur lub włączenie opcji hardeningowych*).

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* Przykłady w sekcji PoC muszą być czytelne, powtarzalne i jednoznaczne.
* ZAWSZE podawaj identyfikatory CWE oraz wytyczne naprawcze skierowane do zespołu deweloperskiego/technicznego.
* W opisach PoC używaj bezpiecznych adresów IP (np. `192.168.x.x`, `10.x.x.x`) oraz nazw domenowych (`example.com`).
* Oddzielaj opisy biznesowe (notatka 07) od technicznego opisu PoC (notatka 08). Notatka 08 służy do komunikacji z inżynierami i programistami.