from tools import QueryScript


def get_dict_pack_fusion(campaign=None):
    if campaign:
        output = QueryScript(
            f"SELECT DISTINCT pack.id, key_dates.measurepoint_fusion_id, pack.nature FROM pack JOIN key_dates ON key_dates.measurepoint_id=pack.measurepoint_id JOIN measurepoint ON measurepoint.id=pack.measurepoint_id WHERE measurepoint.reference LIKE '{campaign}%';"
        ).execute()
    else:    
        output = QueryScript(
            f"SELECT DISTINCT pack.id, key_dates.measurepoint_fusion_id, pack.nature FROM pack JOIN key_dates ON key_dates.measurepoint_id=pack.measurepoint_id;"
        ).execute()

    dict_pack_fusion = {}

    for row in output:
        [pack_id, mp, nature] = row

        try:
            dict_pack_fusion[mp][nature] = pack_id
        except KeyError:
            dict_pack_fusion[mp] = {}
            dict_pack_fusion[mp][nature] = pack_id

    return(dict_pack_fusion)
