# Naam: Casper Juffermans
# Studentnummer: s4270118

import sympy # import the libary sympy om hun priem getal generator te gebruiken
# ik heb sympy gebruikt omdat ik dat eleganter vind dan gewoon hardcoded de array met priemgetallen neerplop 

primes = list(sympy.primerange(0,1000)) # zet alle priemgetallen van 0 tot 1000 in de lijst (technisch kan je ook 2 tot 1000 doen maar idk vind ik lelijk en het is de memorysave niet waard)
mistakes = 0 # maakt een counter voor alle situaties waar een combinatie niet te vinden is

for x in range(3,1000):
    xattempted = False
    if x%2==0:
        for i in primes: # zorgt dat de waarde van de eerste priemgetal varieert tussen alle priemgetallen
            if i<x and xattempted==False: # voorkomt overtollig te checken of een getal een combinatie is van een priemgetal hoger dan het getal zelf, kijkt daarnaast ook of de combinatie al gevonden is
                for j in primes:
                    if j<x and xattempted==False: #zelfde als hierboven
                        if i+j==x: 
                            # print(f"Het getal {x} is te schrijven als de som van {i} en {j}")
                            xattempted=True # zorgt dat de loop niet opnieuw wordt gerund indien een combinatie gevonden is
                    else:
                        break 
            else: 
                break
        if xattempted==False: #indien de loop compleet is maar geen combinatie is gevonden, dan wordt dit in de console geprint en wordt er een mistake bij de counter toegevoegd
            print(f"Het getal {x} is niet te schrijven als de som van twee priemgetallen")
            mistakes+=1

# print(f"Er {mistakes} instanties waarbij de som van twee priemgetallen niet overeenkomt met het getal")

if mistakes==0:
    print(f"Er zijn geen fouten gevonden, dus het vermoeden van Goldbach klopt")