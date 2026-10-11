---

Charakterystyka chmury   

Jeszcze kilka lat temu nikt nie wyobrażał sobie, że organizacje będą umieszczać swoje dane i operacje na oddalonej o wiele kilometrów platformie, którą będą zarządzać nieznane osoby. Jednak chmura obliczeniowa staje się tak popularna, że ​​organizacje każdego typu i wielkości wykorzystują ją do różnych celów, takich jak przechowywanie danych, tworzenie kopii zapasowych, odzyskiwanie danych po awarii i zapewnianie ciągłości działania (BCO). Zyskuje ona popularność ze względu na następujące cechy:

- **Skalowalność** : W chmurze obliczeniowej organizacje kupują zasoby tylko jednorazowo. Zamiast tego kupują je w zależności od potrzeb. Zasoby można również skalować w górę lub w dół w zależności od potrzeb i wymagań biznesowych.
- **Prostota** : Renomowani dostawcy usług w chmurze stawiają na prosty design i interfejs. Zazwyczaj klient musi jedynie zakupić i korzystać z usług w chmurze, minimalizując w ten sposób konfigurację.
- **Opłacalność** : Chmura obliczeniowa pozwala nam płacić za nasze usługi. Koszty są niższe, ponieważ infrastruktura jest dostarczana przez stronę trzecią i nie trzeba jej kupować od razu.
- **Lepsza automatyzacja** : Usługi przetwarzania w chmurze wymagają ograniczonego zaangażowania człowieka w administrowanie, dzięki czemu firmy mogą skupić się na swoich celach, nie martwiąc się o zarządzanie systemami i ich konserwację.

Modele przetwarzania w chmurze  

Przedstawione poniżej trzy modele przetwarzania w chmurze opierają się na ofercie dostawcy chmury i potrzebach klientów/organizacji.

**Infrastruktura jako usługa (IaaS)**  

W modelu IaaS infrastruktura jest dostarczana przez dostawców chmury. Klient ma pełną kontrolę nad systemami operacyjnymi, usługami i aplikacjami.

- Obowiązki dostawcy usług w chmurze: utrzymywanie i wyposażanie centrów danych w stojaki, maszyny, kable i media.
- Odpowiedzialność klienta:  W tym przypadku klient zarządza zasobami logicznymi, takimi jak oprogramowanie i system operacyjny.

**Platforma jako usługa (PaaS)**  

Zawiera wszystkie usługi oferowane w ramach IaaS, a dodatkowo system operacyjny (zarządza nim użytkownik w ramach IaaS). 

- Odpowiedzialność dostawców usług chmurowych: W modelu Platforma jako usługa (Place as a Service) dostawca usług chmurowych oferuje infrastrukturę i platformę. Klienci mogą wybrać dowolną platformę zgodnie ze swoimi potrzebami. Dostawca usług jest odpowiedzialny za zarządzanie infrastrukturą i platformą.
- Odpowiedzialność klienta:  Klienci mogą instalować oprogramowanie zgodnie ze swoimi wymaganiami.

**Oprogramowanie jako usługa (Oprogramowanie jako usługa)**  

Obejmuje wszystkie usługi świadczone w ramach IaaS i PaaS.

- Odpowiedzialność dostawców usług w chmurze:  WOprogramowanie jako usługawszystkim zarządza dostawca chmury, łącznie z infrastrukturą,System operacyjnyi oprogramowanie.
- Odpowiedzialność Klienta:  Ten model jest przeznaczony dla klientów, którzy potrzebują bardziej technicznych umiejętności zarządzania. Płacą tylko za usługi i korzystają z nich, nie martwiąc się o podstawową architekturę.

![obraz dla chmury](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/f04ce2f08624ac4c7973ad4e6e6275cd.png)  

Modele wdrażania w chmurze  

**Chmura publiczna**  

W chmurze publicznej, jak sama nazwa wskazuje, zasoby udostępniane przez dostawców chmury są współdzielone przez wielu klientów. **Organizacja A** będzie korzystać z zasobów z tego samego sprzętu, który oferuje usługi innym organizacjom. Na przykład Microsoft Azure i Amazon Web Services (AWS) są przykładami chmur publicznych. Oferują one jednak również wirtualną chmurę prywatną (Sieć VPC) usług.  

**Prywatna chmura**  

