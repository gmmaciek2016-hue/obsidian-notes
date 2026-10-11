---

Nowoczesne aplikacje internetowe w dużym stopniu opierają się na uwierzytelnianych sesjach, aby wykonywać działania w imieniu użytkowników. Gdy logujesz się do witryny, Twoja przeglądarka zapisuje plik cookie sesji Pozwala to aplikacji rozpoznawać użytkownika w przyszłych żądaniach. Chociaż ułatwia to korzystanie z aplikacji internetowych, stwarza również atakującym możliwości nadużycia tego zaufania. Jednym z takich ataków jest Cross-Site Request Forgery (CSRF).

Zamiast kraść dane uwierzytelniające, CSRF oszukuje przeglądarkę ofiary, zmuszając ją do wykonania czynności na stronie internetowej, na której ofiara jest już uwierzytelniona. Ponieważ przeglądarka automatycznie dołącza pliki cookie do żądań, aplikacja internetowa może uznać złośliwe żądanie za uzasadnione.

W tym pomieszczeniu dowiesz się, w jaki sposób atakujący wykorzystują to zachowanie i jak testerzy penetracyjni mogą identyfikować podatne punkty końcowe w rzeczywistych aplikacjach internetowych.

## Cele edukacyjne

- Zrozumieć podstawową koncepcję CSRF ataki
- Zidentyfikuj funkcje aplikacji, które są podatne na CSRF
- Wykorzystać CSRF używając prostego HTML i słabych tokenów 
- Zrozum powszechne praktyki stosowane w celu wykorzystania CSRF

## Scenariusz

W tym pokoju będziesz korzystać z prostego portalu pracowniczego o nazwie `StaffHub`. Ta wewnętrzna aplikacja umożliwia pracownikom aktualizację ustawień konta, w tym adresu e-mail i preferencji profilu.

Twoim celem jako pentestera jest analiza sposobu wykonywania tych działań i określenie, czy mogą one zostać uruchomione bez wiedzy użytkownika. Jeśli aplikacja nie weryfikuje prawidłowo źródła żądań, atakujący mogą oszukać uwierzytelnionych użytkowników i skłonić ich do nieświadomej modyfikacji ustawień własnego konta.

CSRF to luka w zabezpieczeniach sieci, w której atakujący oszukuje przeglądarkę użytkownika, aby wysłała żądanie do witryny, w której użytkownik jest już uwierzytelniony. Ponieważ przeglądarka automatycznie dołącza pliki cookie sesji do każdego żądania, aplikacja internetowa zakłada, że ​​żądanie zostało celowo wysłane przez użytkownika.

Zamiast kraść dane logowania, atakujący nadużywa relacji zaufania między przeglądarką a aplikacją internetową. Jeśli żądanie wykonuje poufną czynność, taką jak zmiana adresu e-mail lub aktualizacja ustawień konta, atakujący może być w stanie zmodyfikować konto ofiary bez jej wiedzy.

Wyobraźmy sobie na przykład, że użytkownik jest zalogowany do wewnętrznego portalu podczas przeglądania internetu. Jeśli użytkownik odwiedzi złośliwą stronę internetową, strona ta może dyskretnie wygenerować żądanie do portalu. Jeśli aplikacja nie zweryfikuje pochodzenia żądania, może je przetworzyć tak, jakby zostało zainicjowane przez użytkownika.

## Jak CSRF Ataki działają

![Jak działa CSRF.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775481672467.png)Typowy CSRF Atak zazwyczaj przebiega w trzech prostych krokach: 

- Ofiara loguje się do legalnej aplikacji internetowej, a jej przeglądarka zapisuje plik cookie sesji.
- Atakujący podstępem nakłania ofiarę do odwiedzenia złośliwej strony internetowej zawierającej spreparowane żądanie.
- Przeglądarka ofiary automatycznie wysyła żądanie do aplikacji docelowej wraz z zapisanymi danymiplik cookie sesji.

