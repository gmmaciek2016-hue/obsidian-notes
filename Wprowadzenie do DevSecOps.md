---

W tym laboratorium zapoznasz się z różnymi stylami rozwoju oprogramowania i ich ewolucją na przestrzeni lat. Kluczowe jest zrozumienie, jak zmieniały się one na przestrzeni lat i jaki wpływ miały na branżę bezpieczeństwa. 

**Cele edukacyjne**

- Historia praktyk związanych z tworzeniem oprogramowania i ich ewolucja na przestrzeni lat  
    
- Znaczenie tej dziedziny i koncepcje tego, co ją tworzyDevSecOps
- DevSecOpskultura i jako dyscyplina  

DevSecOpsŚcieżka nauki

﻿To pierwszy pokój w nowymDevSecOpsścieżka edukacyjna w trakcie opracowywania. Nowa ścieżka obejmie:

- Wprowadzenie doDevSecOps(BezpiecznySDLC, Środowiska i Narzędzia)
- Bezpieczeństwo potoku (automatyzacja potoku, bezpieczeństwo kodu źródłowego, automatyczne testowanie kodu, zarządzanie zależnościami,CI/płyta CDi Bezpieczeństwa Środowiska)
- Bezpieczeństwo rurociągu (atakowanie rurociągu, wykorzystywanie luk w zabezpieczeniach rurociągu, obrona rurociągu)
- Infrastruktura jako kod (chmura)DevOps, Secret Management, Wykorzystywanie Terraform, Wykorzystywanie Vagrant, Wykorzystywanie Dockera)

Od początku swojego istnienia, Dział Operacji Deweloperskich (DevOps) stał się znaczącym czynnikiem we współczesnym rozwoju oprogramowania, wdrażaniu i operacjach. Skąd jednak wzięło się to określenie?  

---

**Historia DevOps**

Dawno, dawno temu, w odległej galaktyce, istniały wodospady.

**Model wodospadu**  

Tak nazywano podejście do zarządzania projektami w dawnych czasach (lata 70.). Cykl ten opierał się na _hierarchii,_ w której każdy członek zespołu miał przypisane określone obowiązki. Na przykład, administratorzy systemu pracowali niestrudzenie, aby wszystko działało sprawnie i bez zakłóceń. Programiści tworzyli i dodawali jak najwięcej funkcji, a na koniec inżynierowie ds. zapewnienia jakości (QA) testowali funkcjonalność systemu, upewniając się, że wszystko działa zgodnie z oczekiwaniami. 

![Diagram etapów modelu kaskadowego rozwoju oprogramowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/21ff900651b19689600a2a7d0cd2fcea.png)  

Jeśli coś będzie przeszkadzać serwerom lub będzie wymagało wdrożenia, administratorzy systemów się tym zajmą. Jeśli problem będzie dotyczył kodu, programiści ugaszą pożar. Jeśli będzie to miało związek z testowaniem funkcjonalności i zbieraniem opinii, zespoły ds. zapewnienia jakości się tym zajmą. Ale co, jeśli pojawi się wada? Błąd? Kto go naprawi? Takie sytuacje prowadziły do ​​wielu gier oskarżających i przekazywania pałeczki, co powodowało tarcia, zalegały prace, a symbioza między zespołami przestawała działać. Wraz ze wzrostem oczekiwań klientów rosła liczba funkcji i nowych wydań. Obowiązki i zadania kończyły się kumulacją, gigantycznym bałaganem. Błędy i luki w zabezpieczeniach były zaległe, wiele z nich nierozwiązanych, a kolejne zaplanowane wydania były nieskalowalne i chaotyczne. Nadmierny hałas i presja prowadziły do ​​braku zaufania, luk w komunikacji i tarć między zespołami.

Ta popularna strategia i system rozwiązywania problemów stały się główną przyczyną nieskuteczności elastyczności i komunikacji w zespołach.

**Model zwinny  
**

