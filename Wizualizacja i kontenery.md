---

Wraz ze wzrostem popularności komputerów w życiu codziennym, zapotrzebowanie na zasoby obliczeniowe, ich dostępność i rozszerzalność są większe niż kiedykolwiek. Z uwagi na ograniczony dostęp do zasobów obliczeniowych, technologia musiała się dostosować, aby umożliwić osobom bez bezpośredniego dostępu do zasobów dostęp do nowoczesnych technologii. W ten sposób chmura obliczeniowa i wirtualizacja wysunęły się na czoło technologii jako rozwiązanie dla osób prywatnych, małych i dużych firm oraz wszystkich pośrednich sektorów.

Oprócz przetwarzania w chmurze, wirtualizacja może być również wykorzystywana do partycjonowania i tworzenia maszyn wirtualnych (VM). Umożliwia to przeprowadzanie testów atomowych, rozwój, badania i inne zastosowania, które omówimy szczegółowo w tej sali.

W tej sali dokonamy ogólnego przeglądu wirtualizacji i jej zastosowań, stopniowo poznając konkretne technologie wirtualizacji wykorzystywane w nowoczesnych środowiskach.

### Cele edukacyjne

- Dowiedz się, czym jest wirtualizacja oraz jak i dlaczego się ją stosuje.
- Poznaj powszechnie stosowane technologie wirtualizacji, w tym hiperwizory i kontenery.
- Praktyczne wykorzystanie technologii wirtualizacji i zrozumienie ich zastosowań w zakresie bezpieczeństwa i nowoczesnych komputerów.

Sala ta jest przeznaczona do nauczania zaawansowanych koncepcji od podstaw i nie wymaga żadnych warunków wstępnych.

W najbardziej podstawowym rozumieniu wirtualizacja to koncepcja kapsułkowania możliwości i cech maszyny fizycznej w środowisku wirtualnym, zwanym  **maszyną wirtualną** .

Ale dlaczego wirtualizacja jest potrzebna? Dla większości organizacji i osób wirtualizacja wynika z następujących potrzeb:

- **Zmniejszenie wydatków:**  Serwery fizyczne mogą być drogie, a wirtualizacja może zmniejszyć liczbę serwerów i innego sprzętu, a nawet całkowicie wyeliminować sprzęt fizyczny z infrastruktury firmy.
- **Skala:**  Bez odpowiedniej implementacji DevOps, skalowanie zasobów może być dla firmy trudne wraz ze wzrostem wykorzystania serwerów. Wirtualizacja ułatwia ten proces i umożliwia delegowanie zasobów serwera do maszyn wirtualnych w zależności od potrzeb, w zależności od obciążenia.
- **Wydajność:**  Podobnie jak skalowanie, wirtualizacja może także ułatwić zmniejszenie zasobów przydzielanych maszynie wirtualnej w przypadku zmniejszonego ich wykorzystania.

Technologia wirtualizacji  

W tym momencie możesz zapytać, jak możliwa jest wirtualizacja. Chociaż jest to złożone pytanie, w tym pomieszczeniu omówimy szczegółowo różne technologie i platformy, omawiając pokrótce, w jaki sposób oddziałują one na system operacyjny hosta.  

Aby odpowiedzieć na powyższe pytanie, musimy rozszerzyć definicję wirtualizacji. Formalnie wirtualizacja abstrahuje lub tworzy  **warstwę abstrakcji**  na sprzęcie komputerowym. Warstwa abstrakcji umożliwia podzielenie jednego urządzenia na wiele komputerów wirtualnych, zwanych również maszynami wirtualnymi (VM).  

Mówiąc prościej, oznacza to, że maszyna wirtualna będzie miała dostęp do  _zasobów logicznych_  , które są odseparowane od  _zasobów fizycznych_ .

### Struktura wirtualizacji

Wirtualizacja jest implementowana w formacie silnik-maszyna, co oznacza, że ​​oprogramowanie lub system tworzy warstwę abstrakcji i przydziela zasoby, a następnie system operacyjny lub aplikacja może zostać zainstalowana na tym zwirtualizowanym środowisku. System operacyjny zainstalowany na maszynie wirtualnej nazywany jest gościem  **.System operacyjny**, w przeciwieństwie do  **gospodarza System operacyjny** na którym działa silnik wirtualizacji.  

