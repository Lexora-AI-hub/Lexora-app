from transformers import pipeline
import nltk
from nltk import sent_tokenize

# Ensure tokenizer is downloaded
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load a faster summarization model
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum", device=-1)

# Chunk text into smaller segments for speed
def chunk_text(text, max_words=80):  # Smaller = faster
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    words = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if words + word_count <= max_words:
            current_chunk.append(sentence)
            words += word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            words = word_count
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# Summarize using batch inference for speed
def summarize_text(text):
    if len(text.strip()) < 100:
        return ["Text too short to summarize."]

    chunks = chunk_text(text)

    try:
        summaries = summarizer(
            chunks,
            max_length=60,
            min_length=25,
            do_sample=False,
            truncation=True
        )
        return ["• " + s['summary_text'].strip() for s in summaries]
    except Exception as e:
        return [f"• Error summarizing: {str(e)}"]
