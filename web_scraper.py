import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = []
Details = []
count = 0
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
        Url = 'https://indiankanoon.org' + docs[i].get('href')
        response = requests.get(Url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('div', class_='judgments'):
            det['Judgment'] = f'{count+1}_Income_tax.pdf'
            det['Domain'] = 'Family Court'
            if link.find('h3', class_="doc_citations"):
                det['Equivalent Citation'] = link.find('h3', class_="doc_citations").get_text()
            else:
                det['Equivalent Citation'] = ''
            det['Name'] = link.find('h2', class_='doc_title').get_text()
            if link.find('h3', class_='doc_author'):
                det['Author'] = link.find('h3', class_='doc_author').get_text()
            else:
                det['Author'] = ''
            if link.find('h3', class_='doc_bench'):
                det['Bench'] = link.find('h3', class_='doc_bench').get_text()
            else:
                det['Bench'] = ''
            det['Court'] = link.find('h2', class_='docsource_main').get_text()
            det['link'] = Url
        data = {
            'type': 'pdf'
        }
        response = requests.post(Url, data=data)
        with open(f'C:/Users/awsom/Documents/GitHub/Volunteering_project/files/{count+1}_income_tax.pdf', 'wb') as f:
            f.write(response.content)
        Details.append(det)
        count += 1
print(len(Details))
# save the data in an excel file
df = pd.DataFrame(Details)
df.to_excel('income_tax.xlsx')