from tools import QueryScript

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