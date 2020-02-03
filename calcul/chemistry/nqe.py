from tools import QueryScript

elements_crustaces = {
    1115: 'Benzo (a) pyrene',
    1118: 'Benzo (g,h,i) Perylene',
    1117: 'Benzo (k) Fluoranthene',
    1116: 'Benzo (b) Fluoranthene',
    1204: 'Indeno (1,2,3-cd) Pyrene',
    1191: 'Fluoranthene',
    6616: 'DEHP',
    7707: 'Dioxines et composées de type dioxine'
}
code_sandre_elements = tuple(elements_crustaces.keys())

def nqe_info(code_sandre):
    output = QueryScript(f"SELECT maximum, freq_quanti FROM r3 WHERE sandre IN {code_sandre}").execute()

    maximum, freq_quanti = [], []
    for couple in output:
        if couple[0] != 0:
            maximum.append(couple[0])
        else:
            maximum.append(None)
        freq_quanti.append(couple[1])

    return(maximum, freq_quanti)


def nqe_crustace_values(pack_id):
    print('ok')

# print(nqe_crustace_info(code_sandre))