---

Nmap , skrót od Network Mapper, to darmowe oprogramowanie typu open source, udostępniane na licencji GPL, stworzone przez Gordona Lyona (Fyodora), eksperta ds. bezpieczeństwa sieci i programistę open source. Nmap to standardowe narzędzie branżowe do mapowania sieci, identyfikowania aktywnych hostów i wykrywania działających usług. Silnik skryptowy Nmapa może dodatkowo rozszerzyć jego funkcjonalność, od identyfikacji usług po wykorzystywanie luk w zabezpieczeniach. Skanowanie Nmapem zazwyczaj przebiega według kroków pokazanych na poniższym rysunku, choć wiele z nich jest opcjonalnych i zależy od argumentów wiersza poleceń podanych przez użytkownika.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f1b4ede255e008646e425038d709c9b6.png)

## Cele edukacyjne

Kiedy chcemy przeszukać sieć, chcemy znaleźć wydajne narzędzie, które pomoże nam wykonywać powtarzalne zadania i odpowiedzieć na następujące pytania:

1. Które systemy są aktywne?
2. Jakie usługi działają w tych systemach?

Pierwsze pytanie dotyczące wyszukiwania aktywnych komputerów znajduje się w tej sali. To pierwsza z serii czterech sal Nmap . Na drugie pytanie dotyczące wykrywania działających usług odpowiadamy w kolejnych salach Nmap , które koncentrują się na skanowaniu portów.

W tym pomieszczeniu wyjaśniono kroki, jakie #Nmap podejmuje, aby wykryć systemy online przed skanowaniem portów. Ten etap jest kluczowy, ponieważ próba skanowania portów w systemach offline będzie jedynie stratą czasu i generowała niepotrzebny szum sieciowy.

Przedstawiamy różne podejścia wykorzystywane przez Nmap do wykrywania aktywnych hostów. W szczególności omawiamy:

1. **Skanowanie ARP** : to skanowanie wykorzystuje żądania ARP do wykrywania aktywnych hostów
2. **Skanowanie ICMP** : To skanowanie wykorzystuje żądania ICMP do identyfikacji aktywnych hostów
3. **Skanowanie TCP / UDP ping** : To skanowanie wysyła pakiety do portów TCP i UDP w celu określenia aktywnych hostów.

Przedstawiamy również dwa skanery, `arp-scan`i `masscan`, i wyjaśniamy, w jaki sposób pokrywają się one z częścią funkcji wykrywania hostów programu Nmap .

## Wymagania wstępne dotyczące nauki

- [Podstawy aplikacji internetowych](https://tryhackme.com/room/webapplicationbasics)
- [Podstawy sieciowania](https://tryhackme.com/room/networkingessentials)
- [Bezpieczne protokoły sieciowe](https://tryhackme.com/room/networkingsecureprotocols)

W następnym zadaniu przyjrzyjmy się bliżej i zrozumiejmy kilka ważnych koncepcji, zanim przejdziemy do prezentacji na żywo.

### Podsieci 
Przyjrzyjmy się kilku terminom, zanim przejdziemy do głównych zadań. _Segment sieci_ to grupa komputerów połączonych za pomocą współdzielonego medium. Medium może być na przykład przełącznik Ethernet lub punkt dostępu Wi-Fi. W sieci IP _podsieć_ jest zazwyczaj odpowiednikiem jednego lub większej liczby segmentów sieci połączonych ze sobą i skonfigurowanych do korzystania z tego samego routera. Segment sieci odnosi się do połączenia fizycznego, a podsieć – do połączenia logicznego.

Na poniższym schemacie sieciowym mamy cztery segmenty sieci lub podsieci. Ogólnie rzecz biorąc, Twój system będzie podłączony do jednego z tych segmentów/podsieci. Podsieć, lub po prostu podsieć, ma swój własny zakres adresów IP i jest połączona z bardziej rozległą siecią za pośrednictwem routera. W zależności od sieci może istnieć zapora sieciowa , która egzekwuje polityki bezpieczeństwa.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/aa787518e856e0094cb40da8399be0f3.png)

Powyższy rysunek przedstawia dwa typy podsieci:

- Podsieci z `/16`, co oznacza, że ​​maskę podsieci można zapisać jako `255.255.0.0`. Ta podsieć może pomieścić około 65 000 hostów.
- Podsieci z `/24`, co oznacza, że ​​maskę podsieci można wyrazić jako `255.255.255.0`. Ta podsieć może mieć około 250 hostów.

Jeśli chcesz dowiedzieć się więcej na temat podsieci, zapoznaj się z zadaniem 2 w sali [Wprowadzenie do sieci LAN .](https://tryhackme.com/room/introtolan)

W ramach aktywnego rozpoznania chcemy uzyskać więcej informacji o grupie hostów lub o podsieci. Jeśli znajdujesz się w tej samej podsieci, możesz oczekiwać, że skaner będzie używał zapytań protokołu ARP Address Resolution Protocol ( ARP ) do wykrywania aktywnych hostów. Zapytanie #ARP ma na celu uzyskanie adresu sprzętowego (adresu MAC), aby umożliwić komunikację na poziomie łącza; możemy jednak wywnioskować, że host jest online. (Do warstwy łącza wrócimy w Zadaniu 4).

Jeśli znajdujesz się w sieci A, możesz użyć protokołu ARP tylko do wykrywania urządzeń w tej podsieci (10.1.100.0/24). Załóżmy, że jesteś połączony z podsiecią inną niż podsieć systemów docelowych. W takim przypadku wszystkie pakiety generowane przez skaner będą kierowane przez bramę domyślną (router) do systemów w innej podsieci; jednak zapytania ARP nie będą kierowane i dlatego nie mogą przekroczyć routera podsieci. ARP to protokół warstwy łącza, a pakiety ARP są powiązane z ich podsiecią.

Kliknij przycisk „Wyświetl witrynę”, aby uruchomić symulator sieci. Użyjemy tego symulatora, aby odpowiedzieć na pytania w zadaniach 2, 4 i 5.

Odpowiedz na poniższe pytania

Wyślij pakiet zawierający następujące informacje:

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/65a1bdee53403520174388d9de6410ba.png)

- Z **komputera 1**
- Do **komputera 1** (w celu wskazania, że ​​jest nadawany)
- Typ pakietu: „Żądanie ARP”
- Dane: komputer6 (ponieważ żądamy adresu MAC **komputera6 za pomocą żądania ARP)**

Ile urządzeń może zobaczyć żądanie ARP? 4

Wspomnieliśmy o różnych technikach skanowania, których możemy użyć w Zadaniu 1. Zanim szczegółowo omówimy każdą z nich i przetestujemy ją na żywym celu, musimy określić cele, które chcemy przeskanować. Ogólnie rzecz biorąc, można podać listę, zakres lub podsieć. Przykłady specyfikacji celów to:

- lista: `MACHINE_IP scanme.nmap.org example.com`przeskanuje 3 adresy IP.
- zakres: `10.11.12.15-20`przeskanuje 6 adresów IP: `10.11.12.15`, `10.11.12.16`,… i `10.11.12.20`.
- podsieć: `MACHINE_IP/30`przeskanuje 4 adresy IP.

Możesz również podać plik jako dane wejściowe dla swojej listy celów `nmap -iL list_of_hosts.txt`.

Jeśli chcesz sprawdzić listę hostów, które Nmap będzie skanował, możesz użyć `nmap -sL TARGETS`. Ta opcja wyświetla szczegółową listę hostów, które Nmap będzie skanował, bez konieczności ich faktycznego skanowania; jednak Nmap będzie próbował odwrócić adresy DNS dla wszystkich celów, aby uzyskać ich nazwy. Nazwy mogą ujawnić różne informacje testerowi penetracji. (Jeśli nie chcesz, aby Nmap łączył się z serwerem DNS, możesz dodać  `-n`.)

Uruchom AttackBox za pomocą `Start AttackBox`poniższego przycisku. Po otwarciu w widoku podzielonym otwórz , `Terminal`i użyj , `Nmap`aby odpowiedzieć na poniższe pytania.

Przyjrzyjmy się ponownie warstwom TCP /IP pokazanym na poniższym rysunku. Wykorzystamy protokoły do ​​wykrycia aktywnych hostów. Zaczynając od dołu do góry, możemy użyć:

- ARP z warstwy łącza
- ICMP z warstwy sieciowej
- TCP z warstwy transportowej
- UDP z warstwy transportowej

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/745e0412b319d324352c7b29863b74f4.png)

**ARP** z warstwy **łącza** – powszechnie używany do **ataków typu Man-In-Middle** (ARP Spoofing i ARP Poisoning)
ICMP** z warstwy **sieciowej** – powszechnie używany w atakach DDoS
TCP** z warstwy **transportowej** – zalewanie SYN, resetowanie TCP, ataki polegające na przejęciu sesji TCP
UDP** z warstwy **transportowej** – używany również w atakach DDoS, w których atakujący atakuje i przeciąża losowe porty na hoście pakietami IP zawierającymi pakiety protokołu UDP (User Datagram Protocol)

Zanim szczegółowo omówimy, jak można wykorzystać każdy skaner, pokrótce omówimy te cztery protokoły. **Protokół ARP** ma jeden cel: wysyła ramkę na adres rozgłoszeniowy w segmencie sieci i prosi komputer o podanie adresu MAC (sprzętowego) w odpowiedzi.

**ICMP** ma [wiele typów](https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml) . Protokół ICMP ping używa typu 8 (echo) i typu 0 (odpowiedź echa).

Jeśli chcesz wysłać polecenie ping do systemu w tej samej podsieci, zapytanie ARP powinno poprzedzać echo ICMP.

Chociaż TCP i UDP są protokołami warstwy transportowej, w przypadku skanowania sieci skaner może wysłać specjalnie spreparowany pakiet do wspólnych portów TCP lub UDP , aby sprawdzić, czy cel odpowiada. Ta metoda jest wydajna, zwłaszcza gdy blokowane jest echo ICMP.
### Odkrywanie hosta za pomocą ARP

Jak sprawdzić, które hosty są aktywne? Kluczowe jest unikanie marnowania czasu na skanowanie portów hosta offline lub nieużywanego adresu IP. Istnieją różne sposoby wykrywania hostów online. Gdy nie ma dostępnych opcji wykrywania hostów, Nmap stosuje następujące metody wykrywania aktywnych hostów:

1. Gdy użytkownik _uprzywilejowany_ próbuje skanować cele w sieci lokalnej (Ethernet), Nmap korzysta _z żądań_ _ARP_ . Użytkownik uprzywilejowany to `root`użytkownik, który należy do sieci `sudoers`i może ją uruchamiać `sudo`.
2. Gdy _uprzywilejowany_ użytkownik próbuje przeskanować cele znajdujące się poza siecią lokalną, Nmap używa żądań echa ICMP, TCP ACK (potwierdzenie) do portu 80, TCP SYN (synchronizacja) do portu 443 i żądania znacznika czasu ICMP.
3. Gdy użytkownik _bez uprawnień_ próbuje przeskanować cele znajdujące się poza siecią lokalną, Nmap ucieka się do trójetapowego uzgadniania TCP, wysyłając pakiety SYN do portów 80 i 443.

Domyślnie Nmap używa pingowania do wyszukiwania aktywnych hostów, a następnie skanuje tylko aktywne hosty. Jeśli chcesz użyć Nmapa do wykrywania aktywnych hostów bez skanowania portów w aktywnych systemach, możesz wydać polecenie `nmap -sn TARGETS`. Przyjrzyjmy się bliżej, aby lepiej zrozumieć różne stosowane techniki.

Skanowanie ARP jest możliwe tylko wtedy, gdy znajdujesz się w tej samej podsieci co systemy docelowe. W sieciach Ethernet (802.3) i WiFi (802.11) musisz znać adres MAC dowolnego systemu, zanim będziesz mógł się z nim komunikować. Adres MAC jest wymagany w nagłówku warstwy łącza; zawiera on między innymi adresy MAC źródłowego i docelowego. Aby uzyskać adres MAC, system operacyjny wysyła zapytanie ARP. Host, który odpowiada na zapytania ARP, jest aktywny. Zapytanie ARP działa tylko wtedy, gdy cel znajduje się w tej samej podsieci co Ty, tj. w tej samej sieci Ethernet/WiFi. Podczas skanowania sieci lokalnej za pomocą Nmapa należy spodziewać się wielu zapytań ARP . Jeśli chcesz, aby Nmap wykonał tylko skanowanie ARP bez skanowania portów, możesz użyć `nmap -PR -sn TARGETS`, gdzie `-PR`wskazuje, że chcesz tylko skanować ARP. Poniższy przykład pokazuje użycie Nmapa do wykrywania hostów bez skanowania portów. Uruchamiamy `nmap -PR -sn MACHINE_IP/24`, aby wykryć wszystkie aktywne systemy w tej samej podsieci co nasz komputer docelowy.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PR -sn 10.10.210.6/24

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-02 07:12 BST
Nmap scan report for ip-10-10-210-75.eu-west-1.compute.internal (10.10.210.75)
Host is up (0.00013s latency).
MAC Address: 02:83:75:3A:F2:89 (Unknown)
Nmap scan report for ip-10-10-210-100.eu-west-1.compute.internal (10.10.210.100)
Host is up (-0.100s latency).
MAC Address: 02:63:D0:1B:2D:CD (Unknown)
Nmap scan report for ip-10-10-210-165.eu-west-1.compute.internal (10.10.210.165)
Host is up (0.00025s latency).
MAC Address: 02:59:79:4F:17:B7 (Unknown)
Nmap scan report for ip-10-10-210-6.eu-west-1.compute.internal (10.10.210.6)
Host is up.
Nmap done: 256 IP addresses (4 hosts up) scanned in 3.12 seconds
```

W tym przypadku komputer `AttackBox`miał adres IP 10.10.210.6 i użył żądań ARP do wykrycia aktywnych hostów w tej samej podsieci. Skanowanie ARP działa, jak pokazano na poniższym rysunku. Nmap wysyła żądania ARP do wszystkich komputerów docelowych, a te, które są online, powinny odpowiedzieć odpowiedzią ARP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f0ce4cd34b827f529255c5c73bb909d1.png)

Jeśli przyjrzymy się pakietom wygenerowanym za pomocą narzędzi takich jak tcpdump lub Wireshark, zobaczymy ruch sieciowy podobny do tego na poniższym rysunku. Na poniższym rysunku Wireshark wyświetla źródłowy i docelowy adres MAC, protokół oraz zapytanie dla każdego żądania ARP. Adres źródłowy to adres MAC naszego urządzenia AttackBox, a docelowy to adres rozgłoszeniowy, ponieważ nie znamy adresu MAC urządzenia docelowego. Możemy jednak zobaczyć adres IP urządzenia docelowego w kolumnie „Informacje”. Na rysunku widzimy, że żądamy adresów MAC wszystkich adresów IP w podsieci, zaczynając od `10.10.210.1`. Host o adresie IP, o który pytamy, wyśle ​​odpowiedź ARP ze swoim adresem MAC i w ten sposób dowiemy się, że jest online.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/fc86462236edf4ee667f416b533c93fd.png)

Mówiąc o skanowaniu ARP , warto wspomnieć o skanerze opartym na zapytaniach ARP`arp-scan` : ; oferuje on wiele opcji dostosowywania skanowania.  Szczegółowe informacje można znaleźć w wiki [arp -scan](https://github.com/royhills/arp-scan/wiki/arp-scan-User-Guide)`arp-scan --localnet` .
Jednym z popularnych wyborów jest po prostu `arp-scan -l`. To polecenie wysyła zapytania ARP do wszystkich prawidłowych adresów IP w sieciach lokalnych. Ponadto, jeśli system ma więcej niż jeden interfejs i chcesz wykryć aktywne hosty na jednym z nich, możesz określić interfejs za pomocą `-I`. Na przykład, `sudo arp-scan -I eth0 -l`polecenie wysyła zapytania ARP do wszystkich prawidłowych adresów IP na `eth0`interfejsie.

Należy pamiętać, że `arp-scan`nie jest on instalowany na AttackBoxie. Można go jednak zainstalować za pomocą `apt install arp-scan`.

W poniższym przykładzie przeskanowaliśmy podsieć AttackBoxa za pomocą `arp-scan ATTACKBOX_IP/24`. Ponieważ przeprowadziliśmy to skanowanie w zbliżonym czasie do poprzedniego `nmap -PR -sn ATTACKBOX_IP/24`, uzyskaliśmy te same trzy aktywne cele.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo arp-scan 10.10.210.6/24
Interface: eth0, datalink type: EN10MB (Ethernet)
WARNING: host part of 10.10.210.6/24 is non-zero
Starting arp-scan 1.9 with 256 hosts (http://www.nta-monitor.com/tools/arp-scan/)
10.10.210.75	02:83:75:3a:f2:89	(Unknown)
10.10.210.100	02:63:d0:1b:2d:cd	(Unknown)
10.10.210.165	02:59:79:4f:17:b7	(Unknown)

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9: 256 hosts scanned in 2.726 seconds (93.91 hosts/sec). 3 responded
```

Podobnie, polecenie `arp-scan`wygeneruje wiele zapytań ARP , które możemy zobaczyć za pomocą tcpdump, Wireshark lub podobnego narzędzia. Możemy zauważyć, że przechwytywanie pakietów dla `arp-scan`i `nmap -PR -sn`daje podobne wzorce ruchu. Poniżej znajduje się wynik działania Wiresharka.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/7a4f0b5fe57a09aaebd18da5d1e1af16.png)

