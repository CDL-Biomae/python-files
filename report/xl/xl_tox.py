from tools import QueryScript, translate
import pandas as pd
import env

def create_tox_dataframe(campaigns_dict, measurepoint_list):
    list_dataframe = []
    data = QueryScript(f"SELECT measurepoint_id, round(male_survival_7_days), round(alimentation, 1), round(neurotoxicity, 1), round(female_survivor), number_days_exposition, number_female_concerned, round(percent_inhibition_fecondite, 1), number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption FROM {env.DATABASE_TREATED}.toxtable WHERE version=  {env.CHOSEN_VERSION()} AND measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+(str(measurepoint_list[0]) if len(measurepoint_list) else '0')+')'};").execute()
    for campaign_id in campaigns_dict:
        matrix =[]
        for place_id in campaigns_dict[campaign_id]["place"]:
            temp = [None]*18
            if "duplicate" in campaigns_dict[campaign_id]["place"][place_id] and not "chemistry" in campaigns_dict[campaign_id]["place"][place_id]["duplicate"]:
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    number = float(str(campaigns_dict[campaign_id]["place"][place_id]["number"])+'.'+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]))
                    for mp_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption in data :
                        if measurepoint_id==mp_id and measurepoint_id in measurepoint_list :
                            for index in range(4):
                                temp[index] = [campaigns_dict[campaign_id]["number"], number, translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'][index]
                            if male_survival_7_days and alimentation :
                                temp[5], temp[6] = male_survival_7_days, alimentation
                            if neurotoxicity :
                                temp[7] = neurotoxicity
                            if female_survivor and number_days_exposition and number_female_concerned and percent_inhibition_fecondite and number_female_analysis and molting_cycle and number_female_concerned_area and endocrine_disruption :
                                for index in range(9,18):
                                    temp[index] = [female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, measurepoint_id][index-9]
                    matrix.append(temp)
                    temp = [None]*18
            else :
                number = campaigns_dict[campaign_id]["place"][place_id]["number"]
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    for mp_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption in data :
                        if measurepoint_id==mp_id :
                            for index in range(4):
                                temp[index] = [campaigns_dict[campaign_id]["number"], number, translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'][index]
                            if male_survival_7_days and alimentation :
                                temp[5], temp[6] = male_survival_7_days, alimentation
                            if neurotoxicity :
                                temp[7] = neurotoxicity
                            if female_survivor and number_days_exposition and number_female_concerned and percent_inhibition_fecondite and number_female_analysis and molting_cycle and number_female_concerned_area and endocrine_disruption :
                                for index in range(9,18):
                                    temp[index] = [female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, measurepoint_id][index-9]
                matrix.append(temp)
        df = pd.DataFrame(matrix)
        df.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence','','Survie Male - 7 jours', 'Alimentation',
                'Neurotoxicité AChE','', 'Survie Femelle','Nombre jours exposition in situ',
                'n','Fécondité','n','Cycle de mue','n','Perturbation endocrinienne','']
        list_dataframe.append(df)
    df_values = pd.concat(list_dataframe)
    df_sorted = df_values.sort_values(['Numéro', 'Campagne'])
    return df_sorted
