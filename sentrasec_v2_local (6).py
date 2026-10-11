#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║       SENTRASEC v2.0 LOCAL — AI SOC Assistant                   ║
║       100% Offline · Ollama LLM · RAG · SQLite                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STACK:                                                          ║
║  • Ollama (lokalny LLM: llama3, mistral, gemma3, phi3...)        ║
║  • RAG: embeddings → chromadb / in-memory fallback              ║
║  • SQLite — pełna persystencja danych                           ║
║  • Flask + SSE — live log stream                                ║
║  • Zero zewnętrznych API — pełna prywatność danych              ║
║                                                                  ║
║  INSTALL:                                                        ║
║    pip install flask flask-cors requests                         ║
║    pip install chromadb sentence-transformers   # opcjonalne RAG ║
║    # Zainstaluj Ollama: https://ollama.com                       ║
║    ollama pull llama3        # lub mistral, gemma3, phi3         ║
║                                                                  ║
║  RUN:                                                            ║
║    ollama serve   (w osobnym terminalu)                          ║
║    python sentrasec_v2_local.py                                  ║
║    http://localhost:5000                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os, re, json, time, random, sqlite3, hashlib, threading, datetime, ipaddress
import queue, glob, secrets, functools
from pathlib import Path
from collections import defaultdict
from typing import Optional, List, Dict, Any

from flask import Flask, request, jsonify, Response, stream_with_context, render_template_string
from flask_cors import CORS

try:
    import requests as req_lib
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False
    print("[ERROR] Brak biblioteki requests: pip install requests")

# ── Watchdog (opcjonalnie — file tailing) ────────────────────────
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_OK = True
except ImportError:
    WATCHDOG_OK = False

# ── RAG (opcjonalnie) ────────────────────────────────────────────
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_OK = True
except ImportError:
    CHROMA_OK = False

try:
    from sentence_transformers import SentenceTransformer
    ST_OK = True
except ImportError:
    ST_OK = False

# ═══════════════════════════════════════════════════════════════════
#  KONFIGURACJA
# ═══════════════════════════════════════════════════════════════════
OLLAMA_HOST    = os.environ.get("OLLAMA_HOST",    "http://localhost:11434")
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL",   "llama3")
ABUSEIPDB_KEY  = os.environ.get("ABUSEIPDB_API_KEY", "")
DB_PATH        = "sentrasec_local.db"
RAG_DB_PATH    = "sentrasec_rag"
MAX_LOG_LINES  = 1000
OLLAMA_TIMEOUT = 240

# ── Auth & Rate Limiting ─────────────────────────────────────────
API_KEY_FILE   = "sentrasec_apikey.txt"
RATE_LIMIT_REQ = 120   # requests per minute per IP (0 = disabled)

def _load_or_create_api_key() -> str:
    if Path(API_KEY_FILE).exists():
        return Path(API_KEY_FILE).read_text().strip()
    key = secrets.token_hex(24)
    Path(API_KEY_FILE).write_text(key)
    return key

API_KEY = _load_or_create_api_key()

# ── Real-time file tailing ────────────────────────────────────────
TAIL_FILES = [
    "/var/log/auth.log",
    "/var/log/ufw.log",
    "/var/log/syslog",
    "/var/log/kern.log",
    "/var/log/suricata/fast.log",
    "/var/log/nginx/access.log",
    "/var/log/apache2/access.log",
    "/var/log/fail2ban.log",
]
# Queue shared between tailer threads and SSE stream
_ingest_queue: queue.Queue = queue.Queue(maxsize=5000)
_tail_threads: Dict[str, threading.Thread] = {}

# ── Source presets ────────────────────────────────────────────────
SOURCE_PRESETS = {
    "ubuntu_ssh_ufw": {
        "name": "Ubuntu Server + UFW + SSH",
        "files": ["/var/log/auth.log", "/var/log/ufw.log", "/var/log/syslog"],
        "description": "Standardowy serwer Ubuntu z firewallem UFW i SSH"
    },
    "proxmox_wazuh": {
        "name": "Proxmox + Wazuh",
        "files": ["/var/log/auth.log", "/var/ossec/logs/alerts/alerts.log", "/var/log/syslog"],
        "description": "Proxmox VE z agentem Wazuh HIDS"
    },
    "nginx_fail2ban": {
        "name": "NGINX + Fail2ban",
        "files": ["/var/log/nginx/access.log", "/var/log/nginx/error.log", "/var/log/fail2ban.log"],
        "description": "Web server NGINX z ochroną Fail2ban"
    },
    "suricata_ids": {
        "name": "Suricata IDS/IPS",
        "files": ["/var/log/suricata/fast.log", "/var/log/suricata/eve.json", "/var/log/auth.log"],
        "description": "Suricata Network IDS z logami systemowymi"
    },
    "docker_host": {
        "name": "Docker Host",
        "files": ["/var/log/auth.log", "/var/log/syslog", "/var/log/kern.log"],
        "description": "Host Docker z monitoringiem systemowym"
    },
    "windows_eventlog": {
        "name": "Windows Event Log (via Winlogbeat)",
        "files": [],
        "description": "Windows Events przesyłane przez Winlogbeat/Filebeat → /api/ingest"
    },
}

# ── Rate limiter ─────────────────────────────────────────────────
_rate_buckets: Dict[str, List] = defaultdict(list)
_rate_lock = threading.Lock()

def check_rate_limit(ip: str) -> bool:
    """Returns True if request is allowed."""
    if RATE_LIMIT_REQ == 0:
        return True
    now = time.time()
    with _rate_lock:
        bucket = _rate_buckets[ip]
        _rate_buckets[ip] = [t for t in bucket if now - t < 60]
        if len(_rate_buckets[ip]) >= RATE_LIMIT_REQ:
            return False
        _rate_buckets[ip].append(now)
    return True

def require_api_key(f):
    """Decorator: require X-API-Key header or ?api_key= param."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr or "unknown"
        if not check_rate_limit(ip):
            return jsonify({"error": "Rate limit exceeded"}), 429
        key = request.headers.get("X-API-Key") or request.args.get("api_key","")
        if key and key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════
#  OLLAMA ENGINE — sprawdzenie i pomocnicze funkcje
# ═══════════════════════════════════════════════════════════════════
def ollama_ping() -> bool:
    """Sprawdza czy Ollama jest dostępna — z krótkim timeoutem."""
    if not REQUESTS_OK: return False
    try:
        r = req_lib.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def ollama_list_models() -> List[str]:
    """Listuje dostępne modele w Ollama — bezpiecznie."""
    try:
        r = req_lib.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if r.status_code == 200:
            data = r.json()
            models = data.get("models", [])
            return [m["name"] for m in models if isinstance(m, dict) and "name" in m]
    except Exception:
        pass
    return []

def ollama_chat(messages: List[Dict], system: str = "", stream: bool = False):
    """
    Wywołanie Ollama /api/chat.
    messages: [{"role": "user"/"assistant", "content": "..."}]
    Zwraca: str (stream=False) lub generator (stream=True)
    """
    payload = {
        "model":    get_model_name(),
        "messages": [{"role": "system", "content": system}] + messages if system else messages,
        "stream":   stream,
        "options": {
            "temperature": 0.3,   # niższa = bardziej deterministyczne, lepsze dla analizy
            "num_predict": 2048,
            "top_p": 0.9,
        }
    }

    try:
        if stream:
            resp = req_lib.post(
                f"{OLLAMA_HOST}/api/chat",
                json=payload, stream=True, timeout=OLLAMA_TIMEOUT
            )
            def gen_stream():
                for line in resp.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            text  = chunk.get("message", {}).get("content", "")
                            if text:
                                yield text
                            if chunk.get("done"):
                                break
                        except:
                            pass
            return gen_stream()
        else:
            resp = req_lib.post(
                f"{OLLAMA_HOST}/api/chat",
                json=payload, timeout=OLLAMA_TIMEOUT
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("message", {}).get("content", "")
            else:
                return f"[Ollama Error {resp.status_code}] {resp.text[:200]}"
    except req_lib.exceptions.ConnectionError:
        return ("[BŁĄD] Ollama nie jest uruchomiona.\n\n"
                "Uruchom: `ollama serve` w osobnym terminalu.\n"
                f"Host: {OLLAMA_HOST}")
    except req_lib.exceptions.Timeout:
        return f"[TIMEOUT] Ollama nie odpowiedziała w {OLLAMA_TIMEOUT}s. Spróbuj mniejszego modelu lub zwiększ zasoby."
    except Exception as e:
        return f"[BŁĄD] {e}"

def get_model_name() -> str:
    """Zwraca pełną nazwę modelu — dodaje :latest jeśli brak tagu."""
    models = ollama_list_models()
    m = OLLAMA_MODEL
    if m in models:
        return m
    # Try with :latest suffix
    if f"{m}:latest" in models:
        return f"{m}:latest"
    # Try prefix match (e.g. "llama3" matches "llama3:latest")
    for model in models:
        if model.startswith(m.split(':')[0]):
            return model
    return m  # fallback to original
    """Generuje embedding dla tekstu (RAG)."""
    try:
        r = req_lib.post(f"{OLLAMA_HOST}/api/embeddings",
                         json={"model": OLLAMA_MODEL, "prompt": text[:2000]}, timeout=30)
        if r.status_code == 200:
            return r.json().get("embedding")
    except:
        pass
    return None

# ═══════════════════════════════════════════════════════════════════
#  RAG — Knowledge Base
# ═══════════════════════════════════════════════════════════════════
# Wbudowana baza wiedzy SOC (gdy ChromaDB niedostępne)
SOC_KNOWLEDGE_BASE = [
    {
        "id": "mitre_T1110",
        "text": "MITRE T1110 Brute Force: Atakujący próbuje odgadnąć hasło metodą brute-force lub słownikową. Wskaźniki: wielokrotne nieudane logowania z tego samego IP, różni użytkownicy z jednego IP, podejrzane godziny. Remediation: fail2ban, limit prób logowania, MFA, silna polityka haseł.",
        "category": "mitre", "severity": "HIGH"
    },
    {
        "id": "mitre_T1046",
        "text": "MITRE T1046 Network Service Scanning: Atakujący skanuje sieć w poszukiwaniu otwartych portów i usług. Wskaźniki: logi Nmap, Masscan, szybkie połączenia na wiele portów. Remediation: firewall, IDS/IPS, segmentacja sieci.",
        "category": "mitre", "severity": "MEDIUM"
    },
    {
        "id": "mitre_T1548",
        "text": "MITRE T1548 Abuse Elevation Control Mechanism: Eskalacja uprawnień przez sudo, SUID, chmod. Wskaźniki: polecenia sudo z nieoczekiwanego konta, modyfikacja /etc/passwd, /etc/shadow, chmod 777. Remediation: audyt sudo, least privilege, monitoring SUID.",
        "category": "mitre", "severity": "CRITICAL"
    },
    {
        "id": "mitre_T1078",
        "text": "MITRE T1078 Valid Accounts: Atakujący używa skradzionych/legalnych danych uwierzytelniających. Wskaźniki: logowanie z nowego IP/kraju, nieznana pora dnia, anomalie UEBA. Remediation: MFA, UEBA, monitoring sesji.",
        "category": "mitre", "severity": "HIGH"
    },
    {
        "id": "mitre_T1190",
        "text": "MITRE T1190 Exploit Public-Facing Application: Atak na webaplikację przez SQLi, XSS, RCE. Wskaźniki: 500/403 błędy, payloady w URL/body, logi WAF. Remediation: WAF, patching, SAST/DAST.",
        "category": "mitre", "severity": "CRITICAL"
    },
    {
        "id": "mitre_T1041",
        "text": "MITRE T1041 Exfiltration Over C2 Channel: Eksfiltracja danych przez curl/wget/nc. Wskaźniki: duże transfery na zewnętrzne IP, nieznane procesy nawiązujące połączenia. Remediation: DLP, egress filtering, monitorowanie transferu danych.",
        "category": "mitre", "severity": "CRITICAL"
    },
    {
        "id": "mitre_T1059",
        "text": "MITRE T1059 Command and Scripting Interpreter: Wykonanie złośliwych skryptów bash/sh/powershell. Wskaźniki: procesy uruchomione z /tmp, nieznane skrypty, wget/curl piped do bash. Remediation: application whitelisting, script signing, auditd.",
        "category": "mitre", "severity": "HIGH"
    },
    {
        "id": "playbook_brute_force",
        "text": "Playbook Brute Force: 1) Zidentyfikuj źródłowy IP atakującego. 2) Zablokuj IP: `ufw deny from <IP>`. 3) Sprawdź czy konto nie zostało skompromitowane: sprawdź logi auth.log po udanym logowaniu. 4) Włącz fail2ban jeśli nie jest aktywny. 5) Rozważ zmianę hasła zaatakowanego konta. 6) Dodaj alerting na przyszłe próby.",
        "category": "playbook", "severity": "HIGH"
    },
    {
        "id": "playbook_privilege_escalation",
        "text": "Playbook Privilege Escalation: 1) Natychmiast sprawdź aktywne sesje: `who`, `w`, `last`. 2) Zakończ podejrzane sesje: `pkill -u <user>`. 3) Sprawdź modyfikacje /etc/passwd, /etc/shadow, crontab. 4) Przejrzyj logi auditd dla polecenia sudo. 5) Zmień hasło roota i kont admina. 6) Sprawdź nowe konta: `cat /etc/passwd | grep -v nologin`.",
        "category": "playbook", "severity": "CRITICAL"
    },
    {
        "id": "nist_csf",
        "text": "NIST Cybersecurity Framework: Identify (ID), Protect (PR), Detect (DE), Respond (RS), Recover (RC). Kluczowe kontrole: inwentaryzacja aktywów, zarządzanie dostępem, monitoring, plan IR, backupy. Wymagane dokumenty: polityka bezpieczeństwa, procedury IR, inwentarz aktywów.",
        "category": "compliance", "severity": "INFO"
    },
    {
        "id": "iso_27001",
        "text": "ISO 27001: ISMS (Information Security Management System). Kluczowe kontrole Annex A: A.9 Kontrola dostępu, A.12 Bezpieczeństwo operacyjne, A.16 Zarządzanie incydentami, A.17 Ciągłość działania. Wymagane: Statement of Applicability, Risk Assessment, Risk Treatment Plan.",
        "category": "compliance", "severity": "INFO"
    },
    {
        "id": "pci_dss",
        "text": "PCI DSS v4.0: 12 głównych wymagań. Krytyczne dla SOC: Req 10 (logging i monitoring), Req 11 (testy bezpieczeństwa), Req 12 (polityki bezpieczeństwa). Logging musi obejmować: dostęp do danych kart, nieudane logowania, zmiany uprawnień.",
        "category": "compliance", "severity": "INFO"
    },
    {
        "id": "gdpr_security",
        "text": "GDPR Art. 32: Środki techniczne i organizacyjne. Wymagane: szyfrowanie danych osobowych, pseudonimizacja, ocena ryzyka, procedury naruszenia danych (notyfikacja w 72h do UODO). Incydenty naruszające dane osobowe muszą być raportowane.",
        "category": "compliance", "severity": "INFO"
    },
    {
        "id": "ssh_hardening",
        "text": "SSH Hardening: Wyłącz logowanie root (PermitRootLogin no), używaj kluczy SSH (PasswordAuthentication no), zmień port (Port 2222), ogranicz dostęp (AllowUsers, AllowGroups), włącz MaxAuthTries 3, używaj fail2ban, monitoruj /var/log/auth.log.",
        "category": "hardening", "severity": "MEDIUM"
    },
    {
        "id": "firewall_ufw",
        "text": "UFW/iptables best practices: Domyślna polityka DENY (ufw default deny incoming), zezwól tylko na potrzebne porty, loguj odrzucone pakiety (ufw logging on), regularnie przeglądaj reguły (ufw status verbose), automatyczne aktualizacje reguł przy nowych zagrożeniach.",
        "category": "hardening", "severity": "MEDIUM"
    },
    {
        "id": "log_analysis_ssh",
        "text": "Analiza logów SSH: Nieudane logowania: 'Failed password for'. Udane logowania: 'Accepted password/publickey for'. Invalid user: 'Invalid user'. Disconnect: 'Disconnected from'. Kluczowe pola: użytkownik, IP źródłowe, port, metoda. Wzorzec brute-force: >10 failed/min z jednego IP.",
        "category": "log_analysis", "severity": "INFO"
    },
    {
        "id": "log_analysis_ufw",
        "text": "Analiza logów UFW: '[UFW BLOCK]' = zablokowany pakiet. Kluczowe pola: IN=interfejs, SRC=IP źródłowe, DST=IP docelowe, PROTO=protokół, DPT=port docelowy. Wzorzec skanowania: wiele BLOCK z jednego IP na różne DPT w krótkim czasie.",
        "category": "log_analysis", "severity": "INFO"
    },
]

class RAGEngine:
    """
    Prosty RAG (Retrieval Augmented Generation) engine.
    Obsługuje ChromaDB (z embeddings) lub fallback do TF-IDF.
    """
    def __init__(self):
        self.docs    = SOC_KNOWLEDGE_BASE.copy()
        self.use_chroma = False
        self._chroma_client = None
        self._collection    = None
        self._init_storage()

    def _init_storage(self):
        if CHROMA_OK:
            try:
                self._chroma_client = chromadb.PersistentClient(path=RAG_DB_PATH)
                self._collection    = self._chroma_client.get_or_create_collection(
                    name="sentrasec_kb",
                    metadata={"hnsw:space": "cosine"}
                )
                # Zaindeksuj bazę wiedzy jeśli pusta
                existing = self._collection.count()
                if existing == 0:
                    self._index_knowledge_base()
                self.use_chroma = True
                print(f"[RAG] ChromaDB aktywny — {self._collection.count()} dokumentów")
            except Exception as e:
                print(f"[RAG] ChromaDB fallback → TF-IDF ({e})")
        else:
            print("[RAG] ChromaDB niedostępny → TF-IDF in-memory")

    def _index_knowledge_base(self):
        """Indeksuje wbudowaną bazę wiedzy do ChromaDB."""
        ids  = [d["id"] for d in SOC_KNOWLEDGE_BASE]
        docs = [d["text"] for d in SOC_KNOWLEDGE_BASE]
        meta = [{"category": d["category"], "severity": d["severity"]} for d in SOC_KNOWLEDGE_BASE]
        self._collection.add(ids=ids, documents=docs, metadatas=meta)

    def add_log_document(self, session_id: str, text: str, meta: Dict):
        """Dodaje przeanalizowany log do RAG store dla przyszłych zapytań."""
        if not self.use_chroma: return
        doc_id = f"log_{session_id}_{hashlib.md5(text.encode()).hexdigest()[:8]}"
        try:
            self._collection.add(ids=[doc_id], documents=[text[:500]], metadatas=[meta])
        except:
            pass  # duplicate ignore

    def retrieve(self, query: str, n: int = 5, category: str = None) -> List[Dict]:
        """Pobiera najbardziej pasujące dokumenty do zapytania."""
        if self.use_chroma:
            try:
                where = {"category": category} if category else None
                results = self._collection.query(
                    query_texts=[query], n_results=min(n, self._collection.count()),
                    where=where
                )
                docs = results.get("documents", [[]])[0]
                meta = results.get("metadatas", [[]])[0]
                return [{"text": d, "meta": m} for d, m in zip(docs, meta)]
            except:
                pass
        # Fallback: proste TF-IDF keyword matching
        return self._tfidf_retrieve(query, n, category)

    def _tfidf_retrieve(self, query: str, n: int, category: str = None) -> List[Dict]:
        """Prosty keyword retrieval jako fallback."""
        query_words = set(query.lower().split())
        scored = []
        for doc in self.docs:
            if category and doc["category"] != category:
                continue
            doc_words = set(doc["text"].lower().split())
            score = len(query_words & doc_words) / max(len(query_words), 1)
            # Bonus za trafne słowa kluczowe
            kw_bonus = sum(0.3 for kw in ["brute","ssh","sudo","exploit","nmap","fail2ban","block","critical"]
                          if kw in query.lower() and kw in doc["text"].lower())
            scored.append((score + kw_bonus, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"text": d["text"], "meta": {"category": d["category"]}} for _, d in scored[:n]]

rag_engine = RAGEngine()

# ═══════════════════════════════════════════════════════════════════
#  DATABASE — SQLite
# ═══════════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY, created_at TEXT, threat_level TEXT DEFAULT 'low',
            notes TEXT, label TEXT DEFAULT '', tags TEXT DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS log_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, raw TEXT, log_type TEXT, severity TEXT,
            timestamp_raw TEXT, timestamp_iso TEXT, src_ip TEXT, dst_ip TEXT,
            src_port TEXT, dst_port TEXT, username TEXT, event_type TEXT,
            mitre_id TEXT, mitre_name TEXT, inserted_at TEXT,
            source_file TEXT DEFAULT '', ingest_source TEXT DEFAULT 'manual'
        );
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, title TEXT, severity TEXT, src_ip TEXT,
            mitre_ids TEXT, timeline TEXT, risk_score REAL,
            status TEXT DEFAULT 'open', created_at TEXT,
            tags TEXT DEFAULT '[]', comment TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, role TEXT, content TEXT, created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS ip_reputation (
            ip TEXT PRIMARY KEY, country TEXT, isp TEXT, abuse_score INTEGER,
            is_vpn INTEGER, is_tor INTEGER, source TEXT, checked_at TEXT
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, title TEXT, severity TEXT, detail TEXT,
            mitre_id TEXT, created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS playbook_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, action TEXT, target TEXT,
            command TEXT, result TEXT, executed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS ueba_baselines (
            username TEXT PRIMARY KEY, usual_country TEXT,
            usual_hour_start INTEGER, usual_hour_end INTEGER,
            usual_ips TEXT, risk_score REAL DEFAULT 0.0, updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS file_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, file_path TEXT, status TEXT DEFAULT 'watching',
            lines_ingested INTEGER DEFAULT 0, last_seen TEXT, added_at TEXT
        );
        CREATE TABLE IF NOT EXISTS ingest_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT, source TEXT, lines INTEGER,
            received_at TEXT
        );
        /* FTS5 full-text search on log entries */
        CREATE VIRTUAL TABLE IF NOT EXISTS logs_fts USING fts5(
            raw, log_type, severity, src_ip, username, event_type,
            content='log_entries', content_rowid='id'
        );
        /* FTS triggers */
        CREATE TRIGGER IF NOT EXISTS logs_fts_insert AFTER INSERT ON log_entries BEGIN
            INSERT INTO logs_fts(rowid, raw, log_type, severity, src_ip, username, event_type)
            VALUES (new.id, new.raw, new.log_type, new.severity, new.src_ip, new.username, new.event_type);
        END;
        CREATE TRIGGER IF NOT EXISTS logs_fts_delete AFTER DELETE ON log_entries BEGIN
            INSERT INTO logs_fts(logs_fts, rowid, raw, log_type, severity, src_ip, username, event_type)
            VALUES ('delete', old.id, old.raw, old.log_type, old.severity, old.src_ip, old.username, old.event_type);
        END;
    """)
    conn.commit(); conn.close()

def get_db():
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row; return c

init_db()

# ═══════════════════════════════════════════════════════════════════
#  REAL-TIME FILE TAILER + INGEST ENGINE
# ═══════════════════════════════════════════════════════════════════
_ingest_queue: queue.Queue = queue.Queue(maxsize=5000)
_tail_threads: Dict[str, threading.Thread] = {}
_ingest_sse_clients: List[queue.Queue] = []
_ingest_lock = threading.Lock()

def _tail_file(path: str, session_id: str):
    """Tails a file and pushes new lines to _ingest_queue."""
    try:
        with open(path, 'r', errors='replace') as f:
            f.seek(0, 2)
            while path in _tail_threads:
                line = f.readline()
                if line:
                    line = line.rstrip()
                    if line:
                        try:
                            _ingest_queue.put_nowait({
                                "line": line, "source": path,
                                "session_id": session_id,
                                "ts": datetime.datetime.utcnow().isoformat()
                            })
                        except queue.Full:
                            pass
                else:
                    time.sleep(0.25)
    except Exception:
        pass

def start_file_tail(path: str, session_id: str) -> bool:
    if path in _tail_threads and _tail_threads[path].is_alive():
        return False
    if not Path(path).exists():
        return False
    t = threading.Thread(target=_tail_file, args=(path, session_id), daemon=True)
    t.start()
    _tail_threads[path] = t
    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    conn.execute("""INSERT OR REPLACE INTO file_sources
        (session_id,file_path,status,lines_ingested,last_seen,added_at)
        VALUES (?,?,'watching',0,?,?)""", (session_id, path, now, now))
    conn.commit(); conn.close()
    return True

def stop_file_tail(path: str):
    _tail_threads.pop(path, None)
    conn = get_db()
    conn.execute("UPDATE file_sources SET status='stopped' WHERE file_path=?", (path,))
    conn.commit(); conn.close()

