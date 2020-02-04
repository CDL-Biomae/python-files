from tools import QueryScript, fusion_id_finder


def Nbr_Days_Exposition(pack_id):
     fusion_id = fusion_id_finder(pack_id)
     SQL_request = "SELECT date FROM datesclees where date_id IN(4,6) and measurepoint_fusion_id="+str(fusion_id)
     LR_dates =  QueryScript(SQL_request).execute()
     
     if(LR_dates!=""):
          return "NA"
     else:
          nbrdays =  LR_dates[0]-LR_dates[1]
          return nbrdays.days


def Nbr_Female_Concern(pack_id):


 
    
