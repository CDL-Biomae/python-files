from calcul.chemistry import survival
from tools import QueryScript, translate
import pandas as pd
import env

def create_survie_dataframe(campaigns_dict, chemistry_measurepoint_list):
    '''
    Créé une dataframe qui contient les données de l'onglet 'survie' de l'Excel
    :param head_dataframe: cf initialization.py
    :param list_campaigns: list des references de campagne
    :param dict_mp: {'ref_campagne': [mp, ...], ...}
    :return:
    '''
    global_matrix = []
    for campaign_id in campaigns_dict:
        matrix = []
        pack_list = []
        for place_id in campaigns_dict[campaign_id]["place"] :
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for pack_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"]:
                    if campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"][pack_id]=='chemistry':
                        pack_list.append(pack_id)
        survival_dict = survival(pack_list)
        for place_id in campaigns_dict[campaign_id]["place"] :
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                if measurepoint_id in chemistry_measurepoint_list:
                    for pack_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"]:
                        if campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"][pack_id]=='chemistry':
                            if "duplicate" in campaigns_dict[campaign_id]["place"][place_id] and "chemistry" in campaigns_dict[campaign_id]["place"][place_id]["duplicate"]:
                                number = float(str(campaigns_dict[campaign_id]["place"][place_id]["number"])+'.'+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]))
                            else :
                                number = campaigns_dict[campaign_id]["place"][place_id]["number"]
                            if pack_id in survival_dict:
                                matrix.append([campaigns_dict[campaign_id]["number"], number, translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND',survival_dict[pack_id]])
                            else :
                                matrix.append([campaigns_dict[campaign_id]["number"], number, translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND','ND'])
        # for pack in list_pack:
        #     survie = survival(pack)
        #     matrix.append(survie)


        global_matrix.append(matrix)
        
    if len(global_matrix)>1:
        list_dataframe = []
        for campaign in global_matrix:
            df = pd.DataFrame(campaign, columns=['Campagne', 'Numéro', 'Station de mesure', 'Code Agence','Survie biotest chimie'])
            list_dataframe.append(df)
        df_values = pd.concat(list_dataframe)
    else :
        df_values = pd.DataFrame(global_matrix[0])
        df_values.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence','Survie biotest chimie']
    df_survie = df_values.sort_values(['Numéro', 'Campagne'])

    return df_survie
