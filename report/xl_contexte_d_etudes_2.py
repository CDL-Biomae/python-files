from tools import QueryScript


def list_mp(campaign_ref):
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM datesclees WHERE measurepoint_id IN (SELECT id FROM measurepoint WHERE place_id IN (SELECT id FROM place WHERE campaign_id in (SELECT id FROM campaign WHERE reference = '{campaign_ref}')));")
    return output.execute()

print(list_mp('AG-003-01'))