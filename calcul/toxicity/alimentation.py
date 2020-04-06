from tools import QueryScript
import env


class Alimentation:
    '''
    Permet le calcul de la survie alimentation (survie_alim) et de l'inhibition alimentaire (alimentation).
    Elles prennent toutes les deux un dictionnaire de point de mesures de fusion et renvoient le même complété par les résultats.
    '''

    @staticmethod
    def survie_alim(dict_pack):
        pack_dict = {}
        for element in dict_pack:
            try:
                pack_dict[dict_pack[element]['alimentation']] = element
            except KeyError:
                None
        survivor_list =  QueryScript(f"  SELECT pack_id, scud_survivor, scud_quantity, replicate   FROM {env.DATABASE_RAW}.Cage WHERE pack_id IN {tuple([element for element in pack_dict])} AND scud_survivor IS NOT NULL").execute()
        result = {element:None for element in dict_pack}
        pack_checked = None
        current_quantity = None
        for pack_id, scud_survivor, scud_quantity, replicate in survivor_list:
            if pack_checked != pack_id:
                if pack_checked:
                    result[pack_dict[pack_checked]]['average'] = sum([(result[pack_dict[pack_checked]]['replicate'][replicate]*2-current_quantity)/current_quantity*100 for replicate in result[pack_dict[pack_checked]]['replicate']])/len([replicate for replicate in result[pack_dict[pack_checked]]['replicate'] if replicate])
                pack_checked = pack_id
                current_quantity = None
                if scud_quantity:
                    current_quantity = scud_quantity
                    result[pack_dict[pack_checked]] = {'replicate': {replicate: (scud_survivor+current_quantity)/2}}
            else:
                result[pack_dict[pack_checked]]['replicate'][replicate] = (scud_survivor+current_quantity)/2

        return result

    @staticmethod
    def alimentation(dict_pack):
        pack_dict = {}
        for element in dict_pack:
            try:
                pack_dict[dict_pack[element]['alimentation']] = element
            except KeyError:
                pass
        result = {element: None for element in dict_pack}

        ################### Calcul des tailles des spécimens
        specimen_size_data =  QueryScript(f"  SELECT pack_id, individual, size_px, size_mm   FROM {env.DATABASE_RAW}.MeasureSize WHERE pack_id IN {tuple([element for element in pack_dict])}").execute()
        specimen_size = {element:None for element in dict_pack}
        pack_checked = None
        ratio = None
        current_specimen_sample = []
        is_in_mm = False
        for pack_id, individual, size_px, size_mm in specimen_size_data:
            if pack_checked != pack_id:
                if pack_checked and ratio:
                    specimen_size[pack_dict[pack_checked]] = [element*ratio for element in current_specimen_sample]
                elif pack_checked and is_in_mm:
                    specimen_size[pack_dict[pack_checked]] = [element for element in current_specimen_sample]
                pack_checked = pack_id
                ratio = None
                is_in_mm = False
                current_specimen_sample = []
                if individual == '0' and size_px:
                    ratio = size_mm/size_px
                else:
                    if size_mm and size_mm != 0:
                        is_in_mm = True
                        current_specimen_sample = [size_mm]
                    else:
                        current_specimen_sample = [size_px]

            else:

                if individual == '0' and size_px:
                    ratio = size_mm/size_px
                else:
                    if size_mm and size_mm != 0 and not ratio:
                        is_in_mm = True
                        current_specimen_sample.append(size_mm)
                    else:
                        current_specimen_sample.append(size_px)
        ############################################

        ############### Calcul des tailles feuilles ingérées

        standard_leaf_number = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de disques (témoin)' AND version=  {env.LATEST_VERSION()}").execute()[0]
        replicate_leaf_number = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de disques par réplicat' AND version=  {env.LATEST_VERSION()}").execute()[0]
        test_duration = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='Nombre de jour du test' AND version=  {env.LATEST_VERSION()}").execute()[0]
        remaining_leaves_data =  QueryScript(f"  SELECT pack_id, replicate, value   FROM {env.DATABASE_RAW}.MeasureLeaf WHERE pack_id IN {tuple([element for element in pack_dict])}").execute()
        remaining_leaves = {element:None for element in dict_pack}
        pack_checked = None
        for pack_id, replicate, value in remaining_leaves_data:
            pack_checked = pack_id
            if remaining_leaves[pack_dict[pack_checked]]:
                if replicate in remaining_leaves[pack_dict[pack_checked]]:
                    remaining_leaves[pack_dict[pack_checked]][replicate] += value
                else:
                    remaining_leaves[pack_dict[pack_checked]][replicate] = value

            else:
                remaining_leaves[pack_dict[pack_checked]]= {replicate:value}

        ##### Conversion pixel restants -> mm2 consommées par individu par jour
        survivor = Alimentation.survie_alim(dict_pack)
        eaten_leaves = {element: None for element in dict_pack}
        for element in remaining_leaves:
            if remaining_leaves[element] and survivor[element]['replicate']:
                replicate_raw_value = remaining_leaves[element][0]/standard_leaf_number*replicate_leaf_number if 0 in remaining_leaves[element] else None
                eaten_leaves[element] = {replicate: (replicate_raw_value - remaining_leaves[element][replicate])/test_duration/survivor[element]['replicate'][replicate]*0.0071 if replicate in survivor[element]['replicate'] and replicate_raw_value and replicate in remaining_leaves[element] else None for replicate in survivor[element]['replicate']}


        ###################################################


        ##################### Calcul de l'inhibition alimentaire
        inhibition = {element:None for element in dict_pack}
        constant_alim = QueryScript(
            f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name LIKE 'Constante alim%'").execute()
        average_temperature = {element:None for element in dict_pack}
        average_temperature_output = QueryScript(f" SELECT measurepoint_id, sensor1_average   FROM {env.DATABASE_TREATED}.average_temperature WHERE measurepoint_id IN {tuple(dict_pack)} AND version=  {env.LATEST_VERSION()}").execute()
        for measurepoint_id, sensor1_average in average_temperature_output:
            average_temperature[measurepoint_id] = sensor1_average
        for measurepoint_id in dict_pack:
            mean_size = None
            if specimen_size[measurepoint_id]:

                mean_size = sum([specimen if specimen else 0 for specimen in specimen_size[measurepoint_id]])/len([specimen if specimen else 0 for specimen in specimen_size[measurepoint_id]])
                if average_temperature[measurepoint_id]:
                    expected_eaten_value = constant_alim[0] * average_temperature[measurepoint_id] + constant_alim[1] + constant_alim[2] * ( mean_size - constant_alim[3])
                    if eaten_leaves[measurepoint_id]:
                        inhibition_list = [(eaten_leaves[measurepoint_id][replicate] - expected_eaten_value) /expected_eaten_value if eaten_leaves[measurepoint_id][replicate] != None else None for replicate in eaten_leaves[measurepoint_id]]
                        sorted_inhibition_list = []
                        for replicate in inhibition_list:
                            if replicate:
                                sorted_inhibition_list.append(replicate)
                        if len(sorted_inhibition_list):
                            inhibition[measurepoint_id] = sum(sorted_inhibition_list)/len(sorted_inhibition_list)*100

        return inhibition
