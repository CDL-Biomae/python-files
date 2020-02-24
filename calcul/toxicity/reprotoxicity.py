from tools import QueryScript, fusion_id_finder
from calcul.toxicity.reproduction import * 
from math import *
import numbers
from collections import Counter


def number_days_exposition(dict_pack_fusion):
    nature = 'reproduction'
    list_mp_repro = []
    for mp in dict_pack_fusion:
        try:
            pack_id = dict_pack_fusion[mp][nature]
        except KeyError:
            pass
        else:
            list_mp_repro.append(mp)

    # Récupération des dates de début et de fin
    output_dates_debut = QueryScript(
        f"SELECT measurepoint_fusion_id, date FROM key_dates where date_id=6 and measurepoint_fusion_id IN {tuple(list_mp_repro)};"
    ).execute()
    output_dates_fin = QueryScript(
        f"SELECT measurepoint_fusion_id, date FROM key_dates where date_id=4 and measurepoint_fusion_id IN {tuple(list_mp_repro)};"
    ).execute()

    output_mp_debut = [x[0] for x in output_dates_debut]
    output_mp_fin = [x[0] for x in output_dates_fin]

    dict_dates_debut_fin = {}  # {mp: [date_debut, date_fin]}
    for mp in list_mp_repro:
        idx_debut = output_mp_debut.index(mp)
        idx_fin = output_mp_fin.index(mp)
        dict_dates_debut_fin[mp] = [output_dates_debut[idx_debut][1], output_dates_fin[idx_fin][1]]

    # Initialisation du dictionnaire de sortie
    dict_nbr_days_exposition = {}  # {mp: nbrdays}
    for mp in dict_pack_fusion:
        dict_nbr_days_exposition[mp] = None

    # Calcul
    for mp in list_mp_repro:
        [date_debut, date_fin] = dict_dates_debut_fin[mp]
        if date_debut is not None and date_fin is not None:
            if date_debut is None and date_fin is None:
                dict_nbr_days_exposition[mp] = "NA"
            else:
                nbrdays = (date_fin - date_debut).days
                dict_nbr_days_exposition[mp] = nbrdays
        else:
            dict_nbr_days_exposition[mp] = "NA"

    return dict_nbr_days_exposition


def index_fecundity_female(list_pack_repro):
    SQL_request = f"SELECT pack_id, female, molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total FROM biomae.measurereprotoxicity where pack_id IN {tuple(list_pack_repro)};"
    output = QueryScript(SQL_request).execute()

    # Initialisation du dictionnaire de la requête mise en forme
    # {pack_id: {'px_to_mm': int, 'data': [[molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total], [...]] }}
    dict_result = {pack_id: {'px_to_mm': None, 'data': []} for pack_id in list_pack_repro}

    pack_errors = []

    for row in output:
        [pack_id, female, molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total] = row

        if female == '' or female == '0bis':
            continue

        if int(female) == 0:  # Valeur étalon
            try:
                px_to_mm = specimen_size_mm/specimen_size_px
            except TypeError:
                pack_errors.append(pack_id)
                continue
            dict_result[pack_id]['px_to_mm'] = px_to_mm
        elif female is not None:  # Données à traiter ensuite
            data = [molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total]
            dict_result[pack_id]['data'].append(data)

    # Initialisation du dictionnaire de sortie
    dict_index_fecundity = {pack_id: {'list_molting_stage': [], 'list_index_fecundity': []} for pack_id in list_pack_repro}

    for pack_id in dict_result.keys():
        data = dict_result[pack_id]['data']
        px_to_mm = dict_result[pack_id]['px_to_mm']
        for row in data:
            [molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total] = row

            if len(row) == 0:
                dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
            else:
                dict_index_fecundity[pack_id]['list_molting_stage'].append(molting_stage)
                if embryo_stage in [2, 3, 4]:
                    if embryo_total == 0:
                        dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
                    else:
                        if specimen_size_mm is None or specimen_size_mm == 0:
                            if specimen_size_px == 0:
                                continue
                            try:
                                specimen_size_mm = specimen_size_px * px_to_mm
                            except TypeError:
                                pack_errors.append(pack_id)
                                continue
                        if specimen_size_mm == 0:
                            pack_errors.append(pack_id)
                            continue
                        dict_index_fecundity[pack_id]['list_index_fecundity'].append(embryo_total/(specimen_size_mm-5))
                else:
                    dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
    print(f"Il y a eu des erreurs pour les calculs de fécondité des packs suivants: {list(set(pack_errors))}")
    return dict_index_fecundity  # {pack_id: {'list_molting_stage': [...], 'list_index_fecundity': [...]}