W chmurze prywatnej klienci nie będą współdzielić zasobów bazowych (sprzętu i oprogramowania) jak w chmurze publicznej, a zasoby będą dedykowane jednemu klientowi. **Organizacja A** otrzyma maszynę wirtualną hostowaną w systemie specjalnie dedykowanym konkretnemu klientowi.  

**Chmura hybrydowa**  

Jest to połączenie chmury publicznej i prywatnej. Na przykład **Organizacja A** może chcieć korzystać z zasobów chmury prywatnej (do przechowywania poufnych danych systemu produkcyjnego), ale jednocześnie z chmury publicznej (do testowania aplikacji/oprogramowania), aby system produkcyjny nie uległ awarii podczas testów.   

Ważne terminologie

Istnieje kilka podstawowych terminów związanych z chmurą obliczeniową, które warto zrozumieć. Poniżej zdefiniowano niektóre z pojęć:

- **Wirtualizacja:** Wirtualizacja to podstawowa technologia wykorzystywana w przetwarzaniu w chmurze, która umożliwia jednoczesne udostępnianie instancji aplikacji lub zasobów wielu klientom lub użytkownikom.
- **Moc obliczeniowa:**  Definiowana jako moc obliczeniowa potrzebna klientom do uruchamiania aplikacji i systemów do przetwarzania danych oraz wykonywania różnych zadań. W chmurze obliczeniowej klienci mogą uzyskać moc obliczeniową z kombinacji maszyn wirtualnych hostowanych w środowisku chmurowym. 
- **Przechowywanie:**  W przypadku przetwarzania w chmurze nie musimy kupować ani utrzymywać fizycznych dysków twardych. Zamiast tego nasze dane są przechowywane w logicznych pulach fizycznej pamięci masowej w siedzibie dostawcy chmury, a my możemy skalować zasoby w górę i w dół zależnie od potrzeb.
- **Sieciowanie:**  Ponieważ chmura obliczeniowa to system połączonych ze sobą komputerów/procesów, utrzymanie szybkiego połączenia sieciowego jest niezwykle ważne. Dostawca chmury jest odpowiedzialny za zapewnienie łączności sieciowej, aby sprostać potrzebom klientów bez zakłóceń.

Aby zrozumieć koncepcje bezpieczeństwa w chmurze, najpierw musimy wiedzieć, co należy chronić w chmurze. Prosta odpowiedź brzmi: „ **Dane** ”. Dane to aktywa i mogą obejmować dowolne informacje, którymi dysponuje klient lub organizacja. Przed udostępnieniem danych na platformach chmurowych należy je podzielić na różne poziomy (zgodnie z definicją poniżej), aby można było zastosować odpowiednie środki kontroli i chronić je z punktu widzenia bezpieczeństwa. Istnieją trzy główne klasy danych, w zależności od ich wrażliwości:  

- **Dane poufne:**  Dane poufne można uznać za najważniejsze dane, jakimi może dysponować organizacja. Ujawnienie poufnych informacji/danych może zaszkodzić reputacji organizacji, a nawet może obejmować dane osobowe.
- **Dane wewnętrzne:**  Dane wewnętrzne to informacje, których ujawnienie powoduje umiarkowane ryzyko lub szkodę dla firmy.
- **Dane publiczne:**  Dane publiczne to wszelkie informacje zawarte w (lub przeznaczone dla) opinii publicznej. Wyciek danych publicznych nie pociąga za sobą żadnych konsekwencji, ponieważ są one i tak przeznaczone do użytku wszystkich. 

Cykl życia danych w chmurze  

W dzisiejszym świecie organizacje przechowują i wykorzystują ogromne ilości danych, w tym krytyczne i wrażliwe dane klientów.  Danymi w chmurze należy zarządzać w całym cyklu ich życia, aby zapewnić ich bezpieczne wykorzystanie na każdym etapie.  

**Główne kroki**

Cykl życia danych oznacza sekwencję kroków, przez które przechodzą określone dane od momentu ich utworzenia do momentu ich usunięcia.  

![obraz cyklu życia danych w chmurze](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/6ffcd9635986909d32ad621e95827e1c.png)

Aspekty bezpieczeństwa w cyklu życia danych w chmurze

Każda faza cyklu życia danych w chmurze wymaga ochrony. Poniżej przedstawiono etapy cyklu życia danych w chmurze, kwestie bezpieczeństwa i wymagania.

**Utwórz/Aktualizuj**

