

# **Plan na dzisiaj – ProFTPD 1.3.1**

Laboratorium

Tryb egzaminacyjny

Port 2121

**Cel:** sprawdzić, czy ProFTPD 1.3.1 udostępnia anonimowy dostęp, jakie ma możliwości i czy konfiguracja lub wersja stwarzają zagrożenie.

## **Plan ćwiczenia**

|Etap|Zadanie|
|---|---|
|1|Rozpoznanie i fingerprinting|
|2|Enumeracja FTP i funkcji serwera|
|3|Test anonimowego logowania|
|4|Analiza uprawnień i dostępnych zasobów|
|5|Identyfikacja potencjalnych podatności|
|6|Kontrolowana walidacja w laboratorium|
|7|Finding, Impact, Evidence, Remediation|

Dodatkowo będziemy ćwiczyć:

- samodzielne formułowanie hipotez;
    
- dobieranie odpowiednich narzędzi;
    
- interpretację odpowiedzi serwera;
    
- odróżnianie podatności potencjalnej od potwierdzonej.
    

To ważne: nie będę od razu podawał rozwiązania. Najpierw dostaniesz zadanie, spróbujesz sam, a potem wspólnie przeanalizujemy wynik.

## **Zaczynamy – etap 1**

Nasz cel:

`192.168.56.104:2121`

W Kali wykonaj:

```
nmap -sV -sC -p 2121 192.168.56.104
```

To połączy identyfikację wersji z podstawowymi skryptami rozpoznawczymi Nmap.

**Twoje zadanie:** wklej wynik i spróbuj samodzielnie wskazać trzy najważniejsze informacje, które z niego wynikają.

Jedna zasada na najbliższe tygodnie: będziemy pracować według cyklu:

**Target → Recon → Enumeration → Validation → Exploitation → Evidence → Reporting.**

Chcę, żebyś przed egzaminem potrafił nie tylko rozwiązać CTF, ale też wyjaśnić, dlaczego wybrałeś konkretną metodę i jakie dowody potwierdzają Twoje ustalenia.


Zgadza się. Mamy dwa podstawowe ustalenia:

- `2121/tcp` – port otwarty.
    
- `ProFTPD 1.3.1` – zidentyfikowana wersja serwera FTP.
    

Teraz przechodzimy od fingerprintingu do enumeracji.

### **Etap 2 – sprawdzamy obsługiwane funkcje FTP**

Wykonaj:

```
ftp 192.168.56.104 2121
```

Po połączeniu zobaczysz banner serwera i pytanie o login.

Na razie **nie loguj się**. Wklej banner, który otrzymasz.

Chcę, żebyśmy najpierw ustalili, z jakim dokładnie serwerem rozmawiamy. Potem sprawdzimy anonimowy dostęp.

Tryb egzaminacyjny: Ty wykonujesz i interpretujesz, ja weryfikuję. 💪

Dobrze. I to już jest pierwsza różnica w stosunku do usługi na porcie 21.

### **Analiza ProFTPD – port 2121**

Otrzymaliśmy:

```
220 ProFTPD 1.3.1 Server (Debian)
331 Password required for anonymous
530 Login incorrect.
```

Interpretacja:

|Odpowiedź|Znaczenie|
|---|---|
|`220`|Serwer przyjął połączenie|
|`331`|Serwer oczekuje hasła dla użytkownika anonymous|
|`530`|Logowanie nie powiodło się|

**Wniosek:** anonimowe logowanie nie zostało zaakceptowane. Nie oznacza to jeszcze, że anonimowy dostęp jest całkowicie wyłączony — możemy sprawdzić, czy serwer dopuszcza inne mechanizmy dostępu, ale nie będziemy zgadywać haseł.

### **Małe zadanie egzaminacyjne**

Zanim przejdziemy dalej, zapamiętaj różnicę:

- vsftpd na 21: anonimowe logowanie zakończyło się kodem `230`.
    
- ProFTPD na 2121: anonimowe logowanie zakończyło się kodem `530`.
    

