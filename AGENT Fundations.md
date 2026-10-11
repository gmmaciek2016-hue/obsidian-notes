---

Jeśli zbadałeś Sztuczna inteligencja Aplikacje, bezpieczeństwo AI czy nowoczesne przepływy pracy automatyzacji – prawdopodobnie spotkałeś się ze słowem „agent”. Pojawia się ono wszędzie: agenci badawczy, agenci kodujący, SOC agenci, agenci przeglądarkowi, agenci testów penetracyjnych, agenci obsługi klienta i autonomiczni asystenci AI.

Termin ten jest jednak często używany luźno. „Agent” może odnosić się do prostego Magister prawa monit zawarty w aplikacji, deterministyczny przepływ pracy sterowany kodem lub system, który potrafi rozumować, korzystać z narzędzi, utrzymywać stan i decydować, co dalej. Bez jasnych podstaw trudno jest zrozumieć, czym właściwie jest agent, kiedy jest potrzebny i jakie podejście jest odpowiednie do jego zbudowania.

Ten pokój został zaprojektowany tak, aby rozwiać wszelkie wątpliwości.

Przed zbudowaniem całości **Atlas W kolejnej sali, w ramach programu Research Agent** , przepracujesz krótkie, kontrolowane przykłady w Pythonie, które wprowadzą Cię w podstawowe elementy systemów agentowych. Zaczniesz od podstawowego przepływu pracy LLM, a następnie poznasz wywoływanie narzędzi LangChain, ustrukturyzowane wyniki, stan i rozgałęzienia LangGraph, wybór frameworka oraz typowe błędy debugowania.

Celem nie jest omówienie wszystkich funkcji LangChain czy LangGraph. Zamiast tego, ta sala koncentruje się na praktycznej ocenie inżynierskiej: rozpoznawaniu, kiedy zwykły Python jest wystarczający, kiedy LangChain zapewnia użyteczne abstrakcje, a kiedy LangGraph lepiej nadaje się do przepływów pracy ze stanem lub rozgałęzieniami.

![Od przepływu pracy LLM do agenta AI](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786464657156.png)

Pod koniec zajęć będziesz w stanie przeanalizować przepływ pracy oparty na sztucznej inteligencji i odpowiedzieć na proste, ale ważne pytanie:

**Czy to naprawdę musi być agent?**

## Cele edukacyjne

- Wyjaśnij, czym jest agent AI i kiedy jest potrzebny
- Porównanie przepływów pracy w języku Python, LangChain i LangGraph
- Zbuduj podstawowy przepływ pracy LLM w Pythonie
- Utwórz prosty przepływ pracy wywoływania narzędzi LangChain
- Używaj ustrukturyzowanych wyników, aby ułatwić weryfikację odpowiedzi
- Zbuduj podstawowy przepływ pracy LangGraph ze stanem i rozgałęzieniami
- Wybierz najprostszy przepływ pracy, który bezpiecznie rozwiąże zadanie
- Debuguj typowe błędy agentów, takie jak nieprawidłowe dane wejściowe narzędzia, brakujące aktualizacje stanu i błędne decyzje dotyczące routingu

## Wymagania wstępne

