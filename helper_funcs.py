__author__ = 'Sid'
# -*- encoding: utf-8 -*-

from lxml import html
from selenium import webdriver
from time import sleep
from helper_funcs import *
import constants
from datetime import datetime, timedelta
import re

class SeatOptions(object):
    """
    Class to easily save the seat's info
    """

    def __init__(self, cinema_code, cinema_value, movie_code, movie_value,
                 date_code, date_value, time_code, time_value):
        self.cinema_code = cinema_code
        self.cinema_value = cinema_value
        self.movie_code = movie_code
        self.movie_value = movie_value
        self.date_code = date_code
        self.date_value = date_value
        self.time_code = time_code
        self.time_value = time_value
        self.seat_ids = None  # Will be initialized later

    def set_options(self, driver):
        """
        :param driver: WebDriver open on home page where the options will be set
        The function fills the options in the home screen
        """

        # Setting cinema
        set_option(driver, constants.MenuXpaths.cinemas[0], self.cinema_code)
        sleep(constants.SELECTION_WAIT)

        # Setting movie
        set_option(driver, constants.MenuXpaths.movies[0], self.movie_code)
        sleep(constants.SELECTION_WAIT)

        # Setting date
        set_option(driver, constants.MenuXpaths.dates[0], self.date_code)
        sleep(constants.SELECTION_WAIT)

        # Setting time
        set_option(driver, constants.MenuXpaths.times[0], self.time_code)

        driver.find_element_by_xpath(constants.MenuXpaths.submit[0]).click()  # Submit

    def set_seats(self, driver):
        """
        :param driver: WebDriver open on home page where the options will be set
        The function fills the seats in
        """

        for seat_id in self.seat_ids:
            current_xpath = '//div[@id="{0}"]'.format(seat_id)
            driver.find_element_by_xpath(current_xpath).click()  # Finds element and selects it

    def get_seats(self, driver):
        """
        :param driver: WebDriver open on home page where the options will be set
        :return: Saves the choosen seats (and returns them)
        """

        tree = html.fromstring(driver.page_source)
        chosen_seats = tree.xpath(constants.MenuXpaths.taken_seats)  # Returns the id's of the chosen seats
        self.seat_ids = chosen_seats
        return chosen_seats


def retry(func):
    """
    :param func: Function to decorate
    Retries the function every X time until it doesn't return None
    """
    def func_wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        while value is None:
            'failed'
            sleep(constants.RETRY_TIME)
            value = func(*args, **kwargs)
        return value

    return func_wrapper

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
        selected_index = raw_input(
            "Enter the number of wanted {cat} (between {min} and {max}): ".format(cat=selection_category,
                                                                                  min=1,
                                                                                  max=len(options) - 1))
    selected_index = int(selected_index)
    return options[selected_index].attrib['value'], options[selected_index].text  # Return value of choosen option

@retry
def select_item(driver, item_options):
    """
    :param driver: WebDriver to navigate in
    :param item_options: Tuple of relevant xpath and descriptor
    :return: the item's code
    """

    xpath, descriptor = item_options
    html_tree = html.fromstring(driver.page_source)
    item_elements = html_tree.xpath(xpath)
    if len(item_elements) < 2:
        return None  # No options are available yet
    item_code, item_value = parse_option(item_elements, descriptor)

    set_option(driver, xpath, item_code)

    return item_code, item_value


def select_options(driver):
    """
    :param driver: WebDriver to navigate with
    :return: Instance of SeatOptions
    """

    # Sleep between each select so that it can load the following combobox
    cinema_code, cinema_value = select_item(driver, constants.MenuXpaths.cinemas)
    sleep(constants.SELECTION_WAIT)
    movie_code, movie_value = select_item(driver, constants.MenuXpaths.movies)
    sleep(constants.SELECTION_WAIT)
    date_code, date_value = select_item(driver, constants.MenuXpaths.dates)
    sleep(constants.SELECTION_WAIT)
    time_code, time_value = select_item(driver, constants.MenuXpaths.times)

    return SeatOptions(cinema_code, cinema_value, movie_code, movie_value, date_code, date_value, time_code, time_value)


def get_seat_release_time():
    """
    :return: howmuch time to release the seats before the movie starts
    """

    release_time = raw_input(
        "----------\nEnter amount of time (in minutes) you want to release the seats before the movie starts: ")
    while not release_time.isdigit():
        release_time = raw_input(
            "Enter amount of time (in minutes) you want to release the seats before the movie starts: ")
    return int(release_time)


def get_people_amount():
    """
    :return: howmany people to keep seats for
    """

    people = raw_input("----------\nEnter amount of people to save seats for (between 1 and 9): ")
    while not people.isdigit() and not 0 < int(people) < 10:
        people = raw_input("Enter amount of people to save seats for (between 1 and 9): ")
    return int(people)

def combine_to_datetime(date, time):
    """
    :param date: Date + dayname in hebrew
    :param time: Time
    :return: datetime
    """
    date_string = re.sub( r'[^\d/]', '', date)
    string_datetime = "{0} {1}".format(date_string, time)
    return datetime.strptime(string_datetime, '%d/%m/%Y %H:%M')