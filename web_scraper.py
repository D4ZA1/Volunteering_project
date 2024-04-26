import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = []
Details = []
for i in range(10):
    urls.append(f'https://indiankanoon.org/search/?formInput=income%20tax%20judgements&pagenum={i}')
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    docs = []
    for link in soup.find_all('a'):
        if '/doc/' in link.get('href'):
            docs.append(link)

    for i in range(len(docs)):
        det = {}
        response = requests.get('https://indiankanoon.org' + docs[i].get('href'))
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('div', class_='judgments'):
            det['Judgment'] = f'{i}_family_court.pdf'
            det['Domain'] = 'Family Court'
            if link.find('h3', class_="doc_citations"):
                det['Equivalent Citation'] = link.find('h3', class_="doc_citations").get_text()
            else:
                det['Citation'] = ''
            det['Name'] = link.find('h2', class_='doc_title').get_text()
            det['Author'] = link.find('h3', class_='doc_author').get_text()
            det['Bench'] = link.find('h3', class_='doc_bench').get_text()
            det['Court'] = link.find('h2', class_='docsource_main').get_text()
            det['link'] = 'https://indiankanoon.org' + docs[i].get('href')
        Details.append(det)
print(len(Details))
# save the data in an excel file
# df = pd.DataFrame(Details)
# df.to_excel('Family_Court.xlsx')
