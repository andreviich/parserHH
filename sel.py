from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import requests
import pandas as pd
import openpyxl
res = pd.DataFrame()
chromedriver = 'chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless') 
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
browser.get('https://hh.ru/search/vacancy/advanced?no_default_area&L_is_autosearch=false&area=1&area=2019&area=1716&area=1754&area=1880&area=1890&area=1898&area=1905&area=1913&clusters=true&enable_snippets=true&no_magic=true&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+python')
button = browser.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div[1]/div/form/div[2]/div/div[2]/div/div[2]/button')
browser.execute_script("arguments[0].click();", button)
touches = browser.find_elements_by_class_name('bloko-icon-dynamic')
for t in touches:
    browser.execute_script("arguments[0].click();", t)
requiredHtml = browser.page_source
soup = BeautifulSoup(requiredHtml, 'html5lib')
threes = soup.find('div', {'class': "bloko-modal-container bloko-modal-container_visible"}).find_all('div', {'class' : 'Bloko-TreeSelector-Element'})
head = []
for i in threes:
    lst_items = i.find_all('div', {'class' : 'bloko-tree-selector-item'})
    header = i.find('div', {'class': 'Bloko-TreeSelector-SearchContent'})
    spec =  ' '.join(header.find('span', {'class': 'bloko-checkbox__text'}).text.split())+'-профобласть'
    ident = header.find('input', {'class': 'bloko-checkbox__input'})['value']
    res=res.append(pd.DataFrame([[spec, ident, 0]], columns = ['specialization', 'id', 'num']))
    for l in lst_items:
        check = l.find('label', {'class': 'bloko-checkbox'})
        iden = check.find('input')['value']
        text = ' '.join(check.find('span', {'class': 'bloko-checkbox__text'}).text.split())
        head.append({'id': iden, 'text': text})
        url = f'https://hh.ru/search/vacancy?st=searchVacancy&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+python&specialization={iden}&area=1&area=2019&area=1754&area=1890&area=1898&area=1905&area=1913&area=1716&area=1880&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&no_magic=true&L_save_area=true'
        r = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
        soup_l = BeautifulSoup(r.text, "html5lib")
        number_text = soup_l.find('h1', {'class': 'bloko-header-1'}).text.split()
        number = 0
        for n in number_text:
            try: 
                number = int(n)
            except:
                pass
        print(text, number)
        res=res.append(pd.DataFrame([[text, ident, number]], columns = ['specialization', 'id', 'num']))
res.to_excel('ouput.xlsx',  encoding='utf-8')
print(res)
