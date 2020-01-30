from tools import QueryScript

def pack_finder(measurepoint_id) :
    return QueryScript("SELECT id FROM pack WHERE measurepoint_id="+str(measurepoint_id)).execute()
    
