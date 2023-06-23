from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from contextlib import contextmanager


@contextmanager
def setup_playwright(instance):
    with sync_playwright() as p:            
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(9000)
        page.goto(f"https://translate.google.com/?hl=pt-BR&tab=TT&sl=en&tl=pt&text={instance.text}&op=translate")
        yield page
        browser.close()


def get_sentences(instance): 
    _list_sentences = []
    try:
        with setup_playwright(instance) as page:                    
            locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[2]/div[2]/div[1]')
            soup = BeautifulSoup(locator.inner_html(), 'html.parser')
            html = soup.select('div > div')

            for elem in html:
                if not elem.i:
                    _list_sentences.append(elem.get_text())
        
            return _list_sentences
        
    except Exception as exp:
        print(f"get_sentences__error: {exp}")
        return _list_sentences
    

def get_translations(instance): 
    _list = {}
    try:
        with setup_playwright(instance) as page:         
            locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[3]/div/div[1]/table')
            soup = BeautifulSoup(locator.inner_html(), 'html.parser')
            html_base = soup.select('tr')

            for elem in html_base:
                for item in elem.select('th > div'):
                    raw_text = item.get_text().lower()
                    _list[raw_text] = []
                    
                for item in elem.select('td ul li'):
                    _list[raw_text].append(item.get_text().replace(",", "").lower().strip())
        
            return _list
        
    except Exception as exp:
        print(f"get_translations__error: {exp}")
        return _list
    

def get_tags(instance): 
    _list_tags = []
    try:
        with setup_playwright(instance) as page:            
            locator = page.locator(f'//html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[2]/c-wiz/div/div/div[3]/div/div[1]/table')
            soup = BeautifulSoup(locator.inner_html(), 'html.parser')
            html = soup.select('th > div > div')

            for elem in html:
                if not elem.span:
                    _list_tags.append(elem.get_text())
            
            return _list_tags
        
    except Exception as exp:
        print(f"get_tags__error: {exp}")
        return _list_tags