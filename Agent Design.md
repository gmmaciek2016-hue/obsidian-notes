W poprzedniej sali ukończyłeś/aś szkolenie [Agent Discovery](https://tryhackme.com/room/agentdiscovery) dla NorthStar Fashion. Zbadałeś/aś problem biznesowy, zmapowałeś/aś aktualny proces badania alertów, wziąłeś/aś pod uwagę nadzór ludzki i porównałeś/aś możliwe ścieżki rozwiązań.

Ten pokój przechodzi od **odkrywania** do **projektowania** .

NorthStar Fashion bada obecnie kontrolowany Sztuczna inteligencja System wspomaganego dochodzenia w przypadku alertów bezpieczeństwa. System powinien pomagać inżynierowi w gromadzeniu dowodów, korelowaniu kontekstu, przygotowywaniu podsumowań i rekomendowaniu priorytetów dochodzenia.

System nie może jednak zastąpić odpowiedzialności inżyniera. Nie może blokować adresów IP, wyłączać kont, zamykać alertów, modyfikować elementów sterujących, usuwać dowodów ani prowadzić działań powstrzymujących.

Celem tego pokoju jest zdefiniowanie projektu agenta przed rozpoczęciem implementacji.

Decydujesz, co agent powinien robić, czego nie powinien robić, jakich narzędzi może używać, jakiego kontekstu i stanu potrzebuje, kiedy powinien się zatrzymać i kiedy wymagana jest kontrola ze strony człowieka.

## Cele edukacyjne

- Przekształć wyniki odkryć w wymagania projektowe.
- Zdefiniuj rolę agenta, cel i granice przepływu pracy.
- Określ dozwolone i niedozwolone działania agenta.
- Wybierz odpowiednie narzędzia dla agenta wspierającego dochodzenie.
- Zdefiniuj wymagania dotyczące kontekstu, stanu, pamięci i wyników.
- Dodaj punkty kontroli ludzkiej i warunki zatrzymania.

## Wymagania wstępne

- Ukończono  salę [Agent Discovery](https://tryhackme.com/room/agentdiscovery) , ponieważ sala ta bazuje bezpośrednio na scenariuszu NorthStar Fashion, mapie przepływu pracy, analizie nadzoru ludzkiego i ostatecznych zaleceniach.

![etapy odkrywania i projektowania](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785343542460.png)

Przed Sztuczna inteligencja Po wdrożeniu agenta potrzebny jest przejrzysty projekt.

**Projektowanie agenta** to proces definiowania jego zachowania przed wyborem jakiegokolwiek kodu, modelu, frameworka lub integracji narzędzi. Dobry projekt wyjaśnia, za co odpowiada agent, do czego ma dostęp, czego nigdy nie powinien robić, jak powinien radzić sobie z niepewnością oraz gdzie wymagany jest nadzór człowieka.

Ten krok jest ważny, ponieważ agenci mogą podejmować decyzje w trakcie wykonywania kodu. Mogą wybierać narzędzia, interpretować dowody, aktualizować stan, śledzić rozgałęzienia i kontynuować pracę w kilku krokach. Bez jasnego projektu ta elastyczność może stać się niebezpieczna lub nieprzewidywalna.

Na przykład agent dochodzeniowy ds. alertów, którego zadaniem jest wyłącznie pomoc w gromadzeniu dowodów, nie powinien przypadkowo posiadać uprawnień do blokowania adresów IP, wyłączania kont, zamykania alertów ani modyfikowania zabezpieczeń. Są to działania ograniczające i wymagają odpowiedzialności człowieka.

Projektowanie przekształca szeroką ideę w taki sposób:

_Utwórz agenta do badania alertów._

W kierunku bezpieczniejszej i bardziej szczegółowej specyfikacji:

_Zbuduj agenta śledczego wspomaganego przez sztuczną inteligencję, który gromadzi zatwierdzone dowody, zestawia kontekst, przygotowuje uporządkowane podsumowanie, zaleca priorytet śledztwa i przesyła wyniki inżynierowi do przeglądu._

Druga wersja jest lepsza, ponieważ definiuje cel agenta, granice, dane wyjściowe i wymagania dotyczące przeglądu przez człowieka.

## Dlaczego projektowanie agentów ma znaczenie

_Niejasna konstrukcja agenta stwarza ryzyko._

Jeśli rola jest niejasna, od agenta można oczekiwać zbyt wielu działań. Jeśli zakres narzędzi jest zbyt szeroki, agent może uzyskać dostęp do działań, które powinny pozostać pod kontrolą człowieka. Jeśli stan nie jest zdefiniowany, trudniej jest zrozumieć, jakie dowody zostały sprawdzone lub dlaczego wydano rekomendację. Jeśli brakuje warunków zatrzymania, agent może kontynuować działanie, mimo że powinien poprosić o pomoc.

Solidna konstrukcja agenta pomaga odpowiedzieć na pytania takie jak:

- Co agent próbuje osiągnąć?
- Jakie działania są dozwolone?
- Jakie działania są niedozwolone?
- Z jakich narzędzi może korzystać agent?
- Jakie informacje należy podać w kontekście?
- Jakie informacje powinny być śledzone w państwie?
- Jakie zasady pamięci są potrzebne?
- Kiedy agent powinien poprosić o recenzję ludzką?
- Kiedy agent powinien zakończyć działalność?
- Jak powinien wyglądać efekt końcowy?

Pytania te zmniejszają niejednoznaczność przed rozpoczęciem wdrażania.

_Celem nie jest uczynienie agenta tak autonomicznym, jak to możliwe. Celem jest zaprojektowanie najprostszego zachowania agenta, które bezpiecznie obsługuje przepływ pracy._

## Metodologia projektowania

W tym pomieszczeniu specyfikacja agenta podzielona jest na **pięć części** . Każda część koncentruje się na jednym obszarze projektowania i jednej zasadzie projektowania, które pomagają zapewnić użyteczność, kontrolę, możliwość przeglądu i bezpieczeństwo agenta.

Główną zasadą projektowania jest to, że agent powinien wspierać dochodzenie, nie przekraczając swoich uprawnień. Specyfikacja powinna definiować rolę agenta, narzędzia, przepływ informacji, punkty kontroli przez człowieka, warunki zatrzymania i ostateczny wynik przed rozpoczęciem implementacji.

Każdy komponent zostanie przedstawiony w osobnym zadaniu wraz z zasadą projektowania, którą reprezentuje, zanim ukończysz ostatnie wyzwanie Agent Spec Builder. Rozpoczniesz od zdefiniowania roli i zakresu agenta, a następnie granic jego narzędzi. Następnie określisz wymagany kontekst, stan i pamięć, dodasz punkty kontroli przez człowieka i warunki zatrzymania, a na koniec zdefiniujesz jego ustrukturyzowane dane wyjściowe.

Zasady te pomogą Ci zdecydować, które rozwiązania projektowe są bezpieczne, które są niekompletne, a które należy odrzucić.

![Zaprojektuj agenta przed jego utworzeniem](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785343542543.png)

![Rola i zakres agenta](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785344645899.png)

Przed dokonaniem wyboru narzędzi, pamięci lub pól wyjściowych agent musi mieć jasno określoną **rolę** i **zakres** .

- Rola opisuje zakres odpowiedzialności agenta **.**
- Zakres  określa **,** gdzie zaczyna się i kończy odpowiedzialność.

Ma to znaczenie, ponieważ niejasne role agentów mogą tworzyć niebezpieczne oczekiwania. Jeśli agent jest opisany jako „badający alerty”, może to oznaczać wiele różnych rzeczy: Czy tylko gromadzi dowody? Czy rekomenduje priorytet? Czy zamyka alerty? Czy blokuje adresy IP? Czy wyłącza konta?

_![Bezpieczny projekt](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785344645765.png)__Bezpieczny projekt eliminuje tę niejednoznaczność jeszcze przed rozpoczęciem wdrażania._

W przypadku NorthStar Fashion agent powinien wspierać inżyniera podczas dochodzeń w sprawie alertów. Może on pomóc w zebraniu zatwierdzonych dowodów, skorelowaniu kontekstu, przygotowaniu ustrukturyzowanego podsumowania i zaleceniu priorytetu dochodzenia do weryfikacji przez człowieka.

_Nie może podejmować ostatecznych decyzji ani przeprowadzać działań powstrzymujących._

## Dlaczego rola i zakres są ważne

Agenta o dobrze określonym zakresie łatwiej zbudować, przetestować, ocenić i zabezpieczyć.

Jeśli rola jest zbyt szeroka, agent może otrzymać narzędzia lub uprawnienia wykraczające poza rzeczywiste potrzeby. Może to prowadzić do niebezpiecznych zachowań, takich jak modyfikowanie systemów, automatyczne zamykanie alertów lub podejmowanie decyzji bez udziału człowieka.

Dobra rola agenta powinna odpowiadać na cztery pytania:

1. W czym pomaga agent?
2. Jakich informacji może użyć?
3. Jaki wynik powinien wytworzyć?
4. Jakie decyzje musi podjąć człowiek?

W tym pomieszczeniu agent powinien być zaprojektowany jako **agent wspomagający dochodzenie,** a nie agent powstrzymujący.

Oznacza to, że agent może wspierać proces, ale nie ma kontroli nad końcowym wynikiem kontroli bezpieczeństwa.

## Dobra definicja roli

Bezpieczna definicja roli w tym scenariuszu mogłaby wyglądać następująco:

- Agent pomaga inżynierowi w gromadzeniu zatwierdzonych dowodów na potrzeby alertu bezpieczeństwa.
- Korelacja odpowiedniego kontekstu.
- Przygotowanie ustrukturyzowanego podsumowania dochodzenia.
- Zalecanie priorytetowego przeglądu przez człowieka.

Ta rola jest silna, ponieważ definiuje:

- **Cel** : pomoc inżynierowi
- **Granica dowodu** : zatwierdzony dowód
- **Główna aktywność** : korelowanie odpowiedniego kontekstu
- **Wynik** : podsumowanie strukturalnego dochodzenia
- **Granica decyzyjna** : zalecenie do przeglądu przez człowieka

_Agent jest przydatny, ale jego uprawnienia są ograniczone._

## Słaba definicja roli

Niewłaściwa definicja roli wyglądałaby następująco:

_Agent automatycznie bada i obsługuje alerty bezpieczeństwa._

Jest to niebezpieczne, ponieważ jest niejasne i daje agentowi zbyt duże uprawnienia.

![Agent z zbyt dużą władzą](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785344645834.png)

Zwrot „automatycznie obsługuje alerty bezpieczeństwa” może sugerować, że agent może zamykać alerty, eskalować incydenty, blokować adresy IP, wyłączać konta lub wykonywać działania powstrzymujące bez kontroli ze strony człowieka – a wszystkie te czynności wykraczają poza zamierzony zakres.

## Dozwolone obowiązki agenta

W przypadku NorthStar Fashion agent może:

- Czytać SIEM szczegóły alertu.
- Wyodrębnij istotne jednostki, takie jak użytkownicy, adresy IP, urządzenia i znaczniki czasu.
- Zapytaj o zatwierdzone źródła dowodów.
- Przeszukaj poprzednie notatki śledcze.
- Znajdź powiązane alerty.
- Dowody korelacyjne.
- Przygotuj uporządkowane podsumowanie śledztwa.
- Zalecenie nadania priorytetu dochodzeniu w celu przeprowadzenia przeglądu przez człowieka.
- Poproś o opinię człowieka, gdy brakuje dowodów lub są one sprzeczne.

Obowiązki te wspomagają śledztwo, nie dając agentowi kontroli nad działaniami zabezpieczającymi.

## Niedozwolone obowiązki agenta

Agentowi nie wolno:

- Zablokuj adresy IP.
- Wyłącz konta.
- Automatyczne zamykanie alertów.
- Modyfikować zapora sieciowa, JA JESTEM, e-mail lub sterowanie SIEM.
- Usunąć lub zmienić dowody.
- Wymyśl brakujące dowody.
- Kontynuuj w nieskończoność, jeśli dowody są niewystarczające.
- Przedstaw rekomendację bez poparcia dowodami.
- Podejmij ostateczną decyzję dotyczącą bezpieczeństwa.

Działania te wykraczają poza zakres agenta, ponieważ obejmują powstrzymywanie, modyfikację systemu, niepoparte uzasadnienie lub ostateczną odpowiedzialność.

Inżynier pozostaje odpowiedzialny za decyzję o sposobie postępowania z alertem.

## Granica zakresu

Granice przepływu pracy agenta powinny być jasne.

Granica tego pomieszczenia jest następująca:

- Start: Dostępny jest alert bezpieczeństwa do przejrzenia.
- Koniec: Agent przygotowuje dla inżyniera ustrukturyzowane podsumowanie dochodzenia i zalecenia dotyczące priorytetów.

Przebieg prac nie obejmuje powstrzymywania ani naprawiania.

Takie czynności jak blokowanie adresu IP, wyłączanie konta, resetowanie hasła, zmiana reguły zapory sieciowej lub zamykanie alertu powinny być wykonywane poza uprawnieniami agenta.

Bezpieczna konstrukcja pozwala na oddzielenie wsparcia dochodzeniowego od zabezpieczenia.

## Zasada projektowania: Granica zakresu

Rola i zakres powinny być zgodne z następującą zasadą:

_Agent wspiera śledztwo, ale to człowiek podejmuje decyzję._

Zasada ta powinna kierować każdą pozostałą decyzją projektową. Wybór narzędzi, kontekstu, stanu, pamięci, warunków zatrzymania i pól wyjściowych musi zachować tę samą granicę: jeśli jakikolwiek wybór pozwala agentowi na działanie wykraczające poza wsparcie dochodzeniowe, należy go odrzucić.

Narzędzia agenta definiują jego faktyczne możliwości. Podczas gdy monit opisuje rolę agenta, jego narzędzia określają jego rzeczywiste możliwości. Jeśli agent ma dostęp do niebezpiecznego narzędzia, system może być o krok od niebezpiecznego zachowania, zaledwie o jedną złą decyzję, monit, dane wejściowe lub przekierowanie.

Z tego powodu **projektowanie narzędzi** to nie tylko decyzja inżynierska. To także granica bezpieczeństwa.

W tym zadaniu przejrzysz proponowany katalog narzędzi dla NorthStar FashionSztuczna inteligencja-wspierany agent śledczy. Twoim celem jest decyzja, które narzędzia powinny znajdować się w granicach agenta, a które poza nimi.

## Przegląd granic narzędzi

Inżynier NorthStar Fashion chce, aby agent pomógł w dochodzeniach dotyczących alertów.

Agent powinien być w stanie:

- Przeczytaj szczegóły alertu.
- Zbierz zatwierdzone dowody.
- Wyszukaj poprzednie notatki.
- Znajdź powiązane alerty.
- Podsumuj ustalenia.
- Zalecenie priorytetowego przeglądu.

Jednakże agent nie może podejmować działań powstrzymujących lub modyfikować systemów.

Oznacza to, że granica narzędzi powinna oddzielać **narzędzia wspomagające dochodzenie** od **narzędzi służących podejmowaniu działań** .

Przydatnym sposobem myślenia o tym jest:

- Czy to narzędzie może pomóc agentowi zrozumieć alert?
    - Może znajdować się w granicach agenta.
- Czy to narzędzie może zmienić środowisko lub wpłynąć na użytkownika, system, alert lub element sterujący? 
    -  Powinien pozostać poza granicami agenta.

_Najbezpieczniejszy agent to nie ten, który ma najwięcej narzędzi. Najbezpieczniejszy agent to ten, który ma minimum narzędzi potrzebnych do wykonania swojej roli._

## Katalog narzędzi dla kandydatów

Zespół programistów proponuje następujący katalog narzędzi:

|Narzędzie|Opis|
|---|---|
|`get_alert_details`|Pobiera pola alertów z SIEM|
|`check_ip_reputation`|Sprawdza zatwierdzone źródło reputacji IP|
|`search_previous_notes`|Przeszukuje notatki z poprzednich śledztw|
|`find_related_alerts`|Wyszukuje powiązane alerty według użytkownika, adresu IP, urządzenia lub czasu|
|`disable_account`|Wyłącza konto użytkownika|
|`close_alert`|Zamyka alert w systemie SIEM|

Na pierwszy rzut oka wszystkie te narzędzia są związane z bezpieczeństwem. Nie oznacza to jednak, że wszystkie powinny być częścią agenta.

Pytanie nie brzmi:

_Czy to narzędzie jest przydatne pod kątem bezpieczeństwa?_

Lepsze pytanie brzmi:

_Czy to narzędzie jest bezpieczne i niezbędne dla agenta wspierającego śledztwo?_

## Narzędzia wspomagające dochodzenie

Niektóre narzędzia pomagają agentowi gromadzić lub porządkować dowody bez zmiany środowiska.

Narzędzia te są dostosowane do roli agenta:

- `get_alert_details`
- `check_ip_reputation`
- `search_previous_notes`
- `find_related_alerts`

Te narzędzia są odpowiednie, ponieważ wspomagają dochodzenie. Pomagają agentowi odpowiedzieć na pytania takie jak:

- Co się stało?
- Jakie podmioty są zaangażowane?
- Czy ten adres IP pojawił się już wcześniej?
- Czy istnieją powiązane alerty?
- Czy istnieje wcześniejszy kontekst?

Nie zawierają one, nie naprawiają ani nie modyfikują bezpośrednio niczego.

To sprawia, że ​​są bezpieczniejszymi kandydatami dla tego środka.

## Narzędzia do podejmowania działań

Inne narzędzia wykraczają poza ramy badania i odpowiedzi.

Te narzędzia nie powinny być dostępne dla agenta:

- `disable_account`
- `close_alert`

Działania te mogą być prawidłowe w rzeczywistym procesie reagowania na incydenty, jednak nie powinny być wykonywane przez tego agenta.

`disable_account`ma wpływ na użytkownika i może zakłócić działalność biznesową.

`close_alert`zmienia zapis śledztwa i może ukryć prawdziwy problem, jeśli agent się myli.

Obie czynności wymagają odpowiedzialności człowieka: inżynier może zdecydować się na ich wykonanie później, ale agent nie powinien mieć do nich bezpośredniego dostępu.

## Zasada projektowania: Minimalny bezpieczny dostęp

Bezpieczna granica narzędzia opiera się na następującej zasadzie:

_Udziel agentowi wystarczającego dostępu do gromadzenia dowodów, ale nie wystarczającego, aby mógł podjąć nieodwracalne lub mające duży wpływ działania._

W przypadku NorthStar Fashion oznacza to, że agent może pobierać i podsumowywać dowody ze śledztwa, ale nie może wpływać na otoczenie.

To rozdzielenie jest ważne, ponieważ agent może się mylić, narzędzie może zwrócić niekompletne dane lub dostępne dowody mogą być sprzeczne. Jeśli agent gromadzi jedynie dowody, błędy są łatwiejsze do wykrycia podczas weryfikacji przez człowieka. Jeśli agent może działać bezpośrednio, ten sam błąd może mieć wpływ na działanie systemu.

## Lista kontrolna projektowania narzędzi

Zanim zatwierdzisz narzędzie dla agenta, zadaj sobie następujące pytania:

- Czy narzędzie wspiera rolę agenta?
- Czy narzędzie ma jasny i wąski cel?
- Czy narzędzie dostarcza użytecznych dowodów?
- Czy narzędzie może zmieniać systemy, użytkowników, alerty lub elementy sterujące?
- Czy niewłaściwe użycie tego narzędzia może mieć negatywny wpływ na działalność biznesową?
- Czy człowiek powinien zatwierdzić tę akcję?

Narzędzie należy odrzucić lub przenieść poza granice agenta, jeśli może ono modyfikować systemy, wpływać na użytkowników, usuwać dowody, zamykać rekordy lub wykonywać czynności powstrzymujące.

## Bezpieczniejszy alternatywny wzór

Odrzucenie narzędzia do podejmowania działań nie oznacza całkowitego zignorowania działania. Zamiast dawać agentowi narzędzie takie jak `disable_account`, projekt może pozwolić mu na rekomendowanie: 

_Wymagana weryfikacja przez człowieka: wykryto oznaki naruszenia konta. Inżynier powinien sprawdzić, czy konieczne jest zablokowanie konta._

Podobnie, zamiast dawać agentowi narzędzie takie jak `close_alert`, projekt może pozwolić mu na rekomendowanie: 

_Zalecany priorytet: niski. Dowody wskazują, że można się spodziewać takiej aktywności skanera. Przed zamknięciem wymagana jest konsultacja z inżynierem._

Ten wzorzec sprawia, że ​​agent jest użyteczny, a jednocześnie zachowuje kontrolę człowieka: agent może rekomendować, ale decyzję podejmuje inżynier.

## Decyzja dotycząca granicy narzędzia

W przypadku tego pomieszczenia zatwierdzona granica narzędzi wynosi:

|Wewnątrz granicy agenta|Poza granicami agenta|
|---|---|
|`get_alert_details`|`disable_account`|
|`check_ip_reputation`|`close_alert`|
|`search_previous_notes`||
|`find_related_alerts`||

Granica ta zapewnia agentowi wystarczające możliwości wsparcia śledztwa, uniemożliwiając mu jednocześnie przeprowadzenie działań powstrzymujących lub zmianę zapisów śledztwa.

![Granice narzędzia agenta](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785359818051.png)

![Właściwe informacje we właściwym czasie](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785382797556.png)

Projekt agenta nie ogranicza się do tego, co potrafi. Musi on również definiować, co agent widzi, jakie informacje śledzi podczas wykonywania zadania i co pamięta z poprzednich zadań. Te trzy pojęcia są często mylone:

- **Kontekst** : informacje dostępne w trakcie bieżącego uruchomienia.
- **Stan** : informacje śledzone w miarę postępu przepływu pracy.
- **Pamięć** : informacja przechowywana lub odczytywana poza bieżącym przebiegiem.

Dla agenta dochodzeniowego ds. alertów bezpieczeństwa to rozróżnienie ma znaczenie. Agent może potrzebować wystarczających informacji do przeprowadzenia dochodzenia, ale nie powinien otrzymywać niepotrzebnych, poufnych danych, ukrywać ważnych szczegółów przepływu pracy ani traktować starych notatek jako automatycznie poprawnych.

_Bezpieczna konstrukcja zapewnia agentowi dostęp do właściwych informacji we właściwym czasie, a jednocześnie pozwala na śledzenie i przeglądanie śledztwa._

## Kontekst: Co agent widzi teraz

**Kontekst** to informacje przekazywane modelowi podczas konkretnego przebiegu. W przypadku NorthStar Fashion może to obejmować szczegóły bieżącego alertu, wyodrębnione encje, zatwierdzone wyniki dowodowe, istotne wcześniejsze notatki, powiązane alerty oraz wszelkie instrukcje ludzkie dotyczące dochodzenia. Dobry kontekst pomaga agentowi zrozumieć zadanie, ale nadmiarowy lub źle dobrany kontekst może stwarzać ryzyko. Niezwiązane dane pracowników, niepotrzebne logi lub nieaktualne notatki mogą sprawić, że agent będzie polegał na informacjach nieistotnych, wrażliwych lub wprowadzających w błąd.

W tym pomieszczeniu kontekst powinien ograniczać się do informacji niezbędnych do przeprowadzenia bieżącego dochodzenia. Projekt bezpiecznego kontekstu może obejmować:

- Szczegóły bieżącego alertu.
- Wyodrębnione jednostki.
- Zatwierdzone wyniki badań dowodowych.
- Ważne poprzednie uwagi.
- Powiązana oś czasu alertów.
- Instrukcje dla ludzi dotyczące bieżącego śledztwa.

Niewłaściwy projekt kontekstu może obejmować:

- Niezwiązane dane pracowników.
- Wszystkie historyczne dane dotyczące alertów.
- Do przeprowadzenia dochodzenia nie są potrzebne surowe logi systemowe.
- Informacje niepotwierdzone, bez ograniczeń.

_Celem nie jest dostarczenie modelowi wszystkich niezbędnych informacji. Chodzi o dostarczenie mu wystarczającej ilości istotnych informacji, aby uzyskać użyteczny i możliwy do zweryfikowania wynik._

## Stan: Co śledzi przepływ pracy

**Stan** to ustrukturyzowane informacje przekazywane w trakcie przepływu pracy podczas działania agenta.

W prostym przepływie pracy z szybką reakcją stan może nie być konieczny. Jednak  przepływy pracy związane z dochodzeniem zazwyczaj obejmują wiele kroków. Agent może pobrać szczegóły alertu, wyodrębnić jednostki, sprawdzić reputację, wyszukać notatki, znaleźć powiązane alerty, a następnie wygenerować rekomendację.

Bez państwa trudno jest odpowiedzieć na podstawowe pytania:

- Jakie dowody zostały sprawdzone?
- Które narzędzia zwróciły wyniki?
- Jakich informacji brakowało?
- Dlaczego agent zalecił recenzję ludzką?
- Jaki poziom ufności został przypisany?

Bezpieczny projekt agenta powinien uwzględniać widoczność tych informacji.

W przypadku NorthStar Fashion przydatne pola stanu mogą obejmować:

|   |   |   |   |   |
|---|---|---|---|---|
|`alert_id`|`alert_type`|`confidence`|`device`|`evidence_checked`|
|`final_summary`|`missing_evidence`|`recommended_priority`|`related_alerts`|`requires_human_review`|
|`severity`|`source_ip`|`timeline`|`timestamp`|`user`|

Stan ułatwia debugowanie, testowanie, audyt i wyjaśnianie przepływu pracy, pokazując, które dowody wpłynęły na każdą decyzję. Na przykład, jeśli agent rekomenduje wysoki priorytet, inżynier powinien być w stanie prześledzić tę rekomendację do dowodów ją potwierdzających. Projekt, który nie śledzi dowodów, pewności, brakujących informacji ani wymagań weryfikacji przez człowieka, tworzy ukryty stan i może generować wyniki, które wydają się wiarygodne, ale nie są odpowiednio wspierane.

## Pamięć: co można później ponownie wykorzystać

**Pamięć** to informacje przechowywane lub odczytywane po jednorazowym uruchomieniu. Może ona stanowić wsparcie dla dochodzenia, ujawniając, że adres IP należy do zatwierdzonego skanera, że ​​użytkownik wcześniej wywoływał podobne alerty lub że wcześniejsze dochodzenie zidentyfikowało niegroźną aktywność. Ponieważ jednak zapisy historyczne mogą być niekompletne, nieaktualne lub napisane inną terminologią, należy je traktować jako uzupełniający kontekst, a nie jako absolutną prawdę.

W tym przypadku pamięć powinna być zaprojektowana tak, aby **można było ją odczytywać w sposób kontrolowany z zatwierdzonych, poprzednich notatek** , a nie w sposób nieograniczony i długoterminowy.

Bezpieczna konstrukcja pamięci może umożliwić:

- Przeszukaj zatwierdzone notatki z poprzedniego śledztwa.
- Pobierz rekordy odnoszące się do bieżącego alertu.
- Pokaż źródło pobranych notatek.
- Oznacz notatki historyczne jako kontekst pomocniczy.
- Śledź ograniczenia, jeśli notatki mogą być nieaktualne lub niekompletne.

Niewłaściwa konstrukcja pamięci może powodować:

- Przechowuj wszystkie dane alertów bezterminowo.
- Wykorzystaj informacje o pracownikach, które nie mają związku z pracą.
- Traktuj poprzednie notatki jako zawsze poprawne.
- Pobieranie danych bez widoczności źródła.
- Używaj pamięci bez pokazywania ograniczeń.

Agent powinien ostrożnie korzystać z pamięci. Wcześniejsze notatki mogą pomóc w wyjaśnieniu kontekstu, ale aktualne dowody nadal wymagają analizy.

Kontekst, stan i pamięć wspólnie zapewniają, że agent dysponuje istotnymi informacjami, wyraźnie śledzi swoje śledztwo i wykorzystuje poprzednie zapisy wyłącznie jako dowody pomocnicze.

## Zasada projektowania: widoczność dowodów

Projekt kontekstu, stanu i pamięci powinien opierać się na następującej zasadzie:

_Przekaż agentowi wystarczającą ilość informacji, aby mógł on prowadzić śledztwo, ale zadbaj o to, aby dowody były widoczne._

Agent powinien otrzymywać wyłącznie istotne dane, utrzymywać widoczny stan i traktować pamięć jako kontekst pomocniczy, a nie automatycznie wiarygodne informacje. Każde istotne zalecenie powinno być powiązane z bieżącym kontekstem, zarejestrowanym stanem lub pobranymi dowodami.

![Kontekst, projekt i stan agentów IA](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785382797586.png)

![Nadzór ludzki i warunki zatrzymania](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785384921559.png)

Bezpieczna konstrukcja agenta definiuje nie tylko jego możliwości, ale także moment, w którym musi się zatrzymać. Jest to szczególnie ważne w procesach bezpieczeństwa, w których agent wspierający dochodzenie może gromadzić dowody, porównywać sygnały i rekomendować priorytety, ale powinien zatrzymać się, gdy dowody są niedostępne, sprzeczne lub wykraczają poza jego zakres. W NorthStar Fashion inżynier pozostaje odpowiedzialny za ostateczną decyzję: agent wspiera dochodzenie, nie zastępując ludzkiego osądu. Nadzór ludzki i jasne warunki zatrzymania utrzymują zatem agenta w wyznaczonych granicach.

## Problem autonomii

Agenci są przydatni, ponieważ mogą podejmować decyzje w trakcie wykonywania zadania — takie jak wybór narzędzia, sprawdzenie jego wyników, aktualizacja stanu i określenie następnego kroku — jednak ta sama elastyczność wiąże się również z ryzykiem.

Jeżeli agentowi nie zostaną podane jasne limity, może on:

- Próbuj ponownie, gdy dowody nie są dostępne.
- Traktuj brakujące dowody jako bezpieczne.
- Zignoruj ​​sprzeczne wyniki.
- Udzielaj pewnych odpowiedzi bez wsparcia.
- Zalecać działania wykraczające poza jego kompetencje.
- Kontynuuj pracę poza pierwotnym zakresem

Dobrze zaprojektowany agent nie powinien podejmować próby wykonania zadania za wszelką cenę; gdy dowody są niewystarczające, ryzyko jest zbyt wysokie lub sytuacja wymaga ludzkiej oceny, najbezpieczniejszym działaniem jest zatrzymanie się i poproszenie o ocenę przez człowieka.

## Co oznacza nadzór ludzki

![Nadzór ludzki](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785384921407.png)

Nadzór ludzki oznacza, że ​​jedna osoba pozostaje odpowiedzialna za przeglądanie wyników pracy agenta i podejmowanie ostatecznej decyzji. Nie oznacza to jednak, że agent jest mniej użyteczny: nadal może ograniczyć nakład pracy ręcznej poprzez gromadzenie dowodów, porządkowanie kontekstu, identyfikowanie brakujących informacji i przygotowywanie ustrukturyzowanego podsumowania. Kluczowa różnica polega na tym, że agent wspiera proces decyzyjny, podczas gdy inżynier zachowuje odpowiedzialność za decyzję.

W przypadku NorthStar Fashion agent może powiedzieć:

_Powiązane alerty i dane dotyczące reputacji sugerują, że ten alert może wymagać wyższego priorytetu. Przed podjęciem jakichkolwiek działań zaradczych wymagana jest weryfikacja przez człowieka._

Ale nie może powiedzieć:

_To jest złośliwe. Konto zostało wyłączone._

Pierwsza odpowiedź wspomaga proces decyzyjny inżyniera, druga natomiast wykonuje – lub implikuje – działanie wykraczające poza zakres zamierzony przez agenta.

## Punkty przeglądu ludzkiego

Punkt przeglądu przez człowieka to stan, który wymaga zaangażowania inżyniera, aby przepływ pracy mógł być kontynuowany lub aby dane wyjściowe agenta mogły zostać zaakceptowane. W tym projekcie przegląd przez człowieka powinien być wymagany, gdy:

- Brakuje dowodów.
- Dowody są sprzeczne.
- Alert może oznaczać naruszenie bezpieczeństwa konta.
- Zalecany priorytet to wysoki lub krytyczny.
- Agent ma niskie zaufanie.
- Wymagane źródło jest niedostępne.
- Agent nie potrafi wyjaśnić swojej rekomendacji

Te warunki mają znaczenie, ponieważ nieuzasadnione lub zautomatyzowane wnioski mogą stwarzać zagrożenie dla bezpieczeństwa lub firmy. Na przykład, jeśli źródło reputacji IP jest niedostępne, agent nie powinien zakładać, że IP jest bezpieczne; powinien zarejestrować dowód jako brakujący i zlecić weryfikację przez człowieka. Podobnie, jeśli powiązane alerty wskazują na możliwe naruszenie bezpieczeństwa konta, agent powinien przekazać sprawę inżynierowi, zamiast wyłączać samo konto.

## Warunki zatrzymania

Warunek zatrzymania informuje agenta, kiedy musi zatrzymać przepływ pracy zamiast automatycznie go kontynuować. Warunki zatrzymania różnią się od punktów kontroli dokonywanych przez człowieka, ale często działają razem.

W punkcie recenzji ludzkiej napisano:

_Osoba musi to przejrzeć._

Warunek zatrzymania oznacza:

_Agent nie może kontynuować pracy poza tym punktem._

W przypadku NorthStar Fashion agent powinien zakończyć współpracę, gdy:

- Wymaganych dowodów nie można odzyskać.
- Powtarzające się błędy narzędzi.
- Dowody są sprzeczne.
- Żądanie wykracza poza zakres.
- Osiągnięto maksymalną liczbę ponownych prób.
- Wymagana jest recenzja człowieka.
- Agent nie ma wystarczających dowodów, aby poprzeć rekomendację

Zapobiega to zgadywaniu przez agenta, nieskończonemu wykonywaniu operacji lub tworzeniu rekomendacji, która wydaje się pewniejsza, niż pozwalają na to dowody.

## Limity ponownych prób

Ponowne próby mogą pomóc w odzyskaniu sprawności po tymczasowych awariach narzędzia, takich jak przekroczenie limitu czasu podczas sprawdzania reputacji adresów IP, ale muszą mieć jasno określone limity. Bez limitu ponownych prób agent może tracić czas, zwiększać koszty, zapełniać logi powtarzającymi się błędami i opóźniać ręczne sprawdzenie alertu przez inżyniera.

Bezpieczniejszy wzór to:

_Wypróbuj zatwierdzone narzędzie. Jeśli narzędzie zawiedzie, spróbuj ponownie ograniczoną liczbę razy. Jeśli narzędzie nadal będzie zawodzić, oznacz dowody jako niedostępne. Zatrzymaj lub poproś o weryfikację przez człowieka._

Agent nie powinien nigdy ponawiać prób w nieskończoność.

## Niepewność jest słusznym wynikiem

Niebezpieczny projekt zakłada, że ​​agent zawsze musi podać ostateczną odpowiedź, podczas gdy bezpieczniejszy projekt pozwala mu potwierdzić odpowiedź, gdy dostępne dowody są niekompletne.

Na przykład:

_Nie udało się nawiązać połączenia ze źródłem reputacji IP. Znaleziono powiązane alerty, ale brakuje dowodów reputacji. Przed nadaniem ostatecznego priorytetu wymagana jest weryfikacja przez człowieka._

Jest to bezpieczniejsze niż wymyślanie wniosków lub traktowanie niedostępnego źródła jako dowodu na brak ryzyka. W procesach bezpieczeństwa niepewność powinna pozostać widoczna, dlatego ostateczny wynik powinien jasno wskazywać brakujące dowody, znane ograniczenia, poziom ufności oraz wszelkie wymagania dotyczące weryfikacji przez człowieka.

## Zachowanie bezpieczne i niebezpieczne

|Sytuacja|Niebezpieczne zachowanie|Bezpieczniejsze zachowanie|
|---|---|---|
|Niedostępne źródło reputacji IP|Traktuj adres IP jako bezpieczny|Oznacz dowód jako brakujący|
|Konflikt powiązanych alertów|Wybierz jeden wynik bez wyjaśnienia|Wymagaj przeglądu przez człowieka|
|Zalecenie wysokiego ryzyka|Działaj automatycznie|Wyślij do przeglądu inżynierskiego|
|Narzędzie ciągle zawodzi|Ponawiaj w nieskończoność|Zatrzymaj po limicie ponownych prób|
|Zakres jest niejasny|Kontynuuj mimo wszystko|Zatrzymaj się i poproś o wyjaśnienie|
|Dowody są słabe|Wyciągnij pewne wnioski|Uwzględnij ograniczenia|

Agent powinien być zaprojektowany tak, aby awaria przebiegała bezpiecznie. Bezpieczna awaria to taka, w której agent zatrzymuje się, wyjaśnia, co się stało i prosi o weryfikację, zamiast kontynuować działanie w oparciu o niepoparte założenia.

## Zasada projektowania: Bezpieczne zatrzymanie

Nadzór ludzki i warunki zatrzymania powinny opierać się na następującej zasadzie:

_Agent może poprzeć dochodzenie, ale musi je przerwać, gdy dowody nie będą już pozwalały na bezpieczne kontynuowanie śledztwa._

Zasada ta wyraźnie określa granice autonomii agenta: może on zbierać i porządkować informacje, ale nie może działać w ciemno, ukrywać niepewności ani podejmować ostatecznych decyzji dotyczących bezpieczeństwa.

![Zbieraj, organizuj informacje i bezpiecznie zatrzymuj](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785384921475.png)

Agent wspierający śledztwo nie powinien odsyłać jedynie akapitu. Powinien sporządzić spójny, ustrukturyzowany raport z przeglądu, który przedstawia ustalenia, wykorzystane dowody, brakujące informacje i uzasadnienie rekomendacji.

Na przykład odpowiedź niestrukturyzowana może brzmieć następująco:

_„To ostrzeżenie jest prawdopodobnie złośliwe i należy je zgłosić”._

Brzmi to użytecznie, ale pozostawia bez odpowiedzi ważne pytania. Inżynier nie może łatwo sprawdzić, które źródła zostały sprawdzone, czy jakieś narzędzia zawiodły, jakie dowody potwierdzają wniosek ani co oznacza słowo „prawdopodobnie”.

Ustrukturyzowane dane wyjściowe rozdzielają te szczegóły na zdefiniowane pola. Ułatwia to inżynierowi przeglądanie wyników i pozwala systemowi zweryfikować, czy wymagane informacje są obecne przed zaakceptowaniem danych wyjściowych.

## Stan i wyjście są różne

Stan i wynik mogą zawierać pewne wspólne informacje, ale służą różnym celom.

- **Stan**  to dokumentacja robocza przechowywana podczas trwania dochodzenia. Może obejmować wyodrębnione jednostki, pośrednie wyniki narzędzia, liczniki ponownych prób, brakujące dowody oraz kolejny planowany krok.
- **Wynikiem**  jest ostateczny pakiet recenzji przekazywany inżynierowi. Powinien on zawierać dowody, ograniczenia, zalecenia i status recenzji niezbędne do zrozumienia wyniku bez ujawniania zbędnych szczegółów wewnętrznych.

Agent może wykorzystać stan do osiągnięcia wyniku, ale ostateczny wynik musi zostać zaprojektowany jako oddzielny i niezawodny kontrakt.

## Wymagane pola wyjściowe

W przypadku NorthStar Fashion ustrukturyzowane dane wyjściowe mogą zawierać następujące pola:

|Pole|Zamiar|
|---|---|
|`alert_id`|Identyfikuje alert, który jest badany|
|`run_status`|Pokazuje, czy dochodzenie zostało ukończone lub bezpiecznie przerwane|
|`summary`|Zawiera zwięzły opis ustaleń|
|`extracted_entities`|Wyświetla listę odpowiednich użytkowników, adresów IP, urządzeń i znaczników czasu|
|`evidence`|Rejestruje ustalenia wraz z ich źródłami i ograniczeniami|
|`related_alert_timeline`|Pokazuje powiązane wydarzenia w kolejności chronologicznej|
|`contradictions`|Identyfikuje dowody, które nie są zgodne|
|`missing_evidence`|Identyfikuje dowody, których nie można było uzyskać|
|`recommended_priority`|Podaje sugerowany priorytet dochodzenia lub `undetermined`|
|`recommendation_rationale`|Wyjaśnia, w jaki sposób dowody potwierdzają zalecenie|
|`requires_human_review`|Uwidacznia obowiązkowy przegląd inżynierski|
|`stop_reason`|Wyjaśnia, dlaczego agent zatrzymał się, gdy nie mógł normalnie zakończyć działania|

Każdy dowód powinien również zawierać informacje o swoim pochodzeniu. Powinien on co najmniej wskazywać źródło lub narzędzie, z którego dokonano odkrycia, datę uzyskania informacji oraz wszelkie znane ograniczenia.

Na przykład:

```json
{
  "source": "check_ip_reputation",
  "finding": "The source IP has recent malicious reports",
  "retrieved_at": "2026-07-24T09:30:00Z",
  "limitations": []
}
```

Takie podejście jest łatwiejsze do weryfikacji niż umieszczanie ustaleń w podsumowaniu bez podawania źródła.

## Użyj kontrolowanych wartości

Niektóre pola wyjściowe powinny używać niewielkiego zestawu dozwolonych wartości. Wartości kontrolowane zapobiegają tworzeniu przez agenta niespójnych etykiet, takich jak „dość pilne” lub „średnio-wysokie”.

W przypadku tego projektu,  `run_status` powinien to być jeden z:

- `ready_for_review` - Śledztwo zostało zakończone, a pakiet przeglądowy jest gotowy dla inżyniera.
- `needs_human_input` - Agent potrzebuje informacji lub decyzji, aby móc kontynuować.
- `insufficient_evidence` - Gromadzenie ograniczonych dowodów zostało zakończone bez wystarczającego poparcia dla rekomendacji.
- `tool_failure` - Wymagane źródło dowodów pozostało niedostępne po upływie limitu ponownych prób.
- `out_of_scope` - Prośba nie mieści się w ramach wsparcia dochodzenia.

`recommended_priority` powinno być jedno z:

- `low`
- `medium`
- `high`
- `critical`
- `undetermined`

Agent musi korzystać z tej funkcji  `undetermined` , gdy dostępne dowody nie potwierdzają priorytetowej rekomendacji. Nie może po prostu zgadywać, aby uzupełnić pole.

## Przykładowy wynik końcowy

Poniższy przykład przedstawia ukończone dochodzenie gotowe do przeglądu przez inżyniera:

```json
{
  "alert_id": "ALERT-1042",
  "run_status": "ready_for_review",
  "summary": "The source IP has a malicious reputation and appears in related alerts involving the same user",
  "extracted_entities": {
    "users": ["user-17"],
    "source_ips": ["203.0.113.24"],
    "devices": ["device-08"]
  },
  "evidence": [
    {
      "source": "check_ip_reputation",
      "finding": "The source IP has recent malicious reports",
      "retrieved_at": "2026-07-24T09:30:00Z",
      "limitations": []
    }
  ],
  "related_alert_timeline": [
    "09:10 - Unusual-location login",
    "09:20 - External mail-forwarding rule created"
  ],
  "contradictions": [],
  "missing_evidence": [],
  "recommended_priority": "high",
  "recommendation_rationale": "The reputation result and related account activity provide consistent indicators of possible account compromise",
  "requires_human_review": true,
  "stop_reason": null
}
```

Zalecenie pozostaje doradcze. Dane wyjściowe nie wskazują, że konto zostało wyłączone, alert zamknięty ani że wykonano jakąkolwiek inną akcję reagowania.

## Bezpiecznie przedstaw brakujące dowody

Ustrukturyzowane wyniki muszą również wspierać niekompletne dochodzenia. Awaria narzędzia lub luka w dowodach nie upoważniają do wymyślania wyników.

Na przykład:

```json
{
  "alert_id": "ALERT-1043",
  "run_status": "insufficient_evidence",
  "summary": "Related alerts were found, but an approved reputation result could not be retrieved",
  "extracted_entities": {
    "users": [],
    "source_ips": ["198.51.100.18"],
    "devices": []
  },
  "evidence": [],
  "related_alert_timeline": [],
  "contradictions": [],
  "missing_evidence": [
    "IP reputation result was unavailable after the retry limit"
  ],
  "recommended_priority": "undetermined",
  "recommendation_rationale": "The available evidence does not support a reliable priority recommendation",
  "requires_human_review": true,
  "stop_reason": "Required evidence remained unavailable"
}
```

Dane wyjściowe są nadal przydatne, ponieważ informują inżyniera o tym, co zostało podjęte, czego brakuje i dlaczego agent się zatrzymał.

## Pewność siebie wymaga definicji

Pola ufności nie należy uwzględniać tylko dlatego, że agent może je wygenerować. Procent wygenerowany przez model może wydawać się precyzyjny, jeśli nie jest skalibrowany ani obsługiwany.

Jeśli projekt wykorzystuje pewność, musi definiować sposób określania wartości oraz jej związek z kompletnością dowodów, wiarygodnością źródeł i sprzecznościami. W przeciwnym razie projekt powinien wskazywać niepewność poprzez  `missing_evidence`,  `contradictions`,  `run_status`i  `recommended_priority` .

Pewność siebie nigdy nie może zastąpić dowodów.

## Sprawdź poprawność danych wyjściowych

Przed zaakceptowaniem wyniku system powinien sprawdzić, czy:

- Wszystkie wymagane pola są obecne.
- Pola kontrolowane zawierają tylko dozwolone wartości.
- Każde ważne odkrycie zawiera informację o źródle dowodów.
- Widoczne są brakujące i sprzeczne dowody.
- `requires_human_review` jest zawsze  `true`.
- `undetermined` Zamiast zgadywania stosuje się nieobsługiwaną rekomendację  .
- Zatrzymany bieg obejmuje wyczyszczenie  `stop_reason`.
- W wynikach nie stwierdzono, że podjęto działania mające na celu powstrzymanie, naprawę, zamknięcie alertu lub inne zabronione działania.

Dzięki tym kontrolom wyniki są bardziej spójne, a ryzyko, że do inżyniera dotrze wynik wyglądający na pewny, ale niekompletny, jest mniejsze.

## Zasada projektowania: Możliwość przeglądu wyników

Ustrukturyzowany wynik powinien być zgodny z następującą zasadą:

_Zalecenia agenta muszą być zgodne z dowodami, jasno określać ograniczenia i przedstawiać je w formacie, który inżynier będzie mógł wiarygodnie przejrzeć._

Bezpieczne wyjście nie ukrywa niepewności ani nie sugeruje, że to agent podjął ostateczną decyzję dotyczącą bezpieczeństwa. Daje inżynierowi jasny pakiet dochodzeniowy i zachowuje odpowiedzialność człowieka.

Przejrzałeś już kluczowe obszary projektowe niezbędne do zapewnienia bezpieczeństwaSztuczna inteligencja-agent śledczy wspomagający:

- Rola i zakres
- Granica narzędzia
- Kontekst, stan i pamięć
- Przegląd ludzki i warunki zatrzymania
- Ustrukturyzowane wyjście

W tym ostatnim zadaniu zastosujesz te zasady w narzędziu **Agent Spec Builder** , tworząc bezpieczną i kompletną specyfikację agenta dla NorthStar Fashion przed rozpoczęciem implementacji. Nie jest to zadanie programistyczne, lecz wyzwanie projektowe, w którym musisz określić, które opcje należą do specyfikacji, a które wprowadziłyby niebezpieczną autonomię.

## Kreator specyfikacji agentów

Firma NorthStar Fashion chce, aby agent wspomagany sztuczną inteligencją wspierał dochodzenia w sprawie alertów bezpieczeństwa poprzez gromadzenie zatwierdzonych dowodów, korelowanie odpowiedniego kontekstu, przygotowywanie ustrukturyzowanego podsumowania i rekomendowanie priorytetu dochodzenia do weryfikacji przez człowieka. Agent musi jednak pozostawać w wyznaczonych granicach i nie może:

- Wykonaj powstrzymywanie
- Modyfikuj systemy
- Automatyczne zamykanie alertów
- Wyłącz konta
- Blokuj adresy IP
- Wymyśl brakujące dowody
- Ukryj niepewność
- Kontynuuj, gdy dowody są niewystarczające
- Podejmij ostateczne decyzje dotyczące bezpieczeństwa

Inżynier pozostaje odpowiedzialny za przejrzenie dowodów i podjęcie decyzji, co należy zrobić dalej.

## Zasada projektowania: kompletna i bezpieczna specyfikacja

Projekt jest gotowy tylko wtedy, gdy rola agenta, narzędzia, kontekst, stan, pamięć, punkty kontroli przez człowieka, warunki zatrzymania i dane wyjściowe są kompletne, odpowiednio określone i bezpieczne. Kompletność oznacza, że ​​każda wymagana część specyfikacji jest zdefiniowana, natomiast bezpieczeństwo oznacza, że ​​agent nie ma uprawnień wykraczających poza wsparcie w zakresie dochodzenia. Kompletny, ale niebezpieczny projekt nie jest gotowy – na przykład może definiować narzędzia, stan i dane wyjściowe, jednocześnie umożliwiając agentowi wyłączanie kont lub zamykanie alertów. Podobnie, bezpieczny, ale niekompletny projekt nie jest gotowy, jeśli unika działań powstrzymujących, ale nie definiuje warunków zatrzymania, punktów kontroli przez człowieka ani wymaganych pól danych wyjściowych.

Ostateczna specyfikacja musi spełniać obydwa warunki:

- Uwzględnij wymagane obszary projektowe
- Odrzuć niebezpieczną autonomię

## Live Agent Specification

Role & Scope

- Assist the engineer with security-alert investigations
- Gather approved evidence and correlate relevant context
- Recommend investigation priority for human review

Tools

- search_previous_notes
- check_ip_reputation
- get_alert_details
- find_related_alerts

Context / State

- Use approved previous notes through search
- Track evidence checked and missing evidence in state
- Track confidence and whether human review is required
- Use current alert details as context

Oversight

- Stop when required evidence cannot be retrieved
- Stop when the request is outside scope
- Request human review for high-risk recommendations
- Request human review when evidence is missing or contradictory

Output

- Include confidence, limitations, and missing evidence
- Include whether human review is required
- Include alert ID, summary, and extracted entities
- Include supporting evidence and related events

Validation Panel

Design validated. The agent specification is safe and complete.

Zakończyłeś fazę projektowania  **agenta śledczego NorthStar Fashion Security** !

W tym pokoju dowiedziałeś się, że sukces Sztuczna inteligencja Agenci są definiowani nie przez używany przez nich model językowy, ale przez decyzje, które kształtują sposób ich działania. Dobrze zaprojektowany agent rozpoczyna pracę z jasno określonym celem, pozostaje w określonym zakresie, używa tylko niezbędnych narzędzi, utrzymuje odpowiedni kontekst i stan oraz wie, kiedy przerwać i zaangażować człowieka. Te wybory decydują o tym, czy agent stanie się niezawodnym asystentem, czy nieprzewidywalnym źródłem ryzyka.

![Następnym krokiem jest wdrożenie](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1785385569944.png)
