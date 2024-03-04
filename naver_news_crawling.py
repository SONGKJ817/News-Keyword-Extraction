#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import time
import re

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tqdm import tqdm
import requests

import schedule


# 데이터 형태 생성 : 초기에만 1번 실행
# news_data = pd.DataFrame(columns = ["url", "title", "date", "content"])
# news_data.to_csv("./data/news_data.csv", index = False)
# pd.read_csv("./data/news_data.csv")


# 필요한 함수 정의
# Redirect되서 타URL로 이동하여 HTML구조가 변하는 URL 필터링
def filter_non_redirect_urls(url_list):
    non_redirect_url = []

    for url in tqdm(url_list):
        try:
            response = requests.get(url, allow_redirects=False)
            # 302가 아니라는 것은 리다이렉트 되지 않은 URL이라는 것
            if response.status_code != 302:
                non_redirect_url.append(url)
        except Exception:
            pass

    return non_redirect_url

# 기존 데이터에 새로운 데이터 추가하는 함수
def dataframe_concat(learn_news, news_data):
    learn_news['date'] = learn_news['date'].str.extract(r'(\d+\.\d+\.\d+\.)')
    learn_news["date"] = pd.to_datetime(learn_news["date"])
    learn_news = learn_news.sort_values("date", ascending = False).reset_index(drop = True)
    news_data.date = pd.to_datetime(news_data.date)
    news_data = pd.concat([learn_news, news_data], ignore_index=True)
    news_data = news_data.sort_values("date", ascending = False).reset_index(drop = True)
    news_data
    return news_data

def crawl_news():
    start_day = datetime.now() - timedelta(days=1) # 기간 설정
    end_day = datetime.now() - timedelta(days=1) # 기간 설정

    start_day = start_day.strftime("%Y%m%d")
    end_day = end_day.strftime("%Y%m%d")

    start_day = datetime.strptime(start_day, '%Y%m%d')
    end_day = datetime.strptime(end_day, '%Y%m%d')

    start_day = start_day.strftime('%Y.%m.%d')
    end_day = end_day.strftime('%Y.%m.%d')


    # 네이버 검색창에 "법" 키워드 검색
    search_content = "법"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}


    # URL 추출
    url_set = set()
    for page in tqdm(range(1, 2000, 10)): # 크롤링할 기사 개수
        response = requests.get(f"https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query={search_content}&start={page}&pd=3&ds={start_day}&de={end_day}", headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data for page {page}. Exiting.")
            break
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.select_one("div.group_news > ul.list_news")

        if ul is None:
            break
        li_list = ul.find_all('li')
        for li in li_list:
            a_list = li.select('div.news_area > div.news_info > div.info_group > a.info')
            for a_tag in a_list:
                href = a_tag.get('href')
                url_set.add(href)
        time.sleep(1)

    url = list(url_set)


    # NAVER 뉴스만 남기기
    naver_url = []

    for i in tqdm(range(len(url))):
        if "n.news.naver.com" in url[i]:
            naver_url.append(url[i])
        else:
            continue


    # Redirect되서 타URL로 이동하여 HTML구조가 변하는 URL 필터링
    news_url = filter_non_redirect_urls(naver_url)


    # 제목, 본문 추출
    news_title = []
    news_date = []
    news_content = []

    for url in tqdm(news_url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        news_title.append(title.text if title else 'None')

        date = soup.select_one('#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span')
        news_date.append(date.text if date else 'None')

        content = soup.select_one("article#dic_area")
        news_content.append(content.text if content else 'None')

    columns = ["url", "title", "date", "content"]


    # label 대분류명 지정해줘야함
    data = {
        "url": news_url,
        "title": news_title,
        "date": news_date,
        "content": news_content
    }

    learn_news = pd.DataFrame(data, columns=columns)
    learn_news = learn_news.drop_duplicates(subset=['content'], keep='first')
    learn_news['content'] = learn_news['content'].apply(lambda x: re.sub(r'\s+', ' ', x))

    news_data = pd.read_csv("./data/news_data.csv")


    # 두 데이터프레임 합치기
    news_data = dataframe_concat(learn_news, news_data)

    news_data.to_csv("./data/news_data.csv", index = False)



# 3/2까지 크롤링 완료
crawl_news()


# 자동화 : 크롤링을 매일 낮 12시에 실행하도록 예약
# schedule.every().day.at("12:00").do(crawl_news)

# while True:
#    schedule.run_pending()
#    time.sleep(1)

