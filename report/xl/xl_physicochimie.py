from tools import QueryScript
import pandas as pd
from calcul.exposure_conditions.exposure_conditions import conditions
import env

def create_physicochimie_dataframe(head_dataframe, measurepoint_list, campaigns_dict, J_dict):
    context_data = QueryScript(f"SELECT measurepoint_id, recordedAt, conductivity, ph, oxygen FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    temperatures_data = QueryScript(f"SELECT measurepoint_id, sensor1_min, sensor1_average, sensor1_max, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max   FROM {env.DATABASE_TREATED}.average_temperature WHERE version=  {env.CHOSEN_VERSION()} and measurepoint_id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+str(measurepoint_list[0])+')'}").execute()
    global_matrix = []
    
    for campaign_id in campaigns_dict:
        matrix = []
        for place_id in campaigns_dict[campaign_id]["place"]:
            temp = [None]*19
            temp[0] =''
            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for mp_id, sensor1_min, sensor1_average, sensor1_max, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max in temperatures_data:
                    if measurepoint_id==mp_id:
                        if sensor2_min and sensor3_min:
                            temp[1] = round(sensor2_min,1) if sensor2_min < sensor3_min else round(sensor3_min,1)
                        elif not temp[1] and (sensor2_min or sensor3_min) :
                            temp[1] = round(sensor2_min,1) if sensor2_min else round(sensor3_min,1)
                        elif not sensor2_min and not sensor3_min and sensor1_min :
                            temp[1] = round(sensor1_min,1)
                        if sensor2_average :
                            temp[2] = round(sensor2_average,1)
                        elif sensor3_average:
                            temp[2] = round(sensor3_average,1)
                        elif not sensor2_average and not sensor3_average and sensor1_average :
                            temp[2] = round(sensor1_average,1)
                        if sensor2_max and sensor3_max:
                            temp[3] = round(sensor2_max,1) if sensor2_max > sensor3_max else round(sensor3_max,1)
                        elif not temp[3] and (sensor2_max or sensor3_max) :
                            temp[3] = round(sensor2_max,1) if sensor2_max else round(sensor3_max,1)
                        elif not sensor2_max and not sensor3_max and sensor1_max :
                            temp[3] = round(sensor1_max,1)
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
