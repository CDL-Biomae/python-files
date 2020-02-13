import pandas as pd
from datetime import date


def create_version_dataframe():
    today = date.today().strftime("%d/%m/%Y")
    d = {'Date': [today], 'Version': ['V1'], 'Commentaires': ['Création du document']}
    df = pd.DataFrame(data=d)
    return df
