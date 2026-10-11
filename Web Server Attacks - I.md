Zanim zaczniesz enumerować katalogi lub testować dane wejściowe, musisz wiedzieć, z czym masz do czynienia. Oprogramowanie serwera WWW samo w sobie decyduje, jakie błędy w konfiguracji są możliwe, które ścieżki warto sprawdzić i które narzędzia będą najskuteczniejsze. Identyfikacja serwera to nie formalność. Ma ona bezpośredni wpływ na każdą późniejszą decyzję.

Dobra wiadomość jest taka, że ​​większość serwerów WWW sama się ogłasza. Programiści i administratorzy często pozostawiają domyślne konfiguracje, które zazwyczaj zawierają zbyt wiele informacji o wersji. Jest kilka wiarygodnych źródeł informacji, których warto poszukać.

## Nagłówek odpowiedzi serwera

Najbardziej bezpośrednim sygnałem odcisku palca jest `Server`nagłówek w odpowiedzi HTTP. Gdy wysyłasz dowolne żądanie do serwera WWW, serwer uwzględnia ten nagłówek w swojej odpowiedzi. Różne oprogramowania serwerowe formatują go inaczej, a formaty te są na tyle spójne, że można ich używać jako identyfikatorów dodatnich.

Uruchom `curl`z `-I`flagą żądającą wyłącznie nagłówków, a nie treści odpowiedzi:

```bash
# -s suppresses the progress bar
# -I sends a HEAD request, returning only response headers
curl -sI http://MACHINE_IP:80
```

Powinieneś zobaczyć dane wyjściowe podobne do poniższego dla serwera Apache działającego na porcie 80:

Terminal

```shell-session
ubuntu@tryhackme-2404:~$ curl -sI http://MACHINE_IP:80
HTTP/1.1 200 OK
Date: Wed, 08 Apr 2026 13:59:00 GMT
Server: Apache/2.4.58 (Ubuntu)
Last-Modified: Fri, 03 Apr 2026 18:12:44 GMT
ETag: "29af-64e9243796aa2"
Accept-Ranges: bytes
Content-Length: 10671
Vary: Accept-Encoding
Content-Type: text/html
```

Nagłówek `Server`zawiera informacje o oprogramowaniu i jego wersji. Nie każdy serwer udostępnia tak wiele szczegółów. Wdrożenie z utwardzoną strukturą może wyświetlać tylko `Apache`nagłówek lub całkowicie go pomijać, ale domyślna konfiguracja na większości serwerów Ubuntu pozostawia te informacje widoczne.

Oto, co domyślnie zwraca każdy serwer w tym laboratorium:

|Port|Serwer|Domyślny nagłówek serwera|
|---|---|---|
|80|Apache2|`Apache/2.4.x (Ubuntu)`|
|8000|Serwer HTTP Pythona|`SimpleHTTP/0.6 Python/3.xx.x`|
|3000|Node.js Express|Brak (ustawiane przez aplikację)|
|8080|Nginx|`nginx/1.xx.x`|

Zauważ, że wpis Node.js Express nie zawiera `Server`nagłówka. Express nie ustawia go domyślnie; warstwa HTTP Node.js również go nie ustawia. Programista musi dodać go jawnie. W prawdziwej aplikacji Express brak nagłówka  `Server`sam w sobie jest sygnałem. Wiarygodnym identyfikatorem Express jest nagłówek `X-Powered-By`, który Express ustawia automatycznie, chyba że programista go usunie.

## Nagłówek X-Powered-By

Niektóre frameworki dodają `X-Powered-By`nagłówek, który ujawnia warstwę aplikacji znajdującą się za serwerem. Express ustawia to domyślnie:

```text
X-Powered-By: Express
```

Ten nagłówek jest niezależny od `Server`nagłówka i dla Express stanowi podstawowy odcisk palca. W przeciwieństwie do Apache'a i Nginx, które ogłaszają się w `Server`nagłówku, Express opiera się na nim `X-Powered-By`jako na swoim identyfikatorze. Sprawdź go na każdym porcie, na którym `Server`go brakuje lub jest ogólny.

## Narzędzia programistyczne przeglądarki

Jeśli pracujesz w przeglądarce, karta **„Sieć”** w Narzędziach programistycznych udostępnia te same informacje nagłówkowe bez żadnych dodatkowych narzędzi. Otwórz `http://MACHINE_IP:3000`przeglądarkę Mozilla Firefox, a następnie kliknij prawym przyciskiem myszy w dowolnym miejscu strony i wybierz **„Inspekcja”** (lub naciśnij klawisz F12), aby uruchomić Narzędzia programistyczne. Przejdź do karty **„Sieć”** i odśwież stronę, aby przechwycić żądania. Wybierz główne żądanie z listy i w sekcji „Nagłówki” wyświetl nagłówki odpowiedzi, aby sprawdzić szczegóły odpowiedzi serwera.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775661823075.png)

## Domyślne strony błędów

Flaga `-sI`wysyła `HEAD`żądanie, które zwraca tylko nagłówki, bez treści. Aby wyświetlić domyślne strony błędów, należy `GET`przełączyć żądanie na `-s`bez `-I`:

```bash
# HEAD request: headers only, no body
curl -sI http://MACHINE_IP:PORT/

# GET request: full response including body
curl -s http://MACHINE_IP:PORT/nonexistent-page-xyz
```

