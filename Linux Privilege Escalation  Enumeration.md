---

Eskalacja uprawnień to proces. Nie ma cudownych rozwiązań i wiele zależy od konkretnej konfiguracji systemu docelowego. Wersja jądra, zainstalowane aplikacje, obsługiwane języki programowania i hasła innych użytkowników to kilka kluczowych elementów, które wpłyną na Twoją drogę do uzyskania uprawnień roota. Ten pokój obejmuje wiele…LinuxTechniki eskalacji uprawnień są zaprojektowane tak, aby każda technika była samodzielna i stanowiła odrębne zadanie. Możesz studiować każde zadanie niezależnie, ale zalecamy wykonywanie ich po kolei.

## Co oznacza „eskalacja uprawnień”?

W swojej istocie eskalacja uprawnień zazwyczaj polega na przejściu z konta o niższych uprawnieniach na konto o wyższych. Bardziej technicznie rzecz biorąc, jest to wykorzystanie luki w zabezpieczeniach, błędu projektowego lub niedopatrzenia w konfiguracji systemu operacyjnego lub aplikacji w celu uzyskania nieautoryzowanego dostępu do zasobów, które zazwyczaj są zarezerwowane dla użytkowników.

## Dlaczego to takie ważne?

Podczas przeprowadzania rzeczywistych testów penetracyjnych rzadko udaje się uzyskać dostęp (pierwszy dostęp), który daje bezpośredni dostęp administracyjny. Zazwyczaj dostęp do systemów uzyskuje się najpierw jako użytkownik o niskich uprawnieniach. Eskalacja uprawnień jest kluczowa, ponieważ pozwala uzyskać dostęp na poziomie administratora systemu, co umożliwia wykonywanie takich czynności, jak:

- Resetowanie haseł
- Omijanie kontroli dostępu w celu naruszenia bezpieczeństwa danych chronionych
- Edycja konfiguracji oprogramowania
- Włączanietrwałość  - Enabling persistence
- Zmiana uprawnień istniejących (lub nowych) użytkowników
- Wykonaj dowolne polecenie administracyjne

Ta sala została zaprojektowana tak, aby omówić główne wektory eskalacji uprawnień i zapewnić Ci lepsze zrozumienie tego procesu. Ta nowa umiejętność będzie niezbędnym elementem Twojego arsenału, niezależnie od tego, czy bierzesz udział w CTF-ach, zdajesz egzaminy certyfikacyjne, czy pracujesz jako tester penetracyjny.

## Wymagania wstępne

- [Linux](https://tryhackme.com/module/linux-fundamentals)Moduł [podstawowy](https://tryhackme.com/module/linux-fundamentals)

## Cele edukacyjne

- Zrozumieć cel i znaczenie wyliczania wLinuxeskalacja uprawnień
- Zidentyfikuj kluczSystem operacyjnyinformacje za pomocą ręcznych poleceń wyliczania
- Znajdź ukryte pliki
- Wyliczanie użytkowników, grup i uprawnień naLinuxsystem
- Wymień podstawowe informacje o sieci
- Odkryj potencjalne wektory eskalacji uprawnień poprzez ręczne wyliczanie

To zadanie będzie skupiać się na różnych poleceniach i technikach służących do wyliczania właściwości systemu operacyjnego, takich jak:

- nazwa hosta hostname
- zmienić nazwę  uname
- - /proc/version
- /etc/issue
- ps
- cron
- dpkg

## Dowództwo`hostname`​

Polecenie `hostname`zwróci nazwę hosta komputera docelowego. Chociaż wartość tę można łatwo zmienić lub przyjąć stosunkowo mało znaczący ciąg znaków (np. `Ubuntu-3487340239`), w niektórych przypadkach może ona dostarczyć informacji o roli systemu docelowego w sieci korporacyjnej (np. `SQL-PROD-01`w przypadku systemu produkcyjnego).SQLserwer).

## Dowództwo`uname`​

