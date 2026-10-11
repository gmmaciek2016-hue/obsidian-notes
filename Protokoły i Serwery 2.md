---

W sali [protokołów i serwerów](https://tryhackme.com/room/protocolsandservers) omówiono wiele protokołów:

- Telnet
- HTTP
- FTP
- SMTP
- POP3
- IMAP

Serwery implementujące te protokoły są narażone na różnego rodzaju ataki. Aby wymienić tylko kilka, rozważmy:

1. Atak sniffingowy (przechwytywanie pakietów sieciowych)
2. Atak typu Man-in-the-Middle ( MITM )
3. Atak na hasło (atak uwierzytelniający)
4. Luki w zabezpieczeniach

Z perspektywy bezpieczeństwa zawsze musimy myśleć o tym, co chcemy chronić; rozważmy triadę bezpieczeństwa: poufność, integralność i dostępność ( CIA ). **Poufność** odnosi się do zachowania treści komunikacji dostępnej dla docelowych stron. **Integralność** to idea zapewnienia, że ​​wszelkie wysyłane dane są dokładne, spójne i kompletne po dotarciu do miejsca przeznaczenia. Wreszcie **dostępność** odnosi się do możliwości dostępu do usługi, gdy jej potrzebujemy. Różne strony będą kłaść różny nacisk na te trzy. Na przykład poufność będzie najwyższym priorytetem dla agencji wywiadowczych. Bankowość internetowa będzie kłaść największy nacisk na integralność transakcji. Dostępność ma najwyższe znaczenie dla każdej platformy zarabiającej na wyświetlaniu reklam.

Wiedząc, że chronimy poufność, integralność i dostępność ( CIA ), atak ma na celu ujawnienie, modyfikację i zniszczenie ( DAD ). Poniższe liczby to odzwierciedlają.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/992438a051d1355cf1146705557b457d.png)

Ataki te bezpośrednio wpływają na bezpieczeństwo systemu. Na przykład, przechwycenie pakietów sieciowych narusza poufność i prowadzi do ujawnienia informacji. Skuteczny atak na hasło również może prowadzić do ujawnienia. Z drugiej strony, atak typu Man-in-the-Middle ( MITM ) narusza integralność systemu, ponieważ może zmienić przesyłane dane. W tym pomieszczeniu skupimy się na tych trzech atakach, ponieważ są one integralną częścią projektu protokołu i implementacji serwera.

Luki w zabezpieczeniach obejmują szersze spektrum, a wykorzystywane luki mają różny wpływ na systemy docelowe. Na przykład, wykorzystanie luki typu Denial of Service ( DoS ) może wpłynąć na dostępność systemu, podczas gdy wykorzystanie luki typu Remote Code Execution ( RCE ) może prowadzić do poważniejszych szkód. Należy pamiętać, że luka sama w sobie stwarza ryzyko; szkody mogą wystąpić tylko w wyniku jej wykorzystania. Nie omawiamy luk w zabezpieczeniach w tym pomieszczeniu, ponieważ mają one swój własny moduł: [Vulnerability Research (Badania nad Lukami w Zabezpieczeniach)](https://tryhackme.com/module/vulnerability-research) .

W tej sali skupimy się na tym, jak można ulepszyć lub zastąpić protokół, aby chronić go przed ujawnieniem i modyfikacją, czyli chronić poufność i integralność przesyłanych danych. Będziemy rekomendować inne moduły, które obejmują dodatkowe tematy.

Ponadto wprowadzamy Hydrę , która ma za zadanie znajdowanie słabych haseł.

## Sniffing 

Atak typu sniffing polega na wykorzystaniu narzędzia do przechwytywania pakietów sieciowych w celu zebrania informacji o celu. Gdy protokół komunikuje się w postaci jawnego tekstu, wymieniane dane mogą zostać przechwycone przez osobę trzecią w celu analizy. Proste przechwycenie pakietów sieciowych może ujawnić informacje, takie jak treść prywatnych wiadomości i dane logowania, jeśli dane nie są szyfrowane w trakcie transmisji.

Atak typu sniffing można przeprowadzić za pomocą karty sieciowej Ethernet (802.3), pod warunkiem posiadania przez użytkownika odpowiednich uprawnień (uprawnień root w systemie Linux i uprawnień administratora w systemie MS Windows). Dostępnych jest wiele programów do przechwytywania pakietów sieciowych. Rozważymy następujące:

1. **Tcpdump** to darmowy program typu open source z interfejsem wiersza poleceń ( CLI ), który został przeniesiony do działania w wielu systemach operacyjnych.
2. **Wireshark to darmowy program z otwartym** kodem źródłowym , który jest dostępny dla wielu systemów operacyjnych, w tym Linux , macOS i MS Windows.
3. **Tshark**  jest alternatywą CLI dla Wiresharka.

Istnieje kilka specjalistycznych narzędzi umożliwiających przechwytywanie haseł, a nawet całych wiadomości. Można to jednak osiągnąć, wykonując pewne czynności, przy użyciu programów Tcpdump i Wireshark.

Rozważmy użytkownika sprawdzającego swoje wiadomości e-mail za pomocą protokołu POP3 . Najpierw użyjemy programu Tcpdump, aby spróbować przechwycić nazwę użytkownika i hasło. W poniższym wyniku terminala użyliśmy polecenia [tutaj brakuje kontekstu] `sudo tcpdump port 110 -A`. Zanim wyjaśnimy to polecenie, warto wspomnieć, że ten atak wymaga dostępu do ruchu sieciowego, na przykład poprzez podsłuch lub przełącznik z funkcją dublowania portów. Alternatywnie, możemy uzyskać dostęp do przesyłanego ruchu, przeprowadzając udany atak typu Man-in-the-Middle (MITM).

Potrzebujemy, `sudo`ponieważ przechwytywanie pakietów wymaga uprawnień roota. Chcieliśmy ograniczyć liczbę przechwytywanych i wyświetlanych pakietów do tych wymienianych z serwerem POP3. Wiemy, że POP3 korzysta z portu 110, więc filtrowaliśmy nasze pakiety za pomocą `port 110`. Na koniec chcieliśmy wyświetlić zawartość przechwyconych pakietów w formacie ASCII, więc dodaliśmy `-A`.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo tcpdump port 110 -A
[...]
09:05:15.132861 IP 10.20.30.1.58386 > 10.20.30.148.pop3: Flags [P.], seq 1:13, ack 19, win 502, options [nop,nop,TS val 423360697 ecr 3958275530], length 12
E..@.V@.@.g.
...
......n......"............
.;....}.USER frank

