### 21/tcp   open  ftp         vsftpd 2.3.4




**Co to jest:** Protokół do przesyłania plików. Często źle skonfigurowany.

**Co sprawdzić:**

- Czy działa anonymous login
- Wersja serwera
- Możliwość zapisu plików
- Hasła domyślne

**Narzędzia:**  
nmap -sV -p21 --script ftp-* <IP>  
ftp <IP>  
hydra -L users.txt -P passwords.txt ftp://<IP>

**Cel:**  
Zdobyć dostęp do plików (hasła, konfiguracje, backupy, kod źródłowy). Czasem da się wgrać webshella (jeśli FTP jest powiązany z katalogiem WWW). Anonymous login lub słabe hasło = szybki foothold bez większego wysiłku.
Finding: Anonymous FTP Access Enabled  
Severity: do oceny po ustaleniu, jakie zasoby są dostępne.

curl -v --user anonymous:anonymous ftp://192.168.56.104/
curl --user anonymous:anonymous ftp://192.168.56.104/
curl -sS --user anonymous:anonymous --list-only ftp://192.168.56.104/ ; echo "Kod zakończenia: $?"
SMB – enumeracja udziałów sieciowych.
SMB (Server Message Block) służy m.in. do udostępniania plików i drukarek w sieci. Sprawdzimy, czy Metasploitable 2 udostępnia zasoby, do których można uzyskać dostęp bez uwierzytelnienia.
smbclient -L //192.168.56.104 -N
smbclient //192.168.56.104/tmp -N
smbclient //192.168.56.104/opt -N
put /etc/hostname
allinfo .   posix_whoami

##Podsumujmy dotychczasowe ustalenia SMB:
- Lista udziałów dostępna bez hasła.
- `tmp` – anonimowe wejście i odczyt katalogu potwierdzone.
- `opt` – odmowa dostępu.
- Uprawnienia do zapisu – jeszcze nieustalone.   
- Tożsamość sesji POSIX – nieustalona.





### 6. HTTP (port 80)  HTTP – enumeracja serwera WWW Apache.

**Co to jest:** Zwykły ruch webowy.

**Co sprawdzić:**

- Co to za aplikacja i wersja
- Ukryte katalogi i pliki
- Podstawowe podatności (SQLi, XSS, LFI, IDOR)

**Narzędzia:**  
whatweb / httpx  
feroxbuster / gobuster  
nikto  
Burp Suite

**Cel:**  
Znaleźć podatność, która da dostęp do systemu lub danych. Najczęstsze efekty: odczyt plików, obejście logowania, zdalne wykonanie kodu (RCE), kradzież sesji. Web to najczęściej atakowana powierzchnia.

curl -I http://192.168.56.104/
curl -s http://192.168.56.104/ | head -30
curl -i -X OPTIONS http://192.168.56.104/dav/
curl -i -X PROPFIND -H "Depth: 1" http://192.168.56.104/dav/

Co robi PROPFIND?
To metoda WebDAV służąca do odczytywania właściwości zasobów i listowania zawartości katalogu.
Parametr `Depth: 1` oznacza sprawdzenie katalogu oraz jego bezpośrednich elementów.
Nie modyfikujemy żadnych plików. To operacja odczytowa.

WebDAV Enabled – Directory Metadata Disclosure

- Usługa: Apache 2.2.8 (Ubuntu).
- Lokalizacja: `/dav/`.
- Metoda: `PROPFIND`.
- Odpowiedź: `207 Multi-Status`.
- Ujawnione informacje: typ zasobu, daty, ETag i obsługiwane blokady.
- Widoczne pliki: brak.
- Możliwość zapisu: nieustalona.

Nie klasyfikujemy tego automatycznie jako poważnej podatności. Mamy potwierdzoną funkcjonalność WebDAV i ujawnienie metadanych katalogu.



### HTTP rekonesansu Mutillidae

curl -I http://192.168.56.104/mutillidae/

HTTP 200 OK
Aplikacja dostępna

Przeanalizujmy otrzymane nagłówki:

|Nagłówek|Znaczenie|
|---|---|
|`HTTP/1.1 200 OK`|Serwer poprawnie obsłużył żądanie.|
|`Apache/2.2.8 (Ubuntu) DAV/2`|Serwer Apache w starszej wersji.|
|`X-Powered-By: PHP/5.2.4`|Aplikacja korzysta ze starej wersji PHP.|
|`Expires`|Informacja dotycząca wygasania zawartości.|
|`Logged-In-User`|Niestandardowy nagłówek związany ze stanem logowania aplikacji.|

Wnioski z rekonesansu:

1. Mutillidae odpowiada prawidłowo.
2. Potwierdziliśmy środowisko Apache + PHP.
3. Wykryliśmy historyczne wersje oprogramowania, które będą interesujące podczas późniejszej analizy bezpieczeństwa.
4. Na tym etapie nie wykonaliśmy żadnej operacji modyfikującej.


### Krok 2 – Rozpoznanie technologii i zawartości HTTP

Teraz sprawdzimy, co aplikacja ujawnia w odpowiedzi na zwykłe żądanie GET.
Nadal pracujemy wyłącznie na Kali Linux.
Wykonaj:

```
curl -s http://192.168.56.104/mutillidae/ | head -n 30
```

Dlaczego?
- `-s` – wycisza komunikaty postępu. 
- `curl` – pobiera stronę aplikacji. 
- `head -n 30` – wyświetla pierwsze 30 linii HTML.


Co tutaj odkryliśmy?
1. Aplikacja ujawnia potencjalne informacje dotyczące konfiguracji bazy danych. 
2. Komentarz wskazuje dwa możliwe warianty hasła: puste lub `samurai`. 
3. Autor komentarza błędnie zakłada, że komentarze HTML nie są widoczne dla użytkownika. 
4. Informacja jest dostępna bez logowania, bezpośrednio w odpowiedzi HTTP.

To klasyczny przykład problemu z kategorii Information Disclosure (ujawnianie informacji).

Ważne: nie wiemy jeszcze, jakie hasło faktycznie skonfigurowano. Komentarz jest wskazówką, a nie potwierdzeniem konfiguracji.

### Dokumentacja naszego rekonesansu

|Obserwacja|Wynik|
|---|---|
|Dostępność aplikacji|HTTP 200|
|Serwer|Apache 2.2.8|
|PHP|5.2.4|
|Informacje w komentarzach HTML|Tak|
|Potencjalne dane konfiguracyjne|Tak|
|Modyfikacja zasobów|Nie|

### Krok 3 – Rozpoznanie struktury aplikacji

Teraz sprawdzimy, jakie odnośniki aplikacja udostępnia w kodzie HTML.
Wykonaj na Kali Linux jedno polecenie:
```
curl -s http://192.168.56.104/mutillidae/ | grep -oiE 'href="[^"]+"|src="[^"]+"'
```

Dlaczego?

- `grep` – wyszukuje interesujące fragmenty.  
- `-o` – pokazuje wyłącznie dopasowane fragmenty.
- `-i` – ignoruje wielkość liter. 
- `-E` – umożliwia używanie wyrażeń regularnych.
    
Dzięki temu zobaczymy odnośniki i zasoby aplikacji, które pomogą nam zrozumieć jej strukturę.
Wklej wynik. Na razie nie wykonujemy skanowania ani nie testujemy podatności.
Idziemy metodycznie – najpierw rozpoznanie, potem analiza.

Bardzo dobry wynik. Teraz mamy znacznie pełniejszy obraz aplikacji Mutillidae. Co ważne, odkryliśmy nie tylko zwykłe zasoby strony, ale również dużą liczbę funkcjonalności treningowych związanych z podatnościami webowymi.

### Krok 3 – Analiza struktury aplikacji

Rekonesans zakończony pomyślnie

Zidentyfikowaliśmy kilka interesujących grup zasobów.

1. Uwierzytelnianie i zarządzanie użytkownikami
- `login.php`
- `register.php`  
- `user-info.php`
    
1. Funkcjonalności związane z danymi
- `add-to-your-blog.php`
- `view-someones-blog.php`
- `capture-data.php`
- `captured-data.php`

1. Funkcjonalności treningowe związane z bezpieczeństwem
- `text-file-viewer.php`
- `source-viewer.php`
- `arbitrary-file-inclusion.php`
- `dns-lookup.php`
- `password-generator.php`
- `browser-info.php`
    
1. Elementy administracyjne i diagnostyczne
- `show-log.php`
- `secret-administrative-pages.php`
- `set-up-database.php`
- `installation.php`
    
To bardzo wartościowy materiał do dalszego rekonesansu.

### Ważne obserwacje

Zwróć uwagę na trzy rzeczy:

- Parametr `page` występuje w wielu adresach. Będziemy go obserwować, ponieważ odpowiada za wybór wyświetlanej zawartości.
- `arbitrary-file-inclusion.php` wskazuje na funkcjonalność przeznaczoną do ćwiczenia problematyki dołączania plików.
- `source-viewer.php` i `text-file-viewer.php` mogą pomóc w poznaniu sposobu działania aplikacji.
    
Nie zakładamy jeszcze, że którakolwiek z tych funkcjonalności jest podatna. Sama obecność linku nie jest dowodem podatności.

### Krok 4 – Sprawdzenie pliku robots.txt

