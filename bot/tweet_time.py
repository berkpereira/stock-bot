# This function extracts the UTC datetime of a tweet using the
# tweet ID number
# Works for post-snowflake tweets (post 4 Nov 2010)
# Read more: https://ws-dl.blogspot.com/2019/08/2019-08-03-tweetedat-finding-tweet.html#:~:text=According%20to%20Twitter's%20post%20on,Twitter%20epoch%20time%20of%201288834974657.
# Code source: https://github.com/oduwsdl/tweetedat
from datetime import datetime
def get_utc_datetime(tid):
    offset = 1288834974657 # tweet ID timestamp offset
    unix_tstamp = (tid >> 22) + offset
    return datetime.utcfromtimestamp(unix_tstamp/1000.0) # convert from miliseconds to seconds from epoch