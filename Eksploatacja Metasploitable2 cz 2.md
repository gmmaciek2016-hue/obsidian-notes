
## **1. Analiza wyników**

Pogrupujmy wykryte usługi, żeby nie analizować ich chaotycznie.

|Obszar|Porty|Co wykryliśmy|
|---|---|---|
|Dostęp zdalny|22, 23, 5900|SSH, Telnet, VNC|
|FTP|21, 2121|vsftpd, ProFTPD|
|WWW|80, 8009, 8180|Apache, AJP13, Tomcat|
|Poczta i DNS|25, 53|Postfix, BIND|
|SMB / Windows networking|139, 445|Samba|
|Zdalne wykonywanie poleceń|512, 513, 514|rexec, rlogin, rsh|
|Bazy danych|3306, 5432|MySQL, PostgreSQL|
|RPC / NFS|111, 2049 i porty wysokie|rpcbind, NFS|
|Pozostałe|1099, 1524, 3632, 6667, 6697, 8787, 59991|RMI, bindshell, distccd, IRC, Ruby DRb|

## **2. Najciekawsze znaleziska**

Kilka pozycji zasługuje na szczególną uwagę:

**1524/tcp – Metasploitable root shell**                                                                Krytyczne
Usługa opisana przez Nmap jako `Metasploitable root shell`. To bezpośrednio udostępniona powłoka z uprawnieniami root. W rzeczywistym systemie byłaby to sytuacja alarmowa.


**21/tcp – vsftpd 2.3.4**                                                                                       Wysokie ryzyko
Bardzo stara wersja serwera FTP, znana z historycznego incydentu z backdoorem. Warto zweryfikować konkretną usługę, nie zakładając podatności wyłącznie na podstawie numeru wersji.

**6667/tcp – UnrealIRCd**                                                                                 Wysokie ryzyko
Serwer IRC. Niektóre historyczne wersje UnrealIRCd były dystrybuowane z backdoorem.

**3632/tcp – distccd**                                                                                        Do analizy
Usługa rozproszonej kompilacji. Jej nieprawidłowa konfiguracja może umożliwić zdalne wykonywanie poleceń.

**139/445 – Samba**                                                                                         Do analizy
Usługa udostępniania zasobów sieciowych. Sprawdzimy wersję, dostępne udziały i sposób uwierzytelniania.

Ważna uwaga: Nmap identyfikuje usługi i wersje, ale sam wynik nie potwierdza, że każda z nich jest podatna. To dopiero punkt wyjścia do dalszej enumeracji.

## **3. Co robimy dalej?**

Proponuję nie skanować teraz wszystkich usług dodatkowymi skryptami. Wybierzmy jedną i przeprowadźmy pełną enumerację.

Moja rekomendacja: **Samba (139/445)**.

Dlaczego?

- Jest to usługa często spotykana w środowiskach firmowych.
- Pozwala ćwiczyć enumerację udziałów sieciowych.
- Wiedza przyda się później podczas pracy z Active Directory.
- Możemy nauczyć się odróżniać dostęp anonimowy od dostępu wymagającego uwierzytelnienia.

## **4. Pierwszy krok – enumeracja Samby** 139, 445

W Kali wykonaj tylko:

```
nmap -p 139,445 --script smb-os-discovery,smb-protocols 192.168.56.104
```

Co sprawdzamy:

- `smb-os-discovery` – próba identyfikacji systemu i informacji o hoście.
- `smb-protocols` – wykrywanie obsługiwanych wersji protokołu SMB.
- `-p 139,445` – ograniczamy skan do portów Samby.

## **1. Analiza wyniku**

**SMBv1 – NT LM 0.12**

Niebezpieczny protokół

Serwer obsługuje wyłącznie SMBv1. Jest to stara wersja protokołu SMB, która ma znane problemy bezpieczeństwa. W nowoczesnym środowisku powinna być wyłączona.

**Samba 3.0.20-Debian**

Zidentyfikowana wersja serwera Samba. Jest bardzo stara i warto sprawdzić ją pod kątem znanych podatności.

**Nazwa komputera**

`metasploitable`

**Domena**

`localdomain`

**FQDN**

`metasploitable.localdomain`

Ważne: `smb-os-discovery` rozpoznał system jako Unix, a nie Windows. Samba umożliwia systemom Linux udostępnianie zasobów w sieci SMB.

## **2. Następny krok – sprawdzamy udziały SMB**

Teraz chcemy ustalić, jakie katalogi serwer udostępnia i czy można je przeglądać bez podawania hasła.

Wykonaj w Kali:

```
smbclient -L //192.168.56.104 -N
```

Znaczenie parametrów:

- `smbclient` – klient protokołu SMB.
    
