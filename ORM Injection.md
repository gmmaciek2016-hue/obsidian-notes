

Dzięki rozwojowi cyberbezpieczeństwa wielu programistów przyjęło mapowanie obiektowo-relacyjne (ORM) w celu złagodzenia SQLAtaki typu injection. Chociaż ORM ma na celu uproszczenie interakcji z bazami danych i poprawę bezpieczeństwa, zagrożenie atakami typu injection wciąż istnieje. Wstrzyknięcie ORM ma miejsce, gdy atakujący wykorzystują luki w zabezpieczeniach frameworków ORM, umożliwiając im wykonywanie dowolnych zapytań. W tej sali omówimy zaawansowane techniki wstrzykiwania ORM, zapewniając dogłębną wiedzę na temat zaawansowanych wektorów ataku i skutecznych strategii przeciwdziałania im.

Pod koniec tej sali zdobędziesz wszechstronną wiedzę na temat różnych metod wstrzykiwania ORM, co pomoże ci identyfikować i wykorzystywać te luki w zabezpieczeniach w celu ochrony aplikacji internetowych.



Cele edukacyjne

﻿W tym pomieszczeniu zdobędziesz wszechstronne zrozumienie następujących kluczowych koncepcji:

Zrozumienie ORM
Identyfikacja wtrysku
Słaba implementacja
Wrażliwa implementacja
Wymagania wstępne dotyczące nauki

Przed rozpoczęciem zajęć w tym pokoju zaleca się zapoznanie z następującymi tematami:

Wstrzyknięcie SQL
OWASP10 najlepszych
Zaczynajmy! 

Co to jestORM

ORM to technika programowania, która ułatwia konwersję danych między niekompatybilnymi systemami za pomocą obiektowych języków programowania. Pozwala ona programistom na interakcję z bazą danych za pomocą natywnej składni języka programowania, czyniąc manipulację danymi bardziej intuicyjną i redukując potrzebę rozbudowanych narzędzi.SQLzapytania. ORM jest szczególnie przydatny, gdy wymagane są złożone interakcje danych, ponieważ upraszcza dostęp do bazy danych i sprzyja ponownemu wykorzystaniu kodu. 



Zamiar

ORM stanowi pomost między modelem programowania obiektowego a modelem relacyjnej bazy danych. Głównym celem ORM jest abstrakcja warstwy bazy danych, umożliwiająca programistom pracę z obiektami zamiast z tabelami i wierszami. Ta warstwa abstrakcji pomaga w:

Zmniejszenie ilości kodu szablonowego : ORM zmniejsza potrzebę pisania powtarzalnego kodu poprzez automatyczne generowanie zapytań SQL w oparciu o operacje na obiektach.
Zwiększona produktywność : Programiści mogą skupić się na logice biznesowej, nie martwiąc się o interakcje z bazami danych.
Zapewnienie spójności : struktury ORM zapewniają spójną obsługę operacji na bazach danych, co zmniejsza ryzyko wystąpienia błędów.
Poprawa łatwości utrzymania : Zmiany w schemacie bazy danych są łatwiejsze w zarządzaniu, ponieważ można je uwzględnić w modelu obiektów bez konieczności przeprowadzania rozległych modyfikacji kodu.
Często używane struktury ORM

W środowisku programistycznym powszechnie wykorzystuje się kilka frameworków ORM, z których każdy jest dostosowany do różnych języków programowania i środowisk. Oto kilka przykładów:

Doktryna (PHP)

Doctrine to potężny i elastyczny framework ORM dla PHP. Jest szczególnie popularny w frameworku Symfony, ale można go używać niezależnie. Doctrine oferuje kompleksowy zestaw narzędzi do interakcji z bazą danych, w tym kreator zapytań, zarządzanie schematami oraz obiektowy język zapytań. Jego zdolność do mapowania złożonych struktur obiektów na schematy bazy danych sprawia, że ​​jest on ulubionym narzędziem programistów PHP.

Hibernacja (Java)

Hibernate to solidny i dojrzały framework ORM dla aplikacji Java. Upraszcza mapowanie klas Java na tabele bazy danych i zapewnia zaawansowane możliwości pobierania i przetwarzania danych dzięki językowi zapytań Hibernate (Hibernate Query Language).Wysoka jakośćHibernate obsługuje różne systemy zarządzania bazami danych i jest znany ze swoich funkcji optymalizacji wydajności, takich jak buforowanie i leniwe ładowanie.

SQLAlchemy (Python)

SQLAlchemy to wszechstronny i wydajny system ORM dla języka Python. Oferuje zestaw narzędzi SQL oraz system ORM, który pozwala programistom korzystać z surowego kodu SQL w razie potrzeby, zapewniając jednocześnie korzyści systemu ORM. Elastyczność i modułowa architektura SQLAlchemy sprawiają, że nadaje się on do szerokiej gamy aplikacji, od małych skryptów po systemy korporacyjne na dużą skalę.

