---

Chodźmy na przygodę!

Zanim przejdziemy do samego hakowania, warto się rozejrzeć. W Burp wyłącz tryb przechwytywania i przejrzyj witrynę. Dzięki temu Burp będzie mógł rejestrować różne żądania z serwera, które mogą okazać się przydatne później. 

Nazywa się to **„spacerowaniem po** aplikacji”, co jest również formą **rozpoznania** !

Odpowiedz na poniższe pytania

Pytanie nr 1: Jaki jest adres e-mail administratora?

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/654be36872552158be01f92f/room-content/654be36872552158be01f92f-1750841888292.png)

Recenzje zawierają adresy e-mail poszczególnych użytkowników. Kliknięcie na produkt Apple Juice wyświetla nam adres e-mail administratora!

![](https://assets.tryhackme.com/additional/imgur/YFWDP5v.png)

Poprawna odpowiedź

**Pytanie nr 2: Jaki parametr jest używany do wyszukiwania?** 

![](https://assets.tryhackme.com/additional/imgur/pZLtWQl.png)

Kliknij lupę w prawym górnym rogu aplikacji, aby wyświetlić pasek wyszukiwania.

![](https://assets.tryhackme.com/additional/imgur/bFgw6uS.png)

Następnie możemy wpisać tekst i naciskając **Enter** wyszukać wpisany tekst.

Teraz zwróć uwagę na adres URL, który zostanie zaktualizowany o wprowadzony przez nas tekst.

![](https://assets.tryhackme.com/additional/imgur/AzJ3FAM.png)

Teraz możemy zobaczyć parametr wyszukiwania po **/#/search?** literze **q**

Poprawna odpowiedź

Pytanie nr 3: Do jakiego programu Jim nawiązuje w swojej recenzji? 

Jim napisał recenzję produktu Green Smoothie. Widzimy, że wspomina o replikatorze. 

![](https://assets.tryhackme.com/additional/imgur/RCFw2tB.png)

Jeśli wpiszemy w wyszukiwarkę Google „ **replikator** ”, otrzymamy wyniki wskazujące, że pochodzi on z serialu telewizyjnego „Star Trek”

![](https://assets.tryhackme.com/additional/imgur/Sp8ymGR.png)

Wstrzyknąć sok

![](https://assets.tryhackme.com/additional/imgur/uwXqDdH.png)  

To zadanie będzie koncentrować się na lukach w zabezpieczeniach związanych z wstrzykiwaniem. Luki te są dość niebezpieczne dla firmy, ponieważ mogą potencjalnie spowodować przestoje i/lub utratę danych. Identyfikacja punktów wstrzykiwania w aplikacji internetowej jest zazwyczaj dość prosta, ponieważ większość z nich zwróci błąd. Istnieje wiele rodzajów ataków wstrzykiwania, a niektóre z nich to:

|   |   |
|---|---|
|Wstrzyknięcie SQL|Wstrzyknięcie kodu SQL (SQL Injection) to sytuacja, gdy atakujący wprowadza złośliwe lub niepoprawnie sformatowane zapytanie w celu pobrania lub sfałszowania danych z bazy danych. W niektórych przypadkach może również zalogować się na konta.|
|Wstrzykiwanie poleceń|Wstrzykiwanie poleceń (Command Injection) polega na tym, że aplikacje internetowe pobierają dane wejściowe lub kontrolowane przez użytkownika i uruchamiają je jako polecenia systemowe. Atakujący może manipulować tymi danymi, aby wykonywać własne polecenia systemowe. Zjawisko to można zaobserwować w aplikacjach, które wykonują błędnie skonfigurowane testy ping.|
|Wstrzykiwanie wiadomości e-mail|Wstrzyknięcie e-maila to luka w zabezpieczeniach, która umożliwia złośliwym użytkownikom wysyłanie wiadomości e-mail bez uprzedniej autoryzacji serwera pocztowego. Dzieje się tak, gdy atakujący dodaje dodatkowe dane do pól, które nie są poprawnie interpretowane przez serwer.|

W naszym przypadku wykorzystamy atak **SQL Injection** .

Więcej informacji:  [Wstrzyknięcie](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A1-Injection)

Odpowiedz na poniższe pytania

Pytanie nr 1: Zaloguj się na konto administratora!

Po przejściu na stronę logowania wprowadź dane w polach adres e-mail i hasło.

![](https://assets.tryhackme.com/additional/imgur/4XHHSof.png)

 Przed  kliknięciem przycisku „Wyślij” upewnij się, że  tryb przechwytywania jest  włączony .

Dzięki temu będziemy mogli zobaczyć, jakie dane zostały wysłane na serwer!

![](https://assets.tryhackme.com/additional/imgur/6gyZ7Vr.png)  

Teraz zmienimy „ **a** ” obok wiadomości e-mail na:  ' lub 1=1--  i przekażemy ją do serwera.

![](https://assets.tryhackme.com/additional/imgur/tPFJnmC.png)

**Dlaczego to działa?**

1. Znak **'** zamknie nawiasy w zapytaniu SQL
2. Operator „ **OR** ” w instrukcji SQL zwróci wartość true, jeśli którakolwiek ze stron jest prawdziwa. Ponieważ  1=1 zawsze jest prawdą , całe polecenie jest prawdą. W ten sposób serwer otrzyma informację o poprawności adresu e-mail i zaloguje nas na  konto użytkownika o identyfikatorze 0 , które jest jednocześnie kontem administratora.
3. Znak  „-”  jest używany w SQL do komentowania danych. Wszelkie ograniczenia dotyczące logowania nie będą już działać, ponieważ są interpretowane jako komentarz. Jest to  odpowiednik komentarzy „#”  i  „//”  w Pythonie i JavaScript.

                      ![](https://assets.tryhackme.com/additional/imgur/Y7xYGjp.png)

Sprawdzać

Pytanie nr 2: Zaloguj się na konto Bender!  

Podobnie jak w  pytaniu nr 1 , zalogujemy się teraz na konto Bendera! Ponownie przechwyć prośbę o logowanie, ale tym razem jako adres e-mail wpisz:  bender@juice-sh.op'--  . 

![](https://assets.tryhackme.com/additional/imgur/1F1ufc3.png)

Teraz przekaż to na serwer!

Ale dlaczego nie zapiszemy  1=1 ?

Ponieważ adres e-mail jest prawidłowy (co zwróci  wartość true ), nie musimy wymuszać, aby był  prawdziwy . Dzięki temu możemy użyć  **'--** , aby ominąć system logowania. Należy pamiętać, że **1=1** można użyć, gdy adres e-mail lub nazwa użytkownika są nieznane lub nieprawidłowe.

                     ![](https://assets.tryhackme.com/additional/imgur/Rznz31B.png)
