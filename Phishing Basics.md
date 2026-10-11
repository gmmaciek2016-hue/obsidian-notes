---

Wyobraź sobie: Zostałeś poproszony o złamanie zabezpieczeń firmy podczas testów penetracyjnych. Ich zapory sieciowe są niezawodne, a systemy wykrywania włamań nie do przebicia. Ale istnieje jedna luka, której żadna technologia nie jest w stanie w pełni zabezpieczyć: czynnik ludzki.

Phishingto jedno z najpotężniejszych narzędzi w arsenale testera penetracyjnego. Dlaczego? Ponieważ nawet najbezpieczniejsze organizacje polegają na ludziach, można ich oszukać, zmanipulować i nakłonić do udzielenia dostępu.Phishingto często najłatwiejszy sposób na uzyskanie dostępu podczas ataku. Jeden dobrze napisany e-mail może ominąć kontrolę techniczną, podłożyć złośliwe oprogramowanie lub ukraść dane uwierzytelniające, które otworzą Ci dostęp do sieci docelowej.

## Cele edukacyjne

- Cophishingjest i jego rola w teście penetracyjnym 
- Psychologia stojąca zaphishing
- Wspólnyphishingataki
- Anatomiaphishingkampania
- Phishingnarzędzia

## Co to jest Phishing?

Phishing jest formą cyberataku, która wykorzystuje inżynieria społeczną by nakłonić ludzi do ujawnienia poufnych informacji lub uruchomienia złośliwego oprogramowania na ich urządzeniach. Atakujący oszukują ofiary, podszywając się pod legalne źródła za pośrednictwem wiadomości e-mail, SMS-ów, połączeń telefonicznych lub fałszywych stron internetowych. Phishing Wykorzystuje psychologię człowieka, a nie luki techniczne. Atakujący tworzą wiarygodne narracje i stosują taktyki nacisku, aby manipulować ofiarami i narażać je na szwank. Główne kanały phishing Ataki obejmują pocztę elektroniczną, SMS-y (znane jako **smishing** ), połączenia głosowe ( **vishing** ) i fałszywe strony internetowe, które mają sprawiać wrażenie legalnych.phishingCelem ataku jest uzyskanie korzyści finansowych, uzyskanie nieautoryzowanego dostępu do poufnych danych lub zainstalowanie złośliwego oprogramowania na urządzeniu ofiary.

## RodzajePhishing

![Diagram porównujący trzy typy ataków phishingowych: phishing (haczyk wymierzony w wiele różnych ryb, reprezentujący ataki masowe na szeroką skalę), spear phishing (precyzyjna broń wymierzona w konkretną kałamarnicę, reprezentująca ataki ukierunkowane na pojedyncze osoby) i whaling (duży wieloryb, reprezentujący ataki na wysoko postawionych dyrektorów lub kadrę zarządzającą).|697](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1775551569683.png)

**Phishing**

Phishingto szeroko zakrojona wersja oszustwa, polegająca na „rozrzucaniu szerokiej sieci”. Atakujący wysyłają tę samą wiarygodną wiadomość do wielu osób jednocześnie, często wykorzystując typowe motywy, takie jak alerty dotyczące kont czy faktury. Wiadomości te wydają się raczej rutynowe niż osobiste; wszelkie szczegóły są ogólnikowe lub lekko nie na miejscu. Celem jest szybkie osiągnięcie sukcesu na dużą skalę: kradzież haseł, danych kart lub uzyskanie dostępu do urządzenia.

**WłóczniaPhishing**

Włóczniaphishingto atak ukierunkowany na konkretną osobę. Celem jest zazwyczaj nakłonienie ofiary do kliknięcia linku, otwarcia pliku, uruchomienia zadania lub przesłania danych uwierzytelniających, aby atakujący mógł wniknąć głębiej w sieć organizacji.

**Wielorybnictwo**

Polowanie na wieloryby to włóczniaphishingskierowane do decydentów wyższego szczebla i kadry kierowniczej, takich jak prezesi i dyrektorzy finansowi. Oba atakująphishingi wielorybnictwo to ataki celowe i dostosowane do indywidualnych potrzeb; różnica polega na tym, kto jest celem ataku i jakiej siły nacisku się oczekuje.phishingMoże uderzyć w każdego, kto ma dostęp do przyczółka (dział IT, finanse, HR, zespoły projektowe). Ataki wielorybów koncentrują się na osobach, których uprawnienia decyzyjne pozwalają na przepływ pieniędzy, ujawnianie danych objętych regulacjami lub obejście kontroli.

