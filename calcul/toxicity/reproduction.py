from tools import QueryScript
import env

class Reproduction:

    @staticmethod
    def female_survivor(dict_pack_fusion):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack_fusion:
            try:
                pack_id = dict_pack_fusion[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        output = QueryScript(
            f"  SELECT pack_id, scud_survivor_female, scud_quantity   FROM {env.DATABASE_RAW}.Cage WHERE pack_id IN {tuple(list_pack_repro)};"
        ).execute()

        # Reformatage des données de la requête
        dict_requete = {pack_id: {'scud_quantity': None, 'scud_survivor_female': []} for pack_id in list_pack_repro}

        for row in output:
            [pack_id, scud_survivor_female, scud_quantity] = row
            if dict_requete[pack_id]['scud_quantity'] is None:
                dict_requete[pack_id]['scud_quantity'] = scud_quantity
            if scud_survivor_female is not None:
                dict_requete[pack_id]['scud_survivor_female'].append(scud_survivor_female)

        # Calcul du pourcentage de survie par pack
        dict_survie_femelle = {mp_fusion: None for mp_fusion in dict_pack_fusion.keys()}

        for mp_fusion in dict_survie_femelle.keys():
            if mp_fusion not in list_mp_repro:
                continue
            pack_id = dict_pack_fusion[mp_fusion]['reproduction']
            scud_quantity = dict_requete[pack_id]['scud_quantity']
            scud_survivor_female = dict_requete[pack_id]['scud_survivor_female']

            if scud_quantity is not None and len(scud_survivor_female) != 0:
                try:
                    survie_femelle = (sum(scud_survivor_female)/len(scud_survivor_female)) / scud_quantity
                except ZeroDivisionError:
                    print(f"Point de mesure: {mp_fusion} --> Erreur de calcul de survie femelle, quantité de gamares dans la cage inconnu")
                    continue
                dict_survie_femelle[mp_fusion] = survie_femelle*100

        return dict_survie_femelle

    






   
    
 



 