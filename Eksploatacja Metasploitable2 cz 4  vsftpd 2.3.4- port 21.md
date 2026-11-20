
Nie będziemy powtarzać dzisiejszych czynności. Przejdziemy do kolejnych usług z wykrytej listy:

1. FTP – porty 21 i 2121.
2. Telnet – port 23.
3. SSH – port 22.
4. SMTP – port 25.

Zaczniemy od FTP i będziemy postępować tak samo jak dzisiaj: jedno polecenie, analiza wyniku, wnioski i dokumentacja.

# **Dzisiejszy etap: FTP Enumeration**

**Cel:** Metasploitable 2 — `192.168.56.104`

W poprzednim skanowaniu wykryliśmy dwa porty FTP:

|Port|Wykryta usługa|
|---|---|
|`21/tcp`|vsftpd 2.3.4|
|`2121/tcp`|ProFTPD 1.3.1|

Zaczniemy od portu 21.

### **Krok 1 – potwierdzenie usługi**

W Kali wykonaj:

```
nmap -sV -p 21 192.168.56.104
```

To pozwoli nam ponownie potwierdzić wersję usługi i zobaczyć, czy wynik jest zgodny z wcześniejszym skanowaniem.

Dobrze. Wynik potwierdza wcześniejsze ustalenia. Port 21 jest otwarty, a usługą FTP jest **vsftpd 2.3.4**.

### **Analiza wyniku**

|Element|Wynik|Znaczenie|
|---|---|---|
|Port|`21/tcp`|Standardowy port FTP|
|State|`open`|Usługa odpowiada na połączenia|
|Service|`ftp`|Protokół FTP|
|Version|`vsftpd 2.3.4`|Zidentyfikowana wersja serwera|
|OS|Unix|System docelowy sklasyfikowany jako Unix|

**Co warto wiedzieć?**

FTP to protokół przesyłania plików. W klasycznej postaci nie szyfruje danych logowania ani przesyłanych plików. To istotna cecha bezpieczeństwa, którą uwzględnimy w ocenie usługi.

Sama wersja `2.3.4` jest warta uwagi, ale nie będziemy jeszcze testować exploitów.

### **Krok 2 – sprawdzamy dostęp anonimowy**

Teraz sprawdzimy, czy serwer pozwala zalogować się bez indywidualnego konta.

Wykonaj jedno polecenie:

```
ftp 192.168.56.104
```

Gdy pojawi się pytanie `Name`, wpisz:

```
anonymous
```

Jeżeli pojawi się pytanie o hasło, wpisz:

```
anonymous
```

Wklej wynik sesji. Na razie niczego nie pobieramy, nie wysyłamy ani nie modyfikujemy.


Świetnie! Tym razem logowanie zakończyło się sukcesem.

Anonimowy dostęp potwierdzony

### **Analiza wyniku**

Najważniejsza linia:

```
230 Login successful.
```

Oznacza, że serwer zaakceptował logowanie użytkownika `anonymous`.

Pozostałe informacje:

|Komunikat|Znaczenie|
|---|---|
|`220`|Serwer FTP gotowy|
|`331`|Serwer poprosił o hasło|
|`230`|Logowanie udane|
|`Remote system type is UNIX`|Serwer zgłasza system UNIX|
|`Using binary mode`|Transfer w trybie binarnym|

### **Wniosek do dokumentacji**

Na serwerze FTP `vsftpd 2.3.4` działa anonimowe logowanie. To potwierdza możliwość uzyskania sesji FTP bez indywidualnego konta.

Nie wiemy jeszcze, jakie pliki są dostępne ani czy anonimowy użytkownik ma prawo zapisu.

### **Krok 4 – sprawdzamy dostępne pliki**

Jesteś w sesji FTP. Wpisz tylko:

```
ls -la
```

To wyświetli listę plików i katalogów dostępnych dla zalogowanego użytkownika.

Na razie tylko odczyt — niczego nie pobieramy ani nie zmieniamy. Wklej wynik, a przeanalizujemy uprawnienia.

Dobrze. Mamy kolejny potwierdzony wynik.

### **Analiza** `ls -la`

Serwer zwrócił:

```
drwxr-xr-x    2 0        65534        4096 Mar 17  2010 .
drwxr-xr-x    2 0        65534        4096 Mar 17  2010 ..
```

Co to oznacza?

|Element|Znaczenie|
|---|---|
|`drwxr-xr-x`|Katalog: właściciel ma pełne prawa, pozostali odczyt i przejście|
|`2`|Liczba dowiązań katalogu|
|`0`|UID właściciela – root|
|`65534`|GID – zwykle mapowany na `nobody`|
|`4096`|Rozmiar wpisu katalogowego|
|`.` i `..`|Bieżący katalog i katalog nadrzędny|

