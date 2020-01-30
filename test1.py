# import reference_filler

# reference_filler.run()

from query import QueryScript

output = QueryScript("SELECT specimen_size_px FROM measurereprotoxicity WHERE specimen_size_px IS NOT NULL AND pack_id=6393").execute()
for i in output :
    print(i)
