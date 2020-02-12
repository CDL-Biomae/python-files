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
    
def convert_list(list_converted):
    for i in range(len(list_converted)):
        if isinstance(list_converted[i],list):
            try : 
                list_converted[i][0] = float(list_converted[i][0])
            except :
                list_converted[i][0] = f'{list_converted[i][0]}'
        else :
            try : 
                list_converted[i] = float(list_converted[i])
            except :
                list_converted[i] = f'{list_converted[i]}'
            
    return list_converted

def get_unit(pack_id,sandre_list):
    return QueryScript(f"SELECT sandre, unit FROM analysis WHERE pack_id={pack_id} AND sandre IN {tuple(sandre_list)}").execute()

def data(pack_id):
    
    threshold_7j_metal = convert_list(QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly='Métaux' AND 7j_threshold IS NOT NULL").execute())
    threshold_21j_metal = convert_list(QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly='Métaux' AND 21j_threshold IS NOT NULL").execute())
    threshold_7j_organic = convert_list(QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 7j_threshold IS NOT NULL").execute())
    threshold_21j_organic = convert_list(QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 21j_threshold IS NOT NULL").execute())

    # print(threshold_7j_organic)
    sandre_list = convert_list(QueryScript("SELECT sandre FROM r3 WHERE sandre NOT IN ('/',1358,'') ORDER BY id").execute())
    sandre_output = []
    sandre_output.append(result_by_pack_and_sandre(pack_id,[element for element in sandre_list])) 
    total_output = []
    
    crustacean_list = []
    for element in elements_crustacean.keys() : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        crustacean_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(crustacean_list)
    
    fish_list = []
    for element in elements_fish.keys() : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        fish_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(fish_list)
    
    threshold_7j_metal_list = []
    for element in [el[0] for el in threshold_7j_metal] : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        threshold_7j_metal_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(threshold_7j_metal_list)
    
    threshold_7j_organic_list = []
    for element in [el[0] for el in threshold_7j_organic] : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        threshold_7j_organic_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(threshold_7j_organic_list)
    
    threshold_21j_metal_list = []
    for element in [el[0] for el in threshold_21j_metal] : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        threshold_21j_metal_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(threshold_21j_metal_list)
     
    threshold_21j_organic_list = []
    for element in [el[0] for el in threshold_21j_organic] : 
        try :
            index = [int(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        threshold_21j_organic_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(threshold_21j_organic_list)
    
    sandre_output_list = []
    for element in sandre_list : 

        try :
            index = [float(sandre[1]) for sandre in sandre_output[0]].index(element)
        except :
            index = "not found"
        sandre_output_list.append(sandre_output[0][index][0] if index != "not found" else "ND")
    total_output.append(sandre_output_list)
    
    
    return total_output