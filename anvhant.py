import json # importerar json för att kunna läsa och skriva till .json filen
import hashlib # importerar hashlib för att kunna hasha lösenord
from anv import Användare as A # importerar klassen Användare från anv.py
from datetime import datetime # importerar datetime för att kunna logga tidpunkter

# ANSI escape codes för färg och stil i terminalen
RESET = "\033[0m"
RÖD = "\033[31m"
GRÖN = "\033[32m"
GUL = "\033[33m"
BLÅ = "\033[34m"
LJUSBLÅ = "\033[1;34m"
LILA = "\033[35m"
CYAN = "\033[36m"
FET = "\033[1m"
UNDERSTRUKEN = "\033[4m"
BLINKANDE = "\033[5m"

class Användarhantering:
    """
    Hanterar alla olika funktioner vid inlogging eller registering av användare.
    Lagrar alla användare och historik i en .json fil.
    """
    användare: list = [] # lista som håller alla användare

    def hasha_lösenord(self, lösenord: str ):  # konverterar inmatningen av lösenord till ett hashat lösenord
        """
        Tar de inmatade lösenordet och retunerar dess hashade värde.
        """
        return hashlib.sha256(lösenord.encode("utf-8")).hexdigest() # hashar lösenordet så att det inte sparas i klartext. med andra ord krypterar lösenordet.
    

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
            with open(self.filväg, "r") as f:  # öppnar filen i läsläge
                innehåll = f.read()  # läser in filens innehåll
                if not innehåll.strip():  # kollar om filen är tom

                    return []
                jsontext = json.loads(innehåll) # läser in filens innehåll och konverterar det till en dict med "json.loads"
                return [A(anv["namn"], anv["lösenord_hash"]) for anv in jsontext] # skapar en lista av Användare objekt från den inlästa json-datan
        except FileNotFoundError: 
            print("\nAnvändaren hittades inte!")  # retunerar ett felmeddelande om filen inte finns.
            return []
        except json.JSONDecodeError:
            print("\nFel vid läsning av användare, filen är korrupt eller tom.")
            return []
    def logga_händelse(self, händelse: str) -> None:
        """
        Loggar händelser med tidsstämpel till min loggfil.
        """
        tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # hämtar nuvarande tid och datum
        rad = f"[{tid}] {händelse}\n" # formaterar raden som ska loggas
        try:
            with open("historik.log", "a") as f: # öppnar loggfilen i tilläggsläge
                f.write(rad) # skriver raden till loggfilen
        except Exception as e:
            print(f"\nKunde inte logga händelse: {e}") # felmeddelande om loggningen misslyckas

    def visa_logg(self) -> None:
        """
        Visar innehållet i loggfilen i terminalen, denna funktion är för administratörer.
        """
        try:
            with open("historik.log", "r") as f: # öppnar loggfilen i läsläge
                innehåll = f.read() # läser in filens innehåll
                print(f"\n{FET}{UNDERSTRUKEN}Loggfilens innehåll:{RESET}") 
                print(innehåll) if innehåll.strip() else print("Ingen historik hittades.") # skriver ut innehållet i loggfilen
        except FileNotFoundError:
            print("\nLoggfilen hittades inte.") # felmeddelande om loggfilen inte finns.
        self.återgå() # pausar programmet tills användaren trycker på Enter.
        
    def spara_användare(self): 
        """
        Sparar nuvarande användarlista till .json filen.
        """
        try:
            dict_lista = [anv.till_dict() for anv in self.användare] # skapar en lista av dicts från self.användare med hjälp av metoden till_dict i klassen Användare i anv.py
             # sparar användarlistan i .json filen
            with open(self.filväg, "w") as f: 
                #skapa en dict_lista isf self.användare
                json_text = json.dumps(dict_lista) # konverterar listan av dicts till en json-sträng
                f.write(json_text) # skriver json-strängen till filen
        except FileNotFoundError:
            print("\nKunde inte spara användare, Användaren hittades inte!")



    def registrera(self) -> bool:  # start metod för att låta användaren registera en ny obentlig användare.
        """
        Registerar ny användare och sparar användarens uppgifter i .json filen för att låta användaren
        sedan kunna enkelt logga in med sparade uppgifter.
        """
        namn: str = input("Nytt användarnamn: ").strip() # tar bort eventuella extra mellanslag runt användarnamnet.
        lösenord: str = input("Nytt lösenord: ").strip() # tar bort eventuella extra mellanslag runt lösenordet.

        if any(anv.namn == namn for anv in self.användare): # om användarnamnet redan finns i systemet så får användaren ett felmeddelande.
            print("\nAnvändarnamnet finns redan.")
            self.logga_händelse(f"Registrering misslyckades, {namn} var upptaget.") # loggar händelsen att en användare försökte registera sig med ett redan upptaget namn
            return False
        self.användare.append( # om användarnamnet inte finns så skapas en ny användare med hjälp av klassen Användare i anv.py
            A(namn, self.hasha_lösenord(lösenord))
          #  {"namn": namn, "lösenord_hash": self.hasha_lösenord(lösenord)}
          # 
        )
        self.spara_användare() # sparar den nya användaren i .json filen
        self.logga_händelse(f"Ny användare registrerad: {namn}") # loggar händelsen att en ny användare har registrerats
        print("\nAnvändare registerad.") # bekräftelse till användaren att registreringen lyckades.
        return True

    def byt_lösenord(self, användarnamn: str):
        """
        En funktion för att byta lösenord för en befintlig användare.
        """
        for anv in self.användare: # loopar igenom alla användare i systemet
            if anv.namn == användarnamn: # om användarnamnet matchar den inmatade användaren
                nuv_lös = input("Ange nuvarande lösenord: ")
                if anv.lösenord_hash == self.hasha_lösenord(nuv_lös): # om det inmatade lösenordet matchar det sparade lösenordet så körs koden vidare till nedan.
                    nytt_lös = input("Ange nytt lösenord: ").strip() # tar bort eventuella extra mellanslag runt lösenordet.
                    anv.lösenord_hash = self.hasha_lösenord(nytt_lös) # uppdaterar lösenordet med det nya hashade lösenordet.
                    self.spara_användare() # sparar ändringarna i .json filen
                    self.logga_händelse(f"Lösenord ändrat för användare: {användarnamn}") # loggar händelsen att en användare har bytt lösenord
                    print("\nLösenordet är ändrat.") # bekräftelse till användaren att lösenordsbytet lyckades.
                    return
                else:
                    print("\nFelaktigt lösenord.")
                    self.logga_händelse(f"Lösenordsbyte misslyckades för {användarnamn}, felaktigt lösenord inmatat.") # loggar händelsen att en användare försökte byta lösen
                    return
        print("\nAnvändaren hittades inte.")
        self.återgå() # pausar programmet tills användaren trycker på Enter.

    def byt_namn(self):
        """
        En funktion för att byta namn på en befintlig användare.
        """
        nuv_namn = input("Ange nuvarande användarnamn: ")

        # Försöker hitta användaren med det nuvarande namnet

        for anv in self.användare: # för varje användare i listan så kollar vi om användarnamnet matchar den inmatade användaren.
            if anv.namn == nuv_namn: # om användarnamnet matchar den inmatade användaren
                lösen: str = input("Ange lösenord för att bekräfta lösenord: ") # ber användaren att ange lösenordet för att bekräfta namnbytet.
                if anv.lösenord_hash != self.hasha_lösenord(lösen): # om lösenordet INTE stämmer så får användaren ett felmeddelande och funktionen avbryts.
                    print("\nFelaktigt lösenord.")
                    self.logga_händelse(f"Namnbyte {RÖD}{FET}misslyckades{RESET} för {nuv_namn}, felaktigt lösenord.") # loggar händelsen att en användare försökte
                    self.återgå()
                    return
                
                nytt_namn: str = input("\nAnge nytt användarnamn: ").strip() # tar bort eventuella extra mellanslag runt användarnamnet.
                if any(a.namn == nytt_namn for a in self.användare): # kontrollerar om det nya namnet redan finns
                        print("\nAnvändarnamnet är upptaget, vänligen testa med ett annat. ")
                        self.logga_händelse(f"Namnbyte {RÖD}{FET}misslyckades{RESET}, {nytt_namn} var {RÖD}{FET}upptaget{RESET}.") # loggar händelsen att en användare försökte byta namn till ett redan upptaget namn
                        self.återgå()
                        return
                    
                # Uppdatera och spara det nya namnet
                anv.namn = nytt_namn # uppdaterar användarnamnet med det nya namnet.
                self.spara_användare() # sparar ändringarna i .json filen
                self.logga_händelse(f"Användarnamn ändrat från {nuv_namn} till {nytt_namn}") # loggar händelsen att en användare har bytt namn
                print(f"\nAnvändarnamnet {GRÖN}{FET}uppdaterades{RESET} och användare heter numera {LJUSBLÅ} {nytt_namn}.{RESET}") # bekräftelse till användaren att namnbytet lyckades.
                self.återgå()
                return
        print("\nAnvändaren hittades inte.")
        self.återgå()

    def logga_in(self ) -> bool: # start metoden för att låta användaren logga in med en befintlig användare.
        """
        Inloggingsmetod för användare som redan har ett konto sparat i .json filen.
        """
        while self.felaktiga_försök > 0: # så länge användaren har försök kvar att logga in.
            print(f"\nSkriv {RÖD}'avbryt'{RESET} som användarnamn för att avbryta inloggningen.")
            namn: str = input("Användarnamn:").strip() # tar bort eventuella extra mellanslag runt användarnamnet.
            if namn.lower() == "avbryt": # om användaren skriver in 'avbryt' så avbryts inloggningen och användaren återgår till menyn.
                print(f"\nÅtervänder till {UNDERSTRUKEN}{CYAN}huvudmenyn{RESET}...")
                return False
            lösenord: str = input("Lösenord:")
            lösenord_hash: str = self.hasha_lösenord(lösenord) # hashar det inmatade lösenordet för att kunna jämföra med det sparade hashade lösenordet i .json filen.
            for anv in self.användare: # loopar igenom alla användare i systemet
                if anv.namn == namn and anv.lösenord_hash == lösenord_hash: # om både användarnamnet och lösenordet stämmer så loggas användaren in. 
                    self.inloggad_anv = anv # håller reda på vilken användare som är inloggad.
                    self.logga_händelse(f"Användare inloggad: {namn}") # loggar händelsen att en användare har loggats in 
                    return True
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
        En funktion för att ta bort befintliga användare ur .json filen
        """
        for anv in self.användare: # för varje användare i listan så kollar vi om användarnamnet matchar den inmatade användaren.
            if anv.namn == användarnamn: # om användarnamnet matchar den inmatade användaren
                lösen: str = input(f"Ange lösenord för {användarnamn} för att ta bort användaren: ") # ber användaren att ange lösenordet för att bekräfta borttagningen.
                if anv.lösenord_hash == self.hasha_lösenord(lösen): # om lösenordet stämmer så körs koden vidare till nedan. 
                    bekräfta: str = input(f"\nÄr du säker på att du vill ta bort användaren {användarnamn}? (ja/nej): ").lower() # ber användaren att bekräfta borttagningen.
                    if bekräfta == "ja": # om användaren bekräftar borttagningen så tas användaren bort.
                        self.användare = [a for a in self.användare if a.namn != användarnamn] # tar bort användaren från listan och använder "a for a in self.användare" för att skapa en ny lista utan den borttagna användaren.
                        self.spara_användare() # sparar ändringarna i .json filen
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
        print("\nAnvändaren hittades inte.")
        self.återgå()

    def lista_användare(self) -> None:
        """
        En funktion som visar alla registerade användare i systemet.
        """
        print("Registerade användare:")
        for anv in self.användare: # för varje användare i listan så skrivs användarnamnet ut.
            print(f"-{LJUSBLÅ} {anv.namn} {RESET}") # skriver ut användarnamnet
        self.återgå() 

    def __init__(self, filväg: str) -> None:
        self.filväg: str = filväg
        self.felaktiga_försök: bool = 3  # startvärde för antal försök användaren får vid inloggning.
        self.användare: list[A] = self.läs_in_användare()
        self.val: int = 0
        self.inloggad_anv: A | None = None  # håller reda på vilken användare som är inloggad.

if __name__ == "__main__": # testkod för att se att allt fungerar som det ska.
    hantering = Användarhantering("test_användare.json")

    # Registrera en ny användare

    test_anv = A("Kalle", hantering.hasha_lösenord("Telia123"))
    hantering.användare.append(test_anv)
    hantering.spara_användare()

    # Läs in och visa

    hantering.användare = hantering.läs_in_användare()
    for anv in hantering.användare:
        print(f"Användare: {anv.namn}, Lösenord hash: {anv.lösenord_hash}")

    # Testa inlogging
    hantering.spara_användare()
    hantering.logga_in()

