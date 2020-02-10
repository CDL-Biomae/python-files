from openpyxl.styles import Font, Color, colors, PatternFill, Alignment
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd


def add_style_stations(stations_dataframe, filename):
    PATH = f"output\\{filename}"
    print(PATH)
    wb = load_workbook(PATH)
    ws = wb.get_sheet_by_name('Stations')

    nb_rows, nb_columns = stations_dataframe.shape

    ## HEADER STYLE ##
    header_row = '2'
    header_columns = [get_column_letter(col_idx) for col_idx in list(range(2, nb_columns + 2))]
    header_cells = [c+header_row for c in header_columns]
    header_font = Font(size=10, bold=True, name='Arial', color='FFFFFF')
    header_fill = PatternFill(fill_type='solid', start_color='808080', end_color='808080')
    header_alignment = Alignment(horizontal='center')

    for cell_str in header_cells:
        cell = ws[cell_str]
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    wb.save(PATH)
    wb.close()

    print('Style is done')

