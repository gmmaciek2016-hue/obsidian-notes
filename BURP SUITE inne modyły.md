---

Moduł dekodera pakietu Burp Suite umożliwia użytkownikowi manipulowanie danymi. Jak sama nazwa wskazuje, nie tylko dekoduje on dane przechwycone podczas ataku, ale także udostępnia funkcję kodowania własnych danych, przygotowując je do transmisji do celu. Dekoder umożliwia również tworzenie haszów danych, a także udostępnia funkcję inteligentnego dekodowania, która próbuje dekodować dostarczone dane rekurencyjnie, aż do momentu, gdy powrócą do postaci tekstu jawnego (podobnie jak funkcja „Magic” w [programie Cyberchef](https://gchq.github.io/CyberChef/) ).

Aby uzyskać dostęp do Dekodera, przejdź do zakładki Dekoder w menu górnym i zobacz dostępne opcje:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/2258ccd03e0732c2d0bd4729a3f6212f.png)

Ten interfejs udostępnia wiele opcji.

1. To pole służy jako obszar roboczy do wprowadzania lub wklejania danych wymagających kodowania lub dekodowania. Podobnie jak w innych modułach pakietu Burp Suite , dane można przenieść do tego obszaru z różnych części struktury za pomocą opcji „ **Wyślij do dekodera”** po kliknięciu prawym przyciskiem myszy.
2. Na górze listy po prawej stronie znajduje się opcja pozwalająca traktować dane wejściowe jako tekst lub szesnastkowe wartości bajtowe.
3. W miarę przesuwania się w dół listy pojawiają się menu rozwijane umożliwiające kodowanie, dekodowanie lub haszowanie danych wejściowych.
4. Funkcja **Smart Decode**  , znajdująca się na końcu, próbuje automatycznie zdekodować dane wejściowe.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/f795b0f0701d019d37025310fa4ae285.png)

Po wprowadzeniu danych do pola wejściowego interfejs replikuje się, aby wyświetlić wynik naszej operacji. Możemy następnie zastosować dalsze transformacje, korzystając z tych samych opcji:

#### Kodowanie i dekodowanie za pomocą dekodera

Przyjrzyjmy się teraz szczegółowo opcjom ręcznego kodowania i dekodowania. Są one identyczne niezależnie od tego, czy wybrano menu dekodowania, czy kodowania:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/8ce7c550edf3a79cafbb7be8468793ff.png)

- **Zwykły** : Odnosi się to do surowego tekstu przed zastosowaniem jakichkolwiek przekształceń.
    
