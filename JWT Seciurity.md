
W tym pokoju dowiesz się oJSONTokeny internetowe (JWT) i związane z nimi bezpieczeństwo. Wraz z rozwojem interfejsów API, uwierzytelnianie oparte na tokenach zyskało na popularności, a JWT pozostają jedną z najpopularniejszych implementacji. Jednak w przypadku JWT, zapewnienie bezpieczeństwa implementacji jest niezwykle ważne. Niezabezpieczone implementacje mogą prowadzić do poważnych luk w zabezpieczeniach, a atakujący mogą podrabiać tokeny i przejmować sesje użytkowników!  

Wymagania wstępne

- [Wprowadzenie do hakowania stron internetowych](https://tryhackme.com/module/intro-to-web-hacking)
- [Wyliczanie i siłowe atakowanie](https://tryhackme.com/r/room/enumerationbruteforce)
- [Zarządzanie sesjami](https://tryhackme.com/r/room/sessionmanagement)  
    

Cele edukacyjne

- Dowiedz się więcej o uwierzytelnianiu opartym na tokenach
- Dowiedz się więcej o tokenach internetowych JSON (JWT)
- Dowiedz się, dlaczego tokeny JWT są popularne
- Dowiedz się więcej o kwestiach bezpieczeństwa związanych z korzystaniem z tokenów JWT
- Dowiedz się, jak atakować podatne implementacje JWT


Rozwój interfejsów API

Interfejsy programowania aplikacji, w skrócie API, stały się dziś niezwykle popularne. Jednym z głównych powodów tego boomu jest możliwość tworzenia pojedynczychAPIktóre mogą obsługiwać jednocześnie kilka różnych interfejsów, takich jak aplikacja internetowa i aplikacja mobilna. Pozwala to na scentralizowanie i ponowne wykorzystanie tej samej logiki po stronie serwera dla wszystkich interfejsów. Z punktu widzenia bezpieczeństwa jest to również zazwyczaj korzystne, ponieważ oznacza, że ​​możemy zaimplementować zabezpieczenia po stronie serwera w jednym interfejsie API, co chroni nasz serwer niezależnie od używanego interfejsu.

Jednak wraz z rozwojem interfejsów API pojawiły się również nowe metody zarządzania sesjami. Ponieważ pliki cookie są zazwyczaj powiązane z aplikacjami internetowymi używanymi za pośrednictwem przeglądarki, uwierzytelnianie oparte na plikach cookie w interfejsach API zazwyczaj nie działa tak dobrze, ponieważ rozwiązanie to nie jest wtedy uniwersalne dla innych interfejsów. W tym miejscu z pomocą przychodzi zarządzanie sesjami oparte na tokenach.  

Zarządzanie sesjami oparte na tokenach

Zarządzanie sesjami oparte na tokenach to stosunkowo nowa koncepcja. Zamiast korzystać z funkcji automatycznego zarządzania plikami cookie przeglądarki, opiera się ono na kodzie po stronie klienta. Po uwierzytelnieniu aplikacja internetowa dostarcza token w treści żądania. Za pomocą kodu JavaScript po stronie klienta token ten jest następnie przechowywany w pamięci lokalnej przeglądarki.

Gdy wysyłane jest nowe żądanie, kod JavaScript musi załadować token z pamięci masowej i dołączyć go jako nagłówek. Jednym z najpopularniejszych typów tokenów jestJSONTokeny sieciowe (JWT), które są przesyłane przez nagłówek `Authorization: Bearer`. Ponieważ jednak nie korzystamy z wbudowanych funkcji zarządzania plikami cookie przeglądarki, mamy do czynienia z Dzikim Zachodem, gdzie wszystko jest dozwolone. Chociaż istnieją standardy, nic nie zmusza nikogo do ich przestrzegania. Tokeny takie jak JWT to sposób na standaryzację zarządzania sesjami opartego na tokenach.

Projekt API

W tym pokoju przeprowadzisz eksploatację kilku interfejsów API. Interfejsy API można dokumentować na kilka różnych sposobów. Jedną z popularnych metod jest utworzenie pliku [Postman.(otwiera się w nowej karcie)](https://www.postman.com/)projekt lub [Swagger(otwiera się w nowej karcie)](https://swagger.io/)Plik. Chociaż zachęcamy do eksperymentowania z tymi rozwiązaniami, wymagają one posiadania konta, czego nie wymuszamy w tym pokoju. Zamiast tego, poniżej znajduje się uproszczone wyjaśnienie API. API pozostaje spójne dla wszystkich przykładów z wyjątkiem ostatniego, który zawiera dodatkowe funkcje. Podczas pracy nad ćwiczeniami, zapoznaj się z tą sekcją, aby uzyskać wskazówki. API zostało opracowane w Python Flask. W związku z tym przykłady kodowania będą napisane w Pythonie.  

**Punkty końcowe API**  

Projekt API ma pojedynczy punkt końcowy API, mianowicie [http://MACHINE_IP/api/v1.0/exampleX(otwiera się w nowej karcie)](http://machine_ip/api/v1.0/exampleX). `X`Zastępuje się numerem przykładu. Ten punkt końcowy uzyskuje dostęp do dwóchHTTPmetody:

- **POST** : Aby uwierzytelnić i odebrać JWT, należy wysłać żądanie POST z poświadczeniami podanymi w formacie JSON.
- **GET** : Aby uzyskać szczegółowe informacje o użytkowniku i ostatecznie wykonać eskalację uprawnień w celu odzyskania flagi zadania.

**Poświadczenia API**

Aby uwierzytelnić się w API, należy wysłać treść JSON zawierającą dane uwierzytelniające w następujący sposób:

- **nazwa użytkownika** : użytkownik
- **hasło** : hasłoX

Należy `X`zastąpić numerem przykładu.

**Przykłady API**

Poniżej znajdują się dwa żądania cURL, których można użyć do połączenia z API. W celu uwierzytelnienia można wysłać następujące żądanie cURL:

`curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "passwordX" }' http://MACHINE_IP/api/v1.0/exampleX`  

W celu weryfikacji użytkownika można wysłać następujące żądanie cURL:

`curl -H 'Authorization: Bearer [JWT token]' http://MACHINE_IP/api/v1.0/example2?username=Y`

Komponent `[JWT token]`musi zostać zastąpiony tokenem JWT otrzymanym w pierwszym żądaniu. W tym przypadku `Y`może to być albo `user`lub `admin`, w zależności od uprawnień.  

**Uprawnienia API**

Głównym celem w każdym przykładzie jest uzyskanie uprawnień administratora i ich weryfikacja. Po uzyskaniu prawidłowego tokena JWT, w którym parametr „admin” jest ustawiony na 1, można zażądać danych użytkownika o uprawnieniach administratora. Spowoduje to zwrócenie flagi. Proces zostanie pokazany w pierwszym przykładzie, ale konieczne będzie skopiowanie kroków dla pierwszego.odpoczynekprzykładów.

Uruchom maszynę

Teraz, gdy rozumiesz strukturę API, czas zacząć działać. Uruchom maszynę, naciskając przycisk „ **Start Lab Machine”** w prawym rogu. Możesz uzyskać dostęp doMaszyna wirtualnaużywając AttackBox lub twojegoVPNPołączenie. Podczas uruchamiania komputera przyjrzyjmy się bliżej działaniu tokenów JWT.

Tokeny JWT to niezależne tokeny, których można używać do bezpiecznego przesyłania informacji o sesjach. To [otwarty standard.(otwiera się w nowej karcie)](https://tools.ietf.org/html/rfc7519), dostarczając informacji każdemu programiście lub twórcy bibliotek, który chce korzystać z tokenów JWT. Struktura tokenu JWT jest pokazana na poniższej animacji:

Struktura JWT

Token JWT składa się z trzech komponentów, z których każdy jest zakodowany w formacie Base64Url i rozdzielony kropkami:

- **Nagłówek** – nagłówek zwykle wskazuje typ tokena (JWT) oraz użyty algorytm podpisywania.
- **Ładunek (payload)** – Ładunek (payload) to treść tokena zawierająca oświadczenia. Oświadczenie (claim) to informacja dostarczona dla konkretnego podmiotu. W tokenach JWT występują zarejestrowane oświadczenia, które są oświadczeniami predefiniowanymi przez standard JWT oraz oświadczeniami publicznymi i prywatnymi. Oświadczenia publiczne i prywatne to te, które są definiowane przez dewelopera. Warto znać różnicę między oświadczeniami publicznymi i prywatnymi, ale nie ze względów bezpieczeństwa, dlatego nie będziemy się tym zajmować w tym pomieszczeniu.
- **Podpis** – Podpis to część tokena, która zapewnia metodę weryfikacji autentyczności tokena. Podpis jest tworzony za pomocą algorytmu określonego w nagłówku tokena JWT. Przyjrzyjmy się bliżej głównym algorytmom podpisywania.

Algorytmy podpisywania

Mimo że w standardzie JWT zdefiniowano kilka różnych algorytmów, nas interesują tylko trzy główne:

- **Brak** – algorytm „Brak” oznacza, że ​​żaden algorytm nie jest używany do podpisu. W praktyce jest to token JWT bez podpisu, co oznacza, że ​​weryfikacji oświadczeń zawartych w tokenie JWT nie można zweryfikować za pomocą podpisu.
- **Symetryczne podpisywanie** – Algorytm symetrycznego podpisywania, taki jak HS256, tworzy podpis poprzez dodanie tajnej wartości do nagłówka i treści tokena JWT przed wygenerowaniem wartości skrótu. Weryfikacja podpisu może zostać przeprowadzona przez dowolny system znający tajny klucz.
- **Podpisywanie asymetryczne** – Algorytm podpisywania asymetrycznego, taki jak RS256, tworzy podpis za pomocą klucza prywatnego do podpisania nagłówka i treści tokena JWT. Odbywa się to poprzez wygenerowanie skrótu, a następnie zaszyfrowanie go kluczem prywatnym. Weryfikacja podpisu może zostać przeprowadzona przez dowolny system, który zna klucz publiczny powiązany z kluczem prywatnym użytym do utworzenia podpisu.

Bezpieczeństwo w podpisie

Tokeny JWT można szyfrować (nazywane JWE), ale kluczowa moc tokenów JWT tkwi w podpisie. Po podpisaniu token JWT można go wysłać do klienta, który może go używać w dowolnym momencie. Możemy mieć scentralizowany serwer uwierzytelniania, który tworzy tokeny JWT używane w wielu aplikacjach. Każda aplikacja może następnie zweryfikować podpis tokena JWT; jeśli zostanie on zweryfikowany, oświadczenia zawarte w tokenach JWT będą wiarygodne i będą mogły zostać wykorzystane.


Ujawnianie poufnych informacji  

Pierwszym powszechnym problemem, jaki omówimy, jest ujawnienie poufnych informacji w JWT.

Typowym podejściem do zarządzania sesjami opartym na plikach cookie jest wykorzystanie sesji po stronie serwera do przechowywania kilku parametrów.PHPNa przykład, można użyć $SESSION['var']=data do przechowywania wartości powiązanej z sesją użytkownika. Wartości te nie są ujawniane po stronie klienta i dlatego można je odzyskać tylko po stronie serwera. Jednak w przypadku tokenów, deklaracje są ujawniane, gdy cały JWT jest wysyłany po stronie klienta. Jeśli zastosuje się tę samą praktykę programistyczną, możliwe jest ujawnienie poufnych informacji. Oto kilka przykładów z rzeczywistych aplikacji:

- Ujawnienie danych uwierzytelniających za pomocą skrótu hasła lub, co gorsza, przesłanie hasła w postaci jawnego tekstu jako roszczenia.
- Ujawnienie wewnętrznych informacji sieciowych, takich jak prywatny adres IP lub nazwa hosta serwera uwierzytelniającego.

**Przykład praktyczny 1  
**

Przyjrzyjmy się praktycznemu przykładowi. Uwierzytelnijmy się w naszymAPIużywając następującego żądania cURL:

`curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "password1" }' http://MACHINE_IP/api/v1.0/example1`  

To zapewni Ci token JWT. Po odzyskaniu, zdekoduj treść tokenu JWT, aby uzyskać poufne informacje. Możesz zdekodować treść ręcznie lub skorzystać ze strony internetowej, takiej jak [JWT.io.(otwiera się w nowej karcie)](https://jwt.io/)dla tego procesu.

**Błąd rozwoju**

W tym przykładzie do roszczenia dodano poufne informacje, jak pokazano poniżej:

```python
payload = {
    "username" : username,
    "password" : password,
    "admin" : 0,
    "flag" : "[redacted]"
}

access_token = jwt.encode(payload, self.secret, algorithm="HS256")
```

**Naprawa**  

Wartości takie jak hasło czy flaga nie powinny być dodawane jako oświadczenia, ponieważ JWT będzie wysyłany po stronie klienta. Zamiast tego wartości te powinny być bezpiecznie przechowywane po stronie serwera w zapleczu. W razie potrzeby nazwę użytkownika można odczytać ze zweryfikowanego JWT i użyć jej do wyszukania tych wartości, jak pokazano w poniższym przykładzie:

```python
payload = jwt.decode(token, self.secret, algorithms="HS256")

username = payload['username']
flag = self.db_lookup(username, "flag")
```


Drugim częstym błędem w przypadku tokenów JWT jest nieprawidłowa weryfikacja podpisu. Jeśli podpis nie zostanie poprawnie zweryfikowany, atakujący może sfałszować prawidłowy token JWT, aby uzyskać dostęp do konta innego użytkownika. Przyjrzyjmy się typowym problemom z weryfikacją podpisu.

Brak weryfikacji podpisu

Pierwszym problemem związanym z walidacją podpisu jest brak walidacji. Jeśli serwer nie zweryfikuje podpisu tokena JWT, możliwe jest zmodyfikowanie deklaracji w tokenach JWT zgodnie z preferencjami. Chociaż rzadko spotyka się interfejsy API, w których nie przeprowadza się walidacji podpisu, walidacja podpisu mogła zostać pominięta w jednym punkcie końcowym. API w zależności od wrażliwości punktu końcowego może to mieć znaczący wpływ na działalność biznesową.

**Przykład praktyczny 2**

Uwierzytelnijmy się w API:

`curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "password2" }' http://MACHINE_IP/api/v1.0/example2`

Po uwierzytelnieniu zweryfikujmy naszego użytkownika:

`curl -H 'Authorization: Bearer [JWT Token]' http://MACHINE_IP/api/v1.0/example2?username=user`

Spróbujmy jednak zweryfikować naszego użytkownika bez podpisu, usuńmy trzecią część JWT (pozostawiając tylko kropkę) i ponownie wyślijmy żądanie. Zobaczysz, że weryfikacja nadal działa! Oznacza to, że podpis nie jest weryfikowany. Zmień deklarację administratora w treści na „be” `1`i spróbuj zweryfikować się jako użytkownik z uprawnieniami administratora, aby pobrać flagę.

**Błąd rozwoju**

W tym przykładzie podpis nie jest weryfikowany, jak pokazano poniżej:

```python
payload = jwt.decode(token, options={'verify_signature': False})
```

Choć rzadko się to zdarza w przypadku standardowych interfejsów API, często zdarza się to w interfejsach API typu serwer-serwer. W przypadkach, gdy atakujący ma bezpośredni dostęp do serwera zaplecza, tokeny JWT mogą zostać sfałszowane.  

**Naprawa**

JWT zawsze powinien być weryfikowany lub do komunikacji między serwerami należy stosować dodatkowe czynniki uwierzytelniające, takie jak certyfikaty. JWT można zweryfikować, podając klucz tajny (lub publiczny), jak pokazano w poniższym przykładzie:

```python
payload = jwt.decode(token, self.secret, algorithms="HS256")
```

Obniżenie do Brak

Innym częstym problemem jest obniżenie wersji algorytmu podpisu. JWT obsługują `None`algorytm podpisu, co w praktyce oznacza, że ​​żaden podpis nie jest z nim używany. Choć może to brzmieć niedorzecznie, idea stojąca za tym standardem dotyczyła komunikacji między serwerami, gdzie podpis JWT był weryfikowany w procesie nadrzędnym. W związku z tym drugi serwer nie byłby zobowiązany do weryfikacji podpisu. Załóżmy jednak, że programiści nie blokują algorytmu podpisu lub przynajmniej go zablokują `None`. W takim przypadku można po prostu zmienić algorytm określony w JWT na `None`, co spowoduje, że biblioteka używana do weryfikacji podpisu zawsze będzie zwracać wartość true, umożliwiając tym samym ponowne fałszowanie roszczeń w tokenie.

**Przykład praktyczny 3  
**

Uwierzytelnij się w API, aby otrzymać JWT, a następnie zweryfikuj użytkownika. Aby przeprowadzić ten atak, musisz ręcznie zmienić deklarację `alg`w nagłówku na `None`. Możesz użyć [CyberChef.(otwiera się w nowej karcie)](https://gchq.github.io/CyberChef/)W tym celu należy skorzystać z opcji URL-Encoded Base64. Prześlij ponownie JWT, aby sprawdzić, czy jest nadal akceptowany, nawet jeśli podpis nie jest już ważny, ponieważ wprowadzono zmiany. Następnie możesz zmodyfikować deklarację, `admin`aby odzyskać flagę.

**Błąd rozwoju**

Choć może się to wydawać tym samym problemem co poprzednio, z perspektywy programistycznej jest to nieco bardziej złożone. Czasami programiści chcą mieć pewność, że ich implementacja akceptuje kilka algorytmów weryfikacji podpisu JWT. Implementacja zazwyczaj odczytuje wówczas nagłówek JWT i analizuje znaleziony algorytm do komponentu weryfikacji podpisu, jak pokazano poniżej:

```python
header = jwt.get_unverified_header(token)

signature_algorithm = header['alg']

payload = jwt.decode(token, self.secret, algorithms=signature_algorithm)
```

Jednakże, gdy aktor zagrożenia jest określony `None`jako algorytm, weryfikacja podpisu jest pomijana. [Pyjwt(otwiera się w nowej karcie)](https://pyjwt.readthedocs.io/en/stable/)Biblioteka JWT używana w tym pokoju zaimplementowała kod bezpieczeństwa, aby zapobiec temu problemowi. Jeśli po wybraniu algorytmu „Brak” zostanie określony klucz tajny, zgłaszany jest wyjątek.

**Naprawa**

Jeżeli mają być obsługiwane różne algorytmy podpisu, należy przekazać je do funkcji dekodowania w postaci listy tablicowej, jak pokazano poniżej:

```python
payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512"])

username = payload['username']
flag = self.db_lookup(username, "flag")
```

Słabe sekrety symetryczne

W przypadku użycia symetrycznego algorytmu podpisywania, bezpieczeństwo tokena JWT zależy od siły i entropii użytego sekretu. W przypadku użycia słabego sekretu możliwe jest przeprowadzenie łamania offline w celu jego odzyskania. Po ustaleniu wartości sekretu można ponownie zmodyfikować deklaracje w tokenie JWT i ponownie obliczyć prawidłowy podpis, używając tego sekretu.

**Przykład praktyczny 4  
**

W tym przykładzie do wygenerowania tokenu JWT użyto słabego klucza tajnego. Po otrzymaniu tokena JWT masz kilka możliwości złamania klucza tajnego. W naszym przykładzie omówimy użycie [Hashcata.(otwiera się w nowej karcie)](https://hashcat.net/hashcat/)Aby złamać sekret JWT. Możesz również skorzystać z innych rozwiązań, takich jak [John(otwiera się w nowej karcie)](https://www.openwall.com/john/)Również. Aby złamać sekret, możesz wykonać następujące kroki:

1. Zapisz JWT w pliku tekstowym o nazwie jwt.txt.
2. Pobierz listę popularnych sekretów JWT. Dla tego pokoju możesz użyć `wget https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list` tej listy.
3. Użyj Hashcata, aby złamać sekret`hashcat -m 16500 -a 0 jwt.txt jwt.secrets.list`

Gdy już poznasz sekret, możesz wykuć nowy token administratora i odzyskać flagę!

**Błąd rozwoju**

Problem występuje, gdy używany jest słaby klucz tajny JWT. Często zdarza się to, gdy programiści się spieszą lub kopiują kod z przykładów.

**Naprawa**

Należy wybrać bezpieczną wartość tajną. Ponieważ wartość ta będzie wykorzystywana w oprogramowaniu, a nie przez ludzi, należy użyć długiego, losowego ciągu znaków.

Zamieszanie z algorytmem sygnaturowym

Ostatnim częstym problemem związanym z walidacją podpisów jest możliwość przeprowadzenia ataku polegającego na pomyłce algorytmu. Jest on podobny do `None`ataku downgrade, jednak występuje w przypadku pomylenia algorytmów podpisywania symetrycznego i asymetrycznego. Jeśli używany jest asymetryczny algorytm podpisywania, na przykład RS256, możliwe jest obniżenie jego wersji do HS256. W takich przypadkach niektóre biblioteki domyślnie wracają do używania klucza publicznego jako klucza tajnego dla algorytmu podpisywania symetrycznego. Ponieważ klucz publiczny jest znany, można sfałszować prawidłowy podpis, używając algorytmu HS256 w połączeniu z kluczem publicznym.

**Przykład praktyczny 5  
**

Jest to podobne do przykładu 3. Z tą różnicą, że tym razem algorytm „None” jest niedozwolony. Jednak po uwierzytelnieniu w tym przykładzie otrzymasz również klucz publiczny. Ponieważ klucz publiczny nie jest uważany za poufny, często można go znaleźć. Czasami klucz publiczny jest nawet osadzony jako deklaracja w tokenie JWT. W tym przykładzie musisz obniżyć wersję algorytmu do HS256, a następnie użyć klucza publicznego jako klucza tajnego do podpisania tokenu JWT. Możesz skorzystać z poniższego skryptu, aby ułatwić sobie sfałszowanie tego tokenu JWT:

```python
import jwt

# Pyjwt refuses to use an asymmetric key as an HMAC secret. The line below replaces
# that check at runtime, so that no library files have to be edited.
jwt.algorithms.HMACAlgorithm.prepare_key = lambda self, key: key.encode() if isinstance(key, str) else key

public_key = "ADD_KEY_HERE"

payload = {
    'username' : 'user',
    'admin' : 0
}

access_token = jwt.encode(payload, public_key, algorithm="HS256")
print (access_token)
```

Uwaga: Zalecamy użycie AttackBoxa w tym praktycznym przykładzie, ponieważ Pyjwt jest już zainstalowany. Zapisz skrypt jako `forge.py`i uruchom go za pomocą `/usr/bin/python3 forge.py`. Domyślnie `python3`w AttackBoxie znajduje się osobna instalacja Pyenv, która nie zawiera Pyjwt, dlatego należy użyć pełnej `/usr/bin/python3`ścieżki. Jeśli korzystasz z własnej maszyny wirtualnej, może być konieczne `pip3 install pyjwt`wcześniejsze zainstalowanie Pyjwt(), a następnie uruchomienie skryptu za pomocą `python3 forge.py`. Wydano poprawkę na tę lukę, dlatego Pyjwt zgłasza błąd, `InvalidKeyError`gdy klucz asymetryczny jest używany jako sekret HMAC. Trzeci wiersz skryptu wyłącza to sprawdzanie tylko w bieżącym uruchomieniu, co oznacza, że ​​sama biblioteka pozostaje nietknięta, a skrypt działa niezależnie od zainstalowanej wersji Pyjwt. Łatwiejszą metodą, jeśli wolisz w ogóle nie uruchamiać skryptu, jest skorzystanie z [jwt.io.(otwiera się w nowej karcie)](https://jwt.io/). Po sprawdzeniu, czy wszystko działa, możesz zmienić roszczenia, aby nadać sobie uprawnienia administratora i odzyskać flagę, ustawiając wartości `admin`na `1`i `username`na `admin`.

**Błąd rozwoju**

Błąd w tym przykładzie jest podobny do błędu w przykładzie 3, ale nieco bardziej złożony. Chociaż algorytm None jest niedozwolony, kluczowy problem wynika z faktu, że dozwolone są zarówno algorytmy sygnatury symetrycznej, jak i asymetrycznej, jak pokazano w poniższym przykładzie:

```python
payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"])
```

Należy zachować ostrożność i nigdy nie mieszać ze sobą algorytmów podpisu, ponieważ tajny parametr funkcji dekodowania może zostać pomylony z kluczem tajnym lub publicznym.

**Naprawa**

Choć oba typy algorytmów podpisu mogą być dozwolone, potrzeba nieco więcej logiki, aby uniknąć pomyłek, jak pokazano w poniższym przykładzie:

```python
header = jwt.get_unverified_header(token)

algorithm = header['alg']
payload = ""

if "RS" in algorithm:
    payload = jwt.decode(token, self.public_key, algorithms=["RS256", "RS384", "RS512"])
elif "HS" in algorithm:
    payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512"])

username = payload['username']
flag = self.db_lookup(username, "flag")
```



Czas życia tokena

Przed weryfikacją podpisu tokena należy obliczyć jego okres ważności, aby upewnić się, że nie wygasł. Zazwyczaj odbywa się to poprzez odczytanie expinformacji o czasie ważności tokena i obliczenie, czy token jest nadal ważny.

Częstym problemem jest to, że jeśli exp wartość jest zbyt duża (lub w ogóle nie jest ustawiona), token będzie ważny zbyt długo, a nawet może nigdy nie wygasnąć. W przypadku plików cookie, plik cookie może wygasnąć po stronie serwera. Jednak tokeny JWT nie mają wbudowanej tej funkcji. Aby wygasić token przed upływem terminu exp, musimy utworzyć listę blokowanych tokenów, co zaburza model zdecentralizowanych aplikacji korzystających z tego samego serwera uwierzytelniania. Dlatego należy starannie dobrać expwartość, biorąc pod uwagę funkcjonalność aplikacji. Na przykład, expprawdopodobnie używana jest inna wartość między serwerem pocztowym a aplikacją bankową.

Innym podejściem jest użycie tokenów odświeżających. Jeśli zamierzasz testować API korzystające z tokenów JWT, zalecamy zapoznanie się z nimi.

Przykład praktyczny 6

W tym przykładzie implementacja JWT nie określiła wartości exp, co oznacza, że ​​tokeny są trwale trwałe. Użyj poniższego tokena, aby odzyskać flagę:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.ko7EQiATQQzrQPwRO8ZTY37pQWGLPZWEvdWH0tVDNPU

Błąd rozwoju

Jak wspomniano powyżej, token JWT nie ma expwartości, co oznacza, że ​​będzie trwały. W przypadku expbraku deklaracji, większość bibliotek tokenu JWT zaakceptuje token jako ważny, jeśli podpis zostanie zweryfikowany.

Naprawa

Do deklaracji należy dodać wartość exp. Po jej dodaniu większość bibliotek uwzględnia weryfikację czasu wygaśnięcia tokena JWT w procesie sprawdzania poprawności. Można to zrobić, jak pokazano w poniższym przykładzie:


lifetime = datetime.datetime.now() + datetime.timedelta(minutes=5)

payload = {
    'username' : username,
    'admin' : 0,
    'exp' : lifetime
}

access_token = jwt.encode(payload, self.secret, algorithm="HS256")




Ostatnim częstym błędem konfiguracyjnym, który omówimy, jest błąd konfiguracji Cross-Service. Jak wspomniano wcześniej, tokeny JWT są często używane w systemach ze scentralizowanym systemem uwierzytelniania obsługującym wiele aplikacji. Jednak w niektórych przypadkach możemy chcieć ograniczyć dostęp do aplikacji za pomocą tokena JWT, zwłaszcza gdy istnieją deklaracje, które powinny obowiązywać tylko dla określonych aplikacji. Można to zrobić za pomocą deklaracji „audience”. Jeśli jednak deklaracja „audience” nie zostanie poprawnie egzekwowana, może zostać przeprowadzony atak Cross-Service Relay w celu przeprowadzenia ataku z eskalacją uprawnień.

Roszczenie publiczności

Tokeny JWT mogą mieć deklarację odbiorców. W przypadkach, gdy jeden system uwierzytelniania obsługuje wiele aplikacji, deklaracja odbiorców może wskazywać, dla której aplikacji przeznaczony jest token JWT. Jednak egzekwowanie tej deklaracji odbiorców musi odbywać się w samej aplikacji, a nie na serwerze uwierzytelniania. Jeśli deklaracja ta nie zostanie zweryfikowana, ponieważ sam token JWT jest nadal uznawany za ważny na podstawie weryfikacji podpisu, może to mieć niezamierzone konsekwencje.

Przykładem jest sytuacja, gdy użytkownik ma uprawnienia administratora lub wyższą rolę w określonej aplikacji. Token JWT przypisany użytkownikowi zazwyczaj zawiera oświadczenie, które to wskazuje, na przykład "admin" : true. Jednak ten sam użytkownik może nie być administratorem w innej aplikacji obsługiwanej przez ten sam system uwierzytelniania. Jeśli oświadczenie odbiorcy nie zostanie zweryfikowane w tej drugiej aplikacji, która również korzysta z oświadczenia administratora, serwer może błędnie uznać, że użytkownik ma uprawnienia administratora. Nazywa się to atakiem typu Cross-Service Relay, jak pokazano na poniższej animacji:



Przyjrzyjmy się praktycznemu przykładowi.

Przykład praktyczny 7

W tym ostatnim praktycznym przykładzie istnieją dwa punkty końcowe API, mianowicie example7_appAi example7_appB. Możesz użyć tego samego żądania GET, które wysłałeś w poprzednich przykładach, aby odzyskać flagę, ale musisz je skierować do tych punktów końcowych. Ponadto, w celu uwierzytelnienia, musisz teraz również uwzględnić "application" : "appX"wartość danych w żądaniu logowania wysłanym do example7. Wykonaj poniższe kroki, aby wykonać przykład:

Uwierzytelnij się, example7używając następującego segmentu danych: '{ "username" : "user", "password" : "password7", "application" : "appA"}'. Zauważysz, że dodano deklarację grupy odbiorców, ale nie jesteś administratorem.
Używaj tego tokena zarówno w żądaniach administratora, jak i użytkownika, które wysyłasz do [ example7_appAadresu] example7_appB. Zauważysz, że chociaż aplikacja A akceptuje token, nie jesteś administratorem, a aplikacja B nie akceptuje tokena, ponieważ odbiorcy są nieprawidłowi.
Uwierzytelnij się, example7używając następującego segmentu danych: '{ "username" : "user", "password" : "password7", "application" : "appB"}'. Zauważysz, że ponownie dodano deklarację grupy odbiorców, a tym razem jesteś administratorem.
Użyj tego tokena ponownie, aby zweryfikować się w obu aplikacjach i zobacz, co się stanie.
Teraz możesz użyć tego, aby odzyskać swoją flagę.

Błąd rozwoju

Kluczowym problemem jest to, że deklaracja grupy docelowej nie jest weryfikowana w aplikacji AppA. Może to wynikać z wyłączenia weryfikacji deklaracji grupy docelowej lub ustawienia zbyt szerokiego zakresu grupy docelowej.

Naprawa

Deklaracja odbiorców powinna zostać zweryfikowana po zdekodowaniu tokena. Można to zrobić, jak pokazano w poniższym przykładzie:


payload = jwt.decode(token, self.secret, audience=["appA"], algorithms="HS256")
Odpowiedz na poniższe pytania


Wniosek

W tej sali zaprezentowano kilka typowych błędnych konfiguracji i luk w zabezpieczeniach implementacji JWT. Podsumowując, zwróć uwagę na następujące kwestie:

Ponieważ tokeny JWT są wysyłane po stronie klienta i kodowane, w ich żądaniach nie należy przechowywać poufnych informacji.
Bezpieczeństwo tokenu JWT zależy od jego podpisu. Należy zachować ostrożność podczas weryfikacji podpisu, aby upewnić się, że nie ma w nim miejsca na pomyłki ani że nie są używane słabe sekrety.
Tokeny JWT powinny wygasać i mieć rozsądny okres istnienia, aby zapobiec wykorzystywaniu trwałych tokenów JWT przez osoby stwarzające zagrożenie.
WSSO środowiskach, roszczenia odbiorców są kluczowe dla zapewnienia, że ​​JWT konkretnej aplikacji będzie używany tylko w tej aplikacji.
Ponieważ tokeny JWT wykorzystują kryptografię do generowania podpisu, ataki kryptograficzne mogą być również istotne w kontekście wykorzystania tokenów JWT. Zajmiemy się tym tematem nieco szerzej w naszym module poświęconym kryptografii.
W tym pokoju nie omawialiśmy ataku podszywającego się pod JWKS. Jeśli jesteś zainteresowany wykorzystaniem tego exploita, zajrzyj do tego pokoju .