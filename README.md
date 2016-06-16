# dispel4py_workflows
This repository is dedicated to store "real" workflows that we have implemented for different scientific communities ( e.g., Seismologists, Astrophysics, etc) .
Simpler dispel4py workflows can be found [here](https://github.com/rosafilgueira/dispel4py_training_material)

The dispel4py workflows stored in this repository have been presented at several conferences:
- [EGU-2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/EGU2015_OpenSource_dispel4py.pdf)
- [eScience2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/eScience2015_dispel4py.pdf) 
- [AGU2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/AGU2015_IN34A_dispel4py.pdf)

More information about these workflows can be foud [here](https://www.computer.org/csdl/proceedings/e-science/2015/9325/00/9325a454-abs.html). 

# dispel4py
dispel4py is a free and open-source Python library for describing abstract stream-based workflows for distributed data-intensive applications. It enables users to focus on their scientific methods, avoiding distracting details and retaining flexibility over the computing infrastructure they use. It delivers mappings to diverse computing infrastructures, including cloud technologies, HPC architectures and specialised data-intensive machines, to move seamlessly into production with large-scale data loads. The dispel4py system maps workflows dynamically onto multiple enactment systems, such as MPI, STORM and Multiprocessing, without users having to modify their workflows.

# Installation

Visit the [dispel4py GitHub repository](https://github.com/dispel4py/dispel4py), which contains the instructions for installing **dispel4py** 

# Training Material

For learning more about dispel4py, visit the [dispel4py training GitHub repository](), which contains several tutorial and simple workflows for starting with dispel4py

## Seismology:  Seismic Noise Cross Correlation Workflow
	
	
Earthquakes and volcanic eruptions are sometimes preceded or accompanied by changes in the geophysical properties of the Earth, 
such as wave velocities or event rates. The development of reliable risk assessment methods for these hazards requires real-time analysis of seismic data 
and truly prospective forecasting and testing to reduce bias. However, potential techniques, including seismic interferometry and 
earthquake "repeater" analysis, require a large number of waveform cross-correlations, which is computationally intensive, and is particularly challenging in real-time. 

With dispel4py we have developed the *Seismic Ambient Noise Cross-Correlation* workflow (also called the *xcorr* workflow) 
as part of the [VERCE project](http://www.verce.eu) project, which preprocesses and cross-correlates traces from several stations in real-time. 
The *xcorr* workflow consists of two main phases:

![Figure xcorr workflow](https://github.com/rosafilgueira/dispel4py_workflows/blob/master/XcorrWorkflow.pdf)

- Phase 1 -- Preprocess: Each continuous time series from a given seismic station (called a *trace*), is subject to a series of treatments. 
		The processing of each trace is independent from other traces, making this phase "embarrassingly" parallel (complexity O(n), where n is the number of stations
- Phase 2 -- Cross-Correlation  Pairs all of the stations and calculates the cross-correlation for each pair (complexity O(n2)).

**Important!** All the codes for tesing the *xcorr* workflow can be found [here](https://github.com/rosafilgueira/dispel4py_workflows/tree/master/tc_cross_correlation) repository, which includes the instructions for running it.

In this repostory I have stored the presentation [BatchVsRealTime](https://github.com/rosafilgueira/dispel4py_workflows/blob/master/BatchVsRealTime.pdf), 
that I gave in the School of GeoScience (University of Edinburgh) group, 2015,
for presenting the different options that we could use for implementing this use case in their computing resources (Terracorrelator machine).

**Note**: Recently the [Pegasus team](https://pegasus.isi.edu/) and the [dispel4py team](https://github.com/dispel4py/dispel4py) 
have  collaborated  to  enable to run the *xcorr* workflow across different computing resources (MPI cluster and Storm cluster)
collecting data from [IRIS](http://ds.iris.edu/ds/nodes/dmc/earthscope/usarray/_US-TA-operational/). For this work, we have
submitted (and run) the *preprocess* phase to a MPI cluster, and the *cross-correlation* phase to a Storm cluster. 
The streaming and the mapping to different enactment systems, such as MPI or Storm,  are managed by dispel4py, 
while the data movement between different execution computing resources (MPI cluster and Storm cluster), 
and the coordination of the workflow execution are automatically managed by Pegasus. 
And we have adopted Docker containers for implementing this work, 
because they can substantially improve computational research reproducibility.

More information about this work can be found [here](https://www.iris.edu/hq/files/agendas/2016/iris_workshop/FerreiraDaSilvaRafael.pdf)
and [pegasus_dispel4py GitHub repository](https://github.com/dispel4py/pegasus_dispel4py).

	

## Astrophysics: Internal Extinction of Galaxies Workflow

A Virtual Observatory (VO) is a network of tools and
services implementing the standards published by the International
Virtual Observatory Alliance (IVOA) to provide
transparent access to multiple archives of astronomical
data. VO services are used in Astronomy for data sharing
and serve as the main data access point for astronomical
workflows in many cases. This is the case of the workflow
presented here, which calculates the Internal Extinction of
the Galaxies from the AMIGA catalogue. This property
represents the dust extinction within the galaxies and is a
correction coefficient needed to calculate the optical luminosity
of a galaxy. 

![Figure Internal Extinction workflow](https://github.com/rosafilgueira/dispel4py_workflows/blob/master/AstroWorkflow.pdf)

This workflow first reads an input file (coordinates.txt
size 19KB) that contains the right ascension (Ra) and
declination (Dec) values for 1051 galaxies. Then 
queries a VO service for each galaxy in the input file using
the Ra and Dec values. The results of these queries are
filtered by selecting only the values
that correspond to the morphological type (Mtype) and the
apparent flattening (logr25) features of the galaxies. Finally,
their internal extinction is calculated.

**Important!** All the codes for tesing the *internal extinction* workflow can be found at [this](https://github.com/rosafilgueira/dispel4py_workflows/tree/master/internal_extinction) repository, which includes the instructions for running it.


## Social Computing: Twitter Sentiment Analysis Workflow

With over 500 million tweets per day16 and 240 million active
users who post opinions about people, events, products
or services, Twitter has become an interesting resource for
sentiment analysis . In this case study, we investigate
the benefits of dispel4py for analysing Twitter data by
implementing a basic Sentiment Analysis workflow, called
*sentiment*.

![Figure sentiment workflow](https://github.com/rosafilgueira/dispel4py_workflows/blob/master/TweetsWorkflow.pdf)

The *sentiment* workflow, first scans the tweets preprocessing the words they
contain, and then classifies each tweet based on the total
counts for positive and negative words. As the sentiment
workflow applies two analyses, different preprocessing and
classification tasks need to be performed. To classify each
tweet with the AFINN lexicon,
the sentimentAFINN PE tokenises each tweet “text” word,
and then a very rudimentary sentiment score for the tweet
is calculated by adding the score of each word. After
determining the sentiments of all tweets, they are sent to the
findState PE, which searches the US state from which the
tweet originated, and discards tweets which are not sent from
the US. The HappyState PE applies a grouping by based on
the state and aggregates the sentiment scores of tweets from
the same state, which are sent to the top3Happiest PE. This
PE applies all-to-one grouping and determines which are the
top three happiest states.

The *sentiment* workflow also calculates tweet sentiment
in parallel using the SWN3 lexicon. The tokenizationWD
PE is a composite PE, where tweet tokenisation and tagging
takes place: the tokenTweet PE splits the tweet text into tokens, the POSTagged PE
produces a part-of-speech (POS) tag as an annotation based
on the role of each word (e.g. noun, verb, adverb) and
the wordnetDef PE determines the meaning of each word
by selecting the synset that best represents the word in its
context. After pre-processing each tweet, the second phase of
the analysis is performed by the sentiment SWN3 composite
PE: the SWN3 Interpretation PE
searches the sentiment score associated with each synset in
the SWN3 lexicon, the sentimentOrientation PE gets the
positives, negatives and average scores of each term found
in a tweet and the classifySWN3Tweet PE determines the
sentiment of the tweet. After the classification, the same
procedure as before is applied to each tweet, to know which
are the three happiest states.

**Important!** All the codes for tesing the *sentiment* workflow can be found [here](https://github.com/rosafilgueira/dispel4py_workflows/tree/master/twitter_sentiment), which includes the instructions for running it.
