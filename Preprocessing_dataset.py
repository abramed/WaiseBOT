
# coding: utf-8

# In[1]:


import pandas as pd 
import preprocessor as p
import re
import extract_Mots_clés as keywords
from collections import OrderedDict
from nltk.corpus import wordnet,words
from os import path

'''
def Load_data(paths):
    df=pd.read_csv(r"data/all_annotated.csv",engine="python",error_bad_lines=False, index_col=None,sep=';')
    df=df[(df["Definitely English"]==1) & (df["Definitely Not English"]==0) & (df["Ambiguous"]==0) & (df["Ambiguous due to Named Entities"]==0)  ]
    print(df.shape)
    df.dropna(inplace = True)  
    print(df.shape)
    return df 
'''


# la fonction qui appel à tous le monde 

def LoadResembledData(csvpath=None):
    df_all=pd.DataFrame(index=None, columns=['tweet'], dtype=None, copy=False)
    if path.exists(csvpath) :# c'est que le prétraitement est déja fait ! 
        df_all = pd.read_csv(csvpath,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["tweet"])
        
    else : 
        paths=["data/trumptweets1205_127.csv","data/2017_01_28_trump_tweets.csv","data/2016_12_05_trumptwitterall.csv"]
        # print schema
        typedata=["trump","trump","trump"]
        df_all=LoadData(paths,typedata)
        print("aprés load ")
        print(df_all['tweet'])
        df_all=PreprocessData(df_all)
        print("aprés process ")
        print(df_all['tweet'])
        df_all.to_csv(path_or_buf=csvpath, sep=',')
        
    return df_all.tweet.tolist()
    


def LoadData(paths,typedata):
    
   
    df_all=pd.DataFrame(index=None, columns=['tweet'], dtype=None, copy=False)
    # tweet de trump ou de GOt  !! 
    i=0
    for path in paths :
        if typedata[i] == "got":
            df_temps=pd.read_csv(path,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["text"])
        else : 
            df_temps=pd.read_csv(path,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["tweet"])
            
        if typedata[i] == "got" : 
            df_temps['tweet']=df_temps['text']
        df_all=pd.concat([df_all, df_temps])
        i=i+1
    df_all.dropna(inplace = True)
    return df_all 
# read json into a dataframe


# In[2]:



def PreprocessData(df_all):
    cv,word_vector=keywords.ConstruireLeVocabulaire()
    feature_names,tfidf_transformer=keywords.TF_IDF(cv)    
    df_all['tweet'] = df_all['tweet'].apply(lambda x: CleanTweets(x,cv,feature_names,tfidf_transformer))
    return df_all 
    

def CleanTweets(text,cv,feature_names,tfidf_transformer):
    print(text)
    #enlever les urls , les mentions 
    p.set_options(p.OPT.URL,p.OPT.MENTION)
    text=text.lower()
    text= "".join(p.clean(text))
    #sa c'est pour enlever els caractére spéciaux ! 
    #text = re.sub(r'[^a-zA-Z0-9_\s!?.:,;]+', " ", text) # on sentence itself.Here I have modified RegEx to include spaces as well
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    # maintenant , on enleve les charactére '#'
    ''' Ici on doit s assurer que le mot aprés le # nest pas un mot clé  ! si cest un mot clé on le laisse on enléve que le
    # sion on enleve le hashtags ! '''
    list_hashtags=re.findall("#([^\s]+)", text)
    print(list_hashtags)
    #liste des mots importants ! parce que  ici un hashtag peut etre par exemple #is et is est un stopword ! 
    list_important_words=keywords.get_stop_words("ressources/stopwords.txt")
    for old_hashtag in list_hashtags: 
        #old_hashtag ne contient pas # donc on le met  ! 
        old_hashtag_with_hash="{}{}".format("#",old_hashtag)
        print(old_hashtag_with_hash)
        kw=keywords.getKeyWords(old_hashtag,cv,feature_names,tfidf_transformer)
        
        if kw or old_hashtag in  list_important_words: 
            # c'est un mot clé !! 
            print("c'est un mot clé ")
            text=text.replace(old_hashtag_with_hash, old_hashtag)
           
        else : 
            print("ce n'eest pas un mot clé ! ")
            text=text.replace(old_hashtag_with_hash,'')
    

    words_text=text.split()
    resultat=""
    for w in words_text :
        if  w not in words.words(): #ce n'est pas un mot anglais 
            w = re.sub(r'([a-z])\1+', r'\1' , w) # donc on enléve les caractére redondant ! 
        resultat = resultat + " "+ w
    print(resultat)
    return resultat 



# In[3]:



LoadResembledData(csvpath="data/dataset_chatbot_processed.csv")

