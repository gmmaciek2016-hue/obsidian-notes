---

W tym pokoju użytkownik zapoznaje się z kilkoma powszechnie stosowanymi protokołami, takimi jak:

- HTTP
- FTP
- POP3
- SMTP
- IMAP

Każde zadanie dotyczące każdego protokołu zostanie zaprojektowane tak, aby pomóc nam zrozumieć, co dzieje się na niskim poziomie i co zazwyczaj jest ukryte pod eleganckim GUI (Graphical User Interface). Będziemy „omawiać” powyższe protokoły, korzystając z prostego klienta Telnet, aby w pełni zrozumieć, co klient GUI robi „pod maską”. Naszym celem nie jest zapamiętywanie poleceń protokołu, ale raczej bliższe przyjrzenie się protokołowi w trakcie jego działania.

Omawiamy również niektóre zagrożenia. W szczególności skupiamy się na hasłach przesyłanych w postaci jawnego tekstu.

## Telnet

Protokół Telnet to protokół warstwy aplikacji służący do łączenia się z terminalem wirtualnym innego komputera. Za pomocą #Telnetu użytkownik może zalogować się do innego komputera i uzyskać dostęp do jego terminala (konsoli), aby uruchamiać programy, uruchamiać procesy wsadowe i zdalnie wykonywać zadania administracyjne systemu.

Protokół Telnet jest stosunkowo prosty. Po połączeniu użytkownik zostanie poproszony o podanie nazwy użytkownika i hasła. Po poprawnym uwierzytelnieniu uzyska dostęp do terminala zdalnego systemu. Niestety, cała komunikacja między klientem Telnet a serwerem Telnet nie jest szyfrowana, co czyni go łatwym celem dla atakujących.

Serwer Telnet używa protokołu Telnet do nasłuchiwania połączeń przychodzących na porcie 23. (Należy pamiętać, że port Telnet nie jest otwarty na docelowej maszynie wirtualnej ). Rozważmy poniższy przykład. Użytkownik łączy się z `telnetd`serwerem Telnet. Kroki są następujące:

1. Najpierw użytkownik zostaje poproszony o podanie nazwy użytkownika (login). Widzimy, jak użytkownik wpisuje `frank`.
2. Następnie zostanie poproszony o podanie hasła `D2xc9CgD`. Hasło nie jest wyświetlane na ekranie, jednak wyświetlamy je poniżej w celach demonstracyjnych.
3. Po sprawdzeniu danych logowania przez system użytkownik zostanie powitany komunikatem powitalnym.
4. Zdalny serwer udostępnia mu wiersz poleceń `frank@bento:~$`. `$`Oznacza to, że nie jest to terminal root.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
Ubuntu 20.04.3 LTS
bento login: frank
Password: D2xc9CgD
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-84-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri 01 Oct 2021 12:24:56 PM UTC

  System load:  0.05              Processes:              243
  Usage of /:   45.7% of 6.53GB   Users logged in:        1
  Memory usage: 15%               IPv4 address for ens33: MACHINE_IP
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

0 updates can be applied immediately.