W obliczu wyzwań, z jakimi zespoły mierzyły się w modelu kaskadowym, firmy zaczęły opracowywać metody zapewniające większą elastyczność i adaptacyjność. Gdzieś na początku 2000 roku   powstała **metodyka Agile** . Wkrótce potem opublikowano manifest:  [Agile Manifesto .(otwiera się w nowej karcie)](http://agilemanifesto.org/), podkreślając cztery wartości zwinnego rozwoju:

![Diagram etapów modelu Agile Software Development](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/db09323bd5eed6fb32de796bdb20196f.png)  

-  Jednostki i interakcje ponad procesami i narzędziami
-  Działające oprogramowanie ponad obszerną dokumentacją
-  Współpraca z klientem ponad negocjacjami kontraktowymi
-  Reagowanie na zmiany a podążanie za planem

Firmy cenią sobie obecnie współpracę zespołową i opierają się na samoorganizujących się zespołach, które koncentrują się na klientach, a także mają duże możliwości wprowadzania zmian i zapewniają dużą elastyczność.

Ale czegoś nadal brakowało.  

**DevOps:Nowa nadzieja**

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/c31ab1829b8c9ef8850f90e38a4224f6.png)

W 2008 roku rozmowa Andrew Claya i Patricka Debois doprowadziła do czegoś rewolucyjnego. Dyskutując o wadach Agile,DevOpsnarodził się. Po wydarzeniu w Belgii w następnym roku o nazwie „DevOpsDays”,DevOpsstało się kolejnym modnym słowem i jego popularność wzrosła.

DevOpsMetoda ta znacznie różni się od poprzednich, ponieważ koncentruje się na napędzaniu „zmiany kulturowej” w celu zwiększenia wydajności. Osiąga to poprzez połączenie magii wszystkich zespołów pracujących nad projektem, wykorzystując integrację i automatyzację. Dzięki tym składnikom uzyskuje się integrację krzyżową między wszystkimi działami, działem zapewnienia jakości, administratorami systemów i programistami. Na przykład, programiści mogą teraz uczestniczyć we wdrażaniu, a administratorzy systemów pisać skrypty, a dział zapewnienia jakości może znaleźć sposób na naprawienie błędów, zamiast ciągłego testowania funkcjonalności. Dzięki wprowadzeniu automatyzacji i integracji systemów, inżynierowie ci mają teraz stały wgląd w sytuację i mogą odpowiednio współpracować. Zagłębimy się w to, jak…DevOpsrobi to w ostatnich pokojach, o których mówimyrurociągi, automatyzacja, ciągła integracja i ciągłe dostarczanie (CI/płyta CD).

Dlaczego jest DevOps ważny?

DevOpsbuduje filozofię, która kładzie nacisk na budowanie zaufania i lepszą współpracę między programistami a innymi zespołami (administratorami systemów, działem kontroli jakości itp.). Pomaga to organizacji dostosować projekty technologiczne do wymagań biznesowych, zwiększając ich wpływ i wartość dla firmy, ponieważ projekty stają się bardziej wydajne i odpowiednio priorytetyzowane. Wprowadzane zmiany są zazwyczaj niewielkie i odwracalne, widoczne dla wszystkich zaangażowanych zespołów. Zapewnia to lepszy wkład i komunikację, co pomaga w utrzymaniu tempa i zwiększa kompetencje podczas realizacji zadań.  

﻿Podsumowując:  

Dzięki nadejściuDevOpsdzisiejsza infrastruktura rozwojowa jest w pełni zautomatyzowana i działa w oparciu o samoobsługę:

- Deweloperzy mogą udostępniać zasoby chmurom publicznym bez konieczności polegania na dziale IT w zakresie zapewniania infrastruktury, co w przeszłości prowadziło do opóźnień trwających tygodnie lub miesiące.  
    
- Ciągła integracja i wdrażanie (CI/płyta CD) automatycznie konfigurują środowiska testowe, przejściowe i produkcyjne w chmurze lub lokalnie. Można je wycofywać z eksploatacji, skalować lub rekonfigurować w zależności od potrzeb.  
    
