from calcul import chemistry
import pandas as pd
from tools import QueryScript
import env

## CREATE DATAFRAME ##
def create_dataframe(dick_pack_fusion):
    elements_metal = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element)) for element in elements_metal]
    elements_PCB = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element)) for element in elements_PCB]
    elements_HAP = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element)) for element in elements_HAP]
    elements_others = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
    elements_others = [int(float(element)) for element in elements_others]
    
    matrix = []

    data = chemistry.result_by_packs_and_sandre(dick_pack_fusion)
    for mp in dick_pack_fusion:
        if data[mp]:
            matrix.append([''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_metal ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_PCB ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_HAP ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_others ])
        else :
            matrix.append([''] + ['ND' for sandre in elements_metal ]+[''] + ['ND' for sandre in elements_PCB ]+[''] + ['ND' for sandre in elements_HAP ]+[''] + ['ND' for sandre in elements_others ])
            
    associated_t0 = QueryScript(f"SELECT sandre, prefix, value, pack.measurepoint_id FROM {env.DATABASE_RAW}.analysis JOIN {env.DATABASE_RAW}.pack ON pack.id= analysis.pack_id WHERE pack.measurepoint_id IN (SELECT id FROM {env.DATABASE_RAW}.measurepoint where id IN (SELECT code_t0_id FROM {env.DATABASE_RAW}.measurepoint WHERE id IN ({tuple([mp for mp in data])})));").execute()
    print(associated_t0)

    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_metal]  + [''] + [element for element in elements_PCB] + [''] + [element for element in elements_HAP] + [''] + [element for element in elements_others]
    
    df = df.dropna(how='all', axis='columns')

    return df

def create_empty_dataframe(dick_pack_fusion):
    elements_metal = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_metal = [int(float(element[0])) for element in elements_metal]
    elements_PCB = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly LIKE 'PCB%'").execute()
    elements_PCB = [int(float(element[0])) for element in elements_PCB]
    elements_HAP = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly = 'HAP'").execute()
    elements_HAP = [int(float(element[0])) for element in elements_HAP]
    elements_others = QueryScript(f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version={env.VERSION} AND 21j_threshold IS NOT NULL AND familly != 'HAP' AND familly != 'Métaux' AND familly NOT LIKE 'PCB%'").execute()
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
def create_bbac_21j_dataframe(head_dataframe, dick_pack_fusion):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_dataframe(dick_pack_fusion)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

def create_bbac2_21j_dataframe(head_dataframe, dick_pack_fusion):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_empty_dataframe(dick_pack_fusion)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        
