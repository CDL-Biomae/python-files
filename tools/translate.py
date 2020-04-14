def translate(element):
    '''
    Permet de traduire une chaine de caractère encodé en windows-1252 à un encodage utf-8.
    Si l'element en entrée n'est pas une chaîne de caractère, il est renvoyé identique
    :param element: str windows-1252
    :return: element: str utf-8
    '''
    if isinstance(element, str):
        try :
            return element.encode('windows-1252').decode('utf-8')
        except UnicodeDecodeError :
            return element
    else:
        return element
