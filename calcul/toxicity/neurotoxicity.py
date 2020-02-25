from tools import QueryScript

def neurotoxicity(dict_pack_fusion):
    
    constant_AChE = QueryScript(
        "SELECT value FROM r2_constant WHERE name LIKE 'Constante ache%'").execute()

    pack_dict = {}
    for element in dict_pack_fusion:
        try:
            pack_dict[dict_pack_fusion[element]['neurology']] = element 
        except KeyError:
            None 
    output =  QueryScript(f"SELECT pack_id, ache, weight FROM cage WHERE pack_id IN {tuple([element for element in pack_dict])}").execute()
    result = {element:None for element in dict_pack_fusion}
    
    pack_checked = None
    for cage in output:
        if not result[pack_dict[cage[0]]] and cage[1]:
            result[pack_dict[cage[0]]] = {'ache':[cage[1]], 'weight':[cage[2]]}
        elif cage[1] :
            result[pack_dict[cage[0]]]['ache'].append(cage[1])
            result[pack_dict[cage[0]]]['weight'].append(cage[2])
    
    for element in result:
        if result[element]:
            mean_AChE = sum(result[element]['ache'])/len(result[element]['ache'])
            mean_weight = sum(result[element]['weight'])/len(result[element]['weight'])
            AChE_expected = constant_AChE[0] + constant_AChE[1] * ( mean_weight ** constant_AChE[2] )
            result[element] = ( mean_AChE - AChE_expected ) / AChE_expected * 100
            

    return result