import sys
import csv
import json
import nltk
from nltk.corpus import wordnet
import re
import codecs
import operator  
from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.core import GenericPE
from dispel4py.base import IterativePE, ConsumerPE
import bisect
class ReadData(GenericPE): 
    def __init__(self):
        GenericPE.__init__(self)
        self._add_output('output')
	self.count = 0

    def process(self, inputs):
        twitterData= inputs['input']
        #self.log("Reading tweets file %s" % ROOT_DIR + twitterData)
        tweet_file = open(ROOT_DIR + twitterData)
        for line in tweet_file:
            tweet = json.loads(line)
            text = coordinates = place = location = ''
            ## Get the tweet text
            text = tweet[u'text'].encode('utf-8')
            ## Get the tweet location
            if u'coordinates' in tweet and tweet[u'coordinates']:
                coordinates = tweet[u'coordinates'][u'coordinates']
            elif u'place' in tweet and tweet[u'place']:
                place = tweet[u'place'][u'full_name'].encode('utf-8')
            elif u'user' in tweet and tweet[u'user'][u'location']:
                location = tweet[u'user'][u'location'].encode('utf-8')
 	    self.count += 1	
            return_tweet={'text':text, 'coordinates':coordinates,'place':place, 'location':location}
            self.write('output',return_tweet)
	self.log("Total tweets found %s" % self.count)

class AFINNSentimeScore(IterativePE):
    def __init__(self, sentimentData):
        IterativePE.__init__(self)
        afinnfile = open(ROOT_DIR + sentimentData)
        self.sentiment= {}
        for line in afinnfile:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            self.sentiment[term] = float(score)  # Convert the score to an integer.
	self.method = 'AFINN' 	
    def _process(self, data):
        tweet =  data
	avg_score = 0
	count = 0
        tweet_word = nltk.word_tokenize(tweet['text'])
        sent_score = 0 # sentiment score della frase
        for word in tweet_word:
             word = word.rstrip('?:!.,;"!@')
             word = word.replace("\n", "")
             if not (word.encode('utf-8', 'ignore') == ""):
                 if word.encode('utf-8') in self.sentiment.keys():
                     sent_score = sent_score + float(self.sentiment[word])
		     count += 1
	if count <> 0:	
            avg_score = sent_score/count
	else:
	    avg_score = sent_score	 	
	return(tweet, avg_score, self.method)


class PrintAFINNScore(ConsumerPE):
    def __init__(self):
        ConsumerPE.__init__(self)
    def _process(self, data):
	tweet, sent_score = data
        self.log("Tweet %s --- score %s " % ( tweet['text'], str(sent_score)))
	filename=ROOT_DIR+ "Afiinscored.txt"
	with open(filename, "a+") as results:
		results.write(tweet['text'] + " ------score: "+  str(sent_score) + "\n")
	

class FindState(IterativePE):
    def __init__(self):
        IterativePE.__init__(self)
        self.US_states={}  
        self.US_states=self.load_states("us-states.json")
    def _process(self, data):
        tweet,sent_score, method = data
        state = self.find_state(tweet)
        if state:
            self.write('output', [tweet, sent_score, state, method])
    def find_state(self, tweet):
        ## First look at the coordinates attribute
        if tweet['coordinates']:
           coord = tweet['coordinates']
           return self.coord2state(coord)
        ## Then look at the place attribute
        elif tweet[u'place']:
            place = tweet['place']
            place = " "+place+" "
            state_abbr = [s for s in self.US_states['abbr'] if " "+s+" " in place.upper()]
            if state_abbr:
                return state_abbr[0]
        ## Finally look at the user location attribute
        elif tweet[u'location']:
            location = tweet['location']
            location = " " + location + " "
            state_abbr = [s for s in self.US_states['abbr'] if " "+s+" " in location.upper()]
            state_name = [s for s in self.US_states['name'] if s.lower() in location.lower()]
            if state_abbr:
                return state_abbr[0]
            elif state_name:
                state_idx = self.US_states['name'].index(state_name[0])
                return self.US_states['abbr'][state_idx]
        return ''

    def load_states(self, us_file):
        US_states = {'name': [], 'abbr': [], 'coord': []}
        filename= ROOT_DIR + us_file
        states_file = open(filename, "r")
        features = json.load(states_file)[u'features']
        for f in features:
            US_states['name'].append(f[u'properties'][u'name'].encode('utf-8'))
            US_states['abbr'].append(f[u'properties'][u'state'].encode('utf-8'))
            coord = f[u'geometry'][u'coordinates'][0]
            if len(coord)==1: coord = coord[0]
            US_states['coord'].append(coord)
	return US_states	

    def coord2state(self,coord):
        ## Check if the given location is within the state boundaries
        picked = []
        for i in range(len(self.US_states['name'])):
            ## Calculate the boundary box of the state
            xy = self.US_states['coord'][i]
            xmin = min(xy, key=lambda x:x[0])
            xmax = max(xy, key=lambda x:x[0])
            ymin = min(xy, key=lambda x:x[1])
            ymax = max(xy, key=lambda x:x[1])
            ## Check if the location is inside the box
            if (coord[0] >= xmin) and (coord[0] <= xmax) and (coord[1] >= ymin) and (coord[1] <= ymax):
                picked.append(i)

        if len(picked) == 0:
             return ''

        if len(picked) == 1:
            return self.US_states['abbr'][picked[0]]

        ## If multiple states are found, pick the one that has
        ## the shortest distance from its center to the location
        d = []
        for k in picked:
            xcenter = 0.5 * sum(x for x,y in self.US_states['coord'][k])
            ycenter = 0.5 * sum(y for x,y in self.US_states['coord'][k])
            d.append( (x-xcenter)**2+(y-ycenter)**2 )
        idx = d.index(min(d))
        return self.US_states['abbr'][idx]