def fecundity(dict_pack_fusion):  # retourne le nombre de femelles concernées et la fécondité moyenne de chaque pack
    nature = 'reproduction'
    list_pack_repro = []
    list_mp_repro = []
    for mp in dict_pack_fusion:
        try:
            pack_id = dict_pack_fusion[mp][nature]
        except KeyError:
            pass
        else:
            list_mp_repro.append(mp)
            list_pack_repro.append(pack_id)

    dict_index_fecundity = index_fecundity_female(list_pack_repro)  # {pack_id: {'list_molting_stage': [...], 'list_index_fecundity': [...]}

    # Initialisation du dictionnaire de sortie
    # {mp_fusion: {{'nbr_femelles_analysées': int, 'nbr_femelles_concernées': int, 'fécondité_moyenne': float}}
    dict_fecundity = {mp_fusion: {'nbr_femelles_analysées': None, 'nbr_femelles_concernées': None, 'fécondité_moyenne': None} for mp_fusion in dict_pack_fusion.keys()}

    for pack_id in dict_index_fecundity.keys():
        list_index_fecundity = dict_index_fecundity[pack_id]['list_index_fecundity']
        list_molting_stage = dict_index_fecundity[pack_id]['list_molting_stage']
        mp_fusion = list_mp_repro[list_pack_repro.index(pack_id)]

        nbr_femelles_concernees = len(list_index_fecundity) - list_index_fecundity.count(0)
        dict_fecundity[mp_fusion]['nbr_femelles_concernées'] = nbr_femelles_concernees

        cpt_molting_stage = Counter(list_molting_stage)
        cpt_filtre = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1', 'c2', 'd1', 'd2']]

        nbr_femelles_analysees = 0
        for x in cpt_filtre:
            if x is not None:
                nbr_femelles_analysees += x

        if nbr_femelles_analysees == 0:
            dict_fecundity[mp_fusion]['nbr_femelles_analysées'] = 'NA'
        else:
            dict_fecundity[mp_fusion]['nbr_femelles_analysées'] = nbr_femelles_analysees

        if nbr_femelles_analysees > 10 and len(list_index_fecundity) != 0:
            fecondite_moyenne = sum(list_index_fecundity)/len(list_index_fecundity)
        else:
            fecondite_moyenne = "NA"
        dict_fecundity[mp_fusion]['fécondité_moyenne'] = fecondite_moyenne

    return dict_fecundity  # {mp_fusion: {{'nbr_femelles_analysées': int, 'nbr_femelles_concernées': int, 'fécondité_moyenne': float}}


# Cycle de mue
def molting_cycle(dict_pack_fusion):
    nature = 'reproduction'
    list_pack_repro = []
    list_mp_repro = []
    for mp in dict_pack_fusion:
        try:
            pack_id = dict_pack_fusion[mp][nature]
        except KeyError:
            pass
        else:
            list_mp_repro.append(mp)
            list_pack_repro.append(pack_id)

    SQL_request = f"SELECT pack_id, molting_stage FROM biomae.measurereprotoxicity where pack_id IN {tuple(list_pack_repro)};"
    SQL_request_2 = f"SELECT measurepoint_fusion_id, expected_C2,expected_D2 FROM biomae.temperature_repro where measurepoint_fusion_id IN {tuple(list_mp_repro)};"
    resultat_molting_stage =  QueryScript(SQL_request).execute()
    resultat_expected_stage =  QueryScript(SQL_request_2).execute()

    dict_molting_stage = {pack_id: [] for pack_id in list_pack_repro}
    for row in resultat_molting_stage:
        [pack_id, molting_stage] = row
        dict_molting_stage[pack_id].append(molting_stage)

    dict_expected_stage = {mp_fusion: {'expected C2': None, 'expected D2': None} for mp_fusion in list_mp_repro}
    for row in resultat_expected_stage:
        [measurepoint_fusion_id, expected_C2, expected_D2] = row
        dict_expected_stage[measurepoint_fusion_id]['expected C2'] = expected_C2
        dict_expected_stage[measurepoint_fusion_id]['expected D2'] = expected_D2

    # Initialisation du dictionnaire de sortie
    dict_molting = {mp_fusion: {'cycle de mue': None, 'cycle de mue attendu': None} for mp_fusion in dict_pack_fusion.keys()}

    # Remplissage du dictionnaire de sortie
    for i, mp_fusion in enumerate(list_mp_repro):
        pack_id = list_pack_repro[i]
        dict_molting[mp_fusion]['cycle de mue attendu'] = dict_expected_stage[mp_fusion]['expected C2']

        list_molting_stage = dict_molting_stage[pack_id]
        cpt_molting_stage = Counter(list_molting_stage)
        cpt_analysees = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1', 'c2', 'd1', 'd2']]
        cpt_c2_d1 = [cpt_molting_stage.get(molting_stage) for molting_stage in ['c2', 'd1']]

        nbr_femelles_analysees = 0
        for x in cpt_analysees:
            if x is not None:
                nbr_femelles_analysees += x

        nbr_femelles_c2_d1 = 0
        for x in cpt_c2_d1:
            if x is not None:
                nbr_femelles_c2_d1 += x

        if nbr_femelles_analysees == 0:
            molting_percent = 'NA'
        else:
            molting_percent = nbr_femelles_c2_d1/nbr_femelles_analysees

        dict_molting[mp_fusion]['cycle de mue'] = molting_percent if molting_percent == 'NA' else molting_percent*100

    return dict_molting  # {mp_fusion: {'cycle de mue': ..%, 'cycle de mue attendu': ..%}}


    #  n p6 (TOXFILE) il manque des variable dans la base de donner c'est pour cela les resultat sont pas identique


