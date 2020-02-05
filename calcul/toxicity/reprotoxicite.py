from tools import QueryScript, fusion_id_finder
from calcul.toxicity.reproduction import * 
from math import *


def Nbr_Days_Exposition(pack_id):
     fusion_id = fusion_id_finder(pack_id)
     SQL_request = "SELECT date FROM datesclees where date_id IN(4,6) and measurepoint_fusion_id="+str(fusion_id)
     LR_dates =  QueryScript(SQL_request).execute()
     
     if(LR_dates!=""):
          return "NA"
     else:
          nbrdays =  LR_dates[0]-LR_dates[1]
          return nbrdays.days

def size_female_mm(pack_id):
     SQL_request = "SELECT specimen_size_mm, specimen_size_px embryo_total FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     siz_female_mm =[]
     resultat2 =  QueryScript(SQL_request).execute()
          
     for i in range (len(resultat2)-1):
          siz_female_mm.append(resultat2[i][1]*resultat2[len(resultat2)-1][0]/resultat2[len(resultat2)-1][1])

     return siz_female_mm


def Index_Fertility_female_X(pack_id):
     SQL_request = "SELECT embryo_stage, embryo_total FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     
     resultat =  QueryScript(SQL_request).execute()
     index_female =[]
    
     for i in range (len(resultat)-1):
          if resultat[i][0]>=2 and resultat[i][0]<=4:
               if resultat[i][1] == 0:
                   index_female.append(0) 
               else:
                    index_female.append(resultat[i][1]/(size_female_mm(pack_id)[i]-5))
          else:
                index_female.append(0)


     
     return index_female


      # n L6 (TOXFILE)
def nbr_female_concerned(pack_id):
     female = Index_Fertility_female_X(pack_id)
     Nbr = 0
     for i in range(len(female)-1):
          if female[i]==0:
              Nbr = Nbr+1
     
     return len(female)-Nbr

     #  n N6 (TOXFILE)
def Nbr_female_analysis(pack_id):
     SQL_request = "SELECT molting_stage FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     resultat =  QueryScript(SQL_request).execute()
     Nbr_B_C1 = 0
     Nbr_C2_D1 = 0
     Nbr_D2 = 0

     for i in range(len(resultat)-1):
          if resultat[i].upper()=='B' or resultat[i].upper()=='C1':
               Nbr_B_C1 = Nbr_B_C1+1
          elif resultat[i].upper()=='C2' or resultat[i].upper()=='D1':
                Nbr_C2_D1=Nbr_C2_D1+1
          elif resultat[i].upper()=='D2':
                Nbr_D2 =  Nbr_D2+1
               
     return  Nbr_B_C1+Nbr_C2_D1+Nbr_D2

   # Fécondité 
def Index_fertility_moy(pack_id):
     Nbr_female= Nbr_female_analysis(pack_id)
     if Nbr_female<10 :
          return "NA"
     else:
          return sum(Index_Fertility_female_X(pack_id))/len(Index_Fertility_female_X(pack_id))




 # Fécondité Cycle de mue
def Moulting_cycle(pack_id):
     fusion_id = fusion_id_finder(pack_id)
     SQL_request = "SELECT molting_stage FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
     SQL_request_tmp = "SELECT expected_C2,expected_D2 FROM biomae.temperature_repro where measurepoint_fusion_id="+str(fusion_id)
     resultat =  QueryScript(SQL_request).execute()
     resultat2 =  QueryScript(SQL_request_tmp).execute()
     Nbr_C2_D1 = 0
     for i in range(len(resultat)-1):
          if resultat[i].upper()=='C2' or resultat[i].upper()=='D1':
                Nbr_C2_D1=Nbr_C2_D1+1
          

     if female_survivor(pack_id)=='NA':
          return "NA"
     else:
           Moulting = Nbr_female_analysis(pack_id)/Nbr_C2_D1*100

     #  Moulting = round(Moulting) +"%" + round( Max Température repro % attendu au moins en C2 - MAX Température repro % attendu  au moins en D2)
     Moulting = str(round(Moulting)) +"%("+str(round(resultat2[0][0]-resultat2[0][1]))+")%"
  
     return Moulting

    #  n p6 (TOXFILE)
def nbr_female_concerned_area(pack_id):
          SQL_request = "SELECT molting_stage,oocyte_area_pixel,oocyte_area_pixel,oocyte_area_mm FROM biomae.measurereprotoxicity where pack_id ="+str(pack_id)
          resultat =  QueryScript(SQL_request).execute()
          Area_delayµm = [] 
          Area_delay = []
          nbr_f_c = 0
          for i in range(len(resultat)-1):
                    if resultat[i][1]==None:
                         Area_delayµm.append(None)
                    else:
                          Area_delayµm.append(resultat[i][1]*(resultat[i][2]/resultat[i][3]/97,82))


          for i in range(len(resultat)-1):               
                if resultat[i][0].upper()=='C1' or resultat[i][0].upper()=='B':
                     if Area_delayµm[i]==None:
                         Area_delay.append(0)
                     else:
                         Area_delay.append(Area_delayµm[i])
                         nbr_f_c = nbr_f_c +1
          return nbr_f_c, Area_delayµm


def Inhibition_fertility_ANd_Threshold_5_1(pack_id):
     #  change where by name not by id
     SQL_request = "SELECT value FROM biomae.r2_constant where id IN(24,22,25,23)"
     resultat =  QueryScript(SQL_request).execute()
     fertility = []
     fertility.append(100*(resultat[2]-Index_fertility_moy(pack_id))/resultat[2]) #  % INHIBITION - FECONDITE
     fertility.append( (resultat[2]-(resultat[2]-resultat[0]*resultat[3]/sqrt(nbr_female_concerned(pack_id))))/resultat[2]*100 )  #  Seuil 1% fécondité      
     fertility.append( (resultat[2]-(resultat[2]-resultat[1]*resultat[3]/sqrt(nbr_female_concerned(pack_id))))/resultat[2]*100 )  #  Seuil 5% fécondité    
     if Nbr_female_analysis(pack_id)<10:
          return "NA"
     else:
          return fertility

def Result_Fertility(pack_id):
     Inhibition = Inhibition_fertility_ANd_Threshold_5_1(pack_id)

     if Nbr_female_analysis(pack_id)<10:
          return "NA"
     elif  Inhibition[0]>Inhibition[1] and Inhibition[0]>Inhibition[2]:
          return "inhibition fort"
     elif  Inhibition[0]>Inhibition[1] and Inhibition[0]<Inhibition[2]:
          return "inhibition modérée"
     elif Inhibition[0]<Inhibition[1]:
          return "conforme"
     else:
          return ""
def Endocrine_disruption(pack_id):

     female_concerned = nbr_female_concerned_area(pack_id)

     if Result_Fertility(pack_id) == "conforme" or Result_Fertility(pack_id) == "NA":
          return "NA"
     else:
          if Nbr_female_analysis(pack_id)<10:
               return 'NA'
          else:
               return female_concerned[1]/len(female_concerned)
   


     






          
          
          










  
    



     
     
     
     

    
