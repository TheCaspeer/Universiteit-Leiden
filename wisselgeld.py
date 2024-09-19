# Naam: Casper Juffermans
# Studentnummer: s4270118

# alhoewel ik weet dat je mag aannemen dat er een float ingevuld word, wou ik oefenen met error validation en dit leek me een grappig plekje
while True:
    inputVal = input("Hoeveel eurocent moet er terug gegeven worden?\n(vul in de vorm 1.23 in)\n")

    try:
        val = float(inputVal)*100 # zet om in een waarde die makkelijker te gebruiken is
        if(val==0):
            print(f"Het invullen van 0 cent zorgt ook voor 0 wisselgeld, vul een andere waarde in voor een nuttigere uitkomst")
        else:
            startbedrag = int(val)
            break
    except:
        print(f"De waarde die je hebt ingevuld ({inputVal}) is in de verkeerde vorm ingevuld.\nVul alsjeblieft een getal in de goeie vorm (12.34) in\n")
cent = int(startbedrag%100)
euro = int((startbedrag-cent)/100)
print(f"Je hebt succesvol een waarde van {euro} euro en {cent} cent ingevuld\n")

# input = input("Hoeveel eurocent moet er terug gegeven worden?\n(vul in de vorm 1.23 in)\n")

# startbedrag=int(float(input)*100)

# startbedrag = 79

# values init
munteenheden = [20,10,5,2,1] # indien deze wordt aangepast, pas ook de string functie aan zodat de print up-to-date blijft (is te automaten maar ben lui)
munten = [] 
i=0 

def customFloor(val): # custom floor functie omdat ik de math module niet mag gebruiken :(
    return round(val-0.5)

while(startbedrag>0): 
    munten.append(customFloor(startbedrag/munteenheden[i])) # rond naar beneden af hoeveel munten er in kunnen
    startbedrag = startbedrag%munteenheden[i] # gebruikt de modulo functie om de overige hoeveelheid te bereken
    i=i+1 #iterate een verder

# om nullreference errors te voorkomen zorgt het dat de munten array altijd een waarde heeft, ookal heb je 0 munten van die munteenheid
while(startbedrag==0 and len(munten)<len(munteenheden)):
    munten.append(0)

# telt hoeveel munten er per munteenheid zijn en telt dat bij elkaar op
totMunten = 0
for x in munten: 
    totMunten = totMunten + x


# init de array
stringvalues = ["Je moet in totaal: \n"]

# voorkomt dat informatie wordt gegeven over munten die niet betrokken zijn tot de transactie
if(munten[0]>0):
    stringvalues.append(f"{munten[0]} keer 20 cent,\n")

if(munten[1]>0):
    stringvalues.append(f"{munten[1]} keer 10 cent,\n")

if(munten[2]>0):
    stringvalues.append(f"{munten[2]} keer 5 cent,\n")

if(munten[3]>0):
    stringvalues.append(f"{munten[3]} keer 2 cent,\n")

if(munten[4]>0):
    stringvalues.append(f"{munten[4]} keer 1 cent\n")

stringvalues+= f"teruggeven aan de klant. Dit is een totaal van {totMunten} munten"

string = ""
for x in stringvalues: # voegt heel de string samen zodat het geprint kan worden (is met array gedaan zodat je ook nog worden zoals en etc. kan inserten indien gewenst)
    string += x

print(string)
