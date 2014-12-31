RottenTimes
===========
RottenTimes is a movie review app that compares data from the Rotten Tomatoes API and the 
New York Times movie review API, assigning movies an overall grade. The goal is to provide
users with a quantitative version of the New York Time's wordy movie review so that they 
have more objective information available when deciding what movies to watch. In order to 
run the program, make sure positive_words.txt and negative_words.txt are both downloaded 
in the directory in which you are running RottenTimes. The user also needs to download and 
install BeautifulSoup, version 4.3.2 into the same directory, which can be found here: 
http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/.

The app works by gathering the critics' and audiences' scores directly from Rotten Tomatoes
based on reviews for whatever movie the user decides to look up. Once it gathers this 
information from Rotten Tomatoes, it then opens up the New York Times review for that same 
movie and uses BeautifulSoup to screenscrape the text from the article. From there, it iterates 
through this text, accumulating each occurence of positive and negative words in two separate 
lists. If a word is present in the positive_words.txt document, it gets counted as a positive 
word and if it is present in the negative_words.txt document, it is counted as a negative word. 
Note here that certain words are filtered out (such as "evil", "kills", "murder", "slave") 
in the hope that the app does not favor happier, lighter movies over darker dramas simply 
because objective plot description for dramas tend to include more negative words. It then 
calculates a percentage score for the movie based on the number of positive and negative words 
present in the New York Times review. Each numberical score is converted to a letter grade 
and printed for the user to see.
