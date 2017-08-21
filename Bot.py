"""
A Twitter robot which posts a quote of the day, a list of important events on this day, and a free ebook everyday.
@author: Virat Singh, svirat@gmail.com
"""
import tweepy
import Credentials
import Scraper
from time import sleep
from datetime import timedelta, date
from multiprocessing import Process
import random

# Gets the date three days ago
last_few_days = date.today() - timedelta(4)

def setup():
    """
    Sets up the Twitter bot with the correct credentials and returns an object to use the bot.
    :return: authentication to use the bot
    """
    # Set up OAuth and integrate with API
    auth = tweepy.OAuthHandler(Credentials.consumer_key, Credentials.consumer_secret)
    auth.set_access_token(Credentials.access_token, Credentials.access_token_secret)
    return tweepy.API(auth)

def tweet(post):
    """
    Simply updates bot's status to a specified post
    :param post: the new status of the bot
    """
    # Only post if it is a valid status
    if len(post) < 140 and post != "\n":
        # Catch any other unforseen errors
        try:
            bot.update_status(status=post)
        except tweepy.TweepError as e:
            print(e.reason)
    else:
        print("Too many characters in status, or blank status.")

def post_on_this_day():
    """
    Posts an event that occurred on this day, in equal time intervals of the day.
    """
    events = Scraper.get_on_this_day()
    # There will be 1 post per num hours
    for event in events:
        message = "Today: "
        message += event.get_text()
        tweet(message)
        # Sleep for num hours
        sleep(24/len(events) * 60 * 60)

def post_quote():
    """
    Posts a quote every day at a random time
    """
    # Sleep for a random amount of hours, between 1 and 23
    sleep(random.randint(1, 23) * 60 * 60)
    quote = Scraper.get_quote()
    message = "Quote of the day:\n"
    message += quote
    tweet(message)

def post_free_book():
    """
    Posts about a free eBook available at a random time
    """
    # Sleep for a random amount of hours, between 1 and 23
    sleep(random.randint(1, 23) * 60 * 60)
    book_info = Scraper.get_free_book()
    message = "Today's free eBook is:\n"
    message += book_info[0] + " " + book_info[1]
    message += "\nFor more eBooks, visit www.dailyfreebooks.com!"
    tweet(message)

def post_stocks():
    """
    Posts about today's stock information
    """
    num = 1
    stocks = Scraper.get_stocks()
    for stock in stocks:
        message = "Today's Stock Info #" + str(num) + ": \n"
        message += "Name: " + stock[0] + "\n"
        message += "Price: " + stock[1] + "\n"
        message += "Change: " + stock[2] + "\n"
        message += "%Change: " + stock[3]
        num += 1
        sleep(24/len(stocks) * 60 * 60)

def retweet(hashtag, since, until, max_items):
    """
    Retweets a tweet with any hashtag.
    :param hashtag: the hashtag to retweet. Currently set to "#Robot"
    :param since: the tweets since some previous day to retweet
    :param until: the tweets until some next day to retweet
    :param max_items: the max number of retweets a day
    """
    # Filter tweets to get only those with a minimum number of retweets
    tweets = filter(hashtag, since, until, max_items, 3, True)
    for tweet in tweets:
        try:
            if len(tweets) != 0 and len(tweets) != 1:
                num = 24 / len(tweets)
            else:
                num = 1
            tweet.retweet()
            sleep(num * 60 * 60)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def favorite(hashtag, since, until, max_items):
    """
    Favorites a tweet with any hashtag.
    :param hashtag: the hashtag to favorite. Currently set to "#Bird"
    :param since: the tweets since some previous day to favorite
    :param until: the tweets until some next day to favorite
    :param max_items: the max number of favorites a day
    """
    # Filter the tweets to get only those tweets with minimum number of favorites
    tweets = filter(hashtag, since, until, max_items, 3, False)
    for tweet in tweets:
        try:
            tweet.favorite()
            if len(tweets) != 0 and len(tweets) != 1:
                num = 24 / len(tweets)
            else:
                num = 1
            sleep(num * 60 * 60)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def filter(hashtag, since, until, max_items, min_num, retweet):
    """
    Helper function which removes tweet with less number of retweets/favorites.
    :param hashtag: the hashtag to search for
    :param since: the tweets since some previous day to favorite
    :param until: the tweets until some next day to favorite
    :param max_items: the max number of favorites a day
    :param min_num: the minimum number of retweets/favorites the tweet must have
    :param retweet: True if checking for num retweets, false for num favorites
    :return: top 3 items in list of tweets with sufficient retweets or favorites
    """
    tweets = []
    for tweet in tweepy.Cursor(bot.search, q=hashtag, since=since, until=until).items(max_items):
        if retweet:
            if tweet.retweet_count > min_num:
                tweets.append(tweet)
        else:
            if tweet.favorite_count > min_num:
                tweets.append(tweet)
    return tweets[:3]

# Build the bot
bot = setup()

if __name__ == "__main__":
    # Run bot operations in parallel
    # Setting up each operation process
    today_op = Process(target=post_on_this_day)
    quote_op = Process(target=post_quote)
    book_op = Process(target=post_free_book)
    stock_op = Process(target=post_stocks())
    retweet_op = Process(target=retweet,args=("#Robot", last_few_days, date.today(), 50))
    favorite_op = Process(target=favorite,args=("#Bird", last_few_days, date.today(), 50))
    # Starting each operation in parallel
    today_op.start()
    quote_op.start()
    book_op.start()
    stock_op.start()
    retweet_op.start()
    favorite_op.start()
    # Joining operations so all end at the same time
    today_op.join()
    quote_op.join()
    book_op.join()
    stock_op.join()
    retweet_op.join()
    favorite_op.join()
