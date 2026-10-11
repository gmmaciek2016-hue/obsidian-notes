---

Każdy system operacyjny jest dostarczany z zestawem domyślnych konfiguracji. Administratorzy następnie nakładają na nie własne zmiany, instalując oprogramowanie, tworząc konta użytkowników, konfigurując usługi i ustawiając uprawnienia. Gdy te konfiguracje odbiegają od bezpiecznych praktyk, czy to z powodu niedopatrzenia, wygody, czy braku świadomości, wprowadzają one słabości, które można wykorzystać do eskalacji uprawnień na hoście. Ten obszar stanowi podstawę koncepcyjną do identyfikacji i zrozumienia tych słabości.

Eskalacja uprawnień to proces przechodzenia z konta o niższych uprawnieniach na konto o wyższych uprawnieniach w systemie. Jest to krytyczna faza niemal każdego testu penetracyjnego. Atakujący, który uzyskuje wstępny dostęp do hosta, zazwyczaj poprzez lukę w zabezpieczeniach aplikacji internetowej, phishinglub zainfekowana usługa, rzadko uzyskują dostęp administracyjny lub na poziomie roota. Kolejnym krokiem jest znalezienie sposobu na podniesienie uprawnień, a nieprawidłowo skonfigurowane hosty są jednym z najpewniejszych źródeł zagrożeń.

Istnieją zasadniczo dwie kategorie eskalacji uprawnień. Pierwsza to **eskalacja oparta na lukach w** zabezpieczeniach, która wykorzystuje błędy w oprogramowaniu, takie jak luki w jądrze, przepełnienia bufora w zainstalowanych aplikacjach lub znane luki bezpieczeństwa (CVE) w działających usługach. Druga to **eskalacja oparta na konfiguracji** , która wykorzystuje błędy w konfiguracji systemu, takie jak zbyt liberalne uprawnienia do plików, niezabezpieczone konfiguracje usług lub poświadczenia w postaci zwykłego tekstu pozostawione w dostępnych lokalizacjach.

![Diagram przedstawiający dwie kategorie eskalacji uprawnień, odchodzące od początkowego dostępu o niskich uprawnieniach. Lewa gałąź przedstawia eskalację opartą na lukach w zabezpieczeniach, która wymaga niezałatanego oprogramowania, dotyczy błędów na poziomie kodu, a łatanie usuwa dostępne wektory. Prawa gałąź przedstawia eskalację opartą na konfiguracji, która działa w systemach z pełną poprawką, dotyczy decyzji administratora i jest najczęstszym wektorem w praktyce.|700](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1774229168017.svg)

Ta sala koncentruje się na drugiej kategorii. W pełni załatany system bez znanych luk w zabezpieczeniach oprogramowania nadal może zostać poddany prostej eskalacji, jeśli jego konfiguracja jest nieodpowiednia. W praktyce eskalacja oparta na konfiguracji jest często bardziej powszechna i niezawodna niż eskalacja oparta na lukach w zabezpieczeniach, szczególnie w dojrzałych środowiskach, gdzie łatanie jest spójne, ale wzmacnianie zabezpieczeń nie.

W tej sali nie omówiono konkretnych technik eksploatacji. Zamiast tego, przedstawia ona wiedzę niezbędną przed skontaktowaniem się z hostem w celu eskalacji uprawnień. Dowiesz się, jak wygląda bezpieczna konfiguracja zgodnie z uznanymi w branży ramami, jakie kategorie błędów w konfiguracji zazwyczaj prowadzą do eskalacji oraz jak podejść do nowego hosta, stosując ustrukturyzowaną metodologię. Sale, które znajdują się w dalszej części tego modułu, pozwolą na praktyczne zastosowanie tych koncepcji Linux i systemy Windows.

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Wyjaśnij, na czym polega przegląd konfiguracji hosta-serwera i kiedy jest przeprowadzany w ramach testów penetracyjnych.
- Rozróżnij eskalację uprawnień opartą na podatności i eskalację uprawnień opartą na konfiguracji.
- Opisz cel i strukturę WNP Testy porównawcze i standardy DISA STIG oraz sposób, w jaki definiują one bezpieczną linię bazową konfiguracji.
- Określ rolę zautomatyzowanych narzędzi do audytu zgodności, takich jak Nessus, Lynis i OpenSCAP, w przeprowadzaniu przeglądów konfiguracji na dużą skalę.
- Określ główne kategorie błędnej konfiguracji hosta, które prowadzą do eskalacji uprawnień, w tym uprawnienia do plików, konfiguracje usług, zadania zaplanowane i przechowywanie poświadczeń.
- Zastosuj ustrukturyzowaną metodologię enumeracji, która odpowiada kategoriom porównawczym podczas nawiązywania kontaktu z nowym gospodarzem.

## Wymagania wstępne

