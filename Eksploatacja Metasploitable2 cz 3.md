
## **3. Co proponuję jako następne ćwiczenie?**

Przejdźmy do **enumeracji NFS (Network File System)** na tym samym Metasploitable 2.

To logiczna kontynuacja, ponieważ NFS również umożliwia udostępnianie katalogów przez sieć. Sprawdzimy:

- jakie katalogi są eksportowane,  
    
- czy dostęp jest ograniczony do określonych hostów,  
    
- czy możliwe jest anonimowe przeglądanie zasobów,  
    
- jakie ryzyko wynika z konfiguracji.  
    

Zachowamy naszą metodę: jedno polecenie, analiza wyniku, następny krok.

Bardzo ciekawy wynik. Właśnie wykryliśmy potencjalnie poważny problem z konfiguracją NFS.

## **1. Analiza wyniku**

Otrzymaliśmy:

```
Export list for 192.168.56.104:
/ *
```

Interpretacja:

|Element|Znaczenie|
|---|---|
|`/`|Eksportowany katalog główny systemu plików|
|`*`|Dostęp do eksportu nie jest ograniczony do konkretnego adresu IP klienta|

Wysokie ryzyko konfiguracyjne

Serwer udostępnia katalog główny `/` przez NFS wszystkim klientom, których adresy pasują do reguły `*`.

To bardzo szerokie uprawnienie. Nie oznacza jednak automatycznie, że każdy klient może zapisywać pliki lub uzyskać uprawnienia root.

## **2. Następny krok – sprawdzamy szczegóły eksportu**

Teraz chcemy ustalić, jakie opcje eksportu zastosowano, szczególnie:

- `ro` – tylko odczyt,
    
- `rw` – odczyt i zapis,
    
- `root_squash` – mapowanie uprawnień użytkownika root klienta na konto anonimowe,
    
- `no_root_squash` – brak takiego ograniczenia.
    

W Kali wykonaj:

```
nmap -p 111,2049 --script nfs-showmount,nfs-statfs 192.168.56.104
```

Polecenie:

- sprawdzi usługę RPC na porcie 111,
    
- sprawdzi NFS na porcie 2049,
    
- spróbuje uzyskać informacje o eksportach i statystykach systemu plików.
    

Wklej cały wynik.

**Ważne:** na tym etapie tylko rozpoznajemy konfigurację. Nie montujemy jeszcze katalogu głównego i nie próbujemy niczego modyfikować. Najpierw ustalimy zakres dostępnych informacji.


Dobrze. Wynik potwierdza wcześniejsze ustalenie i dostarcza dodatkowych informacji o systemie plików.

## **1. Analiza wyniku NFS**

|Element|Wynik|Znaczenie|
|---|---|---|
|111/tcp|open rpcbind|Usługa RPC odpowiada|
|2049/tcp|open nfs|Serwer NFS jest dostępny|
|Eksport|`/`|Udostępniony katalog główny|
|Reguła klienta|`*`|Dowolny adres klienta pasujący do reguły|
|Rozmiar|ok. 7,3 GB|Wielkość systemu plików|
|Zajęte|ok. 1,5 GB|Wykorzystana przestrzeń|
|Wolne|ok. 5,4 GB|Dostępna przestrzeń|

**Najważniejszy wniosek:** NFS udostępnia cały katalog główny systemu, a nie tylko wybrany katalog użytkownika.

Musimy jednak pamiętać, że `nfs-showmount` nie ujawnia opcji `rw`, `ro`, `root_squash` ani `no_root_squash`. Nie możemy jeszcze stwierdzić, jakie faktyczne uprawnienia otrzyma klient.

## **2. Następny krok – sprawdzamy konfigurację eksportu**

Wykonaj w Kali:

```
nmap -p 2049 --script nfs-ls 192.168.56.104
```

Ten skrypt próbuje wyświetlić zawartość eksportowanych katalogów NFS.

Chcemy ustalić:

- czy możemy przeglądać katalog główny,
    
- jakie katalogi systemowe są widoczne,
    
- czy serwer ogranicza dostęp do określonych zasobów.
    

Na razie nie wykonujemy montowania NFS ani żadnych operacji zapisu.

