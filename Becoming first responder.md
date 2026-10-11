---

Nawet jeśli nie jesteś bezpośrednio wniebieski zespółNie oznacza to jednak, że nigdy nie będziesz musiał mierzyć się z incydentami cybernetycznymi. Jak wyjaśniono w sali „Wprowadzenie do reagowania na incydenty i zarządzania nimi”, jeśli w systemie, za który odpowiadasz, wystąpi incydent, możesz zostać wezwany przez…niebieski zespółaby pomóc.

Jeszcze bardziej przerażające jest to, co się stanie, jeśli to Ty odkryjesz incydent i będziesz musiał powiadomićniebieski zespółGratulacje! Oficjalnie awansowałeś na ratownika! Biorąc pod uwagę, że liczy się każda minuta, to wspaniale, że dokładnie wiesz, co robić, prawda? Bez obaw! W tym pokoju dowiesz się o roli ratownika i o ważnych rzeczach, o których warto pamiętać, jeśli kiedykolwiek znajdziesz się w takiej sytuacji.

Wymagania wstępne

- [Wprowadzenie do reagowania na incydenty i zarządzania nimi](https://tryhackme.com/jr/introtoirandim)
- [Rejestrowanie w celu rozliczeń i monitorowania](https://tryhackme.com/room/loggingforaccountability)  

Cele edukacyjne  

- Czym jest osoba udzielająca pierwszej pomocy
- Jakie zadania musi wykonać ratownik?
- Znaczenie zachowania dowodów
- Procesy wymagane do zapewnienia, żeniebieski zespółmoże skutecznie przejąć kontrolę nad incydentem

Szybko! Ty, inżynier bezpieczeństwa naszego wydziału, właśnie odkryłeś incydent! Jeden z naszych serwerów został naruszony! Co robisz w pierwszej kolejności? Jak w każdym odcinku CSI, musimy zabezpieczyć miejsce zbrodni. W związku z tym musimy zadbać o zabezpieczenie dowodów.

Zmienność dowodów

Największym błędem popełnianym podczas incydentów jest wyłączenie hosta. Jest to niewłaściwe z dwóch głównych powodów:

- Znaczna ilość ważnych dowodów znajduje się w przestrzeniach o dużej zmienności, co oznacza, że ​​zostaną one utracone w momencie utraty zasilania urządzenia
- Natychmiast ostrzega osobę atakującą, że możemy być na jej tropie, co oznacza, że ​​może ona rozpocząć bardziej destrukcyjny atak  

W tym drugim przypadku oznacza to, że na początek nie powinniśmy nawet wyłączać dostępu do sieci na hoście, ponieważ może to mieć ten sam skutek. Zamiast tego chcemy mieć pewność, że dowody zostaną zachowane. Chcemy również zadbać o to, aby dowody były przechowywane według kolejności ich zmienności. Chociaż analityk informatyki śledczej zazwyczaj będzie zaangażowany w gromadzenie większości tych dowodów, ważne jest, aby znać różne rodzaje dowodów i wiedzieć, dlaczego musimy zrobić wszystko, co w naszej mocy, aby je zachować. Grupa Robocza ds. Inżynierii Internetu (IETF) stworzył dokument zatytułowany [Wytyczne dotyczące gromadzenia i archiwizacji dowodów(otwiera się w nowej karcie)](https://datatracker.ietf.org/doc/html/rfc3227.1), który zapewnia następujący rząd zmienności wraz z uzasadnieniem.

**1. Rejestry i pamięć podręczna**

Rejestry i pamięć podręczna są niezwykle zmienne i stale się zmieniają, ponieważ host uruchamia różne aplikacje. Dane te mogą ulec zmianie w ułamku sekundy. Chociaż nigdy nie bylibyśmy wystarczająco szybcy, aby zebrać te dowody dokładnie w momencie wykrycia incydentu, powinniśmy zrobić to jak najszybciej. Dowody te mogą być kluczowe dla analizy złośliwego oprogramowania, aby zrozumieć, co ono zrobiło na hoście. W większości incydentów nie zebralibyśmy tych informacji, ponieważ są one po prostu zbyt zmienne.  

**2. Tabela trasowania, ARP Pamięć podręczna, tabela procesów, statystyki jądra i pamięć**

Chociaż incydent mógł wystąpić na jednym hoście, musimy mieć świadomość, że zainfekowanych mogło zostać więcej hostów. Chcemy również lepiej zrozumieć nie tylko ten host, ale także to, czy komunikował się on z innymi hostami w sieci. Dlatego musimy zebrać informacje, takie jak routing i…ARP tabele. Trasy i ARP Wpisy mają określony czas życia, co oznacza, że ​​jeśli nie uda nam się zebrać tych danych na czas, możemy nie mieć pełnego obrazu tego, jaka komunikacja sieciowa miała miejsce w momencie wystąpienia incydentu. Dane te można zebrać bezpośrednio z hosta.  

Jeśli chodzi o rzeczywistego podejrzewanego hosta, chcemy lepiej zrozumieć, jakie aplikacje były uruchomione i co robiły w momencie wystąpienia incydentu. Dlatego musimy zebrać informacje o procesach, które były wykonywane w momencie wystąpienia incydentu.

Wreszcie, sama nazwa programu nie mówi nam dokładnie, czym on jest ani co robi. Jeśli chcemy naprawdę zrozumieć, czym jest program, będziemy musieli go zapisać w pamięci. Oznacza to, że będziemy musieli przechwycić dowody z pamięci RAM (Random Access Memory).BARAN). Informacje znajdujące się w tym miejscu mogą jednak zostać utracone w przypadku spadku napięcia lub wyłączenia zasilania. Złośliwe oprogramowanie stało się niezwykle zaawansowane i potrafi tworzyć różne ładunki, co oznacza, że ​​nawet jeśli mamy próbkę złośliwego oprogramowania do uruchomienia w piaskownica, nie możemy w pełni zrozumieć, co robiło ono na hoście bez bezpośredniej analizy w pamięci.  

**3. Tymczasowe systemy plików**

Aplikacje często tworzą i używają plików tymczasowych na hostach. Na przykład, na serwerze WWW, aktywne sesje są zazwyczaj przechowywane w plikach tymczasowych. Chociaż pliki te są często przechowywane dłużej na hoście, nie chcemy ryzykować ich utraty, ponieważ mogą być istotne dla śledztwa.  

**4. Dysk**

Następnym krokiem jest upewnienie się, że wykonamy migawkę dysku hosta. Chociaż ta część dowodu może nie być tak niestabilna jak pozostałe, może odegrać ważną rolę w postępowaniu sądowym i dlatego powinna być traktowana priorytetowo. Zachowanie tego dowodu oznacza również możliwość tworzenia lokalnych logów na samym urządzeniu, co może pomóc analitykom ustalić, czy atakujący próbował ukryć swoje ślady, porównując je ze zdalnie przechowywanymi logami.  

**5. Zdalne rejestrowanie i monitorowanie**  

Jak omówiono w sali „Logging for Accountability and Monitoring”, wszyscy gospodarze powinni przekazywać swoje logi do bezpiecznej, zdalnej lokalizacji. Jednak nawet te zdalne lokalizacje nie mają polityki nieograniczonego przechowywania logów. Ponieważ na tym etapie nie jesteśmy pewni, jak daleko wstecz sięga incydent, chcemy mieć pewność, że zachowamy te zdalne logi tak daleko wstecz, jak to możliwe, dopóki trwa dochodzenie.  

**6. Konfiguracja fizyczna i topologia sieci**

Konfiguracja fizyczna hosta i topologia sieci w momencie incydentu zazwyczaj nie ulegają zmianie. Jednak dowody te zazwyczaj mogą pomóc nam w dochodzeniu. Zrozumienie i zachowanie dowodów, takich jak podsieć, do której podłączony był host, będzie ważne, gdy będziemy próbować zrozumieć zakres incydentu i może wskazać nam inne hosty, które należy zbadać i zbadać.  

**7. Nośniki archiwalne**

Ostatnim punktem na liście są kopie zapasowe. Chociaż te informacje zazwyczaj nie są ulotne, mogą posłużyć jako dowód, który pomoże nam określić, jak daleko wstecz sięgał incydent, porównując artefakty na bieżącym dysku z tymi znalezionymi w kopiach zapasowych. Ponieważ jednak te kopie zapasowe zazwyczaj pozostają bezużyteczne, mamy nieco więcej przestrzeni, aby skupić się najpierw na innych, bardziej ulotnych źródłach.

Pozostałe dwa główne NIE

O pierwszym poważnym zakazie, jakim jest niewyłączanie urządzenia, już mówiliśmy; jednak wedługIETF:

- **Nie ufaj programom w systemie.** Oznacza to, że nie powinieneś używać faktycznego oprogramowania na hoście do gromadzenia dowodów. Powód jest prosty: sprawca mógł zmodyfikować te programy, a używając ich, zanieczyszczasz dowody, które próbujesz przechwycić.
- **Nie uruchamiaj programów, które modyfikują czas dostępu do plików.** Data dostępu do pliku sama w sobie stanowi dowód. Jeśli wykonasz proste kopiowanie i wklejanie, spowodujesz skażenie tego dowodu. Dlatego do przechwytywania dowodów używa się specjalnego oprogramowania lub sprzętu, aby zapewnić, że dowody zostaną przechwycone w oryginalnej postaci i nie zostaną skażone.

Nawet jeżeli stało się to nieumyślnie, niezwykle łatwo jest zniszczyć lub zanieczyścić dowody, co oznacza, że ​​nie będzie można ich wykorzystać w dalszym postępowaniu prawnym.  

Łańcuch dowodowy

Aby zapewnić możliwość wykorzystania dowodów w postępowaniu prawnym,łańcuch dostawWażne jest również, aby dowody były dopuszczalne w sądzie. Musimy być w stanie udowodnić, że nie zostały one sfałszowane. Analitycy śledczy zajmujący się informatyką śledczą rozumieją proces, który należy przeprowadzić, a który obejmuje dokumentowanie gromadzonych i aktualizowanych dowodów po każdej ich analizie. Ważnym elementem jest udowodnienie, że analizowana jest tylko kopia rzeczywistego dowodu cyfrowego, która po przeprowadzeniu dochodzenia nadal odpowiada oryginalnemu dowodowi. Oznacza to, że sama analiza nie sfałszowała dowodów.

Dobrze, upewniliśmy się, że nie wpadniemy w częstą pułapkę manipulowania dowodami i rozpoczęliśmy ich gromadzenie. Kolejnym ważnym krokiem jest upewnienie się, że powiadomimy odpowiednie osoby zainteresowane. Jako inżynierowie bezpieczeństwa, naszym głównym celem nie jest zajęcie się incydentem, ale powiadomienie zespołu, który udzieli im dalszej pomocy.

Podręczniki incydentów

Ten niebieski zespół Zazwyczaj jest doświadczony w radzeniu sobie z incydentami i gotowy do działania. Podobnie jak straż pożarna, powinien wykonywać wiele ćwiczeń i znać procedurę postępowania w razie wystąpienia incydentu. Jednym ze sposobów, w jaki…niebieski zespół Przygotowanie odbywa się poprzez tworzenie podręczników. Podręcznik zawiera kroki i działania, które zostały wstępnie zdefiniowane, aby pomóc zespołowi radzić sobie z incydentami. Celem podręcznika jest zapewnienie powtarzalności procesu podczas incydentu i zapobieżenie pominięciu jakichkolwiek działań. Zespół zazwyczaj korzysta z wielu podręczników, aby radzić sobie z różnymi typami incydentów, takimi jak: phishing lub włamania na konto. Te podręczniki są również ze sobą zintegrowane. Na przykład, jeśli dane uwierzytelniające zostały naruszone przez phishing, tenphishingPlaybook wskazywałby, że w tym momencie zespół również zacznie korzystać z playbooka dotyczącego kompromitacji konta. Poniżej znajduje się przykładowy playbook:  

Jako inżynier bezpieczeństwa zazwyczaj nie musisz tworzyć kompletnego playbooka dotyczącego incydentów. Możesz jednak być odpowiedzialny za stworzenie playbooka dla swojego działu, który będzie dokumentował, jak i gdzie należy zgłaszać incydenty.  

Drzewa wywołań

Zazwyczaj istnieje wiele sposobów, aby powiadomić zespół o wystąpieniu incydentu. W dużych organizacjach proces ten jest zazwyczaj w pełni zautomatyzowany dzięki systemom takim jak Jira, które umożliwiają rejestrowanie i eskalację zgłoszenia w zależności od wagi incydentu. Po utworzeniu zgłoszenia odpowiednie osoby zainteresowane zostaną automatycznie powiadomione.

Innym powszechnym podejściem jest wykorzystanie drzewa zgłoszeń. Drzewa zgłoszeń wskazują, kogo należy powiadomić i kto jest odpowiedzialny za powiadomienie. Struktura wskazuje również, do kogo można eskalować sprawę w przypadku, gdy dana osoba nie jest dostępna do wykonywania swoich obowiązków. Gdy eskalacja dotrze do odpowiedniego menedżera, może on wówczas udzielić pomocy, korzystając z własnego drzewa zgłoszeń, aby eskalować problem w zależności od powagi incydentu.

Jako inżynier ds. bezpieczeństwa możesz odpowiadać nie tylko za tworzenie drzewa połączeń dla swojego działu, ale także za pomoc w wskazywaniu, kiedy w drzewie połączeń może być konieczna eskalacja do niebieskiego zespółu.  

Odpowiedzialność ratownika medycznego

Jak wspomniano wcześniej, jako inżynier bezpieczeństwa, możesz nie być odpowiedzialny za tworzenie podręczników, a w niektórych przypadkach nawet za nadzorowanie drzewek. Twoim głównym obowiązkiem będzie jednak zapewnienie, że Twój oddział jest przygotowany na wypadek incydentu. Kontynuując przykład pożaru, możesz nie być odpowiedzialny za gaszenie pożaru, ale jesteś odpowiedzialny za wiedzę o lokalizacji alarmu przeciwpożarowego i najbliższych wyjść ewakuacyjnych. Podobnie, masz obowiązek przygotować swój oddział na incydent, upewniając się, że jego pracownicy wiedzą, gdzie mogą zgłosić incydent i z kim się skontaktować w razie wystąpienia incydentu.

Znaczenie powstrzymywania

Gdy już podniesiemy alarm, kolejnym krokiem jest powstrzymanie rozprzestrzeniania się. Czekając na przyjazd straży pożarnej, chcemy zadbać o to, aby szkody były jak najmniejsze. Ratownicy rzadko podejmują działania bez konsultacji z ratownikami.niebieski zespół; jednakże ważne jest, aby wiedzieć, czym jest powstrzymywanie i jak może ono działać. Ponadto, jako inżynier bezpieczeństwa, niebieski zespół możemy liczyć na Twoją pomoc jako eksperta w danej dziedzinie, który pomoże Ci zrozumieć, jakie metody powstrzymywania można wdrożyć w Twoim dziale.

Proces zarządzania incydentami obejmuje działania mające na celu powstrzymanie, wyeliminowanie i odzyskanie. NISTW ramach zarządzania incydentami te trzy elementy są pogrupowane. Należy jednak pamiętać, że są one unikalne i muszą być wdrażane w podanej kolejności. Największą pułapką podczas incydentu jest przejście do etapu eliminacji i odzyskiwania przed podjęciem odpowiednich działań zapobiegawczych. Jeśli dostęp sprawcy zagrożenia nie zostanie usunięty lub rozprzestrzenianie się incydentu nie zostanie powstrzymane, eliminacja i odzyskiwanie byłyby nie tylko nieskuteczne, ale również stratą czasu, ponieważ zespół musiałby powtarzać dokładnie te same działania. Z tego powodu można argumentować, że zapobieganie jest najważniejsze z tych trzech.  

Metody powstrzymywania

Jak wspomniano wcześniej, najlepszą metodą izolacji jest niewyłączanie hosta, ponieważ zniszczyłoby to dowody i potencjalnie zaalarmowało osobę atakującą. Istnieją jednak inne sposoby izolacji, które można zastosować:

- SiećSegmentacja- Host jest izolowany z perspektywy sieci poprzez umieszczenie go w innym segmencie sieci. Ta izolacja ma na celu uniemożliwienie rozprzestrzeniania się infekcji na inne hosty w sieci. Skuteczne [bezpieczeństwo sieci](https://tryhackme.com/room/intronetworksecurity) jest bardzo ważne!  
    
- Izolacja fizyczna – host jest gromadzony i całkowicie izolowany od sieci i użytkowników. Na przykład stacja robocza użytkownika zostaje skonfiskowana. Izolacja ta ma na celu uniemożliwienie wykonywania dalszych działań na hoście i zachowanie dowodów.  
    
- Wirtualna izolacja – host nie może komunikować się za pośrednictwem oprogramowania. Na przykład EDR Można go użyć do uwięzienia hosta, co oznacza, że ​​może on komunikować się tylko z określonymi podmiotami w sieci i wykonywać określone czynności. Cel tej izolacji jest podobny do konfiskaty hosta, ale można go przeprowadzić zdalnie. Ponadto, w niektórych przypadkach, jeśli EDR jest naruszony, może to nie zadziałać.  

Powrót aktorów zagrożeń do czasów połączeń dial-up

Jeśli powstrzymanie zagrożenia zaalarmuje sprawcę, pojawia się pytanie, czy izolacja jest rozwiązaniem. Chociaż w większości przypadków tak, istnieją pewne sytuacje, w których warto zastosować inne podejście. W niektórych przypadkach możemy chcieć zyskać na czasie, aby lepiej zbadać działania sprawcy.

Niektórzy twierdzą, że wolny internet jest gorszy niż brak internetu, ale to sprawdzona technika dla zespołów niebieskich. Zamiast przeprowadzać pełną izolację, zespół może zdecydować się na ograniczenie prędkości sieci, co często można zrobić poprzez…EDR W ten sposób prawdopodobieństwo, że atakujący podejrzewa, że ​​jesteśmy na jego tropie, jest mniejsze, ponieważ wszystko nadal działa; po prostu połączenie jest powolne. Biorąc pod uwagę, że atakujący muszą korzystać z kanałów dowodzenia i kontroli, nie byliby w stanie dokładnie określić problemu powodującego powolne połączenie. Spowolnienie połączenia pozwoli zespołowi na przeprowadzenie bardziej dogłębnej analizy wykonywanych działań, co może pomóc zespołowi lepiej zrozumieć zakres incydentu i umożliwić podjęcie szerszych działań zapobiegawczych po jego poznaniu.  

Odpowiedzialność ratownika medycznego

Jak wspomniano wcześniej, jako inżynier bezpieczeństwa możesz nie być odpowiedzialny za izolowanie incydentu. Będziesz jednak zobowiązany jako ekspert w danej dziedzinie, aby pomóc zespołowi zrozumieć, jakie metody powstrzymywania mogą być możliwe, a także zrozumieć, jaki wpływ miałoby ich wdrożenie.

Wywoływanie BCP

Skoro zaczęliśmy ograniczać incydent, czas na zdobycie supermocy. Jeśli powaga incydentu jest wystarczająca, czas uruchomić Plan Ciągłości Działania (BCP). BCP to plan mający na celu pomoc w odzyskaniu sprawności po incydencie. Należy pamiętać, że ponieważ BCP jest głównym celem, nie powinniśmy go wdrażać przed ograniczeniem incydentu.

Uruchomienie BCP daje nam pewne supermoce. Zazwyczaj istnieją określone procesy i kroki, które należy wdrożyć, aby coś zrobić w naszym dziale. Na przykład, nie możemy po prostu wprowadzić zmian w środowisku produkcyjnym; musi ono przejść przez cały proces rejestrowania zmiany, jej testowania, przeprowadzania kontroli jakości i wszystkiego innego, zanim zmiana będzie mogła zostać wprowadzona. Uruchomienie BCP pozwala nam jednak ominąć większość tych kroków. Jednak z wielką mocą wiąże się wielka odpowiedzialność, dlatego tylko wybrani członkowie kierownictwa wyższego szczebla mogą mieć możliwość uruchomienia BCP. Jak omówiono w następnym zadaniu, dokumentacja jest kluczowa podczas uruchamiania BCP. Po uruchomieniu BCP może on pomóc nam w powrocie do stanu sprzed incydentu, który nazywamy „Business as Usual” (BAU). BCP nie będzie uruchamiany zawsze, tylko w przypadkach, gdy powaga incydentu jest wystarczająca.  

Plan ciągłości działania a plan zapobiegania utracie danych

BCP jest bardzo podobny do Planu Odzyskiwania Po Awarii (DRP). Jednak DRP koncentruje się głównie na odzyskiwaniu technicznym naszego działu. BCP jest bardziej kompleksowy i obejmuje takie elementy, jak komunikacja z interesariuszami wewnętrznymi i zewnętrznymi. DRP jest zazwyczaj zawarty w BCP, aby ułatwić odzyskiwanie techniczne.

Tworzenie planu ciągłości działania (BCP)

Jako inżynier ds. bezpieczeństwa możesz odpowiadać za stworzenie planu ciągłości działania (BCP). Aby utworzyć skuteczny plan ciągłości działania, wykonaj następujące kroki:

1. **Przeprowadź analizę wpływu na biznes** – musisz przygotować się na najgorszy scenariusz. Przeprowadzając analizę, możesz określić, co może się wydarzyć w przypadku incydentu i jak wpłynie on nie tylko na Twoją organizację, ale także na Twoich klientów. Analiza jest zazwyczaj przeprowadzana z wykorzystaniem połączenia miar jakościowych i ilościowych.
2. **Zdefiniuj potencjalne działania naprawcze** – Na podstawie scenariuszy z pierwszego kroku możesz określić, jakie potencjalne działania naprawcze byłyby możliwe. Na przykład, w przypadku gdyby jeden z serwerów produkcyjnych przestał odpowiadać lub musiał zostać odizolowany, możesz potencjalnie przełączyć się na serwer odzyskiwania po awarii. Udokumentowanie tych działań naprawczych pozwoli zespołowi szybciej odzyskać dane w przypadku rzeczywistego incydentu.
3. **Zaplanuj strukturę zespołu ds. BCP** – Po uruchomieniu BCP pojawiają się pewne obowiązki, które należy spełnić, takie jak dokumentowanie działań i powiadamianie interesariuszy. Obowiązki te należy zaplanować i udokumentować wraz z danymi osób, które będą je wykonywać.
4. **Przetestuj plan BCP** — aby mieć pewność, że Twój plan BCP działa zgodnie z oczekiwaniami, musisz przeszkolić swój zespół w zakresie jego stosowania, a następnie przetestować go, przeprowadzając ćwiczenie symulacyjne.  

Metryki BCP

Jak wspomniano, analiza wpływu na biznes (Business Impact Analysis) będzie wykorzystywać miary ilościowe. Pozwolą one zespołowi określić, ile czasu zajmie wdrożenie działań naprawczych z planu ciągłości działania (BCP) i czy te terminy są akceptowalne. Poniżej przedstawiono niektóre z najczęściej stosowanych wskaźników.

- **Cel punktu odzyskiwania** – ilość danych, jaką jesteśmy gotowi zaakceptować, może zostać utracona. Na przykład, jeśli założymy, że jesteśmy gotowi stracić godzinę danych, ale nie więcej, nasze kopie zapasowe muszą być tworzone co godzinę.  
    
- **Cel czasu odzyskiwania** – ilość czasu potrzebna do odzyskania sprzętu naszego systemu  
    
- **Czas odzyskiwania pracy** – ilość czasu potrzebna na odzyskanie oprogramowania i danych naszego systemu  
    
- **Maksymalny dopuszczalny czas przestoju** – maksymalny czas przestoju, jaki jesteśmy gotowi zaakceptować. Musimy upewnić się, że nasze RTO i WRT łącznie nie przekroczą tego progu.
- **Średni czas między awariami** – jak długo nasz system będzie działał średnio między awariami  
    
- **Średni czas naprawy** – ile czasu zajmie nam odzyskanie systemu w ciągu roku?

Znaczenie dokumentacji

W przypadku uruchomienia BCP pomija się kilka kluczowych etapów procesu. Jak wspomniano wcześniej, BCP pozwala wyznaczonej osobie na wprowadzanie zmian bez przestrzegania właściwego procesu zarządzania zmianą. Chociaż pomaga to zespołowi szybciej uporać się z incydentem, oznacza to, że dokumentacja zmian nie jest już dostępna. Bez niej nie bylibyśmy w stanie odtworzyć naszych kroków. Dlatego nawet w przypadku uruchomienia BCP dokumentacja jest niezwykle ważna. Jako osoba udzielająca pierwszej pomocy, musisz upewnić się, że dokumentujesz wszelkie działania, które Ty lub zespół podejmujecie.odpoczynekzespołu trwa do momentu całkowitego przekazania niebieski zespół jest wykonywany.  

Szablony dokumentacji

Aby ułatwić proces dokumentowania, zazwyczaj zaleca się, aby dokument BCP zawierał również szablon dokumentacji, z którego można skorzystać. Nie chcemy tracić czasu na tworzenie go podczas incydentu, dlatego przygotowanie tego szablonu jest ważne. Szablon powinien umożliwiać podanie następujących informacji:

- Czas, w którym zażądano wykonania działania. Najlepiej podawać czas w standardowym formacie, takim jak:UTCaby zapewnić możliwość dopasowania czasów do innych źródeł
- Opis aktualizacji lub wykonanej czynności
- Uzasadnienie wykonania czynności
- Osoba zatwierdzająca wykonywaną czynność
- Osoba odpowiedzialna za wykonanie czynności
- Czas wykonania czynności
- Opis zmian zaobserwowanych po wykonaniu czynności

Jak widać powyżej, dokumentujemy nie tylko moment, w którym działanie zostało zlecone i przez kogo, ale także moment jego wykonania i osobę odpowiedzialną za jego wykonanie. Dzieje się tak, ponieważ często zdarza się, że działania są omawiane, ale nigdy nie są wdrażane, ponieważ osoba odpowiedzialna za ich wdrożenie nigdy nie została potwierdzona. Często może to prowadzić do zwiększenia zakresu incydentu, ponieważ zespół uważa, że ​​działania są wykonywane, podczas gdy traci się cenny czas.

Wyciągnięte wnioski

Dokumentacja jest ważna nie tylko dla pomyślnego przekazania, ale także daje nam możliwość późniejszego przeanalizowania incydentu i podjętych działań. Dzięki temu procesowi możemy zbadać, co poszło nie tak i co można zrobić, aby zapobiec temu w przyszłości. Ten proces pomaga nam zmniejszyć liczbę incydentów.

W tej sali dowiedzieliśmy się, co trzeba zrobić, żeby zostać ratownikiem. Podsumowując:

- Pamiętaj o zachowaniu dowodów i pamiętaj, że niektóre dowody mogą być bardziej nietrwałe.
- Upewnij się, że rozumiesz, w jaki sposób należy powiadomić o wystąpieniu incydentu – czy to poprzez zgłoszenie, czy za pomocą drzewa połączeń.
- Izolacja jest kluczowa dla zapewnienia ograniczenia skali incydentu. Istnieje jednak wiele różnych metod izolacji.
- Plan ciągłości działania (BCP) można wykorzystać w celu zapewnienia możliwości szybkiego wprowadzenia zmian mających na celu rozwiązanie problemu, jednak dokumentacja ma ogromne znaczenie, ponieważ umożliwia prześledzenie podjętych działań i jak najszybsze przywrócenie normalnego funkcjonowania środowiska.
