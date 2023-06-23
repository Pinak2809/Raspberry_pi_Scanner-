import sqlite3

def connect_to_database():
    conn = sqlite3.connect('/home/pi/IVDB/inventar.db')
    return conn

def add_product_to_database(conn, ArtID, ArtName, Anzahllager, buying_price, Ausleihbar, AblaufsDatum):
    c = conn.cursor()
    c.execute('INSERT INTO Artikel (ArtID, ArtName, Anzahllager, buying_price, Ausleihbar, AblaufsDatum) VALUES (?, ?, ?, ?, ?, ?)', 
              (ArtID, ArtName, Anzahllager, buying_price, Ausleihbar, AblaufsDatum))
    conn.commit()

def main():
    conn = connect_to_database()

    print("Ready to scan a product...")

    while True:
        ArtID = input("Scan a barcode: ")
        ArtName = input("Enter the product name: ")
        Anzahllager = int(input("Enter the number of available pieces: "))
        buying_price = float(input("Enter the buying price: "))
        Ausleihbar = bool(input("Is the Artikle rentable: "))
        AblaufsDatum = input("what is the expiry date: ")

        add_product_to_database(conn, ArtID, ArtName, Anzahllager, buying_price, Ausleihbar, AblaufsDatum)

        print("Product added to database.")

if __name__ == "__main__":
    main()


