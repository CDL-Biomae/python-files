from tools import QueryScript
from . import leaf_size, specimen_size

def alimentation_inhibition(pack_id):
    constant_alim = QueryScript(
        "SELECT value FROM r2_constant WHERE name LIKE 'Constante alim%'").execute()

    eaten_leaves = leaf_size(pack_id)
    size = specimen_size(pack_id)

    mean_size = sum(size)/len(size)
    inhibition_replicate = []

    expected_eaten_value = constant_alim[0] * 12 + constant_alim[1] + constant_alim[2] * (
        mean_size - constant_alim[3])  # 12 est à changer par la température moyenne
    inhibition_list = [(eaten_leaf - expected_eaten_value) /
                       expected_eaten_value for eaten_leaf in eaten_leaves]

    return sum(inhibition_list)/len(inhibition_list)*100