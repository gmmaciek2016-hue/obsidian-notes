
W tym pokoju dowiesz się o wstrzykiwaniu kodu NoSQL.SQLBazy danych oparte na SQL są popularnym wyborem do przechowywania danych w aplikacjach internetowych, istnieje również kilka opcji baz danych, które nie są oparte na SQL. Rozwiązania bazodanowe, takie jak MongoDB, rozwiązanie bazodanowe NoSQL, odnotowały w ostatnich latach znaczny wzrost popularności. Jednak podstawowa zasada ataków typu injection pozostaje ta sama. Jeśli mamy możliwość wstrzyknięcia kodu do samego zapytania do bazy danych, mamy możliwość manipulowania nim!

Wymagania wstępne

- [Burp SuitePodstawy](https://tryhackme.com/r/room/burpsuitebasics)
- [Powtarzacz Burp Suite](https://tryhackme.com/r/room/burpsuiterepeater)
- [Burp Suite: Intruz](https://tryhackme.com/r/room/burpsuiteintruder)  
    
- [Wstrzyknięcie SQL](https://tryhackme.com/r/room/sqlinjectionlm)

Cele edukacyjne

- Zrozum, czym jest NoSQL
- Zrozum, jak działają bazy danych NoSQL, przechowują dane i komunikują się z nimi
- Poznaj różne typy ataków typu NoSQL injection
- Dowiedz się, jak praktycznie wykorzystać lukę w zabezpieczeniach NoSQL


Zanim poznamy mechanizm wstrzykiwania NoSQL, przyjrzyjmy się najpierw, jak działają bazy danych NoSQL. W tym pomieszczeniu skupimy się na MongoDB. Chociaż istnieją inne rozwiązania NoSQL, zasady dotyczące ataków wstrzykiwania w MongoDB można zastosować do dowolnej bazy danych NoSQL.  

MongoDB

Podobnie jak MySQL, MariaDB czy PostgreSQL, MongoDB to kolejna baza danych, w której można przechowywać dane w uporządkowany sposób. MongoDB umożliwia szybkie i ustrukturyzowane pobieranie podzbiorów danych. Jeśli znasz relacyjne bazy danych, możesz założyć, że MongoDB działa podobnie do każdej innej bazy danych. Głównym wyjątkiem jest to, że informacje nie są przechowywane w tabelach, lecz w  dokumentach .  

Można je traktować jako prostą strukturę słownikową, w której przechowywane są pary klucz-wartość. Pod pewnymi względami są one bardzo podobne do tego, co nazwalibyśmy rekordem w tradycyjnej relacyjnej bazie danych, ale informacje są po prostu przechowywane inaczej. Załóżmy na przykład, że tworzymy aplikację internetową dla działu kadr i chcemy przechowywać podstawowe informacje o pracownikach. Następnie utworzylibyśmy dokument dla każdego pracownika zawierający dane w formacie, który wygląda następująco:

`{"_id" : ObjectId("5f077332de2cdf808d26cd74"), "username" : "lphillips", "first_name" : "Logan", "last_name" : "Phillips", "age" : "65", "email" : "lphillips@example.com" }`  

Jak widać, dokumenty w MongoDB są przechowywane w tablicy asocjacyjnej zawierającej dowolną liczbę pól.  

MongoDB pozwala grupować wiele dokumentów o podobnej funkcji w struktury wyższej hierarchii, zwane  kolekcjami  , w celach organizacyjnych. Kolekcje są odpowiednikiem tabel w relacyjnych bazach danych. Kontynuując nasz przykład z działu HR, wszystkie dokumenty pracownika można by wygodnie zgrupować w kolekcji o nazwie „ludzie”, jak pokazano na poniższym diagramie.

![Kolekcja MongoDB](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679544440.png)

Kolekcje są ostatecznie grupowane w  bazach danych , które stanowią najwyższy element hierarchiczny w MongoDB. W relacyjnych bazach danych koncepcja bazy danych grupuje tabele. W MongoDB grupuje ona powiązane kolekcje.

![Kolekcja MongoDB](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679596244.png)  

Zapytanie do bazy danych

Jak w przypadku każdej bazy danych, do pobierania informacji z bazy używany jest specjalny język. Tak jak bazy relacyjne wykorzystują pewną odmianę języka SQL, bazy nierelacyjne, takie jak MongoDB, korzystają z NoSQL. Ogólnie rzecz biorąc, NoSQL odnosi się do dowolnego sposobu wykonywania zapytań do bazy danych, który nie jest SQL, co oznacza, że ​​może się on różnić w zależności od używanej bazy danych.  

W MongoDB zapytania wykorzystują ustrukturyzowaną tablicę asocjacyjną, która zawiera grupy kryteriów, które należy spełnić, aby filtrować informacje. Filtry te oferują funkcjonalność podobną do klauzuli WHERE w SQL i umożliwiają operatorom tworzenie złożonych zapytań w razie potrzeby.

Aby lepiej zrozumieć zapytania NoSQL, załóżmy, że mamy bazę danych zawierającą zbiór osób zawierający następujące trzy dokumenty:

![Kolekcja MongoDB](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679617512.png)  

Gdybyśmy chcieli zbudować filtr, który pobierałby tylko dokumenty, w których nazwisko to „Sandler”, nasz filtr wyglądałby następująco:  

`**['last_name' => 'Sandler']**`

W rezultacie zapytanie to zwraca tylko drugi dokument.

Jeśli chcielibyśmy filtrować dokumenty, w których płeć jest męska, a nazwisko brzmi Phillips, zastosowalibyśmy następujący filtr:

`**['gender' => 'male', 'last_name' => 'Phillips']**`

Zwrócony zostanie tylko pierwszy dokument.

Gdybyśmy chcieli pobrać wszystkie dokumenty, w których wiek jest niższy niż 50 lat, moglibyśmy użyć następującego filtra:

`**['age' => ['$lt'=>'50']]**`

Zwróci to drugi i trzeci dokument. Zwróć uwagę, że używamy operatora **$lt** w zagnieżdżonej tablicy. Operatory umożliwiają bardziej złożone filtry poprzez zagnieżdżanie warunków. Pełną listę możliwych operatorów można znaleźć pod poniższym linkiem:

[Odwołanie do operatora MongoDB(otwiera się w nowej karcie)](https://docs.mongodb.com/manual/reference/operator/query/)


﻿Najpierw uruchommy **maszynę laboratoryjną** , naciskając przycisk „ **Uruchom maszynę laboratoryjną”** u góry tego zadania. Możesz uzyskać dostęp doMaszyna wirtualnaużywając **AttackBox** lub twojego**VPN**połączenie. Gdy urządzenie będzie gotowe, przejdź do[http://IP_MASZYNY(otwiera się w nowej karcie)](http://machine_ip/)aby rozpocząć ćwiczenie.  

Wstrzyknięcie to wstrzyknięcie

Choć rozważania na temat ataków typu NoSQL Injection mogą wydawać się skomplikowane, gdy sprowadzimy je do samej istoty, możemy zrozumieć podobieństwa między nimiSQLWstrzykiwanie i wstrzykiwanie NoSQL.

Podstawową przyczyną ataku typu „injection” jest nieprawidłowe łączenie danych wprowadzanych przez użytkownika, które nie są wiarygodne, z poleceniem, co pozwala atakującemu na modyfikację samego polecenia. W przypadku ataku typu „SQL injection” najczęstszym podejściem jest wstrzyknięcie pojedynczego lub podwójnego cudzysłowu, który przerywa bieżącą konkatenację danych i umożliwia atakującemu modyfikację zapytania. To samo podejście dotyczy ataku typu „NoSQL Injection”. Jeśli dane wprowadzane przez użytkownika, które nie są wiarygodne, zostaną bezpośrednio dodane do zapytania, mamy możliwość modyfikacji samego zapytania. Jednak w przypadku ataku typu „NoSQL Injection”, nawet jeśli nie możemy uciec od bieżącego zapytania, nadal mamy możliwość manipulowania nim. Dlatego istnieją dwa główne typy ataku typu „NoSQL Injection”:

- **Wstrzyknięcie składni** – jest podobne do wstrzyknięcia SQL, gdzie mamy możliwość wyrwania się z zapytania i wstrzyknięcia własnego ładunku. Kluczową różnicą w stosunku do wstrzyknięcia SQL jest składnia używana do przeprowadzenia ataku wstrzyknięcia.
- **Wstrzykiwanie operatora** — nawet jeśli nie możemy wydostać się z zapytania, potencjalnie możemy wstrzyknąć operator zapytania NoSQL, który manipuluje zachowaniem zapytania, umożliwiając nam przeprowadzanie ataków, takich jak omijanie uwierzytelniania.

W tej sali skupimy się na wstrzykiwaniu operatorów i różnych sposobach jego wykorzystania. Wynika to z faktu, że przypadki wstrzykiwania składni nie zdarzają się tak często, ponieważ większość bibliotek używanych do tworzenia zapytań stosuje filtry, które zapobiegają wstrzykiwaniu składni. Jednak ze względu na zmienność danych wprowadzanych przez użytkownika, te same filtry często mogą być podatne na wstrzykiwanie operatorów. Przykład wstrzykiwania składni omówimy na końcu sali.  

Jak wstrzyknąć NoSQL

Patrząc na sposób budowy filtrów NoSQL, ominięcie ich w celu wstrzyknięcia dowolnego ładunku może wydawać się niemożliwe, ponieważ opierają się one na tworzeniu ustrukturyzowanej tablicy. W przeciwieństwie do wstrzykiwania SQL, gdzie zapytania były zazwyczaj budowane poprzez prostą konkatenację ciągów znaków, zapytania NoSQL wymagają zagnieżdżonych tablic asocjacyjnych. Z punktu widzenia atakującego oznacza to, że aby wstrzyknąć NoSQL, trzeba mieć możliwość wstrzyknięcia tablic do aplikacji.  

Na szczęście dla nas, wiele języków programowania po stronie serwera pozwala na przekazywanie zmiennych tablicowych za pomocą specjalnej składni w ciągu zapytania żądania HTTP. Na potrzeby tego przykładu skupmy się na poniższym kodzie napisanym wPHPdla prostej strony logowania:

```php
<?php
$con = new MongoDB\Driver\Manager("mongodb://localhost:27017");


if(isset($_POST) && isset($_POST['user']) && isset($_POST['pass'])){
        $user = $_POST['user'];
        $pass = $_POST['pass'];

        $q = new MongoDB\Driver\Query(['username'=>$user, 'password'=>$pass]);
        $record = $con->executeQuery('myapp.login', $q );
        $record = iterator_to_array($record);

        if(sizeof($record)>0){
                $usr = $record[0];

                session_start();
                $_SESSION['loggedin'] = true;
                $_SESSION['uid'] = $usr->username;

                header('Location: /sekr3tPl4ce.php');
                die();
        }
}
header('Location: /?err=1');

?>
```

Aplikacja internetowa wysyła zapytanie do MongoDB, korzystając z bazy danych „ **myapp** ” i kolekcji „ **login** ”, żądając każdego dokumentu, który przejdzie filtr `**['username'=>$user, 'password'=>$pass]**`, gdzie zarówno **$user** , jak i **$pass** są pobierane bezpośrednio z parametrów HTTP POST. Przyjrzyjmy się, jak możemy wykorzystać wstrzykiwanie operatora (Operator Injection) w celu ominięcia uwierzytelniania.  

Gdybyśmy mogli w jakiś sposób wysłać tablicę do zmiennych **$user** i **$pass** z następującą zawartością:  

`**$user = ['$ne'=>'xxxx']**` 

`**$pass = ['$ne'=>'yyyy']**` 

Wynikowy filtr wyglądałby następująco:  

`**['username'=>['$ne'=>'xxxx'], 'password'=>['$ne'=>'yyyy']]**`

Moglibyśmy oszukać bazę danych, aby zwracała każdy dokument, w którym nazwa użytkownika nie jest równa „ **xxxx** ”, a hasło nie jest równe „ **yyyy** ”. To prawdopodobnie zwróciłoby wszystkie dokumenty z kolekcji loginów. W rezultacie aplikacja uznałaby, że logowanie zostało wykonane poprawnie i zezwoliłaby nam na dostęp z uprawnieniami użytkownika odpowiadającymi pierwszemu dokumentowi pobranemu z bazy danych .

Problem, który pozostaje nierozwiązany, to jak przekazać tablicę w ramach żądania HTTP POST. Okazuje się, że PHP i wiele innych języków programowania pozwala na przekazanie tablicy za pomocą następującej notacji w treści żądania POST:

`**user[$ne]=xxxx&pass[$ne]=yyyy**`

Więc odpalmy naszego ulubionego pełnomocniki spróbuj to przetestować. W tym poradniku użyjemy Burp Proxy.


Omijanie ekranu logowania

Przede wszystkim otwórzmy stronę internetową [http://IP_MASZYNY/(otwiera się w nowej karcie)](http://machine_ip/) i wyślij nieprawidłowego użytkownika/hasło, aby przechwycić żądanie w Burp:

![Widok witryny](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679685897.png)  

Oryginalne przechwycone żądanie logowania wygląda następująco:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679753604.png)  

Teraz przystępujemy do przechwycenia kolejnego żądania logowania i modyfikacji użytkownika oraz przekazania zmiennych w celu wysłania pożądanych tablic:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679773572.png)  

Wymusza to na bazie danych zwrócenie wszystkich dokumentów użytkownika, w wyniku czego jesteśmy ostatecznie zalogowani do aplikacji:

![Widok witryny](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679795855.png)  

Odpowiedz na poniższe pytania

Jeśli pomijasz ekran logowania za pomocą operatora $ne, jaki jest adres e-mail użytkownika, jako którego jesteś zalogowany?



Logowanie jako inni użytkownicy

Udało nam się ominąć ekran logowania aplikacji, ale dzięki tej technice możemy zalogować się tylko jako pierwszy użytkownik zwrócony przez bazę danych. Korzystając z operatora $nin, zmodyfikujemy nasz ładunek, aby móc kontrolować, którego użytkownika chcemy uzyskać.

Po pierwsze, operator $nin pozwala nam utworzyć filtr, określając kryteria, w których żądane dokumenty zawierają jakieś pole, a nie listę wartości. Jeśli więc chcemy zalogować się jako dowolny użytkownik poza użytkownikiem admin, możemy zmodyfikować nasz ładunek, aby wyglądał tak:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679859318.png)  

Oznaczałoby to filtr o następującej strukturze:

`**['username'=>['$nin'=>['admin'] ], 'password'=>['$ne'=>'aweasdf']]**`

Co oznacza, że ​​baza danych zwraca każdego użytkownika, którego nazwa użytkownika nie jest admin, a hasło nie jest aweasdf. W rezultacie uzyskujemy dostęp do konta innego użytkownika.

Zauważ, że operator $nin otrzymuje listę wartości do zignorowania. Możemy ją dalej rozszerzać, dostosowując nasz ładunek w następujący sposób:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679886213.png)  

Spowodowałoby to powstanie takiego filtra:  

`**['username'=>['$nin'=>['admin', 'jude'] ], 'password'=>['$ne'=>'aweasdf']]**`

Można to powtarzać tyle razy, ile potrzeba, aż uzyskamy dostęp do wszystkich dostępnych kont.

**Uwaga: `jude`Użytkownik powyżej nie jest faktycznym użytkownikiem, lecz przykładem tego, jak można dodać dodatkową nazwę użytkownika.**


Wyodrębnianie haseł użytkowników

W tym momencie mamy dostęp do wszystkich kont w aplikacji. Ważne jest jednak, aby spróbować wyodrębnić faktycznie używane hasła, ponieważ mogą one zostać ponownie wykorzystane w innych usługach. Aby to osiągnąć, wykorzystamy operator $regex do zadania serwerowi serii pytań, które pozwolą nam odzyskać hasła w procesie przypominającym grę w wisielca.

Najpierw weźmy jednego z użytkowników, których wcześniej odkryliśmy, i spróbujmy odgadnąć długość jego hasła. Użyjemy do tego następującego kodu:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679978838.png)  

Zauważ, że pytamy bazę danych, czy istnieje użytkownik o nazwie admin i haśle pasującym do wyrażenia regularnego: `**^.{7}$**`. To w zasadzie słowo wieloznaczne o długości 7. Ponieważ serwer odpowiada błędem logowania, wiemy, że długość hasła dla użytkownika admin nie wynosi 7. Po kilku próbach i błędach w końcu doszliśmy do poprawnej odpowiedzi:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/617be9330b818bf2ed2c31f779be7c17.png)  

Wiemy już, że hasło użytkownika admin ma długość 5. Aby ustalić faktyczną zawartość, modyfikujemy nasz ładunek w następujący sposób:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719679996762.png)  