Jeśli zamknąłeś symulator sieci, kliknij `Visit Site`przycisk „ ” w Zadaniu 2, aby go ponownie otworzyć.
### Odkrywanie hosta za pomocą ICMP
Możemy pingować każdy adres IP w sieci docelowej i sprawdzić, kto odpowie na nasze `ping`żądania (ICMP typu 8/Echo) odpowiedzią ping (ICMP typu 0). Proste, prawda? Chociaż byłoby to najprostsze podejście, nie zawsze jest niezawodne. Wiele zapór sieciowych blokuje echo ICMP; nowe wersje systemu MS Windows są skonfigurowane z zaporą hosta, która domyślnie blokuje żądania echa ICMP. Należy pamiętać, że zapytanie ARP poprzedza żądanie ICMP, jeśli cel znajduje się w tej samej podsieci.

Aby użyć żądania echa ICMP do wykrycia aktywnych hostów, dodaj opcję `-PE`. (Pamiętaj o dodaniu tej opcji, `-sn`jeśli nie chcesz, aby następnie nastąpiło skanowanie portów.)

Jak pokazano na poniższym rysunku, skanowanie echa ICMP wysyła żądanie echa ICMP i oczekuje, że cel odpowie za pomocą odpowiedzi echa ICMP, jeśli jest w trybie online.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/25fb5fd5d2009cf69d7aae40e8fde2ec.png)

W poniższym przykładzie przeskanowaliśmy podsieć celu za pomocą `nmap -PE -sn MACHINE_IP/24`. To skanowanie wyśle ​​pakiety echa ICMP do każdego adresu IP w podsieci. Ponownie, oczekujemy odpowiedzi od aktywnych hostów; należy jednak pamiętać, że wiele zapór sieciowych blokuje ICMP. Poniższy wynik przedstawia wynik skanowania podsieci klasy C maszyny wirtualnej za pomocą `sudo nmap -PE -sn MACHINE_IP/24`AttackBox.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PE -sn 10.10.68.220/24

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-02 10:16 BST
Nmap scan report for ip-10-10-68-50.eu-west-1.compute.internal (10.10.68.50)
Host is up (0.00017s latency).
MAC Address: 02:95:36:71:5B:87 (Unknown)
Nmap scan report for ip-10-10-68-52.eu-west-1.compute.internal (10.10.68.52)
Host is up (0.00017s latency).
MAC Address: 02:48:E8:BF:78:E7 (Unknown)
Nmap scan report for ip-10-10-68-77.eu-west-1.compute.internal (10.10.68.77)
Host is up (-0.100s latency).
MAC Address: 02:0F:0A:1D:76:35 (Unknown)
Nmap scan report for ip-10-10-68-110.eu-west-1.compute.internal (10.10.68.110)
Host is up (-0.10s latency).
MAC Address: 02:6B:50:E9:C2:91 (Unknown)
Nmap scan report for ip-10-10-68-140.eu-west-1.compute.internal (10.10.68.140)
Host is up (0.00021s latency).
MAC Address: 02:58:59:63:0B:6B (Unknown)
Nmap scan report for ip-10-10-68-142.eu-west-1.compute.internal (10.10.68.142)
Host is up (0.00016s latency).
MAC Address: 02:C6:41:51:0A:0F (Unknown)
Nmap scan report for ip-10-10-68-220.eu-west-1.compute.internal (10.10.68.220)
Host is up (0.00026s latency).
MAC Address: 02:25:3F:DB:EE:0B (Unknown)
Nmap scan report for ip-10-10-68-222.eu-west-1.compute.internal (10.10.68.222)
Host is up (0.00025s latency).
MAC Address: 02:28:B1:2E:B0:1B (Unknown)
Nmap done: 256 IP addresses (8 hosts up) scanned in 2.11 seconds
```

Wynik skanowania pokazuje, że 8 hostów jest aktywnych, wraz z ich adresami MAC. Generalnie nie spodziewamy się poznać adresów MAC celów, chyba że znajdują się one w tej samej podsieci co nasz system. Powyższe dane wskazują, że Nmap nie musiał wysyłać pakietów ICMP, ponieważ potwierdził działanie tych hostów na podstawie otrzymanych odpowiedzi ARP.

Powtórzymy powyższe skanowanie, jednak tym razem przeskanujemy system w innej podsieci. Wyniki są podobne, ale bez adresów MAC.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PE -sn 10.10.68.220/24

Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 12:16 EEST
Nmap scan report for 10.10.68.50
Host is up (0.12s latency).
Nmap scan report for 10.10.68.52
Host is up (0.12s latency).
Nmap scan report for 10.10.68.77
Host is up (0.11s latency).
Nmap scan report for 10.10.68.110
Host is up (0.11s latency).
Nmap scan report for 10.10.68.140
Host is up (0.11s latency).
Nmap scan report for 10.10.68.142
Host is up (0.11s latency).
Nmap scan report for 10.10.68.220
Host is up (0.11s latency).
Nmap scan report for 10.10.68.222
Host is up (0.11s latency).
Nmap done: 256 IP addresses (8 hosts up) scanned in 8.26 seconds
```

Jeśli przyjrzysz się pakietom sieciowym za pomocą narzędzia takiego jak Wireshark, zobaczysz coś podobnego do poniższego obrazu. Widać, że mamy jeden źródłowy adres IP w innej podsieci niż podsieć docelowa, wysyłający żądania echa ICMP do wszystkich adresów IP w podsieci docelowej, aby sprawdzić, który z nich odpowie.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/0fa352ccc303a6e840929ab4a21848b1.png)

Ponieważ żądania echa ICMP są zazwyczaj blokowane, warto rozważyć również żądania znacznika czasu ICMP lub maski adresów ICMP, aby sprawdzić, czy system jest online. Nmap używa żądania znacznika czasu (typ ICMP 13) i sprawdza, czy otrzyma odpowiedź w postaci znacznika czasu (typ ICMP 14). Dodanie tej  `-PP`opcji spowoduje, że Nmap będzie używał żądań znacznika czasu ICMP. Jak pokazano na poniższym rysunku, oczekuje się odpowiedzi od aktywnych hostów.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/06443faaa41a349ff46732d60e2e3bcd.png)

W poniższym przykładzie uruchamiamy program `nmap -PP -sn MACHINE_IP/24`w celu wykrycia komputerów online w podsieci docelowej.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PP -sn 10.10.68.220/24

Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 12:06 EEST
Nmap scan report for 10.10.68.50
Host is up (0.13s latency).
Nmap scan report for 10.10.68.52
Host is up (0.25s latency).
Nmap scan report for 10.10.68.77
Host is up (0.14s latency).
Nmap scan report for 10.10.68.110
Host is up (0.14s latency).
Nmap scan report for 10.10.68.140
Host is up (0.15s latency).
Nmap scan report for 10.10.68.209
Host is up (0.14s latency).
Nmap scan report for 10.10.68.220
Host is up (0.14s latency).
Nmap scan report for 10.10.68.222
Host is up (0.14s latency).
Nmap done: 256 IP addresses (8 hosts up) scanned in 10.93 seconds
```

Podobnie jak w przypadku poprzedniego skanowania ICMP, to skanowanie będzie wysyłać wiele żądań znacznika czasu ICMP do każdego prawidłowego adresu IP w podsieci docelowej. Na poniższym zrzucie ekranu Wiresharka widać jeden źródłowy adres IP wysyłający pakiety ICMP do każdego możliwego adresu IP w celu wykrycia hostów online.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/61ddb58cf7ffb3472f12388ff3ac3f4b.png)

Podobnie Nmap korzysta z zapytań o maskę adresów (ICMP typu 17) i sprawdza, czy otrzyma odpowiedź z maską adresów (ICMP typu 18). To skanowanie można włączyć za pomocą opcji `-PM`. Jak pokazano na poniższym rysunku, hosty aktywne powinny odpowiadać na zapytania o maskę adresów ICMP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/14c31c66e002e2f50b0f8525c8d8e456.png)

Próbując wykryć aktywne hosty za pomocą zapytań o maski adresów ICMP, uruchamiamy polecenie `nmap -PM -sn MACHINE_IP/24`. Chociaż wcześniejsze skanowanie wykazało co najmniej 8 aktywnych hostów, to skanowanie nie zwróciło żadnego. Powodem jest to, że system docelowy lub zapora sieciowa na trasie blokuje ten typ pakietów ICMP. Dlatego ważne jest, aby nauczyć się wielu podejść, aby osiągnąć ten sam rezultat. Jeśli jeden typ pakietów zostanie zablokowany, zawsze możemy wybrać inny, aby wykryć docelową sieć i usługi.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PM -sn 10.10.68.220/24

Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 12:13 EEST
Nmap done: 256 IP addresses (0 hosts up) scanned in 52.17 seconds
```

Chociaż nie otrzymaliśmy żadnej odpowiedzi i nie mogliśmy ustalić, które hosty są online, należy zauważyć, że to skanowanie wysłało żądania ICMP z maską adresu do każdego prawidłowego adresu IP i oczekiwało na odpowiedź. Każde żądanie ICMP zostało wysłane dwukrotnie, jak pokazano na poniższym zrzucie ekranu.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/8281b22c8eff2c0e09cef3d81c9d299a.png)
### Odkrywanie hostów za pomocą TCP/UDP
**Ping TCP SYN**

Możemy wysłać pakiet z flagą SYN (Synchronizacja) ustawioną na port TCP , domyślnie 80, i czekać na odpowiedź. Otwarty port powinien odpowiedzieć sygnałem SYN/ACK (Potwierdzenie); zamknięty port skutkowałby sygnałem RST (Reset). W tym przypadku sprawdzamy jedynie, czy otrzymaliśmy odpowiedź, aby wywnioskować, czy host jest aktywny. Konkretny stan portu nie ma tu znaczenia. Poniższy rysunek przypomina, jak zazwyczaj działa potrójne uzgadnianie TCP .

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/23e7f481f78de8d3e89ef845b747002d.png)

Jeśli chcesz, aby Nmap używał pingowania TCP SYN, możesz to zrobić za pomocą opcji, `-PS`a następnie numeru portu, zakresu, listy lub ich kombinacji. Na przykład, Nmap `-PS21`będzie kierował na port 21, a `-PS21-25`Nmap na porty 21, 22, 23, 24 i 25. Ostatecznie Nmap `-PS80,443,8080`będzie kierował na trzy porty: 80, 443 i 8080.

Użytkownicy uprzywilejowani (root i sudoers) mogą wysyłać pakiety TCP SYN i nie muszą przeprowadzać trzyetapowego uzgadniania TCP, nawet jeśli port jest otwarty, jak pokazano na poniższym rysunku. Użytkownicy nieuprzywilejowani nie mają innego wyboru, jak tylko przeprowadzić trzyetapowe uzgadnianie, jeśli port jest otwarty.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/168d48701c5f872cf1930e08b32bcd6f.png)

Przeskanujemy `nmap -PS -sn MACHINE_IP/24`docelową podsieć maszyny wirtualnej. Jak widać na poniższym wyniku, wykryliśmy pięć hostów.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PS -sn 10.10.68.220/24
Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 13:45 EEST
Nmap scan report for 10.10.68.52
Host is up (0.10s latency).
Nmap scan report for 10.10.68.121
Host is up (0.16s latency).
Nmap scan report for 10.10.68.125
Host is up (0.089s latency).
Nmap scan report for 10.10.68.134
Host is up (0.13s latency).
Nmap scan report for 10.10.68.220
Host is up (0.11s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 17.38 seconds
```

Przyjrzyjmy się bliżej temu, co działo się za kulisami, analizując ruch sieciowy w Wireshark na poniższym rysunku. Technicznie rzecz biorąc, ponieważ nie określiliśmy żadnych portów TCP do użycia w skanowaniu ping TCP, Nmap użył domyślnego portu TCP – 80. Każda usługa nasłuchująca na porcie 80 powinna odpowiedzieć, co pośrednio wskazuje, że host jest online.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/e580a3279be3798ddb78f61a9ee21587.png)

**TCP ACK Ping**

Jak się domyślasz, wysyła to pakiet z ustawioną flagą ACK. Aby to zrobić, musisz uruchomić Nmapa jako użytkownik uprzywilejowany. Jeśli spróbujesz tego jako użytkownik nieuprzywilejowany, Nmap spróbuje nawiązać potrójne uzgadnianie.

Domyślnie używany jest port 80. Składnia jest podobna do polecenia TCP SYN ping. `-PA`Po komendzie powinien następować numer portu, zakres numerów portów, lista lub ich kombinacja. Na przykład rozważmy  `-PA21`, `-PA21-25`i `-PA80,443,8080`. Jeśli nie określono portu, użyty zostanie port 80.

Poniższy rysunek pokazuje, że każdy pakiet TCP z ustawioną flagą ACK powinien otrzymać pakiet TCP z `RST`ustawioną flagą. Obiekt docelowy odpowiada z `RST`ustawioną flagą, ponieważ pakiet TCP z flagą ACK nie jest częścią żadnego trwającego połączenia. Oczekiwana odpowiedź służy do sprawdzenia, czy host docelowy jest aktywny.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/db5ab44a8c700c4ab0603e85e456040d.png)

W tym przykładzie uruchamiamy `sudo nmap -PA -sn MACHINE_IP/24`wykrywanie hostów online w podsieci docelowej. Widzimy, że skanowanie TCP ACK ping wykryło pięć aktywnych hostów.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PA -sn 10.10.68.220/24
Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 13:46 EEST
Nmap scan report for 10.10.68.52
Host is up (0.11s latency).
Nmap scan report for 10.10.68.121
Host is up (0.12s latency).
Nmap scan report for 10.10.68.125
Host is up (0.10s latency).
Nmap scan report for 10.10.68.134
Host is up (0.10s latency).
Nmap scan report for 10.10.68.220
Host is up (0.10s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 29.89 seconds
```

Jeśli przyjrzymy się ruchowi sieciowemu, jak pokazano na poniższym rysunku, odkryjemy wiele pakietów z ustawioną flagą ACK i wysłanych na port 80 systemów docelowych. Nmap wysyła każdy pakiet dwukrotnie. Systemy, które nie odpowiedzą, są offline lub niedostępne.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/6ccdba7337684b8e8f532a23c5259ffc.png)

