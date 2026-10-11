---

Ludzie zawsze poszukują prostszych i bardziej efektywnych sposobów wykonywania zadań. Kiedy zaczęliśmy programować i tworzyć oprogramowanie, szukaliśmy sposobów na automatyzację niektórych zadań. Obecnie automatyzacja jest silnie zakorzeniona w cyklu życia oprogramowania (SDLC) IDevOpsProcesy. Chociaż jest to niezwykle korzystne dla produkcji, umożliwiając szybszy rozwój i wdrażanie, wprowadza jednak nowe zagrożenia bezpieczeństwa. Gdy procesy te są ręczne, atakujący musiałby przejąć dane uwierzytelniające lub stację roboczą osoby, która wykonała dany proces. Jednak dzięki automatyzacji atakujący może teraz zaatakować sam potok.

Cele edukacyjne

W tej sali poznasz następujące koncepcje:

- Wprowadzenie doDevOpsrurociąg
- Wprowadzenie doDevOpsnarzędzia i automatyzacja
- Wprowadzenie do zasad bezpieczeństwa dlaDevOpsrurociąg  

To jest sala wprowadzająca. W związku z tym większość tych koncepcji zostanie przedstawiona tylko w tej sali i omówiona bardziej szczegółowo w dalszej części.odpoczynekpomieszczeń w tym module.

Zanim zaczniemy zgłębiać temat bezpieczeństwa automatyzacji, powinniśmy zacząć od zdefiniowania potoku i pokazania, gdzie może odbywać się automatyzacja. Poniższy diagram pokazuje, jak może wyglądać typowy potok, a także oprogramowanie, które można wykorzystać w tym celu:

![Schemat rurociągu](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/5bf9574f4b8f6bc202123c9476650e58.png)  

Przyjrzymy się każdemu z tych elementów, ich typowym narzędziom, wprowadzeniu do ich bezpieczeństwa oraz studium przypadku, pokazującym, co może się stać, gdy zabezpieczenia zawiodą. Każdy z tych komponentów zostanie szczegółowo omówiony w kolejnych salach tego modułu.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/3804e1b22987fc90c27d19e511ead12e.png)  

Przyjrzyjmy się kodowi źródłowemu i kontroli wersji. To początek naszego procesu. Potrzebujemy miejsca, w którym będziemy mogli przechowywać nasz kod. Co więcej, często chcemy przechowywać kilka wersji naszego kodu, ponieważ stale go ulepszamy i dodajemy nowe funkcje.

Przechowywanie kodu źródłowego

Musimy wziąć pod uwagę kilka kwestii, decydując, gdzie przechowywać nasz kod:

- W jaki sposób możemy kontrolować dostęp do naszego kodu źródłowego?
- Jak możemy mieć pewność, że wprowadzane zmiany będą śledzone?
- Czy możemy zintegrować nasz system przechowywania kodu źródłowego z narzędziami programistycznymi?
- Czy możemy przechowywać i aktywnie wykorzystywać wiele różnych wersji naszego kodu źródłowego?
- Czy powinniśmy hostować nasz kod źródłowy wewnętrznie, czy możemy zlecić to zadanie zewnętrznej firmie?  

Odpowiedzi na te pytania pomogą nam wybrać właściwe rozwiązanie do przechowywania kodu źródłowego dla naszego projektu.  

Kontrola wersji

Potrzebujemy kontroli wersji z dwóch głównych powodów:

- Często integrujemy nowe funkcje w naszym oprogramowaniu. Nowoczesne metodyki rozwoju oprogramowania, takie jak Agile, oznaczają, że stale aktualizujemy nasz kod. Aby mieć wszystkie te aktualizacje pod kontrolą, potrzebujemy systemu kontroli wersji.
- Nad kodem pracuje cały zespół programistów, a nie tylko jeden programista. Aby zapewnić integrację zmian wprowadzanych przez wielu programistów, niezbędna jest kontrola wersji.

Kontrola wersji pozwala nam przechowywać wiele wersji kodu. Może to być konkretna wersja, nad którą pracuje każdy programista, ale mogą to być również zupełnie różne wersje naszej aplikacji, w tym wersje podrzędne i główne.

Narzędzia powszechne

Dwa najpopularniejsze systemy przechowywania kodu źródłowego i kontroli wersji toGiti SubVersion (SVN).GitSVN to rozproszone narzędzie kontroli wersji, co oznacza, że ​​każdy współautor będzie miał własną kopię kodu źródłowego. Z drugiej strony, SVN to scentralizowane narzędzie kontroli wersji, co oznacza, że ​​kontrola nad repozytorium jest zarządzana centralnie.

GitHub jest zdecydowanie największym dostawcą hostingu internetowego do tworzenia oprogramowania i kontroli wersji, wykorzystującymGitMożesz utworzyć konto GitHub i używać go do zarządzania repozytoriami kodu źródłowego (repo). Możesz jednak również hostować własnegitserwer za pomocą oprogramowania takiego jak Gitlab. W przypadku SVN dwa najpopularniejsze narzędzia to TortoiseSVN iApaczSVN.

Należy jednak zauważyć, że rozwiązania do przechowywania kodu źródłowego, takie jak Gitlab, oferują znacznie więcej funkcji niż tylko przechowywanie i kontrola wersji. Obecnie narzędzia te można wykorzystać niemal w całym procesie!

Zagadnienia bezpieczeństwa

Nasz kod źródłowy to często nasz sekret. Dlatego dbamy o to, aby nie został ujawniony. Właśnie dlatego uwierzytelnianie i kontrola dostępu do naszego kodu źródłowego są tak ważne. Chcemy również mieć pewność, że zmiany i aktualizacje są odpowiednio śledzone, co pozwoli nam zawsze wrócić do poprzedniej wersji, jeśli coś się wydarzy.

Musimy jednak również zachować ostrożność w kwestii tego, co przechowujemy w ramach naszego kodu źródłowego. Kod źródłowy nie może być całkowicie tajny, ponieważ programiści potrzebują do niego dostępu. W związku z tym należy uważać, aby nie mylić przechowywania kodu źródłowego z zarządzaniem tajnymi danymi. Musimy upewnić się, że nie przechowujemy w kodzie źródłowym tajnych danych, takich jak ciągi połączeń z bazą danych i dane uwierzytelniające. Ponieważ przechowujemy wszystkie wersje kodu źródłowego, nawet jeśli usuniemy tajne dane w nowszej wersji, nadal będą one widoczne w poprzednich wersjach.

Studium przypadku:GitNigdy nie zapomina

Jak wspomniano wcześniej, kontrola wersji może się dla nas źle skończyć, jeśli popełnimy błąd. Jest to częsty problem podczas korzystania z narzędzi kontroli wersji, takich jakGit. Jest takie powiedzenie: _„Gitnigdy nie zapomina”_ . Kod jest „zaangażowany” wGitrepozytorium. Kiedy to się stanie,GitOkreśla zmiany wprowadzone w plikach i tworzy nową wersję na ich podstawie. Każdy użytkownik z dostępem do repozytorium może przeglądać historię zatwierdzeń i wprowadzonych zmian.

Często zdarza się, że programista przypadkowo zatwierdzi tajne dane, takie jak dane uwierzytelniające lub ciągi połączeń z bazą danych,Gitrepozytorium. Zdając sobie sprawę ze swojego błędu, usuwają sekrety i tworzą kolejne zatwierdzenie. Jednak repozytorium będzie teraz zawierało oba zatwierdzenia. Jeśli atakujący uzyska dostęp do repozytorium, może użyć narzędzia takiego jak [GittyLeaks.(otwiera się w nowej karcie)](https://github.com/kootenpv/gittyleaks), które skanowałyby zatwierdzenia w poszukiwaniu poufnych informacji. Nawet jeśli te informacje nie istnieją już w bieżącej wersji, narzędzia te mogą przeskanować wszystkie poprzednie wersje i odkryć te sekrety.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/05428b2c1ae49738813c1644df3a31a3.png)  

Porozmawiajmy o zależnościach. Chociaż może się wydawać, że podczas programowania piszemy mnóstwo kodu, prawda jest taka, że ​​to tylko wierzchołek góry lodowej. O ile nie kodujesz w systemie binarnym, prawdopodobnie piszesz tylko ułamek faktycznego kodu. Dzieje się tak, ponieważ znaczna część kodu została już napisana w formie bibliotek i zestawów SDK (Software Development Kit). Nawet zmienne takie jak String w aplikacji mają za sobą całą bibliotekę! Zarządzanie tymi zależnościami jest kluczowym elementem procesu.  

Zależności zewnętrzne i wewnętrzne

Zależności zewnętrzne to publicznie dostępne biblioteki i zestawy SDK. Są one hostowane w zewnętrznych menedżerach zależności, takich jak PyPi dla Pythona, NuGet dla .NET i Gems dla bibliotek Ruby. Zależności wewnętrzne to biblioteki i zestawy SDK, które organizacja opracowuje i utrzymuje wewnętrznie. Na przykład organizacja może opracować bibliotekę uwierzytelniania. Biblioteka ta może być następnie wykorzystywana we wszystkich aplikacjach tworzonych przez organizację.

Istnieją różne obawy dotyczące bezpieczeństwa zależności wewnętrznych i zewnętrznych:

|   |   |
|---|---|
|Wewnętrzny|Zewnętrzny|
|Biblioteki często stają się przestarzałym oprogramowaniem, ponieważ nie są już aktualizowane lub pierwotny twórca opuścił firmę.|Ponieważ nie mamy pełnej kontroli nad zależnościami, musimy zachować należytą staranność, aby upewnić się, że biblioteka jest bezpieczna.|
|Za bezpieczeństwo menedżera pakietów w przypadku bibliotek wewnętrznych odpowiadamy my.|Jeśli menedżer pakietów lub sieć dystrybucji treści (CDN) zostaną naruszone, może to doprowadzić do ataku na łańcuch dostaw.|
|Luka w zabezpieczeniach wewnętrznej biblioteki może mieć wpływ na wiele naszych aplikacji, ponieważ jest używana we wszystkich z nich.|Atakujący mogą badać biblioteki zewnętrzne w celu wykrycia luk typu 0-day. Znalezienie takiej luki może doprowadzić do jednoczesnego ataku na kilka organizacji.|

Narzędzia powszechne

Menedżer zależności, zwany również menedżerem pakietów, jest wymagany do zarządzania bibliotekami i zestawami SDK. Jak wspomniano wcześniej, do obsługi zależności zewnętrznych używane są narzędzia takie jak PyPi, NuGet i Gems. Zarządzanie zależnościami wewnętrznymi jest nieco bardziej skomplikowane. W tym przypadku możemy użyć narzędzi takich jak JFrog Artifactory lub Azure Artifacts.

Zagadnienia bezpieczeństwa

Niektóre kwestie bezpieczeństwa zostały już wcześniej omówione. Jednak głównym problemem bezpieczeństwa jest to, że zależności to kod poza naszą kontrolą. Szczególnie w dzisiejszych czasach, gdzie używa się tak wielu różnych zależności, niezwykle trudno jest je śledzić. Jeśli w tych zależnościach występują jakiekolwiek luki, może to prowadzić do luk w zabezpieczeniach naszej aplikacji.

Studium przypadku: Log4Shell

W 2021 roku odkryto lukę typu 0-day w zależności Log4j o nazwie Log4Shell. Log4j to narzędzie do logowania oparte na Javie. Jest częściąApaczUsługi wyrębowe, projektApaczSoftware Foundation. Luka może umożliwić nieuwierzytelnionemu atakującemu zdalne wykonanie kodu w systemie korzystającym z rejestratora. Prawdziwy problem? Ta niewielka zależność była wykorzystywana niemal wszędzie, jak pokazuje ten [kod XKCD.(otwiera się w nowej karcie)](https://xkcd.com/2347/)rysunek:

![Zależności](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/fc00c5498dde8630a9b4e5f4ebcc308d.png)  

To nie jest przesada. Zajrzyj [tutaj.(otwiera się w nowej karcie)](https://github.com/cisagov/log4j-affected-db/tree/develop/software_lists)Aby sprawdzić, ile różnych produktów było podatnych na ataki, ponieważ korzystały z tej zależności. Lista stała się tak długa, że ​​trzeba było ją podzielić alfabetycznie. To pokazuje, jaki wpływ może mieć odkrycie luki w zabezpieczeniach zależności.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/d532d7168eaa7553b54464a6736f42fd.png)  

Przyjrzyjmy się bliżej testowaniu automatycznemu. W przeszłości testowanie było dość żmudnym i manualnym procesem. Tester musiał ręcznie uruchamiać i dokumentować każdy przypadek testowy, mając nadzieję, że pokrycie jest wystarczające, aby zapewnić działanie aplikacji lub usługi oraz jej stabilność. Jednak w dzisiejszych czasachrurociągi, testy automatyczne mogą wykonać znaczną część tego zadania.

Testowanie jednostkowe

Mówiąc o testowaniu automatycznym w potoku, jest to pierwszy rodzaj testowania, z którym większość programistów i inżynierów oprogramowania ma styczność. Test jednostkowy to przypadek testowy dla niewielkiej części aplikacji lub usługi. Celem jest przetestowanie aplikacji w mniejszych fragmentach, aby upewnić się, że wszystkie funkcjonalności działają prawidłowo.

W nowoczesnymrurociągiTestowanie jednostkowe może służyć jako bramka jakości. Przypadki testowe można zintegrować z procesem ciągłej integracji i ciągłego wdrażania (CI/płyta CD) część potoku, gdzie kompilacja zostanie zatrzymana, jeśli te przypadki testowe się nie powiodą. Jednak testy jednostkowe zazwyczaj koncentrują się na funkcjonalności, a nie na bezpieczeństwie.

Testowanie integracyjne

Inną powszechną metodą testowania są testy integracyjne. Podczas gdy testy jednostkowe koncentrują się na małych fragmentach aplikacji, testy integracyjne koncentrują się na tym, jak te małe fragmenty ze sobą współpracują. Podobnie jak testy jednostkowe, testy będą przeprowadzane dla każdej integracji i mogą być również zintegrowane z…CI/płyta CDczęść potoku. Podzbiorem testów integracyjnych są testy regresyjne, których celem jest zapewnienie, że nowe funkcje nie wpłyną negatywnie na istniejące funkcje i funkcjonalności. Jednak, podobnie jak testy jednostkowe, testy integracyjne, w tym testy regresyjne, zazwyczaj nie są przeprowadzane w celach bezpieczeństwa.  

Testowanie bezpieczeństwa

Jeśli zatem pierwsze dwa rodzaje testów automatycznych nie są przeznaczone do testowania bezpieczeństwa, to które z nich? Istnieją dwa główne rodzaje testów automatycznych bezpieczeństwa.

SAST  

Testowanie bezpieczeństwa aplikacji statycznych (SAST) działa poprzez przeglądanie kodu źródłowego aplikacji lub usługi w celu zidentyfikowania źródeł luk w zabezpieczeniach.SASTNarzędzia te mogą być używane do skanowania kodu źródłowego w poszukiwaniu luk w zabezpieczeniach. Można je zintegrować z procesem rozwoju oprogramowania, aby już na etapie pisania kodu informować programistów o potencjalnych problemach. Możemy je również zintegrować zCI/płyta CDprocesu. Nie jako bramy jakości, ale jako bramy bezpieczeństwa, zapobiegające kontynuacji procesu, jeśliSASTNarzędzie nadal wykrywa luki w zabezpieczeniach, które nie zostały oznaczone jako fałszywie dodatnie.  

DAST

Dynamiczne testowanie bezpieczeństwa aplikacji (DAST) jest podobny doSASTale wykonuje dynamiczne testy, wykonując kod. Pozwala toDASTnarzędzia do wykrywania dodatkowych luk w zabezpieczeniach, których nie dałoby się wykryć za pomocą samej analizy kodu źródłowego. Jedną z metod, któraDASTnarzędzia służące do znajdowania dodatkowych luk w zabezpieczeniach, takich jak Cross Site Scripting (XSS), odbywa się poprzez tworzenie źródeł i ujść. KiedyDASTNarzędzie dostarcza dane wejściowe do pola w aplikacji i oznacza je jako źródło. Gdy dane są zwracane przez aplikację, ponownie szuka tego konkretnego parametru i, jeśli go znajdzie, oznacza go jako odpływ. Następnie może wysłać potencjalnie szkodliwe dane do źródła i, w zależności od tego, co jest wyświetlane w odpływie, określić, czy występuje luka w zabezpieczeniach, taka jak:XSS.Podobne doSAST,DASTnarzędzia mogą być zintegrowane zCI/płyta CDrurociąg jako bramka bezpieczeństwa.

Testowanie penetracyjne

Niestety,SASTIDASTNarzędzia nie mogą w pełni zastąpić testów manualnych, takich jak testy penetracyjne. Odnotowano znaczny postęp w testowaniu automatycznym, a w niektórych przypadkach techniki te połączono z nowocześniejszymi podejściami, aby stworzyć nowe techniki testowania, takie jak interaktywne testowanie bezpieczeństwa aplikacji (Interactive Application Security Testing).IAST) i samodzielna ochrona aplikacji w czasie wykonywania (ZGRZYT). Głównym problemem pozostaje jednak to, że te narzędzia, w tym nowoczesne techniki testowania, nie radzą sobie dobrze z lukami kontekstowymi. Weźmy na przykład przepływ płatności. Częstą luką jest możliwość pominięcia części procesu, na przykład etapu weryfikacji karty kredytowej. Jest to łatwy przypadek testowy do wykonania ręcznie, ale ponieważ wymaga kontekstu, nawetDASTNarzędzia będą miały trudności z wykryciem obejścia. Podobnie, luki w logice biznesowej i kontroli dostępu są trudne do wykrycia za pomocą narzędzi automatycznych, podczas gdy testy ręczne pozwalają na ich wykrycie dość szybko. Nie chodzi o to, że narzędzia automatyczne nigdy nie będą w stanie wykryć tych luk, po prostu bardziej opłacalne jest testowanie ręczne.  

Narzędzia powszechne

Istnieje kilka popularnych narzędzi, których można użyć do testów automatycznych. Zarówno [GitHub(otwiera się w nowej karcie)](https://github.com/features/security/code)i [Gitlab(otwiera się w nowej karcie)](https://docs.gitlab.com/ee/user/application_security/sast/)mieć wbudowaneSASTnarzędzia. Narzędzia takie jak [Snyk(otwiera się w nowej karcie)](https://snyk.io/)i [Sonarqube(otwiera się w nowej karcie)](https://www.sonarqube.org/)są również popularne ze względu naSASTIDAST.  

Studium przypadku: Nie może już znieść kapitana, zaraz wybuchnie!  
Typowy problem zSASTIDASTnarzędzi polega na tym, że narzędzie jest po prostu wdrażane w procesie, nawet w przypadku prostego dowodu koncepcji (PoC). Należy jednak wziąć pod uwagę kilka kwestii:

- Koszt wykonania
- Punkty integracyjne
- Kalibracja wyników
- Wdrażanie bramek jakości i bezpieczeństwa

Pierwszy i ostatni punkt jest bardzo ważny i jego zignorowanie może być kosztowne. PoczątkowyPoCNarzędzie powinno prawdopodobnie działać po godzinach pracy, ponieważ będzie musiało przeskanować cały kod. Ten proces może znacząco wpłynąć na wydajność narzędzia do kontroli kodu źródłowego. Wyobraź sobie, że dzieje się to tuż przed dużą premierą, a programiści nie mogą przygotować i wdrożyć najnowszych commitów.

Co więcej, w miarę jak coraz więcej organizacji przechodzi na bardziej zwinne podejście do rozwoju oprogramowania, większość repozytoriów otrzymuje kilkaset zatwierdzeń dziennie. Jeśli wprowadzisz nową bramkę bezpieczeństwa, nawet tylko na…PoC, która skanuje każde żądanie scalenia pod kątem luk w zabezpieczeniach przed zatwierdzeniem, może to wiązać się z drastycznym spadkiem wydajności infrastruktury i ograniczeniem szybkości, z jaką programiści mogą realizować żądania scalenia.

Wprowadzając nowe narzędzia do automatycznego testowania, należy dokładnie rozważyć, w jaki sposóbPoCnależy przeprowadzić w celu zapewnienia, że ​​nie zostaną spowodowane żadne zakłócenia, ale także w celu zapewnienia, żePoCjest reprezentatywny dla tego, jak narzędzia będą ze sobą współdziałać po ostatecznym zintegrowaniu. To doskonała równowaga, którą warto osiągnąć!

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/678d09b2f788f32a2766556cb4730701.png)  

W nowoczesnym rurociągi Oprogramowanie nie jest ręcznie przenoszone między różnymi środowiskami. Zamiast tego można zastosować zautomatyzowany proces kompilacji, budowania, integracji i wdrażania nowych funkcji oprogramowania. Ten proces nazywa sięCI/płyta CD.

_Uwaga: TerminCI/płyta CDW ostatnich latach podejście firmy do zarządzania oprogramowaniem uległo znacznym zmianom. Początkowo główny nacisk kładziono na zapewnienie, że rozwój oprogramowania odbywa się zgodnie z podejściem Agile, podczas gdy dostarczanie produktu nadal odbywało się w modelu kaskadowym, polegającym na wdrażaniu wyłącznie wersji finalnych. W tym czasie powszechne byłoCI/płyta CDOznaczało to ciągłą integrację i ciągły rozwój. Szybko jednak zdano sobie sprawę, że samo wdrożenie można również przeprowadzić w sposób zwinny (Agile), a akronim zmieniono na ciągłą integrację i ciągłe wdrażanie, a rozwój stał się częścią komponentu integracji. W końcu zdano sobie sprawę, że nie chodzi tylko o wdrożenie, ale o wszystkie aspekty związane z dostarczaniem rozwiązania i sposobem jego monitorowania po dostarczeniu, a akronim ponownie zmieniono na ciągłą integrację i ciągłe dostarczanie. Można więc usłyszeć, że te terminy są używane zamiennie, ale tak naprawdę wszystkie odnoszą się do tego samego._  

CI/płyta CD

Ponieważ stale tworzymy nowe funkcje dla naszego systemu lub usługi, musimy upewnić się, że będą one działać z bieżącą aplikacją. Zamiast czekać do końca cyklu rozwojowego, kiedy wszystkie funkcje zostaną zintegrowane, możemy teraz stale integrować nowe funkcje i testować je w trakcie ich rozwoju.

Możemy stworzyć to, co nazywamyCI/płyta CDrurociąg. Terurociągizwykle mają następujące odrębne elementy:

- Wyzwalacz startowy – akcja rozpoczynająca proces potoku. Na przykład żądanie push jest wysyłane do określonej gałęzi.
- Akcje budowlane – działania podejmowane w celu zbudowania projektu i nowej funkcji.
- Akcje testowe – akcje testujące projekt w celu upewnienia się, że nowa funkcja nie koliduje z żadną z bieżących funkcji aplikacji.
- Akcje wdrożenia – jeśli potok zakończy się sukcesem, akcje wdrożenia określają, co powinno się stać z kompilacją. Na przykład, należy ją wypchnąć do środowiska testowego.
- Akcje dostawy - jakoCI/płyta CDWraz z rozwojem procesów, nacisk kładziony jest już nie tylko na samo wdrożenie, ale na wszystkie aspekty dostarczania rozwiązania. Obejmuje to takie działania, jak monitorowanie wdrożonego rozwiązania.  

CI/płyta CD rurociągiWymagają infrastruktury kompilacji do wykonywania działań tych elementów. Zwykle nazywamy tę infrastrukturę koordynatorami kompilacji i agentami. Koordynator kompilacji kieruje różnymi agentami do wykonywania działańCI/płyta CD rurociągiw razie potrzeby.  

TeCI/płyta CD rurociągiTo właśnie tam zazwyczaj znajduje się największa część automatyzacji. W związku z tym jest to zazwyczaj największa powierzchnia ataku i największe ryzyko wkradnięcia się błędów konfiguracyjnych.  

Narzędzia powszechne

GitHub i Gitlab zapewniająCI/płyta CDMożliwości potoku i są dość popularne w użyciu. GitHub udostępnia agentów kompilacji, natomiast Gitlab udostępnia aplikację Gitlab runner, którą można zainstalować na hoście, aby stała się agentem kompilacji. W przypadku bardziej złożonych kompilacji należy skorzystać z oprogramowania do orkiestracji, takiego jakJenkinsmożna używać. Omówimy te narzędzia i ich typowe błędy w konfiguracji w kolejnych salach.  

Studium przypadku: Powiązanie między rozwojem a produkcją

Jednym z powszechnych błędów w konfiguracjiCI/płyta CD rurociągiużywa tych samych agentów kompilacji zarówno do kompilacji rozwojowej (DEV), jak i produkcyjnej (PROD). Stwarza to ciekawy problem, ponieważ większość programistów ma dostęp do wyzwalacza startowego dla kompilacji DEV, ale nie dla kompilacji PROD.

Gdyby jeden z tych programistów został naruszony, atakujący mógłby wykorzystać jego dostęp do wykonania złośliwej kompilacji DEV, która zhakowałaby agenta kompilacji. Nie stanowiłoby to dużego problemu, gdyby agent kompilacji był używany wyłącznie do kompilacji DEV. Ponieważ jednak agent ten jest również używany do kompilacji PROD, atakujący mógłby po prostu korzystać z tego agenta kompilacji do momentu, aż kompilacja PROD wstrzyknie do niej swój złośliwy kod, co pozwoliłoby mu naruszyć kompilację produkcyjną aplikacji.
