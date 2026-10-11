---

Hasła to najpopularniejszy mechanizm uwierzytelniania w internecie, a jednocześnie jedna z najpewniejszych dróg ataku na system. Niezależnie od tego, czy mamy do czynienia z wyciekiem bazy danych, przechwyconym połączeniem sieciowym, czy hashem wyodrębnionym z zainfekowanego komputera, umiejętność odzyskania tekstu jawnego z hasha jest podstawową umiejętnością zespołu red team.

W tej sali poznamy łamanie haseł od podstaw: jak hasła są przechowywane, jak zidentyfikować algorytm generujący dany skrót, jakie narzędzia i techniki zastosować oraz kiedy je zastosować. Na koniec złamiemy zestaw prawdziwych skrótów, stosując dokładnie taki sam schemat działania, jaki stosowałby tester penetracyjny podczas realizacji zadania.

## Cele edukacyjne

- Wyjaśnij, jak hasła są przechowywane w postaci skrótów i do czego służy solenie
- Identyfikuj popularne typy skrótów na podstawie ich cech wizualnych i za pomocą dedykowanych narzędzi
- Użyj **hashida** , aby zawęzić nieznane formaty hashów
- Przeprowadź ataki słownikowe za pomocą **Hashcat** i**Joh the Ripper
- Zastosuj ataki oparte na regułach i maskach, aby rozszerzyć zasięg poza standardlista słów
- Wybierz odpowiednie narzędzie i technikę dla danego skrótu i ​​scenariusza

## Wymagania wstępne

