---

Cyberbezpieczeństwo to poważny biznes we współczesnym świecie. Ataki hakerskie, o których słyszymy w gazetach, wynikają z wykorzystywania luk w zabezpieczeniach. W tym pomieszczeniu wyjaśnimy dokładnie, czym jest luka w zabezpieczeniach, jakie są jej rodzaje i jak możemy je wykorzystać, aby odnieść sukces w naszych testach penetracyjnych.

Ogromną częścią testów penetracyjnych jest znajomość umiejętności i zasobów niezbędnych do radzenia sobie z każdą sytuacją. W tej sali zapoznasz się z zasobami niezbędnymi do badania luk w zabezpieczeniach, a konkretnie z:

- Jakie są luki w zabezpieczeniach
- Dlaczego warto się o nich dowiedzieć
- Jak oceniane są luki w zabezpieczeniach?
- Bazy danych do badań nad podatnościami
- Pokaz pokazujący, w jaki sposób badania nad podatnością są wykorzystywane w działaniach ACKme

Luka w cyberbezpieczeństwie jest definiowana jako słabość lub wada w projekcie, implementacji lub działaniu systemu lub aplikacji. Atakujący może wykorzystać te słabości, aby uzyskać dostęp do nieautoryzowanych informacji lub wykonać nieautoryzowane działania. Termin „luka” jest definiowany na wiele sposobów przez organizacje zajmujące się cyberbezpieczeństwem. Różnice między nimi są jednak minimalne.

Przykładowo NIST definiuje lukę w zabezpieczeniach jako „słabość w systemie informatycznym, procedurach bezpieczeństwa systemu, kontrolach wewnętrznych lub implementacji, która może zostać wykorzystana lub uruchomiona przez źródło zagrożenia”.

Podatności mogą mieć swoje źródło w wielu czynnikach, m.in. w złym zaprojektowaniu aplikacji lub przeoczeniu przez użytkownika zamierzonych działań.

Omówimy różne rodzaje luk w zabezpieczeniach w następnej sali. Na razie jednak powinniśmy wiedzieć, że istnieje prawdopodobnie pięć głównych kategorii luk w zabezpieczeniach:

|   |   |
|---|---|
|**Wrażliwość**|**Opis**|
|System operacyjny|Tego typu luki występują w systemach operacyjnych i często skutkują zwiększeniem uprawnień.|
|(Błędna) konfiguracja oparta|Tego typu luki wynikają z nieprawidłowo skonfigurowanej aplikacji lub usługi, na przykład strony internetowej ujawniającej dane klienta.|
|Słabe lub domyślne dane uwierzytelniające|Aplikacje i usługi z elementem uwierzytelniania będą miały domyślne dane uwierzytelniające po zainstalowaniu. Na przykład, panel administratora może mieć nazwę użytkownika i hasło „admin”. Są one łatwe do odgadnięcia przez atakującego.|
|Logika aplikacji|Te luki wynikają ze źle zaprojektowanych aplikacji, na przykład źle wdrożonych mechanizmów uwierzytelniania, które mogą umożliwić atakującemu podszywanie się pod użytkownika.|
|Czynnik ludzki|Luki w zabezpieczeniach typu „human-factor” to luki, które wykorzystują ludzkie zachowania. Na przykład wiadomości e-mail typu phishing mają na celu oszukanie ludzi i przekonanie ich, że są legalne.|

Jako badacz cyberbezpieczeństwa będziesz oceniać aplikacje i systemy, wykorzystując luki w zabezpieczeniach w codziennym życiu, dlatego ważne jest, aby zapoznać się z procesem odkrywania i wykorzystywania luk.

## Ocena luk w zabezpieczeniach CVSS i VPR

Zarządzanie podatnościami to proces oceny, kategoryzacji i ostatecznego usuwania zagrożeń (podatności), z którymi mierzy się organizacja.

Można twierdzić, że nie da się załatać i naprawić każdej luki w zabezpieczeniach sieci lub systemu komputerowego, a czasami jest to marnotrawstwo zasobów.

W końcu tylko około 2% luk w zabezpieczeniach kończy się wykorzystaniem ( [Kenna security., 2020](https://www.kennasecurity.com/resources/prioritization-to-prediction-report/) ).  Zamiast tego chodzi o wyeliminowanie najgroźniejszych luk i zmniejszenie prawdopodobieństwa wykorzystania wektora ataku do wykorzystania systemu.

W tym miejscu pojawia się punktacja podatności. Punktacja podatności odgrywa kluczową rolę w zarządzaniu podatnościami i służy do określenia potencjalnego ryzyka i wpływu, jaki luka może mieć na sieć lub system komputerowy. Na przykład popularny system oceny podatności ( CVSS ) przyznaje punkty podatności na podstawie jej cech, dostępności i powtarzalności.

Oczywiście, jak zawsze w świecie IT, nigdy nie ma tylko jednego modelu ramowego ani jednego proponowanego pomysłu. Przyjrzyjmy się dwóm najpopularniejszym modelom ramowym i przeanalizujmy, czym się różnią.

**Wspólny system oceny podatności**

Wprowadzony po raz pierwszy w 2005 roku, Common Vulnerability Scoring System ( #CVSS ) to bardzo popularny system oceny podatności, który doczekał się trzech głównych iteracji. Obecnie, w wersji CVSS 3.1 (wersja 4.0 jest obecnie w fazie roboczej), wynik jest zasadniczo ustalany na podstawie kilku z poniższych czynników (ale nie tylko):

  1. Jak łatwo jest wykorzystać tę lukę?

  2. Czy istnieją exploity na to?

  3. W jaki sposób ta luka w zabezpieczeniach wpływa na działalność triady CIA ?

W rzeczywistości istnieje tak wiele zmiennych, że do obliczenia wyniku w tym systemie konieczne jest użycie kalkulatora [.](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) Luka otrzymuje klasyfikację (w skali od pięciu do pięciu) w zależności od przyznanej jej punktacji. W poniższej tabeli umieściłem Skalę Oceny Jakościowej Wagi (Qualitation Severity Rating Scale) i jej zakresy punktacji. 

|   |   |
|---|---|
|**Ocena**|**Wynik**|
|Nic|0|
|Niski|0,1 - 3,9|
|Średni|4,0 - 6,9|
|Wysoki|7,0 - 8,9|
|Krytyczny|9,0 - 10,0|

Jednak CVSS nie jest rozwiązaniem idealnym. Przeanalizujmy niektóre zalety i wady CVSS w poniższej tabeli:

|   |   |
|---|---|
|**Zalety CVSS**|**Wady CVSS**|
|CVSS istnieje już od dawna.|System CVSS nigdy nie został zaprojektowany z myślą o pomocy w ustalaniu priorytetów luk w zabezpieczeniach, a jedynie o przypisywaniu wartości stopnia ważności.|
|CVSS cieszy się popularnością w organizacjach.|CVSS intensywnie analizuje luki w zabezpieczeniach pod kątem dostępności exploita. Jednak tylko 20% wszystkich luk ma dostępną możliwość wykorzystania exploita ( [Teneable, 2020](https://www.tenable.com/research) ).|
|CVSS to bezpłatne ramy, które można przyjąć i które są zalecane przez takie organizacje, jak NIST .|Ocena luk w zabezpieczeniach rzadko ulega zmianie po przeprowadzeniu oceny, mimo że mogą zostać odkryte nowe rozwiązania, takie jak exploity.|

**Ocena priorytetu podatności ( VPR )**

Struktura VPR to znacznie nowocześniejsze ramy zarządzania podatnościami, opracowane przez Tenable, dostawcę rozwiązań branżowych w tym zakresie. Uważa się, że ramy te są oparte na ryzyku, co oznacza, że ​​podatnościom przypisuje się punkty, koncentrując się na ryzyku, jakie stwarzają dla samej organizacji, a nie na czynnikach takich jak wpływ (jak w przypadku CVSS ).

W przeciwieństwie do CVSS , punktacja VPR uwzględnia istotność podatności. Na przykład, ryzyko związane z podatnością nie jest brane pod uwagę, jeśli nie dotyczy ona organizacji (tj. nie korzysta ona z oprogramowania, które jest podatne). Punktacja VPR jest również bardzo dynamiczna, a ryzyko, jakie może stwarzać podatność, może zmieniać się niemal codziennie wraz z jej starzeniem się.

VPR używa podobnego zakresu punktacji jak CVSS , który również umieściłem w poniższej tabeli. Dwie istotne różnice to brak kategorii _„Brak/Informacyjne”_ w VPR oraz fakt, że VPR używa innej metody punktacji, co oznacza, że ​​ta sama luka w zabezpieczeniach będzie miała inną punktację w VPR niż w CVSS .

|   |   |
|---|---|
|**Ocena**|**Wynik**|
|Niski|0,0 - 3,9|
|Średni|4,0 - 6,9|
|Wysoki|7,0 - 8,9|
|Krytyczny|9,0 - 10,0|

Podsumujmy niektóre zalety i wady korzystania z infrastruktury VPR w poniższej tabeli.

|   |   |
|---|---|
|**Zalety VPR**|**Wady VPR**|
|VPR to nowoczesna i praktyczna technologia.|VPR nie jest rozwiązaniem typu open source, w przeciwieństwie do niektórych innych struktur zarządzania lukami w zabezpieczeniach.|
|VPR bierze pod uwagę ponad 150 czynników przy obliczaniu ryzyka.|Technologia VPR może być wdrożona jedynie poza platformą komercyjną.|
|VPR opiera się na ocenie ryzyka i jest wykorzystywany przez organizacje w celu ustalenia priorytetów łatania luk w zabezpieczeniach.|VPR nie bierze pod uwagę triady CIA w takim stopniu jak CVSS ; oznacza to, że ryzyko naruszenia poufności, integralności i dostępności danych nie odgrywa dużej roli w ocenie luk w zabezpieczeniach podczas korzystania z VPR .|
|Punktacja nie jest ostateczna i jest bardzo dynamiczna, co oznacza, że ​​priorytet, jaki należy nadać danej luce w zabezpieczeniach, może się zmieniać w miarę starzenia się tej luki.|_Celowo pozostawiono puste._|

## Badanie luk w zabezpieczeniach

W swojej podróży po świecie cyberbezpieczeństwa często natkniesz się na mnóstwo różnych aplikacji i usług. Na przykład, CMS , choć wszystkie mają ten sam cel, często różnią się konstrukcją i sposobem działania (a co za tym idzie, potencjalnie różnymi podatnościami).

Na szczęście w internecie dostępne są zasoby, które śledzą luki w zabezpieczeniach wszelkiego rodzaju oprogramowania, systemów operacyjnych i nie tylko! W tej sali zaprezentujemy dwie bazy danych, z których możemy skorzystać, aby wyszukać istniejące luki w zabezpieczeniach aplikacji odkrytych podczas naszej przygody z bezpieczeństwem informacji, a konkretnie następujące strony internetowe:

1. [NVD (Narodowa Baza Danych o Podatnościach)](https://nvd.nist.gov/vuln)

2. [Exploit-DB](http://exploit-db.com/)

Zanim zagłębimy się w te dwa źródła, upewnijmy się, że rozumiemy podobnie pewne podstawowe pojęcia:

|   |   |
|---|---|
|**Termin**|**Definicja**|
|Wrażliwość|Podatność definiuje się jako słabość lub wadę w projekcie, implementacji lub zachowaniu systemu lub aplikacji.|
|Wykorzystać|Exploit to działanie lub zachowanie wykorzystujące lukę w zabezpieczeniach systemu lub aplikacji.|
|Dowód koncepcji ( PoC )|PoC to technika lub narzędzie często demonstrujące wykorzystanie luk w zabezpieczeniach.|

## NVD – Krajowa Baza Danych o Podatnościach

National Vulnerability Database to strona internetowa, która zawiera listę wszystkich publicznie sklasyfikowanych luk w zabezpieczeniach. W cyberbezpieczeństwie luki w zabezpieczeniach są klasyfikowane jako „ **C**ommon **Vulnerabilities** and **Exposures** ” ( w skrócie CVE ).

Te CVE mają formatowanie `CVE-YEAR-IDNUMBER`. Na przykład luka, którą wykorzystywał słynny malware WannaCry, to`CVE-2017-0144.`

NVD pozwala przeglądać wszystkie potwierdzone CVE, korzystając z filtrów według kategorii i miesiąca zgłoszenia. Na przykład, gdy jest już trzeci dzień sierpnia, do bazy danych zgłoszono już 223 nowe CVE.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de96d9ca744773ea7ef8c00/room-content/aa86c1cce478d6c357f5507d927c9e88.png)

Choć witryna ta pomaga śledzić nowe luki w zabezpieczeniach, nie sprawdza się najlepiej przy wyszukiwaniu luk w zabezpieczeniach konkretnych aplikacji lub scenariuszy.

## Exploit-DB

[Exploit-DB](https://www.exploit-db.com/) to zasób, który my, hakerzy, uznamy za znacznie bardziej przydatny podczas oceny. Exploit-DB przechowuje exploity dla oprogramowania i aplikacji, pod nazwą, autorem i wersją oprogramowania lub aplikacji.

Za pomocą Exploit-DB możemy wyszukiwać fragmenty kodu (znane jako Proof of Concepts) służące do wykorzystywania konkretnych luk w zabezpieczeniach.

![](https://assets.tryhackme.com/additional/vulnerability-module/vulnerabilities101/exploitdb1.png)

## Przykłady znalezienia luki w zabezpieczeniach

W tym zadaniu pokażę proces znajdowania jednej niewielkiej luki w zabezpieczeniach, połączony z badaniami baz danych luk, co ostatecznie prowadzi do odkrycia znacznie bardziej wartościowej luki i jej wykorzystania.

Podczas oceny często łączy się wiele luk w zabezpieczeniach, aby uzyskać wyniki. Na przykład, w tym zadaniu wykorzystamy lukę w zabezpieczeniach „ **Ujawnienie wersji”,** aby dowiedzieć się, jaka jest wersja aplikacji. Dzięki tej wersji możemy następnie użyć [Exploit-DB](https://www.exploit-db.com/) do wyszukania exploitów, które działają z tą konkretną wersją. 

Aplikacje i oprogramowanie zazwyczaj mają numer wersji. Informacje te są zazwyczaj pozostawiane z dobrymi intencjami; na przykład autor może obsługiwać wiele wersji oprogramowania itp. Czasami jednak są pozostawiane nieumyślnie.

Na przykład na poniższym zrzucie ekranu możemy zobaczyć, że nazwa i numer wersji tej aplikacji to „ **Apache Tomcat 9.0.17** ”

![](https://assets.tryhackme.com/additional/vulnerability-module/vulnerabilities101/tomcat1.png)

Mając te informacje, skorzystajmy z filtra wyszukiwania w Exploit-DB, aby znaleźć wszelkie exploity, które mogą dotyczyć „ **Apache Tomcat 9.0.17** ”.

![](https://assets.tryhackme.com/additional/vulnerability-module/vulnerabilities101/tomcat2.png)

Świetnie! Po przeszukaniu bazy danych Exploit-DB znaleźliśmy łącznie pięć exploitów, które mogą nam się przydać w tej konkretnej wersji aplikacji.
