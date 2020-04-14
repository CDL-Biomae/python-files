from tools import QueryScript, translate
from report import initialize
from calcul import survival
import env
import json
import datetime

def load_data(reference):
    campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, _, _, _, agency_code_list, J_dict = initialize([reference])
    year = None
    agency_data = QueryScript(f"SELECT code, network, hydroecoregion, latitude, longitude FROM {env.DATABASE_RAW}.Agency  WHERE code IN {tuple(agency_code_list) if len(agency_code_list)>1 else '('+(str(agency_code_list[0]) if len(agency_code_list) else '0')+')'};").execute()
    context_data = QueryScript(f"SELECT measurepoint_id, recordedAt, temperature, conductivity, ph, oxygen, type, comment FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    temperatures_data = QueryScript(f"SELECT measurepoint_id, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max   FROM {env.DATABASE_TREATED}.average_temperature WHERE version=  {env.CHOSEN_VERSION()} and measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    geographic_data = QueryScript(f"SELECT id, latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted, city, zipcode, stream, latitude, longitude FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    place_reference_data = QueryScript(f"SELECT Place.id, Place.reference FROM {env.DATABASE_RAW}.Measurepoint JOIN {env.DATABASE_RAW}.Place ON Place.id= Measurepoint.place_id WHERE Measurepoint.id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    chemistry_survival = survival(chemistry_pack_list)
    global_matrix = []
    place_dict = {}
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
            place_dict[place_id]["condition"] = {"temperature_min":None, "temperature_max": None, "average_temperature":None, "J0":{}, "J7":{},"J14":{}, "J21":{}, "JN":{}}
        for measurepoint_id in place_dict[place_id]["measurepoint"]:
            for pack_id in place_dict[place_id]["measurepoint"][measurepoint_id]["pack"]:
                if pack_id in chemistry_survival:
                    place_dict[place_id]["chemistry_survival"] = chemistry_survival[pack_id]
            for mp_id, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max in temperatures_data:
                if measurepoint_id==mp_id:
                    if sensor2_min and sensor3_min:
                        place_dict[place_id]["condition"]["temperature_min"] = round(sensor2_min,1) if sensor2_min < sensor3_min else round(sensor3_min,1)
                    elif sensor2_min or sensor3_min :
                        place_dict[place_id]["condition"]["temperature_min"] = round(sensor2_min,1) if sensor2_min else round(sensor3_min,1)
                    if sensor2_average :
                        place_dict[place_id]["condition"]["average_temperature"] = round(sensor2_average,1)
                    elif sensor3_average:
                        place_dict[place_id]["condition"]["average_temperature"] = round(sensor3_average,1)
                    if sensor2_max and sensor3_max:
                        place_dict[place_id]["condition"]["temperature_max"] = round(sensor2_max,1) if sensor2_max > sensor3_max else round(sensor3_max,1)
                    elif sensor2_max or sensor3_max :
                        place_dict[place_id]["condition"]["temperature_max"] = round(sensor2_max,1) if sensor2_max else round(sensor3_max,1)
            for mp_id, recordedAt,temperature, conductivity, ph, oxygen, barrel_type, comment in context_data:
                if measurepoint_id==mp_id:
                    for J in J_dict[place_id]:  
                        if J!="J28" and J!="N" and J_dict[place_id][J]["full_date"] and J_dict[place_id][J]["full_date"]==recordedAt :
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
                            if barrel_type :
                                place_dict[place_id]["barrel_type"] = barrel_type

                            place_dict[place_id]["condition"][J]["date"] = (J_dict[place_id][J]["full_date"]).strftime("%d/%m/%Y %H:%M")
                            if not year : 
                                year = J_dict[place_id][J]["full_date"].year
            for mp_id, latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted, city, zipcode, stream, latitude, longitude in geographic_data:
                if mp_id==measurepoint_id :
                    if latitudeSpotted :
                        place_dict[place_id]["latitudeSpotted"] = f"{latitudeSpotted}".replace(',', '.')
                    if longitudeSpotted :
                        place_dict[place_id]["longitudeSpotted"] = f"{longitudeSpotted}".replace(',', '.')
                    if lambertXSpotted :
                        place_dict[place_id]["lambertXSpotted"] = f"{lambertXSpotted}".replace(',', '.')
                    if lambertYSpotted :
                        place_dict[place_id]["lambertYSpotted"] = f"{lambertYSpotted}".replace(',', '.')
                    if city :
                        place_dict[place_id]["city"] = translate(city)
                    if zipcode :
                        place_dict[place_id]["zipcode"] = zipcode
                    if stream:
                        place_dict[place_id]["stream"] = f"{stream}".replace(',', '.')
                    if latitude :
                        place_dict[place_id]["latitude"] = f"{latitude}".replace(',', '.')
                    if longitude :
                        place_dict[place_id]["longitude"] = f"{longitude}".replace(',', '.')
    with open('data.json','w') as outfile :
        json.dump(place_dict, outfile)
    return place_dict, year
