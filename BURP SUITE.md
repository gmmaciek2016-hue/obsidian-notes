---

W istocie #Burp #Suite to oparta na Javie platforma, zaprojektowana jako kompleksowe rozwiązanie do przeprowadzania testów penetracyjnych aplikacji internetowych. Stała się ona standardowym narzędziem branżowym do praktycznej oceny bezpieczeństwa aplikacji internetowych i mobilnych, w tym tych **,** **które** korzystają **z** **interfejsów** API .

Mówiąc prościej, Burp Suite przechwytuje i umożliwia manipulowanie całym ruchem HTTP /HTTPS między przeglądarką a serwerem WWW. Ta fundamentalna funkcja stanowi podstawę platformy. Dzięki przechwytywaniu żądań użytkownicy mają możliwość elastycznego kierowania ich do różnych komponentów platformy Burp Suite , które omówimy w kolejnych sekcjach. Możliwość przechwytywania, przeglądania i modyfikowania żądań WWW, zanim dotrą one do serwera docelowego, a nawet manipulowania odpowiedziami przed ich otrzymaniem przez przeglądarkę, sprawia, że ​​Burp Suite jest nieocenionym narzędziem do ręcznego testowania aplikacji WWW.

Pakiet Burp Suite jest dostępny w różnych edycjach. W tym artykule skupimy się na wersji **Burp Suite Community Edition** , która jest dostępna bezpłatnie do użytku niekomercyjnego w granicach prawnych. Warto jednak zauważyć, że Burp Suite oferuje również edycje Professional i Enterprise, które zawierają zaawansowane funkcje i wymagają licencji:

1. **Burp Suite Professional** to nieograniczona wersja Burp Suite Community. Zawiera takie funkcje, jak:
    
    - Zautomatyzowany skaner luk w zabezpieczeniach.
    - Fuzzer/brute-forcer, który nie ma ograniczeń przepustowości.
    - Zapisywanie projektów do wykorzystania w przyszłości i generowania raportów.
    - Wbudowane API umożliwiające integrację z innymi narzędziami.
    - Nieograniczony dostęp do dodawania nowych rozszerzeń w celu zwiększenia funkcjonalności.
    - Dostęp do Burp Suite Collaborator (w praktyce zapewniający unikalny moduł przechwytywania żądań, hostowany we własnym systemie lub działający na serwerze będącym własnością Portswigger).
      
    Krótko mówiąc, Burp Suite Professional to niezwykle wydajne narzędzie, co czyni je preferowanym wyborem wśród profesjonalistów z tej dziedziny.
    
1. **Burp Suite Enterprise** , w przeciwieństwie do wersji Community i Professional, służy głównie do ciągłego skanowania. Zawiera automatyczny skaner, który okresowo skanuje aplikacje internetowe w poszukiwaniu luk w zabezpieczeniach, podobnie jak narzędzia takie jak #Nessus przeprowadzają automatyczne skanowanie infrastruktury. W przeciwieństwie do innych edycji, które umożliwiają ręczne ataki z komputera lokalnego, Burp Suite Enterprise działa na serwerze i stale skanuje docelowe aplikacje internetowe w poszukiwaniu potencjalnych luk w zabezpieczeniach.
    
    ![Podgląd Burp Suite Enterprise](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/6b7cdf06b365b6908c41525e8efb86e0.png)

Ze względu na konieczność posiadania licencji na edycje Professional i Enterprise, skupimy się na podstawowych funkcjach udostępnianych przez #Burp Suite Community Edition.
Chociaż Burp Suite Community oferuje bardziej ograniczony zestaw funkcji w porównaniu z edycją Professional, nadal oferuje imponujący zestaw narzędzi, które są niezwykle cenne podczas testowania aplikacji internetowych. Przyjrzyjmy się niektórym kluczowym funkcjom:

- **Proxy** : Proxy Burp to najbardziej rozpoznawalny element pakietu Burp Suite . Umożliwia on przechwytywanie i modyfikowanie żądań i odpowiedzi podczas interakcji z aplikacjami internetowymi.
- **Repeater** : Kolejna dobrze znana funkcja.  [Repeater](https://tryhackme.com/room/burpsuiterepeater) umożliwia wielokrotne przechwytywanie, modyfikowanie i ponowne wysyłanie tego samego żądania. Ta funkcjonalność jest szczególnie przydatna podczas tworzenia ładunków metodą prób i błędów (np. w SQLi – Structured Query Language Injection) lub testowania funkcjonalności punktu końcowego pod kątem luk w zabezpieczeniach.
- **Intruder** : Pomimo ograniczeń przepustowości w Burp Suite Community, [Intruder](https://tryhackme.com/room/burpsuiteintruder) pozwala na rozpylanie żądań na punktach końcowych. Jest powszechnie wykorzystywany do ataków siłowych lub rozmycia punktów końcowych.
- **Dekoder** : [Dekoder](https://tryhackme.com/room/burpsuiteom) oferuje cenną usługę transformacji danych. Może dekodować przechwycone informacje lub kodować dane przed wysłaniem ich do celu. Chociaż istnieją alternatywne usługi do tego celu, wykorzystanie Dekodera w Burp Suite może być bardzo wydajne.
- **Comparer** : Jak sama nazwa wskazuje, [Comparer](https://tryhackme.com/room/burpsuiteom) umożliwia porównanie dwóch fragmentów danych na poziomie słowa lub bajtu. Chociaż nie jest to funkcja dostępna wyłącznie w Burp Suite , możliwość wysyłania potencjalnie dużych segmentów danych bezpośrednio do narzędzia porównującego za pomocą jednego skrótu klawiaturowego znacznie przyspiesza ten proces.
- **Sekwencer** : [Sekwencer](https://tryhackme.com/room/burpsuiteom) jest zazwyczaj używany do oceny losowości tokenów, takich jak wartości plików cookie sesji lub inne dane rzekomo generowane losowo. Jeśli algorytm używany do generowania tych wartości nie zapewnia bezpiecznej losowości, może to narazić na ryzyko katastrofalnych ataków.

Oprócz wbudowanych funkcji, baza kodu Java pakietu Burp Suite ułatwia tworzenie rozszerzeń rozszerzających funkcjonalność frameworka. Rozszerzenia te mogą być napisane w Javie, Pythonie (z wykorzystaniem interpretera Java Jython) lub Ruby (z wykorzystaniem interpretera Java JRuby). Moduł **Burp Suite Extender** umożliwia szybkie i łatwe ładowanie rozszerzeń do frameworka, a sklep BApp **Store** umożliwia pobieranie modułów innych firm. Chociaż niektóre rozszerzenia mogą wymagać licencji profesjonalnej do integracji, nadal istnieje znaczna liczba rozszerzeń dostępnych dla społeczności Burp. Na przykład moduł **Logger++** może rozszerzyć wbudowaną funkcjonalność rejestrowania zdarzeń pakietu Burp Suite .
Burp Suite to jedno z narzędzi, które są bardzo przydatne, zarówno do oceny aplikacji internetowych i mobilnych, testów penetracyjnych, wyszukiwania błędów, a nawet debugowania w aplikacjach webowych. Oto przewodnik po instalacji Burp Suite na różnych platformach:

**Uwaga:** Jeśli używasz AttackBox, Burp Suite jest już zainstalowany, więc możesz pominąć ten krok.

#### Pobieranie

Aby pobrać najnowszą wersję pakietu Burp Suite dla innych systemów, kliknij ten [przycisk](https://portswigger.net/burp/releases/) , aby przejść na stronę pobierania.

**Kali Linux :** Pakiet Burp Suite jest preinstalowany w systemie Kali Linux . Jeśli brakuje go w instalacji Kali, można go łatwo zainstalować z repozytoriów Kali apt .

**Linux , macOS i Windows:** W przypadku innych systemów operacyjnych PortSwigger udostępnia dedykowane instalatory Burp Suite Community i Burp Suite Professional na stronie pobierania Burp Suite . Wybierz system operacyjny z menu rozwijanego i wybierz **Burp Suite Community Edition** . Następnie kliknij **przycisk Pobierz** , aby rozpocząć pobieranie.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/cf27fb99c50eb3c2784212d4f56a7b82.png)

#### Instalacja

Zainstaluj Burp Suite , używając metody odpowiedniej dla Twojego systemu operacyjnego. W systemie Windows uruchom plik wykonywalny, a w systemie Linux uruchom skrypt z terminala (z sudo lub bez). Jeśli nie zdecydujesz się na użycie tej opcji `sudo`podczas instalacji w systemie Linux, Burp Suite zostanie zainstalowany w Twoim katalogu domowym `~/BurpSuiteCommunity/BurpSuiteCommunity`i nie zostanie dodany do folderu `PATH`.

Kreator instalacji zawiera jasne instrukcje i zazwyczaj można bezpiecznie zaakceptować ustawienia domyślne. Zawsze jednak zaleca się dokładne zapoznanie się z instalatorem.

Po pomyślnej instalacji Burp Suite możesz teraz uruchomić aplikację. W następnym zadaniu zajmiemy się wstępną instalacją i konfiguracją.
Możesz korzystać z preinstalowanego pakietu Burp Suite Community Edition w naszym AttackBoxie. Aby uruchomić AttackBox, kliknij przycisk „ **Uruchom AttackBox”** u góry tej strony.

Po uruchomieniu Burp Suite i zaakceptowaniu regulaminu, zostaniesz poproszony o wybranie typu projektu. W Burp Suite Community opcje są ograniczone i wystarczy kliknąć **Dalej** , aby kontynuować.

Następne okno umożliwia wybór konfiguracji Burp Suite. Zaleca się zachowanie ustawień domyślnych, które sprawdzają się w większości sytuacji. Kliknij „ **Uruchom Burp”**  , aby otworzyć główny interfejs Burp Suite .

Po pierwszym uruchomieniu Burp Suite możesz zobaczyć ekran z opcjami szkoleniowymi. Zdecydowanie zalecamy zapoznanie się z tymi materiałami szkoleniowymi, gdy tylko znajdziesz na to czas.

Jeśli nie widzisz ekranu szkoleniowego (lub kolejnych sesji), zostanie wyświetlony panel Burp Dashboard, który na początku może wydawać się przytłaczający. Jednak wkrótce stanie się on znajomy.

Panel Burp podzielony jest na cztery kwadranty, oznaczone w kolejności przeciwnej do ruchu wskazówek zegara, zaczynając od lewego górnego rogu:

![Wyświetlanie różnych kwadrantów na pulpicie nawigacyjnym](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/11202e4c73faa30a757f1439b63b85c6.png)

1. **Zadania** : Menu Zadania pozwala zdefiniować zadania w tle, które Burp Suite będzie wykonywać podczas korzystania z aplikacji. W Burp Suite Community domyślne zadanie „Live Passive Crawl”, które automatycznie rejestruje odwiedzane strony, jest wystarczające do celów tego modułu. Burp Suite Professional oferuje dodatkowe funkcje, takie jak skanowanie na żądanie.
    
2. **Dziennik zdarzeń** : Dziennik zdarzeń zawiera informacje o czynnościach wykonywanych przez Burp Suite , takich jak uruchomienie serwera proxy , a także szczegóły dotyczące połączeń nawiązanych za pośrednictwem Burp.
    
3. **Aktywność dotycząca problemu** : Ta sekcja dotyczy pakietu Burp Suite Professional. Wyświetla luki w zabezpieczeniach zidentyfikowane przez automatyczny skaner, uporządkowane według wagi i możliwe do filtrowania na podstawie pewności co do istnienia luki.
    
4. **Zalecenia** : Sekcja „Zalecenia” zawiera bardziej szczegółowe informacje o zidentyfikowanych lukach, w tym odniesienia i sugerowane środki zaradcze. Informacje te można wyeksportować do raportu. W Burp Suite Community sekcja ta może nie wyświetlać żadnych luk w zabezpieczeniach.

Na różnych kartach i w oknach Burp Suite można zauważyć ikony znaku zapytania ( ![ikona znaku zapytania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/93d5f88c31c7e99d65fda7425a572406.png)).

Kliknięcie tych ikon otwiera nowe okno z przydatnymi informacjami dotyczącymi danej sekcji. Ikony pomocy są nieocenione, gdy potrzebujesz pomocy lub wyjaśnienia konkretnej funkcji, dlatego pamiętaj o ich efektywnym wykorzystaniu.

![Menu pomocy po kliknięciu logo ze znakiem zapytania](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/a68c56aa12934f1fa68758f086a0df3a.png)

Poznając różne zakładki i funkcjonalności pakietu #Burp Suite , stopniowo zaznajomisz się z jego możliwościami.
W Burp Suite nawigacja odbywa się domyślnie głównie za pomocą górnych pasków menu, które umożliwiają przełączanie się między modułami i dostęp do różnych podzakładek w obrębie każdego modułu. Podzakładki pojawiają się na drugim pasku menu, bezpośrednio pod paskiem menu głównego.

Oto jak działa nawigacja:

1. **Wybór modułu** : W górnym wierszu paska menu wyświetlane są dostępne moduły w pakiecie Burp Suite . Możesz klikać poszczególne moduły, aby przełączać się między nimi. Na przykład, na poniższym obrazku wybrano moduł Burp Proxy .
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/cb50d9d010fd277b7ce2c9acf2481125.png)
    
2. **Podzakładki** : Jeśli wybrany moduł ma wiele podzakładek, dostęp do nich można uzyskać za pomocą drugiego paska menu, który znajduje się bezpośrednio pod głównym paskiem menu. Te podzakładki często zawierają ustawienia i opcje specyficzne dla danego modułu. Na przykład, na powyższym obrazku, podzakładka „Przechwytywanie proxy” jest wybrana w module „Burp Proxy” .
    
3. **Odłączanie kart** : Jeśli wolisz wyświetlać wiele kart osobno, możesz je odłączyć i umieścić w osobnych oknach. Aby to zrobić, przejdź do opcji **„Okno”** w menu aplikacji nad paskiem **wyboru modułów** . Następnie wybierz opcję „Odłącz”, a wybrana karta otworzy się w osobnym oknie. Odłączone karty można ponownie odłączyć w ten sam sposób.
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/87c7b704d11abbed8e059a0d33672613.png)

Burp Suite oferuje również skróty klawiaturowe umożliwiające szybką nawigację do zakładek klawiszowych. Domyślnie dostępne są następujące skróty:

|Skrót|Patka|
|---|---|
|`Ctrl + Shift + D`|Panel|
|`Ctrl + Shift + T`|Karta docelowa|
|`Ctrl + Shift + P`|Karta proxy|
|`Ctrl + Shift + I`|Karta intruza|
|`Ctrl + Shift + R`|Karta Repeater|
Zanim przejdziemy do Burp Proxy , przyjrzyjmy się dostępnym opcjom konfiguracji Burp Suite . Istnieją dwa typy ustawień: ustawienia globalne (znane również jako ustawienia użytkownika) i ustawienia projektu.

- **Ustawienia globalne** : Te ustawienia mają wpływ na całą instalację Burp Suite i są stosowane przy każdym uruchomieniu aplikacji. Stanowią one konfigurację bazową dla środowiska Burp Suite .
    
- **Ustawienia projektu** : Te ustawienia są specyficzne dla bieżącego projektu i obowiązują tylko podczas sesji. Należy jednak pamiętać, że Burp Suite Community Edition nie obsługuje zapisywania projektów, więc wszelkie opcje specyficzne dla projektu zostaną utracone po zamknięciu Burp.
    
    Aby uzyskać dostęp do ustawień, kliknij przycisk **„Ustawienia”** na górnym pasku nawigacyjnym. Otworzy się osobne okno ustawień.
    
    ![Przycisk Ustawienia, aby otworzyć osobne okno ustawień](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/40a3ea01d6eadc91d98499c3f921c90f.png)
    
    Poniżej znajduje się obraz pokazujący osobne okno ustawień.
    
    ![Osobne okno ustawień](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/8a6df0ac968a5c33e91903b350253b6b.png)

W oknie Ustawienia po lewej stronie znajduje się menu. Umożliwia ono przełączanie między różnymi typami ustawień, w tym:

1. **Szukaj** : Umożliwia wyszukiwanie określonych ustawień przy użyciu słów kluczowych.
2. **Filtr typu** : Filtruje ustawienia opcji **użytkownika** i **projektu**  .
    - **Ustawienia użytkownika** : Wyświetla ustawienia mające wpływ na całą instalację pakietu Burp Suite .
    - **Ustawienia projektu** : Wyświetla ustawienia specyficzne dla bieżącego projektu.
3. **Kategorie** : umożliwia wybór ustawień według kategorii.

![Przycisk ustawień projektu](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/04cf1a4164616772d9495a3ee2bfd10a.png)  

Warto zauważyć, że wiele narzędzi w pakiecie Burp Suite oferuje skróty do określonych kategorii ustawień. Na przykład moduł **Proxy** zawiera przycisk **Ustawienia** **Proxy** , który otwiera okno ustawień bezpośrednio do odpowiedniej sekcji proxy .

![Przycisk ustawień proxy, który otwiera okno ustawień bezpośrednio w odpowiedniej sekcji proxy](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/09211709d4034aa42ce403780ca12ba0.png)

Funkcja wyszukiwania na stronie ustawień to cenny dodatek, umożliwiający szybkie wyszukiwanie ustawień przy użyciu słów kluczowych.

Poświęć trochę czasu na zapoznanie się z zakresem konfigurowalnych opcji w Burp Suite . Gdy już nabierzesz wprawy, możesz przejść do ćwiczeń związanych z konfiguracją ustawień Burp Suite .
Serwer proxy Burp to fundamentalne i kluczowe narzędzie pakietu Burp Suite . Umożliwia on przechwytywanie żądań i odpowiedzi między użytkownikiem a docelowym serwerem WWW. Przechwycony ruch można modyfikować, przesyłać do innych narzędzi w celu dalszego przetwarzania lub jawnie zezwalać na jego kontynuację do miejsca przeznaczenia.

#### Kluczowe punkty do zrozumienia na temat proxy Burp

- **Przechwytywanie żądań:** Żądania wysyłane przez serwer proxy Burp są przechwytywane i uniemożliwiane dotarcie do serwera docelowego. Żądania pojawiają się na karcie Proxy , co umożliwia dalsze działania, takie jak przekazywanie, usuwanie, edycja lub wysyłanie do innych modułów Burp.  Aby wyłączyć przechwytywanie i zezwolić na nieprzerwane przesyłanie żądań przez serwer proxy , kliknij przycisk. `Intercept is on` 
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/73989984d0985412a3405ea1d6f8d171.png)
    
- **Przejęcie kontroli:** Możliwość przechwytywania żądań pozwala testerom uzyskać pełną kontrolę nad ruchem sieciowym, co jest niezwykle cenne przy testowaniu aplikacji internetowych.
    
- **Przechwytywanie i rejestrowanie:** Burp Suite domyślnie przechwytuje i rejestruje żądania wysyłane przez serwer proxy , nawet gdy przechwytywanie jest wyłączone. Ta funkcja rejestrowania może być pomocna w późniejszej analizie i przeglądaniu wcześniejszych żądań.
    
- **Obsługa protokołu WebSocket:** Burp Suite przechwytuje i rejestruje także komunikację protokołu WebSocket, zapewniając dodatkową pomoc przy analizowaniu aplikacji internetowych.
    
- **Dzienniki i historia:** Przechwycone żądania można przeglądać w  podzakładkach **historii** **HTTP**  i **historii WebSockets , co pozwala na przeprowadzenie analizy retrospektywnej i w razie potrzeby wysyłanie żądań do innych modułów Burp.**
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/8d5388b41dc847d2af38acf7ef4b116c.png)
    
    Dostęp do opcji specyficznych dla serwera proxy można uzyskać, klikając przycisk „ **Ustawienia serwera** **proxy”** . Opcje te zapewniają szeroką kontrolę nad zachowaniem i funkcjonalnością serwera proxy . Zapoznaj się z tymi opcjami, aby zoptymalizować korzystanie z serwera proxy Burp .

#### Niektóre godne uwagi funkcje w ustawieniach proxy

- **Przechwytywanie odpowiedzi:** Domyślnie serwer proxy nie przechwytuje odpowiedzi serwera, chyba że zostanie to wyraźnie zażądane w każdym żądaniu. Pole wyboru „Przechwytuj odpowiedzi na podstawie następujących reguł”, wraz ze zdefiniowanymi regułami, umożliwia bardziej elastyczne przechwytywanie odpowiedzi.
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/e24fd91064186b78014d6afd773d60f3.png)
    