Entity Framework (C#)

Entity Framework to platforma ORM firmy Microsoft dla aplikacji .NET. Umożliwia ona programistom pracę z danymi relacyjnymi za pomocą obiektów specyficznych dla domeny, eliminując potrzebę pisania większości kodu dostępu do danych, który zazwyczaj muszą tworzyć programiści. Entity Framework obsługuje wielu dostawców baz danych i płynnie integruje się z innymi technologiami .NET.

Aktywny rekord (Ruby on Rails)

Active Record to domyślny ORM dla aplikacji Ruby on Rails. Jest zgodny ze wzorcem projektowym Active Record, co oznacza, że ​​każda tabela w bazie danych odpowiada klasie, a każdy wiersz w tabeli odpowiada instancji tej klasy. Active Record upraszcza interakcje z bazą danych, oferując bogaty zestaw metod do wyszukiwania i przetwarzania danych.


Mapowanie między obiektami w kodzie i tabelach bazy danych

ORMto technika upraszczająca interakcję danych w aplikacji poprzez mapowanie obiektów w kodzie na tabele bazy danych.PHPProces ten obejmuje definiowanie klas reprezentujących tabele bazy danych i ich relacje. Każda właściwość klasy odpowiada kolumnie w tabeli, a każda instancja klasy reprezentuje wiersz.

Na przykład, używając Eloquent ORM od Laravela, możesz zdefiniować klasę modelu w następujący sposób:


namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class User extends Model
{
    protected $table = 'users';
    protected $fillable = [
        'name', 'email', 'password',
    ];
    // Other Eloquent model configurations can go here...
}
W tym przykładzie Userklasa jest mapowana na userstabelę w bazie danych, z właściwościami odpowiadającymi kolumnom. Eloquent ORM obsługuje translację między tymi reprezentacjami obiektów a bazowymi zapytaniami SQL, umożliwiając programistom manipulowanie rekordami bazy danych za pomocą składni obiektowej.

Typowe operacje ORM (tworzenie, odczyt, aktualizacja, usuwanie)

Infrastruktura ORM usprawnia typowe operacje baz danych, często określane jako operacje CRUD:

Utwórz : Tworzenie nowych rekordów w bazie danych obejmuje utworzenie nowego obiektu modelu, ustawienie jego właściwości i zapisanie go w bazie danych.

use App\Models\User;

// Create a new user
$user = new User();
$user->name = 'Admin';
$user->email = 'admin@example.com';
$user->password = bcrypt('password'); 
$user->save();
Ten kod tworzy nowego użytkownika i zapisuje go w bazie danych. Metoda save przygotowuje encję do wstawienia i wykonujeSQLPolecenie INSERT dodaje nowy rekord do tabeli użytkowników. Funkcja bcrypt()służy do bezpiecznego hashowania hasła przed jego zapisaniem.

Odczyt : Odczyt rekordów z bazy danych polega na pobieraniu danych przy użyciu różnych metod Eloquent.

use App\Models\User;

// Find a user by ID
$user = User::find(1);

// Find all users
$allUsers = User::all();

// Find users by specific criteria
$admins = User::where('email', 'admin@example.com')->get();
Ten kod demonstruje różne sposoby pobierania rekordów z bazy danych. Funkcja find(1)pobiera użytkownika o identyfikatorze 1 poprzez wykonanie instrukcji SQL SELECT. Funkcja all()pobiera wszystkich użytkowników poprzez wykonanie SELECT * FROM usersinstrukcji SQL. Klauzula where('email', 'admin@example.com')->get()pobiera użytkowników o określonym adresie e-mail poprzez wykonanie SELECT * FROM users WHERE email = 'admin@example.com'instrukcji SQL.



Podobnie jak w przypadku operacji tworzenia i odczytu, funkcje aktualizacji i usuwania są realizowane w prosty sposób, wykorzystując platformę ORM Eloquent firmy Laravel. W przypadku aktualizacji pobierasz istniejący rekord, modyfikujesz jego właściwości i zapisujesz zmiany. W przypadku usuwania pobierasz rekord i wywołujesz metodę delete, aby usunąć go z bazy danych. Eloquent zajmuje się przygotowaniem i wykonaniem odpowiednich poleceń SQL, dzięki czemu operacje na bazie danych są proste i intuicyjne.

Porównanie wstrzykiwania SQL i wstrzykiwania ORM

Wstrzykiwanie SQL i wstrzykiwanie ORM to techniki służące do wykorzystywania luk w interakcjach z bazami danych, ale ich celem są różne poziomy stosu:

Wstrzyknięcie SQL : atakuje surowe zapytania SQL, umożliwiając atakującym bezpośrednią manipulację instrukcjami SQL. Zazwyczaj osiąga się to poprzez wstrzyknięcie złośliwych danych wejściowych do ciągów zapytań. Fragment wstrzyknięcia w poniższym zapytaniu, OR '1'='1, zawsze zwraca wartość true, umożliwiając atakującym ominięcie uwierzytelniania:

SELECT * FROM users WHERE username = 'admin' OR '1'='1';
Wstrzyknięcie ORM : atakuje framework ORM, wykorzystując sposób, w jaki konstruuje zapytania z operacji na obiektach. Atakujący manipulują metodami i właściwościami ORM, aby wpływać na wynikowe zapytania SQL.

$userRepository->findBy(['username' => "admin' OR '1'='1"]);
W powyższym kodzie część wstrzykiwania admin' OR '1'='1zawsze ma wartość true.

Kluczowe różnice w technikach eksploatacji

Aspekt	Wstrzyknięcie SQL
Wstrzyknięcie ORM
Poziom wtrysku
Bezpośrednio kieruje zapytania SQL w postaci surowej
Celuje w konstrukcję zapytań w ramach ORM
Złożoność
Bardziej bezpośrednie, ponieważ manipuluje surowym SQL
Wymaga zrozumienia wewnętrznych mechanizmów i metod ORM
Wykrywanie
Łatwiejsze do wykrycia za pomocą tradycyjnych zapór WAF i dzienników zapytań
Trudniejsze do wykrycia, ponieważ ładunki znajdują się w metodach ORM
Łagodzenie
Wykorzystanie przygotowanych instrukcji, sparametryzowanych zapytań, walidacja danych wejściowych
Prawidłowa konfiguracja ORM, walidacja danych wejściowych na poziomie aplikacji, funkcje ORM wymuszające bezpieczeństwo zapytań
Konfigurowanie środowiska

Ponieważ w tym projekcie korzystamy z platformy Laravel, pokrótce wyjaśnimy, jak skonfigurować Eloquent ORM (oparty na platformie Laravel). Eloquent ORM to domyślny ORM dołączony do platformy Laravel, który zapewnia piękną i prostą Active Recordimplementację do pracy z bazą danych. Najpierw musimy zainstalować Laravel za pomocą Composera. Otwórz terminal i uruchom polecenie  composer create-project --prefer-dist laravel/laravel thm-project, gdzie thm-projectto nazwa Twojego projektu. Nie musisz ćwiczyć tych kroków w tym pomieszczeniu; ma to na celu jedynie pomóc Ci zrozumieć, jak ORM ułatwia pracę.

Konfiguruj poświadczenia bazy danych

Następnie musimy skonfigurować dane uwierzytelniające bazy danych. Laravel używa tego .envpliku do przechowywania zmiennych środowiskowych, w tym danych uwierzytelniających bazy danych. Otwórz .envplik w katalogu głównym swojego projektu Laravel i zaktualizuj poniższe wiersze, wprowadzając dane dotyczące bazy danych:


DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=your_database_name
DB_USERNAME=your_database_user
DB_PASSWORD=your_database_password
Konfigurowanie migracji

Migracje są jak system kontroli wersji bazy danych, umożliwiający łatwą modyfikację i udostępnianie schematu bazy danych. System migracji Laravela jest istotną częścią frameworka i upraszcza zarządzanie zmianami w bazie danych.

Utwórz migrację

Aby utworzyć migrację, możemy skorzystać z Artisannarzędzia wiersza poleceń dołączonego do Laravel. Możesz uruchomić polecenie php artisan make:migration create_users_table --create=users aby wygenerować migrację dla userstabeli:

To polecenie generuje plik migracji w katalogu database/migrations. Plik migracji zawiera metody definiujące strukturę tabeli users.


<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
class CreateUsersTable extends Migration
{
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->string('password');
            $table->timestamps();
        });
    }
    public function down()
    {
        Schema::dropIfExists('users');
    }



