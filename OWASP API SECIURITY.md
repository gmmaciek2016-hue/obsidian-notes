---

W [poprzednim pokoju](https://tryhackme.com/jr/owaspapisecuritytop105w) studiowaliśmy pierwsze pięć zasad OWASP API Bezpieczeństwo. Teraz, w tym pomieszczeniu, krótko omówimy pozostałe zasady, ich potencjalny wpływ i środki zaradcze.

**Cele edukacyjne**

- Identyfikacja błędnych konfiguracji zabezpieczeń
- Zapobieganie odmowie usługi (DoS) przeciwkoAPI
- Zapewnienie odpowiedniego rejestrowania i monitorowania

**Wymagania wstępne dotyczące nauki**  
Przed rozpoczęciem zajęć zaleca się zapoznanie się z poniższymi tematami:

- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)
- [HTTPprotokoły i metody](https://tryhackme.com/room/protocolsandservers)
- [Zasady bezpieczeństwa](https://tryhackme.com/room/principlesofsecurity)
- [OWASP10 najpopularniejszych luk w zabezpieczeniach sieci](https://tryhackme.com/room/owasptop10)

**Łączenie się z maszyną**  
Będziemy używać systemu Windows jako maszyny testowej/rozwojowej wraz z TalendemAPITester - bezpłatna edycja w całym pokoju, z następującymi uprawnieniami:

- Adres IP maszyny:  `MACHINE_IP` 
- Nazwa użytkownika:   `Administrator`
- Hasło:    `Owasp@123`

Możesz uruchomić maszynę wirtualną, klikając .  `Start Machine button`Maszyna uruchomi się w widoku podzielonego ekranu. W przypadkuMaszyna wirtualnaJeśli nie jest widoczny, użyj niebieskiego przycisku „Pokaż podzielony widok” w prawym górnym rogu strony. Alternatywnie możesz  połączyć się zMaszyna wirtualnaZa pomocą Pulpitu Zdalnego,  używając powyższych danych logowania.  Odczekaj 1-2 minuty po pełnym uruchomieniu systemu, aby umożliwić automatyczne uruchomienie skryptów, które uruchomią Talend.APIAutomatyczne testowanie i tworzenie aplikacji internetowych opartych na platformie Laravel.

![Obraz dla RDP](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/2e8676dbcc93a6ac0b3f4a491be2ff06.png)

﻿**Jak to się dzieje?**

Masowe przypisanie odzwierciedla scenariusz, w którym **dane po stronie klienta są automatycznie powiązane z obiektami po stronie serwera lub zmiennymi klas** . Jednak hakerzy wykorzystują tę funkcję, najpierw rozumiejąc **logikę biznesową aplikacji** i wysyłając specjalnie spreparowane dane do serwera, uzyskując dostęp administracyjny lub wstawiając zmodyfikowane dane. Ta funkcjonalność jest szeroko wykorzystywana w najnowszych frameworkach, takich jak Laravel, Code Ignitor itp.  

 Rozważmy panel profili użytkowników , gdzie użytkownicy mogą aktualizować swój profil, podając powiązany adres e-mail, imię i nazwisko, adres itp. Nazwa użytkownika jest atrybutem tylko do odczytu i nie można jej zmienić; jednak atakujący może ją edytować i przesłać formularz. Jeśli filtrowanie nie jest włączone po stronie serwera (modelu), dane zostaną po prostu wstawione/zaktualizowane w bazie danych. 

**Prawdopodobny wpływ** 

Atak może skutkować **manipulacją danymi i podniesieniem uprawnień** ze zwykłego użytkownika na administratora. 

Przykład praktyczny  

- OtwórzMaszyna wirtualna. Odkryjesz, że przeglądarka Chrome i TalendAPIAplikacje testowe są uruchamiane automatycznie i będziemy ich używać do debugowaniaAPIpunkty końcowe.  
    
- Bobowi powierzono zadanie opracowania systemu rejestracjiAPIPunkt końcowy `/apirule6/user` , który przyjmuje nazwę, nazwę użytkownika i hasło jako parametry wejściowe (POST). Tabela użytkownika ma `credit column`wartość domyślną `50`. Użytkownicy uaktualnią swoje członkostwo, aby uzyskać większą wartość kredytową.
- Bobowi udało się zaprojektować formularz i wykorzystać funkcję masowego przypisywania w Laravel do przechowywania wszystkich danych przychodzących od strony klienta do bazy danych (jak pokazano poniżej).

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/31d541b9eb6d7f67dec8fdb60d07f8af.png)  

- W czym tu problem? Bob nie stosuje żadnego filtrowania po stronie serwera. Odkąd korzysta z **funkcji masowego przypisywania** , wstawia również wartości punktów do bazy danych (złośliwi użytkownicy mogą aktualizować te wartości).  
    
- Rozwiązanie problemu jest dość proste. Bob musi zapewnić odpowiednie filtrowanie po stronie serwera ( `apirule6/user_s`) i upewnić się, że domyślna wartość kredytu zostanie wprowadzona jako `50`, nawet jeśli od klienta zostanie odebrana wartość powyżej 50 (jak pokazano poniżej). 

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/bfb2c99ce2c72649953967a629cbcc39.png)  

**Środki łagodzące** 

- Przed użyciem jakiegokolwiek frameworka należy zapoznać się ze sposobem wykonywania operacji wstawiania i aktualizacji w back-endzie. W frameworku Laravel, [wypełnianie i zabezpieczanie(otwiera się w nowej karcie)](https://laravel.com/docs/9.x/eloquent)tablice łagodzą wyżej wymienione scenariusze. 
- Unikaj stosowania funkcji, które automatycznie wiążą dane wejściowe od klienta ze zmiennymi kodu.
- Dodaj do listy dozwolonych tylko te właściwości, które wymagają aktualizacji po stronie klienta.

﻿**Jak to się dzieje?**

Nieprawidłowa konfiguracja zabezpieczeń oznacza wdrożenie **nieprawidłowych i źle skonfigurowanych kontroli bezpieczeństwa** , które zagrażają bezpieczeństwu całego systemu. API Stawką jest ryzyko. Błędna konfiguracja zabezpieczeń może wynikać z kilku czynników, w tym nieprawidłowej/niekompletnej konfiguracji domyślnej, publicznie dostępnego przechowywania danych w chmurze, [udostępniania zasobów między różnymi źródłami (CORS)(otwiera się w nowej karcie)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)oraz komunikaty o błędach wyświetlane z poufnymi danymi. Intruzi mogą wykorzystać te błędne konfiguracje do przeprowadzenia szczegółowego rozpoznania i uzyskania nieautoryzowanego dostępu do systemu. 

Błędy w konfiguracji zabezpieczeń są zwykle wykrywane przez skanery podatności lub narzędzia audytowe, dzięki czemu można je ograniczyć już na wstępnym etapie. API dokumentacja, lista punktów końcowych, dzienniki błędów itp. **nie mogą być publicznie dostępne** , aby zapewnić bezpieczeństwo przed błędami w konfiguracji zabezpieczeń. Zazwyczaj firmy wdrażają zabezpieczenia, takie jak zapory sieciowe aplikacji internetowych, które nie są skonfigurowane do blokowania niepożądanych żądań i ataków.  

**Prawdopodobny wpływ** 

Błędna konfiguracja zabezpieczeń może dać intruzom pełną wiedzę o API Po pierwsze, pozwala intruzom ominąć mechanizmy bezpieczeństwa. **Ślad stosu lub inne szczegółowe błędy** mogą zapewnić atakującemu dostęp do poufnych danych i istotnych szczegółów systemu, co dodatkowo ułatwia intruzowi profilowanie systemu i uzyskanie dostępu.    

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i Talend API Tester do debugowania w Maszyna wirtualna.  
    
- Firma MHT boryka się z poważnymi problemami z dostępnością serwerów. Dlatego zlecili Bobowi opracowanieAPIpunkt końcowy `/apirule7/ping_v`(GET), który będzie udostępniał szczegóły dotyczące stanu i kondycji serwera.
- Bobowi udało się zaprojektować punkt końcowy, zapomniał jednak o zaimplementowaniu obsługi błędów, aby zapobiec wyciekowi informacji.

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/76b0298b5134ca3c04e4290b15f4e73a.png)  

- Na czym polega problem? W przypadku nieudanego wywołania serwer wysyła w odpowiedzi pełny ślad stosu, zawierający nazwy funkcji, informacje o kontrolerze i trasie, ścieżkę do pliku itp. Atakujący może wykorzystać te informacje do profilowania i przygotowania konkretnych ataków na środowisko.  
    
- Rozwiązanie problemu jest dość proste. Bob utworzy punkt końcowy API `/apirule7/ping_s` , który będzie obsługiwał błędy i udostępniał użytkownikowi tylko żądane informacje (jak pokazano poniżej).

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9087274b07f2fa5174398b0bb0c69979.png)  

