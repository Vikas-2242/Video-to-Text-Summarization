# from flask import *  
# app = Flask(__name__) 
 
# import wave, math, contextlib
# import speech_recognition as sr
# from moviepy.editor import AudioFileClip
# import spacy 
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# from heapq import nlargest

# def summarize(text, per):
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


# def translator(video_file_name):
#     transcribed_audio_file_name = video_file_name.split('.')[0] + ".wav"
#     audioclip = AudioFileClip(video_file_name)
#     audioclip.write_audiofile(transcribed_audio_file_name)
    
#     with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
#         frames = f.getnframes()
#         rate = f.getframerate()
#         duration = frames / float(rate)
    
#     total_duration = math.ceil(duration / 60)
#     r = sr.Recognizer()
     
#     transcribed_text = ""
    
#     for i in range(0, total_duration):
#         with sr.AudioFile(transcribed_audio_file_name) as source:
#             audio = r.record(source, offset=i * 60, duration=60)
        
#         try:
#             text = r.recognize_google(audio)
#             transcribed_text += text+ " "
#         except:
#             pass
#     return summarize (transcribed_text,0.5)
# @app.route('/')  
# def upload():  
#     return render_template("index.html")  

# @app.route('/success', methods = ['POST'])  
# def success():  
#     if request.method == 'POST':  
#         f = request.files['file']  
#         f.save(f.filename)  
#         return translator(f.filename);  

# if __name__ == '__main__':  
#     app.run(host= '0.0.0.0', debug = True)  



from flask import *  
app = Flask(__name__) 
 
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import spacy 
# it is open source nlp library designed to handle various task like tokenization pos tagging 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest



def summarize(text, per):
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
    print(summary)
    return render_template("index.html",original_text=text, summarized_text=summary)





def translator(video_file_name,percentage):
    transcribed_audio_file_name = video_file_name.split('.')[0] + ".wav"
    audioclip = AudioFileClip(video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name)
    
    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    
    total_duration = math.ceil(duration / 60)
    # print(total_duration)
    r = sr.Recognizer()
    # creates an is instance of the Recognizer class from speech_recognition
     
    transcribed_text = ""
    
    for i in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=i * 60, duration=60)  
        try:
            text = r.recognize_google(audio)
            transcribed_text += text+ " "
        except:
            pass
    return summarize(transcribed_text,percentage)

@app.route('/')  
def upload():  
    return render_template("index.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        user_number = request.form.get('user_number')
        # user_number.save()
        print(user_number)
        print(type(user_number))
        num = int(user_number)
        percentage=(num/100)
        return translator(f.filename,percentage);  
        

if __name__ == '__main__':  
    app.run(host= '0.0.0.0', debug = True)