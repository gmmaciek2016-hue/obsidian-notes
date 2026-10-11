---

Intruder to wbudowane narzędzie do analizy rozmytej (fuzzing) pakietu Burp Suite , które umożliwia automatyczną modyfikację żądań i powtarzalne testowanie z uwzględnieniem zmiennych wartości wejściowych. Wykorzystując przechwycone żądanie (często z modułu Proxy ), Intruder może wysyłać wiele żądań z nieznacznie zmienionymi wartościami w oparciu o konfiguracje zdefiniowane przez użytkownika. Służy do różnych celów, takich jak ataki brute-force na formularze logowania poprzez zastępowanie pól nazwy użytkownika i hasła wartościami z listy słów, lub przeprowadzanie ataków rozmytych z wykorzystaniem list słów do testowania podkatalogów, punktów końcowych lub hostów wirtualnych. Funkcjonalność Intrudera jest porównywalna z narzędziami wiersza poleceń, takimi jak **Wfuzz** lub **ffuf** .

Należy jednak pamiętać, że chociaż Intruder może być używany z Burp Community Edition, ma on ograniczenia przepustowości, co znacznie zmniejsza jego szybkość w porównaniu z Burp Professional. To ograniczenie często skłania osoby zajmujące się bezpieczeństwem do korzystania z innych narzędzi do wykrywania niejasności i ataków siłowych. Niemniej jednak Intruder pozostaje cennym narzędziem i warto nauczyć się, jak go skutecznie używać.

Przyjrzyjmy się interfejsowi Intruder:

![Pokazywanie interfejsu intruza](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/2b2a10c651bee6531f8dbeb5e32733e8.png)

Początkowy widok Intrudera prezentuje prosty interfejs, w którym możemy wybrać cel. To pole będzie już wypełnione, jeśli żądanie zostało wysłane z serwera proxy (używając `Ctrl + I`lub klikając prawym przyciskiem myszy i wybierając „Wyślij do Intrudera”).

W Intruderze znajdują się cztery podziałkii:

- **Pozycje** : Ta zakładka umożliwia nam wybranie typu ataku (który omówimy w przyszłym zadaniu) i skonfigurowanie, gdzie chcemy wstawiać nasze ładunki w szablonie żądania.
- **Ładunki** : Tutaj możemy wybrać wartości do wstawienia w pozycje zdefiniowane na karcie **„Pozycje”** . Mamy różne opcje ładunków, takie jak ładowanie elementów z listy słów. Sposób wstawiania tych ładunków do szablonu zależy od typu ataku wybranego na karcie **„Pozycje”** . Karta **„Ładunki”** umożliwia również modyfikację zachowania Intrudera w odniesieniu do ładunków, na przykład definiowanie reguł wstępnego przetwarzania dla każdego ładunku (np. dodawanie prefiksu lub sufiksu, wykonywanie operacji dopasuj i zamień lub pomijanie ładunków na podstawie zdefiniowanego wyrażenia regularnego).
- **Pula zasobów** : Ta zakładka nie jest szczególnie przydatna w Burp Community Edition. Umożliwia ona alokację zasobów pomiędzy różne zadania automatyczne w Burp Professional. Bez dostępu do tych zadań automatycznych ta zakładka ma ograniczone znaczenie.
- **Ustawienia** : Ta zakładka pozwala nam skonfigurować sposób działania ataku. Dotyczy ona przede wszystkim sposobu, w jaki Burp obsługuje wyniki i sam atak. Na przykład możemy oznaczać żądania zawierające określony tekst lub definiować odpowiedź Burp na przekierowanie (3xx).

