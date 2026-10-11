---

Uwierzytelnianie to proces, w którym aplikacja internetowa weryfikuje tożsamość użytkownika wysyłającego żądanie. Zazwyczaj odbywa się to na serwerze aplikacji, który porównuje dane uwierzytelniające przesłane przez klienta z rekordami przechowywanymi w magazynie danych uwierzytelniających. Gdy dane uwierzytelniające są zgodne, serwer wydaje token sesji, który jest zwracany przy każdym kolejnym żądaniu aż do wygaśnięcia sesji. Aplikacja wykorzystuje ten token do decydowania, co żądanie może wykonać.

Obejście uwierzytelniania to atak, który umożliwia użytkownikowi dostęp do funkcji ograniczonych do danego konta bez podania prawidłowych danych uwierzytelniających dla tego konta. Ataki z obejściem uwierzytelniania nie zawsze wymagają odgadnięcia hasła lub kradzieży tokena sesji. Wiele z nich jest skutecznych, wykorzystując założenia programisty dotyczące sposobu uwierzytelniania lub modyfikując dane, którym serwer ufa bez niezależnej weryfikacji.

![Obraz przedstawiający przepływ uwierzytelniania|697](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1776682922179.svg)

## Środowisko docelowe

Uruchom maszynę przyciskiem u góry tego zadania i poczekaj, aż adres IP pojawi się w banerze, zanim przejdziesz dalej. Wszystkie narzędzia używane w tym pokoju są preinstalowane na AttackBoxie, który można uruchomić zielonym przyciskiem u góry ekranu.

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Wymień prawidłowe nazwy użytkowników na podstawie różnic w odpowiedzi formularza rejestracyjnego za pomocą`ffuf`
- Złamanie formularza logowania metodą brute-force przy użyciu niestandardowej listy nazw użytkowników i listy słów kluczowych hasła
- Zidentyfikuj i wykorzystaj lukę w parametrach zanieczyszczenia w procesie resetowania hasła za pomocą`curl`
- Modyfikuj zwykły tekst, pliki cookie z haszowaniem i zakodowane w formacie Base64, aby zmienić stan uwierzytelnienia, jaki widzi serwer

Wiele rodzajów luk może prowadzić do ominięcia uwierzytelniania. Najczęściej jednak występują cztery techniki, które powtarzają się w testach w warunkach rzeczywistych: enumeracja nazw użytkowników, atak brute force na dane uwierzytelniające, błędy logiczne w odzyskiwaniu kont oraz manipulacja plikami cookie. Każda z nich atakuje inny komponent stosu uwierzytelniania i wymaga innego podejścia do wykrycia i wykorzystania.

![697](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1776682954081.svg)

Enumeracja nazw użytkowników służy do generowania listy kont zarejestrowanych w aplikacji docelowej. Odbywa się to poprzez podanie nazw użytkowników w formularzu, który reaguje inaczej na wartości zarejestrowane i niezarejestrowane, na przykład na stronie rejestracji lub resetowania hasła. Wynikiem jest krótka lista rzeczywistych kont, która bezpośrednio napędza późniejsze ataki na dane uwierzytelniające.

Atak brute force na uwierzytelnianie wykorzystuje tę listę wraz ze słownikiem popularnych haseł, aby znaleźć konta, których hasła można odgadnąć. W najprostszym przypadku atakujący łączy każdą nazwę użytkownika z każdym hasłem ze słownika i wprowadza każdą kombinację w formularzu logowania. Gdy aplikacja nie stosuje limitów przepustowości ani blokad, atak jest niedrogi w przeprowadzeniu i często generuje działającą parę uwierzytelniającą w ciągu kilku sekund.

