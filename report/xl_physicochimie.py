from tools import QueryScript
import pandas as pd
from calcul.conditions_d_expo.conditions_d_expo import conditions

def temperatures_dataframe(list_mp):

def values_dataframe(list_mp):
    matrix = []

    for mp in list_mp:
        list_conductivite, list_ph, list_oxygen = conditions(mp)
        values = list_conductivite + list_ph + list_oxygen
        matrix.append(values)

    df = pd.DataFrame(matrix)
    df.columns = ['Conductivité J0', 'Conductivité J14', 'Conductivité JN', 'Conductivité J21',
                  'pH J0', 'pH J14', 'pH JN', 'pH J21',
                  'Oxygène J0', 'Oxygène J14', 'Oxygène JN', 'Oxygène J21']
    df = df.dropna(how='all', axis='columns')

    return df