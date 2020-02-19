from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from calcul import chemistry, elements_crustacean, elements_fish
from termcolor import colored


def add_style_tox(tox_dataframe, filename):
    PATH = f"output\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['Tox']
    

    nb_rows, nb_columns = tox_dataframe.shape
    header_row = '4'
    header_columns = [get_column_letter(col_idx) for col_idx in list(range(2, nb_columns + 2))]
    borders = Border(left=Side(border_style='thin', color='FFFFFF'),
                     right=Side(border_style='thin', color='FFFFFF'),
                     top=Side(border_style='thin', color='FFFFFF'),
                     bottom=Side(border_style='thin', color='FFFFFF'))
    
    for letter in [get_column_letter(col_idx) for col_idx in range(1, nb_columns+5)]:
        for number in range(1, nb_rows+7):
            ws[letter+str(number)].border = borders
  

   ## HEADER STYLE ##
 ## HEADER STYLE ##
    
    ws['B4'].value = 'Campagne'
    ws['C4'].value = 'némuro'
    ws['D4'].value = 'Station de mesure'
    ws['E4'].value = 'Code agence'
    
    
  
    header_font = Font(size=10, bold=True, name='Arial')
    
    
    ws.column_dimensions['B'].width=20
    ws.column_dimensions['C'].width=20
    ws.column_dimensions['D'].width=20
    ws.column_dimensions['E'].width=20
   
    for letter in header_columns[:4]:
        for number in range(2,5):
            ws[letter+str(number)].border = borders
            ws[letter+str(number)].font = header_font
   
    
    
    
    
    header_font = Font(size=10, name='Arial')
    
    for letter in header_columns[4:]:
        if (ws[letter+'5'].value !=None and ws[letter+'5'].value !='') :
            
            ws.column_dimensions[letter].width=20
         
        else :
            ws.column_dimensions[letter].width=20
    wb.save(PATH)
    wb.close()