W testach penetracyjnychphishingjest niezbędny przy ocenie podatności organizacji nainżynieria społecznaAtaki. Symulując te ataki, pentesterzy mogą odkryć ludzkie słabości w organizacji. Ocena ryzyka związanego z sukcesemphishingataki, takie jak naruszenia bezpieczeństwa danych czy infekcje złośliwym oprogramowaniem, pomagają organizacjom ocenić stopień narażenia na zagrożenia i przygotować obronę przed realnymi zagrożeniami.

Etyczni hakerzy projektują fałszywe wiadomości e-mail, które bardzo przypominają prawdziwe zagrożeniaphishingTesty penetracyjne bez powodowania szkód. Mogą być one skierowane do określonych grup w zależności od ich roli w organizacji. Narzędzia śledzą wskaźniki odpowiedzi, takie jak współczynniki otwarć i klikalności, dostarczając cennych informacji na temat zachowań pracowników. phishingw testy penetracyjne ujawniają podatność organizacji na inżynieria społecznai z czasem wzmacnia swoją pozycję w zakresie cyberbezpieczeństwa.

Kampanie Phishingowe wykorzystują inżynieria społeczna Techniki manipulowania emocjami i wpływania na proces decyzyjny. Taktyki te często wykorzystują słabości ludzkiej psychiki, aby zwiększyć prawdopodobieństwo sukcesu.

## Inżynieria społeczna Zasady

## ![Diagram pajęczynowy ilustrujący sześć zasad inżynierii społecznej rozchodzących się od centralnej etykiety: Strach (emoji smutnej buźki), Autorytet (korona), Niedobór (odmowa ręki), Pilność (zegar ze znakiem ostrzegawczym), Ciekawość (lupa ze znakiem zapytania) i Zaufanie (tarcza ze znacznikiem wyboru). Każda zasada jest skierowana na zewnątrz od środka za pomocą dwukierunkowych strzałek.|697](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1775468868416.png)

**Niedostatek**

Niedobór sprawia, że ​​coś wydaje się rzadkie, co skłania ludzi do działania, zanim pomyślą. Psychologicznie rzecz biorąc,  pojawia się **FOMO (strach przed pominięciem)** i awersja do straty: bardziej nie lubimy tracić szansy niż zyskiwać. Możemy używać takich określeń jak „ograniczona liczba miejsc”, „ostatnia szansa” lub „kończy się dzisiaj”.

Przykład: „Do wzięcia są tylko trzy TryPhone’y”.

**Pilność**

Pilność dodaje odliczanie, więc mózg priorytetyzuje szybkość nad kontrolą. Presja czasu zawęża uwagę i ogranicza celowe sprawdzanie, zwłaszcza gdy konsekwencje wydają się niewygodne (blokady, opóźnienia). Język często zawiera sformułowania „w ciągu 24 godzin”, „natychmiast” lub „termin minął”.

Przykład: „Twoje konto zostanie zawieszone za 12 godzin, jeśli nie zweryfikujesz swojej tożsamości za pośrednictwem tego portalu”.

**Władza**

Autorytet opiera się na postrzeganym statusie lub wiedzy eksperckiej, aby szybko uzyskać posłuszeństwo. Ludzie chętniej stosują się do poleceń, jeśli uważają, że pochodzą od liderów, ekspertów lub oficjalnych działów. Sygnały wizualne (tytuły, podpisy, formalny ton) i oznaczenia stanowisk (HR, IT, finanse) wzmacniają ten efekt.

Przykład: „Od: Administratora IT. Wymagane działanie na TwoimSSOustawienia.”

**Strach**

Strach wykorzystuje groźbę i alarm, aby wywołać reakcję obronną, nakłaniając ludzi do natychmiastowego „naprawienia” problemu. Lęk może przeważyć nad zwykłym sceptycyzmem, zwłaszcza gdy ryzyko wydaje się osobiste (włamanie na konto, problemy prawne). Sformułowania często obejmują „alert bezpieczeństwa”, „naruszenie” lub „nieautoryzowany dostęp”.

Przykład: „Wykryliśmy podejrzane logowania na Twoim koncie. Natychmiast je zabezpiecz tutaj”.

**Ciekawość**

Ciekawość przyciąga uwagę, obiecując interesujące informacje. Mózg chce wypełnić luki informacyjne, co może przeważyć nad ostrożnością, gdy podpowiedź wydaje się istotna lub ekskluzywna. Tematy wiadomości są krótkie, intrygujące i nieco niejasne.