**Najważniejszy wniosek:** anonimowy użytkownik może zalogować się do FTP, ale bieżący katalog nie zawiera widocznych plików. Nie wiemy jeszcze, czy dostępne są inne katalogi.

### **Krok 5 – sprawdzamy katalog roboczy**

Wpisz w sesji FTP:

```
pwd
```

Polecenie pokaże, w jakim katalogu serwer umieścił anonimowego użytkownika po zalogowaniu.

To ważna informacja. Serwer umieścił anonimowego użytkownika w katalogu głównym swojej przestrzeni FTP:

```
Remote directory: /
```

Uwaga: `/` oznacza katalog główny widoczny w sesji FTP, niekoniecznie katalog główny całego systemu Linux.

### **Aktualne ustalenia FTP**

- Logowanie anonimowe: **potwierdzone**.
    
- Katalog początkowy: `/`.
    
- Lista plików: pusta (`.` i `..`).
    
- Dostęp do innych katalogów: jeszcze nieustalony.
    
- Możliwość zapisu: jeszcze nieustalona.
    

### **Krok 6 – sprawdzamy uprawnienia**

W sesji FTP wpisz:

```
help
```

Chcę zobaczyć, jakie polecenia obsługuje klient FTP. Następnie wybierzemy bezpieczny sposób sprawdzenia zakresu dostępu anonimowego.


Dobrze. To lista poleceń obsługiwanych przez klienta FTP w Kali, a nie lista uprawnień przyznanych użytkownikowi na serwerze.

Ważne rozróżnienie: obecność `put`, `delete`, `mkdir` czy `chmod` na tej liście nie oznacza, że anonimowy użytkownik może wykonywać te operacje.

### **Co już wiemy?**

Mamy potwierdzone:

- anonimowe logowanie działa;
    
- katalog początkowy to `/`;
    
- katalog jest pusty;
    
- nie ustaliliśmy jeszcze zakresu dostępu ani praw zapisu.
    

### **Krok 7 – sprawdzamy możliwości serwera**

Wpisz w sesji FTP:

```
quote FEAT
```

To wyśle do serwera zapytanie o obsługiwane rozszerzenia FTP.

Dobrze. Serwer odpowiedział poprawnie na zapytanie `FEAT`. Mamy listę obsługiwanych rozszerzeń protokołu FTP.

### **Analiza wyniku**

```
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
```

|Funkcja|Znaczenie|
|---|---|
|`EPRT`|Rozszerzone wskazywanie adresu i portu transferu|
|`EPSV`|Rozszerzony tryb pasywny|
|`MDTM`|Odczyt czasu modyfikacji pliku|
|`PASV`|Tryb pasywny FTP|
|`REST STREAM`|Wznawianie transferu od wskazanego miejsca|
|`SIZE`|Sprawdzanie rozmiaru pliku|
|`TVFS`|Wirtualny system plików|
|`UTF8`|Obsługa kodowania UTF-8|

To standardowe możliwości protokołu. Same w sobie nie potwierdzają podatności.

### **Co mamy już udokumentowane?**

Potwierdzone

- vsftpd 2.3.4 na porcie 21.
    
- Anonimowe logowanie działa.
    
- Serwer przydziela katalog `/`.
    
- Katalog nie zawiera widocznych plików.
    
- Serwer obsługuje wymienione rozszerzenia FTP.
    

### **Krok 8 – sprawdzamy system serwera**

Wpisz:

```
quote SYST
```

To zapytanie pozwoli sprawdzić, jak serwer identyfikuje swój system operacyjny.

Dobrze. Odpowiedź serwera:

```
215 UNIX Type: L8
```

### **Analiza**

- `215` – pozytywna odpowiedź na zapytanie `SYST`.
    
- `UNIX` – serwer deklaruje system typu UNIX.
    
- `L8` – format listingu oparty na 8-bitowych bajtach, zgodny z formatem UNIX.
    

To potwierdza wcześniejszą informację `Remote system type is UNIX`.

Nie jest to dokładna identyfikacja dystrybucji ani wersji jądra Linux.

### **Krok 9 – sprawdzamy, czy anonimowy użytkownik może zmieniać katalogi**

W sesji FTP wpisz:

```
cd ..
```

To bezpieczna próba przejścia do katalogu nadrzędnego. Nie modyfikuje plików.

Bardzo ciekawy wynik.

```
250 Directory successfully changed.
```

Kod `250` oznacza, że serwer zaakceptował zmianę katalogu.

### **Co to oznacza?**

Anonimowy użytkownik wykonał `cd ..` i serwer nie odrzucił polecenia.

