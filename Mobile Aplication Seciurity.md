---

Urządzenia mobilne są wszędzie. Używamy ich do bankowości, komunikacji, zakupów i przechowywania niektórych z naszych najwrażliwszych danych osobowych. Dla osoby z grupy red team, aplikacje mobilne należą do najciekawszych i najbardziej satysfakcjonujących celów do oceny. Jednak bezpieczeństwo mobilne jest często traktowane jako niszowa umiejętność, coś, co zdobywa się później, po testach aplikacji internetowych i sieci. Ta sala ma to zmienić.

W tej sali wspólnie przejdziemy przez podstawy testów penetracyjnych aplikacji mobilnych. Przyjrzymy się, jak powstają aplikacje mobilne, jak podchodzą do nich testerzy i jakich luk bezpieczeństwa szukają. Zamiast koncentrować się na jednej platformie, skupimy się na szerokim zakresie, aby zdobyte umiejętności i wiedza miały zastosowanie niezależnie od używanego urządzenia.

Testowanie aplikacji mobilnych różni się od testowania aplikacji webowych, mimo że oba te obszary mają pewne wspólne cechy. Aplikacja mobilna ma swój własny format pakietów, własny model uprawnień oraz własny zestaw komponentów, które współdziałają z systemem operacyjnym i ze sobą nawzajem. Zrozumienie tych różnic odróżnia testera, który potrafi znaleźć powierzchowne problemy, od testera, który potrafi rzetelnie rozłożyć aplikację mobilną na czynniki pierwsze.

Pod koniec tego szkolenia będziesz dysponować solidnymi podstawami, na których będziesz mógł dalej budować, niezależnie od tego, czy będzie to oznaczało przejście do testowania konkretnej platformy, zdobycie dedykowanych narzędzi, czy też radzenie sobie z wyzwaniami bezpieczeństwa urządzeń mobilnych w TryHackMe.

## Cele edukacyjne

- Dowiedz się, czym jest testowanie penetracyjne aplikacji mobilnych i dlaczego jest ono ważne z perspektywy zespołu red.
- Dowiedz się, jak zbudowane są aplikacje mobilne i co znajduje się w pakiecie
- Stosuj jasną metodologię podczas testowania aplikacji mobilnych
- Dokonywać analizy statycznej w pakiecie aplikacji mobilnej w celu znalezienia luk w zabezpieczeniach
- Zrozum jak analiza dynamiczna prace i jakie techniki są w nie zaangażowane
- Rozpoznaj najczęstsze kategorie luk w zabezpieczeniach aplikacji mobilnych
- Zastosuj umiejętności analizy statycznej w praktycznym wyzwaniu w stylu CTF

## Wymagania wstępne

Przed rozpoczęciem pracy nad tym pokojem zalecamy wykonanie następujących czynności:

- [LinuxPodstawy](https://tryhackme.com/room/linuxfundamentalspart1) 
- [Podstawy sieci WWW](https://tryhackme.com/path/outline/web)
- [Burp Suite: Moduł](https://tryhackme.com/module/learn-burp-suite)

Pewna znajomość sposobu komunikacji aplikacji internetowych HTTPA protokół HTTPS pomoże Ci w pełni wykorzystać potencjał dynamicznej analizy. Jeśli nie korzystałeś wcześniej z Burp Suite, nie martw się: to zadanie ma charakter koncepcyjny i nie wymaga praktyki. pełnomocnik praca jest wymagana.

Zanim zaczniemy szukać luk w zabezpieczeniach aplikacji mobilnej, musimy zrozumieć, z czym tak naprawdę pracujemy. Aplikacja mobilna to nie tylko pojedynczy plik. To ustrukturyzowany pakiet zawierający wszystko, czego aplikacja potrzebuje do działania: skompilowany kod, pliki konfiguracyjne, zasoby i aktywa. Wiedza o tym, co znajduje się gdzie w tym pakiecie, decyduje o skuteczności testera.

## Pakiet aplikacji

Gdy programista tworzy aplikację mobilną, wynikiem jest plik pakietu. Pakiet ten zawiera plik binarny aplikacji, plik konfiguracyjny, który informuje system operacyjny, jak aplikacja powinna się zachowywać, oraz wszystkie pliki pomocnicze potrzebne aplikacji, takie jak obrazy, czcionki, lokalne bazy danych i zapisane ciągi znaków.

Z perspektywy testera ten pakiet to punkt wyjścia. Jeśli uda nam się go zdobyć, możemy zacząć go rozbierać na części, zanim jeszcze uruchomimy choćby jedną linijkę kodu.

## Manifest i plik konfiguracyjny

Jednym z najważniejszych plików w pakiecie każdej aplikacji mobilnej jest manifest, czyli plik konfiguracyjny. Ten plik stanowi deklarację aplikacji w systemie operacyjnym. Zawiera on nazwę aplikacji, jej wersję, żądane uprawnienia oraz sposób konfiguracji jej wewnętrznych komponentów i informację, czy są one dostępne dla innych aplikacji na urządzeniu.

Dla testera ten plik to prawdziwa kopalnia złota. Błędy w konfiguracji są tu częstym zjawiskiem w rzeczywistych środowiskach. Często dotyczą one niepotrzebnie eksponowanych komponentów lub uprawnień znacznie wykraczających poza potrzeby aplikacji.

## Sandbox Model

Mobilne systemy operacyjne wykorzystują piaskownicę do izolowania aplikacji od siebie. Każda aplikacja działa w swoim własnym pojemniku domyślnie nie może odczytywać plików innej aplikacji ani bezpośrednio wchodzić w interakcje z jej procesami. Jest to celowa kontrola bezpieczeństwa, mająca na celu ograniczenie szkód, jakie może wyrządzić złośliwa lub zainfekowana aplikacja.

Jako testerzy musimy zrozumieć sandbox, ponieważ kształtuje on powierzchnię ataku. Jeśli znajdziemy sposób na wydostanie się z niego lub jeśli aplikacja została skonfigurowana w sposób osłabiający jej własną izolację, jest to godne uwagi odkrycie. Zrozumienie tego, przed czym chroni sandbox, pomaga nam skupić się na obszarach, w których prawdopodobnie występują rzeczywiste luki w zabezpieczeniach.

## Komponenty aplikacji

Aplikacje mobilne nie są monolityczne. Składają się z odrębnych komponentów, z których każdy spełnia określone zadanie i może na różne sposoby oddziaływać na system operacyjny i inne aplikacje. Niektóre komponenty obsługują to, co użytkownik widzi na ekranie. Inne działają w tle, reagują na zdarzenia systemowe lub dostarczają dane innym aplikacjom.

Dla testera istotne jest, aby każdy z tych komponentów można było skonfigurować jako wewnętrzny (dostępny tylko w aplikacji) lub eksportowany (dostępny dla innych aplikacji na urządzeniu). Wyeksportowany komponent, który nie miał być ujawniony, stanowi powierzchnię ataku. Powrócimy do tego w Zadaniu 6, gdzie omówimy typowe luki w zabezpieczeniach.

## Dlaczego struktura pakietu ma znaczenie

Zrozumienie struktury pakietu oznacza, że ​​rozpoczynając analizę aplikacji, dokładnie wiemy, gdzie szukać. Wiemy, że informacje o konfiguracji i uprawnieniach znajdują się w manifeście. Wiemy, że logika aplikacji znajduje się w skompilowanym kodzie. Wiemy, że ciągi znaków, klucze i inne zakodowane na stałe wartości często trafiają do plików zasobów. Ta wiedza sprawia, że…analiza statyczna, które omówimy w Zadaniu 4, zarówno systematyczne, jak i powtarzalne.

Dobre testy penetracyjne nie polegają na uruchamianiu narzędzi i liczeniu na pojawienie się czegoś interesującego. Chodzi o przestrzeganie powtarzalnego procesu, który daje pewność, że dokładnie przeanalizowano aplikację. Testowanie aplikacji mobilnych opiera się na tych samych zasadach, podzielonych na cztery fazy, a wyniki są kategoryzowane według…[OWASPTop 10 urządzeń mobilnych(otwiera się w nowej karcie)](https://owasp.org/www-project-mobile-top-10/).

## Fazy ​​testu penetracyjnego urządzeń mobilnych

Test penetracyjny aplikacji mobilnych zazwyczaj składa się z czterech faz:

![Czteroetapowy przebieg testowania bezpieczeństwa urządzeń mobilnych: (1) Rekonesans, fioletowy, przedstawia telefon, dokument i kulę ziemską pod lupą; (2) Analiza statyczna, zielony, przedstawia plik kodu pod lupą; (3) Analiza dynamiczna, niebieski, przedstawia telefon z błędem i monitorem aktywności; (4) Raportowanie, pomarańczowy, przedstawia listę kontrolną schowka z tarczą. Etapy przebiegają od lewej do prawej.](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1778731395457.png)

- **Rekonesans:** Proces gromadzenia informacji o aplikacji docelowej przed rozpoczęciem testów. Obejmuje on zrozumienie funkcji aplikacji, użytkowników, usług zaplecza, z którymi współpracuje oraz miejsca, w którym można uzyskać pakiet aplikacji. Im szerszy kontekst poznamy, tym bardziej ukierunkowane i skuteczne będą nasze testy.
- **Analiza statyczna:  Badanie** aplikacji bez jej uruchamiania. Rozpakowujemy pakiet, odczytujemy konfigurację, sprawdzamy skompilowany kod i szukamy widocznych problemów bez wykonywania ani jednej instrukcji. Ta faza często dostarcza najszybszych i najbardziej znaczących wniosków.
- **Analiza dynamiczna**: Polega na uruchomieniu aplikacji i obserwowaniu jej zachowania w czasie rzeczywistym. Przechwytujemy wysyłany przez nią ruch, monitorujemy sposób, w jaki przetwarza dane w czasie wykonywania, i wchodzimy w interakcję z jej komponentami, aby sprawdzić, czy zachowują się bezpiecznie. Ta faza ujawnia luki w zabezpieczeniach, które są widoczne tylko wtedy, gdy aplikacja faktycznie działa.
- **Raportowanie:** Dokumentujemy nasze odkrycia, wyjaśniamy ryzyko, jakie stwarza każde z nich, i zapewniamy zespołowi programistów jasne, praktyczne wskazówki, jak je naprawić. Odkrycie, którego nie da się zrozumieć ani odtworzyć, nie jest nikomu przydatne.

## OWASP Mobile Top 10

Projekt [bezpieczeństwa otwartych aplikacji internetowych(otwiera się w nowej karcie)](https://owasp.org/www-project-mobile-top-10/)(OWASP) prowadzi listę 10 najpoważniejszych zagrożeń bezpieczeństwa w aplikacjach mobilnych. Lista ta jest najbliższa uniwersalnej liście kontrolnej do testowania aplikacji mobilnych, jaką posiada branża, i będziemy jej używać w tym miejscu do kategoryzowania ustaleń.

Obecne kategorie obejmują między innymi niewłaściwe użycie danych uwierzytelniających, niewystarczające zabezpieczenia łańcucha dostaw, niezabezpieczone uwierzytelnianie, niewystarczającą walidację danych wejściowych i wyjściowych, niezabezpieczoną komunikację oraz niewystarczające zabezpieczenia binarne. Nie musisz od razu zapamiętywać całej listy. Ważne jest zrozumienie, że takie ramy istnieją, są powszechnie uznawane i że powiązanie ich z wynikami pomaga jasno komunikować ryzyko zarówno deweloperom, jak i interesariuszom.

## Testowanie podejść

Nie wszystkie oceny mobilne są takie same. Ilość informacji i dostęp, jaki ma tester, wpływają na podejście:

- **Testowanie metodą czarnej skrzynki:** rozpoczynanie bez wcześniejszej wiedzy o aplikacji **,**  jak miałoby to miejsce w przypadku ataku z zewnątrz. Masz samą aplikację i nic więcej.
- **Testowanie szarej skrzynki:**  Najpopularniejsze podejście w profesjonalnych projektach. Tester posiada pewne informacje, być może uprawnienia do testowania uwierzytelnionych funkcjonalności lub dostęp do fragmentów kodu źródłowego, ale nie ma pełnej widoczności.
- **Testowanie białoskrzynkowe:** Daje testerowi pełny dostęp do kodu źródłowego, dokumentacji i szczegółów architektonicznych. Pozwala to na najdokładniejszą ocenę, ale wymaga więcej czasu i kontekstu, aby przeprowadzić ją prawidłowo.

## Zakres i raportowanie

Przed rozpoczęciem jakiegokolwiek zaangażowania należy jasno określić zakres. Oznacza to uzgodnienie, które wersje aplikacji będą testowane, które środowiska zaplecza są objęte zakresem oraz jakie działania tester może podjąć. Testowanie poza zakresem, nawet przypadkowe, może mieć realne konsekwencje.

W przypadku raportowania, ustalenia są zazwyczaj uszeregowane według ważności: krytyczne, wysokie, średnie i niskie. Każde ustalenie powinno zawierać jasny opis problemu, kroki prowadzące do jego odtworzenia, potencjalne skutki w przypadku wykorzystania oraz zalecaną poprawkę.

Analiza statycznato proces badania aplikacji mobilnej bez jej uruchamiania. Jest to niemal zawsze pierwszy krok techniczny w interakcji z aplikacją mobilną, ponieważ wymaga jedynie pakietu aplikacji i często pozwala na uzyskanie istotnych wyników jeszcze przed wykonaniem choćby jednej linijki kodu. Poniższe kroki opisują, na co zwracamy uwagę i jak narzędzia przyspieszają i zwiększają niezawodność procesu.

## Odbieranie i rozpakowywanie przesyłki

Pierwszym krokiem jest zdobycie pakietu aplikacji. Może on pochodzić bezpośrednio od klienta w ramach współpracy typu „grey-box” lub „white-box”, zostać pobrany z samego urządzenia lub pochodzić ze sklepu z aplikacjami. Po otrzymaniu pakietu rozpakowujemy go.

Dekompilator to narzędzie, którego używamy do rozpakowania pliku binarnego i konwersji go z powrotem na coś czytelnego dla człowieka. Wynik nie będzie identyczny z kodem źródłowym. Będzie jednak wystarczająco dokładny, aby odczytać logikę aplikacji, śledzić przepływ danych i identyfikować problemy w sposobie, w jaki aplikacja obsługuje poufne informacje.

## Czytanie Manifestu: Android

Po rozpakowaniu pakietu, pierwszym miejscem, do którego zaglądamy, jest plik manifestu. Jak omówiliśmy w Zadaniu 2, plik ten dokumentuje konfigurację aplikacji. Przeglądając go podczas analizy statycznej, szukamy:

- **Zbyt duże żądanie uprawnień** : Czy aplikacja żąda dostępu, którego pozornie nie potrzebuje? Szerokie uprawnienia zwiększają potencjalne szkody w przypadku naruszenia bezpieczeństwa aplikacji.
- **Wyeksportowane komponenty** : Czy jakiekolwiek działania, usługi lub dostawcy danych są oznaczone jako dostępne dla innych aplikacji, mimo że nie powinny być? Wyeksportowany komponent, który obsługuje poufne dane lub akcje uprzywilejowane, stanowi bezpośrednią powierzchnię ataku.
- **Flagi niebezpiecznej konfiguracji** : Niektóre ustawienia w manifeście mogą osłabić bezpieczeństwo aplikacji, jeśli zostaną pozostawione przy niebezpiecznych wartościach domyślnych.

## Czytanie manifestu: iOS

W systemie iOS odpowiednikiem manifestu Androida jest plik `Info.plist`. Ten plik listy właściwości służy temu samemu celowi: deklaruje uprawnienia, ustawienia konfiguracji i zachowanie aplikacji w systemie operacyjnym. Analizując aplikację na iOS, szukamy tych samych kategorii problemów.

Na niebezpieczne flagi konfiguracyjne warto zwrócić szczególną uwagę w systemie iOS. Jedną z najczęstszych jest `NSAllowsArbitraryLoads`klucz w  `NSAppTransportSecurity`słowniku. Po ustawieniu tej flagi na wartość true, ta flaga wyłącza funkcję App Transport Security firmy Apple, która zazwyczaj wymusza protokół HTTPS dla wszystkich połączeń wychodzących. Aplikacja z włączoną tą flagą może komunikować się przez niezaszyfrowane połączenie.HTTP, który bezpośrednio mapuje doOWASPM5: Niebezpieczna komunikacja i M8: Błędna konfiguracja zabezpieczeń.

## Polowanie na zakodowane na stałe sekrety

Jednym z najczęstszych ustaleń w analizie statycznej urządzeń mobilnych jest obecność zakodowanych na stałe wrażliwych danych. Deweloperzy czasami pomijająAPIklucze, hasła, klucze szyfrujące lub wewnętrzne adresy URL bezpośrednio w kodzie aplikacji lub plikach zasobów. Gdy atakujący zdobędzie pakiet aplikacji, jego wyodrębnienie jest banalnie proste.

Szukamy zakodowanych na stałe sekretów w kilku miejscach: w skompilowanym kodzie aplikacji po dekompilacji, w plikach zasobów łańcuchowych, w plikach konfiguracyjnych dołączonych do pakietu oraz w dowolnych plikach lokalnej bazy danych uwzględnionych w zasobach.

W systemie iOS pliki z listami właściwości .plist są częstym miejscem przechowywania poufnych danych. Pliki te są dołączone bezpośrednio do pakietu aplikacji i są w pełni czytelne po rozpakowaniu pliku IPA, co czyni je równie ryzykownymi, jak każdy inny zakodowany na stałe sekret.

Często wystarczy proste wyszukiwanie typowych wzorców, takich jak ciągi znaków, które wydają się być kluczami API, tokenami lub hasłami, aby szybko wykryć te problemy.

## Korzystanie z MobSF do automatycznego skanowania

Ręczna analiza statyczna jest dokładna, ale czasochłonna. Mobile Security Framework (MobSF) to zautomatyzowane narzędzie typu open source, które przeprowadza analizę statyczną pakietu aplikacji mobilnej i generuje szczegółowy raport obejmujący uprawnienia, zakodowane na stałe hasła, niebezpieczne konfiguracje i wiele innych. Działa na obu głównych platformach mobilnych, co czyni je solidnym punktem wyjścia do wszelkich działań mobilnych, niezależnie od typu testowanego urządzenia.

Używamy MobSF, aby uzyskać szybki przegląd stanu bezpieczeństwa aplikacji, zanim przejdziemy do analizy manualnej. Narzędzie to szybko wykryje oczywiste problemy, pozwalając nam skupić się na tym, co zautomatyzowane narzędzie mogłoby przeoczyć, na przykład na błędach w logice biznesowej lub subtelnych problemach z obsługą danych w kodzie aplikacji.

## Mapowanie na podstawie OWASP Mobile Top 10

Wyniki analizy statycznej zazwyczaj odpowiadają następującym kategoriom OWASP Mobile Top 10:

- **M1: Niewłaściwe użycie poświadczeń** , zakodowane na stałe poświadczenia, klucze API i tokeny znalezione w kodzie aplikacji lub zasobach.
- **M8: Nieprawidłowa konfiguracja zabezpieczeń** , żądanie zbyt wielu uprawnień, wyeksportowane komponenty, które powinny być wewnętrzne, oraz niebezpieczne flagi konfiguracji w manifeście.

Kategorie te pojawią się ponownie w Zadaniu 6, gdy przejdziemy przez cały obraz podatności.

Analiza statyczna mówi nam wiele o aplikacji mobilnej, zanim ją uruchomimy. Jednak niektóre luki w zabezpieczeniach pojawiają się dopiero, gdy aplikacja faktycznie działa. Właśnie wtedy analiza dynamiczna To zadanie ma charakter koncepcyjny. Nie będziesz potrzebować laboratorium ani żadnych narzędzi, aby je wykonać, ale uzyskasz jasny obraz tego, co dzieje się na tym etapie mobilnego zaangażowania.

Analiza dynamiczna oznacza obserwację i interakcję z działającą aplikacją. Zamiast czytać kod, obserwujemy, co aplikacja faktycznie robi: jakie dane wysyła przez sieć, jak przechowuje informacje na urządzeniu, co zapisuje w logach i jak reaguje, gdy bezpośrednio sondujemy jej komponenty.

Kluczową różnicą w porównaniu z analizą statyczną jest to, że analiza dynamiczna zajmuje się zachowaniem, a nie kodem. Aplikacja może wyglądać bezpiecznie na papierze, ale w czasie wykonywania przetwarzać dane w sposób niezabezpieczony. Podobnie, coś, co wygląda podejrzanie w kodzie, może być nieszkodliwe w praktyce. Obie fazy są niezbędne do dokładnej oceny.

Przechwytywanie ruchu
Jednym z pierwszych kroków, jakie tester podejmuje podczas analizy dynamicznej, jest przechwycenie ruchu sieciowego aplikacji. Kierując komunikację aplikacji przezpełnomocnik Dzięki temu narzędziu możemy zobaczyć każde żądanie wysyłane przez aplikację i każdą otrzymaną przez nią odpowiedź. Ujawnia to wiele informacji: jakie dane aplikacja wysyła do swojego zaplecza, czy dane te są przesyłane bezpiecznym kanałem (np. HTTPS/TLS), czy tokeny uwierzytelniające są obsługiwane bezpiecznie i czy aplikacja komunikuje się z jakimikolwiek nieoczekiwanymi usługami stron trzecich.

Nieszyfrowany ruch jest natychmiast wykrywany. Dane wrażliwe przesyłane przez HTTP zamiast HTTPS lub przesyłane w sposób umożliwiający odczytanie zwykłego tekstu, mapuje się bezpośrednio do OWASP Kategoria 10 najpopularniejszych usług mobilnych M5: Niebezpieczna komunikacja.

Przypinanie SSL
Wiele aplikacji implementuje przypinanie SSL jako obronę przed przechwytywaniem ruchu. Przypinanie SSL oznacza, że ​​aplikacja otrzymała polecenie, aby ufać tylko określonemu certyfikatowi lub określonemu zestawowi certyfikatów, a nie certyfikatowi podpisanemu przez uznany organ. Gdy tester konfiguruje serwer proxy, serwer proxy prezentuje własny certyfikat, a aplikacja z włączonym przypinaniem SSL odmówi komunikacji, wyświetli błąd lub przestanie działać.

Przypinanie SSL samo w sobie nie jest luką w zabezpieczeniach, lecz mechanizmem kontroli bezpieczeństwa. Testerzy muszą jednak obejść ten mechanizm, aby ocenić ruch w aplikacji. Narzędziem najczęściej kojarzonym z tym problemem jest Objection. (otwiera się w nowej karcie), mobilny zestaw narzędzi do eksploracji środowiska uruchomieniowego, który może wyłączyć przypinanie SSL w działającej aplikacji bez konieczności dostępu do kodu źródłowego. Objection umożliwia również testerom interakcję z wyeksportowanymi komponentami i inspekcję danych aplikacji w czasie wykonywania. Pełny opis Objection wykracza poza zakres tej sali, ale warto wiedzieć, że istnieje i do czego służy, gdy przejdziesz do bardziej zaawansowanych testów mobilnych.

Instrumentacja środowiska wykonawczego
Instrumentacja środowiska uruchomieniowego to technika polegająca na dołączaniu się do działającej aplikacji i obserwowaniu lub modyfikowaniu jej zachowania z zewnątrz. Można ją porównać do debugera, ale takiego, który został zaprojektowany specjalnie do testowania bezpieczeństwa, a nie do programowania.

Frida(otwiera się w nowej karcie)to najpopularniejszy framework instrumentacji środowiska uruchomieniowego do testowania bezpieczeństwa urządzeń mobilnych. Korzystając z Fridy, tester może wyświetlić listę klas i metod w działającej aplikacji, podłączyć się do określonych funkcji, aby sprawdzić, jakie dane są przez nie przekazywane, ominąć weryfikację uwierzytelniania oraz wyodrębnić dane przechowywane w pamięci aplikacji. To potężna technika, dzięki której testerzy znajdują luki w zabezpieczeniach, które nigdy nie pojawiłyby się w samej analizie statycznej. Objection, który omówiliśmy w sekcji dotyczącej przypinania SSL, jest oparty na Fridzie. Jeśli wbudowane polecenia Objection nie obejmują konkretnego, potrzebnego hooka, kolejnym krokiem jest napisanie własnego skryptu Fridy.

Niezabezpieczone rejestrowanie
Aplikacje często zapisują informacje w dzienniku systemowym w celu debugowania. W aplikacji produkcyjnej rejestrowanie to powinno być minimalne i nigdy nie powinno obejmować danych wrażliwych. W praktyce programiści czasami zapominają o usunięciu rejestrowania debugowania przed wydaniem, co skutkuje tym, że aplikacja zapisuje nazwy użytkowników, tokeny,APIodpowiedzi, a nawet hasła do dziennika, który może odczytać każda inna aplikacja na urządzeniu.

Podczas analizy dynamicznej, przeglądanie logów aplikacji podczas jej użytkowania to szybki i często satysfakcjonujący krok. Dane wrażliwe pojawiające się w logach są mapowane na kategorię M9 z listy OWASP Mobile Top 10: Niezabezpieczone przechowywanie danych.

Dzięki metodologii i technikom analizy możemy teraz przyjrzeć się samym kategoriom podatności. Każda z nich opiera się naOWASPTop 10 aplikacji mobilnych zostało wyjaśnione na przykładach, aby były jak najbardziej konkretne. Potraktuj to zadanie jako punkt odniesienia, do którego możesz wrócić podczas wyzwania w Zadaniu 7 i w przyszłych spotkaniach.

Niezabezpieczone przechowywanie danych
Aplikacje mobilne przechowują dane na urządzeniu z różnych powodów: buforując preferencje użytkownika, zapisując tokeny sesji i przechowując lokalną kopię danych konta. Problem pojawia się, gdy poufne dane są przechowywane w miejscu lub formacie, który umożliwia ich odczyt bez autoryzacji.

Typowe przykłady obejmują przechowywanie danych uwierzytelniających lub tokenów w plikach konfiguracyjnych w postaci zwykłego tekstu, przechowywanie poufnych informacji w lokalnej bazie danych bez szyfrowania, zapisywanie prywatnych danych w pamięci współdzielonej, do której mogą uzyskać dostęp inne aplikacje, a także buforowanie odpowiedzi z interfejsów API zaplecza bez uwzględniania zawartości tych odpowiedzi.

Testerzy szukają niebezpiecznych miejsc przechowywania danych, badając pliki tworzone przez aplikację na urządzeniu, bazy danych, które utrzymuje, oraz lokalizacje, w których zapisuje dane podczas normalnego użytkowania. Jest to zgodne z wytycznymi OWASP M9: Niezabezpieczone przechowywanie danych.

Niewłaściwe użycie platformy
Mobilne systemy operacyjne oferują programistom zestaw funkcji i narzędzi zaprojektowanych w celu zapewnienia bezpieczeństwa aplikacji i ich danych. Niewłaściwe korzystanie z platformy oznacza, że ​​aplikacja albo niewłaściwie wykorzystała te funkcje, albo w ogóle z nich nie skorzystała.

Najczęstszym przykładem są uprawnienia. Aplikacja, która żąda dostępu do kamery, kontaktów, lokalizacji i mikrofonu urządzenia, podczas gdy potrzebuje tylko jednej z tych rzeczy, żąda znacznie większego dostępu, niż potrzebuje. Jeśli ta aplikacja zostanie kiedykolwiek naruszona, atakujący odziedziczy wszystkie przyznane jej uprawnienia. Innym przykładem jest wykorzystywanie funkcji platformy w sposób niezabezpieczony, na przykład przesyłanie poufnych danych między komponentami aplikacji w sposób, który może zostać przechwycony przez inne aplikacje na urządzeniu. Jest to odzwierciedlenie w OWASP M1: Niewłaściwe użycie poświadczeń i M8: Błędna konfiguracja zabezpieczeń.

Niezabezpieczone uwierzytelnianie i zarządzanie sesjami
Luki w uwierzytelnianiu w aplikacjach mobilnych często odzwierciedlają te występujące w aplikacjach internetowych, ale z kilkoma niuansami specyficznymi dla kontekstu mobilnego. Słabe tokeny sesji, które nie wygasają, tokeny przechowywane w niezabezpieczony sposób na urządzeniu, brak ponownego uwierzytelnienia w przypadku wrażliwych działań oraz implementacje uwierzytelniania biometrycznego, które można ominąć – to wszystko częste problemy.

Warto w tym miejscu wspomnieć o omijaniu zabezpieczeń biometrycznych. Niektóre aplikacje wykorzystują kontrole biometryczne, takie jak rozpoznawanie odcisków palców lub twarzy, jako bramkę do wrażliwych funkcji. Jeśli weryfikacja jest implementowana poprzez proste zapytanie systemu operacyjnego, czy dane biometryczne zostały zaakceptowane i zaufanie odpowiedzi bez weryfikacji po stronie serwera, często można ją ominąć w czasie wykonywania za pomocą narzędzi instrumentacyjnych. Jest to odzwierciedlenie standardu OWASP M3: Niezabezpieczone uwierzytelnianie i autoryzacja.

Odsłonięte komponenty aplikacji
Jak omówiliśmy w zadaniach 2 i 4, aplikacje mobilne składają się z komponentów, które można skonfigurować tak, aby były eksportowane, co pozwala innym aplikacjom na urządzeniu na bezpośrednią interakcję z nimi. Gdy komponent przetwarzający poufne dane lub wykonujący czynności wymagające uprawnień zostanie ujawniony bez odpowiednich kontroli dostępu, staje się on powierzchnią ataku.

Przykładem z życia wziętym byłby komponent aplikacji wyświetlający dane konta użytkownika, do którego dostęp ma każda inna aplikacja na urządzeniu. Złośliwa aplikacja zainstalowana obok niego mogłaby wywołać ten komponent bezpośrednio i pobrać dane konta bez konieczności podawania danych uwierzytelniających użytkownika. Jest to odzwierciedlenie w raporcie OWASP M8: Security Misconfiguration (błędna konfiguracja zabezpieczeń).

Niewystarczające zabezpieczenia binarne
Zabezpieczenia binarne to mechanizmy kontroli, które utrudniają inżynierię wsteczną, manipulację lub uruchomienie skompilowanej aplikacji mobilnej w nieautoryzowanym środowisku. Gdy te zabezpieczenia są nieobecne lub słabe, atakujący może zdekompilować aplikację, zrozumieć jej logikę, zmodyfikować jej działanie i ponownie ją spakować.

Do najważniejszych kontroli zabezpieczeń binarnych na standardowej liście kontrolnej testów penetracyjnych aplikacji mobilnych należą:

Zaciemnianie : Czy kod został zaciemniony, aby utrudnić jego odczytanie po dekompilacji?
Wykrywanie manipulacji : Czy aplikacja sprawdza, czy została zmodyfikowana przed uruchomieniem?
Wykrywanie rootowania i jailbreakowania : Czy aplikacja wykrywa, czy działa na urządzeniu z rootowanym lub jailbreakowanym dostępem i odpowiednio reaguje?
Wykrywanie rootowania i jailbreaku to szczególnie standardowy element listy kontrolnej. Urządzenie zrootowane lub jailbreakowane daje atakującemu znacznie większy dostęp do danych i działania aplikacji w czasie rzeczywistym. Aplikacje przetwarzające poufne informacje, takie jak aplikacje bankowe czy medyczne, zazwyczaj wykrywają ten stan i ostrzegają użytkownika lub odmawiają działania. Brak tego sprawdzenia jest sam w sobie istotnym odkryciem. Jest to zgodne z OWASP M7: Niewystarczająca ochrona binarna.

Scenariusz
Pojawiła się informacja o Helix Solutions, średniej wielkości firmie technologicznej, która niedawno udostępniła aktualizację swojego wewnętrznego portalu dla pracowników. Źródło informacji twierdzi, że zespół programistów był pod presją szybkiego udostępnienia aktualizacji i że oszczędzano na bezpieczeństwie. W samych pakietach aplikacji mogły znajdować się poufne dane konfiguracyjne, dane uwierzytelniające i szczegóły usług wewnętrznych.

Zostałeś konsultantem zespołu czerwonego, aby rozdzielić obie aplikacje za pomocąanaliza statycznai dowiedzieć się, co dokładnie zostało pominięte. Do tego zadania udostępniono dwa pakiety: plik APK dla Androida i plik IPA dla iOS, oba zbudowane na bazie tego samego kodu Helix Solutions. W tym przewodniku prześlemy każdy z nich do MobSF, systematycznie przeanalizujemy wyniki i pokażemy dokładnie, gdzie ukrywa się każdy fragment wrażliwych danych.

Organizować coś
Uruchom instancję MobSF dołączoną do zadania 4. Po wdrożeniu MobSF będzie dostępny za pośrednictwem TryHackMeVPNw http://10.130.168.71:8000przeglądarce. W przypadku wersji APK na Androida i iOS IPA masz dwie opcje:

Twój komputer: Kliknij przycisk Pobierz pliki zadań powyżej, aby pobrać oba pliki binarne.
TryHackMe AttackBox (w trakcie realizacji, wkrótce dostępny): Te same pliki binarne zostaną wstępnie przygotowane w /root/Rooms/MobileSecurity/LeakyPackage-1773714002799.
Część 1: Analiza pliku APK dla systemu Android
Krok 1: Przesyłanie do MobSF i zapoznanie się z przeglądem

Otwórz instancję MobSF w przeglądarce. Pierwszą rzeczą, jaką zobaczysz, będzie strona logowania. Zaloguj się przy użyciu domyślnych danych logowania ( mobsf/ mobsf). Po zalogowaniu zobaczysz obszar przesyłania.

Przeciągnij i upuść  LeakyPackage.apkplik na ten plik lub skorzystaj z selektora plików. MobSF natychmiast rozpocznie skanowanie. Czas skanowania zależy od rozmiaru pliku binarnego i zasobów komputera, więc poczekaj kilka minut na zakończenie.

Po zakończeniu skanowania MobSF przekieruje Cię do raportu analizy statycznej. Górna część raportu od razu pokazuje stan bezpieczeństwa aplikacji.

Kilka rzeczy rzuca się w oczy od razu:

Wynik bezpieczeństwa: 40/100, niski wynik sygnalizujący wiele ustaleń
Nazwa aplikacji: Helix Solutions, co potwierdza, że ​​jest to właściwa aplikacja
Nazwa pakietu: com.tryhackme.leakypackage
1 / 2 Wyeksportowane aktywności , co oznacza, że ​​jedna aktywność jest eksportowana i dostępna dla innych aplikacji na urządzeniu, co wkrótce zbadamy
Sekcja Decompiled Code zawiera przyciski umożliwiające przeglądanie pliku AndroidManifest.xml, zdekompilowanego kodu źródłowego Java i kodu bajtowego Smali bezpośrednio w przeglądarce
Krok 2: Uprawnienia

Kliknij Uprawnienia na pasku bocznym po lewej stronie.

Tabela uprawnień zawiera siedem wpisów. Pięć z nich oznaczono jako niebezpieczne na czerwono: ACCESS_FINE_LOCATION,  CAMERA, READ_CONTACTS, READ_EXTERNAL_STORAGEi RECORD_AUDIO. Wewnętrzna aplikacja portalu pracowniczego nie ma uzasadnionego powodu, aby uzyskać dostęp do kamery, mikrofonu, kontaktów ani danych o lokalizacji. To podręcznikowy przykład nadmiernego żądania uprawnień, mapowany na OWASP M8: Security Misconfiguration . 

Krok 3: Analiza manifestu

Kliknij opcję Analiza zabezpieczeń na pasku bocznym po lewej stronie, aby rozwinąć podmenu, a następnie kliknij opcję Analiza manifestu .

MobSF zasygnalizowało pięć problemów. Dwa najważniejsze dla tego dochodzenia to:

Wiersz 2: Debugowanie włączone dla aplikacji [android:debuggable=true] , poziom ważności WYSOKI. Aplikacja z możliwością debugowania umożliwia atakującemu z dostępem fizycznym lub ADB dołączenie debugera, zrzucenie stosu i przechwytywanie wywołań metod w czasie wykonywania. Ta flaga nigdy nie może występować w wersji produkcyjnej.
Wiersz 4: Aktywność (com.tryhackme.leakypackage.AdminPanelActivity) nie jest chroniona [android:exported=true] , poziom zagrożenia: OSTRZEŻENIE. AdminPanelActivityKomponent jest oznaczony jako wyeksportowany bez wymagania uprawnień, co oznacza, że ​​każda aplikacja zainstalowana na tym samym urządzeniu może go uruchomić bezpośrednio za pomocą jawnej intencji, omijając wszelkie uwierzytelnianie, które może wymusić główny przepływ aplikacji.
Aby zobaczyć surowy manifest, wróć do głównej strony skanowania i kliknij opcję Wyświetl plik AndroidManifest.xml w sekcji Dekompilowany kod.

Zdekodowany manifest potwierdza wszystko, co MobSF oznaczył flagą. Linia 13 pokazuje element android:debuggable="true"i . Linia 20 pokazuje brak  atrybutu ograniczającego możliwość uruchomienia. Spójrz na wyeksportowaną aktywność, która nie ma atrybutu uprawnień ograniczającego dostęp. W raporcie pentestu oznacz ten komponent pełną nazwą i zanotuj to.android:allowBackup="true"<application>< activity android:name="com.tryhackme.leakypackage.AdminPanelActivity" android:exported="true" />android: permission

Krok 4: Zakodowane na stałe sekrety w zdekompilowanej Javie

Kliknij opcję Analiza kodu w podmenu Analiza zabezpieczeń.

MobSF opublikował jedno ostrzeżenie: „Pliki mogą zawierać zakodowane na stałe poufne informacje, takie jak nazwy użytkowników, hasła, klucze itp.”. Identyfikuje ono dwa pliki: DatabaseHelper.javai HelixConfig.java. Kliknij HelixConfig.javalink w kolumnie PLIKI.

To zakodowany na stałe klucz API przechowywany bezpośrednio w kodzie źródłowym aplikacji. Po udostępnieniu pliku APK każdy użytkownik może go zdekompilować i wyodrębnić klucz za pomocą darmowych narzędzi, takich jak jadx lub apktool, w niecałą minutę. To jest OWASP M1: Niewłaściwe użycie poświadczeń . Zwróć uwagę na wiersz 5; w rzeczywistym zdarzeniu to właśnie tego rodzaju wrażliwe dane wyodrębniłbyś i uwzględnił w raporcie. Czy potrafisz zidentyfikować, o co chodzi?

Teraz wróć i kliknij DatabaseHelper.javalink.

Hasło roota do produkcyjnej bazy danych zostało zakodowane na stałe w kodzie źródłowym aplikacji. W połączeniu ze stałymi DB_HOSTi DB_NAMEwidocznymi w wierszach 5 i 6, atakujący ma wszystko, czego potrzebuje, aby spróbować nawiązać bezpośrednie połączenie z bazą danych zaplecza. Rozważmy wpływ informacji z wiersza 7 oraz szczegółów połączenia widocznych w wierszach 5 i 6. Co programista nieumyślnie ujawnił i co atakujący mógłby z tym zrobić?

Część 2: Analiza IPA dla iOS
Krok 5: Przesłanie pliku IPA i zapoznanie się z przeglądem

Wróć na stronę główną MobSF i prześlij LeakyPackage.ipaplik. Skanowanie iOS przechodzi przez inny proces analityczny niż skanowanie Androida, ale generuje porównywalny raport.

Podsumowanie potwierdza szczegóły aplikacji:

Nazwa aplikacji: LeakyPackage Identyfikator : com.tryhackme.LeakyPackage
Ocena bezpieczeństwa: 45/100
Sekcja Decompiled Assets zawiera trzy przyciski: Wyświetl Info.plist , Wyświetl zrzut klasy i Pobierz IPA
Krok 6: Bezpieczeństwo transportu aplikacji w pliku Info.plist

Kliknij „View Info.plist” w sekcji „Decompiled Assets”. Otworzy się okno modalne z pełną zawartością pliku aplikacji Info.plist.

Przewiń listę, aż dojdziesz do NSAppTransportSecuritywpisu w słowniku. Znajdziesz w nim:

<key>NSAllowsArbitraryLoads</key>
<true/>
Ten pojedynczy wpis całkowicie wyłącza funkcję App Transport Security (ATS) dla aplikacji. Po wyłączeniu ATS aplikacja może przesyłać dane przez niezaszyfrowane połączenia HTTP do dowolnego serwera bez blokowania ich przez system operacyjny. Jest to powiązane z OWASP M5: Insecure Communication i M8: Security Misconfiguration . W słowniku NSAppTransportSecurity zidentyfikuj klucz, który został ustawiony na wartość true. To ustawienie odpowiada za wyłączenie ATS i do niego należy się odwołać podczas dokumentowania tego odkrycia.

Aby uzyskać dodatkowe potwierdzenie, zamknij okno modalne i kliknij opcję Bezpieczeństwo transportu w obszarze Analiza bezpieczeństwa na pasku bocznym po lewej stronie.

MobSF przedstawia to bezpośrednio jako odkrycie o WYSOKIM stopniu zagrożenia: „App Transport Security AllowsArbitraryLoads jest dozwolone” wraz ze szczegółowym opisem, dlaczego jest to niebezpieczne.

Krok 7: Dane wrażliwe na liście łączonych nieruchomości

Przewiń w dół do sekcji Rekonesans w raporcie iOS lub kliknij Pliki na pasku bocznym po lewej stronie.

W sekcji „Możliwe zakodowane na stałe sekrety” MobSF automatycznie przeanalizował wszystkie dołączone .plistpliki i ujawnił ich pary klucz-wartość. Jeden wpis od razu rzuca się w oczy:

Ta wartość pochodzi z internal_config.plistpliku listy właściwości dołączonego bezpośrednio do pliku IPA. Możesz to sprawdzić, przewijając w dół do sekcji Pliki , gdzie  LeakyPackage.app/internal_config.plistznajduje się na liście plików.

Żadna aplikacja dostarczana użytkownikom końcowym nie powinna zawierać wewnętrznego tajnego tokenu. Programista pozostawił w pakiecie produkcyjnym prawdopodobnie wewnętrzny tajny token uwierzytelniania lub podpisu. To jest OWASP M9: Niezabezpieczone przechowywanie danych . Przeanalizuj pary klucz-wartość uzyskane z [brakuje kontekstu] internal_config.plist. Jedna z nich wyraźnie wyróżnia się jako poufny token wewnętrzny, który nigdy nie powinien być dołączany do wersji produkcyjnej. Jaką wartość pozostawił programista?

W tej sali omówiliśmy podstawy testów penetracyjnych aplikacji mobilnych od podstaw. Zaczęliśmy od zrozumienia struktury aplikacji mobilnych i tego, co znajduje się w pakiecie, a następnie przeszliśmy przez przejrzystą metodologię testowania opartą na…OWASPTop 10 aplikacji mobilnych. Omówiliśmy analiz statycznaszczegółowo, wykorzystując MobSF wraz z technikami manualnymi do badania aplikacji bez jej uruchamiania, i omówiliśmy koncepcje, które się za tym kryjąanaliza dynamiczna: przechwytywanie ruchu, przypinanie SSL, instrumentacja środowiska wykonawczego i niebezpieczne logowanie. Następnie zebraliśmy to wszystko, przechodząc przez najczęstsze kategorie luk w zabezpieczeniach, z którymi tester spotyka się podczas rzeczywistej interakcji mobilnej, a następnie zastosowaliśmy te umiejętności analizy statycznej w praktycznym wyzwaniu w stylu CTF w aplikacji Helix Solutions.

Czego się nauczyliśmy
Aplikacje mobilne to ustrukturyzowane pakiety zawierające plik binarny, manifest lub plik konfiguracyjny, zasoby i aktywa, a zrozumienie tej struktury stanowi podstawę skutecznego testowania
Mobilny test penetracyjny składa się z czterech faz: rozpoznania, analizy statycznej, analizy dynamicznej i raportowania
OWASP Mobile Top 10 to branżowy standardowy zestaw kryteriów kategoryzacji i komunikacji wyników dotyczących aplikacji mobilnych
Analiza statyczna obejmuje rozpakowanie pakietu aplikacji, odczytanie jego manifestu lub Info.plist, wyszukiwanie zakodowanych na stałe tajnych informacji i korzystanie z automatycznych narzędzi, takich jak MobSF, w celu wykrywania typowych problemów w systemach Android i iOS
Analiza dynamiczna obejmuje przechwytywanie ruchu sieciowego, obejście przypinania SSL, korzystanie z instrumentów środowiska wykonawczego i przeglądanie dzienników aplikacji pod kątem wycieku poufnych danych
Do najczęstszych kategorii luk w zabezpieczeniach aplikacji mobilnych należą: niebezpieczne przechowywanie danych, niewłaściwe korzystanie z platformy, niebezpieczne uwierzytelnianie, odsłonięte komponenty i niewystarczające zabezpieczenia binarne, w tym brak wykrywania rootowania i jailbreaku
Techniki analizy statycznej można stosować w praktyce, aby znaleźć rzeczywiste ustalenia w pakiecie aplikacji mobilnej
Co dalej?
Ta sala to pierwszy krok na szerszej ścieżce nauki bezpieczeństwa urządzeń mobilnych. Jeśli chcesz zgłębić temat, oto kilka dobrych kroków:

Analiza złośliwego oprogramowania mobilnego w TryHackMe, obejmująca statyczną analizę złośliwych aplikacji na Androida przy użyciu MobSF
Przewodnik po testowaniu bezpieczeństwa urządzeń mobilnych OWASP(otwiera się w nowej karcie) jest najbardziej kompleksowym, darmowym źródłem informacji na temat testowania bezpieczeństwa aplikacji mobilnych
Bądźcie na bieżąco z kolejnymi sesjami na TryHackMe, w których szczegółowo omówimy systemy Android i iOS. Będziemy mogli zapoznać się z narzędziami i technikami przedstawionymi koncepcyjnie w tej sali.