**Ping UDP**

Wreszcie, możemy użyć protokołu UDP, aby sprawdzić, czy host jest online. W przeciwieństwie do protokołu TCP SYN ping, wysłanie pakietu UDP na otwarty port nie powinno skutkować żadną odpowiedzią. Jeśli jednak wyślemy pakiet UDP na zamknięty port UDP, spodziewamy się otrzymania pakietu ICMP informującego o nieosiągalności portu; oznacza to, że system docelowy jest aktywny i dostępny.

Na poniższym rysunku widzimy pakiet UDP wysłany do otwartego portu UDP i nie wywołujący żadnej odpowiedzi. Jednak wysłanie pakietu UDP do dowolnego zamkniętego portu UDP może wywołać odpowiedź pośrednio wskazującą, że obiekt docelowy jest online.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/1b827ef60c39619e281c4ca51a6d57b6.png)

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/c8b2d403667487322058619e561186d2.png)

Składnia określająca porty jest podobna do składni pingów TCP SYN i TCP ACK; Nmap używa jej `-PU`do pingowania UDP . W poniższym przykładzie uruchamiamy skanowanie UDP i wykrywamy pięć aktywnych hostów.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -PU -sn 10.10.68.220/24
Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-02 13:45 EEST
Nmap scan report for 10.10.68.52
Host is up (0.10s latency).
Nmap scan report for 10.10.68.121
Host is up (0.10s latency).
Nmap scan report for 10.10.68.125
Host is up (0.14s latency).
Nmap scan report for 10.10.68.134
Host is up (0.096s latency).
Nmap scan report for 10.10.68.220
Host is up (0.11s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 9.20 seconds
```

Przyjrzyjmy się wygenerowanym pakietom UDP. Na poniższym zrzucie ekranu z Wiresharka widzimy, że Nmap wysyła pakiety UDP do portów UDP, które najprawdopodobniej są zamknięte. Poniższy obraz pokazuje, że Nmap używa nietypowego portu UDP do wygenerowania błędu ICMP „nieosiągalny adres docelowy (port nieosiągalny)”.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/2417b8b03f00fe5f589a08d9e6e62209.png)

**Masscan**

Na marginesie, Masscan stosuje podobne podejście do wykrywania dostępnych systemów. Jednak, aby szybko przeskanować sieć, Masscan generuje pakiety dość agresywnie. Składnia jest bardzo podobna:  `-p`po nazwie może następować numer portu, lista lub zakres. Rozważmy poniższe przykłady:

- `masscan MACHINE_IP/24 -p443`
- `masscan MACHINE_IP/24 -p80,443`
- `masscan MACHINE_IP/24 -p22-25`
- `masscan MACHINE_IP/24 ‐‐top-ports 100`

Masscan nie jest zainstalowany na `AttackBox`; można go jednak zainstalować za pomocą `apt install masscan`.

Domyślnie Nmap korzysta z odwrotnego #DNS dla hostów online. Ponieważ nazwy hostów mogą wiele ujawnić, może to być pomocne. Jeśli jednak nie chcesz wysyłać takich zapytań DNS , możesz `-n`pominąć ten krok.

Domyślnie Nmap wyszukuje hosty online; możesz jednak skorzystać z opcji `-R`zapytania do serwera DNS nawet w przypadku hostów offline. Jeśli chcesz używać konkretnego serwera DNS, możesz dodać tę  `--dns-servers DNS_SERVER` opcję.

Dowiedziałeś się, jak protokoły ARP , ICMP, TCP i UDP mogą wykrywać aktywne hosty, wypełniając ten pokój. Każda odpowiedź od hosta oznacza, że ​​jest on online. Poniżej znajduje się krótkie podsumowanie opcji wiersza poleceń dla Nmap , które omówiliśmy.

|Typ skanowania|Przykładowe polecenie|
|---|---|
|Skanowanie ARP|`sudo nmap -PR -sn MACHINE_IP/24`|
|Skanowanie echa ICMP|`sudo nmap -PE -sn MACHINE_IP/24`|
|Skanowanie znaczników czasu ICMP|`sudo nmap -PP -sn MACHINE_IP/24`|
|Skanowanie maski adresów ICMP|`sudo nmap -PM -sn MACHINE_IP/24`|
|Skanowanie TCP SYN Ping|`sudo nmap -PS22,80,443 -sn MACHINE_IP/30`|
|Skanowanie TCP ACK Ping|`sudo nmap -PA22,80,443 -sn MACHINE_IP/30`|
|Skanowanie pingów UDP|`sudo nmap -PU53,161,162 -sn MACHINE_IP/30`|

Pamiętaj o dodaniu tej opcji, `-sn`jeśli interesuje Cię tylko wykrywanie hostów bez skanowania portów. Pominięcie tej opcji `-sn`spowoduje, że Nmap domyślnie będzie skanował aktywne hosty w poszukiwaniu portów.

| Opcja | Zamiar                                          |
| ----- | ----------------------------------------------- |
| `-n`  | brak wyszukiwania DNS                           |
| `-R`  | odwrotne wyszukiwanie DNS dla wszystkich hostów |
| `-sn` | tylko wykrywanie hosta                          |
### Nmap proste skanowanie portów

To drugie pomieszczenie w serii Nmap (część modułu Wprowadzenie do bezpieczeństwa sieci).

1. [Odkrywanie hosta Nmap Live](https://tryhackme.com/room/nmap01)
2. [Podstawowe skanowanie portów Nmap](https://tryhackme.com/room/nmap02)
3. [Zaawansowane skanowanie portów Nmap](https://tryhackme.com/room/nmap03)
4. [Nmap Post Port Scans](https://tryhackme.com/room/nmap04)

W poprzedniej sali skupiliśmy się na wykrywaniu systemów online. Do tej pory omówiliśmy trzy etapy skanowania Nmap :

1. Wymień cele
2. Odkryj gospodarzy na żywo
3. Odwrotne wyszukiwanie DNS

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f351cd3eaca9da85b9417ca820494ec0.png)
Następnym krokiem będzie sprawdzenie, które porty są otwarte i nasłuchują, a które zamknięte. Dlatego w tej i następnej sali skupimy się na skanowaniu portów i różnych typach skanowania portów używanych przez `nmap`. W tej sali wyjaśniono:

1. Skanowanie portu TCP Connect
2. Skanowanie portu TCP SYN
3. Skanowanie portu UDP

Ponadto omawiamy różne opcje określania portów, częstotliwości skanowania i liczby równoległych sond.

W tym samym sensie, w jakim adres IP określa hosta w sieci wśród wielu innych, port #TCP lub port #UDP służy do identyfikacji usługi sieciowej działającej na tym hoście. Serwer zapewnia usługę sieciową i przestrzega określonego protokołu sieciowego. Przykłady obejmują dostarczanie czasu, odpowiadanie na zapytania DNS i serwowanie stron internetowych. Port jest zwykle powiązany z usługą przy użyciu tego konkretnego numeru portu. Na przykład serwer HTTP domyślnie powiązałby się z portem TCP 80; ponadto, jeśli serwer HTTP obsługuje SSL/ TLS , nasłuchiwałby na porcie TCP 443. ( Porty TCP 80 i 443 są domyślnymi portami dla HTTP i HTTPS; jednak administrator serwera WWW może w razie potrzeby wybrać inne numery portów). Ponadto nie więcej niż jedna usługa może nasłuchiwać na dowolnym porcie TCP lub UDP (na tym samym adresie IP).

Ryzykując nadmierne uproszczenie, możemy podzielić porty na dwa stany:

1. Otwarty port oznacza, że ​​na tym porcie nasłuchuje jakaś usługa.
2. Zamknięty port oznacza, że ​​na tym porcie nie nasłuchuje żadna usługa.

Jednak w praktyce musimy wziąć pod uwagę wpływ zapór sieciowych. Na przykład, port może być otwarty, ale zapora sieciowa może blokować pakiety. Dlatego Nmap uwzględnia następujące sześć stanów:

1. **Otwarte** : oznacza, że ​​usługa nasłuchuje na określonym porcie.
2. **Zamknięty** : oznacza, że ​​żadna usługa nie nasłuchuje na określonym porcie, mimo że port jest dostępny. Przez dostępny rozumiemy, że jest osiągalny i nie jest blokowany przez zaporę sieciową ani inne urządzenia/programy zabezpieczające.
3. **Filtrowany** : oznacza, że ​​Nmap nie może określić, czy port jest otwarty, czy zamknięty, ponieważ jest niedostępny. Ten stan jest zazwyczaj spowodowany przez zaporę sieciową uniemożliwiającą Nmapowi dotarcie do tego portu. Pakiety Nmap mogą zostać zablokowane przed dotarciem do portu; alternatywnie odpowiedzi mogą zostać zablokowane przed dotarciem do hosta Nmap .
4. **Niefiltrowany** : oznacza, że ​​Nmap nie może określić, czy port jest otwarty, czy zamknięty, mimo że jest dostępny. Ten stan występuje podczas skanowania ACK `-sA`.
5. **Otwarte|Filtrowane** : oznacza to, że Nmap nie jest w stanie określić, czy port jest otwarty czy filtrowany.
6. **Zamknięte|Filtrowane** : oznacza to, że Nmap nie może zdecydować, czy port jest zamknięty, czy filtrowany.
### Flaga TCP

Nmap obsługuje różne typy skanowania portów TCP . Aby zrozumieć różnicę między nimi, musimy przyjrzeć się nagłówkowi TCP . Nagłówek TCP to pierwsze 24 bajty segmentu TCP . Poniższy rysunek przedstawia nagłówek TCP zdefiniowany w [dokumencie RFC 793.](https://datatracker.ietf.org/doc/html/rfc793.html) Na pierwszy rzut oka rysunek wygląda skomplikowanie, jednak jest dość prosty do zrozumienia. W pierwszym wierszu znajduje się numer portu źródłowego TCP i numer portu docelowego. Widać, że numerowi portu przydzielono 16 bitów (2 bajty). W drugim i trzecim wierszu znajduje się numer sekwencyjny i numer potwierdzenia. Każdy wiersz ma przydzielone 32 bity (4 bajty), co daje łącznie sześć wierszy, co daje 24 bajty.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/79ca8e4acbd573a27cee413cde927769.png)

W szczególności musimy skupić się na flagach, które Nmap może ustawiać i wyłączać. Flagi TCP zaznaczyliśmy na czerwono. Ustawienie bitu flagi oznacza ustawienie jego wartości na 1. Od lewej do prawej, flagi nagłówka TCP to:

1. **URG** : Flaga pilna oznacza, że ​​pole wskaźnika pilnego jest istotne. Wskaźnik pilny oznacza, że ​​dane przychodzące są pilne i że segment TCP z ustawioną flagą URG jest przetwarzany natychmiast, bez konieczności oczekiwania na wcześniej wysłane segmenty TCP .
2. **ACK** : Flaga potwierdzenia wskazuje, że numer potwierdzenia jest znaczący. Służy do potwierdzenia odbioru segmentu TCP .
3. **PSH** : Wciśnij flagę żądającą od protokołu TCP natychmiastowego przekazania danych do aplikacji.
4. **RST** : Flaga resetowania służy do resetowania połączenia. Inne urządzenie, takie jak zapora sieciowa , może ją wysłać, aby zerwać połączenie TCP . Flaga ta jest również używana, gdy dane są wysyłane do hosta, a po stronie odbiorczej nie ma usługi, która mogłaby odpowiedzieć.
5. **SYN** : Flaga synchronizacji służy do inicjowania uzgadniania TCP w trybie trójetapowym i synchronizacji numerów sekwencyjnych z drugim hostem. Numer sekwencyjny powinien być ustawiany losowo podczas nawiązywania połączenia TCP .
6. **FIN** : Nadawca nie ma już więcej danych do wysłania.
7. 
Skanowanie połączenia TCP działa poprzez wykonanie trzyetapowego uzgadniania TCP . Podczas standardowego nawiązywania połączenia TCP klient wysyła pakiet TCP z ustawioną flagą SYN, a serwer odpowiada pakietem SYN/ACK, jeśli port jest otwarty; na koniec klient kończy trzyetapowe uzgadnianie, wysyłając ACK.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/8390020a13d6f22f49233833f6265de6.png)

Chcemy sprawdzić, czy port TCP jest otwarty i nie nawiązuje połączenia TCP . Połączenie zostaje zerwane natychmiast po potwierdzeniu jego stanu poprzez wysłanie sygnału RST/ACK. Możesz uruchomić skanowanie połączenia TCP`-sT` za pomocą .

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/514972cd54b3f58c83f951978ea9183e.png)

Należy pamiętać, że jeśli nie jesteś użytkownikiem o uprawnieniach administratora (root lub sudoer), skanowanie połączenia TCP jest jedyną możliwą opcją wykrycia otwartych portów TCP.

W poniższym oknie przechwytywania pakietów Wireshark widzimy Nmap wysyłający pakiety TCP z flagą SYN ustawioną na różnych portach: 256, 443, 143 itd. Domyślnie Nmap będzie próbował połączyć się z 1000 najczęściej używanych portów. Zamknięty port TCP odpowiada na pakiet SYN sygnałem RST/ACK, sygnalizując, że nie jest otwarty. Ten schemat będzie powtarzany dla wszystkich zamkniętych portów, gdy będziemy próbowali zainicjować z nimi potrójne uzgadnianie TCP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a975503bd3e006bd32147ba9c9faede4.png)

Zauważamy, że port 143 jest otwarty, więc odpowiedział pakietem SYN/ACK, a Nmap zakończył potrójne uzgadnianie, wysyłając ACK. Poniższy rysunek przedstawia wszystkie pakiety wymienione między naszym hostem Nmap a portem 143 systemu docelowego. Pierwsze trzy pakiety to zakończenie potrójnego uzgadniania TCP. Następnie czwarty pakiet przerywa połączenie pakietem RST/ACK.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/19ebc8172c930867c50e214b630ef4ec.png)

Aby zilustrować `-sT`( skanowanie połączenia TCP ), poniższy przykład polecenia zwrócił szczegółową listę otwartych portów.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ nmap -sT 10.113.157.160

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 09:53 BST
Nmap scan report for 10.113.157.160
Host is up (0.0024s latency).
Not shown: 995 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
111/tcp open  rpcbind
143/tcp open  imap
993/tcp open  imaps
995/tcp open  pop3s
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.40 seconds
```

Należy pamiętać, że możemy użyć tej `-F`opcji, aby włączyć tryb szybki i zmniejszyć liczbę skanowanych portów z 1000 do 100 najczęściej używanych portów.

Warto wspomnieć, że `-r`można również dodać opcję skanowania portów w kolejności sekwencyjnej, a nie losowej. Opcja ta jest przydatna podczas testowania, czy porty otwierają się w spójny sposób, na przykład podczas uruchamiania systemu docelowego.

### Skanowanie TCP/SYN
Użytkownicy bez uprawnień mają ograniczone możliwości skanowania połączeń. Jednak domyślnym trybem skanowania jest skanowanie SYN, które wymaga uprawnień użytkownika (root lub sudoer). Skanowanie #SYN nie wymaga przeprowadzania trzyetapowego uzgadniania TCP ; zamiast tego zrywa połączenie po otrzymaniu odpowiedzi od serwera. Ponieważ nie nawiązaliśmy połączenia TCP , zmniejsza to ryzyko zarejestrowania skanowania. Ten typ skanowania można wybrać za pomocą opcji `-sS`. Poniższy rysunek pokazuje, jak działa skanowanie #TCP SYN bez przeprowadzania trzyetapowego uzgadniania TCP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/48e631fd3deba4a2b759ca48405fcc08.png)

Poniższy zrzut ekranu z Wiresharka przedstawia skanowanie TCP SYN. ​​Zachowanie w przypadku zamkniętych portów TCP jest podobne do skanowania TCP Connect.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/ae4a89999447ab19cc829e436d1ec8fe.png)

