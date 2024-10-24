# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b1dVySO5qMzCIvZwnQ1OJ9KkiAuxdBIN
"""

# Install necessary libraries (uncomment the below lines if needed)
# !pip install requests
# !pip install beautifulsoup4
# !pip install pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the quotes website
base_url = "http://quotes.toscrape.com"
page_url = "/page/1/"
quotes_list = []

while page_url:
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all quotes on the page
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        # Extract quote text
        text = quote.find('span', class_='text').get_text()

        # Extract author name
        author = quote.find('small', class_='author').get_text()

        # Extract tags
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

        # Find author page link
        author_link = base_url + quote.find('a')['href']
        author_response = requests.get(author_link)
        author_soup = BeautifulSoup(author_response.text, 'html.parser')

        # Extract Born date and description
        born_date = author_soup.find('span', class_='author-born-date').get_text()
        born_location = author_soup.find('span', class_='author-born-location').get_text()
        description = author_soup.find('div', class_='author-description').get_text().strip()

        # Append the data to the list
        quotes_list.append({
            'Quote': text,
            'Author': author,
            'Tags': tags,
            'Born': f"{born_date} {born_location}",
            'Description': description
        })

    # Find the next page link
    next_page = soup.find('li', class_='next')
    page_url = next_page.find('a')['href'] if next_page else None

# Create a DataFrame and save as CSV
df = pd.DataFrame(quotes_list)
df.to_csv('quotes_toscrape.csv', index=False)

# Provide a download link for the CSV file in Google Colab
from google.colab import files
files.download('quotes_toscrape.csv')

print("Scraping completed. CSV file is ready for download.")