Ponieważ żądanie zawiera prawidłową plik cookie sesji, serwer traktuje to jako legalną akcję użytkownika.

## Dlaczego to jest niebezpieczne

CSRF Ataki mogą być wykorzystywane do wykonywania wielu czynności, w zależności od funkcjonalności aplikacji docelowej, takich jak:

- Zmiana adresu e-mail użytkownika
- Aktualizowanie ustawień konta
- Wykonywanie transakcji finansowych
- Modyfikowanie preferencji zabezpieczeń

Mimo że ofiara nigdy nie miała zamiaru wykonać tej czynności, aplikacja internetowa traktuje ją jako uzasadnione żądanie.

W poniższych zadaniach przyjrzymy się, w jaki sposób atakujący identyfikują podatne funkcje i tworzą złośliwe żądania w celu wykorzystania tego zachowania.

Zrozumienie dlaczego CSRF Ważne jest, aby upewnić się, że wszystko działa, zanim spróbujesz to wykorzystać. Luka nie istnieje, ponieważ przeglądarki są uszkodzone. W rzeczywistości przeglądarki zachowują się dokładnie tak, jak zostały zaprojektowane. Problem pojawia się, gdy aplikacja internetowa zbyt mocno ufa żądaniom.

Gdy użytkownik loguje się do witryny internetowej, serwer zazwyczaj tworzy sesję i wysyła plik cookie sesji do przeglądarki. Ten plik cookie działa jak dowód tożsamości. Za każdym razem, gdy przeglądarka wysyła żądanie do danej witryny, plik cookie jest automatycznie dołączany, dzięki czemu serwer wie, który użytkownik wysyła żądanie.

Kluczowym szczegółem jest to, że przeglądarka automatycznie wysyła pliki cookie z każdym żądaniem do tej samej domeny. Nie ma znaczenia, czy żądanie pochodzi z legalnej strony w witrynie, czy ze złośliwej strony internetowej znajdującej się gdzie indziej w internecie.

Na przykład, jeśli użytkownik jest zalogowany do staffhub.thmi odwiedzi inną witrynę, witryna ta może wywołać żądanie do staffhub.thm. Kiedy przeglądarka wysyła żądanie, automatycznie uwzględnia ono plik cookie sesji Z perspektywy serwera żądanie wydaje się pochodzić od uwierzytelnionego użytkownika.![Dlaczego CSRF działa.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775481729380.png)To jest dokładnie to samo zachowanie, które atakujący wykorzystują podczas CSRF atak. Jeśli aplikacja nie zweryfikuje pochodzenia żądania, może je przetworzyć, nie zdając sobie sprawy, że zostało ono wywołane przez złośliwą stronę. 

## Kluczowe warunki dla CSRF Atak

Dla CSRF Aby atak zadziałał, zazwyczaj muszą być spełnione trzy główne warunki:

- Ofiara musi zostać uwierzytelniona w aplikacji docelowej.
- Aplikacja musi wykonać akcję zmieniającą stan, taką jak aktualizacja ustawień lub modyfikacja danych konta.
- Aplikacja nie może weryfikować, czy żądanie pochodzi z zaufanego źródła. 

Jeżeli zaistnieją takie warunki, atakujący może wykonywać działania w imieniu ofiary, nie znając jej danych uwierzytelniających.

W kolejnym zadaniu dowiemy się, jak pentesterzy identyfikują, które funkcje aplikacji mogą być podatne na ataki CSRF ataki.

Przed eksploatacją CSRF Pentester musi najpierw zidentyfikować miejsce występowania luki. Nie każda funkcja w aplikacji internetowej jest dobrym celem ataku. CSRF Ataki zwykle koncentrują się na działaniach polegających na zmianie danych lub modyfikacji ustawień konta.