Błędy logiczne występują, gdy zamierzony przepływ pracy związany z uwierzytelnianiem może zostać przekierowany przez dane wejściowe wyglądające na prawidłowe. Przepływy pracy resetowania hasła i odzyskiwania konta są częstym źródłem takich błędów, ponieważ często dzielą dane wejściowe na wiele etapów.HTTPParametry, pliki cookie i zmienne sesji. Błąd w łączeniu tych danych może spowodować, że link resetujący dla jednego konta zostanie wysłany na inny adres niż ten zapisany w pliku.

Manipulacja plikami cookie ma na celu zmianę stanu sesji, który serwer zwraca klientowi po pomyślnym zalogowaniu. Pliki cookie, które nie są podpisane kryptograficznie, mogą być edytowane przez klienta w celu zmiany decyzji uwierzytelniającej podejmowanej przez serwer przy kolejnych żądaniach. Popularne formaty to pliki cookie w postaci zwykłego tekstu, pliki cookie zawierające skrót wartości bazowej oraz pliki cookie zawierające odwracalnie zakodowany ładunek, taki jak base64.

## Przykłady zastosowań i wpływ

Wynik udanego ominięcia uwierzytelniania zależy od konta, do którego atakujący jest w stanie uzyskać dostęp, oraz od uprawnień przyznanych temu kontu.

Po pierwsze, atakujący może użyć obejścia, aby uzyskać dostęp do danych i funkcji należących do konkretnego użytkownika. W przypadku zwykłego konta klienta zazwyczaj obejmuje to dane osobowe, historię transakcji i wszelkie rekordy powiązane z użytkownikiem. W przypadku konta administratora ta sama technika zapewnia kontrolę nad samą aplikacją, w tym możliwość modyfikowania danych innych użytkowników, odczytywania zawartości bazy danych lub zmiany konfiguracji aplikacji.

Obejście jest również często stosowane jako pierwszy krok w dłuższym ataku. Na przykład, ważna sesja agenta wsparcia może posłużyć do odczytania zgłoszeń pomocy technicznej należących do każdego klienta aplikacji. Dostęp do konta administracyjnego może w niektórych przypadkach prowadzić do wykonania dowolnego kodu na serwerze bazowym za pośrednictwem funkcji dostępnych dla tego poziomu uprawnień, takich jak przesyłanie plików czy analiza skryptów.

Dane uwierzytelniające odzyskane w wyniku obejścia są często ponownie wykorzystywane w niepowiązanych aplikacjach. Użytkownicy często dzielą się hasłami w różnych usługach, więc hasło ujawnione w jednej witrynie może zapewnić dostęp do kont w innych. Ten schemat znany jest jako „wypychanie danych uwierzytelniających” (ang. credential stuffing) i odpowiada za znaczną część zgłaszanych obecnie przypadków naruszenia bezpieczeństwa kont w aplikacjach konsumenckich.

Enumeracja nazw użytkowników to technika rozpoznania służąca do określenia, które nazwy użytkowników istnieją w docelowej aplikacji internetowej. Wynikiem jest lista rzeczywistych kont, które mogą zostać wykorzystane w atakach uwierzytelniających, takich jak brute force, password spraying i ukierunkowane ataki. phishing Zanim będzie można przeprowadzić jakikolwiek skuteczny atak na konta użytkowników, atakujący musi wiedzieć, jakie konta istnieją, a aplikacja ujawniająca te informacje eliminuje pierwszy krok, który w przeciwnym razie atakujący musiałby wykonać.

W typowej aplikacji internetowej istnieje wiele miejsc, w których te informacje mogą wyciekać. Formularz rejestracyjny, który odmawia zarejestrowania duplikatu nazwy użytkownika, formularz logowania, który rozróżnia nieznane konto od błędnego hasła, oraz formularz resetowania hasła, który informuje, czy adres e-mail jest zapisany, to wszystko kandydaci do enumeracji. W każdym przypadku aplikacja obsługuje zarejestrowane i niezarejestrowane wartości inaczej, ujawniając w ten sposób, które wartości są które.

## Różnice komunikatów o błędach