Aby lepiej zrozumieć różnicę między tymi dwoma skanowaniami, przyjrzyj się poniższemu zrzutowi ekranu. W górnej połowie poniższego rysunku widzimy `-sT`ruch skanowania połączenia TCP. Każdy otwarty port TCP będzie wymagał od Nmapa przeprowadzenia trzyetapowego uzgadniania TCP`-sS` przed zamknięciem połączenia. W dolnej połowie poniższego rysunku widzimy, że skanowanie SYN nie wymaga przeprowadzenia trzyetapowego uzgadniania TCP; zamiast tego Nmap wysyła pakiet RST po odebraniu pakietu SYN/ACK.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/fe642b2fafb70cbaa2531d2c41d6cddb.png)

Skanowanie TCP SYN jest domyślnym trybem skanowania podczas uruchamiania Nmapa jako użytkownik uprzywilejowany, root lub z użyciem sudo i jest bardzo niezawodnym wyborem. Pomyślnie wykrył otwarte porty, które wcześniej wykryłeś podczas skanowania TCP Connect, ale nie udało się nawiązać pełnego połączenia TCP z celem.

Terminal testera penetracyjnego

shell-session
pentester@TryHackMe$ sudo nmap -sS 10.113.157.160

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 09:53 BST
Nmap scan report for 10.113.157.160
Host is up (0.0073s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.60 seconds

### Skanowanie UDP

UDP jest protokołem bezpołączeniowym, a zatem nie wymaga uzgadniania połączenia w celu nawiązania połączenia. Nie możemy zagwarantować, że usługa nasłuchująca na porcie #UDP odpowie na nasze pakiety. Jeśli jednak pakiet #UDP zostanie wysłany do zamkniętego portu, zwracany jest błąd ICMP – port nieosiągalny (typ 3, kod 3). Możesz wybrać skanowanie UDP`-sU` za pomocą tej opcji; co więcej, możesz je połączyć z innym skanowaniem TCP.

Poniższy rysunek pokazuje, że jeśli wyślemy pakiet UDP do otwartego portu UDP, nie możemy oczekiwać żadnej odpowiedzi. Dlatego wysłanie pakietu UDP do otwartego portu nic nam nie powie.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/085088cd1b2b122312b1ee952c4aa0f7.png)

Jednak, jak pokazano na poniższym rysunku, spodziewamy się otrzymania pakietu ICMP typu 3, miejsce docelowe nieosiągalne, i kodu 3, port nieosiągalny. Innymi słowy, porty UDP, które nie generują żadnej odpowiedzi, to te, które Nmap oznaczy jako otwarte.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/8b8b32517699b96777641a97dbf9d880.png)

Na poniższym zrzucie ekranu z programu Wireshark możemy zobaczyć, że każdy zamknięty port wygeneruje pakiet ICMP o treści „miejsce docelowe nieosiągalne” (port niedostępny).

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/f927563f4778092ced3ef7afa67cece3.png)

Uruchomienie skanowania UDP na tym serwerze Linux okazało się cenne i rzeczywiście dowiedzieliśmy się, że port 111 jest otwarty. Z drugiej strony, Nmap nie jest w stanie określić, czy port UDP 68 jest otwarty, czy filtrowany.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sU 10.113.157.160

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 09:54 BST
Nmap scan report for 10.113.157.160
Host is up (0.00061s latency).
Not shown: 998 closed ports
PORT    STATE         SERVICE
68/udp  open|filtered dhcpc
111/udp open          rpcbind
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1085.05 seconds
```
Możesz określić porty, które chcesz przeskanować, zamiast domyślnych 1000 portów. Określanie portów jest już intuicyjne. Zobaczmy kilka przykładów:

- lista portów: `-p22,80,443`skanowane będą porty 22, 80 i 443.
- zakres portów: `-p1-1023`skanowane będą wszystkie porty od 1 do 1023 włącznie, natomiast `-p20-25` skanowane będą porty od 20 do 25 włącznie.

Możesz zlecić skanowanie wszystkich portów za pomocą `-p-`, co spowoduje przeskanowanie wszystkich 65535 portów. Jeśli chcesz przeskanować 100 najpopularniejszych portów, dodaj `-F`. Użycie `--top-ports 10`przeskanuje dziesięć najpopularniejszych portów.

Możesz kontrolować czas skanowania za pomocą `-T<0-5>`. `-T0`jest najwolniejszy (paranoiczny), a `-T5`najszybszy. Według podręcznika Nmapa istnieje sześć szablonów:

- paranoiczny (0)
- podstępny (1)
- uprzejmy (2)
- normalny (3)
- agresywny (4)
- szalony (5)

Aby uniknąć alertów IDS, możesz rozważyć użycie opcji `-T0`lub `-T1`. Na przykład `-T0`skanuje jeden port na raz i odczekuje 5 minut między wysłaniem każdej sondy, dzięki czemu możesz oszacować, ile czasu zajęłoby skanowanie jednego celu. Jeśli nie określisz czasu, Nmap użyje opcji normalnej `-T3`. Należy pamiętać, że `-T5` jest to najbardziej agresywne ustawienie pod względem szybkości; jednak może to wpłynąć na dokładność wyników skanowania ze względu na zwiększone prawdopodobieństwo utraty pakietów. Należy pamiętać, że opcja ta `-T4`jest często używana podczas operacji CTF i nauki skanowania celów ćwiczebnych, natomiast `-T1`często jest używana w rzeczywistych starciach, gdzie ważniejsze jest zachowanie ukrycia.

Alternatywnie możesz kontrolować szybkość pakietów za pomocą `--min-rate <number>`i `--max-rate <number>`. Na przykład `--max-rate 10`lub `--max-rate=10` zapewnia, że ​​skaner nie wysyła więcej niż dziesięciu pakietów na sekundę.

Co więcej, można kontrolować paralelizację sondowania za pomocą `--min-parallelism <numprobes>`komend i `--max-parallelism <numprobes>`. Nmap sonduje cele, aby wykryć, które hosty są aktywne, a które porty otwarte; paralelizacja sondowania określa liczbę takich sond, które mogą być uruchomione równolegle. Na przykład, `--min-parallelism=512`wymusza na Nmap utrzymanie co najmniej 512 sond równolegle; te 512 sond jest związanych z wykrywaniem hostów i otwartymi portami.
W tym pomieszczeniu można było przeprowadzać trzy rodzaje skanów.

|Typ skanowania portu|Przykładowe polecenie|
|---|---|
|Skanowanie połączenia TCP|`nmap -sT 10.113.157.160`|
|Skanowanie TCP SYN|`sudo nmap -sS 10.113.157.160`|
|Skanowanie UDP|`sudo nmap -sU 10.113.157.160`|

Tego typu skanowanie powinno umożliwić Ci rozpoczęcie wykrywania usług TCP i UDP działających na hoście docelowym.

|Opcja|Zamiar|
|---|---|
|`-p-`|wszystkie porty|
|`-p1-1023`|skanuj porty od 1 do 1023|
|`-F`|100 najpopularniejszych portów|
|`-r`|skanuj porty w kolejności sekwencyjnej|
|`-T<0-5>`|-T0 jest najwolniejsze, a T5 najszybsze|
|`--max-rate 50`|szybkość <= 50 pakietów/sek.|
|`--min-rate 15`|szybkość >= 15 pakietów/sek.|
|`--min-parallelism 100`|co najmniej 100 sond równolegle|

Odpowiedz na poniższe pytania

Upewnij się, że zanotowałeś wszystkie opcje skanowania omówione w tej sali. Czas poznać bardziej zaawansowane techniki skanowania portów, dołączając do  sali [poświęconej zaawansowanemu skanowaniu portów Nmap](https://tryhackme.com/room/nmap03)  .

### Zaawansowane skanowanie NMAP
Ta sala jest trzecią z serii Nmap (część modułu „Wprowadzenie do bezpieczeństwa sieci”). W pierwszych dwóch salach dowiedzieliśmy się o wykrywaniu hostów na żywo i podstawowym skanowaniu portów.

1. [Odkrywanie hosta Nmap Live](https://tryhackme.com/room/nmap01)
2. [Podstawowe skanowanie portów Nmap](https://tryhackme.com/room/nmap02)
3. [Zaawansowane skanowanie portów Nmap](https://tryhackme.com/room/nmap03)
4. [Nmap Post Port Scans](https://tryhackme.com/room/nmap04)

W sekcji „ [Podstawowe skanowanie portów](https://tryhackme.com/room/nmap02) [Nmapa”](https://tryhackme.com/room/nmap02) omówiliśmy flagi TCP i omówiliśmy procedurę uzgadniania #TCP (3-way handshake). Aby zainicjować połączenie, TCP wymaga, aby pierwszy pakiet miał ustawioną flagę #SYN. ​​Dzięki temu możemy stwierdzić, czy port TCP jest otwarty na podstawie otrzymanej odpowiedzi.

Badacze bezpieczeństwa i hakerzy przyjrzeli się flagom TCP , pokazanym na poniższym rysunku i wyjaśnionym w poprzedniej sali, i rozpoczęli eksperyment. Chcieli sprawdzić, co się stanie, jeśli wyślemy pakiet TCP , który nie jest częścią żadnego trwającego połączenia TCP , z ustawioną jedną lub kilkoma flagami.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/23540a5fcd27454892a73ac051d29664.png)

Na przykład, flaga #ACK jest ustawiana, gdy chcesz potwierdzić odebrane dane. Skanowanie ACK przypomina próbę potwierdzenia danych, które nie zostały ani wysłane, ani odebrane. Rozważmy prostą analogię: ktoś przychodzi do ciebie znikąd i mówi: „Tak, rozumiem, proszę kontynuować”, mimo że nic nie powiedziałeś.

W tej sali omówione zostaną zaawansowane typy skanowania i opcje skanowania. Niektóre z tych typów skanowania mogą być przydatne w przypadku konkretnych systemów, inne zaś w konkretnych konfiguracjach sieciowych. Omówimy następujące typy skanowania portów:

- Skanowanie zerowe
- Skanowanie FIN
- Skanowanie świąteczne
- Skanowanie Maimona
- Skanowanie ACK
- Skanowanie okna
- Skanowanie niestandardowe

Ponadto omówimy następujące kwestie:

- Podszywanie się pod IP
- Podrabianie adresu MAC
- Skanowanie wabików
- Pofragmentowane pakiety
- Skanowanie w trybie bezczynności/ zombie

Omówimy opcje i techniki omijania zapór sieciowych i systemów IDS . Przedstawimy również sposoby uzyskiwania bardziej szczegółowych informacji z Nmap .

Zacznijmy od następujących trzech typów skanów:

- Skanowanie zerowe
- Skanowanie FIN
- Skanowanie świąteczne
### Skanowanie zerowe

Skanowanie zerowe nie ustawia żadnej flagi; wszystkie sześć bitów flagi jest ustawionych na zero. Możesz wybrać to skanowanie za pomocą opcji `-sN`. Pakiet TCP bez ustawionych flag nie wywoła żadnej odpowiedzi po dotarciu do otwartego portu, jak pokazano na poniższym rysunku. Zatem, z perspektywy Nmapa, brak odpowiedzi podczas skanowania zerowego wskazuje, że port jest otwarty lub zapora sieciowa blokuje pakiet.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/04b178a9cf7048c21256988b8b2343e3.png)

Oczekujemy jednak, że serwer docelowy odpowie pakietem #RST, jeśli port jest zamknięty. W związku z tym, na podstawie braku odpowiedzi RST, możemy określić, które porty nie są zamknięte: otwarte lub filtrowane.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/224e01a913a1ce7b0fb2b9290ff5e1c8.png)

Poniżej znajduje się przykład skanowania #null na serwerze Linux. Przeprowadzone przez nas skanowanie null pomyślnie zidentyfikowało sześć otwartych portów w systemie docelowym. Ponieważ skanowanie null opiera się na braku odpowiedzi, aby wywnioskować, że port nie jest zamknięty, nie może ono jednoznacznie wskazać, że te porty są otwarte; istnieje możliwość, że porty nie odpowiadają z powodu reguły zapory sieciowej.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sN MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:30 BST
Nmap scan report for MACHINE_IP
Host is up (0.00066s latency).
Not shown: 994 closed ports
PORT    STATE         SERVICE
22/tcp  open|filtered ssh
25/tcp  open|filtered smtp
80/tcp  open|filtered http
110/tcp open|filtered pop3
111/tcp open|filtered rpcbind
143/tcp open|filtered imap
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 96.50 seconds
```

Należy pamiętać, że wiele opcji Nmap wymaga uprawnień użytkownika root. Jeśli nie uruchamiasz Nmapa jako root, musisz użyć opcji `sudo`, jak w powyższym przykładzie `-sN`.

### Skanowanie FIN

Skanowanie FIN wysyła pakiet TCP z ustawioną flagą #FIN. Ten typ skanowania można wybrać za pomocą opcji `-sF` . Podobnie, odpowiedź nie zostanie wysłana, jeśli port TCP jest otwarty. Ponownie, Nmap nie ma pewności, czy port jest otwarty, czy też zapora sieciowa blokuje ruch związany z tym portem TCP .

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/78eb3d6ba158542f2b3223184b032e64.png)

Jednak system docelowy powinien odpowiedzieć RST, jeśli port jest zamknięty. Dzięki temu będziemy mogli dowiedzieć się, które porty są zamknięte i wykorzystać tę wiedzę do wywnioskowania, które porty są otwarte, a które filtrowane. Warto zauważyć, że niektóre zapory sieciowe „po cichu” odrzucają ruch bez wysyłania RST.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/74dc07da7351a5a7f258948ec59efccc.png)

Poniżej znajduje się przykład skanowania FIN serwera Linux. Wynik jest bardzo podobny do wyniku uzyskanego wcześniej za pomocą skanowania zerowego.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sF MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:32 BST
Nmap scan report for MACHINE_IP
Host is up (0.0018s latency).
Not shown: 994 closed ports
PORT    STATE         SERVICE
22/tcp  open|filtered ssh
25/tcp  open|filtered smtp
80/tcp  open|filtered http
110/tcp open|filtered pop3
111/tcp open|filtered rpcbind
143/tcp open|filtered imap
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 96.52 seconds
```
### Skanowanie świąteczne

Skanowanie świąteczne wzięło swoją nazwę od światełek choinkowych. Skanowanie świąteczne ustawia jednocześnie flagi FIN, PSH i URG. Możesz wybrać skanowanie świąteczne za pomocą opcji `-sX`.

Podobnie jak w przypadku skanowania #Null i #FIN, otrzymanie pakietu #RST oznacza zamknięcie portu. W przeciwnym razie zostanie on zgłoszony jako otwarty|filtrowany.

Poniższe dwa rysunki pokazują przypadek, gdy port TCP jest otwarty i przypadek, gdy port TCP jest zamknięty.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/7d28b756aed3b6eb72faf98d6974776c.png)

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/4304eacbc3db1af21657f285bc16ebce.png)

Poniższy wynik konsoli przedstawia przykład skanowania Xmas na serwerze Linux. Uzyskane wyniki są bardzo podobne do wyników skanowania null i skanowania FIN.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sX MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:34 BST
Nmap scan report for MACHINE_IP
Host is up (0.00087s latency).
Not shown: 994 closed ports
PORT    STATE         SERVICE
22/tcp  open|filtered ssh
25/tcp  open|filtered smtp
80/tcp  open|filtered http
110/tcp open|filtered pop3
111/tcp open|filtered rpcbind
143/tcp open|filtered imap
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 84.85 seconds
```

