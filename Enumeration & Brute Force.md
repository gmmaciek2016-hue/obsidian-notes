### Wstęp

Enumeracja uwierzytelniania jest fundamentalnym aspektem testowania bezpieczeństwa, koncentrującym się w szczególności na mechanizmach chroniących wrażliwe aspekty aplikacji internetowych. Proces ten obejmuje metodyczną inspekcję różnych komponentów uwierzytelniania, od walidacji nazw użytkowników, przez polityki haseł, po zarządzanie sesjami. Każdy z tych elementów jest skrupulatnie testowany, ponieważ reprezentuje potencjalne luki w zabezpieczeniach, które w przypadku wykorzystania mogą doprowadzić do poważnych naruszeń bezpieczeństwa.  

### Cele

Pod koniec tego pokoju będziesz:

1. Zrozum znaczenie enumeracji i w jaki sposób przygotowuje ona grunt pod skuteczne ataki siłowe.
2. Poznaj zaawansowane metody wyliczeń, skupiające się głównie na wyodrębnianiu informacji z rozbudowanych komunikatów o błędach.
3. Zrozumieć związek między wyliczaniem a atakami siłowymi w celu złamania mechanizmów uwierzytelniania.
4. Zdobądź praktyczne doświadczenie w stosowaniu narzędzi i technik zarówno do ataków wyliczeniowych, jak i siłowych.

### Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś mieć podstawową wiedzę na temat następujących pojęć:

1. Znajomość z HTTPi HTTPS, w tym struktury żądanie/odpowiedź i typowe kody statusu.
2. Doświadczenie w korzystaniu z narzędzi takich jak[Burp Suite](https://tryhackme.com/module/learn-burp-suite).
3. Podstawowa umiejętność nawigacji i korzystania z[Linuxwiersz poleceń](https://tryhackme.com/module/linux-fundamentals) .

Odpowiedz na poniższe pytania

Wdróż docelową maszynę wirtualną dołączoną do tego zadania, naciskając zielony przycisk „Start Lab Machine”. Po uzyskaniu wygenerowanego adresu IP maszyny możesz użyć AttackBoxa lub własnej maszyny wirtualnej podłączonej do sieci VPN TryHackMe.  
  
Dodaj **parametr MACHINE_IP** do pliku **/etc/hosts** . Na przykład:  

/etc/hosts

```shell-session
MACHINE_IP    enum.thm
```

Po 3 minutach odwiedź stronę **http://enum.thm** , aby uzyskać dostęp do maszyny. Zalecamy użycie AttackBox w tym pokoju.

### Wyliczenie uwierzytelniania

![Ikona odcisku palca](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719928726091.png)

Wyobraź sobie siebie jako cyfrowego detektywa. Nie chodzi tylko o zbieranie wskazówek, ale o zrozumienie, co one ujawniają na temat bezpieczeństwa systemu. Właśnie na tym polega enumeracja uwierzytelniania. To jak układanie puzzli, a nie tylko odhaczanie pozycji na liście kontrolnej.

Enumeracja uwierzytelniania przypomina obieranie cebuli z kolejnych warstw. Usuwasz każdą warstwę zabezpieczeń systemu, aby odsłonić rzeczywiste operacje pod spodem. Nie chodzi tylko o rutynowe kontrole, ale o sprawdzenie, jak wszystko jest ze sobą powiązane.

**Identyfikacja prawidłowych nazw użytkowników**

Znajomość prawidłowej nazwy użytkownika pozwala atakującemu skupić się wyłącznie na haśle. Nazwy użytkowników można poznać na różne sposoby, na przykład obserwując reakcję aplikacji podczas logowania lub resetowania hasła. Na przykład komunikaty o błędach informujące o tym, że „to konto nie istnieje” lub „nieprawidłowe hasło” mogą wskazywać na prawidłowe nazwy użytkowników, ułatwiając atakującemu zadanie.

**Zasady dotyczące haseł**

Wytyczne dotyczące tworzenia haseł mogą dostarczyć cennych informacji na temat złożoności haseł używanych w aplikacji. Rozumiejąc te zasady, atakujący może ocenić potencjalną złożoność haseł i odpowiednio dostosować swoją strategię. Na przykład poniżej PHP kod używa wyrażenia regularnego, aby wymagać hasła zawierającego symbole, cyfry i wielkie litery:

```php
<?php
$password = $_POST['pass']; // Example1
$pattern = '/^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$/';

if (preg_match($pattern, $password)) {
    echo "Password is valid.";
} else {
    echo "Password is invalid. It must contain at least one uppercase letter, one number, and one symbol.";
}
?>
```

W powyższym przykładzie, jeśli podane hasło nie spełnia zasad zdefiniowanych w zmiennej **wzorca** , aplikacja zwróci komunikat o błędzie ujawniający wymóg dotyczący kodu wyrażenia regularnego. Atakujący może wygenerować słownik spełniający te zasady.

### Typowe miejsca do wyliczenia

Aplikacje internetowe oferują mnóstwo funkcji ułatwiających życie użytkownikom, ale mogą też narazić ich na ryzyko:

**Strony rejestracyjne**

Aplikacje internetowe zazwyczaj upraszczają proces rejestracji użytkownika i dostarczają mu informacji, natychmiast informując, czy adres e-mail lub nazwa użytkownika są dostępne. Chociaż ta informacja zwrotna ma na celu poprawę komfortu użytkowania, może nieumyślnie pełnić podwójną funkcję. Jeśli próba rejestracji zakończy się komunikatem informującym, że nazwa użytkownika lub adres e-mail są już zajęte, aplikacja nieświadomie potwierdza ich istnienie każdemu, kto próbuje się zarejestrować. Atakujący wykorzystują tę funkcję, testując potencjalne nazwy użytkowników lub adresy e-mail, tworząc w ten sposób listę aktywnych użytkowników bez konieczności bezpośredniego dostępu do bazy danych.

**Funkcje resetowania hasła**

Mechanizmy resetowania hasła mają na celu pomóc użytkownikom odzyskać dostęp do swoich kont poprzez wprowadzenie danych w celu otrzymania instrukcji resetowania. Jednak różnice w odpowiedzi aplikacji mogą nieumyślnie ujawnić poufne informacje. Na przykład, różnice w odpowiedzi aplikacji dotyczącej istnienia nazwy użytkownika mogą pomóc atakującym w weryfikacji tożsamości użytkowników. Analizując te odpowiedzi, atakujący mogą udoskonalić swoje listy prawidłowych nazw użytkowników, znacznie zwiększając skuteczność kolejnych ataków.

**Błędy szczegółowe**

Rozwlekłe komunikaty o błędach podczas prób logowania lub innych procesów interaktywnych mogą ujawnić zbyt wiele. Rozróżnienie między komunikatami „nie znaleziono nazwy użytkownika” a „nieprawidłowe hasło” ma pomóc użytkownikom zrozumieć problemy z logowaniem. Dostarczają one jednak atakującym jednoznacznych wskazówek dotyczących prawidłowych nazw użytkowników, co może zostać wykorzystane do bardziej ukierunkowanych ataków.

**Informacje o naruszeniu danych**

Dane z poprzednich naruszeń bezpieczeństwa to prawdziwa kopalnia złota dla atakujących, ponieważ pozwalają im sprawdzić, czy skradzione nazwy użytkowników i hasła są ponownie wykorzystywane na różnych platformach. Jeśli atakujący znajdzie pasującą nazwę, sugeruje to nie tylko ponowne wykorzystanie nazwy użytkownika, ale także potencjalne ponowne wykorzystanie haseł, zwłaszcza jeśli platforma była już wcześniej atakowana. Ta technika pokazuje, jak skutki pojedynczego naruszenia bezpieczeństwa danych mogą rozprzestrzenić się na wiele platform, wykorzystując powiązania między różnymi tożsamościami online.

### Zrozumienie błędów opisowych

![Ikona mapy](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719928819961.png)

Wyobraź sobie, że jesteś detektywem z talentem do dostrzegania wskazówek, które inni mogliby przeoczyć. W świecie tworzenia stron internetowych, rozwlekłe błędy są jak niezamierzone szepty systemu, ujawniające sekrety, które miały pozostać ukryte. Te szczegółowe komunikaty o błędach są nieocenione w procesie debugowania, pomagając programistom dokładnie zrozumieć, co poszło nie tak. Jednak tak jak podsłuchana rozmowa może ujawnić zbyt wiele, tak te rozwlekłe błędy mogą nieumyślnie ujawnić poufne dane tym, którzy potrafią słuchać.

Wieloznaczne błędy mogą stać się kopalnią informacji, dostarczając takich spostrzeżeń, jak:

- **Ścieżki wewnętrzne** : Przypominają mapę prowadzącą do ukrytego skarbu i ujawniają ścieżki plików oraz strukturę katalogów serwera aplikacji, które mogą zawierać pliki konfiguracyjne lub klucze tajne niewidoczne dla zwykłego użytkownika.
- **Szczegóły bazy danych** : błędy te umożliwiają wgląd w bazę danych i mogą ujawnić takie tajemnice, jak nazwy tabel i szczegóły kolumn.
- **Informacje o użytkowniku** : Czasami błędy te mogą nawet wskazywać na nazwy użytkowników i inne dane osobowe, dostarczając wskazówek kluczowych dla dalszego dochodzenia.

### Wywoływanie błędów werbalnych

Atakujący wywołują błędy verbose, aby zmusić aplikację do ujawnienia swoich sekretów. Poniżej przedstawiono kilka typowych technik stosowanych do wywoływania tych błędów:

1. **Nieprawidłowe próby logowania** : To jak pukanie do każdych drzwi, aby sprawdzić, które się otworzą. Celowo wprowadzając nieprawidłowe nazwy użytkownika lub hasła, atakujący mogą wywołać komunikaty o błędach, które pomogą odróżnić prawidłowe nazwy użytkowników od nieprawidłowych. Na przykład, wprowadzenie nieistniejącej nazwy użytkownika może wywołać inny komunikat o błędzie niż wprowadzenie istniejącej, ujawniając, które nazwy użytkowników są aktywne.
    
2. **SQL injection : Ta technika polega na wsunięciu złośliwych poleceń SQL do pól wprowadzania danych, licząc na to, że system natknie się na nie i ujawni informacje o strukturze swojej bazy danych. Na przykład, umieszczenie pojedynczego cudzysłowu ( `'`) w polu logowania może spowodować błąd bazy danych, nieumyślnie ujawniając szczegóły dotyczące jej schematu.
    
3. **Dołączanie plików/Przemierzanie ścieżek** : Manipulując ścieżkami plików, atakujący mogą próbować uzyskać dostęp do plików objętych ograniczeniami, nakłaniając system do błędów ujawniających ścieżki wewnętrzne. Na przykład, użycie sekwencji przemierzania katalogów, takich jak , `../../`może prowadzić do błędów ujawniających ścieżki do plików objętych ograniczeniami.
    
4. **Manipulacja formularzami** : Modyfikowanie pól lub parametrów formularza może oszukać aplikację i spowodować wyświetlanie błędów, które ujawniają logikę zaplecza lub poufne informacje o użytkowniku. Na przykład, filtrowanie ukrytych pól formularza w celu wywołania błędów walidacji może ujawnić informacje na temat oczekiwanego formatu lub struktury danych.
    
5. **Rozmycie aplikacji** : Wysyłanie nieoczekiwanych danych wejściowych do różnych części aplikacji w celu sprawdzenia ich reakcji może pomóc w identyfikacji słabych punktów. Na przykład narzędzia takie jak Burp Suite Intruder służą do automatyzacji procesu, bombardując aplikację zróżnicowanymi ładunkami, aby sprawdzić, które z nich powodują błędy informacyjne.

### Rola enumeracji i brutalnego wymuszania

Jeśli chodzi o łamanie uwierzytelniania, enumeracja i atak siłowy często idą ręka w rękę:

- **Wyliczanie użytkowników** : Odkrycie prawidłowych nazw użytkowników tworzy podwaliny, redukując konieczność zgadywania w późniejszych atakach siłowych.
- **Wykorzystywanie błędów opisowych** : Informacje uzyskane na podstawie tych błędów mogą rzucić światło na takie kwestie, jak polityka haseł i mechanizmy blokowania kont, torując drogę skuteczniejszym strategiom siłowym.

Podsumowując, błędy opisowe działają jak ścieżki prowadzące atakujących głębiej w system, dostarczając im informacji niezbędnych do dostosowania strategii i potencjalnego naruszenia bezpieczeństwa w sposób, który mógłby pozostać niezauważony, aż do momentu, gdy będzie za późno.

### Wyliczanie w formularzach uwierzytelniania

W tym [raporcie HackerOne(otwiera się w nowej karcie)](https://hackerone.com/reports/1166054)Atakujący był w stanie enumerować użytkowników za pomocą funkcji „Zapomnij hasło” na stronie internetowej. Podobnie możemy enumerować adresy e-mail w formularzach logowania. Na przykład, przejdź do  [http://enum.thm/labs/verbose_login/(otwiera się w nowej karcie)](http://enum.thm/labs/verbose_login/)[(otwiera się w nowej karcie)](http://enum.thm/labs/verbose_login/) i wpisz dowolny adres e-mail w polu wprowadzania adresu e-mail.

Jeśli podasz nieprawidłowy adres e-mail, na stronie pojawi się komunikat: „Adres e-mail nie istnieje”, co oznacza, że ​​podany adres e-mail nie został jeszcze zarejestrowany.

![Komunikat o błędzie „E-mail nie istnieje”](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1718887845395)

Jeśli jednak adres e-mail jest już zarejestrowany, witryna odpowie komunikatem o błędzie „Nieprawidłowe hasło”. Oznacza to, że adres e-mail istnieje w bazie danych, ale hasło jest niepoprawne.

![Komunikat o błędzie nieprawidłowego hasła](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1718887844791)

### Automatyzacja

Poniżej znajduje się skrypt w Pythonie, który sprawdzi poprawność adresów e-mail w docelowej aplikacji internetowej. Zapisz poniższy kod jako **script.py** .

```python
import requests
import sys

def check_email(email):
    url = 'http://enum.thm/labs/verbose_login/functions.php'  # Location of the login function
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
        'Referer': 'http://enum.thm/labs/verbose_login/',
    }
    data = {
        'username': email,
        'password': 'password',  # Use a random password as we are only checking the email
        'function': 'login'
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def enumerate_emails(email_file):
    valid_emails = []
    invalid_error = "Email does not exist"  # Error message for invalid emails

    with open(email_file, 'r') as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()  # Remove any leading/trailing whitespace
        if email:
            response_json = check_email(email)
            if response_json['status'] == 'error' and invalid_error in response_json['message']:
                print(f"[INVALID] {email}")
            else:
                print(f"[VALID] {email}")
                valid_emails.append(email)

    return valid_emails

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <email_list_file>")
        sys.exit(1)

    email_file = sys.argv[1]

    valid_emails = enumerate_emails(email_file)

    print("\nValid emails found:")
    for valid_email in valid_emails:
        print(valid_email)
```

**Kliknij tutaj, aby zapoznać się ze szczegółowym opisem skryptu.**

**Importy** :

- **żądania** : Biblioteka Pythona do tworzeniaHTTPżądania. Służy do interakcji z serwerem WWW poprzez wysyłanie żądań POST do punktu końcowego docelowego.
    
    ```python
    import requests
    ```

**Organizować coś** :

- **url** : Skrypt kieruje się do punktu końcowego obsługującego funkcjonalność logowania aplikacji.
    
    ```python
    url = 'http://enum.thm/labs/verbose_login/functions.php'
    ```
    
- **nagłówki** : Zbiór nagłówków HTTP jest definiowany w celu imitowania typowego żądania przeglądarki, zapewniając, że żądania wydają się uzasadnione.
    
    ```python
    headers = {
          'Host': 'enum.thm',
          'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest',
          'Origin': 'http://enum.thm',
          'Connection': 'close',
          'Referer': 'http://enum.thm/labs/verbose_login/',
      }
    ```

**Inicjalizacja zmiennych** :

- **valid_emails** : Tablica przechowuje adresy e-mail, których poprawność potwierdzono.
    
    ```python
    valid_emails = []
    ```
    
- **invalid_error** : ciąg zawierający konkretny komunikat o błędzie służący do identyfikacji nieprawidłowych adresów e-mail.
    
    ```python
    invalid_error = 'Email does not exist'
    ```

**Pętla główna** :

- Skrypt odczytuje adresy e-mail z dostarczonego pliku i sprawdza każdy z nich pod kątem poprawności, korzystając z `check_email`funkcji.
    
    ```python
    for email in email_list:
        check_email(email)
    ```

**Tworzenie i wysyłanie żądań HTTP** :

- Dla każdego e-maila skrypt konstruuje słownik danych, który zawiera adres e-mail, hasło zastępcze i polecenie wykonania funkcji „login”.
    
    ```python
    data = {'username': email, 'password': 'password', 'action': 'login'}
    response = requests.post(url, headers=headers, data=data)
    ```

**Obsługa odpowiedzi** :

- Odpowiedź serwera jest przetwarzana w celu sprawdzenia, czy podany adres e-mail istnieje, na podstawie obecności konkretnego komunikatu o błędzie w danych JSON.
    
    ```python
    if invalid_error in response.text:
        print(f"{email} is invalid.")
    else:
        print(f"{email} is valid.")
        valid_emails.append(email)
    ```

**Weryfikacja postaci** :

- Adresy e-mail, których istnienie zostało potwierdzone, są dodawane do `valid_emails`listy, a poprawność każdego adresu e-mail jest rejestrowana w konsoli.
    
    ```python
    for email in valid_emails:
        print(f"Valid email found: {email}")
    ```

Możemy użyć wspólnej listy adresów e-mail z tego [repozytorium(otwiera się w nowej karcie)](https://github.com/nyxgeek/username-lists/blob/master/usernames-top100/usernames_gmail.com.txt).

![Lista nazw użytkowników z githuba](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1720084910130.png)  

Po pobraniu listy ładunków sprawdź na AttackBoxie lub na swoim komputerze, czy podane adresy e-mail są prawidłowe.

**Uwaga:** Przypominamy, że zdecydowanie zalecamy użycie AttackBox do wykonania tego zadania.

skrypt.py

```shell-session
user@tryhackme $ python3 script.py usernames_gmail.com.txt
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[INVALID] xxxxxx@gmail.com
[VALID] xxxxxx@gmail.com
```

### Luki w zabezpieczeniach procesu resetowania hasła

Mechanizm resetowania hasła jest ważnym elementem wygody użytkownika w nowoczesnych aplikacjach internetowych. Jednak jego wdrożenie wymaga starannego rozważenia kwestii bezpieczeństwa, ponieważ słabo zabezpieczone procesy resetowania hasła mogą być łatwo wykorzystywane.

**Resetowanie za pomocą poczty e-mail**

Gdy użytkownik resetuje hasło, aplikacja wysyła wiadomość e-mail zawierającą link do resetowania lub token na zarejestrowany adres e-mail użytkownika. Użytkownik klika ten link, który przekierowuje go na stronę, gdzie może wprowadzić nowe hasło i je potwierdzić. Ewentualnie system automatycznie wygeneruje nowe hasło dla użytkownika. Ta metoda w dużej mierze opiera się na bezpieczeństwie konta e-mail użytkownika oraz poufności przesłanego linku lub tokena.

**Resetowanie na podstawie pytania bezpieczeństwa**

Polega ona na udzieleniu przez użytkownika odpowiedzi na serię wstępnie skonfigurowanych pytań bezpieczeństwa, które ustawił podczas tworzenia konta. Jeśli odpowiedzi są poprawne, system pozwala użytkownikowi na zresetowanie hasła. Chociaż ta metoda dodaje warstwę bezpieczeństwa, wymagając podania informacji, które powinien znać tylko użytkownik, może zostać naruszona, jeśli atakujący uzyska dostęp do danych osobowych (Informacje osobowe), które czasami można łatwo znaleźć lub odgadnąć.

**Resetowanie za pomocą SMS-ów**

Działa podobnie do resetowania hasła za pomocą wiadomości e-mail, ale wykorzystuje SMS-a do przesłania kodu resetowania lub linku bezpośrednio na telefon komórkowy użytkownika. Po otrzymaniu kodu użytkownik może go wprowadzić na podanej stronie internetowej, aby uzyskać dostęp do funkcji resetowania hasła. Ta metoda zakłada, że ​​dostęp do telefonu użytkownika jest bezpieczny, ale może być podatna na ataki typu SIM swapping lub przechwytywanie.

Każda z tych metod ma swoje słabe punkty:

- **Przewidywalne tokeny** : Jeśli tokeny resetowania używane w linkach lub wiadomościach SMS są przewidywalne lub podążają za sekwencyjnym wzorcem, atakujący mogą odgadnąć lub metodą siłową wygenerować prawidłowe adresy URL resetowania.
- **Problemy z wygasaniem tokenów** : Tokeny, które pozostają ważne zbyt długo lub nie wygasają natychmiast po użyciu, stwarzają okazję dla atakujących. Aby ograniczyć to okno, kluczowe jest, aby tokeny szybko wygasały.
- **Niewystarczająca walidacja** : Mechanizmy weryfikacji tożsamości użytkownika, takie jak pytania bezpieczeństwa lub uwierzytelnianie za pomocą poczty e-mail, mogą być słabe i podatne na ataki, jeśli pytania są zbyt częste lub konto e-mail zostanie naruszone.
- **Ujawnianie informacji** : Każdy komunikat o błędzie określający, czy adres e-mail lub nazwa użytkownika jest zarejestrowana, może nieumyślnie pomóc atakującym w wyliczaniu kont i potwierdzaniu ich istnienia.
- **Niezabezpieczony transport** : Przesyłanie łączy resetujących lub tokenów przez połączenia bez protokołu HTTPS może narazić te krytyczne elementy na przechwycenie przez podsłuchujących sieć.

### Wykorzystywanie przewidywalnych tokenów

Tokeny, które są proste, przewidywalne lub mają długi czas wygaśnięcia, mogą być szczególnie podatne na przechwycenie lub ataki siłowe. Na przykład poniższy kod jest używany przez podatną na ataki aplikację hostowaną w laboratorium Predictable Tokens:

```php
$token = mt_rand(100, 200);
$query = $conn->prepare("UPDATE users SET reset_token = ? WHERE email = ?");
$query->bind_param("ss", $token, $email);
$query->execute();
```

Powyższy kod ustawia losowy trzycyfrowy PIN jako token resetujący przesłanego e-maila. Ponieważ token ten nie zawiera znaków mieszanych, można go łatwo złamać metodą brute force.

Aby to zademonstrować, przejdź do [http://enum.thm/laboratoria/przewidywalne_tokeny/(otwiera się w nowej karcie)](http://enum.thm/labs/predictable_tokens/).

![Przewidywalne logowanie tokenami](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719133556444)  

Przejdź do strony resetowania hasła aplikacji, w polu adresu e-mail wpisz „admin@admin.com”  i kliknij Prześlij.

![Strona resetowania aplikacji](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719133557936)  

Aplikacja odpowie komunikatem o powodzeniu operacji.

![Link do resetowania hasła został wysłany](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719133558420)  

W celach demonstracyjnych aplikacja internetowa wykorzystuje łącze reset:`http://enum.thm/labs/predictable_tokens/reset_password.php?token=123`

![Komunikat o błędzie nieprawidłowego tokena](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1721645083625.png)  

Zwróć uwagę, że token to prosta wartość liczbowa.  Korzystając z Burp Suite, przejdź do powyższego adresu URL i przechwyć żądanie.

Następnie wyślij żądanie do Intrudera, zaznacz wartość parametru tokena i kliknij przycisk Dodaj ładunek, jak pokazano poniżej.

![Karta Intruder z podatnym żądaniem](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719133559379)  

Używając AttackBox lub własnej maszyny wirtualnej do ataku, użyj Cruncha do wygenerowania listy liczb od 100 do 200. Lista ta będzie używana jako słownik w ataku siłowym.

Korzystanie z Crunch

```shell-session
user@tryhackme $ crunch 3 3 -o otp.txt -t %%% -s 100 -e 200             

Crunch will now generate the following amount of data: 404 bytes
0 MB
0 GB
0 TB
0 PB
Crunch will now generate the following number of lines: 101 

crunch: 100% completed generating output
```

Wróć do Intrudera i skonfiguruj ładunek tak, aby korzystał z wygenerowanego pliku.

![otp.txt w intruzie](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719134235270)

![pokazując załadowany plik otp.txt](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1722386680524.png)  

Jeśli używasz aplikacji, atak potrwa jakiś czas.Burp SuiteWersja Community. Jednak po pomyślnym zalogowaniu otrzymasz odpowiedź o znacznie obszerniejszej treści w porównaniu z odpowiedziami z komunikatem o błędzie „Nieprawidłowy token”.

![Odpowiedź o największym rozmiarze odpowiedzi](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719134236525)

Zaloguj się do aplikacji używając nowego hasła.

![Flaga na pulpicie nawigacyjnym](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719134237182)

Należy pamiętać, że większość aplikacji internetowych używa kodu 6-cyfrowego zamiast trzycyfrowego. W tej wersji demonstracyjnej używamy niższej wartości, ponieważ korzystamy z wersji Community pakietu Burp Suite.

### Podstawowe uwierzytelnianie w 2k24?

Uwierzytelnianie podstawowe oferuje prostszą metodę zabezpieczania dostępu do urządzeń. Wymaga jedynie nazwy użytkownika i hasła, co ułatwia wdrożenie i zarządzanie na urządzeniach o ograniczonej mocy obliczeniowej.  Urządzenia sieciowe, takie jak routery, zazwyczaj wykorzystują uwierzytelnianie podstawowe do kontrolowania dostępu do interfejsów administracyjnych. W tym scenariuszu głównym celem jest zapobieganie nieautoryzowanemu dostępowi przy minimalnej konfiguracji.

Chociaż uwierzytelnianie podstawowe nie oferuje solidnych zabezpieczeń, jakie oferują bardziej złożone protokoły, takie jak OAuth czy uwierzytelnianie oparte na tokenach, jego prostota sprawia, że ​​nadaje się ono do środowisk, w których zarządzanie sesjami i śledzenie użytkowników nie jest wymagane lub jest zarządzane w inny sposób. Na przykład w urządzeniach takich jak routery, do których dostęp jest uzyskiwany głównie w celu zmiany konfiguracji, a nie do regularnego użytkowania, obciążenie związane z utrzymywaniem stanów sesji jest zbędne i może komplikować wydajność urządzenia.

HTTP Uwierzytelnianie podstawowe jest zdefiniowane w[RFC7617(otwiera się w nowej karcie)](https://datatracker.ietf.org/doc/html/rfc7617), który określa, że ​​dane uwierzytelniające (nazwa użytkownika i hasło) powinny być przesyłane jako ciąg zakodowany w standardzie Base64 w nagłówku autoryzacji HTTP. Ta metoda jest prosta, ale niebezpieczna w przypadku połączeń innych niż HTTPS, ponieważ Base64 nie jest metodą szyfrowania i można ją łatwo zdekodować. Prawdziwe zagrożenie często wynika ze słabych danych uwierzytelniających, które można złamać metodą brute force.

Uwierzytelnianie podstawowe HTTP zapewnia prosty mechanizm typu wyzwanie-odpowiedź, umożliwiający żądanie danych uwierzytelniających użytkownika.

![Podstawowy proces logowania uwierzytelniającego](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719037051793)

_https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication_  

Format nagłówka autoryzacji jest następujący:

```html
Authorization: Basic <credentials>
```

Gdzie `<credentials>`jest kodowanie base64 dla `username:password`. Szczegółowe specyfikacje można znaleźć w [RFC 7617(otwiera się w nowej karcie)](https://tools.ietf.org/html/rfc7617).

### Eksploatacja

Aby to zademonstrować, przejdź do  [http://enum.thm/labs/basic_auth/(otwiera się w nowej karcie)](http://enum.thm/labs/basic_auth/).

![Strona główna laboratorium uwierzytelniania podstawowego](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719138339394)  

Wprowadź nazwę użytkownika i hasło w wyskakującym okienku i przechwyć podstawowe żądanie uwierzytelnienia za pomocą Burp.

![Losowe dane logowania w wyskakującym okienku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719138339820)

![Zakodowane dane logowania w nagłówku żądania HTTP](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719138340268)  

Kliknij prawym przyciskiem myszy żądanie i wyślij je do Intrudera.

![Menu kontekstowe przechwyconego żądania](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719623302038.png)  

W Burp Intruder przejdź do zakładki „Pozycje” i zdekoduj zakodowany ciąg base64 w nagłówku Autoryzacji.

![Zdekodowany ciąg zakodowany w formacie Base64](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719623303064.png)  

Po zdekodowaniu zaznacz zdekodowany ciąg i kliknij przycisk Dodaj w prawym górnym rogu.

![Podświetlony tekst z podświetleniem ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719623303378.png)  

Następnie konfigurujemy ładunki. Przejdź do zakładki „Ładunki”, ustaw typ ładunku na „Lista prosta” i wybierz preferowaną listę słów. W tej wersji demonstracyjnej użyjemy pliku „ [500-worst-passwords.txt”.(otwiera się w nowej karcie)](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt)z SecLists. Jeśli używasz AttackBox, możesz użyć tej samej listy słów, która znajduje się pod adresem  `/usr/share/wordlists/SecLists/Passwords/Common-Credentials/500-worst-passwords.txt`.

![Wybór listy słów](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624218420.png)

Ponieważ nagłówek jest zakodowany w formacie Base64, musimy dodać dwie reguły w sekcji przetwarzania danych. Pierwsza z nich automatycznie dodaje nazwę użytkownika do hasła, więc zamiast 123456, dane będą miały postać „admin:123456”.

![Pierwsza zasada przetwarzania ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1721558974360.png)  

Druga reguła zakoduje w formacie Base64 połączoną nazwę użytkownika i hasło z dostarczonej listy.

![Druga zasada przetwarzania ładunku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1721559029302.png)  

Powinniśmy również usunąć znak „=” (znak równości) z kodowania, ponieważ base64 używa znaku „=” do wypełnienia. Aby to zrobić, przewiń w dół i usuń znak „=” z listy znaków w sekcji „Kodowanie ładunku”.

![Usuwanie znaku równości ze względu na wypełnienie](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1721559089710.png)  

Po zakończeniu wróć do zakładki „Pozycje” i kliknij przycisk „Rozpocznij atak”. Atak zajmie nieco mniej niż 2 minuty.

![Rozpoczęcie ataku](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624746210.png)

Otrzymanie kodu statusu 200 oznacza, że ​​atak siłowy powiódł się i jedno z haseł z podanej listy działa. Zdekoduj zakodowany ciąg base64 w pomyślnym żądaniu.

![Dekodowanie treści pomyślnego żądania](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624746716.png)

![Zdekodowana wartość ciągu base64](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624747204.png)

Użyj zdekodowanego ciągu base64, aby zalogować się do aplikacji.

![Korzystanie z danych uwierzytelniających w celu zalogowania się](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624882640.png)

![Flaga na pulpicie nawigacyjnym](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719624883193.png)

### Wayback URL i Google Dorks  

Zapoznanie się z przeszłością aplikacji internetowej może być równie odkrywcze, co badanie jej teraźniejszości:

**Adresy URL Wayback**

Pomyśl o Wayback Machine Internet Archive ( [https://archive.org/web/(otwiera się w nowej karcie)](https://archive.org/web/)) jako wehikuł czasu. Pozwala cofnąć się w czasie i eksplorować starsze wersje stron internetowych, odkrywając pliki i katalogi, które nie są już widoczne, ale wciąż mogą znajdować się na serwerze. Te relikty mogą czasami stanowić tylne wejście do obecnego systemu.

![Strona główna waybackmachine](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719829002513.png)

Na przykład, używając TryHackMe jako celu, możemy zobaczyć wszystkie poprzednie wersje witryny od 2018 roku do chwili obecnej.

![Zapisane dane witryny internetowej](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1719829002857.png)

Aby zrzucić wszystkie linki zapisane w Wayback Machine, możemy użyć narzędzia o nazwie waybackurls. Hostowane w [GitHubie.(otwiera się w nowej karcie)](https://github.com/tomnomnom/waybackurls)Możemy łatwo zainstalować go na naszym komputerze, korzystając z poniższych poleceń:

**Uwaga:** Instalacja tego narzędzia wykracza poza zakres tego pokoju. Zaleca się również zainstalowanie tego narzędzia przy użyciu własnegoMaszyna wirtualna.  

Zainstaluj waybackurls  

```shell-session
user@tryhackme $ git clone https://github.com/tomnomnom/waybackurls
user@tryhackme $ cd waybackurls
user@tryhackme $ sudo apt install golang-go -y # This command is optional
user@tryhackme $ go build
user@tryhackme $ ls -lah
total 6.6M
drwxr-xr-x 4 user user 4.0K Jul  1 18:20 .
drwxr-xr-x 9 user user 4.0K Jul  1 18:20 ..
drwxr-xr-x 8 user user 4.0K Jul  1 18:20 .git
-rw-r--r-- 1 user user   36 Jul  1 18:20 .gitignore
-rw-r--r-- 1 user user  454 Jul  1 18:20 README.mkd
-rw-r--r-- 1 user user   49 Jul  1 18:20 go.mod
-rw-r--r-- 1 user user 5.4K Jul  1 18:20 main.go
drwxr-xr-x 2 user user 4.0K Jul  1 18:20 script
-rwxr-xr-x 1 user user 6.5M Jul  1 18:20 waybackurls
user@tryhackme $ ./waybackurls tryhackme.com
[-- snip --]
https://tryhackme.com/.well-known/ai-plugin.json
https://tryhackme.com/.well-known/assetlinks.json
https://tryhackme.com/.well-known/dnt-policy.txt
https://tryhackme.com/.well-known/gpc.json
https://tryhackme.com/.well-known/nodeinfo
https://tryhackme.com/.well-known/openid-configuration
https://tryhackme.com/.well-known/security.txt
https://tryhackme.com/.well-known/trust.txt
[-- snip --]
```

**Google Dorks**  

Tutaj Twoja biegłość w wyszukiwarkach się sprawdza. Tworząc konkretne zapytania, znane jako Google Dorks, możesz znaleźć informacje, które nie miały być publiczne. Zapytania te mogą wydobyć wszystko, od ujawnionych katalogów administracyjnych po logi zawierające hasła i indeksy poufnych katalogów. Na przykład:

- Aby znaleźć panele administracyjne:`site:example.com inurl:admin`
- Aby wyszukać pliki dziennika z hasłami:`filetype:log "password" site:example.com`
- Aby odkryć katalogi kopii zapasowych:`intitle:"index of" "backup" site:example.com`

### Wniosek

W tej sali omówiliśmy różne aspekty ataków enumeracyjnych i siłowych na aplikacje internetowe, wyposażając Cię w wiedzę i praktyczne umiejętności niezbędne do przeprowadzania dokładnych ocen bezpieczeństwa.

### Najważniejsze wnioski

- **Skuteczna enumeracja** : Prawidłowa enumeracja ma kluczowe znaczenie dla identyfikacji potencjalnych luk w zabezpieczeniach aplikacji internetowych. Użycie odpowiednich narzędzi i technik może ujawnić cenne informacje, które pomogą w planowaniu dalszych ataków.
- **Skuteczność ataków siłowych** : Optymalizacja ataków siłowych polega na tworzeniu inteligentnych list słów, zarządzaniu parametrami ataku i unikaniu mechanizmów wykrywania, takich jak ograniczanie przepustowości i blokowanie kont.
- **Odpowiedzialność etyczna** : Zawsze przeprowadzaj ataki enumeracyjne i brute force za wyraźną zgodą właściciela systemu. Nieautoryzowane ataki są nielegalne i mogą mieć poważne konsekwencje.
