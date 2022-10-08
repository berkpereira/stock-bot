from models import Mention
import twitter_credentials
import tweepy
import time
import yfinance as yf

# initialise tweepy api object
def init_api():
	# authenticate to twitter using credentials
	auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_KEY_SECRET)
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
	# create API object
	api = tweepy.API(auth, wait_on_rate_limit=True)
	return api

# this function takes in a tweet object, and returns what's read as the user's command to the
# bot, along with an appropriate response string to use in the bot's tweet reply
def user_command_response(tweet):
	tweet_words = tweet.text.split()
	author_name = tweet.author.name.split()[0] # tweet author's first name
	command = next(filter(lambda word: word != '@stockbot42', tweet_words), None) # this fetches the tweet's first word that isn't the @mention 
	if command != None:
		command = command.upper() # make command uppercase
	if command == 'HELP' or command == None: # case where the tweet body includes the @mention and nothing else
		response = (f'Hi, {author_name}! I can help you learn the important facts about some given ticker.\n'
					'For example, if you want to learn about the AAPL ticker, tweet "@stockbot42 AAPL"\n\n'
					"beep boop, I'm a bot")
	else: # case where user did input some attempted command, will try to find the ticker using the yfinance module
		ticker = yf.Ticker(command) # creates yfinance.Ticker object
		try: # now we try to fetch the information about the user's given ticker, assuming we find it
			isin = ticker.get_isin() # get the ticker's ISIN
			current_price = ticker.info['regularMarketPrice']
			beta = ticker.info['beta']

			# the below are 52 week target prices from multiple analysts' reports
			target_median = ticker.info['targetMedianPrice']
			no_analysts = ticker.info['numberOfAnalystOpinions'] if ticker.info['numberOfAnalystOpinions'] != None else '0'

			response = (f'Got it! Here\'s info on {command}:\n\n'
						f'Price: {current_price}\n'
						f'Beta: {beta}\n'
						f'Median price target: {target_median} (from {no_analysts} analysts)\n\n'
						"beep boop, I'm a bot")
						
		except: # if we get some error, most likely due to the ticker info not being found, we respond with an error message
			response = ('Sorry, something went wrong.\n'
						"Please make sure that you've tweeted in the correct format.\n"
						'For example, if you want to learn about the AAPL ticker, tweet "@stockbot42 AAPL"\n\n'
						"beep boop, I'm a bot")
	return command, response

# bot's operating loop
def lambda_handler(event, context):
	api = init_api()
	while True:
		mentions = api.mentions_timeline(count=10) # retrieve 10 latest tweet @mentions
		for mention in mentions:
			mention_id = mention.id_str # take the mention tweet's id as a string
			author_screen_name = mention.author.screen_name
			search_query = Mention.select().where(Mention.tweet_id == mention_id) # search for the mention id within the bot's db

			print(f'looking at tweet by {author_screen_name}: {mention.text}')
			print(f'query count: {search_query.count()}')
			print()
			# case where the mention was not found in db, i.e., not yet replied to
			# we're not keeping bot's own tweets in db, so we need to check for those cases too
			if search_query.count() == 0 and mention.author.screen_name != 'stockbot42':
				command, response = user_command_response(mention) # get the tweet's command and corresponding response
				api.update_status(status=response, in_reply_to_status_id=mention.id_str, auto_populate_reply_metadata=True)
				print(f'Tweeted in response to {mention.user.screen_name}')
				new_mention = Mention.create(tweet_id=mention_id, user_command=command, user_screen_name=author_screen_name)
				new_mention.save()
				print(f'Saved tweet {mention_id} to bot database.')
				print()
			time.sleep(5)

if __name__ == '__main__':
	# run the bot loop
	lambda_handler(event=None, context=None)