### Prawidłowa procedura uruchomienia (najprostsza i najczystsza):

1. **Uruchom Kali w VirtualBox**
    - Włącz maszynę i poczekaj, aż się w pełni załaduje (do pulpitu lub loginu).
2. **(Opcjonalnie)** Sprawdź, czy SSH działa
    - Na hoście w **PowerShell** możesz przetestować:
        
        PowerShell
        
        ```
        ssh kali@IP_maszyny
        ```
        
    - To nie jest konieczne przy każdym uruchomieniu — tylko gdy chcesz się upewnić.
3. **Uruchom VS Code na hoście**
    - Otwórz VS Code
    - Kliknij w lewym dolnym rogu lub Ctrl+Shift+P → wpisz **Remote-SSH: Connect to Host...**
    - Wybierz swój host (np. kali)
4. Gotowe. VS Code sam nawiąże połączenie SSH i uruchomi serwer po stronie Kali.

---

### Czego **nie** robisz:

- Nie łączysz się ręcznie przez SSH z terminala **wewnątrz Kali**.
- Nie musisz najpierw otwierać PowerShell i trzymać tam sesji SSH.
- Nie musisz nic uruchamiać ręcznie na Kali (poza tym, że maszyna jest włączona).

---

### Krótka wersja „codziennej” procedury:

1. Włącz Kali w VirtualBox
2. Otwórz VS Code → połącz się z SSH: kali
3. Pracujesz

Oto przykładowa, dobra konfiguracja ~/.ssh/config na **hoście** (Windows).

### 1. Najpierw otwórz plik konfiguracyjny

W PowerShell:

PowerShell

```
notepad $env:USERPROFILE\.ssh\config
```

Jeśli plik nie istnieje — Notepad go utworzy.

---

### 2. Przykładowa konfiguracja

#### Wariant A – Najczęstszy (NAT + Port Forwarding w VirtualBox)

sshconfig

```
Host kali
    HostName 127.0.0.1
    User kali
    Port 2222                  # port, który ustawiłeś w Port Forwarding
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

#### Wariant B – Bridged / Host-Only (Kali ma własne IP w sieci)

sshconfig

```
Host kali
    HostName 192.168.56.101    # IP Twojej maszyny Kali
    User kali
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

---

### 3. Dodatkowe dobre ustawienia (opcjonalnie)

Możesz dodać na górę pliku:

sshconfig

```
Host *
    AddKeysToAgent yes
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

---

### 4. Co oznaczają najważniejsze linie:

|Linia|Znaczenie|
|---|---|
|Host kali|Nazwa, którą wybierasz w VS Code|
|HostName|IP lub localhost|
|User kali|Użytkownik na Kali|
|Port|Port SSH (ważne przy NAT)|
|IdentityFile|Ścieżka do klucza prywatnego|
|ServerAliveInterval|Utrzymuje połączenie, żeby nie wygasało|

---

### 5. Po zapisaniu

W VS Code:

1. Ctrl + Shift + P
2. Wpisz: **Full Reassessment**
3. Wybierz **kali**
