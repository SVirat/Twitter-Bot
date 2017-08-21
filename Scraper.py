"""
Goes to different websites and collects a list of certain things, for example the
quote of the day, events which occured on this day, free eBooks available, so on.
@author: Virat Singh, svirat@gmail.com
"""
import requests
from bs4 import BeautifulSoup

def get_on_this_day():
    """
    Go to www.onthisday.com to get significant events that occurred on this day.
    :return: the list of important events on this day
    """
    url = "http://www.onthisday.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    events = soup.find_all('li', class_= "event-list__item")
    return events

def get_quote():
    """
    Go to www.brainyquote.com to get the quote of the day, as a twitter description tag.
    :return: the quote of the day
    """
    url = "https://www.brainyquote.com/quotes_of_the_day.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    quote = soup.find(attrs={"name":"twitter:description"})
    return quote['content']

def get_free_book():
    """
    Go to www.dailyfreebooks.com to get the first free eBook mentioned on the site.
    :return: a list, with the book title as first element and author as second element
    """
    url = "http://www.dailyfreebooks.com/free_ebooks/c/?&catID=154821011"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    book = soup.find("p", class_="name")
    author = soup.find("p", class_="author")
    return [book.get_text(), author.get_text()]

def get_stocks():
    """
    Checks 9 stocks and gives their name, price, change and %change.
    :return: list of 9 stocks, with their information
    """
    url = "http://www.money.cnn.com/data/us_markets/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    stocks = soup.find_all('td', class_="wsod_aRight")
    stocks = chunks(stocks, 3)
    returning_stocks = []
    for stock in stocks:
        for item in stock:
            name = str(item.span)
            name = (name.split("streamfeed=")[-1].split(">")[0]).strip("\"")
            if name not in returning_stocks:
                returning_stocks.append(name)
            returning_stocks.append(item.text)
    returning_stocks = list(chunks(returning_stocks, 4))
    return returning_stocks[:9]

def chunks(list, num):
    """
    Helper function that splits a list into num-evenly sized chunks
    :param list: the list to split
    :param num: the number of sublists to make
    :return: a list of the sublists
    """
    for i in range(0, len(list), num):
        yield list[i:i + num]