Polecenie `uname -a`wyświetli informacje o systemie, podając dodatkowe szczegóły dotyczące jądra używanego przez system. Jest to przydatne podczas wyszukiwania potencjalnych luk w zabezpieczeniach jądra, które mogą prowadzić do eskalacji uprawnień.

uname -a

```shell-session
john@home:~$ uname -a
Linux home 6.8.0-41-generic
```

W powyższym przykładzie wynik wygląda następująco:

- **Linux**:System operacyjny
- **dom** : nazwa hosta
- **6.8.0-41-generic** : Wersja jądra

## Plik`/proc/version`​

System plików proc (procfs) dostarcza informacji o procesach systemu docelowego. System proc jest dostępny w wielu różnych wersjach Linuksa, co czyni go niezbędnym narzędziem w arsenale. Zapoznanie się z nim `/proc/version`może dostarczyć informacji o wersji jądra lub kompilatorze użytym do jego utworzenia.

kot /proc/wersja

```shell-session
john@home:~$ cat /proc/version
Linux version 6.8.0-41-generic (buildd@lcy02-amd64-077) (x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0, GNU ld (GNU Binutils for Ubuntu) 2.42)
```

W powyższym przykładzie wynik wygląda następująco:

- **6.8.0-41-generic** : Wersja jądra
- **buildd@lcy02-amd64-077** : Maszyna kompilacji, która skompilowała jądro
- **x86_64-Linux-gnu-gcc-13** : Kompilator używany do budowania jądra
- **Ubuntu 13.2.0-23ubuntu4** : Wersja pakietu Ubuntu kompilatora gcc
- **GNU ld (GNU Binutils dla Ubuntu) 2.42** : Linker używany podczas kompilacji jądra

## Plik`/etc/issue`​

Systemy można również zidentyfikować, patrząc na `/etc/issue`plik. Plik ten zazwyczaj zawiera pewne informacje o systemie operacyjnym, ale można go łatwo dostosować lub zmienić. Ponadto każdy plik zawierający informacje o systemie można dostosować lub zmienić. Aby lepiej zrozumieć system, warto przejrzeć wszystkie te informacje.

kot /etc/issue

```shell-session
john@linux-enumeration:~$ cat /etc/issue
Ubuntu 22.04.1 LTS \n \l
```

W powyższym przykładzie `Ubuntu 22.04.1 LTS`jest to wersja Ubuntu działająca na hoście.

## Dowództwo`ps`​

To `ps`polecenie to skuteczny sposób na wyświetlenie uruchomionych procesów w systemie Linux. Uruchomienie go `ps`w terminalu wyświetli procesy dla bieżącej powłoki.

Wynik polecenia `ps` (Status procesu) będzie wyglądał następująco:

- **PID** : Identyfikator procesu (unikalny dla procesu)
- **TTY** : Typ terminala używanego przez użytkownika
- **Czas** : Ilość czasu procesora wykorzystanego przez proces (NIE jest to czas trwania działania tego procesu)
- **CMD** : Polecenie lub plik wykonywalny uruchomiony (NIE wyświetli żadnych parametrów wiersza polecenia)

Polecenie `ps`udostępnia kilka przydatnych opcji.

- `ps aux`:Ta `aux`opcja pokaże procesy wszystkich użytkowników `a`, wyświetli użytkownika, który uruchomił proces `u`, oraz procesy, które nie są powiązane z terminalem `x`. Analiza `ps aux`wyników polecenia pozwala lepiej zrozumieć system i potencjalne luki w zabezpieczeniach.
- `ps axjf`:Ta `axjf`opcja wyświetli procesy wszystkich użytkowników `a`, uwzględni procesy, które nie mają terminala sterującego `x`, użyje danych wyjściowych w formacie zadań `j`oraz widoku lasu/drzewa `f`. Przykład takiego drzewa można zobaczyć poniżej.

ps axjf