Pracujemy teraz z wyrażeniem regularnym o długości 5 (pojedyncza litera c plus 4 kropki), dopasowując odkrytą długość hasła i pytając, czy hasło administratora pasuje do wyrażenia regularnego `^c....$`, co oznacza, że ​​zaczyna się od małej litery c, po której następują dowolne 4 znaki. Ponieważ odpowiedź serwera to nieprawidłowe logowanie, wiemy teraz, że pierwsza litera hasła nie może być „c”. Kontynuujemy iterację po wszystkich dostępnych znakach, aż otrzymamy pomyślną odpowiedź od serwera:

![Prośba o beknięcie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1719680018918.png)  

Potwierdza to, że pierwszą literą hasła administratora jest „a”. Tę samą procedurę można powtórzyć dla pozostałych liter, aż do odzyskania pełnego hasła. W razie potrzeby można to powtórzyć również dla innych użytkowników.


Znajdowanie wstrzykiwania składni  

Skoro omówiliśmy wstrzykiwanie operatorów, przyjrzyjmy się przykładowi wstrzykiwania składni. Aplikacja Pythona jest uruchomiona, aby umożliwić Ci otrzymanie adresu e-mail dowolnej podanej nazwy użytkownika. Aby skorzystać z aplikacji, należy uwierzytelnić się za pomocąSSHkorzystając `ssh syntax@MACHINE_IP`z poniższych danych uwierzytelniających:

