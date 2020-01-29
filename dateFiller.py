#%%
from query import QueryScript
campaigns = QueryScript(script='SELECT id, reference FROM campaign').execute()
# print(campaigns)

#%%
id_campaigns = [x[0] for x in campaigns]
cap = False

for id_c in id_campaigns:
    places = QueryScript(script='SELECT id, reference, type FROM place WHERE campaign_id='+str(id_c)).execute()
    n_places = len(places)
    for i in range(n_places):
        id_p, ref_p, type_p = places[i]

        if type_p == 'work_monitoring':
            measurepoints = QueryScript(script='SELECT id, reference FROM measurepoint WHERE place_id='+str(id_p)).execute()
            # print(measurepoints)
            id_measurepoints = [x[0] for x in measurepoints]

            for id_mp in id_measurepoints:
                exposureconditions = QueryScript(script='SELECT step, recordedAt, barrel FROM measureexposurecondition WHERE measurepoint_id='+str(id_mp)).execute()
                steps_barrels = [(x[0], x[2]) for x in exposureconditions]
                print(steps_barrels)
                print(exposureconditions[1])

                # Dictionnaire de dates cles à remplir
                dates_cles = {}

                # (step 50, R0) Transplantation Alimentation
                try:
                    idx = steps_barrels.index((50, 'R0'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Transplantation Alimentation'] = {'date': temp_date, 'step': 50, 'barrel': 'R0'}

                # (step 60, R7) Recuperation Alimentation
                try:
                    idx = steps_barrels.index((60, 'R7'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Recuperation Alimentation'] = {'date': temp_date, 'step': 60, 'barrel': 'R7'}

                # (step 20) Lancement Alimentation
                try:
                    idx = steps_barrels.index((20, None))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Lancement Alimentation'] = {'date': temp_date, 'step': 20, 'barrel': None}

                # (step 140, RN) Recuperation Reprotoxicité
                try:
                    idx = steps_barrels.index((140, 'RN'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Recuperation Reprotoxicite'] = {'date': temp_date, 'step': 140, 'barrel': 'RN'}

                # (step 170) Arrêt Reprotoxicité
                try:
                    idx = steps_barrels.index((170, None))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Arret Reprotoxicite'] = {'date': temp_date, 'step': 170, 'barrel': None}

                # (step 50, C0) Lancement Chimie (=Lancement reprotoxicité)
                try:
                    idx = steps_barrels.index((50, 'C0'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Lancement Alimentation'] = {'date': temp_date, 'step': 50, 'barrel': 'C0'}

                # (step 100, R21) Récupération Chimie
                try:
                    idx = steps_barrels.index((100, 'R21'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None

                dates_cles['Lancement Alimentation'] = {'date': temp_date, 'step': 100, 'barrel': 'R21'}

                print(dates_cles)

                cap = True
                break

    if cap:
        break



print('fini')