Przykład: „Poufne: Najważniejsze informacje z planu działania na III kwartał”.

**Zaufanie**

Zaufaj znanym markom, współpracownikom lub stylom komunikacji, aby przekaz automatycznie wydawał się bezpieczny. Rozpoznawalne nazwy, logo lub procedury (raporty miesięczne, numery zgłoszeń) zmniejszają sceptycyzm i sprawiają, że prośby wydają się rutynowe.

Przykład: „Microsoft 365: W Twoim portalu dostępna jest nowa informacja o zabezpieczeniach” lub wiadomość, która wygląda, jakby pochodziła od znanego członka zespołu i prosiła o szybki przegląd.

## Błędy poznawcze

Błąd poznawczy to tendencja do podejmowania decyzji w oparciu o uczucia, założenia lub doświadczenia z przeszłości, a nie fakty. Te błędy zwiększają ryzyko wpadnięcia w pułapkę.phishingoszustwa.

- **Błąd nadmiernej pewności siebie:** Wiele osób, zwłaszcza specjalistów od cyberbezpieczeństwa, uważa, że ​​są zbyt inteligentne, by dać się nabraćphishingoszustw. Jednak ta nadmierna pewność siebie może prowadzić do mniejszej czujności podczas sprawdzania podejrzanych wiadomości.
    
- **Błąd potwierdzenia:** Dzieje się tak, gdy ludzie akceptują informacje, które odpowiadają ich oczekiwaniom. Na przykład, jeśli ktoś czeka na e-mail ze swojego banku, może zaufać…phishinge-mail podszywający się pod wiadomość z banku, bez weryfikacji.
    
- **Błąd autorytetu:** Sprawia, że ​​ludzie bezkrytycznie ufają wiadomościom od osób, które uważają za autorytety. E-mail pochodzący od wysoko postawionego urzędnika ma większe szanse na zaufanie niż ten z nieznanego źródła.

Zrozumienie tych zasad psychologicznych jest niezbędne dla testerów penetracyjnych symulującychphishingkampanie. Włączając taktyki takie jak pilność i autorytet wphishinge-maile lub fałszywe strony docelowe – testerzy penetracyjni mogą sprawdzić, jak dobrze organizacje bronią się przed tymi zagrożeniamiinżynieria społecznaataki.

Teraz, gdy wiemy, który inżynieria społeczna techniki, których możemy użyć, aby oszukać nasze cele, zbadamy stronę techniczną phishing ataki, skupiając się na technikach manipulacji i mechanizmach dostarczania, które sprawiają, że kampanie te odnoszą sukces. Phishing Kampanie wykorzystują manipulację techniczną, aby oszukać cele i ominąć zabezpieczenia. Oto kilka najczęstszych technik stosowanych przez atakujących, aby nakłonić ofiary do interakcji ze złośliwymi treściami.

## Manipulacja adresami URL i domenami

Jako pentesterzy, jednym z naszych głównych celów jest skłonienie naszych odbiorców do kliknięcia kontrolowanego przez nas adresu URL. Aby to osiągnąć, możemy zastosować poniższe techniki:

- **Maskowanie adresów URL:** Polega na ukryciu złośliwego adresu URL za legalnie wyglądającym hiperłączem. Na przykład, atakujący może wyświetlić go  `https://tryhackme.com`podczas przekierowywania użytkowników do domeny `http://phisher.thm`. 
- **Ataki homograficzne:** Wykorzystują wizualne podobieństwa między znakami nazw domen, na przykład zastępując  **„o”** „ **0”** lub używając znaków cyrylicy. Atakujący może zarejestrować domenę, `go0gle.com`która wygląda identycznie jak legalna, ale przekierowuje użytkowników na szkodliwą stronę.
- **Typosquatting:** Polega na rejestrowaniu domen podobnych do legalnych, polegając na przykład na tym, że użytkownicy popełniają błędy literowe  `tryhacme.com`zamiast wprowadzać je ręcznie `tryhackme.com.`. Jako pentester możesz wykorzystywać te domeny do ataków phishingowych lub dystrybucji złośliwego oprogramowania.

Atakujący mogą używać skracaczy adresów URL, aby ukryć prawdziwy adres docelowy linku. Takie adresy URL są trudniejsze do sprawdzenia przez użytkowników i mogą ominąć podstawowe kontrole bezpieczeństwa.

## Podstawy podszywania się pod e-mail