![Klucz THM](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/5d471dd234b7fc4eb4edea3c934663c1.png)

|   |   |
|---|---|
|**Nazwa użytkownika**|składnia|
|**Hasło**|składnia|

Po uwierzytelnieniu możesz podać nazwę użytkownika jako dane wejściowe. Zacznijmy od podania `admin`:

**Terminal**

```shell
ssh syntax@MACHINE_IP
syntax@MACHINE_IP's password: 
Please provide the username to receive their email:admin
admin@nosql.int
Connection to MACHINE_IP closed.
```

Możemy zacząć testować pod kątem wstrzyknięcia składni, po prostu wstrzykując `'`znak, co spowoduje błąd widoczny w odpowiedzi poniżej:

**Terminal**

```shell
syntax@MACHINE_IP's password: 
Please provide the username to receive their email:admin'
Traceback (most recent call last):
  File "/home/syntax/script.py", line 17, in <module>
    for x in mycol.find({"$where": "this.username == '" + username + "'"}):
  File "/usr/local/lib/python3.6/dist-packages/pymongo/cursor.py", line 1248, in next
    if len(self.__data) or self._refresh():
  File "/usr/local/lib/python3.6/dist-packages/pymongo/cursor.py", line 1165, in _refresh
    self.__send_message(q)
  File "/usr/local/lib/python3.6/dist-packages/pymongo/cursor.py", line 1053, in __send_message
    operation, self._unpack_response, address=self.__address
  File "/usr/local/lib/python3.6/dist-packages/pymongo/mongo_client.py", line 1272, in _run_operation
    retryable=isinstance(operation, message._Query),
  File "/usr/local/lib/python3.6/dist-packages/pymongo/mongo_client.py", line 1371, in _retryable_read
    return func(session, server, sock_info, read_pref)
  File "/usr/local/lib/python3.6/dist-packages/pymongo/mongo_client.py", line 1264, in _cmd
    sock_info, operation, read_preference, self._event_listeners, unpack_res
  File "/usr/local/lib/python3.6/dist-packages/pymongo/server.py", line 134, in run_operation
    _check_command_response(first, sock_info.max_wire_version)
  File "/usr/local/lib/python3.6/dist-packages/pymongo/helpers.py", line 180, in _check_command_response
    raise OperationFailure(errmsg, code, response, max_wire_version)
pymongo.errors.OperationFailure: Failed to call method, full error: {'ok': 0.0, 'errmsg': 'Failed to call method', 'code': 1, 'codeName': 'InternalError'}
Connection to MACHINE_IP closed.
```