W powyższym kodzie  up() metoda definiuje strukturę tabeli users. Zawiera ona kolumny dla identyfikatora, nazwy, adresu e-mail, hasła i znaczników czasu. Natomiast metoda down() usuwa  tabelę users, jeśli migracja zostanie wycofana.

Po zdefiniowaniu migracji uruchom polecenie php artisan migrate, aby ją zastosować i utworzyć userstabelę w bazie danych. To polecenie wykona up()metodę z pliku migracji i utworzy userstabelę z określonymi kolumnami w bazie danych.

W kontekście ORM, migracje upraszczają proces mapowania tabel bazy danych na modele aplikacji. Pozwalają programistom skupić się na pisaniu czystego, łatwego w utrzymaniu kodu, zapewniając jednocześnie, że bazowy schemat bazy danych obsługuje wymagania aplikacji dotyczące danych. Jednak z perspektywy zespołu ds. bezpieczeństwa (red team), nieprawidłowo skonfigurowane migracje i słabe implementacje mogą prowadzić do luk w zabezpieczeniach, takich jak wstrzykiwanie ORM. Hakerzy często wykorzystują te słabości do manipulowania zapytaniami do bazy danych i uzyskiwania nieautoryzowanego dostępu do poufnych danych. Dlatego kluczowe jest efektywne wykorzystanie migracji w celu egzekwowania silnych i bezpiecznych projektów schematów bazy danych oraz zapewnienia solidnych konfiguracji ORM, aby zapobiec tego typu lukom w zabezpieczeniach.



IdentyfikowanieORMLuki w zabezpieczeniach związane z iniekcją obejmują badanie sposobu obsługi danych wprowadzanych przez użytkownika w zapytaniach ORM. Luki te zazwyczaj pojawiają się, gdy dane wprowadzane przez użytkownika są bezpośrednio osadzane w metodach zapytań ORM bez odpowiedniej sanityzacji lub walidacji. Wskaźnikami potencjalnych problemów z iniekcją ORM są: użycie dynamicznych zapytań, które łączą dane wprowadzane przez użytkownika, surowe metody wykonywania zapytań oraz niewystarczające wykorzystanie zapytań parametryzowanych.

Łączenie się z maszyną

Możesz uruchomić maszynę laboratoryjną, klikając  Start Lab Machine przycisk dołączony do tego zadania. Dostęp do maszyny wirtualnej można uzyskać, odwiedzając link  https://LAB_WEB_URL.p.thmlabs.com(otwiera się w nowej karcie)Później, w sali, wykorzystamy podatną na ataki aplikację, aby  praktycznie wykonać ćwiczenie i zapoznać się z różnymi wektorami ataku. Proszę odczekać 3-4 minuty po całkowitym uruchomieniu systemu, aby umożliwić prawidłowe uruchomienie automatycznych skryptów.  



Techniki testowania wstrzykiwania ORM

