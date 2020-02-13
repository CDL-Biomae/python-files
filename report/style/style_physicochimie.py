from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
from termcolor import colored

def add_style_physicochimie(physicochimie_dataframe, filename):
    PATH = f"output\\{filename}"
    wb = load_workbook(PATH)
    ws = wb['Physico-chimie']

    nb_rows, nb_columns = physicochimie_dataframe.shape

    thin = Side(border_style='thin', color='FF000000')
    medium = Side(border_style='medium', color='FF000000')
    double = Side(border_style='double', color='FF000000')
    no_border = Side(border_style=None)

    font_Arial9 = Font(size=9, name='Arial')
    alignment_center = Alignment(horizontal='center', vertical='center')

    ## REFORMATAGE STATIONS HEADER ##
    merging_cells = ['B2:B3', 'C2:C3', 'D2:D3', 'E2:E3']
    border_cells = ['B2', 'B3', 'C2', 'C3', 'D2', 'D3', 'E2', 'E3']
    merging_names = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']

    header_stations_border = Border(left=medium, right=medium, top=medium, bottom=medium)
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

    # Nettoyage entre Stations et Values
    cell = ws['F3']
    cell.border = Border(top=no_border, bottom=no_border)

    ## REFORMATAGE VALUE HEADER ##
    # Reformatage temperature
    temperature_cells = 'G2:I2'
    ws.merge_cells(temperature_cells)

    temp_names = ['Température (°C)', 'minimum', 'moyenne', 'maximum']
    temp_cells = ['G2', 'G3', 'H3', 'I3']
    for i in range(len(temp_cells)):
        cell = ws[temp_cells[i]]
        name = temp_names[i]

        cell.value = name
        cell.font = font_Arial9
        cell.alignment = alignment_center

    temp_border_cells = ['G2', 'H2', 'I2', 'G3', 'H3', 'I3']
    for cell in temp_border_cells:
        if cell[-1] == '2':
            ws[cell].border = Border(top=medium, left=medium, right=medium, bottom=medium)
        else:
            ws[cell].border = Border(top=medium, left=medium, right=medium, bottom=double)

    # Reformatage header Conductivité, pH, oxygène
    nb_jours = (nb_columns - 8) // 3
    cond_cells = [f"{get_column_letter(x+10)}2" for x in range(nb_jours)]
    ph_cells = [f"{get_column_letter(x+10)}2" for x in range(nb_jours, nb_jours*2)]
    oxygene_cells = [f"{get_column_letter(x+10)}2" for x in range(nb_jours*2, nb_jours*3)]
    border_cells = cond_cells + ph_cells + oxygene_cells

    ws.merge_cells(f"{cond_cells[0]}:{cond_cells[-1]}")
    ws.merge_cells(f"{ph_cells[0]}:{ph_cells[-1]}")
    ws.merge_cells(f"{oxygene_cells[0]}:{oxygene_cells[-1]}")

    top_left_cells = [ws[cond_cells[0]], ws[ph_cells[0]], ws[oxygene_cells[0]]]
    names = ['Conductivité (µS/cm)', 'pH (unité pH)', 'Oxygène (mg/L)']

    for i in range(len(top_left_cells)):
        cell = top_left_cells[i]
        name = names[i]

        cell.value = name
        cell.font = font_Arial9
        cell.alignment = alignment_center

    for cell_str in border_cells:
        cell = ws[cell_str]
        cell.border = Border(top=medium, left=medium, right=medium, bottom=medium)

    # Reformatage J#
    J_cells = [f"{get_column_letter(x+10)}3" for x in range(3*nb_jours)]

    for cell_str in J_cells:
        cell = ws[cell_str]
        name = cell.value.split()[-1]

        cell.value = name
        cell.font = font_Arial9
        cell.alignment = alignment_center
        cell.border = Border(top=medium, left=medium, right=medium, bottom=double)


    ## BODY STYLE ##
    # Body Stations
    body_rows = [str(r) for r in range(4, nb_rows + 4)]
    body_stations_columns = ['B', 'C', 'D', 'E']
    body_stations_cells = []
    for row in body_rows:
        for column in body_stations_columns:
            body_stations_cells.append(column+row)

    # Body Values
    body_values_columns = [get_column_letter(x+7) for x in range(3 + 3*nb_jours)]  # 3 temperatures puis 3*nb_jours pour conductivité, ph et oxygene
    body_values_cells = []
    for row in body_rows:
        for column in body_values_columns:
            body_values_cells.append(column+row)

    body_cells = body_stations_cells + body_values_cells

    for cell_str in body_cells:
        cell = ws[cell_str]

        if cell_str[0] == 'H':
            cell.font = Font(size=9, name='Arial', italic=True)
        else:
            cell.font = font_Arial9
        cell.alignment = alignment_center
        cell.border = Border(top=medium, left=medium, right=medium, bottom=medium)


    wb.save(PATH)
    wb.close()

    print(colored('[+] La mise en page de l\'onglet \"Physico-chimie\" est terminée', 'green'))