Spoofing e-maili to technika podszywania się pod legalnego nadawcę poprzez modyfikację nagłówków wiadomości e-mail. Na przykład, możemy podrobić pole „Od”, aby wyświetlić adres e-mail zaufanego nadawcy, na przykład menedżera lub pracownika działu kadr. Jeśli domena nie posiada zabezpieczeń uwierzytelniania, atakujący może użyć skryptu Pythona do zmodyfikowania swojego adresu e-mail. Jest to możliwe, ponieważ **protokół SMTP (Simple Mail Transfer Protocol)** nie posiada wbudowanej funkcji uwierzytelniania adresów e-mail.

Podszywanie się pod wyświetlaną nazwę (display name spoofing) polega na zmianie nazwy nadawcy w kliencie pocztowym, przy jednoczesnym ukryciu faktycznego adresu e-mail. Na przykład, używając adresu Gmail, moglibyśmy wyświetlić „Pomoc techniczna” jako nazwę nadawcy. Wiele mobilnych klientów poczty e-mail domyślnie wyświetla tylko nazwę wyświetlaną, ukrywając faktyczny adres e-mail, co czyni tę technikę bardzo skuteczną.

Inne techniki polegają na stosowaniu domen podobnych do legalnych, na przykład `support@tryhackme-secure.com`zamiast `support@tryhackme.com`, aby oszukać odbiorców i wzbudzić u nich zaufanie do wiadomości e-mail.

Stosując niektóre z tych technik, możemy stworzyć wiadomość e-mail, która po stronie odbiorcy będzie wyglądała następująco:

```html
From: Support <support@tryaccounting.thm> 
To: bob@tryaccounting.thm
Subject: Urgent: Account Verification Required

Dear Bob,

As part of our security policy, we require all TryAccounting employees to change their passwords every 3 months. Please log in to our internal portal and update your password before Friday:
http://tryaccounting-security.thm/account

Thank you,
TryAccounting Support Team
```

Na pierwszy rzut oka wygląda to na całkowicie legalny e-mail. Większość klientów poczty e-mail domyślnie nie wyświetla tych szczegółów, ale gdybyśmy przyjrzeli się nagłówkom wiadomości, zobaczylibyśmy prawdziwy adres nadawcy:

```html
From: Support <support@tryaccounting.thm>
Reply-To: attacker@phisher.thm
Return-Path: attacker@phisher.thm
X-Sender: attacker@phisher.thm
Received: from phisher.thm (mail.phisher.thm [192.168.1.25]) by mail.tryaccounting.thm
```

Wiele organizacji stosuje środki bezpieczeństwa, takie jak:**SPF**(Struktura polityki nadawcy),**DMARC**(Uwierzytelnianie wiadomości oparte na domenie, raportowanie i zgodność) oraz**DKIM**(DomainKeys Identified Mail), aby pomóc zapobiegać takim atakom. Chociaż ominięcie tych zabezpieczeń wykracza poza zakres tego forum, zrozumienie podstaw jest kluczowe dla zbudowania solidnego fundamentu.

## Zbieranie poświadczeń

W ataku klonowania logowania atakujący replikuje wszystkie elementy wizualne legalnej witryny, w tym logo, czcionki i pola formularzy, i hostuje je w fałszywej domenie. Podstawowa różnica polega na miejscu docelowym przesłanych danych uwierzytelniających. Na autentycznej stronie dane uwierzytelniające są przesyłane do serwera uwierzytelniającego organizacji. Na sklonowanej stronie dane uwierzytelniające są przesyłane do skryptu kontrolowanego przez atakującego, który rejestruje je w pliku lub bazie danych. Następnie ofiara jest przekierowywana na legalną witrynę, minimalizując podejrzenia. W rezultacie ofiara widzi jedynie nieudaną próbę logowania, podczas gdy atakujący zdobywa hasło ofiary.

## Mechanizmy dostarczania ładunku

Często stosowaną metodą dostarczania wiadomości jest dokument Microsoft Word zawierający makro. Po otwarciu pliku ofiara napotyka monit „Włącz zawartość”, aby wyświetlić dokument, który jest wbudowanym elementem.inżynieria społecznaTaktyka. Po włączeniu makro VBA wykonuje się w tle, niezauważalnie. Podczas rzeczywistego ataku makro to może pobrać i uruchomić złośliwe oprogramowanie. Jednak podczas testu penetracyjnego jest ono zazwyczaj zastępowane łagodnym sygnałem, który jedynie potwierdza wykonanie, nie powodując żadnych szkód.

