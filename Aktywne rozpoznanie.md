---

W pierwszej sali modułu bezpieczeństwa sieci skupiliśmy się na [rozpoznaniu pasywnym](https://tryhackme.com/jr/passiverecon) . W drugiej sali skupimy się na rozpoznaniu aktywnym i niezbędnych narzędziach z nim związanych. Nauczymy się korzystać z przeglądarki internetowej, aby zebrać więcej informacji o naszym celu. Ponadto omówimy użycie prostych narzędzi, takich jak `ping`, `traceroute`, `telnet`i , `nc`do gromadzenia informacji o sieci, systemie i usługach.

Jak dowiedzieliśmy się w poprzedniej sali, pasywny rekonesans pozwala zebrać informacje o celu bez bezpośredniego zaangażowania czy kontaktu. Obserwujesz z daleka lub sprawdzasz publicznie dostępne informacje.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f8b6de84195f6ce2a517b8985497e80f.png)

Aktywny rekonesans wymaga nawiązania kontaktu z celem. Kontakt ten może polegać na rozmowie telefonicznej lub wizycie w firmie docelowej pod pretekstem zebrania dodatkowych informacji, zazwyczaj w ramach socjotechniki. Alternatywnie, może to być bezpośrednie połączenie z systemem docelowym, np. odwiedzenie jego strony internetowej lub sprawdzenie, czy zapora sieciowa ma otwarty port SSH. Wyobraź sobie, że dokładnie sprawdzasz okna i zamki w drzwiach. Dlatego pamiętaj, aby nie podejmować aktywnego rekonesansu bez uzyskania pisemnego upoważnienia prawnego od klienta.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/cfe90ebdead91f2a1abd30833b22b001.png)

W tym pomieszczeniu skupiamy się na aktywnym rozpoznaniu. Aktywny rozpoznanie rozpoczyna się od nawiązania bezpośrednich połączeń z maszyną docelową. Każde takie połączenie może pozostawić w logach informacje, takie jak adres IP klienta, godzina połączenia i jego czas trwania, między innymi. Jednak nie wszystkie połączenia są podejrzane. Możliwe jest, aby aktywny rozpoznanie było postrzegane jako zwykła aktywność klienta. Rozważmy przeglądanie stron internetowych; nikt nie podejrzewałby przeglądarki połączonej z docelowym serwerem wśród setek innych uprawnionych użytkowników. Możesz wykorzystać takie techniki na swoją korzyść, działając w ramach drużyny czerwonej (atakującej) i nie chcąc alarmować drużyny niebieskiej (obrończej).

W tej sali omówimy różne narzędzia powszechnie dołączane do większości systemów operacyjnych lub łatwo dostępne. Zaczniemy od przeglądarki internetowej i jej wbudowanych narzędzi programistycznych; ponadto pokażemy, jak można „uzbroić” przeglądarkę internetową, aby stała się skutecznym narzędziem rozpoznania. Następnie omówimy inne, nieszkodliwe narzędzia, takie jak `ping`, `traceroute`i `telnet`. Wszystkie te programy wymagają połączenia z celem, a zatem nasze działania będą zaliczane do aktywnego rozpoznania.

Ten pokój jest interesujący dla każdego, kto chce zapoznać się z podstawowymi narzędziami i zobaczyć, jak można je wykorzystać w aktywnym rozpoznaniu. Zapoznanie się z narzędziami programistycznymi w przeglądarce internetowej może wymagać pewnego wysiłku, mimo że oferują one graficzny interfejs użytkownika. Omówione narzędzia wiersza poleceń są stosunkowo proste w obsłudze.

Przeglądarka internetowa może być wygodnym narzędziem, zwłaszcza że jest łatwo dostępna we wszystkich systemach. Istnieje kilka sposobów, w jakie można użyć przeglądarki internetowej do zebrania informacji o celu.

Na poziomie transportu przeglądarka łączy się z:

- Domyślnie port TCP 80, gdy dostęp do witryny odbywa się przez HTTP
- Domyślnie port TCP 443, gdy dostęp do witryny odbywa się przez HTTPS

Ponieważ porty 80 i 443 są domyślnymi portami dla protokołów HTTP i HTTPS, przeglądarka internetowa nie wyświetla ich w pasku adresu. Możliwe jest jednak użycie niestandardowych portów w celu uzyskania dostępu do usługi. Na przykład https://127.0.0.1:8834/ połączy się z adresem 127.0.0.1 (localhost) na porcie 8834 za pośrednictwem protokołu HTTPS. Jeśli na tym porcie nasłuchuje serwer HTTPS, otrzymamy stronę internetową.