## **3. Co już mamy w dokumentacji?**

Wstępne ustalenie:

> Serwer Metasploitable 2 udostępnia przez NFS katalog główny `/` z regułą dostępu `*`. Usługa jest osiągalna z sieci laboratoryjnej. Zakres faktycznych uprawnień klienta wymaga dalszej weryfikacji.

Wklej wynik kolejnego polecenia. Będziemy kontynuować tak samo jak przy Sambie — najpierw rozpoznanie, potem ocena ryzyka.

W porządku. Tym razem `nfs-ls` nie zwrócił listy katalogów. Widzimy tylko otwarty port 2049.

To nie oznacza, że NFS nie działa — poprzednie wyniki potwierdziły eksport `/`. Możliwe, że skrypt Nmap nie uzyskał wymaganych informacji o eksporcie lub nie obsłużył poprawnie tej konfiguracji.

Nie będziemy zgadywać. Sprawdzimy to innym narzędziem.

## **Następny krok – ręczne sprawdzenie eksportów NFS**

W Kali wykonaj:

```
rpcinfo -p 192.168.56.104
```

To polecenie odpyta usługę RPC i pokaże zarejestrowane programy, ich wersje oraz porty.

Interesują nas przede wszystkim:

- `nfs` – serwer NFS,
    
- `mountd` – obsługa montowania eksportów,
    
- `nlockmgr` – zarządzanie blokadami plików,
    
- `status` – monitorowanie stanu RPC.
    

Wklej cały wynik. Na jego podstawie ustalimy, jak bezpiecznie przejść do sprawdzenia dostępu do eksportowanego katalogu `/`.


Świetnie. Teraz mamy pełniejszy obraz infrastruktury RPC/NFS. Potwierdziliśmy, że usługa NFS jest aktywna i obsługuje kilka wersji protokołu.

## **1. Analiza wyniku** `rpcinfo`

Najważniejsze pozycje:

|Program|Wersje|Port TCP|Znaczenie|
|---|---|---|---|
|portmapper|2|111|Rejestr usług RPC|
|nfs|2, 3, 4|2049|Udostępnianie systemu plików|
|mountd|1, 2, 3|49850|Obsługa montowania eksportów|
|nlockmgr|1, 3, 4|53477|Blokowanie plików|
|status|1|54934|Monitorowanie stanu RPC|

**Ważne:** obsługa NFSv2, NFSv3 i NFSv4 oznacza, że serwer oferuje kilka generacji protokołu. Nie jest to samo w sobie dowodem podatności.

## **2. Co już wiemy?**

Mamy trzy istotne ustalenia:

1. `showmount -e` pokazał eksport `/` dla `*`.
    
2. `nfs-statfs` potwierdził dostęp do informacji o systemie plików.
    
3. `rpcinfo` potwierdził działające usługi NFS i mountd.
    

Wciąż nie wiemy, czy klient może odczytywać pliki i jakie obowiązują ograniczenia uprawnień.

## **3. Następny krok – kontrolowane montowanie NFS tylko do odczytu**

Teraz sprawdzimy, czy możemy zamontować eksportowany katalog główny w Kali.

Najpierw przygotuj punkt montowania:

```
sudo mkdir -p /mnt/metasploitable_nfs
```

Następnie zamontujemy zasób w trybie tylko do odczytu:

```
sudo mount -t nfs -o ro,nfsvers=3 192.168.56.104:/ /mnt/metasploitable_nfs
```

Dlaczego tak?

- `ro` – montowanie tylko do odczytu.
    
- `nfsvers=3` – jawnie wybieramy NFSv3.
    
- `/` – eksportowany katalog główny serwera.
    

Jeżeli montowanie się powiedzie, na razie niczego nie otwieraj ani nie kopiuj. Wykonaj tylko:

```
mount | grep metasploitable_nfs
```

Wklej wynik.

**Uwaga:** pracujemy na własnym Metasploitable 2, a montowanie jest ograniczone do odczytu. Po zakończeniu ćwiczenia odmontujemy zasób.

To kolejny ważny element praktyki pentesterskiej: sprawdzamy nie tylko, co serwer ujawnia, ale również czy jego eksporty można faktycznie wykorzystać z perspektywy klienta.