To dwa różne wyniki, mimo że obie usługi udostępniają FTP.

### **Następny krok – sprawdzamy funkcje serwera**

Jesteś nadal w kliencie FTP (`ftp>`). Wykonaj:

```
quote FEAT
```

Wklej odpowiedź serwera.

Chcę sprawdzić, jakie rozszerzenia obsługuje ProFTPD, zanim zdecydujemy o kolejnych testach.


Dobrze. ProFTPD odpowiedział na `FEAT`. Widzimy trzy obsługiwane rozszerzenia.

### **Analiza**

```
211-Features:
 MDTM
 REST STREAM
 SIZE
211 End
```

|Funkcja|Znaczenie|
|---|---|
|`MDTM`|Odczyt czasu modyfikacji pliku|
|`REST STREAM`|Wznawianie transferu od wskazanego miejsca|
|`SIZE`|Odczyt rozmiaru pliku|

W porównaniu z vsftpd na porcie 21 ProFTPD reklamuje mniej rozszerzeń.

### **Dotychczasowe ustalenia**

- Port `2121/tcp` otwarty.
    
- ProFTPD `1.3.1`, Debian.
    
- Anonimowe logowanie odrzucone (`530`).
    
- Rozszerzenia FTP: MDTM, REST STREAM, SIZE.
    

### **Następny krok – identyfikacja systemu**

Wpisz:

```
quote SYST
```

**Twoje zadanie:** ustal, czy wynik potwierdza wcześniejszą identyfikację systemu jako Debian/Unix, czy dostarcza nowych informacji.

Świetnie. Tym razem mamy prawidłową odpowiedź.

```
215 UNIX Type: L8
```

### **Analiza**

- `215` – pozytywna odpowiedź serwera na polecenie `SYST`.
    
- `UNIX` – serwer deklaruje system typu UNIX.
    
- `L8` – format danych oparty na 8-bitowych bajtach.
    

Nie jest to dokładna identyfikacja dystrybucji ani wersji systemu.

### **Aktualna dokumentacja – ProFTPD**

|Parametr|Wynik|
|---|---|
|Port|2121/tcp|
|Usługa|ProFTPD 1.3.1|
|System deklarowany|Debian / UNIX|
|Anonymous login|Odrzucony (`530`)|
|FEAT|MDTM, REST STREAM, SIZE|
|SYST|UNIX Type: L8|
|Timeout|300 sekund|

### **Teraz zadanie trochę bardziej egzaminacyjne**

Chcę sprawdzić, czy serwer pozwala na wykonywanie poleceń FTP przed uwierzytelnieniem.

Wykonaj:

```
quote PWD
```

To polecenie zapyta serwer o bieżący katalog roboczy.

Wklej odpowiedź. Interesuje nas, czy dostaniemy informację o katalogu, czy odmowę dostępu.

Bardzo dobrze. To jest konkretny wynik enumeracji.

```
530 Please login with USER and PASS
```

### **Analiza**

Serwer odrzucił polecenie `PWD`, ponieważ nie jesteśmy uwierzytelnieni.

Co możemy wywnioskować?

- Serwer pozwala nawiązać połączenie bez logowania.
    
- Udostępnia banner i odpowiada na `FEAT` oraz `SYST`.
    
- Nie pozwala na odczyt bieżącego katalogu przed uwierzytelnieniem.
    
- Anonimowe logowanie zostało wcześniej odrzucone.
    

To wskazuje na ograniczenie dostępu przed uwierzytelnieniem.

### **Porównanie obu serwerów FTP**

|Funkcja|vsftpd :21|ProFTPD :2121|
|---|---|---|
|Połączenie|Tak|Tak|
|Anonymous login|Sukces|Odrzucony|
|FEAT bez logowania|Tak|Tak|
|SYST bez logowania|Tak|Tak|
|PWD bez logowania|Nie sprawdzaliśmy|Odrzucony|

### **Następny krok – sprawdzamy mechanizm uwierzytelniania**

