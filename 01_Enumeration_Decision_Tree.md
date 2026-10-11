
# 01 Enumeration Decision Tree — Drzewo Decyzyjne Rekonesansu

Ta notatka określa kolejność działań podczas enumeracji po wykryciu otwartych portów.

---

## 🌲 Drzewo Portów i Usług

### 1. PORT 21 — FTP
* **Krok 1: Dostęp anonimowy**
  * *Pytanie:* Czy FTP zezwala na zalogowanie bez poświadczeń?
  * *Akcja:* Sprawdź `anonymous:anonymous` lub `ftp:ftp`.
  * *Zobacz:* `[[FTP_Anonymous_Access]]`
* **Krok 2: Wersja i podatności**
  * *Pytanie:* Czy wersja serwera ma znany exploit (np. vsftpd 2.3.4)?
  * *Akcja:* Wyszukaj wersję w searchsploit.
* **Krok 3: Analiza plików**
  * *Pytanie:* Czy na serwerze są ukryte pliki, backupy, klucze SSH?
  * *Akcja:* Pobierz wszystkie pliki w trybie binarnym (`mget *`).

---

### 2. PORT 80 / 443 — HTTP / HTTPS
* **Krok 1: Identyfikacja technologii**
  * *Pytanie:* Jaki to CMS, serwer www, język skryptowy?
  * *Zobacz:* `[[Web_Technology_Stack]]`
* **Krok 2: Enumeracja katalogów i zasobów**
  * *Pytanie:* Czy istnieją ukryte ścieżki, panele admina, pliki `.env`, `.git`?
  * *Akcja:* Gobuster / Feroxbuster z odpowiednią listą słów.
  * *Zobacz:* `[[Gobuster_Directory_Enum]]`
* **Krok 3: Vhosty i Subdomeny**
  * *Pytanie:* Czy serwer serwuje inne aplikacje pod nagłówkiem `Host`?
  * *Zobacz:* `[[FFUF_Vhost_Enumeration]]`

---

### 3. PORT 139 / 445 — SMB
* **Krok 1: Null Session / Anonymous Listing**
  * *Pytanie:* Czy możemy wyliczyć udziały sieciowe bez logowania?
  * *Akcja:* `smbclient -L //<IP>/ -N` lub `crackmapexec smb <IP> -u '' -p '' --shares`
  * *Zobacz:* `[[SMB_Share_Enumeration]]`
* **Krok 2: Full Enum (Users, Pass Pol, SID)**
  * *Pytanie:* Czy możemy wyciągnąć nazwiska użytkowników lub politykę haseł?
  * *Akcja:* `enum4linux-ng -A <IP>`
  * *Zobacz:* `[[Enum4linux_Usage]]`

---

### 4. PORT 88 / 389 / 636 — Kerberos & LDAP (Active Directory)
* **Krok 1: Anonymous LDAP Bind**
  * *Pytanie:* Czy LDAP udostępnia strukturę domeny anonimowo?
  * *Akcja:* `nmap -p 389 --script ldap-rootdse <IP>`
  * *Zobacz:* `[[LDAP_Anonymous_Bind]]`
* **Krok 2: User Enumeration**
  * *Pytanie:* Czy możemy wyliczyć poprawnych użytkowników domeny?
  * *Akcja:* Kerbrute userenum.
  * *Zobacz:* `[[Kerbrute_User_Enumeration]]`
* **Krok 3: AS-REP Roasting**
  * *Pytanie:* Czy istnieją konta z wyłączonym pre-authentication?
  * *Zobacz:* `[[ASREP_Roasting_Attack]]`

---

### 5. PORT 1433 / 3306 / 5432 — Bazy Danych (MSSQL / MySQL / Postgres)
* **Krok 1: Domyślne poświadczenia**
  * *Pytanie:* Czy działają konto `sa`, `root`, `postgres` z pustym lub domyślnym hasłem?
* **Krok 2: RCE przez bazę danych**
  * *Pytanie:* Czy mssql ma włączone `xp_cmdshell`?
  * *Zobacz:* `[[MSSQL_Command_Execution]]`

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* Gdy użytkownik zapyta *"co robić po znalezieniu portu X"*, natychmiast odnieś się do odpowiedniej sekcji tego drzewa decyzyjnego.
* Zawsze sugeruj wykonać najpierw **Krok 1** z danej sekcji, zanim przejdziesz do kolejnych.