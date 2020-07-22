#!/usr/bin/env python3
import sys
import requests
import pandas as pd

from bs4 import BeautifulSoup as bs

# constants used by crawler
# target url as the start page
TGT_URL = 'https://maoyan.com/films?showType=3'
# request header, fake as Firefox browser, somehow chrome hit the slide bar
# authentication with high chance
HTTP_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',  # noqa: E501
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}  # noqa: E501
# number of films to be extracted
FILM_NUM = 10


def create_request_header():
    return HTTP_HEADER


def send_request():
    request_header = create_request_header()
    try:
        response = requests.get(TGT_URL, headers=request_header)
    except Exception as e:
        sys.exit(e)

    return response


def parse_response(response_txt):
    return bs(response_txt, 'html.parser')


def extract_films(response_txt):
    bs_info = parse_response(response_txt)
    bs_movies = bs_info.\
        find('dl', attrs={'class': 'movie-list'}).\
        find_all('div', attrs={'class': 'movie-hover-info'})

    movies_list = [['电影名称', '电影类型', '上映时间']]
    for m in bs_movies[:FILM_NUM]:
        # extract film name with bs
        film_name = m.find('span', attrs={'class': 'name'}).text.strip()
        # extract all the strings as some of them have no tags at all
        m_strings = [s.strip() for s in m.find_all(string=True)]
        type_index = m_strings.index('类型:') + 1
        time_index = m_strings.index('上映时间:') + 1

        # construct the film dict for pandas to convert
        movies_list.\
            append([film_name, m_strings[type_index], m_strings[time_index]])

    return movies_list


def save_to_csv(movie_list):
    movies = pd.DataFrame(data=movie_list)
    try:
        movies.to_csv('./movies.csv',
                      encoding='utf8', index=False, header=False)
    except Exception as e:
        sys.exit(e)


def fetch_films():
    # Send one time http request to maoyan for page retrival
    response = send_request()
    # Extract films from http response
    film_list = extract_films(response.text)
    # Save extracted films to csv file
    save_to_csv(film_list)


if __name__ == "__main__":
    fetch_films()