Gdy żądasz ścieżki, która nie istnieje, większość serwerów zwraca domyślną stronę błędu 404. Domyślna strona każdego serwera ma charakterystyczny wygląd. Python to odpowiedź w postaci zwykłego tekstu. Nginx dołącza swoją wersję do stopki HTML. Apache dołącza swoją nazwę do treści strony. Te różnice pozwalają na identyfikację serwera nawet po `Server`wyłączeniu nagłówka. Sprawdź to na wszystkich czterech portach, a zobaczysz, jak różnie każdy serwer radzi sobie z tą samą sytuacją.

**Python** jest dostarczany z wbudowanąHTTPSerwer, który każdy programista może uruchomić jednym poleceniem. Właśnie ta wygoda jest powodem, dla którego pojawia się w testach penetracyjnych.

```bash
# This command serves the current working directory over HTTP on port 8000
python3 -m http.server 8000
```

Programiści używają go do szybkiego udostępniania plików, testowania statycznych witryn internetowych lub przesyłania danych między dwoma komputerami w tej samej sieci. Problem polega na tym, że funkcja „szybkiego udostępniania plików” czasami „przypadkowo udostępnia się w internecie na sześć miesięcy”, działając na serwerach publicznych, wewnętrznych zasobach sieciowych i instancjach chmurowych, gdzie ktoś otworzył port 8000 w zaporze i o nim zapomniał. Serwer nie ma kontroli dostępu, uwierzytelniania ani logów wykraczających poza to, co rejestruje system operacyjny.

## Do czego służy

PythonaHTTPSerwer obsługuje cały katalog roboczy, w tym każdy plik w nim zawarty, w tym pliki typu dotfiles, takie jak `.env`. Nie ma `.htaccess`odpowiednika, listy blokowanych ani pliku konfiguracyjnego. Jeśli plik znajduje się w katalogu, każdy, kto ma dostęp do portu 8000, może go pobrać.

Różni się to od Apache'a czy Nginx, gdzie lista katalogów jest domyślnie wyłączona, a administratorzy mogą ograniczać poszczególne ścieżki. Serwer HTTP Pythona ma jeden tryb: obsługuje wszystko.

## Wpis do katalogu

Jeśli `index.html`w katalogu nie ma żadnego pliku, PythonHTTPSerwer generuje stronę HTML z listą wszystkich plików, które widzi. Przejdź do katalogu głównego serwera za pomocą poniższego polecenia lub bezpośrednio `http://10.129.163.58:8000`w przeglądarce:

```bash
curl -s http://10.129.163.58:8000/
```

Powinieneś zobaczyć listę katalogów HTML z tytułem strony `Directory listing for /`. Wszystkie elementy w tej liście są dostępne bezpośrednio.

## ![Listing katalogów włączony poprzez serwer Python.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775890440403.png)Dostęp do plików Dotfiles

Pliki typu „dotfiles” `.env`są ukryte w standardowej nawigacji po katalogach w systemie Linux, ale serwer HTTP Pythona nie respektuje tej konwencji. Obsługuje je jak każdy inny plik. Plik `.env`jest częstym celem, ponieważ programiści używają go do przechowywania konfiguracji specyficznej dla danego środowiska, a konfiguracja ta często zawiera dane uwierzytelniające:

Terminal

```shell-session
root@attackbox:~# curl -s http://10.129.163.58:8000/.env
SECRET_KEY=dev-secret-key-do-not-use
DATABASE_URL=postgresql://webapp:S3cur3DBPass!@localhost/production
DEBUG=True
```

## Pobieranie i przeglądanie archiwów

Jeśli na liście katalogów widzisz `.zip`, `.tar.gz`lub inne archiwum, pobierz je i sprawdź zawartość. Programiści czasami pozostawiają kopie zapasowe w tym samym katalogu, który obsługują. Archiwa te mogą zawierać kod źródłowy, zrzuty bazy danych lub pliki konfiguracyjne.

Terminal

```shell-session
root@attackbox:~# curl -s http://10.129.163.58:8000/backup.zip -o backup.zip
root@attackbox:~# unzip backup.zip -d backup-contents/
root@attackbox:~# cat backup-contents/db_dump.sql
Archive:  backup.zip
  inflating: backup-contents/db_dump.sql
-- Database dump for staging environment

CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR(50));
INSERT INTO users VALUES (1, 'admin', 'admin@company.com');
INSERT INTO users VALUES (2, 'jsmith', 'jsmith@company.com');

-- End of dump
```

## Dlaczego to ma znaczenie

PytonHTTPSerwer jest realistycznym odkryciem, ponieważ nie wymaga żadnej eksploatacji. Nie ma żadnej luki w zabezpieczeniach, którą można by wyzwolić. Serwer działa dokładnie tak, jak został zaprojektowany. Błędna konfiguracja polega na tym, że serwer działa w miejscu, w którym nie powinien się znajdować, udostępniając pliki, które nie powinny być publiczne. Udokumentowanie tego w rzeczywistym działaniu oznacza wyjaśnienie nie tylko istnienia serwera, ale także tego, co ujawnia i co atakujący mógłby zrobić z tymi informacjami.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Jeśli katalog zawiera `index.html`plik, Python wyświetli ten plik zamiast go wyświetlić.lista katalogowa. Jeśli nie widziszlista katalogowaw katalogu głównym spróbuj bezpośrednio poprosić o ścieżki lub przejść do podkatalogów.

**Apacz** jest najpowszechniej wdrożonym serwerem WWW na świecie, co oznacza, że ​​pojawia się w niemal każdym projekcie związanym z infrastrukturą internetową. Jego domyślna konfiguracja Ubuntu pozostawia kilka rzeczy włączonych, które testerzy regularnie znajdują i zgłaszają. Trzy najpopularniejsze to:lista katalogowana określonych ścieżkach, `server-status`moduły i pliki kopii zapasowych znajdujące się w katalogu głównym dokumentów.

