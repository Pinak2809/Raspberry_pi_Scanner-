import sqlite3
import datetime

def create_database():
    conn = sqlite3.connect('Accounter.db')
    c = conn.cursor()

    # Create Artikel
    c.execute('''
        CREATE TABLE Artikel (
            ArtID INTEGER PRIMARY KEY, 
            ArtName  TEXT, 
            barcode TEXT  UNIQUE, 
            Anzahllager  INTEGER,
            buying_price REAL,
            PreisProTag  REAL,
            PreisGesamt REAL,
            AblaufsDatum TEXT,
            Image TEXT,
            NaechstePruefDatum TEXT,
            BestandLimit REAL,
            Ausleihbar INTEGER DEFAULT 0,
            LagerPlatz TEXT
        )
    ''')



    # Create Benutzer
    c.execute('''
        CREATE TABLE Benutzer (
            BenId INTEGER PRIMARY KEY, 
            Benutzername TEXT,
            Passwort TEXT
        )
    ''')

    # Create Ausleihe
    c.execute('''
        CREATE TABLE Ausleihe (
            AusleiheID INTEGER PRIMARY KEY,
            ArtID INTEGER,
            BenId INTEGER,
            ArtName TEXT,
            AusleiheDatum TEXT,
            AbgabeFrist TEXT,
            ArtAnzahl INTEGER,
            Pfand TEXT,
            FOREIGN KEY (ArtID) REFERENCES Artikel (ArtID),
            FOREIGN KEY (BenId) REFERENCES Benutzer (BenId)
        )
    ''')

    # Create Defekt
    c.execute('''
        CREATE TABLE Defekt (
            DefektID INTEGER PRIMARY KEY,
            ArtID INTEGER,
            Anmerkung TEXT, 
            Anzahl REAL,
            ArtName TEXT,
            FOREIGN KEY (ArtID) REFERENCES Artikel (ArtID)
        )
    ''')

     # Create Einkauf
    c.execute('''
        CREATE TABLE Einkauf (
            BestellID INTEGER PRIMARY KEY,
            ArtID INTEGER,
            BestellDatum  TEXT, 
            BestellAnzahl  REAL,
            Anmerkung TEXT,
            FOREIGN KEY (ArtID) REFERENCES Artikel (ArtID)
        )
    ''')

    # Create Kunde
    c.execute('''
        CREATE TABLE Kunde (
            KundID INTEGER PRIMARY KEY,
            KundName TEXT, 
            Matrik TEXT,
            Email TEXT,
            Vermerk TEXT
        )
    ''')

    print("Database and tables created successfully.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()


