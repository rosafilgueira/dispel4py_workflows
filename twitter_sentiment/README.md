#Social Computing: Twitter Sentiment Analysis codes 

- To collect tweets you have to execute (at the end of this file, more information is attached for collecting tweets):
	
		python get_live_tweets.py (The tweets are stored in *tweets.json* file)
	
 **Important**: In this repository we also have attached [some tweets](https://github.com/rosafilgueira/dispel4py_workflows/blob/master/twitter_sentiment/tweets.json) for trying directly the workflow without needing to execute the get_live_tweets.py script.
	
- To execute the sentiment analysis, first you need to install:

		pip install nltk numpy 

   (More information at [here](http://www.nltk.org/install.html))
	 	
- The workflow source code is analysis_sentiment.py. You could modify the ROOT_DIR if you want to indicate a different folder. 

- For executing it with the simple mapping type:
	  	
		dispel4py simple twitter/analysis_sentiment.py  -d '{"read" : [ {"input" : "tweets.json"} ]}'

## Tweets collection
 
- For collecting tweets you need a Twitter account and a Twitter application you would need:

    1.Create a Twitter application
	* Open a web browser and go to https://apps.twitter.com/app/new
    	* Sign in with your normal Twitter username and password if you are not already signed in.
    	* Enter a name, description, and temporary website (e.g. http://coming-soon.com)
    	* Read and accept the terms and conditions. Note principally that you agree not to distribute any of the raw tweet data and to delete tweets from your collection if they should be deleted from Twitter in the future.
    	* Click "Create your Twitter application"
    	* Click on the "API Keys" tab and then click "Create my access token"
    	* Wait a minute or two and press your browser's refresh button (or ctrl+r / cmd+r)
    	* You should now see new fields labeled "Access token" and "Access token secret" at the bottom of the page.
    	* You now have a Twitter application that can act on behalf of your Twitter user to read data from Twitter.

    2.Connect your Twitter application to these scripts
	* Open get_live_tweets.py and enter your information here:
		
			access_token_key = xxxxxxxx
			access_token_secret = xxxxxxx
			api_key = xxxxxxx
			api_secret = xxxxxx
