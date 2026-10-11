---

**Czym jest API i dlaczego jest ważne?**

API to skrót od Application Programming Interface (interfejs programowania aplikacji). Jest to oprogramowanie pośredniczące, które ułatwia komunikację między dwoma komponentami oprogramowania, wykorzystując zestaw protokołów i definicji. W kontekście API termin „ **aplikacja** ” odnosi się do dowolnego oprogramowania o określonej funkcjonalności, a „ **interfejs** ” do kontraktu serwisowego między dwiema aplikacjami, który umożliwia komunikację za pośrednictwem żądań i odpowiedzi. Dokumentacja API zawiera wszystkie informacje na temat struktury tych odpowiedzi i żądań przez programistów.  Znaczenie API dla rozwoju aplikacji można streścić w jednym zdaniu:  **API jest elementem składowym tworzenia złożonych aplikacji klasy korporacyjnej** .

**Ostatnie naruszenia danych za pośrednictwem interfejsów API**

- Wyciek danych z LinkedIn: W czerwcu 2021 roku dane ponad 700 milionów użytkowników LinkedIn zostały wystawione na sprzedaż na jednym z forów w darknecie, a ich pozyskanie nastąpiło poprzez wykorzystanie interfejsu API LinkedIn . Haker opublikował próbkę 1 miliona rekordów, aby potwierdzić autentyczność wycieku danych z LinkedIn, zawierającą pełne imiona i nazwiska użytkowników, adresy e-mail, numery telefonów, dane geolokalizacyjne, linki do profili LinkedIn, informacje o doświadczeniu zawodowym i inne dane dotyczące kont w mediach społecznościowych. 
- Wyciek danych na Twitterze:  W czerwcu 2022 roku dane ponad 5,4 miliona użytkowników [Twittera](https://privacy.twitter.com/en/blog/2022/an-issue-affecting-some-anonymous-accounts) zostały wystawione na sprzedaż w dark webie. Hakerzy dokonali wycieku, wykorzystując lukę typu zero-day w API Twittera , która umożliwiała porównanie nazwy użytkownika Twittera z numerem telefonu komórkowego lub adresem e-mail.
- Wyciek danych PIXLR: W styczniu 2021 roku PIXLR, internetowa aplikacja do edycji zdjęć, padła ofiarą wycieku danych, który dotknął około 1,9 miliona użytkowników. Wszystkie dane hakerów zostały opublikowane na forum dark webowym, gdzie znajdowały się nazwy użytkowników, adresy e-mail, kraje i zaszyfrowane hasła. 

Teraz, gdy poznaliśmy zagrożenia i szkody spowodowane nieprzestrzeganiem środków zapobiegawczych, omówmy opracowanie bezpiecznego interfejsu API zgodnie z **10 najważniejszymi zasadami bezpieczeństwa interfejsu** **API** **OWASP** .
## Luka I — Autoryzacja na poziomie uszkodzonego obiektu (BOLA)

**Jak to się dzieje?**

Generalnie punkty końcowe API są wykorzystywane do powszechnej praktyki pobierania i manipulowania danymi za pomocą identyfikatorów obiektów. #BOLA odnosi się do niezabezpieczonego bezpośredniego odniesienia do obiektu (Insecure Direct Object Reference – IDOR ), które tworzy scenariusz, w którym użytkownik korzysta z **funkcji wprowadzania danych i uzyskuje dostęp do zasobów, do których nie ma uprawnień** .  W API takie kontrolki są zazwyczaj implementowane poprzez programowanie w modelach (architektura Model-Widok-Kontroler) na poziomie kodu.

Prawdopodobny wpływ

Brak mechanizmów kontroli zapobiegających **nieautoryzowanemu dostępowi do obiektów może prowadzić do wycieku danych** , a w niektórych przypadkach do całkowitego przejęcia konta. Dane użytkowników lub subskrybentów w bazie danych odgrywają kluczową rolę w reputacji marki organizacji; wyciek takich danych przez internet może skutkować znacznymi stratami finansowymi.

**Przykład praktyczny**  

- Otwórz maszynę wirtualną . Przeglądarka Chrome i aplikacja Talend API Tester uruchomią się automatycznie, a my użyjemy ich do debugowania punktów końcowych API .
- Bob pracuje jako programista  API`Company MHT`  i opracował punkt końcowy `/apirule1/users/{ID}` , który umożliwi innym aplikacjom lub programistom żądanie informacji poprzez wysłanie identyfikatora pracownika. Na maszynie wirtualnej można żądać wyników, wysyłając `GET` żądania do `http://localhost:80/MHT/apirule1_v/user/1.`

![Obraz dla wniosku o podatność na ataki BOLA](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/a6eec3c1ad211d50ca0ba20ba4f6898e.png)  

- Na czym polega problem z powyższym wywołaniem API? Problem polega na tym, że punkt końcowy nie weryfikuje żadnego przychodzącego wywołania API, aby potwierdzić poprawność żądania. Nie sprawdza też, czy osoba żądająca wywołania API ma prawo o nie poprosić.  
    
- Rozwiązanie tego problemu jest dość proste: Bob wdroży mechanizm autoryzacji, dzięki któremu będzie mógł określić, kto może wykonywać połączenia API w celu uzyskania dostępu do informacji o identyfikatorach pracowników.  
    
- Cel ten osiąga się za pomocą **tokenów dostępu lub tokenów autoryzacji**  w nagłówku. W powyższym przykładzie Bob doda token autoryzacji, aby tylko nagłówki z prawidłowymi tokenami autoryzacji mogły nawiązać połączenie z tym punktem końcowym.
- Na maszynie wirtualnej, tylko dodanie prawidłowego  `Authorization-Token`wywołania `http://localhost:80/MHT/apirule1_s/user/1`, umożliwi uzyskanie poprawnych wyników. Co więcej, wszystkie wywołania API z nieprawidłowym tokenem wyświetlą `403 Forbidden`komunikat o błędzie (jak pokazano poniżej).  

![Obraz dla bezpiecznego żądania BOLA](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/d7276bdd5c3d6fe7b6eea7731d261210.png)  

**Środki łagodzące**

- Należy odpowiednio wdrożyć mechanizm autoryzacji oparty na politykach i hierarchiach użytkowników. 
- Surowe metody kontroli dostępu sprawdzają, czy zalogowany użytkownik jest upoważniony do wykonywania określonych czynności. 
- Promuj używanie całkowicie losowych wartości (silny mechanizm szyfrowania i deszyfrowania) w przypadku tokenów, których prawdopodobieństwo wykrycia jest praktycznie niemożliwe.
## Luka II — zerwane uwierzytelnianie użytkownika (BUA)

**Jak to się dzieje?**

Uwierzytelnianie użytkowników jest kluczowym aspektem tworzenia każdej aplikacji zawierającej wrażliwe dane. Uszkodzone uwierzytelnianie użytkownika (BUA) odzwierciedla scenariusz, w którym punkt końcowy API umożliwia atakującemu dostęp do bazy danych lub uzyskanie wyższych uprawnień niż istniejące. Głównym powodem występowania #BUA jest **nieprawidłowa implementacja uwierzytelniania,** np. użycie niepoprawnych zapytań o adres e-mail/hasło itp., lub brak mechanizmów bezpieczeństwa, takich jak nagłówki autoryzacji, tokeny itp.

Rozważmy scenariusz, w którym atakujący uzyskuje możliwość nadużycia interfejsu API uwierzytelniania ; ostatecznie doprowadzi to do wycieku danych, usunięcia, modyfikacji, a nawet całkowitego przejęcia konta przez atakującego. Zazwyczaj hakerzy tworzą specjalne skrypty do profilowania, enumeracji użytkowników w systemie i identyfikacji punktów końcowych uwierzytelniania. Źle wdrożony system uwierzytelniania może sprawić, że dowolny użytkownik przejmie tożsamość innego użytkownika. 

**Prawdopodobny wpływ** 

W przypadku złamanego uwierzytelnienia użytkownika atakujący mogą naruszyć uwierzytelnioną sesję lub mechanizm uwierzytelniania i łatwo uzyskać dostęp do poufnych danych. Złośliwi atakujący mogą podszywać się pod osoby upoważnione i podejmować niepożądane działania, w tym całkowite przejęcie konta. 

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i narzędzia Talend API Tester do debugowania na maszynie wirtualnej .
- Bob rozumie, że uwierzytelnianie jest kluczowe i otrzymał zadanie opracowania punktu końcowego API`apirule2/user/login_v`  , który będzie uwierzytelniał na podstawie podanego adresu e-mail i hasła.
- Punkt końcowy zwróci token, który zostanie przekazany jako `Authorization-Token`nagłówek (żądanie GET), aby`apirule2/user/details`  wyświetlić dane konkretnego pracownika. Bobowi udało się utworzyć punkt końcowy logowania, jednak do weryfikacji użytkownika użył jedynie adresu e-mail `user table`i zignorował pole hasła w zapytaniu SQL. Atakujący potrzebuje jedynie adresu e-mail ofiary, aby uzyskać prawidłowy token lub przejąć konto.
-  Na maszynie wirtualnej możesz to sprawdzić, wysyłając  `POST` żądanie,  `http://localhost:80/MHT/apirule2/user/login_v` podając adres e-mail i hasło w parametrach formularza.

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/dedcd5391fc513261706967f2c0e34cf.png)  