## Ujawnienie wersji

Zacznij od podstaw: sprawdź `Server`nagłówek.

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -SI http://10.129.163.58:80 | grep -i server
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0 10671    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
Server: Apache/2.4.58 (Ubuntu)
```

Apaczw systemie Ubuntu domyślnie jest to `ServerTokens OS`, które obejmujeSystem operacyjnyetykieta obok numeru wersji. Znajomość dokładnej wersji ułatwia sprawdzenie znanych luk CVE i zrozumienie możliwości serwera.

## Wpis do katalogu

Dyrektywa Apache'a `Options +Indexes`nakazuje serwerowi wyświetlanie listy plików, gdy katalog nie ma `index.html`domyślnego pliku o tym samym lub podobnym numerze. Czasami jest to celowo włączane w przypadku wewnętrznych katalogów współdzielonych plików i przypadkowo pozostawiane w ścieżkach zawierających poufne dane.

Przejdź do `http://10.129.163.58/files/`ścieżki:

![Wykaz katalogów na serwerze Apache.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1777558921639.png)

Powinna zostać wyświetlona strona HTML z tytułem „ `Index of /files`”, zawierająca listę plików dostępnych w tym katalogu.Apacz'Slista katalogowaobejmuje nazwy plików, rozmiary plików i daty ostatniej modyfikacji, co daje Ci jasny obraz tego, co się znajduje, zanim zdecydujesz, co odzyskać.

Kiedy znajdzieszlista katalogowa, przeczytaj każdy plik w nim zawarty. Programiści czasami zostawiają eksporty CSV, notatki wewnętrzne lub pliki kopii zapasowych w katalogach, które przeznaczyli wyłącznie do użytku wewnętrznego. Warto sprawdzić każdy z nich.

## Strona mod_status

ApaczZawiera wbudowaną stronę statusu obsługiwaną przez `mod_status`moduł. Po prawidłowej konfiguracji jest dostępna tylko z poziomu localhost. Po nieprawidłowej konfiguracji `Require all granted`jest dostępna z dowolnego adresu IP. Dostęp do niej można uzyskać za pomocą `http://10.129.163.58:80/server-status`, jak pokazano poniżej:

![Odpowiedź strony stanu serwera Apache.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1777558921642.png)Strona statusu pokazuje aktywne połączenia i żądane przez nie ścieżki, całkowitą liczbę żądań obsłużonych od momentu uruchomienia serwera, stany robocze (bezczynność, zapis, odczyt, zamknięcie) oraz wersję serwera i czas jego uruchomienia. Na serwerze produkcyjnym powoduje to wyciek informacji w czasie rzeczywistym o działaniach innych użytkowników i istniejących ścieżkach wewnętrznych. Potwierdza również dokładną wersję serwera w nagłówku strony.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Info:** `mod_status` jest domyślnie włączona w systemie UbuntuApaczPakiet i jest dostarczany z `Require local`ograniczeniem w `conf-available/security.conf`. Jednak `Require all granted`dyrektywa w dowolnym miejscu konfiguracji hosta wirtualnego po cichu pomija to ograniczenie, udostępniając dostęp `/server-status`wszystkim adresom IP bez modyfikowania konfiguracji modułu. Zawsze sprawdzaj, `/server-status`nawet na serwerach, które wydają się korzystać z ustawień domyślnych.

## Znajdowanie niepowiązanych plików za pomocą Gobustera

Nie wszystko, co interesujące, jest dostępne na stronie lub widoczne w katalogu. Pliki kopii zapasowych, stare kopie konfiguracji i zapomniane pliki testowe często znajdują się w katalogu głównym dokumentów bez żadnych linków do nich. Narzędzia takie jak `Gobuster`te, odkrywają je, odgadując ścieżki na podstawie listy słów.

```bash
# -u is the target URL
# -w is the wordlist path
# -x tells gobuster to also append these extensions to each word
gobuster dir -u http://TARGET_IP:80 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -x bak,txt,html -t 20
```

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** SecLists powinny być dostępne na `/usr/share/wordlists/SecLists/` AttackBoxie. Jeśli używasz własnej maszyny wirtualnej Kali i SecLists nie jest zainstalowany, uruchom go, `sudo apt install seclists`aby go pobrać.

**Wskazówka:** Pełna `common.txt`lista słów SecLists jest obszerna. Z `-x`flagą dodającą trzy warianty rozszerzenia na słowo, skanowanie generuje znaczną liczbę żądań i może trwać kilka minut na zdalnym komputerze docelowym. Aby uzyskać szybszy wynik, spróbuj uruchomić skanowanie bez `-x`wcześniejszego wyszukiwania katalogów, a następnie dodaj `-x bak`skanowanie docelowego rozszerzenia.

Terminal

```shell-session
root@ip-10-81-64-63:~# gobuster dir -u http://10.129.163.58:80 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -x bak,txt -t 20
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.163.58
[+] Method:                  GET
[+] Threads:                 20
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              bak,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.bak        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.hta.txt             (Status: 403) [Size: 275]
/.htaccess.bak        (Status: 403) [Size: 275]
/.hta                 (Status: 403) [Size: 275]
/.hta.bak             (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/backup.bak           (Status: 200) [Size: 178]
/files                (Status: 301) [Size: 308] [--> http://10.129.163.58/files/]
/index.html           (Status: 200) [Size: 10671]
/javascript           (Status: 301) [Size: 313] [--> http://10.129.163.58/javascript/]
/server-status        (Status: 200) [Size: 17539]
Progress: 13965 / 13968 (99.98%)
===============================================================
Finished
===============================================================
```

