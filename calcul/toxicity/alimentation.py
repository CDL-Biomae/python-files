from tools import QueryScript, fusion_id_finder

def survie_alim(pack_id):
    SQL_request = "SELECT scud_survivor,scud_quantity FROM cage where pack_id="+str(pack_id)+" and nature='alimentation' and scud_survivor!='null' "
    resultat2 = []
    resultat =  QueryScript(SQL_request).execute()
    
    
    for j in range(len(resultat)) :       
         tmp = sum(resultat[j])/len(resultat[j])
         resultat2.append(tmp)
        
    return resultat2
   

def survie_7jour(pack_id):
    survi_alim = survie_alim(pack_id)
    SQL_request = "SELECT scud_survivor,scud_quantity FROM cage where pack_id="+str(pack_id)+" and nature='alimentation' and scud_survivor!='null'"
    resultat =  QueryScript(SQL_request).execute()
    survivor = []
    quantity =[]
    for i in range(len(resultat)) :
            survivor.append(resultat[i][0])
            quantity.append(resultat[i][1])

    if sum(survi_alim) == 0:
        return "0"
    else:
        return sum(survivor)/len(survivor)/quantity[0]*100


         

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
    survivor = survie_alim(pack_id)    
    ############## ICI DEMANDEZ A REMI #############
    eaten_leaves = [(replicate_raw_value - leaf_remaining[i][1]) /
                    survivor[i-1]/test_duration*0.0071 for i in range(1, 5)]
    ############################################################################
    return eaten_leaves

def alimentation(pack_id):
    constant_alim = QueryScript(
        "SELECT value FROM r2_constant WHERE name LIKE 'Constante alim%'").execute()
    fusion_id = fusion_id_finder(pack_id)
    average_temperature = QueryScript("SELECT sonde1_moy FROM average_temperature_table WHERE measurepoint_fusion_id="+str(fusion_id)).execute()[0]
    eaten_leaves = leaf_size(pack_id)
    size = specimen_size(pack_id)

    mean_size = sum(size)/len(size)
    inhibition_replicate = []

    expected_eaten_value = constant_alim[0] * average_temperature + constant_alim[1] + constant_alim[2] * (
        mean_size - constant_alim[3]) 
    inhibition_list = [(eaten_leaf - expected_eaten_value) /
                       expected_eaten_value for eaten_leaf in eaten_leaves]
    
    return sum(inhibition_list)/len(inhibition_list)*100