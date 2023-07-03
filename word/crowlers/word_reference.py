from bs4 import BeautifulSoup
import bs4
from playwright.sync_api import sync_playwright
from contextlib import contextmanager

from word.utils import text_normalization


@contextmanager
def setup_playwright(verb):
    try:
        with sync_playwright() as p:            
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"https://www.the-conjugation.com/english/verb/{verb}.php")
            yield page
            browser.close()
    except Exception as exp:
        print(f"setup_playwright__error: {exp}")


def get_conjugation(verb): 
    _list = {}
    try:
        with setup_playwright(verb) as page:         
            locator = page.locator(f'//html/body/div[2]/div[7]/div')
            soup = BeautifulSoup(locator.inner_html(), 'html.parser')
            
            html_base = soup.select("div")


            for elem in html_base:
                for item in elem.select('h3'):
                    tag = text_normalization(item.get_text())
                    _list[tag] = []

                for opt in elem.select('div'):
                    
                    words = []
                    
                    for _opt in opt.contents:
                        words.append(str(_opt).replace('<b>', '').replace('</b>', '').replace('/shall', ''))

                        conjugation = "".join([word for word in words]).split("<br/>")
                        _list[tag] = conjugation

            return _list
        
    except Exception as exp:
        print(f"get_conjugation__error: {exp}")
        return _list