```shell-session
john@linux-enumeration:~$ ps axjf    1  1039  1039  1039 ?           -1 Ss       0   0:00 /usr/sbin/sshd -D
 1039  1854  1854  1854 ?           -1 Ss       0   0:00  \_ sshd: karen [priv]  
 1854  1890  1854  1854 ?           -1 S     1001   0:00      \_ sshd: karen@pts/0   
 1890  1891  1891  1891 pts/0     1975 Ss    1001   0:00          \_ -sh
 1891  1975  1975  1891 pts/0     1975 R+    1001   0:00              \_ ps axjf
```

## Usługa`cron`​

Cron to harmonogram zadań oparty na czasie w systemie Linux, który umożliwia użytkownikom i systemowi planowanie automatycznego uruchamiania poleceń lub skryptów w określonych odstępach czasu. Zadania cron są często używane do zadań takich jak tworzenie kopii zapasowych, rotacja logów czy uruchamianie skryptów konserwacyjnych. Podczas enumeracji warto sprawdzić, czy występują zadania cron, ponieważ czasami są one uruchamiane przez użytkowników uprzywilejowanych. Jeśli zadanie cron uruchamia skrypt, który można modyfikować, może to stać się potencjalnym wektorem eskalacji.

Możesz zacząć od sprawdzenia `/etc/crontab`i wylistowania zawartości pliku `/var/spool/cron/`lub , `/etc/cron.d/`aby zobaczyć, co jest zaplanowane i, co ważniejsze, kto je uruchamia. Później dowiesz się, jak wykorzystać błędnie skonfigurowane zadania cron, ale na razie ważne jest, aby uwzględnić je na liście kontrolnej enumeracji.

Poniżej znajduje się przykład wpisu `/etc/crontab`.

kot /etc/crontab

```shell-session
30 2 * * 1 root /home/ubuntu/clear-mail.sh
```

Wynik jest następujący:

- Pierwsze pole określa minutę, w której skrypt ma zostać uruchomiony (zakres prawidłowy: 0–59)
- Drugie pole wskazuje godzinę, o której skrypt ma zostać uruchomiony (zakres dopuszczalnych wartości: 0–23)
- Trzecie pole określa dzień miesiąca, w którym skrypt ma zostać uruchomiony (zakres dopuszczalnych wartości: 1–31)
- Czwarte pole wskazuje miesiąc, w którym skrypt ma zostać uruchomiony (zakres dopuszczalnych wartości: 1–12)
- Piąte pole określa dzień tygodnia, w którym skrypt ma zostać uruchomiony (zakres dopuszczalnych wartości: 0–7, przy czym zarówno 0, jak i 7 oznaczają niedzielę).
- Szóste pole przedstawia użytkownika, który uruchomi zadanie
- Ostatnie pole przedstawia zadanie do wykonania, które może być dowolnym skryptem lub plikiem binarnym, pod warunkiem, że jest wykonywalny

Podsumowując, powyższy plik crontab jest uruchamiany `/home/ubuntu/clear-mail.sh` **w każdy poniedziałek**  o **2:30 w nocy** przez użytkownika **root** .

## Dowództwo`dpkg`​

Narzędzie `dpkg`pozwala nam sprawdzić wszystkie zainstalowane pakiety i ich wersje. Jest to szczególnie przydatne w przypadku prób eskalacji uprawnień, gdy szukamy podatnych plików binarnych ze znanymi exploitami.

Poleceniem wyświetlającym listę zainstalowanego oprogramowania jest `dpkg -l`.

Zadanie to będzie skupiać się na uzyskiwaniu informacji o użytkownikach lokalnych za pomocą poleceń i plików, takich jak:

- id
- środowisko   env
- history
- sudo -l
- /etc/password

## Dowództwo`id`​

Polecenie `id`zapewni ogólny przegląd poziomu uprawnień użytkownika i członkostwa w grupach. Warto pamiętać, że polecenie id można również wykorzystać do uzyskania tych samych informacji o innym użytkowniku, jak pokazano poniżej:

id

```shell-session
john@home:~$ iduid=1001(john) gid=1001(john) groups=1001(john),100(users)john@home:~$ id mattuid=1002(matt) gid=1002(matt) groups=1002(matt),27(sudo),116(admin)
```

