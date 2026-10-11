---

![Widmo częstotliwości bezprzewodowych pokazujące, gdzie znajdują się cztery technologie bezprzewodowe, od niższej częstotliwości i większego zasięgu po lewej stronie do wyższej częstotliwości i mniejszego zasięgu po prawej stronie. RFID działa w zakresie od 125 kHz do 960 MHz i służy do śledzenia zasobów i kontroli dostępu. NFC działa na częstotliwości 13,56 MHz i służy do płatności zbliżeniowych i przesyłania danych na krótki zasięg. Bluetooth działa na częstotliwości 2,4 GHz i służy do parowania urządzeń na krótkim zasięgu. Wi-Fi działa na częstotliwościach 2,4 GHz i 5 GHz, zapewniając łączność bezprzewodową LAN w standardzie 802.11. Bluetooth i Wi-Fi na częstotliwości 2,4 GHz korzystają z tego samego pasma, co może powodować zakłócenia między urządzeniami.](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1773913328853.svg)

Technologie bezprzewodowe odegrały kluczową rolę w umożliwieniu łączności między urządzeniami, co umożliwiło wymianę danych w nowoczesnych środowiskach bez połączeń fizycznych. Należy jednak pamiętać, że technologie te mogą wprowadzać luki w zabezpieczeniach, które atakujący mogą wykorzystać do naruszenia poufnych danych. Zrozumienie, jak działają technologie bezprzewodowe i jak mogą one narazić organizację na ataki, pomoże zbudować solidne podstawy niezbędne do oceny sieci bezprzewodowych.

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Zrozumieć podstawy sieci bezprzewodowych, w tym sposób komunikacji urządzeń za pośrednictwem częstotliwości radiowych
- Zidentyfikuj powszechnie stosowane technologie bezprzewodowe (Wi-Fi, Bluetooth, NFC i RFID) i przypadki ich zastosowania
- Rozpoznawać typowe zagrożenia bezpieczeństwa i wektory ataków związane z technologiami bezprzewodowymi
- Zastosuj podstawowe środki bezpieczeństwa, aby chronić sieci bezprzewodowe przed typowymi zagrożeniami

## Wymagania wstępne

Przed rozpoczęciem tej sali zaleca się podstawową wiedzę z zakresu sieci. Jeśli dopiero zaczynasz przygodę z sieciami, rozważ najpierw wypełnienie poniższej sali:

- [Koncepcje sieciowe](https://tryhackme.com/room/networkingconcepts)

![Typowa topologia sieci Wi-Fi|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1773920336739.svg)

W dzisiejszych czasach ludzie przyzwyczaili się do korzystania z Wi-Fi w celu łączenia się z internetem. Można je znaleźć w domach, biurach, kawiarniach i na lotniskach. Umożliwia ono urządzeniom komunikację za pomocą sygnałów radiowych zamiast fizycznych kabli, co zapewnia elastyczność i wygodę połączenia. Aby jednak zapewnić bezpieczeństwo, najpierw trzeba zrozumieć, jak ono działa.

Sieć Wi-Fi składa się z następujących kluczowych komponentów:

- **Punkt dostępowy (AP)** : Urządzenie nadające sygnał Wi-Fi. Można go sobie wyobrazić jako most między urządzeniami bezprzewodowymi a siecią przewodową. Przykładem punktu dostępowego jest router domowy.
- **Klienci** : Są to urządzenia łączące się z punktem dostępowym (AP) w celu uzyskania dostępu do zasobów wewnętrznych lub internetu, takie jak telefony komórkowe, laptopy, tablety, drukarki i urządzenia inteligentne. Każde urządzenie posiada bezprzewodową kartę sieciową (NIC), która obsługuje wysyłanie i odbieranie sygnałów radiowych.

## Identyfikatory w sieciach Wi-Fi

Każda sieć Wi-Fi wymaga identyfikacji. Poniżej znajdują się dwa powszechnie używane identyfikatory.

- **SSID (Service Set Identifier):** To po prostu nazwa sieci, którą widzisz po otwarciu ustawień Wi-Fi i przeglądaniu dostępnych sieci. Np.`Office_WiFi`
- **BSSID (Basic Service Set Identifier):** Unikalny identyfikator punktu dostępowego, który zazwyczaj jest reprezentowany przez adres MAC interfejsu bezprzewodowego. Np.`00:1A:2B:3C:4D:5E`

## Jak komunikują się urządzenia bezprzewodowe

Urządzenia komunikują się bezprzewodowo, przesyłając fale radiowe przez wspólną przestrzeń powietrzną. Komunikacja między urządzeniami odbywa się w określonych pasmach częstotliwości. Pasmo częstotliwości używane przez urządzenie w dużym stopniu decyduje o jego szybkości, zasięgu i niezawodności. W sieciach Wi-Fi występują dwa popularne pasma częstotliwości, z których każde wiąże się z pewnymi kompromisami:

- **Pasmo 2,4 GHz** zapewnia lepszy zasięg (do około 45 metrów w pomieszczeniach) i łatwiej przenika przez ściany i podłogi. Wada? Jest tłoczno. Mikrofalówki, urządzenia Bluetooth, elektroniczne nianie i sieć Wi-Fi sąsiada konkurują w tym paśmie. Dodatkowo, prędkość maksymalna sięga około 600 Mb/s.
- **Pasmo 5 GHz** jest szybsze (do około 1300 Mb/s) i znacznie mniej obciążone, ale sygnał nie dociera tak daleko i ma większe trudności z pokonywaniem przeszkód fizycznych (około 15 metrów w pomieszczeniach). Jeśli kiedykolwiek zauważyłeś utratę połączenia podczas przechodzenia do innego pokoju, prawdopodobnie korzystasz z pasma 5 GHz.

Poniższy wykres ilustruje porównanie różnic między częstotliwościami 2,4 GHz i 5 GHz pod względem zasięgu, prędkości, przenikania przez przeszkody fizyczne i zatorów.

![Kluczowe różnice między częstotliwościami 2,4 GHz i 5 GHz|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1773915774873.svg)

## Proces stowarzyszenia

Gdy urządzenie dołącza do sieci Wi-Fi, proces łączenia obejmuje wiele etapów, w tym skojarzenie. Ogólny przebieg wygląda następująco:

1. Urządzenie skanuje obszar w poszukiwaniu dostępnych sieci
2. Ty (lub automatycznie Twoje urządzenie) wybierasz sieć, do której chcesz dołączyć
3. Urządzenie i punkt dostępowy wymieniają się danymi uwierzytelniającymi i nawiązują połączenie
4. Negocjowane są klucze szyfrujące, aby umożliwić ochronę ruchu
5. Dane zaczynają płynąć

Warto wiedzieć, że kolejność tych kroków może się różnić w zależności od używanego protokołu bezpieczeństwa. W przypadku **uwierzytelniania Open System Authentication** (OPA) punkt dostępu nie weryfikuje żadnych danych uwierzytelniających podczas uwierzytelniania. Jest to w zasadzie uzgadnianie, które oznacza „tak, możesz ze mną rozmawiać”. Dzieje się tak zarówno w przypadku WPA2-Personal, jak i WPA2-Enterprise. Różnica polega na tym, co następuje później. W przypadku **WPA2-Personal** urządzenie przechodzi przez 4-etapowe uzgadnianie, aby udowodnić, że zna klucz wstępny. W przypadku **WPA2-Enterprise z 802.1X** urządzenie najpierw nawiązuje połączenie, a następnie zostaje przekazane do dedykowanego serwera uwierzytelniającego (np. RADIUS) w celu pełnego uwierzytelnienia opartego na danych uwierzytelniających. W obu przypadkach oba kroki muszą zostać wykonane przed wymianą jakichkolwiek danych.

![Przepływ pracy procesu kojarzenia Wi-Fi](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1778873800742.svg)

## Czynniki wpływające na sygnały i zasięg Wi-Fi

Siła i niezawodność sygnałów w sieci Wi-Fi zależą od kilku czynników. Poniżej przedstawiamy niektóre z czynników, które obniżają jakość połączenia Wi-Fi.

- **Bariery fizyczne** : ściany, podłogi i sufity osłabiają sygnał Wi-Fi. Beton i metal są najbardziej szkodliwe. Nawet akwarium pełne wody może zauważalnie wpływać na siłę sygnału.
- **Odległość:** Im dalej znajdujesz się od punktu dostępowego, tym słabsze i mniej niezawodne staje się połączenie.
- **Zakłócenia:** Urządzenia elektroniczne o podobnych częstotliwościach mogą zakłócać sygnały. Dotyczy to kuchenek mikrofalowych, urządzeń Bluetooth i innych sieci Wi-Fi.
- **Przeciążenie kanałów:** Wiele sieci działających na nakładających się kanałach może powodować problemy z wydajnością z powodu przeciążenia sygnału i konkurencji. W gęstych środowiskach, takich jak bloki mieszkalne, może to poważnie obniżyć wydajność.
- **Wyciek sygnału:** Sygnały mogą wykraczać poza zamierzone granice fizyczne i docierać do takich obszarów jak ulice, parkingi lub sąsiednie biura, co zwiększa ryzyko narażenia, jeśli nie są odpowiednio zarządzane.

Wi-Fi to technologia bezprzewodowa wykorzystywana w domach, biurach i miejscach publicznych. Jest zgodna ze standardami IEEE 802.11, które określają sposób, w jaki urządzenia bezprzewodowe łączą się i komunikują ze sobą.

Na przestrzeni lat wprowadzono różne generacje Wi-Fi w ramach standardów IEEE 802.11. Standardy te przedstawiono w poniższej tabeli.

![Lista standardów Wi-Fi IEEE 802.11 i najważniejsze usprawnienia](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1773996055257.svg)

Większość przedsiębiorstw wdraża standardy Wi-Fi 5 i Wi-Fi 6, ponieważ dobrze współpracują one z nowoczesnymi laptopami, smartfonami i punktami dostępowymi. Z tego powodu często pojawiają się one w ocenach bezpieczeństwa.

## Uwierzytelnianie i szyfrowanie w sieci Wi-Fi

Bezpieczna komunikacja Wi-Fi opiera się na dwóch głównych elementach: uwierzytelnianiu, które kontroluje, kto może nawiązać połączenie, oraz szyfrowaniu, które chroni przesyłane dane.

Sieci Wi-Fi korzystają z protokołów bezpieczeństwa, aby zapewnić, że tylko autoryzowane urządzenia mogą się połączyć, a dane pozostają chronione. Oto kilka popularnych protokołów bezpieczeństwa Wi-Fi:

![Wyjaśnienie protokołów bezpieczeństwa Wi-Fi](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1773996055277.svg)

## Typowe błędy w konfiguracji Wi-Fi

Prawidłowa konfiguracja sieci Wi-Fi ma kluczowe znaczenie dla utrzymania bezpieczeństwa. Nieprawidłowo skonfigurowane sieci Wi-Fi mogą wprowadzać słabe punkty i zwiększać podatność na ataki sieci bezprzewodowych. Typowe słabe punkty to:

- Korzystanie ze przestarzałych protokołów bezpieczeństwa, takich jak WEP
- Stosowanie słabych haseł
- Korzystanie z niepotrzebnych funkcji, takich jak WPS
- Korzystanie z domyślnych poświadczeń administracyjnych

## Typowe koncepcje ataków Wi-Fi

Gdy sieci Wi-Fi są niezabezpieczone, atakujący mogą próbować wykorzystać luki w uwierzytelnianiu lub konfiguracji. Typowe koncepcje ataków na Wi-Fi obejmują:

- **Ataki na hasła:** łamanie słabych haseł Wi-Fi metodą brute force.
- **Nieautoryzowane punkty dostępu:** Nieautoryzowany punkt dostępu podłączony do sieci bez wiedzy administratora sieci. Może zostać skonfigurowany celowo przez atakującego lub nawet nieumyślnie przez pracownika podłączającego własny router.
- **Ataki typu Evil Twin:** Tworzenie fałszywego punktu dostępu, który imituje legalną sieć, używając tego samego identyfikatora SSID. W przeciwieństwie do nieuczciwego punktu dostępu, który jest fizycznie połączony z siecią docelową, Evil Twin działa niezależnie i polega na podstępnym nakłanianiu użytkowników do połączenia się z nim, często w celu przechwycenia ich ruchu lub danych uwierzytelniających.
- **Ataki polegające na deauthenticacji:** zmuszanie urządzeń do odłączenia się od sieci.
- **Przechwytywanie ruchu:** próba przechwycenia ruchu bezprzewodowego, jeśli szyfrowanie jest słabe lub nieprawidłowo skonfigurowane.

## Ochrona sieci Wi-Fi

Zabezpieczenie sieci Wi-Fi wymaga prawidłowej konfiguracji i monitorowania. Poniżej przedstawiamy kilka najlepszych praktyk związanych z zabezpieczaniem sieci Wi-Fi:

- **Korzystanie z protokołu WPA2 lub WPA3 z silnymi hasłami:** chroni przed nieautoryzowanym dostępem do sieci, zapewniając, że połączyć się mogą wyłącznie uwierzytelnione urządzenia i uniemożliwiając atakującym łatwe odgadnięcie lub złamanie danych uwierzytelniających.
- **Wyłączanie przestarzałych protokołów, takich jak WEP:** Ochrona przed atakami wykorzystującymi słabości szyfrowania w celu odzyskania kluczy szyfrujących sieć bezprzewodową.
- **Wyłączanie funkcji WPS, jeśli nie jest wymagana:** Zapobiega to nawiązywaniu przez atakujących połączenia z siecią Wi-Fi przy użyciu alternatywnych metod uwierzytelniania, takich jak 8-cyfrowy kod PIN.
- **Zmiana domyślnych danych uwierzytelniających administratora:** Zapobiega przejęciu przez atakujących kontroli administracyjnej nad punktami dostępu przy użyciu powszechnie znanych domyślnych nazw użytkowników i haseł.
- **Wdrażanie siecisegmentacja(np. oddzielne sieci dla gości):** Ogranicza dostęp do systemów wewnętrznych poprzez izolowanie urządzeń gościnnych lub urządzeń, którym nie można ufać, od wrażliwych zasobów organizacji.
- **Regularna aktualizacja oprogramowania sprzętowego w punktach dostępowych:** zapewnia ochronę przed znanymi lukami w zabezpieczeniach poprzez stosowanie poprawek zabezpieczeń i napraw udostępnianych przez producentów urządzeń.

Prawidłowa konfiguracja znacznie zmniejsza ryzyko nieautoryzowanego dostępu i naruszenia bezpieczeństwa sieci, jednocześnie chroniąc uczciwość danych przesyłanych zarówno w sieciach prywatnych, jak i publicznych.

Bluetooth to technologia umożliwiająca bezprzewodową komunikację między urządzeniami poprzez bezpośrednie parowanie. Działa w paśmie 2,4 GHz i jest przeznaczona do komunikacji krótkiego zasięgu. Do popularnych urządzeń korzystających z Bluetooth należą:

- Klawiatury i myszy bezprzewodowe
- Słuchawki i głośniki
- Smartwatche i trackery fitness
- Systemy informacyjno-rozrywkowe pojazdów
- Internet rzeczy (IoT) i inteligentne urządzenia domowe

Technologia Bluetooth jest powszechnie włączona w urządzeniach prywatnych i firmowych, co czyni ją atrakcyjnym celem dla atakujących.

## Klasyczny Bluetooth kontra Bluetooth Low Energy (BLE)

Istnieją dwie główne odmiany technologii Bluetooth: Bluetooth klasyczny i Bluetooth Low Energy (BLE).

Klasyczny Bluetooth obsługuje bardziej wymagające zadania, takie jak strumieniowe przesyłanie dźwięku i plików. BLE natomiast jest przeznaczony dla urządzeń, które wysyłają niewielkie ilości danych tylko okazjonalnie. Przykładami urządzeń korzystających z BLE są trackery fitness, inteligentne zamki i sygnalizatory. Wyobraź sobie klasyczny Bluetooth jako połączenie telefoniczne, a BLE jako wiadomość tekstową. Jedno połączenie utrzymuje połączenie, a drugie jest szybkie i nie wymaga wiele wysiłku.

Istotne są również różnice w zabezpieczeniach między tymi dwoma wariantami. Klasyczny Bluetooth przechodzi przez proces parowania, w którym oba urządzenia zgadzają się na wspólny klucz. BLE obsługuje kilka metod parowania, ale najpopularniejszą w niedrogich urządzeniach IoT jest metoda „Just Works”, która nie wymaga weryfikacji użytkownika. Oznacza to, że atakujący może wejść między połączenie i przechwycić wszystko.

Poniższa tabela przedstawia najważniejsze różnice w zabezpieczeniach między technologią Classic Bluetooth i BLE w różnych obszarach.

![Kluczowe różnice między technologią Classic Bluetooth a technologią Bluetooth Low Energy](https://cdn-images.tryhackme.com/user-uploads/6186e45a4c3e9a0043efd100/room-content/6186e45a4c3e9a0043efd100-1779362067496.svg)

## Jak urządzenia Bluetooth łączą się i wymieniają dane

Zanim dwa urządzenia Bluetooth będą mogły się ze sobą komunikować, muszą przejść proces parowania w celu utworzenia bezpiecznego połączenia.

Starsze wersje Bluetooth opierały się na prostym kodzie PIN do parowania. Kod był wyświetlany na jednym urządzeniu, który użytkownik wprowadzał na drugim, lub obaj użytkownicy musieli uzgodnić ten sam numer i wprowadzić go na obu urządzeniach. Chociaż ta metoda jest skuteczna, krótkie lub domyślne kody PIN, takie jak  **0000** lub **1234,** były łatwe do odgadnięcia, a proces parowania mógł czasami zostać przechwycony lub zakłócony przez osobę w pobliżu.

Współczesny Bluetooth wykorzystuje silniejsze metody parowania. W klasycznym Bluetooth, w Bluetooth 2.1 wprowadzono Secure Simple Pairing (SSP), który zastąpił parowanie oparte na kodzie PIN bezpieczniejszą wymianą kluczy kryptograficznych. W BLE nowsze urządzenia korzystają z technologii LE Secure Connections, wprowadzonej w Bluetooth 4.2 i również opierającej się na wymianie kluczy kryptograficznych. Jednak starsze urządzenia BLE z Bluetooth 4.0 lub 4.1 nadal korzystają z LE Legacy Pairing, która zapewnia słabszą ochronę.

Sposób, w jaki parowanie jest widoczne dla użytkownika, zależy od urządzenia. Niektóre urządzenia proszą o potwierdzenie, że na obu ekranach wyświetla się ten sam numer, inne mogą korzystać z NFC.uzyskiwać, a prostsze urządzenia mogą się automatycznie parować z niewielką lub żadną interakcją użytkownika.

Poniższe diagramy pokazują, jak każda odmiana radzi sobie z procesem parowania.

![Klasyczny proces parowania Bluetooth](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774010392350.svg)

---

![Proces parowania Bluetooth Low Energy](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774010392401.svg)

## Typowe zagrożenia bezpieczeństwa Bluetooth

Komunikacja Bluetooth może stwarzać zagrożenia bezpieczeństwa, mimo że jest wygodna. Poniżej przedstawiono typowe zagrożenia bezpieczeństwa, które mogą mieć wpływ na urządzenia obsługujące technologię Bluetooth.

- **Niepotrzebna wykrywalność:** Pozostawienie urządzeń w trybie umożliwiającym ich wykrycie może zostać wykryte przez pobliskich atakujących.
- **Słabe mechanizmy parowania:** Starsze urządzenia wykorzystujące proste kody PIN mogą być podatne na ataki siłowe.
- **Nieautoryzowane parowanie:** atakujący mogą próbować sparować urządzenia, jeśli kontrola zatwierdzania przez użytkownika jest słaba lub nieprawidłowo skonfigurowana.
- **Bluejacking:** wysyłanie niechcianych wiadomości do urządzeń z włączoną technologią Bluetooth.
- **Bluesnarfing:** próba uzyskania dostępu do danych poprzez połączenie Bluetooth.
- **Bluebugging:** wykorzystywanie luk w zabezpieczeniach połączenia Bluetooth w celu przejęcia kontroli nad niektórymi funkcjami urządzenia.
- **Brak aktualizacji urządzeń:** Przestarzałe implementacje Bluetooth mogą zawierać znane luki w zabezpieczeniach.

Atakujący, którzy próbują wykorzystać słabości technologii Bluetooth, muszą znajdować się w pobliżu urządzenia. Miejsca takie jak biura, sale konferencyjne i lotniska to miejsca, w których często mogą dochodzić do ataków Bluetooth.

## Zagadnienia bezpieczeństwa dla klasycznego Bluetooth i BLE

Zarówno urządzenia z klasycznym Bluetooth, jak i BLE powinny być starannie konfigurowane i zarządzane, aby zminimalizować ryzyko zagrożeń bezpieczeństwa. Poniższa tabela przedstawia praktyczne środki, które mogą pomóc, i wyjaśnia, czy dotyczą one klasycznego Bluetooth, BLE, czy obu.

![Zagadnienia bezpieczeństwa dla technologii Classic Bluetooth i BLE](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774007023234.svg)

Chociaż Bluetooth ma ograniczony zasięg, nie daj się zwieść złudnemu poczuciu bezpieczeństwa. Podatne na ataki urządzenie może nadal wyciekać poufne dane lub umożliwiać atakującemu dostęp do szerszej sieci. Wyobraź sobie, że zostawiasz uchylone okno na parterze. Może się to wydawać zbyt błahe, by miało znaczenie, ale często wystarczy, by ktoś zdeterminowany się przedostał. Prawidłowa konfiguracja i odrobina czujności znacząco pomagają w utrzymaniu bezpieczeństwa.

Identyfikacja radiowa (RFID) to technologia wykorzystująca pola elektromagnetyczne do identyfikacji i śledzenia tagów przymocowanych do obiektów. Komunikacja bliskiego zasięgu (NFC) to blisko spokrewniony standard, który umożliwia wymianę danych między dwoma urządzeniami po ich zbliżeniu. Obie technologie umożliwiają bezprzewodową komunikację na krótkich dystansach, ale różnią się przede wszystkim zasięgiem. Urządzenia RFID mogą transmitować fale radiowe na odległość do 100 metrów lub większą, w zależności od rodzaju tagu i pasma częstotliwości. Urządzenia NFC natomiast działają w promieniu około 5 cm. Poniższy rysunek przedstawia kluczowe różnice między RFID a NFC.

![Kluczowe różnice między RFID i NFC|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774737597437.svg)

## Jak działają RFID i NFC

System RFID składa się z dwóch komponentów: czytnika (lub interrogatora) i znacznika. Czytnik emituje fale radiowe, a gdy znacznik znajdzie się w polu czytnika, odpowiada zapisanymi danymi. Znaczniki mogą być pasywne lub aktywne. Znaczniki pasywne nie mają wewnętrznego źródła zasilania i czerpią energię z pola elektromagnetycznego czytnika, co ogranicza ich zasięg, ale czyni je niedrogimi i trwałymi. Znaczniki aktywne zawierają własną baterię, co umożliwia transmisję na znacznie większe odległości, ale wiąże się z wyższymi kosztami i ograniczoną żywotnością.

Poniższy diagram ilustruje sposób działania komunikacji w systemie RFID:

![Ilustracja systemu RFID|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774741867454.svg)

Technologia NFC działa na określonej częstotliwości RFID (13,56 MHz) i obsługuje dwukierunkową komunikację między urządzeniami. Jedno urządzenie generuje pole RF, a drugie albo reaguje pasywnie, albo generuje własne pole, aby dokończyć wymianę. Ta dwukierunkowa funkcjonalność pozwala technologii NFC na obsługę interaktywnych zastosowań, takich jak płatności zbliżeniowe, karty komunikacji miejskiej i parowanie urządzeń. Obie technologie zostały zaprojektowane z myślą o szybkich i prostych interakcjach, które nie wymagają ręcznego połączenia z siecią.

Poniższy diagram ilustruje sposób działania komunikacji w systemie NFC:

![Ilustracja systemu NFC|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774741867519.svg)

RFID i NFC są powszechnie wykorzystywane do identyfikacji, kontroli dostępu i transakcji zbliżeniowych. Identyfikatory pracownicze, etykiety magazynowe, karty-klucze hotelowe i terminale płatnicze wykorzystują jedną lub obie te technologie.

## Typowe zagrożenia bezpieczeństwa RFID i NFC

Poniższe techniki są powszechnie stosowane przez atakujących w celu wykorzystania słabości technologii RFID i NFC:

- **Podsłuchiwanie:** przechwytywanie komunikacji podczas skanowania karty dostępu.
- **Klonowanie:** Kopiowanie danych z jednej karty na drugą.
- **Ataki przekaźnikowe:** przekazywanie komunikacji między ważną kartą a czytnikiem w celu ominięcia ograniczenia odległości, które normalnie uniemożliwiałoby interakcję.
- **Nieautoryzowane skanowanie (skimming):** Ukryte skanowanie karty bez wiedzy właściciela w celu kradzieży danych.
- **Zgubione lub skradzione karty:** Zgubiona pracownicza karta może posłużyć do wejścia do biura lub budynku, jeśli prawa dostępu nie zostały cofnięte.

Przykładem ataku retransmisyjnego jest karta płatnicza zbliżeniowa przechowywana w kieszeni ofiary. Jeden atakujący trzyma urządzenie w pobliżu ofiary, aby odebrać sygnał karty, podczas gdy drugi atakuje, trzymając kolejne urządzenie w pobliżu terminala płatniczego w sklepie. Oba urządzenia przekazują sobie informacje w czasie rzeczywistym, powodując, że terminal przetwarza transakcję tak, jakby karta była fizycznie obecna.

Poniższy diagram ilustruje sposób przeprowadzania ataku przekaźnikowego:

![Ilustracja ataku sztafetowego|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774735469184.svg)

## Zagadnienia bezpieczeństwa dotyczące technologii RFID i NFC

Zabezpieczenie urządzeń RFID i NFC wymaga podejścia wielowarstwowego, co wiąże się z koniecznością ochrony danych podczas transmisji oraz zabezpieczenia fizycznego dostępu do urządzeń. Poniższe środki mogą pomóc zminimalizować narażenie na ryzyko:

- Używaj kart obsługujących szyfrowanie
- Ogranicz poufne dane przechowywane na kartach lub skorzystaj z tokenizacji
- Natychmiast dezaktywuj zgubione lub skradzione karty
- Stosuj osłony ochronne, takie jak torebki Faradaya, aby zabezpieczyć się przed nieautoryzowanym skanowaniem
- Regularnie aktualizuj kontrolę dostępu
- W miarę możliwości wprowadź wtórne uwierzytelnianie biometryczne

![Topologia innych sieci bezprzewodowych|700](https://cdn-images.tryhackme.com/user-uploads/68f9e128ba199589d7ad0335/room-content/68f9e128ba199589d7ad0335-1774821749287.svg)

Oprócz Wi-Fi, Bluetooth, NFC i RFID, w nowoczesnych środowiskach wykorzystuje się wiele innych technologii bezprzewodowych. Technologie te obsługują inteligentne urządzenia, systemy automatyki i infrastrukturę połączoną.

W inteligentnych środowiskach i Internecie rzeczy powszechnie stosuje się kilka technologii bezprzewodowych (IoT) systemów. 

### Zigbee

Zigbee to protokół o niskim poborze mocy i krótkim zasięgu, powszechnie stosowany w inteligentnych urządzeniach domowych, takich jak oświetlenie, czujniki i inteligentne gniazdka. Działa w topologii sieci kratowej. Każde urządzenie może przesyłać dane do urządzeń sąsiednich, zwiększając zasięg sieci.

### Z-Wave

Z-Wave służy podobnym celom co Zigbee, ale wykorzystuje bardziej ustandaryzowany protokół i oferuje szerszy zasięg komunikacji. Jest powszechnie stosowany w systemach automatyki domowej, które sterują termostatami, roletami, oświetleniem i czujnikami bezpieczeństwa.

### LoRa(Długi zasięg)

Technologia LoRa została zaprojektowana do komunikacji na duże odległości i przy niskim poborze mocy. Jest wykorzystywana we wdrożeniach Internetu Rzeczy (IoT), takich jak systemy monitorowania środowiska, czujniki rolnicze i inteligentne oświetlenie uliczne, gdzie urządzenia przesyłają niewielkie ilości danych na odległość kilku kilometrów.

### Sieć komórkowa (np. LTE-M, NB-IoT)

Technologie komórkowe umożliwiają urządzeniom przesyłanie danych przez istniejące sieci komórkowe poprzez połączenie z pobliskimi wieżami komórkowymi, w taki sam sposób, w jaki smartfon łączy się z internetem, gdy Wi-Fi jest niedostępne. Inteligentne liczniki, urządzenia śledzące pojazdy i zdalne czujniki przemysłowe często opierają się na łączności komórkowej.

### Podczerwony

Podczerwień wykorzystuje sygnały świetlne do prostej komunikacji w linii wzroku na bardzo krótkie odległości. Jest stosowana w pilotach do telewizorów, klimatyzatorów i projektorów, choć w nowszych urządzeniach została w dużej mierze zastąpiona protokołami radiowymi.

## Zagrożenia bezpieczeństwa w powstających ekosystemach bezprzewodowych

Ponieważ urządzenia IoT są często małe i niedrogie, bezpieczeństwo nie jest priorytetem podczas projektowania i wdrażania. Wraz ze wzrostem liczby urządzeń łączących się bezprzewodowo, mogą pojawić się nowe zagrożenia bezpieczeństwa. 

Poniższa tabela opisuje znane zagrożenia bezpieczeństwa związane z technologiami bezprzewodowymi wprowadzonymi w ramach tego zadania. Nie jest to lista wyczerpująca, ponieważ pełne omówienie powierzchni ataku każdego protokołu wykracza poza zakres tego pomieszczenia.

|Technologia bezprzewodowa|Znane zagrożenia bezpieczeństwa|Przykład|
|---|---|---|
|Zigbee|Gdy urządzenie bez wstępnie skonfigurowanego klucza dołącza do sieci Zigbee, koordynator może przesłać klucz szyfrowania sieci chroniony jedynie znanym domyślnym kluczem łącza. Atakujący, podsłuchując sieć w tym czasie parowania, może odzyskać klucz i odszyfrować cały dalszy ruch. Topologia kratowa wzmacnia to ryzyko, ponieważ pojedyncze zainfekowane urządzenie może przekazywać złośliwe polecenia do wszystkich pozostałych urządzeń w sieci.|Naukowcy wykorzystali protokół Zigbee w inteligentnych żarówkach Philips Hue, przejmując kontrolę nad żarówką i użyli jej do zainstalowania złośliwego oprogramowania na moście Hue, który następnie zapewnił dostęp do szerszej sieci domowej (CVE-2020-6007).|
|Z-Wave|Z-Wave wykorzystuje strukturę bezpieczeństwa do ochrony klucza szyfrującego wymienianego podczas parowania urządzeń. Pierwotna struktura, znana jako S0, szyfrowała ten klucz za pomocą wartości statycznej składającej się z samych zer, co ułatwiało przechwycenie. Nowsza struktura S2 zastąpiła to wymianą kluczy Diffie-Hellmana, ale urządzenia obsługujące obie wersje mogą zostać zmuszone do przejścia z S2 na S0, ponieważ uzgadnianie parowania nie jest uwierzytelnione.|Naukowcy zaprezentowali ten atak obniżający jakość oprogramowania (nazwany Z-Shave) na inteligentny zamek do drzwi Yale Conexis L1, który umożliwiał wyjęcie klucza sieciowego i uzyskanie trwałego dostępu do zamka.|
|LoRa|Urządzenia aktywowane przez personalizację (ABP) używają statycznych kluczy sesji, które pozostają niezmienione, chyba że zostaną ręcznie obrócone. Jeśli licznik ramek zresetuje się po przepełnieniu lub ponownym uruchomieniu urządzenia, atakujący, który wcześniej przechwycił ruch, może odtworzyć stare wiadomości w ramach okna akceptacji licznika. Urządzenia wdrożone w odległych, bezobsługowych lokalizacjach są również fizycznie narażone na manipulację i wydobycie klucza.|Naukowcy zaprezentowali atak typu replay na urządzenia LoRaWAN 1.0, który desynchronizuje liczniki ramek między czujnikiem a serwerem sieciowym i przerywa legalną komunikację.|
|Sieć komórkowa (LTE-M, NB-IoT)|LTE-M i NB-IoT bazują na infrastrukturze 4G LTE, a nowsze wdrożenia zaczynają działać w sieci 5G. Oba korzystają z uwierzytelniania opartego na karcie SIM i standardowego szyfrowania. Urządzenia są jednak często wdrażane w odległych lokalizacjach, co umożliwia fizyczną manipulację i ekstrakcję oprogramowania układowego. Wiele z nich korzysta z ograniczonych stosów oprogramowania, które są trudne do łatania, a interfejsy zarządzania w bramkach komórkowych wykazały luki w zabezpieczeniach, w tym domyślne dane uwierzytelniające i luki w zabezpieczeniach.|Badanie przeprowadzone w 2021 r. na Uniwersytecie Purdue wykazało, że atakujący potrafią identyfikować urządzenia IoT w sieci komórkowej i wykorzystywać ich tryby uśpienia o niskim poborze mocy do przeprowadzania ukierunkowanych ataków typu „odmowa usługi” i przechwytywania danych.|
|Podczerwony|Sygnały podczerwieni nie są uwierzytelniane ani szyfrowane. Atakujący może przechwycić sygnał z pilota i odtworzyć go, aby sterować urządzeniem docelowym. Ponieważ polecenia podczerwieni są zgodne ze stałymi, publicznie udokumentowanymi protokołami, takimi jak NEC i RC5, atakujący może konstruować prawidłowe polecenia na podstawie specyfikacji bez konieczności przechwytywania jakiegokolwiek sygnału.|Naukowcy wykorzystali Raspberry Pi z niedrogim transceiverem podczerwieni do nagrywania i odtwarzania poleceń, sterując telewizorami, klimatyzatorami i dekoderami telewizji kablowej z drugiego końca pokoju.|

## Zagadnienia bezpieczeństwa w kontekście nowych technologii bezprzewodowych

Poniższe środki pomagają ograniczyć narażenie technologii bezprzewodowych na opisane powyżej ryzyka:

- **Wykorzystanie kodów instalacyjnych do parowania urządzeń Zigbee:** generuje unikalny klucz łącza dla każdego urządzenia, zapewniając, że klucz sieciowy nigdy nie zostanie zaszyfrowany publicznie znanym kluczem domyślnym podczas procesu łączenia. Zapobiega to odzyskaniu klucza sieciowego przez atakującego podsłuchującego wymianę parowania.
- **Wyłączenie wstecznej kompatybilności S0 w kontrolerach Z-Wave:** Zapobiega wymuszeniu przez atakujących obniżenia wersji z S2 do S0 podczas parowania. Jeśli wymagana jest wsteczna kompatybilność, kontroler powinien być skonfigurowany tak, aby wymagał wyraźnego potwierdzenia użytkownika przed zaakceptowaniem połączenia S0.
- **Wykorzystanie aktywacji bezprzewodowej (OTAA) dla urządzeń LoRaWAN:** generuje nowe klucze sesji dla każdego dołączenia, w przeciwieństwie do aktywacji przez personalizację (ABP), która wykorzystuje klucze statyczne, które są zachowywane do momentu ręcznej zmiany. W przypadku, gdy ABP jest nieuniknione, regularna rotacja kluczy i monitorowanie licznika klatek pomagają ograniczyć narażenie na ataki typu replay.
- **Ograniczanie dostępu do interfejsów zarządzania bramą IoT w sieci komórkowej:** Zmiana domyślnych danych uwierzytelniających bezpośrednio po wdrożeniu i umieszczenie urządzeń zaVPNlub prywatny APN ogranicza narażenie na zdalną eksploatację. Aktualizacje oprogramowania układowego należy instalować w miarę ich pojawiania się.
- **Dezaktywacja nieużywanych odbiorników podczerwieni w urządzeniach podłączonych do sieci:** Zmniejsza ryzyko ponownego odtwarzania lubwstrzykiwanie poleceńAtaki poprzez usunięcie nieuwierzytelnionego kanału sterowania. Urządzenia reagujące na podczerwień nie powinny być umieszczane w miejscach dostępnych z zewnątrz, przez okno lub drzwi.
- **Segmentacja urządzeń IoT na dedykowane segmenty sieci:** Izoluje urządzenia bezprzewodowe od systemów przetwarzających wrażliwe dane, niezależnie od używanego protokołu. Ogranicza to wpływ pojedynczego, zainfekowanego urządzenia na całą sieć.

W miarę jak ekosystemy bezprzewodowe nieustannie się rozrastają, specjaliści ds. bezpieczeństwa muszą rozumieć te technologie, rozpoznawać zagrożenia, jakie ze sobą niosą, i stosować odpowiednie środki w celu właściwego zarządzania nimi i ich zabezpieczania.

W tej sali omówiliśmy podstawy sieci bezprzewodowych na wysokim poziomie, w tym różne rodzaje technologii bezprzewodowych, które są obecnie powszechnie stosowane. Omówiliśmy również zagrożenia bezpieczeństwa związane z tymi technologiami oraz środki, które można wdrożyć, aby zmniejszyć ich narażenie na zagrożenia.

Podstawowa wiedza zdobyta w tej sali przygotuje Cię do zajęć, podczas których dogłębniej poznasz scenariusze ataków na sieci bezprzewodowe. Aby pogłębić wiedzę na temat ataków na sieci bezprzewodowe, zdecydowanie zalecamy ukończenie następujących sal:

- [Hackowanie Wi-Fi 101](https://tryhackme.com/room/wifihacking101)
- [Wprowadzenie doIoTPentesting](https://tryhackme.com/room/iotintro)

## Kluczowe terminy omówione w tym pokoju

| Termin      | Definicja                                                                                                                                                                                                                         |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SSID        | Identyfikator zestawu usług. Czytelna dla człowieka nazwa sieci Wi-Fi.                                                                                                                                                            |
| BSSID       | Podstawowy identyfikator zestawu usług. Adres MAC punktu dostępu bezprzewodowego.                                                                                                                                                 |
| WEP         | Wired Equivalent Privacy. Oryginalny protokół bezpieczeństwa Wi-Fi, obecnie wycofany ze względu na fundamentalne słabości szyfrowania opartego na RC4, które umożliwia odzyskanie klucza sieciowego w ciągu kilku minut.          |
| WPA         | Wi-Fi Protected Access. Pośredni protokół bezpieczeństwa wprowadzony jako zamiennik WEP, wykorzystujący TKIP do szyfrowania. Zastąpiony przez WPA2 i WPA3.                                                                        |
| WPA2        | Wi-Fi Protected Access 2. Protokół bezpieczeństwa wykorzystującyAESszyfrowanie w celu ochrony ruchu Wi-Fi.                                                                                                                        |
| WPA3        | Wi-Fi Protected Access 3. Następca WPA2, wprowadzający funkcję jednoczesnego uwierzytelniania równorzędnych (SAE) w celu ochrony przed atakami słownikowymi w trybie offline.                                                     |
| MITM        | Man-in-the-Middle. Atak, w którym przeciwnik potajemnie przechwytuje i potencjalnie modyfikuje komunikację między dwiema stronami, które sądzą, że komunikują się bezpośrednio ze sobą.                                           |
| SAE         | Jednoczesne uwierzytelnianie równorzędnych. Mechanizm wymiany kluczy używany w WPA3, który zastępuje czteroetapowe uzgadnianie bardziej odpornym procesem uwierzytelniania.                                                       |
| BLE         | Bluetooth Low Energy. Energooszczędna odmiana technologii Bluetooth przeznaczona dla urządzeń IoT, które przesyłają niewielkie ilości danych w sposób przerywany.                                                                 |
| SSP         | Bezpieczne i proste parowanie. Mechanizm parowania Bluetooth wprowadzony w wersji 2.1, który wykorzystuje algorytm eliptycznej krzywej Diffie'ego-Hellmana do ochrony przed pasywnym podsłuchem.                                  |
| RFID        | Identyfikacja radiowa. Technologia wykorzystująca pola elektromagnetyczne do identyfikacji i śledzenia znaczników przymocowanych do obiektów.                                                                                     |
| NFC         | Komunikacja bliskiego zasięgu (Near-Field Communication). Standard bezprzewodowy krótkiego zasięgu działający na częstotliwości 13,56 MHz, który obsługuje dwukierunkową komunikację między urządzeniami w odległości około 5 cm. |
| Zigbee      | Protokół sieciowy o niskim poborze mocy i krótkim zasięgu, używany w inteligentnych urządzeniach domowych, takich jak oświetlenie i czujniki.                                                                                     |
| Z-Wave      | Bezprzewodowy protokół do automatyzacji domu, który wykorzystuje standardowe pasmo częstotliwości i strukturę zabezpieczeń S2 do szyfrowanej komunikacji urządzeń.                                                                |
| LoRa        | Duży zasięg. Technologia bezprzewodowa o niskim poborze mocy przeznaczona do przesyłania niewielkich ilości danych na odległość kilku kilometrów w systemach IoT.                                                                 |
| Podczerwony | Bezprzewodowa metoda komunikacji, która wykorzystuje sygnały świetlne do przesyłania danych na niewielką odległość, w linii wzroku, pomiędzy nadajnikiem i odbiornikiem, powszechnie stosowana w pilotach zdalnego sterowania.    |