**Środki łagodzące** 

- Ogranicz dostęp do interfejsów administracyjnych dla autoryzowanych użytkowników i wyłącz go dla pozostałych użytkowników. 
- Wyłącz domyślne nazwy użytkowników i hasła dla urządzeń publicznych (routery, aplikacje internetowe)Zapora sieciowaitp.).
- Wyłączyćlista katalogowai ustaw odpowiednie uprawnienia dla każdego pliku i folderu. 
- Usuń niepotrzebne fragmenty kodu, dzienniki błędów itp. i wyłącz debugowanie, gdy kod jest w produkcji.

**Jak to się dzieje?**

Ataki wstrzyknięciami należą prawdopodobnie do najstarszychAPI/ataki internetowe i nadal są przeprowadzane przez hakerów w rzeczywistych aplikacjach. Luki związane z wstrzykiwaniem kodu występują, gdy dane wejściowe użytkownika **nie są filtrowane i są przetwarzane bezpośrednio przezAPI**; umożliwiając w ten sposób atakującemu wykonanie niezamierzonych działańAPIdziałania bez autoryzacji. Wstrzyknięcie może pochodzić z [języka zapytań strukturalnych (SQL)](https://tryhackme.com/room/sqlinjectionlm) , system operacyjny (System operacyjny) polecenia, Extensible Markup Language (XML) itd.  Obecnie frameworki oferują funkcjonalność chroniącą przed tym atakiem poprzez automatyczne oczyszczanie danych; jednak aplikacje zbudowane w niestandardowych frameworkach, takich jak corePHPnadal są podatne na takie ataki. 

**Prawdopodobny wpływ** 

Wady wstrzykiwania mogą prowadzić do **ujawnienia informacji, utraty danych,DoSi całkowite przejęcie konta** . Skuteczne ataki typu injection mogą również umożliwić intruzom dostęp do poufnych danych, a nawet stworzenie nowej funkcjonalności i zdalne wykonanie kodu. 

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i Talend API Tester do debugowania w Maszyna wirtualna.  
    
- Kilku użytkowników firmy MHT zgłosiło, że hasło do ich konta uległo zmianie i nie mogli się już zalogować na swoje pierwotne konto. W rezultacie zespół programistów odkrył, że Bob opracował podatny na ataki kod logowania. API punkt końcowy `/apirule8/user/login_v`, który nie filtruje danych wprowadzanych przez użytkownika.  
    
- Złośliwy atakujący potrzebuje nazwy użytkownika celu, a jako hasło może wykorzystać ładunek `' OR 1=1--'` i uzyskać klucz autoryzacyjny dla dowolnego konta (jak pokazano poniżej).

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/fb4649a8c9226d5c68d2ece9e1e1246a.png)  