## Dowództwo`env`​

Polecenie `env` wyświetli zmienne środowiskowe.

środowisko

```shell-session
john@home:~$ env
MAIL=/var/mail/john
USER=john
SSH_CLIENT=10.80.88.217 50500 22
HOME=/home/john
SSH_TTY=/dev/pts/0
QT_QPA_PLATFORMTHEME=appmenu-qt5
LOGNAME=john
TERM=linux
```

Zmienna PATH może zawierać kompilator lub język skryptowy (np. Python), który można wykorzystać do uruchomienia kodu w systemie docelowym lub do eskalacji uprawnień.

## Dowództwo`history`​

Przyjrzenie się wcześniejszym poleceniom za pomocą  `history` polecenia może dać nam pewien pogląd na temat systemu docelowego i, choć rzadko, zapisać informacje, takie jak hasła lub nazwy użytkowników.

## Dowództwo`sudo -l`​

System docelowy może być skonfigurowany tak, aby zezwalał użytkownikom na uruchamianie niektórych (lub wszystkich) poleceń z uprawnieniami użytkownika root. `sudo -l`Polecenie to umożliwia wyświetlenie listy wszystkich poleceń, które użytkownik może uruchomić za pomocą sudo. W zależności od konfiguracji, podczas uruchamiania polecenia może być wymagane podanie hasła bieżącego użytkownika `sudo`.

## Plik`/etc/passwd`​

Przeczytanie `/etc/passwd`pliku może okazać się łatwym sposobem odkrycia użytkowników systemu.

kot /etc/passwd

```shell-session
john@home:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
```

Mimo że dane wyjściowe mogą być długie i nieco przerażające, można je łatwo wyciąć i przekształcić w listę przydatną do ataków siłowych.

kot /etc/passwd | cut -d ":" -f 1

```shell-session
john@home:~$ cat /etc/passwd | cut -d ":" -f 1rootdaemonbinsyssyncgamesmanlpmailnewsuucpproxywww-databackuplistircgnatsnobodylibuuid
```

Pamiętaj, że zwróci to wszystkich użytkowników, z których niektórzy to użytkownicy systemu lub usług, co nie byłoby zbyt przydatne. Innym podejściem może być wyszukiwanie w programie Grep w poszukiwaniu „domu”, ponieważ prawdziwi użytkownicy najprawdopodobniej będą mieli swoje foldery w katalogu „domowym”.

kot /etc/passwd | grep /home

```shell-session
john@home:~$ cat /etc/passwd | grep /home
matt:x:1000:1000:matt,,,:/home/matt:/bin/bash
karen:x:1001:1001::/home/karen:
```

cat ~/.bash_history,  cat /etc/passwd | grep 'Mailing List Manager'

W tym zadaniu poznasz `ifconfig`i `netstat`oraz wykorzystasz je, aby uzyskać informacje o interfejsach sieciowych i portach nasłuchujących.

## Dowództwo`ifconfig`​

System docelowy może być punktem zwrotnym dla innej sieci. Polecenie `ifconfig`podaje informacje o interfejsach sieciowych systemu. Na przykład w poniższym fragmencie kodu widać interfejs Dockera, co sugeruje, że Docker prawdopodobnie działa na hoście.

ifconfig

