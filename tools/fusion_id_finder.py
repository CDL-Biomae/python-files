from tools import QueryScript

def fusion_id_finder(pack_id) :
    return QueryScript("SELECT measurepoint_fusion_id FROM datesclees JOIN pack ON datesclees.measurepoint_id=pack.measurepoint_id WHERE pack.id="+str(pack_id)).execute()[0]