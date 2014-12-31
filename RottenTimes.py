import test
import sys
import urllib
from urllib import urlopen
import urllib2
from urllib2 import Request
from urllib2 import urlopen
import json
import webbrowser
import cookielib
from cookielib import CookieJar
import math
import test  
from bs4 import BeautifulSoup

#define the function pretty to make the information more readable
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)
    
#use urllib.urlencode() to generate the query parameter string, with one parameter: 'format', whose value is 'json'
param_str = urllib.urlencode({'format': 'json'}) 
movie_name = raw_input("Please enter the name of a movie here: ")

#Part 1. Rotten Tomatoes API

#creates the dictionary params which includes all the parameters needed to generate the Rotten Tomatoes URL address
RT_params = {}
RT_params['apikey']= 'dkpb6mkkud4qhvkg9xwuuxga'
RT_params['q'] = movie_name
RT_params['page_limit'] = 1

print '---------------'
base_RT_url = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'
RT_url = base_RT_url + "?" + urllib.urlencode(RT_params)

#opens the Rotten Tomatoes API page for that movie and prints a nicely formatted string with the film's information
open_RT_url = webbrowser.open(RT_url)
RT_result = urllib2.urlopen(RT_url).read()
RT_info_str = json.loads(RT_result)
pretty_RT_info_str = pretty(RT_info_str)
print pretty_RT_info_str

#creates a class called Movie() that contains the methods __init__(), year() for getting 
#the movie's release year, and length() for getting the movie's runtime
class Movie():
	"""object representing one movie"""
	def __init__(self, movie_name):
		self.movie_name = movie_name
	
	def year(self):
		movie_title_index = pretty_RT_info_str.find('title')
		year_index = pretty_RT_info_str.find('year')
		movie_title = pretty_RT_info_str[movie_title_index+7:year_index-3]
		release_year = pretty_RT_info_str[year_index-1:year_index+11]
		return release_year
	
	def length(self):
		runtime_index = pretty_RT_info_str.find('runtime')
		movie_runtime = pretty_RT_info_str[runtime_index-1:runtime_index+13]
		return movie_runtime

#retrieves Rotten Tomatoes' audience score for the movie
def Audience(movie_name):
	audience_ratings_link_index = pretty_RT_info_str.find('audience_score')
	audience_rating = pretty_RT_info_str[audience_ratings_link_index:audience_ratings_link_index+19]
	rotten_tomatoes_audience_score = ' "Rotten Tomatoes ' + audience_rating + "%"
	return rotten_tomatoes_audience_score
	
print Audience(movie_name)

print "Audience Test"
try:
	test.testEqual(type(rotten_tomatoes_audience_score), str)
	test.testEqual(len(rotten_tomatoes_audience_score), 21)
except:
	print "Make sure you entered the movie name correctly so the function Audience() executes properly"

#retrieves Rotten Tomatoes' critics' aggregate score for the movie
def Critics(movie_name):
	critics_ratings_link_index = pretty_RT_info_str.find('critics_score')
	critics_rating = pretty_RT_info_str[critics_ratings_link_index:critics_ratings_link_index+18]
	rotten_tomatoes_critics_score = ' "Rotten Tomatoes ' + critics_rating + "%"
	return rotten_tomatoes_critics_score
	
print Critics(movie_name)

print "Critics Test"
try:
	test.testEqual(type(rotten_tomatoes_critics_score), str)
	test.testEqual(len(rotten_tomatoes_critics_score), 21)
except:
	print "Make sure you entered the movie name correctly so the function Critics() executes properly"

#creates the dictionary params which includes all the parameters needed to generate the URL address
params = {}
params['api-key']= '9fa985e0a4edff88d171068be6f9303b:9:18769344'
params['query'] = "'" + movie_name + "'"

print "_________________________________________________________________"	
print Audience(movie_name)
print Critics(movie_name)
print "_________________________________________________________________"	

#Part 2. New York Times API

#formats the movie name that was entered in part 1 in a way that is usable in the URL
def Name(movie_name):
	lower_case_movie_name = movie_name.lower()
	URL_safe_movie_name = lower_case_movie_name.replace(" ", "+")
	NYT_movie_name = "'" + URL_safe_movie_name + "'"
	return NYT_movie_name
	
print Name(movie_name)

print "URL Safe Movie Name Test"
try:
	test.testEqual(type(NYT_movie_name), str)
	test.testEqual(NYT_movie_name.count(" "), 0)
except:
	print "Make sure you entered the name correctly so the function Name() executes properly"