Typowa sekwencja zdarzeń wygląda następująco:

1. Ofiara otrzymuje i otwiera załącznik .docm.
2. Program Microsoft Word wyświetla użytkownikowi monit o włączenie makr.
3. Ofiara klika „Włącz treść”.
4. Makro VBA wykonuje ukryte polecenie.
5. Atakujący otrzymuje potwierdzenie wykonania polecenia.

## Narzędzia handlu

Pentesterzy korzystają ze specjalnych narzędzi do tworzenia i zarządzania realistycznymiphishingkampanie. Poniżej przedstawiamy trzy najpopularniejsze narzędzia:

[GoPhish(otwiera się w nowej karcie)](https://github.com/gophish/gophish)jest opartym na sieci frameworkiem, który ułatwia konfiguracjęphishingkampanie są prostsze. Pozwala to na przechowywanieSMTPUstawienia serwera do wysyłania wiadomości e-mail oraz narzędzie internetowe do tworzenia szablonów wiadomości e-mail za pomocą prostego edytora WYSIWYG (What You See Is What You Get). Możesz również planować wysyłanie wiadomości e-mail i korzystać z pulpitu analitycznego, który pokazuje wskaźniki otwarć i kliknięć. Możesz zdobyć praktyczne doświadczenie z GoPhish w naszym[Phishing](https://tryhackme.com/room/phishingyl)pokój.

[ZłyNginx(otwiera się w nowej karcie)](https://github.com/kgretzky/evilginx2)jest narzędziem przeznaczonym dla zaawansowanychphishingkampanie, które omijają uwierzytelnianie wieloskładnikowe (MFA). Działa jako odwrotnośćpełnomocnikmiędzy ofiarami i legalnymi witrynami, przechwytując dane uwierzytelniające i tokeny sesji w czasie rzeczywistym.

[TenInżynieria społecznaZestaw narzędzi (SET)(otwiera się w nowej karcie)](https://github.com/trustedsec/social-engineer-toolkit)zawiera wiele narzędzi. Mimo to, niektóre z najważniejszych dlaphishingsą zdolnością do tworzenia włóczni-phishingataki i wdrażanie fałszywych wersji popularnych stron internetowych, aby nakłonić ofiary do podania swoich danych uwierzytelniających. W zadaniu 6 zdobędziemy praktyczne doświadczenie z tym narzędziem.

Kampanie nie polegają jedynie na wysyłaniu losowych e-maili z nadzieją, że ktoś kliknie w złośliwy link. Wymagają one szeroko zakrojonego planowania, rozpoznania, realizacji i analizy po ataku, aby odnieść sukces.phishingĆwiczenie ma znaczenie tylko wtedy, gdy kończy się raportem, na podstawie którego decydenci mogą podjąć działania. To zadanie da ci przeglądphishingcykl życia kampanii i pokażemy, jak planują ją pentesterzy.

![Okrągła infografika zatytułowana „Anatomia kampanii phishingowej” przedstawiająca 5 etapów: 1) Planowanie i zakres – Zdefiniowanie celów, 2) Rozpoznanie – Gromadzenie informacji, 3) Opracowanie scenariusza i ładunku – Przygotowanie ataku phishingowego, 4) Eksploatacja i działania poeksploatacyjne – Przeprowadzenie kampanii i wyodrębnienie danych, 5) Raportowanie i podsumowanie – Prezentacja ustaleń. Strzałki pokazują cykl od etapu 1 do 5 i zapętlenie.](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1775468992972.png)

## Planowanie i określanie zakresu

Zacznij od uzgodnienia misji z klientem i spisania jej w jednym zdaniu. Określ, które grupy użytkowników są włączone, a które nie, jakie techniki są dozwolone oraz jakie konkretne rezultaty należy mierzyć, na przykład oddzielenie „kliknięcia w link” od „próby przesłania danych uwierzytelniających”. Ustal harmonogram kampanii i liczbę wiadomości, uzyskaj zgodę prawną i zapisz zasady zaangażowania, wyraźny wyłącznik awaryjny i kontakty alarmowe, aby ćwiczenie pozostało autoryzowane, bezpieczne i odwracalne.

## Rekonesans

