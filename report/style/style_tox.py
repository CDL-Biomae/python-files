from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from calcul import chemistry, elements_crustacean, elements_fish
from termcolor import colored
from tools import QueryScript
import env

def add_style_tox(tox_dataframe, filename, folder_PATH):
    PATH = f"{folder_PATH}\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['Tox']

    nb_rows, nb_columns = tox_dataframe.shape

    thin = Side(border_style='thin', color='FF000000')
    medium = Side(border_style='medium', color='FF000000')
    double = Side(border_style='double', color='FF000000')
    no_border = Side(border_style=None)

    font_Arial9 = Font(size=9, name='Arial')
    font_title = Font(name='Arial',size=10,bold=True,color='FF000000')
    font_small_title = Font(name='Arial',size=8,bold=False ,color='FF000000')
    alignment_center = Alignment(horizontal='center', vertical='center')

    ## COLUMN WIDTH ##
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 45
    ws.column_dimensions['E'].width = 14

   

    ## REFORMATAGE STATIONS HEADER ##
    merging_cells = ['B3:B4', 'C3:C4', 'D3:D4', 'E3:E4']
    border_cells = ['B3', 'B4', 'C3', 'C4', 'D3', 'D4', 'E3', 'E4', 'G3','H3','I3','J3','K3','L3','M3','N3','O3','P3','Q3','R3']
    little_border_columns = ['B','C','D','E','G','H','I','K','L','M','N','O','P', 'Q', 'R']
    titres_columns = ['G','H','I','K','L','M','N','O','P', 'Q', 'R']
    na = ['L','M','N','O','P', 'Q', 'R']
    subtitle = ['M','O','Q']
    n_merge = ['M3:M4','O3:O4','Q3:Q4']
    merging_names = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']

    header_stations_border = Border(left=medium, right=medium, top=medium, bottom=medium)
    normal_cells_border    = Border(left=thin,   right=thin, top=thin, bottom=thin)
    header_stations_font = Font(size=10, bold=True, name='Arial', color='FFFFFF')
    header_stations_fill = PatternFill(fill_type='solid', start_color='808080', end_color='808080')
    header_stations_alignment = Alignment(horizontal='center', vertical='center')
 


    for i in range(len(merging_cells)):
        cells = merging_cells[i]
        top_left_cell = ws[cells[:2]]
        name = merging_names[i]
       
        ws.merge_cells(cells)
        top_left_cell.value = name
        top_left_cell.font = header_stations_font
        top_left_cell.fill = header_stations_fill
        top_left_cell.alignment = header_stations_alignment

    for cell in border_cells:
        ws[cell].border = header_stations_border

    for column in little_border_columns:
        for row in range(3, 5+nb_rows):
            ws[column + str(row)].border = normal_cells_border
            ws[column + str(row)].alignment = alignment_center

    ws.row_dimensions[3].height = 45

    

    cell = ws['F4']
    cell.border = Border(top=no_border, bottom=no_border)

    #  ## REFORMATAGE VALUE HEADER ##

    columns = [get_column_letter(col_idx) for col_idx in range(6, nb_columns+2)]
   
    body_fill_ok = PatternFill(fill_type='solid', start_color='1F75FE', end_color='1F75FE')
    body_fill_not_ok_1 = PatternFill(fill_type='solid', start_color='008000', end_color='008000')
    body_fill_not_ok_2 = PatternFill(fill_type='solid', start_color='FFFF00', end_color='FFFF00')
    body_fill_not_ok_3 = PatternFill(fill_type='solid', start_color='FF7F00', end_color='FF7F00')
    body_fill_not_ok_4 = PatternFill(fill_type='solid', start_color='DE1738', end_color='DE1738')
    body_fill_NA = PatternFill(fill_type='solid', start_color='eff0f1', end_color='bdbdbd')

    ws.column_dimensions['F'].width = 3
    ws.column_dimensions['J'].width = 3
    threshold_list = QueryScript(f" SELECT parameter, threshold   FROM {env.DATABASE_TREATED}.r2_threshold WHERE threshold IS NOT NULL").execute()
    for column in columns:
        if ws[column + '5'].value==None or ws[column + '5'].value=='':
            ws.column_dimensions[column].width = 3
        else :
            threshold =None
            if column=='H':
                threshold = []
                for element in threshold_list:
                    if element[0]=='alimentation':
                        threshold.append(element[1])
            if column=='I':
                threshold = []
                for element in threshold_list:
                    if element[0]=='neurotoxicité AChE':
                        threshold.append(element[1])
            if column=='N':
                threshold = []
                for element in threshold_list:
                    if element[0]=='reproduction':
                        threshold.append(element[1])
            if column=='P':
                threshold = []
                for element in threshold_list:
                    if element[0]=='mue':
                        threshold.append(element[1])
            if column=='R':
                threshold = []
                for element in threshold_list:
                    if element[0]=='perturbation endocrinienne':
                        threshold.append(element[1])

            if threshold :
                for row in range(5,nb_rows+5):
                    cell = ws[column+str(row)]
                    if cell.value != "NA" :
                         value = -float(cell.value) if cell.value  else None
                    if value and value >= threshold[0]:
                        if len(threshold)>=1 and value >= threshold[1]:
                            if len(threshold)>=2 and value >= threshold[2]:
                                if len(threshold)>=3 and value>= threshold[3]:
                                    cell.fill = body_fill_not_ok_4  
                                else:
                                    cell.fill = body_fill_not_ok_3  
                            else:
                                cell.fill = body_fill_not_ok_2
                        else :
                            cell.fill = body_fill_not_ok_1
                    else :
                        cell.fill = body_fill_ok


            cell = ws[column + '4']
            ws[column+'3'].value = cell.value
            ws.column_dimensions[column].width = 20
            if column=='G' or column=='H' or column=='I' or column=='K':
                cell.value = '%'

    for column in titres_columns:
        if column in ["L","P","R"]:
            ws.column_dimensions[column].width = 35
            ws[column + "3"].font = font_title
        else:
            ws.column_dimensions[column].width = 20
            ws[column + "3"].font = font_title


    for column in subtitle:
          ws[column + "5"].font = font_small_title
    
    for column in n_merge:
        ws.merge_cells(column)


    for row in range(5,nb_rows+5):
        if float(ws["K" + str(row)].value) == 0:        
             for column in na:
                ws[column + str(row)].value="NA"
                if column == "N" or column == "P" or column == "R":
                     ws[column + str(row)].fill = body_fill_NA

    ws['N4'].value = "indice"
    ws['p4'].value = "valeur observée (valeur attendue)"
    ws['R4'].value = "surface ovocytaire moyenne (µm²)"
                    
    
    wb.save(PATH)
    wb.close()
    print(colored('[+] La mise en page de l\'onglet \"Tox\" est terminée', 'green'))