import unittest
import tweepy
import requests
import json
import twitter_info

## SI 206 - W17 - HW5
## COMMENT WITH:
## Your section day/time: Fri 9 - 10
## Any names of people you worked with on this assignment: Hailey

######## 500 points total ########

## Write code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function), and prints out the Tweet text and the c value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm an awesome Python programmer.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017

## .. plus one more.

## You should cache all of the data from this exercise in a file, and submit the cache file along with your assignment. 

## So, for example, if you submit your assignment files, and you have already searched for tweets about "rock climbing", when we run your code, the code should use CACHED data, and should not need to make any new request to the Twitter API. 
## But if, for instance, you have never searched for "bicycles" before you submitted your final files, then if we enter "bicycles" when we run your code, it _should_ make a request to the Twitter API.

## The lecture notes and exercises from this week will be very helpful for this. 
## Because it is dependent on user input, there are no unit tests for this -- we will run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

## **** For 50 points of extra credit, create another file called twitter_info.py that contains your consumer_key, consumer_secret, access_token, and access_token_secret, import that file here, and use the process we discuss in class to make that information secure! Do NOT add and commit that file to a public GitHub repository.

# Information stored in twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret

#set up the authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


## **** If you choose not to do that, we strongly advise using authentication information for an 'extra' Twitter account you make just for this class, and not your personal account, because it's not ideal to share your authentication information for a real account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these with variables rather than filling in the empty strings if you choose to do the secure way for 50 EC points
#consumer_key = "" 
#consumer_secret = ""
#access_token = ""
#access_token_secret = ""
## Set up your authentication to Twitter
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) # Set up library to grab stuff from twitter with your authentication, and return it in a JSON-formatted way

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except statement shown in class.
## 2. Write a function to get twitter data that works with the caching pattern, so it either gets new data or caches data, depending upon what the input to search for is. You can model this off the class exercise from Tuesday.
## 3. Invoke your function, save the return value in a variable, and explore the data you got back!
## 4. With what you learn from the data -- e.g. how exactly to find the text of each tweet in the big nested structure -- write code to print out content from 3 tweets, as shown above.

# start out cache
CACHE_FNAME = "cached_data_socialmedia.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# get user's input for string to search for
def get_data_with_userinput():
	search_text = input("Enter the text you would like to search for: ")
	unique_identifier = "twitter_{}".format(search_text) 

	if unique_identifier in CACHE_DICTION:
		print('using cached data for', search_text)
		twitter_results = CACHE_DICTION[unique_identifier]

	else:
		print('getting data from internet for', search_text)
		twitter_results = api.search(q=search_text) # get it from the internet
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_identifier] = twitter_results # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now wi3th new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return twitter_results
	


def main():
	results = get_data_with_userinput()
	results_list = results["statuses"]
	print()
	results_list = results_list[:3]
	for tweet in results_list:
		print("TEXT: ", tweet["text"])
		print("CREATED AT: ", tweet["created_at"])
		print()

if __name__ == "__main__":
	main()
