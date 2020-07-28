from tools import QueryScript
from . import elements_fish, elements_crustacean
import env


def survival(pack_list):
    '''
    Crée un dictionnaire avec comme clé le pack_id et comme valeur sa survie chimie.
    :param pack_list:
    :return: pack_dict:
    '''
    if len(pack_list)==0 :
        return None

    survival_list = QueryScript(
        f"  SELECT pack_id, scud_quantity, scud_survivor FROM {env.DATABASE_RAW}.Cage WHERE pack_id IN {tuple(pack_list) if len(pack_list)>1 else '('+(str(pack_list[0]) if len(pack_list) else '0')+')'} AND scud_survivor IS NOT NULL AND nature='chemistry'").execute()
    
    pack_dict = {}
    for pack_id, quantity, survivor in survival_list:
        if pack_id in pack_dict:
            if quantity and survivor!=None :
                pack_dict[pack_id].append(survivor/quantity)
        else :
            if quantity and survivor!=None :
                pack_dict[pack_id]= [survivor/quantity]
    for pack_id in pack_dict :
        pack_dict[pack_id] = str(round(sum(pack_dict[pack_id])/len(pack_dict[pack_id])*100)) + '%'
    return pack_dict
    

def get_unit_NQE(sandre_list):
    '''
    Crée trois listes qui sont respectivement celle des unités(µg/kg PF ou mg/kg PF), celle des code sandre et enfin celle des seuils NQE à partir d'une liste de code sandre
    :param sandre_list:
    :return: [[unit_list],[sandre_list],[NQE_list]]:
    '''
    output = QueryScript(
        f" SELECT familly, sandre, NQE   FROM {env.DATABASE_TREATED}.r3 WHERE sandre IN {tuple(sandre_list) if len(sandre_list)>1 else '('+(str(sandre_list[0]) if len(sandre_list) else '0')+')'} AND version=  {env.CHOSEN_VERSION()}").execute()
    result = [[], [], []]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre == int(float(element[1])):
                    if element[0] == 'Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2])
                                         if element[2] != '' else '')

                    else:
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2])
                                         if element[2] != '' else '')
    return result


def get_unit(sandre_list):
    '''
    Crée trois listes qui sont respectivement celle des unités(µg/kg PF ou mg/kg PF) et celle des code sandre à partir d'une liste de code sandre
    :param sandre_list:
    :return: [[unit_list],[sandre_list]]:
    '''
    output = QueryScript(
        f" SELECT familly, sandre   FROM {env.DATABASE_TREATED}.r3 WHERE sandre IN {tuple(sandre_list) if len(sandre_list)>1 else '('+(str(sandre_list[0]) if len(sandre_list) else '0')+')'} AND version=  {env.CHOSEN_VERSION()}").execute()
    result = [[], []]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre == int(float(element[1])):
                    if element[0] == 'Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))

                    else:
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
    return result


def result(campaigns_dict, pack_list):
    '''
    Crée un dictionnaire des résultats par code sandre regroupé par point de mesure à partir du dictionnaire global de campagne et la liste des packs chimie
    :param campaigns_dict, pack_list:
    :return: result_dict:
    '''
    sandre_list = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()}").execute()
    for index, sandre in enumerate(sandre_list):
        try:
            sandre_list[index] = int(float(sandre))
        except ValueError :
            pass
    data = QueryScript(f"SELECT pack_id, prefix, value, sandre FROM {env.DATABASE_RAW}.Analysis WHERE pack_id IN {tuple(pack_list) if len(pack_list)>1 else '('+(str(pack_list[0]) if len(pack_list) else '0')+')'} AND sandre IN {tuple(sandre_list) if len(sandre_list)>1 else '('+(str(sandre_list[0]) if len(sandre_list) else '0')+')'}").execute()
    result_dict = {}
    for campaign_id in campaigns_dict:
        for place_id in campaigns_dict[campaign_id]["place"]:
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for pack_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"]:
                    if pack_id in pack_list :
                        for pack, prefix, value, sandre in data :
                            if pack==int(pack_id):
                                try :
                                    sandre = int(float(sandre))
                                except ValueError:
                                    pass
                                if not measurepoint_id in result_dict:
                                    result_dict[measurepoint_id] = {sandre : prefix + str(value) if prefix else str(value)}
                                else :
                                    result_dict[measurepoint_id][sandre] = prefix + str(value) if prefix else str(value) 
    return result_dict