---

Czym jest incydent cybernetyczny?

Zanim zagłębimy się w reagowanie na incydenty i zarządzanie nimi, warto najpierw omówić, czym jest cyberincydent. Zazwyczaj nie zaczynamy od cyberincydentu; zanim do niego dojdziemy, sytuacja się komplikuje.

![Zespół SOC](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/26b59b5363679f01caddcbde9f76c0a2.png)Zwykle wszystko zaczyna się odSOC(Centrum Operacji Bezpieczeństwa). Zespół analityków monitoruje bezpieczeństwo organizacji. W istocie zespół ten monitoruje **_zdarzenia_** w systemie organizacji. Jeśli zdarzenie jest anomalią lub nieoczekiwane, generowany jest **_alert_** . Alerty mogą być nadal nieprawidłowe, dlatego analitycy badają je dalej. Jeśli jednak alert jest prawdziwy, zespół przeprowadza procedurę triażu w celu określenia jego wagi. Jeśli waga alertu jest wystarczająca, zgłaszany jest _**incydent .**_

TenSOCMożna zatem postrzegać je jako filtr. Nie wszystkie zdarzenia trafiają do incydentów. Na przykład organizacje często otrzymują tysiącephishinge-maili każdego dnia. Większość z nich jest automatycznie blokowana przez systemy zapobiegania włamaniom, takie jak filtr antyspamowy. Nawet gdyby użytkownik wchodził w interakcję z większością tych e-maili i uruchamiał złośliwe oprogramowanie, oprogramowanie antywirusowe lub Endpoint Detection and Response automatycznie by to zablokowało. W takich przypadkach zostanie wygenerowany alert, aSOCzespół zajmie się tym, np. aktualizacją reguł filtrowania poczty lub podpisówAVLubEDR.

Z drugiej strony, incydent ma miejsce, gdy w fazie triażu odkrywamy, że alert może mieć jeszcze dalsze konsekwencje i nie dysponujemy wszystkimi ![Zainfekowana maszyna](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/24038ac27be5cfac14434bece4c40e3d.png)informacjami niezbędnymi do poradzenia sobie z nim. Załóżmy na przykład, że wygenerowano alert informujący o nietypowym logowaniu do jednego z naszych serwerów. Mamy kilka pytań, na które wciąż czekamy:

1. Czyje konto zostało użyte?
2. Skąd nastąpiło logowanie?
3. Gdzie to konto było używane przed zalogowaniem?
4. Czy na tym koncie zaobserwowano jakąś inną potencjalnie nietypową aktywność?  

Jeśli stopień zagrożenia jest wystarczająco wysoki, można zgłosić alarm dotyczący incydentu. Później omówimy różne poziomy reagowania na incydenty.  

Reagowanie na incydenty i zarządzanie nimi

Gdy poziom zagrożenia jest na tyle wysoki, że staje się incydentem, zazwyczaj wkraczają Reakcja na Incydenty i Zarządzanie Incydentami. Często te dwie funkcje są łączone i nazywane po prostu Reakcją na Incydenty. Warto jednak omówić ich odrębne cechy.  

**Reagowanie na incydenty**

Reagowanie na incydenty obejmuje techniczny aspekt postępowania z incydentem. Ta część odpowiada za odpowiedź na główne pytanie:

_**Co się stało?**_

Aby odpowiedzieć na to pytanie, zespół reagowania na incydenty wykorzystuje szereg technik i technologii. Dochodzenia te często rozpoczynają się wSOCpoprzez sprawdzenie informacji dostarczonych wraz ze zdarzeniem, które wywołało alert. Można to zrobić za pomocą jednego z następujących narzędzi:

- EDRLubAVAlert – Zazwyczaj te narzędzia generują alerty w przypadku wystąpienia nietypowej aktywności na określonym hoście. Na przykładEDRmoże ostrzegać o próbach monitorowania naciśnięć klawiszy przez użytkownika.
- SiećUzyskiwaćAlert – Podsłuchy sieciowe wysyłają alerty o nietypowej aktywności sieciowej. Na przykład, może pojawić się alert, że host skanuje inne hosty w sieci.
- SIEMAlert - Zarządzanie informacjami i zdarzeniami bezpieczeństwa (SIEM) system mógłby wygenerować alert dotyczący niestandardowej reguły utworzonej przez analityków. Na przykład, reguły uniemożliwiającej podróżowanie, w której konto użytkownika jest logowane jednocześnie z dwóch różnych krajów.

Po utworzeniu alertu analityk otrzymuje wiele informacji. Pierwszym krokiem jest ich analiza, aby lepiej zrozumieć sytuację. W tych systemach, po wygenerowaniu alertu, dołączane są do niego również inne kluczowe informacje. Na przykład w przypadkuSIEMalert, analityk będzie mógł przejrzeć nie tylko ostatnie zdarzenia logowania na koncie użytkownika, ale także historię zdarzeń logowania z ostatnich kilku miesięcy.

