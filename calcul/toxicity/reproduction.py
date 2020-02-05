from tools import QueryScript


def female_survivor(pack_id):
    SQL_request = "SELECT scud_survivor_female,scud_quantity FROM cage where pack_id="+str(pack_id)+" and scud_survivor_female !='null' "
    f_survivor = []
    quantity =[]
    resultat =  QueryScript(SQL_request).execute()
    for i in range(len(resultat)) :
            f_survivor.append(resultat[i][0])
            quantity.append(resultat[i][1])

    if sum(f_survivor) == None:
        return "NA"
    else:
        return sum(f_survivor)/len(f_survivor)/quantity[0]*100

    






   
    
 



 