from tools import QueryScript
from calcul import chemistry, survie_7jour, neurotoxicity,female_survivor,number_days_exposition,number_female_concerned

def measurepoint_result(measurepoint_id):
    packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id={measurepoint_id}").execute()
   # print(packs)
    for pack in packs :
    
        if(pack[0]=='alimentation'):
            print(pack[1])
            print("Survie Mal :"+ str(survie_7jour(pack[1])))
        if(pack[0]=='reproduction'):
            print(pack[1])
            print("Survie female :"+ str(female_survivor(pack[1])))
            print("number_days_exposition :"+ str(number_days_exposition(pack[1])))
            print("n L6 :"+ str(number_female_concerned(pack[1])))


              
          
