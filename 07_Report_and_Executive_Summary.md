
# 07 Report and Executive Summary Playbook — Raportowanie i Podsumowanie Menedżerskie

Ta notatka steruje logiką tłumaczynia skomplikowanych podatności technicznych na język wpływu biznesowego, oceny ryzyka oraz rekomendacji strategicznych dla zarządu (C-Level, CISO, Zarząd).

---

## 🎯 Struktura Podsumowania Menedżerskiego (Executive Summary Flow)

1. OGÓLNY POZIOM RYZYKA I WNIOSKI (TL;DR & Overall Risk Score)
   ↓
2. WPŁYW BIZNESOWY I ZGODNOŚĆ (Business Impact & Compliance)
   ↓
3. MACIERZ KLUCZOWYCH PODATNOŚCI (Key Findings Matrix)
   ↓
4. STRATEGICZNA MAPA DROGOWA NAPRAWY (Prioritized Remediation Roadmap)

---

## 🌲 Zasady Formowania Raportu Menedżerskiego

### Krok 1: Ocena Poziomu Ryzyka (Overall Risk Rating)
* **Kryteria wyceny:**
  * **KRYTYCZNY (Critical):** Bezpośrednie przejęcie infrastruktury, kontrolera domeny, wyciek danych wrażliwych bez uwierzytelnienia.
  * **WYSOKI (High):** Wykonanie komend na serwerze (RCE) po uwierzytelnieniu, lokalna eskalacja uprawnień (PrivEsc), SQL Injection.
  * **ŚREDNI (Medium):** Podatności XSS, słaba konfiguracja szyfrowania, ujawnienie informacji (Information Disclosure).
  * **NISKI (Low):** Brak nagłówków bezpieczeństwa, wygasłe certyfikaty na środowiskach testowych.

### Krok 2: Tłumaczenie Techniki na Wpływ Biznesowy (BIA)
* **Zasada:** Nigdy nie zostawiaj samej nazwy podatności. Zawsze połącz ją z konsekwencją dla organizacji.
* **Przykłady mapowania:**
  * *SQL Injection / RCE* → **Ryzyko:** Całkowite przejęcie bazy danych klientów, zatrzymanie procesów operacyjnych, kar finansowe (RODO/NIS2).
  * *Brak izolacji sieci (Pivoting)* → **Ryzyko:** Przejście z podatnego serwera www do wewnętrznej sieci produkcyjnej i systemów finansowych.
  * *Słabe hasła / Lack of MFA* → **Ryzyko:** Podatność na ataki typu Password Spraying i przejęcie tożsamości pracowników.

### Krok 3: Tabela Wyników (Key Findings Table)
Każdy raport menedżerski musi zawierać zwięzłą tabelę podsumowującą:

| Podatność | Poziom Ryzyka | Zainfekowany Zasób | Wysiłek Naprawczy |
| :--- | :--- | :--- | :--- |
| *Nazwa* | *Critical / High / Med / Low* | *IP / Host / Usługa* | *Niski / Średni / Wysoki* |

### Krok 4: Priorytetyzacja Naprawcza (Remediation Roadmap)
Dziel rekomendacje na 3 horyzonty czasowe:
1. **Natychmiastowe (24–48h):** Izolacja zasobów, zmiana poświadczeń, wyłącznie podatnych usług/funkcji.
2. **Krótkoterminowe (1–2 tygodnie):** Instalacja łat (patching), zmiana konfiguracji, wdrożenie zasad Least Privilege.
3. **Długoterminowe (1–3 miesiące):** Twardnienie infrastruktury (Hardening), segmentacja sieci, szkolenia budowania bezpiecznego kodu.

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* W sekcji Podsumowania Menedżerskiego ZAKAZUJĘ używania surowych komend terminala, skryptów exploitów oraz żargonu wyłącznie technicznego.
* ZAWSZE używaj języka korzyści i ryzyka biznesowego (Częstotliwość, Wpływ, Ciągłość Działania, Zgodność z NIS2 / RODO).
* Raport musi być napisany w sposób zrozumiały dla osoby nie-technicznej (Dyrektor Finansowy, Prezes, Członek Zarządu).
* ZAWSZE podawaj konkretną, skategoryzowaną macierz podatności oraz priorytetyzowaną mapę drogową naprawy.
* Jeśli kontekst dotyczy audytu sieci wewnętrznej, ZAWSZE podkreślaj ryzyko ruchu bocznego (Lateral Movement) i braku segmentacji.