Podczas przeglądania strony internetowej możesz nacisnąć klawisz `Ctrl+Shift+I`na komputerze PC lub `Option + Command + I`( `⌥ + ⌘ + I`) na komputerze Mac, aby otworzyć Narzędzia programistyczne w przeglądarce Firefox. Podobne skróty klawiszowe umożliwiają również rozpoczęcie pracy w przeglądarkach Google Chrome i Chromium. Narzędzia programistyczne pozwalają na sprawdzenie wielu informacji, które przeglądarka otrzymała i wymieniła ze zdalnym serwerem. Na przykład, możesz przeglądać, a nawet modyfikować pliki JavaScript (JS), sprawdzać pliki cookie ustawione w systemie i odkrywać strukturę folderów zawartości witryny.

Poniżej znajduje się zrzut ekranu z Firefox Developer Tools. Chrome DevTools jest dość podobny.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/02722e27a2e85fa803c2baa52ab54fdf.png)

Istnieje również wiele dodatków do przeglądarek Firefox i Chrome, które mogą pomóc w testach penetracyjnych. Oto kilka przykładów:

- **FoxyProxy** pozwala szybko zmienić serwer proxy używany do dostępu do docelowej witryny. To rozszerzenie przeglądarki jest wygodne, gdy korzystasz z narzędzia takiego jak Burp Suite lub gdy musisz regularnie zmieniać serwery proxy . Możesz pobrać FoxyProxy dla Firefoksa [tutaj](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard) .
- **User-Agent Switcher and Manager** umożliwia udawanie, że korzystasz ze strony internetowej z innego systemu operacyjnego lub innej przeglądarki. Innymi słowy, możesz udawać, że przeglądasz stronę za pomocą iPhone'a, podczas gdy w rzeczywistości korzystasz z przeglądarki Mozilla Firefox. Możesz pobrać User-Agent Switcher and Manager dla przeglądarki Firefox [tutaj](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher) .
- **Wappalyzer** dostarcza informacji o technologiach wykorzystywanych na odwiedzanych stronach internetowych. To rozszerzenie jest przydatne, zwłaszcza gdy zbierasz te informacje podczas przeglądania strony internetowej, jak każdy inny użytkownik. Zrzut ekranu Wappalyzera znajduje się poniżej. Wappalyzer dla przeglądarki Firefox znajdziesz [tutaj](https://addons.mozilla.org/en-US/firefox/addon/wappalyzer) .

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d8db9b9e278502db5ae2a6c12e79d890.png)

Z czasem możesz znaleźć kilka rozszerzeń, które idealnie dopasują się do Twojego sposobu pracy.

Ping powinien przypominać grę w ping-ponga (tenisa stołowego). Rzucasz piłeczkę i oczekujesz, że ją odzyskasz. Głównym celem pinga jest sprawdzenie, czy możesz połączyć się ze zdalnym systemem i czy zdalny system może się z Tobą skontaktować. Innymi słowy, początkowo ping służył do sprawdzania połączenia sieciowego; jednak nas bardziej interesują jego różne zastosowania: sprawdzanie, czy zdalny system jest online.

Mówiąc najprościej, polecenie ping wysyła pakiet do systemu zdalnego, a system zdalny odpowiada. W ten sposób można stwierdzić, że system zdalny jest online i że sieć między nimi działa.

Jeśli wolisz bardziej precyzyjną definicję, ping to polecenie wysyłające pakiet ICMP Echo do zdalnego systemu. Jeśli zdalny system jest online, a pakiet ping został poprawnie przekierowany i nie został zablokowany przez żadną zaporę sieciową , zdalny system powinien odesłać odpowiedź ICMP Echo. Podobnie, odpowiedź ping powinna dotrzeć do pierwszego systemu, jeśli została poprawnie przekierowana i nie została zablokowana przez żadną zaporę sieciową .

Celem takiego polecenia jest upewnienie się, że system docelowy jest online zanim poświęcimy czas na przeprowadzenie bardziej szczegółowych skanów w celu wykrycia działającego systemu operacyjnego i usług.

W terminalu AttackBox możesz zacząć używać polecenia ping jako `ping MACHINE_IP`lub `ping HOSTNAME`. W tym drugim przypadku system musi przekształcić nazwę hosta (HOSTNAME) na adres IP przed wysłaniem pakietu ping. Jeśli nie określisz liczby pakietów w systemie Linux, będziesz musiał nacisnąć przycisk , `CTRL+c`aby wymusić zatrzymanie. Dlatego warto rozważyć `ping -c 10 MACHINE_IP`wysłanie tylko dziesięciu pakietów. Jest to odpowiednik `ping -n 10 MACHINE_IP`w systemie MS Windows.

