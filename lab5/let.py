from sys import stderr
from datetime import datetime

from lab5.putnik import Putnik


class Let:
    poletanje_dt_format = "%Y-%m-%d %H:%M"

    def __init__(self, broj_leta, vreme_poletanja):
        self.broj_leta = broj_leta
        self.vreme_poletanja = vreme_poletanja
        self.putnici = []

    @property
    def vreme_poletanja(self):
        if not hasattr(self, "_Let__vreme_poletanja"):
            self.__vreme_poletanja = None
        return self.__vreme_poletanja

    @vreme_poletanja.setter
    def vreme_poletanja(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, Let.poletanje_dt_format)
        if isinstance(value, datetime) and value > datetime.now():
            self.__vreme_poletanja = value
        else:
            stderr.write("Pogresna vrednost za vreme poletanja !\n")

    def dodaj_putnika(self, putnik):
        if not isinstance(putnik, Putnik):
            stderr.write(f"Pogresna tip, ocekivan je Putnik a primljen je {type(putnik)} !\n")
        elif putnik in self.putnici:
            stderr.write(f"Putnik {putnik.ime}:{putnik.pasos} je vec dodat !\n")
        elif not putnik.covid_bezbedan:
            stderr.write(f"Putnik {putnik.ime}:{putnik.pasos} nije bezbedan !\n")
        else:
            self.putnici.append(putnik)

    def __str__(self):
        let_str = "--Let\n"
        let_str += f"Broj leta: {self.broj_leta}\n"
        let_str += f"Vreme: {self.vreme_poletanja}\n"
        let_str += "Putnici na letu:\n" if len(self.putnici) > 0 else "Nema putnika !"
        let_str += "\n".join(str(putnik) for putnik in self.putnici)
        return let_str

    def vreme_do_poletanja(self):
        if self.vreme_poletanja:
            delta = self.vreme_poletanja - datetime.now()
            days = delta.days
            hours, seconds = divmod(delta.seconds, 3600)
            minutes = seconds // 60
            return days, hours, minutes

        stderr.write("Greska, vreme poletanja ne postoji !")
        return None

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == len(self.putnici):
            raise StopIteration

        rezultat = self.putnici[self._index]
        self._index += 1
        return rezultat


if __name__ == '__main__':
    lh1411 = Let('LF1411', '2026-06-10 6:50')
    lh992 = Let('LH992', '2026-07-05 12:20')

    print("\nLETOVI:\n")
    print(lh1411)
    print()
    print(lh992)
    print()

    bob = Putnik("Bob Smith", "UK", "123456", True)
    john = Putnik("John Smith", "USA", 987656, True)
    anna = Putnik("Anna Smith", "Spain", "987659")
    luis = Putnik.from_string("Luis Bouve; France; 123456; True")

    print(f"\nDodavanje putnika na let {lh1411.broj_leta}")
    for p in [bob, john, anna, luis]:
        lh1411.dodaj_putnika(p)

    print(f"\nPokusaj dodavanja putnika koji je vec u listi putnika za let {lh1411.broj_leta}:")
    lh1411.dodaj_putnika(Putnik("J Smith", "USA", "987656", True))
    print()

    print(f"\nPodaci o letu {lh1411.broj_leta} nakon dodavanja putnika na let:\n")
    print(lh1411)

    print()

    do_poletanja = lh1411.vreme_do_poletanja()
    if do_poletanja:
        dani, sati, mins = do_poletanja
        print(f"Vreme preostalo do poletanja leta {lh1411.broj_leta}: "
              f"{dani} dana, {sati} sati, i {mins} minuta")

    print()

    print("\nPUTNICI NA LETU LH1411 (iter / next):")
    p_iter = iter(lh1411)
    try:
        while True:
            print(next(p_iter))
    except StopIteration:
        print("Svi putnici su izlistani")

    print()
    print("\nPUTNICI NA LETU LH1411 (FOR petlja):")
    for p in iter(lh1411):
        print(p)
