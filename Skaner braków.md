```dataviewjs
// Precyzyjne wskazanie Twoich plików na bazie wygenerowanej listy
let nBase = dv.page("lista");
let nMoc = dv.page("MOC Cyberbezpieczeństwo THM");

if (!nBase || !nMoc) {
    dv.paragraph("❌ Błąd techniczny: Sprawdź, czy pliki na pewno są w głównym folderze.");
} else {
    // Pobranie wszystkich linków z notatki "lista"
    let baseLinks = nBase.file.outlinks.map(l => l.path);
    // Pobranie wszystkich linków z notatki "MOC Cyberbezpieczeństwo THM"
    let mocLinks = new Set(nMoc.file.outlinks.map(l => l.path));
    
    // Filtrowanie - zostają tylko te, których brakuje w MOC
    let missing = baseLinks.filter(l => !mocLinks.has(l));
    
    dv.header(3, "🔍 Brakujące notatki z THM (" + missing.length + "):");
    if (missing.length === 0) {
        dv.paragraph("🎉 Sukces! Wszystkie notatki z pliku 'lista' znajdują się już w Twoim MOC!");
    } else {
        dv.list(missing.map(l => dv.fileLink(l)));
    }
}
```
