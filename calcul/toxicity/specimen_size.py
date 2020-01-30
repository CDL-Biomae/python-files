from tools import QueryScript

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