def _ingest_processor():
    """Background: parse queued lines, store in DB, broadcast to SSE."""
    while True:
        try:
            item = _ingest_queue.get(timeout=1)
            line = item.get("line","")
            sid  = item.get("session_id","GLOBAL")
            src  = item.get("source","ingest")
            parsed = parse_log_entry(line)
            sev = parsed["severity"] if parsed else "INFO"
            if parsed:
                now = datetime.datetime.utcnow().isoformat()
                conn = get_db()
                conn.execute("""INSERT INTO log_entries
                    (session_id,raw,log_type,severity,timestamp_raw,timestamp_iso,
                     src_ip,dst_ip,src_port,dst_port,username,event_type,
                     mitre_id,mitre_name,inserted_at,source_file,ingest_source)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (sid, parsed["raw"], parsed["log_type"], sev,
                     (parsed.get("timestamp") or {}).get("raw"),
                     (parsed.get("timestamp") or {}).get("iso"),
                     parsed.get("src_ip"), parsed.get("dst_ip"),
                     parsed.get("src_port"), parsed.get("dst_port"),
                     parsed.get("username"), parsed.get("event"),
                     parsed.get("mitre_id"), parsed.get("mitre_name"),
                     now, src, "tail"))
                conn.commit(); conn.close()
            evt = {
                "ts": datetime.datetime.utcnow().strftime("%H:%M:%S"),
                "sev": sev[:4].upper(), "src": Path(src).name[:14],
                "msg": line[:140], "real": True,
                "mitre": parsed.get("mitre_id","") if parsed else ""
            }
            with _ingest_lock:
                dead = []
                for q in _ingest_sse_clients:
                    try: q.put_nowait(evt)
                    except queue.Full: dead.append(q)
                for q in dead:
                    try: _ingest_sse_clients.remove(q)
                    except: pass
        except queue.Empty:
            pass
        except Exception:
            pass

threading.Thread(target=_ingest_processor, daemon=True).start()

# ═══════════════════════════════════════════════════════════════════
#  MITRE ATT&CK MAPPING
# ═══════════════════════════════════════════════════════════════════
MITRE_MAP = {
    "T1110": {"name":"Brute Force",              "tactic":"Credential Access",   "kw":["failed password","authentication failure","invalid user","brute","login fail"]},
    "T1021": {"name":"Remote Services",           "tactic":"Lateral Movement",    "kw":["ssh","rdp","smb","winrm","telnet"]},
    "T1046": {"name":"Network Service Scanning",  "tactic":"Discovery",           "kw":["nmap","scan","portscan","masscan","shodan"]},
    "T1548": {"name":"Abuse Elevation Control",   "tactic":"Privilege Escalation","kw":["sudo","chmod","setuid","chown","privilege"]},
    "T1078": {"name":"Valid Accounts",             "tactic":"Initial Access",      "kw":["accepted","logged in","login success","authenticated"]},
    "T1190": {"name":"Exploit Public App",         "tactic":"Initial Access",      "kw":["exploit","rce","sqli","xss","lfi","rfi","shell upload"]},
    "T1136": {"name":"Create Account",             "tactic":"Persistence",         "kw":["useradd","adduser","new user","created account"]},
    "T1041": {"name":"Exfiltration Over C2",       "tactic":"Exfiltration",        "kw":["curl","wget","nc ","netcat","data transfer","upload"]},
    "T1059": {"name":"Command-Line Interface",     "tactic":"Execution",           "kw":["bash","sh -c","cmd.exe","powershell","/bin/sh"]},
    "T1083": {"name":"File & Dir Discovery",       "tactic":"Discovery",           "kw":["ls -la","find /","cat /etc","/etc/passwd","/etc/shadow"]},
    "T1070": {"name":"Indicator Removal",          "tactic":"Defense Evasion",     "kw":["rm -rf","shred","unlink","log clear","history -c"]},
    "T1562": {"name":"Disable Security Tools",     "tactic":"Defense Evasion",     "kw":["ufw disable","iptables -F","systemctl stop","disable firewall"]},
    "T1071": {"name":"App Layer Protocol C2",      "tactic":"Command & Control",   "kw":["c2","command and control","beacon","dns tunnel"]},
    "T1505": {"name":"Server Software Component",  "tactic":"Persistence",         "kw":["webshell","php shell","asp shell","crontab","at job"]},
    "T1486": {"name":"Data Encrypted for Impact",  "tactic":"Impact",              "kw":["encrypt","ransom","locked","crypt"]},
}

def map_mitre(line: str) -> Optional[Dict]:
    ll = line.lower()
    for tid, info in MITRE_MAP.items():
        if any(kw in ll for kw in info["kw"]):
            return {"id": tid, **info}
    return None

# ═══════════════════════════════════════════════════════════════════
#  LOG PARSER
# ═══════════════════════════════════════════════════════════════════
TS_PATTERNS = [
    (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?', 'ISO 8601'),
    (r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?', 'DateTime'),
    (r'\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}',           'Syslog-date'),
    (r'[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',    'Syslog RFC3164'),
    (r'\b\d{10,13}\b',                                      'Unix timestamp'),
]

LOG_TYPES = {
    "FIREWALL_UFW":         [r'ufw|iptables|netfilter'],
    "SSH_AUTH":             [r'sshd\[|sshd:'],
    "WEB_ACCESS":           [r'"(GET|POST|PUT|DELETE|HEAD|PATCH)\s|apache|nginx|httpd'],
    "AUTH_FAILURE":         [r'failed password|authentication failure|invalid user'],
    "PRIVILEGE_ESCALATION": [r'sudo:|su\[|chmod\s+[0-7]{3,4}|setuid'],
    "KERNEL_EVENT":         [r'kernel:|kernel\['],
    "IDS_IPS":              [r'snort|suricata|ossec|zeek|alert:'],
    "CRON_JOB":             [r'cron|crond'],
    "DNS":                  [r'\bdns\b|named|resolv'],
    "VPN":                  [r'\bvpn\b|openvpn|wireguard'],
    "DATABASE":             [r'\bsql\b|database|mysql|postgres|mongodb'],
    "AUDIT":                [r'\baudit\b|auditd'],
    "FAIL2BAN":             [r'fail2ban'],
}

def detect_log_type(line: str) -> str:
    ll = line.lower()
    for ltype, pats in LOG_TYPES.items():
        if any(re.search(p, ll) for p in pats): return ltype
    return "GENERIC_SYSLOG"

def extract_timestamp(line: str) -> Optional[Dict]:
    for pat, fmt in TS_PATTERNS:
        m = re.search(pat, line)
        if m:
            raw = m.group()
            dt  = None
            try:
                dt = datetime.datetime.fromisoformat(raw.replace(' ','T').rstrip('Z'))
            except: pass
            return {"raw": raw, "fmt": fmt, "iso": dt.isoformat() if dt else None}
    return None

def extract_ips(line: str) -> List[str]:
    cands = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
    valid = []
    for ip in cands:
        try:
            obj = ipaddress.ip_address(ip)
            if not obj.is_loopback: valid.append(ip)
        except: pass
    return list(set(valid))

def detect_severity(line: str) -> str:
    ll = line.lower()
    if re.search(r'\bcrit(?:ical)?\b|emerg(?:ency)?\b|alert\b', ll): return "CRITICAL"
    if re.search(r'\berr(?:or)?\b|fail(?:ure|ed)?\b|denied\b|block(?:ed)?\b|attack\b|malware\b|brute\b|exploit\b', ll): return "HIGH"
    if re.search(r'\bwarn(?:ing)?\b|invalid\b|unauthorized\b|refused\b|suspicious\b', ll): return "MEDIUM"
    if re.search(r'\binfo\b|notice\b|success\b|accepted\b|established\b', ll): return "LOW"
    if re.search(r'\bdebug\b|dbg\b|trace\b', ll): return "INFO"
    return "MEDIUM"

def parse_log_entry(line: str) -> Optional[Dict]:
    line = line.strip()
    if not line or line.startswith('#'): return None
    ts    = extract_timestamp(line)
    ltype = detect_log_type(line)
    ips   = extract_ips(line)
    sev   = detect_severity(line)
    mitre = map_mitre(line)
    fields = {
        "raw": line, "log_type": ltype, "severity": sev,
        "ips": ips, "src_ip": None, "dst_ip": None, "src_port": None, "dst_port": None,
        "username": None, "event": None, "timestamp": ts,
        "mitre_id": mitre["id"] if mitre else None,
        "mitre_name": mitre["name"] if mitre else None,
        "mitre_tactic": mitre.get("tactic") if mitre else None,
    }
    if ltype == "FIREWALL_UFW":
        for key, pat in [("src_ip","SRC=(\\S+)"),("dst_ip","DST=(\\S+)"),
                          ("src_port","SPT=(\\d+)"),("dst_port","DPT=(\\d+)")]:
            m = re.search(pat, line);
            if m: fields[key] = m.group(1)
        fields["action"] = "BLOCK" if re.search(r'BLOCK|DROP|DENY', line.upper()) else "ALLOW"
        fields["event"]  = f"FIREWALL_{fields['action']}"
    elif ltype == "SSH_AUTH":
        m = re.search(r'(?:for|user)\s+(\S+)', line, re.I)
        if m: fields["username"] = m.group(1)
        m = re.search(r'from\s+([\d.]+)', line, re.I)
        if m: fields["src_ip"] = m.group(1)
        m = re.search(r'port\s+(\d+)', line, re.I)
        if m: fields["src_port"] = m.group(1)
        fields["event"] = ("AUTH_FAILURE" if re.search(r'failed|invalid', line, re.I)
                           else "AUTH_SUCCESS" if re.search(r'accepted', line, re.I) else "SSH_EVENT")
    elif ltype == "WEB_ACCESS":
        m = re.search(r'"?(GET|POST|PUT|DELETE|PATCH|HEAD)\s+(\S+)', line, re.I)
        if m: fields["http_method"] = m.group(1); fields["uri"] = m.group(2)
        m = re.search(r'\s(\d{3})\s', line)
        if m: fields["status_code"] = m.group(1)
    elif ltype == "PRIVILEGE_ESCALATION":
        m = re.search(r'sudo:\s+(\S+)', line, re.I)
        if m: fields["username"] = m.group(1)
        fields["event"] = "PRIVILEGE_ESCALATION"
    elif ltype == "AUTH_FAILURE":
        m = re.search(r'user[=:\s]+(\S+)', line, re.I)
        if m: fields["username"] = m.group(1)
        fields["src_ip"] = ips[0] if ips else None
        fields["event"]  = "AUTHENTICATION_FAILURE"
    elif ltype == "FAIL2BAN":
        m = re.search(r'Ban\s+([\d.]+)', line)
        if m: fields["src_ip"] = m.group(1)
        fields["event"] = "IP_BANNED"
    if ips and not fields["src_ip"]:
        fields["src_ip"] = ips[0]
    return fields

# ═══════════════════════════════════════════════════════════════════
#  INCIDENT CORRELATOR
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
#  CORE RULESET — 20 reguł detekcji (bez ML, regex+liczniki)
# ═══════════════════════════════════════════════════════════════════
DETECTION_RULES = [
    {"id":"R001","name":"SSH Brute Force","mitre":"T1110","severity":"HIGH","nis2":True,
     "pattern":r"failed password|invalid user|authentication failure","log_type":"SSH_AUTH",
     "threshold":5,"group_by":"src_ip","nis2_category":"Authentication",
     "remediation":"Zablokuj IP (ufw deny), włącz fail2ban, ogranicz SSH do kluczy publicznych"},
    {"id":"R002","name":"RDP Brute Force","mitre":"T1110","severity":"HIGH","nis2":True,
     "pattern":r"rdp|3389|remote desktop|logon failure","threshold":5,"group_by":"src_ip",
     "nis2_category":"Authentication",
     "remediation":"Wyłącz RDP jeśli zbędny, wymuś VPN+NLA, ogranicz dostęp po IP"},
    {"id":"R003","name":"WordPress Admin Brute Force","mitre":"T1110","severity":"HIGH","nis2":True,
     "pattern":r"wp-admin|wp-login\.php|xmlrpc\.php","threshold":10,"group_by":"src_ip",
     "nis2_category":"Web Application",
     "remediation":"Ogranicz wp-admin po IP, zainstaluj WAF, wymuś 2FA na koncie admin"},
    {"id":"R004","name":"Root Login via SSH","mitre":"T1078","severity":"CRITICAL","nis2":True,
     "pattern":r"accepted.*for root|logged in as root","threshold":1,"group_by":"src_ip",
     "nis2_category":"Privilege Management",
     "remediation":"Wyłącz PermitRootLogin w sshd_config, używaj sudo z kont osobistych"},
    {"id":"R005","name":"Udane logowanie po serii nieudanych","mitre":"T1078","severity":"CRITICAL","nis2":True,
     "pattern":r"accepted (password|publickey)","threshold":1,"group_by":"src_ip",
     "nis2_category":"Authentication",
     "remediation":"Natychmiast zresetuj hasło, sprawdź aktywne sesje, przejrzyj logi po zalogowaniu"},
    {"id":"R006","name":"Port Scan Detected","mitre":"T1046","severity":"MEDIUM","nis2":True,
     "pattern":r"nmap|masscan|zmap|portscan|et scan|nse script","threshold":1,"group_by":"src_ip",
     "nis2_category":"Network Security",
     "remediation":"Zablokuj skanujące IP, sprawdź czy to autoryzowane testy penetracyjne"},
    {"id":"R007","name":"Firewall Block Spike","mitre":"T1046","severity":"MEDIUM","nis2":False,
     "pattern":r"ufw block|iptables.*drop|firewall.*deny","threshold":20,"group_by":"src_ip",
     "nis2_category":"Network Security",
     "remediation":"Dodaj IP do blacklisty, sprawdź czy to część szerszego ataku"},
    {"id":"R008","name":"Sudo Command Execution","mitre":"T1548","severity":"MEDIUM","nis2":True,
     "pattern":r"sudo:.*command=","threshold":1,"group_by":"username",
     "nis2_category":"Privilege Management",
     "remediation":"Sprawdź czy komenda była autoryzowana, przejrzyj uprawnienia sudo"},
    {"id":"R009","name":"Niebezpieczne uprawnienia (chmod 777)","mitre":"T1548","severity":"HIGH","nis2":True,
     "pattern":r"chmod\s+(777|4777|7777|\+s)|setuid|suid","threshold":1,"group_by":"username",
     "nis2_category":"System Integrity",
     "remediation":"Natychmiast przywróć poprawne uprawnienia, sprawdź co zmodyfikowano"},
    {"id":"R010","name":"Dostęp do wrażliwych plików","mitre":"T1003","severity":"HIGH","nis2":True,
     "pattern":r"/etc/shadow|/etc/passwd|/etc/sudoers|/root/\.ssh|lsass|secretsdump","threshold":1,"group_by":"username",
     "nis2_category":"Data Protection",
     "remediation":"Zbadaj cel dostępu, sprawdź czy dane nie zostały skopiowane"},
    {"id":"R011","name":"Modyfikacja Crontab","mitre":"T1505","severity":"HIGH","nis2":True,
     "pattern":r"crontab -[ei]|/etc/cron|/var/spool/cron|at\s+now","threshold":1,"group_by":"username",
     "nis2_category":"System Integrity",
     "remediation":"Sprawdź crontab: crontab -l -u <user>, usuń podejrzane wpisy"},
    {"id":"R012","name":"Nowe konto użytkownika","mitre":"T1136","severity":"HIGH","nis2":True,
     "pattern":r"useradd|adduser|net user.*\/add|new user.*created","threshold":1,"group_by":"username",
     "nis2_category":"Account Management",
     "remediation":"Zweryfikuj czy konto było autoryzowane, usuń jeśli nieznane"},
    {"id":"R013","name":"Pobieranie pliku z Internetu","mitre":"T1041","severity":"CRITICAL","nis2":True,
     "pattern":r"wget\s+http|curl\s+http|curl\s+-O|powershell.*downloadfile|invoke-webrequest","threshold":1,"group_by":"src_ip",
     "nis2_category":"Malware",
     "remediation":"Natychmiast odizoluj system, sprawdź pobrany plik, skanuj AV"},
    {"id":"R014","name":"Wykonanie z /tmp lub /dev/shm","mitre":"T1059","severity":"HIGH","nis2":True,
     "pattern":r"(?:/tmp/|/dev/shm/).{0,50}\.(sh|py|pl|exe|ps1|bat)","threshold":1,"group_by":"username",
     "nis2_category":"Malware",
     "remediation":"Sprawdź plik, wyizoluj system, przeskanuj pamięć"},
    {"id":"R015","name":"Reverse Shell Indicators","mitre":"T1059","severity":"CRITICAL","nis2":True,
     "pattern":r"bash\s+-i|nc\s+-[el]|/dev/tcp|mkfifo|python.*socket|ncat\s+-","threshold":1,"group_by":"src_ip",
     "nis2_category":"Intrusion",
     "remediation":"NATYCHMIAST odizoluj od sieci, zbierz logi pamięci, powiadom zespół"},
    {"id":"R016","name":"SQL Injection","mitre":"T1190","severity":"HIGH","nis2":True,
     "pattern":r"(?:select|union|insert|drop).*(?:from|where|table)|'.*or.*'.*=|--\s*$","threshold":1,"group_by":"src_ip",
     "nis2_category":"Web Application",
     "remediation":"Zablokuj IP, sprawdź logi aplikacji, zaktualizuj WAF rules"},
    {"id":"R017","name":"Path Traversal","mitre":"T1190","severity":"HIGH","nis2":True,
     "pattern":r"\.\./\.\./|%2e%2e%2f|%252e%252e|\.\.\\ ","threshold":1,"group_by":"src_ip",
     "nis2_category":"Web Application",
     "remediation":"Sprawdź co było celem, zaktualizuj konfigurację serwera web"},
    {"id":"R018","name":"Duży transfer danych","mitre":"T1041","severity":"HIGH","nis2":True,
     "pattern":r"bytes.*[0-9]{7,}|sent\s+[0-9]{7,}","threshold":1,"group_by":"src_ip",
     "nis2_category":"Data Exfiltration",
     "remediation":"Sprawdź cel transferu, zablokuj połączenie jeśli podejrzane"},
    {"id":"R019","name":"Czyszczenie logów","mitre":"T1070","severity":"CRITICAL","nis2":True,
     "pattern":r"rm\s+-rf.*log|truncate.*log|history\s+-c|clearev|wevtutil.*cl","threshold":1,"group_by":"username",
     "nis2_category":"Forensics",
     "remediation":"NATYCHMIAST zabezpiecz kopię logów, zbadaj incydent"},
    {"id":"R020","name":"Wyłączenie narzędzi bezpieczeństwa","mitre":"T1562","severity":"CRITICAL","nis2":True,
     "pattern":r"ufw\s+disable|systemctl\s+stop\s+(ufw|fail2ban|auditd|firewalld)|setenforce\s+0","threshold":1,"group_by":"username",
     "nis2_category":"Security Controls",
     "remediation":"Natychmiast włącz narzędzia, zbadaj kto i dlaczego je wyłączył"},
]
_rule_patterns = {r["id"]: re.compile(r["pattern"], re.IGNORECASE) for r in DETECTION_RULES}

def run_ruleset(entries: List[Dict], session_id: str = "DEMO") -> List[Dict]:
    """Evaluate 20 detection rules against parsed log entries."""
    from collections import Counter
    alerts = []
    now    = datetime.datetime.utcnow().isoformat()
    for rule in DETECTION_RULES:
        pat      = _rule_patterns[rule["id"]]
        group_by = rule.get("group_by","src_ip")
        thr      = rule.get("threshold",1)
        groups: Dict[str, list] = defaultdict(list)
        for e in entries:
            if pat.search(e.get("raw","")):
                key = e.get(group_by,"unknown") or "unknown"
                groups[key].append(e)
        for key, matched in groups.items():
            if len(matched) >= thr:
                alerts.append({
                    "rule_id":     rule["id"],
                    "rule_name":   rule["name"],
                    "mitre_id":    rule["mitre"],
                    "severity":    rule["severity"],
                    "nis2":        rule.get("nis2",False),
                    "nis2_category": rule.get("nis2_category",""),
                    "group_key":   key,
                    "group_by":    group_by,
                    "count":       len(matched),
                    "remediation": rule["remediation"],
                    "timeline":    [{"ts":(e.get("timestamp") or {}).get("iso",""),"raw":e.get("raw","")[:100]} for e in matched[:5]],
                    "session_id":  session_id,
                    "triggered_at":now,
                })
    return alerts

# ── NIS2 significance classifier ──────────────────────────────────
NIS2_CRITERIA = {
    "disruption_of_service":  {"weight":30,"kw":["outage","unavailable","ddos","denial"]},
    "data_breach":            {"weight":35,"kw":["exfil","leak","breach","stolen","export"]},
    "ransomware":             {"weight":40,"kw":["ransom","encrypt","locked",".enc","bitcoin"]},
    "unauthorized_access":    {"weight":25,"kw":["accepted","login success","authenticated"]},
    "persistence_installed":  {"weight":20,"kw":["crontab","systemctl enable","startup","autorun"]},
    "security_tool_disabled": {"weight":20,"kw":["ufw disable","setenforce 0","av disabled"]},
    "privilege_escalation":   {"weight":25,"kw":["chmod 777","sudo","root login","suid"]},
    "data_exfiltration":      {"weight":30,"kw":["wget http","curl http","large transfer","bytes sent"]},
}

def classify_nis2(alerts: List[Dict], entries: List[Dict]) -> Dict:
    """Determine NIS2 Art.23 significance and reporting obligations."""
    score   = 0; factors = []
    combined = " ".join(e.get("raw","").lower() for e in entries)
    combined += " ".join(a.get("rule_name","").lower() for a in alerts)
    for criterion, info in NIS2_CRITERIA.items():
        if any(kw in combined for kw in info["kw"]):
            score += info["weight"]
            factors.append(criterion.replace("_"," ").title())
    score += len([a for a in alerts if a.get("severity")=="CRITICAL"]) * 10
    score += len([a for a in alerts if a.get("nis2")]) * 5
    score  = min(score, 100)
    return {
        "score": score, "significant": score>=50, "reporting_required": score>=40,
        "factors": factors,
        "early_warning_24h": score>=50,
        "notification_72h":  score>=40,
        "final_report_1m":   score>=50,
        "classification": (
            "POWAŻNY INCYDENT — wczesne ostrzeżenie do CSIRT w ciągu 24h" if score>=50 else
            "INCYDENT — zgłoszenie do CSIRT w ciągu 72h" if score>=40 else
            "ZDARZENIE — dokumentuj, brak obowiązku raportowania"
        ),
        "csirt_contact": "incydent@cert.pl | +48 22 38 08 274",
    }

# ── Art.21 assessment from logs ───────────────────────────────────
ART21_REQS = [
    {"id":"21.2.a","name":"Polityki bezpieczeństwa IT","weight":10,"questions":["Czy posiadasz pisemną politykę bezpieczeństwa IT?","Czy polityka jest aktualizowana co roku?"]},
    {"id":"21.2.b","name":"Zarządzanie ryzykiem","weight":10,"questions":["Czy regularnie oceniasz ryzyko cyberbezpieczeństwa?","Czy posiadasz rejestr ryzyk?"]},
    {"id":"21.2.c","name":"Ciągłość działania (BCP/DRP)","weight":10,"questions":["Czy posiadasz plan ciągłości działania?","Czy wykonujesz i testujesz kopie zapasowe?"]},
    {"id":"21.2.d","name":"Bezpieczeństwo łańcucha dostaw","weight":8,"questions":["Czy oceniasz bezpieczeństwo dostawców IT?","Czy umowy zawierają klauzule bezpieczeństwa?"]},
    {"id":"21.2.e","name":"Bezpieczeństwo w pozyskiwaniu systemów","weight":8,"questions":["Czy sprawdzasz bezpieczeństwo przed wdrożeniem systemu?","Czy stosujesz zasadę minimalnych uprawnień?"]},
    {"id":"21.2.f","name":"Zarządzanie podatnościami","weight":10,"questions":["Czy regularnie aktualizujesz systemy?","Czy skanujesz podatności?"]},
    {"id":"21.2.g","name":"Ocena skuteczności zabezpieczeń","weight":8,"questions":["Czy przeprowadzasz audyty bezpieczeństwa?","Czy stosujesz testy penetracyjne?"]},
    {"id":"21.2.h","name":"Cyberhigiena i szkolenia (MFA)","weight":12,"questions":["Czy stosujesz MFA?","Czy pracownicy przechodzą szkolenia?","Czy masz politykę silnych haseł?"]},
    {"id":"21.2.i","name":"Kryptografia i szyfrowanie","weight":8,"questions":["Czy szyfrujesz dane wrażliwe?","Czy komunikacja jest szyfrowana (TLS/HTTPS)?"]},
    {"id":"21.2.j","name":"Bezpieczeństwo zasobów ludzkich","weight":8,"questions":["Czy weryfikujesz pracowników przed przyznaniem dostępu?","Czy szybko odbierasz dostęp odchodzącym pracownikom?"]},
]

def assess_art21(quiz_answers: Dict[str, int], alerts: List[Dict]) -> Dict:
    """
    quiz_answers: {req_id: score_0_100}  (from UI quiz or auto-assessed)
    alerts: from run_ruleset()
    """
    alert_cats = {a.get("nis2_category","") for a in alerts}
    results = []; total_w = 0; max_w = 0
    for req in ART21_REQS:
        max_w += req["weight"]
        score = quiz_answers.get(req["id"], 50)
        findings = []
        # Deduct from alert evidence
        if req["id"]=="21.2.h" and "Authentication" in alert_cats:
            score = min(score, 60); findings.append("Wykryto ataki na uwierzytelnianie — sprawdź MFA")
        if req["id"]=="21.2.f" and "Web Application" in alert_cats:
            score = min(score, 65); findings.append("Ataki na aplikację — sprawdź aktualność oprogramowania")
        if req["id"]=="21.2.c" and any(a["severity"]=="CRITICAL" for a in alerts):
            findings.append("Krytyczne alerty — przetestuj plan odtworzenia")
        if req["id"]=="21.2.g" and "Forensics" in alert_cats:
            score = min(score, 50); findings.append("Wykryto czyszczenie logów — brak ciągłości dowodów")
        score = max(0, min(100, score))
        total_w += (score/100)*req["weight"]
        results.append({"id":req["id"],"name":req["name"],"score":score,"weight":req["weight"],
                        "findings":findings,"questions":req["questions"],
                        "status":"✓" if score>=70 else "⚠" if score>=40 else "✗"})
    overall = round((total_w/max_w)*100) if max_w else 0
    return {
        "overall": overall, "requirements": results,
        "label": ("Wysoka zgodność" if overall>=75 else "Częściowa zgodność" if overall>=50 else "Niska zgodność — pilne działania"),
        "ksc_note": "KSC (Ustawa z dn. 5.07.2018 o krajowym systemie cyberbezpieczeństwa) — implementacja NIS2 w Polsce",
    }

def correlate_incidents(session_id: str, parsed: List[Dict]) -> List[Dict]:
    ip_groups: Dict[str, List[Dict]] = defaultdict(list)
    for e in parsed:
        if e.get("src_ip"): ip_groups[e["src_ip"]].append(e)
    incidents = []
    chain_patterns = [
        (["IDS_IPS","SSH_AUTH"],                          "Recon → Auth Attack",       30),
        (["IDS_IPS","AUTH_FAILURE","SSH_AUTH"],           "Recon → Brute Force → Auth",55),
        (["AUTH_FAILURE","PRIVILEGE_ESCALATION"],         "Brute Force → Privesc",     65),
        (["IDS_IPS","AUTH_FAILURE","PRIVILEGE_ESCALATION"],"Full Attack Chain",         90),
        (["FIREWALL_UFW","AUTH_FAILURE"],                 "Firewall Bypass Attempt",   40),
        (["SSH_AUTH","PRIVILEGE_ESCALATION"],             "Auth Success → Privesc",    70),
    ]
    for ip, entries in ip_groups.items():
        if len(entries) < 2: continue
        mitre_ids  = list({e["mitre_id"] for e in entries if e.get("mitre_id")})
        severities = [e["severity"] for e in entries]
        max_sev    = ("CRITICAL" if "CRITICAL" in severities else
                      "HIGH"     if "HIGH"     in severities else
                      "MEDIUM"   if "MEDIUM"   in severities else "LOW")
        log_types  = [e.get("log_type","") for e in entries]
        chain_name, chain_score = "Multi-Event Activity", 20.0
        for pat, name, score in chain_patterns:
            if all(p in log_types for p in pat):
                if score > chain_score: chain_name, chain_score = name, float(score)
        timeline = []
        for e in sorted(entries, key=lambda x: (x.get("timestamp") or {}).get("iso","") or ""):
            timeline.append({
                "ts": (e.get("timestamp") or {}).get("iso",""),
                "log_type": e.get("log_type",""), "event": e.get("event",""),
                "mitre": e.get("mitre_id",""), "severity": e.get("severity",""),
                "raw": e.get("raw","")[:80]
            })
        risk = min(chain_score + len(entries)*2 + len(mitre_ids)*5, 100.0)
        incidents.append({
            "session_id": session_id, "title": f"{chain_name} — {ip}",
            "severity": max_sev, "src_ip": ip,
            "mitre_ids": json.dumps(mitre_ids), "timeline": json.dumps(timeline),
            "risk_score": round(risk,1), "status": "open",
            "created_at": datetime.datetime.utcnow().isoformat(),
        })
    if incidents:
        conn = get_db()
        for inc in incidents:
            conn.execute("""INSERT INTO incidents
                (session_id,title,severity,src_ip,mitre_ids,timeline,risk_score,status,created_at)
                VALUES (:session_id,:title,:severity,:src_ip,:mitre_ids,:timeline,:risk_score,:status,:created_at)""", inc)
        conn.commit(); conn.close()
    return incidents

# ═══════════════════════════════════════════════════════════════════
#  UEBA
# ═══════════════════════════════════════════════════════════════════
UEBA_DEFAULTS = {
    "admin":         {"usual_country":"PL","usual_hour_start":8,"usual_hour_end":18,"usual_ips":"[]"},
    "root":          {"usual_country":"PL","usual_hour_start":9,"usual_hour_end":17,"usual_ips":"[]"},
    "administrator": {"usual_country":"PL","usual_hour_start":8,"usual_hour_end":18,"usual_ips":"[]"},
}

def ueba_analyze(username: str, src_ip: str, hour: int, country: str = "PL") -> Dict:
    conn = get_db()
    row  = conn.execute("SELECT * FROM ueba_baselines WHERE username=?", (username,)).fetchone()
    conn.close()
    defaults = (dict(row) if row else UEBA_DEFAULTS.get(username,
        {"usual_country":"PL","usual_hour_start":8,"usual_hour_end":18,"usual_ips":"[]"}))
    risk = 0.0; anomalies = []
    h_s = defaults.get("usual_hour_start",8); h_e = defaults.get("usual_hour_end",18)
    uc  = defaults.get("usual_country","PL")
    if not (h_s <= hour <= h_e):
        risk += 35.0; anomalies.append(f"Login o {hour}:00 poza oknem ({h_s}:00-{h_e}:00)")
    if country != uc:
        risk += 45.0; anomalies.append(f"Kraj: {country} (oczekiwany: {uc})")
    if hour < 5:
        risk += 15.0; anomalies.append("Logowanie w nocy (0:00-5:00)")
    risk = min(risk, 100.0)
    level = ("CRITICAL" if risk>=80 else "HIGH" if risk>=50 else "MEDIUM" if risk>=25 else "LOW")
    return {"username":username,"risk_score":round(risk,1),"risk_level":level,
            "anomalies":anomalies,"hour":hour,"src_ip":src_ip,"country":country}

# ═══════════════════════════════════════════════════════════════════
#  IP REPUTATION
# ═══════════════════════════════════════════════════════════════════
DEMO_IP_INTEL = {
    "198.51.100":{"country":"US","isp":"TEST-NET-3","abuse_score":85,"is_vpn":0,"is_tor":0},
    "203.0.113": {"country":"CN","isp":"CHINANET","abuse_score":72,"is_vpn":1,"is_tor":0},
    "45.33.32":  {"country":"US","isp":"Linode","abuse_score":65,"is_vpn":0,"is_tor":0},
    "10.0.0":    {"country":"PL","isp":"Private LAN","abuse_score":0,"is_vpn":0,"is_tor":0},
    "192.168.":  {"country":"PL","isp":"Private LAN","abuse_score":0,"is_vpn":0,"is_tor":0},
}

def lookup_ip_reputation(ip: str) -> Dict:
    conn = get_db()
    cached = conn.execute("SELECT * FROM ip_reputation WHERE ip=?", (ip,)).fetchone()
    conn.close()
    if cached:
        age = (datetime.datetime.utcnow() - datetime.datetime.fromisoformat(cached["checked_at"])).seconds
        if age < 7200: return dict(cached)
    result = None
    if ABUSEIPDB_KEY and REQUESTS_OK:
        try:
            r = req_lib.get("https://api.abuseipdb.com/api/v2/check",
                headers={"Key":ABUSEIPDB_KEY,"Accept":"application/json"},
                params={"ipAddress":ip,"maxAgeInDays":90},timeout=5)
            if r.status_code == 200:
                d = r.json().get("data",{})
                result = {"ip":ip,"country":d.get("countryCode","??"),"isp":d.get("isp","?"),
                          "abuse_score":d.get("abuseConfidenceScore",0),"is_vpn":0,"is_tor":0,
                          "source":"AbuseIPDB","checked_at":datetime.datetime.utcnow().isoformat()}
        except: pass
    if not result:
        p3 = ".".join(ip.split(".")[:3]); p2 = ".".join(ip.split(".")[:2])
        info = DEMO_IP_INTEL.get(p3) or DEMO_IP_INTEL.get(p2) or \
               {"country":"??","isp":"Unknown","abuse_score":random.randint(0,30),"is_vpn":0,"is_tor":0}
        result = {"ip":ip,**info,"source":"local_intel","checked_at":datetime.datetime.utcnow().isoformat()}
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO ip_reputation (ip,country,isp,abuse_score,is_vpn,is_tor,source,checked_at) VALUES (?,?,?,?,?,?,?,?)",
                 (result["ip"],result["country"],result["isp"],result["abuse_score"],
                  result["is_vpn"],result["is_tor"],result["source"],result["checked_at"]))
    conn.commit(); conn.close()
    return result

# ═══════════════════════════════════════════════════════════════════
#  AI ENGINE — Ollama + RAG
# ═══════════════════════════════════════════════════════════════════
def build_soc_system_prompt() -> str:
    return """Jesteś SENTRASEC v2.0 LOCAL — zaawansowanym asystentem AI Security Operations Center (SOC).
Działasz w trybie w pełni offline na lokalnym modelu LLM przez Ollama.

Twoje zadania:
- Analiza logów systemowych, sieciowych, aplikacyjnych
- Mapowanie na framework MITRE ATT&CK (podawaj ID technik np. T1110 Brute Force)
- Korelacja zdarzeń i budowanie osi czasu ataku (Timeline/Attack Storytelling)
- Ocena ryzyka: CRITICAL / HIGH / MEDIUM / LOW / INFO
- Rekomendacje naprawcze (Remediation) i playbooki SOAR
- Analiza UEBA — anomalie zachowań użytkowników
- Raporty compliance: NIST CSF, ISO 27001, PCI DSS, GDPR

Format odpowiedzi:
- Odpowiadaj w języku polskim, profesjonalnie i strukturyzowanie
- Używaj **bold** dla kluczowych informacji
- Używaj `code` dla IP, komend, hashów, ścieżek
- Dla zagrożeń: Severity | MITRE ID | Opis | Zalecenie
- Łącz zdarzenia w narrację "historii ataku"

Bądź konkretny i zwięzły. Nie wymyślaj faktów — analizuj tylko dostarczone dane."""

def ask_ai(session_id: str, user_message: str, log_data: str = "",
           parsed_entries: List[Dict] = None, stream: bool = False):
    """Wywołuje lokalny Ollama LLM z kontekstem RAG."""

    # 1. Pobierz historię czatu z SQLite
    conn = get_db()
    history = conn.execute(
        "SELECT role,content FROM chat_history WHERE session_id=? ORDER BY id DESC LIMIT 8",
        (session_id,)).fetchall()
    parsed_count = conn.execute(
        "SELECT COUNT(*) FROM log_entries WHERE session_id=?", (session_id,)).fetchone()[0]
    inc_count = conn.execute(
        "SELECT COUNT(*) FROM incidents WHERE session_id=?", (session_id,)).fetchone()[0]
    conn.close()

    # 2. RAG — pobierz pasującą wiedzę SOC
    rag_query   = user_message + " " + (log_data[:200] if log_data else "")
    rag_docs    = rag_engine.retrieve(rag_query, n=4)
    rag_context = "\n\n".join([f"[WIEDZA SOC]\n{d['text']}" for d in rag_docs])

    # 3. Zbuduj wiadomość z kontekstem
    content = user_message
    if log_data:
        content += f"\n\n=== DANE LOGÓW DO ANALIZY ===\n{log_data[:4000]}\n=== KONIEC LOGÓW ==="
    if parsed_entries:
        summary = json.dumps(parsed_entries[:8], indent=2, ensure_ascii=False, default=str)
        content += f"\n\n=== SPARSOWANE POLA (pierwsze 8) ===\n{summary}"
    if rag_context:
        content += f"\n\n=== KONTEKST WIEDZY SOC (RAG) ===\n{rag_context}\n=== KONIEC RAG ==="
    content += f"\n\n[Sesja: {session_id} | Logi: {parsed_count} | Incydenty: {inc_count}]"

    # 4. Historia konwersacji
    messages = [{"role": r["role"], "content": r["content"]} for r in reversed(history)]
    messages.append({"role": "user", "content": content})

    system = build_soc_system_prompt()

    # 5. Wywołaj Ollama
    now = datetime.datetime.utcnow().isoformat()
    if stream:
        def gen():
            full = ""
            gen_stream = ollama_chat(messages, system=system, stream=True)
            for chunk in gen_stream:
                full += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            # Zapisz do DB
            c = get_db()
            c.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                      (session_id,"user",user_message,now))
            c.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                      (session_id,"assistant",full,now))
            c.commit(); c.close()
            yield f"data: {json.dumps({'done': True})}\n\n"
        return gen()
    else:
        answer = ollama_chat(messages, system=system, stream=False)
        c = get_db()
        c.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                  (session_id,"user",user_message,now))
        c.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                  (session_id,"assistant",answer,now))
        c.commit(); c.close()
        return answer

# ═══════════════════════════════════════════════════════════════════
#  PLAYBOOKS SOAR
# ═══════════════════════════════════════════════════════════════════
def run_playbook(session_id: str, action: str, target: str) -> Dict:
    now = datetime.datetime.utcnow().isoformat()
    commands = {
        "BLOCK_IP":     f"sudo ufw deny from {target} to any comment 'SENTRASEC-BLOCK'",
        "ALLOW_IP":     f"sudo ufw delete deny from {target}",
        "ISOLATE_HOST": f"sudo iptables -I FORWARD -s {target} -j DROP && sudo iptables -I FORWARD -d {target} -j DROP",
        "SCAN_IP":      f"nmap -sV --script vuln {target} -oN /tmp/sentrasec_scan_{target}.txt",
        "DUMP_CONNS":   f"ss -tnp | grep {target}",
        "KILL_SESSION": f"who | grep {target} | awk '{{print $2}}' | xargs pkill -t",
        "THREAT_INTEL": f"whois {target} | grep -E 'country|org|netname|abuse' | head -10",
    }
    cmd = commands.get(action, f"echo 'Unknown: {action}'")
    demo_results = {
        "BLOCK_IP":     f"[OK] Reguła #{random.randint(100,999)}: DENY {target}",
        "ALLOW_IP":     f"[OK] Reguła usunięta dla {target}",
        "ISOLATE_HOST": f"[OK] {target} izolowany — 2 reguły iptables DROP",
        "SCAN_IP":      f"[DEMO] Skan zakolejkowany → /tmp/sentrasec_scan_{target}.txt",
        "DUMP_CONNS":   f"[DEMO] 3 aktywne połączenia z {target}",
        "KILL_SESSION": f"[OK] Sesje z {target} zakończone",
        "THREAT_INTEL": f"[DEMO] Country: US | ISP: Linode | Abuse reports: 142",
    }
    result = demo_results.get(action, "[DEMO] Komenda staged")
    conn = get_db()
    conn.execute("INSERT INTO playbook_runs (session_id,action,target,command,result,executed_at) VALUES (?,?,?,?,?,?)",
                 (session_id,action,target,cmd,result,now))
    conn.commit(); conn.close()
    return {"action":action,"target":target,"command":cmd,"result":result,"executed":now,
            "mode":"DEMO — wymaga flagi --live do rzeczywistego wykonania"}

# ═══════════════════════════════════════════════════════════════════
#  REPORT GENERATOR — wieloformatowy
# ═══════════════════════════════════════════════════════════════════
def generate_report(session_id: str, fmt: str, standard: str = "all") -> Dict:
    conn  = get_db()
    logs  = conn.execute("SELECT * FROM log_entries WHERE session_id=?", (session_id,)).fetchall()
    incs  = conn.execute("SELECT * FROM incidents WHERE session_id=?",   (session_id,)).fetchall()
    conn.close()
    ts    = datetime.datetime.utcnow().isoformat()
    sev_c = defaultdict(int); ips = set(); mitre = set(); ltypes = set()
    for l in logs:
        sev_c[l["severity"]] += 1
        if l["src_ip"]:   ips.add(l["src_ip"])
        if l["mitre_id"]: mitre.add(l["mitre_id"])
        if l["log_type"]: ltypes.add(l["log_type"])

    # Compliance scores zależne od znalezionych zagrożeń
    crit = sev_c.get("CRITICAL",0); hi = sev_c.get("HIGH",0)
    comp = {
        "NIST CSF":  max(20, 85 - crit*10 - hi*3),
        "ISO 27001": max(20, 80 - crit*8  - hi*2),
        "PCI DSS":   max(20, 90 - crit*12 - hi*4),
        "GDPR":      max(20, 75 - crit*8  - hi*3),
        "MITRE ATT&CK Coverage": max(10, 70 - len(mitre)*5),
    }

    meta = {
        "title":    f"SENTRASEC v2.0 LOCAL — Security Operations Report ({standard.upper()})",
        "generated": ts, "session_id": session_id,
        "log_count": len(logs), "incident_count": len(incs),
        "severity_counts": dict(sev_c), "unique_ips": sorted(ips),
        "mitre_ids": sorted(mitre), "log_types": sorted(ltypes),
        "compliance": comp, "incidents": [dict(i) for i in incs],
        "model": OLLAMA_MODEL, "mode": "LOCAL (Offline)",
    }

    if fmt == "json":
        return {"content": json.dumps(meta, indent=2, ensure_ascii=False),
                "mime": "application/json", "ext": "json"}

    if fmt == "txt":
        sep = "=" * 72
        lines = [sep, "SENTRASEC v2.0 LOCAL — SECURITY OPERATIONS REPORT", sep,
                 f"Generated  : {ts}", f"Session    : {session_id}",
                 f"Model      : {OLLAMA_MODEL} (Offline)", f"Standard   : {standard.upper()}",
                 f"Logs       : {len(logs)} | Incidents: {len(incs)}", "-"*72,
                 "SEVERITY SUMMARY"]
        for s in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"]:
            lines.append(f"  {s:<12} : {sev_c.get(s,0)}")
        lines += ["-"*72, "COMPLIANCE SCORES"]
        for k,v in comp.items():
            bar = "█" * (v//10) + "░" * (10-v//10)
            status = "✓ OK" if v>=70 else "⚠ REVIEW" if v>=50 else "✗ FAIL"
            lines.append(f"  {k:<24} {bar} {v}% {status}")
        lines += ["-"*72, "MITRE ATT&CK TECHNIQUES"]
        for mid in sorted(mitre):
            info = MITRE_MAP.get(mid,{})
            lines.append(f"  {mid} — {info.get('name','?')} [{info.get('tactic','?')}]")
        lines += ["-"*72, "SOURCE IPs"]
        for ip in sorted(ips): lines.append(f"  {ip}")
        lines += ["-"*72, "INCIDENTS"]
        for inc in incs:
            lines.append(f"  [{inc['severity']}] {inc['title']} | Risk: {inc['risk_score']} | {inc['status']}")
        lines.append(sep)
        return {"content": "\n".join(lines), "mime": "text/plain", "ext": "txt"}

    if fmt == "html":
        def sev_badge(s):
            colors={"CRITICAL":"#ff2244","HIGH":"#ff6644","MEDIUM":"#ffaa00","LOW":"#00ff88","INFO":"#00aaff"}
            return f'<span style="color:{colors.get(s,"#ccc")};font-weight:bold;">{s}</span>'
        mitre_rows = "".join(
            f"<tr><td>{mid}</td><td>{MITRE_MAP.get(mid,{}).get('name','?')}</td>"
            f"<td>{MITRE_MAP.get(mid,{}).get('tactic','?')}</td></tr>" for mid in sorted(mitre))
        inc_rows = "".join(
            f"<tr><td>{sev_badge(i['severity'])}</td><td>{i['title']}</td>"
            f"<td>{i['risk_score']}</td><td>{i['status']}</td></tr>" for i in incs)
        comp_rows = "".join(
            f"<tr><td>{k}</td><td><div style='background:#1a2f45;border-radius:3px;height:6px;width:200px;'>"
            f"<div style='width:{v}%;background:{'#00ff88' if v>=70 else '#ffaa00' if v>=50 else '#ff2244'};height:100%;border-radius:3px;'></div>"
            f"</div></td><td>{v}%</td></tr>" for k,v in comp.items())
        html = f"""<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8">
<title>SENTRASEC v2.0 LOCAL — Report</title>
<style>
  body{{font-family:'Courier New',monospace;background:#050a0f;color:#c8dce8;padding:24px;line-height:1.7;}}
  h1{{color:#00d4ff;border-bottom:2px solid #00d4ff;padding-bottom:10px;letter-spacing:2px;}}
  h2{{color:#0099cc;margin-top:22px;font-size:14px;letter-spacing:1px;border-left:3px solid #0099cc;padding-left:10px;}}
  table{{border-collapse:collapse;width:100%;margin-bottom:14px;}}
  th{{background:#0a1825;color:#00d4ff;padding:7px 12px;text-align:left;font-size:11px;letter-spacing:1px;}}
  td{{border:1px solid #1a2f45;padding:5px 10px;font-size:12px;}}
  .badge{{display:inline-block;padding:2px 8px;border-radius:2px;font-size:10px;border:1px solid;}}
  .meta-row{{display:flex;gap:24px;flex-wrap:wrap;margin-bottom:16px;}}
  .meta-item{{background:#0a1422;border:1px solid #1a2f45;border-radius:3px;padding:8px 14px;}}
  .meta-label{{font-size:9px;color:#4a6a85;letter-spacing:1px;text-transform:uppercase;}}
  .meta-value{{font-size:16px;color:#00d4ff;font-weight:bold;}}
  footer{{color:#3a5a78;font-size:10px;margin-top:20px;border-top:1px solid #1a2f45;padding-top:8px;}}
</style></head><body>
<h1>⬡ SENTRASEC v2.0 LOCAL — Security Report</h1>
<div class="meta-row">
  <div class="meta-item"><div class="meta-label">Generated</div><div class="meta-value" style="font-size:11px;">{ts}</div></div>
  <div class="meta-item"><div class="meta-label">Session</div><div class="meta-value" style="font-size:13px;">{session_id}</div></div>
  <div class="meta-item"><div class="meta-label">Model</div><div class="meta-value" style="font-size:13px;">{OLLAMA_MODEL}</div></div>
  <div class="meta-item"><div class="meta-label">Logs</div><div class="meta-value">{len(logs)}</div></div>
  <div class="meta-item"><div class="meta-label">Incidents</div><div class="meta-value">{len(incs)}</div></div>
</div>
<h2>Event Severity Summary</h2>
<table><tr><th>Severity</th><th>Count</th></tr>
{"".join(f"<tr><td>{sev_badge(s)}</td><td>{sev_c.get(s,0)}</td></tr>" for s in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"])}
</table>
<h2>Compliance Scores</h2>
<table><tr><th>Framework</th><th>Progress</th><th>Score</th></tr>{comp_rows}</table>
<h2>MITRE ATT&CK Techniques Detected</h2>
<table><tr><th>ID</th><th>Technique</th><th>Tactic</th></tr>{mitre_rows if mitre_rows else "<tr><td colspan='3' style='color:#4a6a85;'>No MITRE techniques detected</td></tr>"}</table>
<h2>Source IP Addresses</h2>
<p>{" ".join(f'<span class="badge" style="color:#ff6644;border-color:#ff6644;">{ip}</span>' for ip in sorted(ips)) or '<span style="color:#4a6a85;">None</span>'}</p>
<h2>Incidents</h2>
<table><tr><th>Severity</th><th>Title</th><th>Risk Score</th><th>Status</th></tr>
{inc_rows if inc_rows else "<tr><td colspan='4' style='color:#4a6a85;'>No incidents correlated</td></tr>"}</table>
<footer>SENTRASEC v2.0 LOCAL — 100% Offline · Model: {OLLAMA_MODEL} · {ts}</footer>
</body></html>"""
        return {"content": html, "mime": "text/html", "ext": "html"}

    return {"content": json.dumps(meta, indent=2), "mime": "application/json", "ext": "json"}

# ═══════════════════════════════════════════════════════════════════
#  SSE — Live log stream (symulacja)
# ═══════════════════════════════════════════════════════════════════
STREAM_POOL = [
    ("INFO","auth","User login from 10.0.0.5 (admin) — OK"),
    ("INFO","httpd","GET /api/status 200 12ms"),
    ("WARN","firewall","[UFW BLOCK] IN=eth0 SRC=198.51.100.7 DST=10.0.0.1 DPT=22"),
    ("WARN","auth","Failed password for root from 198.51.100.7 port 54321 ssh2"),
    ("INFO","cron","Backup job completed successfully"),
    ("ERR","httpd","POST /api/login 429 rate-limited ip=198.51.100.7"),
    ("WARN","ids","Suricata: ET SCAN Nmap NSE scripts SRC=198.51.100.7"),
    ("INFO","vpn","OpenVPN tunnel: peer=10.8.0.2 AES-256-GCM"),
    ("CRIT","auth","Root login ACCEPTED from 198.51.100.7 — ANOMALY"),
    ("WARN","net","ARP spoofing detected on VLAN 10"),
    ("INFO","antivirus","Scan complete: 0 threats detected"),
    ("ERR","db","Connection timeout db01.internal:5432"),
    ("WARN","auth","7 consecutive failed logins: admin from 45.33.32.156"),
    ("INFO","dns","Query A: updates.internal.corp → 10.0.0.99"),
    ("WARN","fail2ban","Ban 198.51.100.7"),
    ("ERR","sudo","admin : TTY=pts/0 ; COMMAND=/bin/chmod 777 /etc/shadow"),
]
_stream_idx = 0

@app.route("/api/stream/logs")
def stream_logs():
    """SSE: demo stream when no real files tailed, real events when available."""
    global _stream_idx
    client_q: queue.Queue = queue.Queue(maxsize=200)
    with _ingest_lock:
        _ingest_sse_clients.append(client_q)

    def generate():
        last_demo = [0.0]
        try:
            while True:
                # Try real event first (non-blocking)
                try:
                    evt = client_q.get_nowait()
                    yield f"data: {json.dumps(evt)}\n\n"
                    continue
                except queue.Empty:
                    pass
                # If no real events, send demo event occasionally
                now = time.time()
                if now - last_demo[0] > random.uniform(0.9, 3.5):
                    ev = STREAM_POOL[_stream_idx % len(STREAM_POOL)]
                    _stream_idx += 1
                    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
                    data = {"ts": ts, "sev": ev[0], "src": ev[1], "msg": ev[2], "real": False}
                    yield f"data: {json.dumps(data)}\n\n"
                    last_demo[0] = now
                else:
                    time.sleep(0.1)
        except GeneratorExit:
            with _ingest_lock:
                try: _ingest_sse_clients.remove(client_q)
                except: pass

    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# ═══════════════════════════════════════════════════════════════════
#  REST API ROUTES
# ═══════════════════════════════════════════════════════════════════
@app.route("/api/session", methods=["POST"])
def create_session():
    sid = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:12].upper()
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO sessions (id,created_at,threat_level) VALUES (?,?,?)",
                 (sid, datetime.datetime.utcnow().isoformat(), "low"))
    conn.commit(); conn.close()
    return jsonify({"session_id": sid})

@app.route("/api/parse", methods=["POST"])
def parse_logs_route():
    data  = request.json or {}
    raw   = data.get("logs",""); sid = data.get("session_id","DEMO")
    lines  = [l for l in raw.split("\n") if l.strip()]
    parsed = [p for p in (parse_log_entry(l) for l in lines) if p]
    all_ips = list({e["src_ip"] for e in parsed if e.get("src_ip")})
    ip_intel = {ip: lookup_ip_reputation(ip) for ip in all_ips[:10]}
    # UEBA
    ueba_results = []
    for e in parsed:
        if e.get("username") and e.get("src_ip") and e.get("event") in ("AUTH_SUCCESS","AUTH_FAILURE"):
            hour = 12
            if e.get("timestamp") and e["timestamp"].get("iso"):
                try: hour = datetime.datetime.fromisoformat(e["timestamp"]["iso"]).hour
                except: pass
            country = ip_intel.get(e["src_ip"],{}).get("country","??")
            u = ueba_analyze(e["username"], e["src_ip"], hour, country)
            if u["risk_score"] > 0: ueba_results.append(u)
    incidents = correlate_incidents(sid, parsed)
    # RAG indexing
    for e in parsed:
        if e.get("mitre_id"):
            rag_engine.add_log_document(sid, e["raw"],
                {"severity": e["severity"], "category": "parsed_log", "mitre": e.get("mitre_id","")})
    # Save to DB
    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    for e in parsed:
        conn.execute("""INSERT INTO log_entries
            (session_id,raw,log_type,severity,timestamp_raw,timestamp_iso,src_ip,dst_ip,
             src_port,dst_port,username,event_type,mitre_id,mitre_name,inserted_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (sid, e["raw"], e["log_type"], e["severity"],
             (e.get("timestamp") or {}).get("raw"), (e.get("timestamp") or {}).get("iso"),
             e.get("src_ip"), e.get("dst_ip"), e.get("src_port"), e.get("dst_port"),
             e.get("username"), e.get("event"), e.get("mitre_id"), e.get("mitre_name"), now))
    conn.commit(); conn.close()
    return jsonify({"parsed":parsed,"count":len(parsed),"ip_intel":ip_intel,
                    "ueba":ueba_results,"incidents":incidents,
                    "mitre_ids":list({e["mitre_id"] for e in parsed if e.get("mitre_id")})})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    msg  = data.get("message","")
    sid  = data.get("session_id","DEMO")
    logs = data.get("log_data","")
    parsed = data.get("parsed_entries",[])
    do_stream = data.get("stream", False)
    if do_stream:
        gen = ask_ai(sid, msg, logs, parsed, stream=True)
        return Response(stream_with_context(gen), mimetype="text/event-stream",
                        headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
    answer = ask_ai(sid, msg, logs, parsed, stream=False)
    return jsonify({"response": answer})

@app.route("/api/chat/history")
def chat_history():
    sid  = request.args.get("session_id","DEMO")
    conn = get_db()
    rows = conn.execute("SELECT role,content,created_at FROM chat_history WHERE session_id=? ORDER BY id", (sid,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/incidents")
def get_incidents():
    sid  = request.args.get("session_id","DEMO")
    conn = get_db()
    rows = conn.execute("SELECT * FROM incidents WHERE session_id=? ORDER BY risk_score DESC", (sid,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r); d["timeline"]=json.loads(d["timeline"] or "[]"); d["mitre_ids"]=json.loads(d["mitre_ids"] or "[]")
        result.append(d)
    return jsonify(result)

@app.route("/api/playbook", methods=["POST"])
def playbook():
    data = request.json or {}
    return jsonify(run_playbook(data.get("session_id","DEMO"), data.get("action",""), data.get("target","")))

@app.route("/api/ip/reputation")
def ip_rep():
    ip = request.args.get("ip","")
    try: ipaddress.ip_address(ip)
    except: return jsonify({"error":"Invalid IP"}),400
    return jsonify(lookup_ip_reputation(ip))

@app.route("/api/report")
def report():
    sid = request.args.get("session_id","DEMO")
    fmt = request.args.get("format","html")
    std = request.args.get("standard","all")
    res = generate_report(sid, fmt, std)
    return Response(res["content"], mimetype=res["mime"],
                    headers={"Content-Disposition":f"attachment; filename=sentrasec-{sid}.{res['ext']}"})

@app.route("/api/report/nis2", methods=["POST"])
def report_nis2():
    """Generuje strukturyzowany raport NIS2 przez lokalny LLM."""
    data = request.json or {}
    sid  = data.get("session_id","DEMO")
    logs = data.get("logs","")

    conn = get_db()
    log_entries = conn.execute("SELECT * FROM log_entries WHERE session_id=? ORDER BY id", (sid,)).fetchall()
    incidents   = conn.execute("SELECT * FROM incidents WHERE session_id=? ORDER BY risk_score DESC", (sid,)).fetchall()
    conn.close()

    now_dt  = datetime.datetime.utcnow()
    ts      = now_dt.isoformat()
    report_id = f"SR-{now_dt.strftime('%Y%m%d-%H%M%S')}"
    mitre   = sorted({r["mitre_id"] for r in log_entries if r["mitre_id"]})
    sev_c   = defaultdict(int)
    ips     = set()
    log_types = set()
    usernames = set()
    for r in log_entries:
        sev_c[r["severity"]] += 1
        if r["src_ip"]:   ips.add(r["src_ip"])
        if r["log_type"]: log_types.add(r["log_type"])
        if r["username"]: usernames.add(r["username"])

    # Wykryj główny typ incydentu z logów
    log_sample = logs[:4000] if logs else "\n".join([r["raw"] for r in log_entries[:50]])
    inc_lines  = "\n".join([f"• [{i['severity']}] {i['title']} | Risk Score: {i['risk_score']}" for i in incidents[:10]])
    mitre_details = "\n".join([f"  - {m}: {MITRE_MAP.get(m,{}).get('name','?')} [{MITRE_MAP.get(m,{}).get('tactic','?')}]"
                                for m in mitre]) if mitre else "  Brak zmapowanych technik"
    crit_count = sev_c.get("CRITICAL",0)
    high_count = sev_c.get("HIGH",0)
    priority = ("KRYTYCZNY" if crit_count > 0 else
                "WYSOKI"    if high_count > 0 else
                "ŚREDNI"    if sev_c.get("MEDIUM",0) > 0 else "NISKI")

    # Określ główny typ incydentu
    ll = log_sample.lower()
    if "brute" in ll or "failed password" in ll:
        incident_type = "Brute Force / Credential Attack"
    elif "sqli" in ll or "sql injection" in ll or "select " in ll:
        incident_type = "SQL Injection"
    elif "nmap" in ll or "scan" in ll or "portscan" in ll:
        incident_type = "Network Reconnaissance / Port Scan"
    elif "webshell" in ll or "rce" in ll or "exploit" in ll:
        incident_type = "Remote Code Execution / Web Exploit"
    elif "sudo" in ll or "chmod" in ll or "privilege" in ll:
        incident_type = "Privilege Escalation"
    elif "ufw block" in ll or "iptables" in ll:
        incident_type = "Firewall Block / Network Attack"
    elif "ransomware" in ll or "encrypt" in ll:
        incident_type = "Ransomware"
    else:
        incident_type = "Cybersecurity Incident (Multi-vector)"

    # RAG context
    rag_docs = rag_engine.retrieve(
        f"NIS2 incydent {incident_type} raportowanie compliance art23", n=4)
    rag_ctx  = "\n".join([d["text"] for d in rag_docs])

    nis2_prompt = f"""Jesteś certyfikowanym analitykiem SOC i ekspertem NIS2. Sporządź KOMPLETNY, KONKRETNY raport zgodny z Dyrektywą NIS2 (UE) 2022/2555.

DANE TECHNICZNE INCYDENTU:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Report ID:      {report_id}
Typ incydentu:  {incident_type}
Priorytet:      {priority}
Wykryte CRITICAL: {crit_count} | HIGH: {high_count} | MEDIUM: {sev_c.get('MEDIUM',0)}
Atakujące IP:   {', '.join(sorted(ips)) or 'nieznane'}
Zaatakowane konta: {', '.join(sorted(usernames)) or 'nieznane'}
Typy logów:     {', '.join(sorted(log_types)) or 'różne'}

TECHNIKI MITRE ATT&CK:
{mitre_details}

SKORELOWANE INCYDENTY:
{inc_lines or '• Brak automatycznie skorelowanych incydentów'}

SUROWE LOGI (do analizy):
{log_sample}

DODATKOWA WIEDZA SOC:
{rag_ctx}
━━━━━━━━━━━━━━━━━━━━━━━━━━

Sporządź raport w poniższej strukturze. Każda sekcja musi być KONKRETNA i oparta na dostarczonych danych — nie pisz ogólników.

## 1. IDENTYFIKACJA INCYDENTU (Art. 23 NIS2)
Napisz:
- Precyzyjna klasyfikacja: czy to "znaczący incydent" wg Art. 23(3)? Uzasadnij kryteriami (liczba użytkowników, czas przestoju, straty finansowe, zasięg geograficzny).
- Dokładna data i czas pierwszego wykrycia z logów
- Dotknięte systemy i usługi (z nazw w logach)
- Wektor ataku krok po kroku

## 2. ANALIZA RAG — AI SECURITY INTELLIGENCE
Napisz:
- Szczegółowa analiza wzorców ataku wykrytych w logach
- Korelacja zdarzeń: oś czasu (timeline) od pierwszego do ostatniego zdarzenia
- Ocena stopnia zaawansowania atakującego (APT / opportunistic / script kiddie)
- Wskaźniki kompromitacji (IoC): IP, user-agenty, sygnatury

## 3. OCENA RYZYKA (Art. 21 NIS2)
Napisz:
- Wpływ na triada CIA: Dostępność / Poufność / Integralność (ocena 0-10 dla każdej)
- Zagrożone dane i aktywa (konkretne z logów)
- Szacunkowe ryzyko rezydualne po zastosowanych środkach
- Prawdopodobieństwo ponownego ataku (%)

## 4. ŚRODKI ZARZĄDZANIA RYZYKIEM (Art. 21(2) NIS2)
Napisz:
- Zastosowane środki natychmiastowe (co zrobiono)
- Wymagane środki techniczne (lista priorytetowa z terminami)
- Wymagane środki organizacyjne
- Szacunkowy koszt remediation

## 5. OBOWIĄZKI RAPORTOWANIA (Art. 23 NIS2)
Napisz:
- Decyzja: TAK/NIE — wymagane wczesne ostrzeżenie do CERT Polska (w 24h od wykrycia)?
- Decyzja: TAK/NIE — wymagane zgłoszenie incydentu (w 72h)?
- Decyzja: TAK/NIE — wymagany raport końcowy (1 miesiąc)?
- Organ właściwy: CERT Polska / UODO / KNF / inne
- Szkic treści powiadomienia (3-4 zdania gotowe do wysłania)

## 6. DOWODY FORENSIC
Napisz:
- Lista artefaktów do zabezpieczenia (logi, pcap, memory dump)
- Polecenia do wykonania w celu zabezpieczenia dowodów
- Integralność dowodów: rekomendacje hashowania
- Łańcuch dowodowy (chain of custody)

## 7. PLAN ODTWORZENIA (Art. 21(2)(c) NIS2)
Napisz:
- Harmonogram odtworzenia krok po kroku
- RTO (Recovery Time Objective): szacowany czas
- RPO (Recovery Point Objective): szacowany punkt
- Testy weryfikacyjne po odtworzeniu

## 8. PODSUMOWANIE WYKONAWCZE
Napisz 3-5 zdań dla zarządu: co się stało, jaka jest skala, co robić teraz. Bez żargonu technicznego.
Priorytet reakcji: {priority}

Pisz wyłącznie po polsku. Każda sekcja musi zawierać konkretne dane z logów — nie pisz "należy sprawdzić" bez podania co konkretnie."""

    messages = [{"role": "user", "content": nis2_prompt}]
    system   = ("Jesteś certyfikowanym ekspertem NIS2 i analitykiem SOC. "
                "Twoje raporty są używane jako oficjalna dokumentacja incydentów do organów regulacyjnych. "
                "Odpowiadaj WYŁĄCZNIE po polsku. Bądź konkretny, profesjonalny, operacyjny. "
                "Opieraj się TYLKO na dostarczonych danych z logów — nie wymyślaj faktów.")

    report_text = ollama_chat(messages, system=system, stream=False)

    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"user",f"[Raport NIS2 — {incident_type}]",now))
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"assistant",report_text,now))
    conn.commit(); conn.close()

    return jsonify({
        "report":         report_text,
        "session_id":     sid,
        "report_id":      report_id,
        "generated":      ts,
        "model":          OLLAMA_MODEL,
        "mitre":          mitre,
        "sev_counts":     dict(sev_c),
        "incident_count": len(incidents),
        "incident_type":  incident_type,
        "priority":       priority,
        "ips":            sorted(ips),
        "usernames":      sorted(usernames),
    })
@app.route("/api/stats")
def stats():
    sid  = request.args.get("session_id","DEMO")
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM log_entries WHERE session_id=?", (sid,)).fetchone()[0]
    crits = {s: conn.execute("SELECT COUNT(*) FROM log_entries WHERE session_id=? AND severity=?", (sid,s)).fetchone()[0]
             for s in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"]}
    inc_c = conn.execute("SELECT COUNT(*) FROM incidents WHERE session_id=?", (sid,)).fetchone()[0]
    conn.close()
    return jsonify({"total":total,"by_severity":crits,"incidents":inc_c})

@app.route("/api/ollama/test")
def ollama_test():
    """Endpoint diagnostyczny — testuje połączenie z Ollama step-by-step."""
    steps = []
    # Step 1: ping
    try:
        r = req_lib.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        ping_ok = r.status_code == 200
        steps.append({"step":"ping","ok":ping_ok,"detail":f"HTTP {r.status_code}"})
    except Exception as e:
        ping_ok = False
        steps.append({"step":"ping","ok":False,"detail":str(e)})
    # Step 2: models
    models = []
    if ping_ok:
        try:
            r2 = req_lib.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            raw = r2.json()
            models = [m["name"] for m in raw.get("models",[]) if "name" in m]
            steps.append({"step":"models","ok":True,"detail":f"Found: {models}"})
        except Exception as e:
            steps.append({"step":"models","ok":False,"detail":str(e)})
    # Step 3: model check (prefix match — "llama3" matches "llama3:latest")
    base = OLLAMA_MODEL.split(':')[0]
    model_found = any(m == OLLAMA_MODEL or m.startswith(base) for m in models)
    matched = next((m for m in models if m == OLLAMA_MODEL or m.startswith(base)), None)
    steps.append({"step":"model_check","ok":model_found,
                  "detail": f"'{OLLAMA_MODEL}' → używam '{matched}'" if model_found
                             else f"'{OLLAMA_MODEL}' NOT FOUND — run: ollama pull {OLLAMA_MODEL}"})
    return jsonify({"host": OLLAMA_HOST, "model": OLLAMA_MODEL,
                    "overall": ping_ok, "steps": steps, "models": models})
    return jsonify({"models": ollama_list_models(), "current": OLLAMA_MODEL,
                    "host": OLLAMA_HOST, "online": ollama_ping()})

@app.route("/api/ollama/set_model", methods=["POST"])
def set_model():
    global OLLAMA_MODEL
    data  = request.json or {}
    model = data.get("model","").strip()
    if not model: return jsonify({"error":"No model specified"}),400
    OLLAMA_MODEL = model
    return jsonify({"model": OLLAMA_MODEL, "status":"ok"})


# ═══════════════════════════════════════════════════════════════════
#  NEW API ROUTES — Ingest, Tailer, Search, Sessions, Tags
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/ingest", methods=["POST"])
@require_api_key
def ingest():
    """
    Real-time log ingestion endpoint.
    Accepts:
      - JSON: {"lines": [...], "session_id": "...", "source": "..."}
      - Plain text body (one log line per line)
      - Filebeat/Fluent Bit JSON events
    """
    sid    = request.args.get("session_id", request.json.get("session_id","GLOBAL") if request.is_json else "GLOBAL")
    source = request.args.get("source", "http_ingest")
    count  = 0

    if request.is_json:
        data = request.json or {}
        # Support Filebeat format: {"message": "...", "@timestamp": "..."}
        if "message" in data:
            lines = [data["message"]]
        elif "lines" in data:
            lines = data["lines"]
        elif isinstance(data, list):
            lines = [item.get("message", str(item)) for item in data]
        else:
            lines = [data.get("log","")]
    else:
        raw = request.get_data(as_text=True)
        lines = [l.strip() for l in raw.split("\n") if l.strip()]

    for line in lines[:500]:  # max 500 per request
        try:
            _ingest_queue.put_nowait({"line": line, "source": source,
                                      "session_id": sid,
                                      "ts": datetime.datetime.utcnow().isoformat()})
            count += 1
        except queue.Full:
            break

    # Log ingest stats
    conn = get_db()
    conn.execute("INSERT INTO ingest_stats (session_id,source,lines,received_at) VALUES (?,?,?,?)",
                 (sid, source, count, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"accepted": count, "source": source, "session_id": sid})


@app.route("/api/tail/start", methods=["POST"])
@require_api_key
def tail_start():
    """Start tailing a log file."""
    data = request.json or {}
    path = data.get("path","")
    sid  = data.get("session_id","GLOBAL")
    if not path:
        return jsonify({"error": "path required"}), 400
    ok = start_file_tail(path, sid)
    return jsonify({"started": ok, "path": path, "exists": Path(path).exists()})


@app.route("/api/tail/stop", methods=["POST"])
@require_api_key
def tail_stop():
    data = request.json or {}
    path = data.get("path","")
    stop_file_tail(path)
    return jsonify({"stopped": True, "path": path})


@app.route("/api/tail/list")
def tail_list():
    conn = get_db()
    rows = conn.execute("SELECT * FROM file_sources ORDER BY added_at DESC").fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    for r in result:
        r["alive"] = r["file_path"] in _tail_threads and _tail_threads[r["file_path"]].is_alive()
    return jsonify(result)


@app.route("/api/tail/presets")
def tail_presets():
    return jsonify(SOURCE_PRESETS)


@app.route("/api/stream/realtime")
def stream_realtime():
    """SSE endpoint for real-time ingested log events."""
    client_q: queue.Queue = queue.Queue(maxsize=200)
    with _ingest_lock:
        _ingest_sse_clients.append(client_q)

    def generate():
        try:
            while True:
                try:
                    evt = client_q.get(timeout=15)
                    yield f"data: {json.dumps(evt)}\n\n"
                except queue.Empty:
                    yield "data: {\"keepalive\":true}\n\n"
        except GeneratorExit:
            with _ingest_lock:
                try: _ingest_sse_clients.remove(client_q)
                except: pass

    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})


@app.route("/api/search")
@require_api_key
def search_logs():
    """Full-text search using SQLite FTS5."""
    q   = request.args.get("q","").strip()
    sid = request.args.get("session_id")
    limit = min(int(request.args.get("limit","100")), 500)
    if not q:
        return jsonify({"error": "q parameter required"}), 400
    conn = get_db()
    try:
        if sid:
            rows = conn.execute("""
                SELECT le.* FROM logs_fts
                JOIN log_entries le ON le.id = logs_fts.rowid
                WHERE logs_fts MATCH ? AND le.session_id = ?
                ORDER BY rank LIMIT ?""", (q, sid, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT le.* FROM logs_fts
                JOIN log_entries le ON le.id = logs_fts.rowid
                WHERE logs_fts MATCH ? ORDER BY rank LIMIT ?""", (q, limit)).fetchall()
        conn.close()
        return jsonify({"query": q, "count": len(rows), "results": [dict(r) for r in rows]})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e), "hint": "Use FTS5 syntax: word1 word2, 'phrase', word*"}), 400


@app.route("/api/sessions/history")
def sessions_history():
    """List all sessions with stats."""
    conn = get_db()
    sessions = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    result = []
    for s in sessions:
        d = dict(s)
        d["log_count"] = conn.execute("SELECT COUNT(*) FROM log_entries WHERE session_id=?", (s["id"],)).fetchone()[0]
        d["incident_count"] = conn.execute("SELECT COUNT(*) FROM incidents WHERE session_id=?", (s["id"],)).fetchone()[0]
        d["crit_count"] = conn.execute("SELECT COUNT(*) FROM log_entries WHERE session_id=? AND severity='CRITICAL'", (s["id"],)).fetchone()[0]
        result.append(d)
    conn.close()
    return jsonify(result)


@app.route("/api/sessions/<sid>/label", methods=["POST"])
def session_label(sid):
    data = request.json or {}
    conn = get_db()
    conn.execute("UPDATE sessions SET label=? WHERE id=?", (data.get("label",""), sid))
    conn.commit(); conn.close()
    return jsonify({"ok": True})


@app.route("/api/sessions/<sid>/export")
def session_export(sid):
    """Export full session as JSON."""
    conn = get_db()
    session  = conn.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    logs     = conn.execute("SELECT * FROM log_entries WHERE session_id=?", (sid,)).fetchall()
    incidents= conn.execute("SELECT * FROM incidents WHERE session_id=?", (sid,)).fetchall()
    chat     = conn.execute("SELECT * FROM chat_history WHERE session_id=?", (sid,)).fetchall()
    conn.close()
    export = {
        "sentrasec_version": "2.0",
        "exported_at": datetime.datetime.utcnow().isoformat(),
        "session": dict(session) if session else {},
        "log_entries": [dict(r) for r in logs],
        "incidents": [dict(r) for r in incidents],
        "chat_history": [dict(r) for r in chat],
    }
    return Response(json.dumps(export, indent=2, ensure_ascii=False, default=str),
                    mimetype="application/json",
                    headers={"Content-Disposition": f"attachment; filename=sentrasec-session-{sid}.json"})


@app.route("/api/sessions/import", methods=["POST"])
@require_api_key
def session_import():
    """Import a previously exported session JSON."""
    try:
        data = request.json or {}
        if "session" not in data:
            return jsonify({"error": "Invalid export format"}), 400
        orig = data["session"]
        new_sid = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:12].upper()
        now = datetime.datetime.utcnow().isoformat()
        conn = get_db()
        conn.execute("INSERT OR IGNORE INTO sessions (id,created_at,threat_level,notes,label) VALUES (?,?,?,?,?)",
                     (new_sid, now, orig.get("threat_level","low"),
                      f"[Imported from {orig.get('id','?')}] " + (orig.get("notes") or ""),
                      orig.get("label","")))
        imported_logs = 0
        for row in data.get("log_entries", []):
            conn.execute("""INSERT INTO log_entries
                (session_id,raw,log_type,severity,timestamp_raw,timestamp_iso,
                 src_ip,dst_ip,src_port,dst_port,username,event_type,
                 mitre_id,mitre_name,inserted_at,source_file,ingest_source)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (new_sid, row.get("raw",""), row.get("log_type",""), row.get("severity","LOW"),
                 row.get("timestamp_raw"), row.get("timestamp_iso"),
                 row.get("src_ip"), row.get("dst_ip"), row.get("src_port"), row.get("dst_port"),
                 row.get("username"), row.get("event_type"),
                 row.get("mitre_id"), row.get("mitre_name"),
                 now, row.get("source_file","import"), "import"))
            imported_logs += 1
        for inc in data.get("incidents", []):
            conn.execute("""INSERT INTO incidents
                (session_id,title,severity,src_ip,mitre_ids,timeline,risk_score,status,created_at)
                VALUES (?,?,?,?,?,?,?,?,?)""",
                (new_sid, inc.get("title",""), inc.get("severity","LOW"), inc.get("src_ip",""),
                 inc.get("mitre_ids","[]"), inc.get("timeline","[]"),
                 inc.get("risk_score",0), inc.get("status","open"), now))
        for msg in data.get("chat_history", []):
            conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                         (new_sid, msg.get("role","user"), msg.get("content",""), now))
        conn.commit(); conn.close()
        return jsonify({"new_session_id": new_sid, "imported_logs": imported_logs,
                        "original_session": orig.get("id","?")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/incidents/<int:inc_id>/tag", methods=["POST"])
def incident_tag(inc_id):
    data = request.json or {}
    conn = get_db()
    row = conn.execute("SELECT tags FROM incidents WHERE id=?", (inc_id,)).fetchone()
    if not row: conn.close(); return jsonify({"error":"Not found"}), 404
    tags = json.loads(row["tags"] or "[]")
    tag  = data.get("tag","").strip()
    if tag and tag not in tags: tags.append(tag)
    conn.execute("UPDATE incidents SET tags=? WHERE id=?", (json.dumps(tags), inc_id))
    conn.commit(); conn.close()
    return jsonify({"tags": tags})


@app.route("/api/incidents/<int:inc_id>/comment", methods=["POST"])
def incident_comment(inc_id):
    data = request.json or {}
    conn = get_db()
    conn.execute("UPDATE incidents SET comment=? WHERE id=?", (data.get("comment",""), inc_id))
    conn.commit(); conn.close()
    return jsonify({"ok": True})


@app.route("/api/incidents/<int:inc_id>/status", methods=["POST"])
def incident_status(inc_id):
    data = request.json or {}
    status = data.get("status","open")
    if status not in ("open","investigating","resolved","false_positive"):
        return jsonify({"error":"Invalid status"}), 400
    conn = get_db()
    conn.execute("UPDATE incidents SET status=? WHERE id=?", (status, inc_id))
    conn.commit(); conn.close()
    return jsonify({"status": status})


@app.route("/api/upload", methods=["POST"])
@require_api_key
def upload_logs():
    """Multi-file upload — accepts text/log files."""
    sid = request.form.get("session_id", request.args.get("session_id","DEMO"))
    files = request.files.getlist("files") or request.files.getlist("file")
    if not files:
        return jsonify({"error": "No files provided"}), 400
    total_lines = 0
    results = []
    for f in files:
        fname   = f.filename or "upload"
        content = f.read().decode("utf-8", errors="replace")
        lines   = [l.strip() for l in content.split("\n") if l.strip()]
        for line in lines[:2000]:
            try:
                _ingest_queue.put_nowait({
                    "line": line, "source": f"upload:{fname}",
                    "session_id": sid,
                    "ts": datetime.datetime.utcnow().isoformat()
                })
                total_lines += 1
            except queue.Full:
                break
        results.append({"file": fname, "lines": len(lines)})
    return jsonify({"total_lines": total_lines, "files": results, "session_id": sid})


@app.route("/api/config/apikey")
def get_apikey_info():
    """Returns API key info (masked) and rate limit config."""
    return jsonify({
        "api_key_prefix": API_KEY[:8] + "...",
        "api_key_file": API_KEY_FILE,
        "rate_limit_rpm": RATE_LIMIT_REQ,
        "hint": "Include header X-API-Key: <key> or ?api_key=<key> on protected endpoints"
    })



# ═══════════════════════════════════════════════════════════════════
#  NEW ROUTES — Ruleset, Investigation Notebook, Art.21, NIS2 Templates
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/rules/evaluate", methods=["POST"])
def rules_evaluate():
    """Run 20-rule detection engine on parsed entries in session."""
    data = request.json or {}
    sid  = data.get("session_id","DEMO")
    conn = get_db()
    rows = conn.execute("SELECT * FROM log_entries WHERE session_id=? ORDER BY id", (sid,)).fetchall()
    conn.close()
    entries = [dict(r) for r in rows]
    alerts  = run_ruleset(entries, sid)
    nis2    = classify_nis2(alerts, entries)
    # Store alerts to DB
    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    for a in alerts:
        conn.execute("""INSERT INTO alerts (session_id,title,severity,detail,mitre_id,src_ip,created_at,notified)
            VALUES (?,?,?,?,?,?,?,0)""",
            (sid, a["rule_name"], a["severity"],
             f"[{a['rule_id']}] {a['nis2_category']} — {a['group_key']} — {a['count']} zdarzeń | {a['remediation']}",
             a["mitre_id"], a["group_key"] if a["group_by"]=="src_ip" else "", now))
    conn.commit(); conn.close()
    return jsonify({"alerts": alerts, "count": len(alerts), "nis2": nis2,
                    "session_id": sid, "entries_analyzed": len(entries)})


@app.route("/api/rules/list")
def rules_list():
    return jsonify({"rules": DETECTION_RULES, "count": len(DETECTION_RULES)})


@app.route("/api/art21/assess", methods=["POST"])
def art21_assess():
    """Art.21 NIS2 compliance assessment — quiz answers + log analysis."""
    data    = request.json or {}
    sid     = data.get("session_id","DEMO")
    answers = data.get("answers", {})  # {req_id: score_0_100}
    # Get alerts from DB
    conn = get_db()
    entries = [dict(r) for r in conn.execute("SELECT * FROM log_entries WHERE session_id=?", (sid,)).fetchall()]
    conn.close()
    alerts = run_ruleset(entries, sid)
    result = assess_art21(answers, alerts)
    return jsonify(result)


@app.route("/api/notebook/<int:inc_id>", methods=["POST"])
def investigation_notebook(inc_id):
    """AI Investigation Notebook — full incident analysis with LLM+RAG."""
    data = request.json or {}
    sid  = data.get("session_id","DEMO")
    conn = get_db()
    inc  = conn.execute("SELECT * FROM incidents WHERE id=?", (inc_id,)).fetchone()
    if not inc:
        conn.close()
        return jsonify({"error":"Incident not found"}), 404
    inc_d = dict(inc)
    # Get related log entries
    src_ip   = inc_d.get("src_ip","")
    timeline = json.loads(inc_d.get("timeline","[]"))
    mitre_ids = json.loads(inc_d.get("mitre_ids","[]"))
    # Related logs from same IP
    related = conn.execute(
        "SELECT * FROM log_entries WHERE session_id=? AND src_ip=? ORDER BY id LIMIT 50",
        (sid, src_ip)
    ).fetchall() if src_ip else []
    all_entries = [dict(r) for r in conn.execute("SELECT * FROM log_entries WHERE session_id=?", (sid,)).fetchall()]
    conn.close()
    alerts  = run_ruleset(all_entries, sid)
    nis2    = classify_nis2(alerts, all_entries)
    rag_ctx = rag_engine.retrieve(f"incydent {inc_d.get('title','')} {' '.join(mitre_ids)} remediation NIS2", n=4)
    rag_text = "\n".join([d["text"] for d in rag_ctx])
    # Related logs text
    log_sample = "\n".join([r["raw"] for r in related[:20]])
    mitre_details = "\n".join([f"  {m}: {MITRE_MAP.get(m,{}).get('name','?')} [{MITRE_MAP.get(m,{}).get('tactic','?')}]" for m in mitre_ids])
    # Triggered rules for this IP
    ip_alerts = [a for a in alerts if a.get("group_key")==src_ip]
    rules_triggered = "\n".join([f"  [{a['rule_id']}] {a['rule_name']} — {a['count']} zdarzeń" for a in ip_alerts])
    prompt = f"""Jesteś AI Tier-1 analitykiem SOC. Zbadaj incydent i stwórz kompletny Investigation Notebook.

INCYDENT:
- Tytuł: {inc_d.get('title','')}
- Severity: {inc_d.get('severity','')}
- Risk Score: {inc_d.get('risk_score',0)}
- Atakujące IP: {src_ip}
- Status: {inc_d.get('status','open')}

WYKRYTE TECHNIKI MITRE ATT&CK:
{mitre_details or 'brak'}

REGUŁY DETEKCJI (TRIGGERED):
{rules_triggered or 'brak'}

LOGI POWIĄZANE Z INCYDENTEM:
{log_sample or 'brak logów'}

OCENA NIS2:
- Klasyfikacja: {nis2['classification']}
- Score: {nis2['score']}/100
- Wymagane ostrzeżenie 24h: {'TAK' if nis2['early_warning_24h'] else 'NIE'}
- Wymagane zgłoszenie 72h: {'TAK' if nis2['notification_72h'] else 'NIE'}

KONTEKST RAG:
{rag_text}

Sporządź Investigation Notebook w strukturze:

## 1. STRESZCZENIE INCYDENTU
Krótki opis (2-3 zdania) co się stało, kto atakował, jaki był cel.

## 2. TIMELINE ATAKU
Krok po kroku odtwórz sekwencję zdarzeń z timestampami i technikami MITRE.

## 3. ANALIZA TECHNICZNA
- Wektory ataku i techniki
- Podatności/słabości które zostały wykorzystane
- Wskaźniki kompromitacji (IoC): IP, wzorce, sygnatury

## 4. OCENA WPŁYWU (CIA)
- Dostępność (0-10): ...
- Poufność (0-10): ...
- Integralność (0-10): ...
- Czy dane osobowe mogły zostać naruszone? (RODO/NIS2)

## 5. REKOMENDOWANE DZIAŁANIA
Konkretna lista kroków do wykonania TERAZ (priorytet 1-3).

## 6. FRAGMENT RAPORTU NIS2
Gotowy paragraf do włączenia do zgłoszenia CSIRT NASK (po polsku, profesjonalny język).

## 7. WNIOSKI I LEKCJE
Co poprawić żeby zapobiec podobnemu incydentowi w przyszłości.

Pisz wyłącznie po polsku. Bądź konkretny, operacyjny, oparty na danych z logów."""

    messages = [{"role":"user","content":prompt}]
    system   = ("Jesteś doświadczonym analitykiem SOC i ekspertem NIS2. "
                "Twoje raporty są używane przez małe i średnie przedsiębiorstwa do reagowania na incydenty. "
                "Odpowiadaj po polsku, konkretnie i praktycznie.")
    notebook_text = ollama_chat(messages, system=system, stream=False)
    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"user",f"[Investigation Notebook — {inc_d.get('title','')}]",now))
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"assistant",notebook_text,now))
    conn.commit(); conn.close()
    return jsonify({
        "notebook":       notebook_text,
        "incident":       inc_d,
        "alerts":         ip_alerts,
        "nis2":           nis2,
        "mitre_ids":      mitre_ids,
        "related_logs":   len(related),
        "generated_at":   now,
    })


@app.route("/api/report/nis2/template", methods=["POST"])
def report_nis2_template():
    """Generate NIS2 report from specific template: 24h / 72h / final."""
    data     = request.json or {}
    sid      = data.get("session_id","DEMO")
    template = data.get("template","72h")  # 24h | 72h | final
    org_name = data.get("org_name","[Nazwa organizacji]")
    org_type = data.get("org_type","podmiot ważny")
    logs     = data.get("logs","")
    conn = get_db()
    log_entries = conn.execute("SELECT * FROM log_entries WHERE session_id=? ORDER BY id", (sid,)).fetchall()
    incidents   = conn.execute("SELECT * FROM incidents WHERE session_id=? ORDER BY risk_score DESC", (sid,)).fetchall()
    conn.close()
    all_entries = [dict(r) for r in log_entries]
    alerts      = run_ruleset(all_entries, sid)
    nis2        = classify_nis2(alerts, all_entries)
    now_dt      = datetime.datetime.utcnow()
    report_id   = f"NIS2-{template.upper()}-{now_dt.strftime('%Y%m%d-%H%M%S')}"
    sev_c       = defaultdict(int)
    ips         = set(); mitre_ids = set()
    for r in log_entries:
        sev_c[r["severity"]] += 1
        if r["src_ip"]: ips.add(r["src_ip"])
        if r["mitre_id"]: mitre_ids.add(r["mitre_id"])
    log_sample  = logs[:3000] if logs else "\n".join([r["raw"] for r in log_entries[:40]])
    inc_summary = "\n".join([f"[{i['severity']}] {i['title']} Risk:{i['risk_score']}" for i in incidents[:8]])
    alerts_summary = "\n".join([f"[{a['rule_id']}] {a['rule_name']} — {a['group_key']} ({a['count']} zdarzeń)" for a in alerts[:10]])
    templates = {
        "24h": f"""Sporządź WCZESNE OSTRZEŻENIE NIS2 (Art. 23 ust. 4) dla organizacji "{org_name}" ({org_type}).

Formularz WCZESNEGO OSTRZEŻENIA zgodny z CSIRT NASK — termin: 24 godziny od wykrycia.

DANE ZDARZENIA:
{log_sample}
ALERTY: {alerts_summary}
NIS2 Score: {nis2['score']}/100 — {nis2['classification']}

Wypełnij formularz wczesnego ostrzeżenia:

## WCZESNE OSTRZEŻENIE — NIS2 Art. 23(4)

**1. Dane organizacji**
- Nazwa: {org_name}
- Typ podmiotu: {org_type}
- Data/czas wykrycia zdarzenia: {now_dt.strftime('%Y-%m-%d %H:%M')} UTC
- Raport ID: {report_id}

**2. Opis zdarzenia (wstępny)**
[Na podstawie logów — opisz krótko co się stało]

**3. Czy zdarzenie spełnia kryteria poważnego incydentu? (Art. 23(3))**
[TAK/NIE + uzasadnienie]

**4. Wstępna ocena wpływu**
[Które systemy/usługi są/mogą być dotknięte]

**5. Podjęte natychmiastowe działania**
[Co już zrobiono w ciągu ostatnich godzin]

**6. Planowane kolejne kroki**
[Co będzie zrobione w ciągu 72h]

**7. Czy wymagana jest pomoc CSIRT?**
[TAK/NIE — jaka pomoc]

Kontakt CSIRT NASK: incydent@cert.pl | +48 22 38 08 274

Wypełnij każdą sekcję konkretnie na podstawie dostarczonych logów. Pisz po polsku.""",

        "72h": f"""Sporządź ZGŁOSZENIE INCYDENTU NIS2 (Art. 23 ust. 4) dla organizacji "{org_name}" ({org_type}).

Formularz ZGŁOSZENIA zgodny z CSIRT NASK — termin: 72 godziny od wykrycia.

DANE INCYDENTU:
{log_sample}
ALERTY DETEKCJI: {alerts_summary}
INCYDENTY: {inc_summary}
NIS2 Ocena: {nis2['classification']} (score: {nis2['score']}/100)
Czynniki: {', '.join(nis2.get('factors',['brak']))}

Wypełnij pełne zgłoszenie incydentu NIS2:

## ZGŁOSZENIE INCYDENTU NIS2 — Art. 23(4)
**Report ID:** {report_id}
**Organizacja:** {org_name} ({org_type})
**Data zgłoszenia:** {now_dt.strftime('%Y-%m-%d %H:%M')} UTC

**1. IDENTYFIKACJA INCYDENTU**
- Klasyfikacja: [poważny incydent/incydent/zdarzenie]
- Data/czas wykrycia:
- Data/czas rozpoczęcia (szacowany):
- Dotknięte systemy i usługi:
- Wektor ataku:

**2. OPIS TECHICZNY**
[Szczegółowy opis przebiegu incydentu na podstawie logów]

**3. WPŁYW NA DZIAŁALNOŚĆ**
- Dostępność usług: [tak/nie — jakich]
- Naruszenie danych osobowych: [tak/nie — RODO Art. 33]
- Szacowana liczba dotkniętych użytkowników:
- Straty finansowe (szacunek):

**4. TECHNIKI ATT&CK**: {', '.join(mitre_ids) or 'w trakcie analizy'}

**5. PODJĘTE ŚRODKI ZARADCZE**
[Lista konkretnych działań podjętych do momentu zgłoszenia]

**6. PLANOWANE DALSZE DZIAŁANIA**
[Harmonogram z terminami do raportu końcowego]

**7. DANE KONTAKTOWE**
- Osoba kontaktowa ds. incydentu:
- Telefon/e-mail:

Wypełnij każdą sekcję na podstawie logów. Pisz po polsku, językiem formalnym.""",

        "final": f"""Sporządź RAPORT KOŃCOWY incydentu NIS2 (Art. 23 ust. 4) dla "{org_name}" ({org_type}).

Raport KOŃCOWY — termin: 1 miesiąc od zgłoszenia. Dokument do archiwizacji.

KOMPLETNE DANE ZDARZENIA:
{log_sample}
WSZYSTKIE ALERTY: {alerts_summary}
INCYDENTY: {inc_summary}
NIS2: {nis2['classification']}
SEVERITY: CRITICAL:{sev_c.get('CRITICAL',0)} HIGH:{sev_c.get('HIGH',0)} MEDIUM:{sev_c.get('MEDIUM',0)}
IPs: {', '.join(sorted(ips))}
MITRE: {', '.join(mitre_ids)}

Sporządź kompletny raport końcowy NIS2:

## RAPORT KOŃCOWY INCYDENTU NIS2
**Report ID:** {report_id}
**Organizacja:** {org_name} ({org_type})
**Data raportu:** {now_dt.strftime('%Y-%m-%d')}

### 1. PODSUMOWANIE WYKONAWCZE
[2-3 zdania dla zarządu — co się stało, jaki był wpływ, co zrobiono]

### 2. CHRONOLOGIA INCYDENTU (pełna)
[Oś czasu od pierwszych sygnałów do zamknięcia]

### 3. ANALIZA PRZYCZYN ŹRÓDŁOWYCH
[Root cause analysis — dlaczego incydent był możliwy]

### 4. WPŁYW I STRATY
- Systemy dotknięte:
- Dane narażone:
- Czas niedostępności:
- Straty finansowe:
- Wpływ reputacyjny:

### 5. PODJĘTE DZIAŁANIA NAPRAWCZE
[Kompletna lista z datami realizacji]

### 6. LESSONS LEARNED
[Co organizacja nauczyła się z incydentu]

### 7. PLAN POPRAWY BEZPIECZEŃSTWA
[Konkretne działania z terminami i odpowiedzialnymi osobami]

### 8. ZGODNOŚĆ Z NIS2 ART. 21
[Które z 10 wymagań Art. 21 wymagają wzmocnienia]

### 9. OŚWIADCZENIE
Niniejszy raport został sporządzony zgodnie z wymaganiami NIS2 (UE) 2022/2555 
i jest przechowywany przez organizację przez minimum 5 lat.

Wygenerowano przez SENTRAsec v2.0 LOCAL — AI SOC Platform (offline)

Wypełnij każdą sekcję konkretnie. Pisz po polsku."""
    }

    prompt = templates.get(template, templates["72h"])
    rag_ctx = rag_engine.retrieve("NIS2 raportowanie incydent CSIRT NASK Art.23", n=3)
    if rag_ctx:
        prompt += f"\n\nKONTEKST NIS2:\n" + "\n".join([d["text"] for d in rag_ctx])
    messages = [{"role":"user","content":prompt}]
    system   = ("Jesteś certyfikowanym ekspertem NIS2 i analitykiem SOC. "
                "Wypełniasz formularze zgłoszeniowe dla małych podmiotów zgodnie z wymogami CSIRT NASK. "
                "Pisz wyłącznie po polsku. Bądź precyzyjny i profesjonalny.")
    report_text = ollama_chat(messages, system=system, stream=False)
    now = datetime.datetime.utcnow().isoformat()
    conn = get_db()
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"user",f"[Raport NIS2 {template.upper()} — {org_name}]",now))
    conn.execute("INSERT INTO chat_history (session_id,role,content,created_at) VALUES (?,?,?,?)",
                 (sid,"assistant",report_text,now))
    conn.commit(); conn.close()
    return jsonify({
        "report":      report_text,
        "report_id":   report_id,
        "template":    template,
        "org_name":    org_name,
        "generated":   now,
        "nis2":        nis2,
        "alerts_count":len(alerts),
        "sev_counts":  dict(sev_c),
        "model":       OLLAMA_MODEL,
    })


@app.route("/api/alerts")
def get_alerts():
    sid = request.args.get("session_id","DEMO")
    conn = get_db()
    rows = conn.execute("SELECT * FROM alerts WHERE session_id=? ORDER BY id DESC LIMIT 100", (sid,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/health")
def health():
    """Health check — zawsze zwraca poprawny JSON, nigdy nie rzuca wyjątku."""
    try:
        online = ollama_ping()
    except Exception:
        online = False
    try:
        models = ollama_list_models() if online else []
    except Exception:
        models = []
    try:
        rag_ok = rag_engine.use_chroma
    except Exception:
        rag_ok = False
    try:
        db_ok = Path(DB_PATH).exists()
    except Exception:
        db_ok = False
    return jsonify({
        "status":            "ok",
        "version":           "2.0-LOCAL",
        "model":             OLLAMA_MODEL,
        "ollama_online":     online,
        "ollama_host":       OLLAMA_HOST,
        "models_available":  models,
        "rag_active":        rag_ok,
        "abuseipdb":         bool(ABUSEIPDB_KEY),
        "db":                db_ok,
        "ts":                datetime.datetime.utcnow().isoformat(),
    })

@app.route("/api/rag/retrieve", methods=["POST"])
def rag_retrieve():
    data  = request.json or {}
    query = data.get("query","")
    cat   = data.get("category")
    n     = int(data.get("n", 5))
    docs  = rag_engine.retrieve(query, n=n, category=cat)
    return jsonify({"query":query,"results":docs,"count":len(docs),"backend":"chromadb" if rag_engine.use_chroma else "tfidf"})

# ═══════════════════════════════════════════════════════════════════
#  FRONTEND HTML — zachowany styl z v2, dodany model selector
# ═══════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template_string(HTML_APP)

HTML_APP = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SENTRASEC v2.0 LOCAL — AI SOC Assistant</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;800&display=swap');
  :root{
    --bg:#040910;--bg2:#070d17;--bg3:#0c1420;--panel:#0a1320;--panel2:#0d1826;
    --border:#1e3550;--border2:#26415e;
    --accent:#00d4ff;--accent2:#22b0e8;--accent3:#00ffaa;
    --warn:#ffbb00;--danger:#ff3355;--success:#00ff88;
    --muted:#5a7a95;--text:#ddeeff;--text2:#a8c8e0;--text3:#7898b8;
    --glow:0 0 20px rgba(0,212,255,.3);
    --mono:'Share Tech Mono',monospace;--ui:'Rajdhani',sans-serif;--head:'Exo 2',sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--bg);color:var(--text);font-family:var(--ui);font-size:16px;min-height:100vh;overflow-x:hidden;
    background-image:radial-gradient(ellipse 80% 50% at 50% -20%,rgba(0,80,120,.12) 0%,transparent 70%),
      repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(0,212,255,.02) 40px),
      repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(0,212,255,.02) 40px);}
  body::before{content:'';pointer-events:none;position:fixed;inset:0;z-index:9999;
    background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.04) 3px);}

  header{background:linear-gradient(180deg,#0a1825,#070f1c);border-bottom:1px solid var(--border2);
    padding:0 24px;height:82px;display:flex;align-items:center;justify-content:space-between;
    position:sticky;top:0;z-index:100;box-shadow:0 4px 40px rgba(0,0,0,.6),inset 0 -1px 0 rgba(0,212,255,.12);}
  .brand-main{font-family:var(--head);font-weight:800;font-size:28px;letter-spacing:4px;color:var(--accent);
    text-shadow:0 0 28px rgba(0,212,255,.65),0 0 70px rgba(0,212,255,.22);line-height:1;text-transform:uppercase;}
  .brand-sub{font-family:var(--ui);font-size:14px;letter-spacing:3px;color:var(--text3);text-transform:uppercase;margin-top:2px;}
  .clock-time{font-family:var(--mono);font-size:21px;color:var(--accent);letter-spacing:2px;text-shadow:0 0 10px rgba(0,212,255,.4);}
  .clock-date,.clock-utc{font-family:var(--mono);font-size:12px;color:var(--text3);}
  .threat-indicator{display:flex;align-items:center;gap:9px;padding:7px 14px;border:1px solid var(--border);border-radius:3px;background:rgba(0,0,0,.3);}
  .threat-pulse{width:12px;height:12px;border-radius:50%;background:var(--success);box-shadow:0 0 10px var(--success);animation:plow 2s infinite;transition:all .5s;}
  .threat-pulse.medium{background:var(--warn);box-shadow:0 0 12px var(--warn);animation:pmed 1s infinite;}
  .threat-pulse.high{background:var(--danger);box-shadow:0 0 14px var(--danger);animation:phi .4s infinite;}
  @keyframes plow{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}
  @keyframes pmed{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.25)}}
  @keyframes phi{0%,100%{opacity:1;transform:scale(1.3)}50%{opacity:.6;transform:scale(.85)}}
  .threat-level-text{font-family:var(--mono);font-size:14px;font-weight:bold;color:var(--success);transition:color .4s;}
  .threat-level-text.medium{color:var(--warn)}.threat-level-text.high{color:var(--danger)}
  .sdot{display:flex;align-items:center;gap:5px;font-family:var(--mono);font-size:12px;color:var(--text2);}
  .sdot i{width:7px;height:7px;border-radius:50%;animation:plow 3s infinite;}
  .sdot i.ok{background:var(--success);box-shadow:0 0 5px var(--success);}
  .sdot i.warn{background:var(--warn);box-shadow:0 0 5px var(--warn);}
  .sdot i.err{background:var(--danger);box-shadow:0 0 5px var(--danger);}

  /* MODEL SELECTOR */
  .model-selector{display:flex;align-items:center;gap:7px;padding:6px 12px;
    border:1px solid var(--border2);border-radius:3px;background:rgba(0,0,0,.25);}
  .model-label{font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;}
  #modelSelect{background:var(--bg3);border:1px solid var(--border);border-radius:2px;
    color:var(--accent2);font-family:var(--mono);font-size:12px;padding:4px 8px;outline:none;cursor:pointer;}
  #modelSelect:focus{border-color:var(--accent2);}
  .ollama-badge{font-family:var(--mono);font-size:11px;padding:3px 9px;border-radius:2px;letter-spacing:.5px;cursor:pointer;user-select:none;}
  .ollama-badge.online{background:rgba(0,255,136,.1);border:1px solid rgba(0,255,136,.3);color:var(--success);}
  .ollama-badge.offline{background:rgba(255,51,85,.1);border:1px solid rgba(255,51,85,.3);color:var(--danger);animation:badge-pulse 2s infinite;}
  @keyframes badge-pulse{0%,100%{opacity:1}50%{opacity:.6}}

  .app-body{display:grid;grid-template-columns:310px 1fr 340px;height:calc(100vh - 82px);overflow:hidden;}
  .sidebar-left,.sidebar-right{background:var(--panel);display:flex;flex-direction:column;overflow:hidden;}
  .sidebar-left{border-right:1px solid var(--border2);}
  .sidebar-right{border-left:1px solid var(--border2);}
  .ph{padding:13px 16px 10px;border-bottom:1px solid var(--border);font-family:var(--mono);font-size:12px;
    color:var(--accent2);letter-spacing:2px;text-transform:uppercase;display:flex;align-items:center;gap:8px;font-weight:bold;}
  .ph::before{content:'';width:3px;height:14px;background:var(--accent);border-radius:1px;}
  .sep{height:1px;background:var(--border);}
  .scrollable{overflow-y:auto;}.scrollable::-webkit-scrollbar{width:3px}
  .scrollable::-webkit-scrollbar-thumb{background:var(--border2);}

  .sgrid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:10px;}
  .scard{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:12px 14px;}
  .sv{font-family:var(--mono);font-size:28px;color:var(--accent);line-height:1;margin-bottom:3px;}
  .sl{font-size:13px;color:var(--text2);letter-spacing:1px;text-transform:uppercase;font-weight:600;}
  .scard.d .sv{color:var(--danger)}.scard.w .sv{color:var(--warn)}.scard.o .sv{color:var(--success)}

  .tabs{display:flex;border-bottom:1px solid var(--border);}
  .tab{flex:1;padding:10px 5px;font-family:var(--mono);font-size:12px;color:var(--text2);text-align:center;
    cursor:pointer;letter-spacing:.5px;border-bottom:2px solid transparent;transition:all .2s;
    text-transform:uppercase;background:none;border-top:none;border-left:none;border-right:none;}
  .tab:hover{color:var(--accent2);background:rgba(0,212,255,.04);}
  .tab.active{color:var(--accent);border-bottom-color:var(--accent);background:rgba(0,212,255,.06);font-weight:bold;}
  .tc{display:none;flex:1;flex-direction:column;overflow:hidden;}
  .tc.active{display:flex;}

  textarea,input[type=text],select{background:var(--bg);border:1px solid var(--border);border-radius:3px;
    color:var(--text);outline:none;transition:border-color .2s;}
  textarea:focus,input[type=text]:focus{border-color:var(--accent2);}
  textarea::placeholder{color:var(--text3);}
  .btn{padding:10px 16px;border-radius:3px;font-family:var(--mono);font-size:13px;letter-spacing:1px;
    cursor:pointer;border:1px solid transparent;transition:all .2s;text-transform:uppercase;font-weight:600;}
  .bp{background:var(--accent2);color:#fff;border-color:var(--accent);}
  .bp:hover{background:var(--accent);box-shadow:var(--glow);}
  .bs{background:transparent;color:var(--text2);border-color:var(--border2);}
  .bs:hover{border-color:var(--accent2);color:var(--accent2);}
  .brow{display:flex;gap:6px;margin-top:7px;}
  .linput{padding:11px;display:flex;flex-direction:column;gap:7px;flex:1;}
  #logRaw{width:100%;height:130px;resize:none;font-family:var(--mono);font-size:13px;padding:10px;line-height:1.65;}

  /* RAG panel */
  .rag-item{padding:8px 10px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;margin-bottom:6px;}
  .rag-cat{font-family:var(--mono);font-size:11px;color:var(--accent2);margin-bottom:3px;letter-spacing:.5px;}
  .rag-text{font-size:13px;color:var(--text2);line-height:1.6;}

  .chat{display:flex;flex-direction:column;background:var(--bg2);overflow:hidden;}
  .chat-hdr{padding:11px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
  .chat-title{font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:2px;text-transform:uppercase;}
  .msgs{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:16px;scroll-behavior:smooth;}
  .msgs::-webkit-scrollbar{width:4px}.msgs::-webkit-scrollbar-thumb{background:var(--border2);}
  .msg{display:flex;gap:12px;animation:min .3s cubic-bezier(.22,1,.36,1);}
  @keyframes min{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
  .mav{width:38px;height:38px;border-radius:3px;display:flex;align-items:center;justify-content:center;
    font-family:var(--mono);font-size:12px;flex-shrink:0;margin-top:2px;font-weight:bold;}
  .mav.ai{background:rgba(0,212,255,.12);border:1px solid rgba(0,212,255,.35);color:var(--accent);}
  .mav.usr{background:rgba(34,176,232,.12);border:1px solid rgba(34,176,232,.35);color:var(--accent2);}
  .mb{flex:1;min-width:0;}
  .mm{font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:5px;letter-spacing:.5px;}
  .mc{background:var(--panel);border:1px solid var(--border2);border-radius:4px;padding:14px 18px;
    font-size:16px;line-height:1.85;color:var(--text);white-space:pre-wrap;word-wrap:break-word;}
  .msg.usr .mc{background:rgba(34,176,232,.07);border-color:rgba(34,176,232,.25);}
  .mc code{font-family:var(--mono);background:rgba(0,0,0,.4);padding:2px 7px;border-radius:2px;font-size:14px;color:var(--accent3);}
  .mc strong{color:#eef6ff;font-weight:700;}.mc h4{color:var(--accent);margin:10px 0 4px;font-size:15px;letter-spacing:1px;}
  .sC{color:#ff4466;font-weight:bold}.sH{color:#ff7755;font-weight:bold}
  .sM{color:var(--warn);font-weight:600}.sL{color:var(--success)}.sI{color:var(--accent2)}
  .mtag{display:inline-block;padding:2px 8px;background:rgba(34,176,232,.15);border:1px solid rgba(34,176,232,.4);
    border-radius:2px;font-family:var(--mono);font-size:12px;color:var(--accent2);margin:1px;font-weight:bold;}
  .typing{display:none;align-items:center;gap:10px;padding:0 18px 12px;animation:min .2s;}
  .typing.on{display:flex;}
  .tdots{display:flex;gap:5px;align-items:center;padding:10px 14px;background:var(--panel);border:1px solid var(--border);border-radius:4px;}
  .tdots span{width:6px;height:6px;background:var(--accent2);border-radius:50%;animation:db 1.2s infinite;}
  .tdots span:nth-child(2){animation-delay:.2s}.tdots span:nth-child(3){animation-delay:.4s}
  @keyframes db{0%,80%,100%{transform:translateY(0);opacity:.35}40%{transform:translateY(-6px);opacity:1}}
  .cinput{padding:14px 18px;border-top:1px solid var(--border2);flex-shrink:0;background:var(--panel);}
  .irow{display:flex;gap:8px;align-items:flex-end;}
  #chatIn{flex:1;min-height:48px;max-height:120px;resize:none;font-family:var(--ui);font-size:16px;padding:12px 15px;overflow-y:auto;border-radius:4px;color:var(--text);}
  .sbtn{width:48px;height:48px;background:var(--accent2);border:1px solid var(--accent);border-radius:4px;
    color:#fff;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0;}
  .sbtn:hover{background:var(--accent);box-shadow:var(--glow);}
  .sbtn:disabled{opacity:.35;cursor:not-allowed;}
  .hints-row{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px;}
  .hint{padding:5px 10px;background:rgba(0,212,255,.05);border:1px solid var(--border2);border-radius:3px;
    font-family:var(--mono);font-size:12px;color:var(--text2);cursor:pointer;transition:all .15s;}
  .hint:hover{border-color:var(--accent2);color:var(--accent2);background:rgba(0,212,255,.09);}

  /* ── LIVE STREAM ── */
  .logstream{flex:1;overflow-y:auto;padding:8px 6px;font-family:var(--mono);font-size:13px;line-height:1.0;
    display:flex;flex-direction:column;gap:0;background:var(--bg);}
  .logstream::-webkit-scrollbar{width:4px}
  .logstream::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}
  .ll{padding:5px 8px;border-radius:3px;display:flex;gap:8px;align-items:flex-start;
    animation:ll .3s ease;border-bottom:1px solid rgba(255,255,255,.03);transition:background .15s;}
  .ll:hover{background:rgba(0,212,255,.05);}
  @keyframes ll{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}
  .lts{color:var(--muted);flex-shrink:0;font-size:11px;padding-top:2px;min-width:56px;}
  .lsev{flex-shrink:0;font-weight:bold;font-size:11px;padding:1px 6px;border-radius:2px;
    min-width:44px;text-align:center;letter-spacing:.5px;}
  .lsev.CRIT{color:#fff;background:#cc0033;box-shadow:0 0 8px rgba(204,0,51,.5);}
  .lsev.ERR {color:#fff;background:#884422;box-shadow:0 0 6px rgba(136,68,34,.4);}
  .lsev.WARN{color:#1a1200;background:var(--warn);}
  .lsev.INFO{color:#003344;background:var(--accent2);}
  .lsev.DBG {color:var(--muted);background:transparent;border:1px solid var(--border);}
  .lmsg{color:var(--text);font-size:13px;line-height:1.45;word-break:break-word;flex:1;}
  .ll.CRIT{background:rgba(204,0,51,.08);border-left:3px solid #cc0033;}
  .ll.WARN{background:rgba(255,170,0,.05);border-left:3px solid rgba(255,170,0,.5);}
  .ll.ERR {background:rgba(136,68,34,.07);border-left:3px solid rgba(136,68,34,.5);}
  /* stream header stats */
  .stream-stats{display:flex;gap:6px;padding:6px 8px;background:var(--bg3);border-bottom:1px solid var(--border);flex-shrink:0;}
  .ss-item{flex:1;text-align:center;padding:4px 2px;border-radius:3px;border:1px solid var(--border);}
  .ss-num{font-family:var(--mono);font-size:14px;font-weight:bold;line-height:1;}
  .ss-lbl{font-family:var(--mono);font-size:9px;color:var(--text3);letter-spacing:.5px;text-transform:uppercase;}
  .ss-crit{border-color:rgba(204,0,51,.4);background:rgba(204,0,51,.08);}.ss-crit .ss-num{color:#ff4466;}
  .ss-warn{border-color:rgba(255,170,0,.3);background:rgba(255,170,0,.06);}.ss-warn .ss-num{color:var(--warn);}
  .ss-info{border-color:rgba(0,153,204,.3);background:rgba(0,153,204,.06);}.ss-info .ss-num{color:var(--accent2);}
  /* pulse dot on new event */
  .stream-live-dot{width:8px;height:8px;border-radius:50%;background:var(--success);
    box-shadow:0 0 8px var(--success);animation:plow 1.5s infinite;display:inline-block;margin-right:6px;}

  .ip-card{background:var(--bg3);border:1px solid var(--border);border-radius:3px;padding:9px 11px;margin-bottom:7px;}
  .ip-addr{font-family:var(--mono);font-size:14px;color:var(--accent2);font-weight:bold;}
  .ip-meta{font-size:13px;color:var(--text2);margin-top:2px;}
  .abar{height:4px;border-radius:2px;margin-top:5px;transition:width 1.2s;}
  .ip-btn{padding:4px 10px;border-radius:2px;font-family:var(--mono);font-size:12px;cursor:pointer;
    border:1px solid var(--danger);color:var(--danger);background:rgba(255,51,85,.09);transition:all .15s;margin-top:5px;}
  .ip-btn:hover{background:rgba(255,51,85,.22);}

  .crow{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
  .cn{font-family:var(--mono);font-size:12px;color:var(--text2);width:70px;flex-shrink:0;font-weight:600;}
  .cbar{flex:1;height:7px;background:var(--bg3);border-radius:3px;overflow:hidden;}
  .cfill{height:100%;border-radius:3px;transition:width 1.2s;}
  .cpct{font-family:var(--mono);font-size:12px;color:var(--text);width:36px;text-align:right;font-weight:bold;}

  .inc-card{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:11px 13px;margin-bottom:8px;border-left:4px solid;}
  .inc-card.CRITICAL{border-left-color:var(--danger)}.inc-card.HIGH{border-left-color:#ff7755}
  .inc-card.MEDIUM{border-left-color:var(--warn)}.inc-card.LOW{border-left-color:var(--success)}
  .inc-title{font-size:14px;color:var(--text);font-weight:700;margin-bottom:3px;}
  .inc-meta{font-family:var(--mono);font-size:12px;color:var(--text2);}
  .inc-score{float:right;font-family:var(--mono);font-size:14px;color:var(--warn);font-weight:bold;}
  .tl-item{display:flex;gap:8px;margin:4px 0;font-family:var(--mono);font-size:12px;color:var(--text2);}
  .tl-dot{width:7px;height:7px;border-radius:50%;margin-top:3px;flex-shrink:0;}
  .tC{background:var(--danger)}.tH{background:#ff7755}.tM{background:var(--warn)}.tL{background:var(--success)}
  .act-btn{padding:5px 12px;font-family:var(--mono);font-size:12px;border-radius:3px;cursor:pointer;
    border:1px solid;transition:all .15s;margin-right:4px;margin-top:6px;font-weight:600;}
  .ab-block{color:var(--danger);border-color:var(--danger);background:rgba(255,51,85,.09);}
  .ab-block:hover{background:rgba(255,51,85,.22);}
  .ab-iso{color:var(--warn);border-color:var(--warn);background:rgba(255,187,0,.09);}
  .ab-iso:hover{background:rgba(255,187,0,.22);}

  .fmt-btn{padding:6px 11px;background:var(--bg3);border:1px solid var(--border2);border-radius:3px;
    font-family:var(--mono);font-size:12px;color:var(--text2);cursor:pointer;transition:all .15s;font-weight:600;}
  .fmt-btn:hover{border-color:var(--accent2);color:var(--accent);}
  .fmt-btn.active{border-color:var(--accent);color:var(--accent);background:rgba(0,212,255,.1);}

  .modal-backdrop{display:none;position:fixed;inset:0;z-index:200;background:rgba(0,0,0,.82);
    backdrop-filter:blur(5px);align-items:center;justify-content:center;}
  .modal-backdrop.open{display:flex;}
  .modal{background:var(--panel2);border:1px solid var(--border2);border-radius:5px;
    width:740px;max-width:95vw;max-height:84vh;display:flex;flex-direction:column;
    box-shadow:0 24px 90px rgba(0,0,0,.75);animation:min .25s cubic-bezier(.22,1,.36,1);}
  .mhdr{padding:16px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
  .mtitle{font-family:var(--mono);font-size:13px;color:var(--accent);letter-spacing:2px;text-transform:uppercase;font-weight:bold;}
  .mclose{background:none;border:none;color:var(--text2);font-size:20px;cursor:pointer;padding:2px 7px;border-radius:2px;line-height:1;}
  .mclose:hover{color:var(--danger);background:rgba(255,51,85,.12);}
  .mbody{padding:20px;overflow-y:auto;flex:1;}
  .mfoot{padding:13px 20px;border-top:1px solid var(--border);display:flex;gap:8px;justify-content:flex-end;}
  .mono-block{background:var(--bg);border:1px solid var(--border);border-radius:3px;padding:16px;
    font-family:var(--mono);font-size:13px;line-height:1.75;overflow-x:auto;white-space:pre;color:var(--accent3);}

  .toast{position:fixed;bottom:22px;right:22px;z-index:400;padding:11px 18px;background:var(--panel2);
    border:1px solid var(--accent2);border-radius:4px;font-family:var(--mono);font-size:13px;color:var(--accent);
    box-shadow:0 8px 30px rgba(0,0,0,.5);transform:translateY(70px);opacity:0;
    transition:all .3s cubic-bezier(.22,1,.36,1);pointer-events:none;}
  .toast.show{transform:translateY(0);opacity:1;}
  /* NIS2 report button */
  .nis2-btn{width:100%;margin-top:6px;background:rgba(255,187,0,.1);color:var(--warn);border-color:var(--warn);}
  .nis2-btn:hover{background:rgba(255,187,0,.22);box-shadow:0 0 16px rgba(255,187,0,.25);}
  /* Notebook & Art21 buttons */
  .nb-btn{padding:3px 9px;font-family:var(--mono);font-size:11px;border-radius:2px;cursor:pointer;
    border:1px solid var(--accent3);color:var(--accent3);background:rgba(0,255,136,.07);transition:all .15s;margin-right:3px;}
  .nb-btn:hover{background:rgba(0,255,136,.18);}
  /* NIS2 template cards */
  .nis2-tpl-card{padding:12px 16px;background:var(--bg3);border:1px solid var(--border2);border-radius:4px;cursor:pointer;transition:all .2s;}
  .nis2-tpl-card:hover{border-color:var(--accent2);background:rgba(0,212,255,.05);}
  .nis2-tpl-card.selected{border-color:var(--warn);background:rgba(255,187,0,.06);}
  .nis2-tpl-badge{font-family:var(--mono);font-size:11px;font-weight:bold;padding:3px 10px;border:1px solid;border-radius:3px;display:inline-block;margin-bottom:6px;letter-spacing:.5px;}
  .nis2-tpl-desc{font-family:var(--ui);font-size:13px;color:var(--text2);line-height:1.55;}
  /* Art.21 quiz */
  .quiz-req{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:12px 14px;margin-bottom:10px;}
  .quiz-req-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
  .quiz-req-id{font-family:var(--mono);font-size:11px;color:var(--accent2);font-weight:bold;}
  .quiz-req-name{font-family:var(--ui);font-size:13px;color:var(--text);font-weight:600;}
  .quiz-score-bar{display:flex;gap:5px;align-items:center;margin-top:7px;}
  .quiz-score-label{font-family:var(--mono);font-size:10px;color:var(--text3);width:35px;}
  .quiz-slider{flex:1;height:4px;-webkit-appearance:none;background:var(--border2);border-radius:2px;outline:none;}
  .quiz-slider::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:var(--accent2);cursor:pointer;}
  .quiz-val{font-family:var(--mono);font-size:12px;color:var(--accent2);width:35px;text-align:right;}
  /* Notebook sections */
  .nb-section{margin-bottom:14px;padding:11px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;}
  .nb-section-title{font-family:var(--mono);font-size:12px;color:var(--accent3);letter-spacing:1px;margin-bottom:8px;text-transform:uppercase;font-weight:bold;}
  .nb-text{font-size:14px;color:var(--text);line-height:1.8;white-space:pre-wrap;}
  /* Art.21 result bars */
  .art21-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
  .art21-id{font-family:var(--mono);font-size:11px;color:var(--accent2);width:58px;flex-shrink:0;}
  .art21-name{font-size:12px;color:var(--text2);width:210px;flex-shrink:0;}
  .art21-bar{flex:1;height:7px;background:var(--bg3);border-radius:3px;overflow:hidden;}
  .art21-fill{height:100%;border-radius:3px;transition:width 1s;}
  .art21-pct{font-family:var(--mono);font-size:12px;width:36px;text-align:right;font-weight:bold;}
  .art21-status{font-family:var(--mono);font-size:10px;width:16px;text-align:center;}
  /* Rule alert cards */
  .rule-card{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:10px 13px;margin-bottom:8px;}
  .rule-card.CRITICAL{border-left:4px solid var(--danger);}
  .rule-card.HIGH{border-left:4px solid #ff7755;}
  .rule-card.MEDIUM{border-left:4px solid var(--warn);}
  .rule-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
  .rule-name{font-size:13px;color:var(--text);font-weight:700;}
  .rule-meta{font-family:var(--mono);font-size:11px;color:var(--text3);}
  .rule-rem{font-size:12px;color:var(--text2);margin-top:5px;padding:5px 8px;background:rgba(0,212,255,.04);border:1px solid var(--border);border-radius:2px;}
  /* NIS2 modal content */
  .nis2-section{margin-bottom:18px;padding:14px 16px;background:var(--bg3);border:1px solid var(--border);border-radius:4px;}
  .nis2-section-title{font-family:var(--mono);font-size:13px;color:var(--warn);letter-spacing:1px;margin-bottom:9px;text-transform:uppercase;font-weight:bold;}
  .nis2-text{font-size:15px;color:var(--text);line-height:1.8;white-space:pre-wrap;}
  .nis2-spinner{display:none;text-align:center;padding:36px;font-family:var(--mono);font-size:14px;color:var(--accent2);}
  .nis2-spinner.on{display:block;}
  .nis2-dots span{animation:db 1.2s infinite;display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--accent2);margin:0 3px;}
  .nis2-dots span:nth-child(2){animation-delay:.2s}.nis2-dots span:nth-child(3){animation-delay:.4s}
</style>
</head>
<body>

<header>
  <div><div class="brand-main">SENTRASEC v2.0</div><div class="brand-sub">LOCAL · AI SOC Assistant · Offline LLM</div></div>
  <div style="display:flex;align-items:center;gap:14px;">
    <div class="threat-indicator">
      <div class="threat-pulse" id="tPulse"></div>
      <div><div style="font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;">THREAT</div>
      <div class="threat-level-text" id="tText">LOW</div></div>
    </div>
    <div class="model-selector">
      <div class="model-label">MODEL</div>
      <select id="modelSelect" onchange="setModel(this.value)"><option>llama3</option></select>
      <span class="ollama-badge offline" id="ollamaBadge" onclick="retryOllama()" title="Kliknij aby ponowić połączenie">OFFLINE</span>
    </div>
    <div style="display:flex;gap:12px;">
      <div class="sdot"><i id="dotEngine" class="ok"></i>ENGINE</div>
      <div class="sdot"><i id="dotOllama" class="err"></i>OLLAMA</div>
      <div class="sdot"><i id="dotRag" class="warn"></i>RAG</div>
    </div>
  </div>
  <div style="text-align:right;">
    <div class="clock-time" id="cTime">--:--:--</div>
    <div class="clock-date" id="cDate">----/--/--</div>
    <div class="clock-utc"  id="cUtc">UTC</div>
  </div>
</header>

<div class="app-body">

<!-- LEFT -->
<div class="sidebar-left">
  <div class="ph">Dashboard</div>
  <div class="sgrid">
    <div class="scard d"><div class="sv" id="sCrit">0</div><div class="sl">Critical</div></div>
    <div class="scard w"><div class="sv" id="sHigh">0</div><div class="sl">High</div></div>
    <div class="scard">  <div class="sv" id="sMed">0</div> <div class="sl">Medium</div></div>
    <div class="scard o"><div class="sv" id="sLow">0</div>  <div class="sl">Low/Info</div></div>
  </div>
  <div class="sep"></div>
  <div class="tabs" style="flex-wrap:wrap;">
    <button class="tab active" onclick="sw(this,'tLog')" style="flex:0 0 25%;">INPUT</button>
    <button class="tab" onclick="sw(this,'tInc')" style="flex:0 0 25%;">INCIDENTS</button>
    <button class="tab" onclick="sw(this,'tSrc')" style="flex:0 0 25%;">SOURCES</button>
    <button class="tab" onclick="sw(this,'tHist')" style="flex:0 0 25%;">HISTORY</button>
    <button class="tab" onclick="sw(this,'tSearch')" style="flex:0 0 33.3%;">SEARCH</button>
    <button class="tab" onclick="sw(this,'tRag')" style="flex:0 0 33.3%;">RAG KB</button>
    <button class="tab" onclick="sw(this,'tUeba')" style="flex:0 0 33.3%;">UEBA</button>
  </div>

  <div class="tc active" id="tLog">
    <div class="linput">
      <label style="font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;text-transform:uppercase;font-weight:600;">Log Data — Paste or Upload</label>
      <textarea id="logRaw" placeholder="Wklej logi: auth.log, syslog, nginx, firewall, suricata...&#10;&#10;Obsługiwane formaty: Syslog RFC3164, ISO8601, DateTime, Unix timestamp, UFW, SSH, Apache/Nginx, IDS/IPS..."></textarea>
      <div class="brow"><button class="btn bp" style="flex:2" onclick="doAnalyze()">⬡ ANALYZE + LOCAL AI</button><button class="btn bs" onclick="doParse()">PARSE</button></div>
      <div class="brow"><button class="btn bs" onclick="loadSample()">SAMPLE</button><button class="btn bs" onclick="document.getElementById('logRaw').value=''">CLR</button></div>
      <!-- Multi-file upload drop zone -->
      <div id="dropZone" onclick="document.getElementById('fileUpload').click()"
        style="margin-top:8px;border:2px dashed var(--border2);border-radius:4px;padding:12px;text-align:center;cursor:pointer;transition:all .2s;background:var(--bg3);"
        ondragover="event.preventDefault();this.style.borderColor='var(--accent2)'"
        ondragleave="this.style.borderColor='var(--border2)'"
        ondrop="handleDrop(event)">
        <div style="font-family:var(--mono);font-size:11px;color:var(--text3);">⬆ Drag &amp; Drop log files here</div>
        <div style="font-family:var(--mono);font-size:10px;color:var(--muted);margin-top:3px;">or click · multi-file · .log .txt .json</div>
        <input type="file" id="fileUpload" multiple accept=".log,.txt,.json,.gz" style="display:none" onchange="handleFileUpload(this)">
      </div>
      <div id="uploadStatus" style="font-family:var(--mono);font-size:11px;color:var(--accent3);margin-top:4px;"></div>
    </div>
  </div>

  <div class="tc scrollable" id="tInc">
    <div style="padding:10px;" id="incList"><div style="font-family:var(--mono);font-size:13px;color:var(--text2);">Brak incydentów.</div></div>
  </div>

  <!-- SOURCES — file tailer + presets -->
  <div class="tc scrollable" id="tSrc">
    <div style="padding:10px;">
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);font-weight:bold;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Source Presets</div>
      <div id="presetList" style="margin-bottom:10px;"></div>
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);font-weight:bold;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;margin-top:8px;">Custom File Tail</div>
      <div style="display:flex;gap:5px;margin-bottom:6px;">
        <input type="text" id="tailPathInput" placeholder="/var/log/auth.log"
          style="flex:1;font-family:var(--mono);font-size:11px;padding:6px 8px;color:var(--text);">
        <button class="btn bp" style="padding:6px 10px;font-size:11px;" onclick="addTailSource()">ADD</button>
      </div>
      <div id="tailList"><div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Brak aktywnych źródeł.</div></div>
      <div style="margin-top:10px;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;">
        <div style="font-family:var(--mono);font-size:11px;color:var(--text2);font-weight:bold;margin-bottom:4px;">HTTP Ingest (Filebeat/Fluent Bit)</div>
        <div style="font-family:var(--mono);font-size:10px;color:var(--text3);line-height:1.6;">
          POST <span style="color:var(--accent3);" id="ingestUrl">http://localhost:5000/api/ingest</span><br>
          Header: <span style="color:var(--accent2);">X-API-Key: <span id="apiKeyPreview">...</span></span><br>
          Body: JSON lines or plain text
        </div>
        <button class="btn bs" style="margin-top:5px;font-size:10px;padding:4px 8px;" onclick="copyIngestConfig()">COPY FILEBEAT CONFIG</button>
      </div>
    </div>
  </div>

  <!-- SESSION HISTORY -->
  <div class="tc scrollable" id="tHist">
    <div style="padding:10px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div style="font-family:var(--mono);font-size:12px;color:var(--text2);font-weight:bold;text-transform:uppercase;letter-spacing:1px;">Session History</div>
        <button class="btn bs" style="font-size:10px;padding:4px 8px;" onclick="loadHistory()">REFRESH</button>
      </div>
      <div id="historyList"><div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Ładowanie...</div></div>
    </div>
  </div>

  <!-- FTS SEARCH -->
  <div class="tc scrollable" id="tSearch">
    <div style="padding:10px;">
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);font-weight:bold;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Full-Text Search (FTS5)</div>
      <div style="display:flex;gap:5px;margin-bottom:8px;">
        <input type="text" id="searchInput" placeholder="brute force, 198.51.100.7, CRITICAL..."
          style="flex:1;font-family:var(--mono);font-size:12px;padding:7px 9px;color:var(--text);"
          onkeydown="if(event.key==='Enter')doSearch()">
        <button class="btn bp" style="padding:7px 12px;font-size:11px;" onclick="doSearch()">⬡</button>
      </div>
      <div style="font-family:var(--mono);font-size:10px;color:var(--text3);margin-bottom:8px;">FTS5: word1 word2 · "exact phrase" · word* · col:value</div>
      <div id="searchResults"><div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Wpisz zapytanie i naciśnij Enter</div></div>
    </div>
  </div>

  <div class="tc scrollable" id="tRag">
    <div style="padding:11px;">
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;margin-bottom:9px;font-weight:bold;text-transform:uppercase;">BAZA WIEDZY SOC (RAG)</div>
      <div style="display:flex;gap:4px;margin-bottom:9px;flex-wrap:wrap;" id="ragCatBtns">
        <button class="fmt-btn active" onclick="filterRag(this,'')">ALL</button>
        <button class="fmt-btn" onclick="filterRag(this,'mitre')">MITRE</button>
        <button class="fmt-btn" onclick="filterRag(this,'playbook')">PLAYBOOK</button>
        <button class="fmt-btn" onclick="filterRag(this,'compliance')">COMPLY</button>
        <button class="fmt-btn" onclick="filterRag(this,'hardening')">HARDEN</button>
      </div>
      <div id="ragList"></div>
    </div>
  </div>

  <div class="tc scrollable" id="tUeba">
    <div style="padding:11px;" id="uebaList"><div style="font-family:var(--mono);font-size:13px;color:var(--text2);">Brak anomalii UEBA.</div></div>
  </div>
</div>

<!-- CHAT -->
<div class="chat">
  <div class="chat-hdr">
    <div class="chat-title">// SOC ANALYST CONSOLE — LOCAL LLM + RAG</div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);" id="sessLabel">SESSION: ----</div>
  </div>
  <div class="msgs" id="msgs">
    <div style="background:var(--bg3);border:1px solid var(--border2);border-radius:5px;padding:22px;text-align:center;">
      <div style="font-family:var(--head);font-weight:800;font-size:18px;color:var(--accent);letter-spacing:2px;margin-bottom:8px;">⬡ SENTRASEC v2.0 LOCAL — ONLINE</div>
      <div style="font-size:15px;color:var(--text2);line-height:1.75;">Lokalny LLM (Ollama) + RAG · 100% offline · Pełna prywatność danych</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:14px;text-align:left;">
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> Lokalny LLM (llama3/mistral/phi3)</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> RAG — Baza wiedzy SOC</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> Real-time File Tailer</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> HTTP Ingest (Filebeat/Fluent Bit)</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> Multi-file Upload + Drag&amp;Drop</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> FTS5 Full-Text Search</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> Session History + Export/Import</div>
        <div style="padding:9px 11px;background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--text2);"><span style="color:var(--accent)">⬡</span> Source Presets + Rate Limiting</div>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(255,187,0,.06);border:1px solid rgba(255,187,0,.25);border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--warn);">
        ⚑ Wymaga: Ollama + model (llama3/mistral). Uruchom: <code style="color:var(--accent3);">ollama serve</code>
      </div>
    </div>
  </div>
  <div class="typing" id="typing">
    <div class="mav ai">AI</div>
    <div><div class="tdots"><span></span><span></span><span></span></div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-top:4px;letter-spacing:1px;">Lokalny LLM analizuje...</div></div>
  </div>
  <div class="cinput">
    <div class="irow">
      <textarea id="chatIn" rows="1" placeholder="Zadaj pytanie — lokalny LLM odpowie bez dostępu do internetu..." onkeydown="handleKey(event)" oninput="autoGrow(this)"></textarea>
      <button class="sbtn" id="sendBtn" onclick="sendMsg()">➤</button>
    </div>
    <div class="hints-row">
      <span class="hint" onclick="ins('Przeanalizuj logi i opowiedz historię ataku')">Story ataku</span>
      <span class="hint" onclick="ins('Zmapuj wykryte techniki MITRE ATT&CK')">MITRE map</span>
      <span class="hint" onclick="ins('Jakie środki zaradcze powinienem zastosować?')">Remediation</span>
      <span class="hint" onclick="ins('Oceń compliance NIST CSF dla wykrytych zdarzeń')">NIST CSF</span>
      <span class="hint" onclick="ins('Podsumuj wszystkie incydenty i priorytetyzuj działania')">Summary</span>
    </div>
  </div>
</div>

<!-- RIGHT -->
<div class="sidebar-right">
  <div class="ph" style="justify-content:space-between;">
    <span><span class="stream-live-dot"></span>Live Log Stream</span>
    <span style="font-size:10px;color:var(--text3);letter-spacing:0;" id="streamCount">0 events</span>
  </div>
  <div class="stream-stats" id="streamStats">
    <div class="ss-item ss-crit"><div class="ss-num" id="scCrit">0</div><div class="ss-lbl">CRIT</div></div>
    <div class="ss-item ss-warn"><div class="ss-num" id="scWarn">0</div><div class="ss-lbl">WARN</div></div>
    <div class="ss-item ss-info"><div class="ss-num" id="scInfo">0</div><div class="ss-lbl">INFO</div></div>
    <div class="ss-item" style="border-color:rgba(0,212,255,.2);background:rgba(0,212,255,.04);">
      <div class="ss-num" id="scErr" style="color:#ff7755;">0</div><div class="ss-lbl">ERR</div></div>
  </div>
  <div class="logstream" id="logStream"></div>
  <div class="sep"></div>
  <div style="padding:11px;">
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;text-transform:uppercase;margin-bottom:7px;font-weight:bold;">Compliance Score</div>
    <div id="compBars">
      <div class="crow"><span class="cn">NIST CSF</span><div class="cbar"><div class="cfill" id="cN" style="width:78%;background:var(--success)"></div></div><span class="cpct" id="cNp">78%</span></div>
      <div class="crow"><span class="cn">ISO 27001</span><div class="cbar"><div class="cfill" id="cI" style="width:65%;background:var(--warn)"></div></div><span class="cpct" id="cIp">65%</span></div>
      <div class="crow"><span class="cn">PCI DSS</span><div class="cbar"><div class="cfill" id="cP" style="width:82%;background:var(--success)"></div></div><span class="cpct" id="cPp">82%</span></div>
      <div class="crow"><span class="cn">GDPR</span><div class="cbar"><div class="cfill" id="cG" style="width:55%;background:var(--danger)"></div></div><span class="cpct" id="cGp">55%</span></div>
    </div>
  </div>
  <div class="sep"></div>
  <div style="padding:11px;">
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);letter-spacing:1px;text-transform:uppercase;margin-bottom:7px;font-weight:bold;">Export Report</div>
    <div style="display:flex;gap:4px;margin-bottom:7px;" id="fmtBtns">
      <button class="fmt-btn active" onclick="selFmt(this,'html')">HTML</button>
      <button class="fmt-btn" onclick="selFmt(this,'txt')">TXT</button>
      <button class="fmt-btn" onclick="selFmt(this,'json')">JSON</button>
    </div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:5px;font-weight:600;">Standard:</div>
    <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:7px;" id="stdBtns">
      <button class="fmt-btn active" onclick="selStd(this,'all')">ALL</button>
      <button class="fmt-btn" onclick="selStd(this,'nist')">NIST</button>
      <button class="fmt-btn" onclick="selStd(this,'iso')">ISO</button>
      <button class="fmt-btn" onclick="selStd(this,'pci')">PCI</button>
      <button class="fmt-btn" onclick="selStd(this,'gdpr')">GDPR</button>
    </div>
    <button class="btn bp" style="width:100%;" onclick="dlReport()">GENERATE REPORT</button>
    <button class="btn bp nis2-btn" onclick="openNis2TemplateModal()">⬡ RAPORT NIS2 — AI (24h/72h/1M)</button>
    <div class="sep" style="margin:8px 0;"></div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:5px;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Detekcja & Compliance</div>
    <div style="display:flex;gap:4px;flex-wrap:wrap;">
      <button class="btn bs" style="flex:1;font-size:11px;" onclick="runRulesModal()">⬡ REGUŁY (20)</button>
      <button class="btn bs" style="flex:1;font-size:11px;" onclick="openArt21()">⬡ ART.21 QUIZ</button>
    </div>
    <div class="sep" style="margin:8px 0;"></div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:5px;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Session</div>
    <div style="display:flex;gap:4px;">
      <button class="btn bs" style="flex:1;font-size:11px;" onclick="exportSession(S.session)">⬇ EXPORT</button>
      <button class="btn bs" style="flex:1;font-size:11px;" onclick="importSession()">⬆ IMPORT</button>
    </div>
  </div>
</div>

</div><!-- app-body -->

<!-- PARSE MODAL -->
<div class="modal-backdrop" id="parseModal">
  <div class="modal">
    <div class="mhdr"><span class="mtitle">Parsed Log Structure — MITRE ATT&CK</span><button class="mclose" onclick="closeM('parseModal')">✕</button></div>
    <div class="mbody"><div id="parsedOut"></div></div>
    <div class="mfoot"><button class="btn bs" onclick="closeM('parseModal')">CLOSE</button><button class="btn bp" onclick="closeM('parseModal');doAnalyze()">ANALYZE WITH LOCAL AI</button></div>
  </div>
</div>

<!-- PLAYBOOK MODAL -->
<div class="modal-backdrop" id="pbModal">
  <div class="modal" style="max-width:500px;">
    <div class="mhdr"><span class="mtitle" id="pbTitle">Playbook Action</span><button class="mclose" onclick="closeM('pbModal')">✕</button></div>
    <div class="mbody"><div id="pbOut"></div></div>
    <div class="mfoot"><button class="btn bs" onclick="closeM('pbModal')">CLOSE</button></div>
  </div>
</div>

<!-- NIS2 MODAL -->
<div class="modal-backdrop" id="nis2Modal">
  <div class="modal" style="width:820px;max-width:97vw;max-height:90vh;">
    <div class="mhdr">
      <span class="mtitle" style="color:var(--warn);">⬡ Raport NIS2 — Dyrektywa UE 2022/2555 — Analiza AI</span>
      <div style="display:flex;gap:8px;align-items:center;">
        <span id="nis2ModelBadge" style="font-family:var(--mono);font-size:12px;color:var(--text2);"></span>
        <button class="mclose" onclick="closeM('nis2Modal')">✕</button>
      </div>
    </div>
    <div class="mbody">
      <div class="nis2-spinner" id="nis2Spinner">
        <div class="nis2-dots"><span></span><span></span><span></span></div>
        <div style="margin-top:12px;">Lokalny LLM generuje raport NIS2...<br>
        <span style="font-size:13px;color:var(--text2);">Może to potrwać do 60–120 sekund</span></div>
      </div>
      <div id="nis2Content"></div>
    </div>
    <div class="mfoot">
      <button class="btn bs" onclick="closeM('nis2Modal')">ZAMKNIJ</button>
      <button class="btn bs" onclick="copyNis2()">📋 KOPIUJ TEKST</button>
      <button class="btn bs" onclick="downloadNis2()">⬇ POBIERZ TXT</button>
      <button class="btn bp" style="background:rgba(0,51,153,.8);border-color:#0033cc;" onclick="downloadNis2Html()">🖨 OTWÓRZ PDF</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<!-- INVESTIGATION NOTEBOOK MODAL -->
<div class="modal-backdrop" id="notebookModal">
  <div class="modal" style="width:860px;max-width:97vw;max-height:91vh;">
    <div class="mhdr">
      <span class="mtitle" style="color:var(--accent3);">⬡ AI Investigation Notebook</span>
      <div style="display:flex;gap:8px;align-items:center;">
        <span id="nbIncTitle" style="font-family:var(--mono);font-size:11px;color:var(--text3);"></span>
        <button class="mclose" onclick="closeM('notebookModal')">✕</button>
      </div>
    </div>
    <div class="mbody">
      <div id="nbSpinner" style="display:none;text-align:center;padding:36px;font-family:var(--mono);font-size:13px;color:var(--accent2);">
        <div style="margin-bottom:10px;">AI Tier-1 Analyst analizuje incydent...</div>
        <div style="font-size:11px;color:var(--text3);">LLM + RAG · może potrwać 60-120s</div>
      </div>
      <div id="nbContent"></div>
    </div>
    <div class="mfoot">
      <button class="btn bs" onclick="closeM('notebookModal')">ZAMKNIJ</button>
      <button class="btn bs" onclick="copyNotebook()">📋 KOPIUJ</button>
      <button class="btn bp" onclick="downloadNotebook()">⬇ POBIERZ TXT</button>
      <button class="btn bp" style="background:rgba(0,255,136,.15);border-color:var(--success);color:var(--success);" onclick="openNotebookPdf()">🖨 PDF</button>
    </div>
  </div>
</div>

<!-- ART.21 QUIZ MODAL -->
<div class="modal-backdrop" id="art21Modal">
  <div class="modal" style="width:780px;max-width:97vw;max-height:91vh;">
    <div class="mhdr">
      <span class="mtitle" style="color:var(--warn);">⬡ Self-Assessment Art. 21 NIS2</span>
      <button class="mclose" onclick="closeM('art21Modal')">✕</button>
    </div>
    <div class="mbody">
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:14px;padding:9px 12px;background:rgba(255,187,0,.06);border:1px solid rgba(255,187,0,.2);border-radius:3px;">
        Ocena zgodności z 10 minimalnymi wymaganiami NIS2 Art. 21 (2022/2555) + KSC.<br>
        Odpowiedz na pytania, a AI porówna wyniki z analizą Twoich logów.
      </div>
      <div id="art21QuizContent"></div>
      <div id="art21ResultContent" style="display:none;"></div>
    </div>
    <div class="mfoot">
      <button class="btn bs" onclick="closeM('art21Modal')">ZAMKNIJ</button>
      <div id="art21FootBtns">
        <button class="btn bp" style="background:rgba(255,187,0,.2);border-color:var(--warn);color:var(--warn);" onclick="submitArt21()">⬡ OCEŃ ZGODNOŚĆ</button>
      </div>
    </div>
  </div>
</div>

<!-- NIS2 TEMPLATE SELECTOR MODAL -->
<div class="modal-backdrop" id="nis2TemplateModal">
  <div class="modal" style="width:680px;max-width:95vw;max-height:88vh;">
    <div class="mhdr">
      <span class="mtitle" style="color:var(--warn);">⬡ Wybierz szablon raportu NIS2</span>
      <button class="mclose" onclick="closeM('nis2TemplateModal')">✕</button>
    </div>
    <div class="mbody">
      <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-bottom:14px;">
        Zgodnie z Art. 23 NIS2 — wybierz typ raportu do wygenerowania przez AI.
      </div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <div class="nis2-tpl-card" onclick="selectTemplate('24h')" id="tpl24h">
          <div class="nis2-tpl-badge" style="background:rgba(255,51,85,.15);border-color:var(--danger);color:var(--danger);">WCZESNE OSTRZEŻENIE · 24H</div>
          <div class="nis2-tpl-desc">Art. 23(4)(a) — Wstępne powiadomienie CSIRT NASK w ciągu 24h od wykrycia znaczącego incydentu. Krótki formularz z pierwszymi informacjami.</div>
        </div>
        <div class="nis2-tpl-card" onclick="selectTemplate('72h')" id="tpl72h">
          <div class="nis2-tpl-badge" style="background:rgba(255,187,0,.15);border-color:var(--warn);color:var(--warn);">ZGŁOSZENIE INCYDENTU · 72H</div>
          <div class="nis2-tpl-desc">Art. 23(4)(b) — Pełne zgłoszenie do CSIRT w ciągu 72h. Opis techniczny, wpływ, podjęte działania.</div>
        </div>
        <div class="nis2-tpl-card" onclick="selectTemplate('final')" id="tmpFinal">
          <div class="nis2-tpl-badge" style="background:rgba(0,255,136,.1);border-color:var(--success);color:var(--success);">RAPORT KOŃCOWY · 1 MIESIĄC</div>
          <div class="nis2-tpl-desc">Art. 23(4)(c) — Kompletny raport po zakończeniu incydentu. Root cause, lessons learned, plan poprawy.</div>
        </div>
      </div>
      <div style="margin-top:14px;display:flex;flex-direction:column;gap:7px;">
        <div style="display:flex;gap:8px;align-items:center;">
          <label style="font-family:var(--mono);font-size:11px;color:var(--text2);width:130px;">Nazwa organizacji:</label>
          <input type="text" id="orgName" value="[Nazwa podmiotu]" style="flex:1;font-family:var(--mono);font-size:12px;padding:6px 9px;color:var(--text);">
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <label style="font-family:var(--mono);font-size:11px;color:var(--text2);width:130px;">Typ podmiotu:</label>
          <select id="orgType" style="flex:1;font-family:var(--mono);font-size:12px;padding:6px 9px;color:var(--text);background:var(--bg);border:1px solid var(--border);">
            <option>podmiot ważny</option>
            <option>podmiot kluczowy</option>
            <option>dostawca usług cyfrowych</option>
            <option>operator usług kluczowych</option>
          </select>
        </div>
      </div>
    </div>
    <div class="mfoot">
      <button class="btn bs" onclick="closeM('nis2TemplateModal')">ANULUJ</button>
      <button class="btn bp" style="background:rgba(255,187,0,.2);border-color:var(--warn);color:var(--warn);" onclick="genNis2FromTemplate()">⬡ GENERUJ RAPORT AI</button>
    </div>
  </div>
</div>

<!-- RULESET ALERTS MODAL -->
<div class="modal-backdrop" id="rulesModal">
  <div class="modal" style="width:800px;max-width:97vw;max-height:88vh;">
    <div class="mhdr">
      <span class="mtitle">⬡ Detekcja — 20 Reguł Bezpieczeństwa</span>
      <button class="mclose" onclick="closeM('rulesModal')">✕</button>
    </div>
    <div class="mbody"><div id="rulesContent"><div style="font-family:var(--mono);font-size:12px;color:var(--text2);">Uruchom analizę logów aby zobaczyć wyniki detekcji.</div></div></div>
    <div class="mfoot">
      <button class="btn bs" onclick="closeM('rulesModal')">ZAMKNIJ</button>
      <button class="btn bp" onclick="runRules()">⬡ URUCHOM REGUŁY</button>
    </div>
  </div>
</div>

<script>
const S = {session:'', parsed:[], incidents:[], ueba:[], ipIntel:{}, fmt:'html', std:'all'};

// ── INIT ──────────────────────────────────────────────────────────
async function init() {
  try {
    const r = await fetch('/api/session',{method:'POST'});
    const d = await r.json();
    S.session = d.session_id;
    document.getElementById('sessLabel').textContent = 'SESSION: ' + S.session;
  } catch(e) {
    S.session = 'LOCAL-' + Math.random().toString(36).slice(2,8).toUpperCase();
    document.getElementById('sessLabel').textContent = 'SESSION: ' + S.session + ' (fallback)';
  }
  setTimeout(checkHealth, 800);
  setInterval(checkHealth, 20000);
  startStream();
  loadRagKB();
  loadPresets();
  loadHistory();
  loadApiKeyInfo();
  setTimeout(loadTailList, 2000);
}

async function checkHealth() {
  const badge = document.getElementById('ollamaBadge');
  const dotO  = document.getElementById('dotOllama');
  try {
    const r = await fetch('/api/health');
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = await r.json();

    if(d.ollama_online) {
      badge.textContent='ONLINE'; badge.className='ollama-badge online';
      badge.title='Ollama aktywna · Kliknij aby odświeżyć';
      dotO.className='ok';
    } else {
      badge.textContent='OFFLINE'; badge.className='ollama-badge offline';
      badge.title='Ollama niedostępna — uruchom: ollama serve';
      dotO.className='err';
    }

    document.getElementById('dotRag').className = d.rag_active ? 'ok' : 'warn';

    if(d.models_available && d.models_available.length) {
      const sel = document.getElementById('modelSelect');
      const cur = d.model || sel.value;
      sel.innerHTML = d.models_available.map(m =>
        `<option${m===cur||m.startsWith(cur.split(':')[0])?' selected':''}>${m}</option>`
      ).join('');
    }
  } catch(e) {
    badge.textContent='OFFLINE'; badge.className='ollama-badge offline';
    badge.title='Błąd: ' + e.message;
    dotO.className='err';
    setTimeout(checkHealth, 5000);
  }
}

async function retryOllama() {
  const badge = document.getElementById('ollamaBadge');
  badge.textContent = '...'; badge.className = 'ollama-badge offline';
  showToast('Sprawdzam połączenie z Ollama...');
  try {
    const r = await fetch('/api/ollama/test');
    const d = await r.json();
    if(d.overall) {
      showToast('✓ Ollama ONLINE · Modele: ' + (d.models||[]).join(', '));
    } else {
      const failed = (d.steps||[]).find(s=>!s.ok);
      const tip = failed ? failed.detail : 'Uruchom: ollama serve';
      showToast('✗ Ollama — ' + tip.slice(0,80));
      addMsg('ai',
        '**Diagnoza połączenia Ollama:**\n\n' +
        (d.steps||[]).map(s=>`${s.ok?'✓':'✗'} **${s.step}** — ${s.detail}`).join('\n') +
        '\n\n**Rozwiązanie:**\n1. Otwórz nowy terminal\n2. Wpisz: `ollama serve`\n3. Kliknij OFFLINE badge ponownie'
      );
    }
  } catch(e) {
    showToast('Błąd: ' + e.message);
  }
  await checkHealth();
}

async function setModel(model) {
  try {
    await fetch('/api/ollama/set_model',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model})});
    showToast('Model zmieniony: '+model);
    setTimeout(checkHealth, 500);
  } catch(e) { showToast('Blad zmiany modelu: '+e.message); }
}

// ── CLOCK ──────────────────────────────────────────────────────────
function tick() {
  const n=new Date(),p=x=>String(x).padStart(2,'0');
  document.getElementById('cTime').textContent=`${p(n.getHours())}:${p(n.getMinutes())}:${p(n.getSeconds())}`;
  document.getElementById('cDate').textContent=`${n.getFullYear()}/${p(n.getMonth()+1)}/${p(n.getDate())}`;
  const off=-n.getTimezoneOffset(),s=off>=0?'+':'-';
  document.getElementById('cUtc').textContent=`UTC${s}${p(Math.floor(Math.abs(off)/60))}${p(Math.abs(off)%60)}`;
}
setInterval(tick,1000); tick();

// ── THREAT ────────────────────────────────────────────────────────
function setThreat(level) {
  const p=document.getElementById('tPulse'),t=document.getElementById('tText');
  p.className='threat-pulse'+(level!=='low'?' '+level:'');
  t.className='threat-level-text'+(level!=='low'?' '+level:'');
  t.textContent=level.toUpperCase();
}

// ── LIVE STREAM (SSE) ─────────────────────────────────────────────
// ── LIVE STREAM ──────────────────────────────────────────────────
const _streamCounts = {CRIT:0, WARN:0, INFO:0, ERR:0, total:0};

function startStream() {
  const es = new EventSource('/api/stream/logs');
  es.onmessage = function(e) {
    try {
      const d = JSON.parse(e.data);
      const s = document.getElementById('logStream');
      const sev = (d.sev || 'INFO').toUpperCase();

      // Update counters
      _streamCounts.total++;
      if(sev === 'CRIT')  _streamCounts.CRIT++;
      else if(sev === 'WARN') _streamCounts.WARN++;
      else if(sev === 'ERR')  _streamCounts.ERR++;
      else _streamCounts.INFO++;

      var scCrit = document.getElementById('scCrit');
      var scWarn = document.getElementById('scWarn');
      var scInfo = document.getElementById('scInfo');
      var scErr  = document.getElementById('scErr');
      var scCount= document.getElementById('streamCount');
      if(scCrit)  scCrit.textContent  = _streamCounts.CRIT;
      if(scWarn)  scWarn.textContent  = _streamCounts.WARN;
      if(scInfo)  scInfo.textContent  = _streamCounts.INFO;
      if(scErr)   scErr.textContent   = _streamCounts.ERR;
      if(scCount) scCount.textContent = _streamCounts.total + ' events';

      // Build log line
      const ln = document.createElement('div');
      ln.className = 'll ' + sev;

      // Severity label with background badge
      var sevHtml = '<span class="lsev ' + sev + '">' + sev + '</span>';

      // Source label
      var src = d.src || '';
      var msg = d.msg || '';

      // Highlight IP addresses in message
      var msgHtml = msg.replace(
        /\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/g,
        '<span style="color:var(--accent2);font-weight:bold;">$1</span>'
      );

      ln.innerHTML = '<span class="lts">' + (d.ts||'') + '</span>'
        + sevHtml
        + '<span class="lmsg"><span style="color:var(--text3);font-size:11px;">[' + src + ']</span> ' + msgHtml + '</span>';

      s.appendChild(ln);

      // Keep max 150 lines
      while(s.children.length > 150) s.removeChild(s.firstChild);
      s.scrollTop = s.scrollHeight;

      // Flash threat indicator on CRIT
      if(sev === 'CRIT') setThreat('high');
      else if(sev === 'ERR' && _streamCounts.ERR > 3) setThreat('medium');

    } catch(err) {}
  };
  es.onerror = function() { setTimeout(startStream, 3000); };
}

// ── RAG KB ────────────────────────────────────────────────────────
let ragDocs = [], ragCat = '';
async function loadRagKB() {
  try {
    const r = await fetch('/api/rag/retrieve',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({query:'security soc mitre compliance',n:20})});
    const d = await r.json();
    ragDocs = d.results || [];
    renderRag();
  } catch(e) {}
}
function filterRag(btn, cat) {
  ragCat = cat;
  document.querySelectorAll('#ragCatBtns .fmt-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderRag();
}
function renderRag() {
  const el = document.getElementById('ragList');
  const filtered = ragCat ? ragDocs.filter(d=>d.meta&&d.meta.category===ragCat) : ragDocs;
  el.innerHTML = filtered.map(d=>`<div class="rag-item">
    <div class="rag-cat">${(d.meta&&d.meta.category)||'general'}</div>
    <div class="rag-text">${d.text.slice(0,120)}...</div>
  </div>`).join('') || '<div style="font-family:var(--mono);font-size:12px;color:var(--text3);">Brak dokumentów.</div>';
}

// ── PARSE / ANALYZE ───────────────────────────────────────────────
async function doParse() {
  const raw = document.getElementById('logRaw').value.trim();
  if(!raw){showToast('Brak danych do parsowania');return;}
  showToast('Parsowanie logów...');
  try {
    const r = await fetch('/api/parse',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({logs:raw,session_id:S.session})});
    const d = await r.json();
    S.parsed=d.parsed||[]; S.incidents=d.incidents||[]; S.ipIntel=d.ip_intel||{}; S.ueba=d.ueba||[];
    renderParsed(d); renderIncidents(); renderUeba(); updateStats(d.parsed||[]);
    document.getElementById('parseModal').classList.add('open');
    showToast(`Sparsowano ${d.count} wpisów · ${d.incidents.length} incydentów`);
  } catch(e){showToast('Błąd: '+e.message);}
}

async function doAnalyze() {
  await doParse();
  document.getElementById('parseModal').classList.remove('open');
  await sendMsg('Przeanalizuj wklejone logi. Opowiedz historię ataku łącząc zdarzenia w timeline. Zmapuj na MITRE ATT&CK. Podaj priorytety i konkretne zalecenia naprawcze.');
}

function renderParsed(data) {
  const el=document.getElementById('parsedOut'); const entries=data.parsed||[];
  if(!entries.length){el.innerHTML='<div style="color:var(--text3);font-family:var(--mono);font-size:13px;">Nie wykryto struktury logów.</div>';return;}
  const clrMap={CRITICAL:'var(--danger)',HIGH:'#ff6644',MEDIUM:'var(--warn)',LOW:'var(--success)',INFO:'var(--accent2)'};
  el.innerHTML=entries.slice(0,20).map(e=>{
    const clr=clrMap[e.severity]||'var(--text)';
    const intel=S.ipIntel[e.src_ip];
    return `<div style="margin-bottom:7px;padding:7px 9px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;border-left:2px solid ${clr};">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">
        <span style="color:${clr};font-size:13px;font-weight:bold;">${e.severity}</span>
        <span style="font-family:var(--mono);font-size:13px;color:var(--accent2);">${e.log_type}</span>
        ${e.mitre_id?`<span class="mtag">${e.mitre_id} ${e.mitre_name||''}</span>`:''}
      </div>
      ${e.src_ip?`<div style="font-family:var(--mono);font-size:13px;color:var(--text2);">SRC: ${e.src_ip}${intel?` <span style="color:var(--text3)">[${intel.country}·${intel.abuse_score}]</span>`:''}</div>`:''}
      ${e.username?`<div style="font-family:var(--mono);font-size:13px;color:var(--text2);">USR: ${e.username}</div>`:''}
      ${e.event?`<div style="font-family:var(--mono);font-size:13px;color:var(--text2);">EVT: ${e.event}</div>`:''}
      <div style="font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${(e.raw||'').slice(0,85)}</div>
    </div>`;
  }).join('')+(entries.length>20?`<div style="font-family:var(--mono);font-size:12px;color:var(--muted);">+${entries.length-20} więcej...</div>`:'');
}

function renderIncidents() {
  const el=document.getElementById('incList');
  if(!S.incidents.length){el.innerHTML='<div style="font-family:var(--mono);font-size:12px;color:var(--text3);">Brak incydentów.</div>';return;}
  el.innerHTML=S.incidents.map(inc=>{
    const tl=(inc.timeline||[]).map(t=>`<div class="tl-item"><div class="tl-dot t${t.severity.charAt(0)}"></div><span>${t.log_type}${t.mitre?' ['+t.mitre+']':''} — ${(t.raw||'').slice(0,45)}</span></div>`).join('');
    const mitreT=(inc.mitre_ids||[]).map(m=>`<span class="mtag">${m}</span>`).join('');
    return `<div class="inc-card ${inc.severity}">
      <div class="inc-score">${inc.risk_score}</div>
      <div class="inc-title">${inc.title}</div>
      <div class="inc-meta">${inc.severity} · ${inc.src_ip||''} · ${inc.status||'open'}</div>
      <div style="margin-top:3px;">${mitreT}</div>
      <div style="margin-top:5px;">${tl}</div>
      <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:4px;">
        <button class="nb-btn" onclick="openNotebook(${inc.id||0},'${(inc.title||'').replace(/'/g,'')}')" title="AI Investigation Notebook">⬡ NOTEBOOK</button>
        <button class="act-btn ab-block" onclick="runPb('BLOCK_IP','${inc.src_ip||''}')">⊘ BLOCK IP</button>
        <button class="act-btn ab-iso" onclick="runPb('ISOLATE_HOST','${inc.src_ip||''}')">⊡ ISOLATE</button>
      </div>
    </div>`;
  }).join('');
  if(S.incidents.some(i=>i.severity==='CRITICAL')) setThreat('high');
  else if(S.incidents.some(i=>i.severity==='HIGH')) setThreat('medium');
  sw(document.querySelectorAll('.sidebar-left .tab')[1],'tInc');
}

function renderUeba() {
  const el=document.getElementById('uebaList');
  if(!S.ueba.length){el.innerHTML='<div style="font-family:var(--mono);font-size:12px;color:var(--text3);">Brak anomalii.</div>';return;}
  el.innerHTML=S.ueba.map(u=>`<div style="background:var(--bg3);border:1px solid ${u.risk_level==='CRITICAL'?'var(--danger)':u.risk_level==='HIGH'?'#ff6644':'var(--warn)'};border-radius:3px;padding:7px 9px;margin-bottom:5px;">
    <div style="font-size:12px;color:var(--text);font-weight:600;">${u.username} <span style="float:right;font-family:var(--mono);font-size:11px;color:var(--warn);">${u.risk_score}</span></div>
    ${(u.anomalies||[]).map(a=>`<div style="font-family:var(--mono);font-size:12px;color:var(--text3);">⚠ ${a}</div>`).join('')}
    <div style="font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:2px;">${u.src_ip||''} · ${u.country} · ${u.hour}:00</div>
  </div>`).join('');
}

function updateStats(parsed) {
  const c={CRITICAL:0,HIGH:0,MEDIUM:0,LOW:0,INFO:0};
  parsed.forEach(e=>c[e.severity]=(c[e.severity]||0)+1);
  document.getElementById('sCrit').textContent=c.CRITICAL;
  document.getElementById('sHigh').textContent=c.HIGH;
  document.getElementById('sMed').textContent=c.MEDIUM;
  document.getElementById('sLow').textContent=(c.LOW||0)+(c.INFO||0);
  // Update compliance bars based on severity
  const crit=c.CRITICAL||0, hi=c.HIGH||0;
  const comp={N:Math.max(20,85-crit*10-hi*3), I:Math.max(20,80-crit*8-hi*2), P:Math.max(20,90-crit*12-hi*4), G:Math.max(20,75-crit*8-hi*3)};
  for(const [k,v] of Object.entries(comp)) {
    const fill=document.getElementById('c'+k), pct=document.getElementById('c'+k+'p');
    if(fill){fill.style.width=v+'%';fill.style.background=v>=70?'var(--success)':v>=50?'var(--warn)':'var(--danger)';}
    if(pct) pct.textContent=v+'%';
  }
}

// ── PLAYBOOK ──────────────────────────────────────────────────────
async function runPb(action, target) {
  if(!target||target==='undefined'){showToast('Brak celu');return;}
  showToast(`Playbook: ${action} → ${target}`);
  try {
    const r=await fetch('/api/playbook',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({session_id:S.session,action,target})});
    const d=await r.json();
    document.getElementById('pbTitle').textContent=`${action}: ${target}`;
    document.getElementById('pbOut').innerHTML=`
      <div style="margin-bottom:8px;font-family:var(--mono);font-size:13px;color:var(--text2);">COMMAND:</div>
      <pre class="mono-block">${d.command}</pre>
      <div style="margin:8px 0 4px;font-family:var(--mono);font-size:13px;color:var(--text2);">RESULT:</div>
      <pre class="mono-block" style="color:var(--success);">${d.result}</pre>
      <div style="font-family:var(--mono);font-size:12px;color:var(--warn);margin-top:6px;">⚑ ${d.mode}</div>`;
    document.getElementById('pbModal').classList.add('open');
  } catch(e){showToast('Błąd: '+e.message);}
}

// ── CHAT ──────────────────────────────────────────────────────────
function addMsg(role, content) {
  const el=document.getElementById('msgs');
  const d=document.createElement('div'); d.className=`msg ${role}`;
  const now=new Date().toLocaleTimeString();
  d.innerHTML=`<div class="mav ${role}">${role==='ai'?'AI':'OP'}</div>
    <div class="mb">
      <div class="mm">${role==='ai'?'SENTRASEC LOCAL':'ANALYST'} · ${now}</div>
      <div class="mc">${fmt(content)}</div>
    </div>`;
  el.appendChild(d); el.scrollTop=el.scrollHeight;
}

function fmt(t) {
  return t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/### (.*)/g,'<h4>$1</h4>')
    .replace(/\bCRITICAL\b/g,'<span class="sC">CRITICAL</span>')
    .replace(/\bHIGH\b/g,'<span class="sH">HIGH</span>')
    .replace(/\bMEDIUM\b/g,'<span class="sM">MEDIUM</span>')
    .replace(/\bLOW\b/g,'<span class="sL">LOW</span>')
    .replace(/\bINFO\b/g,'<span class="sI">INFO</span>')
    .replace(/(T\d{4})/g,'<span class="mtag">$1</span>');
}

function typing(v) {
  document.getElementById('typing').className='typing'+(v?' on':'');
  if(v) document.getElementById('msgs').scrollTop=1e9;
}

async function sendMsg(override) {
  const inp=document.getElementById('chatIn');
  const msg=override||inp.value.trim(); if(!msg) return;
  inp.value=''; inp.style.height='auto';
  addMsg('user',msg);
  document.getElementById('sendBtn').disabled=true; typing(true);
  try {
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({session_id:S.session,message:msg,
        log_data:document.getElementById('logRaw').value,
        parsed_entries:S.parsed.slice(0,15),stream:false})});
    const d=await r.json();
    typing(false);
    addMsg('ai', d.response||'Brak odpowiedzi z lokalnego modelu.');
  } catch(e) {
    typing(false);
    addMsg('ai',`**Błąd połączenia z Ollama.**\n\nUpewnij się że serwer jest uruchomiony:\n\`ollama serve\`\n\nHost: http://localhost:11434\n\`${e.message}\``);
  }
  document.getElementById('sendBtn').disabled=false;
}

function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
function autoGrow(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,100)+'px';}
function ins(t){document.getElementById('chatIn').value=t;document.getElementById('chatIn').focus();}

// ── REPORT ────────────────────────────────────────────────────────
let selFmtV='html', selStdV='all';
function selFmt(el,f){selFmtV=f;document.querySelectorAll('#fmtBtns .fmt-btn').forEach(b=>b.classList.remove('active'));el.classList.add('active');}
function selStd(el,s){selStdV=s;document.querySelectorAll('#stdBtns .fmt-btn').forEach(b=>b.classList.remove('active'));el.classList.add('active');}
function dlReport(){
  window.open(`/api/report?session_id=${S.session}&format=${selFmtV}&standard=${selStdV}`,'_blank');
  showToast('Generowanie raportu...');
}

// ── TABS ──────────────────────────────────────────────────────────
function sw(btn,id){
  document.querySelectorAll('.sidebar-left .tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.sidebar-left .tc').forEach(t=>t.classList.toggle('active',t.id===id));
}

// ── MODAL ─────────────────────────────────────────────────────────
function closeM(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.modal-backdrop').forEach(el=>el.addEventListener('click',e=>{if(e.target===el)el.classList.remove('open');}));
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.modal-backdrop.open').forEach(m=>m.classList.remove('open'));});

// ── SAMPLE ────────────────────────────────────────────────────────
function loadSample(){
  document.getElementById('logRaw').value=`Jan 15 09:42:11 server sshd[4521]: Failed password for root from 198.51.100.7 port 54321 ssh2
Jan 15 09:42:12 server sshd[4522]: Failed password for root from 198.51.100.7 port 54322 ssh2
Jan 15 09:42:13 server sshd[4523]: Failed password for admin from 198.51.100.7 port 54323 ssh2
2024-03-15 09:42:15 WARN kernel: [UFW BLOCK] IN=eth0 SRC=198.51.100.7 DST=10.0.0.1 PROTO=TCP SPT=54321 DPT=22
2024-03-15T09:42:20.000Z ERROR 403 /wp-admin/install.php ip=198.51.100.7 ua=Nmap/7.80
Jan 15 09:42:22 server sshd[4599]: Accepted password for admin from 203.0.113.5 port 22 ssh2
2024-03-15 09:42:30 CRIT sudo: admin TTY=pts/0 PWD=/tmp USER=root COMMAND=/bin/chmod 777 /etc/shadow
Jan 15 09:42:35 server suricata: ET SCAN Nmap NSE scripts detected SRC=198.51.100.7
2024-03-15 09:43:01 WARN fail2ban.actions: Ban 198.51.100.7
1710494540 INFO vpn: OpenVPN tunnel 203.0.113.99 established AES-256-GCM`;
  showToast('Przykładowe logi załadowane');
}

// ── TOAST ─────────────────────────────────────────────────────────
function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2800);
}

// ── NIS2 REPORT ──────────────────────────────────────────────────
let nis2ReportText = '';
let nis2ReportHtml = '';

async function genNis2Report() {
  const logs = document.getElementById('logRaw').value.trim();
  if(!logs && S.parsed.length === 0){
    showToast('Brak logów — wklej dane lub wykonaj analizę przed generowaniem raportu NIS2');
    return;
  }
  document.getElementById('nis2Content').innerHTML = '';
  document.getElementById('nis2Spinner').className = 'nis2-spinner on';
  document.getElementById('nis2ModelBadge').textContent = 'MODEL: ' + (document.getElementById('modelSelect').value || 'llama3');
  document.getElementById('nis2Modal').classList.add('open');

  try {
    const r = await fetch('/api/report/nis2', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: S.session, logs: logs})
    });
    const d = await r.json();
    document.getElementById('nis2Spinner').className = 'nis2-spinner';

    nis2ReportText = d.report || 'Brak odpowiedzi z modelu.';

    // Render sekcji
    const sections = nis2ReportText.split(/^## /m).filter(s=>s.trim());
    let html = `<div style="margin-bottom:14px;padding:10px 14px;background:rgba(255,170,0,.06);border:1px solid rgba(255,170,0,.25);border-radius:3px;">
      <div style="font-family:var(--mono);font-size:13px;color:var(--warn);font-weight:bold;margin-bottom:4px;">SENTRASEC v2.0 LOCAL — Raport NIS2</div>
      <div style="font-size:13px;color:var(--text2);font-family:var(--mono);">Dyrektywa UE 2022/2555 · Sesja: ${d.session_id} · ${d.generated?.slice(0,19)||''} · Model: ${d.model}</div>
      <div style="font-size:12px;color:var(--text2);margin-top:5px;">
        CRITICAL: <span style="color:var(--danger);font-weight:bold;">${(d.sev_counts||{}).CRITICAL||0}</span> &nbsp;
        HIGH: <span style="color:#ff6644;font-weight:bold;">${(d.sev_counts||{}).HIGH||0}</span> &nbsp;
        Incydenty: <span style="color:var(--warn);font-weight:bold;">${d.incident_count||0}</span> &nbsp;
        MITRE: <span style="color:var(--accent2);">${(d.mitre||[]).join(', ')||'—'}</span>
      </div>
    </div>`;

    if(sections.length > 1) {
      sections.forEach(sec => {
        const lines  = sec.split('\n');
        const title  = lines[0].trim();
        const body   = lines.slice(1).join('\n').trim();
        html += `<div class="nis2-section">
          <div class="nis2-section-title">## ${title}</div>
          <div class="nis2-text">${fmtNis2(body)}</div>
        </div>`;
      });
    } else {
      html += `<div class="nis2-section"><div class="nis2-text">${fmtNis2(nis2ReportText)}</div></div>`;
    }
    document.getElementById('nis2Content').innerHTML = html;

    // Build HTML version for download
    nis2ReportHtml = buildNis2Html(d);
    showToast('Raport NIS2 wygenerowany pomyślnie');
  } catch(e) {
    document.getElementById('nis2Spinner').className = 'nis2-spinner';
    document.getElementById('nis2Content').innerHTML =
      `<div style="color:var(--danger);font-family:var(--mono);font-size:13px;padding:14px;">
      ⚠ Błąd generowania raportu NIS2:<br><code>${e.message}</code><br><br>
      Upewnij się że Ollama jest uruchomiona: <code>ollama serve</code></div>`;
    showToast('Błąd: ' + e.message);
  }
}

function fmtNis2(t) {
  return (t||'')
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/`([^`]+)`/g,'<code style="font-family:var(--mono);background:rgba(0,0,0,.3);padding:1px 5px;border-radius:2px;font-size:12px;color:var(--accent3);">$1</code>')
    .replace(/^- (.*)/gm,'<div style="display:flex;gap:7px;margin:2px 0;"><span style="color:var(--accent2);flex-shrink:0;">▸</span><span>$1</span></div>')
    .replace(/\bKRYTYCZNY\b|\bCRITICAL\b/g,'<span style="color:var(--danger);font-weight:bold;">KRYTYCZNY</span>')
    .replace(/\bWYSOKI\b|\bHIGH\b/g,'<span style="color:#ff6644;font-weight:bold;">WYSOKI</span>')
    .replace(/\bŚREDNI\b|\bMEDIUM\b/g,'<span style="color:var(--warn);font-weight:bold;">ŚREDNI</span>')
    .replace(/\bNISKI\b|\bLOW\b/g,'<span style="color:var(--success);">NISKI</span>')
    .replace(/(T\d{4})/g,'<span style="background:rgba(0,136,187,.15);border:1px solid rgba(0,136,187,.35);padding:1px 5px;border-radius:2px;font-family:var(--mono);font-size:11px;color:var(--accent2);">$1</span>')
    .replace(/\n/g,'<br>');
}

function buildNis2Html(d) {
  var sev   = d.sev_counts || {};
  var ts    = (d.generated || '').slice(0,19).replace('T',' ');
  var pcol  = {'KRYTYCZNY':'#cc0000','WYSOKI':'#cc4400','SREDNI':'#cc7700','NISKI':'#006600'}[d.priority] || '#333';
  var model = d.model || 'llama3';
  var rid   = d.report_id || '';
  var sid   = d.session_id || '';
  var itype = (d.incident_type || 'Cybersecurity Incident').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  var prio  = d.priority || 'NISKI';

  // Sections
  var sections = d.report ? d.report.split(/^## /m).filter(function(s){return s.trim();}) : [];
  var secColors = ['#cc0033','#003399','#cc4400','#cc7700','#006633','#330066','#005588','#333333'];
  var sectHtml = '';
  if(sections.length > 1) {
    sections.forEach(function(sec, i) {
      var lines = sec.split('\n');
      var title = lines[0].trim().replace(/</g,'&lt;').replace(/>/g,'&gt;');
      var body  = lines.slice(1).join('\n').trim()
        .replace(/</g,'&lt;').replace(/>/g,'&gt;')
        .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
        .replace(/^- (.+)/gm,'<div style="margin:3px 0;padding-left:14px;">&#9658; $1</div>')
        .replace(/\bKRYTYCZNY\b/g,'<span style="color:#cc0033;font-weight:700;">KRYTYCZNY</span>')
        .replace(/\bWYSOKI\b/g,'<span style="color:#cc4400;font-weight:700;">WYSOKI</span>')
        .replace(/\bNISKI\b/g,'<span style="color:#006600;">NISKI</span>')
        .replace(/\bTAK\b/g,'<span style="background:#e0ffe0;border:1px solid #0a0;padding:1px 7px;border-radius:3px;color:#006600;font-weight:700;">TAK</span>')
        .replace(/\bNIE\b/g,'<span style="background:#fff0f0;border:1px solid #c00;padding:1px 7px;border-radius:3px;color:#cc0033;font-weight:700;">NIE</span>')
        .replace(/(T\d{4})/g,'<span style="background:#e8eeff;border:1px solid #aabcff;padding:1px 5px;border-radius:2px;font-size:9pt;font-weight:700;color:#003399;">$1</span>')
        .replace(/\n/g,'<br>');
      var col = secColors[i % secColors.length];
      sectHtml += '<div style="margin-bottom:12px;border:1px solid #e0e4ee;border-radius:4px;border-left:5px solid ' + col + ';overflow:hidden;page-break-inside:avoid;">'
        + '<div style="padding:9px 16px;background:#f5f7ff;font-size:10.5pt;font-weight:700;letter-spacing:.5px;border-bottom:1px solid #e0e4ee;color:' + col + ';">## ' + title + '</div>'
        + '<div style="padding:12px 16px;font-size:10pt;color:#222;line-height:1.7;">' + body + '</div>'
        + '</div>';
    });
  } else {
    var raw = (d.report || '').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    sectHtml = '<div style="padding:14px;background:#fafbfc;border:1px solid #dde;border-radius:4px;font-size:10pt;line-height:1.7;white-space:pre-wrap;">' + raw + '</div>';
  }

  // MITRE tags
  var mitreNames = {'T1110':'Brute Force','T1046':'Net Scan','T1548':'Priv Escalation','T1078':'Valid Accounts','T1190':'Exploit App','T1041':'Exfil C2','T1059':'Cmd Line','T1070':'Remove Indicators','T1505':'Server Component','T1136':'Create Account','T1071':'App Layer C2','T1486':'Data Encrypted'};
  var mitreTags = (d.mitre || []).map(function(m){
    return '<span style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px;margin:2px;background:#fff;border:1px solid #003399;border-radius:3px;font-size:9pt;font-weight:700;color:#003399;">'
      + m + '<span style="font-size:8pt;font-weight:400;color:#555;">' + (mitreNames[m]||'') + '</span></span>';
  }).join('');

  // IP tags
  var ipTags = (d.ips || []).map(function(ip){
    return '<span style="display:inline-block;padding:2px 10px;margin:2px;background:#fff;border:1px solid #cc4400;border-radius:3px;font-size:9.5pt;font-weight:700;color:#cc4400;font-family:monospace;">' + ip + '</span>';
  }).join('');

  var ipsBlock = (d.ips && d.ips.length)
    ? '<div style="margin:10px 28px 0;padding:10px 16px;background:#fff8f0;border:1px solid #ffccaa;border-radius:4px;">'
      + '<div style="font-size:8.5pt;font-weight:700;color:#cc4400;letter-spacing:1px;text-transform:uppercase;margin-bottom:5px;">Attacking IP Addresses</div>'
      + ipTags + '</div>'
    : '';

  var mitreBlock = (d.mitre && d.mitre.length)
    ? '<div style="margin:12px 28px 0;padding:10px 16px;background:#f0f4ff;border:1px solid #c8d4ff;border-radius:4px;">'
      + '<div style="font-size:8.5pt;font-weight:700;color:#003399;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">MITRE ATT&CK Techniques Detected</div>'
      + mitreTags + '</div>'
    : '';

  // Build full HTML
  var h = '<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8">'
    + '<title>SentraSec NIS2 - ' + itype + ' - ' + rid + '</title>'
    + '<style>'
    + '@page{size:A4;margin:18mm 16mm;}'
    + '*{box-sizing:border-box;margin:0;padding:0;}'
    + 'body{font-family:Segoe UI,Arial,sans-serif;background:#fff;color:#1a1a2e;font-size:11pt;line-height:1.6;}'
    + '.watermark{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-35deg);font-size:72pt;font-weight:900;color:rgba(200,210,230,.1);letter-spacing:8px;pointer-events:none;z-index:0;}'
    + '@media print{button{display:none;}}'
    + '</style></head><body>'
    + '<div class="watermark">SENTRASEC</div>'
    // Header
    + '<div style="padding:18px 28px 0;display:flex;align-items:flex-end;justify-content:space-between;">'
    +   '<div>'
    +     '<div style="font-size:32pt;font-weight:900;color:#1a1a2e;letter-spacing:2px;line-height:1;">SENTRASEC</div>'
    +     '<div style="font-size:9pt;color:#0055cc;letter-spacing:1px;text-transform:uppercase;margin-top:4px;font-weight:600;">AI SOC Platform v2.0 | NIS2 Compliant Incident Report</div>'
    +   '</div>'
    +   '<div style="text-align:right;">'
    +     '<div style="font-size:8pt;color:#999;">Generated: ' + ts + ' UTC</div>'
    +     '<div style="margin-top:4px;"><span style="display:inline-block;padding:3px 12px;background:#cc0033;color:#fff;font-size:9pt;font-weight:700;letter-spacing:2px;border-radius:3px;">CONFIDENTIAL</span></div>'
    +   '</div>'
    + '</div>'
    // Blue bar
    + '<div style="height:7px;background:linear-gradient(90deg,#0033cc,#0099ff,#00ccff);margin:10px 0;"></div>'
    // Incident table
    + '<div style="margin:16px 28px 0;border:1px solid #dde;border-radius:4px;overflow:hidden;">'
    +   '<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;background:#f8f9ff;border-bottom:1px solid #dde;">'
    +     '<div style="width:5px;height:22px;background:#cc0033;border-radius:2px;flex-shrink:0;"></div>'
    +     '<div style="font-size:13pt;font-weight:700;color:#1a1a2e;letter-spacing:.5px;text-transform:uppercase;">Incident Classification</div>'
    +   '</div>'
    +   '<table style="width:100%;border-collapse:collapse;">'
    +   '<tr><td style="padding:7px 16px;font-weight:600;color:#555;width:160px;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Incident Type</td><td style="padding:7px 16px;border-bottom:1px solid #eef;font-weight:500;"><strong>' + itype + '</strong></td></tr>'
    +   '<tr style="background:#f9fafe;"><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Report ID</td><td style="padding:7px 16px;border-bottom:1px solid #eef;font-family:monospace;font-weight:700;color:#003399;">' + rid + '</td></tr>'
    +   '<tr><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Classification</td><td style="padding:7px 16px;border-bottom:1px solid #eef;"><span style="display:inline-block;padding:3px 12px;background:#cc0033;color:#fff;font-size:9pt;font-weight:700;letter-spacing:2px;border-radius:3px;">CONFIDENTIAL</span></td></tr>'
    +   '<tr style="background:#f9fafe;"><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Framework</td><td style="padding:7px 16px;border-bottom:1px solid #eef;">NIS2 Directive (EU) 2022/2555</td></tr>'
    +   '<tr><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Report Date</td><td style="padding:7px 16px;border-bottom:1px solid #eef;">' + ts + '</td></tr>'
    +   '<tr style="background:#f9fafe;"><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Priority</td><td style="padding:7px 16px;border-bottom:1px solid #eef;"><span style="display:inline-block;padding:3px 12px;border-radius:3px;font-size:9pt;font-weight:700;letter-spacing:1px;color:#fff;background:' + pcol + ';">' + prio + '</span></td></tr>'
    +   '<tr><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;border-bottom:1px solid #eef;">Platform</td><td style="padding:7px 16px;border-bottom:1px solid #eef;">SentraSec v2.0 AI SOC Platform (Offline / ' + model + ')</td></tr>'
    +   '<tr style="background:#f9fafe;"><td style="padding:7px 16px;font-weight:600;color:#555;font-size:9.5pt;text-transform:uppercase;">Session ID</td><td style="padding:7px 16px;font-family:monospace;font-size:9.5pt;">' + sid + '</td></tr>'
    +   '</table>'
    + '</div>'
    // Severity cards
    + '<div style="margin:16px 28px 0;display:flex;gap:10px;">'
    +   '<div style="flex:1;padding:10px 14px;border-radius:4px;border:1px solid #cc0033;background:#fff5f5;text-align:center;"><div style="font-size:20pt;font-weight:900;color:#cc0033;line-height:1;">' + (sev.CRITICAL||0) + '</div><div style="font-size:8pt;font-weight:700;letter-spacing:1px;color:#cc0033;text-transform:uppercase;margin-top:2px;">Critical</div></div>'
    +   '<div style="flex:1;padding:10px 14px;border-radius:4px;border:1px solid #cc4400;background:#fff8f0;text-align:center;"><div style="font-size:20pt;font-weight:900;color:#cc4400;line-height:1;">' + (sev.HIGH||0) + '</div><div style="font-size:8pt;font-weight:700;letter-spacing:1px;color:#cc4400;text-transform:uppercase;margin-top:2px;">High</div></div>'
    +   '<div style="flex:1;padding:10px 14px;border-radius:4px;border:1px solid #cc7700;background:#fffbf0;text-align:center;"><div style="font-size:20pt;font-weight:900;color:#cc7700;line-height:1;">' + (sev.MEDIUM||0) + '</div><div style="font-size:8pt;font-weight:700;letter-spacing:1px;color:#cc7700;text-transform:uppercase;margin-top:2px;">Medium</div></div>'
    +   '<div style="flex:1;padding:10px 14px;border-radius:4px;border:1px solid #006600;background:#f0fff0;text-align:center;"><div style="font-size:20pt;font-weight:900;color:#006600;line-height:1;">' + ((sev.LOW||0)+(sev.INFO||0)) + '</div><div style="font-size:8pt;font-weight:700;letter-spacing:1px;color:#006600;text-transform:uppercase;margin-top:2px;">Low/Info</div></div>'
    +   '<div style="flex:1;padding:10px 14px;border-radius:4px;border:1px solid #003399;background:#f0f4ff;text-align:center;"><div style="font-size:20pt;font-weight:900;color:#003399;line-height:1;">' + (d.incident_count||0) + '</div><div style="font-size:8pt;font-weight:700;letter-spacing:1px;color:#003399;text-transform:uppercase;margin-top:2px;">Incidents</div></div>'
    + '</div>'
    + ipsBlock
    + mitreBlock
    // NIS2 Framework block
    + '<div style="margin:16px 28px 0;border:1px solid #dde;border-radius:4px;overflow:hidden;">'
    +   '<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;background:#f0f4ff;border-bottom:1px solid #dde;">'
    +     '<div style="width:5px;height:22px;background:#0033cc;border-radius:2px;flex-shrink:0;"></div>'
    +     '<div style="font-size:12pt;font-weight:700;color:#003399;letter-spacing:.5px;text-transform:uppercase;">NIS2 Compliance Framework</div>'
    +   '</div>'
    +   '<div style="padding:12px 16px;font-size:10pt;color:#333;line-height:1.65;">'
    +   'This report is generated in accordance with <strong>NIS2 Directive (EU) 2022/2555</strong>. '
    +   '<strong>Article 23 NIS2:</strong> Significant incidents must be reported within <strong>24 hours</strong> (early warning), '
    +   '<strong>72 hours</strong> (notification) and <strong>1 month</strong> (final report).'
    +   '</div>'
    + '</div>'
    // AI Analysis sections
    + '<div style="margin:16px 28px 0;">'
    +   '<div style="margin:16px 0 10px;display:flex;align-items:center;gap:10px;">'
    +     '<div style="width:5px;height:22px;background:#003399;border-radius:2px;flex-shrink:0;"></div>'
    +     '<div style="font-size:13pt;font-weight:700;color:#1a1a2e;letter-spacing:.5px;text-transform:uppercase;">AI Security Analysis (RAG Intelligence)</div>'
    +   '</div>'
    +   sectHtml
    + '</div>'
    // Footer
    + '<div style="margin:24px 28px 0;padding-top:10px;border-top:2px solid #e0e4ee;display:flex;justify-content:space-between;font-size:8pt;color:#999;">'
    +   '<div><strong>SENTRASEC v2.0 LOCAL</strong> - AI SOC Platform - Offline Mode</div>'
    +   '<div>NIS2 Directive (EU) 2022/2555 - <strong>' + rid + '</strong></div>'
    +   '<div>Model: <strong>' + model + '</strong> - ' + ts + ' UTC</div>'
    + '</div>'
    + '<div style="margin:10px 28px 6px;padding:8px 14px;background:#fff8e0;border:1px solid #ffcc00;border-radius:3px;font-size:8.5pt;color:#664400;">'
    +   'Dokument wygenerowany automatycznie przez AI. Wymaga weryfikacji specjalisty ds. cyberbezpieczenstwa przed zlozeniem do organu nadzorczego.'
    + '</div>'
    + '<div style="text-align:center;margin:14px 28px;" class="no-print">'
    +   '<button onclick="window.print()" style="padding:10px 24px;background:#003399;color:#fff;border:none;border-radius:4px;font-size:11pt;font-weight:600;cursor:pointer;">DRUKUJ / ZAPISZ PDF</button>'
    +   '<button onclick="window.close()" style="padding:10px 24px;background:#666;color:#fff;border:none;border-radius:4px;font-size:11pt;cursor:pointer;margin-left:8px;">ZAMKNIJ</button>'
    + '</div>'
    + '</body></html>';
  return h;
}

function copyNis2() {
  if(!nis2ReportText){showToast('Brak raportu');return;}
  navigator.clipboard.writeText(nis2ReportText)
    .then(function(){showToast('Skopiowano do schowka');})
    .catch(function(){showToast('Blad kopiowania');});
}

function downloadNis2() {
  if(!nis2ReportText){showToast('Brak raportu');return;}
  var b = new Blob([nis2ReportText],{type:'text/plain;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(b);
  a.download = 'sentrasec-nis2-' + S.session + '.txt';
  a.click();
  showToast('Pobrano plik TXT');
}

function downloadNis2Html() {
  if(!nis2ReportHtml){showToast('Najpierw wygeneruj raport');return;}
  var w = window.open('','_blank');
  if(w) {
    w.document.write(nis2ReportHtml);
    w.document.close();
    showToast('Otwarto raport - uzyj Ctrl+P aby zapisac jako PDF');
  } else {
    var b = new Blob([nis2ReportHtml],{type:'text/html;charset=utf-8'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(b);
    a.download = 'SentraSec_NIS2_' + S.session + '.html';
    a.click();
    showToast('Pobrano HTML');
  }
}

// ── FILE UPLOAD ────────────────────────────────────────────────────
async function handleFileUpload(input) {
  var files = input.files;
  if(!files.length) return;
  var status = document.getElementById('uploadStatus');
  status.textContent = 'Wysylanie ' + files.length + ' plik(ow)...';
  var fd = new FormData();
  for(var i=0; i<files.length; i++) fd.append('files', files[i]);
  fd.append('session_id', S.session);
  try {
    var r = await fetch('/api/upload', {method:'POST', body:fd});
    var d = await r.json();
    status.textContent = 'Zaladowano: ' + d.total_lines + ' linii z ' + d.files.length + ' plik(ow)';
    status.style.color = 'var(--success)';
    showToast('Upload OK: ' + d.total_lines + ' linii → ingest queue');
    setTimeout(function(){status.textContent=''; status.style.color='var(--accent3)';}, 5000);
  } catch(e) {
    status.textContent = 'Blad: ' + e.message;
    status.style.color = 'var(--danger)';
  }
}

function handleDrop(ev) {
  ev.preventDefault();
  document.getElementById('dropZone').style.borderColor = 'var(--border2)';
  var files = ev.dataTransfer.files;
  if(!files.length) return;
  var fakeInput = {files: files};
  handleFileUpload(fakeInput);
}

// ── SOURCE PRESETS + TAIL MANAGER ─────────────────────────────────
async function loadPresets() {
  try {
    var r = await fetch('/api/tail/presets');
    var d = await r.json();
    var el = document.getElementById('presetList');
    el.innerHTML = Object.entries(d).map(function(entry) {
      var key = entry[0]; var p = entry[1];
      return '<div style="background:var(--bg3);border:1px solid var(--border);border-radius:3px;padding:7px 9px;margin-bottom:5px;">'
        + '<div style="display:flex;justify-content:space-between;align-items:center;">'
        + '<span style="font-family:var(--mono);font-size:12px;color:var(--text);font-weight:600;">' + p.name + '</span>'
        + '<button class="act-btn" style="color:var(--accent2);border-color:var(--accent2);background:rgba(0,153,204,.08);padding:3px 8px;font-size:10px;" onclick="activatePreset(' + JSON.stringify(key) + ')">ACTIVATE</button>'
        + '</div>'
        + '<div style="font-family:var(--mono);font-size:10px;color:var(--text3);margin-top:2px;">' + p.description + '</div>'
        + (p.files.length ? '<div style="font-family:var(--mono);font-size:10px;color:var(--muted);margin-top:3px;">' + p.files.join(' · ') + '</div>' : '')
        + '</div>';
    }).join('');
  } catch(e) {}
}

async function activatePreset(key) {
  try {
    var r = await fetch('/api/tail/presets');
    var d = await r.json();
    var preset = d[key];
    if(!preset || !preset.files.length) { showToast('Ten preset nie ma plikow do tailowania (uzyj HTTP ingest)'); return; }
    var started = 0;
    for(var i=0; i<preset.files.length; i++) {
      var rr = await fetch('/api/tail/start', {method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({path: preset.files[i], session_id: S.session})});
      var dd = await rr.json();
      if(dd.started) started++;
    }
    showToast('Preset "' + preset.name + '": ' + started + '/' + preset.files.length + ' plikow active');
    loadTailList();
  } catch(e) { showToast('Blad: ' + e.message); }
}

async function addTailSource() {
  var path = document.getElementById('tailPathInput').value.trim();
  if(!path) return;
  try {
    var r = await fetch('/api/tail/start', {method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({path: path, session_id: S.session})});
    var d = await r.json();
    if(d.started) { showToast('Tail started: ' + path); }
    else if(!d.exists) { showToast('Plik nie istnieje: ' + path); }
    else { showToast('Juz tailowany: ' + path); }
    document.getElementById('tailPathInput').value = '';
    loadTailList();
  } catch(e) { showToast('Blad: ' + e.message); }
}

async function loadTailList() {
  try {
    var r = await fetch('/api/tail/list');
    var d = await r.json();
    var el = document.getElementById('tailList');
    if(!d.length) { el.innerHTML = '<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Brak aktywnych zrodel.</div>'; return; }
    el.innerHTML = d.map(function(f) {
      var col = f.alive ? 'var(--success)' : 'var(--danger)';
      var status = f.alive ? 'LIVE' : f.status;
      return '<div style="background:var(--bg3);border:1px solid var(--border);border-radius:3px;padding:6px 9px;margin-bottom:4px;border-left:3px solid ' + col + ';">'
        + '<div style="display:flex;justify-content:space-between;">'
        + '<span style="font-family:var(--mono);font-size:11px;color:var(--text2);">' + f.file_path.split('/').pop() + '</span>'
        + '<span style="font-family:var(--mono);font-size:10px;color:' + col + ';">' + status + '</span>'
        + '</div>'
        + '<div style="font-family:var(--mono);font-size:10px;color:var(--muted);">' + f.lines_ingested + ' lines · ' + (f.last_seen||'').slice(0,19) + '</div>'
        + '<button onclick="stopTail(' + JSON.stringify(f.file_path) + ')" style="margin-top:3px;padding:2px 7px;font-family:var(--mono);font-size:10px;border:1px solid var(--danger);color:var(--danger);background:rgba(255,51,85,.08);border-radius:2px;cursor:pointer;">STOP</button>'
        + '</div>';
    }).join('');
  } catch(e) {}
}

async function stopTail(path) {
  await fetch('/api/tail/stop', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({path:path})});
  showToast('Stopped: ' + path);
  loadTailList();
}

function copyIngestConfig() {
  var host = window.location.origin;
  var config = 'filebeat.inputs:\n- type: filestream\n  id: sentrasec\n  paths:\n    - /var/log/*.log\noutput.http:\n  hosts: ["' + host + '/api/ingest"]\n  headers:\n    X-API-Key: "${SENTRASEC_API_KEY}"\n  codec.json:\n    pretty: false';
  navigator.clipboard.writeText(config).then(function(){showToast('Skopiowano konfiguracje Filebeat');}).catch(function(){});
}

// ── SESSION HISTORY ────────────────────────────────────────────────
async function loadHistory() {
  try {
    var r = await fetch('/api/sessions/history');
    var d = await r.json();
    var el = document.getElementById('historyList');
    if(!d.length) { el.innerHTML='<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Brak sesji.</div>'; return; }
    el.innerHTML = d.map(function(s) {
      var threatCol = {'low':'var(--success)','medium':'var(--warn)','high':'var(--danger)'}[s.threat_level] || 'var(--text3)';
      var isActive = s.id === S.session;
      return '<div style="background:' + (isActive?'rgba(0,212,255,.07)':'var(--bg3)') + ';border:1px solid ' + (isActive?'var(--accent2)':'var(--border)') + ';border-radius:3px;padding:8px 10px;margin-bottom:5px;cursor:pointer;" onclick="loadSession(' + JSON.stringify(s.id) + ')">'
        + '<div style="display:flex;justify-content:space-between;align-items:center;">'
        + '<span style="font-family:var(--mono);font-size:12px;color:var(--accent2);font-weight:bold;">' + s.id + (isActive?' ★':' ') + '</span>'
        + '<span style="font-family:var(--mono);font-size:10px;color:' + threatCol + ';">' + (s.threat_level||'low').toUpperCase() + '</span>'
        + '</div>'
        + '<div style="font-family:var(--mono);font-size:10px;color:var(--text3);">' + (s.created_at||'').slice(0,16).replace('T',' ') + ' · ' + s.log_count + ' logs · ' + s.incident_count + ' incidents</div>'
        + (s.label ? '<div style="font-family:var(--mono);font-size:10px;color:var(--text2);margin-top:2px;">' + s.label + '</div>' : '')
        + '<div style="display:flex;gap:4px;margin-top:5px;">'
        + '<button onclick="event.stopPropagation();exportSession(' + JSON.stringify(s.id) + ')" style="padding:2px 7px;font-family:var(--mono);font-size:10px;border:1px solid var(--border2);color:var(--text2);background:transparent;border-radius:2px;cursor:pointer;">EXPORT</button>'
        + '<button onclick="event.stopPropagation();labelSession(' + JSON.stringify(s.id) + ')" style="padding:2px 7px;font-family:var(--mono);font-size:10px;border:1px solid var(--border2);color:var(--text2);background:transparent;border-radius:2px;cursor:pointer;">LABEL</button>'
        + '</div>'
        + '</div>';
    }).join('');
  } catch(e) { document.getElementById('historyList').innerHTML='<div style="font-family:var(--mono);font-size:11px;color:var(--danger);">Blad: '+e.message+'</div>'; }
}

function loadSession(sid) {
  S.session = sid;
  document.getElementById('sessLabel').textContent = 'SESSION: ' + sid;
  showToast('Przelaczono na sesje: ' + sid);
}

function exportSession(sid) {
  window.open('/api/sessions/' + sid + '/export', '_blank');
  showToast('Eksport sesji ' + sid + ' — pobieranie...');
}

function labelSession(sid) {
  var label = prompt('Etykieta dla sesji ' + sid + ':');
  if(label === null) return;
  fetch('/api/sessions/' + sid + '/label', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({label:label})})
    .then(function(){showToast('Etykieta zapisana'); loadHistory();});
}

// Import session
function importSession() {
  var input = document.createElement('input');
  input.type = 'file'; input.accept = '.json';
  input.onchange = async function() {
    var file = input.files[0];
    if(!file) return;
    try {
      var text = await file.text();
      var data = JSON.parse(text);
      var r = await fetch('/api/sessions/import', {method:'POST',
        headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      var d = await r.json();
      showToast('Import OK: ' + d.imported_logs + ' logow → nowa sesja ' + d.new_session_id);
      loadHistory();
    } catch(e) { showToast('Blad importu: ' + e.message); }
  };
  input.click();
}

// ── FULL-TEXT SEARCH ───────────────────────────────────────────────
async function doSearch() {
  var q = document.getElementById('searchInput').value.trim();
  if(!q) return;
  var el = document.getElementById('searchResults');
  el.innerHTML = '<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Szukam...</div>';
  try {
    var url = '/api/search?q=' + encodeURIComponent(q) + '&session_id=' + S.session + '&limit=50';
    var r = await fetch(url);
    var d = await r.json();
    if(d.error) { el.innerHTML='<div style="color:var(--danger);font-family:var(--mono);font-size:11px;">Blad: '+d.error+'<br><span style="color:var(--text3);">'+d.hint+'</span></div>'; return; }
    if(!d.count) { el.innerHTML='<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Brak wynikow dla: '+q+'</div>'; return; }
    el.innerHTML = '<div style="font-family:var(--mono);font-size:11px;color:var(--accent2);margin-bottom:6px;">'+d.count+' wynikow dla "'+q+'"</div>'
      + d.results.map(function(row) {
        var sevCols = {'CRITICAL':'var(--danger)','HIGH':'#ff7755','MEDIUM':'var(--warn)','LOW':'var(--success)','INFO':'var(--accent2)'};
        var col = sevCols[row.severity] || 'var(--text2)';
        // Highlight query words in raw text
        var raw = (row.raw||'').slice(0,140);
        try { raw = raw.replace(new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'), '<mark style="background:rgba(0,212,255,.25);color:var(--text);">$&</mark>'); } catch(e){}
        return '<div style="background:var(--bg3);border:1px solid var(--border);border-radius:3px;padding:6px 9px;margin-bottom:4px;border-left:2px solid '+col+';">'
          + '<div style="display:flex;gap:6px;align-items:center;margin-bottom:2px;">'
          + '<span style="font-family:var(--mono);font-size:10px;color:'+col+';font-weight:bold;">'+row.severity+'</span>'
          + '<span style="font-family:var(--mono);font-size:10px;color:var(--accent2);">'+row.log_type+'</span>'
          + (row.src_ip?'<span style="font-family:var(--mono);font-size:10px;color:var(--text3);">'+row.src_ip+'</span>':'')
          + '</div>'
          + '<div style="font-family:var(--mono);font-size:11px;color:var(--text2);">'+raw+'</div>'
          + '</div>';
      }).join('');
  } catch(e) { el.innerHTML='<div style="color:var(--danger);font-family:var(--mono);font-size:11px;">'+e.message+'</div>'; }
}

// ── API KEY DISPLAY ────────────────────────────────────────────────
async function loadApiKeyInfo() {
  try {
    var r = await fetch('/api/config/apikey');
    var d = await r.json();
    var el = document.getElementById('apiKeyPreview');
    if(el) el.textContent = d.api_key_prefix;
  } catch(e) {}
}

// ── INVESTIGATION NOTEBOOK ─────────────────────────────────────────
let _notebookText = '';
let _notebookData = null;

async function openNotebook(incId, incTitle) {
  document.getElementById('notebookModal').classList.add('open');
  document.getElementById('nbIncTitle').textContent = incTitle || '';
  document.getElementById('nbContent').innerHTML   = '';
  document.getElementById('nbSpinner').style.display = 'block';
  try {
    var r = await fetch('/api/notebook/' + incId, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id: S.session})
    });
    var d = await r.json();
    document.getElementById('nbSpinner').style.display = 'none';
    _notebookText = d.notebook || '';
    _notebookData = d;
    var sections  = _notebookText.split(/^## /m).filter(function(s){return s.trim();});
    var secColors = ['var(--accent2)','var(--danger)','#ff7755','var(--warn)','var(--success)','var(--accent)','var(--text2)'];
    var html = '<div style="margin-bottom:12px;padding:10px 14px;background:rgba(0,255,136,.05);border:1px solid rgba(0,255,136,.2);border-radius:3px;">'
      + '<div style="font-family:var(--mono);font-size:13px;color:var(--accent3);font-weight:bold;margin-bottom:3px;">⬡ Investigation Notebook — AI Tier-1 Analysis</div>'
      + '<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">Incydent: ' + (d.incident && d.incident.title || '') + ' · Risk: ' + (d.incident && d.incident.risk_score || 0) + ' · Alerty: ' + (d.alerts && d.alerts.length || 0) + '</div>'
      + '<div style="font-family:var(--mono);font-size:11px;color:var(--text3);">NIS2: ' + (d.nis2 && d.nis2.classification || '') + '</div>'
      + '</div>';
    if(sections.length > 1) {
      sections.forEach(function(sec, i) {
        var lines = sec.split('\n');
        var title = lines[0].trim().replace(/</g,'&lt;').replace(/>/g,'&gt;');
        var body  = lines.slice(1).join('\n').trim()
          .replace(/</g,'&lt;').replace(/>/g,'&gt;')
          .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
          .replace(/^- (.+)/gm,'<div style="margin:2px 0;padding-left:14px;">&#9658; $1</div>')
          .replace(/\bTAK\b/g,'<span style="color:var(--danger);font-weight:bold;">TAK</span>')
          .replace(/\bNIE\b/g,'<span style="color:var(--success);">NIE</span>')
          .replace(/(T\d{4})/g,'<span style="background:rgba(0,136,187,.15);border:1px solid rgba(0,136,187,.3);padding:1px 5px;border-radius:2px;font-family:var(--mono);font-size:11px;color:var(--accent2);">$1</span>')
          .replace(/\n/g,'<br>');
        var col = secColors[i % secColors.length];
        html += '<div class="nb-section" style="border-left:3px solid ' + col + ';">'
          + '<div class="nb-section-title" style="color:' + col + ';">## ' + title + '</div>'
          + '<div class="nb-text">' + body + '</div></div>';
      });
    } else {
      html += '<div class="nb-section"><div class="nb-text">' + _notebookText.replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>') + '</div></div>';
    }
    document.getElementById('nbContent').innerHTML = html;
    showToast('Investigation Notebook wygenerowany');
  } catch(e) {
    document.getElementById('nbSpinner').style.display = 'none';
    document.getElementById('nbContent').innerHTML = '<div style="color:var(--danger);font-family:var(--mono);font-size:12px;padding:14px;">Błąd: ' + e.message + '</div>';
  }
}

function copyNotebook() {
  if(!_notebookText){showToast('Brak treści');return;}
  navigator.clipboard.writeText(_notebookText).then(function(){showToast('Skopiowano');}).catch(function(){});
}
function downloadNotebook() {
  if(!_notebookText){showToast('Brak treści');return;}
  var b=new Blob([_notebookText],{type:'text/plain;charset=utf-8'});
  var a=document.createElement('a'); a.href=URL.createObjectURL(b);
  a.download='sentrasec-notebook-' + S.session + '.txt'; a.click();
}
function openNotebookPdf() {
  if(!_notebookText){showToast('Brak treści');return;}
  var d = _notebookData || {};
  var html = '<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8"><title>Investigation Notebook</title>'
    + '<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:900px;margin:0 auto;padding:24px;color:#111;font-size:11pt;line-height:1.6;}'
    + 'h1{color:#003366;border-bottom:3px solid #003366;padding-bottom:8px;font-size:20pt;}'
    + 'h2{color:#003366;font-size:14pt;margin-top:22px;border-left:4px solid #003366;padding-left:10px;}'
    + '.meta{background:#f0f4f8;border:1px solid #ccd8e8;border-radius:4px;padding:10px 14px;margin-bottom:16px;font-size:10pt;}'
    + 'pre{background:#f5f5f5;padding:10px;border-radius:3px;white-space:pre-wrap;font-size:10pt;}'
    + '.warn{background:#fff8e1;border:1px solid #ffcc00;border-radius:4px;padding:8px 12px;font-size:9.5pt;}'
    + '@media print{button{display:none;}}'
    + '</style></head><body>'
    + '<h1>⬡ Investigation Notebook — SENTRASEC v2.0</h1>'
    + '<div class="meta"><strong>Incydent:</strong> ' + (d.incident && d.incident.title || '') + '<br>'
    + '<strong>Risk Score:</strong> ' + (d.incident && d.incident.risk_score || 0) + '<br>'
    + '<strong>NIS2:</strong> ' + (d.nis2 && d.nis2.classification || '') + '<br>'
    + '<strong>Wygenerowano:</strong> ' + (d.generated_at || new Date().toISOString()).slice(0,19) + ' UTC</div>'
    + '<pre>' + _notebookText.replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</pre>'
    + '<div class="warn">Wygenerowano przez SENTRAsec v2.0 LOCAL — AI SOC Platform (offline)</div>'
    + '<div style="text-align:center;margin-top:20px;"><button onclick="window.print()" style="padding:10px 24px;background:#003366;color:#fff;border:none;border-radius:4px;font-size:11pt;cursor:pointer;">🖨 DRUKUJ / ZAPISZ PDF</button></div>'
    + '</body></html>';
  var w = window.open('','_blank');
  if(w){w.document.write(html);w.document.close();}
}

// ── ART.21 QUIZ ────────────────────────────────────────────────────
var _art21Scores = {};
var _art21Reqs = [
  {id:'21.2.a',name:'Polityki bezpieczeństwa IT',q:['Czy posiadasz pisemną politykę bezpieczeństwa IT?','Czy polityka jest aktualizowana co roku?']},
  {id:'21.2.b',name:'Zarządzanie ryzykiem',q:['Czy regularnie oceniasz ryzyko?','Czy posiadasz rejestr ryzyk?']},
  {id:'21.2.c',name:'Ciągłość działania (BCP/DRP)',q:['Czy posiadasz plan BCP?','Czy testujesz kopie zapasowe?']},
  {id:'21.2.d',name:'Bezpieczeństwo dostawców',q:['Czy oceniasz bezpieczeństwo dostawców IT?','Czy umowy mają klauzule bezpieczeństwa?']},
  {id:'21.2.e',name:'Bezpieczeństwo systemów',q:['Czy sprawdzasz bezpieczeństwo przed wdrożeniem?','Czy stosujesz minimalne uprawnienia?']},
  {id:'21.2.f',name:'Zarządzanie podatnościami',q:['Czy regularnie aktualizujesz systemy?','Czy skanujesz podatności?']},
  {id:'21.2.g',name:'Ocena skuteczności',q:['Czy przeprowadzasz audyty bezpieczeństwa?','Czy stosujesz pentesty?']},
  {id:'21.2.h',name:'Cyberhigiena i MFA',q:['Czy stosujesz MFA?','Czy pracownicy przechodzą szkolenia?','Czy masz politykę silnych haseł?']},
  {id:'21.2.i',name:'Kryptografia i szyfrowanie',q:['Czy szyfrujesz dane wrażliwe?','Czy stosujesz TLS/HTTPS?']},
  {id:'21.2.j',name:'Bezpieczeństwo personelu',q:['Czy weryfikujesz dostęp pracowników?','Czy szybko odbierasz dostęp po odejściu?']},
];

function openArt21() {
  _art21Scores = {};
  var html = '';
  _art21Reqs.forEach(function(req) {
    _art21Scores[req.id] = 50;
    html += '<div class="quiz-req">'
      + '<div class="quiz-req-hdr">'
      + '<span class="quiz-req-id">' + req.id + '</span>'
      + '<span class="quiz-req-name">' + req.name + '</span>'
      + '</div>'
      + '<div style="font-family:var(--mono);font-size:10px;color:var(--text3);margin-bottom:7px;">' + req.q.join(' · ') + '</div>'
      + '<div class="quiz-score-bar">'
      + '<span class="quiz-score-label">0%</span>'
      + '<input type="range" min="0" max="100" value="50" class="quiz-slider" id="sl_' + req.id + '" oninput="updateQuizScore(\'' + req.id + '\',this.value)">'
      + '<span class="quiz-score-label">100%</span>'
      + '<span class="quiz-val" id="sv_' + req.id + '">50%</span>'
      + '</div></div>';
  });
  document.getElementById('art21QuizContent').innerHTML = html;
  document.getElementById('art21ResultContent').style.display = 'none';
  document.getElementById('art21QuizContent').style.display = 'block';
  document.getElementById('art21FootBtns').innerHTML =
    '<button class="btn bp" style="background:rgba(255,187,0,.2);border-color:var(--warn);color:var(--warn);" onclick="submitArt21()">⬡ OCEŃ ZGODNOŚĆ</button>';
  document.getElementById('art21Modal').classList.add('open');
}

function updateQuizScore(id, val) {
  _art21Scores[id] = parseInt(val);
  var el = document.getElementById('sv_' + id);
  if(el) el.textContent = val + '%';
}

async function submitArt21() {
  try {
    var r = await fetch('/api/art21/assess', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id: S.session, answers: _art21Scores})
    });
    var d = await r.json();
    var overall = d.overall || 0;
    var col = overall>=75?'var(--success)':overall>=50?'var(--warn)':'var(--danger)';
    var html = '<div style="text-align:center;padding:14px 0;margin-bottom:14px;">'
      + '<div style="font-family:var(--mono);font-size:32px;color:' + col + ';font-weight:900;line-height:1;">' + overall + '%</div>'
      + '<div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin-top:4px;">' + (d.label||'') + '</div>'
      + '<div style="font-family:var(--mono);font-size:10px;color:var(--text3);margin-top:3px;">' + (d.ksc_note||'') + '</div>'
      + '</div>'
      + '<div style="margin-bottom:12px;">';
    (d.requirements||[]).forEach(function(req) {
      var rc = req.score>=70?'var(--success)':req.score>=40?'var(--warn)':'var(--danger)';
      html += '<div class="art21-row">'
        + '<span class="art21-id">' + req.id + '</span>'
        + '<span class="art21-name">' + req.name + '</span>'
        + '<div class="art21-bar"><div class="art21-fill" style="width:' + req.score + '%;background:' + rc + ';"></div></div>'
        + '<span class="art21-pct" style="color:' + rc + ';">' + req.score + '%</span>'
        + '<span class="art21-status">' + req.status + '</span>'
        + '</div>';
      if(req.findings && req.findings.length) {
        req.findings.forEach(function(f){
          html += '<div style="font-family:var(--mono);font-size:10px;color:var(--warn);margin-left:58px;margin-bottom:3px;">⚠ ' + f + '</div>';
        });
      }
    });
    html += '</div>';
    document.getElementById('art21ResultContent').innerHTML = html;
    document.getElementById('art21ResultContent').style.display = 'block';
    document.getElementById('art21QuizContent').style.display = 'none';
    document.getElementById('art21FootBtns').innerHTML =
      '<button class="btn bs" onclick="openArt21()">PONÓW QUIZ</button>'
      + '<button class="btn bp" onclick="downloadArt21(' + JSON.stringify(d).replace(/"/g,"'") + ')">⬇ EKSPORT</button>';
    showToast('Art.21 assessment: ' + overall + '% zgodności');
  } catch(e) { showToast('Błąd: ' + e.message); }
}

function downloadArt21(d) {
  var text = 'SENTRASEC v2.0 — Ocena zgodności NIS2 Art. 21\n';
  text += 'Score ogólny: ' + (d.overall||0) + '%  — ' + (d.label||'') + '\n\n';
  (d.requirements||[]).forEach(function(r){
    text += r.status + ' ' + r.id + ' ' + r.name + ': ' + r.score + '%\n';
    (r.findings||[]).forEach(function(f){text += '  ⚠ ' + f + '\n';});
  });
  text += '\n' + (d.ksc_note||'') + '\nWygenerowano: SENTRAsec v2.0 LOCAL';
  var b=new Blob([text],{type:'text/plain;charset=utf-8'});
  var a=document.createElement('a');a.href=URL.createObjectURL(b);
  a.download='sentrasec-art21-' + S.session + '.txt';a.click();
}

// ── NIS2 TEMPLATE SELECTOR ──────────────────────────────────────────
var _selectedTemplate = '72h';

function openNis2TemplateModal() {
  _selectedTemplate = '72h';
  document.querySelectorAll('.nis2-tpl-card').forEach(function(c){c.classList.remove('selected');});
  document.getElementById('tpl72h').classList.add('selected');
  document.getElementById('nis2TemplateModal').classList.add('open');
}

function selectTemplate(tpl) {
  _selectedTemplate = tpl;
  document.querySelectorAll('.nis2-tpl-card').forEach(function(c){c.classList.remove('selected');});
  var ids = {'24h':'tpl24h','72h':'tpl72h','final':'tmpFinal'};
  if(ids[tpl]) document.getElementById(ids[tpl]).classList.add('selected');
}

async function genNis2FromTemplate() {
  var orgName = document.getElementById('orgName').value.trim() || '[Nazwa podmiotu]';
  var orgType = document.getElementById('orgType').value;
  closeM('nis2TemplateModal');
  // Use existing NIS2 modal as output
  document.getElementById('nis2Content').innerHTML = '';
  document.getElementById('nis2Spinner').className = 'nis2-spinner on';
  document.getElementById('nis2ModelBadge').textContent = 'SZABLON: ' + _selectedTemplate.toUpperCase() + ' · ' + (document.getElementById('modelSelect') && document.getElementById('modelSelect').value || 'llama3');
  document.getElementById('nis2Modal').classList.add('open');
  var logs = document.getElementById('logRaw') && document.getElementById('logRaw').value || '';
  try {
    var r = await fetch('/api/report/nis2/template', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id:S.session, template:_selectedTemplate, org_name:orgName, org_type:orgType, logs:logs})
    });
    var d = await r.json();
    document.getElementById('nis2Spinner').className = 'nis2-spinner';
    nis2ReportText = d.report || '';
    nis2ReportHtml = buildNis2Html(d);
    var sections = nis2ReportText.split(/^## /m).filter(function(s){return s.trim();});
    var tplLabels = {'24h':'⚠ WCZESNE OSTRZEŻENIE · 24H','72h':'⬡ ZGŁOSZENIE INCYDENTU · 72H','final':'✓ RAPORT KOŃCOWY · 1 MIESIĄC'};
    var tplCols   = {'24h':'var(--danger)','72h':'var(--warn)','final':'var(--success)'};
    var col = tplCols[_selectedTemplate] || 'var(--warn)';
    var html = '<div style="margin-bottom:14px;padding:10px 14px;background:rgba(255,187,0,.06);border:1px solid rgba(255,187,0,.25);border-radius:3px;">'
      + '<div style="font-family:var(--mono);font-size:13px;color:' + col + ';font-weight:bold;margin-bottom:4px;">' + (tplLabels[_selectedTemplate]||'') + '</div>'
      + '<div style="font-size:12px;color:var(--text2);font-family:var(--mono);">Organizacja: ' + orgName + ' (' + orgType + ') · ' + d.report_id + '</div>'
      + '<div style="font-size:12px;color:var(--text2);margin-top:4px;">NIS2: ' + (d.nis2 && d.nis2.classification || '') + ' · Alerty: ' + (d.alerts_count||0) + '</div>'
      + '</div>';
    if(sections.length > 1) {
      sections.forEach(function(sec) {
        var lines = sec.split('\n');
        var title = lines[0].trim().replace(/</g,'&lt;').replace(/>/g,'&gt;');
        var body  = lines.slice(1).join('\n').trim().replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>');
        html += '<div class="nis2-section" style="border-left-color:' + col + ';">'
          + '<div class="nis2-section-title" style="color:' + col + ';">## ' + title + '</div>'
          + '<div class="nis2-text">' + body + '</div></div>';
      });
    } else {
      html += '<div class="nis2-section"><div class="nis2-text">' + nis2ReportText.replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>') + '</div></div>';
    }
    document.getElementById('nis2Content').innerHTML = html;
    showToast('Raport NIS2 (' + _selectedTemplate + ') wygenerowany');
  } catch(e) {
    document.getElementById('nis2Spinner').className = 'nis2-spinner';
    document.getElementById('nis2Content').innerHTML = '<div style="color:var(--danger);font-family:var(--mono);font-size:12px;padding:14px;">Błąd: ' + e.message + '</div>';
  }
}

// ── RULESET DETECTION ──────────────────────────────────────────────
var _lastAlerts = [];

async function runRulesModal() {
  document.getElementById('rulesModal').classList.add('open');
  document.getElementById('rulesContent').innerHTML = '<div style="font-family:var(--mono);font-size:12px;color:var(--text3);">Uruchamianie 20 reguł detekcji...</div>';
  await runRules();
}

async function runRules() {
  try {
    var r = await fetch('/api/rules/evaluate', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id: S.session})
    });
    var d = await r.json();
    _lastAlerts = d.alerts || [];
    var nis2 = d.nis2 || {};
    var col  = nis2.score>=50?'var(--danger)':nis2.score>=40?'var(--warn)':'var(--success)';
    var html = '<div style="margin-bottom:12px;padding:9px 12px;background:rgba(0,212,255,.04);border:1px solid var(--border);border-radius:3px;">'
      + '<div style="font-family:var(--mono);font-size:12px;color:var(--text2);">Przeanalizowano: <strong style="color:var(--accent2);">' + d.entries_analyzed + '</strong> logów · Alerty: <strong style="color:' + col + ';">' + _lastAlerts.length + '</strong></div>'
      + '<div style="font-family:var(--mono);font-size:11px;color:' + col + ';margin-top:3px;">' + (nis2.classification||'') + '</div>'
      + '</div>';
    if(!_lastAlerts.length) {
      html += '<div style="font-family:var(--mono);font-size:12px;color:var(--success);padding:12px;">✓ Żadna z 20 reguł nie została wyzwolona — brak wykrytych zagrożeń.</div>';
    } else {
      _lastAlerts.forEach(function(a) {
        var sc = {'CRITICAL':'var(--danger)','HIGH':'#ff7755','MEDIUM':'var(--warn)','LOW':'var(--success)'}[a.severity]||'var(--text2)';
        html += '<div class="rule-card ' + a.severity + '">'
          + '<div class="rule-hdr">'
          + '<span class="rule-name">' + a.rule_name + '</span>'
          + '<div style="display:flex;gap:5px;align-items:center;">'
          + '<span style="font-family:var(--mono);font-size:10px;color:var(--accent2);">' + a.mitre_id + '</span>'
          + '<span style="font-family:var(--mono);font-size:11px;color:' + sc + ';font-weight:bold;">' + a.severity + '</span>'
          + '</div></div>'
          + '<div class="rule-meta">[' + a.rule_id + '] ' + a.nis2_category + ' · ' + a.group_by + ': <strong>' + a.group_key + '</strong> · ' + a.count + ' zdarzeń</div>'
          + '<div class="rule-rem">⚑ ' + a.remediation + '</div>'
          + '</div>';
      });
    }
    document.getElementById('rulesContent').innerHTML = html;
    // Update incident cards with Notebook buttons
    renderIncidents(S.incidents);
  } catch(e) {
    document.getElementById('rulesContent').innerHTML = '<div style="color:var(--danger);font-family:var(--mono);font-size:12px;">' + e.message + '</div>';
  }
}

init();
</script>
</body>
</html>"""


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║       SENTRASEC v2.0 LOCAL — AI SOC / SIEM Platform             ║
║       100% Offline · Ollama LLM · RAG · SQLite · Real Ingest    ║
╠══════════════════════════════════════════════════════════════════╣
║  INSTALL:                                                        ║
║    pip install flask flask-cors requests                         ║
║    pip install watchdog                  # file tailing          ║
║    pip install chromadb                  # opcja RAG             ║
║                                                                  ║
║  OLLAMA:  ollama pull llama3 && ollama serve                     ║
║                                                                  ║
║  FILEBEAT/FLUENT BIT → POST /api/ingest                         ║
║    Header: X-API-Key: <see sentrasec_apikey.txt>                 ║
║                                                                  ║
║  URUCHOMIENIE: python sentrasec_v2_local.py                      ║
║  DOSTĘP:       http://localhost:5000                             ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    online = ollama_ping()
    print(f"[Ollama]   Status: {'✓ ONLINE' if online else '✗ OFFLINE (uruchom: ollama serve)'}")
    print(f"[Ollama]   Host: {OLLAMA_HOST} | Model: {OLLAMA_MODEL}")
    print(f"[RAG]      ChromaDB: {'aktywny' if CHROMA_OK else 'niedostępny → TF-IDF fallback'}")
    print(f"[Watchdog] File tailer: {'aktywny' if WATCHDOG_OK else 'niedostępny (pip install watchdog)'}")
    print(f"[DB]       SQLite: {DB_PATH}")
    print(f"[Auth]     API Key: {API_KEY[:8]}... (plik: {API_KEY_FILE})")
    print(f"[Ingest]   POST http://localhost:5000/api/ingest  (Header: X-API-Key: {API_KEY[:8]}...)")
    print(f"[Flask]    http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
