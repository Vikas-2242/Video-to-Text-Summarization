# from flask import*
# from transformers import pipeline
# from youtube_transcript_api import YouTubeTranscriptApi
# from IPython.display import YouTubeVideo
# import wave, math, contextlib
# import speech_recognition as sr
# from moviepy.editor import AudioFileClip
# import spacy 
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# from heapq import nlargest


# app = Flask(__name__)
# @app.route('/')  
# def upload():  
#     return render_template("index.html")  
# @app.route('/success1', methods=['POST'])



# def success1():
#     if request.method == 'POST':
#         youtube_link = request.form['youtube_link']
#         print("YouTube Link:", youtube_link)
#         text = summarize1(youtube_link)
#         return str(text) 



# def summarize1(youtube_link):
#     youtube_video = youtube_link
#     video_id = youtube_video.split("=")[1]
#     YouTubeVideo(video_id)
#     transcript= YouTubeTranscriptApi.get_transcript(video_id)
#     result = ""
#     for i in transcript:
#         result += ' ' + i['text']
#     xyz=summarize2(result,0.3)
#     return xyz

# def summarize2(text, per):
#     print("Total text of given video:\n"+text)
#     nlp = spacy.load('en_core_web_sm')  
#     doc= nlp(text)
#     tokens=[token.text for token in doc]
#     word_frequencies={}
#     for word in doc:
#         if word.text.lower() not in list(STOP_WORDS):
#             if word.text.lower() not in punctuation:
#                 if word.text not in word_frequencies.keys():
#                     word_frequencies[word.text] = 1
#                 else:
#                     word_frequencies[word.text] += 1
#     max_frequency=max(word_frequencies.values())
#     for word in word_frequencies.keys():
#         word_frequencies[word]=word_frequencies[word]/max_frequency
#     sentence_tokens= [sent for sent in doc.sents]
#     sentence_scores = {}
#     for sent in sentence_tokens:
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if sent not in sentence_scores.keys():                            
#                     sentence_scores[sent]=word_frequencies[word.text.lower()]
#                 else:
#                     sentence_scores[sent]+=word_frequencies[word.text.lower()]
#     select_length=int(len(sentence_tokens)*per)
#     summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
#     final_summary=[word.text for word in summary]
#     summary=''.join(final_summary)
#     return summary


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import*
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


app = Flask(__name__)
@app.route('/')  
def upload():  
    return render_template("index.html")  
@app.route('/success1', methods=['POST'])



def success1():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        print("YouTube Link:", youtube_link)
        text = summarize1(youtube_link)
        return str(text) 



def summarize1(youtube_link):
    youtube_video = youtube_link
    video_id = youtube_video.split("=")[1]
    YouTubeVideo(video_id)
    transcript= YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']
    return summarize2(result,0.3)
   
def summarize2(text, per):
    print("Total text of given video:\n"+text)
    nlp = spacy.load('en_core_web_sm')  
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return render_template("index1.html",original_text=text, summarized_text=summary)


if __name__ == '__main__':
    app.run(debug=True)
