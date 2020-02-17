# from tools import QueryScript

# def result_by_pack_and_sandre(pack_id, sandre) :

#     output = QueryScript(f"SELECT prefix, value, sandre FROM analysis WHERE pack_id={pack_id} AND sandre IN {tuple(sandre)}").execute()

#     for i in range(len(output)) :
#         output[i] = [str(output[i][1]) if output[i][0]==None else output[i][0] + str(output[i][1]), output[i][2]]
        
        
#     return output