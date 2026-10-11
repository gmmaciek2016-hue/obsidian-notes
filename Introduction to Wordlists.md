---

W tej sali zapoznasz się z podstawami korzystania, tworzenia i udoskonalania list słów do celów etycznego hakowania i testów penetracyjnych. Listy słów to rozbudowane pliki tekstowe zawierające potencjalne nazwy użytkowników, hasła i nazwy katalogów, stanowiące niezbędne narzędzia do łamania haseł, enumeracji katalogów i innych zadań testowania automatycznego.

## Cele edukacyjne

- Dowiedz się, czym są listy słów i gdzie są wykorzystywane w ofensywnych środkach bezpieczeństwa.
- Dowiedz się, jak zbierać terminy i nazwy użytkowników specyficzne dla firmy, korzystając z informacji typu open source (OSINT) technik.
- Twórz, czyść i usuwaj duplikaty niestandardowych list słów.
- Użyj swoich udoskonalonych list z narzędziami takimi jak **ffuf** , aby odkryć ukryte katalogi internetowe i**Hydra**do siłowego dostępu do stron logowania.

## Wymagania wstępne

Zanim zaczniesz korzystać z tego pokoju, powinieneś czuć się komfortowo z:

- PodstawowyLinuxnawigacja wiersza poleceń ( `ls`,  `cat`, `grep`,  `sort`)
- Tworzenie żądań HTTP z terminala ( `curl`, `wget`)
- Podstawowe pojęcia dotyczące sieci:HTTPkody statusu i sposób działania formularzy logowania

Wykonuj kolejno każde zadanie i uważnie przeczytaj wyjaśnienia. Pod koniec tego pokoju będziesz mieć solidne podstawy do tworzenia ukierunkowanych list słów i efektywnego ich wykorzystywania podczas spotkań.

A**lista słów**to po prostu plik tekstowy, w którym każdy wiersz zawiera potencjalne słowo, frazę, hasło, nazwę pliku lub inny ciąg znaków. W cyberbezpieczeństwie listy te służą do automatycznego zgadywania: zamiast zmuszać człowieka do wypróbowywania tysięcy możliwych haseł, narzędzie wprowadza każdy wpis z pliku do formularza logowania lub pola wyszukiwania. Listy słów są cenne na wielu etapach testów penetracyjnych. Mogą zawierać popularne hasła (takie jak te ujawnione w wyniku włamań), słowa ze słownika języka angielskiego, słowa istotne dla środowiska docelowego lub listy prawdopodobnych subdomen.

Listy słów są podstawą wielu cyberataków i ocen bezpieczeństwa, zwłaszcza **łamania haseł** i **ataków enumeracyjnych** . Są one wykorzystywane w atakach siłowych, gdzie każdy wpis w pliku jest sprawdzany jako hasło, atakach słownikowych, w których używa się prawdziwych słów i często używanych haseł, oraz enumeracji katalogów lub plików, gdzie lista zawiera możliwe nazwy folderów lub plików w celu zlokalizowania ukrytych zasobów na serwerze WWW.

## Gdzie stosuje się listy słów?