Technicznie rzecz biorąc, ping podlega protokołowi ICMP (Internet Control Message Protocol). ICMP obsługuje wiele typów zapytań, ale w szczególności interesują nas ping (ICMP echo/typ 8) i ping reply (ICMP echo reply/typ 0). Do korzystania z pinga nie jest wymagane zapoznanie się ze szczegółami protokołu ICMP.

W poniższym przykładzie określiliśmy całkowitą liczbę pakietów na 5. Z terminala AttackBoxa uruchomiliśmy pingowanie `MACHINE_IP`. Dowiedzieliśmy się, że `MACHINE_IP`jest aktywny i nie blokuje żądań echa ICMP. Co więcej, żadne zapory sieciowe ani routery na trasie pakietów również nie blokują żądań echa ICMP.

Terminal AttackBox

```shell-session
user@AttackBox$ ping -c 5 MACHINE_IP
PING MACHINE_IP (MACHINE_IP) 56(84) bytes of data.
64 bytes from MACHINE_IP: icmp_seq=1 ttl=64 time=0.636 ms
64 bytes from MACHINE_IP: icmp_seq=2 ttl=64 time=0.483 ms
64 bytes from MACHINE_IP: icmp_seq=3 ttl=64 time=0.396 ms
64 bytes from MACHINE_IP: icmp_seq=4 ttl=64 time=0.416 ms
64 bytes from MACHINE_IP: icmp_seq=5 ttl=64 time=0.445 ms

--- MACHINE_IP ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4097ms
rtt min/avg/max/mdev = 0.396/0.475/0.636/0.086 ms
```

W powyższym przykładzie wyraźnie widzieliśmy, że system docelowy odpowiada. Wynik polecenia ping wskazuje, że jest on online i osiągalny. Wysłaliśmy pięć pakietów i otrzymaliśmy pięć odpowiedzi. Zauważyliśmy, że średnio odpowiedź docierała do naszego systemu w ciągu 0,475 ms (milisekundy), a maksymalny czas wynosił 0,636 ms.  

Z punktu widzenia testów penetracyjnych postaramy się dowiedzieć więcej o tym celu. Postaramy się dowiedzieć jak najwięcej, na przykład, które porty są otwarte i które usługi działają.

Rozważmy następujący przypadek: wyłączamy docelową maszynę wirtualną i próbujemy wysłać polecenie ping `MACHINE_IP`. Jak można się spodziewać w poniższym przykładzie, nie otrzymujemy żadnej odpowiedzi.

Terminal AttackBox

```shell-session
user@AttackBox$ ping -c 5 MACHINE_IP
PING MACHINE_IP (MACHINE_IP) 56(84) bytes of data.
From ATTACKBOX_IP icmp_seq=1 Destination Host Unreachable
From ATTACKBOX_IP icmp_seq=2 Destination Host Unreachable
From ATTACKBOX_IP icmp_seq=3 Destination Host Unreachable
From ATTACKBOX_IP icmp_seq=4 Destination Host Unreachable
From ATTACKBOX_IP icmp_seq=5 Destination Host Unreachable

--- MACHINE_IP ping statistics ---
5 packets transmitted, 0 received, +5 errors, 100% packet loss, time 4098ms
pipe 4
```

W tym przypadku wiemy już, że wyłączyliśmy komputer docelowy o adresie MACHINE_IP. Na każde polecenie ping system, którego używamy, w tym przypadku AttackBox, odpowiada komunikatem „Host docelowy niedostępny”. Widzimy, że przesłaliśmy pięć pakietów, ale żaden nie został odebrany, co spowodowało 100% utratę pakietów.  

Mówiąc ogólnie, gdy nie otrzymamy odpowiedzi na polecenie ping, istnieje kilka przyczyn, które mogłyby wyjaśnić, dlaczego tak się stało, na przykład:

- Komputer docelowy nie reaguje; prawdopodobnie nadal się uruchamia lub jest wyłączony, bądź też system operacyjny uległ awarii.
- Urządzenie jest odłączone od sieci lub na ścieżce znajduje się uszkodzone urządzenie sieciowe.
- Zapora sieciowa jest skonfigurowana tak, aby blokować takie pakiety. Zapora może być oprogramowaniem działającym w samym systemie lub oddzielnym urządzeniem sieciowym. Należy pamiętać, że zapora sieciowa systemu MS Windows domyślnie blokuje ping.
- Twój system jest odłączony od sieci.
### Traceroute

