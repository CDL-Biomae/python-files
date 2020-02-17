from tools import QueryScript
from calcul import chemistry, survie_7jour,alimentation, neurotoxicity,female_survivor,number_days_exposition,number_female_concerned,index_fertility_average,number_female_analysis,number_female_concerned_area,endocrine_disruption,molting_cycle

def measurepoint_result(measurepoint_id):
    packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id={measurepoint_id}").execute()
   
    for pack in packs :
        print(pack[1])
        
        if(pack[0]=='alimentation'):
            print("survie_7jour :" +str(survie_7jour(pack[1]))+" alimentation :" +str(alimentation(pack[1])) )
        if(pack[0]=='neurology'):
            print("neurotoxicity :" +str(neurotoxicity(pack[1])))

        if(pack[0]=='reproduction'):
            print(" female_survivor :" +str(female_survivor(pack[1]))+
                  " nombre jour d'exepostion :" + str(number_days_exposition(pack[1]))+
                  " n :" + str(number_female_concerned(pack[1]))+
                  " fécondité :" + str(index_fertility_average(pack[1]))+
                  " n :" + str(number_female_analysis(pack[1]))+
                  " cycle de mue :" + str(molting_cycle(pack[1]))+
                  " n :" + str(number_female_concerned_area(pack[1])[0])+
                  " perturbation endocrinienne :" + str(endocrine_disruption(pack[1]))
             )
            #print("Survie female :"+ str(female_survivor(pack[1])) + "number_days_exposition :  "+ str(number_days_exposition(pack[1]))+"n L6 : "+str(number_female_concerned(pack[1])) +"index_fertility_average : "+str(index_fertility_average(pack[1])))
          


              
          
