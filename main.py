#Uvoz potrebnih paketa
import sqlite3
import time
import os

#Postavka PYFIGLET paketa
import pyfiglet
naziv = pyfiglet.figlet_format("Projekat Ratko")


class Author:
    # Klasa autora rada
    def __init__(self, ime, prezime, tema):
        self.ime = ime
        self.prezime = prezime
        self.tema = tema

    def __str__(self):
        return "Projekat pravio " + self.ime + " " + self.prezime + ", na temu " + self.tema


def menu():
    print(naziv)
    print('Dobrodosli u pocetni meni, za odabir funkcije unesite samo njen redni broj.')
    menu_input = input(
        "1.Instaliranje paketa\n2.Meni\n3.Kreiranje baze podataka\n4.Unos u bazu\n5.Brisanje iz baze\n6.Listanje iz baze\n7.Azuriranje baze")
    if menu_input == "1":
        install_data()
        menu()
    elif menu_input == "2":
        menu()
    elif menu_input == "3":
        try:
            create_base()
        except:
            print("Doslo je do greske, provjerite da baza vec ne postoji")
            menu()
    elif menu_input == "4":
        base_insert()
    elif menu_input == "5":
        base_delete()
    elif menu_input == "6":
        base_select()
    elif menu_input == "7":
        base_update()


def install_data():
    print("Instaliram potrebne pakete..")
    os.system("pip install pyfiglet")
    time.sleep(3)


def create_base():
    connection = sqlite3.connect('projekat.db')
    cursor = connection.cursor()
    # Kreira tabelu sa podatcima o vlasniku
    sql_command = """CREATE TABLE vozac(\
           id INTEGER PRIMARY KEY,\
           Ime VARCHAR(20),\
           Prezime VARCHAR(20),\
           Godine VARCHAR(2));"""
    cursor.execute(sql_command)

# Kreira tabelu sa podatcima o automobilu
    sql_command2 = """CREATE TABLE auto(\
          id INTEGER PRIMARY KEY,\
          Naziv VARCHAR(20),\
          Model VARCHAR(30),\
          Tip VARCHAR(20),\
          Broj_vrata CHAR(1),\
          Motor VARCHAR(5),\
          Konjskih_snaga VARCHAR(4));"""
    cursor.execute(sql_command2)

# Kreira tabelu sa podatcima o dodatnoj opremi koju automobil posjeduje
    sql_command1 = """CREATE TABLE dodatna_oprema(\
            id INTEGER PRIMARY KEY,\
            Parking_Senzori VARCHAR(2),\
            Alu_Felge VARCHAR(2),\
            Klima VARCHAR(2),\
            Rikverc_Kamera VARCHAR(2),\
            Grijanje_sjedista VARCHAR(2),\
            Panorama VARCHAR(2));"""
    cursor.execute(sql_command1)
    sql_command3 = """CREATE TABLE info(\
            id INTEGER PRIMARY KEY,\
            Boja VARCHAR(15),\
            Ostecenja VARCHAR(2),\
            Korozija VARCHAR(2));"""
    cursor.execute(sql_command3)
    connection.close()
    return menu()