Poniższy wiersz w komunikacie o błędzie pokazuje nam, że występuje atak typu Syntax Injection:

`for x in mycol.find({"$where": "this.username == '" + username + "'"}):`

Widzimy, że zmienna username jest bezpośrednio łączona z ciągiem zapytania i że w poleceniu find wykonywana jest funkcja JavaScript, co pozwala nam na wstrzyknięcie składni. W tym przypadku mamy szczegółowe komunikaty o błędach, które wskazują na możliwość wstrzyknięcia. Jednak nawet bez szczegółowych komunikatów o błędach moglibyśmy przetestować wstrzyknięcie składni, podając zarówno warunek fałsz, jak i prawdę, i sprawdzając, czy dane wyjściowe się różnią, jak pokazano w poniższym przykładzie:

**Terminal**

```shell
ssh syntax@MACHINE_IP
syntax@MACHINE_IP's password: 
Please provide the username to receive their email:admin' && 0 && 'x
Connection to MACHINE_IP closed.

ssh syntax@MACHINE_IP
syntax@MACHINE_IP's password: 
Please provide the username to receive their email:admin' && 1 && 'x
admin@nosql.int
Connection to MACHINE_IP closed.
```

Wykorzystanie wstrzykiwania składni

Teraz, gdy potwierdziliśmy atak typu Syntax Injection, możemy wykorzystać ten punkt wstrzyknięcia do pobrania wszystkich adresów e-mail. Aby to zrobić, musimy upewnić się, że testowe wyrażenie warunku zawsze zwraca wartość true. Podczas wstrzyknięcia do kodu JavaScript możemy użyć ładunku  `'||1||'`. Wykorzystajmy to do ujawnienia poufnych informacji:

