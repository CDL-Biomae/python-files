from database import version_filler, reference_filler, reference_key_date_filler, key_date_filler, average_temperature_filler, temperature_repro_filler, tox_table_filler

def run(cas, xl_path=None, date=None, comment=None):
    print("Database management started...")
    version_filler.run(cas, date, comment)
    reference_filler.run(cas, xl_path)

    reference_key_date_filler.run(cas)
    key_date_filler.run(cas)

    temperatures = average_temperature_filler.run(cas)
    temperature_repro_filler.run(cas, temperatures)

    tox_table_filler.run(cas)
    print("Database management finished")

