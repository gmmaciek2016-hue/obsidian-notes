---

To już koniec. Na szczęście byliśmy na to przygotowani, ale w końcu się stało. W końcu mamy do czynienia z cyberkryzysem! Teraz nie czas na bezczynność, musimy działać, aby uratować naszą organizację! Na szczęście mamy Zespół Zarządzania Kryzysowego (CMT), którego zadaniem jest właśnie przeprowadzenie nas przez te wzburzone wody!

W tej sali dowiemy się, czym jest zarządzanie kryzysowe i w jaki sposób zespół CMT może przejąć inicjatywę, aby pomóc organizacji bezpiecznie wyjść z cyberkryzysu.

Wymagania wstępne

- [Wprowadzenie do reagowania na incydenty i zarządzania nimi](https://tryhackme.com/jr/introtoirandim)
- [Rejestrowanie w celu rozliczeń i monitorowania](https://tryhackme.com/room/loggingforaccountability)
- [Zostanie ratownikiem medycznym](https://tryhackme.com/jr/becomingafirstresponder)  

Cele edukacyjne

- Jak CMT radzi sobie z kryzysem cybernetycznym
- Złota godzina podczas CMT i jak ważne mogą być nawet minuty
- Proces CMT i jak inżynierowie ds. bezpieczeństwa mogą pełnić rolę ekspertów przedmiotowych

Czym jest kryzys cybernetyczny?  

[W sali](https://tryhackme.com/room/introtoirandim) „Wprowadzenie do reagowania na incydenty i zarządzania nimi” omówiliśmy, co stanowi incydent cybernetyczny. SOC Otrzymuje informacje z dziennika, które generują zdarzenia i alerty. W przypadku, gdy alert jest wystarczająco poważny, dochodzi do cyberincydentu.

Jednakże biorąc pod uwagę powagę incydentu, niebieski zespół decyduje o najlepszej reakcji. W naszym przykładzie tylko incydent poziomu 4 spowodowałby uruchomienie **Zespołu Zarządzania Kryzysowego (CMT)** . Dla przypomnienia, były to cztery poziomy:

- **Poziom 1:SOCIncydent** – ​​na tyle niewielki, że może nim zająć się bezpośrednio centrum operacji bezpieczeństwa (SOC), na przykład użytkownik zgłaszającyphishinge-mail
- **Poziom 2: Incydent CERT** – na tyle mały, że zespół wSOCmoże zająć się incydentem, takim jak pojedynczy użytkownik, który wszedł w interakcję zphishinge-mail
- **Poziom 3: Incydent CSIRT** – większy incydent, który wymaga nie tylkoSOCzespół, ale także menedżerowie ds. incydentów, np. wielu użytkowników, którzy wchodzili w interakcje zphishinge-mail zawierający złośliwe oprogramowanie
- **Poziom 4: Incydent CMT** – krytyczny incydent, w którym zespół CSIRT musi mieć możliwość podjęcia działań nuklearnych, np. incydent, w którym wdrażane jest oprogramowanie ransomware, a zespół CSIRT musi wyłączyć środowisko w celu ochronyodpoczynekmajątku  

Jak więc zespół faktycznie określa poziom incydentu? Odbywa się to za pomocą macierzy klasyfikacji ważności incydentów, jak pokazano poniżej:

![Skala ciężkości CMT](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/d54b1bd910019fc66fba7413c5b510d7.svg)  

Chociaż jest to przykład, większość metod klasyfikacji ważności incydentów opiera się na mierzeniu zakresu incydentu w stosunku do liczby systemów lub użytkowników, których dotyczy problem, oraz trudności w odzyskaniu dotkniętych nim systemów i zasobów. Dlatego też, jeśli wielu użytkowników jest dotkniętych problemem w systemie krytycznym, zazwyczaj skutkuje to oceną incydentu jako krytycznego, co skutkuje interwencją zespołu CMT. Niektóre organizacje dodają również pewne specjalne reguły do ​​swojej macierzy ważności. Na przykład, jeśli problem dotyczy określonej liczby klientów, ważność incydentu jest oceniana jako krytyczna.

Nie wszystkie głosy są równe  

W CMT istnieje kilka ról i obowiązków, które należy spełnić. Zazwyczaj nie wszyscy członkowie CMT są zaangażowani od samego początku. W zależności od sytuacji kryzysowej, członkowie są dodawani w razie potrzeby. Ma to na celu zapewnienie jak najszybszej reakcji CMT.

Podczas gdy w większości przypadków demokracja jest najlepszym rozwiązaniem, aby zapewnić wysłuchanie głosu każdego, w przypadku CMT sytuacja jest odwrotna. Autokracja to najlepsze podejście dla CMT, aby zapewnić zdecydowane podejmowanie działań bez marnowania cennego czasu. Zazwyczaj odpowiedzialność ta spoczywa na prezesie. To dość skrajne podejście i aby podzielić się odpowiedzialnością za podejmowanie decyzji, niektóre CMT przyznają prawo głosu kluczowym osobom, zazwyczaj nie więcej niż pięciu. Zatem, chociaż nadal jest to niewielki zespół, który może wnioskować o podjęcie działań, odpowiedzialność nie spoczywa już tylko na jednej osobie.

Role w CMT

Poniższa tabela przedstawia szczegółowo niektóre role i obowiązki, jakie można spotkać w typowym CMT:

|                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Rola/Obowiązki**    | **Opis**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Przewodniczący CMT    | Przewodniczący to osoba kierująca zespołem CMT. Zazwyczaj rolę tę pełni prezes lub dyrektor operacyjny organizacji. Przewodniczący jest odpowiedzialny za kierowanie zespołem CMT i, jak wspomniano wcześniej, zazwyczaj ma decydujący głos w kwestii działań, które zostaną wdrożone w czasie cyberkryzysu.                                                                                                                                                                                                                                                                                        |
| Kadra kierownicza     | Kadra kierownicza zazwyczaj stanowi część CMT. Należą do niej dyrektor generalny, dyrektor operacyjny, dyrektor ds. informatyki,Dyrektor techniczny, CFO, a nawet CISO. W przypadkach, gdy nie tylko CEO jest odpowiedzialny za podejmowanie decyzji, każdemu z tych dyrektorów zostanie przyznane prawo głosu. Ponieważ to właśnie dyrektorzy będą ostatecznie pociągnięci do odpowiedzialności za to, co wydarzyło się podczas incydentu, są oni zaangażowani w proces CMT, aby zapewnić, że szkody będą jak najmniejsze.                                                                         |
| Komunikacja           | Ważnym zadaniem w CMT jest komunikacja. Obejmuje ona komunikację zarówno wewnętrzną, jak i zewnętrzną, kierowaną do pracowników i klientów. Ważnym elementem każdego CMT jest kontrolowanie narracji, aby zapobiec wywoływaniu niepotrzebnej paniki. Dlatego komunikacja w czasie cyberkryzysu jest niezwykle istotna.                                                                                                                                                                                                                                                                              |
| Prawny                | Choć chcielibyśmy wierzyć, że CMT może podjąć dowolne działania, ważne jest, aby upewnić się, że są one zgodne z prawem. Bardzo częstym tematem dyskusji podczas niektórych scenariuszy cyberkryzysów jest to, czy zostanie zapłacony okup, czy też zespół będzie współpracował z atakującymi. Należy zauważyć, że w niektórych krajach takie działania mogą być dla zespołu nielegalne.                                                                                                                                                                                                            |
| Operacje              | Jednym z wyłącznych obowiązków członków CMT jest dbanie o jak najlepsze podejście, aby zapewnić jak najmniejszy wpływ cyberkryzysu na działalność organizacji. W niektórych przypadkach rolę tę pełni dyrektor operacyjny (COO); może ją jednak również pełnić cały zespół ekspertów, którzy poszukują sposobów na kontynuację działalności w czasie kryzysu.                                                                                                                                                                                                                                       |
| Eksperci przedmiotowi | Większość członków CMT nie ma wykształcenia technicznego. Są to osoby, które doskonale radzą sobie z problemami biznesowymi, ale zazwyczaj nie przejmują się codziennymi zawiłościami faktycznego zarządzania systemami organizacji. Podczas cyberkryzysu eksperci merytoryczni (SME) odgrywają kluczową rolę w dostarczaniu kluczowych informacji członkom CMT. Informacje te pomagają następnie zespołowi określić skalę kryzysu i wskazać, jakie działania najlepiej podjąć. Podczas cyberkryzysu najprawdopodobniej będzie to obejmować kierownika ds.SOCi/lub kierownika ds. incydentów CSIRT. |
| Uczony w piśmie       | Sporządzanie notatek jest niezwykle ważne podczas cyberkryzysu. Stworzenie pełnej osi czasu zdarzeń jest niezwykle istotne, ponieważ często musi ona zostać ujawniona stronom trzecim, takim jak rząd czy organy regulacyjne. Rolą osoby sporządzającej notatki jest zatem szczegółowe opisanie wszystkich zdarzeń i rozmów podczas sesji CMT.                                                                                                                                                                                                                                                      |

Pierwsza godzina, w której uruchamiany jest CMT, jest jedną z najważniejszych. Podobnie jak w każdym śledztwie, wraz z upływem czasu, odtworzenie tego, co się wydarzyło i wyjście z tego stanu rzeczy staje się trudniejsze. Nazywamy to Złotą Godziną. Podczas Złotej Godziny CMT musi wykonać kilka kluczowych kroków.

Montaż

Pierwszym krokiem w Złotej Godzinie jest powołanie Zespołu ds. Zarządzania Kryzysowego (CMT). Gdy zespół CSIRT zdecyduje się na powołanie CMT, należy wdrożyć procedurę powiadamiania wszystkich początkowych członków CMT o konieczności udzielenia pomocy w przypadku cyberkryzysu. Zazwyczaj w tym celu tworzy się podręcznik i schemat połączeń. Jest to niezwykle ważne, ponieważ niektórzy z wymaganych członków mogą być niedostępni (na przykład dyrektor operacyjny może utknąć w nocnym locie). Dlatego ich zastępstwo i zastępstwo zastępcy powinny być już udokumentowane.

Zazwyczaj przewodniczący zespołu CSIRT jest odpowiedzialny za uruchomienie CMT, a następnie za wstępne powiadomienie. Następnie kilku członków zespołu może pomóc w zorganizowaniu CMT. Zespół powinien również zdecydować, czy zbierze się zdalnie, czy osobiście, oraz jakie kanały komunikacji będą wykorzystywane. Choć decyzja ta może wydawać się prosta, często okazuje się trudniejsza, niż mogłoby się wydawać. Zespół CSIRT może mieć uzasadnione podejrzenie, że jego główne kanały komunikacji zostały naruszone przez atakującego i dlatego konieczna będzie komunikacja poza pasmem (out-of-band).  

Gromadzenie informacji

Po utworzeniu zespołu CMT, pierwszym krokiem jest zrozumienie, co się wydarzyło i jakie działania należy podjąć natychmiast. W przypadku cyberkryzysu odbywa się to zazwyczaj w formie briefingu CSIRT, podczas którego zespół CSIRT zapewnia:

- Podsumowanie informacji odkrytych do tego momentu
- Podsumowanie działań, które zostały już podjęte przez zespół i ich wpływu na incydent
- Zalecenia dotyczące działań nuklearnych, które CMT powinien podjąć natychmiast

Triage kryzysowy

Po odprawie CMT, ważne jest, aby zespół dokonał wstępnej selekcji incydentu i rozważył działania zaproponowane przez CSIRT. CMT powinien dokładnie przemyśleć wpływ, jaki działania te będą miały na organizację, i już teraz zastanowić się nad krokami, które można podjąć, aby ograniczyć ten wpływ. Podczas tej fazy selekcji zespół zdecyduje również, którzy inni interesariusze powinni zostać zaangażowani w CMT.  

Powiadomienia

Jak wspomniano wcześniej, kontrolowanie narracji jest niezwykle ważne. W związku z tym, jednym z pierwszych kroków, które zespół CMT powinien wykonać już podczas Złotej Godziny, jest przygotowanie, a w niektórych przypadkach wysłanie komunikatów, zarówno wewnętrznych, jak i zewnętrznych. Zazwyczaj zespół CMT przygotowuje się, korzystając z komunikatów o charakterze „holding statement”. Są to komunikaty, które nie ujawniają dokładnie, co się dzieje, ale dają pewność, że zespół bada sprawę i przekaże więcej informacji zwrotnych w miarę ich pojawiania się. Może to pomóc uspokoić sytuację, ponieważ interesariusze wiedzą, że zespół pracuje nad danym problemem.

Po ustanowieniu CMT i przeprowadzeniu działań Złotej Godziny, CMT rozpoczyna cykliczny proces radzenia sobie z kryzysem, jak pokazano poniżej.

![Proces CMT](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/71572f39d5d25f6a66d26a11cdcd2192.svg)  

Należy zauważyć, że przez cały proces zespół CMT pozostaje statyczny. Zamiast odłączać członków głównego zespołu CMT i szukać informacji, MŚP są wykorzystywane do dostarczania informacji zespołowi CMT. Wynika to z faktu, że gdyby zespół CMT odłączył się w krytycznym momencie, ponowne jego utworzenie byłoby stratą czasu. Ten model gwarantuje, że zespół CMT zawsze otrzymuje kluczowe informacje od interesariuszy i MŚP.  

Aktualizacje informacji

Zespół ds. Zarządzania Kryzysowego (CMT) otrzymuje aktualizacje od różnych interesariuszy. Zazwyczaj odbywa się to w formie briefingów z MŚP. Celem jest dostarczenie zespołowi CMT nowych informacji, aby lepiej zrozumieć skalę kryzysu i wpływ podjętych w przeszłości działań na kryzys. Zespół CMT decyduje, jak często odbywają się te sesje aktualizacyjne. Na początku kryzysu aktualizacje te często odbywają się częściej.

Jak wspomniano wcześniej, CMT zazwyczaj składa się z członków o mniejszym doświadczeniu technicznym. Dlatego ważne jest, aby MŚP przekazywały informacje o aktualizacjach w sposób zrozumiały dla CMT. Zazwyczaj informacje techniczne są w aktualizacjach abstrakcyjne, a nacisk kładziony jest bardziej na skutki tego, co się wydarzyło, niż na to, co faktycznie się wydarzyło.  

Ocena stanu zdrowia rannych

Po otrzymaniu nowych informacji przez zespół, proces triażu musi zostać powtórzony. Na tym etapie CMT decyduje, czy należy zwiększyć, czy zmniejszyć skalę kryzysu oraz czy w CMT należy zaangażować nowe MŚP. CMT musi również zdecydować, czy zostaną wysłane nowe komunikaty wewnętrzne i zewnętrzne.  

Dyskusje o działaniach

Korzystając z nowych informacji dostarczonych przez różne MŚP, CMT musi omówić proponowane działania. Celem tych dyskusji jest zrozumienie wpływu, jaki te działania będą miały na organizację. W tym przypadku nie mówimy już o łatwych i drobnych działaniach, takich jak usunięciephishingwiadomości ze skrzynki pocztowej użytkownika. Mamy na myśli duże akcje, takie jak:

- Ograniczanie zdalnego dostępu do środowiska poprzez zatrzymanie wszystkichVPNdostęp
- Wykonywanie operacji odzyskania domeny usługi Active Directory
- Przełączanie systemu do środowiska odzyskiwania po awarii

Są to działania, których CMT nie może podjąć lekkomyślnie, ponieważ wpłynęłyby one na działalność firmy. Celem dyskusji jest lepsze zrozumienie tego wpływu i umożliwienie zespołowi określenia, czy istnieją jakieś mniej istotne, ale nadal skuteczne działania, które można podjąć.  

Zatwierdzenia działań

Przewodniczący CMT zazwyczaj ogranicza czas dyskusji. Ma to na celu zapobieżenie ciągnięciu się dyskusji w nieskończoność, prowadząc do bezczynności. Ponadto, w zależności od scenariusza, sytuacja może się pogorszyć wraz z upływem czasu. Na przykład, jeśli ransomware jest wdrażany z centralnej lokalizacji, takiej jak obiekty zasad grupy, całe środowisko Windows zostanie zaszyfrowane w ciągu 120 minut! Z każdą minutą, w której zespół omawia działania, ransomware rozprzestrzenia się. Dlatego dyskusje te są ograniczone, zanim zespół zdecyduje, które działania zostaną podjęte.

Jak wspomniano wcześniej, zazwyczaj nie odbywa się to w sposób demokratyczny i często jest decyzją podejmowaną bezpośrednio przez prezesa. Decyzje te nie są podejmowane pochopnie, ponieważ ostatecznie to kadra zarządzająca poniesie odpowiedzialność za kryzys; jednak bezczynność często może mieć znacznie poważniejsze konsekwencje. Czy byłbyś w stanie podjąć te kluczowe decyzje, wybierając mniejsze zło w ograniczonym czasie?  

Dokumentacja i zamykanie kryzysów

Po zażegnaniu kryzysu należy go udokumentować. Na podstawie notatek skryby tworzony jest dokument kryzysowy. Dokument ten szczegółowo opisuje wydarzenia w trakcie kryzysu i działania podjęte w celu zaradzenia mu. Informacje te nie są przeznaczone wyłącznie do archiwizacji, ale mogą być wykorzystane przez CMT do wyciągnięcia wniosków z kryzysu i dostosowania procesów i polityk, aby lepiej radzić sobie z cyberkryzysem w przyszłości.

Złota rączka

Członkowie CMT zazwyczaj mają szeroki zakres obowiązków. Na przykład, prezes zarządu (CEO) odpowiada za zarządzanie całą organizacją. Chociaż prezes zarządu może posiadać rozległą wiedzę z różnych dziedzin, nie można oczekiwać, że będzie ekspertem we wszystkim, czym zajmuje się organizacja. Dotyczy to większości członków CMT. W związku z tym, zespół ten, działając w izolacji, nie byłby w stanie poradzić sobie z kryzysem i musiałby korzystać z wiedzy innych osób z otoczenia.  

Mistrzowie jednego

W tym miejscu do gry wkraczają eksperci w danej dziedzinie. Jako inżynier bezpieczeństwa możesz być zaangażowany w CMT, jeśli kryzys dotyczy Twojego działu. Jako inżynier bezpieczeństwa powinieneś posiadać niezwykle dogłębną wiedzę na temat swojego konkretnego systemu lub zasobu, dzięki czemu będziesz mógł przekazać CMT kluczowe informacje.

CMT może podejmować skuteczne działania tylko wtedy, gdy spełnione są następujące warunki:

- Zespół CMT musi dokładnie zrozumieć zakres incydentu, w tym jego przebieg i wpływ na działalność firmy. Nigdy nie będzie możliwe zrozumienie pełnego zakresu kryzysu, ponieważ dochodzenie będzie nadal w toku, ale uzyskanie jak najjaśniejszego obrazu jest niezwykle ważne.  
    
- CMT musi zrozumieć, jakie działania może podjąć i jaki będzie wpływ i skuteczność tych działań.

MŚP odgrywają kluczową rolę w dostarczaniu tych informacji. Jako inżynier bezpieczeństwa najlepiej rozumiesz system, aby wiedzieć, jakie potencjalne działania można podjąć w celu odzyskania danych po kryzysie. Będziesz wiedzieć, jak długo przechowywane są kopie zapasowe. Będziesz wiedzieć, czy środowisko może przejść w tryb odzyskiwania po awarii. Będziesz wiedzieć, jaki byłby wpływ konieczności wyłączenia krytycznych zasobów w środowisku.

Informacje te muszą być jasno przekazane CMT, aby umożliwić im podjęcie świadomej decyzji. Bez MŚP wyjście z kryzysu byłoby niemożliwe.

Oprócz reakcji technicznej, jaką CMT może podjąć w celu zaradzenia kryzysowi, istnieją inne działania, które zespół musi rozważyć i potencjalnie podjąć. Niektóre działania pomogą zespołowi kontrolować narrację, inne mogą być wymagane przez prawo.  

Komunikacja wewnętrzna

Zespół CMT będzie musiał zdecydować, jaka komunikacja będzie wysyłana wewnętrznie. Dotyczy to nie tylko wiadomości, które trafią do pracowników, ale także komunikacji przygotowywanej dla kluczowych działów, takich jak dział pomocy technicznej. W zależności od reakcji technicznej zespołu CMT, dział pomocy technicznej może otrzymać napływ zapytań. Aby zapewnić pracownikom wsparcie techniczne i ograniczyć rozprzestrzenianie się paniki, zespół CMT przygotuje również komunikację dla tego zespołu. Chociaż zespół może tworzyć taką komunikację w czasie kryzysu, często nie jest to zalecane ze względu na ograniczony czas, co może prowadzić do błędów. Zespół powinien raczej mieć już przygotowane oświadczenia, które można po prostu zmodyfikować przed ich rozesłaniem.  

Komunikacja zewnętrzna

Komunikacja zewnętrzna jest równie ważna. Ponownie, obejmuje ona nie tylko komunikację kierowaną bezpośrednio do klientów, ale także komunikację taką jak komentarze prasowe czy wywiady, które zostaną przeprowadzone. Ten element stał się niezwykle istotny i niezwykle trudny do opanowania w dzisiejszych czasach ze względu na media społecznościowe. Organizacje często zatrudniają zespoły, które zajmują się tą komunikacją w trakcie incydentu, aby zapewnić, że opinia publiczna jest informowana o sytuacji, nie wywołując przy tym strachu i paniki, które mogłyby zaszkodzić reputacji organizacji.  

Informowanie regulatora

W zależności od kategorii organizacji, może zaistnieć konieczność poinformowania innych podmiotów zewnętrznych. Na przykład, w sektorze finansowym, organizacje są zazwyczaj prawnie zobowiązane do powiadomienia odpowiedniego organu regulacyjnego w przypadku kryzysu. Wynika to z faktu, że kryzys może mieć wpływ na cały kraj. Innym powszechnym organem regulacyjnym, który należy powiadomić w czasie kryzysu, jest organ nadzoru informacji, jeśli kryzys doprowadził do naruszenia danych klientów w krajach, które muszą przestrzegać przepisów takich jak RODO.  

Kontaktowanie się z organami ścigania

Ponadto, w zależności od kraju organizacji, może zaistnieć potrzeba kontaktu z organami ścigania, na przykład FBI. Zazwyczaj procedury te są definiowane przez CMT przed kryzysem i stanowią część ich podręczników. Organy ścigania często mogą pomóc w dochodzeniu i zapewnić, że…łańcuch dostawdowody kryminalistyczne służą później do wszczęcia postępowania karnego.

Ćwiczenie CMT

Skoro rozumiesz już proces CMT, czas wykorzystać tę wiedzę w walce z cyberkryzysem. Uruchom stronę statyczną i zajmij się kryzysem!
