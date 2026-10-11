---

Rejestrowanie służy do zapewnienia „źródła prawdy” dla aktywności zachodzącej w sieci. Rejestrowanie jest najczęściej wykorzystywane, ale nie tylko, do reagowania na incydenty i monitorowania bezpieczeństwa. W trakcie procesu reagowania na incydenty użytkownik może zostać pociągnięty do odpowiedzialności za działanie lub zachowanie, a rejestrowanie odgrywa kluczową rolę w udowodnieniu działań użytkownika.

Odpowiedzialność jest ostatnim filarem identyfikacji, uwierzytelniania, autoryzacji i odpowiedzialności (IAAA) Model. Model ten służy ochronie i zachowaniu poufności,uczciwośći dostępności informacji.

Odpowiedzialność nakłada na użytkowników i uczestników sieci odpowiedzialność za swoje działania. Rejestrowanie stanowi istotną część tego filaru i służy do rejestrowania aktywności.

Aby zapewnić skuteczność rozliczalności, dzienniki i inne źródła danych muszą być chronione, a ich autentyczność musi zostać udowodniona. Jeśli nie da się udowodnić, że dziennik był przechowywany w oryginalnym stanie, traci on swoją ważność.uczciwośćw celu zapewnienia odpowiedzialności i procesu reagowania na incydenty.

### Cele edukacyjne

- Dowiedz się, skąd pochodzą dane, jak są przechowywane i jak inżynier ds. bezpieczeństwa może je wykorzystać.
- Dowiedz się, dlaczego rozliczalność ma duże znaczenie dla bezpieczeństwa i w jaki sposób rejestrowanie danych może pomóc w zwiększeniu jego skuteczności.
- Zastosuj dzienniki i inne źródła danych do reagowania na incydenty i zasady odpowiedzialności.