W kolejnym zadaniu przedstawimy nasz pierwszy typ silnika wirtualizacji -  **hiperwizory** .

W poprzednim zadaniu przedstawiliśmy koncepcję wirtualizacji na wysokim poziomie i krótko omówiliśmy jej strukturę. W tym zadaniu zaprezentujemy nasz pierwszy typ silnika wirtualizacji:  **hiperwizory** .  

Hiperwizor umożliwia tworzenie warstwy abstrakcji między sprzętem a oprogramowaniem. Hiperwizor zazwyczaj zawiera również jakąś formę aplikacji lub oprogramowania zarządzającego, które zapewnia interfejs między użytkownikiem końcowym a warstwą abstrakcji w celu tworzenia lub ładowania maszyn wirtualnych.  

Hiperwizory dzielą się na dwie kategorie, które zależą od ich położenia względem sprzętu. Mogą one albo bezpośrednio tworzyć lekki system operacyjny na sprzęcie, który jest hiperwizorem, albo dodawać hiperwizor jako aplikację na istniejącym już systemie operacyjnym.  

### Hiperwizory typu 1

**Hiperwizory typu 1** , znane również jako  **hiperwizory typu bare metal** , tworzą warstwę abstrakcji bezpośrednio między sprzętem a maszynami wirtualnymi, bez wspólnego systemu operacyjnego. Zamiast tego, hiperwizorem jest system operacyjny i często jest on  _bezobsługowy_ , z jedynie internetowym portalem zarządzania, do którego można uzyskać zdalny dostęp. Te hiperwizory zostały zaprojektowane z myślą o skalowalności i jednoczesnym wdrażaniu dużej liczby maszyn wirtualnych. Są niezwykle lekkie, co pozwala im poświęcić najwięcej zasobów maszynom wirtualnym. Poniżej znajduje się schemat architektury hiperwizora typu 1.  

![Schemat hiperwizora typu 1](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e73cca6ec4fcf1309f2df86/room-content/10f4dce97b527ea3d144442b2190270c.png)  

Przykładami hiperwizorów typu 1 są VMware ESXi, Proxmox, VMware vSphere, Xen i KVM.  

### Hiperwizory typu 2

**Hiperwizory typu 2** , znane również jako **hiperwizory hostowane** , tworzą warstwę abstrakcji z aplikacji programowej zbudowanej na istniejącym systemie operacyjnym. W przeciwieństwie do hiperwizorów typu 1, hiperwizory typu 2 są często zarządzane bezpośrednio z aplikacji za pośrednictwem Interfejs graficzny. Te hiperwizory są często przeznaczone dla użytkowników końcowych lub osób prywatnych, takich jak programiści, i nie są przeznaczone wyłącznie do obsługi dużej liczby maszyn wirtualnych w celu zapewnienia skalowalności. Poniżej znajduje się schemat architektury hiperwizora typu 2.  

![Schemat hiperwizora typu 2](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e73cca6ec4fcf1309f2df86/room-content/44d3a52445a0194a28eb710bf16f52d6.png)  

Przykładami hiperwizorów typu 2 są VMware Workstation, VMware Fusion, VirtualBox, Parallels i QEMU.

Hiperwizory działają zgodnie z oczekiwaniami w wielu przypadkach użycia, ale zaczynają napotykać problemy podczas skalowania lekkich aplikacji. _Mikrousługi_ stanowią dobry przykład architektury aplikacji, która napotyka problemy po wdrożeniu z hiperwizora. mikrousługa to struktura aplikacji podzielona na mniejsze usługi, które są skalowalne i wykorzystują lekkie protokoły i funkcje. Lekka natura tej architektury stwarza oczywiste problemy dla hiperwizorów, które wymagają dużej liczby maszyn wirtualnych, z których każda charakteryzuje się wysokim zużyciem zasobów.

****Kontenery**** są obecnie rozwiązaniem problemów napotykanych w przypadku hiperwizorów na dużą skalę.

### Czym są kontenery