W tej samej sesji FTP wykonaj:

```
quote HELP
```

Zobaczymy, jakie polecenia serwer udostępnia i czy zdradza dodatkowe informacje o swojej konfiguracji.

Nie próbujemy zgadywać haseł ani obchodzić uwierzytelniania. Na tym etapie zbieramy dowody.

Bardzo dobry wynik! To już jest bardziej szczegółowa enumeracja niż samo sprawdzenie wersji.

Serwer zwrócił listę obsługiwanych poleceń FTP.

### **1. Co odkryliśmy?**

W odpowiedzi szczególnie zwracają uwagę:

|Polecenie|Znaczenie|
|---|---|
|`USER`, `PASS`|Uwierzytelnianie|
|`CWD`, `PWD`|Poruszanie się po katalogach|
|`LIST`, `NLST`|Listowanie plików|
|`RETR`|Pobieranie plików|
|`STOR`|Wysyłanie plików|
|`DELE`|Usuwanie plików|
|`MKD`, `RMD`|Tworzenie i usuwanie katalogów|
|`SITE`|Dodatkowe polecenia administracyjne|
|`AUTH`|Negocjowanie zabezpieczeń, np. TLS|
|`FEAT`|Lista rozszerzeń|

Gwiazdka `*` oznacza polecenie niezaimplementowane.

### **2. Ważna obserwacja**

Serwer reklamuje polecenia `STOR`, `RETR`, `DELE`, `MKD` i `RMD`.

Ale pamiętaj: **obsługa polecenia nie oznacza uprawnienia do jego wykonania**.

Nie wiemy jeszcze, jakie operacje będą dostępne po uwierzytelnieniu.

Dodatkowo:

```
214 Direct comments to root@metasploitable.localdomain
```

To ujawnia nazwę hosta i domenę lokalną, które wcześniej widzieliśmy również w enumeracji SMB.

### **3. Zadanie egzaminacyjne – sprawdzamy TLS**

Zauważ, że ProFTPD reklamuje polecenie `AUTH`, którego nie widzieliśmy w wynikach `FEAT`.

Wykonaj:

```
quote AUTH TLS
```

Wklej odpowiedź.

Chcemy ustalić, czy ten serwer oferuje szyfrowanie połączenia FTP. Nie będziemy jeszcze przesyłać żadnych danych.

**Dobra robota:** zaczynasz już rozróżniać trzy rzeczy, które na egzaminie są bardzo ważne: co serwer obsługuje, na co pozwala niezalogowanemu użytkownikowi i co faktycznie udało się potwierdzić.

To wynik jednoznaczny dla tej próby:

```
500 AUTH not understood
```

**ProFTPD 1.3.1 nie rozpoznaje komendy** `AUTH` **w tej konfiguracji.** Nie udało nam się więc potwierdzić obsługi jawnego FTPS (TLS).

Ważne rozróżnienie: nie oznacza to automatycznie, że każda możliwa forma szyfrowania jest wykluczona. Zapisujemy jednak, że próba negocjacji TLS przez `AUTH TLS` zakończyła się niepowodzeniem.

### **Wnioski z enumeracji portu 2121**

|Obszar|Ustalenie|
|---|---|
|Usługa|ProFTPD 1.3.1|
|System|UNIX Type: L8|
|Anonymous|Logowanie odrzucone (`530`)|
|FEAT|MDTM, REST STREAM, SIZE|
|PWD bez logowania|Wymaga uwierzytelnienia|
|AUTH TLS|Nierozpoznana komenda (`500`)|
|Dostęp do plików|Niezweryfikowany|

Nie testowaliśmy zgadywania haseł ani operacji zapisu i usuwania plików.

### **Następny krok – sprawdźmy odpowiedź serwera na STAT**

W tej samej sesji FTP wykonaj tylko:

```
quote STAT
```

To pozwoli sprawdzić, czy serwer udostępnia dodatkowe informacje o swoim stanie bez logowania. Wklej wynik, a przeanalizujemy go przed kolejnym krokiem.

