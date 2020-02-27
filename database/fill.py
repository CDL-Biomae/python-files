from . import *

def run(cas=None):
    reference_filler.run()
    reference_date_filler.run()
    date_filler.run()
    average_temperature_filler.run()
    if cas :
        tox_table_filler.run(cas)