- Bob natychmiast zdał sobie sprawę ze swojego błędu; zaktualizował punkt końcowy API `/apirule8/user/login_s`i użył sparametryzowanych zapytań oraz wbudowanych filtrów Laravel, aby oczyścić dane wprowadzane przez użytkownika.
- W rezultacie wszystkie złośliwe ładunki dotyczące parametrów nazwy użytkownika i hasła zostały skutecznie ograniczone (jak pokazano poniżej)

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/496f9d46040c7a3088f710bbe29cfc0a.png)  

**Środki łagodzące**

- Należy upewnić się, że używana jest znana biblioteka do walidacji danych wejściowych po stronie klienta.
- Jeśli nie korzysta się z żadnej struktury, wszystkie dane dostarczone przez klienta muszą zostać najpierw zweryfikowane, a następnie przefiltrowane i oczyszczone. 
- Dodaj niezbędne zasady bezpieczeństwa do aplikacji internetowejZapora sieciowa(WAF). W większości przypadków luki w zabezpieczeniach można ograniczyć na poziomie sieci.
- Skorzystaj z wbudowanych filtrów w frameworkach takich jak Laravel, Code Ignitor itp., aby sprawdzać poprawność i filtrować dane.

﻿**Jak to się dzieje?**

Niewłaściwe zarządzanie aktywami odnosi się do scenariusza, w którym mamy **dwie wersje API Dostępne w naszym systemie** ; nazwijmy je APIv1 i APIv2. Wszystko jest w całości przełączone na APIv2, ale poprzednia wersja, APIv1, nie została jeszcze usunięta. Biorąc to pod uwagę, można łatwo zgadnąć, że starsza wersja API, tj. APIv1, nie posiada zaktualizowanych ani najnowszych funkcji bezpieczeństwa. Wiele innych przestarzałych funkcji APIv1 umożliwia znalezienie podatnych scenariuszy, które mogą prowadzić do wycieku danych i przejęcia serwera poprzez współdzieloną bazę danych. API wersje.

