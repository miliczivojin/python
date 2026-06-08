import re
from sys import stderr
from datetime import datetime
from collections import defaultdict

from lab6.putnik import Putnik
from lab6.enums import UslugaNaLetu
from lab6.kategorije_putnika import PutnikEkonomskeKlase, PutnikBiznisKlase


class Let:
    poletanje_dt_format = "%Y-%m-%d %H:%M"

    def __init__(self, broj_leta, vreme_poletanja, ruta):
        self.broj_leta = broj_leta
        self.vreme_poletanja = vreme_poletanja
        self.ruta = ruta
        self.putnici = []

    @classmethod
    def from_dict(cls, let):
        def vrednost(kljuc):
            return let.get(kljuc)

        potrebni_kljucevi = ['br_leta', 'vreme_poletanja', 'polazna_lokacija', 'odrediste']
        if any(kljuc not in let for kljuc in potrebni_kljucevi):
            print("Dostupni kljucevi:\n" + "\n".join(kljuc for kljuc in let if kljuc in potrebni_kljucevi))

        return cls(vrednost('br_leta'), vrednost('vreme_poletanja'),
                   (vrednost('polazna_lokacija'), vrednost('odrediste')))

    @property
    def vreme_poletanja(self):
        try:
            return self.__vreme_poletanja
        except AttributeError:
            self.__vreme_poletanja = None
            return self.__vreme_poletanja

    @vreme_poletanja.setter
    def vreme_poletanja(self, value):
        if not isinstance(value, (str, datetime)):
            stderr.write(
                f"Vrednost datuma nije u odgovarajucem tipu podataka; Ocekivano je string ili datetime a uneto je {type(value)} !")
            return

        if isinstance(value, str):
            try:
                value = datetime.strptime(value, Let.poletanje_dt_format)
            except ValueError as ve:
                stderr.write(f"Greska prilikom parsiranja datuma:\n{ve}\n")
                return

        if value > datetime.now():
            self.__vreme_poletanja = value
        else:
            stderr.write("Vreme poletanja mora biti u buducnosti !\n")

    @property
    def ruta(self):
        try:
            return self.__ruta
        except AttributeError:
            self.__ruta = None
            return self.__ruta

    @ruta.setter
    def ruta(self, value):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            self.__ruta = tuple(value)
        elif isinstance(value, str) and sum(ch in ",->" for ch in value) == 1:
            polazak, destinacija = re.split('[,->]', value)
            self.__ruta = polazak.strip(), destinacija.strip()
        else:
            stderr.write("Pogresan tip podataka je unet za rutu u ruta.setter !")

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
        let_str += f"Ruta: {self.ruta if self.ruta else 'Nepoznata'}\n"
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

    def generator_putnika_sa_uslugama(self):
        dictionary = defaultdict(int)

        for putnik in self.putnici:
            if len(putnik.usluge) > 0:
                for usluga in putnik.usluge:
                    dictionary[usluga] += 1
                yield putnik

        print(f"\n\n\nNa letu {self.broj_leta} je stanje ovakvo:\n" + "\n".join(
            f"{key} : {value}" for key, value in dictionary.items()))

    def generator_kandidata_za_biznis_klasu(self, prag_cene):
        def uslov(putnik):
            return (isinstance(putnik, PutnikEkonomskeKlase)
                    and putnik.cena_karte > prag_cene
                    and len(putnik.usluge) > 0)

        for kandidat in sorted(filter(uslov, self.putnici), key=lambda k: k.cena_karte, reverse=True):
            yield kandidat


if __name__ == '__main__':
    lh1411 = Let('LH1411', '2026-06-20 6:50', ('Belgrade', 'Munich'))
    print(lh1411)
    print()

    lh992 = Let('LH992', '2026-06-26 12:20', 'Belgrade > Frankfurt')
    print(lh992)
    print()

    lh1514_dict = {'br_leta': 'lh1514',
                   'vreme_poletanja': '2026-6-21 16:30',
                   'polazna_lokacija': 'Paris',
                   'odrediste': 'Berlin'}

    lh1514 = Let.from_dict(lh1514_dict)
    print(lh1514)
    print()

    bob = PutnikEkonomskeKlase("Bob Smith", "UK", "123456", 250.0, True)
    john = PutnikEkonomskeKlase("John Smith", "USA", 987656, 450, True)
    luis = PutnikBiznisKlase(ime="Luis Bouve", drzava='France', pasos="123654", cena_karte=225,
                             usluge=[UslugaNaLetu.OBROK, UslugaNaLetu.WIFI], covid_bezbedan=True)

    anna = PutnikEkonomskeKlase("Anna Smith", "Spain", "987659", 375, True)
    try:
        dodatne_usluge = {UslugaNaLetu.OBROK: 10, UslugaNaLetu.WIFI: 15}
        anna.dodaj_izabrane_usluge(dodatne_usluge)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")

    print(f"\nDodavanje putnika na let {lh1411.broj_leta}")
    for p in [bob, john, anna, luis]:
        lh1411.dodaj_putnika(p)

    print(f"\nPodaci o letu {lh1411.broj_leta} nakon dodavanja putnika na let:\n")
    print(lh1411)

    print("\nPutnici sa dodatnim uslugama na letu:")
    # Jedan od nacina poziva generatora
    g = lh1411.generator_putnika_sa_uslugama()

    while True:
        try:
            print(next(g))
        except StopIteration:
            print("------- kraj spiska putnika sa dodatnim uslugama --------")
            break
    print()

    # Drugi nacin poziva generatora (tipicno koriscen)
    # for putnik in lh1411.generator_putnika_sa_uslugama():
    #     print(putnik)

    # Dodacemo putnicima usluge na letu radi provere generatorske metode
    try:
        dodatne_usluge_bob = {UslugaNaLetu.SEDISTA: 20, UslugaNaLetu.OSIGURANJE: 35}
        bob.dodaj_izabrane_usluge(dodatne_usluge_bob)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")

    try:
        dodatne_usluge_john = {UslugaNaLetu.OBROK: 20, UslugaNaLetu.WIFI: 35}
        john.dodaj_izabrane_usluge(dodatne_usluge_john)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")

    print("\nKandidati za prelazak u biznis klasu:")
    # Jedan od nacina poziva generatora
    g = lh1411.generator_kandidata_za_biznis_klasu(350)
    try:
        while True:
            print(next(g))
    except StopIteration:
        print("--- kraj liste kandidata ---")

    # Drugi nacin poziva generatora (tipicno koriscen)
    # print("\nPutnici kojima je ponudjena mogucnost prelaska u biznis klasu:")
    # for ind, putnik in enumerate(lh1411.generator_kandidata_za_biznis_klasu(350)):
    #     print(f"{ind+1}. {putnik}")
