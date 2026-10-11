
Oto wyniki skanowania Nmap:

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Welcome to Internal Portal
|_http-server-header: Apache/2.4.41 (Ubuntu)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2

Przeanalizuj powyższe wyniki skanowania w języku polskim. Wskaż najważniejsze wektory ataku i podaj mi konkretne komendy do przeprowadzenia dalszego rekonesansu usług SMB oraz HTTP.




@Szablon - Pentest przeanalizuj ten skan opierając się na pliku @HackTricks - Samba: [Wklej skan]


@Szablon - Pentest przeanalizuj ten skan opierając się na pliku @HackTricks - Samba: Oto wyniki skanowania Nmap: PORT STATE SERVICE VERSION 22/tcp open ssh OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0) 80/tcp open http Apache httpd 2.4.41 ((Ubuntu)) |_http-title: Welcome to Internal Portal |_http-server-header: Apache/2.4.41 (Ubuntu) 139/tcp open netbios-ssn Samba smbd 4.6.2 445/tcp open netbios-ssn Samba smbd 4.6.2