Ręczny przegląd kodu : Dokładna inspekcja kodu źródłowego może ujawnić surowe metody zapytań (takie jak whereRaw() w Laravel), które bezpośrednio uwzględniają dane wejściowe użytkownika. Szukaj połączonych ciągów znaków lub nieskorygowanych znaków wejściowych w metodach ORM, które mogą wskazywać na punkty wstrzyknięcia.
Automatyczne skanowanie : Użyj narzędzi do skanowania bezpieczeństwa zaprojektowanych do wykrywania luk w zabezpieczeniach ORM. Narzędzia te analizują bazę kodu w celu identyfikacji wzorców, które mogą prowadzić do wstrzyknięcia, takich jak dynamiczna konstrukcja zapytania lub nieprawidłowa obsługa danych wejściowych.
Testowanie walidacji danych wejściowych : Przeprowadź testy ręczne, wstrzykując ładunki do danych wejściowych aplikacji, aby sprawdzić, czy wpływają one na zapytanie ORM. Na przykład, wstrzykując znaki kontrolne SQL lub słowa kluczowe, aby sprawdzić, czy wpływają one na wykonanie zapytania.
Testowanie oparte na błędach : celowe wprowadzanie nieprawidłowych lub błędnie sformatowanych danych w celu wywołania błędów. Szczegółowe komunikaty o błędach mogą dostarczyć informacji o strukturze zapytań bazowych i wskazać potencjalne luki w zabezpieczeniach.
Ramy i testy wstrzykiwania ORM

Struktura
Biblioteka ORM
Typowe podatne metody
Laravel
Wymowny ORM
whereRaw(), DB::raw()
Ruby on Rails
Aktywny rekord
where("name = '#{input}'")
Django
Django ORM
extra(),raw()
Wiosna
Hibernować
createQuery()zconcatenation
Node.js
Sequelize
sequelize.query()
Powyższa tabela przedstawia różne frameworki do tworzenia stron internetowych i powiązane z nimi biblioteki ORM, szczegółowo opisując typowe metody podatne na luki w zabezpieczeniach. Na przykład, w Laravel, użycie metody whereRaw() lub DB::raw() z danymi wprowadzanymi przez użytkownika może prowadzić do wstrzyknięcia ORM, ale można temu zapobiec, stosując sparametryzowane zapytania z tą where()metodą. Podobnie, w Django, metody takie jak extra()i raw()mogą wprowadzać luki w zabezpieczeniach, jeśli nie są poprawnie obsługiwane, podczas gdy użycie metody filtru z sparametryzowanymi zapytaniami zapewnia bezpieczniejsze interakcje z bazą danych. Zrozumienie tych typowych pułapek i stosowanie bezpiecznych praktyk kodowania ma kluczowe znaczenie dla utrzymania bezpieczeństwa aplikacji internetowych.

Eksploracja aplikacji docelowej

Teraz, gdy wiemy już, jak identyfikować luki w zabezpieczeniach związane z wstrzykiwaniem ORM, odwiedźmy witrynę https://LAB_WEB_URL.p.thmlabs.com(otwiera się w nowej karcie)Tutaj zobaczysz, że witryna prosi o podanie danych. Aby ustalić, który framework jest używany, możemy zastosować różne techniki, takie jak sprawdzanie plików cookie, przeglądanie kodu źródłowego i analiza nagłówków HTTP . 

Techniki identyfikacji ram

Weryfikacja plików cookie : Sprawdź pliki cookie ustawione przez aplikację. Frameworki często używają unikalnych konwencji nazewnictwa lub formatów dla plików cookie sesji, co może dostarczyć wskazówek dotyczących technologii bazowej.


Przeglądanie kodu źródłowego : Przejrzyj kod źródłowy HTML pod kątem komentarzy, meta tagów i wszelkich osadzonych skryptów, które mogą ujawnić sygnatury specyficzne dla frameworka. Jednak ta metoda może być rozstrzygająca tylko czasami.


Analiza nagłówków HTTP : Nagłówki HTTP mogą czasami zawierać informacje o serwerze i infrastrukturze. Do analizy tych nagłówków można użyć narzędzi takich jak Burp Suite lub narzędzi dla programistów przeglądarek.
Struktura adresów URL : Struktura adresów URL może zawierać wskazówki dotyczące frameworka. Na przykład, niektóre wzorce routingu są unikalne dla konkretnych frameworków.
Strony logowania i komunikaty o błędach : Strony uwierzytelniania i komunikaty o błędach mogą czasami ujawniać strukturę. Niektóre struktury mają charakterystyczne strony błędów lub struktury formularza logowania. 
Teraz, gdy zidentyfikowaliśmy, że aplikacja korzysta z platformy Laravel, analizując pliki cookie, możemy zbadać jej zachowanie, podając złośliwe dane wejściowe, aby dowiedzieć się więcej. W szczególności wprowadzimy dane wejściowe, 1'aby sprawdzić, jak aplikacja przetwarza te dane i potwierdzić użycie ORM. Odwiedzając stronę  https://LAB_WEB_URL.p.thmlabs.com(otwiera się w nowej karcie),  zostajemy poproszeni o podanie danych wejściowych. Wprowadzamy je 1'w polu „Adres e-mail (narażony na atak)” i wysyłamy formularz, aby ustalić, jak aplikacja przetwarza te dane wejściowe. Te dane wejściowe mają na celu zakłócenie struktury zapytania i ujawnienie wszelkich ukrytych problemów z konstruowaniem zapytań przez aplikację.



Po przesłaniu tych danych wejściowych musimy uważnie obserwować odpowiedź aplikacji. Jeśli aplikacja zwróci komunikat o błędzie, może on dostarczyć cennych informacji na temat procesu konstruowania zapytania. Na przykład komunikat o błędzie, taki jak ten, SQLSTATE[42000]: Syntax error or access violationwskazuje, że dane wejściowe zostały nieprawidłowo obsłużone i połączone w jeden ciąg.SQLzapytanie, co skutkuje błędem składni. Dane wyjściowe wskazują, że korzysta ono z Eloquent ORM firmy Laravel, ponieważ komunikaty o błędach i wzorce zapytań są charakterystyczne dla konstruktora zapytań Eloquent.

