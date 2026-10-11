---

**Wstęp**  

W tym laboratorium zapoznasz się z różnymi stylami rozwoju oprogramowania i ich ewolucją na przestrzeni lat. Kluczowe jest zrozumienie, jak zmieniały się one na przestrzeni lat i jaki wpływ miały na branżę bezpieczeństwa. 

**Cele edukacyjne**

- Historia praktyk związanych z tworzeniem oprogramowania i ich ewolucja na przestrzeni lat  
    
- Znaczenie tej dziedziny i koncepcje tego, co ją tworzy DevSecOps
- Kultura DevSecOps i jako dyscyplina  

Ścieżka edukacyjna DevSecOps

﻿To pierwsza sala w ramach nowej ścieżki szkoleniowej DevSecOps, która jest w trakcie opracowywania. Nowa ścieżka obejmie:

- Wprowadzenie do DevSecOps (bezpiecznego SDLC, Środowiska i Narzędzia)
- Bezpieczeństwo potoku (automatyzacja potoku, bezpieczeństwo kodu źródłowego, automatyczne testowanie kodu, zarządzanie zależnościami,CI/płyta CDi Bezpieczeństwa Środowiska)
- Bezpieczeństwo rurociągu (atakowanie rurociągu, wykorzystywanie luk w zabezpieczeniach rurociągu, obrona rurociągu)
- Infrastruktura jako kod (chmura)DevOps, Secret Management, Wykorzystywanie Terraform, Wykorzystywanie Vagrant, Wykorzystywanie Dockera)

Od początku swojego istnienia, Dział Operacji Deweloperskich (DevOps) stał się znaczącym czynnikiem we współczesnym rozwoju oprogramowania, wdrażaniu i operacjach. Skąd jednak wzięło się to określenie?

---

## Historia DevOps

Dawno temu wykorzystywaliśmy wodospady.

### Model wodospadu

Tak nazywano podejście do zarządzania projektami w dawnych czasach (lata 70.). Cykl ten opierał się na _hierarchii_ , w której każdy członek zespołu miał przypisane określone obowiązki. Na przykład, administratorzy systemu pracowali niestrudzenie, aby wszystko działało sprawnie i bez zakłóceń. Programiści tworzyli i dodawali jak najwięcej funkcji, a na koniec inżynierowie ds. zapewnienia jakości (QA) testowali funkcjonalność systemu, upewniając się, że wszystko działa zgodnie z oczekiwaniami.

