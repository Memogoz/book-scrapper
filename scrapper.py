import requests
from bs4 import BeautifulSoup
import random


def scrape_books(queue):
    #https://books.toscrape.com/index.html

    booksCategorys = ['travel_2','mystery_3','historical-fiction_4','sequential-art_5']

    chosenCategoty = booksCategorys[random.randint(0, 4)]

    r = requests.get('https://books.toscrape.com/catalogue/category/books/'+chosenCategoty+'/index.html')
    print(r) #HTTP status code
    
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('section')

    book_list = []

    if s is not None:
        content = s.find_all('h3')
        book_list.append(len(content))
        for paragraph in content:
            book_list.append('<h2>' + paragraph.get_text(strip=True) + '</h2></br>')  # strip=True elimina espacios en blanco extra
    else:
        print("No se encontró el contenido deseado.")

    for book in book_list:
        queue.put(book)





'''
    example_scrape = [4,'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue mattis lorem, sed tincidunt nunc pharetra et.', 'Curabitur non laoreet ante. Integer at tempus magna. Nunc vel fringilla nisi. Sed ut lacinia velit.', 'Sed massa tortor, condimentum in tempus sit amet, elementum sit amet dolor.', 'Nullam ac purus egestas, gravida quam vel, fermentum velit.', None]

    for product in example_scrape:
        queue.put(product)
'''

def test_srapping():
    r = requests.get('https://webscraper.io/test-sites/e-commerce/static/computers/laptops/')
    print(r) #HTTP status code

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup.prettify())

    print(soup.title)

    s = soup.find('div', class_='container test-site')
    #print(s)

    lista = []

    if s is not None:
        content = s.find_all('h4')
        for paragraph in content:
            lista.append(paragraph.get_text(strip=True))  # strip=True elimina espacios en blanco extra
    else:
        print("No se encontró el contenido deseado.")

    print(lista)