Najczęstszym wektorem enumeracji jest formularz rejestracyjny, który odrzuca duplikaty nazw użytkowników. Gdy użytkownik próbuje zarejestrować się pod nazwą, która jest już używana, aplikacja zwraca błąd, taki jak „Konto o tej nazwie użytkownika już istnieje”. Ten sam formularz akceptuje nazwę, która nigdy nie została zarejestrowana i odpowiada komunikatem o pomyślnym zarejestrowaniu. Różnica między tymi dwiema odpowiedziami jest łatwa do odróżnienia programowo i stanowi podstawę automatycznego enumeracji.

Komunikaty o błędach to nie jedyny sygnał. Dwie odpowiedzi mogą zawierać ten sam widoczny tekst, różniąc się jednak długością, kodem statusu, czasem reakcji lub sposobem przekierowania. Dobrze zaprojektowane narzędzie może dopasować się do dowolnej z tych właściwości, co oznacza, że ​​aplikacja zwracająca identyczne komunikaty o błędach może nadal być wyliczalna, nawet jeśli jej odpowiedzi różnią się pod jakimś innym względem.

Strona rejestracji Acme IT Support `http://MACHINE_IP/customers/signup`jest podatna na ten wzorzec. `POST`Żądanie zawierające `username=admin`dowolne wartości w pozostałych polach zwraca komunikat „Konto o tej nazwie użytkownika już istnieje”. Żądanie z nazwą użytkownika, która nigdy nie została zarejestrowana, zwraca inną odpowiedź, a treść tej odpowiedzi stanowi sygnał, na podstawie którego narzędzie automatyczne może filtrować.

![Jak FFuF ustala prawidłową nazwę użytkownika|697](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1776682977409.svg)

## Wyliczanie za pomocą ffuf

