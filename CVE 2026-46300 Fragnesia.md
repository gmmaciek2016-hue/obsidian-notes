---

Fragnesia jest trzecią luką Linux w zabezpieczeniach jądra umożliwiająca eskalację uprawnień lokalnych w klasie zapisu w pamięci podręcznej stron zostanie ujawniona za niecałe trzy tygodnie. Zgłosił ją William Bowling, szef działu audytu w firmie Zellic, który odkrył błąd za pomocą oprogramowania V12, opracowanego przez firmę Zellic. Sztuczna inteligencja-agentowe narzędzie do audytu bezpieczeństwa. Luka uzyskała `CVE-2026-46300`wynik bazowy CVSS v3.1 wynoszący 7,8 (wysoki). Publiczne ujawnienie nastąpiło 13 maja 2026 r., wraz z działającym proof-of-concept i potencjalną poprawką.

To, co wyróżnia Fragnesię, to nie sam prymityw, znany z Copy Fail i Dirty Frag, ale sposób, w jaki powstał. Poprawka Dirty Frag ( `f4c50a4034e6`, scalona 8 maja 2026 r.) dodała kod, który ufa, że ​​określona flaga bufora gniazda jest poprawna. Od 13 maja ta flaga nie zawsze jest poprawna. Fragnesia to luka w zabezpieczeniach wprowadzona przez poprawkę Dirty Frag. Hyunwoo Kim, który zgłosił oryginalną parę Dirty Frag, publicznie przyznał, że Fragnesia pojawiła się jako niezamierzony efekt uboczny jednej z poprawek napisanych w celu naprawienia jego własnego błędu.

Warto na wstępie ustalić dwie kwestie. Po pierwsze, jest to ta sama szeroka powierzchnia ataku co Dirty Frag (XFRM, ESP, pamięć podręczna stron), ale znajduje się w innej ścieżce kodu. Oryginalne błędy Dirty Frag były w `esp_input()`. `rxkad_verify_packet_1()`Fragnesia jest w `skb_try_coalesce()`, funkcji, która scala bufory gniazd. Po drugie, opublikowany proof-of-concept obejmuje tylko wariant espintcp; drugi wariant w `skb_segment()`został ujawniony przez tego samego badacza dzień po opublikowaniu pierwszej poprawki Fragnesia i do 15 maja 2026 roku wariant ten pozostaje niezałatany.

Klasa podatności ciągle ewoluuje, co stanowi praktyczną lekcję, wokół której zbudowano tę salę.

|Nieruchomość|Kopiowanie nie powiodło się|Brudny Frag|Fragnesia|
|---|---|---|---|
|CVE|CVE-2026-31431|CVE-2026-43284 / 43500|CVE-2026-46300|
|Podsystem jądra|AF_ALG / złącze|xfrm-ESP UDP / RxRPC|xfrm-ESP-in-TCP / łączenie skb|
|Zapisz rozmiar pierwotny|4 bajty|4 bajty (ESP) / 8 bajtów (RxRPC)|1 bajt (na wyzwalacz)|
|Wymagany warunek wyścigu|NIE|NIE|NIE|
|Uderzenie w kontener|Tak|Tak|Tak|
|Stan poprawki|Główna linia|linia główna xfrm-ESP; niezałatany RxRPC|Pierwsza wersja na netdev; druga wersja bez poprawek|

Prymityw zapisu 1-bajtowego wydaje się niewielki w porównaniu do swoich poprzedników, ale jest deterministyczny. Każdy wyzwalacz zapisuje jeden wybrany bajt w jednym wybranym przesunięciu w pamięci podręcznej stron. 192-bajtowy fragment ELF jest dostarczany w dowolnej liczbie wyzwalaczy (zwykle około 176, ponieważ niektóre bajty przypadkowo pasują już do pliku docelowego), a cała sekwencja kończy się w ciągu kilkuset milisekund.

## Cele edukacyjne

Pod koniec tego pokoju będziesz w stanie:

- Wyjaśnij, dlaczego poprawka jądra może wprowadzić nową lukę w zabezpieczeniach na tej samej powierzchni ataku, którą miała zamknąć
- Opisz rolę `skb_try_coalesce()`i `SKBFL_SHARED_FRAG`marker w łańcuchu Fragnesia
- Określ warunki, które umożliwiają ścieżce odbiorczej espintcp wykonanie odszyfrowania AES-GCM w miejscu na stronach pamięci podręcznej stron
- Zastosuj opublikowaną łagodzącą metodę modprobe i potwierdź, że koncepcja proof-of-concept jest zablokowana
- Rozpoznawanie wzorca operacyjnego powtarzających się regresji w tym samym obszarze i odpowiednie projektowanie wykrywania

## Wymagania wstępne

