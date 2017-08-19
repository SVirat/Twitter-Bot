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