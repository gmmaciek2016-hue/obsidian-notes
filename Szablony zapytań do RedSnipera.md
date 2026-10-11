

Oto gotowe szablony zapytań (promptów), które możesz wklejać do swojego lokalnego RedSnipera w zależności od tego, w jakim punkcie CTF-a aktualnie się znajdujesz:

### 1. Faza: Rekonesans i Skanowanie (Nmap)

Gdy wspólnie ustalamy, że czas przeszukać porty lub wersje usług, pytasz RedSnipera o optymalne flagi:

- **Prompt do RedSnipera:**
    
    > `RedSniper, podaj mi optymalną komendę Nmap do szybkiego skanowania wszystkich portów TCP z detekcją wersji usług i zapisem do pliku tekstowego.`
    

### 2. Faza: Skanowanie katalogów (Gobuster / Dirsearch)

Gdy omówimy, że na porcie 80 działa serwer WWW i szukamy ukrytych ścieżek:

- **Prompt do RedSnipera:**
    
    > `RedSniper, daj mi komendę Gobuster do enumeracji katalogów na stronie HTTP ze wskazaniem standardowego słownika z Kali Linux.`
    

### 3. Faza: Analiza formularza uploadu i rozszerzeń (Nasza obecna sytuacja)

Gdy omawiamy, jak działa przesyłanie plików i chcesz sprawdzić techniczne triki z HackTricks:

- **Prompt do RedSnipera:**
    
    > `RedSniper, sprawdź w bazie HackTricks jakie są najpopularniejsze alternatywne rozszerzenia plików dla PHP (np. phtml, phar) omijające słabe filtry rozszerzeń.`
    

### 4. Faza: Składnia Netcata i nasłuch

Gdy ustalamy teorię połączeń zwrotnych, a Ty potrzebujesz czystej składni:

- **Prompt do RedSnipera:**
    
    > `RedSniper, podaj dokładną składnię Netcata do otwarcia stabilnego nasłuchu na porcie 4444 w trybie verbose.`
    

### 5. Faza: Szukanie flagi i post-eksploatacja

Gdy masz już powłokę i szukasz konkretnych plików w systemie Linux:

- **Prompt do RedSnipera:**
    
    > `RedSniper, podaj składnię polecenia find w Linuxie do wyszukiwania plików o nazwie "user.txt" w całym systemie z ukryciem błędów braku dostępu (Permission denied).`