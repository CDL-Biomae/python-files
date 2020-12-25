from tools import QueryScript
import pandas as pd
import env

def create_physicochimie_dataframe(head_dataframe, measurepoint_list, campaigns_dict, J_dict):
    context_data = QueryScript(f"SELECT measurepoint_id, recordedAt, conductivity, ph, oxygen FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    temperatures_data = QueryScript(f"SELECT measurepoint_id, sensor1_min, sensor1_max, sensor2_min, sensor2_max, sensor3_min, sensor3_max, all_sensor_average   FROM {env.DATABASE_TREATED}.average_temperature WHERE version=  {env.CHOSEN_VERSION()} and measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    global_matrix = []
    
    for campaign_id in campaigns_dict:
        matrix = []
        for place_id in campaigns_dict[campaign_id]["place"]:
            temp = [None]*19
            temp[0] =''
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for mp_id, sensor1_min, sensor1_max, sensor2_min, sensor2_max, sensor3_min, sensor3_max, all_sensor_average in temperatures_data:
                    if measurepoint_id==mp_id:
                        if sensor3_min or sensor2_min or sensor1_min :
                            temp[1] = round(min(sensor1_min if sensor1_min else 50, sensor2_min if sensor2_min else 50, sensor3_min if sensor3_min else 50, temp[1] if temp[1] else 50),1)
                        if sensor3_max or sensor2_max or sensor1_max :
                            temp[3] = round(max(sensor1_max if sensor1_max else 0, sensor2_max if sensor2_max else 0, sensor3_max if sensor3_max else 0, temp[3] if temp[3] else 0),1)
                        if all_sensor_average :
                            temp[2] = round(all_sensor_average, 1)
                for mp_id, recordedAt, conductivity,ph, oxygen in context_data:
                    if measurepoint_id==mp_id:
                        for day, J in enumerate(J_dict[place_id]):
                            if day<5 and J_dict[place_id][J]["full_date"]==recordedAt :
                                if conductivity:
                                    temp[4+day] = conductivity
                                if ph:
                                    temp[9+day] = ph
                                if oxygen:
                                    temp[14+day] = oxygen
            if not temp[1]:
                temp[1]=""
            if not temp[2]:
                temp[2]=""
            if not temp[3]:
                temp[3]=""
            matrix.append(temp)
        global_matrix.append(matrix)
                
    if len(global_matrix)>1:
        list_dataframe = []
        for matrix in global_matrix :
            df =  pd.DataFrame(matrix, columns=['', 'Temperature minimum', 'Temperature moyenne', 'Temperature maximum','Conductivité J0','Conductivité J7', 'Conductivité J14', 'Conductivité J21', 'Conductivité JN',
                  'pH J0','ph J7', 'pH J14', 'pH J21', 'ph JN',
                  'Oxygène J0','Oxygène J7', 'Oxygène J14', 'Oxygène J21', 'Oxygène JN'])
            list_dataframe.append(df)
        df_values = pd.concat(list_dataframe)
    else :

        df_values = pd.DataFrame(global_matrix[0], columns=['', 'Temperature minimum', 'Temperature moyenne', 'Temperature maximum','Conductivité J0','Conductivité J7', 'Conductivité J14', 'Conductivité J21', 'Conductivité JN',
                  'pH J0','ph J7', 'pH J14', 'pH J21', 'ph JN',
                  'Oxygène J0','Oxygène J7', 'Oxygène J14', 'Oxygène J21', 'Oxygène JN'])
    
    df_values = df_values.dropna(how="all", axis='columns')
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_physicochimie = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_physicochimie
