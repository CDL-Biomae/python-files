from tools import QueryScript


def get_dict_pack_fusion():
    output = QueryScript(
        f"SELECT id, measurepoint_id, nature FROM pack"
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

a = get_dict_pack_fusion()