Kontenery mają wiele wspólnego z maszynami wirtualnymi, ale zamiast być całkowicie odizolowane od systemu operacyjnego hosta, kontenery dzielą z nim pewne właściwości. Kontenery mają własny system plików, czyli część zasobów obliczeniowych (Procesor,BARAN), przestrzeń procesową i wiele innych.   

Oprócz oczywistych zalet wynikających z lekkości, pojemniki są również _przenośne_ i _wytrzymałe,_ ponieważ nie są zupełnie abstrakcyjne.   

Pojemnik Silniki to nasz drugi rodzaj wirtualizacji. Ponieważ maszyny wirtualne wykorzystują hiperwizor do tworzenia warstwy abstrakcji dla wirtualizacji, kontenery korzystają zpojemnikSilnik służący do tworzenia warstwy abstrakcji przy użyciu zasobów logicznych.

W następnym zadaniu przedstawimy nasze pierwszepojemniksilnik -  **Docker** .

Jeśli ktoś zna się na kontenerach, Docker jest prawdopodobnie pierwszą nazwą, jaka przychodzi mu na myśl. Docker to pojemnik platforma i silnik służące do uruchamiania „obrazów” Dockera jako kontenerów.

Każdy obraz Dockera składa się z obrazu bazowego, takiego jak Alpine lub Ubuntu, który jest specjalnie zaprojektowany do użytku w kontenerach i ma niewielką wagę. Aby zbudować obraz Dockera, należy utworzyć plik Dockerfile, który definiuje obraz bazowy dla pojemniki wszelkie polecenia, które mają zostać uruchomione.  

