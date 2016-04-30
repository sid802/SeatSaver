__author__ = 'Sid'
#-*- encoding: utf-8 -*-

from lxml import html
from selenium import webdriver
from time import sleep
import constants

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

    selected_index = raw_input("Enter the number of wanted {0}: ".format(selection_category))
    while not selected_index.isdigit() or not 0 < int(selected_index) < len(options):
        selected_index = raw_input("Enter the number of wanted {cat} (between {min} and {max}): ".format(cat=selection_category,
                                                                                                       min=1,
                                                                                                       max=len(options) - 1))
    selected_index = int(selected_index)
    return options[selected_index].attrib['value']  # Return value of choosen option

def select_item(driver, item_options):
    """
    :param driver: WebDriver to navigate in
    :param item_options: Tuple of relevant xpath and descriptor
    :return: the item's code
    """

    xpath, descriptor = item_options
    html_tree = html.fromstring(driver.page_source)
    item_elements = html_tree.xpath(xpath)
    item = parse_option(item_elements, descriptor)

    # Set the item
    item_xpath = "{generic}[@value='{code}']".format(generic=xpath, code=item)
    driver.find_element_by_xpath(item_xpath).click()

    return item

def select_options(driver):
    """
    :param driver: WebDriver to navigate with
    :return: Instance of SeatOptions
    """

    # Sleep between each select so that it can load the following combobox
    cinema = select_item(driver, constants.MenuXpaths.cinemas)
    sleep(constants.SELECTION_WAIT)
    movie = select_item(driver, constants.MenuXpaths.movies)
    sleep(constants.SELECTION_WAIT)
    date = select_item(driver, constants.MenuXpaths.dates)
    sleep(constants.SELECTION_WAIT)
    time = select_item(driver, constants.MenuXpaths.times)

    return SeatOptions(cinema, movie, date, time)


def main():z
    """
    :return: Starts the whole program to save seats in cinema city
    """

    driver = webdriver.Chrome()
    driver.get(r'http://www.cinema-city.co.il')

    movie_info = select_options(driver)

if __name__ == '__main__':
    main()