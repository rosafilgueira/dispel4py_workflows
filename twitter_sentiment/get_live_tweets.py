import oauth2 as oauth
import urllib2 as urllib
import json

## Authorization
## Values not shown for privacy
access_token_key = xxxxxxxx
access_token_secret = xxxxxxx
api_key = xxxxxxx
api_secret = xxxxxx
oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

## Send request to url
url = "https://stream.twitter.com/1.1/statuses/sample.json"
req = oauth.Request.from_consumer_and_token(oauth_consumer, token=oauth_token, 
                                            http_method="GET", http_url=url)
req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
url = req.to_url()

## Open the connection
opener = urllib.OpenerDirector()
http_handler = urllib.HTTPHandler(debuglevel=0)
https_handler = urllib.HTTPSHandler(debuglevel=0)
opener.add_handler(http_handler)
opener.add_handler(https_handler)

## Get the response
response = opener.open(url)

## Write response to file
f = open('tweets.json', 'w')
i = 0
for line in response:
    entry = json.loads(line)
    if u'lang' in entry and entry[u'lang'] == 'en' and u'text' in entry:
        special=[";",r"\r\n"]
        current=entry['text']
        for curSpec in special:
            current.replace(curSpec,"")        
        current=unicode(current.encode('utf-8'), 'ascii', 'ignore')
        entry['text']=current    
        json.dump(entry, f)
        f.write('\n')
    	i += 1
    if i > 125000:
        break
f.close()