Zanim rozpoczniesz tę salę, powinieneś znać podstawowe pojęcia języka Python, takie jak zmienne, funkcje, instrukcje warunkowe, pętle, pliki i importy. Jeśli te tematy są Ci nieznane, najpierw zapoznaj się z salą [„Podstawy Pythona”](https://tryhackme.com/room/pythonbasics) .

Zalecana jest również podstawowa znajomość koncepcji LLM, w tym poleceń, odpowiedzi, kontekstu, wyników modeli i struktury poleceń. Jeśli potrzebujesz przypomnienia, sala [Prompt Engineering](https://tryhackme.com/room/promptengineeringaisec) wprowadza podstawy LLM, zachowania w ramach poleceń i efektywne projektowanie poleceń.

![Czym jest agent](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786465450691.png)

Częsty błąd w Sztuczna inteligencja inżynieria wzywa każdego Magister prawa- zasilany system **agent** .

W praktyce nie każdy system wykorzystujący model LLM wymaga zachowań agentowych. Niektóre przepływy pracy wymagają jedynie monitu, modelu i wyniku. Inne wymagają deterministycznego kodu, który podąża za ustalonymi regułami. Mniejszy zestaw przepływów pracy wymaga, aby system podejmował decyzje w trakcie wykonywania, korzystał z narzędzi, śledził stan i decydował, co powinno się wydarzyć.

W tym pokoju rozdzielone są trzy często mylone idee:

|Typ przepływu pracy|Opis|
|---|---|
|Podstawowy przepływ pracy LLM|Stała ścieżka od wejścia do monitu, modelu i wyjścia|
|Automatyzacja|Przewidywalny przepływ pracy kontrolowany przez kod, reguły lub funkcje|
|Przepływ pracy agenta|Przepływ pracy, w którym system może wybierać narzędzia, aktualizować stan i decydować o następnym kroku|

Kluczową różnicą jest **podejmowanie decyzji w czasie wykonywania** . Podstawowy przepływ pracy LLM podąża **ustaloną ścieżką** i chociaż zautomatyzowany przepływ pracy może wywoływać funkcje, jego kolejność jest zazwyczaj z góry określona. Przepływ pracy oparty na agentach zapewnia większą elastyczność, decydując, czy żądanie wymaga narzędzia, którego narzędzia użyć, czy potrzebne są dodatkowe informacje, a także która gałąź powinna zostać uruchomiona jako następna. Ta elastyczność może być przydatna, ale zwiększa również złożoność: im większa swoboda systemu, tym trudniej go testować, debugować, oceniać i zabezpieczać.

Przepływy pracy agentów stają się bardziej użyteczne, gdy system musi analizować informacje, które nie są jeszcze dostępne w monicie. W kontekście bezpieczeństwa często oznacza to łączenie się z zatwierdzonymi źródłami danych, takimi jak telemetria punktów końcowych, logi tożsamości, zdarzenia sieciowe, rejestry luk w zabezpieczeniach, poprzednie notatki z dochodzeń lub historia zgłoszeń.

Bez tych powiązań model może wygenerować wiarygodną odpowiedź na podstawie niepełnego kontekstu. Kontrolowane narzędzia pozwalają przepływowi pracy na pozyskanie istotnych dowodów przed podjęciem decyzji, co powinno się stać dalej.

Prowadzi to do prostej zasady inżynieryjnej dla pomieszczenia:

**Użyj najprostszego przepływu pracy, który bezpiecznie rozwiąże problem.**

## Czym jest LangChain?

[**Łańcuch językowy**(otwiera się w nowej karcie)](https://www.langchain.com/)to framework do tworzenia aplikacji i agentów opartych na LLM. W tym pokoju jego najważniejszą koncepcją jest wywoływanie narzędzi. Narzędzie to kontrolowana funkcja, która zapewnia modelowi dostęp do funkcji zewnętrznych, takich jak wyszukiwanie danych pozorowanych, sprawdzanie zaufanego źródła, wyodrębnianie słów kluczowych lub klasyfikowanie żądania.

Agent LangChain może zdecydować, kiedy poprosić o zatwierdzone narzędzie, podać wymagane dane wejściowe, otrzymać wynik i wykorzystać te informacje do wygenerowania ostatecznej odpowiedzi.

LangChain sprawdza się, gdy przepływ pracy wymaga:

- Połączenie modelowe
- Mały zestaw kontrolowanych narzędzi
- Prosty wybór narzędzi
- Wyczyść dane wejściowe i wyjściowe narzędzi
- Lekka pętla agenta

W początkowych ćwiczeniach w tej sali LangChain wprowadza użycie narzędzi bez dodatkowej złożoności związanej z pełnym, opartym na grafie przepływem pracy.

## Czym jest LangGraph?

[**LangGraph**(otwiera się w nowej karcie)](https://www.langchain.com/langgraph)to platforma do budowania przepływów pracy agentów opartych na grafach i stanach. Zamiast traktować agenta jako pojedynczą pętlę, reprezentuje przepływ pracy jako węzły i krawędzie. Każdy węzeł wykonuje określony krok, stan przenosi informacje między krokami, krawędzie definiują ścieżkę wykonania, a krawędzie warunkowe umożliwiają rozgałęzianie przepływu pracy na podstawie wartości przechowywanych w stanie.

LangGraph sprawdza się, gdy przepływ pracy wymaga:

- Stan jawny 
- Wiele kroków
- Trasowanie warunkowe
- Ponowne próby lub ścieżki zapasowe
- Punkty akceptacji człowieka
- Dłuższa lub bardziej złożona orkiestracja

W późniejszych ćwiczeniach w tej sali LangGraph sprawia, że ​​ścieżka wykonywania jest widoczna, możliwa do przetestowania i łatwiejsza do debugowania.

## Wybór właściwego podejścia

Prawidłowa implementacja zależy od przepływu pracy, a nie od tego, czy słowo „agent” brzmi bardziej zaawansowanie.

- Używaj **czystego Pythona,** gdy zadanie jest stałe, przewidywalne i w większości deterministyczne.
- Użyj **LangChain,** gdy przepływ pracy wymaga LLM wraz z niewielką liczbą kontrolowanych narzędzi, ale nie ma potrzeby skomplikowanego zarządzania stanem lub rozgałęziania.
- Używaj **LangGraph,** gdy przepływ pracy wymaga jawnego stanu, ścieżek warunkowych, ponownych prób, punktów zatwierdzania przez człowieka lub ustrukturyzowanej orkiestracji wieloetapowej.

|Przypadek użycia|Dobrze pasuje|
|---|---|
|Naprawiono przepływ monitów i odpowiedzi|Zwykły Python|
|LLM z kilkoma kontrolowanymi narzędziami|Łańcuch językowy|
|Przepływ pracy z uwzględnieniem stanu i routingu lub rozgałęzień|LangGraph|
|Długotrwały obieg prac badawczych z syntezą i obsługą źródeł|AtlasAgent badawczy|

Celem tego porównania nie jest uszeregowanie frameworków od prostych do zaawansowanych. Każda opcja odpowiada innym potrzebom inżynierskim.

Prosty skrypt w Pythonie jest często najbezpieczniejszym i najłatwiejszym rozwiązaniem, gdy przepływ pracy jest przewidywalny. LangChain jest przydatny, gdy model potrzebuje dostępu do kontrolowanych narzędzi. LangGraph lepiej sprawdza się w przepływach pracy wymagających widocznego stanu, jawnego routingu, rozgałęzień warunkowych, ponownych prób lub punktów zatwierdzenia.

_Należy wybrać strukturę agenta, ponieważ wymaga tego przepływ pracy, a nie dlatego, że system używa LLM._

![Przewodnik po przepływie pracy i strukturze studiów LLM](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786465450697.png)

Przed utworzeniem agenta ważne jest zrozumienie jego najprostszej formy Magister prawa Przepływ pracy oparty na technologii Powered Workflow. Podstawowy przepływ pracy LLM nie wykorzystuje narzędzi, pamięci, rozgałęzień, ponawiania prób ani orkiestracji z uwzględnieniem stanu. Zamiast tego podąża ustaloną ścieżką:

![Diagram prostego przepływu pracy LLM, od lewej do prawej. Dane wejściowe Pythona są przekształcane w monit, monit jest wysyłany do modelu, a model zwraca dane wyjściowe. Przepływ pracy jest oznaczony jako ścieżka stała i pokazuje, że narzędzia, pamięć, stan i rozgałęzienia nie są używane.](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786465564790.png)

To podejście sprawdza się, gdy zadanie jest przewidywalne, a system nie musi decydować, co zrobić dalej. W tym zadaniu uruchomisz prosty skrypt w Pythonie, który ładuje przykładowe żądanie, konstruuje monit, wysyła go do modelu i drukuje odpowiedź.

Celem jest zrozumienie fundamentów, na których budowane są bardziej zaawansowane przepływy pracy. LangChain i LangGraph wprowadzają przydatne abstrakcje, ale podstawowy schemat pozostaje ten sam: dostarczają kontekst do modelu i obsługują jego reakcję.

## Dlaczego warto zacząć od Plain Python?

**Prosty Python** ułatwia inspekcję przepływu pracy, ponieważ ma mniej ruchomych części: nie są wywoływane żadne narzędzia, graf nie kieruje wykonywaniem, a stan nie jest przekazywany między węzłami. Dzięki temu łatwiej jest zrozumieć:

- Jakie dane wejściowe otrzymuje przepływ pracy
- Jak skonstruowany jest monit
- Co zwraca model
- Gdzie mogą wystąpić błędy

Jeśli zadanie wymaga tylko jednego monitu i odpowiedzi, wprowadzenie pełnej struktury agenta może niepotrzebnie zwiększyć złożoność.

Na swoim komputerze otwórz terminal i przejdź do katalogu lab:

Terminal

```powershell
user@machine$ cd ~/agent-foundations
```

## Praca z TODO

Pliki laboratoryjne zawierają małe `TODO`znaczniki, które wskazują, gdzie należy uzupełnić lub zmodyfikować kod. Otaczający kod jest już dostępny, dzięki czemu możesz skupić się na jednym zagadnieniu na raz.

Gdy napotkasz błąd `TODO`, przeczytaj najpierw komentarze w pobliżu, aby zrozumieć, co powinien robić brakujący kod. Po jego ukończeniu uruchom skrypt z katalogu głównego projektu i przejrzyj dane wyjściowe, aby upewnić się, że zmiany działają zgodnie z oczekiwaniami.

W tym pokoju możesz edytować wyłącznie pliki znajdujące się w:

```text
agent/
tools/
data/
```

## Skrypt

Otwórz następujący plik:

Terminal

```powershell
user@machine$ cat agent/01_basic_llm_workflow.py
```

Zobaczysz, że skrypt wykonuje cztery proste kroki:

1. Załaduj przykładowe żądanie.
2. Utwórz monit.
3. Wyślij monit do modelu.
4. Wydrukuj i zapisz odpowiedź.

Ten plik nie `TODO`wymaga żadnych działań – działa od początku do końca. Jedyne poprawki dotyczą przykładowego żądania/monitu i żądanego wyniku logu.

Przykładowe żądanie jest ładowane z `data/sample_requests.json`

Przykładowa prośba:

```json
{
  "request_id": "REQ-001",
  "task": "Summarise the latest research on AI agent tool calling in two sentences.",
  "audience": "junior security analyst",
  "expected_route": "direct_answer"
}
```

Skrypt wykorzystuje to żądanie do utworzenia monitu podobnego do:

`You are helping a security team understand an AI research assistant.`  
`Task: Summarise the purpose of an AI research assistant for security analysts.`  
`Audience: junior security analyst`  
`Write a clear and concise explanation.`

Model powinien zwracać krótką odpowiedź skierowaną do określonej **grupy odbiorców** .

## Uruchom przepływ pracy

Z katalogu głównego projektu uruchom:

Terminal

```powershell
user@machine$ python3 agent/01_basic_llm_workflow.py
```

Przejrzyj dane wyjściowe w terminalu, a następnie sprawdź plik dziennika  `logs/agent_foundations.log`.

Każdy wiersz ma format `timestamp | LEVEL | logger name | message`. Powinny pojawić się następujące komunikaty w kolejności:

`Loaded request REQ-001`  
`'Summarise the latest research on AI agent tool calling in two sentences.'`  
`Built prompt from request.`  
`Model response received.`  
`Workflow run completed.`

## Modyfikuj żądanie

Otwórz  `data/sample_requests.json`plik:

Terminal

```powershell
user@machine$ nano data/sample_requests.json
```

Znajdź prośbę `request_id` `REQ-001`i zmień grupę docelową z:

`junior security analyst`

Do:

`SOC manager`

Uruchom skrypt ponownie:

Terminal

```powershell
user@machine$ python3 agent/01_basic_llm_workflow.py
```

Następnie porównaj nową odpowiedź z poprzednią. Główny temat powinien pozostać spójny, ale wyjaśnienie powinno być dostosowane do nowej publiczności.

Po wykonaniu tego zadania powinieneś być w stanie wyjaśnić, jak działa podstawowy przepływ pracy LLM w Pythonie i dlaczego nie jest on jeszcze agentem. Przepływ pracy nie wybiera narzędzi, nie aktualizuje stanu, nie przechodzi między ścieżkami, nie ponawia nieudanych kroków ani nie decyduje, jaką czynność wykonać. Zamiast tego podąża ustaloną ścieżką wykonania od wejścia do wyjścia.

W poprzednim zadaniu uruchomiłeś podstawowe Magister prawa przepływ pracy podążający ustaloną ścieżką:

Wejście → Monit → Model → Wyjście

Podejście to jest przydatne w przypadku zadań przewidywalnych, ma jednak istotne ograniczenie: model może reagować wyłącznie na podstawie kontekstu podanego w poleceniu i dostępnej mu wiedzy.

Poniższy rysunek porównuje stały przepływ pracy LLM z małym agentem wywołującym narzędzia w stylu LangChain. Kluczowa różnica polega na tym, że wywołanie narzędzia pozwala modelowi zażądać zatwierdzonych możliwości zewnętrznych, zamiast polegać wyłącznie na natychmiastowym kontekście i wiedzy o modelu.

![Podstawowy przepływ pracy i Langchain](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786465966103.png)

W tym zadaniu zbudujesz małego agenta wywołującego narzędzie LangChain. Zamiast tworzyć cały **AtlasJako agent ds. badań** będziesz się jednak koncentrować na podstawowej interakcji między użytkownikiem, modelem, zatwierdzonym narzędziem, wynikiem narzędzia i ostateczną odpowiedzią.

## Dlaczego warto łączyć narzędzia ze źródłami danych?

Model nie wie automatycznie, co dzieje się w danym środowisku. W procesach bezpieczeństwa istotne dowody mogą być rozproszone w obrębie telemetrii punktów końcowych, dzienników tożsamości, zdarzeń sieciowych, alertów w chmurze, rejestrów luk w zabezpieczeniach, notatek z poprzednich dochodzeń i historii zgłoszeń.

Każda platforma może zapewniać szeroki wgląd w jedną część środowiska, nie dając pełnego obrazu. Na przykład narzędzie do obsługi punktów końcowych może ujawniać aktywność procesów i urządzeń, podczas gdy kontekst dotyczący tożsamości, sieci, chmury lub analizy historycznej pozostaje w innych systemach.

Wywołanie narzędzi pomaga przezwyciężyć te luki, łącząc przepływ pracy z zatwierdzonymi źródłami danych, zamiast zmuszać model do polegania na niepełnym kontekście lub domysłach. W dobrze zaprojektowanym agencie narzędzia nie są zatem jedynie dodatkowymi możliwościami; to kontrolowane okna do zaufanych danych.

![Narzędzia i bogatszy widok dochodzenia](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786974702240.png)

## Dlaczego warto używać LangChain?

Wywołanie narzędzi można zaimplementować ręcznie, ale frameworki takie jak **LangChain** zapewniają standardowe interfejsy do łączenia modeli języka, komunikatów i narzędzi. LangChain jest przydatny, gdy aplikacja potrzebuje niewielkiego zestawu kontrolowanych narzędzi i prostej pętli wykonania, umożliwiając modelowi żądanie narzędzia, podanie jego argumentów, otrzymanie wyniku i kontynuowanie przepływu pracy.

Jednak LangChain nie zapewnia domyślnie bezpieczeństwa systemu. Deweloper nadal musi kontrolować, które narzędzia są dostępne, weryfikować dane wejściowe, obsługiwać błędy i ograniczać uprawnienia każdego narzędzia. Model może decydować, którego zatwierdzonego narzędzia zażądać, ale aplikacja Python pozostaje odpowiedzialna za weryfikację i wykonanie tego żądania.

## Definiowanie narzędzi

Na swoim komputerze otwórz następujący plik:

Terminal

```powershell
user@machine$ nano ~/agent-foundations/tools/source_tools.py
```

Plik zawiera już importy, `ALLOWED_SEVERITIES`wyrażenie `CVE_ID_PATTERN`regularne i `SECURITY_RECORDS`słownik zastępczy z kluczem CVE. Oba narzędzia są już również odchudzone, z `@tool`dekoratorem, docstringiem i `TODO`miejscem, w którym znajduje się logika wyszukiwania:

```python
@tool
def search_security_record(cve_id: str) -> dict:
    """
    Look up a single security record by its CVE identifier (e.g. 'CVE-2025-1001').

    Returns a dict with a "found" key. When found, also includes "cve_id",
    "title", "severity", and "description". When not found - including when
    cve_id isn't a validly formatted CVE identifier - includes an "error"
    key instead.
    """
    # TODO: validate `cve_id` against CVE_ID_PATTERN, then look it up in
    # SECURITY_RECORDS.
```

Wypełnij `TODO`:

```python
@tool
def search_security_record(cve_id: str) -> dict:
    """
    Look up a single security record by its CVE identifier (e.g. 'CVE-2025-1001').

    Returns a dict with a "found" key. When found, also includes "cve_id",
    "title", "severity", and "description". When not found - including when
    cve_id isn't a validly formatted CVE identifier - includes an "error"
    key instead.
    """
    if not isinstance(cve_id, str) or not CVE_ID_PATTERN.match(cve_id.strip()):
        return {
            "found": False,
            "cve_id": str(cve_id),
            "error": "Invalid CVE identifier format. Expected 'CVE-YYYY-NNNN'.",
        }

    normalized = cve_id.strip().upper()
    record = SECURITY_RECORDS.get(normalized)
    if record is None:
        return {
            "found": False,
            "cve_id": normalized,
            "error": "No security record found for this CVE identifier.",
        }

    return {"found": True, "cve_id": normalized, **record}
```

Zrób to samo dla drugiego narzędzia:

```python
@tool
def list_security_records(severity: Literal["critical", "high", "medium", "low"]) -> dict:
    """
    List security records filtered by severity.

    Args:
        severity: One of 'critical', 'high', 'medium', 'low'.

    Returns:
        {"severity_filter": str, "count": int,
         "records": [{"cve_id": str, "title": str, "severity": str}, ...]}
    """
    if severity not in ALLOWED_SEVERITIES:
        return {
            "severity_filter": str(severity),
            "count": 0,
            "records": [],
            "error": f"severity must be one of {ALLOWED_SEVERITIES}.",
        }

    records = [
        {"cve_id": cve_id, "title": data["title"], "severity": data["severity"]}
        for cve_id, data in SECURITY_RECORDS.items()
        if data["severity"] == severity
    ]

    return {"severity_filter": severity, "count": len(records), "records": records}
```

Dekorator `@tool`konwertuje każdą funkcję Pythona na narzędzie LangChain. Nazwa funkcji, docstring i adnotacje typu opisują narzędzie w modelu, pomagając mu określić, kiedy należy go użyć i jakich argumentów potrzebuje. Każde narzędzie zwraca ustrukturyzowany słownik zamiast tekstu w dowolnej formie, co ułatwia inspekcję, walidację i ponowne wykorzystanie wyniku w całym procesie pracy. Oba narzędzia weryfikują swoje dane wejściowe względem  `SECURITY_RECORDS`/ `ALLOWED_SEVERITIES`przed wykonaniem jakichkolwiek innych czynności – nigdy nie należy ufać, że argument modelu jest poprawnie sformatowany.

## Budowanie agenta

Otwórz plik agenta:

Terminal

```powershell
user@machine$ nano agent/02_langchain_tool_agent.py
```

Dodaj wymagany import:

```python
from langchain.agents import create_agent
```

Model i zatwierdzony zestaw narzędzi są już zdefiniowane:

```python
model = get_model(supports_tools=True)
tools = [search_security_record, list_security_records]
```

Teraz zastąp `agent = None`symbol zastępczy prawdziwym agentem:

```python
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=(
        "You are a security research assistant. "
        "Use only the provided tools to retrieve security records. "
        "Do not invent records or tool results. "
        "Clearly state when a record cannot be found."
    ),
)
```

Monit systemowy definiuje rolę i granice agenta. Nakazuje modelowi korzystanie z zatwierdzonych narzędzi zamiast tworzenia rekordów bezpieczeństwa.

`run_agent()`jest już zaimplementowany - wywołuje agenta z żądaniem użytkownika i zwraca treść ostatecznej wiadomości:

```python
def run_agent(user_request: str) -> str:
    """
    Invoke the agent with a single user message and return the final
    assistant message's content.
    """
    if agent is None:
        # Safe placeholder: lets this script run before the agent above is built.
        logger.info("run_agent() is using the placeholder implementation (agent is None).")
        return "TODO: run_agent() is not implemented yet."

    result = agent.invoke({"messages": [{"role": "user", "content": user_request}]})
    return result["messages"][-1].content
```

Once `agent`jest rzeczywistym `create_agent(...)`obiektem, a nie `None`, więc powyższa gałąź zastępcza nigdy nie jest uruchamiana.

Punkt wejścia jest również już zapisany i wyświetla flagę, gdy odpowiedź agenta faktycznie wspomni o zapytanym CVE:

```python
if __name__ == "__main__":
    print("=== 02_langchain_tool_agent ===")

    response = run_agent("Find the security record for CVE-2025-1001.")
    print(response)

    if agent is not None and "TODO" not in response and "CVE-2025-1001" in response:
        flag = get_flag("langchain_tool_agent_working")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print("\nThe agent isn't fully working yet - no flag.")
```

## Uruchom agenta

Terminal

```powershell
user@machine$ python3 agent/02_langchain_tool_agent.py
```

Agent powinien użyć zatwierdzonego narzędzia do pobrania rekordu CVE-2025-1001, generuje krótką odpowiedź na podstawie wyniku narzędzia i drukuje flagę.

Teraz tymczasowo zmień żądanie przekazane `run_agent()`w punkcie wejścia na :`02_langchain_tool_agent.py`

```python
response = run_agent("Find the security record for 1001.")
```

Uruchom skrypt ponownie:

Terminal

```powershell
user@machine$ python3 agent/02_langchain_tool_agent.py
```

`search_security_record`Należy odrzucić `"1001"`jako nieprawidłowy format CVE, a agent powinien zgłosić, że nie znaleziono rekordu, zamiast go tworzyć – `"CVE-2025-1001"`nie pojawi się w odpowiedzi, więc flaga nie zostanie wydrukowana dla tego przebiegu. Jest to oczekiwane: pokazuje to, że narzędzie nie ufa bezkrytycznie argumentowi modelu, ale weryfikuje dane wejściowe przed ich przetworzeniem i zwróceniem wyniku.

Zmień żądanie z powrotem na:

```python
response = run_agent("Find the security record for CVE-2025-1001.")
```

Zanim przejdziemy dalej, skrypt ponownie drukuje flagę.

W poprzednim zadaniu agent LangChain zwrócił odpowiedź w języku naturalnym. Chociaż ten format jest przydatny dla ludzi, jego walidacja, testowanie i ponowne wykorzystanie przez oprogramowanie może być trudne. Przepływy pracy agentów często wymagają przewidywalnych, ustrukturyzowanych wyników, aby inne części aplikacji mogły niezawodnie wyodrębnić informacje, takie jak:

- Czy potrzebne było narzędzie?
- Jaki poziom ryzyka został przypisany?
- Co powinno się wydarzyć dalej?
- Czy odpowiedź była prawidłowa?

Jeśli model zwraca akapit w dowolnej formie, istotne szczegóły mogą być brakujące, niespójne lub trudne do przeanalizowania przez oprogramowanie. Ustrukturyzowane wyniki rozwiązują ten problem, wymagając, aby odpowiedź była zgodna z określonym schematem.

Zamiast zwracać wyłącznie tekst, przepływ pracy może wygenerować pola takie jak:

- `request_id`
- `summary`
- `risk_level`

Dzięki temu dane wyjściowe można łatwiej sprawdzać, rejestrować, testować, ponownie wykorzystywać i przekazywać do następnego etapu przepływu pracy.

## Dlaczego ustrukturyzowane wyniki są ważne

Odpowiedzi modelu w formie swobodnej są elastyczne, ale ta elastyczność może prowadzić do niejednoznaczności. Na przykład model może zwrócić:

_Ta prośba wydaje się ważna. Myślę, że analityk powinien ją wkrótce przejrzeć._

Mimo że odpowiedź wydaje się rozsądna, nie wskazuje ona jasno przypisanego poziomu ryzyka, nie określa, czy potrzebne było jakieś narzędzie, ani jakie działanie należy podjąć.

Ustrukturyzowany wynik jest bardziej przejrzysty:

```json
{ 
 "request_id": "REQ-003",
 "summary": "The request asks for a security record review.",
 "needs_tools": true,
 "risk_level": "medium",
 "next_action": "retrieve_security_record",
 "confidence": 0.78 
}
```

Drugą odpowiedź łatwiej sprawdzić, ponieważ każde pole ma określony cel.

![Ustrukturyzowane wyniki](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786972844367.png)

## Skrypt

Na swoim komputerze otwórz następujący plik:

Terminal

```powershell
user@machine$ nano agent/03_structured_outputs.py
```

Ten skrypt definiuje już kontrakt wyjściowy: `StructuredResponse`model Pydantic z  polami `request_id`, `summary`, `needs_tools`, `risk_level`,  `next_action`i `confidence`oraz walidatorami odrzucającymi wszystko, co znajduje się poza dozwolonymi wartościami:

```python
ALLOWED_RISK_LEVELS = ["low", "medium", "high"]
ALLOWED_NEXT_ACTIONS = [
    "answer_directly",
    "retrieve_sources",
    "request_human_review",
    "reject_request",
]

class StructuredResponse(BaseModel):
    """The schema every structured agent response must satisfy."""

    request_id: str
    summary: str
    needs_tools: bool
    risk_level: str
    next_action: str
    confidence: float

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        if value not in ALLOWED_RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {ALLOWED_RISK_LEVELS}, got {value!r}")
        return value

    @field_validator("next_action")
    @classmethod
    def validate_next_action(cls, value: str) -> str:
        if value not in ALLOWED_NEXT_ACTIONS:
            raise ValueError(f"next_action must be one of {ALLOWED_NEXT_ACTIONS}, got {value!r}")
        return value

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {value!r}")
        return value
```

Ograniczenie `risk_level`i `next_action`do ustalonego zestawu wartości sprawia, że ​​nieprawidłowe lub niespójne wyniki modelu można łatwo wychwycić zanim jakiekolwiek dalsze etapy nabiorą do nich zaufania.

## Uzupełnianie logiki klasyfikacji

Schemat już istnieje - twoją pracą jest praca `TODO`wewnątrz  `generate_structured_response()`.

Ta funkcja obecnie tworzy kandydata na symbol zastępczy, który zawsze zgłasza `low`ryzyko i `answer_directly`, niezależnie od rzeczywistego żądania. Zastąp symbol zastępczy logiką, która wywołuje współdzielony `classify_request_type()`pomocnik (z `agent/config.py`) i mapuje jego wynik na `risk_level`, `next_action`, i `needs_tools`:

|`request_type`|`risk_level`|`next_action`|`needs_tools`|
|---|---|---|---|
|`invalid`|`low`|`reject_request`|`False`|
|`human_review`|`high`|`request_human_review`|`False`|
|`source_lookup`|`medium`|`retrieve_sources`|`True`|
|`direct_answer`|`low`|`answer_directly`|`False`|

`confidence`powinien nastąpić `{"low": 0.9, "medium": 0.75, "high": 0.55}[risk_level]`.

```python
def generate_structured_response(request: dict) -> dict:
    """Build a candidate structured response from a classification + model summary."""
    task_text = request.get("task", "")

    model = get_model()
    model_summary = model.invoke(f"Summarise this request for a structured report: {task_text}").content
    logger.info("Model produced a raw summary for the structured response.")

    classification = classify_request_type(task_text)
    request_type = classification["request_type"]

    if request_type == "invalid":
        risk_level, next_action, needs_tools = "low", "reject_request", False
    elif request_type == "human_review":
        risk_level, next_action, needs_tools = "high", "request_human_review", False
    elif request_type == "source_lookup":
        risk_level, next_action, needs_tools = "medium", "retrieve_sources", True
    else:  # direct_answer
        risk_level, next_action, needs_tools = "low", "answer_directly", False

    confidence = {"low": 0.9, "medium": 0.75, "high": 0.55}[risk_level]

    candidate = {
        "request_id": request["request_id"],
        "summary": model_summary,
        "needs_tools": needs_tools,
        "risk_level": risk_level,
        "next_action": next_action,
        "confidence": confidence,
    }
    logger.info(f"Structured candidate built for {request['request_id']}: {candidate}")
    return candidate
```

Pozostała część pliku ( `load_sample_request`, `validate_structured_response`i `__main__`blok) jest już kompletna — weryfikuje ona kandydata `StructuredResponse`i drukuje flagę, gdy  poprawnie `generate_structured_response()` sklasyfikuje żądanie próbki ( `REQ-002`, żądanie wyszukiwania źródła) jako `next_action="retrieve_sources"`,,  `needs_tools=True`.`risk_level="medium"`

## Uruchom skrypt

Punkt wejścia na dole pliku jest już zapisany – nie musisz go dodawać:

```python
if __name__ == "__main__":
    print("=== 03_structured_outputs: generate -> validate -> emit structured JSON ===")

    sample_request = load_sample_request("REQ-002")
    candidate_response = generate_structured_response(sample_request)

    validated_response = validate_structured_response(candidate_response)

    print("\nValidated structured output:")
    print(json.dumps(validated_response.model_dump(), indent=2))

    if (
        validated_response.next_action == "retrieve_sources"
        and validated_response.needs_tools is True
        and validated_response.risk_level == "medium"
    ):
        flag = get_flag("structured_outputs_validated")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print("\ngenerate_structured_response() isn't using classify_request_type() yet - no flag.")
```

Uruchom to:

Terminal

```powershell
user@machine$ python3 agent/03_structured_outputs.py
```

Po umieszczeniu mapowania powinieneś zobaczyćJSONodpowiedź zgodna `StructuredResponse`ze schematem `REQ-002`(żądanie wyszukiwania źródła) i wydrukowana flaga.

## Przetestuj walidację

Teraz zrób to celowo. W `generate_structured_response()`, tymczasowo zmień `source_lookup`gałąź z:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "medium", "retrieve_sources", True
```

Do:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "critical", "retrieve_sources", True
```

Uruchom skrypt ponownie:

Terminal

```powershell
user@machine$ python3 agent/03_structured_outputs.py
```

`validate_structured_response()`powinien zgłosić błąd `ValidationError`, ponieważ  `"critical"`nie jest jednym z `ALLOWED_RISK_LEVELS`. To pokazuje, jak walidatory schematu wychwytują nieprawidłową wartość, zanim cokolwiek w dalszej części schematu zacznie jej ufać.

Przed kontynuowaniem zmień gałąź z powrotem na:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "medium",
```

W poprzednim zadaniu agent LangChain zwrócił odpowiedź w języku naturalnym. Chociaż ten format jest przydatny dla ludzi, jego walidacja, testowanie i ponowne wykorzystanie przez oprogramowanie może być trudne. Przepływy pracy agentów często wymagają przewidywalnych, ustrukturyzowanych wyników, aby inne części aplikacji mogły niezawodnie wyodrębnić informacje, takie jak:

- Czy potrzebne było narzędzie?
- Jaki poziom ryzyka został przypisany?
- Co powinno się wydarzyć dalej?
- Czy odpowiedź była prawidłowa?

Jeśli model zwraca akapit w dowolnej formie, istotne szczegóły mogą być brakujące, niespójne lub trudne do przeanalizowania przez oprogramowanie. Ustrukturyzowane wyniki rozwiązują ten problem, wymagając, aby odpowiedź była zgodna z określonym schematem.

Zamiast zwracać wyłącznie tekst, przepływ pracy może wygenerować pola takie jak:

- `request_id`
- `summary`
- `risk_level`

Dzięki temu dane wyjściowe można łatwiej sprawdzać, rejestrować, testować, ponownie wykorzystywać i przekazywać do następnego etapu przepływu pracy.

## Dlaczego ustrukturyzowane wyniki są ważne

Odpowiedzi modelu w formie swobodnej są elastyczne, ale ta elastyczność może prowadzić do niejednoznaczności. Na przykład model może zwrócić:

_Ta prośba wydaje się ważna. Myślę, że analityk powinien ją wkrótce przejrzeć._

Mimo że odpowiedź wydaje się rozsądna, nie wskazuje ona jasno przypisanego poziomu ryzyka, nie określa, czy potrzebne było jakieś narzędzie, ani jakie działanie należy podjąć.

Ustrukturyzowany wynik jest bardziej przejrzysty:

```json
{ 
 "request_id": "REQ-003",
 "summary": "The request asks for a security record review.",
 "needs_tools": true,
 "risk_level": "medium",
 "next_action": "retrieve_security_record",
 "confidence": 0.78 
}
```

Drugą odpowiedź łatwiej sprawdzić, ponieważ każde pole ma określony cel.

![Ustrukturyzowane wyniki](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786972844367.png)

## Skrypt

Na swoim komputerze otwórz następujący plik:

Terminal

```powershell
user@machine$ nano agent/03_structured_outputs.py
```

Ten skrypt definiuje już kontrakt wyjściowy: `StructuredResponse`model Pydantic z  polami `request_id`, `summary`, `needs_tools`, `risk_level`,  `next_action`i `confidence`oraz walidatorami odrzucającymi wszystko, co znajduje się poza dozwolonymi wartościami:

```python
ALLOWED_RISK_LEVELS = ["low", "medium", "high"]
ALLOWED_NEXT_ACTIONS = [
    "answer_directly",
    "retrieve_sources",
    "request_human_review",
    "reject_request",
]

class StructuredResponse(BaseModel):
    """The schema every structured agent response must satisfy."""

    request_id: str
    summary: str
    needs_tools: bool
    risk_level: str
    next_action: str
    confidence: float

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        if value not in ALLOWED_RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {ALLOWED_RISK_LEVELS}, got {value!r}")
        return value

    @field_validator("next_action")
    @classmethod
    def validate_next_action(cls, value: str) -> str:
        if value not in ALLOWED_NEXT_ACTIONS:
            raise ValueError(f"next_action must be one of {ALLOWED_NEXT_ACTIONS}, got {value!r}")
        return value

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {value!r}")
        return value
```

Ograniczenie `risk_level`i `next_action`do ustalonego zestawu wartości sprawia, że ​​nieprawidłowe lub niespójne wyniki modelu można łatwo wychwycić zanim jakiekolwiek dalsze etapy nabiorą do nich zaufania.

## Uzupełnianie logiki klasyfikacji

Schemat już istnieje - twoją pracą jest praca `TODO`wewnątrz  `generate_structured_response()`.

Ta funkcja obecnie tworzy kandydata na symbol zastępczy, który zawsze zgłasza `low`ryzyko i `answer_directly`, niezależnie od rzeczywistego żądania. Zastąp symbol zastępczy logiką, która wywołuje współdzielony `classify_request_type()`pomocnik (z `agent/config.py`) i mapuje jego wynik na `risk_level`, `next_action`, i `needs_tools`:

|`request_type`|`risk_level`|`next_action`|`needs_tools`|
|---|---|---|---|
|`invalid`|`low`|`reject_request`|`False`|
|`human_review`|`high`|`request_human_review`|`False`|
|`source_lookup`|`medium`|`retrieve_sources`|`True`|
|`direct_answer`|`low`|`answer_directly`|`False`|

`confidence`powinien nastąpić `{"low": 0.9, "medium": 0.75, "high": 0.55}[risk_level]`.

```python
def generate_structured_response(request: dict) -> dict:
    """Build a candidate structured response from a classification + model summary."""
    task_text = request.get("task", "")

    model = get_model()
    model_summary = model.invoke(f"Summarise this request for a structured report: {task_text}").content
    logger.info("Model produced a raw summary for the structured response.")

    classification = classify_request_type(task_text)
    request_type = classification["request_type"]

    if request_type == "invalid":
        risk_level, next_action, needs_tools = "low", "reject_request", False
    elif request_type == "human_review":
        risk_level, next_action, needs_tools = "high", "request_human_review", False
    elif request_type == "source_lookup":
        risk_level, next_action, needs_tools = "medium", "retrieve_sources", True
    else:  # direct_answer
        risk_level, next_action, needs_tools = "low", "answer_directly", False

    confidence = {"low": 0.9, "medium": 0.75, "high": 0.55}[risk_level]

    candidate = {
        "request_id": request["request_id"],
        "summary": model_summary,
        "needs_tools": needs_tools,
        "risk_level": risk_level,
        "next_action": next_action,
        "confidence": confidence,
    }
    logger.info(f"Structured candidate built for {request['request_id']}: {candidate}")
    return candidate
```

Pozostała część pliku ( `load_sample_request`, `validate_structured_response`i `__main__`blok) jest już kompletna — weryfikuje ona kandydata `StructuredResponse`i drukuje flagę, gdy  poprawnie `generate_structured_response()` sklasyfikuje żądanie próbki ( `REQ-002`, żądanie wyszukiwania źródła) jako `next_action="retrieve_sources"`,,  `needs_tools=True`.`risk_level="medium"`

## Uruchom skrypt

Punkt wejścia na dole pliku jest już zapisany – nie musisz go dodawać:

```python
if __name__ == "__main__":
    print("=== 03_structured_outputs: generate -> validate -> emit structured JSON ===")

    sample_request = load_sample_request("REQ-002")
    candidate_response = generate_structured_response(sample_request)

    validated_response = validate_structured_response(candidate_response)

    print("\nValidated structured output:")
    print(json.dumps(validated_response.model_dump(), indent=2))

    if (
        validated_response.next_action == "retrieve_sources"
        and validated_response.needs_tools is True
        and validated_response.risk_level == "medium"
    ):
        flag = get_flag("structured_outputs_validated")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print("\ngenerate_structured_response() isn't using classify_request_type() yet - no flag.")
```

Uruchom to:

Terminal

```powershell
user@machine$ python3 agent/03_structured_outputs.py
```

Po umieszczeniu mapowania powinieneś zobaczyćJSONodpowiedź zgodna `StructuredResponse`ze schematem `REQ-002`(żądanie wyszukiwania źródła) i wydrukowana flaga.

## Przetestuj walidację

Teraz zrób to celowo. W `generate_structured_response()`, tymczasowo zmień `source_lookup`gałąź z:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "medium", "retrieve_sources", True
```

Do:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "critical", "retrieve_sources", True
```

Uruchom skrypt ponownie:

Terminal

```powershell
user@machine$ python3 agent/03_structured_outputs.py
```

`validate_structured_response()`powinien zgłosić błąd `ValidationError`, ponieważ  `"critical"`nie jest jednym z `ALLOWED_RISK_LEVELS`. To pokazuje, jak walidatory schematu wychwytują nieprawidłową wartość, zanim cokolwiek w dalszej części schematu zacznie jej ufać.

Przed kontynuowaniem zmień gałąź z powrotem na:

```python
elif request_type == "source_lookup":
    risk_level, next_action, needs_tools = "medium", "retrieve_sources", True
```

W poprzednich zadaniach przepływ pracy albo podążał ustaloną ścieżką, albo zwracał ustrukturyzowaną decyzję. Jednak rzeczywiste przepływy pracy agentów często wymagają przechowywania informacji w wielu krokach, takich jak pierwotne żądanie, jego typ, czy użyto narzędzia, czy wystąpił błąd i ostateczna odpowiedź.

Te śledzone informacje nazywane są stanem. Przenosząc ustrukturyzowany obiekt przez przepływ pracy zamiast przekazywania luźnych wartości między funkcjami, stan ułatwia inspekcję, testowanie i debugowanie każdego kroku.

W tym zadaniu użyjesz LangGraph do zbudowania małego przepływu pracy ze stanem, który podąża następującą ścieżką:

START → load_request → classify_request → generate_answer → END

Każdy węzeł odczytuje bieżący stan, aktualizuje odpowiednie pola i zwraca tylko te pola, które zmienił — LangGraph łączy te dane ze współdzielonym stanem przed przekazaniem go do następnego węzła.

## Dlaczego stan ma znaczenie

Podstawowy przepływ pracy w Pythonie umożliwia bezpośrednie przekazywanie wartości między funkcjami, co sprawdza się w przypadku małych skryptów. Jednak wraz ze wzrostem agentywności przepływy pracy często muszą śledzić dodatkowe informacje:

- Jakie było pierwotne żądanie?
- Jakiego rodzaju jest to prośba?
- Czy były potrzebne narzędzia?
- Czy któryś krok się nie powiódł?
- Jaka odpowiedź została wygenerowana?

Stan zapewnia wspólną strukturę do przechowywania i aktualizowania informacji w całym przepływie pracy. Ponieważ każdy krok rejestruje zmiany, przepływ pracy ze stanem jest łatwiejszy do inspekcji i debugowania, zwłaszcza przed wprowadzeniem rozgałęzień, ponownych prób lub punktów zatwierdzania przez człowieka.

Staje się to jeszcze ważniejsze, gdy przepływ pracy łączy się z wieloma źródłami danych. Jeśli agent sprawdza dane telemetryczne punktów końcowych, logi tożsamości, rejestry luk w zabezpieczeniach i wcześniejsze notatki, powinien śledzić, które źródła zostały zapytane, co każde z nich zwróciło i jakich dowodów nadal brakuje. Bez tego współdzielonego stanu znacznie trudniej jest wyjaśnić, w jaki sposób agent doszedł do swoich wniosków.

## Skrypt

Otwórz następujący plik:

Terminal

```powershell
user@machine$ nano agent/04_langgraph_state.py
```

Schemat stanu jest już dla Ciebie zdefiniowany:

```python
class AgentState(TypedDict):
    """The shared state object every node in the graph reads and updates."""

    request_id: str
    user_request: str
    request_type: str
    tool_results: list
    errors: list
    final_answer: str
```

`AgentState`definiuje pola, które poruszają się po wykresie:

- `request_id` 
- `user_request`
- `request_type`
- `tool_results`
- `errors`
- `final_answer`

## Węzły, które są już podłączone

Węzeł LangGraph to funkcja, która odbiera aktualny stan i zwraca słownik pól, które chce zaktualizować — nie musi zwracać całego stanu.

Trzy z czterech węzłów są już dla Ciebie zaimplementowane:

```python
def load_request(state: AgentState) -> dict:
    """Node 1: populate request_id and user_request from sample data."""
    with open(SAMPLE_REQUESTS_PATH, "r", encoding="utf-8") as f:
        requests = json.load(f)

    request = requests[0]
    logger.info(f"[load_request] Loaded {request['request_id']}.")

    return {
        "request_id": request["request_id"],
        "user_request": request["task"],
    }

def classify_request(state: AgentState) -> dict:
    """Node 2: classify the request and record the result in tool_results."""
    classification = classify_request_type(state["user_request"])
    logger.info(f"[classify_request] request_type={classification['request_type']}")

    updated_tool_results = state["tool_results"] + [
        {"tool": "classify_request_type", "result": classification}
    ]

    return {
        "request_type": classification["request_type"],
        "tool_results": updated_tool_results,
    }

def log_summary(state: AgentState) -> dict:
    """Node 3: log a summary of state so far. No state changes needed."""
    logger.info(
        f"[log_summary] request_id={state['request_id']} "
        f"request_type={state['request_type']} "
        f"tool_calls_so_far={len(state['tool_results'])}"
    )
    return {}
```

`load_request`Odczytuje pierwsze przykładowe żądanie z `data/sample_requests.json`. `classify_request`Używa `classify_request_type()`z `agent/config.py`, tego samego pomocnika, który został wprowadzony w poprzednim zadaniu. Rejestruje również wywołanie, `tool_results`dzięki czemu stan pokazuje, które „narzędzia” zostały uruchomione. `log_summary`Nie zmienia żadnego stanu – po prostu rejestruje, na jakim etapie znajduje się przepływ pracy.

## Zakończenie czwartego węzła

Twoim pierwszym zadaniem jest `TODO`in `generate_answer()`. W tej chwili funkcja zwraca ciąg zastępczy.

Zastąp ją logiką, która używa `state["request_type"]`i `state["user_request"]`do zbudowania monitu, a następnie wywołuje model.

```python
def generate_answer(state: AgentState) -> dict:
    """Node 4: call the model to produce the final answer."""
    prompt = (
        f"Summarise this {state['request_type']} request in one sentence: "
        f"{state['user_request']}"
    )
    answer = get_model().invoke(prompt).content
    logger.info("[generate_answer] Final answer generated.")

    return {"final_answer": answer}
```

## Budowanie wykresu

Twoim drugim zadaniem jest `TODO`wejście `build_graph()`. Obecnie rejestruje ono tylko `load_request`i łączy je bezpośrednio `END`jako bezpieczny symbol zastępczy. Zarejestruj pozostałe trzy węzły i połącz wszystkie pięć krawędzi:

```python
def build_graph() -> StateGraph:
    """Wire the nodes together into the START -> ... -> END graph."""
    graph = StateGraph(AgentState)

    graph.add_node("load_request", load_request)
    graph.add_node("classify_request", classify_request)
    graph.add_node("log_summary", log_summary)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "load_request")
    graph.add_edge("load_request", "classify_request")
    graph.add_edge("classify_request", "log_summary")
    graph.add_edge("log_summary", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()
```

Definiuje ścieżkę wykonania: graf rozpoczyna się, ładuje żądanie, klasyfikuje je, rejestruje podsumowanie, generuje odpowiedź i kończy działanie.

## Uruchom przepływ pracy

Punkt wejścia na dole pliku jest już dla Ciebie zapisany:

```python
if __name__ == "__main__":
    print("=== 04_langgraph_state: START -> load_request -> classify_request -> log_summary -> generate_answer -> END ===")

    compiled_graph = build_graph()

    initial_state: AgentState = {
        "request_id": "",
        "user_request": "",
        "request_type": "",
        "tool_results": [],
        "errors": [],
        "final_answer": "",
    }

    final_state = compiled_graph.invoke(initial_state)

    print("\nFinal state:")
    print(json.dumps(final_state, indent=2))

    logger.info("LangGraph run complete.")

    if (
        final_state["request_type"]
        and final_state["final_answer"]
        and "TODO" not in final_state["final_answer"]
    ):
        flag = get_flag("langgraph_nodes_connected")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print("\nThe graph isn't fully wired yet (build_graph()/generate_answer()) - no flag.")
```

Uruchom to:

Terminal

```powershell
user@machine$ python3 agent/04_langgraph_state.py
```

Stan końcowy powinien zostać wyświetlony w terminalu wraz z flagą po `TODO`zakończeniu obu operacji. Należy zauważyć, że przepływ pracy zwraca więcej niż tylko odpowiedź: ujawnia również informacje przenoszone i aktualizowane w całym grafie ( `request_type`, `tool_results`, itd.).

W poprzednim zadaniu wykorzystałeś stan LangGraph do przenoszenia informacji przez ustalony przepływ pracy:

START → load_request → classify_request → generate_answer → END

To podejście jest przydatne, ale wiele przepływów pracy agentów wymaga wyboru różnych ścieżek w zależności od żądania. Proste pytanie może wymagać bezpośredniej odpowiedzi,CVE- żądanie związane z tematem może wymagać sprawdzenia źródła, a niebezpieczne lub nieobsługiwane żądanie może wymagać odrzucenia.

W tym miejscu przydatne stają się rozgałęzienia i routing. Rozgałęzienia pozwalają przepływowi pracy wybrać kolejny węzeł na podstawie wartości przechowywanych w stanie, dzięki czemu każde żądanie może podążać ścieżką odpowiadającą jego potrzebom.

W tym zadaniu wykonasz przepływ pracy LangGraph z routingiem warunkowym. Każde żądanie rozpoczyna się w gałęzi `classify_request`, a następnie przechodzi przez nią `route_request`, która kieruje je do dokładnie jednej z czterech gałęzi: `direct_answer`, `retrieve_sources`, `needs_human_review`lub `reject_invalid_request`. Po zakończeniu wybranej gałęzi przepływ pracy łączy się ponownie z współdzielonym `finalize`węzłem przed dotarciem do końca grafu.

Żądanie przechodzi przez jedną z czterech gałęzi: `direct_answer`, `retrieve_sources`, `needs_human_review`lub `reject_invalid_request`. Wszystkie cztery gałęzie łączą się ponownie we wspólnym `finalize`węźle przed zakończeniem grafu.

Przepływ pracy przechowuje ważne pola w stanach - `request_type`, `route`, `tool_results`, `errors`, `final_answer`- i `route_request`używa ich `request_type`do decydowania, którą z czterech gałęzi wybrać. Właśnie dlatego stan staje się szczególnie przydatny, gdy przepływy pracy zaczynają się rozgałęziać: zapewnia on grafowi widoczny zapis tego, co się wydarzyło i dlaczego wybrano daną trasę.

![Stan z langgraphem](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786466705493.png)

Właśnie dlatego stan staje się szczególnie przydatny, gdy przepływy pracy zaczynają się rozgałęziać. Dzięki niemu graf zyskuje widoczny zapis tego, co się wydarzyło i dlaczego wybrano trasę.

## Dlaczego rozgałęzianie ma znaczenie

Podstawowy przepływ pracy jest łatwy do zrozumienia, ponieważ każde żądanie podąża tą samą ścieżką. Przepływy pracy związane z bezpieczeństwem i badaniami często wymagają jednak innego zachowania w zależności od żądania, takiego jak bezpośrednia odpowiedź, pobieranie dowodów, bezpieczne zatrzymanie lub odrzucenie czegoś poza zakresem przepływu pracy.

Rozgałęzienie sprawia, że ​​ta decyzja staje się jednoznaczna. Zamiast ukrywać logikę routingu w długim wierszu poleceń, przepływ pracy zapisuje typ żądania w stanie i używa tej wartości do wyboru następnego kroku. Dzięki temu ścieżka wykonania jest łatwiejsza do sprawdzenia, przetestowania i debugowania.

## Skrypt

Otwórz następujący plik:

Terminal

```powershell
user@machine$ nano agent/05_langgraph_branching.py
```

Stan i tabela routingu są już zdefiniowane:

```python
ALLOWED_ROUTES = [
    "direct_answer",
    "retrieve_sources",
    "needs_human_review",
    "reject_invalid_request",
]

# Maps classify_request_type()'s request_type onto this graph's branch names.
_ROUTE_BY_REQUEST_TYPE = {
    "direct_answer": "direct_answer",
    "source_lookup": "retrieve_sources",
    "human_review": "needs_human_review",
    "invalid": "reject_invalid_request",
}

class BranchingState(TypedDict):
    request_id: str
    user_request: str
    request_type: str
    route: str
    tool_results: list
    errors: list
    final_answer: str
```

`request_type`jest wartością przypisaną przez klasyfikator żądań; `route`jest nazwą gałęzi `route_request`, o której decyduje. `_ROUTE_BY_REQUEST_TYPE`jest tabelą łączącą te dwa elementy.

## Węzły, które są już podłączone

`classify_request`jest już zaimplementowany — wykorzystuje ponownie tę samą  `classify_request_type()`funkcję pomocniczą, której `agent/config.py`użyłeś w dwóch ostatnich zadaniach, i zapisuje wywołanie w `tool_results`:

```python
def classify_request(state: BranchingState) -> dict:
    """Classify the request so route_request has something to branch on."""
    classification = classify_request_type(state["user_request"])
    logger.info(f"[classify_request] request_type={classification['request_type']}")
    return {
        "request_type": classification["request_type"],
        "tool_results": state["tool_results"] + [
            {"tool": "classify_request_type", "result": classification}
        ],
    }
```

Wszystkie cztery węzły rozgałęzień i `finalize`węzeł, do którego się one ponownie łączą, są już również zaimplementowane:

```python
def direct_answer(state: BranchingState) -> dict:
    """Branch: answer simple requests directly with the model."""
    prompt = f"Answer this request directly: {state['user_request']}"
    answer = get_model().invoke(prompt).content
    logger.info("[direct_answer] Answered directly, no source retrieval needed.")
    return {"final_answer": answer}

def retrieve_sources(state: BranchingState) -> dict:
    """Branch: retrieve security records before answering."""
    records = list_security_records.invoke({"severity": "critical"})
    logger.info(f"[retrieve_sources] Retrieved {records['count']} critical record(s).")

    answer = f"Found {records['count']} critical security record(s) to cite in this answer."
    return {
        "final_answer": answer,
        "tool_results": state["tool_results"] + [
            {"tool": "list_security_records", "result": records}
        ],
    }

def needs_human_review(state: BranchingState) -> dict:
    """Branch: stop and flag the request for a human instead of answering."""
    logger.info("[needs_human_review] Request flagged for human review; no automatic answer given.")
    return {
        "final_answer": "This request requires human review before the agent can proceed.",
    }

def reject_invalid_request(state: BranchingState) -> dict:
    """Branch: reject requests that are empty or otherwise invalid."""
    logger.warning("[reject_invalid_request] Request rejected as invalid.")
    return {
        "final_answer": "This request could not be processed - it was empty or invalid.",
        "errors": state["errors"] + ["invalid_request"],
    }

def finalize(state: BranchingState) -> dict:
    """Common exit node: log the final outcome for every branch."""
    logger.info(f"[finalize] route={state['route']} final_answer={state['final_answer']!r}")
    return {}
```

Uwaga `retrieve_sources`wywołuje prawdziwe `list_security_records`narzędzie z  `tools/source_tools.py`tego samego pliku, który ukończyłeś wcześniej w tym pokoju, zamiast zakodowanej odpowiedzi. Tu również `needs_human_review`pojawia się problem: jest to czwarta gałąź, która zatrzymuje przepływ pracy i prosi o kontakt z człowiekiem zamiast generować odpowiedź, w przypadku żądań `classify_request_type()` flagi takie jak  `human_review`.

Selektor krawędzi warunkowej jest już również zaimplementowany:

```python
def select_branch(state: BranchingState) -> str:
    """Conditional-edge function: reads state['route'] and returns the next node name."""
    route = state["route"]
    if route not in ALLOWED_ROUTES:
        logger.warning(f"[select_branch] Unknown route {route!r}; defaulting to reject_invalid_request.")
        return "reject_invalid_request"
    return route
```

`select_branch`nie decyduje o trasie samodzielnie — odczytuje jedynie to, co  `route_request`jest już zapisane w stanie i przekazuje pasującą nazwę węzła do LangGraph.

## Wypełnianie routera

Twoim pierwszym zadaniem jest `TODO`in `route_request()`. Ten węzeł faktycznie decyduje o gałęzi: powinien szukać `state["request_type"]`in  `_ROUTE_BY_REQUEST_TYPE`(wracając do niego `"reject_invalid_request"`w przypadku nierozpoznanego elementu) i zapisać wynik w `"route"`:

```python
def route_request(state: BranchingState) -> dict:
    """Decide which branch to take next."""
    route = _ROUTE_BY_REQUEST_TYPE.get(state["request_type"], "reject_invalid_request")
    logger.info(f"[route_request] Selected route: {route}")
    return {"route": route}
```

Ten węzeł nie generuje ostatecznej odpowiedzi – aktualizuje jedynie stan  `select_branch`(oraz krawędzie warunkowe, które zostaną następnie połączone), dzięki czemu można kierować żądanie.

## Budowanie wykresu

Twoim drugim zadaniem jest `TODO`in `build_graph()`. Wszystkie siedem węzłów jest już zarejestrowanych i `route_request`ma prostą krawędź z  `classify_request`. Brakuje gałęzi warunkowej: zastąp krawędź zastępczą z `route_request`straight na `finalize`with  `add_conditional_edges()`, mapując każdą możliwą `select_branch()`wartość zwracaną na pasujący węzeł:

```python
def build_graph() -> StateGraph:
    graph = StateGraph(BranchingState)

    graph.add_node("classify_request", classify_request)
    graph.add_node("route_request", route_request)
    graph.add_node("direct_answer", direct_answer)
    graph.add_node("retrieve_sources", retrieve_sources)
    graph.add_node("needs_human_review", needs_human_review)
    graph.add_node("reject_invalid_request", reject_invalid_request)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "classify_request")
    graph.add_edge("classify_request", "route_request")

    graph.add_conditional_edges(
        "route_request",
        select_branch,
        {
            "direct_answer": "direct_answer",
            "retrieve_sources": "retrieve_sources",
            "needs_human_review": "needs_human_review",
            "reject_invalid_request": "reject_invalid_request",
        },
    )

    for branch_node in ["direct_answer", "retrieve_sources", "needs_human_review", "reject_invalid_request"]:
        graph.add_edge(branch_node, "finalize")

    graph.add_edge("finalize", END)

    return graph.compile()
```

`add_conditional_edges()`łączy router ze wszystkimi czterema możliwymi gałęziami - `select_branch`wartość zwracana wybiera gałąź, która zostanie uruchomiona, a każda gałąź dołącza ponownie w miejscu  `finalize`poprzednim `END`.

## Uruchom przepływ pracy

W przeciwieństwie do poprzednich zadań punkt wejścia nie uruchamia pojedynczego, zakodowanego na stałe żądania — jest już napisany tak, aby przechodzić przez każde żądanie `data/sample_requests.json`i drukować trasę, jaką każde z nich obrało:

```python
if __name__ == "__main__":
    print("=== 05_langgraph_branching: classify -> route -> (branch) -> finalize ===")

    with open(SAMPLE_REQUESTS_PATH, "r", encoding="utf-8") as f:
        sample_requests = json.load(f)

    compiled = build_graph()
    all_routes_seen = set()

    for sample_request in sample_requests:
        result_state = run_for_request(compiled, sample_request)
        all_routes_seen.add(result_state["route"])
        print(
            f"\n{sample_request['request_id']}: route={result_state['route']} "
            f"(expected={sample_request['expected_route']})"
        )
        print(f"  -> {result_state['final_answer']}")

    logger.info("Branching workflow run complete.")

    if all_routes_seen == set(ALLOWED_ROUTES):
        flag = get_flag("branching_logic_verified")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print(f"\nNot all branches are wired yet (routes seen: {sorted(all_routes_seen)}) - no flag.")
```

Uruchom to:

Terminal

```powershell
user@machine$ python3 agent/05_langgraph_branching.py
```

Po zakończeniu obu `TODO`sekcji powinieneś zobaczyć sześć wierszy wyników, po jednym na każde przykładowe żądanie, każdy pokazujący wybraną trasę obok trasy  `data/sample_requests.json`już oczekiwanej:

- `REQ-001`i `REQ-003`(zwykłe pytania) ->`direct_answer`
- `REQ-002`(prosi o sprawdzenie/podanie źródła) ->`retrieve_sources`
- `REQ-004`i `REQ-006`(pytania ryzykowne lub niejednoznaczne) ->`needs_human_review`
- `REQ-005`(puste żądanie) ->`reject_invalid_request`

Flaga jest wyświetlana, gdy każde żądanie zostanie przekierowane przez wszystkie cztery gałęzie co najmniej raz.

## Decyzja ramowa

Pracowałeś już z trzema różnymi stylami przepływu pracy:

- Prosty przepływ pracy w Pythonie
- Przepływ pracy wywoływania narzędzi LangChain
- Przepływ pracy ze stanem w LangGraph z rozgałęzieniami

Każdy z nich służy innemu celowi. Użyj **zwykłego Pythona** , gdy zadanie jest stałe i przewidywalne, **LangChain** , gdy model potrzebuje dostępu do niewielkiego zestawu zatwierdzonych narzędzi, a **LangGraph,** gdy przepływ pracy wymaga stanu, routingu, rozgałęzień, ponownych prób, punktów zatwierdzenia lub większej kontroli nad wykonywaniem wieloetapowym.

Celem nie jest wybór najbardziej skomplikowanego rozwiązania, lecz najprostszego podejścia, które zapewnia wystarczającą kontrolę nad zadaniem.

Dla pełnej wersji**AtlasAgent ds. badań** w następnym pokoju, LangGraph, jest dobrym wyborem, ponieważ przepływ pracy będzie wymagał wielu kroków, śledzenia stanu, pobierania źródeł, rozgałęzień i możliwości przeglądu wyników.

Przepływy pracy agentów są łatwiejsze do zabezpieczenia, gdy łatwiej je kontrolować. W poprzednich zadaniach zbudowałeś fundamenty: podstawowyMagister prawaPrzepływ pracy, wywołanie narzędzia LangChain, ustrukturyzowane wyniki, stan LangGraph i rozgałęzienia. Każdy komponent jest przydatny, ale każdy może również wprowadzać punkty awarii.

Do typowych usterek należą:

- Nieprawidłowe dane wejściowe narzędzia
- Brak aktualizacji stanu
- Błędne decyzje dotyczące trasowania
- Słaba strukturalna walidacja wyników
- Halucynacyjne używanie narzędzi

Bezpieczny przepływ pracy agenta powinien uwidocznić te błędy. Gdy błędy są ukryte, trudniej zrozumieć, dlaczego agent wygenerował określoną odpowiedź lub podążał określoną ścieżką wykonania.

W tym zadaniu wykonasz cztery małe funkcje demonstracyjne, z których każda odtworzy jedną z tych awarii, wykryje ją, a następnie naprawi — wykorzystując prawdziwe komponenty z poprzednich zadań zamiast ręcznie zaprojektowanych makiet.

## Dlaczego debugowanie ma znaczenie

Przepływy pracy agentów mogą zawodzić w sposób mniej oczywisty niż tradycyjne skrypty. Zwykły skrypt często kończy się niepowodzeniem, gdy kod zgłasza wyjątek, podczas gdy agent może wybrać niewłaściwe narzędzie, pominąć aktualizację stanu, nieprawidłowo skierować żądanie lub wygenerować dane wyjściowe, które wydają się rozsądne, ale nie są zgodne z oczekiwanym schematem.

W procesach bezpieczeństwa te ukryte błędy mogą wpływać na jakość dochodzenia. Dobrze zaprojektowany proces powinien zatem umożliwiać znalezienie odpowiedzi na następujące pytania:

- Jakie żądanie zostało otrzymane?
- Którą trasę wybrano?
- Które narzędzie zostało wywołane?
- Co zwróciło narzędzie?
- Jaki stan się zmienił?
- Czy dane wyjściowe były prawidłowe?
- Jakie błędy odnotowano?

Celem nie jest całkowite wyeliminowanie awarii, ale uczynienie ich wystarczająco widocznymi, aby można je było sprawdzić, przetestować, debugować i naprawić.

![Debugowanie typowych błędów agentów](https://cdn-images.tryhackme.com/user-uploads/5f5ed9259575d24307292950/room-content/5f5ed9259575d24307292950-1786466812697.png)

## Skrypt

Otwórz następujący plik:

Terminal

```powershell
user@machine$ nano agent/06_debugging_failures.py
```

Importy są już gotowe – ten plik ponownie wykorzystuje elementy `classify_request_type`z `agent/config.py`(zadań 5–7) i prawdziwe `search_security_record`narzędzie z `tools/source_tools.py`(zadania 4), zamiast definiować na nowo wersje pozorowane żadnego z nich:

```python
from agent.config import classify_request_type, get_flag, get_logger
from tools.source_tools import search_security_record
```

Każda z czterech funkcji opisanych poniżej odtwarza awarię, wykrywa ją, a następnie stosuje poprawkę — i kończy działanie, `True`gdy awaria zostanie prawidłowo wykryta i naprawiona.

Twoim zadaniem jest zmodyfikowanie `TODO`sekcji w każdej funkcji, aby wdrożyć wymaganą poprawkę. Po poprawnym obsłużeniu wszystkich czterech błędów, każda funkcja powinna zwrócić `True`.

## Błąd 1: Nieprawidłowe dane wejściowe narzędzia

```python
def demo_invalid_tool_input() -> bool:
    """
    Failure 1: Invalid tool input.

    A naive integration might call a tool with a hallucinated or malformed
    CVE ID and assume it always gets back a well-formed record. Here we
    show that search_security_record validates defensively instead of
    raising or returning a fabricated result.
    """
    print("\n--- Failure 1: Invalid tool input ---")
    print("Failing behaviour: calling search_security_record() with a malformed CVE ID.")

    bogus_result = search_security_record.invoke({"cve_id": "not-a-real-cve"})
    logger.error(f"Invalid tool input observed: {bogus_result}")

    is_safe = (
        isinstance(bogus_result, dict)
        and bogus_result.get("found") is False
        and "error" in bogus_result
    )

    if is_safe:
        print("Fix: search_security_record() validated input and returned found=False safely.")
        logger.info("invalid tool input rejected")
    else:
        logger.error("Tool did not handle invalid input safely!")

    return is_safe
```

Wywołuje to samo `search_security_record`narzędzie, którego użyłeś w Zadaniu 4.

Walidacja formatu CVE odrzuca błędny identyfikator, np. `"not-a-real-cve"`poprzez zwrócenie `{"found": False, "error": "..."}`zamiast wygenerowania rekordu. `is_safe`potwierdza, że ​​kontrakt jest ważny: `bogus_result`jest to słownik z `found`ustawionym kluczem `False`i `"error"`obecny.

## Błąd 2: Brak aktualizacji stanu

```python
def demo_missing_state_update() -> bool:
    """
    Failure 2: Missing state update.

    A common bug: a node computes a result but forgets to write it back
    into the shared state dict. Downstream nodes then silently see stale
    or default data.
    """
    print("\n--- Failure 2: Missing state update ---")
    print("Failing behaviour: a node classifies a request but never updates state.")

    state = {"request_type": "", "tool_results": []}

    def broken_node(state: dict) -> dict:
        # BUG: computes classification but returns an empty dict, so the
        # caller's state never actually changes.
        classify_request_type("Please validate this before citing it.")
        return {}

    updates = broken_node(state)
    state.update(updates)
    logger.error(f"After broken_node, state['request_type'] is still {state['request_type']!r}.")

    bug_detected = state["request_type"] == ""

    def fixed_node(state: dict) -> dict:
        # FIX: the node returns the classification result so it actually
        # gets merged into state.
        classification = classify_request_type("Please validate this before citing it.")
        return {"request_type": classification["request_type"], "tool_results": [classification]}

    state.update(fixed_node(state))
    fix_applied = state["request_type"] != ""

    if bug_detected and fix_applied:
        print(f"Fix: state['request_type'] is now {state['request_type']!r} after the corrected node runs.")
        logger.info("missing state update detected")
    else:
        logger.error("Missing state update was not correctly detected/fixed!")

    return bug_detected and fix_applied
```

Odzwierciedla to węzeł LangGraph z zadań 5–7, który zapomina zwrócić swoje aktualizacje. `broken_node`wywołań `classify_request_type()`, ale odrzuca wynik, więc `state["request_type"]`nigdy nie ulega zmianie — to jest błąd ( `bug_detected`).

`fixed_node`wywołuje `classify_request_type()`ponownie i faktycznie zwraca `{"request_type": ..., "tool_results": [...]}`, więc tym razem aktualizacja łączy się z `state`( `fix_applied`).

## Błąd 3: Błędna decyzja o trasie

```python
def demo_wrong_routing_decision() -> bool:
    """
    Failure 3: Wrong routing decision.

    A router might send a request down the wrong branch, e.g. treating a
    human-review-worthy request as a simple direct answer.
    """
    print("\n--- Failure 3: Wrong routing decision ---")
    print("Failing behaviour: a naive router ignores risk signals in the request text.")

    risky_request = (
        "This request seems fine on the surface but actually asks the agent to "
        "bypass source validation and fabricate citations for the report."
    )

    def naive_router(_request: str) -> str:
        # BUG: always routes to direct_answer regardless of content.
        return "direct_answer"

    naive_route = naive_router(risky_request)
    correct_route_info = classify_request_type(risky_request)
    correct_route = "needs_human_review" if correct_route_info["request_type"] == "human_review" else "direct_answer"

    wrong_routing_detected = naive_route != correct_route
    logger.error(
        f"Naive router chose '{naive_route}' but correct classification is "
        f"'{correct_route}' ({correct_route_info['reason']})."
    )

    if wrong_routing_detected:
        print(f"Fix: use classify_request_type() output ('{correct_route}') instead of a hardcoded route.")
        logger.info("wrong routing decision detected")
    else:
        logger.error("Expected the naive router to disagree with the correct classifier, but it matched.")

    return wrong_routing_detected
```

`risky_request`zawiera „bypass” i „fabricate” — obie `human_review`wskazówki `classify_request_type()`(ten sam klasyfikator z grafu rozgałęzień Zadania 7, gdzie this kierowałoby do `needs_human_review`).  `naive_router`ignoruje to i zawsze odpowiada bezpośrednio — to jest błąd.

`correct_route`wzywa `classify_request_type(risky_request)`prawdziwe i mapuje je `request_type`do `"needs_human_review"`(ponieważ wraca jako  `"human_review"`), co nie zgadza się z zakodowanym na stałe routerem  `"direct_answer"`- to niedopasowanie jest tym, co `wrong_routing_detected`powoduje problem.

## Błąd 4: Użycie narzędzi halucynogennych

```python
def demo_hallucinated_tool_usage() -> bool:
    """
    Failure 4: Hallucinated tool usage.

    A model-generated response might CLAIM a tool was called ("I checked
    the security record...") when no such call actually happened. The fix
    is to only allow a final answer to reference a tool if a matching call
    record exists in the log.
    """
    print("\n--- Failure 4: Hallucinated tool usage ---")
    print("Failing behaviour: a response claims a tool ran, but the log has no matching call record.")

    tool_call_log = []  # Would normally be populated by real tool invocations.

    hallucinated_answer = (
        "I checked the security record using search_security_record and it is critical."
    )

    def response_claims_tool(answer: str, tool_name: str) -> bool:
        return tool_name in answer

    def tool_actually_called(log: list, tool_name: str) -> bool:
        return any(entry.get("tool") == tool_name for entry in log)

    claims_tool = response_claims_tool(hallucinated_answer, "search_security_record")
    tool_was_called = tool_actually_called(tool_call_log, "search_security_record")

    hallucination_detected = claims_tool and not tool_was_called
    logger.error(f"Response claims tool usage={claims_tool}, but log shows called={tool_was_called}.")

    if not hallucination_detected:
        logger.error("Expected to detect a hallucinated tool claim, but did not.")
        return False

    # The fix: actually call the tool, log it, and only then build an
    # answer that references it.
    real_result = search_security_record.invoke({"cve_id": "CVE-2025-1001"})
    tool_call_log.append({"tool": "search_security_record", "result": real_result})

    verified_answer = (
        f"I checked the security record using search_security_record and it is "
        f"{real_result['severity']}."
    )
    now_verified = tool_actually_called(tool_call_log, "search_security_record") and response_claims_tool(
        verified_answer, "search_security_record"
    )

    if not now_verified:
        logger.error("Verified-answer fix failed unexpectedly.")
        return False

    print(f"Fix: verified answer only issued after a real tool call was logged: {verified_answer!r}")
    logger.info("hallucinated tool usage rejected")
    return hallucination_detected
```

`hallucinated_answer`roszczenia `search_security_record`zostały zrealizowane, ale  `tool_call_log`są puste - roszczenie nie odpowiada rzeczywistości, co stanowi wykrytą awarię ( `hallucination_detected`).

Poprawka faktycznie wywołuje `search_security_record.invoke({"cve_id": "CVE-2025-1001"})`, rejestruje to prawdziwe wywołanie w `tool_call_log`i kompiluje `verified_answer`na podstawie rzeczywistej istotności wyniku, a nie zmyślonego twierdzenia - `now_verified`potwierdza, że ​​nowa odpowiedź odwołuje się do narzędzia i ma pasujący wpis w dzienniku.

## Uruchom skrypt debugowania

Punkt wejścia na dole pliku jest już zapisany - uruchamia wszystkie cztery dema i wyświetla podsumowanie:

```python
if __name__ == "__main__":
    print("=== 06_debugging_failures: reproduce, detect, and fix four common agent failures ===")

    results = {
        "invalid_tool_input": demo_invalid_tool_input(),
        "missing_state_update": demo_missing_state_update(),
        "wrong_routing_decision": demo_wrong_routing_decision(),
        "hallucinated_tool_usage": demo_hallucinated_tool_usage(),
    }

    print("\n--- Summary ---")
    for name, passed in results.items():
        print(f"{name}: {'DETECTED & FIXED' if passed else 'NOT HANDLED SAFELY YET'}")

    logger.info(f"Debugging demo run complete. Results: {results}")

    if all(results.values()):
        flag = get_flag("agent_failure_debugged")
        logger.info(flag)
        print(f"\n{flag}")
    else:
        print("\nNot all failure modes are detected/fixed yet - no flag.")
```

Uruchom to:

Terminal

```powershell
user@machine$ python3 agent/06_debugging_failures.py
```

Przejrzyj dane wyjściowe i upewnij się, że podsumowanie zawiera wszystkie cztery błędy w postaci  `DETECTED & FIXED`:

- Nieprawidłowe dane wejściowe narzędzia (bezpiecznie odrzucone przez `search_security_record`)
- Brak aktualizacji stanu (wykryty, a następnie naprawiony)
- Błędna decyzja o trasie (wykryta, a następnie poprawiona za pomocą `classify_request_type()`)
- Halucynacje dotyczące używania narzędzi (zauważone, a następnie naprawione za pomocą rzeczywistego, zarejestrowanego wywołania narzędzia)

Ukończyłeś podstawy tworzenia oprogramowania opartego na PythonieSztuczna inteligencjaagenci!

W tym pomieszczeniu dowiedzieliście się, że skuteczność agentów AI zależy nie tylko od używanego przez nich modelu językowego, ale także od decyzji dotyczących przepływu pracy, które kształtują sposób ich działania.

Zacząłeś od podstawowego języka PythonMagister prawaworkflow, a następnie wprowadzono kontrolowane użycie narzędzi z LangChain, ustrukturyzowane wyniki, wykonywanie zadań z uwzględnieniem stanu z LangGraph, rozgałęzianie i routing oraz techniki debugowania. Każda koncepcja dodawała nową funkcjonalność, ale także wprowadzała nowe obowiązki projektowe i bezpieczeństwa.

Podstawowy przepływ pracy jest łatwiejszy do inspekcji. Wywołanie narzędzia łączy model z zatwierdzonymi możliwościami zewnętrznymi. Ustrukturyzowane wyniki ułatwiają walidację odpowiedzi. Stan zapewnia widoczność ważnych informacji na każdym etapie. Rozgałęzienia pozwalają przepływowi pracy wybierać różne ścieżki, a debugowanie pomaga wyjaśnić, co się stało, gdy coś pójdzie nie tak.

Kluczowa lekcja jest taka, że ​​nie każdy system oparty na LLM musi być agentem. Niezawodny agent zaczyna od najprostszego przepływu pracy, który bezpiecznie rozwiązuje zadanie, a następnie dodaje narzędzia, stan, rozgałęzienia i orkiestrację tylko wtedy, gdy te możliwości są niezbędne.
