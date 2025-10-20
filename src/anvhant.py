from anv import Användare as A # importerar klassen Användare från anv.py
from datetime import datetime # importerar datetime för att kunna logga tidpunkter
import bcrypt
import sqlite3

# ANSI escape codes för färg och stil i terminalen
RESET = "\033[0m"
RÖD = "\033[31m"
GRÖN = "\033[32m"
GUL = "\033[33m"
LJUSBLÅ = "\033[1;34m"
CYAN = "\033[36m"
FET = "\033[1m"
UNDERSTRUKEN = "\033[4m"

class Användarhantering:
    """
    Hanterar alla olika funktioner vid inlogging eller registering av användare.
    Lagrar alla användare och historik i en .json fil.
    """
    användare: list = [] # lista som håller alla användare

    def hasha_lösenord(self, lösenord: str ):  # konverterar inmatningen av lösenord till ett hashat lösenord
        """
        Tar de inmatade lösenordet och retunerar dess krypterade värde.
        """
        return bcrypt.hashpw(lösenord.encode("utf-8"), bcrypt.gensalt()) # hashar lösenordet så att det inte sparas i klartext. med andra ord krypterar lösenordet.
    

    def återgå(self) -> None:
        """
        En funktion för att återgå till menyn efter att en åtgärd är utförd, gjord för att slippa spamma koden med samma rad.
        """
        input(f"Tryck på {GRÖN}{FET}Enter{RESET} för att återgå till menyn.") # pausar programmet tills användaren trycker på Enter.

    def läs_in_användare(self) -> dict:
        """ "
        Läser in användarna från filen och retunerar dem som en dict så att tidigare data
        är sparad och kan användas igen.
        """
        try: # try & except för att hantera om filen inte finns.
            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
            c = conn.cursor()
            c.execute("SELECT username, password_hash FROM users") # hämtar alla användare
            rader = c.fetchall() # hämtar alla rader från resultatet
            conn.close() # stänger anslutningen till databasen
            return [A(namn=namn, lösenord_hash=lösenord_hash) for namn, lösenord_hash in rader] # retunerar en lista med användare som Användare objekt
        except sqlite3.Error as e:
            print(f"\nKunde inte läsa in användare: {e}") # felmeddelande om filen inte finns
            return []
    def logga_händelse(self, händelse: str, användarnamn: str = "okänd"):
        tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("data/anvdata.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO history (username, action, timestamp) VALUES (?, ?, ?)",
            (användarnamn, händelse, tid)
        )

        conn.commit()
        conn.close()


    def visa_logg(self) -> None:
        """
        Visar innehållet i loggfilen i terminalen, denna funktion är för administratörer.
        """
        try:
            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
            c = conn.cursor()
            c.execute("SELECT tid, användarnamn, händelse FROM history ORDER BY tid DESC") # hämtar alla händelser sorterade efter tid
            rader = c.fetchall() # hämtar alla rader från resultatet
            conn.close() # stänger anslutningen till databasen

            print(f"\n{FET}{UNDERSTRUKEN}Loggfilens innehåll:{RESET}\n")
            if rader:
                for tid, användare, händelse in rader:
                    visningsnamn = användare if användare else "okänd"
                    print(f"[{tid}] ({visningsnamn}) {händelse}")
        except sqlite3.Error as e:
            print(f"\nKunde inte läsa logg: {e}") # felmeddelande om loggningen misslyckas
        self.återgå() # pausar programmet tills användaren trycker på Enter.
        
    def spara_användare(self): 
        """
        Sparar nuvarande användarlista till filen så att data inte försvinner när programmet avslutas.
        """
        try:
            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
            c = conn.cursor()

            for anv in self.användare:
                c.execute("INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)", (anv.namn, anv.lösenord_hash))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"\nKunde inte spara användare: {e}")



    def registrera(self) -> bool:  # start metod för att låta användaren registera en ny obentlig användare.
        """
        Registerar ny användare och sparar användarens uppgifter i databasen.
        """
        namn: str = input("Nytt användarnamn: ").strip() # tar bort eventuella extra mellanslag runt användarnamnet.
        lösenord: str = input("Nytt lösenord: ").strip() # tar bort eventuella extra mellanslag runt lösenordet.

        conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (namn,))
        if c.fetchone(): # om användarnamnet redan finns i systemet så får användaren ett felmeddelande.
            print("\nAnvändarnamnet finns redan.")
            self.logga_händelse(f"Registrering misslyckades, {namn} var upptaget.") # loggar händelsen att en användare försökte registera sig med ett redan upptaget namn
            conn.close()
            return False
        lösenord_hash = self.hasha_lösenord(lösenord)
        tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)", (namn, lösenord_hash, tid))
        conn.commit()
        conn.close()
        
        self.logga_händelse(f"Ny användare registrerad: {namn}") # loggar händelsen att en ny användare har registrerats
        print("\nAnvändare registerad.") # bekräftelse till användaren att registreringen lyckades.
        return True

    def byt_lösenord(self,användarnamn: str):
        """
        En funktion för att byta lösenord för en befintlig användare.
        """
    
        nuv_lös = input("Ange nuvarande lösenord: ").strip()
        try:
            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
            c = conn.cursor()
            c.execute("SELECT password_hash FROM users WHERE username = ?", (användarnamn,))
            resultat = c.fetchone()
            if resultat:
                sparat_lösen_hash = resultat[0]
                if bcrypt.checkpw(nuv_lös.encode("utf-8"), sparat_lösen_hash): # om lösenordet stämmer så körs koden vidare till nedan.
                    nytt_lös = input("Ange nytt lösenord: ").strip()
                    nytt_lös_hash = self.hasha_lösenord(nytt_lös)
                    c.execute("UPDATE users SET password_hash = ? WHERE username = ?", (nytt_lös_hash, användarnamn))
                    conn.commit()
                    conn.close()
                    self.logga_händelse(f"Lösenord ändrat för användare: {användarnamn}") # loggar händelsen att en användare har bytt lösenord
                    print(f"\nLösenordet för användaren {användarnamn} {GRÖN}{FET}uppdaterades{RESET}.") # bekräftelse till användaren att lösenordsbytet lyckades.
                    self.återgå() # pausar programmet tills användaren trycker på Enter.
                    return
                
            else:
                print("\nAnvändaren hittades inte.")
                self.logga_händelse(f"Lösenordsbyte misslyckades för {användarnamn}, användaren hittades inte.")
                conn.close()
                self.återgå()
                return
        except sqlite3.Error as e:
            print(f"\nKunde inte spara användare: {e}")
            self.logga_händelse(f"Fel vid sparande av användare: {e}")
            self.återgå() # pausar programmet tills användaren trycker på Enter.

    def byt_namn(self):
        """
        En funktion för att byta namn på en befintlig användare.
        """
        nuv_namn = input("Ange nuvarande användarnamn: ").strip()

        lösen: str = input("Ange lösenord för att bekräfta namnbytet: ").strip()
        # Försöker hitta användaren med det nuvarande namnet
        conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (nuv_namn,))
        resultat = c.fetchone()

        if resultat:

            sparat_hash = resultat[0]
            if not bcrypt.checkpw(lösen.encode("utf-8"), sparat_hash):
                print("\nFelaktigt lösenord.")
                self.logga_händelse(f"Namnbyte {RÖD}{FET}misslyckades{RESET} för {nuv_namn}, felaktigt lösenord.") # loggar händelsen att en användare försökte
                conn.close()
                self.återgå()
                return
            nytt_namn = input("Ange nytt användarnamn: ").strip()
            c.execute("SELECT * FROM users WHERE username = ?", (nytt_namn,))
            if c.fetchone(): # om det nya användarnamnet redan finns i systemet så får användaren ett felmeddelande.
                print("\nDet nya användarnamnet är redan upptaget.")
                self.logga_händelse(f"Namnbyte {RÖD}{FET}misslyckades{RESET} för {nuv_namn}, {nytt_namn} var upptaget.") # loggar händelsen att en användare försökte
                conn.close()
                self.återgå()
                return
            c.execute("UPDATE users SET username = ? WHERE username = ?", (nytt_namn, nuv_namn))
            conn.commit()
            conn.close()
            self.logga_händelse(f"Namn ändrat från {nuv_namn} till {nytt_namn}") # loggar händelsen att en användare har bytt namn
            print(f"\nAnvändarnamnet har ändrats från {FET}{LJUSBLÅ}{nuv_namn}{RESET} till {FET}{GRÖN}{nytt_namn}{RESET}.") # bekräftelse till användaren att namnbytet lyckades.
            self.återgå() # pausar programmet tills användaren trycker på Enter.
            return
        print("\nAnvändaren hittades inte.")
        self.återgå()

    def logga_in(self ) -> bool: # start metoden för att låta användaren logga in med en befintlig användare.
        """
        Inloggingsmetod för användare som redan har ett konto sparat i databasen.
        """
        while self.felaktiga_försök > 0: # så länge användaren har försök kvar att logga in.
            print(f"\nSkriv {RÖD}'avbryt'{RESET} som användarnamn för att avbryta inloggningen.")
            namn: str = input("Användarnamn:").strip() # tar bort eventuella extra mellanslag runt användarnamnet.
            if namn.lower() == "avbryt": # om användaren skriver in 'avbryt' så avbryts inloggningen och användaren återgår till menyn.
                print(f"\nÅtervänder till {UNDERSTRUKEN}{CYAN}huvudmenyn{RESET}...")
                return False
            lösenord: str = input("Lösenord:").strip()

            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen

            c = conn.cursor()
            c.execute("SELECT password_hash FROM users WHERE username = ?", (namn,))
            resultat = c.fetchone()
            conn.close()

            if resultat:
                sparat_hash = resultat[0]
                if bcrypt.checkpw(lösenord.encode("utf-8"), sparat_hash):# om både användarnamnet och lösenordet stämmer så loggas användaren in. 
                    for anv in self.användare:
                        if anv.namn == namn:
                            self.inloggad_anv = anv # håller reda på vilken användare som är inloggad.
                            self.logga_händelse(f"Användare inloggad: {namn}") # loggar händelsen att en användare har loggats in 
                            return True
          # Om inloggingen misslyckas
            else:
                self.felaktiga_försök -= 1 # minskar antalet försök med 1 vid varje felaktig inloggning.
                if self.felaktiga_försök == 0:
                    print(f"\n{RÖD} För många felaktiga försök. Programmet avslutas.{RESET}") # felmeddelande om användaren har gjort för många felaktiga försök.
                    exit()
                else:
                    print(
                        f"\nFelaktigt användarnamn eller lösenord. Du har {RÖD} {self.felaktiga_försök} {RESET} försök kvar, Försök igen") # informerar användaren hur många försök den har kvar.
                    
                    

    

    def ta_bort_anv(self, användarnamn: str) -> bool: 
        """
        En funktion för att ta bort befintliga användare ur databasen.
        """

        lösen: str = input(f"Ange lösenord för {användarnamn} för att ta bort användaren: ").strip()

        conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (användarnamn,))
        resultat = c.fetchone()

        if resultat:

            sparat_hash = resultat[0]
            if bcrypt.checkpw(lösen.encode("utf-8"), sparat_hash):
                bekräfta: str = input(f"\nÄr du säker på att du vill ta bort användaren {användarnamn}? (ja/nej): ").lower() # ber användaren att bekräfta borttagningen.
                if bekräfta == "ja": # om användaren bekräftar borttagningen så tas användaren bort.
                    c.execute("DELETE FROM users WHERE username = ?", (användarnamn,))
                    conn.commit()
                    conn.close()
                    self.logga_händelse(f"Användare borttagen: {användarnamn}") # loggar händelsen att en användare har tagits bort
                    print(f"Användaren{FET}{LJUSBLÅ} {användarnamn} {RESET}är{FET}{RÖD} BORTTAGEN. {RESET}") # bekräftelse till användaren att borttagningen lyckades.
                    self.återgå() # pausar programmet tills användaren trycker på Enter.
                    return True
                elif bekräfta == "nej":
                    self.logga_händelse(f"Borttagning av användare avbröts: {användarnamn}") # loggar händelsen att borttagningen av en användare avbröts.
                    print("\nÅtgärden avbröts.") # om användaren inte bekräftar borttagningen så avbryts åtgärden.
                    self.återgå()
                    return False
            else:
                print("\nFelaktigt lösenord.")
                self.återgå()
                return False
        else:
            print("\nAnvändaren hittades inte.")
            self.återgå()
            return False

    def lista_användare(self) -> None:
        """
        En funktion som visar alla registerade användare i databasen.
        """
        print("\nRegisterade användare:")
        try:
            conn = sqlite3.connect("data/anvdata.db") # ansluter till SQLite databasen
            c = conn.cursor()
            c.execute("SELECT username FROM users") # hämtar alla användarnamn
            rader = c.fetchall() # hämtar alla rader från resultatet
            conn.close() # stänger anslutningen till databasen

            if rader:
                for (namn,) in rader:
                    print(f"- {LJUSBLÅ} {namn} {RESET}") # skriver ut användarnamnet
            else:
                print("Inga användare registerade.")
        except sqlite3.Error as e:
            print(f"\nKunde inte läsa användare: {e}") # felmeddelande om läsningen misslyckas
        self.återgå()

    def __init__(self, filväg: str = "data/anvdata.db") -> None:
        self.filväg: str = filväg
        self.felaktiga_försök: int = 3  # startvärde för antal försök användaren får vid inloggning.
        self.användare: list[A] = self.läs_in_användare()
        self.val: int = 0
        self.inloggad_anv: A | None = None  # håller reda på vilken användare som är inloggad.

if __name__ == "__main__": # testkod för att se att allt fungerar som det ska.
    pass


# Att göra :

# Fixa tillbaka bekräftelse vid borttagning av användare.
# Fixa historikloggnings funktionen får upp "Kunde inte läsa logg: no such column: tidd" vid visning av loggfilen.
# Finslipa koden och kommentera den bättre.
# Snygga upp databas hanteringen.
# Kasta upp allt de här i en container via docker men låt databasen ligga kvar på värdmaskinen.
# Just nu så efter man har registerat användare eller loggat ut så kan man inte logga in igen då man inte känns igen av någon anledning. 
# Quickfix är att starta om programmet efter varje inloggning eller registrering.
