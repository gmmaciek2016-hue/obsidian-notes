---

Interfejs rozszerzeń w pakiecie Burp Suite zapewnia przegląd rozszerzeń wczytanych do narzędzia. Przyjrzyjmy się różnym komponentom tego interfejsu:

![Interfejs rozszerzeń](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/499907ccb192f8deb8f473accd967df9.png)

1. **Lista rozszerzeń** : W górnym polu wyświetlana jest lista rozszerzeń aktualnie zainstalowanych w Burp Suite dla bieżącego projektu. Umożliwia ona aktywację lub dezaktywację poszczególnych rozszerzeń.
2. **Zarządzanie rozszerzeniami** : Po lewej stronie interfejsu rozszerzeń znajdują się opcje umożliwiające zarządzanie rozszerzeniami:
    - **Dodaj** : Możesz użyć tego przycisku, aby zainstalować nowe rozszerzenia z plików na swoim dysku. Mogą to być moduły zakodowane niestandardowo lub pobrane z zewnętrznych źródeł, które nie są dostępne w oficjalnym sklepie BApp.
    - **Usuń** : Ten przycisk umożliwia odinstalowanie wybranych rozszerzeń z Burp Suite .
    - **W górę/W dół** : Te przyciski kontrolują kolejność, w jakiej wyświetlane są zainstalowane rozszerzenia. Kolejność ta określa kolejność wywoływania rozszerzeń podczas przetwarzania ruchu. Rozszerzenia są stosowane w kolejności malejącej, zaczynając od góry listy i przesuwając się w dół. Kolejność jest istotna, zwłaszcza w przypadku rozszerzeń modyfikujących żądania, ponieważ niektóre mogą kolidować z innymi lub powodować konflikty.
3. **Szczegóły, dane wyjściowe i błędy** : Na dole okna znajdują się sekcje dotyczące aktualnie wybranego rozszerzenia:
    - **Szczegóły** : W tej sekcji znajdują się informacje o wybranym rozszerzeniu, takie jak jego nazwa, wersja i opis.
    - **Dane wyjściowe** : Rozszerzenia mogą generować dane wyjściowe w trakcie wykonywania. W tej sekcji wyświetlane są wszelkie istotne dane wyjściowe i wyniki.
    - **Błędy** : Jeśli rozszerzenie napotka jakiekolwiek błędy podczas wykonywania, zostaną one wyświetlone w tej sekcji. Może to być przydatne podczas debugowania i rozwiązywania problemów z rozszerzeniami.

Podsumowując, interfejs rozszerzeń w pakiecie Burp Suite umożliwia użytkownikom zarządzanie zainstalowanymi rozszerzeniami i monitorowanie ich, aktywowanie lub dezaktywowanie w określonych projektach oraz przeglądanie ważnych szczegółów, wyników i błędów związanych z każdym rozszerzeniem. Dzięki rozszerzeniom Burp Suite staje się potężną i konfigurowalną platformą do różnorodnych zadań związanych z testowaniem bezpieczeństwa i oceną aplikacji internetowych.

W Burp Suite , BApp Store (Burp App Store) pozwala nam łatwo odkrywać i bezproblemowo integrować oficjalne rozszerzenia z narzędziem. Rozszerzenia mogą być napisane w różnych językach, z których najpopularniejsze to Java i Python. Rozszerzenia Javy integrują się automatycznie z frameworkiem Burp Suite , natomiast rozszerzenia Pythona wymagają interpretera Jython.

