from tools import QueryScript, fusion_id_finder
from calcul.toxicity.reproduction import * 
from math import *
import numbers


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
    dict_nbr_days_exposition = {}
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

def size_female_mm(pack_id):
     SQL_request = "SELECT specimen_size_mm, specimen_size_px, embryo_total FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     siz_female_mm =[]
     resultat2 =  QueryScript(SQL_request).execute()
     if(resultat2[len(resultat2)-1][1]!=0):     
          for i in range (len(resultat2)-1):
               siz_female_mm.append(resultat2[i][1]*resultat2[len(resultat2)-1][0]/resultat2[len(resultat2)-1][1])
     
     #print(siz_female_mm)

     return siz_female_mm


def index_fertility_female_X(pack_id):
     SQL_request = "SELECT embryo_stage, embryo_total FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     
     resultat =  QueryScript(SQL_request).execute()
     index_female =[]
    
     for i in range (len(resultat)-1):
       if resultat[i][0]!=None:
               if (resultat[i][0]>=2 and resultat[i][0]<=4):
                      if resultat[i][1] == 0:
                           index_female.append(0) 
                      else:
                           index_female.append(resultat[i][1]/(size_female_mm(pack_id)[i]-5))
               else:
                    index_female.append(0)
       else:
             index_female.append(0)  
          
     return index_female


      # n L6 (TOXFILE)
def number_female_concerned(pack_id):
     female = index_fertility_female_X(pack_id)
     Nbr = 0
     for i in range(len(female)-1):
          if female[i]==0:
              Nbr = Nbr+1
     
     return len(female)-Nbr

     #  n N6 (TOXFILE)
def number_female_analysis(pack_id):
     SQL_request = "SELECT molting_stage FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     resultat =  QueryScript(SQL_request).execute()
     Nbr_B_C1 = 0
     Nbr_C2_D1 = 0
     Nbr_D2 = 0

     for i in range(len(resultat)-1):
          if resultat[i] != None:
               if resultat[i].upper()=='B' or resultat[i].upper()=='C1':
                    Nbr_B_C1 = Nbr_B_C1+1
               elif resultat[i].upper()=='C2' or resultat[i].upper()=='D1':
                    Nbr_C2_D1=Nbr_C2_D1+1
               elif resultat[i].upper()=='D2':
                     Nbr_D2 =  Nbr_D2+1
          

     if Nbr_B_C1+Nbr_C2_D1+Nbr_D2 == 0:
          return 'NA'
     else:
          return  Nbr_B_C1+Nbr_C2_D1+Nbr_D2

               
     

   # Fécondité 
def index_fertility_average(pack_id):
     number_female= number_female_analysis(pack_id)
    
     if type(number_female) == int:
           if number_female<10:
                 return "NA"
           else:
                 return sum(index_fertility_female_X(pack_id))/len(index_fertility_female_X(pack_id))
     else: 
          return "NA"




 # Fécondité Cycle de mue
def molting_cycle(pack_id):
     fusion_id = fusion_id_finder(pack_id)
    
     SQL_request = "SELECT molting_stage FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     SQL_request_tmp = "SELECT expected_C2,expected_D2 FROM biomae.temperature_repro where measurepoint_fusion_id="+str(fusion_id)
     resultat =  QueryScript(SQL_request).execute()
     resultat2 =  QueryScript(SQL_request_tmp).execute()
   
     Nbr_C2_D1 = 0
     for i in range(len(resultat)-1):
          if resultat[i] != None: 
                if resultat[i].upper()=='C2' or resultat[i].upper()=='D1':
                    Nbr_C2_D1=Nbr_C2_D1+1


     if female_survivor(pack_id)=='NA' or number_female_analysis(pack_id) =='NA' or number_female_analysis(pack_id) == 0:
              return "NA"
     else:
           molting = Nbr_C2_D1/number_female_analysis(pack_id)*100
           if resultat2==[] or resultat2[0][0] == None or resultat2[0][1]==None:
                molting = str(round(molting)) +"%"
           else:
                molting = str(round(molting)) +"%("+str(round(resultat2[0][0]-resultat2[0][1]))+")%"


     # molting = round(molting) +"%" + round( Max Température repro % attendu au moins en C2 - MAX Température repro % attendu  au moins en D2)
     
  
     return molting

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
               
                       




               
   


     






          
          
          










  
    



     
     
     
     

    