Faza tworzenia to początkowa faza cyklu życia danych. Obejmuje ona nowo utworzone dane oraz dane świeżo importowane z innych źródeł.  Na tym etapie należy zdefiniować właściciela danych oraz dokonać kategoryzacji lub klasyfikacji danych. Aspekty bezpieczeństwa i wyzwania w tym etapie przedstawiają się następująco:

- **Wdrażanie protokołu SSL/TLS:**  Bezpieczna komunikacja poprzez SSL/TLSnależy wdrożyć w taki sposób, aby uniemożliwić atakującemu podsłuchiwanie danych przesyłanych pomiędzy klientem a dostawcą usług w chmurze.
- **Szyfrowanie:**  Dane powinny być szyfrowane, aby w razie ich ujawnienia atakujący nie mógł ich odczytać bez odszyfrowania.
- **Bezpieczne połączenia:**  Należy ustanowić bezpieczne połączenia i ścieżki do przesyłu danych, aby zminimalizować ryzyko naruszenia bezpieczeństwa danych (zapewniając bezpieczeństwo danych podczas przesyłu).

**Sklep**

Dane są przetwarzane w zależności od ich formy (ustrukturyzowanej lub nieustrukturyzowanej) i przechowywane wpojemnikpowszechnie znany jako baza danych. Aspekty bezpieczeństwa na tym etapie przedstawiają się następująco:

- **Szyfrowanie:**  Dane powinny być szyfrowane w celu ochrony danych w czasie rzeczywistym.odpoczynek.
- **Kopia zapasowa:**  Aby zapobiec utracie danych, należy wykonać kopię zapasową. Jeśli dane zostaną utracone, będzie można je odzyskać z dostępnych kopii zapasowych.

**Używać**

Jak wiemy, jeśli dane są zaszyfrowane, muszą zostać odszyfrowane, aby mogły być wykorzystane przez aplikację. Aspekty bezpieczeństwa obejmują następujące środki:

- **Bezpieczne połączenia:**  Przed przesłaniem danych należy ustanowić ścieżki szyfrowane, aby zapewnić poufność iuczciwośćdanych w tranzycie.
- **Bezpieczna platforma:**  Należy stosować bezpieczny mechanizm uwierzytelniania, chroniący przed atakami i lukami w zabezpieczeniach.
- **Ograniczenie uprawnień:**  Właściciele danych powinni określić ścisłe uprawnienia umożliwiające modyfikację i przetwarzanie danych pochodzących od osób nieupoważnionych.
- **Bezpieczna wirtualizacja:**  W chmurze obliczeniowej istnieje koncepcja wirtualizacji, w której zasoby są współdzielone między użytkownikami. Dlatego dostawcy chmury muszą zapewnić, że dane jednego klienta nie będą widoczne dla innych klientów.

**Udział**

Udostępnianie danych w obrębie infrastruktury chmurowej lub poza nią. Wyzwania obejmują:

- **Jurysdykcja:**  Nakazy/ograniczenia regulacyjne dotyczące udostępniania danych pomiędzy określonymi lokalizacjami/regionami. 
- **Zapobieganie utracie danych (DLP):**  Zapobieganie utracie danych (DLP) pomaga wykrywać i zapobiegać naruszeniom danych lub niepożądanemu zniszczeniu poufnych danych. Chroni poufne dane przed udostępnieniem osobom nieupoważnionym.

**Archiwum**

Długoterminowe przechowywanie danych i aplikacji; aspekty bezpieczeństwa obejmują:

- **Szyfrowanie:**  Dane powinny zostać zaszyfrowane przed ich przechowywaniem w chmurze 
- **Bezpieczeństwo fizyczne:**  wymaga fizycznego zabezpieczenia serwerów pamięci masowej i uniemożliwienia nieautoryzowanego dostępu za pomocą biometrii, monitoringu CCTV itp.
- **Lokalizacja:**  Odzwierciedla fizyczną lokalizację, w której będą przechowywane dane. Czynniki środowiskowe, takie jak klęski żywiołowe, klimat itp., mogą stanowić ryzyko i należy wziąć pod uwagę aspekty jurysdykcyjne (przepisy lokalne i krajowe).
- **Procedura tworzenia kopii zapasowej:** W jaki sposób dane będą odzyskiwane w razie potrzeby i jak często będą wykonywane pełne/przyrostowe kopie zapasowe?

**Zniszczyć**

