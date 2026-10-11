---

W sali [demonstracyjnej Python: Simple Demo](https://tryhackme.com/room/pythonsimpledemo) stworzyliśmy grę „Zgadnij liczbę” i poznaliśmy trzy podstawowe koncepcje programowania: **zmienne** , **instrukcje warunkowe** i `while` pętle. Już same te trzy koncepcje pozwoliły nam stworzyć działający, interaktywny program. Teraz czas na bardziej szczegółowe omówienie tematu.

Rozważ następujący scenariusz. Jesteś początkującym testerem penetracyjnym, a lider Twojego zespołu wręcza Ci plik tekstowy zawierający 10 000 nazw użytkowników zebranych podczas rekonesansu. Twoim zadaniem jest sprawdzenie każdej nazwy użytkownika pod kątem listy znanych domyślnych haseł, oznaczenie słabych danych uwierzytelniających i zapisanie wyników w pliku raportu. Wykonanie tego ręcznie zajęłoby kilka dni. Krótki skrypt w Pythonie może to zrobić w kilka sekund.

Aby napisać ten skrypt, potrzebujesz czegoś więcej niż zmiennych i `if`instrukcji. Musisz umieć pracować z **ciągami znaków** , przechowywać dane na **listach** i **słownikach** , korzystać z bogatego zestawu **operatorów** i opanować drugi rodzaj pętli: **`for`pętlę** . Właśnie to omówiono w tym pokoju.

Ten pokój i towarzyszący mu [Python: Tworzenie skryptów](https://tryhackme.com/room/pythonbuildingscripts) tworzą dwuczęściową serię. W pierwszym pokoju dowiesz się, jak Python obsługuje dane i przepływ sterowania. W drugim pokoju wykorzystasz te podstawy do pisania **funkcji** , obsługi **błędów** , pracy z **plikami** , importowania **bibliotek** i zbudowania od podstaw kompletnego **narzędzia do sprawdzania siły hasła** .

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Przegląd zmiennych, instrukcji warunkowych i pętli języka Python (omówione w Simple Demo)
- Praca z typami danych w Pythonie i wykonywanie konwersji typów
- Użyj sformatowanych ciągów znaków (f-stringów) i rozszerzonych operatorów przypisania
- Manipuluj ciągami znaków za pomocą wbudowanych metod
- Przechowuj i pobieraj dane za pomocą list i słowników
- Użyj operatorów porównania, logicznych, arytmetycznych i przynależności
- Iteruj dane, używając `for`pętli, `while`pętli i`range()`
- Przepływ pętli sterującej z `break`i`continue`

## Wymagania wstępne

Najlepiej będzie, jeśli zajmiesz się tym pokojem po skończeniu:

- [Python: prosta demonstracja](https://tryhackme.com/room/pythonsimpledemo)

## Dostęp do maszyny

Możesz śledzić, klikając `Start Machine`poniższy przycisk, aby uruchomić maszynę docelową (VM). Visual Studio Code (VS Code) powinien otworzyć się automatycznie z gotową do użycia nowoczesną instalacją Pythona. Wszystkie przykładowe skrypty omówione w tym pokoju są zapisane w tym `/home/ubuntu/Core-Concepts/`katalogu. Zdecydowanie zachęcamy do uruchamiania, modyfikowania i eksperymentowania z każdym fragmentem kodu naMaszyna wirtualnaw miarę postępów w wykonywaniu zadań.

> **Uwaga:** Jeśli ukończyłeś/aś już pokój [demonstracyjny Python: Simple Demo](https://tryhackme.com/room/pythonsimpledemo) , pierwsze trzy poniższe podsekcje będą Ci znane. Możesz je przejrzeć, aby odświeżyć swoją wiedzę, i przejść bezpośrednio do podsekcji „Co nowego” oraz pytań na końcu. Jeśli to Twoje pierwsze spotkanie z Pythonem, poświęć chwilę na zapoznanie się z każdą podsekcją, zanim przejdziesz dalej.

## Witaj świecie

Najprostszy program w Pythonie wyświetla tekst na ekranie za pomocą `print()`funkcji. W pokoju demonstracyjnym Python: Simple Demo informowaliśmy `print()`użytkownika, że ​​komputer wybrał tajną liczbę. Przyjrzyjmy się podstawom.

```python
# This is a comment. Python ignores lines starting with #.
print("Hello World")
```

Po uruchomieniu tego tekstu `Hello World`pojawi się on na ekranie. Kilka rzeczy, o których należy pamiętać:

- Linie zaczynające się od `#`to **komentarze** . Komputer je ignoruje; istnieją one po to, aby pomóc _ludziom_ zrozumieć kod.
- Funkcja `print()`zwraca wartość umieszczoną pomiędzy nawiasami.
- Tekst (nazywany **ciągiem znaków** ) musi być ujęty w cudzysłów `"double"`lub `'single'`.

Otwórz plik `hello.py`w programie VS Code na podłączonej maszynie wirtualnej, uruchom go i sprawdź, czy widzisz go `Hello World`w terminalu.

## Zmienne i typy danych

**Zmienne** pozwalają przechowywać i aktualizować dane. Jak widzieliśmy w Simple Demo, zapisaliśmy tajny numer w zmiennej o nazwie `secret`, a dane wprowadzone przez użytkownika w `guess`:

```python
food = "ice cream"   # a string (text)
money = 2000          # an integer (whole number)
```

W powyższym przykładzie zmienna `food`przechowuje ciąg znaków `"ice cream"`, natomiast `money`liczba całkowita `2000`. Zmienne są potężne, ponieważ można zmieniać ich wartości w całym programie:

```python
age = 30
age = age + 1
print(age)   # 31
```

Każda wartość w Pythonie ma **typ danych** . Podstawowe typy, które musisz znać, to:

|Typ|Nazwa|Przykład|Opis|
|---|---|---|---|
|`str`|Smyczkowy|`"hello"`|Tekst, znaki, symbole|
|`int`|Liczba całkowita|`42`|Liczby całkowite|
|`float`|Platforma|`3.14`|Liczby z przecinkami dziesiętnymi|
|`bool`|Boole'a|`True`/`False`|Logiczne włączanie/wyłączanie, wartości tak/nie|
|`list`|Lista|`[1, 2, 3]`|Uporządkowany zbiór przedmiotów|

Typ wartości można sprawdzić za pomocą `type()`:

```python
username = "admin"
port = 8080
print(type(username))   # <class 'str'>
print(type(port))       # <class 'int'>
```

Otwórz `types_demo.py`na maszynie wirtualnej i uruchom. Obserwuj wynik i spróbuj zmienić wartości zmiennych, aby zobaczyć, jak `type()`zareaguje.

## Instrukcje warunkowe i operatory logiczne

W Simple Demo użyliśmy `if`, `elif`, i `else`do porównania wyniku podanego przez użytkownika z liczbą tajną. Podsumujmy strukturę:

```python
age = 18
if age < 17:
    print("You are NOT old enough to drive")
else:
    print("You are old enough to drive")
```

Kluczowymi elementami są:

- Słowo `if`kluczowe, po którym następuje **warunek** i dwukropek`:`
- Wcięty blok kodu, który jest uruchamiany tylko wtedy, gdy spełniony jest warunek`True`
- Opcjonalny `else:`blok uruchamiany, gdy spełniony jest warunek`False`
- Jeden lub więcej `elif CONDITION:`bloków do dodatkowych sprawdzeń (jakich użyliśmy w naszej grze w zgadywanie)

**Operatory porównania** pozwalają na tworzenie warunków:

|Operator|Oznaczający|Przykład|
|---|---|---|
|`==`|Równy|`x == 5`|
|`!=`|Nie równy|`x != 5`|
|`<`|Mniej niż|`x < 5`|
|`>`|Większy niż|`x > 5`|
|`<=`|Mniejsze lub równe|`x <= 5`|
|`>=`|Większy lub równy|`x >= 5`|

**Operatorzy logiczni** łączą wiele warunków:

|Operator|Oznaczający|Przykład|
|---|---|---|
|`and`|Prawda tylko wtedy, gdy _obie_ strony są prawdziwe|`x > 0 and x < 100`|
|`or`|Prawda, jeśli _przynajmniej jedna_ strona jest prawdziwa|`x == 1 or x == 10`|
|`not`|Odwraca wartość logiczną|`not is_locked`|

Rozważmy następujący przykład:

```python
name = "bob"
hungry = True

if name == "bob" and hungry == True:
    print("Bob is hungry")
elif name == "bob" and not hungry:
    print("Bob is not hungry")
else:
    print("Not sure who this is or if they are hungry")
```

Warto powtórzyć istotną różnicę: `=`operator **przypisania** (zapisuje wartość w zmiennej), a `==`operator **równości** (porównuje dwie wartości). Mylenie tych dwóch pojęć to jeden z najczęstszych błędów początkujących.

## Co nowego: konwersja typów i ciągi znaków f

Jeśli ukończyłeś/aś kurs Simple Demo, powyższy materiał powinien wydawać się znajomy. Reszta tej sali wprowadza koncepcje wykraczające poza to, co omówiliśmy w grze w zgadywanki. Zacznijmy od dwóch usprawnień w pracy ze zmiennymi.

**Konwersja typu**

Jak widzieliśmy w Simple Demo, `input()`funkcja zawsze zwraca ciąg znaków. Gdy użytkownik wpisał coś `10`w wierszu poleceń, Python zapisał to jako tekst `"10"`, a nie liczbę `10`. Użyliśmy `int()`go do konwersji. Python oferuje kilka wbudowanych funkcji konwersji:

|Funkcjonować|Konwertuje do|Przykład|
|---|---|---|
|`int()`|Liczba całkowita|`int("42")`daje`42`|
|`float()`|Platforma|`float("3.14")`daje`3.14`|
|`str()`|Smyczkowy|`str(42)`daje`"42"`|
|`bool()`|Boole'a|`bool(0)`daje`False`|

Rozważmy następujący przykład:

```python
text = input("Enter a port number: ")    # user types 443
print(type(text))                         # <class 'str'>

port = int(text)                          # convert to integer
print(type(port))                         # <class 'int'>
print(port + 1)                           # 444
```

Bez `int()`konwersji `text + 1`pojawiłby się błąd, ponieważ Python nie potrafi dodać liczby do fragmentu tekstu.

**Sformatowane ciągi znaków (f-stringi)**

W Simple Demo użyliśmy przecinków w środku `print()`, aby wyświetlić zmienne obok tekstu, na przykład `print("You got it in", tries, "tries!")`. To podejście działa, ale współczesny Python oferuje czystszą alternatywę, zwaną **f-stringami** (sformatowanymi literałami ciągów). f-string zaczyna się od litery `f`przed cudzysłowem otwierającym i pozwala na osadzanie zmiennych bezpośrednio w nawiasach klamrowych:

```python
username = "admin"
port = 443

# Old approach (comma-separated, as used in Simple Demo)
print("User", username, "is on port", port)

# Modern approach (f-string)
print(f"User {username} is on port {port}")
```

Obie linijki generują ten sam wynik: `User admin is on port 443`. Wersja z ciągiem znaków jest łatwiejsza do odczytania i zapewnia precyzyjną kontrolę nad odstępami i formatowaniem. Będziemy używać ciągów znaków w pozostałej części tego pomieszczenia.

**Rozszerzone operatory przypisania**

W Simple Demo napisaliśmy `tries = tries + 1`instrukcję inkrementacji licznika. Python udostępnia skrót dla tego wzorca zwany **rozszerzonym przypisaniem** :

```python
count = 0
count += 1    # same as count = count + 1
count -= 1    # same as count = count - 1
count *= 2    # same as count = count * 2
count /= 4    # same as count = count / 4
```

Te skróty skracają kod i zmniejszają ryzyko literówek. Są `+=`często używane w pętlach i licznikach.

Otwórz `fstrings_demo.py`w załącznikuMaszyna wirtualna, uruchom go i zobacz, jak w praktyce działają f-stringi i rozszerzone operatory przypisania.

Czy zdarzyło Ci się kiedyś wypełnić formularz online i otrzymać komunikat o błędzie „hasło musi zawierać co najmniej jedną wielką literę”? Za tym komunikatem kryje się fragment kodu, który sprawdza hasło znak po znaku. W Pythonie ta inspekcja jest obsługiwana przez **metody stringów** , a ich opanowanie jest niezbędne w przypadku każdego skryptu przetwarzającego tekst. W kontekście bezpieczeństwa oznacza to niemal każdy skrypt, jaki kiedykolwiek napiszesz.

Ciąg **znaków** to sekwencja znaków ujęta w cudzysłowy. W przypadku tekstu wielowierszowego można używać pojedynczych ( `'hello'`), podwójnych ( `"hello"`) lub potrójnych ( ). Python traktuje je wszystkie jako ten sam typ danych.`"""hello"""`

## Długość struny

Funkcja `len()`zwraca liczbę znaków w ciągu. To podstawowa kontrola w wielu skryptach bezpieczeństwa: czy hasło jest wystarczająco długie? Czy dane wejściowe mieszczą się w oczekiwanych granicach?

```python
password = "Tr0ub4dor"
length = len(password)
print(f"Password length: {length}")   # Password length: 9
```

## Indeksowanie i dzielenie ciągów znaków

Każdy znak w ciągu zajmuje ponumerowaną pozycję zwaną **indeksem** . Indeksy w Pythonie zaczynają się od `0`, a nie od `1`. Rozważmy ciąg `"Python"`:

|Indeks|0|1|2|3|4|5|
|---|---|---|---|---|---|---|
|Charakter|P|y|T|H|o|N|

```python
word = "Python"
print(word[0])     # P   (first character)
print(word[5])     # n   (last character)
print(word[-1])    # n   (negative index counts from the end)
```

**Wycinek** pozwala wyodrębnić fragment ciągu za pomocą składni `string[start:end]`. `start`Indeks jest uwzględniany; `end`indeks jest wykluczany.

```python
word = "Python"
print(word[0:3])   # Pyt   (characters at index 0, 1, 2)
print(word[2:])    # thon  (from index 2 to the end)
print(word[:4])    # Pyth  (from the start to index 3)
```

## Przydatne metody łańcuchowe

Ciągi znaków w Pythonie zawierają dziesiątki wbudowanych metod. Oto te, po które będziesz sięgać najczęściej:

|Metoda|Co to robi|Przykład|Wynik|
|---|---|---|---|
|`.upper()`|Konwertuje na wielkie litery|`"hello".upper()`|`"HELLO"`|
|`.lower()`|Konwertuje na małe litery|`"HELLO".lower()`|`"hello"`|
|`.strip()`|Usuwa spacje początkowe/końcowe|`" hi ".strip()`|`"hi"`|
|`.replace(a, b)`|Zastępuje wszystkie wystąpienia `a`słowem`b`|`"cat".replace("c", "b")`|`"bat"`|
|`.split(sep)`|Dzieli się na listę przy każdym`sep`|`"a,b,c".split(",")`|`["a", "b", "c"]`|
|`.startswith(x)`|Sprawdza, czy ciąg zaczyna się od`x`|`"http://".startswith("http")`|`True`|
|`.endswith(x)`|Sprawdza, czy ciąg kończy się na`x`|`"file.txt".endswith(".txt")`|`True`|
|`.count(x)`|Zlicza wystąpienia`x`|`"banana".count("a")`|`3`|

## Sprawdzanie postaci

W przypadku zadań takich jak walidacja hasła musimy wiedzieć, czy znak jest cyfrą, wielką literą, czy czymś innym. Python udostępnia metody właśnie do tego celu:

```python
char = "A"
print(char.isupper())    # True
print(char.islower())    # False
print(char.isdigit())    # False
print(char.isalpha())    # True   (is it a letter?)
print(char.isalnum())    # True   (is it a letter or digit?)
```

Metody te zwracają wartość logiczną ( `True`lub `False`), co czyni je idealnymi do użycia wewnątrz `if`instrukcji. Połączymy je z pętlami później w tym pomieszczeniu, aby przeskanować każdy znak w ciągu.

## Operator`in`​

Operator Pythona `in`sprawdza, czy podciąg istnieje w dłuższym ciągu. Zwraca on wartość `True`or `False`:

```python
url = "https://tryhackme.com/room/pythoncoreconcepts"

print("tryhackme" in url)     # True
print("hackthebox" in url)    # False
print("https" in url)         # True
```

Operator ten `in`jest jednym z najbardziej wszechstronnych narzędzi w Pythonie. Spotkamy się z nim ponownie w kolejnym zadaniu na listach i słownikach.

Otwórz `strings_demo.py`na maszynie wirtualnej. Skrypt zawiera kilka operacji na ciągach znaków. Uruchom go i przeanalizuj jego wyniki. Następnie zmień zmienną `test_string`u góry na swoją własną nazwę i uruchom ponownie, aby zobaczyć, jak zmieni się wynik.

Wyobraź sobie, że jesteś odpowiedzialny za monitorowanie sieci. Masz listę adresów IP do przeskanowania, zbiór otwartych portów dla każdego hosta oraz mapowanie numerów portów na nazwy usług (port 22 toSSH, port 80 toHTTPitd.). Przechowywanie każdego z nich w osobnej zmiennej byłoby niepraktyczne. Python oferuje nam dwie potężne **struktury danych** do obsługi zbiorów danych: **listy** i **słowniki** .

## Listy

Lista to uporządkowany zbiór elementów ujętych w nawiasy kwadratowe. Elementy **mogą** mieć dowolny typ danych, a lista zachowuje ich kolejność.

```python
ports = [22, 80, 443, 8080]
usernames = ["admin", "root", "guest"]
mixed = ["server1", 443, True]
```

**Dostęp do elementów listy i ich modyfikowanie**

Listy używają tego samegoindeksowaniesystem jako ciągi znaków. Pierwszy element znajduje się pod indeksem `0`:

```python
ports = [22, 80, 443, 8080]

print(ports[0])      # 22
print(ports[-1])     # 8080   (last element)
print(ports[1:3])    # [80, 443]   (slicing works on lists too)
```

Możesz zmienić element, przypisując nową wartość do jego indeksu:

```python
ports[0] = 2222
print(ports)         # [2222, 80, 443, 8080]
```

**Metody listy wspólnej**

|Metoda|Co to robi|Przykład|
|---|---|---|
|`.append(x)`|Dodaje `x`na koniec|`ports.append(3306)`|
|`.remove(x)`|Usuwa pierwsze wystąpienie`x`|`ports.remove(80)`|
|`.pop(i)`|Usuwa i zwraca element o indeksie`i`|`ports.pop(0)`|
|`.sort()`|Sortuje listę w kolejności rosnącej|`ports.sort()`|
|`.reverse()`|Odwraca kolejność listy|`ports.reverse()`|
|`len(list)`|Zwraca liczbę elementów|`len(ports)`|

Operator `in`, który wprowadziliśmy dla ciągów znaków, działa również na listach:

```python
common_passwords = ["123456", "password", "admin", "letmein"]

if "password" in common_passwords:
    print("This password is in the common list.")
```

## Słowniki

Słownik przechowuje dane jako **pary klucz-wartość** ujęte w nawiasy klamrowe. Analogią może być słownik fizyczny: wyszukujesz _słowo_ (klucz), aby znaleźć jego **definicję** _(_ wartość). Mówiąc językiem technicznym, słownik pozwala powiązać jeden element danych z drugim w celu szybkiego wyszukiwania.

```python
services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL"
}
```

**Uzyskiwanie dostępu do wartości słownika**

Wartość można pobrać poprzez podanie jej klucza w nawiasach kwadratowych:

```python
print(services[22])     # SSH
print(services[443])    # HTTPS
```

**Dodawanie, aktualizowanie i usuwanie wpisów**

```python
# Add a new entry
services[8080] = "HTTP-Alt"

# Update an existing entry
services[22] = "OpenSSH"

# Remove an entry
del services[3306]

print(services)
# {22: 'OpenSSH', 80: 'HTTP', 443: 'HTTPS', 8080: 'HTTP-Alt'}
```

**Sprawdzanie kluczy**

```python
if 22 in services:
    print(f"Port 22 runs {services[22]}")
```

**Przydatne metody słownikowe**

|Metoda|Zwroty|
|---|---|
|`.keys()`|Wszystkie klucze w słowniku|
|`.values()`|Wszystkie wartości w słowniku|
|`.items()`|Wszystkie pary klucz-wartość jako krotki|
|`.get(key, default)`|Wartość dla `key`lub `default`jeśli klucz nie istnieje|

Ta `.get()`metoda jest szczególnie użyteczna, ponieważ dostęp do nieistniejącego klucza za pomocą nawiasów kwadratowych powoduje błąd, jednocześnie `.get()`umożliwiając podanie bezpiecznego rozwiązania awaryjnego:

```python
result = services.get(9999, "Unknown")
print(result)   # Unknown
```

## Patrząc w przyszłość

W sali towarzyszącej, [Python: Tworzenie skryptów](https://tryhackme.com/room/pythonbuildingscripts) , zbudujemy narzędzie do sprawdzania siły haseł, które przechowuje listę popularnych słabych haseł pobranych z pliku i używa słownika do mapowania każdego poziomu siły na opisową etykietę. Obie struktury danych staną się niezbędnymi narzędziami w Twoim zestawie narzędzi do tworzenia skryptów bezpieczeństwa.

Otwórz `lists_dicts_demo.py`skrypt na maszynie wirtualnej i uruchom go. Skrypt demonstruje listy i słowniki, korzystając z powyższych przykładów. Po uruchomieniu dodaj nową parę port-usługa do `services`słownika w skrypcie i uruchom go ponownie, aby sprawdzić, czy zmiana jest widoczna w wynikach.

W Simple Demo użyliśmy operatorów porównania, takich jak `<`i , `>`aby porównać wynik próby użytkownika z liczbą tajną. W tym zadaniu rozszerzyliśmy nasz zestaw narzędzi o nowe operatory arytmetyczne i przyjrzeliśmy się bliżej temu, jak Python ocenia warunki złożone.

## Nowe operatory arytmetyczne

Znasz już dodawanie ( `+`), odejmowanie ( `-`), mnożenie ( `*`) i dzielenie ( `/`). Dodajmy do zestawu jeszcze trzy:

|Operator|Nazwa|Przykład|Wynik|
|---|---|---|---|
|`**`|Wykładnik potęgowy|`2 ** 8`|`256`|
|`//`|Podział piętra|`7 // 2`|`3`|
|`%`|Moduł (reszta)|`7 % 2`|`1`|

Operator modulo ( ) zwraca resztę z dzielenia. Jest powszechnie używany do sprawdzania **,**`%` czy liczba jest parzysta, czy nieparzysta: jeśli `number % 2 == 0`, liczba jest parzysta.

**Funkcja dzielenia podłogowego** ( `//`) dzieli, a następnie zaokrągla w dół do najbliższej liczby całkowitej. Zwykłe dzielenie ( `/`) zawsze zwraca liczbę zmiennoprzecinkową: `7 / 2`daje `3.5`, podczas gdy `7 // 2`daje `3`.

**Operator wykładnika** ( ) `**`podnosi liczbę po lewej stronie do potęgi liczby po prawej stronie. Na przykład `2 ** 8`oblicza 2 podniesione do potęgi ósmej, czyli `256`. W kontekście bezpieczeństwa często spotyka się to przy omawianiu rozmiarów kluczy: klucz 128-bitowy ma `2 ** 128`możliwe kombinacje.

## Operator członkostwa:`in`

W poprzednich zadaniach przedstawiliśmy `in`ciągi znaków i listy. Zasługuje on na szczególną uwagę, ponieważ działa z niemal każdym typem kolekcji w Pythonie i będzie odgrywał kluczową rolę w wielu skryptach bezpieczeństwa.

```python
# Checking if a password is in a list of common passwords
common = ["123456", "password", "qwerty", "letmein"]
user_password = "qwerty"

if user_password in common:
    print("This password is too common.")
```

Można to zanegować za pomocą `not in`:

```python
if user_password not in common:
    print("Good. This password is not in the common list.")
```

## Łączenie operatorów w praktyce

Rozważmy praktyczny przykład. Hasło można uznać za umiarkowane, jeśli ma co najmniej 8 znaków _i_ zawiera co najmniej jedną cyfrę:

```python
password = "Tr0ubador"
length = len(password)
has_digit = any(char.isdigit() for char in password)

if length >= 8 and has_digit:
    print("Moderate strength")
elif length >= 8 or has_digit:
    print("Weak, but has some merit")
else:
    print("Very weak")
```

Nie martw się, jeśli `any()`linia wygląda nieznajomo; wrócimy do niej w sali towarzyszącej, gdy będziemy omawiać funkcje. Na razie skup się na tym, jak `and`wymaga spełnienia obu warunków, a `or`wymaga spełnienia tylko jednego.

Otwórz `operators_demo.py`w załącznikuMaszyna wirtualnaSkrypt przeprowadzi Cię przez każdego operatora z wydrukowanymi przykładami. Uruchom go i obserwuj wynik.

W Simple Demo użyliśmy `while`pętli, która pytała użytkownika o kolejne odpowiedzi, aż do znalezienia sekretnej liczby. Pętla `while`powtarza się tak długo, jak długo warunek jest spełniony; sprawdza się idealnie, gdy liczba iteracji zależy od pewnego warunku w czasie wykonywania. Python oferuje drugi typ pętli, pętlę **`for`,** która jest przeznaczona do iterowania po sekwencji elementów. Przyjrzyjmy się obu.

## Krótkie podsumowanie: `while`pętle

Pętla `while`działa tak długo, jak jej warunek spełnia `True`:

```python
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    password = input("Enter password: ")
    attempts += 1
    print(f"Attempt {attempts} of {max_attempts}")
```

Ta pętla prosi o hasło maksymalnie 3 razy. Po `attempts`osiągnięciu 3, warunek `attempts < max_attempts`zmienia się na `False`, a pętla się zatrzymuje.

## Pętla`for`​

Rozważmy przypadek, gdy masz listę adresów IP i chcesz przetworzyć każdy z nich. Dokładnie wiesz, ile jest elementów i chcesz odwiedzić każdy z nich po kolei. To jest idealny punkt dla `for`pętli.

```python
targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

for ip in targets:
    print(f"Scanning {ip}...")
```

```python
# The output would be:
Scanning 192.168.1.1...
Scanning 192.168.1.2...
Scanning 192.168.1.3...
```

Rozłóżmy to na czynniki. Zmienna `ip`przyjmuje wartość każdego elementu listy `targets`, po jednym na raz. W pierwszej iteracji `ip`jest to `"192.168.1.1"`; w drugiej jest to `"192.168.1.2"`; i tak dalej. Pętla kończy się, gdy każdy element zostanie odwiedzony.

## Iterowanie po ciągach znaków

Ciąg znaków jest również sekwencją, więc można go przeglądać znak po znaku. Właśnie tego potrzebujemy do zadań takich jak weryfikacja hasła:

```python
password = "S3cure!"

for char in password:
    if char.isdigit():
        print(f"Found digit: {char}")
    elif char.isupper():
        print(f"Found uppercase: {char}")
```

```python
# The output would be:
Found uppercase: S
Found digit: 3
```

## Funkcja`range()`​

Czasami potrzebujesz pętli, która wykona się określoną liczbę razy bez predefiniowanej listy. Funkcja `range()`generuje sekwencję liczb:

```python
# range(stop): 0 to stop-1
for i in range(5):
    print(i)       # prints 0, 1, 2, 3, 4

# range(start, stop): start to stop-1
for i in range(1, 6):
    print(i)       # prints 1, 2, 3, 4, 5

# range(start, stop, step): with custom increment
for i in range(0, 20, 5):
    print(i)       # prints 0, 5, 10, 15
```

W programowaniu liczenie często zaczyna się od 0. W rezultacie `range(5)`otrzymujemy pięć liczb: 0, 1, 2, 3 i 4.

## Iterowanie po słownikach

Jak wspomnieliśmy w zadaniu 4, słowniki mają metody `.keys()`, `.values()`, i `.items()`. Stają się one szczególnie przydatne w `for`pętlach wewnętrznych:

```python
services = {22: "SSH", 80: "HTTP", 443: "HTTPS"}

# Loop through both keys and values
for port, name in services.items():
    print(f"Port {port} = {name}")
```

```python
# The output would be:
Port 22 = SSH
Port 80 = HTTP
Port 443 = HTTPS
```

## `break`I`continue`

Dwa słowa kluczowe umożliwiają szczegółową kontrolę wewnątrz pętli:

- `break`natychmiast całkowicie opuszcza pętlę.
- `continue`pomija resztę bieżącej iteracji i przechodzi do następnej.

```python
# Stop scanning as soon as we find port 443
for port in [22, 80, 443, 8080]:
    if port == 443:
        print(f"Port {port} found. Stopping scan.")
        break
    print(f"Checked port {port}")
```

```python
# The output would be:
Checked port 22
Checked port 80
Port 443 found. Stopping scan.
```

Zauważ, że `8080`nigdy tego nie sprawdzono, ponieważ `break`pętla została zakończona natychmiast po znalezieniu `443`.

```python
# Skip blank lines when processing a file
lines = ["admin", "", "root", "", "guest"]

for line in lines:
    if line == "":
        continue       # skip empty strings
    print(f"Processing: {line}")
```

```python
# The output would be:
Processing: admin
Processing: root
Processing: guest
```

## Wybór pomiędzy `for`a`while`

Ogólna zasada: używaj `for`pętli, gdy znasz z góry liczbę iteracji (lista do przetworzenia, zakres liczb, ciąg znaków do przeskanowania). Używaj pętli, `while`gdy liczba iteracji zależy od warunku, który zmienia się podczas wykonywania (np. oczekiwanie na poprawne dane wejściowe lub ponawianie próby aż do nawiązania połączenia).

Otwórz i uruchom skrypt na maszynie wirtualnej `loops_demo.py`. Skrypt demonstruje `for`pętle, `while`pętle `range()`, `break`, i `continue`w sekwencji. Przeanalizuj wynik i spróbuj dodać nową pętlę, która drukuje każdą liczbę parzystą od 0 do 20, używając `range()`kroku 2.

W tej sali omówiliśmy podstawy przepływu danych i sterowania w Pythonie:

- **Typy danych i konwersja typów** : zrozumienie `str`, `int`, `float`i `bool`konwersja między nimi za pomocą `int()`, `str()`, `float()`i`bool()`
- **Sformatowane ciągi znaków** : ciągi znaków f dla czystego i czytelnego wyjścia
- **Ciągi** : indeksowanie, wycinanie i potężne wbudowane metody, takie jak `.split()`, `.strip()`, `.lower()`, `.isdigit()`i`.isupper()`
- **Listy i słowniki** : przechowywanie zbiorów danych i efektywne ich wyszukiwanie za pomocą indeksowania, `.append()`, `.get()`i `in`operatora
- **Operatorzy** : arytmetyczny ( `+`,,,,,,, `-`) , porównania ( ,,, ) , logiczny ( ,, ) `*`i operator przynależności`/``//``%``**``==``!=``<``>``and``or``not``in`
- **Pętle** : `for`pętle sekwencji i zakresów, `while`pętle powtórzeń opartych na warunkach, plus `break`i`continue`

Posiadasz już słownictwo i mechanizmy pozwalające na czytanie, rozumienie i modyfikowanie programów w Pythonie. Następnym krokiem jest nauczenie się, jak _tworzyć_ z tych programów struktury wielokrotnego użytku, odporne na błędy i praktyczne. Czas dołączyć do sali [„Python: Tworzenie skryptów”](https://tryhackme.com/room/pythonbuildingscripts) , gdzie zdefiniujesz **funkcje** , obsłużysz **błędy** , odczytasz i zapiszesz **pliki** , zaimportujesz **biblioteki** i zbudujesz od podstaw kompletny program **do sprawdzania siły hasła .**