- Jak widać, podatny na ataki punkt końcowy otrzymał token, który można przesłać dalej, aby `/apirule2/user/details`uzyskać szczegółowe informacje o użytkowniku.
- Aby rozwiązać ten problem, zaktualizujemy logikę zapytania logowania i będziemy używać zarówno adresu e-mail, jak i hasła do walidacji. Punkt końcowy `/apirule2/user/login_s`jest prawidłowym punktem końcowym, jak pokazano poniżej, który autoryzuje użytkownika na podstawie zarówno hasła, jak i adresu e-mail.

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/44ee6cbacf493eb437c3711ae413965e.png)  

**Środki łagodzące** 

- Zapewnij  użytkownikom końcowym złożone hasła o wyższej entropii .
- Nie ujawniaj poufnych danych uwierzytelniających w żądaniach **GET** i **POST .**
- Włącz silne tokeny internetowe JSON (JWT), nagłówki autoryzacyjne itp.
- Zadbaj o wdrożenie uwierzytelniania wieloskładnikowego (jeśli to możliwe), blokadę kont lub system captcha, aby ograniczyć ryzyko ataków siłowych na konkretnych użytkowników. 
- Upewnij się, że hasła nie są zapisywane w bazie danych w postaci zwykłego tekstu, aby zapobiec przejęciu konta przez atakującego.