def base_insert():
    connection = sqlite3.connect('projekat.db')
    cursor = connection.cursor()
    username = input("Unesite Vase ime")
    surname = input("Unesite Vase prezime")
    age = int(input("Koliko imate godina"))
    # ID korisnika i vozila je isti
    identif = int(input('Unesite ID'))
    name = str(input('Unesite naziv auta'))
    model = str(input('Unesite model vozila'))
    type = str(input('Unesite tip automobila'))
    car_door = int(input('Unesite broj vrata na automobilu'))
    engine = float(input('Unesite motor automobila'))
    hp = int(input('Unesite broj konjskih snaga automobila'))
    # Podatci za dodatnu opremu automobila
    park_sens = input("Da li automobil ima parking senzore? Da/Ne")
    alu_felge = input("Da li automobil ima aluminijske feluge? Da/Ne")
    air_con = input("Da li automobil ima klimu? Da/Ne")
    rev_camera = input("Da li automobil ima Rikverc kameru? Da/Ne")
    heat_seat = input("Da li automobil ima grijanje u sjedistima? Da/Ne")
    panor = input("Da li automobil ima panoramu? Da/Ne")
    #Podatci za listu info
    carcolor = input('Unesite boju automobila.')
    cardamage = input('Jel auto nekada bilo havarisano? Da/Ne')
    carcorosion = input('Ima li korozije na autu? Da/Ne')
    addons_list = [(identif, park_sens, alu_felge,
                    air_con, rev_camera, heat_seat, panor)]

    infolist = [(identif, carcolor, cardamage, carcorosion)]

    list = [(identif, name, model, type, car_door, engine, hp)]
    connection.executemany("""INSERT INTO auto(id, Naziv, Model,Tip, Broj_vrata, Motor, Konjskih_snaga) VALUES (?,?,?,?,?,?,?)""",
                           list)
    vozac_list = [(identif, username, surname, age)]
    connection.executemany(
        """INSERT INTO vozac(id, Ime, Prezime, Godine) VALUES (?,?,?,?)""", vozac_list)
    connection.executemany(
        """INSERT INTO dodatna_oprema(id, Parking_Senzori, Alu_Felge, Klima, Rikverc_Kamera, Grijanje_sjedista, Panorama) VALUES (?,?,?,?,?,?,?)""", addons_list)
    connection.executemany("""INSERT INTO info(id, Boja, Ostecenja, Korozija) VALUES (?,?,?,?)""", infolist)
    connection.commit()
    connection.close()
    return menu()


def base_delete():
    base_delete_input = input('Unesite ID automobila za brisanje')
    list = [(base_delete_input)]
    connection = sqlite3.connect('projekat.db')
    cursor = connection.cursor()
    # Brise sve podatke iz tabela
    connection.executemany("DELETE FROM auto WHERE id = ?", base_delete_input)
    connection.executemany(
        "DELETE FROM dodatna_oprema WHERE id = ?", base_delete_input)
    connection.executemany("DELETE FROM vozac WHERE id = ?", base_delete_input)
    connection.executemany("DELETE FROM info WHERE id = ?", base_delete_input)
    connection.commit()
    connection.close()
    return menu()


def base_select():
    #Uzima sve podatke iz baze i ispisuje ih
    connection = sqlite3.connect('projekat.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vozac, auto, dodatna_oprema, info")
    ans = cursor.fetchall()
    for i in ans:
        print(i)
        #Pet sekundi pauze do ucitavanja menija
        time.sleep(5)
        return menu()

def base_update():
    #Azurira podatke vozaca u bazi
    xupdate = input('Sta zelite da azurirate, \n1.Ime\n2.Prezime\n3.Godine')
    if xupdate == '1':
        nameupdate = input('Koje ime zelite da unesete?')
        idupdate = int(input('Koji je Vas ID?'))
        updatelist = [(nameupdate, idupdate)]
        connection = sqlite3.connect('projekat.db')
        cursor = connection.cursor()
        cursor.executemany("""UPDATE vozac SET Ime=? WHERE id=?""", updatelist)
        connection.commit()
        connection.close()
        return menu()
    elif xupdate == '2':
        surnameupdate = input('Unesite novo prezime')
        idupdate = int(input('Koji je Vas ID?'))
        updatelist = [(surnameupdate, idupdate)]
        connection = sqlite3.connect('projekat.db')
        cursor = connection.cursor()
        cursor.executemany("""UPDATE vozac SET Prezime=? WHERE id=?""", updatelist)
        connection.commit()
        connection.close()
        return menu()
    elif xupdate == '3':
        ageupdate = input('Unesite nove godine')
        idupdate = int(input('Koji je Vas ID?'))
        updatelist = [(ageupdate, idupdate)]
        connection = sqlite3.connect('projekat.db')
        cursor = connection.cursor()
        cursor.executemany("""UPDATE vozac SET Godine=? WHERE id=?""", updatelist)
        connection.commit()
        connection.close()
        return menu()


d1 = Author("Ratko", "Sopic", "Automobili")
print(d1)
time.sleep(4)
menu()
