---

W tej części poznamy podstawowe koncepcje techniczne różnych protokołów. Aby jednak pójść dalej, musimy mieć jasność co do następujących dwóch idei, które są cechą charakterystyczną każdego protokołu, niezależnie od jego funkcjonalności:

- Każdy protokół reprezentuje określone warstwy modelu OSI lub TCP/model IP i działa zgodnie z funkcjonalnością tej warstwy.
- TCPIUDP- oparte na protokołach działają na określonych portach sieciowych.

### Protokół HTTPS

#### Przegląd techniczny – HTTPS

Hypertext Transfer Protocol Secure (HTTPS) to protokół klient-serwer, odpowiedzialny za bezpieczne przesyłanie danych między serwerem WWW (stroną internetową) a przeglądarką internetową (po stronie klienta). Jest to szyfrowana odmianaHTTPktóry przesyła dane w formacie niezaszyfrowanym.

HTTPWystarczyłoby przejrzeć stronę internetową, aby dowiedzieć się więcej o produkcie firmy; jednak protokół HTTPS jest niezbędny, jeśli chcesz podać dane swojej karty kredytowej, aby złożyć zamówienie online. Protokół HTTPS został opracowany w celu bezpiecznego udostępniania poufnych informacji, w tym haseł, danych kontaktowych i informacji finansowych, między przeglądarkami internetowymi a stronami internetowymi. Bez protokołu HTTPS bezpieczna bankowość internetowa i płatności online nie byłyby możliwe.

#### Przepływ pracy – HTTPS

Protokół HTTPS wykorzystuje swój niezaszyfrowany odpowiednik, tj.HTTPi dodaje warstwę szyfrowania. W tym przypadku jest to SSL/TLS (Bezpieczna warstwa gniazd/Bezpieczeństwo warstwy transportowej);odpoczynekPrzepływ pracy pozostaje taki sam. Zanim przejdziemy dalej, omówimy, jakHTTPżądania i odpowiedzi działają w typowym środowisku klient-serwer.

#### Żądanie i odpowiedź - HTTP

Jakiś HTTP żądanie jest składane przez agenta użytkownika (przeglądarkę lub inną aplikację wysyłającą żądania przez sieć)API(Interfejs Programowania Aplikacji). W przypadku odpowiedzi sytuacja jest odwrotna. Żądanie to ma na celu uzyskanie dostępu do zasobów na zdalnym serwerze WWW, na które następnie odpowiada serwer WWW. Poniższy rysunek przedstawia przeglądarkę internetową wysyłającąHTTPżądanie do serwera WWW, nasłuchującegoTCPport 80.

![Diagram ilustrujący żądanie HTTP z przeglądarki internetowej i odpowiedź HTTP z serwera WWW nasłuchującego na porcie 80. Dane są wysyłane w postaci zwykłego tekstu.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/62d879ca8881dc59a9567a071b330322.png)

