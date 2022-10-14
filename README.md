# WAISE_Twitterbot

the waise chatbot is a twitterbot made by an order 2  markov chain , 
 this project is developed in python . 
 this chatbot publish periodically new tweets and reply to tweets .
 the datasets are in the directory : data , are a collection of donald trump tweets . 

- the file twitterconnexion : make the connexion to the API of twitter ( you must have a twitter  developer account ) , don't forget to enter your tokens in the file .
- the file markovstruct :  define the  structure of the markov chain that  is a dictonery ( a hashmap ) that has a key of two words and a list of the words that can be followed by this two words ... 
for exemple : 

 -for the tweet " to be or not to be ? " : 
   *to,be => [or,?]
   *be, or => [not] 
   *or,not=>[to]
 
 to build  tweets we have to select a keyword or a seed : 
  - the file extractKeywords : is to extract from a tweet the keywords of the tweet we used the tfid model .
 
 to have a good resultats we must preprocess the data : 
 - the file Preprorocessing_Dataset : proprocess the tweets by : 
     - Normalization: transform all text into lowercase.
     - Remove special characters.
     - Eliminate URLS and tags.
     - process hashtags. 
     - Treat doubling characters for exemple : haaaaapppyyy  => happy 
     - ... 
     

