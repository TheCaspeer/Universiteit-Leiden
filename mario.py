# Naam: Casper Juffermans
# Studentnummer: s4270118

hoogte = "x"

while True:
    inputVal = input("Hoe hoog wil je het hebben?\n(een waarde tussen 1 en 23)\n")
    try:
        val = int(inputVal)
        if(1<val<=23): 
            hoogte=val
            break
        else:
            print(f"De waarde die je hebt ingevuld ({val}) is geen correcte waarde.\nVul een waarde in tussen 1 en 23")
    except: # zorgt dat als een getal dat geen integer kan worden (float, string etc.) ingevuld wordt dat die een specifiek bericht stuurt
        print(f"De waarde die je hebt ingevuld ({inputVal}) is geen geheel getal.\nVul alsjeblieft een geheel getal in\n")
print(f"Je hebt succesvol een hoogte van {hoogte} ingevuld")

message="" # init een lege message voor modification

width = hoogte + 1 # +1 zodat je dat ene vlakke stukje krijgt
empty = "  " # whitespace zodat de trap van links naar rechts gaat

for x in range(hoogte): # zorgt dat je bovenaan begint
    # print(x+1) debug value, de +1 is om te compenseren voor index0
    for a in range(0,(width-(x+1))): # zorgt dat er width-(inverse hoogte+1)
        message += empty 
    for b in range(0,(x+2)): # print inverse hoogte + 1 extra blokje
        message += "# "

    message += "\n" 


print(f"\n{message}")


    