Zanim przejdziemy do analizy parametrów aplikacji, sprawdzimy, czy serwer udostępnia plik `robots.txt`.
Dlaczego?

Plik ten może zawierać wskazówki dotyczące ścieżek, których administrator nie chce indeksować przez wyszukiwarki. Nie jest mechanizmem kontroli dostępu, ale bywa źródłem informacji podczas rekonesansu.

Na Kali Linux wykonaj jedno polecenie:

```
curl -i http://192.168.56.104/robots.txt
```

Sprawdzimy:
- czy plik istnieje,
- jaki kod HTTP zwraca serwer,
- czy zawiera dodatkowe ścieżki aplikacji.

### Krok 4 – Analiza robots.txt

HTTP 404 – plik nie istnieje
Otrzymaliśmy:

```
HTTP/1.1 404 Not Found
Server: Apache/2.2.8 (Ubuntu) DAV/2
```
Wnioski:

1. Plik `/robots.txt` nie istnieje w katalogu głównym serwera.
2. Apache poprawnie zwraca kod 404.
3. Nie uzyskaliśmy dodatkowych informacji o ukrytych ścieżkach.
4. Nie oznacza to, że aplikacja nie posiada innych dostępnych zasobów.

Warto odnotować, że sprawdziliśmy katalog główny serwera, a nie katalog samej aplikacji.

### Aktualna dokumentacja rekonesansu

|Test|Wynik|
|---|---|
|Dostępność Mutillidae|HTTP 200|
|Identyfikacja Apache/PHP|Sukces|
|Analiza komentarzy HTML|Informacje konfiguracyjne|
|Rozpoznanie odnośników|Wiele funkcjonalności|
|robots.txt|HTTP 404|

### Krok 5 – Sprawdzenie nagłówków bezpieczeństwa HTTP

Teraz sprawdzimy, czy serwer udostępnia podstawowe nagłówki bezpieczeństwa.
Na Kali Linux wykonaj:

```
curl -s -D - -o /dev/null http://192.168.56.104/mutillidae/
```

Polecenie pobiera nagłówki odpowiedzi, ale nie wyświetla treści HTML.

