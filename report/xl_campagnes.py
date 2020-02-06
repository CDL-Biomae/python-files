from calcul import contexte
import pandas as pd

## CREATING DATAFRAME ##


def create_dataframe(list_mp):
    matrix = []

    for i in range(len(list_mp)):
        mp = list_mp[i]
        [J0, J14, JN, N, J21] = contexte(mp)

        temp = [J0, J14, JN, N, J21]
        print(temp)
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Intervention (J0)', 'Intervention (J14)',
                  'Intervention (JN)', 'N', 'Intervention (J21)']
    df = df.dropna(how='all', axis='columns')

    return df


## MAIN FUNCTION ##
def create_campagnes_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values('Numéro')

    return df_campaigns