```shell-session
john@home:~$ ifconfig
docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:2aff:feef:cb59  prefixlen 64  scopeid 0x20<link>
        ether 02:42:2a:ef:cb:59  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 38  bytes 5128 (5.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0ens5: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9001        inet 10.80.96.65  netmask 255.255.192.0  broadcast 10.80.127.255        inet6 fe80::89f:a8ff:fed4:b8e9  prefixlen 64  scopeid 0x20<link>        ether 0a:9f:a8:d4:b8:e9  txqueuelen 1000  (Ethernet)        RX packets 14085  bytes 14572272 (14.5 MB)        RX errors 0  dropped 0  overruns 0  frame 0        TX packets 4151  bytes 7292416 (7.2 MB)        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

W nowoczesnych dystrybucjach Linuksa polecenie to zostało zastąpione poleceniem `ip`. Odpowiednikiem ifconfig jest `ip addr`. , `ifconfig`które nadal jest częścią pakietu `net-tools`.

## Dowództwo`netstat`​

Po wstępnym sprawdzeniu istniejących interfejsów i tras sieciowych warto przyjrzeć się istniejącej komunikacji. Polecenie netstat można użyć z kilkoma różnymi opcjami, aby zebrać informacje o istniejących połączeniach.

`netstat -a` pokazuje wszystkie porty nasłuchujące i nawiązane połączenia.

`netstat -at`lub `netstat -au`można go również użyć do wyświetlenia odpowiednio protokołów TCP lub UDP.

`netstat -l`Wyświetla listę portów w trybie „nasłuchiwania”. Porty te są otwarte i gotowe do przyjmowania połączeń przychodzących. Można to wykorzystać z opcją `-t`wyświetlania listy tylko portów nasłuchujących za pomocą protokołu TCP, jak pokazano poniżej:

netstat -lt

```shell-session
john@home:~$ netstat -lt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:ldap            0.0.0.0:*               LISTEN     
tcp        0      0 localhost:postgresql    0.0.0.0:*               LISTEN     
tcp        0      0 localhost:5433          0.0.0.0:*               LISTEN 
```

`netstat -s`Wyświetla statystyki wykorzystania sieci według protokołu. Można tego również użyć z opcjami `-t`lub `-u`, aby ograniczyć dane wyjściowe do określonego protokołu.

netstat -s

```shell-session
john@home:~$ netstat -s
Ip:
    Forwarding: 1
    66019 total packets received
    5 with invalid addresses
    0 forwarded
    0 incoming packets discarded
    66012 incoming packets delivered
    60939 requests sent out
    74 outgoing packets dropped
Icmp:
    156 ICMP messages received
    0 input ICMP message failed
    ICMP input histogram:
        destination unreachable: 156
    156 ICMP messages sent
    0 ICMP messages failed
    ICMP output histogram:
        destination unreachable: 156