Sprawdzimy obecność między innymi:
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Content-Security-Policy`
- `Strict-Transport-Security`
    

Nie zakładamy z góry, że ich brak oznacza podatność. Będziemy oceniać je w kontekście aplikacji treningowej.
Wklej wynik. Następnie podsumujemy rekonesans HTTP i zdecydujemy o kolejnym etapie.

### Krok 5 – Analiza nagłówków HTTP

Odpowiedź HTTP 200 OK

Przeanalizujmy wynik:

|Nagłówek|Wynik|Znaczenie|
|---|---|---|
|Server|Apache 2.2.8|Stara wersja serwera|
|X-Powered-By|PHP 5.2.4|Ujawniona wersja PHP|
|Logged-In-User|Pusty|Brak informacji o zalogowanym użytkowniku|
|Cache-Control|public|Odpowiedź może być buforowana|
|Pragma|public|Dyrektywa dotycząca buforowania|
|Set-Cookie|PHPSESSID|Serwer tworzy sesję PHP|
|X-Frame-Options|Brak|Nie zaobserwowano nagłówka|
|X-Content-Type-Options|Brak|Nie zaobserwowano nagłówka|
|Content-Security-Policy|Brak|Nie zaobserwowano nagłówka|
|Strict-Transport-Security|Brak|Nie zaobserwowano nagłówka|

Trzy najważniejsze obserwacje:

1. Ujawnianie technologii – Apache i PHP ujawniają swoje wersje.
2. Zarządzanie sesją – aplikacja tworzy identyfikator `PHPSESSID`.
3. Nagłówki bezpieczeństwa – nie zaobserwowaliśmy podstawowych nagłówków ochronnych.

Uwaga: brak tych nagłówków jest obserwacją konfiguracyjną, a nie automatycznym dowodem wykorzystania podatności. HSTS ma szczególne znaczenie w kontekście HTTPS, którego tutaj nie testowaliśmy.

Nie publikujmy również wartości `PHPSESSID` w żadnych publicznych raportach. To identyfikator sesji.

### Podsumowanie dotychczasowego rekonesansu Mutillidae

## Rekonesans HTTP
Dostępność aplikacji - Potwierdzona
Identyfikacja technologii - Wykonana
Analiza HTML - Wykonana
Rozpoznanie ścieżek - Wykonane
robots.txt - HTTP 404
Nagłówki bezpieczeństwa - Przeanalizowane


Krok 6 – Sprawdzenie obsługiwanych metod HTTP

curl -i -X OPTIONS http://192.168.56.104/mutillidae/
curl -I http://192.168.56.104/mutillidae/


### Krok 7 – Analiza metody HEAD

HTTP 200 OK

Porównajmy trzy dotychczas sprawdzone metody:

|Metoda|Wynik|Obserwacja|
|---|---|---|
|GET|200 OK|Zwraca zawartość HTML|
|OPTIONS|200 OK|Zwraca treść aplikacji, bez `Allow`|
|HEAD|200 OK|Zwraca nagłówki bez treści HTML|

Co jest istotne?

- Apache ujawnia wersję serwera.
- PHP ujawnia wersję środowiska.
- Aplikacja tworzy identyfikator sesji również przy HEAD.
- Nie zaobserwowaliśmy nagłówka `Allow`.
- Nie zaobserwowaliśmy podstawowych nagłówków bezpieczeństwa.
    

Pamiętajmy, że HEAD powinien odpowiadać nagłówkami analogicznymi do GET, bez treści odpowiedzi. Nasz wynik jest z tym zgodny.

### Dokumentacja – metody HTTP

Mutillidae – 192.168.56.104:80
Metoda GET 200 OK
Metoda OPTIONS 200 OK
Metoda HEAD 200 OK

Zakres: pasywny rekonesans HTTP, bez modyfikowania zasobów.

### Krok 8 – Sprawdzenie metod HTTP przez Nmap
Teraz wykorzystamy drugie narzędzie, aby porównać wyniki z `curl`.

```
nmap -p 80 --script http-methods 192.168.56.104
```

Dlaczego?

Nmap spróbuje rozpoznać metody HTTP udostępniane przez serwer i przedstawi wynik w bardziej uporządkowanej formie.

### Krok 8 – Analiza metod HTTP
4 metody rozpoznane
Nmap wykrył:
```
Supported Methods: GET HEAD POST OPTIONS
```
Interpretacja:

|Metoda|Zastosowanie|
|---|---|
|GET|Pobieranie zasobów|
|HEAD|Pobieranie samych nagłówków|
|POST|Przesyłanie danych do aplikacji|
|OPTIONS|Informacje o metodach HTTP|

Co oznacza ten wynik?

1. Serwer udostępnia cztery rozpoznane metody.
2. GET i HEAD potwierdziliśmy wcześniej ręcznie.
3. OPTIONS odpowiedziało kodem 200.
4. POST został zidentyfikowany przez Nmap, ale nie testowaliśmy jeszcze jego działania.

Ważne: POST jest normalną metodą HTTP. Sama jej obecność nie oznacza podatności.

### Aktualizacja dokumentacji

|Obszar|Wynik|
|---|---|
|Apache|2.2.8|
|PHP|5.2.4|
|GET|Dostępna|
|HEAD|Dostępna|
|POST|Rozpoznana przez Nmap|
|OPTIONS|Dostępna|
|robots.txt|404|
|Nagłówki bezpieczeństwa|Nie zaobserwowano podstawowych nagłówków|

### Co dalej?
Proponuję zamknąć rozpoznanie metod HTTP i przejść do kolejnego zagadnienia:
Krok 9 – Rozpoznanie katalogów i zasobów serwera WWW.
Chcemy ustalić, jakie katalogi są publicznie dostępne i czy serwer ujawnia ich zawartość.
Wykorzystamy do tego Nmap, bez prób zapisywania lub modyfikowania plików.
Na razie nie wpisuj kolejnej komendy. Najpierw potwierdźmy, że dokumentacja metod HTTP jest kompletna.
Bardzo dobrze prowadzisz ten rekonesans – zaczynamy już łączyć wyniki z kilku narzędzi, a nie opierać się na pojedynczej obserwacji.

### Rozpoznanie katalogów i zasobów serwera WWW przy użyciu Nmap.

Wykorzystamy skrypt `http-enum`, który sprawdza typowe ścieżki i zasoby serwera WWW.
Na Kali Linux wykonaj jedno polecenie:

```
nmap -p 80 --script http-enum 192.168.56.104
```

Co robi polecenie?

- `nmap` – narzędzie do rozpoznania sieci.
- `-p 80` – ograniczamy sprawdzanie do portu HTTP.
- `--script http-enum` – wyszukuje znane katalogi i zasoby WWW.
- `192.168.56.104` – nasz Metasploitable 2.

Będziemy szukać między innymi:
- dostępnych katalogów,
- paneli administracyjnych,
- aplikacji treningowych,
- plików diagnostycznych,
- ewentualnego indeksowania zawartości katalogów.
    
To rozpoznanie odczytowe, bez celowego zapisywania lub modyfikowania plików.

## Krok 9.1 – Analiza wyników Nmap

6 interesujących ścieżek wykrytych

|Ścieżka|Wykrycie|Znaczenie|
|---|---|---|
|`/tikiwiki/`|Tikiwiki|Dodatkowa aplikacja webowa|
|`/test/`|Test page|Strona testowa|
|`/phpinfo.php`|Possible information file|Możliwy wyciek konfiguracji PHP|
|`/phpMyAdmin/`|phpMyAdmin|Interfejs zarządzania MySQL|
|`/doc/`|Directory listing|Potwierdzone indeksowanie katalogu|
|`/icons/`|Directory listing|Potwierdzone indeksowanie katalogu|
|`/index/`|Interesting folder|Wymaga dalszej weryfikacji|

Mała korekta: Nmap wykrył siedem ścieżek, z czego dwie mają wyraźnie oznaczone directory listing.

### Co jest szczególnie interesujące?

1. `/phpinfo.php`
Może ujawniać:
- wersję PHP,
- konfigurację serwera,
- załadowane moduły,
- zmienne środowiskowe.

2. `/phpMyAdmin/`

To interfejs administracyjny bazy danych. W przyszłości możemy zbadać jego dostępność i sposób uwierzytelniania.

3. `/doc/` i `/icons/`

Nmap wskazuje na możliwość przeglądania zawartości katalogów. To konkretna obserwacja dotycząca konfiguracji Apache.

4. `/tikiwiki/`

Odkryliśmy kolejną aplikację treningową. Nie będziemy jednak przeskakiwać do niej przed zakończeniem rekonesansu.

## Krok 9.2 – Weryfikacja phpinfo.php

Zaczniemy od zasobu, który potencjalnie ujawnia najwięcej informacji o konfiguracji serwera.

Na Kali Linux wykonaj jedno polecenie:

```
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nContent-Type: %{content_type}\nSize: %{size_download} bytes\n" http://192.168.56.104/phpinfo.php
```

Dlaczego?

Chcemy potwierdzić:
- czy plik faktycznie istnieje;
- czy serwer zwraca HTTP 200;
- jaki typ zawartości udostępnia;
- jak duża jest odpowiedź.

Na razie nie pobieramy pełnej konfiguracji PHP i nie wykonujemy żadnych zmian.

## Krok 9.2 – Analiza phpinfo.php

HTTP 200 – zasób dostępny
Otrzymaliśmy:

|Parametr|Wynik|
|---|---|
|HTTP Status|200|
|Content-Type|text/html|
|Rozmiar odpowiedzi|47 987 bajtów|
|Dostępność bezpośrednia|Potwierdzona|

Dlaczego to ważne?

Strona PHPInfo może ujawniać:
- wersję PHP i konfigurację interpreterа;
- aktywne rozszerzenia;
- ścieżki systemowe;
- ustawienia serwera WWW;
- zmienne środowiskowe;
- konfigurację sesji.
    

To potencjalny przykład Information Disclosure.
Pamiętajmy, że sam kod 200 nie potwierdza jeszcze, jakie informacje faktycznie są widoczne.

## Krok 9.3 – Identyfikacja wersji PHP
Teraz wyciągniemy z odpowiedzi tylko najważniejsze informacje dotyczące wersji PHP.
Na Kali Linux wykonaj:

```
curl -s http://192.168.56.104/phpinfo.php | grep -i -m 5 "PHP Version"
```

Dlaczego tak?
- `curl -s` – pobiera stronę.
- `grep -i` – wyszukuje tekst bez uwzględniania wielkości liter.
- `-m 5` – ogranicza liczbę dopasowań do pięciu.
    
Chcemy porównać wersję PHP ujawnioną przez phpinfo z wersją poznaną wcześniej w nagłówku HTTP.

Porównanie z wcześniejszym rekonesansem:
|Źródło informacji|Wersja PHP|
|---|---|
|Nagłówek HTTP `X-Powered-By`|5.2.4-2ubuntu5.10|
|Strona `phpinfo.php`|5.2.4-2ubuntu5.10|

Oba źródła są zgodne.
Wniosek bezpieczeństwa:
Publicznie dostępny `phpinfo.php` ujawnia szczegółowe informacje o środowisku serwera. W rzeczywistym środowisku produkcyjnym taka strona nie powinna być publicznie dostępna.

W naszym laboratorium jest to doskonały przykład Information Disclosure.

## Krok 9.4 – Sprawdzenie katalogu /doc/

Teraz zajmiemy się jednym z dwóch katalogów, dla których Nmap wykrył możliwość przeglądania zawartości.
Cel: potwierdzić, czy serwer rzeczywiście udostępnia indeks katalogu.
Na Kali Linux wykonaj:

```
curl -s http://192.168.56.104/doc/ | head -n 30
```

Sprawdzimy:
- czy pojawia się lista plików;
- czy Apache generuje indeks katalogu;
- jakie nazwy zasobów są widoczne.

To operacja odczytowa – niczego nie zmieniamy.

## Krok 9.4 – Analiza katalogu /doc/

Directory Listing potwierdzony
Serwer zwrócił stronę:

```
<title>Index of /doc</title>
<h1>Index of /doc</h1>
```

To oznacza, że Apache udostępnia automatyczny indeks katalogu.
### Co dokładnie ujawnia serwer?

Wynik zawiera między innymi:
- `apache2/`
- `apache2.2-common/`
- `apache2-utils/`
- `apparmor/`
- `apt/`
- `bash/`
- `adduser/`
    

Widać również daty modyfikacji katalogów, np. z 2010 roku.

Dlaczego to problem bezpieczeństwa?

1. Użytkownik może przeglądać strukturę katalogów bez uwierzytelnienia.
2. Ujawniene są nazwy zainstalowanych pakietów.
3. Można uzyskać informacje o środowisku systemowym.
4. Informacje te mogą ułatwić dalszy rekonesans.

W tym przypadku `/doc/` wygląda na katalog dokumentacji pakietów systemowych Ubuntu.

### Wpis do dokumentacji

|Parametr|Wynik|
|---|---|
|Zasób|`/doc/`|
|Directory Listing|Potwierdzony|
|Uwierzytelnienie|Nie jest wymagane|
|Przykładowe katalogi|apache2, bash, apparmor, apt|
|Ryzyko|Ujawnianie informacji|


## Krok 9.5 – Sprawdzenie katalogu /icons/

Nmap wskazał drugi katalog z potencjalnym indeksowaniem.
Sprawdzimy go analogicznie.
Na Kali Linux wykonaj:

```
curl -s http://192.168.56.104/icons/ | head -n 30
```

Cel: ustalić, czy `/icons/` również ujawnia zawartość katalogu.
Nie pobieramy całej zawartości i nie modyfikujemy żadnych plików.
Wklej wynik. Najpierw przeanalizujemy `/icons/`, a później zamkniemy ten fragment rekonesansu.

Świetnie. Mamy kolejne potwierdzenie — katalog `/icons/` również udostępnia Directory Listing, czyli publiczny spis plików bez konieczności logowania.

### Analiza wyniku – `/icons/`
Potwierdzone

Directory Listing jest aktywny.
Wynik pokazuje:
- Index of /icons – serwer Apache generuje automatyczny indeks katalogu.
- `README` i `README.html` – dostępne pliki tekstowe z dokumentacją.
- Pliki graficzne `.gif` i `.png` – ikony wykorzystywane przez Apache.
- Daty modyfikacji z 2004 i 2007 roku – dodatkowa wskazówka dotycząca wieku zasobów.

Co to oznacza z punktu widzenia bezpieczeństwa?

Samo udostępnienie ikon nie jest poważną podatnością. Problemem jest konfiguracja serwera, która pozwala przeglądać zawartość katalogów. W innych katalogach podobna konfiguracja może ujawnić pliki, których administrator nie zamierzał publikować.

Mamy już dwa potwierdzone przypadki:

|Katalog|Wynik|Znaczenie|
|---|---|---|
|`/doc/`|Directory Listing|Ujawnianie dokumentacji pakietów|
|`/icons/`|Directory Listing|Ujawnianie zawartości katalogu ikon|

### Następny krok – dokumentacja Apache

Chciałbym sprawdzić zawartość pliku `README` z katalogu `/icons/`. To nadal operacja wyłącznie odczytowa.
Maszyny: Kali Linux i Metasploitable 2 – obie pozostają uruchomione. Pracujemy z Kali.

Wykonaj jedno polecenie:

```
curl -s http://192.168.56.104/icons/README | head -n 30
```

### Analiza pliku `/icons/README`

W tym przypadku mamy ważne rozróżnienie: plik README nie zawiera informacji o konfiguracji serwera ani danych poufnych.

Zawiera natomiast:

- informację, że ikony pochodzą z projektu Mosaic for X i były rozpowszechniane wraz z NCSA httpd oraz Apache;
- informację o licencji Public Domain – ikony można swobodnie wykorzystywać;
- nazwiska autorów i historię zestawu ikon;
- sugestie dotyczące wykorzystania poszczególnych grafik.

Czyli sam plik jest nieszkodliwą dokumentacją.

### Co zapisujemy w wynikach rekonesansu?

Mamy już trzy obserwacje:

|Zasób|Ustalenie|Klasyfikacja|
|---|---|---|
|`/mutillidae/`|Ujawnianie informacji w komentarzu HTML|Information Disclosure|
|`/doc/`|Publiczny listing dokumentacji pakietów|Directory Listing|
|`/icons/`|Publiczny listing ikon i plików README|Directory Listing|

Dodatkowo potwierdziliśmy publicznie dostępny `phpinfo.php`, który ujawnia wersję PHP i szczegóły środowiska.
Ważny wniosek: nie każdy publicznie dostępny plik jest podatnością. W rekonesansie zbieramy fakty, a dopiero później oceniamy ich znaczenie i ryzyko.

Na tym etapie nie potrzebujemy już analizować kolejnych ikon. Proponuję zamknąć ten fragment rekonesansu i przejść później do uporządkowania zebranych informacji o serwerze HTTP — bez modyfikowania czegokolwiek na Metasploitable 2.

### **Plan dalszej pracy**

1. **Weryfikacja pozostałych zasobów HTTP** – sprawdzimy ręcznie wybrane ścieżki znalezione przez Nmap, m.in. `/test/`, `/phpMyAdmin/` i `/tikiwiki/`.
2. **Ocena ujawnionych informacji** – ustalimy, co jest zwykłą informacją, a co może stanowić realne ryzyko.
3. **Podsumowanie rekonesansu** – przygotujemy tabelę: zasób, wynik, potencjalne ryzyko i dowód.
4. **Następne ćwiczenie** – dopiero po zamknięciu HTTP wybierzemy kolejny obszar laboratorium.

### **Zaczynamy od jednego kroku**

Maszyny uruchomione

- Kali Linux – `192.168.56.103`
    
- Metasploitable 2 – `192.168.56.104`
    

Pozostałe maszyny pozostają wyłączone.

**Krok 10 – ręczna weryfikacja** `/test/`

Nmap wskazał tę ścieżkę jako potencjalnie interesującą. Teraz sprawdzimy, co faktycznie serwer pod nią udostępnia.

W Kali wykonaj:

```
curl -s http://192.168.56.104/test/ | head -n 20
```

### **Krok 11 – sprawdzenie podkatalogu**
**Maszyny:** Kali Linux i Metasploitable 2 – bez zmian.
W Kali wykonaj jedno polecenie:
```
curl -s http://192.168.56.104/test/testoutput/ | head -n 25
```

Bardzo dobrze. Odkryliśmy coś ciekawego — podkatalog `/test/testoutput/` zawiera plik o nazwie:

`ESAPI_logging_file_test`

### **Analiza wyniku**
Dostępność potwierdzona
|Element|Ustalenie|
|---|---|
|Katalog|`/test/testoutput/`|
|Plik|`ESAPI_logging_file_test`|
|Rozmiar|0 bajtów|
|Data|14.05.2012|
|Dostęp|Publiczny listing|

**Co oznacza nazwa ESAPI?**
ESAPI (Enterprise Security API) to biblioteka związana z bezpieczeństwem aplikacji. Nazwa pliku sugeruje, że może być związany z testowaniem mechanizmu logowania.

Nie wyciągamy jednak wniosku o podatności. Plik ma 0 bajtów, a sama nazwa nie dowodzi, że mechanizm logowania jest wadliwy.
### **Krok 12 – sprawdzenie pliku**

Chcemy potwierdzić, czy plik rzeczywiście jest pusty i jaki status HTTP zwraca serwer.
**Maszyny:** Kali Linux i Metasploitable 2 – nadal uruchomione.

W Kali wykonaj:

```
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nSize: %{size_download} bytes\nContent-Type: %{content_type}\n" http://192.168.56.104/test/testoutput/ESAPI_logging_file_test
```

Świetnie. Wynik jednoznacznie potwierdza, że plik jest dostępny przez HTTP.
### **Krok 12 – interpretacja**
Dostęp potwierdzony

|Parametr|Wynik|
|---|---|
|HTTP Status|`200 OK`|
|Rozmiar|`0 bytes`|
|Content-Type|`text/plain`|
|Dostęp|Bez uwierzytelnienia|

Co z tego wynika?

1. Serwer udostępnia plik anonimowemu użytkownikowi.
2. Plik jest pusty – nie zawiera obecnie danych.
3. Nazwa sugeruje związek z testami ESAPI, ale nie dowodzi żadnego problemu z logowaniem.
4. W połączeniu z listingiem katalogu potwierdza niepotrzebne ujawnianie struktury zasobów.

**Wniosek:** zapisujemy to jako obserwację informacyjną, a nie jako potwierdzoną podatność ESAPI.

### **Krok 13 – sprawdzamy phpMyAdmin**
Teraz przejdziemy do kolejnego zasobu wykrytego przez Nmap: `/phpMyAdmin/`.
Chcemy ustalić, czy panel jest rzeczywiście dostępny i jak odpowiada serwer. Nie próbujemy logowania ani zgadywania haseł.

**Uruchomione maszyny:**

- Kali Linux – `192.168.56.103`
    
- Metasploitable 2 – `192.168.56.104`
    

W Kali wykonaj:

```
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nContent-Type: %{content_type}\nSize: %{size_download} bytes\n" http://192.168.56.104/phpMyAdmin/
```

### **Krok 13 – analiza wyniku**
Dostępność potwierdzona
|Parametr|Wynik|
|---|---|
|Adres|`/phpMyAdmin/`|
|HTTP Status|`200 OK`|
|Content-Type|`text/html; charset=utf-8`|
|Rozmiar odpowiedzi|4145 bajtów|

Co wiemy na tym etapie?

- Serwer udostępnia zasób phpMyAdmin.
- Odpowiedź zawiera dokument HTML.
- Nie wiemy jeszcze, czy jest to właściwy panel logowania, strona informacyjna czy przekierowanie obsłużone przez aplikację.
- Nie sprawdzaliśmy uwierzytelniania ani dostępu do bazy danych.

### **Krok 14 – rozpoznanie zawartości strony**
Chcemy zobaczyć tytuł strony i pierwsze elementy HTML, aby zidentyfikować faktycznie udostępniony zasób.
**Maszyny:** Kali Linux i Metasploitable 2 – nadal uruchomione.
W Kali wykonaj:

```
curl -s http://192.168.56.104/phpMyAdmin/ | grep -iE '<title>|phpmyadmin|login' | head -n 15
```

### **Krok 14 – analiza wyniku**
Panel logowania potwierdzony

Zidentyfikowaliśmy:
- Tytuł strony: `phpMyAdmin`.
- Formularz logowania: `login_form`.
- Metoda formularza: `POST`.
- Punkt obsługi formularza: `index.php`.
- Mechanizm tokenów sesyjnych i formularza.

**Ważna obserwacja:** w odpowiedzi znajduje się token. Nie traktujemy go jako hasła ani dowodu podatności. To element mechanizmu obsługi formularza. Nie będziemy go publikować ani ponownie wykorzystywać.

### **Co zapisujemy w naszym rekonesansie?**
|Obserwacja|Znaczenie|
|---|---|
|phpMyAdmin dostępny|Panel administracyjny bazy danych jest wystawiony przez HTTP|
|Formularz logowania|Dostęp wymaga przejścia przez mechanizm uwierzytelniania|
|POST|Formularz przesyła dane metodą POST|
|HTTP bez szyfrowania|Dane przesyłane przez tę usługę nie są chronione przez TLS|

Ostatni punkt jest istotny: panel administracyjny dostępny przez nieszyfrowane HTTP stanowi ryzyko, szczególnie podczas przesyłania danych logowania.

### **Krok 15 – identyfikacja wersji phpMyAdmin**
Zanim przejdziemy dalej, ustalmy wersję panelu. To ważne, ponieważ pozwoli później ocenić, czy używane oprogramowanie jest przestarzałe.
**Maszyny:** Kali Linux i Metasploitable 2 – bez zmian.
Wykonaj w Kali:

```
curl -s http://192.168.56.104/phpMyAdmin/ | grep -iE 'phpMyAdmin [0-9]|version'
```

W porządku. Nie ma sensu wymuszać identyfikacji wersji na podstawie strony logowania.

Zapisujemy:
- **phpMyAdmin:** panel logowania potwierdzony.
- **Dostęp:** HTTP, bez TLS.
- **Wersja:** nieustalona.
- **Uwierzytelnianie:** nie testowaliśmy.
- **Dostęp do bazy:** nie testowaliśmy.

To ważna zasada rekonesansu: brak wyniku również jest wynikiem. Nie dopisujemy informacji, których nie potwierdziliśmy.

### **Krok 16 – kolejny zasób: TikiWiki**
Nmap wcześniej wykrył `/tikiwiki/`. Sprawdzimy teraz, czy aplikacja jest dostępna.
**Maszyny:**
- Kali Linux – `192.168.56.103`
- Metasploitable 2 – `192.168.56.104`

W Kali wykonaj jedno polecenie:

```
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nContent-Type: %{content_type}\nSize: %{size_download} bytes\n" http://192.168.56.104/tikiwiki/
```

### **Krok 16 – analiza wyniku**
|Parametr|Wynik|
|---|---|
|Adres|`/tikiwiki/`|
|HTTP Status|`200 OK`|
|Content-Type|`text/html; charset=utf-8`|
|Rozmiar|316 bajtów|

Jedna rzecz zwraca uwagę: **odpowiedź ma zaledwie 316 bajtów**. Nie wiemy jeszcze, czy to właściwa aplikacja TikiWiki, strona przekierowująca, czy komunikat błędu wygenerowany z kodem 200.
### **Krok 16.1 – sprawdzamy zawartość odpowiedzi**

Maszyny pozostają bez zmian: Kali i Metasploitable 2.
W Kali wykonaj:
```
curl -s http://192.168.56.104/tikiwiki/
```

### **Krok 16 – analiza TikiWiki**
Błąd konfiguracji potwierdzony
Odpowiedź serwera ujawnia kilka istotnych informacji:
1. **TikiWiki nie jest prawidłowo skonfigurowane** – aplikacja sama informuje o problemie.
2. **Brak połączenia z bazą danych** – komunikat `Unable to connect to the database!`.
3. **Ujawnienie szczegółów błędu bazy danych** – serwer ujawnia:  
    `Access denied for user 'root'@'localhost'`.
4. **Ujawnienie ścieżki instalacyjnej** – aplikacja wskazuje `tiki-install.php`.

### **Dlaczego to jest istotne?**

To przykład _Information Disclosure through Error Messages_ – aplikacja ujawnia informacje techniczne, które normalny użytkownik nie powinien widzieć.

Szczególnie istotne jest ujawnienie:
- nazwy konta bazy danych (`root`);
- lokalizacji połączenia (`localhost`);
- faktu, że aplikacja próbuje uwierzytelniać się hasłem;
- problemu z konfiguracją bazy danych.

Nie oznacza to, że uzyskaliśmy dostęp do bazy danych. Wręcz przeciwnie – komunikat potwierdza odmowę dostępu.

### **Aktualny rejestr ustaleń**
|Zasób|Potwierdzona obserwacja|
|---|---|
|`/doc/`|Directory Listing|
|`/icons/`|Directory Listing|
|`/test/`|Directory Listing|
|`/test/testoutput/`|Directory Listing|
|`ESAPI_logging_file_test`|Plik pusty, HTTP 200|
|`/phpinfo.php`|Ujawnienie informacji o PHP|
|`/phpMyAdmin/`|Dostępny panel logowania|
|`/tikiwiki/`|Błąd połączenia z bazą i ujawnienie szczegółów technicznych|

### **Krok 17 – sprawdzamy stronę instalacyjną TikiWiki**
Nie będziemy jej uruchamiać ani niczego instalować. Chcemy jedynie sprawdzić, czy serwer udostępnia ten zasób.

W Kali wykonaj:

```
curl -s -o /dev/null -w "HTTP Status: %{http_code}\nContent-Type: %{content_type}\nSize: %{size_download} bytes\n" http://192.168.56.104/tikiwiki/tiki-install.php
```

### **Krok 17 – analiza**
Strona instalacyjna dostępna
|Parametr|Wynik|
|---|---|
|Adres|`/tikiwiki/tiki-install.php`|
|HTTP Status|`200 OK`|
|Content-Type|`text/html`|
|Rozmiar|3651 bajtów|
W połączeniu z poprzednim wynikiem wiemy już, że:

- TikiWiki nie może połączyć się z bazą danych.
- Aplikacja ujawnia szczegóły błędu.  
- Strona instalacyjna pozostaje dostępna.
    
**Potencjalne ryzyko:** pozostawienie dostępnego instalatora może być niebezpieczne, jeśli umożliwia ponowną konfigurację aplikacji lub zmianę jej ustawień. Sam status HTTP 200 nie potwierdza jednak, że takie operacje są możliwe.
Nie klikamy instalatora i nie przesyłamy żadnych formularzy.

### **Krok 17.1 – identyfikujemy zawartość strony instalacyjnej**

Chcę sprawdzić, czy strona faktycznie wyświetla formularz instalacyjny, czy tylko komunikat informacyjny.

W Kali wykonaj:

```
curl -s http://192.168.56.104/tikiwiki/tiki-install.php | grep -iE '<title>|install|database|password|form'
```

### **Krok 17 – analiza techniczna**

Formularz instalacyjny potwierdzony
Z odpowiedzi wyciągamy następujące informacje:

|Element|Ustalenie|
|---|---|
|Aplikacja|TikiWiki|
|Wersja|1.9.5|
|Biblioteka DB|ADOdb|
|Sterownik|MySQL|
|Ścieżka błędu|`/var/www/tikiwiki/lib/adodb/drivers/adodb-mysql.inc.php`|
|Linia błędu|340|
|Konto DB|`root`|
|Host DB|`localhost`|
|Instalator|Dostępny publicznie|
|Formularz|Przyjmuje parametry połączenia z bazą|

### **Dlaczego to jest poważniejsze?**
Zwróć uwagę na trzy rzeczy:
1. **Ujawnienie ścieżek systemowych** – poznaliśmy strukturę katalogów aplikacji na serwerze.
2. **Ujawnienie wersji** – TikiWiki 1.9.5.
3. **Dostępny formularz instalacyjny** – aplikacja oczekuje danych połączenia z bazą i informuje, że nie może jej znaleźć.

To już nie jest wyłącznie informacja o błędzie. Mamy potencjalnie niebezpieczną konfigurację pozostawionego instalatora.
Nie wypełniamy formularza, nie klikamy `reload` i nie próbujemy konfigurować bazy. Pozostajemy przy rekonesansie.

### **Aktualizacja naszego rejestru**
TikiWiki otrzymuje trzy osobne obserwacje:

- Information Disclosure – ścieżki systemowe i szczegóły błędu MySQL.
- Version Disclosure – TikiWiki 1.9.5.
- Exposed Installation Interface – publicznie dostępny formularz instalacyjny.

Nie oznaczamy jeszcze żadnej z nich jako potwierdzonego przejęcia ani dostępu do bazy.

### **Krok 18 – zatrzymujemy się na TikiWiki**

Moim zdaniem zebraliśmy już wystarczająco dużo informacji o tym zasobie. Nie ma potrzeby ingerować w instalator.

Następnie proponuję sprawdzić `/phpinfo.php`, ale tym razem pod kątem tego, jakie szczegóły środowiska PHP są publicznie ujawniane. To pozwoli nam zamknąć rekonesans serwera HTTP i przygotować porządny raport.

**Na razie nie wykonuj kolejnego polecenia.** Najpierw zamykamy analizę TikiWiki: mamy potwierdzony błąd konfiguracji, wersję aplikacji i dostępny instalator.


Poniżej zapisuję podsumowanie, żeby jutro można było płynnie kontynuować dokładnie od tego miejsca.

# **Raport z ćwiczenia – rekonesans HTTP**

Ćwiczenie zakończone na dziś

13 listopada 2026

## **1. Środowisko laboratoryjne**

Pracowaliśmy w VirtualBox, w odizolowanym środowisku laboratoryjnym.

|Maszyna|Adres IP|Stan|
|---|---|---|
|Kali Linux|`192.168.56.103`|Uruchomiona|
|Metasploitable 2|`192.168.56.104`|Uruchomiona|
|DC01 – AD|—|Wyłączona|
|WIN11-CLIENT|—|Wyłączona|
|WEB01 – Juice Shop|`192.168.56.107`|Wyłączona|

Cel: rekonesans usług HTTP na Metasploitable 2, bez modyfikowania zasobów.

## **2. Przeprowadzone działania**

### **A. Weryfikacja katalogów i plików**

Sprawdziliśmy następujące zasoby:

|Zasób|Wynik|Wnioski|
|---|---|---|
|`/doc/`|HTTP 200, listing|Publiczne ujawnianie dokumentacji pakietów|
|`/icons/`|HTTP 200, listing|Publiczny spis plików ikon|
|`/icons/README`|Dostępny|Dokumentacja zestawu ikon, bez danych poufnych|
|`/test/`|HTTP 200, listing|Publiczny spis katalogu testowego|
|`/test/testoutput/`|HTTP 200, listing|Ujawniona zawartość podkatalogu|
|`ESAPI_logging_file_test`|HTTP 200, 0 bajtów|Plik pusty, dostępny anonimowo|

Ważny wniosek: potwierdziliśmy działanie Directory Listing w trzech katalogach: `/doc/`, `/icons/` i `/test/`.

### **B. Analiza phpMyAdmin**

Zbadaliśmy:

`http://192.168.56.104/phpMyAdmin/`

