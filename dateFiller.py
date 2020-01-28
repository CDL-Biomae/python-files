#%%
from query import Query
campaigns = Query(script='SELECT id, reference FROM campaign').execute()
print(campaigns)

#%%
id_campaigns = [x[0] for x in campaigns]

for id_c in id_campaigns:
    places = Query(script='SELECT id, reference, type FROM place WHERE campaign_id='+str(id_c)).execute()
    n_places = len(places)
    for i in range(n_places):
        id_p, ref_p, type_p = places[i]

        if type_p == 'work_monitoring':
            measurepoints = Query(script='SELECT id, reference FROM measurepoint WHERE place_id='+str(id_p)).execute()
            print(measurepoints)
            id_measurepoints = [x[0] for x in measurepoints]

            for id_mp in id_measurepoints:
                exposureconditions = Query(script='SELECT step, recordedAt FROM measureexposurecondition WHERE measurepoint_id='+str(id_mp)).execute()
                print(exposureconditions)
                break




print('fini')