Jednym ze scenariuszy, w którym te trzy typy skanowania mogą być skuteczne, jest skanowanie celu za zaporą bezstanową (niestanową) . Zapora bezstanowa sprawdza, czy przychodzący pakiet ma ustawioną flagę #SYN, aby wykryć próbę połączenia. Użycie kombinacji flag niezgodnej z pakietem SYN umożliwia oszukanie zapory i dotarcie do systemu za nią. Jednak zapora stanowa praktycznie blokuje wszystkie takie spreparowane pakiety, czyniąc ten rodzaj skanowania bezużytecznym.

### Skanowanie TCP Maimon

Uriel #Maimon po raz pierwszy opisał to skanowanie w 1996 roku. Podczas tego skanowania ustawiane są bity FIN i ACK. Cel powinien wysłać pakiet RST w odpowiedzi. Jednak niektóre systemy oparte na BSD odrzucają pakiet, jeśli jest to otwarty port, odsłaniając otwarte porty. To skanowanie nie zadziała na większości celów spotykanych w nowoczesnych sieciach; jednak uwzględniamy je w tym artykule, aby lepiej zrozumieć mechanizm skanowania portów i sposób myślenia hakerów. Aby wybrać ten typ skanowania, użyj opcji `-sM`.

Większość systemów docelowych odpowiada pakietem RST niezależnie od tego, czy port TCP jest otwarty. W takim przypadku nie będziemy w stanie wykryć otwartych portów. Poniższy rysunek przedstawia oczekiwane zachowanie w przypadku zarówno otwartych, jak i zamkniętych portów TCP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/8ca5e5e0f6e0a1843cebe11b5b0785b3.png)

Poniższy wynik konsoli to przykład skanowania TCP Maimon na serwerze Linux. Jak wspomniano, ponieważ otwarte i zamknięte porty zachowują się tak samo, skanowanie Maimon nie wykryło żadnych otwartych portów w systemie docelowym.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sM 10.10.252.27

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:36 BST
Nmap scan report for ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27)
Host is up (0.00095s latency).
All 1000 scanned ports on ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27) are closed
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.61 seconds
```

Ten typ skanowania nie jest pierwszym typem skanowania, jaki wybiera się w celu wykrycia systemu. Ważne jest jednak, aby o nim wiedzieć, ponieważ nigdy nie wiadomo, kiedy może się przydać.

### Skanowanie niestandardowe TCP ACK

To zadanie pokaże, jak wykonać skanowanie #TCP #ACK, skanowanie okna TCP i jak utworzyć własne skanowanie flag.

### Skanowanie TCP ACK

Zacznijmy od skanowania TCP ACK. Jak sama nazwa wskazuje, skanowanie ACK wysyła pakiet TCP z ustawioną flagą ACK. Użyj tej `-sA` opcji, aby wybrać to skanowanie. Jak pokazano na poniższym rysunku, cel odpowiedziałby na ACK sygnałem RST, niezależnie od stanu portu. Dzieje się tak, ponieważ pakiet TCP z ustawioną flagą ACK powinien być wysyłany tylko w odpowiedzi na odebrany pakiet TCP, aby potwierdzić odbiór danych, w przeciwieństwie do naszego przypadku. Dlatego to skanowanie nie powie nam, czy port docelowy jest otwarty w prostej konfiguracji.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a991831cedbb2761dde1fe66012a7311.png)

W poniższym przykładzie przeskanowaliśmy docelową maszynę wirtualną przed zainstalowaniem na niej zapory sieciowej. Zgodnie z oczekiwaniami nie udało nam się ustalić, które porty są otwarte.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sA MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:37 BST
Nmap scan report for MACHINE_IP
Host is up (0.0013s latency).
All 1000 scanned ports on MACHINE_IP are unfiltered
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.68 seconds
      
```

Ten rodzaj skanowania byłby pomocny, gdyby przed celem znajdowała się zapora sieciowa . W rezultacie, na podstawie tego, które pakiety ACK spowodowały odpowiedź, dowiesz się, które porty nie zostały zablokowane przez zaporę . Innymi słowy, ten rodzaj skanowania jest bardziej odpowiedni do wykrywania zestawów reguł i konfiguracji zapory sieciowej .

Po skonfigurowaniu docelowej maszyny wirtualnej `MACHINE_IP` z zaporą sieciową powtórzyliśmy skanowanie ACK. Tym razem otrzymaliśmy interesujące wyniki. Jak widać na poniższym wyjściu konsoli, mamy trzy porty, które nie są blokowane przez zaporę sieciową. Ten wynik wskazuje, że zapora blokuje wszystkie pozostałe porty poza tymi trzema.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sA MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-07 11:34 BST
Nmap scan report for MACHINE_IP
Host is up (0.00046s latency).
Not shown: 997 filtered ports
PORT    STATE      SERVICE
22/tcp  unfiltered ssh
25/tcp  unfiltered smtp
80/tcp  unfiltered http
MAC Address: 02:78:C0:D0:4E:E9 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 15.45 seconds
      
```

### Skanowanie okna

Innym podobnym skanowaniem jest skanowanie okna TCP . Skanowanie okna TCP jest prawie takie samo jak skanowanie ACK, jednak bada pole okna TCP w zwróconych pakietach RST. W niektórych systemach może to ujawnić, że port jest otwarty. Ten typ skanowania można wybrać za pomocą opcji `-sW` . Jak pokazano na poniższym rysunku, spodziewamy się otrzymać pakiet RST w odpowiedzi na nasze „niezaproszone” pakiety ACK, niezależnie od tego, czy port jest otwarty, czy zamknięty.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5118dcb424d429376f09bf2f85db5bce.png)

Podobnie, uruchomienie skanowania okna TCP w systemie Linux bez zapory sieciowej nie dostarczy wielu informacji. Jak widać na poniższym wyjściu konsoli, wyniki skanowania okna na serwerze Linux bez zapory sieciowej nie dostarczyły żadnych dodatkowych informacji w porównaniu ze skanowaniem ACK wykonanym wcześniej.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sW MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:38 BST
Nmap scan report for MACHINE_IP
Host is up (0.0011s latency).
All 1000 scanned ports on ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27) are closed
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.60 seconds
      
```

Jednak, jak można się spodziewać, jeśli powtórzymy skanowanie okna TCP na serwerze za zaporą sieciową , spodziewamy się bardziej satysfakcjonujących rezultatów. W poniższym wyniku konsoli, skanowanie okna TCP wskazało, że trzy porty zostały wykryte jako zamknięte. (W przeciwieństwie do skanowania ACK, które oznaczyło te same trzy porty jako niefiltrowane). Chociaż wiemy, że te trzy porty nie są zamknięte, zdajemy sobie sprawę, że zareagowały inaczej, co wskazuje, że zapora sieciowa ich nie blokuje.

Terminal testera penetracyjnego

shell-session
pentester@TryHackMe$ sudo nmap -sW MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-07 11:39 BST
Nmap scan report for MACHINE_IP
Host is up (0.00040s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE
22/tcp  closed ssh
25/tcp  closed smtp
80/tcp  closed http
MAC Address: 02:78:C0:D0:4E:E9 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 14.84 seconds
      
### Skanowanie niestandardowe

Jeśli chcesz poeksperymentować z nową kombinacją flag TCP wykraczającą poza wbudowane typy skanowania TCP , możesz to zrobić za pomocą `--scanflags` . Na przykład, jeśli chcesz ustawić jednocześnie SYN, RST i FIN, możesz to zrobić za pomocą `--scanflags RSTSYNFIN` . Jak pokazano na poniższym rysunku, jeśli tworzysz własne skanowanie, musisz wiedzieć, jak będą zachowywać się różne porty, aby poprawnie interpretować wyniki w różnych scenariuszach.

X![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d76c5020f14ac0d66e7ff3812bb0bec3.png)

Na koniec należy zauważyć, że skanowanie ACK i skanowanie okien bardzo skutecznie pomogły nam w mapowaniu reguł zapory sieciowej . Należy jednak pamiętać, że to, że zapora sieciowa nie blokuje określonego portu, nie oznacza, że ​​usługa nasłuchuje na tym porcie. Na przykład istnieje możliwość, że reguły zapory sieciowej wymagają aktualizacji, aby odzwierciedlały ostatnie zmiany w usługach. W związku z tym skanowanie ACK i skanowanie okien ujawnia reguły zapory sieciowej , a nie usługi.

### Skanowanie okna

Innym podobnym skanowaniem jest skanowanie okna TCP . Skanowanie okna TCP jest prawie takie samo jak skanowanie ACK, jednak bada pole okna TCP w zwróconych pakietach RST. W niektórych systemach może to ujawnić, że port jest otwarty. Ten typ skanowania można wybrać za pomocą opcji `-sW` . Jak pokazano na poniższym rysunku, spodziewamy się otrzymać pakiet RST w odpowiedzi na nasze „niezaproszone” pakiety ACK, niezależnie od tego, czy port jest otwarty, czy zamknięty.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5118dcb424d429376f09bf2f85db5bce.png)

Podobnie, uruchomienie skanowania okna TCP w systemie Linux bez zapory sieciowej nie dostarczy wielu informacji. Jak widać na poniższym wyjściu konsoli, wyniki skanowania okna na serwerze Linux bez zapory sieciowej nie dostarczyły żadnych dodatkowych informacji w porównaniu ze skanowaniem ACK wykonanym wcześniej.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sW 10.113.159.105

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:38 BST
Nmap scan report for 10.113.159.105
Host is up (0.0011s latency).
All 1000 scanned ports on ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27) are closed
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.60 seconds
      
```

Jednak, jak można się spodziewać, jeśli powtórzymy skanowanie okna TCP na serwerze za zaporą sieciową , spodziewamy się bardziej satysfakcjonujących rezultatów. W poniższym wyniku konsoli, skanowanie okna TCP wskazało, że trzy porty zostały wykryte jako zamknięte. (W przeciwieństwie do skanowania ACK, które oznaczyło te same trzy porty jako niefiltrowane). Chociaż wiemy, że te trzy porty nie są zamknięte, zdajemy sobie sprawę, że zareagowały inaczej, co wskazuje, że zapora sieciowa ich nie blokuje.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sW 10.113.159.105

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-07 11:39 BST
Nmap scan report for 10.113.159.105
Host is up (0.00040s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE
22/tcp  closed ssh
25/tcp  closed smtp
80/tcp  closed http
MAC Address: 02:78:C0:D0:4E:E9 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 14.84 seconds
      
```
### Skanowanie niestandardowe

Jeśli chcesz poeksperymentować z nową kombinacją flag TCP wykraczającą poza wbudowane typy skanowania TCP , możesz to zrobić za pomocą `--scanflags` . Na przykład, jeśli chcesz ustawić jednocześnie SYN, RST i FIN, możesz to zrobić za pomocą `--scanflags RSTSYNFIN` . Jak pokazano na poniższym rysunku, jeśli tworzysz własne skanowanie, musisz wiedzieć, jak będą zachowywać się różne porty, aby poprawnie interpretować wyniki w różnych scenariuszach.

X![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/d76c5020f14ac0d66e7ff3812bb0bec3.png)

Na koniec należy zauważyć, że skanowanie ACK i skanowanie okien bardzo skutecznie pomogły nam w mapowaniu reguł zapory sieciowej . Należy jednak pamiętać, że to, że zapora sieciowa nie blokuje określonego portu, nie oznacza, że ​​usługa nasłuchuje na tym porcie. Na przykład istnieje możliwość, że reguły zapory sieciowej wymagają aktualizacji, aby odzwierciedlały ostatnie zmiany w usługach. W związku z tym skanowanie ACK i skanowanie okien ujawnia reguły zapory sieciowej , a nie usługi.

Odpowiedz na poniższe pytania

Ile flag jest ustawionych podczas skanowania okna TCP?

Poprawna odpowiedź

Zdecydowałeś się poeksperymentować z niestandardowym skanowaniem TCP z ustawioną flagą resetowania. Co dodałbyś później  `--scanflags`? RST

### Podszywanie się pod wabiki 

W niektórych konfiguracjach sieciowych możliwe będzie przeskanowanie systemu docelowego przy użyciu sfałszowanego adresu IP, a nawet adresu MAC. Takie skanowanie jest korzystne tylko w sytuacji, gdy masz gwarancję przechwycenia odpowiedzi. Próbując przeskanować system docelowy z losowej sieci przy użyciu sfałszowanego adresu IP, istnieje duże prawdopodobieństwo, że nie otrzymasz żadnej odpowiedzi, a wyniki skanowania mogą być mało wiarygodne.

Poniższy rysunek przedstawia atakującego uruchamiającego polecenie `nmap -S SPOOFED_IP 10.113.159.105`. W rezultacie Nmap będzie tworzyć wszystkie pakiety, korzystając z podanego źródłowego adresu IP `SPOOFED_IP`. Komputer docelowy będzie odpowiadał na przychodzące pakiety, wysyłając odpowiedzi na docelowy adres IP `SPOOFED_IP`. Aby to skanowanie działało i dawało dokładne wyniki, atakujący musi monitorować ruch sieciowy i analizować odpowiedzi.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/45b982d501fd26deb2b381059b16f80c.png)

Krótko mówiąc, skanowanie przy użyciu fałszywego adresu IP składa się z trzech kroków:

1. Atakujący wysyła pakiet z fałszywym adresem IP do komputera docelowego.
2. Komputer docelowy odpowiada na fałszywy adres IP jako miejsce docelowe.
3. Atakujący przechwytuje odpowiedzi, aby znaleźć otwarte porty.

Generalnie oczekuje się określenia interfejsu sieciowego, który ma być używany `-e`, i jawnego wyłączenia skanowania ping `-Pn`. Dlatego zamiast `nmap -S SPOOFED_IP 10.113.159.105`, należy wydać polecenie `nmap -e NET_INTERFACE -Pn -S SPOOFED_IP 10.113.159.105`, aby wskazać programowi Nmap , którego interfejsu sieciowego ma używać i nie oczekiwać odpowiedzi ping. Warto powtórzyć, że to skanowanie będzie bezużyteczne, jeśli system atakujący nie będzie mógł monitorować sieci pod kątem odpowiedzi.

Jeśli znajdujesz się w tej samej podsieci co komputer docelowy, możesz również podszyć się pod swój adres MAC. Możesz określić źródłowy adres MAC za pomocą `--spoof-mac SPOOFED_MAC`. Podszywanie się pod adres jest możliwe tylko wtedy, gdy atakujący i komputer docelowy znajdują się w tej samej sieci Ethernet (802.3) lub Wi-Fi (802.11).

