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
    from matplotlib.ticker import FuncFormatter
    from matplotlib.colors import LinearSegmentedColormap

    temp = np.array(temp, dtype=float)
    lk = np.array(lk, dtype=float)
    klasse = np.array(klasse, dtype=str)

    fig, ax = plt.subplots()

    
    #  Color gradient based on luminosity
    cmap = LinearSegmentedColormap.from_list("red_blue_custom", ["darkred","orange","palegoldenrod","lightblue","darkblue"])
    norm = plt.Normalize(np.min(temp), np.max(temp)) 

    # different symbols for different stellar classes
    markers = {
        "I":  "8",
        "II": "d",
        "III":"s",
        "IV": "v",
        "V":  "*",
    }

    namen_markers = {
        "I":  "Superreuzen",
        "II": "Heldere reuzen",
        "III":"Reuzen",
        "IV": "Subreuzen",
        "V":  "Hoofdreeks sterren",
    }
    
    for stellar_class, marker in markers.items():
        mask = (klasse == stellar_class)
        if np.any(mask):
            ax.scatter(
                temp[mask],
                lk[mask],
                c=temp[mask], # color gradient values
                cmap=cmap,
                norm=norm,
                marker=marker,
                s=20,
                label=f"{namen_markers[stellar_class]}", # legend label
                zorder=1
            )
    
    # log scale, x axis info
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([40000,20000,10000,5000,2500])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter()) 
    ax.minorticks_off()
    ax.invert_xaxis()

    # custom limits 
    ax.set_ylim(1e-3,1e6)
    ax.set_xlim(40000,2000)

    # radius lines
    for log_r in np.linspace(-2,3,6):
        radius = 10**log_r
        x_r_lines = np.linspace(2000,40000,1000)
        y_r_lines = radius**2 * (x_r_lines/5778)**4 # using T/T_sun to ensure units are correct

        ax.plot(x_r_lines,y_r_lines, linestyle="--", color="white",zorder=2)
        middle_point = (x_r_lines[len(x_r_lines)//2], y_r_lines[len(y_r_lines)//2])
        ax.annotate(
            f"R={log_r} R$_\odot$",
            xy=middle_point,
            xytext=(5,5), # offset for readability
            textcoords='offset points',
            color="white",
        )



    # labels and grid
    ax.set_xlabel("Temperatuur (log(K))",c="white")
    ax.set_ylabel(f"Lichtkracht (log(L/L$_\odot$))"  ,c="white")
    ax.grid(True)

    # colors of different items
    ax.set_facecolor("black") # background color
    # tick colors
    ax.tick_params(axis='x',colors='white') 
    ax.tick_params(axis='y',colors='white') 
    # spine colors
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    fig.patch.set_facecolor('gray') # figure background color

    ax.legend()
    

    plt.savefig("hr-diagram.png")


def main():
    """Vanaf hier roep je al je  functies aan.
    """
    temp, abs_mag, klasse, afstand = read()
    print(klasse)
    lk = lichtkracht(abs_mag)
    app_mag = schijnbare_magnitude(abs_mag, afstand)
    massa_levensduur(app_mag, lk, afstand, abs_mag, temp, klasse)
    plot(temp, lk, klasse)


if __name__ == "__main__":
    sys.exit(main())

main()