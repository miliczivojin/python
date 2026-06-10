from sys import stderr
from datetime import datetime


class Putnik:
    def __init__(self, ime, drzava, pasos, covid_bezbedan=False):
        self.ime = ime
        self.drzava = drzava
        self.covid_bezbedan = covid_bezbedan

        self.__pasos = None
        self.pasos = pasos

    @property
    def pasos(self):
        return self.__pasos

    @pasos.setter
    def pasos(self, value):
        if isinstance(value, int):
            value = str(value)

        if not isinstance(value, str):
            raise TypeError("Očekivan je tip int ili str za pasos!")

        if not value.isdigit():
            raise ValueError("Broj pasosa mora da se sastoji samo od cifara!")

        if len(value) != 6:
            raise ValueError("Broj pasosa mora da ima 6 cifara!")

        self.__pasos = value

    def __str__(self):
        putnik_str = "\n--Putnik\n"
        putnik_str += f"Ime: {self.ime}\n"
        putnik_str += f"Drzava: {self.drzava}\n"
        putnik_str += f"Pasos: {self.pasos}\n"
        putnik_str += f"Bezbednost: {'Bezbedan od Covida' if self.covid_bezbedan else 'Nije bezbedan od Covida'}\n"
        return putnik_str

    def azuriraj_covid_bezbedan(self, tip_uverenja, datum_uverenja):
        if not isinstance(tip_uverenja, str):
            raise TypeError("Očekivan je str za tip uverenja!")

        if tip_uverenja.lower() not in ['vakcinacija', 'negativan_test']:
            raise ValueError("Pogrešna vrednost za tip uverenja!")

        if not isinstance(datum_uverenja, (datetime, str)):
            raise TypeError("Očekivan je str ili datetime za datum uverenja!")

        if isinstance(datum_uverenja, str):
            try:
                datum_uverenja = datetime.strptime(datum_uverenja, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Neispravan format datuma uverenja!")

        delta = datetime.now() - datum_uverenja

        if tip_uverenja == "vakcinacija":
            self.covid_bezbedan = delta.days < 365
        else:
            self.covid_bezbedan = delta.days < 3

    @classmethod
    def from_string(cls, putnik_str):
        parts = [part.strip() for part in putnik_str.split(";")]
        if len(parts) == 4:
            return cls(*parts)

        stderr.write("Ulazni string nije odgovarajucg formata !")
        return None

    def __eq__(self, other):
        return isinstance(other, Putnik) and self.pasos == other.pasos and self.drzava == other.drzava


if __name__ == '__main__':
    pass
