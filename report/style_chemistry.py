from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd


def add_style_nqe(campagnes_dataframe, filename):
    PATH = f"output\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['NQE']
    ## a optimiser
    ws.column_dimensions['D'].width=35
    ws.column_dimensions['G'].width=5
    ws.column_dimensions['H'].width=5
    ws.column_dimensions['I'].width=5
    ws.column_dimensions['J'].width=5
    ws.column_dimensions['K'].width=5
    ws.column_dimensions['L'].width=5
    ws.column_dimensions['M'].width=5
    ws.column_dimensions['N'].width=5
    ws.column_dimensions['O'].width=5
    ws.column_dimensions['P'].width=5
    ws.column_dimensions['P'].width=5
    ws.column_dimensions['Q'].width=5
    ws.column_dimensions['R'].width=5
    ws.column_dimensions['S'].width=5
    ws.column_dimensions['T'].width=5
    ws.column_dimensions['U'].width=5
    ws.column_dimensions['V'].width=5
    ws.column_dimensions['W'].width=5
    ws.column_dimensions['X'].width=5
    ws.column_dimensions['Y'].width=5
    ws.column_dimensions['Z'].width=5
    
    

    nb_rows, nb_columns = campagnes_dataframe.shape

    borders = Border(left=Side(border_style='thin', color='FF000000'),
                     right=Side(border_style='thin', color='FF000000'),
                     top=Side(border_style='thin', color='FF000000'),
                     bottom=Side(border_style='thin', color='FF000000'))

    ## HEADER STYLE ##
    header_row = '2'
    header_columns = [get_column_letter(col_idx) for col_idx in list(range(2, nb_columns + 2))]
    header_cells = [c+header_row for c in header_columns]

    header_font = Font(size=10, bold=True, name='Arial', color='FFFFFF')
    header_fill = PatternFill(fill_type='solid', start_color='808080', end_color='808080')
    header_alignment = Alignment(horizontal='center', vertical='center')
    
    for cell_str in header_cells[:4]:
        cell = ws[cell_str]
        cell.font = header_font
        cell.fill = header_fill
        cell.border = borders
        
    header_font = Font(size=10, name='Arial')
    header_fill = PatternFill(fill_type='solid', start_color='FFFFFF', end_color='FFFFFF')
    header_alignment = Alignment(horizontal='left',vertical='center',text_rotation=90)
    header_alignment_measure = Alignment(horizontal='center',vertical='bottom')
    
        
    for cell_str in header_cells[5:]: 
        cell = ws[cell_str]
        if cell.value!=None:
            cell.font = header_font
            cell.fill = header_fill
            cell.border = borders

    for cell_str in header_cells:
        cell = ws[cell_str]
        if cell.value!='Station de mesure':
            cell.alignment = header_alignment
        else :
            cell.alignment = header_alignment_measure


    ## BODY STYLE ##
    body_rows = [str(r) for r in list(range(3, nb_rows+3))]
    body_columns = header_columns
    body_cells = []
    for row in body_rows:
        for column in body_columns:
            body_cells.append(column+row)

    body_font_header = Font(size=9, name='Arial')
    body_font = Font(size=6, name='Arial')
    body_fill_ND = PatternFill(fill_type='solid', start_color='606060', end_color='606060')
    body_fill_not_ND = PatternFill(fill_type='solid', start_color='318CE7', end_color='318CE7')
    body_alignment = Alignment(horizontal='center', vertical='center')

    for cell_str in body_cells:
        cell = ws[cell_str]
        value = cell.value
        if value!=None:
            cell.alignment = body_alignment
            cell.border = borders
            if value=="ND":
                cell.font = body_font
                cell.fill = body_fill_ND
            elif cell.column>"F":
                cell.font = body_font
                cell.fill = body_fill_not_ND

    wb.save(PATH)
    wb.close()

    print('[+] La mise en page de l\'onglet \"NQE\" est terminée')

