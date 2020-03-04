from . import *


def run(cas, xl_path=None, date=None, comment=None):
    version_filler.run(cas, date, comment)
    reference_filler.run(cas, xl_path)

    reference_date_filler.run(cas)
    date_filler.run(cas)

    average_temperature_filler.run(cas)
    temperature_repro.run(cas)

    tox_table_filler.run(cas)
