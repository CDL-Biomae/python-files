from query import QueryScript
from pack_finder import pack_finder

def specimen_size(measurepoint_id):
    packs = pack_finder(measurepoint_id)
    SQL_request = "SELECT size_px, size_mm FROM measuresize WHERE individual>0 AND pack_id IN ("
    SQL_request_standard = "SELECT size_px, size_mm FROM measuresize WHERE individual=0 AND pack_id IN ("
    for i in range(len(packs)) :
        if i == len(packs)-1:
            SQL_request += str(packs[i])
            SQL_request_standard += str(packs[i])
        else :
            SQL_request += str(packs[i]) + ","
            SQL_request_standard += str(packs[i]) + ","
    SQL_request += ")"
    SQL_request_standard += ")"
    standard = QueryScript(SQL_request_standard).execute()
    ratio = standard[0][1]/standard[0][0]
    
    output = QueryScript(SQL_request).execute()

    if output[0][1]!=None and output[0][1]!=0:
        return [size[1] for size in output]
    else :
        return [size[0]*ratio for size in output]
    
    
def leaf_size(measurepoint_id):
    packs = pack_finder(measurepoint_id)
    SQL_request = "SELECT replicate, value FROM measureleaf WHERE pack_id IN ("
    for i in range(len(packs)) :
        if i == len(packs)-1:
            SQL_request += str(packs[i])
        else :
            SQL_request += str(packs[i]) + ","

    SQL_request += ")"

    leaf_remaining = QueryScript(SQL_request).execute()
    
    
    standard_leaf_number = QueryScript("SELECT value FROM r2_constant WHERE name='Nombre de disques (témoin)'").execute()[0]
    replicate_leaf_number = QueryScript("SELECT value FROM r2_constant WHERE name='Nombre de disques par réplicat'").execute()[0]
    test_duration = QueryScript("SELECT value FROM r2_constant WHERE name='Nombre de jour du test'").execute()[0]
    for element in leaf_remaining :
        if element[0]==0:
            replicate_raw_value = element[1]*replicate_leaf_number/standard_leaf_number
    
    ############## ICI A REFAIRE AVEC LA SURVIE ET DEMANDEZ A REMI #############
    eaten_leaves = [(replicate_raw_value - leaf_remaining[i][1])/17.5/test_duration*0.0071 for i in range(1,5)]
    ############################################################################

    return eaten_leaves
    
def inhibition(measurepoint_id):
    constant_alim = QueryScript("SELECT value FROM r2_constant WHERE name LIKE 'Constante alim%'").execute()

    
    eaten_leaves = leaf_size(measurepoint_id)
    print(eaten_leaves)
    size = specimen_size(measurepoint_id)
    
    mean_size = sum(size)/len(size)
    inhibition_replicate = []
    
    expected_eaten_value = constant_alim[0] * 12 + constant_alim[1] + constant_alim[2] * ( mean_size - constant_alim[3] ) ## 12 est à changer par la température moyenne
    inhibition_list = [(eaten_leaf - expected_eaten_value)/expected_eaten_value for eaten_leaf in eaten_leaves]
    
    return sum(inhibition_list)/len(inhibition_list)*100

    
