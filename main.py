__author__ = 'Sid'
# -*- encoding: utf-8 -*-

from lxml import html
from selenium import webdriver
from time import sleep
from helper_funcs import *
import constants
from datetime import datetime, timedelta
import re


def main():
    """
    :return: Starts the whole program to save seats in cinema city
    """

    driver = webdriver.Chrome()
    driver.get(r'http://www.cinema-city.co.il')

    movie_info = select_options(driver)
    release_time = get_seat_release_time()
    people_amount = get_people_amount()

    movie_datetime = combine_to_datetime(movie_info.date_value, movie_info.time_value)
    first_iter = True

    # Rechoose seats until we passed the release time
    while datetime.now() < movie_datetime - timedelta(minutes=release_time):
        movie_info.set(driver)
        sleep(constants.SELECTION_WAIT)
        driver.switch_to.window(driver.window_handles[1])
        if 'ddlTicketQuantity' in driver.page_source:
            driver.find_element_by_xpath('//select[@class="ddlTicketQuantity"][1]/option[@value="{0}"]'
                                         .format(people_amount)).click()
        if first_iter:
            print "Pick your seats in the browser"
            first_iter = False


    return movie_info


if __name__ == '__main__':
    main()