GdyGobusterZnajduje plik z `.bak`rozszerzeniem, które prawie zawsze warto odzyskać. Pliki kopii zapasowych często zawierają fragmenty konfiguracji, dane uwierzytelniające lub kopie kodu źródłowego.

Zwróć również uwagę na `.htpasswd`pliki, jeśli pojawiają się w wynikach. Apache `.htpasswd`przechowuje nazwy użytkowników i zaszyfrowane hasła do uwierzytelniania podstawowego HTTP. Znalezienie dostępnego `.htpasswd`pliku zapewnia skrót uwierzytelniający, który można złamać w trybie offline, i potwierdza, że ​​jakaś część witryny korzysta z uwierzytelniania podstawowego, co wskazuje, na których ścieżkach warto spróbować uwierzytelnić dostęp.

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:80/backup.bak
# Apache config backup - DO NOT COMMIT
ServerName company.internal
DocumentRoot /var/www/html
# DB credentials below
# user: dbadmin pass: Backup2024!
# Last updated: 2024-11-15
```

## Łączenie wszystkiego

Wzór tutaj jest spójny w całymApaczdochodzenia: sprawdź nagłówek wersji, przejrzyj dowolny katalog, który umożliwia wylistowanie, odwiedź `/server-status`i użyjgobusteraby znaleźć niepowiązane pliki. Te cztery kroki obejmują większość problemów związanych z nieprawidłową konfiguracjąApaczserwer ujawni.

**Aplikacje Node.js** zachowują się inaczej niż Apaczi PythonHTTPSerwery. Nie obsługują plików statycznych z skonfigurowanego katalogu głównego dokumentów. Uruchamiają kod aplikacji, a ten kod decyduje, co zwrócić dla każdego żądania. Ta elastyczność jest potężna, ale to właśnie tutaj powstaje wiele błędów.

Atakujący zwracają szczególną uwagę na aplikacje **Node.js Express** , ponieważ programiści często pozostawiają włączone funkcje trybu deweloperskiego podczas wdrażania do produkcji. Punkty końcowe debugowania, rozbudowane odpowiedzi na błędy i ujawnione zmienne środowiskowe – wszystko to wynika z tego samego nawyku: kod, który działał w fazie deweloperskiej, został udostępniony w wersji „tak jak jest”. W rezultacie powstaje aplikacja, która dokładnie informuje o sposobie jej zbudowania, a czasami także o tym, jakich danych uwierzytelniających używa.

## Odciski ramowe

Nagłówki na porcie 3000 potwierdzają, z czym masz do czynienia:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -sI http://10.129.163.58:3000
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: application/json; charset=utf-8
Content-Length: 56
ETag: W/"38-K8iCfm09rMr0MV0NsgqdAb94DAk"
Date: Sat, 11 Apr 2026 07:27:28 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Zobaczysz `X-Powered-By: Express`w odpowiedzi. Express ustawia ten nagłówek automatycznie, chyba że programista wyraźnie go wyłączy. To potwierdza, że ​​masz do czynienia z aplikacją Express i podpowiada, czego szukać dalej.

## Odczyt wersji aplikacji

Ścieżka główna wielu aplikacji Express zwraca odpowiedź statusu JSON:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:3000
{"status":"ok","app":"company-portal","version":"1.2.0"}
```

Jeśli odpowiedź zawiera pole wersji, zanotuj je. Porównanie wersji aplikacji ze znanymi lukami w zabezpieczeniach lub rejestrami zmian może ujawnić przydatne informacje.

## Wyzwalanie błędów szczegółowych

Wbudowany moduł obsługi błędów Express blokuje ślady stosu, gdy `NODE_ENV`jest ustawiony na `production`. W trybie programistycznym przekazuje je. Jednak programiści często piszą własne moduły obsługi błędów, a te niestandardowe moduły udostępniają ślady stosu niezależnie od `NODE_ENV`. W dołączonej maszynie wirtualnej aplikacja internetowa używa niestandardowego modułu obsługi błędów. Szczegółowa odpowiedź JSON, którą widzisz, nie jest częścią działania Express; jest wynikiem kodu aplikacji napisanego do debugowania i nigdy nie jest utwardzany. Oba wzorce występują w rzeczywistych interakcjach: sprawdzenie  `NODE_ENV=production`ma sens tylko wtedy, gdy żaden niestandardowy moduł obsługi błędów go nie nadpisuje. Rozważmy scenariusz, w którym wykonywane jest wywołanie API do serwera Express, jak pokazano poniżej:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:3000/api/users | python3 -m json.tool
{
    "error": "connect ECONNREFUSED 127.0.0.1:5432",
    "stack": "Error: connect ECONNREFUSED 127.0.0.1:5432\n    at /opt/nodeapp/app.js:16:15\n    at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)\n    at next (/opt/nodeapp/node_modules/express/lib/router/route.js:149:13)\n    at Route.dispatch (/opt/nodeapp/node_modules/express/lib/router/route.js:119:3)\n    at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)\n    at /opt/nodeapp/node_modules/express/lib/router/index.js:284:15\n    at Function.process_params (/opt/nodeapp/node_modules/express/lib/router/index.js:346:12)\n    at next (/opt/nodeapp/node_modules/express/lib/router/index.js:280:10)\n    at expressInit (/opt/nodeapp/node_modules/express/lib/middleware/init.js:40:5)\n    at Layer.handle [as handle_request] (/opt/nodeapp/node_modules/express/lib/router/layer.js:95:5)",
    "query": "SELECT * FROM users"
}
```

Warto dokładniej zbadać odpowiedź `500 Internal Server Error`z punktu końcowego API. W trybie programistycznym treść odpowiedzi często zawiera komunikat o błędzie, ślad stosu i kontekst dotyczący tego, co aplikacja próbowała zrobić w momencie wystąpienia błędu. Ślad stosu jest tutaj kluczowym odkryciem, ponieważ ujawnia wewnętrzne ścieżki plików, nazwy modułów, a czasami zapytanie do bazy danych, które wywołało błąd. Każdy z tych szczegółów mówi coś o wewnętrznych mechanizmach aplikacji, czego nie mówi prosty kod statusu.

## Wyliczanie tras za pomocą punktów końcowych debugowania

Jedną z najprzydatniejszych funkcji, jakie może zapewnić źle skonfigurowana aplikacja Express, jest wskazanie wszystkich własnych tras. Programiści czasami tworzą punkt końcowy debugowania, który dla wygody w trakcie tworzenia aplikacji wymienia wszystkie zarejestrowane trasy, a następnie zapominają go usunąć przed uruchomieniem.

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:3000/api/routes
[{"method":"GET","path":"/"},{"method":"GET","path":"/api/users"},{"method":"GET","path":"/api/routes"},{"method":"GET","path":"/api/debug/env"}]
```