Spoofing działa tylko w ograniczonej liczbie przypadków, gdy spełnione są określone warunki. Dlatego atakujący może uciec się do użycia wabików, aby utrudnić jego namierzenie. Koncepcja jest prosta: sprawić, by skanowanie wyglądało na pochodzące z wielu adresów IP, tak aby adres IP atakującego ginął wśród nich. Jak widać na poniższym rysunku, skanowanie komputera docelowego będzie wyglądało na pochodzące z 3 różnych źródeł, a w konsekwencji odpowiedzi również będą wysyłane przez wabiki.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/754fc455556a424ca83f512665beaf7d.png)

Możesz uruchomić skanowanie wabikowe, podając konkretny lub losowy adres IP po `-D`. Na przykład, `nmap -D 10.10.0.1,10.10.0.2,ME 10.113.159.105`skanowanie adresu 10.113.159.105 będzie wyświetlane jako pochodzące z adresów IP 10.10.0.1, 10.10.0.2, a następnie `ME`Twój adres IP powinien pojawić się w trzeciej kolejności. Innym przykładowym poleceniem byłoby `nmap -D 10.10.0.1,10.10.0.2,RND,RND,ME 10.113.159.105`, gdzie trzeci i czwarty źródłowy adres IP są przypisywane losowo, a piąty źródłowy będzie adresem IP atakującego. Innymi słowy, za każdym razem, gdy wykonasz to ostatnie polecenie, spodziewałbyś się, że dwa nowe losowe adresy IP będą trzecim i czwartym źródłem wabikowym.

### Zapora Sieciowa

#Zapora #sieciowa to oprogramowanie lub sprzęt, które zezwala na przepływ pakietów lub je blokuje. Działa w oparciu o reguły zapory , które można streścić jako blokowanie całego ruchu z wyjątkami lub zezwalanie na cały ruch z wyjątkami. Na przykład, można zablokować cały ruch do serwera z wyjątkiem ruchu przychodzącego do serwera WWW. Tradycyjna zapora sieciowa sprawdza co najmniej nagłówek IP i nagłówek warstwy transportowej. Bardziej zaawansowana zapora sieciowa próbowałaby również analizować dane przesyłane przez warstwę transportową.

### IDS

System wykrywania włamań ( #IDS ) sprawdza pakiety sieciowe pod kątem wybranych wzorców zachowań lub określonych sygnatur zawartości. Generuje alert za każdym razem, gdy zostanie spełniona szkodliwa reguła. Oprócz nagłówka IP i nagłówka warstwy transportowej, system IDS sprawdza zawartość danych w warstwie transportowej i sprawdza, czy pasuje ona do jakichkolwiek szkodliwie działających wzorców. Jak zmniejszyć prawdopodobieństwo wykrycia aktywności Nmap przez tradycyjną zaporę sieciową / system IDS ? Odpowiedź na to pytanie nie jest łatwa; jednak w zależności od typu zapory sieciowej / systemu IDS , korzystne może być podzielenie pakietu na mniejsze pakiety.

### Pofragmentowane pakiety

Nmap oferuje opcję `-f`fragmentacji pakietów. Po wybraniu tej opcji dane IP zostaną podzielone na 8 bajtów lub mniej. Dodanie kolejnego `-f`( `-f -f`lub `-ff`) spowoduje podzielenie danych na fragmenty 16-bajtowe zamiast 8. Wartość domyślną można zmienić za pomocą `--mtu`; jednak zawsze należy wybrać wielokrotność 8.

Aby właściwie zrozumieć fragmentację, musimy przyjrzeć się nagłówkowi IP na poniższym rysunku. Na pierwszy rzut oka może wydawać się skomplikowany, ale zauważamy, że znamy większość jego pól. W szczególności zwróć uwagę na adres źródłowy zajmujący 32 bity (4 bajty) w czwartym wierszu, podczas gdy adres docelowy zajmuje kolejne 4 bajty w piątym wierszu. Dane, które będziemy fragmentować na wiele pakietów, są zaznaczone na czerwono. Aby ułatwić ponowne złożenie danych po stronie odbiorcy, protokół IP wykorzystuje identyfikator (ID) i przesunięcie fragmentu, pokazane w drugim wierszu poniższego rysunku.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5e55834e2638ba7ec9e84a0900b68ccb.png)  

Porównajmy działanie `sudo nmap -sS -p80 10.20.30.144`i `sudo nmap -sS -p80 -f 10.20.30.144`. Jak już wiesz, w tym przypadku zostanie użyte ukryte skanowanie TCP SYN na porcie 80; jednak w drugim poleceniu żądamy od Nmapa fragmentacji pakietów IP.

W pierwszych dwóch wierszach widzimy zapytanie i odpowiedź ARP. Nmap wysłał zapytanie ARP, ponieważ cel znajduje się w tej samej sieci Ethernet. Kolejne dwa wiersze pokazują ping TCP SYN i odpowiedź. Piąty wiersz to początek skanowania portów; Nmap wysyła pakiet TCP SYN na port 80. W tym przypadku nagłówek IP ma 20 bajtów, a nagłówek TCP 24 bajty. Należy pamiętać, że minimalny rozmiar nagłówka TCP to 20 bajtów.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/b817b7d8b8ef9ee64dd9494e31def426.png)

Po zażądaniu fragmentacji za pomocą `-f`, 24 bajty nagłówka TCP zostaną podzielone na wielokrotności 8 bajtów, przy czym ostatni fragment będzie zawierał 8 bajtów lub mniej nagłówka TCP . Ponieważ 24 jest podzielne przez 8, otrzymaliśmy 3 fragmenty IP; każdy zawiera 20 bajtów nagłówka IP i 8 bajtów nagłówka TCP . Te trzy fragmenty widzimy między piątym a siódmym wierszem.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/953fd599d2afaa8efb36923b02707d2b.png)

Należy pamiętać, że jeśli dodasz `-ff`(lub `-f -f`), fragmentacja danych będzie wielokrotnością 16. Innymi słowy, 24 bajty nagłówka TCP zostaną w tym przypadku podzielone na dwa fragmenty IP, pierwszy zawierający 16 bajtów, a drugi zawierający 8 bajtów nagłówka TCP.

Z drugiej strony, jeśli wolisz zwiększyć rozmiar pakietów, aby wyglądały nieszkodliwie, możesz użyć opcji `--data-length NUM`, gdzie num określa liczbę bajtów, które chcesz dołączyć do pakietów.

Odpowiedz na poniższe pytania

Jeśli segment TCP ma rozmiar 64 i  `-ff` używana jest opcja, ile fragmentów IP otrzymasz? 4

### Skanowanie w trybie zoombie

Podrabianie źródłowego adresu IP może być świetnym sposobem na dyskretne skanowanie. Jednak podrabianie działa tylko w określonych konfiguracjach sieciowych. Wymaga ono możliwości monitorowania ruchu. Biorąc pod uwagę te ograniczenia, podrabianie adresu IP może być mało przydatne; możemy jednak ulepszyć tę metodę, stosując skanowanie w trybie bezczynności.

Skanowanie w trybie bezczynności, zwane również #skanowaniem #zombie , wymaga bezczynnego systemu podłączonego do sieci, z którym można się komunikować. W praktyce Nmap sprawi, że każda sonda będzie wyglądała tak, jakby pochodziła z bezczynnego hosta ( zombie ), a następnie sprawdzi, czy bezczynny host ( zombie ) otrzymał odpowiedź na sfałszowaną sondę. Odbywa się to poprzez sprawdzenie wartości identyfikatora IP (IP ID) w nagłówku IP. Skanowanie w trybie bezczynności można uruchomić za pomocą `nmap -sI ZOMBIE_IP 10.113.159.105`, gdzie `ZOMBIE_IP`oznacza adres IP bezczynnego hosta ( zombie ).

Skanowanie w trybie bezczynności ( zombie ) wymaga wykonania następujących trzech kroków w celu sprawdzenia, czy port jest otwarty:

1. Wywołaj reakcję bezczynnego hosta, aby móc zapisać bieżący identyfikator IP bezczynnego hosta.
2. Wyślij pakiet SYN do portu TCP w urządzeniu docelowym. Pakiet powinien zostać sfałszowany, aby wyglądał, jakby pochodził z adresu IP nieaktywnego hosta ( zombie ).
3. Ponownie uruchom maszynę bezczynną, aby odpowiedzieć, dzięki czemu będziesz mógł porównać nowy identyfikator IP z otrzymanym wcześniej.

Wyjaśnijmy to za pomocą rysunków. Na poniższym rysunku system atakujący sonduje bezczynną maszynę – drukarkę wielofunkcyjną. Wysyłając pakiet SYN/ACK, odpowiada pakietem RST zawierającym nowo zwiększony identyfikator IP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/a93e181f0effe000554a8b307448bbb2.png)

W następnym kroku atakujący wyśle ​​pakiet SYN do portu TCP , który chce sprawdzić na komputerze docelowym. Pakiet ten będzie jednak używał adresu IP bezczynnego hosta ( zombie ) jako źródła. Możliwe są trzy scenariusze. W pierwszym scenariuszu, pokazanym na poniższym rysunku, port TCP jest zamknięty; w związku z tym komputer docelowy odpowiada bezczynnemu hostowi pakietem RST. Bezczynny host nie odpowiada; w związku z tym jego identyfikator IP nie jest zwiększany.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/8e28bf940936ddbc2367b193ea3550b8.png)

W drugim scenariuszu, jak pokazano poniżej, port TCP jest otwarty, więc komputer docelowy odpowiada pakietem SYN/ACK do bezczynnego hosta ( zombie ). Bezczynny host odpowiada na ten nieoczekiwany pakiet pakietem RST, zwiększając w ten sposób swój identyfikator IP.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/2b0de492e2154a30760852e07cebae0e.png)

W trzecim scenariuszu komputer docelowy w ogóle nie odpowiada z powodu reguł zapory sieciowej . Ten brak odpowiedzi doprowadzi do takiego samego rezultatu, jak w przypadku zamkniętego portu; bezczynny host nie zwiększy identyfikatora IP.

W ostatnim kroku atakujący wysyła kolejny pakiet SYN/ACK do bezczynnego hosta. Bezczynny host odpowiada pakietem RST, ponownie zwiększając identyfikator IP o jeden. Atakujący musi porównać identyfikator IP pakietu RST odebranego w pierwszym kroku z identyfikatorem IP pakietu RST odebranym w trzecim kroku. Różnica 1 oznacza, że ​​port na komputerze docelowym został zamknięty lub filtrowany. Natomiast różnica 2 oznacza, że ​​port na komputerze docelowym był otwarty.

Warto powtórzyć, że to skanowanie nazywa się skanowaniem bezczynnym, ponieważ wybór bezczynnego hosta jest niezbędny dla jego dokładności. Gdyby „bezczynny host” był zajęty, wszystkie zwrócone identyfikatory IP byłyby bezużyteczne.

### Dodatkowe szczegóły skanowania 

