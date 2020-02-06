from tools import QueryScript
from . import result_by_pack_and_sandre, elements_fish, elements_crustacean


def lyophilisation_pourcent(pack_id):
    output = QueryScript(f"SELECT prefix, value, unit FROM analysis WHERE sandre='/' AND pack_id={pack_id}").execute()
    if len(output) :
        return f"{output[0][0]}{output[0][1]}{output[0][2]}"
    else :
        return None

def fat(pack_id):
    output = QueryScript(f"SELECT prefix, value, unit FROM analysis WHERE sandre=1358 AND pack_id={pack_id}").execute()
    if len(output) :
        return f"{output[0][0] if output[0][0] else ''}{output[0][1] * 100}{output[0][2]}"
    else :
        return None
    
def weight(pack_id):
    output = QueryScript(f"SELECT sampling_weight, metal_tare_bottle_weight, sampling_quantity, organic_tare_bottle_weight, organic_total_weight FROM pack WHERE id={pack_id}").execute()
    if len(output):
        return [output[0][0]-output[0][1], (output[0][0]-output[0][1])/output[0][2], output[0][4]-output[0][3]]
    else :
        return None
def survival(pack_id):
    survival_list = QueryScript(f"SELECT scud_quantity, scud_survivor FROM cage WHERE pack_id={pack_id} AND scud_survivor IS NOT NULL").execute()
    if len(survival_list):
        quantity = survival_list[0][0]
        average = 0
        for replicate in survival_list:
            average += replicate[1]
        average = average / len(survival_list)
        return str(average / quantity * 100) +'%'
    else:
        return None

def data(pack_id):
    
    threshold_7j_metal = QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly='Métaux' AND 7j_threshold IS NOT NULL").execute()
    threshold_21j_metal = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly='Métaux' AND 21j_threshold IS NOT NULL").execute()
    threshold_7j_organic = QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 7j_threshold IS NOT NULL").execute()
    threshold_21j_organic = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 21j_threshold IS NOT NULL").execute()

    sandre_list = QueryScript("SELECT sandre FROM r3 WHERE sandre NOT IN ('/',1358)").execute()
    output = []
    # Crustacés
    crustaceans = []
    for element in elements_crustacean:
        crustaceans.append(result_by_pack_and_sandre(pack_id,element))
    output.append(crustaceans) 
        
    # fish
    fishes = []
    for element in elements_fish:
        fishes.append(result_by_pack_and_sandre(pack_id,element))
    output.append(fishes) 
        
    # Métaux 7j
    metal_7j = []
    for element in threshold_7j_metal:
        metal_7j.append(result_by_pack_and_sandre(pack_id,element[0]))
    output.append(metal_7j) 
    
    # Organique 7j
    organic_7j = []
    for element in threshold_7j_organic:
        organic_7j.append(result_by_pack_and_sandre(pack_id,element[0]))
    output.append(organic_7j) 
    
    # Métaux 21j
    metal_21j = []
    for element in threshold_21j_metal:
        metal_21j.append(result_by_pack_and_sandre(pack_id,element[0]))
    output.append(metal_21j) 
    
    # Organique 21j
    organic_21j = []
    for element in threshold_21j_organic:
        organic_21j.append(result_by_pack_and_sandre(pack_id,element[0]))
    output.append(organic_21j) 
    
    # Annexes
    annexes = []
    for element in sandre_list:
        annexes.append(result_by_pack_and_sandre(pack_id,element))
    output.append(annexes)
    
    return output