Jak sama nazwa wskazuje, polecenie #traceroute _śledzi trasę_ pakietów z Twojego systemu do innego hosta. Celem polecenia traceroute jest znalezienie adresów IP routerów lub przeskoków, które pakiet pokonuje w drodze z Twojego systemu do hosta docelowego. To polecenie ujawnia również liczbę routerów między dwoma systemami. Jest to pomocne, ponieważ wskazuje liczbę przeskoków (routerów) między Twoim systemem a hostem docelowym. Należy jednak pamiętać, że trasa pakietów może się zmieniać, ponieważ wiele routerów korzysta z dynamicznych protokołów routingu, które dostosowują się do zmian w sieci.

W systemach Linux i macOS należy użyć polecenia `traceroute MACHINE_IP`, a w systemie MS Windows `tracert MACHINE_IP`. polecenie to `traceroute`próbuje wykryć routery na ścieżce łączącej Twój system z systemem docelowym.

Nie ma bezpośredniego sposobu na odkrycie ścieżki od Twojego systemu do systemu docelowego. Polegamy na protokole ICMP, aby „oszukać” routery i wymusić ujawnienie ich adresów IP. Możemy to osiągnąć, używając małego czasu życia (TTL) w polu nagłówka IP. Chociaż T w TTL oznacza czas, TTL wskazuje maksymalną liczbę routerów/skoków, przez które pakiet może przejść, zanim zostanie porzucony; TTL nie jest maksymalną liczbą jednostek czasu. Gdy router odbiera pakiet, zmniejsza TTL o jeden przed przekazaniem go do następnego routera. Poniższy rysunek pokazuje, że za każdym razem, gdy pakiet IP przechodzi przez router, jego wartość TTL jest zmniejszana o 1. Początkowo opuszcza system z wartością TTL równą 64; dociera do systemu docelowego z wartością TTL równą 60 po przejściu przez 4 routery.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/e82c42dcfae78ac592a8d7843465d2d6.png)

Jeśli jednak TTL osiągnie 0, zostanie odrzucony, a do pierwotnego nadawcy zostanie wysłany komunikat ICMP Time-to-Live (przekroczony czas życia) (TTL). Na poniższym rysunku system ustawił TTL na 1 przed wysłaniem go do routera. Pierwszy router na ścieżce zmniejsza TTL o 1, co daje wartość TTL równą 0. W rezultacie router ten odrzuci pakiet i wyśle ​​komunikat o błędzie ICMP Time-to-Live (przekroczony czas życia) (ITL). Należy pamiętać, że niektóre routery są skonfigurowane tak, aby nie wysyłać takich komunikatów ICMP podczas odrzucania pakietu.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/948388c823b156813fa30225c2fa3f05.png)

W systemie Linux `traceroute`rozpocznie się od wysyłania datagramów UDP w pakietach IP o TTL równym 1. Spowoduje to, że pierwszy router napotka TTL = 0 i odeśle komunikat ICMP o przekroczonym czasie życia (TTL). Zatem TTL równy 1 ujawni adres IP pierwszego routera. Następnie wyśle ​​on kolejny pakiet o TTL = 2; ten pakiet zostanie odrzucony na drugim routerze. I tak dalej. Wypróbujmy to na działających systemach.

W poniższych przykładach uruchamiamy to samo polecenie `traceroute tryhackme.com`z AttackBoxa TryHackMe. Zauważamy, że różne uruchomienia mogą prowadzić do różnych tras wybieranych przez pakiety.

Traceroute A

Terminal AttackBox - Traceroute A