W tym pokoju wymagane jest opanowanie wiersza poleceń Linuksa i praktyczna znajomość lokalnej eskalacji uprawnień. Zdecydowanie polecamy również pokoje [„Copy Fail”](https://tryhackme.com/room/cve202631341) i [„Dirty Frag”](https://tryhackme.com/room/cve202643284) ; Fragnesia bazuje bezpośrednio na prymitywnym mechanizmie zapisu w pamięci podręcznej stron, wprowadzonym w tych pokojach.

Fragnesia to pojedynczy łańcuch składający się z pięciu komponentów, z których cztery istniały przed napisaniem łatki Dirty Frag. Piąty został dodany przez łatkę Dirty Frag. Zrozumienie działania łańcucha wymaga przeanalizowania poszczególnych komponentów, a następnie sprawdzenia, jak łatka zmieniła ścieżki prowadzące do odbiornika deszyfrującego.

## SKBFL_SHARED_FRAG: Flaga uczciwości

Bufor gniazda ( `struct sk_buff`) zawiera tablicę fragmentów, z których każdy opisuje stronę pamięci należącą do pakietu. Większość fragmentów to prywatne bufory należące do stosu sieciowego. Niektóre jednak stanowią odwołania do stron należących do innych podsystemów, najczęściej do pamięci podręcznej stron. Gdy proces wywołuje `splice()`wysłanie zawartości pliku przez gniazdo, jądro dołącza odwołanie do strony pamięci podręcznej stron pliku bezpośrednio do listy fragmentów wychodzącego skb, bez kopiowania żadnych bajtów.

Flaga `SKBFL_SHARED_FRAG`to sposób, w jaki jądro oznacza takie fragmenty jako należące do podmiotów zewnętrznych. Flaga informuje każdą ścieżkę kodu w dół strumienia o jednej rzeczy: „ta pamięć nie należy do ciebie; jeśli musisz ją zmodyfikować, najpierw ją skopiuj”. Funkcje, które muszą mutować dane w skrypcie, sprawdzają `skb_has_shared_frag()`i wywołują `skb_cow_data()`, aby uzyskać prywatny bufor, zanim wykonają jakiekolwiek destrukcyjne działania.

Flaga jest niezmienna. Dopóki każda ścieżka kodu, która dotyka współdzielonego fragmentu, ją respektuje, strony w pamięci podręcznej stron pozostają bezpieczne nawet podczas przechodzenia przez stos sieciowy.

## skb_try_coalesce: Gdzie niezmiennik się łamie

`skb_try_coalesce()`to funkcja jądra, która łączy dwa rekordy SKB w jeden. Stos TCP po stronie odbiorczej używa jej do łączenia segmentów kolejki w większe bufory, co zmniejsza obciążenie pamięci i poprawia przepustowość. Po połączeniu dwóch rekordów SKB fragmenty drugiego rekordu SKB są przenoszone do tablicy fragmentów pierwszego rekordu SKB, a drugi rekord SKB zostaje zwolniony.

W tym właśnie tkwi błąd. `skb_try_coalesce()`Przesyłając fragmenty stronicowane między buforami, nie propaguje `SKBFL_SHARED_FRAG`znacznika na te fragmenty. Scalony skb ostatecznie przenosi fragmenty, które nadal są obsługiwane przez pamięć podręczną stron, ale z wyczyszczoną flagą. Dla każdej ścieżki kodu w dół, scalony skb wygląda teraz jak zupełnie zwyczajny bufor prywatny, który można modyfikować na miejscu.

Błąd pojawił się w 2013 roku (commit `cef401de7be8`) i pozostawał uśpiony przez trzynaście lat, ponieważ przez większość tego czasu żadna ścieżka kodu produkcyjnego nie analizowała połączonych baz danych (SKB) i nie zdecydowała się na ich edycję. Poprawka Dirty Frag zmieniła ten stan rzeczy.

## Ścieżka odbioru XFRM ESP-in-TCP

ESP-in-TCP (RFC 8229) to tryb transportu IPsec, który hermetyzuje pakiety ESP w strumieniu TCP. Jest on używany w scenariuszach NAT, w których enkapsulacja ESP oparta na UDP nie działa. Gdy gniazdo TCP jest skonfigurowane dla espintcp za pomocą `setsockopt`, jądro przełącza obsługę protokołu ULP (Upper Layer Protocol) gniazda na taką, która pobiera pakiety ESP z…TCPstrumień bajtów i przekazuje je do `esp_input()`.

`esp_input()`To funkcja, w której występował pierwotny błąd Dirty Frag. Wykonuje ona deszyfrowanie AEAD na przychodzącym pakiecie, zapisując tekst jawny z powrotem do rejestru SKB. Dla zwiększenia wydajności deszyfrowanie odbywa się w miejscu, gdy wejściowy rejestr SKB jest odklonowany i nie zawiera listy fragmentów. Funkcja jest wywoływana `skb_has_shared_frag()`w celu sprawdzenia, czy żaden z fragmentów nie jest zewnętrznie wspierany. Jeśli flaga jest pusta, funkcja wybiera szybką ścieżkę; jeśli jest ustawiona, funkcja powraca do przydzielenia prywatnego bufora `skb_cow_data()`przed deszyfrowaniem.

`skb_try_coalesce()`To jest dokładnie ta kontrola, którą dodała łatka Dirty Frag. Przed łatką funkcja nie zawsze respektowała flagę. Po łatce funkcja respektuje. Łatka była poprawna. Jednak po jej usunięciu flaga nie jest już godna zaufania .

## Połączenie, które staje się Fragnesią

Połączenie czterech elementów tworzy łańcuch:

```markdown
1. Attacker opens a TCP socket and splices /usr/bin/su's page cache pages
   into the socket's receive queue (skbs are flagged SKBFL_SHARED_FRAG).
2. Kernel coalesces queued skbs via skb_try_coalesce(); the flag is lost.
3. Attacker calls setsockopt(TCP_ULP, "espintcp") to switch the socket to
   ESP-in-TCP mode. Queued data is now processed as ESP ciphertext.
4. esp_input() checks the (now-clear) shared-frag flag, takes the fast
   path, performs AES-GCM decryption in place over the page cache page.
5. The decryption is a XOR of the AES-GCM keystream against the ciphertext.
   By choosing the IV, the attacker chooses the keystream byte, which
   chooses the byte written into the page cache.
```

Technika ta nazywana jest Fragnesia (zlepek słów „fragment” i „amnezja”), ponieważ bufor gniazda zapomina, że ​​jego fragment został współdzielony.

## Dlaczego korupcja staje się głównym hostem

Uszkodzenie znajduje się w globalnej pamięci podręcznej stron jądra, która jest współdzielona przez wszystkie procesy na hoście, niezależnie od przestrzeni nazw, w której znajdują się te procesy. Atakujący dokonuje uszkodzenia z przestrzeni nazw użytkownika, w której posiada uprawnienia root, ale uszkodzone bajty są widoczne dla każdego procesu, który następnie odczytuje ten sam plik, w tym dla procesów uprzywilejowanych działających poza tą przestrzenią nazw.

Eskalacja uprawnień kończy się, gdy plik binarny setuid-root `/usr/bin/su`zostanie wykonany spoza przestrzeń nazw Jądro ładuje plik binarny z uszkodzonej pamięci podręcznej stron, odczytuje bit setuid w pliku na dysku, ustawia efektywny UID na 0, a następnie wykonuje kod powłoki atakującego pod tym efektywnym UID. Kod powłoki wywołuje `setuid(0)`, co powoduje, że proces wywołujący staje się rzeczywistym Identyfikator użytkownika0, a następnie `execve("/bin/sh")`, co powoduje utworzenie powłoki hosta-root.

Ten dwuetapowy schemat ma znaczenie dla praktycznego opisu exploita w Zadaniu 4. Opublikowany proof-of-concept wykonuje tylko pierwszy etap (uszkodzenie) i demonstruje swój sukces, uruchamiając powłokę z przestrzeni nazw. Powłoka ta wydaje się być rootem `whoami`, ale nie może odczytać plików należących do roota, ponieważ jest…przestrzeń nazw-root, a nie host-root. Etap drugi, który tworzy użyteczną powłokę host-root, jest wyzwalany przez operatora uruchamianego `/usr/bin/su`ręcznie spoza przestrzeni nazw po zakończeniu proof-of-concept.

![Diagram pokazujący, jak funkcja skb_try_coalesce usuwa znacznik SKBFL_SHARED_FRAG. Górna połowa przedstawia dwa źródłowe pliki SKB, A i B, każdy z liniową sekcją nagłówka TCP i slotem fragmentów zawierającym stronę z pamięci podręcznej stron z /usr/bin/su z ustawionym parametrem SHARED_FRAG=1. Oba pliki SKB trafiają do czerwonego pola w środku, oznaczonego jako „skb_try_coalesce(), które scala fragmenty z bazy danych SKB B ze stroną z bazy danych SKB A i po cichu usuwa flagę SHARED_FRAG, co jest zachowaniem ukrytym od zatwierdzenia z 2013 roku (cef401de7be8). Dolna połowa przedstawia powstały, połączony plik SKB z dwoma slotami fragmentów, oba nadal oparte na stronach z pamięci podręcznej stron, ale z ustawionym parametrem SHARED_FRAG=0. Kod wywołujący funkcję skb_has_shared_frag() otrzymuje teraz wartość false, więc funkcja esp_input() wybiera szybką ścieżkę i wykonuje odszyfrowanie AES-GCM w miejscu, na stronach pliku w pamięci podręcznej.](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1778925769795.svg)

## Pierwotny zapis 1-bajtowy

Każde odszyfrowanie AES-GCM powoduje kontrolowany zapis jednobajtowy do pamięci podręcznej stronicowania w jednym wybranym przesunięciu. Atakujący kontroluje bajt, zmieniając dolne 32 bity 8-bajtowego ciągu znaków (IV). Zaszyfrowanie bloku licznika znanym kluczem AES-128-GCM generuje 16-bajtowy strumień klucza; używany jest tylko bajt na pozycji 2 bajtu 0. Poprzez iterację nonce'a ciągu znaków (IV) przez maksymalnie 65 536 wartości, osiągalne są wszystkie 256 możliwych wartości bajtów.

Exploit wstępnie oblicza 256-wpisową tablicę wyszukiwania, mapując docelowe bajty na wartości IV, które je generują. Po utworzeniu tablicy, każdy zapis jest pojedynczym wyzwalaczem, który kończy się w mikrosekundach. Publiczny proof-of-concept nadpisuje pierwsze 192 bajty `/usr/bin/su`małym szczątkiem ELF, który wywołuje `setgid(0); setuid(0); execve("/bin/sh", ...)`w punkcie wejścia. Pętla per-byte exploita pomija bajty, których bieżąca wartość już pasuje do żądanego szczątku; `/usr/bin/su`w typowym przypadkuLinuxW systemie około szesnaście bajtów pokrywa się (większość nagłówka ELF), więc uruchamia się około 176 rzeczywistych wyzwalaczy. Pełna sekwencja kończy się w ciągu kilkuset milisekund.

Plik na dysku nigdy nie jest modyfikowany. PlikuczciwośćNarzędzia haszujące dysk nadal zgłaszają plik jako czysty. Jest to identyczne zachowanie jak w przypadku błędów Copy Fail i Dirty Frag, a konsekwencje są takie same.

## Brudna łatka Frag

Oryginalny błąd Dirty Frag xfrm-ESP ( `CVE-2026-43284`) polegał na `esp_input()`pomijaniu szybkiej ścieżki `skb_cow_data()`dla każdego niesklonowanego, nieliniowego pliku skb bez listy fragmentów. Szybka ścieżka była niebezpieczna, ponieważ fragmenty pliku skb mogły być wspierane przez strony pamięci podręcznej stron umieszczone za pomocą `splice()`.

Poprawka o nazwie commit `f4c50a4034e6`dodała dwa fragmenty kodu. Po pierwsze, zaktualizowano ścieżki dołączania datagramów IPv4 i IPv6, aby ustawić je `SKBFL_SHARED_FRAG`na fragmentach łączonych. Po drugie, `esp_input()`zaktualizowano ścieżki sprawdzania `skb_has_shared_frag()`przed przejściem na szybką ścieżkę. Rozumowanie było poprawne, implementacja poprawna, a poprawka zamknęła pierwotny błąd Dirty Frag zgodnie z zamierzeniami.

Poprawka nie przeprowadziła audytu każdej ścieżki kodu, która miała wpływ `SKBFL_SHARED_FRAG`na zachowanie flagi. `skb_try_coalesce()`Była to jedna z takich ścieżek. Istniała już od 2013 roku i przez trzynaście lat nieprawidłowo usuwała flagę. Do czasu wprowadzenia poprawki Dirty Frag żadna ścieżka kodu produkcyjnego nie podjęła krytycznej decyzji w oparciu o flagę, więc błąd był ukryty. Po wprowadzeniu poprawki `esp_input()`zaczęto podejmować właśnie tę decyzję.

Kandydat na łatkę Fragnesia ma dwa `Fixes:`tagi. Jeden wskazuje na łatkę Dirty Frag ( `f4c50a4034e6`). Drugi wskazuje na oryginalne `skb_try_coalesce()`zatwierdzenie z 2013 roku ( `cef401de7be8`). Tagi opowiadają dwie historie w dwóch linijkach: natychmiastowy wyzwalacz i ukryty warunek wstępny.

![Oś czasu i porównanie pokazujące, jak łatka Dirty Frag stworzyła Fragnesię. Oś czasu obejmuje okres od 2013 roku (wprowadzenie skb_try_coalesce, zatwierdzenie cef401de7be8) do 8 maja 2026 roku (scalenie łatki Dirty Frag, zatwierdzenie f4c50a4034e6) do 13 maja 2026 roku (ujawnienie Fragnesii, CVE-2026-46300) i 15 maja 2026 roku (drugi wariant w skb_segment, niezałatany). Czerwony nawias wskazuje pięciodniową przerwę między łatką Dirty Frag a ujawnieniem Fragnesii. Poniżej osi czasu znajdują się dwa panele porównujące zachowanie przed i po łatce. Panel przed łatką oznaczony jako „latent” pokazuje, że esp_input nie sprawdził flagi shared-frag, a błąd flag-strip nie miał żadnego konsumenta produkcyjnego. Panel po zainstalowaniu poprawki oznaczony jako podatny na wykorzystanie pokazuje, że esp_input teraz sprawdza flagę shared-frag, ale skb_try_coalesce nadal ją pomija, przez co zapis do pamięci podręcznej stron staje się osiągalny jako trywialne lokalne zwiększenie uprawnień.](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1778925794757.svg)

## Seria Patch

Kandydat na łatkę Fragnesia ( `f84eca581739`, na liście netdev od 13 maja 2026 r.) opiera się na dwuliniowej zmianie w `skb_try_coalesce()`. Podczas przesyłania fragmentów stronicowanych między buforami, poprawiona funkcja propaguje teraz `SKBFL_SHARED_FRAG`flagę ze źródłowego skb do docelowego skb. `esp_input()`Przywrócona zostaje zależność od niezmiennika.

Pełna seria jest obszerniejsza, niż sugeruje dwuwierszowa poprawka w nagłówku. Oprócz naprawy rdzenia `skb_try_coalesce()`, zawiera ona poprawkę propagacji flagi w `pskb_copy()`, zmianę XFRM w celu uniknięcia odszyfrowywania w miejscu współdzielonych fragmentów SKB oraz grupę poprawek do rxrpc, obejmujących odszyfrowywanie pakietów DATA i RESPONSE, ponowne odszyfrowywanie pakietów RESPONSE, wyrównywanie rxkad, wycieki pamięci w `rxkad_verify_response()`oraz potencjalne użycie po zwolnieniu. Rozmiar serii poprawek sam w sobie wskazuje, że klasa błędów jest szersza niż jakikolwiek pojedynczy błąd.

Implikacja jest jeszcze szersza. Ten sam audyt należy powtórzyć dla każdej funkcji przesyłającej fragmenty między bazami danych SKB, ponieważ każda funkcja usuwająca flagę to potencjalnie kolejna Fragnesia czekająca na decyzję odbiorcy końcowego.

## Druga opcja

15 maja 2026 roku, dwa dni po pierwszym ujawnieniu Fragnesia, ten sam badacz V12 opublikował drugi wariant. Ten wariant omija scaloną poprawkę, wykorzystując `skb_segment()`zamiast tego `skb_try_coalesce()`. Funkcja propaguje `SKBFL_SHARED_FRAG`tylko z głównego pliku skb podczas budowania segmentów GSO, więc element frag_list przenoszący fragmenty oparte na pamięci podręcznej stron z ustawioną flagą będzie generował pliki skb segmentów, które utraciły znacznik.

Wywołanie drugiego wariantu wymaga trzech sieciowych przestrzeni nazw połączonych parami veth i jest mniej niezawodne niż pierwszy, ponieważ opiera się na łączeniu dwóch segmentów przez GRO w tym samym cyklu sondowania NAPI. W dniu publikacji pokoju, drugi wariant nie posiada scalonej poprawki. Zaproponowano osobną poprawkę na netdev, która mogłaby pomóc, ale nie została napisana w celu rozwiązania tego konkretnego błędu.

Istotą operacyjną jest to, że Fragnesia prawdopodobnie nie będzie ostatnią luką w zabezpieczeniach tego typu. Klasą błędu są naruszenia niezmienne w `SKBFL_SHARED_FRAG`. Każda funkcja w jądrze skb, która przesyła fragmenty, jest potencjalną lokalizacją dla kolejnej instancji.

**Informacje:** Wykrycie oryginalnych błędów Dirty Frag zajęło odpowiednio dziewięć i sześć lat od momentu zatwierdzenia ich wprowadzenia. Wykrycie Fragnesii zajęło pięć dni od zatwierdzenia, które je wprowadziło. Tempo wykrywania w tym obszarze kodu uległo zmianie, a zespół V12 publicznie przypisał to częściowo agencjom.Sztuczna inteligencja- wspomagany audyt. Niezależnie od tego, czy to ujęcie jest trafne, czy nie, w praktyce obrońcy powinni traktować poprawki jądra w tym podsystemie jako zmiany w powierzchni ataku, a nie jako gotowe działania łagodzące.

## Łączenie się z maszyną laboratoryjną

Po uruchomieniu komputera, w pokoju otwiera się terminal z podzielonym widokiem, zalogowany jako użytkownik nieuprawniony `karen`. Poniższe kroki należy wykonać w podanej kolejności w tym terminalu. Aby połączyć się z własnego komputera przez SSH, użyj nazwy użytkownika `karen`i hasła `fragnesia2026`:

```bash
ssh karen@10.128.145.38
```

W obu przypadkach otrzymasz ten sam komunikat.

## Krok 1: Potwierdź swój kontekst

```bash
karen@fragnesia:~$ id
uid=1001(karen) gid=1001(karen) groups=1001(karen)
```

Żadnych przywilejów, żadnych grup specjalnych.

## Krok 2: Zbuduj dowód koncepcji

Exploit znajduje się pod adresem `/home/karen/fragnesia/fragnesia.c`. Zbuduj go za pomocą następującego polecenia:

```bash
cd /home/karen/fragnesia
gcc -O2 -w fragnesia.c -o exp
```

Flaga `-w`blokuje kilka niegroźnych ostrzeżeń w opublikowanym kodzie źródłowym. Ostrzeżenia dotyczą nieużywanych funkcji pozostałych po programach debugujących programisty, `execve`argumentu innego niż null, od którego zależy exploit, oraz zignorowanej `write`wartości zwracanej w kodzie resetowania terminala. Żadne z nich nie wpływa na działanie exploita. Kompilacja kończy się w ciągu sekundy lub dwóch.

## Krok 3: Uruchomienie exploita (etap 1: Uszkodzenie pamięci podręcznej strony)

Eksploatacja Fragnesia to proces dwuetapowy. Etap pierwszy uszkadza kopię pamięci podręcznej stron za `/usr/bin/su`pomocą prymitywu zapisu espintcp; jest to zautomatyzowane w opublikowanym proof-of-concept. Etap drugi wyzwala uszkodzony plik binarny spoza przestrzeni nazw użytkownika, co powoduje wygenerowanie powłoki host-root. W proof-of-concept etap drugi nie jest wykonywany automatycznie; operator wykonuje to ręcznie po zakończeniu exploita.

Uruchom exploit:

```bash
./exp
```

Exploit drukuje długi ślad postępu w trakcie działania łańcucha. Poniższy wynik jest skrócony dla lepszej czytelności; rzeczywisty przebieg na komputerze laboratoryjnym jest o kilkaset wierszy dłuższy.

```bash
karen@fragnesia:~/fragnesia$ ./exp
[*] uid=1001 euid=1001 gid=1001 egid=1001
[*] mode=xfrm_espintcp_pagecache_replace collateral=after
[*] target=/usr/bin/su size=55680
outer_write_open_denied=1 errno=13 (Permission denied)
userns_setup: outer_uid=1001 outer_gid=1001 ns_uid=0 ns_gid=0
netns_setup=1
loopback_up=1
xfrm_espintcp_state_add=1
namespace_setup_complete=1
userns_root_mapped_to_outer_user_write_open_denied=1 errno=13 (Permission denied)
[*] timing: rx_pre_ulp=30000us tx_pre_splice=1000us rx_post_ulp=30000us
[*] range: offset=0x0 len=192 last=0xbf enc_len=4080 splice_len=4096
[*] payload=7f454c4602010100... (192 bytes of ELF stub)
stream0_table_entries=256
[*] smashing 192 bytes into read-only page cache  changed=176  skipped=16  remaining=0
  0000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00
  0010  02 00 3e 00 01 00 00 00  78 00 40 00 00 00 00 00
  ...
  00b0  2f 62 69 6e 2f 73 68 00  00 00 00 00 00 00 00 00
  [==================================================] 192/192 (100%)
[*] verifying 192 bytes...
[*] bytes_flip_summary len=192 changed=176 skipped=16
[+] BUG: changed requested copied byte range to desired values
# whoamiroot# cat /root/flag.txtcat: /root/flag.txt: Permission denied
```

Znak zachęty powłoki zmienił się z `$`na `#`i `whoami`zwraca `root`. To jest krok weryfikacji koncepcji proof-of-concept, ale powłoka, do której trafia, nie jest jeszcze powłoką host-root. Kilka szczegółów z tego wyniku zasługuje na bliższą uwagę przed przejściem do etapu drugiego.

- Ten wiersz `outer_write_open_denied=1 errno=13`potwierdza, że ​​Karen nie ma dostępu do zapisu `/usr/bin/su`spoza przestrzeni nazw. To jest granica uprawnień, którą exploit zamierza przekroczyć.
- Linia `userns_setup: ... ns_uid=0 ns_gid=0`pokazuje, że karen jest mapowana na UID 0 w nowym użytkownikuprzestrzeń nazw, przyznając uprawnienia `CAP_NET_ADMIN`do operacji XFRM, które następują bez żadnych rzeczywistych uprawnień na hoście.
- Ten `changed=176 skipped=16`wiersz jest istotny. Plik szczątkowy ELF exploita ma 192 bajty długości, ale `/usr/bin/su`sam jest plikiem binarnym ELF, więc jego pierwsze kilka bajtów ( `7f 45 4c 46 02 01 01 00 ...`) już pasuje do pliku szczątkowego. Pętla per bajt pomija te bajty i zapisuje tylko te 176 różniących się bajtów.
- Powłoka, która pojawia się później, `[+] BUG: ...`to wywołanie proof-of-concept `execve("/usr/bin/su")`działające w przestrzeni nazw użytkownika. W przestrzeni nazw zmienna karen jest mapowana na UID 0, więc kod powłoki `setuid(0)`to no-op, a wynikowa powłoka toprzestrzeń nazw-źródło.
- Zwracana `cat /root/flag.txt`wartość `Permission denied`jest `/root/flag.txt`własnością rzeczywistego UID hosta 0, którego przestrzeń nazw nie może odczytać. Przestrzeń nazw przedstawia pliki należące do niezmapowanych UID-ów jako należące do `nobody`(Identyfikator użytkownika65534).

To jest oczekiwany rezultat etapu pierwszego. Korupcja została dokonana, ale granica uprawnień hosta nie została jeszcze przekroczona. Etap drugi to robi.

## Krok 4: Wywołaj korupcję z zewnątrzPrzestrzeń nazw

Wyjdźprzestrzeń nazwshell, aby powrócić do zwykłej powłoki Karen:

```bash
# exit
```

Monit powraca do `karen@tryhackme-2204:~/fragnesia$`, wskazując, że ponownie znajdujesz się poza przestrzenią nazw jako UID 1001. Pamięć podręczna stron jest jednak nadal uszkodzona. Pamięć podręczna stron jądra jest globalna dla hosta i jest przechowywana poza granicami przestrzeni nazw; tylko usunięcie lub użycie polecenia a `drop_caches`mogłoby ją wyczyścić.

Teraz uruchom `/usr/bin/su`z normalnej powłoki Karen:

```bash
/usr/bin/su
```

```bash
karen@fragnesia:~/fragnesia$ /usr/bin/su
# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root)
```

Tym razem powłoka to rzeczywiście host-root. Sekwencja zdarzeń na poziomie jądra jest następująca.

1. `execve`Powłoka Karen `/usr/bin/su`. Plik na dysku ma ustawiony bit setuid z właścicielem root.
2. Jądro respektuje bit setuid i ustawia efektywny UID procesu na 0 (rzeczywisty UID hosta wynosi 0, ponieważ powłoka Karen znajduje się w początkowej przestrzeni nazw użytkownika).
3. Jądro ładuje bajty pliku binarnego z pamięci podręcznej stron, która nadal zawiera uszkodzony szczątkowy kod ELF.
4. Uszkodzony punkt wejścia uruchamia kod powłoki pod efektywnym UID 0.
5. Wywołania shellcode `setgid(0)`i `setuid(0)`. Ponieważ efektywny UID jest już równy 0 na poziomie hosta, `setuid(0)`operacja kończy się powodzeniem i ustawia rzeczywistyIdentyfikator użytkownikarównież do 0.
6. Kod powłoki wywołuje `execve("/bin/sh", ...)`, tworząc powłokę z prawdziwym UID 0.

Rezultatem jest prawdziwa powłoka host-root. Fakt, że krok dotyczący przestrzeni nazw był potrzebny do uzyskania dostępu `CAP_NET_ADMIN`do operacji XFRM, jest teraz nieistotny; powłoka jest potomkiem zwykłej powłoki Karen i działa całkowicie poza systemem użytkownika.przestrzeń nazw.

## Krok 5: Przeczytaj flagę

Z poziomu powłoki hosta-root flagę można teraz odczytać:

```bash
# cat /root/flag.txt
```

Błąd „Odmowa dostępu” z etapu pierwszego zniknął, ponieważ proces ma teraz rzeczywisty identyfikator UID hosta 0, a nie identyfikator UID przestrzeni nazw 0.

## Krok 6: Zweryfikuj plik na dysku

Sprawdź, czy plik binarny na dysku nigdy nie został zmodyfikowany:

```bash
# sha256sum /usr/bin/su
```

Skrót pasuje do świeżo zainstalowanej kompilacji jądra Ubuntu. Exploit zmodyfikował jedynie kopię w pamięci podręcznej stron; plik binarny na dysku nie został w żaden sposób zmodyfikowany. AIDE, Tripwire, IMA i każde inne narzędzie do sprawdzania integralności plików, które odczytuje dane z dysku, wskazywałoby ten plik jako czysty. Uszkodzenie występuje tylko w pamięci podręcznej stron jądra i jest widoczne tylko dla procesów odczytujących dane z tej pamięci.

## Krok 7: Wyjdź i usuń pamięć podręczną stron

Dowód koncepcji nie czyści się automatycznie po sobie, więc kolejne wywołania `su`będą nadal uruchamiać powłokę główną, aż uszkodzone strony zostaną usunięte. Usuń je ręcznie przed opuszczeniem komputera:

```bash
# exit
karen@fragnesia:~/fragnesia$ sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

Jądro usuwa uszkodzone strony z pamięci podręcznej. Podczas kolejnego odczytu ponownie `/usr/bin/su`ładuje czystą kopię z dysku i `/usr/bin/su`powraca do normalnego działania.

**Ostrzeżenie:** Ponowne uruchomienie exploita po usunięciu pamięci podręcznej jest dozwolone. Pamięć podręczna stron jest ładowana z czystego dysku za każdym razem, a exploit uszkadza nową stronę za każdym razem. Pozostawianie komputera z uszkodzonymi stronami w pamięci podręcznej to niehigieniczne rozwiązanie; zawsze należy go wyłączyć lub zrestartować po testach.

Schemat eksploatacji Fragnesia można wykryć w czasie rzeczywistym za pomocą tego samego podejścia do monitorowania wywołań systemowych, które jest używane w przypadku Copy Fail i Dirty Frag, z jednym konkretnym sygnałem, który jest nowością w tym przypadkuCVE.

## Wykrywanie

Sygnaturą exploita jest sekwencja wywołań systemowych, których nie generuje żadna legalna aplikacja:

- `unshare(CLONE_NEWUSER | CLONE_NEWNET)`po czym pisze do`/proc/self/uid_map`
- `socket(AF_ALG, ...)`wywołania używane do zbudowania tabeli wyszukiwania strumienia kluczy
- A `socket(AF_INET, SOCK_STREAM)`po którym wkrótce następuje`setsockopt(SOL_TCP, TCP_ULP, "espintcp")`
- `splice()`z deskryptora pliku binarnego setuid do tego samego gniazda TCP
- Seria `XFRM_MSG_NEWSA`komunikatów netlink rejestrujących skojarzenie zabezpieczeń ze znanym kluczem AES-128-GCM
- Proces ostateczny `execve("/usr/bin/su", ...)`i proces potomny działający z efektywnym UID 0

setsockopt `TCP_ULP = "espintcp"`to pojedynczy sygnał o najwyższej wierności. Legalne użycie espintcp jest rzadkie; występuje głównie we wdrożeniach strongSwan skonfigurowanych do przechodzenia NAT w środowiskach, w których protokół ESP z enkapsulacją UDP nie działa. Proces spoza tego niewielkiego zbioru demonów wydających setsockopt jest nietypowy; proces spoza zbioru, który wydaje setsockopt, a następnie natychmiast dołącza plik binarny o identyfikatorze setuid do gniazda, jest eksploitem.

![Diagram sekwencji wywołań systemowych Fragnesia z punktami detekcji. Użytkownik bez uprawnień po lewej stronie wprowadza dane do sześciu ponumerowanych kroków, które są wykonywane w jądrze Linuksa po prawej stronie. Krok 1, unshare z CLONE_NEWUSER i CLONE_NEWNET, monitorowany za pomocą reguły auditd przy unshare z a0=0x10000000. Krok 2, tworzenie gniazda AF_ALG SOCK_SEQPACKET, monitorowane za pomocą reguły Falco dla gniazd AF_ALG z procesów innych niż kcapi. Krok 3, otwieranie gniazda TCP i wklejanie do niego /usr/bin/su, monitorowane za pomocą reguły Falco przy wklejaniu pliku binarnego setuid do gniazda TCP, oznaczonego jako sygnał wysokiej wierności. Krok 4, setsockopt z TCP_ULP ustawionym na espintcp, monitorowany za pomocą reguły Falco dla procesów innych niż strongSwan, aktywujących espintcp, pojedynczy sygnał najwyższej wierności. Krok 5, 192 wyzwalacze odszyfrowywania AES-GCM w miejscu, monitorowane za pomocą telemetrii ruchu XFRM SA w pętli zwrotnej. Krok 6, wykonanie /usr/bin/su, dające UID 0 dla dziecka, monitorowane za pomocą korelacji auditd w poprzednich krokach.](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1778925830227.svg)

Reguła auditd przechwytująca ścieżkę setsockopt:

```markdown
-a always,exit -F arch=b64 -S setsockopt -F a0!=-1 -k fragnesia_setsockopt
-a always,exit -F arch=b64 -S unshare -F a0=0x10000000 -k fragnesia_unshare
-a always,exit -F arch=b64 -S splice -k fragnesia_splice
```

Pierwsza reguła rejestruje wszystkie wywołania setsockopt (API jądra auditd nie pozwala na filtrowanie bezpośrednio po argumencie optname); korelacja musi zostać przeprowadzona w systemie SIEM. Druga reguła rejestruje `unshare()`wywołania zawierające `CLONE_NEWUSER`( `0x10000000`). Trzecia reguła rejestruje wszystkie wywołania splice, które mogą być bardzo głośne; ogranicz zakres, dodając `-F path=/usr/bin/su`lub podobnie, jeśli podsystem audytu to obsługuje.

Reguła Falco przechwytująca specyficzny dla Fragnesia sygnał aktywacji espintcp ULP po połączeniu pliku binarnego o identyfikatorze setuid z tym samym gniazdem TCP:

```markdown
- list: setuid_binaries
  items: [/usr/bin/su, /bin/su, /usr/bin/sudo, /usr/bin/passwd, /usr/bin/chsh]

- macro: espintcp_legitimate_processes
  condition: >
    proc.name in (charon, charon-systemd, pluto, swanctl)

- rule: Potential Fragnesia exploit (espintcp ULP after splice)
  desc: >
    Detects an unprivileged process that splices a setuid binary into a
    TCP socket and then activates the espintcp ULP on it, the trigger
    pattern for CVE-2026-46300.
  condition: >
    (evt.type = splice and fd.name in (setuid_binaries)) or
    (evt.type = setsockopt and evt.arg.optname = TCP_ULP and
     not espintcp_legitimate_processes)
  output: >
    Potential Fragnesia trigger
    (user=%user.name uid=%user.uid command=%proc.cmdline pid=%proc.pid
     fd=%fd.name container_id=%container.id)
  priority: CRITICAL
  
```

Pierwsze ramię warunku przechwytuje stronę pamięci podręcznej stron wchodzącą doTCPgniazdo. Drugie ramię przechwytuje aktywację ULP espintcp, która uruchamia odszyfrowanie AES-GCM w miejscu. Każdy z tych sygnałów z osobna jest podejrzany; oba sygnały w tym samym procesie w ciągu kilku sekund oznaczają wykorzystanie luki. Należy zauważyć, że lista dozwolonych procesów dla ULP espintcp jest niewielka — `charon`demon strongSwan i kilka powiązanych demonów IKE. Każdy proces spoza tej listy aktywujący espintcp wymaga zbadania.

## Kluczowe wywołania systemowe do monitorowania

|Wywołanie systemowe|Na co zwrócić uwagę|Znaczenie|
|---|---|---|
|`unshare(CLONE_NEWUSER \| CLONE_NEWNET)`|Proces bez uprawnień tworzący obie przestrzenie nazw|Pierwszy krok na drodze do pewności siebie|
|`setsockopt(TCP_ULP, "espintcp")`|Proces nie znajduje się na znanej liście demonów strongSwan/IPsec|Specyficzne dla Fragnezji, bardzo niski poziom fałszywie dodatnich wyników|
|`socket(AF_ALG, ...)`z`SOCK_SEQPACKET`|Proces nie jest włączony `kcapi-*`lub `cryptsetup`ustawiony|Ten sam sygnał jest używany do wykrywania błędów kopiowania|
|`splice()`z binarnego fd o identyfikatorze setuid do gniazda TCP fd|Strona pamięci podręcznej stron wchodząca do kolejki odbiorczej TCP|Przygotowanie spustu|
|`XFRM_MSG_NEWSA`połączenie sieciowe ze znanym słabym kluczem|Nietypowy wzór rejestracji SA|Rejestracja hurtowa SA w mikrosekundach|

## Mapowanie MITRE ATT&CK

|Technika|MITRE ID|Gdzie się pojawia|
|---|---|---|
|Wykorzystanie w celu eskalacji uprawnień|T1068|Samo jądro LPE|
|Mechanizm kontroli nadużyć: Setuid i Setgid|T1548.001|`execve("/usr/bin/su")`po uszkodzeniu pamięci podręcznej strony|
|Ucieczka do gospodarza|T1611|Gdy exploit jest uruchamiany z wnętrza kontenera|
|Demontaż wskaźnika|T1070|Instrukcja `drop_caches`po eksploatacji|

## Łagodzenie

Kandydat na poprawkę upstream został zatwierdzony `f84eca581739`i opublikowany na liście mailingowej netdev 13 maja 2026 r. Jest to dwulinijkowa zmiana, `skb_try_coalesce()`która zachowuje `SKBFL_SHARED_FRAG`znacznik podczas przesyłania fragmentów stronicowanych. W momencie przygotowywania pokoju poprawka oczekiwała na recenzję opiekuna i nie została jeszcze scalona z drzewem Linusa.

Poprawki dystrybucyjne pojawiają się przed scaleniem głównej linii dystrybucji. AlmaLinux opublikował 13 maja poprawione kernele dla AL8, AL9 i AL10 w swoim repozytorium testowym, 14 maja odświeżył kompilacje, aby uwzględnić poprawki, i przenosi je do produkcji po zakończeniu testów społecznościowych. CloudLinux, SUSE, Debian i Ubuntu opublikowały ostrzeżenia; status poszczególnych wydań jest różny i aktualizowany w miarę pojawiania się poprawek.

Dopóki dystrybucja nie dostarczy poprawionego jądra, ta sama lista denylist modprobe, co w przypadku Dirty Frag, będzie skuteczna przeciwko Fragnesia.

**Krok 1: Zastosuj listę blokowanych modułów**

```bash
sudo sh -c 'printf "install esp4 /bin/false\ninstall esp6 /bin/false\ninstall rxrpc /bin/false\n" > /etc/modprobe.d/dirtyfrag.conf'
sudo rmmod esp4 esp6 rxrpc 2>/dev/null
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

Plik konfiguracyjny blokuje przyszłe ładowanie `esp4`, `esp6`i `rxrpc`. Ten `rmmod`wiersz usuwa wszystkie aktualnie załadowane kopie. Ten `drop_caches`wiersz usuwa wszystkie uszkodzone strony znajdujące się już w pamięci podręcznej.

**Krok 2: Sprawdź, czy blok jest aktywny**

```bash
sudo modprobe esp4
```

Polecenie powinno zwrócić błąd. Moduł jest zablokowany i nie można go załadować.

**Krok 3: Potwierdź, że PoC nie powiodło się**

Uruchom ponownie exploit:

```bash
/home/karen/fragnesia/exp
```

Exploit powinien zakończyć się niepowodzeniem, gdy polecenie espintcp ULP setsockopt zostanie odrzucone, ponieważ `esp4`moduł nie jest już dostępny. Łańcuch nie może przejść dalej.

**Ostrzeżenie:** Lista zakazów blokuje legalne korzystanie z IPsec ESP i AFS RxRPC. Hosty produkcyjne korzystające z klientów strongSwan, libreswan lub AFS nie powinny stosować tego zabezpieczenia; zamiast tego potrzebują poprawionego jądra. W środowiskach programistycznych i laboratoryjnych oraz w przypadku większości obciążeń serwerowych, które nie korzystają z tych protokołów, moduły są nieużywane, a lista zakazów jest bezpieczna. Co ważne, organizacje, które zastosowały listę zakazów modprobe w ramach ochrony przed atakami Dirty Frag, są już chronione przed atakiem Fragnesia. Organizacje, które zastosowały jedynie poprawkę jądra Dirty Frag, nie są chronione.

## Status poprawki w momencie ujawnienia

Ujawnienie Fragnesia skróciło typowy harmonogram od wydania poprawki do jej ujawnienia. PoC, poprawka kandydacka i publiczny opis pojawiły się tego samego dnia, bez embarga. Dwulinijkowy charakter poprawki i niewielka liczba `Fixes:`tagów (dwa) sugerują, że ten sam obszar kodu będzie przedmiotem większej uwagi audytorów w nadchodzących tygodniach, a niezałatany drugi wariant `skb_segment()`już to potwierdza.

Dotknięte tym problemem kernele obejmują wszystkie wydania sprzed 13 maja 2026 roku, w tym poprawkę Dirty Frag. Starsze kernele bez poprawki Dirty Frag zawierają błąd `skb_try_coalesce()`, ale nie mają użytkownika, który podejmowałby decyzję na podstawie flagi „stripped”; technicznie rzecz biorąc, są one dotknięte ukrytą wadą, ale nie można ich wykorzystać konkretnie za pośrednictwem Fragnesia.

Fragnesia to prymitywny mechanizm zapisu jednobajtowej pamięci podręcznej stron wLinuxkernel, który powstał w wyniku regresji wprowadzonej przez wcześniejszą poprawkę bezpieczeństwa. Jest to trzecia luka w tej klasie ujawniona w ciągu trzech tygodni, obok Copy Fail i Dirty Frag, a drugi wariant opublikowany dwa dni po pierwotnym ujawnieniu pozostaje niezałatany w dniu publikacji artykułu.

Z tego łańcucha ujawnień można wyciągnąć dwie praktyczne lekcje, które warto wdrożyć.

Pierwsza lekcja jest taka, że ​​poprawki jądra nie są zdarzeniami powstrzymującymi dla klasy błędów. Poprawka Dirty Frag usunęła pierwotne błędy, ale dokonała tego poprzez wprowadzenie nowego kodu, który ufa inwariantowi. Inwariant nie został zweryfikowany, a luka w audycie stała się Fragnesia. Osoby odpowiedzialne za obronę powierzchni ataku przylegających do jądra powinny traktować każdą poprawkę w podsystemach, takich jak XFRM, AF_ALG, io_uring,BPF, a RxRPC jako zmianę powierzchni ataku, a nie jako kompletne rozwiązanie łagodzące. Kolejne audyty w tym samym podsystemie są uzasadnione, a nie opcjonalne.

Druga lekcja jest taka, że ​​klasa zapisu do pamięci podręcznej stron jest na tyle ogólna, że ​​poprawki dystrybucyjne nie rozwiążą problemu same w sobie. Plik na dysku nigdy nie jest modyfikowany, więc plikuczciwośćNarzędzia te całkowicie pomijają uszkodzenie. Wykrywanie musi odbywać się na poziomie wywołań systemowych, w czasie rzeczywistym, z wykorzystaniem reguł monitorujących sekwencje wywołań systemowych, których nie generuje żadna legalna aplikacja. Sama analiza śledcza systemu plików nie ujawni tego ataku po fakcie.

Trzecia kwestia operacyjna dotyczy pojemnik środowiskach. Pamięć podręczna stron jest współdzielona przez wszystkie procesy korzystające z tego samego jądra, w tym każdy pojemnik Na tym samym hoście. Proces konteneryzowany, który może tworzyć nieuprzywilejowane przestrzenie nazw użytkowników, co jest domyślne w przypadku wdrożeń Docker i Podmana bez uprawnień roota, spełnia wszystkie wymagania wymagane przez exploit Fragnesia. Uprzywilejowane kontenery nie są wymagane, ani żadne specjalne możliwości. Obsługa wielu najemców. Kubernetes klastry, współdzielone CIbiegaczy i każdego hosta działającego bez rootapojemnikobciążenia należy traktować jako narażone do momentu zainstalowania poprawki jądra.

Aktualizacja jądra do kompilacji zawierającej scaloną poprawkę Fragnesia powinna zostać zastosowana, gdy tylko zostanie udostępniona w dystrybucji. Lista dezaktywacji modprobe  `esp4`, `esp6`, i `rxrpc`stanowi skuteczną tymczasową kontrolę na hostach, które nie są zależne od tych modułów, a także chroni przed niezałatanym drugim wariantem. Użytkownicy korzystający z klientów strong Swan, libreswan lub AFS w środowisku produkcyjnym będą musieli poczekać na poprawki przeniesione przez dostawcę.

Poniżej masz obszerną notatkę w prostym języku. Opis dotyczy Fragnesii, czyli podatności CVE-2026-46300, która pojawiła się w jądrze Linux i wiąże się z błędnym obchodzeniem się z fragmentami pakietów oraz ścieżką ESP-in-TCP.mallory+1

## O co chodzi

Ta podatność pokazuje ważną lekcję: nawet poprawka bezpieczeństwa może wprowadzić nową lukę, jeśli naprawia jeden fragment logiki, ale nie zachowa wszystkich wcześniejszych założeń bezpieczeństwa.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)  
W praktyce oznacza to, że programista usuwa jeden problem, ale w innym miejscu tego samego przepływu pojawia się nowa dziura, często na tej samej powierzchni ataku.[tlctc](https://www.tlctc.net/cve-2026-46300.html)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
To jest szczególnie groźne w jądrze systemu, bo ma ono dużo zależności i jedna mała zmiana może wpłynąć na wiele ścieżek przetwarzania.tuxcare+1

## Dlaczego poprawka może stworzyć nową lukę

Poprawki bezpieczeństwa często zmieniają sposób, w jaki dane są kopiowane, łączone albo sprawdzane.[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)  
Jeśli przy tej zmianie nie zostanie zachowany ważny znacznik, warunek lub ograniczenie, inna część systemu może uznać dane za bezpieczne mimo że takie nie są.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)  
W Fragnesii właśnie taki problem pojawia się w łańcuchu przetwarzania fragmentów SKB: poprawka w jednym miejscu miała chronić przed błędem, ale pozostawiła ścieżkę, która pozwala na niebezpieczne przetwarzanie w innym miejscu.[mallory](https://mallory.ai/vulnerabilities/019e222f-db67-7250-ad09-63116dce5432)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
To dobry przykład regresji bezpieczeństwa: łatka zamyka jedną dziurę, ale otwiera inną w tym samym obszarze kodu.tuxcare+1

## Rola skb_try_coalesce()

`skb_try_coalesce()` to funkcja jądra, która próbuje połączyć fragmenty pakietów sieciowych w jeden bardziej spójny obiekt SKB.tuxcare+1  
W uproszczeniu: zamiast trzymać kilka kawałków danych osobno, kernel stara się je „skleić”, żeby oszczędzić pamięć i przyspieszyć przetwarzanie.[mallory](https://mallory.ai/vulnerabilities/019e222f-db67-7250-ad09-63116dce5432)  
Właśnie w tym miejscu powstaje problem, bo przy łączeniu fragmentów może zostać zgubiony ważny marker bezpieczeństwa.tuxcare+1  
Jeżeli ten marker zniknie, dalsze warstwy systemu mogą błędnie uznać fragment za zwykły, nieudostępniany blok danych.[cert](https://www.cert.ug/fragnesia-linux-kernel-local-privilege-escalation-xfrm-esp-tcp-cve-2026-46300)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)

## Rola SKBFL_SHARED_FRAG

`SKBFL_SHARED_FRAG` to znacznik mówiący, że dany fragment jest współdzielony i nie wolno go traktować jak prywatnej, bezpiecznej pamięci do in-place modyfikacji.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[mallory](https://mallory.ai/vulnerabilities/019e222f-db67-7250-ad09-63116dce5432)  
To bardzo ważne, bo współdzielone fragmenty mogą wskazywać na dane pochodzące z page cache, czyli obszaru pamięci używanego przez system plików.[cert](https://www.cert.ug/fragnesia-linux-kernel-local-privilege-escalation-xfrm-esp-tcp-cve-2026-46300)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
Jeżeli ten marker zostanie utracony, kernel może pomyśleć, że wolno wykonać zapis „na miejscu”, choć w rzeczywistości nadpisuje współdzielone dane.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)  
Właśnie to prowadzi do korupcji page cache i później do możliwości nadpisywania plików tylko do odczytu.cloud.tencent+1

## Ścieżka espintcp

Ścieżka odbiorcza `espintcp` odnosi się do obsługi pakietów ESP w tunelowaniu TCP w ramach XFRM/IPsec.[cert](https://www.cert.ug/fragnesia-linux-kernel-local-privilege-escalation-xfrm-esp-tcp-cve-2026-46300)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
W normalnej sytuacji kernel powinien sprawdzić, czy dane są współdzielone, i jeśli tak, zrobić bezpieczną kopię zamiast odszyfrowywać je bezpośrednio w miejscu.[tenable](https://www.tenable.com/blog/fragnesia-cve-2026-46300-faq-about-new-linux-kernel-xfrm-esp-in-tcp-priv-esc)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
Problem polega na tym, że po utracie markera `SKBFL_SHARED_FRAG` ścieżka odbiorcza może uznać, że wolno wykonać odszyfrowanie AES-GCM in-place.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[cert](https://www.cert.ug/fragnesia-linux-kernel-local-privilege-escalation-xfrm-esp-tcp-cve-2026-46300)  
Jeżeli taki zapis trafia w stronę page cache, to może zmienić zawartość pliku, którego nie powinno się dać modyfikować.cloud.tencent+1

## Warunki podatnej ścieżki

Żeby ta ścieżka zadziałała, muszą być spełnione konkretne warunki środowiskowe.tenable+1  
Po pierwsze, musi istnieć podatna wersja jądra, w której marker współdzielonego fragmentu jest tracony podczas koalescencji SKB.tuxcare+1  
Po drugie, musi być aktywna ścieżka XFRM ESP-in-TCP, bo to ona korzysta z informacji o fragmencie przy decyzji o dekodowaniu.tenable+1  
Po trzecie, z punktu widzenia efektu ataku, dane muszą być powiązane z page cache, aby możliwy był zapis do strony używanej przez plik tylko do odczytu.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)

## Dlaczego to jest groźne

Najgorszy scenariusz to sytuacja, w której zwykły użytkownik lokalny może wpłynąć na zawartość chronionego pliku systemowego przez page cache.cloud.tencent+1  
W praktyce oznacza to możliwość podmiany fragmentów programu uprzywilejowanego, a potem uruchomienia go z podniesionymi uprawnieniami.cloud.tencent+1  
To dlatego opisy tej podatności mówią o lokalnym podniesieniu uprawnień i o deterministycznym, stabilnym efekcie exploita.tenable+1  
Ważne jest też to, że jest to kolejny przykład powtarzającej się klasy regresji w tym samym obszarze: zarządzanie fragmentami sieciowymi i ochrona page cache.cloud.tencent+1

## Wzorzec powtarzających się regresji

Tego typu błędy uczą, że sam fakt posiadania poprawki nie oznacza pełnego bezpieczeństwa.tuxcare+1  
Jeżeli wcześniejsza luka została naprawiona tylko częściowo, to później ktoś może odtworzyć podobny efekt inną drogą w tym samym subsystemie.cloud.tencent+1  
Dlatego warto projektować wykrywanie nie tylko pod jeden konkretny CVE, ale pod całą rodzinę zachowań: utrata znaczników, zła decyzja o kopiowaniu, in-place write do współdzielonej pamięci, oraz przetwarzanie danych z page cache.tuxcare+1  
To podejście jest skuteczniejsze niż reagowanie wyłącznie na pojedynczy numer podatności.[tlctc](https://www.tlctc.net/cve-2026-46300.html)

## Łagodzenie przez modprobe

Z opisu dostępnego rozwiązania wynika, że tymczasowa łagodząca metoda polega na zablokowaniu ładowania modułów związanych z ryzykowną ścieżką, zwłaszcza `esp4`, `esp6` i czasem `rxrpc`, przy użyciu reguł modprobe.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)  
Taki krok ma sens jako obejście awaryjne, gdy nie da się od razu wdrożyć poprawionego jądra.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)  
Trzeba jednak pamiętać, że to rozwiązanie może wpływać na działanie usług korzystających z IPsec lub powiązanych funkcji sieciowych.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)  
Po wdrożeniu obejścia należy zweryfikować, że podatna ścieżka nie jest już dostępna, a testowy proof-of-concept nie działa.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)

## Jak myśleć o obronie

Najlepsza obrona ma trzy warstwy.  
Pierwsza to aktualizacja jądra do wersji naprawionej.[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)  
Druga to tymczasowe ograniczenie ładowania ryzykownych modułów, jeśli patch nie może być wdrożony od razu.[cloud.tencent](https://cloud.tencent.com/document/product/1397/131629)  
Trzecia to wykrywanie wzorca, a nie tylko pojedynczego CVE: każda sytuacja, w której znacznik współdzielonego fragmentu ginie, a później pojawia się in-place decrypt lub write do page cache, powinna być traktowana jako sygnał alarmowy.[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)[tlctc](https://www.tlctc.net/cve-2026-46300.html)

## Najkrótsze podsumowanie

Fragnesia pokazuje, że łatka może przypadkiem stworzyć nową lukę, jeśli nie zachowa wszystkich warunków bezpieczeństwa.[tuxcare](https://tuxcare.com/blog/fragnesia-cve-2026-46300/)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
`skb_try_coalesce()` odpowiada za scalanie fragmentów, a `SKBFL_SHARED_FRAG` mówi, że fragment jest współdzielony i nie wolno go traktować jak prywatnego.[mallory](https://mallory.ai/vulnerabilities/019e222f-db67-7250-ad09-63116dce5432)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
Gdy marker zniknie, ścieżka `espintcp` może odszyfrować dane w miejscu, co przy odpowiednich warunkach prowadzi do zapisu w page cache.[cert](https://www.cert.ug/fragnesia-linux-kernel-local-privilege-escalation-xfrm-esp-tcp-cve-2026-46300)[youtube](https://www.youtube.com/watch?v=PW2qe7cZJVc)  
Dlatego warto patrzeć szerzej niż na jedną podatność i budować ochronę oraz detekcję wokół całej klasy błędów.