Czasami jednak informacje o alercie są niewystarczające i musimy zebrać więcej informacji niż te, które są obecnie dostępne. Ten proces jest zazwyczaj określany jako informatyka śledcza. W tym przypadku przeprowadzamy znacznie bardziej praktyczne dochodzenie, które może obejmować następujące czynności:

- Odzyskanie dysku twardego z zainfekowanego komputera w celu zbadania, w jaki sposób złośliwe oprogramowanie się na nim znalazło.
- Odzyskiwanie danych z pamięci ulotnej (np. z pamięci komputera)BARAN) z zainfekowanego hosta w celu zbadania sposobu działania złośliwego oprogramowania.
- Odzyskiwanie logów systemowych i sieciowych z kilku urządzeń w celu ustalenia sposobu rozprzestrzeniania się złośliwego oprogramowania.

Nadrzędnym celem reagowania na incydenty jest próba zrozumienia zakresu incydentu. Jeśli nie zrozumiemy go dokładnie, proces zarządzania incydentami nie będzie w stanie podjąć odpowiednich kroków w celu jego zamknięcia. Oba skrajne przypadki mogą być niezwykle szkodliwe. Jeśli błędnie uznamy zakres za szerszy, możemy zezwolić na bardziej drastyczne działania niż jest to konieczne, co zakłóci działalność firmy. Jeśli błędnie uznamy zakres za mniejszy, możemy podjąć niewystarczające działania wobec sprawcy zagrożenia, co oznacza, że ​​incydent nie zostanie zakończony.  

**Zarządzanie incydentami**

Zarządzanie incydentami obejmuje aspekt procesowy postępowania z incydentem. Ta część odpowiada za odpowiedź na główne pytanie:

_**Jak reagujemy na to, co się wydarzyło?**_  

Gdy już zrozumiemy skalę incydentu, kolejnym pytaniem jest, jak sobie z nim poradzimy. Zarządzanie incydentami musi uwzględniać kilka kwestii, takich jak:

- Wstępna selekcja incydentu w celu dokładnego określenia jego powagi w miarę pojawiania się nowych informacji oraz zaangażowanie większej liczby interesariuszy, na przykład ekspertów merytorycznych, w celu pomocy w rozwiązaniu incydentu.
- Kierowanie działaniami w przypadku incydentu przy użyciu podręczników.  
    
- Podjęcie decyzji, jakie działania należy podjąć w celu powstrzymania, wyeliminowania i odzyskania skutków incydentu.
- Określenie rodzaju komunikacji, która będzie wysyłana wewnętrznie i zewnętrznie, podczas gdy zespół zajmuje się incydentem.
- Dokumentowanie informacji o incydencie, takich jak podjęte działania i ich wpływ na poradzenie sobie z incydentem.
- Zamknięcie incydentu i wyciągnięcie wniosków z incydentu oraz udoskonalenie przyszłych procesów i procedur.

Skuteczne reagowanie na incydenty i zarządzanie nimi są niezbędne do radzenia sobie z nimi. Często błędnie uważa się, że do radzenia sobie z incydentami potrzebne są jedynie umiejętności techniczne. Aspekt zarządzania jest równie ważny. Zostanie on omówiony bardziej szczegółowo w Zadaniu 5.  

Poziomy reagowania na incydenty i zarządzania nimi  

Tak jak nie wszystkie alerty są sobie równe, tak samo nie wszystkie incydenty są sobie równe. W związku z tym proces reagowania na incydenty i zarządzania nimi będzie się różnić w zależności od ich wagi. Jednak waga nie jest stała i może się zmieniać, ponieważ reagowanie na incydenty pomaga lepiej zrozumieć zakres incydentu. W związku z tym istnieją różne poziomy reagowania na incydenty i zarządzania nimi. Istnieje wiele sposobów ich klasyfikacji, a w każdej organizacji będą one unikalne. Skupimy się jednak przede wszystkim na czterech różnych poziomach w tym przypadku. Na każdym z tych poziomów mówimy o powołaniu innego zespołu, co oznacza, że ​​w proces angażują się ważniejsi interesariusze. Co więcej, dostępne działania w celu poradzenia sobie z incydentem stają się bardziej skuteczne, ale także bardziej destrukcyjne. Opisane tutaj poziomy dotyczą dużych organizacji. Na poziomach od pierwszego do trzeciego sytuacja jest taka sama.SOCradzenia sobie z incydentem, a jedynie liczba członków zespołu biorących udział w incydencie.  

**W tym przypadku posłużymy się przykładem** : Użytkownik zgłosiłphishinge-mail  

**Poziom 1:SOCIncydent**

