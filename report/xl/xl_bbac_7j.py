from calcul import chemistry
import pandas as pd
from tools import QueryScript

## CREATE DATAFRAME ##
def create_dataframe(dick_pack_fusion):
    elements_metal = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element)) for element in elements_metal]
    elements_PCB = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element)) for element in elements_PCB]
    elements_HAP = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element)) for element in elements_HAP]
    elements_others = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
    elements_others = [int(float(element)) for element in elements_others]
    
    matrix = []

    data = chemistry.result_by_packs_and_sandre(dick_pack_fusion)
    for mp in dick_pack_fusion:
        matrix.append([''] + [data[mp][sandre] for sandre in elements_metal ]+[''] + [data[mp][sandre] for sandre in elements_PCB ]+[''] + [data[mp][sandre] for sandre in elements_HAP ]+[''] + [data[mp][sandre] for sandre in elements_others ])

 

    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_metal]  + [''] + [element for element in elements_PCB] + [''] + [element for element in elements_HAP] + [''] + [element for element in elements_others]
    
    df = df.dropna(how='all', axis='columns')

    return df

def create_empty_dataframe(dick_pack_fusion):
    elements_metal = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element[0])) for element in elements_metal]
    elements_PCB = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element[0])) for element in elements_PCB]
    elements_HAP = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element[0])) for element in elements_HAP]
    elements_others = QueryScript("SELECT sandre FROM r3 WHERE 7j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
    elements_others = [int(float(element[0])) for element in elements_others]
    
    matrix = []

    data = chemistry.result_by_packs_and_sandre(dick_pack_fusion)
    for mp in dick_pack_fusion:
        matrix.append([''] + ['' for sandre in elements_metal ]+[''] + ['' for sandre in elements_PCB ]+[''] + ['' for sandre in elements_HAP ]+[''] + ['' for sandre in elements_others ])

 

    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_metal]  + [''] + [element for element in elements_PCB] + [''] + [element for element in elements_HAP] + [''] + [element for element in elements_others]
    df = df.dropna(how='all', axis='columns')

    return df


## MAIN FUNCTION ##
def create_bbac_7j_dataframe(head_dataframe, dick_pack_fusion, dict_mp):
    list_dataframe = []
    df_values = create_dataframe(dick_pack_fusion)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

def create_bbac2_7j_dataframe(head_dataframe, dick_pack_fusion, dict_mp):
    list_dataframe = []
    df_values = create_empty_dataframe(dick_pack_fusion)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        