Używaj wyłącznie informacji publicznych, aby przynęty wydawały się wiarygodne, nie przekraczając granic prywatności. Strony internetowe firm, komunikaty prasowe, profile LinkedIn, publiczne wpisy w mediach społecznościowych i istotne wiadomości zapewniają wystarczający kontekst, aby stworzyć wiarygodne preteksty, takie jak odniesienia do niedawnego ogłoszenia lub zmiany polityki. Utrzymuj wszystkie zbiory w ramach zakresu i dokumentuj źródła, aby było jasne, że badania były etyczne i ograniczone do…OSINT.

## Scenariusz i rozwój ładunku

Przekształć dane wywiadowcze w realistyczne, ale nieszkodliwe wiadomości: przypomnienie o fakturze, powiadomienie IT lub aktualizację działu kadr, która wygląda i brzmi jak prawdziwa. Ładunki powinny wspierać uczenie się, a nie wykorzystywanie: linki śledzące, firmowe strony docelowe przechwytujące metadane oraz nieszkodliwe załączniki są odpowiednie. Unikaj całkowicie złośliwego oprogramowania i przechwytywania danych uwierzytelniających na żywo; korzystaj z symulowanych stron logowania i fałszywych kont, aby mierzyć zachowania wolne od ryzyka.

## Eksploatacja i posteksploatacja

Przeprowadź kampanię zgodnie z ustalonym planem, w turach lub w formie pojedynczej wysyłki, i monitoruj otwarcia, kliknięcia, symulowane zgłoszenia i raporty w czasie rzeczywistym. Zadbaj o to, aby wyłącznik awaryjny i ścieżka eskalacji były widoczne dla zespołu i natychmiast wstrzymaj działanie, jeśli wiadomości wyjdą poza zakres lub spowodują niezamierzone konsekwencje. Korzystaj z narzędzi bezpiecznych dla laboratoriów, takich jak **GoPhish** lub podobna platforma testowa, i kieruj działania do prawdziwych użytkowników dopiero po uzyskaniu uprzedniej pisemnej zgody.

## Raportowanie i podsumowanie

Przeanalizuj, co się stało i dlaczego: wskaźniki klikalności, próby przesłania, zachowania związane ze zgłaszaniem i harmonogram w różnych zespołach. Przedstaw wnioski bez wymieniania konkretnych osób i skup się na praktycznych usprawnieniach, takich jak ukierunkowane szkolenia.phishing-odpornyMFA,SPF/DKIM/DMARCKonfiguracja i inne kontrole techniczne, które zmniejszają ryzyko, kończą się uzgodnionymi działaniami następczymi i rozsądnym rytmem ponownego testowania, co pozwala na mierzenie postępów w czasie. Poniższa tabela przedstawia przegląd najczęściej używanych wskaźników podczasphishingkampanie, a także kilka punktów odniesienia i rekomendacji klientów.

## Tabela rekomendacji

AphishingSymulacja przynosi wartość tylko wtedy, gdy jej wyniki są jasno zakomunikowane klientowi. Obowiązki testera penetracyjnego wykraczają poza zakończenie kampanii; kluczowe jest przełożenie surowych metryk na praktyczne wnioski. Poniższa tabela przedstawia ramy tego procesu: biorąc pod uwagę metrykę i jej punkt odniesienia, można sformułować odpowiednie rekomendacje. To podejście odzwierciedla strukturę profesjonalnegophishingraport.

|Metryczny|Co mierzy|Reper|Sugerowane zalecenia|
|---|---|---|---|
|Współczynnik otwarć|% użytkowników, którzy otworzyli wiadomość e-mail.|Branża jest zróżnicowana; typowaphishingwspółczynniki otwarć ~50–65%|Celowane szkolenie uzupełniające|
|Współczynnik klikalności|% wszystkich użytkowników, którzy kliknęli link.|8–14% akceptowalne; >14% wysokie ryzyko|Skoncentrowane szkolenie w zakresie świadomości bezpieczeństwa|
|Wskaźnik wejścia na studia|% wszystkich użytkowników, którzy wprowadzili dane uwierzytelniające po kliknięciu.|<2% niskie ryzyko; 2–5% umiarkowane ryzyko; >5% wysokie ryzyko|Phishingszkolenie w zakresie identyfikacji lokalizacji,MFArealizacja|
|Szybkość detonacji załącznika|% użytkowników, którzy otworzyli/uruchomili załącznik.|Brak formalnego punktu odniesienia; >5–7% sugeruje ryzyko|Edukacja na temat bezpiecznego obchodzenia się z osprzętem,Piaskownicadetonacja|
|Częstotliwość zgłaszania (24h)|% użytkowników, którzy zgłosili otrzymanie wiadomości e-mail w ciągu 24 godzin.|>40% silne; 30–40% przeciętne; <30% słabe|Kampania na rzecz zwiększania świadomości|

