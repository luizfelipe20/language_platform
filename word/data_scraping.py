# https://github.com/dunossauro/live-de-python/tree/main/codigo/Live222
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from contextlib import contextmanager


@contextmanager
def setup_playwright(instance):
    with sync_playwright() as p:            
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(30000)
        page.goto(f"https://translate.google.com/?hl=pt-BR&tab=TT&sl=en&tl=pt&text={instance.text}&op=translate")
        yield page
        browser.close()


def get_sentences(instance): 
    with setup_playwright(instance) as page:                    
        locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[2]/div[2]/div[1]')
        soup = BeautifulSoup(locator.inner_html(), 'html.parser')
        _list_sentences = []

        html = soup.select('div > div')
        for elem in html:
            if not elem.i:
                _list_sentences.append(elem.get_text())
        return _list_sentences
    

def get_translations(instance): 
    with setup_playwright(instance) as page:         
        locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[3]/div/div[1]/table')
        soup = BeautifulSoup(locator.inner_html(), 'html.parser')
        _list_translations = []

        html = soup.select('th > div')
        for elem in html:
            if elem.span:
                _list_translations.append(elem.get_text())
    
        return _list_translations


def get_tags(instance): 
    with setup_playwright(instance) as page:            
        locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[3]/div/div[1]/table')
        soup = BeautifulSoup(locator.inner_html(), 'html.parser')
        _list_tags = []

        html = soup.select('th > div > div')
        for elem in html:
            if not elem.span:
                _list_tags.append(elem.get_text())
        return _list_tags