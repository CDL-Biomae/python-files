from tools import QueryScript
import datetime
import env
import pandas as pd


## MAIN FUNCTION ##
def create_campagnes_dataframe(head_dataframe, campaigns_dict, J_dict):
    global_matrix = []
    for campaign_id in campaigns_dict:
        matrix = []
        for place_id in campaigns_dict[campaign_id]["place"]:
            temp = [None]*6
            temp[0] = J_dict[place_id]["J0"]["truncated_date"]
            temp[1] = J_dict[place_id]["J7"]["truncated_date"]
            temp[2] = J_dict[place_id]["J14"]["truncated_date"]
            temp[3] = J_dict[place_id]["JN"]["truncated_date"]
            temp[4] = J_dict[place_id]["N"]
            temp[5] = J_dict[place_id]["J21"]["truncated_date"]
            matrix.append(temp)
        global_matrix.append(matrix)
    if len(global_matrix)>1:
        list_dataframe = []
        for matrix in global_matrix :
            df =  pd.DataFrame(matrix, columns=['Intervention (J0)', 'Intervention (J7)','Intervention (J14)',
                  'Intervention (JN)', 'N', 'Intervention (J21)']) 
            list_dataframe.append(df)
        df_values = pd.concat(list_dataframe)
    else :
        df_values = pd.DataFrame(global_matrix[0], columns=['Intervention (J0)', 'Intervention (J7)','Intervention (J14)',
                  'Intervention (JN)', 'N', 'Intervention (J21)'])
    df_values = df_values.dropna(how='all', axis='columns')
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])


    return df_campaigns