```shell-session
user@AttackBox$ traceroute tryhackme.com
traceroute to tryhackme.com (172.67.69.208), 30 hops max, 60 byte packets
 1  ec2-3-248-240-5.eu-west-1.compute.amazonaws.com (3.248.240.5)  2.663 ms * ec2-3-248-240-13.eu-west-1.compute.amazonaws.com (3.248.240.13)  7.468 ms
 2  100.66.8.86 (100.66.8.86)  43.231 ms 100.65.21.64 (100.65.21.64)  18.886 ms 100.65.22.160 (100.65.22.160)  14.556 ms
 3  * 100.66.16.176 (100.66.16.176)  8.006 ms *
 4  100.66.11.34 (100.66.11.34)  17.401 ms 100.66.10.14 (100.66.10.14)  23.614 ms 100.66.19.236 (100.66.19.236)  17.524 ms
 5  100.66.7.35 (100.66.7.35)  12.808 ms 100.66.6.109 (100.66.6.109)  14.791 ms *
 6  100.65.14.131 (100.65.14.131)  1.026 ms 100.66.5.189 (100.66.5.189)  19.246 ms 100.66.5.243 (100.66.5.243)  19.805 ms
 7  100.65.13.143 (100.65.13.143)  14.254 ms 100.95.18.131 (100.95.18.131)  0.944 ms 100.95.18.129 (100.95.18.129)  0.778 ms
 8  100.95.2.143 (100.95.2.143)  0.680 ms 100.100.4.46 (100.100.4.46)  1.392 ms 100.95.18.143 (100.95.18.143)  0.878 ms
 9  100.100.20.76 (100.100.20.76)  7.819 ms 100.92.11.36 (100.92.11.36)  18.669 ms 100.100.20.26 (100.100.20.26)  0.842 ms
10  100.92.11.112 (100.92.11.112)  17.852 ms * 100.92.11.158 (100.92.11.158)  16.687 ms
11  100.92.211.82 (100.92.211.82)  19.713 ms 100.92.0.126 (100.92.0.126)  18.603 ms 52.93.112.182 (52.93.112.182)  17.738 ms
12  99.83.69.207 (99.83.69.207)  17.603 ms  15.827 ms  17.351 ms
13  100.92.9.83 (100.92.9.83)  17.894 ms 100.92.79.136 (100.92.79.136)  21.250 ms 100.92.9.118 (100.92.9.118)  18.166 ms
14  172.67.69.208 (172.67.69.208)  17.976 ms  16.945 ms 100.92.9.3 (100.92.9.3)  17.709 ms
```

W powyższym wyniku polecenia traceroute mamy 14 ponumerowanych wierszy; każdy wiersz reprezentuje jeden router/skok. Nasz system wysyła trzy pakiety z TTL ustawionym na 1, następnie trzy pakiety z TTL ustawionym na 2 i tak dalej. W zależności od topologii sieci, możemy otrzymać odpowiedzi od nawet 3 różnych routerów, w zależności od trasy obranej przez pakiet. Rozważmy wiersz numer 12 – dwunasty router z wymienionym adresem IP trzykrotnie odrzucił pakiet i wysłał komunikat ICMP o przekroczeniu czasu transmisji. Wiersz `12 99.83.69.207 (99.83.69.207) 17.603 ms 15.827 ms 17.351 ms`pokazuje czas w milisekundach, jaki upływa, zanim każda odpowiedź dotrze do naszego systemu.

Z drugiej strony, widzimy, że otrzymaliśmy tylko jedną odpowiedź w trzecim wierszu. Dwie gwiazdki w wynikach `3 * 100.66.16.176 (100.66.16.176) 8.006 ms *`wskazują, że nasz system nie otrzymał dwóch oczekiwanych komunikatów ICMP o przekroczeniu czasu transmisji.

Wreszcie, w pierwszym wierszu wyników, widzimy, że pakiety opuszczające AttackBox podążają różnymi trasami. Widzimy dwa routery, które odpowiedziały, że TTL jest jeden. Nasz system nigdy nie otrzymał trzeciego oczekiwanego komunikatu ICMP.

Traceroute B

Terminal AttackBox - Traceroute B