Żądanie może `GET`dotyczyć strony internetowej, obrazu lub pliku. Inne żądania HTTP obejmują `PUT`i `POST`, które wysyłają dane do serwera WWW, takie jak wartość lub plik. Więcej informacji o protokole HTTP można znaleźć w  sekcji [„HTTP in Detail”](https://tryhackme.com/room/httpindetail) .

Jeśli atakujący zdoła przechwycić pakiety sieciowe przesyłane między klientem a serwerem za pośrednictwem protokołu HTTP, będzie mógł odczytać ich zawartość, ponieważ są one wysyłane w postaci zwykłego tekstu.

#### Żądanie i odpowiedź – HTTPS

Po krótkim omówieniu przepływu pracy żądań i odpowiedzi HTTP, warto zapoznać się z protokołem HTTPS. Pamiętaj, że „S” w skrócie HTTPS oznacza dodatkową warstwę szyfrowania SSL/TLS dodaną do protokołu HTTP.

![Diagram ilustrujący żądanie HTTPS z przeglądarki internetowej i odpowiedź HTTPS z serwera WWW nasłuchującego na porcie 443. Dane są wysyłane w postaci zaszyfrowanej.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a31d2f96d32754bdc8327df2dbd5491c.png)

Nawet jeśli atakujący zdoła przechwycić pakiety sieciowe przesyłane między klientem a serwerem za pomocą protokołu HTTPS, nie będzie mógł odczytać zawartości danych TCP ze względu na szyfrowanie.

#### Mechanizm szyfrowania HTTPS

Jak już wspomniano, protokół SSL/TLS zapewnia warstwę szyfrowania protokołu HTTPS. Opiera się on na szyfrowaniu asymetrycznym (kryptografii klucza publicznego) i szyfrowaniu symetrycznym. Szyfrowanie asymetryczne wykorzystuje dwa klucze, tj. klucz publiczny i klucz prywatny; jego zasadą jest wynegocjowanie algorytmu szyfrowania symetrycznego i klucza tajnego. Domyślny port protokołu HTTPS to 443. Szyfrowanie chroni przed przechwyceniem i modyfikacją danych, zachowując poufność i integralność przesyłanego ruchu.

### Protokół FTPS

#### Przegląd techniczny – FTPS

File Transfer Protocol Secure (FTPS) to protokół komunikacyjny, który jest udoskonaloną i bezpieczną wersją File Transfer Protocol (FTP). Początkowo FTP został opracowany w 1971 roku i opublikowany jako RFC 114. Dodatkowe udoskonalenia i zmiany zostały opublikowane w RFC 765 i RFC 959.

FTP został zaprojektowany jako model klient-serwer; między klientem a serwerem stosowane są oddzielne połączenia sterujące/polecenia i dane, a także nazwa użytkownika i hasło. W FTP zarówno uwierzytelnianie, jak i przesyłanie danych między klientem a serwerem odbywa się w formie niezaszyfrowanej; natomiast w FTPS ustanawiany jest kanał szyfrowany.

#### Przepływ pracy

FTPS to rozszerzenie protokołu FTP, które dodaje zabezpieczenia TLS do poleceń i połączeń danych. Aby zrozumieć FTPS, konieczne jest zapoznanie się z jego podstawami.

#### Żądanie i odpowiedź - FTP

Jak opisano wcześniej, FTP opiera się na modelu klient-serwer. Wykorzystuje on dwa następujące kanały komunikacji między klientem a serwerem.

- **Połączenie kontrolne:**  W tym przypadku klient FTP (np. Filezilla i CuteFTP) wysyła żądanie połączenia (uwierzytelnienia) do zdalnego serwera FTP na domyślnym porcie FTP, czyli porcie TCP 21. Jak sama nazwa wskazuje, połączenie kontrolne służy do wysyłania i odbierania poleceń i odpowiedzi.
- **Połączenie danych:**  Po uwierzytelnieniu połączenie to jest wykorzystywane do przesyłania danych (plików i folderów).

#### Typy połączeń FTP

FTP ma dwa tryby:

1. Aktywne tryby
2. Tryb pasywny

##### Tryb aktywny

W trybie połączenia aktywnego klient nawiązuje połączenie sterujące, aby wysłać polecenia/parametry uwierzytelniania do serwera. Po uwierzytelnieniu i na żądanie klienta o zainicjowanie transferu danych, serwer nawiązuje połączenie z klientem w celu przesłania danych. W skrócie:

1. Klient FTP łączy się z serwerem FTP na porcie TCP 21 w celu nawiązania połączenia poleceń.
2. Serwer FTP łączy się z klientem FTP na porcie TCP 20 w celu nawiązania połączenia danych.

![Diagram przedstawiający połączenie FTP w trybie aktywnym](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/59598772945981811433970ce8335d51.png)

Warto wspomnieć, że ten typ połączenia nie jest odpowiedni w środowisku, w którym klient znajduje się za zaporą sieciową, ponieważ blokuje połączenia przychodzące do klienta. W przypadku klienta znajdującego się za zaporą sieciową konieczne byłoby połączenie pasywne.

##### Tryb pasywny

W trybie połączenia pasywnego klient nawiązuje połączenie sterujące i połączenie danych. Klient wysyła polecenie `PASV`do serwera kanałem poleceń, a serwer wysyła klientowi losowy port. Gdy tylko klient otrzyma numer portu, nawiązuje połączenie z podanym numerem portu, aby serwer mógł zainicjować transfer danych do klienta.

![Diagram przedstawiający połączenie FTP w trybie pasywnym](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/9fb1d6121138d219f436d4650b030a8b.png)

Ten typ połączenia działa dobrze, gdy klient znajduje się zazapora sieciowa.

#### FTP Typy danych

Podczas wymiany danych pomiędzy klientem i serwerem używane są następujące typy danych:

- **ASCII/Typ A** : Jest to domyślny typ używany do przesyłania plików tekstowych. W razie potrzeby dane są konwertowane do 8-bitowego kodu ASCII przed transmisją, a następnie konwertowane z powrotem po odbiorze.
- **Obraz/Typ I** : Ten tryb jest powszechnie nazywany trybem binarnym. Wykorzystuje transmisję bajt po bajcie. Odbiorca przechowuje odebrane bajty po odebraniu.
- **EBCDIC/Typ E** : Nadaje się do komunikacji tekstowej przy użyciu zestawu znaków EBCDIC.
- **Typ lokalny Ln:** Jest on zazwyczaj używany do przesyłania plików między maszynami, które nie obsługują transferu 8-bitowych bajtów. Oto `n`drugi parametr reprezentujący rozmiar w bajtach. 

#### Żądanie i odpowiedź - FTPS

Jak sama nazwa wskazuje, FTPS jest rozszerzeniem protokołu FTP. Dodaje warstwę szyfrowania, aby bezpiecznie przesyłać polecenia i dane między klientem a serwerem. Do uruchomienia zabezpieczeń wykorzystywane są dwie następujące metody:

- **Połączenie niejawne** : W tym połączeniu klient i serwer FTPS nawiązują połączenie, w którym kanały poleceń i danych są automatycznie zabezpieczane za pomocą szyfrowania SSL.
- **Połączenie jawne** : Klient FTP wyraźnie żąda od serwera nawiązania zabezpieczonej sesji SSL/TLS na porcie 21, a następnie kontynuowania transferu danych w oparciu o wzajemnie uzgodniony mechanizm uwierzytelniania. W przypadku połączenia jawnego można wybrać kanał do szyfrowania, wybierając jeden z trzech trybów komunikacji dla kanału sterującego i kanału danych, tj. szyfrowany tylko kanał sterujący, szyfrowane tylko dane oraz szyfrowany zarówno kanał sterujący, jak i dane.

Standardowy port dla FTP i jawnego FTPS to 21, natomiast w przypadku niejawnego FTPS jest to 990. Dodanie FTPS chroni przed atakami typu sniffing na dane logowania.

### Protokół SMTPS

#### Przegląd techniczny

Simple Mail Transfer Protocol Secure (SMTPS) to rozszerzenie protokołu SMTP, używanego do komunikacji e-mail. Nie należy mylić SMTP z protokołem POP3. Chociaż oba protokoły są wykorzystywane do komunikacji e-mail, SMTP to protokół „Email Push” służący do przesyłania wiadomości e-mail z klienta na serwer. Natomiast POP3 służy do pobierania wiadomości e-mail z serwera do klienta. SMTPS to rozszerzenie protokołu SMTP; wykorzystuje on protokoły TLS/SSL do zapewnienia uwierzytelniania, integralności i poufności przesyłanych danych. Najpierw przyjrzyjmy się protokołowi SMTP.

#### Protokół SMTP

Jak opisano wcześniej, SMTP to „protokół push poczty elektronicznej” powszechnie używany do przesyłania wiadomości e-mail z klienta SMTP na serwer SMTP. SMTP jest implementowany w następujących dwóch modelach:

- **SMTP End-to-End:**  Ten model jest używany do komunikacji e-mailowej między organizacjami. W tym modelu klient SMTP po stronie nadawcy inicjuje połączenie SMTP z serwerem SMTP odbiorcy.
- **SMTP Store-and-Forward:**  Ten model jest używany do komunikacji e-mailowej w organizacji. W tym modelu serwer SMTP przechowuje kopię wiadomości e-mail w swoim systemie (tj. przechowuje ją), dopóki nie zostanie ona przesłana do odbiorcy.

#### Komponenty SMTP

Aby zrozumieć przepływ pracy protokołu SMTP, przyjrzymy się następującym podstawowym komponentom protokołu SMTP:

- **User Agent (UA):**  UA odpowiada za utworzenie wiadomości e-mail i wysłanie jej do Mail Transfer Agent (MTA). 
- **Agent transferu poczty (MTA):**  MTA przesyła wiadomość e-mail z UA do odbiorcy MTA przez Internet (często MTA i agent dostarczania poczty są hostowane na tym samym serwerze).

![Diagram przedstawiający protokół SMTP używany do przesyłania wiadomości e-mail przez Internet.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0675230daa95a5bcfdaf2d9017de25b1.png)

#### Proces TLS w SMTPS

SMTPS nie jest protokołem zastrzeżonym; zamiast tego opakowuje SMTP w TLS. Można powiedzieć, że SMTPS jest podobny do SMTP w warstwie aplikacji, z rozszerzeniem szyfrowania TLS w warstwie transportowej. Do szyfrowania polecenie  `STARTTLS` jest używane między klientem poczty e-mail a serwerem poczty e-mail.

Porty 587 i 465 są często używane do ruchu SMTPS. Wiadomości przesyłane za pomocą SMTP nie są szyfrowane, więc są podatne na ataki typu sniffing. Dlatego do szyfrowania wiadomości e-mail używany jest protokół SMTPS.TLSprzed transmisją. Ponadto SMTPS zabrania atakującym wysyłania wiadomości spam z zainfekowanych/podatnych domen, eksfiltracji poufnych informacji i przeprowadzania ataków phishingowych.

### Protokół POP3S

#### Przegląd techniczny – POP3S

Protokół Post Office Secure (POP3S) jest rozszerzeniem protokołuPOP3Protokół; służy do szyfrowanego pobierania wiadomości e-mail z serwera pocztowego do klienta pocztowego. Najpierw przyjrzyjmy się bliżejPOP3protokół.

#### POP3Protokół

W poprzedniej sekcji omówiliśmy, w jaki sposób protokół SMTPS jest używany do bezpiecznego przesyłania wiadomości e-mail.SMTPnie jest odpowiedzialny za odbieranie wiadomości e-mail; tutaj,POP3wchodzi do gry.POP3jest najnowszą wersją protokołu POP. Pobiera wiadomości e-mail z agenta dostarczającego pocztę (MDA) do agenta użytkownika poczty (MUA).

#### POP3Komponenty i przepływ pracy

Tak jak SMTP,POP3Składa się z dwóch komponentów: klienta (MUA) i serwera (MDA). Oto kroki:

1. Klient poczty elektronicznej nawiązuje połączenie z serwerem pocztowym.
2. Klient poczty elektronicznej pobiera wszystkie wiadomości e-mail z kolejki na serwerze pocztowym. (Jest to opcja domyślna, jednak klient może wybrać do pobrania tylko konkretne wiadomości e-mail).
3. Wszystkie wiadomości e-mail są zapisywane na urządzeniu, z którego nawiązano połączenie.
4. Serwer pocztowy usuwa kopię wiadomości e-mail. (Jest to opcja domyślna; klient może zdecydować o niepobieraniu wiadomości e-mail po jej pobraniu.)

#### OgraniczeniaPOP3

- **Wiadomości e-mail są przetwarzane lokalnie:**  Brak synchronizacji wiadomości e-mail na wielu urządzeniach. Protokół pobiera wiadomości e-mail na aktualnie zalogowanym urządzeniu i zazwyczaj usuwa je z serwera.
- **Transmisja w postaci zwykłego tekstu:**  Nazwa użytkownika i hasło, wraz z wiadomościami e-mail, są wysyłane w postaci zwykłego tekstu, co czyni je podatnymi na ataki typu sniffing.

#### POP3S

Podsumowując,POP3jest uważany za słaby z punktu widzenia bezpieczeństwa. Wymaga to dodatkowej warstwy zabezpieczeń; stąd w grę wchodzi POP3S. POP3S jest rozszerzeniemPOP3, który obejmuje komunikację związaną z wiadomościami e-mailTLSW tym celu klient i serwer inicjują polecenie `STARTTLS`, jak pokazano na poniższym rysunku. Po tym `EHLO`, serwer POP3S uruchomi przełączenie na TLS. Należy pamiętać, że skrót ten `EHLO`oznacza Extended HELO, gdzie `HELO`jest poleceniem używanym do identyfikacji serwera.

![Rysunek ilustrujący sposób, w jaki protokół POP3S używa protokołu TLS do szyfrowania komunikacji między klientem poczty e-mail a serwerem poczty e-mail.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/9532e1d438c7ad07222bcb3977a4376b.png)

Protokół POP3S wykorzystuje port 995, podczas gdyPOP3używa portu 110. W następnym zadaniu poznamy kilka innych bezpiecznych protokołów na warstwie aplikacji.

Odpowiedz na poniższe pytania

Jaki jest domyślny port dla protokołu HTTPS?

### DNSSEC

Jak już zapewne wiesz,DNSoznacza system nazw domen.DNSProtokół odpowiada głównie za rozwiązywanie nazw domen. Zamiast zapamiętywać adres IP, należy skupić się na nazwie domeny. Na przykład, w momencie pisania tego tekstu, `example.com`resolves to `93.184.216.34`; jasne jest, który z nich jest łatwiejszy do zapamiętania dla ludzkiego umysłu.

DNS działa poprzez wysyłanie zapytania DNS. Na przykład, podczas przeglądania stron internetowych, przeglądarka może wysłać zapytanie o typ rekordu DNS  `A`, `AAAA`np. adresy IPv4 lub IPv6. W poniższym wyniku konsoli widzimy hosta o adresie IP `192.168.0.102`wysyłającego dwa zapytania DNS do serwera DNS `1.0.0.1`dotyczące nazwy domeny `example.com`. Możemy zobaczyć odpowiedzi na zapytania `A`i `AAAA`.

Terminal

```shell-session
user@TryHackMe$ sudo tshark port 53
    1 0.000000000 192.168.0.102 → 1.0.0.1      DNS 82 Standard query 0x2717 A example.com OPT
    2 0.012241216      1.0.0.1 → 192.168.0.102 DNS 98 Standard query response 0x2717 A example.com A 93.184.216.34 OPT
    3 0.013454645 192.168.0.102 → 1.0.0.1      DNS 82 Standard query 0xac05 AAAA example.com OPT
    4 0.018705620      1.0.0.1 → 192.168.0.102 DNS 110 Standard query response 0xac05 AAAA example.com AAAA 2606:2800:220:1:248:1893:25c8:1946 OPT
```

Takie rozwiązanie zamiany nazwy na adres IP jest bardzo wygodne; jednak każdy w sieci mógłby odpowiedzieć sfałszowaną odpowiedzią. Co więcej, host, który wysłał zapytanie, zaakceptowałby odpowiedź „dowolną”. Innymi słowy, host połączyłby się z nieautoryzowanym serwerem. Jednym ze sposobów uniknięcia takiej sytuacji jest użycie protokołu DNSSEC.

DNSSEC umożliwia zapewnienie, żeDNSOdpowiedź, którą otrzymujemy, pochodzi od właściciela domeny. Aby to osiągnąć, DNSSEC wymaga dwóch głównych rzeczy:

1. TenDNSwłaściciel strefy powinien podpisać wszystkieDNSrekordy przy użyciu ich klucza prywatnego.
2. TenDNSstrefa publikuje swój klucz publiczny, aby użytkownicy mogli sprawdzić jego ważnośćDNSrejestruje podpisy.

Innymi słowy, dane dla nasDNSzapytanie jest podpisane w celu zagwarantowania jego integralności i autentyczności; ponadto możemy skutecznie sprawdzić podpis.

W przypadku podpisanych rekordów protokół DNSSEC zapewnia następujące funkcje:

- Autentyczność: Możesz potwierdzić, że danyDNSWłaściciel jest autorem i wysłał rekord. Autentyczność jest możliwa, ponieważ otrzymany rekord jest podpisany przezDNSprywatny klucz właściciela.
- Integralność: Możesz mieć pewność, że w trakcie przesyłania rekordu nie wprowadzono żadnych zmian. Wszelkie zmiany w rekordzie spowodują unieważnienie jego podpisu.

### OpenPGP

Kiedy w 1971 roku wysłano pierwszą wiadomość e-mail, mieliśmy do czynienia z innym krajobrazem cyberbezpieczeństwa. Protokoły poczty elektronicznej, takie jak SMTP i POP3, zostały zaprojektowane do wysyłania wiadomości w postaci zwykłego tekstu. To samo dotyczy protokołu IMAP, który umożliwia synchronizację skrzynki pocztowej ze skrzynką na serwerze. Wszystkie te protokoły sprawiają, że wiadomość e-mail niczym nie różni się od otwartej, otwartej dla wszystkich pocztówki przesyłanej z jednego serwera na drugi.

Poniższy obrazek przedstawia uproszczony przykład, w którym użytkownik używa klienta poczty elektronicznej do wysyłania wiadomości e-mail przez SMTP i odbierania nowych wiadomości e-mail przez POP3 lub IMAP. Serwer pocztowy używa SMTP do dostarczania wiadomości e-mail użytkownika do adresata. Ponieważ wszystkie te protokoły wykorzystują zwykły tekst, intruz może odczytać wiadomości e-mail przesyłane przez Internet.

![Schemat sieci pokazujący, jak protokół SMTP jest używany do wysyłania wiadomości e-mail, a protokół POP3 do ich odbierania.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/6cf8953835d91c3889ec3e51dbb20b21.png)

Wraz ze wzrostem popularności poczty internetowej, użytkownicy zaczęli łączyć się z serwerem WWW, aby czytać i pisać wiadomości e-mail. Poniższy obraz przedstawia wiadomość e-mail pisaną w przeglądarce internetowej. Serwer WWW z kolei wykorzystuje serwer pocztowy do wysyłania i odbierania wiadomości przychodzących. Połączenie odbywało się za pośrednictwem protokołu HTTP, co oznaczało, że nadal występowały te same problemy z bezpieczeństwem związane z poufnością i integralnością.

![Prosty diagram sieciowy pokazujący działanie poczty internetowej przy użyciu protokołów HTTP i SMTP](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/23da18a37a955ab916250d3f2a5496b8.png)

Jednak gdy dostawcy usług zdali sobie sprawę z potrzeby stosowania protokołu SSL/TLS do zabezpieczania ruchu internetowego, protokół HTTPS stał się nowym standardem. W rezultacie większość internetowych systemów poczty elektronicznej przeszła na protokół HTTPS, co spowodowało szyfrowanie ruchu między przeglądarką internetową a serwerem internetowym. Jednak ruch e-mail między serwerem internetowym a serwerem(-ami) pocztowym(-ymi) niekoniecznie jest szyfrowany. Serwer internetowy i serwery pocztowe mogą odczytywać zawartość wiadomości; ponadto serwery pocztowe mogą wykorzystywać protokół SMTP do przesyłania wiadomości, co oznacza, że ​​wiadomości e-mail będą przesyłane przez Internet w postaci zwykłego tekstu.

![Prosty diagram sieciowy pokazujący działanie poczty internetowej przy użyciu protokołu HTTPS i protokołu SMTP lub SMTPS](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/55d996d0d8b73b61232db81e51c45cb5.png)

Z czasem protokoły SSL/TLS zaczęły być stosowane we wszystkich protokołach poczty elektronicznej. SMTP, POP3 i IMAP stały się odpowiednio SMTPS, POP3S i IMAPS. Litera „S” dodana do nazwy protokołu odnosi się do **bezpiecznego protokołu** , wskazując na dodanie protokołu SSL/TLS do istniejącego protokołu.

Poniższy obrazek przedstawia uproszczony przykład, w którym klient poczty używa protokołu SMTPS do wysyłania wiadomości e-mail i protokołu POP3S lub IMAPS do ich odbierania. W rezultacie wiadomości e-mail są przesyłane w formie zaszyfrowanej między klientem a serwerem, jednak serwer poczty może odczytać ich zawartość.

![Schemat sieci przedstawiający sposób wykorzystania protokołu SMTPS do bezpiecznego wysyłania wiadomości e-mail oraz sposób wykorzystania protokołu POP3S do bezpiecznego odbierania wiadomości e-mail.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/ad9e412e946ecbe7b8aa82ccdb55cb42.png)

Wprowadzenie protokołu SSL/TLS znacząco zwiększyło bezpieczeństwo wiadomości e-mail. Nadal jednak musimy ufać serwerom pocztowym, z którymi się łączymy. Jeśli nie czujesz się z tym komfortowo, rozważ standard taki jak OpenPGP. PGP (Pretty Good Privacy) to program szyfrujący stworzony przez Phila Zimmermana. OpenPGP to **otwarty standard** podpisywania i szyfrowania plików oraz wiadomości e-mail, szczegółowo opisany w [dokumencie RFC 4880.(otwiera się w nowej karcie)](https://www.rfc-editor.org/rfc/rfc4880)GnuPG (Gnu Privacy Guard), lub po prostu GPG, to darmowa i otwartoźródłowa implementacja standardu OpenPGP. W skrócie, GnuPG umożliwia podpisywanie i szyfrowanie danych oraz komunikacji.

GnuPG można łatwo zintegrować z klientem poczty elektronicznej, aby bezproblemowo podpisywać, szyfrować i deszyfrować wiadomości e-mail. Wiadomości e-mail zaszyfrowane za pomocą GnuPG (tj. zgodnie ze standardem OpenPGP) mogą być odczytane tylko przez adresata. Innymi słowy, nikt, łącznie z serwerami pocztowymi, nie może odczytać zawartości wiadomości poza odbiorcą.

W przypadku poczty e-mail GnuPG wymaga od każdego użytkownika wygenerowania pary kluczy: klucza prywatnego i klucza publicznego. Mówiąc prościej, klucz prywatny nadawcy służy do podpisu, a klucz publiczny odbiorcy do szyfrowania. Z perspektywy odbiorcy, klucz publiczny nadawcy służy do weryfikacji podpisu, a klucz prywatny odbiorcy do deszyfrowania. Aby uzyskać więcej informacji na temat szyfrowania asymetrycznego, zalecamy zapoznanie się z salą [„Wprowadzenie do kryptografii”](https://tryhackme.com/room/cryptographyintro) .

Implementacje OpenPGP, takie jak GnuPG, oferują doskonałe rozwiązanie do ochrony poufności i integralności treści wiadomości e-mail. Nie obejmuje to jednak nagłówków wiadomości e-mail.

Poniżej znajduje się przykład wiadomości przed i po zaszyfrowaniu za pomocą OpenPGP. Oryginalna wiadomość jest pokazana poniżej.

Terminal

```shell-session
user@TryHackMe$ cat message.txt
Hello,

Please proceed with the transaction.

Best,
Strategos
```

Aby korzystać z OpenPGP, obie strony muszą wygenerować parę kluczy za pomocą polecenia `gpg --gen-key`. Polecenie to poprosi użytkownika o podanie imienia i nazwiska oraz adresu e-mail, a następnie utworzy klucz prywatny i publiczny. Klucz prywatny powinien być przechowywany bezpiecznie, a klucz publiczny powinien być udostępniany innym stronom, z którymi chcemy bezpiecznie się komunikować.

Użycie klienta poczty elektronicznej obsługującego OpenPGP spowoduje zaszyfrowanie wiadomości za pomocą klucza odbiorcy. Jeśli jednak chcemy dokonać tego za pomocą wiersza poleceń, polecenie będzie wyglądać mniej więcej tak:

`gpg --encrypt --sign --armor -r strategos@tryhackme.thm message.txt`

Zwróć uwagę na następujące opcje:

- `--encrypt -r recipient@tryhackme.thm`Szyfrowanie odbywa się `message.txt`za pomocą klucza publicznego powiązanego z adresem e-mail odbiorcy. Zapewnia to poufność.
- `--sign`Podpisze naszą wiadomość (używając naszego klucza prywatnego). To potwierdzi jej autentyczność.
- `--armor`jest generowanie danych wyjściowych w formacie ASCII zamiast binarnym.

Szyfrowanie przy użyciu tej funkcji `gpg`pozwoliło na utworzenie następującej wiadomości, którą można bezproblemowo wysłać za pomocą klienta poczty e-mail.

Terminal

```shell-session
user@TryHackMe$ cat message.txt.asc
-----BEGIN PGP MESSAGE-----

hF4Dt1Jduipo/LESAQdAmqgCLQRRQCFNOBWSF+dY64suA8xtty7ysfolfF7+fnUw
crwR2ioRTcXTe6c0dZl/sdmtjDJPZWGHI3XcD7XWA2hPDb+w4P46e9FJGsCE/JaO
1I4BCQIQZc91A79Ebli/41D0aVkBmDpjIgvpwjHdmomT7dghTcB+Qp80WbYDnV20
4qTgdgdAnLtQp3fnJCXlZ0BfecPB+ZfECdD1IAleBB3o14v5v/ntfPKfXPZwODUm
ELY7piC2GclBWbirrZsnzTLWeYCrABiKJ3Rb75VgJXdM1uKNBY0HLN06VdEuDy+L
=nRQE
-----END PGP MESSAGE-----
```

### SSH

Wraz z pojawieniem się systemów sieciowych pojawiła się potrzeba łączenia się z systemem przez sieć. Na przykład, użytkownik musi wykonywać procesy i administrować systemem. Celem było umożliwienie wykonywania tego zdalnie, bez fizycznej obecności przy komputerze.

Dwoma z najwcześniejszych protokołów były Telnet i zdalne logowanie, odpowiednio z klientami `telnet`i `rlogin`[usługa ta nie jest dostępna w języku polskim]. Oba protokoły umożliwiały logowanie do systemu przez sieć, jednak żaden z nich nie koncentrował się na aspektach bezpieczeństwa. Poufność przesyłanego ruchu, a zwłaszcza danych logowania, nie była chroniona. Co więcej, integralność przesyłanego ruchu i wysyłanych poleceń nie była zagwarantowana. Innymi słowy, atakujący monitorujący sieć mógł łatwo odczytać dane logowania i zmodyfikować polecenia wysyłane przez sieć.

Poniższy zrzut ekranu został wykonany w programie Wireshark po użyciu funkcji „Follow TCP Stream” w sesji Telnet. Widzimy, jak użytkownik wpisuje swoją nazwę użytkownika `michael`i wkleja hasło `RJ9wn^t3T%gC`. Chociaż hasło jest bezpieczne według współczesnych standardów, jest ono przesyłane w postaci jawnego tekstu, który może odczytać każde poprawnie zlokalizowane oprogramowanie do przechwytywania pakietów sieciowych. Należy zauważyć, że na poniższym obrazku tekst w kolorze czerwonym jest wysyłany przez klienta Telnet, a tekst w kolorze niebieskim przez serwer Telnet.

![Zrzut ekranu przedstawiający ruch w postaci zwykłego tekstu przy użyciu protokołu takiego jak Telnet.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/98790dac90da302dc620fa46fc653985.png)

Protokół Secure Shell (SSH) zapewnił wymagania bezpieczeństwa, których brakowało w przypadku Telnetu i zdalnego logowania. DziękiSSH, atakujący nie będzie już mógł odczytać danych logowania ani zmodyfikować ruchu. Jeśli spróbujemy „Śledź”TCP„Stream” w Wireshark po przechwyceniu pakietów, nie otrzymamy żadnych informacji dotyczących nazwy użytkownika, hasła ani wydanych poleceń. Poniższy zrzut ekranu pokazuje, że jedynymi widocznymi informacjami są numery wersji i obsługiwane protokoły. (Należy pamiętać, że czerwone znaki są wysyłane przez klienta, a niebieskie przez serwer).

![Zrzut ekranu przedstawiający szyfrowany ruch przy użyciu protokołu SSH.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d0b6ca8ff1fd74de700084f166b27223.png)

### SSL/TLSProtokół

#### Przegląd techniczny - SSL/TLS

Protokół Secure Socket Layer (SSL) i Transport Layer Security (TLS) to protokoły używane do szyfrowania danych przesyłanych między klientem, takim jak przeglądarka internetowa, a serwerem. Rozważmy SSL/TLSjako opakowanie szyfrujące różne protokoły komunikacyjne, takie jakHTTPIFTP, aby utworzyć HTTPS i FTPS. SSL nie jest obecnie powszechnie używany, ponieważTLSstopniowo go zastępuje.

### SSL/TLSPrzepływ pracy

SSL/TLSUścisk dłoni jest wykonywany w celu zaszyfrowania komunikacji między klientem a serwerem poprzez następujące kroki:

1. Wiadomość powitalna klienta: Klient wysyła do serwera wiadomość powitalną, która zawiera:TLSwersja i zestaw szyfrów obsługiwany przez klienta, oprócz losowych bajtów.
2. Komunikat powitalny serwera: Serwer odpowiada komunikatem powitalnym, podświetlając swój certyfikat, wybrany zestaw szyfrów i losowe bajty.
3. Uwierzytelnianie: Klient uwierzytelnia certyfikat serwera za pośrednictwem urzędu certyfikacji, który go wydał. Na przykład, gdy odwiedzamy [Google(otwiera się w nowej karcie)](https://www.google.com/)Google udostępnia swój certyfikat. Otrzymany certyfikat jest weryfikowany przez naszą przeglądarkę, w której preinstalowane są certyfikaty różnych urzędów certyfikacji.
4. Premaster Secret: Klient szyfruje losowe bajty za pomocą klucza publicznego serwera. (Klient pobiera klucz publiczny z certyfikatu serwera.)
5. Deszyfrowanie pliku Premaster: Serwer odszyfrowuje plik Premaster za pomocą swojego klucza prywatnego.
6. Wygenerowane klucze sesji: Klient i serwer generują klucze sesji na podstawie losowych bajtów klienta, losowych bajtów serwera oraz klucza głównego. Obaj uzyskają ten sam wynik; **ten klucz sesji nie jest przesyłany** , a szyfrowanie i deszyfrowanie odbywa się na jego podstawie.
7. Wiadomości o gotowości: Klient i serwer wysyłają komunikat „zakończono” za pomocą klucza sesji, aby wskazać, że sesja jest gotowa do transmisji. Klient i serwer są teraz gotowi do wymiany wiadomości przez SSL/TLS.TLSszyfrowane połączenie.

![Rysunek przedstawiający uzgadnianie SSL/TLS](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f1a7e8eaf28b773aab4b5d3ae0f563b6.png)

TLSto wrapper szyfrujący komunikację protokołów komunikacyjnych. Zawiera numery portów dla różnych protokołów, takich jak 443 dla HTTPS i 990 dla FTPS.

### Protokół SOCKS5

#### Przegląd techniczny – SOCKS5

Socket Secure (SOCKS) topełnomocnikprotokół wymiany danych przez serwer delegatów (SOCKS5pełnomocnik). Służy do zabezpieczania protokołów warstwy aplikacji. Na przykład serwer Squid implementuje protokół SOCKS5 do przesyłania danych przezHTTPprotokół.

#### Przepływ pracy SOCKS5

Rozważmy scenariusz, w którym użytkownik A chce połączyć się z klientem B przez Internet, alezapora sieciowajest między nimi. Oto kroki uzgadniania:

- **Inicjacja klienta**
    - Klient A łączy się z SOCKS5pełnomocniki wysyła pierwszy bajt (0x05) dopełnomocnikgdzie „5” oznacza wersję SOCKS.
    - Klient A wysyła drugi bajt (0x01). Pierwszy oznacza, że ​​uwierzytelnianie jest obsługiwane.
    - Klient A wysyła trzeci bajt (0x00, 0x01, 0x02 lub 0x03). Bajty te oznaczają obsługiwane metody uwierzytelniania i mogą mieć różną długość.
- **SKARPETKI 5PełnomocnikOdpowiedź**
    - Tenpełnomocnikodsyła drugi bajt, który jest wybraną metodą uwierzytelniania przezpełnomocnikserwer.
    - Po pakiecie inicjującym klient A wysyła pakiet żądania, który zawiera numery BHOST i BPORT.
    - Udana sesja zostaje nawiązana pomiędzy klientem A apełnomocnikTe same kroki są podejmowane w przypadku skojarzenia klienta B zpełnomocnik.
- **Przesyłanie danych**
    - Po pomyślnym połączeniu obu klientów zpełnomocnikserwer, obaj klienci mogą wymieniać się danymi i udostępniać informacje, które będą przesyłane przezpełnomocnikserwer.

![Rysunek przedstawia klienta A łączącego się z serwerem proxy SOCKS5 i używającego go jako przekaźnika do łączenia się z klientem B.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/3814e1abc3946c5f256e5b9aa7eff893.png)

#### Korzyści z SOCKS5

- W komunikacji bezpośredniej za pośrednictwempełnomocnikserwer, ukrywa wewnętrzne szczegóły dotyczące routingu przez Internet.
- Apełnomocnikdziała jako serwer przekaźnikowy, omijając cenzurę internetową opartą na adresie IP klienta.

### IPsec

IPsec to skrót od Internet Protocol Security (bezpieczeństwo protokołu internetowego). W tym pomieszczeniu używamy IPsec w odniesieniu do IPsec-v3. IPsec zapewnia bezpieczeństwo poprzez dodanie uwierzytelniania i ochronęuczciwośći poufność ruchu sieciowego. IPsec wykorzystuje następujące protokoły:

1. Nagłówek uwierzytelniania (AH): zapewnia uwierzytelnianie iuczciwość.
2. Enkapsulacja ładunku zabezpieczającego (ESP): zapewnia uwierzytelnianie,uczciwośći poufności.
3. Security Association (SA): Odpowiada za negocjowanie kluczy i algorytmów szyfrowania. Jednym z przykładów jest Internet Key Exchange (IKE). Bardziej szczegółowe omówienie SA wykracza poza zakres tego forum.

W poniższych sekcjach omówimy AH i ESP bardziej szczegółowo.

#### Nagłówek uwierzytelniania (AH)

Nagłówek uwierzytelniania (AH): Protokół AH jest odpowiedzialny za uwierzytelnianie iuczciwośćruchu; nie może jednak chronić poufności danych.

Protokół AH działa w dwóch trybach, jak pokazano na poniższym rysunku:

1. Tryb transportu: Zapewnia uwierzytelnianie dlaTCP/UDPnagłówek i dane.
2. Tryb tunelowy: zapewnia uwierzytelnianie dla nagłówka IP,TCP/UDPnagłówek i dane.

![Rysunek przedstawiający nagłówek uwierzytelniania IPsec (AH) w trybie transportu i trybie tunelowania.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d33c96d4525b25694790be6ff0c31d8e.png)

Protokół AH jest odpowiedni, jeśli zapewnia uwierzytelnianie iuczciwośćwystarcza bez poufności. Warto wspomnieć, że AH jest opcjonalne w IPsec-v3, ale jego implementacja w IPsec-v2 jest obowiązkowa.

#### Enkapsulacja ładunku zabezpieczającego (ESP)

Enkapsulacja ładunku zabezpieczającego (ESP) zapewnia szyfrowanie oprócz uwierzytelniania iuczciwośćDziała w dwóch trybach:

1. Sposób transportu: Zapewnia bezpieczeństwo (poufność iuczciwość) dlaTCP/UDPnagłówek i dane.
2. Tryb tunelowy: zapewnia bezpieczeństwo (poufność iuczciwość) dla nagłówka IP,TCP/UDPnagłówek i dane.

![Rysunek przedstawiający protokół IPsec Encapsulating Security Payload (ESP) w trybie transportu i tunelowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f8c38bc132212830e305f2bf19185a55.png)

### VPN

KiedyTCP/Zaprojektowano protokół IP, wymagania bezpieczeństwa, takie jak poufność iuczciwośćNie były celem projektowym. Wręcz przeciwnie, dostępność była priorytetem, ponieważ jednym z celów Internetu jest przetrwanie ataku nuklearnego, o czym świadczy szybka adaptacja protokołów routingu w przypadku zerwania połączenia. Musimy jednak umożliwić korporacji wykorzystanie istniejącej infrastruktury internetowej do bezpiecznego połączenia swoich biur. Odpowiedź leży w skonfigurowaniuVPN.

Wirtualna sieć prywatna (VPN) umożliwia nawiązanie prywatnego połączenia przez sieć publiczną. Innymi słowy, możemy nawiązać bezpieczne połączenie przez niezabezpieczoną infrastrukturę.

Na przykład na poniższym rysunku możemy zobaczyć zdalne biuro i zdalnego użytkownika połączonego przezVPNdo biura głównego. AVPNpołączenie wymagaVPNklient iVPNserwer lub koncentrator. Cały ruch pomiędzyVPNklient i serwer są szyfrowane.

![Schemat sieci przedstawiający zdalne biuro i zdalnego użytkownika łączącego się z biurem głównym przez sieć VPN.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/898973f759258b860a457724055fae7b.png)

Dwa najczęściej stosowane protokoły do ​​ustanawianiaVPNpołączenia to:

1. IPsec
2. SSL/TLS

Protokół ESP IPsec to idealny protokół do konfigurowania bezpiecznych tuneli między różnymi sieciami lub komputerem a siecią. ESP może zapewnić bezpieczeństwo iuczciwośćwszystkich danych przesyłanych między dwoma punktami; co więcej, nawet adres IP może być ukryty w trybie tunelowym. Należy pamiętać, że system musi znajdować się zaVPNKoncentrator do ukrywania adresu IP. CiscoVPNsystemy oferują IPsec.

Chociaż protokół SSL został stworzony w celu zapewnienia bezpieczeństwaHTTPruch, SSL/TLSznalazł sposób na ustanowienie bezpiecznegoVPNpołączenia z OpenVPN. Korzystając z różnych narzędzi i bibliotek zbudowanych wokółTLSOpenVPN oferuje różne mechanizmy uwierzytelniania i szyfrowania w celu ustanowieniaVPNznajomości.

Niektóre starsze protokoły, które można wykorzystać do ustanowieniaVPNPołączenia nie są już uważane za bezpieczne. Przykładem jest protokół tunelowania punkt-punkt (PPTP), który nie jest już uważany za bezpieczny.

W tej sali omówiliśmy różne protokoły bezpieczeństwa sieci, niezbędne dla bezpieczeństwa przesyłanych danych. Najczęściej stosowanym mechanizmem zabezpieczania danych w niezabezpieczonym kanale jest dodanie protokołu  **SSL/TLS.TLSwrapper** , jak widzieliśmy w HTTPS, FTPS, POP3S i SMTPS. Protokoły bezpieczeństwa chronią przed atakami typu Man In the Middle (MITM), powtórki i ataki podsłuchowe.

Jeśli chcesz pogłębić swoją wiedzę na temat protokołów sieciowych i powiązanych z nimi kwestii bezpieczeństwa, zalecamy zapoznanie się z pokojem [poświęconym Wireshark](https://tryhackme.com/room/wireshark) .
