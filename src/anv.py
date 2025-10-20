class Användare:
    """
    Skapat en klass som representera varje enskild användare och dessa innehåll
    """

    def __init__(self, namn: str, lösenord_hash: bytes): # initierar klassen med namn och lösenord_hash
        self.namn: str = namn
        self.lösenord_hash: bytes = lösenord_hash
        self.felaktiga_försök: int = 3

    

    def __str__(self) -> str:
        return f"Användare(namn={self.namn}, lösenord_hash={self.lösenord_hash})"