## Luka III – Nadmierne ujawnienie danych
**Jak to się dzieje?**

Nadmierne ujawnianie danych występuje, gdy aplikacje mają tendencję do ujawniania użytkownikowi **zbyt wielu informacji za pośrednictwem odpowiedzi** API .  Twórcy aplikacji mają tendencję do ujawniania wszystkich właściwości obiektów (biorąc pod uwagę implementacje generyczne), nie uwzględniając ich poziomu wrażliwości. Zadanie filtrowania pozostawiają programistom front-end, zanim zostaną one wyświetlone użytkownikowi. W rezultacie atakujący może przechwycić odpowiedź za pośrednictwem API i szybko wyodrębnić pożądane poufne dane.  Narzędzia do wykrywania w czasie wykonywania lub ogólne narzędzia do skanowania bezpieczeństwa mogą ostrzegać o tego typu podatnościach. Nie są one jednak w stanie odróżnić legalnych danych, które powinny zostać zwrócone, od danych wrażliwych. 

**Prawdopodobny wpływ** 

Osoba atakująca może skutecznie przechwycić ruch i łatwo uzyskać dostęp do poufnych danych, w tym danych osobowych, takich jak numery kont, numery telefonów, tokeny dostępu i wiele innych. Zazwyczaj interfejsy API odpowiadają poufnymi tokenami, które mogą być później wykorzystywane do wykonywania połączeń z innymi krytycznymi punktami końcowymi.

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i narzędzia Talend API Tester do debugowania na maszynie wirtualnej .  
    
- Firma MHT uruchomiła portal internetowy oparty na komentarzach, który gromadzi komentarze użytkowników i zapisuje je w bazie danych wraz z innymi informacjami, takimi jak lokalizacja, dane urządzenia itp., aby ulepszyć doświadczenia użytkowników.  
    
- Bobowi powierzono zadanie stworzenia punktu końcowego do wyświetlania komentarzy użytkowników na głównej stronie internetowej firmy. Stworzył punkt końcowy `apirule3/comment_v/{id}` , który pobiera z bazy danych wszystkie dostępne informacje dotyczące komentarza. Bob założył, że programista front-end będzie filtrował informacje podczas wyświetlania ich na głównej stronie internetowej firmy.

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/6733955d8ce9471ce57924fb77a8caf6.png)  