## Scenariusz

Po naszym OSINT śledztwie w końcu zidentyfikowaliśmy dobry cel dla naszego ostrzału phishing Atak: Bob, szef finansów w TryAccounting. Za pośrednictwem LinkedIn znaleźliśmy ten adres e-mail: `bob@tryaccounting.thm`. W jednej z ofert pracy dla inżyniera cyberbezpieczeństwa dowiedzieliśmy się, że:

- Stosuj rygorystyczną politykę dotyczącą haseł (może to być dobry pretekst w wiadomościach phishingowych)
- Użyj zabezpieczeń poczty e-mail, więc może być konieczne wykonanie podstawowego podszywania się pod adres e-mail

Naszym celem jest zdobycie danych uwierzytelniających Boba, dlatego stworzymy aplikację phishingową, aby je zdobyć.

## Przygotowanie ataku

Najpierw nawiąż połączenie SSH z maszyną wirtualną, używając następujących danych logowania:

**Referencje**

Nazwa użytkownika

napastnik

Hasło

atakujący1234

Adres IP

Adres IP maszyny

Połączenie przez

SSH

sshatakujący@MACHINE_IP

Następnie musimy uruchomić Zestaw narzędzi do inżynierii społecznej. Na maszynie wirtualnej znajduje się alias, który ułatwia sprawę: wystarczy wpisać `SET`i nacisnąć Enter.

Jak widać, możemy wybierać spośród kilku modułów. W ramach tego ćwiczenia skonfigurujemy narzędzie do zbierania danych uwierzytelniających z niestandardowym kodem HTML. Pozwoli nam to skonfigurowaćphishingwitryna korzysta z naszego własnego kodu HTML.

Wybierz pierwszą opcję: **Ataki socjotechniczne** :

Terminal

```shell-session
attacker@tryhackme$ SET
Select from the menu:

   1) Social-Engineering Attacks
   2) Penetration Testing (Fast-Track)
   3) Third Party Modules
   4) Update the Social-Engineer Toolkit
   5) Update SET configuration
   6) Help, Credits, and About

  7) Exit the Social-Engineer Toolkit

set 1
 
```

Następnie wybierzemy drugą opcję, **Wektory ataków na witryny internetowe** , a potem trzecią opcję, **Metoda ataku Credential Harvester** :

Terminal

```shell-session

 Select from the menu:

   1) Spear-Phishing Attack Vectors
   2) Website Attack Vectors
   3) Infectious Media Generator
   4) Create a Payload and Listener
   5) Mass Mailer Attack
   6) Arduino-Based Attack Vector
   7) Wireless Access Point Attack Vector
   8) QRCode Generator Attack Vector
   9) Powershell Attack Vectors
  10) Third Party Modules

  11) Return back to the main menu.

set 2

 1) Java Applet Attack Method
   2) Metasploit Browser Exploit Method
   3) Credential Harvester Attack Method
   4) Tabnabbing Attack Method
   5) Web Jacking Attack Method
   6) Multi-Attack Web Method
   7) HTA Attack Method

  8) Return to Main Menu

set 3
```

Wybierz trzecią opcję, **Import niestandardowy,**  aby móc użyć własnego pliku HTML. Podczas prawdziwej kampanii użylibyśmy opcji „Site Cloner”, aby utworzyć realistyczną kopię aplikacji internetowej naszego celu. Gdy pojawi się monit o podanie adresu IP dla żądania POST, upewnij się, że adres IP jest taki sam jak `MACHINE_IP`:

Terminal

```shell-session
  
   1) Web Templates
   2) Site Cloner
   3) Custom Import

  4) Return to Webattack Menu

set 3

set:webattack IP address for the POST back in Harvester/Tabnabbing [10.10.189.116]: 
```

Następnie podaj ścieżkę do pliku index.html `/home/attacker/setoolkit/`i wybierz pierwszą opcję: **Kopiuj tylko plik index.html** . Na koniec wpisz poniższy adres URL `http://tryacounting.thm`i naciśnij Enter:

Terminal

