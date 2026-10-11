---

Sztuczna inteligencja Agenci potrafią analizować informacje, korzystać z narzędzi, wyszukiwać wiedzę i wykonywać wieloetapowe zadania. Te możliwości sprawiają, że są przydatni w rozwiązywaniu niektórych problemów, ale nie każde trudne lub powtarzalne zadanie wymaga zaangażowania agenta.

Udany projekt agenta rozpoczyna się przed wyborem modelu, struktury lub narzędzia. Zespół musi najpierw zrozumieć pracę, osoby, których ona dotyczy, oraz rezultat, jakiego potrzebuje organizacja.

W tym pokoju wcielisz się w rolę inżyniera agenta AI, którego zatrudniono do pomocy firmie NorthStar Fashion. Firma rozważa zatrudnienie agenta AI do pomocy w dochodzeniach dotyczących alertów bezpieczeństwa. Twoim obowiązkiem jest przeanalizowanie pomysłu i określenie, jakie rozwiązanie, jeśli w ogóle, jest odpowiednie.

Nie będziesz budować systemu w tym pomieszczeniu. Polecisz jedną z pięciu praktycznych ścieżek:

- Zbuduj tradycyjny lub zautomatyzowany przepływ pracy.
- Zbuduj przepływ pracy AI.
- Zbuduj asystenta AI.
- Zbuduj agenta AI.
- Nie buduj nowego systemu.

## Cele edukacyjne

Na koniec zajęć Twoja ukończona praca badawcza będzie obejmować:

- Dowiedz się, dlaczego identyfikacja agentów jest konieczna.
- Zdefiniuj problem biznesowy firmy NorthStar Fashion.
- Zaplanuj obecny obieg prac nad alertami i dochodzeniami.
- Podziel przepływ pracy na poszczególne zadania i decyzje.
- Określ, które zadania pasują do tradycyjnego przepływu pracy, a które korzystają zMagister prawa-system oparty na
- Rozróżnij przepływ pracy AI, asystenta AI i agenta AI w zależności od tego, kto kontroluje następny krok.
- Określ, co proponowany system może i czego nie może zrobić.
- Przedstaw ostateczną rekomendację w celu rozwiązania problemu NorthStar.

## Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś zapoznać się z następującymi informacjami:

- Wymagana jest podstawowa znajomość koncepcji sztucznej inteligencji (AI) i uczenia maszynowego, ale nie jest wymagane żadne doświadczenie w budowaniu agentów AI ani korzystaniu z frameworków agentów ( sala [„The Building Blocks of AI” ).](https://tryhackme.com/room/aimlsecuritythreats)
- Podstawowa znajomość SIEM koncepcje i analiza alertów, ponieważ w pomieszczeniu wykorzystywany jest scenariusz badania alertów bezpieczeństwa ( [Wprowadzenie do](https://tryhackme.com/room/introtosiem) pomieszczenia SIEM)
- Ogólna wiedza na temat zasad bezpieczeństwa, w tym dlaczego działania o dużym wpływie wymagają wyraźnego upoważnienia i nadzoru człowieka ( sala poświęcona [zasadom bezpieczeństwa](https://tryhackme.com/room/securityprinciples) )

## Scenariusz

![Ilustracja małej firmy, w której jeden inżynier zarządza bezpieczeństwem, infrastrukturą i rozwojem, jednocześnie badając około 50 alertów SIEM dziennie. Dowody pochodzą z wielu źródeł, w tym alertów SIEM, reputacji IP, wcześniejszych notatek i powiązanych zdarzeń.](https://cdn-images.tryhackme.com/user-uploads/6a2279941bcbd69b64b598f9/room-content/6a2279941bcbd69b64b598f9-1785420898373.png)

NorthStar Fashion to niewielka internetowa firma odzieżowa, która sprzedaje swoje produkty za pośrednictwem sklepu internetowego. Firma opiera się na niewielkim środowisku technicznym, które obsługuje jej stronę internetową, usługi wewnętrzne, konta pracownicze i operacje związane z obsługą klienta.

NorthStar Fashion nie posiada dedykowanego zespołu ds. bezpieczeństwa. Jeden inżynier odpowiada za bezpieczeństwo, infrastrukturę i kod.

Oprócz konserwacji systemów firmy inżynier codziennie przegląda około 50 alertów bezpieczeństwa w systemie SIEM (Security Information and Event Management).

Pięćdziesiąt alertów dziennie może być do opanowania dla dedykowanego zespołu ds. bezpieczeństwa. Jednak dla jednego inżyniera z kilkoma innymi obowiązkami, ich analiza może pochłaniać znaczną część dnia pracy.

Przypisana waga nie zawsze jest wiarygodna, a znaczenie alertu może ulec zmianie w porównaniu z dowodami zewnętrznymi lub powiązanymi zdarzeniami. Zadanie 4 szczegółowo przeanalizuje te problemy i ich wpływ na działalność biznesową.

Firma NorthStar Fashion rozważa wdrożenie agenta AI, który będzie badał alerty razem z inżynierem. Firma chce ograniczyć ręczne gromadzenie dowodów, aby inżynier mógł skupić się na innych zadaniach.

NorthStar Fashion nie zdecydował jeszcze, co powinien zawierać system ani jak bardzo powinien być autonomiczny. Może on wyglądać następująco:

- Tradycyjny obieg pracy wykorzystujący małe skrypty lub kod.
- Asystent AI odpowiadający na pytania śledcze i przygotowujący podsumowania.
- Przepływ pracy oparty na sztucznej inteligencji, który podąża za ustaloną sekwencją dochodzenia.
- Agent AI korzystający z zatwierdzonych narzędzi i dokumentacji.
- Połączenie tych podejść.

Jeśli agent zostanie ostatecznie wybrany, jego narzędzia muszą dostarczać wiarygodnych informacji zwrotnych o środowisku i musi się zatrzymać, gdy nie będzie miał wystarczającej ilości dowodów. Ludzkie punkty kontrolne i jasne warunki zatrzymania zapobiegają kontynuowaniu otwartego śledztwa bez kontroli.

Proponowany system nie może samodzielnie zamykać alertów, blokować adresów IP, wyłączać kont, zmieniaćzapora sieciowareguły, zmieniać ustawienia poczty e-mail, modyfikować inne zabezpieczenia lub przeprowadzać działania powstrzymujące. Inżynier będzie na bieżąco, zapozna się z dowodami i podejmie ostateczną decyzję dotyczącą bezpieczeństwa.

## Twoja rola

Firma NorthStar Fashion zwróciła się do Państwa z prośbą o pomoc w zaleceniu odpowiedniego rozwiązania. Nie należy zakładać, że agent jest potrzebny tylko dlatego, że firma go zaproponowała. Zamiast tego, przed złożeniem rekomendacji należy przeanalizować problem biznesowy i istniejący proces pracy.

Zadania od 3 do 5 wygenerują problem biznesowy i aktualny przepływ pracy potrzebny do ćwiczenia interaktywnego. W zadaniu 6 sklasyfikujesz zadania przepływu pracy, zdecydujesz, czy wymagają one LLM, rozróżnisz przepływ pracy AI, asystenta AI i agenta AI oraz zdefiniujesz dozwolone i zabronione działania systemu, a następnie przedstawisz ostateczną rekomendację.

Jakość Twojego rozumowania jest ważniejsza niż rekomendowanie agenta. Odkrycie, że tradycyjna automatyzacja, asystent AI lub zmiana procesu są bardziej odpowiednie, jest trafnym wnioskiem.

Odpowiedz na poniższe pytania

Terminy „przepływ pracy”, „asystent” i „agent” są czasami używane zamiennie. W przypadku wyszukiwania informacji bardziej przydatne jest rozróżnienie ich według tego,  **kto kontroluje kolejny krok** i czy…Magister prawajest zaangażowany. Tradycyjny przepływ pracy nie jest systemem opartym na LLM, ponieważ wykorzystuje stały kod i reguły bez LLM.

![Diagram porównujący cztery podejścia do realizacji zadań: tradycyjny przepływ pracy, przepływ pracy AI, asystent AI i agent AI. Porównanie podkreśla, kto kontroluje kolejny krok, pokazując przejście od automatyzacji opartej na stałych regułach do agenta AI, który dynamicznie wybiera narzędzia w ramach zdefiniowanych zabezpieczeń.](https://cdn-images.tryhackme.com/user-uploads/6a2279941bcbd69b64b598f9/room-content/6a2279941bcbd69b64b598f9-1785420820446.png)

### Tradycyjny przepływ pracy

Tradycyjny przepływ pracy wykorzystuje kod, reguły, skrypty lub integracje bez LLM. Deweloper definiuje sekwencję, a te same warunki generują te same działania.

W przypadku NorthStar Fashion tradycyjny przepływ pracy mógł wyodrębnić pola alertów, porównać znaczniki czasu lub zapytać o reputację IPAPIwykorzystując ustaloną logikę. Można to zrobić za pomocą prostego skryptu lub kodu.

### Sztuczna inteligencjaPrzepływ pracy

Przepływ pracy oparty na sztucznej inteligencji (AI) łączy model LLM z narzędziami w ramach predefiniowanej sekwencji kontrolowanej przez kod. Model może interpretować notatki lub przygotowywać podsumowanie, ale to programista decyduje o kolejności kroków oraz warunkach kontynuacji, rozgałęzienia lub zatrzymania.

Na przykład, predefiniowany przepływ pracy mógłby wyodrębnić szczegóły alertów, sprawdzić reputację IP, przeszukać historyczne notatki, a następnie poprosić LLM o wygenerowanie ustrukturyzowanego podsumowania. Każde dochodzenie przebiegałoby zgodnie z tą zaprojektowaną ścieżką.

### Asystent AI

Asystent AI pomaga, odpowiadając na pytania. Inżynier zadaje pytanie lub prosi o podsumowanie, a asystent odpowiada, korzystając z dostępnych informacji. Człowiek decyduje, o co zapytać, co zbadać i czy zaakceptować odpowiedź.

Asystent może jedynie odpowiadać na pytania i czasami korzystać z narzędzi, nie ma jednak pełnej kontroli nad przebiegiem śledztwa.

### Agent AI

Agent AI otrzymuje cel i może dynamicznie decydować o dalszym postępowaniu. Na podstawie otrzymanych danych model może wybrać zatwierdzone narzędzie, kiedy przeszukać dokumentację i wiedzę wewnętrzną, zachować pamięć, zdecydować, czy potrzebne jest kolejne wyszukiwanie, oraz dostosować swój plan.

Agent kontroluje części procesu dochodzeniowego, jednak jego uprawnienia muszą być ograniczone uprawnieniami, punktami kontrolnymi wykonywanymi przez człowieka i warunkami zatrzymania.

|Zbliżać się|Kto kontroluje następny krok?|Czy posiada tytuł LLM?|
|---|---|---|
|Tradycyjny przepływ pracy|Stały kod i zasady|NIE|
|Przepływ pracy AI|Stały kod i zasady|Tak|
|Asystent AI|Inżynier|Tak|
|Agent AI|Model w określonych granicach|Tak|

Asystent AI opisuje interakcję kierowaną przez człowieka, podczas gdy przepływ pracy AI opisuje sposób organizacji wielu kroków. Asystent może korzystać z predefiniowanego przepływu pracy, co pozwala na łączenie tych podejść.

Firma Anthropic opisuje przepływy pracy AI i agentów AI pod szerszym terminem **„systemy agentowe”** , rozróżniając je ze względu na to, kto kontroluje proces. Jej wytyczne inżynierskie zalecają rozpoczęcie od prostych, komponowalnych podejść i dodawanie złożoności tylko wtedy, gdy prowadzi to do znaczącej poprawy. Przepływy pracy AI zapewniają większą spójność dla dobrze zdefiniowanych zadań. Agenci AI są bardziej odpowiedni, gdy wymaganych kroków nie można przewidzieć z wyprzedzeniem, ale mogą zwiększać opóźnienia, koszty i ryzyko kumulacji błędów na różnych etapach. Możesz przeczytać artykuł Anthropic na temat [tworzenia skutecznych agentów.(otwiera się w nowej karcie)](https://www.anthropic.com/engineering/building-effective-agents)aby dowiedzieć się więcej na ten temat.

Wyzwanie związane z dochodzeniem w sprawie alertów NorthStar Fashion ma pięć możliwych ścieżek: tradycyjny przepływ pracy, Sztuczna inteligencja Przepływ pracy, asystent AI, agent AI czy brak nowego systemu? Teraz musisz zbadać, dlaczego odkrycie jest wymagane przed wyborem jednej z tych ścieżek.

Agent AI nie jest celem projektu agenta. Celem jest usprawnienie rzeczywistego przepływu pracy w użyteczny, niezawodny i bezpieczny sposób.

Agenci potrafią interpretować nieustrukturyzowane informacje, korzystać z narzędzi i dostosowywać kolejne kroki w miarę odkrywania nowych dowodów. Te możliwości są cenne, gdy praca wymaga elastyczności, ale wiążą się również z niepewnością, kosztami i ryzykiem operacyjnym.

**Odkrywanie agentów** to proces badawczy przeprowadzany przed podjęciem decyzji o utworzeniu agenta. Pomaga on zespołowi określić, czy możliwości agenta są niezbędne, czy też bardziej odpowiednie będzie prostsze rozwiązanie.

## Zacznij od problemu

![Ilustracja zatytułowana „Wybór właściwego rozwiązania” porównuje cztery podejścia do rozwiązania problemu biznesowego: sterowanie przez człowieka, automatyzacja, wspomaganie AI i kontrolowany agent. Grafika kładzie nacisk na rozpoczęcie od problemu biznesowego, ocenę dostępnych opcji i wybór najprostszego, odpowiedniego rozwiązania, zamiast zakładać, że wymagany jest agent AI. Podpis u dołu brzmi: „Zrozum zadanie. Oceń opcje. Pozostaw kontrolę ludziom”.](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1787951548457.png)Rozważ następujące stwierdzenie: „NorthStar Fashion potrzebuje agenta AI do badania alertów bezpieczeństwa”.

To propozycja rozwiązania, a nie opis problemu. Problem w tym, że nie wyjaśnia, która część dochodzenia jest trudna, jak ta trudność wpływa na firmę ani dlaczego agent miałby ją usprawnić.

Rozpoczęcie pracy od preferowanej technologii może spowodować, że zespół wybierze modele, frameworki i narzędzia, zanim zrozumie specyfikę pracy. Rezultat może być imponujący pod względem technicznym, ale nie rozwiąże rzeczywistego problemu.

Discovery odwraca tę kolejność:

- Zrozum problem biznesowy.
- Sprawdź, w jaki sposób praca jest obecnie wykonywana.
- Określ zadania powtarzalne, trudne, wartościowe i ryzykowne.
- Porównaj pracę ręczną, tradycyjne przepływy pracy, przepływy pracy AI, asystentów AI i agentów AI.
- Zdecyduj, gdzie wymagany jest udział człowieka.
- Poleć najprostsze podejście, które może bezpiecznie przynieść wartość.

W Zadaniu 4 zdefiniujesz problem biznesowy NorthStar Fashion, nie zakładając, że agent jest rozwiązaniem.

## Powtarzalność nie oznacza agencyjności

Praca inżyniera nad dochodzeniem jest powtarzalna, ale sama powtarzalność jest zazwyczaj powodem, aby rozważyć tradycyjny obieg pracy, a niekoniecznie agenta AI.

Niektóre zadania mają ustrukturyzowane dane wejściowe i stabilne reguły. Wyodrębnianie adresu IP, porównywanie identyfikatorów lub porządkowanie zdarzeń według znacznika czasu można zaimplementować jako tradycyjny przepływ pracy. Są to **zadania deterministyczne** : ten sam typ danych wejściowych podlega predefiniowanym regułom, aby uzyskać przewidywalny wynik.

Inne zadania wymagają użycia niestrukturyzowanego języka lub niekompletnych dowodów. Na przykładMagister prawamoże porównać poprzedni zapis incydentu z nowym alertem i wyjaśnić, czy wcześniejsze dochodzenie dostarcza przydatnego kontekstu.

Sposób dostarczania możliwości determinuje typ systemu. Jeśli kod kontroluje predefiniowaną sekwencję, mamy do czynienia z przepływem pracy LLM. Jeśli inżynier zleci wykonanie zadania i zdecyduje, co będzie dalej, jest to asystent AI. Jeśli model wybiera spośród zatwierdzonych kolejnych kroków na podstawie dowodów, jest to agent AI. Wszystkie trzy systemy korzystają z LLM, ale tylko podejście końcowe daje modelowi kontrolę nad ścieżką dochodzenia.

Zachowanie agenta staje się istotne, gdy nie zawsze można z góry wybrać kolejny krok. Na przykład, system może potrzebować wybrać inne zatwierdzone narzędzie dochodzeniowe, ponieważ pierwsze źródło nie dostarczyło wystarczających dowodów.

Discovery oddziela te rodzaje prac zamiast traktować całe śledztwo jako jedno duże zadanie sztucznej inteligencji.

## Porównaj dostępne podejścia

![Ilustracja zatytułowana „Ocena przydatności agenta” przedstawiająca ramy decyzyjne służące do wyboru najodpowiedniejszego rozwiązania dla różnych zadań. Osoba przegląda pulpit nawigacyjny, który ocenia działania takie jak wyszukiwanie źródeł, ocena wiarygodności i porównywanie dowodów pod kątem czynników takich jak przewidywalność, złożoność, ryzyko i niepewność. Na podstawie oceny każde zadanie jest przypisywane do kontrolowanego agenta, asystenta AI lub przeglądu przez człowieka, co podkreśla, że ​​różne części przepływu pracy mogą wymagać różnych poziomów automatyzacji.](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1787951548486.png)Odkrywanie agentów nie polega na wyborze między człowiekiem a w pełni autonomicznym agentem. Przepływ pracy może łączyć kilka podejść.

|Zbliżać się|Nadaje się do|Przykład mody NorthStar|
|---|---|---|
|Praca ręczna|Niejednoznaczne lub obarczone wysokim ryzykiem decyzje wymagające kontekstu i odpowiedzialności|Inżynier podejmuje ostateczną decyzję dotyczącą bezpieczeństwa|
|Tradycyjny przepływ pracy|Przewidywalne zadania ze strukturalnymi danymi wejściowymi i stałymi zasadami|Wyodrębnij pola alertów lub, jeśli dostęp jest możliwy, zapytaj o zatwierdzoneAPI|
|Przepływ pracy AI|Praca wieloetapowa, która przebiega według stabilnej sekwencji kontrolowanej przez kod|Zbierz zatwierdzone dowody i wygeneruj podsumowanie, wykonując za każdym razem te same kroki|
|Asystent AI|Pytania kierowane przez człowieka, interpretacja i podsumowanie|Pomóż inżynierowi przejrzeć dokumentację lub przygotuj podsumowanie na żądanie|
|Agent AI|Praca wieloetapowa, w której nowe dowody mogą zmienić kolejne narzędzie lub działanie|Wybierz zatwierdzone narzędzie dochodzeniowe, gdy dowody są niewystarczające|

Te podejścia nie są poziomami dojrzałości. W pełni autonomiczny agent nie jest automatycznie lepszy od skryptu, narzędzia wyszukiwania czy asystenta.

Najlepszy projekt to taki, który jest najprostszy i pozwala bezpiecznie osiągnąć wymagany rezultat. Prostszy komponent jest zazwyczaj łatwiejszy do testowania, wyjaśnienia, obsługi i konserwacji.

## Dlaczego agenci wymagają dodatkowej kontroli

Tradycyjny lub oparty na sztucznej inteligencji przepływ pracy podąża ścieżkami zdefiniowanymi z góry. Agent AI może mieć możliwość wyboru narzędzia, opracowania planu lub zmiany kierunku na podstawie otrzymanych informacji.

Taka elastyczność rodzi pytania, na które należy odpowiedzieć przed wdrożeniem:

- Do jakich narzędzi agent ma dostęp?
- Jakie informacje może wysyłać do tych narzędzi?
- Jak powinien sobie radzić z niedostępnym lub niezaufanym źródłem?
- W jaki sposób inżynier może zweryfikować dowody stanowiące podstawę rekomendacji?
- Kiedy agent musi się zatrzymać i poprosić o interwencję człowieka?
- Co się stanie, jeśli narzędzie zwróci nieprawidłowe lub sprzeczne informacje?
- Jakie będą skutki operacyjne, jeśli wniosek agenta okaże się błędny?

Te pytania są istotne, ponieważ prawdopodobna odpowiedź niekoniecznie jest poprawna. Magister prawa (LLM) potrafi brzmieć pewnie, nawet gdy jego dowody są niekompletne lub błędne.

Im większy autorytet otrzyma system, tym poważniejsze konsekwencje błędu. System, który przygotowuje podsumowanie dochodzenia, ma mniejszy wpływ niż system, który zamyka alerty, blokuje adresy IP lub dezaktywuje konta.

W przypadku NorthStar Fashion dochodzenie i działanie muszą zatem pozostać rozdzielone. Proponowany system może wspierać dochodzenie, ale ostateczną decyzję podejmuje inżynier.

## Czego zapobiega odkrycie

Pominięcie wykrywania może powodować występowanie kilku typowych błędów.

- **Automatyzacja niewłaściwego wąskiego gardła:** ponowne napisanie opisu alertu zaoszczędziłoby niewiele czasu, gdyby inżynier nadal musiał ręcznie przeszukiwać każde źródło.
- **Wykorzystanie sztucznej inteligencji tam, gdzie reguły są wystarczające:** model wprowadziłby zmienność i koszty do zadań, które ustrukturyzowany kod mógłby wykonywać niezawodnie.
- **Zakładając, że dane są gotowe:** istniejąca dokumentacja może być niekompletna, niespójna, nieaktualna lub trudna do pobrania.
- **Brak zdefiniowania ulepszenia:** jeśli zespół nie jest w stanie opisać, co można poprawić, nie jest w stanie określić, czy projekt zakończył się sukcesem.

Odkrycie uwidacznia te ryzyka, a jednocześnie umożliwia tanią modyfikację rozwiązania. Zapobiega to stosowaniu przez zespół tej samej technologii na każdym etapie tylko dlatego, że cały proces został oznaczony jako projekt agenta.

## Ważne wyniki odkryć

Ostateczne zalecenie będzie następujące:

- Zbuduj tradycyjny lub zautomatyzowany przepływ pracy.
- Zbuduj przepływ pracy AI.
- Zbuduj asystenta AI.
- Zbuduj agenta AI.
- Kontynuuj lub udoskonalaj istniejący proces bez tworzenia nowego systemu.

Wybór tradycyjnego przepływu pracy, przepływu pracy AI, asystenta AI lub braku kompilacji nie oznacza nieudanego projektu z agentem. Oznacza to, że odkrycie zapobiegło niepotrzebnej złożoności i ukierunkowało firmę na bardziej odpowiednią reakcję.

Teraz przekształcisz prośbę NorthStar Fashion w jasny problem biznesowy. Celem nie jest wybór między tradycyjnym procesem pracy,Magister prawaprzepływ pracy,Sztuczna inteligencjaAsystent, agent AI czy brak nowego systemu. Decyzja zapadnie później.

Pod koniec tego zadania będziesz mieć opis problemu biznesowego poparty dowodami z bieżącej sytuacji.

## Zacznij od prośby

Początkowe żądanie NorthStar Fashion można podsumować w następujący sposób: Zbudować agenta AI, który pomoże badać alerty bezpieczeństwa.

To mówi nam, co firma rozważa, ale nie czego potrzebuje. Nie identyfikuje najtrudniejszej części dochodzenia, wpływu na działalność ani wyniku, który powinien ulec poprawie.

Zamiast tego rozmowa kwalifikacyjna powinna zawierać pytania o to, kto przeprowadza dochodzenie, które części pochłaniają najwięcej wysiłku, jakie dowody są potrzebne, co się dzieje, gdy kontekst zostaje pominięty, co musi pozostać pod kontrolą człowieka i w jaki sposób NorthStar Fashion rozpoznałoby poprawę.

Pytania te sprawiają, że śledztwo koncentruje się na wartości operacyjnej, a nie na preferowanej technologii.

## Zbadaj dowody

![Ilustracja zatytułowana „Ważność to sygnał, a nie werdykt” pokazuje, że ważność alertu SIEM należy oceniać w kontekście dowodów zewnętrznych i kontekstu historycznego. Jeden przykład pokazuje, że alert o wysokiej ważności traci priorytet, ponieważ pasuje do zatwierdzonej aktywności historycznej, podczas gdy inny pokazuje, że alert o niskiej ważności zyskuje na znaczeniu ze względu na szkodliwą reputację IP. Grafika podkreśla, że ​​świadome ustalanie priorytetów zależy od połączenia ważności alertu z dowodami kontekstowymi, a nie wyłącznie od samej ważności.](https://cdn-images.tryhackme.com/user-uploads/6a2279941bcbd69b64b598f9/room-content/6a2279941bcbd69b64b598f9-1785421024657.png)

Problem biznesowy musi być poparty dowodami z obecnej sytuacji. NorthStar Fashion przedstawił już kilka przydatnych spostrzeżeń.

**Objętość alertów spełnia ograniczenia pojemności**

Inżynier analizuje około 50 alertów dziennie, dbając jednocześnie o bezpieczeństwo, infrastrukturę i kod. Ilość ta może być do opanowania dla dedykowanego zespołu ds. bezpieczeństwa, ale w NorthStar Fashion pracuje tylko jeden inżynier, który zajmuje się wszystkimi tymi zadaniami.

Liczba alertów jest zatem istotna ze względu na ograniczone możliwości firmy, a nie dlatego, że 50 jest automatycznie wysoką liczbą dla każdej organizacji.

**Wysoka powaga może być fałszywie dodatnia**

Inżynier zgłaszał przypadki, w którychSIEMsklasyfikował wielokrotne skanowanie sieci jako problem o wysokim stopniu zagrożenia. Po sprawdzeniu wcześniejszej dokumentacji inżynier stwierdził, że źródło należało do zatwierdzonego skanera luk w zabezpieczeniach.

Alert wydawał się niebezpieczny bez kontekstu, ale przypisana mu waga przeceniała rzeczywiste ryzyko.

**Niska powaga może ukrywać prawdziwe ryzyko**

Zdarzyła się również sytuacja odwrotna. Alertowi przypisano niską wagę, ale sprawdzenie reputacji IP wykazało, że jego adres źródłowy był powiązany ze złośliwą aktywnością.

Pokazuje to, że inżynier nie może opierać się wyłącznie na ocenie ważności SIEM, lecz musi zebrać dowody z innego źródła.

**Powiązane alerty mogą zmienić znaczenie**

Rozważmy dwa alerty dotyczące tego samego użytkownika:

- Logowanie następuje z nietypowej lokalizacji.
- Dziesięć minut później zostanie utworzona zewnętrzna reguła przekazywania poczty.

Każde zdarzenie samo w sobie może wydawać się niskie lub średnie. Razem mogą one wskazywać na naruszenie bezpieczeństwa konta i próbę przekierowania przyszłych wiadomości e-mail.

Inżynier musi zatem porównywać użytkowników, adresy IP, urządzenia, znaczniki czasu i zachowania w przypadku różnych alertów, zamiast badać każde zdarzenie w izolacji.

**Dowody są rozproszone**

Aby wyciągnąć wnioski, inżynier może potrzebować alertu SIEM, wyników oceny reputacji adresów IP, powiązanych zdarzeń, dokumentacji poprzednich incydentów i osobistych notatek z dochodzenia.

Problem nie polega tylko na tym, że dowody istnieją. Problem polega na tym, że inżynier musi je znaleźć, porównać i zinterpretować ręcznie, jednocześnie zajmując się innymi obowiązkami.

## Oddzielne objawy, przyczyny, skutki i rozwiązania

Odkrycia stają się jaśniejsze, gdy każde stwierdzenie zostanie umieszczone we właściwej kategorii.

|Kategoria|Przykład mody NorthStar|
|---|---|
|Objaw|Codziennie trzeba przejrzeć około 50 alertów|
|Przyczyna współistniejąca|Istotne dowody pochodzą z kilku źródeł|
|Trudność podejmowania decyzji|Poważność SIEM i pojedyncze alerty mogą nie odzwierciedlać rzeczywistego ryzyka|
|Wpływ operacyjny|Powtarzające się badania konkurują z innymi pracami inżyniera|
|Proponowane rozwiązanie|Zbuduj agenta AI|

„NorthStar Fashion otrzymuje zbyt wiele alertów” jest niekompletne, ponieważ koncentruje się wyłącznie na liczbie. Ukrywanie lub odrzucanie alertów mogłoby zmniejszyć ich liczbę, nie zwiększając bezpieczeństwa śledztw.

„NorthStar Fashion nie ma agenta AI” to również nie problem biznesowy. Opisuje on raczej brak technologii, a nie potrzebę operacyjną.

Podstawowy problem polega na tym, że inżynier musi wielokrotnie gromadzić i interpretować fragmentaryczne dowody, zanim alerty będą mogły zostać z pewnością priorytetyzowane. To jest prawdziwy problem, z którym zmaga się NorthStar.

## Oświadczenie o problemie biznesowym

Dowody można teraz połączyć w oświadczenie problemu biznesowego:

**Jedyny inżynier NorthStar Fashion musi ręcznie gromadzić i interpretować dowody z kilku źródeł, analizując jednocześnie około 50 alertów bezpieczeństwa każdego dnia. Poziom zagrożenia w systemie SIEM może błędnie odzwierciedlać rzeczywiste ryzyko, a powiązane zdarzenia mogą zmieniać znaczenie alertu. To powtarzalne dochodzenie zabiera inżynierowi czas, który mógłby poświęcić innym obowiązkom związanym z bezpieczeństwem, infrastrukturą i rozwojem.**

Oświadczenie opisuje interesariuszy, trudności, przyczynę i wpływ operacyjny. Nie zaleca tradycyjnego przepływu pracy, przepływu pracy LLM, asystenta AI ani agenta AI.

W następnym zadaniu zmapujesz aktualny przebieg prac dochodzeniowych i zweryfikujesz, w którym miejscu poszczególnych kroków pojawia się ten problem.

Zadanie 4 zidentyfikowało problem biznesowy NorthStar Fashion: jedyny inżynier firmy musi wielokrotnie zbierać i interpretować fragmentaryczne dowody, zanim alerty bezpieczeństwa będą mogły zostać priorytetyzowane z całą pewnością.

Następnym krokiem jest dokładne zrozumienie, jak ta praca jest obecnie wykonywana. Problem biznesowy wyjaśnia,  **co jest nie tak** ; mapa przepływu pracy wyjaśnia,  **gdzie i jak występuje problem** .

W tym zadaniu zmapujesz bieżące śledztwo prowadzone przez człowieka. Nie projektujeszSztuczna inteligencjaagent lub ulepszony proces.

## Dlaczego warto mapować aktualny przepływ pracy?

![Ilustracja zatytułowana „Archeologia przepływu pracy” przedstawia proces mapowania istniejącego przepływu pracy w ramach śledztwa przed jego przeprojektowaniem. Przepływ pracy przechodzi przez sześć etapów: wniosek, wyjaśnienie, wyszukiwanie, ocena, szkic i weryfikacja przez człowieka. Wzmianki wskazują na typowe źródła problemów, takie jak opóźnienia, powtarzalność działań, sprzeczne dowody i wąskie gardło w procesie weryfikacji, podkreślając wagę zrozumienia obecnego procesu przed wprowadzeniem sztucznej inteligencji lub automatyzacji.](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1787951707440.png)Zwrot „zbadaj alert” sugeruje, że praca ta brzmi jak jedno zadanie. W praktyce obejmuje ona kilka działań, wyszukiwań, porównań i decyzji.

Jeśli NorthStar Fashion traktuje dochodzenie jako jedno duże zadanie, może zastosować tę samą technologię na każdym etapie. Mapowanie przepływu pracy ujawnia, które kroki są przewidywalne, które zależą od kontekstu, a w których inżynier musi podjąć decyzję.

Przydatna mapa stanu bieżącego rejestruje czynnik wyzwalający, kolejność prac, wykorzystane informacje i narzędzia, dane wyjściowe każdego kroku, decyzje zmieniające ścieżkę, powtarzane prace i punkt, w którym kończy się przepływ pracy.

Proces ten bywa czasem nazywany  **archeologią przepływu pracy**  , ponieważ niektóre ważne kroki mogą istnieć jedynie w nawykach inżyniera lub osobistych notatkach, a nie w oficjalnej procedurze.

## Ustaw granicę przepływu pracy

Mapa przepływu pracy wymaga wyraźnego początku i końca. Bez granic mapa może rozszerzyć się na niezwiązane ze sobą operacje bezpieczeństwa.

Do tego ćwiczenia:

- **Początek:**  ASIEMinżynier może zapoznać się z alertem.
- **Koniec:**  Inżynier zapisuje wnioski z dochodzenia i decyduje, jaki priorytet należy nadać alertowi lub jak go obsłużyć w następnej kolejności.

Działania ograniczające, takie jak blokowanie adresu IP, wyłączanie konta czy zmiana ustawień zabezpieczeń, wykraczają poza ten proces. NorthStar Fashion oświadczył już, że proponowany system nie może wykonywać tych działań.

Mapa opisuje to, co inżynier aktualnie robi, w tym pracę nieefektywną lub powtarzalną. Nie zastępuj czynności manualnej proponowanym narzędziem podczas mapowania.

**Krok 1: Przejrzyj alert SIEM**

Przepływ pracy rozpoczyna się w momencie otwarcia alertu w systemie SIEM przez inżyniera.

Dostępne informacje mogą obejmować typ alertu, znacznik czasu, przypisaną wagę, użytkownika, adres IP, urządzenie, miejsce docelowe i opis zdarzenia. Dokładne pola zależą od alertu.

Inżynier przegląda alert i zapisuje szczegóły, które mogą pomóc w dochodzeniu, takie jak nazwa użytkownika, adres IP, urządzenie i znacznik czasu. Dane te są następnie wykorzystywane do wyszukiwania dowodów w innych źródłach.

**Krok 2: Zdecyduj, jakie dowody są potrzebne**

Nie każdy alert zawiera te same informacje. Alert może zawierać źródłowy adres IP, konto użytkownika, urządzenie lub kilka z tych identyfikatorów.

Inżynier decyduje, które informacje mogą pomóc w weryfikacji alertu. Jeśli źródłowy adres IP jest dostępny, można sprawdzić jego reputację. Jeśli użytkownik lub urządzenie jest dostępne, można wyszukać powiązaną aktywność. Jeśli brakuje przydatnych identyfikatorów, inżynier musi wykorzystać pozostały kontekst.

Ścieżka dochodzenia zależy zatem od treści alertu.

**Krok 3: Sprawdź reputację IP**

Jeśli alert zawiera zewnętrzny adres IP, inżynier sprawdza go za pomocą usługi reputacji adresów IP.

Wynik może wskazywać na zgłoszoną szkodliwą aktywność, brak znanego nadużycia lub niewystarczające informacje. Dowód ten należy porównać z alertem SIEM, a nie traktować jako ostatecznej odpowiedzi.

Adres IP, który nie ma historii znanych nadużyć, nie jest automatycznie bezpieczny, a zgłoszony adres nadal wymaga kontekstu.

**Krok 4: Wyszukaj poprzednią dokumentację**

Inżynier przeszukuje dokumentację poprzednich incydentów i notatki z dochodzeń w celu znalezienia pasujących użytkowników, adresów IP, urządzeń, typów alertów lub zachowań.

Kontekst historyczny może wyjaśniać, że adres należy do zatwierdzonego skanera lub że podobna działalność była wcześniej badana. Zapisy mogą być również niekompletne, nieaktualne lub sporządzone przy użyciu innych terminów.

Wynikiem tego kroku nie jest po prostu dopasowany dokument. Inżynier musi zdecydować, czy rekord jest istotny dla bieżącego alertu.

**Krok 5: Wyszukaj powiązane alerty**

Inżynier przeszukuje system SIEM w celu znalezienia innych alertów dotyczących tego samego użytkownika, adresu IP, urządzenia lub okresu.

Ten krok jest konieczny, ponieważ oddzielne zdarzenia mogą wydawać się mało ryzykowne, dopóki nie zostaną połączone. Przykładem jest logowanie do nietypowej lokalizacji, po którym następuje zewnętrzna reguła przekierowania poczty.

Inżynier umieszcza potencjalnie powiązane zdarzenia na osi czasu i sprawdza, czy ich identyfikatory i zachowania tworzą sensowną sekwencję.

**Krok 6: Porównaj i skoreluj dowody**

Inżynier porównuje teraz oryginalny alert z wynikami reputacji IP, historyczną dokumentacją, notatkami osobistymi i powiązanymi zdarzeniami.

Dowody mogą być zgodne, sprzeczne lub niekompletne. Na przykład, alert o wysokiej wadze może pasować do zatwierdzonego adresu IP skanera, podczas gdy alert o niskiej wadze może dotyczyć złośliwego adresu IP.

To najbardziej wymagająca osądu część obecnego procesu pracy. Inżynier musi zdecydować, które dowody są istotne i co oznaczają połączone informacje.

**Krok 7: Podejmij decyzję o dochodzeniu**

Po przeanalizowaniu dostępnych dowodów inżynier podejmuje decyzję, czy alertowi można nadać niższy priorytet, czy wymaga on dalszego zbadania, czy też powinien zostać przekazany dalej.

Jeśli dowody są niewystarczające lub sprzeczne, inżynier może powrócić do wcześniejszego kroku, przeprowadzić kolejne wyszukiwanie lub poszukać dodatkowego kontekstu. Dlatego przepływ pracy nie zawsze przebiega w linii prostej.

Inżynier pozostaje odpowiedzialny za decyzję.

**Krok 8: Zanotuj wynik**

Inżynier rejestruje wniosek i dowody wykorzystane do jego sformułowania. Może to obejmować powód, dla którego alert został uznany za oczekiwaną aktywność, dlaczego pozostaje podejrzany lub które powiązane zdarzenia zmieniły jego priorytet.

Zapis staje się notatką lub jest dokumentowany jako kontekst do przyszłych dochodzeń. Słaba lub niekompletna dokumentacja na tym etapie może stwarzać problemy, gdy podobny alert pojawi się później.

Bieżący obieg pracy kończy się po zarejestrowaniu wniosku i ustaleniu priorytetu następnego zadania.

## Mapa przepływu pracy w stanie bieżącym

Główną ścieżkę można przedstawić następująco:

![Schemat blokowy ilustrujący aktualny przebieg badania alertów bezpieczeństwa. Proces rozpoczyna się od alertu SIEM, a następnie następuje gromadzenie dowodów z adresu IP źródłowego, użytkownika lub urządzenia oraz szczegółów alertu. Następnie badanie wykonuje takie zadania, jak sprawdzanie reputacji adresów IP, wyszukiwanie powiązanych alertów i przeglądanie dokumentacji przed porównaniem zebranych dowodów. Punkt decyzyjny określa, czy dostępne dowody są wystarczające. Jeśli nie, przepływ pracy zawraca w celu zebrania dodatkowych dowodów; w przeciwnym razie badacz podejmuje decyzję i rejestruje wynik. Diagram pokazuje, że badanie jest procesem iteracyjnym, opartym na gromadzeniu dowodów i podejmowaniu decyzji.](https://cdn-images.tryhackme.com/user-uploads/6a2279941bcbd69b64b598f9/room-content/6a2279941bcbd69b64b598f9-1785421141727.png)

## Zbuduj mapę zadań

Przed oceną możliwych rozwiązań należy podzielić przepływ pracy na pojedyncze zadania.

|Krok|Wejście|Aktualne działanie|Wyjście|
|---|---|---|---|
|Alert przeglądu|Alert SIEM|Przeczytaj szczegóły i zidentyfikuj przydatne jednostki|Wyodrębnione fakty dotyczące alertów|
|Wybierz dowody|Alertowe fakty|Zdecyduj, które kontrole są istotne|Ścieżka dochodzenia|
|Sprawdź reputację|Źródło IP|Wyszukaj zewnętrzną usługę reputacji|Wynik reputacji|
|Historia wyszukiwania|Informacje i identyfikatory alertów|Przeszukaj dokumentację i notatki|Potencjalnie istotne rekordy|
|Znajdź powiązane alerty|Użytkownik, adres IP, urządzenie i czas|Wyszukaj i zorganizuj powiązane wydarzenia|Oś czasu wydarzenia|
|Dowody korelacyjne|Wyniki ze wszystkich źródeł|Porównaj trafność, spójność i znaczenie|Ocena śledztwa|
|Podjąć decyzję|Ocena śledztwa|Zastosuj ocenę bezpieczeństwa|Priorytet lub następne działanie|
|Wynik rekordu|Decyzja i dowody|Napisz wniosek z dochodzenia|Zapis śledztwa|

Nie oznaczaj zadania jako tradycyjnego, Magister prawaoparte na, kierowane przez asystenta lub agenta. Zadanie 6 oceni zadania po zebraniu bieżącego przepływu pracy.

## Identyfikuj wąskie gardła i punkty decyzyjne

Mapa ujawnia kilka obszarów, które wymagają późniejszej oceny. Inżynier porusza się między kilkoma źródłami, poziom istotności SIEM wymaga kontekstu, dane historyczne wymagają oceny trafności, a powiązane alerty muszą być skorelowane pod względem identyfikatorów i czasu. Brakujące lub sprzeczne dowody mogą powtarzać wcześniejsze kroki, a ostateczny wniosek wymaga odpowiedzialności człowieka.

Obserwacje te opisują przepływ pracy, ale nie dowodzą, że agent AI jest konieczny.

W następnym zadaniu wprowadzisz tę mapę do płótna Agent Discovery Canvas, ocenisz częstotliwość, złożoność i ryzyko zadań, zastosujesz skalę Human Agency Scale i porównasz pięć ścieżek rozwiązań.

![Ilustracja zatytułowana „Ostateczna decyzja o kompilacji” przedstawia możliwe wyniki procesu wykrywania agentów. Pokazano trzy ścieżki decyzyjne: Buduj z warunkami, Sprawdź przed kompilacją i Nie buduj. Grafika podkreśla, że ​​agent AI powinien być budowany tylko wtedy, gdy istnieją odpowiednie zabezpieczenia, w tym zatwierdzone źródła danych, gromadzenie dowodów, weryfikacja przez człowieka, rejestrowanie przepływu pracy i eskalacja w razie niepewności. Podkreśla, że ​​ostateczna decyzja opiera się na wynikach wykrywania, a nie na preferencjach wobec sztucznej inteligencji.](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1787951837597.png)  
Kliknij przycisk „ **Wyświetl witrynę”** u góry zadania, aby uruchomić witrynę statyczną i zakończyć działanie. Przeanalizuj każdy etap, aby zidentyfikować rzeczywisty problem biznesowy, zbudować aktualny wykres alertów i dochodzeń oraz sklasyfikować zadania, które pasują do tradycyjnego przepływu pracy, a które wymagają…Magister prawa-system oparty na systemie. Następnie musisz rozróżnić między Sztuczna inteligencja przepływ pracy, asystenta AI i agenta AI w zależności od tego, kto kontroluje następny krok, a także określ, co proponowany system może, a czego nie może zrobić.

W tym pomieszczeniu przeszedłeś od proponowanego rozwiązania NorthStar Fashion do rekomendacji opartej na dowodach. Wyróżniłeś tradycyjne procesy pracy, Sztuczna inteligencja przepływy pracy, asystentów AI i agentów AI; zidentyfikowano rzeczywisty problem biznesowy; zmapowano bieżący proces alertów i dochodzeń; oraz wykorzystano narzędzie Agent Discovery Canvas do oceny poszczególnych zadań. Rezultatem jest rekomendacja dla kontrolowanego agenta AI wspierającego dochodzenia, który może gromadzić zatwierdzone dowody, korelować alerty, przygotowywać podsumowania i sugerować kolejny krok dochodzenia, podczas gdy inżynier zachowuje odpowiedzialność za ostateczną decyzję i wszystkie działania mające na celu powstrzymanie zagrożenia.

## Najważniejsze wnioski

- **Odkrywanie agentów zaczyna się od problemu, a nie od proponowanego agenta.** Zrozumienie potrzeb biznesowych, osób, których to dotyczy, i bieżącego przepływu pracy zapobiega automatyzowaniu przez zespoły niewłaściwych wąskich gardeł lub dodawaniu sztucznej inteligencji tam, gdzie prostsze rozwiązanie sprawdziłoby się lepiej.
- **To, kto kontroluje następny krok, decyduje o rodzaju systemu;** w tradycyjnej automatyzacji obowiązują stałe reguły, sterowane kodem Magister prawa Kroki tworzą przepływ pracy AI, interakcje prowadzone przez inżynierów tworzą asystenta AI, a decyzje oparte na dowodach podejmowane przez model tworzą agenta AI.
- **Wsparcie śledztwa i działania zabezpieczające muszą pozostać oddzielne;** kontrolowany agent może gromadzić dowody, łączyć alerty, przygotowywać podsumowania i zalecać kolejne kroki, ale jasne granice, warunki zatrzymania i kontrola człowieka pozostawiają ostateczne decyzje i działania powstrzymujące inżynierowi.
