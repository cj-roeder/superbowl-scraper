#!/usr/bin/env python3

import concurrent.futures
import html
import re
import time
import requests

HEADERS = {'User-Agent': 'superbowl-scraper/1.0'}
SITE  = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'

def scrape(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()#checking if the requsts worked
        match = re.search(r'>MVP<.*?<td[^>]*>(.*?)</td>', response.text, re.DOTALL)
        if not match:
            return ''
        text = re.sub(r'<[^>]+>', '', match.group(1))      #remove tags
        text = re.sub(r'\[\d+\]', '', text)                 
        return ' '.join(html.unescape(text).split())
    except requests.RequestException as error:
        print(error)
        return ''

def main():
    index = requests.get(SITE, headers=HEADERS, timeout=10).text
    names = dict.fromkeys(re.findall(r'href="(?:https://en\.wikipedia\.org)?(?:\./|/wiki/)(Super_Bowl_[IVXLC]+)"', index))
    urls  = list(map(lambda name: 'https://en.wikipedia.org/wiki/' + name, names))
    urls = urls[:10]

    for workers in [1, 8,14]:
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:#concurrent futures 8 workers at a time vs. 1
            mvps = list(executor.map(scrape, urls))
        elapsed = time.perf_counter() - start
        print(f'{workers} worker(s): {elapsed:.3f} seconds')

    for url, mvp in zip(urls, mvps):#need to pair mvp with url
        if mvp:
            print(f"{url.split('_')[-1]:>7}: {mvp}")

if __name__ == '__main__':
    main()
