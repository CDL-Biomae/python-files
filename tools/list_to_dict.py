def list_to_dict(liste):  # liste avec en premier l'element qui servira de clef
    dict = dict()
    for elt in liste:
        if len(elt) == 2:
            dict[elt[0]] = elt[1]
        else:
            dict[elt[0]] = elt[1:]
    return dict