- `-L` – wyświetlenie listy dostępnych udziałów.
    
- `//192.168.56.104` – nasz serwer.
    
- `-N` – próba połączenia bez podawania hasła.
    

## **3. Na co zwrócimy uwagę?**

W wyniku interesują nas przede wszystkim:

- `Sharename` – nazwa udostępnionego zasobu.
    
- `Type` – rodzaj zasobu, np. Disk lub IPC.
    
- `Comment` – opis udziału.
    
- `Anonymous login successful` – informacja o powodzeniu anonimowego logowania.


Zwróć uwagę na komunikat:

`Anonymous login successful`

Oznacza to, że anonimowa sesja SMB została zaakceptowana. Nie oznacza to jednak automatycznie, że mamy prawo czytać i zapisywać pliki we wszystkich udziałach.

## **1. Co znaleźliśmy?**

|Udział|Typ|Wstępna interpretacja|
|---|---|---|
|`print$`|Disk|Zasób związany ze sterownikami drukarek|
|`tmp`|Disk|Katalog tymczasowy – szczególnie interesujący|
|`opt`|Disk|Dodatkowy katalog systemowy|
|`IPC$`|IPC|Komunikacja międzyprocesowa SMB|
|`ADMIN$`|IPC|Udział administracyjny|

Najbardziej interesuje nas teraz `tmp`, ponieważ jego opis `oh noes!` sugeruje, że warto sprawdzić jego konfigurację.

## **2. Następny krok – sprawdzamy dostęp do tmp**

Wykonaj jedno polecenie:

```
smbclient //192.168.56.104/tmp -N
```

Jeśli połączenie się powiedzie, zobaczysz znak zachęty:

```
smb: \>
```

Na tym etapie niczego nie zmieniaj i nie usuwaj.

Wpisz tylko:

```
ls
```

To wyświetli zawartość udziału.

Aby wyjść z klienta SMB, wpisz:

```
exit
```

## **3. Czego się uczymy?**

Rozróżniamy trzy poziomy dostępu:

1. **Enumeracja** – możemy zobaczyć nazwy udziałów.
    
2. **Odczyt** – możemy przeglądać i pobierać pliki.
    
3. **Zapis** – możemy tworzyć lub modyfikować pliki.
    

To ważne rozróżnienie w pracy pentestera. Samo anonimowe wyświetlenie udziałów nie oznacza jeszcze pełnego dostępu do danych.


To już nie jest tylko enumeracja nazw udziałów — potwierdziliśmy **anonimowy dostęp do zawartości katalogu**.

## **1. Analiza zawartości** `tmp`

|Element|Typ / atrybut|Interpretacja|
|---|---|---|
|`.`|D|Bieżący katalog|
|`..`|DR|Katalog nadrzędny|
|`4560.jsvc_up`|R|Plik, 0 bajtów|
|`.ICE-unix`|DH|Ukryty katalog|
|`.X11-unix`|DH|Ukryty katalog|
|`.X0-lock`|HR|Ukryty plik, 11 bajtów|

Kilka wyjaśnień:

- `.ICE-unix` – katalog związany z mechanizmami środowiska graficznego X11.
    
- `.X11-unix` – katalog związany z komunikacją serwera X11.
    
- `.X0-lock` – plik blokady sesji X11.
    
- `4560.jsvc_up` – plik, którego nazwa może być związana z procesem Java Service Wrapper; na razie nie wyciągamy wniosków bez dalszej weryfikacji.
    

## **2. Co już potwierdziliśmy?**

**Anonimowe połączenie SMB**

**Wyświetlenie listy udziałów**

**Wejście do udziału** `tmp`

**Odczyt listy plików i katalogów**

**Możliwość pobierania i zapisywania plików – jeszcze niezweryfikowana**

## **3. Następny krok – sprawdzamy uprawnienia do zapisu**

Zanim cokolwiek utworzymy, sprawdźmy, czy serwer deklaruje możliwość zapisu do udziału.

Wyjdź z klienta SMB:

```
exit
```

Następnie w Kali wykonaj:

```
smbmap -H 192.168.56.104 -u '' -p ''
```


To narzędzie sprawdzi dostęp anonimowy do udziałów i przedstawi wykryte uprawnienia, np.:

- `READ ONLY` – tylko odczyt,
    
- `READ, WRITE` – odczyt i zapis,
    
- `NO ACCESS` – brak dostępu.
    

Wklej cały wynik.

**Dlaczego tak postępujemy?** W prawdziwym audycie nie wystarczy znaleźć otwarty udział. Musimy określić, jakie operacje może wykonać niezalogowany użytkownik. To właśnie różnica między samym wykryciem usługi a oceną jej rzeczywistego ryzyka.