Potwierdziliśmy:

- panel phpMyAdmin jest dostępny;
    
- wyświetla rzeczywisty formularz logowania;
    
- formularz wykorzystuje metodę POST;
    
- panel jest dostępny przez nieszyfrowane HTTP;
    
- próby identyfikacji wersji na podstawie strony logowania nie przyniosły rezultatu.
    

Wersja phpMyAdmin pozostaje nieustalona.

Nie wykonywaliśmy prób logowania ani testów haseł.

### **C. Analiza TikiWiki**

To najciekawszy fragment dzisiejszego ćwiczenia.

Sprawdziliśmy:

`http://192.168.56.104/tikiwiki/`

Serwer zwrócił:

- HTTP 200;
    
- komunikat `TikiWiki is not properly set up`;
    
- błąd połączenia z bazą danych;
    
- `Access denied for user 'root'@'localhost'`.
    

Następnie sprawdziliśmy instalator:

`http://192.168.56.104/tikiwiki/tiki-install.php`

Potwierdziliśmy:

Wersja i formularz potwierdzone

|Element|Wynik|
|---|---|
|Aplikacja|TikiWiki|
|Wersja|1.9.5|
|Biblioteka|ADOdb|
|Sterownik|MySQL|
|Konto bazy|root|
|Host bazy|localhost|
|Instalator|Publicznie dostępny|
|Formularz konfiguracji|Obecny|