class HappyState(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_input ('input', grouping=[2,3])
        self._add_output('output')
        self.mood = {}
        self.happiest = -5000, None
    def _process(self, inputs):
        tweet, sent_score, state, method = inputs['input']
        
        if state not in self.mood:
            self.mood[state] = sent_score
        else:
            self.mood[state] +=sent_score
        
        happiest_state, happiest_score= self.happiest
        
        if self.mood[state] > happiest_score:
            happiest_score = self.mood[state]
            self.happiest = state, happiest_score 
            #self.log("!!!Happiest country is %s, score = %s"  % (state, happiest_score))
            self.write('output', [state, happiest_score,method ])

class GlobalHappyState(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_input ('input', grouping='global')
        self.state = None
        self.happiness={} #pair state, sentiment
        self.top_number = 3  
        self.top_states = []
        self.top_scores = []
	self.total_tweets = 0
    def _process(self, inputs):
        state, score, method = inputs['input']
	self.total_tweets += 1
        #self.log('new max for %s: (%s, %s)' % (method, state, score))
        self.happiness[state]=score 
        try:
            state_index = self.top_states.index(state)
            del self.top_states[state_index]
            del self.top_scores[state_index]
        except ValueError:
            pass
        index = bisect.bisect_left(self.top_scores, score)
        self.top_scores.insert(index, score)
        self.top_states.insert(index, state)
        if len(self.top_scores) > self.top_number:
            self.top_scores.pop(0)
            self.top_states.pop(0)
        self.score = self.top_scores[0]
        #self.log("country %s, score %d, len %d" % (state, self.happiness[state], len(self.happiness.keys())))
        #self.log("!!! Top countries for method %s" % method)
	count = 0
        for (score, state) in zip(self.top_scores, self.top_states):
            self.log("METHOD:%s - top:%s----> state = %s, score = %s, total_tweets = %s"  % (method, count, state, score, self.total_tweets))
            count += 1

class Tokenization_WD(IterativePE):
    def __init__(self):
        IterativePE.__init__(self)
    def _process(self, data):
        tweet = data
        tweet_tagged= self.tag_tweet(tweet['text'])
        tweet_word_def = self.wordnet_definitions(tweet_tagged)
        return (tweet_word_def, tweet)


    def tag_tweet(self, tweet):    
        sents = nltk.sent_tokenize(tweet)
        sentence = []
        for sent in sents:
            tokens = nltk.word_tokenize(sent)
            tag_tuples = nltk.pos_tag(tokens)
            for (string, tag) in tag_tuples:
                token = {'word':string, 'pos':tag}            
                sentence.append(token)    
        return sentence

    def wordnet_definitions(self,sentence):
        wnl = nltk.WordNetLemmatizer()
        for token in sentence:
            word = token['word']
            wn_pos = wordnet_pos_code(token['pos'])
            if self.is_punctuation(word):
                token['punct'] = True
            elif self.is_stopword(word):
                pass
            elif len(wordnet.synsets(word, wn_pos)) > 0:
                token['wn_lemma'] = wnl.lemmatize(word.lower())
                token['wn_pos'] = self.wordnet_pos_label(token['pos'])
                defs = [sense.definition() for sense in wordnet.synsets(word, wn_pos)]
	        token['wn_def'] = "; \n".join(defs) 	
            else:
               pass
        return sentence

    def wordnet_pos_label(self, tag):
        if tag.startswith('NN'):
            return "Noun"
        elif tag.startswith('VB'):
            return "Verb"
        elif tag.startswith('JJ'):
            return "Adjective"
        elif tag.startswith('RB'):
            return "Adverb"
        else:
            return tag

    def is_stopword(self,string):
        if string.lower() in nltk.corpus.stopwords.words('english'):
            return True
        else:
            return False

    def is_punctuation(self,string):
        for char in string:
            if char.isalpha() or char.isdigit():
                return False
        return True


class SentiWordNetScore(IterativePE):
    def __init__(self, sentimentData):
	IterativePE.__init__(self)
	self.filename= ROOT_DIR + sentimentData
        self.db = {}
        self.sentiment=self.parse_src_file()
        self.threshold = 0.87

    def _process(self,data):
	tweet_word_def , tweet = data
        obj_score = 0 # object score 
        pos_score=0 # positive score
        neg_score=0 #negative score
        pos_score_tre=0
        neg_score_tre=0
        count = 0
        count_tre = 0
        for word in tweet_word_def:
            if 'punct' not in word :
                sense = self.word_sense_disambiguate(word['word'], wordnet_pos_code(word['pos']), tweet['text'])
                if sense is not None:
                    sent = self.senti_synset(sense.name())
                    if sent is not None and sent.obj_score <> 1:
                        obj_score = obj_score + float(sent.obj_score)
                        pos_score = pos_score + float(sent.pos_score)
                        neg_score = neg_score + float(sent.neg_score)
                        count=count+1
			#self.log("pos %s, neg %s, obj %s" % (str(sent.pos_score), str(sent.neg_score), str(sent.obj_score)))
                        if sent.obj_score < self.threshold:
                            pos_score_tre = pos_score_tre + float(sent.pos_score)
                            neg_score_tre = neg_score_tre + float(sent.neg_score)
                            count_tre=count_tre+1
	
	return(tweet, pos_score_tre, neg_score_tre, count_tre)

    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(unicode.strip, fields)
            try:            
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))

    def senti_synset(self, *vals):        
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            synset = wordnet._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wordnet.synset(vals[0])
            pos = synset.pos()
            offset = synset.offset()
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wordnet.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name))
        sentis = filter(lambda x : x, sentis)
        return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.iteritems():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wordnet._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)

    def word_sense_disambiguate(self, word, wn_pos, tweet):
        senses = wordnet.synsets(word, wn_pos)
        if len(senses) >0:
            cfd = nltk.ConditionalFreqDist(
                   (sense, def_word)
                   for sense in senses
                   for def_word in sense.definition().split()
                   if def_word in tweet)
            best_sense = senses[0] # start with first sense
            for sense in senses:
                try:
                    if cfd[sense].max() > cfd[best_sense].max():
                        best_sense = sense
                except: 
                    pass                
            return best_sense
        else:
            return None

            
