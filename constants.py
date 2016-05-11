__author__ = 'Sid'
#-*- encoding: utf-8 -*-

SELECTION_WAIT = 1  # in seconds
REORDER_WAIT = 7 * 60  # In seconds
RETRY_TIME = 1.5 # in seconds

class MenuXpaths(object):
    # Contains tuples of the proper xpath and a descriptor
    cinemas = ('//select[@class="scheduleDropBox_subSite"]/option', 'cinema')
    movies = ('//select[@class="scheduleDropBox_feature"]/option', 'movie')
    dates = ('//select[@class="scheduleDropBox_date"]/option', 'date')
    times = ('//select[@class="scheduleDropBox_time"]/option', 'time')
    submit = ('//input[@class="scheduleDropBox_submit"]', 'submit')
    taken_seats = ('//div[contains(@style,"SeatStatus=3")]/@id', 'seats')
    submit_seats = ('//a[contains(@id,"lnkSubmit")][1]', 'submit seats')
    submit_seat_amount = ('//input[@id="ctl00_CPH1_imgNext1"]', 'submit seat amount')
    submit_popcorn = ('//input[@id="Assets/Images/NLC/NextButton.jpg"]', 'submit popcorn')

    