- Infrastruktura jako kod (IaC) jest powszechnie stosowana do deklaratywnego* wdrażania środowisk przy użyciu narzędzi takich jak Terraform i Vagrant.  
    
- Organizacje mogą teraz dynamicznie dostarczać konteneryzowane obciążenia robocze za pomocą zautomatyzowanych, adaptacyjnych procesów

*Podejście deklaratywne wymaga od użytkowników określenia stanu końcowego infrastruktury – na przykład wdrożenia tych maszyn w stanie uruchomionym bezpośrednio w środowisku, automatyzując wybory konfiguracyjne w całym procesie pracy. Oprogramowanie tworzy je i udostępnia bez ingerencji człowieka.

Podejście imperatywne/proceduralne polega na konfigurowaniu systemów w serii możliwych do wykonania kroków. Na przykład, można zadeklarować wdrożenie nowej wersji oprogramowania i zautomatyzować szereg kroków, aby uzyskać stan gotowości do wdrożenia. Wybór momentu zastosowania tych zmian następuje na końcu, poprzez dodanie „bramki”. Bramka ta może być przyciskiem do zwalniania zmian, np. „Wdrażaj zmiany”, po pomyślnym zakończeniu wszystkich automatycznych sprawdzeń i wprowadzeniu nowych konfiguracji.

W takim przepływie pracy nawet drobny problem może narobić bałaganu. Co więcej, wraz ze wzrostem liczby nowych wydań (co jest faktem), cała sprawa może przerodzić się w katastrofę. Sytuacja z pewnością wymknęłaby się spod kontroli, gdyby problem pozostał nierozwiązany, a wiele funkcji miało zostać wydanych.

