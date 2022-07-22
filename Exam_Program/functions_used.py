import spacy
from spacy.matcher import Matcher
import pandas as pd
import random
from youtube_transcript_api import YouTubeTranscriptApi
nlp = spacy.load('en_core_web_sm')

def download_subtitles(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    df = pd.DataFrame([ (i["text"].replace("\n"," ") ,i["start"]) 
                        for i in transcript], columns=['text','start'])
    df.to_csv('Raw_Subtitles.csv')    

def time_limit(start, end):
    d = pd.read_csv('Raw_Subtitles.csv')
    between_times = ""
   
    for i in range(len(d)):
        if float( d["start"][i] ) >= float( start ):
          between_times += str( d["text"][i] )+ " "
        if float( d["start"][i] ) >= float( end ):    
            break

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(str(between_times))    
    
    df2 = pd.DataFrame([(sent.text.replace("\n", " ")) 
                        for sent in doc.sents], columns=["arrange"])
    df2.to_csv("Edit_Subtitles.csv")
            

def main_matcher():
    df = pd.read_csv('Edit_Subtitles.csv')
    
    matcher = Matcher(nlp.vocab)
    pattern = [[{"POS": "NOUN"}, {"POS": "NOUN"}],
                [{"POS": "ADJ"}, {"POS": "NOUN"}],
                [{"POS":"PROPN"},{"POS":"PROPN"}]]
    matcher.add("match", pattern)
    
    x="________"
    answers=[]
    questions=[]
    
    for i in range(len(df)):
        a=df["arrange"][i]
        doc = nlp(str(a))
        matches = matcher(doc)
        
        if len(matches) != 0:
            for i ,start,end in matches:
                    
                answers.append(doc[start:end].text)
                questions.append(str(a).replace(doc[start:end].text,x))
                       
    data=pd.DataFrame(list(zip(questions, answers)),columns =['questions', 'answers'])
    data.to_csv("Exam.csv")

def question_answer():
    
    df2 = pd.read_csv('Exam.csv')
    rand = random.sample(range(1,len(df2)), 2)
    
    index="""
    <form action = "/question_list" method = "post">
    <p>answer1:</p><p><input type = "text" name = "user_answer1" />
    <p>answer2:</p><p><input type = "text" name = "user_answer2" /></p>
    <p><input type = "submit" value = "submit" /></p>  <br></form>"""    
    
    qu1=df2["questions"][rand[0]]
    qu2=df2["questions"][rand[1]]    
        
    ans1=str(df2["answers"][rand[0]])
    ans2=str(df2["answers"][rand[1]])
    
    with open ("C:\\python\\pydosya\\templates\\questions.html","w") as f:         
        
        f.write( "<pre>"+str(rand[0])+"\t" + qu1 +"</pre> \n"+ 
                "\n<pre>" +str(rand[1])+"\t" + qu2 +"</pre> \n"+index )
    return ans1,ans2,qu1,qu2
  