Na poziomie pierwszym często nie są one nawet klasyfikowane jako incydenty. Zazwyczaj wymagają one podejścia czysto technicznego. Na tym poziomie, po przeanalizowaniu naszego przykładu, analityk stwierdza, że ​​jest to zdarzenie odosobnione i dlatego po prostu aktualizuje reguły filtrowania poczty, aby zablokować nadawcę. Incydenty tego poziomu mogą zdarzać się kilka razy dziennie i zazwyczaj są szybko rozwiązywane, a analityk zajmuje się tym samodzielnie.

Jednak w naszym przykładzie zespół CERT (Computer Emergency Readiness Team) może zostać powołany, jeśli dochodzenie wykaże, że wiadomość e-mail otrzymała większa liczba użytkowników.  

**Poziom 2: Incydent CERT**

Na poziomie drugim kilku analityków wSOCMoże być zaangażowany w śledztwo. Incydent CERT to taki, w którym nie mamy jeszcze wystarczających informacji, aby podnieść alarm. Mimo to jesteśmy zaniepokojeni i dlatego przeprowadzamy dodatkowe śledztwo w celu ustalenia zakresu incydentu. Zwykle analityk prosi o pomoc i więcej członków zespołu.SOCZespół by się zaangażował. W naszym przykładzie, na tym etapie sprawdzalibyśmy, czy któryś z tych użytkowników wszedł w interakcję z wiadomością e-mail. Chcielibyśmy również lepiej zrozumieć, co ona robi.

Gdybyśmy mogli powstrzymać incydent, zanim którykolwiek z użytkowników wszedł w interakcję z wiadomością e-mail, zazwyczaj zatrzymalibyśmy się na tym etapie. Jeśli jednak odkrylibyśmy, że wiadomość e-mail zawiera złośliwe oprogramowanie i że niektórzy użytkownicy faktycznie z nią weszli, wezwalibyśmy Zespół Reagowania na Incydenty Bezpieczeństwa Komputerowego (CSIRT).  

**Poziom 3: Incydent CSIRT**

Na poziomie trzecim całośćSOCjest w stanie najwyższej gotowości i aktywnie pracuje nad rozwiązaniem incydentu. W tym momencie całaSOCZespół skupi się na pojedynczym incydencie, aby się nim zająć. Analitycy i zespół kryminalistyczny pracują nad ujawnieniem pełnego zakresu incydentu, a zespół zarządzający podejmuje działania przeciwko sprawcy zagrożenia, aby powstrzymać rozprzestrzenianie się złośliwego oprogramowania, wyeliminować je z hostów, na których zostało wykryte, i odzyskać zainfekowane systemy.

Jeśli zespołowi uda się powstrzymać rozprzestrzenianie się ataku, zanim dojdzie do jakichkolwiek zakłóceń, lub jeśli sprawca zagrożenia będzie mógł rozszerzyć swoje uprawnienia w ramach systemu, zespół CSIRT zamknie incydent. Jeśli jednak w toku dochodzenia okaże się, że zakres incydentu jest szerszy, powołamy Zespół Zarządzania Kryzysowego (CMT).  

**Poziom 4: Incydent CMT**  

Na czwartym poziomie wszyscy są zaangażowani i oficjalnie mamy do czynienia z pełnowymiarowym kryzysem cybernetycznym. Zespół CMT zazwyczaj składa się z kilku kluczowych interesariuszy biznesowych, takich jak cała kadra kierownicza, członkowie zespołów prawnych i komunikacyjnych, a także innych podmiotów zewnętrznych, takich jak organ regulacyjny lub policja. Co więcej, na tym poziomie zaczynamy wkraczać na terytorium tzw. działań „nuklearnych”. Zamiast prostych działań mających na celu powstrzymanie, wyeliminowanie i naprawę, zespół ten może autoryzować zastosowanie działań nuklearnych, takich jak wyłączenie całej organizacji z sieci w celu ograniczenia szkód spowodowanych incydentem.  

Korzyści z reagowania na incydenty i zarządzania nimi  

