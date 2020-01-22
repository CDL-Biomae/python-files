from query import Query

New_Query = Query(column="t0",table="measurepoint", filter=["temperature_max=20","conductivity_min=100"])

print(New_Query.execute())