Świetnie. Montowanie zakończyło się powodzeniem. To bardzo ważny moment ćwiczenia NFS.

Potwierdziliśmy, że Kali może zamontować katalog główny systemu Metasploitable 2 przez NFSv3.

NFS zamontowany – tylko do odczytu

## **1. Co potwierdza wynik?**

Najważniejsze fragmenty:

```
192.168.56.104:/ on /mnt/metasploitable_nfs
type nfs
(ro,relatime,vers=3,...)
```

|Parametr|Znaczenie|
|---|---|
|`192.168.56.104:/`|Eksportowany katalog główny serwera|
|`/mnt/metasploitable_nfs`|Punkt montowania w Kali|
|`type nfs`|System plików NFS|
|`ro`|Tylko do odczytu|
|`vers=3`|NFSv3|
|`sec=sys`|Uwierzytelnianie oparte na identyfikatorach UID/GID|

Szczególnie istotne jest `sec=sys`: serwer opiera kontrolę dostępu na identyfikatorach użytkowników i grup przekazywanych przez klienta. Nie jest to silne, kryptograficzne uwierzytelnianie tożsamości użytkownika.

## **2. Następny krok – sprawdzamy, co widzimy**

Wykonaj jedno polecenie:

```
ls -lah /mnt/metasploitable_nfs/
```

Wyświetlimy zawartość katalogu głównego systemu Metasploitable 2.

Na razie:

- nie kopiujemy plików,
    
- nie otwieramy plików konfiguracyjnych,
    
- niczego nie modyfikujemy.
    

Chcemy najpierw potwierdzić zakres widoczności systemu.

## **3. Co oznacza dotychczasowy wynik dla bezpieczeństwa?**

Mamy już mocny dowód błędnej konfiguracji:

- serwer eksportuje `/`,
    
- reguła eksportu obejmuje `*`,
    
- Kali może zamontować ten zasób,
    
- montowanie tylko do odczytu pozwala nam bezpiecznie zbadać jego widoczność.
    

To potencjalnie poważny problem poufności danych. Ostateczną ocenę zakresu ekspozycji oprzemy na tym, co rzeczywiście uda się odczytać.

Czekam na wynik `ls -lah`.

To jest bardzo ważny wynik. Właśnie potwierdziliśmy, że przez NFS widzimy **strukturę całego systemu plików Metasploitable 2**, a nie tylko wybrany katalog udostępniony przez administratora.

Co więcej, pojawiły się dwa elementy, które wymagają szczególnej uwagi.

## **1. Analiza wyniku**

Poważna ekspozycja systemu plików

Najważniejsze obserwacje:

|Element|Co oznacza|
|---|---|
|`/etc`|Katalog konfiguracji systemu|
|`/home`|Katalogi użytkowników|
|`/root`|Katalog domowy administratora root|
|`/var`|Logi, dane usług i inne pliki systemowe|
|`/tmp`|Katalog tymczasowy|
|`gTmwVXExBhX`|Nietypowy plik, 1,2 MB, uprawnienia `700`|
|`vlmDGdjT`|Nietypowy plik, 1,2 MB, uprawnienia `700`|
|`nohup.out`|Plik wyjściowy procesu uruchomionego z `nohup`|

### **Szczególnie interesujące: dwa pliki o losowych nazwach**

```
-rwx------ 1 root root 1.2M Nov  2 19:10 gTmwVXExBhX
-rwx------ 1 root root 1.2M Nov 11 15:21 vlmDGdjT
```

Nie wiemy jeszcze, czym są. Nie należy zakładać, że to malware lub pliki wykonywalne związane z konkretną usługą.

Uprawnienia `700` oznaczają, że dostęp do ich zawartości ma właściciel root. Z perspektywy zwykłego użytkownika Kali nie są więc automatycznie dostępne do odczytu.

## **2. Najważniejszy wniosek bezpieczeństwa**

Mamy już potwierdzone:

1. Eksport NFS obejmuje `/`.
    
2. Reguła eksportu zawiera `*`.
    
3. Możemy zamontować system plików z Kali.
    
4. Możemy przeglądać strukturę katalogów systemowych.
    