Dobrze. To kolejny istotny wynik:

```
530 Please login with USER and PASS
```

**Wniosek:** ProFTPD nie udostępnia nam informacji `STAT` przed uwierzytelnieniem. Wymaga zalogowania użytkownika.

To potwierdza, że:

- `PWD` bez logowania – zablokowane;
    
- `STAT` bez logowania – zablokowane;
    
- próba logowania `anonymous` – odrzucona (`530`);
    
- `HELP`, `FEAT` i `SYST` – dostępne bez logowania.
    

Nie jest to jeszcze dowód, że po zalogowaniu `STAT` nie zadziała. Serwer po prostu wymaga uwierzytelnienia.

### **Następny krok – sprawdźmy** `SITE`

Wpisz:

```
quote SITE HELP
```

Chcemy ustalić, czy serwer udostępnia dodatkowe polecenia administracyjne. Sama obecność takich poleceń nie oznacza jeszcze, że można je wykonać bez uprawnień. Czekam na wynik.

Świetnie! Tym razem mamy odpowiedź serwera. I to jest ciekawy wynik z punktu widzenia enumeracji.

```
214-The following SITE commands are recognized (* =>'s unimplemented)
214-QUOTA
214-HELP
214-CHGRP
214-CHMOD
```

### **1. Co odkryliśmy?**

ProFTPD 1.3.1 udostępnia następujące komendy `SITE`:

|Komenda|Znaczenie|
|---|---|
|`QUOTA`|Informacje o limitach przestrzeni dyskowej|
|`HELP`|Pomoc dotycząca komend SITE|
|`CHGRP`|Zmiana grupy pliku|
|`CHMOD`|Zmiana uprawnień pliku|

**Najciekawsza jest** `CHMOD`**.** To komenda pozwalająca zmieniać uprawnienia plików na serwerze FTP, ale jej obecność na liście nie oznacza, że anonimowy lub nieuwierzytelniony użytkownik może jej użyć.

Nie wiemy jeszcze, czy serwer wymaga autoryzacji, ani jakie uprawnienia są potrzebne.

### **2. Wniosek egzaminacyjny**

Rozróżniaj trzy rzeczy:

- **Command advertised** – serwer deklaruje obsługę komendy.
    
- **Command accessible** – możemy ją wywołać.
    
- **Command authorized** – serwer pozwala wykonać operację na zasobie.
    

Na razie potwierdziliśmy pierwsze dwie rzeczy dla `SITE HELP`, ale nie trzecią dla `CHMOD`.

### **3. Następny krok – bezpieczna walidacja**

Wpisz:

```
quote SITE CHMOD
```

Nie podajemy żadnego pliku ani trybu uprawnień. Chcemy tylko zobaczyć, jak serwer reaguje na niekompletną komendę.

Wklej wynik. Na jego podstawie ustalimy, czy możemy przejść do dalszej walidacji.

Dokładnie. I to jest ważna obserwacja — serwer pozwala nam wyświetlić listę komend `SITE`, ale nie pozwala przejść do ich wykonania bez uwierzytelnienia.

Otrzymujemy:

```
530 Please login with USER and PASS
```

### **Aktualny wniosek**

|Funkcja|Bez logowania|
|---|---|
|`SITE HELP`|Dostępna|
|`SITE CHMOD`|Wymaga logowania|
|`SITE CHGRP`|Niezweryfikowana|
|`SITE QUOTA`|Niezweryfikowana|

Nie zakładamy, że `CHMOD` jest podatny tylko dlatego, że widnieje na liście.

### **Co dalej?**

Mamy już wystarczająco dużo danych o zachowaniu ProFTPD przed uwierzytelnieniem. Nie będziemy zgadywać haseł.

Proponuję teraz sprawdzić **podatności przypisane do wersji ProFTPD 1.3.1**, ale najpierw zweryfikujemy dokładną wersję i dostępne informacje o usłudze.

W Kali wykonaj:

```
searchsploit ProFTPD 1.3.1
```

