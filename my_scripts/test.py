import requests
from bs4 import BeautifulSoup

'''Получение HTML-кода страницы'''
# url = "https://povar.ru"
url = "https://povar.ru/list/goryachie_bliuda/" # find_parent() -  Получить родительский элемент
response = requests.get(url)
html_content = response.text
# print(html_content)

'''Создание объекта Beautiful Soup'''
soup = BeautifulSoup(html_content, 'html.parser')

'''find() - Этот метод используется для поиска первого элемента, соответствующего заданным критериям.'''
# first_paragraph = soup.find('p') # Питательную и сытную закуску из лаваша с колбасой и сыром...
# print(first_paragraph.text)

'''find_all() -  Этот метод возвращает все элементы, соответствующие критериям, в виде списка.'''
# all_paragraphs = soup.find_all('p')
# for paragraph in all_paragraphs:
#     print(paragraph.text)

''' Находим элементы с классом 'fmHead' (список всех категорий); 'fmItem' (список всех подкатегорий)'''
# elements = soup.find_all(class_='fmHead') # список всех категорий
# for element in elements:
#     print(element.text)
#
# elements = soup.find_all(class_='fmItem') # список всех подкатегорий
# for element in elements:
#     print(element.text)

'''Чтобы извлечь все ссылки (теги `<a>`) с веб-страницы, можно использовать:'''
# links = soup.find_all('a')
# for link in links:
#     print(link.get('href'))

# '''Beautiful Soup поддерживает навигацию между элементами структуры документа.
# find_parent() -  Получите родительский элемент:'''
# parent = first_paragraph.find_parent()
# print(parent)