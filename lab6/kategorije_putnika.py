from sys import stderr

from lab6.enums import UslugaNaLetu
from lab6.putnik import Putnik


class PutnikEkonomskeKlase(Putnik):

    def dodaj_izabrane_usluge(self, cena_usluga):
        if not self.cena_karte:
            raise ValueError("Greska, ne postoji cena karte !\n")

        suma, nove_usluge = 0, []
        for usluga, cena in cena_usluga.items():
            nove_usluge.append(usluga)
            suma += cena

        self.usluge.extend(nove_usluge)
        self.cena_karte += suma

        print(
            "\nOvo su nove usluge:\n" +
            "\n".join(usluga.value for usluga in nove_usluge) +
            f"\nUkupna cena usluga je: {suma}"
        )

    def __str__(self):
        return super().__str__().replace("Putnik", "Putnik ekonomske klase")


class PutnikBiznisKlase(Putnik):
    def __init__(self, usluge=(UslugaNaLetu.BRZO_UKRCAVANJE,), **kwargs):
        super().__init__(**kwargs)

        for usluga in usluge:
            if UslugaNaLetu.valid_service_str(usluga):
                self.usluge.append(UslugaNaLetu.get_service_from_str(usluga))
            elif isinstance(usluga, UslugaNaLetu):
                self.usluge.append(usluga)

    def __str__(self):
        return super().__str__().replace("Putnik", "Putnik biznis klase")


if __name__ == '__main__':
    jim = PutnikEkonomskeKlase("Jim Jonas", 'UK', '123456', 450, True)
    print(jim)
    print()

    extra_services = {
        UslugaNaLetu.OBROK: 10,
        UslugaNaLetu.WIFI: 15
    }
    try:
        jim.dodaj_izabrane_usluge(extra_services)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")
    print(f"\nPutnik {jim.ime} nakon dodavanja usluga:")
    print(jim)
    print()

    bob = PutnikEkonomskeKlase("Bob Jones", 'Denmark', '987654', 420)
    print(bob)
    print()

    mike = PutnikBiznisKlase(ime="Mike Stone", drzava="USA",
                             pasos='234567', cena_karte=550, covid_bezbedan=True,
                             usluge=(UslugaNaLetu.BRZO_UKRCAVANJE, UslugaNaLetu.WIFI))
    print(mike)
    print()

    brian = PutnikBiznisKlase(ime="Brian Brown", drzava="UK",
                              pasos='546234', cena_karte=670, covid_bezbedan=True,
                              usluge=("Osiguranje leta", "Uzina", "Izbor sedista"))
    print(brian)
