def clean_dict(dico):
    for key in dico.keys():
        if isinstance(dico[key], dict):
            clean_dict(dico[key])
        else:
            if dico[key] == None:
                dico[key] = ""
