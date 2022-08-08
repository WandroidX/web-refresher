import re
from typing import Pattern
# ??? esta función es para abrir el archivo pasado como parámetro y retornar el texto de este

def read_file(filepath: str) -> str:
    '''return the text of an specified file'''
    while True:
        try:
            with open(filepath, encoding='utf-8') as file:
                return file.read()
        except PermissionError:
            continue
        except OSError:
            break
    return ''


def parse_href_and_src(html_text: str ) -> tuple[list[str], list[str]]:
    '''parse the src of script tags and the href of links'''

    re_link: Pattern = re.compile(r'(<link.*? href\s?=\s?(\'.*?\.css.*?\'|".*?\.css.*?").*?>)')
    re_script: Pattern = re.compile(r'(<script.*? src\s?=\s?(\'.*?\.js.*?\'|".*?\.js.*?").*?>)')

    findall_re_link: list[str] = [
        match[1].replace("'", '') if "'" in match[1] 
        else match[1].replace('"', '') 
        for match in re_link.findall(html_text)]
    
    findall_re_link = list(map(lambda string: string.strip(), findall_re_link))

    findall_re_script: list[str] = [
        match[1].replace("'", '') if "'" in match[1]
        else match[1].replace('"', '') 
        for match in re_script.findall(html_text)]

    findall_re_script = list(map(lambda string: string.strip(), findall_re_script))


    return (findall_re_link, findall_re_script)