`ffuf`to szybki fuzzer internetowy napisany w języku Go. Podmienia każdy wpis z listy słów na znacznik w żądaniu HTTP i raportuje odpowiedzi spełniające zadany warunek. Narzędzie jest preinstalowane w AttackBox i można je również pobrać ze strony [https://github.com/ffuf/ffuf.(otwiera się w nowej karcie)](https://github.com/ffuf/ffuf).

Poniższe polecenie wylicza prawidłowe nazwy użytkowników na stronie rejestracji Acme:

```bash
ffuf -w /usr/share/wordlists/SecLists/Usernames/Names/names.txt -X POST -d "username=FUZZ&email=x&password=x&cpassword=x" -H "Content-Type: application/x-www-form-urlencoded" -u http://MACHINE_IP/customers/signup -mr "username already exists"
```

Argument `-w`wybiera listę słów kandydatów na nazwy użytkowników. `-X POST`Argument ustawia metodę HTTP, zgodnie z wymaganiami formularza rejestracyjnego. `-d`Argument definiuje treść żądania, a token `FUZZ`działa jako symbol zastępczy, który `ffuf`jest zastępowany każdym słowem z listy słów. `-H`Argument ustawia `Content-Type`nagłówek, dzięki czemu serwer traktuje treść jako dane formularza zakodowane w adresie URL. `-u`Argument ustawia docelowy adres URL. Na koniec `-mr`argument (dopasuj wyrażenie regularne) ogranicza dane wyjściowe do odpowiedzi, których treść zawiera ciąg znaków `username already exists`.

Uruchomienie polecenia generuje krótką listę pasujących nazw, z których każda odpowiada nazwie użytkownika zarejestrowanej w aplikacji. Zapisz pasujące nazwy użytkowników w pliku o nazwie `valid_usernames.txt`, po jednej w wierszu, do wykorzystania w następnym zadaniu. Plik zostanie przekazany bezpośrednio `ffuf`jako lista słów, więc jego zawartość musi zawierać wyłącznie nazwy użytkowników bez kodów statusu, kolumn czasu ani dodatkowych spacji.

Błąd logiczny to luka w zabezpieczeniach, w której zamierzony przepływ danych w aplikacji może zostać przekierowany poprzez podanie danych wejściowych, których programista nie przewidział. W przeciwieństwie do błędów związanych z wstrzykiwaniem kodu lub uszkodzeniem pamięci, błędy logiczne nie polegają na błędnie sformatowanych danych, lecz na całkowicie poprawnych danych wejściowych, które kierują aplikacją przez niezamierzoną sekwencję decyzji. Atakujący osiąga stan uprzywilejowany nie poprzez złamanie pojedynczej reguły, ale poprzez wykorzystanie niespójności między dwiema regułami, które zostały zaprojektowane do działania w izolacji.

![697](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1776683025612.svg)

Automatyczne skanery rzadko wykrywają błędy logiczne, ponieważ zależą one od reguł biznesowych konkretnej aplikacji. Skaner może zidentyfikować istnienie przepływu pracy resetowania hasła, ale nie jest w stanie ocenić, czy przepływ ten poprawnie wiąże adres e-mail z pliku z docelową nazwą użytkownika. Aby skutecznie wykryć te błędy, należy zapoznać się z kodem źródłowym, dokumentacją architektoniczną aplikacji lub ręcznie przetestować każdy przepływ pracy.

## Porównanie ścieżek uwzględniające wielkość liter

Najprostsza klasa błędów logicznych pojawia się, gdy dwa komponenty tej samej aplikacji nie zgadzają się co do sposobu interpretacji danych wejściowych. Struktura routingu, która nie uwzględnia wielkości liter, traktuje `/admin`i `/adMin`jako ten sam adres URL. Kontrola autoryzacji w dół, która wykorzystuje ścisłe porównanie ciągów znaków, traktuje je jako różne wartości. Żądanie `/adMin`dociera do modułu obsługi administracyjnej, ponieważ router nie zwraca uwagi na wielkość liter, i pomija kontrolę autoryzacji, ponieważ ta ją uwzględnia.

Rozważmy poniższy fragment kodu po stronie serwera, który decyduje, czy przed renderowaniem strony zastosować sprawdzenie uprawnień administratora:

```php
if( url.substr(0,6) === '/admin') {
    # Code to check user is an admin
} else {
    # View Page
}
```

Operator `===`przeprowadza ścisłą kontrolę równości, więc `/admin`przechodzi do gałęzi uprzywilejowanej, ale `/adMin`tego nie robi. Jeśli warstwa routingu poniżej nie rozróżnia wielkości liter i mapuje `/adMin`na ten sam moduł obsługi co `/admin`, żądanie dociera do strony administracyjnej bez przeprowadzania kontroli uprawnień.

Luka nie występuje w żadnym z komponentów osobno. Ścisłe porównanie ciągów znaków jest rozsądną decyzją w oderwaniu od kontekstu, podobnie jak routing bez uwzględniania wielkości liter. Wada wynika z rozbieżności między tymi dwoma elementami.

## Zanieczyszczenie parametrów podczas resetowania hasła

Strona resetowania hasła `http://10.130.162.225/customers/reset`realizuje dwuetapowy przepływ pracy. Krok pierwszy akceptuje adres e-mail i, jeśli adres pasuje do znanego konta, przechodzi do kroku drugiego. Krok drugi akceptuje nazwę użytkownika powiązaną z tym adresem e-mail i, w przypadku powodzenia, wysyła link do resetowania hasła na zarejestrowany adres e-mail.

Po wysłaniu `robert@acmeitsupport.thm`nazwy użytkownika `robert`zostanie wyświetlone potwierdzenie pokazane poniżej.

![Ekran potwierdzenia zresetowania hasła Acme IT Support pokazujący, że wiadomość e-mail z resetem zostanie wysłana na adres robert@acmeitsupport.thm](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/f457baf00c357990014739bd6bce5b75.png)

Na pierwszy rzut oka ten obieg pracy wydaje się dobrze zabezpieczony. Wymagany jest zarówno adres e-mail, jak i nazwa użytkownika, a link resetowania jest wysyłany na adres e-mail zapisany dla danego konta. Jednak implementacja rozdziela te dwie wartości na różne części żądania HTTP. Adres e-mail jest przenoszony w ciągu zapytania URL, a nazwa użytkownika w treści żądania POST.

Poniższe `curl`polecenie odtwarza prawidłowe żądanie z kroku drugiego. `curl`to klient HTTP z wiersza poleceń, preinstalowany w AttackBoxie. Uruchom polecenie z AttackBoxa, aby ścieżka sieciowa do celu była już ustalona:

```bash
curl 'http://10.130.162.225/customers/reset?email=robert%40acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert'
```

Argument `-H`ustawia `Content-Type`nagłówek, tak aby serwer traktował treść jako dane formularza zakodowane w adresie URL, i `-d`dostarcza tę treść. Sekwencja `%40`to zakodowana w adresie URL forma znaku `@`.

Po stronie serwera aplikacja identyfikuje konto docelowe na podstawie parametru ciągu zapytania `email`, ale tworzy wychodzącą wiadomość resetującą, korzystając z `$_REQUEST`superglobalnej tablicy PHP. `$_REQUEST`Łączy dane z ciągu zapytania, treści zapytania POST i plików cookie w jedną tablicę, a gdy ten sam klucz pojawia się w więcej niż jednym źródle, treść zapytania POST ma domyślnie pierwszeństwo.

W rezultacie drugi `email`parametr umieszczony w treści żądania po cichu nadpisuje wartość załadowaną przez aplikację z ciągu zapytania. Link resetujący jest następnie wysyłany na adres wybrany przez atakującego:

```bash
curl 'http://10.130.162.225/customers/reset?email=robert%40acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert&email=attacker@hacker.com'
```

![Ekran potwierdzenia zresetowania hasła pomocy technicznej Acme IT, na którym widać przekierowanie wiadomości e-mail z prośbą o zresetowanie hasła na adres attacker@hacker.com](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/3d97e3e37bf9e4db4f95f4f945a7e290.png)

Dlaczego aplikacja zachowuje się w ten sposób? Deweloper potraktował ciąg zapytania i treść żądania POST jako wymienne źródła tego samego parametru, nie uwzględniając reguł scalania w pliku `$_REQUEST`. Weryfikacja tożsamości odczytuje dane z jednego źródła, a efekt uboczny wiadomości e-mail wychodzących odczytuje dane z innego. Wszelkie dane wejściowe wpływające na którekolwiek ze źródeł mogą spowodować desynchronizację obu źródeł i przekierować łącze resetowania na inny adres.

## Powielanie exploita przeciwko kontu Roberta

Do przeprowadzenia ataku potrzebna jest skrzynka odbiorcza, która może odebrać e-mail z resetem. Portal klienta Acme przekazuje każdemu zarejestrowanemu klientowi wewnętrzny adres formularza `{username}@customer.acmeitsupport.thm`. Wiadomość wysłana na ten adres pojawia się jako zgłoszenie pomocy technicznej na odpowiednim koncie klienta. Zarejestruj konto klienta w portalu, zanotuj adres przypisany do tego konta i uruchom atak, wpisując swój adres w miejsce wartości atakującego:

```bash
curl 'http://10.130.162.225/customers/reset?email=robert@acmeitsupport.thm' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=robert&email={your_username}@customer.acmeitsupport.thm'
```

Link do resetowania pojawia się jako nowy bilet pomocy technicznej na Twoim koncie klienta. Skorzystanie z linku uwierzytelnia przeglądarkę jako Roberta, a jego istniejące bilety pomocy technicznej zawierają flagę dla tego zadania.

HTTPjest protokołem bezstanowym, co oznacza, że ​​każde żądanie jest przetwarzane niezależnie od pozostałych. Aplikacje internetowe potrzebują sposobu na zapamiętanie, że dany użytkownik został uwierzytelniony, aby kolejne żądania od tego użytkownika nie wymagały ponownego przesyłania danych uwierzytelniających. Zazwyczaj odbywa się to za pomocą plików cookie, czyli małych fragmentów danych ustawianych przez serwer i zwracanych przez klienta przy każdym kolejnym żądaniu do tego samego źródła.

Gdy plik cookie zawiera stan sesji uwierzytelnionej, jego zawartość decyduje o decyzji uwierzytelniającej, którą serwer podejmuje przy kolejnym żądaniu. Jeśli plik cookie nie jest podpisany kryptograficznie, klient może modyfikować jego zawartość i zmieniać decyzję. Plik cookie zaakceptowany bez weryfikacji przyznaje sesję użytkownikowi, którego opisuje. Przypomnienie informacji na temat plików cookie i sposobu ich przesyłania jest dostępne w dokumencie [tutaj brakuje kontekstu].[HTTPw pokoju szczegółów](https://tryhackme.com/room/httpindetail) .

Trzy formaty plików cookie najczęściej spotykane w podatnych na ataki aplikacjach to zwykły tekst, hasz i kodowanie. Każdy z nich omówiono w osobnej sekcji poniżej.

## Pliki cookie w postaci zwykłego tekstu

Plik cookie w postaci zwykłego tekstu przechowuje stan bazowy bezpośrednio w nagłówku, w formie widocznej i łatwej do edycji dla każdego posiadacza pliku cookie. Rozważmy serwer, który po pomyślnym zalogowaniu generuje następującą parę:

```bash
Set-Cookie: logged_in=true; Max-Age=3600; Path=/
Set-Cookie: admin=false; Max-Age=3600; Path=/
```

Aplikacja odczytuje dwa pliki cookie przy każdym kolejnym żądaniu i na ich podstawie decyduje, czy zwrócić odpowiedź uwierzytelnioną, administracyjną czy nieuwierzytelnioną. Ponieważ do żadnej z wartości nie jest dołączony podpis ani kontrola integralności, klient może swobodnie modyfikować plik cookie, a serwer nie ma możliwości wykrycia tej zmiany.

Punkt końcowy `http://10.130.162.225/cookie-test`w pełni demonstruje ten wzorzec. Żądanie bez plików cookie zwraca komunikat „ **Niezalogowany”** :

```bash
curl http://10.130.162.225/cookie-test
```

Ustawienie `logged_in=true`i pozostawienie `admin=false`zmiany powoduje zmianę odpowiedzi na **Zalogowany jako użytkownik** :

```bash
curl -H "Cookie: logged_in=true; admin=false" http://10.130.162.225/cookie-test
```

Ustawienie obu plików cookie na `true`zwraca **stan Zalogowany jako administrator** i uwzględnia flagę dla tej części zadania:

```bash
curl -H "Cookie: logged_in=true; admin=true" http://10.130.162.225/cookie-test
```

## Haszowane ciasteczka

Hasz to wynik funkcji jednokierunkowej o stałej długości zastosowanej do danych wejściowych. Te same dane wejściowe zawsze generują te same dane wyjściowe, a funkcji nie można odwrócić, aby odzyskać dane wejściowe z danych wyjściowych. Ta ostatnia właściwość skłania niektórych programistów do przechowywania wartości haszowanych w plikach cookie, zakładając, że hasz zabezpiecza dane bazowe przed manipulacją.

To założenie jest błędne. Skrót nie jest podpisem; jest reprezentacją adresowalną treściowo. Każda strona, która zna lub odgadnie oryginalną wartość, może niezależnie wygenerować ten sam skrót i podstawić go do pliku cookie. Poniższa tabela przedstawia skrót pojedynczego znaku `1`dla czterech powszechnie stosowanych algorytmów.

|Oryginalny sznurek|Metoda haszująca|Wyjście|
|---|---|---|
|1|MD5|`c4ca4238a0b923820dcc509a6f75849b`|
|1|SHA-1|`356a192b7913b04c54574d18c28d46e6395428ab`|
|1|SHA-256|`6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b`|
|1|SHA-512|`4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a`|

Nieodwracalność skrótu chroni jedynie przed siłowym odzyskaniem oryginalnej wartości. W przypadku krótkich lub przewidywalnych danych wejściowych, wstępnie obliczone tabele obejmujące wszystkie wspólne wartości przekształcają skrót w reprezentację skutecznie odwracalną. Usługi publiczne, takie jak [https://crackstation.net(otwiera się w nowej karcie)](https://crackstation.net/)przechowują bazy danych zawierające miliardy wstępnie obliczonych skrótów i ich ciągi źródłowe, a znaczną część wartości plików cookie chronionych wyłącznie przez skrót można odzyskać za pomocą prostego wyszukiwania.

## Zakodowane pliki cookie

Kodowanie to odwracalna transformacja stosowana do danych binarnych lub ustrukturyzowanych, umożliwiająca ich przesyłanie kanałem akceptującym jedynie ograniczony zestaw znaków. Kodowanie nie zapewnia poufności ani integralności; jego jedynym zadaniem jest konwersja danych do postaci, którą może przesyłać dany protokół. Dwa powszechnie spotykane kodowania w plikach cookie to base32, które wykorzystuje znaki `A-Z`i `2-7`, oraz base64, które wykorzystuje znaki `a-z`, `A-Z`, `0-9`, `+`, `/`, i `=`do dopełnienia.

Programiści często używają base64 w plikach cookie, aby dopasować dane strukturalne, takie jak obiekt JSON, do wartości zgodnej ze składnią plików cookie w specyfikacji HTTP. Rozważmy serwer, który przechowuje dane sesji jako obiekt JSON zakodowany w base64 i wysyła następujący nagłówek podczas logowania:

```bash
Set-Cookie: session=eyJpZCI6MSwiYWRtaW4iOmZhbHNlfQ==; Max-Age=3600; Path=/
```

Dekodowanie wartości za pomocą base64 generuje `{"id":1,"admin":false}`, co pozwala na natychmiastowy podgląd schematu sesji. Plik JSON można edytować, ustawiając `"admin":true`, zakodować z powrotem do base64 i zastąpić nim oryginalny plik cookie. Ponieważ serwer nie weryfikuje ani nie podpisuje danych, zmodyfikowany plik cookie jest akceptowany przy kolejnym żądaniu, a odpowiedź odzwierciedla uprawnienia administratora.

Luki w zabezpieczeniach umożliwiające ominięcie uwierzytelnienia są zazwyczaj spowodowane źle zakodowanymi aplikacjami internetowymi lub źle skonfigurowanym zarządzaniem sesjami. Istnieją jednak bezpieczne metody kodowania i wzorce projektowe, które zmniejszają ryzyko podatności na każdą z klas ataków omówionych w tym artykule.

## Łagodzenie wyliczania nazw użytkowników

Wyliczanie nazw użytkowników jest minimalizowane poprzez zwracanie identycznych odpowiedzi dla wartości zarejestrowanych i niezarejestrowanych na każdym punkcie końcowym związanym z uwierzytelnianiem, w tym rejestracji, logowania i resetowania hasła. Treść odpowiedzi, kody statusu i czas muszą być zgodne w obu przypadkach. Na przykład, dobrze zaprojektowany proces rejestracji akceptuje każde zgłoszenie i wysyła wiadomość e-mail z potwierdzeniem na podany adres. Jeśli adres jest już zarejestrowany, wiadomość e-mail wyjaśnia, że ​​podjęto próbę duplikacji rejestracji, ale odpowiedź zwrócona do przeglądarki jest identyczna w obu przypadkach.

Ograniczanie przepustowości i testy CAPTCHA zapewniają dodatkową warstwę ochrony, zwiększając koszt uruchomienia automatycznej enumeracji na ujawnionych formularzach. Te mechanizmy kontroli nie eliminują wycieku, ale spowalniają eksploatację na tyle, że prawdopodobieństwo wykrycia aktywności przed zakończeniem enumeracji jest większe.

## Łagodzenie brutalnej siły

Ataki brute force są spowalniane przez limity szybkości uwierzytelniania w punktach końcowych i blokowane przez blokadę konta po osiągnięciu progowej liczby nieudanych prób. Obie kontrole muszą być starannie dostrojone, aby uniknąć wygenerowania wektora odmowy usługi (DOS) dla uprawnionych użytkowników. Uwierzytelnianie wieloskładnikowe to najskuteczniejsza pojedyncza obrona, ponieważ gwarantuje, że samo hasło nie wystarczy, nawet jeśli zostanie poprawnie odgadnięte.

Zasady dotyczące haseł, które wymagają długości, złożoności i rotacji, w subtelny sposób oddziałują na metody siłowe. Długie hasło jest bardzo skuteczne w walce z siłami siłowymi, natomiast krótkie i złożone hasło nie. Zasady zachęcające użytkowników do wybierania krótkich, złożonych haseł z częstą rotacją często przynoszą gorsze rezultaty niż zasady wymagające długich, łatwych do zapamiętania haseł z mniejszą częstotliwością rotacji.

## Łagodzenie błędów logicznych

Luki logiczne są najtrudniejszą do uniknięcia klasą błędów, ponieważ zależą od decyzji specyficznych dla danej aplikacji. Ogólna zasada jest taka, że ​​każda decyzja istotna dla bezpieczeństwa powinna odczytywać dane wejściowe z jednego, zaufanego źródła. Przepływ pracy resetowania hasła, który wczytuje konto docelowe z ciągu zapytania, powinien tworzyć wychodzącą wiadomość e-mail przy użyciu adresu powiązanego z tym kontem w bazie danych, a nie wartości odczytanej ponownie z żądania.

W ścieżkach kodu istotnych ze względów bezpieczeństwa należy unikać frameworków i funkcji językowych, które w sposób dyskretny łączą dane wejściowe z wielu źródeł.PHP, jawny dostęp do `$_GET`, `$_POST`, i `$_COOKIE`powinien być preferowany nad `$_REQUEST`. W innych językach i frameworkach równoważną zasadą jest odczytywanie każdego parametru żądania z dokładnie jednej, dobrze zdefiniowanej lokalizacji.

## Ograniczanie manipulacji plikami cookie

Manipulacji plikami cookie można zapobiec, stosując jedno z dwóch podejść. Pierwsze polega na podpisywaniu tokenów sesji silnym kluczem tajnym po stronie serwera, zazwyczaj przy użyciu konstrukcji takiej jak HMAC lub podpisany JSONToken internetowy (JWT). Podpis gwarantuje, że każda modyfikacja wartości pliku cookie unieważnia token, a serwer może odrzucić sfałszowane pliki cookie bez konieczności sprawdzania stanu zewnętrznego. Drugie podejście polega na wydaniu jedynie nieprzejrzystego identyfikatora sesji i przechowywaniu rzeczywistego stanu sesji w magazynie po stronie serwera, takim jak Redis lub baza danych. Ponieważ plik cookie nie zawiera żadnego istotnego ładunku, atakujący nie ma czego modyfikować.

Haszowanie wartości pliku cookie nie zastępuje żadnego z tych podejść. Hasz dowodzi jedynie, że klient widział jakąś wartość; nie dowodzi jednak, że wartość została wydana przez serwer ani że nie została od tego czasu zmodyfikowana.

## Dalsza lektura

Ten[OWASPW 10 najpopularniejszych](https://tryhackme.com/room/owasptop10) pokojach szczegółowo opisano awarie kontroli dostępu i błędy identyfikacji.[HTTPW](https://tryhackme.com/room/httpindetail) pokoju „Szczegóły” opisano mechanizmy żądań i odpowiedzi, od których zależy każdy atak opisany w tym pokoju.
