from anvhant import Användarhantering 
from anv import Användare 

# importerar klassen Användarhantering som innehåller alla mina menyvals funktioner som bokstaven "a".

# ANSI escape codes för färg och stil i terminalen
RESET = "\033[0m"
RÖD = "\033[31m"
GRÖN = "\033[32m"
GUL = "\033[33m"
BLÅ = "\033[34m"
LJUSBLÅ = "\033[1;34m"
CYAN = "\033[36m"
FET = "\033[1m"
UNDERSTRUKEN = "\033[4m"
BLINKANDE = "\033[5m"




def meny_innan_inloggning(hantering: Användarhantering) -> bool:
    """
    Meny som visas när användaren inte är inloggad.
    """
    while True: # så länge användaren inte är inloggad så ska denna meny visas.
        print(f"""{CYAN}
┌────────────────────────────────────────────┐
│{RESET}{FET}{GUL}          Välj alternativ:                  {RESET}{CYAN}│
│{RESET}{GUL}   1.Logga in med befintlig användare       {RESET}{CYAN}│
│{RESET}{GUL}   2.Registrera ny användare                {RESET}{CYAN}│
│{RESET}{GUL}   3.Avsluta programmet                     {RESET}{CYAN}│
└────────────────────────────────────────────┘{RESET}
""")


        val: str = input(f"\n{CYAN}❰ ❱{RESET}\b\b") # sparar användarens val i variabeln "val"
        try:
            if val == "1":
                if hantering.logga_in(): # kallar på logga_in funktionen i klassen Användarhantering
                    return True # om inloggningen lyckas så returneras True och menyn efter inloggning visas.
            elif val == "2":
                    hantering.registrera() # kallar på registrera funktionen i klassen Användarhantering
            elif val == "3":
                    print(f"\n{RÖD}Programmet avslutas.{RESET}") 
                    exit() # avslutar programmet
        except ValueError: # om användaren skriver in felaktig inmatning så fås ett felmeddelande.
            print(f"\n{RÖD}Felaktig inmatning, försök igen{RESET}")



def meny_efter_inloggning(hantering: Användarhantering) -> bool:
    """
    Meny som visas när användaren är inloggad.
    """
    while True: # så länge användaren är inloggad så ska denna meny visas.
        print(f"\nInloggad som{FET}{LJUSBLÅ} {hantering.inloggad_anv.namn} {RESET}") # visar vilken användare som är inloggad
        print(f"""{CYAN}
┌────────────────────────────────────────────┐
│{RESET}{FET}{GUL}          Välj alternativ:                  {RESET}{CYAN}│
│{RESET}{GUL}   1. Byt lösenord                          {RESET}{CYAN}│
│{RESET}{GUL}   2. Byt namn                              {RESET}{CYAN}│
│{RESET}{GUL}   3. Byt användare                         {RESET}{CYAN}│
│{RESET}{GUL}   4. Ta bort användare                     {RESET}{CYAN}│
│{RESET}{GUL}   5. Visa användarlista                    {RESET}{CYAN}│
│{RESET}{GUL}   6. Avsluta programmet                    {RESET}{CYAN}│
└────────────────────────────────────────────┘{RESET}
""")

        val: str = input(f"\n{CYAN}❰ ❱{RESET}\b\b") # sparar användarens val i variabeln "val"    
        try:
            if val == "1":  # genererar en ny hash nyckel
                namn: str = input("\nAnge ditt användarnamn: ")
                hantering.byt_lösenord(namn)

            elif val == "2": # byter namn på användaren
                hantering.byt_namn()

            elif val == "3": # byter användare
                print("\nDu är nu utloggad.")
                hantering.logga_händelse(f"{hantering.inloggad_anv.namn} loggade ut.") # loggar händelsen att en användare har loggat ut
                if meny_innan_inloggning(hantering): # kallar på menyn innan inloggning
                    continue
            elif val == "4": # tar bort användare
            
                namn: str = input("\nAnge användarnamn på den användaren du vill ta bort: ")
                borttagen: bool = hantering.ta_bort_anv(namn) # kallar på ta_bort_anv funktionen i klassen Användarhantering
                 # sparar resultatet av borttagningen i variabeln "borttagen
                if borttagen: # endast om borttagningen lyckades
                    
                    if hantering.inloggad_anv and hantering.inloggad_anv.namn == namn:
                        print("\nDu har tagit bort den inloggade användaren, du är nu utloggad.")
                        hantering.inloggad_anv = None
                        if meny_innan_inloggning(hantering): # kallar på menyn innan inloggning
                            continue 
            elif val == "5":
                hantering.lista_användare() # visar alla användare i systemet
            elif val == "6":
                print(f"\n{RÖD}Programmet avslutas.{RESET}")
                hantering.logga_händelse(f"Programmet avslutades av {hantering.inloggad_anv.namn}.") # loggar händelsen att programmet avslutades
                exit() # avslutar programmet
            elif val == "7": # dolt alternativ för att visa loggen, admin log
                hantering.visa_logg() 
        except ValueError: # om användaren skriver in felaktig inmatning så fås ett felmeddelande.
            print("\nFelaktig inmatning, försök igen") 
        
def main() -> None:
    """
    Startar programmet och kallar på menyerna.
    """
    hantering = Användarhantering("anvdata.json") # skapar ett objekt av klassen Användarhantering med filnamnet "anvdata.json"
    if meny_innan_inloggning(hantering):
        meny_efter_inloggning(hantering) # kallar på menyn efter inloggning

        
    

if __name__ == "__main__": # startar programmet
    main() # kallar på main funktionen




    # att göra så du behöver bekräfta lösenord när du byter namn på användare # check
    # finslipa menyer med utseende mässig pimpning
    # type hinta allt # check
    # kommentera allt # check
    # hantera fel bättre 
    # läs in all kod. 
    # läg till datum för skapade användare och skicka logarna till hisotrik.log filen. 
    