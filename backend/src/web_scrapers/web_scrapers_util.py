import html


def remove_html_entities(string):
    string = html.unescape(string)
    string = string.replace(" ", " ")

    return string
