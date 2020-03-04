def translate(element):
    if isinstance(element, str):
        return element.encode('windows-1252').decode('utf-8')
    else:
        return element
