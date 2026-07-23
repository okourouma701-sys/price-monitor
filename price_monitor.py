import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Connect to database
connection = sqlite3.connect('prices.db')
cursor = connection.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    price REAL,
    date TEXT
)
''')
connection.commit()

# Scrape the website
def scrape_prices():
    url = 'https://books.toscrape.com'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')
    today = datetime.now().strftime('%Y-%m-%d %H:%M')

    count = 0
    for book in books:
        title = book.find('h3').find('a')['title']
        price = float(book.find('p', class_='price_color').text.replace('£', ''))
        cursor.execute('INSERT INTO price_history (product, price, date) VALUES (?, ?, ?)', (title, price, today))
        count = count + 1

    connection.commit()
    print(f'Scraped and saved {count} products at {today}')

# Show insights
def show_insights():
    print('\n--- PRICE INSIGHTS ---')

    cursor.execute('SELECT COUNT(*) FROM price_history')
    total = cursor.fetchone()[0]
    print(f'Total records: {total}')

    cursor.execute('SELECT AVG(price) FROM price_history')
    avg = cursor.fetchone()[0]
    print(f'Average price: £{round(avg, 2)}')

    cursor.execute('SELECT product, price FROM price_history ORDER BY price ASC LIMIT 1')
    cheapest = cursor.fetchone()
    print(f'Cheapest: {cheapest[0]} at £{cheapest[1]}')

    cursor.execute('SELECT product, price FROM price_history ORDER BY price DESC LIMIT 1')
    expensive = cursor.fetchone()
    print(f'Most expensive: {expensive[0]} at £{expensive[1]}')

# Create a price chart
def make_chart():
    cursor.execute('SELECT product, price FROM price_history ORDER BY price DESC LIMIT 10')
    data = cursor.fetchall()

    products = [row[0][:25] for row in data]
    prices = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.barh(products, prices, color='teal')
    plt.xlabel('Price (£)')
    plt.title('Top 10 Most Expensive Products')
    plt.tight_layout()
    plt.savefig('price_report.png')
    print('Chart saved as price_report.png!')

# Run everything
scrape_prices()
show_insights()
make_chart()
connection.close()