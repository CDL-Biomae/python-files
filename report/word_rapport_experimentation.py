from docx import Document


def create_doc(campain):
    doc = Document('Page_de_garde.docx')
    style = doc.styles['Normal']
    font = style.font
    font.name = "Arial"
    return []


def recuperation_donnee(campain):
    return []
