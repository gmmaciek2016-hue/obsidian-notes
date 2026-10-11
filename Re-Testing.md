Test penetracyjny generuje raport. Klient wdraża poprawki. Następnie zadaje pytanie, które zadaje każdy klient: „Czy rzeczywiście naprawiliśmy usterkę?”.

To pytanie brzmi, po co są ponowne testy, a odpowiedź jest trudniejsza, niż się wydaje. Badania z [Netlas(otwiera się w nowej karcie)](https://netlas.io/blog/when_patches_fail/)Stwierdzono, że 15,5% poprawek zabezpieczeń jest z jakiegoś powodu zawodnych: 8,05% klasyfikowano jako niekompletne, 4,15% jako całkowicie nieprawidłowe, a pozostałe jako obejmujące inne rodzaje awarii. W przypadku danego zlecenia, mniej więcej co szóste ustalenie, które klienci uważają za zamknięte, nie przetrwa kompetentnego ponownego testu. Klienci nie zdają sobie z tego sprawy. Patrzą na zamknięte zgłoszenie w Jira i zakładają, że problem zniknął.

Faza ponownego testowania polega na sprawdzeniu, czy poprawka faktycznie rozwiązała lukę, czy też po prostu spowodowała, że ​​konkretny ładunek z raportu przestał działać. To nie to samo, a ten pokój jest właśnie o tej różnicy.

## Cele edukacyjne

- Rozróżnij ponowne badanie od pełnej ponownej oceny i wyjaśnij, kiedy każde z nich jest właściwe
- Zdefiniuj wyniki zaliczone, niezaliczone, częściowo zaliczone i zaakceptowane pod względem ryzyka i zastosuj je do różnych typów działań naprawczych
- Identyfikuj niekompletne poprawki, testując warianty ładunków, gdy oryginalny dowód koncepcji jest zablokowany
- Zbieraj i organizuj dowody zarówno dla ustaleń stałych, jak i błędnych

## Wymagania wstępne

- Podstawy testów penetracyjnych (poprzednie sale w tym module)
- Podstawowy Burp Suite użytkowanie; musisz czuć się komfortowo HTTP Historia i powtarzacz
- Znajomość struktury raportu pentestu (poprzednie sale w tym module)

Uruchom maszynę poniżej, klikając `Start Lab Machine`przycisk. Docelowa aplikacja internetowa będzie gotowa za około dwie minuty.

Ponowne testowanie i pełna ponowna ocena to dwa rodzaje zaangażowania, których nie można stosować zamiennie, a klienci używają słowa „ponowne testowanie” w odniesieniu do obu. Częścią pracy młodszego pentestera jest zrozumienie rzeczywistych potrzeb klienta, nawet jeśli sam nie wie, na czym polega różnica.

![Różnica między ponownym testowaniem a pełną oceną.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1778754859187.png)

**Czym jest ponowne badanie**

Ponowny test, zwany również weryfikacją naprawczą lub walidacją naprawczą, obejmuje wyłącznie ustalenia z oryginalnego raportu. Używa się tych samych wektorów ataku, ładunków i technik, co w oryginalnym teście. Nie bada się nowej powierzchni ataku ani nie podąża za łańcuchami nowo odkrytych ścieżek. Interwencja jest znacznie krótsza niż w przypadku pierwotnego testu, a rezultatem jest dodatek lub zaktualizowany raport, a nie nowy, pełny raport. Pytanie, na które odpowiadasz, brzmi: „Czy znane problemy zostały naprawione?”

**Czym jest pełna ponowna ocena**

Pełna ponowna ocena traktuje środowisko tak, jakby nie przeprowadzono żadnego wcześniejszego testu. Obejmuje ona całą powierzchnię ataku zdefiniowaną w zakresie, może uwzględniać zaktualizowane narzędzia i nowe dane wywiadowcze dotyczące zagrożeń oraz generuje nowy raport z testów penetracyjnych. Jest to właściwe po istotnych zmianach w infrastrukturze, takich jak migracja do chmury, fuzja lub przejęcie, lub znacząca przeróbka kodu. Pytanie, na które odpowiadasz, brzmi: „Jakie luki w zabezpieczeniach istnieją obecnie?”

**Problem zamieszania**

Klienci kontaktują się z prośbą o „ponowny test” po przebudowie platformy e-commerce od podstaw. Używają słowa, które znają. Tak naprawdę potrzebują ponownej oceny, ponieważ powierzchnia ataku uległa całkowitej zmianie, a pierwotne ustalenia nie stanowią już istotnego punktu odniesienia. Przeprowadzając w tych warunkach ponowny test o określonym zakresie, potwierdzisz, że trzy konkretne luki w zabezpieczeniach z pierwotnego raportu już nie występują, a jednocześnie potencjalnie przeoczysz zupełnie nowe problemy w przebudowanej aplikacji.

Wyjaśnienie tego to umiejętność komunikacyjna, a nie techniczna. Zapytaj, co się zmieniło między pierwotnym testem a obecnym. Jeśli odpowiedź brzmi „wszystko”, konieczna jest ponowna ocena.

Poniższa tabela przedstawia różnice praktyczne:

|Wymiar|Ponowny test|Pełna ponowna ocena|
|---|---|---|
|Zakres|Wnioski wyłącznie z oryginalnego raportu|Pełna powierzchnia ataku|
|Linia bazowa|Oryginalny raport iPoCnotatki|Traktuj środowisko jak nowe|
|Czas trwania|30% pierwotnego czasu zaangażowania|Pełny czas zaangażowania|
|Wyzwalacze|Klient naprawia ustalenia|Istotne zmiany w infrastrukturze, fuzje i przejęcia, przepisywanie kodu|
|Dokument wyjściowy|Dodatek lub zaktualizowany raport|Nowy raport z testów penetracyjnych|
|Pytanie odpowiedziało|Czy znane problemy zostały naprawione?|Jakie luki istnieją obecnie?|

**Gdzie ponowne testowanie znajduje swoje miejsce w cyklu życia testu penetracyjnego**

Standard [przeprowadzania testów penetracyjnych (PTES)(otwiera się w nowej karcie)](http://www.pentest-standard.org/index.php/Main_Page)definiuje siedem faz, które kończą się raportowaniem. Ponowne testowanie nie jest jedną z tych faz; jest to osobne zadanie, które rozpoczyna się po tym, jak klient podejmie działania w związku z raportem. Ma to znaczenie biznesowe: gdy klient pyta: „Czy to nie jest po prostu część tego, za co już zapłaciliśmy?”, odpowiedź brzmi, że oryginalne upoważnienie, czyli Oświadczenie o Zakresie Prac (SIAĆ), jak i dokument zakresu, należą do zamkniętego projektu. Ponowny test wymaga własnej dokumentacji przedprojektowej, nawet jeśli wykonuje go ten sam zespół.

Ponowne testowanie wydaje się proste, ponieważ najtrudniejsza część wydaje się już zrobiona. Oryginalny raport istnieje, zakres jest zdefiniowany, a klient poinformował Cię, co poprawił. Jednak zasada „oryginalne upoważnienie nadal obowiązuje” nie zastępuje kontroli przed rozpoczęciem współpracy, a ich pominięcie stwarza realne problemy.

**Okno naprawcze**

Okno naprawcze to uzgodniony okres między dostarczeniem pierwotnego raportu a ponownym testem, w którym klient wdraża poprawki. Okno to musi zostać określone w pierwotnym Oświadczeniu o Zakresie Prac, a nie negocjowane po dostarczeniu raportu. Oczekiwania stawiane po dostarczeniu raportu są niemal zawsze kontrowersyjne.

Typowe długości okien spotykane w projektach komercyjnych różnią się w zależności od firmy i powinny być określone wSIAĆraczej niż zakładano:

|Długość okna|Kontekst|
|---|---|
|15-30 dni|Poprawki dotyczą wyłącznie krytycznych i ważnych ustaleń|
|30 - 60 dni|Standardowa aplikacja internetowa lub zaangażowanie sieciowe|
|60 - 90 dni|Pełna ocena ze złożonymi ustaleniami wymagającymi zmian w kodzie lub prac architektonicznych|
|90+ dni|Duże przedsięwzięcia lub ustalenia wymagające zmian w infrastrukturze|

**Język zakresu ma znaczenie**

Istnieje realna różnica między „ponownym testowaniem”SQLi„znalezienie”, „ponowne przetestowanie formularza logowania” i „ponowne przetestowanie uwierzytelniania”. Pierwszy z nich jest ściśle ograniczony do udokumentowanej luki w zabezpieczeniach. Drugi obejmuje cały formularz logowania. Trzeci potencjalnie obejmuje wszystkie powierzchnie uwierzytelniania. Jeśli język zakresu w autoryzacji ponownego testu jest niejednoznaczny, należy go wyjaśnić przed testowaniem, a nie po znalezieniu czegoś nieoczekiwanego.

**Nowa powierzchnia ataku podczas ponownego testowania**

Czasami podczas ponownego testu można odkryć coś, czego nie było w pierwotnym raporcie. Być może zauważysz punkt końcowy, który nie powinien istnieć, lub zaobserwujesz zachowanie, które nie zostało przetestowane za pierwszym razem. Prawidłowy protokół to: udokumentuj to, zgłoś klientowi w osobnej notatce, liście obserwacyjnym lub dodatkowym zaleceniu, w zależności od firmy. Nazwa ma mniejsze znaczenie niż fakt, że jest napisany, opatrzony datą i wyraźnie oddzielony od raportu z ponownego testu. Ten pisemny zapis służy ochronie obu stron: dokumentuje on, że zaobserwowałeś, ale nie przetestowałeś powierzchni poza zakresem, tworząc jasną granicę prawną i zgodności.

![Nowa powierzchnia ataku w trakcie ponownego testowania.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1778754980156.png)

Nie należy testować nowej nawierzchni bez pisemnego zezwolenia. Jest to kwestia zgodności i granic prawnych, a nie preferencji stylistycznych. Kontynuowanie prac bez zezwolenia jest działaniem wykraczającym poza zakres, niezależnie od tego, jak bardzo nawierzchnia jest podatna na uszkodzenia.

**Akceptacja ryzyka i kontrola kompensacyjna**

Akceptacja ryzyka to ważny i udokumentowany wynik. Kiedy klient formalnie decyduje się nie naprawiać nieprawidłowości, ponieważ ograniczenia biznesowe przeważają nad ryzykiem, podpisuje dokument akceptujący to ryzyko. Wynik ten jest odnotowywany w raporcie z ponownego testu jako „ **Ryzyko zaakceptowane** ”, a nie „ **Naprawione** ”. Jest to uzasadniona decyzja biznesowa. Twoim zadaniem jest dokładne jej udokumentowanie, aby audytorzy i interesariusze wiedzieli, że nieprawidłowości nie zostały naprawione, a jedynie zaakceptowane.

Powiązanym, ale odrębnym rezultatem jest kontrola kompensacyjna. W tym przypadku klient nie może naprawić błędu, ale wdraża udokumentowaną alternatywną kontrolę, która zmniejsza ryzyko do akceptowalnego poziomu bez usuwania przyczyny źródłowej. Na przykład, w starszym systemie, którego nie można naprawić, dostęp do sieci może zostać ograniczony. Kontrola kompensacyjna jest rejestrowana jako „Kontrola kompensacyjna” lub „Złagodzona” w raporcie z ponownego testu, a nie jako „Zaakceptowane ryzyko”, ponieważ klient podjął działania w celu zmniejszenia ryzyka, zamiast po prostu zaakceptować je w obecnym stanie.

Umiejętność prawidłowej klasyfikacji wyniku ponownego testu stanowi techniczne sedno tego typu zaangażowania. Kategorie wydają się proste, dopóki nie dowiesz się, czego tak naprawdę wymaga „ustalenie”.

**Co tak naprawdę oznacza „naprawiony”**

Wynik zostaje uznany za pozytywny w ponownym testowaniu, gdy pierwotny exploit proof-of-concept przestaje działać, a poprawka nie wprowadza żadnej nowej luki w zabezpieczeniach. Oba warunki muszą zostać spełnione. Poprawka, która zatrzymuje pierwotny ładunek, ale nie narusza głównej przyczyny, nie jest poprawką; jest to częściowe złagodzenie, które nie przejdzie ponownego testowania.

![Rzeczywista definicja naprawy maszyny.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1778755145830.png)Pułapką, w którą wpada wielu programistów, jest blokowanie konkretnego ładunku w raporcie. Widzą  `' OR '1'='1`wyniki, dodają sprawdzenie tego ciągu i oznaczają zgłoszenie jako zamknięte. Testując tylko ten konkretny ładunek, można potwierdzić działanie blokady. Testując warianty, można stwierdzić, że podstawowa luka w zabezpieczeniach nadal istnieje.

**Klasyfikacja wyników**

|Wynik|Kryteria|
|---|---|
|Przechodzić|Oryginalny PoC zablokowany; oczywiste warianty również nie działają; rozwiązano przyczynę źródłową; nie wprowadzono regresji|
|Ponieść porażkę|Oryginalny PoC nadal działa; wariant odnosi sukces, gdy blokowany jest określony ładunek; ten sam podatny wzorzec występuje w sąsiednim kodzie|
|Częściowe/warunkowe zaliczenie|Podatność złagodzona, ale nie wyeliminowana; zaakceptowano kontrolę kompensacyjną; należy wyraźnie udokumentować pozostałe ryzyko o mniejszym stopniu zagrożenia|
|Akceptowane ryzyko|Klient formalnie zaakceptował ryzyko na piśmie, nie testował go jako stałego; udokumentowano go osobno|

Etykiety wyników różnią się w zależności od firmy. W szablonach raportowania różnych organizacji „ **Częściowo zaliczony** ” może być wyświetlany jako „ **Częściowo naprawiony** ”, „ **Złagodzony** ” lub „ **Warunkowo zaliczony** ”. PTES, OWASP, CREST i NIST SP 800-115 nie definiują standardowego schematu klasyfikacji czterech wyników. Kryteria są ważniejsze niż etykieta.

**Weryfikacja poprawki lub aktualizacji oprogramowania**

Gdy klient zastosuje poprawkę dostawcy, należy potwierdzić, że numer wersji uległ zmianie i jest zgodny z poprawioną wersją. Następnie należy ponownie uruchomić PoC dla zaktualizowanej wersji. Samo potwierdzenie wersji nie jest ponownym testowaniem, lecz sprawdzaniem wersji. Skaner, który odczytuje baner wersji i oznacza znalezienie jako zamknięte, robi to samo. Widziałem środowiska, w których baner wersji pokazywał poprawioną wersję, a mimo to podstawowa luka w zabezpieczeniach pozostawała w pełni możliwa do wykorzystania.

Sprawdź, czy poprawka została zastosowana do wszystkich instancji. Środowiska klastrowe często pomijają węzeł. Sprawdź, czy poprawka faktycznie rozwiązuje konkretny zgłoszony problem CVE. Poprawki od dostawców nie zawsze są kompletne (konkretne przykłady omówimy w Zadaniu 5).

Przydatne narzędzia: `nmap`wykrywanie wersji `whatweb`, ręczne sprawdzanie banerów.

**Weryfikacja poprawki kodu**

Wypróbuj oryginalny ładunek w poprawionym punkcie końcowym. Następnie przetestuj warianty kodowania i alternatywne ścieżki parametrów. Jeśli poprawka wygląda na zablokowaną listę, a nie na poprawkę przyczyny źródłowej, zazwyczaj jest odpowiednio testowana.

Gdy dostępny jest przegląd kodu, sprawdź różnice w zatwierdzeniach, aby potwierdzić, że usunięto przyczynę źródłową, a nie tylko dodano listę blokowanych. Programiści często naprawiają jeden punkt końcowy, pozostawiając ten sam wzorzec podatności w trzech innych. Szukaj sąsiedniego kodu, który używa tej samej konstrukcji. W przypadku luk klasy iniekcyjnej, rozwiązanie przyczyny źródłowej oznacza, że ​​struktura zapytania nie może zostać zmieniona, a kanonicznym rozwiązaniem są zapytania z parametrami wejściowymi. Omówimy, jak to wygląda w praktyce w Zadaniu 7.

**Weryfikacja zmiany architektonicznej**

Zmiany architektoniczne są najtrudniejsze do zweryfikowania. Należy zmapować nową architekturę i potwierdzić, że pierwotna ścieżka ataku już nie istnieje. Jeśli usługa została przeniesiona za zaporę WAF, należy sprawdzić, czy pierwotny punkt końcowy jest niedostępny bezpośrednio ORAZ czy reguły WAF są poprawne dla danego typu ataku. Jeśli sieć…segmentacjadodano, sprawdź, czy podsieć dostępna dla atakującego nie może dotrzeć do systemu docelowego.

Zmiany architektoniczne niosą ze sobą również największe ryzyko wprowadzenia nowej powierzchni ataku, ponieważ zmiany na dużą skalę dotyczą wielu systemów, a wzajemne zależności są trudne do przewidzenia.

Pułapki, które powodują, że osoby ponownie testujące wydają fałszywe zaliczenia, nie są egzotycznymi przypadkami skrajnymi. To przewidywalne tryby awarii, w których racjonalni ludzie pracują pod presją czasu, dysponując niekompletnymi informacjami. Znajomość tych błędów z wyprzedzeniem to sposób na ich uniknięcie.

**Pułapka 1: Badanie objawu, a nie przyczyny źródłowej**

To najczęstszy wzorzec awarii. Deweloper otrzymuje raport, widzi dokładny ładunek, który wyzwolił lukę, i blokuje ten konkretny ciąg. Podstawowa luka, niebezpieczna konstrukcja zapytania, niezweryfikowane przekierowanie i deserializowane dane wejściowe nadal występują.

Jeśli odtwarzasz tylko dokładnie to samoPoCZ oryginalnego raportu dowiesz się, czy blokada działa. Wygląda na to, że błąd został naprawiony. Jednak główna przyczyna problemu pozostaje nienaruszona, a każdy atakujący, który wypróbuje wariant, natychmiast ominie blokadę.

Przykład z życia wzięty, który to potwierdza: SAP wydał poprawkę dlaCVE-2025-31324 (CVSS10.0, nieuwierzytelnione przesyłanie plików za pośrednictwem Visual Composer) w kwietniu 2025 r. CVE-2025-42999 demonstruje powiązany problem. Po tym, jak SAP załatał ścieżkę nieuwierzytelnionego przesyłania plików w CVE-2025-31324, badacze zidentyfikowali, że Visual Composer nadal zawiera niebezpieczną lukę w zabezpieczeniach deserializacji. Luka CVE-2025-42999 wymaga użycia uprzywilejowanego atakującego, ale w połączeniu z luką CVE-2025-31324, nieuwierzytelniony atakujący może wykorzystać ścieżkę przesyłania plików do umieszczenia ładunku, który następnie wykonuje komponent deserializacji. Organizacja, która ponownie przetestowała, potwierdzając pytanie „czy uwierzytelnianie jest teraz wymagane na punkcie końcowym przesyłania?”, oznaczyłaby pierwotne ustalenie jako zamknięte. Osoba ponownie testująca, która przetestowała ścieżkę deserializacji i sprawdziła, czy obie luki można połączyć, stwierdziłaby, że złożone ryzyko nadal istnieje.

**Pułapka 2: Brakujące instancje**

Znalezisko istniejące w jednym miejscu, zwykle występuje w podobnych miejscach. SQL injection w formularzu logowania często odzwierciedla podatny na ataki schemat budowania zapytań używany w wielu formularzach. Domyślne dane uwierzytelniające w panelu administracyjnym mogą nadal być domyślnymi danymi uwierzytelniającymi w APIpunkt końcowy. Alista katalogowa To, co znajduje się na jednej ścieżce, może nadal istnieć na innej ścieżce.

![Przykład brakującej instancji w formularzu hasła.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1778755494535.png)Wzorzec brakującej instancji szybko staje się pytaniem o zakres. Jeśli okaże się, że formularz logowania SQLi Błąd został naprawiony za pomocą zapytań parametryzowanych, ale formularz resetowania hasła nadal używa konkatenacji ciągów znaków, a formularz resetowania hasła nie znajdował się w oryginalnym raporcie. Mamy obserwację wykraczającą poza zakres, a nie wynik ponownego testu. Prawidłowe działanie: udokumentować, zgłosić klientowi jako osobną notatkę i nie testować dalej bez pisemnego upoważnienia.

**Pułapka 3: Zastosowano poprawkę, ale niewłaściwa wersja lub niewłaściwe środowisko**

Programiści czasami stosują poprawkę, która rozwiązuje powiązany problem, ale nie konkretny zgłoszony błąd CVE. Albo stosują poprawkę w środowisku testowym, ale wdrożenie produkcyjne jeszcze się nie rozpoczęło. Zawsze weryfikuj numery wersji w systemie, który faktycznie możesz testować, a nie na serwerze kompilacji lub w środowisku testowym, chyba że jest to objęte zakresem.

**Pułapka 4: Niekompletne poprawki dostawców**

Same poprawki od dostawców są czasami niekompletne i nie jest to rzadkością. Udokumentowany przykład:

CVE-2023-43208 powstał bezpośrednio w wyniku niekompletnej poprawki dla CVE-2023-37679. Pierwotny kod CVE nie został uwierzytelniony.RCEpoprzez deserializację Java XStream w Mirth Connect. Poprawka w wersji 4.4.0 rozwiązała lukę, dodając listę blokowanych niebezpiecznych klas Java. Badacze odkryli, że listę blokowanych można było ominąć za pomocą alternatywnych łańcuchów gadżetów, których nie ma na liście. Pełna poprawka pojawiła się w wersji 4.4.1. Tester sprawdzający „czy wersja 4.4.0 jest zainstalowana?” rejestrował błąd PASS w oryginalnym CVE, pozostawiając obejście w pełni podatne na wykorzystanie.

**Pułapka 5: Fałszywa pewność siebie wynikająca ze skanerów automatycznych**

Automatyczne skanery raportują znane sygnatury i numery wersji. Jeśli poprawka zmienia baner wersji, skaner oznacza wykrycie jako rozwiązane. Istnieje drugi, równie niebezpieczny tryb awarii: skaner może wyświetlać komunikat o błędzie po zastosowaniu poprawki z listy odrzuconych, ponieważ zmienił się format odpowiedzi na błąd, a nie dlatego, że luka została naprawiona. Skaner nie dopasowuje już swojej sygnatury do nowej odpowiedzi, więc raportuje wykrycie jako zamknięte, ale konstrukcja zapytania lub obsługa danych wejściowych pozostają nienaruszone. Dokładnie taki scenariusz analizujemy w Zadaniu 6: lista odrzuconych zmienia dane zwracane przez formularz logowania, ale główna przyczyna pozostaje w pełni możliwa do wykorzystania.

Wróciłeś, aby ponownie przetestować aplikację internetową z pierwotnego zlecenia. Podejście z zadania 4 ma zastosowanie bezpośrednio, zaczynając od dokładnego PoCz oryginalnego raportu, a następnie testując warianty ładunków. Załóżmy, że zespół programistów klienta potwierdził, że wszystkie trzy ustalenia z oryginalnego raportu zostały naprawione:

- **F-01** :SQLFormularz logowania do wstrzykiwań (krytyczny)
- **F-02** : Panel administracyjny domyślnych poświadczeń (wysoki)
- **F-03** : Brak nagłówka zabezpieczeń (niski)

Twoim zadaniem jest zweryfikowanie każdego z nich. Skupimy się na F-01, bo to właśnie tam kryje się interesujący wynik.

Obserwuj, jak krok po kroku przechodzimy przez aplikację internetową.

**Krok 1: Przejrzyj pierwotne ustalenia**

Rozważmy raport z testu penetracyjnego zawierający trzy główne ustalenia, jak wspomniano powyżej.

Znajdź Finding F-01. Oryginalny raport dokumentuje ominięcie uwierzytelniania poprzez atak typu SQL injection w formularzu logowania, wykorzystując dane `' OR '1'='1`w polu nazwy użytkownika z dowolnym hasłem. Dowód pokazuje wszystkie rekordy użytkownika zwrócone w treści odpowiedzi.

To jest Twój punkt odniesienia. Wszystko w teście powtórnym jest z nim porównywane.

**Krok 2: Potwierdź stan aplikacji**

Przejdź do `http://10.130.163.66/login`przeglądarki. Sprawdź, czy strona logowania się załadowała.

![Wchodzę na stronę główną BurpSuite.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060168.png)

Otwórz Burp Suite i skonfiguruj przeglądarkę tak, aby obsługiwała proxy przez Burp w przeglądarce `127.0.0.1:8080`. Możesz też użyć FoxyProxy w Firefoksie. Na razie nie włączaj Intercept – sprawdzamy tylko łączność. Powinna załadować się strona logowania, a żądanie powinno pojawić się w karcie historii HTTP.

![Opcja zakładki Historia pakietu Burp Suite.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060294.png)

**Krok 3: Wypróbuj oryginalny ładunek**

Prześlij oryginalny ładunek z raportu. W polu nazwy użytkownika wpisz `' OR '1'='1`dowolną wartość i użyj jej w polu hasła. Prześlij formularz.

Spójrz na odpowiedź w Burp SuiteHTTPKarta Historia. Poszukaj kolumny „Status” w tabeli Historia HTTP, która zawiera trzycyfrowy kod odpowiedzi dla każdego żądania. Aplikacja zwraca stronę z komunikatem „Wykryto nieprawidłowe dane wejściowe” w treści odpowiedzi.

![Określenie dokładnego żądania w Burp Suite.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060314.png)Wygląda na to, że problem został rozwiązany. Ładunek opisany w raporcie jest zablokowany. Ale to nie koniec. To dokładnie taki scenariusz, przed którym ostrzegało nas Zadanie 4. Deweloper mógł zamaskować symptom, nie ujawniając przyczyny problemu.

**Krok 4: Przetestuj warianty kodowania**

Kliknij prawym przyciskiem myszy `POST /login`żądanie w historii HTTP i wyślij je do Repeatera.

![Wysyłanie żądania do zakładki Repeater.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060174.png)

W panelu żądania Repeater zmodyfikuj `username`wartość parametru. Wypróbuj zakodowaną w adresie URL formę oryginalnego ładunku:

```text
%27%20OR%20%271%27%3D%271
```

Wyślij żądanie i obserwuj odpowiedź. Flask `request.form`dekoduje parametr URL przed uruchomieniem jakiegokolwiek kodu aplikacji, więc lista blokowanych adresów widzi ten sam zdekodowany ciąg znaków, który wcześniej zablokowała. Nadal powinieneś widzieć komunikat „ **Wykryto nieprawidłowe dane wejściowe** ”.

![Wykryto nieprawidłowe dane wejściowe w Burp Suite.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060205.png)Potwierdza to, że lista osób blokujących sprawdza zdekodowane dane wejściowe, co jest poprawną higieną, ale nadal nie jest to właściwe rozwiązanie, ponieważ główna przyczyna problemu pozostaje taka sama.

**Krok 5: Przetestuj alternatywną składnię wstrzykiwania**

Nadal w trybie Repeater, spróbuj innego schematu wstrzykiwania. Zastąp wartość nazwy użytkownika:

```text
' OR 1=1--
```

Wyślij prośbę. Zwróć uwagę na panel odpowiedzi, a w szczególności na nagłówki odpowiedzi.

Pomyślne pominięcie uwierzytelnienia nie zwróci danych użytkownika w treści odpowiedzi; w tym przypadku aplikacja przekieruje na inną stronę po pomyślnym zalogowaniu. Poszukaj nagłówka  `Location`w sekcji nagłówków odpowiedzi. Jeśli uwierzytelnienie się powiedzie, odpowiedź będzie zawierać przekierowanie do `/dashboard`strony.

![Nieudane uwierzytelnianie w Burp Suite.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1776336060292.png)

Ten wariant wykorzystuje inną strukturę logiczną niż oryginalny ładunek. W oryginale zastosowano porównanie ciągów znaków ( `'1'='1`). Ten wariant używa porównania liczb całkowitych ( `1=1`) i kończy resztę zapytania SQL operatorem `--`komentarza. Jeśli poprawka programisty polegała na sprawdzeniu oryginalnego ciągu znaków pod kątem listy denylist, ten wariant nie będzie go pasował, a jeśli zapytanie bazowe nadal będzie tworzone poprzez konkatenację ciągów znaków, zostanie wykonane.

**Refleksja metodologiczna**

Cofnijmy się i spójrzmy na to, co właśnie zrobiliśmy. Zaczęliśmy od dokładnego ładunku z oryginalnego raportu, potwierdziliśmy, że jest zablokowany, a następnie przeszliśmy przez warianty kodowania i alternatywną składnię, aż znaleźliśmy wariant, który zadziałał. Ponowne sprawdzenie nie powiodło się, nie dlatego, że konkretny ładunek działa, ale dlatego, że główna przyczyna konkatenacji ciągów w zapytaniu SQL nadal występuje. Każdy wariant, który dotrze do silnika zapytań z prawidłową strukturą wstrzyknięcia, zakończy się powodzeniem.

Podejście jest spójne: najpierw oryginalny dowód koncepcji, potem warianty, a następnie odnotowywanie obserwacji sąsiadujących bez ich testowania. Ta sekwencja sprawdza się w przypadku każdej aplikacji internetowej, która musi znaleźć miejsce, w którym zgłoszono poprawkę kodu.

Raport z ponownego testu nie jest drugą wersją oryginalnego raportu z testu penetracyjnego. Nie zastępuje on oryginału i nie zawiera nowego streszczenia ani nowej narracji dotyczącej ryzyka biznesowego. Uzupełnia oryginał, dostarczając wyniki weryfikacji poszczególnych ustaleń i to wszystko.

Wiarygodność raportu z ponownego testu zależy od porównywalnych dowodów. Te same narzędzia, ta sama metodologia i wyraźne porównanie wyników pierwotnego testu z wynikami ponownego testu.

**Standardy dowodowe**

W przypadku stałych ustaleń zarejestruj blokowany atak.Burp Suite HTTPZrzut ekranu historii pokazujący żądanie i zablokowaną odpowiedź ma poprawny format. Należy dołączyć pełną parę żądania i odpowiedzi HTTP, nie tylko kod statusu, ale także treść, która pokazuje, że atak się nie powiódł. Jeśli poprawka polegała na aktualizacji wersji, należy dołączyć wynik weryfikacji wersji wraz z zablokowaną odpowiedzią.PoC.

![Standardowy format dowodów w raportowaniu.](https://cdn-images.tryhackme.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1778755793194.png)Oznacz wszystko: użyte narzędzie, datę, docelowy adres URL i identyfikator znalezienia. Data ponownego testu musi wyraźnie odróżniać się od daty pierwotnego testu.

**Organizacja dowodów**

Zorganizuj dowody, znajdując dokumenty tożsamości:

```text
/retests/
  F-01/
    original-evidence/      (screenshots from the original report)
    retest-evidence/        (screenshots from your re-test)
    notes.txt               (what you tested, in what order, what you observed)
  F-02/
    ...
```

Oznacz wszystko znacznikiem czasu. Używaj nazw plików zawierających datę i identyfikator wyszukiwania. Kiedy spojrzysz na ten folder po sześciu miesiącach, data ponownego testu musi być jednoznaczna.

**Struktura raportu ponownego testu**

**Sekcja 1: Podsumowanie ponownego testu**

Uwzględnij daty ponownego testu (nie daty pierwotnej oceny), liczbę ponownie sprawdzonych ustaleń, podział na zaliczone/niezaliczone/zaakceptowane ryzyko oraz zalecenia dotyczące wszelkich ustaleń, które nie zostały zaliczone. Przykładowy wiersz podsumowania: „3 ponownie sprawdzone ustalenia: 1 NIEZAAKCEPTOWANE, 2 POPRAWIONE”.

**Sekcja 2: Tabela statusu ustaleń**

To jest główny cel. Każde ustalenie w zakresie otrzymuje wiersz:

|Znalezienie ID|Tytuł|Oryginalna powaga|Rodzaj naprawy|Wynik ponownego testu|Notatki|
|---|---|---|---|---|---|
|F-01|SQLFormularz logowania do wstrzykiwań|Krytyczny|Poprawka kodu|PONIEŚĆ PORAŻKĘ|Dodano listę denylist dla konkretnego ładunku; konkatenacja ciągów pozostaje; wariant `' OR 1=1--`powiódł się|
|F-02|Domyślny panel administracyjny poświadczeń|Wysoki|Zmiana konfiguracji|PRZECHODZIĆ|Zmieniono dane uwierzytelniające; domyślne konto zostało wyłączone|
|F-03|Brak nagłówka bezpieczeństwa|Niski|Zmiana konfiguracji|PRZECHODZIĆ|Nagłówek jest obecny we wszystkich odpowiedziach|

Kolumna „Notatki” zawiera dwie rzeczy: zmiany wprowadzone przez programistę oraz krótką obserwację wyniku dla nieudanych ustaleń. W przypadku pozytywnego wyniku wystarczy jedna klauzula: „Zmieniono dane uwierzytelniające; konto domyślne wyłączone”. W przypadku niepowodzenia należy dodać obserwację wyjaśniającą błąd: „Dodano listę odrzuconych dla określonego ładunku; konkatenacja ciągów znaków pozostaje; wariant `' OR 1=1--`powiódł się”. Notatki powinny być krótkie; szczegóły znajdują się w sekcji 3.

**Sekcja 3: Szczegóły dotyczące poszczególnych ustaleń w przypadku nieudanych ustaleń**

W przypadku stwierdzenia, że ​​wyniki są niekompletne, należy uwzględnić krótką sekcję obejmującą:

- Krótkie podsumowanie pierwotnego ustalenia
- Co zrobił deweloper, aby to naprawić
- Jak to testowałeś podczas ponownego testu?
- Dowody awarii (zrzuty ekranu, archiwa HTTP)
- Zaktualizowana rekomendacja

**Sekcja 4: Dodatek dowodowy**

Zrzuty ekranu z opisowymi podpisami, archiwami HTTP i wynikami narzędzia. Do każdego zrzutu ekranu dodaj identyfikator znalezienia, datę, użyte narzędzie i jego zawartość.

**Czym nie jest raport z ponownego testu**

Raport z ponownego testu, który obejmuje trzy ustalenia, nie jest czystą kartą zdrowia aplikacji. Obejmuje on trzy ustalenia. Jeśli podczas ponownego testu wykryto nową powierzchnię ataku, te obserwacje zostaną umieszczone w osobnej notatce, a nie w raporcie z ponownego testu. Uwzględnienie obserwacji wykraczających poza zakres w raporcie z ponownego testu utrudnia śledzenie zgodności i może rozszerzyć zakres tego, co klienci uważają za zweryfikowane.

Ukończenie ponownego testu wymaga innej dyscypliny niż pierwotna ocena. Pierwotny test polega na odkrywaniu i znajdowaniu tego, co jest. Ponowny test polega na porównaniu, sprawdzając, czy to, co zostało znalezione, zostało faktycznie uwzględnione. Ta zmiana sposobu myślenia, z eksploracji na weryfikację, sprawia, że ​​ponowne testowanie jest odrębną umiejętnością.

Dwa wzorce, które powodują najwięcej niepowodzeń w testach retestowych w praktyce, to te, nad którymi pracowaliśmy bezpośrednio. Łatanie symptomów, gdzie programista blokuje konkretny ładunek zgłoszony w teście bez zajęcia się przyczyną źródłową, odpowiada za dużą część nieudanych testów retestowych. Wzorzec brakującej instancji, gdzie poprawka zastosowana do jednej powierzchni pozostawia tę samą lukę w zabezpieczeniach na sąsiedniej, odpowiada za większośćodpoczynek, choć Zadanie 5 obejmuje pięć dodatkowych pułapek, które regularnie pojawiają się w pracach nad ponownym testowaniem komercyjnym.

Wiarygodny raport z ponownego badania dokumentuje dowody na każde ustalenie, a nie tylko te, które się nie powiodły. Dowód zamknięcia badania jest równie ważny, jak dowód niepowodzenia, ponieważ audytorzy i organy regulacyjne muszą mieć pewność, że każde ustalenie zostało niezależnie zweryfikowane, a nie tylko zamknięte w systemie zgłoszeń.

Ponowne testowanie jest często pierwszym samodzielnym obowiązkiem młodszego pentestera. Ustrukturyzowany, skoncentrowany na porównaniach charakter pracy idealnie pasuje do tej roli. Pracujesz na zdefiniowanej liście, używasz tych samych narzędzi, co w pierwotnej ocenie, i tworzysz dokument z jasną odpowiedzią „zaliczony/niezaliczony” dla każdego wyniku. Wyzwanie analityczne polega na rozpoznaniu, kiedy pozorny wynik jest w rzeczywistości niezaliczony, a umiejętności rozpoznawania takich sytuacji są właśnie tym, co omawialiśmy na tym spotkaniu.
