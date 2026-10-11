---

Eskalacja uprawnień to proces. Nie ma cudownych rozwiązań i wiele zależy od konkretnej konfiguracji systemu docelowego. Wersja jądra, zainstalowane aplikacje, obsługiwane języki programowania i hasła innych użytkowników to kilka kluczowych elementów, które wpłyną na Twoją drogę do uzyskania uprawnień roota.  
  
Ta sala została zaprojektowana tak, aby omówić główne wektory eskalacji uprawnień i zapewnić Ci lepsze zrozumienie tego procesu. Ta nowa umiejętność będzie niezbędna w Twoim arsenale, niezależnie od tego, czy bierzesz udział w CTF-ach, zdajesz egzaminy certyfikacyjne, czy pracujesz jako tester penetracyjny.

## Czym jest eskalacja uprawnień

Co oznacza „eskalacja uprawnień”?

W swojej istocie eskalacja uprawnień zazwyczaj polega na przejściu z konta o niższych uprawnieniach na konto o wyższych. Bardziej technicznie rzecz biorąc, jest to wykorzystanie luki w zabezpieczeniach, błędu projektowego lub niedopatrzenia w konfiguracji systemu operacyjnego lub aplikacji w celu uzyskania nieautoryzowanego dostępu do zasobów, które zazwyczaj są niedostępne dla użytkowników.  

Dlaczego to takie ważne?

Podczas przeprowadzania rzeczywistych testów penetracyjnych rzadko udaje się uzyskać dostęp (pierwszy dostęp), który daje bezpośredni dostęp administracyjny. Eskalacja uprawnień jest kluczowa, ponieważ pozwala uzyskać dostęp na poziomie administratora systemu, co umożliwia wykonywanie takich czynności, jak:

- Resetowanie haseł  
    
- Omijanie kontroli dostępu w celu naruszenia bezpieczeństwa danych chronionych
- Edycja konfiguracji oprogramowania
- Włączanie trwałość
- Zmiana uprawnień istniejących (lub nowych) użytkowników
- Wykonaj dowolne polecenie administracyjne
## Enumeracja wyliczenie

**Uwaga: Aby wykonać czynność, uruchom maszynę docelową podłączoną do tego zadania.**

**Możesz uruchomić maszynę docelową i uzyskać do niej dostęp bezpośrednio z przeglądarki.**

**Alternatywnie, możesz uzyskać do niego dostęp przezSSHz poniższymi danymi uwierzytelniającymi użytkownika o niskich uprawnieniach:  
**

**Nazwa użytkownika: karen**

**Hasło: Hasło1**

Enumeracja to pierwszy krok, który należy wykonać po uzyskaniu dostępu do dowolnego systemu. Możliwe, że uzyskano dostęp do systemu, wykorzystując krytyczną lukę w zabezpieczeniach, która umożliwiła dostęp na poziomie root, lub po prostu znaleziono sposób na wysyłanie poleceń z konta o niskich uprawnieniach. Testy penetracyjne, w przeciwieństwie do maszyn CTF, nie kończą się po uzyskaniu dostępu do określonego systemu lub poziomu uprawnień użytkownika. Jak zobaczysz, enumeracja jest równie ważna w fazie po ataku, jak i przed nim.

### nazwa hosta

Polecenie `hostname` zwróci nazwę hosta komputera docelowego. Chociaż wartość tę można łatwo zmienić lub może ona zawierać stosunkowo mało znaczący ciąg znaków (np. Ubuntu-3487340239), w niektórych przypadkach może ona dostarczyć informacji o roli systemu docelowego w sieci korporacyjnej (np. SQL-PROD-01 dla produkcyjnego serwera SQL).

### uname -a

Wyświetli informacje o systemie, które dostarczą nam dodatkowych szczegółów na temat jądra używanego przez system. Będzie to przydatne podczas wyszukiwania potencjalnych luk w jądrze, które mogłyby prowadzić do eskalacji uprawnień.

### /proc/wersja

System plików proc (procfs) dostarcza informacji o procesach systemu docelowego. System proc jest dostępny w wielu wersjach Linuksa, co czyni go niezbędnym narzędziem w arsenale.

Przeglądanie tej opcji `/proc/version`może dostarczyć informacji o wersji jądra i dodatkowych danych, na przykład czy zainstalowany jest kompilator (np. GCC).  

### /etc/problem

Systemy można również zidentyfikować, patrząc na `/etc/issue`plik. Plik ten zazwyczaj zawiera pewne informacje o systemie operacyjnym, ale można go łatwo dostosować lub zmienić. Skoro już o tym mowa, każdy plik zawierający informacje o systemie można dostosować lub zmienić. Aby lepiej zrozumieć system, warto przyjrzeć się wszystkim tym informacjom.

### polecenie ps

To `ps` polecenie to skuteczny sposób na wyświetlenie uruchomionych procesów w systemie Linux. Wpisanie go `ps` w terminalu spowoduje wyświetlenie procesów dla bieżącej powłoki.

Wynik polecenia `ps` (Status procesu) będzie wyglądał następująco:

- PID: Identyfikator procesu (unikalny dla procesu)
- TTY: Typ terminala używanego przez użytkownika
- Czas: Ilość czasu procesora wykorzystanego przez proces (NIE jest to czas trwania działania tego procesu)
- CMD: Polecenie lub plik wykonywalny uruchomiony (NIE wyświetli żadnych parametrów wiersza polecenia)

Polecenie „ps” udostępnia kilka przydatnych opcji.

- `ps -A`: Wyświetl wszystkie uruchomione procesy
- `ps axjf`: Zobacz drzewo procesów (zobacz formację drzewa, aż do `ps axjf`uruchomienia poniżej)

