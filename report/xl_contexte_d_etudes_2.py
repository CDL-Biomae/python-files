from tools import QueryScript
from tools import agency_finder
from calcul.contexte_d_etudes_2.contexte_d_etudes_2 import contexte
import pandas as pd

## CREATING DATAFRAME ##
def campaign(campaign_ref):
    return int(campaign_ref[-2:])

def measure_points(campaign_ref):
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM datesclees WHERE measurepoint_id IN (SELECT id FROM measurepoint WHERE place_id IN (SELECT id FROM place WHERE campaign_id in (SELECT id FROM campaign WHERE reference = '{campaign_ref}')));"
    )
    return output.execute()

def number_name_mp(list_mp):
    output = QueryScript(
        f"SELECT report_pin, name FROM measurepoint WHERE id in {tuple(list_mp)}"
    ).execute()
    list_number = [x[0] for x in output]
    list_name = [x[1] for x in output]

    return list_number, list_name

def agency_mp(list_mp):
    list_agency = []
    for mp in list_mp:
        list_agency.append(agency_finder(mp))

    return list_agency

def create_dataframe(campaign_ref):
    campaign_id = campaign(campaign_ref)
    list_mp = measure_points(campaign_ref)
    list_number, list_name = number_name_mp(list_mp)
    list_agency = agency_mp(list_mp)

    matrix = []

    for i in range(len(list_mp)):
        mp = list_mp[i]
        number = list_number[i]
        name = list_name[i]
        agency = list_agency[i]
        [J0, J14, JN, N, J21] = contexte(mp)

        temp = [campaign_id, number, name, agency, J0, J14, JN, N, J21]
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence', 'Intervention (J0)', 'Intervention (J14)', 'Intervention (JN)', 'N', 'Intervention (J21)']

    return df

## CREATING EXCEL ##
def clean(dataframe):
    return dataframe.dropna(how='all', axis='columns')

def write_excel(list_dataframe, list_campaigns):
    df_concat = pd.concat(list_dataframe)
    df_excel = clean(df_concat)

    filename = 'Rapport_pour'
    for c in list_campaigns:
        filename += f"_{c}"
    filename += '.xlsx'

    df_excel.to_excel(filename, sheet_name='sheet1', index=False)
    print(f"Rapport créé sous le nom: \"{filename}\"")

## MAIN FUNCTION ##
def create_report(list_campaigns):
    list_dataframe = []
    for campaign_str in list_campaigns:
        df = create_dataframe(campaign_str)
        list_dataframe.append(df)

    write_excel(list_dataframe, list_campaigns)

