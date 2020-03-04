def translate(element):
    if isinstance(element, str):
        element.replace("‰", "\\x89")
        return element.encode('iso-8859-1').decode('utf-8')
    else:
        return element
