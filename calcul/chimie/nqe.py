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

def nqe_crustace_info(pack_id):
    code_sandre_elements = tuple(elements_crustaces.keys())
    maximum = QueryScript("SELCT maximum FROM r3 WHERE ")


def nqe_crustace_values(pack_id):
    print('ok')