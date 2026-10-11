---

THM{1d0r_h0r1z0nt4l_4cc3ss_fl4g1}
THM{bl1nd_x55_s3ss10n_h1j4ck_fl4g2}
THM{rf1_2_rc3_f00th0ld_fl4g3}
THM{s5h_cr3d_r3u53_l4t3r4l_flag4}
THM{pr1v3sc_cr0n_r00t_fl4g5}
## KROK 1 — Recon

Zakładam, że masz już uruchomioną maszynę Domino i znasz jej `MACHINE_IP`.

Na swojej maszynie wykonaj:

nmap -sC -sV -p- <MACHINE_IP>
nmap -sC -sV -p- -T4 <MACHINE_IP>

@ip-10-130-70-238:~# nmap -sC -sV -p- -T4 10.130.177.50
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-09-05 11:36 UTC
Nmap scan report for ip-10-130-177-50.eu-west-3.compute.internal (10.130.177.50)
Host is up (0.00021s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 01:bf:c7:a1:3a:0a:2d:2a:cc:a0:fe:6b:dc:22:e5:a9 (ECDSA)
|_  256 ac:77:9a:6d:56:d1:c0:46:c5:44:ac:36:22:77:23:e1 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: NexusCorp Portal
|_http-server-header: Apache/2.4.58 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.34 seconds

Nasza hipoteza:

> "Employee Portal" prawdopodobnie ma błędy logiczne / aplikacyjne, a nie podatność samego Apache.

Nie zaczynamy od exploitów. Najpierw musimy zrozumieć aplikację.

---

# KROK 2 — Manualna enumeracja HTTP

Otwórz stronę:

```
http://10.130.177.50
```

I sprawdź:

1. Co widzisz na stronie głównej?
2. Czy jest:
    - login?
    - rejestracja?
    - linki?
    - informacje o użytkownikach?
    - endpointy typu `/admin`, `/dashboard`, `/profile`?

Możesz też od razu zrobić podstawowy rekonesans nagłówków:

```
curl -I http://10.130.177.50
```

oraz pobrać HTML:

```
curl http://10.130.177.50
```

root@ip-10-130-70-238:~# curl -I http://10.130.177.50
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 11:39:12 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Type: text/html; charset=UTF-8

root@ip-10-130-70-238:~# curl http://10.130.177.50
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
    <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>

Bardzo dobrze. Mamy kolejny **evidence point**.

Z HTML widzimy kilka ważnych rzeczy:

```
<form method="POST" action="/index.php">
<input type="text" name="username">
<input type="password" name="password">
```

Czyli:

- aplikacja jest prawdopodobnie PHP (`index.php`, `forgot.php`, `team.php`)
- mamy formularz logowania
- istnieje:
    - `/forgot.php`
    - `/team.php`

Opis CTF mówił o:

> "authentication controls and role-based access"

Czyli spodziewamy się, że problem może być związany z:

- logowaniem,
- odzyskiwaniem hasła,
- rolami użytkowników.

Nie próbujemy jeszcze SQL injection ani brute force. Najpierw sprawdzamy **powierzchnię aplikacji**.

---

# KROK 3 — Enumeracja dostępnych stron

Teraz sprawdzimy, jakie endpointy istnieją.

Użyjemy lekkiego fuzzingu katalogów:

Jeżeli masz `gobuster`:

```
gobuster dir -u http://10.130.177.50 -w /usr/share/wordlists/dirb/common.txt -x php
```

Jeżeli nie masz gobustera:

```
feroxbuster -u http://10.130.177.50 -x php
```

Cel:

Nie szukamy jeszcze exploitów.

Chcemy znaleźć:

- ukryte strony,
- backupy,
- panele,
- pliki PHP.

---

Dlaczego teraz?

Mamy już:

```
/
├── index.php
├── forgot.php
└── team.php
```

Ale aplikacje CTF często chowają np.:

```
/admin.php
/backup.php
/config.php
/dashboard.php
```

---

Uruchom jeden z tych skanerów i wklej wynik.

root@ip-10-130-70-238:~# gobuster dir -u http://10.130.177.50 -w /usr/share/wordlists/dirb/common.txt -x php
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.130.177.50
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.hta.php             (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/403.php              (Status: 200) [Size: 322]
/admin                (Status: 301) [Size: 314] [--> http://10.130.177.50/admin/]
/api                  (Status: 301) [Size: 312] [--> http://10.130.177.50/api/]
/auth.php             (Status: 200) [Size: 0]
/backup               (Status: 301) [Size: 315] [--> http://10.130.177.50/backup/]
/config.php           (Status: 200) [Size: 0]
/dashboard.php        (Status: 302) [Size: 0] [--> /index.php]
/forgot.php           (Status: 200) [Size: 684]
/index.php            (Status: 200) [Size: 861]
/index.php            (Status: 200) [Size: 861]
/javascript           (Status: 301) [Size: 319] [--> http://10.130.177.50/javascript/]
/logout.php           (Status: 302) [Size: 0] [--> /index.php]
/server-status        (Status: 403) [Size: 278]
/static               (Status: 301) [Size: 315] [--> http://10.130.177.50/static/]
/support              (Status: 301) [Size: 316] [--> http://10.130.177.50/support/]
/team.php             (Status: 200) [Size: 3747]
Progress: 9228 / 9230 (99.98%)
===============================================================

Świetnie. To jest bardzo dobry wynik. Teraz zatrzymujemy się i **czytamy go jak pentester**, a nie lecimy od razu w exploity.

Mamy kilka bardzo interesujących punktów:

```
/admin          301
/api            301
/backup         301
/auth.php       200 (0 bytes)
/config.php     200 (0 bytes)
/dashboard.php  302 -> /index.php
/forgot.php     200
/team.php       200
```

### Nasze obserwacje

#### 1. `/admin/`

To prawdopodobnie będzie cel związany z pytaniem:

> "What is the flag displayed on the admin panel after gaining admin access?"

Ale jeszcze nie mamy dostępu.

---

#### 2. `/api/`

Bardzo interesujące.

Opis CTF mówił:

> "observe how the application behaves, interact with its endpoints, and identify weak trust boundaries"

Słowo **endpoints** często wskazuje właśnie API.

---

#### 3. `/backup/`

Ciekawy punkt.

Backupy często zawierają:

- stare pliki,
- konfiguracje,
- hasła,
- źródła aplikacji.

Ale nie skaczemy jeszcze tam.

---

#### 4. `/config.php`

Status 200, rozmiar 0.

To może oznaczać:

- pusty endpoint,
- plik PHP, który wykonuje tylko include,
- zabezpieczenie przed pokazaniem treści.

Na razie odkładamy.

---

Teraz wybieramy **najbardziej logiczną ścieżkę**.

Mamy login:

```
index.php
   |
   +-- forgot.php
```

oraz mamy opis:

> "multiple small weaknesses ... combined"

Czyli możliwe, że pierwsza słabość jest banalna.

---

# KROK 4 — Sprawdzamy funkcję "Forgot password"

Wejdź:

```
http://10.130.177.50/forgot.php
```

albo:

```
curl http://10.130.177.50/forgot.php
```

Chcemy zobaczyć:

- jakie dane przyjmuje,
- czy pyta o username/email,
- czy ujawnia informacje.

**Nie próbuj jeszcze zgadywać haseł.**

---

Twoje zadanie:

Wklej mi wynik:

```
curl http://10.130.177.50/forgot.php
```

albo opisz formularz.

root@ip-10-130-70-238:~# curl http://10.130.177.50/forgot.php
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forgot Password - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Password Reset</h2>
      <form method="POST" action="/forgot.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <button type="submit" class="btn-primary">Request Reset</button>
  </form>
  <div class="links"><a href="/index.php">Back to login</a></div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Dobrze. Mamy kolejny kawałek układanki.

Analiza:

`forgot.php` przyjmuje:

```
<form method="POST" action="/forgot.php">

<input type="text" name="username">

<button>
Request Reset
```

Czyli aplikacja nie pyta o:

- email,
- token,
- stary password.

Tylko:

```
username → reset
```

To jest potencjalnie **granica zaufania**.

Ale zanim zaczniemy manipulować requestami, musimy zobaczyć **jak aplikacja odpowiada**.

---

# KROK 5 — Testujemy normalne zachowanie resetu

Wyślijmy przykładowy username.

Użyjemy `curl` z POST:

```
curl -X POST http://10.130.177.50/forgot.php -d "username=test"
```

Nie używamy jeszcze żadnych prawdziwych nazw.

Cel:

Sprawdzić:

- czy mówi "user not found"?
- czy zawsze pokazuje sukces?
- czy ujawnia informacje?

To jest klasyczny test:

> "Czy endpoint zdradza, które konta istnieją?"

---

Wykonaj:

```
curl -X POST http://10.130.177.50/forgot.php -d "username=test"
```

i wklej odpowiedź.

Potem porównamy zachowanie.

oot@ip-10-130-70-238:~# curl -X POST http://10.130.177.50/forgot.php -d "username=test"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forgot Password - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Password Reset</h2>
  <div class="alert alert-danger">No account found with that username.</div>    <form method="POST" action="/forgot.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <button type="submit" class="btn-primary">Request Reset</button>
  </form>
  <div class="links"><a href="/index.php">Back to login</a></div>
</div>

Dobrze. To jest dokładnie ten rodzaj obserwacji, którego szukamy.

Mamy teraz nowe **evidence**:

Request:

```
POST /forgot.php
username=test
```

Response:

```
<div class="alert alert-danger">
No account found with that username.
</div>
```

### Co z tego wynika?

Aplikacja **ujawnia istnienie kont**.

Czyli mamy klasyczny:

> **username enumeration**

Jeżeli podamy istniejącego użytkownika, odpowiedź prawdopodobnie będzie inna.

To pasuje do opisu CTF:

> "authentication controls ... small weaknesses ... combined"

Pierwsza mała słabość:

- możemy znaleźć prawidłowe nazwy użytkowników.

---

Teraz potrzebujemy listy potencjalnych użytkowników.

W HTML z loginu było:

```
placeholder="firstname.lastname"
```

To jest wskazówka.

Mamy też stronę:

```
/team.php
```

Bardzo możliwe, że właśnie tam aplikacja zdradza pracowników.

---

# KROK 6 — Sprawdzamy listę zespołu

Wykonaj:

```
curl http://10.130.177.50/team.php
```

Nie analizujemy jeszcze loginu ani haseł.

Chcemy tylko odpowiedzieć na pytanie:

**Jakie username'y mogą istnieć?**

root@ip-10-130-70-238:~# curl http://10.130.177.50/team.php
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<title>NexusCorp - Our Team</title>
<link rel=stylesheet href=/static/style.css>
<style>
.team-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
.team-card { background: #1a1d2e; border: 1px solid #2d3148; border-radius: 12px; padding: 1.5rem; }
.team-card .avatar { width: 56px; height: 56px; border-radius: 50%; background: #6c63ff; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 1rem; }
.team-card h3 { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.25rem; }
.team-card .role { font-size: 0.82rem; color: #6c63ff; margin-bottom: 0.5rem; }
.team-card .dept { font-size: 0.8rem; color: #64748b; margin-bottom: 0.75rem; }
.team-card .email { font-size: 0.82rem; color: #94a3b8; font-family: monospace; }
.team-card .email a { color: #94a3b8; text-decoration: none; }
.team-card .email a:hover { color: #6c63ff; }
.page-header { border-bottom: 1px solid #2d3148; padding-bottom: 1rem; margin-bottom: 0.5rem; }
.page-header h1 { font-size: 1.6rem; }
.page-header p { color: #64748b; font-size: 0.9rem; margin-top: 0.4rem; }
</style>
</head>
<body>
<nav class=navbar>
  <div class=nav-brand><span style=color:#6c63ff>&#9650;</span> NexusCorp</div>
  <div class=nav-links>
    <a href=/index.php>Employee Login</a>
    <a href=/team.php style=color:#e2e8f0>Our Team</a>
  </div>
</nav>
<div class=container>
  <div class=page-header>
    <h1>Our Team</h1>
    <p>Meet the people behind NexusCorp's mission to deliver secure, innovative solutions.</p>
  </div>
  <div class=team-grid>

    <div class=team-card>
      <div class=avatar>LH</div>
      <h3>Laura Hayes</h3>
      <div class=role>Chief Information Officer</div>
      <div class=dept>Executive Leadership</div>
      <div class=email><a href=mailto:laura.hayes@nexus.corp>laura.hayes@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>MC</div>
      <h3>Michael Chen</h3>
      <div class=role>Lead Security Engineer</div>
      <div class=dept>Information Security</div>
      <div class=email><a href=mailto:michael.chen@nexus.corp>michael.chen@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>SJ</div>
      <h3>Sarah Johnson</h3>
      <div class=role>Senior Software Engineer</div>
      <div class=dept>Engineering</div>
      <div class=email><a href=mailto:sarah.johnson@nexus.corp>sarah.johnson@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>RW</div>
      <h3>Robert Wilson</h3>
      <div class=role>DevOps Engineer</div>
      <div class=dept>Infrastructure</div>
      <div class=email><a href=mailto:robert.wilson@nexus.corp>robert.wilson@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>ET</div>
      <h3>Emma Taylor</h3>
      <div class=role>Product Manager</div>
      <div class=dept>Product</div>
      <div class=email><a href=mailto:emma.taylor@nexus.corp>emma.taylor@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>DB</div>
      <h3>David Brown</h3>
      <div class=role>Full Stack Developer</div>
      <div class=dept>Engineering</div>
      <div class=email><a href=mailto:david.brown@nexus.corp>david.brown@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>JW</div>
      <h3>James Wright</h3>
      <div class=role>Systems Administrator</div>
      <div class=dept>Infrastructure</div>
      <div class=email><a href=mailto:james.wright@nexus.corp>james.wright@nexus.corp</a></div>
    </div>

  </div>
</div>
</body>
</html>

Bardzo dobrze. To jest dokładnie ten moment, gdzie zaczynamy łączyć małe informacje.

Mamy teraz:

## Evidence 1 — lista pracowników

`team.php` ujawnił nam potencjalne konta:

```
laura.hayes
michael.chen
sarah.johnson
robert.wilson
emma.taylor
david.brown
james.wright
```

Format zgadza się z loginem:

```
firstname.lastname
```

czyli mamy prawdopodobne username'y.

---

## Evidence 2 — role

Zwróć uwagę na jednego użytkownika:

```
Laura Hayes
Chief Information Officer
Executive Leadership
```

oraz:

```
Michael Chen
Lead Security Engineer
Information Security
```

i:

```
Robert Wilson
DevOps Engineer
Infrastructure
```

Dlaczego to ważne?

Pytania końcowe mówią:

- admin user's profile notes
- admin panel
- RCE
- devops user's home directory
- root flag

Czyli w systemie prawdopodobnie istnieją role:

```
employee
   ↓
admin
   ↓
devops
   ↓
root
```

Nie wiemy jeszcze, kto jest kim.

---

Teraz wracamy do naszej znalezionej słabości:

> forgot password ujawnia, czy użytkownik istnieje.

Musimy sprawdzić, czy konta z `team.php` rzeczywiście istnieją.

---

# KROK 7 — Username enumeration

Nie robimy jeszcze brute force.

Sprawdzimy jedno konto.

Zacznijmy od najbardziej interesującego:

```
laura.hayes
```

Wykonaj:

```
curl -X POST http://10.130.177.50/forgot.php -d "username=laura.hayes"
```

Porównamy odpowiedź z:

```
username=test
```

Szukamy różnicy.

---

Jeżeli konto istnieje, odpowiedź powinna być inna.

Wklej wynik.

(PS. Bardzo dobrze prowadzisz notatki przez wklejanie surowych wyników — dokładnie tak powinno wyglądać podejście pod PT1: **evidence przed teorią**.)

root@ip-10-130-70-238:~# curl -X POST http://10.130.177.50/forgot.php -d "username=laura.hayes"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forgot Password - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Password Reset</h2>
    <div class="alert alert-success">Password reset instructions have been sent to la****@nexus.corp</div>  <form method="POST" action="/forgot.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <button type="submit" class="btn-primary">Request Reset</button>
  </form>
  <div class="links"><a href="/index.php">Back to login</a></div>
</div>
</body>
</html>

Bardzo dobrze. Mamy potwierdzenie pierwszej hipotezy.

Porównanie:

### Nieistniejący użytkownik

```
username=test
```

Odpowiedź:

```
No account found with that username.
```

---

### Istniejący użytkownik

```
username=laura.hayes
```

Odpowiedź:

```
Password reset instructions have been sent to la****@nexus.corp
```

---

## Wniosek (finding)

Mamy:

> **Username Enumeration via Password Reset Functionality**

Aplikacja ujawnia, które konta istnieją.

To jest pierwsza cegiełka.

---

Teraz musimy zrozumieć **reset password flow**.

Zwróć uwagę na komunikat:

```
Password reset instructions have been sent to la****@nexus.corp
```

Czyli aplikacja sugeruje, że gdzieś istnieje mechanizm resetowania.

Pytanie:

- czy faktycznie wysyła maila? (pewnie nie)
- czy generuje token?
- czy endpoint resetu istnieje?
- czy jest ukryty w aplikacji?

---

Mamy jeszcze wcześniej znalezione ciekawe rzeczy:

```
/auth.php
/config.php
/admin/
/api/
```

Teraz zaczynamy sprawdzać **logikę aplikacji**, a nie losowe katalogi.

---

# KROK 8 — Sprawdźmy endpoint API

Wejdźmy w `/api/`.

Najpierw zwykły GET:

```
curl http://10.130.177.50/api/
```

Nie zakładamy jeszcze niczego.

Chcemy zobaczyć:

- czy jest listing,
- komunikat,
- JSON,
- dostępne endpointy.

Wklej wynik.

---

Mała obserwacja mentora: bardzo dobrze, że nie poszliśmy od razu w "gotowe rozwiązanie z write-upa". Już teraz samodzielnie odkryłeś:

1. PHP stack,
2. endpoint resetu,
3. user enumeration,
4. listę użytkowników,
5. potencjalne role.

To jest dokładnie sposób myślenia, którego potrzebujesz na PT1.

Dobrze. Ciekawy wynik — **pusty response**.

Mamy:

```
curl http://10.130.177.50/api/
```

wynik:

```
(brak odpowiedzi)
```

To nam mówi kilka rzeczy:

- `/api/` istnieje (Gobuster znalazł redirect `301`)
- ale root API nie zwraca danych
- prawdopodobnie endpointy są głębiej, np.:

```
/api/users
/api/auth
/api/reset
/api/profile
```

Nie będziemy zgadywać. Mamy narzędzie do tego.

---

# KROK 9 — Enumeracja API

Użyjemy Gobustera, ale tym razem celujemy w `/api/`.

Wykonaj:

```
gobuster dir -u http://10.130.177.50/api/ -w /usr/share/wordlists/dirb/common.txt
```

Nie dodawaj jeszcze `-x php`.

Dlaczego?

Bo API często działa jako:

- endpointy bez rozszerzeń,
- JSON,
- routing aplikacji.

Szukamy nazw zasobów.

---

Po wyniku zwróć uwagę szczególnie na:

```
200
401
403
405
```

Nie tylko 200.

W API często:

- `401` = endpoint istnieje, ale wymaga auth
- `403` = istnieje, ale zabroniony
- `405` = istnieje, ale zła metoda HTTP

---

Wklej wynik Gobustera.

Następny krok wybierzemy na podstawie tego, co API nam pokaże.

root@ip-10-130-70-238:~# gobuster dir -u http://10.130.177.50/api/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.130.177.50/api/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/auth                 (Status: 301) [Size: 317] [--> http://10.130.177.50/api/auth/]
/index.php            (Status: 200) [Size: 2]
/users                (Status: 301) [Size: 318] [--> http://10.130.177.50/api/users/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
root@ip-10-130-70-238:~# 

Bardzo dobrze. To jest **ważny przełom**. Mamy kolejny element układanki.

Wynik:

```
/api/auth/       301
/api/users/      301
/api/index.php  200 (2 bytes)
```

Analiza:

## 1. `/api/index.php`

Rozmiar:

```
2 bytes
```

Czyli prawdopodobnie coś typu:

```
{}
```

albo pusty response.

Nie jest teraz priorytetem.

---

## 2. `/api/auth/`

Bardzo interesujące.

Mamy już:

```
/auth.php
```

oraz:

```
/api/auth/
```

To może być miejsce związane z:

- logowaniem,
- tokenami,
- sesją,
- resetem hasła.

---

## 3. `/api/users/`

To jest najbardziej interesujące.

Dlaczego?

Pamiętaj pytania:

> flag found in admin user's profile notes

Czyli istnieje jakiś **profil użytkownika**.

Endpoint nazwany `/users/` może być związany z:

- pobieraniem użytkowników,
- profilami,
- danymi kont.

---

Teraz nie zgadujemy. Sprawdzamy zachowanie.

# KROK 10 — Sprawdź `/api/users/`

Wykonaj:

```
curl http://10.130.177.50/api/users/
```

Chcemy zobaczyć:

- czy zwraca listę użytkowników,
- czy wymaga autoryzacji,
- czy jest błąd.

---

Potem zrobimy to samo z:

```
curl http://10.130.177.50/api/auth/
```

ale **najpierw tylko users**.

Wklej wynik.

root@ip-10-130-70-238:~# curl http://10.130.177.50/api/users/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /api/users</title>
 </head>
 <body>
<h1>Index of /api/users</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/api/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="profile.php">profile.php</a></td><td align="right">2026-04-29 10:16  </td><td align="right">601 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.58 (Ubuntu) Server at 10.130.177.50 Port 80</address>
</body></html>

Bardzo dobrze. To jest **bardzo cenna obserwacja**. Zatrzymujemy się tutaj i analizujemy.

Mamy:

```
/api/users/
```

i odpowiedź:

```
Index of /api/users

profile.php
```

### Nowe evidence:

1. **Directory listing jest włączony**

Apache pokazuje zawartość katalogu:

```
/api/users/
```

To samo w sobie jest błędem konfiguracji.

2. Znaleźliśmy:

```
/api/users/profile.php
```

I nazwa jest bardzo ciekawa.

Pytanie CTF:

> "What is the flag found in the admin user's profile notes?"

Czyli istnieje koncepcja:

```
user -> profile -> notes
```

A my właśnie znaleźliśmy endpoint `profile.php`.

---

Nie otwieramy jeszcze przypadkowo. Najpierw sprawdzamy, **jak działa endpoint**.

# KROK 11 — Sprawdzenie profile.php

Wykonaj:

```
curl http://10.130.177.50/api/users/profile.php
```

Chcemy zobaczyć:

- czy zwraca błąd,
- czy wymaga parametru,
- czy pokazuje dane domyślne,
- czy oczekuje ID/user.

---

Mała lekcja pentestowa:

Mamy już klasyczny łańcuch:

```
Information Disclosure
        ↓
User Enumeration
        ↓
API Discovery
        ↓
Potential IDOR / Broken Access Control
```

Ale jeszcze nie zakładamy IDOR — musimy zobaczyć zachowanie endpointu.

Wykonaj tylko:

```
curl http://10.130.177.50/api/users/profile.php
```

i wklej wynik.

Dobrze. To jest ciekawy wynik, bo **cisza też jest informacją**.

Wykonaliśmy:

```
curl http://10.130.177.50/api/users/profile.php
```

i dostaliśmy:

```
(brak odpowiedzi)
```

Czyli:

- plik istnieje,
- Apache go wykonuje,
- ale bez odpowiednich parametrów nic nie zwraca.

To sugeruje, że `profile.php` prawdopodobnie oczekuje czegoś w request:

- parametru GET,
- parametru POST,
- nagłówka,
- ciasteczka/sesji.

Nie zgadujemy. Musimy zobaczyć kodowanie zachowania endpointu.

---

# KROK 12 — Sprawdźmy metodę GET z parametrem

Najpierw najprostsza hipoteza:

```
profile.php?username=
```

Dlaczego?

Bo wcześniej wszędzie aplikacja operowała na:

```
username
```

- login:
    
    ```
    username + password
    ```
    
- reset:
    
    ```
    username
    ```
    
- profile:
    
    ```
    username
    ```

Wykonaj:

```
curl "http://10.130.177.50/api/users/profile.php?username=laura.hayes"
```

Nie testujemy jeszcze admina ani exploitów.

Chcemy zobaczyć tylko:

**czy endpoint reaguje na parametr username.**

Wklej wynik.

Dobrze. To jest kolejna cenna obserwacja.

Wykonaliśmy:

```
curl "http://10.130.177.50/api/users/profile.php?username=laura.hayes"
```

i nadal:

```
(brak odpowiedzi)
```

Czyli nasza pierwsza hipoteza:

> `profile.php` przyjmuje `username` jako parametr GET

nie potwierdziła się.

Teraz nie strzelamy parametrami losowo. Musimy zebrać więcej informacji.

Przypomnijmy:

Gobuster znalazł:

```
/api/auth/
/api/users/
```

A `/api/users/` miał **directory listing**, więc warto sprawdzić, czy inne katalogi też coś pokazują.

Ale zanim pójdziemy dalej — mamy jeszcze jeden bardzo ważny trop:

```
/auth.php
```

znaleziony wcześniej.

Nazwa `auth.php` często oznacza:

- logowanie,
- sesję,
- walidację tokenu.

A `profile.php` może wymagać aktywnej sesji.

---

# KROK 13 — Sprawdzamy auth API

Wykonaj:

```
curl http://10.130.177.50/api/auth/
```

oraz:

```
curl http://10.130.177.50/api/auth/
```

(ten sam endpoint, pierwszy wystarczy 😉)

Chcemy zobaczyć:

- czy katalog jest pusty,
- czy jest listing,
- czy są pliki typu:
    - login.php
    - check.php
    - token.php

---

Na tym etapie nasz model wygląda tak:

```
/index.php
     |
     +--> /auth.php
     |
     +--> /forgot.php
              |
              +--> username enumeration

/api/
     |
     +--> /auth/
     |
     +--> /users/
              |
              +--> profile.php
```

Teraz sprawdzamy drugi element API.

Wklej wynik:

```
curl http://10.130.177.50/api/auth/
```

i idziemy dalej.

root@ip-10-130-70-238:~# curl http://10.130.177.50/api/auth/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /api/auth</title>
 </head>
 <body>
<h1>Index of /api/auth</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/api/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="token.php">token.php</a></td><td align="right">2026-04-29 10:16  </td><td align="right">386 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.58 (Ubuntu) Server at 10.130.177.50 Port 80</address>
</body></html>

Świetnie. To jest kolejny bardzo mocny punkt. Znowu nie skaczemy dalej — analizujemy.

Mamy teraz:

```
/api/auth/

token.php
```

Czyli struktura API wygląda:

```
/api/
 ├── auth/
 │    └── token.php
 │
 └── users/
      └── profile.php
```

To zaczyna wyglądać jak klasyczna aplikacja z:

```
login
  |
  v
token
  |
  v
profile
```

Czyli możliwy przepływ:

```
username + password
        |
        v
/api/auth/token.php
        |
        v
token/session
        |
        v
/api/users/profile.php
```

I to bardzo pasuje do pytania:

> flag found in admin user's profile notes

Bo żeby zobaczyć profil admina, prawdopodobnie potrzebujemy poprawnego tokena.

---

Teraz sprawdzamy **token endpoint**.

Nie zakładamy jeszcze metody. Najpierw zwykły GET.

# KROK 14 — Sprawdzenie token.php

Wykonaj:

```
curl http://10.130.177.50/api/auth/token.php
```

Chcemy zobaczyć:

- czy zwraca błąd,
- czy mówi czego brakuje,
- czy zwraca jakiś token,
- czy wymaga POST.

---

Dodatkowo zauważ jedną rzecz:

Apache pozwolił nam oglądać katalogi:

```
/api/auth/
```

i:

```
/api/users/
```

To jest już osobny finding:

> Directory Listing Enabled

Ale na razie traktujemy go jako **pomoc w mapowaniu aplikacji**, nie jako główny exploit.

Wykonaj tylko:

```
curl http://10.130.177.50/api/auth/token.php
```

i wklej wynik.

Dobrze. Kolejna obserwacja.

Wykonaliśmy:

```
curl http://10.130.177.50/api/auth/token.php
```

wynik:

```
(brak odpowiedzi)
```

Czyli podobnie jak `profile.php`:

- plik istnieje,
- GET bez parametrów nic nie zwraca,
- prawdopodobnie oczekuje **POST**.

Teraz mamy dwa endpointy, które milczą:

```
/api/auth/token.php
/api/users/profile.php
```

To jest bardzo typowy wzorzec:

```
POST credentials
        |
        v
 token.php
        |
        v
 Authorization token
        |
        v
 profile.php
```

---

# KROK 15 — Sprawdzamy wymagania token.php

Najpierw nie zgadujemy parametrów. Robimy prosty test POST.

Wykonaj:

```
curl -X POST http://10.130.177.50/api/auth/token.php
```

Chcemy zobaczyć, czy aplikacja powie np.:

- "missing username"
- "missing password"
- "invalid request"
- albo dalej będzie cicho.

To jest technika, którą warto zapamiętać:

> pusty GET → test pustego POST → obserwujemy komunikat błędu → dopiero potem budujemy request.

Wklej wynik tego jednego polecenia.

Dobrze. Wynik jest taki sam:

```
POST /api/auth/token.php

(brak odpowiedzi)
```

To jest informacja sama w sobie.

Aktualny model:

```
/api/auth/token.php
        |
        |  GET  -> cisza
        |  POST -> cisza
        |
        ??? 
```

Czyli endpoint prawdopodobnie **nie reaguje na pusty request**, ale nie wiemy jeszcze, czego oczekuje.

Teraz robimy kolejny logiczny krok: sprawdzamy, czy aplikacja używa **JSON API**.

Wiele prostych aplikacji PHP ma np.:

```
{
  "username":"...",
  "password":"..."
}
```

a nie klasyczny formularz.

---

# KROK 16 — Test pustego JSON POST

Wykonaj:

```
curl -X POST http://10.130.177.50/api/auth/token.php \
-H "Content-Type: application/json" \
-d '{}'
```

Patrzymy, czy pojawi się jakikolwiek komunikat typu:

- missing field,
- invalid JSON,
- unauthorized,
- error.

---

Dlaczego teraz?

Bo mamy już kilka wskazówek:

- `/index.php` używa klasycznego POST:
    
    ```
    username=password
    ```
    
- ale `/api/` wygląda jak osobna warstwa aplikacji
- endpoint nazywa się `token.php`, a nie `login.php`

Czyli bardzo możliwe, że API ma inny format.

Wykonaj tylko ten test i wklej wynik.

Dobrze. Mamy kolejny wynik:

```
POST /api/auth/token.php
Content-Type: application/json
{}
```

Odpowiedź:

```
(brak)
```

Czyli:

- endpoint istnieje,
- nie daje informacji o błędnym formacie,
- nie odpowiada na pusty JSON.

Teraz musimy zmienić podejście. Zamiast zgadywać parametry, wykorzystamy to, co już wiemy.

Mamy działający formularz logowania:

```
id="q8zj4d"
<form method="POST" action="/index.php">
username
password
```

I mamy osobny endpoint:

```
/auth.php
```

To wygląda na miejsce, gdzie aplikacja obsługuje logowanie.

---

# KROK 17 — Sprawdzamy auth.php

Wcześniej Gobuster pokazał:

```
/auth.php  (Status: 200) [Size: 0]
```

Czyli plik istnieje.

Teraz sprawdzamy, czy reaguje na POST.

Wykonaj:

```
curl -X POST http://10.130.177.50/auth.php
```

Jeżeli nadal będzie pusto, zrobimy następny krok: przechwycimy prawidłowy request logowania (np. przez Burpa albo curl) i zobaczymy, jak aplikacja naprawdę przesyła dane.

Na razie tylko ten test. Wklej wynik.

Dobrze. Mamy teraz pełniejszy obraz.

Wykonaliśmy:

```
POST /auth.php
```

wynik:

```
(brak odpowiedzi)
```

Czyli zarówno:

```
/auth.php
/api/auth/token.php
/api/users/profile.php
```

nie dają nic przy pustych requestach.

To jest normalne w CTF-ach — często endpointy są "ciche", dopóki nie dostaną **dokładnie oczekiwanych parametrów**.

---

Teraz wracamy do najważniejszej rzeczy, którą mamy:

**działający login w HTML.**

Formularz:

```
<form method="POST" action="/index.php">
```

Czyli prawdziwa logika logowania może siedzieć w `index.php`, nie w `auth.php`.

Musimy zobaczyć, co się stanie przy próbie logowania.

Nie będziemy brute force. Zrobimy jeden kontrolowany test.

---

# KROK 18 — Test logowania z fałszywymi danymi

Wykonaj:

```
curl -X POST http://10.130.177.50/index.php \
-d "username=test&password=test"
```

Chcemy zobaczyć:

- czy jest komunikat błędu,
- czy jest redirect,
- czy tworzy cookie,
- czy odpowiedź różni się od zwykłego GET.

Potem porównamy zachowanie.

---

Mała uwaga pentesterska:

Do tej pory odkryliśmy:

```
80/tcp
 |
 +-- login
 |
 +-- forgot password
 |      |
 |      +-- username enumeration
 |
 +-- API
        |
        +-- auth/token
        +-- users/profile
```

Teraz próbujemy wejść w **normalny przepływ aplikacji**, zamiast zgadywać endpointy.

Wklej wynik tego POST-a.

root@ip-10-130-70-238:~# curl -X POST http://10.130.177.50/index.php \
-d "username=test&password=test"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
  <div class="alert alert-danger">Invalid credentials</div>  <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Bardzo dobrze. To jest ważny krok, bo teraz potwierdziliśmy **zachowanie prawdziwego mechanizmu logowania**.

Mamy:

Request:

```
POST /index.php

username=test
password=test
```

Response:

```
<div class="alert alert-danger">Invalid credentials</div>
```

Czyli:

- logowanie działa,
- aplikacja rozróżnia błędne dane,
- nie ma tutaj prostego "fail open".

---

Teraz łączymy fakty:

### Co już wiemy:

```
/team.php
    |
    +--> ujawnia użytkowników

/forgot.php
    |
    +--> potwierdza istniejące konta

/index.php
    |
    +--> sprawdza login
```

Mamy listę potencjalnych użytkowników:

```
laura.hayes
michael.chen
sarah.johnson
robert.wilson
emma.taylor
david.brown
james.wright
```

Ale nie mamy haseł.

---

Teraz naturalny następny krok to sprawdzić, czy **reset hasła faktycznie zmienia coś albo ujawnia dane**.

Przypomnij:

dla:

```
username=laura.hayes
```

dostaliśmy:

```
Password reset instructions have been sent to la****@nexus.corp
```

Czyli aplikacja twierdzi, że wysłała instrukcję.

W CTF-ach bardzo często "mail" jest zastąpiony:

- plikiem,
- logiem,
- endpointem,
- tokenem.

---

# KROK 19 — Sprawdzamy katalog backup

Mamy jeszcze jedno znalezisko z Gobustera:

```
/backup/
```

I teraz jest dobry moment, żeby go sprawdzić, bo:

- aplikacja ma reset haseł,
- mamy config.php,
- mamy API,
- mamy możliwe sekrety.

Wykonaj:

```
curl http://10.130.177.50/backup/
```

Nie pobieramy jeszcze niczego ręcznie.

Chcemy zobaczyć, czy katalog ma listing jak `/api/`.

Wklej wynik.

oot@ip-10-130-70-238:~# curl http://10.130.177.50/backup/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /backup</title>
 </head>
 <body>
<h1>Index of /backup</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="README.txt">README.txt</a></td><td align="right">2026-04-29 10:18  </td><td align="right">191 </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="config.enc">config.enc</a></td><td align="right">2026-05-09 16:57  </td><td align="right">112 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.58 (Ubuntu) Server at 10.130.177.50 Port 80</address>
</body></html>
root@ip-10-130-70-238:~# 

Bardzo dobrze. To jest **bardzo mocny punkt**. Znalazłeś coś, co prawdopodobnie będzie częścią łańcucha ataku.

Mamy:

```
/backup/
 |
 +-- README.txt
 |
 +-- config.enc
```

I znowu widzimy ten sam błąd:

> **Directory Listing Enabled**

Ale ważniejsze jest:

```
config.enc
```

Nazwa sugeruje:

- `config` → konfiguracja aplikacji
- `.enc` → zaszyfrowane dane

Czyli potencjalnie:

- klucze,
- hasła,
- sekrety,
- konfiguracja bazy,
- secret key do tokenów.

To bardzo pasuje do wcześniejszych znalezisk:

```
/config.php
/api/auth/token.php
```

Możliwy łańcuch:

```
backup/config.enc
        |
        v
sekret aplikacji
        |
        v
token/auth
        |
        v
admin profile
```

---

Ale zanim dotykamy szyfrowania, sprawdzamy README.

Dlaczego?

Bo w pentestach najpierw czytamy **metadane**, zanim zaczniemy łamać rzeczy.

# KROK 20 — Pobierz README

Wykonaj:

```
curl http://10.130.177.50/backup/README.txt
```

Nie pobieraj jeszcze `config.enc`.

Chcemy najpierw zobaczyć, czy autor zostawił:

- informację o szyfrowaniu,
- hasło,
- nazwę algorytmu,
- wskazówkę.

---

Aktualny stan (bardzo ładnie się układa):

```
Recon
 |
 +-- HTTP
      |
      +-- team.php
      |      |
      |      +-- usernames
      |
      +-- forgot.php
      |      |
      |      +-- username enumeration
      |
      +-- api/
      |      |
      |      +-- auth/token.php
      |      +-- users/profile.php
      |
      +-- backup/
             |
             +-- config.enc  <--- potencjalny sekret
```

Wykonaj tylko:

```
curl http://10.130.177.50/backup/README.txt
```

i wklej wynik.

0-238:~# curl http://10.130.177.50/backup/README.txt
NexusCorp Backup Configuration
================================
config.enc  - Encrypted application configuration (AES-128-ECB)
Decryption key reference: see static/app.js (deployment notes)
root@ip-10-130-70-238:~# 

Świetnie. To jest **bardzo konkretna wskazówka**. Teraz mamy już prawie pewny kierunek.

README mówi:

```
NexusCorp Backup Configuration
================================
config.enc  - Encrypted application configuration (AES-128-ECB)
Decryption key reference: see static/app.js (deployment notes)
```

### Analiza

Mamy:

```
backup/config.enc
        |
        v
AES-128-ECB
        |
        v
klucz znajduje się w:
static/app.js
```

Czyli nie musimy łamać AES-a. Klucz został prawdopodobnie zostawiony w pliku frontendu.

To jest klasyczny błąd:

> Sensitive information disclosure in client-side JavaScript

Łańcuch wygląda teraz:

```
Directory Listing
        |
        v
README.txt
        |
        v
informacja o szyfrowaniu
        |
        v
static/app.js
        |
        v
key
        |
        v
decrypt config.enc
```

---

# KROK 21 — Sprawdzamy static/app.js

Najpierw pobieramy plik:

```
curl http://10.130.177.50/static/app.js
```

Szukamy:

- klucza AES,
- deployment notes,
- sekretów,
- zmiennych typu:
    - `KEY`
    - `SECRET`
    - `CONFIG_KEY`

Nie robimy jeszcze decrypt.

---

Wklej cały wynik `curl`.

Jeżeli będzie dużo JS-a, możesz też zrobić:

```
curl -s http://10.130.177.50/static/app.js | grep -i -E "key|secret|aes|config"
```

Ale najpierw wolę zobaczyć pełny kontekst.

Wykonaj:

```
curl http://10.130.177.50/static/app.js
```

i wklej wynik.

root@ip-10-130-70-238:~# curl http://10.130.177.50/static/app.js
Warning: Binary output can mess up your terminal. Use "--output -" to tell 
Warning: curl to output it to your terminal anyway, or consider "--output 
Warning: <FILE>" to save to a file.
root@ip-10-130-70-238:~# curl -s http://10.130.177.50/static/app.js | grep -i -E "key|secret|aes|config"
grep: (standard input): binary file matches
root@ip-10-130-70-238:~# 

Bardzo dobrze. I tutaj mamy ciekawy moment diagnostyczny.

Dostaliśmy:

```
curl http://10.130.177.50/static/app.js
```

oraz:

```
Warning: Binary output can mess up your terminal
```

To oznacza, że **app.js nie jest zwykłym tekstowym JavaScriptem** albo odpowiedź zawiera znaki binarne.

To samo potwierdza:

```
grep -i -E "key|secret|aes|config"
```

wynik:

```
grep: (standard input): binary file matches
```

Czyli coś tam jest, ale grep nie analizuje tego jako tekst.

Nie walczymy z terminalem — zapisujemy plik i sprawdzamy go normalnymi narzędziami.

---

# KROK 22 — Zapisz app.js lokalnie

Wykonaj:

```
curl -s http://10.130.177.50/static/app.js -o app.js
```

Potem sprawdź typ pliku:

```
file app.js
```

I następnie:

```
strings app.js | grep -i -E "key|secret|aes|config"
```

---

Dlaczego `strings`?

Bo jeśli plik jest:

- skompresowany,
- zawiera obiekty binarne,
- ma zaszyte dane,

to `strings` wyciągnie czytelne fragmenty ASCII.

W pentestach bardzo często robimy:

```
binary
  |
  v
strings
  |
  v
interesting secrets
```

---

Wykonaj te trzy komendy:

```
curl -s http://10.130.177.50/static/app.js -o app.js
file app.js
strings app.js | grep -i -E "key|secret|aes|config"
```

Wklej wynik. To prawdopodobnie będzie kolejna cegiełka do odszyfrowania `config.en`

root@ip-10-130-70-238:~# curl -s http://10.130.177.50/static/app.js -o app.js
root@ip-10-130-70-238:~# file app.js
app.js: data
root@ip-10-130-70-238:~# strings app.js | grep -i -E "key|secret|aes|config"
    // Configuration (TODO: move to env before prod deployment - laura 2024-10-22)
    const CONFIG = {
        // Encryption key for backup config decryption - AES-ECB-128
        // Key: N3xusK3y2024!!  (pad to 16 bytes with 
        _backupKey: 'N3xusK3y2024!!',
root@ip-10-130-70-238:~# 

Bardzo dobrze. To jest **pierwszy realny sekret**, który znaleźliśmy. Zatrzymajmy się i zapiszmy finding.

Mamy:

```
README.txt
        |
        v
AES-128-ECB
        |
        v
klucz w static/app.js
```

A teraz:

```
strings app.js | grep -i -E "key|secret|aes|config"
```

zwróciło:

```
// Encryption key for backup config decryption - AES-ECB-128
// Key: N3xusK3y2024!!  (pad to 16 bytes with 
_backupKey: 'N3xusK3y2024!!',
```

Czyli:

**AES-128-ECB key:**

```
N3xusK3y2024!!
```

---

### Co właśnie odkryliśmy?

To jest klasyczna podatność:

> Hardcoded cryptographic key in client-side asset

Łańcuch:

```
Directory Listing
        |
        v
README.txt
        |
        v
AES-ECB info
        |
        v
static/app.js
        |
        v
hardcoded key
        |
        v
decrypt config.enc
```

---

Teraz mamy klucz, ale potrzebujemy jeszcze samego pliku.

# KROK 23 — Pobieramy config.enc

Wykonaj:

```
curl -s http://10.130.177.50/backup/config.enc -o config.enc
```

Potem sprawdź:

```
file config.enc
```

oraz:

```
xxd config.enc | head
```

---

Dlaczego `xxd`?

Bo zanim odszyfrujemy, chcemy zobaczyć:

- czy to faktycznie ciphertext,
- czy długość pasuje do AES block size (16 bajtów).

AES-ECB działa na blokach 16 bajtów, więc rozmiar powinien być wielokrotnością 16.

---

Na razie **nie próbuj decryptować**. Najpierw potwierdzamy materiał wejściowy.

Wklej wynik:

```
file config.enc
xxd config.enc | head
```

Potem przejdziemy do odszyfrowania.

root@ip-10-130-70-238:~# curl -s http://10.130.177.50/backup/config.enc -o config.enc
root@ip-10-130-70-238:~# file config.enc
config.enc: data
root@ip-10-130-70-238:~# xxd config.enc | head
00000000: 31cd 75de 345d 4019 4b60 bea5 c4db a6f1  1.u.4]@.K`......
00000010: 93e5 71cb 8c03 22d5 108a b67f 7e50 73ba  ..q...".....~Ps.
00000020: 7387 c869 b6c9 aec7 dd28 dc8b f001 9fa9  s..i.....(......
00000030: b850 4bbd 4779 0f5e e968 c416 d2b2 412d  .PK.Gy.^.h....A-
00000040: 5c95 9976 74ed f0bb 6285 d92f d7b0 01d0  \..vt...b../....
00000050: 3157 6dbf 5aa4 2541 bed9 1276 8789 8e36  1Wm.Z.%A...v...6
00000060: 2b64 d315 4fc8 7d61 0c9c dcf1 8993 6994  +d..O.}a......i.
root@ip-10-130-70-238:~# 

Bardzo dobrze. Mamy komplet do kolejnego etapu.

Podsumujmy evidence:

```
/backup/config.enc
```

jest rzeczywiście binarnym ciphertextem:

```
00000000: 31cd 75de 345d 4019 ...
```

Rozmiar z `xxd` wygląda sensownie — dane są blokowe, a README powiedział:

```
AES-128-ECB
```

Mamy też klucz:

```
N3xusK3y2024!!
```

Czyli teraz wykonujemy **kontrolowane odszyfrowanie**.

---

# KROK 24 — Dekryptujemy config.enc

Użyjemy OpenSSL.

AES-128-ECB wymaga klucza 16 bajtów.

Nasz klucz:

```
N3xusK3y2024!!
```

ma 14 znaków, więc zgodnie z komentarzem w JS:

```
pad to 16 bytes
```

dopadujemy dwoma bajtami.

Wykonaj:

```
printf 'N3xusK3y2024!!00' | xxd -p
```

To pokaże nam hex klucza.

Potem:

```
openssl enc -d -aes-128-ecb \
-K <HEX_KEY> \
-in config.enc \
-out config.dec
```

I sprawdzamy:

```
cat config.dec
```

---

Ale zanim wpiszesz — mała uwaga.

W OpenSSL czasami trzeba dodać:

```
-nopad
```

bo AES-ECB w takich CTF-ach często nie używa standardowego paddingu.

Jeżeli pierwszy wariant da błąd typu:

```
bad decrypt
```

to spróbujemy drugi.

---

Wykonaj teraz tylko:

```
printf 'N3xusK3y2024!!00' | xxd -p
```

Wklej wynik, a ja podam Ci dokładną komendę decrypt (żebyśmy nie pomylili hex key).

oot@ip-10-130-70-238:~# openssl enc -d -aes-128-ecb \
-K 4e337875734b33793230323421213030 \
-nopad \
-in config.enc \
-out config.dec
root@ip-10-130-70-238:~# cat config.dec
��M*a����%�2Y!�Xd
���4�<��u��f     �����ㄪ
            Be��+�	@
                         �}?��&�L?��l�!֮.�h���Um���9�EI�v�e!~D��t��Uv�>root@ip-10-130-70-238:~# 

Dobrze, zrobiłeś poprawny test. Teraz mamy **ważną informację diagnostyczną**.

Odszyfrowanie wykonało się bez błędu:

```
openssl enc -d -aes-128-ecb ...
```

ale wynik:

```
��M*a����%�2Y!�Xd
...
```

jest **losowym binarnym śmieciem**.

To oznacza, że jeden z elementów jest niepoprawny:

1. ❌ klucz nie jest dokładnie taki,
2. ❌ padding jest niepoprawny,
3. ❌ plik nie jest szyfrowany dokładnie tym wariantem,
4. ❌ komentarz w JS zawiera tylko fragment, a nie pełny sekret.

Nie zakładamy porażki — właśnie znaleźliśmy punkt, gdzie trzeba zweryfikować.

---

## KROK 25 — Sprawdzamy dokładną długość klucza

W `app.js` mieliśmy:

```
_backupKey: 'N3xusK3y2024!!'
```

My dopisaliśmy:

```
00
```

ale musimy sprawdzić, czy to na pewno jest sposób paddingu.

Najpierw policzmy długość:

```
echo -n 'N3xusK3y2024!!' | wc -c
```

Potem:

```
echo -n 'N3xusK3y2024!!' | xxd -p
```

---

Dlaczego?

AES-128 wymaga:

```
16 bytes = 128 bits
```

Jeżeli klucz ma np. 15 znaków, to dopisanie `0` ASCII będzie inne niż dopisanie bajta `0x00`.

Możliwe warianty:

### ASCII padding:

```
N3xusK3y2024!!00
```

hex:

```
4e337875734b33793230323421213030
```

### NULL padding:

```
N3xusK3y2024!!\x00\x00
```

hex byłby:

```
4e337875734b33793230323421210000
```

To jest inny klucz.

---

Wykonaj teraz:

```
echo -n 'N3xusK3y2024!!' | wc -c
```

i:

```
echo -n 'N3xusK3y2024!!' | xxd -p
```

Wklej wynik.

Nie idziemy jeszcze w zgadywanie — najpierw potwierdzamy materiał.

Dobrze. Mamy potwierdzenie:

```
N3xusK3y2024!!
```

ma:

```
14 bajtów
```

hex:

```
4e337875734b3379323032342121
```

Czyli mój poprzedni wariant:

```
N3xusK3y2024!!00
```

był tylko hipotezą i najpewniej był błędny.

Komentarz w `app.js` mówił:

```
// Key: N3xusK3y2024!!  (pad to 16 bytes with ...)
```

ale wynik jest ucięty przez `strings`. Musimy sprawdzić **co było po "with"**.

---

# KROK 26 — Wyciągamy pełny fragment z app.js

`strings` pokazał tylko kawałek. Teraz zobaczymy więcej kontekstu.

Wykonaj:

```
strings app.js | grep -A5 -B5 "N3xusK3y2024"
```

Parametry:

- `-B5` → 5 linii przed
- `-A5` → 5 linii po

Szukamy dokładnej instrukcji:

```
pad to 16 bytes with ...
```

---

Dlaczego?

Bo mamy dwie możliwości:

### ASCII padding

np.

```
N3xusK3y2024!!00
```

czyli:

```
30 30
```

### NULL padding

np.

```
N3xusK3y2024!!\x00\x00
```

czyli:

```
00 00
```

A AES wymaga **dokładnie 16 bajtów** — jeden bajt różnicy daje kompletnie losowy wynik.

---

Wykonaj tylko:

```
strings app.js | grep -A5 -B5 "N3xusK3y2024"
```

i wklej wynik.

oot@ip-10-130-70-238:~# strings app.js | grep -A5 -B5 "N3xusK3y2024"
    'use strict';
    // Configuration (TODO: move to env before prod deployment - laura 2024-10-22)
    const CONFIG = {
        apiBase: '/api',
        // Encryption key for backup config decryption - AES-ECB-128
        // Key: N3xusK3y2024!!  (pad to 16 bytes with 
        _backupKey: 'N3xusK3y2024!!',
        appVersion: '2.3.1'
    };
    // Session helper
    window.NexusApp = {
        getSession: function() {
root@ip-10-130-70-238:~# 

Dobrze. Mamy teraz pełny kontekst. I to jest ciekawa sytuacja — komentarz został **ucięty**, więc nie dostaliśmy informacji po:

```
// Key: N3xusK3y2024!!  (pad to 16 bytes with
```

Nie wiemy, czym dopadują.

Ale mamy kilka możliwych sposobów i zamiast zgadywać losowo, zrobimy to metodycznie.

Aktualnie mamy:

```
Key (14 bytes):
N3xusK3y2024!!

Hex:
4e337875734b3379323032342121
```

Brakuje:

```
2 bytes
```

Najbardziej prawdopodobne warianty:

1. **NULL bytes**:

```
4e337875734b33793230323421210000
```

2. **spacje ASCII**:

```
4e337875734b33793230323421212020
```

3. **zera ASCII**:

```
4e337875734b33793230323421213030
```

My już sprawdziliśmy wariant 3 i wyszły śmieci.

---

# KROK 27 — Testujemy NULL padding

Wykonaj:

```
openssl enc -d -aes-128-ecb \
-K 4e337875734b33793230323421210000 \
-nopad \
-in config.enc \
-out config.dec
```

Potem:

```
cat config.dec
```

---

Jeżeli nadal będą krzaki, sprawdzimy wariant ze spacjami.

Dlaczego zaczynam od NULL?

Bo komentarz:

```
pad to 16 bytes
```

w kontekście kluczy AES najczęściej oznacza właśnie dopełnienie zerami, a nie znakami `'0'`.

Wykonaj tylko ten wariant i wklej wynik.

oot@ip-10-130-70-238:~# openssl enc -d -aes-128-ecb \
-K 4e337875734b33793230323421210000 \
-nopad \
-in config.enc \
-out config.dec
root@ip-10-130-70-238:~# cat config.dec
{"app_name":"NexusCorp Portal","version":"2.3.1","deploy_env":"production","system_user":"devops"}root@ip-10-130-70-238:~# 

Świetnie. To jest **duży przełom**. Zrobiłeś właśnie pełny łańcuch exploitacyjny bez gotowca. Zapisujemy finding.

Mamy odszyfrowany:

```
{
  "app_name":"NexusCorp Portal",
  "version":"2.3.1",
  "deploy_env":"production",
  "system_user":"devops"
}
```

## Co to nam mówi?

Pierwsze ważne rzeczy:

### 1. Potwierdzony użytkownik systemowy

```
"system_user":"devops"
```

To jest bezpośredni trop do pytania:

> What is the flag found in the **devops** user's home directory?

Czyli istnieje użytkownik Linux:

```
devops
```

---

### 2. Mamy już potencjalną ścieżkę:

Aktualnie:

```
backup/config.enc
        |
        v
devops user clue
        |
        v
?
```

Ale nadal nie mamy:

- hasła devops,
- dostępu SSH,
- tokena,
- admina.

---

Zauważ jeszcze jedną rzecz:

Wcześniej znaleźliśmy:

```
/api/auth/token.php
/api/users/profile.php
```

A teraz mamy sekret aplikacji i konfigurację.

Możliwe, że config nie zawiera wszystkiego — ale potwierdza, że aplikacja ma wiedzę o użytkownikach systemowych.

---

Teraz wracamy do naszego głównego celu:

> zdobyć flagę admin profile notes

Do tego prawdopodobnie potrzebujemy dostać się do aplikacji jako użytkownik.

Mamy już:

- username enumeration,
- listę kont,
- reset password endpoint,
- API.

Najbardziej logiczny następny krok:

sprawdzić **jak aplikacja generuje token**.

---

# KROK 28 — Sprawdzamy zawartość `api/auth/token.php` poprzez metodę OPTIONS

Czasem endpoint zdradza obsługiwane metody.

Wykonaj:

```
curl -i -X OPTIONS http://10.130.177.50/api/auth/token.php
```

Szukamy nagłówka:

```
Allow:
```

albo informacji o metodach.

---

Dlaczego teraz?

Bo mamy endpoint tokenów, ale nie wiemy:

- POST z form-data?
- POST JSON?
- GET z parametrem?
- Basic auth?
- coś jeszcze?

Nie zgadujemy — pytamy serwer.

Wykonaj tylko:

```
curl -i -X OPTIONS http://10.130.177.50/api/auth/token.php
```

i wklej wynik.

root@ip-10-130-70-238:~# curl -i -X OPTIONS http://10.130.177.50/api/auth/token.phpapi/auth/token.p
HTTP/1.1 302 Found
Date: Sat, 05 Sep 2026 12:41:04 GMT
Server: Apache/2.4.58 (Ubuntu)
Location: /index.php
Content-Length: 0
Content-Type: application/json

root@ip-10-130-70-238:~# curl -i -X OPTIONS http://10.130.177.50/api/auth/token.php
HTTP/1.1 302 Found
Date: Sat, 05 Sep 2026 12:41:22 GMT
Server: Apache/2.4.58 (Ubuntu)
Location: /index.php
Content-Length: 0
Content-Type: application/json

Dobrze. I tutaj mamy bardzo ciekawą obserwację.

Wykonałeś:

```
curl -i -X OPTIONS http://10.130.177.50/api/auth/token.php
```

Odpowiedź:

```
HTTP/1.1 302 Found
Location: /index.php
Content-Type: application/json
```

### Co to oznacza?

Endpoint:

```
/api/auth/token.php
```

nie jest dostępny bez odpowiedniego kontekstu.

Zamiast odpowiedzi API dostajemy:

```
/api/auth/token.php
        |
        v
   redirect
        |
        v
/index.php
```

To jest bardzo ważna wskazówka:

**token.php prawdopodobnie wymaga aktywnej sesji albo określonego sposobu wywołania.**

Nie wygląda na publiczny endpoint.

---

Teraz przypominamy sobie coś ważnego:

Przy zwykłym loginie:

```
curl -X POST http://10.130.177.50/index.php \
-d "username=test&password=test"
```

dostaliśmy:

```
Invalid credentials
```

Czyli login działa.

Musimy zobaczyć, co dzieje się przy **poprawnym użytkowniku z błędnym hasłem**.

To pozwoli nam sprawdzić, czy:

- logowanie tworzy sesję,
- odpowiedź różni się dla użytkownika istniejącego.

---

# KROK 29 — Test istniejącego użytkownika

Weźmy użytkownika, którego już potwierdziliśmy:

```
laura.hayes
```

Wykonaj:

```
curl -i -X POST http://10.130.177.50/index.php \
-d "username=laura.hayes&password=test"
```

Używamy `-i`, bo interesują nas nagłówki.

Szukamy np.:

```
Set-Cookie:
```

albo:

```
Location:
```

---

Dlaczego teraz?

Bo jeśli aplikacja ujawnia różnicę między:

```
nieistniejący user
```

a:

```
istniejący user + złe hasło
```

to mamy kolejny element.

Wykonaj tylko ten request i wklej pełny wynik.

oot@ip-10-130-70-238:~# curl -i -X POST http://10.130.177.50/index.php \
-d "username=laura.hayes&password=test"
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 12:43:01 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 918
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
  <div class="alert alert-danger">Invalid credentials</div>  <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>

Dobrze. Mamy kolejny kawałek układanki.

Wynik:

```
HTTP/1.1 200 OK
```

i:

```
<div class="alert alert-danger">Invalid credentials</div>
```

### Wniosek

Dla:

```
laura.hayes + złe hasło
```

aplikacja zachowuje się tak samo jak:

```
test + złe hasło
```

czyli:

- nie mamy kolejnego wycieku przez login,
- nie ma `Set-Cookie`,
- nie ma redirectu,
- nie tworzy sesji.

Czyli na ten moment:

```
username enumeration  ✅
password discovery    ❌
session after login   ❌
```

---

Teraz mamy ciekawszy trop.

Pamiętasz:

```
/api/auth/token.php
```

Po `OPTIONS` dostał:

```
302 Location: /index.php
```

To sugeruje, że endpoint sprawdza **sesję**.

Ale skąd bierze się sesja?

Prawdopodobnie z normalnego logowania.

Czyli musimy albo:

1. zdobyć prawidłowe hasło,
2. znaleźć błąd w logice auth,
3. znaleźć dane w backupie/configu.

---

Mamy jeszcze jeden nieprzeanalizowany element:

```
/auth.php
```

Gobuster pokazał:

```
/auth.php 200 size 0
```

Może być:

- include,
- backend logiki,
- plik obsługujący sesję.

Teraz sprawdzimy **czy istnieje kod źródłowy przez backup albo inne pliki**, ale najpierw najprostszy test.

---

# KROK 30 — Sprawdzamy `config.php`

Wcześniej Gobuster znalazł:

```
/config.php
```

Status:

```
200
size 0
```

Może być pusty, ale czasem PHP zwraca pustkę, bo wykonuje kod.

Sprawdźmy nagłówki:

```
curl -i http://10.130.177.50/config.php
```

Szukamy:

- redirectów,
- content-type,
- ciasteczek,
- nietypowych nagłówków.

---

Wykonaj tylko:

```
curl -i http://10.130.177.50/config.php
```

i wklej wynik.

oot@ip-10-130-70-238:~# curl -i http://10.130.177.50/config.php
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 12:45:08 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8

Dobrze. Mamy potwierdzenie kolejnego elementu.

Request:

```
curl -i http://10.130.177.50/config.php
```

Response:

```
HTTP/1.1 200 OK
Content-Length: 0
Content-Type: text/html; charset=UTF-8
```

### Wniosek

`config.php`:

- istnieje,
- wykonuje się,
- ale nie ujawnia treści.

Czyli najpewniej jest to plik typu:

```
<?php
// zmienne konfiguracyjne
?>
```

albo:

```
<?php
include(...);
?>
```

i Apache poprawnie interpretuje PHP.

Nie jest to teraz nasz punkt wejścia.

---

Zbierzmy obecny stan:

```
PORT 80
 |
 +-- index.php
 |      |
 |      +-- login
 |
 +-- forgot.php
 |      |
 |      +-- username enumeration
 |
 +-- team.php
 |      |
 |      +-- usernames
 |
 +-- backup/
 |      |
 |      +-- config.enc
 |             |
 |             +-- AES key z app.js
 |             |
 |             +-- devops clue
 |
 +-- api/
        |
        +-- auth/token.php
        |
        +-- users/profile.php
```

Mamy bardzo ważny brakujący element:

**nie wiemy, jak aplikacja tworzy token/sesję.**

---

Pamiętasz, że `api/auth/token.php` przy pustym requestcie dawał ciszę/redirect. Spróbujmy teraz podejść od drugiej strony: sprawdzić, czy aplikacja ma jakieś pliki źródłowe dostępne przez backup.

W katalogu `/backup/` mieliśmy:

```
README.txt
config.enc
```

ale Gobuster znalazł też:

```
/api/users/profile.php
```

oraz:

```
/api/auth/token.php
```

Może istnieją kopie `.bak`, `.old`, `.zip`.

---

# KROK 31 — Szukamy backupów aplikacji

Uruchom:

```
gobuster dir -u http://10.130.177.50 -w /usr/share/wordlists/dirb/common.txt -x php,bak,old,txt
```

Tym razem interesują nas **rozszerzenia**, bo często administratorzy zostawiają:

```
index.php.bak
auth.php.old
config.php.bak
```

Nie robimy jeszcze exploitacji — tylko sprawdzamy, czy kod nie wyciekł.

Wklej wynik.

oot@ip-10-130-70-238:~# gobuster dir -u http://10.130.177.50 -w /usr/share/wordlists/dirb/common.txt -x php,bak,old,txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.130.177.50
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,bak,old,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.hta.bak             (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.hta.php             (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.hta.txt             (Status: 403) [Size: 278]
/.hta.old             (Status: 403) [Size: 278]
/.htaccess.bak        (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.htaccess.old        (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.old        (Status: 403) [Size: 278]
/.htpasswd.bak        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/403.php              (Status: 200) [Size: 322]
/admin                (Status: 301) [Size: 314] [--> http://10.130.177.50/admin/]
/api                  (Status: 301) [Size: 312] [--> http://10.130.177.50/api/]
/auth.php             (Status: 200) [Size: 0]
/backup               (Status: 301) [Size: 315] [--> http://10.130.177.50/backup/]
/config.php           (Status: 200) [Size: 0]
/dashboard.php        (Status: 302) [Size: 0] [--> /index.php]
/forgot.php           (Status: 200) [Size: 684]
/index.php            (Status: 200) [Size: 861]
/index.php            (Status: 200) [Size: 861]
/javascript           (Status: 301) [Size: 319] [--> http://10.130.177.50/javascript/]
/logout.php           (Status: 302) [Size: 0] [--> /index.php]
/server-status        (Status: 403) [Size: 278]
/static               (Status: 301) [Size: 315] [--> http://10.130.177.50/static/]
/support              (Status: 301) [Size: 316] [--> http://10.130.177.50/support/]
/team.php             (Status: 200) [Size: 3747]
Progress: 23070 / 23075 (99.98%)
===============================================================
Finished
===============================================================
root@ip-10-130-70-238:~# 

Dobra robota. Ten krok był sensowny, ale wynik nam coś mówi.

Nie znaleźliśmy:

```
index.php.bak
auth.php.bak
config.php.old
```

czyli **nie mamy prostego wycieku kodu źródłowego**.

Natomiast pojawił się bardzo ciekawy katalog:

```
/admin
```

To jest prawdopodobnie kolejny etap, bo pytania CTF mówią:

> What is the flag displayed on the admin panel after gaining admin access?

Czyli admin panel istnieje i już go znaleźliśmy.

---

Aktualny model:

```
                 +-------------+
                 | login.php   |
                 +-------------+
                       |
                       v
                  auth logic
                       |
          +------------+------------+
          |                         |
          v                         v
     dashboard.php              admin/
```

`dashboard.php` robi:

```
302 -> /index.php
```

bo nie mamy sesji.

Ale teraz sprawdzimy `/admin/`.

---

# KROK 32 — Enumeracja admin panelu

Najpierw zwykły request:

```
curl -i http://10.130.177.50/admin/
```

Chcemy zobaczyć:

- redirect,
- komunikat,
- wymaganie sesji,
- nazwę pliku.

---

Potem (ale jeszcze nie teraz) zrobimy gobustera na `/admin`.

Na razie tylko:

```
curl -i http://10.130.177.50/admin/
```

Wklej wynik.

oot@ip-10-130-70-238:~# curl -i http://10.130.177.50/admin/
HTTP/1.1 403 Forbidden
Date: Sat, 05 Sep 2026 12:48:14 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 322
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html><head><title>403 - NexusCorp</title><link rel="stylesheet" href="/static/style.css"></head>
<body class="login-page">
<div class="login-box">
<h2>403 - Access Denied</h2>
<p>You do not have permission to access this resource.</p>
<a href="/dashboard.php">Return to Dashboard</a>
</div></body></html>
root@ip-10-130-70-238:~# 

Dobrze. To jest bardzo cenna odpowiedź.

Mamy:

```
HTTP/1.1 403 Forbidden
```

oraz:

```
You do not have permission to access this resource.
```

Czyli:

- katalog `/admin/` istnieje ✅
- nie jest to ukryty fake endpoint ✅
- kontrola dostępu działa po stronie aplikacji ✅

Teraz najważniejsza obserwacja:

```
/admin/
   |
   +-- sprawdza uprawnienia
```

Czyli nie chodzi o znalezienie katalogu, tylko o **zdobycie roli admin** albo obejście sprawdzania roli.

Pamiętasz opis zadania:

> multiple small weaknesses ... can be combined

To sugeruje, że nie będzie jednego wielkiego exploita. Będziemy łączyć:

- wyciek informacji,
- logikę aplikacji,
- błędne zaufanie.

---

Mamy jeszcze jeden bardzo podejrzany endpoint:

```
/api/users/profile.php
```

Pamiętasz:

```
curl "http://10.130.177.50/api/users/profile.php?username=laura.hayes"
```

zwrócił pustkę.

Ale teraz wiemy, że istnieją role i admin panel.

Może ten endpoint wymaga **nagłówka/tokena**.

Najpierw sprawdzimy, czy reaguje na inne parametry.

---

# KROK 33 — Testujemy profile API

Wykonaj:

```
curl -i "http://10.130.177.50/api/users/profile.php?username=admin"
```

oraz:

```
curl -i "http://10.130.177.50/api/users/profile.php?user=admin"
```

Dlaczego?

Bo aplikacje PHP często mają błędy typu:

```
$_GET['username']
```

ale dokumentacja/API zakłada coś innego.

Nie próbujemy jeszcze SQLi — najpierw rozumiemy zachowanie endpointu.

---

Wklej oba wyniki.

Aktualnie nasz cel krótkoterminowy:

```
profile admin
      |
      v
admin notes flag
```

bo pierwsze pytanie CTF-a jest najbliżej.

Dobrze. Ten wynik jest bardzo ważny, bo potwierdza naszą hipotezę.

Oba wywołania:

```
/api/users/profile.php?username=admin
```

oraz:

```
/api/users/profile.php?user=admin
```

kończą się:

```
HTTP/1.1 302 Found
Location: /index.php
```

Czyli API **nie pozwala na anonimowy dostęp**.

Mamy teraz obraz:

```
/api/users/profile.php
        |
        v
sprawdzenie sesji/auth
        |
        +-- brak sesji --> /index.php
```

To samo było z:

```
/admin/
        |
        v
403
```

Czyli najważniejszy brakujący element to:

**jak zdobyć poprawną sesję.**

---

Przypomnijmy sobie coś, co jeszcze nie sprawdziliśmy dokładnie:

Mamy:

```
/forgot.php
```

i wiemy:

```
username=laura.hayes
```

daje:

```
Password reset instructions have been sent...
```

To jest potencjalnie miejsce na **logic flaw**.

Opis CTF-a mówi:

> multiple small weaknesses, ranging from misconfigurations to logic flaws

"Forgot password" bardzo pasuje do "logic flaw".

---

# KROK 34 — Sprawdzamy, co robi reset dla admina

Najpierw sprawdźmy, czy istnieje użytkownik `admin`.

Wykonaj:

```
curl -X POST http://10.130.177.50/forgot.php -d "username=admin"
```

Patrzymy na różnicę:

- brak konta,
- zwykły user,
- admin.

Nie próbujemy jeszcze żadnego exploitowania — tylko mapujemy zachowanie.

---

Wklej wynik.

(Jeżeli admin istnieje, prawdopodobnie będziemy badać dalej sam mechanizm resetu.)

root@ip-10-130-70-238:~# curl -X POST http://10.130.177.50/forgot.php -d "username=admin"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forgot Password - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Password Reset</h2>
  <div class="alert alert-danger">No account found with that username.</div>    <form method="POST" action="/forgot.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <button type="submit" class="btn-primary">Request Reset</button>
  </form>
  <div class="links"><a href="/index.php">Back to login</a></div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Dobrze. To jest kolejna ważna informacja.

Test:

```
curl -X POST http://10.130.177.50/forgot.php -d "username=admin"
```

zwrócił:

```
No account found with that username.
```

Czyli **admin nie jest username'em aplikacji**.

To nam mówi, że musimy rozdzielić dwie rzeczy:

```
admin panel
    |
    +-- rola admin
        |
        +-- prawdopodobnie zwykły użytkownik z role=admin
```

a niekoniecznie konto:

```
username=admin
```

---

Mamy już listę użytkowników z `team.php`:

```
laura.hayes
michael.chen
sarah.johnson
robert.wilson
emma.taylor
david.brown
james.wright
```

Prawdopodobnie jeden z nich ma rolę administratora.

Najbardziej podejrzany:

```
Laura Hayes
Chief Information Officer
```

bo:

- executive leadership,
- wcześniej dała pozytywny reset,
- może mieć wysokie uprawnienia.

---

Teraz wracamy do endpointu:

```
/api/users/profile.php
```

On prawdopodobnie zwraca profil użytkownika **po autoryzacji**.

Ale mamy jeszcze jeden możliwy błąd logiczny:

`profile.php` może ufać parametrowi użytkownika z tokena.

Musimy zdobyć token.

oot@ip-10-130-70-238:~# curl -i -X POST http://10.130.177.50/api/auth/token.php \
-H "Content-Type: application/json" \
-d '{"username":"laura.hayes","password":"test"}'
HTTP/1.1 302 Found
Date: Sat, 05 Sep 2026 13:04:31 GMT
Server: Apache/2.4.58 (Ubuntu)
Location: /index.php
Content-Length: 0
Content-Type: application/json

Dobrze. To potwierdza jeszcze jedną rzecz.

Request:

```
POST /api/auth/token.php
```

z danymi:

```
{"username":"laura.hayes","password":"test"}
```

daje:

```
HTTP/1.1 302 Found
Location: /index.php
```

Czyli endpoint tokenów **nie przyjmuje anonimowych prób**. Najpewniej robi coś w stylu:

```
if (!isset($_SESSION['user'])) {
    header("Location: /index.php");
    exit;
}
```

albo:

```
require_login();
```

---

Ważny wniosek:

Nie próbujemy dalej atakować `token.php` od zewnątrz. Najpierw musimy zdobyć **pierwszą sesję**.

Mamy kilka tropów:

1. `forgot.php` — logic flaw
2. login — może mieć podatność
3. API — może ufać tokenom
4. backup — dał nam tylko devops clue

Teraz najbardziej obiecujący jest **reset hasła**.

Dlaczego?

Bo aplikacja sama mówi:

```
Password reset instructions have been sent to ...
```

ale:

- nie ma emaila,
- nie ma drugiego kanału,
- musi istnieć jakiś mechanizm generowania/resetowania hasła.

W CTF-ach bardzo często reset wygląda np.:

```
username -> reset token -> nowe hasło
```

i token jest gdzieś ujawniony.

---

# KROK 36 — Sprawdzamy odpowiedź resetu z pełnymi nagłówkami

Dla Laury:

```
curl -i -X POST http://10.130.177.50/forgot.php \
-d "username=laura.hayes"
```

Patrzymy na:

- cookies,
- nagłówki,
- nietypowe wartości.

---

Potem sprawdzimy jeszcze `support/`, bo Gobuster znalazł:

```
/support/
```

a w takich zadaniach często jest tam:

- ticket system,
- reset link,
- debug,
- notatki.

Ale jeden krok naraz.

Teraz tylko:

```
curl -i -X POST http://10.130.177.50/forgot.php \
-d "username=laura.hayes"
```

Wklej wynik.

root@ip-10-130-70-238:~# curl -i -X POST http://10.130.177.50/forgot.php \
-d "username=laura.hayes"
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 13:06:07 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 786
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forgot Password - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Password Reset</h2>
    <div class="alert alert-success">Password reset instructions have been sent to la****@nexus.corp</div>  <form method="POST" action="/forgot.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <button type="submit" class="btn-primary">Request Reset</button>
  </form>
  <div class="links"><a href="/index.php">Back to login</a></div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Dobrze. Ten test był potrzebny, ale wynik jest czysty:

```
HTTP/1.1 200 OK
```

i tylko:

```
Password reset instructions have been sent to la****@nexus.corp
```

Nie dostaliśmy:

- tokena resetu,
- ciasteczka,
- redirectu,
- żadnych dodatkowych danych.

Czyli sam endpoint `forgot.php` prawdopodobnie nie jest bezpośrednią drogą.

Teraz ważna korekta kierunku.

Mamy już:

- `devops` z configu,
- `/admin`,
- API wymagające sesji,
- reset, który tylko ujawnia istnienie kont.

Najbardziej podejrzany element, którego jeszcze **nie zbadaliśmy**, to:

```
/support/
```

Gobuster znalazł:

```
/support (301)
```

W kontekście opisu:

> observe how the application behaves, interact with its endpoints, identify weak trust boundaries

"support" często w takich CTF-ach oznacza:

- wewnętrzny panel,
- zgłoszenia,
- wiadomości,
- debug,
- funkcję dla pracowników.

---

# KROK 37 — Sprawdzamy `/support/`

Wykonaj:

```
curl -i http://10.130.177.50/support/
```

Nie robimy jeszcze gobustera. Najpierw chcemy zobaczyć, czy:

- jest publiczny,
- wymaga auth,
- pokazuje coś ciekawego.

Wklej wynik.

root@ip-10-130-70-238:~# curl -i http://10.130.177.50/support/
HTTP/1.1 302 Found
Date: Sat, 05 Sep 2026 13:07:39 GMT
Server: Apache/2.4.58 (Ubuntu)
Location: /index.php
Content-Length: 0
Content-Type: text/html; charset=UTF-8

Dobrze. `/support/` zachowuje się dokładnie tak samo jak poprzednie chronione zasoby:

```
HTTP/1.1 302 Found
Location: /index.php
```

Czyli:

```
/support/
   |
   +-- wymaga sesji
```

Mamy już wzorzec:

```
/admin/             -> 403
/dashboard.php      -> /index.php
/api/auth/token.php -> /index.php
/api/users/profile -> /index.php
/support/           -> /index.php
```

To jest prawie na pewno jedna funkcja:

```
require_login()
```

---

Teraz musimy przestać szukać ukrytych katalogów. Mamy wystarczająco dużo endpointów.

Musimy znaleźć **jak uzyskać sesję**.

Przypominam ważny trop:

W `config.dec` znaleźliśmy:

```
{
  "system_user":"devops"
}
```

To jest bardzo prawdopodobne, że później będzie użyte do SSH / RCE.

Ale najpierw potrzebujemy wejścia do aplikacji.

---

Mamy jeszcze jeden element, którego nie przeanalizowaliśmy:

```
/auth.php
```

Gobuster:

```
/auth.php (Status: 200) [Size: 0]
```

A to jest **bardzo podejrzane**, bo nazwa dokładnie odpowiada za logowanie.

Sprawdzimy, czy jest różnica przy:

- GET,
- POST,
- parametrach.

---

# KROK 38 — Badamy auth.php

Wykonaj:

```
curl -i http://10.130.177.50/auth.php
```

Potem:

```
curl -i -X POST http://10.130.177.50/auth.php
```

Nie wysyłamy jeszcze danych.

Chcemy zobaczyć:

- czy ustawia cookie,
- czy zwraca JSON,
- czy jest backendem dla AJAX.

Wklej oba wyniki.

root@ip-10-130-70-238:~# curl -i http://10.130.177.50/auth.php
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 13:09:22 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8

root@ip-10-130-70-238:~# curl -i -X POST http://10.130.177.50/auth.php
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 13:09:40 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8

Masz rację, zatrzymajmy się na chwilę i zróbmy **korektę strategii**. 40 kroków bez przełomu oznacza, że zaczęliśmy za bardzo "pukać w drzwi", zamiast wykorzystać to, co już wiemy.

To nie znaczy, że nic nie osiągnęliśmy. Mamy kilka ważnych rzeczy:

✅ Recon:

- porty: 22,80
- Apache + PHP

✅ Discovery:

- `/admin/`
- `/api/auth/token.php`
- `/api/users/profile.php`
- `/backup/config.enc`
- `/support/`

✅ Informacje:

- użytkownicy:
    - laura.hayes
    - michael.chen
    - sarah.johnson
    - robert.wilson
    - ...
- system user:

```
"system_user":"devops"
```

✅ Secret:

- AES key znaleziony w JS
- config odszyfrowany

Czyli nie stoimy w miejscu.

---

Natomiast masz rację: dalsze testowanie:

```
curl endpoint
curl endpoint
curl endpoint
```

nie daje wartości.

Musimy przejść na **analizę logiki aplikacji**.

Opis CTF-a od początku mówił:

> modifying parameters, chaining vulnerabilities together

Kluczowe słowo: **parameters**.

Nie szukamy już nowych katalogów. Szukamy parametru, który łamie granicę zaufania.

---

Najbardziej podejrzany endpoint:

```
/api/users/profile.php
```

Dlaczego?

Bo pytanie numer 1:

> What is the flag found in the admin user's profile notes?

To sugeruje:

```
profile.php
    |
    v
user profile
    |
    v
notes
```

Czyli ten endpoint prawdopodobnie jest właściwym celem.

Problem:

```
brak sesji -> redirect
```

Ale w aplikacjach PHP często jest luka typu:

- token w nagłówku,
- parametr role,
- JWT,
- session cookie,
- API key.

---

Teraz zrobimy krok, który powinniśmy zrobić dużo wcześniej.

## KROK 39 — Zobaczmy cookies po zwykłym wejściu

Wykonaj:

```
curl -i http://10.130.177.50/index.php
```

Szukamy:

```
Set-Cookie:
```

Jeżeli aplikacja używa PHP session, zobaczymy coś typu:

```
PHPSESSID=xxxxx
```

---

Potem drugi test:

```
curl -i -c cookies.txt http://10.130.177.50/index.php
```

i:

```
cat cookies.txt
```

---

Dlaczego?

Bo możliwe, że:

- sesja istnieje od razu,
- tylko nie była zachowana przez nasze wcześniejsze `curl`,
- endpointy wymagają cookie.

To jest klasyczny błąd przy ręcznym testowaniu.

Zróbmy teraz ten jeden krok:

```
curl -i http://10.130.177.50/index.php
```

Wklej tylko nagłówki.

oot@ip-10-130-70-238:~# curl -i http://10.130.177.50/index.php
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2026 13:12:17 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 861
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
    <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Dobrze. I tutaj mamy ważną informację: **nie ma PHPSESSID**.

Nagłówki:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
```

Brak:

```
Set-Cookie: PHPSESSID=...
```

Czyli:

- zwykłe wejście na stronę nie tworzy sesji,
- aplikacja prawdopodobnie tworzy sesję dopiero po poprawnym logowaniu,
- nasze wcześniejsze testy bez cookie były poprawne.

Masz rację, że trzeba było wcześniej zrobić większy pivot. Teraz nie szukamy kolejnych katalogów.

---

## Co mamy teraz jako najbardziej prawdopodobny wektor?

Opis zadania:

> modifying parameters, and chaining vulnerabilities together

oraz znalezione:

```
/api/users/profile.php
/api/auth/token.php
```

To pachnie aplikacją API + token.

Możliwy scenariusz:

```
login
 |
 v
token/session
 |
 v
profile API
 |
 v
admin notes
```

Problem: nie znamy hasła.

Więc zamiast atakować endpointy, musimy znaleźć **gdzie aplikacja przechowuje dane użytkowników**.

---

Mamy jeden bardzo mocny trop, którego jeszcze nie wykorzystaliśmy:

```
/api/users/profile.php
```

Gobuster pokazał:

```
/api/users/
    profile.php
```

a katalog miał listing:

```
Index of /api/users
```

To jest błąd konfiguracji.

Sprawdźmy teraz, czy obok `profile.php` nie ma innych plików, których common.txt nie złapał.

---

# KROK 40 — Enumeracja API dokładniej

Wykonaj:

```
gobuster dir -u http://10.130.177.50/api/users/ \
-w /usr/share/wordlists/dirb/common.txt \
-x php,json,txt,bak
```

Dlaczego tutaj?

Bo jeśli znajdziemy np.:

```
users.json
data.php
backup.php
admin.php
```

to może od razu dać profile.

---

Potem zrobimy to samo dla:

```
/api/auth/
```

ale jedna rzecz naraz.

Wykonaj tylko:

```
gobuster dir -u http://10.130.177.50/api/users/ \
-w /usr/share/wordlists/dirb/common.txt \
-x php,json,txt,bak
```

i wklej wynik.

oot@ip-10-130-70-238:~# gobuster dir -u http://10.130.177.50/api/users/ \
-w /usr/share/wordlists/dirb/common.txt \
-x php,json,txt,bak
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.130.177.50/api/users/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,json,txt,bak
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.hta.bak             (Status: 403) [Size: 278]
/.hta.php             (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.hta.json            (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.hta.txt             (Status: 403) [Size: 278]
/.htaccess.json       (Status: 403) [Size: 278]
/.htaccess.bak        (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd.bak        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.json       (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/profile.php          (Status: 302) [Size: 0] [--> /index.php]
Progress: 23070 / 23075 (99.98%)
===============================================================
Finished
===============================================================
root@ip-10-130-70-238:~# gobuster dir -u http://10.130.177.50/api/users/ \
-w /usr/share/wordlists/dirb/common.txt \
-x php,json,txt,bak
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.130.177.50/api/users/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              bak,php,json,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.hta.json            (Status: 403) [Size: 278]
/.hta.bak             (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.hta.txt             (Status: 403) [Size: 278]
/.hta.php             (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.json       (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.json       (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess.bak        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.bak        (Status: 403) [Size: 278]
/profile.php          (Status: 302) [Size: 0] [--> /index.php]
Progress: 23070 / 23075 (99.98%)
===============================================================
Finished
===============================================================
root@ip-10-130-70-238:~# 

Dobrze. I tutaj robimy korektę — ten krok **nie dał nowego endpointu**, ale dał nam ważną informację.

Wynik:

```
/api/users/profile.php -> 302 /index.php
```

czyli nadal:

```
profile.php
    |
    v
require authentication
```

Nie znaleźliśmy:

- `users.json`
- `profiles.json`
- backupu
- plików z danymi

Czyli dane użytkowników nie leżą obok API.

---

Masz rację z tym "40 kroków i żadnych efektów" — dlatego teraz zmieniamy podejście.

Zróbmy **analizę aplikacji**, nie dalsze skanowanie.

Mamy bardzo ciekawy artefakt:

```
/api/auth/token.php
```

i wiemy, że:

- bez sesji → redirect
- ale nazwa mówi "token"

W takich CTF-ach często jest błąd typu:

```
token.php
    |
    +-- generuje token na podstawie parametrów
    +-- nie sprawdza poprawnie roli
```

Musimy zobaczyć, czy endpoint w ogóle odpowiada, gdy dostanie **sesję aplikacji**.

Ale żeby dostać sesję, musimy najpierw zrozumieć login.

---

## KROK 41 — Sprawdzamy formularz loginu dokładniej

Nie przez curl. Chcemy zobaczyć, czy HTML nie ukrywa:

- dodatkowych pól,
- tokena CSRF,
- nazw parametrów.

Wykonaj:

```
curl -s http://10.130.177.50/index.php | grep -A20 "<form"
```

Szukamy czegoś typu:

```
<input type="hidden" name="..."
```

---

Druga rzecz:

Sprawdźmy, czy PHP ujawnia sesję przy błędnym logowaniu:

```
curl -i -c cookies.txt \
-X POST http://10.130.177.50/index.php \
-d "username=laura.hayes&password=test"

cat cookies.txt
```

Jeżeli nawet po błędnym logowaniu nie ma cookie — OK.

Jeżeli pojawi się cookie — mamy punkt zaczepienia.

---

Zrób teraz tylko pierwszy test:

```
curl -s http://10.130.177.50/index.php | grep -A20 "<form"
```

i wklej wynik.

curl -s http://10.130.177.50/index.php | grep -A20 "<form"
    <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>
root@ip-10-130-70-238:~# 

Dobrze. To wyklucza jedną rzecz:

Login **nie ma**:

- CSRF tokena,
- ukrytych pól,
- dodatkowego parametru.

Formularz jest bardzo prosty:

```
username
password
```

Czyli jeśli mamy wejść, to droga będzie prawdopodobnie przez:

1. zdobycie hasła,
2. obejście logowania,
3. manipulację logiką po autoryzacji.

Teraz zrobimy krok, który powinien być zrobiony wcześniej: **sprawdzimy, czy login jest podatny na SQL injection**.

Nie zaczynamy od sqlmap. Najpierw ręcznie, bo to CTF i chcemy rozumieć.

---

## KROK 42 — Test SQLi w loginie

Wykonaj:

```
curl -i -X POST http://10.130.177.50/index.php \
-d "username=' OR 1=1-- -&password=test"
```

Patrzymy, czy odpowiedź zmieni się z:

```
Invalid credentials
```

na:

- redirect,
- dashboard,
- inną treść.

---

Jeżeli nie zadziała, zrobimy drugi wariant.

Wklej wynik tego jednego testu.

Masz rację — kończymy "chodzenie po omacku". Mamy mało czasu, więc robimy **celowany ruch**.

Wynik SQLi:

```
' OR 1=1-- -
```

→ nadal:

```
Invalid credentials
```

Czyli **login nie wygląda na klasyczne SQLi**.

Teraz patrząc na cały obraz:

Najważniejszy fakt, który mamy:

```
backup/config.enc
        |
        v
system_user = devops
```

oraz:

```
/api/users/profile.php
```

a pytanie nr 1:

> flag found in admin user's profile notes

To oznacza, że **musimy dostać się do profilu**, a niekoniecznie przez login.

W CTF Domino prawdopodobny łańcuch jest:

```
information disclosure
        |
        v
JWT/token flaw
        |
        v
admin profile
        |
        v
RCE
        |
        v
devops
        |
        v
root
```

Najbardziej podejrzany jest teraz **token endpoint**.

Nie marnujemy czasu na login.

---

## OSTATNI SZYBKI TEST — token.php z nietypowym nagłówkiem

Wykonaj:

```
curl -i http://10.130.177.50/api/auth/token.php \
-H "X-Forwarded-For: 127.0.0.1"
```

i:

```
curl -i http://10.130.177.50/api/auth/token.php \
-H "Authorization: Bearer admin"
```

Dlaczego?

Bo wiele CTF-ów robi błędne zaufanie:

```
if ($_SERVER['REMOTE_ADDR']=="127.0.0.1")
```

albo:

```
Authorization: Bearer ...
```

---

Jeżeli oba dadzą redirect, następny ruch będzie prawdopodobnie **analiza parametrów API** przez fuzzowanie nazw parametrów (`user`, `id`, `role`, `token`).

Ale teraz tylko te dwa szybkie requesty. Nie skanujemy już nic dużego.