class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name() + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def __repr__(self):
        return "Senti" + repr(self.synset)

class ComputeSentiWordNetScore(IterativePE):
    def __init__(self):
	IterativePE.__init__(self)
	self.method = 'SWN3'
    def _process(self,data):
	#tweet, pos_score, neg_score, count, pos_score_tre, neg_score_tre, count, count_tre = data
	tweet, pos_score_tre, neg_score_tre, count_tre = data
	if count_tre <> 0:
            avg_pos_score_tre=pos_score_tre/count_tre
            avg_neg_score_tre=neg_score_tre/count_tre
	    if avg_pos_score_tre > avg_neg_score_tre:
	        sent_score = avg_pos_score_tre
	    else:
		sent_score = (avg_neg_score_tre) * (-1)
	    #self.log("sent_score %s, method %s" % (sent_score, self.method)
	    self.write('output', [tweet, sent_score,self.method])
	

# Translation from nltk to Wordnet (words tag) (code)
def wordnet_pos_code(tag):
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''


ROOT_DIR="./"	
tweets= ReadData() 
tweets.name='read'
sentiment_afinn= AFINNSentimeScore("AFINN-111.txt")            
findstate1=FindState()
findstate2=FindState()
happystate1=HappyState()
happystate2=HappyState()
findhappystate1 = GlobalHappyState()
findhappystate2 = GlobalHappyState()

preprocess_sentiword=Tokenization_WD()
sentiment_sentiword=SentiWordNetScore("SentiWordNet_3.0.0_20130122.txt")
sentiwordscore=ComputeSentiWordNetScore()

graph = WorkflowGraph()
graph.connect(tweets, 'output', sentiment_afinn, 'input')
graph.connect(sentiment_afinn, 'output', findstate1, 'input')
graph.connect(findstate1, 'output', happystate1, 'input')
graph.connect(happystate1, 'output', findhappystate1, 'input')

graph.connect(tweets, 'output', preprocess_sentiword, 'input')
graph.connect(preprocess_sentiword, 'output', sentiment_sentiword, 'input')
graph.connect(sentiment_sentiword, 'output', sentiwordscore, 'input')
graph.connect(sentiwordscore, 'output', findstate2, 'input')
graph.connect(findstate2, 'output', happystate2, 'input')
graph.connect(happystate2, 'output', findhappystate2, 'input')
