---

Celem tego pokoju jest zapoznanie użytkowników z podstawowymi koncepcjami kryptografii, takimi jak:

- Szyfrowanie symetryczne, takie jak AES
- Szyfrowanie asymetryczne, takie jak RSA
- Wymiana kluczy Diffie-Hellman
- Haszowanie
- Infrastruktura klucza publicznego

Załóżmy, że chcesz wysłać wiadomość, której nikt poza adresatem nie zrozumie. Jak to zrobić?

![Dokument ściśle tajny z napisem WUB KDFN PH](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a31ad9ee6b4e321453508e8662fc4679.png)  

Jednym z najprostszych szyfrów jest szyfr Cezara, używany ponad 2000 lat temu. Szyfr Cezara przesuwa literę o ustaloną liczbę miejsc w lewo lub w prawo. Rozważmy przypadek przesunięcia o 3 miejsca w prawo w celu zaszyfrowania, jak pokazano na poniższym rysunku.

![Ilustracja szyfrowania szyfrem Cezara](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/b4f1cbf444e5f19f855dadb7f272ab50.png)  

Odbiorca musi wiedzieć, że tekst został przesunięty o 3 w prawo, aby odzyskać oryginalną wiadomość.

![Ilustracja deszyfrowania szyfru Cezara](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/45b482f79ebcc2f202813a5d7de4df87.png)  

Używając tego samego klucza do zaszyfrowania „TRY HACK ME”, otrzymujemy „WUB KDFN PH”.

Szyfr Cezara, który opisaliśmy powyżej, może używać klucza od 1 do 25. Przy kluczu 1 każda litera jest przesuwana o jedną pozycję, gdzie A zmienia się w B, a Z w A. Przy kluczu 25 każda litera jest przesuwana o 25 pozycji, gdzie A zmienia się w Z, a B w A. Klucz 0 oznacza brak zmiany; co więcej, klucz 26 również nie spowoduje zmiany, ponieważ doprowadzi do pełnego obrotu. W związku z tym wnioskujemy, że szyfr Cezara ma przestrzeń kluczy 25; użytkownik ma do wyboru 25 różnych kluczy.

Rozważmy przypadek, w którym przechwyciliśmy wiadomość zaszyfrowaną szyfrem Cezara: „YMNX NX FQUMF GWFAT HTSYFHYNSL YFSLT MTYJQ RNPJ”. Zostaliśmy poproszeni o odszyfrowanie jej bez znajomości klucza. Możemy spróbować tego metodą siłową, tj. wypróbować wszystkie możliwe klucze i sprawdzić, który jest najbardziej sensowny. Na poniższym rysunku zauważyliśmy, że klucz 5 jest najbardziej sensowny: „THIS IS ALPHA BRAVO CONTACTING TANGO HOTEL MIKE”.

![Odszyfrowanie tekstu zaszyfrowanego poprzez wypróbowanie wszystkich możliwych kluczy, czyli metodą siłową](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/83c79636b07babb43ffe5402e2697772.png)  

Szyfr Cezara jest uważany za **szyfr podstawieniowy,** ponieważ każda litera alfabetu jest zastępowana inną.

Innym rodzajem szyfru jest **szyfr transpozycyjny** , który szyfruje wiadomość poprzez zmianę kolejności liter. Rozważmy prosty szyfr transpozycyjny na poniższym rysunku. Zaczynamy od wiadomości „THIS IS ALPHA BRAVO CONTACTING TANGO HOTEL MIKE” i klucza `42351`. Po napisaniu liter naszej wiadomości poprzez wypełnienie jednej kolumny po drugiej, przestawiamy kolumny na podstawie klucza, a następnie odczytujemy wiersze. Innymi słowy, zapisujemy kolumnami i odczytujemy wierszami. Zauważ również, że w tym przykładzie zignorowaliśmy całą przestrzeń w tekście jawnym. Wynikowy szyfrogram „NPCOTGHOTH…” jest odczytywany wiersz po wierszu. Innymi słowy, szyfr transpozycyjny po prostu przestawia kolejność liter, w przeciwieństwie do szyfru podstawieniowego, który podstawia litery bez zmiany ich kolejności.

![Ilustracja szyfru transpozycyjnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d1c99f9bf3e305eb4b50cb8c30be430d.png)  

To zadanie wprowadziło proste szyfry podstawieniowe i transpozycyjne oraz zastosowało je do wiadomości złożonych ze znaków alfabetycznych. Aby algorytm szyfrowania był uważany za **bezpieczny** , odtworzenie oryginalnej wiadomości, tj. tekstu jawnego, powinno być niemożliwe. (Mówiąc matematycznie, potrzebujemy **trudnego** problemu, tj. problemu, którego nie da się rozwiązać w czasie wielomianowym. Problem, który możemy rozwiązać w czasie wielomianowym, to problem, który jest wykonalny nawet dla dużej ilości danych wejściowych, chociaż jego rozwiązanie może zająć komputerowi sporo czasu).

Jeśli zaszyfrowaną wiadomość uda się złamać w ciągu tygodnia, zastosowane szyfrowanie będzie uznane za niebezpieczne. Jeśli jednak uda się złamać zaszyfrowaną wiadomość w ciągu miliona lat, szyfrowanie będzie można uznać za praktycznie bezpieczne.

Rozważmy monoalfabetyczny szyfr podstawieniowy, w którym każda litera jest odwzorowywana na nową literę. Na przykład, w języku angielskim „a” jest odwzorowywane na jedną z 26 liter alfabetu angielskiego, następnie „b” jest odwzorowywane na jedną z pozostałych 25 liter alfabetu angielskiego, a następnie „c” jest odwzorowywane na jedną z pozostałych 24 liter alfabetu angielskiego i tak dalej.

Na przykład, moglibyśmy wybrać litery alfabetu „abcdefghijklmnopqrstuvwxyz”, które mają zostać zmapowane na „xpatvrzyjhecsdikbfwunqgmol”. Innymi słowy, „a” staje się „x”, „b” staje się „p” i tak dalej. Odbiorca musi znać klucz „xpatvrzyjhecsdikbfwunqgmol”, aby pomyślnie odszyfrować zaszyfrowane wiadomości.

Ten algorytm może wydawać się bardzo bezpieczny, zwłaszcza że wypróbowanie wszystkich możliwych kluczy nie jest wykonalne. Jednakże, różne techniki mogą być użyte do złamania szyfrogramu za pomocą takiego algorytmu szyfrującego. Jedną ze słabości takiego algorytmu jest częstotliwość występowania liter. W tekstach angielskich najczęstszymi literami są „e”, „t” i „a”, które pojawiają się odpowiednio z częstotliwością 13%, 9,1% i 8,2%. Ponadto, w tekstach angielskich najczęstszymi pierwszymi literami są „t”, „a” i „o”, które pojawiają się odpowiednio z częstotliwością 16%, 11,7% i 7,6%. Dodaj do tego fakt, że większość słów w wiadomościach to słowa słownikowe, a będziesz w stanie złamać zaszyfrowany tekst za pomocą alfabetycznego szyfru podstawieniowego w mgnieniu oka.

