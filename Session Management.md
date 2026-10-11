---

W tym pokoju dowiesz się o zarządzaniu sesjami. Myśląc o interakcjach z aplikacjami internetowymi, powinieneś zdać sobie sprawę, że nie podajesz aplikacji internetowej swojej nazwy użytkownika i hasła przy każdym żądaniu. Zamiast tego, po uwierzytelnieniu otrzymujesz sesję. Ta sesja jest używana przez aplikację internetową do przechowywania Twojego stanu, śledzenia Twoich działań i decydowania, czy możesz wykonywać dane działanie. Zarządzanie sesjami ma na celu zapewnienie prawidłowego wykonania tych kroków. W przeciwnym razie atakujący może naruszyć Twoją sesję i skutecznie ją przejąć!  

Wymagania wstępne

- [Wprowadzenie do hakowania stron internetowych](https://tryhackme.com/module/intro-to-web-hacking)
- [Wyliczanie i siłowe atakowanie](https://tryhackme.com/r/room/enumerationbruteforce)

Cele edukacyjne

- Zrozum, czym jest zarządzanie sesjami
- Poznaj różnice między uwierzytelnianiem a autoryzacją i dowiedz się, jaką rolę odgrywają one w zarządzaniu sesjami.
- Poznaj dwie główne metody zarządzania sesjami
- Dowiedz się więcej o cyklu zarządzania sesjami
- Dowiedz się, jak w praktyce wykorzystać podatne na ataki implementacje zarządzania sesjami

Zanim omówimy wszystko, co może pójść nie tak, musimy poznać zasady zarządzania sesjami. Jak wspomniano w poprzednim zadaniu, nie wysyłasz nazwy użytkownika i hasła z każdym żądaniem. Jednak…HTTPProtokół jest z natury bezstanowy. Sesje służą zatem do śledzenia użytkowników podczas korzystania z aplikacji internetowej. Zarządzanie sesjami to proces zarządzania tymi sesjami i zapewniania ich bezpieczeństwa.

Cykl życia zarządzania sesjami

Najlepszym sposobem na zdobycie wiedzy na temat zarządzania sesjami jest wykorzystanie cyklu życia zarządzania sesjami, jak pokazano na poniższej animacji.

**Tworzenie sesji**

Można by pomyśleć, że ten pierwszy krok w cyklu życia następuje dopiero po podaniu danych uwierzytelniających, takich jak nazwa użytkownika i hasło. Jednak w wielu aplikacjach internetowych początkowa sesja jest już tworzona w momencie uruchomienia aplikacji. Dzieje się tak, ponieważ niektóre aplikacje chcą śledzić Twoje działania jeszcze przed uwierzytelnieniem. Jednak w tym artykule skupimy się głównie na sesjach uwierzytelnionych. Po podaniu nazwy użytkownika i hasła otrzymujesz wartość sesji, która jest następnie wysyłana z każdym nowym żądaniem. Sposób generowania, używania i przechowywania tych wartości sesji ma kluczowe znaczenie dla bezpieczeństwa tworzenia sesji.  

**Śledzenie sesji**

Po otrzymaniu wartości sesji jest ona przesyłana z każdym nowym żądaniem. Dzięki temu aplikacja internetowa może śledzić Twoje działania, nawet jeśli…HTTPProtokół ten ma charakter bezstanowy. Po każdym wysłaniu żądania aplikacja internetowa może pobrać wartość sesji z żądania i przeprowadzić wyszukiwanie po stronie serwera, aby dowiedzieć się, do kogo należy sesja i jakie ma uprawnienia. W przypadku problemów z procesem śledzenia sesji, może to umożliwić atakującemu przejęcie sesji lub podszycie się pod inną osobę.  

**Wygaśnięcie sesji**

Ponieważ HTTPPonieważ protokół jest bezstanowy, może się zdarzyć, że użytkownik aplikacji internetowej nagle przestanie z niej korzystać. Na przykład, możesz zamknąć kartę lub całą przeglądarkę. Ponieważ protokół jest bezstanowy, aplikacja internetowa nie ma możliwości dowiedzenia się o tym fakcie. Właśnie tutaj pojawia się problem wygaśnięcia sesji. Sama wartość sesji powinna mieć przypisany czas życia. Jeśli czas życia wygaśnie i prześlesz starą wartość sesji do aplikacji internetowej, powinna ona zostać odrzucona, ponieważ sesja powinna już wygasnąć. Zamiast tego powinieneś zostać przekierowany na stronę logowania w celu ponownego uwierzytelnienia i rozpoczęcia cyklu zarządzania sesją od nowa!  

**Zakończenie sesji**

Jednak w niektórych przypadkach użytkownik może wymusić wylogowanie. W takim przypadku aplikacja internetowa powinna zakończyć sesję użytkownika. Chociaż jest to podobne do wygaśnięcia sesji, jest to wyjątkowe w tym sensie, że nawet jeśli czas życia sesji jest nadal ważny, sama sesja powinna zostać zakończona. Problemy w tym procesie mogą umożliwić atakującemu uzyskanie trwałego dostępu do konta.  

W tej sali przyjrzymy się, co może pójść nie tak w każdym z tych stanów sesji. Chcemy zapewnić bezpieczeństwo sesji w całym cyklu życia. Najpierw jednak musimy omówić nieco więcej teorii.

Aby zrozumieć typowe luki w zabezpieczeniach zarządzania sesjami, najpierw musimy przyjrzeć się uwierzytelnianiu i autoryzacji. Choć brzmią podobnie i często są mylone, każdy z nich odgrywa kluczową i unikalną rolę w zarządzaniu sesjami. Aby lepiej wyjaśnić różnice, przyjrzyjmy się…IAAA model:

![Model IAAA](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722529402239.png)  

Identyfikacja

Identyfikacja to proces weryfikacji tożsamości użytkownika. Zaczyna się on od podania przez użytkownika konkretnej tożsamości. W większości aplikacji internetowych odbywa się to poprzez podanie nazwy użytkownika. Użytkownik potwierdza, że ​​jest osobą powiązaną z daną nazwą użytkownika. Niektóre aplikacje używają unikatowych nazw użytkowników, podczas gdy inne przyjmują jako nazwę użytkownika adres e-mail.  

Uwierzytelnianie

Uwierzytelnianie to proces weryfikacji, czy użytkownik jest tym, za kogo się podaje. Podczas identyfikacji podajesz nazwę użytkownika, natomiast w celu uwierzytelnienia dostarczasz dowód, że jesteś tym, za kogo się podajesz. Na przykład, możesz podać hasło powiązane z podaną nazwą użytkownika. Aplikacja internetowa może potwierdzić te informacje, jeśli są prawidłowe; w tym momencie rozpoczyna się tworzenie sesji.  

Upoważnienie

Autoryzacja to proces upewniania się, że dany użytkownik posiada uprawnienia wymagane do wykonania żądanej czynności. Na przykład, chociaż wszyscy użytkownicy mogą przeglądać dane, tylko nieliczni mogą je modyfikować. W cyklu zarządzania sesją śledzenie sesji odgrywa kluczową rolę w procesie autoryzacji.  

Odpowiedzialność

Rozliczalność to proces tworzenia rejestru działań podejmowanych przez użytkowników. Powinniśmy śledzić sesję użytkownika i rejestrować wszystkie działania wykonywane w ramach danej sesji. Informacje te odgrywają kluczową rolę w przypadku incydentu bezpieczeństwa, pozwalając na złożenie w całość zdarzeń.  

IAAAi zarządzanie sesjami

Skoro rozumiesz już różnice między uwierzytelnianiem a autoryzacją, wróćmy do zarządzania sesjami. Uwierzytelnianie odgrywa rolę w procesie tworzenia sesji. Autoryzacja staje się istotna, aby zweryfikować, czy użytkownik powiązany z daną sesją ma uprawnienia do wykonania żądanej czynności. Odpowiedzialność jest dla nas kluczowa, aby móc poskładać w całość to, co faktycznie wydarzyło się w incydencie, co oznacza, że ​​ważne jest, aby żądania były rejestrowane, a także aby sesja powiązana z każdym żądaniem była rejestrowana.

Ostatnim tematem, który należy omówić przed zagłębieniem się w bezpieczeństwo zarządzania sesjami, jest rodzaj używanych sesji. Dwa główne podejścia to pliki cookie i tokeny, z których każde ma swoje zalety i wady.

Zarządzanie sesjami oparte na plikach cookie

Zarządzanie sesjami oparte na plikach cookie jest często nazywane staromodnym sposobem zarządzania sesjami. Gdy aplikacja internetowa chce rozpocząć śledzenie, w odpowiedzi wysyłana jest wartość nagłówka Set-Cookie. Przeglądarka zinterpretuje ten nagłówek, aby zapisać nową wartość pliku cookie. Przyjrzyjmy się takiemu nagłówkowi Set-Cookie:

`Set-Cookie: session=12345;`  

Twoja przeglądarka utworzy wpis pliku cookie o nazwie, której `session`wartość `12345`będzie ważna dla domeny, z której plik cookie został pobrany. Do tego nagłówka można również dodać kilka atrybutów. Aby dowiedzieć się więcej o wszystkich, zapoznaj się z informacjami [tutaj.(otwiera się w nowej karcie)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie), ale niektóre z godnych uwagi to:

- **Bezpieczny** – informuje przeglądarkę, że plik cookie może być przesyłany wyłącznie przez zweryfikowane kanały HTTPS. W przypadku błędów certyfikatu lub użycia protokołu HTTP wartość pliku cookie nie zostanie przesłana.
- **HTTPOnly** – informuje przeglądarkę, że wartość pliku cookie nie może zostać odczytana przez JavaScript po stronie klienta.
- **Wygaśnięcie** – informuje przeglądarkę, kiedy wartość pliku cookie nie będzie już ważna i powinna zostać usunięta.
- **SameSite** – informuje przeglądarkę, czy plik cookie może być przesyłany w żądaniach między witrynami, aby pomóc w ochronie przed atakami CSRF.  

Kluczową kwestią, o której należy pamiętać w przypadku uwierzytelniania opartego na plikach cookie, jest to, że przeglądarka sama decyduje, kiedy określona wartość pliku cookie zostanie wysłana wraz z żądaniem. Po sprawdzeniu domeny i atrybutów pliku cookie, przeglądarka podejmuje decyzję, a plik cookie jest dołączany automatycznie, bez żadnego dodatkowego kodu JavaScript po stronie klienta.  

Zarządzanie sesjami oparte na tokenach

Zarządzanie sesjami oparte na tokenach to stosunkowo nowa koncepcja. Zamiast korzystać z funkcji automatycznego zarządzania plikami cookie przeglądarki, opiera się ono na kodzie po stronie klienta. Po uwierzytelnieniu aplikacja internetowa dostarcza token w treści żądania. Za pomocą kodu JavaScript po stronie klienta token ten jest następnie przechowywany w pamięci lokalnej przeglądarki.

Po wysłaniu nowego żądania kod JavaScript musi załadować token z pamięci masowej i dołączyć go jako nagłówek. Jednym z najpopularniejszych typów tokenów są JSON Web Tokens (JWT), które są przesyłane przez nagłówek `Authorization: Bearer`. Ponieważ jednak nie korzystamy z wbudowanych funkcji zarządzania plikami cookie przeglądarki, sytuacja przypomina nieco Dziki Zachód, gdzie wszystko jest dozwolone. Chociaż istnieją standardy, nic nie stoi na przeszkodzie, aby ktokolwiek się do nich stosował.  

Korzyści i wady

Zalety i wady każdej z tych metod są ze sobą bezpośrednio powiązane. Przyjrzyjmy się im bliżej:

|                                                                                                                                                                          |                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Zarządzanie sesjami plików cookie**                                                                                                                                    | **Zarządzanie sesjami oparte na tokenach**                                                                                                                                                            |
| Plik cookie jest automatycznie wysyłany przez przeglądarkę przy każdym żądaniu                                                                                           | Token musi zostać przesłany jako nagłówek przy każdym żądaniu za pomocą JavaScript po stronie klienta                                                                                                 |
| Atrybuty plików cookie mogą być używane w celu zwiększenia ochrony przeglądarki przed plikami cookie                                                                     | Tokeny nie mają automatycznych zabezpieczeń, dlatego należy je chronić przed ujawnieniem                                                                                                              |
| Pliki cookie mogą być podatne na konwencjonalne ataki po stronie klienta, takie jak:CSRF, w którym przeglądarka zostaje oszukana i wysyła żądanie w imieniu użytkownika. | Ponieważ token nie jest automatycznie dodawany do żadnego żądania i nie może być odczytany z pamięci lokalnej przez inne domeny, typowe ataki po stronie klienta, takie jakCSRFsą zablokowane.        |
| Ponieważ pliki cookie są przypisane do konkretnej domeny, ich bezpieczne używanie w zdecentralizowanych aplikacjach internetowych może być trudne.                       | Tokeny sprawdzają się w zdecentralizowanych aplikacjach internetowych, ponieważ są zarządzane za pomocą JavaScript i często mogą zawierać wszystkie informacje wymagane do weryfikacji samego tokena. |

Nadszedł wreszcie czas, aby dowiedzieć się więcej o bezpieczeństwie zarządzania sesjami. Wracając do cyklu zarządzania sesjami, przyjrzyjmy się, co może pójść nie tak na każdym etapie.

Tworzenie sesji

Najwięcej luk w zabezpieczeniach może pojawić się podczas tworzenia sesji. Przyjrzyjmy się kilku najczęstszym.

**Słabe wartości sesji**

W dzisiejszych czasach rzadziej obserwuje się słabe wartości sesji, ponieważ konsekwentnie stosuje się ramy. Jednak wraz z rozwojem LLM i innychSztuczna inteligencjarozwiązań wspomagających kodowanie, zdziwiłbyś się, jak często te stare luki w zabezpieczeniach znów się ujawniają.

Jeśli wdrożono niestandardowy mechanizm tworzenia sesji, istnieje duże prawdopodobieństwo, że wartości sesji będą możliwe do odgadnięcia. Dobrym przykładem jest mechanizm, który po prostu koduje nazwę użytkownika w formacie base64 jako wartość sesji. Jeśli atakujący potrafi odtworzyć proces tworzenia sesji, może generować lub odgadywać wartości sesji, aby przejąć konta legalnych użytkowników.  

**Kontrolowane wartości sesji**

W niektórych tokenach, takich jak JWT, dostępne są wszystkie istotne informacje niezbędne do utworzenia i weryfikacji ważności tokena. Jeśli środki bezpieczeństwa, takie jak weryfikacja podpisu tokena lub zapewnienie, że sam podpis został utworzony w sposób bezpieczny, atakujący będzie mógł wygenerować własny token. Tego typu ataki zostaną omówione bardziej szczegółowo w kolejnym artykule.  

**Utrwalenie sesji**

Pamiętasz aplikację internetową, która przydzieliła Ci sesję przed uwierzytelnieniem? Te aplikacje internetowe mogą być podatne na zjawisko zwane fiksacją sesji. Jeśli wartość Twojej sesji nie zostanie odpowiednio zmieniona po uwierzytelnieniu, odpowiednio pozycjonowany atakujący może ją zarejestrować, gdy nadal nie jesteś uwierzytelniony, i czekać na Twoje uwierzytelnienie, aby uzyskać dostęp do sesji.  

**Niebezpieczna transmisja sesji**

W nowoczesnych środowiskach serwer uwierzytelniania i serwery aplikacji często są odrębne. Weźmy na przykład pod uwagę logowanie jednokrotne (SSO) rozwiązań. Jedna aplikacja jest używana do uwierzytelniania w kilku innych aplikacjach internetowych. Aby ten proces zadziałał, materiał sesji musi zostać przesłany z serwera uwierzytelniania do serwera aplikacji za pośrednictwem przeglądarki. Podczas tej transmisji mogą jednak pojawić się pewne problemy, które naraziłyby informacje o sesji na atak. Najczęstszym przypadkiem jest niebezpieczne przekierowanie, gdzie atak może kontrolować adres URL, do którego nastąpi przekierowanie po uwierzytelnieniu. Może to umożliwić atakowi przejęcie kontroli nad sesją. Nie dotyczy to tylko niestandardowych implementacji, ale rozwiązań Oracle.SSOrozwiązanie zawierało [ogromny błąd, który umożliwił zaistnienie takiej sytuacji(otwiera się w nowej karcie)](https://krbtgt.pw/oracle-oam-10g-session-hijacking/).  

Śledzenie sesji

Śledzenie sesji to druga co do wielkości przyczyna luk w zabezpieczeniach. Przyjrzyjmy się temu bliżej.

**Ominięcie autoryzacji**

Omijanie autoryzacji występuje, gdy nie przeprowadza się wystarczającej liczby kontroli, czy użytkownik ma prawo wykonać żądaną czynność. W istocie prowadzi to do nieprawidłowego śledzenia sesji użytkownika i powiązanych z nią uprawnień. Warto również omówić dwa rodzaje ominięć autoryzacji:

- Obejście pionowe – możesz wykonać akcję zarezerwowaną dla bardziej uprzywilejowanego użytkownika
- Obejście poziome – możesz wykonać czynność, którą masz prawo wykonać, ale na zestawie danych, na którym nie powinieneś mieć prawa jej wykonać  

W większości aplikacji obrona przed obejściami pionowymi jest łatwa, ponieważ wykorzystuje dekoratory funkcji i konfiguracje kontroli dostępu oparte na ścieżkach. Jednak w przypadku obejść poziomych użytkownik wykonuje czynność, którą powinien mieć prawo wykonać. Problem polega na tym, że wykonuje ją na danych należących do kogoś innego. Aby temu zaradzić, wymagany jest kod weryfikujący tożsamość użytkownika (wyodrębnioną z jego sesji), żądane przez niego dane oraz to, czy ma on prawo żądać lub modyfikować zbiór danych.  

**Niewystarczające rejestrowanie**

Kluczowym problemem podczas incydentów jest brak wystarczających informacji, aby poskładać atak w całość. Chociaż wiele logów będzie miało miejsce na poziomie infrastruktury, logowanie aplikacji może mieć kluczowe znaczenie dla zrozumienia, co poszło nie tak. W przypadku braku działań wykonanych przez daną sesję i możliwości odtworzenia tej sesji z użytkownikiem, może to pozostawić luki w śledztwie, których nie da się wypełnić. Warto również upewnić się, że logi obejmują zarówno działania zaakceptowane, jak i odrzucone. W przypadku ataku polegającego na przejęciu sesji, działania te będą wydawać się uzasadnione. Dlatego samo rejestrowanie odrzuconych działań nie wystarczy, aby uzyskać obraz sytuacji.  

Wygaśnięcie sesji

Wygasanie sesji ma tylko jedną lukę: zbyt długi czas wygaśnięcia sesji. Sesję należy traktować jak bilet do kina. Każdej nocy wyświetlany jest ten sam film, ale nie chcemy, aby ktoś mógł ponownie użyć tego samego biletu. To samo dotyczy sesji – musimy upewnić się, że czas wygaśnięcia sesji uwzględnia specyfikę danej aplikacji. Aplikacja bankowa powinna mieć krótszy czas życia sesji niż klient poczty internetowej.

Ponadto, w przypadku sesji o długim czasie trwania, takich jak sesje klienta poczty internetowej, sama sesja powinna potwierdzać lokalizację, w której jest używana. W przypadku zmiany tej lokalizacji (co może wskazywać na przejęcie sesji), sesja powinna zostać zakończona.  

Zakończenie sesji

W przypadku kończenia sesji kluczowym problemem jest sytuacja, gdy sesje nie są prawidłowo zamykane po stronie serwera podczas wylogowywania. Załóżmy, że atakujący przejąłby sesję użytkownika. W takim przypadku, nawet jeśli użytkownik dowiedziałby się o problemie, bez możliwości unieważnienia sesji po stronie serwera, nie miałby możliwości usunięcia dostępu atakującego. Może to jednak stanowić poważny problem w przypadku tokenów, których czas życia jest osadzony w samym tokenie. W takich przypadkach token może zostać dodany do listy blokowanych w celu weryfikacji. Niektóre aplikacje idą o krok dalej, umożliwiając podgląd i zamykanie wszystkich sesji użytkownika. Ponadto, po pomyślnym zresetowaniu hasła, zaleca się również zamknięcie wszystkich sesji, aby umożliwić użytkownikowi odzyskanie pełnej kontroli nad swoim kontem.

Wykorzystując zdobytą wiedzę, czas zbadać, jak można zamapować i przetestować cykl życia zarządzania sesjami. Uruchom maszynę, naciskając przycisk „ **Start Machine”** na górze tego zadania i zacznijmy hakować! Możesz uzyskać dostęp do…Maszyna wirtualnaużywając **AttackBox** lub twojego**VPN**połączenie.

Wyliczenie

Aby skutecznie wykorzystać podatny na ataki cykl zarządzania sesjami, musimy najpierw sami go zmapować i sporządzić szczegółowe notatki. Po zrozumieniu zamierzonego cyklu, możemy zacząć szukać słabych punktów. W tej demonstracji wykorzystamy wbudowane narzędzia przeglądarki. Można jednak również skorzystać z bardziej zaawansowanych narzędzi do testowania aplikacji internetowych, takich jak Burp. Przejdźmy do naszej aplikacji pod adresem[http://IP_MASZYNY(otwiera się w nowej karcie)](http://machine_ip/)najpierw powinniśmy zobaczyć następującą stronę:

![Panel logowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722450848675.png)

Po pierwsze, zauważamy, że podczas pierwszej wizyty na stronie nie otrzymujemy żadnych plików cookie ani tokenów. To oznacza, że ​​sesje bez uwierzytelnienia najprawdopodobniej nie są śledzone. Po kliknięciu przycisku „Zarejestruj się” widzimy, że istnieją dwie główne rejestracje:

- Uczeń – może z tego skorzystać każdy, aby utworzyć profil
- Wykładowca – Wymaga kodu weryfikacyjnego w celu rejestracji

To pokazuje nam, że nawet bez użycia technik siłowych możemy rozpocząć cykl zarządzania sesją, tworząc konto studenckie. Utwórzmy konto studenckie i zobaczmy, co się stanie:

![Panel rejestracyjny](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722451429592.png)

Po utworzeniu konta użytkownika pojawia się komunikat o utworzeniu konta i wracamy na stronę logowania. Zalogujmy się jako nasz użytkownik i monitorujmy ruch sieciowy:

![Żądanie logowania](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722451429583.png)

To mówi nam sporo informacji:

- Pliki cookie są używane do zarządzania sesjami.
- Ustawiona jest flaga HTTPOnly, co oznacza, że ​​nie będziemy mogli wykorzystać JavaScript do odczytania wartości pliku cookie.

Dzięki temu uwierzytelnianiu możemy teraz uzyskać dostęp do większej funkcjonalności:

![Widok pulpitu nawigacyjnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722451873193.png)

Korzystając z nawigacji menu i analizując ruch sieciowy, możemy zobaczyć, że śledzenie sesji jest wymuszane za pomocą pliku cookie przesyłanego z każdym żądaniem:

![Żądanie modułów](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722451873192.png)

Należy pamiętać, że nagłówki mogą się nieznacznie różnić w zależności od używanej przeglądarki. Ciekawostką jest jednak to, że nawet jeśli czas wygaśnięcia pliku cookie jeszcze nie upłynął, ten sam nagłówek pliku cookie jest używany do odświeżania pliku cookie do dokładnie tej samej wartości i dalszego wydłużania jego żywotności. Może to wskazywać na trwały plik cookie. Zobaczmy, co się stanie, gdy usuniemy ten plik cookie. W sekcji „Przechowywanie” usuń plik cookie i ponownie wyślij żądanie modułu:

![Żądanie modułów](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722452082078.png)

Wygląda na to, że prośba nadal działa? Jednak jeśli przyjrzysz się bliżej, zobaczysz, że teraz widzimy tylko moduły, ale nie liczbę zapisanych studentów ani potencjalne testy:

![Widok pulpitu nawigacyjnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722452094296.png)

Sugeruje to, że być może będziemy musieli przeprowadzić dalsze dochodzenie, aby dokładnie określić, do czego mamy dostęp z perspektywy całkowicie nieuwierzytelnionej. Wymagałoby to dalszych badań, aby w pełni zmapować cykl życia zarządzania sesjami. Jednak uprościmy sprawę. Przyjrzyjmy się funkcji wylogowania. Po naciśnięciu przycisku wylogowania widać, że nasza sesja została usunięta po stronie klienta:

![Pamięć podręczna plików cookie](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722452255723.png)

Powinniśmy jednak sprawdzić, czy sesja jest również kończona po stronie serwera. Możesz ponownie uwierzytelnić się w aplikacji i zastąpić nowy plik cookie starą wartością pliku cookie. Wygląda jednak na to, że kończenie sesji działa w miarę sprawnie, ponieważ po odświeżeniu strony pojawia się błąd wewnętrzny serwera 500. To wskazuje, że coś jest nie tak, ponieważ nieprawidłowa sesja nie powinna prowadzić do wewnętrznego błędu serwera. Przyjrzyjmy się temu bliżej.

Przyjrzyjmy się bliżej naszym wcześniejszym twierdzeniom. Jeśli przejdziemy do pamięci lokalnej, zauważymy, że przechowywana jest tam spora ilość danych:

![Pamięć podręczna tokenów](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722454261803.png)

Poeksperymentujmy, aktualizując naszą Rolę użytkownika ze studenta na wykładowcę i odświeżając stronę:

![Widok pulpitu nawigacyjnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1722454362144.png)

Chociaż mamy teraz dostęp do większej liczby kart, wydaje się, że nie mamy dostępu do większej ilości informacji, ponieważ widzimy wszystkich uczniów lub próby testów. Rozwińmy to dalej, aktualizując naszą rolę w wartości użytkownika z 2 do 3. Niestety, nadal daje to te same wyniki. Jest jednak więcej wartości do wykorzystania, takich jak nasz identyfikator i nazwa użytkownika. Będziemy musieli do tego wrócić. Jednak te nowe informacje sugerują, że sesje mogą być zarządzane nie tylko za pomocą pliku cookie, ale także za pomocą informacji o tokenach.

Mamy już zaplanowaną mapę cyklu zarządzania sesjami. Przyjrzyjmy się temu:

|   |   |
|---|---|
|**Faza cyklu życia**|**Obserwacja**|
|Tworzenie sesji|Stosowane jest połączenie zarządzania sesjami opartego na plikach cookie i tokenach|
|Tworzenie sesji|Przy każdej próbie logowania podawana jest nowa wartość sesji|
|Tworzenie sesji|Sama wartość sesji wydaje się być wystarczająco losowa|
|Śledzenie sesji|Nieautoryzowane działania nie są śledzone za pośrednictwem sesji|
|Śledzenie sesji|Plik cookie jest wysyłany w każdym żądaniu śledzenia|
|Śledzenie sesji|Kilka żądań można wysłać bez pliku cookie|
|Śledzenie sesji|Początkowe wartości tokenów ładowane po uwierzytelnieniu określają widoczne informacje|
|Wygaśnięcie sesji|Występuje niezgodność pomiędzy czasem wygaśnięcia po stronie klienta i serwera|
|Wygaśnięcie sesji|Czas ważności jest niesamowicie długi|
|Zakończenie sesji|Użytkownicy mogą wymusić zakończenie sesji|
|Zakończenie sesji|Sesje są zamykane po stronie serwera, ale ponowne użycie starej sesji prowadzi do wewnętrznego błędu serwera|

Biorąc pod uwagę wszystkie te informacje, zgłosilibyśmy już następujące luki w zabezpieczeniach podczas oceny bezpieczeństwa:

- Nadmierne czasy trwania sesji

Musielibyśmy także zbadać dokładniej następujące kwestie:

- Kontrola dostępu do wszystkichAPIpunkty końcowe
- Rejestry aplikacji internetowych do rozliczania działań

Eksploatacja

Biorąc pod uwagę wszystkie powyższe informacje, wydaje się, że musimy przeprowadzić nieco więcej badań, aby sprawdzić, czy możemy uzyskać dostęp do poufnych danych. Korzystając z informacji o zabezpieczaniu cyklu zarządzania sesjami oraz informacji o zmapowanym cyklu, sprawdź, czy jako student możesz uzyskać dostęp do informacji o wykładowcy i odpowiedz na poniższe pytania.

Obrona

Aby bronić się przed tymi atakami, ważne jest wdrożenie bezpiecznego cyklu zarządzania sesjami. Chociaż na tym spotkaniu poruszono kilka kwestii, przyjrzyjmy się ich podsumowaniu:

- Wartości sesji muszą być przechowywane bezpiecznie, niezależnie od tego, czy są to pliki cookie czy tokeny.
- Same wartości sesji muszą być albo wystarczająco losowe i niemożliwe do odgadnięcia, albo korzystać z mechanizmu podpisu, aby mieć pewność, że nie da się ich zmienić.
- Sesje powinny być używane do śledzenia działań użytkownika i przeprowadzania kontroli autoryzacji, aby mieć pewność, że użytkownik może wykonać żądaną czynność.
- Sesje powinny wygasać po upływie określonego czasu, aby uniemożliwić ich wykorzystanie do stałego dostępu.
- Po naciśnięciu przycisku wylogowania sesja powinna zostać usunięta po stronie klienta i unieważniona po stronie serwera. W przeciwnym razie użytkownik nie będzie mógł zniszczyć swojej sesji, jeśli zostałaby ona naruszona.