W zasadzie chodzi o nieprawidłowe śledzenie API punkty końcowe. Potencjalne przyczyny mogą być niekompletne API dokumentacji lub braku zgodności z [cyklem życia oprogramowania](https://tryhackme.com/room/securesdlc) . Prawidłowo utrzymywana, aktualna dokumentacja API inwentaryzacja i odpowiednia dokumentacja są dla organizacji ważniejsze niż kontrola bezpieczeństwa oparta na sprzęcie.  

**Prawdopodobny wpływ** 

Starsze lub **niełataneAPIwersje** mogą umożliwić intruzom uzyskanie nieautoryzowanego dostępu do poufnych danych lub nawet całkowitej kontroli nad systemem. 

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i TalendAPITester do debugowania wMaszyna wirtualna.  
    
- PodczasAPIrozwój, firma MHT opracowała różneAPIwersje takie jak v1 i v2. Firma zadbała o korzystanie z najnowszych wersji iAPIpołączeń, ale zapomniał usunąć starą wersję z serwera.  
    
- W rezultacie stwierdzono, że stareAPIpołączenia takie jak `apirule9/v1/user/login`zwracanie dodatkowych informacji, takich jak saldo, adres itp., na temat użytkownika (jak pokazano poniżej).

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/a3d12beaea5bfdbcab5659d9145b189e.png)  

- Bob, będąc twórcą punktu końcowego, zdał sobie sprawę, że musi natychmiast dezaktywować stare i nieużywane zasoby, aby użytkownicy mogli uzyskać dostęp jedynie do ograniczonych i pożądanych informacji z nowego punktu końcowego `/apirul9/v2/user/login`(jak pokazano poniżej).

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/38d853bd141ee2e604216640d3af067c.png)

**Środki łagodzące**   