Przed rozpoczęciem pracy w tym pokoju powinieneś zapoznać się z treściami, które są w nim omówione.[LinuxSale Fundamentals](https://tryhackme.com/module/linux-fundamentals) i [Windows Fundamentals](https://tryhackme.com/module/windows-fundamentals) . ZnajomośćLinuxwiersz poleceń, wiersz poleceń systemu Windows, podstawowysystem plikównawigacja, a koncepcja kont użytkowników i ich uprawnień jest wszędzie przyjęta.

Przegląd **konfiguracji** to ustrukturyzowany audyt ustawień, uprawnień, usług i zasad hosta, mierzony w odniesieniu do akceptowanego poziomu bazowego bezpieczeństwa. Jego celem jest identyfikacja odchyleń od tego poziomu bazowego, które mogą stanowić zagrożenie bezpieczeństwa. W kontekście testów penetracyjnych, odchylenia te stanowią potencjalne wektory eskalacji uprawnień.

Przeglądy konfiguracji różnią się od skanowania podatności. Skaner podatności, taki jak Nessus lub Qualys, identyfikuje znane luki w oprogramowaniu, brakujące poprawki i luki w zabezpieczeniach (CVE). Przegląd konfiguracji natomiast koncentruje się na sposobie konfiguracji systemu, a nie na oprogramowaniu, które jest w nim uruchomione. Host może przejść skanowanie podatności bez wykrycia, a mimo to nie przejść przeglądu konfiguracji, ponieważ jego usługi działają z nadmiernymi uprawnieniami, uprawnienia do plików są zbyt szerokie lub administratorzy pozostawili dane uwierzytelniające w dostępnych lokalizacjach.

Przeglądy konfiguracji różnią się również od tworzenia exploitów. Exploit atakuje konkretny błąd oprogramowania za pomocą specjalnie spreparowanego ładunku. Przegląd konfiguracji identyfikuje słabości w sposobie administrowania hostem. Umiejętności te się uzupełniają, ale podejście jest inne. Eksploatacja polega na pytaniu: „co jest zepsute w tym oprogramowaniu?”. Przegląd konfiguracji polega na pytaniu: „co jest nieprawidłowo skonfigurowane w tym systemie?”.

## Kiedy odbywają się przeglądy konfiguracji

Podczas testów penetracyjnych przeglądy konfiguracji zazwyczaj odbywają się w fazie posteksploatacyjnej, po uzyskaniu wstępnego dostępu do hosta. Gdy tester ma już powłokę w systemie docelowym, kolejnym celem jest zazwyczaj eskalacja uprawnień. Przegląd konfiguracji to systematyczny proces badania hosta pod kątem błędnych konfiguracji, które umożliwiają eskalację.

Przeglądy konfiguracji mogą być również przeprowadzane jako samodzielne oceny, niezależne od pełnego testu penetracyjnego. W tym kontekście zespół ds. bezpieczeństwa lub audytor otrzymuje uwierzytelniony dostęp do hostów i ocenia ich konfigurację w odniesieniu do zdefiniowanej linii bazowej. Wyniki są zgłaszane jako luki w zabezpieczeniach, a nie jako luki podatne na wykorzystanie, ale przeprowadzane kontrole są takie same.

## Perspektywa ofensywna

Z punktu widzenia obronnego, przeglądy konfiguracji są ćwiczeniem w zakresie zgodności i wzmacniania zabezpieczeń. Zespoły ds. bezpieczeństwa przeprowadzają audyty hostów, aby upewnić się, że spełniają one standardy organizacyjne, wymogi regulacyjne i najlepsze praktyki branżowe. Celem jest naprawa.

Z ofensywnego punktu widzenia proces jest identyczny, ale cel jest odwrotny. Tester penetracyjny przeprowadzający audyt konfiguracji hosta szuka tych samych odchyleń, które zasygnalizowałby audytor zgodności, ale z zamiarem ich wykorzystania, a nie naprawienia. Ta sama lista kontrolna, której administrator systemu używa do zabezpieczenia serwera, jest w rzeczywistości przewodnikiem enumeracyjnym dla atakującego.

![Diagram przedstawiający rozgałęzienie pojedynczego procesu przeglądu konfiguracji na dwie równoległe ścieżki. Lewa ścieżka reprezentuje audyt defensywny z trzema krokami: identyfikacja odchyleń, ocena ryzyka, a następnie działania naprawcze. Prawa ścieżka reprezentuje ofensywne wyliczenie z trzema krokami: identyfikacja słabości, ustalenie priorytetów, a następnie eskalacja uprawnień. Obie ścieżki wychodzą z tego samego procesu przeglądu konfiguracji.|700](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1774229201503.svg)

Ważne jest, aby zrozumieć tę dwoistość. Kiedy dowiesz się, jak wygląda bezpieczna konfiguracja, jednocześnie dowiesz się, jak wygląda konfiguracja niebezpieczna i jak ją rozpoznać podczas interakcji.

## Jakie systemy są recenzowane

Przeglądy konfiguracji dotyczą każdego systemu, który można poddać audytowi. Przeglądowi konfiguracji podlegają stacje robocze, serwery plików, kontrolery domeny, serwery WWW, serwery baz danych, urządzenia sieciowe i instancje chmurowe. Szczegółowe kontrole różnią się w zależności od systemu operacyjnego i roli, ale kategorie błędów konfiguracji są zasadniczo spójne na wszystkich platformach. Linux Serwer WWW i kontroler domeny Windows mają uprawnienia do plików, konfiguracje usług, konta użytkowników i magazyn poświadczeń, które można audytować w oparciu o dane bazowe.

Poziom **bazowy bezpieczeństwa** to udokumentowany standard, który definiuje sposób konfiguracji systemu, aby zapewnić akceptowalny poziom bezpieczeństwa. Zamiast polegać na indywidualnej ocenie tego, co stanowi „bezpieczną” konfigurację, organizacje przyjmują poziomy bazowe, które zawierają konkretne, mierzalne zalecenia dla każdego konfigurowalnego aspektu systemu, od zasad dotyczących haseł i uprawnień do plików, po konfiguracje usług i ustawienia sieciowe.

Kilka uznanych w branży ram publikuje te dane bazowe. Dwa najczęściej cytowane to: WNPTesty porównawcze i wskaźniki DISA STIG.

## WNPPunkty odniesienia

Centrum **Bezpieczeństwa Internetu (WNP)** publikuje testy konfiguracji dla szerokiej gamy systemów operacyjnych, platform chmurowych, aplikacji i urządzeń sieciowych. WNPBenchmarki opracowywane są w drodze konsensusu, w którym uczestniczą specjaliści ds. bezpieczeństwa z sektora rządowego, przemysłowego i akademickiego. Każdy benchmark zawiera setki indywidualnych rekomendacji, z których każda zawiera opis, uzasadnienie wyjaśniające ryzyko bezpieczeństwa, którego dotyczy, procedurę audytu w celu sprawdzenia zgodności oraz procedurę naprawczą w celu skorygowania odchyleń.

WNPBenchmarki definiują dwa poziomy profilu. Rekomendacje **poziomu 1** to praktyczne, szeroko stosowane ustawienia, które można wdrożyć w większości systemów bez znaczącego wpływu na funkcjonalność. Rekomendacje **poziomu 2** zapewniają głębsze wzmocnienie obrony, ale mogą ograniczać pewne funkcjonalności lub wymagać bardziej starannego testowania przed wdrożeniem. Organizacja zazwyczaj wybiera jeden z tych profili jako punkt odniesienia i porównuje go z hostami.

Na przykład, WNPBenchmark dla Ubuntu Linux może zawierać zalecenie poziomu 1, zgodnie z którym `PermitRootLogin`dyrektywa w konfiguracji serwera SSH musi być ustawiona na `no`. Uzasadnienie wyjaśnia, że ​​zezwolenie na bezpośrednie logowanie roota przezSSHZapewnia atakującemu, który uzyska lub zdobędzie hasło roota metodą brute force, natychmiastowy dostęp uprzywilejowany, omijając wszelkie uprawnienia wynikające z indywidualnych kont użytkowników. Procedura audytu określa polecenie sprawdzenia bieżącego ustawienia w `sshd_config`, a procedura naprawcza zapewnia zmianę konfiguracji w celu jego wyłączenia.

## DISA STIGs

Agencja **Systemów Informacyjnych Departamentu Obrony (DISA)** , będąca częścią Departamentu Obrony USA, publikuje **Przewodniki Implementacji Technicznej Bezpieczeństwa (STIG)** . STIG określają wymagania dotyczące wzmocnienia systemów wykorzystywanych w środowiskach rządowych i wojskowych. Są one bardziej rygorystyczne niż WNPPunkty odniesienia są obowiązkowe dla systemów w ramach sieci rządu USA.

Każdy STIGZ nalezieniu przypisuje się kategorię ważności. Znaleziska **kategorii I** oznaczają najwyższe ryzyko, a ich wykorzystanie może bezpośrednio prowadzić do utraty poufności. uczciwość lub dostępność. Wyniki **CAT II** oznaczają średnie ryzyko, a wyniki **CAT III** – niskie. Ta kategoryzacja pomaga administratorom w ustalaniu priorytetów działań naprawczych i testerom penetracyjnym w ustaleniu, które odchylenia należy zbadać w pierwszej kolejności.

## Związek ze standardami zgodności

WNPBenchmarki i standardy DISA STIG nie istnieją w izolacji. Szersze ramy zgodności, takie jak PCI-DSS (dla przetwarzania kart płatniczych), ISO 27001 (dla zarządzania bezpieczeństwem informacji) iNIST800-53 (dla federalnych systemów informacyjnych) często się odwołujeWNPLubSTIGutwardzanie jako wytyczne dotyczące wdrażania własnych wymagań kontrolnych. Kiedy organizacja musi wykazać zgodność z PCI-DSS, konkretne wzmocnienie systemu, które wdraża, często jest zaczerpnięte bezpośrednio zWNPReper.

Dla testera penetracyjnego znajomość tych ram służy dwóm celom. Po pierwsze, definiują one, co organizacja docelowa uważa za „bezpieczne”, co oznacza, że ​​odchylenia od przyjętej linii bazowej są najbardziej wiarygodnymi ustaleniami w raporcie z testów penetracyjnych. Po drugie, dostarczają ustrukturyzowaną, kompleksową listę elementów do sprawdzenia, która jest znacznie bardziej wiarygodna niż…ogłoszenie-hoc wyliczenie.

Ręczne audytowanie hosta w oparciu o pełną WNPBenchmark lub DISASTIGjest czasochłonne. Pojedynczy benchmark może zawierać kilkaset indywidualnych rekomendacji, a środowiska korporacyjne mogą obejmować tysiące hostów do oceny. Zautomatyzowane narzędzia do kontroli zgodności rozwiązują ten problem, programowo skanując hosty pod kątem zdefiniowanych wartości bazowych i generując raporty sygnalizujące odchylenia.

W tym celu powszechnie wykorzystuje się kilka narzędzi. Każde z nich służy nieco innej grupie odbiorców i przypadkom użycia, ale wszystkie mają wspólny cel, jakim jest porównanie konfiguracji hosta ze znanym, dobrym standardem.

## Nessus

**Nessus** to komercyjny skaner podatności opracowany przez Tenable. Chociaż jest najbardziej znany ze skanowania podatności, Nessus oferuje również funkcję audytu zgodności. Administratorzy mogą skonfigurować Nessus do skanowania hostów pod kątem…WNPBenchmarki, DISA STIG i niestandardowe zasady audytu. Wynikowy raport zgodności zawiera listę wszystkich kontroli, ich status zaliczenia lub niezaliczenia oraz wskazówki dotyczące działań naprawczych w przypadku niezaliczonych kontroli.

Z perspektywy testera penetracyjnego raport zgodności Nessus jest cennym źródłem informacji, o ile jest dostępny. Jeśli organizacja docelowa przeprowadziła już wewnętrzne skanowanie zgodności i udostępnia wyniki w ramach analizy szarej lub białej skrzynki, raport w praktyce stanowi gotową listę błędnych konfiguracji. Każde nieudane sprawdzenie to potencjalny wektor eskalacji, który warto zbadać.

## Lynis

**Lynis** to narzędzie do audytu bezpieczeństwa o otwartym kodzie źródłowym, przeznaczone do:Linux, macOS i inne systemy oparte na Uniksie. W przeciwieństwie do Nessusa, Lynis działa lokalnie na kontrolowanym hoście, a nie zdalnie. Sprawdza konfigurację systemu pod kątem zgodności z najlepszymi praktykami w zakresie wzmacniania zabezpieczeń i generuje wynik **indeksu wzmacniania zabezpieczeń** wraz z skategoryzowaną listą ustaleń, ostrzeżeń i sugestii.

Lynis jest przydatny zarówno w kontekście defensywnym, jak i ofensywnym. Administrator systemu uruchamia Lynis w celu identyfikacji luk w zabezpieczeniach na zarządzanych przez siebie serwerach. Pentester, który uzyskał dostęp do powłokiLinuxDocelowy system może uruchomić Lynis, aby szybko wyliczyć słabe punkty konfiguracji bez konieczności ręcznego sprawdzania każdej kategorii. Jednak przesyłanie lub uruchamianie dodatkowych narzędzi na celu podczas interwencji wiąże się z ryzykiem wykrycia i może naruszać zasady zaangażowania. Decyzja o użyciu Lynis na celu powinna być rozważona w kontekście uzgodnionego zakresu i operacyjnych wymagań bezpieczeństwa oceny.

## OpenSCAP

**OpenSCAP** to platforma open source implementująca **protokół Security Content Automation Protocol (SCAP)** , czyli standardową metodę określania i oceny zasad konfiguracji zabezpieczeń. OpenSCAP ocenia hosta na podstawie profili sformatowanych przez SCAP, w tym: WNPISTIG treść i generuje szczegółowe raporty z wynikami zaliczenia/niezaliczenia każdej reguły.

OpenSCAP jest powszechnie wdrażany w środowiskach rządowych i korporacyjnych, gdzie automatyczna walidacja zgodności jest wymogiem prawnym. Dane wyjściowe są ustrukturyzowane i czytelne maszynowo, co czyni je odpowiednimi do integracji z szerszymi procesami zarządzania zgodnością.

## WNP-KOT

**WNP-CAT** to własne narzędzie oceny Centrum Bezpieczeństwa Internetu, stworzone specjalnie do oceny hostówWNPTesty porównawcze. Jest dostępny zarówno w bezpłatnej, limitowanej wersji (WNP-CAT Lite) i pełną wersję komercyjną (WNP-CAT Pro).WNP-CAT generuje szczegółowe raporty dotyczące zaliczenia/niezaliczenia testu, które są bezpośrednio powiązane z zaleceniami dotyczącymi testów porównawczych, co czyni go najbardziej przejrzystym narzędziem doWNPZgodność z normami.

## Narzędzia do enumeracji ofensywnej

Opisane powyżej narzędzia są przeznaczone głównie do defensywnego audytu zgodności. Istnieje osobna kategoria narzędzi do ofensywnego wyliczania eskalacji uprawnień. Narzędzia takie jak **LinPEAS** , **WinPEAS** i **PowerUp** są zaprojektowane do działania na zainfekowanym hoście i identyfikowania słabych punktów konfiguracji z perspektywy atakującego. Sprawdzają one wiele tych samych problemów, które sygnalizują narzędzia do zgodności, takich jak możliwość zapisu plików, słabe uprawnienia usług i przechowywane dane uwierzytelniające, ale ich wyniki są dostosowane do wykorzystania luk, a nie do ich naprawy.

Nakładanie się tych dwóch kategorii jest znaczące. WNPKontrola porównawcza, która weryfikuje SSH logowanie roota jest wyłączone, jest funkcjonalnie powiązane z kontrolą LinPEAS, która podświetla SSH Konfiguracja. Różnica polega na docelowej grupie odbiorców i działaniu podjętym w związku z ustaleniem. Narzędzia zgodności i narzędzia ofensywne omówione w kolejnych salach tego modułu to dwie strony tej samej monety.

Odpowiedz na poniższe pytania

Który komercyjny skaner podatności opracowany przez Tenable obejmuje funkcjonalność audytu zgodności ze standardami CIS?

Błędy w konfiguracji hosta prowadzące do eskalacji uprawnień można przyporządkować do zestawu ściśle zdefiniowanych kategorii. Zrozumienie tych kategorii zapewnia ramy mentalne do podejścia do każdego systemu, niezależnie od jego systemu operacyjnego lub roli. Każda kategoria reprezentuje rodzaj odchylenia od bezpiecznej konfiguracji bazowej, które atakujący może wykorzystać.

To zadanie opisuje każdą kategorię na poziomie koncepcyjnym. Konkretne techniki identyfikacji i wykorzystania tych błędnych konfiguracjiLinuxi Windows zostaną omówione w dedykowanych pomieszczeniach w dalszej części tego modułu.

![Diagram przedstawiający sześć kategorii błędnej konfiguracji hosta, które prowadzą do eskalacji uprawnień, zgrupowanych w kontenerze z liniami przerywanymi. Te sześć kategorii to: Użytkownicy i grupy, Uprawnienia do plików, Usługi, Zadania zaplanowane, Magazyn danych uwierzytelniających i Konfiguracja sieci. Pojedyncza strzałka wchodzi do kontenera z nagłówka „Kategorie błędnej konfiguracji hosta”, a pojedyncza strzałka wychodzi do pola wyników z napisem „Odchylenia od bezpiecznej linii bazowej równają się wektorom eskalacji uprawnień”.](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1774229222684.svg)

## Konfiguracja użytkowników i grup

Systemy operacyjne używają kont i grup do kontrolowania, kto może wykonywać poszczególne czynności. Bezpieczna linia bazowa definiuje zasadę minimalnych uprawnień, zgodnie z którą każde konto ma tylko uprawnienia niezbędne do wykonywania swojej funkcji. Odstępstwa od tej zasady stwarzają ryzyko eskalacji.

Typowe błędy w konfiguracji w tej kategorii obejmują niepotrzebne przypisywanie kont użytkowników do grup administracyjnych, tworzenie kont usług z nadmiernymi uprawnieniami, pomijanie dezaktywacji lub usuwania domyślnych kont dostarczanych z systemem operacyjnym oraz konfigurowanie słabych lub nieistniejących zasad dotyczących haseł, które umożliwiają łatwe odgadnięcie danych uwierzytelniających. Na przykład atakujący, który włamie się na konto użytkownika należące do grupy administracyjnej, może już mieć podwyższone uprawnienia bez konieczności dalszej eksploatacji.

## Uprawnienia plików i katalogów

Uprawnienia do plików i katalogów kontrolują, którzy użytkownicy mogą odczytywać, zapisywać lub wykonywać określone pliki.LinuxSystemy Windows i Windows wdrażają w tym celu mechanizmy kontroli dostępu, choć modele różnią się specyfiką. Bezpieczna linia bazowa definiuje ścisłe uprawnienia do wrażliwych plików, plików binarnych systemu i katalogów konfiguracyjnych.

NA Linux Błędy w konfiguracji w tej kategorii obejmują ustawienie bitu **SUID** (Set User ID) w plikach binarnych, które go nie wymagają. Bit SUID to specjalne uprawnienie, które powoduje, że plik wykonywalny jest uruchamiany z uprawnieniami właściciela pliku, a nie użytkownika, który go uruchamia. Gdy plik binarny z SUID jest własnością użytkownika root i zawiera funkcjonalność umożliwiającą wykonywanie dowolnych poleceń lub dostęp do plików, staje się on bezpośrednim wektorem eskalacji uprawnień. Inne typowe problemy obejmują skrypty lub pliki binarne z możliwością zapisu przez wszystkich użytkowników, wykonywane przez procesy uprzywilejowane, oraz pliki wrażliwe, takie jak `/etc/shadow`klucze prywatne SSH, z uprawnieniami do odczytu o zbyt szerokim zakresie.

W systemie Windows analogiczne problemy dotyczą **list kontroli dostępu (ACL),** które przyznają nadmierne uprawnienia. Do tej kategorii zaliczają się katalogi w systemie `PATH`, do których dostęp mają użytkownicy bez uprawnień, katalogi instalacyjne programów ze słabymi domyślnymi uprawnieniami oraz nieprawidłowo skonfigurowane listy kontroli dostępu kluczy rejestru.

## Konfiguracje usług

Usługi to długotrwałe procesy, które wykonują zadania w tle w systemie. W systemie Linux usługi są zazwyczaj zarządzane przez **systemd** i definiowane w plikach jednostek. W systemie Windows usługi są zarządzane przez **Menedżera kontroli usług (SCM)** i konfigurowane za pomocą rejestru i właściwości usług.

Bezpieczna wersja bazowa wymaga, aby usługi działały z minimalnymi wymaganymi uprawnieniami, były skonfigurowane z restrykcyjnymi kontrolami dostępu zapobiegającymi nieautoryzowanym modyfikacjom i odwoływały się do swoich plików wykonywalnych, używając pełnych, jednoznacznych ścieżek.

Do typowych błędnych konfiguracji należą usługi uruchamiane jako root lub `LocalSystem`gdy nie jest to konieczne, pliki konfiguracyjne usług lub pliki binarne, do których mogą zapisywać użytkownicy bez uprawnień, oraz ścieżki binarne usług, które nie są ujęte w cudzysłów i zawierają spacje. W systemie Windows problem **ze ścieżkami usług bez cudzysłowów** jest szczególnie znany. Gdy ścieżka wykonywalna usługi zawiera spacje i nie jest ujęta w cudzysłów, Menedżer sterowania usługami próbuje rozwiązać ścieżkę, testując każdą możliwą granicę tokenu. W przypadku usługi o ścieżce `C:\Program Files\My App\service.exe`, system Windows najpierw spróbuje wykonać `C:\Program.exe`, następnie `C:\Program Files\My.exe`, a następnie `C:\Program Files\My App\service.exe`. Jeśli użytkownik bez uprawnień może zapisywać do dowolnego z katalogów pośrednich, może umieścić złośliwy plik binarny w jednej z testowanych ścieżek, a zostanie on wykonany z uprawnieniami konta usługi.

## Zaplanowane zadania i zadania cron

Zarówno Linux, jak i Windows obsługują planowanie poleceń lub skryptów, które uruchamiają się automatycznie w określonych odstępach czasu. W systemie Linux obsługuje to **cron** , harmonogram zadań, który wykonuje polecenia zgodnie z regułami czasowymi zdefiniowanymi w plikach crontab. W systemie Windows **harmonogram zadań** zapewnia podobną funkcjonalność.

Zaplanowane zadania uruchamiane z podwyższonymi uprawnieniami i odwołujące się do skryptów lub plików binarnych, które użytkownik bez uprawnień może modyfikować, stanowią bezpośredni wektor eskalacji. Bezpieczna linia bazowa wymaga, aby każdy skrypt lub plik binarny wykonywany przez uprzywilejowane zadanie zaplanowane był chroniony odpowiednimi uprawnieniami, a konfiguracja zadania nie mogła być modyfikowana przez nieupoważnionych użytkowników.

Drugim problemem jest zachowanie niektórych narzędzi podczas przetwarzania nazw plików przypominających flagi wiersza poleceń. Zaplanowane zadanie, które używa symbolu wieloznacznego do przetwarzania plików w katalogu, może być podatne na **wstrzyknięcie symbolu wieloznacznego** . Na przykład, jeśli zadanie cron z uprawnieniami użytkownika root zostanie uruchomione `tar cf /backup/archive.tar *`w katalogu, atakujący, który może tworzyć pliki w tym katalogu, może dodawać pliki o nazwach `--checkpoint=1`i `--checkpoint-action=exec=sh shell.sh`. Podczas `tar`przetwarzania symbolu wieloznacznego, interpretuje on te nazwy plików jako argumenty wiersza poleceń i wykonuje skrypt atakującego z uprawnieniami zadania cron.

## Przechowywanie poświadczeń

Administratorzy i użytkownicy często przechowują dane uwierzytelniające w lokalizacjach dostępnych dla innych kont w systemie. Nie jest to błędna konfiguracja uprawnień w tradycyjnym rozumieniu, lecz raczej praktyka operacyjna, która narusza zasadę higieny danych uwierzytelniających.

W systemie Linux typowe miejsca ujawnienia danych uwierzytelniających to pliki historii powłoki, takie jak `~/.bash_history`pliki zmiennych środowiskowych, pliki konfiguracji aplikacji zawierające ciągi połączeń z bazą danych lub klucze API, a także prywatne klucze SSH przechowywane z nadmiernie ograniczonym dostępem do odczytu.

W systemie Windows ujawnienie poświadczeń może obejmować wpisy w **Menedżerze poświadczeń systemu Windows** (dostępnym za pośrednictwem `cmdkey /list`), zapisane poświadczenia używane w `runas /savecred`, hasła w postaci zwykłego tekstu w rejestrze systemu Windows, pliki wdrożeniowe, takie jak `Unattend.xml`pliki konfiguracyjne programu Sysprep, historię poleceń programu PowerShell oraz pliki konfiguracyjne aplikacji internetowych, takie jak `web.config`.

Osoba atakująca, która odkryje zapisane dane uwierzytelniające konta uprzywilejowanego, może od razu eskalować atak, nie wykorzystując żadnych błędów technicznych w samym systemie.

## Konfiguracja sieci

Błędy w konfiguracji sieci są rzadziej kojarzone z eskalacją uprawnień lokalnych niż kategorie wymienione powyżej, ale nadal mają znaczenie dla ogólnego poziomu bezpieczeństwa hosta. Kategoria ta została uwzględniona dla zachowania kompletności i nie stanowi głównego tematu tego modułu.

Bezpieczna linia bazowa definiuje, które porty i usługi powinny być dostępne, z których interfejsów i do których adresów źródłowych. Odstępstwa od tej linii bazowej zwiększają powierzchnię ataku dostępną dla atakującego, który uzyskał już dostęp do sieci. Na przykład usługa bazy danych, taka jak MySQL, powiązana z `0.0.0.0`(wszystkimi interfejsami) zamiast `127.0.0.1`(tylko z hostem lokalnym), jest dostępna z sieci, a nie ograniczona do połączeń lokalnych. Jeśli baza danych ma słabe dane uwierzytelniające lub nie posiada uwierzytelnienia, ta błędna konfiguracja umożliwia dostęp do danych lub, w niektórych przypadkach, wykonywanie poleceń za pośrednictwem funkcji specyficznych dla bazy danych, takich jak MySQL `INTO OUTFILE`lub PostgreSQL `COPY TO PROGRAM`.

Do innych częstych problemów należą: niepotrzebne otwarte porty, nadmierna pobłażliwośćzapora sieciowareguły zezwalające na połączenia przychodzące do interfejsów zarządzania i niezabezpieczone protokoły zarządzania zdalnego, które przesyłają dane uwierzytelniające w postaci zwykłego tekstu.

Podejście do hosta bez określonej metodologii prowadzi do niespójnych wyników. Testerzy, którzy polegają na pamięci lub intuicji, nieuchronnie przeoczą kategorie błędów konfiguracji, szczególnie pod presją czasu. Ustrukturyzowana metodologia enumeracji zapewnia kompleksowe pokrycie poprzez przypisanie każdego kroku do zdefiniowanej kategorii błędów konfiguracji.

Przedstawiona tutaj metodologia jest niezależna od systemu operacyjnego. Definiuje ona, co należy sprawdzić, a nie jak to zrobić. Konkretne polecenia i narzędzia doLinuxi Windows zostaną omówione w dedykowanych pomieszczeniach, o których mowa w tym module.

## Faza 1 – Świadomość sytuacyjna

Zanim sprawdzisz konkretne błędy konfiguracji, musisz zrozumieć kontekst hosta. Ta wstępna faza odpowiada na fundamentalne pytania dotyczące systemu i konta, na którym działasz.

Należy określić tożsamość i uprawnienia bieżącego konta użytkownika, w tym członkostwo w grupach. Należy zidentyfikować system operacyjny, jego wersję i architekturę. Należy określić nazwę hosta i zrozumieć rolę hosta w sieci, niezależnie od tego, czy jest to stacja robocza, serwer WWW, serwer bazy danych, czy kontroler domeny. Należy również sprawdzić, czy host jest przyłączony do domeny, ponieważ ma to wpływ na dostępne ścieżki eskalacji.

Informacje te kształtują następującą enumerację. Serwer Windows przyłączony do domeny, działającyIISprezentuje inne możliwości niż samodzielneLinuxstanowisko pracy. Wiedza o tym, z czym pracujesz, zapobiega marnowaniu wysiłku.

## Faza 2 – Wyliczenie oparte na kategoriach

Po uzyskaniu świadomości sytuacyjnej, enumeracja przechodzi przez każdą kategorię błędnych konfiguracji zidentyfikowaną w poprzednim zadaniu. Kolejność nie jest ściśle ustalona, ​​ale spójna sekwencja gwarantuje, że nic nie zostanie pominięte.

**Konfiguracja użytkowników i grup.** Wypisz wszystkie konta użytkowników w systemie i ich przynależność do grup. Zidentyfikuj konta z dostępem administracyjnym lub root. Sprawdź, które konta domyślne powinny zostać wyłączone. Przejrzyj ustawienia zasad dotyczących haseł, jeśli są dostępne.

**Uprawnienia do plików i katalogów.** Wyszukaj pliki i katalogi z nadmiernie restrykcyjnymi uprawnieniami dostępu. WłączoneLinuxObejmuje to lokalizowanie plików binarnych SUID i SGID, plików i katalogów z możliwością zapisu przez wszystkich użytkowników oraz plików poufnych z szerokimi uprawnieniami odczytu. W systemie Windows obejmuje to przeglądanie list kontroli dostępu (ACL) dla katalogów w zmiennej systemowej PATH, katalogów instalacyjnych programów oraz kluczy rejestru powiązanych z usługami.

**Konfiguracje usług.** Wypisz wszystkie uruchomione usługi i ich konfiguracje. Zidentyfikuj konto użytkownika, na którym działa każda usługa. Sprawdź, czy plik binarny lub konfiguracyjny usługi jest dostępny do zapisu dla bieżącego użytkownika. W systemie Windows sprawdź ścieżki dostępu do usług bez cudzysłowów i przejrzyj deskryptory zabezpieczeń usług.

**Zaplanowane zadania i zadania cron.** Wypisz wszystkie zaplanowane zadania i zidentyfikuj te, które działają z podwyższonymi uprawnieniami. Sprawdź uprawnienia do skryptów lub plików binarnych, do których odwołują się uprzywilejowane zaplanowane zadania. WłączoneLinux, przejrzyj wpisy crontab dla całego systemu i dla konkretnego użytkownika. W systemie Windows przejrzyj zadania w Harmonogramie zadań.

**Przechowywanie poświadczeń.** Wyszukaj poświadczenia przechowywane w dostępnych lokalizacjach. Sprawdź pliki historii powłoki, zmienne środowiskowe, pliki konfiguracyjne, wpisy rejestru, magazyny poświadczeń i pliki wdrożeniowe. Ten krok często prowadzi do najkrótszej drogi do eskalacji.

**Konfiguracja sieci.** Przejrzyj porty nasłuchujące, powiązane interfejsy izapora sieciowaZasady. Zidentyfikuj usługi, które są niepotrzebnie eksponowane lub niedostępne. Ten krok jest bardziej istotny dla ruchu bocznego niż lokalnej eskalacji, ale przyczynia się do ogólnego zrozumienia postawy gospodarza.

![Schemat blokowy przedstawiający trzyetapową metodologię enumeracji. Faza 1, Świadomość sytuacyjna, jest powiązana z Fazą 2, Enumeracją opartą na kategoriach, która zawiera sześć równoległych kontroli w kontenerze z liniami przerywanymi: Użytkownicy i grupy, Uprawnienia do plików, Usługi, Zaplanowane zadania, Magazyn danych uwierzytelniających i Konfiguracja sieci. Kontener jest powiązany z Fazą 3, Priorytetyzacja i eksploatacja, która prowadzi do uzyskania dostępu z podwyższonym poziomem uprawnień.](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1774229240590.svg)

## Faza 3 – Priorytetyzacja i eksploatacja

Enumeracja zazwyczaj prowadzi do wielu ustaleń. Nie wszystkie ustalenia są równie podatne na wykorzystanie lub mają równie duży wpływ. Ustalenia należy priorytetyzować w oparciu o bezpośredniość ścieżki eskalacji, preferując ustalenia zapewniające najpewniejszą drogę do najwyższego poziomu uprawnień.

Na przykład zapisane dane uwierzytelniające konta root lub administratora stanowią bardziej bezpośrednią ścieżkę eskalacji niż plik z możliwością zapisu w zadaniu cron wykonywanym co godzinę. Oba wnioski są prawidłowe, ale pierwszy nie wymaga czekania ani dodatkowych kroków.

Niektóre ustalenia nie nadają się do wykorzystania w izolacji, ale stają się istotne po połączeniu. Na przykład, enumeracja może ujawnić, że zadanie cron użytkownika root jest uruchamiane `/opt/scripts/backup.sh`co pięć minut (wykrycie zaplanowanego zadania) i że skrypt jest dostępny do zapisu dla wszystkich użytkowników (wykrycie uprawnień do pliku). Żadne z tych ustaleń nie jest wystarczające samo w sobie. Zadanie cron nie jest z natury niebezpieczne, a plik z możliwością zapisu dla wszystkich użytkowników, który nigdy nie jest wykonywany przez proces uprzywilejowany, jest problemem o niskim priorytecie. Jednak połączenie tych dwóch elementów zapewnia bezpośrednią ścieżkę eskalacji uprawnień: zmodyfikuj skrypt, poczekaj, aż zadanie cron wykona go jako użytkownik root, i uzyskaj wyższy poziom uprawnień. Rozpoznawanie tych łańcuchów w różnych kategoriach jest podstawową umiejętnością w metodologii eskalacji uprawnień.

## Rola narzędzi automatycznych

Zautomatyzowane narzędzia do enumeracji, takie jak LinPEAS, WinPEAS i PowerUp, są bezpośrednio powiązane z tą metodologią. Wykonują one wiele opisanych powyżej kontroli i wyróżniają ustalenia według ważności. Stanowią one jednak uzupełnienie metodologii, a nie jej zamiennik. Zrozumienie, co i dlaczego sprawdzają narzędzia, pozwala na prawidłową interpretację ich wyników, identyfikację fałszywych alarmów i luk wymagających ręcznego sprawdzenia.

Jeśli wyniki skanowania zgodności z narzędziami takimi jak Nessus lub Lynis są dostępne, czy to poprzez analizę typu white-box, czy poprzez uruchomienie Lynis na zainfekowanym hoście, ich wyniki mogą zostać wykorzystane do ustalenia priorytetów, które kategorie należy zbadać w pierwszej kolejności.WNPNa przykład kontrola uprawnień usługi wskazuje bezpośrednio na kategorię konfiguracji usługi.

Zrozumienie struktury WNP Rekomendacja benchmarkowa to praktyczna umiejętność, przydatna zarówno w ofensywie, jak i defensywie. Każda rekomendacja ma spójny format, który po zapoznaniu się z nim pozwala szybko ocenić, przed czym chroni dana kontrola i jak wygląda odchylenie, które można wykorzystać.

## Struktura rekomendacji

Typowy WNP Rekomendacja benchmarkowa zawiera kilka standardowych pól.

Tytuł **identyfikuje** konkretne ustawienie lub konfigurację podlegającą ocenie. Zazwyczaj jest sformułowany jako stwierdzenie rozkazujące lub deklaratywne. Przykład z WNP Benchmark dla Ubuntu Linux „Upewnij się, że uprawnienia do pliku /etc/shadow są skonfigurowane”.

**Stosowalność profilu** wskazuje , czy zalecenie należy do profilu Poziomu 1, czy Poziomu 2. Jak opisano w Zadaniu 3, zalecenia Poziomu 1 mają szerokie zastosowanie przy minimalnym ryzyku zakłócenia funkcjonalności, natomiast zalecenia Poziomu 2 zapewniają dodatkowe wzmocnienie kosztem potencjalnego wpływu na działanie.

Opis wyjaśnia w prostych słowach **,** czego wymaga zalecenie. W `/etc/shadow`przykładzie podano, że właścicielem pliku powinien być użytkownik root, z grupą ustawioną na `shadow`, a uprawnieniami tak, aby tylko użytkownik root miał dostęp do odczytu i zapisu, podczas gdy grupa shadow ma dostęp do odczytu.

Uzasadnienie wyjaśnia zagrożenie bezpieczeństwa, którego dotyczy zalecenie. W tym przypadku, w uzasadnieniu wyjaśniono, że plik **zawiera**`/etc/shadow` zaszyfrowane hasła dla wszystkich lokalnych kont użytkowników i że jeśli użytkownicy bez uprawnień będą mogli odczytać ten plik, będą mogli wyodrębnić zaszyfrowane hasła i podjąć próbę złamania go offline w celu odzyskania haseł w postaci zwykłego tekstu.

Sekcja **audytu** zawiera konkretne polecenia lub procedury weryfikujące, czy host spełnia zalecenia. W tym `/etc/shadow`przykładzie procedura audytu określa uruchomienie `stat /etc/shadow`i sprawdzenie, czy dane wyjściowe zawierają oczekiwane wartości własności i uprawnień.

Sekcja **naprawcza** zawiera polecenia lub kroki, które należy wykonać, aby przywrócić zgodność niezgodnego hosta. W tym przykładzie określono by polecenia `chown`i `chmod`polecenia korygujące własność i uprawnienia.

## Czytanie z perspektywy ofensywnej

Tester penetracyjny czyta tę samą rekomendację, mając na myśli inne pytanie. Zamiast pytać „czy ten system jest zgodny?”, pyta: „jeśli ten system nie jest zgodny, co mogę zrobić z tym odkryciem?”.

W tym `/etc/shadow`przykładzie, ofensywny odczyt jest prosty. Jeśli kontrola audytu zakończy się niepowodzeniem i `/etc/shadow`bieżący użytkownik będzie mógł odczytać plik, można skopiować go, wyodrębnić skróty haseł i przeprowadzić atak łamania offline za pomocą narzędzia takiego jak John the Ripper lub Hashcat. Pomyślne złamanie skrótu użytkownika root lub administratora zapewnia bezpośrednią eskalację uprawnień.

Nie każda nieudana kontrola porównawcza prowadzi do bezpośredniej ścieżki eskalacji. Niektóre ustalenia stanowią udoskonalenia w zakresie obrony dogłębnej, które w izolacji nie nadają się do wykorzystania. Umiejętność polega na rozpoznaniu, które odchylenia są bezpośrednio podatne na działania, które w połączeniu z innymi ustaleniami przyczyniają się do łańcucha wykorzystania, a które stanowią kwestie informacyjne o niskim priorytecie.

## Mapowanie na zautomatyzowane dane wyjściowe narzędzia

Kontrole przeprowadzane przez zautomatyzowane narzędzia zgodności odpowiadają bezpośrednio indywidualnym zaleceniom testów porównawczych. Skanowanie zgodności z flagą „7.1.5 – Upewnij się, że uprawnienia do pliku /etc/shadow są skonfigurowane – NIEPOWODZENIE” raportuje wynik tej samej procedury audytu, która została opisana w teście porównawczym CIS Ubuntu Linux 24.04 LTS. Podobnie, skanowanie LinPEAS, które oznacza plik `/etc/shadow`jako czytelny dla bieżącego użytkownika, wykrywa ten sam problem z perspektywy ataku.

Zrozumienie rekomendacji dotyczących wyników testów porównawczych, na podstawie których narzędzie wykryło błąd, pozwala na ocenę jego wagi i podatności na wykorzystanie z większą pewnością niż w przypadku polegania wyłącznie na wynikach narzędzia.

## Ćwiczenie praktyczne

Dołączona statyczna witryna do tego zadania zawiera dane wyjścioweWNPAudyt porównawczy przeprowadzony na trzech hostach:

- DwaLinuxserwery ( `linux-web-01`w `10.10.45.12`i `linux-db-02`w `10.10.45.20`, oba oceniane na podstawie CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0)
- Jeden serwer Windows ( `win-dc-01`w `10.10.45.50`, oceniany w porównaniu zWNPTest porównawczy systemu Microsoft Windows Server 2022 w wersji 3.0.0)

Jeden zLinuxserwery przechodzą wszystkie kontrole. PozostałeLinuxSerwer i serwer Windows mają wiele nieudanych kontroli.

Kliknij nazwy hostów, aby przełączać się między maszynami. Rozwiń każde zalecenie, aby sprawdzić jego opis, uzasadnienie, polecenie audytu, oczekiwane i rzeczywiste dane wyjściowe oraz kroki naprawcze. Użyj wyników, aby odpowiedzieć na poniższe pytania.

Odpowiedz na poniższe pytania

Jaka jest faktyczna wartość uprawnień zaobserwowana w /etc/shadow w systemie linux-web-01 przy nieudanej kontroli 7.1.5?

Sprawdzać

Ile plików z możliwością zapisu przez wszystkich użytkowników zostało wykrytych w systemie linux-web-01 przez sprawdzenie 7.1.11?

Sprawdzać

Jaka jest pełna ścieżka do nieoczekiwanego pliku binarnego SUID znalezionego podczas sprawdzania 7.1.13 w systemie linux-web-01?

Sprawdzać

Jaka jest minimalna długość hasła skonfigurowana obecnie w systemie win-dc-01, zgodnie z kontrolą 1.1.4?

Sprawdzać

Jaka jest aktualna wartość klucza rejestru FilterAdministratorToken w systemie win-dc-01, zgłoszona przez sprawdzenie 2.3.17.1?

Sprawdzać

Ile w sumie sprawdzeń przechodzi linux-db-02?

W tej sali omówiliśmy podstawowe koncepcje związane z przeglądami konfiguracji hostów i serwerów. Teraz rozumiesz różnicę między eskalacją uprawnień opartą na podatnościach a eskalacją opartą na konfiguracji oraz dlaczego błędne konfiguracje pozostają jednymi z najczęstszych i najpewniejszych wektorów eskalacji spotykanych podczas testów penetracyjnych.

Zapoznałeś się z ramami branżowymi, które definiują, jak powinna wyglądać bezpieczna konfiguracja bazowa.WNPBenchmarki i DISA STIG zapewniają kompleksowe, audytowalne standardy, według których można porównywać dowolnego hosta. Zautomatyzowane narzędzia do zapewniania zgodności, takie jak Nessus, Lynis, OpenSCAP iWNP-CAT ułatwia ocenę hostów pod kątem tych standardów na dużą skalę, a jego wyniki służą zarówno do obronnej naprawy, jak i ofensywnej enumeracji.

Sześć kategorii błędów konfiguracji omówionych w tej sali, a konkretnie konfiguracja użytkowników i grup, uprawnienia do plików i katalogów, konfiguracje usług, zadania zaplanowane i zadania cron, przechowywanie danych uwierzytelniających oraz konfiguracja sieci, stanowią podstawę ustrukturyzowanej metodologii enumeracji, którą zaprezentujesz w kolejnych salach. Każda kategoria odpowiada konkretnym kontrolom w omawianych ramach i narzędziach, a każda reprezentuje klasę ustaleń, które pojawiają się wielokrotnie w rzeczywistych sytuacjach.