![](https://assets.tryhackme.com/additional/imgur/xsbohSd.png)  

- `ps aux`:Ta `aux` opcja pokaże procesy wszystkich użytkowników (a), wyświetli użytkownika, który uruchomił proces (u) oraz pokaże procesy, które nie są powiązane z terminalem (x). Patrząc na wynik polecenia ps aux, możemy lepiej zrozumieć system i potencjalne luki w zabezpieczeniach.  

### środowisko

Polecenie `env` wyświetli zmienne środowiskowe.

![](https://assets.tryhackme.com/additional/imgur/LWdJ8Fw.png)

Zmienna PATH może zawierać kompilator lub język skryptowy (np. Python), który można wykorzystać do uruchomienia kodu w systemie docelowym lub do eskalacji uprawnień.

### sudo -l

System docelowy można skonfigurować tak, aby zezwalał użytkownikom na uruchamianie niektórych (lub wszystkich) poleceń z uprawnieniami roota. Polecenie to `sudo -l` umożliwia wyświetlenie listy wszystkich poleceń, które użytkownik może uruchomić za pomocą `sudo`.

ls

Jednym z najczęściej używanych poleceń w systemie Linux jest prawdopodobnie `ls`.

Szukając potencjalnych wektorów eskalacji uprawnień, pamiętaj, aby zawsze używać `ls` polecenia z `-la` parametrem. Poniższy przykład pokazuje, jak łatwo przeoczyć plik „secret.txt” za pomocą poleceń `ls` lub `ls -l` .

![](https://assets.tryhackme.com/additional/imgur/2jOtOat.png)  

### Id

Polecenie `id` zapewni ogólny przegląd poziomu uprawnień użytkownika i członkostwa w grupach.

Warto pamiętać, że `id` polecenie to można wykorzystać również do uzyskania tych samych informacji dla innego użytkownika, jak pokazano poniżej.

![](https://assets.tryhackme.com/additional/imgur/YzfJliG.png)

### /etc/passwd

Przeczytanie `/etc/passwd`pliku może okazać się łatwym sposobem odkrycia użytkowników systemu.

![](https://assets.tryhackme.com/additional/imgur/r6oYOEi.png)

Mimo że dane wyjściowe mogą być długie i nieco przerażające, można je łatwo wyciąć i przekształcić w listę przydatną do ataków siłowych.

![](https://assets.tryhackme.com/additional/imgur/cpS2U93.png)

Pamiętaj, że zwróci to wszystkich użytkowników, z których część to użytkownicy systemowi lub usług, co nie byłoby zbyt przydatne. Innym podejściem może być wyszukiwanie w programie Grep w poszukiwaniu „domu”, ponieważ prawdziwi użytkownicy najprawdopodobniej będą mieli swoje foldery w katalogu „domowym”.

![](https://assets.tryhackme.com/additional/imgur/psxE6V4.png)

### historia

Przyjrzenie się wcześniejszym poleceniom za pomocą  `history` polecenia może dać nam pewne wyobrażenie o systemie docelowym i, choć rzadko, o zapisanych informacjach, takich jak hasła lub nazwy użytkowników.

### ifconfig

System docelowy może być punktem zwrotnym dla innej sieci. Polecenie `ifconfig` dostarczy nam informacji o interfejsach sieciowych systemu. Poniższy przykład pokazuje, że system docelowy ma trzy interfejsy (eth0, tun0 i tun1). Nasz atakujący komputer może uzyskać dostęp do interfejsu eth0, ale nie może bezpośrednio uzyskać dostępu do dwóch pozostałych sieci.

![](https://assets.tryhackme.com/additional/imgur/hcdZnwK.png)

Można to sprawdzić za pomocą `ip route` polecenia, aby zobaczyć, które trasy sieciowe istnieją.

![](https://assets.tryhackme.com/additional/imgur/PSrmz5O.png)
 
### netstat

Po wstępnym sprawdzeniu istniejących interfejsów i tras sieciowych warto przyjrzeć się istniejącej komunikacji. Polecenie `netstat`można użyć z kilkoma różnymi opcjami, aby zebrać informacje o istniejących połączeniach.

- `netstat -a`: pokazuje wszystkie porty nasłuchujące i nawiązane połączenia.
- `netstat -at`lub `netstat -au`można go również użyć do wyszczególnienia protokołów TCP lub UDP.
- `netstat -l`: lista portów w trybie „nasłuchiwania”. Porty te są otwarte i gotowe do przyjmowania połączeń przychodzących. Można tego użyć z opcją „t”, aby wyświetlić tylko porty nasłuchujące za pomocąTCPprotokół (poniżej)

![](https://assets.tryhackme.com/additional/imgur/BbLdyrr.png)

- `netstat -s`:wyświetla statystyki wykorzystania sieci według protokołu (poniżej). Można tego również używać z opcjami `-t` lub `-u` , aby ograniczyć dane wyjściowe do określonego protokołu.

![](https://assets.tryhackme.com/additional/imgur/mc8OWP0.png)

- `netstat -tp`:wyświetla listę połączeń wraz z nazwą usługi i informacjami PID.

![](https://assets.tryhackme.com/additional/imgur/fDYQwbW.png)

Można tego również użyć z `-l` opcją wyświetlenia listy portów nasłuchujących (poniżej)

![](https://assets.tryhackme.com/additional/imgur/JK7DNv0.png)

Możemy zobaczyć „PIDKolumna „Nazwa programu” jest pusta, ponieważ ten proces należy do innego użytkownika.

Poniżej znajduje się to samo polecenie uruchomione z uprawnieniami roota, które ujawnia te informacje jako 2641/nc (netcat)

![](https://assets.tryhackme.com/additional/imgur/FjZHqlY.png)`   `

- `netstat -i`:Pokazuje statystyki interfejsu. Poniżej widać, że „eth0” i „tun0” są bardziej aktywne niż „tun1”.

![](https://assets.tryhackme.com/additional/imgur/r6IjpmZ.png)

`netstat` Najczęściej spotykane zastosowanie we wpisach na blogach, artykułach i kursach można `netstat -ano` podzielić w następujący sposób:

- `-a`: Wyświetl wszystkie gniazda
- `-n`: Nie rozwiązuj nazw
- `-o`: Wyświetlanie timerów

![](https://assets.tryhackme.com/additional/imgur/UxzLBRw.png)

### znajdź polecenie

Przeszukanie systemu docelowego w poszukiwaniu ważnych informacji i potencjalnych wektorów eskalacji uprawnień może okazać się owocne. Wbudowane polecenie „find” jest przydatne i warto je mieć w swoim arsenale.

Poniżej znajdziesz kilka przydatnych przykładów polecenia „find”.

**Znajdź pliki:**

- `find . -name flag1.txt`:znajdź plik o nazwie „flag1.txt” w bieżącym katalogu
- `find /home -name flag1.txt`: znajdź nazwy plików „flag1.txt” w katalogu /home
- `find / -type d -name config`: znajdź katalog o nazwie config w „/”
- `find / -type f -perm 0777`:znajdź pliki z uprawnieniami 777 (pliki możliwe do odczytu, zapisu i wykonania przez wszystkich użytkowników)
- `find / -perm a=x`:znajdź pliki wykonywalne
- `find /home -user frank`:znajdź wszystkie pliki użytkownika „frank” w „/home”
- `find / -mtime 10`:znajdź pliki, które zostały zmodyfikowane w ciągu ostatnich 10 dni
- `find / -atime 10`:znajdź pliki, do których uzyskano dostęp w ciągu ostatnich 10 dni
- `find / -cmin -60`:znajdź pliki zmienione w ciągu ostatniej godziny (60 minut)
- `find / -amin -60`:znajdź dostępy do plików w ciągu ostatniej godziny (60 minut)
- `find / -size 50M`:znajdź pliki o rozmiarze 50 MB

Tego polecenia można również używać ze znakami (+) i (-), aby określić plik większy lub mniejszy od podanego rozmiaru.

![](https://assets.tryhackme.com/additional/imgur/pSMfoz4.png)

Powyższy przykład zwraca pliki większe niż 100 MB. Należy pamiętać, że polecenie „find” często generuje błędy, co czasami utrudnia odczytanie danych wyjściowych. Dlatego warto użyć polecenia „find” z opcją „-type f 2>/dev/null”, aby przekierować błędy do „/dev/null” i uzyskać czystsze dane wyjściowe (poniżej).

![](https://assets.tryhackme.com/additional/imgur/UKYSdE3.png)

Foldery i pliki, do których można zapisywać lub z których można wykonywać dane:

- `find / -writable -type d 2>/dev/null`:Znajdź foldery, w których każdy może zapisywać
- `find / -perm -222 -type d 2>/dev/null`:Znajdź foldery, w których każdy może zapisywać
- `find / -perm -o w -type d 2>/dev/null`:Znajdź foldery, w których każdy może zapisywać

Powód, dla którego widzimy trzy różne polecenia „find”, które potencjalnie mogą prowadzić do tego samego rezultatu, można znaleźć w dokumentacji podręcznika. Jak widać poniżej, parametr perm wpływa na sposób działania polecenia „find”.

![](https://assets.tryhackme.com/additional/imgur/qb0klHH.png)  

- `find / -perm -o x -type d 2>/dev/null` :Znajdź foldery wykonywalne dla całego świata

Znajdź narzędzia programistyczne i obsługiwane języki:

- `find / -name perl*`
- `find / -name python*`
- `find / -name gcc*`

Znajdź określone uprawnienia do pliku:

Poniżej znajduje się krótki przykład wyszukiwania plików z ustawionym bitem SUID. Bit SUID pozwala plikowi uruchomić się z poziomem uprawnień konta, do którego jest on przypisany, a nie konta, które go uruchamia. Pozwala to na ciekawą ścieżkę eskalacji uprawnień, którą omówimy bardziej szczegółowo w zadaniu 6. Poniższy przykład służy do uzupełnienia tematu polecenia „find”.

- `find / -perm -u=s -type f 2>/dev/null`:Znajdź pliki z bitem SUID, który umożliwia uruchomienie pliku z wyższym poziomem uprawnień niż bieżący użytkownik.

### Ogólne polecenia Linuksa

Ponieważ jesteśmy w świecie Linuksa, znajomość poleceń Linuksa będzie bardzo przydatna. Prosimy o poświęcenie chwili na zapoznanie się z poleceniami takimi jak `find`, `locate`, `grep`, `cut`, `sort`, itd.

## Zautomatyzowane narzędzia do wyliczenia

Kilka narzędzi może pomóc Ci zaoszczędzić czas podczas procesu enumeracji. Należy z nich korzystać wyłącznie w celu zaoszczędzenia czasu, wiedząc, że mogą one pominąć pewne wektory eskalacji uprawnień. Poniżej znajduje się lista popularnych Linux narzędzia wyliczeniowe z linkami do odpowiednich repozytoriów Github.

Środowisko systemu docelowego będzie miało wpływ na narzędzie, z którego będziesz mógł korzystać. Na przykład, nie będziesz mógł uruchomić narzędzia napisanego w Pythonie, jeśli nie będzie ono zainstalowane w systemie docelowym. Dlatego lepiej jest znać kilka, niż korzystać z jednego, uniwersalnego narzędzia.

- **LinPeas** : [https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS(otwiera się w nowej karcie)](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS)
- **LinEnum:** [https://github.com/rebootuser/LinEnum(otwiera się w nowej karcie)](https://github.com/rebootuser/LinEnum)[(otwiera się w nowej karcie)](https://github.com/rebootuser/LinEnum)
- **LES (LinuxSugestia wykorzystania luk):** [https://github.com/mzet-/Linux-exploit-sugester(otwiera się w nowej karcie)](https://github.com/mzet-/linux-exploit-suggester)
- **LinuxInteligentne wyliczanie:** [https://github.com/diego-treitos/Linux-inteligentne wyliczanie(otwiera się w nowej karcie)](https://github.com/diego-treitos/linux-smart-enumeration)
- **LinuxSprawdzanie uprawnień:** [https://github.com/linted/linuxprivchecker](https://github.com/linted/linuxprivchecker)

Możemy porównać listę plików binarnych, które właśnie wygenerowano, z [GTFOBinami](https://gtfobins.github.io/#+capabilities) posortowanymi według możliwości, aby to ustalić.

![[Pasted image 20260317184618.png]]

**Uwaga: Aby wykonać czynność, uruchom maszynę docelową podłączoną do tego zadania.**
**Możesz uruchomić maszynę docelową i uzyskać do niej dostęp bezpośrednio z przeglądarki.**

**Alternatywnie, możesz uzyskać do niego dostęp przezSSHz poniższymi danymi uwierzytelniającymi użytkownika o niskich uprawnieniach:  

**Nazwa użytkownika: karen**

**Hasło: Hasło1**

Eskalacja uprawnień w idealnym przypadku prowadzi do uzyskania uprawnień roota. Czasami można to osiągnąć po prostu wykorzystując istniejącą lukę w zabezpieczeniach lub w niektórych przypadkach uzyskując dostęp do innego konta użytkownika, które ma więcej uprawnień, informacji lub dostępu.

Jeżeli pojedyncza luka nie prowadzi do użycia powłoki root, proces eskalacji uprawnień będzie opierał się na błędnych konfiguracjach i niewystarczających uprawnieniach.

Jądro włączoneLinux Systemy zarządzają komunikacją między komponentami, takimi jak pamięć systemowa i aplikacje. Ta krytyczna funkcja wymaga od jądra określonych uprawnień; zatem udane wykorzystanie luk w zabezpieczeniach może potencjalnie prowadzić do uzyskania uprawnień roota.

Metodologia wykorzystywania luk w jądrze jest prosta;

1. Zidentyfikuj wersję jądra
2. Wyszukaj i znajdź kod exploita dla wersji jądra systemu docelowego
3. Uruchom exploita

Choć wygląda to prosto, pamiętaj, że nieudana eksploitacja jądra może doprowadzić do awarii systemu. Przed podjęciem próby wykorzystania eksploitu jądra upewnij się, że taki potencjalny wynik jest akceptowalny w ramach zakresu Twoich testów penetracyjnych.

**Źródła badań:**  

1. Na podstawie uzyskanych informacji możesz użyć wyszukiwarki Google, aby wyszukać istniejący kod exploita.
2. Źródła takie jak [https://www.cvedetails.com/(otwiera się w nowej karcie)](https://www.cvedetails.com/)może być również przydatne.
3. Inną alternatywą byłoby użycie skryptu takiego jak LES (LinuxExploit Suggester), ale pamiętaj, że narzędzia te mogą generować fałszywe alarmy (zgłaszać luki w zabezpieczeniach jądra, które nie mają wpływu na system docelowy) lub fałszywe alarmy (nie zgłaszać żadnych luk w zabezpieczeniach jądra, mimo że jądro jest podatne).

**Wskazówki/uwagi:**

1. Zbytnie określanie wersji jądra podczas wyszukiwania exploitów w Google, Exploit-db lub searchsploit
2. Upewnij się, że rozumiesz, jak działa kod exploita, ZANIM go uruchomisz. Niektóre kody exploita mogą wprowadzać zmiany w systemie operacyjnym, które mogą spowodować utratę bezpieczeństwa podczas dalszego użytkowania lub nieodwracalne zmiany w systemie, powodując późniejsze problemy. Oczywiście, w laboratorium lub środowisku CTF nie stanowią one dużego problemu, ale są absolutnie niedopuszczalne podczas rzeczywistych testów penetracyjnych.
3. Niektóre exploity mogą wymagać dalszej interakcji po uruchomieniu. Przeczytaj wszystkie komentarze i instrukcje dołączone do kodu exploita.
4. Możesz przenieść kod exploita ze swojego komputera do systemu docelowego korzystając odpowiednio `SimpleHTTPServer` z modułu Pythona i `wget` .
## Eskalacja uprawnień Sudo
Polecenie sudo domyślnie pozwala na uruchomienie programu z uprawnieniami roota. W pewnych okolicznościach administratorzy systemu mogą potrzebować dać zwykłym użytkownikom pewną elastyczność w zakresie uprawnień. Na przykład, młodszy użytkownikSOCanalityk może potrzebować użyćNmapRegularnie, ale nie będzie można go wyczyścić, aby uzyskać pełny dostęp do konta root. W takiej sytuacji administrator systemu może zezwolić temu użytkownikowi na uruchamianie tylkoNmapz uprawnieniami roota, zachowując jednocześnie standardowy poziom uprawnieńodpoczyneksystemu.

Każdy użytkownik może sprawdzić swoją aktualną sytuację związaną z uprawnieniami roota, korzystając z `sudo -l`polecenia.

[https://gtfobins.github.io/(otwiera się w nowej karcie)](https://gtfobins.github.io/)jest cennym źródłem informacji o tym, jak można używać dowolnego programu, do którego posiadasz uprawnienia sudo.

**Wykorzystaj funkcje aplikacji**  

Niektóre aplikacje nie będą miały znanego exploita w tym kontekście. Taką aplikacją może być serwer Apache2.

W tym przypadku możemy użyć „hacka”, aby ujawnić informacje, wykorzystując funkcję aplikacji. Jak widać poniżej, Apache2 ma opcję, która obsługuje ładowanie alternatywnych plików konfiguracyjnych ( `-f`: określ alternatywny plik ServerConfigFile).

![](https://assets.tryhackme.com/additional/imgur/rNpbbL8.png)  

Załadowanie `/etc/shadow`pliku przy użyciu tej opcji spowoduje wyświetlenie komunikatu o błędzie zawierającego pierwszy wiersz pliku `/etc/shadow`.

**Wykorzystaj LD_PRELOAD**

W niektórych systemach może być widoczna opcja środowiskowa LD_PRELOAD.

![](https://assets.tryhackme.com/additional/imgur/gGstS69.png)  

LD_PRELOAD to funkcja, która pozwala każdemu programowi korzystać z bibliotek współdzielonych. Ten [wpis na blogu(otwiera się w nowej karcie)](https://rafalcieslak.wordpress.com/2013/04/02/dynamic-linker-tricks-using-ld_preload-to-cheat-inject-features-and-investigate-programs/)da Ci pojęcie o możliwościach LD_PRELOAD. Jeśli opcja „env_keep” jest włączona, możemy wygenerować bibliotekę współdzieloną, która zostanie załadowana i wykonana przed uruchomieniem programu. Pamiętaj, że opcja LD_PRELOAD zostanie zignorowana, jeśli rzeczywisty identyfikator użytkownika różni się od efektywnego.  

Kroki tego wektora eskalacji uprawnień można podsumować następująco:

1. Sprawdź LD_PRELOAD (z opcją env_keep)
2. Napisz prosty kod C skompilowany jako plik obiektu współdzielonego (rozszerzenie .so)
3. Uruchom program z uprawnieniami sudo i opcją LD_PRELOAD wskazującą na nasz plik .so

Kod C po prostu uruchomi powłokę główną i można go zapisać w następujący sposób:

#include <stdio.h>  
#include <sys/types.h>  
#include <stdlib.h>  
  
void _init() {  
unsetenv("LD_PRELOAD");  
setgid(0);  
setuid(0);  
system("/bin/bash");  
}  

Możemy zapisać ten kod jako shell.c i skompilować go za pomocą gcc do pliku obiektu współdzielonego, korzystając z następujących parametrów;

`gcc -fPIC -shared -o shell.so shell.c -nostartfiles`

![](https://assets.tryhackme.com/additional/imgur/HxbszMW.png)  

Możemy teraz używać tego pliku obiektu współdzielonego podczas uruchamiania dowolnego programu, który użytkownik może uruchomić za pomocą sudo. W naszym przypadku można użyć Apache2, find lub prawie każdego programu, który uruchamiamy za pomocą sudo.

Musimy uruchomić program, określając opcję LD_PRELOAD w następujący sposób;

`sudo LD_PRELOAD=/home/user/ldpreload/shell.so find`

Spowoduje to utworzenie powłoki z uprawnieniami roota.

![](https://assets.tryhackme.com/additional/imgur/1YwARyZ.png)
## Eskalacja uprawnień SUID

Dużo zLinuxKontrola uprawnień polega na kontrolowaniu interakcji użytkowników z plikami. Odbywa się to za pomocą uprawnień. Wiesz już, że pliki mogą mieć uprawnienia do odczytu, zapisu i wykonywania. Są one przyznawane użytkownikom w ramach ich poziomów uprawnień. Zmienia się to za pomocą SUID (Set-user Identification) i SGID (Set-group Identification). Umożliwiają one wykonywanie plików z poziomem uprawnień właściciela pliku lub grupy.  
  
Zauważysz, że te pliki mają ustawiony bit „s”, wskazujący ich specjalny poziom uprawnień.  
  
`find / -type f -perm -04000 -ls 2>/dev/null`Wyświetli listę plików z ustawionymi bitami SUID lub SGID.

![](https://assets.tryhackme.com/additional/imgur/fJEeZ4m.png)

Dobrą praktyką byłoby porównanie plików wykonywalnych na tej liście z GTFOBins ( [https://gtfobins.github.io(otwiera się w nowej karcie)](https://gtfobins.github.io/)Kliknięcie przycisku SUID spowoduje odfiltrowanie plików binarnych, które mogą być podatne na atak, gdy ustawiony jest bit SUID (listę wstępnie przefiltrowanych plików można znaleźć również pod tym linkiem:  [https://gtfobins.github.io/#+suid(otwiera się w nowej karcie)](https://gtfobins.github.io/#+suid)).

Powyższa lista pokazuje, że nano ma ustawiony bit SUID. Niestety, GTFObins nie daje nam łatwego rozwiązania. W typowych scenariuszach eskalacji uprawnień w życiu codziennym, będziemy musieli znaleźć kroki pośrednie, które pomogą nam wykorzystać wszelkie drobne odkrycia, jakie posiadamy.

![](https://assets.tryhackme.com/additional/imgur/rSRTn5v.png)  

**Uwaga** : dołączona maszyna wirtualna ma inny plik binarny z SUID innym niż `nano`.  

Bit SUID ustawiony dla edytora tekstu nano pozwala nam tworzyć, edytować i odczytywać pliki, korzystając z uprawnień właściciela pliku. Nano jest własnością roota, co prawdopodobnie oznacza, że ​​możemy odczytywać i edytować pliki na wyższym poziomie uprawnień niż ma nasz obecny użytkownik. Na tym etapie mamy dwie podstawowe opcje eskalacji uprawnień: odczyt pliku `/etc/shadow`lub dodanie naszego użytkownika do `/etc/passwd`.  
  
Poniżej przedstawiono proste kroki z wykorzystaniem obu wektorów.  
  
odczyt `/etc/shadow`pliku  
  
Widzimy, że edytor tekstu nano ma ustawiony bit SUID, uruchamiając polecenie `find / -type f -perm -04000 -ls 2>/dev/null`.  
  
`nano /etc/shadow`wydrukuje zawartość pliku `/etc/shadow`. Teraz możemy użyć narzędzia unshadow, aby utworzyć plik możliwy do złamania przez Johna the Rippera. Aby to osiągnąć, unshadow potrzebuje zarówno plików `/etc/shadow`i `/etc/passwd`.

![](https://assets.tryhackme.com/additional/imgur/DAWxbJD.png)  

Poniżej można zobaczyć zastosowanie narzędzia Unshadow;  
`unshadow passwd.txt shadow.txt > passwords.txt`  

![](https://assets.tryhackme.com/additional/imgur/6cHBAr1.png)  

Z poprawną listą słów i odrobiną szczęścia, John the Ripper może zwrócić jedno lub kilka haseł w postaci zwykłego tekstu. Więcej szczegółów na temat John the Ripper znajdziesz na stronie  [https://tryhackme.com/room/johntheripperbasics](https://tryhackme.com/room/johntheripperbasics) .

Inną opcją byłoby dodanie nowego użytkownika z uprawnieniami roota. Pomogłoby nam to ominąć żmudny proces łamania haseł. Poniżej znajduje się prosty sposób, aby to zrobić:

Będziemy potrzebować wartości skrótu hasła, które chcemy przekazać nowemu użytkownikowi. Można to szybko zrobić za pomocą narzędzia openssl w systemie Kali Linux.

![](https://assets.tryhackme.com/additional/imgur/bkOGaHY.png)  

Następnie dodamy to hasło i nazwę użytkownika do `/etc/passwd` pliku.

![](https://assets.tryhackme.com/additional/imgur/huGoEtj.png)

Gdy już dodamy naszego użytkownika (proszę zwrócić uwagę, w jaki sposób `root:/bin/bash`zapewniliśmy mu uprawnienia roota), będziemy musieli przełączyć się na tego użytkownika i mamy nadzieję, że uzyskamy uprawnienia roota.

![](https://assets.tryhackme.com/additional/imgur/HZcWGhi.png)  

Teraz nadeszła Twoja kolej, aby wykorzystać umiejętności, których właśnie się nauczyłeś, i znaleźć podatny na ataki kod binarny.

## Eskalacja uprawnień: możliwości

Inną metodą, z której administratorzy systemów mogą skorzystać, aby zwiększyć poziom uprawnień procesu lub pliku binarnego, są „Możliwości”. Możliwości pomagają zarządzać uprawnieniami na bardziej szczegółowym poziomie. Na przykład, jeśliSOCAnalityk musi użyć narzędzia, które inicjuje połączenia z gniazdem, a zwykły użytkownik nie byłby w stanie tego zrobić. Jeśli administrator systemu nie chce nadać temu użytkownikowi wyższych uprawnień, może zmienić uprawnienia pliku binarnego. W rezultacie plik binarny wykona swoje zadanie bez konieczności korzystania z uprawnień użytkownika o wyższych uprawnieniach.  
Strona podręcznika „ability” zawiera szczegółowe informacje na temat jego użycia i opcji.  
  
Możemy użyć tego `getcap` narzędzia, aby wyświetlić listę włączonych uprawnień.

![](https://assets.tryhackme.com/additional/imgur/Q6XYr0p.png)

Uruchomienie jako użytkownik bez uprawnień `getcap -r /`generuje ogromną liczbę błędów, dlatego dobrą praktyką jest przekierowywanie komunikatów o błędach do /dev/null.  
  
Należy pamiętać, że ani vim, ani jego kopia nie mają ustawionego bitu SUID. Ten wektor eskalacji uprawnień nie jest zatem wykrywalny podczas enumeracji plików w poszukiwaniu SUID.

![](https://assets.tryhackme.com/additional/imgur/6csoabB.png)

GTFObins oferuje dobrą listę plików binarnych, które można wykorzystać do eskalacji uprawnień, jeśli znajdziemy jakieś ustalone uprawnienia.  
  
Zauważamy, że vim można używać z następującym poleceniem i ładunkiem:  
  
![](https://assets.tryhackme.com/additional/imgur/nlpCMWj.png)  

Spowoduje to uruchomienie powłoki roota, jak pokazano poniżej;

![](https://assets.tryhackme.com/additional/imgur/jCjvgo3.png)

## Eskalacja usprawnień: cron

Zadania cron służą do uruchamiania skryptów lub plików binarnych w określonych momentach. Domyślnie są one uruchamiane z uprawnieniami ich właścicieli, a nie bieżącego użytkownika. Chociaż poprawnie skonfigurowane zadania cron nie są z natury podatne na ataki, mogą one w pewnych warunkach stanowić wektor eskalacji uprawnień.  
Idea jest dość prosta: jeśli istnieje zaplanowane zadanie uruchamiane z uprawnieniami roota i możemy zmienić skrypt, który zostanie uruchomiony, to nasz skrypt zostanie uruchomiony z uprawnieniami roota.  
  
Konfiguracje zadań cron są przechowywane jako crontab (tabele cron), aby zobaczyć następny czas i datę uruchomienia zadania.  
  
Każdy użytkownik w systemie ma swój plik crontab i może uruchamiać określone zadania niezależnie od tego, czy jest zalogowany, czy nie. Jak można się spodziewać, naszym celem będzie znalezienie zadania cron ustawionego przez roota i uruchomienie przez nie naszego skryptu, najlepiej powłoki.  
  
Każdy użytkownik może odczytać plik przechowujący systemowe zadania cron. `/etc/crontab`  
  
Podczas gdy maszyny CTF mogą mieć zadania cron uruchamiane co minutę lub co 5 minut, częściej można zobaczyć zadania uruchamiane codziennie, co tydzień lub co miesiąc w testach penetracyjnych.  
![](https://assets.tryhackme.com/additional/imgur/fwqPuHN.png)  

Jak widać, `backup.sh`skrypt został skonfigurowany do uruchamiania co minutę. Zawartość pliku pokazuje prosty skrypt, który tworzy kopię zapasową pliku prices.xls.

![](https://assets.tryhackme.com/additional/imgur/qlDj93R.png)

Ponieważ nasz obecny użytkownik ma dostęp do tego skryptu, możemy go łatwo zmodyfikować, aby utworzyć powłokę odwrotną, miejmy nadzieję, z uprawnieniami roota.  
  
Skrypt użyje narzędzi dostępnych w systemie docelowym do uruchomienia powłoki odwrotnej.  
Dwie uwagi:

1. Składnia polecenia będzie się różnić w zależności od dostępnych narzędzi. (np. `nc`prawdopodobnie nie będzie obsługiwała `-e`opcji, którą mogłeś widzieć w innych przypadkach)
2. Zawsze powinniśmy preferować uruchamianie powłok odwrotnych, ponieważ nie chcemy narażać integralności systemu podczas rzeczywistych testów penetracyjnych.

Plik powinien wyglądać tak:  

![](https://assets.tryhackme.com/additional/imgur/579yg6H.png)  

Teraz uruchomimy program nasłuchujący na naszej maszynie atakującej, aby odebrać połączenie przychodzące.

![](https://assets.tryhackme.com/additional/imgur/xwYXfY1.png)

Zawsze warto sprawdzić Crontab, ponieważ może on czasami prowadzić do eskalacji uprawnień. Poniższy scenariusz nie jest rzadkością w firmach, które nie mają określonego poziomu dojrzałości cyberbezpieczeństwa:

1. Administratorzy systemu muszą uruchamiać skrypt w regularnych odstępach czasu.
2. Tworzą zadanie cron, aby to zrobić
3. Po pewnym czasie skrypt staje się bezużyteczny i zostaje usunięty  
    
4. Nie czyszczą odpowiedniego zadania cron

Ten problem z zarządzaniem zmianami może potencjalnie prowadzić do wykorzystania zadań cron.

![](https://assets.tryhackme.com/additional/imgur/SovymJL.png)

Powyższy przykład pokazuje podobną sytuację, w której skrypt antivirus.sh został usunięty, ale zadanie cron nadal istnieje.  
Jeśli pełna ścieżka skryptu nie jest zdefiniowana (jak w przypadku skryptu backup.sh), cron będzie odwoływał się do ścieżek wymienionych w zmiennej PATH w pliku /etc/crontab. W takim przypadku powinniśmy móc utworzyć skrypt o nazwie „antivirus.sh” w folderze domowym użytkownika i uruchomić go za pomocą zadania cron.  

Plik w systemie docelowym powinien wyglądać znajomo:  

![](https://assets.tryhackme.com/additional/imgur/SHknR87.png)  

Przychodzące połączenie powłoki odwrotnej ma uprawnienia roota:

![](https://assets.tryhackme.com/additional/imgur/EBCue17.png)  

W przypadku znalezienia istniejącego skryptu lub zadania powiązanego z zadaniem cron, zawsze warto poświęcić czas na zrozumienie funkcji skryptu i sposobu użycia danego narzędzia w danym kontekście. Na przykład, tar, 7z, rsync itp. mogą zostać wykorzystane do ataku z wykorzystaniem funkcji symboli wieloznacznych.

## Eskalacja uprawnień: path

Jeśli w ścieżce znajduje się folder, do którego użytkownik ma uprawnienia zapisu, istnieje ryzyko przejęcia aplikacji w celu uruchomienia skryptu. ŚCIEŻKA wLinuxto zmienna środowiskowa, która wskazuje systemowi operacyjnemu, gdzie szukać plików wykonywalnych. Dla każdego polecenia, które nie jest wbudowane w powłokę lub nie jest zdefiniowane ze ścieżką bezwzględną,Linuxrozpocznie przeszukiwanie folderów zdefiniowanych w zmiennej PATH. (PATH to zmienna środowiskowa, o której tu mówimy, a ścieżka to lokalizacja pliku).  
  
Zazwyczaj ścieżka PATH wygląda tak:

![](https://assets.tryhackme.com/additional/imgur/ch2Z4zp.png)  

Jeśli wpiszemy „thm„do wiersza poleceń, oto lokalizacjeLinuxposzuka pliku wykonywalnego o nazwiethmPoniższy scenariusz da Ci lepsze wyobrażenie o tym, jak można to wykorzystać do zwiększenia poziomu uprawnień. Jak zobaczysz, zależy to całkowicie od istniejącej konfiguracji systemu docelowego, więc upewnij się, że potrafisz odpowiedzieć na poniższe pytania, zanim spróbujesz.

1. Jakie foldery znajdują się w $PATH
2. Czy Twój obecny użytkownik ma uprawnienia do zapisu w którymś z tych folderów?
3. Czy możesz zmodyfikować $PATH?
4. Czy istnieje skrypt/aplikacja, którą możesz uruchomić i która będzie narażona na tę lukę?

W celach demonstracyjnych użyjemy poniższego skryptu:  

![](https://assets.tryhackme.com/additional/imgur/qX7m2Jq.png)  

Ten skrypt próbuje uruchomić plik binarny systemu o nazwie „thm„ale przykład ten można łatwo powtórzyć przy użyciu dowolnego pliku binarnego.

Kompilujemy to do pliku wykonywalnego i ustawiamy bit SUID.

![](https://assets.tryhackme.com/additional/imgur/A6QQ65I.png)  

Nasz użytkownik ma teraz dostęp do skryptu „path” z ustawionym bitem SUID.

![](https://assets.tryhackme.com/additional/imgur/Af1RpuY.png)  

Po wykonaniu „ścieżka” będzie szukać pliku wykonywalnego o nazwie „thm” wewnątrz folderów wymienionych w ścieżce PATH.

Jeżeli w zmiennej PATH znajduje się jakikolwiek zapisywalny folder, możemy utworzyć plik binarny o nazwiethmw tym katalogu i niech nasz skrypt „ścieżka” go uruchomi. Ponieważ bit SUID jest ustawiony, ten plik binarny będzie działał z uprawnieniami roota.

Proste wyszukiwanie folderów z możliwością zapisu można przeprowadzić za pomocą `find / -writable 2>/dev/null`polecenia „ ”. Dane wyjściowe tego polecenia można oczyścić, wykonując prostą sekwencję cięcia i sortowania.

![](https://assets.tryhackme.com/additional/imgur/7UekB3t.png)  

Niektóre scenariusze CTF mogą prezentować różne foldery, ale standardowy system wyświetliłby coś takiego, jak widać powyżej.

Porównanie tego ze zmienną PATH pomoże nam znaleźć foldery, z których możemy skorzystać.

![](https://assets.tryhackme.com/additional/imgur/67mdmmG.png)  

Widzimy, że w katalogu /usr znajduje się wiele folderów, więc łatwiej będzie ponownie uruchomić wyszukiwanie w folderach zapisywalnych, aby objąć podfoldery.

![](https://assets.tryhackme.com/additional/imgur/Y3pDsrL.png)  

Alternatywą może być poniższe polecenie.

`find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u`

Dodaliśmy „grep -v proc”, aby pozbyć się wielu wyników związanych z uruchomionymi procesami.

Niestety, podfoldery w /usr nie są zapisywalne

Folder, do którego będzie łatwiej zapisywać, to prawdopodobnie /tmp. W tym momencie, ponieważ /tmp nie znajduje się w zmiennej PATH, musimy go dodać. Jak widać poniżej, `export PATH=/tmp:$PATH`polecenie „ ” pozwala to osiągnąć.

![](https://assets.tryhackme.com/additional/imgur/u1PM8ZD.png)  

W tym momencie skrypt ścieżki będzie również szukał w folderze /tmp pliku wykonywalnego o nazwie „thm”.

Utworzenie tego polecenia jest dość proste poprzez skopiowanie /bin/bash jako „thm” w folderze /tmp.

![](https://assets.tryhackme.com/additional/imgur/7UdrEnd.png)  

Nadaliśmy prawa wykonywalne naszej kopii /bin/bash. Proszę pamiętać, że na tym etapie będzie ona uruchamiana z uprawnieniami naszego użytkownika. W tym kontekście eskalacja uprawnień jest możliwa, ponieważ skrypt ścieżki działa z uprawnieniami użytkownika root.

![](https://assets.tryhackme.com/additional/imgur/MlBJ8kb.png)

## Eskalacja uprawnień: NFS

Wektory eskalacji uprawnień nie ograniczają się do dostępu wewnętrznego. Foldery współdzielone i interfejsy zdalnego zarządzania, takie jakSSHTelnet może również pomóc Ci uzyskać dostęp do roota w systemie docelowym. W niektórych przypadkach konieczne będzie również użycie obu wektorów, np. znalezienie roota.SSHklucza prywatnego w systemie docelowym i połączenia za pośrednictwemSSHz uprawnieniami roota, zamiast próbować zwiększyć poziom uprawnień bieżącego użytkownika.  
  
Innym wektorem, który jest bardziej istotny w przypadku testów CTF i egzaminów, jest nieprawidłowo skonfigurowana powłoka sieciowa. Ten wektor można czasami zaobserwować podczas testów penetracyjnych, gdy obecny jest system kopii zapasowej sieci.  
  
Konfiguracja NFS (Network File Sharing – udostępnianie plików sieciowych) jest przechowywana w pliku /etc/exports. Plik ten jest tworzony podczas instalacji serwera NFS i zazwyczaj może być odczytany przez użytkowników.

![](https://assets.tryhackme.com/additional/imgur/irDQTze.png)  

Kluczowym elementem tego wektora eskalacji uprawnień jest opcja „no_root_squash”, którą widać powyżej. Domyślnie NFS zmienia użytkownika root na nfsnobody i uniemożliwia działanie plików z uprawnieniami roota. Jeśli opcja „no_root_squash” jest obecna w udziale zapisywalnym, możemy utworzyć plik wykonywalny z ustawionym bitem SUID i uruchomić go w systemie docelowym.  
  
Zaczniemy od enumeracji udziałów montowalnych na naszej maszynie atakującej.

![](https://assets.tryhackme.com/additional/imgur/CmXPDcv.png)  

Zamontujemy jeden z udziałów „no_root_squash” na komputerze atakującym i rozpoczniemy budowę pliku wykonywalnego.

![](https://assets.tryhackme.com/additional/imgur/DwAB1qs.png)  

Ponieważ możemy ustawić bity SUID, prosty plik wykonywalny, który uruchomi /bin/bash na systemie docelowym, wykona zadanie.

![](https://assets.tryhackme.com/additional/imgur/nWKpFkK.png)  

Po skompilowaniu kodu ustawimy bit SUID.

![](https://assets.tryhackme.com/additional/imgur/rkZOOjZ.png)  

Poniżej widać, że oba pliki (nfs.c i nfs) są obecne w systemie docelowym. Pracowaliśmy na zamontowanym udziale, więc nie było potrzeby ich przenoszenia.

![](https://assets.tryhackme.com/additional/imgur/U7IjT38.png)  

Należy pamiętać, że plik wykonywalny nfs ma ustawiony bit SUID na systemie docelowym i działa z uprawnieniami roota.
