from sys import stderr
from datetime import datetime

from lab5.putnik import Putnik


class Let:
    poletanje_dt_format = "%Y-%m-%d %H:%M"

    def __init__(self, broj_leta, vreme_poletanja):
        self.broj_leta = broj_leta
        self.putnici = []

        self.__vreme_poletanja = None
        self.vreme_poletanja = vreme_poletanja

    @property
    def vreme_poletanja(self):
        return self.__vreme_poletanja

    @vreme_poletanja.setter
    def vreme_poletanja(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, Let.poletanje_dt_format)
            except ValueError:
                raise ValueError("Neispravan format datuma i vremena poletanja!")

        if not isinstance(value, datetime):
            raise TypeError("Očekivan je tip str ili datetime za vreme poletanja!")

        if value <= datetime.now():
            raise ValueError("Vreme poletanja mora biti u budućnosti!")

        self.__vreme_poletanja = value

    def dodaj_putnika(self, novi_putnik):
        if not isinstance(novi_putnik, Putnik):
            raise TypeError(f"Očekivan je Putnik, primljen je {type(novi_putnik)}")

        if novi_putnik in self.putnici:
            raise ValueError(f"Putnik {novi_putnik.ime}:{novi_putnik.pasos} je već dodat!")

        if not novi_putnik.covid_bezbedan:
            raise ValueError(f"Putnik {novi_putnik.ime}:{novi_putnik.pasos} nije COVID bezbedan!")

        self.putnici.append(novi_putnik)

    def __str__(self):
        let_str = "--Let\n"
        let_str += f"Broj leta: {self.broj_leta}\n"
        let_str += f"Vreme: {self.vreme_poletanja}\n"
        let_str += "Putnici na letu:\n" if len(self.putnici) > 0 else "Nema putnika !"
        let_str += "\n".join(str(putnik) for putnik in self.putnici)
        return let_str

    def vreme_do_poletanja(self):
        if self.vreme_poletanja is None:
            stderr.write("Greška, vreme poletanja ne postoji!\n")
            return None

        seconds = int((self.vreme_poletanja - datetime.now()).total_seconds())
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, _ = divmod(seconds, 60)

        return days, hours, minutes

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
    lh1411 = None

    print("\nLETOVI:\n")
    try:
        lh1411 = Let('LF1411', '2026-06-11 6:50')
        print(lh1411)
    except (ValueError, TypeError) as er:
        print("Greška za LH1411:", er)
    print()
    try:
        lh992 = Let('LH992', '2026-07-05 12:20')
        print(lh992)
    except (ValueError, TypeError) as er:
        print("Greška za LH992:", er)
    print()

    putnici = []

    putnici_podaci = [
        ("Bob Smith", "UK", "12456", True),
        ("John Smith", "USA", 987656, True),
        ("Anna Smith", "Spain", "987659"),
    ]

    for p in putnici_podaci:
        try:
            putnici.append(Putnik(*p))
        except (ValueError, TypeError) as er:
            print("Greška pri pravljenju putnika:", er)

    try:
        putnici.append(Putnik.from_string("Luis Bouve; France; 123456; True"))
    except (ValueError, TypeError) as er:
        print("Greška iz from_string:", er)

    if lh1411:
        print(f"\nDodavanje putnika na let {lh1411.broj_leta}")
        for p in putnici:
            try:
                lh1411.dodaj_putnika(p)
            except (ValueError, TypeError) as er:
                print(f"Greška pri dodavanju putnika na Let: {er}\n")

        print(f"\nPokusaj dodavanja putnika koji je vec u listi putnika za let {lh1411.broj_leta}:")
        try:
            lh1411.dodaj_putnika(Putnik("J Smith", "USA", "987656", True))
        except (ValueError, TypeError) as er:
            print("Greška pri dodavanju novog putnika:", er)
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