```shell-session
user@AttackBox$ traceroute tryhackme.com
traceroute to tryhackme.com (104.26.11.229), 30 hops max, 60 byte packets
 1  ec2-79-125-1-9.eu-west-1.compute.amazonaws.com (79.125.1.9)  1.475 ms * ec2-3-248-240-31.eu-west-1.compute.amazonaws.com (3.248.240.31)  9.456 ms
 2  100.65.20.160 (100.65.20.160)  16.575 ms 100.66.8.226 (100.66.8.226)  23.241 ms 100.65.23.192 (100.65.23.192)  22.267 ms
 3  100.66.16.50 (100.66.16.50)  2.777 ms 100.66.11.34 (100.66.11.34)  22.288 ms 100.66.16.28 (100.66.16.28)  4.421 ms
 4  100.66.6.47 (100.66.6.47)  17.264 ms 100.66.7.161 (100.66.7.161)  39.562 ms 100.66.10.198 (100.66.10.198)  15.958 ms
 5  100.66.5.123 (100.66.5.123)  20.099 ms 100.66.7.239 (100.66.7.239)  19.253 ms 100.66.5.59 (100.66.5.59)  15.397 ms
 6  * 100.66.5.223 (100.66.5.223)  16.172 ms 100.65.15.135 (100.65.15.135)  0.424 ms
 7  100.65.12.135 (100.65.12.135)  0.390 ms 100.65.12.15 (100.65.12.15)  1.045 ms 100.65.14.15 (100.65.14.15)  1.036 ms
 8  100.100.4.16 (100.100.4.16)  0.482 ms 100.100.20.122 (100.100.20.122)  0.795 ms 100.95.2.143 (100.95.2.143)  0.827 ms
 9  100.100.20.86 (100.100.20.86)  0.442 ms 100.100.4.78 (100.100.4.78)  0.347 ms 100.100.20.20 (100.100.20.20)  1.388 ms
10  100.92.212.20 (100.92.212.20)  11.611 ms 100.92.11.54 (100.92.11.54)  12.675 ms 100.92.11.56 (100.92.11.56)  10.835 ms
11  100.92.6.52 (100.92.6.52)  11.427 ms 100.92.6.50 (100.92.6.50)  11.033 ms 100.92.210.50 (100.92.210.50)  10.551 ms
12  100.92.210.139 (100.92.210.139)  10.026 ms 100.92.6.13 (100.92.6.13)  14.586 ms 100.92.210.69 (100.92.210.69)  12.032 ms
13  100.92.79.12 (100.92.79.12)  12.011 ms 100.92.79.68 (100.92.79.68)  11.318 ms 100.92.80.84 (100.92.80.84)  10.496 ms
14  100.92.9.27 (100.92.9.27)  11.354 ms 100.92.80.31 (100.92.80.31)  13.000 ms 52.93.135.125 (52.93.135.125)  11.412 ms
15  150.222.241.85 (150.222.241.85)  9.660 ms 52.93.135.81 (52.93.135.81)  10.941 ms 150.222.241.87 (150.222.241.87)  16.543 ms
16  100.92.228.102 (100.92.228.102)  15.168 ms 100.92.227.41 (100.92.227.41)  10.134 ms 100.92.227.52 (100.92.227.52)  11.756 ms
17  100.92.232.111 (100.92.232.111)  10.589 ms 100.92.231.69 (100.92.231.69)  16.664 ms 100.92.232.37 (100.92.232.37)  13.089 ms
18  100.91.205.140 (100.91.205.140)  11.551 ms 100.91.201.62 (100.91.201.62)  10.246 ms 100.91.201.36 (100.91.201.36)  11.368 ms
19  100.91.205.79 (100.91.205.79)  11.112 ms 100.91.205.83 (100.91.205.83)  11.040 ms 100.91.205.33 (100.91.205.33)  10.114 ms
20  100.91.211.45 (100.91.211.45)  9.486 ms 100.91.211.79 (100.91.211.79)  13.693 ms 100.91.211.47 (100.91.211.47)  13.619 ms
21  100.100.6.81 (100.100.6.81)  11.522 ms 100.100.68.70 (100.100.68.70)  10.181 ms 100.100.6.21 (100.100.6.21)  11.687 ms
22  100.100.65.131 (100.100.65.131)  10.371 ms 100.100.92.6 (100.100.92.6)  10.939 ms 100.100.65.70 (100.100.65.70)  23.703 ms
23  100.100.2.74 (100.100.2.74)  15.317 ms 100.100.66.17 (100.100.66.17)  11.492 ms 100.100.88.67 (100.100.88.67)  35.312 ms
24  100.100.16.16 (100.100.16.16)  19.155 ms 100.100.16.28 (100.100.16.28)  19.147 ms 100.100.2.68 (100.100.2.68)  13.718 ms
25  99.83.89.19 (99.83.89.19)  28.929 ms *  21.790 ms
26  104.26.11.229 (104.26.11.229)  11.070 ms  11.058 ms  11.982 ms
```

W drugim uruchomieniu programu traceroute zauważyliśmy, że tym razem pakiety podążały dłuższą trasą, przechodząc przez 26 routerów. Jeśli uruchamiasz traceroute do systemu w swojej sieci, trasa raczej się nie zmieni. Nie możemy jednak oczekiwać, że pozostanie niezmienna, gdy pakiety będą musiały przejść przez inne routery poza naszą siecią.

Podsumowując, możemy zauważyć następujące rzeczy:

- Liczba przeskoków/routerów między Twoim systemem a systemem docelowym zależy od momentu uruchomienia polecenia traceroute. Nie ma gwarancji, że pakiety zawsze będą podążać tą samą trasą, nawet jeśli znajdujesz się w tej samej sieci lub powtórzysz polecenie traceroute w krótkim czasie.
- Niektóre routery zwracają publiczny adres IP. Możesz sprawdzić kilka z tych routerów w zależności od zakresu planowanych testów penetracyjnych.
- Niektóre routery nie zwracają odpowiedzi.
### Telnet
Protokół TELNET (Teletype Network) został opracowany w 1969 roku w celu komunikacji ze zdalnym systemem za pośrednictwem interfejsu wiersza poleceń ( CLI ). W związku z tym polecenie `telnet`wykorzystuje protokół #TELNET do zdalnej administracji. Domyślnym portem używanym przez telnet jest port 23. Z punktu widzenia bezpieczeństwa, telnet `telnet`wysyła wszystkie dane, w tym nazwy użytkowników i hasła, w postaci jawnego tekstu. Wysyłanie jawnego tekstu ułatwia każdemu, kto ma dostęp do kanału komunikacyjnego, kradzież danych logowania. Bezpieczną alternatywą jest protokół SSH (Secure SHell).