Ale uwaga: **nie dowodzi to jeszcze, że wyszedł poza przydzielony obszar FTP**. Serwer może ograniczać użytkownika mechanizmem chroot, a przejście do katalogu nadrzędnego może po prostu pozostawić go w wirtualnym `/`.

### **Krok 10 – sprawdzamy, gdzie teraz jesteśmy**

Wpisz:

```
pwd
```

I to jest istotna wskazówka.

Po wykonaniu `cd ..` nadal widzimy:

```
Remote directory: /
```

### **Interpretacja**

Najbardziej prawdopodobne wyjaśnienie: anonimowy użytkownik jest ograniczony do wirtualnego katalogu głównego FTP (mechanizm typu **chroot**).

Próba przejścia wyżej nie zmieniła widocznej ścieżki.

Nie traktujmy tego jeszcze jako stuprocentowego potwierdzenia chroot — potrzebowalibyśmy dodatkowych testów.

### **Krok 11 – sprawdzamy katalog nadrzędny przez listing**

Wpisz:

```
ls -la
```

Wklej wynik.

Sprawdzimy, czy nadal widzimy tylko `.` i `..`. Nie będziemy próbować omijać ograniczeń ani modyfikować systemu.

Wynik jest identyczny jak poprzednio. To dobra informacja do naszej dokumentacji.

### **Analiza**

Po wykonaniu `cd ..` ponownie otrzymaliśmy:

```
drwxr-xr-x  2 0 65534 4096 .
drwxr-xr-x  2 0 65534 4096 ..
```

Nie pojawiły się żadne nowe katalogi ani pliki.

**Co możemy stwierdzić:**

- `cd ..` zostało zaakceptowane przez serwer.
    
- `pwd` nadal wskazuje `/`.
    
- Listing katalogu nadal jest pusty.
    
- Zachowanie jest zgodne z hipotezą ograniczenia anonimowego użytkownika do wirtualnego katalogu FTP (chroot), ale nie potwierdza jej definitywnie.
    

### **Dotychczasowa ocena FTP**

|Obszar|Ustalenie|
|---|---|
|Usługa|vsftpd 2.3.4|
|Port|21/tcp|
|Anonimowe logowanie|Działa|
|Odczyt katalogu|Potwierdzony|
|Widoczne pliki|Brak|
|Zapis|Niebadany|
|Ograniczenie chroot|Prawdopodobne, niepotwierdzone|

### **Krok 12 – sprawdzamy, czy serwer obsługuje TLS**

Wpisz:

```
quote AUTH TLS
```

To zapytanie sprawdzi, czy serwer obsługuje możliwość przejścia na szyfrowane połączenie FTP.

Wklej odpowiedź. To ostatni element, który chcę dzisiaj sprawdzić w ramach podstawowej enumeracji portu 21.

500 Unknown command.

Dobrze, mamy odpowiedź serwera:

`500 Unknown command.`

### **Analiza**

Kod `500` oznacza, że serwer nie rozpoznał lub nie obsłużył polecenia `AUTH TLS`.

W praktyce oznacza to, że **nie udało nam się potwierdzić obsługi FTP over TLS**. W połączeniu z klasycznym FTP oznacza to ryzyko przesyłania loginu, hasła i danych bez szyfrowania.

Mała uwaga techniczna: odpowiedź `500` nie jest absolutnym dowodem braku TLS — serwer może nie obsługiwać tego rozszerzenia albo odrzucać polecenie w danym kontekście.

## **Podsumowanie FTP – port 21**

Podstawowa enumeracja zakończona

|Element|Wynik|
|---|---|
|Usługa|vsftpd 2.3.4|
|Port|21/tcp|
|Anonimowe logowanie|Potwierdzone|
|Katalog początkowy|`/`|
|Widoczne pliki|Brak|
|Zapis anonimowy|Nie sprawdzaliśmy|
|Chroot|Prawdopodobny, niepotwierdzony|
|Rozszerzenia FTP|FEAT potwierdzone|
|Identyfikacja systemu|UNIX Type: L8|
|AUTH TLS|Odpowiedź 500|

### **Notatka bezpieczeństwa**

Najważniejsze znalezisko to anonimowy dostęp do FTP. Drugim problemem jest brak potwierdzonej możliwości szyfrowania połączenia.

Nie testowaliśmy zapisu, pobierania plików ani podatności wersji 2.3.4.

### **Co dalej?**

Jutro możemy przejść do drugiej usługi FTP:

**ProFTPD 1.3.1 – port 2121.**

Zachowamy tę samą metodę: jedno polecenie, analiza wyniku, wniosek i dokumentacja.

Na dzisiaj dobra robota. Nie musimy robić wszystkiego podczas jednej sesji.