Za każdym razem, gdy użytkownik wykonuje jakąś czynność na stronie internetowej, przeglądarka wysyła HTTP żądanie do serwera. Niektóre żądania po prostu pobierają informacje, podczas gdy inne modyfikują stan aplikacji. Te żądania zmieniające stan są głównymi celami CSRF ataki. 

Jako pentester powinieneś dokładnie sprawdzić funkcjonalność aplikacji i zadać sobie proste pytanie:

**_Czy tę akcję można uruchomić bez weryfikacji, czy żądanie rzeczywiście pochodzi od użytkownika?_**

Jeśli odpowiedź brzmi „tak”, funkcja może być podatna na atakiCSRF.

## Cechy wspólne podatne na ataki CSRF

Niektóre działania często pojawiają się w CSRF Luki w zabezpieczeniach, ponieważ modyfikują ważne dane użytkownika. Podczas testowania aplikacji należy zwrócić szczególną uwagę na żądania wykonujące operacje takie jak:

![Typowe funkcje narażone na ataki CSRF.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775481944957.png)Jeżeli te żądania nie obejmują żadnego mechanizmu ochrony, takiego jak CSRF tokenów, mogą one być podatne na sfałszowane żądania.

## GET kontra POST – powszechne nieporozumienie

Wielu programistów zakłada, że ​​użycie metody POST automatycznie chroni przed CSRF ataki. To nieprawda.

Zarówno żądania GET, jak i POST mogą być nadużywane, jeśli aplikacja nie zweryfikuje, czy żądanie pochodzi z zaufanej strony. W rzeczywistości wiele CSRF Ataki polegają na prostych żądaniach GET, które można wywołać za pomocą łączy lub obrazów.

Z tego powodu testerzy penetracyjni nigdy nie powinni polegać wyłącznie na metodzie żądania podczas testowania CSRF podatności.

W kolejnych zadaniach przeanalizujemy portal pracowniczy StaffHub i zaobserwujemy, jak aktualizowane są niektóre ustawienia konta. Następnie spróbujesz odtworzyć te żądania ze złośliwej strony internetowej, pokazując, jak atakujący mogą wykorzystać brakujące dane. CSRF zabezpieczenia umożliwiające wykonywanie działań w imieniu uwierzytelnionego użytkownika.

Teraz, gdy rozumiemy, gdzie CSRF Pojawiają się luki, czas zobaczyć, jak atakujący je wykorzystują. W tym zadaniu przeprowadzimy podstawowe CSRF atak polegający na sfałszowaniu złośliwego formularza HTML.

## Praktyczny

W załączniku Maszyna wirtualna Odwiedź aplikację StaffHub pod adresem `http://staffhub.thm:8080`i zaloguj się za pomocą danych logowania `user`i `user`. Użyj podanej nazwy domeny zamiast uzyskiwać dostęp do aplikacji internetowej za pomocą adresu IP. Po zalogowaniu przejdź na stronę ustawień, gdzie znajdziesz opcję zmiany adresu e-mail, jak pokazano poniżej:

![Strona ustawień z opcją „Aktualizuj adres e-mail”.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1772918648421.png)

Portal pracowniczy StaffHub umożliwia użytkownikom aktualizację adresu e-mail na stronie ustawień konta. Gdy użytkownik wysyła formularz, przeglądarka wysyła do serwera żądanie POST zawierające nowy adres e-mail. Aplikacja nie obsługuje jednak ochrony CSRF, co oznacza **,** że ​​serwer nie weryfikuje pochodzenia żądania. Oto kod HTML, który publikuje treść:

```html
<form action="update_email.php" method="POST">
    <div class="input-field">
        <i class="material-icons prefix">alternate_email</i>
        <input id="email" type="email" name="email" required>
        <label for="email">New Email Address</label>
    </div>

    <button class="btn waves-effect waves-light teal btn-rounded" type="submit">
        Update Email
        <i class="material-icons right">save</i>
    </button>
</form>
```

