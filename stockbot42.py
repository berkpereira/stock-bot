import twitter_credentials
import tweepy
import time
from tweet_time import get_utc_datetime


# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_KEY_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Keep a register of the IDs of the tweets already responded to, avoids duplicate responses
replied_to = set()

"""
# First trial run of a basic continuously running bot operation loop
while True:
	mentions = api.mentions_timeline()
	for mention in mentions:
		if mention.id_str not in replied_to:
			api.update_status(status=f'Hello, {mention.user.name}!', in_reply_to_status_id=mention.id_str, auto_populate_reply_metadata=True)
			replied_to.add(mention.id_str)
			print(f'Tweeted in response to {mention.user.screen_name}')
			time.sleep(10)
		time.sleep(10)
"""