Dodatkowo serwer ujawnił ścieżkę:

`/var/www/tikiwiki/lib/adodb/drivers/adodb-mysql.inc.php`

oraz numer linii 340, w której wystąpił błąd.

**Ocena:** mamy potwierdzone ujawnianie informacji technicznych oraz publicznie dostępny interfejs instalacyjny. Nie potwierdziliśmy możliwości zmiany konfiguracji ani dostępu do bazy danych.

## **3. Zbiorczy rejestr znalezisk**

|Nr|Znalezisko|Status|
|---|---|---|
|1|Directory Listing `/doc/`|Potwierdzone|
|2|Directory Listing `/icons/`|Potwierdzone|
|3|Directory Listing `/test/`|Potwierdzone|
|4|Directory Listing `/test/testoutput/`|Potwierdzone|
|5|Publiczny `phpinfo.php`|Potwierdzone|
|6|Publiczny panel phpMyAdmin|Potwierdzone|
|7|Błędy ujawniające informacje TikiWiki|Potwierdzone|
|8|TikiWiki 1.9.5|Potwierdzone|
|9|Publiczny instalator TikiWiki|Potwierdzone|
|10|Dostęp do bazy danych|Niepotwierdzony|

## **4. Czego się dzisiaj nauczyliśmy?**