**Terminal**

```shell
ssh syntax@MACHINE_IP
syntax@MACHINE_IP's password: 
Please provide the username to receive their email:admin'||1||'
admin@nosql.int
pcollins@nosql.int
jsmith@nosql.int
[...]
Connection to MACHINE_IP closed.
```

Wyjątek od reguły

Warto zauważyć, że aby doszło do wstrzyknięcia składni, programista musi utworzyć niestandardowe zapytania JavaScript. Tę samą funkcję można wykonać za pomocą wbudowanych funkcji filtrujących, które `['username' : username]`zwrócą ten sam wynik, ale nie będą podatne na wstrzyknięcie. Z tego powodu wstrzyknięcie składni jest rzadkością, ponieważ oznacza to, że programiści nie korzystają z wbudowanych funkcji i filtrów. Chociaż niektóre złożone zapytania mogą wymagać bezpośredniego JavaScript, zawsze zaleca się unikanie tego, aby zapobiec wstrzyknięciu składni. Powyższy przykład dotyczy MongoDB; w przypadku innych rozwiązań NoSQL mogą występować podobne przypadki wstrzyknięcia składni, ale rzeczywista składnia będzie inna.


Obrona

Aby bronić się przed atakami typu NoSQL Injection, kluczowym sposobem jest upewnienie się, że nie ma pomyłki między zapytaniem a danymi wprowadzonymi przez użytkownika. Można to rozwiązać, stosując sparametryzowane zapytania, które oddzielają polecenie zapytania od danych wprowadzonych przez użytkownika, uniemożliwiając pomylenie silnika. Ponadto, aby uniknąć ataków typu Syntax Injection, należy zawsze korzystać z wbudowanych funkcji i filtrów rozwiązania NoSQL. Wreszcie, walidacja i sanityzacja danych wejściowych mogą być również wykorzystane do filtrowania składni i znaków operatorów oraz ich usuwania.