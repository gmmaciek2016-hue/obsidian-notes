jak uruchomić RDP :

Nie widzisz paska Windows, ponieważ ==znajdujesz się na pulpicie systemu Linux (**THM AttackBox**), z którego dopiero musisz połączyć się z maszyną Windows za pomocą protokołu RDP==.

Aby zobaczyć system Windows i wykonać zadanie, wykonaj następujące kroki:

Jak uruchomić sesję RDP:

1. **Otwórz Terminal**: Kliknij dwukrotnie ikonę **Terminal** na pulpicie swojego AttackBoxa.
2. **Wpisz komendę połączenia**: Użyj programu `xfreerdp` (lub `remmina`), wpisując w terminalu:
    
    bash
    
    ```
    xfreerdp /v:10.129.113.160 /u:Administrator /p:HASŁO /dynamic-resolution +clipboard
    ```
    
    Używaj kodu z rozwagą.
    
    _(Zastąp słowo `HASŁO` faktycznym hasłem podanym w treści zadania na TryHackMe)._
3. **Zaakceptuj certyfikat**: Jeśli terminal zapyta o certyfikat bezpieczeństwa, wpisz `Y` lub `yes` i naciśnij Enter.

Po poprawnym zalogowaniu otworzy się nowe okno z pełnym pulpitem Windows i szukanym paskiem zadań.

Czy masz w treści zadania podane **hasło administratora** do tej maszyny Windows?

nie poszło zobacz : xfreerdp /v:10.129.113.160 /u:Administrator /p:N3w34829DJdd?1 /dynamic-resolution +clipboard

Problem polega na tym, że w hasłach zawierających znaki specjalne (takie jak **pytajnik `?`**), Linux interpretuje je jako symbole wieloznaczne (wildcards). Blokuje to poprawne przekazanie hasła do komendy `xfreerdp` i przerywa połączenie. [[1](https://medium.com/meetcyber/intro-to-credential-harvesting-cbc21e4e7fb8)]

Aby to naprawić, musisz **zamknąć hasło w pojedynczych cudzysłowach** `' '`.

Poprawna komenda do wpisania w terminalu:

bash

```
xfreerdp /v:10.129.113.160 /u:Administrator /p:'N3w34829DJdd?1' /dynamic-resolution +clipboard
```

Alternatywne rozwiązanie graficzne (Remmina):

Jeśli z jakiegoś powodu terminal nadal zgłasza błąd, użyj zainstalowanego na AttackBoxie programu graficznego: 

1. W lewym górnym rogu ekranu kliknij   **Applications -> Internet -> Remmina**.
2. Na górnym pasku programu zmień protokół z SSH na **RDP**.
3. Wpisz adres IP `10.129.113.160` i naciśnij Enter.
4. Gdy pojawi się okienko logowania, wprowadź standardowo login `Administrator` oraz hasło `N3w34829DJdd?1`.

Daj znać, czy po dodaniu cudzysłowów w terminalu lub po użyciu Remminy otworzyło Ci się **okno z pulpitem Windows**! [[1](https://medium.com/meetcyber/intro-to-credential-harvesting-cbc21e4e7fb8)]

==Wszystkie komendy związane z narzędziem Mimikatz musisz wpisać w **PowerShellu (lub CMD) wewnątrz okna RDP z systemem Windows**==.

Terminal Linux (AttackBox) służył wyłącznie do ustanowienia połączenia. Teraz wykonaj poniższe kroki bezpośrednio na pulpicie Windows:

Instrukcja wewnątrz okna RDP (Windows):

1. Wewnątrz okna Windows kliknij lupę (wyszukiwarkę) obok menu Start.
2. Wpisz **PowerShell**, kliknij na wynik prawym przyciskiem myszy i wybierz **Uruchom jako administrator** (Run as administrator).
3. W niebieskim oknie PowerShell przejdź do Pulpitu komendą:
    
    powershell
    
    ```
    cd C:\Users\Administrator\Desktop
    ```
    
    Używaj kodu z rozwagą.
    
4. Uruchom narzędzie:
    
    powershell
    
    ```
    .\mimikatz.exe
    ```
