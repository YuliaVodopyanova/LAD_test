import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


urls = [
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=1&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=2&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=3&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=4&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=5&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=6&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=7&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=8&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=9&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=1&q=Data%20Science&type=all',
    'https://career.habr.com/vacancies?locations[]=c_715&locations[]=c_678&page=2&q=Data%20Science&type=all'
]

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}

vacancies = {}
res = {}
senior = []
middle = []
junior = []
no_info = []

for url in urls:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        vacancy = soup.find_all('div', {'class': 'vacancy-card__inner'})
        for i in vacancy:
            name = i.find('div', class_="vacancy-card__title").text
            additional_info = i.find('div', class_="vacancy-card__skills").text
            vacancies[name] = additional_info

    for name, info in vacancies.items():
        if 'senior' in info.lower():
            senior.append(name)
        if 'middle' in info.lower():
            middle.append(name)
        if 'junior' in info.lower():
            junior.append(name)
        if name not in senior and name not in middle and name not in junior:
            no_info.append(name)
        res['Senior positions'] = {'Vacancies': senior, 'Total count': len(senior)}
        res['Middle positions'] = {'Vacancies': middle, 'Total count': len(middle)}
        res['Junior positions'] = {'Vacancies': junior, 'Total count': len(junior)}
        res['Not specified level'] = {'Vacancies': no_info, 'Total count': len(no_info)}


df = pd.DataFrame(res)
print('Data science vacancies across NN and Moscow:\n\n')
print(df)

df2 = df.drop('Vacancies')
print('Table only with number of vacancies of different levels:\n\n')
print(df2)

df.T.plot(kind='bar')
plt.xlabel('Level')
plt.ylabel('Number of vacancies')
plt.title('Vacancies for different levels')
plt.xticks(rotation=45)
plt.show()
