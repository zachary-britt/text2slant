# text2slant

## Looking for bias in news articles via NLP.

By reading in sentences from a news article into an RNN can we mathematically map the ideology of the article? The issue of bias in journalism has long been a hot button issue, but it has blown up in the Trump era with vitrolic attacks coming from the very top on political reporting.

People can manually judge bias, but it inherantly involves subjective human assessment. People have also created maps of the biases of different news sources:

![](https://i.imgur.com/kP4Yax1.png "Partisan map")

My goal is to tackle this by reading the text itself. 



### Web-scraping

The first major component of the project was data collection.

For training data I used political news articles from:

1. Right wing outlets:
	* Fox 
	* Breitbart
	* Trump election advertisements

2. Left wing outlets
	* the Huffington Post
	* Mother Jones
	* Occupy Democrats
	* Clinton election advertisements

3. Neutral outlets
	* Reuters

I also scraped
* Addicting Info (left)
and
* Gateway Pundit (right)

but left them as a holdout set.


These sources required customized web scraping [src/scrapers/](https://github.com/zachary-britt/text2slant/tree/master/src/scrapers "scrapers").

To further generalize I also downloaded a year of reddit comments and partitioned them into left wing, right wing, and non-political subreddits. The comments were filtered for length and and high score to ensure that they both fit the ethos of their subreddit and are long enough that they make sense out of context.

1. Right wing subs:
	* /r/The_Donald 
	* /r/Conservative
	* /r/Republican

2. Left wing subs
	* /r/politics
	* /r/hillaryclinton
	* /r/progressive

3. Neutral (non-political) subs
	* /r/nfl
	* /r/nhl
	* /r/nba
	* /r/baseball
	* /r/soccer
	* /r/hockey
	* /r/Fitness
	* /r/WritingPrompts
	* /r/philosophy
	* /r/askscience
	* /r/gaming


The political comments are then filtered to include at least one recognized political keyword/name, while the non-political subreddits recieve the opposite of this filter. See [src/scrapers/database_cleaning](https://github.com/zachary-britt/text2slant/blob/master/src/scrapers/database_cleaning.py "cleaning")

All of this data is saved to a mongo database for convenient storage.


### Pre-processing

The next component of the project was pre-processing the text in a way which removed any obvious "tells" as to the source of the article. The text is loaded from mongo into a pandas dataframe and then stripped of source consistent introductory/ending sentences 

e.g.: 

	"Chris Stirewalt is the politics editor for Fox News. Brianna McClelland contributed to this report. Want FOX News Halftime Report in your inbox every day? Sign up here." 
	
gets cut, along with other references to the news source. (replacing 'Fox news' with 'this newspaper' and so on) 

<br>

After links and strange introductory - conclusion punctuation are stripped, the text is checked to be at least 400 characters long to ensure the model isn't being punished for not understanding a short collection of sentence fragments.

At this stage the reddit comments are similarily also stripped of links, and the comments from political subreddits are filtered for length. See [src/formatter](https://github.com/zachary-britt/text2slant/blob/master/src/formatter.py "formatting")

### spaCy NLP

With the text obfuscated we move on to processing the text in the spaCy NLP ecosystem. Instead of relearning how to read from scratch

https://spacy.io/usage/training#section-textcat

<br>

### Model training

[src/spacy_textcat](https://github.com/zachary-britt/text2slant/blob/master/src/spacy_textcat.py "textcat")

[src/spacy_textcat](https://github.com/zachary-britt/text2slant/blob/master/src/runner_script
 "textcat")



### Model Performance 



### Model next steps:

Bin content by date and topic to leverage variance in reporting.  

By scrambling the dates and topics we lose a huge amount of valuable information. Covering Clinton scandals in November 2017 is humongously different than covering a scandal of a frontrunning presidential nominee.

