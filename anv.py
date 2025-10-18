import json



class Användare:
    """
    Skapat en klass som representera varje enskild användare och dessa innehåll
    """

    def __init__(self, namn: str, lösenord_hash: str): # initierar klassen med namn och lösenord_hash
        self.namn: str = namn
        self.lösenord_hash: str = lösenord_hash
        self.felaktiga_försök: int = 3

    

    def till_dict(self) -> dict:
        """
        Gör om användaren som en dict för att kunna spara den i .json filen.
        """
        return {"namn": self.namn, "lösenord_hash": self.lösenord_hash} # returnerar en dict med namn och lösenord_hash