09:05:15.133465 IP 10.20.30.148.pop3 > 10.20.30.1.58386: Flags [.], ack 13, win 510, options [nop,nop,TS val 3958280553 ecr 423360697], length 0
E..4..@.@.O~
...
....n....".........?P.....
...i.;..
09:05:15.133610 IP 10.20.30.148.pop3 > 10.20.30.1.58386: Flags [P.], seq 19:43, ack 13, win 510, options [nop,nop,TS val 3958280553 ecr 423360697], length 24
E..L..@.@.Oe
...
....n....".........<-.....
...i.;..+OK Password required.

09:05:15.133660 IP 10.20.30.1.58386 > 10.20.30.148.pop3: Flags [.], ack 43, win 502, options [nop,nop,TS val 423360698 ecr 3958280553], length 0
E..4.W@.@.g.
...
......n......".....??.....
.;.....i
09:05:22.852695 IP 10.20.30.1.58386 > 10.20.30.148.pop3: Flags [P.], seq 13:28, ack 43, win 502, options [nop,nop,TS val 423368417 ecr 3958280553], length 15
E..C.X@.@.g.
...
......n......".....6......
.<.....iPASS D2xc9CgD
[...]
```

W powyższym wyjściu terminala usunęliśmy nieistotne pakiety, aby pomóc Ci skupić się na tych, które są istotne. W szczególności nazwa użytkownika i hasło zostały wysłane w osobnych pakietach. Pierwszy pakiet zawiera jawne wskazanie „USER frank”, a ostatni ujawnia hasło „PASS D2xc9CgD”.

Możemy również użyć Wiresharka, aby osiągnąć te same rezultaty. W poniższym oknie Wiresharka widzimy, że wprowadziliśmy dane `pop`w polu filtru. Teraz, gdy przefiltrowaliśmy tylko interesujący nas ruch, widzimy, że nazwa użytkownika i hasło zostały przechwycone.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/c1ec79277c1f02beeb20f7dc81df2fd3.png)

Krótko mówiąc, każdy protokół wykorzystujący komunikację jawną jest podatny na tego rodzaju atak. Jedynym warunkiem powodzenia tego ataku jest dostęp do systemu znajdującego się pomiędzy dwoma komunikującymi się systemami. Atak ten wymaga uwagi; zabezpieczenie polega na dodaniu warstwy szyfrującej do każdego protokołu sieciowego. W szczególności protokół Transport Layer Security ( TLS ) został dodany do protokołów HTTP , FTP , SMTP , POP3 , IMAP i wielu innych. W przypadku dostępu zdalnego Telnet został zastąpiony bezpieczną alternatywą, Secure Shell ( SSH ).

Jeśli chcesz dowiedzieć się więcej o narzędziu Wireshark, polecamy salę [Wireshark 101](https://tryhackme.com/room/wireshark) .

## MITM, Man-in-the-Middle

Atak typu Man-in-the-Middle ( MITM ) ma miejsce, gdy ofiara (A) wierzy, że komunikuje się z legalnym adresem (B), ale nieświadomie komunikuje się z atakującym (E). Na poniższym rysunku A żąda przelewu 20 USD do M; jednak E zmienił tę wiadomość i zastąpił oryginalną wartość nową. B otrzymał zmodyfikowaną wiadomość i podjął na jej podstawie odpowiednie działania.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/3cb0c4f9dde184bf8dcd6b3a45418a44.png)

Atak ten jest stosunkowo prosty do przeprowadzenia, jeśli obie strony nie potwierdzą autentyczności i integralności każdej wiadomości. W niektórych przypadkach wybrany protokół nie zapewnia bezpiecznego uwierzytelniania ani sprawdzania integralności; co więcej, niektóre protokoły mają wrodzone luki w zabezpieczeniach, które czynią je podatnymi na tego rodzaju ataki.

Za każdym razem, gdy przeglądasz strony przez HTTP , jesteś podatny na atak #MITM , a co gorsza, nie potrafisz go rozpoznać. Wiele narzędzi, takich jak [Ettercap](https://www.ettercap-project.org/) i [Bettercap](https://www.bettercap.org/) , pomoże Ci w przeprowadzeniu takiego ataku .

Ataki #MITM mogą również wpływać na inne protokoły tekstowe, takie jak FTP , SMTP i POP3 . Zapobieganie temu atakowi wymaga zastosowania kryptografii. Rozwiązaniem jest odpowiednie uwierzytelnianie oraz szyfrowanie lub podpisywanie wymienianych wiadomości. Dzięki infrastrukturze klucza publicznego ( PKI ) i zaufanym certyfikatom głównym, protokół Transport Layer Security ( TLS ) chroni przed atakami MITM .

## Zabezpieczenie warstwy transportowej TLS SSL

W tym zadaniu poznajemy standardowe rozwiązanie chroniące poufność i integralność wymienianych pakietów. Poniższe podejście może chronić przed podsłuchiwaniem haseł i atakami MITM .

Protokół #SSL (Secure Sockets Layer) pojawił się wraz z pojawieniem się w sieci WWW nowych zastosowań, takich jak zakupy online i przesyłanie danych płatniczych. Firma Netscape wprowadziła protokół SSL w 1994 roku, a wersja SSL 3.0 została wydana w 1996 roku. Ostatecznie jednak zapotrzebowanie na większe bezpieczeństwo wzrosło, dlatego w 1999 roku wprowadzono protokół TLS (Transport Layer Security). Zanim wyjaśnimy, co oferują protokoły #TLS i #SSL, zobaczmy, jak wpisują się one w model sieciowy.

Omawiane dotychczas popularne protokoły przesyłają dane w postaci jawnego tekstu, co umożliwia każdemu użytkownikowi sieci przechwytywanie, zapisywanie i analizowanie wymienianych wiadomości. Poniższy rysunek przedstawia warstwy sieciowe ISO/OSI. Protokoły, które omówiliśmy dotychczas w tej sali, znajdują się w warstwie aplikacji. Rozważmy model ISO/OSI; możemy dodać szyfrowanie do naszych protokołów poprzez warstwę prezentacji. W rezultacie dane będą prezentowane w formacie zaszyfrowanym (szyfrowanym), a nie w oryginalnej formie.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/9d265987c58331f6fd2f664837f85380.png)

Ze względu na ścisły związek między protokołami SSL i TLS , jeden z nich może być używany zamiast drugiego. Jednak TLS jest bezpieczniejszy niż SSL i praktycznie zastąpił SSL. Moglibyśmy pominąć SSL i napisać TLS zamiast SSL/ TLS , ale nadal będziemy o nich wspominać, aby uniknąć niejasności, ponieważ termin SSL jest nadal powszechnie używany. Można się jednak spodziewać, że wszystkie nowoczesne serwery będą korzystać z TLS .

Istniejący protokół tekstowy można zaktualizować, aby korzystał z szyfrowania SSL/ TLS . Możemy użyć TLS do aktualizacji protokołów HTTP , FTP , SMTP , POP3 i IMAP , żeby wymienić tylko kilka. Poniższa tabela zawiera listę protokołów, które omówiliśmy, oraz ich domyślne porty przed i po aktualizacji szyfrowania SSL/ TLS . Lista nie jest wyczerpująca, jednak ma na celu pomóc nam lepiej zrozumieć ten proces.

|Protokół|Domyślny port|Protokół zabezpieczony|Domyślny port z TLS|
|---|---|---|---|
|HTTP|80|HTTPS|443|
|FTP|21|FTPS|990|
|SMTP|25|SMTP|465|
|POP3|110|POP3S|995|
|IMAP|143|IMAPS|993|

Rozważmy przypadek protokołu HTTP . Początkowo, aby pobrać stronę internetową przez protokół HTTP , przeglądarka internetowa musiałaby wykonać co najmniej dwa następujące kroki:

1. Nawiąż połączenie TCP ze zdalnym serwerem internetowym
2. Wysyłaj żądania HTTP do serwera WWW, takie jak żądania `GET`i .`POST`

Protokół HTTPS wymaga dodatkowego kroku w celu zaszyfrowania ruchu. Ten nowy krok ma miejsce po nawiązaniu połączenia TCP , a przed wysłaniem żądań HTTP . Ten dodatkowy krok można wywnioskować z modelu ISO/OSI na zaprezentowanym wcześniej rysunku. W związku z tym protokół HTTPS wymaga co najmniej trzech następujących kroków:

1. Nawiąż połączenie TCP
2. **Nawiąż połączenie SSL/ TLS**
3. Wysyłaj żądania HTTP do serwera WWW

Aby nawiązać połączenie SSL/ TLS , klient musi wykonać odpowiednie nawiązanie połączenia z serwerem. Zgodnie z [RFC 6101](https://datatracker.ietf.org/doc/html/rfc6101) , nawiązanie połączenia SSL będzie wyglądać jak na poniższym rysunku.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/ea654470ae699d10e9c07bd11a8320ac.png)

Po nawiązaniu połączenia TCP z serwerem, klient nawiązuje połączenie SSL/ TLS , jak pokazano na powyższym rysunku. Terminy mogą wydawać się skomplikowane, w zależności od wiedzy z zakresu kryptografii, ale możemy uprościć te cztery kroki w następujący sposób:

1. Klient wysyła do serwera komunikat ClientHello, aby wskazać jego możliwości, takie jak obsługiwane algorytmy.
2. Serwer odpowiada komunikatem ServerHello, wskazując wybrane parametry połączenia. Serwer udostępnia swój certyfikat, jeśli wymagane jest uwierzytelnienie serwera. Certyfikat jest plikiem cyfrowym służącym do jego identyfikacji; zazwyczaj jest on podpisany cyfrowo przez osobę trzecią. Ponadto, przed wysłaniem komunikatu ServerHelloDone, serwer może wysłać dodatkowe informacje niezbędne do wygenerowania klucza głównego w komunikacie ServerKeyExchange, aby potwierdzić zakończenie negocjacji.
3. Klient odpowiada komunikatem ClientKeyExchange, który zawiera dodatkowe informacje niezbędne do wygenerowania klucza głównego. Ponadto przełącza się na szyfrowanie i informuje serwer za pomocą komunikatu ChangeCipherSpec.
4. Serwer również przełącza się na szyfrowanie i informuje o tym klienta w komunikacie ChangeCipherSpec.

Jeśli to nadal brzmi skomplikowanie, nie martw się; potrzebujemy tylko sedna sprawy. Klient był w stanie uzgodnić klucz tajny z serwerem posiadającym certyfikat publiczny. Ten klucz tajny został wygenerowany w bezpieczny sposób, aby osoba trzecia monitorująca kanał nie mogła go odkryć. Dalsza komunikacja między klientem a serwerem będzie szyfrowana za pomocą wygenerowanego klucza.

W rezultacie, po nawiązaniu połączenia SSL/ TLS , żądania HTTP i wymieniane dane nie będą dostępne dla nikogo obserwującego kanał komunikacji.

Na koniec, aby protokół SSL/ TLS był skuteczny, zwłaszcza podczas przeglądania stron internetowych przez HTTPS, polegamy na certyfikatach publicznych podpisanych przez urzędy certyfikacji, którym ufają nasze systemy. Innymi słowy, gdy przeglądamy [TryHackMe](https://tryhackme.com/) przez HTTPS, nasza przeglądarka oczekuje, że serwer TryHackMe dostarczy podpisany certyfikat od zaufanego urzędu certyfikacji, jak w poniższym przykładzie. W ten sposób nasza przeglądarka ma pewność, że komunikuje się z właściwym serwerem, co uniemożliwia przeprowadzenie ataku MITM .

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/2362c08e3a718863a1b1b56279931538.png)  

Na powyższym rysunku możemy zobaczyć następujące informacje:

1. Komu wydawany jest certyfikat? To nazwa firmy, która będzie go używać.
2. Kto wydał certyfikat? Jest to urząd certyfikacji, który wydał ten certyfikat.
3. Okres ważności. Na przykład nie chcesz używać certyfikatu, który wygasł.

Na szczęście nie musimy ręcznie sprawdzać certyfikatu dla każdej odwiedzanej strony; zrobi to za nas nasza przeglądarka internetowa. Dzięki certyfikatowi serwera przeglądarka upewni się, że komunikujemy się z właściwym serwerem i że nasza komunikacja jest bezpieczna.

Odpowiedz na poniższe pytania

DNS można również zabezpieczyć za pomocą TLS. Jaki jest trzyliterowy akronim protokołu DNS wykorzystującego TLS?  DoT

## Bezpieczna powłoka SSH

Protokół Secure Shell ( SSH ) został stworzony, aby zapewnić bezpieczny sposób zdalnego administrowania systemami. Innymi słowy, umożliwia on bezpieczne łączenie się z innym systemem przez sieć i wykonywanie poleceń w systemie zdalnym. Mówiąc prościej, „S” w #SSH oznacza „secure”, co można podsumować w następujący sposób:

1. Możesz potwierdzić tożsamość zdalnego serwera
2. Wymieniane wiadomości są szyfrowane i mogą zostać odszyfrowane tylko przez odbiorcę
3. Obie strony mogą wykryć wszelkie modyfikacje w wiadomościach

Powyższe trzy punkty są gwarantowane przez kryptografię. Mówiąc bardziej technicznie, stanowią one element poufności i integralności, możliwe dzięki odpowiedniemu wykorzystaniu różnych algorytmów szyfrowania.

Aby korzystać z protokołu SSH , potrzebny jest serwer SSH i klient SSH . Serwer SSH domyślnie nasłuchuje na porcie 22. Klient #SSH może uwierzytelnić się za pomocą:

- Nazwa użytkownika i hasło
- Klucz prywatny i publiczny (po skonfigurowaniu serwera SSH w celu rozpoznania odpowiadającego mu klucza publicznego)

W systemach Linux , macOS i MS Windows po 2018 roku można połączyć się z serwerem SSH za pomocą poniższego polecenia `ssh username@MACHINE_IP`. To polecenie spróbuje połączyć się z serwerem o adresie IP `MACHINE_IP`i nazwie użytkownika `username`. Jeśli serwer SSH nasłuchuje na domyślnym porcie, poprosi o podanie hasła `username`. Po uwierzytelnieniu użytkownik uzyska dostęp do terminala serwera docelowego. Poniższy wynik terminala przedstawia przykład użycia SSH do uzyskania dostępu do serwera Debian Linux.

Terminal

```shell-session
user@TryHackMe$ ssh mark@MACHINE_IP
mark@MACHINE_IP's password: XBtc49AB

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Sep 20 13:53:17 2021
mark@debian8:~$ 
```

W powyższym przykładzie wydaliśmy polecenie `ssh mark@MACHINE_IP`. Następnie, po wpisaniu poprawnego hasła, uzyskaliśmy dostęp do terminala systemu zdalnego. Protokół SSH jest bardzo niezawodny w przypadku administracji zdalnej, ponieważ nasza nazwa użytkownika i hasło zostały przesłane w postaci zaszyfrowanej; co więcej, wszystkie polecenia wykonywane w systemie zdalnym będą przesyłane zaszyfrowanym kanałem.

Należy pamiętać, że jeśli łączymy się z tym systemem po raz pierwszy, będziemy musieli potwierdzić odcisk palca klucza publicznego serwera SSH , aby uniknąć ataków typu man-in-the-middle (MITM). Jak wyjaśniono wcześniej, MITM ma miejsce, gdy strona atakująca, E, znajduje się między A i B i komunikuje się z A, podszywając się pod B, a następnie z B, podszywając się pod A, podczas gdy A i B myślą, że komunikują się bezpośrednio ze sobą. W przypadku SSH zazwyczaj nie mamy osoby trzeciej, która sprawdziłaby poprawność klucza publicznego, więc musimy to zrobić ręcznie. Ten atak pokazano na poniższym obrazku.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/fb2eb64abf54ed721dd55486d283b297.png)

Możemy użyć SSH do przesyłania plików za pomocą protokołu SCP (Secure Copy Protocol) opartego na protokole SSH . Przykładowa składnia wygląda następująco: `scp mark@MACHINE_IP:/home/mark/archive.tar.gz ~`To polecenie skopiuje plik o nazwie `archive.tar.gz`ze zdalnego systemu znajdującego się w `/home/mark`katalogu do katalogu głównego `~`, tj. do katalogu domowego aktualnie zalogowanego użytkownika.

Innym przykładem składni jest `scp backup.tar.bz2 mark@MACHINE_IP:/home/mark/`. To polecenie skopiuje plik `backup.tar.bz2`z systemu lokalnego do katalogu  `/home/mark/`w systemie zdalnym.

Terminal

```shell-session
user@TryHackMe$ scp document.txt mark@MACHINE_IP:/home/mark
mark@MACHINE_IP's password: 
document.txt                                        100% 1997KB  70.4MB/s   00:00
```

Na zakończenie warto dodać, że FTP można zabezpieczyć protokołem SSL/ TLS , wykorzystując protokół FTPS, który wykorzystuje port 990. Warto również wspomnieć, że FTP można zabezpieczyć również protokołem SSH , czyli SFTP. Domyślnie usługa ta nasłuchuje na porcie 22, podobnie jak SSH .

## Atak na Hasło

Omówiliśmy przechwytywanie pakietów sieciowych i ataki MITM , a także sposoby przeciwdziałania tym atakom za pomocą protokołów TLS i SSH . Trzecim rodzajem ataku, który omówimy w tej sali, jest atak na hasła.

Wiele protokołów wymaga uwierzytelnienia. Uwierzytelnienie polega na potwierdzeniu tożsamości. Korzystając z protokołów takich jak POP3 , nie powinniśmy uzyskiwać dostępu do skrzynki pocztowej przed zweryfikowaniem naszej tożsamości. Przykład POP3 z sali [„Protokoły i serwery”](https://tryhackme.com/room/protocolsandservers) został powtórzony poniżej dla ułatwienia. W tym przykładzie jesteśmy identyfikowani jako użytkownik frank, a serwer uwierzytelnił nas, ponieważ podaliśmy prawidłowe hasło. Innymi słowy, hasło jest jednym ze sposobów uwierzytelnienia.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet 10.129.176.19 110
Trying 10.129.176.19...
Connected to 10.129.176.19.
Escape character is '^]'.
+OK 10.129.176.19 Mail Server POP3 Wed, 15 Sep 2021 11:05:34 +0300 
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
+OK 10.129.176.19 closing connection
Connection closed by foreign host.
```