#creates the dictionary params which includes all the parameters needed to generate the NYT URL address
NYT_params = {}
NYT_params['api-key'] = '8b170b9b55472a17e6121295d8959ce0:1:18769344'
NYT_params['query'] = Name(movie_name)
NYT_param_str =  urllib.urlencode(NYT_params)

baseurl = 'http://api.nytimes.com/svc/movies/v2/reviews/search.json'
url = baseurl + "?" + urllib.urlencode(params)

#opens the New York Times' API page for that movie and prints a nicely formatted string with the film's information
open_url = webbrowser.open(url)
result = urllib2.urlopen(url).read()
info_str = json.loads(result)
pretty_info_str = pretty(info_str)
#print pretty_info_str
#print type(pretty_info_str)

#finds the URL for the NYT's review of that particular movie
url_index = pretty_info_str.index("http://movies.nytimes.com")
print url_index
html_index = pretty_info_str.index(".html")
print html_index
complete_url = pretty_info_str[url_index:html_index+5]
print complete_url

#allows access to the NYT movie review 
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
request_url = urllib2.Request(complete_url)
open_url = opener.open(request_url)

#scrapes the article text from the webpage
soup = BeautifulSoup(open_url.read())
article_text = soup.get_text()
#print article_text

#creates a list to which all the words in the positive_words.txt document are appended
pos_ws = []
f = open('positive_words.txt', 'r')
for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