Możesz rozważyć dodanie, `--reason`jeśli chcesz, aby Nmap dostarczył więcej szczegółów dotyczących swojego rozumowania i wniosków. Rozważ dwa poniższe skany systemu; jednak to drugie dodaje `--reason`.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS 10.10.252.27

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:39 BST
Nmap scan report for ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27)
Host is up (0.0020s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.60 seconds
```

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS --reason 10.10.252.27

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:40 BST
Nmap scan report for ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27)
Host is up, received arp-response (0.0020s latency).
Not shown: 994 closed ports
Reason: 994 resets
PORT    STATE SERVICE REASON
22/tcp  open  ssh     syn-ack ttl 64
25/tcp  open  smtp    syn-ack ttl 64
80/tcp  open  http    syn-ack ttl 64
110/tcp open  pop3    syn-ack ttl 64
111/tcp open  rpcbind syn-ack ttl 64
143/tcp open  imap    syn-ack ttl 64
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.59 seconds
```

Podanie tej `--reason`flagi pozwala nam jednoznacznie stwierdzić, dlaczego Nmap uznał, że system jest aktywny lub że dany port jest otwarty. W powyższym wyniku konsoli widzimy, że system jest uważany za online, ponieważ Nmap „otrzymał odpowiedź ARP”. Z drugiej strony wiemy, że port SSH jest uważany za otwarty, ponieważ Nmap otrzymał pakiet zwrotny „syn-ack”.

Aby uzyskać bardziej szczegółowy wynik, możesz rozważyć użycie `-v`opcji „Wyjście szczegółowe” lub `-vv`„Jeszcze więcej szczegółów”.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS -vv 10.10.252.27

Starting Nmap 7.60 ( https://nmap.org ) at 2021-08-30 10:41 BST
Initiating ARP Ping Scan at 10:41
Scanning 10.10.252.27 [1 port]
Completed ARP Ping Scan at 10:41, 0.22s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 10:41
Completed Parallel DNS resolution of 1 host. at 10:41, 0.00s elapsed
Initiating SYN Stealth Scan at 10:41
Scanning ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27) [1000 ports]
Discovered open port 22/tcp on 10.10.252.27
Discovered open port 25/tcp on 10.10.252.27
Discovered open port 80/tcp on 10.10.252.27
Discovered open port 110/tcp on 10.10.252.27
Discovered open port 111/tcp on 10.10.252.27
Discovered open port 143/tcp on 10.10.252.27
Completed SYN Stealth Scan at 10:41, 1.25s elapsed (1000 total ports)
Nmap scan report for ip-10-10-252-27.eu-west-1.compute.internal (10.10.252.27)
Host is up, received arp-response (0.0019s latency).
Scanned at 2021-08-30 10:41:02 BST for 1s
Not shown: 994 closed ports
Reason: 994 resets
PORT    STATE SERVICE REASON
22/tcp  open  ssh     syn-ack ttl 64
25/tcp  open  smtp    syn-ack ttl 64
80/tcp  open  http    syn-ack ttl 64
110/tcp open  pop3    syn-ack ttl 64
111/tcp open  rpcbind syn-ack ttl 64
143/tcp open  imap    syn-ack ttl 64
MAC Address: 02:45:BF:8A:2D:6B (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1.59 seconds
           Raw packets sent: 1002 (44.072KB) | Rcvd: 1002 (40.092KB)
```

Jeśli `-vv`nie zaspokoi to Twojej ciekawości, możesz użyć go `-d`do debugowania szczegółów lub `-dd`po prostu do uzyskania jeszcze większej ilości szczegółów. Możesz mieć pewność, że `-d`wynik będzie widoczny nie tylko na jednym ekranie.

Odpowiedz na poniższe pytania

Uruchom AttackBoxa, jeśli jeszcze tego nie zrobiłeś. Po upewnieniu się, że zakończyłeś działanie maszyny wirtualnej w zadaniu 4, uruchom maszynę wirtualną dla tego zadania. Poczekaj na jej pełne załadowanie, a następnie otwórz terminal w AttackBoxie i użyj Nmapa  `nmap -sS -F --reason 10.113.159.105` do przeskanowania maszyny wirtualnej. Jaki jest podany powód otwarcia wskazanych portów?

### Podsumowanie

W tym pomieszczeniu można było przeprowadzać następujące rodzaje skanów.

|Typ skanowania portu|Przykładowe polecenie|
|---|---|
|Skanowanie TCP Null|`sudo nmap -sN 10.113.159.105`|
|Skanowanie TCP FIN|`sudo nmap -sF 10.113.159.105`|
|Skanowanie świąteczne TCP|`sudo nmap -sX 10.113.159.105`|
|Skanowanie TCP Maimon|`sudo nmap -sM 10.113.159.105`|
|Skanowanie TCP ACK|`sudo nmap -sA 10.113.159.105`|
|Skanowanie okna TCP|`sudo nmap -sW 10.113.159.105`|
|Niestandardowe skanowanie TCP|`sudo nmap --scanflags URGACKPSHRSTSYNFIN 10.113.159.105`|
|Sfałszowany adres IP źródłowy|`sudo nmap -S SPOOFED_IP 10.113.159.105`|
|Podrobiony adres MAC|`--spoof-mac SPOOFED_MAC`|
|Skanowanie wabików|`nmap -D DECOY_IP,ME 10.113.159.105`|
|Skanowanie w trybie bezczynności (zombie)|`sudo nmap -sI ZOMBIE_IP 10.113.159.105`|
|Fragmentacja danych IP na 8 bajtów|`-f`|
|Fragmentacja danych IP na 16 bajtów|`-ff`|

|Opcja|Zamiar|
|---|---|
|`--source-port PORT_NUM`|określ numer portu źródłowego|
|`--data-length NUM`|dołącz losowe dane, aby osiągnąć zadaną długość|

Te typy skanowania polegają na ustawianiu flag TCP w nieoczekiwany sposób, aby nakłonić porty do odpowiedzi. Skanowanie null, FIN i Xmas wywołuje odpowiedź z zamkniętych portów, podczas gdy skanowanie Maimon, ACK i Window wywołuje odpowiedź z otwartych i zamkniętych portów.

### Nmap POST Skanowanie Portów

To ostatnia sala z serii poświęconej Nmap (część modułu „Wprowadzenie do bezpieczeństwa sieci”). W tej sali skupiamy się na krokach następujących po skanowaniu portów: w szczególności na wykrywaniu usług, wykrywaniu systemu operacyjnego , silniku skryptowym Nmap oraz zapisywaniu wyników skanowania.

1. [Odkrywanie hosta Nmap Live](https://tryhackme.com/room/nmap01)
2. [Podstawowe skanowanie portów Nmap](https://tryhackme.com/room/nmap02)
3. [Zaawansowane skanowanie portów Nmap](https://tryhackme.com/room/nmap03)
4. [Nmap Post Port Scans](https://tryhackme.com/room/nmap04)

W pierwszej sali tej serii dowiedzieliśmy się, jak Nmap może enumerować cele, wykrywać aktywne hosty i używać odwrotnego DNS do wyszukiwania interesujących nazw. W drugiej i trzeciej sali serii skupiliśmy się na podstawowych i zaawansowanych typach skanowania portów sieciowych.

W ostatnim pomieszczeniu, jak pokazano na poniższym rysunku, skupimy się na tym, jak można używać Nmapa do:

- Wykryj wersje uruchomionych usług (na wszystkich otwartych portach)
- Wykryj system operacyjny na podstawie wszelkich oznak ujawnionych przez cel
- Uruchom traceroute Nmapa
- Uruchom wybrane skrypty Nmap
- Zapisz wyniki skanowania w różnych formatach

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/c9724491cb38c1ebcd83b5b98f13e1d9.png)

W tej sali skupimy się na tych krokach i sposobie ich wykonania po przeskanowaniu portu.
### Wykrywanie usług 

Gdy Nmap wykryje otwarte porty, możesz sprawdzić dostępny #port, aby wykryć działającą usługę. Dalsze badanie otwartych portów jest kluczową informacją, ponieważ pentester może ją wykorzystać do sprawdzenia, czy istnieją znane luki w zabezpieczeniach usługi. Dołącz do [Vulnerabilities 101,](https://tryhackme.com/room/vulnerabilities101) aby dowiedzieć się więcej o wyszukiwaniu podatnych usług.

Dodanie `-sV`polecenia Nmap spowoduje zebranie i określenie informacji o usłudze i wersji dla otwartych portów. Możesz kontrolować intensywność, `--version-intensity LEVEL`gdzie poziom waha się od 0 (najniższy) do 9 (najbardziej kompletny). `-sV --version-light`ma intensywność 2, podczas gdy `-sV --version-all`ma intensywność 9.

Należy pamiętać, że użycie tej opcji `-sV`wymusi na Nmapie przeprowadzenie trzyetapowego uzgadniania TCP i nawiązanie połączenia. Nawiązanie połączenia jest konieczne, ponieważ Nmap nie może wykryć wersji bez pełnego nawiązania połączenia i skomunikowania się z usługą nasłuchującą. Innymi słowy, ukryte skanowanie SYN `-sS`nie jest możliwe po `-sV`wybraniu tej opcji.

Poniższy wynik konsoli przedstawia proste skanowanie SYN programu Nmap z `-sV`opcją stealth. Dodanie tej `-sV`opcji powoduje utworzenie nowej kolumny w wynikach, pokazującej wersję dla każdej wykrytej usługi. Na przykład, w przypadku otwartego portu TCP 22, zamiast `22/tcp open ssh`, otrzymujemy `22/tcp open ssh OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)`. Należy zauważyć, że protokół SSH jest zgadywany jako usługa, ponieważ port TCP 22 jest otwarty; Nmap nie musiał łączyć się z portem 22, aby to potwierdzić. `-sV`Wymagało to jednak połączenia z tym otwartym portem, aby pobrać baner usługi i wszelkie informacje o wersji, takie jak `nginx 1.6.2`. Zatem, w przeciwieństwie do kolumny _usługi_ , kolumna _wersji_ nie jest zgadywana.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sV MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-10 05:03 BST
Nmap scan report for MACHINE_IP
Host is up (0.0040s latency).
Not shown: 995 closed ports
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
25/tcp  open  smtp    Postfix smtpd
80/tcp  open  http    nginx 1.6.2
110/tcp open  pop3    Dovecot pop3d
111/tcp open  rpcbind 2-4 (RPC #100000)
MAC Address: 02:A0:E7:B5:B6:C5 (Unknown)
Service Info: Host:  debra2.thm.local; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.40 seconds
```

Należy pamiętać, że wiele opcji Nmap wymaga uprawnień użytkownika root. Jeśli nie uruchamiasz Nmapa jako root, należy użyć opcji `sudo`jak w powyższym przykładzie.

Uruchom maszynę wirtualną . Gdy będzie gotowa, otwórz terminal w AttackBoxie, aby odpowiedzieć na poniższe pytania.

### Wykrywanie systemu operacyjnego

Nmap potrafi wykryć system operacyjny ( OS ) na podstawie jego zachowania i wszelkich oznak ostrzegawczych w odpowiedziach. Wykrywanie systemu operacyjnego można włączyć za pomocą `-O`; jest to _wielka litera O,_ jak w słowie OS. W tym przykładzie uruchomiliśmy `nmap -sS -O MACHINE_IP`AttackBox. Nmap wykrył, że systemem operacyjnym jest Linux 3.X, a następnie domyślił się, że korzysta z jądra 3.13.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS -O MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-10 05:04 BST
Nmap scan report for MACHINE_IP
Host is up (0.00099s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
MAC Address: 02:A0:E7:B5:B6:C5 (Unknown)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3.13
OS details: Linux 3.13
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.91 seconds
```

System, który przeskanowaliśmy i próbowaliśmy wykryć wersję systemu operacyjnego , działa pod kontrolą jądra w wersji 3.16. W tym przypadku Nmap był w stanie dokonać trafnego odgadnięcia. W innym przypadku przeskanowaliśmy system Fedora Linux z jądrem 5.13.14; jednak Nmap wykrył go jako Linux 2.6.X. Dobra wiadomość jest taka, że ​​Nmap poprawnie wykrył system operacyjny ; gorsza wiadomość jest taka, że ​​wersja jądra była błędna.

Wykrywanie systemu operacyjnego jest bardzo wygodne, ale wiele czynników może wpływać na jego dokładność. Przede wszystkim Nmap musi znaleźć co najmniej jeden otwarty i jeden zamknięty port na komputerze docelowym, aby móc wiarygodnie zgadnąć. Ponadto, odciski palców systemu operacyjnego gościa mogą ulec zniekształceniu ze względu na rosnące wykorzystanie wirtualizacji i podobnych technologii. Dlatego zawsze należy podchodzić do wersji systemu operacyjnego z dystansem.

### Traceroute

Jeśli chcesz, aby Nmap znalazł routery między Tobą a celem, po prostu dodaj `--traceroute`. W poniższym przykładzie Nmap dodał traceroute do wyników skanowania. Należy pamiętać, że traceroute Nmapa działa nieco inaczej niż polecenie `traceroute`dostępne w systemach Linux i macOS lub `tracert`MS Windows. Standardowe polecenie `traceroute`zaczyna się od pakietu o niskim TTL (czasie życia) i stale go zwiększa, aż dotrze do celu. Traceroute Nmapa zaczyna się od pakietu o wysokim TTL i stopniowo go zmniejsza.

W poniższym przykładzie wykonaliśmy polecenie `nmap -sS --traceroute MACHINE_IP`na AttackBoxie. Widzimy, że nie ma między nimi żadnych routerów ani przeskoków, ponieważ są połączone bezpośrednio.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS --traceroute MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-10 05:05 BST
Nmap scan report for MACHINE_IP
Host is up (0.0015s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
MAC Address: 02:A0:E7:B5:B6:C5 (Unknown)

TRACEROUTE
HOP RTT     ADDRESS
1   1.48 ms MACHINE_IP

Nmap done: 1 IP address (1 host up) scanned in 1.59 seconds
```

Warto wspomnieć, że wiele routerów jest skonfigurowanych tak, aby nie wysyłać komunikatu ICMP o przekroczeniu czasu życia (TTL), co uniemożliwiłoby nam odkrycie ich adresów IP. Więcej informacji można znaleźć w sali [Active Reconnaissance](https://tryhackme.com/room/activerecon) .

### Silnik skryptowy NSE

Skrypt to fragment kodu, którego nie trzeba kompilować. Innymi słowy, pozostaje on w oryginalnej, czytelnej dla człowieka formie i nie wymaga konwersji na język maszynowy. Wiele programów zapewnia dodatkową funkcjonalność za pośrednictwem skryptów; co więcej, skrypty umożliwiają dodawanie niestandardowych funkcji, które nie istniały wcześniej za pośrednictwem wbudowanych poleceń. Podobnie, Nmap zapewnia obsługę skryptów w języku Lua. Nmap Scripting Engine (NSE) , będący częścią Nmapa , to interpreter Lua, który umożliwia Nmapowi wykonywanie skryptów Nmap napisanych w języku Lua. Jednak nie musimy uczyć się Lua, aby korzystać ze skryptów Nmapa .

Domyślna instalacja Nmapa może z łatwością zawierać blisko 600 skryptów. Spójrz na folder instalacyjny Nmapa . W AttackBoxie sprawdź pliki w [brakuje nazwy] , a zauważysz, że znajdują się tam setki skryptów, których nazwy zaczynają się od protokołu, którego dotyczą. Poniżej wymieniliśmy wszystkie skrypty rozpoczynające się od HTTP w AttackBoxie; znaleźliśmy około 130 skryptów rozpoczynających się od http. Wraz z kolejnymi aktualizacjami można się spodziewać wzrostu liczby zainstalowanych skryptów.`/usr/share/nmap/scripts`

Terminal testera penetracyjnego

```shell-session
pentester@AttackBox /usr/share/nmap/scripts# ls http*
http-adobe-coldfusion-apsa1301.nse      http-passwd.nse
http-affiliate-id.nse                   http-php-version.nse
http-apache-negotiation.nse             http-phpmyadmin-dir-traversal.nse
http-apache-server-status.nse           http-phpself-xss.nse
http-aspnet-debug.nse                   http-proxy-brute.nse
http-auth-finder.nse                    http-put.nse
http-auth.nse                           http-qnap-nas-info.nse
http-avaya-ipoffice-users.nse           http-referer-checker.nse
http-awstatstotals-exec.nse             http-rfi-spider.nse
http-axis2-dir-traversal.nse            http-robots.txt.nse
http-backup-finder.nse                  http-robtex-reverse-ip.nse
http-barracuda-dir-traversal.nse        http-robtex-shared-ns.nse
http-brute.nse                          http-security-headers.nse
http-cakephp-version.nse                http-server-header.nse
http-chrono.nse                         http-shellshock.nse
http-cisco-anyconnect.nse               http-sitemap-generator.nse
http-coldfusion-subzero.nse             http-slowloris-check.nse
http-comments-displayer.nse             http-slowloris.nse
http-config-backup.nse                  http-sql-injection.nse
http-cookie-flags.nse                   http-stored-xss.nse
http-cors.nse                           http-svn-enum.nse
http-cross-domain-policy.nse            http-svn-info.nse
http-csrf.nse                           http-title.nse
http-date.nse                           http-tplink-dir-traversal.nse
http-default-accounts.nse               http-trace.nse
http-devframework.nse                   http-traceroute.nse
http-dlink-backdoor.nse                 http-unsafe-output-escaping.nse
http-dombased-xss.nse                   http-useragent-tester.nse
http-domino-enum-passwords.nse          http-userdir-enum.nse
http-drupal-enum-users.nse              http-vhosts.nse
http-drupal-enum.nse                    http-virustotal.nse
http-enum.nse                           http-vlcstreamer-ls.nse
http-errors.nse                         http-vmware-path-vuln.nse
http-exif-spider.nse                    http-vuln-cve2006-3392.nse
http-favicon.nse                        http-vuln-cve2009-3960.nse
http-feed.nse                           http-vuln-cve2010-0738.nse
http-fetch.nse                          http-vuln-cve2010-2861.nse
http-fileupload-exploiter.nse           http-vuln-cve2011-3192.nse
http-form-brute.nse                     http-vuln-cve2011-3368.nse
http-form-fuzzer.nse                    http-vuln-cve2012-1823.nse
http-frontpage-login.nse                http-vuln-cve2013-0156.nse
http-generator.nse                      http-vuln-cve2013-6786.nse
http-git.nse                            http-vuln-cve2013-7091.nse
http-gitweb-projects-enum.nse           http-vuln-cve2014-2126.nse
http-google-malware.nse                 http-vuln-cve2014-2127.nse
http-grep.nse                           http-vuln-cve2014-2128.nse
http-headers.nse                        http-vuln-cve2014-2129.nse
http-huawei-hg5xx-vuln.nse              http-vuln-cve2014-3704.nse
http-icloud-findmyiphone.nse            http-vuln-cve2014-8877.nse
http-icloud-sendmsg.nse                 http-vuln-cve2015-1427.nse
http-iis-short-name-brute.nse           http-vuln-cve2015-1635.nse
http-iis-webdav-vuln.nse                http-vuln-cve2017-1001000.nse
http-internal-ip-disclosure.nse         http-vuln-cve2017-5638.nse
http-joomla-brute.nse                   http-vuln-cve2017-5689.nse
http-litespeed-sourcecode-download.nse  http-vuln-cve2017-8917.nse
http-ls.nse                             http-vuln-misfortune-cookie.nse
http-majordomo2-dir-traversal.nse       http-vuln-wnr1000-creds.nse
http-malware-host.nse                   http-waf-detect.nse
http-mcmp.nse                           http-waf-fingerprint.nse
http-method-tamper.nse                  http-webdav-scan.nse
http-methods.nse                        http-wordpress-brute.nse
http-mobileversion-checker.nse          http-wordpress-enum.nse
http-ntlm-info.nse                      http-wordpress-users.nse
http-open-proxy.nse                     http-xssed.nse
http-open-redirect.nse
```

Możesz określić użycie dowolnego lub grupy zainstalowanych skryptów; co więcej, możesz zainstalować skrypty innych użytkowników i używać ich do skanowania. Zacznijmy od skryptów domyślnych. Możesz wybrać uruchamianie skryptów z kategorii domyślnej, używając `--script=default`lub po prostu dodając `-sC`. Oprócz kategorii [domyślnej](https://nmap.org/nsedoc/categories/default.html) , kategorie obejmują uwierzytelnianie, rozgłaszanie, atak brute, atak domyślny, wykrywanie, DOS, exploit, zewnętrzny, fuzzer, intruzywny, malware, bezpieczny, wersja i podatność. Krótki opis znajduje się w poniższej tabeli.

|Kategoria skryptu|Opis|
|---|---|
|`auth`|Skrypty związane z uwierzytelnianiem|
|`broadcast`|Odkryj gospodarzy, wysyłając wiadomości rozgłoszeniowe|
|`brute`|Przeprowadza audyt haseł metodą brute force w odniesieniu do logowań|
|`default`|Skrypty domyślne, takie same jak`-sC`|
|`discovery`|Pobieranie dostępnych informacji, takich jak tabele baz danych i nazwy DNS|
|`dos`|Wykrywa serwery podatne na ataki typu DoS (odmowa usługi )|
|`exploit`|Próby wykorzystania różnych podatnych na ataki usług|
|`external`|Sprawdzanie przy użyciu usługi innej firmy, np. Geoplugin i Virustotal|
|`fuzzer`|Uruchom ataki fuzzingowe|
|`intrusive`|Intruzywne skrypty, takie jak ataki siłowe i wykorzystywanie|
|`malware`|Skanowanie w poszukiwaniu tylnych drzwi|
|`safe`|Bezpieczne skrypty, które nie spowodują awarii systemu docelowego|
|`version`|Pobierz wersje usług|
|`vuln`|Sprawdzanie luk w zabezpieczeniach lub wykorzystywanie podatnych usług|

Niektóre skrypty należą do więcej niż jednej kategorii. Co więcej, niektóre skrypty przeprowadzają ataki siłowe na usługi, podczas gdy inne przeprowadzają ataki DoS i wykorzystują luki w zabezpieczeniach systemów. Dlatego należy zachować ostrożność przy wyborze skryptów do uruchomienia, aby nie dopuścić do awarii usług lub ich wykorzystania.

Używamy Nmapa do uruchomienia skanowania SYN `MACHINE_IP`i wykonania domyślnych skryptów w konsoli pokazanej poniżej. Polecenie `sudo nmap -sS -sC MACHINE_IP`, gdzie , `-sC`zapewni, że Nmap wykona domyślne skrypty po skanowaniu SYN. ​​Poniżej znajdują się nowe szczegóły. Przyjrzyjmy się usłudze SSH na porcie 22; Nmap odzyskał wszystkie cztery klucze publiczne powiązane z działającym serwerem. Rozważmy inny przykład: usługę HTTP na porcie 80; Nmap odzyskał domyślny tytuł strony. Widzimy, że strona została pozostawiona jako domyślna.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS -sC MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-10 05:08 BST
Nmap scan report for ip-10-10-161-170.eu-west-1.compute.internal (10.10.161.170)
Host is up (0.0011s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
| ssh-hostkey: 
|   1024 d5:80:97:a3:a8:3b:57:78:2f:0a:78:ae:ad:34:24:f4 (DSA)
|   2048 aa:66:7a:45:eb:d1:8c:00:e3:12:31:d8:76:8e:ed:3a (RSA)
|   256 3d:82:72:a3:07:49:2e:cb:d9:87:db:08:c6:90:56:65 (ECDSA)
|_  256 dc:f0:0c:89:70:87:65:ba:52:b1:e9:59:f7:5d:d2:6a (EdDSA)
25/tcp  open  smtp
|_smtp-commands: debra2.thm.local, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
| ssl-cert: Subject: commonName=debra2.thm.local
| Not valid before: 2021-08-10T12:10:58
|_Not valid after:  2031-08-08T12:10:58
|_ssl-date: TLS randomness does not represent time
80/tcp  open  http
|_http-title: Welcome to nginx on Debian!
110/tcp open  pop3
|_pop3-capabilities: RESP-CODES CAPA TOP SASL UIDL PIPELINING AUTH-RESP-CODE
111/tcp open  rpcbind
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100024  1          38099/tcp  status
|_  100024  1          54067/udp  status
143/tcp open  imap
|_imap-capabilities: LITERAL+ capabilities IMAP4rev1 OK Pre-login ENABLE have LOGINDISABLEDA0001 listed SASL-IR ID more post-login LOGIN-REFERRALS IDLE
MAC Address: 02:A0:E7:B5:B6:C5 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 2.21 seconds
```

Możesz również określić skrypt według nazwy `--script "SCRIPT-NAME"`, używając wzorca, takiego jak `--script "ftp*"`, który zawierałby `ftp-brute`. Jeśli nie masz pewności, co robi skrypt, możesz otworzyć plik skryptu za pomocą czytnika tekstu, takiego jak `less`, lub edytora tekstu. W przypadku `ftp-brute`, skrypt zawiera następującą informację: „Wykonuje audyt haseł metodą brute force na serwerach FTP ”. Należy zachować ostrożność, ponieważ niektóre skrypty są dość inwazyjne. Ponadto niektóre skrypty mogą być przeznaczone dla konkretnego serwera i, jeśli zostaną wybrane losowo, stracą Twój czas, nie przynosząc żadnych korzyści. Jak zwykle, upewnij się, że masz uprawnienia do uruchamiania takich testów na serwerze docelowym.

Rozważmy nieszkodliwy skrypt, `http-date`który, jak przypuszczamy, pobierałby datę i godzinę z serwera HTTP , co rzeczywiście potwierdza jego opis: „Pobiera datę z usług podobnych do HTTP . Wyświetla również, o ile data różni się od czasu lokalnego…”. W AttackBoxie wykonujemy `sudo nmap -sS -n --script "http-date" MACHINE_IP`polecenie pokazane w konsoli poniżej.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ sudo nmap -sS -n --script "http-date" MACHINE_IP

Starting Nmap 7.60 ( https://nmap.org ) at 2021-09-10 08:04 BST
Nmap scan report for MACHINE_IP
Host is up (0.0011s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
|_http-date: Fri, 10 Sep 2021 07:04:26 GMT; 0s from local time.
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
MAC Address: 02:44:87:82:AC:83 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.78 seconds
```

Wreszcie, możesz rozszerzyć funkcjonalność Nmapa poza oficjalne skrypty Nmapa ; możesz napisać własny skrypt lub pobrać skrypty Nmapa z internetu. Pobieranie i używanie skryptu Nmapa z internetu wiąże się z pewnym ryzykiem. Dlatego dobrze jest nie uruchamiać skryptu od autora, któremu nie ufasz.

### Zapisywanie danych wyjsciowych

Za każdym razem, gdy uruchamiasz skanowanie Nmap , rozsądnym rozwiązaniem jest zapisanie wyników w pliku. Wybór i przyjęcie odpowiedniej konwencji nazewnictwa plików jest również kluczowe. Liczba plików może szybko wzrosnąć i utrudnić znalezienie poprzednich wyników skanowania. Trzy główne formaty to:

1. Normalna
2. Możliwość grepowania ( `grep`możliwość)
3. XML

Jest jeszcze czwarta opcja, której nie możemy polecić:

- Script Kiddie

### Normalna

Jak sama nazwa wskazuje, format normalny jest podobny do wyniku, który pojawia się na ekranie podczas skanowania obiektu. Możesz zapisać skan w formacie normalnym, używając `-oN FILENAME`; N oznacza normalny. Oto przykład wyniku.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ cat MACHINE_IP_scan.nmap 
# Nmap 7.60 scan initiated Fri Sep 10 05:14:19 2021 as: nmap -sS -sV -O -oN MACHINE_IP_scan MACHINE_IP
Nmap scan report for MACHINE_IP
Host is up (0.00086s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
25/tcp  open  smtp    Postfix smtpd
80/tcp  open  http    nginx 1.6.2
110/tcp open  pop3    Dovecot pop3d
111/tcp open  rpcbind 2-4 (RPC #100000)
143/tcp open  imap    Dovecot imapd
MAC Address: 02:A0:E7:B5:B6:C5 (Unknown)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3.13
OS details: Linux 3.13
Network Distance: 1 hop
Service Info: Host:  debra2.thm.local; OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Sep 10 05:14:28 2021 -- 1 IP address (1 host up) scanned in 9.99 seconds
```

### Możliwość grepowania

Format grepowalny wziął swoją nazwę od polecenia `grep`; grep oznacza Global Regular Expression Printer (Globalna Drukarka Wyrażeń Regularnych). Mówiąc prościej, usprawnia on filtrowanie wyników skanowania pod kątem określonych słów kluczowych lub terminów. Wynik skanowania można zapisać w formacie grepowalnym za pomocą polecenia `-oG FILENAME`. Wynik skanowania, wyświetlony powyżej w formacie normalnym, jest wyświetlany w konsoli poniżej w formacie grepowalnym. Standardowy wynik ma 21 wierszy, natomiast wynik grepowalny ma tylko 4 wiersze. Głównym powodem jest to, że Nmap chce, aby każdy wiersz był zrozumiały i kompletny, gdy użytkownik zastosuje polecenie `grep`. W rezultacie wiersze w formacie grepowalnym są tak długie i niewygodne w odczycie w porównaniu ze standardowym wynikiem.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ cat MACHINE_IP_scan.gnmap 
# Nmap 7.60 scan initiated Fri Sep 10 05:14:19 2021 as: nmap -sS -sV -O -oG MACHINE_IP_scan MACHINE_IP
Host: MACHINE_IP	Status: Up
Host: MACHINE_IP	Ports: 22/open/tcp//ssh//OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)/, 25/open/tcp//smtp//Postfix smtpd/, 80/open/tcp//http//nginx 1.6.2/, 110/open/tcp//pop3//Dovecot pop3d/, 111/open/tcp//rpcbind//2-4 (RPC #100000)/, 143/open/tcp//imap//Dovecot imapd/	Ignored State: closed (994)	OS: Linux 3.13	Seq Index: 257	IP ID Seq: All zeros
# Nmap done at Fri Sep 10 05:14:28 2021 -- 1 IP address (1 host up) scanned in 9.99 seconds
```

Przykładowym zastosowaniem `grep`jest `grep KEYWORD TEXT_FILE`; to polecenie wyświetli wszystkie wiersze zawierające podane słowo kluczowe. Porównajmy wynik polecenia using `grep`na standardowym wyjściu i wyjściu z możliwością wyszukiwania grepowalnego. Zauważysz, że pierwsze z nich nie podaje adresu IP hosta. Zamiast tego zwraca `80/tcp open http nginx 1.6.2`, co jest bardzo niewygodne podczas przeglądania wyników skanowania wielu systemów. Drugie z kolei dostarcza w każdym wierszu wystarczającą ilość informacji, takich jak adres IP hosta, aby skanowanie było kompletne.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ grep http MACHINE_IP_scan.nmap 
80/tcp  open  http    nginx 1.6.2
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ grep http MACHINE_IP_scan.gnmap 
Host: MACHINE_IP	Ports: 22/open/tcp//ssh//OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)/, 25/open/tcp//smtp//Postfix smtpd/, 80/open/tcp//http//nginx 1.6.2/, 110/open/tcp//pop3//Dovecot pop3d/, 111/open/tcp//rpcbind//2-4 (RPC #100000)/, 143/open/tcp//imap//Dovecot imapd/	Ignored State: closed (994)	OS: Linux 3.13	Seq Index: 257	IP ID Seq: All zeros
```

### XML

Trzecim formatem jest XML. Wyniki skanowania można zapisać w formacie XML za pomocą `-oX FILENAME`. Format XML jest najwygodniejszy do przetwarzania danych wyjściowych w innych programach. Co więcej, wyniki skanowania można zapisać we wszystkich trzech formatach za pomocą `-oA FILENAME`, `-oN`, `-oG`i `-oX`dla plików normalnych, z możliwością grepowania i XML.

### Script Kiddie

Czwarty format to Script Kiddie. Jak widać, ten format jest bezużyteczny, jeśli chcesz przeszukać wynik skanowania pod kątem interesujących słów kluczowych lub zachować wyniki do wykorzystania w przyszłości. Możesz go jednak użyć do zapisania wyniku skanowania `nmap -sS 127.0.0.1 -oS FILENAME`, wyświetlenia nazwy pliku wyjściowego i wyświetlenia go znajomym, którzy nie są obeznani z technologią, w formacie 31337.

Terminal testera penetracyjnego

```shell-session
pentester@TryHackMe$ cat MACHINE_IP_scan.kiddie 

$tart!ng nMaP 7.60 ( httpz://nMap.0rG ) at 2021-09-10 05:17 B$T
Nmap scan rEp0rt f0r |p-10-10-161-170.EU-w3$t-1.C0mputE.intErnaL (10.10.161.170)
HOSt !s uP (0.00095s LatEncy).
N0T $H0wn: 994 closed pOrtS
PoRT    st4Te SeRViC3 VERS1on
22/tcp  Open  ssH     Op3n$$H 6.7p1 Deb|an 5+dEb8u8 (pr0t0COl 2.0)
25/tCp  Op3n  SmTp    P0$Tf!x Smtpd
80/tcp  0p3n  http    Ng1nx 1.6.2
110/tCP 0pen  pOP3    d0v3coT P0p3D
111/TcP op3n  RpcbInd 2-4 (RPC #100000)
143/Tcp opEn  Imap    Dovecot 1mApd
mAC 4Ddr3sz: 02:40:e7:B5:B6:c5 (Unknown)
Netw0rk d!stanc3: 1 h0p
$3rv1c3 InFO: Ho$t:  dEBra2.thM.lOcal; 0s: Linux; cPe: cP3:/0:linux:l|nux_k3rnel

0S and servIc3 D3tEcti0n pErf0rm3d. Plea$e r3p0rt any !nc0RrecT rE$ultz at hTtpz://nmap.0rg/$ubmit/ .
Nmap d0nE: 1 |P addr3SS (1 hoSt up) $CaNnEd !n 21.80 s3c0Ndz
```
### Podsumowanie

W tej sali nauczyliśmy się, jak wykrywać uruchomione usługi i ich wersje, a także system operacyjny hosta. Dowiedzieliśmy się, jak włączyć traceroute i omówiliśmy wybór jednego lub kilku skryptów wspomagających testy penetracyjne. Na koniec omówiliśmy różne formaty zapisu wyników skanowania do wykorzystania w przyszłości. Poniższa tabela podsumowuje najważniejsze opcje omówione w tej sali.

|Opcja|Oznaczający|
|---|---|
|`-sV`|określ informacje o usłudze/wersji na otwartych portach|
|`-sV --version-light`|wypróbuj najbardziej prawdopodobne sondy (2)|
|`-sV --version-all`|wypróbuj wszystkie dostępne sondy (9)|
|`-O`|wykryj system operacyjny|
|`--traceroute`|uruchom traceroute do celu|
|`--script=SCRIPTS`|Skrypty Nmap do uruchomienia|
|`-sC`Lub`--script=default`|uruchom domyślne skrypty|
|`-A`|odpowiednik`-sV -O -sC --traceroute`|
|`-oN`|zapisz dane wyjściowe w normalnym formacie|
|`-oG`|zapisz dane wyjściowe w formacie grepowalnym|
|`-oX`|zapisz dane wyjściowe w formacie XML|
|`-oA`|zapisz dane wyjściowe w formatach normalnych, XML i grepowalnych|

1 nmap -sC -sV -p- -T4 <MACHINE_IP> -vv
2 nano users.txt
3 cat users.txt
hydra -t 8 -L users.txt -P /usr/share/wordlists/rockyou.txt ftp:10.10.101.15:10021
hydra -t 8 -vV -L /your_path_to_your_usernames_file.txt/your_usernames_file.txt -P /usr/share/rockyou.txt/rockyou.txt ftp://10.129.168.93:10021