Jednak klient telnet, dzięki swojej prostocie, może być używany do innych celów. Wiedząc, że klient telnet opiera się na protokole TCP, można użyć Telnetu do połączenia się z dowolną usługą i pobrania jej baneru. Za pomocą Telnetu `telnet MACHINE_IP PORT`można połączyć się z dowolną usługą działającą w protokole TCP , a nawet wymienić kilka wiadomości, chyba że korzysta ona z szyfrowania.

Załóżmy, że chcemy uzyskać więcej informacji o serwerze WWW nasłuchującym na porcie 80. Łączymy się z serwerem na porcie 80, a następnie komunikujemy się za pomocą protokołu HTTP. Nie trzeba zagłębiać się w szczegóły protokołu HTTP; wystarczy wydać polecenie `GET / HTTP/1.1`. Aby określić coś innego niż domyślna strona indeksu, można wydać polecenie `GET /page.html HTTP/1.1`, które spowoduje żądanie `page.html`. Wskazaliśmy również zdalnemu serwerowi WWW, że chcemy używać protokołu HTTP w wersji 1.1 do komunikacji. Aby uzyskać prawidłową odpowiedź, zamiast błędu, należy wprowadzić wartość dla hosta `host: example`i nacisnąć dwukrotnie klawisz Enter. Wykonanie tych kroków zapewni żądaną stronę indeksu.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ telnet MACHINE_IP 80
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.
GET / HTTP/1.1
host: telnet

HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Tue, 17 Aug 2021 11:13:25 GMT
Content-Type: text/html
Content-Length: 867
Last-Modified: Tue, 17 Aug 2021 11:12:16 GMT
Connection: keep-alive
ETag: "611b9990-363"
Accept-Ranges: bytes

...
```

Szczególnie interesujące jest dla nas ustalenie typu i wersji zainstalowanego serwera WWW `Server: nginx/1.6.2`. W tym przykładzie komunikowaliśmy się z serwerem WWW, więc użyliśmy podstawowych poleceń HTTP . Łącząc się z serwerem pocztowym, musimy użyć odpowiednich poleceń opartych na protokole, takich jak SMTP i POP3 .

### Netcat
Netcat, lub po prostu `nc`inny, oferuje wiele aplikacji, które mogą być niezwykle cenne dla pentestera. #Netcat obsługuje protokoły TCP i UDP. Może działać jako klient łączący się z portem nasłuchującym; alternatywnie, może działać jako serwer nasłuchujący na wybranym porcie. Jest to zatem wygodne narzędzie, którego można używać jako prostego klienta lub serwera przez TCP lub UDP.

Po pierwsze, możesz połączyć się z serwerem, tak jak w przypadku Telnetu, aby pobrać jego baner za pomocą `nc MACHINE_IP PORT`, co jest dość podobne do naszego poprzedniego `telnet MACHINE_IP PORT`. Pamiętaj, że może być konieczne naciśnięcie SHIFT+ENTER po wierszu GET.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ nc MACHINE_IP 80
GET / HTTP/1.1
host: netcat

HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Tue, 17 Aug 2021 11:39:49 GMT
Content-Type: text/html
Content-Length: 867
Last-Modified: Tue, 17 Aug 2021 11:12:16 GMT
Connection: keep-alive
ETag: "611b9990-363"
Accept-Ranges: bytes
...
```

W terminalu pokazanym powyżej, użyliśmy netcata do połączenia z portem MACHINE_IP 80 za pomocą `nc MACHINE_IP 80`. Następnie, używając , wydaliśmy polecenie get dla strony domyślnej `GET / HTTP/1.1`; informujemy serwer docelowy, że nasz klient obsługuje protokół HTTP w wersji 1.1. Na koniec musimy nadać nazwę naszemu hostowi, więc dodaliśmy w nowym wierszu: `host: netcat`; możesz nadać hostowi dowolną nazwę, ponieważ nie ma to wpływu na to ćwiczenie.

