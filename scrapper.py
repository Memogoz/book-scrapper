import requests
from bs4 import BeautifulSoup


def scrape_books(queue,chosenCategoty):
    #https://books.toscrape.com/index.html

    r = requests.get('https://books.toscrape.com/catalogue/category/books/'+chosenCategoty+'/index.html')
    print(r) #HTTP status code
    
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('section')

    book_list = []

    if s is not None:
        titles = s.find_all('h3')
        book_list.append(len(titles))

        prices = s.find_all('p', class_='price_color')
        stocks = s.find_all('p', class_='availability')

        for book in range(len(titles)):
            book_list.append('<h2>' + titles[book].get_text(strip=True) + '</h2>' +
                             '<b>' + prices[book].get_text(strip=True) + '</b>' +
                             '<p style="color:green">' + stocks[book].get_text(strip=True) + '</p><p></p>')
            
        book_list.append(None)

    else:
        print("No se encontró el contenido deseado.")

    for book in book_list:
        queue.put(book)
