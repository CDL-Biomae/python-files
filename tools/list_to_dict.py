def list_to_dict(list):
    '''
    Créer un dictionnaire à partir d'une liste de liste. Le premier élément de chaque liste est utilisé comme clé
    :param list: liste avec en premier l'element qui servira de clef
    :return: dictionnaire:
    '''
    dictionnary = dict()
    for elt in list:
        if len(elt) == 2:
            dictionnary[elt[0]] = elt[1]
        else:
            dictionnary[elt[0]] = elt[1:]
    return dictionnary
