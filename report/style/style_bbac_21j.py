from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from calcul import chemistry
from tools import QueryScript
from termcolor import colored


def add_style_bbac_21j(bbac_dataframe, filename, folder_PATH):
    PATH = f"{folder_PATH}\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['BBAC_21j']
    ws2 = wb['BBAC2_21j']
    
    nb_rows, nb_columns = bbac_dataframe.shape
    header_row = '4'
    header_columns = [get_column_letter(col_idx) for col_idx in list(range(2, nb_columns + 2))]
    borders = Border(left=Side(border_style='thin', color='FFFFFF'),
                     right=Side(border_style='thin', color='FFFFFF'),
                     top=Side(border_style='thin', color='FFFFFF'),
                     bottom=Side(border_style='thin', color='FFFFFF'))
    elements_metal = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly='Métaux' AND 21j_threshold IS NOT NULL").execute()
    elements_organic = QueryScript("SELECT sandre, parameter, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM r3 WHERE familly!='Métaux' AND 21j_threshold IS NOT NULL").execute()
    
    for letter in [get_column_letter(col_idx) for col_idx in range(1, nb_columns+5)]:
        for number in range(1, nb_rows+21):
            ws[letter+str(number)].border = borders
            ws2[letter+str(number)].border = borders
    
    ## UNIT 
    [unit_metal, sandre_metal] = chemistry.get_unit([int(float(element[0])) for element in elements_metal])
    threshold_metal = [element[2:] for element in elements_metal]
    [unit_organic, sandre_organic] = chemistry.get_unit([int(float(element[0])) for element in elements_organic])
    threshold_organic = [element[2:] for element in elements_organic]
    index = 0
    sandre_checked = sandre_metal
    unit_checked = unit_metal
    
    for letter in header_columns[5:]:
        
        if index<len(sandre_checked):
            ws[letter + '2'].value = unit_checked[index]
            ws2[letter + '2'].value = unit_checked[index]
            ws[letter + '3'].value = sandre_checked[index]
            ws2[letter + '3'].value = sandre_checked[index]
            index+=1
        else :
            index=0
            sandre_checked = sandre_organic
            unit_checked = unit_organic
    ## Merge unit
    
    current_unit = ws['G2'].value 
    first_letter = 'G'           
    last_letter = 'G'           
    index = 6
    while index <len(header_columns): 
        while index <len(header_columns) and ws[header_columns[index] + '2'].value == current_unit :   
            last_letter = header_columns[index]
            index +=1
        ws.merge_cells(first_letter + '2:'+last_letter+'2')
        ws2.merge_cells(first_letter + '2:'+last_letter+'2')
        if index<len(header_columns):
            first_letter = last_letter = header_columns[index]
        current_unit = ws[first_letter +'2'].value
        index+=1
    
            
    
    ## HEADER STYLE ##
    
    ws['B2'].value = 'Campagne'
    ws2['B2'].value = 'Campagne'
    ws['C2'].value = '#'
    ws2['C2'].value = '#'
    ws['D2'].value = 'Station de mesure'
    ws2['D2'].value = 'Station de mesure'
    ws['E2'].value = 'Code agence'
    ws2['E2'].value = 'Code agence'
    
    ws.merge_cells('B2:B4')
    ws2.merge_cells('B2:B4')
    ws.merge_cells('C2:C4')
    ws2.merge_cells('C2:C4')
    ws.merge_cells('D2:D4')
    ws2.merge_cells('D2:D4')
    ws.merge_cells('E2:E4')
    ws2.merge_cells('E2:E4')
    
    header_cells = [c+header_row for c in header_columns]
    header_font = Font(size=8, bold=True, name='Arial')
    header_alignment_rotate = Alignment(horizontal='center', vertical='bottom', text_rotation=90)
    header_alignment_no_rotate = Alignment(horizontal='center', vertical='bottom')
    borders = Border(left=Side(border_style='thin', color='FF000000'),
                     right=Side(border_style='thin', color='FF000000'),
                     top=Side(border_style='thin', color='FF000000'),
                     bottom=Side(border_style='thin', color='FF000000'))
    
    ws.column_dimensions['B'].width=3
    ws2.column_dimensions['B'].width=3
    ws.column_dimensions['C'].width=3
    ws2.column_dimensions['C'].width=3
    ws.column_dimensions['D'].width=30
    ws2.column_dimensions['D'].width=30
    ws.column_dimensions['E'].width=8
    ws2.column_dimensions['E'].width=8
    for letter in header_columns[:4]:
        for number in range(2,5):
            ws[letter+str(number)].border = borders
            ws2[letter+str(number)].border = borders
            ws[letter+str(number)].font = header_font
            ws2[letter+str(number)].font = header_font
    ws['B2'].alignment = header_alignment_rotate
    ws['C2'].alignment = header_alignment_no_rotate
    ws['D2'].alignment = header_alignment_no_rotate
    ws['E2'].alignment = header_alignment_rotate
    ws2['B2'].alignment = header_alignment_rotate
    ws2['C2'].alignment = header_alignment_no_rotate
    ws2['D2'].alignment = header_alignment_no_rotate
    ws2['E2'].alignment = header_alignment_rotate
    
    
    
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
            ws2.column_dimensions[letter].width=4
            ws2[letter+'4'].alignment = header_alignment_rotate
            ws2[letter+'4'].font = header_font
            ws2[letter+'3'].alignment = header_alignment_no_rotate
            ws2[letter+'3'].font = header_font
            ws2[letter+'2'].alignment = header_alignment_no_rotate
            ws2[letter+'2'].font = header_font
        else :
            ws.column_dimensions[letter].width=2
            ws2.column_dimensions[letter].width=2
            


    ## BODY STYLE ##
    body_rows = [str(r) for r in list(range(5, nb_rows+5))]
    body_columns = header_columns[5:]

    body_font = Font(size=6, name='Arial')
    body_font_white = Font(size=6, name='Arial', color='FFFFFF')
    body_fill_ok = PatternFill(fill_type='solid', start_color='DBB7FF', end_color='DBB7FF')
    body_fill_nd = PatternFill(fill_type='solid', start_color='A6A6A6', end_color='A6A6A6')
    body_fill_not_ok = PatternFill(fill_type='solid', start_color='B565F7', end_color='B565F7')
    body_fill_not_ok_25 = PatternFill(fill_type='solid', start_color='8909FF', end_color='8909FF')
    body_fill_not_ok_50 = PatternFill(fill_type='solid', start_color='6600CC', end_color='6600CC')
    body_fill_not_ok_75 = PatternFill(fill_type='solid', start_color='47008E', end_color='47008E')
    body_alignment = Alignment(horizontal='center', vertical='center')

    for column in header_columns:
        for row in body_rows:
            if column in ['B','C','D','E']:
                ws[column+row].border = borders
                ws[column+row].font = body_font
                ws2[column+row].border = borders
                ws2[column+row].font = body_font


    for column in body_columns:
        sandre_checked = ws[column+'3'].value
        threshold_21j=''
        if sandre_checked!='' and sandre_checked!=None:
            try :
                index = sandre_metal.index(sandre_checked)
                threshold_21j = threshold_metal[index][0]
                threshold_21j_25 = threshold_metal[index][1]
                threshold_21j_50 = threshold_metal[index][2]
                threshold_21j_75 = threshold_metal[index][3]
            except :
                index = sandre_organic.index(sandre_checked)
                threshold_21j = threshold_organic[index][0]
                threshold_21j_25 = threshold_organic[index][1]
                threshold_21j_50 = threshold_organic[index][2]
                threshold_21j_75 = threshold_organic[index][3]
        for row in body_rows:
            cell = ws[column+row]
            cell2 = ws2[column+row]
            value = cell.value
            cell.font = body_font
            cell2.font = body_font
            if value!=None :
                cell.alignment = body_alignment
                cell.border = borders
                cell2.alignment = body_alignment
                cell2.border = borders
                if (value!="ND" and value!='0.0' and threshold_21j!='') and ((value!='' and value[0]=='<') or float(value)<threshold_21j):
                    cell.fill = body_fill_ok
                    cell2.fill = body_fill_ok
                    cell2.value = 0
                elif (value!="ND" and value!='0.0' and threshold_21j!='' and float(value)>=threshold_21j):
                    if threshold_21j_25==None:
                        cell.fill = body_fill_not_ok_75
                        cell.font = body_font_white
                        cell2.fill = body_fill_not_ok_75
                        cell2.value = 4
                        cell2.font = body_font_white
                    elif float(value)>=threshold_21j_25 :
                        if float(value)>=threshold_21j_50:
                            if float(value)>=threshold_21j_75:
                                cell.fill = body_fill_not_ok_75
                                cell.font = body_font_white
                                cell2.value = 4
                                cell2.fill = body_fill_not_ok_75
                                cell2.font = body_font_white
                            else :    
                                cell.fill = body_fill_not_ok_50 
                                cell.font = body_font_white
                                cell2.fill = body_fill_not_ok_50 
                                cell2.value = 3
                                cell2.font = body_font_white
                        else:
                            cell.fill = body_fill_not_ok_25 
                            cell2.fill = body_fill_not_ok_25 
                            cell2.value = 2
                    else :
                        cell.fill = body_fill_not_ok
                        cell2.fill = body_fill_not_ok
                        cell2.value = 1
                else :
                    cell.fill = body_fill_nd
                    cell2.fill = body_fill_nd
                    cell2.value = 'nd'
    wb.save(PATH)
    wb.close()

    print(colored('[+] La mise en page des onglets \"BBAC_21j\" et \"BBAC2_21j\" est terminée','green'))