Dane powinny być niszczone jednorazowo, aby uniemożliwić ich niewłaściwe wykorzystanie przez jakiegokolwiek użytkownika (umyślne lub nieumyślne). Niszczenie danych kryptograficznych to proces, w którym zaszyfrowane dane stają się bezużyteczne poprzez zniszczenie kluczy kryptograficznych (bez kluczy danych nie można odszyfrować).  

Problemy bezpieczeństwa w chmurze i ich rozwiązanie

Pomimo korzyści płynących z przetwarzania w chmurze, konieczne jest skuteczne rozwiązanie kilku problemów związanych z bezpieczeństwem. Wyzwania te rodzą obawy dotyczące podstawowych właściwości bezpieczeństwa, takich jak poufność,uczciwośći dostępności. Istotne kwestie zdefiniowano poniżej:

- **Poufność danych:**  Gdy dane są hostowane w chmurze, ich prywatność jest zagrożona. Ponieważ użytkownicy nie mają fizycznego dostępu do swoich danych po ich przekazaniu na zewnątrz, nie wiedzą, w jaki sposób jest zachowywana ich poufność. Dostawcy usług chmurowych mogą analizować dane użytkowników bez wykrycia.
- **Problemy z wirtualizacją:** Umożliwia ona współdzielenie zasobów między użytkownikami. Potrzebujemy mechanizmu zapewniającego izolację i bezpieczną komunikację między maszynami wirtualnymi. Użytkownicy nie są izolowani w środowisku wielodostępnym, więc jeden użytkownik może przeglądać dane innego użytkownika.
- **Niezabezpieczone interfejsy iAPI:** Usługami w chmurze zarządzają klienci za pomocą oprogramowania lub interfejsów API. W związku z tym podatne na ataki oprogramowanie lubAPImoże być ryzykowne, a poufność danych lub klientów iuczciwośćsą zagrożone.  
    
- **Złośliwi insiderzy:** Niektórzy złośliwi insiderzy mogą spowodować wyciek danych innych klientów. Wykorzystując luki w zabezpieczeniach współdzielonej technologii, mogą oni ujawnić dane innych użytkowników lub wykorzystać luki w zabezpieczeniach, stwarzając w ten sposób zagrożenie dla bezpieczeństwa innych klientów w chmurze.
- **Przejęcie konta lub usługi:** Przejęcie konta lub usługi może nastąpić na kilka sposobów. Należą do nich:phishingoszustwa, wykorzystywanie luk w zabezpieczeniach i ponowne używanie haseł przez użytkowników.
- **Mechanizm kontroli dostępu (ACM):**  W środowisku przetwarzania w chmurze użytkownicy i serwery w chmurze nie znajdują się w tej samej domenie. Zapewnienie wydajnego i niezawodnego dostępu do informacji ma kluczowe znaczenie w przypadku outsourcingu danych do chmury. Osoba nieupoważniona może uzyskać dostęp do danych z powodu braku uprawnień kontroli dostępu.

## SIEM 

![Obraz systemu SIEM pobierającego dane z wielu źródeł](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/394ecb48936ee792b1197c1cd2f7bf89.svg)

Zarządzanie informacjami i zdarzeniami bezpieczeństwa (SIEM) to zbiór zintegrowanych technologii zarządzania, które zapewniają całościowy obraz bezpieczeństwa informacji w organizacji.SIEMSystemy zbierają i agregują dane dziennika generowane w całej infrastrukturze informatycznej organizacji z urządzeń sieciowych, systemów i aplikacji.

SIEM Oprogramowanie następnie identyfikuje i kategoryzuje incydenty i zdarzenia oraz je analizuje. Analiza ta może być pomocna w identyfikowaniu problemów, takich jak zagrożenia bezpieczeństwa, zainfekowane systemy i złośliwe działania. Może również pomóc w podejmowaniu potencjalnych działań w odpowiedzi na incydenty.

![Ilustracja przedstawiająca system SIEM z 4 funkcjami: zbieranie danych ze źródeł, agregowanie danych, wykrywanie i wykrywanie zagrożeń oraz identyfikacja naruszeń i badanie alertów.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/7f7d18c7dcd2eea96e14a0bca68d23dc.svg)  

Kluczowe możliwościSIEMtechnologia obejmuje:

- **Agregacja danych** : Umożliwia zbieranie danych z wielu źródeł, takich jak urządzenia sieciowe, kontrole bezpieczeństwa, serwery i bazy danych, zapewniając globalny obraz środowiska IT.
- **Korelacja i analiza** :SIEMSystemy mogą korelować różne zdarzenia i logi, aby wykryć wzorce potencjalnie złośliwych działań.
- **Alerty i raportowanie** : Na podstawie analizy danych,SIEMmoże automatycznie wysyłać alerty po zidentyfikowaniu jakiejkolwiek nietypowej aktywności oraz tworzyć pulpity nawigacyjne/raporty dla administratorów IT.
- **Analiza kryminalistyczna** : umożliwia przeprowadzanie analizy historycznej danych zdarzeń w celu badania i łagodzenia zagrożeń cybernetycznych.
- **Kanały informacji o zagrożeniach** : WieleSIEMNarzędzia integrują źródła informacji o zagrożeniach, aby usprawnić wykrywanie incydentów i proaktywnie identyfikować zagrożenia zewnętrzne.
- **Automatyzacja i orkiestracja** : Niektóre zaawansowane systemy SIEM będą miały również możliwość automatycznego reagowania na wykryte incydenty, na przykład poprzez blokowanie adresów IP lub dezaktywację podatnych usług.

SIEMjest kluczowym narzędziem zapewniającym zgodność z wewnętrznymi i zewnętrznymi zasadami bezpieczeństwa oraz utrzymującym solidną postawę bezpieczeństwa w całej organizacji.

Jest ich wieleSIEMdostępne rozwiązania takie jakWazuhISplunkAby zdobyć praktyczne doświadczenie w pracy zSIEM, polecamy[Wazuh](https://tryhackme.com/room/wazuhct)i[Splunk:](https://tryhackme.com/room/splunk101) Pokoje podstawowe.

Rejestrowanie, monitorowanie i audyt stanowią kluczowe elementy strategii zarządzania danymi i cyberbezpieczeństwa.

Rejestrowanie pozwala na zapisywanie szczegółowych zapisów zdarzeń dotyczących działania systemu, często stanowiąc pierwszy punkt odniesienia podczas rozwiązywania problemów lub optymalizacji systemu.

Monitorowanie stanowi kontynuację procesu rejestrowania w czasie rzeczywistym, oferując natychmiastowy wgląd w stan i wydajność systemu oraz możliwość identyfikowania potencjalnych problemów, zanim się nasilą.

Z drugiej strony, audyt zapewnia systematyczny przegląd logów i historii monitorowania, niezbędny do zapewnienia zgodności z przepisami. Pomaga identyfikować rozbieżności lub problemy, przypisując odpowiedzialność za działania systemowe. Co istotne, rejestrowanie, monitorowanie i audyt sprzyjają stworzeniu środowiska systemowego o zwiększonym bezpieczeństwie, wiarygodności, wydajności i zgodności z przepisami.uczciwość.

Poniżej znajduje się tabela podsumowująca porównująca rejestrowanie, monitorowanie i audyt.

||Wycięcie lasu|Monitorowanie|Audyt|
|---|---|---|---|
|**Definicja**|Rejestrowanie aktywności i zmian w systemie|Gromadzenie danych i raportów w czasie rzeczywistym w celu monitorowania stanu systemu|Systematyczna analiza i przegląd działań w ramach systemów|
|**Funkcja główna**|Przechowuje historię procesów, działań lub zdarzeń systemowych|Rejestruje i wizualizuje stan systemów na żywo|Sprawdza zgodność z ustalonymi standardami IT i działaniami korygującymi|
|**Identyfikacja wyników**|Często po wydaniu lub przy sprawdzeniu|W czasie rzeczywistym, w momencie wystąpienia anomalii lub naruszenia|Zwykle po akcji, podczas kontroli zgodności|
|**Przepływ procesu**|Działa pasywnie, zbierając dane w miarę zachodzenia zdarzeń|Aktywne analizowanie procesów i regularne sprawdzanie wydajności systemu|Wykonywane w określonych godzinach, często okresowo, mogą być wyzwalane przez zdarzenia|
|**Zastosowania**|Znajdź błędy, debuguj, przeprowadź analizę kryminalistyczną, pomóż w audytach|Utrzymywanie wydajności systemu, śledzenie błędów w czasie rzeczywistym, przewidywanie problemów|Sprawdzanie prawidłowości, kontrola bezpieczeństwa, wykazywanie odpowiedzialności i ograniczanie potencjalnych zagrożeń|
|**Kluczowa rola**|Gromadzenie danych i rozliczanie|Konserwacja zapobiegawcza i predykcyjna|Zgodność, weryfikacja i profesjonalizm prawny|

![[Pasted image 20260404093048.png]]
