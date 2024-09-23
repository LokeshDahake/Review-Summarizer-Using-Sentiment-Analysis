import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

def preprocess_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return filtered_words

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    if sentiment_score > 0.05:
        sentiment = 'Positive'
    elif sentiment_score < -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return sentiment

def summarize_text(text, num_sentences):
    words = preprocess_text(text)
    freq_dist = FreqDist(words)
    sentence_scores = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq_dist[word]
                else:
                    sentence_scores[sentence] += freq_dist[word]
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    summary = ' '.join([sentence[0] for sentence in top_sentences])
    return summary

def analyze_and_summarize():
    input_text = text_area.get("1.0", tk.END)
    try:
        num_sentences = int(num_sentences_entry.get())
        if num_sentences <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid positive integer for the number of sentences.")
        return

    if input_text.strip() == "":
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    summary = summarize_text(input_text, num_sentences)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    sentiment = analyze_sentiment(input_text)
    sentiment_label.config(text="Sentiment: " + sentiment)
    
    # Display word count
    word_count = len(input_text.split())
    word_count_label.config(text=f"Word Count: {word_count}")

def clear_fields():
    text_area.delete("1.0", tk.END)
    summary_text.delete("1.0", tk.END)
    sentiment_label.config(text="")
    num_sentences_entry.delete(0, tk.END)
    word_count_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Text Analyzer and Summarizer")

# Create widgets
text_label = tk.Label(root, text="Enter the text you want to analyze and summarize:")
text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

text_area = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

num_sentences_label = tk.Label(root, text="Number of sentences in the summary:")
num_sentences_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

num_sentences_entry = tk.Entry(root, width=5)
num_sentences_entry.grid(row=2, column=1, padx=10, pady=5)

analyze_button = tk.Button(root, text="Analyze and Summarize", command=analyze_and_summarize)
analyze_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

clear_button = tk.Button(root, text="Clear Fields", command=clear_fields)
clear_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

summary_label = tk.Label(root, text="Summarized Text:")
summary_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

summary_text = scrolledtext.ScrolledText(root, width=50, height=5, wrap=tk.WORD)
summary_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

sentiment_label = tk.Label(root, text="")
sentiment_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

word_count_label = tk.Label(root, text="")
word_count_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Start the main event loop
root.mainloop()