Dla członków zespołu red team identyfikacja luk w zabezpieczeniach związanych z iniekcją ORM ma kluczowe znaczenie dla oceny poziomu bezpieczeństwa aplikacji. Iniekcja ORM może zostać wykorzystana, jeśli dane wejściowe użytkownika nie zostaną odpowiednio oczyszczone i zweryfikowane, co prowadzi do nieautoryzowanego dostępu lub manipulacji zapytaniami do bazy danych. Członkowie zespołu red team mogą wykryć te luki, stosując techniki takie jak ręczny przegląd kodu, automatyczne skanowanie i rygorystyczne testy walidacji danych wejściowych. Stosowanie bezpiecznych praktyk kodowania, takich jak parametryzowane zapytania i solidna walidacja danych wejściowych, jest niezbędne do ograniczenia ryzyka związanego z iniekcją ORM. Regularne przeglądy kodu i korzystanie z narzędzi bezpieczeństwa mogą pomóc programistom w identyfikacji i naprawie tych problemów.


W tym zadaniu zbadamy, w jaki sposób atakujący może wykorzystaćORMLuki w zabezpieczeniach, gdy ORM jest słabo wdrożony. Na początek odwiedź stronę internetową  [https://10-130-153-110.reverse-pełnomocnik.cell-prod-eu-west-3c.maszyna wirtualna.tryhackme.com](https://10-130-153-110.reverse-proxy.cell-prod-eu-west-3c.vm.tryhackme.com/) , gdzie znajdują się dwa pola wejściowe, umożliwiające wpisanie adresu e-mail.

![panel wyświetlający formularz wyszukiwania wiadomości e-mail](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719303122392)  

Przyjrzyjmy się bliżej kodowi źródłowemu wykorzystanemu przez programistę: Przyjrzyjmy się bliżej kodowi źródłowemu wykorzystanemu przez programistę dla pola wprowadzania **adresu e-mail (narażony na atak) :**

```php
public function searchBlindVulnerable(Request $request)
{
    $users = [];
    $email = $request->input('email');
    $users = Admins::whereRaw("email = '$email'")->get();
    if ($users) {
        return view('user', ['users' => $users]);
    } else {
        return view('user', ['message' => 'User not found']);
    }
}
```

  

Co robi ta funkcja  

Ten`searchBlindVulnerable()`Funkcja ta służy do pobierania rekordów użytkownika na podstawie parametru adresu e-mail podanego przez użytkownika. Oto szczegółowy opis funkcji:

- **Pobieranie danych wejściowych** : Funkcja przechwytuje `email` parametr z żądania HTTP. Odbywa się to za pomocą metody wprowadzania danych obiektu `$request`.
- **Konstruowanie zapytania** : Funkcja konstruuje następnie surowe zapytanie SQL przy użyciu `whereRaw()` metody Laravel, która bezpośrednio włącza wartość e-maila doSQLoświadczenie.
- **Wykonaj zapytanie** : To zapytanie jest wykonywane, a wynik jest zapisywany w `$users`zmiennej.
- **Return view** : Na koniec funkcja zwraca widok. Jeśli `$users`tablica nie jest pusta, przekazuje dane użytkownika do widoku; w przeciwnym razie przekazuje komunikat „ **Użytkownik nie został znaleziony** ”.

Kluczowym problemem w tej funkcji jest bezpośrednie użycie danych `whereRaw()` wprowadzanych przez użytkownika. Ta metoda konstruowania zapytań jest podatna na ataki typu injection, ponieważ nie oczyszcza danych wejściowych.

Atakujący może wykorzystać tę lukę, manipulując parametrem e-mail. Jeśli atakujący wprowadzi `1' OR '1'='1`, wynikowe zapytanie SQL będzie wyglądać następująco:

```php
SELECT * FROM users WHERE email = '1' OR '1'='1';
```

To zapytanie zawsze zwróci wszystkie rekordy użytkowników, ponieważ warunek „1”=„1” jest zawsze prawdziwy.

![Zerwany most reprezentujący wstrzyknięcie między bazą danych a kodem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1718912926278)

Szczegółowa eksploatacja 

- **Wprowadź złośliwą wartość** : atakujący odwiedza pole wprowadzania danych na stronie internetowej i wprowadza spreparowane dane, np `1' OR '1'='1`. .
- **Konstrukcja zapytania** :`searchBlindVulnerable()`Funkcja odbiera te dane wejściowe i konstruuje następujące zapytanie przy użyciu `whereRaw()`:

```php
$users = User::whereRaw("email = '1' OR '1'='1'")->get();
```

Ta surowa konstrukcja zapytania bezpośrednio wstawia złośliwe dane wejściowe do zapytania SQL.

- **Wykonywanie zapytania** : Eloquent ORM firmy Laravel tłumaczy to na polecenie SQL  `SELECT * FROM users WHERE email = '1' OR '1'='1';`.
- **Wynik** : Ponieważ `'1'='1'`argument zawsze ma wartość true, zapytanie zwraca wszystkie rekordy w tabeli użytkownika. Atakujący ma teraz dostęp do potencjalnie poufnych informacji o wszystkich użytkownikach w bazie danych, jak pokazano poniżej:

![formularz wyszukiwania po pomyślnym wstrzyknięciu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719304413178)  

Wdrażanie bezpiecznych zapytań ORM

Przyjrzyjmy się bezpiecznej wersji funkcji zapytania, aby pokazać, jak bezpieczna implementacja może chronić przed lukami w zabezpieczeniach związanymi z wstrzykiwaniem ORM. Używając zapytań parametryzowanych, możemy zapewnić prawidłowe oczyszczanie danych wprowadzanych przez użytkownika, znacznie zmniejszając ryzyko ataków wstrzykiwania. Oto bezpieczna implementacja funkcji za pośrednictwem pola wprowadzania **danych (bezpieczny adres e-mail)** :  

```php
public function searchBlindSecure(Request $request)
{
    $email = $request->input('email');
    $users = User::where('email', $email)->get();
    if (isset($users) && count($users) > 0) {
        return view('user', ['users' => $users]);
    } else {
        return view('user', ['message' => 'User not found']);
    }
}
```

  

Awaria bezpiecznej implementacji

- **Pobieranie danych wejściowych** : Funkcja przechwytuje parametr adresu e-mail z żądania HTTP, używając metody wprowadzania danych obiektu `$request`. Działa to tak samo, jak w wersji podatnej na atak.
- **Bezpieczne konstruowanie zapytania** : Zamiast metody `whereRaw()`, bezpieczna wersja korzysta z metody Eloquent `where()`. Metoda ta automatycznie usuwa znaki specjalne z danych wejściowych, zapobiegając w ten sposób atakom typu SQL injection. `where()`Metoda ta konstruuje sparametryzowane zapytanie w tle, zapewniając, że dane wejściowe użytkownika nie zostaną bezpośrednio uwzględnione w instrukcji SQL.
- **Wykonywanie zapytania** : Zapytanie jest wykonywane, a wynik zapisywany w `$users`zmiennej. Ponieważ zapytanie jest sparametryzowane, dane wejściowe są oczyszczane, co oznacza, że ​​nie mogą one naruszyć struktury zapytania SQL.
- **Zwracanie widoku** : Na koniec funkcja zwraca widok. Jeśli `$users` tablica zawiera dane, przekazuje dane użytkownika do widoku; w przeciwnym razie wyświetla komunikat o błędzie. Ta logika zapewnia przetwarzanie i wyświetlanie tylko prawidłowych danych.

Teraz spróbuj użyć tego samego złośliwego ładunku `1' OR '1'='1`z bezpieczną implementacją. Odwiedź stronę internetową  [https://10-130-153-110.reverse-proxy.cell-prod-eu-west-3c.vm.tryhackme.com](https://10-130-153-110.reverse-proxy.cell-prod-eu-west-3c.vm.tryhackme.com/) i wprowadź ładunek w polu wprowadzania **„E-mail (bezpieczny)”** . Po wprowadzeniu tych danych zauważysz, że aplikacja nie uszkadza ani nie zwraca wszystkich danych użytkownika.  Zamiast tego zachowuje się zgodnie z oczekiwaniami, albo nie znajduje użytkownika o tym adresie e-mail, albo zwraca odpowiednie dane użytkownika, jeśli podany adres e-mail jest prawidłowy, jak pokazano poniżej: 

![formularz wyszukiwania po nieudanej próbie wstrzyknięcia](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719304704357)

Dlaczego to jest bezpieczne

- **Zapytania sparametryzowane** : zapytania sparametryzowane zapewniają, że wartości wejściowe są traktowane wyłącznie jako dane, a nie jako kod wykonywalny. Zapobiega to wykonywaniu wstrzykniętego kodu SQL.
- **Automatyczne ukrywanie** : Eloquent automatycznie ukrywa wartości wejściowe, negując wszelkie znaki specjalne, które mogłyby zostać użyte do wstrzykiwania kodu SQL.
- **Spójna logika zapytań** : Dzięki stosowaniu metod Eloquent, takich jak `where()`, logika zapytań pozostaje spójna i przejrzysta, co ułatwia jej utrzymanie i audyt pod kątem bezpieczeństwa.  

Użycie `whereRaw()` w funkcji `searchBlindVulnerable()`wskazuje na słabą implementację ORM, co czyni aplikację wysoce podatną na ataki typu injection. Rozumiejąc, w jaki sposób dane wejściowe użytkownika są bezpośrednio włączane do zapytań SQL, atakujący mogą tworzyć dane wejściowe w celu manipulowania logiką zapytania. Podkreśla to wagę stosowania sparametryzowanych zapytań i prawidłowej walidacji danych wejściowych w celu zabezpieczenia aplikacji internetowych przed tego typu atakami.


Chociaż bezpieczne praktyki kodowania są niezbędne, ważne jest również rozpoznanie, w jaki sposób programista może nieumyślnie wdrożyć podatną na ataki wersjęORM, stwarzając możliwości wykorzystania luk. Implementacje podatne na ataki mogą wystąpić, gdy programiści używają **przestarzałych lub błędnie skonfigurowanych bibliotek ORM** , które zawierają wrodzone luki w zabezpieczeniach. Luki te mogą zostać wykorzystane przez atakujących do manipulowania zapytaniami do bazy danych i uzyskania nieautoryzowanego dostępu lub kontroli. Takie luki mogą wynikać z problemów, takich jak nieprawidłowa obsługa parametrów zapytania lub niewystarczająca ochrona przed atakami typu injection w samej infrastrukturze ORM. Programiści muszą upewnić się, że korzystają z aktualnych i bezpiecznych wersji bibliotek ORM, aby uniknąć wprowadzenia do swoich aplikacji luk, które mogą zostać wykorzystane.

Przykład praktyczny

Jednym z takich przykładów jest pakiet Laravel Query Builder, który miał znaczną lukę w zabezpieczeniach w wersjach wcześniejszych niż 1.17.1. Luka ta umożliwiałaSQLWstrzyknięcie za pomocą niesanityzowanych parametrów zapytania. Luka została zidentyfikowana w sposobie, w jaki pakiet obsługiwał parametry sortowania bezpośrednio z danych wprowadzonych przez użytkownika, bez odpowiedniej walidacji. Użyliśmy [kreatora zapytań Spatie.(otwiera się w nowej karcie)](https://github.com/spatie/laravel-query-builder)w tym przykładzie wykorzystano również wewnętrznie konstruktor zapytań Laravel do tworzenia zapytań.

Aby zademonstrować tę lukę w zabezpieczeniach, możesz uzyskać dostęp do maszyny pod adresem  [https://LAB_WEB_URL.p.thmlabs.com/query_users?sort=name(otwiera się w nowej karcie)](https://lab_web_url.p.thmlabs.com/query_users?sort=name)Ten punkt końcowy umożliwia sortowanie najlepszych użytkowników według `name`kolumny za pomocą `sort`parametru.

![odpowiedź po posortowaniu użytkowników według nazwy](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719171806193)  

Odpowiednikiem tłumaczenia tego zapytania w języku Laravel jest  `SELECT * FROM users ORDER BY name ASC LIMIT 2`.

**Próba wstrzyknięcia**

Jeśli spróbujemy wstrzyknąć parametr name za pomocą `name'`, zobaczymy, że aplikacja zwróci błąd informujący o tym, że nie mogła znaleźć nazwy kolumny.

![próba wstrzyknięcia złośliwego kodu wejściowego](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719479019501)  

Naszym celem jest takie manipulowanie zapytaniem, aby pobrać kompletne dane z  `users` tabeli, zamiast ograniczać się do określonej liczby wierszy.  

Jednak wstrzyknięcie parametru sortowania w tym kontekście nie jest proste – wystarczy połączyć go z zapytaniem `SELECT`i zastosować rutynowe metody wstrzykiwania. Wyzwanie polega na efektywnym wyjściu poza klauzulę ORDER BY, aby manipulować wykonaniem zapytania. Aby to osiągnąć, możemy wykorzystać specjalną funkcję: - [>(otwiera się w nowej karcie)](https://dev.mysql.com/doc/refman/8.4/en/json.html)Operator, który służy jako alias dla `json_extract`funkcji w MySQL. Ten operator pozwala nam nawigowaćJSONdanych i wyodrębnić określone wartości. Używając `->`operatora w połączeniu z `"%27))`danymi, możemy wyjść poza klauzulę ORDER BY. `->"%27))`Dane skutecznie kończą ekstrakcję JSON, omijają ograniczenia narzucone przez zapytanie początkowe  i pozwalają nam dołączyć dodatkowe polecenia SQL.

**Ostateczny ładunek**

Przygotujemy ostateczny ładunek w następujący sposób:

- **Zapytanie początkowe** : zapytanie początkowe, które Laravel tłumaczy w celu sortowania użytkowników według nazwy, to  `SELECT * FROM users ORDER BY name ASC LIMIT 2`.
- **Przerwanie zapytania** : Wstrzykując `name->"%27))`, możemy spowodować przerwanie zapytania i w ten sposób stworzyć okazję do wstawienia własnego kodu SQL.
- **Tworzenie ładunku** : Aby wykorzystać lukę, tworzymy ładunek, który wyłamuje się z ciągu i wstrzykuje nasz kod SQL. Ładunek wyglądałby mniej więcej tak `name->"%27)) SQL INJECTION QUERY #`: . W obrębie wartości parametru  `name->`, `->`jest parsowany przez Laravel i zastępowany funkcją JSON MySQL. Z drugiej strony,  `"%27))`zamyka poprzedni ciąg i warunek. `SQL INJECTION QUERY` Pozwala atakującemu na napisanie własnego zapytania. Znak ten  `#` zakomentowuje resztę zapytania, aby zapobiec błędom składniowym.
- **Wynik końcowy** : Dane potrzebne do pobrania dodatkowych wierszy z bazy danych będą wyglądać następująco:  [https://LAB_WEB_URL.p.thmlabs.com/query_users?sort=name-%3E%22%27))%20LIMIT%2010%23(otwiera się w nowej karcie)](https://lab_web_url.p.thmlabs.com/query_users?sort=name-%3E%22%27\)\)%20LIMIT%2010%23), podczas gdy zapytanie wygenerowane przez Laravel do bazy danych MySQL uwzględniałoby  ``SELECT * FROM `users` ORDER BY json_unquote(json_extract(`name`, '$.""')) LIMIT 10#"')) ASC LIMIT 2`` wstrzyknięty ładunek. Powyższe zapytanie ominęłoby ograniczenie i pobrało 10 wierszy z tabeli.

![udane wstrzyknięcie w celu uzyskania maksymalnej liczby wierszy z tabeli użytkowników](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1719171665479)  

Powyższy przykład podkreśla kluczowe znaczenie walidacji i sanityzacji danych wejściowych w zapobieganiu podatnościom na wstrzyknięcia ORM. Rozumiejąc, jak pozornie nieszkodliwe parametry zapytania mogą zostać wykorzystane, programiści mogą lepiej docenić potrzebę stosowania bezpiecznych praktyk kodowania. Korzystanie z funkcji ORM bez odpowiedniego zrozumienia ich konsekwencji może nieumyślnie narazić aplikacje na poważne zagrożenia bezpieczeństwa.


Teraz, gdy rozumiemy powierzchnię zagrożenia,ORMZapobieganie tym lukom wymaga wdrożenia solidnych środków bezpieczeństwa i ciągłego monitorowania potencjalnych słabych punktów. W poniższych sekcjach przedstawiono najlepsze praktyki w zakresie zabezpieczania danych wprowadzanych przez użytkowników i wykorzystywania technik automatyzacji w celu skutecznej identyfikacji i minimalizacji luk w zabezpieczeniach związanych z wstrzykiwaniem.![](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1718912983084)

Kilka ważnych praktyk

- **Walidacja danych wejściowych** : Zawsze waliduj dane wprowadzane przez użytkownika zarówno po stronie klienta, jak i serwera. Upewnij się, że dane są zgodne z oczekiwanym formatem, typem i długością. Użyj wyrażeń regularnych i wbudowanych funkcji walidacyjnych, aby wymusić rygorystyczne zasady walidacji danych wejściowych.
- **Zapytania sparametryzowane** : Użyj sparametryzowanych zapytań (przygotowanych instrukcji) do interakcji z bazą danych. Takie podejście gwarantuje, że dane wprowadzane przez użytkownika są traktowane jako dane, a nie jako kod wykonywalny. Unikaj bezpośredniego łączenia danych wprowadzanych przez użytkownika z bazą danych.SQLzapytania.
- **Użycie ORM** : Wykorzystaj wbudowane narzędzia ORM do interakcji z bazą danych. ORM-y abstrahują zapytania SQL i pomagają zapobiegać atakom typu SQL injection poprzez bezpieczne przetwarzanie danych wprowadzanych przez użytkownika. Upewnij się, że ORM jest poprawnie skonfigurowany i że wszystkie niestandardowe zapytania SQL są sparametryzowane.
- **Ucieczka i sanityzacja** : Ucieczka danych wprowadzanych przez użytkownika w celu usunięcia wszelkich znaków specjalnych używanych do ataków typu injection. Sanityzacja danych wprowadzanych w celu usunięcia potencjalnie szkodliwych danych przed ich przetworzeniem lub zapisaniem.
- **Lista dozwolonych danych wejściowych** : Wdróż podejście z listą dozwolonych danych wejściowych. Dopuszczaj tylko określone, oczekiwane wartości i odrzucaj wszystkie inne. Ta metoda jest bezpieczniejsza niż blokowanie znanych, nieprawidłowych wartości, które mogą być niekompletne.

Aplikacja w popularnych frameworkach

Przyjrzymy się podstawowym praktykom ochrony przed wstrzyknięciem ORM w powszechnie stosowanych frameworkach ORM. Narzędzia ORM, takie jak Doctrine (PHP), SQLAlchemy (Python), Hibernate (Java) i Entity Framework (.NET) zapewniają zaawansowane abstrakcje dla interakcji z bazami danych. Aby jednak zapobiec podatnościom na ataki typu SQL injection, kluczowe jest stosowanie bezpiecznych praktyk kodowania, takich jak parametryzowane zapytania, parametry nazwane i techniki specyficzne dla ORM. Przyjrzyjmy się tym najlepszym praktykom wraz z praktycznymi przykładami dla każdego frameworka:

**Doktryna (PHP)**

Używaj przygotowanych instrukcji z parametryzowanymi zapytaniami, aby zapobiegać atakom typu SQL injection.

```php
$query = $entityManager->createQuery('SELECT u FROM User u WHERE u.username = :username');
$query->setParameter('username', $username);
$users = $query->getResult();
```

**SQLAlchemy (Python)**

Wykorzystaj ORM i zapytania SQLAlchemyAPIaby używać sparametryzowanych zapytań, które automatycznie obsługują uciekanie i wiązanie parametrów.

```php
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
user = session.query(User).filter_by(username=username).first()
```

**Hibernacja (Java)**

Użyj nazwanych parametrów z interfejsem API zapytań Hibernate, aby mieć pewność, że dane wejściowe są odpowiednio powiązane i zabezpieczone znakami ucieczki.

```php
String hql = "FROM User WHERE username = :username";
Query query = session.createQuery(hql);
query.setParameter("username", username);
List results = query.list();
```

**Entity Framework (.NET)**

Stosuj sparametryzowane zapytania w Entity Framework, aby zabezpieczyć interakcje z bazami danych i ograniczyć ryzyko ataków typu SQL injection.

```php
var user = context.Users.FirstOrDefault(u => u.Username == username);
```

Praktyki te podkreślają znaczenie przyjęcia bezpiecznych praktyk kodowania dostosowanych do każdego frameworka ORM, gwarantujących solidną ochronę przed lukami w zabezpieczeniach polegającymi na wstrzykiwaniu kodu ORM.



Podczas naszej eksploracjiORMW ramach projektu injection zaczęliśmy od gruntownego zrozumienia istoty ORM i jego fundamentalnej roli we współczesnym tworzeniu stron internetowych. Zbadaliśmy jego działanie, rozumiejąc, w jaki sposób ORM abstrakcyjnie przekształcają interakcje z bazami danych w paradygmaty obiektowe, zwiększając produktywność programistów i łatwość utrzymania kodu.

W dalszej części skupiliśmy się na perspektywie testera penetracyjnego, ucząc się, jak identyfikować potencjalne luki w zabezpieczeniach, szczególnie w Laravelu, powszechnie używanym środowiskuPHPDzięki tej podstawowej wiedzy zbadaliśmy wykorzystanie słabo wdrożonych systemów ORM. Odkryliśmy, jak luki w zabezpieczeniach konfiguracji ORM mogą prowadzić do ataków typu injection, umożliwiając złośliwym podmiotom manipulowanie zapytaniami do bazy danych i potencjalnie uzyskanie nieautoryzowanego dostępu do poufnych informacji.

Podsumowując, podkreśliliśmy podstawowe praktyki bezpieczeństwa w popularnych frameworkach. Obejmują one rygorystyczną walidację danych wejściowych, prawidłowe użycie sparametryzowanych zapytań lub przygotowanych instrukcji w celu ograniczenia ryzyka wstrzyknięcia oraz wykorzystanie frameworków ORM z wbudowanymi funkcjami bezpieczeństwa. Stosując te praktyki, programiści mogą chronić swoje aplikacje przed lukami w zabezpieczeniach związanymi z wstrzyknięciem ORM, zapewniając dobrze chronioną i bezpieczną aplikację internetową.