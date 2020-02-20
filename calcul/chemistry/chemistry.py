from tools import QueryScript
from . import elements_fish, elements_crustacean


def lyophilisation_pourcent(pack_id):
    output = QueryScript(f"SELECT prefix, value, unit FROM analysis WHERE sandre='/' AND pack_id={pack_id}").execute()
    if len(output):
        return f"{output[0][0]}{output[0][1]}{output[0][2]}"
    else:
        return None

def fat(pack_id):
    output = QueryScript(f"SELECT prefix, value, unit FROM analysis WHERE sandre=1358 AND pack_id={pack_id}").execute()
    if len(output):
        return f"{output[0][0] if output[0][0] else ''}{output[0][1] * 100}{output[0][2]}"
    else:
        return None
    
def weight(pack_id):
    output = QueryScript(f"SELECT sampling_weight, metal_tare_bottle_weight, sampling_quantity, organic_tare_bottle_weight, organic_total_weight FROM pack WHERE id={pack_id}").execute()
    if len(output):
        return [output[0][0]-output[0][1], (output[0][0]-output[0][1])/output[0][2], output[0][4]-output[0][3]]
    else:
        return None
    
def survival(pack_id):
    if pack_id is None:
        return None

    survival_list = QueryScript(f"SELECT scud_quantity, scud_survivor FROM cage WHERE pack_id={pack_id} AND scud_survivor IS NOT NULL").execute()
    if len(survival_list):
        quantity = survival_list[0][0]
        average = 0
        for replicate in survival_list:
            average += replicate[1]
        average = average / len(survival_list)
        return str(round(average / quantity * 100)) + '%'
    else:
        return None
    
def convert_list(list_converted):
    for element in list_converted:
        if isinstance(list_converted[i], list):
            try:
                element[0] = float(element[0])
            except:
                element[0] = f'{element[0]}'
        else:
            try:
                element = float(element)
            except:
                element = f'{element}'
            
    return list_converted

def get_unit_NQE(sandre_list):
    output = QueryScript(f"SELECT familly, sandre, NQE FROM r3 WHERE sandre IN {tuple(sandre_list)}").execute()
    result=[[],[],[]]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre==int(float(element[1])):
                    if element[0]=='Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2]) if element[2]!='' else '')
                        
                    else :
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2]) if element[2]!='' else '')
    return result

def get_unit(sandre_list):
    output = QueryScript(f"SELECT familly, sandre FROM r3 WHERE sandre IN {tuple(sandre_list)}").execute()
    result=[[],[]]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre==int(float(element[1])):
                    if element[0]=='Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))

                    else :
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
    return result

def result_by_pack_and_sandre(pack_id, sandre_list) :
    result = [[],[]]
    output = QueryScript(f"SELECT prefix, value, sandre FROM analysis WHERE pack_id={pack_id} AND sandre IN {tuple(sandre_list)}").execute()

    for sandre in sandre_list:
        try :
            index = [int(element[2]) for element in output].index(sandre)
            result[0].append(str(output[index][1]) if output[index][0]==None else output[index][0] + str(output[index][1]))
            result[1].append(output[index][2])
        except :
            result[0].append("ND")
            result[1].append(sandre)
           
    return result