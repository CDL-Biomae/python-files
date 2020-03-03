from . import *


def run(cas):
    version_filler.run(cas)
    reference_filler.run()

    reference_date_filler.run(cas)
    date_filler.run(cas)

    average_temperature_filler.run()
    temperature_repro.run()

    tox_table_filler.run(cas)
