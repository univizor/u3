from bs4 import BeautifulSoup

def html2text(html):
    return BeautifulSoup(html).get_text('\n')