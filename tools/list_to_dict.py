def list_to_dict(liste):  # liste avec en premier l'element qui servira de clef
    dico = dict()
    for elt in liste:
        if len(elt) == 2:
            dico[elt[0]] = elt[1]
        else:
            dico[elt[0]] = elt[1:]
    return dico