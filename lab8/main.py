from sys import stderr

import pickle as pkl
import csv

from pathlib import Path
from collections import defaultdict
from operator import itemgetter

DATA_DIR = Path.cwd() / 'data'


def get_results_dir():
    results_dir = Path.cwd() / 'results'
    if not results_dir.exists():
        results_dir.mkdir()
    return results_dir


# .txt
def ucitaj_iz_txt_fajla(putanja):
    try:
        with open(putanja, "r") as fobj:
            return [linija.rstrip("\n") for linija in fobj.readlines()]
    except FileNotFoundError:
        stderr.write(f"Iz ucitaj_iz_txt_fajla: fajl sa zadatom putanjom {putanja} ne postoji\n")
    except OSError as ose:
        stderr.write(f"Iz ucitaj_iz_txt_fajla: greska pri ucitavanju podataka iz fajla {putanja} \n {ose}\n")
    return None


def upisi_u_txt_fajl(lista, putanja):
    try:
        with open(putanja, "w") as fobj:
            for linija in lista:
                fobj.write(f"{linija}")
    except OSError as ose:
        stderr.write(f"Iz upisi_u_txt_fajla: greska pri upisivanju podataka u fajla {putanja} \n {ose}\n")


# .bin, .dat
def deserijalizuj_podatke(putanja):
    try:
        with open(putanja, "rb") as fobj:
            return pkl.load(fobj)
    except pkl.PickleError as pe:
        stderr.write(f"Iz deserijalizuj_podatke: Pickle greska pri deserijalizaciji podataka iz {putanja} \n{pe}\n")
    except OSError as ose:
        stderr.write(f"Iz deserijalizuj_podatke: OS greska pri deserijalizaciji podataka iz {putanja}\n{ose}\n")
    return None


def serijalizuj_podatke(podaci, putanja):
    try:
        with open(putanja, "wb") as fobj:
            pkl.dump(podaci, fobj)
    except pkl.PicklingError as pe:
        stderr.write(f"Iz serijalizuj_podatke: Pickling greska pri serijalizaciji podataka\n{pe}\n")
    except OSError as ose:
        stderr.write(f"Iz serijalizuj_podatke: OS greska pri serijalizaciji podataka\n{ose}\n")


# .csv
def ucitaj_iz_csv_fajla(putanja):
    try:
        with open(putanja, "r") as fobj:
            return list(csv.DictReader(fobj))
    except OSError as ose:
        stderr.write(f"Iz ucitaj_iz_csv_fajla: greska pri ucitavanju iz csv fajla {putanja} \n {ose}\n")
    return None


def upisi_u_csv(putanja, lista_recnika):
    try:
        with open(putanja, "w", newline='') as fobj:
            header = tuple(lista_recnika[0].keys())
            csv_writer = csv.DictWriter(fobj, fieldnames=header)
            csv_writer.writeheader()

            for podaci in lista_recnika:
                csv_writer.writerow(podaci)
    except OSError as ose:
        stderr.write(f"Greska pri upisu podataka u fajl {putanja} \n {ose}\n")


def analiza_fajlova_sa_slikama(putanja):
    dict_slika = defaultdict(list)

    slike = ucitaj_iz_txt_fajla(putanja)

    if not slike:
        return

    for slika in slike:
        putanja, naziv = slika.rsplit("/", maxsplit=1)
        entitet = putanja.split("/", maxsplit=2)[2].replace("/", "_")

        dict_slika[entitet].append(naziv)

    broj_slika = []
    for entitet, lista in dict_slika.items():
        broj_slika.append(f"{entitet} : {len(lista)}\n")

    upisi_u_txt_fajl(broj_slika, get_results_dir() / 'zadatak1_stats.txt')
    serijalizuj_podatke(dict_slika, get_results_dir() / 'zadatak1_dict.pkl')


def unos_podataka_o_timu():
    print(""" 
    Potrebno je da unesete podatke o svakom clanu tima u sl obliku:
    ime_prezime, godine_starosti, poeni_na_takmicenju
    Za kraj unosa, unesite 'kraj'
    """)

    clanovi = []
    k = 1

    while True:
        podaci = input(f"Unesite podatke o {k}. clanu tima:\n")
        if podaci.lower() == "kraj":
            break
        try:
            ime, godine, poeni = podaci.split(',')
            clanovi.append({"ime_prezime": ime.strip(), "godina": int(godine.strip()), "poeni": float(poeni.strip())})
        except ValueError as ve:
            print(f"Greksa pri unosu podataka (originalna poruka: {ve}). Probajte ponovo")
        else:
            k += 1

    clanovi.sort(key=itemgetter("poeni"), reverse=True)
    upisi_u_csv(get_results_dir() / 'zadatak2_clanovi_tima.csv', clanovi)


def zabelezi_presek_brojeva(putanja1, putanja2):
    lista1 = ucitaj_iz_txt_fajla(putanja1)
    lista2 = ucitaj_iz_txt_fajla(putanja2)

    if not (lista1 and lista2):
        raise Exception("GRESKA: Podaci iz bar jednog od zadatih fajlova se ne mogu ucitati!")

    lista1 = [int(red) for red in lista1 if red.isdigit()]
    lista2 = [int(red) for red in lista2 if red.isdigit()]

    presek = [broj for broj in lista1 if broj in lista2]

    dictionary = {putanja1.name: lista1, putanja2.name: lista2, "zajednicki_brojevi": presek}
    serijalizuj_podatke(dictionary, get_results_dir() / 'zadatak3_rezultati.pkl')


if __name__ == '__main__':
    analiza_fajlova_sa_slikama(DATA_DIR / 'image_files_for_training.txt')

    zad1_recnik = deserijalizuj_podatke(get_results_dir() / 'zadatak1_dict.pkl')
    if zad1_recnik:
        for ent, lista_slika in zad1_recnik.items():
            print(f"{ent.upper()}: {', '.join(lista_slika)}")

    zad1_lista = ucitaj_iz_txt_fajla(get_results_dir() / 'zadatak1_stats.txt')
    if zad1_lista:
        for entity_stat in zad1_lista:
            print(entity_stat)

    unos_podataka_o_timu()

    podaci_o_timu = ucitaj_iz_csv_fajla(get_results_dir() / 'zadatak2_clanovi_tima.csv')
    if podaci_o_timu:
        for podaci_o_clanu in podaci_o_timu:
            # pprint(podaci_o_clanu)
            name, years, points = podaci_o_clanu.values()
            print(f"{name}, {years} godina, {points} poena")

    f1 = DATA_DIR / 'happy_numbers.txt'
    f2 = DATA_DIR / 'prime_numbers.txt'
    zabelezi_presek_brojeva(f1, f2)

    zad1_recnik = deserijalizuj_podatke(get_results_dir() / 'zadatak3_rezultati.pkl')
    print(zad1_recnik)