Więcej informacji na temat Dockera znajdziesz w  pokoju [Wprowadzenie do Dockera](https://tryhackme.com/room/introtodockerk8pdqk)  .  

### Uruchamianie i interakcja z DockeremPojemnik

Docker Hub to zdalne repozytorium obrazów Docker, podobne do GitHub – zdalnego repozytorium Git Korzystając z Docker Hub, możemy pobierać obrazy Dockera utworzone przez innych lub przesyłać własne.  

```bash
docker pull <user>/<image>
```

Alternatywnie, obraz kontenera może zostać automatycznie pobrany podczas pierwszego uruchomienia kontenera. Po pierwszym pobraniu kontenera zostanie on zapisany w pamięci podręcznej lokalnie, a Docker wyszuka go lokalnie przed próbą pobrania.  

```bash
docker run <user>/<image>
```

Po uruchomieniu obrazu możemy sprawdzić, czy silnik Dockera działa pojemnik wyświetlając listę procesów uruchomionych w Dockerze za pomocą poniższego polecenia.  

```bash
docker ps
```

Z powyższego polecenia wynika, że ​​kontenerowi zostanie przypisany losowy identyfikator, adres IP i interfejs sieciowy.

### Aplikacja praktyczna

Aby zapoznać się z kontenerami i Dockerem, wdrożymy serwer webowy Flask w kontenerze Docker.  Aby uzyskać dostęp do terminala, wdróż maszynę wirtualną dołączoną do tego zadania, naciskając zielony przycisk **„Uruchom maszynę”** . Poczekaj 3–5 minut na wdrożenie maszyny. Maszyna uruchomi się w widoku podzielonym; jeśli maszyna się nie pojawi, kliknij niebieski przycisk **„Pokaż widok podzielony”** znajdujący się w prawym górnym rogu tej sali. Alternatywnie, możesz uzyskać dostęp do maszyny przez SSH, używając poniższych danych logowania.

Adres IP maszyny:  `MACHINE_IP` Nazwa użytkownika:  `thmuser` Hasło: `TryHackMe!`  

Przed uruchomieniem kontenera Docker musimy najpierw wprowadzić dwie nowe flagi, które muszą być używane z poleceniem `run`, aby umożliwićpojemnikAby odłączyć się od bieżącego terminala ( `-d`) i udostępnić porty zewnętrznie ( `-p`). Poniżej znajduje się wymagana składnia uruchomienia przykładowej aplikacji Flask w kontenerze Docker, udostępniając serwer WWW na porcie 5000.  

```bash
docker run -p 5000:5000 -d cryillic/thm_example_app 
```

Aby sprawdzić, czy serwer WWW działa w Dockerzepojemnik, możemy zeskanowaćpojemniklub uzyskaj dostęp do wskazanego portu w przeglądarce internetowej.  
  
**Uwaga:** niektóre znaki specjalne mogą nie być widoczne na podanym porcie.Maszyna wirtualnaPodczas kopiowania i wklejania wszystkie znaki nadal zostaną skopiowane.

Dzięki wykorzystaniu hiperwizorów i kontenerów rozwiązuje się większość problemów związanych z tradycyjnym przetwarzaniem, takich jak  _koszty_ i  _wydajność_ . Pozostaje jednak pytanie: co, jeśli potrzebujemy szybszego i bardziej skalowalnego rozwiązania? Oznacza to, że wraz ze zmianą obciążenia lub innych kryteriów, zasoby lub liczba instancji przydzielonych do aplikacji lub usługi będą zwiększać się lub zmniejszać w locie, w zależności od potrzeb.

**Kubernetes**, w skrócie „ **K8s** ”, to jedno z takich rozwiązań, znane jako  **platforma orkiestracji** . Platforma orkiestracji ma na celu integrację z innymi produktami, takimi jak Docker, i rozszerzenie ich możliwości lub „synchronizację” ich z innymi produktami lub aplikacjami.

Kubernetes opiera się na tradycyjnych modelach wirtualizacji, takich jak hiperwizory i kontenery, i rozszerza ich zastosowania, funkcje i możliwości.

Możliwości i funkcje obejmują następujące elementy:

- **Skalowanie poziome** : W przeciwieństwie do tradycyjnego skalowania „pionowego”, skalowanie „poziome” polega na dodawaniu urządzeń lub maszyn w celu obsługi zwiększonego obciążenia pracą, zamiast dodawania zasobów logicznych, takich jak Procesor Lub BARAN.
- **Rozszerzalność** : Klastry można modyfikować dynamicznie, nie wpływając na kontenery spoza docelowej grupy.
- **Samonaprawianie** : K8 może automatycznie ponownie uruchamiać, zastępować, zmieniać harmonogram i zamykać kontenery, które nie działają prawidłowo, na podstawie zdefiniowanych przez użytkownika kontroli kondycji.
- **Automatyczne wdrażanie i wycofywanie** : K8 może stopniowo wdrażać zmiany w kontenerach. W miarę wprowadzania zmian monitoruje stan aplikacji i decyduje, czy kontynuować wdrażanie, czy wycofywać. Zapewnia to stałą dostępność klastra, nawet w przypadku awarii niektórych kontenerów.

### Aplikacja praktyczna

Aby umożliwić Ci praktyczne zapoznanie się z K8s, udostępniliśmy Ci dostęp do wstępnie wdrożonego klastra skonfigurowanego za pomocą _kubectl_ . Ponieważ Kubernetes Chociaż domyślnie zapewnia większość podstawowej automatyzacji, chcemy, abyś samodzielnie odkrył różnice między K8 a tradycyjną platformą wirtualizacyjną. Kubernetesto duża platforma z bogatą listą funkcji. Zachęcamy do dalszego zgłębiania tematu. DevOpsi funkcji K8s, ponieważ dostarczymy Ci tylko podstawowy zestaw pytań, aby rozpocząć eksplorację Kubernetes grupa.

Aby uzyskać dostęp do klastra,  wdróż maszynę wirtualną dołączoną do tego zadania, naciskając zielony przycisk „Uruchom maszynę” . Wdrożenie maszyny zajmie od 3 do 5 minut. Maszyna uruchomi się w widoku podzielonym; jeśli się nie pojawi, kliknij niebieski przycisk „Pokaż widok podzielony”  znajdujący się w prawym górnym rogu tego pomieszczenia.   

Aby ułatwić Ci korzystanie z kubectl, możesz skorzystać z dostępnego  [tutaj odnośnika online(otwiera się w nowej karcie)](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)Zachęcamy  do korzystania z podpowiedzi, które pomogą Ci odpowiedzieć na pytania.