- [LinuxPodstawy Część 1](https://tryhackme.com/room/linuxfundamentalspart1) : Nawigacja po wierszu poleceń, czytanie i zapisywanie plików
- [Podstawy haszowania](https://tryhackme.com/room/hashingbasics) : Czym są funkcje haszujące i jakie są ich podstawowe właściwości
- [Wprowadzenie do list słów](https://tryhackme.com/room/introductiontowordlists) : CeWL, crunch iHydrado tworzenia i używania ukierunkowanych list słów

Przechowywanie haseł w postaci zwykłego tekstu to katastrofalny błąd, ale wciąż się zdarza. Gdy baza danych przechowuje dane `password:hunter2`w postaci dosłownej, pojedyncze włamanie natychmiast ujawnia wszystkie konta, bez konieczności ich łamania. Standardowym rozwiązaniem jest przechowywanie **skrótu** hasła, a nie samego hasła.

Gdy użytkownik się loguje, system haszuje przesłane hasło i porównuje je z zapisanym hashem. Jeśli hasła są zgodne, dostęp jest przyznawany. Oryginalnego hasła nigdy nie trzeba nigdzie przechowywać.

## Dlaczego funkcja skrótu jest w tym przypadku przydatna

![Schemat blokowy uwierzytelniania logowania. Użytkownik przesyła hasło do systemu logowania, który je haszuje i porównuje z hashem zapisanym w bazie danych haseł. Jeśli hashe są zgodne, dostęp jest udzielany; jeśli nie, dostęp jest odmawiany.](https://cdn-images.tryhackme.com/user-uploads/6808d44047ac5684351c94da/room-content/6808d44047ac5684351c94da-1779195455402.png)

Kryptograficzna funkcja skrótu ma cztery właściwości, które czynią ją odpowiednią do przechowywania haseł:

- **Jednokierunkowa:** Nie ma możliwości cofnięcia hasha do pierwotnego wejścia. Możemy iść dalej jedynie hashując kandydata i porównując go.
- **Deterministyczny:** te same dane wejściowe zawsze generują te same dane wyjściowe.  `hash("hunter2")`Zawsze zwróci tę samą wartość, na dowolnej maszynie, za każdym razem.
- **Dane wyjściowe o stałej długości:** Niezależnie od długości danych wejściowych, dane wyjściowe mają zawsze ten sam rozmiar. MD5 zawsze generuje 32 znaki szesnastkowe, niezależnie od tego, czy dane wejściowe są  `a`ciągiem 10 000 znaków.
- **Odporność na kolizje:** Powinno być obliczeniowo niewykonalne, aby dwa różne dane wejściowe wygenerowały ten sam skrót. Gdy algorytm traci tę właściwość (jakMD5i SHA-1), ze względów bezpieczeństwa uznaje się je za złamane.

## Typowe algorytmy haszujące

|Algorytm|Długość wyjściowa|Nadal używasz haseł?|Notatki|
|---|---|---|---|
|MD5|128 bitów (32 znaki szesnastkowe)|NIE|Szybki, podatny na kolizje, szeroko popękany|
|SHA-1|160 bitów (40 znaków szesnastkowych)|NIE|Szybszy niż SHA-256, przestarzały|
|SHA-256|256 bitów (64 znaki szesnastkowe)|Czasami|Lepszy niżMD5/SHA-1, ale nadal szybki|
|NTLM|128 bitów (32 znaki szesnastkowe)|Tak (starsze uwierzytelnianie systemu Windows)|Oparty na MD4, używany do skrótów kont systemu Windows|
|bcrypt|~ 60 znaków, prefiks $2*$|Tak, zalecane|Celowo powolny, konfigurowalny pod względem kosztów|
|Argon2|Zmienny|Tak, zalecane|Nowoczesny standard, duża pamięć|

Wszystko sprowadza się do **prędkości** .MD 5SHA-1 i SHA-256 zostały zaprojektowane do sprawdzania integralności plików i podpisów cyfrowych, a nie do przechowywania haseł. Nowoczesny procesor graficzny może obliczyć miliardyMD5haszy na sekundę. bcrypt jest inny: został stworzony specjalnie do haseł, a jego koszt sprawia, że ​​obliczenia są celowo kosztowne. Atakujący przeszukujący listę słów jest spowolniony tak samo, jak serwer weryfikujący logowanie – i o to właśnie chodzi.

## Solenie

Nawet przy silnym algorytmie problem pozostaje: jeśli dwóch użytkowników ma to samo hasło, ich zapisane skróty będą identyczne. Atakujący, który wstępnie oblicza skróty dla wspólnych haseł, tzw. **tablicę tęczową** , może natychmiast wyszukać pasujące hasła bez konieczności przeprowadzania jakichkolwiek prób złamania zabezpieczeń.

**Solenie** rozwiązuje ten problem. Sól to unikalny, losowy ciąg znaków generowany dla każdego użytkownika i łączony z jego hasłem przed haszowaniem:

```text
stored_value = hash(password + salt)
```

Powyższa notacja jest uproszczona. W praktyce bcrypt i Argon2 obsługują generowanie soli wewnętrznie, więc programista wywołuje `bcrypt.hash(password)`funkcję, a ona automatycznie generuje, osadza i zapisuje sól. Model ręcznej konkatenacji ma zastosowanie do starszych schematów, takich jak algorytm SHA-256 z solą.

Sól jest przechowywana w bazie danych wraz z hashem. Ponieważ każdy użytkownik otrzymuje inną sól, identyczne hasła generują zupełnie różne hashe. Tabele tęczowe stają się bezużyteczne, ponieważ atakujący musiałby wstępnie obliczyć osobną tabelę dla każdej możliwej wartości soli.

## Kiedy przechowywanie haseł zawodzi

Włamanie **do systemu RockYou** w 2009 roku ujawniło około 32 milionów haseł użytkowników zapisanych w **postaci zwykłego tekstu** . Powstały plik,  `rockyou.txt`, stał się standardową listą słów pierwszego przejścia w atakach słownikowych. Jest on preinstalowany w systemach Kali Linux i AttackBox pod adresem  `/usr/share/wordlists/rockyou.txt`.

**Wyciek danych Aptoide** w kwietniu 2020 roku ujawnił ponad 20 milionów kont w niezależnym sklepie z aplikacjami na Androida. Hasła były przechowywane jako skróty SHA-1 bez soli. Pojedynczy nowoczesny procesor graficzny może testować ponad 10 miliardów kandydatów SHA-1 na sekundę, co oznacza, że ​​pełne przetworzenie pliku rockyou.txt zajmuje ułamek sekundy. Bez soli, tablice tęczowe jeszcze bardziej przyspieszają proces: nie jest wymagane żadne łamanie hasła, które pojawia się we wstępnie obliczonej tabeli wyszukiwania.

Szybki hasz, brak soli i atakujący nie musi prawie czekać.

Zanim złamiemy hash, musimy wiedzieć, jaki algorytm go wygenerował. Podanie niewłaściwego trybu lub formatu do narzędzia łamającego hasła nie przyniesie żadnych rezultatów, niezależnie od czasu trwania ataku. Na szczęście większość formatów hashów ma rozpoznawalne cechy, które pozwalają nam szybko zawęzić zakres poszukiwań.

Aby śledzić przykłady w tym zadaniu, możesz uruchomić AttackBox, klikając `Start AttackBox`przycisk powyżej. Po załadowaniu otwórz terminal, a polecenia będą gotowe do uruchomienia.

## Cechy wizualne

Najszybszą kontrolą jest zawsze długość i format:

|Typ skrótu|Długość|Prefiks / Format|Przykład|
|---|---|---|---|
|MD5|32 znaki szesnastkowe|Nic|5f4dcc3b5aa765d61d8327deb882cf99|
|SHA-1|40 znaków szesnastkowych|Nic|5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8|
|SHA-256|64 znaki szesnastkowe|Nic|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|
|NTLM|32 znaki szesnastkowe|Nic|8846f7eaee8fb117ad06bdd830b7586c|
|bcrypt|~60 znaków|2a, 2b lub 2y|2 lata temu 12 lat temu...|

Najtrudniejsza niejasność: **MD5 i NTLM składają się z 32 znaków szesnastkowych** . Sam skrót nie powie nam, który jest który. Rozstrzyga to kontekst. Skrót wyodrębniony z pliku SAM systemu Windows lub pobrany z Active Directory to prawie na pewno skrót NTLM. Skrót pobrany z bazy danych aplikacji internetowej to najprawdopodobniej MD5 lub wariant SHA. W przypadku braku kontekstu, wypróbuj oba.

Haszy bcrypt są niemożliwe do pomylenia. Prefiks `$2a$`, `$2b$`, lub  `$2y$`natychmiast identyfikuje algorytm. Liczba, która po nim następuje (np. `$2y$12$`) to współczynnik kosztu, który kontroluje, jak wolno przebiega obliczanie hasza.

## Korzystanie z hashida

**Funkcja hashid** analizuje format ciągu haszującego i zwraca listę możliwych algorytmów. Jest ona preinstalowana w systemie Kali. Jeśli nie znajdziesz jej preinstalowanej w systemie AttackBox, możesz uruchomić program, `apt install hashid`aby ją zainstalować z oficjalnych repozytoriów.

hashid

```shell-session
root@tryhackme:~# hashid '5f4dcc3b5aa765d61d8327deb882cf99'
Analyzing '5f4dcc3b5aa765d61d8327deb882cf99'
[+] MD2 
[+] MD5 
[+] MD4 
[+] Double MD5 
[+] LM 
[+] RIPEMD-128 
[+] Haval-128 
[+] Tiger-128 
[+] Skein-256(128) 
[+] Skein-512(128) 
[+] Lotus Notes/Domino 5 
[+] Skype 
[+] Snefru-128 
[+] NTLM 
[+] Domain Cached Credentials 
[+] Domain Cached Credentials 2 
[+] DNSSEC(NSEC3) 
[+] RAdmin v2.x
```

Funkcja hashid zwraca kilka kandydatów na 32-znakowy ciąg szesnastkowy, ponieważ wiele algorytmów generuje dane wyjściowe o takiej długości. Użyj kontekstu, aby zawęzić wybór, lub wypróbuj najbardziej prawdopodobne kandydatury w kolejności podczas łamania.

W przypadku bcrypt hashid daje jednoznaczny wynik:

hashid

```shell-session
root@tryhackme:~# hashid '$2y$10$wJ/mZDURD4jQ0lrCEMheE.8FzMXNEBNjIkuZgEFm9VMn1m4ZP4eDG'
Analyzing '$2y$10$wJ/mZDURD4jQ0lrCEMheE.8FzMXNEBNjIkuZgEFm9VMn1m4ZP4eDG'
[+] Blowfish(OpenBSD) 
[+] Woltlab Burning Board 4.x 
[+] bcrypt
```

Wszystkie trzy wyniki odnoszą się do tego samego formatu skrótu. `hashid`Oznacza to `Blowfish(OpenBSD)`, że bcrypt wewnętrznie korzysta z harmonogramu kluczy Blowfish i został pierwotnie dostarczony z OpenBSD. Prefiks „any” `$2y$`lub  „any `$2b$`” oznacza bcrypt.

## Hashcat --zidentyfikuj

Jeśli już pracujemy w Hashcacie, możemy całkowicie pominąć przełączanie narzędzi. Od wersji 6.2.6 Hashcat zawiera wbudowaną flagę identyfikacyjną:

hashcat

```shell-session
root@tryhackme:~# hashcat --identify '5f4dcc3b5aa765d61d8327deb882cf99'
The following 11 hash-modes match the structure of your input hash:

      # | Name                                                       | Category
  ======+============================================================+======================================
    900 | MD4                                                        | Raw Hash
      0 | MD5                                                        | Raw Hash
     70 | md5(utf16le($pass))                                        | Raw Hash
   2600 | md5(md5($pass))                                            | Raw Hash salted and/or iterated
   3500 | md5(md5(md5($pass)))                                       | Raw Hash salted and/or iterated
   4400 | md5(sha1($pass))                                           | Raw Hash salted and/or iterated
  20900 | md5(sha1($pass).md5($pass).sha1($pass))                    | Raw Hash salted and/or iterated
   4300 | md5(strtoupper(md5($pass)))                                | Raw Hash salted and/or iterated
   1000 | NTLM                                                       | Operating System
   9900 | Radmin2                                                    | Operating System
   8600 | Lotus Notes/Domino 5                                       | Enterprise Application Software (EAS)
```

W wynikach wyświetlana jest lista pasujących trybów wraz z ich numerami, gotowa do skopiowania bezpośrednio do polecenia łamania. Dla czystego przepływu pracy `--identify`jest to często najszybsza ścieżka od nieznanego skrótu do pierwszej próby złamania.

## Zasoby online

Jeśli chodzi o szybkie wyszukiwanie, warto poznać dwie strony:

- [crackstation.net(otwiera się w nowej karcie)](https://crackstation.net/): Wklej hash, a on sprawdzi go w wstępnie obliczonej tabeli wyszukiwania zawierającej miliardy wpisów. Jeśli tekst jawny był już wcześniej widziany, zostanie natychmiast zwrócony.
- [hashes.com(otwiera się w nowej karcie)](https://hashes.com/en/decrypt/hash): Identyfikuje typ skrótu i ​​próbuje wyszukać go w dużej bazie danych. Akceptuje również zbiorcze przesyłanie skrótów.

Oba są przydatne w środowiskach CTF i laboratoryjnych, gdzie liczy się szybkość.

> **Uwaga:** W przypadku rzeczywistego zaangażowania nigdy nie przesyłaj haszy klienta do stron trzecich. Hasz może być poufny, a każde wyszukiwanie tworzy zapis tego, co i kiedy łamałeś.

## Tryby Hashcat i formaty Johna

Po zidentyfikowaniu algorytmu tłumaczymy go na format specyficzny dla danego narzędzia lub numer trybu:

| Algorytm | Tryb Hashcat (-m) | Jan Format ( --format=) |
| -------- | ----------------- | ----------------------- |
| MD5      | 0                 | raw-md5                 |
| SHA-1    | 100               | raw-sha1                |
| SHA-256  | 1400              | raw-sha256              |
| SHA-512  | 1700              | raw-sha512              |
| NTLM     | 1000              | nt                      |
| bcrypt   | 3200              | bcrypt                  |

Te wartości są stałe. Bieganie `hashcat -m 1000`zawsze oznaczaNTLM, niezależnie od formatu skrótu. Błędne ustawienie trybu jest jedną z najczęstszych przyczyn braku rezultatów po złamaniu.

> **Uwaga:** Jeśli hashid podaje wielu kandydatów na 32-znakowy skrót szesnastkowy, spróbujMD5(tryb  `0`) jako pierwszy. Jeśli atak zakończy się bez rezultatów, spróbuj NTLM (tryb  `1000`).

Mamy już hash. Teraz potrzebujemy planu. Głównym wyzwaniem w łamaniu haseł jest wygenerowanie odpowiednich haseł kandydatów wystarczająco szybko, aby znaleźć pasujące hasła, zanim zabraknie czasu lub kandydatów. Żadna metoda nie działa w każdym przypadku, a wybór niewłaściwej strategii to strata czasu bez rezultatów.

> **Uwaga:** Wszystkie narzędzia ilista słówŚcieżki w tym zadaniu odzwierciedlają aktualny AttackBox. Jeśli korzystasz ze starszej wersji, ścieżki mogą się różnić: reguły Hashcat w [brakuje nazwy użytkownika] `/opt/hashcat/rules/`, a reguły Johna w [ brakuje nazwy użytkownika] `/opt/john/rules/`. Jeśli ścieżka nie istnieje, użyj [brakuje nazwy użytkownika] `find / -name <filename> 2>/dev/null`, aby ją zlokalizować.

## Ataki słownikowe

Atak słownikowy polega na porównywaniu gotowej listy haseł kandydackich z hashem, jedno po drugim. To najszybszy pierwszy krok w większości zadań łamania haseł i zawsze powinniśmy od niego zaczynać.

Najczęściej używaną listą słów jest **rockyou.txt** , prawdziwy zbiór 14 milionów haseł, który wyciekł podczas włamania RockYou w 2009 roku. Jest on preinstalowany w systemie AttackBox pod adresem  `/usr/share/wordlists/rockyou.txt`. Ponieważ pochodzi z prawdziwego włamania, odzwierciedla rzeczywiste wybory użytkowników dotyczące haseł, co czyni go niezwykle skutecznym.

Aby zapewnić szerszy zasięg, kolekcja  **SecLists**`/usr/share/wordlists/SecLists/` zawiera listy słów kluczowych dla konkretnych kontekstów: popularnych haseł do aplikacji internetowych, domyślnych ustawień aplikacji oraz list dla poszczególnych krajów. Ścieżka `/usr/share/wordlists/SecLists/Passwords/`to ta, z której korzystamy najczęściej.

Od czasu wycieku RockYou, liczba list słów znacznie wzrosła. [RockYou2024(otwiera się w nowej karcie)](https://cybernews.com/security/rockyou2024-largest-password-compilation-leak/), opublikowany w lipcu 2024 roku, to skompilowana lista około 9,9 miliarda unikalnych haseł w postaci zwykłego tekstu, zebranych z dekad włamań. Przy takiej skali prawdopodobieństwo, że dane hasło z prawdziwego świata pojawi się gdzieś na liście, jest wysokie. Nie jest to coś, co wrzucamy do ćwiczenia dla początkujących; nieskompresowany plik zajmuje około 150 GB, ale ilustruje to, dlaczego ataki słownikowe są nadal tak skuteczne: atakujący nie zgadują, lecz korzystają z haseł, których faktycznie używali prawdziwi ludzie.

Atak słownikowy łamie każde hasło, które pojawia się dosłownie na liście słów. Jego słabość jest równie oczywista: jeśli hasła nie ma na liście, nie da się go złamać.

## Ataki siłowe

Atak siłowy generuje każdą możliwą kombinację znaków o określonej długości. Mając nieograniczony czas, zawsze odzyska hasło. W praktyce rzadko jest to wykonalne w przypadku kombinacji dłuższej niż 6-7 znaków, ponieważ przestrzeń wyszukiwania rośnie wykładniczo.

W przypadku hasła 6-znakowego składającego się wyłącznie z małych liter: `26^6 = 308,915,776`kombinacje. W przypadku hasła 8-znakowego, zawierającego zarówno wielkie, jak i małe litery, `62^8 = 218,340,105,584,896`kombinacje. Nawet przy 1 miliardzie kandydatów na sekundę, pełny atak siłowy na 8 znaków z użyciem wielkich i małych liter zająłby ponad 2 dni na hash.

Czysta siła ma sens tylko wtedy, gdy przestrzeń wyszukiwania jest naprawdę niewielka: na przykład 4-cyfrowy kod PIN lub tak ograniczony wzór, że wyczerpanie wszystkich opcji jest szybkie.

## Ataki oparte na regułach

Ataki oparte na regułach polegają na wykorzystaniu istniejącej listy słów i zastosowaniu transformacji do każdego słowa, generując mutacje powszechnie stosowane przez ludzi podczas tworzenia haseł:

- Zacznij pisać wielką literą: `password`→`Password`
- Dodaj liczbę: `password`→`password1`
- Dodaj znak specjalny: `password`→`password!`
- Zamień znaki: `password`→`p@ssw0rd`

Reguły znacząco rozszerzają zasięg, nie generując ogromnej przestrzeni kandydatów, jak w przypadku ataku siłowego. Zasady dotyczące haseł wymagające wielkiej litery, cyfry lub znaku specjalnego tworzą przewidywalne mutacje: użytkownicy zaczynają od wielkiej litery, dodają `1`lub  `!`i uznają to za gotowe. Reguły wykorzystują właśnie te wzorce. W AttackBox pliki reguł Hashcata znajdują się pod adresem  `/opt/hashcat/rules/`:

|Plik reguł|Opis|
|---|---|
|best64.rule|64 wysoce skuteczne mutacje, dobry pierwszy wybór|
|rockyou-30000.rule|30 000 reguł opracowanych na podstawie analizy RockYou|
|d3ad0ne.rule|Duży zestaw zasad stworzony przez społeczność|
|reguła nurkowania|Obszerny zestaw reguł obejmujący szeroki zakres mutacji|
|JednaRegułaAbyRządzićWszystkimi.reguła|Popularny zestaw reguł opracowany przez społeczność; nie jest domyślnie dołączony, przed użyciem należy sprawdzić, czy znajduje się w systemie|

John the Ripper ma własne zestawy zasad pod adresem `/usr/local/john/run/rules/`. Możesz je aktywować za pomocą  `--rules=wordlist`(zastosowuje domyślne mutacje) lub  `--rules=single`(zastosowuje pojedynczy zestaw zasad, który generuje mutacje oparte na imieniu i nazwie użytkownika).

John również popiera ataki maskowe za pośrednictwem swojej `--mask=`opcji, jednak w tym pokoju skupimy się na składni maski Hashcata, ponieważ jest ona szerzej udokumentowana.

## Ataki maskowe

Atak maskowy to ustrukturyzowany atak siłowy, w którym definiuje się **wzór** hasła, a nie tylko zestaw znaków. Jeśli wiemy, że hasło ma określoną strukturę, na przykład słowo i czterocyfrowy rok, atak maskowy generuje tylko kandydatów pasujących do tej struktury.

Składnia maski Hashcat wykorzystuje symbole zastępcze dla zestawów znaków:

|Symbol zastępczy|Zestaw znaków|
|---|---|
|?l|Małe litery (az)|
|?u|Wielkie litery (AZ)|
|?D|Cyfry (0-9)|
|?S|Znaki specjalne|
|?A|Wszystkie do druku ASCII|

Maska hasła taka jak `Summer2026!`.  `?u?l?l?l?l?l?d?d?d?d?s`Generuje ona znacznie mniej kandydatów niż pełne, brutalne łamanie hasła o tej samej długości.

## Wybór właściwego podejścia

|Scenariusz|Najlepsze podejście|
|---|---|
|Brak informacji o haśle|Atak słownikowy z użyciem pliku rockyou.txt|
|Słownik zawodzi, hasło prawdopodobnie uległo mutacji|Słownik + reguły (np. best64.rule)|
|Znany wzór hasła lub wymuszona polityka|Atak maskowy|
|Krótkie hasło, mały zestaw znaków|Siła brutalna (tylko o ograniczonej długości)|
|Cel prawdopodobnie użył terminów specyficznych dla firmy|Zwyczajlista słów+ zasady|

Zacznij od ataku słownikowego, ponieważ jest szybki i obejmuje najpopularniejsze hasła. Jeśli się nie powiedzie, przejdź do reguł. Używaj masek, gdy dysponujesz wiarygodnymi informacjami o strukturze hasła.

Mając przygotowaną strategię, możemy przeprowadzić pierwsze próby.**Jan Rozpruwacz**i **Hashcat** to dwa narzędzia, których będziemy używać najczęściej do łamania zabezpieczeń offline. Oba obsługują ataki słownikowe, reguły i maski. Różnią się jednak szybkością, obsługą formatów i sposobem przetwarzania danych wyjściowych.

## Konfigurowanie przykładowego skrótu

Wszystkie przykłady w tym zadaniu używają dwóch MD5hasze. Zapisz je do plików przed uruchomieniem czegokolwiek:

```bash
echo "5f4dcc3b5aa765d61d8327deb882cf99" > demo.txt
```

```bash
echo "0571749e2ac330a7455809c6b0e7af90" > demo2.txt
```

```bash
echo "37b4e2d82900d5e94b8da524fbeb33c0" > demo3.txt
```

`demo.txt`jest używany do podstawowych ataków słownikowych, `demo2.txt`ataków opartych na regułach i `demo3.txt`ataków maskowych.

## Jan Rozpruwacz

John the Ripper (zwykle po prostu „John”) to wszechstronny cracker oparty na procesorze. Obsługuje szeroką gamę formatów skrótów, w tym wiele niestandardowych, i potrafi automatycznie wykrywać formaty, gdy nie zostaną one określone wprost. Jest szczególnie przydatny w przypadku wpisów w plikach shadow w systemach Unix oraz szybkich prób wymagających automatycznego wykrywania formatu.

**Podstawowy atak słownikowy:**

Jan --format

```shell-session
root@tryhackme:~# john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt demo.txt
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=2
Press 'q' or Ctrl-C to abort, almost any other key for status
password         (?)     
1g 0:00:00:00 DONE (2026-03-24 06:24) 4.166g/s 1600p/s 1600c/s 1600C/s 123456..michael1
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Wyjaśnienie flag:

- `--format=raw-md5`, określa format skrótu jawnie (użyj etykiet formatu Johna z zadania 3)
- `--wordlist=`, ścieżka dolista słówplik
- `demo.txt`plik zawierający jeden hash na linię

**Tryb automatycznego wykrywania** (gdy nie masz pewności co do formatu):

John automatycznie wykrywa

```shell-session
root@tryhackme:~# john --wordlist=/usr/share/wordlists/rockyou.txt demo.txt
Warning: detected hash type "LM", but the string is also recognized as "dynamic=md5($p)"
Use the "--format=HAVAL-128-4" option to force loading these as that type instead
Use the "--format=NT" option to force loading these as that type
Loaded 2 password hashes with no different salts (LM [DES 256/256 AVX2])
Warning: poor OpenMP scalability for this hash type, consider --fork=2
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
...
0g 0:00:00:24 DONE (2026-03-24 06:25) 0g/s 440565p/s 440565c/s 881130C/s !!1QWER..*7¡VA
Session completed.
```

Zwróć uwagę na wynik: `0g`oznacza zero złamanych haseł. John domyślnie użył formatu LM, który jest błędny dla naszego skrótu MD5, więc cała lista słów została wygenerowana bez ani jednego dopasowania. Właśnie dlatego  `--format`preferujemy format jawny, gdy znamy algorytm.

**Atak oparty na regułach:**

John --zasady

```shell-session
root@tryhackme:~# john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt --rules=wordlist demo2.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=2
Press 'q' or Ctrl-C to abort, almost any other key for status
sunshine         (?)     
1g 0:00:00:00 DONE (2026-03-24 06:40) 1.492g/s 573.1p/s 573.1c/s 573.1C/s 123456..michael1
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

**Wyświetlanie złamanych haseł**

John przechowuje wyniki w pliku potfile pod adresem `/usr/local/john/run/john.pot`. Aby wyświetlić wcześniej złamane hasze:

John --pokaż

```shell-session
root@tryhackme:~# john --show --format=raw-md5 demo.txt                    
?:password

1 password hash cracked, 0 left
```

Zawsze dołączaj `--format`z  `--show`, w przeciwnym razie John może nie zlokalizować poprawnie wpisów w pliku potfile.

## Hashcat

Hashcat jest akcelerowany przez GPU, dzięki czemu jest znacznie szybszy niż John w przypadku większości typów haszowania. Na nowoczesnym GPU Hashcat może przetwarzać miliardy kandydatów MD5 lub SHA-1 na sekundę, w porównaniu do milionów na procesorze. W przypadku bcrypt różnica w szybkości ma mniejsze znaczenie, ponieważ koszt bcrypt ogranicza przepustowość niezależnie od sprzętu.

**Podstawowy atak słownikowy:**

hashcat

```shell-session
root@tryhackme:~# hashcat -m 0 -a 0 demo.txt /usr/share/wordlists/rockyou.txt

hashcat (v6.2.6) starting
...

5f4dcc3b5aa765d61d8327deb882cf99:password

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: 5f4dcc3b5aa765d61d8327deb882cf99
Speed.#1.........:     7724 H/s (0.08ms) @ Accel:256 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
...
```

Wyjaśnienie flag:

- `-m 0`, typ skrótu (0 = MD5; użyj numerów trybów z zadania 3)
- `-a 0`, tryb ataku (0 = słownik)
- `demo.txt`plik zawierający jeden hash na linię
- Ostatnim argumentem jest ścieżka listy słów

**Atak oparty na regułach:**

zasady hashcat

```shell-session
root@tryhackme:~# hashcat -m 0 -a 0 demo2.txt /usr/share/wordlists/rockyou.txt -r /usr/local/hashcat/rules/best64.rule
hashcat (v6.2.6) starting

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 1104517645

0571749e2ac330a7455809c6b0e7af90:sunshine                 
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: 5f4dcc3b5aa765d61d8327deb882cf99
Time.Started.....: Tue Mar 24 06:51:23 2026 (0 secs)
Time.Estimated...: Tue Mar 24 06:51:23 2026 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Mod........: Rules (/usr/share/hashcat/rules/best64.rule)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  8591.6 kH/s (4.07ms) @ Accel:256 Loops:77 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
...

Started: Tue Mar 24 06:51:22 2026
Stopped: Tue Mar 24 06:51:25 2026
```

Wyjaśnienie flag:

- `-r`, określa plik reguł, który ma zostać zastosowany do listy słów

**Atak maskowy:**

maska ​​hashcat

```shell-session
root@tryhackme:~# hashcat -m 0 -a 3 demo3.txt '?l?l?l?l?l?l?l?l'
hashcat (v6.2.6) starting

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Brute-Force
* Raw-Hash

Host memory required for this attack: 0 MB

37b4e2d82900d5e94b8da524fbeb33c0:football                
                                                          
Session..........: hashcatStatus...........: CrackedHash.Mode........: 0 (MD5)Hash.Target......: 37b4e2d82900d5e94b8da524fbeb33c0Time.Started.....: Wed May 20 12:49:52 2026 (11 secs)Time.Estimated...: Wed May 20 12:50:03 2026 (0 secs)Kernel.Feature...: Pure KernelGuess.Mask.......: ?l?l?l?l?l?l?l?l [8]Guess.Queue......: 1/1 (100.00%)Speed.#1.........: 27970.6 kH/s (4.14ms) @ Accel:128 Loops:512 Thr:1 Vec:8Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)Progress.........: 310855680/208827064576 (0.15%)Rejected.........: 0/310855680 (0.00%)Restore.Point....: 17664/11881376 (0.15%)Restore.Sub.#1...: Salt:0 Amplifier:1024-1536 Iteration:0-512Candidate.Engine.: Device GeneratorCandidates.#1....: rladoner -> mrelkessHardware.Mon.#1..: Util: 90%

Started: Tue Mar 24 07:06:42 2026
Stopped: Tue Mar 24 07:06:50 2026
```

Wyjaśnienie flag:

- `-a 3`, tryb ataku 3 = atak maskowy
- Ostatnim argumentem jest wzór maski

**Zapisywanie danych wyjściowych do pliku**

Zapisywanie danych wyjściowych

```shell-session
root@tryhackme:~# hashcat -m 0 -a 0 demo2.txt /usr/share/wordlists/rockyou.txt -o cracked.txt
cat cracked.txt
0571749e2ac330a7455809c6b0e7af90:sunshine
```

**Wyświetlanie wyników po biegu**

Hashcat przechowuje wyniki w formacie `/usr/local/hashcat/hashcat.potfile`. Po zakończeniu sesji dodaj,  `--show`aby wyświetlić wyniki bez ponownego uruchamiania ataku:

hashcat --pokaż

```shell-session
root@tryhackme:~# hashcat -m 0 demo.txt --show
5f4dcc3b5aa765d61d8327deb882cf99:password
```

## Notatki dotyczące wydajności

Warto wiedzieć przed rozpoczęciem czegoś dłuższego:

- **Zapasowy procesor:** Na AttackBoxie bez dedykowanego procesora graficznego, Hashcat działa w trybie procesora. Ataki słownikowe na MD5 i SHA-256 nadal będą szybko się kończyć. Niezależnie od tego, bcrypt będzie powolny z założenia.
- **Zachowanie pliku potfile:** Oba narzędzia pomijają skróty, które już znajdują się w pliku potfile. Ponowne przeprowadzenie ataku na te same skróty nie będzie stratą czasu na ponowne łamanie.
- **Wznawianie sesji:** W przypadku długich przebiegów Hashcata użyj ,  `--session=`aby nadać nazwę sesji i  `--restore`wznowić ją w przypadku przerwania:

Sesja Hashcat

```shell-session
root@tryhackme:~# hashcat -m 3200 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt --session=bcrypt_crack
```

Jeżeli bieg zostanie przerwany, kontynuuj dokładnie od miejsca, w którym został przerwany:

Wznowienie Hashcat

```shell-session
root@tryhackme:~# hashcat --session=bcrypt_crack --restore
```

## Porównanie

||Jan Rozpruwacz|Hashcat|
|---|---|---|
|Przyśpieszenie|Procesor(głównie)|GPU (głównie,Procesor(awaryjny)|
|Prędkość (MD5/SHA)|Szybko|Bardzo szybko|
|Wykrywanie formatu|Dobre automatyczne wykrywanie|Wymagany tryb jawny|
|Formaty niestandardowe|Doskonały|Dobry|
|Zestawy reguł|Wbudowany + rozszerzalny|Duża biblioteka plików|
|Najlepszy dla|Szybkie próby, różne formaty, pliki cieni|Ciągłe ataki, łamanie przyśpieszone przez GPU|

Żadne z tych narzędzi nie jest zdecydowanie lepsze. W praktyce John sprawdza się dobrze w przypadku szybkich prób automatycznego wykrywania oraz w przypadku formatów, z którymi Hashcat radzi sobie słabo. Hashcat to doskonały wybór w przypadku ciągłych, szybkich ataków słownikowych, regułowych lub maskowych.

Czas na zastosowanie wszystkich zmian. Cztery pliki hash są wstępnie załadowane w AttackBoxie w formacie `/root/Rooms/PasswordCracking/`. Jeśli pracujesz na komputerze lokalnym, pobierz plik zip, klikając przycisk **Pobierz pliki zadań** , i rozpakuj go, aby uzyskać `hash1.txt`pliki , `hash2.txt`, `hash3.txt`i `hash4.txt`. Przejrzyj pliki po kolei. Dla każdego z nich:

Przeanalizuj kolejno wszystkie hasze. Dla każdego z nich:

1. Uruchom `hashid`go i porównaj wynik z cechami wizualnymi z zadania 3, aby potwierdzić działanie algorytmu
2. Wybierz odpowiedni tryb Hashcat lub format John z tabeli referencyjnej zadania 3
3. Przeprowadź atak słownikowy za pomocą`/usr/share/wordlists/rockyou.txt`

Hash 4 to bcrypt. Złamie się wolniej niż inne, ponieważ bcrypt jest zaprojektowany z myślą o wysokim koszcie. Bądź cierpliwy.

Dwa z czterech haszy mają ten sam tekst jawny. To celowe. Jeśli porównamy je ze sobą, wyniki nie będą do siebie podobne, a o to właśnie chodzi: algorytm jest tak samo ważny jak samo hasło. Identyfikacja typu hasza nie jest formalnością.

Różnica między „mam hash” a „mam hasło” jest krótsza, niż się wydaje. Zidentyfikuj algorytm, wybierz atak, który pasuje do tego, co wiemy o celu, i skieruj na niego odpowiednie narzędzie. Skrót bcrypt w zadaniu 6 powinien zająć zauważalnie więcej czasu niż pozostałe. To nie błąd, a cel powolnej funkcji skrótu, która działa dokładnie tak, jak powinna.

Przeszliśmy od tematu przechowywania haseł i znaczenia wyboru algorytmu, przez identyfikację skrótu za pomocą `hashid`i  `hashcat --identify`, po przeprowadzanie ataków słownikowych, opartych na regułach i maskach za pomocą obuJan Rozpruwaczi Hashcat. Ta sama wiedza działa w drugą stronę: wybór bcrypt lub Argon2 o wysokim współczynniku kosztów, wymuszanie zasolenia i unikanie szybkich skrótów do przechowywania haseł to defensywny aspekt wszystkiego, co tutaj praktykowaliśmy.

## Następne kroki

Umiejętności nabyte w tym pokoju bezpośrednio przekładają się na pracę dyplomową:

- [Szach-mat](https://tryhackme.com/jr/checkmate) : Zastosuj wszystko w pełnym scenariuszu: profiluj cel, buduj niestandardowe listy słów i rozwiązuj wielokomorowe wyzwanie haszujące przy realistycznych ograniczeniach
- [Ataki na hasła](https://tryhackme.com/room/passwordattacks) : szerszy zakres technik ataków online i offline, obejmujący rozpylanie danych uwierzytelniających i siłowe ataki na usługi na żywo
