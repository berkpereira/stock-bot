# This function extracts the timestamp of a tweet using the
# tweet ID number
# Works for post-snowflake tweets (post 4 Nov 2010)
# Read more: https://ws-dl.blogspot.com/2019/08/2019-08-03-tweetedat-finding-tweet.html#:~:text=According%20to%20Twitter's%20post%20on,Twitter%20epoch%20time%20of%201288834974657.
def get_tweet_timestamp(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    utcdttime = datetime.utcfromtimestamp(tstamp/1000)
    print(str(tid) + " : " + str(tstamp) + " => " + str(utcdttime))