To poważne naruszenie zasady minimalnych uprawnień i potencjalne zagrożenie poufności.

Nie wiemy jeszcze, czy serwer stosuje `root_squash`, dlatego nie wyciągamy wniosków o możliwości uzyskania uprawnień administratora.

## **3. Następny krok – sprawdzamy widoczność katalogu** `/etc`

Zamiast otwierać przypadkowe pliki, sprawdzimy metadane katalogu konfiguracyjnego.

Wykonaj:

```
ls -lah /mnt/metasploitable_nfs/etc/
```

Interesuje nas, jakie pliki konfiguracyjne są widoczne i jakie mają uprawnienia.

Na razie nie wyświetlamy zawartości plików z hasłami ani danych użytkowników.

**Ważna rzecz:** zachowajmy dotychczasowy tryb montowania `ro`. Dzięki temu nasze ćwiczenie pozostaje nieinwazyjne i nie zmieniamy systemu docelowego.

Tak, sporo — ale spokojnie, **nie będziemy analizować całego** `/etc` **plik po pliku**. Właśnie po to robimy enumerację, żeby wyłowić najważniejsze informacje.

Przejrzałem wynik. Są trzy rzeczy, które zwracają uwagę:

1. `exports` – plik konfiguracyjny NFS. Może wyjaśnić, dlaczego cały katalog `/` jest udostępniony klientom.
    
2. `passwd` – lista kont systemowych, widoczna w katalogu.
    
3. `shadow` – plik z danymi uwierzytelniającymi; ma ograniczone uprawnienia (`root:shadow`, `640`). Nie będziemy go odczytywać.
    

Zajmijmy się teraz tylko NFS. Wykonaj jedno polecenie:

```
cat /mnt/metasploitable_nfs/etc/exports
```

To pozwoli nam sprawdzić, jakie zasady eksportu skonfigurowano na serwerze. Nadal pracujemy w trybie `ro` — niczego nie zmieniamy.

**Ważne:** już teraz mamy istotne ustalenie: przez NFS widzimy strukturę całego systemu Metasploitable 2. To jest poważny problem z konfiguracją udostępniania, który warto dokładnie udokumentować.

No i mamy **bardzo ważne odkrycie**. Ten jeden wpis wyjaśnia, dlaczego mogliśmy zobaczyć strukturę całego systemu Metasploitable 2.

```
/ *(rw,sync,no_root_squash,no_subtree_check)
```

Rozłóżmy go na części:

|Opcja|Znaczenie|
|---|---|
|`/`|Udostępniony jest katalog główny całego systemu|
|`*`|Reguła obejmuje dowolnego klienta pasującego do eksportu|
|`rw`|Serwer dopuszcza odczyt i zapis|
|`sync`|Serwer zapisuje zmiany synchronicznie|
|`no_root_squash`|Zdalny użytkownik root nie jest mapowany na konto anonimowe|
|`no_subtree_check`|Wyłączono dodatkowe sprawdzanie poddrzewa|

### **Najpoważniejszy problem:** `no_root_squash`

To szczególnie niebezpieczna konfiguracja.

Wysokie ryzyko

**Co oznacza to w praktyce?**

Jeżeli klient NFS uzyska dostęp jako root, serwer nie sprowadzi jego uprawnień do anonimowego użytkownika. W połączeniu z eksportem całego `/` i prawem `rw` może to umożliwić bardzo poważną ingerencję w system.

### **Co już potwierdziliśmy?**

- Eksportowany jest cały system plików `/`.
    
- Eksport obejmuje klientów pasujących do `*`.
    
- Konfiguracja serwera dopuszcza zapis (`rw`).
    
- Wyłączono `root_squash`.
    
- Z Kali zamontowaliśmy zasób tylko do odczytu (`ro`), więc dotychczas nie testowaliśmy zapisu przez NFS.
    

**Ważne rozróżnienie:** `ro` w naszym poleceniu montowania ograniczało dostęp po stronie Kali. Nie zmieniało konfiguracji serwera.

### **Następny krok**

Na razie niczego nie zapisujemy ani nie modyfikujemy. Mamy już wystarczająco dużo dowodów, żeby uznać konfigurację NFS za poważnie niebezpieczną.