Dzięki temu atakujący może wysłać to samo żądanie z innej strony internetowej i oszukać przeglądarkę ofiary, tak aby automatycznie je wysłała.

Należy pamiętać, że żądanie zawiera jedynie parametr adresu e-mail. Nie ma żadnej dodatkowej wartości, tokenu ani mechanizmu weryfikacji potwierdzającego, że żądanie pochodzi z legalnej witryny. Oznacza to, że każdy, kto zna strukturę tego żądania, może je odtworzyć w innym miejscu.

## Tworzenie złośliwej strony

Atakujący może stworzyć złośliwą stronę internetową zawierającą ukryty formularz, który wysyła to samo żądanie do serwera StaffHub. Formularz może zostać automatycznie wysłany za pomocą JavaScript po otwarciu strony przez ofiarę. Przejdź do zakładki AttackBox i przejdź do niej  `/var/www/html`za pomocą `cd /var/www/html`polecenia, a następnie utwórz nowy plik, używając  `nano settings.html`poniższego kodu:

```javascript
<html>
<body>

<form action="http://staffhub.thm:8080/update_email.php" method="POST" id="attack">
<input type="hidden" name="email" value="attacker@evilmail.thm">
</form>

<script>
document.getElementById("attack").submit();

// redirect user after the request is sent
setTimeout(function() {
    window.location.href = "http://staffhub.thm:8080/settings.php";
}, 1000);
</script>

</body>
</html>
```

Dostęp do tej strony można uzyskać za pomocą linku `http://10.129.89.0:81/settings.html`. Jeśli ofiara, która jest już zalogowana w StaffHub, odwiedzi tę stronę, jej przeglądarka automatycznie wyśle ​​sfałszowane żądanie do serwera wraz z plikiem cookie sesji. Z perspektywy serwera żądanie wydaje się pochodzić od uwierzytelnionego użytkownika.

Atakujący może wysłać adres URL do celu, wykorzystując dowolną technikę inżynierii społecznej, np. nakłonienie celu do kliknięcia łącza na czacie lub w wiadomości e-mail.

Wróć do zakładki docelowej maszyny wirtualnej. Następnie otwórz link `http://10.129.89.0:81/settings.html`w tej samej przeglądarce i na tej samej karcie, na której jesteś zalogowany do aplikacji. Zaktualizuje to Twój adres e-mail, [`attacker@evilmail.thm`](mailto:attacker@evilmail.thm)jak pokazano poniżej:

![oznacz flagą po zaktualizowaniu wiadomości e-mail.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1772922823745.png)

## Co dokładnie się wydarzyło?

Ponieważ aplikacja nie weryfikuje pochodzenia żądania, serwer przetwarza je normalnie i aktualizuje adres e-mail użytkownika zgodnie z wartością atakującego. Ta prosta technika demonstruje sedno idei.CSRFataki: zmuszanie przeglądarki uwierzytelnionego użytkownika do wykonywania działań bez jego wiedzy.

W kolejnym zadaniu zobaczymy, jak słaba implementacja tokenaCSRFmoże spowodować automatyczną zmianę informacji na koncie ofiary.

W poprzednim zadaniu wykorzystaliśmy funkcję, której brakowało CSRF ochrona. W rzeczywistych aplikacjach programiści często próbują się jednak bronić przed CSRF poprzez dodanie tokena do wrażliwych żądań. To dobry krok, ale tylko wtedy, gdy token jest unikalny, nieprzewidywalny i poprawnie zweryfikowany. Jeśli token jest generowany w sposób słaby lub odwracalny, atakujący nadal może być w stanie ominąć to zabezpieczenie.

W tym zadaniu przyjrzymy się podstawowemu przykładowi odwrócenia słabego CSRF ochronę, a następnie wykorzystać tę wiedzę do uruchomienia opartej na obrazie CSRF atak.

## Praktyczny 

