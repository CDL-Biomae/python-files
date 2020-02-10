from tools import QueryScript
from calcul import chemistry, alimentation, neurotoxicity

def measurepoint_result(measurepoint_id):
    packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id={measurepoint_id}").execute()
    for pack in packs :
        if(pack[0]=='chemistry'):
            print(chemistry.data(pack[1]))
        if(pack[0]=='alimentation'):
            print(alimentation(pack[1]))
        if(pack[0]=='neurology'):
            print(neurotoxicity(pack[1]))