Uwierzytelnienie lub potwierdzenie swojej tożsamości można uzyskać za pomocą jednej z poniższych metod lub ich kombinacji:

1. Coś, co _znasz_ , na przykład hasło i kod PIN.
2. Coś , co _posiadasz_ , np. karta SIM, karta RFID i klucz sprzętowy USB.
3. Coś, czym _jesteś_ , na przykład odcisk palca i tęczówka.

To zadanie będzie koncentrować się na atakach na hasła, czyli na coś, co cel _zna_ . Jeśli przeanalizujemy komunikację z kilkoma poprzednimi serwerami za pomocą protokołów takich jak Telnet, SSH, POP3 i IMAP, zawsze będziemy potrzebować hasła, aby uzyskać dostęp. Na podstawie 150 milionów nazw użytkowników i haseł wyciekłych w wyniku włamania do systemu Adobe w 2013 roku, dziesięć najpopularniejszych haseł to:

- 123456
- 123456789
- hasło
- adobe123
- 12345678
- qwerty
- 1234567
- 111111
- Photoshop
- 123123

Tylko dwa hasła są powiązane z firmą Adobe i jej produktami, ale reszta jest ogólna. Można by pomyśleć, że to się zmieniło w ciągu ostatniej dekady; jednak 123456, 1234567, 12345678 i 123456789 nadal są popularnymi hasłami dla wielu użytkowników. Inni jeszcze nie zdają sobie sprawy, że qwerty nie jest tajne i jest używane przez wielu jako hasło.