```shell-session
[!] Example: /home/website/ (make sure you end with /)
[!] Also note that there MUST be an index.html in the folder you point to.
set:webattack Path to the website to be cloned: /home/ubuntu/setoolkit/
[*] Index.html found. Do you want to copy the entire folder or just index.html?

1. Copy just the index.html
2. Copy the entire folder

Enter choice [1/2]: 1
[-] Example: http://www.blah.com
set:webattack URL of the website you imported: http://tryacounting.thm

The best way to use this attack is if username and password form fields are available. Regardless, this captures all POSTs on a website.
[*] The Social-Engineer Toolkit Credential Harvester Attack
[*] Credential Harvester is running on port 80
[*] Information will be displayed to you as it arrives below:
```

**Pozostaw okno terminala otwarte, ponieważ to właśnie tutaj przechwycę dane uwierzytelniające naszego celu.**

Zwróć uwagę na celową literówkę w domenie: brakuje jednego „c”. W przypadku ataku phishingowego, kontrola nad domeną, która uległa typosquattingowi, może zmaksymalizować nasze szanse na sukces. Powinieneś zobaczyć wynik wskazujący, że program **Credential Harvester działa na porcie 80.** Wynik można wyświetlić, wpisując `http://MACHINE_IP` w przeglądarce:

![Sklonowana strona logowania TryAccounting umieszczona na komputerze atakującego, pokazująca narzędzie do zbierania danych uwierzytelniających działające na porcie 80](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1774966013945.png)

## Czas na phishing

Następnym krokiem będzie utworzenie i wysłanie naszegophishinge-mail. Przejdź do `http://MACHINE_IP:8080`przeglądarki Attackboxes i zaloguj się do klienta Rainloop, używając adresu e-mail **attacker@phisher.thm** i hasła **attacker1234.**

Podczas fazy rozpoznania odkryliśmy, że TryAccounting może korzystać z zabezpieczeń poczty e-mail. Jeśli spróbujemy wysłać wiadomość e-mail do naszego celu, `bob@tryaccounting.thm`, otrzymamy następującą odpowiedź:

![Odpowiedź informująca o niedostarczeniu wiadomości e-mail, pokazująca, że ​​zabezpieczenia poczty e-mail TryAccounting blokują sfałszowaną wiadomość wysłaną z adresu atakującego](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1761315547999.png)

W Rainloop możemy używać aliasów, które ułatwiają nam podstawowe podszywanie się. 

Kliknij przycisk „Nowa wiadomość”, następnie w nowym e-mailu kliknij adres e-mail atakującego znajdujący się obok pola „Od” i wybierz go `support@tryaccounting.thm`z listy rozwijanej. W ten sposób będziemy sprawiać wrażenie, że jesteśmy pracownikiem wysyłającym wewnętrzną wiadomość e-mail do `bob@tryaccounting.thm`:

![Rozwijana lista w polu „Od” klienta poczty Rainloop, wyświetlająca alias support@tryaccounting.thm wybrany do podszywania się pod adres e-mail](https://cdn-images.tryhackme.com/user-uploads/62ff64c3c859dc0042b2b9f6/room-content/62ff64c3c859dc0042b2b9f6-1761315899589.png)

Możemy wykorzystać poniższy adres e-mail i wymyślić przekonujący temat, na przykład: „Wymagane działanie: Powiadomienie o wygaśnięciu hasła”

```html
Dear Bob,

As part of our security policy, we require all TryAccounting employees to change their passwords every 3 months. Please log in to our internal portal and update your password before Friday:
http://tryacounting.thm
Thank you,
TryAccounting Support Team
```

W końcu możemy wysłać tego e-maila do Boba. Tym razem nie otrzymaliśmy powiadomienia o bezpieczeństwie e-maila. Jeśli wrócimy do okna terminala, powinniśmy zobaczyć jego dane uwierzytelniające.

Terminal

```shell-session
attacker@tryhackme$ 
[*] WE GOT A HIT! Printing the output:
POSSIBLE USERNAME FIELD FOUND: username=bob.wilkinson
POSSIBLE PASSWORD FIELD FOUND: password=***************
[*] WHEN YOU'RE FINISHED, HIT CONTROL-C TO GENERATE A REPORT.
```

Gratulacje z okazji udanego wykonania włóczniphishingatak!

W tym pomieszczeniu zgłębialiśmy podstawyphishingz perspektywy testera penetracyjnego, w tym psychologii stojącej zainżynieria społeczna, techniki techniczne, takie jak podszywanie się ityposquattingi niektóre narzędzia używane do uruchomieniaphishingkampanie.

Rozumiejąc jakphishingdziała i jak można to etycznie symulować, posiadasz teraz kluczową umiejętność w swoim zestawie narzędzi do testów penetracyjnych.
