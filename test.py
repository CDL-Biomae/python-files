from query import Query

New_Query = Query(column="city", table="agency")

print(New_Query)

New_Query.setLimit(100)
print(New_Query)

New_Query.setLimit()
print(New_Query)