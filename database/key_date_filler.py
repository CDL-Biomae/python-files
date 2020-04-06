
from tools import QueryScript
import env

def create_global_dict():
    output = QueryScript(f'SELECT Place.id, Measurepoint.id, MeasureExposureCondition.id, MeasureExposureCondition.step, MeasureExposureCondition.recordedAt,MeasureExposureCondition.barrel, Pack.id, Pack.nature FROM {env.DATABASE_RAW}.Place JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.place_id=Place.id JOIN {env.DATABASE_RAW}.MeasureExposureCondition ON MeasureExposureCondition.measurepoint_id=Measurepoint.id JOIN {env.DATABASE_RAW}.Pack ON Pack.measurepoint_id=Measurepoint.id').execute()
    print(f'{len(output)} rows loaded')
    global_dict = {"data":  {}}

    for [place_id, measurepoint_id, measureExposureCondition_id, measureExposureCondition_step, measureExposureCondition_recordedAt, measureExposureCondition_barrel, pack_id, pack_nature] in output:
        [place_id, measurepoint_id, measureExposureCondition_id, measureExposureCondition_step, measureExposureCondition_recordedAt, pack_id, pack_nature] = [str(element) for element in [place_id, measurepoint_id, measureExposureCondition_id, measureExposureCondition_step, measureExposureCondition_recordedAt, pack_id, pack_nature]]
        if place_id not in list(global_dict["data"].keys()):
            global_dict["data"][place_id]={measurepoint_id:{"measureExposureCondition":{measureExposureCondition_id:{"step":measureExposureCondition_step,"recordedAt":measureExposureCondition_recordedAt,"barrel":measureExposureCondition_barrel}},"pack":{pack_id:pack_nature}}}
        else :
            if measurepoint_id not in list(global_dict["data"][place_id].keys()):
                global_dict["data"][place_id][measurepoint_id]={"measureExposureCondition":{measureExposureCondition_id:{"step":measureExposureCondition_step,"recordedAt":measureExposureCondition_recordedAt,"barrel":measureExposureCondition_barrel}},"pack":{pack_id:pack_nature}}
            else :
                if pack_id not in list(global_dict["data"][place_id][measurepoint_id]["pack"].keys()):
                    global_dict["data"][place_id][measurepoint_id]["pack"][pack_id]=pack_nature
                if measureExposureCondition_id not in list(global_dict["data"][place_id][measurepoint_id]["measureExposureCondition"].keys()) :
                    global_dict["data"][place_id][measurepoint_id]["measureExposureCondition"][measureExposureCondition_id]={"step":measureExposureCondition_step,"recordedAt":measureExposureCondition_recordedAt,"barrel":measureExposureCondition_barrel}
    return global_dict

def order_dates(measureExposureCondition, chemistry_present):
    dates_sorted = [None]*7
    chemistry_end_stored = False
    for measureExposureCondition_id in measureExposureCondition:
        if measureExposureCondition[measureExposureCondition_id]["step"]=="50" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="R0":
            dates_sorted[0] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="60" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="R7":
            dates_sorted[1] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="20" and not measureExposureCondition[measureExposureCondition_id]["barrel"]:
            dates_sorted[2] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="140" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="RN":
            dates_sorted[3] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="170" and not measureExposureCondition[measureExposureCondition_id]["barrel"]:
            dates_sorted[4] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="50" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="R0":
            dates_sorted[5] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
        if measureExposureCondition[measureExposureCondition_id]["step"]=="100" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="R21":
            dates_sorted[6] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
            chemistry_end_stored = True
    if not chemistry_end_stored and chemistry_present:
        for measureExposureCondition_id in measureExposureCondition:
            if measureExposureCondition[measureExposureCondition_id]["step"]=="60" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="R7" :
                dates_sorted[6] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]
            elif not dates_sorted[6] and chemistry_present and measureExposureCondition[measureExposureCondition_id]["step"]=="140" and measureExposureCondition[measureExposureCondition_id]["barrel"]=="RN":
                dates_sorted[6] = measureExposureCondition[measureExposureCondition_id]["recordedAt"]

    return dates_sorted
        
def intersection(liste1, liste2):
    liste3 = [x for x in liste1 if x in liste2]
    return liste3


def insert_key_dates():
    QueryScript(f"DROP TABLE IF EXISTS key_dates").execute(True)
    QueryScript(f'CREATE TABLE key_dates (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT, date_id INT, date DATETIME, version INT)').execute(True)
    insertion = QueryScript(f" INSERT INTO key_dates (measurepoint_id, date_id, date, version) VALUES (%s, %s, %s, %s)")
    values = []
    global_dict = create_global_dict()
    fusion = 0
    for place_id in global_dict["data"]:
        for measurepoint_id in global_dict["data"][place_id]:
            chemistry_present = False
            for pack_id in global_dict["data"][place_id][measurepoint_id]["pack"]:
                if global_dict["data"][place_id][measurepoint_id]["pack"][pack_id]=='chemistry':
                    chemistry_present = True
            for i, date in enumerate(order_dates(global_dict["data"][place_id][measurepoint_id]["measureExposureCondition"], chemistry_present)):
                values.append((int(measurepoint_id), i+1, date))
    insertion.setRows(values)
    insertion.executemany()    

def run():
    print("--> key_dates table")
    insert_key_dates()
    print("--> key_dates table ready")