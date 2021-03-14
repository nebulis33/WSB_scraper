import requests
import csv
import time
import re
from bs4 import BeautifulSoup

url = "https://old.reddit.com/r/wallstreetbets/search?q=yolo&restrict_sr=on&sort=relevance&t=all"
headers = {'User-Agent': 'Mozilla/5.0'}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')
# posts = soup.find_all('div', class_='thing')

counter = 1
while (counter <= 500):
    posts = soup.find_all('div', class_='search-result')
    for post in posts:
        title = post.find('a', class_="search-title").text
        flair = post.find('span', class_='linkflairlabel')
        # if not (flair and flair.text == 'YOLO'):
        #     continue
        likes = post.find('span', class_='search-score').text
        if likes == "•":
            likes = 0
        else:
            likes = int(likes.split()[0].replace(',', ''))
        comments = post.find('a', class_="search-comments")
        if comments == "comment":
            comments = 0
        else:
            comments = int(comments.text.split()[0].replace(',', ''))
        # likes = post.find('div', attrs={"class": "score likes"})['title']
        date = post.find('time')["datetime"]
        
        post_line = [date, title, likes, comments]
        with open('yolo_search_output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(post_line)
    counter += 1
    next_button = soup.find('a', rel="next")
    if next_button:
        next_page_link = next_button.attrs['href']
    else:
        break
    time.sleep(2)
    page = requests.get(next_page_link, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')