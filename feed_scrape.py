import requests
import csv
import time
import re
from bs4 import BeautifulSoup
num_pages: 50
url = "https://old.reddit.com/r/wallstreetbets/"
headers = {'User-Agent': 'Mozilla/5.0'}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

counter = 1
print(f'Scraping {num_pages} pages from: {url}')
while (counter <= 100):
    posts = soup.find_all('div', class_='thing')
    for post in posts:
        title = post.find('a', class_="title").text
        flair = post.find('span', class_='linkflairlabel')

        if 'promoted' in post.attrs['class']:
            continue
        if not re.search('yolo', title, re.IGNORECASE) or not (flair and flair.text == 'YOLO'):
            continue

        likes = post.attrs['data-score']

        comments = post.find('a', class_="comments")
        if comments == "comment":
            comments = 0
        else:
            comments = comments.text.split()[0]

        date = post.find('time', class_="live-timestamp")["datetime"]
        
        post_line = [date, title, likes, comments]
        with open('yolo_feed_output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(post_line)

    next_button = soup.find('span', class_="next-button")
    if next_button:
        next_page_link = next_button.find('a').attrs['href']
    else:
        print("Ran out of pages")
        break
    time.sleep(2)
    page = requests.get(next_page_link, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    counter += 1
print("All done")
