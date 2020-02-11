from report import recuperation_donnee


def create_doc(campaign):
    doc = Document('Page_de_garde.docx')
    style = doc.styles['Normal']
    font = style.font
    font.name = "Arial"
    dico_exposure_condition, dico_avg_tempe, dico_geo_mp, dico_geo_agency = recuperation_donnee(
        campaign)
    nb_measurepoint = len(dico_avg_tempe)
    for i in range(1, nb_measurepoint+1):
        doc.add_page_break()
        table_geo = doc.add_table(rows=8, cols=4)

        for j in range(2, 8):
            table_geo.cell(j, 0).merge(table_geo.cell(j, 1))
        for j in range(2, 5):
            table_geo.cell(j, 2).merge(table_geo.cell(j, 3))

        header = table_geo.rows[0].cells
        header[0].merge(header[-1])
        case_header = table_geo.cell(0, 0).paragraphs[0].add_run(dico_geo_agency[i]['code'] +
                                                                 " : " + dico_geo_agency[i]['name'])
        case_header.bold = True
        case_header = table_geo.cell(0, 0).paragraphs[0].alignment = 1

        table_geo.cell(1, 0).paragraphs[0].add_run('Commune :').bold = True
        table_geo.cell(1, 1).paragraphs[0].add_run(
            dico_geo_agency[i]['city'] + "    " + dico_geo_agency[i]['zipcode'])
        table_geo.cell(1, 2).paragraphs[0].add_run(
            "Cours d'eau : ").bold = True
        table_geo.cell(1, 3).paragraphs[0].add_run(
            dico_geo_agency[i]['stream'])

        table_geo.cell(2, 0).paragraphs[0].add_run("Biotests")
        table_geo.cell(2, 0).paragraphs[0].alignment = 1
        table_geo.cell(2, 2).paragraphs[0].add_run(
            "Alimentation, Neurotoxicité, Reproduction ? Trouver data")
        table_geo.cell(2, 2).paragraphs[0].alignment = 1

        table_geo.cell(3, 0).paragraphs[0].add_run("Réseau de surveillance :")
        table_geo.cell(3, 2).paragraphs[0].add_run(
            dico_geo_agency[i]['network'])

        table_geo.cell(4, 0).paragraphs[0].add_run("Type d'hydroécorégion :")
        table_geo.cell(4, 2).paragraphs[0].add_run(
            dico_geo_agency[i]['hydroecoregion'])

        table_geo.cell(5, 0).paragraphs[0].add_run(
            "Coordonnées Agence Lambert 93 :")
        table_geo.cell(5, 2).paragraphs[0].add_run('Y ' +
                                                   dico_geo_agency[i]['lambertY'])
        table_geo.cell(5, 3).paragraphs[0].add_run('X ' +
                                                   dico_geo_agency[i]['lambertX'])

        table_geo.cell(6, 0).paragraphs[0].add_run(
            "Coordonnées BIOMÆ en degrés décimaux : ")
        table_geo.cell(6, 2).paragraphs[0].add_run(
            str(dico_geo_mp[i]['longitudeSpotted']))
        table_geo.cell(6, 3).paragraphs[0].add_run(
            str(dico_geo_mp[i]['latitudeSpotted']))

        table_geo.cell(7, 0).paragraphs[0].add_run(
            "Coordonnées BIOMÆ Lambert 93 : ")
        table_geo.cell(7, 2).paragraphs[0].add_run('Y ' +
                                                   dico_geo_mp[i]['lambertYSpotted'])
        table_geo.cell(7, 3).paragraphs[0].add_run('X ' +
                                                   dico_geo_mp[i]['lambertXSpotted'])

        doc.add_page_break()

    doc.save(campaign + "_Rapport d'expérimentation.docx")
