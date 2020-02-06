def list_to_dict(liste):  # liste avec en premier l'element qui servira de clef
    dictionnary = dict()
    for elt in liste:
        if len(elt) == 2:
            dictionnary[elt[0]] = elt[1]
        else:
            dictionnary[elt[0]] = elt[1:]
    return dictionnary