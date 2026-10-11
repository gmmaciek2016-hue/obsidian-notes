---

Spędziłeś dwanaście modułów ucząc się, jak włamać się do systemów na ścieżce [Jr Penetration Tester](https://tryhackme.com/path/outline/jrpenetrationtester) . Skanowałeś sieci za pomocą `nmap`, wymusiłeś uwierzytelnienia za pomocą `hydra`, enumerowałeś katalogi internetowe za pomocą `gobuster`i wykorzystywałeś luki w zabezpieczeniach za pomocą .MetasploitOto pytanie, nad którym prawdopodobnie nie zastanawiałeś się: co dzieje się po drugiej stronie ekranu w momencie, gdy twoje ataki wylądują?

Gdzieś w tle zapalił się panel analityka bezpieczeństwa. Uruchomił się alert. Wpis w logu zarejestrował Twój źródłowy adres IP, nieudane próby logowania i próby ataku brute force na Twój katalog. Pytanie nie brzmi, czy Twoja aktywność została zauważona, ale czy ktoś na nią zareagował. Zrozumienie, jak pracuje analityk, z jakich narzędzi korzysta i gdzie kryją się jego słabe punkty, odróżnia kompetentnego pentestera od wybitnego.

![Analitycy SOC sprawdzają zdarzenia SIEM](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779221212567.png)

## DlaczegoNiebieski zespółTo ma dla Ciebie znaczenie

To nie jest zmiana kariery. Nie prosimy Cię, żebyś zostałSOCAnalityk. Dajemy Ci wiedzę, jak myśleć jak analityk, ponieważ pentesterzy, którzy rozumieją perspektywę obrońcy, zyskują trzy konkretne korzyści:

- **Ukrycie** : Kiedy wiesz, co wyzwala alert, możesz działać poniżej progu detekcji. Pentester, który rozumie, że 50 nieudanych logowań z jednego adresu IP w czasie krótszym niż minuta, rozświetla każdySIEMw budynku ograniczą próby siłowego dostępu do danych lub zamiast tego będą stosować rozsyłanie poświadczeń.
- **Lepsze raportowanie** : Klienci nie chcą tylko wiedzieć, co zepsułeś. Chcą wiedzieć, czy ich zabezpieczenia to wykryły, a jeśli nie, to dlaczego. Pentester, który potrafi powiązać wyniki z lukami w detekcji, daje klientom coś, co można wykorzystać.
- **Realistyczne testowanie** : Prawdziwi przeciwnicy dostosowują się do obrony. Jeśli nie rozumiesz tych mechanizmów obronnych, twoje testy pozostają sztuczne. Starcia w fioletowych zespołach, gdzie atak i obrona iterują razem, przynoszą najgłębsze ulepszenia bezpieczeństwa.

## Czerwony, niebieski i fioletowy

Oznaczmy te role jasno. **Zespół czerwony** symuluje przeciwników. Ich zadaniem jest znajdowanie słabości, wykorzystywanie ich i demonstrowanie realnego wpływu. Rozwijasz umiejętności zespołu czerwonego od Modułu 1.

**Zespół niebieski** zajmuje się obroną. Monitoruje sieci, analizuje alerty, bada incydenty i reaguje na naruszenia. Ich zestaw narzędzi obejmuje systemy SIEM, systemy wykrywania włamań, platformy wykrywania punktów końcowych oraz narzędzia do analizy kryminalistycznej.

**Zespół fioletowy** zamyka pętlę między atakiem a obroną. W ćwiczeniu zespołu fioletowego, czerwony wykonuje technikę ataku, podczas gdy niebieski obserwuje w czasie rzeczywistym. Następnie obie strony powtarzają: niebieski dostosowuje swoje wykrycia, czerwony dostosowuje swoje podejście i cykl się powtarza. To właśnie w tej pętli sprzężenia zwrotnego organizacje obserwują największe korzyści w zakresie bezpieczeństwa.

## Cele edukacyjne

W tym pokoju poznasz świat obrońcy w sześciu etapach:

1. **Operacje SOC** – jak zorganizowane jest Centrum Operacji Bezpieczeństwa i dlaczego alerty czasami przepadają
2. **Podstawy SIEM** – praktyczna nawigacja Splunkplatforma, na której obrońcy przeszukują i korelują logi
3. **Analiza dzienników** — rozpoznawanie wzorców ataków (tych samych ataków, które nauczyłeś się wykonywać) w dziennikach zdarzeń systemu Windows i dziennikach serwera WWW
4. **Reagowanie na incydenty** – ustrukturyzowany proces, który stosują obrońcy, gdy coś pójdzie nie tak
5. **Wywiad zagrożeń** – ramy takie jak MITRAATT&CK i Piramida Bólu, które zapewniają obrońcom wspólny język dla zachowań przeciwnika
6. **Dochodzenie końcowe** – kompleksowe dochodzenie w rzeczywistym scenariuszu ataku, wykorzystujące wszystkie dostępne informacje

Na koniec będziesz w stanie spojrzeć na własną aktywność w testach penetracyjnych oczami osoby broniącej się i dokładnie zrozumieć, jakie ślady za sobą zostawiasz.

Aby zrozumieć świat obrońcy, musimy najpierw zrozumieć ludzi i procesy panujące w Centrum Operacji Bezpieczeństwa. To właśnie tutaj rozpoczyna się Zadanie 2.

W listopadzie 2013 r. system wykrywania włamań FireEye firmy Target Corporation wykrył złośliwe oprogramowanie w swojej sieci. Uruchomiono alert. SOCAnalityk z Bangalore to zauważył. System był nawet skonfigurowany do automatycznego usuwania zagrożenia, ale ta funkcja była wyłączona. Nikt nie eskalował alarmu. Przez kolejne 18 dni złośliwe oprogramowanie BlackPOS kontynuowało zbieranie danych kart kredytowych z terminali POS. Do czasu opanowania ataku skradziono 40 milionów kart płatniczych, naruszono 70 milionów danych klientów, a ostateczny koszt przekroczył 162 miliony dolarów. Prezes i dyrektor ds. informatyki złożyli rezygnacje.

Oto, co sprawia, że ​​warto poznać tę historię: technologia zadziałała. System wykrywania wykonał dokładnie to, co powinien. Awaria była całkowicie ludzka i proceduralna. Aby zrozumieć, jak dochodzi do tego typu awarii, musimy poznać ludzi, strukturę i presję panującą w **Centrum Operacji Bezpieczeństwa (SOC)** .

Jak wspomnieliśmy w poprzednim zadaniu, zrozumienie świata obrońcy czyni cię lepszym praktykiem ofensywnym. To zadanie przedstawia konkretne osoby pracujące w tym świecie i procesy, którymi kierują się na co dzień.

## Struktura poziomów SOC

SOC jest podzielony na poziomy, z których każdy ma odrębne obowiązki i ścieżki eskalacji. Rozważmy szpitalny oddział ratunkowy: pielęgniarka triażowa ocenia każdego pacjenta przy wejściu i decyduje, kto potrzebuje natychmiastowej pomocy specjalisty. Pielęgniarka nie wykonuje operacji, a chirurg nie siedzi w poczekalni, mierząc temperaturę. Każda rola istnieje, ponieważ liczba przypadków wymaga specjalizacji. Z technicznego punktu widzenia poziomy SOC działają w ten sam sposób.

**Poziom 1: Analityk Triage** znajduje się u podstawy. Analitycy poziomu 1 monitorują kolejkę alertów, przeprowadzają wstępną klasyfikację, zamykają fałszywe alarmy i eskalują wszystko, co wygląda na prawdziwy incydent. Obsługują największą liczbę zadań i stanowią pierwszą linię obrony. Jeśli alert wygląda podejrzanie, ale wymaga głębszej analizy, analityk poziomu 1 nie próbuje rozwiązać go samodzielnie, lecz eskaluje w górę.

**Poziom 2: Analityk ds. Incydentów** otrzymuje alerty eskalowane z poziomu 1. Analitycy poziomu 2 przeprowadzają dogłębną analizę, określają zakres incydentu, aby określić liczbę systemów, których dotyczy, koordynują działania powstrzymujące i zbierają dowody. Mają większe doświadczenie i szerszy dostęp do narzędzi niż poziom 1.

**Poziom 3: Łowca Zagrożeń / Starszy Analityk** działa proaktywnie. Zamiast czekać na alerty, analitycy poziomu 3 formułują hipotezy dotyczące zachowania atakujących i poszukują oznak zagrożenia, które zostały przeoczone przez automatyczne wykrywanie. Tworzą również nowe reguły detekcji, przeprowadzają zaawansowaną analizę kryminalistyczną i opracowują narzędzia. Niektóre organizacje dodają poziom **L4** do zarządzania SOC, inżynierii i konserwacji platformy.

Przepływ eskalacji zawsze jest skierowany w górę: poziom 1 dokonuje selekcji, poziom 2 prowadzi dochodzenie, poziom 3 poluje i wysyła inżynierów. Każdy poziom filtruje obciążenie pracą dla poziomu wyższego.

## Przepływ pracy analityka

Kiedy analityk L1 rozpoczyna zmianę, proces przebiega według pewnego schematu:

1. **Monitoruj kolejkę** : Otwórz panel alertów i przejrzyj nowe, nieprzypisane alerty.
2. **Selekcja** : Wybierz alert, zapoznaj się z jego szczegółami i sklasyfikuj go. Czy to znany fałszywy alarm? Czy źródłowy adres IP, typ zdarzenia lub zasób docelowy sugerują realne zagrożenie?
3. **Zbadaj** : Jeśli alert wymaga uwagi, skoreluj go z innymi źródłami danych. Sprawdź powiązane logi, poszukaj wzorców i zbierz kontekst.
4. **Zdecyduj** : zamknąć alert jako fałszywie pozytywny wraz z dokumentacją lub eskalować go do poziomu L2, załączając ustalenia.

Ten cykl powtarza się dziesiątki, a nawet setki razy na zmianę. Szybkość i precyzja pod presją odróżniają skutecznego pracownika pierwszego poziomu od osoby, która przepuszcza krytyczne alerty przez palce.

## Pomiar wydajności SOC:Średnia dzienna dnia (MTTD)IMTTR

Dwa wskaźniki definiują wydajność SOC.

**Średni czas wykrycia (MTTD)** mierzy średni czas między początkowym atakiem atakującego a wykryciem naruszenia przez organizację. [Raport IBM dotyczący kosztów naruszenia danych z 2025 r.(otwiera się w nowej karcie)](https://www.ibm.com/think/x-force/2025-cost-of-a-data-breach-navigating-ai)Średnia globalna wynosi 181 dni. Oznacza to, że wielu atakujących działa w sieciach przez ponad sześć miesięcy, zanim ktokolwiek to zauważy. [Trendy M Mandiant na rok 2026(otwiera się w nowej karcie)](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026)Raport pokazuje globalną medianę czasu pozostawania na poziomie 14 dni, w porównaniu z 11 dniami rok wcześniej i 10 dniami rok wcześniej. Liczby z obu raportów różnią się, ponieważ mierzą różne populacje: IBM bada szeroko organizacje, które padły ofiarą włamań; Mandiant czerpie z działań reagowania na incydenty na pierwszej linii frontu, gdzie przypadki zazwyczaj obejmują bardziej wyrafinowanych napastników. Oba kierunki podróży mają znaczenie dla pentestera. Średnia makroekonomiczna pokazuje, jak długo zazwyczaj trwa niewykryty dostęp; rosnąca mediana Mandiant sugeruje, że ukierunkowani atakujący, dysponujący dużymi zasobami, coraz lepiej radzą sobie z ukrywaniem się.

**Średni czas reakcji (MTTR)** mierzy średni czas od wykrycia do powstrzymania ataku. Dane IBM z 2025 roku wskazują, że wynosi on 60 dni. Wykrycie naruszenia to tylko połowa problemu; powstrzymanie go, zanim atakujący osiągnie swój cel, to druga połowa.

Niższe wartości są lepsze dla obu wskaźników. Każdy dodatkowy dzień przebywania w sieci daje atakującemu więcej możliwości poruszania się w różnych kierunkach, eskalacji uprawnień i wykradania danych.

## Zmęczenie czujności: wąskie gardło człowieka

Teraz docieramy do rzeczywistości, która wyjaśnia wyciek danych w Target. Analitycy SOC mierzą się z nieustannym strumieniem alertów, a większość z nich to szum informacyjny. [Badania(otwiera się w nowej karcie)](https://www.praetorian.com/security-101/alert-fatigue-and-false-positives/)wskazują, że wskaźniki fałszywie dodatnich wyników w nowoczesnych centrach operacji bezpieczeństwa wahają się od 50% do 80%, a jedynie około **37%** alertów jest faktycznie badanych, zgodnie z [raportem o stanie bezpieczeństwa z 2026 r.(otwiera się w nowej karcie)](https://www.crogl.com/resources/research/state-of-secops-ai). Tenodpoczyneksą automatycznie zamykane, tracą priorytet lub po prostu nigdy nie są otwierane.

To jest **zmęczenie alertami** : spadek uwagi i osądu analityka spowodowany ciągłym napływem alertów niskiej jakości. Kiedy 7 na 10 alertów, które badasz, okazuje się niczym, zaczynasz oczekiwać, że kolejny też będzie niczym. Pomnóż to przez 8-godzinną zmianę z setkami alertów, a stanie się jasne, jak realne zagrożenie może kryć się na widoku.

Dokładnie to wydarzyło się w Target. System FireEye wygenerował uzasadniony alert o aktywnym złośliwym oprogramowaniu. Jednak w środowisku, w którym analitycy byli uwarunkowani do obserwowania fałszywych alarmów, alert nie wzbudził należnej mu pilności. Proces zawiódł nie z powodu niekompetencji, ale dlatego, że stosunek sygnału do szumu w systemie podkopał zaufanie analityków.

## Patrząc w przyszłość

Analitycy SOC potrzebują narzędzi, aby przebić się przez ten szum. Monitorowanie surowych plików logów z dziesiątek systemów, każdy w innym formacie, nie jest skalowalne. Potrzebują scentralizowanej platformy, która gromadzi, normalizuje i koreluje dane z każdego źródła w jednym miejscu, zapewniając im pojedynczy interfejs do wyszukiwania, badania i wykrywania zagrożeń. W kolejnym zadaniu przyjrzymy się właśnie tej platformie: systemowi zarządzania informacjami i zdarzeniami bezpieczeństwa (Security Information and Event Management), czyli…SIEMi będziemy mogli osobiście zapoznać się zSplunkpo raz pierwszy.

Wyobraź sobie analityka L1 przychodzącego na poniedziałkową zmianę rano. Kolejka alertów liczy już 200 zdarzeń. Niektóre z nich pochodzą z…zapora sieciowa Niektóre pochodziły z serwera WWW. Niektóre pochodziły z punktów końcowych Windows. Każde źródło logów ma swój własny format, własne konwencje znaczników czasu i własną lokalizację przechowywania. Bez jednej platformy do gromadzenia, wyszukiwania i korelowania wszystkich tych zdarzeń, analityk musiałby logować się do kilkunastu różnych systemów, ręcznie porównywać znaczniki czasu i mieć nadzieję, że nic nie umknie jego uwadze. W 2017 roku ten sam problem kosztował Equifax 147 milionów rekordów klientów. Wygasły certyfikat SSL na urządzeniu do inspekcji ruchu nie był odnawiany przez 19 miesięcy, tworząc martwą strefę w monitorowaniu szyfrowanego ruchu, którą atakujący wykorzystali podczas 77-dniowego naruszenia bezpieczeństwa. Lekcja jest jasna: scentralizowana widoczność nie jest opcjonalna; jest fundamentem wszystkiego, co…SOCrobi.

Kontynuując temat omówiony w Zadaniu 2, gdzie omówiliśmy strukturę poziomów SOC i przepływ pracy kolejki alertów, to zadanie przedstawia narzędzie, którego analitycy faktycznie używają do badania alertów. Tym narzędziem jest system **Security Information and Event Management** , czyli…**SIEM**.

## Co robi SIEM (i czego nie robi)

Wyobraź sobie kuchnię restauracyjną, w której zamówienia napływają z sali jadalnej, baru, lady na wynos i aplikacji do dostaw. Jeśli każde zamówienie trafia do osobnego notatnika w osobnym kącie kuchni, obsługa ulega załamaniu. Działająca kuchnia kieruje każde zamówienie na jeden ekran, gdzie szef kuchni może je priorytetyzować, ustalać kolejność i śledzić. System SIEM to ten pojedynczy ekran dla centrum obsługi klienta (SOC).

Mówiąc językiem technicznym, SIEM realizuje sześć podstawowych funkcji (tutaj skupiamy się na pięciu; pulpity nawigacyjne i raportowanie stanowią część bardziej zaawansowanego szkolenia SOC):

1. **Agregacja** zbiera logi z punktów końcowych, serwerów, zapór sieciowych, czujników IDS, aplikacje i usługi w chmurze na jednej platformie.
2. **Normalizacja** konwertuje te różne formaty dzienników do wspólnego schematu, dzięki czemu zdarzenie systemu Windows i Linux Komunikaty syslog można porównywać obok siebie.
3. **Indeksowanie**przechowuje zdarzenia w sposób umożliwiający szybkie przeszukiwanie milionów lub miliardów rekordów.
4. **Korelacja** polega na stosowaniu reguł wykrywających wzorce w wielu źródłach danych i przedziałach czasowych, np. po nieudanym logowaniu następuje udane logowanie, a następnie dostęp do poufnych plików.
5. **Alert** powiadamia analityków o uruchomieniu reguły korelacji.

SIEM _nie_ myśli za Ciebie. Bez dostrojonych reguł, przeszkolonych analityków i procedur reagowania, SIEM jest jedynie kosztownym archiwum logów. To błędne przekonanie nr 1 dla początkujących analityków: wdrożenie narzędzia nie jest równoznaczne z monitorowaniem bezpieczeństwa.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

Jedna rzecz, o której należy pamiętać.SplunkW naszym laboratorium działa Splunk Free, który eliminuje alerty, kontrolę dostępu opartą na rolach i wyszukiwanie rozproszone. W produkcyjnym centrum danych SOC z systemem Splunk Enterprise lub innym komercyjnym systemem SIEM te funkcje są kluczowe dla skalowalności operacyjnej. Pracujemy bez nich, ponieważ koncentrujemy się na nauce wyszukiwania i analizowania danych, a nie na konfigurowaniu infrastruktury przedsiębiorstwa.

## Model danych Splunk

Zanim dotkniemy klawiatury, musimy zrozumieć, jak Splunk organizuje dane. Cztery pola mają największe znaczenie:

- **`index`**:Logiczny kontener na dane, podobny do bazy danych. Nasz zbiór danych znajduje się w `index=botsv1`.
- **`source`**: Ścieżka do pliku lub dane wejściowe, które wygenerowały zdarzenie (np. `WinEventLog://Security`).
- **`sourcetype`**:Klasyfikacja formatu danych. To pole informuje Splunk, _jak_ analizować zdarzenia. `WinEventLog:Security`Jest typem źródłowym. `suricata`Jest innym typem źródłowym. `access_combined`Jest jeszcze innym. Każdy z nich ma własne ekstrakcje pól i reguły analizy.
- **`host`**: Nazwa hosta lub adres IP urządzenia, które wygenerowało zdarzenie.

Przy każdym zdarzeniu pojawiają się dwa dodatkowe pola: `_time`(znacznik czasu) i `_raw`(oryginalny tekst zdarzenia przed analizą składniową).

## Łączenie się z laboratorium

Kliknij **„Uruchom maszynę laboratoryjną”** u góry tego zadania, aby uruchomić maszynę wirtualną Splunk. Odczekaj 2–3 minuty, aż maszyna wirtualna uruchomi się całkowicie. Naciśnij „Pokaż podzielony ekran”, jeśli opcja ta nie jest jeszcze dostępna.

Po zalogowaniu trafisz do aplikacji Splunk Search & Reporting. Przyjrzyjmy się interfejsowi. Liczą się cztery obszary:

- **Pasek wyszukiwania** : miejsce, w którym wpisujesz zapytania **SPL** (Search Processing Language).
- **Selektor czasu** : rozwijana lista po lewej stronie paska wyszukiwania, która kontroluje przedział czasowy. To najważniejsza funkcja dla nowych użytkowników i za chwilę zobaczymy dlaczego.
- **Pasek boczny pól** : Po lewej stronie panelu wyników znajdują się wyodrębnione pola, które można kliknąć, aby przeglądać wartości.
- **Karty** : Pod paskiem wyszukiwania znajdują się cztery karty, które kontrolują sposób wyświetlania wyników: Zdarzenia (widok surowego dziennika), Wzory, Statystyki (tabele z poleceń agregacji) i Wizualizacja (wykresy i diagramy).

## Pułapka zbieracza czasu

Oto moment, który wprawia w zakłopotanie każdego nowego użytkownika Splunka. Wpisz poniższe zapytanie w pasku wyszukiwania i naciśnij Enter:

```spl
index=botsv1
```

![Wyszukiwanie Splunk](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779219855827.png)

Jeśli selektor czasu jest ustawiony na wartość domyślną  `Last 24 hours`, nie otrzymasz żadnych wyników. Nic. Zapytanie jest poprawne, dane istnieją, ale Splunk zwraca pustą stronę. Zbiór danych BOTSv1 zawiera zdarzenia z **sierpnia 2016 r.** , przy czym główne scenariusze ataku koncentrowały się wokół 10-11 sierpnia. „Ostatnie 24 godziny” dotyczą daty dzisiejszej, dla której nie ma żadnych zdarzeń. Zmień selektor czasu na „ **Cały czas”** , a nagle pojawią się miliony zdarzeń.

To nie błąd. Tak działa Splunk w każdym środowisku produkcyjnym; zakres czasowy zawsze ma znaczenie. Analitycy, którzy zapominają ustawić odpowiednie okno, marnują minuty wpatrując się w puste ekrany, podczas gdy zegar odlicza czas do zdarzenia.

## Core SPL: wyszukiwanie i agregacja

SPL działa jak potok. Zaczyna się od wyszukiwania, a następnie przekierowuje `|`wyniki przez polecenia transformacji, z których każde udoskonala wynik. Przeanalizujmy trzy podstawowe zapytania.

**Zapytanie 1: Jakie dane posiadamy?**

```spl
index=botsv1 | stats count by sourcetype
```

Po uruchomieniu tego zapytania kliknij kartę **Statystyki** . Każdy wiersz reprezentuje inny format danych w zestawie danych BOTSv1 wraz z liczbą zdarzeń. Zobaczysz wpisy takie jak `WinEventLog:Security`, `suricata`, `access_combined`, `stream:http`, `stream:dns`i inne. `stats count by sourcetype`Polecenie grupuje wszystkie zdarzenia według typu źródła i zlicza, ile zdarzeń należy do każdej grupy.

**Zapytanie 2: Przeglądanie surowych zdarzeń**

```spl
index=botsv1 sourcetype=WinEventLog:Security | head 10
```

Polecenie `head 10`ogranicza dane wyjściowe do pierwszych 10 zdarzeń. Przejdź do karty **„Zdarzenia”** , aby wyświetlić surowe wpisy w dzienniku zabezpieczeń systemu Windows. Każde zdarzenie zawiera pola takie jak `EventCode`, `Account_Name`, `Source_Network_Address`i pełny `_raw`tekst.

**Zapytanie 3: Objętość zdarzeń w czasie**

```spl
index=botsv1 sourcetype=WinEventLog:Security | timechart span=1h count
```

Polecenie `timechart`tworzy agregację szeregów czasowych. Przejdź do karty **Wizualizacja** , aby zobaczyć wykres liniowy pokazujący liczbę zdarzeń bezpieczeństwa, które wystąpiły w każdej godzinie w całym oknie danych. Skoki na tym wykresie to pierwsza rzecz, na którą zwraca uwagę analityk; wskazują one, że w danym oknie wydarzyło się coś nietypowego.

Należy pamiętać, że **złożone zapytania obejmujące miliony zdarzeń mogą zająć od 30 do 60 sekund** . Jest to normalne, biorąc pod uwagę liczbę zdarzeń i dostępne zasoby.

## Normalne a podejrzane: odczytywanie wykresu czasowego

Patrząc na wolumen zdarzeń w czasie, nie każdy skok jest atakiem. Wiedza o tym, jak wygląda sytuacja normalna, to połowa sukcesu.

|Wzór|Normalna|Podejrzany|
|---|---|---|
|Wolumen zdarzeń bezpieczeństwa|Stała linia bazowa z niewielkimi wzrostami w godzinach pracy; niewielkie spadki w nocy|Ostre skoki skupione w wąskim oknie, szczególnie poza godzinami pracy|
|Nieudana dystrybucja logowania|Rozproszone wśród użytkowników iAdresy IP; jednocyfrowa liczba błędnie wpisanych haseł na godzinę|Setki awarii z jednego adresu IP skierowanych na jedno konto w ciągu kilku minut|
|HTTP404 tom|Sporadyczne błędy 404 z powodu uszkodzonych linków lub błędów użytkowników; rozłożone na wiele godzin|Tysiące błędów 404 z jednego adresu IP w szybkiej kolejności z sekwencjąURIwzory|
|Nowe instalacje usług|Rzadko; powiązane z przerwami konserwacyjnymi lub aktualizacjami oprogramowania|Wiele instalacji poza oknami zmian z losowymi nazwami usług|

Przyjrzymy się tym konkretnym wzorcom w Zadaniu 4. Na razie najważniejsze jest to, że pojedyncza liczba nic nie znaczy bez kontekstu. Wykres czasowy z 500 zdarzeniami w ciągu godziny może być zupełnie normalny na obciążonym serwerze WWW lub może być wynikiem ataku siłowego na cichy punkt końcowy. Zadaniem analityka jest poznanie punktu odniesienia.

## Refleksja metodologiczna

Cofnijmy się i spójrzmy na to, co właśnie zrobiliśmy. Podłączyliśmy się do SIEM-a, zorientowaliśmy się w interfejsie, odkryliśmy, że zakres czasowy kontroluje wszystko, a następnie użyliśmy trzech stopniowo bardziej złożonychSPLzapytania, aby przejść od „jakie dane istnieją”, przez „pokaż mi surowe zdarzenia”, po „wizualizację wzorców zdarzeń w czasie”. To podstawowa pętla badawcza w każdym systemie SIEM: określ zakres danych, zawęź obszar zainteresowania, zwizualizuj wzorzec. Konkretne platformy się zmieniają (Splunk, Microsoft Sentinel, Elastic), ale przejście od analizy ogólnej do wąskiej i wizualnej jest wszędzie takie samo.

Teraz możemy wyszukiwać i agregować zdarzenia w Splunku, ale wiedza o _tym, jak_ wyszukiwać, to tylko połowa sukcesu. Musimy również wiedzieć, _czego_ szukać. W kolejnym zadaniu poznamy konkretne identyfikatory zdarzeń systemu Windows i wzorce ataków, które ujawniają działania atakujących, przekształcając surowe dane z dziennika w przydatne informacje.

Uciekłeś Hydrana stronie logowania i obserwowałeś hasła przewijające się na Twoim terminalu. Uruchomiłeś Gobusteri obserwował ścieżki katalogów testowane jedna po drugiej. Z perspektywy atakującego narzędzia te wydają się chirurgiczne i ciche. Teraz pomyśl, co dzieje się po drugiej stronie: każde błędne hasło generuje wpis w dzienniku, każda odpowiedź 404 jest rejestrowana, a każda nowa zainstalowana usługa pozostawia ślad w dzienniku zdarzeń systemu Windows. W maju 2017 roku robak ransomware WannaCry wykorzystał…CVE-2017-0144 (EternalBlue) i przedarł się przez 230 000 systemów w 150 krajach. Na każdym zainfekowanym hoście dropper instalował swój ładunek jako nową usługę systemu Windows, generując **zdarzenie o identyfikatorze 7045** w dzienniku systemowym. Obrońcy, którzy obserwowali to pojedyncze zdarzenie, otrzymali wczesny sygnał ostrzegawczy. Ci, którzy nie byli obserwowani, szyfrowali swoje sieci. Więcej informacji na ten temat można znaleźć [tutaj.(otwiera się w nowej karcie)](https://www.cisa.gov/news-events/alerts/2017/05/12/indicators-associated-wannacry-ransomware).

Jak wspomnieliśmy w poprzednim zadaniu, wiesz już, jak wyszukiwać i agregować zdarzenia wSplunkNarzędzie jest w Twoich rękach. Teraz potrzebujemy słownika sygnatur ataków: konkretnego zdarzeniaIdentyfikatoryi wzorce logów, które oddzielają normalne operacje od aktywnych zagrożeń. Właśnie to zapewnia to zadanie.

## Identyfikatory zdarzeń, które mają znaczenie

System Windows generuje setki typów zdarzeń, ale garstka z nich ma nadmierną wartość wykrywania. Skupmy się na tychSOCanalitycy sprawdzają to w pierwszej kolejności.

**Wydarzenia uwierzytelniania** (sourcetype: `WinEventLog:Security`):

|Identyfikator zdarzenia|Co rejestruje|Dlaczego to ma znaczenie|
|---|---|---|
|`4624`|Pomyślne logowanie|Potwierdza dostęp. `Logon Type`Pole pokazuje, jak: Typ 2 (interaktywny/konsola), Typ 3 (sieć/SMB), Typ 10 (RDP).|
|`4625`|Nieudane logowanie|Objętość i klasteryzacja ujawniają brutalną siłę. Garstka dziennie to norma; setki z jednego adresu IP to już nie.|
|`4672`|Specjalne uprawnienia przypisane nowemu logowaniu|Wyzwala się za każdym razem, gdy loguje się konto administratora. Jest to typowe dla pracowników IT, ale podejrzane w przypadku kont usługowych o nietypowych porach.|

**Zarządzanie kontami** (sourcetype: `WinEventLog:Security`):

|Identyfikator zdarzenia|Co rejestruje|Dlaczego to ma znaczenie|
|---|---|---|
|`4720`|Utworzono konto użytkownika|Trwałość poprzez nowe konta, szczególnie poza przepływami pracy.|
|`4732`|Członek dodany do lokalnej grupy zabezpieczeń|Dodanie konta do grupy Administratorzy to klasyczny sposób na zwiększenie uprawnień.|

**Wydarzenia procesowe i usługowe** :

|Identyfikator zdarzenia|Typ źródła|Co rejestruje|Dlaczego to ma znaczenie|
|---|---|---|---|
|`4688`|`WinEventLog:Security`|Utworzono nowy proces|Śledzi, co działa w systemie. Najbardziej przydatne, gdy włączony jest audyt wiersza poleceń (ustawienie zasad grupy, które rejestruje cały wywołany wiersz poleceń, a nie tylko nazwę pliku wykonywalnego).|
|`7045`|`WinEventLog:System`|Zainstalowano nową usługę|Usługi instalacyjne PsExec, malware dropperów i ransomware (w tym WannaCry). Niska wolumenowość w stabilnych środowiskach.|

**Uchylanie się od obrony** :

|Identyfikator zdarzenia|Co rejestruje|Dlaczego to ma znaczenie|
|---|---|---|
|`1102`|Wyczyszczono dziennik audytu bezpieczeństwa|Wskaźnik wysokiego poziomu ufności po wystąpieniu naruszenia. To zdarzenie nie zanika po wyczyszczeniu, ponieważ samo działanie czyszczące generuje je przed opróżnieniem dziennika. Występowanie bliskie zeru w środowiskach o dobrej kondycji. [Zweryfikowano]|

## Poznaj normę, aby zobaczyć nienormalność

Wykrywanie ataków wymaga najpierw zrozumienia, jak wygląda legalna aktywność. Weźmy na przykład stanowisko ochrony budynku: jeśli nie wiesz, kto pracuje w budynku, nie możesz wykryć intruza. Ta sama zasada dotyczy danych z logów. Z technicznego punktu widzenia, ustalenie punktu odniesienia w zachowaniach pozwala wykryć odchylenia sygnalizujące naruszenie.

|Wzór|Normalna|Podejrzany|
|---|---|---|
|Identyfikator zdarzenia `4625`(nieudane logowania)|Jednocyfrowe lub dwucyfrowe wartości na dzień, rozproszone wśród różnych użytkowników i adresów IP, spowodowane literówkami|Setki z jednego adresu IP źródłowego w ciągu kilku minut, skierowane do jednego lub kilku kont, a następnie z `4624`tego samego adresu IP|
|Identyfikator zdarzenia `4672`(uprawnienia specjalne)|Pożary dla znanych kont administratorów na oczekiwanych maszynach w godzinach pracy|Pożary na kontach niebędących kontami administratora, na kontach administratora w nietypowych godzinach lub na maszynach, którymi zazwyczaj nie administruje|
|Identyfikator zdarzenia `7045`(nowa usługa)|Sporadyczne, koreluje z udokumentowanymi oknami konserwacji i wdrożeniami oprogramowania|Poza oknami konserwacji; losowe nazwy usług; ścieżki wykonywalne w katalogach tymczasowych lub folderach profilu użytkownika|
|`404`Odpowiedzi HTTP|Sporadycznie, rozproszone po różnych URI i adresach IP klientów|Setki lub tysiące z jednego adresu IP w ciągu kilku minut; sekwencyjne alfabetyczne wzorce URI; ciągi User-Agent specyficzne dla danego narzędzia (narzędzia skanujące często wysyłają identyfikowalne ciągi)|
|Identyfikator zdarzenia `1102`(wyczyszczony dziennik)|Wyjątkowo rzadkie; występuje wyłącznie podczas ponownej instalacji systemu operacyjnego lub udokumentowanej konserwacji|Jakiekolwiek zdarzenie mające miejsce podczas aktywnego dochodzenia lub poza udokumentowaną konserwacją|

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

Należy pamiętać o jednej rzeczy. Te linie bazowe są jasne i oczywiste w zbiorze danych BOTSv1, ponieważ analizujemy kontrolowany scenariusz ataku z ograniczonym szumem. W środowisku produkcyjnym z tysiącami użytkowników, zaplanowanymi zadaniami i kontami usług stosunek sygnału do szumu jest znacznie gorszy. Potrzebne byłyby odpowiednio dostrojone progi, listy dozwolonych dla znanych kont usług oraz filtry uwzględniające porę dnia, aby uniknąć utonięcia w błędnych wynikach. Warto o tym wiedzieć, zanim zastosujesz to podejście poza laboratorium.

## Polowanie w kłodach: trzy ćwiczenia SPL

Czas wykorzystać te wzorce. Twoja maszyna wirtualna Splunk jest już uruchomiona od zadania 3. Upewnij się, że selektor czasu jest nadal ustawiony na `All time`.

### Ćwiczenie 1: Wykrywanie zautomatyzowanych narzędzi ataku za pośrednictwem sieciowego systemu IPS

Napływ sygnatur ataków na poziomie sieci z jednego adresu IP to jeden z najwyraźniejszych wskaźników ataku siłowego i skanowania, jakie może wykryć obrońca. Mechanizm IPS FortiGate UTM rejestruje każdą zablokowaną lub wykrytą sygnaturę ataku ze źródłowym adresem IP. Uruchom to zapytanie w pasku wyszukiwania Splunk:

```spl
index=botsv1 sourcetype=fgt_utm subtype=ips
| stats count by srcip
| sort -count
| head 1
```

![Wyszukiwanie Splunk](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779219969585.png)

To zapytanie zlicza każdyIPSZdarzenie ataku wywołanego przez atak jest pogrupowane według źródłowego adresu IP i zwraca wynik na górze listy. Sprawdź zakładkę Statystyki. Adres IP na górze listy wygenerował tysiące sygnatur IPS w sieci Wayne Corp, co jest niepodważalnym dowodem na obecność automatycznego skanowania lub narzędzia do ataków siłowych.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga dotycząca typów źródeł i ataków siłowych.** W środowiskach, w których występuje atak siłowy na poświadczenia systemu Windows, równoważne wykrywanie używa `EventCode=4625`(nieudanego logowania) w `WinEventLog:Security`: `index=botsv1 sourcetype=WinEventLog:Security EventCode=4625 | stats count by src_ip | sort -count`. Atak BOTSv1 na Wayne Corp. koncentrował się na wykorzystaniu aplikacji internetowych, a nie na atakach na poświadczenia systemu Windows, dlatego ten zestaw danych demonstruje atak siłowy na poziomie sieci. Logika wykrywania jest identyczna: agregacja według źródła, liczenie i wyszukiwanie wartości odstających.

### Ćwiczenie 2: Wykrywanie ataków brute-force na katalogi internetowe

Gdy Gobuster lub podobne narzędzie jest uruchamiane na serwerze WWW, generuje mnóstwo żądań do nieistniejących ścieżek. Serwer odpowiada `404`na każde z nich za pomocą protokołu HTTP. Wayne Corp korzysta z IIS, więc odpytujemy `iis`sourcetype, który używa nazw pól w formacie dziennika W3C: `c_ip`dla adresu IP klienta i `sc_status`dla kodu odpowiedzi serwera. Uruchom:

```spl
index=botsv1 sourcetype=iis sc_status=404
| stats count by c_ip
| where count > 100
| sort -count
```

Adres IP na górze wyników zasypywał serwer WWW żądaniami ścieżek, które nie istnieją. Ta liczba błędów 404 z jednego źródła nie jest wynikiem klikania niedziałających linków, lecz automatycznego wyliczania.

### Ćwiczenie 3: Wykrywanie nowych instalacji usługowych

Dropper WannaCry zainstalował się jako usługa systemu Windows. PsExec robi to samo podczas ruchu poziomego. Poszukajmy instalacji usług w danych BOTSv1:

```spl
index=botsv1 sourcetype=WinEventLog:System EventCode=7045
| table _time, Service_Name, Service_File_Name
```

![Wyszukiwanie Splunk](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779219969595.png)

Przejrzyj wyniki. Zwróć uwagę na  `Service_File_Name`kolumnę. Usługi ze ścieżkami wykonywalnymi wskazującymi na katalogi tymczasowe, foldery profili użytkowników lub nazwy losowe zasługują na bliższe przyjrzenie się. W zestawie danych BOTSv1 zobaczysz `tenable_mw_scan`installed from `%SystemRoot%`z długim, losowym hashem w nazwie pliku — to skaner luk w zabezpieczeniach Nessus, który instaluje usługę systemu Windows podczas zdalnego skanowania. Nawet legalne narzędzie wygląda podejrzanie na podstawie tego wyniku: nietypowa nazwa usługi, nazwa pliku przypominająca hash, dwie instalacje w odstępie minuty od siebie. Prawdziwy analityk musiałby to skorelować z rekordem zarządzania zmianami, aby potwierdzić autoryzację. W środowisku produkcyjnym należy je porównać z systemem zarządzania zmianami, aby zweryfikować, czy każda instalacja została autoryzowana.

## Łączenie kropek

Cofnijmy się i przyjrzyjmy wzorcowi w tych trzech ćwiczeniach. Zaczęliśmy od logów uwierzytelniania, aby wykryć działania siłowe, przeszliśmy do logów dostępu do sieci, aby wykryć enumerację, i sprawdziliśmy logi systemowe pod kątem…trwałośćpoprzez instalację usługi. Każde zapytanie dotyczyło innego źródła logów i innej fazy ataku, ale logika wykrywania była za każdym razem taka sama: agregacja według źródła, liczenie i wyszukiwanie wartości odstających. Ten schemat, zliczanie zdarzeń z jednego źródła i oznaczanie woluminów przekraczających linię bazową, stanowi podstawę detekcji opartej na progach. Konkretny identyfikator zdarzenia i typ źródła zmieniają się w zależności od celu, ale podejście analityczne jest przenoszone bezpośrednio.

Możemy teraz wykrywać pojedyncze wskaźniki ataku w logach uwierzytelniania, logach dostępu do sieci i logach systemowych. Jednak prawdziwe incydenty nie składają się z pojedynczego wskaźnika; łączą się one w łańcuchy w różnych fazach: rozpoznania, dostępu początkowego, utrwalania, a następnie ruchu poziomego. W kolejnym zadaniu zbadamy cykl reagowania na incydenty, który definiuje sposób, w jaki obrońcy zarządzają pełnym zakresem incydentu, od pierwszego wykrycia do odzyskania.

Wykryłeś atak. Próby siłowe powodują wyświetlanie się pulpitu nawigacyjnego, enumeracja katalogów internetowych jest oczywista, a podejrzana usługa właśnie pojawiła się na serwerze krytycznym. Co teraz? Różnica między incydentem kontrolowanym a katastrofalnym włamaniem często sprowadza się do tego, co wydarzy się w ciągu następnych 60 minut. Czy analityk podejmie eskalację? Czy zespół wie, do kogo zadzwonić? Czy istnieje jakiś plan działania, czy wszyscy improwizują?

W poprzednim zadaniu nauczyliśmy się wykrywać pojedyncze wzorce ataków w danych z logów. Każdy wzorzec był sygnałem, pojedynczym dowodem na to, że coś jest nie tak. Ale prawdziwy incydent to nie pojedynczy sygnał; to kaskada zdarzeń, która wymaga skoordynowanej, ustrukturyzowanej reakcji. Umiejętność rozpoznania ataku siłowego jest cenna. Wiedza o tym, co zrobić po jego wykryciu, odróżnia funkcjonalny zespół ds. bezpieczeństwa od takiego, który obserwuje naruszenie w zwolnionym tempie. Ta ustrukturyzowana reakcja to **cykl życia reakcji na incydent** .

## TenNISTSP 800-61 Rev 2 Cykl życia

Najpowszechniej przyjętym schematem reagowania na incydenty jest dokument [NIST Special Publication 800-61 Revision 2(otwiera się w nowej karcie)](https://csrc.nist.gov/pubs/sp/800/61/r2/final), opublikowana w 2012 roku. Definiuje ona cztery fazy, które tworzą cykl, a nie linię prostą:

1. **Przygotowanie** : Zbuduj potencjał, zanim cokolwiek pójdzie nie tak. Stwórz polityki, wdróż narzędzia monitorujące, przeszkol analityków, opracuj plany komunikacji, zdefiniuj procedury eskalacji. Zespół, który pomija tę fazę, improwizuje w czasie kryzysu.
2. **Wykrywanie i analiza** : Zidentyfikuj, że wystąpił incydent, a następnie określ jego zakres i wagę. To tutajSIEMAlerty, analiza logów i triaż są realizowane. Umiejętności, które ćwiczyliśmy w Zadaniu 4, czyli wykrywanie wzorców ataków siłowych, sygnalizowanie zdarzeń czyszczenia logów i rozpoznawanie instalacji usług, są wykorzystywane w tej fazie.
3. **Powstrzymanie, eliminacja i odzyskiwanie** : Zatrzymaj krwawienie, usuń zagrożenie i przywróć działanie. Krótkotrwałe powstrzymanie izoluje zainfekowane systemy. Eliminacja usuwa punkt zaczepienia atakującego. Odzyskiwanie przywraca działanie systemów, monitorując je w celu potwierdzenia, że ​​zagrożenie zniknęło.
4. **Działania poincydentalne** : Wyciągnij wnioski z tego, co się wydarzyło. Przeprowadź spotkanie podsumowujące, udokumentuj harmonogram, zidentyfikuj, co się sprawdziło, a co nie, i przekaż usprawnienia do fazy przygotowawczej.

Kluczowym wnioskiem jest ta strzałka prowadząca od działań poincydentalnych z powrotem do przygotowań. Każdy incydent uczy zespół czegoś. Być może w podręczniku brakowało jakiegoś kroku. Być może przechowywanie logów było zbyt krótkie, aby odtworzyć pełną oś czasu ataku. Być może ścieżka eskalacji była niejasna. Te lekcje stają się doskonalsze w przygotowaniach do kolejnego incydentu. Cykl życia jest cykliczny, ponieważ incydenty nigdy się nie kończą, a każdy z nich powinien wzmacniać zespół.

Norma NIST SP 800-61 Rev 2 ustala również trzy kluczowe definicje, które warto znać:

- **Wydarzenie** : Każde obserwowalne zdarzenie w systemie lub sieci
- **Zdarzenie niepożądane** : zdarzenie mające negatywne konsekwencje
- **Incydent bezpieczeństwa komputerowego** : naruszenie lub bezpośrednie zagrożenie naruszenia zasad bezpieczeństwa komputerowego, zasad akceptowalnego użytkowania lub standardowych praktyk bezpieczeństwa

Nie każde zdarzenie jest niekorzystne i nie każde zdarzenie niepożądane jest incydentem. Częścią procesu wykrywania i analizy jest dokonanie tego ustalenia.

W kwietniu 2025 r. NIST opublikował [SP 800-61 Rev 3(otwiera się w nowej karcie)](https://csrc.nist.gov/pubs/sp/800/61/r3/final), który zachowuje wszystkie trzy koncepcje, ale je aktualizuje: „zdarzenie” teraz wyraźnie obejmuje platformy chmurowe i wirtualne; „zdarzenie niepożądane” zostało rozszerzone o przyczyny niezwiązane z cyberbezpieczeństwem; a „incydent bezpieczeństwa komputerowego” został przemianowany na „incydent bezpieczeństwa cybernetycznego” zCIA-definicja do przodu triady zaczerpnięta zFISMA2014. Wersja 2 pozostaje najczęściej nauczanym modelem ze względu na przejrzystość koncepcji i to na niej się tutaj skupimy.

## Model SANS PICERL

W terenie spotkasz się z drugim modelem: modelem SANS **PICERL** . Dzieli on reakcję na sześć faz:

|Faza SANS|Mapy do fazy NIST Rev 2|
|---|---|
|**Przygotowanie**​|Przygotowanie|
|**Identyfikacja**​|Wykrywanie i analiza|
|**Powstrzymanie**​|Ograniczanie, eradykacja i odzyskiwanie|
|Radikacja **E**|Ograniczanie, eradykacja i odzyskiwanie|
|**Powrót** do zdrowia|Ograniczanie, eradykacja i odzyskiwanie|
|Wyciągnięte **wnioski**|Działania poincydentalne|

Kluczową różnicą jest szczegółowość: SANS traktuje powstrzymywanie, eliminację i odzyskiwanie jako odrębne fazy operacyjne, zamiast grupować je pod jedną etykietą. W praktyce powstrzymywanie, eliminacja i odzyskiwanie to odrębne działania o różnych celach i angażujące różne osoby. SANS wyraźnie to podkreśla. Żaden z modeli nie jest „lepszy”; opisują ten sam proces na różnym poziomie szczegółowości. Wiele organizacji korzysta z NIST do dokumentowania polityk, a SANS do podręczników operacyjnych.

![Model SANS PICERL](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779221097327.png)

## Studium przypadku: Kiedy frameworki zawodzą

Ramy działają tylko wtedy, gdy ludzie ich przestrzegają. Przyjrzyjmy się dwóm naruszeniom, w których poszczególne fazy uległy awarii.

**Target, 2013.** FireEye, platforma Target do wykrywania złośliwego oprogramowania, zidentyfikowała złośliwe oprogramowanie BlackPOS i wygenerowała alert 30 listopada 2013 r. Faza wykrywania zadziałała. Narzędzie wykonało swoje zadanie. Ale BangaloreSOCZespół, który otrzymał alert, nie zdołał skutecznie przekazać go do zespołu bezpieczeństwa w Minneapolis. Część „Analiza i eskalacja” w ramach „Wykrywania i Analizy” zawiodła. Od pierwszego alertu do jego powstrzymania minęło osiemnaście dni. Rezultat: 40 milionów skradzionych rekordów kart płatniczych, 162 miliony dolarów kosztów naruszenia bezpieczeństwa oraz rezygnacja prezesa i dyrektora ds. informatyki. Jak omówiliśmy w Zadaniu 2, zmęczenie alertami odegrało tu pewną rolę, ale głębszy błąd miał charakter proceduralny. Nie było wymuszonej ścieżki eskalacji, która gwarantowałaby, że krytyczny alert nie zostanie po cichu porzucony.

**SolarWinds SUNBURST, 2020.** APT29 wprowadził backdoora do procesu kompilacji SolarWinds Orion. Trojanizowana aktualizacja została rozesłana do około 18 000 organizacji. Backdoor pozostawał aktywny przez około dziewięć miesięcy, zanim FireEye wykrył go w grudniu 2020 roku. Dziewięć miesięcy. To błąd wykrywania i analizy mierzony nie w dniach, ale w sezonach.Średnia dzienna dnia (MTTD)Metryka, którą omówiliśmy w Zadaniu 2, odzwierciedla dokładnie ten problem: gdy czas między naruszeniem a wykryciem rozciąga się na miesiące, atakujący ma praktycznie nieograniczoną swobodę poruszania się w różnych kierunkach, eksfiltracji danych i ustanawianiatrwałośćPrzypadek SolarWinds pokazuje również, dlaczego przechowywanie logów ma znaczenie. Jeśli organizacja przechowuje logi tylko przez 90 dni, nie jest w stanie odtworzyć tego, co wydarzyło się podczas dziewięciomiesięcznego włamania. Faza działań po incydencie w organizacjach dotkniętych awarią SolarWinds doprowadziła do szeroko zakrojonych zmian w przygotowaniach: ulepszona weryfikacja łańcucha dostaw, dłuższe zasady przechowywania logów oraz funkcje wykrywania zachowań, które wyszukują anomalie, a nie pasują do znanych wskaźników.

## Ugruntowanie struktury: wykrywanie i analiza w działaniu

Frameworki mogą wydawać się abstrakcyjne, dopóki nie połączymy ich z rzeczywistymi artefaktami. Ugruntujmy fazę wykrywania i analizy na konkretnym przykładzie z zestawu danych BOTSv1. W zadaniu 4 wymieniliśmy identyfikator zdarzenia `1102`(wyczyszczenie dziennika audytu bezpieczeństwa) jako wskaźnik o wysokim stopniu wiarygodności czyszczenia po naruszeniu. Teraz uruchom to zapytanie i zobacz, jak wygląda w praktyce.

W pasku wyszukiwania Splunk uruchom:

```spl
index=botsv1 sourcetype=WinEventLog:Security EventCode=1102
```

Jeśli pojawią się wyniki, każde zdarzenie reprezentuje moment, w którym ktoś wyczyścił dziennik zdarzeń zabezpieczeń systemu Windows. To właśnie taki artefakt nie może umknąć uwadze zespołu ds. wykrywania i analizy. Atakujący, który czyści dzienniki, aktywnie próbuje usunąć dowody, co świadczy o dwóch rzeczach: już zhakował system i ma wystarczającą wiedzę, aby zatrzeć ślady. To pojedyncze zdarzenie zmienia klasyfikację ważności całego incydentu.

Należy pamiętać o jednej rzeczy. W zbiorze danych BOTSv1 zdarzenia czyszczenia logów mogą być ograniczone lub nie występować wcale, ponieważ jest to scenariusz CTF, a nie środowisko produkcyjne. W rzeczywistym przedsiębiorstwie identyfikator zdarzenia `1102`występuje na tyle rzadko, że każde zdarzenie poza udokumentowaną konserwacją powinno skutkować natychmiastowym dochodzeniem i eskalacją.

Wzorzec, który właśnie zastosowaliśmy, polegający na wykrywaniu poszczególnych wskaźników i klasyfikowaniu ich w ramachIRCykl życia i wykorzystanie ich do określenia zakresu i wagi zagrożenia stanowi sedno działań podejmowanych w fazie wykrywania i analizy. Narzędzia różnią się w zależności od organizacji, ale proces pozostaje ten sam: identyfikacja sygnałów, ocena kontekstu i odpowiednia eskalacja.

Omówiliśmy już ramy, które wskazują obrońcom, jak zarządzać incydentem od momentu jego wykrycia, przez odzyskanie, aż po wyciągnięcie wniosków. Jednak zarządzanie reakcją to tylko połowa problemu. Aby w pełni zrozumieć działania atakującego, obrońcy potrzebują ustrukturyzowanej bazy wiedzy o technikach przeciwnika, wspólnego języka, który odwzorowuje zachowania atakujących na znane wzorce. W kolejnym zadaniu zajmiemy się właśnie tym:MITRAStruktura ATT&CK.

W ciągu ostatnich kilku zadań zbudowaliśmy poważne możliwości. Potrafimy poruszać się poSIEM, wykrywać ataki siłowe, lokalizować enumerację katalogów internetowych, identyfikować instalacje usług i strukturyzować naszą odpowiedź, korzystając zNIST IRCykl życia. Ale rozważmy następujący scenariusz: kończysz test penetracyjny i teraz musisz przekazać swoje ustalenia zespołowi bezpieczeństwa klienta, platformie analizy zagrożeń lub organizacji partnerskiej w innym kraju. Jak opisać działanie atakującego w sposób zrozumiały dla każdego obrońcy na świecie?

Potrzebujesz wspólnego języka dla zachowań przeciwnika. Jak wspomnieliśmy w poprzednim zadaniu, cykl życia IR mówi nam, _jak_ zarządzać incydentem. To zadanie dostarcza nam słownictwa do opisania _tego, co_ faktycznie zrobił przeciwnik, oraz ram do decydowania, które wskaźniki warto zablokować.

## MITRAATT&CK: Wspólny słownik zachowań adwersarzy

Poznałeś Cyber ​​Kill Chain na wcześniejszym etapie ścieżki. Daje on siedem liniowych faz ataku, od rozpoznania do działań na cele. To solidny model mentalny, ale ma swoje ograniczenia. Prawdziwe ataki nie są liniowe; atakujący cofają się, pomijają etapy i działają jednocześnie na wielu celach. Cyber ​​Kill Chain nie przypisuje również konkretnych zachowań atakujących do grup, które je stosują.

Ramy **MITRE ATT&CK** (Adversarial Tactics, Techniques, and Common Knowledge) rozwiązują te problemy. Wyobraź sobie ATT&CK jako słownik zachowań przeciwnika. Tak jak słownik porządkuje słowa według definicji i użycia, tak ATT&CK porządkuje działania atakującego według _powodu, dla którego_ coś robi (cel), _co_ robi (metoda) i _jak_ konkretnie to robi (implementacja). Z technicznego punktu widzenia oznacza to, że ramy są podzielone na trzy poziomy:

- **Taktyka** (14 w macierzy Enterprise): Cel przeciwnika. Każda taktyka odpowiada na pytanie „dlaczego atakujący to robi?”. Na przykład taktyka „ _Dostęp do danych uwierzytelniających_ ” (TA0006) oznacza, że ​​celem atakującego jest kradzież danych uwierzytelniających konta.
- **Techniki** : Metoda stosowana przez przeciwnika do osiągnięcia celu taktycznego. W ramach _dostępu do danych uwierzytelniających_ jedną z technik jest metoda _brute-force_ (T1110), polegająca na próbie odgadnięcia wielu haseł w celu odgadnięcia właściwego.
- **Podtechniki** : Bardziej szczegółowa implementacja techniki. W przypadku _ataku siłowego_ , podtechnika T1110.001 to _odgadywanie hasła_ , gdzie atakujący atakuje określone konto, wielokrotnie próbując podać hasło.

**Poniżej przedstawiono** podtechniki , czyli udokumentowane implementacje w świecie rzeczywistym przez określone grupy zagrożeń lub złośliwe oprogramowanie. APT29 wykorzystuje tylne drzwi SUNBURST do komunikacji przezDNS„to” `avsvmcloud.com`to udokumentowana procedura w ramach `T1071.004`protokołu warstwy aplikacji (DNS). Procedury osadzają abstrakcyjne ramy w obserwowanej rzeczywistości.

W przeciwieństwie do siedmiu liniowych kroków Kill Chain, 14 taktyk ATT&CK jest nieliniowych. Atakujący może osiągnąć _stan Persistence_ przed _eskalacją uprawnień_ lub wielokrotnie powracać do _stanu Discovery_ w trakcie operacji. Struktura jest również stale aktualizowana w miarę, jak badacze dokumentują nowe zachowania przeciwnika, co czyni ją żywą bazą wiedzy, a nie statycznym modelem.

## Piramida bólu: nie wszystkie wskaźniki są sobie równe

Wykrycie atakującego to jedno. Sprawienie mu _bólu_ to drugie. W książce Davida Bianco „ **Piramida bólu”** (2013) sześć typów wskaźników uszeregowano według stopnia trudności operacyjnych, jakie stwarzają atakującemu, gdy obrońca je wykryje i zablokuje.

Wyobraź sobie piramidę z sześcioma warstwami. Podstawa jest szeroka i łatwo na niej stanąć; szczyt jest wąski i trudno na nim utrzymać równowagę. Każda warstwa reprezentuje typ wskaźnika:

|Warstwa|Typ wskaźnika|Poziom bólu|Przykład BOTSv1|
|---|---|---|---|
|6 (góra)|TTP|Trudny|Zachowanie siłowe (T1110)|
|5|Narzędzia|Wyzywający|Konkretna struktura exploita używana przez`po1s0n1vy`|
|4|Artefakty sieciowe/hosta|Irytujący|Wzorce URI z wyliczenia katalogów|
|3|Nazwy domen|Prosty|Domena C2|
|2|Adresy IP|Łatwy|Źródło adresu IP atakującego|
|1 (dół)|Wartości skrótu|Trywialny|MD5 pliku binarnego złośliwego oprogramowania|

Logika jest prosta. Jeśli zablokujesz skrót złośliwego oprogramowania, atakujący przekompiluje plik binarny, wprowadzając jednobajtową zmianę, generując zupełnie nowy skrót w ciągu kilku sekund. Jeśli zablokujesz adres IP, uruchomią nowy serwer w chmurze w ciągu kilku minut. Ale jeśli wykryjesz i zablokujesz sam _wzorzec zachowania_ , atakujący będzie musiał gruntownie przeprojektować swoje działanie. To prawdziwy problem.

Rozważmy to w przypadku SolarWinds SUNBURST (2020). Atak ten był odwzorowany na wiele technik ATT&CK: `T1195.002`(kompromis w łańcuchu dostaw), `T1071.004`(C2 oparty na DNS) i `T1036.005`(maskarada). Gdy obrońcy zablokowaliC2domena `avsvmcloud.com`, co było działaniem warstwy 3 (Simple). APT29 mógł zarejestrować nową domenę. Jeśli jednak obrońcy wykryją zachowanie _mechanizmów_ aktualizacji oprogramowania wysyłających zakodowane zapytania DNS do nieznanych domen, atak obejmie warstwę TTP, a atakujący będzie musiał przeprojektować całą infrastrukturę C2.

## Mapowanie BOTSv1 na ATT&CK

Oprzyjmy ten schemat na atakach, które już wykryliśmy. Każdy wzorzec z naszych wcześniejszych zapytań jest odwzorowywany na konkretną technikę ATT&CK:

|Wzór ataku|Technika ATT&CK|ID|
|---|---|---|
|Próby siłowego logowania|Brute-Force: zgadywanie haseł|T1110.001|
|Skanowanie portów i usług|Odkrywanie usług sieciowych|T1046|
|Wyliczanie katalogów internetowych|Aktywne skanowanie: skanowanie listy słów|T1595.003|
|Ruch boczny poprzez SMB|Usługi zdalne: udziały administracyjne SMB/Windows|T1021.002|
|Czyszczenie dziennika audytu|Usuwanie wskaźników: Wyczyść dzienniki zdarzeń systemu Windows|T1070.001|

Teraz przyjrzyjmy się wzorcowi, którego jeszcze nie badaliśmy. W swojej instancji Splunk uruchom następujące zapytanie, aby sprawdzić zdarzenia tworzenia procesów:

```spl
index=botsv1 sourcetype=WinEventLog:Security EventCode=4688 | table _time, New_Process_Name, Creator_Process_Name | head 20
```

![Strona wyszukiwania Splunk](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779220119152.png)

To zapytanie wyszukuje identyfikator zdarzenia  `4688`(utworzenie nowego procesu) i wyświetla uruchomiony proces wraz z procesem, który go uruchomił. Spójrz na wyniki. Powinny pojawić się wpisy, w których zmienna `cmd.exe`lub `powershell.exe`jest generowana przez proces nadrzędny, który normalnie nie wywołałby interpretera poleceń, takiego jak proces serwera WWW lub plik binarny usługi. Gdy atakujący uzyskuje dostęp do systemu i musi wykonać polecenia, prawie zawsze sięga po zmienną `cmd.exe`lub `powershell.exe`. To zachowanie jest odzwierciedleniem techniki ATT&CK `T1059`(interpreter poleceń i skryptów).

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

Należy pamiętać o jednej rzeczy. W tym środowisku laboratoryjnym zbiór danych BOTSv1 zawiera wystarczającą liczbę zdarzeń tworzenia procesów, co ułatwia identyfikację nietypowych relacji nadrzędny-podrzędny. W środowisku produkcyjnym z setkami punktów końcowych i tysiącami legalnych procesów generujących interpretery poleceń podczas wdrażania oprogramowania i administrowania systemem, konieczne byłoby ustalenie punktu odniesienia dla normalnych relacji procesów nadrzędny-podrzędny i generowanie alertów tylko w przypadku odchyleń. Warto o tym wiedzieć, zanim zastosujesz to podejście poza laboratorium.

## Nawigator ATT&CK

MITRE udostępnia bezpłatne narzędzie internetowe o nazwie **ATT&CK Navigator** pod adresem `https://mitre-attack.github.io/attack-navigator/`. Przedstawia ono pełną macierz przedsiębiorstwa jako interaktywną siatkę, w której można kodować kolorami techniki, aby wizualizować, które z nich może wykryć organizacja, które wykorzystuje konkretna grupa zagrożeń lub które pojawiły się w konkretnym incydencie. Instalacja nie jest wymagana. Aby z niej skorzystać, otwórz Navigatora w przeglądarce (na własnym komputerze, a nie na komputerze).Maszyna wirtualna) i zobacz, w jaki sposób 14 kolumn taktyk jest wypełnianych technikami.

## Odbicie

Cofnijmy się. Rozpoczęliśmy to zadanie od zidentyfikowania luki: potrzeby wspólnego języka. Wypełniliśmy ją hierarchiczną strukturą ATT&CK (taktyki, techniki, podtechniki, procedury), a następnie nałożyliśmy na nią Piramidę Bólu, aby ocenić, które wskaźniki są rzeczywiście istotne. Przenoszalny wzorzec to priorytetyzacja według kosztu przeciwnika. Niezależnie od tego, czy piszesz reguły wykrywania, czy alokujeszSOCZasoby lub planowanie zaangażowania zespołu purpurowego, pytanie „jak bardzo to szkodzi atakującemu?” powinno kierować twoimi decyzjami. Blokowanie hasza jest darmowe i prawie bezużyteczne; wykrywanieTTPjest trudniejszy do zbudowania, ale zmusza przeciwnika do gruntownej przebudowy.

Mamy już wszystkie niezbędne elementy: przepływ pracy SOC, umiejętności SIEM, wiedzę o identyfikacji zdarzeń, cykl życia IR oraz ramy analizy zagrożeń. W kolejnym zadaniu połączymy wszystko w kompletne śledztwo w sprawie ataku na Wayne Corp, analizując cały łańcuch zdarzeń, od wstępnego alertu po mapowanie ATT&CK.

Jest godzina 8:47 rano twojego pierwszego dnia w Wayne Corp. SO Wciąż uczysz się, gdzie jest ekspres do kawy, gdy pojawia się alert Suricata: nietypowy ruch na serwerze internetowym. Twój analityk L2 zadzwonił, że jest chory. Kolejka jest Twoja. Musisz dokonać selekcji tego alertu, ustalić, kto za nim stoi, prześledzić, co zrobił i zdecydować, co dalej. Każda umiejętność, którą rozwinęliśmy w tym pokoju, SPL zapytania, interpretacja identyfikatora zdarzenia, IRcykl życia, mapowanie ATT&CK, zbiega się tutaj.

To nie są ćwiczenia. Poćwiczmy.

## Krok 1: Selekcja alertów

Alert informuje o „nietypowym ruchu”. To niejasne. Naszym pierwszym zadaniem jest zawężenie go do konkretnego źródła. Jak omówiliśmy w Zadaniu 3,Splunkpozwala nam agregować i sortować miliony zdarzeń w ciągu kilku sekund. Zaczynamy od źródła alertu: `suricata`typu źródła.

Uruchom następujące zapytanie w Splunk:

```spl
index=botsv1 sourcetype=suricata NOT src_ip=192.168.* NOT src_ip=10.*
| stats count by src_ip
| sort -count
| head 1
```

Ta funkcja zlicza wszystkie alerty IDS Suricata pogrupowane według źródłowego adresu IP, filtrując prywatne zakresy RFC1918, aby skupić się na atakujących z zewnątrz. Adres IP na szczycie listy to host zewnętrzny, który generuje więcej alertów IDS przeciwko Wayne Corp niż jakiekolwiek inne źródło. To jest nasz główny podejrzany.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Po co filtrować prywatne adresy IP?** W tym zbiorze danych hosty wewnętrzne generują dużą liczbę alertów Suricata, ponieważ sprawdzany jest również ruch między segmentami sieci. Filtrowanie zewnętrznych adresów IP ujawnia atakującego, który zainicjował atak spoza sieci. Podczas prawdziwego śledztwa należałoby również zbadać główny wewnętrzny adres IP, ponieważ może on wskazywać na zainfekowany host wewnętrzny używany jako punkt kontaktowy.

Zapisz ten adres IP. Każde zapytanie od tego momentu będzie się na nim opierać.

## Krok 2: Przejdź do dzienników dostępu do sieci

Znając adres IP atakującego, sprawdzamy teraz, co robił na serwerze WWW. Przechodzimy z `suricata`do `iis`Wayne Corp.IISDzienniki dostępu do serwera WWW. IIS używa formatu dziennika W3C, więc pole adresu IP klienta to `c_ip`, metoda żądania to `cs_method`, a ścieżka URI to `cs_uri_stem`. Dokładniej, chcemy wiedzieć, któryURIścieżki otrzymały najwięcej `POST`żądań od naszego podejrzanego, ponieważ `POST`żądania przenoszą dane do serwera i są powszechnie wykorzystywane do przesyłania formularzy, plików i ładunków eksploatacyjnych.

Zastąp `<attacker_ip>`adresem IP znalezionym w kroku 1:

```spl
index=botsv1 sourcetype=iis c_ip=<attacker_ip> cs_method=POST
| stats count by cs_uri_stem
| sort -count
| head 1
```

URI na górze wyników to punkt końcowy, który atakujący zaatakował najmocniej. To wskazuje nam cel ataku: konkretną stronę lub skrypt, który wykorzystywał.

## Krok 3: Potwierdź rozpoznanie

Przed wykorzystaniem atakujący zazwyczaj przeprowadzają rekonesans. W zadaniu 4 dowiedzieliśmy się, że atak brute force na katalogi internetowe generuje charakterystyczny podpis: falę odpowiedzi HTTP 404 (Nie znaleziono) z jednego źródła. Sprawdźmy, czy nasz atakujący zastosował się do tego schematu:

```spl
index=botsv1 sourcetype=iis c_ip=<attacker_ip> sc_status=404
| stats count
```

Jeśli liczba ta wynosi setki lub tysiące, atakujący uruchomił skaner listy słów na serwerze internetowym Wayne Corp przed próbą wykorzystania luki. Jest to odzwierciedlenie techniki ATT&CK `T1595.003`(Active Scanning:Lista słówSkanowanie) w ramach taktyki rozpoznania, czyli dokładnie to, co omówiliśmy w zadaniu 4.

## Krok 4: Sprawdź dzienniki zdarzeń systemu Windows pod kątem zdarzeń poeksploatacyjnych

Atakujący, który znajdzie sposób na włamanie, rzadko zatrzymuje się na serwerze WWW. Musimy sprawdzić, czy naruszenie rozprzestrzeniło się na środowisko Windows. Używając adresu IP atakującego jako frazy wyszukiwania w wolnym tekście, przeszukujemy zdarzenia uwierzytelniania:

```spl
index=botsv1 sourcetype=WinEventLog:Security (EventCode=4624 OR EventCode=4625) <attacker_ip> | stats count by EventCode
```

Wyszukiwanie adresu IP jako czystego tokena pozwala na znalezienie go w dowolnym miejscu surowego zdarzenia, co jest najpewniejszym podejściem w konfiguracjach analizy dziennika zdarzeń systemu Windows. `4625`Wpisy identyfikatorów zdarzeń z adresu IP atakującego wskazują na nieudane próby logowania do hostów Windows. `4624`Wpisy identyfikatorów zdarzeń wskazują na udane logowania. Jeśli oba wpisy występują, atakujący przeszedł z serwera WWW do uwierzytelniania Windows, rozszerzając zakres incydentu.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Oczekiwany wynik dla tego zestawu danych.** Atak na Wayne Corp. koncentrował się na wykorzystaniu aplikacji internetowych, a nie na bezpośrednich atakach na poświadczenia systemu Windows z zewnętrznego adresu IP. Dzienniki zabezpieczeń systemu Windows mogą zwrócić zero wyników dla zewnętrznego adresu IP atakującego, który zidentyfikowaliśmy wcześniej. Jest to samo w sobie pouczające: informuje, że atak atakującego ograniczył się do warstwy aplikacji internetowych w dostępnych danych z dziennika — nie uwierzytelniał się on bezpośrednio na hostach Windows z zewnętrznego adresu IP. W rzeczywistym dochodzeniu, zero wyników w tym przypadku skłoniłoby do sprawdzenia, czy serwer WWW był używany jako punkt kontaktowy do uzyskania dostępu do wewnętrznych systemów Windows.

## Rekonstrukcja łańcucha ataku

Podsumowując nasze ustalenia, `po1s0n1vy`atak na Wayne Corp przebiegał według rozpoznawalnego ciągu zdarzeń:

1. **Rozpoznanie** (T1595.003): skanowanie listy słów na serwerze internetowym wygenerowało ponad 2000 `404`odpowiedzi — potwierdzone za pomocą dzienników FortiGate IPS i IIS
2. **Początkowe wykorzystanie** : Ponad 14 000 skoncentrowanych `POST`żądań `/joomla/index.php/component/search/`wskazuje na aktywną eksploatację systemu CMS Joomla — prawdopodobnie atak typu SQL injection
3. **Wpływ** (T1491.002): Utrzymująca się `POST`aktywność w określonych punktach końcowych Joomla jest zgodna z publicznie ogłoszonym incydentem niszczenia sieci przez firmę Wayne Corp.

Każde znalezisko pochodziło z innego źródła. Suricata wskazała nam atakującego. FortiGateIPSPotwierdzono wolumen skanowania. Logi internetowe IIS ujawniły cel ataku i wolumen żądań. Żadne pojedyncze źródło logów nie ujawniło pełnego obrazu.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

Należy pamiętać o jednej rzeczy. Korelacja między źródłami działa tutaj bezproblemowo, ponieważ wszystkie źródła danych są wstępnie gromadzone w jednym indeksie Splunk. W środowisku produkcyjnym z rozproszoną infrastrukturą, opóźnieniami w przekazywaniu logów i niepełnym pokryciem, konieczne byłoby uwzględnienie przesunięcia czasowego między źródłami i sprawdzenie, czy każde istotne źródło logów jest faktycznie gromadzone. Warto o tym wiedzieć, zanim zastosujesz to podejście poza laboratorium.

## Mapowanie cyklu życia IR

Gdzie to nas zostawia w tej sytuacji?NISTCykl życia SP 800-61 Rev 2, który omawialiśmy w Zadaniu 5? Właśnie zakończyliśmy fazę wykrywania i analizy: dokonaliśmy wstępnej selekcji alertu, zidentyfikowaliśmy atakującego, określiliśmy zakres incydentu w wielu źródłach danych i zrekonstruowaliśmy łańcuch ataku. Kolejną fazą jest powstrzymanie, eliminacja i odzyskiwanie, w której zespół izoluje zainfekowany serwer WWW, usuwa dostęp atakującego i przywraca uszkodzoną witrynę ze znanej, dobrej kopii zapasowej.

## Refleksja metodologiczna

Cofnijmy się i przyjrzyjmy schematowi. Zaczęliśmy od pojedynczego alertu z jednego źródła danych (Suricata), wyodrębniliśmy wskaźnik (adres IP atakującego) i wykorzystaliśmy go jako punkt odniesienia do przeszukiwania coraz głębszych źródeł danych: dzienników internetowych dla aktywności na poziomie aplikacji, a następnie dzienników zdarzeń systemu Windows dla kompromitacji na poziomie hosta. Na każdym etapie poprzednie odkrycie kształtowało kolejne zapytanie. Ten przepływ pracy, od selekcji alertów, przez ekstrakcję wskaźników, po przechodzenie między źródłami i rekonstrukcję osi czasu, stanowi podstawową pętlę dochodzeniową dla każdego analityka SOC, niezależnie od…SIEMPlatforma lub rodzaj ataku. Konkretne zapytania ulegają zmianie, ale schemat pozostaje ten sam.

W tym dochodzeniu wykorzystano wszystkie umiejętności z sali: zapytania SPL z zadania 3, interpretację identyfikatorów zdarzeń z zadania 4, cykl życia IR z zadania 5 i mapowanie ATT&CK z zadania 6. W następnym zadaniu cofniemy się i połączymy wszystko, czego się nauczyliśmy, z szerszym obrazem tego, jakniebieski zespółWiedza ta wzmacnia Twoją pracę jako testera penetracyjnego.

Teraz, gdy już usiedliście po obu stronach ekranu, w jaki sposób zmienia się Wasze podejście do kolejnego testu penetracyjnego?

To nie jest pytanie retoryczne. W ciągu ostatnich siedmiu zadań przeszliśmy od zrozumienia, jakSOCdziała, do nawigacjiSIEM, odczytywanie wzorców ataków z logów, strukturyzacja reakcji na incydenty, mapowanie zachowań przeciwnika za pomocą ATT&CK, aż po przeprowadzenie pełnego śledztwa w Wayne Corp. Jak wspomnieliśmy w zadaniu 7, śledztwo końcowe połączyło wszystkie umiejętności w jednym procesie. Teraz połączmy to z tym, dlaczego tu jesteś: szkolisz się na testera penetracyjnego, a wszystko, czego się właśnie nauczyłeś, czyni cię lepszym.

## Trzy drogiNiebieski zespółWiedza poprawia Twoje testy penetracyjne

**Ukrycie.** Teraz wiesz, co wyzwala alerty. Setki `EventCode=4625`zdarzeń z jednego adresu IP w ciągu dwóch minut wyświetlają się na pulpicie każdego centrum bezpieczeństwa (SOC) w budynku. Powolny, rozproszony test uwierzytelniania rozłożony na wiele godzin na wielu kontach wygląda jak typowy szum uwierzytelniania. Pentesterzy, którzy rozumieją progi wykrywania, projektują działania, które testują rzeczywiste mechanizmy obronne, zamiast uruchamiać pierwszy alarm i dać się złapać w holu.

**Raportowanie.** Widziałeś, co analityk poziomu pierwszego robi z wynikami: klasyfikuje je, sprawdza kontekst i eskaluje na podstawie dowodów. Pentesterzy, którzy rozumieją ten proces, tworzą wyniki, na podstawie których obrońcy mogą faktycznie działać. Zamiast „SQL„wstrzyknięcie znalezione na stronie logowania”, wpisujesz ustalenie ze źródłem, w którym pojawia się dowód, zdarzenieIdentyfikatorySOC powinien monitorować, a identyfikator techniki ATT&CK powinien zapewnić spójną klasyfikację. Twój raport staje się materiałem do analizy, z którego może skorzystać zespół niebieski, a nie dokumentem, który musi przetłumaczyć.

**Zakres.** Teraz rozumiesz, że każdy incydent wyzwala pełnąIRCykl życia: wykrywanie, analiza, powstrzymywanie, eliminacja, odzyskiwanie, przegląd po incydencie. To tygodnie pracy dla zespołu ds. bezpieczeństwa. Pentesterzy, którzy realistycznie podchodzą do tego zakresu zadań, ustalają zasady zaangażowania, które testują zabezpieczenia bez konieczności poświęcania klientowi miesięcy na czyszczenie.

## Pętla sprzężenia zwrotnego zespołu Purple

W tym pomieszczeniu nieustannie powracaliśmy do idei, że czerwony i niebieski to nie są odrębne dyscypliny. To dwie połowy tej samej pętli sprzężenia zwrotnego. Atakujący wykonuje technikę; obrońca ją wykrywa (lub nie); obie strony powtarzają te same czynności. To właśnie esencja pracy w fioletowym zespole i jedna z najcenniejszych ścieżek kariery w branży bezpieczeństwa. Specjaliści, którzy potrafią działać po obu stronach tej pętli, którzy potrafią stworzyć mechanizm wykrywania, a następnie go ominąć, są niezmiennie najtrudniejsi do zatrudnienia i mają największy wpływ na każdy zespół.

Potraktuj to jako model kariery, a nie tylko zestaw umiejętności. Każdy test penetracyjny, który przeprowadzisz od tego momentu, to okazja do odnotowania, które z twoich działań zostałyby wykryte, a które umknęły. Ta obserwacja, zarejestrowana i udostępniona, to właśnie praca w zespole fioletowym w praktyce.

## Co dalej na ścieżce edukacyjnej

W tym pomieszczeniu omawiano obronę reaktywną: monitorowanie alertów, triażowanie incydentów, reagowanie po wystąpieniu zdarzenia. W kolejnym pomieszczeniu w module 13,DevSecOps101, przenosi nacisk na proaktywne bezpieczeństwo. Zamiast czekać na atak i dopiero wtedy reagować, DevSecOps integruje testy bezpieczeństwa z samym procesem rozwoju oprogramowania, wykrywając luki w zabezpieczeniach, zanim dotrą one do produkcji. To różnica między strażą pożarną, która reaguje na pożary, a przepisami budowlanymi, które im zapobiegają.

Oto jak umiejętności się ze sobą łączą:

|Pokój|Centrum|Kiedy bezpieczeństwo się dzieje|
|---|---|---|
|Perspektywa Niebieskiego Zespołu (ten pokój)|Operacje SOC, SIEM, cykl życia IR, informacje o zagrożeniach|Po wdrożeniu, w odpowiedzi na ataki|
|DevSecOps 101 (następne pomieszczenie)|Bezpieczeństwo wCI/płyta CD, automatyczne testowanie, przesunięcie w lewo|W trakcie rozwoju, przed wdrożeniem|

Oba podejścia są konieczne. Żadne z nich nie zastępuje drugiego. Skuteczny program bezpieczeństwa wymaga obrońców, którzy potrafią reagować na incydenty _, oraz_ procesów, które zapobiegają ich wystąpieniu.

Ta sala dała Ci perspektywę obrońcy: ludzi, narzędzia, frameworki i proces badawczy, które stoją za każdym testem penetracyjnym, jaki kiedykolwiek przeprowadzisz. Kontynuuj tę perspektywę. W następnej sali przyjrzymy się, jak bezpieczeństwo integruje się bezpośrednio z cyklem życia oprogramowania dzięki DevSecOps.
