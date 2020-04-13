from tools import QueryScript, list_agency_finder, translate
import pandas as pd
import env
import json
import datetime

## DONNE LE DEBUT DE CHAQUE TABLEAU DU EXCEL ##
def create_head_dataframe(campaigns_dict):

    list_dataframe_normal = []
    list_dataframe_filtered = []
    place_done = []
    matrix_filtered = []
    for campaign_id in campaigns_dict:
        matrix = []
        for place_id in campaigns_dict[campaign_id]["place"] :

            if campaigns_dict[campaign_id]["place"][place_id]["number"] not in place_done:
                place_done.append(campaigns_dict[campaign_id]["place"][place_id]["number"])
                matrix_filtered.append([campaigns_dict[campaign_id]["place"][place_id]["number"], translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])

            matrix.append([campaigns_dict[campaign_id]["number"], campaigns_dict[campaign_id]["place"][place_id]["number"], translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
        
        df_normal = pd.DataFrame(matrix)
        df_normal.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']
        list_dataframe_normal.append(df_normal)

    df_concat_normal = pd.concat(list_dataframe_normal)



    df_filtered = pd.DataFrame(matrix_filtered)
    df_filtered.columns = ['Numéro', 'Station de mesure', 'Code Agence']
    list_dataframe_filtered.append(df_filtered)
    return df_concat_normal, df_filtered, place_done

def create_head_special_dataframe(campaigns_dict, chemistry_measurepoint_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, tox_measurepoint_list):
    list_dataframe = []
    list_dataframe_7j = []
    list_dataframe_21j = []
    for campaign_id in campaigns_dict:
        matrix = []
        matrix_7j = []
        matrix_21j = []
        for place_id in campaigns_dict[campaign_id]["place"] :
            seperate_chemistry = []
            if "duplicate" in campaigns_dict[campaign_id]["place"][place_id] :
                if "chemistry" in campaigns_dict[campaign_id]["place"][place_id]["duplicate"] :
                    for measurepoint in campaigns_dict[campaign_id]["place"][place_id]["duplicate"]["chemistry"]:
                        if measurepoint not in seperate_chemistry:
                            seperate_chemistry.append(measurepoint)

            df_normal = None
            df_7j = None
            df_21j = None
            
            if len(seperate_chemistry):
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    if measurepoint_id in seperate_chemistry :
                        matrix.append([campaigns_dict[campaign_id]["number"], str(campaigns_dict[campaign_id]["place"][place_id]["number"])+' - '+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]), translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
                        if measurepoint_id in chemistry_7j_measurepoint_list :
                            matrix_7j.append([campaigns_dict[campaign_id]["number"], str(campaigns_dict[campaign_id]["place"][place_id]["number"])+' - '+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]), translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
                        if measurepoint_id in chemistry_21j_measurepoint_list :
                            matrix_21j.append([campaigns_dict[campaign_id]["number"], str(campaigns_dict[campaign_id]["place"][place_id]["number"])+' - '+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]), translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
            
            else :
                in_list = False
                in_7j_list = False
                in_21j_list = False
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    if measurepoint_id in chemistry_measurepoint_list:
                        in_list = True
                        if measurepoint_id in chemistry_7j_measurepoint_list:
                            in_7j_list = True
                        if measurepoint_id in chemistry_21j_measurepoint_list:
                            in_21j_list = True

                if in_list :
                    matrix.append([campaigns_dict[campaign_id]["number"], campaigns_dict[campaign_id]["place"][place_id]["number"], translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
                    if in_7j_list :
                        matrix_7j.append([campaigns_dict[campaign_id]["number"], campaigns_dict[campaign_id]["place"][place_id]["number"], translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])
                    if in_21j_list :
                        matrix_21j.append([campaigns_dict[campaign_id]["number"], campaigns_dict[campaign_id]["place"][place_id]["number"], translate(campaigns_dict[campaign_id]["place"][place_id]["name"]), campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'])


        if len(matrix):
            for row in matrix :
                df_normal = pd.DataFrame([row], columns=['Campagne', 'Numéro', 'Station de mesure', 'Code Agence'])
                list_dataframe.append(df_normal)
        if len(matrix_7j):
            for row in matrix_7j :
                df_7j = pd.DataFrame([row], columns=['Campagne', 'Numéro', 'Station de mesure', 'Code Agence'])
                list_dataframe_7j.append(df_7j)
        if len(matrix_21j):
            for row in matrix_21j :
                df_21j = pd.DataFrame([row], columns=['Campagne', 'Numéro', 'Station de mesure', 'Code Agence'])
                list_dataframe_21j.append(df_21j)
    if len(list_dataframe)>1 :
        df_concat = pd.concat(list_dataframe)
    else :
        df_concat = df_normal 
    if len(list_dataframe_7j)>1 :
        df_concat_7j = pd.concat(list_dataframe_7j)
    else :
        df_concat_7j = df_7j 
    if len(list_dataframe_21j)>1 :
        df_concat_21j = pd.concat(list_dataframe_21j)
    else :
        df_concat_21j = df_21j
   


    return df_concat, df_concat_7j, df_concat_21j

def create_campaigns_dict(references):
    campaigns_dict = {}
    place_list = []
    references_tuple = tuple(references) if len(references)>1  else "('"+references[0]+"')"
    data = QueryScript(f"SELECT Campaign.id, substring(Campaign.reference,-2,2), Place.id, Place.name, substring(Place.reference,-2,2), Measurepoint.id, Pack.id, Pack.nature, substring(Measurepoint.reference, -2, 2), Measurepoint.name FROM {env.DATABASE_RAW}.Place JOIN {env.DATABASE_RAW}.Campaign ON Campaign.id=Place.campaign_id JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.place_id=Place.id JOIN {env.DATABASE_RAW}.Pack ON Measurepoint.id=Pack.measurepoint_id WHERE Campaign.reference IN {references_tuple}").execute()
    for campaign_id, campaign_number, place_id, place_name, place_number, measurepoint_id, pack_id, pack_nature, measurepoint_number, measurepoint_name  in data :
        if campaign_id in campaigns_dict:
            if place_id in campaigns_dict[campaign_id]["place"]:
                # ici on regarde s'il n'y a pas deux points de mesure au sein de la même place qui ont un type de pack identique
                for measurepoint in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    for pack in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint]["pack"]:
                        if campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint]["pack"][pack]==pack_nature :
                            if "duplicate" in campaigns_dict[campaign_id]["place"][place_id]:
                                if pack_nature in campaigns_dict[campaign_id]["place"][place_id]["duplicate"] :
                                    campaigns_dict[campaign_id]["place"][place_id]["duplicate"][pack_nature][int(measurepoint_number)] = measurepoint_id
                                else :
                                    campaigns_dict[campaign_id]["place"][place_id]["duplicate"][pack_nature] = {campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint]["number"]:measurepoint,int(measurepoint_number):measurepoint_id}
                            else :    
                                campaigns_dict[campaign_id]["place"][place_id]["duplicate"] = {pack_nature:{campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint]["number"]:measurepoint,int(measurepoint_number):measurepoint_id}}
                #################################################################################################################
                if measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"][pack_id] = pack_nature
                else :
                    campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id] = {"number":int(measurepoint_number),"pack" : {pack_id :pack_nature}, "name": measurepoint_name}
            else :
                place_list.append(place_id)
                campaigns_dict[campaign_id]["place"][place_id] = {"name": place_name,"number":int(place_number), "measurepoint": {measurepoint_id: {"number":int(measurepoint_number),"pack" : {pack_id:pack_nature}, "name": measurepoint_name}}}
        else :
            place_list.append(place_id)
            campaigns_dict[campaign_id] =  {"number" : int(campaign_number), "place" :{place_id : {"name": place_name,"number":int(place_number), "measurepoint": {measurepoint_id: {"number":int(measurepoint_number),"pack" : {pack_id:pack_nature}, "name": measurepoint_name}}}}}
    agency_data = QueryScript(f"SELECT Place.id, Agency.code FROM {env.DATABASE_RAW}.Place JOIN {env.DATABASE_RAW}.Agency ON Place.agency_id=Agency.id WHERE Place.id IN {tuple(place_list) if len(place_list)>1 else '('+(str(place_list[0]) if len(place_list) else '0')+')'}").execute()
    for place_id, agency_code in agency_data:
        for campaign in campaigns_dict:
            for place in campaigns_dict[campaign]["place"]:
                if place==place_id:
                    campaigns_dict[campaign]["place"][place]["agency"] = agency_code
    with open('data.json','w') as outfile :
        json.dump(campaigns_dict, outfile)

    return campaigns_dict

def initialize(references):
    campaigns_dict = create_campaigns_dict(references)
    measurepoint_list = []
    chemistry_measurepoint_list = []
    chemistry_pack_list = []
    tox_measurepoint_list = []
    agency_code_list = []
    for campaign_id in campaigns_dict:
        for place_id in campaigns_dict[campaign_id]["place"]:
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for pack_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"]:
                    if campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["pack"][pack_id]=='chemistry':
                        if pack_id not in chemistry_pack_list :
                            chemistry_pack_list.append(int(pack_id))
                        if measurepoint_id not in chemistry_measurepoint_list:
                            chemistry_measurepoint_list.append(measurepoint_id)
                    else :
                        if measurepoint_id not in tox_measurepoint_list:
                            tox_measurepoint_list.append(measurepoint_id) 
                if measurepoint_id not in measurepoint_list:
                    measurepoint_list.append(measurepoint_id) 
            if "agency" in campaigns_dict[campaign_id]["place"][place_id]:
                agency_code_list.append(campaigns_dict[campaign_id]["place"][place_id]["agency"])
    
    # Détermination des J0, J14, J21, JN ainsi que les chimies 7j et 21j
    date_data = QueryScript(f"SELECT measurepoint_id, date_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+(str(measurepoint_list[0]) if len(measurepoint_list) else '0')+')'}").execute()
    date_dict = {}
    for measurepoint_id, date_id, date in date_data :
        if measurepoint_id in date_dict:
            date_dict[measurepoint_id][date_id] = date
        else :
            date_dict[measurepoint_id] = {date_id:date}

    J_dict = {}
    chemistry_7j_measurepoint_list = []
    chemistry_21j_measurepoint_list = []

    for campaign_id in campaigns_dict:

        for place_id in campaigns_dict[campaign_id]["place"] :
            nature_duplicate = None
            if "duplicate" in campaigns_dict[campaign_id]["place"][place_id]:
                nature_duplicate = list(campaigns_dict[campaign_id]["place"][place_id]["duplicate"].keys())
            [J0,J7,J14,J21,J28,JN] = [None]*6
            place_dates = []
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                measurepoint_dates = [None]*7
                if measurepoint_id in date_dict:
                    for date_id in date_dict[measurepoint_id]:
                        measurepoint_dates[date_id-1] = date_dict[measurepoint_id][date_id]
                    # Détermination chimie 7j ou 21j
                    if measurepoint_dates[6] and measurepoint_dates[5]:
                        if (measurepoint_dates[6]-measurepoint_dates[5]).days < 14:
                            chemistry_7j_measurepoint_list.append(measurepoint_id)
                        else :
                            chemistry_21j_measurepoint_list.append(measurepoint_id)
                    ###############################

                place_dates.append(measurepoint_dates)
            ## Nécessité de séparer les places
            need_to_be_seperate = False
            if nature_duplicate:
                number_of_measurepoints = len(place_dates)
                if "alimentation" in nature_duplicate :
                    for id_date in range(7):
                        starting_date_list = [place_dates[x][0] for x in range(number_of_measurepoints)]
                        for first_measurepoint_checked,_ in enumerate(starting_date_list):
                            for second_measurepoint_checked in range(first_measurepoint_checked+1, len(starting_date_list)):
                                if starting_date_list[second_measurepoint_checked] and starting_date_list[first_measurepoint_checked]:
                                    if abs((starting_date_list[second_measurepoint_checked]-starting_date_list[first_measurepoint_checked]).days) < 4:
                                        need_to_be_seperate= True
                if "chemistry" in nature_duplicate :
                    for id_date in range(7):
                        starting_date_list = [place_dates[x][5] for x in range(number_of_measurepoints)]
                        for first_measurepoint_checked,_ in enumerate(starting_date_list):
                            for second_measurepoint_checked in range(first_measurepoint_checked+1, len(starting_date_list)):
                                if starting_date_list[second_measurepoint_checked] and starting_date_list[first_measurepoint_checked]:
                                    if abs((starting_date_list[second_measurepoint_checked]-starting_date_list[first_measurepoint_checked]).days) < 4:
                                        need_to_be_seperate= True
                if "reproduction" in nature_duplicate :
                    for id_date in range(7):
                        starting_date_list = [place_dates[x][2] for x in range(number_of_measurepoints)]
                        for first_measurepoint_checked,_ in enumerate(starting_date_list):
                            for second_measurepoint_checked in range(first_measurepoint_checked+1, len(starting_date_list)):
                                if starting_date_list[second_measurepoint_checked] and starting_date_list[first_measurepoint_checked]:
                                    if abs((starting_date_list[second_measurepoint_checked]-starting_date_list[first_measurepoint_checked]).days) < 4:
                                        need_to_be_seperate= True
            if need_to_be_seperate:
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"] :
                    new_place_id = float(str(place_id)+"."+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]))
                    new_number = float(str(campaigns_dict[campaign_id]["place"][place_id]["number"])+'.'+str(campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["number"]))
                    campaigns_dict[campaign_id]["place"][new_place_id] = {"measurepoint" : {measurepoint_id : campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]}, "number": new_number, "name": campaigns_dict[campaign_id]["place"][place_id]["name"]+' - '+campaigns_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]["name"], "agency": campaigns_dict[campaign_id]["place"][place_id]["agency"] if "agency" in campaigns_dict[campaign_id]["place"][place_id] else 'ND'}
                campaigns_dict[campaign_id]["place"].pop(place_id)
                with open('data.json','w') as outfile :
                    json.dump(campaigns_dict, outfile)
                return initialize(campaigns_dict)
                        
            ###################################
            # Détermination du J0 et du JN
            for measurepoint_number, _ in enumerate(place_dates):
                for index in [0,5]:
                    if place_dates[measurepoint_number][index]:
                        if not J0 :
                            J0 = place_dates[measurepoint_number][index]
                        elif place_dates[measurepoint_number][index] < J0:
                            J0 = place_dates[measurepoint_number][index]
                if place_dates[measurepoint_number][3]:
                    JN = place_dates[measurepoint_number][3]
            ###################################

            for measurepoint_number, _ in enumerate(place_dates):
                for date_id, date in enumerate(place_dates[measurepoint_number]):
                    if date and date_id!=4 :
                        if (date-J0).days>3 and (date-J0).days<10 :
                            J7 = date
                        elif (date-J0).days>10 and (date-J0).days<17 :
                            J14 = date
                        elif (date-J0).days>17 and (date-J0).days<24 :
                            J21 = date
                        elif (date-J0).days>24 :
                            J28 = date
            
            J_dict[place_id] = {"J0": {"full_date": J0},"J7": {"full_date": J7},"J14": {"full_date": J14},"J21": {"full_date": J21},"JN": {"full_date": JN},"J28": {"full_date": J28},"N":None}
            [J0,J7,J14,J21,J28,JN] = [J.strftime("%d/%m/%Y") if J else None for J in [J0,J7,J14,J21,J28,JN]]
            J_dict[place_id]["J0"]["truncated_date"] = J0
            J_dict[place_id]["J7"]["truncated_date"] = J7
            J_dict[place_id]["J14"]["truncated_date"] = J14
            J_dict[place_id]["J21"]["truncated_date"] = J21
            J_dict[place_id]["JN"]["truncated_date"] = JN
            J_dict[place_id]["J28"]["truncated_date"] = J28
            if JN and J0 :
                J_dict[place_id]["N"] = (datetime.datetime.strptime(JN, '%d/%m/%Y')-datetime.datetime.strptime(J0, '%d/%m/%Y')).days
                       
    return campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, tox_measurepoint_list, agency_code_list, J_dict

