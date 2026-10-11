---

Witamy w pierwszej sali modułu „Bezpieczeństwo sieci”. Ten moduł obejmuje:

1. [Rozpoznanie pasywne](https://tryhackme.com/room/passiverecon)
2. [Aktywny rozpoznanie](https://tryhackme.com/room/activerecon)
3. [Odkrywanie hosta Nmap Live](https://tryhackme.com/room/nmap01)
4. [Podstawowe skanowanie portów Nmap](https://tryhackme.com/room/nmap02)
5. [Zaawansowane skanowanie portów Nmap](https://tryhackme.com/room/nmap03)
6. [Nmap Post Port Scans](https://tryhackme.com/room/nmap04)
7. [Protokoły i serwery](https://tryhackme.com/room/protocolsandservers)
8. [Protokoły i serwery 2](https://tryhackme.com/room/protocolsandservers2)
9. [Wyzwanie bezpieczeństwa sieci](https://tryhackme.com/room/netsecchallenge)

W tej sali, po zdefiniowaniu rozpoznania pasywnego i aktywnego, skupimy się na podstawowych narzędziach związanych z rozpoznaniem pasywnym. Poznamy trzy narzędzia wiersza poleceń:

- `whois`do zapytań na serwerach #WHOIS
- `nslookup`do zapytań serwerów #DNS
- `dig`do zapytań serwerów #DNS

Do wyszukiwania rekordów WHOIS używamy `whois`funkcji `nslookup`oraz `dig`do wyszukiwania rekordów w bazie danych DNS . Wszystkie te rekordy są publicznie dostępne i dlatego nie generują alertów dla celu.

Nauczymy się również korzystać z dwóch usług online:

- DNSDumpster
- Shodan.io

Te dwie usługi online pozwalają nam zbierać informacje o naszym celu, bez konieczności bezpośredniego łączenia się z nim.

Wymagania wstępne: Ta sala wymaga podstawowej wiedzy z zakresu sieci oraz podstawowej znajomości wiersza poleceń. Moduły [„Podstawy sieci”](https://tryhackme.com/module/network-fundamentals) i [„Podstawy](https://tryhackme.com/module/linux-fundamentals) [systemu Linux”](https://tryhackme.com/module/linux-fundamentals) zapewniają niezbędną wiedzę, jeśli jest to konieczne.

Zanim narodziły się systemy komputerowe i sieci, Sun Tzu nauczał w „Sztuce wojny”: „Jeśli znasz wroga i znasz siebie, twoje zwycięstwo nie będzie wątpliwe”. Grając rolę atakującego, musisz zebrać informacje o swoich systemach docelowych. Grając rolę obrońcy, musisz wiedzieć, co przeciwnik odkryje na temat twoich systemów i sieci.

Rekonesans (recon) można zdefiniować jako wstępne badanie mające na celu zebranie informacji o celu. Jest to pierwszy krok w [Zjednoczonym Łańcuchu Zabójstw](https://www.unifiedkillchain.com/) , mający na celu uzyskanie wstępnego punktu zaczepienia w systemie. Rekonesans dzielimy na:

1. Rozpoznanie pasywne
2. Aktywny rozpoznanie

W rozpoznaniu pasywnym polegasz na wiedzy publicznie dostępnej. To wiedza, do której możesz uzyskać dostęp z publicznie dostępnych źródeł, bez bezpośredniego kontaktu z celem. Wyobraź sobie, że patrzysz na teren docelowy z daleka, nie wchodząc na niego.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/dbda3c79cc81408315a218749030256a.png)

Działania rozpoznania pasywnego obejmują wiele czynności, na przykład:

- Wyszukiwanie rekordów DNS domeny na publicznym serwerze DNS .
- Sprawdzanie ogłoszeń o pracę powiązanych z docelową stroną internetową.
- Czytanie artykułów prasowych na temat spółki docelowej.

Z drugiej strony, aktywnego rozpoznania nie da się przeprowadzić tak dyskretnie. Wymaga ono bezpośredniego kontaktu z celem. Wyobraź sobie, że sprawdzasz zamki w drzwiach i oknach, a także inne potencjalne punkty wejścia.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/cddef8bc0ee2d177a96ea62f680ad28f.png)

Przykłady aktywnych działań rozpoznawczych obejmują:

- Nawiązywanie połączenia z jednym z serwerów firmy, takim jak HTTP , FTP lub SMTP .
- Próba uzyskania informacji telefonicznie ( inżynieria społeczna ).
- Wchodzenie na teren firmy podając się za fachowca.

Biorąc pod uwagę inwazyjny charakter aktywnego rozpoznania, można łatwo popaść w kłopoty prawne, jeśli nie uzyska się odpowiedniego zezwolenia.

WHOIS to protokół żądań i odpowiedzi zgodny ze specyfikacją [RFC 3912.](https://www.ietf.org/rfc/rfc3912.txt) Serwer WHOIS nasłuchuje żądań przychodzących na porcie TCP 43. Rejestrator domeny jest odpowiedzialny za utrzymywanie rekordów WHOIS dla dzierżawionych nazw domen. Serwer WHOIS odpowiada, podając różne informacje dotyczące żądanej domeny. Szczególnie interesujące są następujące informacje:

- Rejestrator: Za pośrednictwem którego rejestratora została zarejestrowana nazwa domeny?
- Dane kontaktowe osoby rejestrującej: imię i nazwisko, nazwa organizacji, adres, numer telefonu i inne. (chyba że dane te zostały ukryte za pomocą usługi ochrony prywatności)
- Daty utworzenia, aktualizacji i wygaśnięcia: Kiedy nazwa domeny została zarejestrowana po raz pierwszy? Kiedy była ostatnio aktualizowana? I kiedy należy ją odnowić?
- Serwer nazw: Do którego serwera zwrócić się o rozwiązanie nazwy domeny?

Aby uzyskać te informacje, musimy skorzystać z `whois`klienta lub usługi online. Wiele usług online udostępnia `whois`informacje, jednak zazwyczaj szybciej i wygodniej jest skorzystać z lokalnego klienta whois. Używając AttackBox (lub lokalnego komputera z systemem Linux, takiego jak Parrot lub Kali), można łatwo uzyskać dostęp do klienta whois w terminalu. Składnia jest następująca `whois DOMAIN_NAME`: , gdzie `DOMAIN_NAME`to domena, o której próbujesz uzyskać więcej informacji. Rozważmy poniższy przykład wykonania `whois tryhackme.com`:

Terminal

```shell-session
user@TryHackMe$ whois tryhackme.com
[Querying whois.verisign-grs.com]
[Redirected to whois.namecheap.com]
[Querying whois.namecheap.com]
[whois.namecheap.com]
Domain name: tryhackme.com
Registry Domain ID: 2282723194_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.namecheap.com
Registrar URL: http://www.namecheap.com
Updated Date: 2021-05-01T19:43:23.31Z
Creation Date: 2018-07-05T19:46:15.00Z
Registrar Registration Expiration Date: 2027-07-05T19:46:15.00Z
Registrar: NAMECHEAP INC
Registrar IANA ID: 1068
Registrar Abuse Contact Email: abuse@namecheap.com
Registrar Abuse Contact Phone: +1.6613102107
Reseller: NAMECHEAP INC
Domain Status: clientTransferProhibited https://icann.org/epp
Registry Registrant ID: 
Registrant Name: Withheld for Privacy Purposes
Registrant Organization: Privacy service provided by Withheld for Privacy ehf
[...]
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
>>> Last update of WHOIS database: 2021-08-25T14:58:29.57Z <<<
For more information on Whois status codes, please visit https://icann.org/epp
```

Widzimy mnóstwo informacji; przeanalizujemy je w kolejności wyświetlania. Najpierw zauważamy, że zostaliśmy przekierowani do strony, `whois.namecheap.com`aby uzyskać nasze informacje. W tym przypadku i obecnie, `namecheap.com`utrzymuje ona rekord WHOIS dla tej nazwy domeny. Ponadto możemy zobaczyć datę utworzenia, datę ostatniej aktualizacji i datę wygaśnięcia.

Następnie uzyskujemy informacje o rejestratorze i abonencie. Możemy znaleźć imię i nazwisko abonenta oraz dane kontaktowe, chyba że korzysta on z usług ochrony prywatności. Chociaż nie są one wyświetlane powyżej, uzyskujemy dane kontaktowe administratora i działu technicznego dla tej domeny. Na koniec widzimy serwery nazw domen, które powinniśmy sprawdzić, jeśli mamy jakieś rekordy DNS do wyszukania.

Zebrane informacje można poddać analizie w celu wykrycia nowych obszarów ataków, takich jak socjotechnika czy ataki techniczne. Na przykład, w zależności od zakresu testu penetracyjnego, można rozważyć atak na serwer poczty e-mail użytkownika z uprawnieniami administratora lub serwery DNS, zakładając, że należą one do klienta i są objęte zakresem testu penetracyjnego.

Należy pamiętać, że ze względu na zautomatyzowane narzędzia wykorzystujące zapytania WHOIS do zbierania adresów e-mail, wiele usług WHOIS podejmuje środki zapobiegawcze. Mogą one na przykład usuwać adresy e-mail. Ponadto wielu użytkowników subskrybuje usługi ochrony prywatności, aby uniknąć zbierania adresów e-mail przez spamerów i zachować prywatność swoich danych.

W AttackBoxie otwórz terminal i uruchom polecenie, `whois tryhackme.com`aby uzyskać informacje potrzebne do udzielenia odpowiedzi na poniższe pytania.

### nslookup

W poprzednim zadaniu wykorzystaliśmy protokół WHOIS, aby uzyskać różne informacje o nazwie domeny, której szukaliśmy. W szczególności udało nam się uzyskać serwery DNS od rejestratora.

Znajdź adres IP nazwy domeny za pomocą polecenia `nslookup`, co oznacza wyszukiwanie serwera nazw (Name Server Look Up). Musisz wydać polecenie `nslookup DOMAIN_NAME`, na przykład `nslookup tryhackme.com`. Lub, bardziej ogólnie, możesz użyć `nslookup OPTIONS DOMAIN_NAME SERVER`. Te trzy główne parametry to:

- OPTIONS zawiera typ zapytania pokazany w poniższej tabeli. Na przykład, można go użyć `A`dla adresów IPv4 i `AAAA`IPv6.
- DOMAIN_NAME to nazwa domeny, której szukasz.
- SERWER to serwer DNS, do którego chcesz wysłać zapytanie. Możesz wybrać dowolny lokalny lub publiczny serwer DNS. Cloudflare oferuje `1.1.1.1`i `1.0.0.1`, Google oferuje `8.8.8.8`i `8.8.4.4`, a Quad9 oferuje `9.9.9.9`i `149.112.112.112`. Istnieje wiele [innych publicznych serwerów DNS](https://duckduckgo.com/?q=public+dns) , spośród których możesz wybierać, jeśli szukasz alternatywy dla serwerów DNS swojego dostawcy usług internetowych.

|Typ zapytania|Wynik|
|---|---|
|A|Adresy IPv4|
|AAAA|Adresy IPv6|
|CNAME|Nazwa kanoniczna|
|MX|Serwery pocztowe|
|SOA|Początek autorytetu|
|Tekst|Rekordy TXT|

Na przykład `nslookup -type=A tryhackme.com 1.1.1.1`(lub `nslookup -type=a tryhackme.com 1.1.1.1`ponieważ nie jest rozróżniana wielkość liter) można użyć tego polecenia, aby zwrócić wszystkie adresy IPv4 używane przez tryhackme.com.

Terminal

```shell-session
user@TryHackMe$ nslookup -type=A tryhackme.com 1.1.1.1
Server:		1.1.1.1
Address:	1.1.1.1

Non-authoritative answer:
Name:	tryhackme.com
Address: 172.67.69.208
Name:	tryhackme.com
Address: 104.26.11.229
Name:	tryhackme.com
Address: 104.26.10.229
```

Rekordy A i AAAA służą do zwracania odpowiednio adresów IPv4 i IPv6. To wyszukiwanie jest przydatne z perspektywy testów penetracyjnych. W powyższym przykładzie zaczęliśmy od jednej nazwy domeny i uzyskaliśmy trzy adresy IPv4. Każdy z tych adresów IP można dodatkowo sprawdzić pod kątem luk w zabezpieczeniach, zakładając, że mieszczą się one w zakresie testu penetracyjnego.

Załóżmy, że chcesz dowiedzieć się więcej o serwerach pocztowych i konfiguracjach dla konkretnej domeny. Możesz to zrobić za pomocą `nslookup -type=MX tryhackme.com`. Oto przykład:

Terminal

```shell-session
user@TryHackMe$ nslookup -type=MX tryhackme.com
Server:		127.0.0.53
Address:	127.0.0.53

Non-authoritative answer:
tryhackme.com	mail exchanger = 5 alt1.aspmx.l.google.com.
tryhackme.com	mail exchanger = 1 aspmx.l.google.com.
tryhackme.com	mail exchanger = 10 alt4.aspmx.l.google.com.
tryhackme.com	mail exchanger = 10 alt3.aspmx.l.google.com.
tryhackme.com	mail exchanger = 5 alt2.aspmx.l.google.com.
```

Widzimy, że aktualna konfiguracja poczty tryhackme.com korzysta z wyszukiwarki Google. Ponieważ MX wyszukuje serwery wymiany poczty, zauważamy, że gdy serwer poczty próbuje dostarczyć wiadomość e-mail `@tryhackme.com`, próbuje połączyć się z serwerem `aspmx.l.google.com`o numerze zamówienia 1. Jeśli jest on zajęty lub niedostępny, serwer poczty próbuje połączyć się z kolejnym w kolejności serwerem wymiany poczty, `alt1.aspmx.l.google.com`czyli `alt2.aspmx.l.google.com`.

Google udostępnia listę serwerów pocztowych, dlatego nie należy oczekiwać, że serwery pocztowe będą działać w wersji serwerowej podatnej na ataki. W innych przypadkach możemy jednak znaleźć serwery pocztowe, które nie są odpowiednio zabezpieczone ani nie posiadają zainstalowanych poprawek.

Takie informacje mogą okazać się cenne podczas pasywnego rozpoznania celu. Możesz powtórzyć podobne zapytania dla innych nazw domen i wypróbować różne typy, takie jak `-type=txt`. Kto wie, jakie informacje możesz odkryć po drodze!

W przypadku bardziej zaawansowanych zapytań DNS i dodatkowych funkcji możesz użyć `dig`, skrótu od „Domain Information Groper”, jeśli jesteś ciekawy. Użyjmy `dig`, aby wyszukać rekordy MX i porównać je z `nslookup`. Możemy użyć `dig DOMAIN_NAME`, ale aby określić typ rekordu, użyjemy `dig DOMAIN_NAME TYPE`. Opcjonalnie możemy wybrać serwer, do którego chcemy wysłać zapytanie, używając `dig @SERVER DOMAIN_NAME TYPE`.

- SERVER to serwer DNS, który chcesz zapytać.
- DOMAIN_NAME to nazwa domeny, której szukasz.
- TYPE zawiera typ rekordu DNS, jak pokazano w tabeli podanej wcześniej.

Terminal

```shell-session
user@TryHackMe$ dig tryhackme.com MX

; <<>> DiG 9.16.19-RH <<>> tryhackme.com MX
;; global options: +cmd
;; Got answer:
;; ->>HEADER<
        
```

Szybkie porównanie wyników `nslookup`i `dig`pokazuje, że `dig`zwrócono więcej informacji, takich jak domyślnie TTL (czas życia). Aby wysłać zapytanie do `1.1.1.1`serwera DNS, można wykonać polecenie `dig @1.1.1.1 tryhackme.com MX`.

Używając AttackBox, otwórz terminal i użyj polecenia `nslookup`lub `dig`, aby uzyskać informacje potrzebne do odpowiedzi na poniższe pytanie.

### DNSdumpster

Narzędzia do wyszukiwania DNS , takie jak #nslookup i #dig, nie są w stanie samodzielnie znaleźć subdomen. Domena, którą sprawdzasz, może zawierać inną subdomenę, która może ujawnić wiele informacji o obiekcie docelowym. Na przykład, jeśli tryhackme.com ma subdomeny wiki.tryhackme.com i webmail.tryhackme.com, warto dowiedzieć się o nich więcej, ponieważ mogą one zawierać mnóstwo informacji o obiekcie docelowym. Istnieje możliwość, że jedna z tych subdomen została skonfigurowana i nie jest regularnie aktualizowana. Brak odpowiednich, regularnych aktualizacji zazwyczaj prowadzi do powstania usług podatnych na ataki. Ale skąd możemy wiedzieć, że takie subdomeny istnieją?

Możemy rozważyć użycie wielu wyszukiwarek, aby skompilować listę publicznie znanych subdomen. Jedna wyszukiwarka nie wystarczy; co więcej, powinniśmy spodziewać się przejrzenia co najmniej dziesiątek wyników, aby znaleźć interesujące dane. W końcu szukasz subdomen, które nie są jawnie reklamowane, a zatem nie musisz znajdować się na pierwszej stronie wyników wyszukiwania. Innym sposobem na odkrycie takich subdomen byłoby wykorzystanie zapytań brute-force w celu znalezienia subdomen z rekordami DNS .

Aby uniknąć czasochłonnego wyszukiwania, można skorzystać z usługi online oferującej szczegółowe odpowiedzi na zapytania DNS , takiej jak [DNSDumpster](https://dnsdumpster.com/) . Wpisując w #DNSDumpster hasło `tryhackme.com`, odkryjemy subdomenę `blog.tryhackme.com`, której standardowe zapytanie DNS nie jest w stanie podać. Dodatkowo, DNSDumpster zwróci zebrane informacje DNS w czytelnych tabelach i wykresie. DNSDumpster udostępni również wszelkie zebrane informacje o serwerach nasłuchujących.

Przeszukamy `tryhackme.com`DNSDumpster, aby dać Ci przedsmak oczekiwanych wyników. Wśród wyników znalazła się lista serwerów DNS dla poszukiwanej domeny. DNSDumpster przetworzył również nazwy domen na adresy IP, a nawet spróbował je geolokalizować. Możemy również zobaczyć rekordy MX; DNSDumpster przetworzył wszystkie pięć serwerów wymiany poczty na ich adresy IP i dostarczył więcej informacji o właścicielu i lokalizacji. Na koniec możemy zobaczyć rekordy TXT. Praktycznie jedno zapytanie wystarczyło, aby uzyskać wszystkie te informacje.

 ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/655c1ce6c3bb53e6252128b6da135ba9.png)

DNSDumpster przedstawi również zebrane informacje w formie graficznej. DNSDumpster wyświetlił dane z tabeli wcześniej w formie wykresu. Można zobaczyć rozgałęzienia DNS i MX do odpowiednich serwerów oraz adresy IP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/844a43bc37547bbb13f94894605992d3.png)  

Obecnie dostępna jest funkcja beta, która umożliwia również eksportowanie wykresu. W razie potrzeby można manipulować wykresem i przesuwać bloki.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/eb95e62815b6ace3c823fd0159884731.png)  

Użyj przeglądarki internetowej w AttackBoxie lub swoim systemie, aby odpowiedzieć na poniższe pytanie.

### Shodan.oi

Gdy otrzymasz zadanie przeprowadzenia testu penetracyjnego na określonych celach, w ramach fazy pasywnego rozpoznania, usługa taka jak [Shodan.io](https://www.shodan.io/) może być pomocna w uzyskaniu różnych informacji o sieci klienta, bez konieczności aktywnego łączenia się z nią. Ponadto, w ramach obrony, możesz skorzystać z różnych usług Shodan.io, aby dowiedzieć się o podłączonych i narażonych urządzeniach należących do Twojej organizacji.

#Shodan.io próbuje połączyć się z każdym urządzeniem dostępnym online, aby zbudować wyszukiwarkę połączonych „rzeczy”, w przeciwieństwie do wyszukiwarki stron internetowych. Po otrzymaniu odpowiedzi, zbiera wszystkie informacje związane z usługą i zapisuje je w bazie danych, aby umożliwić ich wyszukiwanie. Rozważmy zapisany rekord jednego z serwerów tryhackme.com.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a8ac6c22a64b8413ee8d02c2224eddac.png)  

Ten rekord wskazuje serwer WWW; jednak, jak już wspomniano, Shodan.io gromadzi informacje dotyczące każdego urządzenia podłączonego do sieci, które znajdzie. Wyszukanie `tryhackme.com`w Shodan.io wyświetli co najmniej rekord widoczny na powyższym zrzucie ekranu. Dzięki temu wynikowi wyszukiwania w Shodan.io możemy dowiedzieć się kilku rzeczy związanych z naszym wyszukiwaniem, takich jak:

- Adres IP
- firma hostingowa
- położenie geograficzne
- typ i wersja serwera

Możesz również spróbować wyszukać adresy IP uzyskane z wyszukiwań DNS . Oczywiście mogą one ulec zmianie. Na [stronie pomocy](https://help.shodan.io/the-basics/search-query-fundamentals) możesz dowiedzieć się więcej o wszystkich opcjach wyszukiwania dostępnych w Shodan.io. Zachęcamy również do dołączenia do [Shodan.io](https://tryhackme.com/room/shodan) na TryHackMe .

Aby uzyskać odpowiedzi na poniższe pytania, najlepiej odwiedzić Shodan.io. Pamiętaj jednak, że odpowiedzi na Shodan.io możesz znaleźć bez konieczności posiadania konta premium.

Odpowiedz na poniższe pytania

Według Shodan.io, który kraj na świecie ma największą liczbę publicznie dostępnych serwerów Apache?

W tym pokoju skupiliśmy się na biernym rozpoznaniu. W szczególności omówiliśmy narzędzia wiersza poleceń, `whois`, `nslookup`i `dig`. Omówiliśmy również dwie publicznie dostępne usługi: [DNSDumpster](https://dnsdumpster.com/) i [Shodan.io](https://www.shodan.io/) . Siłą takich narzędzi jest możliwość zbierania informacji o celach bez bezpośredniego łączenia się z nimi. Co więcej, zasoby informacji, które można znaleźć za pomocą takich narzędzi, mogą być ogromne, gdy opanuje się opcje wyszukiwania i przyzwyczai się do czytania wyników.

|Zamiar|Przykład wiersza poleceń|
|---|---|
|Wyszukaj rekord WHOIS|`whois tryhackme.com`|
|Wyszukaj rekordy DNS A|`nslookup -type=A tryhackme.com`|
|Wyszukaj rekordy DNS MX na serwerze DNS|`nslookup -type=MX tryhackme.com 1.1.1.1`|
|Wyszukaj rekordy DNS TXT|`nslookup -type=TXT tryhackme.com`|
|Wyszukaj rekordy DNS A|`dig tryhackme.com A`|
|Wyszukaj rekordy DNS MX na serwerze DNS|`dig @1.1.1.1 tryhackme.com MX`|
|Wyszukaj rekordy DNS TXT|`dig tryhackme.com TXT`|

Więcej informacji na temat DNS znajdziesz w artykule [DNS in Detail](https://tryhackme.com/room/dnsindetail) .
