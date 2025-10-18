----------------------------------

Inloggningssystem – Individuell inlämningsuppgift

Detta skript är ett användarvänligt inloggningssystem, med fokus på säkerhet, tydlig menystruktur och stabil felhantering. Systemet hanterar registrering, inloggning, användarlistning och radering med verifiering, och loggar viktiga händelser i en lokal historikfil.

----------------------------------------

Instruktioner
- Klona repot
- skriv: git clone https://github.com/ikarosbernardini/Individuell-uppgift.git i din terminal. 
- skriv sedan: cd Individuell-uppgift
- Kör skriptet:
python main.py eller python3 main.py beroende på ditt operativsystem


----------------------------------------

Funktioner
- Registrera nya användare med lösenord (hashas säkert)
- Logga in med verifiering mot sparad data i .json filen
- Byt lösenord med bekräftelse av nuvarande lösenord
- Byt användarnamn med lösenordsverifiering och koll mot namnkonflikter(upptagna namn)
- Radera användare (med lösenordsverifiering och bekräftelse)
- Automatisk utloggning om aktuell användare tas bort
- Lista alla registrerade användare
- Tydlig menystruktur med validering och återkoppling
- "Tryck Enter för att fortsätta"-flöde för bättre användarupplevelse
- Loggning av alla viktiga händelser i historik.log (registrering, inloggning, borttagning, misslyckade försök)
- Dold adminfunktion: menyval 7 visar hela logghistoriken
- Färgglad och stilren terminal "look" med Unicode symboler och ANSI färgkoder
- Stabilare felhantering för tomma fält, ogiltiga val, filfel


----------------------------------------

Moduler och språk
- Språk: Python
- Moduler: hashlib,datetime,json
- Loggfil: historik.log


----------------------------------------

Källor
- COPILOT 
- Stackoverflow
- Python book - Automate the boring stuff :  
https://automatetheboringstuff.com/#toc
- Python imports : 
https://docs.python.org/3/library/hashlib.html

https://docs.python.org/3/library/datetime.html

https://docs.python.org/3/library/json.html

-Unicode tecken table :
https://symbl.cc/en/unicode-table/#spacing-modifier-letters

-ANSI escape codes table : 
https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007

----------------------------------------

Framtids planer för detta skript.

1. Byta .json hanteringen mot en SQLDatabas
2. Kasta in skriptet i en container via podman och ha det aktivt körandes på en lokalport.
3. connecta skriptet med en API och dra upp mot en server så loggningar och liknande blir mer än bara lokala loggningar.
4. lär dig etrinket och skapa en interaktiv gui.
5. lägg även till en authticator och förbättra säkerheten ännu mer.
6. Skapa flera meny val, 1 för profil hantering meny, 2. för container status och log meny, 3. server stauts meny osv osv 




Skapat av Ikaros Bernardini