Aby zapoznać się ze sklepem BApp Store i zainstalować rozszerzenie Java, zainstalujmy rozszerzenie [Request Timer](https://github.com/portswigger/request-timer)  autorstwa Nicka Taylora. Rozszerzenie Request Timer umożliwia rejestrowanie czasu potrzebnego na otrzymanie odpowiedzi na każde żądanie. Ta funkcjonalność jest szczególnie przydatna do identyfikowania i wykorzystywania luk w zabezpieczeniach opartych na czasie. Na przykład, jeśli formularz logowania przetwarza żądania z prawidłowymi nazwami użytkowników dłużej niż z nieprawidłowymi, możemy wykorzystać różnice czasu do określenia, które nazwy użytkowników są prawidłowe.

Aby zainstalować rozszerzenie Request Timer ze sklepu BApp Store, wykonaj następujące czynności:

1. Przejdź do podzakładki **BApp Store w** Burp Suite .
2. Użyj funkcji wyszukiwania, aby znaleźć **„Request Timer”** . Dla tego rozszerzenia powinien zostać wyświetlony tylko jeden wynik.
3. Aby zobaczyć więcej szczegółów, kliknij zwrócone rozszerzenie.
4. Kliknij przycisk **Instaluj**  , aby zainstalować rozszerzenie Request Timer.

![Proces instalacji timera żądania ze sklepu BApp Store](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f667309abf35384b10ab28ffe04da311.png)

Po pomyślnej instalacji rozszerzenia zauważysz nową zakładkę w menu głównym u góry interfejsu Burp Suite . Różne rozszerzenia mogą działać w różny sposób. Niektóre mogą dodawać nowe elementy do menu kontekstowych prawego przycisku myszy, podczas gdy inne tworzą zupełnie nowe zakładki na pasku menu głównego.

Ponieważ ta instalacja to jedynie przykład korzystania ze sklepu BApp Store, nie będziemy tutaj omawiać, jak korzystać z Request Timer. Gorąco polecam jednak przejście do nowej karty i zapoznanie się z rozszerzeniem, aby lepiej zrozumieć jego funkcje. Request Timer może być przydatny w różnych scenariuszach, zwłaszcza podczas oceny bezpieczeństwa aplikacji internetowych i identyfikacji potencjalnych luk w zabezpieczeniach opartych na czasie.

**Uwaga:** Jeśli używasz AttackBox, integracja Jython została już wykonana, więc możesz pominąć to zadanie.

Aby korzystać z modułów Pythona w Burp Suite , musimy dołączyć plik JAR interpretera Jython , który jest implementacją Pythona w Javie. Interpreter Jython umożliwia uruchamianie rozszerzeń opartych na Pythonie w Burp Suite.

Aby zintegrować Jython z Burp Suite na swoim komputerze lokalnym, wykonaj następujące kroki:

1. **Pobierz JAR** Jython : Odwiedź [stronę Jython](https://www.jython.org/download) i pobierz samodzielne archiwum JAR . Znajdź opcję **Jython Standalone** . Zapisz plik JAR w wybranym miejscu na dysku.
    
    ![Link do pobrania wersji samodzielnej Jython](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/bdfe7373a7aa5fc356cdd95f0f7a2370.png)
    
2. **Skonfiguruj Jython w Burp Suite** : Otwórz Burp Suite i przejdź do modułu **Rozszerzenia** . Następnie przejdź do podzakładki **Ustawienia rozszerzeń .**
3. **Środowisko Pythona** : Przewiń w dół do sekcji „Środowisko Pythona”.
4. **Ustaw lokalizację pliku JAR** Jython : W polu „Lokalizacja samodzielnego pliku JAR Jython ” ustaw ścieżkę do pobranego pliku JAR Jython .
    
    ![Ustawianie lokalizacji Jython Standalone](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/092c98a31ec4a28c39ef9e1446305762.png)

Po wykonaniu tych kroków Jython zostanie zintegrowany z Burp Suite , umożliwiając korzystanie z modułów Pythona w narzędziu. Ta integracja znacząco zwiększa liczbę dostępnych rozszerzeń i usprawnia wykonywanie różnorodnych zadań związanych z testowaniem bezpieczeństwa i oceną aplikacji internetowych.

**Uwaga:** Proces dodawania Jythona do Burp Suite jest taki sam dla wszystkich systemów operacyjnych, ponieważ Java jest technologią wieloplatformową.

API

W module rozszerzeń Burp Suite masz dostęp do szerokiej gamy punktów końcowych API , które umożliwiają tworzenie i integrację modułów z Burp Suite . Te API udostępniają różnorodne funkcjonalności, umożliwiając rozszerzenie możliwości Burp Suite zgodnie z Twoimi specyficznymi potrzebami.

Aby wyświetlić dostępne punkty końcowe API , przejdź do podzakładki **API** w module Rozszerzenia. Każdy element wymieniony w lewym panelu reprezentuje inny punkt końcowy API , do którego można uzyskać dostęp z poziomu rozszerzeń.

![Interfejsy API rozszerzenia Burp Suite](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/b815da3ba5714ffd2cbfa13c1c034aae.png)

Interfejsy API rozszerzeń dają programistom znaczną swobodę i elastyczność podczas tworzenia własnych rozszerzeń. Możesz ich używać do płynnej interakcji z istniejącymi funkcjami Burp Suite i dostosowywania rozszerzeń do wykonywania określonych zadań.

Burp Suite obsługuje wiele języków do pisania rozszerzeń, takich jak:

1. Java (natywnie): Możesz bezpośrednio używać Javy do pisania rozszerzeń dla Burp Suite , korzystając z dostępnych zaawansowanych interfejsów API.
2. Python (za pośrednictwem Jython): Jeśli wolisz Pythona jako swój język programowania, możesz wykorzystać Jython, czyli implementację Pythona w Javie, służącą do tworzenia rozszerzeń Burp Suite .
3. Ruby (za pośrednictwem JRuby): Programiści znający język Ruby mogą wykorzystać JRuby, implementację języka Ruby w języku Java, do tworzenia rozszerzeń pakietu Burp Suite .

Należy pamiętać, że kodowanie rozszerzeń dla Burp Suite może być złożonym zadaniem i wykracza poza zakres tego modułu. Załóżmy jednak, że chcesz zgłębić ten temat i stworzyć własne rozszerzenia. W takim przypadku PortSwigger oferuje kompleksowy podręcznik, który stanowi doskonałe źródło informacji do tworzenia rozszerzeń Burp Suite .

Aby dowiedzieć się więcej o tworzeniu rozszerzeń Burp Suite i uzyskać dostęp do szczegółowych informacji, zapoznaj się z oficjalną [dokumentacją](https://portswigger.net/burp/extender/writing-your-first-burp-suite-extension) PortSwigger . Zasób ten zawiera informacje i wskazówki niezbędne do tworzenia zaawansowanych i dostosowanych rozszerzeń, które ulepszą Twoje doświadczenia z Burp Suite .

Gratulacje! Ukończyłeś moduł „Rozszerzenia Burp Suite” . Dzięki niemu zdobyłeś cenne informacje na temat korzystania z rozszerzeń w celu zwiększenia funkcjonalności Burp Suite .

Teraz masz już solidną wiedzę na temat tego, jak:

1. Instaluj i zarządzaj rozszerzeniami ze sklepu BApp, aby rozszerzyć możliwości Burp Suite.
2. Zintegruj Jython, aby wykorzystać moduły Pythona w Burp Suite .
3. Poznaj interfejsy API umożliwiające tworzenie niestandardowych modułów Java, Python lub Ruby.

Dzięki tym umiejętnościom będziesz mógł w pełni wykorzystać potencjał modułu Burp Suite Extensions podczas testowania zabezpieczeń aplikacji internetowych i oceny podatności na zagrożenia.

Świetna robota z ukończeniem modułu i gratulacje za poświęcenie i wysiłek! Kontynuuj zgłębianie wiedzy, uczenie się i doskonalenie umiejętności z zakresu cyberbezpieczeństwa. Powodzenia w hakowaniu!
