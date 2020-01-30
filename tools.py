from query import QueryScript


def pack_finder(measurepoint_id):
    return QueryScript("SELECT id FROM pack WHERE measurepoint_id="+str(measurepoint_id)).execute()


def list_to_dict(liste):  # liste avec en premier l'element qui servira de clef
    dico = dict()
    for elt in liste:
        if len(elt) == 2:
            dico[elt[0]] = elt[1]
        else:
            dico[elt[0]] = elt[1:]
    return dico
