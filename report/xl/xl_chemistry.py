from tools import translate
import pandas as pd
import env
import json

def create_chemistry_dataframe(context_data, main_data, analysis_data, chemical_threshold_data, context_threshold_data):
    global_matrix = []
    report_dict = {}
    for measurepoint_id, pack_id, reference, start_date, end_date, name, agency_code, network, hydroecoregion, sensor3_min, sensor3_average, sensor3_max, sampling_weight, metal_tare_bottle_weight, organic_tare_bottle_weight, organic_total_weight, quantity,t0_reference, t0_sampling_weight, t0_metal_tare_bottle_weight, t0_organic_tare_bottle_weight, t0_organic_total_weight, t0_quantity, survival_percent in main_data:
        contract = reference.split('-')[0]
        if not contract in report_dict :
            report_dict[contract] = {
                'count':1,
                'survival_under_25_percent' : 0,
                'survival_under_50_percent' : 0,
                'vandalism' : 0,
                'out_of_water' : 0,
                'out_of_water_up_50_percent' : 0,
                'out_of_water_under_50_percent' : 0,
                'survival_under_25_percent_not_conform':0,
                'survival_under_25_percent_conform_preferred':0,
                'survival_under_25_percent_conform_compulsory':0,
                'not_totally_analysed':0,
                'survival_null':0
            }
        else :
            report_dict[contract]['count'] += 1
        
        context_preferred_exceeded = False
        context_compulsory_exceeded = False
        vandalism = False
        out_of_water = False
        context_exceeded_list = []
        comment_list = []
        if sensor3_max and sensor3_max>21 :
            context_exceeded_list.append('Température haute')
            context_compulsory_exceeded = True
        if end_date and start_date :
            chemistry_duration = "21j" if (end_date-start_date).days > 14 else "7j"
        for mp_id, recordedAt, temperature, conductivity, oxygen, pH, barrel, comment in context_data:
            comment = translate(comment)
            if mp_id==measurepoint_id and barrel and barrel[0]=='R':
                if comment :
                    if not comment.find('andalisme')==-1 and 'Vandalisme' not in comment_list :
                        comment_list.append('Vandalisme')
                        vandalism = True
                    if (not comment.find('vol')==-1 or not comment.find('Vol')==-1)  and 'Vol' not in comment_list :
                        comment_list.append('Vol')
                        vandalism = True
                    if not comment.find('ystème non récupérable')==-1 and 'Système non récupérable' not in comment_list :
                        comment_list.append('Système non récupérable')
                        vandalism = True
                    if not comment.find("ors d'eau")==-1 and "Hors d'eau" not in comment_list :
                        comment_list.append("Hors d'eau")
                        out_of_water = True
                if temperature :
                    for threshold_name, _min, _max in context_threshold_data :
                        if threshold_name=='Température moyenne (chimie)':
                            if _min > temperature and not 'Température basse' in context_exceeded_list:
                                context_exceeded_list.append('Température basse')
                                context_preferred_exceeded = True
                            if _max < temperature and not 'Température haute' in context_exceeded_list :
                                context_exceeded_list.append('Température haute')
                                context_preferred_exceeded = True
                if conductivity :
                    for threshold_name, _min, _max in context_threshold_data :
                        if threshold_name=='Conductivité (chimie)':
                            if 100 > conductivity and not 'Conductivité basse' in context_exceeded_list:
                                context_exceeded_list.append('Conductivité basse')
                                if 50 > conductivity :
                                    context_compulsory_exceeded = True
                                else :
                                    context_preferred_exceeded = True
                            if _max < conductivity and not 'Conductivité haute' in context_exceeded_list :
                                context_exceeded_list.append('Conductivité haute')
                                context_preferred_exceeded = True
                if pH :
                    for threshold_name, _min, _max in context_threshold_data :
                        if threshold_name=='pH (chimie)':
                            if _min > pH and not 'pH bas' in context_exceeded_list:
                                context_exceeded_list.append('pH bas')
                                context_compulsory_exceeded = True
                            if _max < pH and not 'pH haut' in context_exceeded_list :
                                context_exceeded_list.append('pH haut')
                                context_compulsory_exceeded = True
                if oxygen :
                    for threshold_name, _min, _max in context_threshold_data :
                        if threshold_name=='Oxygène (chimie)':
                            if 7.5 > oxygen and not 'Oxygène bas' in context_exceeded_list:
                                context_exceeded_list.append('Oxygène bas')
                                if 5 > oxygen :
                                    context_compulsory_exceeded = True
                                else :
                                    context_preferred_exceeded = True
                if recordedAt==start_date :
                    temperatureJ0 = temperature
                    oxygenJ0 = oxygen
                    pHJ0 = pH
                    conductivityJ0 = conductivity
                if recordedAt==end_date :
                    temperatureJ21 = temperature
                    oxygenJ21 = oxygen
                    pHJ21 = pH
                    conductivityJ21 = conductivity
        metal_element = []
        organic_element = []
        for packId, value, sandre_analysis, element_name in analysis_data:
            if pack_id==packId :
                for sandre_threshold, familly,  graduate_50_7j, graduate_50_21j in chemical_threshold_data :
                    if sandre_analysis==sandre_threshold :
                        if chemistry_duration == "21j" and graduate_50_21j and value > graduate_50_21j :
                            metal_element.append(translate(element_name)) if familly == 'Métaux' else organic_element.append(translate(element_name))
                        if chemistry_duration == "7j" and graduate_50_7j and value > graduate_50_7j :
                            metal_element.append(translate(element_name)) if familly == 'Métaux' else organic_element.append(translate(element_name))
        if survival_percent and survival_percent > 1:
            if survival_percent > 25 :
                if survival_percent < 50 :
                    report_dict[contract]['survival_under_50_percent'] += 1
                    if out_of_water :
                        report_dict[contract]['out_of_water_under_50_percent'] += 1
                elif out_of_water :
                    report_dict[contract]['out_of_water_up_50_percent'] += 1

            else :
                report_dict[contract]['survival_under_25_percent'] += 1
                if not context_preferred_exceeded and not context_compulsory_exceeded:
                    report_dict[contract]['survival_under_25_percent_conform_preferred'] += 1
                elif context_preferred_exceeded and not context_compulsory_exceeded:
                    report_dict[contract]['survival_under_25_percent_conform_compulsory'] += 1
                else :
                    report_dict[contract]['survival_under_25_percent_not_conform'] += 1
        else :
            report_dict[contract]['survival_null'] += 1
            if out_of_water :
                report_dict[contract]['out_of_water'] += 1
            elif vandalism :
                report_dict[contract]['vandalism'] += 1

        if organic_tare_bottle_weight and organic_total_weight :
            if (organic_total_weight-organic_tare_bottle_weight) <2000 :
                report_dict[contract]['not_totally_analysed'] += 1



        temp = [measurepoint_id, reference, start_date.strftime("%d/%m/%Y") if start_date else None, contract, int(reference.split('-')[1]) if reference.split('-')[1][0]=='0' else int(reference.split('-')[2]), int(reference.split('-')[2]), translate(name), agency_code, sensor3_min, sensor3_average, sensor3_max, max([temperatureJ0 if temperatureJ0 else 0, temperatureJ21 if temperatureJ21 else 0]) if temperatureJ0 or temperatureJ21 else 'NA', (str(round(survival_percent))+'%') if survival_percent and  survival_percent > 1  else 'Non analysé', ', '.join(context_exceeded_list), ', '.join(comment_list), ', '.join(metal_element),', '.join(organic_element),network, hydroecoregion, temperatureJ0, temperatureJ21, conductivityJ0, conductivityJ21, oxygenJ0, oxygenJ21, pHJ0, pHJ21, metal_tare_bottle_weight, sampling_weight, (sampling_weight-metal_tare_bottle_weight) if sampling_weight and metal_tare_bottle_weight else "NA", quantity, '', organic_tare_bottle_weight, organic_total_weight, (organic_total_weight-organic_tare_bottle_weight) if organic_tare_bottle_weight and organic_total_weight else 'NA', '', t0_reference, t0_metal_tare_bottle_weight, t0_sampling_weight, (t0_sampling_weight-t0_metal_tare_bottle_weight) if t0_metal_tare_bottle_weight and t0_sampling_weight else 'NA', t0_organic_tare_bottle_weight, t0_organic_total_weight, (t0_organic_total_weight-t0_organic_tare_bottle_weight) if t0_organic_tare_bottle_weight and t0_organic_total_weight else 'NA', t0_quantity]
        global_matrix.append(temp)
    df = pd.DataFrame(global_matrix, columns=['#', 'Code BIOMÆ', 'Jour de lancement',	'Bassin', 'Contrat', 'Campagne', 'Station de mesure', 'Code Agence', 'Température min sonde (°C)', 'Température Moyenne sonde (°C)', 'Température max sonde (°C)', 'Température max ponctuelle (°C)', 'Taux de survie (exprimé en %)', "Hors domaine d'application", "Problème d'expérimentation", "Métaux (Fort à très fort)",	"Composés organiques (Fort à très fort)", 'Type de réseau',	'Hydroécorégion', 'Température T+0 - Encagement sur site', 'Température T+21 - Site > Récupération', 'Conductivité T+0 - Encagement sur site', 'Conductivité T+21 - Site > Récupération', 'Oxygène T+0 - Encagement sur site', 'Oxygène T+21 - Site > Récupération', 'pH T+0 - Encagement sur site', 'pH T+21 - Site > Récupération', 'Tare échantillon métaux (mg)','Masse totale échantillon métaux (mg)', 'Masse Fraiche métaux (mg)', "Nombre de gammares dans l'echantillon", 'Poids moyen (mg)', 'Tare échantillon organiques (mg, sans bouchon)', 'Masse totale échantillon organiques (mg, sans bouchon)', 'Masse fraiche organiques (mg)', 'Poids moyen avant expo (contrôle)', 'Libellé T0', 'Tare échantillon métaux (mg)', 'Masse totale échantillon métaux (mg)', 'Masse Fraiche métaux (mg)', 'Tare échantillon organiques (mg, sans bouchon)', 'Masse totale échantillon organiques (mg, sans bouchon)',	'Masse fraiche organiques (mg)', "Nombre de gammares dans l'echantillon métaux"])
    
    report_dict['TOTAL'] = {
        'count':sum([report_dict[key]['count'] for key in list(report_dict.keys())]),
        'survival_under_25_percent' : sum([report_dict[key]['survival_under_25_percent'] for key in list(report_dict.keys())]),
        'survival_under_50_percent' : sum([report_dict[key]['survival_under_50_percent'] for key in list(report_dict.keys())]),
        'vandalism' : sum([report_dict[key]['vandalism'] for key in list(report_dict.keys())]),
        'out_of_water' : sum([report_dict[key]['out_of_water'] for key in list(report_dict.keys())]),
        'out_of_water_under_50_percent' : sum([report_dict[key]['out_of_water_under_50_percent'] for key in list(report_dict.keys())]),
        'out_of_water_up_50_percent' : sum([report_dict[key]['out_of_water_up_50_percent'] for key in list(report_dict.keys())]),
        'survival_under_25_percent_not_conform':sum([report_dict[key]['survival_under_25_percent_not_conform'] for key in list(report_dict.keys())]),
        'survival_under_25_percent_conform_preferred':sum([report_dict[key]['survival_under_25_percent_conform_preferred'] for key in list(report_dict.keys())]),
        'survival_under_25_percent_conform_compulsory':sum([report_dict[key]['survival_under_25_percent_conform_compulsory'] for key in list(report_dict.keys())]),
        'not_totally_analysed':sum([report_dict[key]['not_totally_analysed'] for key in list(report_dict.keys())]),
        'survival_null':sum([report_dict[key]['survival_null'] for key in list(report_dict.keys())])
    }

    with open('data.json','w') as outfile :
        json.dump(report_dict, outfile)
    


    report_matrix = []
    report_matrix = add_new_section(report_matrix, "Bilan", report_dict.keys())
    survival_under_25_percent_row = ["Survie inférieure à 25%"]
    for contract in report_dict.values() :
        survival_under_25_percent_row.append(contract['survival_under_25_percent'])
        survival_under_25_percent_row.append(contract['survival_under_25_percent']/contract['count']*100)
        survival_under_25_percent_row.append('')
    report_matrix.append(survival_under_25_percent_row)

    survival_under_50_percent_row = ["Survie comprise entre 25% à 50%"]
    for contract in report_dict.values() :
        survival_under_50_percent_row.append((contract['survival_under_50_percent']-contract['out_of_water_under_50_percent']))
        survival_under_50_percent_row.append((contract['survival_under_50_percent']-contract['out_of_water_under_50_percent'])/contract['count']*100)
        survival_under_50_percent_row.append('')
    report_matrix.append(survival_under_50_percent_row)

    survival_up_50_percent_row = ["Survie supérieure 50%"]
    for contract in report_dict.values() :
        survival_up_50_percent_row.append(contract['count']-contract['survival_under_25_percent']-contract['survival_under_50_percent']-contract['out_of_water_under_50_percent']-contract['out_of_water_up_50_percent'])
        survival_up_50_percent_row.append((contract['count']-contract['survival_under_25_percent']-contract['survival_under_50_percent']-contract['out_of_water_under_50_percent']-contract['out_of_water_up_50_percent'])/contract['count']*100)
        survival_up_50_percent_row.append('')
    report_matrix.append(survival_up_50_percent_row)

    vandalism_row = ["Vandalisme"]
    for contract in report_dict.values() :
        vandalism_row.append(contract['vandalism'])
        vandalism_row.append(contract['vandalism']/contract['count']*100)
        vandalism_row.append('')
    report_matrix.append(vandalism_row)

    out_of_water_row = ["Crues - Hors d'eau"]
    for contract in report_dict.values() :
        out_of_water_row.append(contract['out_of_water'])
        out_of_water_row.append(contract['out_of_water']/contract['count']*100)
        out_of_water_row.append('')
    report_matrix.append(out_of_water_row)

    out_of_water_under_50_percent_row = ["Partiellement hors d'eau (25%)"]
    for contract in report_dict.values() :
        out_of_water_under_50_percent_row.append(contract['out_of_water_under_50_percent'])
        out_of_water_under_50_percent_row.append(contract['out_of_water_under_50_percent']/contract['count']*100)
        out_of_water_under_50_percent_row.append('')
    report_matrix.append(out_of_water_under_50_percent_row)

    out_of_water_up_50_percent_row = ["Partiellement hors d'eau (50%)"]
    for contract in report_dict.values() :
        out_of_water_up_50_percent_row.append(contract['out_of_water_up_50_percent'])
        out_of_water_up_50_percent_row.append(contract['out_of_water_up_50_percent']/contract['count']*100)
        out_of_water_up_50_percent_row.append('')
    report_matrix.append(out_of_water_up_50_percent_row)

    total_row = ["Total"]
    for contract in report_dict.values() :
        total_row.append(contract['count'])
        total_row.append(contract['count']/contract['count']*100)
        total_row.append('')
    report_matrix.append(total_row)



    report_matrix = add_new_section(report_matrix, "Bilan", report_dict.keys())

    survival_under_25_percent_row = ["Survie inférieure à 25%"]
    for contract in report_dict.values() :
        survival_under_25_percent_row.append(contract['survival_under_25_percent'])
        survival_under_25_percent_row.append(contract['survival_under_25_percent']/contract['count']*100)
        survival_under_25_percent_row.append('')
    report_matrix.append(survival_under_25_percent_row)

    survival_under_50_percent_row = ["Survie comprise entre 25% à 50%"]
    for contract in report_dict.values() :
        survival_under_50_percent_row.append((contract['survival_under_50_percent']))
        survival_under_50_percent_row.append((contract['survival_under_50_percent'])/contract['count']*100)
        survival_under_50_percent_row.append('')
    report_matrix.append(survival_under_50_percent_row)

    survival_up_50_percent_row = ["Survie supérieure 50%"]
    for contract in report_dict.values() :
        survival_up_50_percent_row.append(contract['count']-contract['survival_under_25_percent']-contract['survival_under_50_percent'])
        survival_up_50_percent_row.append((contract['count']-contract['survival_under_25_percent']-contract['survival_under_50_percent'])/contract['count']*100)
        survival_up_50_percent_row.append('')
    report_matrix.append(survival_up_50_percent_row)
    report_matrix.append(vandalism_row)
    report_matrix.append(out_of_water_row)
    report_matrix.append(total_row)


    report_matrix = add_new_section(report_matrix, "Bilan", report_dict.keys())
    report_matrix.append(survival_under_25_percent_row)
    survival_up_25_percent_row = ["Survie supérieure 25%"]
    for contract in report_dict.values() :
        survival_up_25_percent_row.append(contract['count']-contract['survival_under_25_percent'])
        survival_up_25_percent_row.append((contract['count']-contract['survival_under_25_percent'])/contract['count']*100)
        survival_up_25_percent_row.append('')
    report_matrix.append(survival_up_25_percent_row)
    report_matrix.append(total_row)

    report_matrix = add_new_section(report_matrix, "Survie inférieure à 25%", report_dict.keys())
    not_conform_row = ["Conditions physico-chimiques non conformes"]
    for contract in report_dict.values() :
        not_conform_row.append(contract['survival_under_25_percent_not_conform'])
        not_conform_row.append((contract['survival_under_25_percent_not_conform'])/contract['count']*100)
        not_conform_row.append('')
    report_matrix.append(not_conform_row)

    not_conform_preferred_row = ["Conditions physico-chimiques conformes 'de préférence'"]
    for contract in report_dict.values() :
        not_conform_preferred_row.append(contract['survival_under_25_percent_conform_preferred'])
        not_conform_preferred_row.append((contract['survival_under_25_percent_conform_preferred'])/contract['count']*100)
        not_conform_preferred_row.append('')
    report_matrix.append(not_conform_preferred_row)
    not_conform_compulsory_row = ["Conditions physico-chimiques conformes 'obligatoire'"]
    for contract in report_dict.values() :
        not_conform_compulsory_row.append(contract['survival_under_25_percent_conform_compulsory'])
        not_conform_compulsory_row.append((contract['survival_under_25_percent_conform_compulsory'])/contract['count']*100)
        not_conform_compulsory_row.append('')
    report_matrix.append(not_conform_compulsory_row)
    survival_under_25_percent_row[0]='Total'
    report_matrix.append(survival_under_25_percent_row)

    report_matrix = add_new_section(report_matrix, "Analyses chimiques", report_dict.keys())
    survival_null_row = ["Echantillon non analysé : vandalisme, survie nulle"]
    for contract in report_dict.values() :
        survival_null_row.append(contract['survival_null'])
        survival_null_row.append((contract['survival_null'])/contract['count']*100)
        survival_null_row.append('')
    report_matrix.append(survival_null_row)
    not_totally_analysed_row = ["Echantillon partiellement analysé : survie faible"]
    for contract in report_dict.values() :
        not_totally_analysed_row.append(contract['not_totally_analysed'])
        not_totally_analysed_row.append((contract['not_totally_analysed'])/contract['count']*100)
        not_totally_analysed_row.append('')
    report_matrix.append(not_totally_analysed_row)
    analysed_row = ["Echantillon partiellement analysé : survie faible"]
    for contract in report_dict.values() :
        analysed_row.append(contract['count']-contract['not_totally_analysed']-contract['survival_null'])
        analysed_row.append((contract['count']-contract['not_totally_analysed']-contract['survival_null'])/contract['count']*100)
        analysed_row.append('')
    report_matrix.append(analysed_row)
    report_matrix.append(total_row)



    report_matrix = add_new_section(report_matrix, "Survie inférieure à 25%", report_dict.keys())
    report_matrix.append(not_conform_row)
    conform_row = ["Conditions physico-chimiques conformes"]
    for contract in report_dict.values() :
        conform_row.append(contract['survival_under_25_percent']-contract['survival_under_25_percent_not_conform'])
        conform_row.append((contract['survival_under_25_percent']-contract['survival_under_25_percent_not_conform'])/contract['count']*100)
        conform_row.append('')
    report_matrix.append(conform_row)
    report_matrix.append(survival_under_25_percent_row)



    column_number = 1 + len(list(report_dict.keys()))*3

    report_df = pd.DataFrame(report_matrix, columns=[''] * column_number) 

    return df, report_df

def add_new_section(matrix, section_name, keys) :
    empty_row = [""]
    for key in keys :
        empty_row.append('')
        empty_row.append('')
        empty_row.append('')
    first_row = [""]
    for key in keys :
        first_row.append(key)
        first_row.append('')
        first_row.append('')

    second_row = [section_name]
    for key in keys :
        second_row.append('Total')
        second_row.append('')
        second_row.append('')
    
    third_row = [""]
    for key in keys :
        third_row.append('Nb')
        third_row.append('%')
        third_row.append('')

    matrix.append(empty_row)
    matrix.append(first_row)
    matrix.append(second_row)
    matrix.append(third_row)

    return matrix