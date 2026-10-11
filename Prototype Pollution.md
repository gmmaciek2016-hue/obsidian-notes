


W fascynującym świecie cyberbezpieczeństwa, gdzie hakerzy i pentesterzy krążą w poszukiwaniu luk w zabezpieczeniach, rozwija się koncepcja znana jako zanieczyszczenie prototypów. Pozwala ona cyberprzestępcom manipulować i wykorzystywać wewnętrzne mechanizmy aplikacji JavaScript, a także umożliwia atakującym uzyskanie dostępu do poufnych danych i zaplecza aplikacji.

Chociaż zanieczyszczenie prototypów najczęściej omawiane jest w kontekście języka JavaScript, koncepcję tę można zastosować do dowolnego systemu wykorzystującego podobny model [dziedziczenia oparty na prototypach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain) .

Jednak powszechne zastosowanie JavaScriptu, szczególnie w tworzeniu stron internetowych, oraz jego elastyczny i dynamiczny model obiektów sprawiają, że zanieczyszczenie prototypami jest w tym języku bardziej widocznym i istotnym problemem. Z kolei języki [dziedziczenia opartego na klasach,](https://en.wikipedia.org/wiki/Class-based_programming) takie jak Java czy C++, mają inny model dziedziczenia, w którym klasy (plany obiektów) są zazwyczaj statyczne, a modyfikacja klasy w czasie wykonywania w celu wpłynięcia na wszystkie jej instancje nie jest powszechną praktyką ani prostym zadaniem.  

Cele edukacyjne

﻿W tym pomieszczeniu zdobędziesz wszechstronne zrozumienie następujących kluczowych koncepcji:

- Jak działa prototyp zanieczyszczenia  
    
- Potencjalne zagrożenia dla aplikacji internetowych
- Techniki eksploatacji (po stronie klienta i serwera)
- Techniki łagodzenia

Wymagania wstępne dotyczące nauki  
Przed rozpoczęciem zajęć zaleca się zapoznanie się z poniższymi tematami:

- [Jak działają strony internetowe](https://tryhackme.com/room/howwebsiteswork)
- [HTTPprotokoły i metody](https://tryhackme.com/room/protocolsandservers)
- [OWASP10 najpopularniejszych luk w zabezpieczeniach sieci](https://tryhackme.com/room/owasptop10)

Łączenie z maszyną  
Możesz uruchomić maszynę laboratoryjną, klikając `Start Lab Machine`. Maszyna uruchomi się w widoku podzielonego ekranu. W przypadkuMaszyna wirtualnaJeśli nie jest widoczny, użyj niebieskiego przycisku „Pokaż podzielony widok” w prawym górnym rogu strony. W całym pomieszczeniu korzystamy z podatnej na ataki aplikacji mediów społecznościowych, aby wykonać ćwiczenie w praktyce i zapoznać się z różnymi wektorami ataku . Odczekaj 1–2 minuty po całkowitym uruchomieniu systemu, aby umożliwić prawidłowe uruchomienie automatycznych skryptów. 

Zaczynajmy!


﻿﻿Zanim przejdziemy do zaawansowanych zagadnień, takich jak zanieczyszczenie prototypów, najpierw poznajmy kilka podstawowych zagadnień JavaScriptu. Wyobraźmy sobie **obiekty** jako klocki, które przechowują informacje. **Dziedziczenie** to przekazywanie cech z jednego obiektu do drugiego. **Funkcje** są jak narzędzia, których można używać samodzielnie lub jako części tych obiektów. Wreszcie, **klasy** w JavaScript są jak plany, które pomagają nam łatwo tworzyć podobne rzeczy. Po zapoznaniu się z tymi podstawami, możemy zgłębić bardziej złożony temat zanieczyszczenia prototypów w naszym pokoju.

Obiekty

﻿W JavaScript obiekty są jak kontenery, które mogą przechowywać różne informacje. Wyobraź sobie profil w serwisie społecznościowym jako obiekt, gdzie każdy profil ma właściwości takie jak imię, wiek i liczbę obserwujących. Możesz to przedstawić za pomocą nawiasów klamrowych i par klucz-wartość:

```javascript
let user = {
  name: 'Ben S',
  age: 25,
  followers: 200,
  DoB: '1/1/1990'
};
```

Tutaj  `user` mamy obiekt z właściwościami takimi jak `name`, `age`, i `followers`. Właściwości te przechowują określone informacje o użytkowniku. Obiekty w JavaScript umożliwiają nam organizowanie i zarządzanie powiązanymi danymi, co czyni je fundamentalną koncepcją w tworzeniu dynamicznych i interaktywnych aplikacji.  

Aby przetestować to w praktyce, otwórz aplikację `Chrome`na dołączonej maszynie wirtualnej i po otwarciu przeglądarki kliknij prawym przyciskiem myszy i wybierz [nazwa_użytkownika] `Inspect`, a następnie `Console`[nazwa_użytkownika]. Spowoduje to otwarcie poniższego okna. Skopiuj powyższy kod i wklej go do konsoli. Utworzy on obiekt użytkownika. Teraz możesz uzyskać dostęp do właściwości obiektu, postępując `console.log`zgodnie z poniższym schematem:  

![obraz dla dziennika konsoli](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/99cc8d4964ad5650031e743fd3dddcd4.png)  
  

Zajęcia

W JavaScript klasy są niczym plany, które pomagają tworzyć wiele obiektów o podobnych strukturach i zachowaniach. Pozostając przy naszym przykładzie sieci społecznościowej, możemy użyć klasy do zdefiniowania zwykłego użytkownika i twórcy treści. Klasy zapewniają wygodny sposób organizowania i tworzenia instancji obiektów o wspólnych cechach.

```javascript
// Class for User 
class UserProfile {
  constructor(name, age, followers, dob) {
    this.name = name;
    this.age = age;
    this.followers = followers;
    this.dob = dob; // Adding Date of Birth
  }
}

// Class for Content Creator Profile inheriting from User 
class ContentCreatorProfile extends UserProfile {
  constructor(name, age, followers, dob, content, posts) {
    super(name, age, followers, dob);
    this.content = content;
    this.posts = posts;
  }
}

// Creating instances of the classes
let regularUser = new UserProfile('Ben S', 25, 1000, '1/1/1990');
let contentCreator = new ContentCreatorProfile('Jane Smith', 30, 5000, '1/1/1990', 'Engaging Content', 50);
 
```

Teraz `User` klasa zawiera datę urodzenia (ang. ud.) jako część swoich właściwości i `ContentCreatorProfile`dziedziczy tę właściwość. Tworząc instancje tych klas, możemy podać datę urodzenia i inne szczegóły. Jak widać, uwzględnienie daty urodzenia wzbogaca profile użytkowników o dodatkowe informacje.

Prototyp

W JavaScript każdy obiekt jest powiązany z obiektem prototypowym, a te prototypy tworzą łańcuch, powszechnie nazywany **łańcuchem prototypów** . Prototyp służy jako szablon lub plan dla obiektów. Podczas tworzenia obiektu za pomocą funkcji konstruktora lub klasy, JavaScript automatycznie tworzy połączenie między obiektem a jego prototypem.  W kontekście naszego przykładu z siecią społecznościową, zilustrujmy, jak działają prototypy:

```javascript
// Prototype for User 
let userPrototype = {
  greet: function() {
    return `Hello, ${this.name}!`;
  }
};

// User Constructor Function
function UserProfilePrototype(name, age, followers, dob) {
  let user = Object.create(userPrototype);
  user.name = name;
  user.age = age;
  user.followers = followers;
  user.dob = dob;
  return user;
}

// Creating an instance
let regularUser = UserProfilePrototype('Ben S', 25, 1000, '1/1/1990');

// Using the prototype method
console.log(regularUser.greet());
```

Możesz skopiować kod na dołączonej maszynie wirtualnej i zapoznać się z nim, aby zobaczyć, jak działają obiekty JavaScript.

Różnica między klasą a prototypem

Klasy i prototypy w JavaScript to dwa sposoby na osiągnięcie podobnego celu: tworzenia obiektów z zachowaniami i cechami. Wyobraź sobie, że budujesz modele samochodów w swoim pokoju. Korzystanie z klas jest jak posiadanie szczegółowego projektu lub zestawu instrukcji dla każdego modelu samochodu, który chcesz opracować. Ściśle przestrzegasz projektu, aby stworzyć każdy samochód, a wszystkie samochody zbudowane na podstawie tego samego projektu mają gwarancję tych samych cech i zachowań. Klasy w JavaScript działają podobnie; zapewniają przejrzysty, ustrukturyzowany sposób tworzenia obiektów o tych samych właściwościach i metodach, dzięki czemu są łatwe do zrozumienia i użycia.

Z drugiej strony, prototypy można porównać do posiadania podstawowego modelu samochodu, a następnie jego personalizacji poprzez dodawanie lub modyfikowanie funkcji bezpośrednio w samym samochodzie. W prototypach zaczyna się od prostego obiektu, a następnie dodaje się do niego zachowania, łącząc go z obiektem prototypowym, który już posiada te zachowania. Obiekty utworzone w ten sposób są połączone w łańcuchu prototypów, co pozwala im dziedziczyć zachowania od innych obiektów. Ta metoda jest bardziej dynamiczna i elastyczna, ale może być trudniejsza w zarządzaniu i zrozumieniu niż strukturalne podejście oparte na klasach.

Dziedzictwo

W JavaScript dziedziczenie pozwala jednemu obiektowi dziedziczyć właściwości od drugiego, tworząc hierarchię powiązanych obiektów. Kontynuując nasz przykład z siecią społecznościową, rozważmy bardziej szczegółowy profil twórcy treści. Ten nowy obiekt może dziedziczyć właściwości z ogólnego profilu użytkownika, takie jak „lubię to” `name` i „ lubię to `followers`”, oraz dodawać określone właściwości, takie jak „ `content` lubię to” `posts`.

```javascript
let user = {
  name: 'Ben S',
  age: 25,
  followers: 1000,
DoB: '1/1/1990'
};

// Content Creator Profile inheriting from User 
let contentCreatorProfile = Object.create(user);
contentCreatorProfile.content = 'Engaging Content';
contentCreatorProfile.posts = 50;
 
```

Tutaj `contentCreatorProfile`dziedziczy właściwości od użytkownika za pomocą `Object.create()`. Teraz ma określone właściwości, takie jak `content`, , , i , `posts`z ogólnego profilu użytkownika, jak pokazano poniżej.`name``age``followers`  

![obraz dla dziennika konsoli](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/de24c38d79efaee48dcc302e6a0b4411.png)  

W ten sposób dziedziczenie pomaga tworzyć bardziej wyspecjalizowane obiekty, wykorzystując jednocześnie wspólne właściwości obiektu nadrzędnego. JavaScript obsługuje zarówno dziedziczenie klasowe, jak i oparte na prototypach.

- **Dziedziczenie oparte na prototypie** : W JavaScript każdy obiekt ma prototyp, a tworząc nowy obiekt, można określić jego prototyp. Obiekty dziedziczą właściwości i metody po swoim prototypie. Można użyć tej `Object.create()`metody, aby utworzyć nowy obiekt o określonym prototypie, lub bezpośrednio zmodyfikować prototyp istniejącego obiektu, używając jego właściwości prototype.
- **Dziedziczenie oparte na klasach** : JavaScript obsługuje również klasy, które zapewniają bardziej znaną składnię definiowania obiektów i dziedziczenia. Klasy w JavaScript to jedynie lukier składniowy na istniejącym w JavaScript dziedziczeniu opartym na prototypach. Pod spodem klasy nadal korzystają z prototypów.

![obraz prototypu profilu użytkownika](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/c78a12f7d39bbcf14ef8832fefaf930d.svg)

Diagram po prawej stronie przedstawia dziedziczenie oparte na prototypach w JS:

- **Definiowanie obiektu UserProfile** : Zaczynamy od zdefiniowania `UserProfile`obiektu ogólnego, który reprezentuje wspólne właściwości współdzielone przez różne typy profili. W tym przykładzie `UserProfile`obejmuje on właściwości takie jak adres e-mail i hasło, które mogą być wspólne dla wszystkich profili użytkowników.
- **Tworzenie profilu ContentCreatorProfile** : Tworzymy specjalistyczny profil o nazwie `ContentCreatorProfile`. Ten profil jest specyficzny dla twórców treści i może zawierać dodatkowe właściwości lub zachowania wykraczające poza te w ogólnym profilu użytkownika. Osiągamy to poprzez utworzenie `ContentCreatorProfile`za pomocą `Object.create(UserProfile)`, które ustawia się `UserProfile`jako prototyp `ContentCreatorProfile`.
- **Dodawanie dodatkowych właściwości** : Po utworzeniu ContentCreatorProfile dodajemy określone właściwości, takie jak posty. Ta właściwość jest unikalna `ContentCreatorProfile`i nie jest dziedziczona `UserProfile`.
- **Dostęp do właściwości** : Podczas uzyskiwania dostępu do właściwości obiektu `ContentCreatorProfile`, JavaScript najpierw sprawdza, czy dana właściwość istnieje bezpośrednio w obiekcie `ContentCreatorProfile`. Jeśli jej tam nie znajdzie, przeszukuje łańcuch prototypów i sprawdza, czy istnieje w obiekcie `UserProfile`. Jeśli zostanie znaleziona, zwraca wartość z łańcucha prototypów. W ten sposób obiekt `ContentCreatorProfile`dziedziczy właściwości „email” i „password” z obiektu `UserProfile`, mając jednocześnie własną, unikalną właściwość „liczba wpisów”. Pozwala to na stworzenie struktury hierarchicznej, w której wyspecjalizowane profile mogą dziedziczyć wspólne właściwości z profilu ogólnego, dodając jednocześnie swoje specyficzne atrybuty.

![obraz podsumowujący klasy i dziedziczenie](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/ba889a24229822ded96d81b5a97484d0.svg)  

Podsumujmy to, co omówiliśmy do tej pory, korzystając z powyższego diagramu. Koncepcja prototypów odgrywa kluczową rolę w implementacji dziedziczenia. Każdy obiekt w JavaScript ma prototyp, który służy jako plan dla właściwości i metod obiektu. Na powyższym obrazku, gdy definiujemy klasę taką jak `UserProfile`, jej prototyp staje się prototypem wszystkich instancji utworzonych z niej. Oznacza to, że właściwości i metody zdefiniowane w klasie `UserProfile`są dostępne dla wszystkich instancji `UserProfile`. Ponadto JavaScript pozwala nam dynamicznie rozszerzać te prototypy, umożliwiając dziedziczenie poprzez łańcuchowanie prototypów. Na przykład podklasy takie jak `ContentCreator`, `ContentDesigner`, i `Moderator`mogą rozszerzać prototyp klasy `UserProfile`, aby dziedziczyć jej właściwości i metody. Wykorzystując prototypy, JavaScript zapewnia elastyczny i wydajny mechanizm implementacji dziedziczenia, umożliwiając ponowne wykorzystanie kodu i łatwość utrzymania w paradygmatach programowania obiektowego.

﻿Skoro mamy już podstawową wiedzę o JavaScript, zagłębmy się w temat zanieczyszczenia prototypami, wykorzystując ten sam przykład z siecią społecznościową. ![obraz postaci trzymającej laptopa](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/d63bebfd81c03b6adbc1ce2e1f59750c.svg)Zanieczyszczenie prototypami to podatność, która pojawia się, gdy atakujący manipuluje prototypem obiektu, wpływając na wszystkie jego instancje. W JavaScript, gdzie prototypy ułatwiają dziedziczenie, atakujący może to wykorzystać do modyfikacji współdzielonych właściwości lub wprowadzenia złośliwego zachowania w obiektach.  

_Samo zanieczyszczenie prototypów nie zawsze stanowi bezpośrednie zagrożenie, które można wykorzystać. Jednak jego prawdziwy potencjał szkodliwości staje się szczególnie widoczny, gdy łączy się z innymi rodzajami podatności, takimi jakXSSICSRF._

Typowy przykład

Załóżmy, że mamy podstawowy prototyp `Person`metody `introduce`. Atakujący dąży do manipulowania zachowaniem metody `introduce`we wszystkich instancjach poprzez modyfikację prototypu.  

```javascript
// Base Prototype for Persons
let personPrototype = {
  introduce: function() {
    return `Hi, I'm ${this.name}.`;
  }
};

// Person Constructor Function
function Person(name) {
  let person = Object.create(personPrototype);
  person.name = name;
  return person;
}

// Creating an instance
let ben = Person('Ben');
```

Skopiuj powyższy kod, wklej go do konsoli i naciśnij `enter`. Po utworzeniu nowego obiektu `ben`i wywołaniu `introduce`metody wyświetli się `Hi, I'm Ben`, jak pokazano na poniższym rysunku.  

![obraz konsoli](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/23cf37880af1735915022ab52c32a166.png)  

Co się stanie, jeśli atakujący wstrzyknie złośliwą zawartość do metody „intro” dla wszystkich instancji korzystających z tej `__proto__`właściwości? W JavaScript `__proto__`właściwość jest powszechnym sposobem dostępu do prototypu obiektu, zasadniczo wskazującym na obiekt, z którego dziedziczy właściwości i metody. Zobaczmy, w jakiś sposób atakujący wykonuje poniższy kod, używając dowolnego wektora ataku, takiego jak XSS, CSRF itp.  

```javascript
// Attacker's Payload
ben.__proto__.introduce=function(){console.log("You've been hacked, I'm Bob");}
console.log(ben.introduce()); 
 
```

Omówimy szczegółowo, co dokładnie dzieje się w tle:  

- **Definicja prototypu** : Prototyp Osoby (personPrototype) jest początkowo definiowany za pomocą nieszkodliwej `introduce`metody wprowadzającej osobę.
- **Instancjacja obiektu** : tworzona jest instancja Osoby o nazwie `'Ben' (let ben = Person('Ben');)`.
- **Atak typu „prototype pollition”** : Atakujący wstrzykuje złośliwy ładunek do metody prototypu `introduce`, zmieniając jej zachowanie i wyświetlając szkodliwy komunikat. W tym przypadku zanieczyściliśmy tę  `__proto__`właściwość.
- **Wpływ na istniejące wystąpienia** : W rezultacie nawet istniejące wystąpienie ( `ben`) jest zagrożone, a wywołanie `ben.introduce()`teraz powoduje wyświetlenie wstrzykniętego komunikatu atakującego.

Ten przykład pokazuje, jak atakujący może zmienić działanie metod współdzielonych w różnych obiektach, potencjalnie stwarzając zagrożenia bezpieczeństwa. Zapobieganie zanieczyszczeniu prototypów polega na starannej walidacji danych wejściowych i unikaniu bezpośredniej modyfikacji prototypów o niezaufanej zawartości.


Podejście standardowe

Jak wiemy, wiele właściwości jest nieodłącznie obecnych w prototypie obiektu w JavaScript. Wśród nich właściwości `constructor` i `__proto__` wyróżniają się jako szczególnie istotne cele ataków ze strony cyberprzestępców. Właściwość `constructor` wskazuje na funkcję, która konstruuje prototyp obiektu, podczas gdy `__proto__` odnosi się do obiektu prototypu, po którym bieżący obiekt bezpośrednio dziedziczy. Cyberprzestępcy często wykorzystują te właściwości do manipulowania łańcuchem prototypów obiektu, co potencjalnie prowadzi do zanieczyszczenia prototypu.

Złota zasada

Koncepcja opiera się na zdolności atakującego do wpływania na pewne kluczowe parametry, takie jak `x` i `val`, w wyrażeniach podobnych do `Person[x][y] = val`. Załóżmy, że atakujący przypisuje `__proto__`. `x`W takim przypadku atrybut identyfikowany przez `y`jest uniwersalnie ustawiany we wszystkich obiektach współdzielących tę samą klasę co obiekt o wartości oznaczonej przez `val`.

W bardziej złożonym scenariuszu, gdy atakujący ma kontrolę nad `x`, `y`, i `val` w strukturze takiej jak `Person[x][y][z] = val`, przypisanie `x` as `constructor` i `y` as `prototype` prowadzi do nowej właściwości zdefiniowanej poprzez `z` ustanowienie jej we wszystkich obiektach w aplikacji z przypisanym `val`. To ostatnie podejście wymaga bardziej złożonego układu właściwości obiektów, co czyni je mniej powszechnym w praktyce.

Kilka ważnych funkcji

Identyfikując potencjalne luki w zabezpieczeniach związane z zanieczyszczeniem prototypów, testerzy penetracyjni powinni skupić się na powszechnie używanych wektorach/funkcjach podatnych na zanieczyszczenie prototypów. Dokładna analiza sposobu, w jaki aplikacja obsługuje manipulację obiektami, jest kluczowa. Zrozumiemy kilka ważnych funkcji, które atakujący może wykorzystać, a następnie przeprowadzimy praktyczną eksploatację.

- **Definicja właściwości według ścieżki** : Funkcje ustawiające właściwości obiektu na podstawie danej ścieżki (takie jak [brakuje kontekstu `object[a][b][c] = value`]) mogą być niebezpieczne, jeśli komponenty ścieżki są kontrolowane przez dane wejściowe użytkownika. Należy sprawdzić te funkcje, aby upewnić się, że nie modyfikują one przypadkowo prototypu obiektu.  Rozważ punkt końcowy, który umożliwia użytkownikom aktualizowanie recenzji dowolnego znajomego.

**Początkowa struktura obiektu**

Zanim zostaną wprowadzone jakiekolwiek aktualizacje, mamy początkową tablicę znajomych zawierającą obiekt reprezentujący profil znajomego. Każdy obiekt profilu zawiera właściwości takie jak identyfikator, nazwa, recenzje i albumy.

```javascript
let friends = [ { id: 1, name: "testuser", age: 25, country: "UK", reviews: [], albums: [{ }], password: "xxx", } ]; _.set(friend, input.path, input.value);
```

**Dane wejściowe otrzymane od użytkownika**

Użytkownik chce dodać recenzję dla swojego znajomego. Podaje ładunek zawierający ścieżkę do miejsca, w którym recenzja powinna zostać dodana ( **recenzje.content** ) oraz treść recenzji ( **<script>alert(anycontent)</script>** ).  

Atakujący aktualizuje ścieżkę, aby zaatakować prototyp:

```javascript
{ "path": "reviews[0].content", "value": "&#60;script&#62;alert('anycontent')&#60;/script&#62;" };
```

Używamy funkcji **_set** z lodash, aby zastosować ładunek i dodać zawartość recenzji do określonej ścieżki w obiekcie profilu znajomego.

**Wynikowa struktura obiektu**

Po wykonaniu kodu tablica „friends” zostanie zmodyfikowana i uwzględniona w niej zostanie recenzja użytkownika. Jednak z powodu braku prawidłowej walidacji danych wejściowych, treść recenzji dostarczona przez użytkownika ( **<script>alert('anycontent')</script>** ) została dodana bezpośrednio do obiektu profilu bez odpowiedniej sanityzacji.

```javascript
let friends = [
  {
    id: 1,
    name: "testuser",
    age: 25,
    country: "UK",
    reviews: [
      "<script>alert('anycontent')</script>"
    ],
    albums: [{}],
    password: "xxx",
  }
];
```

Podobnie, załóżmy, że atakujący chce wstawić szkodliwą właściwość do profilu znajomego. W takim przypadku dostarcza ładunek zawierający ścieżkę, pod którą właściwość powinna zostać dodana ( **isAdmin** ) oraz wartość tej szkodliwej właściwości (true).  

```javascript
const payload = { "path": "isAdmin", "value": true };
```

Po wykonaniu kodu `friends`tablica zostanie zmodyfikowana w celu uwzględnienia złośliwej właściwości **isAdmin** w obiekcie profilu znajomego. `friends`Obiekt będzie miał następującą strukturę:  

```javascript
let friends = [
  {
    id: 1,
    name: "testuser",
    age: 25,
    country: "UK",
    reviews: [],
    albums: [],
    password: "xxx",
    isAdmin: true // Malicious property inserted by the attacker
  }
];
```

Przykład praktyczny

Teraz zobaczymy, jak atakujący mogą wykorzystać tę lukę w praktyce. Załóżmy, że pracujesz jako pentester w firmie, której zadaniem jest przeprowadzenie testów penetracyjnych aplikacji mediów społecznościowych. Dostęp do aplikacji można uzyskać za pośrednictwem adresu `MACHINE_IP:5000`URL, używając następujących danych logowania:  

- Nazwa użytkownika:`bob`
- Hasło:`bob@123`

Po zalogowaniu zobaczysz taki panel:

![obraz deski rozdzielczej](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e8b58c7609886ffefb79435e3ac75f23.png)  

Aby zidentyfikować zanieczyszczenie prototypowe, przyjrzymy się różnym funkcjom aplikacji mediów społecznościowych, takim jak dodawanie albumów, wysyłanie zaproszeń do znajomych, dodawanie recenzji itp. Po zalogowaniu możesz dodać innych znajomych do swojej listy znajomych. Odwiedź profil dowolnego znajomego (na przykład Sabalenki). Po wejściu na stronę zobaczysz różne opcje, takie jak dodawanie recenzji, klonowanie albumu itp. Przyjrzyjmy się funkcji przesyłania recenzji.

![funkcja przesyłania recenzji](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/f730a61990991d810591859a18ee0974.png)  

Funkcja przesyłania recenzji pozwala użytkownikom przesłać dowolną recenzję, która zostanie zapisana w bazie danych. Przyjrzyjmy się kodowi po stronie klienta i serwera, aby przeanalizować różne możliwości wykorzystania tej funkcji.

```shell-html
    <form action="/submit-friend-review" method="post" class="mb-4">
        <h2 class="mb-3">Submit a Review</h2>
        <input type="hidden" name="friendId" value="1">
        <div class="form-group">
            <textarea class="form-control" name="reviewContent" placeholder="Write your review here"
                rows="3"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit Review</button>
    </form>
 
```

Kod po stronie klienta przyjmuje recenzję jako parametr wejściowy i wywołuje punkt końcowy API `/submit-friend-review` , aby dodać recenzję wraz z ukrytym parametrem `friendId`.  Jak omówiono w poprzednich zadaniach, samo zanieczyszczenie prototypów rzadko jest podatne na ataki; jednak w połączeniu z innymi wektorami ataku, takimi jak XSS, może zapewnić lepszą powierzchnię ataku. Przyjrzyjmy się teraz kodowi po stronie serwera.

```javascript
let friends = [
  {
    id: 1,
    name: "Sabalenka",
    age: 25,
    country: "UK",
    reviews: [],
    albums: [{ name: "USA Trip", photos: "git.thm" }],
    password: "xxx",
  },
...
...
app.post("/submit-friend-review", (req, res) => {
  if (!req.session.user) {
    return res.redirect("/signin");
  }
  const { friendId, reviewContent } = req.body;
  const friend = friends.find((f) => f.id === parseInt(friendId));
  if (!friend) {
    return res.status(404).send("Friend not found");
  }
  try {
    const input = JSON.parse(reviewContent);
    _.set(friend, input.path, payload.value);
  } catch (e) { }
  res.redirect(`/friend/${friendId}`);
});
 
```

 Ten kod wykonuje następujące czynności:

- Najpierw weryfikuje sesję zalogowanego użytkownika; jeśli nie, przekierowuje go na stronę logowania.
- Następnie kod wyodrębnia parametr i weryfikuje połączenie między zalogowanym użytkownikiem a `friendId`otrzymanymi w żądaniu parametrami.
- Po sprawdzeniu połączenia znajomego kod wstawia recenzję do obiektu znajomego.
- Kod wykorzystuje `_.set`funkcję narzędzia Lodash, która pozwala ustawić wartość właściwości w danej ścieżce obiektu. To wygodny sposób na ustawianie wartości obiektów na poziomie głębszym, bez konieczności sprawdzania, czy każdy poziom ścieżki istnieje. Jeśli fragment ścieżki nie istnieje, `_set`zostanie utworzony.  
    
- Analiza kodu pokazuje, że jest to doskonała okazja do przeprowadzenia ataku **polegającego na zdefiniowaniu właściwości przez ścieżkę** .
- Teraz dodajmy znajomego i odwiedźmy jego profil, aby dodać prostą recenzję i sprawdzić, czy to działa.

![obraz po pomyślnym dodaniu recenzji](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/63a1b1a9086c96548a20e1e607368019.png)  

- Recenzja została pomyślnie dodana. Bazując na wiedzy uzyskanej z przeglądu kodu źródłowego, przygotujmy ładunek do wysłania recenzji, który wyzwoli alert. Wiemy, że obiekt znajomego zawiera tablicę, `reviews`w której przechowywane są recenzje każdego użytkownika. Funkcja dodawania recenzji działa tylko na profilu znajomego.

```javascript
{"path": "reviews[0].content", "value": "<script>alert('Hacked')</script>"}
 
```

![Obraz XSS po zanieczyszczeniu prototypu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/49e3129bac73bee07c10fe3a1909ac3c.png)

Teraz, gdy ktoś odwiedzi profil tego użytkownika, zostanie uruchomiony atak XSS. W takich sytuacjach atakujący może nawet manipulować innymi właściwościami, które mogą umożliwić użytkownikowi dostęp administracyjny, takimi jak [brakujący element] `isAdmin`itp `isloggedIn`.

W tym zadaniu dowiedzieliśmy się, jak atakujący może uruchomić prototyp zanieczyszczenia iXSSAtak z wykorzystaniem techniki „własności z definicji”. W następnym zadaniu będziemy kontynuować naukę kilku kolejnych funkcji.


Kilka ważnych funkcji

- **Rekurencyjne scalanie obiektów** : Ta funkcja polega na rekurencyjnym scalaniu właściwości z obiektów źródłowych do obiektu docelowego. Atakujący może wykorzystać tę funkcjonalność, jeśli funkcja scalania nie zweryfikuje danych wejściowych i zezwoli na scalanie właściwości w łańcuchu prototypów. Rozważając ten sam przykład z siecią społecznościową, załóżmy, że poniższy kod. Załóżmy, że aplikacja ma funkcję scalania ustawień użytkownika:

```javascript
// Vulnerable recursive merge function
function recursiveMerge(target, source) {
    for (let key in source) {
        if (source[key] instanceof Object) {
            if (!target[key]) target[key] = {};
            recursiveMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

// Endpoint to update user settings
app.post('/updateSettings', (req, res) => {
    const userSettings = req.body; // User-controlled input
    recursiveMerge(globalUserSettings, userSettings);
    res.send('Settings updated!');
});
 
```

Atakujący wysyła żądanie z zagnieżdżonym obiektem zawierającym `__proto__`:

```javascript
 { "__proto__": { "newProperty": "value" } } 
```

- **Klonowanie obiektów** : Klonowanie obiektów to podobna funkcjonalność, która umożliwia operacjom głębokiego klonowania przypadkowe kopiowanie właściwości z łańcucha prototypów do innego. Testowanie powinno zapewnić, że te funkcje klonują tylko zdefiniowane przez użytkownika właściwości obiektu i filtrują specjalne słowa kluczowe, takie jak __proto__, konstruktor itp. Możliwym przypadkiem użycia jest klonowanie obiektów przez zaplecze aplikacji w celu utworzenia nowych profili użytkowników:

Przykład praktyczny

Teraz zobaczymy, jak atakujący mogą wykorzystać tę lukę w praktyce.  Przyjrzyjmy się funkcji klonowania albumu.  Funkcja ta pozwala użytkownikom sklonować album, podając nową nazwę.

![Funkcja klonowania albumu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/ad5f4fc5de32c3280cc67bdeecb40a23.png)  

Przyjrzyjmy się kodowi po stronie klienta i serwera, aby zbadać różne możliwości wykorzystania luk.

```javascript
<form action="/clone-album/1" method="post" class="mb-4">
        <h2 class="mb-3">Clone Album of Josh</h2>
        <div class="form-group">
            <label for="selectedAlbum">Select an Album to Clone:</label>
            <select class="form-control" name="selectedAlbum" id="selectedAlbum">
                    <option value="Trip to US">
                        Trip to US
                    </option>
            </select>
        </div>
        <div class="form-group">
            <label for="newAlbumName">New Album Name:</label>
            <input type="text" class="form-control" name="newAlbumName" id="newAlbumName"
                placeholder="Enter new album name">
        </div>
        <button type="submit" class="btn btn-primary">Clone Album</button>
    </form>
 
```

Kod po stronie klienta przyjmuje nazwę jako dane wejściowe i wywołuje punkt końcowy API `/clone-album/{album_ID}` w celu sklonowania albumu. Jak omówiono w poprzednich zadaniach, samo zanieczyszczenie prototypów rzadko jest podatne na ataki; jednak w połączeniu z innymi wektorami ataku, takimi jak XSS, może zapewnić lepszą powierzchnię ataku .  Przyjrzyjmy się teraz kodowi po stronie serwera.

```javascript
app.post("/clone-album/:friendId", (req, res) => {
  const { friendId } = req.params;
  const { selectedAlbum, newAlbumName } = req.body;
  const friend = friends.find((f) => f.id === parseInt(friendId));
  if (!friend) {
    console.log("Friend not found");
    return res.status(404).send("Friend not found");
  }
  const albumToClone = friend.albums.find(
    (album) => album.name === selectedAlbum
  );
  if (albumToClone && newAlbumName) {
    let clonedAlbum = { ...albumToClone };
    try {
      const payload = JSON.parse(newAlbumName);
      merge(clonedAlbum, payload);
    } catch (e) {
    }

function merge(to, from) {
  for (let key in from) {
    if (typeof to[key] == "object" && typeof from[key] == "object") {
      merge(to[key], from[key]);
    } else {
      to[key] = from[key];
    }
  }
  return to;
}
 
```

W powyższym kodzie serwery otrzymująJSONobiekt zawierający nazwę albumu, skopiuj album, który chcesz skopiować, do innego obiektu i zmień nazwę nowo utworzonej kopii, wywołując funkcję scalania.  

Wiemy, że funkcja scalania jest idealnym kandydatem na zanieczyszczenie prototypu, jeśli bezmyślnie kopiuje wszystkie obiekty i właściwości bez oczyszczania na podstawie kluczy. Widzimy, że funkcja scalania stworzona przez programistę nie posiadała żadnych takich filtrów oczyszczania. Co się stanie, jeśli wyślemy żądanie zawierające wartość `__proto__`z parametrem `newProperty`  i, jak opisano poniżej:

```javascript
{"__proto__": {"newProperty": "hacked"}}
```

Funkcja scalania potraktuje „[]” `__proto__`  jako właściwość i wywoła „[] `obj.__proto__.newProperty=value`. W ten sposób „ `newProperty`[]” nie zostanie dodany bezpośrednio do obiektu „znajomy”. Zamiast tego zostanie dodany do prototypu obiektu „znajomy”. Oznacza to, że `newProperty`nie będzie widoczny we właściwościach „znajomego” (takich jak imię, wiek itp.), ale nadal będzie dostępny. Sklonujmy album, odwiedzając profil Josha i używając powyższego ładunku jako nazwy albumu.

![obraz po klonowaniu albumu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/985c66e44b234218ff481dfb9fc2ef48.png)  

No i zaczynamy! Mamy nową właściwość dla wszystkich obiektów znajomych.

- **Wpływ na wszystkie obiekty tego samego typu** : Ponieważ wszystkie obiekty zaprzyjaźnione współdzielą ten sam prototyp (są tworzone z tego samego szablonu lub konstruktora), dodanie `newProperty`do prototypu oznacza, że ​​wszystkie obiekty zaprzyjaźnione mają teraz dostęp do właściwości newProperty. To jak dodanie nowej funkcji do szablonu;
    
    teraz każdy obiekt utworzony na podstawie tego szablonu ma tę nową funkcję.
- **Obserwacja zmiany** : Chociaż `newProperty`nie jest ona bezpośrednio widoczna podczas drukowania obiektu znajomego, nadal tam jest. Można uzyskać do niej dostęp, wywołując `friend.newProperty`, co spowoduje wyświetlenie komunikatu " `testValue`".
- **Jak newProperty staje się widoczne** : Kiedy dodajesz newProperty za pośrednictwem prototypu, nie istnieje ono bezpośrednio w poszczególnych obiektach (jak każdy obiekt partnerski), lecz w ich prototypie. Jednak gdy uzyskujesz dostęp do właściwości obiektu, JavaScript najpierw szuka tej właściwości w samym obiekcie. Jeśli jej nie znajdzie, JavaScript przeszukuje łańcuch prototypów, aż ją znajdzie (lub dotrze do końca łańcucha).
- **Renderowanie na ekranie** : W szablonie [EJS](https://ejs.co/) , gdy przechodzisz przez właściwości obiektu znajomego za pomocą `for...in loop`( `<% for (let key in friend) { %> ... <% } %>`) i wyświetlasz je, pętla ta iteruje po wszystkich wyliczalnych właściwościach obiektu znajomego, w tym tych odziedziczonych z prototypu. Dlatego, mimo że newProperty nie znajduje się bezpośrednio w obiekcie znajomego, lecz w jego prototypie, nadal pojawia się w tej pętli i jest renderowana na ekranie.  
    

W tym zadaniu nauczyliśmy się, jak dodać nową właściwość do prototypu obiektu, aby zanieczyścić jego ogólną strukturę. W następnym zadaniu dowiemy się, jak spowodować awarię całej aplikacji, jeśli programista nie podejmie niezbędnych działań.

Uwaga: Aby odpowiedzieć na poniższe pytania, odwiedź adres URL `http://MACHINE_IP:8080/getFlag.php`, aby pobrać flagi. Zobaczysz następujący panel, aby pobrać flagi:

![panel do otrzymywania flag](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e9c9b96e18ff0aac5850831cb879842d.png)


Odmowa usługi

Zanieczyszczenie prototypu, krytyczna luka w zabezpieczeniach aplikacji JavaScript, może prowadzić do odmowy usługi (DoS) atak, który może mieć poważne konsekwencje. Dzieje się tak, gdy atakujący manipuluje prototypem powszechnie używanego obiektu, powodując nieoczekiwane zachowanie aplikacji lub jej całkowitą awarię. W JavaScript obiekty dziedziczą właściwości i metody ze swojego prototypu, a modyfikacja tego prototypu wpływa na wszystkie obiekty, które go współdzielą.![obraz awarii serwera z technikiem](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/ac8fe0c7e8bfbfc77c034bc399e1da7f.svg)  

Na przykład, jeśli atakujący zanieczyści `Object.prototype.toString` metodę, każde kolejne wywołanie tej metody przez dowolny obiekt spowoduje wykonanie zmienionego zachowania. W złożonej aplikacji, gdzie `toString`jest to często używane, może to prowadzić do nieoczekiwanych rezultatów, potencjalnie powodując awarię aplikacji. `toString`Metoda ta jest powszechnie stosowana w JavaScript. Jest automatycznie wywoływana w wielu kontekstach, zwłaszcza gdy obiekt musi zostać przekonwertowany na ciąg znaków.

Jeśli zanieczyszczona metoda prowadzi do nieefektywnego przetwarzania lub nieskończonej pętli, może wyczerpać zasoby systemowe, powodując w efekcie atak DoS. Co więcej, zanieczyszczenie prototypów może również zakłócać logikę biznesową aplikacji. Zmiana istotnych metod lub właściwości może wywołać nieobsłużone wyjątki lub błędy, prowadzące do zakończenia działania procesów lub usług. Może to spowodować, że serwer przestanie odpowiadać w aplikacjach internetowych, odmawiając dostępu do usług uprawnionym użytkownikom.

Przykład praktyczny

- Ponownie odwiedź adres URL `http://MACHINE_IP:5000` i sprawdź, czy możemy spowodować awarię serwera poprzez dowolne dane wejściowe. Jak już wspomniano, mamy metodę `Object.prototype.toString`, która konwertuje obiekt na typ danych String.  
    
- Odwiedź stronę profilu dowolnego znajomego; możemy zobaczyć na przykładzie poprzedniego zadania, jak wygląda kod po stronie serwera

```html
<form action="/clone-album/1" method="post" class="mb-4">
        <h2 class="mb-3">Clone Album of Josh</h2>
        <div class="form-group">
            <label for="selectedAlbum">Select an Album to Clone:</label>
            <select class="form-control" name="selectedAlbum" id="selectedAlbum">
                    <option value="Trip to US">
                        Trip to US
                    </option>
            </select>
        </div>
        <div class="form-group">
            <label for="newAlbumName">New Album Name:</label>
            <input type="text" class="form-control" name="newAlbumName" id="newAlbumName"
                placeholder="Enter new album name">
        </div>
        <button type="submit" class="btn btn-primary">Clone Album</button>
    </form>
 
```

- Widzimy, że ta funkcja wywołuje funkcję scalania, która scala dwa obiekty. Co się stanie, jeśli spróbujemy wysłać ładunek, który nadpisze istniejącą funkcję, taką jak `toString()`, a następnie wywołamy ją na jakimś obiekcie, spowoduje to nagłe zachowanie serwera?  
    
- Aby przygotować ładunek, użyjmy prostego kodu JSON, który nadpisze funkcję toString, jak pokazano poniżej:

```javascript
{"__proto__": {"toString": "Just crash the server"}}
 
```

- Przejdź na stronę profilu i wprowadź ładunek zamiast nazwy nowego albumu, jak pokazano poniżej:

![klon obrazu albumu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/0c526f55ae09c8a2edd3bb9424d67223.png)  

- Zdekodujmy ładunek po `app.js`otrzymaniu żądania, przeanalizujmy JSON i przypisajmy `toString` wartość funkcji we `__proto__`właściwości obiektu znajomego.
- Powoduje to nagłe zachowanie, `toString`powszechnie spotykane w przypadku różnych obiektów. Po kliknięciu „Klonuj album” aplikacja ulega awarii, jak pokazano poniżej:

![zrzut ekranu błędu po nadpisaniu ciągu](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/63081473d800a1e88f5a46c40ed09aa5.png)  

- To, `TypeError` co otrzymujemy, `Object.prototype.toString.call`nie jest funkcją, ponieważ już zastąpiliśmy tę funkcję za pomocą zanieczyszczenia prototypu.
- Możesz nadpisać kilka innych wbudowanych obiektów/funkcji, takich jak `toJSON`, `valueOf`, `constructor`itd., ale aplikacja nie ulegnie awarii w przypadku wszystkich zachowań. Zależy to całkowicie od funkcji, którą nadpisujesz.


Główne problemy podczas identyfikacji

Identyfikacja zanieczyszczenia prototypami to trudny problem w każdym języku, a szczególnie w JavaScript, ze względu na sposób, w jaki JavaScript pozwala ![automatyzacja prototypu zanieczyszczeń](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/fabc3c2e9580c19e3a8cd9c878784ed7.svg)obiektom współdzielić swoje funkcje z innymi. Automatyczne wykrywanie tego problemu za pomocą narzędzi programowych jest naprawdę trudne, ponieważ nie jest on tak prosty, jak inne typowe problemy z bezpieczeństwem stron internetowych. Każda strona internetowa lub aplikacja internetowa jest inna, a ustalenie, gdzie może wystąpić zanieczyszczenie prototypami, wymaga dokładnego przyjrzenia się kodowi strony, zrozumienia jego działania i wykrycia ewentualnych błędów.  

W przeciwieństwie do innych problemów bezpieczeństwa, które można znaleźć, szukając konkretnych wzorców lub oznak, znalezienie zanieczyszczenia prototypów wymaga dogłębnej analizy kodu strony internetowej przez pentestera/programistę. Chodzi o zrozumienie złożonych sposobów, w jakie obiekty w JavaScript mogą na siebie wpływać, i wykrycie potencjalnych problemów. Narzędzia bezpieczeństwa mogą pomóc w zidentyfikowaniu potencjalnych problemów, ale nie są w stanie wykryć wszystkich. Dlatego tak ważne jest, aby osoby potrafiące uważnie czytać i analizować kod były w stanie to zrobić.   

Kilka ważnych skryptów

W społecznościach zajmujących się bezpieczeństwem i oprogramowaniem open source opracowano szereg narzędzi i projektów wspomagających automatyzację wyszukiwania prototypowych luk w zabezpieczeniach związanych z zanieczyszczeniem. Oto kilka renomowanych repozytoriów GitHub, które udostępniają narzędzia, biblioteki lub analizy ułatwiające wykrywanie prototypowych luk w zabezpieczeniach związanych z zanieczyszczeniem:

- **[NodeJsScan](https://github.com/ajinabraham/nodejsscan)** to statyczny skaner kodu bezpieczeństwa dla aplikacji Node.js. Obejmuje on weryfikację różnych luk w zabezpieczeniach, w tym zanieczyszczenia prototypów. Zintegrowanie NodeJsScan z procesem rozwoju oprogramowania może pomóc w automatycznej identyfikacji potencjalnych problemów bezpieczeństwa w bazie kodu. 
- [**Prototype Pollution Scanner**](https://github.com/KathanP19/protoscan) to narzędzie przeznaczone do skanowania kodu JavaScript w poszukiwaniu luk w zabezpieczeniach prototypów. Można go używać do analizy baz kodu pod kątem wzorców podatnych na zanieczyszczenia, pomagając programistom identyfikować i rozwiązywać potencjalne problemy bezpieczeństwa w ich aplikacjach.
- [**PPFuzz**](https://github.com/dwisiswant0/ppfuzz)  to kolejny fuzzer zaprojektowany do automatyzacji procesu wykrywania luk w zabezpieczeniach związanych z zanieczyszczeniem prototypów w aplikacjach internetowych. Poprzez fuzzing wektorów wejściowych, które mogą oddziaływać z właściwościami obiektów,`PPFuzz`można zidentyfikować punkty w aplikacji podatne na zanieczyszczenie prototypów. 
- Wykrywanie po stronie klienta przez [**BlackFan**](https://github.com/BlackFan/client-side-prototype-pollution) koncentruje się na identyfikacji luk w zabezpieczeniach JavaScript po stronie klienta, związanych z zanieczyszczeniem prototypów. Zawiera przykłady wykorzystania zanieczyszczenia prototypów w przeglądarkach do wykonywania…XSSataków i innych złośliwych działań. To cenne źródło informacji pozwalające zrozumieć wpływ zanieczyszczenia prototypów na stronę klienta.

Identyfikując zanieczyszczenie prototypów, pentester powinien szukać przypadków, w których dane wprowadzane przez użytkownika mogłyby wpłynąć na klucze lub właściwości poddawane łączeniu, definiowaniu lub klonowaniu. Weryfikacja, czy aplikacja prawidłowo oczyszcza i weryfikuje takie dane wprowadzane pod kątem modyfikacji łańcucha prototypów, ma kluczowe znaczenie dla zapobiegania podatnościom na zanieczyszczenie prototypów.


﻿Ograniczanie ryzyka związanego z zanieczyszczeniem prototypów jest kluczowe zarówno dla pentesterów, jak i twórców bezpiecznego kodu, ponieważ luka ta umożliwia atakującym manipulowanie prototypem obiektu, co potencjalnie może prowadzić do nieoczekiwanego zachowania i problemów z bezpieczeństwem. Oto kilka środków zaradczych w przypadku zanieczyszczenia prototypów:  

Pentesterzy

- ![ochrona przed podatnym na ataki kodem JS](https://cdn-images.tryhackme.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e1b7beee648bad62b755daf172eb1b0d.svg)**Rozmycie i manipulacja danymi wejściowymi** : Intensywna interakcja z danymi wejściowymi użytkownika, zwłaszcza tymi używanymi do interakcji ze strukturami opartymi na prototypach, i rozmycie ich za pomocą różnorodnych ładunków. Należy szukać scenariuszy, w których niepewne dane mogą prowadzić do zanieczyszczenia prototypu.
- **Analiza kontekstu i wstrzykiwanie danych** : Przeanalizuj bazę kodu aplikacji, aby zrozumieć, jak dane wprowadzane przez użytkownika są wykorzystywane w strukturach opartych na prototypach. Wstrzykuj dane do tych kontekstów, aby przetestować podatności na zanieczyszczenie prototypów.
- **CSPObejście i wstrzykiwanie danych** : Oceń skuteczność nagłówków bezpieczeństwa, takich jak CSP, w ograniczaniu zanieczyszczenia prototypów. Spróbuj ominąć ograniczenia CSP i wstrzyknąć dane w celu manipulowania prototypami.
- **Analiza i eksploatacja zależności** : Przeprowadź dokładną analizę bibliotek zewnętrznych i zależności używanych przez aplikację. Zidentyfikuj przestarzałe lub podatne biblioteki, które mogą wprowadzać luki w zabezpieczeniach związane z zanieczyszczeniem prototypów. Wykorzystaj te luki do manipulowania prototypami i uzyskiwania nieautoryzowanego dostępu lub wykonywania innych złośliwych działań.
- **Statyczna analiza kodu** : Użyj narzędzi do statycznej analizy kodu, aby zidentyfikować potencjalne luki w zabezpieczeniach prototypów w fazie rozwoju. Narzędzia te mogą dostarczyć informacji na temat niebezpiecznych wzorców kodowania i potencjalnych zagrożeń bezpieczeństwa.

Bezpieczni programiści kodu

- **Unikaj używania __proto__** : Powstrzymaj się od używania tej `__proto__`właściwości, ponieważ jest ona najbardziej podatna na zanieczyszczenie prototypu. Zamiast tego użyj jej, `Object.getPrototypeOf()`aby uzyskać dostęp do prototypu obiektu w bezpieczniejszy sposób.
- **Niezmienne obiekty** : Projektuj obiekty tak, aby były niezmienne, gdy tylko jest to możliwe. Zapobiega to niezamierzonym modyfikacjom prototypu, zmniejszając wpływ podatności na zanieczyszczenie środowiska prototypu.
- **Hermetyzacja** : Hermetyzuj obiekty i ich funkcjonalności, udostępniając tylko niezbędne interfejsy. Może to pomóc w zapobieganiu nieautoryzowanemu dostępowi do prototypów obiektów.
- **Używaj bezpiecznych wartości domyślnych** : Podczas tworzenia obiektów, ustal bezpieczne wartości domyślne i unikaj polegania na danych wprowadzanych przez użytkownika przy ustawianiu właściwości prototypów. Inicjuj obiekty bezpiecznie, aby zminimalizować ryzyko zanieczyszczenia.
- **Sanityzacja danych wejściowych** : Dokładnie sanityzuj i waliduj dane wejściowe użytkownika. Zachowaj ostrożność, używając danych kontrolowanych przez użytkownika do modyfikacji prototypów obiektów. Stosuj rygorystyczne praktyki walidacji danych wejściowych, aby zminimalizować ryzyko wstrzyknięcia.
- **Zarządzanie zależnościami** : Regularnie aktualizuj i monitoruj zależności. Wybieraj dobrze utrzymane biblioteki i frameworki oraz bądź na bieżąco z aktualizacjami zabezpieczeń i poprawkami związanymi z zanieczyszczeniem prototypów.
- Nagłówki bezpieczeństwa : Wdrażaj nagłówki bezpieczeństwa, takie jak Content Security Policy (CSP), aby kontrolować źródła, z których można ładować zasoby. Może to pomóc w zmniejszeniu ryzyka załadowania złośliwych skryptów manipulujących prototypami.

Łącząc rygorystyczne praktyki testowania, zasady bezpiecznego kodowania i stałą świadomość bezpieczeństwa, zarówno pentesterzy, jak i twórcy bezpiecznego kodu mogą przyczynić się do skutecznego minimalizowania luk w zabezpieczeniach aplikacji związanych z zanieczyszczeniem prototypów. Regularna aktualizacja wiedzy na temat pojawiających się zagrożeń i luk jest niezbędna, aby uniknąć potencjalnych zagrożeń.


W tym pomieszczeniu zbadaliśmy tajniki zanieczyszczenia prototypów, odkrywając, w jaki sposób atakujący wykorzystują luki w zabezpieczeniach, aby wykonywać szkodliwe działania, takie jakXSS,RCE, IDOSAtaki. Omawiając te techniki, podkreśliliśmy znaczenie zachowania czujności w celu zapobiegania potencjalnym zagrożeniom. Omówiliśmy również praktyczne środki zwiększające bezpieczeństwo aplikacji. Podsumowując, pamiętajmy, że **świadomość jest kluczem do ochrony aplikacji cyfrowych** . Bądź na bieżąco, aby uzyskać więcej interesujących treści dotyczących zaawansowanych ataków po stronie serwera. 

Dajcie nam znać, co myślicie o tym pokoju, na naszym kanale [Discord](https://discord.gg/tryhackme) lub [koncie X.](http://x.com/realtryhackme) Do zobaczenia.

Odpowiedz na poniższe pytania

Udało mi się ukończyć pokój.