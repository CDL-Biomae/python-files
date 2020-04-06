from calcul import chemistry
import pandas as pd
from tools import QueryScript
import env

## CREATE DATAFRAME ##
def create_dataframe(dict_pack):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont les sandres dont les seuils 21j sont non nuls dans r3 (table reference)
    Les colonnes vides sont supprimées
    :param dict_pack:
    :return: dataframe:
    '''
    elements_metal = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element)) for element in elements_metal]
    elements_PCB = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element)) for element in elements_PCB]
    elements_HAP = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element)) for element in elements_HAP]
    elements_others = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
    elements_others = [int(float(element)) for element in elements_others]
    
    matrix = []

    data = chemistry.result_by_packs_and_sandre(dict_pack)
    for mp in dict_pack:
        if data[mp]:
            matrix.append([''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_metal ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_PCB ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_HAP ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_others ] + [mp])
        else :
            matrix.append([''] + ['ND' for sandre in elements_metal ]+[''] + ['ND' for sandre in elements_PCB ]+[''] + ['ND' for sandre in elements_HAP ]+[''] + ['ND' for sandre in elements_others ] + [mp])
            

    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_metal]  + [''] + [element for element in elements_PCB] + [''] + [element for element in elements_HAP] + [''] + [element for element in elements_others] + ['']
    
    df = df.dropna(how='all', axis='columns')

    return df

def create_empty_dataframe(dict_pack):
    elements_metal = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element[0])) for element in elements_metal]
    elements_PCB = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element[0])) for element in elements_PCB]
    elements_HAP = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element[0])) for element in elements_HAP]
    elements_others = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()} AND 21j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
    elements_others = [int(float(element[0])) for element in elements_others]
    
    matrix = []

    data = chemistry.result_by_packs_and_sandre(dict_pack)
    for mp in dict_pack:
        matrix.append([''] + ['' for sandre in elements_metal ]+[''] + ['' for sandre in elements_PCB ]+[''] + ['' for sandre in elements_HAP ]+[''] + ['' for sandre in elements_others ])

 

    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_metal]  + [''] + [element for element in elements_PCB] + [''] + [element for element in elements_HAP] + [''] + [element for element in elements_others]
    df = df.dropna(how='all', axis='columns')

    return df


## MAIN FUNCTION ##
def create_bbac_21j_dataframe(head_dataframe, dict_pack):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_dataframe(dict_pack)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

def create_bbac2_21j_dataframe(head_dataframe, dict_pack):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_empty_dataframe(dict_pack)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        