Proponuję teraz zakończyć enumerację NFS i przejść do podsumowania ustaleń.

Najważniejszy wniosek z tego etapu: **NFS jest skonfigurowany w sposób, który może umożliwić zdalnemu klientowi uzyskanie bardzo szerokiego dostępu do systemu.**

Świetna robota. Dzisiaj zrobiliśmy naprawdę solidny kawałek enumeracji. Nie ograniczyliśmy się do wykrycia portów — sprawdziliśmy rzeczywisty dostęp do usług i znaleźliśmy poważne błędy konfiguracji.

# **Podsumowanie ćwiczenia – SMB i NFS**

Etap zakończony

17 listopada 2026

## **1. SMB – Samba**

Wykryta usługa:

- Porty: `139/tcp`, `445/tcp`
    
- Samba: `3.0.20-Debian`
    
- Protokół: SMBv1 (`NT LM 0.12`)
    

Przeprowadzone testy:

|Test|Wynik|
|---|---|
|Anonimowe logowanie|Potwierdzone|
|Lista udziałów|Dostępna|
|Dostęp do `tmp`|Potwierdzony|
|Odczyt zawartości `tmp`|Potwierdzony|
|Zapis anonimowy|Potwierdzony|
|Usunięcie pliku testowego|Potwierdzone|

Najważniejsze ustalenie: udział `tmp` umożliwia anonimowy odczyt i zapis.

## **2. NFS – Network File System**

Wykryte usługi:

- `111/tcp` – rpcbind
    
- `2049/tcp` – NFS
    
- `49850/tcp` – mountd
    
- `53477/tcp` – nlockmgr
    
- `54934/tcp` – status
    

Eksport:

```
/ *(rw,sync,no_root_squash,no_subtree_check)
```

Co ustaliliśmy:

|Element|Wynik|
|---|---|
|Eksport katalogu `/`|Potwierdzony|
|Dostęp dla klientów `*`|Skonfigurowany|
|Odczyt struktury systemu|Potwierdzony|
|Zapis po stronie serwera|Dozwolony przez konfigurację|
|`no_root_squash`|Potwierdzony|
|Test zapisu przez NFS|Nie wykonywaliśmy|

Zamontowaliśmy zasób na Kali w trybie tylko do odczytu:

```
sudo mount -t nfs -o ro,nfsvers=3 192.168.56.104:/ /mnt/metasploitable_nfs
```

Dzięki temu mogliśmy zobaczyć strukturę katalogów systemu, nie wykonując żadnych zmian.

## **3. Najważniejsze znaleziska bezpieczeństwa**

**SMB – anonimowy zapis**

Wysokie ryzyko

Anonimowy użytkownik może zapisywać pliki w udziale `tmp`.

**NFS – eksport całego systemu**

Krytyczny potencjał

Eksport `/` z opcjami `rw` i `no_root_squash` stwarza bardzo poważne ryzyko przejęcia kontroli nad systemem przez odpowiednio uprzywilejowanego klienta.

Ocena dotyczy konfiguracji i potencjalnego wpływu. Nie przeprowadzaliśmy próby zapisu przez NFS ani próby eskalacji uprawnień.

## **4. Dokumentacja – co zapisujemy w notatkach**

- Pełny skan portów TCP.
    
- Identyfikacja wersji usług.
    
- Enumeracja SMB.
    
- Anonimowy dostęp do udziału `tmp`.
    
- Test zapisu i usunięcie pliku testowego.
    
- Enumeracja RPC/NFS.
    
- Odkrycie eksportu `/`.
    
- Odczyt struktury systemu przez NFS.
    
- Analiza `/etc/exports`.
    

**Na koniec dzisiejszej sesji:** odmontujmy NFS z Kali:

```
sudo umount /mnt/metasploitable_nfs
```

Potem możesz wyłączyć maszyny.

Dzisiaj najważniejsze było to, że nauczyliśmy się odróżniać samo wykrycie usługi od potwierdzenia rzeczywistego dostępu i błędnej konfiguracji.

To właśnie jest praktyczna praca pentestera: **zbieranie dowodów, ocena ryzyka i wyciąganie uzasadnionych wniosków.**