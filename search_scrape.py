import requests
import csv
import time
import re
from bs4 import BeautifulSoup

num_pages = 500

#url = "https://old.reddit.com/r/wallstreetbets/search?q=flair%3Ayolo&restrict_sr=on&sort=new&t=all"
urls = ["https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3ADD", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3ADiscussion", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AGain", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3ALoss", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AShitpost", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AMeme", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AStorytime", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3ASatire", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AOptions", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AFutures", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AStocks", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AFundamentals", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3ATechnicals", 
"https://ns.reddit.com/r/wallstreetbets/search?sort=new&restrict_sr=on&q=flair%3AYOLO"]

def scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    counter = 1
    print(f'Scraping {num_pages} pages from: {url}')
    while (counter <= num_pages):
        posts = soup.find_all('div', class_='search-result')
        for post in posts:
            title = post.find('a', class_="search-title").text
            flair = post.find('span', class_='linkflairlabel')
            if not re.search('yolo', title, re.IGNORECASE) and not (flair and flair.text == 'YOLO'):
                continue

            likes = post.find('span', class_='search-score')
            if likes:
                likes = int(likes.text.split()[0].replace(',', ''))
            else:
                likes = 0

            comments = post.find('a', class_="search-comments")
            if comments:
                comments = int(comments.text.split()[0].replace(',', ''))
            else:
                comments = 0

            date = post.find('time')["datetime"].split('T')[0]
            
            post_line = [date, title, likes, comments]
            with open('yolo_search_output.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(post_line)
        next_button = soup.find('a', rel="next")
        if next_button:
            next_page_link = next_button.attrs['href']
        else:
            print("ran out of pages")
            break
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        counter += 1
    print("All done!")

for url in urls:
    scrape(url)