W załącznikuMaszyna wirtualnaZaloguj się do aplikacji StaffHub, `http://staffhub.thm:8080`używając danych logowania `user`i `user`. Po zalogowaniu przejdź do strony ustawień, gdzie znajdziesz funkcję aktualizującą rolę aktualnie zalogowanego użytkownika.

![Strona ustawień z opcją „Aktualizuj rolę”.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1773043120537.png)

Ta akcja jest chroniona tokenem CSRF. Na pierwszy rzut oka może się to wydawać bezpieczne. Jeśli jednak obejrzysz kod źródłowy lub sprawdzisz żądanie i wartość tokena, zauważysz, że token nie jest generowany losowo. Zamiast tego jest on generowany na podstawie przewidywalnych danych użytkownika i można go łatwo odwrócić, ponieważ w rzeczywistości jest to zakodowana w formacie base64 wartość roli użytkownika.

![przegląd kodu źródłowego pokazujący token csrf.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1773045097317.png)

 Na przykład aplikacja zawiera ukryte pole CSRF w następujący sposób:

```html
<input type="hidden" name="csrf_token" value="YWRtaW4=">
```

Jeśli zdekodujemy tę wartość, otrzymamy wartość `admin`. Możesz użyć  [CyberChef(otwiera się w nowej karcie)](https://gchq.github.io/CyberChef/#recipe=From_Base64\('A-Za-z0-9%2B/%3D',true,false\)&input=WVdSdGFXND0)lub zdekoduj używając [tego(otwiera się w nowej karcie)](https://emn178.github.io/online-tools/base64_decode.html)strona internetowa.

Oznacza to, że aplikacja korzysta ze słabej, przewidywalnej metody generowania tokenów. Ponieważ atakujący rozumie, w jaki sposób token jest tworzony, może go odtworzyć na własnej, złośliwej stronie.

## Przygotowanie ładunku

W AttackBoxie przejdź do katalogu web za pomocą `cd /var/www/html`, utwórz plik za pomocą `nano role.html`  i dodaj następujący kod:

```html
<html>
<body>

<h2>StaffHub Internal Notice</h2>
<p>Move your mouse over the banner below to load the latest role updates.</p>

<img src="http://staffhub.thm:8080/one.png"
onmouseover="window.location='http://staffhub.thm:8080/update_role.php?role=staff&csrf_token=YWRtaW4='"
width="400">

</body>
</html>
```

Zapisz plik w celu udostępnienia go docelowemu za pomocą `http://10.128.87.8:81/role.html`.

Powyższy kod tworzy prostą stronę internetową wyświetlającą obraz z dołączonym małym modułem obsługi zdarzeń JavaScript. Gdy użytkownik najedzie kursorem myszy na obraz, `onmouseover`zdarzenie to wyzwala przekierowanie do adresu URL StaffHub, który zawiera żądanie aktualizacji roli wraz z tokenem CSRF. W rezultacie przeglądarka ofiary automatycznie wysyła żądanie do aplikacji, używając uwierzytelnionego pliku cookie sesji ofiary, umożliwiając zmianę roli bez wiedzy użytkownika.

## Wysyłanie ładunku

Podobnie jak w poprzednim przypadku, atakujący może użyć dowolnej metody socjotechnicznej, aby wysłać link ofierze (pocztą e-mail lub czatem). Jeśli ofiara jest już zalogowana w StaffHub i odwiedza tę stronę, najechanie kursorem na obrazek spowoduje, że przeglądarka zażąda podania podatnego adresu URL. Ponieważ żądanie zawiera oczekiwany token CSRF, a plik cookie sesji ofiary jest automatycznie dołączany, aplikacja potraktuje je jako legalne.

Wróć do zakładki docelowej maszyny wirtualnej. Następnie otwórz link w tej samej przeglądarce, w której jesteś zalogowany do aplikacji, jak pokazano poniżej:

![Podatna na ataki strona stworzona przez atakującego.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775072457287.png)

W rezultacie po najechaniu kursorem myszy przeglądarka nawiąże połączenie z podatnym na ataki punktem końcowym, podając prawidłowe parametry, takie jak `role`i `csrf-token`, co spowoduje zmianę roli zalogowanego użytkownika z administratora na pracownika. 

![wartość flagi po zdegradowaniu użytkownika z administratora do pracownika.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1773046634047.png)

SłabyCSRF Ochrona może stwarzać fałszywe poczucie bezpieczeństwa. Token musi być unikalny, nieprzewidywalny i bezpiecznie powiązany z sesją użytkownika. Nawet jeśli da się go odgadnąć lub odwrócić, nadal może zostać wykorzystany przez atakującego. W kolejnym zadaniu przeanalizujemy odpowiednie środki obronne, które powinni stosować programiści, aby zapobiec…CSRF atakuje skutecznie.

Po nauczeniu się jak CSRF Luki w zabezpieczeniach mogą zostać wykorzystane, dlatego ważne jest, aby pentesterzy wiedzieli, jak skutecznie je identyfikować podczas oceny. Poniższe praktyki pomogą Ci szybko zidentyfikować potencjalne zagrożenia. CSRF słabości w testowaniu aplikacji internetowych.

## Kluczowe praktyki

![Najlepsze praktyki testowania CSRF.](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/62a7685ca6e7ce005d3f3afe-1775481780978.png)

1. Skoncentruj się na **żądaniach zmieniających stan** : Priorytetowo traktuj żądania modyfikujące dane, takie jak zmiana hasła, aktualizacja poczty e-mail, ustawienia konta czy transakcje finansowe. Te punkty końcowe są najczęstszymi celami ataków. CSRF ataki.
2. **Sprawdź prośby o CSRF tokeny** : Sprawdź, czy wrażliwe działania obejmują CSRF token. Jeśli token nie istnieje lub jeśli token wydaje się statyczny lub przewidywalny, żądanie może być podatne na ataki. 
3. **Analizować HTTP Metody** : Akcje wrażliwe powinny zazwyczaj korzystać z żądań POST. Jeśli ważne operacje są wykonywane za pomocą żądań GET, łatwiej jest je wykorzystać, używając obrazów lub prostych linków. 
4. **Przetestuj żądania poza aplikacją** : Skopiuj żądanie i spróbuj odtworzyć je z zewnętrznej strony HTML. Jeśli działanie zakończy się powodzeniem bez dodatkowej weryfikacji, punkt końcowy prawdopodobnie jest podatny na ataki. CSRF. 
5. **Obserwuj zachowanie plików cookie** : Sprawdź, czy uwierzytelnianie opiera się wyłącznie na plikach cookie sesji. Jeśli aplikacja automatycznie akceptuje żądania zawierające plik cookie sesji bez sprawdzania pochodzenia żądania, CSRF ataki stają się możliwe.

W tym pokoju zgłębialiśmy koncepcję CSRFi jak atakujący mogą wykorzystać uwierzytelnioną sesję ofiary do wykonania niezamierzonych działań. Podczas ćwiczeń praktycznych zaobserwowaliśmy, że proste czynności, takie jak przesłanie ukrytego formularza lub interakcja z elementem strony internetowej, mogą wywołać złośliwe żądania.

Widzieliśmy również, że nawet aplikacje, które wdrażająCSRFOchrona może pozostać podatna na ataki, jeśli mechanizm ochrony jest słaby lub przewidywalny. Odwracając źle zaprojektowany token, odtworzyłeś prawidłowe żądanie i skutecznie ominąłeś obronę. Na koniec omówiliśmy ważne praktyki, których powinni przestrzegać pentesterzy podczas identyfikacji…CSRFluk w zabezpieczeniach podczas ocen. 

Zrozumienie, jak działają te ataki i jak można je wykryć, jest kluczowe zarówno dla testerów zabezpieczeń, jak i programistów tworzących bezpieczniejsze aplikacje.