*** System restart required ***
Last login: Fri Oct  1 12:17:25 UTC 2021 from meiyo on pts/3
You have mail.
frank@bento:~$
```

Chociaż Telnet zapewnił nam dostęp do terminala zdalnego systemu w mgnieniu oka, nie jest to niezawodny protokół do zdalnej administracji, ponieważ wszystkie dane są przesyłane w postaci jawnego tekstu. Na poniższym rysunku przechwyciliśmy ruch generowany przez Telnet i znalezienie hasła było bardzo proste. Poniższy rysunek przedstawia dane ASCII wymieniane między naszym komputerem a systemem zdalnym. Tekst w kolorze czerwonym to tekst, który wysyłamy do systemu zdalnego, a tekst w kolorze niebieskim to tekst wysyłany przez system zdalny. Zwróć uwagę, jak nazwa użytkownika została odesłana (wyświetlona w naszym terminalu), ale hasło nie. Innymi słowy, jeśli ktoś obserwuje nas, jak wpisujemy, nie będzie mógł zobaczyć znaków hasła na ekranie.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/7102401bfd9313a5beb5e23ae93ff17f.png)

Telnet nie jest już uważany za bezpieczną opcję, zwłaszcza że każdy, kto przechwyci Twój ruch sieciowy, będzie mógł poznać Twoje nazwy użytkowników i hasła, co umożliwi mu dostęp do zdalnego systemu. Bezpieczną alternatywą jest SSH , które przedstawimy w następnym pomieszczeniu.

## HTTP

Protokół przesyłania hipertekstu ( HTTP ) to protokół używany do przesyłania stron internetowych. Przeglądarka internetowa łączy się z serwerem WWW i używa protokołu #HTTP do pobierania stron HTML i obrazów, a także innych plików, a także do przesyłania formularzy i plików. Za każdym razem, gdy przeglądasz sieć WWW, z pewnością korzystasz z protokołu #HTTP .

Poniższy obraz przedstawia klienta żądającego strony HTML `index.html`, którą udostępnia serwer WWW. Następnie klient żąda obrazu, `logo.jpg`który serwer WWW wysyła.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a23a13cef49ae7fff87bfd94f6a175dc.png)

Protokół HTTP wysyła i odbiera dane w postaci jawnego tekstu (nieszyfrowanego); dlatego można użyć prostego narzędzia, takiego jak Telnet (lub Netcat), aby komunikować się z serwerem WWW i działać jako „przeglądarka internetowa”. Kluczowa różnica polega na tym, że to Ty musisz wprowadzać polecenia związane z protokołem HTTP, a nie przeglądarka internetowa.

W poniższym przykładzie pokażemy, jak zażądać strony z serwera WWW; ponadto poznamy wersję serwera WWW. W tym celu użyjemy klienta Telnet. Wybraliśmy go, ponieważ Telnet jest prostym protokołem; ponadto wykorzystuje on tekst jawny do komunikacji. `telnet`Zamiast przeglądarki WWW użyjemy jej do zażądania pliku z serwera WWW. Kroki będą następujące:

1. Najpierw łączymy się z portem 80 za pomocą `telnet MACHINE_IP 80`.
2. Następnie musimy wpisać kod `GET /index.html HTTP/1.1`, aby pobrać stronę `index.html`lub `GET / HTTP/1.1`pobrać stronę domyślną.
3. Na koniec należy podać jakąś wartość dla hosta, np. nacisnąć **dwukrotnie**`host: telnet` klawisz Enter/Return .

W poniższym wyniku konsoli mogliśmy odzyskać żądaną stronę wraz z wieloma informacjami, które zazwyczaj nie są wyświetlane przez przeglądarkę internetową. Jeśli żądana strona nie zostanie znaleziona, pojawi się błąd 404.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP 80
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
GET /index.html HTTP/1.1
host: telnet

HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Wed, 15 Sep 2021 08:56:20 GMT
Content-Type: text/html
Content-Length: 234
Last-Modified: Wed, 15 Sep 2021 08:53:59 GMT
Connection: keep-alive
ETag: "6141b4a7-ea"
Accept-Ranges: bytes

<!DOCTYPE html>
<html lang="en">
<head>
  <title>Welcome to my Web Server</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
</head>
<body>
  <h1>Coming Soon<h1>
</body>
</html>
```

Szczególnie interesujące w powyższym wyniku jest to, że użytkownik musi wpisać tylko kilka poleceń, aby uzyskać potrzebną stronę, `GET /index.html HTTP/1.1`a następnie `host: telnet`.

Aby korzystać z protokołu HTTP , potrzebujemy serwera HTTP (serwera WWW) i klienta HTTP (przeglądarki WWW) . Serwer WWW „dostarczy” określony zestaw plików żądającej przeglądarce WWW.

Trzy popularne opcje serwerów HTTP to:

- [Apacz](https://www.apache.org/)
- [Usługi informacyjne Internetu ( IIS )](https://www.iis.net/)
- [nginx](https://nginx.org/)

Apache i Nginx to darmowe i otwarte oprogramowanie. Natomiast IIS to oprogramowanie o zamkniętym kodzie źródłowym, wymagające opłacenia licencji.

Dostępnych jest wiele przeglądarek internetowych. W chwili pisania tego tekstu najpopularniejsze to:

- Chrome od Google
- Edge firmy Microsoft
- Firefox firmy Mozilla
- Safari od Apple.

Przeglądarki internetowe można na ogół zainstalować i używać bezpłatnie, co więcej, giganci technologiczni toczą ze sobą walkę o większy udział w rynku swoich przeglądarek.

## Protokół transferu plików FTP

Protokół transferu plików ( FTP ) został opracowany w celu usprawnienia przesyłania plików pomiędzy różnymi komputerami wyposażonymi w różne systemy operacyjne.

FTP również wysyła i odbiera dane w postaci jawnego tekstu, dlatego możemy użyć Telnetu (lub Netcata) do komunikacji z serwerem FTP i działać jako klient #FTP . W poniższym przykładzie wykonaliśmy następujące kroki:

1. Połączyliśmy się z serwerem FTP za pomocą klienta Telnet. Ponieważ serwery FTP domyślnie nasłuchują na porcie 21, musieliśmy wskazać naszemu klientowi Telnet, aby próbował połączyć się z portem 21 zamiast z domyślnym portem Telnet.
2. Musieliśmy podać nazwę użytkownika w poleceniu `USER frank`.
3. Następnie podaliśmy hasło za pomocą polecenia `PASS D2xc9CgD`.
4. Udało nam się zalogować, ponieważ podaliśmy prawidłową nazwę użytkownika i hasło.

Polecenie takie jak „ `STAT`może dostarczyć dodatkowych informacji”. `SYST`Polecenie to pokazuje typ systemu docelowego (w tym przypadku UNIX). `PASV`Przełącza tryb na pasywny. Warto zauważyć, że FTP ma dwa tryby:

- Aktywny: W trybie aktywnym dane są przesyłane osobnym kanałem pochodzącym z portu 20 serwera FTP.
- Pasywny: W trybie pasywnym dane są przesyłane oddzielnym kanałem pochodzącym z portu klienta FTP o numerze powyżej portu 1023.

Polecenie `TYPE A`przełącza tryb przesyłania plików na ASCII, a `TYPE I`tryb przesyłania plików na binarny. Nie możemy jednak przesłać pliku za pomocą prostego klienta, takiego jak Telnet, ponieważ FTP tworzy osobne połączenie do przesyłania plików.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP 21
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
220 (vsFTPd 3.0.3)
USER frank
331 Please specify the password.
PASS D2xc9CgD
230 Login successful.
SYST
215 UNIX Type: L8
PASV
227 Entering Passive Mode (10,10,0,148,78,223).
TYPE A
200 Switching to ASCII mode.
STAT          
211-FTP server status:
     Connected to ::ffff:10.10.0.1
     Logged in as frank
     TYPE: ASCII
     No session bandwidth limit
     Session timeout in seconds is 300
     Control connection is plain text
     Data connections will be plain text
     At session startup, client count was 1
     vsFTPd 3.0.3 - secure, fast, stable
211 End of status
QUIT
221 Goodbye.
Connection closed by foreign host.
```

Poniższy rysunek pokazuje, jak wyglądałby rzeczywisty transfer plików za pomocą protokołu FTP . Aby uprościć ten rysunek, skupmy się tylko na tym, że klient FTP nawiąże połączenie z serwerem FTP , który domyślnie nasłuchuje na porcie 21. Wszystkie polecenia będą wysyłane kanałem sterującym. Gdy klient zażąda pliku, zostanie między nimi nawiązane kolejne połączenie TCP. (Szczegóły nawiązywania połączenia/kanału danych wykraczają poza zakres tego artykułu).

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/da71a52fddfbb268dc6c5857daf07f18.png)

Biorąc pod uwagę złożoność transferu danych przez FTP , użyjmy prawdziwego klienta FTP do pobrania pliku tekstowego. Do pobrania pliku potrzebowaliśmy tylko kilku poleceń. Po pomyślnym zalogowaniu pojawia się monit FTP`ftp>` , umożliwiający wykonanie różnych poleceń FTP`ls` . Najpierw wylistowaliśmy pliki i poznaliśmy ich nazwy; następnie przełączyliśmy się na [brakuje nazwy pliku], `ascii`ponieważ jest to plik tekstowy (nie binarny). Na koniec sprawiliśmy, `get FILENAME`że klient i serwer ustanowią kolejny kanał do transferu plików.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ ftp MACHINE_IP
Connected to MACHINE_IP.
220 (vsFTPd 3.0.3)
Name: frank
331 Please specify the password.
Password: D2xc9CgD
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
227 Entering Passive Mode (10,20,30,148,201,180).
150 Here comes the directory listing.
-rw-rw-r--    1 1001     1001         4006 Sep 15 10:27 README.txt
226 Directory send OK.
ftp> ascii
200 Switching to ASCII mode.
ftp> get README.txt
local: README.txt remote: README.txt
227 Entering Passive Mode (10,10,0,148,125,55).
150 Opening BINARY mode data connection for README.txt (4006 bytes).
WARNING! 9 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
4006 bytes received in 0.000269 secs (14892.19 Kbytes/sec)
ftp> exit
221 Goodbye.
```

Serwery FTP i klienci FTP korzystają z protokołu FTP . Istnieje wiele różnych programów serwerowych FTP , spośród których możesz wybrać, jeśli chcesz hostować swój serwer plików FTP . Przykłady oprogramowania serwera FTP obejmują:

- [vsftpd](https://security.appspot.com/vsftpd.html)
- [ProFTPD](http://www.proftpd.org/)
- [uFTP](https://www.uftpserver.com/)

W przypadku klientów FTP , oprócz konsoli FTP powszechnie dostępnej w systemach Linux , można skorzystać z klienta FTP z interfejsem graficznym , takiego jak [FileZilla](https://filezilla-project.org/) . Niektóre przeglądarki internetowe również obsługują protokół #FTP .

Ponieważ protokół FTP wysyła dane logowania wraz z poleceniami i plikami w postaci zwykłego tekstu, ruch FTP może być łatwym celem dla atakujących.

## Protokół SMTP

Poczta elektroniczna to jedna z najczęściej używanych usług w internecie. Istnieją różne konfiguracje serwerów pocztowych; na przykład można skonfigurować system pocztowy umożliwiający użytkownikom lokalnym wymianę wiadomości e-mail bez dostępu do internetu. Rozważymy jednak bardziej ogólną konfigurację, w której różne serwery pocztowe łączą się przez internet.

Do dostarczania wiadomości e-mail przez Internet wymagane są następujące elementy:

1. Agent przesyłania poczty (MSA)
2. Agent transferu poczty ( MTA )
3. Agent dostarczający pocztę ( MDA )
4. Agent użytkownika poczty ( MUA )

Powyższe cztery terminy mogą wydawać się zagadkowe, ale są bardziej oczywiste, niż się wydaje. Wyjaśnimy je na poniższym rysunku.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/822a449fd569c16c875a13ca2487b714.png)

Na rysunku przedstawiono pięć kroków, przez które musi przejść wiadomość e-mail, aby trafić do skrzynki odbiorczej odbiorcy:

1. Klient poczty elektronicznej ( MUA ) ma do wysłania wiadomość e-mail. MUA łączy się z agentem przesyłania poczty (MSA), aby wysłać wiadomość.
2. MSA odbiera wiadomość, sprawdza ją pod kątem ewentualnych błędów, a następnie przesyła do serwera Mail Transfer Agent ( MTA ), zazwyczaj znajdującego się na tym samym serwerze.
3. Agent MTA wyśle ​​wiadomość e-mail do agenta MTA odbiorcy. Agent MTA może również pełnić funkcję agenta przesyłania poczty (MSA).
4. Typowa konfiguracja zakłada, że ​​serwer MTA pełni również funkcję agenta dostarczającego pocztę ( MDA ).
5. Odbiorca będzie odbierał pocztę od MDA za pośrednictwem swojego klienta poczty elektronicznej.

Jeśli powyższe kroki wydają się mylące, rozważ następującą analogię:

1. Chcesz ( MUA ) wysłać pocztę.
2. Pracownik poczty (MSA) sprawdza przesyłkę pocztową pod kątem ewentualnych usterek przed jej przyjęciem przez lokalny urząd pocztowy ( MTA ).
3. Lokalny urząd pocztowy sprawdza adresata przesyłki i wysyła ją do urzędu pocztowego ( MTA ) we właściwym kraju.
4. Urząd pocztowy ( MTA ) dostarcza pocztę do skrzynki pocztowej adresata ( MDA ).
5. Odbiorca ( MUA ) regularnie sprawdza skrzynkę pocztową w poszukiwaniu nowej poczty. Zauważa nową pocztę i ją odbiera.

Podobnie, musimy przestrzegać protokołu, aby komunikować się z serwerem HTTP , i musimy polegać na protokołach poczty elektronicznej, aby komunikować się z MTA i MDA . Protokoły te to:

1. Protokół SMTP (Simple Mail Transfer Protocol )
2. Protokół pocztowy w wersji 3 ( POP3 ) lub protokół dostępu do wiadomości internetowych ( IMAP )

W tym zadaniu wyjaśnimy protokół SMTP , a w kolejnych dwóch zadaniach omówimy protokoły POP3 i IMAP .

Protokół SMTP (Simple Mail Transfer Protocol ) służy do komunikacji z serwerem MTA . Ponieważ SMTP wykorzystuje tekst jawny, w którym wszystkie polecenia są wysyłane bez szyfrowania, możemy użyć prostego klienta Telnet do połączenia się z serwerem SMTP i pełnienia funkcji klienta poczty elektronicznej ( MUA ) wysyłającego wiadomość.

Serwer SMTP domyślnie nasłuchuje na porcie 25. Aby zobaczyć podstawową komunikację z serwerem SMTP , połączyliśmy się z nim za pomocą Telnetu. Po nawiązaniu połączenia wysyłamy `helo hostname`i zaczynamy pisać wiadomość e-mail.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP 25
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
220 bento.localdomain ESMTP Postfix (Ubuntu)
helo telnet
250 bento.localdomain
mail from: 
250 2.1.0 Ok
rcpt to: 
250 2.1.5 Ok
data
354 End data with .
subject: Sending email with Telnet
Hello Frank,
I am just writing to say hi!             
.
250 2.0.0 Ok: queued as C3E7F45F06
quit
221 2.0.0 Bye
Connection closed by foreign host.
```

Po `helo`, wydajemy `mail from:`, `rcpt to:`aby wskazać nadawcę i odbiorcę. Wysyłając wiadomość e-mail, wydajemy polecenie `data`i wpisujemy treść. Wydajemy `<CR><LF>.<CR><LF>`(lub `Enter . Enter`mówiąc prościej). Serwer SMTP umieszcza teraz wiadomość w kolejce.

Ogólnie rzecz biorąc, nie musimy zapamiętywać poleceń SMTP . Powyższe dane wyjściowe konsoli mają na celu lepsze wyjaśnienie działania typowego klienta poczty podczas korzystania z protokołu SMTP .

## Protokół pocztowy POP3

Protokół pocztowy w wersji 3 ( #POP3 ) to protokół używany do pobierania wiadomości e-mail z serwera agenta dostarczania poczty ( MDA ), jak pokazano na poniższym rysunku. Klient poczty łączy się z serwerem POP3 , uwierzytelnia się, pobiera nowe wiadomości e-mail, a następnie (opcjonalnie) je usuwa.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/ed910ad418376edc846846fc2a0dd3f6.png)

Poniższy przykład pokazuje, jak wyglądałaby sesja POP3 przeprowadzona za pośrednictwem klienta Telnet. Najpierw użytkownik łączy się z serwerem POP3 na domyślnym porcie POP3 110. Aby uzyskać dostęp do wiadomości e-mail, wymagane jest uwierzytelnienie; użytkownik uwierzytelnia się, podając swoją nazwę użytkownika `USER frank`i hasło `PASS D2xc9CgD`. Używając polecenia `STAT`, otrzymujemy odpowiedź `+OK 1 179`; zgodnie z [RFC 1939](https://datatracker.ietf.org/doc/html/rfc1939) , pozytywna odpowiedź na `STAT`ma format `+OK nn mm`, gdzie _nn_ to liczba wiadomości e-mail w skrzynce odbiorczej, a _mm_ to rozmiar skrzynki odbiorczej w oktetach (bajtach). Polecenie `LIST`dostarczyło listę nowych wiadomości na serwerze i `RETR 1`pobrało pierwszą wiadomość z listy. Nie musimy zapamiętywać tych poleceń, jednak warto pogłębić naszą wiedzę na temat tego protokołu.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP 110
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
+OK MACHINE_IP Mail Server POP3 Wed, 15 Sep 2021 11:05:34 +0300 
USER frank
+OK frank
PASS D2xc9CgD
+OK 1 messages (179) octets
STAT
+OK 1 179
LIST
+OK 1 messages (179) octets
1 179
.
RETR 1
+OK
From: Mail Server 
To: Frank 
subject: Sending email with Telnet
Hello Frank,
I am just writing to say hi!
.
QUIT
+OK MACHINE_IP closing connection
Connection closed by foreign host.
```

Powyższy przykład pokazuje, że polecenia są wysyłane w postaci jawnego tekstu. Użycie Telnetu wystarczyło do uwierzytelnienia i pobrania wiadomości e-mail. Ponieważ nazwa użytkownika i hasło są wysyłane w postaci jawnego tekstu, każda osoba trzecia obserwująca ruch sieciowy może ukraść dane logowania.

Zasadniczo Twój klient poczty ( MUA ) połączy się z serwerem POP3 ( MDA ), uwierzytelni i pobierze wiadomości. Chociaż komunikacja za pomocą protokołu POP3 będzie ukryta za eleganckim interfejsem, zostaną wydane podobne polecenia, jak pokazano w sesji Telnet powyżej.

Zgodnie z ustawieniami domyślnymi, klient poczty usuwa wiadomość po jej pobraniu. Domyślne zachowanie można zmienić w ustawieniach klienta poczty, jeśli chcesz ponownie pobrać wiadomości e-mail z innego klienta poczty. Dostęp do tego samego konta pocztowego za pośrednictwem wielu klientów za pomocą protokołu POP3 zazwyczaj nie jest zbyt wygodny, ponieważ traci się kontrolę nad przeczytanymi i nieprzeczytanymi wiadomościami. Aby zapewnić synchronizację wszystkich skrzynek pocztowych, należy rozważyć inne protokoły, takie jak IMAP .

## Protokół dostępu do wiadomości IMAP

Protokół IMAP (Internet Message Access Protocol ) jest bardziej zaawansowany niż POP3 . Umożliwia on synchronizację poczty e-mail na wielu urządzeniach (i klientach pocztowych). Innymi słowy, jeśli oznaczysz wiadomość e-mail jako przeczytaną podczas sprawdzania poczty na smartfonie, zmiana zostanie zapisana na serwerze #IMAP ( MDA ) i zreplikowana na Twoim laptopie podczas synchronizacji skrzynki odbiorczej.

Przyjrzyjmy się przykładowym poleceniom IMAP . W poniższym wyniku konsoli używamy Telnetu do połączenia się z domyślnym portem serwera IMAP , a następnie uwierzytelniamy się za pomocą `LOGIN username password`. Protokół #IMAP wymaga, aby każde polecenie było poprzedzone losowym ciągiem znaków, aby móc śledzić odpowiedź. Dlatego dodaliśmy `c1`, then `c2`i tak dalej. Następnie wylistowaliśmy nasze foldery pocztowe za pomocą `LIST "" "*"`, a następnie sprawdziliśmy, czy w skrzynce odbiorczej są jakieś nowe wiadomości za pomocą `EXAMINE INBOX`. Nie musimy zapamiętywać tych poleceń; jednak poniższy przykład podajemy po prostu, aby dać jasny obraz tego, co się dzieje, gdy klient poczty komunikuje się z serwerem IMAP.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet 10.128.169.164 143
Trying 10.128.169.164...
Connected to 10.128.169.164.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 UIDPLUS CHILDREN NAMESPACE THREAD=ORDEREDSUBJECT THREAD=REFERENCES SORT QUOTA IDLE ACL ACL2=UNION STARTTLS ENABLE UTF8=ACCEPT] Courier-IMAP ready. Copyright 1998-2018 Double Precision, Inc.  See COPYING for distribution information.
c1 LOGIN frank D2xc9CgD
* OK [ALERT] Filesystem notification initialization error -- contact your mail administrator (check for configuration errors with the FAM/Gamin library)
c1 OK LOGIN Ok.
c2 LIST "" "*"
* LIST (\HasNoChildren) "." "INBOX.Trash"
* LIST (\HasNoChildren) "." "INBOX.Drafts"
* LIST (\HasNoChildren) "." "INBOX.Templates"
* LIST (\HasNoChildren) "." "INBOX.Sent"
* LIST (\Unmarked \HasChildren) "." "INBOX"
c2 OK LIST completed
c3 EXAMINE INBOX
* FLAGS (\Draft \Answered \Flagged \Deleted \Seen \Recent)
* OK [PERMANENTFLAGS ()] No permanent flags permitted
* 0 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 631694851] Ok
* OK [MYRIGHTS "acdilrsw"] ACL
c3 OK [READ-ONLY] Ok
c4 LOGOUT
* BYE Courier-IMAP server shutting down
c4 OK LOGOUT completed
Connection closed by foreign host.
```
## Podsumowanie

W tej sali omówiono różne protokoły, ich zastosowanie i sposób działania pod maską. Wiele innych standardowych protokołów jest interesujących dla atakujących. Na przykład protokół SMB (Server Message Block ) zapewnia współdzielony dostęp do plików i drukarek między sieciami i może być ciekawym celem. Jednak celem tej sali jest jedynie zapoznanie z kilkoma popularnymi protokołami i ich działaniem pod maską. Jedna sala, a nawet cały moduł, nie jest w stanie objąć wszystkich protokołów sieciowych.

Warto zapamiętać domyślny numer portu dla popularnych protokołów. Poniżej znajduje się podsumowanie omawianych protokołów, posortowane alfabetycznie, wraz z ich domyślnymi numerami portów.

|Protokół|Port TCP|Aplikacja(e)|Bezpieczeństwo danych|
|---|---|---|---|
|FTP|21|Przesyłanie plików|Tekst jawny|
|HTTP|80|Światowa sieć|Tekst jawny|
|IMAP|143|E-mail ( MDA )|Tekst jawny|
|POP3|110|E-mail ( MDA )|Tekst jawny|
|SMTP|25|E-mail ( MTA )|Tekst jawny|
|Telnet|23|Zdalny dostęp|Tekst jawny|

W następnej sali tego modułu poznamy różne rodzaje ataków na te protokoły i serwery oraz sposoby ich łagodzenia.