- **URL** : Kodowanie URL służy do zapewnienia bezpiecznego przesyłania danych w adresie URL żądania sieciowego. Polega ono na zastępowaniu znaków ich kodem ASCII w formacie szesnastkowym, poprzedzonym symbolem procenta (%). Ta metoda jest niezbędna do testowania każdego typu aplikacji internetowych.
    
    Na przykład, zakodowanie znaku ukośnika ( **/** ), którego kod ASCII to 47, konwertuje go na **2F** w systemie szesnastkowym, stając się tym samym **%2F** w kodowaniu URL. Można to sprawdzić za pomocą dekodera, wpisując ukośnik w polu wprowadzania, a następnie wybierając `Encode as -> URL`:
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/72ecaaf06fc248457d61c079d6d98e8f.png)
    
- **HTML** : Kodowanie encji HTML zastępuje znaki specjalne znakiem ampersand (&), po którym następuje liczba szesnastkowa lub odwołanie do znaku, który ma zostać zastąpiony znakiem ucieczki, a całość kończy się średnikiem (;). Ta metoda zapewnia bezpieczne renderowanie znaków specjalnych w HTML i pomaga zapobiegać atakom takim jak XSS. Opcja HTML w Dekoderze umożliwia zakodowanie dowolnego znaku do jego formatu ucieczki HTML lub dekodowanie przechwyconych encji HTML. Na przykład, aby zdekodować wcześniej omówiony cudzysłów, wprowadź zakodowaną wersję i wybierz `Decode as -> HTML`:
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/99ccb4aba6cb243b7c3b990e82061a86.png)
    
- **Base64 : Base64, powszechnie stosowana metoda kodowania, konwertuje dowolne dane do formatu zgodnego z ASCII. Na tym etapie nie jest to kluczowe, jednak osoby zainteresowane mogą znaleźć** [tutaj](https://stackabuse.com/encoding-and-decoding-base64-strings-in-python) podstawowe informacje matematyczne .
    
- **ASCII Hex** : Ta opcja umożliwia konwersję danych między reprezentacją ASCII a szesnastkową. Na przykład słowo „ASCII” można przekonwertować na liczbę szesnastkową „4153434949”. Każdy znak jest konwertowany z jego numerycznej reprezentacji ASCII na szesnastkową.
    
- **System szesnastkowy, ósemkowy i binarny** : Te metody kodowania mają zastosowanie wyłącznie do danych numerycznych i umożliwiają konwersję między reprezentacją dziesiętną, szesnastkową, ósemkową (o podstawie osiem) i binarną.
    
- **Gzip** : Gzip kompresuje dane, zmniejszając rozmiar plików i stron przed transmisją przez przeglądarkę. Krótsze czasy ładowania są niezwykle pożądane przez programistów, którzy chcą poprawić swój wynik SEO i uniknąć niedogodności dla użytkowników. Dekoder ułatwia ręczne kodowanie i dekodowanie danych gzip, chociaż często nie są one zgodne ze standardem ASCII/Unicode. Na przykład:
    
    ![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/01db98e37c59a26e307eb29cd9e04139.png)

Metody te można łączyć. Na przykład frazę („Burp Suite Decoder”) można przekonwertować na zapis szesnastkowy ASCII, a następnie na ósemkowy:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/4a1065502dd1020858694994767b4156.gif)

Łącznie metody te dają nam znaczącą kontrolę nad danymi, które kodujemy lub dekodujemy.

Każda metoda kodowania/dekodowania jest oznaczona kolorem, co pozwala na szybką identyfikację zastosowanej transformacji.

##### Format szesnastkowy

Chociaż wprowadzanie danych w formacie ASCII jest korzystne, zdarzają się sytuacje, gdy konieczna jest edycja danych bajt po bajcie. W takich sytuacjach przydatny okazuje się „Widok szesnastkowy”, dostępny nad opcjami dekodowania:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/704444afc761deabd6a8a3492dffd89b.png)

Funkcja ta umożliwia przeglądanie i modyfikowanie danych w szesnastkowym formacie bajtów, co jest niezwykle przydatne podczas pracy z plikami binarnymi lub innymi danymi w formacie innym niż ASCII.

##### Inteligentne dekodowanie

Na koniec mamy opcję **Inteligentnego dekodowania** . Ta funkcja próbuje automatycznie dekodować zakodowany tekst. Na przykład, tekst `&#x42;&#x75;&#x72;&#x70;&#x20;&#x53;&#x75;&#x69;&#x74;&#x65;` jest automatycznie rozpoznawany jako zakodowany w formacie HTML i odpowiednio dekodowany:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5d9e176315f8850e719252ed/room-content/e6330851dfa9ea47e3d2d54ab78b0023.gif)

Choć funkcja ta nie jest idealna, może okazać się szybkim rozwiązaniem umożliwiającym dekodowanie nieznanych fragmentów danych.

`Hash`Oprócz funkcjonalności kodowania/dekodowania Decoder oferuje również możliwość generowania sum skrótów dla naszych danych.

#### Teoria

Haszowanie to proces jednokierunkowy, który przekształca dane w unikalny podpis. Aby funkcja kwalifikowała się jako algorytm haszujący, generowane przez nią dane wyjściowe muszą być nieodwracalne. Sprawny algorytm haszujący gwarantuje, że każde dane wejściowe wygenerują całkowicie unikalny hasz. Na przykład, użycie algorytmu MD5 do wygenerowania sumy haszującej dla tekstu „MD5sum” zwraca `4ae1a02de5bd02a5515f583f4fca5e8c`. Użycie tego samego algorytmu dla „MD5SUM” daje zupełnie inny hasz, pomimo bliskiego podobieństwa danych wejściowych: `13b436b09172400c9eb2f69fbd20adad`. Dlatego hasze są powszechnie używane do weryfikacji integralności plików i dokumentów, ponieważ nawet niewielka zmiana w pliku znacząco zmienia sumę haszującą.

**Uwaga:** algorytm MD5 jest przestarzały i nie należy go używać w nowoczesnych aplikacjach.

Co więcej, skróty służą do bezpiecznego przechowywania haseł, ponieważ jednokierunkowy proces haszowania sprawia, że ​​hasła są stosunkowo bezpieczne, nawet w przypadku naruszenia bezpieczeństwa bazy danych. Gdy użytkownik tworzy hasło, aplikacja je haszuje i zapisuje. Podczas logowania aplikacja haszuje przesłane hasło i porównuje je z zapisanym skrótem; jeśli są one zgodne, hasło jest poprawne. Dzięki tej metodzie aplikacja nigdy nie musi przechowywać oryginalnego hasła (w postaci jawnego tekstu).

#### Haszowanie w dekoderze

Dekoder pozwala nam tworzyć sumy skrótów dla danych bezpośrednio w Burp Suite; działa podobnie do opcji kodowania/dekodowania, które omówiliśmy wcześniej. Dokładniej, klikamy menu rozwijane **„Skrót”** i wybieramy algorytm z listy:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/c212c8a83418b3674928270f258ddd72.png)

**Uwaga:** Ta lista jest znacznie dłuższa niż lista algorytmów kodowania/dekodowania – warto ją przejrzeć, aby zobaczyć liczne dostępne algorytmy haszujące.

Kontynuując nasz wcześniejszy przykład, wpiszmy „MD5sum” w polu wprowadzania, a następnie przewińmy listę w dół, aż znajdziemy „ MD5 ”. Zastosowanie tej opcji automatycznie przeniesie nas do widoku szesnastkowego:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/01a73d9cb47f274259543585f91a3664.png)

Wynik algorytmu haszującego nie daje czystego tekstu w formacie ASCII/Unicode. Dlatego zazwyczaj konwertuje się go na ciąg szesnastkowy; jest to forma „haszu”, z którą być może jesteś zaznajomiony.

Uzupełnijmy to, stosując kodowanie „ASCII Hex” do sumy skrótu, aby utworzyć uporządkowany ciąg szesnastkowy z naszego początkowego przykładu.

Oto cały proces:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/8bb114a4bce68b068f6dd0c0aaffe9e1.gif)

Odpowiedz na poniższe pytania

4.3 Przyjrzyjmy się przykładowi w kontekście:

Najpierw pobierz plik załączony do tego zadania.

**Uwaga:** Ten plik można również pobrać z wdrożonej maszyny wirtualnej za pomocą — może się to okazać pomocne, jeśli używasz AttackBox.`**wget** **http://MACHINE_IP:9999/AlteredKeys.zip**`

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*oZWqXpy6UCwu13iVbWWTIg.png)

Teraz przeczytaj specyfikację problemu poniżej:

„Jakiś żartowniś majstrował przy moim kluczu SSH! W katalogu są cztery klucze i nie mam pojęcia, który jest prawdziwy. Suma haszująca MD5 mojego klucza to `**3166226048d6ad776370dc105d40d9f8**`— czy mógłbyś ją dla mnie znaleźć?” (Skopiuj i wklej każdy z kluczy do Dekodera, a następnie haszuj je po kolei algorytmem MD5. Szukasz klucza, którego suma haszująca MD5 jest równa tej w pytaniu. Upewnij się, że nie usuniesz ostatniego znaku nowej linii z końca kluczy!)

## Otrzymuj historie IritT w swojej skrzynce odbiorczej

Dołącz do Medium za darmo, aby otrzymywać aktualności od tego autora.

Subskrybować

Przejdź do katalogu kluczy i wyświetl jego zawartość

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*i6QX12NSdmu9A-MXRzJkDg.png)

keys   
CD ls   
ls

Wyświetlanie zawartości pliku klucza prywatnego

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*QV1iA4H0JUC5EP2JMhyN6g.png)

klucz kota 1

Skopiuj zawartość i wklej ją do środka

-----BEGIN OPENSSH PRYWATNY KEY-----   
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   
-----END OPENSSH PRIVATE KEY----

Zrób to samo ze wszystkimi kluczami

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Be362R34qwuNY4BXxAxE5A.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*OpzSnUA_W3yyWJRQCrFBew.png)

-----BEGIN OPENSSH PRYWATNY KEY-----   
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   
-----END OPENSSH PRIVATE KEY-----

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*MwHY8Ktq_1G6DeH-Dt8txA.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*W0-gBNb7NtoElj1eFEYxsA.png)

-----BEGIN OPENSSH PRYWATNY KEY-----   
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   
-----END OPENSSH PRIVATE KEY-----

![](https://miro.medium.com/v2/1*ihtx3th7x1bomR0knmqVPQ.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*JRbIUVw2xJvnuFLsNk-lfg.png)

-----BEGIN OPENSSH PRYWATNY KEY-----   
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   
-----END OPENSSH PRIVATE KEY-----

4.3 Jaka jest prawidłowa nazwa klucza?

![](https://miro.medium.com/v2/resize:fit:530/1*GrESlftH5U_z4f2uuB-RRw.png)

Odpowiedź: **klucz 3**

## Zadanie 5 Porównywacz: Przegląd

Comparer, jak sama nazwa wskazuje, umożliwia porównywanie dwóch zestawów danych, albo według słów ASCII, albo według bajtów.

Najpierw sprawdźmy interfejs:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*9FAAbelKCv1dm-pD.png)

Interfejs można podzielić na trzy główne sekcje:

1. Po lewej stronie widzimy elementy do porównania. Po załadowaniu danych do narzędzia Comparer, pojawią się one jako wiersze w tych tabelach. Wybieramy dwa zestawy danych do porównania.
2. W prawym górnym rogu znajdują się opcje wklejania danych ze schowka (Wklej), ładowania danych z pliku (Załaduj), usuwania bieżącego wiersza (Usuń) i czyszczenia wszystkich zestawów danych (Wyczyść).
3. Na koniec, w prawym dolnym rogu, możemy wybrać porównanie naszych zestawów danych według słów lub bajtów. Nie ma znaczenia, który z tych przycisków wybierzesz początkowo, ponieważ można to później zmienić. To właśnie te przyciski klikamy, gdy jesteśmy gotowi porównać wybrane dane.

Podobnie jak w przypadku większości modułów Burp Suite, możemy również ładować dane do Comparera z innych modułów, klikając prawym przyciskiem myszy i wybierając polecenie **Wyślij do Comparera** .

Po dodaniu co najmniej 2 zestawów danych do porównania i kliknięciu opcji **Słowa** lub **Bajty** , pojawi się okno dialogowe, które pokaże nam porównanie:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*MyHKVpjZvymF2ptM.png)

To okno również składa się z trzech odrębnych sekcji:

1. Porównywane dane zajmują większą część okna; można je wyświetlać w formacie tekstowym lub szesnastkowym. Format początkowy zależy od tego, czy w poprzednim oknie wybraliśmy porównywanie według słów, czy bajtów, ale można to zmienić, używając przycisków nad polami porównania.
2. Klucz porównania znajduje się w lewym dolnym rogu i pokazuje, które kolory reprezentują zmodyfikowane, usunięte i dodane dane w obu zestawach danych.
3. Pole wyboru „ Synchronizuj **widoki”** znajduje się w prawym dolnym rogu okna. Po zaznaczeniu zapewnia synchronizację formatów obu zestawów danych. Innymi słowy, jeśli zmienisz jeden z nich na widok szesnastkowy, drugi dostosuje się do niego.

W tytule okna wyświetlana jest całkowita liczba znalezionych różnic.

Odpowiedz na poniższe pytania

Kliknij mnie, aby przejść do następnego zadania.

## Zadanie 6 Porównujący: przykład

Wiemy już, co robi Comparer, ale do czego może się przydać?

Istnieje wiele sytuacji, w których możliwość szybkiego porównania dwóch (potencjalnie bardzo dużych) zbiorów danych może okazać się przydatna.

Na przykład, przeprowadzając atak siłowy na logowanie lub atak polegający na wykorzystaniu danych uwierzytelniających za pomocą narzędzia Intruder, możesz porównać dwie odpowiedzi o różnej długości, aby sprawdzić, gdzie leżą różnice i czy różnice te wskazują na udane logowanie.

### Przykład praktyczny

1. Przejdź do`[**http://MACHINE_IP/support/login**](http://machine_ip/support/login)`
2. Spróbuj zalogować się przy użyciu nieprawidłowej nazwy użytkownika i hasła — przechwyć żądanie w serwerze [proxy Burp](https://tryhackme.com/room/burpsuitebasics) .

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*sWxlCOt2g7ImTQA_6bNbSw.png)

1. Wyślij żądanie do [Repeatera](https://tryhackme.com/room/burpsuiterepeater) za pomocą `Ctrl + R`(lub odpowiednika na komputerze Mac) lub klikając prawym przyciskiem myszy na żądaniu w module Proxy i wybierając opcję **Wyślij do Repeatera** .

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*IhQ_8CBXxgRubVrZBBNPgA.png)

3. Wyślij żądanie, a następnie kliknij prawym przyciskiem myszy odpowiedź i wybierz opcję **Wyślij do programu porównującego** .

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*tR9l0UDuEncQqwzEnr_ckw.png)

1. Na karcie Repeater zmień dane uwierzytelniające na:

- Nazwa użytkownika:`**support_admin**`
- Hasło:`**w58ySK4W**`

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*J-sbtUEHyh1JBSNu5zBJ2g.png)

Wyślij żądanie ponownie, a następnie przekaż nową odpowiedź do Comparera.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Xgr6zZFxYpjIIE1jB_r_TA.png)

Odpowiedz na poniższe pytania

6.1 Porównaj obie odpowiedzi, używając słów. Czy potrafisz wskazać główne różnice?

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*4cByWB6sCfwEuC-nBERkZQ.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*gcuhOznYV6-6MCkVPfkdFg.png)

Odpowiedź: Nie potrzeba odpowiedzi

## Zadanie 7 Sekwencer: Przegląd

Sekwencer pozwala nam ocenić entropię, czyli losowość, „tokenów”. Tokeny to ciągi znaków służące do identyfikacji czegoś i idealnie powinny być generowane w sposób kryptograficznie bezpieczny. Tokeny te mogą być plikami cookie sesji lub tokenami **CSRF (** **Cross** - **Site** Request **Forgery** ) używanymi do ochrony przesyłanych formularzy. Jeśli te tokeny nie są generowane bezpiecznie, teoretycznie moglibyśmy przewidzieć nadchodzące wartości tokenów. Konsekwencje mogłyby być znaczące, na przykład, gdyby dany token był używany do resetowania haseł.

Zacznijmy od przyjrzenia się interfejsowi sekwencera:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*1JO8-naVCgQIKh2M.png)

Analizę tokenów za pomocą Sequencera można przeprowadzić na dwa główne sposoby:

- **Przechwytywanie na żywo** : Jest to bardziej powszechna metoda i domyślna podzakładka Sequencera. Przechwytywanie na żywo pozwala nam przekazać żądanie, które wygeneruje token do Sequencera w celu analizy. Na przykład, możemy chcieć przekazać żądanie POST do punktu końcowego logowania do Sequencera, wiedząc, że serwer odpowie plikiem cookie. Po przekazaniu żądania możemy poinstruować Sequencera, aby rozpoczął przechwytywanie na żywo. Następnie automatycznie wyśle ​​to samo żądanie tysiące razy, zapisując wygenerowane próbki tokenów do analizy. Po zebraniu wystarczającej liczby próbek zatrzymujemy Sequencer i pozwalamy mu przeanalizować przechwycone tokeny.
- **Ładowanie ręczne** : Pozwala nam to załadować listę wstępnie wygenerowanych próbek tokenów bezpośrednio do sekwencera w celu analizy. Korzystanie z ładowania ręcznego oznacza, że ​​nie musimy wysyłać tysięcy żądań do naszego celu, co może być uciążliwe i wymagać dużych zasobów. Wymaga to jednak posiadania obszernej listy wstępnie wygenerowanych tokenów.

W tym pomieszczeniu skupimy się na transmisjach na żywo.

Odpowiedz na poniższe pytania

7.1 Co możemy ocenić dzięki Sequencerowi?

Odpowiedź: **entropia**

## Zadanie 8 Sekwencer: Przechwytywanie na żywo

Świetnie, przyjrzyjmy się teraz procesowi wykorzystania funkcji przechwytywania na żywo sekwencera do analizy entropii tokena zabezpieczającego przed atakami siłowymi, używanego w formularzu logowania administratora.

Najpierw przechwyć żądanie do `**http://MACHINE_IP/admin/login/**`serwera proxy. Kliknij prawym przyciskiem myszy żądanie i wybierz opcję **„Wyślij do sekwencera”** .

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*-I-cMRyWbAgJ-aEkiEiuuw.png)

W sekcji „Lokalizacja tokena w odpowiedzi” możemy wybrać pomiędzy **Cookie** , **Pole formularza** i **Lokalizacja niestandardowa** . Ponieważ w tym przypadku testujemy loginToken, zaznacz opcję „Pole formularza” i wybierz loginToken z menu rozwijanego:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*KjFIj5TCQMMa9BYf-x6IWQ.png)

W tej sytuacji możemy bezpiecznie pozostawić wszystkie pozostałe opcje bez zmian. Kliknij przycisk „ **Rozpocznij przechwytywanie na żywo”** .

Pojawi się nowe okno z informacją o trwającym przechwytywaniu na żywo i liczbą przechwyconych tokenów. Poczekaj, aż zostanie przechwycona wystarczająca liczba tokenów (około 10 000 powinno wystarczyć); im więcej tokenów zdobędziemy, tym dokładniejsza będzie nasza analiza.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*TCS08S0sfgoUvs3D9HR47g.png)

Po przechwyceniu około 10 000 tokenów kliknij przycisk **Wstrzymaj** , a następnie wybierz przycisk **Analizuj teraz** :

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*ZL8_hVsZtWJew15w.png)

Warto zauważyć, że mogliśmy również zatrzymać **przechwytywanie** . Jednak wybierając opcję wstrzymania, zachowujemy możliwość późniejszego wznowienia przechwytywania, jeśli raport nie zawiera wystarczającej liczby próbek, aby dokładnie obliczyć entropię tokena.

Gdybyśmy chcieli okresowych aktualizacji analizy, moglibyśmy również zaznaczyć pole wyboru „Automatyczna analiza”. Ta opcja nakazuje programowi Burp przeprowadzanie analizy entropii po każdych 2000 żądaniach, zapewniając częste aktualizacje, które będą coraz dokładniejsze w miarę ładowania kolejnych próbek do sekwencera.

Warto w tym momencie zaznaczyć, że możemy zdecydować się na skopiowanie lub zapisanie przechwyconych tokenów w celu przeprowadzenia dalszej analizy w późniejszym czasie.

Po kliknięciu przycisku **Analizuj teraz** Burp przeanalizuje entropię tokena i wygeneruje raport.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*oLkyW1-gWjf8oYxD_w1M1w.png)

Odpowiedz na poniższe pytania

8.1 Jaka jest ogólna jakość losowości?

Odpowiedź: **doskonała**

## Zadanie 9 Sekwencer: Analiza

Teraz, gdy mamy raport z analizy entropii naszego tokena, czas na jego analizę!

Wygenerowany raport analizy entropii jest podzielony na cztery główne sekcje. Pierwsza z nich to **Podsumowanie** wyników. Podsumowanie zawiera następujące informacje:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*gVoJSP7gR4s0xV5R.png)

- **Wynik ogólny** : Daje to ogólną ocenę bezpieczeństwa mechanizmu generowania tokenów. W tym przypadku poziom entropii wskazuje, że tokeny są prawdopodobnie generowane bezpiecznie.
- **Efektywna entropia** : Mierzy losowość tokenów. Efektywna entropia 117 bitów jest stosunkowo wysoka, co wskazuje, że tokeny są wystarczająco losowe, a zatem odporne na ataki predykcyjne i siłowe.
- **Niezawodność** : Poziom istotności 1% oznacza 99% pewności co do dokładności wyników. Ten poziom pewności jest dość wysoki i zapewnia pewność co do dokładności oszacowania efektywnej entropii.
- **Próbka** : Zawiera szczegółowe informacje na temat próbek tokenów analizowanych podczas procesu testowania entropii, w tym liczbę tokenów i ich charakterystykę.

Chociaż raport podsumowujący często dostarcza wystarczających informacji do oceny bezpieczeństwa procesu generowania tokenów, należy pamiętać, że w niektórych przypadkach konieczne może być przeprowadzenie dalszych badań. Analiza na poziomie znaków i bitów może zapewnić bardziej szczegółowy wgląd w losowość tokenów, zwłaszcza gdy wyniki podsumowujące budzą potencjalne obawy.

Chociaż raport entropii może stanowić silny wskaźnik bezpieczeństwa mechanizmu generowania tokenów, potrzebne są bardziej jednoznaczne dowody. Na bezpieczeństwo tokenów mogą wpływać również inne czynniki, a natura prawdopodobieństwa i statystyki oznacza, że ​​zawsze istnieje pewien stopień niepewności. Niemniej jednak, efektywna entropia wynosząca 117 bitów przy poziomie istotności 1% sugeruje solidnie bezpieczny proces generowania tokenów.

Odpowiedz na poniższe pytania

Kliknij mnie, aby przejść do następnego zadania.

## Zadanie 10 Organizator: Przegląd

Moduł „Organizator” pakietu Burp Suite został zaprojektowany, aby pomóc Ci przechowywać i opisywać kopie żądań HTTP, do których możesz chcieć wrócić później. To narzędzie może być szczególnie przydatne w organizacji procesu testów penetracyjnych. Oto niektóre z jego kluczowych funkcji:

- Możesz zapisać prośby, które chcesz później zbadać, zapisać prośby, które już zidentyfikowałeś jako interesujące lub zapisać prośby, które chcesz później dodać do raportu.
- Możesz wysyłać żądania HTTP do Burp Organizer z innych modułów Burp, takich jak **Proxy** lub **Repeater** . Możesz to zrobić, klikając prawym przyciskiem myszy żądanie i wybierając **„Wyślij do Organizera”** lub używając domyślnego skrótu klawiszowego `**Ctrl + O**`. Każde żądanie HTTP wysyłane do Organizera jest kopią tylko do odczytu oryginalnego żądania zapisaną w momencie jego wysłania do Organizera.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*Vx9xUxZDbKhuSsUZ.png)

- Żądania są przechowywane w tabeli, która zawiera kolumny, takie jak numer indeksu żądania, czas utworzenia żądania, status przepływu pracy, narzędzie Burp, z którego wysłano żądanie, metoda HTTP, nazwa hosta serwera, ścieżka dostępu do pliku URL, ciąg zapytania URL, liczba parametrów w żądaniu, kod statusu HTTP odpowiedzi, długość odpowiedzi w bajtach i wszelkie notatki.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*tgN0MRyL3J_C8wVp.png)

Aby wyświetlić żądanie i odpowiedź:

1. Kliknij dowolny element Organizatora.
2. Zarówno żądanie, jak i odpowiedź są tylko do odczytu. Możesz przeszukać żądanie lub odpowiedź, wybrać żądanie, a następnie skorzystać z paska wyszukiwania pod żądaniem.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/0*a9DXy_fA-ZX9zu4i.png)

Odpowiedz na poniższe pytania

10.1 Czy zapisane żądania są tylko do odczytu? (tak/nie)

Odpowiedź: **tak**

## Zadanie 11 Wnioski

Gratulacje z okazji ukończenia sali Burp Suite Other Modules!

Podsumowując, Decoder umożliwia kodowanie i dekodowanie danych, ułatwiając odczyt i zrozumienie przesyłanych informacji. Comparer pozwala na wykrycie różnic między dwoma zbiorami danych, co może mieć kluczowe znaczenie dla identyfikacji luk w zabezpieczeniach lub anomalii. Sequencer pomaga w analizie entropii tokenów, dostarczając informacji na temat losowości ich generacji, a tym samym poziomu bezpieczeństwa. Organizer umożliwia przechowywanie i adnotowanie kopii żądań HTTP, które można później przejrzeć.

Podstawowa znajomość tych narzędzi wyposaży Cię w szerszy wachlarz umiejętności w zakresie testowania penetracyjnego aplikacji internetowych.

W kolejnej i ostatniej sali tego modułu zapoznasz się z narzędziem [Burp Suite Extensions](https://tryhackme.com/room/burpsuiteextensions) .
