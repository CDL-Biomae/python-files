from tools import QueryScript

def result_by_pack_and_sandre(pack_id, sandre) :
    output = QueryScript(f"SELECT prefix, value FROM analysis WHERE pack_id={pack_id} AND sandre={sandre}").execute()
    if len(output)!=0:
        return str(output[0][1]) if output[0][0]==None else output[0][0] + str(output[0][1])
    if len(output)==0:
        return []