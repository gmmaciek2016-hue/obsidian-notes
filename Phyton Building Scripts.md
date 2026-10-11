---

W sali [„Python: Koncepcje podstawowe”](https://tryhackme.com/room/pythoncoreconcepts) nauczyliśmy się pracy z typami danych, ciągami znaków, listami, słownikami, operatorami i pętlami. Teraz możemy przechowywać dane, analizować je, iterować po nich i podejmować decyzje w oparciu o warunki. To są podstawowe elementy. W tej sali nauczymy się, jak _łączyć_ te podstawowe elementy w prawdziwe programy.

Zastanów się nad różnicą między znajomością poszczególnych nut a umiejętnością zagrania utworu. W Core Concepts nauczyłeś się nut. W tej sali zagrasz utwór.

W szczególności omówimy cztery możliwości, które odróżniają fragment kodu od rzeczywistego skryptu: **funkcje** do organizowania i ponownego wykorzystywania logiki, **obsługę błędów** w celu budowania odporności, obsługę **plików wejścia/wyjścia** do odczytu danych wejściowych i zapisu danych wyjściowych oraz **biblioteki** do wykorzystywania kodu napisanego już przez innych. Na koniec połączymy wszystkie koncepcje z obu sal w jeden, działający **moduł sprawdzania siły hasła** : narzędzie, które ocenia hasła pod kątem wymagań dotyczących długości, reguł różnorodności znaków i wspólnych haseł.lista słów.

## Cele edukacyjne

Po ukończeniu tego pokoju będziesz:

- Definiowanie i wywoływanie funkcji z parametrami, wartościami zwracanymi i wartościami domyślnymi
- Zrozumieć zakres zmiennych
- Obsługuj błędy czasu wykonania za pomocą `try`/`except`
- Odczytuj i zapisuj do plików za pomocą menedżerów kontekstu ( `with`)
- Importuj moduły ze standardowej biblioteki Pythona
- Zainstaluj pakiety innych firm za pomocą`pip`
- Połącz wszystkie koncepcje w kompletny program mający znaczenie dla bezpieczeństwa

## Wymagania wstępne

Najlepiej będzie, jeśli zajmiesz się tym pokojem po skończeniu:

- [Python: prosta demonstracja](https://tryhackme.com/room/pythonsimpledemo)
- [Python: podstawowe koncepcje](https://tryhackme.com/room/pythoncoreconcepts)

## Dostęp do maszyny

Możesz śledzić proces, uruchamiając podłączoną maszynę wirtualną (VM). Program Visual Studio Code (VS Code) powinien otworzyć się automatycznie z gotową do użycia nowoczesną instalacją Pythona. Wszystkie przykładowe skrypty omówione w tym miejscu są zapisane w tym `/home/ubuntu/Building-Scripts/`katalogu. Zdecydowanie zachęcamy do uruchamiania, modyfikowania i eksperymentowania z każdym fragmentem kodu na komputerze. Maszyna wirtualna w miarę postępów w wykonywaniu zadań.

W miarę jak programy stają się coraz większe, zauważysz, że piszesz tę samą logikę w wielu miejscach. Rozważmy nasz program do sprawdzania siły hasła: możemy chcieć sprawdzić siłę hasła w jednej części programu, a następnie ponownie później, gdy użytkownik próbuje ponownie. Kopiowanie i wklejanie tego samego bloku kodu jest podatne na błędy i żmudne. Właśnie ten problem rozwiązują **funkcje .**

Jedną z analogii byłby automat sprzedający. Naciskasz przycisk (wywołanie **)** , opcjonalnie wrzucasz pieniądze ( **argumenty** ), a automat podaje ci napój ( **wartość zwracana** ). Wewnętrzny mechanizm jest ukryty; interesuje cię tylko to, co wchodzi i co wychodzi. Mówiąc językiem technicznym, funkcja to wielokrotnego użytku blok kodu, który przyjmuje dane wejściowe, wykonuje zadanie i opcjonalnie zwraca wynik.

## Definiowanie funkcji

W Pythonie funkcję definiuje się za pomocą `def`słowa kluczowego, po którym następuje nazwa funkcji, nawiasy zawierające **parametry** oraz dwukropek. Wcięty blok kodu pod nim to treść funkcji.

```python
def greet(name):
    print(f"Hello, {name}. Welcome to the system.")
```

Aby użyć (lub **wywołać** ) tę funkcję:

```python
greet("Alice")    # Hello, Alice. Welcome to the system.
greet("Bob")      # Hello, Bob. Welcome to the system.
```

Zdefiniowaliśmy funkcję raz, ale możemy ją wywoływać tyle razy, ile chcemy, podając różne argumenty.

## Parametry kontra argumenty

Parametr to nazwa zmiennej w definicji funkcji ( in ). **Argument** to faktyczna wartość przekazywana podczas wywołania funkcji ( in ). W codziennej komunikacji ludzie często używają tych terminów zamiennie, ale rozróżnienie to ma znaczenie podczas czytania dokumentacji **.**`name``def greet(name)``"Alice"``greet("Alice")`

## Wartości zwracane

Funkcje mogą zwracać wynik do wywołującego za pomocą `return`słowa kluczowego. To właśnie sprawia, że ​​funkcje są naprawdę potężne: potrafią coś obliczyć i przekazać do zapisania, wydrukowania lub wykorzystania w dalszych obliczeniach.

```python
def check_length(password, min_length):
    if len(password) >= min_length:
        return True
    else:
        return False

result = check_length("Tr0ub4dor", 8)
print(result)   # True
```

Gdy Python napotka `return`, natychmiast opuszcza funkcję i odsyła określoną wartość. Jeśli funkcja nie ma instrukcji, domyślnie `return`zwraca wartość .`None`

## Wiele parametrów

Funkcje mogą przyjmować dowolną liczbę parametrów rozdzielonych przecinkami:

```python
def score_password(password, common_list):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if password not in common_list:
        score += 1

    return score
```

Ta funkcja przyjmuje hasło i listę popularnych haseł, a następnie zwraca wynik liczbowy. Zwróć uwagę, jak wykorzystuje operatory `len()`, `.isdigit()`, `.isupper()`i `in`z podręcznika Core Concepts. Udoskonalimy i wykorzystamy tę funkcję w naszym zadaniu końcowym.

## Domyślne wartości parametrów

Możesz nadać parametrowi wartość domyślną, dzięki czemu osoba wywołująca nie będzie musiała jej podawać za każdym razem:

```python
def check_length(password, min_length=8):
    return len(password) >= min_length

print(check_length("short"))          # False   (uses default min_length of 8)
print(check_length("short", 4))       # True    (overrides default with 4)
```

## Zakres

Zmienne utworzone wewnątrz funkcji istnieją tylko w jej obrębie. Nie są dostępne z zewnątrz. Ta koncepcja nazywa się  **zakresem** .

```python
def calculate():
    result = 42     # local variable
    return result

calculate()
# print(result)    # This would cause an error: result is not defined here
```

Zakres zapobiega przypadkowemu zakłócaniu danych między funkcjami. Jest to funkcja, a nie ograniczenie.

Otwórz go `functions_demo.py`na podłączonej maszynie wirtualnej i uruchom. Skrypt definiuje `greet()`, `check_length()`, i `score_password()`. Wywołuje każdy z nich i wyświetla wyniki. Po uruchomieniu spróbuj utworzyć własną funkcję, `is_long_enough(password)`która zwraca wartość, `True`jeśli hasło ma 12 lub więcej znaków.

Co się dzieje, gdy użytkownik wpisuje tekst `"abc"`w wierszu poleceń, który oczekuje podania liczby? W Simple Demo nasza gra „Zgadnij liczbę” zawieszała się z powodu błędu „ `ValueError`ponieważ ” `int("abc")`nie jest prawidłową konwersją. W dopracowanym programie nie chcemy awarii, chcemy otrzymać pomocny komunikat i możliwość ponownej próby. Właśnie tutaj pojawia się **obsługa błędów .**

## Problem

Rozważ ten krótki scenariusz:

```python
text = input("Enter a number: ")   # user types "hello"
number = int(text)                  # CRASH: ValueError
print(f"You entered {number}")
```

Przykład uruchomienia tego skryptu może wyglądać następująco:

Terminal

```shell-session
Enter a number: hello
Traceback (most recent call last):
  File "demo.py", line 2, in <module>
    number = int(text)
ValueError: invalid literal for int() with base 10: 'hello'
```

Program zatrzymuje się całkowicie. Linia 3 nigdy się nie uruchamia. W narzędziu bezpieczeństwa skanującym tysiące hostów, pojedynczy nieoczekiwany sygnał wejściowy może zatrzymać całą operację.

## Blok `try`/`except`​

`try`Struktura / języka Python `except`pozwala na _podjęcie_ ryzykownej operacji i _wychwycenie_ błędu, jeśli wystąpi. Zamiast dopuścić do zawieszenia się programu, program poprosi użytkownika o ponowną próbę:

```python
try:
    text = input("Enter a number: ")
    number = int(text)
    print(f"You entered {number}")
except ValueError:
    print("That is not a valid number. Please try again.")
```

Przykład uruchomienia tego skryptu może wyglądać następująco:

Terminal

```shell-session
Enter a number: hello
That is not a valid number. Please try again.
```

Kod wewnątrz `try`jest uruchamiany jako pierwszy. Jeśli nie wystąpi błąd, Python całkowicie pomija blok. Jeśli jednak _wystąpi_`except` błąd , Python przechodzi do pasującego bloku i uruchamia ten kod, zamiast się zawieszać.`except`

## Typowe typy wyjątków

|Wyjątek|Kiedy to nastąpi|Przykład|
|---|---|---|
|`ValueError`|Nieprawidłowa konwersja typu|`int("abc")`|
|`FileNotFoundError`|Plik nie istnieje|`open("missing.txt")`|
|`ZeroDivisionError`|Dzielenie przez zero|`10 / 0`|
|`KeyError`|Nie znaleziono klucza słownika|`d["missing_key"]`|
|`IndexError`|Indeks listy poza zakresem|`mylist[99]`|

## Wychwytywanie wielu wyjątków

Różne błędy można obsługiwać na różne sposoby:

```python
try:
    filename = input("File to open: ")
    with open(filename) as f:
        data = f.read()
    port = int(data.strip())
except FileNotFoundError:
    print(f"Error: '{filename}' does not exist.")
except ValueError:
    print(f"Error: the file does not contain a valid number.")
```

## Generyczny`except`

Użycie `except Exception as e`funkcji wychwytuje większość wyjątków. Używaj jej oszczędnie, ponieważ może ukrywać błędy, o których warto wiedzieć:

```python
try:
    risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
```

Część `as e`przechowuje komunikat wyjątku w zmiennej `e`, którą można wydrukować w celu debugowania.

## Łączenie obsługi błędów z pętlami

Powszechnym i skutecznym wzorcem jest umieszczanie danych wprowadzanych przez użytkownika w pętli, dzięki czemu program pyta, aż do momentu podania prawidłowych danych:

```python
while True:
    try:
        age = int(input("Enter your age: "))
        break   # valid input received; exit the loop
    except ValueError:
        print("Invalid input. Please enter a whole number.")
```

Ten wzorzec jest niezbędny w narzędziach interaktywnych. Nasz moduł sprawdzający siłę hasła użyje go, aby upewnić się, że użytkownik wprowadzi niepuste hasło przed przetworzeniem.

Otwórz go na maszynie wirtualnej `error_demo.py`i uruchom. Skrypt celowo wyzwala kilka typów wyjątków i przechwytuje każdy z nich. Przeanalizuj, jak każdy blok `try`/ obsługuje swój konkretny typ błędu.`except`

W cyberbezpieczeństwie będziesz stale pracować z plikami: czytając listy słów w poszukiwaniu ataków siłowych, analizując pliki dziennika pod kątem podejrzanej aktywności lub zapisując wyniki skanowania w raporcie. Python sprawia, że ​​operacje na plikach są proste, a nowoczesne, najlepsze praktyki zapewniają ich bezpieczeństwo.

## Odczyt pliku

Wbudowana `open()`funkcja otwiera plik. Przekazujesz jej ścieżkę do pliku oraz **tryb** : `"r"`odczytu, `"w"`zapisu i `"a"`dodawania.

```python
f = open("passwords.txt", "r")
content = f.read()
print(content)
f.close()
```

Działa, ale jest pewien problem. Jeśli błąd wystąpi między `open()`a `close()`, plik pozostaje otwarty w pamięci. Z czasem wyciekające uchwyty plików mogą powodować problemy z wydajnością lub uszkodzenie danych. Python rozwiązuje ten problem za pomocą **menedżerów kontekstu** .

## Oświadczenie `with`(Menedżerowie kontekstu)

Zalecanym sposobem pracy z plikami w nowoczesnym Pythonie jest `with`polecenie. Automatycznie zamyka ono plik po zakończeniu wciętego bloku, nawet jeśli wystąpi błąd:

```python
with open("passwords.txt", "r") as f:
    content = f.read()

print(content)   # the file is already closed at this point
```

Od tego momentu zawsze używaj tej `with`opcji do operacji na plikach. Jest to bezpieczniejsze, bardziej przejrzyste i uważane za najlepszą praktykę w branży.

## Metody czytania

|Metoda|Zwroty|Najlepsze dla|
|---|---|---|
|`.read()`|Cały plik jako pojedynczy ciąg|Małe pliki przetwarzane jako jeden blok|
|`.readline()`|Następny pojedynczy wiersz|Przetwarzanie jednej linii na raz|
|`.readlines()`|Lista, w której każdy element jest jednym wierszem|Kiedy potrzebujesz wszystkich wierszy w formie listy|

Powszechnym i efektywnym pod względem pamięci wzorcem jest wykonywanie pętli bezpośrednio po obiekcie pliku:

```python
with open("common_passwords.txt", "r") as f:
    for line in f:
        password = line.strip()    # remove the trailing newline
        print(password)
```

To `.strip()`wywołanie jest tutaj kluczowe. Każdy wiersz w pliku tekstowym kończy się znakiem nowej linii ( `\n`). Bez niego zamiast `.strip()`, otrzymalibyśmy .`"password123\n"``"password123"`

## Ładowanie listy słów do listy

Na potrzeby naszego narzędzia do sprawdzania siły haseł chcemy załadować plik z popularnymi hasłami do listy Pythona, abyśmy mogli porównać go z danymi wprowadzonymi przez użytkownika:

```python
common_passwords = []

with open("common_passwords.txt", "r") as f:
    for line in f:
        common_passwords.append(line.strip())

print(f"Loaded {len(common_passwords)} common passwords.")
```

Teraz możemy użyć `in`operatora, aby sprawdzić, czy hasło jest słabe:

```python
if user_password in common_passwords:
    print("This password appears in the common-passwords list.")
```

## Zapisywanie do pliku

Aby utworzyć nowy plik lub nadpisać istniejący, użyj trybu `"w"`:

```python
with open("results.txt", "w") as f:
    f.write("Scan Results\n")
    f.write("============\n")
    f.write(f"Target: 192.168.1.1\n")
    f.write(f"Open ports: 22, 80, 443\n")
```

Aby dodać zawartość na końcu istniejącego pliku bez jej usuwania, użyj trybu `"a"`(append):

```python
with open("results.txt", "a") as f:
    f.write(f"Additional finding: port 3306 open\n")
```

## Typowe tryby plików

|Tryb|Opis|
|---|---|
|`"r"`|Odczyt (plik musi istnieć)|
|`"w"`|Zapisz (tworzy plik lub _nadpisuje_ istniejącą zawartość)|
|`"a"`|Dołącz (tworzy plik lub dodaje do istniejącej zawartości)|

Zachowaj ostrożność przy `"w"`wyborze trybu. Jeśli plik już istnieje, otwarcie go w trybie zapisu spowoduje natychmiastowe usunięcie całej jego zawartości. Jeśli chcesz zachować oryginalną zawartość i dodać do niej nowe elementy, zawsze używaj trybu `"a"`.

`common_passwords.txt`Na maszynie wirtualnej w katalogu zapisywany jest plik o nazwie „swordlist” `/home/ubuntu/Building-Scripts/`. Otwórz `files_demo.py`go i uruchom. Skrypt wczytuje listę słów, wyświetla liczbę znalezionych haseł i porównuje przykładowe hasło z listą. Następnie otwórz `common_passwords.txt`go w programie VS Code i zanotuj, ile wierszy zawiera.

W Simple Demo korzystaliśmy `import random`z dostępu do tej `random.randint()`funkcji. Ta pojedyncza linijka kodu pozwoliła nam generować liczby losowe bez konieczności samodzielnego pisania algorytmu. Koncepcja importowania gotowego kodu jest jedną z największych zalet Pythona.

## Czym jest biblioteka?

Biblioteka (nazywana również **modułem** lub **pakietem** **,** w zależności od kontekstu) to zbiór wstępnie napisanego kodu, który można importować do własnych programów. Analogią może być skrzynka z narzędziami: zamiast kuć klucz francuski z surowego metalu za każdym razem, gdy jest potrzebny, sięgasz do skrzynki z narzędziami i wyciągasz klucz francuski, który ktoś już wykonał. Mówiąc językiem technicznym, biblioteki oszczędzają konieczności wyważania otwartych drzwi.

## Importowanie bibliotek

Python oferuje kilka sposobów importowania:

```python
# Import the entire library
import os
print(os.getcwd())          # prints the current working directory

# Import a specific function
from datetime import datetime
now = datetime.now()
print(f"Current time: {now}")

# Import with an alias (nickname)
import datetime as dt
now = dt.datetime.now()
```

## Biblioteka standardowa Pythona

Python zawiera bogatą kolekcję wbudowanych modułów zwanych **biblioteką standardową** . Są one dostępne od razu, bez konieczności instalowania czegokolwiek. Oto kilka z nich, z którymi często się spotkasz:

|Moduł|Zamiar|Przykładowe użycie|
|---|---|---|
|`os`|Współdziałanie z systemem operacyjnym|Wyświetlanie listy plików, pobieranie zmiennych środowiskowych|
|`sys`|Parametry specyficzne dla systemu|Odczytaj argumenty wiersza poleceń|
|`random`|Generuj liczby losowe|Wybieraj losowe przedmioty, mieszaj listy|
|`datetime`|Praca z datami i godzinami|Znaczniki czasu, obliczenia czasu|
|`json`|Czytać i pisaćJSONdane|Analizowanie odpowiedzi API, plików konfiguracyjnych|
|`hashlib`|Haszowanie kryptograficzne|Skróty MD5, SHA-256|
|`string`|Stałe łańcuchowe i narzędzia|Dostęp `string.punctuation`,`string.digits`|

Moduł ten jest szczególnie przydatny w naszym narzędziu do sprawdzania siły hasła `string`. Zawiera stałe, takie jak `string.ascii_uppercase`, `string.digits`, i `string.punctuation`, których możemy użyć do sprawdzenia różnorodności znaków w haśle bez konieczności samodzielnego kodowania każdego znaku specjalnego:

```python
import string

password = "S3cure!Pass"

has_upper = any(c in string.ascii_uppercase for c in password)
has_digit = any(c in string.digits for c in password)
has_special = any(c in string.punctuation for c in password)

print(f"Uppercase: {has_upper}")     # True
print(f"Digit: {has_digit}")         # True
print(f"Special: {has_special}")     # True
```

## Instalowanie bibliotek innych firm za pomocą`pip`

Oprócz biblioteki standardowej, tysiące bibliotek stworzonych przez społeczność jest dostępnych w **Python Package Index (PyPI)** . Instaluje się je za pomocą `pip`menedżera pakietów Pythona, w terminalu:

```python
pip install requests
```

Po zainstalowaniu importujesz je tak jak każdy inny standardowy moduł biblioteczny:

```python
import requests

response = requests.get("https://tryhackme.com")
print(response.status_code)   # 200
```

## Biblioteki istotne dla bezpieczeństwa

W miarę postępów na ścieżce Jr Penetration Tester natkniesz się na następujące biblioteki w sali [Python dla pentesterów](https://tryhackme.com/room/pythonforcybersecurity) :

-  **requests**: wysyłaj żądania HTTP (web scraping, interakcja z API)
- **scapy** : tworzy, wysyła i podsłuchuje pakiety sieciowe
- **pwntools** : zestaw narzędzi do CTF i eksploatacji plików binarnych
- **paramiko** : Implementacja klienta i serwera SSH
- **beautifulsoup4** : parsowanie i wyodrębnianie danych ze stron HTML

Nie musisz ich teraz zapamiętywać. Kluczem jest to, że ekosystem Pythona pozwala przejść od „muszę wysłać pakiet” do „pakiet został wysłany” w zaledwie kilku linijkach kodu, ponieważ ktoś inny już stworzył trudne części.

Na maszynie wirtualnej otwórz `imports_demo.py`go i uruchom. Skrypt demonstruje importowanie z `os`, `datetime`, `string`i `hashlib`. Po uruchomieniu obserwuj, jak `hashlib`obliczaSHA-256hash. Spróbuj zmienić ciąg wejściowy i uruchomić ponownie, aby zobaczyć, jak hash całkowicie się zmieni.

Odpowiedz na poniższe pytania

Jak nazywa się menedżer pakietów Pythona służący do instalowania bibliotek innych firm?

W trakcie poprzednich zadań i w sali „Pojęcia podstawowe” poznaliśmy typy danych, ciągi znaków, listy, słowniki, operatory, pętle, funkcje, obsługę błędów, operacje wejścia/wyjścia plików oraz biblioteki. Teraz nadszedł czas, aby połączyć wszystkie te koncepcje w jeden, działający program: program **do sprawdzania siły hasła** .

Nasz program wykona następujące czynności:

1. Załaduj listę popularnych haseł z pliku ( `common_passwords.txt`)
2. Poproś użytkownika o podanie hasła
3. Sprawdź długość hasła, różnorodność znaków i obecność na liście wspólnej
4. Przypisz wynik siły i etykietę (Słaby, Umiarkowany lub Silny)
5. Wyświetl wynik i zapisz go w pliku dziennika

Zbudujmy go krok po kroku. Cały program jest zapisany w `password_checker.py`katalogu `/home/ubuntu/Building-Scripts/`na podłączonej maszynie wirtualnej.

## Krok 1: Importy i popularne hasła

```python
import string

def load_common_passwords(filepath):
    """Load a list of common passwords from a text file."""
    common = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                common.append(line.strip().lower())
    except FileNotFoundError:
        print(f"Warning: '{filepath}' not found. Skipping common-password check.")
    return common
```

Ta funkcja wykorzystuje wejście/wyjście pliku (zadanie 4), obsługę błędów (zadanie 3), listy i pętle (podstawowe koncepcje) oraz definicję funkcji (zadanie 2). Zwróć uwagę na blok `try`/ `except`: jeśli plik nie istnieje, program wyświetla ostrzeżenie i kontynuuje działanie zamiast się zawiesić. Wywołanie `.lower()`normalizuje każde hasło, dzięki czemu porównania nie uwzględniają wielkości liter.

## Krok 2: Funkcja punktacji

```python
def check_password(password, common_list):
    """Evaluate a password and return (score, feedback_list)."""
    score = 0
    feedback = []

    # Length checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")

    if len(password) >= 12:
        score += 1

    # Character variety checks
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if any(c in string.digits for c in password):
        score += 1
    else:
        feedback.append("Add at least one digit.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g., !, @, #).")

    # Common password check (overrides all other scoring)
    if password.lower() in common_list:
        score = 0
        feedback = ["This password is in the common-passwords list. Choose another."]

    return score, feedback
```

Ta funkcja wykorzystuje ciągi znaków i metody ciągów znaków, `in`operatora, logikę warunkową, listy oraz `string`moduł (zadanie 5). Zwraca _dwie_ wartości: wynik liczbowy i listę sugestii. W Pythonie można zwrócić wiele wartości oddzielonych przecinkami; wywołujący otrzymuje je jako **krotkę** .

## Krok 3: Program główny

```python
def main():
    strength_labels = {
        0: "Weak", 1: "Weak",
        2: "Moderate", 3: "Moderate",
        4: "Strong", 5: "Strong"
    }

    common_list = load_common_passwords("common_passwords.txt")

    while True:
        password = input("\nEnter a password to check (or 'quit' to exit): ")

        if password.lower() == "quit":
            print("Goodbye.")
            break

        if len(password) == 0:
            print("Password cannot be empty. Try again.")
            continue

        score, feedback = check_password(password, common_list)
        label = strength_labels.get(score, "Unknown")

        print(f"\nStrength: {label} ({score}/5)")

        if feedback:
            print("Suggestions:")
            for tip in feedback:
                print(f"  - {tip}")

        # Log the result (mask the actual password with asterisks)
        with open("password_log.txt", "a") as log:
            log.write(f"Password: {'*' * len(password)} | Strength: {label} ({score}/5)\n")

main()
```

W tej ostatniej sekcji wykorzystano słownik do mapowania etykiet, `while True`pętlę z operatorami `break`‚i’ `continue`, ciągi znaków ‚f-string’, zapis pliku w trybie dopisywania (zadanie 4) oraz wywołania funkcji (zadanie 2). Należy zauważyć, że nie logujemy samego hasła, lecz zamiast niego zapisujemy je gwiazdkami. Ze względów bezpieczeństwa nigdy nie przechowuj haseł w postaci zwykłego tekstu w logach.

## Uruchamianie programu

Terminal

```shell-session
$ python3 password_checker.py

Enter a password to check (or 'quit' to exit): password

Strength: Weak (0/5)
Suggestions:
  - This password is in the common-passwords list. Choose another.

Enter a password to check (or 'quit' to exit): Tr0ub4dor

Strength: Moderate (3/5)
Suggestions:
  - Add at least one special character (e.g., !, @, #).

Enter a password to check (or 'quit' to exit): C0mpl3x!Pass

Strength: Strong (5/5)

Enter a password to check (or 'quit' to exit): quit
Goodbye.
```

Każda koncepcja z obu sal jest obecna w tym programie. Zachęcamy do otwarcia się `password_checker.py`na Maszyna wirtualna, uruchom go, przeanalizuj kod i poeksperymentuj. Spróbuj dodać nowe kontrole (minimalna liczba znaków specjalnych, wykrywanie kolejnych powtórzeń znaków, odrzucanie słów ze słownika), aby jeszcze bardziej zwiększyć niezawodność modułu sprawdzającego.

W tej sali omówiliśmy możliwości, które pozwalają przekształcić fragmenty kodu w prawdziwe skrypty:

- **Funkcje** : definiowanie wielokrotnego użytku bloków kodu z `def`parametrami, wartościami zwracanymi, wartościami domyślnymi i zakresem
- **Obsługa błędów** : używanie `try`/ `except`do wychwytywania wyjątków i tworzenia odpornych programów, które nie zawieszają się po nieoczekiwanym wprowadzeniu danych
- **Wejście/wyjście pliku** : bezpieczne odczytywanie i zapisywanie plików za pomocą `with`menedżera kontekstu oraz zrozumienie trybów `"r"`, `"w"`, i`"a"`
- **Biblioteki** : importowanie standardowych modułów, takich jak `os`, `string`, i `hashlib`, oraz instalowanie pakietów innych firm za pomocą`pip`

Połączyliśmy wszystkie te koncepcje, tworząc narzędzie do sprawdzania siły hasła, praktyczne narzędzie, które odzwierciedla rodzaj przetwarzania tekstu i pracy weryfikacyjnej, jaką wykonujesz jako tester penetracyjny.

Patrząc wstecz na oba pokoje, zaczynałeś od pojedynczych nut, a skończyłeś na całej piosence. Teraz potrafisz czytać, modyfikować i pisać programy w Pythonie, które przetwarzają dane, podejmują decyzje, obsługują błędy, pracują z plikami i wykorzystują ekosystem bibliotek. Kolejnym krokiem jest zastosowanie tych umiejętności w kontekście bezpieczeństwa. Czas dołączyć do pokoju [Python: Pentesting Scripts](https://tryhackme.com/room/pythonpentestingscripts) , gdzie będziesz używać Pythona do enumeracji celów, interakcji z aplikacjami internetowymi, skanowania sieci i nie tylko.
