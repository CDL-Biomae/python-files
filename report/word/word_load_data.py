from tools import QueryScript, translate, convert_gps_into_lambert
from report import initialize
from calcul import survival
import env
import json
import datetime

def load_data(reference):
    campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, _, _, tox_measurepoint_list, agency_code_list, J_dict = initialize([reference])

    agency_data = QueryScript(f"SELECT code, network, hydroecoregion, latitude, longitude FROM {env.DATABASE_RAW}.Agency  WHERE code IN {tuple(agency_code_list) if len(agency_code_list)>1 else '('+(str(agency_code_list[0]) if len(agency_code_list) else '0')+')'};").execute()
    context_data = QueryScript(f"SELECT measurepoint_id, recordedAt, temperature, conductivity, ph, oxygen, type, comment FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    temperatures_data = QueryScript(f"SELECT measurepoint_id, sensor1_min, sensor1_average, sensor1_max, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max   FROM {env.DATABASE_TREATED}.average_temperature WHERE version=  {env.CHOSEN_VERSION()} and measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    geographic_data = QueryScript(f"SELECT id, latitudeSpotted, longitudeSpotted, lambertX, lambertY, city, zipcode, stream FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    place_reference_data = QueryScript(f"SELECT Place.id, Place.reference FROM {env.DATABASE_RAW}.Measurepoint JOIN {env.DATABASE_RAW}.Place ON Place.id= Measurepoint.place_id WHERE Measurepoint.id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    conform_threshold = QueryScript(f"SELECT parameter, min, max FROM {env.DATABASE_TREATED}.r1 WHERE version={env.CHOSEN_VERSION()}").execute()
    conform_chemistry_portion_test = QueryScript(f"SELECT Measurepoint.id, (organic_total_weight-organic_tare_bottle_weight)>2500 FROM {env.DATABASE_RAW}.Pack JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.id=Pack.measurepoint_id WHERE Measurepoint.id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'} and Pack.nature='chemistry'").execute()
    chemistry_survival = survival(chemistry_pack_list)
    

    place_dict = {}
    year = None
    week_start_number = None
    week_end_number = None
    for campaign_id in campaigns_dict:
        place_dict = campaigns_dict[campaign_id]["place"]
    for place_id in place_dict:
        for place, reference in place_reference_data:
            if place_id==place :
                place_dict[place_id]["reference"] = reference
        for code, network, hydroecoregion, latitudeTh, longitudeTh in agency_data :
            if "agency" in place_dict[place_id] and place_dict[place_id]["agency"]==code:
                if network :
                    place_dict[place_id]["network"] = network 
                if hydroecoregion :
                    place_dict[place_id]["hydroecoregion"] = hydroecoregion 
                if latitudeTh :
                    place_dict[place_id]["latitudeTh"] = latitudeTh 
                if longitudeTh :
                    place_dict[place_id]["longitudeTh"] = longitudeTh 
        if "condition" not in place_dict[place_id]:
            place_dict[place_id]["condition"] = {"temperature_min":None, "temperature_max": None,"alimentation_average_temperature_min":None,"alimentation_average_temperature_max":None, "reproduction_average_temperature_min":None, "reproduction_average_temperature_max":None,"chemistry_average_temperature_min":None, "chemistry_average_temperature_max":None,"average_temperature":None, "J0":{}, "J7":{},"J14":{}, "J21":{}, "JN":{}}
        for measurepoint_id in place_dict[place_id]["measurepoint"]:

            ### Add chemistry _survival
            for pack_id in place_dict[place_id]["measurepoint"][measurepoint_id]["pack"]:
                if pack_id in chemistry_survival:
                    place_dict[place_id]["chemistry_survival"] = chemistry_survival[pack_id]
            ### Add temperature data
            for mp_id, sensor1_min, sensor1_average, sensor1_max, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max in temperatures_data:
                if measurepoint_id==mp_id:

                    if sensor1_average:
                        if place_dict[place_id]["condition"]["alimentation_average_temperature_min"]:
                            place_dict[place_id]["condition"]["alimentation_average_temperature_min"] = min(sensor1_average, place_dict[place_id]["condition"]["alimentation_average_temperature_min"])
                        else :
                            place_dict[place_id]["condition"]["alimentation_average_temperature_min"] = sensor1_average
                        if place_dict[place_id]["condition"]["alimentation_average_temperature_max"]:
                            place_dict[place_id]["condition"]["alimentation_average_temperature_max"] = max(sensor1_average, place_dict[place_id]["condition"]["alimentation_average_temperature_max"])
                        else :
                            place_dict[place_id]["condition"]["alimentation_average_temperature_max"] = sensor1_average

                    if sensor2_average:
                        if place_dict[place_id]["condition"]["reproduction_average_temperature_min"]:
                            place_dict[place_id]["condition"]["reproduction_average_temperature_min"] = min(sensor2_average, place_dict[place_id]["condition"]["reproduction_average_temperature_min"])
                        else :
                            place_dict[place_id]["condition"]["reproduction_average_temperature_min"] = sensor2_average
                        if place_dict[place_id]["condition"]["reproduction_average_temperature_max"]:
                            place_dict[place_id]["condition"]["reproduction_average_temperature_max"] = max(sensor2_average, place_dict[place_id]["condition"]["reproduction_average_temperature_max"])
                        else :
                            place_dict[place_id]["condition"]["reproduction_average_temperature_max"] = sensor2_average

                    if sensor3_average:
                        if place_dict[place_id]["condition"]["chemistry_average_temperature_min"]:
                            place_dict[place_id]["condition"]["chemistry_average_temperature_min"] = min(sensor3_average, place_dict[place_id]["condition"]["chemistry_average_temperature_min"])
                        else :
                            place_dict[place_id]["condition"]["chemistry_average_temperature_min"] = sensor3_average
                        if place_dict[place_id]["condition"]["chemistry_average_temperature_max"]:
                            place_dict[place_id]["condition"]["chemistry_average_temperature_max"] = max(sensor3_average, place_dict[place_id]["condition"]["chemistry_average_temperature_max"])
                        else :
                            place_dict[place_id]["condition"]["chemistry_average_temperature_max"] = sensor3_average
                    if sensor1_min or sensor2_min or sensor3_min:
                        last_value, sensor1_min, sensor2_min, sensor3_min = [element if element!=None else 100 for element in [place_dict[place_id]["condition"]["temperature_min"], sensor1_min, sensor2_min, sensor3_min]]
                        place_dict[place_id]["condition"]["temperature_min"] = round(min(last_value, sensor1_min, sensor2_min, sensor3_min),1)
                    if sensor1_max or sensor2_max or sensor3_max:
                        last_value, sensor1_max, sensor2_max, sensor3_max = [element if element!=None else -100 for element in [place_dict[place_id]["condition"]["temperature_max"], sensor1_max, sensor2_max, sensor3_max]]
                        place_dict[place_id]["condition"]["temperature_max"] = max(last_value, sensor1_max, sensor2_max, sensor3_max)
                    if sensor1_average and not place_dict[place_id]["condition"]["average_temperature"] :
                        place_dict[place_id]["condition"]["average_temperature"] = round(sensor1_average,1)
                    if sensor2_average :
                        place_dict[place_id]["condition"]["average_temperature"] = round(sensor2_average,1)
                    elif sensor3_average:
                        place_dict[place_id]["condition"]["average_temperature"] = round(sensor3_average,1)

            ### Add context data
            for mp_id, recordedAt,temperature, conductivity, ph, oxygen, barrel_type, comment in context_data:
                if measurepoint_id==mp_id:
                    if barrel_type :
                        place_dict[place_id]["barrel_type"] = barrel_type
                    for J in J_dict[place_id]:  
                        if J!="J28" and J!="N" and J_dict[place_id][J]["full_date"] and J_dict[place_id][J]["full_date"]==recordedAt :
                            if not week_start_number:
                                week_start_number = J_dict[place_id][J]["full_date"].isocalendar()[1]
                            elif J_dict[place_id][J]["full_date"].isocalendar()[1] < week_start_number:
                                week_start_number = J_dict[place_id][J]["full_date"].isocalendar()[1]
                            if not week_end_number:
                                week_end_number = J_dict[place_id][J]["full_date"].isocalendar()[1]
                            elif J_dict[place_id][J]["full_date"].isocalendar()[1] > week_end_number:
                                week_end_number = J_dict[place_id][J]["full_date"].isocalendar()[1]
                            if conductivity:
                                place_dict[place_id]["condition"][J]["conductivity"] = conductivity
                            if ph:
                                place_dict[place_id]["condition"][J]["ph"] = ph
                            if oxygen:
                                place_dict[place_id]["condition"][J]["oxygen"] = oxygen
                            if temperature :
                                place_dict[place_id]["condition"][J]["temperature"] = temperature
                            if comment :
                                place_dict[place_id]["condition"][J]["comment"] = comment

                            place_dict[place_id]["condition"][J]["date"] = (J_dict[place_id][J]["full_date"]).strftime("%d/%m/%Y %H:%M")
                            if not year : 
                                year = J_dict[place_id][J]["full_date"].year

            ### Add geographic data                    
            for mp_id, latitudeSpotted, longitudeSpotted, lambertX, lambertY, city, zipcode, stream in geographic_data:
                if mp_id==measurepoint_id :
                    if latitudeSpotted and longitudeSpotted :
                        place_dict[place_id]["latitudeSpotted"] = f"{latitudeSpotted}".replace(',', '.')
                        place_dict[place_id]["longitudeSpotted"] = f"{longitudeSpotted}".replace(',', '.')
                        lambertXSpotted, lambertYSpotted = convert_gps_into_lambert(latitudeSpotted, longitudeSpotted)
                        place_dict[place_id]["lambertXSpotted"] = f"{round(lambertXSpotted,1)}".replace(',', '.')
                        place_dict[place_id]["lambertYSpotted"] = f"{round(lambertYSpotted,1)}".replace(',', '.')
                    if lambertX and lambertY :
                        place_dict[place_id]["lambertX"] = f"{lambertX}".replace(',', '.')
                        place_dict[place_id]["lambertY"] = f"{lambertY}".replace(',', '.')

                    if city :
                        place_dict[place_id]["city"] = translate(city)
                    if zipcode :
                        place_dict[place_id]["zipcode"] = zipcode
                    if stream:
                        place_dict[place_id]["stream"] = f"{stream}".replace(',', '.')
            
            ### Add conformity
            place_dict[place_id]["not conform"] = []
            for parameter, min_treshold, max_threshold in conform_threshold:
                
                ### chemistry conformity
                if measurepoint_id in chemistry_measurepoint_list :
                    if parameter == 'Température moyenne (chimie)' :
                        if place_dict[place_id]["condition"]["chemistry_average_temperature_min"] and (min_treshold > place_dict[place_id]["condition"]["chemistry_average_temperature_min"] or place_dict[place_id]["condition"]["chemistry_average_temperature_max"] > max_threshold) :
                            if not "chemistry_temperature" in place_dict[place_id]["not conform"] :
                                place_dict[place_id]["not conform"].append("chemistry_temperature")
                    if parameter == 'Oxygène (chimie)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "oxygen" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["oxygen"] and min_treshold > place_dict[place_id]["condition"][J]["oxygen"] :
                                    if not "oxygen" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("oxygen")
                    if parameter == 'Conductivité (chimie)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "conductivity" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["conductivity"] and (min_treshold > place_dict[place_id]["condition"][J]["conductivity"] or place_dict[place_id]["condition"][J]["conductivity"] > max_threshold):
                                    if not "conductivity" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("conductivity")
                    if parameter == 'pH (chimie)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "ph" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["ph"] and (min_treshold > place_dict[place_id]["condition"][J]["ph"] or place_dict[place_id]["condition"][J]["ph"] > max_threshold):
                                    if not "ph" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("ph")
                    
                ### toxicity conformity
                if measurepoint_id in tox_measurepoint_list :
                    if parameter == 'Température moyenne (toxicité)':
                        if place_dict[place_id]["condition"]["alimentation_average_temperature_min"] and (min_treshold > place_dict[place_id]["condition"]["alimentation_average_temperature_min"] or place_dict[place_id]["condition"]["alimentation_average_temperature_max"] > max_threshold) :
                            if not "alimentation_temperature" in place_dict[place_id]["not conform"] :
                                place_dict[place_id]["not conform"].append("alimentation_temperature")
                        if place_dict[place_id]["condition"]["reproduction_average_temperature_min"] and (min_treshold > place_dict[place_id]["condition"]["reproduction_average_temperature_min"] or place_dict[place_id]["condition"]["reproduction_average_temperature_max"] > max_threshold) :
                            if not "reproduction_temperature" in place_dict[place_id]["not conform"] :
                                place_dict[place_id]["not conform"].append("reproduction_temperature")
                    if parameter == 'Oxygène (toxicité)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "oxygen" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["oxygen"] and min_treshold > place_dict[place_id]["condition"][J]["oxygen"] :
                                    if not "oxygen" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("oxygen")
                    if parameter == 'Conductivité (toxicité)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "conductivity" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["conductivity"] and (min_treshold > place_dict[place_id]["condition"][J]["conductivity"] or place_dict[place_id]["condition"][J]["conductivity"] > max_threshold):
                                    if not "conductivity" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("conductivity")
                    if parameter == 'pH (toxicité)':
                        for J in place_dict[place_id]["condition"]:
                            if J[0]=='J' and place_dict[place_id]["condition"][J] and "ph" in place_dict[place_id]["condition"][J]:
                                if place_dict[place_id]["condition"][J]["ph"] and (min_treshold > place_dict[place_id]["condition"][J]["ph"] or place_dict[place_id]["condition"][J]["ph"] > max_threshold):
                                    if not "ph" in place_dict[place_id]["not conform"] :
                                        place_dict[place_id]["not conform"].append("ph")
            ### Add chemistry portion validation 
            for mp_id, result in conform_chemistry_portion_test:
                if mp_id==measurepoint_id: 
                    place_dict[place_id]["chemistry portion validation"] = result
                    

    with open('data.json','w') as outfile :
        json.dump(place_dict, outfile)
    return place_dict, year, week_start_number, week_end_number
