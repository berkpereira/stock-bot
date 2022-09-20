from db.models import Mention, db
import twitter_credentials
import tweepy
import time
from tweet_time import get_utc_datetime


# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_KEY_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)


# THIS IS THE FUNCTION WHERE WE WILL TAKE CARE OF WHAT TO DO
# TO GET THE RELEVANT OUTPUT TO TWEET DEPENDING ON SOME USER'S
# REQUEST/COMMAND TWEET
def user_command_response(tweet):
	tweet_words = tweet.text.split()
	author_name = tweet.author.name.split()[0] # tweet author's first name
	command = next(filter(lambda word: word != '@stockbot42', tweet_words), None)
	if command == None: # case where the tweet body includes the @mention and nothing else
		return f'Hi, {author_name}! If you want '



# First trial run of a basic continuously running bot operation loop
def bot_watch():
	while True:
		mentions = api.mentions_timeline(count=50) # retrieve 50 latest tweet @mentions
		for mention in mentions:
			mention_id = mention.id_str # take the mention tweet's id as a string
			search_query = Mention.select().where(Mention.tweet_id == mention_id) # search for the mention id within the bot's db
			
			# case where the mention was not found in db, i.e., not yet replied to
			# not keeping bot's own tweets in db, so we need to check for those cases too
			if search_query.count == 0 and mention.author.screen_name != 'stockbot42':
				api.update_status(status=f'Hello, {mention.user.name}!', in_reply_to_status_id=mention.id_str, auto_populate_reply_metadata=True)
				# replied_to.add(mention.id_str)
				print(f'Tweeted in response to {mention.user.screen_name}')
				time.sleep(10)
			time.sleep(10)
