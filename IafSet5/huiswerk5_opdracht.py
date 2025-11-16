# Naam:
# Studentnummer:

import sys
import numpy as np
import matplotlib.pyplot as plt

def read():
    """Lees tabel "sterren.txt". De output van deze functie zijn lijsten van de kolommen in de tabel.
    """
    with open("IafSet5\\sterren.txt", "r") as f:
        lines = f.readlines()
        temperaturen = np.array([])
        abs_magnitudes = np.array([])
        klasse = np.array([])
        afstand = np.array([])
        for l in lines:
            if l[0] == "#":
                continue
            else:
                temperaturen = np.append(temperaturen, float(l.split()[0]))
                abs_magnitudes = np.append(abs_magnitudes, float(l.split()[1]))
                klasse = np.append(klasse, str(l.split()[2]))
                afstand = np.append(afstand, float(l.split()[3]))
    return temperaturen, abs_magnitudes, klasse, afstand



def lichtkracht(abs_mag):
    """Gebruik de absolute magnitude van de sterren om de lichtkracht in eenheid L_zon te berekenen.
    De output van deze functie is een lijst met de lichtkracht van de sterren.
    """
    abs_mag_zon = 4.75    # absolute bolometrische magnitude van de zon
    
    lk = [10**((abs_mag_zon - mag) / 2.5) for mag in abs_mag]  # in L_zon
    # voor als de np.vect array methode niet werkt:
    """"
    lk = []
    for mag in abs_mag:
        lk.append(10**((abs_mag_zon-mag)/-2.5)) # in L_zon
    """ 

    return lk


def schijnbare_magnitude(abs_mag, afstand):
    """Bereken de schijnbare magnitude van de sterren.
    De output van deze functie is een lijst van de schijnbare magnitudes van de sterren.
    """
    app_mag = [5*np.log(0.1*afstand)+ abs_mag] # assuming d in parsec
    # TODO bereken de schijnbare magnitude van de sterren
    return app_mag


def massa_levensduur(app_mag, lk, afstand, abs_mag, temp, klasse):
    """Print de gegevens van de vanaf aarde gezien helderste ster, en de vanaf aarde gezien zwakste ster,
    Bereken de massa van deze sterren, en de verhouding van de levensduren van deze twee sterren.
    """
    helderste_ster_index = np.argmin(app_mag)
    zwakste_ster_index = np.argmax(app_mag) 

    print(f"Helderste ster: \n"
          f"Absolute magnitude: {abs_mag[helderste_ster_index]}\n"
          f"Temperatuur: {temp[helderste_ster_index]} K\n"
          f"Klasse: {klasse[helderste_ster_index]}\n"
          f"Afstand: {afstand[helderste_ster_index]} pc\n")
    
    print(f"Zwakste ster: \n"
          f"Absolute magnitude: {abs_mag[zwakste_ster_index]}\n"
          f"Temperatuur: {temp[zwakste_ster_index]} K\n"
          f"Klasse: {klasse[zwakste_ster_index]}\n"
          f"Afstand: {afstand[zwakste_ster_index]} pc\n")
    
    boundary_condition = 0.7**2.5 # boundary condition for main sequence stars, according the scaling law.

    # calculating weakest star in solar masses
    if lk[helderste_ster_index] < boundary_condition:
        mass_helderste = (lk[helderste_ster_index])**(1/2.5)
    else:
        mass_helderste = (lk[helderste_ster_index])**(1/4)

    # calculating weakest star in solar masses
    if lk[zwakste_ster_index] < boundary_condition:
        mass_zwakste = (lk[zwakste_ster_index])**(1/2.5)
    else:
        mass_zwakste = (lk[zwakste_ster_index])**(1/4)

    print(f"Massa van de helderste ster: {mass_helderste} M_zon \n")
    print(f"Massa van de zwakste ster: {mass_zwakste} M_zon \n")
    
    verhouding_levensduur = (mass_helderste / mass_zwakste)**-3
    print(f"De verhouding van de levensduur van de helderste ster tot de zwakste ster is: {verhouding_levensduur} \n")

def plot(temp, lk, klasse):
    """Plot een hr-diagram van de sterren. De x-as is de temperatuur, de y-as is de lichtkracht. Beide assen
    hebben een logaritmische schaal. Vergeet niet de assen te labelen (met eenheden), en geef duidelijk aan
    wat de hoofdreeks sterren, reuzen en superreuzen zijn.
    """
    from matplotlib.ticker import LogLocator, FuncFormatter

    x_axis = np.array(temp)
    y_axis = np.array(lk)
    fig, ax = plt.subplots()

    ax.scatter(x_axis, y_axis, s=5)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("Temperatuur (K) (log)")
    ax.set_ylabel("Lichtkracht (L_zon) (log)")
    ax.grid(True)

    ax.xaxis.set_major_locator(LogLocator(base=10))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.2f}"))

    # ax.legend(["Hoofdreeks", "Reuzen", "Superreuzen"])

    plt.savefig("hr-diagram.png")


def main():
    """Vanaf hier roep je al je  functies aan.
    """
    temp, abs_mag, klasse, afstand = read()
    lk = lichtkracht(abs_mag)
    app_mag = schijnbare_magnitude(abs_mag, afstand)
    massa_levensduur(app_mag, lk, afstand, abs_mag, temp, klasse)
    plot(temp, lk, klasse)


if __name__ == "__main__":
    sys.exit(main())

main()