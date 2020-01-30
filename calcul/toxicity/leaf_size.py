from tools import QueryScript

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