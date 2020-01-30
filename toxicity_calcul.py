from query import QueryScript
from tools import pack_finder


def specimen_size(pack_id):
    SQL_request = "SELECT size_px, size_mm FROM measuresize WHERE individual>0 AND pack_id="+str(pack_id)
    SQL_request_standard = "SELECT size_px, size_mm FROM measuresize WHERE individual=0 AND pack_id="+str(pack_id)

    standard = QueryScript(SQL_request_standard).execute()
    ratio = standard[0][1]/standard[0][0]

    output = QueryScript(SQL_request).execute()

    if output[0][1] != None and output[0][1] != 0:
        return [size[1] for size in output]
    else:
        return [size[0]*ratio for size in output]


def leaf_size(pack_id):

    SQL_request = "SELECT replicate, value FROM measureleaf WHERE pack_id="+str(pack_id)

    leaf_remaining = QueryScript(SQL_request).execute()

    standard_leaf_number = QueryScript(
        "SELECT value FROM r2_constant WHERE name='Nombre de disques (témoin)'").execute()[0]
    replicate_leaf_number = QueryScript(
        "SELECT value FROM r2_constant WHERE name='Nombre de disques par réplicat'").execute()[0]
    test_duration = QueryScript(
        "SELECT value FROM r2_constant WHERE name='Nombre de jour du test'").execute()[0]
    for element in leaf_remaining:
        if element[0] == 0:
            replicate_raw_value = element[1] * \
                replicate_leaf_number/standard_leaf_number

    ############## ICI A REFAIRE AVEC LA SURVIE ET DEMANDEZ A REMI #############
    eaten_leaves = [(replicate_raw_value - leaf_remaining[i][1]) /
                    17.5/test_duration*0.0071 for i in range(1, 5)]
    ############################################################################

    return eaten_leaves


def alimentation_inhibition(pack_id):
    constant_alim = QueryScript(
        "SELECT value FROM r2_constant WHERE name LIKE 'Constante alim%'").execute()

    eaten_leaves = leaf_size(pack_id)
    size = specimen_size(pack_id)

    mean_size = sum(size)/len(size)
    inhibition_replicate = []

    expected_eaten_value = constant_alim[0] * 12 + constant_alim[1] + constant_alim[2] * (
        mean_size - constant_alim[3])  # 12 est à changer par la température moyenne
    inhibition_list = [(eaten_leaf - expected_eaten_value) /
                       expected_eaten_value for eaten_leaf in eaten_leaves]

    return sum(inhibition_list)/len(inhibition_list)*100

def neurotoxicity(pack_id):
    
    constant_AChE = QueryScript(
        "SELECT value FROM r2_constant WHERE name LIKE 'Constante ache%'").execute()
    SQL_request = "SELECT ache, weight FROM cage WHERE pack_id="+str(pack_id)
    output = QueryScript(SQL_request).execute()

    AChE_list = []
    weight_list = []

    for element in output :
        if element[0]!=None:
            AChE_list.append(element[0])
            weight_list.append(element[1])
            
    mean_AChE = sum(AChE_list)/len(AChE_list)
    mean_weight = sum(weight_list)/len(weight_list)

    AChE_expected = constant_AChE[0] + constant_AChE[1] * ( mean_weight ** constant_AChE[2] )
    
    return ( mean_AChE - AChE_expected ) / AChE_expected * 100
