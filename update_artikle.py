import sqlite3
import datetime

def connect_to_database():
    conn = sqlite3.connect('/home/pi/IVDB/Accounter.db')
    return conn

def add_product_to_database(conn, ArtID, ArtName, Anzahllager, buying_price, AblaufsDatum, Ausleihbar):
    c = conn.cursor()
    c.execute('INSERT INTO Artikel (ArtID, ArtName, Anzahllager, buying_price, AblaufsDatum, Ausleihbar) VALUES (?, ?, ?, ?, ?, ?)', 
              (ArtID, ArtName, Anzahllager, buying_price, AblaufsDatum, Ausleihbar))
    conn.commit()

def update_product_in_database(conn, ArtID, Anzahllager):
    c = conn.cursor()
    c.execute('UPDATE Artikel SET Anzahllager = ? WHERE ArtID = ?', 
              (Anzahllager, ArtID))
    conn.commit()

def delete_product_in_database(conn, ArtID):
    c = conn.cursor()
    c.execute('DELETE FROM Artikel WHERE ArtID = ?', (ArtID,))
    conn.commit()

def product_exists_in_database(conn, ArtID):
    c = conn.cursor()
    c.execute('SELECT * FROM Artikel WHERE ArtID = ?', (ArtID,))
    return c.fetchone() is not None

def is_rentable(conn, ArtID):
    c = conn.cursor()
    c.execute('SELECT * FROM Artikel WHERE ArtID = ?', (ArtID,))
    product = c.fetchone()
    
    if product[5] == 1:  # Check if the product is rentable.
        return True
    else:
        return False

def is_available(conn, ArtID):
    c = conn.cursor()
    c.execute('SELECT * FROM Artikel WHERE ArtID = ?', (ArtID,))
    product = c.fetchone()

    if product[3] > 0:
        return True
    else:
        return False

def rent_product_in_database(conn, ArtID, ArtAnzahl):
    c = conn.cursor()
    c.execute('UPDATE Artikel SET Anzahllager = Anzahllager - ? WHERE ArtID = ?', 
                  (ArtAnzahl, ArtID))
    conn.commit()   
    print("Product rented. Thank you!")
 

def add_rent_to_database(conn, AusleiheDatum, AbgabeFrist, ArtID, KundID, ArtAnzahl, pfand):
    c = conn.cursor()
    c.execute('INSERT INTO Ausleihe (AusleiheDatum, AbgabeFrist, ArtID, KundID, ArtAnzahl, pfand) VALUES (?, ?, ?, ?, ?, ?)', 
              (AusleiheDatum, AbgabeFrist, ArtID, KundID, ArtAnzahl, pfand))
    conn.commit()


def add_customer_to_database(conn, KundID, KundName, Matrik, email, Vermerk):
    c = conn.cursor()
    c.execute('INSERT INTO Kunde (KundID, KundName, Matrik, email, Vermerk) VALUES (?, ?, ?, ?, ?)', 
              (KundID, KundName, Matrik, email, Vermerk))
    conn.commit()


def main():
    conn = connect_to_database()

    print("Ready to scan a product...")

    while True:
        ArtID = input("Scan a barcode: ")

        if product_exists_in_database(conn, ArtID):
            print("Product already exists in the database. What would you like to do?")
            print("1. Update the number of available pieces")
            print("2. Delete the product from the database")
            print("3. Rent a product")
            option = input("Enter your option (1-3): ")

            if option == '1':
                Anzahllager = int(input("Enter the new number of available pieces: "))
                update_product_in_database(conn, ArtID, Anzahllager)
                print("Product updated in the database.")
            elif option == '2':
                delete_product_in_database(conn, ArtID)
                print("Product deleted from the database.")
            elif option == '3':
                if is_available(conn, ArtID):
                    KundID = input("Enter customer ID: ")
                    KundName = input("Enter customer name: ")
                    Matrik = input("Enter matrikel number: ")
                    email = input("Enter email: ")
                    Vermerk = input("Enter comment: ")

                    add_customer_to_database(conn, KundID, KundName, Matrik, email,  Vermerk)
            
                    AusleiheDatum = datetime.date.today().isoformat()  # Today's date
                    AbgabeFrist = input("Enter return date (YYYY-MM-DD): ")
                    ArtAnzahl = input("Enter the number of products to be rented: ")
                    pfand = input("Enter the caution money to be paid: ")

                    add_rent_to_database(conn, KundID, AusleiheDatum, AbgabeFrist, ArtID, ArtAnzahl, pfand)
                    rent_product_in_database(conn, ArtID, ArtAnzahl)
                elif not is_available(conn, ArtID):
                    print("The product is currently not available")

                else:
                    print("This product is not rentable")
                 
        else:
            ArtID = input("Scan a barcode: ")
            ArtName = str(input("Enter the product name: "))
            Anzahllager = int(input("Enter the number of available pieces: "))
            buying_price = float(input("Enter the buying price: "))
            AblaufsDatum = str(input("what is the expiry date: "))
            Ausleihbar = input("Is the product rentable? Enter 1 for YES and 0 for NO: ")

            add_product_to_database(conn, ArtID, ArtName, Anzahllager, buying_price, Ausleihbar, AblaufsDatum)
            print("Product added to database.")

if __name__ == "__main__":
    main()
