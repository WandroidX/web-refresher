import  sys, os
from src import file_handler
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import time


def main():
 
    if len(sys.argv) == 2:
        file_path: str = sys.argv[1]
        if os.path.exists(file_path):
            dirname: str = os.path.dirname(file_path)

            file_url: str = sys.argv[1].replace('\\', '/')

            browser = webdriver.Firefox(executable_path=r'C:\users\crist\downloads\creative_projects\Python\geckodriver\geckodriver.exe')
            browser.get('file:///'+ file_url.replace(' ', '%20'))
            html_text1: str = file_handler.read_file(file_path)

            links_href1: list[str]
            scripts_src1: list[str]
            links_href1, scripts_src1 = file_handler.parse_href_and_src(html_text1)

            css_text1: list[str]= [
                file_handler.read_file(fr'{dirname}\{link}') 
                for link in links_href1
            ]
            js_text1: list[str]= [
                file_handler.read_file(fr'{dirname}\{link}') 
                for link in scripts_src1
            ]


            while True: 
                try:
                    browser.current_window_handle
                except NoSuchWindowException:
                    exit()

                        

                    # tiempo necesario para notar cambios en los archivos en caso de que se den
                time.sleep(0.5)

                html_text2: str = file_handler.read_file(file_path)

                if html_text2:
                    text: str | None
                    if html_text1 != html_text2:
                        html_text1 = html_text2
                        browser.refresh()
                        continue

                    links_href2: list[str]
                    scripts_src2: list[str]
                    links_href2, scripts_src2 = file_handler.parse_href_and_src(html_text2)

                    css_text2: list[str] = [file_handler.read_file(fr'{dirname}\{link}') for link in links_href2]
                    js_text2: list[str] = [file_handler.read_file(fr'{dirname}\{link}') for link in scripts_src2]

                    # verify if there is any change in the html file
                    for text in css_text2:
                        if text and text not in css_text1:
                            browser.refresh()
                            css_text1 = css_text2
                    else:
                        for text in js_text2:
                            if text and text not in js_text1:
                                browser.refresh()
                                js_text1 = js_text2
                                break
        else:
            raise Exception('that file doesnt exist')
    elif len(sys.argv) < 2:
        raise Exception('need an argument: FILE_PATH')
    elif len(sys.argv) > 2:
        raise Exception('too many arguments')

if __name__ == "__main__":
    main()