Na podstawie `Server: nginx/1.6.2`otrzymanych danych wyjściowych możemy stwierdzić, że na porcie 80 mamy wersję Nginx 1.6.2, która nasłuchuje połączeń przychodzących.

Za pomocą programu netcat można nasłuchiwać na porcie TCP i łączyć się z portem nasłuchującym w innym systemie.

W systemie _serwerowym_ , w którym chcesz otworzyć port i nasłuchiwać na nim, możesz użyć polecenia `nc -lp 1234`, a jeszcze lepiej `nc -vnlp 1234`, co jest odpowiednikiem `nc -v -l -n -p 1234`, jak zapewne pamiętasz z sali [linuksowej](https://tryhackme.com/module/linux-fundamentals) . Dokładna kolejność liter nie ma znaczenia, o ile numer portu jest poprzedzony bezpośrednio przez `-p`.

|opcja|oznaczający|
|---|---|
|-l|Tryb słuchania|
|-P|Podaj numer portu|
|-N|Tylko numeryczne; brak rozwiązywania nazw hostów za pomocą DNS|
|-v|Szczegółowe dane wyjściowe (opcjonalne, ale przydatne do wykrywania błędów)|
|-vv|Bardzo szczegółowy (opcjonalnie)|
|-k|Kontynuuj słuchanie po rozłączeniu się klienta|

Uwagi:

- opcja `-p`powinna pojawić się tuż przed numerem portu, na którym chcesz nasłuchiwać.
- opcja ta `-n`pozwoli uniknąć wyszukiwań DNS i ostrzeżeń.
- numery portów mniejsze niż 1024 wymagają uprawnień roota do nasłuchiwania.

Po stronie _klienta_ należy wydać polecenie `nc MACHINE_IP PORT_NUMBER`. Oto przykład użycia `nc`funkcji echo. Po pomyślnym nawiązaniu połączenia z serwerem, wszystko, co wpiszesz po stronie klienta, zostanie wyświetlone po stronie serwera i odwrotnie.

Rozważmy poniższy przykład. Po stronie serwera będziemy nasłuchiwać na porcie 1234. Możemy to osiągnąć za pomocą polecenia `nc -vnlp 1234`(to samo co `nc -lvnp 1234`). W naszym przypadku serwer nasłuchujący ma adres IP `MACHINE_IP`, więc możemy połączyć się z nim po stronie klienta, wykonując polecenie `nc MACHINE_IP 1234`. Taka konfiguracja będzie przesyłać wszystko, co wpiszesz po jednej stronie tunelu TCP , na drugą stronę . Nagranie tego procesu znajdziesz poniżej. Zwróć uwagę, że serwer nasłuchujący znajduje się po lewej stronie ekranu.

W tej sali omówiliśmy wiele różnych narzędzi. Łatwo połączyć kilka z nich za pomocą skryptu powłoki, aby zbudować prymitywny skaner sieci i systemu. Można go użyć `traceroute`do mapowania ścieżki do celu, `ping`sprawdzenia, czy system docelowy odpowiada na echo ICMP, oraz `telnet`do sprawdzenia, które porty są otwarte i osiągalne, próbując się z nimi połączyć. Dostępne skanery robią to na znacznie bardziej zaawansowanym i wyrafinowanym poziomie, co zobaczymy w kolejnych czterech salach z [tutaj brakuje kontekstu] `nmap`.

|Rozkaz|Przykład|
|---|---|
|świst|`ping -c 10 MACHINE_IP`na Linuksie lub macOS|
|świst|`ping -n 10 MACHINE_IP`na systemie MS Windows|
|traceroute|`traceroute MACHINE_IP`na Linuksie lub macOS|
|tracert|`tracert MACHINE_IP`na systemie MS Windows|
|telnet|`telnet MACHINE_IP PORT_NUMBER`|
|netcat jako klient|`nc MACHINE_IP PORT_NUMBER`|
|netcat jako serwer|`nc -lvnp PORT_NUMBER`|

Chociaż są to podstawowe narzędzia, są one łatwo dostępne w większości systemów. W szczególności przeglądarka internetowa jest zainstalowana na praktycznie każdym komputerze i smartfonie i może być niezbędnym narzędziem w arsenale do prowadzenia rekonesansu bez wywoływania alarmów. Jeśli chcesz pogłębić swoją wiedzę na temat narzędzi programistycznych, zalecamy dołączenie do [Walking An Application](https://tryhackme.com/room/walkinganapplication) .

|System operacyjny|Skrót do narzędzi programistycznych|
|---|---|
|Linux lub MS Windows|`Ctrl+Shift+I`|
|macOS|`Option + Command + I`|