def number_female_concerned_area(pack_id):
          SQL_request = "SELECT molting_stage,oocyte_area_pixel,oocyte_area_pixel,oocyte_area_mm FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
          resultat =  QueryScript(SQL_request).execute()
          
          Area_delayµm = [] 
          Area_delay = []
          nbr_f_c = 0

          for i in range(len(resultat)-1):
                              
               if resultat[i][1]==None or resultat[i][1]==0 or resultat[i][3]==0 or resultat[i][2]:
                    Area_delayµm.append('ND') # si tous les resultat dans la base donnée c'est vide sinn dans notre cas c'est NO DATA
               else:
                    Area_delayµm.append(resultat[i][1]*(resultat[i][2]/resultat[i][3]/97,82))


          for i in range(len(resultat)-1): 
               if resultat[i][0] != None:               
                    if (resultat[i][0].upper()=='C1' or resultat[i][0].upper()=='B'):
                         if Area_delayµm[i]=='ND':  #si aArea_delayµm[i] == 0 ou bien not defiend
                              Area_delay.append('ND')  # 0 ça veut dire le vide 
                         else:
                              Area_delay.append(Area_delayµm[i])
                              nbr_f_c = nbr_f_c +1
                    else:
                         Area_delay.append('NDV')# c'est le vide 
               else:
                    Area_delay.append('ND')  

          return nbr_f_c, Area_delay


def inhibition_fertility_and_threshold_5_1(pack_id):
     #  change where by name not by id
     SQL_request = "SELECT value FROM biomae.r2_constant where name IN('indice de fertilité attendu - moyenne','Constante fertilité 1','indice de fertilité attendu - sd','Constante fertilité 2')"
     resultat =  QueryScript(SQL_request).execute()
     fertility = []
     if isinstance(index_fertility_average(pack_id),numbers.Number): 
          if resultat[2] != 0:
                fertility.append(100*(resultat[2]-index_fertility_average(pack_id))/resultat[2]) #  % inhibition - FECONDITE
                fertility.append( (resultat[2]-(resultat[2]-resultat[0]*resultat[3]/sqrt(number_female_concerned(pack_id))))/resultat[2]*100 )  #  Seuil 1% fécondité      
                fertility.append( (resultat[2]-(resultat[2]-resultat[1]*resultat[3]/sqrt(number_female_concerned(pack_id))))/resultat[2]*100 )  #  Seuil 5% fécondité    
          else:
               return "NA"
     
     else:
          return "NA"
     
     if number_female_analysis(pack_id)<10:
          return "NA"
     else:
          return fertility

def Result_Fertility(pack_id):
     inhibition = inhibition_fertility_and_threshold_5_1(pack_id)

     if isinstance(index_fertility_average(pack_id),numbers.Number): 
        if number_female_analysis(pack_id)<10:
            return "NA"
        elif  inhibition[0]>inhibition[1] and inhibition[0]>inhibition[2]:
            return "inhibition fort"
        elif  inhibition[0]>inhibition[1] and inhibition[0]<inhibition[2]:
            return "inhibition modérée"
        elif inhibition[0]<inhibition[1]:
            return "conforme"
        else:
          return "NDV"
     else:
          return "NA"
          
def endocrine_disruption(pack_id):
     somme = 0  
     female_concerned = number_female_concerned_area(pack_id)

     if Result_Fertility(pack_id) == "conforme" or Result_Fertility(pack_id)=="NA":
          return "NA"
     else:
          if number_female_analysis(pack_id)<10 or number_female_analysis(pack_id)=="NA" :
               return 'NA'
          else:
               
               if female_concerned[0] != 0 :     
                    for i in range(len(female_concerned[1])):
                         if female_concerned[i] != "ND":
                              somme = somme+female_concerned[i]
                    return  somme/female_concerned[0]
               else:
                    return "ND"
               
                       




               
   


     






          
          
          










  
    



     
     
     
     

    