Wklej wynik. Przeanalizujemy, które pozycje są rzeczywiście związane z naszą wersją i konfiguracją, a które są tylko potencjalnymi tropami.


To wcale nie jest dziwne — `searchsploit` przeszukuje lokalną kopię bazy Exploit-DB, a nie cały internet. Brak wyników oznacza tylko, że **w Twojej lokalnej bazie nie znaleziono wpisu pasującego do frazy** `ProFTPD 1.3.1`. Nie oznacza, że usługa jest wolna od podatności.

Warto też pamiętać, że wersja `1.3.1` jest dość ogólna. Niektóre wpisy dotyczą konkretnych wydań, np. `1.3.1rc` albo `1.3.1a`, i nie muszą pasować do naszej instalacji.

Sprawdziłem również publiczne informacje o podatnościach. Są co najmniej dwa interesujące tropy:

1. **CVE-2009-0542** – SQL Injection w ProFTPD 1.3.1–1.3.2rc2. Dotyczy konfiguracji korzystającej z modułu `mod_sql`.
    
2. **CVE-2009-0543** – problem związany z obsługą znaków wielobajtowych, wymagający m.in. włączonego NLS oraz odpowiednich modułów SQL.
    
    security-tracker.debian.org+1
    

To ważne: **sama wersja 1.3.1 nie potwierdza podatności**. Nie wiemy, czy nasz serwer ma `mod_sql`, `mod_sql_mysql` lub `mod_sql_postgres`.

### **Zróbmy teraz mały krok**

W Kali wykonaj:

```
searchsploit ProFTPD
```

Tym razem bez ograniczania wersji.

Chcę zobaczyć, co znajduje Twoja lokalna baza dla całego projektu. Potem porównamy wyniki z wersją i konfiguracją Metasploitable 2.

Nie uruchamiamy jeszcze żadnego exploita. Najpierw ustalamy, czy mamy rzeczywistą ścieżkę ataku, czy tylko historyczny wpis w bazie.

Teraz mamy znacznie ciekawszy materiał. W wynikach są pozycje, które warto przeanalizować, ale nie wszystkie dotyczą naszej wersji.

### **1. Selekcja wyników**

|Wpis|Ocena dla naszego celu|
|---|---|
|ProFTPd `mod_mysql` Authentication Bypass|Warto sprawdzić, czy moduł jest używany|
|ProFTPd 1.3 `mod_sql` Username SQL Injection|Potencjalnie interesujący, wymaga weryfikacji modułu i warunków|
|ProFTPd 1.3.5 `mod_copy`|Nie pasuje do wersji 1.3.1|
|ProFTPd 1.3.3c Backdoor|Nie pasuje do wersji 1.3.1|
|ProFTPd 1.3.7a DoS|Nie pasuje do wersji 1.3.1|
|ProFTPd 1.x `mod_tls`|Wymaga sprawdzenia szczegółów; nie potwierdziliśmy obsługi TLS|

Najbardziej interesują nas na razie wpisy związane z `mod_sql` i `mod_mysql`.

### **2. Najpierw poznajmy szczegóły exploita**

Nie uruchamiamy go. Otwórz opis wpisu dotyczącego `mod_mysql`:

```
searchsploit -x 8037
```

To wyświetli lokalny opis PoC.

**Zadanie egzaminacyjne:** spróbuj ustalić z opisu:

- jakiego modułu wymaga podatność;
    
- jakie warunki musi spełniać konfiguracja;
    
- czy jest to rzeczywiście RCE, czy tylko obejście uwierzytelnienia.
    

Świetnie — to jest właściwa treść historycznego PoC dla wpisu Exploit-DB 8037. Teraz możemy przeanalizować go jak na egzaminie PT1a.

## **1. Co robi ten exploit?**

Autor opisuje SQL Injection w mechanizmie uwierzytelniania ProFTPD korzystającym z MySQL.

Podany login:

```
%') and 1=2 union select 1,1,uid,gid,homedir,shell from users; --
```