Tak naprawdę nie musimy używać klucza szyfrującego, aby odszyfrować otrzymany tekst zaszyfrowany: „Uyv sxd gyi siqvw x sinduxjd pvzjdw po axffojdz xgxo wsxcc wuidvw”. Jak pokazano na poniższym rysunku, korzystając ze strony internetowej takiej jak [quipqiup](https://www.quipqiup.com/) , zajmie chwilę odkrycie, że oryginalny tekst brzmiał: „Człowiek, który przenosi góry, zaczyna od noszenia małych kamieni”. Ten przykład wyraźnie pokazuje, że ten algorytm jest zepsuty i nie powinien być używany do poufnej komunikacji.

![Zrzut ekranu strony internetowej quipquip](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0b4ac26e6f49c1156b6dc5c283b413a7.png)

#Szyfrowanie #Symetryczne

Przyjrzyjmy się pewnej terminologii:

- **Algorytm kryptograficzny** lub **szyfr** : Algorytm ten definiuje procesy szyfrowania i deszyfrowania.
- **Klucz** : Algorytm kryptograficzny potrzebuje klucza, aby zamienić tekst jawny na tekst zaszyfrowany i odwrotnie.
- **tekst jawny** to oryginalna wiadomość, którą chcemy zaszyfrować
- **szyfrogram** to wiadomość w zaszyfrowanej formie

Algorytm szyfrowania symetrycznego używa tego samego klucza do szyfrowania i deszyfrowania. W związku z tym strony komunikacji muszą uzgodnić klucz tajny, zanim będą mogły wymieniać wiadomości.

Na poniższym rysunku nadawca przekazuje procesowi _szyfrowania_ tekst jawny i klucz do uzyskania tekstu zaszyfrowanego. Tekst zaszyfrowany jest zazwyczaj przesyłany kanałem komunikacyjnym.

![Ogólny schemat blokowy szyfrowania z użyciem klucza tajnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/dc0cc0d61133400277c47d039d8d69e1.png)  

Z drugiej strony, odbiorca przekazuje procesowi _odszyfrowania_ ten sam klucz, którego nadawca użył do odzyskania oryginalnego tekstu jawnego z otrzymanego szyfrogramu. Bez znajomości klucza odbiorca nie będzie w stanie odzyskać tekstu jawnego.

![Ogólny schemat blokowy deszyfrowania za pomocą klucza tajnego](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/4003a3e6e0ecd139078eefe30a336ce2.png)  

Narodowy Instytut Standardów i Technologii ( NIST ) opublikował w 1977 roku Standard Szyfrowania Danych ( DES ). DES to symetryczny algorytm szyfrowania wykorzystujący klucz o długości 56 bitów. W 1997 roku rozwiązano problem złamania wiadomości zaszyfrowanej algorytmem DES . W rezultacie wykazano, że możliwe stało się znalezienie klucza metodą siłową i złamanie wiadomości zaszyfrowanej algorytmem DES . W 1998 roku klucz DES został złamany w ciągu 56 godzin. Przypadki te wskazywały, że algorytm DES nie może być już uważany za bezpieczny.

NIST opublikował Advanced Encryption Standard ( AES ) w 2001 roku. Podobnie jak DES , jest to algorytm szyfrowania symetrycznego, jednak wykorzystuje klucz o długości 128, 192 lub 256 bitów i nadal jest uważany za bezpieczny i jest nadal używany. AES powtarza następujące cztery transformacje wielokrotnie:

1. `SubBytes(state)`:Ta transformacja wyszukuje każdy bajt w danej tablicy podstawień (S-box) i zastępuje go odpowiednią wartością. To `state`16 bajtów, czyli 128 bitów, zapisanych w tablicy 4x4.
2. `ShiftRows(state)`:Drugi wiersz jest przesunięty o jedno miejsce, trzeci o dwa miejsca, a czwarty o trzy miejsca. Widać to na poniższym rysunku.
3. `MixColumns(state)`:Każda kolumna jest mnożona przez stałą macierz (tablica 4 na 4).
4. `AddRoundKey(state)`:Klucz rundy jest dodawany do stanu za pomocą operacji XOR.

![Ilustracja funkcji ShiftRows zastosowanej do tablicy cztery na cztery](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/049bad7deb4e6dd426335d7c3477f10a.png)  

Całkowita liczba rund transformacji zależy od rozmiaru klucza.  

Nie martw się, jeśli uważasz to za zagadkowe, bo tak właśnie jest! Naszym celem nie jest zgłębianie szczegółów działania AES ani implementacja go jako biblioteki programistycznej; naszym celem jest docenienie różnicy w złożoności między starożytnymi a współczesnymi algorytmami szyfrowania. Jeśli chcesz zagłębić się w szczegóły, możesz sprawdzić specyfikacje AES, w tym pseudokod i przykłady, w opublikowanym standardzie [FIPS PUB 197](https://csrc.nist.gov/publications/detail/fips/197/final) .

Oprócz AES, wiele innych algorytmów szyfrowania symetrycznego jest uznawanych za bezpieczne. Oto lista algorytmów szyfrowania symetrycznego obsługiwanych przez GPG (GnuPG) 2.37.7, na przykład:

|Algorytm szyfrowania|Notatki|
|---|---|
|AES, AES192 i AES256|AES z kluczem o rozmiarze 128, 192 i 256 bitów|
|POMYSŁ|Międzynarodowy algorytm szyfrowania danych (IDEA)|
|3DES|Triple DES (Data Encryption Standard) jest oparty na DES. Należy pamiętać, że 3DES zostanie wycofany w 2023 roku, a w 2024 roku stanie się niedozwolony.|
|CAST5|Znany również jako CAST-128. Niektóre źródła podają, że CAST to skrót od nazwisk jego autorów: Carlisle Adams i Stafford Tavares.|
|ROZDYMKA|Zaprojektowany przez Bruce'a Schneiera|
|DWURYBNY|Zaprojektowany przez Bruce'a Schneiera i wywodzący się z Blowfish|
|CAMELLIA128, CAMELLIA192 i CAMELLIA256|Zaprojektowany przez Mitsubishi Electric i NTT w Japonii. Nazwa pochodzi od kwiatu kamelii japońskiej.|

Wszystkie wymienione do tej pory algorytmy to symetryczne algorytmy szyfrowania blokowego. Algorytm szyfrowania blokowego konwertuje dane wejściowe (tekst jawny) na bloki i szyfruje każdy blok. Blok ma zazwyczaj 128 bitów. Na poniższym rysunku chcemy zaszyfrować tekst jawny „TANGO HOTEL MIKE”, składający się z 16 znaków. Pierwszym krokiem jest przedstawienie go w systemie binarnym. W kodzie ASCII „T” jest `0x54`w formacie szesnastkowym, „A” to `0x41`, itd. Każde dwie cyfry szesnastkowe stanowią 8 bitów i reprezentują jeden bajt. Blok 128 bitów ma praktycznie 16 bajtów i jest reprezentowany w tablicy 4x4. 128-bitowy blok jest przekazywany jako pojedyncza jednostka do metody szyfrowania.

![Przykład algorytmu szyfrowania blokowego zastosowanego do tablicy cztery na cztery](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/2d69973a4fbf8220e64c3e896841b21d.png)  

Innym rodzajem algorytmu szyfrowania symetrycznego są szyfry strumieniowe, które szyfrują tekst jawny bajt po bajcie. Rozważmy przypadek, w którym chcemy zaszyfrować wiadomość „TANGO HOTEL MIKE”; każdy znak musi zostać przekonwertowany na jego reprezentację binarną. Jeśli użyjemy kodu ASCII, „T” będzie `0x54`w systemie szesnastkowym, „A” w systemie szesnastkowym `0x41`itd. Metoda szyfrowania będzie przetwarzać jeden bajt na raz. Jest to przedstawione na poniższym rysunku.

![Przykład algorytmu szyfrowania strumieniowego zastosowanego do tablicy bajtów](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/6c0edb0faf15df0c6675c6829fddae01.png)  

Szyfrowanie symetryczne rozwiązuje wiele problemów bezpieczeństwa omawianych w sali poświęconej [zasadom bezpieczeństwa](https://tryhackme.com/room/securityprinciples) . Załóżmy, że Alicja i Bob spotkali się, wybrali algorytm szyfrowania i uzgodnili konkretny klucz. Zakładamy, że wybrany algorytm szyfrowania jest bezpieczny, a klucz tajny jest bezpieczny. Przyjrzyjmy się, co możemy osiągnąć:

- **Poufność** : Gdyby Ewa przechwyciła zaszyfrowaną wiadomość, nie byłaby w stanie odzyskać tekstu jawnego. W związku z tym wszystkie wiadomości wymieniane między Alicją a Bobem są poufne, o ile są wysyłane w formie zaszyfrowanej.
- **Integralność** : Kiedy Bob otrzyma zaszyfrowaną wiadomość i pomyślnie ją odszyfruje, używając klucza uzgodnionego z Alicją, może mieć pewność, że nikt nie mógł zmanipulować wiadomości przez kanał. W przypadku stosowania bezpiecznych, nowoczesnych algorytmów szyfrowania, każda drobna modyfikacja szyfrogramu uniemożliwiłaby pomyślne odszyfrowanie lub doprowadziłaby do powstania bełkotu w postaci tekstu jawnego.
- **Autentyczność** : Możliwość odszyfrowania tekstu zaszyfrowanego za pomocą klucza tajnego stanowi również dowód autentyczności wiadomości, ponieważ tylko Alicja i Bob znają klucz tajny.

Dopiero zaczynamy i wiemy, jak zachować poufność, sprawdzić integralność i zapewnić autentyczność wymienianych wiadomości. Bardziej praktyczne i efektywne podejścia zostaną zaprezentowane w kolejnych zadaniach. Na razie pytanie brzmi, czy jest to skalowalne.

W przypadku Alicji i Boba potrzebowaliśmy jednego klucza. Jeśli mamy Alicję, Boba i Charliego, potrzebujemy trzech kluczy: jednego dla Alicji i Boba, drugiego dla Alicji i Charliego oraz trzeciego dla Boba i Charliego. Jednak liczba kluczy szybko rośnie; komunikacja między 100 użytkownikami wymaga prawie 5000 różnych kluczy tajnych. (Jeśli ciekawi Cię matematyka, która za tym stoi, to jest to 99 + 98 + 97 + … + 1 = 4950).

Co więcej, jeśli jeden system zostanie naruszony, konieczne będzie utworzenie nowych kluczy do użytku z pozostałymi 99 użytkownikami. Kolejnym problemem byłoby znalezienie bezpiecznego kanału do wymiany kluczy ze wszystkimi innymi użytkownikami. Oczywiście, sytuacja szybko wymyka się spod kontroli.

W następnym zadaniu zajmiemy się szyfrowaniem asymetrycznym. Jednym z problemów rozwiązywanych przez szyfrowanie asymetryczne jest sytuacja, gdy 100 użytkowników musi dzielić się zaledwie 100 kluczami, aby zapewnić bezpieczną komunikację. (Jak wyjaśniono wcześniej, szyfrowanie symetryczne wymagałoby około 5000 kluczy, aby zabezpieczyć komunikację dla 100 użytkowników).

Dostępnych jest wiele programów do szyfrowania symetrycznego. Skupimy się na dwóch, które są również szeroko stosowane do szyfrowania asymetrycznego:

- GNU Privacy Guard
- Projekt OpenSSL

### GNU Privacy Guard

GNU [Privacy Guard](https://gnupg.org/) , znany również jako GnuPG lub GPG, implementuje standard OpenPGP.

Możemy zaszyfrować plik za pomocą GnuPG (GPG) korzystając z następującego polecenia:

`gpg --symmetric --cipher-algo CIPHER message.txt`, gdzie CIPHER to nazwa algorytmu szyfrowania. Obsługiwane szyfry można sprawdzić poleceniem `gpg --version`. Zaszyfrowany plik zostanie zapisany jako `message.txt.gpg`.

Domyślnie dane wyjściowe są w binarnym formacie OpenPGP; jeśli jednak wolisz utworzyć dane wyjściowe w formacie ASCII, które można otworzyć w dowolnym edytorze tekstu, powinieneś dodać opcję `--armor`. Na przykład: `gpg --armor --symmetric --cipher-algo CIPHER message.txt`.

Możesz odszyfrować za pomocą następującego polecenia:

`gpg --output original_message.txt --decrypt message.gpg`

### Projekt OpenSSL

Projekt [OpenSSL](https://www.openssl.org/) utrzymuje oprogramowanie OpenSSL.

Możemy zaszyfrować plik za pomocą OpenSSL, korzystając z następującego polecenia:

`openssl aes-256-cbc -e -in message.txt -out encrypted_message`

Wynikowy plik możemy odszyfrować za pomocą następującego polecenia:

`openssl aes-256-cbc -d -in encrypted_message -out original_message.txt`

Aby szyfrowanie było bezpieczniejsze i bardziej odporne na ataki siłowe, możemy dodać `-pbkdf2`funkcję wyprowadzania klucza opartego na haśle 2 (PBKDF2); co więcej, możemy określić liczbę iteracji hasła w celu wyprowadzenia klucza szyfrującego za pomocą `-iter NUMBER`. Aby wykonać iterację 10 000 razy, poprzednie polecenie wyglądałoby następująco:

`openssl aes-256-cbc -pbkdf2 -iter 10000 -e -in message.txt -out encrypted_message`

W rezultacie polecenie odszyfrowania wygląda następująco:

`openssl aes-256-cbc -pbkdf2 -iter 10000 -d -in encrypted_message -out original_message.txt`

W poniższych pytaniach wykorzystamy `gpg` i `openssl`w AttackBoxie do przeprowadzenia szyfrowania symetrycznego.

Pliki niezbędne do wykonania tego zadania znajdują się w katalogu `/root/Rooms/cryptographyintro/task02`.  **Plik zip dołączony do tego zadania można wykorzystać do rozwiązania pytań z zadań 2, 3, 4, 5 i 6** .

Wymiana kluczy #Diffiego-Hellmana

Alicja i Bob mogą komunikować się przez niezabezpieczony kanał. Przez niezabezpieczony rozumiemy podsłuchiwanie wiadomości wymienianych na tym kanale. Jak Alicja i Bob mogą uzgodnić klucz tajny w takiej sytuacji? Jednym ze sposobów byłoby wykorzystanie wymiany kluczy Diffiego-Hellmana.

Algorytm Diffiego-Hellmana to asymetryczny algorytm szyfrowania. Umożliwia on wymianę sekretu przez kanał publiczny. Pominiemy podstawy arytmetyki modularnej i przedstawimy prosty przykład liczbowy. Potrzebne będą dwa działania matematyczne: potęgowanie i modulo. _xp_ _,_ tj. _x_ podniesione do potęgi _p_ , to _x_ pomnożone przez siebie _p_ razy. Ponadto _x_ mod _m_ , tj. _x_ modulo _m_ , to reszta z dzielenia _x_ przez _m_ .

1. Alicja i Bob zgadzają się co do _q_ i _g_ . Aby to zadziałało, _q_ musi być liczbą pierwszą, a _g_ musi być liczbą mniejszą od _q_ , spełniającą określone warunki. (W arytmetyce modularnej _g_ jest generatorem). W tym przykładzie przyjmujemy _q_  = 29 i _g_  = 3 .
2. Alicja wybiera losową liczbę _a_ mniejszą niż _q_ . Oblicza _A_  = ( _g_ _a_ ) mod _q_ . Liczba _a_ musi pozostać tajemnicą; jednak _A_ jest wysyłana do Boba. Załóżmy, że Alicja wybiera liczbę _a_  = 13 i oblicza _A_  = 3 13 % 29 = 19 , a następnie wysyła ją do Boba.
3. Bob losuje liczbę _b_ mniejszą niż _q_ . Oblicza _B_  = ( _g_ _b_ ) mod _q_ . Bob musi zachować _b_ w tajemnicy, jednak wysyła _B_ Alicji. Rozważmy przypadek, w którym Bob wybiera liczbę _b_  = 15 i oblicza _B_  = 3 15 % 29 = 26 . Następnie wysyła ją Alicji.
4. Alicja otrzymuje _B_ i oblicza _klucz_ _e_ _y_  =  _B_ _a_ mod _q_ . Przykład liczbowy _klucz_ _e_ _y_  = 26 13 mod 29 = 10.
5. _Bob_ otrzymuje _A_ i oblicza _klucz_ _y_  =  _A_ _b_ mod _q_ . Przykład liczbowy _klucz_ _y_ _=_  19 15 mod 29 = 10.

Widzimy, że Alicja i Bob dotarli do tego samego klucza.

_Chociaż_ podsłuchujący poznał wartości _q_ ,  _g_ ,  _A_ i _B_ , nie będzie w stanie obliczyć tajnego _klucza_ , _którym_ wymienili się Alicja i Bob. Powyższe kroki podsumowano na poniższym rysunku.

![Ilustracja graficzna przedstawiająca przykład liczbowy pięciu kroków metody Diffiego-Hellmana](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/6993f1edbc899d252e949ac403294d52.png)  

Chociaż wybrane przez nas liczby ułatwiają znalezienie _a_ i _b_ , nawet bez użycia komputera, w rzeczywistych przykładach wylosowalibyśmy _q_ o długości 256 bitów. W liczbach dziesiętnych to 115 z 75 zerami po prawej stronie (też nie wiem, jak to odczytać, ale powiedziano mi, że można to odczytać jako 115 quattuorvigintillion). Tak duże q _uniemożliwi_ znalezienie _a_ lub _b,_ pomimo znajomości _q_ ,  _g_ ,  _A_ i _B._

Przyjrzyjmy się rzeczywistym parametrom Diffie-Hellmana. Możemy `openssl`ich użyć do wygenerowania; musimy określić opcję `dhparam`, która wskazuje, że chcemy generować parametry Diffie-Hellmana wraz z określonym rozmiarem w bitach, na przykład `2048`lub `4096`.

W poniższym wyniku konsoli możemy wyświetlić liczbę pierwszą `P`i generator `G`za pomocą polecenia `openssl dhparam -in dhparams.pem -text -noout`. (Jest to podobne do tego, co zrobiliśmy z kluczem prywatnym RSA).

Terminal

```shell-session
user@TryHackMe$ openssl dhparam -out dhparams.pem 2048
Generating DH parameters, 2048 bit long safe prime
[...]
$ openssl dhparam -in dhparams.pem -text -noout
    DH Parameters: (2048 bit)
    P:   
        00:82:3b:9d:b5:29:31:f8:12:fe:21:e1:90:30:37:
        ac:d2:48:41:f7:d7:55:e5:d2:5d:dd:87:67:9e:bd:
        b3:97:df:05:a9:d2:d9:56:4f:66:b5:d9:d8:65:06:
        58:c3:8f:b3:0e:30:d2:9a:0b:c3:0a:56:8d:fc:0f:
        f2:e2:9e:4f:16:16:93:4e:b9:a4:c3:9c:09:2d:48:
        a2:ec:b6:97:92:63:a3:b4:75:36:3f:51:77:ca:ac:
        44:6d:99:eb:4d:4a:97:d5:4b:52:c8:07:f8:16:30:
        37:d3:b2:47:30:e6:4e:bc:6a:53:d1:9b:6a:4d:91:
        7a:4b:4f:af:3b:f0:ce:b9:ed:91:4d:8b:52:5a:3f:
        bb:6b:06:ae:32:95:7d:53:da:9b:ce:b0:ec:7d:81:
        25:05:d8:ce:ca:76:e7:d1:5a:31:13:d2:9f:62:b4:
        d5:ad:7d:cd:c9:ab:3d:28:e3:92:27:9f:f3:66:a0:
        be:61:49:cc:47:21:d8:e0:2c:e8:c6:35:4b:2f:ba:
        35:36:8f:bb:41:c6:89:b2:60:3c:62:bb:fe:bf:59:
        d3:7f:05:69:55:dc:61:1b:b4:bb:68:fa:65:1e:2e:
        46:2f:2d:21:62:d1:9f:a0:2b:aa:81:df:3a:f9:7d:
        0b:9d:0e:47:68:01:4f:6e:81:cc:4c:2a:91:fc:8c:
        f4:6f
    G:    2 (0x2)
```

Algorytm wymiany kluczy Diffiego-Hellmana pozwala dwóm stronom uzgodnić sekret za pośrednictwem niezabezpieczonego kanału. Omawiana wymiana kluczy jest jednak podatna na atak typu Man-in-the-Middle ( MitM ); atakujący może odpowiedzieć Alicji, podszywając się pod Boba, a następnie odpowiedzieć Bobowi, podszywając się pod Alicję. Rozwiązanie tego problemu omawiamy w Zadaniu 6.

Odpowiedz na poniższe pytania

W AttackBoxie katalog tego zadania znajdziesz w lokalizacji  `/root/Rooms/cryptographyintro/task04`; alternatywnie możesz wykorzystać plik zadania z Zadania 2, aby pracować na własnym komputerze.

Zestaw parametrów Diffiego-Hellmana można znaleźć w pliku  `dhparam.pem`. Jaki jest rozmiar liczby pierwszej w bitach?

#Haszowanie

Kryptograficzna funkcja skrótu to algorytm, który przyjmuje dane o dowolnym rozmiarze jako dane wejściowe i zwraca wartość o stałym rozmiarze, zwaną _skrótem wiadomości_ lub _sumą kontrolną_ , jako wynik. Na przykład, `sha256sum`oblicza skrót wiadomości SHA256 (Secure Hash Algorithm 256). SHA256, jak sama nazwa wskazuje, zwraca sumę kontrolną o rozmiarze 256 bitów (32 bajty). Ta suma kontrolna jest zazwyczaj zapisywana za pomocą cyfr szesnastkowych. Wiedząc, że cyfra szesnastkowa reprezentuje 4 bity, 256-bitową sumę kontrolną można przedstawić jako 64 cyfry szesnastkowe.

W poniższym wyjściu terminala obliczamy wartości skrótu SHA256 dla trzech plików o różnych rozmiarach: 4 bajty, 275 MB i 5,2 GB. Używając `sha256sum`do obliczenia skrótu wiadomości dla każdego z trzech plików, otrzymujemy trzy zupełnie różne wartości, które wydają się losowe. Warto podkreślić, że długość wynikowego skrótu wiadomości lub sumy kontrolnej jest taka sama, niezależnie od rozmiaru pliku. W szczególności, plik czterobajtowy `abc.txt`i plik 5,2 GB skutkowały skrótami wiadomości o tej samej długości, niezależnie od rozmiaru pliku.

Terminal

```shell-session
user@TryHackMe$ ls -lh
total 5.5G
-rw-r--r--. 1 strategos strategos    4  7月 21 12:46 abc.txt
-rw-r--r--. 1 strategos strategos 275M  2月 12 19:08 debian-hurd.img.tar.xz
-rw-r--r--. 1 strategos strategos 5.2G  4月 26 16:55 Win11_English_x64v1.iso
$ sha256sum *
c38bb113c89d8fec6475a9936411007c45563ecb7ce8acd5db7fb58c0872bda0  abc.txt
0317ff0150e0d64b70284b28c97bb788310585ea7ac46cc8139d5a3c850dea55  debian-hurd.img.tar.xz
4bc6c7e7c61af4b5d1b086c5d279947357cff45c2f82021bb58628c2503eb64e  Win11_English_x64v1.iso
```

Ale po co nam taka funkcja? Ma wiele zastosowań, w szczególności:

- Przechowywanie haseł: Zamiast przechowywać hasła w postaci zwykłego tekstu, przechowywany jest ich skrót. W rezultacie, w przypadku naruszenia bezpieczeństwa danych, atakujący otrzyma listę skrótów haseł zamiast haseł oryginalnych. (W praktyce hasła są również „solone”, co zostanie omówione w dalszej części zadania).
- Wykrywanie modyfikacji: Wszelkie drobne zmiany w oryginalnym pliku mogą spowodować drastyczną zmianę wartości skrótu, czyli sumy kontrolnej.

W poniższym wyjściu terminala mamy dwa pliki, `text1.txt`i `text2.txt`, które są niemal identyczne, z wyjątkiem (dosłownie) jednego bitu; litery `T`i `t`różnią się jednym bitem w ich reprezentacji ASCII. Mimo że zmieniliśmy tylko jeden bit, widać wyraźnie, że sumy kontrolne SHA256 są zupełnie różne. W związku z tym, jeśli użyjemy bezpiecznego algorytmu funkcji skrótu, możemy łatwo sprawdzić, czy nastąpiły jakiekolwiek modyfikacje. Może to pomóc w ochronie zarówno przed celową manipulacją, jak i błędami transferu plików.

Terminal

```shell-session
user@TryHackMe$ hexdump text1.txt -C
00000000  54 72 79 48 61 63 6b 4d  65 0a                    |TryHackMe.|
0000000a
$ hexdump text2.txt -C
00000000  74 72 79 48 61 63 6b 4d  65 0a                    |tryHackMe.|
0000000a
$ sha256sum text1.txt
f4616fd825a10ded9af58fbaee09f3e31751d15591f9323ea68b03a0e8ac3783  text1.txt
$ sha256sum text2.txt
9ffa3533ee33998aeb1df76026f8031c8af6ccabd8393eca002d5b7471a0b536  text2.txt
```

Niektóre z używanych algorytmów haszujących, które nadal uważa się za bezpieczne, to:

- SHA224, SHA256, SHA384, SHA512
- RIPEMD160

Niektóre starsze funkcje skrótu, takie jak MD5 (Message Digest 5) i SHA-1, są kryptograficznie złamane. Przez złamane rozumiemy możliwość wygenerowania innego pliku z tą samą sumą kontrolną, co dany plik. Oznacza to, że możemy doprowadzić do kolizji skrótów. Innymi słowy, atakujący może utworzyć nową wiadomość z daną sumą kontrolną, a wykrycie manipulacji plikiem lub wiadomością będzie niemożliwe.

### HMAC

Kod uwierzytelniania wiadomości oparty na haszu (HMAC) to kod uwierzytelniania wiadomości (MAC) wykorzystujący klucz kryptograficzny oprócz funkcji haszującej.

Zgodnie z [RFC2104](https://www.rfc-editor.org/rfc/rfc2104) , HMAC potrzebuje:

- klucz tajny
- pad wewnętrzny (ipad) – stały ciąg znaków. (RFC2104 używa bajtu `0x36`powtórzonego B razy. Wartość B zależy od wybranej funkcji skrótu.)
- pad zewnętrzny (opad) – stały ciąg znaków. (RFC2104 używa bajtu `0x5C`powtórzonego B razy.)

Obliczenie HMAC odbywa się według następujących kroków, jak pokazano na rysunku:

1. Dodaj zera do klucza, aby uzyskać długość B, tzn. aby jego długość odpowiadała długości iPada.
2. Oblicz _klucz_  ⊕  _ipad używając_ _bitowej_ _operacji_ wyłącznego OR (XOR) _,_ _reprezentowanej_ _przez_ ⊕ .
3. Dołącz wiadomość do wyniku XOR z kroku 2.
4. Zastosuj funkcję skrótu do powstałego strumienia bajtów (w kroku 3).
5. Używając _operacji_ XOR, oblicz _klucz_ _⊕_  o  _p_ _a_ _d_ _._
6. Dołącz wynik funkcji skrótu z kroku 4 do wyniku XOR z kroku 5.
7. Zastosuj funkcję skrótu do powstałego strumienia bajtów (w kroku 6), aby uzyskać HMAC.

![Ilustracja graficzna pokazująca sposób obliczania HMAC](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d8b175af1d32a759f66b223efdac8972.png)  

_Powyższy_ rysunek przedstawia kroki wyrażone następującym _wzorem_ : _H_ ( _K_ ⊕ _opad_ , _H_ ( _K_ _⊕_ _ipad_ _,_ _t_ _e_ _x_ _t_ ) _)_ _._

Aby obliczyć HMAC w systemie Linux, można użyć dowolnego z dostępnych narzędzi, takich jak `hmac256`(lub `sha224hmac`, `sha256hmac`, `sha384hmac`i `sha512hmac`, gdzie klucz tajny jest dodawany po opcji `--key`). Poniżej przedstawiamy przykład obliczenia HMAC przy użyciu `hmac256`i `sha256hmac`z dwoma różnymi kluczami.

Terminal

```shell-session
user@TryHackMe$ hmac256 s!Kr37 message.txt
3ec65b7e80c5bf2e623e52e0528f1c6a74f605b10616621ba1c22a89fb244e65  message.txt

user@TryHackMe$ hmac256 1234 message.txt
4b6a2783631180fca6128592e3d17fb5bff6b0e563ad8f1c6afc1050869e440f  message.txt

user@TryHackMe$ sha256hmac message.txt --key s!Kr37
3ec65b7e80c5bf2e623e52e0528f1c6a74f605b10616621ba1c22a89fb244e65  message.txt

user@TryHackMe$ sha256hmac message.txt --key 1234
4b6a2783631180fca6128592e3d17fb5bff6b0e563ad8f1c6afc1050869e440f  message.txt
```

Odpowiedz na poniższe pytania

W AttackBoxie katalog tego zadania znajdziesz w lokalizacji  `/root/Rooms/cryptographyintro/task05`; alternatywnie możesz wykorzystać plik zadania z Zadania 2, aby pracować na własnym komputerze.

Jaka jest suma kontrolna SHA256 pliku  `order.json`?

#PKI/SSL/TLS
Wykorzystanie wymiany kluczy, takiej jak wymiana kluczy Diffiego-Hellmana, pozwala nam uzgodnić tajny klucz pod czujnym okiem i uszami podsłuchujących. Klucz ten może być używany z algorytmem szyfrowania symetrycznego w celu zapewnienia poufności komunikacji. Jednak opisana wcześniej wymiana kluczy nie jest odporna na ataki typu Man-in-the-Middle ( MITM ). Dzieje się tak, ponieważ Alicja nie ma możliwości upewnienia się, że komunikuje się z Bobem, a Bob nie ma możliwości upewnienia się, że komunikuje się z Alicją podczas wymiany tajnego klucza.

Rozważ poniższy rysunek. Jest to atak na wymianę kluczy, opisaną w zadaniu wymiany kluczy Diffiego-Hellmana. Kroki są następujące:

1. Alicja i Bob zgadzają się co do _q_ i _g_ . Każdy, kto podsłuchuje kanał komunikacyjny, może odczytać te dwie wartości, w tym atakujący, Mallory.
2. Jak zwykle, Alicja wybiera zmienną losową _a_ , oblicza _A_ ( _A_  = ( _g_ _a_ ) mod _q_ ) i wysyła _A_ do Boba. Mallory czekała na ten krok i wybrała zmienną losową _m_ oraz obliczyła odpowiadającą jej _M_ . Gdy tylko Mallory otrzyma _A_ , wysyła _M_ do Boba, udając, że jest Alicją.
3. Bob odbiera _M,_ myśląc, że wysłała je Alicja. Bob wybrał już zmienną losową _b_ i obliczył odpowiednią _B_ ; ​​wysyła _B_ do Alicji. Podobnie, Mallory przechwytuje wiadomość, odczytuje _B_ i wysyła _M_ do Alicji.
4. Alicja otrzymuje _M_ i oblicza _klucz_ _e_ _y_  =  _M_ _a_ mod _q_ .
5. Bob otrzymuje _M_ i oblicza _klucz_ _e_ _y_  =  _M_ _b_ mod _q_ .

Alicja i Bob nadal komunikują się ze sobą, myśląc, że komunikują się bezpośrednio, nieświadomi, że komunikują się z Mallory, która może czytać i modyfikować wiadomości przed wysłaniem ich do zamierzonego odbiorcy.

![Ilustracja przedstawiająca atak typu Man-in-the-Middle na wymianę kluczy Diffie-Hellmana](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/640464d74c639afe684eed13c6707229.png)  

Ta podatność wymaga mechanizmu, który pozwoliłby nam potwierdzić tożsamość drugiej strony. To prowadzi nas do Infrastruktury Klucza Publicznego ( PKI ).

Rozważmy przypadek, w którym przeglądasz witrynę [example.org](https://example.org/) przez protokół HTTPS. Jak możesz mieć pewność, że rzeczywiście komunikujesz się z serwerem `example.org`(-ami)? Innymi słowy, jak możesz mieć pewność, że żaden pośrednik (man-in-the-middle) nie przechwycił pakietów i nie zmodyfikował ich, zanim dotarły do ​​Ciebie? Odpowiedź leży w certyfikacie witryny.

Poniższy rysunek przedstawia stronę, którą widzimy podczas przeglądania witryny example.org. Większość przeglądarek oznacza szyfrowane połączenie ikoną kłódki. Ta ikona kłódki oznacza, że ​​połączenie jest zabezpieczone przez HTTPS i posiada ważny certyfikat.

![Zrzut ekranu przeglądarki pokazujący ikonę kłódki oznaczającą połączenie szyfrowane](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0c5bba05433f39f193e19b111a623f33.png)  

W chwili pisania tego tekstu example.org korzysta z certyfikatu podpisanego przez DigiCert Inc., jak pokazano na poniższym rysunku. Innymi słowy, DigiCert potwierdza ważność tego certyfikatu (do określonej daty).

![Zrzut ekranu pokazujący ważność certyfikatu witryny internetowej](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/22c1e51aec7038f6247317f8c3299616.png)  

Aby certyfikat został podpisany przez urząd certyfikacji, musimy:

1. Generowanie żądania podpisania certyfikatu (CSR): Tworzysz certyfikat i wysyłasz swój klucz publiczny do podpisania przez osobę trzecią.
2. Wyślij CSR do urzędu certyfikacji (CA): Celem jest podpisanie certyfikatu przez urząd certyfikacji. Alternatywnym i zazwyczaj niebezpiecznym rozwiązaniem byłoby samodzielne podpisanie certyfikatu.

Aby to zadziałało, odbiorca powinien rozpoznać i zaufać urzędowi certyfikacji, który podpisał certyfikat. Jak można się spodziewać, nasza przeglądarka ufa DigiCert Inc. jako urzędowi certyfikacji; w przeciwnym razie wyświetliłaby ostrzeżenie o bezpieczeństwie zamiast przejść do żądanej witryny.

![Zrzut ekranu przedstawiający urzędy certyfikacji, którym ufa przeglądarka internetowa](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0892193b8b3defdc3cedbc1dcf1843a8.png)  

Żądanie podpisania certyfikatu można `openssl`wygenerować za pomocą polecenia `openssl req -new -nodes -newkey rsa:4096 -keyout key.pem -out cert.csr`. Użyliśmy następujących opcji:

- `req -new`utwórz nowe żądanie podpisania certyfikatu
- `-nodes`zapisz klucz prywatny bez hasła
- `-newkey`wygeneruj nowy klucz prywatny
- `rsa:4096`wygeneruj klucz RSA o rozmiarze 4096 bitów
- `-keyout`określ, gdzie zapisać klucz
- `-out`zapisz prośbę o podpisanie certyfikatu

Następnie zostaniesz poproszony o odpowiedź na serię pytań, tak jak pokazano na poniższym wyjściu konsoli.

Terminal

```shell-session
user@TryHackMe$ openssl req -new -nodes -newkey rsa:4096 -keyout key.pem -out cert.csr
[...]
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:UK
State or Province Name (full name) []:London
Locality Name (eg, city) [Default City]:London
[...]
```

Gdy plik CSR będzie gotowy, możesz wysłać go do wybranego urzędu certyfikacji, aby został podpisany i przygotowany do użycia na Twoim serwerze.

Gdy klient, czyli przeglądarka, otrzyma podpisany certyfikat, któremu ufa, następuje uzgadnianie SSL/TLS. Celem jest uzgodnienie szyfrów i klucza tajnego.

Właśnie opisaliśmy, jak PKI ma zastosowanie do certyfikatów internetowych i SSL/TLS. Zaufana strona trzecia jest niezbędna, aby system był skalowalny.

W celach testowych utworzyliśmy certyfikat podpisany samodzielnie. Na przykład, poniższe polecenie wygeneruje certyfikat podpisany samodzielnie.

`openssl req -x509 -newkey -nodes rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365`

Oznacza to `-x509`, że chcemy wygenerować certyfikat z podpisem własnym zamiast żądania certyfikatu. Określa `-sha256`użycie skrótu SHA-256. Będzie on ważny przez rok, ponieważ dodaliśmy `-days 365`.

Aby odpowiedzieć na poniższe pytania, musisz sprawdzić plik certyfikatu `cert.pem`w `task06`katalogu. Możesz użyć następującego polecenia, aby wyświetlić swój certyfikat:

`openssl x509 -in cert.pem -text

Uwierzytelnianie za pomocą haseł

Zobaczmy, jak kryptografia może pomóc zwiększyć bezpieczeństwo haseł. Dzięki PKI i SSL/ TLS możemy komunikować się z dowolnym serwerem i podawać nasze dane logowania, jednocześnie zapewniając, że nikt nie będzie mógł odczytać naszych haseł przesyłanych przez sieć. To przykład ochrony danych w ruchu. Przyjrzyjmy się, jak możemy chronić hasła podczas ich zapisywania w bazie danych, czyli w stanie spoczynku .

Najmniej bezpieczną metodą byłoby zapisanie nazwy użytkownika i hasła w bazie danych. W ten sposób każde naruszenie danych ujawniłoby hasła użytkowników. Nie wymaga to żadnego wysiłku poza odczytaniem bazy danych zawierającej hasła.

|Nazwa użytkownika|hasło|
|---|---|
|`alice`|`qwerty`|
|`bob`|`dragon`|
|`charlie`|`princess`|

Ulepszone podejście polegałoby na zapisaniu nazwy użytkownika i zahaszowanej wersji hasła w bazie danych. W ten sposób wyciek danych ujawniłby zahaszowane wersje haseł. Ponieważ funkcja haszująca jest nieodwracalna, atakujący musi wielokrotnie próbować różnych haseł, aby znaleźć to, które da ten sam hasz. Poniższa tabela przedstawia sumę MD5 haseł. (Wybraliśmy MD5 tylko po to, aby pole hasła było małe w tym przykładzie; w przeciwnym razie użylibyśmy algorytmu SHA256 lub czegoś bezpieczniejszego).

|Nazwa użytkownika|Hash (hasło)|
|---|---|
|`alice`|`d8578edf8458ce06fbc5bb76a58c5ca4`|
|`bob`|`8621ffdbc5698829397d97767ac13db3`|
|`charlie`|`8afa847f50a716e64932d995c8e7435a`|

Poprzednie podejście wydawało się bezpieczne, jednak dostępność tablic tęczowych sprawiła, że ​​stało się ono niebezpieczne. **Tablica tęczowa** zawiera listę haseł wraz z ich wartościami skrótu. W związku z tym atakujący musi jedynie sprawdzić hash, aby odzyskać hasło. Na przykład, łatwo byłoby sprawdzić `d8578edf8458ce06fbc5bb76a58c5ca4`oryginalne hasło do `alice`. W związku z tym musimy znaleźć bezpieczniejsze metody bezpiecznego zapisywania haseł; możemy dodać sól. **Sól** to losowa wartość, którą możemy dodać do hasła przed jego hashowaniem. Przykład pokazano poniżej.

|Nazwa użytkownika|Hash (hasło + sól)|Sól|
|---|---|---|
|`alice`|`8a43db01d06107fcad32f0bcfa651f2f`|`12742`|
|`bob`|`aab2b680e6a1cb43c79180b3d1a38beb`|`22861`|
|`charlie`|`3a40d108a068cdc8e7951b82d312129b`|`16056`|

W powyższej tabeli użyto `hash(password + salt)`; innym podejściem byłoby użycie `hash(hash(password) + salt)`. Zwróć uwagę, że użyliśmy stosunkowo małej soli wraz z funkcją skrótu MD5 . Powinniśmy przejść na (bezpieczniejszą) funkcję skrótu i ​​dużą sól dla większego bezpieczeństwa, gdyby to była rzeczywista konfiguracja.

Innym ulepszeniem, które możemy wprowadzić przed zapisaniem hasła, jest użycie funkcji pochodnej klucza, takiej jak PBKDF2 (Password-Based Key Derivation Function 2). PBKDF2 pobiera hasło i sól, a następnie przesyła je przez określoną liczbę iteracji, zazwyczaj setek tysięcy.

Jeśli chcesz poznać inne techniki związane z przechowywaniem haseł, zalecamy zapoznanie się z [ściągawką dotyczącą przechowywania haseł.](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
# Arkusz ściągawek dotyczący przechowywania haseł[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

## Wstęp[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Ta ściągawka zawiera wskazówki dotyczące prawidłowych metod przechowywania haseł do uwierzytelniania. Przechowywane hasła muszą być chronione przed atakującymi, nawet jeśli aplikacja lub baza danych zostaną naruszone. Na szczęście większość współczesnych języków programowania i frameworków oferuje wbudowane funkcje ułatwiające bezpieczne przechowywanie haseł.

Jednak po uzyskaniu przez atakującego zapisanych haseł, zawsze jest on w stanie dokonać ataku siłowego w trybie offline. Osoby broniące się mogą spowolnić ataki offline, wybierając algorytmy haszujące, które wymagają jak największej ilości zasobów.

Podsumowując nasze rekomendacje:

- **Użyj [Argon2id](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) z minimalną konfiguracją 19 MiB pamięci, liczbą iteracji równą 2 i 1 stopniem paralelizmu.**
- **Jeśli [Argon2id](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) nie jest dostępny, należy użyć [scrypt](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) z minimalnym parametrem kosztu procesora/pamięci równym (2^17), minimalnym rozmiarem bloku równym 8 (1024 bajty) i parametrem paralelizacji równym 1.**
- **W przypadku starszych systemów wykorzystujących [bcrypt](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) należy użyć współczynnika pracy wynoszącego 10 lub więcej i limitu długości hasła wynoszącego 72 bajty.**
- **Jeżeli wymagana jest zgodność ze standardem FIPS-140, należy użyć [PBKDF2](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) ze współczynnikiem pracy wynoszącym 600 000 lub więcej i ustawić go przy użyciu wewnętrznej funkcji skrótu HMAC-SHA-256.**
- **Warto rozważyć użycie [pieprzu](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) , aby zapewnić dodatkową, głęboką ochronę (choć sam pieprz nie zapewnia żadnych dodatkowych właściwości zabezpieczających).**

## Tło[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

### Hashowanie a szyfrowanie[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Haszowanie i szyfrowanie mogą chronić poufne dane, ale w większości przypadków **hasła powinny być haszowane, a NIE szyfrowane.**

Ponieważ **haszowanie jest funkcją jednokierunkową** (tj. nie da się „odszyfrować” hasha i uzyskać oryginalnej wartości w postaci tekstu jawnego), jest to najodpowiedniejsze podejście do walidacji hasła. Nawet jeśli atakujący uzyska zahaszowane hasło, nie będzie mógł go użyć, aby zalogować się jako ofiara.

Ponieważ **szyfrowanie jest funkcją dwukierunkową** , atakujący mogą odzyskać oryginalny tekst jawny z zaszyfrowanych danych. Można go wykorzystać do przechowywania danych, takich jak adres użytkownika, ponieważ dane te są wyświetlane w postaci tekstu jawnego w profilu użytkownika. Zahaszowanie adresu spowodowałoby powstanie nieczytelnego komunikatu.

Szyfrowanie haseł powinno być stosowane jedynie w sytuacjach skrajnych, gdy konieczne jest uzyskanie oryginalnego hasła w postaci jawnej. Może to być konieczne, gdy aplikacja musi użyć hasła do uwierzytelnienia w innym systemie, który nie obsługuje nowoczesnego sposobu programowego przyznawania dostępu, takiego jak OpenID Connect (OIDC). W miarę możliwości należy stosować architekturę alternatywną, aby uniknąć konieczności przechowywania haseł w postaci zaszyfrowanej.

Więcej wskazówek na temat szyfrowania znajdziesz w [ściągawce dotyczącej przechowywania kryptograficznego](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) .

### Kiedy hasze haseł można złamać[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

**Silne hasła przechowywane z wykorzystaniem nowoczesnych algorytmów haszujących i najlepszych praktyk haszowania powinny być praktycznie niemożliwe do złamania przez atakującego.** Jako właściciel aplikacji jesteś odpowiedzialny za wybór nowoczesnego algorytmu haszującego.

Istnieją jednak sytuacje, w których atakujący może „złamać” skróty w pewnych okolicznościach, wykonując następujące czynności:

- Wybranie hasła, które Twoim zdaniem wybrała ofiara (np. `password1!`)
- Obliczanie skrótu
- Porównujesz obliczony hash z hashem ofiary. Jeśli są one zgodne, poprawnie „złamałeś” hash i znasz teraz wartość jawnego tekstu jej hasła.

Zazwyczaj atakujący powtarza ten proces, korzystając z listy zawierającej dużą liczbę potencjalnych haseł, takich jak:

- Listy haseł uzyskane z innych zainfekowanych witryn
- Siła brutalna (wypróbowanie każdego możliwego kandydata)
- Słowniki lub listy słów zawierające popularne hasła

Mimo że liczba permutacji może być ogromna, biorąc pod uwagę szybki sprzęt (taki jak procesory GPU) i usługi w chmurze z wieloma serwerami na wynajem, koszt skutecznego złamania hasła dla atakującego jest stosunkowo niewielki, zwłaszcza gdy nie są przestrzegane najlepsze praktyki dotyczące haszowania.

## Metody ulepszania przechowywania haseł[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

### Solenie[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Sól to unikalny, losowo generowany ciąg znaków, który jest dodawany do każdego hasła w ramach procesu haszowania. Ponieważ sól jest unikalna dla każdego użytkownika, atakujący musi łamać hasze pojedynczo, używając odpowiedniej soli, zamiast obliczać hasz jednorazowo i porównywać go z każdym zapisanym haszem. To znacznie utrudnia łamanie dużej liczby haszy, ponieważ wymagany czas rośnie proporcjonalnie do liczby haszy.

Salting chroni również przed wstępnym obliczeniem haszy przez atakującego za pomocą tablic tęczowych lub wyszukiwań w bazie danych. Salting oznacza również, że nie da się ustalić, czy dwaj użytkownicy mają to samo hasło bez złamania haszy, ponieważ różne saltingi dadzą różne hasze, nawet jeśli hasła są takie same.

Na poziomie algorytmu i specyfikacji, nowoczesne funkcje haszujące hasła, takie jak [Argon2id](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) , [bcrypt](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) i [PBKDF2](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) , wymagają od wywołującego podania soli. Jednak większość powszechnie używanych implementacji i bibliotek automatycznie generuje i zarządza solami wewnętrznie, więc programiści aplikacji zazwyczaj nie muszą ręcznie generować soli, jeśli poprawnie korzystają z tych bibliotek.

### Pieprzenie[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

[Peppering](https://datatracker.ietf.org/doc/html/draft-ietf-kitten-password-storage-07.2) to klasa strategii, które można stosować oprócz saltingu, aby zapewnić dodatkową warstwę ochrony. Uniemożliwiają one atakującemu złamanie któregokolwiek z haszy, jeśli ma on dostęp tylko do bazy danych, na przykład jeśli wykorzystał lukę w zabezpieczeniach SQL Injection lub uzyskał kopię zapasową bazy danych.

#### Wspólne wymagania dotyczące strategii pieprzenia[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

- „Pepper” jest **współdzielony przez wiele przechowywanych haseł** , a nie jest _unikalny_ dla pojedynczego hasła, jak w przypadku „soli” hasła.
- W przeciwieństwie do hasła „sól”, „pieprz” nie powinien być publiczny i **nie powinien być przechowywany razem z wygenerowanym hashem** . „Pieprz” powinien być przechowywany oddzielnie od bazy danych haseł.
- Papryczki to sekrety i powinny być przechowywane w „skarbcach sekretów” lub modułach HSM (sprzętowych modułach bezpieczeństwa). Więcej informacji na temat bezpiecznego przechowywania sekretów można znaleźć [w ściągawce „Zarządzanie sekretami” .](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- W przypadku naruszenia hasła peppera, konieczne będzie jego wymienienie. Pepperów nie można zmienić bez znajomości hasła użytkownika. Dlatego zmiana peppera będzie wymagała wymuszenia na wszystkich użytkownikach, których hasła były chronione przez poprzednie hasło peppera, zresetowania haseł.

#### Wstępne mieszanie papryki[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

W tej strategii do hasła dodaje się „pieprz” przed jego hashowaniem przez algorytm haszujący. Obliczony skrót jest następnie zapisywany w bazie danych. W tym przypadku „pieprz” powinien być wartością losową wygenerowaną w bezpieczny sposób. Więcej informacji na temat bezpiecznego generowania wartości losowych można znaleźć w dokumencie [Cryptographic_Storage_Cheat_Sheet .](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

#### Papryczki po haszowaniu[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

W tej strategii hasło jest haszowane jak zwykle za pomocą algorytmu haszującego. Uzyskany hasz jest następnie haszowany ponownie za pomocą algorytmu HMAC (np. HMAC-SHA256, HMAC-SHA512, w zależności od pożądanej długości danych wyjściowych) przed zapisaniem go w bazie danych. W tym przypadku klucz HMAC pełni rolę klucza HMAC i powinien zostać wygenerowany zgodnie z wymaganiami algorytmu HMAC.

### Korzystanie z czynników pracy[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Współczynnik pracy to liczba iteracji algorytmu haszującego wykonywanych dla każdego hasła (zazwyczaj jest to `2^work`liczba iteracji). Współczynnik pracy jest zazwyczaj przechowywany w danych wyjściowych hasha. Powoduje to, że obliczenie hasha jest bardziej kosztowne obliczeniowo, co z kolei zmniejsza szybkość i/lub zwiększa koszt, jaki atakujący może ponieść, próbując złamać hash hasła.

Wybierając współczynnik pracy, należy zachować równowagę między bezpieczeństwem a wydajnością. Chociaż wyższe współczynniki pracy utrudniają atakującemu złamanie haszy, spowalniają one proces weryfikacji próby logowania. Zbyt wysoki współczynnik pracy może obniżyć wydajność aplikacji, co może zostać wykorzystane przez atakującego do przeprowadzenia ataku typu DoS (DoS) poprzez obciążenie procesora serwera dużą liczbą prób logowania.

Nie ma złotej reguły na idealny współczynnik pracy – będzie on zależał od wydajności serwera i liczby użytkowników aplikacji. Określenie optymalnego współczynnika pracy będzie wymagało eksperymentów na konkretnych serwerach używanych przez aplikację. Zasadniczo obliczenie skrótu powinno zająć mniej niż sekundę.

#### Podnoszenie współczynnika pracy[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Jedną z głównych zalet posiadania współczynnika pracy jest to, że można go zwiększać z czasem, w miarę jak sprzęt staje się wydajniejszy i tańszy.

Najczęstszym sposobem aktualizacji współczynnika pracy jest oczekiwanie na kolejne uwierzytelnienie użytkownika, a następnie ponowne hashowanie hasła z nowym współczynnikiem pracy. Różne skróty będą miały różne współczynniki pracy, a skróty mogą nigdy nie zostać zaktualizowane, jeśli użytkownik nie zaloguje się ponownie do aplikacji. W zależności od aplikacji, zasadne może być usunięcie starszych skrótów haseł i wymaganie od użytkowników resetowania haseł przy następnym logowaniu, aby uniknąć przechowywania starszych i mniej bezpiecznych skrótów.

## Algorytmy haszujące hasła[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Niektóre współczesne algorytmy haszujące zostały zaprojektowane specjalnie z myślą o bezpiecznym przechowywaniu haseł. Oznacza to, że powinny być wolne (w przeciwieństwie do algorytmów takich jak MD5 i SHA-1, które zostały zaprojektowane z myślą o szybkości), a ich szybkość można regulować, zmieniając współczynnik pracy.

Nie musisz ukrywać, który algorytm haszowania haseł jest używany przez aplikację. Jeśli korzystasz z nowoczesnego algorytmu haszowania haseł z odpowiednimi parametrami konfiguracyjnymi, powinieneś móc publicznie ujawnić, które algorytmy haszowania haseł są używane i umieścić je [tutaj](https://pulse.michalspacek.cz/passwords/storages) .

Wybierając algorytm haszowania hasła, programiści powinni preferować nowoczesne algorytmy, które są odporne zarówno na ataki oparte na GPU, jak i na atakach opartych na pamięci. Jeśli to możliwe, nowsze algorytmy powinny być wybierane do nowych aplikacji, podczas gdy starsze algorytmy mogą być nadal akceptowalne dla starszych systemów przy odpowiedniej konfiguracji.

Trzy algorytmy haszujące, które warto wziąć pod uwagę.

### Argon2id[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

[Argon2](https://en.wikipedia.org/wiki/Argon2) zwyciężył w [konkursie haszowania haseł](https://en.wikipedia.org/wiki/Password_Hashing_Competition) w 2015 roku . Spośród trzech wersji Argon2, wybierz wariant Argon2id, ponieważ zapewnia on zrównoważone podejście do przeciwdziałania atakom zarówno z wykorzystaniem kanału bocznego, jak i opartym na GPU.

Zamiast prostego współczynnika pracy, jak w innych algorytmach, Argon2id oferuje trzy różne parametry, które można skonfigurować: minimum bazowe minimalnego rozmiaru pamięci (m), minimalną liczbę iteracji (t) oraz stopień paralelizmu (p). Zalecamy następujące ustawienia konfiguracji:

Parametry te kontrolują koszt obliczeniowy obliczenia skrótu hasła. Zwiększone wykorzystanie pamięci, liczba iteracji lub paralelizm znacznie spowalniają i zwiększają koszty łamania haseł dla atakujących, a jednocześnie, po odpowiednim dostrojeniu, pozostają praktyczne w przypadku uzasadnionych żądań uwierzytelnienia.

- m=47104 (46 MiB), t=1, p=1 (Nie stosować z Argon2i)
- m=19456 (19 MiB), t=2, p=1 (Nie stosować z Argon2i)
- m=12288 (12 MiB), t=3, p=1
- m=9216 (9 MiB), t=4, p=1
- m=7168 (7 MiB), t=5, p=1

Te ustawienia konfiguracji zapewniają równy poziom ochrony, a jedyną różnicą jest kompromis pomiędzy wykorzystaniem procesora i pamięci RAM.

### skrypt[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

[scrypt](http://www.tarsnap.com/scrypt/scrypt.pdf) to funkcja wyprowadzania kluczy oparta na hasłach, stworzona przez [Colina Percivala](https://twitter.com/cperciva) . Chociaż [Argon2id](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) powinien być najlepszym wyborem do hashowania haseł, [scrypt](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) powinien być używany, gdy ten pierwszy jest niedostępny.

Podobnie jak [Argon2id](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) , scrypt ma trzy parametry, które można skonfigurować: minimalny koszt pamięci (N), rozmiar bloku (r) i stopień paralelizmu (p). Użyj jednego z następujących ustawień:

- N=2^17 (128 MiB), r=8 (1024 bajtów), p=1
- N=2^16 (64 MiB), r=8 (1024 bajtów), p=2
- N=2^15 (32 MiB), r=8 (1024 bajtów), p=3
- N=2^14 (16 MiB), r=8 (1024 bajtów), p=5
- N=2^13 (8 MiB), r=8 (1024 bajtów), p=10

Te ustawienia konfiguracji zapewniają podobny minimalny poziom ochrony, przy czym głównym kompromisem jest paralelizm i wykorzystanie pamięci RAM.

### bcrypt[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Funkcja haszująca hasła bcrypt **powinna być używana wyłącznie** do przechowywania haseł w starszych systemach, w których nie są dostępne Argon2 i scrypt [.](https://en.wikipedia.org/wiki/bcrypt)

Współczynnik pracy powinien być tak duży, jak pozwala na to wydajność serwera weryfikacyjnego, przy czym minimalna wartość powinna wynosić 10.

#### Limity wejściowe bcrypt[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Maksymalna długość danych wejściowych [w większości implementacji](https://security.stackexchange.com/questions/39849/does-bcrypt-have-a-maximum-password-length) bcrypt wynosi 72 bajty , dlatego należy wymusić maksymalną długość hasła wynoszącą 72 bajty (lub mniej, jeśli implementacja bcrypt ma mniejsze ograniczenia).

#### Wstępne hashowanie haseł za pomocą bcrypt[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Alternatywnym podejściem jest wstępne hashowanie hasła podanego przez użytkownika za pomocą szybkiego algorytmu, takiego jak SHA-2, HMAC lub BLAKE3, a następnie hashowanie otrzymanej wartości skrótu za pomocą bcrypt (tj. `bcrypt(H($password)), $salt, $cost)`). Może to być **niebezpieczne** ze względu na bajty zerowe w wartości wyjściowej skrótu oraz z powodu [zmiany hasła](https://www.youtube.com/watch?v=OQD3qDYMyYQ) .

Oryginalny bcrypt oczekuje ciągu hasła zakończonego zerem, co oznacza, że ​​wartość skrótu będzie używana tylko do pierwszego bajtu zerowego w wartości skrótu. ( `bcrypt(H($password)), $salt, $cost) == bcrypt("", $salt, $cost)`jeśli `H($password)[0] == 0`) Zwiększa to szansę znalezienia kolizji podczas [łączenia bcrypt z innymi funkcjami skrótu](https://blog.ircmaxell.com/2015/03/security-issue-combining-bcrypt-with.html) i ​​można tego uniknąć, kodując wartość skrótu w drukowalnym ciągu za pomocą czegoś takiego jak base64. Base64 może zwiększyć długość wartości skrótu powyżej 72 znaków, więc występuje niewielkie obcięcie dużych wartości skrótu z skrótów takich jak SHA-512, jest to [nieistotne](https://soatok.blog/2024/11/27/beyond-bcrypt/) .

Zmienianie haseł wykorzystuje fakt, że łatwo sprawdzić, czy `bcrypt(base64(H($password))), $salt, $cost) == bcrypt(base64($leaked_hash), $salt, $cost)`… Jeśli wewnętrzna funkcja skrótu `H`jest używana z tym samym hasłem gdzie indziej i jest znana atakującemu, złamanie hasła można sprowadzić do złamania funkcji skrótu `H`. Samo użycie czystego algorytmu SHA-512 (tj.… `bcrypt(base64(sha512($password))), $salt, $cost)`) jest **niebezpieczną praktyką** i jest tak samo bezpieczne, jak użycie czystego algorytmu SHA-512. Zmienianie haseł działa tylko wtedy, gdy atakujący zna wyciek hasha, czy to z bazy danych, czy z tabel tęczowych. Aby złagodzić skutki zmieniania haseł, można użyć… [pieprzu .](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

Podsumowując, jeśli konieczne jest użycie bcrypt i hasło ma być wstępnie zaszyfrowane, należy to zrobić `bcrypt(base64(hmac-sha384(data:$password, key:$pepper)), $salt, $cost)`i zapisać pepper, a nie w bazie danych.

### PBKDF2[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Ponieważ [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) jest zalecany przez [NIST](https://pages.nist.gov/800-63-3/sp800-63b.html) i ma implementacje zatwierdzone przez FIPS-140, powinien być preferowanym algorytmem, gdy jest to wymagane.

Algorytm PBKDF2 wymaga wybrania wewnętrznego algorytmu haszującego, takiego jak HMAC lub jeden z wielu innych algorytmów haszujących. HMAC-SHA-256 jest powszechnie obsługiwany i zalecany przez NIST.

Współczynnik pracy dla PBKDF2 jest implementowany za pomocą liczby iteracji, która powinna być ustawiana inaczej w zależności od użytego wewnętrznego algorytmu haszującego.

- PBKDF2-HMAC-SHA1: 1 300 000 iteracji
- PBKDF2-HMAC-SHA256: 600 000 iteracji
- PBKDF2-HMAC-SHA512: 210 000 iteracji

### Równoległy PBKDF2[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

- PPBKDF2-SHA512: koszt 2
- PPBKDF2-SHA256: koszt 5
- PPBKDF2-SHA1: koszt 10

Te ustawienia konfiguracji są równoważne pod względem zapewnianej ochrony. ( [Dane z grudnia 2022 r., oparte na testach kart graficznych RTX 4000](https://tobtu.com/minimum-password-settings/) )

#### PBKDF2 Pre-Hashowanie[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Gdy PBKDF2 jest używany z algorytmem HMAC, a hasło jest dłuższe niż rozmiar bloku funkcji skrótu (64 bajty dla SHA-256), hasło zostanie automatycznie wstępnie zahaszowane. Na przykład hasło „To jest hasło dłuższe niż 512 bitów, co odpowiada rozmiarowi bloku SHA-256” jest konwertowane na wartość skrótu (w formacie szesnastkowym): `fa91498c139805af73f7ba275cca071e78d78675027000c99a9925e2ec92eedd`.

Dobre implementacje PBKDF2 wykonują wstępne hashowanie przed kosztowną, iterowaną fazą hashowania. Jednak niektóre implementacje wykonują konwersję w każdej iteracji, co może sprawić, że hashowanie długich haseł będzie znacznie droższe niż hashowanie krótkich haseł. Gdy użytkownicy podają bardzo długie hasła, może wystąpić potencjalna luka w zabezpieczeniach typu „odmowa usługi”, taka jak ta opublikowana w [Django](https://www.djangoproject.com/weblog/2013/sep/15/security/) w 2013 roku. Ręczne wstępne hashowanie może zmniejszyć to ryzyko, ale wymaga dodania [soli](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) do etapu wstępnego hashowania.

## Aktualizowanie starszych skrótów[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Starsze aplikacje, które korzystają z mniej bezpiecznych algorytmów haszujących, takich jak MD5 lub SHA-1, można zaktualizować do nowoczesnych algorytmów haszujących hasła, jak opisano powyżej. Gdy użytkownicy wpisują swoje hasło (zazwyczaj uwierzytelniając się w aplikacji), dane te powinny zostać ponownie zahaszowane przy użyciu nowego algorytmu. Obrońcy powinni unieważnić bieżące hasło użytkownika i zażądać od niego wprowadzenia nowego, tak aby wszelkie starsze (mniej bezpieczne) hasze hasła nie były już przydatne dla atakującego.

Oznacza to jednak, że stare (mniej bezpieczne) skróty haseł będą przechowywane w bazie danych do momentu zalogowania użytkownika. Aby uniknąć tego dylematu, można zastosować jedno z dwóch podejść.

Pierwsza metoda aktualizacji: Wygaś i usuń skróty haseł użytkowników, którzy byli nieaktywni przez dłuższy czas, i wymagaj od nich zresetowania haseł, aby się ponownie zalogować. Chociaż to podejście jest bezpieczne, nie jest szczególnie przyjazne dla użytkownika. Wygaśnięcie haseł wielu użytkowników może powodować problemy dla personelu wsparcia lub być interpretowane przez użytkowników jako oznaka naruszenia bezpieczeństwa.

Metoda aktualizacji nr 2: Użyj istniejących skrótów haseł jako danych wejściowych dla bezpieczniejszego algorytmu. Na przykład, jeśli aplikacja pierwotnie zapisywała hasła w formacie `md5($password)`, można je łatwo zaktualizować do `bcrypt(md5($password))`. Nakładanie skrótów eliminuje konieczność znajomości oryginalnego hasła, jednak może ułatwić ich złamanie. Te skróty należy zastąpić bezpośrednimi skrótami haseł użytkowników przy następnym logowaniu.

Pamiętaj, że po wybraniu metody haszowania hasła, będzie ona wymagała aktualizacji w przyszłości, dlatego zadbaj o to, aby aktualizacja algorytmu haszującego była jak najłatwiejsza. W okresie przejściowym należy zezwolić na mieszankę starych i nowych algorytmów haszujących. Korzystanie z kombinacji algorytmów haszujących jest łatwiejsze, jeśli algorytm haszujący hasło i współczynnik pracy są przechowywane razem z hasłem w standardowym formacie, na przykład w [modularnym formacie ciągu PHC](https://github.com/P-H-C/phc-string-format/blob/master/phc-sf-spec.md) .

### Znaki międzynarodowe[¶](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html "Stały link")

Twoja biblioteka haszująca musi akceptować szeroki zakres znaków i być kompatybilna ze wszystkimi kodami Unicode, aby użytkownicy mogli korzystać z pełnego zakresu znaków dostępnych na nowoczesnych urządzeniach – zwłaszcza klawiaturach mobilnych. Powinny one umożliwiać wybór haseł z różnych języków i uwzględniać piktogramy. Przed haszowaniem entropia wpisu użytkownika nie powinna być zmniejszona, a biblioteki haszujące hasła muszą obsługiwać dane wejściowe, które mogą zawierać bajt NULL.

### Kryptografia i dane
W tym zadaniu chcielibyśmy zbadać, co się dzieje, gdy logujemy się do witryny internetowej za pomocą protokołu HTTPS.

1. Klient żąda certyfikatu SSL/ TLS serwera
2. Serwer wysyła certyfikat SSL/ TLS do klienta
3. Klient potwierdza ważność certyfikatu

Rola kryptografii zaczyna się od sprawdzenia certyfikatu. Aby certyfikat był uznany za ważny, musi być podpisany. Podpisanie oznacza, że ​​skrót certyfikatu jest szyfrowany kluczem prywatnym zaufanej osoby trzeciej; zaszyfrowany skrót jest dołączany do certyfikatu.

Jeśli strona trzecia jest zaufana, klient użyje jej klucza publicznego do odszyfrowania zaszyfrowanego skrótu i ​​porównania go ze skrótem certyfikatu. Jeśli jednak strona trzecia nie zostanie rozpoznana, połączenie nie zostanie nawiązane automatycznie.

Gdy klient potwierdzi ważność certyfikatu, rozpoczyna się uzgadnianie SSL/ TLS . Pozwala ono klientowi i serwerowi uzgodnić między innymi klucz tajny i algorytm szyfrowania symetrycznego. Od tego momentu cała komunikacja w ramach sesji będzie szyfrowana za pomocą szyfrowania symetrycznego.

Ostatnim krokiem jest podanie danych logowania. Klient przesyła je na serwer za pomocą szyfrowanej sesji SSL/ TLS . Serwer otrzymuje nazwę użytkownika i hasło i musi potwierdzić ich zgodność.

Zgodnie z wytycznymi bezpieczeństwa, oczekujemy, że serwer zapisze zahaszowaną wersję hasła po dodaniu do niej losowej soli. W ten sposób, w przypadku włamania do bazy danych, hasła będą trudne do odzyskania.
