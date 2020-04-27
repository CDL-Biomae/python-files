import pandas as pd
from calcul.chemistry import survival
from tools import QueryScript, translate
import datetime
import env

## CREATE DATAFRAME ##
def create_edi_dataframe(campaign, place_dict, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont les sandres précisés dans /calcul/chemistry/nqe
    Les colonnes vides sont supprimées
    :param place_dict:
    :return: dataframe:
    '''
    measurepoint_data = QueryScript(f"SELECT id, city, zipcode, r0_threshold, r0_sample_taken, r0_aspect, r0_iridescence, r0_foam, r0_leafs, r0_sludge, r0_other_bodies, r0_color, r0_clearness, r0_odor, r0_shadow, r0_weather, r0_hydrological_situation, r0_scale, r0_secchi, r0_air_temperature, r0_oxygen_saturation, r21_threshold, r21_sample_taken, r21_aspect, r21_iridescence, r21_foam, r21_leafs, r21_sludge, r21_other_bodies, r21_color, r21_clearness, r21_odor, r21_shadow, r21_weather, r21_hydrological_situation, r21_scale, r21_secchi, r21_air_temperature, r21_oxygen_saturation FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(chemistry_measurepoint_list) if len(chemistry_measurepoint_list)>1 else '('+(str(chemistry_measurepoint_list[0]) if len(chemistry_measurepoint_list) else '0')+')'}").execute()
    dates_data = QueryScript(f"SELECT measurepoint_id, date_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_id IN {tuple(chemistry_measurepoint_list) if len(chemistry_measurepoint_list)>1 else '('+(str(chemistry_measurepoint_list[0]) if len(chemistry_measurepoint_list) else '0')+')'}").execute()
    conditions_data = QueryScript(f"SELECT measurepoint_id, recordedAt, temperature, conductivity, ph, oxygen, comment FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id IN {tuple(chemistry_measurepoint_list) if len(chemistry_measurepoint_list)>1 else '('+(str(chemistry_measurepoint_list[0]) if len(chemistry_measurepoint_list) else '0')+')'}").execute()
    pack_data = QueryScript(f"SELECT id, sampling_weight, metal_tare_bottle_weight, organic_tare_bottle_weight, organic_total_weight, sampling_comment  FROM {env.DATABASE_RAW}.Pack WHERE id IN {tuple(chemistry_pack_list) if len(chemistry_pack_list)>1 else '('+(str(chemistry_pack_list[0]) if len(chemistry_pack_list) else '0')+')'}").execute()
    survival_dict = survival(chemistry_pack_list)
    matrix= []
    for place_id in place_dict :
        temp = [None]*72
        start_time = None
        end_time = None
        temp[15] = "biomae"
        temp[41] = "biomae"
        if "agency" in place_dict[place_id]:
            temp[1] = place_dict[place_id]["agency"]
        if "number" in place_dict[place_id]:
            number = place_dict[place_id]["number"] 
            temp[8] = f"{campaign}-{'0'+str(number) if number<10 else number }" 
        for measurepoint_id in place_dict[place_id]["measurepoint"]:
            for mp_id, date_id, date in dates_data:
                if mp_id==measurepoint_id:
                    if date_id==6 and date and not start_time:
                        start_time=date
                        temp[14] = date.strftime("%d/%m/%Y")
                        temp[0] = date
                    if date_id==7 and date and not end_time:
                        end_time=date
                        temp[40] = date.strftime("%d/%m/%Y")
            place_dict[place_id]["measurepoint"][measurepoint_id]["start_time"] = start_time
            place_dict[place_id]["measurepoint"][measurepoint_id]["end_time"] = end_time
            if temp[40] and temp[14]:
                temp[9] = (datetime.datetime.strptime(temp[40], '%d/%m/%Y')-datetime.datetime.strptime(temp[14], '%d/%m/%Y')).days
            for mp_id, city, zipcode, r0_threshold, r0_sample_taken, r0_aspect, r0_iridescence, r0_foam, r0_leafs, r0_sludge, r0_other_bodies, r0_color, r0_clearness, r0_odor, r0_shadow, r0_weather, r0_hydrological_situation, r0_scale, r0_secchi, r0_air_temperature, r0_oxygen_saturation, r21_threshold, r21_sample_taken, r21_aspect, r21_iridescence, r21_foam, r21_leafs, r21_sludge, r21_other_bodies, r21_color, r21_clearness, r21_odor, r21_shadow, r21_weather, r21_hydrological_situation, r21_scale, r21_secchi, r21_air_temperature, r21_oxygen_saturation in measurepoint_data:
                if mp_id==measurepoint_id:
                    try :
                        int(zipcode)
                        temp[5] = translate(city)
                    except ValueError:
                        temp[5] = translate(zipcode)
                    except TypeError:
                        pass
                    temp[20] = r0_oxygen_saturation
                    temp[21] = r0_air_temperature
                    temp[22] = r0_threshold
                    temp[23] = r0_sample_taken
                    temp[24] = r0_aspect
                    temp[25] = r0_iridescence
                    temp[26] = r0_foam
                    temp[27] = r0_leafs
                    temp[28] = r0_sludge
                    temp[29] = r0_other_bodies
                    temp[30] = r0_color
                    temp[31] = r0_clearness
                    temp[32] = r0_odor
                    temp[33] = r0_shadow
                    temp[34] = r0_weather
                    temp[35] = r0_hydrological_situation
                    temp[36] = r0_scale
                    temp[37] = r0_secchi

                    temp[46] = r21_oxygen_saturation
                    temp[47] = r21_air_temperature
                    temp[48] = r21_threshold
                    temp[49] = r21_sample_taken
                    temp[50] = r21_aspect
                    temp[51] = r21_iridescence
                    temp[52] = r21_foam
                    temp[53] = r21_leafs
                    temp[54] = r21_sludge
                    temp[55] = r21_other_bodies
                    temp[56] = r21_color
                    temp[57] = r21_clearness
                    temp[58] = r21_odor
                    temp[59] = r21_shadow
                    temp[60] = r21_weather
                    temp[61] = r21_hydrological_situation
                    temp[62] = r21_scale
                    temp[63] = r21_secchi
            for mp_id, recordedAt, temperature, conductivity, ph, oxygen, comment in conditions_data:
                if mp_id==measurepoint_id:
                    if recordedAt == place_dict[place_id]["measurepoint"][measurepoint_id]["start_time"]:
                        temp[16]=temperature
                        temp[17]=ph
                        temp[18]=conductivity
                        temp[19]=oxygen
                    
                    if recordedAt == place_dict[place_id]["measurepoint"][measurepoint_id]["end_time"]:
                        temp[42]=temperature
                        temp[43]=ph
                        temp[44]=conductivity
                        temp[45]=oxygen
                        if comment:
                            dissociated_comment = [information.replace("\n",", ") for information in comment.split("\t")]
                            need_to_be_removed = []
                            for information in dissociated_comment:
                                if information!="":
                                    if len(information)>=10 and information[:10]=="Vandalisme":
                                        place_dict[place_id]["vandalism"] = True
                                    if information[-1]=="%" or "Scan" in information or "#" in information or 'RAS' in information:
                                        need_to_be_removed.append(information)
                                    else :
                                        try :
                                            int(information)
                                            need_to_be_removed.append(information)
                                        except ValueError :
                                            pass
                            for element in need_to_be_removed:
                                dissociated_comment.remove(element)
                            if len(dissociated_comment):
                                temp[65] = '. '.join([translate(information) for information in dissociated_comment]) 
            for pack_id in place_dict[place_id]["measurepoint"][measurepoint_id]["pack"]:
                if place_dict[place_id]["measurepoint"][measurepoint_id]["pack"][pack_id]=='chemistry':
                    if pack_id in survival_dict:
                        temp[64]=survival_dict[pack_id]
                    for pack,sampling_weight, metal_tare_bottle_weight, organic_tare_bottle_weight, organic_total_weight, comment in pack_data:
                        if pack==pack_id:
                            temp[66]= metal_tare_bottle_weight
                            temp[67]= sampling_weight
                            temp[68]= organic_tare_bottle_weight
                            temp[69]= organic_total_weight
                            if comment :
                                dissociated_comment = [information.replace("\n",", ") for information in comment.split("\t")]
                                need_to_be_removed = []
                                for information in dissociated_comment:
                                    if information!="":
                                        if len(information)>=10 and information[:10]=="Vandalisme":
                                            place_dict[place_id]["vandalism"] = True
                                        if information[-1]=="%" or "Scan" in information or "#" in information or 'RAS' in information:
                                            need_to_be_removed.append(information)
                                        else :
                                            try :
                                                int(information)
                                                need_to_be_removed.append(information)
                                            except ValueError :
                                                pass
                                for element in need_to_be_removed:
                                    dissociated_comment.remove(element)
                                if len(dissociated_comment):
                                    if temp[65]:
                                        temp[65] += '. '.join([translate(information) if information else '' for information in dissociated_comment]) 
                                    else :
                                        temp[65] = '. '.join([translate(information) if information else '' for information in dissociated_comment]) 


        matrix.append(temp)
                    

    df = pd.DataFrame(matrix)
    df.columns = ["Mois", "Code Agence  Station", "Code Plvt EDI", "N° Prélèvement", "Département", "Commune", "Lieu prel", "", "Réfèrence BIOMAE",	"Durée du prélèvement","Taux de Lyophylisation (à patir de l'Eppendorf)",	"Taux de Lyophylisation (à patir du flacon verre)", "N° Prélèvement Eau Sup Encagement", "", "Date d'encagement", "Préleveur","Température de l'Eau", "Potentiel en Hydrogène (pH)", "Conductivité à  25°C", "Oxygène dissous", "Taux de saturation en oxygène", "Température de l'air", "Seuil", "Echantillon pris","Aspect","Irisations sur l'eau", "Présence de mousse de détergents à la surface", "Présence de produits ligneux ou herbacés frais", "Boue", "Autres corps", "Couleur", "Clarté", "Odeur", "Ombre", "Conditions météorologiques pendant le prélèvement", "Situation hydrologique apparente", "Echelle", "Secchi", "N° Prélèvement Eau Sup", "",	"Date de prélèvement",	"Préleveur","Température de l'Eau", "Potentiel en Hydrogène (pH)", "Conductivité à 25°C","Oxygène dissous", "Taux de saturation en oxygène", "Température de l'air", "Seuil", "Echantillon pris","Aspect","Irisations sur l'eau", "Présence de mousse de détergents à la surface", "Présence de produits ligneux ou herbacés frais", "Boue", "Autres corps", "Couleur", "Clarté", "Odeur", "Ombre", "Conditions météorologiques pendant le prélèvement", "Situation hydrologique apparente", "Echelle", "Secchi", "Taux de survie", "Commentaires", "Tare Eppendorf en mg", "Eppendorf + Echantillon en mg", "Tare Flacon Verre en mg", "Flacon Verre + Echantillon en mg", "Eppendorf + Echantillon Lyophilisé en mg", "Flacon Verre + Echantillon Lyophilisé en mg"]

    return df


