
from flask import*
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
model_name = "facebook/bart-large-cnn"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

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
    return summarize2(result)
  
 
def summarize2(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)

    # summarize2 function takes an input_text, tokenizes it using the specified tokenizer with certain settings 
    # (max_length and truncation), and prepares the tokenized input as PyTorch tensors (return_tensors="pt") stored 
    # in the inputs dictionary. This inputs dictionary can then be used as input to a pre-trained model for text 
    # summarization or other sequence-to-sequence tasks.

    # After executing these lines, inputs will contain a dictionary of tokenized inputs suitable 
    # for feeding directly into the pre-trained model

# tensors are fundamental data structures

   
# PyTorch tensors are multi-dimensional arrays (similar to NumPy arrays) that are used to 
# represent data in PyTorch, a popular deep learning framework
 
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
# length_penalty is a parameter used in text generation to control the length of the output sequences,
# ensuring that the generated text is of optimal length based on the specified penalty factor.
# higher value of length penality inclined to generate longer sequence


# num_beams In simple terms, num_beams in text generation is like exploring different paths or options 
# simultaneously to find the best sequence of words for a summary
# Using a higher num_beams value can increase the diversity of generated text but may require more computation.     





    return render_template("index1.html", original_text=input_text, summarized_text=summary)

if __name__ == '__main__':
    app.run(debug=True)