![Diagram etapów modelu kaskadowego rozwoju oprogramowania](https://cdn-images.tryhackme.com/user-uploads/61a7523c029d1c004fac97b3/room-content/21ff900651b19689600a2a7d0cd2fcea.png)

Jeśli coś będzie przeszkadzać serwerom lub będzie wymagało wdrożenia, administratorzy systemów się tym zajmą. Jeśli problem będzie dotyczył kodu, programiści ugaszą pożar. Jeśli będzie to miało związek z testowaniem funkcjonalności i zbieraniem opinii, zespoły ds. zapewnienia jakości się tym zajmą. Ale co, jeśli pojawi się wada? Błąd? Kto go naprawi? Takie sytuacje prowadziły do ​​wielu gier oskarżających i przekazywania pałeczki, co powodowało tarcia, zalegały prace, a symbioza między zespołami przestawała działać. Wraz ze wzrostem oczekiwań klientów rosła liczba funkcji i nowych wydań. Obowiązki i zadania kończyły się kumulacją, gigantycznym bałaganem. Błędy i luki w zabezpieczeniach były zaległe, wiele z nich nierozwiązanych, a kolejne zaplanowane wydania były nieskalowalne i chaotyczne. Nadmierny hałas i presja prowadziły do ​​braku zaufania, luk w komunikacji i tarć między zespołami.

Ta popularna strategia i system rozwiązywania problemów stały się główną przyczyną nieskuteczności elastyczności i komunikacji w zespołach.

### Model zwinny

W obliczu wyzwań, z jakimi zespoły mierzyły się w modelu kaskadowym, firmy zaczęły opracowywać metody zapewniające większą elastyczność i adaptacyjność. Gdzieś na początku 2000 roku powstała **metodyka Agile** . Wkrótce potem opublikowano manifest: [Agile Manifesto .(otwiera się w nowej karcie)](http://agilemanifesto.org/), podkreślając cztery wartości zwinnego rozwoju:

![Diagram etapów modelu Agile Software Development](https://cdn-images.tryhackme.com/user-uploads/61a7523c029d1c004fac97b3/room-content/db09323bd5eed6fb32de796bdb20196f.png)

- Jednostki i interakcje ponad procesami i narzędziami
- Działające oprogramowanie ponad obszerną dokumentacją
- Współpraca z klientem ponad negocjacjami kontraktowymi
- Reagowanie na zmiany a podążanie za planem

Firmy cenią sobie obecnie współpracę zespołową i opierają się na samoorganizujących się zespołach, które koncentrują się na klientach, a także mają duże możliwości wprowadzania zmian i zapewniają dużą elastyczność.

Ale czegoś nadal brakowało.

W 2008 roku rozmowa Andrew Claya i Patricka Debois doprowadziła do czegoś rewolucyjnego. Dyskusja o wadach metodyki Agile doprowadziła do narodzin DevOps. Po wydarzeniu „DevOpsDays” w Belgii w następnym roku, DevOps stał się kolejnym modnym hasłem, a jego popularność wzrosła.

DevOps znacznie różni się od poprzednich metodologii, ponieważ koncentruje się na wprowadzaniu „zmian kulturowych” w celu zwiększenia wydajności. Osiąga to poprzez łączenie magii wszystkich zespołów pracujących nad projektem, wykorzystując integrację i automatyzację. Dzięki tym składnikom uzyskuje się integrację krzyżową między wszystkimi działami: działem zapewnienia jakości (QA), administratorami systemów (Sysadmins) i programistami. Na przykład, programiści mogą teraz uczestniczyć we wdrażaniu, a administratorzy systemów mogą pisać skrypty, dział zapewnienia jakości (QA) może znaleźć sposób na naprawienie błędów, zamiast ciągłego testowania funkcjonalności. Dzięki wprowadzeniu automatyzacji i integracji systemów, inżynierowie ci mają teraz stały wgląd w sytuację i mogą odpowiednio współpracować. W kolejnych częściach zajmiemy się tym, jak DevOps to robi, omawiając…rurociągi, automatyzacja, ciągła integracja i ciągłe dostarczanie (CI/płyta CD).

## Dlaczego DevOps jest ważny?

DevOps opiera się na filozofii, która kładzie nacisk na budowanie zaufania i lepszą współpracę między programistami a innymi zespołami (administratorami systemów, działem kontroli jakości itp.). Pomaga to organizacji dostosować projekty technologiczne do wymagań biznesowych, zwiększając ich wpływ i wartość dla firmy, ponieważ stają się one bardziej wydajne i odpowiednio priorytetyzowane. Wprowadzane zmiany są zazwyczaj niewielkie i odwracalne, widoczne dla wszystkich zaangażowanych zespołów. Zapewnia to lepszy wkład i komunikację, co sprzyja tempu i zwiększa kompetencje w realizacji zadań.

## Podsumowanie

Dzięki pojawieniu się DevOps dzisiejsza infrastruktura programistyczna jest w pełni zautomatyzowana i działa w oparciu o samoobsługę:

- Deweloperzy mogą udostępniać zasoby chmurom publicznym bez konieczności polegania na dziale IT w zakresie zapewniania infrastruktury, co w przeszłości prowadziło do opóźnień trwających tygodnie lub miesiące.
- Ciągła integracja i wdrażanie (CI/CD) automatycznie konfigurują środowiska testowe, przejściowe i produkcyjne w chmurze lub lokalnie. Można je wycofywać z eksploatacji, skalować lub rekonfigurować w zależności od potrzeb.
- Infrastruktura jako kod (IaC) jest powszechnie stosowana do deklaratywnego wdrażania środowisk przy użyciu narzędzi takich jak Terraform i Vagrant.
- Organizacje mogą teraz dynamicznie dostarczać konteneryzowane obciążenia robocze, korzystając ze zautomatyzowanych, adaptacyjnych procesów.

*Podejście deklaratywne wymaga od użytkowników określenia stanu końcowego infrastruktury — na przykład wdrożenia tych maszyn w stanie uruchomionym bezpośrednio w środowisku, automatyzując wybory konfiguracyjne w całym procesie pracy. Oprogramowanie buduje je i udostępnia bez ingerencji człowieka.

Podejście imperatywne/proceduralne polega na konfigurowaniu systemów w serii możliwych do wykonania kroków. Na przykład, można zadeklarować wdrożenie nowej wersji oprogramowania i zautomatyzować szereg kroków, aby uzyskać stan gotowości do wdrożenia. Wybór momentu zastosowania tych zmian następuje na końcu poprzez dodanie „bramki” — taką bramką może być przycisk zwalniający zmiany, np. „Wdróż zmiany”, po pomyślnym zakończeniu wszystkich automatycznych sprawdzeń i wprowadzeniu nowych konfiguracji.

W takim przepływie pracy nawet drobny problem może narobić bałaganu. Co więcej, wraz ze wzrostem liczby nowych wydań (co jest faktem), cała sprawa może przerodzić się w katastrofę. Sytuacja z pewnością wymknęłaby się spod kontroli, gdyby problem pozostał nierozwiązany, a wiele funkcji miało zostać wydanych.

Przeczytaj więcej na: [https://www.appknox.com/blog/history-of-devops](https://www.appknox.com/blog/history-of-devops)

W poprzednim zadaniu poznaliśmy różne style tworzenia oprogramowania na przestrzeni lat i ich ważną rolę w  powstaniu DevOpsTo zadanie wprowadzi Cię w kluczowe koncepcje, narzędzia i sposób ich współdziałania.

Jak działa DevOps?

DevOps można wizualizować jako nieskończoną pętlę opisującą wszystkie składające się na nią fazy:

![diagram pętli nieskończonej opisujący cykl życia DevOps](https://cdn-images.tryhackme.com/user-uploads/61a7523c029d1c004fac97b3/room-content/538ad9f777ec0153d5d648edd4bcf65a.png)

Podążając za nieskończoną pętlą diagramu DevOps, rozszerzmy niektóre narzędzia i procesy DevOps, które omówimy, podążając za DevSecOps ścieżki i jak pomagają organizacji:

1. **CI/CD**– W poprzednim zadaniu wspomnieliśmyCI/CD(Ciągła Integracja i Ciągłe Wdrażanie); CI/CD polega na częstym scalaniu kodu i automatycznym dodawaniu testów w celu przeprowadzania kontroli w miarę wypychania i scalania nowego kodu. Możemy testować kod w trakcie wypychania i scalania dzięki nowej dynamice i procedurze wdrażania, która przyjmuje formę systematycznych i rutynowych drobnych zmian w kodzie. Dzięki tej zmianie dynamiki, CI/CD pomaga wykrywać błędy na wczesnym etapie i zmniejsza nakład pracy związany z masowym utrzymaniem modułowego kodu, co pozwala na niezawodne wycofywanie wersji/kodu.
2. **INFRASTRUKTURA JAKO KOD** (IaC) – sposób zarządzania i udostępniania infrastruktury za pomocą kodu i automatyzacji. Dzięki temu podejściu możemy ponownie wykorzystać kod używany do wdrażania infrastruktury (na przykład instancji w chmurze), co pomaga w spójnym tworzeniu i zarządzaniu zasobami. Standardowymi narzędziami IaC są Terraform, Vagrant itp. Będziemy z nich korzystać w dalszej części kursu, eksperymentując z bezpieczeństwem IaC. 
3. **ZARZĄDZANIE KONFIGURACJĄ** – W tym miejscu stan infrastruktury jest stale zarządzany, a zmiany są skutecznie wprowadzane, co ułatwia jej utrzymanie. Dzięki temu oszczędza się mnóstwo czasu i zyskuje się lepszy wgląd w konfigurację infrastruktury. Do zarządzania konfiguracją można wykorzystać IaC.
4. **ORKIESTRACJA** – Orkiestracja to automatyzacja przepływów pracy. Pomaga osiągnąć stabilność; na przykład, automatyzując planowanie zasobów, możemy szybko reagować w przypadku wystąpienia problemu (np. niepowodzenia kontroli stanu); jest to możliwe dzięki monitorowaniu.
5. **MONITORING** – koncentruje się na gromadzeniu danych o wydajności i stabilności usług oraz infrastruktury. Umożliwia to szybsze odzyskiwanie danych, poprawia widoczność międzyzespołową, dostarcza więcej danych do analizy w celu lepszej analizy przyczyn źródłowych, a także generuje automatyczną odpowiedź, jak wspomniano wcześniej.
6. **MIKROUSŁUGI** – Architektura, która dzieli aplikację na wiele małych usług. Ma to szereg zalet, takich jak elastyczność w razie potrzeby skalowania, mniejsza złożoność i więcej możliwości wyboru technologii w ramach mikrousług. Przyjrzymy się temu bardziej szczegółowo w ścieżce DevSecOps.

Wstęp

Bezpieczeństwo można teraz łatwo zintegrować dzięki widoczności i elastyczności, DevOps Wprowadzenie. Być może słyszałeś o koncepcji „przesunięcia w lewo”. Oznacza to, że  zespoły DevOps koncentrują się na wdrażaniu bezpieczeństwa już na najwcześniejszych etapach cyklu rozwoju oprogramowania i wprowadzaniu kultury współpracy między programistami a bezpieczeństwem.

Dzięki możliwości wczesnego wdrażania zabezpieczeń ryzyko jest teraz znacznie ograniczone. W przeszłości luki w zabezpieczeniach i błędy były wykrywane na bardzo późnych etapach, nawet w fazie produkcyjnej. Prowadziło to do stresu, wycofań i strat ekonomicznych. Integracja narzędzi do analizy kodu i testów automatycznych na wcześniejszym etapie procesu pozwala teraz na identyfikację tych luk w zabezpieczeniach już na wczesnym etapie rozwoju.

Przesunięcie w lewo

W przeszłości testy bezpieczeństwa wdrażano pod koniec cyklu rozwoju oprogramowania. Wraz z rozwojem branży i wprowadzaniem funkcji bezpieczeństwa, zespoły ds. bezpieczeństwa przeprowadzały różne analizy i testy bezpieczeństwa na końcowych etapach cyklu życia. 

W zależności od wyników testów bezpieczeństwa, aplikacja albo zezwalała na wdrożenie do produkcji, albo odrzucała ją i odsyłała do programistów w celu usunięcia zidentyfikowanych błędów. Powodowało to długie opóźnienia w rozwoju i tarcia między zespołami.

Wdrażanie środków bezpieczeństwa na wszystkich etapach cyklu rozwoju oprogramowania (przesunięcie w lewo), a nie na jego końcu, gwarantuje, że oprogramowanie będzie projektowane z uwzględnieniem najlepszych praktyk bezpieczeństwa. Wykrywanie luk w zabezpieczeniach na wczesnym etapie rozwoju obniża koszty ich usuwania i eliminuje konieczność wycofywania zmian, ponieważ są one naprawiane na czas. To obniża koszty, buduje zaufanie oraz poprawia bezpieczeństwo i jakość produktu.

Dlaczego przesuwamy się w lewo

Dawniej, przed wprowadzeniem metodyki Agile, programiści zamawiali infrastrukturę od działu IT i otrzymywali serwery po tygodniach lub miesiącach. Obecnie dostarczanie infrastruktury w chmurze jest zautomatyzowane.  Ta zmiana poprawiła produktywność i szybkość rozwoju oprogramowania. Jednak ta zwiększona prędkość może również budzić obawy dotyczące bezpieczeństwa i prowadzić do luk, które mogą pozostać niezauważone. 

![Korzyści z przesunięcia w lewo](https://cdn-images.tryhackme.com/user-uploads/61a7523c029d1c004fac97b3/room-content/2078c48d1463aaf4245f2ed0d1175cab.png)

Podejście Shift-Left gwarantuje wczesne wykrycie tych wad poprzez wdrożenie procesów od samego początku. W tym dynamicznym środowisku, przeglądy bezpieczeństwa nowych wersji oprogramowania po ich wdrożeniu lub analiza konfiguracji infrastruktury chmurowej stają się wąskim gardłem. Nawet po wykryciu problemów, brakuje czasu na ich rozwiązanie przed wprowadzeniem kolejnej wersji lub funkcji. Aby sprostać potrzebom klientów, potrzebują oni dynamicznego środowiska do skalowania i rozwoju. Istnieje ryzyko, że bezpieczeństwo pozostanie w tyle; wdrożenie zabezpieczeń na samym początku i dostosowanie testów bezpieczeństwa do cyklu rozwoju oprogramowania zwiększa szanse na szybkie reagowanie na problemy.

To podejście rozwojowe polegające na przesunięciu w lewo w DevOps można nazwać**DevSecOps.**

Yes, you heard it right. With DevOps, security gets introduced early in the development cycle, which minimizes risks massively. Integrating code analysis tools and automated tests earlier can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would enhance the impact of DevOps and eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devops(opens in new tab)](https://www.appknox.com/blog/history-of-devops)

Yes, you heard it right. With DevOps, security gets introduced early in the development cycle, which minimizes risks massively. Integrating code analysis tools and automated tests earlier can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would enhance the impact of DevOps and eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devops(opens in new tab)](https://www.appknox.com/blog/history-of-devops).

Yes, you heard it right. With DevOps, security gets introduced early in the development cycle, which minimizes risks massively. Integrating code analysis tools and automated tests earlier can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would not only enhance the impact of DevOps but also eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now but indeed an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devops(opens in new tab)](https://www.appknox.com/blog/history-of-devops).

With DevOps, security gets introduced early in the development cycle, which minimizes risks massively. Integrating code analysis tools and automated tests earlier can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would not only enhance the impact of DevOps but also eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devops(opens in new tab)](https://www.appknox.com/blog/history-of-devops)

With DevOps, security gets to be introduced early in the development cycle and this minimizes risks massively. Integrating code analysis tools and automated tests earlier in the process can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would not only enhance the impact of DevOps but also eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now, but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devop(opens in new tab)](https://www.appknox.com/blog/history-of-devops)

Yes, you heard it right. With DevOps, security gets to be introduced early in the development cycle and this minimizes risks massively. Integrating code analysis tools and automated tests earlier in the process can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would not only enhance the impact of DevOps but also eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now, but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devop(opens in new tab)](https://www.appknox.com/blog/history-of-devops)

With DevOps, security gets to be introduced early in the development cycle and this minimizes risks massively. Integrating code analysis tools and automated tests earlier in the process can lead to better identification and elimination of security loopholes. And as the software gets to the deployment stage, everything works smoothly as anticipated. Security is not an add-on. It's a must-have design feature. Blending security in DevOps would not only enhance the impact of DevOps but also eliminate a lot of other bottlenecks that could arise otherwise. With a rise in the frequency of cyber threats and tightening regulations, adding security to DevOps is not a choice now, but certainly an obligation.  
Read more at: [https://www.appknox.com/blog/history-of-devo(opens in new tab)](https://www.appknox.com/blog/history-of-devops)

Dzięki DevOps bezpieczeństwo jest wdrażane na wczesnym etapie cyklu rozwoju oprogramowania, co znacząco minimalizuje ryzyko. Integracja narzędzi do analizy kodu i testów automatycznych na wcześniejszym etapie procesu może prowadzić do lepszej identyfikacji i eliminacji luk w zabezpieczeniach. A gdy oprogramowanie dociera do etapu wdrożenia, wszystko działa płynnie, zgodnie z oczekiwaniami. Bezpieczeństwo nie jest dodatkiem. To niezbędna cecha projektu. Połączenie bezpieczeństwa z DevOps wzmocniłoby jego wpływ i wyeliminowałoby wiele innych wąskich gardeł, które mogłyby się pojawić w przeciwnym razie. Wraz ze wzrostem częstotliwości cyberzagrożeń i zaostrzaniem przepisów, dodanie bezpieczeństwa do DevOps nie jest już wyborem, lecz wręcz obowiązkiem.  
Przeczytaj więcej [tutaj](https://www.appknox.com/blog/history-of-devops)

DevSecOps To podejście, które w dużej mierze opiera się na automatyzacji i projektowaniu platformy, integrując bezpieczeństwo jako wspólną odpowiedzialność. To styl rozwoju uwarunkowany kulturowo, który normalizuje bezpieczeństwo jako codzienną czynność.

Jaka jest wartość?

DevSecOps pomaga eliminować luki w zabezpieczeniach, maksymalizuje zakres testów i intensyfikuje automatyzację struktur bezpieczeństwa. To znacząco zmniejsza ryzyko, pomagając organizacjom zapobiegać utracie reputacji marki i stratom ekonomicznym spowodowanym incydentami związanymi z lukami w zabezpieczeniach, ułatwiając audyt i monitorowanie.

Jak wdrożyć to efektywnie?

Kultura jest kluczowa. Nie działa bez otwartej komunikacji i zaufania. Działa tylko dzięki wspólnemu wysiłkowi. DevSecOps powinien dążyć do niwelowania luk w wiedzy o bezpieczeństwie między zespołami; aby każdy mógł myśleć i brać odpowiedzialność za bezpieczeństwo, najpierw potrzebuje narzędzi i wiedzy, które pozwolą mu skutecznie i pewnie realizować tę autonomię.

Wyzwania DevSecOps

**Silosy bezpieczeństwa**

Często zdarza się, że wiele zespołów ds. bezpieczeństwa zostaje pominiętych DevOps procesy i przedstawiają bezpieczeństwo jako odrębną jednostkę, w której wyspecjalizowane osoby mogą jedynie utrzymywać i zarządzać praktykami bezpieczeństwa. Taka sytuacja tworzy wyizolowaną strukturę wokół bezpieczeństwa i uniemożliwia inżynierom zrozumienie potrzeby bezpieczeństwa lub stosowania środków bezpieczeństwa od samego początku.

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
  
﻿Jak wspomniano wcześniej, wpajanie bezpieczeństwa DevOps Procesy z widocznością i transparentnością nie są łatwym zadaniem. Istnieje czynnik, który może decydować o sukcesie: poziom zrozumienia i empatii. Oznacza to, że definicja ryzyka dla zespołów ds. bezpieczeństwa jest jednoznaczna, ale dla innych zespołów ryzyko może być inne i równie precyzyjne. Dotyczy to nie tylko ryzyka, ale całego spektrum rzeczy; przekłada się to na to, co traktują priorytetowo, jak pracują i co uważają za wystarczająco ważne, aby odrzucić projekt z krótkim terminem naprawy błędu.  
  
Nie ma magicznego narzędzia ani procesu dla wszystkich. Niezbędne jest zrozumienie, jak pracują programiści/inżynierowie, co uznają za ryzyko i co traktują priorytetowo. Znając ich perspektywę, łatwiej jest zbudować proces, który znajdzie wspólny język i ma większe szanse na powodzenie, niż dodawać kolejne narzędzie, które generuje więcej hałasu i stresu dla wszystkich. To zrozumienie buduje perspektywę, która uwzględnia empatię dla sposobu pracy innych zespołów i buduje proces, który zapewnia elastyczność. Jest to konieczne, ponieważ każda sytuacja może być inna, terminy mogą być różne, a przepustowość może się zmieniać z czasem.  
  
Jako inżynier DevSecOps, załóżmy, że poświęciłeś czas na zrozumienie, jak zespół zarządza usługą. W takim przypadku będzie on miał dodany skaner bezpieczeństwa do swojego procesu rozwoju, działający i przeglądany priorytetowo; łatwiej będzie uzyskać ich akceptację i wykazać wartość. Na przykład, jeśli jest to zespół platformowy i posiada usługę wewnętrzną, ale podstawową, ryzykiem będzie błąd zakłócający działanie usługi, a nie potencjalny atak, który znajduje się za…pełnomocnikPotrzebne byłyby wewnętrzne uprawnienia, aby to wykorzystać. Możesz dostroić skanery lub dodać proces triażu, który zajmie się pytaniami, które same sobie zadadzą, a to z kolei zbuduje zaufanie, zapobiegając podważaniu bezpieczeństwa i podważaniu procedur bezpieczeństwa.﻿

Przeczytaj [tutaj historie sukcesów DevSecOps(otwiera się w nowej karcie)](https://www.csoonline.com/article/3439737/3-devsecops-success-stories.html).

Modele rozwoju oprogramowania

SEC3PO,X Fighter Dev,Chewba-QAi S2-A2 zostały przydzielone do odkrywania minerałów na pobliskich planetach Galaktyki. Watto, Robaczek, finansuje misję, dostarczając sprzęt i paliwo do realizacji tego projektu. Mają za zadanie wyznaczyć kurs i zbadać te planety. Czy potrafisz zgadnąć, jaki model rozwoju oprogramowania wykorzystali w każdym przypadku, aby zrealizować misję?

**Kliknij** `View Site`**przycisk w prawym górnym rogu i spójrz na statyczną stronę powiązaną z tym zadaniem. Czy potrafisz określić, jakie podejście zastosowano w każdym fragmencie komiksu? Aby ponownie wyświetlić komiks, kliknij przycisk ponownie.**

****Aby ponownie obejrzeć komiks, kliknij**** ****przycisk jeszcze raz.**** `View Site`

**Tło**

**Misja:** Podróż na planetę z jak najmniejszym ryzykiem.

**Paliwo:** odpowiada za 130 000 lat świetlnych podróży

**Modele:** Waterfall, Agile iDevOps  

|   |   |
|---|---|
|**Planeta**|**Odległość od statku kosmicznego**|
|Testoine|125 000 lat świetlnych|
|Hackboo|100 000 lat świetlnych|
|WypróbujHothMe|80 000 lat świetlnych|
|Dagobug|60 000 lat świetlnych|

Komiks 1

****Niektóre testy zakończyły się sukcesem i wysłano je na Testooine, co było pierwotną decyzją twórców X Fightera. Zdecydowano, że to będzie kolejna planeta do odwiedzenia.****

Komiks 2

****Niektóre testy wykazały, że podróż na Testooine wiąże się z dużym ryzykiem; początkowo niektóre testy powiodły się dla Naboo, ale S2-D2 zdecydował, że należy zmienić trasę na Hoth.****

Komiks 3

**Wstępna decyzja, oparta na analizie myśliwca X Dev, to lot na Hoth. Koszty zostały zakwestionowane, a chociaż Hoth jest jedną z najbliższych planet, SEC3PO przeanalizował trajektorię i ustalił nowe parametry testów. Chewba-QA zdecydował o zmianie orbity na Dagobah na podstawie dalszych testów.**