Hasło:

```
1
```

Celem jest zmiana zapytania SQL wykonywanego przez serwer podczas logowania.

Mechanizm ataku:

1. Znak `%` wpływa na sposób przetwarzania danych wejściowych.
    
2. Apostrof pozwala wyjść z kontekstu tekstowego w zapytaniu SQL.
    
3. `UNION SELECT` próbuje dołączyć wyniki z tabeli `users`.
    
4. `--` komentuje dalszą część zapytania.
    
5. W rezultacie mechanizm uwierzytelniania może zaakceptować logowanie bez znajomości prawidłowego hasła.
    

To podatność w konkretnym mechanizmie uwierzytelniania SQL, a nie uniwersalna podatność każdego serwera ProFTPD 1.3.1.

## **2. Najważniejsze wymagania**

Żeby ta ścieżka miała zastosowanie, muszą być spełnione istotne warunki:

- ProFTPD korzysta z `mod_sql`.
    
- Uwierzytelnianie wykorzystuje MySQL (`mod_sql_mysql`).
    
- Konfiguracja i sposób budowania zapytania odpowiadają podatnej implementacji.
    
- Usługa jest dostępna z naszej maszyny Kali.
    

**Na razie nie potwierdziliśmy żadnego z dwóch pierwszych warunków.**

## **3. Zadanie egzaminacyjne – oceń hipotezę**

Mamy:

- ProFTPD 1.3.1 na porcie 2121.
    
- Odrzucone logowanie anonimowe.
    
- Brak uwierzytelnienia zwykłym użytkownikiem.
    
- Wpis Exploit-DB dotyczący SQL Injection.
    

Czy na podstawie tych informacji możemy już stwierdzić, że serwer jest podatny?

**Nie.** Mamy hipotezę, ale brakuje potwierdzenia konfiguracji.

## **4. Następny krok – enumeracja konfiguracji zdalnej**

Wróćmy do Kali i sprawdźmy, czy Nmap ma skrypt FTP, który może dostarczyć dodatkowych informacji o usłudze.

Wykonaj:

```
nmap --script "ftp-* " -p 2121 192.168.56.104
```

Uwaga: między `ftp-*` a cudzysłowem nie powinno być spacji. Poprawna komenda:

```
nmap --script "ftp-*" -p 2121 192.168.56.104
```

Wklej wynik.

Nie próbujemy jeszcze payloadu SQL Injection. Najpierw ustalimy, co można dowiedzieć się bez uwierzytelnienia i bez ingerowania w konfigurację serwera.

### **3. Następny krok – sprawdźmy dokładnie dostępne skrypty**

Wykonaj:

```
ls /usr/share/nmap/scripts/ftp-*
```

Chcę zobaczyć, jakie skrypty FTP masz w swojej instalacji Nmap. Wybierzemy z nich odpowiedni do dalszej enumeracji.

Na razie nadal nie wykonujemy SQL Injection. Najpierw musimy znaleźć dowód, że ProFTPD korzysta z podatnego mechanizmu `mod_sql`/MySQL.

┌──(kali㉿Kali)-[~]  
└─$ ls /usr/share/nmap/scripts/ftp-*  
/usr/share/nmap/scripts/ftp-anon.nse /usr/share/nmap/scripts/ftp-proftpd-backdoor.nse  
/usr/share/nmap/scripts/ftp-bounce.nse /usr/share/nmap/scripts/ftp-syst.nse  
/usr/share/nmap/scripts/ftp-brute.nse /usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse  
/usr/share/nmap/scripts/ftp-libopie.nse /usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse

Dobrze. Mamy 8 skryptów FTP w Twojej instalacji Nmap. Teraz możemy wybrać te, które mają sens dla naszego celu.

### **1. Ocena dostępnych skryptów**