Najważniejsze umiejętności praktyczne:

1. Weryfikowanie wyników Nmap za pomocą `curl`.
    
2. Rozpoznawanie Directory Listing.
    
3. Identyfikowanie formularzy logowania i instalacyjnych.
    
4. Analizowanie nagłówków HTTP i odpowiedzi serwera.
    
5. Rozpoznawanie Information Disclosure.
    
6. Odróżnianie potwierdzonego znaleziska od potencjalnej podatności.
    
7. Dokumentowanie dowodów bez ingerowania w system.
    

To bardzo ważna umiejętność: **skaner wskazuje kierunek, ale analityk musi samodzielnie potwierdzić i zinterpretować wynik.**

## **5. Plan na jutro**

Zachowujemy dotychczasową kolejność i nie dodajemy nowych maszyn.

**Następna sesja – dokończenie rekonesansu HTTP**

1. **Analiza** `phpinfo.php`
    
    Sprawdzimy, jakie informacje o PHP i konfiguracji serwera są publicznie dostępne.
    
2. **Ocena całego serwera HTTP**
    
    Zbierzemy ustalenia dotyczące Apache, PHP, katalogów i aplikacji.
    
3. **Raport końcowy**
    
    Przygotujemy uporządkowany raport z dowodami, ryzykiem i rekomendacjami naprawczymi.
    
4. **Decyzja o kolejnym ćwiczeniu**
    
    Po zamknięciu HTTP wybierzemy następny obszar praktyki.
    

### **6. Punkt wznowienia**

Jutro zaczynamy dokładnie od:

```
Krok 19 – analiza phpinfo.php
Cel: rozpoznanie informacji ujawnianych przez konfigurację PHP.

Kali Linux:        192.168.56.103
Metasploitable 2:  192.168.56.104

Obie maszyny uruchomione.
Pozostałe maszyny wyłączone.
```

Na dziś nie wykonujemy już żadnych poleceń.

**Moja ocena dzisiejszej sesji:** bardzo dobra praca. Zaczynamy już przechodzić od prostego skanowania do rzeczywistej analizy bezpieczeństwa aplikacji i serwera. Właśnie tak powinien wyglądać trening w naszym homelabie — spokojnie, metodycznie i z rozumieniem każdego wyniku.

# RAPORT Z REKONESANSU HTTP I ANALIZY ZASOBÓW WEB

**Cel testu:** Metasploitable 2 (`192.168.56.104`)

**Data:** 2026-02-17

**Audytor:** Mat

**Zakres:** Rekonesans usług webowych, identyfikacja ujawniania informacji (Information Disclosure) oraz podatnych punktów wejścia.

## 1. Streszczenie Zarządcze (Executive Summary)

Przeprowadzony rekonesans HTTP wykazał szereg poważnych błędów konfiguracyjnych na docelowym serwerze. Do najważniejszych należą **publiczny listing katalogów (Directory Listing)**, ekspozycja poufnych informacji o konfiguracji PHP (`phpinfo.php`), niezabezpieczony panel administracyjny **phpMyAdmin** oraz publicznie dostępny instalator przestarzałego systemu CMS (**TikiWiki 1.9.5**). Znalezione luki pozwalają potencjalnemu atakującemu na pełne rozeznanie w architekturze serwera oraz ułatwiają dalsze próby eskalacji uprawnień lub kompromitacji aplikacji.

## 2. Metodologia i Ograniczenia

Testy przeprowadzono w kontrolowanym środowisku laboratoryjnym przy użyciu bezpiecznych metod pasywnego i aktywnego rekonesansu (narzędzia: `curl`, analiza nagłówków HTTP, weryfikacja manualna). W trakcie sesji **nie przeprowadzano** prób przełamywania haseł (brute-force) ani destrukcyjnych ataków na aplikacje.

## 3. Szczegółowe Wyniki i Dowody (Detailed Findings)

### 3.1. Directory Listing w kluczowych katalogach

- **Opis:** Serwer WWW zezwala na przeglądanie zawartości katalogów (indeksowanie), co ujawnia strukturę plików i dokumentację pakietów.
    
- **Potwierdzone ścieżki:**
    
    - `/doc/` (Dokumentacja pakietów systemowych)
        
    - `/icons/` (Zestaw ikon serwera)
        
    - `/test/` oraz `/test/testoutput/` (Katalogi testowe i ścieżki wyjściowe skryptów)
        
- **Ryzyko:** Niskie / Średnie (Ujawnianie struktury wewnętrznej aplikacji).
    

### 3.2. Publicznie dostępny panel phpMyAdmin oraz phpinfo.php

- **Opis:** Zidentyfikowano aktywny panel zarządzania bazą danych MySQL (`/phpMyAdmin/`) oraz skrypt diagnostyczny `phpinfo.php`.
    
- **Dowód:** Zapytanie `curl` zwróciło `HTTP Status: 200` oraz poprawne nagłówki HTML dla formularza logowania phpMyAdmin.
    
- **Ryzyko:** Średnie (Ułatwia przeprowadzenie ataku słownikowego na bazy danych oraz identyfikację wersji oprogramowania).
    

### 3.3. Ekspozycja TikiWiki 1.9.5 i instalatora

- **Opis:** Aplikacja TikiWiki w przestarzałej wersji 1.9.5 jest niepoprawnie skonfigurowana, co powoduje błąd połączenia z bazą danych (`Access denied for user 'root'@'localhost'`) połączony z pełnym ujawnieniem ścieżki systemowej (`/var/www/tikiwiki/lib/adodb/...`). Dodatkowo dostępny jest skrypt instalacyjny `tiki-install.php`.
    
- **Ryzyko:** Wysokie (Ujawnianie ścieżek systemowych, wersjonowania oprogramowania oraz potencjalna możliwość ingerencji w instalację aplikacji).
    

## 4. Zbiorczy Rejestr Znalezisk (Risk Matrix)

|**Nr**|**Znalezisko**|**Kategoria**|**Status**|**Poziom Ryzyka**|
|---|---|---|---|---|
|1|Directory Listing (`/doc/`, `/icons/`, `/test/`)|Information Disclosure|Potwierdzone|Niskie|
|2|Publiczny plik `phpinfo.php`|Information Disclosure|Potwierdzone|Średnie|
|3|Publiczny panel `phpMyAdmin`|Attack Surface|Potwierdzone|Średnie|
|4|Błędy ujawniające ścieżki (TikiWiki)|Information Disclosure|Potwierdzone|Wysokie|
|5|Przestarzała wersja TikiWiki 1.9.5|Outdated Software|Potwierdzone|Wysokie|
|6|Publiczny instalator TikiWiki (`tiki-install.php`)|Misconfiguration|Potwierdzone|Wysokie|

## 5. Rekomendacje Naprawcze (Remediation)

1. **Wyłączenie Directory Listing:** W konfikuracji serwera Apache (np. plik `httpd.conf` lub `.htaccess`) należy usunąć opcję `Indexes` dla dyrektywy `Options` (`Options -Indexes`).
    
2. **Usunięcie plików diagnostycznych i instalatorów:** Usunąć z serwera produkcyjnego pliki takie jak `phpinfo.php` oraz skrypty instalacyjne (`tiki-install.php`).
    
3. **Zabezpieczenie phpMyAdmin:** Ograniczyć dostęp do panelu administracyjnego wyłącznie z zaufanych adresów IP (np. poprzez reguły `Allow/Deny` w Apache) lub zabezpieczyć dodatkowym uwierzytelnianiem (HTTP Basic Auth).
    
