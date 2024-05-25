from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Szoba(ABC):
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam

    @abstractmethod
    def ar(self):
        pass

class EgyagyasSzoba(Szoba):
    def ar(self):
        return 15000

class KetagyasSzoba(Szoba):
    def ar(self):
        return 25000

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szoba, datum, napok):
        self.szoba = szoba
        self.datum = datum
        self.napok = napok

    def get_ar(self):
        szoba_ar = self.szoba.ar()
        foglalas_ar = szoba_ar * self.napok
        print(f"A foglalás ára: {foglalas_ar} HUF (Szoba ára: {szoba_ar} HUF/éjszaka)")
        return foglalas_ar

    def __repr__(self):
        return f"Szoba: {self.szoba.szobaszam}, Dátum: {self.datum}, Napok: {self.napok}"

def main():
    # Szálloda létrehozása
    szalloda = Szalloda("Kényelmes Szálloda")

    # Szobák létrehozása és hozzáadása a szállodához
    egyagyas1 = EgyagyasSzoba("101")
    egyagyas2 = EgyagyasSzoba("102")
    egyagyas3 = EgyagyasSzoba("103")
    egyagyas4 = EgyagyasSzoba("104")
    egyagyas5 = EgyagyasSzoba("105")
    ketagyas1 = KetagyasSzoba("201")
    ketagyas2 = KetagyasSzoba("202")
    ketagyas3 = KetagyasSzoba("203")
    ketagyas4 = KetagyasSzoba("204")
    ketagyas5 = KetagyasSzoba("205")
    szalloda.add_szoba(egyagyas1)
    szalloda.add_szoba(egyagyas2)
    szalloda.add_szoba(egyagyas3)
    szalloda.add_szoba(egyagyas4)
    szalloda.add_szoba(egyagyas5)
    szalloda.add_szoba(ketagyas1)
    szalloda.add_szoba(ketagyas2)
    szalloda.add_szoba(ketagyas3)
    szalloda.add_szoba(ketagyas4)
    szalloda.add_szoba(ketagyas5)


    # Foglalások létrehozása
    foglalasok = [
        Foglalas(egyagyas1, datetime(2024, 4, 21), 2),
        Foglalas(egyagyas2, datetime(2024, 4, 22), 3),
        Foglalas(ketagyas1, datetime(2024, 4, 23), 1),
        Foglalas(ketagyas2, datetime(2024, 4, 24), 4),
        Foglalas(ketagyas3, datetime(2024, 6, 25), 2),
        Foglalas(ketagyas4, datetime(2024, 5, 19), 9),
        Foglalas(egyagyas5, datetime(2024, 4, 26), 2)
    ]

    # Felhasználói interfész
    while True:
        print("\nVálassz műveletet:")
        print("1. Foglalás")

        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Művelet kiválasztása (1/2/3/4): ")

        if valasztas == "1":
            # Foglalás
            szoba_szam = input("Kérem a szoba számát: ")
            datum_str = input("Kérem a foglalás kezdő dátumát (ÉÉÉÉ-HH-NN): ")
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            napok = int(input("Kérem a foglalás napjainak számát: "))

            # Ellenőrizze, hogy a szoba létezik
            szoba = next((sz for sz in szalloda.szobak if sz.szobaszam == szoba_szam), None)
            if szoba is None:
                print("Hiba: A megadott szoba nem létezik.")
                continue

            # Ellenőrizze, hogy a dátum jövőbeli
            if datum < datetime.now():
                print("Hiba: A foglalás kezdő dátuma nem lehet a múltban.")
                continue

            # Ellenőrizze, hogy a foglalás legalább egy napra szól
            if napok < 1:
                print("Hiba: A foglalásnak legalább egy napra kell szólnia.")
                continue

            # Ellenőrizze, hogy a szoba elérhető-e a megadott dátumon
            foglalt_szobak = [f.szoba for f in foglalasok if f.datum <= datum <= f.datum + timedelta(days=f.napok)]
            if szoba in foglalt_szobak:
                print("Hiba: A megadott szoba már foglalt ezen a napon.")
                continue

            # Foglalás létrehozása és hozzáadása a foglalásokhoz
            foglalas = Foglalas(szoba, datum, napok)
            foglalasok.append(foglalas)
            foglalas.get_ar()
            print("Foglalás sikeresen létrehozva.")

        elif valasztas == "2":
            # Lemondás
            print("Foglalások:")
            for i, foglalas in enumerate(foglalasok):
                print(f"{i+1}. {foglalas}")

            foglalas_index = input("Kérem a lemondandó foglalás sorszámát: ")
            try:
                foglalas_index = int(foglalas_index)
                if foglalas_index < 1 or foglalas_index > len(foglalasok):
                    raise ValueError()
            except ValueError:
                print("Hiba: Érvénytelen sorszám.")
                continue

            lemondando_foglalas = foglalasok[foglalas_index - 1]
            foglalasok.remove(lemondando_foglalas)
            print("Foglalás sikeresen lemondva.")

        elif valasztas == "3":
            # Foglalások listázása
            print("Foglalások:")
            for foglalas in foglalasok:
                print(f"- {foglalas}")

        elif valasztas == "4":
            # Kilépés
            print("Kilépés...")
            break

        else:
            print("Hiba: Érvénytelen művelet.")
            

if __name__ == "__main__":
    main()