Przeczytaj więcej na: [https://www.appknox.com/blog/history-of-DevOps](https://www.appknox.com/blog/history-of-devops)

W poprzednim zadaniu poznaliśmy różne style tworzenia oprogramowania na przestrzeni lat i ich ważną rolę w  powstaniu DevOps To zadanie wprowadzi Cię w kluczowe koncepcje, narzędzia i sposób ich współdziałania.

Jak to działa? DevOps praca?

DevOps jest wizualizowany jako nieskończona pętla, opisująca wszystkie składające się na nią fazy:

![diagram pętli nieskończonej opisujący cykl życia DevOps](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/538ad9f777ec0153d5d648edd4bcf65a.png)

Podążając za nieskończoną pętlą DevOpsdiagram, rozszerzmy go o kilka DevOps narzędzia i procesy, które będziemy analizować, postępując zgodnie z DevSecOps ścieżki i jak pomagają organizacji:

1. **CI/płyta CD**– W poprzednim zadaniu wspomnieliśmyCI/płyta CD(Ciągła integracja i ciągłe wdrażanie);CI/płyta CDZajmuje się częstym scalaniem kodu i dodawaniem testów w sposób zautomatyzowany, aby przeprowadzać kontrole w miarę wgrywania i scalania nowego kodu. Możemy testować kod w trakcie wgrywania i scalania dzięki nowej dynamice i procedurze wdrażania, która przyjmuje formę drobnych zmian w kodzie systematycznie i rutynowo. Dzięki tej zmianie dynamiki,CI/płyta CDpomaga wykrywać błędy na wczesnym etapie i zmniejsza nakład pracy związany z utrzymaniem modułowego kodu na dużą skalę, co umożliwia niezawodne wycofywanie wersji/kodu.
2. **INFRASTRUKTURA JAKO KOD** (IaC) – sposób zarządzania i udostępniania infrastruktury za pomocą kodu i automatyzacji. Dzięki temu podejściu możemy ponownie wykorzystać kod używany do wdrażania infrastruktury (na przykład instancji w chmurze), co pomaga w spójnym tworzeniu i zarządzaniu zasobami. Standardowymi narzędziami IaC są Terraform, Vagrant itp. Będziemy z nich korzystać w dalszej części kursu, eksperymentując z bezpieczeństwem IaC. 
3. **ZARZĄDZANIE KONFIGURACJĄ** – W tym miejscu stan infrastruktury jest stale zarządzany, a zmiany są skutecznie wprowadzane, co ułatwia jej utrzymanie. Dzięki temu oszczędza się mnóstwo czasu i zyskuje się lepszy wgląd w konfigurację infrastruktury. Do zarządzania konfiguracją można wykorzystać IaC.
4. **ORKIESTRACJA** – Orkiestracja to automatyzacja przepływów pracy. Pomaga osiągnąć stabilność; na przykład, automatyzując planowanie zasobów, możemy szybko reagować w przypadku wystąpienia problemu (np. niepowodzenia kontroli stanu); jest to możliwe dzięki monitorowaniu.
5. **MONITORING** – koncentruje się na gromadzeniu danych o wydajności i stabilności usług oraz infrastruktury. Umożliwia to szybsze odzyskiwanie danych, poprawia widoczność międzyzespołową, dostarcza więcej danych do analizy w celu lepszej analizy przyczyn źródłowych, a także generuje automatyczną odpowiedź, jak wspomniano wcześniej.
6. **MIKROUSŁUGI** – Architektura, która dzieli aplikację na wiele małych usług. Ma to kilka zalet, takich jak elastyczność w razie potrzeby skalowania, mniejsza złożoność i więcej opcji wyboru technologii w ramach mikrousług. Przyjrzymy się temu bardziej szczegółowo w dalszej części. DevSecOps ścieżka.

Wstęp Przesunięcie w Lewo

Bezpieczeństwo można teraz łatwo zintegrować dzięki widoczności i elastyczności, DevOps wprowadza. Być może słyszałeś o koncepcji „przesunięcia w lewo”. Oznacza to, że  DevOps Zespoły skupiają się na wdrażaniu zasad bezpieczeństwa już na najwcześniejszych etapach cyklu rozwoju oprogramowania oraz wprowadzaniu kultury współpracy między działem rozwoju oprogramowania a działem bezpieczeństwa.

Dzięki możliwości wczesnego wdrażania zabezpieczeń ryzyko jest teraz znacznie ograniczone. W przeszłości luki w zabezpieczeniach i błędy były wykrywane na bardzo późnych etapach, nawet w fazie produkcyjnej. Prowadziło to do stresu, wycofań i strat ekonomicznych. Integracja narzędzi do analizy kodu i testów automatycznych na wcześniejszym etapie procesu pozwala teraz na identyfikację tych luk w zabezpieczeniach już na wczesnym etapie rozwoju.

Przesunięcie w lewo

W przeszłości testy bezpieczeństwa wdrażano pod koniec cyklu rozwoju oprogramowania. Wraz z rozwojem branży i wprowadzaniem funkcji bezpieczeństwa, zespoły ds. bezpieczeństwa przeprowadzały różne analizy i testy bezpieczeństwa na końcowych etapach cyklu życia. 

W zależności od wyników testów bezpieczeństwa, aplikacja albo zezwalała na wdrożenie do produkcji, albo odrzucała ją i odsyłała do programistów w celu usunięcia zidentyfikowanych błędów. Powodowało to długie opóźnienia w rozwoju i tarcia między zespołami.  

Wdrażanie środków bezpieczeństwa na wszystkich etapach cyklu rozwoju oprogramowania (przesunięcie w lewo), a nie na jego końcu, gwarantuje, że oprogramowanie będzie projektowane z uwzględnieniem najlepszych praktyk bezpieczeństwa. Wykrywanie luk w zabezpieczeniach na wczesnym etapie rozwoju obniża koszty ich usuwania i eliminuje konieczność wycofywania zmian, ponieważ są one naprawiane na czas. To obniża koszty, buduje zaufanie oraz poprawia bezpieczeństwo i jakość produktu.  

Dlaczego przesuwamy się w lewo

Dawniej, przed wprowadzeniem metodyki Agile, programiści zamawiali infrastrukturę od działu IT i otrzymywali serwery po tygodniach lub miesiącach. Obecnie dostarczanie infrastruktury w chmurze jest zautomatyzowane.  Ta zmiana poprawiła produktywność i szybkość rozwoju oprogramowania. Jednak ta zwiększona prędkość może również budzić obawy dotyczące bezpieczeństwa i prowadzić do luk, które mogą pozostać niezauważone. 

![Korzyści z przesunięcia w lewo](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/2078c48d1463aaf4245f2ed0d1175cab.png)

Podejście Shift-Left gwarantuje wczesne wykrycie tych wad poprzez wdrożenie procesów od samego początku. W tym dynamicznym środowisku, przeglądy bezpieczeństwa nowych wersji oprogramowania po ich wdrożeniu lub analiza konfiguracji infrastruktury chmurowej stają się wąskim gardłem. Nawet po wykryciu problemów, brakuje czasu na ich rozwiązanie przed wprowadzeniem kolejnej wersji lub funkcji. Aby sprostać potrzebom klientów, potrzebują oni dynamicznego środowiska do skalowania i rozwoju. Istnieje ryzyko, że bezpieczeństwo pozostanie w tyle; wdrożenie zabezpieczeń na samym początku i dostosowanie testów bezpieczeństwa do cyklu rozwoju oprogramowania zwiększa szanse na szybkie reagowanie na problemy.

To podejście rozwojowe do przesunięcia w lewo DevOps można nazwać **DevSecOps.**

Tak, dobrze słyszałeś. Z DevOps Bezpieczeństwo jest wdrażane na wczesnym etapie cyklu rozwoju, co znacząco minimalizuje ryzyko. Wcześniejsza integracja narzędzi do analizy kodu i testów automatycznych może prowadzić do lepszej identyfikacji i eliminacji luk w zabezpieczeniach. A gdy oprogramowanie dociera do etapu wdrożenia, wszystko działa płynnie, zgodnie z oczekiwaniami. Bezpieczeństwo nie jest dodatkiem. To niezbędna funkcja projektowa. Łączenie bezpieczeństwa z…DevOps wzmocniłoby wpływ DevOpsi wyeliminować wiele innych wąskich gardeł, które mogłyby się pojawić w przeciwnym razie. Wraz ze wzrostem częstotliwości cyberzagrożeń i zaostrzeniem przepisów, dodanie zabezpieczeń do DevOps Nie jest to już wybór, ale z pewnością obowiązek.  
Czytaj więcej na: [https://www.appknox.com/blog/history-of-DevOps(otwiera się w nowej karcie)](https://www.appknox.com/blog/history-of-devops)

DevSecOps:Bezpieczeństwo kontratakuje

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/61a7523c029d1c004fac97b3/room-content/f008fcb933365fa95cc2f9acfa8ef443.png)  

DevSecOps To podejście, które w dużej mierze opiera się na automatyzacji i projektowaniu platformy, integrując bezpieczeństwo jako wspólną odpowiedzialność. To styl rozwoju uwarunkowany kulturowo, który normalizuje bezpieczeństwo jako codzienną czynność.

Jaka jest wartość?  

DevSecOpsPomaga eliminować luki w zabezpieczeniach, maksymalizuje zakres testów i intensyfikuje automatyzację struktur bezpieczeństwa. To znacząco zmniejsza ryzyko, pomagając organizacjom zapobiegać utracie reputacji marki i stratom ekonomicznym spowodowanym incydentami związanymi z lukami w zabezpieczeniach, ułatwiając audyt i monitorowanie.

Jak wdrożyć to efektywnie?

Kultura jest kluczowa. Nie działa bez otwartej komunikacji i zaufania. Działa tylko dzięki wspólnemu wysiłkowi.DevSecOpspowinniśmy dążyć do zniwelowania luk w wiedzy na temat bezpieczeństwa między zespołami; aby każdy mógł myśleć i brać odpowiedzialność za bezpieczeństwo, najpierw trzeba wyposażyć zespoły w narzędzia i wiedzę, które pozwolą na efektywne i pewne zarządzanie tą autonomią.  

DevSecOpsWyzwania  

**Silosy bezpieczeństwa**

Często zdarza się, że wiele zespołów ds. bezpieczeństwa zostaje pominiętychDevOpsprocesy i przedstawiają bezpieczeństwo jako odrębną jednostkę, w której wyspecjalizowane osoby mogą jedynie utrzymywać i zarządzać praktykami bezpieczeństwa. Taka sytuacja tworzy wyizolowaną strukturę wokół bezpieczeństwa i uniemożliwia inżynierom zrozumienie potrzeby bezpieczeństwa lub stosowania środków bezpieczeństwa od samego początku.

To nie jest skalowalne ani elastyczne. Bezpieczeństwo powinno być funkcją wspierającą, pomagającą innym zespołom skalować i budować bezpieczeństwo, bez blokowania zespołów bezpieczeństwa, a raczej jako punkt wyjścia do promowania bezpiecznych rozwiązań i decyzji. Najlepszą praktyką jest dzielenie się tymi obowiązkami między wszystkich członków zespołu, zamiast zatrudniania wyspecjalizowanego inżyniera ds. bezpieczeństwa.

**Brak widoczności i priorytetyzacji**  

Dążymy do stworzenia kultury, w której bezpieczeństwo i inne istotne komponenty aplikacji traktują bezpieczeństwo jako stały aspekt aplikacji. Dzięki temu programiści mogą skupić się na rozwoju oprogramowania, mając pewność co do bezpieczeństwa, zamiast aby działy bezpieczeństwa odgrywały rolę policjantów i szukały winnych. Należy budować zaufanie między zespołami, a bezpieczeństwo powinno promować ich autonomię poprzez ustanowienie procesów, które je wdrażają.

**Surowe procesy**

Żaden nowy eksperyment ani oprogramowanie nie musi przechodzić skomplikowanego procesu i weryfikacji zgodności z wymogami bezpieczeństwa przed ich wykorzystaniem przez programistów. Procedury powinny być elastyczne, aby uwzględniać takie scenariusze, w których zadania niższego poziomu powinny być traktowane inaczej, a zadania i zmiany o wyższym ryzyku są ukierunkowane na te bardziej rygorystyczne procesy.  

Programiści potrzebują środowisk do testowania nowego oprogramowania bez typowych ograniczeń bezpieczeństwa. Środowiska te są znane jako „Piaskownica”, które są tymczasowo odizolowanymi środowiskami. Środowiska te nie mają połączenia z żadną siecią wewnętrzną i nie zawierają danych klientów.

**DevSecOpsKultura**  
  
Promuj autonomię zespołów Niezależnie  
  
od tego, czy jest to duża organizacja, czy start-up o hiperwzroście, jedynym sposobem, aby nie pozostawić bezpieczeństwa w tyle, jest promowanie autonomii zespołów. Można to zrobić, automatyzując procesy, które płynnie wpasowują się w proces rozwoju, dopóki testy bezpieczeństwa nie staną się po prostu kolejnym rodzajem testów, takim jak testy jednostkowe, bomby dymne itp.  
  
Dając przykład i promując edukację, taką jak tworzenie playbooków/runbooków, aby wykryć te wady i je naprawić, zrozumieć ich ryzyko i zbudować zaufanie inżynierów do samodzielnego podejmowania bezpiecznych decyzji. Proporcje programistów, platformy, inżynierów infrastruktury itp. nie będą takie same jak inżynierów bezpieczeństwa i musimy zrozumieć, że nie mogą oni być w każdej rozmowie. Bezpieczeństwo powinno działać jako funkcja wspomagająca, która koncentruje się na budowaniu zaufania i tworzeniu jak największego nakładania się wiedzy między zespołami.  
  
Widoczność i przejrzystość  
  
Dla każdego wprowadzanego lub praktykowanego narzędzia musi istnieć proces wspomagający, który zapewnia widoczność i promuje przejrzystość dla innych zespołów. Oznacza to, że jeśli chcemy budować autonomię w grupach, jak wspomniano wcześniej, muszą one mieć wgląd w stan bezpieczeństwa usługi, której są właścicielami lub którą utrzymują. Na przykład, pulpit nawigacyjny wizualizuje liczbę luk w zabezpieczeniach według krytyczności usługi. Pomaga to odpowiednio priorytetyzować zadania, aby nie gubiły się w zaległościach lub szumie informacyjnym, a zespoły mogły zająć się lukami we właściwym czasie. Miara stanu bezpieczeństwa zależy od firmy, ale może nią być liczba istotnych ustaleń, które usługa może lub nie może mieć, decydująca o tym, czy jest ona w dobrym stanie bezpieczeństwa.  
  
Przejrzystość odnosiłaby się do wprowadzania narzędzi i praktyk dostępnych dla zespołów. Na przykład, jeśli przed scaleniem kodu przedstawisz sprawdzenie, a przegląd nie przejdzie i wyświetli komunikat „Wykryto sygnaturę potencjalnego błędu w postaci wstrzyknięcia kodu, proszę go naprawić”, programista lub inżynier powinien mieć dostęp do narzędzia, które sygnalizuje ten komunikat. Zazwyczaj narzędzia analityczne sygnalizujące te alerty mają interfejs użytkownika, który określa wiersz kodu, którego dotyczy problem. Zawierają one definicję i sugestię naprawy wraz z krokami. W tym przykładzie można utworzyć rolę programisty, aby zapewnić mu dostęp do większej ilości informacji. Promuje to edukację i autonomię poprzez zwiększenie przejrzystości, która tradycyjnie była dostępna tylko dla zespołów ds. bezpieczeństwa.  

Należy uwzględnić elastyczność dzięki zrozumieniu i empatii.  
  
﻿Jak wspomniano wcześniej, wpajanie bezpieczeństwaDevOpsProcesy z widocznością i transparentnością nie są łatwym zadaniem. Istnieje czynnik, który może decydować o sukcesie: poziom zrozumienia i empatii. Oznacza to, że definicja ryzyka dla zespołów ds. bezpieczeństwa jest jednoznaczna, ale dla innych zespołów ryzyko może być inne i równie precyzyjne. Dotyczy to nie tylko ryzyka, ale całego spektrum rzeczy; przekłada się to na to, co traktują priorytetowo, jak pracują i co uważają za wystarczająco ważne, aby odrzucić projekt z krótkim terminem naprawy błędu.  
  
Nie ma magicznego narzędzia ani procesu dla wszystkich. Niezbędne jest zrozumienie, jak pracują programiści/inżynierowie, co uznają za ryzyko i co traktują priorytetowo. Znając ich perspektywę, łatwiej jest zbudować proces, który znajdzie wspólny język i ma większe szanse na powodzenie, niż dodawać kolejne narzędzie, które generuje więcej hałasu i stresu dla wszystkich. To zrozumienie buduje perspektywę, która uwzględnia empatię dla sposobu pracy innych zespołów i buduje proces, który zapewnia elastyczność. Jest to konieczne, ponieważ każda sytuacja może być inna, terminy mogą być różne, a przepustowość może się zmieniać w czasie.  
  
JakoDevSecOpsInżynierze, załóżmy, że poświęciłeś czas na zrozumienie, jak zespół zarządza usługą. W takim przypadku do procesu rozwoju zostanie dodany skaner bezpieczeństwa, który będzie działał i będzie miał priorytet w przeglądaniu; łatwiej będzie uzyskać ich akceptację i wykazać wartość. Na przykład, jeśli jest to zespół platformowy i posiada usługę wewnętrzną, ale podstawową, ryzykiem będzie błąd zakłócający działanie usługi, a nie potencjalny atak, który znajduje się za…pełnomocnikPotrzebne byłyby wewnętrzne uprawnienia, aby to wykorzystać. Możesz dostroić skanery lub dodać proces triażu, który zajmie się pytaniami, które same sobie zadadzą, a to z kolei zbuduje zaufanie, zapobiegając podważaniu bezpieczeństwa i podważaniu procedur bezpieczeństwa.﻿

Przeczytaj oDevSecOpshistorie sukcesu [tutaj(otwiera się w nowej karcie)](https://www.csoonline.com/article/3439737/3-devsecops-success-stories.html).
