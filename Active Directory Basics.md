---

Wstęp

Usługa Active Directory firmy Microsoft stanowi podstawę świata korporacyjnego. Upraszcza zarządzanie urządzeniami i użytkownikami w środowisku korporacyjnym.

W tym pomieszczeniu dokładnie przyjrzymy się podstawowym komponentom usługi Active Directory i wcielimy się w rolę nowego administratora IT.THM Sp. z o.o. Naszym pierwszym zadaniem było utworzenie nowej domeny podrzędnej Active Directory, dołączenie serwera do domeny, a następnie sprawdzenie niektórych istniejących kontrolek i konfiguracji w domenie nadrzędnej. Otrzymasz uprawnienia administracyjne do wszystkich serwerów, aby wprowadzić te zmiany w konfiguracji i ukończyć kolejne zadania.

## Cele edukacyjne

W tej sali dowiemy się więcej na temat usługi Active Directory i zapoznamy się z następującymi tematami:

- Czym jest Active Directory
- Czym jest domena Active Directory
- Jakie komponenty wchodzą w skład domeny Active Directory
- Lasy i zaufanie domenowe

## Wymagania wstępne

Zanim rozpoczniesz pracę w tym pokoju, powinieneś zapoznać się z następującymi informacjami:

- Ogólna znajomość systemu Windows
- Koncepcje omówione w [Podstawach systemu Windows](https://tryhackme.com/module/windows-fundamentals)

## Konfiguracja sieci

W tym pokoju znajdziesz sieć, w której utworzysz własny las Active Directory! Jeśli korzystasz z sieci w TryHackMe po raz pierwszy, zalecamy zapoznanie się z [Przewodnikiem po pokoju sieciowym](https://tryhackme.com/room/networkroomguide) . Dla przypomnienia, możesz użyć AttackBoxa do połączenia się z tą siecią lub pobrać plik OVPN sieci z poniższego diagramu sieci:

![Przycisk pobierania sieciowego|700](https://cdn-images.tryhackme.com/user-uploads/6241db5522713b00497f96ac/room-content/6241db5522713b00497f96ac-1783428046066.png)

Jeśli masz problemy z połączeniem z siecią, zapoznaj się z instrukcjami debugowania podanymi w [Network Guide Room](https://tryhackme.com/jr/networkroomguide) . Twój zakres podsieci dla tego network roomu będzie wynosił `192.168.10.0/24`.

## Dlaczego Active Directory

Wyobraź sobie, że administrujesz małą siecią firmową z zaledwie pięcioma komputerami i pięcioma pracownikami. W tak małej sieci prawdopodobnie bez problemu skonfigurujesz każdy komputer osobno. Będziesz ręcznie logować się do każdego komputera, tworzyć konta użytkowników dla tych, którzy będą z nich korzystać, i wprowadzać konkretne konfiguracje dla kont każdego pracownika. Jeśli komputer użytkownika przestanie działać, prawdopodobnie udasz się do jego lokalizacji i naprawisz go na miejscu.

Choć brzmi to jak bardzo swobodny styl życia, załóżmy, że Twoja firma nagle się rozrasta i ma teraz 157 komputerów i 320 różnych użytkowników w czterech różnych biurach. Czy nadal mógłbyś zarządzać każdym komputerem jako oddzielnym elementem, ręcznie konfigurować zasady dla każdego użytkownika w sieci i zapewniać wsparcie techniczne na miejscu? Odpowiedź brzmi: najprawdopodobniej nie.

Aby pokonać te ograniczenia, możemy użyć domeny Windows. Mówiąc najprościej, **domena Windows** to grupa użytkowników i komputerów zarządzana przez daną firmę. Główną ideą domeny jest centralizacja zarządzania wspólnymi komponentami sieci komputerowej Windows w jednym repozytorium o nazwie **Active Directory (OGŁOSZENIE)** Serwer, na którym działają usługi Active Directory, nazywany jest **kontrolerem domeny (DC)** . 

![Przegląd domeny Windows|700](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/bebe5dfec0208bf563d01fa2dd1fb7a7.png)

Główne zalety posiadania skonfigurowanej domeny Windows to:

- **Centralne zarządzanie tożsamościami:** wszystkich użytkowników w sieci można skonfigurować z poziomu usługi Active Directory przy minimalnym wysiłku.
- **Zarządzanie zasadami bezpieczeństwa:** Możesz konfigurować zasady bezpieczeństwa bezpośrednio w usłudze Active Directory i stosować je w razie potrzeby wobec użytkowników i komputerów w całej sieci.

## Przykład ze świata rzeczywistego

Jeśli wydaje Ci się to trochę zagmatwane, istnieje duże prawdopodobieństwo, że w szkole, na uniwersytecie lub w miejscu pracy miałeś już styczność z domeną Windows.

W sieciach szkolnych/uniwersyteckich często otrzymasz nazwę użytkownika i hasło, których możesz używać na dowolnym komputerze dostępnym na terenie kampusu. Twoje dane uwierzytelniające są ważne na wszystkich komputerach, ponieważ za każdym razem, gdy je wpiszesz na komputerze, proces uwierzytelniania jest przekazywany z powrotem do Active Directory, gdzie Twoje dane uwierzytelniające są sprawdzane. Dzięki Active Directory Twoje dane uwierzytelniające nie muszą być przechowywane na każdym komputerze i są dostępne w całej sieci.

Active Directory to również komponent, który pozwala Twojej szkole/uczelni ograniczyć Twój dostęp do panelu sterowania na swoich komputerach. Zasady zazwyczaj są wdrażane w całej sieci, więc nie masz uprawnień administratora na tych komputerach.

## Domena nadrzędna

Będziemy teraz pracować w domenie nadrzędnej (lub głównej) naszego lasu Active Directory. Jest to `THM.LOC`domena TryHackMe(). Połącz się z kontrolerem domeny ( `ROOTDC.THM.LOC`) przez RDP, używając następujących danych logowania:

Referencje

Nazwa użytkownika

THM\Administrator

Hasło

learningadisfun1!

Adres IP

192.168.10.100

Połączenie przez

RDP

xfreerdp /u:Administrator /p:'learningadisfun1!' /d:THM.LOC /v:192.168.10.100 /dynamic-resolution

## Usługa domeny Active Directory

Podstawą każdej domeny Windows jest  **usługa Active Directory Domain Service (AD DS)** . Usługa ta działa jak katalog przechowujący informacje o wszystkich obiektach istniejących w sieci. Wśród wielu obiektów obsługiwanych przez AD znajdują się użytkownicy, grupy, komputery, drukarki, udziały i wiele innych. Przyjrzyjmy się niektórym z nich:

**Użytkownicy**

Użytkownicy to jeden z najpopularniejszych typów obiektów w usłudze Active Directory. Są oni jednym z obiektów znanych jako **podmioty zabezpieczeń** , co oznacza, że ​​mogą być uwierzytelniani przez domenę i przydzielani do  **zasobów,** takich jak pliki czy drukarki. Można powiedzieć, że podmiot zabezpieczeń to obiekt, który może działać na zasobach sieciowych.

Użytkownicy mogą reprezentować dwa typy podmiotów:

- **Ludzie:** Użytkownicy to zazwyczaj osoby w Twojej organizacji, które potrzebują dostępu do sieci, np. pracownicy.
- **Usługi:** Możesz również definiować użytkowników dla usług takich jak IIS czy MSSQL. Każda usługa wymaga użytkownika do uruchomienia, ale użytkownicy usług różnią się od zwykłych użytkowników, ponieważ mają uprawnienia wymagane tylko do uruchomienia swojej konkretnej usługi.

**Maszyny**

Maszyny to kolejny typ obiektów w usłudze Active Directory; dla każdego komputera dołączającego do domeny Active Directory tworzony jest obiekt maszyny. Maszyny są również uważane za „podmioty zabezpieczeń” i przypisuje się im konta, tak jak każdemu zwykłemu użytkownikowi. Konto to ma nieco ograniczone uprawnienia w obrębie samej domeny.

Konta maszynowe są kontami lokalnych administratorów na przypisanym komputerze. Zasadniczo nikt poza użytkownikiem samego komputera nie powinien mieć do nich dostępu, ale tak jak w przypadku każdego innego konta, jeśli znasz hasło, możesz się za jego pomocą zalogować.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Hasła do kont komputerów są automatycznie zmieniane i zazwyczaj składają się ze 120 losowych znaków.

Identyfikacja kont maszynowych jest stosunkowo łatwa. Stosują one określony schemat nazewnictwa. Nazwa konta maszynowego to nazwa komputera, po której następuje znak dolara. Na przykład, komputer o nazwie `ROOTDC`będzie miał konto maszynowe o nazwie `ROOTDC$`.

**Grupy zabezpieczeń**

Jeśli znasz system Windows, prawdopodobnie wiesz, że możesz definiować grupy użytkowników, aby przypisywać prawa dostępu do plików lub innych zasobów całym grupom, a nie poszczególnym użytkownikom. Pozwala to na łatwiejsze zarządzanie, ponieważ możesz dodawać użytkowników do istniejącej grupy, a oni automatycznie odziedziczą wszystkie uprawnienia grupy. Grupy zabezpieczeń są również uważane za podmioty zabezpieczeń i dlatego mogą mieć uprawnienia do zasobów sieciowych.

Grupy mogą zawierać zarówno użytkowników, jak i maszyny jako członków. W razie potrzeby grupy mogą obejmować również inne grupy.

W domenie domyślnie tworzonych jest kilka grup, które można wykorzystać do nadawania użytkownikom określonych uprawnień. Dla przykładu, oto kilka najważniejszych grup w domenie:

|   |   |
|---|---|
|**Grupa Bezpieczeństwa**|**Opis**|
|Administratorzy domeny|Użytkownicy tej grupy mają uprawnienia administracyjne w całej domenie. Domyślnie mogą administrować dowolnym komputerem w domenie, w tym kontrolerami domeny.|
|Operatorzy serwerów|Użytkownicy w tej grupie mogą administrować kontrolerami domeny. Nie mogą zmieniać członkostwa w żadnej grupie administracyjnej.|
|Operatorzy zapasowi|Użytkownicy z tej grupy mają dostęp do dowolnego pliku, ignorując swoje uprawnienia. Służą do tworzenia kopii zapasowych danych na komputerach.|
|Operatorzy kont|Użytkownicy tej grupy mogą tworzyć lub modyfikować inne konta w domenie.|
|Użytkownicy domeny|Obejmuje wszystkie istniejące konta użytkowników w domenie.|
|Komputery domenowe|Obejmuje wszystkie istniejące komputery w domenie.|
|Kontrolery domeny|Obejmuje wszystkie istniejące kontrolery domeny w domenie.|

Pełną listę domyślnych grup zabezpieczeń można uzyskać w [dokumentacji firmy Microsoft(otwiera się w nowej karcie)](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups).

## Użytkownicy i komputery usługi Active Directory

Aby skonfigurować użytkowników, grupy lub komputery w usłudze Active Directory, musimy zalogować się do kontrolera domeny i uruchomić „Użytkownicy i komputery usługi Active Directory” z menu Start:

![Menu Start Użytkownicy i komputery AD|519](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/11d01963392078c1450300d2881f9160.png)

Otworzy się okno, które pokazuje hierarchię użytkowników, komputerów i grup w domenie. Obiekty te są zorganizowane w **jednostki organizacyjne (OU),** które są obiektami kontenerowymi umożliwiającymi klasyfikację użytkowników i maszyn. Jednostki organizacyjne służą głównie do definiowania zestawów użytkowników o podobnych wymaganiach dotyczących kontroli. Pracownicy działu sprzedaży w Twojej organizacji prawdopodobnie mają inny zestaw zasad niż na przykład pracownicy działu IT. Należy pamiętać, że użytkownik może należeć tylko do jednej jednostki organizacyjnej na raz.

Sprawdzając naszą maszynę, widzimy, że istnieje już wywołana jednostka organizacyjna `THM`z pięcioma jednostkami podrzędnymi dla działów IT, Zarządzania, Marketingu, Badań i Rozwoju oraz Sprzedaży. Jednostki organizacyjne często odzwierciedlają strukturę firmy, ponieważ pozwala to na efektywne wdrażanie zasad bazowych, które mają zastosowanie do całych działów. Należy pamiętać, że chociaż w większości przypadków byłby to oczekiwany model, jednostki organizacyjne można definiować dowolnie. Możesz utworzyć nową jednostkę.Jednostka organizacyjnawywoływane `Students`tylko dla zabawy poprzez kliknięcie prawym przyciskiem myszy na `THM`jednostkę organizacyjną i wybranie **Nowy** , a następnie **Jednostka organizacyjna** .

![Użytkownicy i komputery AD](https://cdn-images.tryhackme.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1751295060748.png)

Po otwarciu dowolnej jednostki organizacyjnej (OU) możesz zobaczyć użytkowników, których ona zawiera, i w razie potrzeby wykonać proste zadania, takie jak tworzenie, usuwanie lub modyfikowanie. W razie potrzeby możesz również zresetować hasła (bardzo przydatne dla działu pomocy technicznej):

![Dział IT OU](https://cdn-images.tryhackme.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1751295060689.png)

Prawdopodobnie zauważyłeś już, że istnieją inne domyślne kontenery oprócz`THM` Jednostka organizacyjnaTe kontenery są tworzone automatycznie przez system Windows i zawierają następujące elementy:

- **Wbudowane:** Zawiera domyślne grupy dostępne dla dowolnego hosta Windows.
- **Komputery:** Domyślnie wszystkie komputery dołączające do sieci będą umieszczane w tym miejscu. Możesz je przenieść w razie potrzeby.
- **Kontrolery domeny:** domyślne Jednostka organizacyjna zawierający kontrolery domeny w Twojej sieci.
- **Użytkownicy:** Domyślni użytkownicy i grupy, które mają zastosowanie w kontekście całej domeny.
- **Zarządzane konta usług:** Zawierają konta używane przez usługi w domenie Windows.

## Grupy zabezpieczeń kontra jednostki organizacyjne

Prawdopodobnie zastanawiasz się, dlaczego mamy zarówno grupy, jak i jednostki organizacyjne. Chociaż oba służą do klasyfikowania użytkowników i komputerów, ich cele są zupełnie inne:

- **Jednostki organizacyjne** są przydatne do  **stosowania zasad** do użytkowników i komputerów, w tym do konkretnych konfiguracji, które mają zastosowanie do grup użytkowników w oparciu o ich role w przedsiębiorstwie. Należy pamiętać, że użytkownik może być członkiem tylko jednej Jednostka organizacyjnanaraz, ponieważ nie miałoby sensu stosowanie dwóch różnych zestawów zasad do jednego użytkownika.
- **Grupy zabezpieczeń** służą natomiast do **przyznawania uprawnień do zasobów** . Na przykład, za pomocą grup można zezwolić wybranym użytkownikom na dostęp do folderu współdzielonego lub drukarki sieciowej. Użytkownik może należeć do wielu grup, co jest niezbędne do przyznania dostępu do wielu zasobów.

W przypadku korzystania z domen Windows wszystkie dane uwierzytelniające są przechowywane w kontrolerach domeny. Za każdym razem, gdy użytkownik próbuje uwierzytelnić się w usłudze przy użyciu danych uwierzytelniających domeny, usługa musi poprosić kontroler domeny o weryfikację poprawności danych uwierzytelniających. Do uwierzytelniania sieciowego w domenach Windows można używać dwóch protokołów:

- **Kerberos:** Używany przez każdą nowszą wersję systemu Windows. Jest to domyślny protokół w każdej nowszej domenie.
- **NetNTLM:** Zachowano starszy protokół uwierzytelniania w celu zapewnienia kompatybilności.

Chociaż NetNTLM należy uznać za przestarzały, większość sieci będzie miała włączone oba protokoły. Przyjrzyjmy się bliżej, jak działa każdy z nich.

## Kerberos Uwierzytelnianie

Kerberos Uwierzytelnianie to domyślny protokół uwierzytelniania w najnowszych wersjach systemu Windows. Użytkownicy logujący się do usługi za pomocą Kerberos Otrzymają bilety. Pomyśl o biletach jako o dowodzie wcześniejszego uwierzytelnienia. Użytkownicy posiadający bilety mogą je przedstawić w usłudze, aby udowodnić, że uwierzytelnili się już w sieci i są upoważnieni do korzystania z niej.

Gdy Kerberos służy do uwierzytelniania, odbywa się następujący proces:

1. Użytkownik wysyła swoją nazwę użytkownika i znacznik czasu zaszyfrowane kluczem uzyskanym na podstawie hasła do **Centrum Dystrybucji Kluczy (KDC)** , usługa zwykle instalowana na kontrolerze domeny, która wydaje Kerberos  
      
    bilety w sieci. KDC utworzy i odeśle **Bilet Udzielający Biletu (TGT)** , co umożliwi użytkownikowi zamawianie dodatkowych biletów w celu uzyskania dostępu do określonych usług. Potrzeba posiadania biletu, aby uzyskać więcej biletów, może wydawać się dziwna, ale pozwala użytkownikom zamawiać bilety na usługi bez konieczności podawania danych logowania za każdym razem, gdy chcą połączyć się z usługą. Wraz z TGT Użytkownikowi dostarczany jest klucz sesji, który będzie musiał wygenerować w celu realizacji kolejnych żądań. Należy **pamiętać**  
      
    , że TGT Jest szyfrowany  hasłem konta **krbtgt** , więc użytkownik nie ma dostępu do jego zawartości. Należy pamiętać, że szyfrowane TGT zawiera kopię Klucza Sesji jako część swojej zawartości, a KDC nie musi przechowywać klucza sesji, ponieważ może odzyskać kopię poprzez odszyfrowanie TGTjeśli to konieczne.![Krok 1 Kerberos](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/d36f5a024c20fb480cdae8cd09ddc09f.png)
1. Gdy użytkownik chce połączyć się z usługą w sieci, np. udostępnionym zasobem, witryną internetową lub bazą danych, użyje swojego TGTaby poprosić o **usługę przyznawania biletów (TGS)** bilet z KDC.TGSto bilety umożliwiające połączenie tylko z konkretną usługą, dla której zostały utworzone. Aby poprosić oTGSużytkownik wyśle ​​swoją nazwę użytkownika i znacznik czasu zaszyfrowane kluczem sesji wraz zTGTi **główną nazwę usługi (SPN)** wskazujące nazwę usługi i serwera, do którego chcemy uzyskać dostęp.  
      
    W rezultacieKDCwyśle ​​namTGSwraz z **kluczem sesji usługi** , który będzie nam potrzebny do uwierzytelnienia się w usłudze, do której chcemy uzyskać dostęp.TGSjest szyfrowany przy użyciu klucza uzyskanego z  **skrótu właściciela usługi** . Właścicielem usługi jest konto użytkownika lub komputera, na którym działa usługa.TGSzawiera kopię klucza sesji usługi w swojej zaszyfrowanej zawartości, dzięki czemu właściciel usługi może uzyskać do niego dostęp, odszyfrowującTGS.  
    ![Kerberos krok 2](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/84504666e78373c613d3e05d176282dc.png)
2. TenTGSNastępnie można je wysłać do wybranej usługi w celu uwierzytelnienia i nawiązania połączenia. Usługa użyje skrótu hasła skonfigurowanego konta do odszyfrowania.TGSi zatwierdź klucz sesji serwisowej.  
    ![Krok 3 Kerberos](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/8fbf08d03459c1b792f3b6efa4d7f285.png)

## Uwierzytelnianie NetNTLM

NetNTLM działa w oparciu o mechanizm „wyzwanie-odpowiedź”. Cały proces wygląda następująco:

![Uwierzytelnianie NetNTLM](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/2eab5cacbd0d3e9dc9afb86169b711ec.png)

1. Klient wysyła żądanie uwierzytelnienia do serwera, do którego chce uzyskać dostęp.
2. Serwer generuje losową liczbę i wysyła ją jako wyzwanie do klienta.
3. Klient łączy swojeNTLMskrót hasła wraz z wyzwaniem (oraz innymi znanymi danymi) w celu wygenerowania odpowiedzi na wyzwanie i odesłania jej do serwera w celu weryfikacji.
4. Serwer przekazuje wyzwanie i odpowiedź do kontrolera domeny w celu weryfikacji.
5. Kontroler domeny wykorzystuje wyzwanie do ponownego obliczenia odpowiedzi i porównuje ją z oryginalną odpowiedzią wysłaną przez klienta. Jeśli obie odpowiedzi są zgodne, klient zostaje uwierzytelniony; w przeciwnym razie dostęp zostaje odrzucony. Wynik uwierzytelnienia jest odsyłany do serwera.
6. Serwer przesyła wynik uwierzytelnienia do klienta.

Należy pamiętać, że hasło użytkownika (lub jego skrót) nigdy nie jest przesyłane przez sieć ze względów bezpieczeństwa.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Opisany proces ma zastosowanie w przypadku korzystania z konta domenowego. W przypadku korzystania z konta lokalnego serwer może zweryfikować odpowiedź na wyzwanie bez konieczności interakcji z kontrolerem domeny, ponieważ ma już zapisany lokalnie skrót hasła w swoim systemie zarządzania kontem (SAM).

Na razie przyjrzeliśmy się tylko jednej domenie.

![Pojedyncza domena](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/69f2441bbafd4cfe57a101d87f3c5950.png)

Wraz z rozwojem firm, rozwijają się również ich sieci. Posiadanie jednej domeny dla firmy wystarczy na początek, ale z czasem, wraz z rozwojem potrzeb, może się okazać, że będziesz musiał mieć więcej niż jedną. 

## Drzewa

Wyobraźmy sobie na przykład, że TryHackMe postanawia rozszerzyć działalność na sektor bankowy. Zamiast po prostu dodać wszystko do istniejącej domeny, łatwiej będzie zarządzać nową subdomeną. W tym przypadku `thm.loc`będzie ona działać jako domena nadrzędna, a my utworzymy `tbm.thm.loc`domenę TryBankMe(). Zarówno w organizacji nadrzędnej, jak i w organizacji bankowej, będziemy mieć zespoły IT, które będą musiały zarządzać swoimi zasobami. Posiadanie tylko jednej, rozległej struktury AD będzie trudne w zarządzaniu i podatne na błędy konfiguracji oraz luki w zabezpieczeniach.

Na szczęście dla nas, Active Directory obsługuje integrację wielu domen, co pozwala na podzielenie sieci na jednostki, którymi można zarządzać niezależnie. Jeśli masz dwie domeny współdzielące tę samą przestrzeń nazw ( `thm.loc`w naszym przykładzie), możesz je połączyć w **drzewo** .

Dla naszej `thm.loc`domeny chcemy utworzyć nową subdomenę dla działu bankowości o nazwie `tbm.thm.loc`. Podobnie, gdybyśmy mieli biura w kilku regionach, moglibyśmy rozwinąć to jeszcze bardziej, tworząc domeny `us.tbm.thm.loc`i `uk.tbm.thm.loc`, z których każda ma swoją domenę AD, komputery i użytkowników:

![Drzewo](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/abea24b7979676a1dcc0c568054544c8.png)

Ta podzielona struktura daje nam lepszą kontrolę nad tym, kto ma dostęp do czego w domenie. Zespół IT z działu bankowości będzie miał własny kontroler domeny, który będzie zarządzał wyłącznie zasobami bankowymi. Na przykład, użytkownik bankowości nie będzie mógł zmieniać uprawnień w domenie nadrzędnej. 

Omawiając drzewa i lasy, należy wprowadzić nową grupę zabezpieczeń.  Grupa **Enterprise Admins** przyznaje użytkownikowi uprawnienia administracyjne we wszystkich domenach przedsiębiorstwa. Każda domena nadal będzie miała swoich administratorów domeny z uprawnieniami administracyjnymi w poszczególnych domenach oraz administratorów Enterprise Admins, którzy będą mogli kontrolować wszystko w przedsiębiorstwie.

## Lasy

Zarządzane domeny można również skonfigurować w różnych przestrzeniach nazw. Załóżmy, że Twoja firma stale się rozwija i w końcu musi zintegrować się z nowym dostawcą o nazwie TryVendorMe. Obie firmy będą miały własne domeny Active Directory ( **drzewa** ), ale zasoby będą musiały być współdzielone między tymi domenami ( **lasami** ). Na szczęście usługa Active Directory (AD) oferuje również metodę łączenia tych lasów.

![Las](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/03448c2faf976db890118d835000bab7.png)

## Relacje oparte na zaufaniu

Posiadanie wielu domen zorganizowanych w drzewa i lasy pozwala na stworzenie dobrze zorganizowanej, podzielonej na sekcje sieci do zarządzania i alokacji zasobów. Jednak w pewnym momencie użytkownik TryVendorMe może potrzebować wsparcia pracownika banku. Aby to osiągnąć, domeny zorganizowane w drzewa i lasy są połączone **relacjami zaufania** .

Mówiąc prościej, relacja zaufania między domenami pozwala na upoważnienie użytkownika danej domeny  `tvm.loc`do dostępu do zasobów danej domeny  `tbm.thm.loc`.

Najprostszą relacją zaufania, jaką można ustanowić, jest **jednokierunkowa relacja zaufania** . W przypadku jednokierunkowej relacji zaufania, jeśli `Domain AAA`, `Domain BBB`oznacza to, że użytkownik BBB może uzyskać autoryzację do dostępu do zasobów w AAA:

![Trusty](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/af95eb1a4b6c672491d8989f79c00200.png)

Kierunek jednokierunkowej relacji zaufania jest przeciwny do kierunku dostępu.

**Można również ustanowić dwukierunkowe relacje zaufania** , aby umożliwić obu domenom wzajemną autoryzację użytkowników z drugiej domeny. Domyślnie połączenie kilku domen w ramach drzewa lub lasu tworzy dwukierunkową relację zaufania.

Należy pamiętać, że relacja zaufania między domenami nie zapewnia automatycznie dostępu do wszystkich zasobów w innych domenach. Po ustanowieniu relacji zaufania możesz autoryzować użytkowników w różnych domenach, ale to od Ciebie zależy, co zostanie autoryzowane, a co nie.

Teraz, gdy znamy już podstawy usługi Active Directory i lasów, możemy skonfigurować własne!

## Domeny podrzędne

Jak omówiliśmy w poprzednim zadaniu, chcemy skonfigurować nowe drzewo w naszym lesie dla działu bankowości. Mamy już domenę główną TryHackMe( `thm.loc`), a teraz chcemy utworzyć nową domenę zależną TryBankMe (TBM). W tym przypadku naszą domeną podrzędną będzie `tbm.thm.loc`. Nawiążmy połączenie RDP z serwerem, który awansujemy do roli kontrolera domeny, korzystając z poniższych danych logowania:

Referencje  

Nazwa użytkownika

Administrator

Hasło

zKGjt4iDckMQtT5TC8uZFwUL

Adres IP

192.168.10.110

Połączenie przez

RDP

xfreerdp /u:Administrator /p:zKGjt4iDckMQtT5TC8uZFwUL /d:THM.LOC /v:192.168.10.110 /dynamic-resolution

## Promocja domeny

Aby awansować ten serwer do roli kontrolera domeny, skorzystamy ze skryptu programu PowerShell udostępnionego w `C:\install-domain.ps1`, którego szczegółowy opis znajduje się poniżej:

```powershell
#DNS
$parentdcIPAddress = "192.168.10.100"

echo 'Configuring DNS...'
$adapters = Get-WmiObject Win32_NetworkAdapterConfiguration
if ($adapters) {
    $adapters | ForEach-Object {$_.SetDNSServerSearchOrder($parentdcIPAddress)}
}

#Password Reset
$domainAdministratorPassword = "childdomainftw1!"
$domainSafeModeAdministratorPassword = "childdomainftw1!"

echo 'Resetting the Administrator account password and settings...'
$localAdminPassword = ConvertTo-SecureString $domainAdministratorPassword -AsPlainText -Force
Set-LocalUser `
    -Name Administrator `
    -AccountNeverExpires `
    -Password $localAdminPassword `
    -PasswordNeverExpires:$true `
    -UserMayChangePassword:$true

$safeModePassword = ConvertTo-SecureString $domainSafeModeAdministratorPassword -AsPlainText -Force

#Parent Domain Credentials
$parentAdministratorPassword = "learningadisfun1!"
$parentName = "THM.LOC"

$parentPassword = ConvertTo-SecureString $parentAdministratorPassword -AsPlainText -Force
$parentDA =  $parentName + "\Administrator" 

echo 'Configuring the parent domain credentials'
$parentCredentials = New-Object System.Management.Automation.PSCredential($parentDA, $parentPassword)

#Tool Installation
echo 'Installing the AD services and administration tools...'
#Install-WindowsFeature AD-Domain-Services,RSAT-AD-AdminCenter,RSAT-ADDS-Tools

#Promoting to DC
$domainName = "tbm"
$domainNetbiosName = "TBM"
$parentFqdn = "thm.loc"

echo 'Installing the AD domain (be patient, this will take more than 5m to install)...'

Import-Module ADDSDeployment
Install-ADDSDomain `
    -Credential $parentCredentials `
    -NewDomainName $domainName `
    -SafeModeAdministratorPassword $safeModePassword `
    -CreateDnsDelegation:$true `
    -DatabasePath "C:\Windows\NTDS" `
    -DomainMode "6" `
    -NewDomainNetbiosName $domainNetbiosName `
    -InstallDns:$true `
    -NoRebootOnCompletion:$true `
    -Force:$true `
    -ParentDomainName $parentFqdn

echo 'Promotion complete! Restart required!'
```

Przyjrzyjmy się bliżej temu, co zrobi ten skrypt:

- **DNS:** Ten serwer będzie musiał komunikować się z istniejącym kontrolerem domeny. Można to zrobić, konfigurując adres IP ROOTDC jakoDNSdla tego serwera.
- **Resetowanie hasła:** Kiedy awansujemy serwer do roli kontrolera domeny, obecne konto administratora staje się kontem administratora nowej domeny. W związku z tym musimy już ustawić hasło dla tego konta.
- **Dane uwierzytelniające domeny nadrzędnej:** Aby awansować serwer, potrzebujemy uprawnień i uprawnień z domeny nadrzędnej. Musimy również utworzyć obiekt danych uwierzytelniających, używając konta administratora domeny nadrzędnej.
- **Instalacja narzędzi:** Aby promować serwer, wymagane są dodatkowe role i funkcje systemu Windows. To polecenie zostało jednak oznaczone komentarzem, ponieważ narzędzia zostały już zainstalowane.
- **Promocja doDC:** Po wykonaniu wszystkich kroków wstępnych nadszedł czas na awans serwera do roli kontrolera domeny. Udostępniamy mu dane uwierzytelniające do domeny nadrzędnej, a także kilka opcji konfiguracyjnych, takich jak miejsce instalacji bazy danych i nazwa nowej domeny ( `TBM`).

Teraz, gdy rozumiemy, co robi skrypt, możemy go uruchomić za pomocą programu PowerShell:

Terminal PowerShell

```powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\Administrator> C:\install-domain.ps1
```

Po zakończeniu skryptu należy ponownie uruchomić serwer, aby dokończyć proces, jak pokazano poniżej:

Terminal

```powershell
PS C:\Users\Administrator> Restart-Computer -Force
```

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Ponieważ właśnie awansowaliśmy ten serwer na nowy kontroler domeny, wprowadzenie konfiguracji może potrwać trochę czasu. Po ponownym uruchomieniu odczekaj co najmniej 5 minut przed ponownym uwierzytelnieniem hosta.

Jednak teraz, gdy utworzyliśmy nową domenę i kontroler domeny, musisz zmienić dane uwierzytelniające, których używasz do uwierzytelniania:

Referencje  

Nazwa użytkownika

Administrator

Hasło

domenapodrzędnaftw1!

Adres IP

192.168.10.110

Połączenie przez

RDP

xfreerdp /u:Administrator /p:'domenapodrzędnaftw1!' /d:TBM.THM.LOC /v:192.168.10.110 /dynamic-resolution

Kontroler domeny może nadal stosować zarówno zasady komputera, jak i użytkownika. Ten proces może potrwać kolejne 5 minut. Po jego zakończeniu zostaniesz uwierzytelniony na nowym kontrolerze domeny! Automatyczny skrypt wstępnie wypełniłby Twoją domenę. Przyjrzyjmy się temu i wyliczmy niektóre obiekty.

Odpowiedz na poniższe pytania

Po awansowaniu serwera do roli kontrolera domeny przejdź do systemu weryfikacji flag ( `http://192.168.10.250:5000`) i kliknij **„Zweryfikuj promocję domeny TBM”** , aby otrzymać flagę  `C:\flag1.txt`na CDC1. Co to jest flaga?

Answer the questions below

Once you have promoted the server to a domain controller, navigate to the flag verification system (`http://192.168.10.250:5000`) and click **Verify TBM Domain Promotion** to receive a flag in `C:\flag1.txt` on CDC1. What is the flag?

Twoim pierwszym zadaniem jako nowego administratora domeny organizacji TryBankMe jest sprawdzenie istniejącychOGŁOSZENIEJednostki organizacyjne i użytkownicy, ponieważ ostatnio zaszły zmiany w firmie. Tak jak na nadrzędnym kontrolerze domeny, otwórz panel **Użytkownicy i komputery usługi Active Directory** i do dzieła! Po otrzymaniu flagi w poprzednim zadaniu domena powinna zostać automatycznie wypełniona. Po otwarciu panelu Użytkownicy i komputery usługi Active Directory, domena powinna wyglądać mniej więcej tak:

![Panel Użytkownicy i komputery usługi Active Directory](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768332784412.png)

Zanim przejdziemy dalej, włącz **funkcje zaawansowane** w menu Widok:

![Włączanie zaawansowanych funkcji](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/15b282b6e3940f4c26c477a8c21f8266.png)

Spowoduje to wyświetlenie dodatkowych kontenerów i włączenie większej liczby opcji, takich jak usuwanie obiektów. Zapoznaj się ze strukturą tej domeny, przyglądając się bliżej jednostkom organizacyjnym ( OU) `Groups`i `People`. 

## Delegacja

Jedną z przydatnych funkcji w usłudze Active Directory jest przyznanie poszczególnym użytkownikom kontroli nad określonymi jednostkami organizacyjnymi (OU). Ten proces, znany jako  **delegowanie** , pozwala na przyznanie użytkownikom określonych uprawnień do wykonywania zaawansowanych zadań w jednostkach organizacyjnych bez konieczności interwencji administratora domeny.

Jednym z najczęstszych zastosowań jest nadawanie `IT support`uprawnień do resetowania haseł innym użytkownikom o niskich uprawnieniach. W domenie TryBankMe członkowie grupy wsparcia technicznego zapewniają wsparcie IT bankowcom, dlatego chcemy delegować kontrolę nad resetowaniem haseł dla jednostki `Bankers`organizacyjnej (OU) dowolnemu członkowi tej grupy.

W tym przykładzie delegujemy kontrolę nad`Bankers` Jednostka organizacyjnaAby `Tech Support`delegować kontrolę nad jednostką organizacyjną, kliknij ją prawym przyciskiem myszy i wybierz opcję **Deleguj kontrolę** :

![Deleguj kontrolę](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768332784588.png)

Powinno otworzyć się nowe okno, w którym najpierw zostaniesz poproszony o podanie użytkowników, którym chcesz delegować kontrolę.

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Aby uniknąć pomyłki w nazwie grupy, wpisz „tech” i kliknij  przycisk **„Sprawdź nazwy** ” . System Windows automatycznie uzupełni nazwę użytkownika.

![Sprawdź nazwy](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768332886705.png)

Kliknij OK i w następnym kroku wybierz opcję Resetuj hasła użytkowników i wymuś zmianę hasła przy następnym logowaniu :

![Delegowanie resetowania haseł](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/3f81df2b38e35ca5729aee7a76c6b220.png)

Kliknij **„Dalej”** kilka razy, a następnie **„Zakończ”** . Teraz każdy użytkownik grupy `Tech Support`powinien móc resetować hasła dla dowolnego użytkownika w dziale bankowości. Istnieje wiele uprawnień, które można delegować. Możesz je dowolnie modyfikować. Możesz nawet utworzyć niestandardowe zadanie do delegowania, co pozwala na niezwykle szczegółową kontrolę nad konfiguracją delegowania i obiektami, do których ma ono zastosowanie w ramach grupy.Jednostka organizacyjna.

## Komputery domenowe

TryBankMe kupił nowy serwer (Serwer1) i chce go dołączyć do domeny. Po dołączeniu komputera do domeny, usługi Active Directory mogą być używane do zarządzania tym komputerem i zapewniania do niego dostępu. Zachowaj swojeRDPsesja otwarta na kontrolerze domeny TBM, utwórzmy nowąRDPsesja do tego serwera:

Referencje  

Nazwa użytkownika

Administrator

Hasło

FwSA85KNn5R9pjxzZk7fmyjB

Adres IP

192.168.10.51

Połączenie przez

RDP

xfreerdp /u:Administrator /p:FwSA85KNn5R9pjxzZk7fmyjB /v:192.168.10.51 /dynamic-resolution

Ponownie skorzystamy ze skryptu, `C:\join-domain.ps1`aby przyłączyć ten serwer do naszej domeny, jak pokazano poniżej: 

```powershell
#DNS
$dcIPAddress = "192.168.10.110"

echo "Pointing DNS"
$adapters = Get-WmiObject Win32_NetworkAdapterConfiguration
if ($adapters) {
    $adapters | ForEach-Object {$_.SetDNSServerSearchOrder($dcIPAddress)}
}

#Credentials
$domainAdministratorPassword = "childdomainftw1!"
$domainNetbiosName = "tbm.thm.loc"

$securePassword = ConvertTo-SecureString $domainAdministratorPassword -AsPlainText -Force
$username = $domainNetbiosName + "\Administrator" 
$domainAdminCredentials = New-Object System.Management.Automation.PSCredential($username, $securePassword)

#Domain Joining
echo "Joining computer"
Add-Computer -DomainName $domainNetbiosName -Credential $domainAdminCredentials
echo "Computer Joined"
```

Przyjrzyjmy się trzem głównym krokom skryptu:

- **DNSPodobnie** jak w przypadku awansowania serwera do roli kontrolera domeny, musimy wskazać serwerowi, gdzie znaleźć kontroler domeny. Wskazując jegoDNSdo naszego nowego DC, będzie mógł nawiązać kontakt z naszą domeną.
- **Dane uwierzytelniające:** Nie każdy ma uprawnienia do dołączenia tego nowego serwera. Gdyby ktokolwiek mógł dołączyć komputer do Twojej domeny, stanowiłoby to poważne zagrożenie bezpieczeństwa. W związku z tym musimy podać skryptowi dane uwierzytelniające użytkownika usługi Active Directory, który ma uprawnienia do dołączenia tego komputera do domeny. Nie musi to być użytkownik administratora, ale zazwyczaj używane jest konto użytkownika o dość wysokich uprawnieniach.
- **Dołączanie do domeny:** Używając podanych danych uwierzytelniających, możemy poprosić serwer o nawiązanie kontaktu z kontrolerem domeny i dołączenie jej do domeny.

Teraz, gdy rozumiemy, co robi skrypt, wykonajmy go za pomocąPowerShell:

PowerShellTerminal

```powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\Administrator> C:\join-domain.ps1
```

Po zakończeniu skryptu należy ponownie uruchomić serwer, aby dokończyć proces, jak pokazano poniżej:

Terminal

```powershell
PS C:\Users\Administrator> Restart-Computer -Force
```

Ponieważ host został teraz dołączony doOGŁOSZENIEW przypadku domeny nie musimy już używać konta lokalnego do uwierzytelniania. Zamiast tego możemy użyć danych uwierzytelniających z naszej domeny:

Referencje  

Nazwa użytkownika

Administrator

Hasło

domenapodrzędnaftw1!

Adres IP

192.168.10.51

Połączenie przez

RDP

xfreerdp /u:Administrator /p:'domenapodrzędnaftw1!' /d:TBM.THM.LOC /v:192.168.10.51 /dynamic-resolution

W następnym zadaniu przyjrzymy się, jak możemy zarządzać tymi komputerami wOGŁOSZENIE.

Odpowiedz na poniższe pytania

Po dołączeniu hosta do domeny przejdź do systemu weryfikacji flag ( `http://192.168.10.250:5000`) i kliknij **„Zweryfikuj dołączenie do domeny Serwer1”** , aby otrzymać flagę `C:\flag2.txt`na Serwerze1. Czym jest ta flaga?

Wróćmy do kontrolera domeny TryBankMe. Domyślnie wszystkie komputery dołączające do domeny (z wyjątkiem kontrolerów domeny) są umieszczane wpojemnikNazywa się `Computers`. Jeśli sprawdzimy nasz DC, zobaczymy, że niektóre urządzenia już tam są:

![Urządzenia AD](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768333661167.png)

Widzimy kilka serwerów i laptopów odpowiadających użytkownikom w naszej sieci. Umieszczenie tam wszystkich naszych urządzeń nie jest najlepszym pomysłem, ponieważ prawdopodobnie chcesz zastosować inne zasady dla swoich serwerów i maszyn, z których korzystają codziennie zwykli użytkownicy.

Chociaż nie ma złotej zasady organizacji urządzeń, dobrym punktem wyjścia jest segregacja urządzeń według ich przeznaczenia. Generalnie można się spodziewać podziału urządzeń na co najmniej trzy następujące kategorie:

**Stacje robocze**

Stacje robocze to jedne z najpopularniejszych urządzeń w domenie Active Directory. Każdy użytkownik w domenie prawdopodobnie zaloguje się do stacji roboczej. To właśnie tego urządzenia będzie używać do pracy lub do przeglądania stron internetowych. Na tych urządzeniach nigdy nie powinien być zalogowany żaden użytkownik z uprawnieniami.

**Serwery**

Serwery są drugim najczęściej używanym urządzeniem w domenie Active Directory. Serwery są zazwyczaj wykorzystywane do świadczenia usług użytkownikom lub innym serwerom.

**Kontrolery domeny**

Kontrolery domeny to trzecie najczęściej używane urządzenia w domenie Active Directory. Umożliwiają one zarządzanie domeną Active Directory. Urządzenia te są często uważane za najbardziej wrażliwe urządzenia w sieci, ponieważ przechowują zaszyfrowane hasła do wszystkich kont użytkowników w danym środowisku.

Ponieważ porządkujemy naszą usługę AD, użyjmy osobnych jednostek organizacyjnych dla `Workstations`i `Servers`(kontrolery domeny znajdują się już w jednostce organizacyjnej utworzonej przez system Windows). Przeciągnij i upuść różne serwery z`Computers` Jednostka organizacyjnado `Servers`jednostki organizacyjnej, aż uzyskasz taką strukturę:

![Jednostki organizacyjne](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768333661178.png)

Teraz przenieś laptopy do`Workstations` Jednostka organizacyjnaDzięki temu będziemy mogli skonfigurować zasady dla każdegoJednostka organizacyjnapóźniej.

Do tej pory organizowaliśmy użytkowników i komputery w jednostki organizacyjne tylko dla zasady, ale głównym założeniem jest możliwość wdrażania różnych zasad dla każdej z nichJednostka organizacyjnaindywidualnie. W ten sposób możemy wdrażać różne konfiguracje i podstawowe poziomy bezpieczeństwa dla użytkowników, w zależności od ich działu.

System Windows zarządza takimi zasadami za pośrednictwem **obiektów zasad grupy (GPO)** . GPO to po prostu zbiór ustawień, które można zastosować do jednostek organizacyjnych. GPO mogą zawierać zasady skierowane do użytkowników lub komputerów, co pozwala na ustalenie punktu odniesienia dla konkretnych maszyn i tożsamości.

Aby skonfigurować obiekty zasad grupy, możesz skorzystać z narzędzia **Zarządzanie zasadami grupy** , dostępnego w menu Start:

![Menu startowe GPM](https://cdn-images.tryhackme.com/user-uploads/5ed5961c6276df568891c3ea/room-content/b19052c41e27fbbb2651038cede63e11.png)

Pierwszą rzeczą, którą zobaczysz po otwarciu, jest Twój kompletnyJednostka organizacyjnahierarchii, jak zdefiniowano wcześniej. Aby skonfigurować zasady grupy, najpierw utwórzGPOw  **Obiektach zasad grupy**  , a następnie połącz je zJednostka organizacyjnagdzie chcesz, aby zasady były stosowane. Na przykład, możesz zobaczyć, że na Twoim komputerze istnieją już pewne obiekty zasad grupy:

![Widok GPO](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1780398125506.png)

Powyższy obraz pokazuje, że utworzono 2 obiekty zasad grupy (GPO). Z nich obiekt GPO  `Default Domain Policy`jest powiązany z `tbm.thm.loc`całą domeną, a obiekt GPO `Default Domain Controllers Policy`jest powiązany tylko z `Domain Controllers`jednostką organizacyjną (OU). Należy pamiętać, że każdy obiekt GPO będzie miał zastosowanie do powiązanej jednostki organizacyjnej (OU) i wszystkich podjednostek organizacyjnych (OU) w jej obrębie. Na przykład:`Bankers` Jednostka organizacyjnanadal będzie podlegać wpływowi `Default Domain Policy`.

Przyjrzyjmy się, `Default Domain Policy`co znajduje się w obiekcie GPO. Pierwsza zakładka, którą zobaczysz po wybraniu obiektu GPO, pokazuje jego **zakres** , czyli miejsce, w którym obiekt GPO jest powiązany w usłudze Active Directory. W przypadku bieżącej polityki widać, że została ona powiązana tylko z `tbm.thm.loc`domeną:

![Widok GPO](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1780397886163.png)

Jak widać, można również zastosować **filtrowanie zabezpieczeń** do obiektów zasad grupy (GPO), aby były one stosowane tylko do określonych użytkowników/komputerów w danej jednostce organizacyjnej. Domyślnie będą one stosowane do grupy **„Użytkownicy uwierzytelnieni”** , która obejmuje wszystkich użytkowników/komputery.

Karta **Ustawienia** zawiera rzeczywistą zawartośćGPOi pokazuje nam, jakie konkretne konfiguracje stosuje. Jak wspomniano wcześniej, każdaGPOma konfiguracje, które dotyczą tylko komputerów i tylko użytkowników.

## Tworzenie administratorów lokalnych

TryBankMe chce zapewnić członkom grupy `Product Admins`możliwość wykonywania zadań administracyjnych na wszystkich serwerach. Oznacza to, że musimy upewnić się, że `Product Admins`grupa zostanie dodana do grupy lokalnej `Administrators`na wszystkich serwerach w jednostce organizacyjnej ( `Servers`OU). Utwórzmy nowy obiekt GPO, aby przesłać tę konfigurację. Kliknij prawym przyciskiem myszy`Servers` Jednostka organizacyjna, a następnie kliknij **UtwórzGPOw tej domenie i umieść tutaj link do niej** .

![Tworzenie administratorów lokalnych](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334219473.png)

DajGPOnazwę, kliknij OK, a następnie kliknij prawym przyciskiem myszy nowo utworzoną nazwę GPO Aby to edytować :

![Edytuj GPO](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334220581.png)

Zmiana, którą chcemy wprowadzić, musi dotyczyć obiektów typu Komputer. W związku z tym musimy zmodyfikować **konfigurację komputera** wGPOPrzejdź do **Konfiguracja komputera** -> **Zasady** -> **Ustawienia systemu Windows** -> **Ustawienia zabezpieczeń** -> **Grupy z ograniczeniami** . Tutaj możemy kliknąć prawym przyciskiem myszy, aby dodać nową grupę:

![Ograniczone grupy](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334543431.png)

Używając opcji Przeglądaj , wpisz „Produkt”, a następnie kliknij opcję **Sprawdź nazwy** , aby wyszukać `Product Admins`grupę:

![Sprawdź nazwy administratorów produktów](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334543264.png)

Kliknij **OK** . Teraz możemy określić, co `Product Admins`ma zostać dodane do `Administrators`grupy, jak pokazano poniżej:

![Administratorzy produktu Administratorzy lokalni](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334543419.png)

Kliknij **OK** , a Twój obiekt zasad grupy zostanie skonfigurowany:

![Obiekt zasad grupy administratorów produktu](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768334543588.png)

Sprawdźmy, czy nasz GPO został zastosowany!

## Dystrybucja GPO

Obiekty zasad grupy (GPO) są dystrybuowane do sieci za pośrednictwem udziału sieciowego o nazwie `SYSVOL`, który jest przechowywany w kontrolerze domeny (DC). Wszyscy użytkownicy w domenie powinni zazwyczaj mieć dostęp do sieci, aby okresowo synchronizować swoje obiekty zasad grupy. Domyślnie udział SYSVOL wskazuje na `C:\Windows\SYSVOL\sysvol\`katalog w każdymDCw naszej sieci.

Po wprowadzeniu zmian w obiektach zasad grupy (GPO), komputery mogą potrzebować do 2 godzin, aby je zsynchronizować. Jeśli chcesz wymusić natychmiastową synchronizację obiektów zasad grupy na danym komputerze, możesz zawsze uruchomić na nim następujące polecenie:

Windows PowerShell

```shell-session
PS C:\> gpupdate /force
```

Aby sprawdzić, czy nasz obiekt zasad grupy został zastosowany, uruchom to polecenie na serwerze Server1. Po jego wykonaniu możesz użyć następujących danych logowania, aby nawiązać połączenie RDP z serwerem Server1 jako członek grupy Product Admins:

Referencje  

Nazwa użytkownika

tbm.thm.loc\terry.fox

Hasło

nACFhAsbA1Xv

Adres IP

192.168.10.51

Połączenie przez

RDP

xfreerdp /u:terry.fox /p:nACFhAsbA1Xv /d:TBM.THM.LOC /v:192.168.10.51 /dynamic-resolution

Jeśli GPO zostało zastosowane, `terry.fox`konto będzie mogłoRDPdo Serwera1.

## Wypróbuj Sprzedawcę

TryHackMe zdecydowało się nawiązać partnerstwo z TryVendorMe. W ramach tego partnerstwa niektórzy członkowie TryHackMe potrzebują dostępu do zasobów w domenie TryVendorMe i odwrotnie. Zanim będziemy mogli udzielić dostępu do tych zasobów, musimy najpierw nawiązać zaufanie między dwoma lasami.

Zacznij od uwierzytelnienia się w kontrolerze domeny TryVendorMe:

Referencje  

Nazwa użytkownika

Administrator

Hasło

kolejnylas1!

Adres IP

192.168.10.120

Połączenie przez

RDP

xfreerdp /u:Administrator /p:'anotherforest1!' /d:TVM.LOC /v:192.168.10.120 /dynamic-resolution

Po uwierzytelnieniu przyjrzyjmy się ustanowieniu zaufania między dwoma lasami. Kliknij Start i wyszukaj „Zaufanie”:

![Menu startowe domen i relacji zaufania AD](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768265852514.png)

Otwórz **domeny i relacje zaufania usługi Active Directory** :

![Panel domen i zaufania AD](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768265888203.png)

Kliknij prawym przyciskiem myszy `tvm.loc`domenę i wybierz **Właściwości** , a następnie **Zaufanie** . Kliknij przycisk **Nowe zaufanie** :

![Nowy Panel Zaufania](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768265931398.png)

Kliknij **Dalej** na pierwszym ekranie, a następnie podaj nazwę domeny `thm.loc`:

![Nowy kreator zaufania](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768265973840.png)

Wybierz opcję **Forest Trust** , ponieważ kontrolujemy oba lasy:

![Kreator typów zaufania](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266084152.png)

Ponieważ zasoby muszą być udostępniane w obu kierunkach, musimy skonfigurować **dwukierunkową** relację zaufania:

![Zaufanie dwustronne](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266064647.png)

Ponieważ mamy już dane uwierzytelniające domeny TryHackMe, wybierz opcję konfiguracji relacji zaufania dla obu domen:

![Kreator Stron Zaufania](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266234716.png)

Podaj dane uwierzytelniające dla domeny TryHackMe ( `Administrator`: `learningadisfun1!`) i wybierz metodę **uwierzytelniania w całym lesie** dwukrotnie dla obu domen:

![Konfiguracja uwierzytelniania w całym lesie](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266234738.png)

Po zakończeniu kliknij **Dalej** ,  aby skonfigurować zaufanie:

![Wybór zaufania zakończony](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266234719.png)

Wybierz opcję potwierdzenia **zarówno zaufania wychodzącego, jak i przychodzącego** :

![Potwierdź zaufanie wychodzące](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266544353.png)

Po potwierdzeniu powinieneś zobaczyć następujące informacje:

![Kreator zakończeń](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266544340.png)

## Udostępnianie zasobów

Teraz, gdy nasza relacja zaufania została ustanowiona, możemy udostępniać zasoby. Na kontrolerze domeny TVM otwórz „ **Użytkownicy i komputery usługi Active Directory”** i wyszukaj `Groups`jednostkę organizacyjną (OU):

![Grupy reklam](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266544374.png)

Chcemy przyznać `Claire`dostęp administracyjny z TryHackMe do Serwera 2. Skonfigurujmy to, dodając konto do  `Server Admins`grupy. Kliknij prawym przyciskiem myszy tę grupę i wybierz **Właściwości** :

 ![Dodaj do administratorów serwera](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768266544346.png)

Na karcie **Członkowie** kliknij  przycisk **Dodaj** :

![Dodaj członków do grupy](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1780398727764.png)

W polu tekstowym dodaj konto Claire, używając „THM\Claire”, a następnie wybierz opcję  „Sprawdź nazwy” . Musisz podać THM\, aby wskazać, że Claire nie należy do domeny TVM:

![Dodaj Claire przez Panel Członków](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1783403269337.png)

Kliknij **OK** , a następnie ponownie **OK** , a konto Claire zostanie dodane. Teraz, gdy  `Claire`jest administratorem serwera w domenie TryVendorMe, konto może zostać użyte do uwierzytelnienia przy `Server2`użyciu następujących danych logowania:

Referencje  

Nazwa użytkownika

THM\Claire

Hasło

learningadisfun1!

Adres IP

192.168.10.52

Połączenie przez

RDP

xfreerdp /u:Claire /p:'learningadisfun1!' /d:THM.LOC /v:192.168.10.52 /dynamic-resolution

## Dwukierunkowe zaufanie

Jak wspomniano wcześniej, utworzyliśmy dwukierunkową relację zaufania między domenami tvm.loc i thm.loc. Jednak biorąc pod uwagę, że thm.loc i tbm.thm.loc należą do tego samego lasu w konfiguracji nadrzędny-podrzędny, to zaufanie rozciąga się teraz również na  domeny `tvm.loc`i `tbm.thm.loc`.

Korzystając z sesji RDP w kontrolerze domeny TBM, sprawdźmy to w sekcji Użytkownicy i komputery usługi Active Directory, dodając  `alice.king`konto do `Product Admins`grupy. Zacznijmy od potwierdzenia, że `tvm.loc`​​domena jest widoczna w TBM. Kliknij prawym przyciskiem myszy `tbm.thm.loc`, wybierz opcję **Zmień domenę** i zmień ją na `tvm.loc`:

![Zmień domenę](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768268008446.png)

Umożliwi to podgląd całej `tvm.loc`domeny bezpośrednio z kontrolera domeny TBM. Zmień domenę z powrotem na `tbm.thm.loc`i dodaj `tvm\alice.king`do `Product Admins`grupy, korzystając z tego samego kroku, który wykonaliśmy poprzednio: **Właściwości** -> **Członkowie** -> **Dodaj :**

![Dodaj Alicję Królową](https://cdn-images.tryhackme.com/user-uploads/6241db5522713b00497f96ac/room-content/6241db5522713b00497f96ac-1783425564243.png)

Po dodaniu powinno wyglądać to tak:

![Członkostwo w grupie Alicji King](https://cdn-images.tryhackme.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1768268008454.png)

Kliknij **OK**  , aby zastosować zmianę. Biorąc pod uwagę, że w poprzednim zadaniu skonfigurowaliśmy obiekt zasad grupy (GPO) w celu nadania wszystkim  `Product Admins`lokalnym uprawnieniom administratora na serwerach, `alice.king`konto powinno teraz móc się uwierzytelniać `Server1`. Cofnijmy się o krok i podziwiajmy, jak bardzo możemy ze sobą łączyć elementy w usłudze Active Directory:

1. Konto `alice.king`jest zarządzane w `tvm.loc`domenie.
2. `tvm.loc`Pomiędzy lasami oraz istnieje dwukierunkowe zaufanie `thm.loc`.
3. Biorąc pod uwagę, że `tbm.thm.loc`jest to domena podrzędna `thm.loc`, istnieje wewnętrzne obustronne zaufanie między tymi domenami w `thm.loc`lesie.
4. Oznacza to, że istnieje dwukierunkowe zaufanie między użytkownikiem `tvm.loc`a użytkownikiem `tbm.thm.loc`, co pozwala nam uczynić `alice.king`konto członkiem grupy `Product Admins`.
5. Grupa `Product Admins`jest zarządzana w `tbm.thm.loc`domenie, `Server1`która znajduje się w `Servers`jednostce organizacyjnej domeny `tbm.thm.loc`, w której skonfigurowano obiekt zasad grupy (GPO) w celu udzielenia `Product Admins`uprawnień administratora lokalnego wszystkim komputerom w tej jednostce organizacyjnej.
6. Dlatego `alice.king`od `tvm.loc`tej pory konto będzie posiadało lokalne uprawnienia administracyjne `Server1`!

Sprawdźmy to, uwierzytelniając się na serwerze Server1 przy użyciu `alice.king`konta:

Referencje  

Nazwa użytkownika

TVM\alice.king

Hasło

Rhtv7924

Adres IP

192.168.10.51

Połączenie przez

RDP

xfreerdp /u:alice.king /p:Rhtv7924 /d:TVM.LOC /v:192.168.10.51 /dynamic-resolution

W tej sali omówiliśmy podstawowe komponenty i koncepcje Active Directory oraz domen Windows. Należy pamiętać, że ta sala powinna służyć jedynie jako wprowadzenie do podstawowych koncepcji, ponieważ jest jeszcze wiele do omówienia, aby wdrożyć środowisko Active Directory gotowe do produkcji.

Jeśli chcesz dowiedzieć się, jak zabezpieczyć instalację Active Directory, koniecznie zajrzyj na stronę [Active Directory Hardening Room](https://tryhackme.com/room/activedirectoryhardening) . Jeśli natomiast chcesz dowiedzieć się, jak atakujący mogą wykorzystać powszechneOGŁOSZENIEbłędne konfiguracje i inneOGŁOSZENIEJeśli chodzi o techniki hakerskie, [moduł Compromising Active Directory](https://tryhackme.com/module/hacking-active-directory) jest najlepszym rozwiązaniem.