Ataki na hasła przeprowadzane są zazwyczaj poprzez:

1. Odgadywanie hasła: Aby odgadnąć hasło, potrzebna jest pewna wiedza o adresacie, na przykład imię jego zwierzaka lub rok urodzenia.
2. Atak słownikowy: Podejście to rozszerza metodę zgadywania haseł i próbuje uwzględnić wszystkie prawidłowe słowa w słowniku lub na liście słów.
3. Atak siłowy: Jest to najbardziej wyczerpujący i czasochłonny atak, w którym atakujący może posunąć się aż do wypróbowania wszystkich możliwych kombinacji znaków. Liczba kombinacji szybko rośnie (wykładniczo wraz z liczbą znaków).

Skupmy się na atakach słownikowych. Z biegiem czasu hakerzy tworzyli listy zawierające hasła wyciekłe z wycieków danych. Jednym z przykładów jest lista wykradzionych haseł RockYou, którą można znaleźć w AttackBox pod adresem [brakuje kontekstu] `/usr/share/wordlists/rockyou.txt`. Wybór listy słów powinien zależeć od znajomości celu. Na przykład, użytkownik francuski może użyć francuskiego słowa zamiast angielskiego. W związku z tym, francuska lista słów może być bardziej obiecująca.

Potrzebujemy zautomatyzowanego sposobu sprawdzania popularnych haseł lub wpisów z listy słów – oto [THC Hydra](https://github.com/vanhauser-thc/thc-hydra) . Hydra obsługuje wiele protokołów, w tym FTP, POP3, IMAP , SMTP, SSH i wszystkie metody związane z HTTP. Ogólna składnia wiersza poleceń wygląda `hydra -l username -P wordlist.txt server service`następująco:

- `-l username`: `-l`powinien poprzedzać `username`, tj. nazwę logowania celu.
- `-P wordlist.txt`: `-P`poprzedza `wordlist.txt`plik, który jest plikiem tekstowym zawierającym listę haseł, które chcesz wypróbować przy użyciu podanej nazwy użytkownika.
- `server`jest nazwą hosta lub adresem IP serwera docelowego.
- `service`wskazuje usługę, na której próbujesz przeprowadzić atak słownikowy.

Rozważmy następujące konkretne przykłady:

- `hydra -l mark -P /usr/share/wordlists/rockyou.txt 10.129.176.19 ftp`będzie używana `mark`jako nazwa użytkownika podczas sprawdzania podanych haseł na serwerze FTP.
- `hydra -l mark -P /usr/share/wordlists/rockyou.txt ftp://10.129.176.19`jest identyczny jak w poprzednim przykładzie. `10.129.176.19 ftp`jest taki sam jak `ftp://10.129.176.19`.
- `hydra -l frank -P /usr/share/wordlists/rockyou.txt 10.129.176.19 ssh`będzie używana `frank`jako nazwa użytkownika podczas próby logowania się przez SSH przy użyciu różnych haseł.

Możesz dodać kilka dodatkowych, opcjonalnych argumentów:

- `-s PORT`aby określić port inny niż domyślny dla danej usługi.
- `-V`lub `-vV`, dla trybu verbose, powoduje, że #Hydra wyświetla kombinacje nazwy użytkownika i hasła, które są sprawdzane. Ta szczegółowość jest bardzo wygodna do śledzenia postępów, zwłaszcza jeśli nadal nie jesteś pewny składni wiersza poleceń.
- `-t n`gdzie n jest liczbą równoległych połączeń z celem. `-t 16`utworzy 16 wątków używanych do łączenia się z celem.
- `-d`, do debugowania, aby uzyskać bardziej szczegółowe informacje o tym, co się dzieje. Dane wyjściowe debugowania mogą zaoszczędzić Ci frustracji; na przykład, jeśli Hydra spróbuje połączyć się z zamkniętym portem i nastąpi przekroczenie limitu czasu, `-d`natychmiast to ujawni.

Po znalezieniu hasła możesz wydać polecenie `CTRL-C`zakończenia procesu. W zadaniach TryHackMe spodziewamy się, że każdy atak zakończy się w czasie krótszym niż pięć minut; jednak w rzeczywistych sytuacjach atak zazwyczaj trwa dłużej. Opcje wyświetlania szczegółów lub debugowania mogą być bardzo pomocne, jeśli chcesz, aby Hydra informowała Cię o postępach.

Podsumowując, ataki na systemy logowania można skutecznie przeprowadzić za pomocą narzędzia takiego jak THC Hydra w połączeniu z odpowiednią listą słów kluczowych. Zapobieganie takim atakom może być zaawansowane i zależy od systemu docelowego. Oto kilka z podejść:

- Zasady dotyczące haseł: Egzekwują ograniczenia minimalnej złożoności haseł ustawianych przez użytkownika.
- Blokada konta: Blokuje konto po określonej liczbie nieudanych prób.
- Ograniczanie prób uwierzytelnienia: Opóźnia odpowiedź na próbę logowania. Kilka sekund opóźnienia jest do przyjęcia dla osoby znającej hasło, ale może poważnie utrudnić działanie narzędzi automatycznych.
- Korzystanie z CAPTCHA: Wymaga rozwiązania pytania trudnego dla maszyn. Działa dobrze, jeśli strona logowania jest dostępna za pośrednictwem graficznego interfejsu użytkownika ( GUI ). (Należy pamiętać, że CAPTCHA to skrót od Completely Automated Public Turing test to tell Computers and Humans Apart, czyli Całkowicie Zautomatyzowany Publiczny Test Turinga Odróżniający Komputery od Ludzi).
- Wymaganie użycia certyfikatu publicznego do uwierzytelnienia. To podejście dobrze sprawdza się na przykład w przypadku protokołu SSH .
- Uwierzytelnianie dwuskładnikowe: Poproś użytkownika o podanie kodu, który można uzyskać również za pośrednictwem poczty e-mail, aplikacji na smartfonie lub SMS-a.
- Istnieje wiele innych podejść, które są bardziej zaawansowane lub mogą wymagać pewnej wiedzy na temat użytkownika, jak np. geolokalizacja oparta na adresie IP.

Doskonałym sposobem na ochronę przed atakami na hasła jest wykorzystanie kombinacji powyższych podejść.

Odpowiedz na poniższe pytania

Dowiedzieliśmy się, że jednym z kont e-mail jest  `lazie`… Jakie jest hasło do usługi IMAP na 10.129.176.19?
## Podsumowanie

W tym pokoju omówiono różne protokoły, ich zastosowanie i sposób działania. Trzy najczęstsze ataki to:

1. Atak węszenia
2. Atak MITM
3. Atak na hasło

W każdym z powyższych przypadków skupiliśmy się zarówno na szczegółach ataku, jak i na krokach zapobiegawczych.

Można przeprowadzić wiele innych ataków na określone serwery i protokoły. Przedstawimy listę kilku powiązanych modułów.

- [Badania luk w zabezpieczeniach](https://tryhackme.com/module/vulnerability-research) : W tym module można znaleźć więcej informacji o lukach i wykorzystaniu luk w zabezpieczeniach.
- [Metasploit](https://tryhackme.com/module/metasploit) : W tym module dowiesz się, jak używać #Metasploit do wykorzystywania ataków na systemy docelowe.
- [Burp Suite](https://tryhackme.com/module/learn-burp-suite) : W tym module dowiesz się, jak używać #Burp #Suite do przechwytywania ruchu HTTP i uruchamiania ataków związanych z siecią.

Warto zapamiętać domyślny numer portu dla popularnych protokołów. Dla wygody omówione przez nas usługi zostały wymienione w poniższej tabeli, posortowane alfabetycznie.

|Protokół|Port TCP|Aplikacja(e)|Bezpieczeństwo danych|
|---|---|---|---|
|FTP|21|Przesyłanie plików|Tekst jawny|
|FTPS|990|Przesyłanie plików|Zaszyfrowane|
|HTTP|80|Światowa sieć|Tekst jawny|
|HTTPS|443|Światowa sieć|Zaszyfrowane|
|IMAP|143|E-mail ( MDA )|Tekst jawny|
|IMAPS|993|E-mail ( MDA )|Zaszyfrowane|
|POP3|110|E-mail ( MDA )|Tekst jawny|
|POP3S|995|E-mail ( MDA )|Zaszyfrowane|
|SFTP|22|Przesyłanie plików|Zaszyfrowane|
|SSH|22|Zdalny dostęp i przesyłanie plików|Zaszyfrowane|
|SMTP|25|E-mail ( MTA )|Tekst jawny|
|SMTP|465|E-mail ( MTA )|Zaszyfrowane|
|Telnet|23|Zdalny dostęp|Tekst jawny|

Hydra pozostaje bardzo wydajnym narzędziem, które można uruchomić z terminala, aby wypróbować różne hasła. Podsumowujemy jego główne opcje w poniższej tabeli.

|Opcja|Wyjaśnienie|
|---|---|
|`-l username`|Podaj nazwę logowania|
|`-P WordList.txt`|Określ listę haseł, której chcesz użyć|
|`server service`|Ustaw adres serwera i usługę do ataku|
|`-s PORT`|Użyj w przypadku numeru portu usługi innego niż domyślny|
|`-V`Lub`-vV`|Pokaż kombinacje nazwy użytkownika i hasła, które są testowane|
|`-d`|Wyświetl dane wyjściowe debugowania, jeśli szczegółowe dane wyjściowe nie pomagają|
