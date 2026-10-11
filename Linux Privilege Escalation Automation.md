---

Powinieneś już rozumieć podstawowe techniki eskalacji uprawnień oraz wiedzieć, jak je wyliczać i wykorzystywać. W tej sali posuniemy się o krok dalej i poszerzymy Twój arsenał o narzędzia, które zautomatyzują ten proces lub pomogą Ci znaleźć ukryte wektory eskalacji uprawnień.

![Automatyzacja](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1773132164927.png)

## Cele edukacyjne

- Zaprezentuj wyliczanie eskalacji uprawnień za pomocą zautomatyzowanych narzędzi
- Zaprezentuj techniki eskalacji uprawnień, wykorzystując publiczne luki w zabezpieczeniach
- ZrozumiećLinuxpodglądanie procesów

## Wymagania wstępne

- [LinuxEskalacja uprawnień: wyliczenie](https://tryhackme.com/room/linprivenum)
- [LinuxEskalacja uprawnień: podstawy](https://tryhackme.com/room/linprivbasics)

Kilka narzędzi może pomóc Ci zaoszczędzić czas podczas procesu enumeracji. Należy z nich korzystać wyłącznie w celu zaoszczędzenia czasu, pamiętając, że mogą one pominąć pewne wektory eskalacji uprawnień. Poniżej znajduje się lista popularnych Linux narzędzia wyliczeniowe z linkami do odpowiednich repozytoriów GitHub.

Środowisko systemu docelowego będzie miało wpływ na narzędzie, z którego będziesz mógł korzystać. Na przykład, nie będziesz mógł uruchomić narzędzia napisanego w Pythonie, jeśli nie będzie ono zainstalowane w systemie docelowym. Dlatego lepiej jest znać kilka, niż korzystać z jednego, uniwersalnego narzędzia.

- [**LinPeas**(otwiera się w nowej karcie)](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS):Zautomatyzowany skrypt, który podświetla ścieżki eskalacji uprawnień w systemie — błędne konfiguracje, słabe uprawnienia, poświadczenia i inne
- **[LinEnum(otwiera się w nowej karcie)](https://github.com/rebootuser/LinEnum)**: Skryptowe narzędzie do lokalnego wyliczania, które zrzuca informacje o systemie, użytkownikach, cronach i plikach binarnych SUID w czytelnym raporcie
- **[LES (LinuxSugerowanie wykorzystania luk)(otwiera się w nowej karcie)](https://github.com/mzet-/linux-exploit-suggester)**:Porównuje wersję jądra ze znanymi lukami CVE i sugeruje możliwe lokalne luki w zabezpieczeniach umożliwiające eskalację uprawnień
- **[LinuxInteligentne wyliczanie(otwiera się w nowej karcie)](https://github.com/diego-treitos/linux-smart-enumeration)**:Skrypt wyliczeń z regulowanymi poziomami szczegółowości — zaczyna cicho i ujawnia więcej szczegółów wraz ze wzrostem poziomu
- **[LinuxSprawdzanie prywatności(otwiera się w nowej karcie)](https://github.com/linted/linuxprivchecker)**:Wylicza informacje o systemie i automatycznie sprawdza możliwości eskalacji uprawnień, sygnalizując problemy w trybie online

![](https://cdn-images.tryhackme.com/room-icons/68d2c1e7ab94268f6271de1d-1771765213861)

**Uwaga:** Możesz znaleźćLinuxExploit Suggester w katalogu domowym Johna **.**

## Wykorzystywanie publiczne

Wiele technik eskalacji uprawnień opiera się na błędnych konfiguracjach: zbyt liberalnej regule sudo, zadaniu cron wywołującym skrypt z możliwością zapisu przez wszystkich użytkowników lub możliwości przypisanej do pliku binarnego, która nie powinna jej mieć. W takich przypadkach oprogramowanie działa dokładnie tak, jak powinno; ktoś po prostu je źle skonfigurował.

Publiczne exploity są inne. W tym przypadku samo oprogramowanie jest uszkodzone. Błąd w kodzie (przepełnienie bufora, wyścig, błąd logiczny) pozwala na zrobienie czegoś, czego programiści nigdy nie zamierzali. Po wykryciu tych błędów, przypisuje się imCVE(Common Vulnerabilities and Exposures) identyfikator, a często także działający kod exploita jest publikowany publicznie.

## Metodologia

Korzystanie z publicznego exploita nie polega tylko na pobraniu kodu i jego uruchomieniu. To proces, a pomijanie kroków to sposób na zawieszenie komputerów lub zmarnowanie godzin na exploity, które i tak nigdy nie zadziałają. Ogólny schemat działania wygląda następująco:

- **Wyliczenie:** Zidentyfikuj zainstalowane oprogramowanie i uruchomione wersje. Wiesz już, jak to zrobić z laboratorium wyliczeń. Kluczowe kwestie do zapamiętania: wersja jądra, wersja dystrybucji oraz wszelkie pliki binarne SUID lub usługi uruchomione jako root.
- **Badania:** Weź to, co znalazłeś i poszukaj znanych luk. Czy istniejeCVECzy istnieje publiczny exploit dla tej wersji? Czy pasuje on do architektury i dystrybucji twojego celu?
- **Oceń:** Nie każdy znaleziony exploit zadziała. Przeczytaj kod. Zrozum, co robi. Sprawdź wymagania: czy jest wymagany `gcc`na celu? Czy działa tylko na określonych wersjach jądra? Czy spowoduje awarię systemu?
- **Exploit:** Przenieś exploit na cel, skompiluj go, jeśli to konieczne, i uruchom.
- **Sprawdź:** Upewnij się, że masz podwyższone uprawnienia. Zaznacz `whoami`, `id`, i spróbuj uzyskać dostęp do czegoś, do czego wcześniej nie mogłeś.

## Gdzie znaleźć publiczne exploity

Istnieje kilka źródeł, z których możesz skorzystać, aby znaleźć kod exploita. Powinieneś czuć się swobodnie korzystając ze wszystkich.

**searchsploit (Exploit-DB offline)**

`searchsploit`to narzędzie wiersza poleceń, które przeszukuje lokalną kopię bazy danych Exploit-DB. Jest ono preinstalowane w systemie Kali.

Stosowanie:

`searchsploit <software> <version>`

**GitHub**

GitHub ma wiele repozytoriów zawierających publiczne exploity dla znanych luk CVE. Jeśli kiedykolwiek znajdziesz lukę CVE dla konkretnej wersji oprogramowania, możesz wyszukać repozytorium GitHub w Google.

`CVE-<id> github`

**Narzędzia wyliczeniowe**

Narzędzia takie jak Linpeas nie tylko identyfikują błędne konfiguracje, ale także sprawdzają znane luki bezpieczeństwa (CVE). Jeśli Linpeas zgłosi podatną wersję oprogramowania, często będzie ona zawierać…CVEliczba, która daje Ci bezpośredni punkt wyjścia do Twoich badań.

## Exploity jądra

Jądro to najbardziej uprzywilejowany element oprogramowania w systemie Linux. Luka w jądrze może umożliwić przejście z użytkownika bez uprawnień na roota, niezależnie od tego, jak dobrze skonfigurowane są wszystkie inne elementy.

Przypomnienie, jak wyliczyć wersję jądra na obiekcie docelowym:

`uname -r`

`uname -a`

`cat /etc/os-release`

Następnie wyszukaj znane exploity dla tej wersji korzystając z wyszukiwarki Searchsploit lub Google.

## Publiczne exploity poza jądrem

Nie wszystkie publiczne exploity atakują jądro. Wiele luk CVE związanych z eskalacją uprawnień występuje w oprogramowaniu użytkownika — programach i narzędziach, które działają z podwyższonymi uprawnieniami. Często są one łatwiejsze do wykorzystania i mniej prawdopodobne, że spowodują awarię systemu.

Następnie będziesz musiał użyć publicznego exploita, aby uzyskać uprawnienia roota na komputerze laboratoryjnym. Wcześniej zidentyfikowałeś, że cel jest podatny na lukę CVE. Teraz musisz to wykorzystać, aby uzyskać uprawnienia roota. Exploit znajdziesz na GitHubie, pobierzesz go na AttackBoxa, a następnie prześlesz na komputer docelowy za pomocą  `scp`.

`scp <file> john@MACHINE_IP:/home/john/`

## Kwestia sondaży

Chociaż zautomatyzowane narzędzia wspomniane w poprzednim zadaniu doskonale sprawdzają się w wyliczaniu statycznych błędów konfiguracji, przechwytują one jedynie migawkę systemu w momencie uruchomienia. Nie potrafią wskazać procesów działających w tle, zwłaszcza tych krótkotrwałych, takich jak zadania cron czy zaplanowane skrypty, które uruchamiają się i kończą w ciągu milisekund. Właśnie tutaj [pspy(otwiera się w nowej karcie)](https://github.com/dominicbreuker/pspy)wypełnia lukę.

pspy to narzędzie do monitorowania procesów, które umożliwia nieuprawnionym użytkownikom obserwowanie uruchomionych procesów, zadań cron i poleceń wykonywanych przez innych użytkowników w czasie rzeczywistym, bez konieczności posiadania uprawnień roota.

## Podejście oparte na zdarzeniach

NALinuxProcesy są izolowane — użytkownicy o niskich uprawnieniach widzą tylko swoje własne procesy za pośrednictwem [ `/proc`brakuje kontekstu]. Krótkotrwałe zadania (takie jak zadania cron) mogą zostać przerwane, zanim ktokolwiek zdąży je zaobserwować, co sprawia, że ​​tradycyjne narzędzia do sondowania są mało wiarygodne w kontekście wykrywania.

**Pspy** wykorzystuje podejście sterowane zdarzeniami zamiast sondowania. Ustawia obserwację inotify w często używanych katalogach (np. `/etc`, `/tmp`, `/usr`, `/var`). Po wykryciu aktywności w systemie plików, pspy skanuje `/proc`w celu zidentyfikowania nowego procesu, przechwytując jego **UID** , **PID** , **znacznik czasu** i **pełne polecenie** — nawet w przypadku procesów uruchamianych przez innych użytkowników.

Dzieje się tak, ponieważ metadane procesu `/proc`są przez krótki czas dostępne w trakcie jego istnienia, nawet dla użytkowników bez uprawnień. pspy nie omija żadnych uprawnień jądra — reaguje na tyle szybko, aby wychwycić to, czego nie zauważą narzędzia sondujące.

## Korzystanie z pspy

**pspy** można znaleźć w `/home/john/`.

Uruchom pspy z katalogu domowego Johna w następujący sposób **:**

`./pspy64`

Po krótkiej chwili powinieneś zobaczyć proces roota, podobny do przykładu poniżej.

Terminal

```markdown

2026/02/10 06:40:11 CMD: UID=0     PID=12     |
2026/02/10 06:40:11 CMD: UID=0     PID=11     |
2026/02/10 06:40:11 CMD: UID=0     PID=10     |
2026/02/10 06:40:11 CMD: UID=0     PID=9      |
2026/02/10 06:40:11 CMD: UID=0     PID=8      |
2026/02/10 06:40:11 CMD: UID=0     PID=7      |
2026/02/10 06:40:11 CMD: UID=0     PID=6      |
2026/02/10 06:40:11 CMD: UID=0     PID=5      |
2026/02/10 06:40:11 CMD: UID=0     PID=4      |
2026/02/10 06:40:11 CMD: UID=0     PID=3      |
2026/02/10 06:40:11 CMD: UID=0     PID=2      |
2026/02/10 06:40:11 CMD: UID=0     PID=1      | /sbin/init
2026/02/10 06:40:16 CMD: UID=0     PID=1937   | /bin/bash /root/run-backup.sh
2026/02/10 06:40:16 CMD: UID=0     PID=1938   | tar -czf /var/backup/syslog.tar.gz /var/log/syslog
2026/02/10 06:40:16 CMD: UID=0     PID=1939   | /bin/sh -c gzip
2026/02/10 06:40:16 CMD: UID=0     PID=1940   | gzip
2026/02/10 06:40:16 CMD: UID=0     PID=1941   | sleep 10
2026/02/10 06:40:16 CMD: UID=0     PID=1942   | /bin/bash /root/run-rm-tmp.sh
2026/02/10 06:40:16 CMD: UID=0     PID=1943   | /bin/bash /usr/local/bin/rm-tmp.sh
2026/02/10 06:40:16 CMD: UID=0     PID=1944   | /bin/bash /usr/local/bin/rm-tmp.sh
2026/02/10 06:40:16 CMD: UID=0     PID=1945   |
2026/02/10 06:40:16 CMD: UID=0     PID=1946   | chpasswd
2026/02/10 06:40:16 CMD: UID=0     PID=1948   | /bin/bash /root/run-rm-tmp.sh
```

Jak widać, korzeń (Identyfikator użytkownika=0) uruchamia skrypt w `/root`folderze (do którego nie mają dostępu użytkownicy niskiego poziomu) i inny w `/usr/local/bin`.

Sprawdzenie uprawnień i zawartości pliku ujawnia następujące informacje:

Terminal

```markdown
john@privesc:~$ ls -la /usr/local/bin/rm-tmp.sh
-rwxrwxrwx 1 root root 57 Jan 20 10:27 /usr/local/bin/rm-tmp.sh
john@privesc:~$ cat /usr/local/bin/rm-tmp.sh
#!/bin/bash
rm -r /tmp/*
```

Wygląda na to, że ten skrypt ma na celu wyczyszczenie `/tmp`folderu. Ponieważ jednak skrypt jest dostępny dla wszystkich użytkowników i działa w pętli jako root, możesz dodać własne polecenie, aby zwiększyć uprawnienia. W poniższym przykładzie dodano polecenie zmieniające hasło roota.

Terminal

```markdown
#!/bin/bashrm -r /tmp/*echo "root:newpass" | chpasswd
```

Na koniec możesz zalogować się jako użytkownik root, po prostu wywołując polecenie `su`i podając nowe hasło.

Terminal

```markdown
john@privesc:~$ suPassword:root@privesc:/home/john#
```

Następnie będziesz musiał skorzystać  `pspy`z , aby ułatwić sobie wykorzystanie podobnego scenariusza i uzyskać uprawnienia roota.

W tym pokoju przyspieszyłeś eskalację uprawnień, dodając automatyzację do swojego przepływu pracy.

- Wykorzystałeś zautomatyzowane narzędzia do wykrywania i znajdowania luk w zabezpieczeniach, aby szybko wykryć błędne konfiguracje i podatne oprogramowanie, ucząc się, że nie ma jednego narzędzia, które wychwyci wszystko.
- Następnie pracowałeś nad publicznymi exploitami, postępując zgodnie z jasną metodologią 
- Na koniec, dzięki pspy udało Ci się zakryć martwy punkt, którego nie dostrzegają skanery: krótkotrwałe procesy. 

Wniosek: automatyzacja mnoży siłę, a nie zastępuje zrozumienia. Narzędzia pokazują, gdzie szukać, ale nadal musisz wiedzieć, na co patrzysz.