#creates a list to which all the words in the negative_words.txt document are appended
neg_ws = []
f = open('negative_words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))
    u = unicode(l, "utf-8")

#lists words that should not be in the neg_ws list for the specific purpose of this application
filter_words = ['2-faced', '2-faces', 'addict', 'addicts', 'callous', 'crook', 'crooks', 'die', 'dies', 'died', 'evil', 
'evils', 'illegal', 'illegally', 'illicit', 'insanity', 'invader', 'jobless', 'kill', 'killed', 'killer', 
'killing', 'kills', 'knife', 'mobster', 'murder', 'murderer', 'murderous', 'mysterious', 'mysteriously', 
'mystery', 'plot', 'premeditated', 'scare', 'scared', 'scarier', 'scariest', 'scarily', 'scars', 'scary', 'sick',
'slave', 'slaves', 'subpoena', 'subpoenas', 'tragedy', 'two-faced', 'two-faces', 'zombie']

#filters out the above words from the list neg_ws
neg_ws= filter(lambda m: m not in filter_words, neg_ws)

#splits the article text into a list of words, to which 'u' is added in order to potentially match 
#the unicode in pos_ws and neg_ws (because these words are string literals, none of them are preceded
#by 'u', and therefore would not match up with the unicode)
text_list = article_text.split(" ")
for word in text_list:
	word = "u" + word	
#print text_list

#counts the occurrences of positive words in the text of the NYT review
pos_accum = 0
for x in text_list:
	if x in pos_ws:
		pos_accum = pos_accum + 1
print pos_accum

#counts the occurrences of negative words in the text of the NYT review
neg_accum = 0
for y in text_list:
	if y in neg_ws:
		neg_accum = neg_accum + 1
print neg_accum

#generates a percentage score based on the word counts above
def NYT(movie_name):
	total_emo_words = pos_accum + neg_accum
	NYT_critics_score = 100 * pos_accum / total_emo_words
	return NYT_critics_score

#converts all the scores to integers
RT_audience_score = Audience(movie_name)
RT_audience_score = int(RT_audience_score[-3:-1])
RT_critics_score = Critics(movie_name)
RT_critics_score = int(RT_critics_score[-3:-1])
NYT_score = NYT(movie_name)

#sorts all three scores in increasing order
score_list = [RT_audience_score, RT_critics_score, NYT_score]
sorted_score_list = sorted(score_list)
print sorted_score_list

#assigns the Rotten Tomatoes critics' score a letter grade based on its percentage score
def RT_Critics_Grade(RT_critics_score):
	if RT_critics_score >= 97 and RT_critics_score <= 100:
		return "Rotten Tomatoes critics gave " + movie_name + " an A+."
	elif RT_critics_score >= 93 and RT_critics_score <= 96:
		return "Rotten Tomatoes critics gave " + movie_name + " an A."
	elif RT_critics_score >= 90 and RT_critics_score <=92:
		return "Rotten Tomatoes critics gave " + movie_name + " an A-."
	elif RT_critics_score >= 87 and RT_critics_score <= 90:
		return "Rotten Tomatoes critics gave " + movie_name + " a B+."  
	elif RT_critics_score >= 83 and RT_critics_score <= 86:
		return "Rotten Tomatoes critics gave " + movie_name + " a B."
	elif RT_critics_score >= 80 and RT_critics_score <= 82:
		return "Rotten Tomatoes critics gave " + movie_name + " a B-."
	elif RT_critics_score >= 77 and RT_critics_score <= 80:
		return "Rotten Tomatoes critics gave " + movie_name + " a C+."    
	elif RT_critics_score >= 73 and RT_critics_score <= 76:
		return "Rotten Tomatoes critics gave " + movie_name + " a C."  
	elif RT_critics_score >= 70 and RT_critics_score <= 72:
		return "Rotten Tomatoes critics gave " + movie_name + " a C-."
	elif RT_critics_score >= 67 and RT_critics_score <= 70:
		return "Rotten Tomatoes critics gave " + movie_name + " a D+."
	elif RT_critics_score >= 65 and RT_critics_score <= 67:
		return "Rotten Tomatoes critics gave " + movie_name + " a D."
	else:
		return "Rotten Tomatoes critics gave " + movie_name + " an F."
       
#assigns the Rotten Tomatoes audience score a letter grade based on its percentage score 
def RT_Audience_Grade(RT_audience_score):        
	if RT_audience_score >= 97 and RT_audience_score <= 100:
		return "Rotten Tomatoes audiences gave " + movie_name + " an A+."
	elif RT_audience_score >= 93 and RT_audience_score <= 96:
		return "Rotten Tomatoes audiences gave " + movie_name + " an A."
	elif RT_audience_score >= 90 and RT_audience_score <= 92:
		return "Rotten Tomatoes audiences gave " + movie_name + " an A-."
	elif RT_audience_score >= 87 and RT_audience_score <= 90:
		return "Rotten Tomatoes audiences gave " + movie_name + " a B+."       
	elif RT_audience_score >= 83 and RT_audience_score <= 86:
		return "Rotten Tomatoes audiences gave " + movie_name + " a B."
	elif RT_audience_score >= 80 and RT_audience_score <= 82:
		return "Rotten Tomatoes audiences gave " + movie_name + " a B-."
	elif RT_audience_score >= 77 and RT_audience_score <= 80:
		return "Rotten Tomatoes audiences gave " + movie_name + " a C+."
	elif RT_audience_score >= 73 and RT_audience_score <= 76:
		return "Rotten Tomatoes audiences gave " + movie_name + " a C."
	elif RT_audience_score >= 70 and RT_audience_score <= 72:
		return "Rotten Tomatoes audiences gave " + movie_name + " a C-."
	elif RT_audience_score >= 67 and RT_audience_score <= 70:
		return "Rotten Tomatoes audiences gave " + movie_name + " a D+."
	elif RT_audience_score >= 65 and RT_audience_score <= 67:
		return "Rotten Tomatoes audiences gave " + movie_name + " a D."    
	else:
		return "Rotten Tomatoes audiences gave " + movie_name + " an F."

#assigns the NYT critic's score a letter grade based on its percentage score
def NYT_Grade(NYT_score):   
	if NYT_score >= 97 and NYT_score <= 100:
		return "The New York Times gave " + movie_name + " an A+."
	elif NYT_score >= 93 and NYT_score <= 96:
		return "The New York Times gave " + movie_name + " an A."
	elif NYT_score >= 90 and NYT_score <= 92:
		return "The New York Times gave " + movie_name + " an A-."
	elif NYT_score >= 87 and NYT_score <= 90:
		return "The New York Times gave " + movie_name + " a B+."
	elif NYT_score >= 83 and NYT_score <= 86:
		return "The New York Times gave " + movie_name + " a B."
	elif NYT_score >= 80 and NYT_score <= 82:
		return "The New York Times gave " + movie_name + " a B-."
	elif NYT_score >= 77 and NYT_score <= 80:
		return "The New York Times gave " + movie_name + " a C+." 
	elif NYT_score >= 73 and NYT_score <= 76:
		return "The New York Times gave " + movie_name + " a C."  
	elif NYT_score >= 70 and NYT_score <= 72:
		return "The New York Times gave " + movie_name + " a C-."
	elif NYT_score >= 67 and NYT_score <= 70:
		return "The New York Times gave " + movie_name + " a D+."
	elif NYT_score >= 65 and NYT_score <= 67:
		return "The New York Times gave " + movie_name + " a D."   
	else:
		return "The New York Times gave " + movie_name + " an F."

print "_________________________________________________________________________"
print Critics(movie_name)
print Audience(movie_name)
print "The New York Times gave " + movie_name + ":"
print NYT(movie_name)
print "_________________________________________________________________________"
print movie_name + ":"
this_movie = Movie(movie_name)
print this_movie.year()
print this_movie.length() + " minutes"
print RT_Critics_Grade(RT_critics_score)
print RT_Audience_Grade(RT_audience_score)
print NYT_Grade(NYT_score)
