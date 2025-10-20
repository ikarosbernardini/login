import os
import sqlite3

# ANSI-färger för CLI-feedback
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def get_db_path():
    """Returnerar absolut sökväg till anvdata.db"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "data", "anvdata.db")

def migrate_users_table(cursor):
    """Lägger till saknade kolumner i users-tabellen"""
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]

    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        print(f"{YELLOW}[~] Kolumn 'password_hash' tillagd i users-tabellen{RESET}")

def init_db():
    """Skapar databasen och tabeller om de inte finns"""
    try:
        db_path = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Skapa användartabell
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Kör migrationskontroll
        migrate_users_table(cursor)

        # Skapa historiklogg
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)


        conn.commit()
        conn.close()
        print(f"{GREEN}[✓] Databasen initierad: {db_path}{RESET}")

    except Exception as e:
        print(f"{RED}[X] Fel vid databasinitiering: {e}{RESET}")
