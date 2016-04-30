__author__ = 'Sid'
#-*- encoding: utf-8 -*-

from lxml import html
from selenium import webdriver
from time import sleep
import constants
from datetime import datetime

class SeatOptions(object):
    """
    Class to easily save the seat's info
    """
    def __init__(self, cinema, movie, date, time):
        self.cinema = cinema
        self.movie = movie
        self.date = date
        self.time = time

    def set(self, driver):
        """
        :param driver: WebDriver open on home page where the options will be set
        """

        # Setting cinema
        driver.find_element_by_xpath(constants.MenuXpaths.cinemas[0]).click()
        sleep(constants.SELECTION_WAIT)

        # Setting movie
        driver.find_element_by_xpath(constants.MenuXpaths.movies[0]).click()
        sleep(constants.SELECTION_WAIT)

        # Setting date
        driver.find_element_by_xpath(constants.MenuXpaths.dates[0]).click()
        sleep(constants.SELECTION_WAIT)

        # Setting time
        driver.find_element_by_xpath(constants.MenuXpaths.times[0]).click()

        driver.find_element_by_xpath(constants.MenuXpaths.submit[0]).click()  # Submit

def set_option(driver, generic_xpath, item_code):
    """
    :param driver: WebDriver open on home page where the options will be se
    :param generic_xpath: xpath to all the possible options
    :param item_code: the way to pick the correct option
    """

    # Set the item
    item_xpath = "{generic}[@value='{code}']".format(generic=generic_xpath, code=item_code)
    driver.find_element_by_xpath(item_xpath).click()

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

    set_option(driver, xpath, item)

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

def get_seat_release_time():
    """
    :return: howmuch time to release the seats before the movie starts
    """

    release_time = raw_input("----------\nEnter amount of time (in minutes) you want to release the seats before the movie starts: ")
    while not release_time.isdigit():
        release_time = raw_input("Enter amount of time (in minutes) you want to release the seats before the movie starts: ")
    return int (release_time)

def get_people_amount():
    """
    :return: howmany people to keep seats for
    """

    people = raw_input("----------\nEnter amount of people to save seats for: ")
    while not release_time.isdigit():
        people = raw_input("Enter amount of people to save seats for: ")
    return int (release_time)

def main():
    """
    :return: Starts the whole program to save seats in cinema city
    """

    driver = webdriver.Chrome()
    driver.get(r'http://www.cinema-city.co.il')

    movie_info = select_options(driver)
    release_time = get_seat_release_time()
    people_amount = get_people_amount()
    
    string_datetime = "{0} {1}".format(movie_info.date, movie_info.time)
    movie_datetime = datetime.strptime(string_datetime, '%d/%m/&Y &H:%M')

    # Rechoose seats until we passed the release time
    while datetime.now() < movie_datetime - release_time:
        movie_info.set(driver)



    return movie_info

if __name__ == '__main__':
    main()