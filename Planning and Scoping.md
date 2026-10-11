Właśnie udało Ci się zdobyć pierwsze zlecenie konsultingowe. Średniej wielkości firma e-commerce, _BrightCart_ , znalazła się w centrum uwagi z zupełnie niewłaściwych powodów: w zeszłym kwartale padła ofiarą naruszenia bezpieczeństwa danych, a zarząd BrightCart zadał sobie teraz pytanie: „Czy to samo może się nam przydarzyć ponownie?”. Firma stosuje zapory sieciowe, program antywirusowy i politykę haseł. Ale czy te środki rzeczywiście działają? Zarząd chce dowodów i tu właśnie pojawia się Wasza pomoc.

Zabezpieczenie firmy to nie jednorazowe wydarzenie; to ciągły proces budowania zabezpieczeń _i_ ich testowania. W świecie analogowym nie wystarczy po prostu zamontować zapięcia na rowerze i bezgranicznie mu zaufać. Trzeba je pociągnąć. Próbować je otworzyć. Zachowuje się jak złodziej, aby sprawdzić, czy zapięcie działa. Świat cyfrowy działa według tej samej logiki, z tą różnicą, że „zamek” to połączenie zasad bezpieczeństwa, zapór sieciowych, systemów wykrywania włamań i kontroli dostępu, a „złodziej” to wykwalifikowany specjalista zatrudniony do ich testowania.

