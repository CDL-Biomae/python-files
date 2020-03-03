from . import *


def run(cas):


    reference_filler.run()
    date_filler.run(cas)
    average_temperature_filler.run()
    temperature_repro.run()
    tox_table_filler.run(cas)