```

`netstat -tp`wyświetla połączenia wraz z nazwą usługi i informacjami PID.

netstat -tp

```shell-session
john@home~$ netstat -tp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 10.80.96.65:55010       172.31.66.192:9092      TIME_WAIT   -                   
tcp        0      0 localhost:5901          localhost:55988         ESTABLISHED
```

Można tego również użyć z `-l`opcją listy nasłuchujących portów/usług. `-n`Flaga ta informuje netstat o wyświetlaniu adresów numerycznych i numerów portów zamiast ich rozwiązywania.

netstat -tpl

```shell-session
john@home~$ netstat -tpln
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:389            0.0.0.0:*               LISTEN
```

Możesz zobaczyć „PIDKolumna „/Nazwa programu” jest pusta, ponieważ ten proces należy do innego użytkownika. Poniżej znajduje się to samo polecenie uruchomione z uprawnieniami roota, które ujawnia te informacje jako `1144/slapd`.

netstat -tpl

```shell-session
john@home~$ netstat -tpln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:389            0.0.0.0:*               LISTEN      1144/slapd
```

`netstat -i`pokazuje statystyki interfejsu.

netstat -i

```shell-session
john@home~$ netstat -i
Kernel Interface table
Iface      MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
docker0   1500        0      0      0 0            72      0      0      0 BMRU
ens5      9001    75667      0      0 0         54412      0      0      0 BMRU
```

Najczęściej spotykanym zastosowaniem netstat we wpisach na blogach, opracowaniach i kursach jest `netstat -ano`to, co można podzielić w następujący sposób;

- `-a`: Wyświetl wszystkie gniazda
- `-n`: Nie rozwiązuj nazw
- `-o`: Wyświetlanie timerów

netstat -ano

```shell-session
john@home:~$ netstat -ano
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       Timer
tcp        0      0 0.0.0.0:389             0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.1:5433          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:53              0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:5901            0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:6001            0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN
```

W nowoczesnych dystrybucjach Linuksa `netstat`polecenie zostało zastąpione poleceniem `ss`. Rdzeń jest zasadniczo taki sam, z pewnymi subtelnymi różnicami, takimi jak przeniesienie informacji o routingu do IP i dodanie kilku nowych funkcjonalności. Na przykład `ss -tpl`odpowiednik polecenia `netstat -tpl`. `netstat`nadal istnieje jako część pakietu `net-tools`.

W tym zadaniu poszerzysz swoją wiedzę `ls`na `find` temat lokalizowania poufnych plików w systemach Linux.

## Dowództwo`ls`​

Jedno z najczęściej używanych poleceńLinuxPrawdopodobnie jest to `ls`… . Szukając potencjalnych wektorów eskalacji uprawnień, pamiętaj, aby zawsze używać `ls`polecenia z `-la`parametrem. Poniższy przykład pokazuje, jak łatwo można przeoczyć plik „secret.txt” za pomocą poleceń `ls`lub `ls -l`.

ls

```shell-session
john@home:~$ ls
john@home:~$ ls -l
total 0
john@home~$ ls -la
total 24
drwxrwxrwt  4 root  root  4096 Feb 16 04:36 .
drwxr-xr-x 23 root  root  4096 Jun 18  2021 ..
drwxrwxrwt  2 root  root  4096 Feb 16 04:25 .ICE-unix
-rw-rw-r--  1 karen karen   23 Feb 16 04:36 .secret.txt
-r--r--r--  1 root  root    11 Feb 16 04:25 .X0-lock
drwxrwxrwt  2 root  root  4096 Feb 16 04:25 .X11-unix
john@home:~$ cat .secret.txt
This is a secret file.
```

## Dowództwo`find`​

Przeszukanie systemu docelowego w poszukiwaniu ważnych informacji i potencjalnych wektorów eskalacji uprawnień może okazać się owocne. Wbudowane `find`polecenie jest przydatne i warto je mieć w swoim arsenale.

Poniżej znajdziesz kilka przydatnych przykładów polecenia `find`.

**Znajdź pliki:**

- `find . -name flag1.txt`wyszukuje plik o nazwie „flag1.txt” w bieżącym katalogu i podkatalogach rekurencyjnie
- `find /home -name flag1.txt`wyszukuje nazwy plików „flag1.txt” w katalogu /home i podkatalogach rekurencyjnie
- `find / -type d -name config`znajduje katalog o nazwie config w „/”
- `find / -type f -perm 0777`wyszukuje pliki z uprawnieniami 777 (pliki możliwe do odczytu, zapisu i wykonania przez wszystkich użytkowników)
- `find / -perm -a=x`znajduje pliki wykonywalne
- `find /home -user frank`znajduje wszystkie pliki użytkownika „frank” w katalogu „/home”
- `find / -mtime -10` wyszukuje pliki, które zostały zmodyfikowane w ciągu ostatnich 10 dni
- `find / -atime -10`wyszukuje pliki, do których uzyskiwano dostęp w ciągu ostatnich 10 dni
- `find / -cmin -60`wyszukuje pliki zmienione w ciągu ostatniej godziny (60 minut)
- `find / -amin -60`wyszukuje pliki, do których uzyskano dostęp w ciągu ostatniej godziny (60 minut)
- `find / -size +50M`wyszukuje pliki o rozmiarze co najmniej 50 MB

Tego polecenia można również używać ze znakami (+) i (-), aby określić plik większy lub mniejszy od podanego rozmiaru.

znajdź / -rozmiar +100M

```shell-session
john@home:~$ find / -size +100M
/john/.ZAP/plugin/ZAP_2.15.0_Linux.tar.gz
/john/.gradle/wrapper/dists/gradle-6.8-bin/1jblhjyydfkclfzx1agp92nyl/gradle-6.8-bin.zip
```

Powyższy przykład zwraca pliki większe niż 100 MB. Należy pamiętać, że polecenie `find`ma tendencję do generowania błędów, co czasami utrudnia odczyt danych wyjściowych. Aby temu zaradzić, możemy użyć `2>/dev/null`, które wysyła błędy do `/dev/null`, skutecznie je ignorując.

Foldery i pliki, do których można zapisywać lub z których można wykonywać dane:

- `find / -writable -type d 2>/dev/null`wyszukuje foldery, w których każdy może zapisywać.
- `find / -perm -222 -type d 2>/dev/null`wyszukuje foldery, w których każdy może zapisywać.
- `find / -perm -o w -type d 2>/dev/null`wyszukuje foldery, w których każdy może zapisywać.

Powód, dla którego widzisz trzy różne `find`polecenia, które potencjalnie mogą prowadzić do tego samego rezultatu, można znaleźć w dokumentacji podręcznika. Jak widać poniżej, parametr perm wpływa na sposób `find`działania.

-perm użycie

```shell-session
       -perm mode
              File's  permission  bits  are  exactly mode (octal or symbolic).
              Since an exact match is required, if you want to use  this  form
              for  symbolic  modes,  you  may have to specify a rather complex
              mode string.  For example `-perm  g=w'  will  only  match  files
              which  have  mode 0020 (that is, ones for which group write per\u2010
              mission is the only permission set).  It is more likely that you
              will want to use the `/' or `-' forms, for example `-perm -g=w',
              which matches any file with group write permission.  See the EX\u2010
              AMPLES section for some illustrative examples.

       -perm -mode
              All  of the permission bits mode are set for the file.  Symbolic
              modes are accepted in this form, and this is usually the way  in
              which  you would want to use them.  You must specify `u', `g' or
              `o' if you use a symbolic mode.  See the  EXAMPLES  section  for
              some illustrative examples.

       -perm /mode
              Any  of the permission bits mode are set for the file.  Symbolic
              modes are accepted in this form.  You must specify `u',  `g'  or
              `o'  if  you  use a symbolic mode.  See the EXAMPLES section for
              some illustrative examples.
```