- W czym tkwi problem? API wysyła więcej danych niż potrzeba. Zamiast polegać na inżynierze front-end, który filtruje dane, z bazy danych muszą być wysyłane tylko istotne dane.
- Bob zdał sobie sprawę ze swojego błędu, zaktualizował punkt końcowy i utworzył prawidłowy punkt końcowy `/apirule3/comment_s/{id}` , który zwraca deweloperowi tylko niezbędne informacje (jak pokazano poniżej).

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/23e044cc3efe648691292fac6f6e4acf.png)  

**Środki łagodzące** 

- Nigdy nie powierzaj zadań filtrowania poufnych danych programistom front-end. 
- Należy zapewnić regularny przegląd odpowiedzi z interfejsu API , aby mieć pewność, że zwracane dane są prawidłowe, oraz sprawdzać, czy nie stwarzają one zagrożenia bezpieczeństwa. 
- Unikaj stosowania metod ogólnych, takich jak `to_string() and to_json()`. 
- Przeprowadź testy punktów końcowych interfejsu API za pomocą różnych przypadków testowych i zweryfikuj za pomocą testów automatycznych i ręcznych, czy interfejs API nie wycieka dodatkowych danych.

## Luka IV — brak zasobów i ograniczenie przepustowości

**Jak to się dzieje?**

Brak zasobów i limity przepustowości oznaczają, że **interfejsy API nie wymuszają żadnych ograniczeń** częstotliwości żądań klientów dotyczących zasobów ani rozmiaru plików, co negatywnie wpływa na wydajność serwera API i prowadzi do ataków DoS (Denial of Service) lub braku dostępności usługi. Rozważmy scenariusz, w którym limit API nie jest egzekwowany, co pozwala użytkownikowi (zazwyczaj intruzowi) na jednoczesne przesyłanie plików o rozmiarze kilku GB lub wykonywanie dowolnej liczby żądań na sekundę. Takie punkty końcowe interfejsu API będą skutkować nadmiernym wykorzystaniem zasobów sieciowych, pamięci masowej, obliczeniowych itp.

Obecnie atakujący stosują tego typu ataki, aby **zapewnić brak dostępności usług dla organizacji** , co z kolei niszczy reputację marki poprzez dłuższe przestoje. Prostym przykładem jest nieprzestrzeganie systemu Captcha w formularzu logowania, co pozwala każdemu na wykonywanie licznych zapytań do bazy danych za pomocą niewielkiego skryptu napisanego w Pythonie.

**Prawdopodobny wpływ** 

Atak ten jest skierowany przede wszystkim na  zasady bezpieczeństwa dotyczące **dostępności** . Może jednak zaszkodzić reputacji marki i spowodować straty finansowe.  

Przykład praktyczny

- Kontynuuj korzystanie z przeglądarki Chrome i narzędzia Talend API Tester do debugowania na maszynie wirtualnej .  
    
- Firma MHT zakupiła plan marketingu e-mailowego (20 tys. e-maili miesięcznie) w celu wysyłania materiałów marketingowych, wiadomości e-mail z prośbą o odzyskanie hasła itp. Bob zdał sobie sprawę, że udało mu się opracować interfejs API logowania , ale musi istnieć opcja „Zapomniałem hasła”, która umożliwia odzyskanie konta.  
    
- Zaczął tworzyć punkt końcowy `/apirule4/sendOTP_v`, który będzie wysyłał 4-cyfrowy kod numeryczny na adres e-mail użytkownika. Uwierzytelniony użytkownik będzie używał tego jednorazowego hasła (OTP) do odzyskania konta.

![Obraz scenariusza podatnego na zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e893ab4958ff54d17bedf53a0e22d772.png)  

- Na czym polega problem? Bob nie włączył żadnego limitu przepustowości w punkcie końcowym. Osoba atakująca może napisać krótki skrypt i zaatakować punkt końcowy metodą brute force, wysyłając wiele e-maili w ciągu kilku sekund i wykorzystując niedawno zakupiony plan marketingu e-mailowego firmy (strata finansowa).
- W końcu Bob wpadł na inteligentne rozwiązanie `(/apirule4/sendOTP_s)`i włączył ograniczenie przepustowości, dzięki któremu użytkownik musi odczekać 2 minuty, aby ponownie poprosić o token OTP.

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/a47bc005c405264850984ca7fb19b24b.gif)

**Środki łagodzące** 