Dobrze, przerwanie było właściwą decyzją. Nie uzyskaliśmy jeszcze wyniku `smbmap`, ale mamy już potwierdzone wcześniejszym testem, że anonimowe logowanie i przeglądanie udziału `tmp` działają.

Możliwe, że `smbmap` ma problem z negocjacją starego protokołu SMBv1 na tej konfiguracji.

## **Następny krok – sprawdzimy uprawnienia inną metodą**

Wróćmy do narzędzia, które już zadziałało, czyli `smbclient`.

W Kali wykonaj:

```
smbclient //192.168.56.104/tmp -N
```

Po pojawieniu się `smb: \>` wpisz:

```
put /etc/hostname test_lab.txt
```

To spróbuje przesłać do udziału niewielki plik tekstowy z nazwą hosta Kali.

**Uwaga:** to kontrolowany test zapisu w naszym własnym laboratorium. Jeśli operacja się powiedzie, usuniemy wyłącznie utworzony przez nas plik `test_lab.txt`.

Mamy to! Operacja zakończyła się powodzeniem.

```
putting file /etc/hostname as \test_lab.txt
```

To oznacza, że anonimowy użytkownik może nie tylko przeglądać udział `tmp`, ale również **zapisywać w nim pliki bez uwierzytelnienia**.

To istotne ustalenie z punktu widzenia bezpieczeństwa.

## **1. Co właśnie udowodniliśmy?**

|Test|Wynik|
|---|---|
|Anonimowe logowanie SMB|Sukces|
|Wyświetlenie zawartości `tmp`|Sukces|
|Zapis pliku bez hasła|Sukces|

Potwierdziliśmy anonimowy dostęp do odczytu i zapisu w udziale `tmp`.

## **2. Teraz sprzątamy po teście**

Będąc nadal w konsoli `smb: \>`, wykonaj:

```
del test_lab.txt
```

Następnie:

```
ls
```

Chcemy potwierdzić, że nasz plik został usunięty.

**Nie usuwaj żadnych innych plików.**

## **3. Wstępny wniosek do dokumentacji**

Możesz już zapisać następujące ustalenie:

> Serwer Samba 3.0.20 udostępnia zasób `tmp`, do którego możliwe jest anonimowe logowanie. Użytkownik niezalogowany może odczytywać zawartość katalogu oraz przesyłać do niego pliki. Potwierdzono możliwość zapisu poprzez testowy plik `test_lab.txt`.

Po potwierdzeniu usunięcia pliku przejdziemy do oceny, jakie konsekwencje bezpieczeństwa może mieć taka konfiguracja.

Świetnie. Sprzątanie zakończone — nasz testowy plik został usunięty. Udział `tmp` pozostawiliśmy bez zmian.

## **1. Podsumowanie ćwiczenia – Samba Enumeration**

Ćwiczenie zakończone

Zebraliśmy następujące dowody:

|Etap|Wynik|
|---|---|
|Identyfikacja Samby|Samba 3.0.20-Debian|
|Wykrycie protokołu|SMBv1|
|Enumeracja udziałów|5 udziałów|
|Anonimowe logowanie|Potwierdzone|
|Odczyt `tmp`|Potwierdzony|
|Zapis do `tmp`|Potwierdzony|
|Usunięcie pliku testowego|Potwierdzone|

## **2. Ocena bezpieczeństwa**

Najważniejsze ustalenie:

**Anonimowy użytkownik może zapisywać pliki w udziale sieciowym** `tmp`**.**

W rzeczywistym środowisku może to prowadzić między innymi do:

- przechowywania nieautoryzowanych plików,
    
- wykorzystania udziału jako miejsca wymiany danych,
    
- nadużyć wynikających z błędnych uprawnień,
    
- dalszych zagrożeń, jeśli inne usługi korzystają z tych plików.
    

Nie oznacza to automatycznie możliwości wykonania przesłanego pliku na serwerze.

Etap zakończony

17 listopada 2026

## **1. SMB – Samba**

Wykryta usługa:

- Porty: `139/tcp`, `445/tcp`  
    
- Samba: `3.0.20-Debian`  
    
- Protokół: SMBv1 (`NT LM 0.12`)  
    

Przeprowadzone testy:

|Test|Wynik|
|---|---|
|Anonimowe logowanie|Potwierdzone|
|Lista udziałów|Dostępna|
|Dostęp do `tmp`|Potwierdzony|
|Odczyt zawartości `tmp`|Potwierdzony|
|Zapis anonimowy|Potwierdzony|
|Usunięcie pliku testowego|Potwierdzone|

Najważniejsze ustalenie: udział `tmp` umożliwia anonimowy odczyt i zapis.