Jeśli ten punkt końcowy istnieje, odpowiedzią jest lista wszystkich ścieżek obsługiwanych przez aplikację. Oszczędza to czas na enumerację i pokazuje, które punkty końcowe istnieją, zanim poświęcisz czas na ich zgadywanie za pomocą Gobustera.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Punkt `/api/routes`końcowy działa poprzez odczytanie wewnętrznej właściwości Express `app._router.stack`w celu enumeracji zarejestrowanych tras. Jest to znany wzorzec błędnej konfiguracji Express, ale `app._router.stack`jest to właściwość wewnętrzna, której struktura może się różnić w zależności od wersji Express, a Express 5 zmienił wewnętrzne elementy routera na tyle, że zakłócił implementacje oparte na strukturze Express 4. Jeśli napotkasz punkt końcowy trasy, który zwraca nieoczekiwany format lub błąd, aplikacja może korzystać z innej wersji Express niż ta używana w tym laboratorium.

## Wystawione zmienne środowiskowe

Zmienne środowiskowe w aplikacjach Node.js często zawierają dane uwierzytelniające bazy danych, klucze API i flagi konfiguracyjne. Punkt końcowy debugowania, który zwraca dane, `process.env`to istotne odkrycie:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:3000/api/debug/env
{"NODE_ENV":"development","DB_PASSWORD":"NodeDBPass2024!","PORT":"3000","DB_HOST":"localhost:5432","APP_NAME":"company-portal"}r
```

Jeśli odpowiedź zawiera pola `DB_PASSWORD`, `SECRET_KEY`lub podobne, należy je udokumentować. `NODE_ENV`Wartość ta również jest istotna. `NODE_ENV=development`Na serwerze produkcyjnym jest to sygnał, że aplikacja została wdrożona bez odpowiedniego zabezpieczenia.

## Obsługa plików statycznych

Aplikacje Express często wykorzystują oprogramowanie `express.static()`pośredniczące do obsługi zasobów front-end, takich jak pliki JavaScript, arkusze stylów i konfiguracja. Trasa plików statycznych, jeśli istnieje, obsługuje wszystko w katalogu. Pliki JavaScript po stronie klienta czasami zawierają adresy URL punktów końcowych API, wewnętrzne nazwy hostów lub flagi debugowania osadzone jako stałe.

Gdy już znasz trasy z `/api/routes`punktu końcowego, sprawdź, co jest obsługiwane statycznie:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:3000/static/config.js
// Client-side configuration
const API_BASE = 'http://internal-api.company.local:8080';
const DEBUG = true;
const VERSION = '1.2.0';
```

Pliki konfiguracyjne służące jako zasoby statyczne łatwo przeoczyć, ponieważ technicznie rzecz biorąc, są publiczne (przeglądarka ich potrzebuje). Jednak „przeznaczone do publicznego użytku” to co innego niż „zawierają tylko informacje publiczne”.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** `express.static()` domyślnie zwraca kod błędu 404 dla plików typu dotfiles (plików zaczynających się od `.`). Jest to przeciwieństwo serwera HTTP Pythona, który obsługuje pliki typu dotfiles jak każdy inny plik. Jeśli szukasz `.env`pliku lub podobnego na trasie statycznej Express i otrzymujesz kod błędu 404, nie oznacza to, że plik jest nieobecny, ale że blokuje go oprogramowanie pośredniczące. Aby do niego dotrzeć, potrzebny jest dostęp do powłoki lub inna trasa.

## Łącząc wszystko razem

Cofnijmy się o krok i spójrzmy na to, co właśnie zrobiliśmy. Zaczęliśmy od inspekcji nagłówków, aby potwierdzić framework, następnie wywołaliśmy błąd, aby sprawdzić, co aplikacja ujawnia w trybie awarii, następnie użyliśmy punktu końcowego debugowania do wyliczenia tras, sprawdziliśmy ujawnienie danych uwierzytelniających w zmiennych środowiskowych i na koniec prześledziliśmy listę tras do plików statycznych, w których znajduje się flaga. Ten schemat działa, ponieważ każdy krok zawęża zakres kolejnego. Nagłówki informują o frameworku. Błędy informują o wewnętrznych mechanizmach. Punkty końcowe debugowania informują o trasach. Pliki statyczne informują o tym, co programiści uznali za bezpieczne do ujawnienia.