- **Dopasuj i zamień:** Sekcja „Dopasuj i zamień” w **ustawieniach** **serwera proxy** umożliwia użycie wyrażeń regularnych (regex) do modyfikowania żądań przychodzących i wychodzących. Ta funkcja umożliwia dynamiczne zmiany, takie jak modyfikacja agenta użytkownika lub manipulowanie plikami cookie.

### Server proxy
    
Poświęć trochę czasu na zapoznanie się z opcjami #serwera #proxy i poeksperymentowanie z nimi, ponieważ pomoże Ci to lepiej zrozumieć narzędzie i nabrać w nim biegłości.
Należy pamiętać, że podane instrukcje dotyczą przeglądarki Firefox. 

Oto kroki konfiguracji serwera proxy Burp Suite z FoxyProxy:

1. **Zainstaluj FoxyProxy:** Pobierz i zainstaluj [rozszerzenie FoxyProxy Basic](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-basic/) .
    
    **Uwaga: FoxyProxy jest już zainstalowany na AttackBox.**
    
2. **Dostęp do opcji FoxyProxy:** Po zainstalowaniu, w prawym górnym rogu przeglądarki Firefox pojawi się przycisk. Kliknij przycisk FoxyProxy, aby uzyskać dostęp do wyskakującego okienka z opcjami FoxyProxy.
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/fee3f150ebb4d9301023188fddc0458a.png)
    
3. **Utwórz konfigurację proxy Burp :** W oknie opcji FoxyProxy kliknij przycisk **Opcje** . Spowoduje to otwarcie nowej karty przeglądarki z konfiguracjami FoxyProxy. Kliknij przycisk **Dodaj** , aby utworzyć nową konfigurację proxy .
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/5a73425b5de3395c5db2962b9d613506.png)
    
4. **Dodaj szczegóły serwera proxy :** Na stronie „Dodaj serwer proxy ” wprowadź następujące wartości:
    
    - Tytuł: `Burp`(lub dowolna preferowana nazwa)
    - Adres IP serwera proxy:`127.0.0.1`
    - Port:`8080`

    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/b2d6f2b724f123070ca434bf2759df91.png)
    
5. **Zapisz konfigurację:** Kliknij **Zapisz** , aby zapisać konfigurację serwera proxy Burp.
    
6. **Aktywuj konfigurację proxy:** Kliknij ikonę FoxyProxy w prawym górnym rogu przeglądarki Firefox i wybierz `Burp` konfigurację. Spowoduje to przekierowanie ruchu przeglądarki przez `127.0.0.1:8080`. Pamiętaj, że pakiet Burp Suite musi być uruchomiony, aby przeglądarka mogła wysyłać żądania po aktywacji tej konfiguracji.
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/20f5e9db304d164b57c7f7d89fabc63a.png)
    
7. **Włącz przechwytywanie serwera proxy w Burp Suite:** Przejdź do Burp Suite i upewnij się, że opcja Przechwytywanie jest włączona na karcie **Proxy** .
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/9e0f6f47486737deff0e16c4e066120f.png)  
    
8. **Przetestuj serwer proxy:** Otwórz przeglądarkę Firefox i spróbuj uzyskać dostęp do witryny, takiej jak strona główna `http://MACHINE_IP/`. Przeglądarka się zawiesi, a serwer proxy zostanie wypełniony żądaniem HTTP . Gratulacje, udało Ci się przechwycić pierwsze żądanie!

**Zapamiętaj następujące informacje:**

- Gdy konfiguracja serwera proxy jest aktywna, a przechwytywanie jest włączone w Burp Suite , przeglądarka będzie się zawieszać za każdym razem, gdy wysyłasz żądanie.
- Należy zachować ostrożność i nie pozostawiać włączonej funkcji podsłuchu przypadkowo, ponieważ może to uniemożliwić przeglądarce wysyłanie żądań.
- Kliknięcie prawym przyciskiem myszy na żądaniu w Burp Suite umożliwia wykonanie różnych czynności, takich jak przekazanie dalej, porzucenie, wysłanie do innych narzędzi lub wybranie opcji z menu kontekstowego.

Zwróć uwagę na te szczegóły, gdy zaczniesz korzystać z serwera proxy Burp Suite .

**Uwaga:** przed włączeniem przechwytywania należy rozważyć zamknięcie innych kart w przeglądarce AttackBox, ponieważ zamiast żądań z docelowej maszyny wirtualnej , będą odbierane żądania WebSocket .
Karta **„Cel”** w pakiecie Burp Suite oferuje więcej niż tylko kontrolę nad zakresem naszych testów. Składa się z trzech podzakładek:

1. **Mapa witryny** : Ta podzakładka pozwala nam na mapowanie docelowych aplikacji internetowych w strukturze drzewa. Każda strona, którą odwiedzimy, gdy serwer proxy jest aktywny, będzie wyświetlana na mapie witryny. Ta funkcja umożliwia automatyczne generowanie mapy witryny poprzez proste przeglądanie aplikacji internetowej. W Burp Suite Professional możemy również użyć mapy witryny do automatycznego indeksowania docelowej witryny, eksplorowania linków między stronami i mapowania jak największej części witryny. Nawet w Burp Suite Community nadal możemy wykorzystać mapę witryny do gromadzenia danych podczas początkowych etapów enumeracji. Jest to szczególnie przydatne do mapowania interfejsów API, ponieważ wszystkie punkty końcowe API , do których uzyskuje dostęp aplikacja internetowa, zostaną przechwycone na mapie witryny.
    
2. **Definicje problemów** : Chociaż społeczność Burp nie oferuje pełnej funkcjonalności skanowania podatności dostępnej w pakiecie Burp Suite Professional, nadal mamy dostęp do listy wszystkich luk w zabezpieczeniach, których szuka skaner. Sekcja **„Definicje problemów”** zawiera obszerną listę luk w zabezpieczeniach internetowych wraz z opisami i odnośnikami. Zasób ten może być przydatny do odwoływania się do luk w raportach lub do opisu konkretnej luki, która mogła zostać zidentyfikowana podczas testów ręcznych.
    
3. **Ustawienia zakresu** : To ustawienie pozwala nam kontrolować zakres docelowy w Burp Suite . Umożliwia ono uwzględnienie lub wykluczenie określonych domen/ adresów IP w celu zdefiniowania zakresu naszych testów. Zarządzając zakresem, możemy skupić się na aplikacjach internetowych, które są dla nas szczególnie istotne, i uniknąć przechwytywania zbędnego ruchu.

Ogólnie rzecz biorąc, zakładka **Cel** oferuje funkcje wykraczające poza zakres, umożliwiając mapowanie aplikacji internetowych, precyzyjne dostrajanie zakresu docelowego i dostęp do kompleksowej listy luk w zabezpieczeniach sieci w celach informacyjnych.

#### Wyzwanie

Rozejrzyj się po witrynie `http://MACHINE_IP/`– będziemy z niej często korzystać w tym module. Odwiedź każdą inną stronę, do której prowadzą linki ze strony głównej, a następnie sprawdź mapę witryny – jeden punkt końcowy powinien wyróżniać się jako bardzo nietypowy!

Przejdź do tej strony w swojej przeglądarce (lub skorzystaj z sekcji „Odpowiedź” na mapie witryny dla tego punktu końcowego)
Jeśli poprzednie zadania wydawały Ci się zbyt skomplikowane, możesz być pewien, że ten temat będzie o wiele prostszy.

Oprócz modyfikacji naszej zwykłej przeglądarki internetowej, aby mogła współpracować z serwerem proxy , Burp Suite zawiera również wbudowaną przeglądarkę Chromium, która jest wstępnie skonfigurowana do korzystania z serwera proxy bez żadnych modyfikacji, które musieliśmy wprowadzić.

Aby uruchomić przeglądarkę Burp, kliknij `Open Browser`przycisk na karcie proxy. Pojawi się okno przeglądarki Chromium, a wszystkie żądania w tej przeglądarce będą przesyłane przez serwer proxy.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/61ee07fd18e8bac9ec6a566c25a3e814.png)

**Uwaga:** W opcjach projektu i ustawieniach użytkownika dostępnych jest wiele ustawień związanych z przeglądarką Burp. Koniecznie je przejrzyj i dostosuj w razie potrzeby.

Jeśli jednak uruchamiasz Burp Suite w systemie Linux jako użytkownik root (jak w przypadku AttackBox), możesz natknąć się na błąd uniemożliwiający uruchomienie przeglądarki Burp Browser z powodu braku możliwości utworzenia środowiska testowego.

Są dwa proste rozwiązania tego problemu:

1. **Sprytne rozwiązanie:** utwórz nowego użytkownika i uruchom Burp Suite na koncie o niskich uprawnieniach, aby umożliwić bezproblemowe działanie przeglądarki Burp Browser.
2. **Prosta opcja:** Przejdź do sekcji „ `Settings -> Tools -> Burp's browser`i zaznacz opcję `Allow Burp's browser to run without a sandbox` ”. Włączenie tej opcji umożliwi uruchomienie przeglądarki bez piaskownicy . Należy jednak pamiętać, że ta opcja jest domyślnie wyłączona ze względów bezpieczeństwa. Jeśli zdecydujesz się ją włączyć, zachowaj ostrożność, ponieważ włamanie się do przeglądarki może zapewnić atakującemu dostęp do całego komputera. W środowisku szkoleniowym AttackBox prawdopodobnie nie będzie to stanowić poważnego problemu, ale należy z niej korzystać odpowiedzialnie.
Na koniec dochodzimy do jednego z najważniejszych aspektów korzystania z serwera proxy Burp : **zakresu** .

Rejestrowanie i rejestrowanie całego ruchu może szybko stać się przytłaczające i uciążliwe, zwłaszcza gdy chcemy skupić się tylko na konkretnych aplikacjach internetowych. Właśnie tutaj pojawia się zakres.

Ustawiając zakres projektu, możemy zdefiniować, co ma być obsługiwane przez proxy i logowane w Burp Suite . Możemy ograniczyć Burp Suite do konkretnych aplikacji internetowych, które chcemy testować. Najprostszym sposobem jest przejście do `Target`zakładki, kliknięcie prawym przyciskiem myszy na docelowym obiekcie z listy po lewej stronie i wybranie opcji `Add To Scope`. Burp poprosi nas następnie o wybranie, czy chcemy zatrzymać logowanie czegokolwiek, co nie mieści się w zakresie, i w większości przypadków wybieramy `yes`.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/5db0a2b0597830ae32aaaf9b80d73187.gif)  

Aby sprawdzić nasz zakres, możemy przełączyć się na podzakładkę **Ustawienia zakresu w zakładce** **Cel** .

Okno ustawień zakresu pozwala nam kontrolować zakres docelowy poprzez uwzględnianie lub wykluczanie domen/adresów IP. Ta sekcja jest bardzo rozbudowana i warto poświęcić czas na jej dokładne zapoznanie się.

Jednak nawet jeśli wyłączymy rejestrowanie ruchu poza zakresem, serwer proxy nadal będzie przechwytywał wszystko. Aby temu zapobiec, musimy przejść do podzakładki **Ustawienia serwera proxy**`And` `URL` `Is in target scope` i wybrać opcję „Przechwytywanie żądań klientów”.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/97db105960dfe71e42855461e3ef0de2.png)  

Włączenie tej opcji powoduje, że serwer proxy całkowicie ignoruje cały ruch, który nie mieści się w zdefiniowanym zakresie, co skutkuje bardziej przejrzystym widokiem ruchu w pakiecie Burp Suite .
**Uwaga:** AttackBox jest już skonfigurowany do rozwiązania problemu opisanego w tym zadaniu. Jeśli używasz AttackBox i nie chcesz czytać tych informacji, możesz pominąć ten krok i przejść do następnego zadania.

Podczas przechwytywania ruchu HTTP możemy napotkać problem podczas nawigowania do witryn z włączonym protokołem TLS . Na przykład, podczas uzyskiwania dostępu do witryny takiej jak [usunięto błąd] `https://google.com/`, możemy otrzymać błąd informujący, że Urząd Certyfikacji (CA) PortSwigger nie ma uprawnień do zabezpieczenia połączenia. Dzieje się tak, ponieważ przeglądarka nie ufa certyfikatowi prezentowanemu przez Burp Suite.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/8b4b43cac91cd9a80622b953598d05eb.png)

Aby rozwiązać ten problem, możemy ręcznie dodać certyfikat CA PortSwigger do listy zaufanych urzędów certyfikacji w naszej przeglądarce. Oto jak to zrobić:

1. **Pobierz certyfikat CA:** Po aktywowaniu serwera proxy Burp przejdź do http://burp/cert. Spowoduje to pobranie pliku o nazwie `cacert.der`. Zapisz ten plik w dowolnym miejscu na swoim komputerze.
    
2. **Przejdź do ustawień certyfikatów przeglądarki Firefox:** wpisz `about:preferences`adres URL w pasku adresu przeglądarki Firefox i naciśnij **Enter** . Przeniesie Cię to na stronę ustawień przeglądarki Firefox. Wyszukaj na stronie hasło „certyfikaty” i kliknij przycisk „ **Wyświetl certyfikaty** ” .
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/a9de0495b2ac6738520c8f9946afdecb.png)
    
3. **Zaimportuj certyfikat urzędu certyfikacji:** W oknie Menedżera certyfikatów kliknij przycisk **Importuj** . Wybierz `cacert.der`plik pobrany w poprzednim kroku.
    
4. **Ustaw zaufanie dla certyfikatu urzędu certyfikacji :** W wyświetlonym oknie zaznacz pole wyboru „Ufaj temu urzędowi certyfikacji przy identyfikowaniu witryn internetowych” i kliknij przycisk OK.
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/23e5cb317d00c1a5e64def1d46fa9301.png)

Wykonując te kroki, dodaliśmy certyfikat CA PortSwigger do naszej listy zaufanych urzędów certyfikacji. Teraz powinniśmy móc odwiedzać dowolną witrynę z włączonym protokołem TLS bez napotykania błędu certyfikatu.

Aby zapoznać się ze szczegółami procesu importowania certyfikatu, możesz obejrzeć poniższy film:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/fb2a8717ae887eda024a7791d83cefaf.gif)

Postępując zgodnie z tymi instrukcjami, możesz mieć pewność, że Twoja przeglądarka ufa certyfikatowi CA PortSwigger i bezpiecznie komunikuje się ze stronami internetowymi obsługującymi protokół TLS za pośrednictwem serwera proxy Burp Suite .
Mając za sobą informacje na temat konfiguracji serwera proxy , przeanalizujmy uproszczony przykład z życia wzięty.

Zacznijmy od zapoznania się z formularzem wsparcia pod adresem `http://MACHINE_IP/ticket/`:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/5b50c536c72d943a3aa5665bcf8858a5.png)
W teście penetracyjnym rzeczywistej aplikacji internetowej testowalibyśmy to pod kątem różnych czynników, w tym między innymi pod kątem ataku typu Cross-Site Scripting (XSS). Jeśli jeszcze nie zetknąłeś się z atakiem XSS, można go porównać do wstrzyknięcia skryptu po stronie klienta (zazwyczaj w JavaScripcie) do strony internetowej w taki sposób, aby został on wykonany. Istnieją różne rodzaje ataków XSS – typ, którego używamy tutaj, nazywany jest „odbitym” atakiem XSS, ponieważ dotyczy on tylko osoby wysyłającej żądanie internetowe.

#### Przewodnik

Spróbuj wpisać: `<script>alert("Succ3ssful XSS")</script>`w polu „Adres e-mail kontaktowy”. Powinieneś zauważyć, że po stronie klienta znajduje się filtr, który uniemożliwia dodawanie znaków specjalnych niedozwolonych w adresach e-mail:

![GIF demonstrujący filtr po stronie klienta](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/04acd78be44400cf105c7d41b104b7fe.gif)

Na szczęście dla nas filtry po stronie klienta są absurdalnie łatwe do obejścia. Istnieje wiele sposobów, aby wyłączyć skrypt lub po prostu uniemożliwić jego załadowanie.

Skupmy się na razie na prostym pominięciu filtra.

Najpierw upewnij się, że serwer proxy Burp jest aktywny i że podsłuch jest włączony.

Teraz wprowadź poprawne dane do formularza pomocy technicznej. Na przykład: „pentester@example.thm” jako adres e-mail i „Test Attack” jako zapytanie.

Prześlij formularz  —  żądanie powinno zostać przechwycone przez pełnomocnika.

Po przechwyceniu żądania przez serwer proxy możemy teraz zmienić pole adresu e-mail na nasz bardzo prosty ładunek z powyższego linku: `<script>alert("Succ3ssful XSS")</script>`. Po wklejeniu ładunku musimy go zaznaczyć, a następnie zakodować go w adresie URL za pomocą `Ctrl + U`skrótu, aby bezpiecznie wysłać. Proces ten pokazano na poniższym pliku GIF:

![GIF przedstawiający objaśniony proces przechwytywania i kodowania adresu URL wklejonego ładunku](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/58c5bf5382cdee55ab12e0752d819ebe.gif)

Na koniec naciśnij przycisk „Przekaż dalej”, aby wysłać prośbę.

Powinieneś zobaczyć okno ostrzegawcze witryny informujące o udanym ataku XSS !

![Zrzut ekranu pokazujący udany atak XSS](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/0ee12f5040b4c2898a71c1300a76f03f.png)

#BURP #SQL #INJECTION
