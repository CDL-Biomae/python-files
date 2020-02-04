from tools import QueryScript
from . import result_by_pack_and_sandre, elements_fish, elements_crustacean

threshold_7j_metal = QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly='Métaux' AND 7j_threshold IS NOT NULL").execute()
threshold_21j_metal = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly='Métaux' AND 21j_threshold IS NOT NULL").execute()
threshold_7j_organic = QueryScript("SELECT sandre, parameter, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 7j_threshold IS NOT NULL").execute()
threshold_21j_organic = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 21j_threshold IS NOT NULL").execute()

sandre_list = QueryScript("SELECT sandre FROM r3").execute()

def report_data(pack_id):
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
    # annexes = []
    # for element in sandre_list:
    #     annexes.append(result_by_pack_and_sandre(pack_id,element))
    # output.append(annexes)
    
    return output