Odpowiedz na poniższe pytania

Jaką wartość `NODE_ENV`ma zmienna w odpowiedzi punktu końcowego debugowania?

Po Apacz i Node.js, dochodzenie w sprawie **Nginx** przebiega według tego samego schematu, ale z własnym słownikiem konfiguracji. Kategorie ujawniania wersji błędów konfiguracji, lista katalogowa, a odsłonięte strony statusu pojawiają się ponownie, ale konkretne dyrektywy i ścieżki są inne.

Nginx zajmuje inną przestrzeń niż Apacz i Node.js. Najczęściej jest używany jako odwrotny pełnomocnik, moduł równoważenia obciążenia lub wysokowydajny statyczny serwer plików. W środowiskach produkcyjnych Nginx często znajduje się przed serwerem aplikacji i obsługuje ruch publiczny. To umiejscowienie sprawia, że ​​jego konfiguracja jest istotna. Źle skonfigurowana instancja Nginx może ujawnić wewnętrzną strukturę, dane operacyjne lub udostępnić pliki, które nie powinny być dostępne.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacje:** W załączniku Maszyna wirtualna Nginx działa na porcie 8080, a nie standardowym porcie 80. Dzieje się tak, ponieważ Apaczkorzysta już z portu 80 na tym komputerze. W rzeczywistym wdrożeniu Nginx zazwyczaj działałby na porcie 80 lub 443.

**Ujawnienie wersji**

Schemat jest taki sam jak poprzednio: zacznij od `Server`nagłówka.

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -sI http://10.129.163.58:8080 | grep -i server
Server: nginx/1.24.0 (Ubuntu)
```

`Server`Nginx domyślnie uwzględnia swoją wersję w nagłówku . W przeciwieństwie do Apache'a, który `ServerTokens`kontroluje to za pomocą dyrektywy, Nginx używa `server_tokens`. Domyślnie jest to `on`, które ujawnia wersję. Znajomość dokładnej wersji jest przydatna podczas sprawdzania dziennika zmian Nginx w poszukiwaniu poprawek bezpieczeństwa lub podczas tworzenia raportu z zaangażowania.

Dyrektywa `server_tokens`kontroluje `Server`jednocześnie nagłówek i ciąg wersji na domyślnych stronach błędów; ustawienie `server_tokens off`blokuje wyświetlanie wersji z obu miejsc jednocześnie. Jeśli nagłówek `Server`jest blokowany, żądanie nieistniejącej ścieżki potwierdzi, czy `server_tokens`jest ona rzeczywiście wyłączona, czy tylko częściowo skonfigurowana.

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:8080/nonexistent-path
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.24.0 (Ubuntu)</center>
</body>
</html>
```

## Wpis do katalogu z funkcją automatycznego indeksowania

Nginx domyślnie nie włącza listowania katalogów. Gdy programista chce udostępnić listę katalogów, dodaje ją `autoindex`do bloku lokalizacji w konfiguracji:

```nginx
location /files/ {
    autoindex on;
    root /var/www/nginx/;
}
```

Jest to udokumentowana opcja konfiguracji Nginx i pojawia się w legalnych konfiguracjach udostępniania plików. Błędem w konfiguracji jest użycie jej na ścieżce zawierającej poufne pliki lub pozostawienie jej włączonej na serwerze produkcyjnym bez kontroli dostępu.

Przejdź do `http://10.129.163.58/files/`katalogu:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:8080/files/
<html>
<head><title>Index of /files/</title></head>
<body>
<h1>Index of /files/</h1><hr><pre><a href="../">../</a>
<a href="deploy-notes.txt">deploy-notes.txt</a>                                   03-Apr-2026 18:23                 148
<a href="old-backup.tar.gz">old-backup.tar.gz</a>                                  03-Apr-2026 18:23                 236
<a href="server-config.txt">server-config.txt</a>                                  03-Apr-2026 18:23                 135
</pre><hr></body>
</html>
```

Format HTML z funkcją autoindeksowania Nginx wykorzystuje prostą tabelę z nazwą pliku, datą ostatniej modyfikacji i rozmiarem pliku. Po jej znalezieniu przeczytaj każdy wymieniony plik. Listy katalogów Nginx często pojawiają się w ścieżkach skonfigurowanych przez programistów jako współdzielone miejsce do przechowywania danych, a następnie wypełnionych danymi operacyjnymi.

## Punkt końcowy nginx_status

Moduł Nginx `stub_status`udostępnia metryki połączeń w czasie rzeczywistym pod konfigurowalnym adresem URL. Bezpieczna konfiguracja ogranicza dostęp tylko do adresu lokalnego. Wersja błędnie skonfigurowana umożliwia dostęp z dowolnego adresu IP:

```nginx
location /nginx_status {
    stub_status;
    allow all;  # Should be: allow 127.0.0.1; deny all;
}
```

Poproś o to, aby zobaczyć, co ujawnia:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s http://10.129.163.58:8080/nginx_status
Active connections: 1 
server accepts handled requests
 15 15 15 
Reading: 0 Writing: 1 Waiting: 0 
```

Format wyjściowy jest kompaktowy i wykorzystuje nieoznakowane liczby w drugim wierszu, co może być dezorientujące, gdy zobaczysz to po raz pierwszy:

Trzy liczby w drugim wierszu są uporządkowane: łączna liczba zaakceptowanych połączeń, łączna liczba obsłużonych połączeń i łączna liczba żądań od uruchomienia serwera. Trzeci wiersz przedstawia zestawienie aktualnie aktywnych połączeń według stanu. Chociaż dane te nie nadają się bezpośrednio do wykorzystania, ujawniają informacje operacyjne dotyczące obciążenia serwera i wzorców użytkowania. W rzeczywistym przypadku ujawniony `/nginx_status`punkt końcowy jest odkryciem, ponieważ potwierdza wewnętrzną konfigurację monitorowania i może wskazywać na podobne ujawnienie innych punktów końcowych monitorowania.

## Łączenie wszystkiego w całość

Badanie Nginx przebiega podobnie do zadania Apache. Sprawdź nagłówek wersji, przejrzyj katalogi z włączonym autoindeksowaniem i sprawdź punkt końcowy statusu. Konkretne ścieżki i dyrektywy konfiguracyjne różnią się, ale podejście do badania jest takie samo.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** Pliki konfiguracyjne Nginx są dostępne `/etc/nginx/`w systemie Ubuntu. Jeśli kiedykolwiek będziesz mieć dostęp do powłoki na komputerze z Nginx, zapoznanie się z konfiguracją witryny `/etc/nginx/sites-available/`pokaże Ci dokładnie, które katalogi są dostępne i które moduły są włączone.

## Typowe błędy w konfiguracji serwerów

Przeprowadziliśmy już analizę czterech różnych serwerów WWW, z których każdy miał swój własny model konfiguracji i własny zestaw typowych błędów. Występują również wzorce, które pojawiają się niezależnie od serwera. Dwa z najbardziej powtarzalnych to brakujące nagłówki zabezpieczeń oraz szybkie wykrywanie błędów przez automatyczne skanery.

## Nagłówki bezpieczeństwa

**Nagłówki bezpieczeństwa** to HTTP Nagłówki odpowiedzi, które instruują przeglądarkę, jak obsługiwać zawartość strony. Chronią one przed szeregiem ataków po stronie klienta, w tym przed clickjackingiem, MIMsniffing i cross-site scripting. Żaden z serwerów w tym laboratorium nie został skonfigurowany do wysyłania tych nagłówków, co jest stanem domyślnym dla wszystkich czterech typów serwerów.

Oto najczęstsze z nich i ich działanie:

|Chodnikowiec|Przed czym chroni|Przykładowa wartość|
|---|---|---|
|`X-Frame-Options`|Clickjacking (uniemożliwia osadzenie strony w ramce iframe w innej domenie)|`DENY`Lub`SAMEORIGIN`|
|`X-Content-Type-Options`|Podsłuchiwanie MIME (uniemożliwia przeglądarce zgadywanie typów zawartości)|`nosniff`|
|`Content-Security-Policy`|Ogranicza miejsce, z którego mogą być ładowane skrypty, arkusze stylów i inne zasoby|`default-src 'self'`|
|`Referrer-Policy`|Kontroluje, co jest wysyłane w `Referer`nagłówku podczas przechodzenia do innej strony|`no-referrer`Lub`strict-origin`|
|`Strict-Transport-Security`|Wymusza protokół HTTPS dla kolejnych żądań (ma znaczenie tylko na serwerach HTTPS)|`max-age=31536000`|

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** `X-Frame-Options` technicznie rzecz biorąc, jest zastąpione przez `Content-Security-Policy: frame-ancestors`, które zapewnia bardziej szczegółową kontrolę. Zabezpieczone, nowoczesne witryny mogą obsługiwać ochronę przed kliknięciami wyłącznie za pośrednictwem CSP i celowo pomijać `X-Frame-Options`. Podczas zapisywania wyników, sprawdź oba.

Przeprowadź audyt każdego serwera za pomocą `curl`:

Terminal

```shell-session
root@ip-10-81-64-63:~# for port in 80 8000 3000 8080; do echo "=== Port $port ==="; curl -sI http://10.129.163.58:$port/ | grep -iE "x-frame-options|x-content-type|content-security-policy|strict-transport|referrer-policy" || echo "(no security headers found)"; done
=== Port 80 ===
(no security headers found)
=== Port 8000 ===
(no security headers found)
=== Port 3000 ===
(no security headers found)
=== Port 8080 ===
(no security headers found)
```

Brak `grep`wyniku oznacza brak tych nagłówków. Wykonaj tę czynność na wszystkich czterech portach, a zobaczysz, że domyślne konfiguracje dla wszystkich czterech typów serwerów mają tę samą lukę. Nagłówki zabezpieczeń wymagają aktywnej konfiguracji. Domyślnie nigdy nie są obecne.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** `Strict-Transport-Security` dotyczy tylko połączeń HTTPS. Ponieważ to laboratorium korzysta z protokołu HTTP, jego brak jest oczekiwany i odnotowano go tutaj dla zapewnienia kompletności, a nie jako aktywny błąd konfiguracji.

## Automatyczne skanowanie z Nikto

`Nikto`to skaner serwera WWW, który sprawdza znane błędy konfiguracji, nieaktualne oprogramowanie, odsłonięte interfejsy administracyjne i brakujące nagłówki zabezpieczeń. Nie jest subtelny; generuje duży ruch i jest łatwy do wykrycia. Dzięki temu nadaje się do autoryzowanych testów, a nie do działania w ukryciu. Uruchom go na serwerze Apache:

Terminal

