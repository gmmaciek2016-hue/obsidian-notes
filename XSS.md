

Ataki typu cross-site scripting (XSS) pozostaje jedną z powszechnych luk w zabezpieczeniach, które do dziś zagrażają aplikacjom internetowym. Ataki XSS polegają na wstrzyknięciu złośliwego skryptu do nieszkodliwej witryny internetowej, aby uruchomić go w przeglądarce użytkownika. Innymi słowy, ataki XSS wykorzystują zaufanie użytkownika do podatnej aplikacji internetowej, stąd szkody.

Jedną z pierwszych luk XSS rozpoznano w 1999 r. i doprowadziła ona do CERT doradczy[Kalifornia-2000-02](https://vuls.cert.org/confluence/display/historical/CERT+Advisory+CA-2000-02+Malicious+HTML+Tags+Embedded+in+Client+Web+Requests) . W ciągu ostatnich dekad różnorodne, solidne praktyki bezpieczeństwa sieci stały się częścią nowoczesnych frameworków aplikacji internetowych, domyślnie chroniąc przed wieloma lukami XSS. Z drugiej strony, wzrosły również motywy i wyrafinowanie ataków.

Wraz z rozwojem aplikacji internetowych nie jest przesadą stwierdzenie, że co miesiąc odkrywane i wykorzystywane są pewne luki w zabezpieczeniach XSS.[OWASPW pierwszej dziesiątce](https://owasp.org/www-project-top-ten/) XSS znalazł się na siódmym miejscu w 2017 r. W raporcie z 2021 r. XSS został zgrupowany z innymi atakami typu injection i razem zajmuje trzecie miejsce.

W tym pokoju szczegółowo omówiono kwestię XSS, aby pomóc w odkrywaniu, wykorzystywaniu i łataniu luk w zabezpieczeniach XSS.

## Wymagania dotyczące pokoju

Oczekuje się, że kandydat będzie posiadał podstawową wiedzę na temat HTTP i jak działają strony internetowe. Jeśli nie posiadasz tej wiedzy, zalecamy najpierw ukończenie modułu „ [Jak działa sieć”](https://tryhackme.com/module/how-the-web-works) .

Jeśli nie znasz XSS, gorąco polecamy zapoznanie się z salą [„Wprowadzenie do ataków międzywitrynowych](https://tryhackme.com/room/xss) ”, ponieważ ta sala jest jej rozwinięciem.

Wreszcie, ten pokój wykorzystuje fragmenty kodu wPHP, JavaScript, Python i C-Sharp. Znajomość wszystkich tych języków programowania nie jest wymagana. Zamiast tego wyjaśniamy niezbędne fragmenty kodu i skupiamy się na przyczynach i sposobach rozwiązania luk XSS.

Poniżej znajduje się lista pokoi, z których możesz skorzystać, aby uzupełnić wszelkie luki w wiedzy przed rozpoczęciem nauki w tym pokoju:

- [HTTP w szczegółach](https://tryhackme.com/room/httpindetail)
- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)
- [Podstawy JavaScript](https://tryhackme.com/room/javascriptessentials)
- [Wprowadzenie do ataków typu cross-site scripting](https://tryhackme.com/room/xss)
- Opcjonalnie: [Podstawy Pythona](https://tryhackme.com/room/pythonbasics?path=undefined)

## Cele edukacyjne

Po ukończeniu tego pokoju użytkownik powinien lepiej zrozumieć XSS, w szczególności:

- Odbity XSS
- Zapisany XSS
- XSS oparty na DOM
- Jak chronić się przed XSS

Dostarczamy fragmenty kodu wykorzystujące różne frameworki internetowe, aby lepiej zrozumieć wykorzystanie luk XSS i zabezpieczenia przed nimi. Nie skupiamy się na samym kodzie, lecz na przyczynach powstania luki i niektórych rozwiązaniach. Celem jest lepsze zrozumienie przyczyn powstania XSS i tego, co czyni go podatnym na wykorzystanie.

Jak już powiedziano, XSS to luka w zabezpieczeniach, która pozwala atakującemu na wstrzyknięcie złośliwych skryptów na stronę internetową przeglądaną przez innego użytkownika. W rezultacie omijają oni zasadę **Same-Origin Policy (MACZANKA)** ; SOP to mechanizm bezpieczeństwa zaimplementowany w nowoczesnych przeglądarkach internetowych, który zapobiega uzyskaniu przez złośliwy skrypt na jednej stronie internetowej dostępu do poufnych danych na innej stronie. SOP definiuje pochodzenie na podstawie protokołu, nazwy hosta i portu. W konsekwencji złośliwy skrypt ogłoszenie Nie można uzyskać dostępu do danych ani manipulować stroną lub jej funkcjonalnością z innego źródła, takiego jak sklep internetowy lub strona banku. XSS omija SOP, ponieważ jest wykonywany z tego samego źródła.

## JavaScript dla XSS

Podstawowa znajomość języka JavaScript jest kluczowa dla zrozumienia exploitów XSS i dostosowania ich do własnych potrzeb. Wiedząc, że XSS to atak po stronie klienta, który odbywa się w przeglądarce internetowej ofiary, powinniśmy wypróbować nasze ataki na przeglądarce podobnej do przeglądarki ofiary. Warto zauważyć, że różne przeglądarki przetwarzają pewne fragmenty kodu w różny sposób. Innymi słowy, jeden kod exploita może działać w przeglądarce Google Chrome, ale nie w przeglądarkach Mozilla Firefox czy Safari.

Załóżmy, że chcesz poeksperymentować z kodem JavaScript w przeglądarce. W takim przypadku musisz otworzyć **Konsolę** , która znajduje się w Narzędziach dla programistów stron internetowych w Firefoksie, Narzędziach dla programistów w Google Chrome oraz Inspektorze stron internetowych w Safari. Alternatywnie, skorzystaj z odpowiednich skrótów:

- W przeglądarce Firefox naciśnij Ctrl + Shift + K
- W przeglądarce Google Chrome naciśnij Ctrl + Shift + J
- W Safari naciśnij Command + Option + J

![Przeglądarka internetowa z otwartą kartą Konsola.](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/ea22f6ec937fa5d9c24dc024372e357b.png)  

Przyjrzyjmy się i wypróbujmy kilka podstawowych funkcji JavaScript:

- **Alert** : Możesz użyć tej `alert()`funkcji, aby wyświetlić alert JavaScript w przeglądarce internetowej. Spróbuj użyć klawiszy `alert(1)`lub `alert('XSS')`(lub `alert("XSS")`), aby wyświetlić pole alertu z cyfrą 1 lub tekstem XSS.
- **Dziennik konsoli** : Podobnie, możesz wyświetlić wartość w konsoli JavaScript przeglądarki za pomocą `console.log()`. Wypróbuj poniższe dwa przykłady w dzienniku konsoli: `console.log(1)`i , `console.log("test text")` aby wyświetlić liczbę lub ciąg tekstowy.
- **Kodowanie** : Funkcja JavaScript `btoa("string")`koduje ciąg danych binarnych, tworząc ciąg ASCII zakodowany w formacie Base64. Jest to przydatne do usuwania białych znaków i znaków specjalnych lub kodowania innych alfabetów. Funkcja odwrotna to `atob("base64_string")`:

Ponadto można poeksperymentować z wyświetlaniem wartości, korzystając `document.cookie`na `alert(document.cookie)`przykład z .

![Przeglądarka internetowa wyświetlająca komunikat „Witaj, świecie!”](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0ba756c3c7a74a2cc0fecdca6311b117.png)  

![Przeglądarka internetowa z kartą Konsola wyświetlającą przykładowe funkcje JavaScript.](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/35bc1c17a4e32135c8a75593c0fbba7f.png)  

## Typy XSS

Podsumowując informacje z sali [Wprowadzenie do ataków typu Cross-site Scripting](https://tryhackme.com/room/xss) , wyróżniamy trzy główne typy ataków XSS:

- **Odbity XSS** : Ten atak opiera się na kontrolowanych przez użytkownika danych wejściowych, które są mu przekazywane. Na przykład, jeśli wyszukasz określone hasło, a strona wyników wyświetli szukane hasło ( **_odbite_** ), atakujący spróbuje osadzić złośliwy skrypt w wyszukiwanym haśle.
- **Stored XSS** : Ten atak opiera się na danych wprowadzonych przez użytkownika, przechowywanych w bazie danych witryny. Na przykład, jeśli użytkownicy mogą pisać recenzje produktów, które są zapisywane w bazie danych ( **_store_** ) i wyświetlane innym użytkownikom, atakujący próbowałby umieścić złośliwy skrypt w swojej recenzji, aby została ona uruchomiona w przeglądarkach innych użytkowników.
- **XSS oparty na DOM : Ten atak wykorzystuje luki w zabezpieczeniach modelu** **DOM** (Document Object Model ) do manipulowania istniejącymi elementami strony bez konieczności ich odzwierciedlenia lub przechowywania na serwerze. Ta luka jest najrzadsza spośród tych trzech.


Ataki typu cross-site scripting (XSS) to luka w zabezpieczeniach sieci, która umożliwia atakującemu wstrzyknięcie złośliwych skryptów do strony internetowej przeglądanej przez innych użytkowników. W rezultacie niczego niepodejrzewający użytkownicy uruchamiają nieautoryzowany skrypt w swoich przeglądarkach, mimo że odwiedzana przez nich strona internetowa jest uznawana za nieszkodliwą. Dlatego atak XSS może stanowić poważne zagrożenie, ponieważ wykorzystuje zaufanie użytkowników do danej witryny.

## Co umożliwia XSS

Istnieje wiele powodów, dla których luki XSS wciąż występują w aplikacjach internetowych. Poniżej wymieniamy kilka z nich.

**Niewystarczająca walidacja i dezynfekcja danych wejściowych**

Aplikacje internetowe akceptują dane użytkownika, np. za pośrednictwem formularzy, i wykorzystują je do dynamicznego generowania stron HTML. W rezultacie złośliwe skrypty mogą zostać osadzone jako część legalnych danych wejściowych i ostatecznie zostaną wykonane przez przeglądarkę, jeśli nie zostaną odpowiednio oczyszczone.

**Brak kodowania wyjściowego**

Użytkownik może użyć różnych znaków, aby zmienić sposób, w jaki przeglądarka internetowa przetwarza i wyświetla stronę internetową. W przypadku kodu HTML kluczowe jest prawidłowe zakodowanie znaków takich jak `<`, `>`, `"`, `'`i `&`w odpowiednim kodowaniu HTML. W przypadku JavaScript należy zwrócić szczególną uwagę na znaki escape `'`, `"`i `\`. Nieprawidłowe zakodowanie danych dostarczonych przez użytkownika jest główną przyczyną luk w zabezpieczeniach XSS.

**Niewłaściwe użycie nagłówków bezpieczeństwa**

Różne nagłówki zabezpieczeń mogą pomóc w ograniczeniu luk XSS. Na przykład polityka bezpieczeństwa treści (CSP) ogranicza ryzyko XSS, definiując źródła zaufane dla skryptów wykonywalnych. Nieprawidłowo skonfigurowana polityka CSP, na przykład zbyt liberalne zasady lub niewłaściwe użycie dyrektyw `unsafe-inline`lub `unsafe-eval`, może ułatwić atakującemu wykonywanie ataków XSS.

**Luki w zabezpieczeniach frameworka i języka**

Niektóre starsze frameworki webowe nie zapewniały mechanizmów bezpieczeństwa przed atakami XSS; inne miały niezałatane luki w zabezpieczeniach XSS. Nowoczesne frameworki webowe automatycznie unikają ataków XSS i natychmiast łatają każdą wykrytą lukę.

**Biblioteki stron trzecich**

Integrowanie bibliotek innych firm w aplikacji internetowej może być przyczyną podatności na ataki typu XSS, nawet jeśli podstawowa aplikacja internetowa nie jest podatna.

![Złośliwy haker pisze komentarz na stronie internetowej, który zaczyna się od powitania i stwierdza, że ​​to jego pierwszy wpis. Ponadto dołącza adres URL, który wygląda, jakby kradł plik cookie użytkownika.](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/984673339466701119cb694803ff0d27.svg)  

## Konsekwencje XSS

Istnieje wiele implikacji XSS. Poniżej wymieniamy kilka z nich.

**Przejęcie sesji**

Ponieważ atak XSS może zostać wykorzystany do kradzieży plików cookie sesji, atakujący mogą przejąć sesję i, jeśli im się to uda, podszyć się pod ofiarę.

**Phishingi kradzież danych uwierzytelniających**

Wykorzystując XSS, atakujący mogą wyświetlić użytkownikowi fałszywy monit o zalogowanie. W jednym z ostatnich przypadków strona przeglądarki była częściowo zasłonięta oknem dialogowym z prośbą o połączenie z portfelem kryptowalutowym.

**Inżynieria społeczna**

Za pomocą XSS atakujący może stworzyć pozornie legalne wyskakujące okienko lub alert w zaufanej witrynie. Może to skłonić użytkowników do kliknięcia w złośliwe linki lub odwiedzenia złośliwych witryn.

**Manipulacja treścią i jej niszczenie**

Oprócz phishingu i inżynierii społecznej atakujący może użyć XSS, aby zmienić stronę internetową w innych celach, np. zaszkodzić reputacji firmy.

**Eksfiltracja danych**

XSS może uzyskać dostęp i wykraść wszelkie informacje wyświetlane w przeglądarce użytkownika. Dotyczy to również informacji poufnych, takich jak dane osobowe i informacje finansowe.

**Instalacja złośliwego oprogramowania**

Wyrafinowany atakujący może wykorzystać XSS do rozprzestrzeniania złośliwego oprogramowania. W szczególności może on przeprowadzać ataki drive-by download na podatną na ataki stronę internetową.

