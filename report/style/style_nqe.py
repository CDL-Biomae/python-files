from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from calcul import chemistry, elements_crustacean, elements_fish
from termcolor import colored



def add_style_nqe(nqe_dataframe, filename, folder_PATH):
    PATH = f"{folder_PATH}\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['NQE Biote']
    
    nb_rows, nb_columns = nqe_dataframe.shape
    header_row = '4'
    header_columns = [get_column_letter(col_idx) for col_idx in list(range(2, nb_columns + 2))]
    borders = Border(left=Side(border_style='thin', color='FFFFFF'),
                     right=Side(border_style='thin', color='FFFFFF'),
                     top=Side(border_style='thin', color='FFFFFF'),
                     bottom=Side(border_style='thin', color='FFFFFF'))
    
    for letter in [get_column_letter(col_idx) for col_idx in range(1, nb_columns+5)]:
        for number in range(1, nb_rows+7):
            ws[letter+str(number)].border = borders
    
    ## UNIT 
    [unit_crustacean, sandre_crustacean, NQE_crustacean] = chemistry.get_unit_NQE(elements_crustacean.keys()) 
    [unit_fish, sandre_fish, NQE_fish] = chemistry.get_unit_NQE(elements_fish.keys()) 
    index = 0
    sandre_checked = sandre_crustacean
    unit_checked = unit_crustacean
    
    for letter in header_columns[5:]:
        
        if index<len(sandre_checked):
            ws[letter + '2'].value = unit_checked[index]
            ws[letter + '3'].value = sandre_checked[index]
            index+=1
        else :
            index=0
            sandre_checked = sandre_fish
            unit_checked = unit_fish

    ## Merge unit
    
    current_unit = ws['G2'].value 
    first_letter = 'G'           
    last_letter = 'G'           
    index = 6
    while index <len(header_columns): 
        while ws[header_columns[index] + '2'].value == current_unit and index <len(header_columns):   
            last_letter = header_columns[index]
            index +=1
        ws.merge_cells(first_letter + '2:'+last_letter+'2')
        first_letter = last_letter = header_columns[index]
        current_unit = ws[first_letter +'2'].value
        index+=1
    
            
    
    ## HEADER STYLE ##
    
    ws['B2'].value = 'Campagne'
    ws['C2'].value = '#'
    ws['D2'].value = 'Station de mesure'
    ws['E2'].value = 'Code agence'
    
    
    header_cells = [c+header_row for c in header_columns]
    header_font = Font(size=8, bold=True, name='Arial')
    header_alignment_rotate = Alignment(horizontal='center', vertical='bottom', text_rotation=90)
    header_alignment_no_rotate = Alignment(horizontal='center', vertical='bottom')
    borders = Border(left=Side(border_style='thin', color='FF000000'),
                     right=Side(border_style='thin', color='FF000000'),
                     top=Side(border_style='thin', color='FF000000'),
                     bottom=Side(border_style='thin', color='FF000000'))
    
    ws.column_dimensions['B'].width=3
    ws.column_dimensions['C'].width=3
    ws.column_dimensions['D'].width=30
    ws.column_dimensions['E'].width=8
    for letter in header_columns[:4]:
        for number in range(2,5):
            ws[letter+str(number)].border = borders
            ws[letter+str(number)].font = header_font
    ws['B2'].alignment = header_alignment_rotate
    ws['C2'].alignment = header_alignment_no_rotate
    ws['D2'].alignment = header_alignment_no_rotate
    ws['E2'].alignment = header_alignment_rotate
    
    ws.merge_cells('B2:B4')
    ws.merge_cells('C2:C4')
    ws.merge_cells('D2:D4')
    ws.merge_cells('E2:E4')
    
    
    header_font = Font(size=8, name='Arial')
    
    for letter in header_columns[4:]:
        if (ws[letter+'5'].value !=None and ws[letter+'5'].value !='') :
            
            ws.column_dimensions[letter].width=6
            ws[letter+'4'].alignment = header_alignment_rotate
            ws[letter+'4'].font = header_font
            ws[letter+'3'].alignment = header_alignment_no_rotate
            ws[letter+'3'].font = header_font
            ws[letter+'2'].alignment = header_alignment_no_rotate
            ws[letter+'2'].font = header_font
        else :
            ws.column_dimensions[letter].width=2
            


    ## BODY STYLE ##
    body_rows = [str(r) for r in list(range(5, nb_rows+5))]
    body_columns = header_columns[5:]

    body_font = Font(size=6, name='Arial')
    body_fill_ok = PatternFill(fill_type='solid', start_color='318CE7', end_color='318CE7')
    body_fill_not_ok = PatternFill(fill_type='solid', start_color='BB0B0B', end_color='BB0B0B')
    body_alignment = Alignment(horizontal='center', vertical='center')

    for column in header_columns:
        for row in body_rows:
            if column in ['B','C','D','E']:
                ws[column+row].border = borders
                ws[column+row].font = body_font


    for column in body_columns:
        sandre_checked = ws[column+'3'].value
        if sandre_checked!='' and sandre_checked!=None:
            try :
                index = sandre_crustacean.index(sandre_checked)
                threshold = NQE_crustacean[index]
            except :
                index = sandre_fish.index(sandre_checked)
                threshold = NQE_fish[index]
        for row in body_rows:
            cell = ws[column+row]
            value = cell.value
            cell.font = body_font
            if value!=None :
                cell.alignment = body_alignment
                cell.border = borders
                if (value!="ND" and value!='0.0' and threshold!='') and ((value!='' and value[0]=='<') or float(value)<threshold):
                    if threshold=='':
                        print('oui')
                    cell.fill = body_fill_ok
                elif (value!="ND" and value!='0.0' and threshold!='' and float(value)>=threshold):
                    cell.fill = body_fill_not_ok
    wb.save(PATH)
    wb.close()

    print(colored('[+] La mise en page de l\'onglet \"NQE\" est terminée','green'))