- **Odgadywanie i łamanie haseł:** Narzędzia do łamania haseł, takie jak**Jan Rozpruwacz**i **hashcat** iterują przezlista słówaby znaleźć prawidłowe hasło.
- **Wymuszanie logowania do usługi metodą brute-force:** narzędzia takie jak**Hydra**i **Medusa** testują kombinacje nazwy użytkownika i hasłaSSH,FTP, LubHTTP.Hydrakorzysta z list słów w celu logowania się do różnych usług sieciowych.
- **Brutalne wymuszanie katalogów:** Skaner katalogów internetowych (**DirBuster**,**Gobuster**, **ffuf** ) odczytuje listę standardowych nazw plików i katalogów, a następnie testuje każdą z nich na serwerze WWW.DirBusterNa przykład, SecLists wykorzystuje listy słów zawierające popularne nazwy plików i ścieżki do znajdowania ujawnionych plików i katalogów [.(otwiera się w nowej karcie)](https://github.com/danielmiessler/SecLists)W tym celu w kolekcji znajdują się specjalne listy słów.
- **Odkrywanie subdomen:** DNSNarzędzia enumeracyjne, takie jak **DNSRecon** , **Sublist3r** i **ffuf,** używają list możliwych nazw subdomen do znajdowania dodatkowych hostów. SecLists udostępnia listy, np. `subdomains-top1million-5000.txt`do szybkiego skanowania.

## Popularne narzędzia wykorzystujące listy słów

| Narzędzie              | Zamiar                                   | Jak wykorzystuje listy słów                                                                                      |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| John Ripper            | Łamanie haseł                            | Przeprowadza ataki słownikowe na skróty haseł, wykorzystując listy słów będących popularnymi hasłami.            |
| hashcat                | Łamanie haseł                            | Wykorzystuje listy słów i mutacje oparte na regułach do łamania skrótów haseł.                                   |
| Hydra                  | Wymuszanie logowania do usług sieciowych | Wprowadza listy słów kluczowych zawierające nazwę użytkownika i hasło do monitów logowania dla wielu protokołów. |
| Gobuster / ffuf        | Wyliczanie katalogów i subdomen          | Odczytuje listy słów nazw katalogów lub subdomen i wysyła żądania w celu odkrycia ukrytych zasobów.              |
| Burp Suite / OWASP ZAP | Rozmycie sieci                           | Używa list słów do rozmycia parametrów, plików cookie i nagłówków w celu wykrywania luk w zabezpieczeniach.      |
| Aircrack-ng            | Łamanie haseł bezprzewodowych            | Używa list słów do odgadywania haseł WPA/WPA2.                                                                   |

## Popularne źródła list słów

- **Gotowe listy słów:** Niektóre znane listy są dołączane do dystrybucji do testów penetracyjnych. Lista słów w pliku **rockyou.txt** jest dostarczana przez Kali Linux i zawiera ponad 14 milionów powszechnie używanych haseł. Strona pakietu Kali pokazuje, że `rockyou.txt`jest ona dołączona `/usr/share/wordlists/`, a nieskompresowany plik ma 14 344 392 wierszy. Kolejną istotną kolekcją jest **SecLists** – obszerny zestaw list obejmujący nazwy użytkowników, hasła, katalogi, punkty końcowe API i ładunki ataków. SecLists zawiera listy dostosowane do wyszukiwania treści internetowych ( `raft-large-files.txt`, `common.txt`), łamania haseł ( `top-passwords-shortlist.txt`, `rockyou.txt`), DNS ( `subdomains-top1million-5000.txt`) i wielu innych scenariuszy.
- **Niestandardowe listy słów:** Gotowe listy zapewniają szeroki zakres, ale listy niestandardowe, dopasowane do grupy docelowej, często przynoszą lepsze rezultaty. Listy niestandardowe mogą zawierać dane osobowe, język lokalny, terminologię branżową lub odniesienia kulturowe. Gromadzenie konkretnych słów redukuje szum informacyjny i zwiększa szansę na odgadnięcie prawdziwych kwalifikacji.
- **Automatyczne generatory list słów:** Jeśli znasz wzór hasła lub chcesz wyczerpać wszystkie kombinacje zestawu znaków, generator taki jak **Crunch** może utworzyć listę za Ciebie. Crunch przyjmuje minimalną i maksymalną długość oraz opcjonalny zestaw znaków i generuje każdy możliwy ciąg znaków spełniający te kryteria. Zgodnie z dokumentacją narzędzia Kali, Crunch to generator list słów, który może oddzielnie używać małych i wielkich liter, cyfr i symboli, aby generować listy o zdefiniowanym rozmiarze. Na przykład polecenie `crunch 6 6 0123456789abcdef -o 6chars.txt`generuje każdy sześcioznakowy ciąg z szesnastkowego zestawu znaków i zapisuje go do pliku.   
-
    Crunch może również wysyłać dane wyjściowe do innego programu, umożliwiając bezpośrednie przesyłanie wygenerowanych haseł do narzędzi takich jak Crunch.**Hydra**Lub**Jan Rozpruwacz**. Chociaż generatory kombinatoryczne są skuteczne, należy je stosować rozważnie, ponieważ generują bardzo duże pliki; ukierunkowane listy niestandardowe zbudowane zOSINTczęsto przynoszą skuteczniejsze rezultaty.

Po uruchomieniu komputera docelowego i uzyskaniu jego adresu IP uruchom następujące polecenie, aby dodać niezbędne wpisy do `/etc/hosts`pliku, dzięki czemu nazwy domen będą poprawnie rozpoznawane:

Dodaj adres IP do /etc/hosts

```bash
user@tryhackme:~$ echo '10.128.135.175 tryfinanceme.local social.tryfinanceme.local' >> /etc/hosts
```

Tworzenie skutecznej, spersonalizowanej listy słów zaczyna się od **zebrania informacji** . Listy ogólne często pomijają terminy specyficzne dla danej firmy lub technologii, a dobra, spersonalizowana lista powinna zawierać trzy kategorie:

- **Słowa kluczowe specyficzne dla firmy:** nazwy produktów, funkcje wewnętrzne lub nazwy kodowe projektów
- **Słowa kluczowe dotyczące konkretnych technologii:** terminy oparte na używanych frameworkach lub językach (np. wtyczki WordPress, trasy Laravel)
- **Słowa kluczowe ogólne:** wspólne foldery i trasy API , takie jak `api`, `assets`, `admin`, , i`dev``login``settings`

Połączenie tych kategorii pozwala nam odkryć ukryte katalogi, parametry i poddomeny, których nie wykrywają ogólne listy słów.

Aby utworzyć te listy, musimy zebrać publiczne dane o docelowej organizacji lub osobie. Zbierając nazwy, produkty, lokalizacje lub zainteresowania ze źródeł OSINT, możemy wywnioskować słowa-kandydatki, które prawdopodobnie pojawią się w hasłach, subdomenach lub nazwach katalogów. Ta czynność jest czasami nazywana _zbieraniem (_ ang. harvesting ).

## Proste źródła OSINT

- **Sieci zawodowe:** Nazwiska pracowników, stanowiska i technologie z **serwisu LinkedIn** , stron firmowych lub portali rekrutacyjnych mogą ujawnić wzorce nazewnictwa. MITRE ATT&CK kataloguje to pod [numerem T1591.004 Identyfikacja ról(otwiera się w nowej karcie)](https://attack.mitre.org/techniques/T1591/004/), rozpoznając nazwiska pracowników, role i opisy stanowisk jako źródła rozpoznania, które ujawniają narzędzia, technologie i procesy wewnętrzne. Narzędzia takie jak [linkedin2username(otwiera się w nowej karcie)](https://github.com/initstring/linkedin2username)lub [usieciowane(otwiera się w nowej karcie)](https://github.com/m8sec/crosslinked)zautomatyzować liczenie pracowników.
- **Strony internetowe firm i media społecznościowe:** Strony internetowe firm często wymieniają nazwy projektów, nazwy produktów, lokalizacje biur i slogany. Konta w mediach społecznościowych (Twitter/X, Facebook, GitHub) mogą ujawniać hashtagi, wewnętrzne akronimy lub używane usługi. Dane zebrane z profili, połączeń i postów na platformach takich jak LinkedIn, Facebook, Twitter i GitHub mogą być źródłem ataków socjotechnicznych i rozszerzać powierzchnię ataku.
- **Ogłoszenia o pracę:** Oferty pracy opisują technologie firmy. Frazy takie jak „AWS”, „Salesforce” lub „React” mogą pojawiać się w wewnętrznych subdomenach lub katalogach. Wyszukiwanie firmy i dodawanie hasła „praca” lub korzystanie z serwisów takich jak Indeed czy LinkedIn Jobs może przynieść takie wyniki.

## Podstawowe metody rozpoznania

- **Wyszukiwanie WHOIS** **:** Wyszukiwanie WHOIS ujawnia szczegóły rejestracji domen, serwery nazw, a czasem dane kontaktowe pracowników IT. Bazy danych WHOIS zawierają nazwę organizacji i serwery DNS, na których znajdują się jej dane. Narzędzia takie jak `whois`są preinstalowane w systemie Kali Linux.
- **Wyliczanie subdomen i wyszukiwanie certyfikatów:** Narzędzia takie jak **theHarvester** , **Sublist3r** i **Recon-ng** wyodrębniają subdomeny i adresy e-mail ze źródeł publicznych. Dzienniki przejrzystości certyfikatów (np. crt.sh) i pasywneDNSUsługi mogą ujawniać historyczne nazwy domen.
- **Przeszukiwanie witryny:** Przeszukiwanie witryny docelowej może gromadzić słowa użyte na stronach, w metatagach lub dokumentach. Narzędzie **CeWL** automatyzuje ten proces, przeszukując strony i wyodrębniając słowa.
- **Odcisk palca technologii:** Aby wygenerować słowa kluczowe specyficzne dla danej technologii, odcisk palca technologii docelowej. Możesz użyć narzędzi takich jak **BuiltWith** lub **Wappalyzer** , albo odczytać nagłówki HTTP, aby zidentyfikować frameworki, języki lub systemy CMS. Po zapoznaniu się z technologią, przejrzyj **listy SecLists** w poszukiwaniu list dostosowanych do tych platform (np. ścieżek wtyczek WordPress lub tras API). Takie podejście pozwala uwzględnić istotne nazwy katalogów i punkty końcowe, które są pomijane w listach ogólnych.

## Narzędzia i techniki zbierania słów

Zanim wykonasz poniższe polecenia, upewnij się, że oba komputery działają zgodnie z instrukcjami podanymi na początku tego zadania.

**Cewl: Poszukiwanie słów i e-maili**

[CeWL(otwiera się w nowej karcie)](https://github.com/digininja/CeWL)to narzędzie Ruby, które skanuje adres URL i wyodrębnia z niego unikalne słowa. Może również zbierać adresy e-mail za pomocą `-e`flagi. Użyjemy go do zebrania terminów specyficznych dla danej firmy z witryny TryFinanceMe.

Generowanie listy słów CeWL

```bash
user@tryhackme:~$ cewl -d 2 -m 3 --lowercase --with-numbers -e --email_file emails.txt -w cewl_words.txt http://tryfinanceme.local

CeWL 6.2.1 (More Fixes) Robin Wood (robin@digi.ninja) (https://digi.ninja/)
```

Wyjaśnienie flag:

- `-d 2`:Pająk dwa poziomy głębi.
- `-m 3`:Uwzględnij tylko słowa składające się z trzech lub więcej znaków.
- `--lowercase`:Zmień wszystkie wyodrębnione słowa na małe litery.
- `--with-numbers`:Uwzględnij słowa zawierające liczby.
- `-e`:Włącz wyodrębnianie wiadomości e-mail.
- `--email_file emails.txt`:Zapisz znalezione wiadomości e-mail w `emails.txt`.
- `-w cewl_words.txt`:Zapisz wyodrębnione słowa do `cewl_words.txt`.
- `http://tryfinanceme.local`:Docelowy adres URL do indeksowania.

W ten sposób powstają dwie przydatne listy: `cewl_words.txt`(słowa kluczowe) i `emails.txt`(pełne adresy e-mail firmy). 

**Pobieranie dokumentów i wyodrębnianie ciągów znaków**

Następnie poszukaj hostowanych dokumentów. Wiele organizacji publikuje pliki PDF i dokumenty zawierające żargon wewnętrzny, a nawet dane uwierzytelniające. W środowisku TryFinanceMe `/docs`pliki PDF są hostowane w katalogu. Pobierz te pliki rekurencyjnie i wyodrębnij z nich ciągi znaków zrozumiałe dla człowieka:

Pobieranie plików PDF

```bash
user@tryhackme:~$ wget -r -A pdf http://tryfinanceme.local/docs/--2025-08-13 09:25:37--  http://tryfinanceme.local/docs/
Resolving tryfinanceme.local (tryfinanceme.local)... 10.10.32.241
Connecting to tryfinanceme.local (tryfinanceme.local)|10.10.32.241|:80... connected.
HTTP request sent, awaiting response... 200 OK[...]
user@tryhackme:~$ for f in $(find tryfinanceme.local/docs -name '*.pdf'); do strings -n 5 "$f" | grep -vP '^[/<>%0-9\\]|^(stream|endstream|endobj|xref|trailer|startxref)$' >> raw_words.txt; done
```

**Wyodrębnianie wiadomości e-mail z pobranych plików PDF**

Pliki PDF często zawierają adresy e-mail w stopkach lub polach autora. Wyodrębnij wszystkie adresy e-mail z pobranych dokumentów i zamień je na nazwy użytkowników:

Wyodrębnianie wiadomości e-mail z plików PDF

```bash
user@tryhackme:~$ grep -RhiaoP '[A-Za-z0-9._%+-]+@tryfinanceme\.com' tryfinanceme.local/docs > emails_docs.txt
user@tryhackme:~$ sort -u emails_docs.txt > emails_docs.unique.txt
user@tryhackme:~$ grep -Po '^[^@]+' emails_docs.unique.txt > users_from_emails.txt
```

Oto co robi każdy wiersz:

- Wyrażenie regularne `grep`rekurencyjnie przeszukuje pobrane pliki w celu znalezienia dowolnego pasującego ciągu znaków `username@tryfinanceme.com`i zapisuje wynik w pliku `emails_docs.txt`.
- `sort -u`usuwa zduplikowane adresy e-mail.
- Drugie polecenie grep usuwa część domeny ( `@tryfinanceme.com`), pozostawiając tylko część lokalną. Będzie ona stanowić część listy nazw użytkowników.

**Zbieranie nazw ze strony społecznościowej**

W adresach e-mail i identyfikatorach logowania często pojawiają się imiona i nazwiska prawdziwych osób. W serwisie `social.tryfinanceme.local`każda nazwa profilu jest wyświetlana w kodzie HTML jako:

Kod źródłowy

```html
<h3 class="profile-name">Alex Johnson</h3>
```

Dokładne wyrażenie regularne wyodrębni te nazwy bez pobierania innego tekstu:

Zbieranie nazw ze strony społecznościowej

```bash
user@tryhackme:~$ curl -s http://social.tryfinanceme.local/ | grep -Po '(?<=<h3 class="profile-name">)[^<]+' > names.txt
```

Wzorzec wykorzystuje **dodatni lookbehind** do zakotwiczenia tuż za znacznikiem otwierającym ( `<h3 class="profile-name">`). Następnie dopasowuje wszystkie znaki z wyjątkiem `<`znacznika zamykającego. W rezultacie powstaje czysta lista nazw.

Przekształć te nazwy w prawdopodobne wzorce nazw użytkowników:

Generowanie formatów nazw użytkowników

```bash
user@tryhackme:~$ awk '{print tolower($1)"."tolower($2)}' names.txt > users_first.last.txt
user@tryhackme:~$ awk '{print tolower(substr($1,1,1))tolower($2)}' names.txt > users_flast.txt
user@tryhackme:~$ awk '{print tolower($1)tolower(substr($2,1,1))}' names.txt > users_firstl.txt
```

Dzielimy `awk`każde imię i nazwisko na pierwsze i ostatnie, a następnie tworzymy trzy popularne formaty nazw użytkowników. Dla „Alex Johnson” generują one:

- `users_first.last.txt`: imię, kropka, nazwisko, np.`alex.johnson`
- `users_flast.txt`: pierwsza **litera imienia** + nazwisko, np.`ajohnson`
- `users_firstl.txt`: imię + pierwsza **litera nazwiska** , np.`alexj`

Zamiana na małe litery pozwala uniknąć rozbieżności.

Podsumowanie dotychczas zebranych plików:

- `cewl_words.txt`: Słowa kluczowe ze strony internetowej.
- `emails.txt`:E-maile odkryte przez CeWL.
- `raw_words.txt`:Ciągi znaków wyodrębnione z plików PDF.
- `emails_docs.txt`:E-maile znalezione w plikach PDF.
- `names.txt`:Imiona pracowników ze strony społecznościowej.
- `users_first.last.txt`, `users_flast.txt`, `users_firstl.txt`: Permutacje nazw użytkowników.
- `users_from_emails.txt`:Nazwy użytkowników wyodrębnione z wiadomości e-mail.

Powinieneś teraz mieć zestaw surowych list słów i kandydatów na nazwy użytkowników z różnych źródeł. Surowe listy są często chaotyczne: zawierają duplikaty, mieszaną wielkość liter i nieistotne ciągi znaków. Czyszczenie przekształca ten bałagan w uporządkowane, pozbawione duplikatów listy, które narzędzia enumeracyjne mogą analizować.

## Dlaczego sprzątanie ma znaczenie

Wzdęty, niefiltrowanylista słówMarnuje czas. Katalogi `#include`lub ciągi znaków zawierające znaki interpunkcyjne raczej nie istnieją na serwerze WWW. Zduplikowane wpisy spowalniają brutalne próby bez dodawania wartości. Zapisywanie wszystkiego małymi literami zmniejsza fragmentację, ponieważ `Helios`, `helios`i `HELios`wszystkie odnoszą się do tego samego ciągu. Filtrowanie bardzo krótkich lub złożonych tokenów koncentruje wyliczenia na prawdopodobnych ścieżkach. Wreszcie, podgląd i zliczanie list pomaga ocenić, czy są one za duże, czy za małe.

## Łączenie i normalizacja słów w hasłach

Najpierw połącz słowa pobrane ze strony ( `cewl_words.txt`) i ciągi znaków wyodrębnione z plików PDF ( `raw_words.txt`). Sortowanie i usuwanie duplikatów daje czystszy punkt wyjścia:

Łączenie list słów

```bash
user@tryhackme:~$ cat cewl_words.txt raw_words.txt | sort -u > words_raw.txt
```

`sort -u` Sortuje wiersze alfabetycznie i usuwa duplikaty. Nawet po usunięciu duplikatów lista może zawierać słowa pisane wielkimi literami, znaki powrotu karetki z dokumentów systemu Windows oraz krótkie lub nieprawidłowo sformatowane ciągi znaków. Zastosuj drugi przebieg w celu normalizacji i filtrowania:

Normalizacja i filtrowanie

```bash
user@tryhackme:~$ cat words_raw.txt | tr '[:upper:]' '[:lower:]' | tr -d '\r' | grep -P '^[a-z0-9][a-z0-9._-]{4,}$' | sort -u > words_clean.txt
```

- `tr '[:upper:]' '[:lower:]'`: Zamienia wielkie litery na małe.
- `tr -d '\r'`:Usuwa znaki powrotu karetki w systemie Windows.
- Wzorzec `grep`zachowuje ciągi znaków rozpoczynające się od znaku alfanumerycznego, a następnie dopuszcza litery, cyfry, kropki, podkreślenia lub myślniki i mające co najmniej pięć znaków. Dzięki temu eliminuje się wiele wpisów zakłócających.
- Finał `sort -u`gwarantuje niepowtarzalność.

Sprawdź rozmiar i zapoznaj się z zawartością:

Sprawdzanie listy haseł

```bash
user@tryhackme:~$ wc -l words_clean.txt
user@tryhackme:~$ head words_clean.txtaboutaccessaccountaccuracyadvancedanalysisanalystanalyticsanalyzeassessment
```

Ogromna lista spowolni ffuf; mała może pomijać prawidłowe ścieżki. Powinieneś zobaczyć kilkaset wpisów, wszystkie pisane małymi literami i poprawnie sformatowane.

## Scalanie i normalizowanie nazw użytkowników

Nazwy użytkowników zebrane z adresów e-mail i nazw również muszą zostać usunięte. Scal wszystkie warianty i usuń duplikaty:

Scalanie list nazw użytkowników

```bash
user@tryhackme:~$ cat users_first.last.txt users_flast.txt users_firstl.txt users_from_emails.txt | sort -u > users.txt
```

## Generowanie listy haseł opartej na wzorcu

Jak dotąd Twoja lista słów obejmuje wyszukiwanie katalogów i plików. Aby złamać formularz logowania, potrzebujesz ukierunkowanej listy haseł. Podczas OSINT dowiedziałeś się, że hasła w systemie Helios znajdują się `Helios20NN!`po `NN`cyfrach. Generator kombinatoryczny, taki jak Crunch, może efektywnie wykorzystać tę przestrzeń:

„Generowanie haseł wzorcowych

```bash
user@tryhackme:~$ crunch 11 11 -t Helios20%%! -o pass_helios.txt
```

- Dwa `11`argumenty ustawiają minimalną i maksymalną długość na 11 znaków.
- `-t`: Definiuje wzór, w którym `%%`cyfry są zastępowane cyframi ( `00`do `99`).
- `-o pass_helios.txt`: Zapisuje 100 wpisów na dysku.

Ta lista jest niewielka, co przyspiesza działanie Hydry. Jeśli później zauważysz, że hasła mają inny format, dostosuj odpowiednio wzorzec (np. inny rok lub więcej cyfr).

Na tym etapie powinieneś mieć dwie czyste listy gotowe do użycia:

- `words_clean.txt`:Do wyszukiwania katalogów i plików.
- `users.txt`i `pass_helios.txt`: Do siłowego ataku na formularz logowania.

Mając gotowe czyste listy, użyjemy naszego katalogulista słówAby znaleźć ukryte ścieżki w TryFinanceMe, użyj listy nazw użytkowników i haseł, aby zhakować stronę logowania.

## Odkrywanie katalogów i plików za pomocą Ffuf

Wyliczanie katalogów odpowiada na pytanie: **jakie zasoby istnieją na serwerze WWW, które nie są publicznie linkowane?** Narzędzia takie jak `ffuf`„biorą” listę potencjalnych ścieżek i dołączają każdą z nich do bazowego adresu URL. Następnie interpretują kody odpowiedzi HTTP, aby ustalić, czy dany element istnieje.

Używamy `words_clean.txt`tego tutaj, ponieważ zawiera terminy specyficzne dla firmy, które zebraliśmy w Zadaniu 3 – dokładnie takie, które prawdopodobnie pojawią się jako ukryte nazwy katalogów. Uruchom ffuf w ten sposób:

Przeszukiwanie katalogów

```bash
user@tryhackme:~$ ffuf -w words_clean.txt -u http://tryfinanceme.local/FUZZ -e .php,.html,/ -mc 200,301,302
```

Wyjaśnienie flag:

- `-w words_clean.txt`:Ścieżka do listy słów.
- `-u http://tryfinanceme.local/FUZZ`: Adres URL docelowy; ffuf zastępuje `FUZZ`każdym słowem z listy.
- `-e .php,.html,/`:Przetestuj każde słowo w obecnej postaci i z dołączonymi rozszerzeniami.
- `-mc 200,301,302`: Raportuj tylko odpowiedzi z tymi kodami statusu.

W tym przypadku ffuf przetestuje każde słowo w stanie niezmienionym oraz z rozszerzeniami `.php`, `.html`, i `/`, i zgłosi tylko odpowiedzi HTTP 200, 301 lub 302 (tj. prawidłowe strony lub przekierowania). Przewijając dane wyjściowe, powinniśmy zauważyć wpis o nazwie `helios/`. Jeśli zauważymy setki fałszywych alarmów, dodaj `-fs <bytes>`(filtruj według rozmiaru odpowiedzi) lub `-fl <lines>`(filtruj według liczby wierszy) po zanotowaniu rozmiaru lub liczby wierszy typowej odpowiedzi 404.

ffuf potrafi więcej: możemy go również używać do wykrywania subdomen, parametrów lub punktów końcowych API poprzez dostosowanie wzorca adresu URL i listy słów. W tym laboratorium ograniczymy się do katalogów.

## Atak brute-force na stronę logowania za pomocą Hydry

Gdy już znajdziemy ukryty katalog, przejdźmy do niego. Formularz logowania znajdziemy pod adresem `http://tryfinanceme.local/helios/login.php`.Hydramogę wysłaćHTTPWyślij żądania POST i przeanalizuj kombinacje nazw użytkowników i haseł.

Moduł `http-post-form`przyjmuje specyfikację formularza jako argument, składający się z trzech części rozdzielonych dwukropkiem:

1. `/helios/login.php`:Ścieżka do programu obsługi logowania.
2. `username=^USER^&password=^PASS^`: Treść POST, zawierająca obiekty Hydra `^USER^`i `^PASS^`symbole zastępcze.
3. `S=THM{`: Warunek powodzenia. Hydra uznaje logowanie za pomyślne, jeśli odpowiedź HTTP zawiera `THM{`. Jest to specyficzne dla naszego laboratorium, gdzie flaga pojawia się po pomyślnym zalogowaniu.

HydraBrutalna siła

```bash
user@tryhackme:~$ hydra -L users.txt -P pass_helios.txt -f -V -t 4 tryfinanceme.local http-post-form '/helios/login.php:username=^USER^&password=^PASS^:S=THM{'

[DATA] attacking http-post-form://tryfinanceme.local:80/helios/login.php:username=^USER^&password=^PASS^:S=THM{
[80][http-post-form] host: tryfinanceme.local   login: ****.*****   password: *********
1 of 1 target successfully completed, 1 valid password found
```

Wyjaśnienie flag:

- `-L users.txt`:Odczyt nazw użytkowników z pliku.
- `-P pass_helios.txt`:Odczyt haseł z pliku.
- `-f`: Zatrzymaj się po znalezieniu pierwszych prawidłowych danych uwierzytelniających.
- `-V`: Drukuj każdą próbę.
- `-t 4`:Użyj czterech wątków; jeśli potrzebujesz większej prędkości, zwiększaj ją ostrożnie.

Hydra wyświetli każdą parę nazwa użytkownika/hasło, którą wypróbuje. Gdy pojawi się wiersz z loginem, zanotuj poprawne dane. Możemy teraz otworzyć `http://tryfinanceme.local/helios/`przeglądarkę, zalogować się przy użyciu odkrytej nazwy użytkownika i hasła i wyświetlić flagę.

Świetna robota z ukończeniem **„Wprowadzenia do list słów”** ! W trakcie tej lekcji:

- Przyjrzano się, czym są listy słów, jak się ich używa i dlaczego listy ogólne często są niewystarczające.
- UżywanyOSINTtechniki, takie jak zbieranie nazw z mediów społecznościowych, wyszukiwanie w bazie WHOIS i przeszukiwanie witryn, w celu tworzenia list specyficznych dla danej firmy.
- Połączyliśmy i wyczyściliśmy nasze surowe listy, a następnie zastosowaliśmy filtry w celu usunięcia duplikatów, znormalizowania wielkości liter i wyeliminowania szumu.
- Wygenerowano hasła oparte na wzorcach za pomocą **narzędzia crunch** , połączono wiele formatów nazw użytkowników i przygotowano czyste pliki `words_clean.txt`, `users.txt`i .`pass_helios.txt`
- Użyłem **ffuf** , aby odkryć ukryte katalogi na stronie docelowej i zatrudniłem**Hydra**aby przeprowadzić atak siłowy na formularz logowania, korzystając z naszych niestandardowych list.

Dostosowując nasze listy słów do celu i dbając o ich przejrzystość, zwiększamy wydajność i skuteczność podczas enumeracji lub łamania haseł. Pamiętaj, że te techniki należy zawsze stosować odpowiedzialnie i wyłącznie w systemach, które jesteśmy upoważnieni do testowania. Możemy kontynuować ćwiczenie tych umiejętności w innych pomieszczeniach i eksperymentować z dodatkowymi narzędziami i źródłami, aby jeszcze bardziej udoskonalić nasze niestandardowe…lista słówprzepływ pracy.

Pokój TryHackMe „Wprowadzenie do list słów” to pokój dostępny wyłącznie dla subskrybentów, który wprowadza w koncepcję list słów i sposobu tworzenia ukierunkowanej listy słów za pomocą OSINT. Pokój jest dostępny pod adresem: [https://tryhackme.com/room/introductiontowordlists](https://tryhackme.com/room/introductiontowordlists)

1. Jakie narzędzie może wygenerować niestandardową listę słów na podstawie znanych wzorców?

**Odpowiedź: chrupnięcie**

2.1  **`CeWL`** Ile unikalnych adresów e-mail udało Ci się zebrać po uruchomieniu polecenia pokazanego w zadaniu?

**Odpowiedź: 4**

![](https://simontaplin.net/wp-content/uploads/2026/05/image.png?w=757)

2.2 Ile plików PDF udało Ci się znaleźć?

**Odpowiedź: 1**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-1.png?w=637)

2.3 Ile adresów e-mail (lub nowych adresów e-mail) udało Ci się wyodrębnić z plików PDF?

**Odpowiedź: 4**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-2.png?w=523)

2.4 Jaka jest ostatnia nazwa użytkownika w  `users_from_emails.txt` pliku?

**Odpowiedź: bezpieczeństwo**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-3.png?w=532)

3.1 Ile słów pozostało  `words_clean.txt` po oczyszczeniu pliku?

**Odpowiedź: 161**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-4.png?w=723)

3.2 Jakie jest 10. hasło w  `**pass_helios.txt**` pliku?

**Odpowiedź: Helios2009!**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-5.png?w=517)

3.3 Jakiej flagi  `sort` używa się do usuwania zduplikowanych wierszy?

**Odpowiedź: -u**

3.4 Który znak szablonu crunch reprezentuje cyfrę?

**Odpowiedź: %**

4.1 Jaki kod statusu HTTP raportuje ffuf  `helios/`?

**Odpowiedź: 200**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-6.png?w=718)

4.2 Jaką nazwę użytkownika odkrywa Hydra?

**Odpowiedź: alex.johnson**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-7.png?w=725)

4.3 Co to jest flaga?

Odpowiedź: **THM{w0rdlists_win_rooms}**

![](https://simontaplin.net/wp-content/uploads/2026/05/image-8.png?w=744)
