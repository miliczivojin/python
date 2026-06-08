from sys import stderr
from datetime import datetime


class Putnik:
    def __init__(self, ime, drzava, pasos, covid_bezbedan=False):
        self.ime = ime
        self.drzava = drzava
        self.pasos = pasos
        self.covid_bezbedan = covid_bezbedan

    @property
    def pasos(self):
        if not hasattr(self, '_Putnik__pasos'):
            self.__pasos = None
        return self.__pasos

    @pasos.setter
    def pasos(self, value):
        if isinstance(value, str) and len(value) == 6 and value.isdigit():
            self.__pasos = value
        elif isinstance(value, int) and 100000 <= value <= 999999:
            self.__pasos = str(value)

    def __str__(self):
        putnik_str = "\n--Putnik\n"
        putnik_str += f"Ime: {self.ime}\n"
        putnik_str += f"Drzava: {self.drzava}\n"
        putnik_str += f"Pasos: {self.pasos}\n"
        putnik_str += f"Bezbednost: {'Bezbedan od Covida' if self.covid_bezbedan else 'Nije bezbedan od Covida'}\n"
        return putnik_str

    def azuriraj_covid_bezbedan(self, tip_uverenja, datum_uverenja):
        if not isinstance(tip_uverenja, str) or tip_uverenja.lower() not in ['vakcinacija', 'negativan_test']:
            stderr.write("Pogresna vrednost za tip uverenja, promena statusa ne moze biti izvrsena !")
            return
        if not isinstance(datum_uverenja, (datetime, str)):
            stderr.write("Pogresna vrednost za datum uverenja, promena statusa ne moze biti izvrsena !")
            return
        if isinstance(datum_uverenja, str):
            datum_uverenja = datetime.strptime(datum_uverenja, "%d/%m/%Y")

        delta = datetime.now() - datum_uverenja
        self.covid_bezbedan = (tip_uverenja.lower() == "vakcinacija" and delta.days < 365) or (
                tip_uverenja.lower() == "negativan_test" and delta.days < 3)

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