**Uwaga:** Termin „fuzzing” odnosi się do procesu testowania funkcjonalności lub istnienia poprzez zastosowanie zestawu danych do parametru. Na przykład, fuzzing dla punktów końcowych w aplikacji internetowej polega na pobraniu każdego słowa z listy słów i dołączeniu go do adresu URL żądania (np. http ://MACHINE_IP/WORD_GOES_HERE) w celu obserwacji odpowiedzi serwera.

POZYCJE
Podczas przeprowadzania ataku za pomocą Burp Suite Intruder, pierwszym krokiem jest sprawdzenie pozycji w żądaniu, w których chcemy umieścić nasze ładunki. Pozycje te informują Intruder o lokalizacjach, w których zostaną one umieszczone (co omówimy w kolejnych zadaniach).

Przejdźmy do zakładki Pozycje:

![Wyświetlanie zakładki pozycji](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/1372bbafab835e10806ee6beb6681f36.png)

Należy zauważyć, że Burp Suite automatycznie próbuje zidentyfikować najbardziej prawdopodobne miejsca, w których można umieścić ładunki. Miejsca te są zaznaczone na zielono i oznaczone znacznikami sekcji ( `§`).

Po prawej stronie interfejsu znajdziemy następujące przyciski: `Add §`, `Clear §`i `Auto §`:

- Przycisk `Add §`umożliwia nam ręczne definiowanie nowych pozycji poprzez ich zaznaczenie w edytorze żądań i kliknięcie przycisku.
- Przycisk `Clear §`usuwa wszystkie zdefiniowane pozycje, zapewniając puste miejsce, na którym możemy zdefiniować własne pozycje.
- Przycisk `Auto §`automatycznie próbuje zidentyfikować najbardziej prawdopodobne pozycje na podstawie zapytania. Ta funkcja jest przydatna, jeśli wcześniej usunęliśmy pozycje domyślne i chcemy je odzyskać.

Poniższy plik GIF przedstawia proces dodawania, czyszczenia i automatycznego ponownego wybierania pozycji:

![Proces dodawania, czyszczenia i automatycznego ponownego wybierania pozycji](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/504d75f7c90e1c985dae5e05038f50ac.gif)

Poświęć trochę czasu na zapoznanie się z dodawaniem, czyszczeniem i automatycznym wybieraniem pozycji za pomocą interfejsu Burp Suite Intruder.
PAYLOADS
Na karcie **„Ładunki”**  w Burp Suite Intruder możemy tworzyć, przypisywać i konfigurować ładunki dla naszego ataku. Ta podkarta jest podzielona na cztery sekcje:

![Podzakładka „Ładunki” podzielona na cztery sekcje](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f049dff9e1172b76c0f81ad4771b012d.png)

1. **Zestawy ładunków** :
    - Ta sekcja umożliwia nam wybranie pozycji, dla której chcemy skonfigurować zestaw ładunku, a także wybranie typu ładunku, którego chcemy użyć.
    - Podczas korzystania z typów ataku, które pozwalają na użycie tylko jednego zestawu ładunku (Snajper lub Taran ) , rozwijane menu „Zestaw ładunku” będzie zawierało tylko jedną opcję, niezależnie od liczby zdefiniowanych pozycji.
    - Jeżeli użyjemy typów ataku wymagających wielu zestawów ładunków (Pitchfork lub bomba kasetowa), na liście rozwijanej będzie znajdować się jeden element dla każdej pozycji.
    - **Uwaga:** Przypisując numery w menu rozwijanym „Zestaw danych” dla wielu pozycji, należy zachować kolejność od góry do dołu i od lewej do prawej. Na przykład, przy dwóch pozycjach ( `username=§pentester§&password=§Expl01ted§`), pierwszy element w menu rozwijanym „Zestaw danych” będzie odnosił się do pola nazwy użytkownika, a drugi do pola hasła.
  
2. **Ustawienia ładunku** :
    - W tej sekcji znajdują się opcje specyficzne dla wybranego typu ładunku dla bieżącego zestawu ładunków.
    - Na przykład, używając typu ładunku „Prosta lista”, możemy ręcznie dodawać lub usuwać ładunki z zestawu za pomocą pola **Dodaj** tekst, **Wklej** wiersze lub **Załaduj** ładunki z pliku. Przycisk **Usuń** usuwa aktualnie zaznaczony wiersz, a przycisk **Wyczyść** czyści całą listę. Zachowaj ostrożność podczas ładowania dużych list, ponieważ może to spowodować awarię programu Burp.
    - Każdy typ ładunku będzie miał swój własny zestaw opcji i funkcjonalności. Zapoznaj się z dostępnymi opcjami, aby zrozumieć zakres możliwości.  
        
        ![Dostępne opcje](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/722a734ac5dd6437211504d3bc7bb6c2.png)

3. **Przetwarzanie ładunku** :
    - W tej sekcji możemy zdefiniować reguły, które mają być stosowane do każdego ładunku w zestawie przed jego wysłaniem do celu.
    - Na przykład możemy pisać wielkimi literami każde słowo, pomijać ładunki pasujące do wzorca wyrażenia regularnego lub stosować inne przekształcenia i filtrowanie.
    - Choć możesz nie korzystać z tej sekcji często, może się ona okazać bardzo przydatna, gdy w celu przeprowadzenia ataku konieczne będzie przetworzenie określonego ładunku.
  
4. **Kodowanie ładunku** :
    - Ta sekcja umożliwia nam dostosowanie opcji kodowania naszych ładunków.
    - Domyślnie Burp Suite stosuje kodowanie adresów URL, aby zapewnić bezpieczne przesyłanie danych. Mogą jednak wystąpić sytuacje, w których będziemy chcieli dostosować sposób kodowania.
    - Możemy zastąpić domyślne opcje kodowania adresów URL, modyfikując listę znaków do zakodowania lub odznaczając pole wyboru „Koduj te znaki w adresach URL”.

Wykorzystując te sekcje, możemy tworzyć i dostosowywać zestawy ładunków do specyficznych wymagań naszych ataków. Ten poziom kontroli pozwala nam precyzyjnie dostroić nasze ładunki pod kątem efektywnego testowania i eksploatacji.

Karta **„Pozycje”**  w Burp Suite Intruder zawiera menu rozwijane umożliwiające wybór typu ataku. Intruder oferuje cztery typy ataków, z których każdy ma określone zastosowanie. Przyjrzyjmy się każdemu z nich:

1. **Snajper** : Atak typu Snajper jest domyślną i najczęściej używaną opcją. Przechodzi on cyklicznie przez ładunki, umieszczając jeden ładunek na raz w każdej pozycji zdefiniowanej w żądaniu. Ataki typu Snajper iterują wszystkie ładunki w sposób liniowy, umożliwiając precyzyjne i ukierunkowane testowanie.
    
2. **Taran** : Atak **typu** taran różni się od ataku typu snajper tym, że wszystkie ładunki są wysyłane jednocześnie, a każdy z nich umieszczany jest na odpowiedniej pozycji. Ten typ ataku jest przydatny podczas testowania warunków wyścigu lub gdy ładunki muszą być wysyłane jednocześnie.
    
3. **Pitchfork** : Atak typu Pitchfork umożliwia jednoczesne testowanie wielu pozycji z różnymi ładunkami. Pozwala testerowi zdefiniować wiele zestawów ładunków, z których każdy jest powiązany z określoną pozycją w żądaniu. Ataki Pitchfork są skuteczne, gdy istnieją różne parametry wymagające oddzielnego testowania.
    
4. **Bomba kasetowa** : Atak typu bomba kasetowa łączy w sobie podejście Snajpera i Pitchforka. Wykonuje atak podobny do ataku Snajpera na każdej pozycji, jednocześnie testując wszystkie ładunki z każdego zestawu. Ten typ ataku jest przydatny, gdy wiele pozycji ma różne ładunki i chcemy przetestować je wszystkie razem.

Każdy typ ataku ma swoje zalety i sprawdza się w różnych scenariuszach testowych. Zrozumienie różnic między nimi pomaga nam wybrać odpowiedni typ ataku w oparciu o cele testowe.

Atak typu **Sniper** jest domyślnym i najczęściej używanym typem ataku w Burp Suite Intruder. Jest on szczególnie skuteczny w przypadku ataków jednopozycyjnych, takich jak brute-force hasła lub fuzzing punktów końcowych API . W ataku Sniper dostarczamy zestaw ładunków, który może być listą słów lub zakresem liczb, a Intruder wstawia każdy ładunek w każdą zdefiniowaną pozycję w żądaniu.

Wróćmy do naszego przykładowego szablonu z poprzedniej strony:

Przykładowe stanowiska

POST /support/login/ HTTP/1.1
Host: 10.113.187.115
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
Akceptuj: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Akceptuj język: en-US,en;q=0.5
Akceptacja kodowania: gzip, deflate
Typ zawartości: aplikacja/x-www-form-urlencoded
Długość treści: 37
Pochodzenie: http:// 10.113.187.115
Połączenie: zamknięte
Referent: http:// 10.113.187.115 /support/login/
Żądania aktualizacji niezabezpieczone: 1
nazwa użytkownika= **§pentester§** & hasło= **§Expl01ted§**

W tym przykładzie mamy dwie pozycje zdefiniowane dla parametrów body `username`i `password`body. W ataku Snajpera Intruder bierze każdy ładunek z zestawu i podstawia go kolejno w każdą zdefiniowaną pozycję.

Zakładając, że mamy listę słów zawierającą trzy słowa: `burp`, `suite`i `intruder`, Intruder wygeneruje sześć żądań:

|Numer żądania|Treść żądania|
|---|---|
|1|`username=burp&password=Expl01ted`|
|2|`username=suite&password=Expl01ted`|
|3|`username=intruder&password=Expl01ted`|
|4|`username=pentester&password=burp`|
|5|`username=pentester&password=suite`|
|6|`username=pentester&password=intruder`|

Zaobserwuj, jak Intruder zaczyna od pierwszej pozycji ( `username`) i podstawia na nią każdy ładunek, a następnie przechodzi do drugiej pozycji ( `password`) i wykonuje tę samą zamianę z ładunkami. Całkowitą liczbę żądań wysłanych przez Intruder Sniper można obliczyć jako `requests = numberOfWords * numberOfPositions`.

Atak typu Snajper jest przydatny, gdy chcemy przeprowadzić testy ataków z jednej pozycji, wykorzystując różne ładunki dla każdej pozycji. Pozwala to na precyzyjne testowanie i analizę różnych wariantów ładunku.
Taran
Atak typu **taran** w Burp Suite Intruder różni się od ataku Sniper tym **,** że umieszcza ten sam ładunek w każdej pozycji jednocześnie, zamiast umieszczać każdy ładunek w każdej pozycji po kolei.

Wróćmy do naszego poprzedniego przykładowego szablonu:

Przykładowe stanowiska

POST /support/login/ HTTP/1.1
    Host: MACHINE_IP
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
    Akceptuj: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Akceptuj język: en-US,en;q=0.5
    Akceptacja kodowania: gzip, deflate
    Typ zawartości: aplikacja/x-www-form-urlencoded
    Długość treści: 37
    Pochodzenie: http:// MACHINE_IP
    Połączenie: zamknięte
    Odnośnik: http:// MACHINE_IP /support/login/
    Żądania aktualizacji niezabezpieczone: 1
    
    nazwa użytkownika= §pentester§ & hasło= §Expl01ted§

Używając ataku typu Battering Ram z tą samą listą słów co wcześniej ( `burp`, `suite`, i `intruder`), Intruder wygenerowałby trzy żądania:

|Numer żądania|Treść żądania|
|---|---|
|1|`username=burp&password=burp`|
|2|`username=suite&password=suite`|
|3|`username=intruder&password=intruder`|

Jak pokazano w tabeli, każdy ładunek z listy słów jest wstawiany w każdą pozycję dla każdego żądania. W ataku Battering Ram ten sam ładunek jest wrzucany w każdą zdefiniowaną pozycję jednocześnie, co zapewnia podejście do testowania przypominające atak siłowy.

Atak typu Battering Ram jest przydatny, gdy chcemy przetestować ten sam ładunek w wielu pozycjach jednocześnie, bez potrzeby sekwencyjnej podmiany.

W kolejnych zadaniach przyjrzymy się bliżej konfiguracjom i ustawieniom związanym z atakiem typu Intruder's Battering Ram oraz przeanalizujemy jego zastosowanie w różnych scenariuszach.

PICHFORK

Atak typu **Pitchfork** w Burp Suite Intruder przypomina jednoczesne wykonywanie wielu ataków Snipera. Podczas gdy Sniper używa jednego zestawu ładunków do jednoczesnego testowania wszystkich pozycji, Pitchfork wykorzystuje jeden zestaw ładunków na pozycję (maksymalnie 20) i iteruje je wszystkie jednocześnie.

Aby lepiej zrozumieć Pitchfork, powróćmy do naszego przykładu siłowego, ale tym razem z dwiema listami słów:

1. Pierwsza lista słów zawiera nazwy użytkowników: `joel`, `harriet`i `alex`.
2. Druga lista słów zawiera hasła: `J03l`, `Emma1815`i `Sk1ll`.

Możemy użyć tych dwóch list do przeprowadzenia ataku typu „pitchfork” na formularz logowania. Każde żądanie wykonane podczas ataku wyglądałoby następująco:

|Numer żądania|Treść żądania|
|---|---|
|1|`username=joel&password=J03l`|
|2|`username=harriet&password=Emma1815`|
|3|`username=alex&password=Sk1ll`|

Jak pokazano w tabeli, Pitchfork pobiera pierwszy element z każdej listy i podstawia je do żądania, po jednym na pozycję. Następnie powtarza ten proces dla następnego żądania, pobierając drugi element z każdej listy i podstawiając go do szablonu. Intruder kontynuuje tę iterację, aż jedna lub wszystkie listy wyczerpią się. Należy pamiętać, że Intruder kończy testowanie, gdy tylko jedna z list zostanie ukończona. Dlatego w atakach Pitchfork najlepiej, aby zestawy danych miały tę samą długość. Jeśli długości zestawów danych różnią się, Intruder będzie wysyłał żądania tylko do wyczerpania krótszej listy, a pozostałe elementy z dłuższej listy nie będą testowane.

Atak typu „pitchfork” jest szczególnie przydatny podczas przeprowadzania ataków polegających na wypełnianiu danych uwierzytelniających (credential-stuffing) lub gdy wiele stanowisk wymaga oddzielnych zestawów danych. Umożliwia on jednoczesne testowanie wielu stanowisk z różnymi danymi.

W kolejnych zadaniach przyjrzymy się bliżej konfiguracjom i ustawieniom związanym z atakiem typu Intruder's Pitchfork i przeanalizujemy jego zastosowania w różnych scenariuszach, w tym atakach polegających na wypełnianiu danych uwierzytelniających.

CLASTER BOMB

Atak **bombą kasetową** w Burp Suite Intruder pozwala na wybór wielu zestawów ładunków, po jednym na pozycję (maksymalnie 20). W przeciwieństwie do Pitchforka, gdzie wszystkie zestawy ładunków są testowane jednocześnie, atak bombą kasetową iteruje każdy zestaw osobno, zapewniając przetestowanie każdej możliwej kombinacji ładunków.

Aby zilustrować atak bombą kasetową, użyjmy tych samych list słów, co poprzednio:

- Nazwy użytkowników: `joel`, `harriet`i `alex`.
- Hasła: `J03l`, `Emma1815`i `Sk1ll`.

W tym przykładzie załóżmy, że nie wiemy, które hasło należy do którego użytkownika. Mamy trzech użytkowników i trzy hasła, ale mapowania są nieznane. W takim przypadku możemy użyć ataku typu Clusterbomb, aby przetestować każdą kombinację wartości. Tabela żądań dla naszych pozycji nazwy użytkownika i hasła wyglądałaby następująco:

|Numer żądania|Treść żądania|
|---|---|
|1|`username=joel&password=J03l`|
|2|`username=harriet&password=J03l`|
|3|`username=alex&password=J03l`|
|4|`username=joel&password=Emma1815`|
|5|`username=harriet&password=Emma1815`|
|6|`username=alex&password=Emma1815`|
|7|`username=joel&password=Sk1ll`|
|8|`username=harriet&password=Sk1ll`|
|9|`username=alex&password=Sk1ll`|

Jak pokazano w tabeli, atak bombą kasetową iteruje każdą kombinację dostarczonych zestawów ładunków. Testuje każdą możliwość, podstawiając każdą wartość z każdego zestawu ładunków w odpowiednie miejsce w żądaniu.

Ataki bombami kasetowymi mogą generować znaczny ruch, ponieważ testują każdą kombinację. Liczbę żądań wysyłanych w ataku bombami kasetowymi można obliczyć, mnożąc liczbę wierszy w każdym zestawie danych. Należy zachować ostrożność podczas stosowania tego typu ataku, zwłaszcza w przypadku dużych zestawów danych. Dodatkowo, w przypadku korzystania z Burp Community i jego funkcji ograniczania prędkości Intruder, wykonanie ataku bombami kasetowymi z zestawem danych o umiarkowanej wielkości może zająć znacznie więcej czasu.

Atak typu Cluster bomb jest szczególnie przydatny w scenariuszach siłowego wymuszenia dostępu do danych uwierzytelniających, w których powiązanie między nazwami użytkowników i hasłami jest nieznane.

W kolejnych zadaniach przyjrzymy się bliżej konfiguracjom i ustawieniom związanym z atakiem bombą kasetową typu Intruder oraz przeanalizujemy jego zastosowanie w różnych scenariuszach.
