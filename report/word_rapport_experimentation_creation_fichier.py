from report import recuperation_donnee


def create_doc(campaign):
    doc = Document('Page_de_garde.docx')
    style = doc.styles['Normal']
    font = style.font
    font.name = "Arial"
    dico_exposure_condition, dico_avg_tempe, dico_geo_mp, dico_geo_agency = recuperation_donnee(
        campaign)
    nb_measurepoint = len(dico_avg_tempe)
    for i in range(nb_measurepoint):
        doc.add_page_break()
        table_geo = doc.add_table(rows=8, cols=4)
        header = table_geo.rows[0]
        header.merge_cells()
        table_geo[0][0] = dico_geo_agency['i']['code'] + \
            " : " + dico_geo_agency['i']['name']
    doc.save(campaign + " Rapport d'expérimentation.docx")
