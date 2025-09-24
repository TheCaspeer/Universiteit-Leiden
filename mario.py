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

width_total = hoogte + 1

for x in range(1,hoogte):
    # x is hier het niveau, vanaf boven getelt
    width_blocks = 1+x 
    width_empty = width_total - width_blocks - 1 # -1 to offset extra whitespace
    for empty_tile in range(width_empty):
        message += empty
    for block in range(width_blocks-1):
        message += "# " # whitespace after hash to prevent cluttering
    message += "#" # los van de bovenste forloop, hierdoor is er rechts van de pyramide geen whitespace
    
    if(x != hoogte): # voorkomt dat bij de laatste rij er nog een witregel onder komt
        message += "\n" 

print(f"\n{message}")





    