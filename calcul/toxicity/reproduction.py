from tools import QueryScript
from math import *


def female_survivor(pack_id):
    SQL_request = "SELECT scud_survivor_female,scud_quantity FROM cage where pack_id="+str(pack_id)+" and scud_survivor_female is not null "
    f_survivor = []
    quantity =[]
    resultat =  QueryScript(SQL_request).execute()
    for element in resultat :
            f_survivor.append(element[0])
            quantity.append(element[1])

    if sum(f_survivor) == None:
        return "NA"
    else:
        return round(sum(f_survivor)/len(f_survivor)/quantity[0]*100)

    






   
    
 



 