```shell-session
root@ip-10-81-64-63:~# nikto -h http://10.129.163.58:80 -nointeractive
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.129.163.58
+ Target Hostname:    10.129.163.58
+ Target Port:        80
+ Start Time:         2026-04-11 09:16:09 (GMT1)
---------------------------------------------------------------------------
+ Server: Apache/2.4.58 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0x29af 0x64e9243796aa2 
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: HEAD, GET, POST, OPTIONS 
+ OSVDB-561: /server-status: This reveals Apache information. Comment out appropriate line in httpd.conf or restrict access to allowed hosts.
+ OSVDB-3268: /files/: Directory indexing found.
+ OSVDB-3092: /files/: This might be interesting...
+ 6544 items checked: 0 error(s) and 6 item(s) reported on remote host
+ End Time:           2026-04-11 09:16:18 (GMT1) (9 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Flaga ta `-nointeractive`blokuje monity, dzięki czemu skanowanie przebiega bez oczekiwania na dane wejściowe. Nikto sprawdzi setki typowych ścieżek i wzorców. Szukaj wyników zaczynających się od `+`w danych wyjściowych.

W przypadku nieprawidłowo skonfigurowanego serwera Apache, takiego jak ten, należy spodziewać się, że Nikto oznaczy wystawioną na próbę `/server-status`stronę, `backup.bak`plik w katalogu głównym dokumentów, listę katalogów w `/files/`oraz liczne ostrzeżenia dotyczące brakujących nagłówków zabezpieczeń.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** Dane wyjściowe Nikto mogą być szczegółowe. Ta `-Tuning`opcja pozwala ograniczyć zakres przeprowadzanych sprawdzeń. W przypadku szybkiego skanowania `nikto -h TARGET -Tuning 123`obejmuje najczęstsze ustalenia bez uruchamiania pełnego zestawu sygnatur. Należy pamiętać, że kody dostrajające są łączone, a nie rozdzielane przecinkami.

## Wzory, które mają zastosowanie wszędzie

Przyglądając się wszystkim czterem serwerom, wielokrotnie pojawiają się te same kategorie błędnych konfiguracji:

|Błędna konfiguracja|Apacz|HTTP w Pythonie|Node.js|Nginx|
|---|---|---|---|---|
|Ujawnianie wersji w nagłówkach|Tak|Tak|Częściowy|Tak|
|Wpis do katalogu|`/files/`|Ścieżka główna|Nie dotyczy|`/files/`|
|Wystawiony status lub punkt końcowy debugowania|`/server-status`|Nie dotyczy|`/api/debug/env`,`/api/routes`|`/nginx_status`|
|Dostępne są poufne pliki|`backup.bak`,`internal-notes.txt`|`.env`, `notes.txt`,`backup.zip`|`config.js`|`server-config.txt`,`deploy-notes.txt`|
|Brak nagłówków bezpieczeństwa|Wszystko|Wszystko|Wszystko|Wszystko|

Spójnym wątkiem jest to, że domyślne konfiguracje priorytetyzują łatwość wdrożenia nad bezpieczeństwem. Ujawnianie wersji, listy katalogów i strony statusu są domyślnie włączone w celach diagnostycznych. Ułatwiają one pracę administratora. Usunięcie lub ograniczenie tych funkcji wymaga świadomego działania. W rzeczywistych zastosowaniach znalezienie tych wzorców nie oznacza zaniedbania. Wskazuje raczej, że ustawienia domyślne nigdy nie zostały sprawdzone.

Odpowiedz na poniższe pytania

Który nagłówek zabezpieczeń, w przypadku jego braku, pozwala na osadzenie strony w ramce iframe w innej domenie?

Praca z czterema różnymi serwerami WWW na tej samej maszynie ujawnia coś, co łatwo przeoczyć, analizując każdy typ serwera w izolacji: podstawowe wzorce są takie same. Ujawnienie wersji,lista katalogowa, odsłonięte strony statusu i brakujące nagłówki zabezpieczeń pojawiają się naApacz, Nginx, Node.js i PythonHTTPserwer z tego samego powodu. Domyślne konfiguracje są dozwolone. Bezpieczeństwo wymaga konfiguracji.

## Najważniejsze wnioski

- Nagłówki odpowiedzi to najszybsza powierzchnia odcisku palca. Nagłówki `Server`i `X-Powered-By`ujawniają typ oprogramowania, a czasem jego wersję, jeszcze zanim użytkownik wyśle ​​jakiekolwiek żądanie do faktycznej ścieżki aplikacji.
- Wbudowany serwer HTTP Pythona nie ma żadnych mechanizmów kontroli dostępu. Gdy pojawia się w zaangażowaniu, należy założyć, że cały katalog roboczy jest czytelny, łącznie z plikami typu dotfiles, takimi jak `.env`.
- Apache `mod_status`i lista katalogów są domyślnie włączone w instalacjach Ubuntu i wymagają aktywnej konfiguracji, aby je ograniczyć. Ich obecność jest powszechna i warto ją sprawdzać przy każdej instalacji.Apaczzaręczyny.
- Aplikacje Node.js Express w trybie deweloperskim ujawniają ślady stosu, listy tras i zmienne środowiskowe. Każde z nich jest odkryciem samym w sobie, a razem dają pełny obraz wnętrza aplikacji.
- Nginx `autoindex`i `stub_status`mirror Apache wyświetlają listę katalogów i `mod_status`wzorce. Dyrektywy różnią się, ale podejście do analizy jest takie samo.
- Nagłówki zabezpieczeń są domyślnie nieobecne na wszystkich czterech typach serwerów. Audyt z użyciem `curl -sI`i `grep`dla nazw nagłówków to szybka i niezawodna kontrola, która jest nieodłączną częścią każdego zaangażowania serwera WWW.

Następne pomieszczenia modułu będą zawierały nowoczesne stosy sieciowe i atakująceIISserwery WWW oparte na systemie Windows, które są konfigurowane w środowisku Windows.