4. **Aktualizacja oprogramowania:** Przeprowadzić aktualizację przestarzałych aplikacji CMS (TikiWiki) do wspieranych, bezpiecznych wersji.



### Port 80 – otwarty

```
PORT   STATE SERVICE
80/tcp open  http

http-methods:
Supported Methods: GET HEAD POST OPTIONS
```

|Metoda|Znaczenie|Ocena|
|---|---|---|
|GET|Pobieranie zasobów|Standardowa|
|HEAD|Pobieranie nagłówków|Standardowa|
|POST|Przesyłanie danych do aplikacji|Standardowa|
|OPTIONS|Informacja o metodach|Standardowa|
|PUT|Nie wykryto|Pozytywny sygnał|
|DELETE|Nie wykryto|Pozytywny sygnał|

**Ważne:** brak PUT i DELETE na liście nie oznacza jeszcze, że WebDAV jest całkowicie niedostępny. Nmap wykrywa metody deklarowane przez serwer w badanym kontekście. Poszczególne ścieżki mogą mieć inne konfiguracje.

## **2. Co już wiemy o Metasploitable 2?**

Zebraliśmy następujące informacje:

|Obszar|Ustalenia|
|---|---|
|System|Linux, kernel 2.6.24|
|Architektura|i686, 32-bit|
|WWW|Apache 2.2.8|
|PHP|5.2.4|
|WebDAV|DAV/2|
|Port HTTP|80/tcp|
|Metody HTTP|GET, HEAD, POST, OPTIONS|
|Aplikacje|TWiki, phpMyAdmin, Mutillidae, DVWA|

To już całkiem przyzwoity materiał do dokumentacji rekonesansu HTTP.

## **3. Następne ćwiczenie – sprawdzamy katalogi i zasoby**
Teraz chcę, żebyśmy sprawdzili, jakie dodatkowe katalogi i pliki serwer udostępnia.
W Kali wykonaj:

```
gobuster dir -u http://192.168.56.104/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,html
```

Co robi polecenie?

- `gobuster dir` – enumeracja katalogów i plików.
- `-u` – adres badanego serwera.
- `-w` – lista potencjalnych nazw.
- `-x` – dodatkowe rozszerzenia plików.
    
To ćwiczenie wykonujemy wyłącznie na naszym lokalnym Metasploitable 2.

Bardzo dobry wynik. Zakończyliśmy pełne skanowanie listą `common.txt` – 18 452 wpisy sprawdzone. Co ważne, Gobuster znalazł kilka zasobów, które zasługują na osobną analizę.

Przejdźmy przez nie jak podczas rzeczywistego audytu.
## **1. Analiza wyników Gobuster**

Podzielmy znaleziska według znaczenia.
### **A. Najważniejsze znaleziska**
**phpinfo.php**
Wysoki priorytet
HTTP 200 · 48 026 bajtów

Ujawnia szczegółowe informacje o konfiguracji PHP, modułach, zmiennych środowiskowych i ustawieniach serwera.

**/dav/**    Do weryfikacji
HTTP 301    Katalog WebDAV. Warto sprawdzić jego dostępność i konfigurację.

**/test/**     Do weryfikacji
HTTP 301    Dodatkowy katalog, którego zawartość warto rozpoznać.

**/server-status**  Do weryfikacji
HTTP 403 Endpoint statusowy Apache. Dostęp zabroniony, ale sama jego obecność jest informacją o konfiguracji.

### **B. Pozostałe znaleziska**

|Zasób|Status|Interpretacja|
|---|---|---|
|`.htaccess`|403|Dostęp zabroniony|
|`.htpasswd`|403|Dostęp zabroniony|
|`.hta`|403|Dostęp zabroniony|
|`/cgi-bin/`|403|Katalog CGI istnieje lub jest blokowany|
|`/phpMyAdmin/`|301|Przekierowanie do katalogu|
|`/twiki/`|301|Przekierowanie do katalogu|
|`/index.php`|200|Strona główna|

**Ważne:** kod 403 nie potwierdza, że znaleziony plik rzeczywiście istnieje. Oznacza, że serwer odmówił dostępu do wskazanej ścieżki.

## **2. Najważniejsze znalezisko: phpinfo.php**

To będzie nasz następny punkt analizy.

W Kali wykonaj:

```
curl -s http://192.168.56.104/phpinfo.php -o phpinfo.html
```

Następnie:

```
grep -Ei "PHP Version|System|Server API|Loaded Configuration File|DOCUMENT_ROOT|SERVER_SOFTWARE|allow_url_include|allow_url_fopen|display_errors|expose_php" phpinfo.html
```

Co chcemy ustalić?

- wersję PHP;
    
- ścieżkę konfiguracji PHP;
    
- informacje o serwerze;
    
- ustawienia bezpieczeństwa PHP;
    
- potencjalnie niebezpieczne konfiguracje.
    

## **3. Nasz dotychczasowy postęp**

**HTTP Recon – Metasploitable 2**

Postęp

1. Rozpoznanie systemu i kernela
    
2. Rozpoznanie Apache i PHP
    
3. Sprawdzenie nagłówków HTTP
    
4. Sprawdzenie metod HTTP
    
5. Enumeracja katalogów Gobuster
    
6. Analiza phpinfo.php – następny krok
    

Moja rekomendacja: nie przechodźmy jeszcze do exploitów. Najpierw zbierzmy i udokumentujmy konfigurację PHP.

**Wykonaj dwa polecenia i wklej wynik.** Przeanalizujemy go razem, linijka po linijce.


Bardzo dobrze. To jeden z ciekawszych wyników naszego dotychczasowego rekonesansu. `phpinfo.php` ujawnił nam nie tylko wersję PHP, ale również ścieżki systemowe i ustawienia konfiguracyjne.

Przeanalizujmy to dokładnie.

## **1. Analiza konfiguracji PHP**

Istotne ujawnienie informacji

|Parametr|Wartość|Znaczenie|
|---|---|---|
|PHP Version|5.2.4|Bardzo stara wersja PHP|
|System|Linux 2.6.24|Kernel systemu|
|Architecture|i686|System 32-bitowy|
|Server API|CGI/FastCGI|Sposób obsługi PHP|
|php.ini|`/etc/php5/cgi/php.ini`|Lokalizacja konfiguracji|
|DOCUMENT_ROOT|`/var/www/`|Główny katalog WWW|
|SERVER_SOFTWARE|Apache 2.2.8|Serwer WWW|

Szczególnie istotne są teraz ustawienia PHP.

## **2. Ocena ustawień bezpieczeństwa**

|Ustawienie|Wartość|Ocena|
|---|---|---|
|`allow_url_fopen`|On|Wymaga analizy użycia|
|`allow_url_include`|Off|Korzystniejsze ustawienie|
|`display_errors`|On|Ryzyko ujawniania informacji|
|`expose_php`|On|Ujawnianie wersji PHP|

Kilka ważnych wyjaśnień:

**allow****_****url****_****fopen = On**

Pozwala funkcjom obsługującym strumienie plików korzystać z adresów URL. Samo włączenie tej opcji nie oznacza podatności.

**allow****_****url****_****include = Off**

Dobrze. Ogranicza możliwość dołączania zdalnych zasobów przez mechanizmy include/require obsługujące URL.

**display****_****errors = On**

To ustawienie może ujawniać szczegóły aplikacji, ścieżki plików i informacje o błędach użytkownikom.

**expose****_****php = On**

PHP ujawnia swoją obecność i wersję, co ułatwia identyfikację technologii przez osobę prowadzącą rekonesans.

## **3. Najważniejsze odkrycie**

**Serwer ujawnia ścieżki wewnętrzne**

# **/var/www/**

DOCUMENT_ROOT

## **/etc/php5/cgi/php.ini**

Loaded Configuration File
To informacje, które mogą być przydatne przy dalszym analizowaniu błędów aplikacji i konfiguracji serwera.

## **4. Następny krok – sprawdzamy katalog WebDAV**
Wcześniej znaleźliśmy `/dav/`, a serwer ujawnia `DAV/2`.
Teraz sprawdzimy odpowiedź tego konkretnego katalogu:

```
curl -i -X OPTIONS http://192.168.56.104/dav/
```
Następnie:

```
curl -i -X PROPFIND http://192.168.56.104/dav/ -H "Depth: 1"
```
Drugie polecenie wykonuje zapytanie WebDAV o właściwości katalogu i jego bezpośrednią zawartość. Jest to metoda odczytowa.

Nie próbujemy jeszcze zapisywać ani usuwać plików.

## **5. Aktualny stan naszego rekonesansu**

- Identyfikacja systemu operacyjnego.
- Identyfikacja Apache i PHP.
- Analiza nagłówków HTTP.
- Rozpoznanie metod HTTP.
- Enumeracja katalogów Gobuster.
- Analiza phpinfo.php.
- Analiza konfiguracji WebDAV.
- Podsumowanie podatności i ryzyk HTTP.
    

**Wklej wyniki obu poleceń.** WebDAV może być interesującym elementem tego serwera, dlatego warto go dokładnie rozpoznać przed zakończeniem etapu HTTP Recon.