![Lupa nad dokumentem](https://cdn-images.tryhackme.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1779331126455.png)

Wyzwaniem jest to, że testowanie bezpieczeństwa systemów komputerowych jest o wiele bardziej złożone niż szarpanie za zamek rowerowy. Powierzchnia ataku firmy może przęsło Aplikacje internetowe, sieci wewnętrzne, infrastruktura chmurowa, interfejsy API i aplikacje mobilne. Każdy z nich wymaga specjalistycznych umiejętności i narzędzi do prawidłowej oceny. Z tego powodu organizacje polegają na testerach penetracyjnych – autoryzowanych specjalistach, którzy symulują rzeczywiste cyberataki, aby znaleźć luki w zabezpieczeniach, zanim zrobią to cyberprzestępcy.

Słowo kluczowe w tej definicji to **„autoryzowany”** . Bez wyraźnego, udokumentowanego upoważnienia ze strony organizacji klienta, test penetracyjny jest nie do odróżnienia od ataku przestępczego. Jak zobaczymy na tej sali, planowanie, określenie zakresu i przygotowanie prawne, które mają miejsce _przed_ wysłaniem choćby jednego pakietu, odróżniają profesjonalne zaangażowanie od nielegalnego włamania.

## Wymagania wstępne

Ta sala bazuje na koncepcjach przedstawionych w salach [„Guided Pentest: Infrastructure”](https://tryhackme.com/room/guidedpentestinfrastructure) i [„Dive Into Pentesting”](https://tryhackme.com/room/diveintopentesting) . Zanim zagłębisz się w szczegóły planowania i zakresu testów penetracyjnych, powinieneś zapoznać się z ogólną ideą tego, jak wygląda test penetracyjny od początku do końca.

## Cele edukacyjne

- Wyjaśnij, czym jest test penetracyjny i czym różni się od testu penetracyjnego, ocena podatności
- Rozróżnij podejście do znanego środowiska, częściowo znanego środowiska i nieznanego środowiska
- Określ zakres testu penetracyjnego i zidentyfikuj ryzyko błędów w zakresie
- Zidentyfikuj dokumenty prawne i zezwolenia wymagane przed rozpoczęciem testów
- Opisz kluczowe elementy dokumentu zasad zaangażowania
- Rozpoznać główne ramy regulacyjne, które nakazują lub zalecają przeprowadzanie testów penetracyjnych
- Zastosuj koncepcje planowania i określania zakresu do realistycznego scenariusza klienta

Wróćmy do BrightCart, firmy e-commerce z poprzedniego zadania. Zarząd zatwierdził budżet i firma jest gotowa zatrudnić zespół do testów penetracyjnych. Zanim jednak testerzy otworzą terminal, warto zadać sobie fundamentalne pytanie: do czego _właściwie_ zostali zatrudnieni?

Test **penetracyjny** to **kompleksowa ocena bezpieczeństwa,** w ramach której autoryzowani specjaliści symulują rzeczywiste cyberataki na systemy, sieci lub aplikacje organizacji. Celem jest wykrycie luk w zabezpieczeniach i zademonstrowanie ich potencjalnego wpływu, _zanim_ atakujący będzie mógł je wykorzystać. Dwa słowa w tej definicji zasługują na szczególną uwagę: **autoryzowany** i **symulować** . Testerzy mają wyraźne pozwolenie na przeprowadzenie ataku i robią to w sposób kontrolowany, mający na celu ocenę ryzyka bez powodowania trwałych szkód.

**Innymi słowy, test penetracyjny pomaga ocenić stan bezpieczeństwa** organizacji . Dokładniej rzecz ujmując, test penetracyjny ma na celu:

- **Identyfikuj luki w zabezpieczeniach** wynikające z wad oprogramowania, błędnych konfiguracji, słabych poświadczeń lub błędów projektowych
- **Oceń wpływ** udanej eksploatacji, aby organizacja mogła oszacować rzeczywistą wagę każdego odkrycia
- **Ocena skuteczności** istniejących rozwiązań bezpieczeństwa i środków obronnych
- **Sporządź raport** z praktycznymi zaleceniami dotyczącymi poprawy mechanizmów obronnych organizacji

Z perspektywy klienta, test penetracyjny odpowiada na proste, ale kluczowe pytanie: „Gdzie jesteśmy narażeni, jak źle może być i co z tym zrobić?”. Tester penetracyjny powinien mieć tę perspektywę na uwadze przez cały czas trwania projektu. Każde odkrycie, każdy exploit i każda rekomendacja ostatecznie służą potrzebie klienta, aby chronić swoje zasoby i użytkowników.

## Cykl życia testów penetracyjnych

Test penetracyjny przebiega według ustrukturyzowanego procesu od początku do końca. Ten cykl życia jest definiowany przez kilka branżowych ram; najczęściej cytowanym jest [Standard Wykonania Testów Penetracyjnych (PTES).(otwiera się w nowej karcie)](http://www.pentest-standard.org/index.php/Main_Page), który dzieli test penetracyjny na siedem faz:

1. **Interakcje przed rozpoczęciem prac:** Określanie zakresu, zasad i umów prawnych przed rozpoczęciem jakichkolwiek testów
2. **Gromadzenie informacji wywiadowczych:** Zbieranie informacji o celu za pomocą rozpoznania pasywnego i aktywnego
3. **Modelowanie zagrożeń:** Identyfikacja najbardziej prawdopodobnych scenariuszy ataków na podstawie zebranych informacji wywiadowczych
4. **Analiza podatności:** systematyczne wykrywanie słabych punktów w systemach docelowych
5. **Wykorzystanie:** Próba wykorzystania odkrytych luk w celu uzyskania nieautoryzowanego dostępu
6. **Po eksploatacji:** Określanie wartości zagrożonych systemów i utrzymywanie dostępu w celu dalszej analizy
7. **Raportowanie:** Dokumentowanie ustaleń, wpływu i wskazówek dotyczących działań naprawczych dla klienta

Zauważ, że tylko dwie z tych siedmiu faz (eksploatacja i posteksploatacja) obejmują praktyczne „hakowanie”, które większość ludzi wyobraża sobie, słysząc o „teście penetracyjnym”. Zasadnicza część profesjonalnego zaangażowania to planowanie, analiza i raportowanie. Ta sala koncentruje się na fazie 1, interakcjach przed zaangażowaniem, czyli planowaniu i określaniu zakresu, które umożliwiają realizację wszystkich pozostałych etapów.

Warto zauważyć, że ostatnia aktualizacja PTES miała miejsce w 2014 r. Pomimo swojego wieku, pozostaje ona najczęściej cytowanym w branży systemem zarządzania cyklem życia i jest powoływana przez standardy zgodności, takie jakPCI DSSPoprzednia część tej ścieżki, zatytułowana [„Struktury testów penetracyjnych”](https://tryhackme.com/room/penetrationtestingframeworks) , omawia PTES i inne struktury bardziej szczegółowo.

## Testowanie penetracyjne kontra Ocena podatności

Pytanie, które często pojawia się na wczesnym etapie kariery w cyberbezpieczeństwie: czym różni się test penetracyjny od **oceny podatności** ? Te dwa procesy są komplementarne, ale jednocześnie odrębne.

Jedną z analogii byłoby porównanie wizyty u lekarza na rutynowe badanie kontrolne z testem wysiłkowym serca. Badanie kontrolne (ocena podatności) obejmuje szeroki zestaw standardowych testów, sygnalizuje wszelkie nieprawidłowości i przedstawia listę wyników. Test wysiłkowy (test penetracyjny) testuje organizm do granic możliwości w kontrolowanych warunkach, aby dokładnie określić, jak i gdzie zawodzi. Oba są cenne; odpowiadają na różne pytania.

Mówiąc językiem technicznym:

- Ocena **podatności** jest szeroka, ale powierzchowna. Opiera się głównie na zautomatyzowanych narzędziach skanujących (np. Nessus, OpenVAS lub Qualys) w celu identyfikacji _znanych_ luk w zabezpieczeniach w szerokiej gamie systemów. Wynikiem jest skategoryzowana lista słabych punktów wraz z oceną ich ważności. Większość pracy wykonuje automatyzacja.
- Test **penetracyjny** jest wąski, ale głęboki. Jest to ćwiczenie w przeważającej mierze manualne, prowadzone przez człowieka, w którym tester aktywnie _wykorzystuje_ luki w zabezpieczeniach, aby zademonstrować rzeczywisty wpływ. Tester łączy ze sobą ustalenia, zwiększa uprawnienia i działa lateralnie, tak jak zrobiłby to prawdziwy atakujący. Wynikiem jest szczegółowa relacja z tego, co osiągnięto, do jakich danych uzyskano dostęp i jak daleko zaszedł tester.

Organizacje odnoszą korzyści z częstego przeprowadzania oceny podatności (kwartalnie, a nawet co miesiąc) w celu utrzymania higieny, a następnie okresowego przeprowadzania testów penetracyjnych (corocznie lub po wprowadzeniu istotnych zmian), aby zweryfikować, które zagrożenia przekładają się na realne ryzyko. Jedno nie zastępuje drugiego.

Zarząd BrightCart zatwierdził test penetracyjny. Teraz rozmowa przenosi się na szczegóły. Dyrektor ds. Bezpieczeństwa Informacji (CISO) pyta: „Co dokładnie testujemy i ile nasi testerzy powinni wiedzieć przed rozpoczęciem testu?”. Te dwa pytania determinują projekt każdego projektu. **_To, co_** decyduje o rodzaju testu, a to, **_jak dużo_** testów jest determinuje podejście.

## Rodzaje testów penetracyjnych

Testy penetracyjne są kategoryzowane według ocenianej technologii docelowej. W zależności od potrzeb organizacji klienta, test penetracyjny może koncentrować się na jednym lub kilku z poniższych elementów:

- **Test penetracji sieci:** obejmuje wewnętrzną i zewnętrzną infrastrukturę sieciową organizacji, w tym routery, przełączniki, zapory sieciowe i serwery
- **Test penetracyjny aplikacji internetowych:** ocena witryn internetowych, portali internetowych i ich usług zaplecza pod kątem luk w zabezpieczeniach, takich jak:SQLwstrzyknięcie, atak między witrynami (XSS) i wady uwierzytelniania
- **Test penetracji sieci bezprzewodowych:** ocena bezpieczeństwa sieci Wi-Fi, punktów dostępowych i protokołów bezprzewodowych
- **Test penetracji chmury:** badanie konfiguracji infrastruktury chmurowej, zarządzanie tożsamościami i dostępem (JA JESTEM) zasady i uprawnienia do przechowywania danych u różnych dostawców, takich jakAWS, Azure lub Google Cloud Platform (GCP)
- **Test penetracyjny aplikacji mobilnych:** testowanie aplikacji na iOS i Androida wraz z powiązanymi interfejsami API i usługami zaplecza
- **Test penetracji fizycznej:** ocena kontroli bezpieczeństwa fizycznego obiektu, takich jak czytniki identyfikatorów, zamki i systemy nadzoru

Organizacja taka jak BrightCart, której działalność koncentruje się wokół aplikacji e-commerce, z pewnością potrzebowałaby testu penetracyjnego aplikacji webowej. Jeśli BrightCart obsługuje również infrastrukturę wewnętrzną i akceptuje płatności, test penetracyjny sieci byłby również niezbędny, szczególnie biorąc pod uwagę wymogi zgodności, które omówimy w Zadaniu 7.

## Metody testowania: Ile wie tester?

Istnieją różne podejścia do przeprowadzania testów penetracyjnych. Podejścia te zależą od ilości informacji o środowisku docelowym udostępnionych testerowi penetracyjnemu przed rozpoczęciem współpracy. Firma ocenia swoje potrzeby i podejmuje decyzję na tej podstawie.

Istnieją trzy podejścia:

- **Znane środowisko** : znane również jako testowanie **typu „white-box”** . Klient udostępnia szczegółowe informacje o swoim środowisku, w tym schematy sieci, inwentaryzacje systemów, kod źródłowy, dane uwierzytelniające i dokumentację architektury. To podejście maksymalizuje wykrywanie luk w zabezpieczeniach, pozwalając testerowi skupić się na analizie, a nie na rekonesansie.
- **Środowisko częściowo znane** : Nazywane również testowaniem **szarej skrzynki** . Tester otrzymuje częściową wiedzę, taką jak konto użytkownika, informacje o architekturze wysokiego poziomu lub ograniczoną dokumentację, ale nie ma pełnego wglądu w środowisko. To podejście równoważy realizm z wydajnością.
- **Nieznane środowisko** : znane również jako testowanie **typu „black-box”** . Tester otrzymuje jedynie minimalne informacje potrzebne do zdefiniowania zakresu, często tylko nazwę firmy lub zakres adresów IP. Tester zaczyna od zera, symulując zewnętrznego atakującego bez wiedzy osoby z wewnątrz.

Uwaga dotycząca terminologii: branża odchodzi od etykiet „pudełkowych” opartych na kolorze na rzecz etykiet „środowiskowych” opartych na wiedzy. W terenie spotkasz się z obydwoma, dlatego ważne jest, aby biegle posługiwać się każdym z nich.

Rozważmy ponownie scenariusz BrightCart. Jeśli BrightCart chce odkryć jak najwięcej luk w zabezpieczeniach swojej aplikacji internetowej, wybrałby podejście oparte na znanym środowisku i przyznałby testerowi penetracyjnemu dostęp do kodu źródłowego aplikacji. W końcu lepiej, aby osoba pracująca _dla_ firmy znalazła wszystkie słabe punkty, zanim zrobi to ktoś działający _przeciwko_ niej. Udostępnianie kodu źródłowego wymaga odpowiednich umów prawnych, a konkretnie **umowy o zachowaniu poufności (NDA)** .

## Testowanie wewnętrzne a zewnętrzne

_Oprócz podejścia opartego na poziomie wiedzy, testy penetracyjne są również klasyfikowane według pozycji początkowej_ testera :

- Zewnętrzny **test penetracyjny** ma na celu sprawdzenie zasobów organizacji mających dostęp do Internetu, takich jak serwery WWW, serwery poczty e-mail,VPNbramy,DNSinfrastruktura i usługi w chmurze. Główne pytanie brzmi: „Czy zewnętrzny atakujący może się dostać do środka?”
- Wewnętrzny **test penetracyjny** ocenia bezpieczeństwo w _obrębie_ sieci organizacji. Tester zaczyna od pozycji, jaką zajmowałby osoba z wewnątrz lub atakujący po włamaniu. Kluczowe pytanie brzmi: „Gdy atakujący dostanie się do środka, jak daleko może się posunąć?”

Jedną z analogii byłoby testowanie bezpieczeństwa budynku. Test zewnętrzny sprawdza, czy osoba z zewnątrz może przejść przez drzwi wejściowe, okna lub rampę załadunkową. Test wewnętrzny zakłada, że ​​ktoś jest już w holu i sprawdza, czy może dotrzeć do serwerowni, piętra dla kadry kierowniczej lub skarbca. Obie perspektywy są niezbędne dla uzyskania pełnego obrazu. W rzeczywistości standardy zgodności, takie jakPCI DSSwymagają corocznych testów penetracyjnych _zarówno_ wewnętrznych, jak i zewnętrznych.

## Red Team kontra test penetracyjny

Czasami termin **„red team engagement”** jest używany obok lub mylony z testami penetracyjnymi. Choć techniki te mają podobne ofensywne techniki bezpieczeństwa, różnią się zakresem, czasem trwania i celami:

- Test **penetracyjny** ma zdefiniowany, konkretny zakres (taki jak aplikacja internetowa lub zakres adresów IP), trwa zazwyczaj od jednego do trzech tygodni i jest przeprowadzany za wiedzą organizacji klienta. Jego celem jest zidentyfikowanie i zgłoszenie jak największej liczby luk w zabezpieczeniach w obrębie obszaru docelowego.
- **Zaangażowanie zespołu „czerwonego”** obejmuje całą organizację i może trwać od kilku tygodni do kilku miesięcy. Zespoły „czerwone” testują ludzi, procesy i technologie jednocześnie, często wykorzystującinżynieria społeczna, wtargnięcie fizyczne i ataki techniczne w połączeniu. Co istotne, zespół czerwony działa w ukryciu; kluczowym miernikiem sukcesu jest to, czy obrońcy organizacji (**niebieski zespół**) może wykryć włamanie.

Na tym etapie test penetracyjny jest właściwym punktem wyjścia dla BrightCart. Zaangażowanie zespołu Red Team wymaga wyższego poziomu dojrzałości bezpieczeństwa organizacji, dojrzałego Centrum Operacji Bezpieczeństwa (SOC) oraz zespół niebieski, który jest gotowy do testów. Pomyśl o tym jak o progresji: organizacje zazwyczaj zaczynają od oceny podatności, przechodzą do testów penetracyjnych, a następnie, w miarę dojrzewania programu bezpieczeństwa, przeprowadzają działania zespołu czerwonego.

Rozważmy następujący scenariusz. BrightCart zatrudnia zespół do testów penetracyjnych i po dwóch tygodniach testów zespół przedstawia raport. CISO zapoznaje się z nim i natychmiast zauważa problem: testerzy spędzili większość czasu na stronie internetowej firmy, ale nigdy nie zajęli się przetwarzaniem płatności.API, wewnętrznego portalu pracowniczego lub chmurowych kontenerów pamięci masowej, w których przechowywane są dane klientów. Tymczasem testerzy przypadkowo przeszukali system zewnętrznego dostawcy usług logistycznych, który współdzieli segment sieci z BrightCart, a dostawca ten grozi teraz podjęciem kroków prawnych.

Co poszło nie tak? Zakres był źle zdefiniowany. Testerzy nie mieli jasnego planu, co testować, a co zostawić w spokoju. To nie jest hipotetyczny problem; zdarza się w rzeczywistych projektach, a konsekwencje wahają się od zmarnowanych budżetów po pozwy sądowe.

## Czym jest Scope?

Zakres testu penetracyjnego określa granice zaangażowania. Odpowiada on na dwa fundamentalne pytania: jakie systemy, sieci i aplikacje masz **prawo** _testować_ , a co jest wyraźnie _zabronione_ ?

Jak wspomnieliśmy w poprzednim zadaniu, słowo „autoryzowane” jest kluczowe w testach penetracyjnych. Dokument określający zakres to miejsce, w którym to upoważnienie staje się konkretne i konkretne. Musisz wiedzieć, które zasoby znajdują się na liście **dozwolonych** (cele w zakresie, które masz uprawnienia do testowania), a które na  **liście** **zablokowanych** (zasoby spoza zakresu, których nie wolno dotykać). Bez tej jasności ryzykujesz dwa scenariusze: pominięcie systemów, które powinny zostać przetestowane, co prowadzi do słabego, niekompletnego raportu, lub zaatakowanie systemów poza zakresem, co grozi problemami prawnymi.

## Co zawiera dokument zakresu?

Dobrze zdefiniowany zakres obejmuje następujące kategorie:

- **Systemy i sieci docelowe** : zakresy adresów IP (zarówno zewnętrznych, jak i wewnętrznych), listy domen i subdomen, podsieci sieciowe oraz wszelka prywatna lub publiczna infrastruktura chmurowa
- **Aplikacje i usługi** : adresy URL aplikacji internetowych, punkty końcowe API, aplikacje mobilne i powiązane z nimi usługi zaplecza
- **Sieci bezprzewodowe** : należy ocenić identyfikatory SSID, lokalizacje punktów dostępu i protokoły bezprzewodowe
- **Infrastruktura chmurowa** : Konkretne konta chmurowe, regiony,JA JESTEMkonfiguracje i usługi przechowywania danych u różnych dostawców, takich jakAWS, Azure lub GCP
- **Konta i role użytkowników** : konta testowe udostępnione do uwierzytelnionego testowania, w tym poziomy uprawnień dla każdego konta

Podobnie, dokument zakresu określa zasoby **poza zakresem** , zazwyczaj wymienione jako zakresy adresów IP, domeny lub usługi, których nie wolno modyfikować podczas realizacji projektu. Typowe powody wykluczenia zasobów to:

- **Bazy danych produkcyjnych** : zawierające bieżące dane klientów, w przypadku których jakiekolwiek zakłócenia mogłyby wpłynąć na działalność biznesową
- **Systemy stron trzecich** : hostowane przez dostawców lub partnerów, których klient nie jest właścicielem i nie może autoryzować przeprowadzania testów
- **Wspólna infrastruktura** : W tym przypadku wpływ będą mieli inni najemcy lub organizacje
- **Zamrożenie systemów w trakcie zmian** : ze względu na nadchodzące wydanie lub okno audytu regulacyjnego

Rozważ poniższy przykład, jak mógłby wyglądać dokument o częściowym zakresie dla BrightCart:

|Kategoria|W zakresie|Poza zakresem|
|---|---|---|
|ZewnętrznyAdresy IP|`203.0.113.0/24`|`203.0.113.50`(bramka płatności stron trzecich)|
|Domeny|`brightcart.thm`,`api.brightcart.thm`|`mail.brightcart.thm` (hostowane przez zewnętrznego dostawcę)|
|Aplikacje internetowe|Portal klienta, panel administracyjny|Portal zarządzania dostawcami (należący do partnera logistycznego)|
|Chmura|`us-east-1`Konto produkcyjne AWS|`eu-west-1`Konto odzyskiwania po awarii AWS|
|Bezprzewodowy|Wi-Fi w siedzibie głównej firmy (SSID: `BC-Corp`)|Sieć gościnna (SSID: `BC-Guest`)|

Ta tabela jest uproszczona dla zobrazowania, ale oddaje istotę schematu: każda kategoria ma jasno określoną listę dozwolonych i zablokowanych. Nie ma wątpliwości co do tego, co testerzy mogą, a czego nie mogą modyfikować.

## Dwie pułapki: zbyt szerokie i zbyt wąskie

Istnieją dwa powszechne błędy w określaniu zakresu, które niosą ze sobą poważne konsekwencje.

Zbyt **szeroki zakres** szkodzi wszystkim zaangażowanym stronom. Zespół ds. testów penetracyjnych jest zmuszony rozłożyć swoje wysiłki na zbyt wiele systemów, co prowadzi albo do wydłużenia czasu realizacji zlecenia, albo, częściej, do płytkich, powierzchownych testów, które nie obejmują dogłębnie żadnego pojedynczego celu. Z perspektywy klienta, szeroki zakres oznacza wyższe koszty, opóźnienia w raportowaniu i wyniki, które mogą nie być wystarczająco szczegółowe, aby skutecznie określić priorytety działań naprawczych.

Z drugiej strony, zbyt **wąski zakres** tworzy niebezpieczny martwy punkt. To tak, jakby testować bezpieczeństwo drzwi wejściowych, ignorując okna na parterze. Atakującemu nie zależy na tym, które zasoby zdecydujesz się przetestować; sprawdza wszystko. Jeśli zakres wyklucza krytyczne wektory ataku, test penetracyjny daje niewystarczającą ocenę ryzyka i pozostawia klienta z fałszywym poczuciem bezpieczeństwa. W branżach regulowanych zbyt wąski zakres może również prowadzić do nieprzestrzegania przepisów.PCI DSSNa przykład asesor będzie oczekiwał, że test penetracyjny obejmie _całe_ środowisko danych posiadacza karty (CDE), a nie tylko te części, które klient uznał za bezpieczne podczas testowania.

Optymalny zakres zapewnia równowagę między dokładnością a praktycznością. Obejmuje on wszystkie krytyczne i wysokiego ryzyka zasoby, jednocześnie pozostając osiągalnym w ramach harmonogramu i budżetu projektu. Określenie tej równowagi jest procesem współpracy zespołu ds. testów penetracyjnych z klientem; żadna ze stron nie powinna podejmować decyzji samodzielnie.

## Rozszerzanie zakresu

Kolejnym zagrożeniem, na które należy zwrócić uwagę, jest zjawisko „ **pełzania zakresu** ”. Ma ono miejsce, gdy granice projektu stopniowo rozszerzają się w trakcie testu bez formalnej zmiany w dokumencie zakresu. Na przykład, klient może mimochodem wspomnieć w trakcie projektu: „A tak przy okazji, czy mógłby Pan również rzucić okiem na nasz nowy serwer testowy?”. Bez udokumentowanej zmiany zakresu, prowadzi to do niejasności dotyczących autoryzacji i może prowadzić do sporów dotyczących produktów końcowych, harmonogramów i rozliczeń.

Rozwiązanie jest proste. Każda zmiana zakresu w trakcie aktywnego zaangażowania powinna zostać udokumentowana na piśmie, zatwierdzona przez obie strony i dołączona do pierwotnej umowy o zakresie przed rozpoczęciem dodatkowych testów. Szybkie potwierdzenie e-mailem jest lepsze niż nic, ale formalna zmiana zakresu jest standardem zawodowym.

[We wrześniu 2019 r. aresztowano i oskarżono o włamanie](https://www.iowacourts.gov/collections/445/files/919/embedDocument) dwóch testerów penetracyjnych z firmy ochroniarskiej Coalfire[(otwiera się w nowej karcie)](https://www.iowacourts.gov/collections/445/files/919/embedDocument)Ich przestępstwo? Włamanie do sądu okręgowego w stanie Iowa, _dokładnie tak, jak ich zatrudniono_ . Administracja Sądu Stanowego zleciła firmie Coalfire przeprowadzenie testu penetracji fizycznej budynków sądowych w całym stanie. Testerzy mieli przy sobie podpisany list autoryzacyjny. Wykonywali swoją pracę.

Problem polegał na tym, że szeryf hrabstwa nie był świadomy zaangażowania, a list autoryzacyjny nie określał jednoznacznie, kto ma władzę prawną nad budynkiem sądu. Testerzy spędzili noc w areszcie, wpłacając kaucję w wysokości 50 000 dolarów każdy. Urzędnicy stanowi, którzy ich zatrudnili, początkowo zdystansowali się od sprawy. Umorzenie zarzutów zajęło miesiące, a w 2024 roku hrabstwo Dallas zapłaciło 600 000 dolarów w ramach ugody w sprawie bezprawnego aresztowania.

Ta sprawa nie jest historią sprzed wieków; to bezpośrednia lekcja pokazująca, dlaczego planowanie przedwstępne i dokumentacja prawna to nie biurokratyczne formalności. To one chronią przed kajdankami.

## Dlaczego podstawy prawne są najważniejsze

Zanim tester penetracyjny otworzy terminal, uruchomi skaner lub wyśle ​​pojedynczy pakiet, konieczne jest podpisanie szeregu umów prawnych. Dokumenty te pełnią dwa cele: upoważniają **testera** do wykonywania działań, które w innym przypadku byłyby nielegalne, oraz **chronią** obie strony, określając zakres odpowiedzialności, granice i oczekiwania.

Jak ustaliliśmy w Zadaniu 1, słowo „autoryzowany” odróżnia test penetracyjny od ataku przestępczego. Faza poprzedzająca zaangażowanie to moment, w którym autoryzacja staje się podpisaną, prawnie wiążącą rzeczywistością.

## Podstawowe dokumenty prawne

Profesjonalne testy penetracyjne zazwyczaj obejmują cztery kluczowe dokumenty, wykonywane mniej więcej w następującej kolejności:

1. **Umowa o zachowaniu poufności (NDA)** : Podpisywane w pierwszej kolejności, często przed udostępnieniem jakichkolwiek szczegółów technicznych. Umowa NDA, czasami obustronna, zapewnia obu stronom ochronę informacji poufnych wymienianych podczas rozmów dotyczących zakresu prac i w trakcie trwania współpracy. Zazwyczaj określa ona zakres informacji poufnych (dane o podatnościach, architekturę sieci, dane uwierzytelniające, wyniki testów), okres obowiązywania zobowiązania do zachowania poufności (zwykle od 2 do 5 lat), wymagania dotyczące przetwarzania i przechowywania danych oraz procedury powiadamiania o naruszeniach.
2. **Umowa ramowa o świadczenie usług (MSA)** : Umowa ta ustanawia nadrzędny stosunek prawny między klientem a firmą testującą. Obejmuje ona kwestie odpowiedzialności i odszkodowania, prawa własności intelektualnej, mechanizmy rozstrzygania sporów oraz wymogi ubezpieczeniowe. Umowa MSA jest negocjowana jednorazowo i reguluje wszystkie przyszłe zobowiązania między obiema stronami.
3. **Oświadczenie o pracy (SIAĆ)** : To dokument specyficzny dla danego zlecenia. Każdy test penetracyjny ma swój własny SOW (Specyfikacja Pracy), który definiuje systemy do przetestowania (zakres), metodologię i podejście, harmonogram i kamienie milowe, produkty końcowe (zazwyczaj raport) oraz koszt. Kluczowa różnica: MSA określa zasady relacji; SOW szczegółowo opisuje każdy konkretny test.
4. **List autoryzacyjny** : Znany również jako **list „wyjścia z więzienia na wolność”** , ten dokument udziela wyraźnej pisemnej zgody na przeprowadzenie testu. Prawidłowy list autoryzacyjny zawiera pełną nazwę prawną testera i nazwę firmy, konkretny zakres dat autoryzowanego testu, objęte nim systemy, obiekty lub sieci, dozwolone działania (testowanie sieci, wejście fizyczne,inżynieria społeczna, itp.) oraz dane kontaktowe co najmniej dwóch przedstawicieli klienta, z którymi można się skontaktować w godzinach testów. List _musi_ zostać podpisany przez osobę posiadającą niekwestionowane uprawnienia prawne do testowanych zasobów, zazwyczaj CISO, CIO, CEO lub wiceprezesa ds. IT. Jak pokazuje sprawa Coalfire, niejasność co do tego, kto jest uprawniony do autoryzacji testów, może mieć poważne konsekwencje.

## Obowiązujące prawa

Dwa przepisy są szczególnie istotne dla testerów penetracyjnych działających w Stanach Zjednoczonych i Wielkiej Brytanii.

Ustawa **o oszustwach komputerowych i nadużyciach (Computer Fraud and Abuse Act, CFAA)** , skodyfikowana w 18 USC § 1030, jest podstawowym federalnym prawem USA dotyczącym przeciwdziałania hakerstwu. Zabrania ona nieautoryzowanego dostępu do chronionych komputerów, kategorii obejmującej praktycznie każdy system podłączony do internetu. Kary sięgają do 10 lat pozbawienia wolności za umyślny nieautoryzowany dostęp. W 2021 roku Sąd Najwyższy Stanów Zjednoczonych wydał przełomowe orzeczenie w sprawie **Van Buren przeciwko Stanom Zjednoczonym** , które wyjaśniło zakres ustawy CFAA. Sąd orzekł w orzeczeniu większością 6 do 3 głosów, że „przekroczenie autoryzowanego dostępu” ma zastosowanie tylko wtedy, gdy ktoś uzyskuje dostęp do obszarów komputera, które są dla niego całkowicie niedostępne, a nie wtedy, gdy nadużywa dostępu, który w innym przypadku posiada. Społeczność badaczy bezpieczeństwa z zadowoleniem przyjęła tę węższą interpretację, choć nie eliminuje ona potrzeby wyraźnego pisemnego upoważnienia. W 2022 roku Departament Sprawiedliwości ponownie zrewidował swoją politykę pobierania opłat na podstawie ustawy CFAA, aby odmówić ścigania badań nad bezpieczeństwem prowadzonych w dobrej wierze. Jest to wytyczna prokuratorska, a nie ustawowa bezpieczna przystań; przyszła administracja może to cofnąć, nie będzie to miało wpływu na odpowiedzialność cywilną.

Brytyjska **ustawa o nadużyciach komputerowych z 1990 r. (CMA)** definiuje trzy główne rodzaje przestępstw: nieautoryzowany dostęp do materiałów komputerowych (art. 1, kara do 2 lat pozbawienia wolności), nieautoryzowany dostęp z zamiarem popełnienia dalszych przestępstw (art. 2, kara do 5 lat) oraz nieautoryzowane działania zakłócające działanie komputera (art. 3, kara do 10 lat). W przeciwieństwie do przepisów obowiązujących po uchwaleniu ustawy CFAA w sprawie Van Burena, ustawa CMA _nie zawiera wyraźnych przepisów ustawowych_ dotyczących legalnych testów bezpieczeństwa. Autoryzacja musi zostać udzielona przez właściciela systemu w wyraźnej, pisemnej formie. Organizacje branżowe z branży bezpieczeństwa, w tym CREST i NCC Group, apelowały o reformę ustawy CMA w celu wprowadzenia ustawowej ochrony przed testami w dobrej wierze. Jednak do początku 2026 r. taka nowelizacja nie została jeszcze uchwalona.

Wniosek dla testerów penetracyjnych jest prosty: **pisemne upoważnienie nie jest opcjonalne. Jest niezbędne.** Bez niego każda stosowana technika, od skanowania portów po eksploatację, jest potencjalnie przestępstwem w rozumieniu jednego lub obu tych przepisów.

## Zasady testowania dostawców usług w chmurze

Jeśli infrastruktura klienta obejmuje usługi chmurowe, tester penetracyjny musi zweryfikować zasady testowania dostawcy chmury. Od 2025 roku wszyscy trzej główni dostawcy zezwalają na testowanie penetracyjne zasobów należących do klienta bez konieczności uzyskania uprzedniej zgody:

- **AWS**umożliwia testowanie usług obejmującychEC2, RDS,CloudFrontZorza polarnaAPIWejście,Lambda, Lightsail i Elastic Beanstalk.DoStestowanie,DNSzabronione jest poruszanie się pieszo trasą nr 53 oraz zalewanie portu.
- **Microsoft Azure** zezwala na testowanie na zasobach należących do klienta bez konieczności wcześniejszego powiadomienia. Testowanie DoS, ataki międzydzierżawcze i socjotechnika w stosunku do pracowników Microsoft są zabronione.
- **Platforma Google Cloud Platform (GCP)** nigdy nie wymagała powiadomienia ani wcześniejszej zgody. Testy mogą być przeprowadzane wyłącznie na własnych projektach testera i zgodne z Polityką Dozwolonego Użytkowania.

Wszyscy trzej dostawcy surowo zabraniają testowania ataków typu Denial-of-Service (DoS) oraz testowania zasobów innych klientów. W ramach współpracy z BrightCart, zespół testujący musiałby potwierdzić, że testy AWS odbywają się na koncie BrightCart us-east-1 (zgodnie z definicją w zakresie zadania 4) i nie obejmują żadnych zabronionych działań.

Termin **„Zasady Działania** ” wywodzi się z doktryny wojskowej. W tym kontekście Zasady Działania to dyrektywy określające, kiedy, gdzie i jak siły zbrojne mogą angażować przeciwników lub używać siły. Zapewniają one, że działania militarne są zgodne z celami strategicznymi, przy jednoczesnym poszanowaniu granic prawnych i etycznych. Definiują one, co może być celem ataku oraz jaka broń i taktyka są dozwolone.

Testy penetracyjne bezpośrednio zapożyczają tę koncepcję. W teście penetracyjnym **zasady zaangażowania (Ikra)** to formalne porozumienia, które określają granice operacyjne zaangażowania: co można testować, kiedy testowanie może się odbyć, jak strony się komunikują i co się dzieje, gdy coś pójdzie nie tak. Jeśli zakres (Zadanie 4) definiuje, _co_ jest na stole, a dokumenty prawne (Zadanie 5) ustanawiają _upoważnienie_ do udziału w stole, to RoE definiuje, _jak należy się zachowywać_ przy stole.

Spójrzmy na to z perspektywy zaangażowania BrightCart. Zakres zakłada, że ​​zespół testujący może ocenić BrightCart.thm,API.brightcart.thm iAWSŚrodowisko us-east-1. Dokumenty prawne upoważniają do zaangażowania i chronią obie strony. Jednak sam zakres i umowy nie dają odpowiedzi na pytania takie jak: Czy testerzy mogą przeprowadzać skanowanie w godzinach pracy? Do kogo mają się zwrócić, jeśli przypadkowo wyłączą API płatności? Co się stanie, jeśli znajdą dane uwierzytelniające dyrektora finansowego w pliku tekstowym? RoE odpowiada na wszystkie te pytania.

## Elementy dokumentu zasad zaangażowania

RoE obejmuje kilka obszarów operacyjnych. Przyjrzyjmy się każdemu z nich.

**Czas trwania i czas trwania**

RoE określa datę rozpoczęcia i zakończenia zaangażowania, a także wszelkie ograniczenia czasowe dotyczące działań testowych. Ma to znaczenie, ponieważ niektóre działania testowe, zwłaszcza agresywne skanowanie lub próby wykorzystania luk w zabezpieczeniach, mogą obniżyć wydajność systemu lub wywołać alerty zakłócające jego działanie.

Rozważmy sytuację BrightCart. Ich szczytowy ruch przypada na wieczory robocze między 18:00 a 22:00, a przetwarzanie płatności wsadowych odbywa się każdej nocy o 2:00 w nocy. RoE może określać, że aktywne testy w zakresie eksploatacji są dozwolone tylko między 22:00 a 1:30 w nocy w dni robocze oraz swobodnie w weekendy, podczas gdy pasywne rozpoznanie i analiza mogą być przeprowadzane o dowolnej porze. Dokładne przedziały czasowe zależą od potrzeb operacyjnych klienta, a ich błędne ustalenie może zadecydować o tym, czy uda się sprawnie przeprowadzić interakcję, czy też otrzymać telefon od zespołu operacyjnego z pretensjami.

**Protokoły komunikacyjne**

To nie jest o tymTCP/IP lub protokoły sieciowe; chodzi o sposób, w jaki organizacja klienta i zespół testów penetracyjnych komunikują się w trakcie realizacji zlecenia.

Sekcja komunikacji w RoE wskazuje **punkty kontaktowe** po obu stronach, określa **kanały komunikacji** dla różnych typów wiadomości oraz definiuje kanał komunikacji pilnej. Rozważmy poniższą macierz kontaktów dla zaangażowania BrightCart:

|Rola|Nazwa|Kanał|Przypadek użycia|
|---|---|---|---|
|Główny kontakt klienta|Dyrektor ds. bezpieczeństwa informacji (CISO), BrightCart|Zaszyfrowana poczta e-mail|Codzienne aktualizacje statusu, pytania niepilne|
|Kontakt alarmowy klienta|Wiceprezes ds. inżynierii, BrightCart|Telefon komórkowy (bezpośredni)|Awarie systemu, krytyczne ustalenia|
|Przewód pomiarowy|Główny pentester, firma testująca|Zaszyfrowana poczta e-mail|Codzienne aktualizacje statusu, wyjaśnienia zakresu|
|Testowanie awaryjne|Testowanie operacji firmy|Całodobowa infolinia|Prośby o wstrzymanie działalności, koordynacja incydentów|

Dlaczego ma to znaczenie w praktyce? Rozważmy dwa scenariusze. W pierwszym zespół operacyjny BrightCart zauważa, że ​​interfejs API płatności nie odpowiada o 23:30. Czy jest to wynik testu penetracyjnego, czy też niezwiązana z nim awaria infrastruktury? Bez wyraźnego kanału komunikacji zespół operacyjny nie ma możliwości szybkiego potwierdzenia, czy to testerzy spowodowali problem. W drugim, testerzy penetracyjni odkrywają, że nieuwierzytelniony punkt końcowy interfejsu API ujawnia numery kart kredytowych klientów w czasie rzeczywistym. To kluczowe odkrycie, które nie może czekać na raport końcowy; klient musi dowiedzieć się o tym _natychmiast_ , aby móc działać.

Tutaj właśnie pojawiają się **procedury eskalacji** . RoE powinien określać proces zgłaszania krytycznych incydentów i krytycznych ustaleń w trakcie zaangażowania. Typowa struktura obejmuje trzy poziomy:

1. **Informacyjne** : Rutynowe aktualizacje statusu dostarczane za pośrednictwem uzgodnionego kanału i z uzgodnioną częstotliwością (np. codzienne podsumowania e-mailem)
2. **Pilne** : ustalenia lub incydenty wymagające uwagi klienta w ciągu kilku godzin (np. poważna luka w zabezpieczeniach systemu produkcyjnego), przekazywane bezpośrednio pocztą elektroniczną lub wiadomością do osoby kontaktowej.
3. **Krytyczne** : ustalenia lub incydenty stanowiące bezpośrednie ryzyko, takie jak aktywne ujawnienie danych, dowody rzeczywistego naruszenia lub niezamierzone zakłócenie działania systemu, przekazywane telefonicznie do osoby kontaktowej w nagłych wypadkach

Wreszcie, aby uniknąć nieporozumień, RoE powinno określić na piśmie **częstotliwość i format raportowania** . Czy testerzy będą dostarczać codzienne aktualizacje statusu? Cotygodniowe podsumowania? Czy raport końcowy jest wymagany pięć, czy dziesięć dni roboczych po zakończeniu testów? Obie strony powinny dokładnie wiedzieć, czego się spodziewać i kiedy.

**Poufność i przetwarzanie danych**

Podczas testu penetracyjnego ujawniona zostanie znaczna ilość poufnych informacji o organizacji klienta, jej pracownikach i użytkownikach. Niezależnie od rodzaju organizacji, od placówki opieki zdrowotnej po firmę e-commerce, dane te muszą być traktowane z zachowaniem ścisłej poufności. Jako tester penetracyjny nie chcesz, aby prywatne informacje Twojego klienta wyciekły z powodu niewłaściwego obchodzenia się z jego danymi; poza obowiązkiem etycznym, niewłaściwe obchodzenie się z danymi może narazić Cię na odpowiedzialność prawną na mocy przepisów takich jak:RODOLubHIPAA.

Zastanów się, na co może natknąć się tester podczas zaangażowania. Co się stanie, jeśli odkryjesz sekretny przepis na sos restauracji klienta, zapisany w niezabezpieczonym pliku? Co się stanie, jeśli znajdziesz hasło prezesa w pliku konfiguracyjnym i będzie to to samo hasło, którego używa on do swoich prywatnych kont w mediach społecznościowych? Co się stanie, jeśli uzyskasz dostęp do bazy danych zawierającej dane o wynagrodzeniach pracowników lub dane dotyczące zdrowia klientów? To nie są hipotetyczne sytuacje; zdarzają się w rzeczywistych zaangażowaniach.

RoE powinno ustanowić jasne, udokumentowane zasady postępowania z takimi odkryciami:

- **Minimalizacja danych** : Testerzy powinni gromadzić wyłącznie dowody niezbędne do wykazania luki w zabezpieczeniach, a nie eksfiltrować całych baz danych
- **Szyfrowanie** : Wszystkie zebrane dowody powinny być szyfrowaneodpoczynek(AES-256 lub równoważny) i w tranzycie
- **Przechowywanie i niszczenie** : RoE powinno określać, jak długo firma testująca przechowuje dane z projektu po dostarczeniu raportu oraz w jaki sposób te dane są niszczone. Powszechnym standardem jest okres od 30 do 90 dni, po którym wszystkie dowody są bezpiecznie usuwane.
- **Kanały zgłaszania** : Powinien istnieć udokumentowany, uzgodniony proces zgłaszania poufnych ustaleń, określający, kto otrzymuje informacje i w jaki sposób są one przekazywane.

**Dozwolone i zabronione działania**

RoE powinien wyraźnie określać, które techniki i narzędzia testowe są dozwolone, a które nie. Lista zabronionych działań różni się w zależności od rodzaju zlecenia, ale typowe ograniczenia obejmują:

- **Odmowa usługi (DoS) ataki** na systemy produkcyjne
- **Inżynieria społeczna**pracowników (chyba że wyraźnie zezwolono na to jako osobne zaangażowanie)
- **Testowanie bezpieczeństwa fizycznego** (ponownie, chyba że określono zakres i autoryzację oddzielnie)
- **Wykorzystanie luk w zabezpieczeniach, które mogą spowodować utratę danych** lub trwałe uszkodzenie systemów produkcyjnych
- **Korzystanie z niezatwierdzonych narzędzi** , które mogą pozostawiać trwałe artefakty lub tylne furtki

Równie ważne jest określenie, co _jest_ dozwolone. Czy testerzy mogą korzystać ze skanerów automatycznych, takich jakNmapi Nessus? Czy mogą próbować eskalacji uprawnień na zainfekowanych hostach? Czy mogą próbować przejść do sąsiednich systemów w zakresie? Jeśli RoE milczy na temat danej techniki, najbezpieczniej jest założyć, że nie jest ona autoryzowana. Niejednoznaczność w RoE nikomu nie służy.

## Przykładowe podsumowanie ROE

Podsumowując, oto skrócone podsumowanie tego, jak może wyglądać wskaźnik ROE firmy BrightCart:

|Komponent RoE|Szczegół|
|---|---|
|**Okno zaangażowania**|Od 15 marca 2026 r. do 28 marca 2026 r.|
|**Godziny testowania**|Eksploatacja: 22:00 - 1:30 w dni robocze, w weekendy bez ograniczeń. Rozpoznanie pasywne: bez ograniczeń.|
|**Główny kontakt (klient)**|CISO, BrightCart, szyfrowana poczta e-mail|
|**Kontakt alarmowy (klient)**|Wiceprezes ds. inżynierii, telefony komórkowe|
|**Raportowanie statusu**|Codzienne podsumowanie e-mailem do godziny 9:00 rano do głównego kontaktu|
|**Eskalacja ustaleń krytycznych**|Natychmiastowy telefon do osoby kontaktowej w nagłych wypadkach|
|**Dozwolone działania**|Skanowanie portów, skanowanie luk w zabezpieczeniach, eksploatacja, eskalacja uprawnień, ruch boczny w zakresie|
|**Zabronione działania**|DoS/DDoS, inżynieria społeczna, testy fizyczne, eksfiltracja danych poza proof-of-concept|
|**Przetwarzanie danych**|Dowody zaszyfrowane algorytmem AES-256; przechowywane przez 30 dni po zgłoszeniu; bezpieczne usunięcie potwierdzone pisemnie|
|**Termin złożenia raportu końcowego**|10 dni roboczych po zakończeniu testów|

Ta tabela jest uproszczona dla celów ilustracyjnych, ale oddaje istotę struktury. W praktyce dokument RoE dla zaangażowania przedsiębiorstwa może mieć kilka stron.

## Patrząc w przyszłość

W tym zadaniu omówiliśmy główne elementy operacyjne dokumentu „Zasady zaangażowania”. Istnieją dodatkowe kwestie, które pokrywają się z „Zasadami zaangażowania”, ale zasługują na osobne omówienie:

- **Wymagania dotyczące zgodności z przepisami** , które mają wpływ na to, co i jak testujesz (omówione w zadaniu 7)
- **Ramki testów penetracyjnych** zapewniające ustrukturyzowane metodologie przeprowadzania testów (opisane w sali [Ramki testów penetracyjnych](https://tryhackme.com/room/penetrationtestingframeworks) )
- **Przedstaw elementy raportu** i opisz, jak wygląda wynik końcowy (omówiono to w sali poświęconej [pisaniu raportów z testów penetracyjnych](https://tryhackme.com/room/writingpentestreports) )

BrightCart przetwarza płatności kartami kredytowymi. Ten pojedynczy fakt pociąga za sobą lawinę obowiązków regulacyjnych. Ponieważ BrightCart przetwarza dane posiadaczy kart, musi przestrzegać standardów bezpieczeństwa danych branży kart płatniczych (Payment Card Industry Data Security Standard – PIC).PCI DSS), które ma określone, niepodlegające negocjacjom wymagania dotyczące testów penetracyjnych. Jeśli BrightCart obsługuje również klientów w Unii Europejskiej, obowiązuje ogólne rozporządzenie o ochronie danych (RODO).RODO) dodaje kolejny poziom obowiązków związanych z bezpieczeństwem danych i prywatnością. A jeśli partner BrightCart z branży opieki zdrowotnej udostępnia dane pacjentów poprzez integrację, ustawa o przenoszalności i odpowiedzialności w ubezpieczeniach zdrowotnych (Health Insurance Portability and Accountability Act)HIPAA) ma również zastosowanie.

Chodzi o to, że testy penetracyjne nie zawsze są decyzją uznaniową. W wielu branżach _wymagają_ tego przepisy. Jako tester penetracyjny, zrozumienie ram zgodności obowiązujących u klienta pomaga Ci zaprojektować projekt, który spełnia zarówno cele klienta w zakresie bezpieczeństwa, jak i jego obowiązki regulacyjne. Jako klient, zrozumienie tych wymagań pomaga Ci upewnić się, że zlecony test penetracyjny rzeczywiście przejdzie audyt.

## PCI DSS

Standard **bezpieczeństwa danych branży kart płatniczych (PCI DSS)** to najbardziej rygorystyczny system zgodności dla wymagań testów penetracyjnych. Każda organizacja, która przechowuje, przetwarza lub przesyła dane posiadaczy kart, musi przestrzegać PCI DSS. Aktualna wersja to **PCI DSS v4.0.1** , która stała się jedyną aktywną wersją 31 grudnia 2024 r. Wszystkie przyszłe wymagania stały się obowiązkowe 31 marca 2025 r.

Wymagania dotyczące testów penetracyjnych są zawarte w **Wymaganiu 11.4** , które nakazuje:

- **Testy penetracyjne wewnętrzne i zewnętrzne** należy przeprowadzać co najmniej raz na 12 miesięcy oraz po każdej istotnej zmianie infrastruktury lub aplikacji.
- Metodologia testowania musi opierać się na **podejściu akceptowanym w branży** , takim jak:NISTSP 800-115, PTES, OSSTMM lubOWASP.
- Testy muszą obejmować **całe środowisko danych posiadacza karty (CDE)** i wszelkie systemy z nim połączone.
- Należy ocenić zarówno luki w zabezpieczeniach **na poziomie aplikacji** (takie jak te wymienione w raporcie OWASP Top 10), jak i luki w zabezpieczeniach **na poziomie sieci .**
- Wszystkie odkryte luki w zabezpieczeniach i podatne na wykorzystanie luki muszą zostać **naprawione i ponownie przetestowane,** aby potwierdzić skuteczność poprawki.

Warto podkreślić ten ostatni punkt. PCI DSS wymaga nie tylko znalezienia luk w zabezpieczeniach, ale także udowodnienia, że ​​zostały one naprawione. Praca testera penetracyjnego nie kończy się wraz z dostarczeniem raportu. Ponowny test potwierdzający naprawę jest częścią cyklu zgodności.

Dla BrightCart oznacza to, że test penetracyjny, który przeprowadzamy w tym pomieszczeniu, musi obejmować wszystkie systemy, które mają kontakt z danymi posiadaczy kart, wykorzystywać uznaną metodologię i obejmować fazę weryfikacji działań naprawczych. Dokument zakresu z zadania 4 iIkraz Zadania 6 powinny odzwierciedlać te wymagania.

## HIPAA

Ustawa **o przenoszalności i odpowiedzialności w ubezpieczeniach zdrowotnych (HIPAA)** reguluje ochronę danych pacjentów w Stanach Zjednoczonych. W przeciwieństwie do PCI DSS, HIPAA historycznie _nie_ wymagała wprost testów penetracyjnych. Najbliższym przepisem jest standard oceny zasad bezpieczeństwa (§ 164.308(a)(8)), który wymaga „okresowych technicznych i nietechnicznych ocen” zabezpieczeń, ale nie określa szczegółowo testów penetracyjnych.

Mimo to, testy penetracyjne są powszechnie uważane za najlepszą praktykę w zakresie zgodności z ustawą HIPAA i wielu audytorów spodziewa się dowodów na ich istnienie. Sytuacja może się jeszcze bardziej zmienić: w grudniu 2024 r. Departament Zdrowia i Opieki Społecznej Stanów Zjednoczonych (HHS) opublikował zawiadomienie **o proponowanym procesie legislacyjnym** , które, jeśli zostanie sfinalizowane, będzie wymagało przeprowadzania testów penetracyjnych co najmniej co 12 miesięcy dla wszystkich objętych przepisami podmiotów i partnerów biznesowych. Proponowane przepisy będą również wymagały skanowania podatności co sześć miesięcy.

Dla testera penetracyjnego kluczowym aspektem HIPAA jest przetwarzanie danych. Jeśli podczas realizacji zlecenia natrafisz na **elektroniczne chronione informacje zdrowotne (ePHI)** , dane te podlegają zasadom prywatności i bezpieczeństwa HIPAA. Procedury przetwarzania danych określone w RoE (Zadanie 6) muszą to uwzględniać: minimalizuj ilość gromadzonych danych, szyfruj je w trakcie transmisji i w dowolnym momencie.odpoczyneki zniszczyć je zgodnie z ustalonym harmonogramem.

## RODO

Rozporządzenie **Ogólne o Ochronie Danych (RODO)** ma zastosowanie do każdej organizacji przetwarzającej dane osobowe osób fizycznych w Unii Europejskiej, niezależnie od jej siedziby. BrightCart wysyła produkty do klientów z UE, dlatego RODO ma zastosowanie.

RODO nie wymienia z nazwy testów penetracyjnych. **Artykuł 32(1)(d)** nakłada jednak na organizacje obowiązek wdrożenia „procesu regularnego testowania, oceniania i ewaluacji skuteczności środków technicznych i organizacyjnych zapewniających bezpieczeństwo przetwarzania”. Brytyjskie Biuro Komisarza ds. Informacji (ICO) jednoznacznie zinterpretowało ten przepis jako zalecaną praktykę w zakresie testów penetracyjnych.

Dla testerów penetracyjnych RODO wprowadza szczególną komplikację: jeśli uzyskasz dostęp do danych osobowych w trakcie realizacji zlecenia, stajesz się **podmiotem przetwarzającym dane** w rozumieniu RODO. Nakłada to na Ciebie szereg obowiązków:

- Przed rozpoczęciem testów tester i klient muszą podpisać umowę **o przetwarzaniu danych (DPA)**
- **Obowiązuje minimalizacja danych** ; należy zbierać tylko dowody niezbędne do wykazania luki w zabezpieczeniach, a nie całe zestawy danych
- Dane osobowe zebrane podczas testów muszą być traktowane z zachowaniem tych samych zabezpieczeń, jakie są wymagane na mocy rozporządzenia
- Kary za nieprzestrzeganie przepisów mogą sięgać nawet **20 milionów euro lub 4% rocznego globalnego obrotu** , w zależności od tego, która kwota jest wyższa

W praktyce oznacza to, żeNDAa sekcje dokumentacji przed podjęciem współpracy poświęcone przetwarzaniu danych (zadania 5 i 6) muszą wyraźnie określać obowiązki wynikające z RODO, w przypadku gdy systemy klienta zawierają dane osobowe UE.

## SOC2 i ISO 27001

Warto zwrócić uwagę na dwa dodatkowe modele, choć opierają się one na łagodniejszym podejściu do wymagań dotyczących testów penetracyjnych.

**SOC 2** (Service Organization Control 2) to struktura audytu opracowana przez Amerykański Instytut Biegłych Rewidentów (AICPA). Ocenia ona mechanizmy kontroli organizacji w oparciu o pięć kryteriów usług zaufania: bezpieczeństwo, dostępność i przetwarzanie.uczciwość, poufności i prywatności. Norma SOC 2 nie nakłada wprost obowiązku przeprowadzania testów penetracyjnych, ale jej wytyczne dotyczące kryterium usług zaufania CC4.1 wspominają o testach penetracyjnych jako metodzie oceny. W praktyce audytorzy rutynowo oczekują, że wyniki testów penetracyjnych będą stanowić dowód, a klienci przeglądający raporty SOC 2 często tego wymagają.

**ISO 27001:2022** to międzynarodowa norma dotycząca systemów zarządzania bezpieczeństwem informacji (SZBI). Podobnie, nie nakłada ona wprost obowiązku przeprowadzania testów penetracyjnych, ale kontrole A.8.8 (Zarządzanie lukami technicznymi) i A.8.29 (Testowanie bezpieczeństwa w fazie rozwoju i akceptacji) są najskuteczniej realizowane poprzez testy penetracyjne. Wiele organizacji ubiegających się o certyfikat ISO 27001 uwzględnia coroczne testy penetracyjne w ramach wdrażania kontroli.

Schemat jest wyraźny: nawet tam, gdzie testy penetracyjne nie są wyraźnie wymagane, coraz częściej _oczekuje się_ ich jako dowodu należytej staranności. Organizacja, która rezygnuje z testów penetracyjnych, będzie musiała stawić czoła trudniejszym pytaniom ze strony audytorów, klientów i organów regulacyjnych niż ta, która regularnie przeprowadza i dokumentuje testy.

## Streszczenie

Poniższa tabela zawiera krótki przegląd tego, w jaki sposób poszczególne ramy obsługują testy penetracyjne:

| Struktura      | Czy test penetracyjny jest wyraźnie wymagany?               | Kluczowe postanowienie      | Częstotliwość                   |
| -------------- | ----------------------------------------------------------- | --------------------------- | ------------------------------- |
| PCI DSS v4.0.1 | Tak                                                         | Wymaganie 11.4              | Rocznie + po istotnych zmianach |
| HIPAA          | Obecnie nie (propozycja przepisu w toku)                    | § 164.308(a)(8) Norma oceny | Proponowane: corocznie          |
| RODO           | Nie (zdecydowanie zalecane)                                 | Artykuł 32(1)(d)            | Nie określono                   |
| SOC 2          | Nie (oczekiwane rutynowo)                                   | Wytyczne CC4.1              | Zwykle corocznie                |
| ISO 27001:2022 | Nie (wymagane w przypadku kluczowych elementów sterujących) | A.8.8, A.8.29               | Zwykle corocznie                |

W ciągu ostatnich siedmiu zadań dowiedziałeś się, czym są testy penetracyjne, czym różnią się rodzaje i podejścia do testowania, jak zdefiniować zakres, jakie podstawy prawne muszą być spełnione, jak zasady zaangażowania regulują testowanie oraz jakie ramy regulacyjne określają wymagania dotyczące testowania. Teraz nadszedł czas, aby to wszystko wdrożyć.

W tym zadaniu wcielisz się w rolę konsultanta ds. testów penetracyjnych. BrightCart, firma e-commerce, którą śledziliśmy w tym pomieszczeniu, przesłała Ci wstępne zapytanie. Przeczytaj uważnie poniższy opis, a następnie odpowiedz na pytania. Każde pytanie wymaga od Ciebie wykorzystania koncepcji z wielu poprzednich zadań; nie ma tu odpowiedzi na jedno pytanie.

## Krótki opis klienta

Otrzymasz następującą wiadomość e-mail od CISO firmy BrightCart:

> **Od:** Sarah Chen, CISO, BrightCart
> 
> **Do:** Ciebie (Tester penetracyjny)
> 
> **Temat:** Zaangażowanie w testy penetracyjne – wstępny zakres
> 
> Cześć,
> 
> Dziękujemy za spotkanie w zeszłym tygodniu. Jak już wspomnieliśmy, BrightCart prosi o zlecenie testów penetracyjnych w celu oceny bezpieczeństwa naszych systemów bazowych przed naszym corocznym PCI DSS audyt w czerwcu.
> 
> Poniżej znajduje się podsumowanie naszego środowiska i wymagań:
> 
> **O BrightCart:**
> 
> Jesteśmy średniej wielkości firmą e-commerce z siedzibą główną w Stanach Zjednoczonych i rosnącą bazą klientów w Unii Europejskiej. Miesięcznie przetwarzamy około 50 000 transakcji kartą kredytową za pośrednictwem naszej aplikacji internetowej.
> 
> **Systemy i infrastruktura:**
> 
> - Aplikacja internetowa skierowana do klientów: www.brightcart.thm
> - ODPOCZYNEK API do przetwarzania płatności: api.brightcart.thm
> - Wewnętrzny portal pracowniczy: internal.brightcart.thm (dostępny tylko z sieci korporacyjnej)
> - Aplikacja mobilna (iOS i Android) komunikująca się z API REST
> - Infrastruktura chmurowa hostowana naAWS(region us-east-1, środowisko produkcyjne)
> - Sieć Wi-Fi korporacyjna w siedzibie głównej
> - Platforma logistyczna stron trzecich obsługiwana przez ShipFast Inc. (zintegrowana za pomocą API)
> 
> **Co chcemy przetestować:**
> 
> Chcemy jak najdokładniejszej oceny naszej aplikacji internetowej, interfejsu API płatności i infrastruktury chmurowej. Jesteśmy również zainteresowani przetestowaniem sieci wewnętrznej, aby ocenić, do jakich danych mógłby uzyskać dostęp atak z wewnątrz. Zarząd zwrócił się z pytaniem, czy atakujący mógłby uzyskać dostęp do naszej bazy danych płatności z sieci korporacyjnej.
> 
> **Co jest poza zasięgiem:**
> 
> - Platforma logistyczna ShipFast (nie jesteśmy jej właścicielami i nie możemy autoryzować testów)
> - Nasze środowisko odzyskiwania po awarii w AWS eu-west-1 (aktualnie zamrożone zmiany)
> - Wszelkie formy testowania pod kątem odmowy usługi (nasz zespół operacyjny jest w tej kwestii stanowczy)
> 
> **Ograniczenia:**
> 
> - Testowanie nie może zakłócać działalności w godzinach szczytu (wieczorami w dni robocze, od 18:00 do 22:00 czasu wschodniego)
> - Codziennie o 2:00 czasu wschodniego uruchamiamy zadanie przetwarzania płatności wsadowych, którego nie wolno przerywać
> - Potrzebujemy raportu końcowego co najmniej trzy tygodnie przed audytem PCI DSS, który jest zaplanowany na 15 czerwca 2026 r.
> 
> **Co możemy zapewnić:**
> 
> Jesteśmy gotowi udostępnić diagramy sieci, dokumentację architektury aplikacji, szczegóły konfiguracji AWS oraz zestaw testowych kont użytkowników o różnych poziomach uprawnień dla aplikacji webowej. Chcemy, aby testerzy mieli wszelkie atuty, abyśmy mogli wykryć jak najwięcej problemów.
> 
> **Dodatkowe uwagi:**
> 
> - Nasz zespół prawny będzie wymagałNDAzanim udostępnimy jakąkolwiek dokumentację techniczną
> - Już mamyMSAna miejscu z Twoją firmą z poprzedniegoocena podatności
> - Chcielibyśmy mieć dla Ciebie jeden punkt kontaktowy, z którym będziesz mógł codziennie otrzymywać aktualizacje statusu
> - W przypadku krytycznych ustaleń potrzebujemy natychmiastowego powiadomienia — należy skontaktować się bezpośrednio z naszym wiceprezesem ds. inżynierii
> 
> Prosimy o zapoznanie się z proponowanym podejściem, harmonogramem i przesłanie nam wszelkich pytań.
> 
> Z wyrazami szacunku,
> 
> Sarah Chen
> 
> Dyrektor ds. bezpieczeństwa informacji, BrightCart

## Analiza

Omówmy szczegółowo to streszczenie, korzystając z ram, które zbudowaliśmy w tym pomieszczeniu.

**Podejście testowe**

W e-mailu Sarah czytamy, że BrightCart jest gotowy udostępnić schematy sieci, dokumentację architektury, szczegóły konfiguracji AWS oraz konta testowe o różnych poziomach uprawnień. CISO wyraźnie chce, aby testerzy „mieli wszelkie atuty”, aby zmaksymalizować wykrywanie luk w zabezpieczeniach. Jest to bezpośrednio powiązane z podejściem **znanego środowiska** (białej skrzynki), o którym mówiliśmy w Zadaniu 3. Testerzy będą dysponować kompleksową wiedzą na temat środowiska docelowego przed rozpoczęciem testów.

**Zakres**

Korzystając z kategorii z Zadania 4, możemy zmapować brief BrightCart na definicję zakresu, określając, co jest uważane za „w zakresie”, a co za „poza zakresem”.

Należy pamiętać, że platforma logistyczna ShipFast nie jest objęta zakresem, ponieważ BrightCart nie jest jej właścicielem i _nie może autoryzować_ testów na niej. Jak omówiliśmy w zadaniu 5, list autoryzacyjny musi zostać podpisany przez osobę posiadającą uprawnienia prawne do testowanych zasobów. BrightCart nie ma takich uprawnień w odniesieniu do systemów ShipFast.

**Typ testu**

W ramach tego zadania łączone są różne typy testów z Zadania 3:

- **Test penetracyjny aplikacji internetowych** dla www.brightcart.thm i internal.brightcart.thm
- **Test penetracji sieci** obejmujący zarówno perspektywę zewnętrzną (zwróconą do Internetu), jak i wewnętrzną (sieć korporacyjna)
- **Test penetracji chmury** dla środowiska AWS us-east-1
- **Test penetracyjny aplikacji mobilnych** dla systemów iOS i Android

Konkretne pytanie zarządu, czy atakujący może uzyskać dostęp do bazy danych płatności z sieci korporacyjnej, wymaga przeprowadzenia **wewnętrznego testu penetracyjnego,** skupiającego się na przemieszczaniu się bocznym i eskalacji uprawnień.

**Dokumenty prawne**

E-mail Sary informuje nas o statusie prawnym dokumentu:

- **NDA** : Jeszcze nie podpisane. Zespół prawny BrightCart wymaga tego przed udostępnieniem dokumentacji technicznej. Umowa musi zostać podpisana w pierwszej kolejności.
- **MSA** : Umowa została już wdrożona w wyniku poprzedniej oceny podatności. Nie ma potrzeby przeprowadzania nowych negocjacji.
- **SIAĆ**:Sporządzono na potrzeby tego konkretnego zlecenia, definiując zakres, metodologię, harmonogram, produkty dostarczane i koszty.
- **List autoryzacyjny** : Nieobecny w e-mailu, ale wymagany przed rozpoczęciem testów. Musi być podpisany przez osobę posiadającą uprawnienia do wszystkich zasobów objętych zakresem.

**Zasady zaangażowania**

Na podstawie ograniczeń zawartych w streszczeniu Sary możemy opracować kluczIkraskładniki:

- **Okno testowe** : Unikaj wieczorów w dni powszednie (18:00–22:00 czasu wschodniego) i nocnego zadania wsadowego o godzinie 2:00 czasu wschodniego
- **Zabronione działania** :DoS/DDoStestowanie (wyraźnie zabronione przez klienta)
- **Komunikacja** : codzienne aktualizacje statusu przekazywane pojedynczemu punktowi kontaktowemu; krytyczne ustalenia przekazywane natychmiast za pośrednictwem połączenia telefonicznego do wiceprezesa ds. inżynierii
- **Termin składania raportu** : co najmniej trzy tygodnie przed 15 czerwca 2026 r., co oznacza, że ​​raport końcowy musi zostać dostarczony najpóźniej do 25 maja 2026 r.

**Zgodność z przepisami**

W przypadku BrightCart obowiązują dwa modele zgodności (omówione w Zadaniu 7):

- **PCI DSS v4.0.1** : BrightCart przetwarza transakcje kartami kredytowymi i jest objęty planowanym audytem PCI DSS. Test penetracyjny musi obejmować całe środowisko danych posiadacza karty (CDE), wykorzystywać metodologię akceptowaną w branży i obejmować ponowne testy naprawcze.
- **RODO**:BrightCart obsługuje klientów z UE, co oznacza, że ​​wszelkie dane osobowe pozyskane podczas testów podlegają obowiązkom podmiotu przetwarzającego dane, w tym minimalizacji danych, szyfrowaniu i umowie o przetwarzaniu danych.

Prześledźmy tę podróż. Na początku tego spotkania zarząd BrightCart zadawał proste pytanie: „Czy może nam się przydarzyć naruszenie danych?”. Pod koniec zadania 8 przełożyłeś to pytanie na w pełni zakresowe testy penetracyjne, wraz ze zdefiniowanym podejściem testowym, dokumentem zakresu, umowami prawnymi, zasadami zaangażowania i zgodnością z przepisami. Nie uruchomiono żadnego skanera. Nie uruchomiono żadnego exploita. A jednak praca, którą wykonałeś w ramach tych ośmiu zadań, jest tym, co umożliwia _wszystko, co następuje_ .

To jest główna lekcja płynąca z tej sali: **faza planowania i określania zakresu to moment, w którym testy penetracyjne kończą się sukcesem lub porażką.** Źle określony zakres projektu to strata czasu i pieniędzy. Brak listu autoryzacyjnego może zakończyć karierę.IkraBrak procedur eskalacji naraża obie strony na ryzyko w przypadku problemów. Umiejętności techniczne, które zdobędziesz w trakcie tej ścieżki edukacyjnej, są potężne, ale ich skuteczność zależy od planowania, które nimi kieruje.

## Co omówiliśmy

Poniżej znajduje się podsumowanie materiału, który omówiliśmy, na podstawie celów edukacyjnych z Zadania 1:

**Wyjaśnij, czym jest test penetracyjny i czym różni się od testu penetracyjnego.ocena podatności**(Zadanie 2). Test penetracyjny to autoryzowany, symulowany atak cybernetyczny mający na celu identyfikację i wykorzystanie luk w zabezpieczeniach. W przeciwieństwie do oceny podatności, która jest szeroka i zautomatyzowana, test penetracyjny jest dogłębny, manualny i demonstruje rzeczywisty wpływ poprzez aktywną eksploatację.

**Rozróżnij podejścia do środowiska znanego, częściowo znanego i nieznanego** (Zadanie 3). Te trzy podejścia definiują ilość informacji, jakie tester otrzymuje przed rozpoczęciem testu. Branża odchodzi od starszej terminologii białej/szarej/czarnej skrzynki na rzecz etykiet środowiska opartego na wiedzy, ale oba te zestawy pozostają w aktywnym użyciu.

**Zdefiniuj zakres testu penetracyjnego i zidentyfikuj ryzyko błędów w jego określaniu** (Zadanie 4). Zakres definiuje granice zaangażowania poprzez wyraźne listy dozwolonych i zablokowanych uprawnień. Zbyt szeroki zakres prowadzi do płytkich testów; zbyt wąski zakres tworzy niebezpieczne martwe pola i potencjalne błędy w przestrzeganiu przepisów.

**Określ dokumenty prawne i zezwolenia wymagane przed rozpoczęciem testów** (zadanie 5). Cztery podstawowe dokumenty regulują zaangażowanie zawodowe:NDA,MSA,SIAĆoraz list autoryzacyjny. Ustawa CFAA (Stany Zjednoczone) i ustawa Computer Misuse Act (Wielka Brytania) uznają nieautoryzowany dostęp za przestępstwo; pisemne upoważnienie jest warunkiem, aby test penetracyjny był zgodny z prawem.

**Opisz kluczowe elementy dokumentu „Zasady zaangażowania”** (Zadanie 6). Zasady zaangażowania (RoE) określają granice operacyjne zaangażowania: czas i czas trwania, protokoły komunikacyjne, procedury eskalacji, wymogi dotyczące poufności i przetwarzania danych oraz działania dozwolone i zabronione.

**Rozpoznaj główne ramy regulacyjne, które nakazują lub zalecają przeprowadzanie testów penetracyjnych** (zadanie 7).PCI DSSWersja 4.0.1 wyraźnie wymaga corocznych testów penetracyjnych środowiska danych posiadacza karty.HIPAA,RODO,SOCNormy ISO 27001 i ISO 27001 regulują kwestie testów penetracyjnych z różnym stopniem szczegółowości, lecz branża zmierza w kierunku przyjęcia uniwersalnego oczekiwania w tym zakresie.

**Zastosuj koncepcje planowania i określania zakresu do realistycznego scenariusza klienta** (Zadanie 8). Ćwiczenie angażujące BrightCart obejmowało wszystkie koncepcje: przełożenie wiadomości e-mail od klienta na podejście testowe, dokument dotyczący zakresu, listę kontrolną dokumentów prawnych, ramy RoE oraz mapowanie zgodności.
