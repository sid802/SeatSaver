__author__ = 'Sid'
#-*- encoding: utf-8 -*-

SELECTION_WAIT = 0.5  # in seconds

class MenuXpaths(object):
    # Contains tuples of the proper xpath and a descriptor
    cinemas = ('//select[@class="scheduleDropBox_subSite"]/option', 'cinema')
    movies = ('//select[@class="scheduleDropBox_feature"]/option', 'movie')
    dates = ('//select[@class="scheduleDropBox_date"]/option', 'date')
    times = ('//select[@class="scheduleDropBox_time"]/option', 'time')