- `find / -perm -o x -type d 2>/dev/null`znajduje foldery wykonywalne dla całego świata

Znajdź narzędzia programistyczne i obsługiwane języki:

- `find / -name perl*`
- `find / -name python*`
- `find / -name gcc*`

Symbole wieloznaczne można stosować, gdy nie znasz dokładnej nazwy pliku, którego szukasz. Załóżmy na przykład, że chcesz znaleźć plik tekstowy zawierający hasła. Możesz użyć następującego polecenia.

- `find / -name pass*.txt`

Powyższe polecenie znajdzie nazwy plików takie jak `pass.txt`, `password.txt`, `passwords.txt`itd.

Poniżej znajduje się krótki przykład wyszukiwania plików z ustawionym bitem SUID. Bit SUID pozwala plikowi uruchomić się z poziomem uprawnień konta, do którego jest on przypisany, a nie konta, które go uruchamia. 

- `find / -perm -u=s -type f 2>/dev/null`wyszukuje pliki z bitem SUID, który umożliwia uruchomienie pliku z wyższym poziomem uprawnień niż bieżący użytkownik.

john@linux-enumeration:~$ cat .hidden_secret.txt
john@linux-enumeration:~$ find / -name "*TryHackMe*" 2>/dev/null
john@linux-enumeration:~$ cat /var/local/TryHackMe-flag.txt

W tym pokoju dowiedziałeś się:

- Jak znaleźć informacje o systemie, który Cię interesuje
- Jak wyliczyć użytkowników lokalnych
- Jak wykorzystać `ifconfig`i `netstat`uzyskać informacje o połączeniach sieciowych
- Jak znaleźć interesujące lub ukryte pliki w systemach Linux

Jak widać, można uzyskać wiele informacji o systemie docelowym, które niekoniecznie wskazują jasną ścieżkę eskalacji, ale pomagają w eskalacji uprawnień. Poświęć trochę czasu na oswojenie się z poleceniami takimi jak  `find`, `locate`, `grep`, `cut`, `sort`, itd.