- Dostęp do wcześniej opracowanych, wrażliwych i przestarzałychAPIpołączenia muszą być blokowane na poziomie sieci.
- Interfejsy API opracowane na potrzeby prac badawczo-rozwojowych, zapewnienia jakości, produkcji itd. muszą być oddzielone i hostowane na oddzielnych serwerach.
- Zapewnij dokumentację wszystkichAPIaspektów, w tym uwierzytelniania, przekierowań, błędów,CORSpolityka i ograniczanie szybkości. 
- Wdrażaj otwarte standardy, aby automatycznie generować dokumentację.

**Jak to się dzieje?**

Niewystarczające rejestrowanie i monitorowanie odzwierciedlają sytuację, w której atakujący prowadzi złośliwą działalność na Twoim serwerze. Jednak gdy próbujesz śledzić hakera, **brakuje wystarczających dowodów z powodu braku mechanizmów rejestrowania i monitorowania** . Wiele organizacji koncentruje się wyłącznie na rejestrowaniu infrastruktury, takiej jak zdarzenia sieciowe lub rejestrowanie serwera, ale brakuje im…APIRejestrowanie i monitorowanie. Informacje takie jak adres IP odwiedzającego, uzyskane punkty końcowe, dane wejściowe itp., wraz ze znacznikiem czasu, umożliwiają identyfikację wzorców ataków stanowiących zagrożenie. Bez mechanizmów rejestrowania zidentyfikowanie atakującego i jego danych byłoby trudne.  Obecnie najnowsze frameworki internetowe mogą automatycznie rejestrować żądania na różnych poziomach, takich jak błąd, debugowanie, informacje itp. Błędy te mogą być rejestrowane w bazie danych lub pliku, a nawet przekazywane do…[SIEMrozwiązanie](https://tryhackme.com/room/defensivesecurity) do szczegółowej analizy.

**Prawdopodobny wpływ** 

Brak możliwości zidentyfikowania atakującego lub hakera stojącego za atakiem. 

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i TalendAPITester do debugowania wMaszyna wirtualna.  
    
- W przeszłości firma MHT była podatna na liczne ataki, a sprawcy tych ataków nie udało się zidentyfikować. Dlatego Bobowi powierzono zadanie…APIpunkt końcowy `/apirule10/logging`(GET), który będzie rejestrował metadane użytkowników (adres IP, wersję przeglądarki itp.) i zapisywał je również w bazie danych (jak pokazano poniżej).  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/9112accb6150c21ee9daadff3d5560e7.png)  

- Później podjęto również decyzję o przekazaniu tego samego doSIEMrozwiązanie do korelacji i analizy.

**Środki łagodzące** 

- Zapewnij korzystanie z Zarządzania informacjami i zdarzeniami bezpieczeństwa (SIEM) system do zarządzania logami. 
- Śledź wszystkie odmowy dostępu, nieudane próby uwierzytelnienia i błędy walidacji danych wejściowych, korzystając z formatu importowanego przezSIEMi wystarczająco dużo szczegółów, aby zidentyfikować intruza.
- Traktuj dzienniki jak dane wrażliwe i upewnij się, że są bezpieczne.uczciwośćNaodpoczyneki tranzyt. Co więcej, wdróż niestandardowe alerty, aby wykrywać podejrzane działania.

Uff. To było proste.  Można by rzec, że ponad **połowa OWASP APILista 10 najważniejszych zagadnień bezpieczeństwa dotyczy autoryzacji i uwierzytelniania** . NajczęściejAPIsystemy padają ofiarą ataków z powodu błędów w mechanizmach autoryzacji i uwierzytelniania oraz błędnej konfiguracji zabezpieczeń.

W paru słowach, API Programiści muszą **chronić interfejsy API zgodnie z najlepszymi praktykami cyberbezpieczeństwa** . Moduły takie jak logowanie, dostęp oparty na rolach, ustawienia profilu użytkownika itp. muszą być traktowane priorytetowo, ponieważ cyberprzestępcy często atakują znane punkty końcowe, aby uzyskać dostęp do systemu.

Bądźcie czujni! I rozwijajcie bezpieczne interfejsy API.