|Skrypt|Zastosowanie|Czy pasuje?|
|---|---|---|
|`ftp-anon`|Test dostępu anonimowego|Tak, już częściowo sprawdziliśmy|
|`ftp-syst`|Pobiera informacje systemowe|Tak|
|`ftp-bounce`|Test FTP bounce|Na później|
|`ftp-brute`|Próby haseł|Pomijamy|
|`ftp-proftpd-backdoor`|Test znanego backdoora|Nie pasuje do znanej wersji|
|`ftp-vsftpd-backdoor`|Backdoor vsftpd|Nie dotyczy ProFTPD|
|`ftp-libopie`|Test problemu z biblioteką OPIE|Nie mamy przesłanek|
|`ftp-vuln-cve2010-4221`|Test konkretnej podatności|Nie mamy przesłanek, że dotyczy tej wersji|

### **2. Wykonajmy bezpieczny test informacyjny**

Uruchom tylko:

```
nmap -p 2121 --script ftp-syst 192.168.56.104
```

To powinno ponownie sprawdzić informacje systemowe serwera FTP.

### **3. Ważna lekcja**

Zwróć uwagę na różnicę między enumeracją a skanowaniem podatności:

- enumeracja mówi nam, co serwer ujawnia;
    
- skan podatności sprawdza określone znane problemy;
    
- brak wyników skanera nie oznacza braku podatności.
    

Po tym teście zdecydujemy, czy zamykamy enumerację portu 2121, czy mamy jeszcze uzasadniony trop do sprawdzenia.

W porządku. `ftp-syst` nie zwrócił dodatkowych informacji. To nie jest błąd skryptu ani dowód na brak funkcji FTP.

Mamy już całkiem dobry obraz portu 2121.

### **Podsumowanie enumeracji ProFTPD – port 2121**

|Test|Wynik|
|---|---|
|Banner|ProFTPD 1.3.1|
|Anonymous login|Odrzucony|
|`FEAT`|MDTM, REST STREAM, SIZE|
|`SYST`|UNIX Type: L8|
|`PWD` bez logowania|530|
|`STAT` bez logowania|530|
|`AUTH TLS`|500 – nierozpoznana komenda|
|`SITE HELP`|QUOTA, HELP, CHGRP, CHMOD|
|`SITE CHMOD`|Wymaga uwierzytelnienia|
|`ftp-syst`|Bez dodatkowych informacji|
|SQL Injection|Hipoteza, niepotwierdzona|

### **Teraz ważna decyzja analityczna**

Mamy historyczny PoC SQL Injection, ale nie mamy dowodu na obecność `mod_sql` ani `mod_sql_mysql`.

Nie chcę, żebyśmy popełnili częsty błąd początkujących: zobaczyli wersję w Exploit-DB i od razu uznali cel za podatny.

Proponuję zakończyć na chwilę enumerację zdalną i sprawdzić lokalnie dokumentację oraz konfigurację Metasploitable 2. To może dać nam odpowiedź, czy ProFTPD korzysta z MySQL.

**Jedno pytanie:** czy masz możliwość zalogowania się do konsoli Metasploitable 2 jako użytkownik systemowy? Nie musimy niczego zmieniać — wystarczy odczyt konfiguracji.

## **Zamykamy port 2121 – ProFTPD 1.3.1**

Najważniejsze ustalenia:

- ProFTPD 1.3.1 – potwierdzony banner.
    
- Anonymous login – odrzucony.
    
- Moduły `mod_sql` i `mod_sql_mysql` – wskazane w `modules.conf` jako ładowane.
    
- Konfiguracja SQL w `sql.conf` – zakomentowana.
    
- Aktywne uwierzytelnianie SQL – niepotwierdzone.
    
- SQL Injection – niepotwierdzona.
    

Nie mamy podstaw, żeby uznać tę usługę za podatną na opisany PoC.

## **Następna usługa: SMTP – port 25**

Następny etap enumeracji

Przechodzimy do Postfix SMTP.

W Kali wykonaj:

```
nmap -sV -sC -p 25 192.168.56.104
```

Wklej wynik. Zaczniemy od bannera, możliwości serwera SMTP i metod enumeracji użytkowników.

Pracujemy dalej według schematu: