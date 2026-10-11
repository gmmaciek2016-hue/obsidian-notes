---

Bezpieczny cykl rozwoju oprogramowania (SSDLC)  

Podczas SDLC Testowanie bezpieczeństwa zostało wprowadzone bardzo późno w cyklu życia. Błędy, wady i inne luki w zabezpieczeniach były identyfikowane późno, przez co ich naprawa była znacznie bardziej kosztowna i czasochłonna. W większości przypadków testowanie bezpieczeństwa nie było uwzględniane w fazie testowania, więc użytkownicy końcowi zgłaszali błędy po wdrożeniu.SDLCmodele mają na celu wprowadzenie bezpieczeństwa na każdym etapie SDLC.  

Dlaczego jest bezpieczny SDLC ważny?

Badanie przeprowadzone przez Instytut Systemów i Nauk IBM wykazało, że naprawa błędu wykrytego podczas wdrażania kosztuje sześć razy więcej niż błąd zidentyfikowany już na etapie projektowania. Stwierdzono również, że błąd zidentyfikowany podczas testowania kosztuje 15 razy więcej, a nawet 100 razy więcej, jeśli zostanie zidentyfikowany w fazie konserwacji i eksploatacji. Zobacz poniższy rysunek:

![diagram pokazujący względny koszt poprawek błędów](https://tryhackme-images.s3.amazonaws.com/user-uploads/5c549500924ec576f953d9fc/room-content/1688d77f6f6401862a668820ab96061e.png)  

Źródło: Pracę badawczą na temat kosztów identyfikacji luk w zabezpieczeniach można znaleźć  [tutaj(otwiera się w nowej karcie)](https://www.researchgate.net/profile/Maurice-Dawson/publication/255965523_Integrating_Software_Assurance_into_the_Software_Development_Life_Cycle_SDLC/links/02e7e52114e5e1ba71000000/Integrating-Software-Assurance-into-the-Software-Development-Life-Cycle-SDLC.pdf?origin=publication_detail).

Oprócz szybszego rozwoju i redukcji kosztów, integracja zabezpieczeń w całymSDLCPomaga wcześnie wykryć i zredukować luki w zabezpieczeniach, znacząco zmniejszając ryzyko biznesowe. Przykładami wdrażania zabezpieczeń na wszystkich etapach są analiza architektury podczas projektowania, przegląd kodu i skanery na etapie rozwoju oraz przeprowadzanie ocen bezpieczeństwa (np. testów penetracyjnych) przed wdrożeniem. Na przykład w modelach kaskadowych tego rodzaju testy przeprowadzano pod koniec cyklu życia, tuż przed produkcją; w bardziej zwinnych procesach możemy wdrożyć podejście „bezpieczeństwo w fazie projektowania”. Jeśli testy penetracyjne prowadzą do błędów, takich jakSQLW scenariuszu kaskadowym, wstrzyknięcie, łagodzenie błędów wymagałoby wykonania kolejnego cyklu w celu ich naprawienia. Wymagałoby to przeprojektowania, zastosowania zmian i ponownego przetestowania, aby sprawdzić, czy błąd został naprawiony. W bardziej zwinnym podejściu, dyskusje na temat zapobiegania takim błędom, na przykład decyzja o parametryzacji na etapie planowania, pozwalają uniknąć konieczności wycofywania zmian, a kosztują jedynie dyskusję planistyczną.   

﻿Streszczenie

- Bezpieczeństwo jest stałą kwestią, dlatego jakość i bezpieczeństwo oprogramowania muszą być stale podnoszone.  
    
- Podnoszenie poziomu edukacji i świadomości w zakresie bezpieczeństwa: wszystkie strony zainteresowane znają zalecenia i wymogi dotyczące bezpieczeństwa na każdym etapie.
- Wady są wykrywane na wczesnym etapie, jeszcze przed wdrożeniem, co zmniejsza ryzyko włamania lub zakłócenia pracy systemu.
- Koszty ulegają obniżeniu, a szybkość rośnie dzięki wczesnemu wykrywaniu i usuwaniu luk w zabezpieczeniach. Pozwala to uniknąć ryzyka biznesowego, utraty reputacji marki i kar finansowych, które mogłyby doprowadzić do katastrofy ekonomicznej firmy.
## Realizowanie SSDLC

Jako [wstęp doDevSecOps](https://tryhackme.com/room/introductiontodevsecops)pokazy pokojowe, Bezpieczne SDLC Obejmuje wdrażanie procesów bezpieczeństwa na wszystkich etapach cyklu życia. Od narzędzi do testowania bezpieczeństwa po tworzenie wymagań bezpieczeństwa równolegle z wymaganiami funkcjonalnymi.  

Zrozumienie postawy bezpieczeństwa

﻿Jak w przypadku każdego nowego procesu , zrozumienie luk i stanu jest kluczowe dla skutecznego wdrożenia nowego narzędzia, rozwiązania lub zmiany.  Aby lepiej zrozumieć swoją postawę bezpieczeństwa, możesz zacząć od następujących kroków:﻿

- Przeprowadź **analizę luk** , aby określić, jakie działania i zasady obowiązują w Twojej organizacji i jak są skuteczne. Na przykład, sprawdź, czy zasady są przestrzegane (co robi zespół) i jakie procedury bezpieczeństwa (jak zespół je wdraża).  
    
- Twórz **Inicjatywy Bezpieczeństwa Oprogramowania** (SSI), wyznaczając realistyczne i osiągalne cele wraz ze zdefiniowanymi wskaźnikami sukcesu. Na przykład, może to być Standard Bezpiecznego Kodowania, podręczniki dotyczące przetwarzania danych itp., monitorowane za pomocą narzędzi do zarządzania projektami.  
    
- **Sformalizuj procesy** działań związanych z bezpieczeństwem w ramach SSI. Po uruchomieniu programu lub standardu, niezbędne jest poświęcenie okresu operacyjnego na zapoznanie się z nim przez inżynierów i zebranie opinii przed jego wdrożeniem. Podczas przeprowadzania analizy luk, każda polityka powinna mieć zdefiniowane procedury, aby zapewnić jej skuteczność.  
    
- **Zainwestuj w szkolenia z zakresu bezpieczeństwa** dla inżynierów oraz w odpowiednie narzędzia. Upewnij się, że pracownicy znają nowe procesy i narzędzia, które będą z nimi związane, aby je wdrożyć, i zainwestuj w szkolenia na wczesnym etapie, najlepiej przed wdrożeniem narzędzia.

**SSDLC Procesy**

Po zrozumieniu swojej postawy bezpieczeństwa nadszedł czas na ustalenie priorytetów i wdrożenie zabezpieczeń w swoim systemie. SDLC. Ogólnie rzecz biorąc, bezpieczne SDLC Polega na integracji procesów, takich jak testowanie bezpieczeństwa i inne działania, z istniejącym procesem rozwoju. Przykładami są: tworzenie wymagań bezpieczeństwa wraz z wymaganiami funkcjonalnymi oraz przeprowadzanie analizy ryzyka architektonicznego na etapie projektowania.SDLCProcesy te są następujące : 

![Macierz ryzyka](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/3d1e3379a1e3ccc46f3c7471095cbfae.png) 

- **Ocena ryzyka** – na wczesnych etapach SDLC, kluczowe jest zidentyfikowanie kwestii bezpieczeństwa, które promują podejście oparte na bezpieczeństwie w fazie projektowania, podczas gromadzenia wymagań funkcjonalnych na etapie planowania i określania wymagań. Na przykład, jeśli użytkownik zażąda wpisu na blogu z poziomu witryny, nie powinien mieć możliwości edycji bloga ani usuwania zbędnych pól wprowadzania.  
    
- **Modelowanie zagrożeń** – to proces identyfikacji potencjalnych zagrożeń w przypadku braku odpowiednich zabezpieczeń. Jest on bardzo skuteczny po przeprowadzeniu oceny ryzyka i na etapie projektowania. SDLC, ponieważ modelowanie zagrożeń koncentruje się na tym, co nie powinno się wydarzyć. Z kolei wymagania projektowe określają, jak oprogramowanie będzie się zachowywać i wchodzić w interakcje. Na przykład, należy upewnić się, że użytkownik zażąda informacji o koncie, a następnie zostanie przeprowadzona weryfikacja.
- **Skanowanie/recenzja kodu** – Recenzja kodu może być ręczna lub automatyczna. Skanowanie kodu lub automatyczna rewizja kodu może wykorzystywać technologie statycznych i dynamicznych testów bezpieczeństwa. Są one kluczowe na etapach rozwoju, podczas pisania kodu.
- **Oceny bezpieczeństwa – podobnie jak testy penetracyjne i oceny podatności –**  są formą zautomatyzowanego testowania, która pozwala zidentyfikować krytyczne ścieżki aplikacji, które mogą prowadzić do wykorzystania luk w zabezpieczeniach. Są one jednak hipotetyczne, ponieważ ocena nie obejmuje symulacji tych ataków. Z kolei testy penetracyjne identyfikują te luki i próbują je wykorzystać w celu udowodnienia ich słuszności. Pentesty i oceny podatności są przeprowadzane w fazie eksploatacji i utrzymania systemu. SDLC po stworzeniu prototypu aplikacji.

Istnieją metodologie wdrażania procesów z zadania 5, które ułatwią Ci nawigację i poprowadzą Cię przez proces wdrażania oceny ryzyka, modelowania zagrożeń, skanowania i testowania oraz zapewnienia operacyjnego. Poniższe zadania omówią te procesy bardziej szczegółowo.

Ryzyko odnosi się do prawdopodobieństwa wykorzystania zagrożenia, co negatywnie wpłynie na zasób lub cel, na który ono oddziałuje. Na przykład, wykorzystanie luk w zabezpieczeniach po opublikowaniu nowej wersji oprogramowania, błędy projektowe i źle zweryfikowany kod mogą zwiększać ryzyko wystąpienia takich scenariuszy. Zarządzanie ryzykiem jest ważnym filarem, który należy zintegrować z SDLC w celu ograniczenia ryzyka związanego z produktem lub usługą.  

---

Ocena ryzyka służy do określenia poziomu potencjalnego zagrożenia. Ryzyko zidentyfikowane w procesie oceny ryzyka można ograniczyć lub wyeliminować poprzez zastosowanie odpowiednich środków kontroli w procesie ograniczania ryzyka. Zazwyczaj po ocenie ryzyka następuje modelowanie zagrożeń, które zostanie omówione szczegółowo w następnej sekcji.  

**Przeprowadzanie oceny ryzyka**

1. Pierwszym krokiem w procesie oceny ryzyka jest założenie, że oprogramowanie zostanie zaatakowane i rozważenie czynników motywujących atakującego. Wypisz takie czynniki, jak wartość danych programu, poziom bezpieczeństwa firm dostarczających zasoby, od których zależy kod, klientów kupujących oprogramowanie oraz skalę dystrybucji oprogramowania (pojedyncze, małe grupy robocze lub globalne). Na podstawie tych czynników zapisz akceptowalny poziom ryzyka. Na przykład utrata danych może spowodować straty liczone w milionach dolarów dla firmy, zwłaszcza jeśli obecnie musi ona zapłacić grzywny zgodnie z RODO, ale wyeliminowanie wszystkich potencjalnych luk w zabezpieczeniach kodu może kosztować 40 000 dolarów. Firma i kilka innych grup interesariuszy muszą zdecydować, czy warto; kluczowe jest również zakomunikowanie tych kompromisów. Dlatego wszyscy rozumieją ryzyko i jego konsekwencje. Z punktu widzenia reputacji marki, jeśli atak zaszkodzi wizerunkowi firmy, w dłuższej perspektywie będzie kosztował firmę więcej niż naprawa kodu.
2. Kolejnym krokiem jest ocena ryzyka. Należy uwzględnić takie czynniki, jak najgorszy scenariusz, gdyby atakujący skutecznie zaatakował oprogramowanie. Możesz zademonstrować najgorszy scenariusz kierownictwu i starszym inżynierom, symulując atak ransomware. Określ wartość danych, które mają zostać skradzione, cenne dane, takie jak tożsamość użytkownika, dane uwierzytelniające umożliwiające kontrolę nad punktami końcowymi w sieci, oraz dane lub zasoby, które stanowią mniejsze ryzyko. Kolejnym czynnikiem, który należy wziąć pod uwagę, jest trudność przeprowadzenia udanego ataku, innymi słowy jego złożoność. Na przykład, jeśli atakujący może uzyskać dostęp do firmowego narzędzia do przekazywania informacji zwrotnych współpracownikom lub prowadzenia spotkań retrospektywnych, będzie to miało mniejszy wpływ niż dostęp do systemu monitorowania i alertów środowiska produkcyjnego. Wysoki poziom ryzyka będzie nie do zaakceptowania i najlepiej go zminimalizować. Na przykład, luka może zostać wykorzystana przez każdego, kto uruchamia predefiniowane skrypty ataku lub używa botnetów do rozprzestrzeniania skryptów w celu naruszenia bezpieczeństwa komputerów i sieci. Kluczowym czynnikiem są użytkownicy, których atak dotyczy.
3. Niektóre ataki dotyczą tylko jednego lub dwóch użytkowników, ale atak typu „odmowa usługi” (DOS) dotknie tysiące użytkowników, gdy zaatakowany zostanie serwer. Co więcej, tysiące komputerów może zostać zainfekowanych przez rozprzestrzenianie się robaków. Ostatnim czynnikiem jest dostępność celu. Należy ustalić, czy cel akceptuje żądania przez sieć, czy tylko lokalny dostęp, czy uwierzytelnianie jest wymagane do nawiązania połączenia, a także czy każdy może wysyłać żądania. Większe znaczenie ma to, czy atakujący uzyskuje dostęp do środowiska produkcyjnego, a nie do…piaskownicaśrodowisko wykorzystywane na lokalnych placach zabaw, gdzie ludzie mogą wykonywać ćwiczenia laboratoryjne lub uczestniczyć w instruktażach.

Rodzaje ocen ryzyka

Istnieje kilka rodzajów ocen ryzyka, które najlepiej sprawdzają się w różnych scenariuszach. Poniżej przedstawiono różne rodzaje ocen ryzyka:

**Jakościowa ocena ryzyka**

To najpopularniejszy rodzaj oceny ryzyka, jaki można spotkać w firmach (miejmy nadzieję). Celem jakościowej oceny ryzyka jest ocena i klasyfikacja ryzyka według progów, takich jak „Niski”, „Średni” i „Wysoki”. Systematycznie bada ona, co może spowodować szkody i jakie decyzje należy podjąć w celu zdefiniowania lub ulepszenia odpowiednich środków kontroli. Podobnie jak w przypadku wszystkich rodzajów oceny ryzyka, każdy poziom ma priorytet, gdzie „Wysoki” jest najpilniejszy. Chociaż jakościowe oceny ryzyka nie wykorzystują liczb, typowy wzór oceny ryzyka jakościowego to:

`Risk = Severity x Likelihood`

„Stopień” to wpływ konsekwencji, a prawdopodobieństwo to prawdopodobieństwo ich wystąpienia. Ocena tych okoliczności należy do osoby oceniającej ryzyko.

**Ilościowa ocena ryzyka**  

Ilościowa Ocena Ryzyka służy do pomiaru ryzyka za pomocą wartości liczbowych. Zamiast poziomów „Niski”, „Średni” i „Wysoki” stosuje się liczby reprezentujące te przedziały. Przeprowadzając ilościową analizę ryzyka, możemy skorzystać z narzędzi do określania wagi i prawdopodobieństwa wystąpienia zdarzenia lub niestandardowego zestawu obliczeń opartego na procesach firmy.

Załóżmy na przykład, że istnieją usługi z przypisanymi poziomami krytyczności biznesowej. W takim przypadku można powiedzieć, że jeśli błąd wpłynie na usługę krytyczną dla firmy (usługę uwierzytelniania, infrastrukturę płatności itp.), przyznamy jej 5 punktów. To pokazuje, jak ważne jest zrozumienie polityki bezpieczeństwa i jej procesów. Pomiar ryzyka i priorytetów za pomocą równania endemicznego dla usług firmy przyniesie znakomite rezultaty. Przykład macierzy ilościowej oceny ryzyka można zobaczyć poniżej:

![Macierz ryzyka](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/e5fb607dfd764c3e162da1783dd58e02.png)

Ocenę ryzyka lepiej przeprowadzać na początku SDLC, na etapie planowania i określania wymagań. Na przykład: „Dane klientów zostają wykradzione w wyniku ataku”. Po opracowaniu systemu można przeprowadzić ilościową analizę ryzyka: „Jeden klient może nas pozwać o 20 000 dolarów, jeśli jego dane zostaną ujawnione”, a mamy 100 klientów. Jednak Roczny Wskaźnik Występowania (ARO) wynosi 0,001. Zatem Roczna Oczekiwana Strata wynosi = 20 000 dolarów * 100 * 0,001 = 2000 dolarów, co oznacza, że ​​dopóki nasza kompensacyjna kontrola bezpieczeństwa jest niższa niż 2000 dolarów, nie wydajemy zbyt dużo na bezpieczeństwo.

Modelowanie zagrożeń

Modelowanie zagrożeń najlepiej zintegrować z fazą projektowania SDLCprzed napisaniem jakiegokolwiek kodu. Modelowanie zagrożeń to ustrukturyzowany proces identyfikacji potencjalnych zagrożeń bezpieczeństwa i priorytetyzacji technik łagodzenia ataków, aby chronić dane lub zasoby, które zostały sklasyfikowane jako cenne lub obarczone wyższym ryzykiem podczas oceny ryzyka, takie jak dane poufne. Wczesne przeprowadzenie tego procesu przynosi ogromną korzyść: potencjalne problemy można wykryć i rozwiązać na wczesnym etapie, co pozwala zaoszczędzić na kosztach napraw w przyszłości. 

Istnieją różne metody modelowania zagrożeń. Nie wszystkie mają ten sam cel; niektóre koncentrują się na ryzyku lub ochronie prywatności, podczas gdy inne są bardziej zorientowane na klienta. Możemy łączyć te metody, aby lepiej zrozumieć potencjalne zagrożenia; kluczowe jest przeanalizowanie, która z nich jest bardziej zgodna z projektem lub firmą.KROK,STRACH, IMAKARONnależą do powszechnych metodologii modelowania zagrożeń.  

**KROK**  

KROKskrót od Spoofing, Tampering, Repudiation, Information Disclosure, Denial Of Service i Elevation/Escalation of Privilege (podszywanie się, manipulacja, zaprzeczanie, ujawnianie informacji, odmowa usługi i podnoszenie/eskalowanie uprawnień).KROKto powszechnie używany model zagrożeń opracowany przez firmę Microsoft, który pozwala na szczegółową ocenę projektu systemu. Możemy z niego korzystaćKROKAby zidentyfikować zagrożenia, w tym własność naruszoną przez zagrożenie i jej definicję. W tym modelu należy opracować diagram przepływu danych systemu, a każdy węzeł powinien być zastosowany zKROKModel. Identyfikacja zagrożeń bezpieczeństwa to proces manualny, który nie jest obsługiwany przez narzędzia i powinien być przeprowadzany podczas oceny ryzyka. Wykorzystanie diagramów przepływu danych i integracjaKROK, jednostki systemu, powierzchnie ataku, jak znane granice i zdarzenia atakujące stają się bardziej identyfikowalne.KROKjest zbudowany naCIAzasada triady (poufność,Uczciwośći dostępność). Specjaliści ds. bezpieczeństwa, którzy wykonująKROKChcą odpowiedzieć na pytanie „Co mogłoby pójść nie tak z tym systemem”. Oto komponenty frameworka:

- **Spoofing:** Podszywanie się pod użytkownika przez osobę o złych intencjach, naruszające zasadę uwierzytelniania. Przykłady obejmują:ARP, IP iDNSpodszywanie się.
- **Manipulacja:** Modyfikacja informacji przez nieuprawnionego użytkownika, naruszającauczciwośćzasada.
- **Odrzucenie:** Brak odpowiedzialności za działania, za które nie można przypisać odpowiedzialności, co stanowi naruszenie zasady niezaprzeczalności.
- **Ujawnienie informacji:** naruszenie poufności, np. w przypadku wycieku danych.
- **Odmowa usługi:** wyczerpanie zasobów, uniemożliwiające autoryzowanym użytkownikom dostęp do systemu, naruszenie dostępności.
- **Podniesienie uprawnień:** uzyskanie nieautoryzowanego dostępu poprzez podwyższenie uprawnień i naruszenie zasad autoryzacji.

![Diagram STRIDE](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/a5904cf6f063a62e77df6623eb1cbd33.png)

**STRACH**  

SkrótSTRACHskłada się z pięciu pytań dotyczących każdego potencjalnego zagrożenia: Potencjalne szkody, Powtarzalność, Możliwość wykorzystania, Narażeni użytkownicy i Możliwość odkrycia.STRACHKlasyfikuje zagrożenia, przypisując im punkty na podstawie ich wagi i prawdopodobieństwa wystąpienia ryzyka. Oto jego elementy:

- **Uszkodzenie:** potencjalny wpływ zagrożenia, oceniany w skali od 0 do 10.
- **Powtarzalność:** Złożoność odtworzenia zagrożenia, oceniana w skali 0–10.
- **Możliwość wykorzystania:** Stopień, w jakim zagrożenie może zostać wykorzystane (ocena 0–10).
- **Dotknięci użytkownicy:** Liczba dotkniętych użytkowników, oceniona w skali 0–10.
- **Wykrywalność:** Łatwość wykrycia zagrożenia, oceniana w skali 0–10.

**MAKARON**  

MAKARONSkrót od Process for Attack Simulation and Threat Analysis (proces symulacji ataków i analizy zagrożeń). Dostosowuje on wymagania techniczne do celów biznesowych i zapewnia strategiczny obraz zagrożeń.MAKARONSiedem etapów to:

- **Określ cele:** Ustal zakres i zadania.
- **Określ zakres techniczny:** Utwórz diagramy architektoniczne w celu zmapowania powierzchni ataku.
- **Dekompozycja i analiza:** Wyznaczanie granic zaufania i ocena podatności.
- **Analiza zagrożeń:** identyfikacja potencjalnych zagrożeń na podstawie danych wywiadowczych.
- **Analiza luk i słabości:** ocena i łagodzenie słabości.
- **Wyliczanie i modelowanie ataków/exploitów:** symulowanie ścieżek ataków i luk w zabezpieczeniach.
- **Analiza wpływu ryzyka:** Dokumentowanie ryzyka i proponowanie działań łagodzących.

![Diagram PASTA](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/8222ed08e31753d975ec3ec3aa2e43a9.png)

﻿﻿﻿﻿Bezpieczny przegląd i analiza kodu

Według badań Verizon dotyczących naruszeń danych przeprowadzonych w 2020 roku, 43% naruszeń stanowiły ataki na aplikacje internetowe, a niektóre inne naruszenia bezpieczeństwa wynikały z luk w zabezpieczeniach aplikacji internetowych. Wdrożenie bezpiecznego przeglądu kodu w fazach SDLC, szczególnie w fazie wdrażania, zwiększy odporność i bezpieczeństwo produktu bez ponoszenia dodatkowych kosztów przyszłych poprawek. Bezpieczny przegląd kodu definiuje się jako środek, w którym sam kod jest weryfikowany i walidowany w celu zapewnienia możliwości minimalizacji i usuwania wykrytych luk w zabezpieczeniach, aby uniknąć luk i wad. Świadomość i proaktywność programistów w przeglądaniu kodu podczas tworzenia oprogramowania może skutkować szybszymi reakcjami łagodzącymi i mniejszą liczbą niezauważonych zagrożeń. Przegląd kodu jest kluczowym etapem w procesie SDLC dla programistów. Zapobiega to wszelkim opóźnieniom w wydaniu i problemom, na jakie narażeni są użytkownicy. Jak pokazano w poprzednim SSDLC Zadanie, koszt samego projektu i włożony wysiłek są proporcjonalne i tańsze w dłuższej perspektywie niż koszty stosowania przeglądów i analiz kodu. Wdrażając to podejście, organizacja będzie również zgodna ze standardami określonymi przez organy rządowe i certyfikacyjnymi. 

Przegląd kodu może być przeprowadzany ręcznie lub automatycznie. Ręczny przegląd kodu polega na tym, że ekspert analizuje i weryfikuje kod źródłowy, linijka po linijce, aby zidentyfikować luki w zabezpieczeniach. Dlatego wysokiej jakości ręczny przegląd kodu wymaga od eksperta komunikacji z programistami, aby poznać cel i funkcjonalność aplikacji. Wyniki analizy zostaną następnie przekazane programistom, jeśli zajdzie potrzeba naprawy błędów.   

Analiza kodu

Analiza statyczna bada kod źródłowy bez uruchamiania programu. W przeciwieństwie do tego, Analiza dynamiczna patrzy na źródło

kod podczas działania programu, analiza statyczna wykrywa błędy na poziomie implementacji ianaliza dynamiczna Wykrywa błędy w czasie wykonywania programu. Automatyczne testowanie bezpieczeństwa aplikacji statycznych (SAST) automatycznie analizuje i sprawdza kod źródłowy. 

SAST

SAST oznacza Statyczne Testowanie Bezpieczeństwa Aplikacji, białą metodę testowania, która bezpośrednio analizuje kod źródłowy.

Wiele osób tworzy aplikacje, które mogłyby zautomatyzować lub szybko wykonywać procesy, a także poprawić wydajność i komfort użytkownika, zapominając o negatywnym wpływie, jaki może mieć aplikacja niezabezpieczona. 

**Dlaczego jest to wersja statyczna?**  - Ponieważ test jest przeprowadzany przed uruchomieniem aplikacji.SASTmoże nawet pomóc wykryć luki w zabezpieczeniach aplikacji przed scaleniem kodu lub jego zintegrowaniem z oprogramowaniem, jeśli zostanie dodany jako częśćSDLCfaza rozwoju.

**Jak to działa SAST Praca**

SAST stosuje metodologię testowania polegającą na analizie kodu źródłowego w celu wykrycia wszelkich śladów luk, które mogą stanowić furtkę dla atakującego.SASTzwykle analizuje i skanuje aplikację przed kompilacją kodu.  

ProcesSASTJest również znane jako testowanie białoskrzynkowe. Po wykryciu luki w zabezpieczeniach, kolejnym krokiem jest sprawdzenie kodu i załatanie go, zanim zostanie skompilowany i wdrożony w środowisku produkcyjnym.  Testowanie białoskrzynkowe to podejście lub metoda, której testerzy używają do testowania wewnętrznej struktury oprogramowania i sprawdzania, jak integruje się ono z systemami zewnętrznymi.

Premia:SCA

﻿Podsumowując, SASTsłuży do skanowania kodu źródłowego w poszukiwaniu luk w zabezpieczeniach. Inny rodzaj testów idzie w parze zS AST, Analiza składu oprogramowania (SCA).SCAsłuży do skanowania zależności w celu wykrycia luk w zabezpieczeniach, pomagając zespołom programistycznym śledzić i analizować wszystkie komponenty typu open source włączane do projektu.SCAjest obecnie kluczowym filarem testów bezpieczeństwa, ponieważ nowoczesne aplikacje coraz częściej składają się z kodu open source. Jednym z największych wyzwań stojących przed zespołami programistów jest obecnie zapewnienie bezpieczeństwa ich bazy kodu, ponieważ aplikacje składają się z różnych bloków konstrukcyjnych.   

DAST

DAST oznacza dynamiczne testowanie bezpieczeństwa aplikacji, metodę testowania typu „czarna skrzynka”, która wykrywa luki w zabezpieczeniach w czasie wykonywania. DAST to narzędzie do skanowania dowolnej aplikacji internetowej w celu znalezienia luk w zabezpieczeniach. Służy do wykrywania luk w zabezpieczeniach aplikacji internetowej wdrożonej w środowisku produkcyjnym. DAST narzędzia będą zawsze wysyłać alerty do zespołu ds. bezpieczeństwa wyznaczonego do podjęcia natychmiastowych działań naprawczych.

Jak to działa DAST Praca

DAST Działa poprzez symulację zautomatyzowanych ataków na aplikację, naśladując złośliwego atakującego. Celem jest znalezienie nieoczekiwanych rezultatów, które atakujący mogliby wykorzystać do złamania zabezpieczeń aplikacji. Ponieważ DAST Narzędzia te nie posiadają wewnętrznych informacji o aplikacji ani kodzie źródłowym, atakują więc tak samo, jak zewnętrzni hakerzy — dysponując tą samą ograniczoną wiedzą i informacjami na temat aplikacji.

DAST to narzędzie, które można zintegrować na bardzo wczesnym etapie cyklu rozwoju oprogramowania. Jego celem jest pomoc organizacjom w ograniczaniu i ochronie przed ryzykiem, jakie mogą powodować luki w zabezpieczeniach aplikacji. Różni się ono znacznie od SAST ponieważ DASTwykorzystuje metodologię testowania czarnej skrzynki; przeprowadza swoje ocena podatnościna zewnątrz, ponieważ nie ma dostępu do kodu źródłowego aplikacji.DASTjest zazwyczaj używany w fazie testowaniaSDLC.

IAST

IASTOznacza interaktywne testowanie bezpieczeństwa aplikacji, które analizuje kod pod kątem luk w zabezpieczeniach podczas działania aplikacji. Zazwyczaj jest ono wdrażane równolegle z główną aplikacją na serwerze aplikacji.IASTto narzędzie do zabezpieczania aplikacji, przeznaczone dla aplikacji internetowych i mobilnych, które wykrywa i zgłasza problemy nawet podczas ich działania. Zanim ktoś w pełni zrozumie,IASTzrozumienie, osoba musi wiedzieć, coSASTIDASTmieć na myśli.IASTzostał opracowany, aby wyeliminować wszystkie ograniczenia w obuSASTIDAST. Wykorzystuje metodologię testowania Grey Box. **Jak to działaIASTPraca** IASTtestowanie odbywa się w czasie rzeczywistym, tak jakDAST, podczas gdy aplikacja działa w środowisku testowym.IASTmoże zidentyfikować linię kodu powodującą problemy z bezpieczeństwem i szybko poinformować o tym programistę w celu podjęcia natychmiastowych działań naprawczych.IASTsprawdza kod źródłowy podobnie doSASTale na etapie po budowie, w przeciwieństwie doSAST, który ma miejsce w trakcie rozwoju.IASTAgenci są zazwyczaj wdrażani na serwerach aplikacji. KiedyDASTskaner wykonuje swoją pracę, zgłaszając lukę w zabezpieczeniach, wdrożonyIASTAgent będzie teraz zwracał numer wiersza problemu z kodu źródłowego. Można wdrożyćIASTAgentów na serwerze aplikacji. Podczas testów funkcjonalnych przeprowadzanych przez testera QA agent analizuje każdy wzorzec, według którego przebiega transfer danych w aplikacji, niezależnie od tego, czy jest on niebezpieczny. Na przykład, jeśli dane pochodzą od użytkownika, a użytkownik chce wykonać…SQLWstrzyknięcie do aplikacji poprzez dołączenieSQLzapytanie do żądania, żądanie zostanie oznaczone jako niebezpieczne.

_Premia:ZGRZYT_

"ZGRZYT„ oznacza samodzielną ochronę aplikacji w czasie wykonywania.ZGRZYTto aplikacja środowiska uruchomieniowego zintegrowana z aplikacją, która analizuje ruch przychodzący i wychodzący oraz wzorce zachowań użytkowników końcowych, aby zapobiegać atakom bezpieczeństwa. To narzędzie różni się od innych, ponieważZGRZYTjest używany po wydaniu produktu, co sprawia, że ​​jest to narzędzie bardziej zorientowane na bezpieczeństwo w porównaniu do innych, znanych z testowania.

**Jak to działa?ZGRZYTpraca** ZGRZYTjest wdrażany na serwerze WWW lub aplikacji obok aplikacji głównej podczas działania, aby monitorować i analizować ruch przychodzący i wychodzący. Natychmiast po wykryciu problemu,ZGRZYTwyśle ​​alerty do zespołu ds. bezpieczeństwa i natychmiast zablokuje dostęp osobie zgłaszającej żądanie. Podczas wdrażaniaZGRZYT, zabezpieczy całą aplikację przed różnymi atakami. Nie czeka ani nie próbuje polegać wyłącznie na konkretnych sygnaturach znanych luk w zabezpieczeniach.

ZGRZYTto kompletne rozwiązanie, które obserwuje każdy szczegół różnych ataków na Twoją aplikację i rozumie jej zachowanie.

Wybór narzędzi

SAST,DAST, IIASTto świetne narzędzia, które wzajemnie się uzupełniają.  Kluczową zaletąDASTpolega na tym, że identyfikuje problemy występujące w czasie wykonywania — słabości, których nie da się wykryć, gdy aplikacja nie jest uruchomiona.SASTdoskonale identyfikuje luki w zabezpieczeniach podczas pisania kodu. Dodatkowo,DASTanalizuje reakcję aplikacji na atak, dostarczając cennych informacji o tym, jak prawdopodobne jest wykorzystanie danej luki. AST umożliwiaDevSecOpsi obsługuje ciągłe testowanie, monitorowanie, ocenę i walidację w czasie rzeczywistym.IASTPomaga priorytetyzować i ostrzegać o istotnych, krytycznych zagrożeniach, zgodnie z celami biznesowymi i potrzebami bezpieczeństwa aplikacji. Eksperci ds. bezpieczeństwa zawsze popierają korzystanie z dwóch lub więcej z tych narzędzi, aby zapewnić lepsze pokrycie, co zmniejszy ryzyko wystąpienia luk w zabezpieczeniach w środowisku produkcyjnym. Upewnij się, że narzędzia te są dopasowane do sposobu, w jaki inżynierowie wprowadzają kod i wchodzą w interakcję z potokiem; zwracaj uwagę na integracje i skup się na zapewnianiu wsparcia i edukacji, a nie na blokowaniu. Na przykład, jeśli wybierzesz…SAST, można je zintegrować, gdy inżynierowie przesyłają kod, a oni mogą otrzymać opinię na temat żądania połączenia przed scaleniem.

Oś czasu automatyzacji bezpieczeństwa aplikacji

Sprawdź poniższy schemat, aby zobaczyć, gdzie możesz umieścić narzędzia do testowania bezpieczeństwa!

![Harmonogram testów bezpieczeństwa](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/ed41446ac19972111b12a8b41bdb3599.png)  

Powyżej przedstawiono standardowy harmonogram wyboru momentu wdrożenia narzędzi do testowania bezpieczeństwa. Jak opisano wcześniej,SASTjest podejściem statycznym; nie ma potrzeby uruchamiania aplikacji. DlategoSASTmożna wdrożyć już na najwcześniejszych etapach rozwoju.SCAZazwyczaj najlepiej sprawdza się w przypadku identyfikacji komponentów open source, takich jak pakiety, za pomocą zależności. Jest to również korzystne w przypadku identyfikacji używanych licencji open source, szczególnie z perspektywy ryzyka prawnego. Dzięki temu można wdrożyć zarządzanie i kontrolę, egzekwując zasady bezpieczeństwa i licencjonowania na różnych etapach.SDLC.

Z drugiej strony,DASTopiera się na wykonaniu aplikacji, więc jej integracja w procesie nie jest tak prosta, jakSAST.DASTZazwyczaj jest wdrażany po etapie akceptacji kodu i fazie przedprodukcyjnej. To właśnie wtedy aplikacja zaczyna działać w środowiskach testowych (np.piaskownica/inscenizacja) podobna doIAST.DASTIIASTznajduje się na skrajnej prawej stronie twojego kanału, ponieważ wykonanie twojej aplikacji jest wymaganeDASTnarzędzi do wykonywania swojej pracy. Może to być dość czasochłonne, zwłaszcza jeśli Twoja aplikacja rozrosła się z czasem.ZGRZYT Pomaga wykrywać pakiety firm trzecich i powiązane z nimi luki w zabezpieczeniach w czasie wykonywania, umożliwiając programistom bardziej efektywne ustalanie priorytetów w zakresie usuwania i łagodzenia skutków najpilniejszych luk. Funkcja ta jest zazwyczaj włączana na etapie produkcji, ponieważ luki w zabezpieczeniach są analizowane w trakcie działania aplikacji.

﻿Ocena bezpieczeństwa  

Ocena bezpieczeństwa odgrywa podstawową rolę w zapewnieniu bezpieczeństwa wSDLCi powinny być wdrażane na wszystkich etapach, jeśli to możliwe. Testy bezpieczeństwa oceniają system, oprogramowanie lub aplikację internetową pod kątem luk w zabezpieczeniach i innych wektorów ataków. Ponieważ testy przeprowadzane są z holistycznego punktu widzenia aplikacji, zazwyczaj przeprowadza się je pod koniec.SDLC, w fazie eksploatacji i konserwacji, gdy wersja zawiera już wszystkie działające komponenty i aktualizacje. Istnieją dwa rodzaje ocen: testy penetracyjne iOcena podatnościZazwyczaj **firma zatrudnia i upoważnia zewnętrznych testerów bezpieczeństwa do podejmowania legalnych prób włamania się do sieci i systemów firmy** **.**

Ocena podatności

Ocena podatności koncentruje się na wyszukiwaniu luk, ale nie weryfikuje ich ani nie symuluje, aby udowodnić, że są one możliwe do wykorzystania w rzeczywistości. Zazwyczaj zautomatyzowane narzędzia działają w sieci i systemach organizacji. Przykładami narzędzi są OpenVAS, Nessus (Tenable) i ISS Scanner. Skanery te badają porty i usługi w systemach, w różnych systemach i na różnych adresach IP. Inne działania obejmują sprawdzanie wersji usług w bazie danych luk dotyczących danej wersji. Rezultatem jest raport z listą zazwyczaj wykrywanych luk, z automatyczną klasyfikacją poziomu zagrożenia, np. Wysoki/Średni/Niski lub przypisany.CVSSwynik.  

Testowanie penetracyjne

Obejmuje testowanie podatności, ale jest bardziej szczegółowe. Rozszerza je o testowanie/walidację podatności, kwantyfikację ryzyka i próby penetracji systemów. Na przykład, próbując zwiększyć uprawnienia po wykryciu luki, niektóre luki mogą stanowić mniejsze ryzyko, ale mogą być wykorzystane jako dźwignia do wyrządzenia większych szkód. Tester może sporządzić szczegółowy raport z sugerowanymi środkami zaradczymi w celu zminimalizowania podatności. Ułatwia to zrozumienie zagrożeń poprzez zademonstrowanie rzeczywistego ryzyka, na przykład odzyskania hasła pracownika poprzez wykorzystanie wspomnianej luki.  

Plusy i minusy

**Ocena podatności**  

|   |   |
|---|---|
|Zalety|Wady|
|- Nadaje się do szybkiej identyfikacji potencjalnych luk w zabezpieczeniach|- Możliwość wygenerowania dużej liczby raportów|
|- Część testu penetracyjnego|- Jakość zależy od użytego narzędzia|
|- Lepsze dla budżetu, są tańsze niż testy penetracyjne|- Nie uwzględniono rzeczywistych scenariuszy dotyczących luk w zabezpieczeniach (mogą one znajdować się zapełnomocniklub możliwe do wykorzystania tylko zinżynieria społeczna/referencje)|
||- Luka o niskim ryzyku może zostać wykorzystana jako element silniejszego ataku.|

**Testowanie penetracyjne**

|                                                                                                                                |                                                                |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Zalety                                                                                                                         | Wady                                                           |
| Tester pokazuje organizacjom, co może zrobić atakujący.                                                                        | Bardzo drogie                                                  |
| W jaki sposób wszelkie luki w zabezpieczeniach mogą zostać wykorzystane przeciwko niemu przez atakujących – rzeczywiste ryzyko | Wymaga rozległego planowania i czasu na przeprowadzenie testów |
| Można pokazać klientowi                                                                                                        |                                                                |

## ﻿﻿﻿SSDLCMetodologie

Można zastosować różne metody integracji zabezpieczeń wSDLCNajlepiej. Zanim zagłębimy się w każdą metodę, niezależnie od wybranej metodyki rozwoju (Agile,DevOps, Extreme Waterfall, itp.) konieczne jest:

- Buduj z myślą o bezpieczeństwie
    
- Wprowadzenie testów skoncentrowanych na bezpieczeństwie

Istnieje kilka metodologiiSDLC; oto kilka przykładów powszechnie stosowanych metodologii:

- Cykl rozwoju zabezpieczeń firmy Microsoft (SDL)
    
- OWASPProjekt bezpiecznego cyklu życia oprogramowania (S-SDLC)
    
- Punkty styku bezpieczeństwa oprogramowania

MicrosoftuSDL  

#### SDLzasady:

- Bezpieczeństwo w fazie projektowania: Bezpieczeństwo to wbudowana cecha jakościowa wpływająca na cały cykl życia oprogramowania.
    
- Bezpieczeństwo domyślne: Systemy oprogramowania są konstruowane tak, aby zminimalizować potencjalne szkody wyrządzone przez atakujących, np. oprogramowanie jest wdrażane z najmniejszymi niezbędnymi uprawnieniami.
    
- Bezpieczne wdrożenie: wdrażaniu oprogramowania towarzyszą narzędzia i wskazówki dla użytkowników i administratorów.
    
- Komunikacja: twórcy oprogramowania są przygotowani na pojawiające się zagrożenia, komunikując się otwarcie i na czas z użytkownikami i administratorami

SDLto zbiór obowiązkowych działań z zakresu bezpieczeństwa, pogrupowanych według tradycyjnych faz cyklu życia oprogramowania. Dane są gromadzone w celu oceny skuteczności szkoleń. Metryki wewnątrzprocesowe służą do potwierdzenia zgodności procesu. Metryki po wdrożeniu służą do kierowania przyszłymi zmianami.SDLkładzie duży nacisk na zrozumienie przyczyn i skutków luk w zabezpieczeniach. Zespół programistów musi wykonać obowiązkowe działania w zakresie bezpieczeństwa, aby zachować zgodność z wytycznymi Microsoft.SDLproces. Możesz wdrożyćSDLstosując się do poniższych praktyk:

|   |   |
|---|---|
|**Praktyka**|**Dlaczego?**|
|### **Zapewnij szkolenie**|Inżynierowie, menedżerowie programów i produktów muszą znać podstawy bezpieczeństwa i wiedzieć, jak wdrażać zabezpieczenia w oprogramowaniu i usługach, aby zwiększyć bezpieczeństwo produktów, a jednocześnie odpowiadać na potrzeby biznesowe i dostarczać wartość użytkownikom.<br><br>Szkolenia praktyczne będą uzupełniać i wzmacniać zasady bezpieczeństwa,SDLpraktyki, standardy i wymagania bezpieczeństwa oprogramowania oraz kierować się wnioskami uzyskanymi z danych lub nowo dostępnych możliwości technicznych.|
|### **Zdefiniuj wymagania bezpieczeństwa**|Uwzględnienie bezpieczeństwa i prywatności jest fundamentalnym aspektem tworzenia wysoce bezpiecznych aplikacji i systemów. Niezależnie od stosowanej metodologii rozwoju, wymagania bezpieczeństwa muszą być stale aktualizowane, aby odzwierciedlały zmiany w wymaganej funkcjonalności i krajobrazie zagrożeń.|
|### Zdefiniuj metryki i raportowanie zgodności|Kluczowe jest zdefiniowanie minimalnych akceptowalnych poziomów jakości bezpieczeństwa i pociągnięcie zespołów inżynierskich do odpowiedzialności za ich spełnienie. Określenie tych kryteriów na wczesnym etapie pomaga zespołowi zrozumieć ryzyko związane z problemami bezpieczeństwa, identyfikować i naprawiać luki w zabezpieczeniach w trakcie rozwoju oraz stosować standardy w całym projekcie.|
|### Wykonaj modelowanie zagrożeń|Dzięki temu zespołowi programistów możliwe jest rozważenie, udokumentowanie i omówienie kwestii bezpieczeństwa projektów w zaplanowanym środowisku operacyjnym w sposób ustrukturyzowany.<br><br>Zastosowanie ustrukturyzowanego podejścia do scenariuszy zagrożeń pomaga zespołowi skuteczniej i taniej identyfikować luki w zabezpieczeniach, określać ryzyko wynikające z tych zagrożeń, dokonywać wyboru funkcji bezpieczeństwa i wdrażać odpowiednie środki zaradcze.|
|### Ustal wymagania projektowe|TenSDLZazwyczaj rozumie się je jako działania zapewniające bezpieczeństwo, które pomagają inżynierom wdrażać „bezpieczne funkcje”, ponieważ są one dobrze zaprojektowane pod kątem bezpieczeństwa. Inżynierowie zazwyczaj polegają na funkcjach bezpieczeństwa, takich jak kryptografia, uwierzytelnianie, rejestrowanie itp. W wielu przypadkach wybór lub wdrożenie funkcji bezpieczeństwa okazuje się tak skomplikowane, że decyzje projektowe lub implementacyjne mogą prowadzić do powstania luk w zabezpieczeniach. Dlatego niezwykle ważne jest ich konsekwentne stosowanie i spójne zrozumienie zapewnianych przez nie zabezpieczeń.|
|### Definiowanie i stosowanie standardów kryptograficznych|Niezwykle ważne jest zapewnienie ochrony wszystkich danych, w tym informacji wrażliwych pod względem bezpieczeństwa oraz danych zarządczych i kontrolnych, przed niezamierzonym ujawnieniem lub modyfikacją podczas przesyłania lub przechowywania. W tym celu zazwyczaj stosuje się szyfrowanie. Na przykład,  należy korzystać wyłącznie z bibliotek szyfrujących sprawdzonych w branży i upewnić się, że są one wdrożone w sposób umożliwiający ich łatwą wymianę w razie potrzeby.|
|### Zarządzanie ryzykiem bezpieczeństwa związanym z korzystaniem z komponentów innych firm|Wybierając komponenty innych firm, należy koniecznie zrozumieć wpływ luki w zabezpieczeniach na bezpieczeństwo bardziej rozbudowanego systemu, z którym są zintegrowane. Dokładna inwentaryzacja komponentów innych firm i plan reagowania na wykrycie nowych luk w zabezpieczeniach w znacznym stopniu przyczynią się do ograniczenia tego ryzyka.|
|**Użyj zatwierdzonych narzędzi  <br>**|Zdefiniuj i opublikuj listę zatwierdzonych narzędzi i powiązanych z nimi mechanizmów kontroli bezpieczeństwa, takich jak opcje kompilatora/linkera i ostrzeżenia. Inżynierowie powinni dążyć do korzystania z najnowszych wersji zatwierdzonych narzędzi, takich jak wersje kompilatora, oraz korzystać z nowych funkcji analizy bezpieczeństwa i zabezpieczeń.|
|### **Wykonaj testy bezpieczeństwa (SAST,DAST,IAST)**|Analiza kodu źródłowego przed kompilacją zapewnia wysoce skalowalną metodę przeglądu bezpieczeństwa kodu i pomaga zapewnić przestrzeganie zasad bezpiecznego kodowania. To samo dotyczy weryfikacji w czasie wykonywania w pełni skompilowanego lub spakowanego oprogramowania, sprawdzając jego funkcjonalność, która staje się widoczna dopiero po zintegrowaniu i uruchomieniu wszystkich komponentów.|
|### **Przeprowadź ocenę bezpieczeństwa:Ocena podatnościi testy penetracyjne**|Celem testu penetracyjnego jest wykrycie potencjalnych luk w zabezpieczeniach wynikających z błędów kodowania, błędów konfiguracji systemu lub innych słabości wdrożenia operacyjnego. W związku z tym test zazwyczaj wykrywa najszerszy zakres luk w zabezpieczeniach.|
|### Ustanowienie standardowego procesu reagowania na incydenty|Przygotowanie planu reagowania na incydenty ma kluczowe znaczenie dla przeciwdziałania nowym zagrożeniom, które mogą pojawić się z czasem.  Plan powinien określać, z kim należy się skontaktować w przypadku awarii bezpieczeństwa, a także ustanawiać protokół obsługi bezpieczeństwa, w tym metody postępowania z kodem odziedziczonym od innych grup w organizacji oraz kodem pochodzącym od stron trzecich.|

OWASP'SS-SDLC  

#### S-SDLCZasady

- SDLjest zbiorem obowiązkowych działań związanych z bezpieczeństwem, pogrupowanych według faz tradycyjnego cyklu życia oprogramowania.
    
- Dane są zbierane w celu oceny skuteczności szkolenia.
    
- Do potwierdzenia zgodności procesu stosuje się wskaźniki wewnątrzprocesowe.
    
- Do planowania przyszłych zmian wykorzystuje się wskaźniki podawane po wydaniu.
    
- SDLkładzie duży nacisk na zrozumienie przyczyn i skutków luk w zabezpieczeniach.
    
- Zespół programistów musi wykonać szesnaście obowiązkowych czynności związanych z bezpieczeństwem, aby zachować zgodność z wytycznymi firmy MicrosoftSDLproces.

    ![Metodologia OWASP SSDLC](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/1e76d9be1c116a8d68925162aa3b01f0.png)

OWASPS-SDLCCelem jest zbudowanie „bramek jakości bezpieczeństwa”, które wspierają jakość i bezpieczeństwo oprogramowania tworzonego w całym procesie. Odbywa się to poprzez zastosowanie podejścia Agile Security, w którym sprinty są dedykowane bezpieczeństwu. Przykłady sprintów mogą obejmować: przeglądy kodu, uwierzytelnianie, autoryzację, walidację danych wejściowych oraz ocenę ryzyka technicznego, takiego jak wstrzykiwanie kodu. Bramki obejmują sprinty koncentrujące się na podobnych elementach konstrukcyjnych, jak te stosowane w Microsoft.SDL.OWASPS-SDLCPodejście Agile jest w dużym stopniu ukształtowane i oparte na podejściu „Modelu dojrzałości”, w szczególnościOWASP SAMMModel dojrzałości zapewniania oprogramowania (SAMM) to otwarta platforma, która pomaga organizacjom formułować i wdrażać strategię bezpieczeństwa oprogramowania dostosowaną do specyficznych ryzyk organizacji. Pomaga ona ocenić istniejące praktyki bezpieczeństwa oprogramowania w organizacji, zbudować program zapewnienia bezpieczeństwa oprogramowania, zademonstrować usprawnienia tego programu oraz zdefiniować i zmierzyć działania związane z bezpieczeństwem w organizacji.SAMMPomaga wyjaśnić cele, działania, wyniki, wskaźniki sukcesu, koszty itp. Przykładem może być karta wyników bezpieczeństwa do analizy luk, na przykład w określonym obszarze, takim jak ochrona punktów końcowych. Ma ona na celu odpowiedź na pytanie: „Jak dobrze sobie radzimy i dokąd chcemy dojść?”.[OWASP SAMMpołączyć(otwiera się w nowej karcie)](https://owasp.org/www-project-samm/)

Innym istotnym modelem bezpieczeństwa jest Building Security In Maturity Model (BSIMM).BSIMMjest studium rzeczywistych inicjatyw w zakresie bezpieczeństwa oprogramowania i odzwierciedla obecny stan bezpieczeństwa oprogramowania. BSIMMMożna go opisać jako „wskaźnik” pozwalający zrozumieć stan bezpieczeństwa firmy poprzez porównanie stanu bezpieczeństwa innych firm. Innymi słowy, nie mówi, co należy zrobić, ale co się robi źle. W sprawę zaangażowane są setki organizacji. [BSIMMpołączyć](https://owaspsamm.org/blog/2020/10/29/comparing-bsimm-and-samm/)

### SAST

W tym pomieszczeniu przyjrzymy się testowaniu bezpieczeństwa aplikacji statycznych (SAST), jedno z wielu narzędzi służących do wykrywania luk w zabezpieczeniach w trakcie cyklu rozwoju aplikacji. Przeanalizujemy jego zalety i wady oraz to, jak uzupełnia inne metody zabezpieczania aplikacji na wczesnym etapie rozwoju.

Cele edukacyjne

- Dowiedz się, w jaki sposób można zastosować metodę SAST do  wykrywania słabych punktów w rzeczywistych zastosowaniach.
- Zrozum zalety i wady korzystania SAST.
- Zapoznaj się z tym, jak SAST można wdrożyć w cyklu życia oprogramowania.

Wymagania dotyczące pokoju

Zanim przejdziemy dalej do tego pokoju, ważne jest zapoznanie się z lukami w zabezpieczeniach sieci, jak pokazano na rysunku [OWASPTop 10](https://tryhackme.com/room/owasptop102021) i[OWASP API10 najlepszych](https://tryhackme.com/room/owaspapisecuritytop105w) pokoi. Mile widziana jest również podstawowa wiedza o etapach cyklu życia oprogramowania, więc zachęcamy do zapoznania się z[SDLCpokój](https://tryhackme.com/room/sdlc) jeśli potrzebujesz.

Jedną z metod stosowanych w tworzeniu bezpiecznych aplikacji jest częste testowanie kodu pod kątem luk bezpieczeństwa w ramach procesu znanego jako przegląd kodu. Przegląd kodu polega na analizie kodu źródłowego aplikacji w celu wykrycia potencjalnych luk w zabezpieczeniach, wykorzystując podejście „białej skrzynki”. Dzięki dostępowi do kodu, recenzent może zagwarantować lepsze pokrycie funkcjonalności aplikacji i skrócić czas potrzebny na znalezienie błędów.

Jeśli luki w zabezpieczeniach zostaną zignorowane na wczesnym etapie procesu rozwoju, będą rozprzestrzeniać się aż do końca projektu, gdzie ich rozwiązanie jest bardziej pracochłonne i kosztowne. Przeglądy kodu będą miały na celu wykrycie takich luk w zabezpieczeniach na wczesnym etapie, gdy łatwiej je naprawić.  

![Koszt wad oprogramowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1e9aa4ddd5746ee00e0ad76d30208eb5.png)  

Ręczny a automatyczny przegląd kodu

Przeglądy kodu często przeprowadza się poprzez połączenie analizy ręcznej i narzędzi automatycznych, aby uzyskać najlepsze rezultaty. Oba podejścia mają zalety, które należy wziąć pod uwagę przy podejmowaniu decyzji, co jest najlepsze na każdym etapie cyklu rozwoju oprogramowania.

Z jednej strony, ręczne przeglądy kodu mają tę zaletę, że kod jest oceniany przez człowieka, co pozwala na dogłębną analizę i uzyskanie bardziej precyzyjnych wyników. Jednak ponieważ aplikacja często zawiera tysiące linii kodu, zadanie to może szybko stać się przytłaczające dla recenzenta, co może prowadzić do przeoczenia niektórych luk w zabezpieczeniach z powodu zmęczenia.

Z drugiej strony, narzędzia zautomatyzowane doskonale radzą sobie z niemal natychmiastowym wykrywaniem typowych luk w zabezpieczeniach, oszczędzając recenzentowi mnóstwo czasu. Narzędzia zautomatyzowane działają również spójnie, niezależnie od rozmiaru bazy kodu, więc nie przeoczą luk w zabezpieczeniach tak, jak zrobiłby to człowiek, o ile mają predefiniowane reguły do ​​ich wykrywania. Jeśli narzędzie nie ma skonfigurowanych reguł dla określonego typu luk, prawdopodobnie je przeoczy.

Kolejnym ważnym aspektem do porównania jest koszt. Koszt ręcznego przeglądu często będzie wyższy, ponieważ recenzent musi poświęcić dużo czasu na śledzenie luk w kodzie. Zautomatyzowane narzędzia przeprowadzą analizę niemal natychmiast.

Z tych powodów zazwyczaj warto uruchamiać automatyczne testy na wczesnym etapie cyklu rozwoju oprogramowania, aby zająć się wszystkimi łatwiejszymi zadaniami przy niższych kosztach, a także przeprowadzać ręczne przeglądy okresowo lub wtedy, gdy osiągnięte zostaną ważne cele projektu, aby zająć się złożonymi lukami w zabezpieczeniach, których automatyczne narzędzia mogą nie być w stanie wykryć.

Zanim wskoczysz SAST narzędzia, przyjrzymy się, jak zwykle przeprowadza się ręczny przegląd rdzeni, ponieważ ułatwi to zrozumienie, jak SAST narzędzia analizują kod.  

Podczas tego zadania naszym celem będzie znalezienie SQL Luki w zabezpieczeniach typu injection w kodzie źródłowym prostej aplikacji. Aplikacja ma inne luki, ale skupimy się na jednym typie luki, aby zrozumieć, jak przeprowadzane są tradycyjne przeglądy kodu i jak te kroki odnoszą się do technik analizy stosowanych przez SAST narzędzia.

Przed kontynuowaniem upewnij się, że Maszyna wirtualna uruchamia się po naciśnięciu zielonego przycisku **„Start Machine”** dołączonego do tego zadania. Maszyna wirtualna Rozpoczyna się w widoku podzielonym. Jeśli maszyna nie jest widoczna, naciśnij niebieski przycisk **„Pokaż widok podzielony”** w prawym górnym rogu tego pokoju.

Do tego zadania użyjemy kodu, który można znaleźć w`/home/ubuntu/Desktop/simple-webapp/`

Wyszukiwanie niebezpiecznych funkcji

Pierwszym krokiem podczas analizy kodu jest identyfikacja potencjalnie niebezpiecznych funkcji. Ponieważ szukamy ataków typu SQL injection, powinniśmy skupić się na funkcjach, które mogłyby zostać użyte do wysyłania surowych zapytań do bazy danych. Ponieważ nasz kod wykorzystuje PHP i MySQL, oto kilka funkcji, które są zazwyczaj używane do wysyłania zapytań MySQL:

|Silnik bazy danych|Funkcjonować|
|---|---|
|MySQL|mysqli_query()  <br>mysql_query()  <br>mysqli_prepare()  <br>query()  <br>prepare()|

Prostym sposobem ręcznego wyszukiwania wystąpień takich funkcji jest użycie polecenia grep do rekurencyjnego sprawdzenia wszystkich plików naszego projektu. Na przykład, aby wyszukać wystąpienia funkcji `mysqli_query()`, przejdź do katalogu bazowego projektu i uruchom następujące polecenie:

Linux

```shell-session
user@machine$ cd /home/ubuntu/Desktop/simple-webapp/html/

user@machine$ grep -r -n 'mysqli_query('
  db.php:18: $result = mysqli_query($conn, $query);
```

Opcja ta `-r`nakazuje grepowi rekurencyjne przeszukanie wszystkich plików w bieżącym katalogu i `-n`wskazuje, że chcemy, aby grep podał nam numer wiersza, w którym znaleziono wzorzec. W powyższym wyniku terminala widać, że `mysqli_query()`w wierszu znaleziono pojedyncze wystąpienie `18`.

Zidentyfikowaliśmy linię, która może prowadzić do ataków SQL Injection. Jednak sama analiza tej linii nie pozwala na stwierdzenie, czy występuje luka w zabezpieczeniach.

Zrozumienie kontekstu

Przyjrzyjmy się `db.php`bliżej kontekstowi `mysqli_query()`funkcji, aby sprawdzić, czy możemy lepiej zrozumieć, jak jest ona używana:

```php
function db_query($conn, $query){
    $result = mysqli_query($conn, $query);
    return $result;
}
```

Tutaj widzimy, że `mysqli_query()`jest to zawarte w `db_query()`funkcji, a `$query`parametr jest przekazywany bezpośrednio, bez modyfikacji. Funkcje często zagnieżdżają się w innych funkcjach, więc sama analiza lokalnego kontekstu funkcji czasami nie wystarcza, aby ustalić, czy występuje luka w zabezpieczeniach. Teraz musimy prześledzić użycie funkcji `db_query()`w całym kodzie, aby zidentyfikować potencjalne luki w zabezpieczeniach.

Śledzenie danych wprowadzanych przez użytkownika do potencjalnie podatnych na ataki funkcji

Możemy ponownie użyć polecenia grep, aby wyszukać zastosowania `db_query()`:

Linux

```shell-session
user@machine$ grep -rn 'db_query('
    hidden-panel.php:7:$result = db_query($conn, $sql);
    hidden-panel.php:20:$result2 = db_query($conn, $sql2);
    hidden-panel.php:23:$result3 = db_query($conn, $sql3);
    db.php:17:function db_query($conn, $query){
```

Tutaj otrzymujemy trzy zastosowania dla `db_query()`on `hidden-panel.php`. Ponownie możemy przeanalizować kontekst każdego wywołania, zaczynając od wywołania w wierszu 7:

```php
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];
$result = db_query($conn, $sql);
```

Gratulacje z okazji znalezieniaSQLWstrzyknięcie! Wszystko, co zostanie przekazane w `guest_id`parametrze za pomocą metody GET, zostanie połączone z surowym zapytaniem SQL bez żadnej dezynfekcji danych wejściowych, co umożliwi atakującemu zmianę zapytania.

Jeżeli przeprowadzimy podobny proces dla dwóch pozostałych zastosowań `db_query()`, otrzymamy następujący kod:

```php
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";
$result2 = db_query($conn, $sql2);

$sql3 = "SELECT id, name FROM asciiart WHERE id=".preg_replace("/[^0-9]/", "", $_GET['art_id'], 1);
$result3 = db_query($conn, $sql3);
```

Ponownie mamy kilka parametrów GET łączonych w zapytania SQL. To mogłoby sugerować, że zidentyfikowaliśmy dwie kolejne luki w zabezpieczeniach. Jednak w obu przypadkach parametry GET są oczyszczane poprzez `preg_replace()`użycie różnych wyrażeń regularnych, które zastępują każdy niedozwolony znak pustym ciągiem. Aby zdecydować, czy te wiersze kodu są podatne na atak, musimy ocenić, czy zastosowane filtry pozwalają na…SQLzastrzyki do przejścia.

Zapytanie `$sql2`jest przepuszczane przez filtr, który dopuszcza tylko znaki alfanumeryczne lub cudzysłowy. Chociaż cudzysłowy mogą wydawać się potencjalnym wektorem dla SQLi, w tym przypadku nie stanowią zagrożenia, ponieważ zdanie SQL zawiera przekazywany ciąg znaków `$_GET['log_id']`w pojedynczych cudzysłowach ('). Ponieważ atakujący nie miałby możliwości ucieczki z ciągu znaków wSQLw zdaniu możemy być pewni, że linia ta nie jest podatna na ataki.

Zapytanie on `$sql3`jest jeszcze bardziej restrykcyjne, pozwalając na przekazywanie tylko znaków numerycznych `$_GET['art_id']`. Należy jednak zauważyć, że `preg_replace()`funkcja jest wywoływana z trzecim parametrem ustawionym na „1”. Jeśli odwołamy się do [strony podręcznika funkcji,(otwiera się w nowej karcie)](https://www.php.net/manual/en/function.preg-replace.php)Dowiemy się, że trzeci parametr wskazuje maksymalną liczbę zamian. Ponieważ jest ustawiony na 1, tylko pierwszy znak, który nie jest liczbą, zostanie zastąpiony pustym ciągiem. Wszystkie pozostałe znaki zostaną przepuszczone bez zamiany, co umożliwiaSQLzastrzyki. Ta linia jest rzeczywiście podatna na ataki.

Wystarczająco dużo recenzji podręczników

Wykorzystaliśmy ręczny przegląd kodu, aby zidentyfikować dwaSQLpunktów wstrzykiwania w naszej aplikacji. Chociaż przykładowa aplikacja jest dość prosta, prawdziwa aplikacja ma o wiele więcej linii kodu. Śledzenie każdej instancji potencjalnie podatnej funkcji będzie znacznie bardziej skomplikowane. Do tej pory powinno być już jasne, że ręczne przeglądanie dużych baz kodu może szybko stać się żmudnym zadaniem. Przejdźmy teraz do…SAST narzędzia, które wykonają dla nas tę samą analizę i sprawdzą, jak dobrze sobie radzą.

Testowanie bezpieczeństwa aplikacji statycznych

Testowanie bezpieczeństwa aplikacji statycznych (SAST) odnosi się do wykorzystania zautomatyzowanych narzędzi do analizy kodu. Celem nie jest zastąpienie ręcznych przeglądów kodu, lecz zapewnienie prostej metody automatyzacji prostych kontroli kodu w celu szybkiego wykrywania luk w zabezpieczeniach w trakcie procesu rozwoju, bez konieczności angażowania wyspecjalizowanej osoby.

SASTuzupełnia inne techniki, takie jak dynamiczne testowanie bezpieczeństwa aplikacji (DAST) lub Analiza składu oprogramowania (SCA), aby zapewnić holistyczne podejście do bezpieczeństwa aplikacji w całym cyklu życia oprogramowania. Podobnie jak w przypadku każdej innej techniki,SASTbędzie miało swoje zalety i wady, o których musimy wiedzieć:

|   |   |
|---|---|
|**Zalety:**<br><br>- Nie wymaga uruchomienia instancji aplikacji docelowej.  <br>    <br>- Zapewnia szeroki zakres funkcjonalności aplikacji.<br>- Działa szybko, w przeciwieństwie do innych dynamicznych technik.<br>- SASTNarzędzia te dokładnie informują o tym, gdzie w kodzie znajdują się luki w zabezpieczeniach.<br>- Łatwy do zintegrowania z TwoimCI/płyta CDrurociąg.|**Wady:**<br><br>- Kod źródłowy aplikacji nie zawsze jest dostępny (w przypadku aplikacji innych firm).<br>- Skłonny do fałszywie pozytywnych wyników.<br>- Nie można identyfikować luk, które mają charakter dynamiczny.<br>- SASTNarzędzia są w większości specyficzne dla danego języka. Mogą sprawdzać tylko języki, które znają.|

SASTPod maską

Podczas gdy każdySASTnarzędzie jest inne, większość z nich będzie wykonywać dwa główne zadania:

1. **Przekształć kod w model abstrakcyjny:** SASTNarzędzia zazwyczaj pobierają kod źródłowy i generują abstrakcyjną reprezentację do dalszej analizy. WiększośćSASTNarzędzia będą reprezentować kod za pomocą abstrakcyjnych drzew składniowych (AST), ale niektóre narzędzia mogą mieć inne, równoważne, zastrzeżone struktury. Pozwala to na łatwiejszą analizę kodu w sposób niezależny od używanego języka programowania. Ten krok jest kluczowy dla późniejszej analizy, ponieważ każda cecha języka programowania, która nie zostanie poprawnie przetłumaczona na AST, prawdopodobnie nie zostanie skutecznie przeanalizowana pod kątem bezpieczeństwa.
2. **Przeanalizuj abstrakcyjny model pod kątem problemów bezpieczeństwa:** Zostaną użyte różne techniki analizy w celu wyszukania potencjalnych luk w modelu kodu.

W tej sali nie będziemy szczegółowo omawiać modelowania kodu, ponieważ nie będziesz musiał zajmować się nim z perspektywy użytkownika. Zamiast tego skupimy się na różnych technikach analizy powszechnie stosowanych przezSASTnarzędzia:

|   |   |
|---|---|
|![Analiza semantyczna](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/7c3d17f4c1cb81950fe4a9f056e03dba.png)|**Analiza semantyczna:** Ten rodzaj analizy można porównać do wyszukiwania potencjalnie niebezpiecznych funkcji podczas ręcznego przeglądu kodu. Jej celem jest znalezienie błędów związanych z wykorzystaniem potencjalnie niebezpiecznego kodu w kontekście lokalnym.<br><br>Przykładem może być wyszukiwanie wywołań, w `mysqli_query()`których parametry GET lub POST są bezpośrednio łączone z ciągiem zapytania:<br><br>```php<br>mysqli_query($db, "SELECT * from users where username=".$_GET['username'])<br>```|
|![Analiza przepływu danych](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/fb294ccfe9bbd914c21a174e64f13213.png)|**Analiza przepływu danych:** Istnieją sytuacje, w których używane są potencjalnie niebezpieczne funkcje, ale analiza lokalnego kontekstu wywołania funkcji nie pozwala na stwierdzenie, czy występuje luka w zabezpieczeniach. Weźmy na przykład funkcję zdefiniowaną w następujący sposób:<br><br>```php<br>function db_query($conn, $query){<br>    $result = mysqli_query($conn, $query);<br>    return $result;<br>}<br>```<br><br>Patrząc na kod funkcji, trudno stwierdzić, czy występują w nim jakiekolwiek luki. Analiza lokalnego kontekstu wywołania niebezpiecznej funkcji w tym przypadku nie wystarczy.<br><br>Analiza przepływu danych pozwoli prześledzić, w jaki sposób informacje przepływają od danych wejściowych, którymi użytkownik może manipulować, do potencjalnie podatnych na ataki funkcji, tak jak robiliśmy to podczas ręcznej analizy kodu dostarczonej aplikacji. W terminologii analizy przepływu danych, dane wejściowe będą nazywane **źródłami** , a potencjalnie podatne funkcje – **ujściami** . Jeśli dane przepływają ze źródła do ujścia bez przeprowadzenia sanityzacji, mamy do czynienia z luką w zabezpieczeniach.  <br><br>Wracając do `db_query()`funkcji, analiza przepływu danych musiałaby znaleźć wszystkie jej przypadki użycia i prześledzić je, aby sprawdzić, czy jakiekolwiek zanieczyszczone dane wejściowe (źródło) zostały do ​​niej wysłane i ostatecznie trafiły jako część zapytania wykonywanego przez `mysqli_query()`(odbiornik).<br><br>![Wykres przepływu danych](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/aa9389c3ba8aaadd6ed4ce84025f818d.png)|
|![Analiza przepływu sterowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1747a47ae9ed1257e9a2e83cf51940bd.png)|**Analiza przepływu sterowania:** analizuje kolejność operacji w kodzie w poszukiwaniu sytuacji wyścigu, użycia niezainicjowanych zmiennych lub wycieków zasobów. Jako przykład spójrzmy na poniższy fragment kodu Java:<br><br>```javascript<br>String cmd = System.getProperty("cmd");  <br>cmd = cmd.trim();<br>```<br><br>Jeśli `cmd`właściwość nie jest zdefiniowana, wywołanie `System.getProperty()`zwróci wartość NULL. Wywołanie metody trim ze zmiennej NULL spowoduje zgłoszenie wyjątku w czasie wykonywania.|
|![Analiza strukturalna](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/8e1238f36efec1e0d531a1b3fb422d7e.png)|**Analiza strukturalna:** Analizuje specyficzne struktury kodu każdego języka programowania. Obejmuje to przestrzeganie najlepszych praktyk podczas deklarowania klas, ocenę bloków kodu, które mogą nigdy nie zostać wykonane (martwy kod), prawidłowe stosowanie bloków try/catch oraz inne kwestie związane z używaniem niezabezpieczonych materiałów kryptograficznych (słabych kluczy lub IV).<br><br>Oto szybki przykład kodu, który zostanie wykryty przez analizę strukturalną:<br><br>```php<br>$options = array('private_key_bits' => 1024, 'private_key_type' => OPENSSL_KEYTYPE_RSA);  <br>$res = openssl_pkey_new($options);<br>```<br><br>W tym przypadku mamy implementację RSA z rozmiarem klucza wynoszącym 1024, co według dzisiejszych standardów jest uznawane za niewystarczające.|
|![Analiza konfiguracji](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/66518f2330b41f5fcab67b49daae3fc4.png)|**Analiza konfiguracji:** Wyszukuje błędy w konfiguracji aplikacji, a nie sam kod. Na przykład aplikacje działające w ramach Internetowych Usług Informacyjnych (IIS) będą miały plik konfiguracyjny o nazwie [brakujący fragment tekstu] `web.config`, PHP będzie przechowywał wszystkie opcje konfiguracyjne w pliku o nazwie [ `php.ini`brakujący fragment tekstu], a większość aplikacji będzie korzystała z pliku konfiguracyjnego. Sprawdzając konfiguracje, narzędzie zidentyfikuje możliwe ulepszenia.<br><br>Oto przykład dwóch dyrektyw konfiguracyjnych wPHPco prawdopodobnie spowodowałoby wzrost zagrożenia dla narzędzi SAST, gdyż ułatwiają one niektóre wektory ataków na RFI, SSRF lub inne:<br><br>```php<br>allow_url_include = On<br>allow_url_fopen = On<br>```|

Ważne jest, aby pamiętać, że nie każdy SASTNarzędzie to zaimplementuje wszystkie omówione przez nas techniki analizy, ale dobrze jest mieć je jako punkt odniesienia, aby porównywać różne dostępne rozwiązania.

Teraz, gdy wiemy jakSASTNarzędzia działają, jesteśmy gotowi użyć kilku z nich. Użyjemy prostegoPHPAplikacja jest naszym celem dla tego zadania. Kod aplikacji znajdziesz w `simple-webapp`folderze na pulpicie.

Ponowne sprawdzenie naszej aplikacji z Psalmem

Najpierw użyjemy **Psalm (PHP Static Analysis Linting Machine)** , prostego narzędzia do analizy kodu PHP. Narzędzie jest już zainstalowane w projekcie aplikacji, więc nie musisz go instalować, ale instrukcje instalacji znajdziesz w [dokumentacji online Psalm.(otwiera się w nowej karcie)](https://psalm.dev/docs/running_psalm/installation/)jeśli to konieczne.

Otwórz terminal i przejdź do katalogu projektu. W katalogu głównym projektu znajdziesz plik psalm.xml. To jest plik konfiguracyjny Psalma i powinien wyglądać tak:  

```xml
<?xml version="1.0"?>
<psalm
    errorLevel="3"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
    findUnusedBaselineEntry="true"
>
    <projectFiles>
        <directory name="html/" />
        <ignoreFiles>
            <directory name="vendor" />
        </ignoreFiles>
    </projectFiles>
</psalm>
```

Nie będziemy zagłębiać się w opcje konfiguracji, ale tutaj widać `errorLevel`parametr, który wskazuje, jak rygorystyczne będzie podejście Psalmu do zgłaszania problemów. Im niższa wartość, tym więcej problemów zostanie zgłoszonych. Jest również sekcja o nazwie `projectFiles`, w której wskazane są pliki do skanowania. W tym projekcie skanowany będzie tylko katalog html, a katalog dostawcy zostanie zignorowany (ponieważ nie chcemy testować zależności od oprogramowania firm trzecich).

Po skonfigurowaniu pliku konfiguracyjnego możesz uruchomić Psalm za pomocą następującego polecenia z poziomu katalogu projektu:

Linux

```shell-session
user@machine$ cd /home/ubuntu/Desktop/simple-webapp/
user@machine$ ./vendor/bin/psalm --no-cache

ERROR: TypeDoesNotContainType - html/hidden-panel.php:10:5 - Operand of type 0 is always falsy (see https://psalm.dev/056)
  if ($result->num_rows = 0) {
```

Domyślnie Psalm przeprowadza jedynie analizę strukturalną kodu i wskazuje błędy programistyczne wymagające naszej uwagi. W poprzednim przykładzie Psalm informuje, że warunek w `if`klauzuli to zawsze `false`. W tym przypadku programista omyłkowo użył operatora przypisania ( `=`) zamiast operatora porównania ( `==`). Ponieważ operator przypisania zawsze zwraca przypisaną wartość ( `0`w tym przypadku ), warunek zawsze będzie oceniany jako fałsz ( `0`zostanie automatycznie rzutowany `false`w PHP).

Domyślne testy będą wyszukiwać problemy z typami zmiennych, inicjalizacją zmiennych i innymi bezpiecznymi wzorcami kodowania. Chociaż problemy te nie stanowią luk w zabezpieczeniach, Psalm przedstawi rekomendacje, aby kod był zgodny z najlepszymi praktykami kodowania, co stanowi dobry punkt wyjścia do uniknięcia błędów w czasie wykonywania.

Psalm oferuje również możliwość uruchomienia analizy przepływu danych w naszym kodzie za pomocą `--taint-analysis`flagi. Wynik tego polecenia będzie o wiele ciekawszy, ponieważ wskaże potencjalne problemy z bezpieczeństwem. Wynik polecenia będzie wyglądał następująco:

Linux

```shell-session
user@machine$ cd /home/ubuntu/Desktop/simple-webapp/
user@machine$ ./vendor/bin/psalm --no-cache --taint-analysis

ERROR: TaintedInclude - html/view.php:22:9 - Detected tainted code passed to include or similar (see https://psalm.dev/251)
  $_GET
    <no known location>

  $_GET['img'] - html/view.php:22:28
include('./gallery-files/'.$_GET['img']);

  concat - html/view.php:22:9
include('./gallery-files/'.$_GET['img']);
```

Dla każdego zgłoszonego błędu Psalm pokaże Ci pełny ślad przepływu danych od źródła ( `$_GET`) do funkcji odbiorczej ( `include()`). Mamy tu do czynienia z typową luką w zabezpieczeniach typu Local File Inclusion (LFI), ponieważ parametr GET `img`jest łączony bezpośrednio z nazwą pliku przekazaną do funkcji `include()`.

Analiza przepływu danych zazwyczaj pozwala na uzyskanie najciekawszych wniosków z punktu widzenia bezpieczeństwa. Jednak równie ważne jest naprawienie innych ustaleń strukturalnych, nawet jeśli nie przekładają się one bezpośrednio na podatność na wykorzystanie. Luki strukturalne często mogą prowadzić do błędów logiki biznesowej, które mogą być trudne do wykrycia, lub do nieprzewidywalnych zachowań w aplikacji.

Radzenie sobie z wynikami fałszywie pozytywnymi i fałszywie negatywnymi

Niezależnie od tego, jakiego narzędzia SAST używasz, błędy zawsze będą występować. Przypominamy, że zazwyczaj będziemy się zajmować dwoma następującymi typami błędów:

- **Fałszywe alarmy:** narzędzie zgłasza lukę w zabezpieczeniach, której nie ma w kodzie.
- **Fałszywe negatywy:** Narzędzie nie zgłasza luki w zabezpieczeniach kodu.

Błędy te mogą pojawić się, gdy narzędzie nie jest w stanie prawidłowo ocenić kodu docelowego, ale mogą się również pojawić, gdy my, jako użytkownicy, nie używamy narzędzia prawidłowo.

Jako szybki przykład, podczas wcześniejszego ręcznego przeglądu kodu znaleźliśmy trzy możliwe przypadki ataku typu SQL injection. Mimo to odrzuciliśmy jeden z nich, ponieważ skutecznie stosowano do niego filtrowanie znaków, co pozostawiło nam dwie potwierdzone luki w zabezpieczeniach typu SQL injection. Jeśli sprawdzimy wynik Psalma, zauważymy, że zgłoszony został tylko jeden przypadek ataku typu SQL injection (pierwszy w wierszach `6-7`) `hidden-panel.php`:

Linux

```shell-session
user@machine$ ./vendor/bin/psalm --no-cache --taint-analysis

ERROR: TaintedSql - html/db.php:18:32 - Detected tainted SQL (see https://psalm.dev/244)
  $_GET
    <no known location>

  $_GET['guest_id'] - html/hidden-panel.php:6:65
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];

  concat - html/hidden-panel.php:6:8
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];

```

Tylko w ramach eksperymentu zakomentujmy linie `6`i `7`w pliku hidden-pannel.php i zobaczmy, co się stanie:

```php
// $sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];
// $result = db_query($conn, $sql);
```

Teoretycznie nie powinniśmy już zgłaszać błędów dotyczących instancji TaintedSQL. Jeśli jednak ponownie uruchomimy Psalm, zgłosi on teraz inny błąd TaintedSQL odpowiadający jednemu z dwóch pozostałych.SQLzapytania:

Linux

```shell-session
user@machine$ ./vendor/bin/psalm --no-cache --taint-analysis

ERROR: TaintedSql - html/db.php:18:32 - Detected tainted SQL (see https://psalm.dev/244)
  $_GET
    <no known location>

  $_GET['log_id'] - html/hidden-panel.php:19:87
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  call to preg_replace - html/hidden-panel.php:19:87
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";
```

Pewnie zastanawiasz się teraz, dlaczego Psalm nie wykrył tej luki za pierwszym razem. Przyczynę tego można znaleźć, sprawdzając pierwszy wiersz obu błędów. Oba wskazują na wiersz 'line `18`of' `db.php`jako źródło problemu. W przypadku Psalm obie luki są takie same i związane ze sposobem wywołania wiersza ' `mysqli_query()`line `18`of' `db.php`. Innymi słowy, Psalm oczekuje, że zastosujesz poprawkę w tym miejscu, ponieważ nie rozumie, że kod definiuje się `db_query()`jako wrapper dla zapytań do bazy danych.

Przed kontynuowaniem upewnij się, że odkomentowałeś wiersze `6-7`w `hidden-panel.php`:

```php
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];
$result = db_query($conn, $sql);
```

Aby lepiej zrozumieć sytuację, możemy użyć **adnotacji,** które dostarczą więcej kontekstu. Możemy określić, że dane `db_query()`powinny być traktowane jako ujścia, dzięki czemu otrzymamy błąd, jeśli jakiekolwiek zanieczyszczone dane wejściowe dotrą do funkcji poprzez `$query`parametr. Aby to zrobić, dodaj następujący komentarz do `db_query()`definicji funkcji w `db.php`:

```php
/**
 * @psalm-taint-sink sql $query
 * @psalm-taint-specialize
 */
function db_query($conn, $query){
    $result = mysqli_query($conn, $query);
    return $result;
}
```

Adnotacja `@psalm-taint-sink`nakazuje Psalmowi sprawdzenie `$query`parametru pod kątem zanieczyszczonych danych wejściowych typu `sql`. Teraz Psalm będzie generował błąd TaintedSQL za każdym razem, gdy zanieczyszczone dane wejściowe osiągną wartość `db_query()`.

Musimy również dodać `@psalm-taint-specialize`adnotację, aby poinformować Psalm, że każde wywołanie funkcji powinno być traktowane jako osobne zagadnienie i że skażenie funkcji zależy wyłącznie od otrzymanych danych wejściowych. W ten sposób otrzymamy oba zagadnienia oddzielnie.

Po ponownym uruchomieniu Psalmu powinniśmy teraz otrzymać wszystkie wystąpienia błędów TaintedSQL, zgodnie z oczekiwaniami:

Linux

```shell-session
user@machine$ ./vendor/bin/psalm --no-cache --taint-analysis

ERROR: TaintedSql - html/db.php:21:26 - Detected tainted SQL (see https://psalm.dev/244)
  $_GET
    <no known location>

  $_GET['guest_id'] - html/hidden-panel.php:6:65
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];

  concat - html/hidden-panel.php:6:8
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];

  $sql - html/hidden-panel.php:6:1
$sql = "SELECT id, firstname, lastname FROM MyGuests WHERE id=".$_GET['guest_id'];

  call to db_query - html/hidden-panel.php:7:27
$result = db_query($conn, $sql);

ERROR: TaintedSql - html/db.php:21:26 - Detected tainted SQL (see https://psalm.dev/244)
  $_GET
    <no known location>

  $_GET['log_id'] - html/hidden-panel.php:19:87
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  call to preg_replace - html/hidden-panel.php:19:87
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  preg_replace - html/hidden-panel.php:19:87
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  preg_replace - vendor/vimeo/psalm/stubs/CoreGenericFunctions.phpstub:1182:10
function preg_replace($pattern, $replacement, $subject, int $limit = -1, &$count = null) {}

  concat - html/hidden-panel.php:19:9
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  concat - html/hidden-panel.php:19:9
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  $sql2 - html/hidden-panel.php:19:1
$sql2 = "SELECT id, logtext FROM logs WHERE id='".preg_replace('/[^a-z0-9A-Z"]/', "", $_GET['log_id']). "'";

  call to db_query - html/hidden-panel.php:20:28
$result2 = db_query($conn, $sql2);
```

**Uwaga:** pojawi się trzeci błąd, powtarzający jeden z poprzednich. Dzieje się tak, ponieważ  `mysqli_query`jest on nadal uważany za prawidłowy odpływ (Psalm ma wbudowaną listę domyślnych odpływów), więc oryginalny alert powinien być nadal wyświetlany na nowych alertach.

Na koniec, jeśli porównasz wyniki Psalma z wynikami naszej ręcznej recenzji, zauważysz pewne różnice:

||Przegląd ręczny|Przegląd Psalmów|Werdykt|
|---|---|---|---|
|$SQL|Wrażliwy|Wrażliwy|OK|
|$sql2|Niewrażliwy|Wrażliwy|Fałszywie pozytywny|
|$sql3|Wrażliwy|Niewrażliwy|Fałszywie negatywny|

Podczas korzystania z urządzenia zawsze należy spodziewać się pewnego poziomu wyników fałszywie dodatnich i fałszywie ujemnych.SASTnarzędzia. Jak w przypadku każdego innego narzędzia, należy ręcznie sprawdzić raport w celu wyszukania ewentualnych błędów. SASTstanowi doskonałe uzupełnienie przeglądów ręcznych, ale nigdy nie należy go uważać za ich zamiennik.

SASTto jedno z pierwszych narzędzi pojawiających się w cyklu rozwoju oprogramowania. Często jest wdrażane na etapie kodowania, ponieważ nie wymaga posiadania funkcjonalnej aplikacji, aby z niego korzystać.

![SAST w cyklu rozwoju](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/8d4c2f1e6b6b61d8e13d8e0c4597773e.png)

W zależności od przypadku,SASTmożna wdrożyć na jeden z następujących sposobów:  

- **CI/płyta CDintegracja:** Za każdym razem, gdy zostanie wysłane żądanie ściągnięcia lub scalenia,SASTNarzędzia sprawdzą kod pod kątem luk w zabezpieczeniach. Sprawdzanie żądań ściągnięcia zapewnia, że ​​kod, który trafia do scaleń, przeszedł co najmniej podstawową kontrolę bezpieczeństwa. W niektórych przypadkach, zamiast sprawdzać każde żądanie ściągnięcia, wykonuje sięSASTskanowanie tylko podczas scalania może pomóc zapobiec spowolnieniom w procesie rozwoju, ponieważ pozwala uniknąć sytuacji, w której wszyscy programiści muszą czekać na pełneSASTskany.
- **Integracja IDE:** SASTNarzędzia można zintegrować z ulubionymi środowiskami programistycznymi (IDE) programistów, zamiast czekać na żądanie ściągnięcia lub scalenie. W ten sposób kod można poprawić jak najwcześniej, oszczędzając czas na dalszym etapie projektu.

Pamiętaj, że możesz chciećSASTdziała zarówno na środowiskach IDE programistów, jak i na TwoimCI/płyta CDpotoku, co byłoby prawidłowe. Na przykład narzędzia IDE mogą przeprowadzać podstawowe kontrole strukturalne i egzekwować wytyczne dotyczące bezpiecznego kodowania, podczas gdyCI/płyta CDIntegracje mogą wymagać bardziej czasochłonnej analizy przepływu danych/skażeń. Pamiętaj, że Twoja konkretna konfiguracja będzie zależeć od wymagań każdego projektu i powinna zostać dokładnie oceniona przez zespół.

Jeśli chcesz dowiedzieć się, jak można zintegrować narzędzia bezpieczeństwa zCI/płyta CDrurociąg, sprawdź[DASTmiejsce](https://tryhackme.com/room/dastzap) na przykład integracjiDASTnarzędzie doJenkinsrurociąg. Proces zSASTnarzędzia są dość podobne, więc nie będziemy ich tu powtarzać.  

IntegrowanieSASTw środowiskach IDE

Na Twojej maszynie wirtualnej zainstalowany jest edytor VS Code, który jest już skonfigurowany do używania kilku SAST narzędzia:

- **Psalm:** Narzędzie, którego używamy, obsługuje integrację ze środowiskiem IDE poprzez zainstalowanie wtyczki Psalm w programie VS Code bezpośrednio z [Visual Studio Marketplace(otwiera się w nowej karcie)](https://marketplace.visualstudio.com/items?itemName=getpsalm.psalm-vscode-plugin)Ta wtyczka będzie sprawdzać wszystko, co wpisujesz, w czasie rzeczywistym i wyświetlać te same alerty, co wersja konsolowa, bezpośrednio w kodzie. Analiza skażeń nie będzie dostępna, więc zobaczysz tylko problemy strukturalne zgłoszone w podstawowej analizie Psalmów.
    
- **Semgrep:**  Jeszcze jedenSASTnarzędzie, które można zainstalować w programie VS Code bezpośrednio z [Visual Studio Marketplace(otwiera się w nowej karcie)](https://marketplace.visualstudio.com/items?itemName=Semgrep.semgrep)Podobnie jak w przypadku Psalmu, alerty będą wyświetlane bezpośrednio w kodzie. Semgrep pozwala nam nawet w razie potrzeby tworzyć własne reguły. Reguły załadowane dla tego projektu można sprawdzić w katalogu `semgrep-rules`wewnątrz katalogu projektu. Szczegóły dotyczące budowania reguł Semgrep zostaną omówione w przyszłości, więc nie martw się tym teraz. Reguły można sprawdzić w katalogu, ale nie będzie to wymagane w tym przypadku.

Oba narzędzia działają podobnie, wyświetlając wszelkie wykryte problemy bezpośrednio w kodzie. Jedyną istotną różnicą jest to, że Semgrep uruchamia się po uruchomieniu VS Code i wyświetla wykryte problemy we wszystkich plikach, podczas gdy Psalm wyświetla tylko problemy związane z aktualnie edytowanym plikiem. Wtyczki dodają następujące informacje do ekranu IDE:

![SAST w VS Code](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/0409daf7cdf144dfaa3e9f1e4ab2fcb9.png)  

Dla każdego wiersza, w którym wykryto problemy, możesz uzyskać dodatkowe informacje, najeżdżając na niego kursorem myszy. Oto, co otrzymasz, najeżdżając kursorem na wiersz 46 `login.php`:

![Problemy wbudowane w VS Code](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/9b3cd323e1ef63bac1c9dab83171827f.png)  

Pełną listę problemów możesz sprawdzić również klikając wskaźnik Błędy u dołu ekranu VS Code:

![Panel Problemów](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/a879e9d06f657dbfd45dcc874dc3c91f.png)  

Sprawdzanie środowiska IDE pod kątem problemów pozwala programistom pisać bardziej przejrzysty kod, co znacząco wpływa na bezpieczeństwo końcowej aplikacji.

Używając obu narzędzi w swoim środowisku IDE, odpowiedz na pytania znajdujące się na końcu zadania.

SAST to jedna z wielu technik, które możemy wykorzystać do poprawy bezpieczeństwa naszych aplikacji w trakcie ich rozwoju. Pokazaliśmy, jak korzystać z Psalm, jednego z wielu dostępnych SAST narzędzia i ile czasu nam to oszczędza w porównaniu z ręcznymi przeglądami. Jak w przypadku każdego innego zautomatyzowanego narzędzia, niezbędna jest ręczna walidacja wyników, ponieważ mogą pojawić się fałszywe alarmy.

Pamiętaj, aby sprawdzić[DASTmiejsce,](https://tryhackme.com/room/dastzap) aby nauczyć się, jak Analiza dynamiczna uzupełnia SAST aby wzmocnić bezpieczeństwo Twojego procesu rozwoju.

Co to jest DAST?

**Dynamiczne testowanie bezpieczeństwa aplikacji (DAST)** to proces testowania działającej instancji aplikacji internetowej pod kątem słabych punktów i luk w zabezpieczeniach. Koncentruje się on na podejściu „czarnej skrzynki”, w którym luki w zabezpieczeniach są wykrywane tak samo, jak zrobiłby to zwykły atakujący. Mówiąc prościej, DAST identyfikuje luki w zabezpieczeniach, próbując je wykorzystać ręcznie lub za pomocą narzędzi automatycznych.

Testując aplikację z zewnętrznej perspektywy, możemy oderwać się od jej wewnętrznego działania i skupić się na identyfikacji luk, które prawdopodobnie wykryłby atakujący. Oznacza to, że wyniki uzyskane z DAST często wskazują na luki w zabezpieczeniach wymagające priorytetowej uwagi, ponieważ można się ich spodziewać bez wcześniejszej znajomości danej aplikacji.

Ważne jest, aby pamiętać, że DAST Nie zastępuje innych metod wykrywania luk w zabezpieczeniach aplikacji, lecz je uzupełnia. Bezpieczny cykl rozwoju oprogramowania często łączy kilka technik, aby zapewnić wystarczająco dobre pokrycie luk w zabezpieczeniach.

Manualne kontra automatyczne DAST

Istnieją dwa sposoby DAST można wykonać:

- **Podręcznik DAST Inżynier ds .** bezpieczeństwa ręcznie przeprowadzi testy aplikacji w celu sprawdzenia, czy nie ma w niej luk.
- **Automatyczny DAST:** Automatyczne narzędzie przeskanuje aplikację internetową w poszukiwaniu luk w zabezpieczeniach.

Oba procesy są komplementarne i mogą być stosowane na różnych etapach **cyklu życia oprogramowania (SDLC)** Łączenie narzędzi ręcznych i automatycznych często daje najlepsze rezultaty niż poleganie na każdym z nich osobno.

Podręcznik DAST pomoże nam znaleźć słabości, których zautomatyzowane narzędzie nie wykryje od razu, ponieważ nie rozumie aplikacji z punktu widzenia funkcjonalnego.

Problem z robieniem wszystkiego ręcznie polega na tym, że ręczne testy dla każdego commita lub drobnej zmiany w kodzie w fazie rozwoju zajmą zbyt dużo czasu. Właśnie tutaj zautomatyzowaneDASTwyróżnia się tym, że umożliwia szybkie przeprowadzanie wielu testów w aplikacji docelowej bez konieczności interakcji z człowiekiem.

DASTwSDLC

![DAST w SSDLC](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d5b8c1597d4d218692e466e39364c9cb.png)  

Chociaż każdy scenariusz jest inny, powszechnie stosuje się automatyczneDASTpodczas faz testowych. ZautomatyzowaneDASTNarzędzia te są często optymalizowane pod kątem szybkości, aby programiści mogli szybko uzyskać informacje zwrotne, w przeciwieństwie do tradycyjnego skanera luk w zabezpieczeniach aplikacji internetowych, którego uruchomienie może zająć kilka godzin. Chodzi tu nie o dokładne skanowanie aplikacji, ale o wczesne wykrycie problemów.  

PodręcznikDASTZ drugiej strony, skanowanie ręczne jest często przeprowadzane okresowo, aby uniknąć spowolnienia całego procesu rozwoju. Zazwyczaj skanowanie ręczne przeprowadza się co tydzień podczas tworzenia aplikacji, ale w dużej mierze zależy to od projektu. W skanowaniu ręcznym można zastosować bardziej intensywny profil skanowania, aby zidentyfikować jeszcze więcej luk w zabezpieczeniach.

Kiedy aplikacja jest gotowa do wdrożenia do produkcji, zawsze dobrym zwyczajem jest przeprowadzenie pełnego testu penetracyjnego aplikacji internetowej, aby wykryć wszelkie wady w implementacji finalnego produktu.

**Uwaga:** W większości literatury często mówi się o automatyzacjiDASTpo prostu jakoDASTi często rozważymy ręcznyDASTw ramach testów penetracyjnych aplikacji internetowych. PodręcznikDASTmożna również określić jako „tradycyjny”DAST".

DASTPlusy i minusy

Podobnie jak w przypadku każdego innego procesu służącego do znajdowania luk w zabezpieczeniach aplikacji,DASTbędzie miało swoje zalety i wady:

|   |   |
|---|---|
|Zalety:<br><br>- Wykrywa luki w zabezpieczeniach w czasie wykonywania. Obejmuje to luki specyficzne dla procesu wdrażania, których nie da się wykryć, analizując sam kod.<br>- DASTznajdzie luki takie jakHTTPPrzemyt żądań, zatruwanie pamięci podręcznej i zanieczyszczenie parametrów, których nie można znaleźć za pomocąSAST.<br>- DASTNarzędzia nie zwracają uwagi na język programowania używany przez Twoją aplikację. PonieważDASTjest to testowanie typu black-box, w którym wszystkie aplikacje są traktowane niezależnie od języka.<br>- Zmniejszona liczba wyników fałszywie dodatnich w porównaniu doSAST.<br>- DASTNarzędzia mogą wykryć pewne luki w logice biznesowej. Skuteczność zależy od narzędzia i nie powinna być traktowana jako zamiennik testowania ręcznego.|Wady:<br><br>- Pokrycie kodu nie jest najlepsze.DASTmoże nie obejmować określonych sytuacji, które zostaną wywołane wyłącznie przez określone przypadki użycia w Twojej aplikacji.<br>- Niektóre luki mogą być trudniejsze do znalezienia przy użyciuDAST, w porównaniu do technik analizy kodu statycznego.<br>- Niektóre aplikacje są trudne do indeksowania. Nowoczesne aplikacje w dużym stopniu opierają się na przetwarzaniu JavaScript po stronie klienta. To utrudniaDASTnarzędzia do ich pokonywania.<br>- DASTskanery nie będą w stanie powiedzieć Ci, jak szczegółowo naprawić niektóre luki w zabezpieczeniach, ponieważ nie mają pojęcia o kodzie źródłowym.<br>- Niektóre typy skanowania mogą wymagać dużo czasu.<br>- Aby przeprowadzić testowanie, potrzebna jest działająca aplikacja.|

Gotowy doDAST?

W większości przypadków znajdzieszDASTkontekstualizowany jako seria testów automatycznych. Zbadamy jednak, jak działa proces ręczny, aby lepiej zrozumieć, co zasadniczo robi większość narzędzi. Ogólnie rzecz biorąc,DASTNarzędzie wykona co najmniej dwa następujące zadania na stronie docelowej:

- **Spidering/Crawling:** Narzędzie będzie poruszać się po aplikacji internetowej, próbując ją zmapować i zidentyfikować listę stron i parametrów, które mogą zostać zaatakowane.
- **Skanowanie podatności:** Narzędzie będzie próbowało uruchomić ładunki atakujące zidentyfikowane strony i parametry. Użytkownik zazwyczaj może dostosować rodzaj ataków, aby obejmowały tylko te, które są istotne dla aplikacji docelowej.

Będziemy używaćZASTRZELIĆ pełnomocnikjako naszDASTnarzędzie do celów demonstracyjnych w tym pomieszczeniu. Należy jednak pamiętać, że wieleDASTNarzędzia używane w przedsiębiorstwach są płatne i dość drogie, ale opierają się na tych samych zasadach, co inne skanery podatności w aplikacjach internetowych. Główną różnicą między narzędziami będą możliwości wykrywania podatności oraz liczba dodatkowych funkcji dodawanych do produktu, przydatnych w przedsiębiorstwach, takich jak panele sterowania, integracja z systemem zgłoszeń i wiele innych.

W całym tym pomieszczeniu będziesz korzystać z maszyny wirtualnej (Maszyna wirtualna). PonieważMaszyna wirtualnaUruchomienie zajmie kilka minut, warto kliknąć `Start Machine`przycisk w prawym górnym rogu tego zadania. Możesz uzyskać dostęp do maszyny wirtualnej za pomocą AttackBox lub połączenia VPN. Jeśli używasz AttackBox, pamiętaj o kliknięciu przycisku `Start AttackBox`u góry strony.

Przeszukiwanie aplikacji za pomocą ZASTRZELIĆ

Pierwszym krokiem, jaki podejmiemy, będzie stworzenie mapy wszystkich zasobów w docelowej aplikacji internetowej, co pozwoli nam określić zakres analizy.ZASTRZELIĆudostępnia moduł indeksujący, którego możemy użyć w tym celu. **Spider** przejdzie do podanej przez Ciebie strony startowej i dokładnie przeszuka witrynę, podążając za wszystkimi wykrytymi linkami.

![Pająk](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/9a6c2409ddb76cc7d67e97dc4ab9e118.png)  

Aby przeszukać witrynę, przejdź do **Narzędzia -> Przeszukiwanie** . Spowoduje to wyświetlenie okna dialogowego Przeszukiwanie, w którym wystarczy wskazać witrynę jako punkt wyjścia. Na razie pola Kontekst i Użytkownik pozostawmy puste. W razie potrzeby możesz zaznaczyć następujące opcje dodatkowe:

- **Rekursja:** rekurencyjne przeszukiwanie witryny w poszukiwaniu linków.
- **Tylko poddrzewo przeszukiwania:** ogranicz przeszukiwanie do podfolderów adresu URL punktu początkowego.
- **Pokaż opcje zaawansowane:** Włącz kartę Zaawansowane, na której możesz określić dodatkowe parametry, aby dostroić indeksowanie.

![Okno pająka](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1cc8aecf25ac7dd193f23eda02aaf643.png)  

Wskaż na[http://IP_MASZYNY:8082/(otwiera się w nowej karcie)](http://machine_ip:8082/)i naciśnij „Rozpocznij skanowanie”. Po chwili powinieneś zobaczyć wszystkie adresy URL znalezione przez robota na karcie „Witryny”:

![Karta Witryny](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/70b413458e34d59dfab7730076a6d299.png)  

Lista witryn powinna teraz zawierać wszystkie adresy URL znalezione podczas indeksowania. Każdy element spoza adresu URL strony startowej jest uznawany za „poza zakresem” i nie zostanie dodany do listy.

Możesz zauważyć, że jeśli ręcznie przejdziesz do[http://IP_MASZYNY:8082/(otwiera się w nowej karcie)](http://machine_ip:8082/), w menu powinien pojawić się link kierujący do `/nospiders-gallery.php`, ale jeśli rozwiniesz listę witryn w ZAP, nie zobaczysz tego adresu URL.

![Ograniczenia pająków](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d3cc974c61c619d9d1c8ad3a105693e9.png)  

Dzieje się tak, ponieważ ten konkretny link nie jest bezpośrednio osadzony w kodzie HTML strony, ale jest generowany na bieżąco za pomocą JavaScriptu w przeglądarce (jak w wielu nowoczesnych aplikacjach). Ponieważ standardowy robot w ZAP nie obsługuje JavaScriptu, nie ma możliwości znalezienia tego linku.

Więcej pająków

Aby pokonać ograniczenia standardowego robota ZAP, ZAP może wykorzystać prawdziwą przeglądarkę, taką jak Firefox lub Chrome, do przetworzenia dowolnych skryptów dołączonych do witryny i pobrania wynikowego kodu HTML. Zamiast analizować linki bezpośrednio z odpowiedzi HTTP, będzie to robić na podstawie wyniku przetwarzania witryny przez przeglądarkę. Można to osiągnąć za pomocą **robota AJAX** .

![ZAP kontrolujący Firefoksa](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/5dd02378d74d65fd218806179a7bee7c.png)

Korzystanie z prawdziwej przeglądarki jest bardzo korzystne, ponieważ ZAP nie musi radzić sobie ze wszystkimi zawiłościami obecnych silników JavaScript, lecz deleguje to zadanie przeglądarce, gwarantując, że wynik będzie odpowiadał temu, co zobaczy użytkownik, jeśli skorzysta z tej samej przeglądarki.

Korzystanie z AJAX Spider jest podobne do korzystania ze zwykłego spidera. Wystarczy przejść do **Narzędzia -> AJAX Spider** , skonfigurować adres URL jako punkt początkowy i zaznaczyć odpowiednie opcje. Jedyną nową opcją jest wybór przeglądarki, gdzie tym razem wybierzemy Firefox. Lista przeglądarek zawiera również opcje headless, które uruchamiają wybraną przeglądarkę bez wyświetlania interfejsu graficznego. Na razie jednak trzymajmy się zwykłego Firefoksa, ponieważ ułatwia to zrozumienie działania AJAX Spidera. Konfiguracja powinna wyglądać następująco:

![AJAX Spider](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/279812c28d032528c9e21a242556a55d.png)  

Kliknijmy „Rozpocznij skanowanie”, aby to zadziałało. Powinieneś zobaczyć wyskakującego Firefoksa i nawigującego przez chwilę po witrynie. Po zakończeniu działania robota AJAX, zapełni on witryny w ZAP, tak jak zwykły robot. Ponieważ robot AJAX wykorzystuje moc Firefoksa, aby uzyskać lepsze wyniki, `/nospiders-gallery.php` na liście witryn powinieneś teraz zobaczyć…ZASTRZELIĆ.

Konfigurowanie zasad skanowania wZASTRZELIĆ

Podczas bieguDASTW przypadku narzędzi, kluczowe jest dostosowanie typów testów, które będą przeprowadzane na aplikacji. Im lepiej dopasujesz profil skanowania do swojej aplikacji internetowej, tym mniej czasu skaner będzie poświęcał na wysyłanie ładunków, które nie są istotne w konkretnym scenariuszu. PonieważDASTNarzędzia będą używane głównie w konfiguracji white box, znane są wszystkie szczegóły technologii bazowych wykorzystywanych do obsługi aplikacji. Oto szczegóły aplikacji, z której będziemy korzystać w całej sali:

- **System operacyjny:** Linux
- **Serwer WWW:** Apacz2.4
- **Język programowania:** PHP(Nie użyto żadnych frameworków)
- **Bazy danych:** Brak

Na przykład nasza aplikacja nie korzysta z bazy danych. Jeśli uruchomisz domyślny profil skanowania, skaner spróbuje wykonać następujące czynności:SQLzastrzyki, które nie miałyby sensu w tym kontekście. To wydłużyłoby czas skanowania, co może być akceptowalne w przypadku małych aplikacji, takich jak ta w tym pomieszczeniu, ale wydłużenie czasu będzie zauważalne podczas skanowania bardziej złożonych aplikacji.

Aby utworzyć lub zmodyfikować zasady skanowania wZASTRZELIĆPrzejdź do **Analyze -> Scan Policy Manager** . Kliknij przycisk Add (Dodaj), aby utworzyć nową:

![Tworzenie zasad skanowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1ac88f365d495e2e16d2c08a3b72f1f8.png)  

Tutaj możesz kontrolować typy testów, które mają być przeprowadzane w ramach Twojej polityki. Dla każdej kategorii będziesz mieć dwa parametry do skonfigurowania:

- **Próg:** Ten parametr kontroluje szczegółowość każdej kategorii. Niższy próg oznaczaZASTRZELIĆjest bardziej skłonny zgłosić lukę w zabezpieczeniach na podstawie niewielkiej ilości informacji. To pozwoliłoby Ci uzyskać więcej ustaleń, ale z ryzykiemZASTRZELIĆzgłaszaj luki, które mogą nie występować (fałszywe alarmy). Wyższy próg będzie wskazywałZASTRZELIĆzgłaszać tylko ustalenia z wysokim stopniem pewności. To da mniej wyników, ale będą one bardziej prawdopodobne do potwierdzenia. Ryzyko związane z użyciem wyższych progów polega na tym, żeZASTRZELIĆmoże nie zgłaszać niektórych luk w zabezpieczeniach, które mogą faktycznie występować (fałszywe negatywy). Możesz również ustawić próg na WYŁ., aby wyłączyć daną kategorię.
- **Siła:** Ten parametr kontroluje liczbę testów przeprowadzanych dla każdej kategorii. Wyższe poziomy siły prawdopodobnie dadzą dodatkowe wyniki, kosztem znacznego wydłużenia czasu skanowania.

Ponieważ każda aplikacja jest inna, parametry te muszą być odpowiednio dostrojone. Potraktuj to jako proces prób i błędów, który można z czasem udoskonalić.

W przypadku naszej aplikacji, ponieważ nie jest używana żadna baza danych ani żadna inna,XMLPo zakończeniu przetwarzania możemy bezpiecznie wyłączyć wszystkie powiązane testy, jak pokazano na poniższym obrazku:

![Polityka wtrysku](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/66f829c81447674a82d4471f20ee5415.png)

Pamiętaj, aby tym razem wyłączyć testy Cross Site Scripting (DOM Based), ponieważ pochłaniają one dużo zasobów i mogą spowolnić skanowanie tego pokoju: 

![Wyłączanie sprawdzania przeglądarki klienta](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/3d6bb6853578feee1cf0244963e4a666.png)  

Uruchamiamy pierwsze skanowanie

Mając już dostosowaną politykę skanowania, uruchommy skanowanie w poszukiwaniu luk w zabezpieczeniach, wybierając w menu **Narzędzia -> Aktywne skanowanie** . Możemy tu wybrać punkt początkowy z wcześniej przeszukanych zasobów i nowo utworzonej polityki skanowania. Użyjmy[http://IP_MASZYNY:8082/(otwiera się w nowej karcie)](http://machine_ip:8082/)jako punkt początkowy i zaznacz pole „Rekursja”, aby upewnić się, że wszystkie strony inne niż punkt początkowy zostaną przeskanowane. Zignorujmyodpoczynekz dostępnych opcji i kliknij **Rozpocznij skanowanie** .

![Uruchamianie skanowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/9c098496f5c0fde49e12cd2cc8dd8665.png)  

Po chwili powinniśmy zobaczyć wyniki w sekcji **Alerty** . Możesz uzyskać opis każdego z wyników, który powinien wskazywać, co zostało znalezione w ogólnych zarysach. Możesz również sprawdzić konkretne żądanie i odpowiadającą mu odpowiedź.ZASTRZELIĆSłuży do wykrywania podatności.

![Sprawdzanie alertów](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1fccaddf7d53f1d4ff346ccb3a0c5dcb.png)  

Dzięki temu możesz sprawdzić wyniki i upewnić się, że wszystkie są poprawne. Jeśli uważasz, że któryś z nich jest fałszywie dodatni, możesz go oznaczyć, klikając wynik prawym przyciskiem myszy i wybierając opcję „Oznacz jako fałszywie dodatni”.

Radzenie sobie z logowaniami

Jak dotąd przeprowadziliśmy udane skanowanie i znaleźliśmy pewne luki w zabezpieczeniach aplikacji docelowej. Nasza aplikacja nadal jednak ma luki do odkrycia. Jeśli ręcznie przejdziemy do naszej aplikacji, zobaczymy konsolę administracyjną, do której dostęp jest możliwy tylko po podaniu odpowiednich danych uwierzytelniających.ZASTRZELIĆnie zna tych danych uwierzytelniających, nie będzie w stanie sprawdzić niczego, co wymaga uwierzytelnienia.

Musimy nauczaćZASTRZELIĆJak uwierzytelnić i upewnić się, że sesja jest aktywna, aby rozwiązać ten problem. W tym celu zarejestrujemy proces uwierzytelniania w skrypcie ZEST, aby…ZASTRZELIĆMożna powtórzyć ten proces podczas skanowania. Na razie pomyśl o skrypcie ZEST jako o sposobie zapisywania i odtwarzania serii żądań.

**Uwaga:** W przypadku tego zadania należy upewnić się, że opcja jest wyłączonaZASTRZELIĆHUD z paska narzędzi. Po włączeniu niektóre funkcje nie będą działać zgodnie z oczekiwaniami. Przycisk do tego celu znajduje się na końcu paska narzędzi:

![Wyłączanie ZAP HUD](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/ff24a4999f2585c783868e9831c541e6.png)  

Nagrywanie uwierzytelniania

Aby zarejestrować uwierzytelnianie, klikamy przycisk **Zarejestruj nowy skrypt ZEST** na pasku narzędzi:

![Nagrywanie skryptów ZEST](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/e2b64ff46306fcaa73f43ef6d03f8f55.png)  

Ustawmy tytuł naszego skryptu i wybierzmy typ **„Uwierzytelnianie”.** Chcemy również ustawić prefiks dla podstawowego adresu URL naszej aplikacji, ponieważ odfiltruje to wszelkie żądania kierowane do innych witryn **:**

![Nagraj skrypt ZEST](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1010de6ca8abc4959cfb08c3038f7d16.png)  

Po kliknięciu przycisku **Rozpocznij nagrywanie** każdeHTTPprośba, która przechodziZASTRZELIĆ pełnomocnikzostanie nagrany jako część skryptu. Zróbmy to i otwórzmy przeglądarkę, klikając przycisk „ **Otwórz przeglądarkę”** na pasku narzędzi:

![Otwórz przeglądarkę Firefox z ZAP](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/0388f61af29511f725930e7276b24b65.png)  

Przejdź do[http://IP_MASZYNY:8082/login.php(otwiera się w nowej karcie)](http://machine_ip:8082/login.php)w nowo otwartej przeglądarce. Zalogujemy się do witryny ręcznie, abyZASTRZELIĆmoże nagrywać proces.

![Logowanie do witryny](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1d0b37c6177d140a7d56e54b6b34824f.png)  

Aby uzyskać dostęp do aplikacji internetowej ze strony logowania w menu, możesz użyć następujących danych logowania:

![Klucz THM](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/5d471dd234b7fc4eb4edea3c934663c1.png)

|   |   |
|---|---|
|**Nazwa użytkownika**|pająki|
|**Hasło**|pająki|

Po poprawnym zalogowaniu się do aplikacji zatrzymamy nagrywanie, klikając ponownie przycisk **„Nagraj nowy skrypt ZEST”** . Możesz zamknąć aplikację.ZASTRZELIĆPrzeglądarka również. Niektóre z przechwyconych żądań mogą nie być niezbędne do procesu uwierzytelniania i można je usunąć. W takim przypadku liczą się tylko następujące żądania:

![Nagrany skrypt uwierzytelniania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/222ed38cf31852051a655d82837c3269.png)  

Dla każdego z żądań,ZASTRZELIĆsprawdzi kod statusu i długość odpowiedzi, aby sprawdzić, czy są zgodne. Jeśli tak,ZASTRZELIĆZałożymy, że logowanie zakończyło się pomyślnie.  Możesz teraz przetestować nagrany skrypt, naciskając przycisk „ **Uruchom”** w **konsoli skryptów** :

![Odtwarzanie zarejestrowanego uwierzytelnienia](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/a9adece360ec6c218e18c19fedce7404.png)  

Powinno to pozwolić na sprawdzenie, czy proces został poprawnie zarejestrowany, poprzez sprawdzenie odpowiedzi na żądania. Nasza aplikacja powinna odpowiedzieć na żądanie POST `login.php`przekierowaniem do `cowsay.php`:

![Sprawdzanie wyniku uwierzytelniania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/3c14c45c4b8d5de40535cf43067b1407.png)  

Tworzenie kontekstu

Teraz, gdy nasz proces uwierzytelniania został zarejestrowany, musimy wskazać ZAP, gdzie ma go używać. Robi się to poprzez utworzenie **kontekstu** , który jest niczym innym jak sposobem na zdefiniowanie grupy adresów URL.

Ponieważ jest to prosta aplikacja, zarejestrowane uwierzytelnienie będzie miało zastosowanie do całej aplikacji. Musimy zatem zdefiniować kontekst obejmujący każdy adres URL w aplikacji, abyśmy mogli połączyć z nim nasz skrypt ZEST.

**Uwaga:** W zależności od aplikacji docelowej, zarejestrowane uwierzytelnienie może przyznawać dostęp tylko do części aplikacji. Wyobraźmy sobie na przykład platformę edukacyjną, na której są nauczyciele i uczniowie. Można się spodziewać, że nauczyciele i uczniowie będą mieli dostęp do różnych części aplikacji, w zależności od pełnionych ról. Aby ZAP obejmował obie strony aplikacji, musielibyśmy zarejestrować dwa skrypty uwierzytelniające ZEST (jeden dla konta ucznia i jeden dla nauczyciela) i dołączyć je do dwóch różnych kontekstów z odpowiednimi adresami URL.

Aby utworzyć nowy kontekst, przejdź do karty **Witryny** i kliknij prawym przyciskiem myszy adres URL bazy docelowej aplikacji na karcie **Witryny , a następnie wybierz opcję** **Uwzględnij w kontekście -> Nowy kontekst** :

![Tworzenie kontekstu](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/477b3e232d8941566c7bbbc1f2e50eb3.png)  

Spowoduje to automatyczne utworzenie wyrażenia regularnego pasującego do dowolnej strony w aplikacji internetowej. Istnieje wiele opcji, które można skonfigurować w kontekście. Na razie kliknij uwierzytelnianie i połącz swój skrypt Zest za pomocą **uwierzytelniania opartego na skryptach** :

![Konfiguracja uwierzytelniania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/43e47a26527ef59d5a680578be12f05b.png)  

Pamiętaj, aby kliknąć przycisk **„Załaduj”** po prawej stronie nazwy skryptu. Na tej karcie możesz również skonfigurować weryfikację uwierzytelnienia, aby ZAP mógł sprawdzić, czy ma prawidłową sesję, czy też wymaga ponownego uwierzytelnienia podczas skanowania. Zrobimy to później w prostszy sposób.

Aby przeprowadzić uwierzytelnione skanowanie, ZAP będzie również wymagał zdefiniowania co najmniej jednego użytkownika w sekcji **„Użytkownicy”** . W naszym przypadku nie będzie to w ogóle potrzebne, ponieważ nasz skrypt ZEST osadza użytkownika i hasło, których będziemy używać. Jednak ZAP wymaga zdefiniowania użytkownika, w przeciwnym razie pominie uwierzytelnianie.

![Konfiguracja użytkowników](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/1a8f38f5a68497ac2440bb108ad04fbe.png)  

Po wykonaniu tej czynności naciśnij przycisk OK, a zobaczysz, że wszystkie zasoby witryny są teraz oznaczone ikoną celu, co oznacza, że ​​stały się częścią zdefiniowanego kontekstu.

Ponowne uruchomienie aplikacji

Teraz, gdy mamy już ustawiony kontekst za pomocą skryptu uwierzytelniania, uruchommy ponownie robota, ustawiając tym razem poprawny kontekst i utworzonego użytkownika:

![Uwierzytelnione Spidering](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/36544ecae3c4accf94f905d77ce6aa71.png)  

Tym razem ZAP powinien znaleźć wszystkie zasoby wymagające uwierzytelnienia, które nie zostały wcześniej wykryte. Kliknijmy przycisk **„Rozpocznij skanowanie”** i zobaczmy, co się stanie. Jeśli chcesz sprawdzić, czy podczas sesji indeksowania wykryto jakieś nowe zasoby, zawsze możesz sprawdzić zakładkę „ **Dodane węzły”** :

![Uwierzytelnione wyniki Spider](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/ce5af212852eb375ebb04ba68c92cb85.png)  

ZAP znalazł kilka dodatkowychPHPSkrypty. Jeden z takich skryptów odpowiada za wylogowanie użytkownika i może stanowić problem. Jeśli ZAP spróbuje uzyskać do niego dostęp, wyloguje się z sesji.

Unikanie wylogowań

Aby zapobiec wylogowaniu się ZAP, należy kliknąć prawym przyciskiem myszy ikonę wylogowania.phpskrypt na karcie Witryny i wyklucz skrypt z naszego kontekstu:

![Wykluczanie wylogowania z kontekstu](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/822f88eccd14b5cae0a1b7628b19720f.png)  

ZAP będzie teraz unikał interakcji ze skryptem wylogowania podczas indeksowania lub skanowania. Należy pamiętać, że w zależności od aplikacji, może być wskazane wykluczenie również niektórych innych skryptów. Znajomość działania aplikacji jest niezwykle ważna, aby w pełni wykorzystać proces skanowania.

Oprócz zapobiegania bezpośrednim wylogowaniom, możemy określić wskaźniki dla ZAP, aby określić, czy sesja jest nadal aktywna, czy nie, i w razie potrzeby powtórzyć skrypt logowania. Można to łatwo zrobić, wybierając fragmenty odpowiedzi, które pojawiają się tylko po zalogowaniu lub wylogowaniu.

Na przykład wiemy, że `cowsay.php`dostęp do niego jest możliwy tylko po pomyślnym zalogowaniu, więc może zawierać dobre wskaźniki, których możemy użyćZASTRZELIĆWybierzmy `cowsay.php`z zakładki „Witryny” tekst odpowiadający linkowi wylogowania. Kliknij prawym przyciskiem myszy zaznaczony tekst i wybierz **„Oznacz jako kontekst” -> (Twoja nazwa kontekstu): Wskaźnik uwierzytelnienia zalogowanego:**

![Definiowanie wskaźnika zalogowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d69810f47d95da3ea83578209d03e95c.png)

Od teraz ZAP będzie szukał linku do wylogowania w każdej odpowiedzi. Jeśli go nie będzie, założy, że sesja wymaga odnowienia i zaloguje się ponownie do aplikacji za pomocą zarejestrowanego przez nas skryptu ZEST.

Możesz również zrobić to samo, aby wybrać wskaźnik „Wylogowany”. Ponieważ wiemy, że link logowania powinien być widoczny tylko po wylogowaniu, możemy go użyć w tym celu, postępując w podobny sposób. Pobierzmy kod HTML linku ze `aboutme.php` skryptu w karcie „Witryny”:

![Definiowanie wskaźnika wylogowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/e9c500784d6e3c0fa6d83dd2ac776a26.png)

Kliknij prawym przyciskiem myszy zaznaczony tekst i wybierz  opcję Oznacz jako kontekst -> (Nazwa Twojego kontekstu): Wskaźnik wylogowania uwierzytelniania.

Uwaga: Możliwe, żeZASTRZELIĆzapisał w pamięci podręcznej uwierzytelnioną odpowiedź dla `aboutme.php`. W takim przypadku należy ponownie wysłać żądanie za pomocą wbudowanej przeglądarki na ten adres URL, aby uzyskać poprawny wzorzec.

Teraz, gdy ZAP dysponuje wzorcami identyfikującymi prawidłowe logowanie, musimy wybrać  strategię weryfikacji , która wskaże mu, jak poprawnie korzystać ze skonfigurowanych wzorców. W zależności od sprawdzanej witryny, należy zastosować różne strategie i dostosować je do aplikacji docelowej. W tym przypadku użyjemy  strategii „Odpytywanie określonego adresu URL”  i polecimy mu odpytywać  `/aboutme.php` zasób co 60 żądań w celu sprawdzenia wzorców zalogowania/wylogowania. Aby to zrobić, kliknij dwukrotnie „Kontekst” i zmień następujące ustawienia w sekcji  „Uwierzytelnianie” :

![Strategia weryfikacji](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/82bf35da966f39f6a8e1d01612c41766.png)  

Ponowne skanowanie aplikacji po raz ostatni

W końcu jesteśmy gotowi do uruchomienia nowego skanowania aplikacji, wiedząc, że obejmie ono teraz obszary aplikacji wymagające uwierzytelnienia. Przejdźmy do **Narzędzia -> Aktywne skanowanie** i wybierzmy utworzony przez nas **kontekst** i **użytkownika :**

![Uwierzytelnione skanowanie](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/ab0ec48b4dc540aa44d5fce75bed3ac5.png)

Obecnie aplikacje internetowe korzystają z interfejsów API, aby wykonywać część lub całość swoich zadań.DASTProces, który pokazaliśmy do tej pory, polega na możliwości przeszukiwania tradycyjnej aplikacji internetowej, ale API nie są czymś, co można łatwo przeszukiwać. Punkty końcoweAPIZwykle nie ujawnia informacji o innych punktach końcowych, co utrudnia proces wyszukiwania. Co więcej, nawet jeśli poznamy nazwę punktu końcowego, nadal musimy wiedzieć, jakie parametry można do niego przekazać.

Zamiast przeszukiwać interfejsy API, będziemy polegać na zespole programistów, który zapewni nam dokładną specyfikację dostępnych punktów końcowych wAPIi wszystkie parametry, które możemy im przesłać. W ten sposób nie musimy tracić czasu na proces wykrywania, ale możemy skupić się bezpośrednio na testowaniu bezpieczeństwa.

APIOpisy

Istnieje kilka standardów dokumentujących interfejsy API, które zazwyczaj zawierają wszystkie informacje potrzebne programistom do tworzenia prawidłowych żądań i przewidywania odpowiedzi dla każdego z dostępnych punktów końcowych. To wszystko, czego potrzebujemy, aby rozpocząć testowanie pod kątem luk w zabezpieczeniach.

ZASTRZELIĆmoże importować interfejsy API zdefiniowane przez **OpenAPI** (dawniej **Swagger** ),**MYDŁO**lub **GraphQL** . W zależności odAPIjeśli testujesz, możesz otrzymać jeden z tych formatów od zespołu programistów.

Aby dać Ci lepsze pojęcie o tym, co zawierają te pliki, przyjrzyjmy się plikowi opublikowanemu na[http://MACHINE_IP:8081/swagger.json(otwiera się w nowej karcie)](http://machine_ip:8081/swagger.json), który jest zgodny ze standardem OpenAPI 2.0. W pliku znajduje się sekcja o nazwie `paths`, w której wymieniony jest każdy punkt końcowy API. Dla każdego z punktów końcowych prezentowana jest pełna lista dostępnych parametrów. Na przykład, tutaj znajduje się fragment specyfikacji opisujący interakcję z `/asciiart/{art_id}`:

```none
    "/asciiart/{art_id}": {
      "get": {
        "parameters": [
          {
            "description": "art id",
            "in": "path",
            "name": "art_id",
            "required": true,
            "type": "string"
          }
        ],
        "responses": {
          "default": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/ASCIIArt"
            }
          }
        }
      }
    }
```

Plik wskazuje, że można wykonywać wywołania za `/asciiart/{art_id}`pomocą metody GET, wysyłając  `art_id` parametr w adresie URL, który jest ciągiem znaków. Podobne definicje można znaleźć dla innych ścieżek, takich jak `/asciiart/generate`lub `/asciiart/add`.

APIPliki definicji mają być przetwarzane przez maszyny, więc ich format może być trudny do odczytania. Aby ułatwić nam ich zrozumienie, niektóre interfejsy API oferują również bardziej przyjazny interfejs użytkownika, który umożliwia szybkie testy i przeglądanie dostępnych punktów końcowych. Możesz przejść do[http://IP_MASZYNY:8081/swagger-ui/(otwiera się w nowej karcie)](http://machine_ip:8081/swagger-ui/)żeby to sprawdzić.

**Uwaga:** Aplikacje produkcyjne mogą się ukrywaćAPIDefinicje, aby uniemożliwić atakującym z zewnątrz poznanie sposobu interakcji z nimi. Pamiętaj, że zawsze możesz poprosić o nie zespół programistów, jeśli zajdzie taka potrzeba (o ile taki istnieje).  

Importowanie definicji OpenAPI wZASTRZELIĆ

ZASTRZELIĆobsługuje dwie metody importowaniaAPIDefinicje: możesz podać plik offline lub adres URL, z którego można go pobrać. Ponieważ naszeAPIudostępnia swój plik definicji w[http://MACHINE_IP:8081/swagger.json(otwiera się w nowej karcie)](http://machine_ip:8081/swagger.json)Użyjmy opcji URL. Przejdź do **Importuj -> Importuj definicję OpenAPI z adresu URL** . Podaj odpowiedni adres URL i kliknij przycisk **Importuj** .

![Importowanie definicji OpenAPI](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/9244ab35510e9ede17da5288dec678f1.png)  

Teraz powinieneś zobaczyć wszystkie dostępne punkty końcowe i parametry załadowane na karcie Witryny.

![Karta Witryny z punktami końcowymi API](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/c5ed878d9c4a18dabcdc7da7ecfb0c82.png)

ZASTRZELIĆautomatycznie przeprowadzi również pasywne skanowanie punktów końcowych i zgłosi pewne alerty. Po zaimportowaniuAPIdefinicja,ZASTRZELIĆbędzie leczyćAPIjak każda inna normalna strona internetowa.

SkanowanieAPI

KiedyśAPIdefinicja jest ładowana doZASTRZELIĆMożesz korzystać z dostępnych narzędzi tak samo, jak w przypadku każdej innej witryny. Aby uruchomić skanowanie,API, kliknij prawym przyciskiem myszy jego adres URL i wybierz **Atak -> Aktywne skanowanie** .

![Skanowanie API](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/88c61f3f3e892283034832da488dfa6a.png)

Po uruchomieniu skanowania,ZASTRZELIĆpowinien odkryć pewne luki w zabezpieczeniachAPI. Wykorzystaj wyniki skanowania, aby odpowiedzieć na pytania na końcu zadania.

Generalnie, podczas dyskusjiDASTLudzie będą odnosić się do wdrożenia automatycznego skanowania podatności w procesie rozwoju oprogramowania, a nie do ręcznego procesu, który omówiliśmy. W ten sposób termin ten różni się od tego, co zazwyczaj nazywa się testowaniem penetracyjnym aplikacji.

MającyDASTdodanie do procesu rozwoju może wydawać się dość proste, ale wiąże się z pewnymi zastrzeżeniami:

- Musimy zdecydować, na którym etapie procesu rozwoju przeprowadzimy skanowanie.
- Musimy zdecydować, co wywoła skanowanie. Możemy uruchamiać skanowanie po każdym zatwierdzeniu kodu lub według harmonogramu.
- Musimy określić intensywność każdego skanowania. Przeprowadzenie pełnego skanowania pod kątem luk w zabezpieczeniach aplikacji średniej wielkości zajmie dużo czasu, a nie chcemy spowalniać pracy zespołu programistów.

Ponieważ nie ma rozwiązań pasujących do wszystkich scenariuszy, ustalenie wszystkich tych kwestii musi odbywać się przy udziale zespołu programistów, tak aby spełnić wymagania bezpieczeństwa, nie powodując przy tym znaczących zakłóceń w ustalonych procesach.

W tym zadaniu sprawdzimy, jak możemy szybko wdrożyćDASTbezpośrednio do procesu rozwoju, aby zapewnić wczesną widoczność luk w zabezpieczeniach. Skanowanie będzie uruchamiane automatycznie przy każdym zatwierdzeniu i będzie testowane tylko pod kątem określonego podzbioru luk w zabezpieczeniach, aby uniknąć wprowadzania dużych opóźnień w procesie rozwoju.

Przeglądanie naszychCI/płyta CDRurociąg

Nasza obecna maszyna implementuje cały proces rozwoju aplikacji internetowej iAPIzeskanowałeś wcześniej. Za to odpowiadają następujące dwa komponenty:

- Repozytorium Gitea jest uruchomione na[http://IP_MASZYNY:3000/(otwiera się w nowej karcie)](http://machine_ip:3000/), w którym przechowywany jest kod obu aplikacji.
- AJenkinsinstancja, która uruchamiaCI/płyta CDrurociągu. Możesz uzyskać dostępJenkinsNa[http://IP_MASZYNY:8080/(otwiera się w nowej karcie)](http://machine_ip:8080/).

Za każdym razem, gdy w Gitea zostanie dokonane zatwierdzenie,Jenkinspobierze kod z repozytorium i skompiluje go do instancji Dockera. Te instancje Dockera zostały już przeskanowane. 

![Proces CI/CD w akcji](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/2cb91a58ca81963c65e2cc15c7d320d8.png)  

Aby uzyskać dostęp do Gitea lubJenkins, możesz użyć następujących danych logowania:

![Klucz THM](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/5d471dd234b7fc4eb4edea3c934663c1.png)

|   |   |
|---|---|
|**Nazwa użytkownika**|thm|
|**Hasło**|thm|

Uruchamianie automatycznych skanów za pomocą zap2docker

ZintegrowaćZASTRZELIĆw naszym procesie będziemy używać **zap2docker** , zdokeryzowanej wersjiZASTRZELIĆ pełnomocnikZbudowany z myślą o automatyzacji jako głównym celu. Pełną dokumentację zap2docker można znaleźć [tutaj.(otwiera się w nowej karcie)](https://www.zaproxy.org/docs/docker/).

**Uwaga:** Polecenia w tej sekcji służą wyłącznie celom informacyjnym. Nie musisz ich uruchamiać ręcznie, ponieważ…Jenkinszrób to dla nas później.

Aby zainstalować zap2docker, możesz go pobrać z Docker Hub za pomocą następującego polecenia:

```none
docker pull owasp/zap2docker-stable
```

Możesz uruchomić ZAP z instancji Dockera, korzystając z jednego ze spakowanych skryptów skanowania, które umożliwią Ci uruchomienie jednego z następujących profili skanowania:  

**Skanowanie bazowe:** ZAP będzie skanować docelową witrynę przez maksymalnie 1 minutę. Nie zostanie przeprowadzone żadne aktywne skanowanie. Opcjonalnie można uruchomić skanowanie AJAX, jeśli zajdzie taka potrzeba.

```none
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://www.example.com
```

**Pełne skanowanie:** ZASTRZELIĆuruchomi pająka bez ograniczeń czasowych, po czym nastąpi aktywne skanowanie.

```none
docker run -t owasp/zap2docker-stable zap-full-scan.py -t https://www.example.com
```

**Skanowanie API:** ZASTRZELIĆWykona aktywne skanowanie interfejsu API. Konieczne będzie podanie adresu URL pliku opisu interfejsu API (OpenAPI, GraphQL lub SOAP).  

```none
docker run -t owasp/zap2docker-stable zap-api-scan.py -t https://www.example.com/swagger.json -f openapi
```

W każdym ze skanowań wyniki skanowania pasywnego będą ograniczone do 10 alertów. Oprócz poleceń bazowych można dodać przełącznik `-j`, aby wykonać skanowanie AJAX w skanowaniu bazowym i pełnym.

Integracja ZAP z rurociągiem

Środowisko, do którego masz dostęp, ma już gotową do użycia instancję zap2docker. Wystarczy, że polecimy Jenkinsowi uruchomienie zap2dockera z potrzebnymi opcjami i to wszystko.

Zanim przejdziemy do konkretów, przyjrzyjmy się bliżej temu, co mamy w Jenkinsie. Po zalogowaniu się do Jenkinsa znajdziesz **organizację** o nazwie thm, która zawiera dwa **repozytoria** dla aplikacji webowej i API. Dla każdego z repozytoriów możesz zobaczyć dostępne **gałęzie** . 

![Organizacja, repozytoria i oddziały](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/573d790980b009dc97643c03e6357207.png)  

W obu projektach będziesz mieć jedną gałąź o nazwie `main`. Klikając na gałąź, zobaczysz jej kompilacje. Projekt `simple-webapp`, na przykład, został już skompilowany dwa razy:  

![Kompilacje Jenkinsa](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/49813ba174a02e86bd73d39ec73d1c82.png)  

Dla każdej kompilacji możemy zobaczyć, że skonfigurowano dwa etapy:  

- **Zbuduj obraz Dockera:** Na tym etapie zostanie zbudowany kontener Dockera w oparciu o plik Dockerfile dla każdego projektu.
- **Wdrażanie obrazu Docker:** Na tym etapie zostanie wdrożony kontener Docker.

Oba te etapy są zdefiniowane w pliku **Jenkinsfile** w każdym repozytorium. Jeśli przejdziemy do Gitea i otworzymy plik [Jenkinsfile,(otwiera się w nowej karcie)](http://machine_ip:3000/thm/simple-webapp/src/branch/main/Jenkinsfile)w repozytorium simple-webapp możemy zobaczyć konkretne polecenia uruchamiane na każdym z etapów:

![Przykład Jenkinsfile](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/cf141221964b4306947780a09c1f5ef3.png)  

Na drugim etapie możesz zobaczyć na przykład, jak ręcznie przeskanowana aplikacja internetowa jest wdrażana na porcie 8082.

Jeśli chcemy włączyć zap2docker do naszego potoku, możemy dodać trzeci etap, który uruchomi skanowanie po zbudowaniu kontenera. Dla wygody etap jest już zdefiniowany na końcu pliku Jenkinsfile i można go odkomentować, aby go uruchomić. Możesz użyć tego polecenia, `git`aby wysłać commit do repozytorium lub skorzystać z wbudowanego edytora Gitea, jeśli wolisz:

![Edycja pliku Jenkinsfile z Gitea](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/edc92bcb8a4db9cc674e9dc6dcbf887d.png)  

Należy pamiętać, że uruchamiamy tylko **skanowanie bazowe** , ponieważ będzie ono uruchamiane dla każdego zatwierdzenia w repozytorium. Dlatego nie ma sensu opóźniać procesu skanowania pełnym skanowaniem, którego ukończenie może zająć kilka godzin. Celem tego skanowania jest znalezienie tylko najłatwiej dostępnych rozwiązań. Oznacza to, że nie zobaczysz żadnych ataków typu SQL injection, Cross Site Scripting ani niczego innego, co wymagałoby aktywnego skanowania. 

OdJenkinsPrzechwycą wszelkie zmiany w repozytorium i rozpoczną proces kompilacji natychmiast po edycji pliku. Możesz wrócić do projektu simple-webapp wJenkinsaby zobaczyć postęp na żywo:

 ![Zbuduj z ZAP Stage](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/66397388a1c813a454cb7622db12e884.png)

Jak widać, bieżąca kompilacja dodaje teraz `Scan with OWASP ZAP`etap. Skanowanie potrwa około 5 minut. Po zakończeniu kompilacja zakończy się niepowodzeniem, ponieważZASTRZELIĆZnajdzie pewne luki w zabezpieczeniach aplikacji. Aby sprawdzić raport, otwórz kompilację i przejdź do sekcji **„Obszary robocze”** w menu:  

![Kompilacja nie powiodła się z powodu luk w zabezpieczeniach](https://tryhackme-images.s3.amazonaws.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d91ad74b7900ca2039e91711852c09b2.png)  

Tutaj możesz przeglądać pliki projektu iZASTRZELIĆumieści swoje raporty wzastrzelić-folder raportów. Pobierz i przejrzyj raport, aby odpowiedzieć na pytanie na końcu zadania.

**Uwaga:** Przed otwarciem raportu należy kliknąć go prawym przyciskiem myszy i zapisać. Otwieranie bezpośrednio zJenkinsspowoduje uszkodzenie formatowania.

Powtórz ten sam proces, aby włączyćZASTRZELIĆna prostym-APIrepozytorium i pobierz odpowiedni raport. Użyj raportu, aby odpowiedzieć na pytania na końcu tego zadania.

W tym pokoju omówiliśmy podstawy tego, jakDASTdziała i wprowadziłZASTRZELIĆ pełnomocnikjako narzędzie, które może wykonaćDASTw sposób ręczny i zautomatyzowany.DASTjest tylko jednym z wielu sposobów sprawdzania luk w zabezpieczeniach aplikacji i powinien być stosowany w połączeniu z innymi typami testów, takimi jakSAST,SCA, testy penetracyjne i inne, aby zagwarantować rozsądny poziom bezpieczeństwa naszych aplikacji. Jak w przypadku każdej innej techniki,DASTnie będzie rozwiązaniem idealnym, ale przyczyni się do ogólnego bezpieczeństwa aplikacji w całym cyklu rozwoju oprogramowania.