Zbudowanie zespołu i wszystkich niezbędnych narzędzi do reagowania na incydenty i zarządzania incydentami nie jest tanie. Często trudno jest też namacalnie wytłumaczyć firmie, dlaczego jest to potrzebne. Jednak koszty incydentu mogą być tak wysokie, że organizacja może po nim całkowicie zamknąć działalność. To nie jest problem tylko „dużej firmy”. Mówiąc z szerszej perspektywy, według [National CyberSecurity Alliance(otwiera się w nowej karcie)](https://staysafeonline.org/)Około 60% małych firm, które padły ofiarą cyberataku, zamyka działalność po zaledwie sześciu miesiącach. Nie można przecenić znaczenia skutecznej reakcji na incydenty i zarządzania nimi.

Do efektywnego reagowania na incydenty i zarządzania incydentami wymagane jest wiele ról. Poniższa tabela przedstawia niektóre z tych ról, z którymi warto się zapoznać:

|   |   |
|---|---|
|**Rola**|**Opis**|
|SOCAnalityk|ASOCAnalityk to osoba, która zajmuje się różnymi zdarzeniami i alertami, które mają miejsce wSOCZazwyczaj analitycy mają różne poziomy kompetencji. Ostatecznie analitycy są zazwyczaj jednymi z pierwszych osób zaangażowanych w rozwiązywanie incydentów.|
|SOCOłów|TenSOCołów, zwany takżeSOCMenedżer lub KierownikSOC, jest odpowiedzialny za podział zadań wSOCi podjęcie decyzji o eskalacji alertu do poziomu incydentu. ZwykleSOCkierownik rozumie informacje techniczne niezbędne do przeprowadzenia dochodzenia, co pozwala mu na lepszy podział zadań w trakcie incydentu.|
|Analityk kryminalistyczny|Analityk kryminalistyczny to osoba, która przeprowadza dochodzenie w celu lepszego zrozumienia, co wydarzyło się podczas incydentu. Często jest to analiza kryminalistyczna danych cyfrowych, która wymaga analizy artefaktów, takich jak pamięć lub dysk twardy urządzenia.|
|Analityk złośliwego oprogramowania|Analityk złośliwego oprogramowania to analityk kryminalistyczny, który koncentruje się na zrozumieniu działania złośliwego oprogramowania. Analitycy ci często dysponują znacznymi umiejętnościami technicznymi w zakresie debugowania i dekompilowania złośliwego oprogramowania, aby zrozumieć jego działanie. Analitycy ci często pomagają w odkryciu wskaźników zagrożenia (IoC), czyli sygnatur złośliwego oprogramowania, które można wykorzystać do jego identyfikacji w środowisku.|
|Łowca zagrożeń|Łowca zagrożeń to osoba aktywnie poszukująca nowych zagrożeń w środowisku. Celem polowania na zagrożenia jest tworzenie nowych reguł alertów w oparciu o informacje dostępne w logach i innych źródłach. W wyniku polowania na zagrożenia generowany jest alert, który może pomóc zespołowi w wykryciu atakującego, który próbował zastosować tę samą technikę.|
|Ratownik medyczny|W niektórych przypadkach nie jest to w rzeczywistościSOCktóry jako pierwszy został powiadomiony o incydencie. Często incydent cybernetyczny mógł rozpocząć się od incydentu biznesowego. Na przykład, zespół produktowy odkrywa, że ​​jego aplikacja działa wolniej i nie reaguje prawidłowo. W takich przypadkach ten zespół staje się służbą reagowania incydentu. Chociaż nie oczekuje się, że sami poradzą sobie z całym incydentem, istnieje kilka kluczowych kroków, które służby reagowania powinny podjąć, aby upewnić się, że nie ujawnią informacji niezbędnych do lepszego zrozumienia incydentu cybernetycznego.|
|Inżynier bezpieczeństwa|Chociaż inżynierowie ds. bezpieczeństwa nie są bezpośrednio zaangażowani wSOC, często mogą być zaangażowani w incydenty. Inżynierowie bezpieczeństwa odpowiadają za bezpieczeństwo swojego działu, aplikacji lub systemu. W przypadku wystąpienia incydentu w ich obszarze, często są oni proszeni o pomoc w dochodzeniu jako eksperci merytoryczni. Ponadto inżynierowie bezpieczeństwa często ściśle współpracują z…SOCaby zapewnić, żeSOCotrzymuje informacje z dziennika zdarzeń ze swojego działu.|
|Specjalista ds. bezpieczeństwa informacji|Podobnie jak inżynier bezpieczeństwa, inspektor bezpieczeństwa informacji (ISO) odpowiada za bezpieczeństwo swojego działu. Zazwyczaj jednak jego rola koncentruje się bardziej na zarządzaniu niż na kwestiach technicznych, takich jak w przypadku inżynierów bezpieczeństwa. Inspektorzy bezpieczeństwa informacji często angażują się również w obsługę incydentów jako eksperci merytoryczni i pełnią rolę pomostu między zespołem reagowania na incydenty a zespołem swojego działu, który będzie wdrażał działania wskazane przez menedżera ds. incydentów.|
|Menedżer incydentów|Menedżer ds. incydentów to osoba przeszkolona w zakresie wykonywania obowiązków kierowniczych w zakresie reagowania na incydenty i zarządzania nimi. Menedżerowie ds. incydentów muszą być wyjątkowo sprawni w sporządzaniu notatek i zorganizowani, aby zapewnić, że wszystko podczas incydentu jest odpowiednio udokumentowane i że procedury są przestrzegane.|
|Właściciel projektu|Właściciel produktu to zazwyczaj osoba, która przewodzi w procesie rozwoju rozwiązania. W przeszłości, w metodzie kaskadowej, produkty były wydawane dopiero po ich całkowitym ukończeniu. Jednak obecnie, dzięki procesom Agile, produkty są wydawane i stale aktualizowane. W związku z tym, ponieważ wersja projektu jest już aktywna, a zespół wciąż pracuje nad rozwojem, incydenty mogą wystąpić. W przypadku incydentu właściciel produktu jest często wzywany jako ekspert merytoryczny do pomocy w dochodzeniu.|
|Ekspert przedmiotowy|Tenniebieski zespółNie można oczekiwać, że będą ekspertami w każdej technologii lub systemie. W związku z tym często polega się na ekspertach merytorycznych (SME) w zależności od konkretnego incydentu. Na przykład, jeśli w incydencie doszło do naruszenia bezpieczeństwa usługi Active Directory, jeden z administratorów domeny może zostać wezwany jako SME. Od ekspertów merytorycznych często oczekuje się dostarczenia dodatkowych informacji, które pozwolą na…niebieski zespółaby lepiej zrozumieć zakres incydentu i potencjalne działania, jakie można podjąć wobec sprawców zagrożenia.|
|Menedżer kryzysowy|Menedżer kryzysowy kieruje zespołem zarządzania kryzysowego. Zazwyczaj jest to osoba na stanowisku kierowniczym, taka jak dyrektor ds. informatyki (CIO) lub dyrektor operacyjny (COO). Osoba ta odpowiada za zapewnienie prawidłowego funkcjonowania zespołu CMT i radzenia sobie z kryzysem.|
|Wykonawczy|W przypadku wystarczająco poważnego incydentu, w CMT zaangażowani będą członkowie kierownictwa firmy. W skład CMT wchodzą: prezes zarządu, dyrektor operacyjny, dyrektor ds. informatyki,Dyrektor technicznyi CISO.|

Otwórz statyczną witrynę i pokaż, że rozumiesz różne role związane z otrzymywaniem flagi!

Aby skutecznie poradzić sobie z incydentem, należy ustanowić odpowiedni proces zarządzania incydentami. Chociaż organizacje często tworzą własne procesy, zazwyczaj opierają się one na[NISTZarządzanie incydentami(otwiera się w nowej karcie)](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r2.pdf)Proces ten pokazano na poniższym schemacie.  

![Struktura zarządzania incydentami NIST](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/dcab2ddeb05cd1300a0d2142d87b447e.png)  

Przygotowanie

Przygotowanie jest kluczem do skutecznego radzenia sobie z incydentem. Podczas incydentu często panuje stres i liczy się każda minuta, aby jak najszybciej uporać się z incydentem i zminimalizować skalę szkód. W takich stresujących sytuacjach łatwo o zapomnienie, co może mieć poważne konsekwencje.

Aby temu zapobiec, zespół musi przygotować się na wypadek incydentu. Im lepiej zespół jest przygotowany, tym mniejsze jest prawdopodobieństwo popełnienia prostych błędów podczas incydentu. Aby się przygotować, zespół może podjąć kilka działań, takich jak:

- Zidentyfikuj i udokumentuj kluczowe strony zainteresowane i schematy połączeń, które zostaną wykorzystane w trakcie incydentu
- Tworzenie i aktualizowanie podręczników, które pomagają zespołowi w przestrzeganiu ustalonego procesu w przypadku incydentów o znanym charakterze
- Ćwicz umiejętność zespołu w radzeniu sobie z incydentami poprzez ćwiczenia planszowe i gry cyberwojenne
- Ciągłe wykrywanie zagrożeń w celu tworzenia nowych reguł alertów w oparciu o nowoczesne techniki ataku  

Wykrywanie i analiza

Organizacje często dzielą fazę wykrywania i analizy na dwie. Ma to na celu wprowadzenie etapu pośredniego, zwanego triażem. Jak wspomniano wcześniej, nie wszystkie alerty zostaną sklasyfikowane jako incydent, a nawet jeśli incydent wystąpi, istnieją różne poziomy incydentów. Etap triażu odpowiada za określenie powagi incydentu. Jednak wNISTramy te są uwzględniane w fazie wykrywania i analizy.

To podstawowa faza reagowania na incydenty, w której staramy się odpowiedzieć na pytanie, co się stało. W tej fazieniebieski zespółPracuje nad lepszym zrozumieniem zakresu incydentu i przekazaniem tych informacji menedżerowi ds. incydentów. Może to obejmować następujące działania:

- Przeglądanie alertów wAV,EDR, ISIEMpulpity nawigacyjne
- Przeprowadzenie dochodzenia kryminalistycznego artefaktów zarówno w systemach, jak i w sieci
- Analizowanie odkrytego złośliwego oprogramowania w celu lepszego zrozumienia jego działania i tworzenia nowych sygnatur, które mogą być użyte do jego identyfikacji

Ograniczanie, eradykacja i odzyskiwanie

Po lepszym zrozumieniu skali incydentu, zespół rozpocznie działania od jego powstrzymania, wyeliminowania i odzyskania. Jest to główna faza zarządzania incydentem, w której staramy się zająć incydentem. Często organizacje dzielą tę fazę na trzy różne etapy, z których każdy obejmuje następujące kwestie:

- Ograniczenie – działania podejmowane w celu „zatrzymania krwawienia”. Są to działania mające na celu zapobieżenie rozprzestrzenianiu się incydentu.
- Likwidacja – działania podejmowane w celu wyeliminowania sprawcy zagrożenia z majątku.
- Przywracanie – działania podjęte w celu przywrócenia środowiska naturalnego pozwalają organizacji powrócić do normalnego trybu działania (BAU).

Podział na trzy fazy wynika z faktu, że ich kolejność ma znaczenie. Jeśli rozpoczniemy eliminację lub odzyskiwanie przed powstrzymaniem ataku, sprawca zagrożenia będzie mógł przetrwać. Na przykład, jeśli sprawca zagrożenia naruszył Active Directory, a my po prostu zmieniliśmy hasło każdego konta (działanie eliminacji), sprawca zagrożenia mógłby po prostu wykorzystać swoje bieżące uprawnienia, aby odzyskać dane uwierzytelniające. Najpierw musielibyśmy się upewnić, że dostęp do sprawcy zagrożenia został zablokowany, zanim podejmiemy inne działania.

Jak widać na schemacie, fazy 2 i 3 są cykliczne. Dzieje się tak, ponieważ rozpoczynając pracę nad incydentem, nie rozumiemy jego pełnego zakresu. Jednak nie możemy się doczekać, aż poznamy go w pełni, zanim podejmiemy jakiekolwiek działania. Dlatego, w trakcie trwania dochodzenia, podejmujemy już pewne działania i obserwujemy ich wpływ na incydent. Dopiero po powrocie do BAU zatrzymujemy ten proces.  

Aktywność po incydencie

Zamknięcie incydentu nie kończy procesu zarządzania incydentami. Na koniec chcemy ocenić, co wydarzyło się podczas incydentu, aby wyciągnąć wnioski i udoskonalić sposób radzenia sobie z incydentami w przyszłości. W ten sposób wyciągamy wnioski z tych incydentów, aby lepiej przygotować się do radzenia sobie z kolejnymi.

Otwórz i uzupełnij stronę statyczną, aby pokazać, że rozumiesz proces zarządzania incydentami!  

Odpowiedz na poniższe pytania
Omówiliśmy już reagowanie na incydenty i zarządzanie nimi. Przyjrzyjmy się teraz kilku typowym pułapkom, które mogą wystąpić podczas incydentu.

Niewystarczające utwardzenie

Niewystarczające wzmocnienie to zjawisko, które ma miejsce jeszcze przed incydentem. Organizacje często przedkładają szybkość i zyski nad bezpieczeństwo. Dlatego czasami bezpieczeństwo może być postrzegane jako przeszkoda dla organizacji. Po wdrożeniu rozwiązania organizacja po prostu przechodzi do kolejnego. Jednak w inżynierii bezpieczeństwa istnieje ważny etap zwany wzmocnieniem. Po wdrożeniu rozwiązania mogą nadal występować konfiguracje, które nie były zgodne z najlepszymi praktykami bezpieczeństwa, ale zostały wprowadzone w celu szybszego uruchomienia rozwiązania. Proces wzmocnienia odwraca te konfiguracje, aby przywrócić je do zgodności z najlepszymi praktykami bezpieczeństwa.

W przypadku pominięcia tego kroku wzrasta prawdopodobieństwo wystąpienia incydentów. Ta pułapka prowadzi zatem do wzrostu liczby incydentów i chociaż większość z nich można powstrzymać przed wystąpieniem rzeczywistych szkód, wystarczy jeden udany incydent, aby okazał się bardzo kosztowny dla organizacji. W związku z tym nie należy pomijać etapu wzmacniania zabezpieczeń. Aby to ułatwić, organizacje zaczęły stosować wzmacnianie zabezpieczeń w trakcie rozwoju, a nie dopiero na końcu. Zasada ta znana jest jako zasada przesunięcia w lewo i została omówiona w publikacji [Secure.SDLCpokój.](https://tryhackme.com/jr/securesdlc)  

Niewystarczające rejestrowanie

Abyniebieski zespółAby otrzymywać powiadomienia o incydentach, muszą najpierw otrzymać odpowiednie informacje, które mogą skutkować zdarzeniami i alertami. Często zdarza się, że organizacje nie rejestrują odpowiednio informacji. Można to postrzegać jako „działanie w ciemno”, ponieważniebieski zespółnie byłby w stanie nawet wiedzieć, że ma miejsce jakieś zdarzenie.

Częstym problemem jest koszt pobierania informacji z dziennika. CzęstoSIEMDostawcy będą pobierać opłaty od klientów na podstawie przepustowości danych. W rezultacie organizacje ograniczają liczbę pobieranych logów. Co więcej, przesyłanie informacji z logów przez sieć komórkową z urządzeń zdalnych, takich jak bankomaty, jest często kosztowne. Wszystko to może prowadzić do ograniczenia widoczności.niebieski zespółChociaż część tych informacji z dziennika będzie dostępna bezpośrednio na urządzeniu, ich przechowywanie jest często ograniczone, a w gorszych przypadkach osoba atakująca mogła usunąć te lokalne logi.

W przypadku braku wystarczającej ilości danych do rejestrowania, niektóre incydenty mogą zostać wykryte dopiero później, gdy już wystąpią negatywne skutki. W innych przypadkach dokładne określenie zakresu incydentu może być niemożliwe.  

Niedostateczne i nadmierne ostrzeganie

Czasami otrzymujemy logi, ale nie robimy z nimi nic pożytecznego.SIEMRozwiązania często pochłaniają niewiarygodne ilości danych, co może sprawiać wrażenie, że śledczy szukają igły w stogu siana. Dlatego tak ważne jest śledzenie zagrożeń. Pomaga ono w identyfikacji informacji, które można przekształcić w nowe alerty, informujące zespół o tym, kiedy pojawi się coś wartego zbadania.

Jednak druga strona medalu również może stanowić problem. Jeśli alert generuje zbyt dużo szumu informacyjnego z powodu zbyt wielu fałszywych alarmów, może to doprowadzić do jego zignorowania przez zespół. Jest to podobne do sytuacji „wilczego alarmu”. W przypadku wystąpienia rzeczywistego incydentu, który powoduje alarm, zespół może go po prostu zignorować, dopóki nie będzie on miał znaczącego wpływu. Dlatego też, podczas wykrywania zagrożeń należy zwracać uwagę nie tylko na tworzenie nowych alertów, ale także na optymalizację stosunku sygnału do szumu.  

Niewystarczające określenie zakresu incydentu

Dużym błędem, który często zdarza się podczas reagowania na incydenty i zarządzania nimi, jest niezrozumienie ich zakresu. Chociaż często niemożliwe jest pełne zrozumienie zakresu incydentu, należy dołożyć wszelkich starań. W przypadku niedoszacowania zakresu incydentu, działania podjęte przeciwko sprawcy zagrożenia nie będą wystarczające, aby wyeliminować go z systemu. W przypadku przeszacowania zakresu incydentu, zespół może podjąć drastyczne działania, które doprowadzą do niepotrzebnych zakłóceń w działalności.

Niestety, nie ma szybkiego rozwiązania tego problemu. Konieczne jest ciągłe przygotowywanie się na incydenty, aby podnosić kwalifikacje zespołu i pomóc w rozwiązaniu tego problemu.

Niewystarczająca odpowiedzialność

Kolejnym problemem podczas incydentów jest bezczynność. Niezwykle ważne jest zrozumienie, że istnieje różnica między omawianiem działań powstrzymujących, zwalczających i regenerujących a ich realizacją. Często podczas incydentów omawiane są działania, ale żadna osoba nie jest pociągnięta do odpowiedzialności za ich faktyczne wykonanie. To często prowadzi do narastania incydentu, ponieważ wszyscy myślą, że coś już zostało wykonane, podczas gdy w rzeczywistości tak nie jest.

Skuteczne zarządzanie incydentami i sporządzanie notatek mogą pomóc w rozwiązaniu tego problemu. Menedżer ds. incydentów może udokumentować podejmowane działania i upewnić się, że wyznaczona zostanie osoba odpowiedzialna nie tylko za ich wykonanie, ale także za przekazanie menedżerowi informacji zwrotnej po ich wykonaniu.  

Niewystarczająca liczba kopii zapasowych

Ostatnią częstą pułapką podczas incydentów są niewystarczające kopie zapasowe. W przypadku, gdy incydent doprowadzi do działań zakłócających, takich jak atak ransomware, jedynym ratunkiem są kopie zapasowe, które pozwolą odzyskać dane. Jednak bez jasno określonych i przestrzeganych procedur tworzenia kopii zapasowych, odzyskanie danych po incydencie nie będzie możliwe.

Co więcej, czasami kopie zapasowe nie są wystarczająco izolowane. W dzisiejszych czasach, gdzie priorytetem jest dostępność, starsze kopie zapasowe są często eliminowane na rzecz nowych środowisk High Availability Disaster Recovery. Problem polega jednak na tym, że jeśli ransomware zostanie uruchomiony w systemie głównym, zostanie on zreplikowany w środowisku DR. Dlatego kopie zapasowe offline i zdalne są dziś równie ważne.

Otwórz i zagraj w grę na stronie statycznej, aby ominąć typowe pułapki, na które można natknąć się podczas cyberataków!

W tej sali dowiedzieliśmy się o reagowaniu na incydenty i zarządzaniu nimi. Podsumowując:

- Incydenty są częścią życia. Incydenty się zdarzają, dlatego musimy być przygotowani, aby sobie z nimi poradzić.
- Nie wszystkie zdarzenia i alerty prowadzą do incydentu. Nawet w przypadku wystąpienia incydentu, dysponujemy różnymi poziomami reakcji, które możemy wykorzystać, aby sobie z nim poradzić.
- Reagowanie na incydenty koncentruje się na odpowiedzi na pytanie, co wydarzyło się podczas incydentu. Zarządzanie incydentami koncentruje się na skutecznym podejmowaniu działań w celu zamknięcia incydentu.
- Podczas incydentu istnieje wiele różnych ról i obowiązków. Nawet jeśli nie jesteś częściąniebieski zespółmożesz być ratownikiem lub możesz zostać wezwany jako ekspert w danej dziedzinie, aby pomócniebieski zespółporadzić sobie z incydentem.  
    
- Większość organizacji ma własne ramy zarządzania incydentami, ale większość opiera się naNISTstruktura zarządzania incydentami obejmująca cztery fazy: przygotowania, wykrywania i analizy, powstrzymywania, eliminacji i odzyskiwania oraz analizy poincydentalnej.
- Podczas incydentu może pójść nie tak wiele rzeczy, a odpowiednie przygotowanie może pomóc w ograniczeniu skutków tych nieprzewidzianych zdarzeń.
Mimo że w tym pokoju nie będziemy poruszać szczegółów dotyczących analizy logów ani systemów SIEM, ważne jest, aby osiągnąć podstawowy poziom zrozumienia.

Systemy SIEM są zazwyczaj projektowane z trzema komponentami używanymi do wyszukiwania,indeksowaniei równoważenia obciążenia; komponenty te są powszechnie znane odpowiednio jako **głowica wyszukiwania** , **indeksator** i **przekierowywanie** .

W tym pomieszczeniu naszym celem jest odpowiedzialność, dlatego skupimy się głównie na indeksatorze i sposobie, w jaki dane docierają z urządzenia do indeksatora. Proces ten jest powszechnie znany jako **pobieranie danych** .

- Rodzaje pozyskiwania danych
    - Agent/spedytor
    - Przekierowanie portów
    - Dziennik systemowy
    - Wgrywać

Chociaż istnieje wiele sposobów pobierania danych, to sposobów ich przechowywania jest zazwyczaj mniej. Chociaż głównym punktem odniesienia w kwestii rozliczalności jest pobieranie danych, ich przechowywanie może być równie trudne.

W przypadku problemów z przechowywaniem danych często nie powinniśmy martwić się o atakujących, ale o usterki techniczne, na przykład przypadkowe usunięcie indeksu lub uszkodzenie urządzenia pamięci masowej.

Oto kilka przykładów kwestii, które należy wziąć pod uwagę podczas projektowania rozwiązania do przechowywania danych dla źródeł logów. Chociaż zachowanie autentyczności i bezpieczeństwa tych danych jest ważne dla zapewnienia rozliczalności, często nakłada się to na kwestie zgodności. Zgodność i przepisy idą w parze; jednym z takich przepisów może być wymóg archiwizacji lub przechowywania danych logów przez określony czas. To ponownie wpływa na rozliczalność, gdzie w celu zapewnienia zgodności należy zastosować zasadę niezaprzeczalności dla źródła logów. Na przykład, audyt wymaga danych z ostatnich sześciu miesięcy z X źródeł logów. Jako interesariusz musisz zagwarantować, że te źródła logów odzwierciedlają aktywność sieci.

Jednym z rozwiązań problemu przechowywania danych jest tzw. cold storage. Cold storage to proces lub standard przechowywania danych, który można streścić jako optymalne przechowywanie dużej ilości danych.

Dostęp do pamięci masowej typu cold storage jest rzadki i dlatego nie wymaga urządzeń pamięci masowej o wysokiej wydajności. Przykładami pamięci masowej typu cold storage mogą być niedrogie dyski twarde, a nawet napędy taśmowe! Z kolei pamięć masowa typu hot storage to częsty dostęp do danych, który wymaga wyższej wydajności. Może ona obejmować dyski SSD, a w niektórych przypadkach dyski twarde o wysokiej wydajności. W całym cyklu życia danych mogą występować inne poziomy dostępu i wydajności, które można określić mianem pamięci masowej typu warm storage. 

Standard określający, jak długo dane pozostają w każdej fazie, będzie zależał od wymogów regulacyjnych i wytycznych firmy. Przykładem procesu przechowywania może być przechowywanie danych w trybie gorącym przez sześć miesięcy, w trybie ciepłym przez trzy miesiące i w trybie zimnym przez trzy lata. W zależności od rodzaju danych, mogą one być przechowywane w trybie zimnym bezterminowo.

Standard bezpieczeństwa danych branży kart płatniczych (PCI DSS) to przykład normy, która wymaga przechowywania dzienników audytu przez rok i umożliwienia natychmiastowego dostępu do nich przez 90 dni w celu zachowania zgodności.