- Upewnij się, że używasz captcha, aby uniknąć żądań ze strony automatycznych skryptów i botów.
- Zapewnij wdrożenie limitu, tzn. tego, jak często klient może wywołać API w określonym czasie, i natychmiast wyślij powiadomienie w przypadku przekroczenia limitu. 
- Upewnij się, że zdefiniowano maksymalny rozmiar danych dla wszystkich parametrów i ładunków, tj. maksymalną długość ciągu i maksymalną liczbę elementów tablicy.

## Luka V — Autoryzacja poziomu uszkodzonej funkcji

**Jak to się dzieje?**

Autoryzacja na poziomie funkcji z przerwami (Broken Function Level Authorization) odzwierciedla scenariusz, w którym użytkownik o niskich uprawnieniach (np. dział sprzedaży) omija kontrole systemu i uzyskuje dostęp do **poufnych danych, podszywając się pod użytkownika o wysokich uprawnieniach (administratora)** . Rozważmy scenariusz ze złożonymi zasadami kontroli dostępu z różnymi hierarchiami, rolami i grupami oraz niejasnym podziałem między funkcjami zwykłymi i administracyjnymi, co prowadzi do poważnych luk w autoryzacji. Wykorzystując te problemy, intruzi mogą łatwo uzyskać dostęp do nieautoryzowanych zasobów innego użytkownika lub, co najniebezpieczniejsze, do funkcji administracyjnych.   

Autoryzacja na poziomie uszkodzonej funkcji odzwierciedla uprawnienia IDOR , dzięki którym użytkownik, najprawdopodobniej intruz, może wykonywać zadania na poziomie administracyjnym. Interfejsy API ze złożonymi rolami i uprawnieniami użytkowników, które mogą obejmować całą hierarchię, są bardziej podatne na ten atak. 

**Prawdopodobny wpływ** 

Atak ten jest skierowany przede wszystkim na zasady bezpieczeństwa dotyczące autoryzacji i niezaprzeczalności. Złamana autoryzacja poziomu funkcjonalnego może skłonić intruza do podszywania się pod autoryzowanego użytkownika i umożliwienia mu uzyskania uprawnień administracyjnych do wykonywania poufnych zadań. 

Przykład praktyczny  

- Kontynuuj korzystanie z przeglądarki Chrome i narzędzia Talend API Tester do debugowania na maszynie wirtualnej .  
    
- Bobowi powierzono kolejne zadanie polegające na stworzeniu panelu administracyjnego dla kadry kierowniczej firmy, aby mogli oni przeglądać dane wszystkich pracowników i wykonywać określone zadania.  
    
- Bob opracował punkt końcowy `/apirule5/users_v`do pobierania danych wszystkich pracowników z bazy danych. Aby zwiększyć bezpieczeństwo, dodał kolejną warstwę zabezpieczeń, dodając specjalny nagłówek `isAdmin`do każdego żądania. API pobiera informacje o pracownikach z bazy danych tylko wtedy, gdy są `isAdmin=1`one `Authorization-Token`poprawne. Token autoryzacyjny dla użytkownika Alice z działu HR to `YWxpY2U6dGVzdCFAISM6Nzg5Nzg=` .

![Obraz przedstawiający scenariusz zagrożenia](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/4fb8a31217d2d1af51cad8cbdc318754.png)  

- Możemy zobaczyć, że Alicja nie jest użytkownikiem z uprawnieniami administratora (dział HR), ale może zobaczyć dane wszystkich pracowników, ustawiając niestandardowe żądania do punktu końcowego za pomocą `isAdmin value = 1`. 
- Problem można rozwiązać programowo, wdrażając poprawne reguły autoryzacji i sprawdzając role funkcjonalne każdego użytkownika w bazie danych podczas wykonywania zapytania. Bob zaimplementował kolejny punkt końcowy   `/apirule5/users_s`, który weryfikuje rolę każdego użytkownika i wyświetla dane pracowników tylko wtedy, gdy rolą jest administrator.

![Obraz dla bezpiecznego scenariusza](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/5a708a5bc9daad5002e4824a0eda5511.gif)  

**Środki łagodzące** 

- Zadbaj o właściwy projekt i testowanie wszystkich systemów autoryzacji i domyślnie zablokuj wszelki dostęp. 
- Upewnij się, że operacje są dozwolone wyłącznie użytkownikom należącym do autoryzowanej grupy. 
- Należy sprawdzić punkty końcowe interfejsu API pod kątem błędów dotyczących autoryzacji na poziomie funkcjonalnym, a także pamiętać o logice biznesowej hierarchii aplikacji i grup.
