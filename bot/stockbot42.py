from db.models import Mention, db
import twitter_credentials
import tweepy
import time


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
	command = next(filter(lambda word: word != '@stockbot42', tweet_words), None).upper() # this fetches the tweet's first word that isn't the @mention 
	
	if command == 'HELP' or command == None: # case where the tweet body includes the @mention and nothing else
		response = (f'Hi, {author_name}! I can help you learn the important facts about some given ticker.\n'
					'For example, if you want to learn about the AAPL ticker, tweet "@stockbot42 AAPL"\n\n'
					'beep boop, I am a bot by @berkpereira')
	else: # case where user did input some attempted command, will try to find the ticker using the yfinance module
		ticker = yf.Ticker(command)
		try:
			isin = ticker.get_isin() # this attempts to get the ticker's ISIN
			
		except:
			response = (f'Sorry, could not find the {command} ticker.\n'
						"Please make sure that you've tweeted in the correct format.\n"
						'For example, if you want to learn about the AAPL ticker, tweet "@stockbot42 AAPL"\n\n'
						'beep boop, I am a bot by @berkpereira')
						

	return response



# First trial run of a basic continuously running bot operation loop
def bot_watch():
	while True:
		mentions = api.mentions_timeline(count=50) # retrieve 50 latest tweet @mentions
		for mention in mentions:
			mention_id = mention.id_str # take the mention tweet's id as a string
			search_query = Mention.select().where(Mention.tweet_id == mention_id) # search for the mention id within the bot's db
			
			# case where the mention was not found in db, i.e., not yet replied to
			# we're not keeping bot's own tweets in db, so we need to check for those cases too
			if search_query.count == 0 and mention.author.screen_name != 'stockbot42':
				api.update_status(status=f'Hello, {mention.user.name}!', in_reply_to_status_id=mention.id_str, auto_populate_reply_metadata=True)
				# replied_to.add(mention.id_str)
				print(f'Tweeted in response to {mention.user.screen_name}')
				time.sleep(10)
			time.sleep(10)
