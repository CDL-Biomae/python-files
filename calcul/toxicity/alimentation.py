from tools import QueryScript
import env


class Alimentation:
    '''
    Permet le calcul de la survie alimentation (survie_alim) et de l'inhibition alimentaire (alimentation).
    Elles prennent toutes les deux un dictionnaire de point de mesures de fusion et renvoient le même complété par les résultats.
    '''

    @staticmethod
    def survie_alim(dict_pack_fusion):
        pack_dict = {}
        for element in dict_pack_fusion:
            try:
                pack_dict[dict_pack_fusion[element]['alimentation']] = element
            except KeyError:
                None
        survivor_list =  QueryScript(f"  SELECT pack_id, scud_survivor, scud_quantity, replicate   FROM {env.DATABASE_RAW}.cage WHERE pack_id IN {tuple([element for element in pack_dict])} AND scud_survivor IS NOT NULL").execute()
        result = {element:None for element in dict_pack_fusion}
        pack_checked = None
        current_quantity = None
        for cage in survivor_list:
            if pack_checked != cage[0]:
                if pack_checked:
                    result[pack_dict[pack_checked]]['average'] = sum([(result[pack_dict[pack_checked]]['replicate'][replicate]*2-current_quantity)/current_quantity*100 for replicate in result[pack_dict[pack_checked]]['replicate']])/len([replicate for replicate in result[pack_dict[pack_checked]]['replicate'] if replicate])
                pack_checked = cage[0]
                current_quantity = None
                if cage[2]:
                    current_quantity = cage[2]
                    result[pack_dict[pack_checked]] = {'replicate': {cage[3]: (cage[1]+current_quantity)/2}}
            else:
                result[pack_dict[pack_checked]]['replicate'][cage[3]] = (cage[1]+current_quantity)/2

        return result

    @staticmethod
    def alimentation(dict_pack_fusion):
        pack_dict = {}
        for element in dict_pack_fusion:
            try:
                pack_dict[dict_pack_fusion[element]['alimentation']] = element
            except KeyError:
                pass
        result = {element: None for element in dict_pack_fusion}

        ################### Calcul des tailles des spécimens
        specimen_size_data =  QueryScript(f"  SELECT pack_id, individual, size_px, size_mm   FROM {env.DATABASE_RAW}.measuresize WHERE pack_id IN {tuple([element for element in pack_dict])}").execute()
        specimen_size = {element:None for element in dict_pack_fusion}
        pack_checked = None
        ratio = None
        current_specimen_sample = []
        is_in_mm = False
        for size in specimen_size_data:
            if pack_checked != size[0]:
                if pack_checked and ratio:
                    specimen_size[pack_dict[pack_checked]] = [element*ratio for element in current_specimen_sample]
                elif pack_checked and is_in_mm:
                    specimen_size[pack_dict[pack_checked]] = [element for element in current_specimen_sample]
                pack_checked = size[0]
                ratio = None
                is_in_mm = False
                current_specimen_sample = []
                if size[1] == '0' and size[2]:
                    ratio = size[3]/size[2]
                else:
                    if size[3] and size[3] != 0:
                        is_in_mm = True
                        current_specimen_sample = [size[3]]
                    else:
                        current_specimen_sample = [size[2]]

            else:

                if size[1] == '0' and size[2]:
                    ratio = size[3]/size[2]
                else:
                    if size[3] and size[3] != 0 and not ratio:
                        is_in_mm = True
                        current_specimen_sample.append(size[3])
                    else:
                        current_specimen_sample.append(size[2])
        ############################################

        ############### Calcul des tailles feuilles ingérées

        standard_leaf_number = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de disques (témoin)' AND version=  {env.LATEST_VERSION()}").execute()[0]
        replicate_leaf_number = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de disques par réplicat' AND version=  {env.LATEST_VERSION()}").execute()[0]
        test_duration = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de jour du test' AND version=  {env.LATEST_VERSION()}").execute()[0]
        remaining_leaves_data =  QueryScript(f"  SELECT pack_id, replicate, value   FROM {env.DATABASE_RAW}.measureleaf WHERE pack_id IN {tuple([element for element in pack_dict])}").execute()
        remaining_leaves = {element:None for element in dict_pack_fusion}
        pack_checked = None
        for leaf in remaining_leaves_data:
            pack_checked = leaf[0]
            if remaining_leaves[pack_dict[pack_checked]]:
                if leaf[1] in remaining_leaves[pack_dict[pack_checked]]:
                    remaining_leaves[pack_dict[pack_checked]][leaf[1]] += leaf[2]
                else:
                    remaining_leaves[pack_dict[pack_checked]][leaf[1]] = leaf[2]

            else:
                remaining_leaves[pack_dict[pack_checked]]= {leaf[1]:leaf[2]}

        ##### Conversion pixel restants -> mm2 consommées par individu par jour
        survivor = Alimentation.survie_alim(dict_pack_fusion)
        eaten_leaves = {element: None for element in dict_pack_fusion}
        for element in remaining_leaves:
            if remaining_leaves[element] and survivor[element]['replicate']:
                replicate_raw_value = remaining_leaves[element][0]/standard_leaf_number*replicate_leaf_number if 0 in remaining_leaves[element] else None
                eaten_leaves[element] = {replicate: (replicate_raw_value - remaining_leaves[element][replicate])/test_duration/survivor[element]['replicate'][replicate]*0.0071 if replicate in survivor[element]['replicate'] and replicate_raw_value and replicate in remaining_leaves[element] else None for replicate in survivor[element]['replicate']}


        ###################################################


        ##################### Calcul de l'inhibition alimentaire
        inhibition = {element:None for element in dict_pack_fusion}
        constant_alim = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name LIKE 'Constante alim%'").execute()
        average_temperature = {element:None for element in dict_pack_fusion}
        average_temperature_output = QueryScript(f" SELECT measurepoint_fusion_id, sensor1_average   FROM {env.DATABASE_TREATED}.average_temperature WHERE measurepoint_fusion_id IN {tuple(dict_pack_fusion)} AND version=  {env.LATEST_VERSION()}").execute()
        for element in average_temperature_output:
            average_temperature[element[0]] = element[1]
        for element in dict_pack_fusion:
            mean_size = None
            if specimen_size[element]:

                mean_size = sum([specimen if specimen else 0 for specimen in specimen_size[element]])/len([specimen if specimen else 0 for specimen in specimen_size[element]])
                if average_temperature[element]:
                    expected_eaten_value = constant_alim[0] * average_temperature[element] + constant_alim[1] + constant_alim[2] * ( mean_size - constant_alim[3])
                    if eaten_leaves[element]:
                        inhibition_list = [(eaten_leaves[element][replicate] - expected_eaten_value) /expected_eaten_value if eaten_leaves[element][replicate] != None else None for replicate in eaten_leaves[element]]
                        sorted_inhibition_list = []
                        for replicate in inhibition_list:
                            if replicate:
                                sorted_inhibition_list.append(replicate)
                        if len(sorted_inhibition_list):
                            inhibition[element] = sum(sorted_inhibition_list)/len(sorted_inhibition_list)*100

        return inhibition