Świetnie! To jest bardzo ważne odkrycie w naszym laboratorium. Właśnie znaleźliśmy coś, czego nie wykazało wcześniejsze skanowanie Nmap.
**Katalog główny** `/` **i katalog** `/dav/` **mają różne zestawy obsługiwanych metod HTTP.**

To doskonały przykład, dlaczego pentester nie powinien ograniczać się do jednego skanowania całego serwera.
## **1. Analiza OPTIONS – WebDAV**
Otrzymaliśmy:
```
HTTP/1.1 200 OK
DAV: 1,2
MS-Author-Via: DAV
Allow: OPTIONS,GET,HEAD,POST,DELETE,TRACE,PROPFIND,PROPPATCH,COPY,MOVE,LOCK,UNLOCK
```

Najważniejsze informacje:

|Metoda|Znaczenie|Ocena|
|---|---|---|
|GET|Pobieranie zasobów|Standardowa|
|HEAD|Pobieranie nagłówków|Standardowa|
|OPTIONS|Informacje o metodach|Standardowa|
|POST|Przesyłanie danych|Standardowa|
|PROPFIND|Odczyt właściwości zasobów|WebDAV|
|PROPPATCH|Modyfikowanie właściwości|WebDAV|
|COPY|Kopiowanie zasobów|WebDAV|
|MOVE|Przenoszenie zasobów|WebDAV|
|DELETE|Usuwanie zasobów|WebDAV|
|LOCK|Blokowanie zasobów|WebDAV|
|UNLOCK|Zdejmowanie blokady|WebDAV|
|TRACE|Diagnostyczna metoda HTTP|Wymaga oceny|

Istotne

**DELETE, COPY, MOVE i PROPPATCH**
Serwer deklaruje obsługę operacji modyfikujących zasoby.
Nie oznacza to jednak, że każdy użytkownik może je wykonywać. Musimy osobno sprawdzić uprawnienia.

## **2. Analiza PROPFIND**
Drugi wynik:
```
HTTP/1.1 207 Multi-Status
```
To prawidłowa odpowiedź WebDAV.

Co udało nam się ustalić?
|Parametr|Wynik|Znaczenie|
|---|---|---|
|href|`/dav/`|Badany katalog|
|resourcetype|collection|Katalog|
|creationdate|2012-05-20|Data utworzenia|
|getlastmodified|20.05.2012|Ostatnia modyfikacja|
|supportedlock|exclusive/shared|Obsługa blokowania|
|getcontenttype|httpd/unix-directory|Katalog systemowy|

### **Co oznacza 207 Multi-Status?**
WebDAV wykorzystuje odpowiedź 207 do przekazywania informacji o wielu właściwościach zasobu w formacie XML.
W naszym przypadku serwer ujawnił właściwości katalogu `/dav/`.
Zwróć uwagę na jeszcze jedną rzecz: `PROPFIND` nie ujawnił żadnych plików wewnątrz katalogu. Pokazał jedynie sam katalog.

## **3. Najważniejsze odkrycie z całego ćwiczenia**
**Porównanie dwóch punktów końcowych**
**Katalog główny** `/`
Ograniczony zestaw metod
`GET HEAD POST OPTIONS`
**Katalog** `/dav/`
Rozszerzony zestaw metod
`GET HEAD POST OPTIONS PROPFIND PROPPATCH COPY MOVE DELETE LOCK UNLOCK TRACE`

Wyniki pochodzą z dwóch różnych ścieżek HTTP. Nie należy traktować ich jako jednej globalnej konfiguracji serwera.
To pokazuje, że enumeracja powinna być wykonywana również na poziomie poszczególnych katalogów.
## **4. Następny krok – sprawdzamy dostępność WebDAV bez zapisu**

Chciałbym teraz sprawdzić, czy katalog `/dav/` pozwala anonimowo odczytywać swoje właściwości i czy istnieje w nim zawartość.

Wykonaj:

```
curl -i -X PROPFIND http://192.168.56.104/dav/ \
-H "Depth: 1" \
-u anonymous:
```

Uwaga: to zapytanie nie wykonuje zapisu ani usuwania. Sprawdzimy jedynie odpowiedź serwera dla jawnie podanego użytkownika `anonymous`.
Porównamy ją z poprzednim wynikiem bez uwierzytelnienia.

## **5. Aktualizacja naszego dziennika pentesterskiego**

HTTP Recon – kolejny etap wykonany

|Etap|Status|
|---|---|
|Rozpoznanie systemu i kernela|Wykonany|
|Apache i PHP|Wykonany|
|Nagłówki HTTP|Wykonany|
|Metody HTTP na `/`|Wykonany|
|Gobuster|Wykonany|
|phpinfo.php|Wykonany|
|WebDAV OPTIONS|Wykonany|
|WebDAV PROPFIND|Wykonany|
|Weryfikacja dostępu anonimowego|W toku|

**Moja uwaga:** nie spieszymy się z exploitami. To, co właśnie robimy, to prawdziwa enumeracja usług i kontrola konfiguracji. Umiejętność wyciągania wniosków z takich wyników jest znacznie ważniejsza niż samo uruchamianie gotowych narzędzi.


### **Wniosek**

Katalog WebDAV udostępnia swoje właściwości bez uwierzytelnienia.
Jednak ważne zastrzeżenie: parametr `-u anonymous:` wysyła dane uwierzytelniające dla użytkownika `anonymous`. Nie jest to dokładnie to samo co całkowity brak nagłówka Authorization.

Na podstawie tych wyników możemy potwierdzić anonimowy odczyt właściwości katalogu, ale nie możliwość zapisywania lub usuwania plików.

## **2. Co zapisujemy w dokumentacji?**

**Finding: WebDAV – dostęp do właściwości bez uwierzytelnienia**

Potencjalne ryzyko informacyjne
- Endpoint: `http://192.168.56.104/dav/`
- Serwer: Apache 2.2.8
- Protokół: WebDAV
- Odpowiedź: HTTP 207 Multi-Status
- Dostęp: właściwości katalogu dostępne bez uwierzytelnienia
- Modyfikacja zasobów: jeszcze niezweryfikowana

**Rekomendacja:** ograniczyć dostęp do WebDAV i wyłączyć niepotrzebne metody.

## **3. Następny krok – sprawdzamy, czy katalog zawiera pliki**

Wykonajmy teraz zapytanie PROPFIND z głębokością `1`, ale bez uwierzytelnienia, i sprawdźmy dokładnie odpowiedź:

```
curl -s -X PROPFIND \
http://192.168.56.104/dav/ \
-H "Depth: 1" | xmllint --format -
```

To polecenie jedynie porządkuje odpowiedź XML, aby łatwiej było ją odczytać.

Jeżeli ponownie zobaczymy tylko `/dav/`, będziemy wiedzieli, że serwer nie zwrócił żadnych bezpośrednich elementów tego katalogu.

**Mała uwaga metodyczna:** nie testujemy jeszcze DELETE, PUT ani MOVE. Najpierw kończymy rozpoznanie i dokumentujemy dostęp. Potem ocenimy, czy warto przeprowadzić kontrolowany test zapisu w naszym laboratorium.

## **1. Analiza ostatniego wyniku**
Najważniejszy fragment:

```
<D:href>/dav/</D:href>
<D:resourcetype>
    <D:collection/>
</D:resourcetype>
```
Oznacza to:

- `/dav/` jest kolekcją WebDAV, czyli katalogiem.
- Serwer zwraca jego właściwości. 
- Nie zwrócił żadnych dodatkowych zasobów bezpośrednio wewnątrz katalogu.
- `Depth: 1` oznacza żądanie informacji o katalogu i jego bezpośrednich elementach.

**Wniosek:** w odpowiedzi nie ma widocznych plików ani podkatalogów. Nie oznacza to jednak, że fizyczny katalog na serwerze jest pusty w każdych okolicznościach.

## **2. Podsumowanie WebDAV**

## **WebDAV – 192.168.56.104/dav/**
Status usługi  Aktywna

Dostęp do PROPFIND  Potwierdzony

Dostęp do właściwości bez logowania  Potwierdzony

Widoczne pliki  Nie wykazano

Możliwość zapisu  Niezweryfikowana

Możliwość usuwania  Niezweryfikowana

## **3. Co dalej? Kontrolowany test zapisu**

Mamy dwie możliwości, ale proponuję wykonać teraz test zapisu do WebDAV.
W naszym laboratorium możemy sprawdzić, czy anonimowy użytkownik jest w stanie przesłać plik testowy.
Będzie to ważne, ponieważ samo występowanie metody `PUT` w nagłówku `Allow` nie dowodzi, że zapis jest rzeczywiście dozwolony.

Test przeprowadzimy bezpiecznie:

- utworzymy nieszkodliwy plik tekstowy;
    
- spróbujemy przesłać go do `/dav/`;
    
- sprawdzimy odpowiedź HTTP;
    
- jeżeli zapis się powiedzie, usuniemy wyłącznie nasz plik testowy.
    

Nie będziemy modyfikować istniejących zasobów.

**Zanim przejdziemy dalej, ważny wniosek:** dotychczasowy rekonesans wykazał, że `/dav/` ma znacznie szerszy zestaw metod HTTP niż katalog główny. To jeden z najciekawszych wyników całego naszego HTTP Recon na Metasploitable 2.