import env
from tools import QueryScript
import datetime

def create_global_dict() :
    packs = QueryScript(f'SELECT Pack.id, Measurepoint.id FROM {env.DATABASE_RAW}.Pack JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.id=Pack.measurepoint_id').execute()
    key_dates =  QueryScript(f'SELECT measurepoint_id, date_id, date FROM {env.DATABASE_TREATED}.key_dates').execute()
    temperatures = QueryScript(f'SELECT measurepoint_id, pack_id, recordedAt, value, nature FROM {env.DATABASE_RAW}.MeasureTemperature WHERE recordedAt<="2017-00-00 00:00:00"').execute()
    print(f'{len(temperatures)} rows loaded')
    temperatures2=QueryScript(f'SELECT measurepoint_id, pack_id, recordedAt, value, nature FROM {env.DATABASE_RAW}.MeasureTemperature WHERE recordedAt<="2018-00-00 00:00:00" AND recordedAt>="2017-00-00 00:00:00"').execute()
    for element in temperatures2 :
        temperatures.append(element)
    print(f'{len(temperatures)} rows loaded')
    temperatures2=QueryScript(f'SELECT measurepoint_id, pack_id, recordedAt, value, nature FROM {env.DATABASE_RAW}.MeasureTemperature WHERE recordedAt<="2019-00-00 00:00:00" AND recordedAt>="2018-00-00 00:00:00"').execute()
    for element in temperatures2 :
        temperatures.append(element)
    print(f'{len(temperatures)} rows loaded')
    temperatures2=QueryScript(f'SELECT measurepoint_id, pack_id, recordedAt, value, nature FROM {env.DATABASE_RAW}.MeasureTemperature WHERE recordedAt<="2020-00-00 00:00:00" AND recordedAt>="2019-00-00 00:00:00"').execute()
    for element in temperatures2 :
        temperatures.append(element)
    print(f'{len(temperatures)} rows loaded')
    temperatures2=QueryScript(f'SELECT measurepoint_id, pack_id, recordedAt, value, nature FROM {env.DATABASE_RAW}.MeasureTemperature WHERE recordedAt<="2021-00-00 00:00:00" AND recordedAt>="2020-00-00 00:00:00"').execute()
    for element in temperatures2 :
        temperatures.append(element)
    print(f'{len(temperatures)} rows loaded')
    global_dict = {"data":{}}
    for pack_id, measurepoint_id in packs:
        measurepoint_id = measurepoint_id
        if measurepoint_id in global_dict["data"]:
            if pack_id not in global_dict["data"][measurepoint_id]:
                global_dict["data"][measurepoint_id]["packs"].append(pack_id)
        else :
            global_dict["data"][measurepoint_id]= {"packs":[pack_id]}
    for measurepoint_id, date_id, date in key_dates:
        measurepoint_id = measurepoint_id
        if measurepoint_id in global_dict["data"]:
            if "key_dates" in global_dict["data"][measurepoint_id]:
                global_dict["data"][measurepoint_id]["key_dates"][date_id] = str(date) if date else None
            else :
                global_dict["data"][measurepoint_id]["key_dates"] = {date_id: str(date) if date else None}
        else :
            global_dict["data"][measurepoint_id] ={"key_dates":{date_id: str(date) if date else None}} 


    current_measurepoint_id = str(temperatures[0][0]) if temperatures[0][0] else None
    current_key_dates = {}
    count = 0
    no_key_dates_mp_id_list = []
    for mp_id, pack_id, recordedAt, value, nature in temperatures:
        recordedAt =   str(recordedAt) if recordedAt else None
        count+=1
        can_be_stored = False
        is_lab = False
        if mp_id :
            if not mp_id==current_measurepoint_id:
                for measurepoint in global_dict["data"]:
                    if measurepoint==mp_id :
                        current_measurepoint_id = measurepoint

        elif pack_id :
            for measurepoint in global_dict["data"]:
                if "packs" in global_dict["data"][measurepoint] and pack_id in global_dict["data"][measurepoint]["packs"]:
                    current_measurepoint_id = measurepoint
        if current_measurepoint_id==None :
            print("Point sans pack_id ni measurepoint_id")
        elif "key_dates" in global_dict["data"][current_measurepoint_id] :
            for key_date in global_dict["data"][current_measurepoint_id]["key_dates"]:
                current_key_dates[key_date] = global_dict["data"][current_measurepoint_id]["key_dates"][key_date]


            if nature=="sensor1" and (1 in current_key_dates and 2 in current_key_dates) :
                if current_key_dates[1]:
                    start_date = str(datetime.datetime.strptime(current_key_dates[1], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(0,3600))
                else :
                    start_date = None
                end_date =  current_key_dates[2]
                if start_date and end_date :
                    
                    if (recordedAt <= end_date and recordedAt >= start_date):
                        can_be_stored = True
                    
            elif nature=="sensor2" and (3 in current_key_dates and 4 in current_key_dates and 5 in current_key_dates):
                if current_key_dates[3]:
                    start_date = str(datetime.datetime.strptime(current_key_dates[3], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(0,3600)) 
                else :
                    start_date = None
                end_date =  current_key_dates[4]
                lab_date =  current_key_dates[5]
                if start_date and lab_date and (recordedAt <= lab_date and recordedAt >= start_date) :
                    is_lab =True
                if start_date and end_date and (recordedAt <= end_date and recordedAt >= start_date):
                    can_be_stored = True                
            elif nature=="sensor3" and (6 in current_key_dates and 7 in current_key_dates):
                if current_key_dates[6]:
                    start_date = str(datetime.datetime.strptime(current_key_dates[6], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(0,3600)) 
                else :
                    start_date = None
                end_date =  current_key_dates[7]
                if start_date and end_date and (recordedAt <= end_date and recordedAt >= start_date):
                    can_be_stored = True
            if value :
                if can_be_stored:
                    if nature in global_dict["data"][current_measurepoint_id]:
                        global_dict["data"][current_measurepoint_id][nature].append(value)
                    else :
                        global_dict["data"][current_measurepoint_id][nature] = [value]
                if is_lab :
                    if "sensor2lab" in global_dict["data"][current_measurepoint_id]:
                        global_dict["data"][current_measurepoint_id]["sensor2lab"].append(value)
                    else :
                        global_dict["data"][current_measurepoint_id]["sensor2lab"] = [value]
            if count %10000==0:
                print(f'{count} rows sorted')
    
    return global_dict

def insert_average_temperature(global_dict) :
    QueryScript("DROP TABLE IF EXISTS biomae_treated.average_temperature").execute()
    average_temperature_table = QueryScript("CREATE TABLE average_temperature (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT(11), sensor1_average DOUBLE, sensor1_min DOUBLE, sensor1_max DOUBLE, sensor2_average DOUBLE, sensor2_min DOUBLE, sensor2_max DOUBLE, sensor3_average DOUBLE, sensor3_min DOUBLE, sensor3_max DOUBLE, sensor2_average_labo DOUBLE, version INT );")
    average_temperature_table.execute(True)
    insertion = QueryScript(f" INSERT INTO average_temperature (measurepoint_id, sensor1_average, sensor1_min, sensor1_max, sensor2_average, sensor2_min, sensor2_max, sensor3_average, sensor3_min, sensor3_max, sensor2_average_labo, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    output = []
    for measurepoint_id in global_dict["data"]:
        if measurepoint_id != "None" :
            row = [measurepoint_id]
            if "sensor1" in global_dict["data"][measurepoint_id]:
                row.append(sum(global_dict["data"][measurepoint_id]["sensor1"])/len(global_dict["data"][measurepoint_id]["sensor1"]))
                row.append(min(global_dict["data"][measurepoint_id]["sensor1"]))
                row.append(max(global_dict["data"][measurepoint_id]["sensor1"]))
            else:
                row+=[None]*3
            if "sensor2" in global_dict["data"][measurepoint_id]:
                row.append(sum(global_dict["data"][measurepoint_id]["sensor2"])/len(global_dict["data"][measurepoint_id]["sensor2"]))
                row.append(min(global_dict["data"][measurepoint_id]["sensor2"]))
                row.append(max(global_dict["data"][measurepoint_id]["sensor2"]))
            else:
                row+=[None]*3
            if "sensor3" in global_dict["data"][measurepoint_id]:
                row.append(sum(global_dict["data"][measurepoint_id]["sensor3"])/len(global_dict["data"][measurepoint_id]["sensor3"]))
                row.append(min(global_dict["data"][measurepoint_id]["sensor3"]))
                row.append(max(global_dict["data"][measurepoint_id]["sensor3"]))
            else:
                row+=[None]*3
            if "sensor2lab" in global_dict["data"][measurepoint_id]:
                row.append(sum(global_dict["data"][measurepoint_id]["sensor2lab"])/len(global_dict["data"][measurepoint_id]["sensor2lab"]))
            else :
                row.append(None)
            output.append(tuple(row))
    insertion.setRows(output)
    insertion.executemany()

def run():
    print("--> average_temperature table")
    global_dict = create_global_dict()
    insert_average_temperature(global_dict)
    print("--> average_temperature table ready")
    return global_dict