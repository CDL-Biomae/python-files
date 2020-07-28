from tools import QueryScript
import env

elements_crustacean = {
    1115: 'Benzo (a) pyrene',
    1118: 'Benzo (g,h,i) Perylene',
    1117: 'Benzo (k) Fluoranthene',
    1116: 'Benzo (b) Fluoranthene',
    1204: 'Indeno (1,2,3-cd) Pyrene',
    1191: 'Fluoranthene',
    6616: 'DEHP',
    7707: 'Dioxines et composées de type dioxine'
}
elements_fish = {
    1197: 'Heptachlore',
    1198: 'Heptachlore Epoxyde',
    1172: 'Dicofol',
    1652: 'Hexachlorobutadiene',
    1199: 'Hexachlorobenzene',
    7128: 'HBCDD',
    1955: 'Chloroalcanes C10-13',
    1888: 'Pentachlorobenzene',
    7705: 'PBDE (BDE-28,47,99,100,153,154)',
    6560: 'PFOS',
    1387: 'Mercure (Hg)'
}

code_sandre_elements = tuple(elements_crustacean.keys())

def maximum_freq_quanti(code_sandre):
    '''
    Crée un tuple composé d'une liste de fréquences quanti et une autre des maxima
    :param code_sandre:
    :return: ([maximum], [freq_quanti]):
    '''
    output = QueryScript(f" SELECT maximum, freq_quanti   FROM {env.DATABASE_TREATED}.r3 WHERE sandre IN {tuple(code_sandre) if len(code_sandre)>1 else '('+(str(code_sandre[0]) if len(code_sandre) else '0')+')'} AND version=  {env.CHOSEN_VERSION()}").execute()

    maximum, freq_quanti = [], []
    for couple in output:
        if couple[0] != 0:
            maximum.append(couple[0])
        else:
            maximum.append(None)
        freq_quanti.append(couple[1])

    return(maximum, freq_quanti)