Przed rozpoczęciem tej sali zalecamy zapoznanie się z możliwościami rejestrowania i źródłami danych lub ukończenie  [kursu „Wprowadzenie do rejestrowania”](https://tryhackme.com/room/introtologs) . Zalecamy również podstawową wiedzę na tematSplunklub kompletne[SplunkPodstawy](https://tryhackme.com/room/splunk101) .

W tej sali przedstawimy, jak rejestrowanie i gromadzenie danych wpływa na rozliczalność. Przedstawimy najlepsze praktyki i wyjaśnimy rozliczalność na różnych etapach procedury reagowania na incydenty.

Rejestrowanie wspomaga każdego członka zaangażowanego w proces reagowania na incydenty. W zależności od źródła rejestrowania, może ono zapewniać różne korzyści lub wgląd w sieć lub urządzenie. Oto kilka przykładów:

- Pliki zostały utworzone.
- E-maile wysłane.
- Inne TTP (taktyki, techniki i procedury) określone przez [MITRAStruktura ATT&CK(otwiera się w nowej karcie)](https://attack.mitre.org/).

Ponieważ logi odgrywają istotną rolę w reagowaniu na incydenty, muszą być autentyczne i, po analizie, identyczne z tymi, które zostały wygenerowane.

Dodanie odpowiedzialności do procesu reagowania na incydenty. Gdy źródła logów są wiarygodne i wiarygodne, użytkownik może zostać pociągnięty do odpowiedzialności za swoje działania, co jest udowodnione w logach.

To zastosowanie odpowiedzialności jest bardziej formalnie znane jako niezaprzeczalność i przyczynia się do wielu modeli zagrożeń, takich jak [KROKmodel(otwiera się w nowej karcie)](https://www.microsoft.com/en-us/security/blog/2007/09/11/stride-chart/)Niezaprzeczalność oznacza, że ​​osoba fizyczna nie może zakwestionować podjętej czynności, w przeciwieństwie do niezaprzeczalności, kiedy osoba fizyczna kwestionuje daną czynność.

### Zarządzanie informacjami i zdarzeniami bezpieczeństwa

System  **zarządzania** **informacjami** i  zdarzeniami  **bezpieczeństwa** **(**​ **​**​ **SIEM)**  to narzędzie służące do gromadzenia, indeksowania i wyszukiwania danych z różnych punktów końcowych i lokalizacji sieciowych. Chociaż ta sala nie będzie obejmować dogłębnej analizy logów i systemów SIEM, ważne jest, aby zbudować podstawowy poziom zrozumienia. WykorzystamySIEMw późniejszych zadaniach, aby zapoznać się w praktyce z koncepcjami zaprezentowanymi w tej sali.

Systemy SIEM oferują wiele funkcji i możliwości, często przeznaczonych do konkretnych zastosowań. Poniżej znajduje się podsumowanie korzyści i funkcji, jakie oferuje system SIEM.SIEMmoże zaoferować na najbardziej podstawowym poziomie:

- Pobieranie logów w czasie rzeczywistym.
- Ostrzeganie przed działaniami odbiegającymi od normy.
- Monitoring i widoczność 24/7.
- Analizowanie i wizualizacja danych.
- Zdolność do badania przeszłych incydentów.

Przykłady systemów SIEM mogą obejmować:Wazuh,Splunk,JELEŃ KANADYJSKIi QRadar. Więcej informacji znajdziesz w sekcji [Audyt i monitorowanie](https://tryhackme.com/room/auditingandmonitoringse) .

Mimo że w tym pokoju nie będziemy poruszać szczegółów dotyczących analizy logów ani systemów SIEM, ważne jest, aby osiągnąć podstawowy poziom zrozumienia.

Systemy SIEM są zazwyczaj projektowane z trzema komponentami używanymi do wyszukiwania, indeksowanie i równoważenia obciążenia; komponenty te są powszechnie znane odpowiednio jako **głowica wyszukiwania** , **indeksator** i **przekierowywanie** .

W tym pomieszczeniu naszym celem jest odpowiedzialność, dlatego skupimy się głównie na indeksatorze i sposobie, w jaki dane docierają z urządzenia do indeksatora. Proces ten jest powszechnie znany jako **pobieranie danych** .

- Rodzaje pozyskiwania danych
    - Agent/spedytor
    - Przekierowanie portów
    - Dziennik systemowy
    - Wgrywać

Chociaż istnieje wiele sposobów pobierania danych, to sposobów ich przechowywania jest zazwyczaj mniej. Chociaż głównym punktem odniesienia w kwestii rozliczalności jest pobieranie danych, ich przechowywanie może być równie trudne.

W przypadku problemów z przechowywaniem danych często nie powinniśmy martwić się o atakujących, ale o usterki techniczne, na przykład przypadkowe usunięcie indeksu lub uszkodzenie urządzenia pamięci masowej.

Oto kilka przykładów kwestii, które należy wziąć pod uwagę podczas projektowania rozwiązania do przechowywania danych dla źródeł logów. Chociaż zachowanie autentyczności i bezpieczeństwa tych danych jest ważne dla zapewnienia rozliczalności, często nakłada się to na kwestie zgodności. Zgodność i przepisy idą w parze; jednym z takich przepisów może być wymóg archiwizacji lub przechowywania danych logów przez określony czas. To ponownie wpływa na rozliczalność, gdzie w celu zapewnienia zgodności należy zastosować zasadę niezaprzeczalności dla źródła logów. Na przykład, audyt wymaga danych z ostatnich sześciu miesięcy z X źródeł logów. Jako interesariusz musisz zagwarantować, że te źródła logów odzwierciedlają aktywność sieci.

Jednym z rozwiązań problemu przechowywania danych jest tzw. cold storage. Cold storage to proces lub standard przechowywania danych, który można streścić jako optymalne przechowywanie dużej ilości danych.

Dostęp do pamięci masowej typu cold storage jest rzadki i dlatego nie wymaga urządzeń pamięci masowej o wysokiej wydajności. Przykładami pamięci masowej typu cold storage mogą być niedrogie dyski twarde, a nawet napędy taśmowe! Z kolei pamięć masowa typu hot storage to częsty dostęp do danych, który wymaga wyższej wydajności. Może ona obejmować dyski SSD, a w niektórych przypadkach dyski twarde o wysokiej wydajności. W całym cyklu życia danych mogą występować inne poziomy dostępu i wydajności, które można określić mianem pamięci masowej typu warm storage. 

Standard określający, jak długo dane pozostają w każdej fazie, będzie zależał od wymogów regulacyjnych i wytycznych firmy. Przykładem procesu przechowywania może być przechowywanie danych w trybie gorącym przez sześć miesięcy, w trybie ciepłym przez trzy miesiące i w trybie zimnym przez trzy lata. W zależności od rodzaju danych, mogą one być przechowywane w trybie zimnym bezterminowo.

Standard bezpieczeństwa danych branży kart płatniczych (PCI DSS) to przykład normy, która wymaga przechowywania dzienników audytu przez rok i umożliwienia natychmiastowego dostępu do nich przez 90 dni w celu zachowania zgodności.

Teraz, gdy rozwiązano pewne problemy związane ze sposobem przesyłania danych do indeksatora, SIEM Rozwiązaniem jest zastanowienie się nad tym, co stanowi dobry dziennik.

Podczas gdy SIEM zapewnia doskonałą funkcjonalność, jego celem jest pozyskiwanie dowolnych danych i zapewnienie skutecznego i łatwego sposobu ich indeksowania i przeszukiwania.

Jeśli w dzienniku nie ma informacji wymaganych do przeprowadzenia dochodzenia, nie można na jego podstawie ustalić odpowiedzialności i nie jest on podstawą do uznania niezaprzeczalności.

Istnieje wiele źródeł logów, które pozwalają na efektywne gromadzenie danych z jak największą ilością istotnych informacji. W tym zadaniu przedstawimy kilka najpopularniejszych źródeł logów i sposoby ich wykorzystania w procesie reagowania na incydenty.

- Ręczne źródła dzienników
    - Każdy dziennik napisany ręcznie lub sporządzony przez autora
    - Dzienniki zmian
- Zautomatyzowane źródła dzienników
    - Wszelkie logi generowane automatycznie domyślnie, na przykład konfiguracja, narzędzie lub programista
    - Dzienniki systemowe
    - Dzienniki aplikacji
- Inne rodzaje dzienników
    - Niektóre dzienniki mogą nie być kategoryzowane, ale często są wymagane do zachowania zgodności
    - Dzienniki e-mail
    - Wiadomości lub inna komunikacja

Dobre źródło logów może nie obejmować tylko jednego. Ze względu na charakter sieci, utworzenie jednego, wysokiej jakości źródła logów może wymagać wielu typów logów, na przykład…zapora sieciowa Dziennik i dziennik systemowy służą razem do wzajemnego rozliczania. Oznacza to, że ważność jednego dziennika można udowodnić za pomocą innego i odwrotnie.

Źródło dziennika może również gromadzić zbyt dużo informacji; oznacza to, że jeśli kilka typów dzienników gromadzi te same dane lub generuje te same alerty, może to spowodować wzrost szumu, złożoności przechowywania i inne konsekwencje.

Istnieje wiele typów systemów SIEM do wyboru, a każda funkcja i możliwości mogą wpływać na efektywne wykorzystanie logów. Jeśli nie korzystasz z konkretnej funkcji systemu,SIEMNie oznacza to, że nie korzystasz efektywnie z logów, ponieważ zależy to od źródeł logów i wymagań dotyczących użytkowania. Na przykład, jeśli używasz logów jedynie jako narzędzia reagowania na incydenty, a nie do monitorowania w czasie rzeczywistym, funkcja monitorowania w czasie rzeczywistym w niektórych systemach SIEM może nie być potrzebna lub nie być wykorzystywana.

Jak pokrótce przedstawiono w zadaniu czwartym, korzystanie z wielu typów i źródeł logów jest korzystne dla walidacji logów i tworzenia kompletnej historii incydentu. Koncepcja ta jest bardziej formalnie znana jako **korelacja** lub budowanie relacji między dwoma elementami: logami i danymi. Na przykład, jeśli użytkownik wykonał podejrzaną czynność (utworzył Biblioteka DLL Plik na dysku), dziennik aplikacji przeglądarki może posłużyć do powiązania historii wyszukiwania w przeglądarce z zachowaniem. Jeśli szukali konkretnego instalatora lub procesu rozwiązywania problemów, może to wyjaśniać podejrzane działanie. Jeśli dzienniki e-mail wskazywały na potencjalny phishing Próba ta może być poprzedzona podejrzaną akcją, co może skutkować dalszym dochodzeniem. Wzbogacanie danych można również uwzględnić w działaniach korelacyjnych.
