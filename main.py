__author__ = 'Sid'
#-*- encoding: utf-8 -*-

from lxml import html
from selenium import webdriver

class SeatOptions(object):
    """
    Class to easily save the seat's info
    """
    def __init__(self, cinema, movie, date, hour):
        self.cinema = cinema
        self.movie = movie
        self.date = date
        self.hour = hour

def parse_option(options, selection_category):
    """
    :param options: List of HTML elements of options to be selected
    :param selection_category: What is it we are choosing (cinema/movie etc...)
    :return: The value attrib of the choosen option
    """
    for index, option in enumerate(options):
        option_name = option.text  # What the user sees
        option_key = option.attrib['value']  # Make sure the value isn't zero because that's the default text
        if option_key == '0':
            continue
        print u"{0}: {1}".format(index, option_name)

    selected_index = raw_input("Enter the number of wanted {0}".format(selection_category))
    while not selected_index.isdigit() or not 0 < int(selected_index) < len(options):
        selected_index = raw_input("Enter the number of wanted {cat} (between {min} and {max}): ".format(cat=selection_category,
                                                                                                       min=1,
                                                                                                       max=len(options) - 1))
    return options[selected_index].attrib['value']  # Return value of choosen option

def select_cinema(html_tree):
    """
    :param html_tree: html (lxml) tree
    :return: The cinema's code
    """
    cinemas_xpath = '//select[@class="scheduleDropBox_subSite"]/option'
    cinemas_elements = html_tree.xpath(cinemas_xpath)
    cinema = parse_option(cinemas_elements, 'cinema')
    return cinema

def select_movie(html_tree):
    """
    :param html_tree: html (lxml) tree
    :return: The movie's code
    """
    movies_xpath = '//select[@class="scheduleDropBox_feature"]/option'
    movies_elements = html_tree.xpath(movies_xpath)
    movie = parse_option(movies_elements, 'movie')
    return movie

def select_date(html_tree):
    """
    :param html_tree: html (lxml) tree
    :return: The date's code
    """
    hours_xpath = '//select[@class="scheduleDropBox_date"]/option'
    hours_elements = html_tree.xpath(hours_xpath)
    hour = parse_option(hours_elements, 'hour')
    return hour

def select_time(html_tree):
    """
    :param html_tree: html (lxml) tree
    :return: The time's code
    """
    times_xpath = '//select[@class="scheduleDropBox_time"]/option'
    times_elements = html_tree.xpath(times_xpath)
    time = parse_option(times_elements, 'time')
    return time

def select_options(driver):
    """
    :param driver: WebDriver to navigate with
    :return: Instance of SeatOptions
    """

    tree = html.fromstring(driver.page_source)

    cinema = select_cinema(tree)
    movie = select_movie(tree)
    date = select_date(tree)
    time = select_time(tree)

    return SeatOptions(cinema, movie, date, time)


def main():
    """
    :return: Starts the whole program to save seats in cinema city
    """

    driver = webdriver.Chrome()
    driver.get(r'http://www.cinema-city.co.il')

    movie_info = select_options(driver)

if __name__ == '__main__':
    main()