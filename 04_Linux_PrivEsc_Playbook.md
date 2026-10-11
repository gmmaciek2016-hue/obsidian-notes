
```
# 04 Linux PrivEsc Playbook — Eskalacja Uprawnień w Linux

Ta notatka steruje logiką podnoszenia uprawnień z użytkownika nisko uprzywilejowanego do `root` na systemach Linux.

---

## 🎯 Metodologia Eskalacji (Linux PrivEsc Flow)

```

1. SYSTEM & ENVIRONMENT ENUMERATION (Kto ja jestem? Co tu działa?) ↓
    
2. AUTOMATED ENUMERATION (Uruchomienie skryptów rozpoznawczych) ↓
    
3. MANUAL PRIVILEGE CHECKS (Sudo, SUID, Capabilities, Cron) ↓
    
4. EXPLOITATION & ROOT (Wykorzystanie GTFOBins lub Exploitów Kernel)
    

```

---

## 🌲 Drzewo Decyzyjne Eskalacji Uprawnień

### Krok 1: Automatyczne Skrypty Rozpoznawcze
* **Pytanie:** Co skrypty automatyczne wykryły w pierwszej kolejności?
* **Akcja:** Uruchom `linpeas.sh` lub `linenum.sh` z pamięci / katalogu `/tmp`.
* **Zobacz:** `[[Linpeas_Usage]]`

---

### Krok 2: Manualna Analiza Wektorów (Główne Furtki)

Wektor | Pytanie Sprawdzające | Komenda | Zobacz
---|---|---|---
**Sudo Rules** | Czy użytkownik może uruchomić cokolwiek jako root bez hasła? | `sudo -l` | `[[Sudo_PrivEsc_GTFOBins]]`
**Pliki SUID/SGID** | Czy istnieją pliki z bitem SUID należące do roota? | `find / -perm -4000 -type f 2>/dev/null` | `[[SUID_Exploitation]]`
**Capabilities** | Czy binarne pliki mają nadane specjalne uprawnienia? | `getcap -r / 2>/dev/null` | `[[Linux_Capabilities]]`
**Cron Jobs** | Czy zadania w tle uruchamiają edytowalne skrypty jako root? | `cat /etc/crontab` lub `pspy64` | `[[Cron_Jobs_PrivEsc]]`
**Wersja Kernela** | Czy wersja jądra Linux jest podatna na znany exploit (np. Dirty Pipe)? | `uname -a` | `[[Kernel_Exploits_Linux]]`

---

### Krok 3: Przeszukiwanie Plików i Poświadczeń w Systemie
* **Pytanie:** Czy w systemie znajdują się zapisane hasła w plikach konfiguracyjnych, historii bash lub procesach?
* **Akcja:**
  * Historia komend: `cat ~/.bash_history`
  * Pliki www/konfiguracyjne: `grep -i "password" /var/www/html/*`
  * Nasłuchujące porty lokalne (Loopback): `ss -tulpn` lub `netstat -tlpn` (sprawdzenie usług dostępnych tylko na `127.0.0.1`).

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* Gdy użytkownik napisze "mam dostęp do powłoki / zdobyłem użytkownika X", Twoim pierwszym krokiem musi być polecenie sprawdzenia `sudo -l` oraz uruchomienia `linpeas.sh`.
* Jeśli w wynikach pojawi się jakikolwiek plik z uprawnieniem Sudo lub SUID, wskaż serwis **GTFOBins** jako źródło gotowej komendy eskalacyjnej.
* Zawsze sprawdzaj usługi nasłuchujące na `127.0.0.1` — mogą to być wewnętrzne aplikacje podatne na lokalne atakowanie.
```